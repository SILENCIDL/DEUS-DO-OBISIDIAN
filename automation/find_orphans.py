"""
find_orphans.py
---------------
Detect orphan notes in an Obsidian vault (notes with no incoming links).

Usage:
    python automation/find_orphans.py --vault /path/to/vault [--fix] [--output orphans.json]

Options:
    --fix       Move orphan notes to notes/inbox/ for triage instead of just listing them.
    --output    Write a JSON list of orphan paths to the given file.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    import obsidiantools.api as otools
    from rich.console import Console
    from rich.table import Table
except ImportError as exc:
    sys.exit(
        f"Missing dependency: {exc}\n"
        "Run: pip install -r automation/requirements.txt"
    )

console = Console()


def find_orphans(vault_path: Path) -> list[str]:
    """Return a list of vault-relative paths for orphan notes."""
    vault = otools.Vault(vault_path).connect().gather()
    graph = vault.graph

    # Orphan = node with degree 0 (no links in or out)
    orphans = [
        node
        for node, degree in graph.degree()
        if degree == 0 and not node.startswith(".obsidian")
    ]
    return sorted(orphans)


def move_to_inbox(vault_path: Path, orphans: list[str]) -> None:
    """Move orphan files to notes/inbox/ for manual triage."""
    inbox = vault_path / "notes" / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    for rel_path in orphans:
        src = vault_path / rel_path
        if not src.exists():
            console.print(f"[yellow]Skipping (not found):[/] {rel_path}")
            continue
        dst = inbox / src.name
        if dst.exists():
            console.print(f"[yellow]Skipping (already in inbox):[/] {src.name}")
            continue
        shutil.move(str(src), str(dst))
        console.print(f"[green]Moved:[/] {rel_path} → notes/inbox/{src.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Find orphan notes in an Obsidian vault.")
    parser.add_argument(
        "--vault",
        required=True,
        type=Path,
        help="Absolute path to the vault root directory.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Move orphan notes to notes/inbox/ for triage.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write a JSON list of orphan paths.",
    )
    args = parser.parse_args()

    if not args.vault.is_dir():
        sys.exit(f"Vault path does not exist or is not a directory: {args.vault}")

    console.print(f"[bold]Scanning vault for orphans:[/] {args.vault}")
    orphans = find_orphans(args.vault)

    if not orphans:
        console.print("[green]✅ No orphan notes found.[/]")
    else:
        table = Table(title=f"Orphan Notes ({len(orphans)})", show_lines=True)
        table.add_column("Path", style="cyan")
        for p in orphans:
            table.add_row(p)
        console.print(table)

        if args.fix:
            move_to_inbox(args.vault, orphans)

    if args.output:
        args.output.write_text(json.dumps(orphans, indent=2), encoding="utf-8")
        console.print(f"\n[dim]Orphan list saved to {args.output}[/]")


if __name__ == "__main__":
    main()
