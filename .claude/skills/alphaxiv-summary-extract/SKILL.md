---
name: alphaxiv-summary-extract
description: "Generate enriched Obsidian KnowledgeHub notes ({arxiv_ID}.md) from arxiv papers, single paper or full knowledge.py batch. Use whenever the user wants to ingest, add, or save arxiv papers into the knowledge hub, or shares an arxiv URL/ID to save (e.g. 'update knowledge hub', 'add these papers'). Also use it to rescue notes missing a Detailed Report by auto-generating the alphaxiv overview via a cmux browser (e.g. 'backfill the missing detailed reports', 'generate overviews for these papers'). Covers content generation (via mcp__alphaxiv__get_paper_content), enrichment, tagging, and note-formatting rules."
---

# AlphaXiv Summary Extract

Generate Obsidian markdown notes (`{ID}.md`) for arxiv papers — works for a single paper or a full batch from `knowledge.py`. Each note carries a structured summary (Summary / Problem / Method / Results / Takeaways), a hidden BibTeX block, and a `## Detailed Report`. The five structured fields are synthesized by `extract_summaries.py` itself — it shells out to a headless `claude -p` subagent per paper, which reads the paper's own full text via `mcp__alphaxiv__get_paper_content(fullText=true)`. The `## Detailed Report` is fetched from alphaxiv's machine-readable `.md` render (`overview/{ID}.md`).

## When to Use

- User says "update knowledge hub" → **batch mode** (processes all papers in `knowledge.py`)
- User shares an arxiv URL/ID and wants it saved as a note → **single-paper mode**

## Prerequisites

- The vault's **`.venv`** (managed by `uv`) with `requests`, `beautifulsoup4`, `tqdm`. Run every `python …` command below with that interpreter — `.venv/bin/python …` (or `uv run python …`). Install if missing: `uv sync` (or `.venv/bin/python -m pip install requests beautifulsoup4 tqdm`).
- `claude` CLI on PATH, reachable non-interactively as `claude -p ... --allowedTools "mcp__alphaxiv__get_paper_content" --permission-mode acceptEdits --output-format json`, including from inside a Python `subprocess.run()` call.
- `cmux` on PATH — only needed for the Detailed Report rescue (`generate_overviews.py`), not for normal ingest.

## Workflow

One script call does the whole thing, single paper or batch — `extract_summaries.py` generates each paper's five fields itself (via `generate_summary()`, a `claude -p` subprocess), then fetches title, BibTeX, and Detailed Report, then writes the note. No external `Agent`-tool dispatch, no stdin, no intermediate file.

The five fields — `Summary` (one paragraph, 40-70 words) and `Problem`/`Method`/`Results`/`Takeaways` (exactly 3 bullets each, 15-35 words/bullet) — have their content rules and limits defined in exactly one place: `retrieve.py`'s `GENERATION_PROMPT` constant, which the subprocess runs verbatim. Read that constant for the exact wording rather than a second copy here. Enforced by the prompt only, not re-checked in Python — no separate limit-warning pass.

**Why a script at all, and not just a bare `claude -p` call?** `render_note()` must be the only thing that writes a KH note. 8,700+ existing notes share exact structure (frontmatter key order, the `%%`-wrapped BibTeX block, `> [!summary]`/`> [!tip]` callout syntax) that `validate_reports.py`, `paper-curate`, and `kh-graph-sync` all parse — a bare subagent hand-writing markdown drifts on some fraction of a large batch, silently, in fields nothing checks. `generate_summary()`'s subprocess only ever returns a JSON string in memory; nothing touches disk until `render_note()` writes the final `.md`.

### Mode A: Single paper

When the user shares an arxiv URL/ID:

```bash
.venv/bin/python .claude/skills/alphaxiv-summary-extract/scripts/extract_summaries.py \
  --ids 2608.13474 --out _KnowledgeHub_
```

Multiple IDs/URLs work too (`--ids 2607.08857 2606.12995 ...`); `--force` overwrites an existing note.

### Mode B: Batch (update knowledge hub)

```bash
.venv/bin/python .claude/skills/alphaxiv-summary-extract/scripts/extract_summaries.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py --out _KnowledgeHub_
```

Add `--limit N` for a small test run. The script computes pending (`{knowledge.py IDs} − {existing KH stems}`) itself and processes each one, printing a live `tqdm` bar and a final Processed/Skipped/Failed report — one process, no orchestrator loop needed.

