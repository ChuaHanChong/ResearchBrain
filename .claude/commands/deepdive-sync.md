---
description: Sync `Embodied-AI/NN_*.md` deep-dives with current `_KnowledgeHub_/` state — autonomously discover new papers, place them into the right section/sub-section/file, enrich sparse bullets to depth parity, sweep for 6-layer anti-patterns, repair section-sequence + cross-vault link drift. Self-contained — embeds the canonical Deep-Dive Format spec.
---

# /deepdive-sync

Topic / scope from the user: **$ARGUMENTS**

**Dispatch this task to the research-assistant agent** via the Agent tool (`subagent_type: research-assistant`). The agent drives every phase below end-to-end and returns the final report. Deep-dive maintenance is **high-volume vault traversal** — Phase 1 alone fingerprints every in-scope file and screens every uncited KH note; those file-content reads belong in the subagent's context, not the parent's. The research-assistant is the right specialist: its skill toolchain (`obsidian-cli`, `alphaxiv-search`, `knowledgehub-query`, `graphify`, `paper-curate`) is already bound to its persona, its memory carries prior refactor-session context that canonicalized the 6-layer format, and `Embodied-AI/` maintenance is named in its job description.

Pass the agent these instructions:

- **Task**: synchronize in-scope `Embodied-AI/NN_*.md` files with the current state of `_KnowledgeHub_/` and the canonical 6-layer deep-dive format.
- **Format**: strictly follow the **Deep-Dive Format** in the `## Format reference (canonical)` section at the end of this command. That's the single source of truth — do not improvise. (CLAUDE.md only points here; it carries no spec content of its own.)
- **Source-of-truth rule**: metrics, methods, and architectural specifics come from the paper's `_KnowledgeHub_/{ID}.md` note. **Never invent.** If KH lacks a number, skip the metric — do not write `(metrics not yet reported)` placeholders (the v2 format dropped them).
- **Voice rule**: edits are *additive* and *minimal*. Preserve existing L1 framing prose, L5/L6 callout voice, and Decision Matrix structure. Touch only what the phase identified as drift.
- **Workflow**: run the 6 phases below in order, end-to-end. No user-confirmation pauses between phases — drive the work autonomously, except where Phase 2's deferral rules explicitly punt to user review.
- **Skip file 01**: `01_Embodied-AI-101.md` is an intentional 101-narrative document — out of scope. Do not touch.
- **Output**: use `Skill(skill="obsidian:obsidian-markdown")` for Obsidian-formatting guidance (wikilinks, callouts, highlight syntax) and write edits via the Edit tool. Then run the Phase 6 audit.

## Mode

Parse `$ARGUMENTS`:

- **Full sweep** (default, empty `$ARGUMENTS`): run all phases (0–6) across the full in-scope set (`Embodied-AI/[0-9][0-9]_*.md` minus `01_Embodied-AI-101.md`). Autonomous discovery → placement → enrichment → anti-pattern repair → cross-vault reciprocity → audit.

- **Single-file** (`<NN_File>`, e.g. `04_WAM`, `04_WAM.md`, `Embodied-AI/04_WAM.md`): run all phases (0–6) scoped to that file only:
  - **Argument normalization**: strip `Embodied-AI/` prefix and `.md` suffix; resolve to `Embodied-AI/<NN_Title>.md` for file operations
  - **Phase 5 differs**: only outbound links from the in-scope file are checked; inbound reciprocity from sibling files is skipped (single-file scope can't justify edits to other files' L6 callouts)

- **Audit-only** (`audit`): if `$ARGUMENTS` contains `audit`, skip Phases 0–5 and run only **Phase 6** audit against the in-scope set. Read-only structural compliance check; no rewriting. Useful as a diagnostic "what's the current state?" run without committing to fixes.

The agent owns *discovering* which KH papers are new (uncited in any in-scope file) and *deciding* their topical placement. The user never specifies paper IDs or topics — that's the agent's job.

## Phase 0 — Scope setup

- Resolve in-scope files from mode (defaults to the full set under `Embodied-AI/[0-9][0-9]_*.md` minus `01_*`)
- Internalize the **6-layer pattern + full template** from the `## Format reference (canonical)` section at the end of this command — that is the spec the audit and all edits must conform to
- Pull baseline metrics for each in-scope file: `### N.` count, `#### N.N` count, L4/L5/L6 counts, line count, KH-citation count. Store for the Phase 6 delta report.
- **Graphify freshness check**: verify `graphify-out/graph.json` is newer than the newest `_KnowledgeHub_/*.md`. If stale, abort with a directive to run `/kh-graph-sync` first — Phase 1a's concept-proximity placement signal needs current graph data, and a stale graph silently degrades placement accuracy.

  ```bash
  if [ ! -f graphify-out/graph.json ]; then
    echo "MISSING GRAPH — graphify-out/graph.json does not exist; run /kh-graph-sync first"
  else
    NEWEST_KH=$(ls -t _KnowledgeHub_/*.md | head -1)
    [ "graphify-out/graph.json" -nt "$NEWEST_KH" ] || \
      echo "STALE GRAPH — run /kh-graph-sync first; graph.json is older than $NEWEST_KH"
  fi
  ```

## Phase 1 — Drift detection

For each in-scope file, identify four drift classes in parallel using the **three vault search methods** (introduced in `/research-directions`):

