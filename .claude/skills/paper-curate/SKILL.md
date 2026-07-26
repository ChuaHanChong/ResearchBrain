---
name: paper-curate
description: "Maintain General/ topic overview files using a graph + agent hybrid. Assign new KnowledgeHub papers to topics, refresh `[!star]`/`[!tip]`/`[!success]` callouts, audit coverage and find orphans, detect topic-boundary issues, create or split topic files, and lint vault quality. Use after a KnowledgeHub ingest or when the user says 'update General', 'assign papers', 'refresh callouts', 'audit coverage', 'find orphans', 'lint vault', or 'create new topic'."
---

# General/ Topic Overview Maintainer

Assign new KnowledgeHub papers to the correct General/ topic overview files, placing each paper into the appropriate curated sub-topic group. Also handles refreshing callouts, updating key paper highlights, creating new topic files, and auditing coverage.

## When to Use

- After adding new papers to `_KnowledgeHub_/` (batch or single) → **Mode A**
- User says "update General", "assign papers", "add to General" → **Mode A**
- User wants to check coverage gaps, find orphans, low-citation papers, redundant papers → **Mode B**
- User wants to create a new topic file, or asks "should I split/merge topics" → **Mode C**
- User wants to refresh callouts (`[!star]`, `[!tip]`, `[!success]`), key papers, or insights → **Mode D**
- User says "lint", "health check", "audit quality", "check vault", asks about topic boundaries → **Mode E**

## Workflow

### Mode A: Assign New Papers

#### Step 1: Find unassigned papers

```bash
PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
HELPER=.claude/skills/paper-curate/scripts/graph_query.py
$PY $HELPER unassigned
```

#### Step 2: Determine target topic file

**Signal 1 — Tag mapping (default).** Read the KH note's frontmatter `tags`, look up in the table below. Tag definitions live in `Skill(skill="alphaxiv-summary-extract")`; this table only specifies routing.

- One matching topic → assign there. Done.
- Multiple matching topics → assign to all that fit (multi-assignment is allowed).
- No tags or ambiguous → drop to the fallbacks below.

**Fallback — Graph neighbors.** Use when Signal 1 is inconclusive, or to validate placement.

```bash
PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
HELPER=.claude/skills/paper-curate/scripts/graph_query.py
$PY $HELPER neighbors 2604.28192   # any unassigned arxiv ID
```

**Tag → Topic mapping** (a paper can appear in multiple topic files if relevant):

| Tags | Topic File |
|------|-----------|
| `pre-training`, `vision-transformer`, `self-supervised-learning`, `contrastive-learning`, `scaling`, `knowledge-distillation` | `01_Foundation-Models.md` |
| `VLM`, `visual-grounding`, `in-context-learning` | `05_Vision-Language-Models.md` |
| `reasoning`, `spatial-reasoning`, `chain-of-thought`, `planning` | `07_Reasoning-and-Planning.md` |
| `reinforcement-learning`, `RLHF`, `reward-model`, `self-play`, `curriculum-learning` | `08_Reinforcement-Learning.md` |
| `object-detection`, `segmentation`, `3D-understanding`, `domain-adaptation` | `02_Computer-Vision-and-3D.md` |
| `video-understanding`, `egocentric` | `04_Video-and-Temporal.md` |
| `robotics`, `VLA`, `world-model`, `manipulation`, `embodied-AI`, `navigation`, `imitation-learning`, `autonomous-driving`, `humanoid`, `dexterous`, `tactile`, `sim-to-real`, `egocentric` | `11_Robotics-and-Embodied-AI.md` |
| `survey`, `benchmark`, `dataset` | `12_Benchmarks-and-Surveys.md` |
| `LLM`, `hallucination` | `06_Multimodal-LLMs.md` |
| `agentic-AI`, `tool-use`, `code-generation` | `10_Agents-and-Tool-Use.md` |
| `continual-learning`, `meta-learning` | `09_Self-Evolving-AI.md` |
| `diffusion`, `image-generation`, `flow-matching`, `generative-model`, `physics-aware` | `03_Diffusion-and-Generation.md` |

Edge cases:
- **Tag absent from the table** — pick the closest topic by reading the KH note's content. Add a row here if the same un-mapped tag recurs across 3+ papers.
- **Survey or benchmark in a specific domain** — assign to `12_Benchmarks-and-Surveys.md` AND the domain topic.
- **`tags: []` empty** — re-extract via `Skill(skill="alphaxiv-summary-extract")` before treating as un-mapped.

To detect drift between this table and the canonical vocabulary, run:

```bash
PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
HELPER=.claude/skills/paper-curate/scripts/graph_query.py
$PY $HELPER validate-tags
```

#### Step 3: Read the paper and place it

For each unassigned paper:

