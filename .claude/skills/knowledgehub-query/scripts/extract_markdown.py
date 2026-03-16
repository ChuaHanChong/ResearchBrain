#!/usr/bin/env python3
"""
Extract and print KnowledgeHub note content for arxiv IDs found in the input text.

Usage:
    echo "query text with https://arxiv.org/abs/2602.15922 and 2507.04447" | python extract_markdown.py
    python extract_markdown.py --notes-dir X01_KnowledgeHub < query.txt
    python extract_markdown.py 2602.15922 2507.04447 2506.21539

Prints the full content of each matching note, separated by dividers.
Warns to stderr for any IDs with no matching note.
"""

import argparse
import re
import sys
from pathlib import Path


ARXIV_ID_PATTERN = re.compile(
    r"(?:arxiv\.org/(?:abs|pdf)/|arxiv\.org/overview/)?(\d{4}\.\d{4,5})(?:v\d+)?"
)


def extract_ids(text: str) -> list[str]:
    """Extract unique arxiv IDs from text, preserving order."""
    seen = set()
    ids = []
    for match in ARXIV_ID_PATTERN.finditer(text):
        arxiv_id = match.group(1)
        if arxiv_id not in seen:
            seen.add(arxiv_id)
            ids.append(arxiv_id)
    return ids


def main():
    parser = argparse.ArgumentParser(description="Print KnowledgeHub note content for arxiv IDs")
    parser.add_argument("ids", nargs="*", help="Arxiv IDs or URLs (if omitted, reads from stdin)")
    parser.add_argument("--notes-dir", default="X01_KnowledgeHub", help="KnowledgeHub directory")
    args = parser.parse_args()

    notes_dir = Path(args.notes_dir)
    if not notes_dir.exists():
        print(f"Error: notes directory '{notes_dir}' not found", file=sys.stderr)
        sys.exit(1)

    if args.ids:
        text = " ".join(args.ids)
    else:
        text = sys.stdin.read()

    ids = extract_ids(text)
    if not ids:
        print("No arxiv IDs found in input", file=sys.stderr)
        sys.exit(0)

    missing = []
    for arxiv_id in ids:
        note_path = notes_dir / f"{arxiv_id}.md"
        if note_path.exists():
            print(f"\n{'='*60}")
            print(f"# {arxiv_id}  ({note_path})")
            print('='*60)
            print(note_path.read_text(encoding="utf-8"))
        else:
            missing.append(arxiv_id)

    if missing:
        print(f"\nWarning: no notes found for: {', '.join(missing)}", file=sys.stderr)


if __name__ == "__main__":
    main()
