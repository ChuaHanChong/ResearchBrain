#!/usr/bin/env python3
"""
Convert an existing KnowledgeHub JSON file into individual Obsidian markdown notes.
No Selenium required — content is read directly from the JSON.

Usage:
    python from_json.py --json X01_KnowledgeHub/KnowledgeHub_VLA-WAM.json
    python from_json.py --json X01_KnowledgeHub/KnowledgeHub_VLA-WAM.json --limit 3
    python from_json.py --json X01_KnowledgeHub/KnowledgeHub_VLA-WAM.json --no-bibtex
    python from_json.py --json X01_KnowledgeHub/KnowledgeHub_VLA-WAM.json --force
"""

import argparse
import json
import sys
import time
from pathlib import Path

from tqdm import tqdm

# Reuse shared utilities from run.py
scripts_dir = str(Path(__file__).parent)
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)
from run import arxiv_id_from_url, fetch_bibtex, render_note


def load_knowledge_hub(json_path: str) -> dict:
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Convert KnowledgeHub JSON to individual Obsidian .md notes"
    )
    parser.add_argument(
        "--json",
        required=True,
        help="Path to KnowledgeHub JSON file (e.g. X01_KnowledgeHub/KnowledgeHub_VLA-WAM.json)",
    )
    parser.add_argument(
        "--out",
        default="X01_KnowledgeHub",
        help="Output directory for .md notes (default: X01_KnowledgeHub)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most N papers (for testing)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing notes",
    )
    parser.add_argument(
        "--no-bibtex",
        action="store_true",
        help="Skip BibTeX fetching (faster; run refresh_bibtex.py afterwards)",
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    data = load_knowledge_hub(args.json)
    print(f"Loaded {len(data)} papers from {args.json}")

    to_process = []
    skipped = 0
    for url in data:
        arxiv_id = arxiv_id_from_url(url)
        note_path = out_dir / f"{arxiv_id}.md"
        if note_path.exists() and not args.force:
            skipped += 1
        else:
            to_process.append(url)

    if args.limit:
        to_process = to_process[: args.limit]

    print(f"Already written: {skipped}")
    print(f"To process     : {len(to_process)}")

    if not to_process:
        print("Nothing to do.")
        return

    processed = 0
    failed = []

    for url in tqdm(to_process, desc="Converting"):
        arxiv_id = arxiv_id_from_url(url)
        entry = data[url]
        try:
            title = entry.get("Title", arxiv_id)
            summary = {
                "Summary": entry.get("Summary", ""),
                "Problem": entry.get("Problem", []),
                "Method": entry.get("Method", []),
                "Results": entry.get("Results", []),
                "Takeaways": entry.get("Takeaways", []),
            }

            if args.no_bibtex:
                bibtex = ""
            else:
                bibtex = fetch_bibtex(arxiv_id)
                time.sleep(0.3)  # polite rate limiting

            note = render_note(arxiv_id, title, summary, bibtex)
            (out_dir / f"{arxiv_id}.md").write_text(note, encoding="utf-8")
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

    if args.no_bibtex and processed > 0:
        print(
            f"\nBibTeX skipped. Run afterwards:\n"
            f"  python refresh_bibtex.py --notes-dir {args.out}"
        )


if __name__ == "__main__":
    main()
