#!/usr/bin/env python3
"""Drive a cmux browser to fill the Detailed Report of KH notes that are missing one.

The report comes from alphaxiv's `overview/{id}.md` intermediate report when it exists; otherwise from
the abs page's AI OVERVIEW panel, copied as markdown via its Copy button (alphaxiv's 2026-09 UI no longer
publishes a `.md` for newly generated overviews). Patches the existing KH note in place, no note
regeneration. Run in the foreground — nohup and `run_in_background` both break cmux's socket eval.

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
from format_reports import format_report
from retrieve import fetch_research_report
from validate_reports import check

MIN_OVERVIEW_CHARS = 1500  # smallest real AI overview seen was ~4.3k chars; below this the copy failed
CLIPBOARD_SETTLE_SECONDS = 2  # Copy click -> pbpaste; 2s was enough on all 101 rescued notes

# Locate the abs page's "AI OVERVIEW" panel; its container sits 4 ancestors above the label leaf.
_AI_PANEL_JS = r"""
  const leaf = [...document.querySelectorAll("*")].find(x => x.childElementCount === 0 && /^AI OVERVIEW$/i.test((x.textContent||"").trim()));
  let box = leaf; for (let i = 0; leaf && i < 4; i++) box = box.parentElement;
"""

# Page state: is the AI overview rendered (Copy button, no progress text), and is the page an error page?
PROBE_JS = r"""(() => {""" + _AI_PANEL_JS + r"""
  const body = document.body.innerText || "";
  const t = box ? (box.innerText || "") : "";
  const copy = !!box && [...box.querySelectorAll("button")].some(b => /^copy$/i.test((b.textContent||"").trim()));
  const gen = [...document.querySelectorAll("button")].some(b => /generate/i.test(b.textContent||"") && !/audio/i.test(b.textContent||""));
  // A real paper page shows its ABSTRACT, whose own text can contain these phrases (2609.35200's says "no longer available").
  const err = !/\bABSTRACT\b/.test(body) && /page not found|does not exist|couldn.t find|no longer available|error loading/i.test(body.slice(0, 2000));
  // Progress is "Reading the paper" or a bare N% line; a percentage inside overview prose (2609.38905: "14.0% of the time") is not.
  return JSON.stringify({found: !!leaf, copy: copy, progress: /Reading the paper|^\s*\d{1,3}%\s*$/im.test(t.slice(0, 300)), gen: gen, len: t.length, err: err});
})()"""

# Click a generate button if one is present (the AI overview usually auto-generates on visit).
CLICK_JS = r"""(() => {
  const b = [...document.querySelectorAll("button")].find(x => /generate/i.test(x.textContent||"") && !/audio/i.test(x.textContent||""));
  if (!b) return "no-btn";
  b.click();
  return "clicked";
})()"""

# Click the AI overview's Copy button, which puts the overview's markdown on the clipboard.
COPY_JS = r"""(() => {""" + _AI_PANEL_JS + r"""
  if (!box) return "no-panel";
  const b = [...box.querySelectorAll("button")].find(x => /^copy$/i.test((x.textContent||"").trim()));
  if (!b) return "no-copy";
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
    """Return True when the AI overview has finished rendering (Copy button present, no progress text)."""
    return bool(state and state.get("copy") and not state.get("progress"))


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
    if state.get("gen"):
        cmux(surface, "eval", CLICK_JS)

    start = time.time()
    while time.time() - start < per_timeout:
        time.sleep(poll)
        state = probe(surface)
        if is_done(state):
            return "generated"
        if state and state.get("gen"):  # a click that didn't register — retry
            cmux(surface, "eval", CLICK_JS)
    return "timeout"


def copy_ai_overview(surface: str) -> str:
    """Click the rendered AI overview's Copy button and return the clipboard markdown ("" on failure)."""
    # macOS clipboard (pbcopy/pbpaste): the Copy button is the only way to get the overview as markdown.
    subprocess.run(["pbcopy"], input="", text=True)
    if "clicked" not in cmux(surface, "eval", COPY_JS):
        return ""
    time.sleep(CLIPBOARD_SETTLE_SECONDS)
    return subprocess.run(["pbpaste"], capture_output=True, text=True).stdout


def ai_overview_to_report(raw_md: str, kh_ids: set, paper_id: str) -> str:
    """Format copied AI-overview markdown into a Detailed Report body (intro kept, [pN] cites dropped)."""
    raw_md = re.sub(r"\[p\d+(?:[,\u2013-]\s*p?\d+)*\]", "", raw_md)

    def _link(match: "re.Match") -> str:
        """Rewrite an alphaxiv/arxiv markdown link: self-link to plain text, in-vault paper to a wikilink."""
        text, pid = match.group(1), match.group(2)
        if pid == paper_id:
            return text
        return f"[[{pid}|{text}]]" if pid in kh_ids else match.group(0)

    raw_md = re.sub(
        r"\[([^\]]+)\]\(https?://(?:www\.)?(?:alphaxiv|arxiv)\.org/(?:abs|overview|pdf)/(\d{4}\.\d{4,5})[^)]*\)",
        _link, raw_md)
    if not raw_md.lstrip().startswith("#"):
        raw_md = "## Overview\n\n" + raw_md  # format_report drops text before the first heading
    return format_report(raw_md, kh_ids)


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


def patch_detailed_report(kh_dir: str, paper_id: str, surface: Optional[str] = None) -> str:
    """Fetch a paper's Detailed Report (.md, else the page's AI overview) and append it to its KH note."""
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
    for attempt in range(2):
        report = fetch_research_report(paper_id, kh_ids)
        if report.strip():
            break
        if attempt < 1:
            time.sleep(5)
    source = "md"
    if not report.strip() and surface:
        # No intermediate report: fall back to the AI overview the browser just confirmed is rendered.
        raw = copy_ai_overview(surface)
        if len(raw) < MIN_OVERVIEW_CHARS:
            return "copy-failed"
        report, source = ai_overview_to_report(raw, kh_ids, paper_id), "ai-overview"
    if not report.strip():
        return "fetch-failed"
    patched = text.rstrip("\n") + f"\n\n## Detailed Report\n\n{report}\n"
    problems = check(patched)
    if problems:
        return f"validate-fail {problems}"
    note_path.write_text(patched, encoding="utf-8")
    return f"patched-{source}"


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
            patch_outcome = patch_detailed_report(args.kh_dir, paper_id, surface)
            outcome = f"{outcome}+{patch_outcome}"
        stats[outcome] = stats.get(outcome, 0) + 1
        print(f"[{n:>3}/{len(ids)}] {paper_id}  {outcome}  ({int(time.time() - start)}s)", flush=True)
    print(f"\nDONE  {json.dumps(stats)}")
    print("Existing notes patched in place (+patched). For any ID with no KH note yet, run")
    print("extract_summaries.py now — its Detailed Report fetch will succeed immediately.")


if __name__ == "__main__":
    main()
