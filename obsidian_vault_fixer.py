#!/usr/bin/env python3
"""
Obsidian Vault Fixer V2
Corrige os dois maiores problemas do vault:
1. Caracteres Unicode escapados (u{00e9} → é) em conteúdo de notas
2. Links internos com caminhos de pasta desnecessários
3. Links de index Zoottelkeeper apontando para caminhos antigos

Uso:
    python obsidian_vault_fixer.py
    python obsidian_vault_fixer.py --dry-run
    python obsidian_vault_fixer.py --vault-path "./pasta do obsidian/ponto 000/"
"""

import argparse
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────
# Regex patterns
# ─────────────────────────────────────────────

# Matches u{XXXX} unicode escape sequences (e.g., u{00e9} → é)
UNICODE_ESCAPE = re.compile(r"u\{([0-9a-fA-F]{4})\}")

# Matches [[folder/subfolder/NoteName]] or [[folder/subfolder/NoteName|Alias]]
LINK_WITH_PATH = re.compile(r"\[\[([^\]|]+/[^\]|]+?)(\|[^\]]+)?\]\]")

# Matches all wikilinks
ALL_LINKS = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")


class VaultFixer:
    def __init__(self, vault_path: str, dry_run: bool = False, no_backup: bool = False):
        self.vault_path = Path(vault_path).resolve()
        self.dry_run = dry_run
        self.no_backup = no_backup
        self.fixes_log: list[str] = []
        self.stats = defaultdict(int)

        # Build name index: filename (no ext) -> relative path
        self.name_to_path: dict[str, Path] = {}
        # All existing filenames (lowercase) for matching
        self.all_names: set[str] = set()
        self.all_names_original: dict[str, str] = {}  # lowercase -> original case

        if not self.vault_path.exists():
            print(f"ERRO: Caminho não encontrado: {self.vault_path}")
            raise SystemExit(1)

    def build_index(self):
        """Index all files in the vault."""
        print("📂 Indexando vault...")
        for f in self.vault_path.rglob("*"):
            rel = f.relative_to(self.vault_path)
            if any(p.startswith(".") for p in rel.parts):
                continue
            name = f.stem
            self.name_to_path[name] = rel
            self.all_names.add(name.lower())
            self.all_names_original[name.lower()] = name

        print(f"   Indexados: {len(self.name_to_path)} arquivos")

    def create_backup(self):
        """Create backup of the vault."""
        if self.no_backup or self.dry_run:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.vault_path.parent / f"vault_backup_fixer_{timestamp}"
        print(f"📦 Criando backup em: {backup_dir}")
        shutil.copytree(
            self.vault_path, backup_dir,
            ignore=shutil.ignore_patterns(".obsidian", ".git", ".makemd", ".space")
        )
        print(f"✅ Backup completo")

    def fix_unicode_escapes(self, content: str) -> tuple[str, int]:
        """Replace u{XXXX} sequences with actual Unicode characters."""
        count = 0

        def replacer(m):
            nonlocal count
            code_point = int(m.group(1), 16)
            count += 1
            return chr(code_point)

        new_content = UNICODE_ESCAPE.sub(replacer, content)
        return new_content, count

    def fix_path_links(self, content: str, note_name: str) -> tuple[str, int]:
        """Strip folder paths from links, keeping just the note name.

        [[📸 Fotografia/NOTA]] → [[NOTA]]
        [[📸 Fotografia/NOTA|Alias]] → [[NOTA|Alias]]  (keep alias)
        [[📸 Fotografia/NOTA|NOTA]] → [[NOTA]]  (remove redundant alias)

        Only fixes links where the target note exists by just its name.
        """
        count = 0

        def replacer(m):
            nonlocal count
            full_target = m.group(1)
            alias = m.group(2) or ""  # includes the | if present

            # Only process links that have a path separator
            if "/" not in full_target:
                return m.group(0)

            # Extract just the filename part
            just_name = full_target.split("/")[-1]

            # Remove .canvas extension for matching but keep for link
            match_name = just_name.replace(".canvas", "")

            # Check if the note exists by its simple name
            if match_name.lower() in self.all_names:
                actual_name = self.all_names_original[match_name.lower()]
                count += 1

                # If alias is the same as the name, remove it
                if alias:
                    alias_text = alias[1:]  # Remove leading |
                    if alias_text.strip() == actual_name or alias_text.strip() == just_name:
                        return f"[[{actual_name}]]"
                    return f"[[{actual_name}{alias}]]"
                return f"[[{actual_name}]]"

            # Also check if just_name (with .canvas) exists as a file
            if just_name.lower() in self.all_names:
                actual_name = self.all_names_original[just_name.lower()]
                count += 1
                if alias:
                    alias_text = alias[1:]
                    if alias_text.strip() == actual_name or alias_text.strip() == just_name:
                        return f"[[{actual_name}]]"
                    return f"[[{actual_name}{alias}]]"
                return f"[[{actual_name}]]"

            # Note doesn't exist by simple name, leave as is
            return m.group(0)

        new_content = LINK_WITH_PATH.sub(replacer, content)
        return new_content, count

    def fix_dot_suffix_links(self, content: str) -> tuple[str, int]:
        """Fix links ending with unnecessary dots.
        [[QUEM SOU EU.]] → [[QUEM SOU EU]] (if the note without dot exists)
        [[ESTUDOS DE FINANÇAS.]] → [[ESTUDOS DE FINANÇAS]]
        """
        count = 0

        def replacer(m):
            nonlocal count
            target = m.group(1)
            alias = m.group(2)

            # Check if target ends with a dot and note without dot exists
            if target.endswith(".") and not target.endswith(".canvas"):
                without_dot = target[:-1].strip()
                if without_dot.lower() in self.all_names:
                    actual = self.all_names_original[without_dot.lower()]
                    count += 1
                    if alias:
                        return f"[[{actual}|{alias}]]"
                    return f"[[{actual}]]"

            return m.group(0)

        new_content = ALL_LINKS.sub(replacer, content)
        return new_content, count

    def fix_zoottelkeeper_links(self, content: str) -> tuple[str, int]:
        """Fix Zoottelkeeper index links that point to old paths.

        The index files have links like [[👕 VRGS/BAGS|BAGS]]
        where BAGS was moved to 🗂️ Arquivo/VRGS-BAGS.md

        We fix these to point to the actual note name.
        """
        count = 0

        def replacer(m):
            nonlocal count
            full_target = m.group(1)
            alias = m.group(2) or ""

            if "/" not in full_target:
                return m.group(0)

            just_name = full_target.split("/")[-1]
            match_name = just_name.replace(".canvas", "")

            # Check exact match first
            if match_name.lower() in self.all_names:
                actual = self.all_names_original[match_name.lower()]
                count += 1
                if alias:
                    alias_text = alias[1:]
                    if alias_text.strip() == actual:
                        return f"[[{actual}]]"
                    return f"[[{actual}{alias}]]"
                return f"[[{actual}]]"

            # Check with common prefixes from reorganization
            # e.g., BAGS → VRGS-BAGS, COPY → NEG-COPY
            folder_name = full_target.split("/")[0]
            # Extract prefix from folder emoji name
            prefix_map = {
                "👕 VRGS": "VRGS-",
                "💼 Negócios": "NEG-",
                "💰 Finanças": "",
                "📱 Conteúdo": "CONT-",
                "📸 Fotografia": "FOTO-",
            }

            for folder_key, prefix in prefix_map.items():
                if folder_key in folder_name and prefix:
                    prefixed_name = f"{prefix}{match_name}"
                    if prefixed_name.lower() in self.all_names:
                        actual = self.all_names_original[prefixed_name.lower()]
                        count += 1
                        if alias:
                            return f"[[{actual}{alias}]]"
                        return f"[[{actual}]]"

            return m.group(0)

        new_content = LINK_WITH_PATH.sub(replacer, content)
        return new_content, count

    def process_file(self, filepath: Path) -> bool:
        """Process a single file, applying all fixes."""
        try:
            content = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            try:
                content = filepath.read_text(encoding="latin-1")
            except OSError:
                return False

        original = content
        note_name = filepath.stem
        total_fixes = 0

        # Fix 1: Unicode escapes
        content, n = self.fix_unicode_escapes(content)
        if n:
            self.stats["unicode_fixes"] += n
            total_fixes += n
            self.fixes_log.append(f"Unicode: {n} caracteres corrigidos em '{note_name}'")

        # Fix 2: Path links
        content, n = self.fix_path_links(content, note_name)
        if n:
            self.stats["path_link_fixes"] += n
            total_fixes += n

        # Fix 3: Dot suffix links
        content, n = self.fix_dot_suffix_links(content)
        if n:
            self.stats["dot_link_fixes"] += n
            total_fixes += n

        # Fix 4: Zoottelkeeper index links (only for index files)
        if note_name.startswith("_Index_of_"):
            content, n = self.fix_zoottelkeeper_links(content)
            if n:
                self.stats["zoottelkeeper_fixes"] += n
                total_fixes += n

        if content != original:
            self.stats["files_modified"] += 1
            if not self.dry_run:
                filepath.write_text(content, encoding="utf-8")
            return True
        return False

    def generate_report(self):
        """Generate a fix report."""
        report_path = self.vault_path / "📊 Relatório de Correções.md"
        now = datetime.now().strftime("%d/%m/%Y às %H:%M")

        lines = [
            "---",
            "tags: [vault, correcoes, relatorio]",
            "tipo: relatorio",
            f"date_created: {datetime.now().strftime('%Y-%m-%d')}",
            "---",
            "",
            "# 🔧 Relatório de Correções do Vault",
            "",
            f"*Gerado em {now}*",
            "",
            "---",
            "",
            "## 📊 Resumo",
            "",
            f"| Correção | Quantidade |",
            f"|----------|-----------|",
            f"| Arquivos modificados | {self.stats['files_modified']} |",
            f"| Caracteres Unicode corrigidos | {self.stats['unicode_fixes']} |",
            f"| Links com caminho de pasta corrigidos | {self.stats['path_link_fixes']} |",
            f"| Links com ponto final corrigidos | {self.stats['dot_link_fixes']} |",
            f"| Links Zoottelkeeper corrigidos | {self.stats['zoottelkeeper_fixes']} |",
            f"| **Total de correções** | **{sum(self.stats.values()) - self.stats['files_modified']}** |",
            "",
            "---",
            "",
            "## 📝 Detalhes das Correções",
            "",
            "### Unicode Escapado",
            "Caracteres como `u{00e9}` (é), `u{00f3}` (ó), `u{00e7}` (ç) foram convertidos para seus equivalentes reais.",
            "",
            "### Links com Caminho de Pasta",
            "Links como `[[📸 Fotografia/NOTA]]` foram simplificados para `[[NOTA]]` — o Obsidian resolve pelo nome do arquivo.",
            "",
            "### Links com Ponto Final",
            "Links como `[[QUEM SOU EU.]]` foram corrigidos para `[[QUEM SOU EU]]`.",
            "",
            "---",
            f"*Fim do relatório — {now}*",
        ]

        if not self.dry_run:
            report_path.write_text("\n".join(lines), encoding="utf-8")
            print(f"📊 Relatório salvo em: {report_path.name}")

    def run(self):
        """Run all fixes."""
        mode = "DRY RUN (sem modificações)" if self.dry_run else "Correção completa"
        print("=" * 55)
        print("  🔧 OBSIDIAN VAULT FIXER V2")
        print("=" * 55)
        print(f"  Vault: {self.vault_path}")
        print(f"  Modo:  {mode}")
        print("=" * 55)

        self.create_backup()
        self.build_index()

        # Process all markdown files
        md_files = list(self.vault_path.rglob("*.md"))
        md_files = [f for f in md_files if not any(p.startswith(".") for p in f.relative_to(self.vault_path).parts)]

        print(f"\n🔧 Processando {len(md_files)} arquivos...")

        for filepath in md_files:
            self.process_file(filepath)

        # Print summary
        print("\n" + "=" * 55)
        print("  📊 RESUMO DAS CORREÇÕES")
        print("=" * 55)
        print(f"  📁 Arquivos modificados:          {self.stats['files_modified']}")
        print(f"  🔤 Unicode corrigidos:             {self.stats['unicode_fixes']}")
        print(f"  📂 Links com caminho corrigidos:   {self.stats['path_link_fixes']}")
        print(f"  ⚫ Links com ponto corrigidos:     {self.stats['dot_link_fixes']}")
        print(f"  📑 Links Zoottelkeeper corrigidos: {self.stats['zoottelkeeper_fixes']}")
        total = sum(self.stats.values()) - self.stats["files_modified"]
        print(f"  ✅ Total de correções:             {total}")
        print("=" * 55)

        if self.dry_run:
            print("\n⚠️  Modo DRY RUN — nenhum arquivo foi modificado")
            print("    Execute sem --dry-run para aplicar as correções")
        else:
            self.generate_report()
            print(f"\n🎉 Concluído! {total} correções aplicadas em {self.stats['files_modified']} arquivos")


def main():
    parser = argparse.ArgumentParser(
        description="🔧 Obsidian Vault Fixer V2 — Corrige Unicode e links quebrados",
    )
    parser.add_argument(
        "--vault-path",
        default="./pasta do obsidian/ponto 000/",
        help="Caminho para o vault",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas mostra o que seria corrigido, sem modificar",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Não criar backup antes de modificar",
    )

    args = parser.parse_args()
    fixer = VaultFixer(
        vault_path=args.vault_path,
        dry_run=args.dry_run,
        no_backup=args.no_backup,
    )
    fixer.run()


if __name__ == "__main__":
    main()
