---
description: Generate or refresh a research-direction doc under _Projects_/Research-Directions/. Self-contained — embeds the canonical format spec; engages the research-assistant agent's Hinton-as-mentor advisory mode for direction theses.
---

# /research-directions

Topic / scope from the user: **$ARGUMENTS**

**Dispatch this task to the research-assistant agent** via the Agent tool (`subagent_type: research-assistant`). The agent drives every phase below end-to-end and returns the final doc + audit. Research-direction generation is **survey-grounded ideation** — Phase 1 alone enumerates surveys + benchmarks across the vault and reads full paper content via alphaxiv-search (and the alphaxiv `.md` endpoint); those reads belong in the subagent's context, not the parent's. The research-assistant is the right specialist: its skill toolchain (`obsidian-cli`, `alphaxiv-search`, `knowledgehub-query`, `graphify`, `paper-curate`) is already bound to its persona, its `Hinton-as-mentor` advisory voice is the canonical mode for thesis formulation, and research-direction synthesis is named in its job description. Do not execute the phases in the parent context.

Pass the agent these instructions:

- **Task**: generate (or refresh) the research-direction doc for the topic above, under `_Projects_/Research-Directions/` (see Output filename below for axis routing).
- **Format**: strictly follow the **Research-Direction Document Format** in the `## Format reference (canonical)` section at the end of this command. That's the single source of truth — do not improvise. (CLAUDE.md only points here; it carries no spec content of its own.)
- **Source-of-truth rule**: paper aliases, contributions, anchor papers, and benchmark numbers come from `_KnowledgeHub_/{ID}.md`. **Never invent.** If a benchmark number isn't in the cited paper's KH note, skip the metric — do not fabricate placeholder numbers in Thesis bets or Key targets rows.
- **Curate, don't concatenate** (the core quality rule): a direction doc is *synthesis*, not a pile of one-liners copied from KH / General / deep-dives. For the load-bearing papers of each direction (its anchors + the strongest Related-table rows), **read the full papers** (method + results — via `Skill(skill="alphaxiv-search")`, the alphaxiv `.md` endpoint, or arxiv) **and the related content already in the vault** (the matching `General/` topic files and `Embodied-AI/` deep-dives), then write the **inter-paper linkage**: how the papers relate (lineage / contrast / composition) and the gap each leaves that motivates the direction. Never paste a KH / General / deep-dive line verbatim. **Every sentence must read smoothly and coherently** — the Why-it-matters list and the Related comparison table are one connected argument, not stitched-together copied summaries.
- **Persona**: engage **Hinton-as-mentor advisory mode** (per the agent's `## Persona — Hinton-as-mentor`) for direction theses. Apply integrated thinking — first-principles + research taste + novelty fire together. **Hinton-validate the whole intellectual structure** — the **cluster scheme**, **every research direction**, **each First-principles framing**, and **every Hypothesis** must pass Hinton-as-mentor review: the clusters carve the space the way a strong researcher would; each direction is a distinct, non-consensus bet worth pursuing (not a re-slice of a sibling); the bet is falsifiable with a number; the three FP bullets each carry distinct intellectual load; each hypothesis is a sharp falsifiable prediction a strong researcher would actually run — not a generic "does X work?". If any of these does not pass, iterate it or drop it.
- **Workflow**: run the phases specified by the active mode (New = 0–7, Update = affected only, Audit = 7 only, Plan = 0–3), in order, end-to-end. No user-confirmation pauses — drive the work autonomously, except where Phase 3's Plan-mode brainstorming explicitly punts to user review.
- **Skip topic `_Projects_/01_FirstPublication/`**: that subtree is an independent-study project artifact (blueprint + roadmap + repo). Out of scope — do not cross-link from research-direction docs.
- **Output**: depends on mode. **New** / **Update** → use `Skill(skill="obsidian:obsidian-markdown")` for Obsidian-formatting guidance (wikilinks, callouts, frontmatter syntax) and write the file via the Write tool, then run the Phase 7 audit. **Audit** → run Phase 7 audit only (no write). **Plan** → return the cluster overview + direction titles to the user (no write, no audit).

## Mode

Parse `$ARGUMENTS`:

- **New** (default, plain topic argument): create the doc from scratch. Run all phases (0–7).
- **Update** (`update` / `refresh` keyword or names an existing doc): refresh the named doc. Read current state, identify deltas, re-run only affected phases:
  - New papers in vault → Phase 1c (full-content reading) for the new papers + update affected Phase 4 cards
  - Stale or weak thesis → Phase 4 for that direction only
  - New convergence pattern → Phase 2 + Cross-Cutting Themes refresh
  - Preserve existing direction cards unless their thesis is stale or new papers reshape the framing
- **Audit** (`audit` / `check` keyword + doc name): skip Phases 0–6 and run only **Phase 7** on the named doc. Read-only structural compliance check; no rewriting. Useful as a diagnostic "does this doc still meet canonical format?" run without committing to fixes.
- **Plan** (`plan` / `outline` / `dry-run` keyword): run only **Phases 0–3** (scope → papers → patterns → clusters) and return the proposed cluster structure + direction titles. Skip Phases 4–7 (no per-direction cards, no synthesis, no doc write). Useful for previewing the structure before committing to full generation.

The agent owns *deriving* clusters and directions from convergence patterns. The user never pre-specifies cluster count, theme names, or direction labels — those emerge from the topic's research landscape (per Phase 3's divergent-thinking rule). Judgment is reserved for Plan-mode brainstorming where new-clustering proposals warrant conversation — the agent flags those rather than guessing.

