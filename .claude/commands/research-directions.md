---
description: Generate or refresh a Research-Directions-<Topic>.md doc. Self-contained — embeds the canonical format spec; engages the research-assistant agent's Hinton-as-mentor advisory mode for direction theses.
---

# /research-directions

Topic / scope from the user: **$ARGUMENTS**

**Dispatch this task to the research-assistant agent** via the Agent tool (`subagent_type: research-assistant`). The agent drives every phase below end-to-end and returns the final doc + audit. Research-direction generation is **survey-grounded ideation** — Phase 1 alone enumerates surveys + benchmarks across the vault and reads full paper content via the alphaxiv MCP; those reads belong in the subagent's context, not the parent's. The research-assistant is the right specialist: its skill toolchain (`obsidian-cli`, `alphaxiv-search`, `knowledgehub-query`, `graphify`, `paper-curate`) is already bound to its persona, its `Hinton-as-mentor` advisory voice is the canonical mode for thesis formulation, and research-direction synthesis is named in its job description. Do not execute the phases in the parent context.

Pass the agent these instructions:

- **Task**: generate (or refresh) `_Projects_/Research-Directions-<Topic>.md` for the topic above.
- **Format**: strictly follow the **Research-Direction Document Format** in the `## Format reference (canonical)` section at the end of this command. That's the single source of truth — do not improvise. (CLAUDE.md only points here; it carries no spec content of its own.)
- **Source-of-truth rule**: paper aliases, contributions, anchor surveys, and benchmark numbers come from `_KnowledgeHub_/{ID}.md`. **Never invent.** If a benchmark number isn't in the cited paper's KH note, skip the metric — do not fabricate placeholder numbers in Thesis bets or Key targets rows.
- **Persona**: engage **Hinton-as-mentor advisory mode** (per the agent's `## Persona — Hinton-as-mentor`) for direction theses. Apply integrated thinking — first-principles + research taste + novelty fire together. Direction ideas must be **novel**; if framing matches consensus, iterate.
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
- **Update**: from the existing doc's frontmatter and Scope callout; apply any explicit overrides from `$ARGUMENTS`.
- **Audit**: skips Phase 0 — runs Phase 7 only.

Scope fields:
- Topic + working title (`Promising Research Directions: <Title>`)
- Output filename: `_Projects_/Research-Directions-<Topic>.md`
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

Use `Skill(skill="alphaxiv-search")` to read full content for all selected papers. Full content supplies the verbatim open-problem statements, methodology assumptions, and measurable numbers that Phase 2 and Phase 4 draw on.

Output: paper list (minimum 15 papers; more if the topic is broad) with type tag (survey/benchmark) + sub-theme + 1-sentence note (verbatim open-problem statement for surveys; key metric + reported number for benchmarks).

If fewer than 15 papers are available after 1a + 1b, proceed with what's available and note the limitation in the doc's Scope callout (e.g., "corpus limited to N papers due to topic specificity").

## Phase 2 — Convergence patterns

Identify cross-survey convergence patterns from the read content (multiple surveys diagnosing the same gap under different vocabulary). Format per the `> [!tip] Convergence patterns` callout in the Format reference below.

## Phase 3 — Clustering proposal

**Apply divergent-then-convergent thinking** — don't lock in the first clustering that comes to mind.

- **New / Update modes** (autonomous): generate 2–3 candidate clusterings internally (different ways to group the convergence patterns), evaluate each against criteria (cluster balance, theme coherence, density of cross-direction synergy), and commit to the strongest.
- **Plan mode** (interactive preview): invoke `Skill(skill="superpowers:brainstorming")` to refine the clustering collaboratively with the user before committing. Brainstorming's user-pause is appropriate here because Plan mode is itself an interactive preview.

Use Latin cluster letters (A/B/C/…) with cluster-prefixed direction labels (A1, A2, B1, …). For each cluster: theme name, directions under it, shared bottleneck, cross-direction synergy — present as the Cluster Overview table per the Format reference below.

## Phase 4 — Per-direction generation (Hinton-as-mentor advisory mode ON)

Per the agent's `## Persona — Hinton-as-mentor`: for each direction, **apply integrated thinking** — **first-principles** + **Hinton's research taste** (4 tenets) + **novelty** fire together. Generate the per-direction card following the canonical 8 sub-sections in the Format reference below; the Thesis row must follow the integrated thesis sentence template (also in the Format reference).

**Direction ideas must be novel** — iterate until the framing is non-consensus and defensible on first principles.

### Parallel dispatch (optional — large direction counts)

For **≥6 directions** where total wall-clock matters more than token cost, invoke `Skill(skill="superpowers:dispatching-parallel-agents")` for orchestration guidance, then dispatch one sub-agent per direction via the Agent tool (`subagent_type: research-assistant` or `general-purpose`). Each sub-agent prompt must include: direction title + cluster context + Phase 1c corpus *subset relevant to that direction* (not the full corpus — keep payloads tight) + the 8-section card template + Hinton-as-mentor persona engagement instruction. After parallel completion, assemble the returned cards in cluster order.

**Tradeoff**: parallel dispatch costs N× the corpus-read tokens (each sub-agent loads its own subset). For ≤5 directions or token-constrained sessions, generate sequentially within the parent context — the latency win is small and the tokens add up.

### Paper-adding workflow

When adding papers to a card (Evidence / Related research papers / Benchmarks):

1. **Vault search first** using the three methods (see Phase 1a): `obsidian-cli` for tag/property, `graphify` for concept-graph navigation, and `General/` topic → `knowledgehub-query` for topic-anchored content search.
2. `Skill(skill="alphaxiv-search")` for full-content reading of each candidate.
3. Write a 1-line framing: contribution + how it supports the direction.
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
grep -cE '^\| \*\*(Cluster|Thesis|Anchor surveys|Key targets)\*\*' "$DOC"

# Spine section checks (each should be 1)
grep -c '^> \[!abstract\] Overview' "$DOC"        # top-of-doc Overview callout
grep -c '^> \[!info\] Scope' "$DOC"               # Scope callout
grep -c '^## Methodology' "$DOC"                  # Methodology
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

# Per-card structural completeness — each direction must have all 8 sub-sections
# Flag-setting rules are gated by `label` so content outside direction blocks
# (Cross-Cutting Themes, Benchmark Gaps, etc.) cannot leak into the last direction's flags
awk '
  function emit() {
    if (!label) return
    ok = has_card && has_why && has_fp && has_ev && has_q && has_rel && has_bench && has_risk
    if (!ok) {
      m = ""
      if (!has_card)  m = m " card"
      if (!has_why)   m = m " why-it-matters"
      if (!has_fp)    m = m " FP-framing"
      if (!has_ev)    m = m " Evidence"
      if (!has_q)     m = m " Questions"
      if (!has_rel)   m = m " Related"
      if (!has_bench) m = m " Benchmarks"
      if (!has_risk)  m = m " Risks"
      print "  ✗ " label ": missing -" m
    } else {
      print "  ✓ " label ": all 8 sub-sections present"
    }
    label = ""
  }
  /^### [A-Z][0-9]+ —/ {
    emit()
    label = $2
    has_card = has_why = has_fp = has_ev = has_q = has_rel = has_bench = has_risk = 0
    next
  }
  /^## Cross-Cutting Themes/ { emit(); next }    # boundary: stop accumulating flags
  label && /^\| \*\*Cluster\*\*/                  { has_card = 1 }
  label && /\*\*Why it matters\.\*\*/             { has_why = 1 }
  label && /\*\*First-principles framing\.\*\*/   { has_fp = 1 }
  label && /\*\*Evidence\.\*\*/                   { has_ev = 1 }
  label && /\*\*Concrete research questions\.\*\*/ { has_q = 1 }
  label && /\*\*Related research papers\.\*\*/    { has_rel = 1 }
  label && /\*\*Benchmarks & metrics\.\*\*/       { has_bench = 1 }
  label && /\[!warning\] Risks/                   { has_risk = 1 }
  END { emit() }                                  # handles case where CCT is missing
