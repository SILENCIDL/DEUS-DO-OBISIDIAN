#!/usr/bin/env python3
"""
Organiza wikilinks do vault DEUS-DO-OBISIDIAN:
1. Adiciona link pai ([[_MOC-Area]]) em cada nota
2. Atualiza cada MOC com lista de notas filhas não listadas
"""

import os
import re
from pathlib import Path

VAULT = Path("/home/user/DEUS-DO-OBISIDIAN")

# Mapeamento: pasta → MOC pai
FOLDER_TO_MOC = {
    "📸 01 — FOTOGRAFIA":     "_MOC-Fotografia",
    "📱 02 — REDES & CONTEÚDO": "_MOC-Redes",
    "💼 03 — NEGÓCIOS & MARCA": "_MOC-Negocios",
    "💰 04 — FINANÇAS":        "_MOC-Financas",
    "📚 05 — ESTUDOS":         "_MOC-Estudos",
    "👕 06 — VRGS":            "_MOC-VRGS",
    "💻 07 — TECH & SISTEMAS": "_MOC-Tech",
    "🙋 08 — PESSOAL":         "_MOC-Pessoal",
    "🗂️ 09 — ARQUIVO":        "_MOC-Arquivo",
    "🔒 10 — SEGURO":          "_MOC-Vault",
    "📋 00 — SISTEMA":         "_MOC-Vault",
    # Estrutura secundária (DIREÇÃO vault)
    "01_Fotografia":            "_MOC-Fotografia",
    "02_Desenvolvimento":       "_MOC-Tech",
    "03_Idiomas":               "_MOC-Estudos",
    "04_Projetos_Pessoais":     "_MOC-Pessoal",
    "05_Redes_e_Conteudo":      "_MOC-Redes",
    "06_Negocios_e_Marca":      "_MOC-Negocios",
    "07_Financas":              "_MOC-Financas",
}

SKIP_DIRS = {"pasta do obsidian", ".git", ".obsidian", ".smart-env", ".makemd", ".space", ".injector", "memory", "scripts", "CODIFICAÇÃO + IA"}
SKIP_FILES = {"_MOC-", "ÍNDICE", "DASHBOARD", "AUDITORIA", "PADRÃO", "MAPA DE EXPANSÃO", "MOC —", "HUB-CONEXOES", "INSTRUÇÕES", "PROJETOS-ATIVOS", "PLANO-REORGANIZACAO", "VINICIUS —", "PLANEJAMENTO —", "RELATORIO", "AÇÕES-MANUAIS", "Bem-vindo", "CLAUDE", "README", "Template-"}

def should_skip_file(name: str) -> bool:
    return any(skip in name for skip in SKIP_FILES)

def get_moc_for_file(filepath: Path) -> str | None:
    """Determina o MOC pai para um arquivo baseado na pasta raiz."""
    parts = filepath.relative_to(VAULT).parts
    if not parts:
        return None
    top = parts[0]
    return FOLDER_TO_MOC.get(top)

def has_parent_link(content: str, moc: str) -> bool:
    return f"[[{moc}]]" in content

def add_parent_link(content: str, moc: str, note_name: str) -> str:
    """Adiciona link pai no final do frontmatter YAML ou no início do conteúdo."""
    pai_line = f"\n---\n*Pai: [[{moc}]]*\n"

    # Se já tem "Pai:" no final, não adiciona
    if f"*Pai: [[{moc}]]" in content or f"[[{moc}]]" in content:
        return content

    # Adiciona no final do arquivo (antes de eventual whitespace final)
    content = content.rstrip()
    # Verifica se já tem uma linha "Pai:" de outro MOC
    if "*Pai: [[" in content:
        # Substitui o pai existente
        content = re.sub(r'\n---\n\*Pai: \[\[.*?\]\]\*\n?$', pai_line, content)
    else:
        content += pai_line
    return content

def process_notes():
    """Adiciona link pai em todas as notas de conteúdo."""
    updated = []
    skipped = []

    for folder_name in FOLDER_TO_MOC:
        folder = VAULT / folder_name
        if not folder.exists():
            continue

        moc = FOLDER_TO_MOC[folder_name]

        for md_file in folder.rglob("*.md"):
            # Pula MOCs e índices
            if should_skip_file(md_file.name):
                continue
            if md_file.name.startswith("_MOC") or md_file.name.startswith("📋 ÍNDICE"):
                continue

            content = md_file.read_text(encoding="utf-8", errors="ignore")

            if has_parent_link(content, moc):
                skipped.append(md_file.name)
                continue

            new_content = add_parent_link(content, moc, md_file.stem)
            md_file.write_text(new_content, encoding="utf-8")
            updated.append(f"{folder_name}/{md_file.relative_to(folder)}")

    return updated, skipped