1. **`obsidian-cli` (tag / alias / property search)** — invoke `Skill(skill="obsidian:obsidian-cli")` for tag (`tag:<topic>`), alias, or frontmatter property search. Best for "which KH papers carry tag X but aren't yet cited in this file."
2. **`graphify` (concept graph)** — invoke `Skill(skill="graphify")` to query the precomputed concept graph at `graphify-out/graph.json`. Read `graphify-out/GRAPH_REPORT.md` first for god-nodes + surprising connections (cheap, low-token); drop to CLI queries (`query`, `path`, `explain`) for specific concept navigation. Best for "which KH papers cluster near this file's existing cited set."
3. **`General/` topic → `knowledgehub-query` (topic-anchored content search)** — first read the relevant `General/` topic file to identify sub-topics + curated papers; then invoke `Skill(skill="knowledgehub-query")` to filter papers within that scope by content. Best for "within General/0N_Topic, which papers aren't yet in deep-dive 0M_X."

### 1a. Missing-paper drift (autonomous discovery)

The agent owns this entirely — no user-supplied IDs, no user-supplied topics.

For each in-scope file, enumerate KH papers that *should* be cited but aren't:

1. **Build the file's "topical fingerprint"** — collect its `tags:` (frontmatter), `### N.` section titles, `#### N.N` sub-section titles, and the union of `tags:` from every paper it already cites. This fingerprint defines "what belongs in this file."
2. **Build the candidate pool** — `_KnowledgeHub_/*.md` minus papers already cited *anywhere* in the in-scope set. (Cross-cited papers are fine; uncited papers are the candidate pool.)
3. **Score candidates against fingerprints** using three signals:
   - **Tag overlap** (`obsidian:obsidian-cli` for tag/property queries): candidate ↔ file tag intersection
   - **Concept proximity** (`graphify`): candidate's graph distance to the file's cited-set centroid; God-node co-membership is a strong positive
   - **General/ co-location** (`General/` topic → `knowledgehub-query`): if a candidate sits in the General/ topic that points at this deep-dive in Cross-References, that's a strong positive
4. **Assign each candidate to its best-fit file** (or to none — long-tail papers may legitimately belong nowhere). When two files tie, prefer the one with more existing thematic siblings of the candidate. Each paper goes to **exactly one** deep-dive file.
5. **Flag confidence** (high/med/low) — high = multiple signals agree; low = only one signal, with surfaceable rationale for Phase 6's deferred-review list.
6. **Cluster the "no good home" pool** — for papers that score low against *every* existing file, check whether they cluster among themselves (graphify community membership + shared tags). If a cluster of **5+ papers** shares a coherent theme that no existing file covers, flag it as a candidate **new-deep-dive proposal** for Phase 2's deferral list. Below 5 papers → just leave them unplaced (long-tail).

The agent does not ask the user which papers to add — both discovery and placement are auto-executed from signal scores (tag overlap + graphify distance + General/ co-location for discovery; best-fit-by-fingerprint for placement). Judgment is reserved for Phase 2's deferral edges (sub-section axis splits, new-section warrant, new-file warrant) — the agent flags those for user review rather than guessing.

### 1b. Sparse-bullet drift

For each file's L3 bullets, count `==highlight==` markers and `**bold**` markers per bullet. Compute the file's median. Bullets below `max(1, median-2)` on either axis are *sparse* — candidates for depth enrichment from KH.

### 1c. Anti-pattern + structural drift (regex sweep)

Loop the checks below over the in-scope set:

```bash
for F in Embodied-AI/[0-9][0-9]_*.md; do
  [[ "$(basename "$F")" == 01_* ]] && continue
  echo "--- $F ---"

  # Anti-pattern A: legacy bold mini-headers (must be zero in in-scope sections)
  grep -nE '^\*\*\[[A-Z][^]]+\]\*\*\s+—' "$F"

  # Anti-pattern B: paper-listing bullets `- [[a]], [[b]]`
  grep -nE '^- \[\[[^]]+\]\],\s*\[\[' "$F"

  # Anti-pattern C: per-paper prose paragraph blocks (`**How X works**:` or `**Companion:**`)
  grep -nE '^\*\*(How [A-Z][a-z]+ works|Companion|Approach):\*\*' "$F"

  # Anti-pattern D: unbolded wikilink bullets at L3 (`- [[id|alias]] —` instead of `- **[[id|alias]]** —`)
  grep -nE '^- \[\[[0-9]{4}\.[0-9]+\|[^]]+\]\]\s+—' "$F"

  # Anti-pattern E: residual `(metrics not yet reported)` placeholders (dropped in v2)
  grep -n 'metrics not yet reported' "$F"

  # Anti-pattern F: whole-file cross-vault links in L6 callouts (should be section-anchored)
  # Excludes only ] and # — `|` allowed so `[[NN_File|alias]]` (whole-file-with-alias) is also caught
  awk '/^> \[!tip\]/,/^$/' "$F" | grep -oE '\[\[[0-9]{2}_[A-Z][^]#]+\]\]'

  # Anti-pattern G: bracket-wrapped L4 Decision Matrix header (`**[X — Decision Matrix]**`); paragon = no brackets
  grep -nE '^\*\*\[[^]]+— Decision Matrix\]\*\*' "$F"

  # Sequence integrity: `### N.` numbering must be 1,2,3,... no dupes / gaps
  grep -oE '^### [0-9]+\.' "$F" | grep -oE '[0-9]+' | \
    awk 'NR==1{p=$1} NR>1{if ($1!=p+1) print "GAP/DUPE at #" NR ": expected " p+1 " got " $1; p=$1}'

  # Per-section 6-layer distribution: each `### N.` section MUST have exactly 1 L4 + 1 L5 + 1 L6
  awk '
    BEGIN { l4=0; l5=0; l6=0 }
    function flush() {
      if (sect != "" && (l4!=1 || l5!=1 || l6!=1))
        printf "LAYER DRIFT in %s — L4=%d L5=%d L6=%d (each must be 1)\n", sect, l4, l5, l6
    }
    /^### [0-9]+\./ { flush(); sect=$0; l4=0; l5=0; l6=0; next }
    /^\*\*\[?[^][]*— Decision Matrix\]?\*\*/ { l4++ }
    /^> \[!star\]/ { l5++ }
    /^> \[!tip\]/  { l6++ }
    END { flush() }
  ' "$F"
