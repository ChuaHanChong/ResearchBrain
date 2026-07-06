#!/usr/bin/env python3
"""Per-report format validator for the ## Detailed Report section of KnowledgeHub notes.

Checks every note against all format rules, prints `checked N | PASS x | FAIL y` with the failing
notes and a reason tally, and exits non-zero if any fail. FAIL 0 is necessary but not sufficient:
still read a sample, since regex under-counts judgement cases.

Usage:
    python validate_reports.py   # from the vault root
"""
import re
import sys
from pathlib import Path
from collections import Counter
from collections.abc import Iterator

from common import KH_DIR

KH = Path(KH_DIR)
KH_IDS = {p.stem for p in KH.glob("*.md")}

# A self-title heading: a report/analysis descriptor restating the paper title, at the top.
SELF = re.compile(r'^#{3,5} \d+(?:\.\d+)*\. '
                  r'((Detailed |In-Depth |Comprehensive )?(Research )?(Paper )?(Report|Analysis|Summary)\b.*:'
                  r'|Report on\b)', re.I)
HEAD = re.compile(r'^(#{3,6}) (.*)$')          # any ###/####/#####/###### heading
NUMHEAD = re.compile(r'^(#{3,6}) (\d+(?:\.\d+)*)\.\s+(.*)$')   # numbered heading -> (hashes, number, title)


def _headings(lines: list[str]) -> Iterator[tuple]:
    """Yield (index, level, number-or-None, title) for every heading outside code fences."""
    fence = False
    for i, l in enumerate(lines):
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence:
            continue
        h = HEAD.match(l)
        if not h:
            continue
        lvl = len(h.group(1))
        nm = NUMHEAD.match(l)
        if nm:
            yield i, lvl, nm.group(2), nm.group(3)
        else:
            yield i, lvl, None, h.group(2)


