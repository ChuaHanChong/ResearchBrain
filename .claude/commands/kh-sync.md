---
description: Sync `_KnowledgeHub_/` and `General/` with the URL list in `knowledge.py`. Scrape new papers, enrich + validate their Detailed Reports, rescue failures by auto-generating missing overviews on a signed-in cmux browser, then curate into General/ topic files.
---

# /kh-sync

Use the **research-assistant agent** to sync the vault with `.claude/skills/alphaxiv-summary-extract/scripts/knowledge.py`. The agent applies its memory, vault conventions, and tag/alias judgment throughout.

## 1. Scrape

Invoke `Skill(skill="alphaxiv-summary-extract")` in batch mode. The skill skips papers whose `{ID}.md` already exists and reports Processed / Skipped / Failed counts.

`knowledge.py` is a living mirror — the user appends IDs continuously, sometimes mid-run. Compute pending fresh as `{knowledge.py IDs} − {existing KH stems}` (not the truncatable extract_summaries.py "Failed" line), and recompute after every scrape/retry.

## 2. Enrich, validate & format-QA

Apply the **post-processing defined in the alphaxiv-summary-extract skill** to the newly-written notes — that owns the note-quality work and runs on every ingest:

- frontmatter enrichment (authors / tags / aliases) + Method/Results formatting;
- **validate + format-QA the Detailed Reports** (`validate_reports.py` → `claude -p` subagent repair for failures → semantic sonnet format-QA for heading-hierarchy / glued-word issues the regex can't catch → re-validate to `FAIL 0`);
- the **alias dedup check** (surface vault-wide alias collisions before moving on).

Don't re-implement these here — the skill is the single source of truth; this step just says *run them*.

## 3. Rescue failed papers (only if step 1 had failures)

Persistent failures (chromedriver stack traces surviving auto-retry) are papers with **no pre-generated overview** (`/overview/{ID}.md` → 404). **Generating one requires being signed into alphaxiv and clicking the "Generate Overview" button** — merely opening the page does *not* warm or generate it (a fresh surface just redirects to `/signin`). So the rescue is: the user signs into alphaxiv **once** in a cmux browser, then the skill's **auto-generate** rescue drives that **single authenticated surface** through every failed paper hands-free (`generate_overviews.py --ids-file <failed> --surface <signed-in surface>`, harness-managed background — never `nohup`, which breaks cmux eval). Invoke `Skill(skill="alphaxiv-summary-extract")` and follow its **"auto-generate via cmux browser (hands-free)"** rescue section — **don't open a browser tab per paper.**

**Don't block** — kick off generation, then keep enriching/curating the successful notes while it runs. On `retry`, recompute pending (step 1), scrape the newly-generated overviews (`--force` not needed — they have no note yet), and re-run from step 2. A 404 on `/abs/{ID}.md` means no overview yet (generate it); a 404 on arxiv itself means withdrawn — skip it. Note: some papers time out generation repeatedly (alphaxiv-side) and stay pending across syncs — list them, don't loop on them.

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
Curated:  P placements across Q General/ files
Graph:    <nodes before> → <nodes after> (+ΔN nodes, +ΔE edges)
Failed:   F papers (still pending, listed by ID)
```
