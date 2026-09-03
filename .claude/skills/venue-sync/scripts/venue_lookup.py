#!/usr/bin/env python3
"""Resolve where each KnowledgeHub paper was published and record it in the note.

Four sources by precedence: a manual override, the venue's own proceedings (the only source of
presentation tier), Semantic Scholar, then the authors' arxiv comment. Only the ten conferences in
CORE_VENUES reach the notes; the rest stay resolved in the cache.

Usage:
    .venv/bin/python venue_lookup.py refresh   # fetch + apply + annotate + stats
    .venv/bin/python venue_lookup.py fetch     # populate data/.venue-cache/
    .venv/bin/python venue_lookup.py apply     # dry run; --write to commit to notes
    .venv/bin/python venue_lookup.py stats     # rewrite Venue Coverage in General/00_Index.md
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

CACHE_DIR = Path("data/.venue-cache")
NOTES_DIR = Path("_KnowledgeHub_")

VENUE_SITES: tuple[tuple[str, str], ...] = (
    ("neurips.cc", "neurips"),
    ("icml.cc", "icml"),
    ("iclr.cc", "iclr"),
    ("cvpr.thecvf.com", "cvpr"),
    ("iccv.thecvf.com", "iccv"),
    ("eccv.ecva.net", "eccv"),
    ("wacv.thecvf.com", "wacv"),
)
VENUE_SITE_SHORT = {
    "neurips": "NeurIPS", "icml": "ICML", "iclr": "ICLR",
    "cvpr": "CVPR", "iccv": "ICCV", "eccv": "ECCV", "wacv": "WACV",
    "corl": "CoRL", "rss": "RSS",
}

# CoRL and RSS publish no programme JSON, so read their open archives instead. No tier from either.
PMLR_URL = "https://proceedings.mlr.press"
PMLR_DELAY_S = 0.4
PMLR_HEADER_CHARS = 4000  # enough to reach the volume's venue-and-year line
PMLR_VENUES: tuple[tuple[str, str], ...] = (
    (r"conference on robot learning", "corl"),
    (r"international conference on machine learning", "icml"),
)
RSS_URL = "https://www.roboticsconference.org/{year}/program/papers/"
RSS_DELAY_S = 0.5
RSS_FIRST_YEAR = 2023  # earlier years use a different URL layout and return nothing
REJECT_RE = re.compile(r"reject|withdraw|desk|decline", re.I)

# Tier vocabulary varies per venue-year: bare tiers, "Accept (oral)", "notable-top-5%", "Long Presentation".
TIER_RANK = {"": 0, "poster": 1, "spotlight": 2, "highlight": 3, "oral": 4}
TIER_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"oral|long presentation|notable-top-5", "oral"),
    (r"highlight", "highlight"),
    (r"spotlight|notable-top-25", "spotlight"),
    (r"poster|short presentation|regular|accept", "poster"),
)


def parse_tier(*fields: str) -> str:
    """Return the highest presentation tier named by any of the given decision/eventtype strings."""
    best = ""
    for text in fields:
        low = (text or "").lower()
        for pattern, tier in TIER_PATTERNS:
            if re.search(pattern, low):
                if TIER_RANK[tier] > TIER_RANK[best]:
                    best = tier
                break
    return best


# The only venues stored on notes. They hold 373 of the 375 tier-bearing papers, so widening this
# adds venue membership but no tier signal. Everything stays in the cache, so widening needs no refetch.
CORE_VENUES: frozenset[str] = frozenset(
    {"NeurIPS", "ICML", "ICLR", "CVPR", "ICCV", "ECCV", "ICRA", "IROS", "CoRL", "RSS"}
)

FIRST_YEAR = 2018
LAST_YEAR = 2027  # exclusive upper bound; probes one year past the newest known conference

DBLP_URL = "https://dblp.org/search/publ/api"
DBLP_DELAY_S = 1.2
# DBLP spells venues out; map to our short names so a hit can be matched to the note.
DBLP_VENUE_MAP: tuple[tuple[str, str], ...] = (
    (r"neurips|nips|neural information processing", "NeurIPS"),
    (r"^icml$|international conference on machine learning", "ICML"),
    (r"^iclr$|learning representations", "ICLR"),
    (r"^cvpr$|computer vision and pattern recognition", "CVPR"),
    (r"^iccv$|international conference on computer vision", "ICCV"),
    (r"^eccv$|european conference on computer vision", "ECCV"),
    (r"^icra$|robotics and automation", "ICRA"),
    (r"^iros$|intelligent robots and systems", "IROS"),
    (r"^corl$|conference on robot learning", "CoRL"),
    (r"^rss$|robotics.*science and systems", "RSS"),
)

S2_BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
S2_FIELDS = "title,externalIds,venue,publicationVenue,year,citationCount"
S2_BATCH_SIZE = 500
ARXIV_QUERY_URL = "https://export.arxiv.org/api/query"
ARXIV_BATCH_SIZE = 100
ARXIV_DELAY_S = 3.0
UA = "Mozilla/5.0 (compatible; ResearchBrain venue-lookup)"
HTTP_TIMEOUT_S = 180


def http_json(url: str, payload: bytes | None = None, timeout: int = HTTP_TIMEOUT_S) -> dict:
    """GET or POST a URL and parse the response as JSON."""
    headers = {"User-Agent": UA}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def http_text(url: str, timeout: int = HTTP_TIMEOUT_S) -> str:
    """GET a URL and return its body as decoded text."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def titles_agree(a: str, b: str) -> bool:
    """Judge whether two titles name the same paper, tolerating truncation, subtitles, and version drift."""
    x, y = norm_title(a), norm_title(b)
    if not x or not y:
        return False
    if x == y:
        return True
    # S2 truncates titles and drops subtitles, so a prefix is agreement rather than a mismatch.
    shorter, longer = (x, y) if len(x) <= len(y) else (y, x)
    if len(shorter) >= 8 and longer.startswith(shorter):
        return True
    # A short prefix counts only at a subtitle boundary: makes "ASE" match, keeps "Mind" a mismatch.
    a_raw, b_raw = a.strip().lower(), b.strip().lower()
    short_raw, long_raw = (a_raw, b_raw) if len(a_raw) <= len(b_raw) else (b_raw, a_raw)
    if len(short_raw) >= 3 and long_raw.startswith(short_raw) and long_raw[len(short_raw):len(short_raw) + 1] == ":":
        return True
    return difflib.SequenceMatcher(None, x, y).ratio() >= 0.85


