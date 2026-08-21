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
| **alphaxiv-search skill** | `.claude/skills/alphaxiv-search/` | Search guide for 4 alphaxiv MCP research tools with query patterns and strategies |
| **alphaxiv-summary-extract skill** | `.claude/skills/alphaxiv-summary-extract/` | `extract_summaries.py` self-generates Summary/Problem/Method/Results/Takeaways (shells out to `claude -p` per paper → MCP `get_paper_content(fullText=true)`) + alphaxiv-scraped Detailed Report → `_KnowledgeHub_/` notes, enrichment rules, tag taxonomy |
| **knowledgehub-query skill** | `.claude/skills/knowledgehub-query/` | Reads KnowledgeHub notes by arxiv ID and answers questions from their content |
| **paper-curate skill** | `.claude/skills/paper-curate/` | Assigns papers to General/ topics, audits coverage, formatting rules |
| **paper-figure-extract skill** | `.claude/skills/paper-figure-extract/` | Extracts a paper's pipeline figure from its **alphaxiv overview** (alphaxiv alt-label + caption), or its **arxiv HTML render** as a fallback, requires a visual check that it is the real diagram, and embeds it (caption verbatim) under the KH note's `## Method` section |
| **kh-graph-sync skill** | `.claude/skills/kh-graph-sync/` | Additively adds new KH notes to `graphify-out/graph.json` (delta → subagent extract → additive merge + `tag_*` wiring); `enrich` subcommand adds TF-IDF similarity + `concept_*` hub edges. Bypasses graphify's broken native `--update` |
| **alphaxiv MCP** | External service | 4 research tools: `discover_papers` (unified keyword+embedding+multi-round search), paper content, PDF Q&A, GitHub reader. Plus 6 library-management tools (out of scope here) |

`.claude/settings.json` names **research-assistant** as the vault's main agent, so every session opens in it. The ml-optimizer submodule serves it: `/optimize` runs the optimization pipeline, and its Phase 5 routes research back to research-assistant so proposals come from the curated vault rather than a cold web search.

### Slash Commands

| Command | Purpose |
|---------|---------|
| `/kh-sync` | Sync `_KnowledgeHub_/` + `General/` with `knowledge.py` — one `extract_summaries.py` call generates the five short fields (self-contained, `claude -p` per paper) and assembles notes (Detailed Report still alphaxiv-scraped), rescue any missing Detailed Reports via cmux, enrich, validate + subagent format-QA the Detailed Reports, curate, then refresh the concept graph via the **kh-graph-sync skill** |
| `/deepdive-sync` | Sync `Embodied-AI/NN_*.md` deep dives with current KH state (embeds Deep-Dive Format spec) |
| `/research-directions` | Generate or refresh a research-direction doc under `_Projects_/Research-Directions/` (embeds Format spec) |

### Vault Structure