## Phase 0 — Scope setup

Derive scope:
- **New** / **Plan**: from `$ARGUMENTS`.
- **Update**: from the existing doc's frontmatter and the scope content in `## Methodology`; apply any explicit overrides from `$ARGUMENTS`.
- **Audit**: skips Phase 0 — runs Phase 7 only.

Scope fields:
- Topic + working title (`Promising Research Directions: <Title>`)
- Output filename: `_Projects_/Research-Directions/<axis>/<Topic>.md` — `<axis>` is `Mechanism/` (embodiment-agnostic: data/training/eval substrates, world-action-model architecture, sim-to-real) or `Capability/` (a physical capability/embodiment: manipulation, locomotion, whole-body coordination). The cross-cutting umbrella lives at the folder root as `Embodied-AI.md`
- Corpus filter: parse from `$ARGUMENTS` if explicit (e.g., "last 2 years", "post-2024"); otherwise no filter

Direction count, cluster count, and cluster themes are **not pre-set** — they emerge from the topic's research landscape in Phases 1–3.

## Phase 1 — Source paper discovery (surveys + benchmark papers)

Surveys reveal open problems; benchmarks reveal what's measurable. Both are required inputs.

### 1a. Vault-first

The vault supports **three search methods** — use them in combination for comprehensive coverage:

1. **`obsidian-cli` (tag / alias / property search)** — invoke `Skill(skill="obsidian:obsidian-cli")` to search by tag (`tag:survey`, `tag:benchmark`, `tag:<topic>`), alias, or frontmatter property. Best for finding papers by metadata.
2. **`graphify` (concept graph)** — invoke `Skill(skill="graphify")` to query the precomputed concept graph at `graphify-out/graph.json`. Read `graphify-out/GRAPH_REPORT.md` first for god-nodes + surprising connections (cheap, ~5K tokens); drop to CLI queries (`query`, `path`, `explain`) for specific concept navigation. Best for cross-paper bridges and concept-proximity discovery.
3. **`General/` topic → `knowledgehub-query` (topic-anchored content search)** — first read the relevant `General/` topic file to identify sub-topics + curated papers; then invoke `Skill(skill="knowledgehub-query")` to filter papers within that scope by content. Best for topic-anchored discovery.

Also read `Embodied-AI/` deep-dives for surveys and benchmarks cited there.

### 1b. Vault sufficiency check, then alphaxiv expansion if needed

Assess whether the vault corpus is sufficient for the topic. If sufficient, proceed to 1c with the vault set. If gaps remain (recency, sub-topic coverage), invoke `Skill(skill="alphaxiv-search")` to find additional surveys and benchmarks beyond vault coverage.

### 1c. Full-content reading via alphaxiv-search [Required]

Use `Skill(skill="alphaxiv-search")` to read full content for all selected papers. **You MUST read the FULL survey and benchmark papers** — surveys for their verbatim open-problem statements (the fuel that motivates every direction), benchmarks for what they actually measure + their protocol — never work from a survey's or benchmark's one-line KH summary. Likewise, **you MUST read the FULL method papers** — the method *and* results in full for every load-bearing paper, never the abstract or its one-line KH summary — because Phase 4's synthesis and inter-paper linkage (lineage, contrast, composition) depend on how each paper actually works.

Output: paper list (minimum 15 papers; more if the topic is broad) with type tag (survey/benchmark) + the verbatim open-problem statement (surveys) or key metric + number (benchmarks) — this becomes the Survey Landscape's middle column.

If fewer than 15 papers are available after 1a + 1b, proceed with what's available and note the limitation in the doc's `## Methodology` scope content (e.g., "corpus limited to N papers due to topic specificity").

## Phase 2 — Convergence patterns

Identify convergence patterns from the read content — where **multiple survey and benchmark papers** diagnose the same gap under different vocabulary. **Cite ONLY survey and benchmark papers in the patterns** (the fuel); never method papers. Format per the `> [!tip] Convergence patterns` callout in the Format reference below.

## Phase 3 — Clustering proposal

**Apply divergent-then-convergent thinking** — don't lock in the first clustering that comes to mind.

- **New / Update modes** (autonomous): generate 2–3 candidate clusterings internally (different ways to group the convergence patterns), evaluate each against criteria (cluster balance, theme coherence, density of cross-direction synergy), and commit to the strongest.
- **Plan mode** (interactive preview): invoke `Skill(skill="superpowers:brainstorming")` to refine the clustering collaboratively with the user before committing. Brainstorming's user-pause is appropriate here because Plan mode is itself an interactive preview.

Use Latin cluster letters (A/B/C/…) with cluster-prefixed direction labels (A1, A2, B1, …). For each cluster: theme name, directions under it, shared bottleneck, cross-direction synergy — present as the Cluster Overview table per the Format reference below.

