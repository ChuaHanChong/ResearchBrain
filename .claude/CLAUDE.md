# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ResearchBrain is an Obsidian vault augmented with Claude Code agents and skills for **visual explanation of AI research papers**. It combines alphaxiv.org paper summaries with Excalidraw diagrams to help researchers quickly understand and compare papers.

## Key Commands

```bash
# Render an Excalidraw diagram to PNG (requires Playwright)
cd .claude/skills/excalidraw/references && uv run python render_excalidraw.py /path/to/file.excalidraw

# Batch-process papers into KnowledgeHub
python .claude/skills/alphaxiv-summary-extract/scripts/run.py --input .claude/skills/alphaxiv-summary-extract/scripts/knowledge.py --output KnowledgeHub.json

# Limit batch processing for testing
python .claude/skills/alphaxiv-summary-extract/scripts/run.py --input ... --output ... --limit 3

# Install Playwright browser (first-time setup)
cd .claude/skills/excalidraw/references && uv sync && uv run playwright install chromium
```

## Architecture

### Data Flow

```
arxiv paper ID
  → alphaxiv-paper-lookup skill (fetches summary via WebFetch)
  → paper-visual-explainer agent (extracts 7 visual dimensions)
  → excalidraw skill (generates diagram JSON)
  → render_excalidraw.py (PNG output via Playwright)
  → Artefacts/{PAPER_ID}.excalidraw + .png
```

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| **paper-visual-explainer agent** | `.claude/agents/paper-visual-explainer.md` | Main agent with 3 modes: single paper (A), comparison (B), update (C) |
| **alphaxiv-paper-lookup skill** | `.claude/skills/alphaxiv-paper-lookup/` | Fetches paper summaries from `alphaxiv.org/overview/{ID}.md` |
| **alphaxiv-summary-extract skill** | `.claude/skills/alphaxiv-summary-extract/` | Batch scraping via Selenium → KnowledgeHub.json |
| **excalidraw skill** | `.claude/skills/excalidraw/` | Diagram creation with color palette, element templates, and rendering |
| **KnowledgeHub.json** | Root | Database of ~200 papers with Problem/Method/Results/Takeaways |

### Naming Conventions

- Individual diagrams: `Artefacts/{PAPER_ID}.excalidraw` (e.g., `2602.15922.excalidraw`)
- Comparison diagrams: `Artefacts/compare-{ID1}-{ID2}-[...].excalidraw`
- PNG renders: Same filename with `.png` extension

### alphaxiv API Notes

- Endpoints redirect from `alphaxiv.org` to `www.alphaxiv.org` — always use `-L` flag with curl
- Primary endpoint: `https://www.alphaxiv.org/overview/{PAPER_ID}.md` (machine-readable)
- Fallback: `https://www.alphaxiv.org/abs/{PAPER_ID}.md` (full extracted text)

## Environment

- **Python**: 3.13+ (managed via `uv`)
- **Package manager**: `uv` (Rust-based, see `uv.lock`)
- **Key deps**: `selenium`, `beautifulsoup4`, `playwright`, `anthropic`
- **Virtual env**: `.venv/` (gitignored)

## Conventions

- Never commit to git without explicit user instruction
- Artefacts directory is gitignored — diagrams are local output only
- The excalidraw skill has its own color palette (`references/color-palette.md`) and element templates (`references/element-templates.md`) — always reference these when creating diagrams