def norm_title(title: str) -> str:
    """Reduce a paper title to a collision-resistant match key (lowercase alphanumerics only)."""
    return re.sub(r"[^a-z0-9]", "", title.lower())


# --------------------------------------------------------------------------- fetch


def _fetch_dump(url: str, label: str) -> list[dict]:
    """Fetch one conference virtual-site dump, warning when the static file is truncated."""
    blob = http_json(url)
    rows = list(blob.get("results", []))
    total = blob.get("count") or len(rows)
    # The /api/miniconf/events endpoint that would page the rest is 403, so a short dump is all there is.
    if len(rows) < total:
        print(f"  WARN {label}: static dump truncated at {len(rows)} of {total}", file=sys.stderr)
    return rows


def fetch_venue_sites(force: bool = False) -> int:
    """Download every live conference virtual-site dump, slimmed to name/decision/eventtype."""
    out_dir = CACHE_DIR / "venuesite"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    rejects: dict[str, set[str]] = {}
    for site, slug in VENUE_SITES:
        for year in range(FIRST_YEAR, LAST_YEAR):
            dest = out_dir / f"{slug}-{year}.json"
            if dest.exists() and not force:
                continue
            url = f"https://{site}/static/virtual/data/{slug}-{year}-orals-posters.json"
            try:
                results = _fetch_dump(url, f"{slug}-{year}")
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
                continue
            slim = [
                {
                    "name": r.get("name", ""),
                    "decision": r.get("decision") or "",
                    "eventtype": r.get("eventtype") or "",
                }
                for r in results
                if r.get("name")
            ]
            # Rejections would let a title match mark a rejected paper accepted. Bare tiers are routine.
            bad = {s["decision"] for s in slim if REJECT_RE.search(s["decision"])}
            if bad:
                rejects[f"{slug}-{year}"] = bad
            dest.write_text(json.dumps(slim))
            written += 1
            print(f"  {slug}-{year}: {len(slim)} records", flush=True)
    if rejects:
        for key, vals in rejects.items():
            print(f"ABORT: {key} carries rejection decisions: {sorted(vals)[:5]}", file=sys.stderr)
        raise SystemExit("rejections present in a dump; resolve before applying")
    return written


def _write_dump(slug: str, year: int, titles: list[str], force: bool = False) -> bool:
    """Write titles into the venuesite cache in the same shape the conference dumps use."""
    dest = CACHE_DIR / "venuesite" / f"{slug}-{year}.json"
    if (dest.exists() and not force) or not titles:  # never clobber a programme dump, which has tiers
        return False
    dest.write_text(json.dumps([{"name": t, "decision": "", "eventtype": ""} for t in titles]))
    print(f"  {slug}-{year}: {len(titles)} records", flush=True)
    return True


def fetch_pmlr(force: bool = False) -> int:
    """Index the PMLR volumes for CoRL and ICML, which publish no conference programme JSON."""
    (CACHE_DIR / "venuesite").mkdir(parents=True, exist_ok=True)
    try:
        index = http_text(f"{PMLR_URL}/")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return 0
    written = 0
    for vol in sorted({m for m in re.findall(r'href="(v\d+)"', index)}, key=lambda v: -int(v[1:])):
        try:
            page = http_text(f"{PMLR_URL}/{vol}/")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            continue
        header = page[:PMLR_HEADER_CHARS]
        slug = next((sl for pat, sl in PMLR_VENUES if re.search(pat, header, re.I)), "")
        year = re.search(r"\b(20[0-2]\d)\b", header)
        if not slug or not year:
            continue
        titles = [re.sub(r"\s+", " ", t).strip() for t in re.findall(r'<p class="title">([^<]+)', page)]
        written += _write_dump(slug, int(year.group(1)), titles, force)
        time.sleep(PMLR_DELAY_S)
    return written


def fetch_rss(force: bool = False) -> int:
    """Index the RSS proceedings pages, which list every accepted paper per year."""
    (CACHE_DIR / "venuesite").mkdir(parents=True, exist_ok=True)
    written = 0
    for year in range(RSS_FIRST_YEAR, LAST_YEAR):
        try:
            page = http_text(RSS_URL.format(year=year))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            continue
        titles = [re.sub(r"\s+", " ", t).strip()
                  for t in re.findall(r'href="/\d{4}/program/papers/[^"]*"><b>([^<]+)</b>', page)]
        written += _write_dump("rss", year, titles, force)
        time.sleep(RSS_DELAY_S)
    return written