**Hinton-validate before committing**: the chosen cluster scheme *and* the direction list must pass Hinton-as-mentor review — each cluster is a theme a strong researcher would genuinely carve, and each direction is a distinct, non-consensus bet (not a re-slice of a sibling direction or another doc). Drop or merge any that does not pass.

## Phase 4 — Per-direction generation (Hinton-as-mentor advisory mode ON)

Per the agent's `## Persona — Hinton-as-mentor`: for each direction, **apply integrated thinking** — **first-principles** + **Hinton's research taste** (4 tenets) + **novelty** fire together. Generate the per-direction card following the canonical 6-block structure in the Format reference below (table → Why it matters → First-principles → Related comparison table → Hypotheses & tests → Risks); the Thesis row must follow the integrated thesis sentence template (also in the Format reference).

**Direction ideas must be novel** — iterate until the framing is non-consensus and defensible on first principles.

**Curate with linkage, not concatenation.** Each card is one connected argument grounded in the *full* papers read in Phase 1c. The Why-it-matters list, the First-principles framing, the Related comparison table, and the Hypotheses & tests must all turn on the **same load-bearing 3–5 papers**, each section doing a different job on them: Why-it-matters narrates the field state, First-principles argues from/against them, the Related table compares them on a direction-specific axis, and **each Hypothesis tests the bet against a specific table row** (its `Row`). A reader must be able to trace the bet → its evidence → its tests across the card. Never paste a KH one-liner where synthesis is needed.

### Parallel dispatch (optional — large direction counts)

For **≥6 directions** where total wall-clock matters more than token cost, invoke `Skill(skill="superpowers:dispatching-parallel-agents")` for orchestration guidance, then dispatch one sub-agent per direction via the Agent tool (`subagent_type: research-assistant` or `general-purpose`). Each sub-agent prompt must include: direction title + cluster context + Phase 1c corpus *subset relevant to that direction* (not the full corpus — keep payloads tight) + the 6-block card template + the curate-with-linkage mandate (read the load-bearing papers in full; the card must be one connected argument) + the Hinton-as-mentor validation instruction (First-principles + Hypotheses). After parallel completion, assemble the returned cards in cluster order.

**Tradeoff**: parallel dispatch costs N× the corpus-read tokens (each sub-agent loads its own subset). For ≤5 directions or token-constrained sessions, generate sequentially within the parent context — the latency win is small and the tokens add up.

### Paper-adding workflow

When adding papers to a card (a row in the Related comparison table, or an Anchor-papers / Key-targets entry):

1. **Vault search first** using the three methods (see Phase 1a): `obsidian-cli` for tag/property, `graphify` for concept-graph navigation, and `General/` topic → `knowledgehub-query` for topic-anchored content search.
2. `Skill(skill="alphaxiv-search")` for full-content reading of each candidate.
3. Write the comparison-table row: where the paper sits on the direction's axis, its key result, and **what it leaves missing** — related to the other rows (lineage / contrast), not a standalone summary.
4. Add to the card using the paper's exact alias from `_KnowledgeHub_/{ID}.md`.

Never list a paper without reading its content. Never fabricate aliases, contributions, or numbers.

## Phase 5 — Synthesis

Generate per the Format reference below: Cross-Cutting Themes, Benchmark Gaps, Cross-References.

## Phase 6 — Assembly

Assemble in canonical H2 order per the Format reference below. Write the file (see Output instruction in the dispatch directive).

## Phase 7 — Audit

Run format compliance audit (counts derived from the doc, not hardcoded):

