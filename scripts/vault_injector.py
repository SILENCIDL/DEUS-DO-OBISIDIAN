"""
vault_injector.py v2 — DEUS-DO-OBSIDIAN
=========================================
Arquitetura correta para Windows 10.

COMO FUNCIONA:
  Os logs do Claude Desktop em %APPDATA%/Claude/logs/ são logs técnicos
  do Electron (MCP startup, erros, conexões) — não contêm conversas.

  Este injector usa três fontes reais de conteúdo:

  FONTE 1 — INBOX (principal):
    Você cria um arquivo .md ou .txt em DEUS-DO-OBSIDIAN/INBOX/
    com o resumo/notas da sessão. O injector processa, classifica
    e move para o módulo correto com frontmatter completo.

  FONTE 2 — CLAUDE.AI EXPORT (quando disponível):
    claude.ai permite exportar conversas como JSON.
    Coloque o export em INBOX/ e o injector parseia automaticamente.

  FONTE 3 — MCP LOGS (filtrado):
    Extrai apenas eventos MCP relevantes dos logs técnicos
    (ferramentas usadas, erros de servidor) para registro no vault.

USO:
    python vault_injector.py                 # processa INBOX + exports
    python vault_injector.py --dry-run       # simula sem escrever
    python vault_injector.py --fonte mcp     # só loga eventos MCP
    python vault_injector.py --force         # reprocessa arquivos já injetados
    python vault_injector.py --nova-sessao   # abre editor para nova nota rápida
"""

import os
import re
import sys
import json
import shutil
import hashlib
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────

# Detecção automática: o script está em VAULT\scripts\, então o vault é o pai da pasta scripts
_SCRIPT_DIR = Path(__file__).resolve().parent
_VAULT_CANDIDATE = _SCRIPT_DIR.parent  # scripts\ está dentro do vault

# Valida: o vault tem pelo menos uma pasta de módulo conhecida
_VAULT_MARKERS = ["FOTOGRAFIA", "CODIFICAÇÃO + IA", "INBOX", "PROJETOS E IDEIAS"]
if any((_VAULT_CANDIDATE / m).exists() for m in _VAULT_MARKERS):
    VAULT_ROOT = _VAULT_CANDIDATE
else:
    # Fallback: tenta encontrar pelo nome da pasta
    for parent in _SCRIPT_DIR.parents:
        if "OBSIDIAN" in parent.name.upper() or "OBISIDIAN" in parent.name.upper():
            VAULT_ROOT = parent
            break
    else:
        # Último recurso: pasta pai do script
        VAULT_ROOT = _VAULT_CANDIDATE

INBOX         = VAULT_ROOT / "INBOX"
INJECTOR_DIR  = VAULT_ROOT / ".injector"
REGISTRY_FILE = INJECTOR_DIR / "injected.json"
LOG_FILE      = INJECTOR_DIR / "injector.log"
PROCESSED_DIR = INJECTOR_DIR / "processados"   # arquivos INBOX após injeção

# Diretório de logs do Claude Desktop (logs técnicos do Electron)
CLAUDE_LOG_DIR = Path(os.environ.get("APPDATA", "")) / "Claude" / "logs"

MODULOS = {
    "FOTOGRAFIA":        VAULT_ROOT / "FOTOGRAFIA",
    "CODIFICAÇÃO + IA":  VAULT_ROOT / "CODIFICAÇÃO + IA",
    "REDES SOCIAIS":     VAULT_ROOT / "REDES SOCIAIS",
    "SITE":              VAULT_ROOT / "SITE FOTOGRAFIA VINÍCIUS",
    "ORGANIZAÇÃO":       VAULT_ROOT / "ORGANIZAÇÃO DE ARQUIVOS",
    "PROJETOS E IDEIAS": VAULT_ROOT / "PROJETOS E IDEIAS",
    "GERAL":             INBOX,
}