' "$DOC"

# Audit verdict summary — convert raw counts to PASS/FAIL assertions
echo ""
echo "===== AUDIT VERDICT ====="
DIR=$(grep -cE '^### [A-Z][0-9]+ —' "$DOC")
FP=$(grep -c '^\*\*First-principles framing\.\*\*$' "$DOC")
RISKS=$(grep -c '^> \[!warning\] Risks' "$DOC")
ROWS=$(grep -cE '^\| \*\*(Cluster|Thesis|Anchor surveys|Key targets)\*\*' "$DOC")
THEMES=$(awk '/^## Cross-Cutting Themes/,/^## Benchmark Gaps/' "$DOC" | grep -cE '^> \[!tip\] ')
GAPS=$(awk '/^## Benchmark Gaps/,/^## Cross-References/' "$DOC" | grep -cE '^\| .*\| [A-Z][0-9]+')
MISSING_LINKS=$(grep -oE '\[\[[0-9]{4}\.[0-9]+' "$DOC" | sort -u | sed 's/\[\[//' | while read id; do [ -f "_KnowledgeHub_/${id}.md" ] || echo X; done | wc -l | tr -d ' ')

[ "$DIR" -eq "$FP" ]              && echo "✓ FP framing count matches direction count ($DIR)"             || echo "✗ FP framing $FP ≠ directions $DIR"
[ "$DIR" -eq "$RISKS" ]           && echo "✓ Risks callouts match direction count ($DIR)"                 || echo "✗ Risks $RISKS ≠ directions $DIR"
[ "$ROWS" -eq "$((DIR * 4))" ]    && echo "✓ Card rows = 4 × direction count ($ROWS)"                     || echo "✗ Card rows $ROWS ≠ 4×$DIR = $((DIR * 4))"
[ "$THEMES" -ge 3 ]               && echo "✓ Cross-cutting themes ≥3 ($THEMES)"                           || echo "✗ Cross-cutting themes $THEMES < 3"
[ "$GAPS" -eq "$DIR" ]            && echo "✓ Benchmark Gaps rows = direction count ($DIR)"                || echo "✗ Benchmark Gaps $GAPS ≠ directions $DIR"
[ "$MISSING_LINKS" -eq 0 ]        && echo "✓ All KH wikilinks resolve"                                    || echo "✗ $MISSING_LINKS missing KH wikilinks"

