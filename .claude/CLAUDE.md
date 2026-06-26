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
| **paper-figure-extract skill** | `.claude/skills/paper-figure-extract/` | Extracts a paper's pipeline figure from its **alphaxiv overview** (alphaxiv alt-label + caption), or its **arxiv HTML render** as a fallback, requires a visual check that it is the real diagram, and embeds it (caption verbatim) under the KH note's `## Method` section |
| **kh-graph-sync skill** | `.claude/skills/kh-graph-sync/` | Additively adds new KH notes to `graphify-out/graph.json` (delta → subagent extract → additive merge + `tag_*` wiring); `enrich` subcommand adds TF-IDF similarity + `concept_*` hub edges. Bypasses graphify's broken native `--update` |
| **alphaxiv MCP** | External service | 6 tools: semantic search, full-text search, agentic retrieval, paper content, PDF Q&A, GitHub reader |

### Slash Commands

| Command | Purpose |
|---------|---------|
| `/kh-sync` | Sync `_KnowledgeHub_/` + `General/` with `knowledge.py` — scrape, enrich, rescue chromedriver failures via cmux, curate, then refresh the concept graph via the **kh-graph-sync skill** |
| `/deepdive-sync` | Sync `Embodied-AI/NN_*.md` deep dives with current KH state (embeds Deep-Dive Format spec) |
| `/research-directions` | Generate or refresh a research-direction doc under `_Projects_/Research-Directions/` (embeds Format spec) |

### Vault Structure

| Folder | Purpose |
|--------|---------|
| `_KnowledgeHub_/` | Individual paper notes (`{arxiv_ID}.md`) with structured summaries |
| `General/` | Topic overview files grouping papers by theme with sub-topics, callouts, mermaid graphs |
| `Embodied-AI/` | 14 deep dives (`02`–`15`, mechanism-organized in five blocks). **Substrate:** `02` datasets/benchmarks/sim, `03` imitation-learning & RL. **Model families:** `04` VLA, `05` VLA reasoning/CoT, `06` WAM, `07` JEPA/latent world models, `08` physics-aware. **Physical capabilities:** `09` manipulation skill-learning, `10` contact-rich & tactile, `11` whole-body & locomotion, `12` navigation & mobile-manipulation. **Scaling data:** `13` egocentric pretraining. **Deployment lifecycle:** `14` sim-to-real, `15` self-evolving. (`01` is the 101 intro.) |
| `_Projects_/` | Active project `00_ResearchProposal/`; retired projects (`01_FirstPublication*`, `02_BenchmarkPipeline-WAM`) live in `__archive__/`. `Research-Directions/` holds the synthesis docs: `Embodied-AI.md` umbrella + `Focus-Direction.md`, plus `Mechanism/` & `Capability/` axes (3 docs each) with `__ELI5__/` + `__TLDR__/` Chinese derived versions |
| `data/papers/` | Local PDF files for papers (downloaded on demand with version suffix, e.g., `2602.15922v2.pdf`) |
| `data/.repositories/` | Local code repositories for referenced papers (cloned on demand; hidden folder so Obsidian ignores it) |
| `graphify-out/` | Graphify pilot artifacts: `graph.json`, `GRAPH_REPORT.md`, viz cache (gitignored except the report) |
| `docs/` | Long-form notes that don't belong in `_KnowledgeHub_/`, `General/`, or `Embodied-AI/` |

### alphaxiv API Notes

- Overview page: `https://www.alphaxiv.org/overview/{PAPER_ID}` — JS-rendered HTML, scraped via Selenium + BeautifulSoup in `alphaxiv-summary-extract/scripts/run.py`
- Domain redirects from `alphaxiv.org` → `www.alphaxiv.org` (use `-L` if probing with curl)
- The `.md` suffix endpoint exists (machine-readable render) but is **not used** — static render misses JS-loaded sections this vault needs
- MCP tools (preferred over scraping when possible): `embedding_similarity_search`, `full_text_papers_search`, `agentic_paper_retrieval`, `get_paper_content`, `answer_pdf_queries`, `read_files_from_github_repository`

## Environment

- **Python**: 3.13+ (managed via `uv`)
- **Package manager**: `uv` (Rust-based, see `uv.lock`)
- **Key deps**: `selenium`, `beautifulsoup4`, `requests`, `anthropic`, `tqdm`
- **Virtual env**: `.venv/` (gitignored)

## Conventions

- Never commit to git without explicit user instruction
- KH enrichment rules (authors, tags, aliases, formatting) are in the `alphaxiv-summary-extract` skill
- General/ formatting rules (wikilinks, sorting, callouts) are in the `paper-curate` skill
- Use Edit tool + obsidian-markdown skill for KH enrichment, not custom Python scripts
- Download arxiv PDFs with `curl -fLJO --create-dirs --output-dir data/papers "https://arxiv.org/pdf/{ID}"` — the version suffix comes from arxiv's `Content-Disposition` filename (e.g., `2412.02818v4.pdf`); one file per paper. Selenium (`alphaxiv-summary-extract/scripts/run.py`) scrapes alphaxiv overview pages, not PDFs.

## Deep-Dive Format (`Embodied-AI/`)

The canonical format spec lives in `.claude/commands/deepdive-sync.md` (the sync/maintenance slash command), under its `## Format reference (canonical)` section. That file is the single source of truth — it embeds the format so the `/deepdive-sync` workflow is self-contained.

Covered there: frontmatter (3 fields: title, tags, aliases), H2 spine (`[!abstract]` Overview → `## Evolution Graph` → `## Part A/B/C` → `## Quick-Reference Matrix` → `## Cross-References`), 6-layer per-section pattern (L1 framing prose → L2 `#### N.N` sub-sections → L3 bullet-per-paper → L4 Decision Matrix → L5 `[!star]` Key Papers → L6 `[!tip]` Strategic), per-section template (the heart) with Open Problems variant, anti-pattern table (A bold mini-headers / B paper-listings / C prose paragraphs / D unbolded wikilinks / E residual placeholders / F whole-file cross-links / G bracket-wrapped L4 / H over-long bullets / Seq sequence drift), connective-tissue conventions (filename, wikilink syntax, callouts, dates).

## Research-Direction Document Format (`_Projects_/Research-Directions/`)

The canonical format spec lives in `.claude/commands/research-directions.md` (the doc-generation slash command), under its `## Format reference (canonical)` section. That file is the single source of truth — it embeds the format so the `/research-directions` workflow is self-contained.

Covered there: frontmatter (3 fields: title, aliases, tags), H2 spine (`[!abstract]` Overview callout → Methodology → Survey Landscape → Formal Framing → Cluster Overview → Cluster A/B/C → Cross-Cutting Themes (each as `[!tip]` callout) → Benchmark Gaps → Cross-References), per-direction card (4-row card → Why it matters → First-principles framing → Evidence → Concrete research questions → Related research papers → Benchmarks & metrics → `[!warning]` Risks), thesis sentence template (integrated taste + first-principles + novelty in one sentence), first-principles framing rubric (3-bullet litmus test: First principle / Assumption challenged / The bet), connective-tissue conventions.