KEYWORDS_MODULO = {
    "FOTOGRAFIA":        ["foto", "fotografia", "lightroom", "photoshop", "câmera",
                          "casamento", "evento", "paisagem", "street", "pedra do baú",
                          "vôlei", "capcut", "preset", "edição", "lightbox", "ensaio",
                          "filmora", "retratos", "shooting"],
    "CODIFICAÇÃO + IA":  ["python", "script", "código", "api", "mcp", "ollama",
                          "claude code", "github", "vs code", "javascript", "html",
                          "css", "obsidian mcp", "automação", "bot", "ia", "llm",
                          "gpt", "rocm", "rx 6600", "vault_injector", "watcher",
                          "task scheduler", "powershell", "json", "sqlite"],
    "REDES SOCIAIS":     ["instagram", "reels", "feed", "grid", "post", "story",
                          "hashtag", "engajamento", "carrossel", "social media",
                          "conteúdo", "caption", "workana", "fiverr", "trampos"],
    "SITE":              ["site", "website", "landing page", "tailwind", "vanilla js",
                          "playfair", "dm sans", "deploy", "portfólio",
                          "fotografia-vinicius", "domínio", "hospedagem"],
    "ORGANIZAÇÃO":       ["pasta", "arquivo", "estrutura", "backup", "organização",
                          "hdd", "rename", "sync", "gdrive", "nuvem", "diretório",
                          "onedrive", "duplicado"],
    "PROJETOS E IDEIAS": ["projeto", "ideia", "esp32", "irrigação", "geada", "padaria",
                          "cnh", "moto", "renda", "freelance", "rede de estudo",
                          "mei", "openclaw", "whatsapp bot", "planejamento",
                          "meta", "objetivo", "negócio"],
}

# ─── LOGGING ──────────────────────────────────────────────────────────────────

def setup_logging(verbose: bool = False):
    INJECTOR_DIR.mkdir(parents=True, exist_ok=True)
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8", mode="a"),
    ]
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
    )

log = logging.getLogger("vault_injector")

# ─── UTILITÁRIOS ──────────────────────────────────────────────────────────────

def garantir_estrutura():
    for pasta in MODULOS.values():
        pasta.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def hash_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    h.update(caminho.read_bytes())
    return h.hexdigest()[:16]

def carregar_registro() -> dict:
    if REGISTRY_FILE.exists():
        try:
            return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def salvar_registro(reg: dict):
    REGISTRY_FILE.write_text(
        json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8"
    )

def sanitizar_nome(texto: str) -> str:
    texto = re.sub(r'[\\/:*?"<>|]', '', texto)
    return re.sub(r'\s+', ' ', texto).strip()[:80] or "nota-sem-titulo"

# ─── CLASSIFICAÇÃO ────────────────────────────────────────────────────────────

def classificar_modulo(texto: str) -> str:
    t = texto.lower()
    pontos = {m: sum(t.count(kw) for kw in kws) for m, kws in KEYWORDS_MODULO.items()}
    melhor = max(pontos, key=pontos.get)
    return melhor if pontos[melhor] > 0 else "GERAL"

def extrair_tags(texto: str) -> list[str]:
    t = texto.lower()
    mapa = {
        "python": "python", "javascript": "js", "html": "html", "css": "css",
        "api": "api", "mcp": "mcp", "obsidian": "obsidian", "lightroom": "lightroom",
        "photoshop": "photoshop", "instagram": "instagram", "github": "github",
        "ollama": "ollama", "claude": "claude-ai", "esp32": "esp32",
        "whatsapp": "whatsapp", "tailwind": "tailwind", "python": "python",
    }
    tags = [tag for kw, tag in mapa.items() if kw in t]
    if any(w in t for w in ["erro", "bug", "fix", "não funciona", "problema"]):
        tags.append("debug")
    if any(w in t for w in ["estratégia", "plano", "planejamento", "meta", "objetivo"]):
        tags.append("estratégia")
    if any(w in t for w in ["ideia", "conceito", "brainstorm", "insight"]):
        tags.append("ideia")
    if any(w in t for w in ["tutorial", "como fazer", "passo a passo", "how to"]):
        tags.append("tutorial")
    return sorted(set(tags))[:8]

def extrair_titulo(texto: str, nome_arquivo: str = "") -> str:
    # Prioridade 1: primeira linha H1 do markdown
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha.startswith("# "):
            return sanitizar_nome(linha[2:])
    # Prioridade 2: primeira linha não vazia com conteúdo real
    for linha in texto.splitlines():
        linha = linha.strip()
        if len(linha) > 15 and not linha.startswith(("#", "---", "```", ">")):
            return sanitizar_nome(linha[:80])
    # Fallback: nome do arquivo sem extensão
    if nome_arquivo:
        return sanitizar_nome(Path(nome_arquivo).stem)
    return "Sessão Claude"

