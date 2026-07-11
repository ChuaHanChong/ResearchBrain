"""Helpers to pull a paper's title, its Problem/Method/Results/Takeaways (Selenium), and its Detailed Report (`.md`, formatted by format_reports) from the alphaxiv overview."""
import re
import time
from collections.abc import Set
from typing import Optional

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import ABS_URL, REPORT_URL, overview_link_selector
from format_reports import format_report
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


def _panel_for(driver: webdriver.Chrome, tab: str) -> WebElement:
    """Return the ARIA tabpanel element that the tab button labeled `tab` controls."""
    # The overview renders each section as a role=tabpanel whose id the tab button points to via
    # aria-controls (the id prefix is a dynamic React useId, so resolve it per-page). Inactive panels
    # are hidden but already in the DOM with their content, so no click is needed — textContent reads them.
    btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//button[normalize-space()='{tab}']"))
    )
    return driver.find_element(By.ID, btn.get_attribute("aria-controls"))


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

    # Summary is a paragraph panel; Problem/Method/Results/Takeaways each render a <ul><li> list. Read
    # each from its own aria-controls panel (earlier ancestor-hop grabbed a shared wrapper of all tabs).
    info["Summary"] = _js_text(driver, _panel_for(driver, "Summary"))
    for tab in ["Problem", "Method", "Results", "Takeaways"]:
        items = _panel_for(driver, tab).find_elements(By.XPATH, ".//li")
        info[tab] = [t for t in (_js_text(driver, li) for li in items) if t]

    return info