def check(t: str) -> list[str]:
    """Return a list of format issues for one note's text, or [] if its ## Detailed Report is clean."""
    issues = []
    if "## Research Report" in t:
        issues.append("old-heading '## Research Report'")
    if "\n\n\n" in t:
        issues.append("triple-newline")

    m = re.search(r'^## Detailed Report[ \t]*$', t, re.M)
    if not m:
        return ["NO '## Detailed Report' section"]
    body = t[m.end():]
    if not body.strip():
        return ["EMPTY report"]

    bl = body.split("\n")
    L = t[m.start():].split("\n")
    heads = list(_headings(bl))               # (idx, level, number, title) within body

    # ---- section presence / lead content ----
    if not heads:
        issues.append("no ###/#### headings")
    for l in bl:
        if HEAD.match(l):
            break
        if l.strip():
            issues.append("lead-content before first heading")
            break

    # ---- heading numbering + level ----
    if any(lv >= 6 for _, lv, _, _ in heads):
        issues.append("heading deeper than ##### (H6+)")
    if heads and heads[0][1] != 3:
        issues.append(f"first heading is H{heads[0][1]} (should be ### )")
    for _, lv, num, title in heads:
        if num is None:
            issues.append(f"unnumbered heading: {title[:40]!r}")
            break
    # numbers must be present, sequential-from-1 per level, parents must exist, no dups
    prims = [num for _, lv, num, _ in heads if lv == 3 and num]
    if prims and [int(n) for n in prims] != list(range(1, len(prims) + 1)):
        issues.append(f"primaries not sequential-from-1: {prims}")
    allnums = [num for _, _, num, _ in heads if num]
    if "0" in [n.split(".")[0] for n in allnums]:
        issues.append("heading numbered under phantom parent '0.'")
    if len(allnums) != len(set(allnums)):
        dups = [n for n, c in Counter(allnums).items() if c > 1]
        issues.append(f"duplicate heading numbers: {dups}")
    # parent existence: N.M needs N ; N.M.K needs N.M
    numset = set(allnums)
    for n in allnums:
        parts = n.split(".")
        if len(parts) >= 2 and ".".join(parts[:-1]) not in numset:
            issues.append(f"heading with missing parent: {n}")
            break
    # leftover double-number in a title (e.g. "#### 3.1. 4.1 Foo")
    if any(re.match(r'^\d+(?:\.\d+)*\.?\s', title) for _, _, num, title in heads if num):
        issues.append("double-number in heading title")

    # ---- heading cleanliness (all levels) ----
    if any("**" in l for l in bl if HEAD.match(l)):
        issues.append("bold in heading")
    if any(re.match(r'^#{3,6} .*:\s*$', l) for l in bl if HEAD.match(l)):
        issues.append("heading ends with colon")
    # a self-title only ever appears as the FIRST heading (a title restatement); a deep
    # "#### 4.3. Analysis: X" is legitimate content, not a self-title.
    first_head = next((bl[i] for i, _, _, _ in heads[:1]), "")
    if SELF.match(first_head):
        issues.append("self-title heading")

    # ---- empty sections (heading with no content before next same/higher-level heading) ----
    hpos = [(i, lv) for i, lv, _, _ in heads]
    for idx, (i, lv) in enumerate(hpos):
        nxt = next((hpos[j][0] for j in range(idx + 1, len(hpos)) if hpos[j][1] <= lv), len(bl))
        if not any(x.strip() for x in bl[i + 1:nxt]):
            issues.append("empty section (heading with no content)")
            break

    # ---- blank line before + after every heading (fence-aware via L over whole tail) ----
    fence = False
    for j, l in enumerate(L):
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence or not HEAD.match(l):
            continue
        if j + 1 < len(L) and L[j + 1].strip():
            issues.append("heading glued to content BELOW"); break
    fence = False
    for j, l in enumerate(L):
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence or not HEAD.match(l):
            continue
        if j > 0 and L[j - 1].strip():
            issues.append("heading glued to content ABOVE"); break

    # ---- content cleanliness ----
    if "analysis of the research paper" in body:
        issues.append("boilerplate sentence")
    if re.search(r'(?im)^(#{3,6}[ 0-9.]*|\*\*[ 0-9.]*)(Authors?|Institutions?)\b', body):
        issues.append("author/institution section")
    if re.search(r'^\s*!\[', body, re.M):
        issues.append("figure embed")
    if re.search(r'^\s*(---|\*\*\*|___)\s*$', body, re.M):
        issues.append("horizontal rule")

    # ---- bold pseudo-headings & dangling colons (fence-aware; the opus review surfaced these) ----
    canon = (r'(How This Work Fits|Key Objectives and Motivation|Methodology and Approach'
             r'|Main Findings and Results|Significance and Potential Impact)')
    fence = False
    for i, l in enumerate(bl):
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence:
            continue
        # a numbered bold line acting as a sub-heading, e.g. "**4.1 Model Architecture**" — should be #### N.M
        if re.match(r'^\*\*\d+(?:\.\d+)+\.?\s+.+\*\*:?\s*$', l):
            issues.append("bold pseudo-sub-heading (**N.M …**) — should be a #### heading")
            break
    fence = False
    for l in bl:
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence:
            continue
        # a canonical section title rendered as a standalone bold line instead of a ### heading
        if re.match(r'^\*\*' + canon + r'[^*]*:?\*\*\s*$', l):
            issues.append("canonical section as bold pseudo-heading (not ###)")
            break
    # a prose sentence ending ':' immediately before a ### primary (its figure/list was stripped)
    for i in range(len(bl) - 1):
        l = bl[i]
        if (re.search(r'[a-z][a-z ]+:\s*$', l) and not l.strip().startswith(('-', '#', '*'))
                and len(l.strip()) > 25):
            j = i + 1
            while j < len(bl) and not bl[j].strip():
                j += 1
            if j < len(bl) and re.match(r'^### ', bl[j]):
                issues.append("dangling colon sentence before a ### primary (stripped figure/list)")
                break
    # inline numbered bold label, e.g. "**6.1. Title:** text" — the off-by-one number should be stripped
    fence = False
    for l in bl:
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence:
            continue
        if re.match(r'^\*\*\d+\.\d+\.?\s+[^*]+:\*\* \S', l):
            issues.append("inline numbered bold label (**N.M Title:** …) — strip the number prefix")
            break

    # ---- garbled punctuation left by [N]-citation stripping (outside code fences) ----
    prose = re.sub(r'```.*?```', '', body, flags=re.S)
    if re.search(r'\S,,', prose):
        issues.append("doubled comma ',,' (stripped citation)")
    if re.search(r'[A-Za-z]–[\s,.;:)\]]', prose):
        issues.append("dangling en-dash after word (stripped citation range)")
    if re.search(r'\(\s*[–\-,;\s]+\s*\)', prose):
        issues.append("paren remnant of stripped citations '(,,)'/'(–)'")

    # ---- mangled inline math: subscripts/superscripts split onto their own lines ----
    # e.g. source rendered "$\pi_Q$" as "(π\nQ\n)". Signature: many lone 1-2 char tokens on
    # their own line (a Greek/Latin/digit subscript). Well-formed reports keep paragraphs on
    # one line, so a cluster of these means the extraction broke the math across lines.
    lone = 0
    fence = False
    for l in bl:
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence:
            continue
        if re.fullmatch(r'[A-Za-zδθβγλμσπΘΦΨΩαρτφψωΔΣΠ0-9]{1,2}', l.strip()):
            lone += 1
    if lone >= 4:
        issues.append(f"mangled inline math ({lone} lone subscript/superscript lines)")

    # ---- bullets + whitespace (skip code fences) ----
    fence = False
    for l in bl:
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence:
            continue
        if re.match(r'^\s*[*+]\s+\S', l):
            issues.append("* or + bullet"); break
    if any(re.match(r'^\s*-\s{2,}\S', l) for l in bl):
        issues.append("multi-space after dash")
    if any(l != l.rstrip() for l in bl):
        issues.append("trailing whitespace")
    if any(re.match(r'^\s*-\s*$', l) for l in bl):
        issues.append("empty bullet")

    # ---- inline [N] citations (outside code fences, not wikilinks/callouts) ----
    fence = False
    for l in bl:
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence:
            continue
        if re.search(r'(?<!\[)\[\d+\](?!\])', l):
            issues.append("inline [N] citation"); break

    # ---- every in-KH cited paper wikilinked (markdown-link OR bare id) ----
    linked = set(re.findall(r'\[\[([0-9]{4}\.[0-9]{4,5})', body))
    for mm in re.finditer(r'\[[^\]]+\]\([^)]*?/abs/([0-9]{4}\.[0-9]{4,5})', body):
        if mm.group(1) in KH_IDS:
            issues.append(f"in-KH citation not linked (md): {mm.group(1)}"); break
    masked = re.sub(r'\[\[[^\]]*\]\]', '', body)
    masked = re.sub(r'```.*?```', '', masked, flags=re.S)
    for mm in re.finditer(r'(?<![\w.])([0-9]{4}\.[0-9]{4,5})(?![\w])', masked):
        if mm.group(1) in KH_IDS and mm.group(1) not in linked:
            issues.append(f"in-KH citation not linked (bare): {mm.group(1)}"); break

    return issues


def main() -> None:
    """Validate every KH note and print PASS/FAIL counts, the failing notes, and a reason tally."""
    total = failed = 0
    reasons = Counter()
    fails = []
    for p in sorted(KH.glob("*.md")):
        total += 1
        iss = check(p.read_text(encoding="utf-8"))
        if iss:
            failed += 1
            fails.append((p.stem, iss))
            for i in iss:
                reasons[i.split(":")[0]] += 1
    print(f"checked {total} notes | PASS {total - failed} | FAIL {failed}\n")
    if fails:
        print("=== failing notes ===")
        for name, iss in fails[:80]:
            print(f"  {name}: {'; '.join(iss)}")
        if len(fails) > 80:
            print(f"  ... and {len(fails) - 80} more")
        print("\n=== reason tally ===")
        for r, c in reasons.most_common():
            print(f"  {c:>4}  {r}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
