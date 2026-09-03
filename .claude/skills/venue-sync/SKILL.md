---
name: venue-sync
description: "Record where each KnowledgeHub paper was published - venue, year, presentation tier (oral/spotlight/highlight) and citation count - and badge them inline in General/ and Embodied-AI/. Invoke only when the user explicitly asks for it: 'update the venues', 'refresh venue data', 'which papers are orals', or a direct question about a paper's venue, tier or citation count."
---

# Venue Sync

Papers arrive in `_KnowledgeHub_/` as arXiv preprints with no sign of whether they were ever peer-reviewed.
This resolves that from public sources and records it, so the vault can be filtered by where work was
published rather than by arXiv ID alone.

Run from the project root with the vault's `.venv`:

```bash
S=.claude/skills/venue-sync/scripts
.venv/bin/python $S/venue_lookup.py refresh      # fetch + apply + annotate + stats; the normal entry point
.venv/bin/python $S/venue_lookup.py fetch        # populate data/.venue-cache/
.venv/bin/python $S/venue_lookup.py apply        # dry run; --write to commit to notes
.venv/bin/python $S/venue_lookup.py stats        # rewrite the Venue Coverage table in General/00_Index.md
.venv/bin/python $S/venue_annotate.py --write    # inline badges; --strip is the exact inverse
```

## Fields

A resolved paper carries five keys in frontmatter, where Bases can filter on them:

```yaml
venue: "ICML"            # closed vocab, one of the core ten
venue_year: 2021         # the venue year, never the preprint year
venue_type: "conference" # conference | journal | workshop
venue_tier: "oral"       # oral | highlight | spotlight | poster
citations: 54924         # Semantic Scholar; -1 means absent from it
```

An unresolved paper carries **only `citations`** — venue keys are omitted, not blanked, since most of the
vault is unpublished and Bases reads an absent property as null. `citations` always appears because 0 is a
real count and it is the only signal an unpublished paper has.

Provenance lives under `## Publication` in the note's `%%` block, hidden by Obsidian but plain text to the scripts:

```
## Publication

- venue_source: proceedings   # proceedings | semantic-scholar | arxiv-comment | manual
- venue_checked: 2026-09-02   # when the record was set, not when it was last looked at
```

The block reads BibTeX, then `## Assessment` if `paper-rigor` has run, then `## Publication`.

`venue_checked` moves only when a resolved value moves, not when the layout does.

## Sources

Four, highest precedence first. Each is a lookup; nothing is inferred.

1. **`manual`** — the note is skipped entirely. Set it by hand after correcting a venue and it survives
   every future run.
2. **`proceedings`** — the venue's own record, and the **only source of tier**: conference programme JSON
   (`{site}/static/virtual/data/{slug}-{year}-orals-posters.json`), PMLR for CoRL and pre-2020 ICML, and the
   RSS proceedings pages. Matched on title within `[arxiv_year - 1, arxiv_year + 3]`. OpenReview would be
   the obvious source and is unusable — 403 bot challenge on both API versions.
3. **`semantic-scholar`** — venue name only, no year: its `year` is the preprint year, so ResNet would read
   2015 where the venue is CVPR 2016.
4. **`arxiv-comment`** — the authors' own comment string. Never updated after acceptance, so a missing venue
   means *no evidence found*, never *rejected*. Hence no `rejected` value anywhere in the schema.

## Two rules that keep it honest

Both were added after catching real errors, so removing either silently reintroduces a bug.

**A venue must have a year.** An unyeared venue cannot be sorted, filtered by recency, or badged, so such
papers have their venue dropped rather than half-recorded. The year is never guessed from the preprint date.
This costs ~1,100 papers, deliberately.

**A title check gates venue *and* citations.** Semantic Scholar sometimes maps an arXiv ID to a different
paper, and an unnoticed wrong citation count is worse than none. Matching tolerates truncation (`ASE` for
`ASE: Large-Scale Reusable Adversarial Skill Embeddings`), dropped subtitles, and version drift. Exact
matching was tried first and was too strict.

## Scope

`CORE_VENUES` lists NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, ICRA, IROS, CoRL, RSS — 373 of the 375
tier-bearing papers, so widening adds venue membership without adding tier signal. Only these reach notes;
everything else is blanked after resolution. Widening is a one-line edit plus `apply --write`, but it only
brings back papers that already carry a year: of 1,032 non-core papers, 247 return and 785 stay dropped
because Semantic Scholar supplies no year for them.

Consequences worth knowing: journals hold the vault's highest citation counts yet can never carry a tier, so
any tier-only view excludes them by construction; and ICRA/IROS have no open tier source at all (IEEE Xplore
needs a key), so they show venue and year but never oral/poster.

## Badges

`venue_annotate.py` appends the venue after each paper wikilink in `General/` and `Embodied-AI/`:

```
[[2210.13066|DaXBench]] (ICLR'23 Oral)
```

Its strip regex is built from the **closed set of short venue names in use**, not a generic `]] (...)`
pattern — those files carry 100+ hand-written parentheticals like `(MCTS)` and `(driving NPCs)` that a loose
pattern deletes. Build the vocabulary from *all* venues, not just the core ten, or a venue dropped from the
list leaves orphaned badges forever. Code fences are skipped.

Side effect: badges push ~519 deep-dive bullets past the 400-character anti-pattern-H ceiling. Attribute an
AP_H count on a de-badged copy before blaming a sweep.

## Verifying

`apply --write` and `venue_annotate.py --write` are both idempotent, so a second run reporting anything but
**0 changes** means state is drifting. Beyond that: every venued note should have a year, type and source;
an unvenued note should carry none of those; every badge should match its note.

Write the check carefully and disbelieve it when it contradicts a spot check. Three separate verification
scripts here reported thousands of false failures while the data was fine — `\s*` matching newlines under
`re.M` so a bare key read the next line's value, and a lookbehind pattern applied to a substring where it can
never match. Confirm one failure by hand before believing a mass one.