# ─── CONSTRUÇÃO DA NOTA ───────────────────────────────────────────────────────

BACKLINKS = {
    "FOTOGRAFIA":        "[[MOC-FOTOGRAFIA]]",
    "CODIFICAÇÃO + IA":  "[[MOC-CODIFICACAO-IA]]",
    "REDES SOCIAIS":     "[[MOC-REDES-SOCIAIS]]",
    "SITE":              "[[MOC-SITE]]",
    "ORGANIZAÇÃO":       "[[MOC-ORGANIZACAO]]",
    "PROJETOS E IDEIAS": "[[MOC-PROJETOS]]",
    "GERAL":             "[[INBOX]]",
}

def construir_nota(titulo: str, corpo: str, modulo: str, tags: list[str],
                   data: datetime, fonte: str = "inbox") -> str:
    tags_yaml = "\n".join(f"  - {t}" for t in tags) if tags else "  - claude-sessao"
    backlink = BACKLINKS.get(modulo, "[[INBOX]]")
    mes_log = f"[[LOG-SESSOES-{data.strftime('%Y-%m')}]]"

    return f"""---
titulo: "{titulo}"
data: {data.strftime('%Y-%m-%d')}
modulo: {modulo}
tipo: sessao-claude
fonte: {fonte}
tags:
{tags_yaml}
criado_em: {data.strftime('%Y-%m-%d %H:%M')}
injetado_por: vault_injector-v2
---

# {titulo}

> Sessão Claude · {data.strftime('%d/%m/%Y %H:%M')} · Módulo: **{modulo}**

{corpo}

---

## Referências

- {backlink}
- {mes_log}

*Gerado automaticamente pelo vault_injector.py v2*
"""

# ─── FONTE 1: INBOX (.md / .txt) ─────────────────────────────────────────────

def processar_inbox(registro: dict, dry_run: bool, force: bool) -> int:
    """Processa arquivos .md e .txt colocados manualmente no INBOX."""
    arquivos = list(INBOX.glob("*.md")) + list(INBOX.glob("*.txt"))
    # Ignora arquivos que já são notas injetadas
    arquivos = [a for a in arquivos if not a.name.startswith("_") and a.stat().st_size > 50]

    if not arquivos:
        log.info("INBOX vazio — nenhum arquivo para processar.")
        return 0

    log.info(f"INBOX: {len(arquivos)} arquivo(s) encontrado(s)")
    injetados = 0

    for arq in arquivos:
        h = hash_arquivo(arq)
        if h in registro and not force:
            log.debug(f"Pulando (já injetado): {arq.name}")
            continue

        try:
            corpo = arq.read_text(encoding="utf-8", errors="replace")
            data = datetime.fromtimestamp(arq.stat().st_mtime)
            titulo = extrair_titulo(corpo, arq.name)
            modulo = classificar_modulo(corpo)
            tags = extrair_tags(corpo)

            pasta_destino = MODULOS.get(modulo, INBOX)
            nome_nota = f"{data.strftime('%Y-%m-%d')} {titulo}.md"
            caminho_nota = pasta_destino / nome_nota

            # Evita sobrescrever
            if caminho_nota.exists() and not force:
                caminho_nota = pasta_destino / f"{data.strftime('%Y-%m-%d')} {titulo} [{h[:6]}].md"

            nota_md = construir_nota(titulo, corpo, modulo, tags, data, fonte="inbox")

            if dry_run:
                log.info(f"[DRY-RUN] {arq.name}")
                log.info(f"          → {caminho_nota}")
                log.info(f"          Módulo: {modulo} | Tags: {tags}")
            else:
                caminho_nota.write_text(nota_md, encoding="utf-8")
                # Move o original para processados/
                destino_proc = PROCESSED_DIR / f"{data.strftime('%Y%m%d_%H%M%S')}_{arq.name}"
                shutil.move(str(arq), str(destino_proc))
                registro[h] = {
                    "arquivo_nota": str(caminho_nota),
                    "arquivo_origem": str(destino_proc),
                    "data": data.isoformat(),
                    "modulo": modulo,
                    "injetado_em": datetime.now().isoformat(),
                }
                log.info(f"✓ {arq.name} → {modulo}/{nome_nota}")
            injetados += 1

        except Exception as e:
            log.error(f"Erro ao processar {arq.name}: {e}")

    return injetados

# ─── FONTE 2: EXPORT JSON DO CLAUDE.AI ───────────────────────────────────────

