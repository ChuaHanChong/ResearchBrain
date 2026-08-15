"""Format alphaxiv's raw overview `.md` into a clean, validator-passing ## Detailed Report body.

Consolidates the cleanup a newly-ingested KH Detailed Report needs: heading hierarchy + numbering,
boilerplate/figure/citation removal, in-KH citation wikilinks, mangled-math rejoin, and punctuation.
`format_report` runs the pipeline (each step is a helper below); `validate_reports.py` has the checks.
"""
import re
from collections.abc import Set

SELF = re.compile(
    r'^((Detailed |In-Depth |Comprehensive )?(Research )?(Paper )?(Report|Analysis|Summary)\b'
    r'|Report on\b|Analysis of )', re.I)
GREEK = 'δθβγλμσπΘΦΨΩαρτφψωϕ𝒒𝑞'
LONE = re.compile(r'^[A-Za-z0-9' + GREEK + r'⃗ˆ./,]{1,6}$')


def _author(t: str) -> bool: return bool(re.search(r'\bauthors?\b|institution', t, re.I))
def _selft(t: str) -> bool: return bool(SELF.match(t))
def _clean_title(t: str) -> str: return re.sub(r'^\d+(?:\.\d+)*\.?\s+', '', t.replace("**", "").strip()).strip().rstrip(":").strip()


def _pre_convert_bold_headings(lines: list[str]) -> list[str]:
    """Turn standalone bold pseudo-headings into markdown headings, when the render is mostly bold."""
    # A numbered bold sub-heading `**4.1 Title**` always becomes a sub (`#### `); `**N Title**` /
    # `**Title:**` become primaries only in the bold-only case, so inline labels like `**Metrics:**`
    # inside a normally-headed report are left as content.
    fence = False
    md_headings = 0
    for l in lines:
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if not fence and re.match(r'^#{1,6}\s', l):
            md_headings += 1
    bold_only = md_headings < 2
    out = []
    fence = False
    for l in lines:
        if re.match(r'^\s*```', l):
            fence = not fence
            out.append(l)
            continue
        if fence:
            out.append(l)
            continue
        # numbered bold sub-heading, e.g. "**4.1 Task Formulation**" -> "#### Task Formulation"
        m = re.match(r'^\*\*(\d+(?:\.\d+)+)\.?\s+(.+?):?\*\*:?\s*$', l)
        if m:
            depth = m.group(1).count(".")
            out.append(f"{'#' * (3 + min(depth, 2))} {m.group(2).strip()}")
            continue
        if bold_only:
            m = re.match(r'^\*\*([A-Z0-9][^*\n]{2,90}?)\s*:?\*\*\s*$', l)
            if m and not m.group(1).rstrip().endswith('.'):
                out.append(f"## {m.group(1).strip()}")
                continue
        out.append(l)
    return out


