import time

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def extract_title(url):
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


def _js_click(driver, xpath):
    """Find element by XPath and click it via JS (bypasses overflow/interactability issues)."""
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", el)
    return el


def _js_text(driver, element):
    """Extract text via JS textContent (works even when CSS hides the element from .text)."""
    return driver.execute_script("return arguments[0].textContent;", element).strip()


def extract_summary(driver, url):
    driver.get(url)
    time.sleep(5)

    # Switch to Machine view (new UI toggle added since original scripts were written)
    _js_click(driver, "//button[normalize-space()='Machine']")
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
