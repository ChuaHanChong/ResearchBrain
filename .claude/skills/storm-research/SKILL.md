---
name: storm-research
description: Use when someone asks to run Storm Research, use the storm-research skill, run the STORM method on a topic, says "storm research this", "storm report on X", "give me a STORM briefing on X", or "storm review the research directions", or wants a multi-perspective, citation-verified HTML research briefing. The topic can be an external subject or an internal vault unit (a research-direction doc, a cluster, or a direction card), one unit at a time or as a batch. Runs the same 4-phase pipeline either way, with five expert lenses (Practitioner, Academic, Skeptic, Economist, Historian), then a contradiction map, a synthesized HTML report, and adversarial peer review with primary-source verification. Best when competing viewpoints and fact-checked claims matter; overkill for a simple factual lookup. For a plain multi-source research report without the five-lens panel or HTML briefing, defer to deep-research.
argument-hint: "[topic or vault unit to research]"
---

# Storm Research

## What this does

Turns one topic into a verified, multi-perspective HTML briefing. The topic can be an external subject ("storm research X") or an internal research document of this project such as a direction card, a cluster, or a whole doc ("storm review cluster B of the WAM doc"); the pipeline is identical either way, only the evidence base shifts (see the vault hook in Phase 1). It simulates five expert lenses on the topic, maps where they contradict each other, synthesizes everything into a single self-contained HTML report, then adversarially peer-reviews its own output and verifies every citation against its primary source before delivering.

Run the full pipeline end to end. Do not shortcut a phase. This is heavier than a quick web lookup; that is the point.

## Phase 0: Scope the topic

1. If `$ARGUMENTS` has the topic, use it. Otherwise ask what to research.
2. State your interpretation of the topic in one line and proceed. Only ask a clarifying question if the topic is genuinely ambiguous in a way that changes the research. Default to proceeding.
3. Identify the **reader's role** so the actionable section can target it. Infer it from the topic and any stated context; if unclear, ask in one line, or default to "a practitioner or decision-maker in this field." For an internal vault unit, default to "the researcher deciding whether to commit to this direction."
4. Derive a kebab-case `topic-slug` from the topic for the filename.
5. Tell the user the pipeline is running (5 lenses, then verify). One line.

## Batch runs (reviewing many units)

When asked to storm-review many units at once (e.g., every cluster and then its research directions in a doc, or a whole folder of direction docs):

- Run the full pipeline once per unit, each cluster before its directions, sequentially from the main conversation (a workflow engine may drive the units when the environment provides one); only the lens, verifier, and reviewer agents fan out.
- State the expected scale before launching and let the user confirm a large batch; skip the per-unit chat notes (Phase 0 step 5 and the Phase 1 convergence note).
- Output stays HTML: one template briefing per unit, with the unit's `topic-slug` derived as `{doc}-{unit}` (e.g., `docs/storm-reports/wam-cluster-a-briefing.html`, and `wam-a1-briefing.html` for direction card A1).
- At the end, do not auto-open every report or repeat the full per-unit chat summary; give one table in chat (unit, letter grade, verification tally, file path).

## Phase 1: Five expert lenses (parallel agents)

Spawn **five `general-purpose` agents in a single message** so they run concurrently. Each gets the SAME topic framing plus its own lens. Use these exact prompts, substituting `{TOPIC}` and a one-line `{TOPIC_FRAME}` (your Phase 0 interpretation):

**1. THE PRACTITIONER**: `You are THE PRACTITIONER for: {TOPIC} ({TOPIC_FRAME}). You work with this daily. Do real web research (prioritize recent sources, case studies, practitioner threads, operator data). Surface the GAP between what hands-on operators know and what academics/pundits miss, and the practical realities (workflow friction, what actually works, where it breaks) that get ignored. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each with a concrete data point/case/named source + URL. 3) THE ONE THING only a practitioner would say. Cite real sources with URLs. Under 400 words.`

**2. THE ACADEMIC**: `You are THE ACADEMIC for: {TOPIC} ({TOPIC_FRAME}). You care about peer-reviewed evidence and effect sizes, not anecdotes. Do real web research (peer-reviewed studies, arXiv, university and research-institute reports, journals). Answer: what does the rigorous evidence ACTUALLY say vs popular belief, and where does it CONTRADICT the hype. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each tied to a named study/report + URL with the actual finding/effect size. 3) THE ONE THING only an academic would say. Flag where evidence is thin or contested, and note peer-review status (published vs preprint). Under 400 words.`

