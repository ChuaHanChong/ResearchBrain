"""Shared utilities for alphaxiv-summary-extract scripts."""

import requests


def find_duplicates(papers):
    seen = set()
    duplicates = set()
    for paper in papers:
        if paper in seen:
            duplicates.add(paper)
        else:
            seen.add(paper)
    return duplicates


def fetch_bibtex(arxiv_id: str) -> str:
    """Fetch BibTeX from arXiv and return with trailing whitespace stripped per line."""
    try:
        resp = requests.get(f"https://arxiv.org/bibtex/{arxiv_id}", timeout=15)
        resp.raise_for_status()
        return "\n".join(line.rstrip() for line in resp.text.strip().splitlines())
    except Exception as e:
        print(f"  Warning: could not fetch BibTeX for {arxiv_id}: {e}")
        return ""
