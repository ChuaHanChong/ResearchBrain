"""Helpers to pull a paper's title, its Problem/Method/Results/Takeaways (Selenium), and its detailed Research Report (`.md`) from the alphaxiv overview."""
import re
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import ABS_URL, REPORT_URL, overview_link_selector
from sanitize import sanitize


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


def _clean_research_report(md: str) -> str:
    """Normalize alphaxiv's raw overview `.md` into the note's ## Research Report body."""
    # The `.md` render is inconsistent across papers (some open with `## Research Report: <title>`,
    # others a bare paragraph + `---`); normalize to a stable shape. render_note adds the heading back.
    lines = md.replace("\r\n", "\n").split("\n")

    # Drop a single leading `## Research Report...` heading if the render included one.
    body, dropped_heading = [], False
    for line in lines:
        if not dropped_heading and re.match(r"^##\s+Research Report\b", line):
            dropped_heading = True
            continue
        body.append(line)

    # Each `### ` heading opens a section running until the next `### `. Drop the authors section,
    # drop standalone `---` rules, and renumber the rest from 1.
    out, drop_section, seq = [], False, 0
    for line in body:
        heading = re.match(r"^###\s+(?:\d+\.\s*)?(.*)$", line)
        if heading:
            title = heading.group(1).strip()
            drop_section = bool(re.search(r"\bauthors?\b", title, re.IGNORECASE))
            if drop_section:
                continue
            seq += 1
            out.append(f"### {seq}. {title}")
        elif drop_section or line.strip() == "---":
            continue
        else:
            out.append(line)

    return "\n".join(out).strip()


def fetch_research_report(arxiv_id: str) -> str:
    """Fetch alphaxiv's detailed overview `.md`, normalized for the note's ## Research Report section."""
    # Return "" on any failure (rate-limit, 404/withdrawn) so the note is still written without it —
    # a missing report beats a fabricated one.
    try:
        resp = requests.get(REPORT_URL.format(arxiv_id), headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"  Warning: could not fetch research report for {arxiv_id}: {e}")
        return ""
    return _clean_research_report(resp.text)


def _js_click(driver: webdriver.Chrome, xpath: str) -> object:
    """Find element by XPath and click it via JS (bypasses overflow/interactability issues)."""
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", el)
    return el


def _js_text(driver: webdriver.Chrome, element: object) -> str:
    """Extract an element's text via JS textContent and repair KaTeX/LaTeX/control-char corruption."""
    # textContent works even when CSS hides the element from Selenium's .text.
    raw = driver.execute_script("return arguments[0].textContent;", element)
    # collapse spurious newlines (each call is one paragraph/<li>; KaTeX math else explodes per token)
    raw = re.sub(r'\s*\n\s*', ' ', raw).strip()
    return sanitize(raw)


def _click_through_to_overview(driver: webdriver.Chrome, arxiv_id: str) -> None:
    """Navigate to the paper's overview by clicking through from its /abs/ page."""
    # Click through from /abs/ rather than hitting /overview/ directly — the direct SSR route is
    # per-IP rate-limited (HTTP 500).
    driver.get(ABS_URL.format(arxiv_id))
    time.sleep(5)
    # Click the in-app anchor (not driver.get) so the SPA router soft-navigates.
    link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, overview_link_selector(arxiv_id)))
    )
    driver.execute_script("arguments[0].click();", link)


def extract_summary(driver: webdriver.Chrome, arxiv_id: str) -> dict[str, object]:
    """Scrape the alphaxiv overview and return Summary/Problem/Method/Results/Takeaways."""
    _click_through_to_overview(driver, arxiv_id)
    time.sleep(1)

    # Click the Human/Machine toggle only if present (2026-06 UI dropped it).
    machine = driver.find_elements(By.XPATH, "//button[normalize-space()='Machine']")
    if machine:
        driver.execute_script("arguments[0].click();", machine[0])
        time.sleep(1)

    info = {}

    # Summary tab — plain text paragraph
    _js_click(driver, "//button[normalize-space()='Summary']")
    time.sleep(1)
    content = driver.find_element(By.XPATH, "//button[normalize-space()='Summary']/../../../../div[2]")
    info["Summary"] = _js_text(driver, content)

    # Problem / Method / Results / Takeaways — each renders a <ul><li> list
    for tab in ["Problem", "Method", "Results", "Takeaways"]:
        _js_click(driver, f"//button[normalize-space()='{tab}']")
        time.sleep(1)
        items = driver.find_elements(By.XPATH, f"//button[normalize-space()='{tab}']/../../../../div[2]//li")
        info[tab] = [t for t in (_js_text(driver, li) for li in items) if t]

    return info
