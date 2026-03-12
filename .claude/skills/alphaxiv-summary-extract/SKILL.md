---
name: alphaxiv-summary-extract
description: Use when the user says "update knowledge hub". Batch-processes a list
  of arxiv papers from knowledge.py using Selenium, scrapes structured summaries
  (Problem/Method/Results/Takeaways) from alphaxiv.org, and saves incrementally to
  KnowledgeHub.json — skipping papers already in the KB. Do NOT use for single-paper
  lookup — use alphaxiv-paper-lookup instead.
---

# AlphaXiv Summary Extract

Batch-process arxiv papers from `knowledge.py`, scrape structured summaries via Selenium on alphaxiv.org, and save results incrementally to `KnowledgeHub.json`.

## When to Use

- User says "update knowledge hub"

## Prerequisites

- Chrome + ChromeDriver installed and on PATH
- Python dependencies — install into the active environment with:
  ```bash
  python3 -m pip install selenium requests beautifulsoup4 tqdm
  ```

## Workflow

### Step 1: Confirm paths

Default paths (relative to vault root):
- **Paper list**: `.claude/skills/alphaxiv-summary-extract/scripts/knowledge.py`
- **Output**: `KnowledgeHub.json`

If the user specifies different paths, use those. Otherwise, proceed with defaults.

### Step 2: Run the pipeline

From the vault root:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py \
  --output KnowledgeHub.json
```

For a test run on a small batch first, add `--limit 3`:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py \
  --output KnowledgeHub.json \
  --limit 3
```

### Step 3: Report results

After the script completes, report to the user:
- **Processed**: N new papers added to `KnowledgeHub.json`
- **Skipped**: N papers already in KB (not re-scraped)
- **Failed**: list any paper URLs that errored
- **Quality warnings**: any sections with fewer than 3 items

## Notes

- The script saves **incrementally** after each paper — safe to interrupt and resume
- Papers already in `KnowledgeHub.json` are automatically skipped (deduplication by URL)
- Duplicate URLs within `knowledge.py` are silently deduplicated before processing