# Spine compliance — each required spine item must appear exactly once
SPINE_DRIFT=""
for h in "^> \[!abstract\] Overview" "^> \[!info\] Scope" "^## Methodology" "^## .*Survey Landscape" "^## Formal Framing" "^## Cluster Overview" "^## Cross-References" "^> \[!tip\] Convergence patterns"; do
  n=$(grep -cE "$h" "$DOC")
  [ "$n" -eq 1 ] || SPINE_DRIFT="$SPINE_DRIFT|  ✗ spine '$h' count=$n (expected 1)"
done
if [ -z "$SPINE_DRIFT" ]; then
  echo "✓ Spine compliance: all 8 required items present (7 H2 sections + Convergence callout)"
else
  echo "✗ Spine drift:"
  echo "$SPINE_DRIFT" | tr '|' '\n'
fi

# Size — informational only, not an assertion
wc -lw "$DOC"
```

Invoke `Skill(skill="superpowers:verification-before-completion")` for the evidence-before-claims gate: the **AUDIT VERDICT** block above must show all `✓` and the per-card completeness check must show `✓` for every direction. If any line is not `✓`, address the gap and re-run the audit. The verdict block is the completion contract.

## Exemplars

Defer to these for style after the Format reference: `_Projects_/Research-Directions-WAM.md` (3+3+2 cluster split, dedicated `## Formal Framing` section, definitional block-quotes in Formal Framing), `_Projects_/Research-Directions-Embodied-AI.md` (2+3+3 cluster split, concrete cross-direction synergy in Cluster Overview table). Use them for direction-card prose style and synergy-table density; defer to the Format reference (canonical) below for callout structure and the current spec.