```bash
DOC="<output filename>"

# Direction labels (A1/B2/...)
grep -cE '^### [A-Z][0-9]+ —' "$DOC"

# Cluster headers
grep -cE '^## Cluster [A-Z] —' "$DOC"

# First-principles framing blocks — should equal direction count
grep -c '^\*\*First-principles framing\.\*\*$' "$DOC"

# Risks callouts — should equal direction count
grep -c '^> \[!warning\] Risks' "$DOC"

# Card rows — should equal 4 × direction count
grep -cE '^\| \*\*(Cluster|Thesis|Anchor papers|Key targets)\*\*' "$DOC"

# FP 'The bet' bullets lacking a number — should be 0 (Anti-pattern C; the bet's number lives in First-principles, not the Thesis row)
grep -E '^- \*\*The bet\*\*' "$DOC" | grep -vcE '[0-9]'

# Spine section checks (each should be 1)
grep -c '^> \[!abstract\] Overview' "$DOC"        # top-of-doc Overview callout
grep -c '^## Methodology' "$DOC"                  # Methodology (absorbs the scope: corpus / filter / exclusions)
grep -cE '^## .*Survey Landscape' "$DOC"          # Survey Landscape (with or without domain prefix)
grep -c '^## Formal Framing' "$DOC"               # Formal Framing
grep -c '^## Cluster Overview' "$DOC"             # Cluster Overview
grep -c '^## Cross-References' "$DOC"             # Cross-References

# Convergence callout
grep -c '^> \[!tip\] Convergence patterns' "$DOC"

# Wikilinks resolve
grep -oE '\[\[[0-9]{4}\.[0-9]+' "$DOC" | sort -u | sed 's/\[\[//' | \
  while read id; do [ -f "_KnowledgeHub_/${id}.md" ] || echo "MISSING: $id"; done

# No status/created/modified in frontmatter (extracts YAML block regardless of size)
awk '/^---$/{c++; next} c==1' "$DOC" | grep -cE '^(status|created|modified):'  # expect 0

# H1 matches frontmatter title
H1=$(grep -m1 '^# ' "$DOC" | sed 's/^# //')
FM_TITLE=$(awk '/^---$/{c++; next} c==1 && /^title:/ {sub(/^title:[ ]*/, ""); gsub(/^"|"$/, ""); print; exit}' "$DOC")
[ "$H1" = "$FM_TITLE" ] && echo "✓ H1 ↔ frontmatter title match" || echo "✗ H1 ↔ title MISMATCH: H1='$H1' title='$FM_TITLE'"

# Cross-Cutting Themes — count [!tip] callouts (should be ≥3)
awk '/^## Cross-Cutting Themes/,/^## Benchmark Gaps/' "$DOC" | grep -cE '^> \[!tip\] '

# Cross-Cutting Themes per-callout direction refs (each callout body should reference ≥2 labels)
awk '/^## Cross-Cutting Themes/,/^## Benchmark Gaps/' "$DOC" | awk '
  /^> \[!tip\]/ {
    if (t > 0) print "  theme " t ": " n " direction refs" (n<2 ? " ⚠ WEAK" : "")
    t++; n = 0
    next                                              # skip title-line ref count
  }
  t > 0 && /^> / { n += gsub(/[A-Z][0-9]+/, "&") }
  END { if (t > 0) print "  theme " t ": " n " direction refs" (n<2 ? " ⚠ WEAK" : "") }
'

# Benchmark Gaps rows — should equal direction count
awk '/^## Benchmark Gaps/,/^## Cross-References/' "$DOC" | grep -cE '^\| .*\| [A-Z][0-9]+'

# Per-card structural completeness — each direction must have all 6 blocks
# Flag-setting rules are gated by `label` so content outside direction blocks
# (Cross-Cutting Themes, Benchmark Gaps, etc.) cannot leak into the last direction's flags
awk '
  function emit() {
    if (!label) return
    ok = has_card && has_why && has_fp && has_rel && has_hyp && has_risk
    if (!ok) {
      m = ""
      if (!has_card)  m = m " card-table"
      if (!has_why)   m = m " why-it-matters"
      if (!has_fp)    m = m " FP-framing"
      if (!has_rel)   m = m " Related-table"
      if (!has_hyp)   m = m " Hypotheses&tests"
      if (!has_risk)  m = m " Risks"
      print "  ✗ " label ": missing -" m
    } else {
      print "  ✓ " label ": all 6 blocks present"
    }
    label = ""
  }
  /^### [A-Z][0-9]+ —/ {
    emit()
    label = $2
    has_card = has_why = has_fp = has_rel = has_hyp = has_risk = 0
    next
  }
  /^## Cross-Cutting Themes/ { emit(); next }    # boundary: stop accumulating flags
  label && /^\| \*\*Cluster\*\*/                  { has_card = 1 }
  label && /\*\*Why it matters\.\*\*/             { has_why = 1 }
  label && /\*\*First-principles framing\.\*\*/   { has_fp = 1 }
  label && /\*\*Related research papers\.\*\*/    { has_rel = 1 }
  label && /\*\*Hypotheses & tests\.\*\*/         { has_hyp = 1 }
  label && /\[!warning\] Risks/                   { has_risk = 1 }
  END { emit() }                                  # handles case where CCT is missing
' "$DOC"

# Audit verdict summary — convert raw counts to PASS/FAIL assertions
echo ""
echo "===== AUDIT VERDICT ====="
DIR=$(grep -cE '^### [A-Z][0-9]+ —' "$DOC")
FP=$(grep -c '^\*\*First-principles framing\.\*\*$' "$DOC")
RISKS=$(grep -c '^> \[!warning\] Risks' "$DOC")
ROWS=$(grep -cE '^\| \*\*(Cluster|Thesis|Anchor papers|Key targets)\*\*' "$DOC")
THEMES=$(awk '/^## Cross-Cutting Themes/,/^## Benchmark Gaps/' "$DOC" | grep -cE '^> \[!tip\] ')
GAPS=$(awk '/^## Benchmark Gaps/,/^## Cross-References/' "$DOC" | grep -cE '^\| .*\| [A-Z][0-9]+')
MISSING_LINKS=$(grep -oE '\[\[[0-9]{4}\.[0-9]+' "$DOC" | sort -u | sed 's/\[\[//' | while read id; do [ -f "_KnowledgeHub_/${id}.md" ] || echo X; done | wc -l | tr -d ' ')
BET_NONUM=$(grep -E '^- \*\*The bet\*\*' "$DOC" | grep -vcE '[0-9]')
LEGACY=$(grep -cE '^\*\*(Evidence|Benchmarks & metrics|Concrete research questions)\.\*\*' "$DOC")
HYP_THIN=$(awk '/^## Cross-Cutting Themes/{if(seen&&c<5)bad++; seen=0} /^### [A-Z][0-9]+ —/{if(seen&&c<5)bad++; seen=1; c=0} seen&&/^[0-9]+\. \*\*H[0-9]/{c++} END{if(seen&&c<5)bad++; print bad+0}' "$DOC")
# Convergence patterns must cite only Survey-Landscape (survey/benchmark) papers — never method papers (Anti-pattern N).
# The fuel-table IDs are the lines between the Survey-Landscape header and the Convergence callout; any convergence ID outside that set is a method paper.
SL_TABLE_IDS=$(awk '/Survey Landscape/{f=1} /Convergence patterns/{f=0} f&&/^\|/' "$DOC" | grep -oE '[0-9]{4}\.[0-9]+' | sort -u)
CONV_BAD=$(awk '/^> \[!tip\] Convergence patterns/{f=1;next} /^---/{f=0} f' "$DOC" | grep -oE '[0-9]{4}\.[0-9]+' | sort -u | grep -vxF "$SL_TABLE_IDS" | grep -c .)

[ "$DIR" -eq "$FP" ]              && echo "✓ FP framing count matches direction count ($DIR)"             || echo "✗ FP framing $FP ≠ directions $DIR"
[ "$DIR" -eq "$RISKS" ]           && echo "✓ Risks callouts match direction count ($DIR)"                 || echo "✗ Risks $RISKS ≠ directions $DIR"
[ "$ROWS" -eq "$((DIR * 4))" ]    && echo "✓ Card rows = 4 × direction count ($ROWS)"                     || echo "✗ Card rows $ROWS ≠ 4×$DIR = $((DIR * 4))"
[ "$THEMES" -ge 3 ]               && echo "✓ Cross-cutting themes ≥3 ($THEMES)"                           || echo "✗ Cross-cutting themes $THEMES < 3"
[ "$GAPS" -eq "$DIR" ]            && echo "✓ Benchmark Gaps rows = direction count ($DIR)"                || echo "✗ Benchmark Gaps $GAPS ≠ directions $DIR"
[ "$MISSING_LINKS" -eq 0 ]        && echo "✓ All KH wikilinks resolve"                                    || echo "✗ $MISSING_LINKS missing KH wikilinks"
[ "$BET_NONUM" -eq 0 ]           && echo "✓ All First-principles bets carry a number"                      || echo "✗ $BET_NONUM FP 'The bet' bullet(s) lack a number (Anti-pattern C)"
[ "$LEGACY" -eq 0 ]              && echo "✓ No removed sub-sections (Evidence / Benchmarks / Concrete-questions)" || echo "✗ $LEGACY removed sub-section(s) present (Anti-pattern K — fold into Related table + Anchor tags)"
[ "$HYP_THIN" -eq 0 ]            && echo "✓ Every direction has ≥5 hypotheses"                              || echo "✗ $HYP_THIN direction(s) with <5 hypotheses (Anti-pattern L)"
[ "$CONV_BAD" -eq 0 ]            && echo "✓ Convergence patterns cite only Survey-Landscape (survey/benchmark) papers" || echo "✗ $CONV_BAD convergence paper(s) absent from the Survey Landscape (Anti-pattern N — only surveys/benchmarks fuel convergence)"

# Spine compliance — each required spine item must appear exactly once
SPINE_DRIFT=""
for h in "^> \[!abstract\] Overview" "^## Methodology" "^## .*Survey Landscape" "^## Formal Framing" "^## Cluster Overview" "^## Cross-References" "^> \[!tip\] Convergence patterns"; do
  n=$(grep -cE "$h" "$DOC")
  [ "$n" -eq 1 ] || SPINE_DRIFT="$SPINE_DRIFT|  ✗ spine '$h' count=$n (expected 1)"
done
if [ -z "$SPINE_DRIFT" ]; then
  echo "✓ Spine compliance: all 7 required items present (5 H2 sections + Overview + Convergence callouts)"
else
  echo "✗ Spine drift:"
  echo "$SPINE_DRIFT" | tr '|' '\n'
fi

# Size — informational only, not an assertion
wc -lw "$DOC"
```

