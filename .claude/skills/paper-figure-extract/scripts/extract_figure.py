#!/usr/bin/env python3
"""
Download a figure from ar5iv and embed it into a KnowledgeHub note.

Usage:
    python extract_figure.py 2506.19850 --list
    python extract_figure.py 2506.19850 --fig 2
"""

import argparse
import json
import re
from pathlib import Path

import requests


def fetch_figures(arxiv_id: str) -> list:
    """Fetch ar5iv page and return list of {fig, image_url, caption} dicts.

    Prints a specific error and returns [] when ar5iv has no entry for the paper
    or when the page exists but has no <figure> elements.
    """
    url = f"https://ar5iv.org/abs/{arxiv_id}"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"ERROR: ar5iv has no entry for {arxiv_id} ({e})")
        return []

    figures = []
    seen = set()
    for m in re.finditer(r"<figure[^>]*>(.*?)</figure>", resp.text, re.DOTALL):
        block = m.group(1)
        img = re.search(r'src="([^"]+/assets/(x\d+)\.png)"', block)
        cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", block, re.DOTALL)
        if not (img and cap) or img.group(2) in seen:
            continue
        seen.add(img.group(2))
        caption = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", cap.group(1))).strip()
        n = re.search(r"\bFigure\s+(\d+)\b", caption, re.IGNORECASE)
        if not n:
            continue
        image_url = img.group(1)
        if image_url.startswith("/"):
            image_url = "https://ar5iv.org" + image_url
        figures.append({"fig": int(n.group(1)), "image_url": image_url, "caption": caption})

    if not figures:
        print(f"ERROR: ar5iv page exists but has no <figure> elements: {url}")
    return sorted(figures, key=lambda f: f["fig"])


def download_figure(url: str, dest: Path) -> None:
    """Download a single figure PNG to dest."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    dest.write_bytes(resp.content)


def embed_in_note(note: Path, image: Path, caption: str) -> bool:
    """Insert ![[image]] + caption under ## Method. Idempotent.

    The caption is used verbatim — the agent is responsible for crafting it.
    """
    if not note.exists():
        return False
    text = note.read_text(encoding="utf-8")
    link = f"![[{image.name}]]"
    if link in text:
        return True
    m = re.search(r"^##\s*Methods?\s*$", text, re.MULTILINE)
    if not m:
        return False
    block = f"\n\n{link}\n*{caption.strip()}*\n"
    note.write_text(text[:m.end()] + block + text[m.end():], encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Download a figure from ar5iv and embed it into a KH note")
    parser.add_argument("arxiv_id", help="arXiv ID, e.g. 2401.02117")
    parser.add_argument("--list", action="store_true", help="Print all figures + captions as JSON")
    parser.add_argument("--fig", type=int, help="Figure number to download and embed")
    parser.add_argument("--caption", help="Caption text to embed under the figure (agent-crafted; falls back to raw ar5iv caption if omitted)")
    parser.add_argument("--out", default="data/figures", help="Output directory for the downloaded PNG")
    parser.add_argument("--kh", default="_KnowledgeHub_", help="KnowledgeHub directory for the embed step")
    args = parser.parse_args()

    figures = fetch_figures(args.arxiv_id)
    if not figures:
        return  # error already printed by fetch_figures

    if args.list:
        print(json.dumps(figures, indent=2))
        return

    if args.fig is None:
        parser.error("either --list or --fig N is required")

    chosen = next((f for f in figures if f["fig"] == args.fig), None)
    if chosen is None:
        available = [f["fig"] for f in figures]
        print(f"ERROR: Figure {args.fig} not in ar5iv list. Available: {available}")
        return

    dest = Path(args.out) / f"{args.arxiv_id}-method.png"
    download_figure(chosen["image_url"], dest)
    print(f"Figure : {chosen['fig']}")
    print(f"Source : {chosen['image_url']}")
    print(f"Saved  : {dest}")

    caption = args.caption if args.caption else chosen["caption"]
    embedded = embed_in_note(Path(args.kh) / f"{args.arxiv_id}.md", dest, caption)
    print(f"Embed  : {'yes' if embedded else 'skipped (note missing or no ## Method section)'}")


if __name__ == "__main__":
    main()
