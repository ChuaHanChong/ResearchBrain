"""Fetch a paper's title, five short fields, and Detailed Report; validate a summary payload's shape.

Title and the Detailed Report come straight from arxiv/alphaxiv. The five short fields are generated
by generate_summary(), which shells out to a headless `claude -p` subagent.
"""
import json
import subprocess
from collections.abc import Set
from typing import Optional

import requests
from bs4 import BeautifulSoup

from common import REPORT_URL
from format_reports import format_report

SUMMARY_KEYS = ("Summary", "Problem", "Method", "Results", "Takeaways")

# Canonical prompt — mirrored in SKILL.md Step 1; keep both in sync.
GENERATION_PROMPT = """\
Call mcp__alphaxiv__get_paper_content with url="https://arxiv.org/abs/{arxiv_id}" and fullText=true.

From that raw text, synthesize five short fields, each with a content rule and a strict limit:

- Summary: what the method IS, its core mechanism(s) plus the headline outcome, plain terms like a
  strong abstract. One paragraph, 40-70 words.
- Problem: the gap or limitation in PRIOR WORK that motivates this paper, not what this paper does, not
  background survey. Exactly 3 bullets, each 15-30 words.
- Method: this paper's OWN NAMED components/mechanisms, what it introduces or builds, not a restatement
  of Problem. Name the technique (architecture, loss, algorithm, data pipeline) each bullet describes.
  Exactly 3 bullets, each 15-35 words.
- Results: EMPIRICAL EVIDENCE, benchmark numbers, comparisons to baselines, ablation confirmations.
  Every bullet should carry a concrete number where the paper has one; don't restate Method. Exactly 3
  bullets, each 15-35 words.
- Takeaways: the GENERALIZABLE INSIGHT for a reader, what transfers beyond this paper's exact setup or
  numbers (a design principle, a surprising finding, a caution), not a re-summary of Results. Exactly 3
  bullets, each 15-30 words.

No [N]-style citation markers or bare arxiv IDs in any field.

Reply with ONLY this JSON object, no other text, no markdown code fence:
{{"Summary": "...", "Problem": ["...", "...", "..."], "Method": ["...", "...", "..."], "Results": ["...", "...", "..."], "Takeaways": ["...", "...", "..."]}}
"""

GENERATE_TIMEOUT = 300  # measured ~90-130s/paper; margin


def extract_title(url: str) -> Optional[str]:
    """Fetch the arxiv abstract page and return the paper title, or None on failure."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.find("h1", class_="title mathjax").text.replace("Title:", "").strip()
        return title

    except Exception as e:
        print(f"Error extracting title: {e}")
        return None


def fetch_research_report(arxiv_id: str, kh_ids: Set[str] = frozenset()) -> str:
    """Fetch alphaxiv's overview `.md` and format it into the note's ## Detailed Report body."""
    # kh_ids (in-vault arxiv IDs) lets format_reports wikilink in-KH citations. Returns "" on any failure
    # (rate-limit, 404/withdrawn) so the note is still written without it (a missing report beats a
    # fabricated one). All cleaning lives in format_reports.format_report; checks in validate_reports.py.
    try:
        resp = requests.get(REPORT_URL.format(arxiv_id), headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"  Warning: could not fetch research report for {arxiv_id}: {e}")
        return ""
    return format_report(resp.text, kh_ids)


def generate_summary(arxiv_id: str) -> dict:
    """Shell out to a headless claude -p subagent to synthesize the five short fields for one paper."""
    prompt = GENERATION_PROMPT.format(arxiv_id=arxiv_id)
    try:
        result = subprocess.run(
            [
                "claude", "-p", prompt,
                "--allowedTools", "mcp__alphaxiv__get_paper_content",
                "--permission-mode", "acceptEdits",
                "--output-format", "json",
            ],
            capture_output=True, text=True, timeout=GENERATE_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"claude -p timed out after {GENERATE_TIMEOUT}s")
    if result.returncode != 0:
        raise RuntimeError(f"claude -p exited {result.returncode}: {result.stderr[:300]}")
    outer = json.loads(result.stdout)
    if outer.get("is_error"):
        raise RuntimeError(f"claude -p reported error: {str(outer.get('result'))[:300]}")
    text = outer.get("result", "")
    # the agent's final message should be pure JSON, but tolerate stray prose/fences around it
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise RuntimeError(f"no JSON object in claude -p result: {text[:300]!r}")
    payload = json.loads(text[start:end + 1])
    return validate_summary(payload)


def validate_summary(payload: dict) -> dict[str, object]:
    """Validate a paper's generated summary payload has the five expected keys and shapes."""
    # Raises ValueError so a malformed payload is a clear Failed reason, not a bad note.
    missing = [k for k in SUMMARY_KEYS if k not in payload]
    if missing:
        raise ValueError(f"summary payload missing keys: {missing}")
    if not isinstance(payload["Summary"], str):
        raise ValueError("Summary must be a string")
    for k in ("Problem", "Method", "Results", "Takeaways"):
        if not isinstance(payload[k], list) or not all(isinstance(x, str) for x in payload[k]):
            raise ValueError(f"{k} must be a list of strings")
    return payload