**Cost/time note:** each paper's `generate_summary()` call costs roughly ~140k-180k tokens and ~25-130s (measured) — the `claude -p` subprocess does a full `fullText` fetch + synthesis per paper, unavoidable regardless of batching. For a large pending backlog, run with `--limit` first, confirm `validate_reports.py` passes, then run the rest — don't silently fan out hundreds in one call.

**Failure handling:** a paper that fails `generate_summary()` (timeout, malformed JSON, MCP error) is caught per-paper and folded into the Failed list — the loop continues to the next paper, nothing else is lost. Re-run with `--ids <failed-id>` to retry just that one.

### Post-processing (both modes)

#### Enrich newly generated notes

Use `Skill(skill="obsidian:obsidian-markdown")` and the Edit tool to enrich each new `.md` file. For batch frontmatter property updates across many notes (e.g., adding a tag to N papers at once), prefer `Skill(skill="obsidian:obsidian-cli")` over per-file Edits.

1. **Extract `authors`** from the BibTeX block. If the paper has 5 or fewer authors, list all of them. If the paper has more than 5 authors, keep exactly 5 entries: the first 3 authors plus the last 2 authors (i.e., `authors[:3] + authors[-2:]`). Use real author names only — no `- ...` placeholder entry.
   - **Worked example** — given 8 authors `[A, B, C, D, E, F, G, H]`, the result is `[A, B, C, G, H]` (5 names), not `[A, B, C, H]` (4 names — that form drops the second-to-last author, which is the historical bug).
   - **Sanity check** — after trimming, an original list of >5 authors leaves exactly 5 entries. If you end up with 4, the second-to-last author was dropped; redo it, keeping both of the last two authors.
2. **Infer `tags`** (3–6 tags from the canonical taxonomy in the next sub-section) and add them to the frontmatter.
3. **Set `aliases`** (the model/system short name, e.g., `DreamZero`) and add them to the frontmatter. Always provide at least one alias. Use the model/system short name if the paper introduces one (e.g., `DreamZero`). For surveys or papers without a specifically named contribution, derive a descriptive alias from the title (e.g., `VLM Survey 2025`, `RLHF Benchmark`). Never leave `aliases: []` empty.
4. **Apply formatting** to the **Method** section only:
   - Use `==technical term==` highlights for key technical terms (architectures, losses, algorithms).
   - Use `**ModelName**` in bold for the paper's model or method names.
5. **Apply formatting** to the **Results** section only:
   - Use `**X%**` in bold for numbers, percentages, and key metrics.

> Do NOT add highlights or bold to Summary, Problem, or Takeaways sections.

> The **`## Detailed Report`** section is fetched from alphaxiv's `.md` render and normalized at assembly by `format_reports.py` (see **"Validate & format-QA the Detailed Reports"** below). Don't add highlights or hand-tune its prose; after a batch, run the validator and read a sample.

##### Canonical Tag Taxonomy (64 tags)

> **Single source of truth for the tag vocabulary used across all skills.** `Skill(skill="paper-curate")` references this table for routing — keep tag names exact (renames must propagate). Run `validate-tags` (see `Skill(skill="paper-curate")`) after any change to detect drift.

Pick 3–6 tags per note (step 2 above). Only use tags from this list.

