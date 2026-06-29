---
description: Sync `_KnowledgeHub_/` and `General/` with the URL list in `knowledge.py`. Scrape new papers, enrich them, rescue any chromedriver failures via cmux browser-warming, then curate into General/ topic files.
---

# /kh-sync

Use the **research-assistant agent** to sync the vault with `.claude/skills/alphaxiv-summary-extract/scripts/knowledge.py`. The agent applies its memory, vault conventions, and tag/alias judgment throughout.

## 1. Scrape

Invoke `Skill(skill="alphaxiv-summary-extract")` in batch mode. The skill skips papers whose `{ID}.md` already exists and reports Processed / Skipped / Failed counts.

`knowledge.py` is a living mirror — the user appends IDs continuously, sometimes mid-run. Compute pending fresh as `{knowledge.py IDs} − {existing KH stems}` (not the truncatable extract_summaries.py "Failed" line), and recompute after every scrape/retry.

## 2. Enrich

For each newly-written note, apply the post-processing defined in the alphaxiv-summary-extract skill (frontmatter + Method/Results formatting), then run the skill's **alias dedup check** to surface any vault-wide collisions before moving on.

## 3. Rescue failed papers (only if step 1 had failures)

Persistent failures (chromedriver stack traces surviving auto-retry) are papers with **no pre-generated overview**; opening the URL in a real browser warms alphaxiv's backend so a later retry succeeds. **Don't block** — open *all* failed URLs at once, then keep enriching/curating the successful notes while the user generates overviews on their own schedule.

```bash
cmux new-surface --type browser --url "https://www.alphaxiv.org/abs/<ID>" --focus false
```

Tell them how many surfaces opened and list the pending IDs in the report's Failed line. On `retry`, recompute pending (step 1) and re-run from step 2. A 404 on `/abs/{ID}.md` means withdrawn — skip it.

## 4. Curate

Invoke `Skill(skill="paper-curate")` (Mode A). For each newly-enriched note, the agent places its `[[ID|Alias]]` wikilink into the matching sub-topic of the right `General/` topic file (descending-arxiv-ID sort). Surveys and benchmarks also go into `08_Benchmarks-and-Surveys.md`.

Refresh the paper count in `General/00_Index.md`.

## 5. Refresh the concept graph

If step 1 ingested ≥1 new paper, invoke `Skill(skill="kh-graph-sync")`. Its graph-source diff finds exactly the notes just added, extracts them, and additively merges them into `graphify-out/graph.json` (Steps 1–3 of that skill). Skip if 0 new papers. Run its `enrich` pass only periodically, not every sync.

## 6. Report

Print:

```
KH:       <before> → <after> (+N)
Curated:  P placements across Q General/ files
Graph:    <nodes before> → <nodes after> (+ΔN nodes, +ΔE edges)
Failed:   F papers (still pending, listed by ID)
```
