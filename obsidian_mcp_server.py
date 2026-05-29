#!/usr/bin/env python3
"""
Obsidian MCP Server v3
Conecta o Claude Desktop ao vault do Obsidian via FastMCP (stdio).
19 ferramentas cobrindo CRUD, busca, metadados, grafo e fluxo diário.

Configuração: defina OBSIDIAN_VAULT_PATH no ambiente ou no claude_desktop_config.json.
"""

import json
import os
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, date
from pathlib import Path
from typing import Any

try:
    import frontmatter
except ImportError:
    raise SystemExit("ERRO: pip install python-frontmatter")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise SystemExit("ERRO: pip install 'mcp[cli]>=1.3.0'")

# ---------------------------------------------------------------------------
# Configuração do vault
# ---------------------------------------------------------------------------
VAULT_PATH = Path(
    os.getenv("OBSIDIAN_VAULT_PATH", r"C:\Users\Usuário\Desktop\V1")
)
LIXO_PATH = VAULT_PATH / "🗂️ Arquivo" / "_Lixo"
INBOX_PATH = VAULT_PATH / "00_INBOX"
DIARIO_PATH = VAULT_PATH / "📓 Diário"

LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?\s*(?:\|[^\]]+)?\]\]")
TAG_RE = re.compile(
    r"(?:^|\s)#([a-zA-ZÀ-ɏ][a-zA-Z0-9À-ɏ_/\-]*)",
    re.MULTILINE,
)
TASK_RE = re.compile(r"^- \[ \] (.+)$", re.MULTILINE)

mcp = FastMCP("obsidian-v3")


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------
def _resolve(path_str: str) -> Path:
    """Aceita caminho relativo ao vault ou absoluto."""
    p = Path(path_str)
    if not p.is_absolute():
        p = VAULT_PATH / p
    if not p.suffix:
        p = p.with_suffix(".md")
    return p


def _read_note(path: Path) -> tuple[frontmatter.Post, str]:
    post = frontmatter.load(str(path))
    return post, post.content


def _all_notes() -> list[Path]:
    return [
        p for p in VAULT_PATH.rglob("*.md")
        if ".obsidian" not in p.parts and "_Lixo" not in p.parts
    ]


def _inline_tags(content: str) -> list[str]:
    return [m.group(1) for m in TAG_RE.finditer(content)]


def _outlinks(content: str) -> list[str]:
    return [m.group(1).strip() for m in LINK_RE.finditer(content)]


def _fmt_path(p: Path) -> str:
    return str(p.relative_to(VAULT_PATH)).replace("\\", "/")


# ---------------------------------------------------------------------------
# 1. ler_nota
# ---------------------------------------------------------------------------
@mcp.tool()
def ler_nota(caminho: str) -> str:
    """Retorna o conteúdo completo (frontmatter + corpo) de uma nota."""
    p = _resolve(caminho)
    if not p.exists():
        return f"ERRO: nota não encontrada — {caminho}"
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 2. criar_nota
# ---------------------------------------------------------------------------
@mcp.tool()
def criar_nota(
    titulo: str,
    conteudo: str,
    pasta: str = "00_INBOX",
    tags: list[str] | None = None,
) -> str:
    """
    Cria uma nota nova com frontmatter obrigatório (created + tags).
    Cria primeiro em 00_INBOX se pasta não for especificada.
    """
    target_dir = VAULT_PATH / pasta
    target_dir.mkdir(parents=True, exist_ok=True)

    safe_title = re.sub(r'[\\/:*?"<>|]', "", titulo)
    path = target_dir / f"{safe_title}.md"

    if path.exists():
        return f"ERRO: nota já existe — {_fmt_path(path)}"

    fm_tags = tags or []
    now = date.today().isoformat()
    body = f"---\ncreated: {now}\ntags:\n"
    for t in fm_tags:
        body += f"  - {t}\n"
    body += f"---\n\n# {titulo}\n\n{conteudo}\n"

    path.write_text(body, encoding="utf-8")
    return f"OK: nota criada em {_fmt_path(path)}"


