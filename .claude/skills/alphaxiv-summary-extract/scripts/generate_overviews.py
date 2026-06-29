#!/usr/bin/env python3
"""Drive a cmux browser to generate the alphaxiv overview pages for papers
that failed to scrape (those with no pre-generated overview), so `extract_summaries.py --force` can then ingest
them. Run it in the foreground or a harness-managed background — nohup breaks cmux's socket eval.
See the SKILL.md "rescue" section for the why and the gotchas; the inline comments cover the
completion-detection logic.

Usage:
    python generate_overviews.py --ids 2606.18426 2603.11980
    python generate_overviews.py --ids-file failed.json   # json array or newline-delimited txt
    python generate_overviews.py --pending                # every knowledge.py ID with no KH note
    python generate_overviews.py --ids 2606.18426 --surface surface:51
"""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from common import ABS_URL, ARXIV_ID_RE, KH_DIR, OVERVIEW_URL, overview_link_selector

# Probe the page state: is the Generate button present, and is the overview fully rendered?
PROBE_JS = r"""(() => {
  const body = document.body.innerText || "";
  const genBtn = [...document.querySelectorAll("button")].some(b => /generate overview/i.test(b.textContent||""));
  const heads = [...document.querySelectorAll("h1,h2,h3")].map(h => (h.textContent||"").trim().toLowerCase());
  const hasToC = heads.some(h => h.includes("table of contents"));
  const err = /page not found|404|does not exist|couldn.t find|no longer available|error loading/i.test(body);
  return JSON.stringify({genBtn: genBtn, hasToC: hasToC, len: body.length, err: err});
})()"""

# Click the "Generate Overview" button if present.
CLICK_JS = r"""(() => {
  const b = [...document.querySelectorAll("button")].find(x => /generate overview/i.test(x.textContent||""));
  if (!b) return "no-btn";
  b.click();
  return "clicked";
})()"""