**3. THE SKEPTIC**: `You are THE SKEPTIC for: {TOPIC} ({TOPIC_FRAME}). You think the mainstream view is overstated or wrong. Build the STRONGEST steelman bear case. Do real web research for backlash, failures, contradicting data, policy/regulatory changes, debunkings. Answer: the strongest counterargument, and what proponents conveniently ignore. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each with a concrete source + URL. 3) THE ONE THING only a skeptic would say. Be rigorous, not contrarian for sport. Cite real sources with URLs. Under 400 words.`

**4. THE ECONOMIST**: `You are THE ECONOMIST for: {TOPIC} ({TOPIC_FRAME}). You follow the money. Do real web research for revenues, valuations, market size, funding flows, unit economics, incentives. Answer: who profits from the current narrative, and what financial incentives shape the research and hype. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each with a real number (revenue/valuation/market size/funding) + named source + URL. 3) THE ONE THING only an economist would say (the follow-the-money insight). Cite real figures with URLs. Under 400 words.`

**5. THE HISTORIAN**: `You are THE HISTORIAN for: {TOPIC} ({TOPIC_FRAME}). You have seen disruption cycles before and look for patterns. Do real web research for genuine historical parallels (prior technologies, manias, market shifts). Answer: what parallels actually fit, and what we learn from how they played out (who won, who lost, what stabilized). Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each a specific historical case with dates/outcomes + a source URL. 3) THE ONE THING only a historian would say (the pattern no one else surfaces). Cite sources with URLs. Under 400 words.`

**Vault hook (optional).** Two cases, depending on what the topic is; when the needed resources are absent, skip silently.

- An external topic in an AI/ML/robotics area, in a project with `_KnowledgeHub_/` paper notes or alphaxiv MCP tools (`get_paper_content`, `answer_pdf_queries`): append one line to THE ACADEMIC's prompt: `Also draw on the local _KnowledgeHub_/{arxiv_ID}.md notes and alphaxiv MCP tools for papers already in the vault, and cite their primary arxiv sources.`
- An internal unit of this project (a research-direction card, a cluster, or a whole doc): prepend to EVERY lens prompt: `The topic is an internal research document. Read {DOC_PATH} (section {UNIT}) and its cited papers first (KnowledgeHub notes, then alphaxiv or arxiv for full content). Ground your position in what it actually claims, and use web research to hunt the external threats and prior art it missed.`

When all five return, post a 2-3 line note in chat: which way they converge, and the sharpest disagreement. Keep raw briefs out of chat (the agents already returned them).

## Phase 2: Map the contradictions

Working only from the five briefs, determine (do this inline, no agents):

1. **Direct conflicts**: where two or more lenses claim opposite things. Name the specific clashing claims, not just topics.
2. **Strongest vs weakest evidence**: which lens is best-supported (rank: peer-reviewed causal > official data > anecdote/analogy) and which is weakest, with why.
3. **The resolving question**: the single empirical question that would settle the biggest contradiction.
4. **Universal agreement**: what every lens confirms, even opponents. This is the likely-true load-bearing finding.
5. **The blind spot**: what NO lens addressed, and the open question it implies. This becomes the "missing 6th lens".
6. **The hidden connection**: two claims that appear to conflict and the non-obvious link that reconciles them, visible only when all five briefs are read together.

This map is not a separate deliverable. It is the raw material for the report's findings (supports/challenges), hidden connection, 6th-lens box, and frontier question.

## Phase 3: Synthesize the HTML report

1. Read `report-template.html` in this skill folder. Clone it; do not rebuild the CSS.
2. Fill every section. Mapping from the phases:
   - **60-second summary**: decision-maker-grade, nuance not headline. Lead with the settled fact, then the contested interpretation.
   - **5 key findings, ranked by reliability**: most important things now known, highest reliability first. Each carries a 1-10 confidence score (set in Phase 4) and Supported-by / Challenged-by chips drawn from the contradiction map. Map the score to the template's reliability label as 9-10 high, 7-8 medhigh, 4-6 medium, 1-3 low.
   - **Hidden connection**: the non-obvious link from Phase 2 that only appears across all five lenses.
   - **Key assumption / missing 6th lens**: the blind spot from Phase 2, framed as the lens that could change the conclusions.
   - **Actionable insight**: 3-6 specific moves for the reader's role identified in Phase 0. Specific, not abstract.
   - **Claim safety guide**: assert / caveat / avoid, populated after Phase 4 verification.
   - **Frontier question**: the one question that would change everything; pick the sharper of Phase 2's resolving question and the blind spot's open question, and mention the other in the why-it-matters paragraph.
   - **References**: every citation with a verification-status tag (set in Phase 4).