# ---------------------------------------------------------------------------
# 3. editar_nota
# ---------------------------------------------------------------------------
@mcp.tool()
def editar_nota(caminho: str, old_text: str, new_text: str) -> str:
    """
    Substituição cirúrgica de texto numa nota (str_replace).
    Nunca reescreve o arquivo inteiro.
    """
    p = _resolve(caminho)
    if not p.exists():
        return f"ERRO: nota não encontrada — {caminho}"

    original = p.read_text(encoding="utf-8")
    if old_text not in original:
        return "ERRO: trecho não encontrado na nota — verifique espaços e quebras de linha."

    count = original.count(old_text)
    if count > 1:
        return f"ERRO: trecho encontrado {count}× — forneça mais contexto para torná-lo único."

    updated = original.replace(old_text, new_text, 1)
    p.write_text(updated, encoding="utf-8")
    return f"OK: edição aplicada em {_fmt_path(p)}"


# ---------------------------------------------------------------------------
# 4. mover_nota
# ---------------------------------------------------------------------------
@mcp.tool()
def mover_nota(origem: str, destino: str) -> str:
    """Move ou renomeia uma nota dentro do vault."""
    src = _resolve(origem)
    dst = _resolve(destino)

    if not src.exists():
        return f"ERRO: origem não encontrada — {origem}"
    if dst.exists():
        return f"ERRO: destino já existe — {_fmt_path(dst)}"

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    return f"OK: movida de {_fmt_path(src)} → {_fmt_path(dst)}"


# ---------------------------------------------------------------------------
# 5. arquivar_nota
# ---------------------------------------------------------------------------
@mcp.tool()
def arquivar_nota(caminho: str, motivo: str = "") -> str:
    """Move a nota para 🗂️ Arquivo/_Lixo/ (nunca deleta permanentemente)."""
    src = _resolve(caminho)
    if not src.exists():
        return f"ERRO: nota não encontrada — {caminho}"

    LIXO_PATH.mkdir(parents=True, exist_ok=True)
    dst = LIXO_PATH / src.name
    if dst.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = LIXO_PATH / f"{src.stem}_{stamp}{src.suffix}"

    shutil.move(str(src), str(dst))
    log = f" (motivo: {motivo})" if motivo else ""
    return f"OK: arquivada em {_fmt_path(dst)}{log}"


# ---------------------------------------------------------------------------
# 6. buscar_texto
# ---------------------------------------------------------------------------
@mcp.tool()
def buscar_texto(query: str, case_sensitive: bool = False) -> str:
    """Busca full-text em todas as notas do vault. Retorna lista com trechos."""
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(re.escape(query), flags)
    results: list[str] = []

    for p in _all_notes():
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        matches = list(pattern.finditer(text))
        if not matches:
            continue
        # Exibe o primeiro trecho com contexto de 60 chars
        m = matches[0]
        start = max(0, m.start() - 60)
        end = min(len(text), m.end() + 60)
        snippet = text[start:end].replace("\n", " ").strip()
        results.append(f"• {_fmt_path(p)} ({len(matches)}×)\n  …{snippet}…")

    if not results:
        return f"Nenhum resultado para '{query}'."
    return f"{len(results)} nota(s) encontrada(s):\n\n" + "\n\n".join(results)


# ---------------------------------------------------------------------------
# 7. buscar_por_tag
# ---------------------------------------------------------------------------
@mcp.tool()
def buscar_por_tag(tag: str) -> str:
    """Lista todas as notas que contêm determinada tag (frontmatter ou inline)."""
    tag_clean = tag.lstrip("#").lower()
    results: list[str] = []

    for p in _all_notes():
        try:
            post = frontmatter.load(str(p))
        except Exception:
            continue

        fm_tags = post.metadata.get("tags", [])
        if isinstance(fm_tags, str):
            fm_tags = [fm_tags]
        fm_tags = [str(t).lower() for t in fm_tags]

        inline = [t.lower() for t in _inline_tags(post.content)]

        if tag_clean in fm_tags or tag_clean in inline:
            results.append(f"• {_fmt_path(p)}")

    if not results:
        return f"Nenhuma nota com a tag '#{tag_clean}'."
    return f"{len(results)} nota(s) com #{tag_clean}:\n\n" + "\n".join(results)