def _rank_and_number(lines: list[str], kh_ids: Set[str]) -> str:
    """Rank heading levels to ###/####/#####, drop self-title/author sections, renumber, clean body."""
    # Renumbers sequentially with valid parents (no phantom-0), strips figures/rules/[N] citations,
    # normalizes bullets to `-`, and wikilinks in-KH citations in the Relevant Citations section.
    fh = next((i for i, l in enumerate(lines) if re.match(r'^#{1,6}\s', l)), 0)
    lines = lines[fh:]
    fence = False
    levels = set()
    seen = False
    for l in lines:
        if re.match(r'^\s*```', l):
            fence = not fence
            continue
        if fence:
            continue
        h = re.match(r'^(#{1,6})\s+(.*)$', l)
        if not h:
            continue
        ti = _clean_title(h.group(2))
        if _author(ti):
            continue
        if _selft(ti) and not seen:
            continue
        seen = True
        levels.add(len(h.group(1)))
    rank = {lv: i for i, lv in enumerate(sorted(levels))}
    hashes = {0: "###", 1: "####", 2: "#####", 3: "#####"}

    out = []
    cnt = [0, 0, 0]
    fence = False
    drop_level = None
    drop_meta = False
    in_cit = False

    def lk(mm):   # wikilink an in-KH citation `[Title](arxiv/abs/ID)` -> `[[ID|Title]]`, else leave it
        a = mm.group(2)
        return f"[[{a}|{mm.group(1)}]]" if a in kh_ids else mm.group(0)

    for l in lines:
        if re.match(r'^\s*```', l):
            fence = not fence
            out.append(l)
            continue
        if fence:
            out.append(l)
            continue
        h = re.match(r'^(#{1,6})\s+(.*)$', l)
        if h:
            lv = len(h.group(1))
            ti = _clean_title(h.group(2))
            if drop_level is not None and lv > drop_level:
                continue
            drop_level = None
            drop_meta = False
            if _author(ti):
                drop_level = lv
                continue
            if _selft(ti) and cnt[0] == 0:
                drop_meta = True
                continue
            in_cit = bool(re.search(r'relevant citations|references|bibliography', ti, re.I))
            d = min(rank.get(lv, 0), 2)
            cnt[d] += 1
            for k in range(d + 1, 3):
                cnt[k] = 0
            if cnt[0] == 0:
                cnt[0] = 1
            num = ".".join(str(cnt[k]) for k in range(d + 1))
            out.append(f"{hashes[d]} {num}. {ti}")
            continue
        if drop_level is not None or drop_meta:
            continue
        if re.match(r'^\s*(---|\*\*\*|___)\s*$', l):
            continue
        if re.match(r'^\s*!\[.*\]\(.*\)\s*$', l):
            continue
        if re.match(r'^\s*\*Figure\b.*\*\s*$', l, re.I):
            continue
        l = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', l)
        if in_cit:
            l = re.sub(r'\s*\[Online\]\.\s*Available:\s*https?://\S+', '', l)
            l = re.sub(r'^\s*\[\d+\]\s*', '', l)
        else:
            l = re.sub(r'[ \t]?\[\d+(?:\s*[,\-]\s*\d+)*\](?!\])', '', l)
        # wikilink in-KH citations wherever they appear, not just inside a References section — an
        # LLM-generated report (unlike alphaxiv's old scrape) usually cites inline in prose, no
        # dedicated citations section guaranteed.
        l = re.sub(r'\[([^\]]+)\]\((?:https?://)?(?:www\.)?(?:alphaxiv|arxiv)\.org/abs/([0-9]+\.[0-9]+)\)', lk, l)
        l = re.sub(r'^(\s*)[*+](\s+)', r'\1- ', l)
        l = re.sub(r'^(\s*)-\s+', r'\1- ', l)
        out.append(l.rstrip())
    return "\n".join(out)


def _smart_join(body: str) -> str:
    """Re-join inline math the render split across lines (block-scoped, only blocks with lone tokens)."""
    # Merges a blank-separated block only when it contains a lone subscript/superscript token, joining
    # tight for subscripts / closing punctuation and with a space at word boundaries. Legit
    # paragraph/label/equation blocks (no lone token) are left intact, so this never glues real prose.
    lines = body.split("\n")
    blocks = []
    cur = []
    fence = False
    for l in lines:
        if re.match(r'^\s*```', l):
            fence = not fence
            cur.append(l)
            continue
        if fence:
            cur.append(l)
            continue
        # a blank line OR a heading is a block boundary (headings may not yet have blank lines around
        # them at this stage, so treat them explicitly or they'd contaminate the following content block)
        if l.strip() == "" or re.match(r'^#{1,6}\s', l):
            if cur:
                blocks.append(cur)
                cur = []
            blocks.append([l])
        else:
            cur.append(l)
    if cur:
        blocks.append(cur)
    out = []
    for blk in blocks:
        has_lone = any(LONE.match(l.strip()) for l in blk)
        first = blk[0].lstrip()
        if len(blk) > 1 and has_lone and not first.startswith(('|', '#', '```', '$$')):
            segs = []
            acc = None
            for l in blk:
                s = l.strip()
                if re.match(r'^([-*+]\s|\d+\.\s|#{1,6}\s)', s) or s.startswith(('|', '$$')):
                    if acc is not None:
                        segs.append(acc)
                    acc = l.rstrip()
                    continue
                if acc is None:
                    acc = l.rstrip()
                    continue
                if not s:
                    continue
                tight = LONE.match(s) or re.match(r'^[)\]\},.;:*]', s)
                # don't tight-join onto a boundary that needs a space: sentence/label punctuation, or a
                # closing markdown emphasis `*`/`**` (the next token is new content, not a subscript).
                if tight and not re.search(r'[.:;!?]$|\*$', acc):
                    acc = acc + s
                else:
                    acc = acc + " " + s
            if acc is not None:
                segs.append(acc)
            out.extend(segs)
        else:
            out.extend(blk)
    return "\n".join(out)


