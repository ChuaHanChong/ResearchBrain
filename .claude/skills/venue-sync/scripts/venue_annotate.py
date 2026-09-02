#!/usr/bin/env python3
"""Render venue badges next to paper wikilinks in General/ and Embodied-AI/.

Reads each paper's venue from its KnowledgeHub frontmatter and appends it after the wikilink, e.g.
`[[2210.13066|DaXBench]] (ICLR\'23 Oral)`. Idempotent, and --strip is its exact inverse.

Usage:
    .venv/bin/python venue_annotate.py                    # dry run
    .venv/bin/python venue_annotate.py --write            # apply
    .venv/bin/python venue_annotate.py --write --strip    # remove every badge
    .venv/bin/python venue_annotate.py --files a.md b.md  # spot-check specific files
"""
import argparse
import re
from pathlib import Path

from venue_lookup import CORE_VENUES

NOTES_DIR = Path("_KnowledgeHub_")
TARGET_GLOBS = ("General/*.md", "Embodied-AI/*.md")
TIER_LABEL = {"oral": " Oral", "highlight": " Highlight", "spotlight": " Spotlight"}
SUFFIXES = ("Oral", "Highlight", "Spotlight", "Workshop")
# Space-free short names only: that is what keeps the strip regex disjoint from the 100+ hand-written
# parentheticals in these files. Leading digit allowed so 3DV still gets a badge.
SHORT_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9.&-]*\Z")
WIKILINK_RE = re.compile(r"\[\[(\d{4}\.\d{4,5})\|[^\]]*\]\]")
FENCE_RE = re.compile(r"\A\s*(```|~~~)")
FRONTMATTER_CHARS = 2000  # frontmatter always fits well inside this prefix


def read_badges(notes_dir: Path) -> dict[str, tuple[str, str]]:
    """Map each arxiv ID to its (venue, badge text), skipping papers with no venue or no short name."""
    badges: dict[str, tuple[str, str]] = {}
    for path in notes_dir.glob("*.md"):
        if not re.fullmatch(r"\d{4}\.\d{4,5}", path.stem):
            continue
        head = path.read_text()[:FRONTMATTER_CHARS]
        venue = _field(head, "venue")
        if not venue or not SHORT_RE.match(venue):  # multi-word venue names would read as prose in a badge
            continue
        year = _field(head, "venue_year")
        stamp = f"{venue}'{year[2:]}" if year.isdigit() and int(year) else venue
        if _field(head, "venue_type") == "workshop":
            suffix = " Workshop"  # workshops carry no tier, so the two can never collide
        else:
            suffix = TIER_LABEL.get(_field(head, "venue_tier"), "")
        badges[path.stem] = (venue, f" ({stamp}{suffix})")
    return badges


def _field(text: str, key: str) -> str:
    """Read one frontmatter scalar value out of a note's head."""
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', text, re.M)
    return m.group(1) if m else ""


def strip_pattern(badges: dict[str, tuple[str, str]]) -> re.Pattern[str]:
    """Build the badge-removal regex from the exact short-name vocabulary actually in use."""
    alt = "|".join(re.escape(v) for v in sorted({b[0] for b in badges.values()}, key=len, reverse=True))
    tail = "|".join(SUFFIXES)
    return re.compile(rf"(?<=\]\]) \((?:{alt})(?:'\d\d)?(?: (?:{tail}))?\)")


def annotate(text: str, badges: dict[str, str], strip: re.Pattern[str]) -> str:
    """Strip existing badges then re-insert current ones after every paper wikilink, outside code fences."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if FENCE_RE.match(line):
            in_fence = not in_fence
        if in_fence or "[[" not in line:
            out.append(line)
            continue
        line = strip.sub("", line)
        line = WIKILINK_RE.sub(lambda m: m.group(0) + badges.get(m.group(1), ""), line)
        out.append(line)
    return "".join(out)


def main() -> None:
    """Parse arguments and annotate (or dry-run) every target file."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--notes-dir", default=str(NOTES_DIR))
    ap.add_argument("--write", action="store_true", help="write changes (default is a dry run)")
    ap.add_argument("--files", nargs="*", default=[], help="restrict to these paths instead of the full sweep")
    ap.add_argument("--strip", action="store_true", help="remove every badge instead of refreshing them")
    args = ap.parse_args()

    # Strip against every venue ever badged, or one dropped from CORE_VENUES leaves orphans forever.
    all_badges = read_badges(Path(args.notes_dir))
    strip = strip_pattern(all_badges)
    badges = {} if args.strip else {k: b for k, (v, b) in all_badges.items() if v in CORE_VENUES}
    print(f"{len(badges)} papers have a renderable badge")

    paths = [Path(f) for f in args.files] or [p for g in TARGET_GLOBS for p in sorted(Path().glob(g))]
    total = 0
    for path in paths:
        text = path.read_text()
        new = annotate(text, badges, strip)
        if new == text:
            continue
        added = len(strip.findall(new)) - len(strip.findall(text))
        total += added
        print(f"  {path}: {added:+d} badges")
        if args.write:
            path.write_text(new)
    print(f"{'wrote' if args.write else 'would add'} {total} badges across {len(paths)} files")


if __name__ == "__main__":
    main()