| Category | Tag | Explanation |
|----------|-----|-------------|
| **Models/Architectures** | `LLM` | Large language model — text-centric foundation model |
| | `VLM` | Vision-language model — image/video + text understanding |
| | `VLA` | Vision-language-action model — a VLM that outputs robot actions |
| | `world-model` | Learns environment dynamics to predict / imagine future states |
| | `diffusion` | Denoising-diffusion generative model (images, video, or policies) |
| | `vision-transformer` | ViT-style transformer backbone for visual inputs |
| | `mixture-of-experts` | Sparsely-activated expert routing (MoE) architecture |
| | `reward-model` | Learned model that scores outputs to guide RL / preference training |
| | `generative-model` | Generative backbone (VAE / GAN / autoregressive) not covered by `diffusion` |
| **Methods/Techniques** | `reinforcement-learning` | Policy learning from reward signals |
| | `self-supervised-learning` | Learning from unlabeled data via pretext tasks |
| | `contrastive-learning` | Representation learning by pulling / pushing sample pairs |
| | `knowledge-distillation` | Transferring knowledge from a teacher to a student model |
| | `domain-adaptation` | Transferring across distribution shift / domains |
| | `continual-learning` | Learning new tasks without catastrophic forgetting |
| | `imitation-learning` | Learning policies from demonstrations (behavior cloning) |
| | `fine-tuning` | Adapting a pretrained model to a task / domain |
| | `chain-of-thought` | Step-by-step intermediate reasoning traces |
| | `RLHF` | Reinforcement learning from human (or AI) feedback |
| | `meta-learning` | Learning to learn / fast adaptation across tasks |
| | `curriculum-learning` | Ordering training data / tasks easy-to-hard |
| | `in-context-learning` | Task adaptation from prompt examples, no weight update |
| | `self-play` | Improving by competing / cooperating with copies of oneself |
| | `flow-matching` | Continuous-time generative training via velocity fields |
| | `model-merging` | Combining multiple models' weights into one |
| | `retrieval` | Retrieval-augmented generation (RAG) and retrieval / memory systems that fetch external context |
| | `sim-to-real` | Simulation-to-real transfer (domain randomization, real-to-sim, etc.) |
| | `optimal-control` | Model-based control via optimization — MPC, trajectory optimization, sampling-based / receding-horizon control, LQR; solves for actions by optimization rather than a learned policy (distinguishes control-theory papers from learning ones) |
| **Training/Scaling** | `pre-training` | Large-scale training of a foundation model from scratch |
| | `scaling` | Scaling laws / behavior of compute, data, or model size |
| | `synthetic-data` | Training on generated or simulated data |
| | `parameter-efficient` | Low-cost adaptation (LoRA, adapters, prompt tuning) |
| | `test-time-scaling` | Spending more compute at inference (search, sampling, longer reasoning) |
| **Applications** | `robotics` | Physical robot control and manipulation systems |
| | `autonomous-driving` | Self-driving perception, prediction, and planning |
| | `embodied-AI` | Agents acting in simulated or real physical environments |
| | `agentic-AI` | Autonomous LLM agents with tools, memory, and multi-step plans |
| | `code-generation` | Generating or reasoning about source code |
| | `medical-imaging` | Medical / clinical image analysis |
| | `humanoid` | Humanoid / whole-body / bipedal robot platforms |
| | `locomotion` | Legged / quadruped / bipedal locomotion, gait, and agile-skill control (the moving-the-body problem, vs. `humanoid` = platform) |
| | `dexterous` | Multi-finger / dexterous manipulation (vs. parallel-jaw) |
| | `human-robot-interaction` | Human-robot interaction, teleoperation, shared autonomy, assistive / collaborative robotics |
| | `multi-agent` | Multiple interacting agents or robots — coordination, cooperation, swarms, decentralized control (vs. `agentic-AI` = single agent) |
| **Tasks/Capabilities** | `reasoning` | Multi-step logical / mathematical / commonsense inference |
| | `spatial-reasoning` | Reasoning about spatial relations and layout |
| | `visual-grounding` | Linking language to image regions / objects |
| | `planning` | Producing action sequences toward a goal |
| | `object-detection` | Localizing and classifying objects |
| | `segmentation` | Pixel-level region / instance labeling |
| | `3D-understanding` | 3D geometry, scenes, reconstruction, and pose |
| | `neural-rendering` | NeRF / 3D Gaussian Splatting / radiance fields / novel-view synthesis (scene representation & rendering, vs. `3D-understanding` = geometry analysis) |
| | `state-estimation` | SLAM, localization, odometry, visual-inertial / Kalman / observer-based estimation of pose and state |
| | `video-understanding` | Temporal understanding of video |
| | `image-generation` | Synthesizing images |
| | `video-generation` | Synthesizing video — text-to-video, image-to-video, video diffusion (vs. `image-generation` = stills) |
| | `navigation` | Moving an agent to goals through environments |
| | `manipulation` | Grasping and manipulating objects |
| | `tool-use` | Invoking external tools / APIs / functions |
| | `tactile` | Touch / force / haptic sensing (GelSight, DIGIT, visuo-tactile) |
| | `egocentric` | First-person / hand-cam / Ego4D-style data and pretraining |
| **Properties/Concerns** | `hallucination` | Fabricated / ungrounded model outputs |
| | `efficiency` | Compute / memory / latency efficiency |
| | `interpretability` | Understanding model internals / behavior |
| | `robustness` | Resistance to perturbations, OOD, and adversarial inputs |
| | `uncertainty-estimation` | Uncertainty quantification, calibration, conformal prediction, predictive confidence |
| | `safety` | Alignment, harm avoidance, and safe deployment |
| | `physics-aware` | Grounds models in physical priors / Newtonian / commonsense physics |
| **Paper Type** | `survey` | Literature review / taxonomy of a research area |
| | `benchmark` | Primary contribution is an evaluation protocol / suite |
| | `dataset` | Primary contribution is a data corpus / collection for training (vs. `benchmark` = eval protocol; a paper can carry both) |

