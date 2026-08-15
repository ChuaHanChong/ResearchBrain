#!/usr/bin/env python3
"""Drive a cmux browser to generate alphaxiv overviews for papers whose Detailed Report is missing.

`retrieve.fetch_research_report` 404s until alphaxiv generates that paper's overview — this only
affects the Detailed Report, not the five short fields. Patches the report into the existing KH note
in place once generated, no note regeneration. Run in the foreground or a harness-managed background —
nohup breaks cmux's socket eval.

Usage:
    python generate_overviews.py --missing-reports        # every KH note lacking ## Detailed Report
    python generate_overviews.py --ids 2606.18426 2603.11980
    python generate_overviews.py --ids-file failed.json    # json array or newline-delimited txt
    python generate_overviews.py --pending                 # every knowledge.py ID with no KH note at all
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

from common import ABS_URL, ARXIV_ID_RE, KH_DIR, overview_link_selector
from retrieve import fetch_research_report

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
    """Eval the page state and parse its JSON, retrying transient empty reads."""
    # The first read after navigation is often empty (browser warm-up) — one empty read isn't a failure.
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
    """Load /abs/<id> and click through to reveal the overview. Returns ok/navfail."""
    # The direct /overview/ SSR route is per-IP rate-limited (HTTP 500); the in-app soft-nav from
    # /abs/ is not — and alphaxiv embeds the overview on /abs/ itself anyway.
    if cmux(surface, "goto", ABS_URL.format(paper_id)).startswith("__ERR__"):
        return "navfail"
    cmux(surface, "wait", "--load-state", "complete", "--timeout", "25")
    time.sleep(3)
    sel = overview_link_selector(paper_id)
    link_js = (f'(() => {{ const a = document.querySelector("{sel}"); '
               'if (!a) return "no-link"; a.click(); return "clicked"; })()')
    cmux(surface, "eval", link_js)  # best-effort; /overview/ 302s to /abs/ anyway, so no fallback nav needed
    cmux(surface, "wait", "--load-state", "complete", "--timeout", "25")
    return "ok"


def generate_one(surface: str, paper_id: str, per_timeout: int, poll: int = 7) -> str:
    """Generate one paper's overview; returns an outcome string."""
    # Outcomes: already / generated / timeout / withdrawn / probe-fail / navfail.
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
    """Resolve the target arxiv IDs from --ids, --ids-file, --pending, or --missing-reports."""
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
    if args.missing_reports:
        notes = Path(args.kh_dir).glob("*.md")
        return sorted(
            (p.stem for p in notes if re.match(rf"^{ARXIV_ID_RE}$", p.stem)
             and "## Detailed Report" not in p.read_text(encoding="utf-8")),
            key=lambda i: (int(i.split(".")[0]), int(i.split(".")[1])),
        )
    sys.exit("provide --ids, --ids-file, --pending, or --missing-reports")


def patch_detailed_report(kh_dir: str, paper_id: str) -> str:
    """Fetch a paper's now-generated Detailed Report and append it to its existing KH note in place."""
    # Only for notes that already exist and already have their five fields — this never regenerates
    # a note, it only backfills the one section that depends on alphaxiv having an overview.
    note_path = Path(kh_dir) / f"{paper_id}.md"
    if not note_path.exists():
        return "note-missing"
    text = note_path.read_text(encoding="utf-8")
    if "## Detailed Report" in text:
        return "already-has-report"
    kh_ids = {p.stem for p in Path(kh_dir).glob("*.md")}
    # cmux just confirmed the overview is rendered server-side, but the `.md` endpoint is a separate
    # request and can lag briefly behind — retry rather than treat a fresh generation as a dead end.
    report = ""
    for attempt in range(3):
        report = fetch_research_report(paper_id, kh_ids)
        if report.strip():
            break
        if attempt < 2:
            time.sleep(5)
    if not report.strip():
        return "fetch-failed"
    note_path.write_text(text.rstrip("\n") + f"\n\n## Detailed Report\n\n{report}\n", encoding="utf-8")
    return "patched"


def main() -> None:
    """Parse args, open a cmux surface, generate each target paper's overview, and report outcomes."""
    parser = argparse.ArgumentParser(description="Auto-generate alphaxiv overviews via cmux browser.")
    parser.add_argument("--ids", nargs="*", help="explicit arxiv IDs")
    parser.add_argument("--ids-file", help="JSON array or newline-delimited file of IDs")
    parser.add_argument("--pending", action="store_true", help="target every knowledge.py ID with no KH note")
    parser.add_argument("--missing-reports", action="store_true", help="target every KH note lacking ## Detailed Report")
    parser.add_argument("--knowledge", default=".claude/skills/alphaxiv-summary-extract/scripts/knowledge.py")
    parser.add_argument("--kh-dir", default=KH_DIR)
    parser.add_argument("--surface", help="reuse an existing cmux surface (e.g. surface:51)")
    parser.add_argument("--no-visible", action="store_true", help="open the surface unfocused (default: visible)")
    parser.add_argument("--timeout", type=int, default=360, help="max seconds to wait per paper (default 360)")
    args = parser.parse_args()

    ids = load_ids(args)
    if args.pending and args.kh_dir and Path(args.kh_dir).is_dir():
        have = {p.stem for p in Path(args.kh_dir).glob("*.md")}
        ids = [i for i in ids if i not in have]  # --pending only: skip papers already ingested
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
        # A note that already exists (--missing-reports, or a --pending id ingested meanwhile) gets
        # its Detailed Report backfilled in place — no note regeneration, no re-running content synthesis.
        if outcome in ("generated", "already"):
            patch_outcome = patch_detailed_report(args.kh_dir, paper_id)
            outcome = f"{outcome}+{patch_outcome}"
        stats[outcome] = stats.get(outcome, 0) + 1
        print(f"[{n:>3}/{len(ids)}] {paper_id}  {outcome}  ({int(time.time() - start)}s)", flush=True)
    print(f"\nDONE  {json.dumps(stats)}")
    print("Existing notes patched in place (+patched). For any ID with no KH note yet, run")
    print("extract_summaries.py now — its Detailed Report fetch will succeed immediately.")


if __name__ == "__main__":
    main()
