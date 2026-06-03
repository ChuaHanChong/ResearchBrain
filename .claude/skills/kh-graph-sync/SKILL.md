---
name: kh-graph-sync
description: Refresh the graphify concept graph (graphify-out/graph.json) over _KnowledgeHub_ by additively adding only the notes missing from the graph. Use when the user says 'kh-graph-sync', 'refresh the graph', 'update the concept graph', 'sync graphify', or after a KnowledgeHub ingest. Robust to graphify's broken native --update.
---

# kh-graph-sync

Additively refresh `graphify-out/graph.json` to match `_KnowledgeHub_/` — add only the genuinely-new notes, preserve every existing node/edge. All deterministic logic lives in `scripts/kh_graph_sync.py`; the only step needing the LLM is reading the new notes (Step 2). Run everything from the project root.

> **Do NOT use `graphify --update` / `--backend claude-cli` on this vault.** Its content-addressed cache is invalidated by bulk note edits (→ full re-extract, 5+ hrs), and its generic extraction/merge corrupts the graph (parent-dir node IDs → orphans; no `tag_*` wiring; `build_merge`'s `dedup.deduplicate_entities` fuzzy-collapses existing nodes). This skill bypasses all of that.

## Recipe

```bash
PY=$(cat graphify-out/.graphify_python 2>/dev/null) || \
  { mkdir -p graphify-out; python3 -c "import sys;open('graphify-out/.graphify_python','w').write(sys.executable)"; PY=$(cat graphify-out/.graphify_python); }
SKILL=.claude/skills/kh-graph-sync/scripts/kh_graph_sync.py
```

**Step 1 — delta.** `$PY $SKILL delta` → prints `{"missing": N, "chunks": C}` and writes `.chunklist_NN.txt`. If `missing == 0`, report "graph already current" and stop.

**Step 2 — extract (the only LLM step).** Dispatch **C subagents in a single message**, `subagent_type="general-purpose"`, `model="sonnet"` (cheap, structured). Give each the prompt below with `NN` and the absolute project root `/ABS` substituted:

> graphify extraction subagent for the ResearchBrain vault. Read every file in `cat /ABS/graphify-out/.chunklist_NN.txt` (paths relative to project root). Each is a KnowledgeHub paper note: frontmatter (`id`=arxiv, `title`, `tags`, `link`) + `## Problem/Method/Results/Takeaways`. For arxiv id `X.Y` let `ARX=X_Y`. Emit ONE `{ARX}_paper` node (file_type `paper`, label=title) and 3–6 `{ARX}_{slug}` nodes (file_type `rationale`, ≤12-word labels) for key methods/datasets/benchmarks/results. Edges: each rationale→its paper as `rationale_for` (EXTRACTED 1.0); paper→`{CITED_ARX}_paper` as `cites` if the body references another arxiv id; within-chunk `semantically_similar_to` (INFERRED, score ∈ {0.95,0.85,0.75,0.65,0.55}) only for non-obvious cross-cutting links. IDs lowercase `[a-z0-9_]`, deterministic, no chunk suffixes, **no parent-dir prefix**. file_type ∈ {code,document,paper,image,rationale,concept}. source_file = path relative to root; source_url = frontmatter `link`. Write ONLY valid JSON (no fences) via the Write tool to the absolute path `/ABS/graphify-out/.graphify_chunk_NN.json` with schema `{"nodes":[...],"edges":[...],"hyperedges":[],"input_tokens":0,"output_tokens":0}`. Reply one line: `chunk NN done: X nodes, Y edges, Z papers`.

**Step 3 — finalize.** `$PY $SKILL finalize` → validates+sanitizes+merges the chunk files, additively merges into `graph.json`, wires each new note's frontmatter tags into the `tag_*` backbone, re-clusters, writes `graph.json` + `GRAPH_REPORT.md`, caches the new notes (0.8.28 format), refreshes the manifest, and prints before→after + god nodes + surprises + new-paper connectivity. Then relay that report.

**Step 4 — enrich (periodic, optional).** `$PY $SKILL enrich` → adds `semantically_similar_to` edges (TF-IDF kNN, K≤5 cos≥0.22) and `concept_*` hub nodes for named entities (GRPO, CLIP, JEPA, LIBERO…) spanning ≥3 papers, then re-clusters. Run occasionally to keep new↔old cross-links rich; not needed every add.

## Conventions (must match graph.json or new nodes orphan)

| Element | id | file_type |
|---|---|---|
| Paper | `{ARX}_paper` (label=title) | `paper` |
| Method/dataset/result | `{ARX}_{slug}` | `rationale` |
| Tag (shared backbone) | `tag_{tag_lc_underscored}` | `rationale` |
| Concept hub (enrich) | `concept_{entity_lc}` | `concept` |

Edges: `rationale_for` (concept→paper), `references` (paper→tag/concept), `cites` (paper→paper), `semantically_similar_to` (INFERRED). EXTRACTED→1.0; INFERRED ∈ {0.95,0.85,0.75,0.65,0.55}.

## Never

- ❌ `graphify --update` / `--backend claude-cli` (full re-extract trap).
- ❌ `build_merge` / `dedup.deduplicate_entities` (fuzzy-collapses existing nodes).
- ❌ parent-dir-prefixed node IDs; ❌ skipping tag wiring (it's the main new↔old connectivity).