#### Validate & format-QA the Detailed Reports

`extract_summaries.py` auto-formats every new report via `format_reports.py::format_report` (heading hierarchy + numbering, boilerplate/figure/`[N]`-citation removal, in-KH citation wikilinks, mangled-math rejoin, punctuation — see that file's docstrings for the full pipeline). It deliberately does **not** force canonical section titles, merge near-duplicate sections, or touch `**bold**`/`*italic*` emphasis. Still, the raw alphaxiv render is inconsistent enough that some cases slip through — so validate + repair on **every** ingest (single or batch), scoped to the notes just written.

1. **Deterministic validate** — the single source of truth for the format rules:
   ```bash
   .venv/bin/python .claude/skills/alphaxiv-summary-extract/scripts/validate_reports.py
   ```
   A clean run is `FAIL 0`; it lists each failing note + reason (`check()` is self-documenting).
2. **Validate-driven repair** — for flagged notes, drive headless `claude -p --permission-mode acceptEdits` subagents (≈8–12 notes/batch, `sonnet`; escalate to `opus` only if quotes reveal hallucinated fixes) to READ and fix, each flag **quoting the exact offending line verbatim**. Also wikilink any in-KH citations flagged as unlinked. **Never blanket-join consecutive lines** (legit label→paragraph / equation-on-its-own-line get corrupted); `git checkout -- <file>` restores if a bulk edit goes wrong.
3. **Semantic format-QA** — dispatch `claude -p --model sonnet` subagents over the new notes for what the regex validator can't catch: sub-sections mis-leveled as `### N` instead of `#### N.M`, non-sequential numbering, a whole report nested under a title wrapper, glued words (`model.The`). Fix **formatting only**; never reword content.
4. **Re-validate** — confirm `FAIL 0`. Necessary but not sufficient: also read a random sample. Regex under-counts judgement cases (truncated source, a subtly-wrong title, odd-reading prose) — every "check again" pass this vault went through surfaced a pattern only reading caught.

#### Report results

- **Processed**: N new notes written to `_KnowledgeHub_/`
- **Skipped**: N papers already have a note
- **Failed**: list any paper URLs that errored

#### Alias dedup check

After enrichment, verify each new alias is unique across the vault. For each newly-set alias, invoke `Skill(skill="obsidian:obsidian-cli")` to search for other notes using the same alias. List all collisions in chat (the user needs to know which notes collide to decide who renames). Accept the collision only if the papers are genuinely related variants (e.g., `DreamerV3` vs `DreamerV3-XL`); otherwise rename one.

#### Refresh graph

If extraction wrote at least one new note, invoke `Skill(skill="kh-graph-sync")` — it additively adds just the new notes to `graphify-out/graph.json`. **Do not run `graphify --update` on this vault:** bulk note edits invalidate its content-addressed cache (→ full multi-hour re-extract) and its generic merge corrupts existing nodes; `kh-graph-sync` bypasses both.

## Refreshing BibTeX (optional, on demand)

To update BibTeX blocks in existing notes with the latest data from arXiv:

```bash
.venv/bin/python .claude/skills/alphaxiv-summary-extract/scripts/refresh_bibtex.py \
  --notes-dir _KnowledgeHub_
```

To refresh specific papers only:

```bash
.venv/bin/python .claude/skills/alphaxiv-summary-extract/scripts/refresh_bibtex.py \
  --notes-dir _KnowledgeHub_ \
  --ids 2602.15922 2601.16163
```

## Papers with no full text reachable (rare failures)

Generation fails a paper only when `mcp__alphaxiv__get_paper_content` genuinely can't return text for that ID (withdrawn paper, bad ID) — it reads straight from arxiv's own PDF/HTML, not from any alphaxiv-side generated state, so **the five short fields never need a rescue mode**. A withdrawn paper (arxiv itself 404s) should be skipped, not retried — see Mode B's "Failure handling" above for what `generate_summary()` failures look like and how to retry.

Every note's five short fields must be sourced from the paper's own full text: do **not** fabricate content when the fetch fails. If `get_paper_content` can't return text, leave the paper **un-ingested** — a missing note beats a fabricated one.

**The Detailed Report is a separate, real gap, non-fatal to the note** (written without that section) — see the rescue section right after this one.

## Papers with no pre-generated alphaxiv overview (rescue for the Detailed Report only)

Persistent Detailed Report fetch failures (`fetch_research_report` returns `""`, note ends up missing `## Detailed Report`) mean that specific paper has **no pre-generated overview** on alphaxiv — `alphaxiv.org/overview/{ID}` shows a *"Generate Overview"* button. This is **not** transient or rate-limiting; re-fetching alone won't fix it. Generation is **server-side and per-paper** (not per-browser): once an overview exists, any later fetch — including a plain unauthenticated `curl` to the `.md` endpoint — can read it. So the rescue is to trigger generation once, then patch the Detailed Report into the existing note (no note regeneration, no re-running the five-field synthesis).

### `generate_overviews.py --missing-reports` (primary use case now)

Targets every KH note currently lacking `## Detailed Report` — exactly `validate_reports.py`'s "NO '## Detailed Report' section" failure signature — drives a cmux browser surface through each one, clicks *"Generate Overview"*, waits for it to fully render, then **patches the Detailed Report directly into the existing note** (`patch_detailed_report`, appends after existing content — never touches the five fields already there):

```bash
.venv/bin/python .claude/skills/alphaxiv-summary-extract/scripts/generate_overviews.py --missing-reports
```

Also supports `--ids`/`--ids-file` (explicit targets) and `--pending` (every `knowledge.py` ID with no KH note at all — a pre-warming pass, though most fresh papers already succeed on first fetch without it).

It opens a **visible** surface by default (`--focus true`, via `--no-visible` to suppress) so a human can watch it work, reuses that one surface (navigating in place), retries the probe on warm-up, detects withdrawn/404 pages, and caps each paper at `--timeout` seconds so one stuck page can't hang the loop.

Four gotchas the script encodes — they cost real debugging time, so respect them when invoking or adapting it:

- **Never `nohup ... &` it.** Detaching from the TTY breaks cmux's socket `eval` (returns empty → every paper silently skipped, nothing generated). Run it in the **foreground**, or via a harness-managed background runner that keeps the cmux socket alive (Claude Code's `run_in_background`). The tell-tale is `[probe empty]` on every paper.
- **Completion = a "Table of Contents" heading + a large body (~>5000 chars).** Don't poll for the word *"generating"* — it false-positives on section headings (e.g. *"Generating Obstacle-Aware Trajectory Supervision"*).
- **The first probe after navigation is often empty** (browser warm-up); one empty read is not a failure, so the script retries before giving up.
- **Each paper takes ~30–120 s** to generate, so a large failed batch runs for a while — that's inherent (you're waiting on alphaxiv's server), not a bug.