# ---------------------------------------------------------------------------
# 8. buscar_por_data
# ---------------------------------------------------------------------------
@mcp.tool()
def buscar_por_data(data_inicio: str, data_fim: str = "") -> str:
    """
    Busca notas pelo campo 'created' no frontmatter.
    Datas no formato YYYY-MM-DD.
    """
    try:
        d_start = date.fromisoformat(data_inicio)
        d_end = date.fromisoformat(data_fim) if data_fim else date.today()
    except ValueError as e:
        return f"ERRO: formato de data inválido — {e}"

    results: list[str] = []
    for p in _all_notes():
        try:
            post = frontmatter.load(str(p))
        except Exception:
            continue

        raw = post.metadata.get("created")
        if not raw:
            continue
        try:
            created = date.fromisoformat(str(raw))
        except ValueError:
            continue

        if d_start <= created <= d_end:
            results.append(f"• {created} — {_fmt_path(p)}")

    if not results:
        return f"Nenhuma nota criada entre {data_inicio} e {data_fim or 'hoje'}."
    results.sort()
    return f"{len(results)} nota(s):\n\n" + "\n".join(results)


# ---------------------------------------------------------------------------
# 9. listar_pasta
# ---------------------------------------------------------------------------
@mcp.tool()
def listar_pasta(pasta: str = "", recursivo: bool = False) -> str:
    """Lista as notas de uma pasta do vault (raiz por padrão)."""
    base = VAULT_PATH / pasta if pasta else VAULT_PATH
    if not base.exists():
        return f"ERRO: pasta não encontrada — {pasta}"

    if recursivo:
        notes = [p for p in base.rglob("*.md") if ".obsidian" not in p.parts]
    else:
        notes = [p for p in base.glob("*.md")]

    subdirs = [p for p in base.iterdir() if p.is_dir() and not p.name.startswith(".")]

    out = [f"📁 {_fmt_path(base)}\n"]
    for d in sorted(subdirs):
        count = len(list(d.rglob("*.md")))
        out.append(f"  📂 {d.name}/  ({count} notas)")
    if subdirs:
        out.append("")
    for n in sorted(notes):
        out.append(f"  📄 {n.stem}")

    if not notes and not subdirs:
        return "Pasta vazia."
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 10. listar_backlinks
# ---------------------------------------------------------------------------
@mcp.tool()
def listar_backlinks(caminho: str) -> str:
    """Lista todas as notas que linkam para a nota especificada."""
    p = _resolve(caminho)
    target_stem = p.stem.lower()
    results: list[str] = []

    for note in _all_notes():
        if note == p:
            continue
        try:
            content = note.read_text(encoding="utf-8")
        except Exception:
            continue
        links = [l.lower() for l in _outlinks(content)]
        if target_stem in links or str(p.relative_to(VAULT_PATH)).replace("\\", "/").lower() in links:
            results.append(f"• {_fmt_path(note)}")

    if not results:
        return f"Nenhum backlink para '{p.stem}'."
    return f"{len(results)} backlink(s) para [[{p.stem}]]:\n\n" + "\n".join(results)


# ---------------------------------------------------------------------------
# 11. listar_outlinks
# ---------------------------------------------------------------------------
@mcp.tool()
def listar_outlinks(caminho: str) -> str:
    """Lista todos os links que partem da nota especificada."""
    p = _resolve(caminho)
    if not p.exists():
        return f"ERRO: nota não encontrada — {caminho}"

    content = p.read_text(encoding="utf-8")
    links = _outlinks(content)

    if not links:
        return f"'{p.stem}' não tem outlinks."

    out = [f"{len(links)} outlink(s) de [[{p.stem}]]:\n"]
    for lnk in links:
        target = VAULT_PATH / f"{lnk}.md"
        exists = "✅" if target.exists() else "⚠️ (nota não encontrada)"
        out.append(f"  • [[{lnk}]] {exists}")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 12. listar_notas_orfas
# ---------------------------------------------------------------------------
@mcp.tool()
def listar_notas_orfas() -> str:
    """Lista notas que não recebem nenhum backlink (potenciais candidatos a integrar)."""
    all_notes = _all_notes()
    linked: set[str] = set()

    for note in all_notes:
        try:
            content = note.read_text(encoding="utf-8")
        except Exception:
            continue
        for lnk in _outlinks(content):
            linked.add(lnk.lower())

    orphans = [n for n in all_notes if n.stem.lower() not in linked]

    if not orphans:
        return "Nenhuma nota órfã encontrada."
    out = [f"{len(orphans)} nota(s) sem backlinks:\n"]
    for o in sorted(orphans):
        out.append(f"  • {_fmt_path(o)}")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 13. ler_frontmatter
