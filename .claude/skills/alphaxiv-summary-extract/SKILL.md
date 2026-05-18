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

Two entry modes (single paper / batch) feed identical post-processing.

### Mode A: Single paper

When `$ARGUMENTS` contains an arxiv ID or URL:

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

### Mode B: Batch (update knowledge hub)

Defaults (relative to vault root):
- Paper list: `.claude/skills/alphaxiv-summary-extract/scripts/knowledge.py`
- Output directory: `_KnowledgeHub_`

```bash
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py \
  --out _KnowledgeHub_
```

Add `--limit 3` for a small test run; `--force` to overwrite existing notes.

### Post-processing (both modes)

#### Enrich newly generated notes

Use `Skill(skill="obsidian:obsidian-markdown")` and the Edit tool to enrich each new `.md` file. For batch frontmatter property updates across many notes (e.g., adding a tag to N papers at once), prefer `Skill(skill="obsidian:obsidian-cli")` over per-file Edits.

1. **Extract `authors`** from the BibTeX block. If the paper has 5 or fewer authors, list ALL of them. If the paper has MORE than 5 authors, keep exactly 5 entries: the first 3 authors AND the last 2 authors (i.e., `authors[:3] + authors[-2:]`). Never include `- ...` as a placeholder entry.
   - **Worked example** — given 8 authors `[A, B, C, D, E, F, G, H]`, the result MUST be `[A, B, C, G, H]` (5 names). DO NOT output `[A, B, C, H]` (4 names — this drops the second-to-last author and is the historical bug).
   - **Sanity check** — after trimming, if the original list had >5 authors, your result MUST have exactly 5 entries. If it has 4, you have made the historical mistake; redo it including BOTH last-two authors.
2. **Infer `tags`** (3–6 tags from the canonical taxonomy in the next sub-section) and add them to the frontmatter.
3. **Set `aliases`** (the model/system short name, e.g., `DreamZero`) and add them to the frontmatter. Always provide at least one alias. Use the model/system short name if the paper introduces one (e.g., `DreamZero`). For surveys or papers without a specifically named contribution, derive a descriptive alias from the title (e.g., `VLM Survey 2025`, `RLHF Benchmark`). Never leave `aliases: []` empty.
4. **Apply formatting** to the **Method** section only:
   - Use `==technical term==` highlights for key technical terms (architectures, losses, algorithms).
   - Use `**ModelName**` in bold for the paper's model or method names.
5. **Apply formatting** to the **Results** section only:
   - Use `**X%**` in bold for numbers, percentages, and key metrics.

> Do NOT add highlights or bold to Summary, Problem, or Takeaways sections.

##### Canonical Tag Taxonomy (61 tags)

> **Single source of truth for the tag vocabulary used across all skills.** `Skill(skill="paper-curate")` references this table for routing — keep tag names exact (renames must propagate). Run `validate-tags` (see `Skill(skill="paper-curate")`) after any change to detect drift.

Pick 3–6 tags per note (step 2 above). Only use tags from this list.

| Category | Tags |
|----------|------|
| **Models/Architectures** | `LLM`, `VLM`, `VLA`, `world-model`, `diffusion`, `vision-transformer`, `mixture-of-experts`, `reward-model`, `generative-model` |
| **Methods/Techniques** | `reinforcement-learning`, `self-supervised-learning`, `contrastive-learning`, `knowledge-distillation`, `domain-adaptation`, `continual-learning`, `imitation-learning`, `fine-tuning`, `chain-of-thought`, `RLHF`, `meta-learning`, `curriculum-learning`, `in-context-learning`, `self-play`, `flow-matching`, `model-merging`, `sim-to-real` |
| **Training/Scaling** | `pre-training`, `scaling`, `synthetic-data`, `parameter-efficient`, `test-time-scaling` |
| **Applications** | `robotics`, `autonomous-driving`, `embodied-AI`, `agentic-AI`, `code-generation`, `medical-imaging`, `humanoid`, `dexterous` |
| **Tasks/Capabilities** | `reasoning`, `spatial-reasoning`, `visual-grounding`, `planning`, `object-detection`, `segmentation`, `3D-understanding`, `video-understanding`, `image-generation`, `navigation`, `manipulation`, `tool-use`, `tactile`, `egocentric` |
| **Properties/Concerns** | `hallucination`, `efficiency`, `interpretability`, `robustness`, `safety`, `physics-aware` |
| **Paper Type** | `survey`, `benchmark` |

**Definitions for the 6 newly-added tags** (added 2026-05-18 after vault-wide audit):
- `physics-aware` — paper grounds models in physical priors / Newtonian / commonsense physics (methods, datasets, or benchmarks that test physical fidelity)
- `sim-to-real` — focuses on the simulation-to-real transfer problem (domain randomization, real-to-sim, etc.)
- `humanoid` — humanoid / whole-body / bipedal robot platforms
- `dexterous` — multi-finger / dexterous manipulation (vs. parallel-jaw)
- `tactile` — touch / force / haptic sensing (GelSight, DIGIT, visuo-tactile)
- `egocentric` — first-person / hand-cam / Ego4D-style data and pretraining

#### Report results

- **Processed**: N new notes written to `_KnowledgeHub_/`
- **Skipped**: N papers already have a note
- **Failed**: list any paper URLs that errored

#### Alias dedup check

After enrichment, verify each new alias is unique across the vault. For each newly-set alias, invoke `Skill(skill="obsidian:obsidian-cli")` to search for other notes using the same alias. List all collisions in chat (the user needs to know which notes collide to decide who renames). Accept the collision only if the papers are genuinely related variants (e.g., `DreamerV3` vs `DreamerV3-XL`); otherwise rename one.

#### Refresh graph

If extraction wrote at least one new note:

```
Skill(skill="graphify", args="./_KnowledgeHub_ --update --no-viz")
```

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
- `authors`, `tags`, and `aliases` in frontmatter start empty (`[]`) — the post-processing enrichment step fills them in
- `authors` must never contain `- ...` as a placeholder — use real names only, or omit the field
- `aliases` must never remain `[]` — always derive at least one alias from the title or paper content
- `authors` and `aliases` values must always be double-quoted in YAML (e.g., `- "Author Name"`, `- "ModelName"`)
- `tags` must NOT be quoted — use plain values (e.g., `- robotics`, NOT `- "robotics"`)
- Use the Edit tool + `Skill(skill="obsidian:obsidian-markdown")` for enrichment — do not write custom Python scripts for frontmatter changes