Same rule as the five fields, applied to this one section: never fabricate a Detailed Report from the arxiv abstract/HTML/PDF as a substitute. If an overview still cannot be generated, leave that note without one. A `404` on `/abs/{ID}.md` (or an `err` page in the generator) means the paper is withdrawn — skip it.

## Notes

- The script skips papers whose `{ID}.md` already exists — safe to interrupt and resume
- Title is fetched from arxiv's own abstract page (`retrieve.extract_title`) — independent of alphaxiv, unaffected by any of its redesigns
- BibTeX is fetched from `https://arxiv.org/bibtex/{ID}` during note generation
- The **`## Detailed Report`** section sits **outside** the `%%` BibTeX block so it renders in preview — see "Validate & format-QA the Detailed Reports" above for how it's fetched, formatted, and checked
- `authors`, `tags`, and `aliases` in frontmatter start empty (`[]`) — the post-processing enrichment step fills them in
- `authors` must never contain `- ...` as a placeholder — use real names only, or omit the field
- `aliases` must never remain `[]` — always derive at least one alias from the title or paper content
- `authors` and `aliases` values must always be double-quoted in YAML (e.g., `- "Author Name"`, `- "ModelName"`)
- `tags` must NOT be quoted — use plain values (e.g., `- robotics`, NOT `- "robotics"`)
- Use the Edit tool + `Skill(skill="obsidian:obsidian-markdown")` for enrichment — do not write custom Python scripts for frontmatter changes
