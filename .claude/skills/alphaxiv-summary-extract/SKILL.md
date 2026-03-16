---
name: alphaxiv-summary-extract
description: Use when the user wants to save a paper (or papers) as an Obsidian note in the KnowledgeHub — whether that's a single arxiv URL/ID or a full batch update ("update knowledge hub"). Scrapes structured summaries from alphaxiv.org and writes one Obsidian markdown note per paper into the output directory, skipping papers that already have a note.
---

# AlphaXiv Summary Extract

Scrape paper summaries from alphaxiv.org and write Obsidian markdown notes (`{ID}.md`) — works for a single paper or a full batch from `knowledge.py`.

## When to Use

- User says "update knowledge hub" → batch mode
- User shares an arxiv URL/ID and wants it saved as a note → single-paper mode

## Prerequisites

- Chrome + ChromeDriver installed and on PATH
- Python dependencies:
  ```bash
  python3 -m pip install selenium requests beautifulsoup4 tqdm
  ```

## Workflow

### Single paper

When `$ARGUMENTS` contains an arxiv ID or URL, run:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --ids $ARGUMENTS \
  --out X01_KnowledgeHub
```

Multiple IDs or URLs in `$ARGUMENTS` are passed directly — they all work:

```
2602.15922
2602.15922 2601.16163
https://arxiv.org/abs/2602.15922
```

### Batch (update knowledge hub)

#### Step 1: Confirm paths

Defaults (relative to vault root):
- **Paper list**: `.claude/skills/alphaxiv-summary-extract/scripts/knowledge.py`
- **Output directory**: `X01_KnowledgeHub`

#### Step 2: Run the pipeline

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py \
  --out X01_KnowledgeHub
```

For a test run on a small batch first, add `--limit 3`:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py \
  --out X01_KnowledgeHub \
  --limit 3
```

Use `--force` to overwrite existing notes.

### Step 3: Enrich newly generated notes (obsidian-markdown skill)

For each newly written `.md` file, use the `obsidian-markdown` skill to:

1. **Extract `authors`** from the BibTeX block (first + last author, max 5 total) and add to frontmatter
2. **Infer `tags`** (3–6 topic tags, e.g. `diffusion`, `VLA`, `world-model`, `RL`, `robotics`) and add to frontmatter
3. **Extract `aliases`** (the model/system short name, e.g. `DreamZero`) and add to frontmatter
4. **Apply formatting** to **Method** section only:
   - `==technical term==` highlights on key technical terms (architectures, losses, algorithms)
   - `**ModelName**` bold on the paper's model/method names
5. **Apply formatting** to **Results** section only:
   - `**X%**` bold on numbers, percentages, and key metrics

> Do NOT add highlights or bold to Summary, Problem, or Takeaways sections.

### Step 4: Report results

- **Processed**: N new notes written to `X01_KnowledgeHub/`
- **Skipped**: N papers already have a note
- **Failed**: list any paper URLs that errored

## Refreshing BibTeX (optional, on demand)

To update BibTeX blocks in existing notes with the latest data from arXiv:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/refresh_bibtex.py \
  --notes-dir X01_KnowledgeHub
```

To refresh specific papers only:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/refresh_bibtex.py \
  --notes-dir X01_KnowledgeHub \
  --ids 2602.15922 2601.16163
```

## Notes

- The script skips papers whose `{ID}.md` already exists — safe to interrupt and resume
- BibTeX is fetched from `https://arxiv.org/bibtex/{ID}` during note generation
- `authors`, `tags`, and `aliases` in frontmatter start empty (`[]`) — Step 3 fills them in