def _fix_punct(body: str) -> str:
    """Clean punctuation the [N]-citation stripping leaves behind (outside code fences)."""
    # Removes paren remnants `(,,)`/`(–)`, dangling en-dash after a word, doubled commas, and
    # space-before-comma. Legit en-dashes (`1–5`, `2020–2023`, `well–being`) are preserved.
    def fix(seg):
        seg = re.sub(r'\s*\(\s*[–\-,;\s]*\s*\)', '', seg)
        seg = re.sub(r'([A-Za-z])–(?=[\s,.;:)\]])', r'\1', seg)
        seg = re.sub(r',(\s*,)+', ',', seg)
        seg = re.sub(r'([A-Za-z0-9])\s+([,;])', r'\1\2', seg)
        seg = re.sub(r',\s*\.', '.', seg)
        seg = re.sub(r'  +', ' ', seg)
        return seg
    parts = re.split(r'(```.*?```|`[^`]*`)', body, flags=re.S)
    return "".join(seg if seg.startswith('`') else fix(seg) for seg in parts)


def format_report(raw_md: str, kh_ids: Set[str] = frozenset()) -> str:
    """Return the cleaned ## Detailed Report body (no heading) for a raw alphaxiv overview `.md`."""
    # kh_ids (in-vault arxiv IDs) is used to wikilink in-KH citations. See the module docstring for the
    # full pipeline; the acceptance checks live in validate_reports.py.
    if not raw_md or not raw_md.strip():
        return ""
    lines = raw_md.replace("\r\n", "\n").split("\n")
    lines = _pre_convert_bold_headings(lines)
    body = _rank_and_number(lines, kh_ids)
    body = _smart_join(body)
    body = _fix_punct(body)
    # de-number inline bold labels: "**6.1. Title:** text" -> "**Title:** text"
    body = re.sub(r'^\*\*\d+\.\d+\.?\s+([^*]+:)\*\*(\s\S)', r'**\1**\2', body, flags=re.M)
    # strip any leftover source number prefix in a heading title ("#### 3.1. 4.1 Foo" -> "#### 3.1. Foo")
    lines = body.split("\n")
    for k, l in enumerate(lines):
        hm = re.match(r'^(#{3,5} \d+(?:\.\d+)*\.)\s+(.*)$', l)
        if hm:
            nt = re.sub(r'^\d+(?:\.\d+)*\.?\s+', '', hm.group(2))
            if nt.strip():
                lines[k] = f"{hm.group(1)} {nt.strip()}"
    body = "\n".join(lines)
    # a prose sentence ending ':' right before a ### primary promised a figure/list that was stripped;
    # turn the orphaned colon into a period so it reads as a complete statement.
    L = body.split("\n")
    for i in range(len(L) - 1):
        if (re.search(r'[a-z][a-z ]+:\s*$', L[i]) and not L[i].strip().startswith(('-', '#', '*'))
                and len(L[i].strip()) > 25):
            j = i + 1
            while j < len(L) and not L[j].strip():
                j += 1
            if j < len(L) and re.match(r'^### ', L[j]):
                L[i] = re.sub(r':\s*$', '.', L[i])
    body = "\n".join(L)
    # blank line before and after every heading
    L = body.split("\n")
    res = []
    for j, l in enumerate(L):
        if re.match(r'^#{3,5} ', l) and res and res[-1].strip():
            res.append("")
        res.append(l)
        if re.match(r'^#{3,5} ', l) and j + 1 < len(L) and L[j + 1].strip():
            res.append("")
    return re.sub(r'\n{3,}', '\n\n', "\n".join(res)).strip()
