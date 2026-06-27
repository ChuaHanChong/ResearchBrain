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

##### Canonical Tag Taxonomy (71 tags)

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

## Papers with no pre-generated alphaxiv overview (rescue)

Persistent failures (chromedriver stack traces surviving `run.py`'s auto-retry) are papers with **no pre-generated overview** — `alphaxiv.org/overview/{ID}` shows a *"Generate Overview"* button behind a login the headless scraper can't click. This is **not** transient or rate-limiting; re-running alone won't fix it.

**Rescue: warm the backend / generate the overview, then retry — don't block.** Opening the paper's page in a real (logged-in) browser warms alphaxiv's backend so a later retry succeeds (and lets the user generate the overview on their own schedule). Open *all* failed URLs at once and keep enriching/curating the successful notes meanwhile:

```bash
cmux new-surface --type browser --url "https://www.alphaxiv.org/abs/<ID>" --focus false
```

Tell them how many surfaces opened and list the pending IDs in the run's **Failed** line. On retry, recompute pending (the still-missing `{ID}.md`) and re-scrape with `--force`.

Every note must be sourced from the alphaxiv overview: do **not** fabricate one from the arxiv abstract/HTML/PDF as a substitute. If an overview still cannot be generated, leave the paper **un-ingested** (a missing note beats a fabricated one). A `404` on `/abs/{ID}.md` means the paper is withdrawn — skip it.

## Notes

- The script skips papers whose `{ID}.md` already exists — safe to interrupt and resume
- BibTeX is fetched from `https://arxiv.org/bibtex/{ID}` during note generation
- `authors`, `tags`, and `aliases` in frontmatter start empty (`[]`) — the post-processing enrichment step fills them in
- `authors` must never contain `- ...` as a placeholder — use real names only, or omit the field
- `aliases` must never remain `[]` — always derive at least one alias from the title or paper content
- `authors` and `aliases` values must always be double-quoted in YAML (e.g., `- "Author Name"`, `- "ModelName"`)
- `tags` must NOT be quoted — use plain values (e.g., `- robotics`, NOT `- "robotics"`)
- Use the Edit tool + `Skill(skill="obsidian:obsidian-markdown")` for enrichment — do not write custom Python scripts for frontmatter changes