Invoke `Skill(skill="superpowers:verification-before-completion")` for the evidence-before-claims gate: the **AUDIT VERDICT** block above must show all `✓` and the per-card completeness check must show `✓` for every direction. If any line is not `✓`, address the gap and re-run the audit. The verdict block is the completion contract.

## Exemplars

Defer to the **v3 exemplar**: `_Projects_/Research-Directions/Capability/Whole-Body.md` — **Cluster A (A1–A4)** shows the canonical 6-block card (Why-it-matters list, paper-grounded First-principles with the bet stated once, the Related comparison table on a direction-specific axis, and Hypotheses & tests with *Prediction · Test · Row · Falsifier*), and its Overview / Methodology / Survey Landscape / Formal Framing show the new spine. The other direction docs are **mid-migration to v3** — do not copy their card or spine style yet. The Format reference (canonical) below is the authority.

---

## Format reference (canonical)

The canonical **Research-Direction Document Format** for `_Projects_/Research-Directions/**/*.md` docs. Strictly follow this spec.

### Frontmatter (3 fields, mandatory)

```yaml
---
title: "<Title>"
aliases:
  - "<Alias 1>"
  - "<Alias 2>"
tags:
  - research-directions
  - <domain-tag-1>
  - <domain-tag-2>
---
```

