---
name: alphaxiv-summary-extract
description: "Extract paper summaries from alphaxiv.org and write enriched Obsidian notes into KnowledgeHub. Use whenever the user says 'update knowledge hub', 'add this paper', 'save this paper', 'extract this paper', shares an arxiv URL/ID and wants it saved as a note, or wants to batch-process new papers. Also trigger when the user asks about enrichment rules, tag taxonomy, or KnowledgeHub note formatting conventions."
---

# AlphaXiv Summary Extract

Scrape paper summaries from alphaxiv.org and write Obsidian markdown notes (`{ID}.md`) — works for a single paper or a full batch from `knowledge.py`.

## When to Use

- User says "update knowledge hub" → **batch mode** (processes all papers in `knowledge.py`)
- User shares an arxiv URL/ID and wants it saved as a note → **single-paper mode**

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
  --out _KnowledgeHub_
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
- **Output directory**: `_KnowledgeHub_`

#### Step 2: Run the pipeline

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py \
  --out _KnowledgeHub_
```

For a test run on a small batch first, add `--limit 3`:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py \
  --out _KnowledgeHub_ \
  --limit 3
```

Use `--force` to overwrite existing notes.

### Step 3: Enrich newly generated notes

After extraction (both single-paper and batch mode), use the `obsidian-markdown` skill and Edit tool to enrich each new `.md` file:

1. **Extract `authors`** from the BibTeX block (maximum of 5 total; keep the first 3 and the last 2 if there are more than 5 authors) and add them to the frontmatter. Never include `- ...` as a placeholder entry.
2. **Infer `tags`** (3–6 tags from the canonical taxonomy below) and add them to the frontmatter.

#### Canonical Tag Taxonomy (55 tags)

Pick 3–6 tags per note. Only use tags from this list.

| Category | Tags |
|----------|------|
| **Models/Architectures** | `LLM`, `VLM`, `VLA`, `world-model`, `diffusion`, `vision-transformer`, `mixture-of-experts`, `reward-model`, `generative-model` |
| **Methods/Techniques** | `reinforcement-learning`, `self-supervised-learning`, `contrastive-learning`, `knowledge-distillation`, `domain-adaptation`, `continual-learning`, `imitation-learning`, `fine-tuning`, `chain-of-thought`, `RLHF`, `meta-learning`, `curriculum-learning`, `in-context-learning`, `self-play`, `flow-matching`, `model-merging` |
| **Training/Scaling** | `pre-training`, `scaling`, `synthetic-data`, `parameter-efficient`, `test-time-scaling` |
| **Applications** | `robotics`, `autonomous-driving`, `embodied-AI`, `agentic-AI`, `code-generation`, `medical-imaging` |
| **Tasks/Capabilities** | `reasoning`, `spatial-reasoning`, `visual-grounding`, `planning`, `object-detection`, `segmentation`, `3D-understanding`, `video-understanding`, `image-generation`, `navigation`, `manipulation`, `tool-use` |
| **Properties/Concerns** | `hallucination`, `efficiency`, `interpretability`, `robustness`, `safety` |
| **Paper Type** | `survey`, `benchmark` |

3. **Set `aliases`** (the model/system short name, e.g., `DreamZero`) and add them to the frontmatter. Always provide at least one alias. Use the model/system short name if the paper introduces one (e.g., `DreamZero`). For surveys or papers without a specifically named contribution, derive a descriptive alias from the title (e.g., `VLM Survey 2025`, `RLHF Benchmark`). Never leave `aliases: []` empty.
4. **Apply formatting** to the **Method** section only:
   - Use `==technical term==` highlights for key technical terms (architectures, losses, algorithms).
   - Use `**ModelName**` in bold for the paper's model or method names.
5. **Apply formatting** to the **Results** section only:
   - Use `**X%**` in bold for numbers, percentages, and key metrics.

> Do NOT add highlights or bold to Summary, Problem, or Takeaways sections.

### Step 4: Report results

- **Processed**: N new notes written to `_KnowledgeHub_/`
- **Skipped**: N papers already have a note
- **Failed**: list any paper URLs that errored

## Refreshing BibTeX (optional, on demand)

To update BibTeX blocks in existing notes with the latest data from arXiv:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/refresh_bibtex.py \
  --notes-dir _KnowledgeHub_
```

To refresh specific papers only:

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/refresh_bibtex.py \
  --notes-dir _KnowledgeHub_ \
  --ids 2602.15922 2601.16163
```

## Notes

- The script skips papers whose `{ID}.md` already exists — safe to interrupt and resume
- BibTeX is fetched from `https://arxiv.org/bibtex/{ID}` during note generation
- `authors`, `tags`, and `aliases` in frontmatter start empty (`[]`) — Step 3 fills them in
- `authors` must never contain `- ...` as a placeholder — use real names only, or omit the field
- `aliases` must never remain `[]` — always derive at least one alias from the title or paper content
- `authors` and `aliases` values must always be double-quoted in YAML (e.g., `- "Author Name"`, `- "ModelName"`)
- Use the Edit tool + obsidian-markdown skill for enrichment — do not write custom Python scripts for frontmatter changes

## Enrichment Health Check

When asked to "lint", "check quality", or "audit enrichment", scan KH notes for:
- `authors: []` — missing authors, re-extract from BibTeX
- `tags: []` — missing tags, infer from title and content
- `aliases: []` — missing aliases, derive from title
- Method sections without `==highlights==` or `**bold**` formatting
- Results sections without `**bold**` metrics
