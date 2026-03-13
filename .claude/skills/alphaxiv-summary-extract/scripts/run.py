#!/usr/bin/env python3
"""
Batch-extract paper summaries from alphaxiv.org via Selenium.

Usage:
    python run.py --input scripts/knowledge.py --output KnowledgeHub.json
    python run.py --input scripts/knowledge.py --output KnowledgeHub.json --limit 3
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

from selenium import webdriver
from tqdm import tqdm


def load_papers(input_path: str) -> list:
    spec = importlib.util.spec_from_file_location("knowledge", input_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.papers


def load_knowledge_base(output_path: str) -> tuple:
    path = Path(output_path)
    if path.exists():
        with open(path) as f:
            data = json.load(f)
    else:
        data = {}
    return data, set(data.keys())


def save_knowledge_base(data: dict, output_path: str) -> None:
    sorted_data = dict(sorted(data.items(), reverse=True))
    with open(output_path, "w") as f:
        json.dump(sorted_data, f, indent=4, ensure_ascii=False)


def init_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


def arxiv_to_alphaxiv_url(arxiv_url: str) -> str:
    """Convert arxiv URL to alphaxiv overview URL.

    https://arxiv.org/abs/2601.22628 -> https://alphaxiv.org/overview/2601.22628
    https://arxiv.org/pdf/2602.23759 -> https://alphaxiv.org/overview/2602.23759
    """
    paper_id = arxiv_url.rstrip("/").split("/")[-1]
    return f"https://alphaxiv.org/overview/{paper_id}"


def quality_check(entry: dict, url: str) -> None:
    for section in ["Problem", "Method", "Results", "Takeaways"]:
        items = entry.get(section, [])
        if isinstance(items, list) and len(items) < 3:
            print(f"  Warning: {section} has only {len(items)} items for {url}")


def main():
    parser = argparse.ArgumentParser(description="Batch-extract paper summaries from alphaxiv.org")
    parser.add_argument("--input", required=True, help="Path to knowledge.py with papers list")
    parser.add_argument("--output", default="KnowledgeHub.json", help="Output JSON path (default: KnowledgeHub.json)")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N papers (for testing)")
    args = parser.parse_args()

    # Make retrieve.py importable from the scripts directory
    scripts_dir = str(Path(__file__).parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from retrieve import extract_title, extract_summary

    # Load paper list, deduplicate preserving order
    all_papers = load_papers(args.input)
    unique_papers = list(dict.fromkeys(all_papers))
    if len(all_papers) != len(unique_papers):
        print(f"Removed {len(all_papers) - len(unique_papers)} duplicates from paper list.")

    data, processed_urls = load_knowledge_base(args.output)
    to_process = [url for url in unique_papers if url not in processed_urls]
    if args.limit:
        to_process = to_process[: args.limit]

    print(f"Papers in list : {len(unique_papers)}")
    print(f"Already in KH  : {len(processed_urls)}")
    print(f"To process     : {len(to_process)}")

    if not to_process:
        print("Nothing to do.")
        return

    driver = init_driver()
    processed = 0
    failed = []

    try:
        for url in tqdm(to_process, desc="Extracting"):
            try:
                alphaxiv_url = arxiv_to_alphaxiv_url(url)
                title = extract_title(url)
                summary = extract_summary(driver, alphaxiv_url)

                entry = {"Title": title, **summary}
                quality_check(entry, url)

                data[url] = entry
                save_knowledge_base(data, args.output)  # incremental save
                processed += 1

            except Exception as e:
                print(f"\n  Failed: {url}\n    {e}")
                failed.append(url)
    finally:
        driver.quit()

    print(f"\n{'=' * 40}")
    print(f"Processed : {processed}")
    print(f"Skipped   : {len(processed_urls)} (already in Knowledge Hub)")
    print(f"Failed    : {len(failed)}")
    if failed:
        print("Failed papers:")
        for paper in failed:
            print(f"  - {paper}")


if __name__ == "__main__":
    main()
