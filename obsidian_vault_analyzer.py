#!/usr/bin/env python3
"""
Obsidian Vault Analyzer & Auto-Improver
Analisa profundamente um vault do Obsidian e aplica melhorias automáticas.

Uso:
    python obsidian_vault_analyzer.py --vault-path "C:\Users\Usuário\Documents\GitHub\DEUS-DO-OBISIDIAN\pasta do obsidian\ponto 000"
    python obsidian_vault_analyzer.py --analyze-only
    python obsidian_vault_analyzer.py --no-backup
"""

import argparse
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

try:
    import frontmatter
except ImportError:
    print("ERRO: Instale python-frontmatter: pip install python-frontmatter")
    sys.exit(1)


# ─────────────────────────────────────────────
# Mapeamento de pastas para tags automáticas
# ─────────────────────────────────────────────
FOLDER_TAG_MAP = {
    "Idiomas": "idiomas",
    "Pessoal": "pessoal",
    "Saúde": "saude",
    "Rotina": "saude",
    "VRGS": "vrgs",
    "Finanças": "financas",
    "Negócios": "negocios",
    "Diário": "diario",
    "Estudos": "estudos",
    "Conteúdo": "conteudo",
    "Fotografia": "fotografia",
    "Seguro": "seguro",
    "Arquivo": "arquivo",
}

LINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?\s*(?:\|[^\]]+)?\]\]")
INLINE_TAG_PATTERN = re.compile(r"(?:^|\s)#([a-zA-Z\u00C0-\u024F][a-zA-Z0-9\u00C0-\u024F_/\-]*)", re.MULTILINE)


# ─────────────────────────────────────────────
# Classe Note
# ─────────────────────────────────────────────
@dataclass
class Note:
    path: Path
    title: str = ""
    content: str = ""
    raw_content: str = ""
    frontmatter_data: dict = field(default_factory=dict)
    has_frontmatter: bool = False
    outgoing_links: list = field(default_factory=list)
    incoming_links: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    word_count: int = 0
    is_index: bool = False
    folder: str = ""

    def __post_init__(self):
        self.title = self.path.stem

    @property
    def relative_path(self):
        return str(self.path)


