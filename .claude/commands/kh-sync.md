---
description: Sync `_KnowledgeHub_/` and `General/` with the URL list in `knowledge.py`. Scrape new papers, enrich them, rescue any chromedriver failures via cmux browser-warming, then curate into General/ topic files.
---

# /kh-sync

Use the **research-assistant agent** to sync the vault with `.claude/skills/alphaxiv-summary-extract/scripts/knowledge.py`. The agent applies its memory, vault conventions, and tag/alias judgment throughout.

## 1. Scrape

Invoke `Skill(skill="alphaxiv-summary-extract")` in batch mode. The skill skips papers whose `{ID}.md` already exists and reports Processed / Skipped / Failed counts.

## 2. Enrich

For each newly-written note, apply the post-processing defined in the alphaxiv-summary-extract skill (frontmatter + Method/Results formatting), then run the skill's **alias dedup check** to surface any vault-wide collisions before moving on.

## 3. Rescue failed papers (only if step 1 had failures)

> **Checkpoint** — needs human-in-the-loop.

Open each failed URL in cmux:

```bash
cmux new-surface --type browser --url "https://www.alphaxiv.org/abs/<ID>" --focus false
```

Tell the user: "Click 'Generate Overview' on each surface, then reply 'retry' (or 'skip <ID>' to abandon a paper)."

On `retry`: re-run the scrape with `--ids <still-failed-list>`, then loop back to step 2 for the rescues.

## 4. Curate

Invoke `Skill(skill="paper-curate")` (Mode A). For each newly-enriched note, the agent places its `[[ID|Alias]]` wikilink into the matching sub-topic of the right `General/` topic file (descending-arxiv-ID sort). Surveys and benchmarks also go into `08_Benchmarks-and-Surveys.md`.

Refresh the paper count in `General/00_Index.md`.

## 5. Report

Print:

```
KH:       <before> → <after> (+N)
Curated:  P placements across Q General/ files
Failed:   F papers (still pending, listed by ID)
```

Suggest `/kh-graph-sync` as the natural follow-up.