def processar_exports_json(registro: dict, dry_run: bool, force: bool) -> int:
    """
    Processa exports de conversa do claude.ai (formato JSON).
    Para exportar: claude.ai → ⋯ → Settings → Export data
    """
    exports = list(INBOX.glob("*.json")) + list(INBOX.glob("conversations*.json"))
    if not exports:
        return 0

    log.info(f"Exports JSON: {len(exports)} arquivo(s) encontrado(s)")
    injetados = 0

    for arq in exports:
        h = hash_arquivo(arq)
        if h in registro and not force:
            continue

        try:
            dados = json.loads(arq.read_text(encoding="utf-8"))

            # Formato de export do claude.ai
            conversas = dados if isinstance(dados, list) else dados.get("conversations", [dados])

            for conv in conversas:
                if not isinstance(conv, dict):
                    continue

                nome = conv.get("name") or conv.get("title") or "Conversa exportada"
                msgs = conv.get("chat_messages") or conv.get("messages") or []
                criado = conv.get("created_at") or conv.get("updated_at") or ""

                try:
                    data = datetime.fromisoformat(criado.replace("Z", "+00:00"))
                    data = data.replace(tzinfo=None)
                except Exception:
                    data = datetime.now()

                # Monta o corpo com as mensagens
                partes = []
                for msg in msgs:
                    role = msg.get("sender") or msg.get("role") or "?"
                    role_label = "**Você**" if role in ("human", "user") else "**Claude**"
                    content = msg.get("text") or msg.get("content") or ""
                    if isinstance(content, list):
                        content = "\n".join(
                            b.get("text", "") for b in content
                            if isinstance(b, dict) and b.get("type") == "text"
                        )
                    if content.strip():
                        partes.append(f"{role_label}\n{content.strip()}")

                if not partes:
                    continue

                corpo = "\n\n---\n\n".join(partes)
                titulo = sanitizar_nome(nome)
                modulo = classificar_modulo(corpo)
                tags = extrair_tags(corpo)

                pasta_destino = MODULOS.get(modulo, INBOX)
                nome_nota = f"{data.strftime('%Y-%m-%d')} {titulo}.md"
                caminho_nota = pasta_destino / nome_nota

                nota_md = construir_nota(titulo, corpo, modulo, tags, data, fonte="claude-export")

                if dry_run:
                    log.info(f"[DRY-RUN] Export: {titulo[:50]}")
                    log.info(f"          → {caminho_nota}")
                else:
                    caminho_nota.write_text(nota_md, encoding="utf-8")
                    log.info(f"✓ Export: {titulo[:50]} → {modulo}")
                injetados += 1

            if not dry_run:
                destino_proc = PROCESSED_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{arq.name}"
                shutil.move(str(arq), str(destino_proc))
                registro[h] = {
                    "arquivo_origem": str(destino_proc),
                    "injetado_em": datetime.now().isoformat(),
                    "fonte": "claude-export",
                }

        except Exception as e:
            log.error(f"Erro ao processar export {arq.name}: {e}")

    return injetados

# ─── FONTE 3: EVENTOS MCP DOS LOGS TÉCNICOS ───────────────────────────────────

