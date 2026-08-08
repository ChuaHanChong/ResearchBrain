# Research Brain

An Obsidian vault powered by Claude Code for **full-stack AI research** — from literature discovery and paper synthesis to idea formulation, mathematical verification, and research documentation.

## Research Flow

```
General/ (topic overview, landscape, key papers)
  → _KnowledgeHub_/ (paper details: Problem/Method/Results)
    → alphaxiv MCP (full paper content, PDF Q&A, math understanding)
      → Code & PDFs (local repos, GitHub reader, paper PDFs)
```

## Vault Structure

```
ResearchBrain/
├── _KnowledgeHub_/           # Paper notes ({arxiv_ID}.md)
├── _Projects_/               # Research projects, blueprints, Research-Directions/
├── General/                  # Topic overviews with evolution graphs
├── Embodied-AI/              # 14 deep dives (02-15) on datasets, VLA, WAM, JEPA,
│                             #   manipulation, locomotion, sim-to-real, self-evolving
├── data/papers/              # Local PDFs (downloaded on demand)
├── data/.repositories/       # Local code repos (cloned on demand)
├── docs/                     # Long-form notes outside the three note folders
├── graphify-out/             # Graphify artifacts (gitignored except report)
├── ml-optimizer/             # Submodule: ML-optimization plugin (/optimize)
└── .claude/                  # Agent, skills, commands, config
    ├── settings.json         # Names research-assistant the vault's main agent
    ├── agents/
    │   └── research-assistant.md
    ├── commands/
    │   ├── kh-sync.md
    │   ├── deepdive-sync.md
    │   └── research-directions.md
    └── skills/
        ├── alphaxiv-search/
        ├── alphaxiv-summary-extract/
        ├── knowledgehub-query/
        ├── paper-curate/
        ├── paper-figure-extract/
        └── kh-graph-sync/
```

## Agent & Skills

| Component | Purpose |
|-----------|---------|
| **research-assistant** agent | Full-stack research: discovery, idea formulation, math verification, synthesis, documentation |
| **alphaxiv-search** skill | Search guide for alphaxiv MCP tools with query patterns and strategies |
| **alphaxiv-summary-extract** skill | Batch-scrape papers into KnowledgeHub notes with enrichment |
| **knowledgehub-query** skill | Read and synthesize from existing paper notes |
| **paper-curate** skill | Assign papers to General/ topics, audit coverage |
| **paper-figure-extract** skill | Pull a paper's pipeline figure from its alphaxiv overview (arxiv HTML render as fallback) and embed it under the KH note's `## Method` section |
| **kh-graph-sync** skill | Additively add new KH notes to `graphify-out/graph.json`, plus a TF-IDF `enrich` pass |
| **ml-optimizer** plugin | Submodule serving the agent: `/optimize` runs the ML-optimization pipeline, and its research phase reads the vault instead of cold-searching the web |

`.claude/settings.json` names research-assistant the vault's main agent, so every session opens in it.

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/kh-sync` | Scrape new papers from `knowledge.py` into `_KnowledgeHub_/`, enrich, curate into `General/`, refresh the concept graph |
| `/deepdive-sync` | Sync `Embodied-AI/NN_*.md` deep dives with current KnowledgeHub state |
| `/research-directions` | Generate or refresh a doc under `_Projects_/Research-Directions/` |
| `/optimize` | Run the ml-optimizer pipeline on an ML project |

## Paper Note Format

Each `_KnowledgeHub_/{ID}.md` note:

```yaml
---
title: "Paper Title"
authors:
  - "First Author"
  - "Second Author"
tags:
  - topic-1
  - topic-2
aliases:
  - "ModelName"
---
```

- **Summary** — one-paragraph overview
- **Problem** — what was unsolved
- **Method** — how they solved it (`==technical terms==` highlighted, `**ModelName**` bolded)
- **Results** — key metrics (`**X%**` bolded)
- **Takeaways** — key insights
- **BibTeX** — citation block

## Prerequisites

- [Obsidian](https://obsidian.md/) for viewing the vault
- [Claude Code](https://claude.ai/code) for automation
- Python 3.13+ via [uv](https://github.com/astral-sh/uv)
- Chrome + ChromeDriver for Selenium-based extraction
- [alphaxiv MCP](https://www.alphaxiv.org/docs/mcp) for paper search and retrieval

## License

Personal research vault. Paper summaries derived from [alphaxiv.org](https://alphaxiv.org). BibTeX entries from [arXiv](https://arxiv.org).
