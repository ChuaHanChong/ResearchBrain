#!/usr/bin/env python3
"""Extract a paper's pipeline figure from its alphaxiv OVERVIEW page
(headless Chromium): alphaxiv's own alt-label + caption + the CDN image, then embed a chosen
figure (verbatim alphaxiv caption) under the KH note's ``## Method``.

The alphaxiv overview curates the paper's key figures and writes a clean caption
+ a short alt-label for each (e.g. alt "ADAPT Framework Overview"), so the
alt-label usually flags the pipeline/architecture figure. You (the agent) still
VISUALLY inspect the candidates and pick the real pipeline diagram.

Usage:
    uv run python alphaxiv_figures.py {ID} --list                # scrape overview, download figs, print JSON
    uv run python alphaxiv_figures.py {ID} --embed --xnum N      # embed figure xN with its alphaxiv caption (verbatim)
    uv run python alphaxiv_figures.py {ID} --revert              # remove any embed + png

--list writes a cache: data/figures/_alphaxiv/{ID}/x{N}.png + data/figures/_alphaxiv/{ID}.json
(so --embed reuses the exact alphaxiv caption). Re-run --list with --refresh to re-scrape.
"""

import argparse
import json
import os
import re
import shutil
import sys
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

H = {"User-Agent": "Mozilla/5.0"}
KH_DIR = "_KnowledgeHub_"           # vault-relative KnowledgeHub notes dir
FIGURES_DIR = "data/figures"        # vault-relative figures output dir
CACHE = f"{FIGURES_DIR}/_alphaxiv"  # per-paper overview-figure cache


def _driver() -> webdriver.Chrome:
    """Build and return a headless Chromium Selenium webdriver."""
    o = Options()
    for a in ["--headless=new", "--no-sandbox", "--disable-gpu",
              "--window-size=1400,5000", "--disable-dev-shm-usage"]:
        o.add_argument(a)
    return webdriver.Chrome(options=o)


def scrape(pid: str) -> list[dict]:
    """Load the alphaxiv overview and return [{xnum, alt, caption, src}] for its curated figures."""
    d = _driver()
    figs = []
    try:
        d.get(f"https://www.alphaxiv.org/overview/{pid}")
        time.sleep(4)
        # poll: scroll + wait until the lazy-loaded figures appear (a fixed wait misses slow loads)
        for _ in range(8):
            h = d.execute_script("return document.body.scrollHeight")
            for y in range(0, h + 900, 900):
                d.execute_script(f"window.scrollTo(0,{y})")
                time.sleep(0.15)
            time.sleep(1.5)
            if d.find_elements("css selector", "img[src*='paper-assets']"):
                break
        time.sleep(1)
        seen = set()
        for im in d.find_elements("css selector", "img[src*='paper-assets']"):
            src = im.get_attribute("src") or ""
            # accept any /figures image (alphaxiv names them x{N}.png, img-{N}.jpeg, {name}-fig.png, ...)
            if "/figure" not in src or src in seen:
                continue
            seen.add(src)
            base = src.rsplit("/", 1)[-1]
            m = re.search(r"(\d+)\.(?:png|jpe?g|webp)$", base)
            xnum = m.group(1) if m else str(len(figs))
            if any(f["xnum"] == xnum for f in figs):  # keep ids unique within a paper
                xnum = f"f{len(figs)}"
            cap = ""
            try:
                cap = im.find_element("xpath", "./ancestor::*[1]").text.replace("\n", " ").strip()
            except Exception:
                pass
            figs.append({"xnum": xnum, "alt": im.get_attribute("alt") or "",
                         "caption": cap[:500], "src": src})
    finally:
        d.quit()
    return figs


def cmd_list(pid: str, refresh: bool = False, quiet: bool = False) -> None:
    """Scrape the overview, download figures to cache, and print the figure JSON (--list)."""
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
    """Embed cached figure xN with its verbatim alphaxiv caption under the note's Method (--embed)."""
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
    cap = re.sub(r"\s+", " ", fig["caption"]).strip()  # alphaxiv caption, verbatim (only whitespace collapsed)
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