def get_notes_in_folder(folder: Path, moc_name: str) -> list[str]:
    """Lista todas as notas de uma pasta (excluindo MOCs e índices)."""
    notes = []
    if not folder.exists():
        return notes

    for md_file in sorted(folder.rglob("*.md")):
        if should_skip_file(md_file.name):
            continue
        if md_file.name.startswith("_MOC") or md_file.name.startswith("📋 ÍNDICE"):
            continue
        notes.append(md_file.stem)
    return notes

def update_mocs():
    """Adiciona seção de notas não listadas ao final de cada MOC."""
    results = []

    for folder_name, moc_name in FOLDER_TO_MOC.items():
        folder = VAULT / folder_name
        if not folder.exists():
            continue

        # Encontra o arquivo MOC
        moc_file = None
        for candidate in [
            VAULT / f"📸 01 — FOTOGRAFIA/_MOC-Fotografia.md",
            VAULT / f"📱 02 — REDES & CONTEÚDO/_MOC-Redes.md",
            VAULT / f"💼 03 — NEGÓCIOS & MARCA/_MOC-Negocios.md",
            VAULT / f"💰 04 — FINANÇAS/_MOC-Financas.md",
            VAULT / f"📚 05 — ESTUDOS/_MOC-Estudos.md",
            VAULT / f"👕 06 — VRGS/_MOC-VRGS.md",
            VAULT / f"💻 07 — TECH & SISTEMAS/_MOC-Tech.md",
            VAULT / f"🙋 08 — PESSOAL/_MOC-Pessoal.md",
            VAULT / f"🗂️ 09 — ARQUIVO/_MOC-Arquivo.md",
            VAULT / f"📋 00 — SISTEMA/_MOC-Vault.md",
        ]:
            if candidate.name == f"{moc_name}.md" and candidate.exists():
                moc_file = candidate
                break

        if not moc_file:
            # Tenta encontrar o MOC em qualquer lugar
            for f in VAULT.rglob(f"{moc_name}.md"):
                if ".git" not in str(f) and "pasta do obsidian" not in str(f):
                    moc_file = f
                    break

        if not moc_file or not moc_file.exists():
            continue

        moc_content = moc_file.read_text(encoding="utf-8", errors="ignore")
        all_notes = get_notes_in_folder(folder, moc_name)

        # Encontra notas que ainda não estão linkadas no MOC
        unlisted = []
        for note in all_notes:
            if f"[[{note}]]" not in moc_content and f"[[{note}|" not in moc_content:
                unlisted.append(note)

        if not unlisted:
            results.append(f"  {moc_name}: sem novas notas para adicionar")
            continue

        # Agrupa por subpasta para melhor organização
        section = "\n\n---\n\n## 📎 Notas importadas (ponto 000 / DIREÇÃO)\n\n"
        section += "\n".join(f"- [[{note}]]" for note in unlisted)
        section += "\n"

        # Adiciona a seção apenas se não existir ainda
        if "## 📎 Notas importadas" in moc_content:
            # Atualiza a seção existente
            new_links = "\n".join(f"- [[{note}]]" for note in unlisted)
            moc_content = re.sub(
                r'## 📎 Notas importadas.*?(?=\n---|\Z)',
                f"## 📎 Notas importadas (ponto 000 / DIREÇÃO)\n\n{new_links}\n",
                moc_content, flags=re.DOTALL
            )
        else:
            moc_content = moc_content.rstrip() + section

        moc_file.write_text(moc_content, encoding="utf-8")
        results.append(f"  {moc_name}: +{len(unlisted)} notas adicionadas")

    return results

def main():
    print("=" * 60)
    print("ORGANIZANDO WIKILINKS DO VAULT")
    print("=" * 60)

    print("\n[1/2] Adicionando links pai nas notas...")
    updated, skipped = process_notes()
    print(f"  ✅ Atualizadas: {len(updated)}")
    print(f"  ⏭️  Já tinham link: {len(skipped)}")
    if updated:
        for f in updated[:15]:
            print(f"     + {f}")
        if len(updated) > 15:
            print(f"     ... e mais {len(updated)-15}")

    print("\n[2/2] Atualizando MOCs com notas não listadas...")
    moc_results = update_mocs()
    for r in moc_results:
        print(r)

    print("\n✅ CONCLUÍDO!")
    print(f"   {len(updated)} notas receberam link pai")
    print(f"   MOCs atualizados com novas notas das estruturas importadas")

if __name__ == "__main__":
    main()