---

## Format reference (canonical)

The canonical **Research-Direction Document Format** for `_Projects_/Research-Directions-*.md` docs. Strictly follow this spec.

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
2. `> [!abstract] Overview` callout — 2–4 sentence executive summary: how many directions, how many clusters, what corpus, what each direction surfaces (first-principles framing + non-consensus bet)
3. `> [!info] Scope` callout — detailed scope: corpus filter, exclusion criteria, methodology one-liner
4. `## Methodology` — bullets covering: Survey enumeration / Deep-dive mining / Filter / First-principles framing practice (add more bullets if the methodology warrants — these four are the minimum content)
5. `## <Domain> Survey Landscape` — 3-col table: `Survey | Sub-theme | Key open problems`, followed by `> [!tip] Convergence patterns` callout (at least 3 patterns, each enumerating ≥3 surveys; more if the corpus is broad)
6. `## Formal Framing` — math + tables defining central objects; block-quotes allowed here for *definitional* survey quotes only
7. `## Cluster Overview` — 4-col synergy table: `Cluster | Directions | Shared bottleneck | Cross-direction synergy`
8. `## Cluster A — <Theme>` (then B, C, …) — each opens with italicized 1-line framing, contains the per-direction cards
9. `## Cross-Cutting Themes` — at least 3 `> [!tip] <Insight Title>` callouts synthesizing across directions; each callout body references **≥2 directions** by label (otherwise it isn't cross-cutting), e.g., "A1, B2, C1 all rely on…". The callout title names the insight (e.g., "The Sim-to-Real Bottleneck Is Now Differentiable")
10. `## Benchmark Gaps` — 3-col table: `Gap | Direction | Existing closest` (1 row per direction)
11. `## Cross-References` — relative-path wikilinks to deep-dives, `General/`, KH

### Per-direction card (the heart)

Each direction is an H3 `### A1 — <Title>` followed by the structure below. **All 8 sub-sections in order; no skips.**

```markdown
### A1 — <Direction Title>

| | |
|---|---|
| **Cluster** | A — <Theme> |
| **Thesis** | <1 sentence — what to build/test and why it advances the domain> |
| **Anchor surveys** | [[id\|alias]], [[id\|alias]], [[id\|alias]] (at least 3 — the foundational surveys this direction anchors on) |
| **Key targets** | <concrete metric anchors with specific numbers: SR / latency / OOD %, etc.> |

**Why it matters.** At least 1 paragraph framing the gap — what's broken in the current state, why this direction resolves it. Reference anchor papers in prose with `[[id|alias]]` wikilinks.

**First-principles framing.**
- **First principle**: <the irreducible structure of the problem — what's necessarily true, independent of training distribution or convention>
- **Assumption being challenged**: <the conventional wisdom this direction breaks from — name WHO believes WHAT and the boundary the assumption hits>
- **The bet**: <the measurable, falsifiable prediction — must include specific numbers / thresholds (e.g., "ρ > 0.7", "≥30 Hz", "X pp gain over Y baseline")>

**Evidence.**
- [[id\|alias]] — 1-sentence framing of what this paper contributes to the direction's evidence base.
- (at least 4 bullets; foundational papers, not long-tail — list more if the direction has more foundational work)

**Concrete research questions.**
1. **Q1 — <Title>.** <specific, testable question; can include math>
2. **Q2 — <Title>.** ...
3. **Q3 — <Title>.** ... (at least 3 questions; can include math; list more if the direction has more testable questions)

**Related research papers.**
- [[id\|alias]] — <one-line contribution + gap this direction addresses>
- (at least 8 papers, inline-list format — NOT a 3-column table; list more if the related-work surface is broader)

**Benchmarks & metrics.**
- [[id\|alias]] — <what it measures, why it matters here, with specific numbers>
- (at least 3 benchmarks with measured numbers)

> [!warning] Risks
> - <Risk 1: specific failure mode> — <1-line consequence + mitigation hook>
> - (at least 3 risk bullets)
```

**Thesis sentence template.** The Thesis row's "1 sentence" must follow the integrated form below — one sentence packing taste + first-principles + novelty into a single thought:

> *"[Taste-attracting problem] has the irreducible truth that [first principle], which breaks the field's assumption that [conventional wisdom], and I bet that [measurable falsifiable prediction]."*

Filling all four blanks with substance *is* the integrated thinking. Iterate until each blank — particularly the bet with measurable numbers — fills substantively.

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
| **C** | Thesis row lacks the measurable bet (no specific number / threshold like `ρ > 0.7`, `≥30 Hz`, `+X pp`) | ✗ semantic | Iterate per First-principles framing rubric — the bet must include numbers |
| **D** | `**First-principles framing.**` block absent or filled with consensus restatement (three bullets don't carry distinct intellectual load) | ✓ presence only; semantic quality is a narrative gate | Apply the rubric's litmus test; if you can't fill all three bullets distinctly, drop the direction |
| **E** | Paper aliases fabricated or anchor surveys cited without arxiv IDs | ✗ semantic (audit catches missing-file wikilinks only) | Use exact alias from `_KnowledgeHub_/{ID}.md`; cross-check before adding |
| **F** | Related research papers presented as a 3-column table instead of inline bulleted list | ✗ semantic | Convert to `- [[id\|alias]] — contribution + gap addressed` bullets |
| **G** | Cross-Cutting Themes callouts reference only one direction label (not actually cross-cutting) | ✓ (per-callout direction-ref count <2) | Iterate to reference ≥2 directions per theme; if no ≥2-direction synthesis is possible, drop the theme |
| **H** | Benchmark Gaps without `Existing closest` column populated (just naming the gap with no current-state reference) | ✗ semantic | Add closest existing benchmark + brief delta from required scope |
| **I** | Per-direction Risks bullets lack mitigation hooks (just naming failures) | ✗ semantic | Add 1-line mitigation per risk — `Risk: X → Mitigation: Y` |
| **J** | Per-direction card missing one of the 8 sub-sections (most common: Risks dropped) | ✓ (per-card structural completeness check in Phase 7) | Restore the missing sub-section per the card template |

Patterns A–J should reach their canonical form before the Phase 7 verdict.

### Connective-tissue conventions

| Element | Convention |
|---|---|
| **Direction heading** | H3 `### A1 — Title` (em-dash, TOC-visible in Obsidian's outline pane) |
| **Direction labels** | Cluster-prefixed: `A1, A2, A3 / B1, B2, B3 / C1, C2, …` — cluster sizes and total direction count vary per doc (determined by the topic's research landscape) |
| **Cluster letters** | `A / B / C / …` (Latin); never Roman numerals |
| **Wikilink syntax in tables** | Pipe-escape: `[[id\|alias]]` |
| **Wikilink syntax in prose** | Plain pipe: `[[id|alias]]` |
| **Cross-doc refs** | Relative-path: `[[../Embodied-AI/NN_File]]`, `[[../General/NN_File]]` |
| **Math in prose** | Inline `$...$` or block `$$...$$` |
| **Block-quotes** | Reserved for *definitional* survey quotes in `## Formal Framing` only; no per-direction evidence quotes |
| **Callouts used** | `[!abstract]` (top-of-doc Overview), `[!info]` (Scope), `[!tip]` (Convergence patterns + each Cross-Cutting Theme with a titled insight), `[!warning]` (per-direction Risks). First-principles framing uses a bolded `**First-principles framing.**` label. |
| **Dates in prose** | Avoid explicit dates; the frontmatter has no `created` / `modified` fields either |
| **No cross-refs to `_Projects_/01_FirstPublication/`** | These docs are independent-study artifacts |
