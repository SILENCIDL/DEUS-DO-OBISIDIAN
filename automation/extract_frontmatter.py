"""
extract_frontmatter.py
----------------------
Batch-extract YAML frontmatter from all notes in an Obsidian vault.

Usage:
    python automation/extract_frontmatter.py --vault /path/to/vault \
        [--folder notes/projects] \
        [--fields status,priority,due] \
        [--output frontmatter.csv]

Options:
    --folder    Restrict scan to a vault-relative folder (default: entire vault).
    --fields    Comma-separated list of frontmatter keys to extract.
                If omitted, ALL frontmatter keys are extracted.
    --output    Path for the output CSV file (default: stdout as JSON).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import frontmatter
    import pandas as pd
    from rich.console import Console
    from rich.table import Table
except ImportError as exc:
    sys.exit(
        f"Missing dependency: {exc}\n"
        "Run: pip install -r automation/requirements.txt"
    )

console = Console()


def iter_markdown_files(base: Path, sub_folder: str = "") -> list[Path]:
    """Yield all .md files under base / sub_folder."""
    root = base / sub_folder if sub_folder else base
    if not root.exists():
        return []
    return sorted(root.rglob("*.md"))


def extract(vault_path: Path, sub_folder: str, fields: list[str]) -> list[dict]:
    """Return a list of dicts: one per note, containing requested frontmatter."""
    records = []
    files = iter_markdown_files(vault_path, sub_folder)

    for md_file in files:
        try:
            post = frontmatter.load(md_file)
        except Exception as exc:
            console.print(f"[yellow]Warning:[/] could not parse {md_file}: {exc}")
            continue

        meta = post.metadata
        rel_path = md_file.relative_to(vault_path).as_posix()

        if fields:
            row = {"path": rel_path, **{f: meta.get(f) for f in fields}}
        else:
            row = {"path": rel_path, **meta}

        records.append(row)

    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-extract YAML frontmatter from Obsidian vault notes."
    )
    parser.add_argument(
        "--vault",
        required=True,
        type=Path,
        help="Absolute path to the vault root directory.",
    )
    parser.add_argument(
        "--folder",
        default="",
        help="Vault-relative folder to restrict the scan (default: entire vault).",
    )
    parser.add_argument(
        "--fields",
        default="",
        help="Comma-separated list of frontmatter keys to extract.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to write a CSV file. If omitted, prints JSON to stdout.",
    )
    args = parser.parse_args()

    if not args.vault.is_dir():
        sys.exit(f"Vault path does not exist or is not a directory: {args.vault}")

    requested_fields = [f.strip() for f in args.fields.split(",") if f.strip()]

    console.print(f"[bold]Extracting frontmatter from:[/] {args.vault / args.folder or args.vault}")
    records = extract(args.vault, args.folder, requested_fields)

    if not records:
        console.print("[yellow]No notes found.[/]")
        return

    df = pd.DataFrame(records)

    if args.output:
        df.to_csv(args.output, index=False, encoding="utf-8")
        console.print(f"[green]✅ Wrote {len(df)} records to {args.output}[/]")
    else:
        # Pretty-print first 20 rows as a Rich table
        preview_cols = list(df.columns[:6])
        table = Table(title=f"Frontmatter Preview ({len(df)} notes)", show_lines=True)
        for col in preview_cols:
            table.add_column(col, style="cyan", no_wrap=True)
        for _, row in df.head(20).iterrows():
            table.add_row(*[str(row[c]) if row[c] is not None else "—" for c in preview_cols])
        console.print(table)

        # Full JSON to stdout for piping
        print(json.dumps(records, indent=2, default=str))


if __name__ == "__main__":
    main()