1. Read the KH note's **title**, **summary**, and **tags** to understand the paper
2. Run `same-community` to find graph-similar papers already in the topic file:
   ```bash
   PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
   HELPER=.claude/skills/paper-curate/scripts/graph_query.py
   $PY $HELPER same-community {arxiv_id} General/{topic_file}.md
   ```
   Look at which sub-topic group those neighbors live in — start there.
3. If `same-community` returns nothing useful, scan the target General/ topic file's existing sub-topic groups directly.
4. Append the wikilink `[[ID|Alias]]` to the matching sub-topic group's bullet list.
5. If no existing group fits, create a new **bold sub-topic group** with a 1-sentence description in the most relevant section.

> **Bulk influx — organize by topic, not provenance.** Merge each paper into the file's *existing* `## N. Theme` sections by what it is; never create a provenance section (`Recent Additions`, `Conference Batch`, dates). Cap a bullet at ~**30** wikilinks — when it overflows, split hierarchically (sub-theme → tag → year → `· part N`). Fold buckets <5 papers into one `**Additional methods**` bullet. Verify by grep ground-truth (every source placed ≥1×), not a section regex.

#### Step 4: Sort papers within each sub-topic

Within each sub-topic's bullet list, sort wikilinks by arxiv ID in **descending order** (newest first). This makes it easy to see the latest work at a glance.

```
Before: - [[2104.14294|DINO]], [[2502.10385|SimDINO]], [[2304.07193|DINOv2]]
After:  - [[2502.10385|SimDINO]], [[2304.07193|DINOv2]], [[2104.14294|DINO]]
```

#### Step 5: Update callouts if new papers are noteworthy

After placing papers, review whether any newly added paper deserves to be highlighted:

- **`[!star]` Key Papers**: If a new paper is more impactful than existing starred papers in that sub-topic (e.g., higher citation count, paradigm-shifting result, state-of-the-art), add it to the `[!star]` callout or replace a less impactful entry. Each `[!star]` should have 3-5 papers max.
- **`[!tip]` Insights**: If the new papers reveal a trend, shift, or practical takeaway not captured by the existing `[!tip]`, update the insight text to reflect the latest understanding.

#### Step 6: Update the Index

Update the paper count in `00_Index.md`:
```bash
total=$(ls _KnowledgeHub_/*.md | wc -l)
```

### Mode B: Audit Coverage

Coverage table + unassigned-by-centrality + orphan flagging in one call:

```bash
PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
HELPER=.claude/skills/paper-curate/scripts/graph_query.py
$PY $HELPER audit-coverage
```

Output (in chat): per-topic counts, top-10 unassigned ranked by graph centrality (high-priority to assign), orphan count, and suspicious orphans (orphans assigned to a major topic — re-tag candidates).

For a live per-topic count without running the script, see `General/_Topic-Coverage.base`.

### Mode C: Create New Topic File

Two paths to triggering this mode:

**Path 1: User asks for a new topic explicitly.** Follow the Formatting Rules template, number `{NN}_{Topic-Name}.md`, add to `00_Index.md`.

**Path 2: Graph signals an existing topic should split (SPRAWL).** When a single General/ topic spans many distinct high-cohesion communities, it's grown beyond a coherent scope. Detect:

```bash
PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
HELPER=.claude/skills/paper-curate/scripts/graph_query.py
$PY $HELPER sprawl
```

If a SPRAWL is reported, agent reviews the topic's papers + graph community structure to propose a split (e.g., split `02_VLM` into `02a_VLM-Pretraining` and `02b_VLM-Finetuning`). Show the proposed split + paper redistribution in chat. User confirms before any new topic file is created.

### Mode D: Refresh Callouts & Insights

Each callout type follows the same template: **graph supplies candidates → agent reads & synthesizes → show preview in chat → apply on user confirmation.**

```bash
PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
HELPER=.claude/skills/paper-curate/scripts/graph_query.py
TOPIC=General/08_Reinforcement-Learning.md   # any General/<X>.md
```

#### `[!star]` — top central papers in this topic

1. **Graph**: `$PY $HELPER star $TOPIC` → top-5 by topic-restricted degree.
2. **Agent**: read the topic file's prose context. Prune candidates that are central by edges but off-topic in narrative (e.g., a foundational paper that's heavily cited but no longer represents current work).
3. **Preview** in chat:
   ```
   [topic] proposed [!star] update:
     - removing: [[2503.20752|GRPO]] (no longer in top-5)
     + adding:   [[2604.23747|SFT-then-RL]] (degree 13)
   ```
4. **Apply** iff user confirms (or `--auto` flag for batch refresh after large ingest).

#### `[!tip]` — emerging trends in this topic

