#!/usr/bin/env python3
"""Extract a paper's pipeline figure from its arxiv HTML render
(https://arxiv.org/html/{ID}, static HTML): the paper's own figures + figcaptions,
then embed a chosen figure (verbatim caption) under the KH note's ``## Method``.

Reads arxiv's LaTeX-to-HTML render with requests + BeautifulSoup (no browser). You
(the agent) still VISUALLY inspect the candidates and pick the real pipeline diagram.

Usage:
    uv run python arxiv_figures.py {ID} --list                 # fetch HTML, download figs, print JSON
    uv run python arxiv_figures.py {ID} --embed --xnum N       # embed figure N with its arxiv caption (verbatim)
    uv run python arxiv_figures.py {ID} --revert               # remove any embed + png

--list writes a cache: data/figures/_arxiv/{ID}/x{N}.png + data/figures/_arxiv/{ID}.json
(so --embed reuses the exact caption). Re-run --list with --refresh to re-fetch.
"""

import argparse
import json
import os
import re
import shutil
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

H = {"User-Agent": "Mozilla/5.0"}
KH_DIR = "_KnowledgeHub_"           # vault-relative KnowledgeHub notes dir
FIGURES_DIR = "data/figures"        # vault-relative figures output dir
CACHE = f"{FIGURES_DIR}/_arxiv"     # per-paper arxiv-HTML figure cache


def scrape(pid: str) -> list[dict]:
    """Fetch the arxiv HTML render and return [{xnum, alt, caption, src}] for its figures."""
    try:
        r = requests.get(f"https://arxiv.org/html/{pid}", headers=H, timeout=30)
        r.raise_for_status()
    except Exception:
        return []
    if "No HTML for" in r.text:  # arxiv stub page: no HTML render exists for this paper
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    # resolve relative img srcs against the page's <base href> (or .../html/ if absent)
    base_tag = soup.find("base")
    base_url = urljoin(r.url, base_tag["href"]) if base_tag and base_tag.get("href") else "https://arxiv.org/html/"
    figs = []
    seen = set()
    for fig in soup.select("figure.ltx_figure"):
        if fig.find_parent("figure"):  # a nested subfigure panel; its top-level figure covers it
            continue
        img = fig.select_one("img.ltx_graphics")
        if img is None:
            continue
        src = img.get("src") or ""
        if not src or src.startswith("data:"):
            continue
        try:
            if int(img.get("width") or 999) < 60:  # spacer / inline glyph, not a real figure
                continue
        except ValueError:
            pass
        caps = fig.find_all("figcaption")
        cap_el = next((c for c in caps if re.match(r"\s*fig", c.get_text(strip=True), re.I)),
                      caps[0] if caps else None)
        # collapse whitespace; the span-join leaves "Figure 1 :" so close it back to "Figure 1:"
        caption = re.sub(r"\s+:", ":", re.sub(r"\s+", " ", cap_el.get_text(" ", strip=True))).strip() if cap_el else ""
        m = (re.search(r"\bFig(?:ure)?\.?\s*([A-Za-z]?\d+)", caption)
             or re.search(r"\.F(\d+)", img.get("id") or ""))
        xnum = m.group(1) if m else str(len(figs))
        if xnum in seen:
            xnum = f"f{len(figs)}"
        seen.add(xnum)
        abs_url = urljoin(base_url, src)
        figs.append({"xnum": xnum, "alt": "", "caption": caption[:500], "src": abs_url})
    return figs


def cmd_list(pid: str, refresh: bool = False, quiet: bool = False) -> None:
    """Fetch the arxiv HTML, download figures to cache, and print the figure JSON (--list)."""
    metap = f"{CACHE}/{pid}.json"
    if os.path.exists(metap) and not refresh:
        if not quiet:
            print(open(metap).read())
        return
    figs = scrape(pid)
    os.makedirs(f"{CACHE}/{pid}", exist_ok=True)
    out = []
    for f in figs:
        path = f"{CACHE}/{pid}/x{f['xnum']}.png"
        try:
            ir = requests.get(f["src"], headers=H, timeout=30)
            if "image" in ir.headers.get("content-type", "") and len(ir.content) > 3000:
                open(path, "wb").write(ir.content)
                f["path"] = os.path.abspath(path)
                out.append(f)
        except Exception:
            pass
    meta = {"id": pid, "figures": out}
    json.dump(meta, open(metap, "w"))
    if not quiet:
        print(json.dumps(meta))


def _strip(t: str, pid: str) -> str:
    """Remove any existing method-figure embed and its caption line from note text t."""
    return re.sub(r"\n!\[\[" + re.escape(pid) + r"-method\.png\]\]\n\*[^\n]*\*\n", "\n", t, count=1)


def cmd_embed(pid: str, xnum: str) -> None:
    """Embed cached figure N with its verbatim arxiv caption under the note's Method (--embed)."""
    metap = f"{CACHE}/{pid}.json"
    if not os.path.exists(metap):
        print("no-cache (run --list first)")
        return
    meta = json.load(open(metap))
    fig = next((f for f in meta["figures"] if f["xnum"] == str(xnum)), None)
    if not fig:
        print(f"xnum {xnum} not in cache")
        return
    src = fig.get("path") or f"{CACHE}/{pid}/x{xnum}.png"
    os.makedirs(FIGURES_DIR, exist_ok=True)
    shutil.copy(src, f"{FIGURES_DIR}/{pid}-method.png")
    p = f"{KH_DIR}/{pid}.md"
    t = _strip(open(p).read(), pid)
    cap = re.sub(r"\s+", " ", fig["caption"]).strip()  # arxiv caption, verbatim (only whitespace collapsed)
    t = t.replace("## Method\n", "## Method\n" + f"\n![[{pid}-method.png]]\n*{cap}*\n", 1)
    open(p, "w").write(t)
    print(f"embedded x{xnum}: {cap[:80]}")


def cmd_revert(pid: str) -> None:
    """Remove the note's method-figure embed and delete its png (--revert)."""
    p = f"{KH_DIR}/{pid}.md"
    if os.path.exists(p):
        open(p, "w").write(_strip(open(p).read(), pid))
    fp = f"{FIGURES_DIR}/{pid}-method.png"
    if os.path.exists(fp):
        os.remove(fp)
    print("reverted")


def main() -> None:
    """Parse CLI args and dispatch to the --list / --embed / --revert handler."""
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--embed", action="store_true")
    ap.add_argument("--xnum")
    ap.add_argument("--revert", action="store_true")
    a = ap.parse_args()
    if a.revert:
        cmd_revert(a.id)
    elif a.embed:
        cmd_embed(a.id, a.xnum)
    elif a.list:
        cmd_list(a.id, a.refresh)
    else:
        print("specify --list / --embed --xnum N / --revert", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