done
```

Sequence-integrity drift looks like consecutive duplicate `### N.` headers (leftover from a section merge where downstream numbering wasn't propagated) or non-monotonic gaps (from deleted sections). The awk check above catches both.

### 1d. Wikilink integrity

**Primary**: invoke `Skill(skill="obsidian:obsidian-cli")` for vault-level broken-link detection — it's the dedicated Obsidian-native tool for this check and surfaces issues beyond just missing files (orphaned aliases, broken anchors, malformed links).

**Fallback** (if obsidian-cli is unavailable): per-file grep against `_KnowledgeHub_/` (only catches missing-file case, misses anchor and alias issues):

```bash
for F in Embodied-AI/[0-9][0-9]_*.md; do
  [[ "$(basename "$F")" == 01_* ]] && continue
  grep -oE '\[\[[0-9]{4}\.[0-9]+' "$F" | sort -u | sed 's/\[\[//' | \
    while read id; do [ -f "_KnowledgeHub_/${id}.md" ] || echo "MISSING: $id in $F"; done
done
```

Report per-file drift summary: `+N missing papers / N sparse bullets / N anti-pattern hits / N broken links / sequence ok|broken`.

## Phase 2 — Paper placement (for new papers)

For each paper flagged in 1a:

1. **Read its KH note** to extract: methods (for `==highlights==`), metrics (for `**bold**`), one-line significance. If the KH note lacks methods or metrics (truncated extraction, paper too new for full enrichment), optionally invoke `Skill(skill="alphaxiv-search")` to fetch full paper content from the alphaxiv MCP — *when available*. If the MCP backend is unavailable, fall back to the KH-note-only path; the resulting L3 bullet will be sparse and Phase 3 of a future run will enrich it.
2. **Decide its `### N.` section** by graphify-neighbor majority (of the candidate's top-5 nearest nodes in `graphify-out/graph.json`, which file is most represented) + General/ topic + the target file's Cross-References list.
3. **Decide its `#### N.N` sub-section** by axis-of-division match. If no fit:
   - If 2+ other unfiled papers share the new axis → propose a new `#### N.N` sub-section
   - If only this paper → place under the closest existing sub-section
4. **Decide insertion position** by descending arxiv ID within sub-section (matches `paper-curate` skill convention).
5. **Write the bullet** in canonical L3 format:
   ```
   - **[[arxiv_id|Paper Alias]]** — Description with ==method highlights== + **bold metrics**; significance clause.
   ```
   Use the paper's *exact* alias from `_KnowledgeHub_/{ID}.md`. Never fabricate. For wikilink, highlight (`==…==`), and callout syntax guidance, invoke `Skill(skill="obsidian:obsidian-markdown")`.
6. **Optional KH enrichment**: if the newly-placed paper's KH note lacks a figure in its `## Method` section, invoke `Skill(skill="paper-figure-extract")` to download a method figure from ar5iv and embed it in the KH note. This is a *compounding* fix — future `/deepdive-sync` enrichment runs (Phase 3) will have richer KH source material to draw `==highlight==` terms from.

**Decision-deferral rules** — blast radius decides who decides:

- **Auto** (agent does it, no user prompt):
  - Place a paper into an existing `### N.` / `#### N.N`
  - Create a new `#### N.N` sub-section when 2+ unfiled papers share a clean axis-of-division
  - Choose insertion position (descending arxiv ID within sub-section)
  - Write bullet text in canonical L3 format
- **Defer** (surface in Phase 6 report for user review):
  - Create a new `### N.` parent section in an existing file (3+ unfiled papers form a new theme inside that file's scope)
  - Rename an existing `### N.` to absorb a candidate cluster (changes downstream cross-vault anchors)
  - **Create a new deep-dive file** (`<NN+1>_<New-Topic>.md`, using the next available prefix after the highest existing one) — triggered by Phase 1a step 6 when 5+ unfiled papers cluster around a theme that no existing file covers
  - Demote a low-confidence candidate that has no good home in any file (flag as long-tail unplaced)

**New-deep-dive proposal payload.** When deferring a new-file creation, the agent generates a one-page proposal in the report containing: (a) proposed filename + title, (b) the 5+ anchor papers and why they cluster, (c) sketched `### N.` section list (3–5 sections minimum to justify a file), (d) the 2–3 existing files this new file would draw L6 cross-vault links from, (e) suggested frontmatter tags. The user decides yes/no; if yes, a follow-up `/deepdive-sync` run (or a dedicated session) creates the file from the proposal using the canonical template (see Format reference at the end of this command).

The deferral list is short and substantive — not a dumping ground for low-confidence calls the agent should have made itself.

### Parallel dispatch (optional — large placement workloads)

For **≥10 new placements** (Phase 1a's candidate pool is unusually full, e.g. after a large `/kh-sync` ingest), invoke `Skill(skill="superpowers:dispatching-parallel-agents")` for orchestration guidance, then dispatch one sub-agent per target deep-dive file via the Agent tool (`subagent_type: research-assistant`). Each sub-agent prompt includes: the target file's topical fingerprint + the candidate papers assigned to it by Phase 1a + the Phase 2 placement procedure + the L3 bullet format. After parallel completion, the parent agent merges results and continues to Phase 3.

**Tradeoff**: parallel dispatch costs N× the per-file fingerprint-read tokens (each sub-agent loads its file's existing content). For ≤9 placements or token-constrained sessions, place sequentially within the parent context — the latency win is small and the tokens add up.

### Brainstorming (optional — new-deep-dive proposals)

When Phase 1a step 6 flags a 5+ paper cluster as a candidate new-deep-dive proposal, invoke `Skill(skill="superpowers:brainstorming")` to refine the proposal collaboratively with the user before surfacing it in the Phase 6 report. Brainstorming's user-pause is appropriate here because new-file creation is a high-blast-radius decision that warrants conversation — unlike auto-placement of an individual paper into an existing section.

## Phase 3 — Bullet enrichment (for sparse bullets)

For each bullet flagged in 1b:

1. Read the paper's KH note (`_KnowledgeHub_/{ID}.md`)
2. Extract method terms from the note's `## Method` section → wrap in `==highlight==`
3. Extract metric numbers from the note's `## Results` section → wrap in `**bold**` (include unit / baseline / delta)
4. Rewrite the bullet preserving its existing significance clause; **never** drop information that was already there
5. Skip if KH note also lacks methods/metrics — sparse bullet is genuinely sparse upstream, not a maintenance issue. **Optional upstream fix**: invoke `Skill(skill="alphaxiv-search")` to fetch full paper content from the alphaxiv MCP (when available) and update the KH note. This pushes the fix to the source of truth; future `/deepdive-sync` runs will then enrich automatically. If the MCP is unavailable, skip and document the bullet as upstream-sparse.

Use the Edit tool (per the project convention against custom Python scripts for KH-adjacent work). Each enrichment must round-trip through the canonical L3 format — no shortcuts that re-introduce anti-patterns.

## Phase 4 — Anti-pattern + sequence repair

For each issue flagged in 1c, apply the fix from the **Anti-patterns table** (`## Format reference (canonical)` → `### Anti-patterns`). Two repairs need cross-file reads: **F** needs the target file's `### N.` headings to pick the right section-anchor, and **Seq** needs other in-scope files scanned for reciprocal `[[NN_File#N. …]]` references that the renumbering breaks.

Use `Skill(skill="obsidian:obsidian-markdown")` for wikilink + callout + heading-anchor syntax when retrofitting D (unbold→bold wikilinks), F (whole-file→section-anchored cross-vault links), and G (bracket-wrapped→paragon L4 headers).

Repair operations preserve all existing content — they restructure, never delete.

## Phase 5 — Cross-vault reciprocity

For each L6 `[!tip]` callout in the in-scope set:

- Extract its `[[NN_File#N. Section]]` cross-vault links
- For each linked target, verify the target file's parallel section either links back *or* would benefit from a back-link (use the agent's judgment)
- Propose reciprocal additions only when the target file's L6 callouts have **zero cross-vault links to the source file** (any link to the source — anchored or whole-file — counts as a non-zero connection). Non-zero connection is sufficient; we do not require per-link bidirectionality

This phase runs *only* in full-sweep mode (no args). In single-file mode, only outbound links from the in-scope file are checked.

## Phase 6 — Audit + report

Run format compliance audit (counts derived per-file, not hardcoded). The glob excludes `01_*` automatically and includes any future `NN_*` files added under `Embodied-AI/`:

```bash
for F in Embodied-AI/[0-9][0-9]_*.md; do
  [[ "$(basename "$F")" == 01_* ]] && continue
  echo "=== $F ==="

  # Structural counts
  SECT=$(grep -cE '^### [0-9]+\.' "$F")
  SUBS=$(grep -cE '^#### [0-9]+\.[0-9]+' "$F")
  # L4 grep anchored to header line — matches both paragon (no brackets) AND Anti-G (bracket-wrapped)
  MTX=$(grep -cE '^\*\*\[?[^][]*— Decision Matrix\]?\*\*' "$F")
  STAR=$(grep -cE '^> \[!star\]' "$F")
  TIP=$(grep -cE '^> \[!tip\]' "$F")
  echo "  §=$SECT  ####=$SUBS  L4=$MTX  L5=$STAR  L6=$TIP  (each L4/L5/L6 must equal §)"

  # Anti-patterns (each count must be 0)
  AP_A=$(grep -cE '^\*\*\[[A-Z][^]]+\]\*\*\s+—' "$F")
  AP_B=$(grep -cE '^- \[\[[^]]+\]\],\s*\[\[' "$F")
  AP_C=$(grep -cE '^\*\*(How [A-Z][a-z]+ works|Companion|Approach):\*\*' "$F")
  AP_D=$(grep -cE '^- \[\[[0-9]{4}\.[0-9]+\|[^]]+\]\]\s+—' "$F")
  AP_E=$(grep -c 'metrics not yet reported' "$F")
  AP_G=$(grep -cE '^\*\*\[[^]]+— Decision Matrix\]\*\*' "$F")
  echo "  anti-patterns: A=$AP_A B=$AP_B C=$AP_C D=$AP_D E=$AP_E G=$AP_G"

  # H2-spine presence (each required H2 must exist exactly once)
  # Use -Fx (fixed string + exact-line) to avoid prefix-substring false positives
  for h2 in "## Evolution Graph" "## Quick-Reference Matrix" "## Cross-References"; do
    n=$(grep -cFx "$h2" "$F")
    [ "$n" = "1" ] || echo "  H2 SPINE DRIFT: '$h2' count=$n (must be 1)"
  done

  # Sequence integrity (numbering must be 1,2,3,... contiguous)
  grep -oE '^### [0-9]+\.' "$F" | grep -oE '[0-9]+' | \
    awk -v f="$F" 'NR==1{p=$1} NR>1{if($1!=p+1)print "  SEQ DRIFT: expected "p+1" got "$1; p=$1}'

  # Per-section 6-layer distribution (each ### N. must have exactly 1 L4 + 1 L5 + 1 L6)
  awk '
    function flush() {
      if (sect != "" && (l4!=1 || l5!=1 || l6!=1))
        printf "  LAYER DRIFT — %s: L4=%d L5=%d L6=%d (each must be 1)\n", sect, l4, l5, l6
    }
    /^### [0-9]+\./ { flush(); sect=$0; l4=0; l5=0; l6=0; next }
    /^\*\*\[?[^][]*— Decision Matrix\]?\*\*/ { l4++ }
    /^> \[!star\]/ { l5++ }
    /^> \[!tip\]/  { l6++ }
    END { flush() }
  ' "$F"
done

# Wikilink integrity (loop over the same in-scope set)
for F in Embodied-AI/[0-9][0-9]_*.md; do
  [[ "$(basename "$F")" == 01_* ]] && continue
  grep -oE '\[\[[0-9]{4}\.[0-9]+' "$F" | sort -u | sed 's/\[\[//' | \
    while read id; do [ -f "_KnowledgeHub_/${id}.md" ] || echo "MISSING: $id in $F"; done
done

# paper-curate cross-check: every cited arxiv ID in deep-dives should also appear in General/
# (Soft warning — paper-curate is /kh-sync's responsibility, not deepdive-sync's, but uncurated
# citations indicate vault drift that should be surfaced.)
for F in Embodied-AI/[0-9][0-9]_*.md; do
  [[ "$(basename "$F")" == 01_* ]] && continue
  grep -oE '\[\[[0-9]{4}\.[0-9]+' "$F" | sort -u | sed 's/\[\[//' | \
    while read id; do
      grep -lq "\[\[${id}" General/*.md 2>/dev/null || \
        echo "  UNCURATED in General/: $id (cited in $F)"
    done
done

# Audit verdict — convert raw checks to PASS/FAIL assertions across the in-scope set
echo ""
echo "===== AUDIT VERDICT ====="

T_A=0; T_B=0; T_C=0; T_D=0; T_E=0; T_G=0
T_MISSING=0
for F in Embodied-AI/[0-9][0-9]_*.md; do
  [[ "$(basename "$F")" == 01_* ]] && continue
  T_A=$((T_A + $(grep -cE '^\*\*\[[A-Z][^]]+\]\*\*\s+—' "$F")))
  T_B=$((T_B + $(grep -cE '^- \[\[[^]]+\]\],\s*\[\[' "$F")))
  T_C=$((T_C + $(grep -cE '^\*\*(How [A-Z][a-z]+ works|Companion|Approach):\*\*' "$F")))
  T_D=$((T_D + $(grep -cE '^- \[\[[0-9]{4}\.[0-9]+\|[^]]+\]\]\s+—' "$F")))
  T_E=$((T_E + $(grep -c 'metrics not yet reported' "$F")))
  T_G=$((T_G + $(grep -cE '^\*\*\[[^]]+— Decision Matrix\]\*\*' "$F")))
  T_MISSING=$((T_MISSING + $(grep -oE '\[\[[0-9]{4}\.[0-9]+' "$F" | sort -u | sed 's/\[\[//' | \
    while read id; do [ -f "_KnowledgeHub_/${id}.md" ] || echo X; done | wc -l | tr -d ' ')))
done

[ "$T_A" -eq 0 ]       && echo "✓ Anti-pattern A (legacy bold mini-headers): 0"       || echo "✗ Anti-pattern A: $T_A instances"
[ "$T_B" -eq 0 ]       && echo "✓ Anti-pattern B (paper-listing bullets): 0"          || echo "✗ Anti-pattern B: $T_B instances"
[ "$T_C" -eq 0 ]       && echo "✓ Anti-pattern C (per-paper prose paragraphs): 0"     || echo "✗ Anti-pattern C: $T_C instances"
[ "$T_D" -eq 0 ]       && echo "✓ Anti-pattern D (unbolded L3 wikilinks): 0"          || echo "✗ Anti-pattern D: $T_D instances"
[ "$T_E" -eq 0 ]       && echo "✓ Anti-pattern E (residual placeholders): 0"          || echo "✗ Anti-pattern E: $T_E instances"
[ "$T_G" -eq 0 ]       && echo "✓ Anti-pattern G (bracket-wrapped L4 headers): 0"     || echo "✗ Anti-pattern G: $T_G instances"
[ "$T_MISSING" -eq 0 ] && echo "✓ All KH wikilinks resolve"                           || echo "✗ $T_MISSING broken KH wikilinks"

# Structural drift (LAYER, H2 SPINE, SEQ) and UNCURATED are surfaced inline by the per-file loops above.
# Clean run = no output for those checks. UNCURATED is a soft warning, not a fail.
```

**Pass criteria** (the verdict block is the contract):

- AUDIT VERDICT block above shows all `✓`
- Per-file loops above produced zero `LAYER DRIFT`, `H2 SPINE DRIFT`, `SEQ DRIFT`, or `MISSING:` lines
- `UNCURATED in General/:` lines are soft warnings — do not block pass, but suggest running `/kh-sync` to refresh paper-curate coverage

Invoke `Skill(skill="superpowers:verification-before-completion")` to enforce the evidence-before-claims gate: the AUDIT VERDICT block must show all `✓` and the per-file loops must have produced no drift lines. If any check fails, identify which one, re-apply the relevant Phase 4 repair (or fix the structural gap manually), and re-run the audit. Never claim completion based on partial evidence — the verdict block is the contract.

After the audit passes, the agent prints:

```
DEEPDIVE-SYNC REPORT — <mode summary>

Candidate pool: N uncited KH papers detected
Auto-placed:    M papers across K files (confidence: H high / M med / L low)
Unplaced:       (N - M) papers — no good home in any file (listed below)

Per-file deltas:
  02_Dataset-Benchmark-Environment.md  +3 papers  4 enriched  2 AP fixed  seq✓  links✓
  04_WAM.md                            +1 paper   0 enriched  0 AP fixed  seq✓  links✓
  ...

Aggregate: +M papers placed, N bullets enriched, N anti-patterns repaired,
           N sequence renumberings, N broken links resolved,
           N cross-vault reciprocity additions

Deferred (need user review — short list, substantive only):
  - <file>: propose new ### N. "<theme>" — backed by N unfiled papers [list IDs]
  - <file>: propose ### N.N split — N papers now under one axis "<…>"
  - NEW DEEP-DIVE PROPOSAL: 12_<Topic>.md
      Anchor papers (N): [list IDs + 1-line each]
      Proposed sections: [3–5 ### N. titles]
      Cross-vault sources: [existing files this would link from]
      Suggested tags: [...]
      Rationale: <why no existing file fits>
  - Unplaced (long-tail): [arxiv_ids] — flag if you expected coverage
```

Suggest `/kh-graph-sync` as the natural follow-up if N+ new papers were placed (graph should re-extract to include them).

## Exemplars

Defer to these for style after the Format reference: `Embodied-AI/02_Dataset-Benchmark-Environment.md` §4 (the original paragon), `Embodied-AI/11_Sim-to-Real-Transfer.md` §2–§5 (full 6-layer pattern with non-trivial Decision Matrices).

---

## Format reference (canonical)

The canonical **Deep-Dive Format** for `Embodied-AI/NN_*.md` notes. Strictly follow this spec.

### Frontmatter (3 fields, mandatory)

```yaml
---
title: "<Topic> — Deep Dive"
tags:
  - <primary-tag>
  - <secondary-tag>
  - <secondary-tag>
aliases:
  - "<Topic>"
  - "<Alternative Name>"
---
```

`status` / `created` / `modified` intentionally omitted — Obsidian tracks mtime in file metadata, and deep-dives don't have meaningful "draft" states.

### H2 spine (in order)

1. `# <Topic> — Deep Dive` — H1 matches frontmatter `title`
2. `> [!abstract] Overview` callout — 2–4 sentence top-level summary: what the deep-dive covers, the canonical papers, the key tension, what the reader gets
3. `## Evolution Graph` — `mermaid` diagram with year-range subgraphs + 1–2 paragraph narrative + 3-col timeline table (`Year | Paper | Contribution`)
4. `## Part A — <Conceptual / Foundational chunk>`, `## Part B — <Methods / Architecture chunk>`, `## Part C — <Capabilities / Comparison / Open Problems chunk>` — each opens with italicized 1-line framing, then contains the per-section `### N.` blocks (next H3 below)
5. `## Quick-Reference Matrix` — 2-col `| Question | Answer |` table; the file's "fast scan" entry point
6. `## Cross-References` — wikilinks to sibling deep-dives with 1-line relevance note + 1-line trailing italicized "See [[X]] for Y" sentence

Inside Parts A/B/C, every `### N. Section Title` follows the 6-layer pattern below.

### Section structure (the heart)

Every `### N. Section` contains these layers in order. **L4, L5, L6 each appear once per `### N.` section** — sub-sections (`#### N.N`) only carry L3 bullets, no callouts of their own.

1. **L1 — Framing prose** (2–4 paragraphs): why the category exists / what tension it resolves. Not a bullet-summary.
2. **L2 — `#### N.N Sub-section Title`** (0 or more per section; no upper limit): the *axis of division*. Opens with 1–2 sentence intro + L3 bullets. Use 0 sub-sections for single-paper or single-axis sections — L3 bullets go directly under `### N.` in that case.
3. **L3 — Bullet-per-paper** (four rules):
   1. **Format** (two variants by entry type):
      - Arxiv paper: `- **[[arxiv_id|Paper Alias]]** — Description with ==highlighted methods== + **bold metrics**; significance clause.`
      - Non-arxiv tool (engine, simulator, framework, dataset without arxiv ID): `- **[Tool Name](https://url)** — Description with ==highlighted methods== + **bold metrics**; significance clause.`
   2. **Bold the lead link** at bullet start — either `- **[[...]]**` (wikilink) or `- **[...](url)**` (external link).
   3. **One bullet = one paper / tool.** Multi-sentence OK if precise — every sentence earns its place.
   4. **`==highlight==` the methods** (e.g. `==RSSM==`, `==MoE gating==`, `==flow-matching action expert==`) and **bold the metric numbers** (`**99.2%**`, `**+27pp**`, `**3–4 ms/step**`, `**>900K FPS**`). If no metric available, skip — no placeholder.
4. **L4 — Decision Matrix**: `**<Section> — Decision Matrix**` header + table (paragon-canonical, no brackets — e.g., `**Engine — Decision Matrix**`). 2 columns canonical (`| Need | Recommendation |`); 3+ columns OK when the decision is an axis-comparison (e.g. `| Paradigm | Speed | Robustness | Best For |`). Table cells may carry wikilinks `[[id\|alias]]` *or* bold external links `[Tool](url)` depending on whether the entry has an arxiv ID. Decision-oriented (intent → paper/tool), not a data-dump of L3 bullets.
5. **L5 — `> [!star] <Title>` callout**: a curated **3–5 paper shortlist** with **editorial significance** — *foundational/canonical* papers and **why they matter to the field**, not their specs. The `[!star]` callout type is mandatory; **title default is `Key Papers`**, with two relaxed variants encouraged when they sharpen the framing: `Key Papers — <Editorial Suffix>` (e.g., `Key Papers — Design-Space Exemplars`, `Key Papers — WAM Failure Frontier`) or a fully custom editorial label (`Key Recipes`, `Key Datasets`, `Key Design-Space Papers`, `Bimanual Tactile Landmark`). **No metric overlap with L3** (exception: when the metric IS the claim, e.g. DreamerV3's "**150+** tasks with fixed hyperparameters"). Bullet format: `> - [[id|alias]] — significance clause` (wikilink unbolded inside callouts — the `> ` prefix provides visual weight).
   - Good clauses: "the canonical X for Y" · "established the Z paradigm" · "first proof that W" · "the reference architecture for V" · "the methodological landmark that mapped the design space".
6. **L6 — `> [!tip] [Strategic Title]` callout** (placed AFTER L5): the section's **takeaway** — the meta-trade-off, surprising finding, or strategic framing. Synthesize **across sub-sections**, not summarize one.
   - **Title** names the insight directly: `Late Fusion Beats Early Concatenation`, `When to Use WAM vs VLA`, `The Compute-Data Axis Is Now Measurable`, `Egocentric Is the New Pretraining Substrate`.
   - **Pick one of five framings** (illustrative, not exhaustive):
     - *Trade-off*: "X gives you Y at the cost of Z."
     - *Surprising-finding*: "The 2026 surprise: X is *not necessary* — Y emerges from Z."
     - *Composition-recipe*: "These compose — train with A, deploy with B."
     - *Strategic-when-to-use*: "Reach for this when X; otherwise see [[file#N. Section]]."
     - *Common-root*: "All these failures share root X" (for Open Problems sections).
   - **End with ≥1 section-anchored cross-vault link** — never whole-file. Use Obsidian heading-anchor syntax:
     - `[[NN_OtherDeepDive#N. Section Title]]` — jumps to that `### N. Section`
     - `[[NN_OtherDeepDive#N.N Sub-section Title]]` — jumps to that `#### N.N` sub-section
   - Whole-file `[[NN_OtherDeepDive]]` links only for genuine whole-document references. Pick targets where a reader who finishes THIS section would naturally want to deepen on a related topic.

The canonical per-section template:

```markdown
### N. <Section Title>

<L1: 1–2 paragraphs framing prose explaining WHY this category exists / what tension it resolves.>

#### N.1 <Axis-of-Division Title>

<Brief 1–2 sentence intro on what unifies these papers.>

- **[[id|alias]]** — Compressed description with ==architectural highlight== + **bold metric**; significance clause.
- **[[id|alias]]** — Description with **bold metric**.
- **[Tool Name](https://url)** — Non-arxiv tool variant for engines / simulators / frameworks without an arxiv ID; same `==highlight==` + **bold metric** rules apply.

#### N.2 <Axis-of-Division Title>

<Brief intro.>

- **[[id|alias]]** — Description with ==highlight== + **bold metric**.
- **[[id|alias]]** — Description.

**<Section> — Decision Matrix**

| Need | Recommendation |
|---|---|
| <Use case 1> | [[id\|alias]] (**metric**) |
| <Use case 2> | [Tool Name](https://url) |

> [!star] Key Papers — <optional editorial suffix, or use a fully custom title>
> - [[id|alias]] — Editorial significance: the canonical X for Y / established the Z paradigm / first proof that W. (No metric overlap with L3 unless the metric IS the significance.)
> - [[id|alias]] — Editorial significance clause.
> - [[id|alias]] — Editorial significance clause.

> [!tip] <Strategic Title — name the trade-off / surprising finding / composition recipe / when-to-use / common-root>
> <The one takeaway — pick one of the 5 framings (Trade-off / Surprising-finding / Composition-recipe / Strategic-when-to-use / Common-root). Synthesize across sub-sections, not summarize one.> Cross-reference [[NN_OtherDeepDive#N. Section Title]] for the related topic and [[MM_AnotherDeepDive#N.N Sub-section Title]] for the complementary view.
```

The Evolution Graph at file top, the Quick-Reference Matrix near file bottom, and the file-trailing italicized cross-reference sentence (`*See [[OtherDeepDive]] for <related topic>, or [[01_Embodied-AI-101]] to start from the basics.*`) are file-level wrappers around the per-section blocks — see H2 spine above for ordering.

### Open Problems variant

The last `### N+1. Open Problems & Failure Modes` section uses the same 6-layer scaffold with three substitutions:

| Layer | Standard section | Open Problems variant |
|---|---|---|
| **L3** | `- **[[arxiv_id\|Alias]]** — …` | `- **<Problem name>** — <description with citations>; significance clause.` (failure modes, not papers) |
| **L4** | `| Need | Recommendation |` | `| Problem | Remediation Path |` (same no-brackets `**Section — Decision Matrix**` header) |
| **L5** | `> [!star] Key Papers` | `> [!star] Key Papers — <Topic> Failure Frontier` (Failure Frontier variant of the editorial-suffix pattern) |
| **L6** | Any of the 5 framings | *Common-root* framing: "All these failures share root X" — cross-references the orthogonal failure-mode section in a sibling file |

L1, L2, and the per-section layer counts (1× L4 / 1× L5 / 1× L6) are unchanged.

### Anti-patterns (zero tolerance — Phase 1c regex catches these)

Each anti-pattern below has a matching regex in Phase 1c above and a matching repair in Phase 4.

| ID | Pattern | Fix |
|---|---|---|
| **A** | Legacy bold mini-header (`**[Title]** —`) instead of `#### N.N Title` | Retrofit to `#### N.N`, renumber within section |
| **B** | Paper-listing bullet (`- [[a]], [[b]]`) | Split into one bullet per paper |
| **C** | Per-paper prose paragraph (`**How X works:**`, `**Companion:**`) | Absorb into bullet with `==highlight==` for specifics |
| **D** | Unbolded L3 wikilink (`- [[…]]` instead of `- **[[…]]**`) | Add bold |
| **E** | Residual `(metrics not yet reported)` placeholder | Delete the placeholder text; bullet stands on non-metric content |
| **F** | Whole-file L6 cross-vault link (`[[NN_File]]` in `[!tip]`) | Retrofit to section-anchored `[[NN_File#N. Section]]` |
| **G** | Bracket-wrapped L4 header (`**[X — Decision Matrix]**`) | Strip outer brackets → `**X — Decision Matrix**` (paragon convention) |
| **Seq** | `### N.` numbering with dupes or gaps (consecutive duplicate numbers from a section merge, or non-monotonic gaps from a deleted section) | Renumber downstream; update reciprocal `[[NN_File#N. …]]` anchors |

A deep-dive that triggers *any* of A–G or Seq is not yet at canonical state — Phase 4 must repair before Phase 6 declares pass.

### Connective-tissue conventions

| Element | Convention |
|---|---|
| **Filename** | `Embodied-AI/NN_Title-With-Dashes.md` — two-digit zero-padded prefix, dash-joined title in title-case, `.md` extension. New files use the next available prefix continuing from the highest existing one. |
| **Section heading** | H3 `### N. Title` for parent; H4 `#### N.N Title` for sub-section; numbering is contiguous within file (no gaps, no dupes) |
| **L3 bullet (arxiv paper)** | `- **[[arxiv_id\|Alias]]** — Description ==methods== + **metric**; significance.` Bold wikilink at bullet start. |
| **L3 bullet (non-arxiv tool)** | `- **[Tool Name](https://url)** — Description ==methods== + **metric**; significance.` Bold external link at bullet start; same `==highlight==` + **bold metric** rules. |
| **Decision Matrix header** | `**<Section> — Decision Matrix**` — no brackets (paragon-canonical); see L4 spec for full rules. Bracket-wrapped form is caught by Anti-pattern G. |
| **Wikilinks in tables** | Pipe-escape: `[[id\|alias]]` |
| **Wikilinks in prose / callouts** | Plain pipe: `[[id\|alias]]` (no escape) |
| **Cross-vault links (L6 callouts)** | Section-anchored: `[[NN_File#N. Section Title]]` or `[[NN_File#N.N Sub-section Title]]`. Whole-file `[[NN_File]]` only for genuine whole-doc references. |
| **Required callouts** | `[!star]` (L5) and `[!tip]` (L6) appear **exactly once** per `### N.` section (also `[Section] — Decision Matrix` for L4). Phase 6 audit's per-section LAYER DRIFT check enforces this. L5-title flexibility is specified in the L5 spec. |
| **Optional callouts** | `[!abstract]` (Overview), `[!success]`, `[!warning]`, `[!example]`, `[!info]`, `[!question]` (in-section supplements; placed wherever they aid the reader) |
| **Mermaid in Evolution Graph** | `graph TD` or `graph LR`; year-range subgraphs; `style A fill:#hex,stroke:#hex` for thread colouring |
| **Dates in prose** | Avoid — frontmatter carries no `created` / `modified` either; Obsidian tracks mtime |
| **File 01 (`Embodied-AI-101`)** | Out of scope for `/deepdive-sync` — intentional 101-narrative format; do not retrofit |