# ---------------------------------------------------------------------------
@mcp.tool()
def ler_frontmatter(caminho: str) -> str:
    """Retorna o frontmatter YAML de uma nota como JSON formatado."""
    p = _resolve(caminho)
    if not p.exists():
        return f"ERRO: nota não encontrada — {caminho}"

    try:
        post = frontmatter.load(str(p))
    except Exception as e:
        return f"ERRO ao parsear frontmatter: {e}"

    if not post.metadata:
        return f"'{p.stem}' não tem frontmatter."
    return json.dumps(post.metadata, ensure_ascii=False, indent=2, default=str)


# ---------------------------------------------------------------------------
# 14. atualizar_frontmatter
# ---------------------------------------------------------------------------
@mcp.tool()
def atualizar_frontmatter(caminho: str, campos: dict[str, Any]) -> str:
    """
    Atualiza ou adiciona campos no frontmatter de uma nota.
    Exemplo: campos = {"status": "revisado", "tags": ["projeto", "ativo"]}
    """
    p = _resolve(caminho)
    if not p.exists():
        return f"ERRO: nota não encontrada — {caminho}"

    try:
        post = frontmatter.load(str(p))
    except Exception as e:
        return f"ERRO ao parsear frontmatter: {e}"

    for k, v in campos.items():
        post.metadata[k] = v

    p.write_text(frontmatter.dumps(post), encoding="utf-8")
    updated = ", ".join(f"{k}={v!r}" for k, v in campos.items())
    return f"OK: frontmatter atualizado em {_fmt_path(p)} — {updated}"


# ---------------------------------------------------------------------------
# 15. listar_todas_tags
# ---------------------------------------------------------------------------
@mcp.tool()
def listar_todas_tags() -> str:
    """Lista todas as tags do vault com contagem, ordenadas por frequência."""
    counter: Counter[str] = Counter()

    for p in _all_notes():
        try:
            post = frontmatter.load(str(p))
        except Exception:
            continue

        fm = post.metadata.get("tags", [])
        if isinstance(fm, str):
            fm = [fm]
        for t in fm:
            counter[str(t).lower()] += 1

        for t in _inline_tags(post.content):
            counter[t.lower()] += 1

    if not counter:
        return "Nenhuma tag encontrada no vault."

    lines = [f"  #{tag} ({n})" for tag, n in counter.most_common()]
    return f"{len(counter)} tag(s) encontrada(s):\n\n" + "\n".join(lines)


# ---------------------------------------------------------------------------
# 16. resumo_vault
# ---------------------------------------------------------------------------
@mcp.tool()
def resumo_vault() -> str:
    """Retorna estatísticas gerais do vault: total de notas, tags, links, tamanho."""
    notes = _all_notes()
    total_chars = 0
    total_links = 0
    tag_counter: Counter[str] = Counter()
    folder_counter: Counter[str] = Counter()

    for p in notes:
        try:
            post = frontmatter.load(str(p))
        except Exception:
            continue

        content = post.content
        total_chars += len(content)
        total_links += len(_outlinks(content))

        fm = post.metadata.get("tags", [])
        if isinstance(fm, str):
            fm = [fm]
        for t in fm:
            tag_counter[str(t).lower()] += 1
        for t in _inline_tags(content):
            tag_counter[t.lower()] += 1

        rel = p.relative_to(VAULT_PATH)
        folder = rel.parts[0] if len(rel.parts) > 1 else "(raiz)"
        folder_counter[folder] += 1

    top_tags = ", ".join(f"#{t}({n})" for t, n in tag_counter.most_common(5))
    top_folders = "\n".join(
        f"  {f}: {n}" for f, n in folder_counter.most_common()
    )

    return (
        f"📊 RESUMO DO VAULT\n"
        f"  Notas totais : {len(notes)}\n"
        f"  Tags únicas  : {len(tag_counter)}\n"
        f"  Links totais : {total_links}\n"
        f"  Tamanho total: {total_chars:,} chars\n\n"
        f"Top 5 tags: {top_tags}\n\n"
        f"Notas por pasta:\n{top_folders}"
    )


