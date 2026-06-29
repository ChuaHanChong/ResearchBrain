#!/usr/bin/env python3
"""Batch-extract paper summaries from alphaxiv and write Obsidian markdown notes.

Usage:
    python run.py --input scripts/knowledge.py --out _KnowledgeHub_
    python run.py --input scripts/knowledge.py --out _KnowledgeHub_ --limit 3
    python run.py --input scripts/knowledge.py --out _KnowledgeHub_ --force
"""

import argparse
import importlib.util
import sys
from pathlib import Path

from tqdm import tqdm
from selenium import webdriver

from utils import fetch_bibtex

KH_DIR = "_KnowledgeHub_"  # default output dir for KH notes (vault-relative)


def load_papers(input_path: str) -> list:
    """Import the knowledge.py module at the given path and return its papers list."""
    spec = importlib.util.spec_from_file_location("knowledge", input_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.papers


def init_driver() -> webdriver.Chrome:
    """Build and return a headless Chrome webdriver configured for scraping."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


def arxiv_id_from_url(url: str) -> str:
    """Return the arxiv ID from a URL by taking its last path segment."""
    return url.rstrip("/").split("/")[-1]


def render_note(
    arxiv_id: str,
    title: str,
    summary: dict,
    bibtex: str,
) -> str:
    """Render the full Obsidian KH note markdown for a paper from its summary and BibTeX."""
    link = f"https://www.alphaxiv.org/overview/{arxiv_id}"

    def bullets(items: list) -> str:
        """Render items as a markdown bullet list, or a placeholder bullet when empty."""
        return "\n".join(f"- {item}" for item in items) if items else "- (none)"

    bibtex_block = f"```bibtex\n{bibtex}\n```" if bibtex else "```bibtex\n(unavailable)\n```"

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
"""


def quality_check(entry: dict, url: str) -> None:
    """Warn when any summary section has fewer than three extracted items."""
    for section in ["Problem", "Method", "Results", "Takeaways"]:
        items = entry.get(section, [])
        if isinstance(items, list) and len(items) < 3:
            print(f"  Warning: {section} has only {len(items)} items for {url}")


def main() -> None:
    """Parse args, scrape each paper, and write its Obsidian KH note, reporting a summary."""
    parser = argparse.ArgumentParser(description="Scrape alphaxiv and write Obsidian notes")
    parser.add_argument("--input", default=None, help="Path to knowledge.py with papers list (batch mode)")
    parser.add_argument("--ids", nargs="+", help="One or more arxiv IDs or URLs to process directly")
    parser.add_argument("--out", default=KH_DIR, help="Output directory for .md notes")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N papers (for testing)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing notes")
    args = parser.parse_args()

    if not args.input and not args.ids:
        parser.error("Provide either --input (batch) or --ids (single/few papers)")

    scripts_dir = str(Path(__file__).parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from retrieve import extract_title, extract_summary

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.ids:
        # Normalise IDs/URLs to full arxiv URLs
        all_papers = [
            f"https://arxiv.org/abs/{arxiv_id_from_url(id_or_url)}"
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
        arxiv_id = arxiv_id_from_url(url)
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

    driver = init_driver()
    processed = 0
    failed = []

    try:
        for url in tqdm(to_process, desc="Extracting"):
            arxiv_id = arxiv_id_from_url(url)
            try:
                title = extract_title(url)

                summary = extract_summary(driver, arxiv_id)
                quality_check(summary, url)

                bibtex = fetch_bibtex(arxiv_id)

                note = render_note(arxiv_id, title or arxiv_id, summary, bibtex)
                (out_dir / f"{arxiv_id}.md").write_text(note, encoding="utf-8")
                processed += 1

            except Exception as e:
                print(f"\n  Failed: {url}\n    {e}")
                failed.append(url)
    finally:
        driver.quit()

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