def processar_logs_mcp(dry_run: bool) -> int:
    """
    Extrai eventos MCP relevantes dos logs técnicos do Claude Desktop.
    Útil para registrar: quais servers foram usados, erros, ferramentas chamadas.
    """
    if not CLAUDE_LOG_DIR.exists():
        log.debug(f"Logs MCP não encontrados: {CLAUDE_LOG_DIR}")
        return 0

    # Só processa logs MCP, não os logs gerais
    logs_mcp = list(CLAUDE_LOG_DIR.glob("mcp*.log")) + list(CLAUDE_LOG_DIR.glob("mcp-server-*.log"))
    if not logs_mcp:
        return 0

    eventos = []
    padrao = re.compile(r'\[(\w+)\]\s+(.+)')

    for arq_log in sorted(logs_mcp, key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
        try:
            linhas = arq_log.read_text(encoding="utf-8", errors="replace").splitlines()
            for linha in linhas[-200:]:  # últimas 200 linhas
                m = padrao.search(linha)
                if m:
                    nivel, msg = m.group(1), m.group(2)
                    # Filtra apenas eventos úteis (não startup/shutdown genéricos)
                    if any(kw in msg.lower() for kw in
                           ["tool", "error", "ferramenta", "call", "result", "obsidian"]):
                        eventos.append(f"- `[{nivel}]` {msg[:120]}")
        except Exception as e:
            log.debug(f"Erro ao ler {arq_log.name}: {e}")

    if not eventos:
        return 0

    hoje = datetime.now()
    nome_log = f"{hoje.strftime('%Y-%m-%d')} MCP Log.md"
    pasta_mcp = MODULOS["CODIFICAÇÃO + IA"]
    caminho = pasta_mcp / nome_log

    corpo = "## Eventos MCP registrados\n\n" + "\n".join(eventos[:50])
    nota = construir_nota("MCP Log", corpo, "CODIFICAÇÃO + IA",
                          ["mcp", "debug", "claude-ai"], hoje, fonte="mcp-log")

    if dry_run:
        log.info(f"[DRY-RUN] MCP log: {len(eventos)} eventos → {caminho}")
    else:
        # Append se já existe nota do dia
        if caminho.exists():
            existente = caminho.read_text(encoding="utf-8")
            caminho.write_text(existente + "\n\n---\n\n" + corpo, encoding="utf-8")
        else:
            caminho.write_text(nota, encoding="utf-8")
        log.info(f"✓ MCP log: {len(eventos)} eventos registrados")

    return 1

# ─── NOTA RÁPIDA (--nova-sessao) ─────────────────────────────────────────────

def criar_nota_rapida():
    """
    Cria um arquivo template no INBOX e abre no editor padrão.
    Preencha e salve — o injector processa na próxima execução.
    """
    agora = datetime.now()
    nome = f"sessao-{agora.strftime('%Y-%m-%d_%H%M')}.md"
    caminho = INBOX / nome

    template = f"""# Título da sessão

> Data: {agora.strftime('%d/%m/%Y %H:%M')}

## O que foi feito

(descreva o que foi desenvolvido ou discutido nesta sessão)

## Decisões tomadas

- 

## Próximos passos

- 

## Código ou comandos relevantes

```python
# cole aqui se houver
```

## Referências e links

- 
"""
    INBOX.mkdir(parents=True, exist_ok=True)
    caminho.write_text(template, encoding="utf-8")
    print(f"\n✓ Template criado: {caminho}")
    print("  Preencha, salve e feche o editor.")
    print("  Depois rode: python vault_injector.py\n")

    # Abre no editor padrão do Windows
    try:
        os.startfile(str(caminho))
    except Exception:
        try:
            subprocess.Popen(["notepad.exe", str(caminho)])
        except Exception:
            print(f"  Abra manualmente: {caminho}")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="DEUS-DO-OBSIDIAN — Vault Injector v2")
    parser.add_argument("--dry-run",     action="store_true",  help="Simula sem escrever")
    parser.add_argument("--force",       action="store_true",  help="Reprocessa já injetados")
    parser.add_argument("--verbose",     action="store_true",  help="Log detalhado")
    parser.add_argument("--nova-sessao", action="store_true",  help="Cria nota template no INBOX")
    parser.add_argument("--fonte",       choices=["inbox", "export", "mcp", "todas"],
                        default="todas", help="Fonte de dados a processar")
    args = parser.parse_args()

    setup_logging(args.verbose)

    if args.nova_sessao:
        criar_nota_rapida()
        return

    log.info("=" * 52)
    log.info("DEUS-DO-OBSIDIAN — vault_injector.py v2")
    log.info(f"Vault:  {VAULT_ROOT}")
    log.info(f"INBOX:  {INBOX}")
    log.info(f"Modo:   {'DRY-RUN' if args.dry_run else 'REAL'} | Fonte: {args.fonte}")
    log.info("=" * 52)

    if not args.dry_run:
        garantir_estrutura()

    registro = carregar_registro()
    total = 0

    if args.fonte in ("inbox", "todas"):
        total += processar_inbox(registro, args.dry_run, args.force)

    if args.fonte in ("export", "todas"):
        total += processar_exports_json(registro, args.dry_run, args.force)

    if args.fonte in ("mcp", "todas"):
        total += processar_logs_mcp(args.dry_run)

    if not args.dry_run and total > 0:
        salvar_registro(registro)

    log.info(f"\nResumo: {total} item(s) processado(s)")
    log.info("vault_injector.py v2 concluído.")

if __name__ == "__main__":
    main()