# ---------------------------------------------------------------------------
# 17. gerar_indice_pasta
# ---------------------------------------------------------------------------
@mcp.tool()
def gerar_indice_pasta(pasta: str, salvar: bool = False) -> str:
    """
    Gera um índice Markdown com todas as notas de uma pasta, usando [[links]].
    Se salvar=True, grava o índice em _Index_of_<pasta>.md dentro da pasta.
    """
    base = VAULT_PATH / pasta
    if not base.exists():
        return f"ERRO: pasta não encontrada — {pasta}"

    notes = sorted(base.rglob("*.md"), key=lambda p: p.stem)
    if not notes:
        return f"Pasta '{pasta}' está vazia."

    lines = [f"# Índice — {base.name}\n", f"*Gerado em {date.today().isoformat()}*\n"]
    current_sub = None

    for note in notes:
        rel = note.relative_to(base)
        if len(rel.parts) > 1:
            sub = rel.parts[0]
            if sub != current_sub:
                current_sub = sub
                lines.append(f"\n## {sub}\n")
        else:
            if current_sub is not None:
                current_sub = None
                lines.append("")
        lines.append(f"- [[{note.stem}]]")

    index_md = "\n".join(lines)

    if salvar:
        safe = re.sub(r'[\\/:*?"<>|]', "", base.name)
        out_path = base / f"_Index_of_{safe}.md"
        out_path.write_text(index_md, encoding="utf-8")
        return f"OK: índice salvo em {_fmt_path(out_path)}\n\n{index_md}"

    return index_md


# ---------------------------------------------------------------------------
# 18. criar_entrada_diario
# ---------------------------------------------------------------------------
@mcp.tool()
def criar_entrada_diario(
    conteudo: str,
    data: str = "",
    humor: str = "",
) -> str:
    """
    Cria ou atualiza a entrada do diário do dia.
    Data no formato YYYY-MM-DD (padrão: hoje).
    """
    entry_date = date.fromisoformat(data) if data else date.today()
    DIARIO_PATH.mkdir(parents=True, exist_ok=True)

    filename = f"{entry_date.isoformat()}.md"
    path = DIARIO_PATH / filename

    if path.exists():
        # Appende ao final da nota existente
        existing = path.read_text(encoding="utf-8")
        timestamp = datetime.now().strftime("%H:%M")
        addition = f"\n\n---\n*{timestamp}*\n\n{conteudo}"
        path.write_text(existing + addition, encoding="utf-8")
        return f"OK: conteúdo adicionado em {_fmt_path(path)}"

    fm_tags = ["diario"]
    if humor:
        fm_tags.append(f"humor-{humor.lower()}")

    body = (
        f"---\n"
        f"created: {entry_date.isoformat()}\n"
        f"tags:\n"
        + "".join(f"  - {t}\n" for t in fm_tags)
        + f"---\n\n"
        f"# Diário — {entry_date.strftime('%d/%m/%Y')}\n\n"
        + (f"**Humor:** {humor}\n\n" if humor else "")
        + conteudo + "\n"
    )
    path.write_text(body, encoding="utf-8")
    return f"OK: entrada criada em {_fmt_path(path)}"


# ---------------------------------------------------------------------------
# 19. listar_tarefas
# ---------------------------------------------------------------------------
@mcp.tool()
def listar_tarefas(pasta: str = "") -> str:
    """
    Lista todas as tarefas abertas (- [ ] ...) no vault ou numa pasta específica.
    """
    base = VAULT_PATH / pasta if pasta else VAULT_PATH
    notes = [
        p for p in base.rglob("*.md")
        if ".obsidian" not in p.parts and "_Lixo" not in p.parts
    ]

    results: list[str] = []
    for p in sorted(notes):
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            continue
        tasks = TASK_RE.findall(content)
        if tasks:
            results.append(f"\n**{_fmt_path(p)}**")
            for t in tasks:
                results.append(f"  - [ ] {t}")

    if not results:
        scope = f"em '{pasta}'" if pasta else "no vault"
        return f"Nenhuma tarefa aberta {scope}."
    total = sum(1 for r in results if r.strip().startswith("- [ ]"))
    return f"{total} tarefa(s) aberta(s):\n" + "\n".join(results)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
