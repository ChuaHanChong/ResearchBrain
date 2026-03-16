#!/usr/bin/env python3
"""
Refresh the BibTeX block in existing Obsidian notes under a notes directory.
Reads the arxiv ID from each filename, fetches fresh BibTeX, and updates in-place.

Usage:
    python refresh_bibtex.py --notes-dir VLA-WAM/KnowledgeHub
    python refresh_bibtex.py --notes-dir VLA-WAM/KnowledgeHub --ids 2602.15922 2601.16163
"""

import argparse
import re
import sys
from pathlib import Path

from utils import fetch_bibtex


def update_bibtex_in_note(note_path: Path, bibtex: str) -> bool:
    """Replace the content of the ```bibtex ... ``` block. Returns True if changed."""
    content = note_path.read_text(encoding="utf-8")
    pattern = r"(```bibtex\n).*?(```)"
    new_content, count = re.subn(
        pattern,
        lambda m: m.group(1) + bibtex + "\n" + m.group(2),
        content,
        flags=re.DOTALL,
    )
    if count == 0:
        # No bibtex block found — append one
        new_content = content.rstrip() + f"\n\n## BibTeX\n\n```bibtex\n{bibtex}\n```\n"
    if new_content == content:
        return False
    note_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Refresh BibTeX in Obsidian notes")
    parser.add_argument("--notes-dir", default="VLA-WAM/KnowledgeHub", help="Directory of .md notes")
    parser.add_argument("--ids", nargs="*", help="Specific arxiv IDs to refresh (e.g. 2602.15922)")
    args = parser.parse_args()

    notes_dir = Path(args.notes_dir)
    if not notes_dir.exists():
        print(f"Error: {notes_dir} does not exist.")
        sys.exit(1)

    if args.ids:
        note_paths = [notes_dir / f"{arxiv_id}.md" for arxiv_id in args.ids]
        note_paths = [p for p in note_paths if p.exists()]
    else:
        note_paths = sorted(notes_dir.glob("*.md"))

    print(f"Notes to refresh: {len(note_paths)}")

    updated = 0
    unchanged = 0
    failed = 0

    for note_path in note_paths:
        arxiv_id = note_path.stem
        bibtex = fetch_bibtex(arxiv_id)
        if not bibtex:
            failed += 1
            continue
        changed = update_bibtex_in_note(note_path, bibtex)
        if changed:
            print(f"  UPDATED {arxiv_id}")
            updated += 1
        else:
            unchanged += 1

    print(f"\n{'=' * 40}")
    print(f"Updated  : {updated}")
    print(f"Unchanged: {unchanged}")
    print(f"Failed   : {failed}")


if __name__ == "__main__":
    main()
