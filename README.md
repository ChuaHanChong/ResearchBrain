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
├── _KnowledgeHub_/          # Paper notes ({arxiv_ID}.md)
├── _Projects_/               # Research projects, blueprints, code repos
├── General/                  # Topic overviews with evolution graphs
├── Embodied-AI/              # Deep-dive notes on VLA, WAM, JEPA, self-evolving
├── data/papers/              # Local PDFs (downloaded on demand)
├── data/repo/                # Local code repos (cloned on demand)
├── graphify-out/             # Graphify pilot artifacts (gitignored except report)
└── .claude/                  # Agent, skills, config
    ├── agents/
    │   └── research-assistant.md
    └── skills/
        ├── alphaxiv-search/
        ├── alphaxiv-summary-extract/
        ├── knowledgehub-query/
        ├── paper-curate/
        └── paper-figure-extract/
```

## Agent & Skills

| Component | Purpose |
|-----------|---------|
| **research-assistant** agent | Full-stack research: discovery, idea formulation, math verification, synthesis, documentation |
| **alphaxiv-search** skill | Search guide for alphaxiv MCP tools with query patterns and strategies |
| **alphaxiv-summary-extract** skill | Batch-scrape papers into KnowledgeHub notes with enrichment |
| **knowledgehub-query** skill | Read and synthesize from existing paper notes |
| **paper-curate** skill | Assign papers to General/ topics, audit coverage |
| **paper-figure-extract** skill | Download a paper's figure from ar5iv and embed it under the KH note's `## Method` section |

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