1. **Graph**: `$PY $HELPER recent $TOPIC` → 5 newest arxiv IDs in the topic (lexical sort).
2. **Agent**: read each KH note (Problem/Method/Results) and synthesize a 1-2 sentence trend statement.
3. **Preview** the proposed `[!tip]` text in chat.
4. **Apply** iff user confirms.

#### `[!success]` — recipes from cross-community bridges

1. **Graph**: `$PY $HELPER bridges $TOPIC` → top-5 papers with edges into other communities.
2. **Agent**: read bridge papers, identify the recipe (e.g., "GRPO + reward modeling for VLA fine-tuning").
3. **Preview** the proposed `[!success]` text in chat.
4. **Apply** iff user confirms.

#### Other callouts (`[!info]`, `[!warning]`, etc.)

No graph signal — pure agent reading and synthesis. Same preview-then-confirm flow.

#### Sort step (after any callout refresh)

Sort all paper lists by arxiv ID descending (newest first):
```
Before: - [[2104.14294|DINO]], [[2502.10385|SimDINO]], [[2304.07193|DINOv2]]
After:  - [[2502.10385|SimDINO]], [[2304.07193|DINOv2]], [[2104.14294|DINO]]
```

**Safety:** vault is git-tracked — any callout-block change is reversible via git history. Mode D modifies only callout blocks in `General/<X>.md` files. All output (diffs, proposed prose) goes to chat — never writes report files.

### Mode E: Vault Linting & Health Checks

Trigger when user says "lint", "health check", "audit quality", or "check vault". All output to chat — never writes report files.

#### Data Quality (agent reads KH notes)

```bash
PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
HELPER=.claude/skills/paper-curate/scripts/graph_query.py
$PY $HELPER data-quality
```

Findings: weak notes, empty frontmatter, tag inconsistencies. Report to chat. Offer re-extraction via `Skill(skill="alphaxiv-summary-extract")`.

#### Stale Callouts (graph-driven check)

```bash
PY=$(head -1 "$(command -v graphify)" | sed 's|^#!||')
HELPER=.claude/skills/paper-curate/scripts/graph_query.py
$PY $HELPER stale-stars
```

Per-topic drift report. User can then run Mode D on drifted topics.

#### Topic-Boundary Mismatches (graph-driven SPLIT detection)

Communities whose members span multiple General/ topics — suggests merging or noting the cross-topic connection in a `[!tip]`.

```bash
$PY $HELPER split
```

Surface findings in chat. User decides whether to merge topics or note the cross-topic bridge. Mode E never modifies topic files.

#### Missing Connections (agent-driven)

- Cross-citation gaps — agent reads Method/Results sections looking for paper-name mentions, flags pairs not grouped together
- New sub-topic candidates — agent reviews 3+ related papers in a General/ sub-topic that could form a more specific group
- Auto-refresh `00_Index.md` paper counts

## Formatting Rules

These rules are critical — they come from user feedback and define what makes a well-maintained General/ file.

### Document Structure

```
---
title: "{Topic Title} — Topic Overview"
tags:
  - tag1
  - tag2
aliases:
  - Short Alias
---

# {Topic Title}

> [!abstract] Overview
> {2-3 sentences explaining scope and evolution}

## Evolution Graph
{ASCII/Unicode box diagram in a ```text fence — see references/topic-file-formatting.md}

{1-2 sentence evolutionary trend paragraph}

| Year | Paper | Contribution |
|------|-------|-------------|
| YYYY | [[ID\|Name]] | One-sentence contribution |

---

## 1. {Section Title}
{1-2 sentence description}

**{Sub-topic}** — {Description}
- [[newest_ID|Paper1]], [[older_ID|Paper2]], [[oldest_ID|Paper3]]

> [!star] Key Papers
> - [[ID|Paper1]] — Why it matters (1 sentence)
> - [[ID|Paper2]] — Why it matters (1 sentence)

**{Sub-topic 2}** — {Description}
- [[ID|Paper1]], [[ID|Paper2]]

> [!star] Key Papers
> - [[ID|Paper1]] — Why it matters

> [!tip] {Insight Title}
> {2-3 sentences of practical guidance or synthesis}

---

## Cross-References
- [[Related_Topic]] — How it connects

---
*Next: [[Next_Topic]] for X.*
```

> When creating or restructuring a General/ topic file, read `references/topic-file-formatting.md` for paper-ordering rules, callout types, wikilink format, sub-topic group conventions, ASCII evolution graphs, and the "what NOT to do" list.

## Notes

- A paper can appear in multiple topic files if it spans multiple areas
- Surveys and benchmarks go in `12_Benchmarks-and-Surveys.md` AND the relevant domain file
- When >15 papers in a sub-topic, consider splitting into 2 sub-topics
- Keep the Index file's paper count updated after changes
- When adding papers, always check if they deserve `[!star]` status — a great paper buried in a list without recognition is a missed opportunity
