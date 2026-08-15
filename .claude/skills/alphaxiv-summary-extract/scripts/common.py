"""Shared constants and helpers for the alphaxiv-summary-extract scripts.

fetch_bibtex imports `requests` lazily, so light entry points can use the constants and arxiv-ID
parsers without pulling it in.
"""

import re

KH_DIR = "_KnowledgeHub_"                              # default KH notes dir (vault-relative)
ARXIV_ID_RE = r"\d{4}\.\d{4,5}"                        # arxiv ID, e.g. 2602.15922
ABS_URL = "https://www.alphaxiv.org/abs/{}"            # note's `link:` frontmatter; /overview/ 302s here too
REPORT_URL = "https://www.alphaxiv.org/overview/{}.md" # machine-readable render — source of the note's ## Detailed Report


def parse_arxiv_id(url_or_id: str) -> str:
    """Return the bare arxiv ID from a URL or raw ID (e.g. '.../abs/2602.15922v2' -> '2602.15922')."""
    # Fall back to the last path segment when no ID pattern is present.
    match = re.search(ARXIV_ID_RE, url_or_id)
    return match.group(0) if match else url_or_id.rstrip("/").split("/")[-1]


def overview_link_selector(paper_id: str) -> str:
    """CSS selector for the in-app /overview/<id> anchor (the rate-limit-avoiding click-through)."""
    return f"a[href*='/overview/{paper_id}']"


def fetch_bibtex(arxiv_id: str) -> str:
    """Fetch BibTeX from arXiv, with trailing whitespace stripped per line."""
    # Import `requests` lazily so importing this module stays light for callers that only need the
    # constants/parsers above (e.g. generate_overviews.py).
    import requests

    try:
        resp = requests.get(f"https://arxiv.org/bibtex/{arxiv_id}", timeout=15)
        resp.raise_for_status()
        return "\n".join(line.rstrip() for line in resp.text.strip().splitlines())
    except Exception as e:
        print(f"  Warning: could not fetch BibTeX for {arxiv_id}: {e}")
        return ""