# ─────────────────────────────────────────────
# Classe VaultAnalyzer
# ─────────────────────────────────────────────
class VaultAnalyzer:
    def __init__(self, vault_path: str, analyze_only: bool = False,
                 no_backup: bool = False, report_path: str = None):
        self.vault_path = Path(vault_path).resolve()
        self.analyze_only = analyze_only
        self.no_backup = no_backup
        self.report_path = Path(report_path) if report_path else self.vault_path / "📊 Relatório do Vault.md"
        self.notes: dict[str, Note] = {}  # title -> Note
        self.all_titles: set[str] = set()
        self.results: dict = {}
        self.improvements_log: list[str] = []

        if not self.vault_path.exists():
            print(f"ERRO: Caminho não encontrado: {self.vault_path}")
            sys.exit(1)

    # ─── Backup ───
    def create_backup(self):
        if self.no_backup:
            print("⏭️  Backup pulado (--no-backup)")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.vault_path.parent / f"vault_backup_{timestamp}"
        print(f"📦 Criando backup em: {backup_dir}")
        shutil.copytree(
            self.vault_path, backup_dir,
            ignore=shutil.ignore_patterns(".obsidian", ".git", ".makemd", ".space")
        )
        print(f"✅ Backup completo: {backup_dir}")
        self.improvements_log.append(f"Backup criado em `{backup_dir.name}/`")

    # ─── Carregar Notas ───
    def load_notes(self):
        print("📂 Carregando notas do vault...")
        md_files = list(self.vault_path.rglob("*.md"))
        skipped = 0
        for md_file in md_files:
            # Ignorar pastas de configuração
            rel = md_file.relative_to(self.vault_path)
            parts = rel.parts
            if any(p.startswith(".") for p in parts):
                skipped += 1
                continue

            note = Note(path=md_file)
            note.is_index = note.title.startswith("_Index_of_")
            note.folder = parts[0] if len(parts) > 1 else ""

            try:
                raw = md_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                try:
                    raw = md_file.read_text(encoding="latin-1")
                except OSError:
                    skipped += 1
                    continue

            note.raw_content = raw

            # Parse frontmatter
            try:
                post = frontmatter.loads(raw)
                if post.metadata:
                    note.has_frontmatter = True
                    note.frontmatter_data = dict(post.metadata)
                note.content = post.content
            except Exception:
                note.content = raw
                note.has_frontmatter = False

            # Extrair links
            note.outgoing_links = LINK_PATTERN.findall(raw)
            note.outgoing_links = [link.strip() for link in note.outgoing_links]

            # Extrair tags
            fm_tags = note.frontmatter_data.get("tags", [])
            if isinstance(fm_tags, str):
                fm_tags = [t.strip() for t in fm_tags.split(",")]
            elif isinstance(fm_tags, list):
                fm_tags = [str(t).strip() for t in fm_tags]
            else:
                fm_tags = []
            inline_tags = INLINE_TAG_PATTERN.findall(note.content)
            note.tags = list(set(fm_tags + inline_tags))

            # Word count
            note.word_count = len(note.content.split())

            self.notes[note.title] = note
            self.all_titles.add(note.title)

        # Calcular incoming links
        for note in self.notes.values():
            for link in note.outgoing_links:
                if link in self.notes:
                    self.notes[link].incoming_links.append(note.title)

        print(f"   Carregadas: {len(self.notes)} notas ({skipped} ignoradas)")

    # ─── ANÁLISES ───

    def analyze_structure(self):
        """Contagem de notas por pasta."""
        folder_counts = Counter()
        for note in self.notes.values():
            folder = note.folder if note.folder else "(raiz)"
            folder_counts[folder] += 1
        self.results["structure"] = dict(folder_counts.most_common())
        return self.results["structure"]

    def find_orphan_notes(self):
        """Notas sem links de entrada nem de saída."""
        orphans = []
        for note in self.notes.values():
            if note.is_index:
                continue
            if not note.outgoing_links and not note.incoming_links:
                orphans.append(note.title)
        self.results["orphans"] = orphans
        return orphans

    def find_broken_links(self):
        """Links que não apontam para nenhum arquivo existente."""
        broken = {}  # {source_title: [broken_links]}
        for note in self.notes.values():
            broken_in_note = []
            for link in note.outgoing_links:
                if link not in self.all_titles:
                    # Checar variações (com/sem extensão)
                    link_no_ext = link.replace(".md", "") if link.endswith(".md") else link
                    if link_no_ext not in self.all_titles:
                        broken_in_note.append(link)
            if broken_in_note:
                broken[note.title] = broken_in_note
        self.results["broken_links"] = broken
        return broken

    def analyze_frontmatter(self):
        """Quais notas têm/não têm frontmatter."""
        with_fm = []
        without_fm = []
        field_counts = Counter()
        for note in self.notes.values():
            if note.is_index:
                continue
            if note.has_frontmatter:
                with_fm.append(note.title)
                for key in note.frontmatter_data:
                    field_counts[key] += 1
            else:
                without_fm.append(note.title)
        self.results["frontmatter"] = {
            "with": with_fm,
            "without": without_fm,
            "field_counts": dict(field_counts.most_common()),
        }
        return self.results["frontmatter"]

    def find_empty_notes(self):
        """Notas com conteúdo muito curto."""
        empty = []  # < 50 chars
        short = []  # < 200 chars
        for note in self.notes.values():
            if note.is_index:
                continue
            content_len = len(note.content.strip())
            if content_len < 50:
                empty.append((note.title, content_len))
            elif content_len < 200:
                short.append((note.title, content_len))
        self.results["empty_notes"] = empty
        self.results["short_notes"] = short
        return empty, short

    def analyze_tags(self):
        """Análise de tags do vault."""
        all_tags = Counter()
        notes_without_tags = []
        for note in self.notes.values():
            if note.is_index:
                continue
            if note.tags:
                for tag in note.tags:
                    all_tags[tag] += 1
            else:
                notes_without_tags.append(note.title)

        # Tags usadas apenas uma vez
        orphan_tags = [tag for tag, count in all_tags.items() if count == 1]

        self.results["tags"] = {
            "all": dict(all_tags.most_common()),
            "without_tags": notes_without_tags,
            "orphan_tags": orphan_tags,
            "total_unique": len(all_tags),
        }
        return self.results["tags"]

    def analyze_link_graph(self):
        """Notas mais e menos conectadas."""
        connectivity = {}
        for note in self.notes.values():
            if note.is_index:
                continue
            total = len(set(note.outgoing_links)) + len(set(note.incoming_links))
            connectivity[note.title] = {
                "outgoing": len(set(note.outgoing_links)),
                "incoming": len(set(note.incoming_links)),
                "total": total,
            }

        sorted_conn = sorted(connectivity.items(), key=lambda x: x[1]["total"], reverse=True)
        self.results["link_graph"] = {
            "most_connected": sorted_conn[:15],
            "least_connected": [x for x in sorted_conn if x[1]["total"] == 0],
        }
        return self.results["link_graph"]

    def find_duplicates(self):
        """Detecta notas com títulos muito similares."""
        titles = [n.title for n in self.notes.values() if not n.is_index]
        duplicates = []
        seen = set()
        for i, t1 in enumerate(titles):
            for t2 in titles[i + 1:]:
                pair = tuple(sorted([t1, t2]))
                if pair in seen:
                    continue
                ratio = SequenceMatcher(None, t1.lower(), t2.lower()).ratio()
                if ratio > 0.85 and t1 != t2:
                    duplicates.append((t1, t2, round(ratio, 2)))
                    seen.add(pair)
        self.results["duplicates"] = duplicates
        return duplicates

    def check_date_formats(self):
        """Verifica inconsistências em datas no frontmatter."""
        date_formats = Counter()
        inconsistent = []
        for note in self.notes.values():
            if not note.has_frontmatter:
                continue
            for key in ["date_created", "date_modified", "updated", "date", "created"]:
                val = note.frontmatter_data.get(key)
                if val:
                    val_str = str(val)
                    if re.match(r"\d{4}-\d{2}-\d{2}", val_str):
                        date_formats["YYYY-MM-DD"] += 1
                    elif re.match(r"\d{2}\.\d{2}\.\d{4}", val_str):
                        date_formats["DD.MM.YYYY"] += 1
                    elif re.match(r"\d{2}/\d{2}/\d{4}", val_str):
                        date_formats["DD/MM/YYYY"] += 1
                    else:
                        inconsistent.append((note.title, key, val_str))
        self.results["date_formats"] = {
            "formats": dict(date_formats),
            "inconsistent": inconsistent,
        }
        return self.results["date_formats"]

    def run_all_analyses(self):
        """Executa todas as análises."""
        print("\n🔍 Executando análises...")
        self.analyze_structure()
        print("   ✓ Estrutura de pastas")
        self.find_orphan_notes()
        print(f"   ✓ Notas órfãs: {len(self.results['orphans'])}")
        self.find_broken_links()
        total_broken = sum(len(v) for v in self.results["broken_links"].values())
        print(f"   ✓ Links quebrados: {total_broken}")
        self.analyze_frontmatter()
        print(f"   ✓ Frontmatter: {len(self.results['frontmatter']['without'])} sem frontmatter")
        self.find_empty_notes()
        print(f"   ✓ Notas vazias: {len(self.results['empty_notes'])}, curtas: {len(self.results['short_notes'])}")
        self.analyze_tags()
        print(f"   ✓ Tags: {self.results['tags']['total_unique']} únicas")
        self.analyze_link_graph()
        print(f"   ✓ Grafo de links analisado")
        self.find_duplicates()
        print(f"   ✓ Possíveis duplicatas: {len(self.results['duplicates'])}")
        self.check_date_formats()
        print(f"   ✓ Formatos de data verificados")

    # ─── MELHORIAS AUTOMÁTICAS ───

    def _infer_tag_from_folder(self, folder: str) -> str:
        """Infere tag baseada no nome da pasta."""
        for keyword, tag in FOLDER_TAG_MAP.items():
            if keyword.lower() in folder.lower():
                return tag
        return ""

    def add_missing_frontmatter(self):
        """Adiciona frontmatter YAML a notas que não têm."""
        count = 0
        for note in self.notes.values():
            if note.has_frontmatter or note.is_index:
                continue

            # Pegar datas do arquivo
            try:
                stat = note.path.stat()
                created = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d")
                modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
            except OSError:
                created = modified = datetime.now().strftime("%Y-%m-%d")

            # Inferir tag da pasta
            tags = []
            inferred = self._infer_tag_from_folder(note.folder)
            if inferred:
                tags.append(inferred)

            fm = {
                "tags": tags,
                "tipo": "nota",
                "date_created": created,
                "date_modified": modified,
            }

            # Construir novo conteúdo
            new_content = f"---\ntags: {tags}\ntipo: nota\ndate_created: {created}\ndate_modified: {modified}\n---\n\n{note.raw_content}"

            note.path.write_text(new_content, encoding="utf-8")
            note.has_frontmatter = True
            note.frontmatter_data = fm
            count += 1

        if count:
            self.improvements_log.append(f"Frontmatter adicionado a {count} notas")
        print(f"   ✓ Frontmatter adicionado: {count} notas")
        return count

    def standardize_frontmatter(self):
        """Garante campos mínimos em todos os frontmatters existentes."""
        count = 0
        for note in self.notes.values():
            if not note.has_frontmatter or note.is_index:
                continue

            updated = False
            fm = note.frontmatter_data.copy()

            # Garantir campo 'tags'
            if "tags" not in fm:
                fm["tags"] = []
                updated = True

            # Garantir campo 'tipo'
            if "tipo" not in fm:
                fm["tipo"] = "nota"
                updated = True

            # Garantir 'date_modified'
            if "date_modified" not in fm and "updated" not in fm:
                try:
                    modified = datetime.fromtimestamp(note.path.stat().st_mtime).strftime("%Y-%m-%d")
                except OSError:
                    modified = datetime.now().strftime("%Y-%m-%d")
                fm["date_modified"] = modified
                updated = True

            if updated:
                try:
                    post = frontmatter.loads(note.raw_content)
                    post.metadata.update(fm)
                    new_content = frontmatter.dumps(post)
                    note.path.write_text(new_content, encoding="utf-8")
                    note.frontmatter_data = dict(post.metadata)
                    count += 1
                except Exception:
                    pass

        if count:
            self.improvements_log.append(f"Frontmatter padronizado em {count} notas")
        print(f"   ✓ Frontmatter padronizado: {count} notas")
        return count

    def fix_broken_links(self):
        """Corrige links quebrados usando fuzzy matching."""
        auto_fixed = 0
        suggestions = []

        for note_title, broken_links in self.results.get("broken_links", {}).items():
            note = self.notes.get(note_title)
            if not note:
                continue

            content = note.raw_content
            modified = False

            for broken_link in broken_links:
                best_match = None
                best_ratio = 0

                for existing_title in self.all_titles:
                    ratio = SequenceMatcher(None, broken_link.lower(), existing_title.lower()).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = existing_title

                if best_match and best_ratio >= 0.90:
                    # Correção automática
                    content = content.replace(f"[[{broken_link}]]", f"[[{best_match}]]")
                    content = re.sub(
                        rf"\[\[{re.escape(broken_link)}\|",
                        f"[[{best_match}|",
                        content,
                    )
                    modified = True
                    auto_fixed += 1
                    self.improvements_log.append(
                        f"Link corrigido: `[[{broken_link}]]` → `[[{best_match}]]` em '{note_title}'"
                    )
                elif best_match and best_ratio >= 0.70:
                    suggestions.append((note_title, broken_link, best_match, round(best_ratio, 2)))

            if modified:
                note.path.write_text(content, encoding="utf-8")

        self.results["link_suggestions"] = suggestions
        if auto_fixed:
            self.improvements_log.append(f"Total de links corrigidos automaticamente: {auto_fixed}")
        print(f"   ✓ Links corrigidos: {auto_fixed}, sugestões: {len(suggestions)}")
        return auto_fixed, suggestions

    def generate_mocs(self):
        """Cria MOC (Map of Content) para pastas sem arquivo de índice."""
        created = 0
        folders_with_notes = defaultdict(list)

        for note in self.notes.values():
            if note.folder and not note.is_index:
                folders_with_notes[note.folder].append(note)

        for folder, notes in folders_with_notes.items():
            # Verificar se já tem índice
            has_index = any(n.is_index for n in self.notes.values() if n.folder == folder)
            has_hub = any("HUB" in n.title.upper() for n in notes)

            if has_index or has_hub:
                continue

            if len(notes) < 2:
                continue

            # Gerar MOC
            folder_path = self.vault_path / folder
            clean_name = re.sub(r"^[^\w]+", "", folder).strip()
            moc_path = folder_path / f"MOC - {clean_name}.md"

            lines = [
                "---",
                f"tags: [moc, {self._infer_tag_from_folder(folder) or 'geral'}]",
                "tipo: moc",
                f"date_created: {datetime.now().strftime('%Y-%m-%d')}",
                "---",
                "",
                f"# 🗺️ MOC — {clean_name}",
                "",
                f"Mapa de conteúdo da pasta **{folder}**.",
                "",
                "---",
                "",
            ]

            sorted_notes = sorted(notes, key=lambda n: n.title)
            for note in sorted_notes:
                word_info = f"({note.word_count} palavras)" if note.word_count > 0 else "(vazia)"
                lines.append(f"- [[{note.title}]] {word_info}")

            lines.extend(["", "---", f"", f"*Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M')}*"])

            moc_path.write_text("\n".join(lines), encoding="utf-8")
            created += 1
            self.improvements_log.append(f"MOC criado: `{moc_path.name}` em `{folder}`")

        print(f"   ✓ MOCs criados: {created}")
        return created

    def add_backlinks_section(self):
        """Adiciona seção de backlinks a notas muito referenciadas."""
        added = 0
        for note in self.notes.values():
            if note.is_index:
                continue
            if len(note.incoming_links) < 3:
                continue

            # Verificar se já tem seção de backlinks
            if "## Backlinks" in note.raw_content or "## 🔗 Backlinks" in note.raw_content:
                continue

            backlinks_section = "\n\n---\n\n## 🔗 Backlinks\n\n"
            for link_title in sorted(set(note.incoming_links)):
                backlinks_section += f"- [[{link_title}]]\n"

            new_content = note.raw_content.rstrip() + backlinks_section
            note.path.write_text(new_content, encoding="utf-8")
            added += 1

        if added:
            self.improvements_log.append(f"Seção de backlinks adicionada a {added} notas")
        print(f"   ✓ Backlinks adicionados: {added} notas")
        return added

    def apply_improvements(self):
        """Aplica todas as melhorias automáticas."""
        if self.analyze_only:
            print("\n⏭️  Modo análise apenas — melhorias não aplicadas")
            return

        print("\n🔧 Aplicando melhorias automáticas...")
        self.add_missing_frontmatter()
        self.standardize_frontmatter()
        self.fix_broken_links()
        self.generate_mocs()
        self.add_backlinks_section()

    # ─── RELATÓRIO ───

    def generate_report(self):
        """Gera relatório completo em markdown."""
        print(f"\n📊 Gerando relatório em: {self.report_path}")

        total_notes = len(self.notes)
        total_words = sum(n.word_count for n in self.notes.values())
        total_links = sum(len(n.outgoing_links) for n in self.notes.values())
        now = datetime.now().strftime("%d/%m/%Y às %H:%M")

        lines = [
            "---",
            "tags: [vault, relatorio, analise]",
            "tipo: relatorio",
            f"date_created: {datetime.now().strftime('%Y-%m-%d')}",
            "---",
            "",
            "# 📊 Relatório de Saúde do Vault",
            "",
            f"*Gerado automaticamente em {now}*",
            "",
            "---",
            "",
            "## 📈 Estatísticas Gerais",
            "",
            f"| Métrica | Valor |",
            f"|---------|-------|",
            f"| Total de notas | {total_notes} |",
            f"| Total de palavras | {total_words:,} |",
            f"| Total de links internos | {total_links} |",
            f"| Tags únicas | {self.results.get('tags', {}).get('total_unique', 0)} |",
            f"| Notas órfãs | {len(self.results.get('orphans', []))} |",
            f"| Links quebrados | {sum(len(v) for v in self.results.get('broken_links', {}).values())} |",
            "",
            "---",
            "",
        ]

        # Distribuição por pasta
        lines.append("## 📁 Distribuição por Pasta\n")
        lines.append("| Pasta | Notas |")
        lines.append("|-------|-------|")
        for folder, count in self.results.get("structure", {}).items():
            lines.append(f"| {folder} | {count} |")
        lines.extend(["", "---", ""])

        # Notas sem frontmatter
        without_fm = self.results.get("frontmatter", {}).get("without", [])
        lines.append(f"## ⚠️ Notas sem Frontmatter ({len(without_fm)})\n")
        if without_fm:
            for title in sorted(without_fm)[:30]:
                lines.append(f"- [[{title}]]")
            if len(without_fm) > 30:
                lines.append(f"- *... e mais {len(without_fm) - 30} notas*")
        else:
            lines.append("Todas as notas possuem frontmatter! ✅")
        lines.extend(["", "---", ""])

        # Links quebrados
        broken = self.results.get("broken_links", {})
        total_broken = sum(len(v) for v in broken.values())
        lines.append(f"## 🔗 Links Quebrados ({total_broken})\n")
        if broken:
            for source, links in sorted(broken.items()):
                lines.append(f"**[[{source}]]**:")
                for link in links:
                    lines.append(f"  - `[[{link}]]` — não encontrado")
        else:
            lines.append("Nenhum link quebrado encontrado! ✅")
        lines.extend(["", ""])

        # Sugestões de correção de links
        suggestions = self.results.get("link_suggestions", [])
        if suggestions:
            lines.append(f"### 💡 Sugestões de Correção de Links ({len(suggestions)})\n")
            lines.append("| Nota | Link Quebrado | Sugestão | Similaridade |")
            lines.append("|------|---------------|----------|-------------|")
            for source, broken_link, suggestion, ratio in suggestions:
                lines.append(f"| [[{source}]] | `{broken_link}` | [[{suggestion}]] | {int(ratio*100)}% |")
            lines.extend(["", "---", ""])

        # Notas órfãs
        orphans = self.results.get("orphans", [])
        lines.append(f"## 🏝️ Notas Órfãs ({len(orphans)})\n")
        lines.append("*Notas sem nenhum link de entrada ou saída.*\n")
        if orphans:
            for title in sorted(orphans):
                lines.append(f"- [[{title}]]")
        else:
            lines.append("Nenhuma nota órfã! ✅")
        lines.extend(["", "---", ""])

        # Notas vazias/curtas
        empty = self.results.get("empty_notes", [])
        short = self.results.get("short_notes", [])
        lines.append(f"## 📝 Notas Vazias ou Curtas\n")
        if empty:
            lines.append(f"### Vazias (< 50 caracteres): {len(empty)}\n")
            for title, chars in sorted(empty, key=lambda x: x[1]):
                lines.append(f"- [[{title}]] ({chars} caracteres)")
        if short:
            lines.append(f"\n### Curtas (< 200 caracteres): {len(short)}\n")
            for title, chars in sorted(short, key=lambda x: x[1]):
                lines.append(f"- [[{title}]] ({chars} caracteres)")
        if not empty and not short:
            lines.append("Nenhuma nota vazia ou curta! ✅")
        lines.extend(["", "---", ""])

        # Análise de tags
        tags_data = self.results.get("tags", {})
        all_tags = tags_data.get("all", {})
        lines.append(f"## 🏷️ Análise de Tags\n")
        lines.append(f"**Tags únicas:** {tags_data.get('total_unique', 0)}\n")
        if all_tags:
            lines.append("### Top 20 Tags\n")
            lines.append("| Tag | Uso |")
            lines.append("|-----|-----|")
            for tag, count in list(all_tags.items())[:20]:
                lines.append(f"| `{tag}` | {count} |")

        without_tags = tags_data.get("without_tags", [])
        if without_tags:
            lines.append(f"\n### Notas sem Tags ({len(without_tags)})\n")
            for title in sorted(without_tags)[:20]:
                lines.append(f"- [[{title}]]")
            if len(without_tags) > 20:
                lines.append(f"- *... e mais {len(without_tags) - 20}*")

        orphan_tags = tags_data.get("orphan_tags", [])
        if orphan_tags:
            lines.append(f"\n### Tags Usadas Apenas 1 Vez ({len(orphan_tags)})\n")
            for tag in sorted(orphan_tags)[:20]:
                lines.append(f"- `{tag}`")
            if len(orphan_tags) > 20:
                lines.append(f"- *... e mais {len(orphan_tags) - 20}*")
        lines.extend(["", "---", ""])

        # Grafo de links
        graph = self.results.get("link_graph", {})
        most_connected = graph.get("most_connected", [])
        if most_connected:
            lines.append("## 🕸️ Notas Mais Conectadas (Top 15)\n")
            lines.append("| Nota | Saída | Entrada | Total |")
            lines.append("|------|-------|---------|-------|")
            for title, data in most_connected:
                lines.append(f"| [[{title}]] | {data['outgoing']} | {data['incoming']} | {data['total']} |")
            lines.extend(["", "---", ""])

        # Duplicatas
        duplicates = self.results.get("duplicates", [])
        if duplicates:
            lines.append(f"## 🔄 Possíveis Duplicatas ({len(duplicates)})\n")
            lines.append("| Nota 1 | Nota 2 | Similaridade |")
            lines.append("|--------|--------|-------------|")
            for t1, t2, ratio in duplicates:
                lines.append(f"| [[{t1}]] | [[{t2}]] | {int(ratio*100)}% |")
            lines.extend(["", "---", ""])

        # Formatos de data
        date_data = self.results.get("date_formats", {})
        formats = date_data.get("formats", {})
        if formats:
            lines.append("## 📅 Formatos de Data no Frontmatter\n")
            for fmt, count in formats.items():
                lines.append(f"- `{fmt}`: {count} ocorrências")
            inconsistent = date_data.get("inconsistent", [])
            if inconsistent:
                lines.append(f"\n### Datas Inconsistentes ({len(inconsistent)})\n")
                for title, key, val in inconsistent:
                    lines.append(f"- [[{title}]]: `{key}` = `{val}`")
            lines.extend(["", "---", ""])

        # Melhorias aplicadas
        if self.improvements_log:
            lines.append("## ✅ Melhorias Aplicadas\n")
            for improvement in self.improvements_log:
                lines.append(f"- {improvement}")
            lines.extend(["", "---", ""])

        # Sugestões manuais
        lines.append("## 💡 Sugestões Manuais\n")
        lines.append("*Melhorias que requerem revisão humana:*\n")

        if orphans:
            lines.append(f"1. **Revisar {len(orphans)} notas órfãs** — considere conectá-las ou arquivá-las")
        if empty:
            lines.append(f"2. **Preencher {len(empty)} notas vazias** — adicione conteúdo ou remova-as")
        if duplicates:
            lines.append(f"3. **Verificar {len(duplicates)} possíveis duplicatas** — mescle ou diferencie")
        if suggestions:
            lines.append(f"4. **Revisar {len(suggestions)} sugestões de links** — verifique na tabela acima")

        lines.append(f"5. **Mantenha o vault organizado** — execute este script periodicamente")
        lines.extend(["", "---", f"*Fim do relatório — {now}*", ""])

        report_content = "\n".join(lines)
        self.report_path.write_text(report_content, encoding="utf-8")
        print(f"✅ Relatório salvo em: {self.report_path}")

    # ─── RESUMO CONSOLE ───

    def print_summary(self):
        """Imprime resumo no console."""
        total = len(self.notes)
        print("\n" + "=" * 55)
        print("  📊 RESUMO DA ANÁLISE DO VAULT")
        print("=" * 55)
        print(f"  📁 Total de notas:        {total}")
        print(f"  📝 Total de palavras:      {sum(n.word_count for n in self.notes.values()):,}")
        print(f"  🔗 Links internos:         {sum(len(n.outgoing_links) for n in self.notes.values())}")
        print(f"  🏷️  Tags únicas:            {self.results.get('tags', {}).get('total_unique', 0)}")
        print(f"  ⚠️  Sem frontmatter:        {len(self.results.get('frontmatter', {}).get('without', []))}")
        print(f"  💔 Links quebrados:        {sum(len(v) for v in self.results.get('broken_links', {}).values())}")
        print(f"  🏝️  Notas órfãs:            {len(self.results.get('orphans', []))}")
        print(f"  📝 Notas vazias:           {len(self.results.get('empty_notes', []))}")
        print(f"  🔄 Possíveis duplicatas:   {len(self.results.get('duplicates', []))}")
        print("=" * 55)

        if self.improvements_log:
            print("\n  ✅ MELHORIAS APLICADAS:")
            for imp in self.improvements_log:
                print(f"     • {imp}")
            print()

    # ─── EXECUÇÃO PRINCIPAL ───

    def run(self):
        """Executa o fluxo completo."""
        print("=" * 55)
        print("  🔮 OBSIDIAN VAULT ANALYZER & AUTO-IMPROVER")
        print("=" * 55)
        print(f"  Vault: {self.vault_path}")
        print(f"  Modo:  {'Análise apenas' if self.analyze_only else 'Análise + Melhorias'}")
        print("=" * 55)

        if not self.analyze_only:
            self.create_backup()

        self.load_notes()
        self.run_all_analyses()
        self.apply_improvements()
        self.generate_report()
        self.print_summary()

        print(f"\n🎉 Concluído! Abra o relatório no Obsidian: {self.report_path.name}")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🔮 Obsidian Vault Analyzer & Auto-Improver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python obsidian_vault_analyzer.py
  python obsidian_vault_analyzer.py --analyze-only
  python obsidian_vault_analyzer.py --vault-path "/caminho/do/vault"
  python obsidian_vault_analyzer.py --no-backup
        """,
    )
    parser.add_argument(
        "--vault-path",
        default="./pasta do obsidian/ponto 000/",
        help="Caminho para o vault do Obsidian (padrão: ./pasta do obsidian/ponto 000/)",
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Apenas analisar, sem aplicar melhorias",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Não criar backup antes de modificar",
    )
    parser.add_argument(
        "--report-path",
        default=None,
        help="Caminho customizado para o relatório",
    )

    args = parser.parse_args()

    analyzer = VaultAnalyzer(
        vault_path=args.vault_path,
        analyze_only=args.analyze_only,
        no_backup=args.no_backup,
        report_path=args.report_path,
    )
    analyzer.run()


if __name__ == "__main__":
    main()