def fetch_s2(arxiv_ids: list[str], force: bool = False) -> dict[str, dict]:
    """Fetch Semantic Scholar venue and citation records for every arxiv ID, resuming from cache."""
    dest = CACHE_DIR / "s2.json"
    cache: dict[str, dict] = {}
    if dest.exists() and not force:
        cache = json.loads(dest.read_text())
    todo = [i for i in arxiv_ids if i not in cache]
    url = f"{S2_BATCH_URL}?fields={S2_FIELDS}"
    for start in range(0, len(todo), S2_BATCH_SIZE):
        chunk = todo[start:start + S2_BATCH_SIZE]
        body = json.dumps({"ids": [f"ARXIV:{i}" for i in chunk]}).encode()
        for attempt in range(6):
            try:
                rows = http_json(url, payload=body)
                break
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
                time.sleep(2 ** attempt)
        else:
            print(f"  s2: giving up on batch at offset {start}", file=sys.stderr)
            continue
        for aid, row in zip(chunk, rows):
            cache[aid] = row or {}
        dest.write_text(json.dumps(cache))
        print(f"  s2: {len(cache)}/{len(arxiv_ids)}", flush=True)
        time.sleep(1.0)
    return cache


def fetch_arxiv(arxiv_ids: list[str], force: bool = False) -> dict[str, dict]:
    """Fetch arxiv comment and journal_ref fields for every arxiv ID, resuming from cache."""
    dest = CACHE_DIR / "arxiv.json"
    cache: dict[str, dict] = {}
    if dest.exists() and not force:
        cache = json.loads(dest.read_text())
    todo = [i for i in arxiv_ids if i not in cache]
    for start in range(0, len(todo), ARXIV_BATCH_SIZE):
        chunk = todo[start:start + ARXIV_BATCH_SIZE]
        url = f"{ARXIV_QUERY_URL}?id_list={','.join(chunk)}&max_results={ARXIV_BATCH_SIZE}"
        try:
            xml = http_text(url)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            print(f"  arxiv: batch at offset {start} failed", file=sys.stderr)
            time.sleep(ARXIV_DELAY_S)
            continue
        for entry in xml.split("<entry>")[1:]:
            m = re.search(r"<id>https?://arxiv\.org/abs/([^v<]+)", entry)
            if not m:
                continue
            comment = re.search(r"<arxiv:comment[^>]*>(.*?)</arxiv:comment>", entry, re.S)
            journal = re.search(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", entry, re.S)
            cache[m.group(1)] = {
                "comment": (comment.group(1).strip() if comment else ""),
                "journal_ref": (journal.group(1).strip() if journal else ""),
            }
        for aid in chunk:  # record misses so a rerun does not retry withdrawn IDs forever
            cache.setdefault(aid, {"comment": "", "journal_ref": ""})
        dest.write_text(json.dumps(cache))
        print(f"  arxiv: {len(cache)}/{len(arxiv_ids)}", flush=True)
        time.sleep(ARXIV_DELAY_S)
    return cache


def dblp_year(entry: dict, venue: str) -> int:
    """Return the publication year of a DBLP hit, but only when its venue matches the given short name."""
    names = entry.get("venue") or ""
    for name in names if isinstance(names, list) else [names]:
        for pattern, short in DBLP_VENUE_MAP:
            if re.search(pattern, str(name), re.I) and short == venue:
                year = str(entry.get("year") or "")
                return int(year) if year.isdigit() else 0
    return 0


def fetch_dblp(targets: dict[str, str], force: bool = False) -> dict[str, list[dict]]:
    """Query DBLP by title for papers whose venue year is still unknown, caching the raw hits."""
    dest = CACHE_DIR / "dblp.json"
    cache: dict[str, list[dict]] = {}
    if dest.exists() and not force:
        cache = json.loads(dest.read_text())
    todo = [k for k in targets if k not in cache]
    for i, arxiv_id in enumerate(todo, 1):
        params = urllib.parse.urlencode({"q": targets[arxiv_id], "format": "json", "h": 10})
        blob = None
        # DBLP rate-limits aggressively and drops connections, so retry rather than lose the paper.
        for attempt in range(4):
            try:
                blob = http_json(f"{DBLP_URL}?{params}", timeout=45)
                break
            except (OSError, urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
                time.sleep(DBLP_DELAY_S * 4 * (attempt + 1))
        cache[arxiv_id] = ([h.get("info", {}) for h in blob.get("result", {}).get("hits", {}).get("hit", [])]
                           if blob else [])
        if i % 10 == 0 or i == len(todo):
            dest.write_text(json.dumps(cache))
            print(f"  dblp: {i}/{len(todo)}", flush=True)
        time.sleep(DBLP_DELAY_S)
    dest.write_text(json.dumps(cache))
    return cache


def kh_ids(notes_dir: Path) -> list[str]:
    """List every arxiv ID that has a KnowledgeHub note."""
    return sorted(p.stem for p in notes_dir.glob("*.md") if re.fullmatch(r"\d{4}\.\d{4,5}", p.stem))


def cmd_fetch(args: argparse.Namespace) -> None:
    """Populate the venue cache from all three sources."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    ids = kh_ids(Path(args.notes_dir))
    print(f"{len(ids)} KH notes")
    print("venue sites:")
    fetch_venue_sites(force=args.force)
    print("pmlr (CoRL, ICML):")
    fetch_pmlr(force=args.force)
    print("rss:")
    fetch_rss(force=args.force)
    print("semantic scholar:")
    fetch_s2(ids, force=args.force)
    print("arxiv:")
    arxiv = fetch_arxiv(ids, force=args.force)
    # DBLP is per-title, so query only papers that would otherwise be dropped for having no year.
    venue_index = load_venue_index()
    s2 = json.loads((CACHE_DIR / "s2.json").read_text())
    targets: dict[str, str] = {}
    for path in sorted(Path(args.notes_dir).glob("*.md")):
        if not re.fullmatch(r"\d{4}\.\d{4,5}", path.stem):
            continue
        title = note_title(path.read_text())
        r = resolve(path.stem, title, venue_index, s2, arxiv)
        if r.venue in CORE_VENUES and not r.year and title:
            targets[path.stem] = title
    print(f"dblp: {len(targets)} papers need a venue year")
    fetch_dblp(targets, force=args.force)
    print("cache complete")



# --------------------------------------------------------------------------- resolve

VENUE_FIELDS = ("venue", "venue_year", "venue_type", "venue_tier", "citations", "venue_source", "venue_checked")
NOT_A_VENUE = {"", "arxiv.org", "arxiv"}
S2_VENUE_MAP: tuple[tuple[str, str], ...] = (
    (r"pattern recognition workshops|cvprw", "CVPR Workshop"),
    (r"computer vision workshops|iccvw", "ICCV Workshop"),
    (r"neurips datasets and benchmarks", "NeurIPS-D&B"),
    (r"neural information processing systems", "NeurIPS"),
    (r"computer vision and pattern recognition", "CVPR"),
    (r"learning representations", "ICLR"),
    (r"international conference on machine learning", "ICML"),
    (r"robotics and automation letters", "RA-L"),
    (r"conference on robotics and automation", "ICRA"),
    (r"intelligent robots and systems", "IROS"),
    (r"conference on robot learning", "CoRL"),
    (r"european conference on computer vision", "ECCV"),
    (r"international conference on computer vision", "ICCV"),
    (r"robotics: science and systems|^robotics$", "RSS"),
    (r"north american chapter", "NAACL"),
    (r"empirical methods in natural language", "EMNLP"),
    (r"association for computational linguistics", "ACL"),
    (r"aaai conference", "AAAI"),
    (r"joint conference on artificial intelligence", "IJCAI"),
    (r"trans\. mach\. learn\. res|transactions on machine learning research", "TMLR"),
    (r"transactions on pattern analysis", "TPAMI"),
    (r"transactions on robotics", "T-RO"),
    (r"transactions on graphics", "TOG"),
    (r"applications of computer vision", "WACV"),
    (r"humanoid robots", "Humanoids"),
    (r"3d vision", "3DV"),
    (r"international journal of computer vision", "IJCV"),
    (r"interactive techniques in asia", "SIGGRAPH-Asia"),
    (r"computer graphics and interactive techniques", "SIGGRAPH"),
    (r"science robotics|sci\. robotics", "Science-Robotics"),
    (r"journal of robotics research|int\. j\. robotics res", "IJRR"),
    (r"transactions on image processing", "TIP"),
    (r"transactions on neural networks and learning", "TNNLS"),
    (r"transactions on mechatronics", "T-MECH"),
    (r"automation science and engineering", "T-ASE"),
    (r"transactions on multimedia", "TMM"),
    (r"transactions on circuits and systems for video", "TCSVT"),
    (r"computer graphics forum", "CGF"),
    (r"artificial intelligence research", "JAIR"),
    (r"autonomous agents and multiagent systems|adaptive agents and multi-agent", "AAMAS"),
    (r"conference on decision and control", "CDC"),
    (r"american control conference", "ACC"),
    (r"acm multimedia", "ACM-MM"),
    (r"acoustics, speech", "ICASSP"),
    (r"journal of machine learning research", "JMLR"),
    (r"acm computing surveys", "CSUR"),
    # Long-tail venues, hand-curated. Standard acronyms only; nothing guessed from capitals.
    (r"human-robot interaction", "HRI"),
    (r"european control conference", "ECC"),
    (r"conference on soft robotics", "RoboSoft"),
    (r"joint conference on neural network", "IJCNN"),
    (r"symposium on system integration", "SII"),
    (r"uncertainty in artificial intelligence", "UAI"),
    (r"learning for dynamics", "L4DC"),
    (r"asian conference on computer vision", "ACCV"),
    (r"british machine vision conference", "BMVC"),
    (r"systems, man and cybernetics", "SMC"),
    (r"genetic and evolutionary computation", "GECCO"),
    (r"robotics and biomimetics", "ROBIO"),
    (r"symposium on artificial neural networks", "ESANN"),
    (r"intelligent vehicles symposium", "IV"),
    (r"intelligent transportation systems", "ITSC"),
    (r"mediterranean conference on control", "MED"),
    (r"advanced intelligent mechatronics", "AIM"),
    (r"knowledge discovery", "KDD"),
    (r"control, decision and information tech", "CoDIT"),
    (r"real-time computing and robotics", "RCAR"),
    (r"ieee access", "IEEE-Access"),
    (r"nature machine intelligence", "Nature-MI"),
    (r"nature communications", "Nature-Comms"),
    (r"science china information", "Sci-China-IS"),
    (r"autonomous robots", "AutRob"),
    (r"frontiers.*robotics", "Frontiers-Robotics"),
    (r"sensors journal", "IEEE-Sensors"),
    (r"instrumentation and measurement", "TIM"),
    (r"transactions on cybernetics", "T-Cyb"),
    (r"emerging topics in computational intelligence", "TETCI"),
    (r"transactions on industrial electronics", "TIE"),
    (r"expert systems with applications", "ESWA"),
    (r"engineering applications of artificial intelligence", "EAAI"),
    (r"knowledge-based systems", "KBS"),
    (r"image and vision computing", "IVC"),
    (r"information fusion", "Info-Fusion"),
    (r"artificial intelligence review", "AI-Review"),
    (r"ai magazine", "AI-Magazine"),
    (r"biomimetic intelligence and robotics", "BIR"),
    (r"visual intelligence", "Visual-Intelligence"),
    (r"pattern recognition letters", "PRL"),
    (r"^pattern recognition$", "PR"),
    (r"neural networks", "Neural-Networks"),
    (r"robotics and autonomous systems|robotics auton\. syst", "RAS"),
    (r"artificial intelligence and stat", "AISTATS"),
    (r"neural computing (?:&|and) applications", "NCA"),
    (r"^robot learning$", "CoRL"),
    (r"computer vision and image understanding", "CVIU"),
    (r"international conference on pattern recognition", "ICPR"),
    (r"conference on computer and communications", "ICCC"),
    # Duplicate spellings S2 emits (long, abbreviated, HTML-entity), plus venues the list missed.
    (r"auton\. robots|autonomous robots", "AutRob"),
    (r"robotics (?:&|&amp;) automation magazine", "RAM"),
    (r"^visigrapp", "VISIGRAPP"),
    (r"^hri companion", "HRI"),
    (r"siggraph asia", "SIGGRAPH-Asia"),
    (r"found\. trends mach\. learn|foundations and trends in machine learning", "FnT-ML"),
    (r"robotics comput\. integr\. manuf", "RCIM"),
    (r"usenix security", "USENIX-Security"),
    (r"theory of computing", "STOC"),
    (r"national academy of sciences", "PNAS"),
    (r"computational learning theory", "COLT"),
    (r"sigir conference", "SIGIR"),
    (r"multimodal interaction", "ICMI"),
    (r"multimedia retrieval", "ICMR"),
    (r"information and knowledge management", "CIKM"),
    (r"multimedia and expo", "ICME"),
    (r"document analysis and recognition", "ICDAR"),
    (r"fairness, accountability and transparency", "FAccT"),
    (r"^chi extended abstracts", "CHI"),
    (r"ecml/pkdd", "ECML-PKDD"),
    (r"automated planning", "ICAPS"),
    (r"symposium on computer architecture", "ISCA"),
    (r"circuits and systems$|symposium on circuits and systems", "ISCAS"),
    (r"robot and human interactive communicat", "RO-MAN"),
    (r"unmanned aircraft systems", "ICUAS"),
    (r"transactions on haptics", "T-Haptics"),
    (r"transactions on automatic control", "T-AC"),
    (r"transactions on artificial intelligence", "T-AI"),
    (r"transactions on affective computing", "T-Affective"),
    (r"systems, man, and cybernetics: systems", "T-SMC"),
    (r"control systems letters", "L-CSS"),
    (r"communications surveys", "COMST"),
    (r"transactions on mobile computing", "TMC"),
    (r"cognitive and developmental systems", "TCDS"),
    (r"scientific reports", "Sci-Reports"),
    (r"machine intelligence research", "MIR"),
    (r"national science review", "NSR"),
    (r"^artificial intelligence$", "AIJ"),
    (r"^computational linguistics$", "CL"),
    (r"photogrammetry and remote sensing", "ISPRS-J"),
    (r"journal of computational physics", "JCP"),
    (r"optics express", "Optics-Express"),
    (r"advanced intelligent systems", "AIS"),
    (r"intelligent service robotics", "ISR"),
    (r"control engineering practice", "CEP"),
    (r"information processing (?:&|and) management", "IPM"),
    (r"advanced engineering informatics", "AEI"),
    (r"aerospace science and technology", "AST"),
    (r"^computers (?:&|and) graphics", "C&G"),
    (r"npj robotics", "npj-Robotics"),
    (r"ifac-papersonline", "IFAC"),
    (r"advanced robotics", "Advanced-Robotics"),
)
WORKSHOP_RE = re.compile(r"\bworkshop|\bwksp\b", re.I)
ARXIV_VENUE_RE = re.compile(
    r"\b(CVPR|ICCV|ECCV|WACV|BMVC|NeurIPS|NIPS|ICLR|ICML|AAAI|IJCAI|ACL|EMNLP|NAACL|COLING|COLM|"
    r"CoRL|ICRA|IROS|RSS|SIGGRAPH|TPAMI|IJCV|JMLR|TMLR|RA-L|T-RO|TRO|ICASSP|INTERSPEECH|KDD|WWW|CHI|SIGIR)"
    r"[\s'’]*((?:19|20)?\d{2})\b"
)


@dataclass
class Resolved:
    """Venue metadata resolved for one paper."""

    venue: str = ""
    year: int = 0
    type: str = ""
    tier: str = ""
    citations: int = -1
    source: str = ""


ARXIV_EPOCH = 2000  # arxiv IDs encode the year as YY since 2000


def _venue_year(arxiv_id: str) -> int:
    """Return the 4-digit calendar year encoded in an arxiv ID's YYMM prefix."""
    return ARXIV_EPOCH + int(arxiv_id[:2])


def load_venue_index() -> dict[str, list[tuple[str, int, str]]]:
    """Build a normalized-title index over every cached conference dump."""
    index: dict[str, list[tuple[str, int, str]]] = {}
    for path in sorted((CACHE_DIR / "venuesite").glob("*.json")):
        slug, year = path.stem.rsplit("-", 1)
        short = VENUE_SITE_SHORT.get(slug, slug.upper())
        for rec in json.loads(path.read_text()):
            key = norm_title(rec["name"])
            if key:
                index.setdefault(key, []).append((short, int(year), parse_tier(rec["decision"], rec["eventtype"])))
    return index


JOURNAL_RE = re.compile(
    r"journal|transactions|\bletters?\b|magazine|^nature|science china|science robotics|neurocomputing|"
    r"ieee access|\breview\b|^t-|^tpami$|^ijcv$|^jmlr$|^tmlr$|^ra-l$|^tog$|^ijrr$|^tip$|^tnnls$|"
    r"^t-mech$|^t-ase$|^tmm$|^tcsvt$|^cgf$|^jair$|^csur$|^science-robotics$|information fusion|"
    r"expert systems", re.I)


def classify_venue(name: str) -> str:
    """Classify a venue name as workshop, journal, or conference."""
    if WORKSHOP_RE.search(name):
        return "workshop"
    return "journal" if JOURNAL_RE.search(name) else "conference"


def shorten_venue(name: str) -> str:
    """Map a Semantic Scholar venue name onto its short form, or return it cleaned if unmapped."""
    low = name.lower()
    for pattern, short in S2_VENUE_MAP:
        if re.search(pattern, low):
            return short
    # Many S2 names carry their own acronym, e.g. "... Intelligent Vehicles Symposium (IV)".
    m = re.search(r"\(([A-Z][A-Za-z0-9-]{1,11})\)\s*$", name)
    if m and m.group(1).lower() not in ("print", "online"):
        return m.group(1)
    return re.sub(r"\s+", " ", name).strip()


def s2_year(s2_row: dict, venue: str, dblp_hits: list[dict]) -> int:
    """Recover a venue year for an s2-sourced paper, from its DBLP conference key or DBLP's own search."""
    # A `conf/...` key ends in the conference year; `journals/corr/...` is the arXiv record, so unusable.
    key = (s2_row.get("externalIds") or {}).get("DBLP") or ""
    m = re.match(r"conf/[^/]+/.*?(\d{2})$", key)
    if m:
        return ARXIV_EPOCH + int(m.group(1))
    for hit in dblp_hits:
        year = dblp_year(hit, venue)
        if year:
            return year
    return 0


def resolve(
    arxiv_id: str,
    title: str,
    venue_index: dict[str, list[tuple[str, int, str]]],
    s2: dict[str, dict],
    arxiv: dict[str, dict],
    stats: Counter | None = None,
    dblp: dict[str, list[dict]] | None = None,
) -> Resolved:
    """Resolve one paper's venue, tier, and citation count from the cached sources by precedence."""
    dblp, stats = dblp or {}, Counter() if stats is None else stats
    s2_row = s2.get(arxiv_id) or {}
    # Gates citations too: S2 sometimes maps to a different paper, and a wrong count beats no count.
    if s2_row.get("title") and not titles_agree(s2_row["title"], title):
        stats["title-mismatch"] += 1
        s2_row = {}
    citations = s2_row.get("citationCount")
    out = Resolved(citations=citations if isinstance(citations, int) else -1)

    hits = venue_index.get(norm_title(title), [])
    if hits:
        lo, hi = _venue_year(arxiv_id) - 1, _venue_year(arxiv_id) + 3
        in_window = [h for h in hits if lo <= h[1] <= hi]
        if not in_window:
            stats["guard_rejected"] += 1
        else:
            short, year, tier = max(in_window, key=lambda h: (TIER_RANK[h[2]], h[1]))
            out.venue, out.year, out.type = short, year, "conference"
            out.tier, out.source = tier, "proceedings"
            stats["proceedings"] += 1
            return out

    # Semantic Scholar: no tier, and its two venue fields disagree, so try both.
    pv = s2_row.get("publicationVenue") or {}
    for cand in (pv.get("name") or "", s2_row.get("venue") or ""):
        if cand.strip().lower() in NOT_A_VENUE:
            continue
        # S2's `year` is the preprint year - ResNet reads 2015 where the venue is CVPR 2016.
        out.venue = shorten_venue(cand)
        out.year = s2_year(s2_row, out.venue, dblp.get(arxiv_id, []))
        out.type = classify_venue(out.venue)
        if out.type == "workshop":  # e.g. "CVPR Workshop"; the track lives in venue_type, not the name
            out.venue = re.sub(r"\s*workshops?\s*$", "", out.venue, flags=re.I)
        out.source = "semantic-scholar"
        stats["semantic-scholar"] += 1
        return out

    # arxiv comment: last resort, self-reported and often stale.
    ax = arxiv.get(arxiv_id) or {}
    text = f"{ax.get('comment', '')} {ax.get('journal_ref', '')}"
    m = ARXIV_VENUE_RE.search(text)
    if m:
        year = m.group(2)
        year = f"20{year}" if len(year) == 2 else year
        workshop = bool(WORKSHOP_RE.search(text))
        out.venue, out.year = m.group(1), int(year)
        out.type = "workshop" if workshop else classify_venue(out.venue)
        # A workshop oral is not a main-conference oral, so a workshop never carries a tier.
        out.tier = "" if workshop else parse_tier(text.lower()) if re.search(r"oral|spotlight|highlight", text, re.I) else ""
        out.source = "arxiv-comment"
        stats["arxiv-comment"] += 1
        return out

    stats["unknown"] += 1
    return out


# --------------------------------------------------------------------------- apply

FM_RE = re.compile(r"\A---\n(.*?\n)---\n", re.S)
# Heading optional so apply migrates notes still on the older bare bullets.
PROVENANCE_RE = re.compile(r"^(?:## Publication\n\n)?(?:- venue_source:.*\n)?- venue_checked: .*\n\n?", re.M)


def render_fields(r: Resolved) -> str:
    """Render the five displayed venue frontmatter lines for a resolved paper."""
    # Unknown fields are omitted, not blanked: most papers have no venue, and Bases reads absent as null.
    def line(key: str, value: object, quote: bool = True) -> str:
        """Render one frontmatter line, or nothing at all when the value is unknown."""
        if not value:
            return ""
        return f'{key}: "{value}"\n' if quote else f"{key}: {value}\n"

    return (
        line("venue", r.venue)
        + line("venue_year", r.year, quote=False)
        + line("venue_type", r.type)
        + line("venue_tier", r.tier)
        + f"citations: {r.citations}\n"
    )


def render_provenance(r: Resolved, today: str) -> str:
    """Render the two bookkeeping lines that live hidden in the note's %% block."""
    source = f"- venue_source: {r.source}\n" if r.source else ""
    return f"{source}- venue_checked: {today}\n"


def patch_provenance(text: str, lines: str) -> str:
    """Insert or replace the note's Publication section, last in the %% block after BibTeX and any Assessment."""
    # Always strip then re-insert at the anchor, so a note still carrying the old top-of-block bullets migrates.
    text = PROVENANCE_RE.sub("", text)
    opened = text.index("%%\n") + len("%%\n")
    at = text.index("\n%%\n", opened) + 1  # the closing %% line; anchoring at the block start would race paper-rigor
    head = text[:at].rstrip("\n") + "\n"  # collapse whatever the strip left, so a re-run is byte-identical
    return head + "\n## Publication\n\n" + lines + text[at:]


def patch_frontmatter(text: str, fields: str) -> str:
    """Insert or replace the five venue keys in a note's frontmatter, leaving every other line untouched."""
    m = FM_RE.match(text)
    if not m:
        raise ValueError("note has no frontmatter block")
    body = m.group(1)
    kept = [ln for ln in body.splitlines(keepends=True) if not ln.split(":", 1)[0].strip() in VENUE_FIELDS]
    return "---\n" + "".join(kept) + fields + "---\n" + text[m.end():]


def note_title(text: str) -> str:
    """Extract the title value from a KnowledgeHub note's frontmatter."""
    m = re.search(r'^title:\s*"?(.*?)"?\s*$', text, re.M)
    return m.group(1) if m else ""


FIELD_RE = re.compile(r"^(?:venue|venue_year|venue_type|venue_tier|citations): .*\n", re.M)


def existing_fields(text: str) -> str:
    """Return the note's current venue frontmatter lines, in file order."""
    m = FM_RE.match(text)
    return "".join(FIELD_RE.findall(m.group(1))) if m else ""


def existing_checked(text: str) -> str:
    """Return the note's current venue_checked date, or an empty string when absent."""
    m = re.search(r"^- venue_checked: (.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def existing_source(text: str) -> str:
    """Return the note's current venue_source value from the %% block, or an empty string when absent."""
    m = re.search(r"^- venue_source:\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def cmd_apply(args: argparse.Namespace) -> None:
    """Resolve every note's venue metadata and write it into the note frontmatter."""
    notes_dir = Path(args.notes_dir)
    today = time.strftime("%Y-%m-%d")
    venue_index = load_venue_index()
    s2 = json.loads((CACHE_DIR / "s2.json").read_text())
    arxiv = json.loads((CACHE_DIR / "arxiv.json").read_text())
    dblp_path = CACHE_DIR / "dblp.json"
    dblp = json.loads(dblp_path.read_text()) if dblp_path.exists() else {}
    print(f"venue index: {len(venue_index)} titles | s2: {len(s2)} | arxiv: {len(arxiv)} | dblp: {len(dblp)}")

    stats: Counter = Counter()
    changed = 0
    paths = sorted(p for p in notes_dir.glob("*.md") if re.fullmatch(r"\d{4}\.\d{4,5}", p.stem))
    if args.limit:
        paths = paths[: args.limit]
    for path in paths:
        text = path.read_text()
        if existing_source(text) == "manual":
            stats["manual-skipped"] += 1
            continue
        if args.only_unknown and "\nvenue:" in text:
            continue
        r = resolve(path.stem, note_title(text), venue_index, s2, arxiv, stats, dblp)
        # Store a venue only if core and yeared; an unyeared venue is a half-record. The cache keeps
        # the rest, so widening CORE_VENUES and re-running apply restores them without a refetch.
        if r.venue and not (r.year and r.venue in CORE_VENUES):
            stats["no-year-suppressed" if not r.year else "non-core-suppressed"] += 1
            r = Resolved(citations=r.citations)
        if r.tier:
            stats[f"tier:{r.tier}"] += 1
        if r.type:
            stats[f"type:{r.type}"] += 1
        # Only a resolved value that actually moved earns today's date. Comparing rendered notes instead
        # would restamp all 9,794 on any layout change, which is not an update.
        fields = render_fields(r)
        stamp = today if fields != existing_fields(text) or r.source != existing_source(text) else (existing_checked(text) or today)
        new = patch_provenance(patch_frontmatter(text, fields), render_provenance(r, stamp))
        if new == text:
            continue
        changed += 1
        if args.dry_run:
            if changed <= args.show:
                print(f"\n--- {path.name}")
                print(render_fields(r).rstrip())
                print(render_provenance(r, stamp).rstrip())
        else:
            path.write_text(new)

    print(f"\n{'would change' if args.dry_run else 'changed'}: {changed} notes")
    for key in ("proceedings", "semantic-scholar", "arxiv-comment", "unknown", "manual-skipped", "guard_rejected", "title-mismatch", "non-core-suppressed", "no-year-suppressed"):
        print(f"  {key:16s} {stats[key]}")
    for vtype in ("conference", "journal", "workshop"):
        print(f"  type:{vtype:11s} {stats['type:' + vtype]}")
    for tier in ("oral", "highlight", "spotlight", "poster"):
        print(f"  tier:{tier:11s} {stats['tier:' + tier]}")


STATS_PATH = Path("General/00_Index.md")
STATS_HEADING = "### Venue Coverage"


def read_note_venue(text: str) -> dict:
    """Pull the venue fields out of one note's frontmatter and %% block."""
    def field(key: str) -> str:
        m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', text, re.M)
        return m.group(1) if m else ""

    src = re.search(r"^- venue_source: (.*)$", text, re.M)
    return {
        "venue": field("venue"),
        "year": field("venue_year"),
        "type": field("venue_type"),
        "tier": field("venue_tier"),
        "citations": field("citations"),
        "source": src.group(1).strip() if src else "",
    }


def cmd_stats(args: argparse.Namespace) -> None:
    """Write the venue-distribution section into General/00_Index.md from what the notes actually hold."""
    all_rows = [read_note_venue(p.read_text()) for p in sorted(Path(args.notes_dir).glob("*.md"))
                if re.fullmatch(r"\d{4}\.\d{4,5}", p.stem)]
    total = len(all_rows)
    accepted = [r for r in all_rows if r["venue"]]
    per: dict[str, list[dict]] = {}
    for r in accepted:
        per.setdefault(r["venue"], []).append(r)
    n_acc = len(accepted)

    def cites(rs: list[dict]) -> str:
        """Median citation count over notes that have one, as a string."""
        vals = sorted(int(r["citations"]) for r in rs
                      if r["citations"].lstrip("-").isdigit() and int(r["citations"]) >= 0)
        return str(vals[len(vals) // 2]) if vals else "-"

    out = [
        STATS_HEADING,
        "",
        f"**{n_acc} of {total} papers ({100 * n_acc // total}%)** carry a venue.",
        "",
        "| Venue | Papers | Oral | Spotlight | Highlight | Median citations |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for venue in sorted(per, key=lambda v: -len(per[v])):
        rs = per[venue]
        tiers = Counter(r["tier"] for r in rs)
        out.append(f"| {venue} | {len(rs)} | {tiers['oral'] or '-'} | {tiers['spotlight'] or '-'} | "
                   f"{tiers['highlight'] or '-'} | {cites(rs)} |")
    out.append(f"| **Total** | **{n_acc}** | **{sum(1 for r in accepted if r['tier'] == 'oral')}** | "
               f"**{sum(1 for r in accepted if r['tier'] == 'spotlight')}** | "
               f"**{sum(1 for r in accepted if r['tier'] == 'highlight')}** | |")

    out.append("")

    block = "\n".join(out)
    text = STATS_PATH.read_text()
    # Replace up to the next same-or-higher heading. Renaming the heading makes a rerun append instead.
    m = re.search(rf"^{re.escape(STATS_HEADING)}\n(?:.*\n)*?(?=^#{{1,3}} |\Z)", text, re.M)
    if m:
        text = text[:m.start()] + block + text[m.end():]
    else:
        text = text.rstrip("\n") + "\n\n---\n\n" + block
    STATS_PATH.write_text(text)
    print(f"wrote the venue section in {STATS_PATH}: {len(per)} venues, {n_acc}/{total} with a venue")


def cmd_refresh(args: argparse.Namespace) -> None:
    """Refetch every source, fill in notes that still have no venue, then re-render the inline badges."""
    cmd_fetch(args)
    args.dry_run, args.show, args.only_unknown = False, 0, True
    cmd_apply(args)
    annotate = Path(__file__).with_name("venue_annotate.py")
    subprocess.run([sys.executable, str(annotate), "--write", "--notes-dir", args.notes_dir], check=True)
    cmd_stats(args)


def main() -> None:
    """Parse arguments and dispatch to a subcommand."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--notes-dir", default=str(NOTES_DIR))
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="download venue-site, Semantic Scholar, and arxiv metadata into the cache")
    f.add_argument("--force", action="store_true", help="ignore the cache and refetch everything")
    f.set_defaults(func=cmd_fetch)
    a = sub.add_parser("apply", help="resolve the cache into venue frontmatter fields on every note")
    a.add_argument("--write", dest="dry_run", action="store_false", default=True, help="actually write (default is a dry run)")
    a.add_argument("--limit", type=int, default=0, help="process only the first N notes")
    a.add_argument("--show", type=int, default=20, help="how many resolved records to print in a dry run")
    a.add_argument("--only-unknown", action="store_true", help="skip notes that already have a non-empty venue")
    a.set_defaults(func=cmd_apply)
    r = sub.add_parser("refresh", help="refetch, fill in still-unknown venues, and re-render inline badges")
    r.add_argument("--force", action="store_true", help="ignore the cache and refetch everything")
    r.add_argument("--limit", type=int, default=0, help="process only the first N notes")
    r.set_defaults(func=cmd_refresh)
    st = sub.add_parser("stats", help="write the venue-distribution table to the Venue Coverage section of General/00_Index.md")
    st.set_defaults(func=cmd_stats)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
