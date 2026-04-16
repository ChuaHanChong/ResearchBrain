# Research Brain

An Obsidian vault augmented with Claude Code agents and skills for **full-stack AI research** — from literature discovery and paper synthesis to idea formulation, mathematical verification, and research documentation.

## Architecture

### Research Flow

```
General/ (topic overview, landscape, key papers)
  → _KnowledgeHub_/ (paper details: Problem/Method/Results)
    → alphaxiv MCP (full paper content, PDF Q&A, math understanding)
      → Code & PDFs (local repos, GitHub reader, paper PDFs)
```

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| **research-assistant agent** | `.claude/agents/research-assistant.md` | Full-stack research: discovery, idea formulation, math verification, synthesis, documentation, vault maintenance |
| **alphaxiv-search skill** | `.claude/skills/alphaxiv-search/` | Search guide for 6 alphaxiv MCP tools with query patterns and strategies |
| **alphaxiv-summary-extract skill** | `.claude/skills/alphaxiv-summary-extract/` | Batch scraping via Selenium → `_KnowledgeHub_/` notes, enrichment rules, tag taxonomy |
| **knowledgehub-query skill** | `.claude/skills/knowledgehub-query/` | Reads KnowledgeHub notes by arxiv ID and answers questions from their content |
| **paper-curate skill** | `.claude/skills/paper-curate/` | Assigns papers to General/ topics, audits coverage, formatting rules |
| **alphaxiv MCP** | External service | 6 tools: semantic search, full-text search, agentic retrieval, paper content, PDF Q&A, GitHub reader |

### Vault Structure

| Folder | Purpose |
|--------|---------|
| `_KnowledgeHub_/` | Individual paper notes (`{arxiv_ID}.md`) with structured summaries |
| `General/` | Topic overview files grouping papers by theme with sub-topics, callouts, mermaid graphs |
| `Embodied-AI/` | Deep-dive notes on VLAs, WAMs, JEPA/latent world models, self-evolving embodied AI |
| `_Projects_/` | Research projects; `01_FirstPublication/` has blueprint, roadmap, math formulations + code repos in `repo/` |
| `data/papers/` | Local PDF files for papers (downloaded on demand with version suffix, e.g., `2602.15922v2.pdf`) |
| `data/repo/` | Local code repositories for referenced papers (cloned on demand) |

### alphaxiv API Notes

- Endpoints redirect from `alphaxiv.org` to `www.alphaxiv.org` — always use `-L` flag with curl
- Primary endpoint: `https://www.alphaxiv.org/overview/{PAPER_ID}.md` (machine-readable)
- Fallback: `https://www.alphaxiv.org/abs/{PAPER_ID}.md` (full extracted text)
- MCP tools: `embedding_similarity_search`, `full_text_papers_search`, `agentic_paper_retrieval`, `get_paper_content`, `answer_pdf_queries`, `read_files_from_github_repository`

## Environment

- **Python**: 3.13+ (managed via `uv`)
- **Package manager**: `uv` (Rust-based, see `uv.lock`)
- **Key deps**: `selenium`, `beautifulsoup4`, `anthropic`
- **Virtual env**: `.venv/` (gitignored)

## Conventions

- Never commit to git without explicit user instruction
- KH enrichment rules (authors, tags, aliases, formatting) are in the `alphaxiv-summary-extract` skill
- General/ formatting rules (wikilinks, sorting, callouts) are in the `paper-curate` skill
- Use Edit tool + obsidian-markdown skill for KH enrichment, not custom Python scripts
- Download papers with version suffix via Playwright (preferred) or curl (fallback)
