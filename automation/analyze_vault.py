"""
analyze_vault.py
----------------
Topological analysis of an Obsidian vault using obsidiantools and NetworkX.

Usage:
    python automation/analyze_vault.py --vault /path/to/vault [--output report.json]

Outputs:
  - Node count, edge count
  - Top 10 most-connected notes (by in-degree)
  - Isolated (orphan) notes
  - Strongly-connected components
  - Optional JSON report
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import obsidiantools.api as otools
    import networkx as nx
    import pandas as pd
    from rich.console import Console
    from rich.table import Table
except ImportError as exc:
    sys.exit(
        f"Missing dependency: {exc}\n"
        "Run: pip install -r automation/requirements.txt"
    )

console = Console()


def build_vault(vault_path: Path) -> otools.Vault:
    """Connect to an Obsidian vault and build its graph."""
    vault = otools.Vault(vault_path).connect().gather()
    return vault


def analyse(vault: otools.Vault) -> dict:
    """Return a dict with key graph metrics."""
    graph: nx.DiGraph = vault.graph

    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()

    # In-degree = how many notes link TO this note
    in_degrees = sorted(graph.in_degree(), key=lambda x: x[1], reverse=True)
    top_10 = in_degrees[:10]

    # Orphans = zero in-degree AND zero out-degree
    orphans = [n for n, d in graph.degree() if d == 0]

    # Weakly connected components
    wcc = list(nx.weakly_connected_components(graph))
    largest_wcc = max(wcc, key=len) if wcc else set()

    return {
        "nodes": nodes,
        "edges": edges,
        "top_10_by_in_degree": [{"note": n, "in_degree": d} for n, d in top_10],
        "orphan_count": len(orphans),
        "orphans": orphans,
        "component_count": len(wcc),
        "largest_component_size": len(largest_wcc),
    }


def print_report(report: dict) -> None:
    """Render a Rich console report."""
    console.rule("[bold cyan]Vault Analysis Report[/]")
    console.print(f"[green]Nodes:[/] {report['nodes']}")
    console.print(f"[green]Edges:[/] {report['edges']}")
    console.print(
        f"[green]Connected components:[/] {report['component_count']} "
        f"(largest: {report['largest_component_size']} notes)"
    )
    console.print(f"[yellow]Orphan notes:[/] {report['orphan_count']}")

    # Top-10 table
    table = Table(title="Top 10 Notes by Incoming Links", show_lines=True)
    table.add_column("Note", style="cyan")
    table.add_column("In-Degree", justify="right", style="magenta")
    for row in report["top_10_by_in_degree"]:
        table.add_row(row["note"], str(row["in_degree"]))
    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse an Obsidian vault graph.")
    parser.add_argument(
        "--vault",
        required=True,
        type=Path,
        help="Absolute path to the vault root directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write a JSON report.",
    )
    args = parser.parse_args()

    if not args.vault.is_dir():
        sys.exit(f"Vault path does not exist or is not a directory: {args.vault}")

    console.print(f"[bold]Connecting to vault:[/] {args.vault}")
    vault = build_vault(args.vault)
    report = analyse(vault)
    print_report(report)

    if args.output:
        args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
        console.print(f"\n[dim]Report saved to {args.output}[/]")


if __name__ == "__main__":
    main()