`status` / `created` / `modified` are omitted — Obsidian tracks mtime in file metadata.

### H2 spine (in order)

1. `# <Title>` — H1 matches frontmatter `title`
2. `> [!abstract] Overview` callout — 2–4 sentences of **substance, not process**: (1) the domain's structural problem / central tension, (2) how the directions are organized (N directions across M clusters, around what axis), (3) the non-consensus thesis the doc collectively bets on. Do NOT restate the method ("each direction states a first-principles framing", "every number is sourced from KH") — the reader *sees* the framing in the cards, and provenance is a command rule, not reader content.
3. `## Methodology` — **scope only**, one short paragraph: the corpus (what was read), the recency/filter, and what is excluded. Do NOT list the generation process (survey-grounded ideation, the admission gates, first-principles practice, deep-dive mining) — that is agent-instruction, it lives in this command, and it is obvious to a reader. Keep it to what a reader needs about coverage. There is no separate Scope callout — scope lives here.
4. `## <Domain> Survey Landscape` — the **fuel** for the directions. 3-col table: `Survey / Benchmark | The open problem it names (surveys) or what it measures (benchmarks) | Fuels` — where **Fuels** lists the *direction labels* the paper feeds (a paper may fuel several; the single-`Sub-theme` grouping is dropped). The middle column must be the *specific* named problem a direction picks up, not a generic restatement. Followed by a `> [!tip] Convergence patterns` callout that **cites ONLY survey and benchmark papers** (never method papers — the method-level theses they motivate live in Cross-Cutting Themes) — keep a pattern **only when ≥3 survey/benchmark papers genuinely name the same gap in different vocabulary** (cross-corroboration that the gap is real, not one author's concern); drop any "pattern" that is really one paper. The callout holds the pattern bullets directly — **no italic preamble** explaining the callout's sourcing or pointing the reader to other sections (process boilerplate the reader doesn't need; anti-pattern M).
5. `## Formal Framing` — the **doc's own formalization**: the shared math objects the directions build on, defined in your words (the central quantities, distributions, metrics). A block-quote is allowed **only** when a survey gives the *canonical definition of a term* — never to paste a paper's method description.
6. `## Cluster Overview` — 4-col synergy table: `Cluster | Directions | Shared bottleneck | Cross-direction synergy`
7. `## Cluster A — <Theme>` (then B, C, …) — each opens with an italicized **1–2 sentence theme framing only** (what the cluster is about); no per-direction enumeration (that's the cards' job), no leadership/synergy prose (that's the `## Cluster Overview` table's job), no cross-doc deltas. Then the per-direction cards.
8. `## Cross-Cutting Themes` — at least 3 `> [!tip] <Insight Title>` callouts synthesizing across directions; each callout body references **≥2 directions** by label (otherwise it isn't cross-cutting), e.g., "A1, B2, C1 all rely on…". The callout title names the insight (e.g., "The Sim-to-Real Bottleneck Is Now Differentiable")
9. `## Benchmark Gaps` — 3-col table: `Gap | Direction | Existing closest` (1 row per direction)
10. `## Cross-References` — relative-path wikilinks to deep-dives, `General/`, KH, and sibling `Research-Directions/` docs (linked by basename, e.g. `[[WAM]]`, `[[Embodied-AI]]`)

### Per-direction card (the heart)

Each direction is an H3 `### A1 — <Title>` followed by the structure below — a 4-row card table (block 1), then **blocks 2–6 in order: Why it matters → First-principles framing → Related research papers → Hypotheses & tests → Risks** (six blocks total; the Phase 7 audit checks all six). No skips; no separate Evidence or Benchmarks sub-sections (folded in — see below).

```markdown
### A1 — <Direction Title>

| | |
|---|---|
| **Cluster** | A — <Theme> |
| **Thesis** | <2–3 short, plain sentences: the problem + the first principle that leads there + the assumption it challenges. NO metric number — the measurable bet lives once, in First-principles → The bet. End with "The bet is in First-principles below."> |
| **Anchor papers** | [[id\|alias]] (method), [[id\|alias]] (benchmark), [[id\|alias]] (survey), … — the foundational papers this direction rests on, each **tagged by its role in this direction**: `(method)` / `(benchmark)` / `(survey)`. No fixed count. |
| **Key targets** | <concrete metric anchors with specific numbers: SR / latency / OOD %, etc.> |

**Why it matters.** A 3-bullet list (not a paragraph), each a bolded lead + `:` —
- **The gap**: what's broken in the current state.
- **Today's answers**: the 1–2 current approaches, named with `[[id|alias]]` + numbers, and what they do *not* do.
- **The opening**: the existence proof / ablation that makes the bet reachable, with a number.

**First-principles framing.**
- **First principle**: <the irreducible structure — what's necessarily true, independent of training data; cite the paper(s) that demonstrate it, e.g. an ablation>
- **Assumption being challenged**: <name WHO holds it — cite the papers that bet the opposite, with their results>
- **The bet**: <the measurable, falsifiable prediction — specific numbers / thresholds (e.g. "ρ > 0.7", "≥30 Hz", "+X pp over Y"); cite the target paper(s). This is the card's ONLY home for the bet's number.>

**Related research papers.** One **comparison table** — every related paper is a row, compared on a *direction-specific axis* (the column[s] that capture how the papers differ), plus `Key result` and `What's missing`:

| <Direction-specific axis> | … | Key result | What's missing |
|---|---|---|---|
| [[id\|alias]] | … | <measured number> | <the gap this paper leaves open> |

(at least 8 rows; the axis choice IS the curation — pick the one dimension the direction turns on. No separate "breadth" bullet list and no plain bulleted list — this single table is the related-work section, and it absorbs what the old Evidence list held: the load-bearing "proof" papers are simply the strongest rows.)

**Hypotheses & tests.** The FP bet decomposed into falsifiable sub-hypotheses. Each item is a heading + four sub-bullets:
1. **H1 — <Title>.**
   - *Prediction*: <expected direction / number>
   - *Test*: <the experiment that would show it>
   - *Row*: <which Related-table row it lands on>
   - *Falsifier*: <what result kills the sub-hypothesis>
2. **H2 — <Title>.** … (**at least 5**; each a genuine, distinct sub-hypothesis of the FP bet — do not pad to hit the count)

> [!warning] Risks
> - <Risk 1: specific failure mode> — <1-line consequence + mitigation, tied to a Falsifier where relevant>
> - (at least 3 risk bullets)
```

**Thesis sentence template.** The Thesis row states three things — the taste-attracting problem, the first principle that leads there, and the assumption it challenges — in **2–3 short, plain sentences**. The measurable bet (with its number) lives **once**, in First-principles → "The bet"; the Thesis does *not* repeat it. Plain form:

> *"[Problem, in plain terms — the first principle can lead here]. The field assumes [conventional wisdom]. The bet is in First-principles below."*

**Write for clarity**: short sentences, plain words, no nested run-on. The Thesis carries no metric number — that is the FP bet's job.

### First-principles framing rubric (litmus test)

Each direction's `**First-principles framing.**` block has three bullets that must each carry **distinct intellectual load** — they cannot be merged or paraphrased into each other. The bullets themselves are described in the card template above; the table below specifies the *failure mode* for each (the litmus test):

| Bullet | Failure mode if missing |
|---|---|
| **First principle** | Without it, the direction reads as "what others did" rather than "what must be true." |
| **Assumption being challenged** | Without it, the direction isn't first-principles at all — it's incremental refinement of consensus. |
| **The bet** | Without it, the direction is a research framing rather than a proposal — no way to know if it succeeds. |

**The litmus test for committing to a direction: each of the three bullets fills with distinct intellectual load.** If any bullet does not yet fill, defer the direction until the framing crystallizes.

### Anti-patterns

Each pattern below is either caught by Phase 7's audit (structural) or enforced by the spec as a narrative gate (semantic). Listed alongside the canonical form.

| ID | Pattern | Audit-caught? | Fix |
|---|---|---|---|
| **A** | Direction labels use flat numeric (`D1, D2, D3`) instead of cluster-prefixed (`A1, A2, B1`) | ✓ (regex matches only cluster-prefixed) | Renumber per Connective-tissue conventions |
| **B** | Cluster letters use Roman numerals (`I, II, III`) | ✓ (regex matches only Latin) | Switch to Latin `A / B / C` per conventions |
| **C** | The bet (First-principles → **The bet**) lacks a number, or the **Thesis** row carries the number instead of pointing to First-principles | ✓ digit-presence proxy (an FP "The bet" bullet with no digit fails; the Thesis should carry none) | Put the measurable number in the FP bet; the Thesis ends "The bet is in First-principles below." |
| **D** | `**First-principles framing.**` block absent or filled with consensus restatement (three bullets don't carry distinct intellectual load) | ✓ presence only; semantic quality is a narrative gate | Apply the rubric's litmus test; if you can't fill all three bullets distinctly, drop the direction |
| **E** | Paper aliases fabricated, anchor papers cited without arxiv IDs, or anchor papers **not tagged** `(method)`/`(benchmark)`/`(survey)` | ✗ semantic (audit catches missing-file wikilinks only) | Use exact alias from `_KnowledgeHub_/{ID}.md`; tag each anchor by its role in this direction |
| **F** | **Related research papers** as a plain bulleted list, or split into a small table + a separate "breadth" bullet list, instead of ONE comparison table (every paper a row on a direction-specific axis + `Key result` + `What's missing`) | ✗ semantic | Use the single comparison table; the axis choice is the curation |
| **G** | Cross-Cutting Themes callouts reference only one direction label (not actually cross-cutting) | ✓ (per-callout direction-ref count <2) | Iterate to reference ≥2 directions per theme; if no ≥2-direction synthesis is possible, drop the theme |
| **H** | Benchmark Gaps without `Existing closest` column populated (just naming the gap with no current-state reference) | ✗ semantic | Add closest existing benchmark + brief delta from required scope |
| **I** | Per-direction Risks bullets lack mitigation hooks (just naming failures) | ✗ semantic | Add 1-line mitigation per risk — `Risk: X → Mitigation: Y` |
| **J** | Per-direction card missing one of the 6 blocks (card-table / Why it matters / First-principles / Related table / Hypotheses & tests / Risks) | ✓ (per-card structural completeness check in Phase 7) | Restore the missing block per the card template |
| **K** | A separate **Evidence**, **Benchmarks & metrics**, or **Concrete research questions** sub-section present (all removed/renamed in v3 — evidence papers are the load-bearing rows of the Related table; benchmark papers are tagged `(benchmark)` in Anchor papers; measured numbers live in Key targets + the table's `Key result` column; "Concrete research questions" is now **Hypotheses & tests**) | ✓ (LEGACY check flags any of the three) | Fold Evidence / Benchmarks into the Related table + Anchor tags; rename Concrete research questions → Hypotheses & tests |
| **L** | **Hypotheses & tests** with fewer than 5 items, or items written as open questions ("does X work?") instead of falsifiable predictions with *Prediction* / *Test* / *Row* / *Falsifier* | ✓ count partly audited; predictive quality is a narrative gate | Each item = Prediction · Test · Row · Falsifier; ≥5 genuine sub-hypotheses of the FP bet |
| **M** | Doc-level boilerplate: **Overview** / **Methodology** restate the generation process (admission gates, "survey-grounded ideation", "each direction states a first-principles framing"), or **Formal Framing** pastes a paper's method description as a block-quote, or a **Convergence patterns** callout opens with an italic meta-preamble explaining its sourcing / pointing to other sections | ✗ semantic | Overview = tension + structure + the bet; Methodology = scope only; Formal Framing = the doc's own object definitions; the Convergence callout holds only its pattern bullets (the process lives in this command) |
| **N** | **Convergence patterns** cite method papers, or papers absent from the Survey Landscape, instead of only surveys/benchmarks (the fuel) | ✓ (convergence IDs must be a subset of the Survey-Landscape table's IDs) | Cite only survey/benchmark papers that appear in the Survey Landscape table; move method-level corroboration to Cross-Cutting Themes |

Patterns A–N should reach their canonical form before the Phase 7 verdict.

### Connective-tissue conventions

| Element | Convention |
|---|---|
| **Direction heading** | H3 `### A1 — Title` (em-dash, TOC-visible in Obsidian's outline pane) |
| **Direction labels** | Cluster-prefixed: `A1, A2, A3 / B1, B2, B3 / C1, C2, …` — cluster sizes and total direction count vary per doc (determined by the topic's research landscape) |
| **Cluster letters** | `A / B / C / …` (Latin); never Roman numerals |
| **Wikilink syntax in tables** | Pipe-escape: `[[id\|alias]]` |
| **Wikilink syntax in prose** | Plain pipe: `[[id|alias]]` |
| **Paper display text** | The `alias` in `[[id\|alias]]` must be the **exact KH-canonical alias** from `_KnowledgeHub_/{id}.md` — never a paraphrase, variant, or task-name that differs from the note's alias |
| **Cross-doc refs (deep-dive / General / sibling docs)** | Relative-path with the **exact note name as display text**: `[[../Embodied-AI/NN_File\|NN_File]]`, `[[../General/NN_File\|NN_File]]`. Sibling research-direction docs link by **basename** (they live in `_Projects_/Research-Directions/`): `[[WAM\|WAM]]`, `[[Manipulation\|Manipulation]]`, `[[Embodied-AI\|Embodied-AI]]`. Never an abbreviation (`General/08`) and never a bare path link that renders the `../` prefix |
| **Section-anchored cross-refs** | When the reference is to a *specific section* of a deep-dive / General file, anchor the link to that section instead of writing `§N` as plain text outside it: `[[../Embodied-AI/NN_File#N. Section Title\|NN_File §N]]` (use the target's exact `### N. Section Title` heading). For a multi-section reference, anchor each: `[[../File#4. A\|§4]]/[[../File#5. B\|§5]]` |
| **Math in prose** | Inline `$...$` or block `$$...$$` |
| **Block-quotes** | In `## Formal Framing` only, and **only** for the *canonical definition of a term* from a survey — never to paste a paper's method description. No per-direction evidence quotes. |
| **Callouts used** | `[!abstract]` (top-of-doc Overview), `[!tip]` (Convergence patterns + each Cross-Cutting Theme with a titled insight), `[!warning]` (per-direction Risks). Scope lives inside `## Methodology` (no separate `[!info]` Scope callout). First-principles framing uses a bolded `**First-principles framing.**` label. |
| **Dates in prose** | Avoid explicit dates; the frontmatter has no `created` / `modified` fields either |
| **Plain wording** | Write for clarity — short sentences, plain words, minimal nested clauses and jargon; prefer 2–3 short sentences over one dense run-on. Applies to the Thesis, Why-it-matters, First-principles framing, and all prose |
| **Cluster intros = theme only** | The italic line under each `## Cluster X —` states the cluster's theme in 1–2 sentences; it does NOT enumerate the directions, assign leadership, or restate a card's cross-doc delta — those live in the `## Cluster Overview` table and the per-direction cards |
| **Current-state only** | Docs describe the current state, not their edit history — no "X used to live here / moved to Y / former / relocated" stubs after content moves; keep forward cross-references (sibling-doc pointers describing the present relationship) |
| **No cross-refs to `_Projects_/01_FirstPublication/`** | These docs are independent-study artifacts |