3. Write to `docs/storm-reports/{topic-slug}-briefing.html` when the project has a `docs/` folder (create `storm-reports/` inside it if needed); otherwise write to `storm-reports/` at the working directory.

## Phase 4: Adversarial peer review + verification (do not skip)

This is what separates Storm Research from a normal report. Run it before delivering.

**4a. Peer review.** Score each of the 5 findings 1-10 for reliability and justify. Identify the weakest link and what would verify it. Run a bias check (which lens dominated the synthesis, what got underweighted). Name the missing 6th perspective. Assign an honest overall letter grade. For a single external-topic briefing, do this yourself inline; for a batch or any vault review, hand it to a separate reviewer agent per unit, since fresh eyes grade harder.

**4b. Verify every citation (parallel agents).** Spawn `general-purpose` agents in one message, one per distinct citation cluster (group related claims; judge the number of clusters from the citation load). Each agent prompt:

`Independently verify each citation below against its PRIMARY source. Be skeptical; do not trust secondary blog summaries. CLAIMS (numbered): {one line per claim, each with the claim + cited figure + named source}. For each claim, find the actual primary source and confirm or correct: exact title/authors/venue/year/URL, the real figure or effect size as published, sample/method and any author-stated limits, and peer-review status (published vs preprint). For any contested claim, find the strongest credible counter-source. Return one block per claim: its number, VERDICT = CONFIRMED / PARTIALLY CONFIRMED (list corrections) / UNVERIFIED / FALSE, the corrected one-line citation, then 1-3 bullets of specifics with the primary URL. Under 120 words per claim.`

**4c. Apply corrections.** Edit the report:
- Write the final 4a confidence scores into each finding, with their mapped reliability labels.
- Fix any wrong figures, titles, dates, or mischaracterizations.
- Downgrade confidence scores where evidence turned out thin. Demote into the "Contested signal" sidebar, with a re-scored confidence, any claim that came back UNVERIFIED or drew a credible counter-source, plus, on external topics only, findings resting solely on a preprint. In an internal vault review, a verified preprint stays in the findings (see the reliability guardrail).
- Re-attribute single-survey or commissioned stats honestly.
- Fill the verification banner (`X fabricated, Y corrected, Z demoted`) and the per-citation status tags.
- Populate the claim safety guide from the verdicts.

## Output

1. Final deliverable: the briefing at the Phase 3 path (the v2, post-verification version).
2. Open it for the user with the platform's default opener (`open <path>` on macOS); if that is not possible, just give the path.
3. In chat, give: the file path, the overall letter grade, the verification tally (`N/N checked, X fabricated, Y corrected, Z demoted`), the one universal finding, the frontier question, and the claim safety summary (what is safe to assert vs avoid). Keep it tight.

## Notes & guardrails

- **Real research only.** Every lens and every citation must trace to a real, fetched source. No invented studies, numbers, or URLs. If a figure can't be verified, demote or cut it; never paper over it.
- **The panel is author-built.** Always disclose this in the report. Agreement across lenses is a strong hypothesis, not independent proof. Do not present convergence as consensus of the field.
- **Verification is mandatory.** A report delivered without Phase 4 is not a Storm Research report. The verification banner must be truthful.
- **Reliability = evidence quality, not confidence.** Score on the source hierarchy: peer-reviewed causal > official policy/financial data > single commissioned survey > analogy > preprint. In an internal vault review, a verified arxiv preprint is the primary literature of the field; judge it on its evidence rather than auto-demoting it.
- **Target the reader, not a default person.** The actionable insight and claim safety guide speak to the role identified in Phase 0.
- **Cost.** A run fans out multiple agents (the five lenses, the citation verifiers, and in batch mode a reviewer per unit). That is expected; scale the fan-out to what the topic needs, keeping the structure of five lenses and one verifier per citation cluster.
