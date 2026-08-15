#!/usr/bin/env python3
"""Generate and write KnowledgeHub notes for arxiv papers, single or batch.

For each paper, fetches title, the generated five short fields, BibTeX, and the Detailed Report
(all via `retrieve.py`) and writes the note (`render_note`). One script call does everything — no
external Agent-tool dispatch needed.

Usage:
    python extract_summaries.py --input scripts/knowledge.py --out _KnowledgeHub_
    python extract_summaries.py --input scripts/knowledge.py --out _KnowledgeHub_ --limit 3
    python extract_summaries.py --ids 2608.13474 2608.13489 --out _KnowledgeHub_
    python extract_summaries.py --ids 2608.13474 --out _KnowledgeHub_ --force
"""

import argparse
import importlib.util
from pathlib import Path

from tqdm import tqdm

from common import ABS_URL, KH_DIR, fetch_bibtex, parse_arxiv_id
from retrieve import extract_title, fetch_research_report, generate_summary


def load_papers(input_path: str) -> list:
    """Import the knowledge.py module at the given path and return its papers list."""
    spec = importlib.util.spec_from_file_location("knowledge", input_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.papers


def render_note(
    arxiv_id: str,
    title: str,
    summary: dict,
    bibtex: str,
    research_report: str = "",
) -> str:
    """Render the full Obsidian KH note markdown from a paper's summary, BibTeX, and optional Detailed Report."""
    link = ABS_URL.format(arxiv_id)

    def bullets(items: list) -> str:
        """Render items as a markdown bullet list, or a placeholder bullet when empty."""
        return "\n".join(f"- {item}" for item in items) if items else "- (none)"

    bibtex_block = f"```bibtex\n{bibtex}\n```" if bibtex else "```bibtex\n(unavailable)\n```"
    # Detailed analysis rendered after (outside) the hidden BibTeX block, so it shows in preview.
    report_block = f"\n## Detailed Report\n\n{research_report}\n" if research_report.strip() else ""

    return f"""\
---
id: "{arxiv_id}"
title: "{title}"
link: "{link}"
authors: []
tags: []
aliases: []
---
# {title}

> [!summary] Summary
> {summary.get("Summary", "").strip()}

## Problem

{bullets(summary.get("Problem", []))}

## Method

{bullets(summary.get("Method", []))}

## Results

{bullets(summary.get("Results", []))}

## Takeaways

> [!tip] Key Insights
{chr(10).join("> - " + t for t in summary.get("Takeaways", []))}

%%
## BibTeX

{bibtex_block}
%%
{report_block}
"""


def main() -> None:
    """Parse args, generate + assemble each paper's note, reporting a Processed/Skipped/Failed summary."""
    parser = argparse.ArgumentParser(description="Generate summaries via claude -p and write Obsidian notes")
    parser.add_argument("--input", default=None, help="Path to knowledge.py with papers list (batch mode)")
    parser.add_argument("--ids", nargs="+", help="One or more arxiv IDs or URLs to process directly")
    parser.add_argument("--out", default=KH_DIR, help="Output directory for .md notes")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N papers (for testing)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing notes")
    args = parser.parse_args()

    if not args.input and not args.ids:
        parser.error("Provide either --input (batch) or --ids (single/few papers)")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.ids:
        # Normalise IDs/URLs to full arxiv URLs
        all_papers = [
            f"https://arxiv.org/abs/{parse_arxiv_id(id_or_url)}"
            for id_or_url in args.ids
        ]
    else:
        all_papers = load_papers(args.input)

    unique_papers = list(dict.fromkeys(all_papers))
    if len(all_papers) != len(unique_papers):
        print(f"Removed {len(all_papers) - len(unique_papers)} duplicates from paper list.")

    to_process = []
    skipped = 0
    for url in unique_papers:
        arxiv_id = parse_arxiv_id(url)
        note_path = out_dir / f"{arxiv_id}.md"
        if note_path.exists() and not args.force:
            skipped += 1
        else:
            to_process.append(url)

    if args.limit:
        to_process = to_process[:args.limit]

    print(f"Papers in list : {len(unique_papers)}")
    print(f"Already written: {skipped}")
    print(f"To process     : {len(to_process)}")

    if not to_process:
        print("Nothing to do.")
        return

    # in-vault arxiv IDs, so the Detailed Report can wikilink citations to existing KH notes
    kh_ids = {p.stem for p in out_dir.glob("*.md")}

    processed = 0
    failed = []

    for url in tqdm(to_process, desc="Extracting"):
        arxiv_id = parse_arxiv_id(url)
        try:
            title = extract_title(url)

            summary = generate_summary(arxiv_id)

            bibtex = fetch_bibtex(arxiv_id)
            research_report = fetch_research_report(arxiv_id, kh_ids)

            note = render_note(arxiv_id, title or arxiv_id, summary, bibtex, research_report)
            (out_dir / f"{arxiv_id}.md").write_text(note, encoding="utf-8")
            kh_ids.add(arxiv_id)
            processed += 1

        except Exception as e:
            print(f"\n  Failed: {url}\n    {e}")
            failed.append(url)

    print(f"\n{'=' * 40}")
    print(f"Processed : {processed}")
    print(f"Skipped   : {skipped} (already written)")
    print(f"Failed    : {len(failed)}")
    if failed:
        print("Failed papers:")
        for paper in failed:
            print(f"  - {paper}")


if __name__ == "__main__":
    main()
