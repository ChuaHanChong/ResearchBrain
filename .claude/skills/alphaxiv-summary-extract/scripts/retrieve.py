"""retrieve.py — Selenium helpers to scrape a paper's title and Problem/Method/Results/Takeaways from its alphaxiv overview."""
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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


def _js_click(driver: webdriver.Chrome, xpath: str) -> object:
    """Find element by XPath and click it via JS (bypasses overflow/interactability issues)."""
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", el)
    return el


def _js_text(driver: webdriver.Chrome, element: object) -> str:
    """Extract text via JS textContent (works even when CSS hides the element from .text)."""
    return driver.execute_script("return arguments[0].textContent;", element).strip()


def _click_through_to_overview(driver: webdriver.Chrome, arxiv_id: str) -> None:
    """Reach the overview by clicking through from /abs/ rather than hitting
    /overview/ directly — the direct SSR route is per-IP rate-limited (HTTP 500)."""
    driver.get(f"https://www.alphaxiv.org/abs/{arxiv_id}")
    time.sleep(5)
    # Click the in-app anchor (not driver.get) so the SPA router soft-navigates.
    link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"a[href*='/overview/{arxiv_id}']"))
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