| Folder | Purpose |
|--------|---------|
| `_KnowledgeHub_/` | Individual paper notes (`{arxiv_ID}.md`) with structured summaries |
| `General/` | Topic overview files grouping papers by theme with sub-topics, callouts, ASCII/Unicode evolution-graph diagrams |
| `Embodied-AI/` | 15 deep dives (`02`–`16`, mechanism-organized in reading order, not creation order — see the numbering convention below). **Substrate:** `02` datasets/benchmarks/sim, `03` imitation-learning & RL. **Model families & mechanisms:** `04` VLA, `05` VLA reasoning/CoT, `06` WAM, `07` JEPA/latent world models, `08` physics-aware, `09` robot memory (spatial & temporal persistence — episodic/retrieval, object-permanence, cognitive maps, progress-aware control, memory-augmented reasoning, self-evolution's memory substrate — a cross-cutting mechanism like `07`, pulled multi-home from across every block below it). **Physical capabilities:** `10` manipulation skill-learning, `11` contact-rich & tactile, `12` whole-body & locomotion, `13` navigation & mobile-manipulation. **Scaling data:** `14` egocentric pretraining. **Deployment lifecycle:** `15` sim-to-real, `16` self-evolving. (`01` is the 101 intro.) |
| `_Projects_/` | Active project `00_ResearchProposal/`; retired projects (`01_FirstPublication*`, `02_BenchmarkPipeline-WAM`, `Research-Directions-FocusDirection`) live in `__archive__/`. `Research-Directions/` holds the synthesis docs: `Embodied-AI.md` umbrella, plus `Mechanism/` & `Capability/` axes (3 docs each) with `__ELI5__/` + `__TLDR__/` Chinese derived versions |
| `data/papers/` | Local PDF files for papers (downloaded on demand with version suffix, e.g., `2602.15922v2.pdf`) |
| `data/.repositories/` | Local code repositories for referenced papers (cloned on demand; hidden folder so Obsidian ignores it) |
| `ml-optimizer/` | Git submodule — the ML-optimization plugin, registered as a local-scope marketplace so edits are live. Excluded from Obsidian's file index. Entry point `/optimize`; see its `.claude/CLAUDE.md` |
| `graphify-out/` | Graphify pilot artifacts: `graph.json`, `GRAPH_REPORT.md`, viz cache (gitignored except the report) |
| `docs/` | Long-form notes that don't belong in `_KnowledgeHub_/`, `General/`, or `Embodied-AI/` |

**`Embodied-AI/` numbering convention:** deep-dive prefixes follow reading order within the block taxonomy above, not creation order. A new file's number is chosen by where it belongs in that taxonomy — inserting one may require renumbering later files, using the reference method below. This supersedes `.claude/commands/deepdive-sync.md`'s older "next available prefix" rule for *cross-block placement*; that rule still governs ordering *within* a block (a new file joins after the last file already in its block). Reference renumber procedure: `git mv` every affected file to a temp name first (avoids mid-rotation collisions), then to final names; one single-pass, dict-based regex substitution across every `.md` file in the vault (never sequential per-target passes, which double-substitute); reorder `00_Table-of-Contents.md`'s physical row order to match; update this table.

### alphaxiv API Notes

- The five short fields (Summary/Problem/Method/Results/Takeaways) are synthesized by `extract_summaries.py` itself, which shells out to a headless `claude -p` subprocess per paper to call `mcp__alphaxiv__get_paper_content(fullText=true)` — the paper's own full text. See the `alphaxiv-summary-extract` skill.
- Overview page: `https://www.alphaxiv.org/overview/{PAPER_ID}` — the `.md` suffix (machine-readable render) is still fetched directly for the note's `## Detailed Report`, unaffected by the tab-UI redesign above
- Domain redirects from `alphaxiv.org` → `www.alphaxiv.org` (use `-L` if probing with curl)
- MCP tools: `discover_papers`, `get_paper_content`, `answer_pdf_queries`, `read_files_from_github_repository`

## Environment

- **Python**: 3.13+ (managed via `uv`)
- **Package manager**: `uv` (Rust-based, see `uv.lock`)
- **Key deps**: `beautifulsoup4`, `requests`, `anthropic`, `tqdm`, `claude` CLI on PATH (for `extract_summaries.py`'s `claude -p` subprocess)
- **Virtual env**: `.venv/` (gitignored)

## Conventions

- Never commit to git without explicit user instruction
- KH enrichment rules (authors, tags, aliases, formatting) are in the `alphaxiv-summary-extract` skill
- General/ formatting rules (wikilinks, sorting, callouts) are in the `paper-curate` skill
- Use Edit tool + obsidian-markdown skill for KH enrichment, not custom Python scripts
- Download arxiv PDFs with `curl -fLJO --create-dirs --output-dir data/papers "https://arxiv.org/pdf/{ID}"` — the version suffix comes from arxiv's `Content-Disposition` filename (e.g., `2412.02818v4.pdf`); one file per paper.
- Right after `ExitPlanMode` is approved, render the plan file to `docs/visuals/plan-{YYYY-MM-DD}-{slug}.html`, date = today, slug from its H1, with the **visualize** skill, Implementation-plan form: phases collapsed, click to expand, one inline SVG of the phase sequence.

## Deep-Dive Format (`Embodied-AI/`)

The canonical format spec lives in `.claude/commands/deepdive-sync.md` (the sync/maintenance slash command), under its `## Format reference (canonical)` section. That file is the single source of truth — it embeds the format so the `/deepdive-sync` workflow is self-contained.

Covered there: frontmatter (3 fields: title, tags, aliases), H2 spine (`[!abstract]` Overview → `## Evolution Graph` → `## Part A/B/C` → `## Quick-Reference Matrix` → `## Cross-References`), 6-layer per-section pattern (L1 framing prose → L2 `#### N.N` sub-sections → L3 bullet-per-paper → L4 Decision Matrix → L5 `[!star]` Key Papers → L6 `[!tip]` Strategic), per-section template (the heart) with Open Problems variant, anti-pattern table (A bold mini-headers / B paper-listings / C prose paragraphs / D unbolded wikilinks / E residual placeholders / F whole-file cross-links / G bracket-wrapped L4 / H over-long bullets / Seq sequence drift), connective-tissue conventions (filename, wikilink syntax, callouts, dates).

## Research-Direction Document Format (`_Projects_/Research-Directions/`)

The canonical format spec lives in `.claude/commands/research-directions.md` (the doc-generation slash command), under its `## Format reference (canonical)` section. That file is the single source of truth — it embeds the format so the `/research-directions` workflow is self-contained.

Covered there: frontmatter (3 fields: title, aliases, tags), H2 spine (`[!abstract]` Overview callout → Methodology → Survey Landscape → Formal Framing → Cluster Overview → Cluster A/B/C → Cross-Cutting Themes (each as `[!tip]` callout) → Benchmark Gaps → Cross-References), per-direction card (4-row card → Why it matters → First-principles framing → Evidence → Concrete research questions → Related research papers → Benchmarks & metrics → `[!warning]` Risks), thesis sentence template (integrated taste + first-principles + novelty in one sentence), first-principles framing rubric (3-bullet litmus test: First principle / Assumption challenged / The bet), connective-tissue conventions.