def cmux(surface: str, *args: str, timeout: int = 40) -> str:
    """Run a `cmux browser --surface <surface> ...` command and return its stripped stdout."""
    try:
        result = subprocess.run(
            ["cmux", "browser", "--surface", surface, *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return (result.stdout or "").strip()
    except Exception as exc:
        return f"__ERR__ {exc}"


def open_surface(first_url: str, visible: bool) -> str:
    """Open (or reuse) a cmux browser surface and return its ref (e.g. 'surface:51')."""
    flag = "true" if visible else "false"
    opened = subprocess.run(
        ["cmux", "browser", "open", first_url, "--focus", flag],
        capture_output=True,
        text=True,
        timeout=40,
    ).stdout
    match = re.search(r"surface:\d+", opened or "")
    if match:
        return match.group(0)
    identified = subprocess.run(
        ["cmux", "browser", "identify"], capture_output=True, text=True
    ).stdout
    match = re.search(r"surface:\d+", identified or "")
    if not match:
        sys.exit("could not resolve a cmux browser surface")
    return match.group(0)


def probe(surface: str, retries: int = 4) -> Optional[dict]:
    """Eval the page state and parse its JSON. Retries because the first read after navigation
    is often empty (browser warm-up) — one empty read is not a failure."""
    last = ""
    for _ in range(retries):
        last = cmux(surface, "eval", PROBE_JS)
        try:
            return json.loads(last)
        except Exception:
            time.sleep(3)
    print(f"      [probe empty] {last!r:.120}  (if EVERY paper shows this, you backgrounded with nohup — don't)")
    return None


def is_done(state: Optional[dict]) -> bool:
    """Strong/fast completion signal: a fully-rendered overview with a Table-of-Contents heading."""
    return bool(state and state.get("hasToC") and state.get("len", 0) > 5000)


def open_overview(surface: str, paper_id: str) -> str:
    """Reach /overview/<id> by clicking through from /abs/ — the direct /overview/ SSR route is
    per-IP rate-limited (HTTP 500), but the in-app soft-nav from /abs/ is not. Returns ok/navfail."""
    if cmux(surface, "goto", ABS_URL.format(paper_id)).startswith("__ERR__"):
        return "navfail"
    cmux(surface, "wait", "--load-state", "complete", "--timeout", "25")
    time.sleep(3)
    sel = overview_link_selector(paper_id)
    link_js = (f'(() => {{ const a = document.querySelector("{sel}"); '
               'if (!a) return "no-link"; a.click(); return "clicked"; })()')
    if "clicked" not in cmux(surface, "eval", link_js):
        cmux(surface, "goto", OVERVIEW_URL.format(paper_id))  # link not rendered — fall back to direct nav
    cmux(surface, "wait", "--load-state", "complete", "--timeout", "25")
    return "ok"


def generate_one(surface: str, paper_id: str, per_timeout: int, poll: int = 7) -> str:
    """Generate one paper's overview. Returns an outcome: already / generated / timeout /
    withdrawn / probe-fail / navfail."""
    if open_overview(surface, paper_id) == "navfail":
        return "navfail"
    time.sleep(3)
    state = probe(surface)
    if state is None:
        return "probe-fail"
    if state.get("err"):
        return "withdrawn"  # 404 / withdrawn — nothing to generate
    if is_done(state):
        return "already"  # overview already exists
    if state.get("genBtn") and "clicked" not in cmux(surface, "eval", CLICK_JS):
        time.sleep(2)
        cmux(surface, "eval", CLICK_JS)  # first click didn't register — retry once

    # Done = ToC heading + large body (fast, strong), OR a button-free large body that stopped
    # growing across two polls — the stream finished even without a ToC (older/short papers).
    start = time.time()
    prev_len = -1
    stable = 0
    while time.time() - start < per_timeout:
        time.sleep(poll)
        state = probe(surface)
        if not state:
            continue
        if is_done(state):
            return "generated"
        if not state.get("genBtn") and state.get("len", 0) > 6000:
            stable = stable + 1 if abs(state["len"] - prev_len) < 200 else 0
            prev_len = state["len"]
            if stable >= 2:  # ~2 polls (~14s) of a stable, button-free, sizable page
                return "generated"
        elif state.get("genBtn"):  # click didn't register — retry and reset stability
            cmux(surface, "eval", CLICK_JS)
            stable = 0
            prev_len = -1
    return "timeout"


def load_ids(args: argparse.Namespace) -> list:
    """Resolve the target arxiv IDs from --ids, --ids-file, or --pending."""
    if args.ids:
        return list(dict.fromkeys(args.ids))
    if args.ids_file:
        raw = Path(args.ids_file).read_text(encoding="utf-8").strip()
        try:
            return list(dict.fromkeys(json.loads(raw)))
        except Exception:
            return list(dict.fromkeys(re.findall(ARXIV_ID_RE, raw)))
    if args.pending:
        knowledge = Path(args.knowledge).read_text(encoding="utf-8")
        kp = set(re.findall(rf"arxiv\.org/abs/({ARXIV_ID_RE})", knowledge))
        kh = {p.stem for p in Path(args.kh_dir).glob("*.md") if re.match(rf"^{ARXIV_ID_RE}$", p.stem)}
        return sorted(kp - kh, key=lambda i: (int(i.split(".")[0]), int(i.split(".")[1])))
    sys.exit("provide --ids, --ids-file, or --pending")


def main() -> None:
    """Parse args, open a cmux surface, and generate the overview for each target paper, reporting outcomes."""
    parser = argparse.ArgumentParser(description="Auto-generate alphaxiv overviews via cmux browser.")
    parser.add_argument("--ids", nargs="*", help="explicit arxiv IDs")
    parser.add_argument("--ids-file", help="JSON array or newline-delimited file of IDs")
    parser.add_argument("--pending", action="store_true", help="target every knowledge.py ID with no KH note")
    parser.add_argument("--knowledge", default=".claude/skills/alphaxiv-summary-extract/scripts/knowledge.py")
    parser.add_argument("--kh-dir", default=KH_DIR)
    parser.add_argument("--surface", help="reuse an existing cmux surface (e.g. surface:51)")
    parser.add_argument("--no-visible", action="store_true", help="open the surface unfocused (default: visible)")
    parser.add_argument("--timeout", type=int, default=360, help="max seconds to wait per paper (default 360)")
    args = parser.parse_args()

    ids = load_ids(args)
    if args.kh_dir and Path(args.kh_dir).is_dir():
        have = {p.stem for p in Path(args.kh_dir).glob("*.md")}
        ids = [i for i in ids if i not in have]  # skip papers already ingested
    if not ids:
        print("nothing to generate (0 papers)")
        return

    surface = args.surface or open_surface(ABS_URL.format(ids[0]), visible=not args.no_visible)
    print(f"surface={surface} | {len(ids)} papers | timeout={args.timeout}s/paper")
    print("NOTE: keep this in the foreground or a harness-managed background — nohup breaks cmux eval.\n")

    stats = {}
    for n, paper_id in enumerate(ids, 1):
        start = time.time()
        outcome = generate_one(surface, paper_id, args.timeout)
        stats[outcome] = stats.get(outcome, 0) + 1
        print(f"[{n:>3}/{len(ids)}] {paper_id}  {outcome}  ({int(time.time() - start)}s)", flush=True)
    print(f"\nDONE  {json.dumps(stats)}")
    print("Next: re-run extract_summaries.py --force on the still-missing IDs to ingest the newly-generated overviews.")


if __name__ == "__main__":
    main()
