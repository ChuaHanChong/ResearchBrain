---
description: Sync `_KnowledgeHub_/` and `General/` with the URL list in `knowledge.py`. Generate the five short fields for new papers via `extract_summaries.py` (self-contained, shells out to `claude -p` per paper), rescue any missing Detailed Reports via cmux, enrich + validate, then curate into General/ topic files.
---

# /kh-sync

Use the **research-assistant agent** to sync the vault with `.claude/skills/alphaxiv-summary-extract/scripts/knowledge.py`. The agent applies its memory, vault conventions, and tag/alias judgment throughout.

## 1. Generate & assemble

Invoke `Skill(skill="alphaxiv-summary-extract")`: run `extract_summaries.py --input .../knowledge.py --out _KnowledgeHub_` (Mode B). One script call does everything — it computes pending IDs itself, and for each one shells out to a `claude -p` subprocess to synthesize the five short fields (Summary/Problem/Method/Results/Takeaways) from `mcp__alphaxiv__get_paper_content(fullText=true)`, then fetches title, BibTeX, and the `## Detailed Report` (still fetched from alphaxiv's `.md` render, unaffected by any of its redesigns), then writes the note. No subagent dispatch, no stdin, no intermediate file. Prints Processed / Skipped / Failed at the end; a paper that fails is caught per-paper and the loop continues.

`knowledge.py` is a living mirror — the user appends IDs continuously, sometimes mid-run. The script recomputes pending fresh on every invocation (`{knowledge.py IDs} − {existing KH stems}`), so just re-run it to pick up new appends or retry failures.

**Cost gate:** each pending paper costs ~140k-180k tokens / ~25-130s to generate the five fields (measured). For a large pending backlog, run with `--limit N` first, confirm `validate_reports.py` passes, then ask the user before running the rest uncapped — don't silently fan out a hundreds-deep backlog in one call.

## 2. Enrich, validate & format-QA

Apply the **post-processing defined in the alphaxiv-summary-extract skill** to the newly-written notes — that owns the note-quality work and runs on every ingest:

- frontmatter enrichment (authors / tags / aliases) + Method/Results formatting;
- **validate + format-QA the Detailed Reports** (`validate_reports.py` → `claude -p` subagent repair for failures → semantic sonnet format-QA for heading-hierarchy / glued-word issues the regex can't catch → re-validate to `FAIL 0`);
- the **alias dedup check** (surface vault-wide alias collisions before moving on).

Don't re-implement these here — the skill is the single source of truth; this step just says *run them*.

## 3. Rescue notes missing a Detailed Report (only if any exist)

Some newly-written notes will be missing `## Detailed Report` because alphaxiv has no intermediate report for that paper: `overview/{id}.md` 404s. Expect this for a large share of fresh papers (98 of 201 in the 2026-09-26 sync). The five fields are unaffected.

Invoke `Skill(skill="alphaxiv-summary-extract")` and run `generate_overviews.py --missing-reports` **after enrichment finishes** (it rewrites the notes it patches, so concurrent edits to the same note can collide). It uses the `.md` report when one exists and otherwise copies the abs page's AI overview into the note. Run it in the foreground: `nohup` and `run_in_background` both break cmux eval. A note stays without a Detailed Report only if neither source exists - a missing section beats a fabricated one. **Name the IDs, don't just count them**: list every ID whose outcome isn't `+patched-md` / `+patched-ai-overview` (e.g. `timeout`, `withdrawn`, `probe-fail`, `+copy-failed`, `+validate-fail`) in the final report (step 6).

## 4. Curate

Invoke `Skill(skill="paper-curate")` (Mode A). For each newly-enriched note, the agent places its `[[ID|Alias]]` wikilink into the matching sub-topic of the right `General/` topic file (descending-arxiv-ID sort). Surveys and benchmarks also go into `12_Benchmarks-and-Surveys.md`.

Refresh the paper count in `General/00_Index.md`.

## 5. Refresh the concept graph

If step 1 ingested ≥1 new paper, invoke `Skill(skill="kh-graph-sync")`. Its graph-source diff finds exactly the notes just added, extracts them, and additively merges them into `graphify-out/graph.json` (Steps 1–3 of that skill). Skip if 0 new papers. Run its `enrich` pass only periodically, not every sync.

## 6. Report

Print:

```
KH:       <before> → <after> (+N)
Reports:  validated N | FAIL 0 (M repaired via subagents)
Rescue:   R still missing a Detailed Report (IDs: ..., outcome: timeout/withdrawn/...)
Curated:  P placements across Q General/ files
Graph:    <nodes before> → <nodes after> (+ΔN nodes, +ΔE edges)
Failed:   F papers (still pending, listed by ID)
```
