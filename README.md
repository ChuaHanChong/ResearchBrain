# ResearchBrain

An Obsidian vault powered by Claude Code for AI research paper analysis. It automates paper ingestion, generates structured summaries, creates visual diagrams, and organizes 1,761 papers into a navigable knowledge graph.

## What It Does

```
arxiv paper ID
  → fetch summary from alphaxiv.org
  → extract structured notes (Problem/Method/Results/Takeaways)
  → enrich with authors, tags, highlights
  → assign to topic overview
  → (optional) generate Excalidraw diagram
```

## Vault Structure

```
ResearchBrain/
├── _KnowledgeHub_/          # 1,761 paper notes ({arxiv_ID}.md)
├── General/                  # 12 topic overviews with evolution graphs
│   ├── 00_Index.md
│   ├── 01_Foundation-Models.md
│   ├── 02_Vision-Language-Models.md
│   ├── 03_Reasoning-and-Planning.md
│   ├── 04_Reinforcement-Learning.md
│   ├── 05_Computer-Vision-and-3D.md
│   ├── 06_Video-and-Temporal.md
│   ├── 07_Robotics-and-Embodied-AI.md
│   ├── 08_Benchmarks-and-Surveys.md
│   ├── 09_Multimodal-LLMs.md
│   ├── 10_Agents-and-Tool-Use.md
│   ├── 11_Self-Evolving-AI.md
│   ├── 12_Diffusion-and-Generation.md
│   └── scripts/              # Paper assignment & listing generation
├── _Projects_/               # Research project planning
├── _Artefacts_/              # Excalidraw diagrams & PNGs (gitignored)
└── .claude/                  # Claude Code agents, skills, config
```

## Paper Note Format

Each `_KnowledgeHub_/{ID}.md` note follows a consistent template:

```yaml
---
title: "Paper Title"
authors: [First Author, ...]
tags: [topic-1, topic-2]
aliases: [ModelName]
---
```

- **Summary** — one-paragraph overview
- **Problem** — what was unsolved
- **Method** — how they solved it (`==technical terms==` highlighted, `**ModelName**` bolded)
- **Results** — key metrics (`**X%**` bolded)
- **Takeaways** — key insights
- **BibTeX** — citation block (hidden in Obsidian reading view)

## Topic Overviews

Each `General/` file provides:
- Curated narrative with landmark papers and Mermaid evolution graphs
- Complete paper listing — every KnowledgeHub paper appears in exactly one topic
- Cross-references to related topics and deep-dive folders

## Claude Code Integration

### Skills

| Skill | Trigger | What It Does |
|-------|---------|--------------|
| `alphaxiv-summary-extract` | "update knowledge hub" | Batch-scrape papers from alphaxiv.org into notes |
| `alphaxiv-paper-lookup` | Share an arxiv URL/ID | Fetch and explain a single paper |
| `knowledgehub-query` | Reference paper IDs | Answer questions from existing notes |
| `excalidraw` | "diagram this" | Generate visual Excalidraw diagrams |

### Agents

| Agent | Purpose |
|-------|---------|
| `paper-visual-explainer` | Extract visual dimensions from papers and create diagrams |

## Quick Start

### Prerequisites

- [Obsidian](https://obsidian.md/) (for viewing the vault)
- [Claude Code](https://claude.ai/code) (for automation)
- Python 3.13+ via [uv](https://github.com/astral-sh/uv)
- Chrome + ChromeDriver (for alphaxiv scraping)

### Add Papers

```bash
# Single paper
# Just share the arxiv URL in Claude Code — the skill handles the rest

# Batch update (from knowledge.py paper list)
python .claude/skills/alphaxiv-summary-extract/scripts/run.py \
  --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py \
  --out _KnowledgeHub_

# Regenerate General/ topic listings after adding papers
python General/scripts/assign_papers.py
python General/scripts/generate_listings.py
```

### Generate Diagrams

```bash
# First-time setup
cd .claude/skills/excalidraw/references && uv sync && uv run playwright install chromium

# Render a diagram to PNG
cd .claude/skills/excalidraw/references && uv run python render_excalidraw.py /path/to/file.excalidraw
```

## Stats

- **1,761** paper notes in KnowledgeHub
- **12** topic overview files in General/
- Papers spanning **2016–2026** across RL, VLMs, robotics, diffusion, and more

## License

This is a personal research vault. Paper summaries are derived from [alphaxiv.org](https://alphaxiv.org). BibTeX entries are from [arXiv](https://arxiv.org).
