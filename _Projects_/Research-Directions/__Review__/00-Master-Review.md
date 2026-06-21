---
title: Master Cross-Cutting Review of the Research-Directions Corpus
aliases:
  - Master Review
  - 00-Master-Review
tags:
  - review
  - research-directions
  - meta
---

> [!abstract] Executive summary
> This is the whole-corpus brief for a researcher deciding where to spend the next year. The agenda is **well-aimed but late**: across 78 directions, **zero are fully pre-empted**, yet **56 of 78 are only partially-pre-empted**, which means the carve is correct everywhere and the surviving novelty wedge is narrow and aging almost everywhere. Quality is uniformly high and uniformly bunched: grades cluster at B+/A- (62 B+, 26 A-, mean peer confidence 7.03/10), with no weak directions and no breakout A's. The single most important finding is a structural one that recurs in all 8 docs: **the durable, fundable asset is repeatedly the measurement artifact (the benchmark, the protocol, the diagnostic), not the proposed mechanism** — because every mechanism cell is filling within 6-12 months by compute-rich labs while the matched-comparison protocol nobody has run stays open. The corpus already half-knows this (every doc's reviewers independently route value to "own the protocol"), so the correct move is not to find new directions but to **promote the instruments from strategic nicety to primary deliverable** and to **commit the 5 still-whitespace A- bets**, while treating the 13 lowest-graded directions with care — though on a ground-truth re-check their flagged "defects" were almost all review-grounding artifacts, not card problems (see the RESHAPE list). The corpus's two deepest exposures are also shared: (1) it bets on *stacking/composing* mechanisms that the reviews repeatedly predict are either redundant or gradient-conflicting, and (2) its load-bearing thresholds sit below the statistical noise floor of a feasible real-robot trial budget, so several headline bets may be **unfalsifiable in practice** before they are wrong. Read the **COMMIT shortlist**, the **RESHAPE list**, and **Field-wide blind spots** before deciding; the blind-spots section is where the unclaimed opportunity actually lives.

## Methodology

103 units (25 clusters + 77 directions + 1 Focus synthesis) were each independently stress-tested by an analyst (5 adversarial perspectives + a contradiction map + a synthesis) and an independent peer reviewer (confidence 1-10 + a Stanford-prof letter grade), with every novelty claim probed against the live literature via alphaxiv. The 8 per-doc syntheses, the 78-direction + 25-cluster commit/de-risk/reshape ranking, and the per-unit `_verdicts.json` are the inputs to this master review. Numeric distributions below are precomputed from the verdict data, not recounted here.

## Headline metrics

| Slice | Tier | Novelty | Grades | Mean conf |
|---|---|---|---|---|
| **Directions + Focus (78)** | COMMIT 5 / DE-RISK 60 / RESHAPE 13 | whitespace 22 / partial 56 / pre-empted **0** | A- 19 / B+ 46 / B 10 / B- 3 | — |
| **Clusters (25)** | — | whitespace 8 / partial 17 | A- 7 / B+ 16 / B- 2 | — |
| **All 103** | — | — | A- 26 / B+ 62 / B 10 / B- 5 | **7.03 / 10** |

**Per-doc quality (avg grade, higher = better):** Embodied-AI 9.3 · WAM 9.3 · Locomotion 8.6 · Sim2Real 8.4 · Manipulation 8.4 · Whole-Body 8.2 · Spatial-4D 8.1 · Focus-Direction A-.

Interpretation: the **0 fully-pre-empted / 56 partially-pre-empted** split is the headline. It says the researcher's *taste* is excellent — every direction targets a real gap that the field has not closed — but the gaps are narrow and a single 2026 paper already occupies most of nearly every slot. The grade distribution is tightly bunched at B+/A- with no A's and almost no weak directions, which is the signature of a mature agenda: low variance, high floor, modest ceiling. The practical reading is that this portfolio will not be killed by a bad bet; it will be eroded by being second to publish on the mechanism. That is why the corpus-wide escape hatch (own the measurement) matters more than any single direction.

## The COMMIT shortlist — the 5 still-whitespace A- directions

These five are the only directions that are simultaneously **still-whitespace** *and* **A-**: they survive the live-literature probe and the reviewer grade together. Commit to each, gated on its one locking experiment.

1. **Embodied-AI · C2 — cross-embodiment invariant bake-off** (conf 7.8). A genuinely well-scoped *measurement* bet whose durable harness + diagnostic survives whoever wins the leaderboard. Survives because it is a benchmark, not a mechanism, so it cannot be scooped by GPUs. **Lock it:** add a sim-RL-tuning control *before* the interpolation control, and re-derive AnyBody's 0% extrapolation number with a properly tuned joint-space baseline (it may be an architecture artifact, not a law).
2. **Locomotion · A4 — joint embodiment-cost conditioning** (conf 7.6, highest in its doc). Premise is rock-solid and a real defensible core survives even after dropping the false "conditioning is necessary" headline: the FORCE cost axis nobody else has + the measured thermal-vs-acoustic curve + the amortization thesis. **Lock it:** retire the necessity headline up front and lead with the amortization result (one conditioned policy vs N specialist policies) plus the force-cost suite.
3. **WAM · A3 — bottleneck-type encoding sweep** (conf 7.4, the cleanest unit in WAM). The settled half (semantic > reconstruction) is a near-certain publishable floor; the live half (does bottleneck *type* matter on closed-loop SR) is genuinely unrun, and the experiment is the cheapest per unit novelty (encoder swap on a frozen backbone). **Lock it:** demote the predicted tie direction to "genuinely open," pre-register the null, and commit to the protocol (matched-capacity three-arm sweep), not to either outcome.
4. **Embodied-AI · B4 — geometric-forgetting law + selective protection** (conf 7.4). The H1 overlap-matrix diagnostic delivers a durable artifact regardless of whether the protection scheme wins, and the null result ("policies self-orthogonalize") is itself publishable. **Lock it:** promote external validity to a first-class step — measure subspace overlap on a *correlated* continual stream (repeated re-fine-tunes of one skill family), not just on the easy orthogonal case.
5. **Locomotion · A1 — perceptive gaze × generation fusion** (conf 7.4). Both pillars are proven on a real G1 and the fusion is genuinely unbuilt. **Lock it:** ingest and verify T-GMP (2606.06944) into KnowledgeHub first, disambiguate map-attention from gaze-generation, then run the matched-compute 2×2 with the H1 null pre-registered and the deploy-latency baseline corrected.

> [!note] Honorable mentions just outside the still-whitespace+A- intersection
> **Whole-Body C/C2** (wrench-aware certified safe set, A-/B+ still-whitespace) and **Whole-Body A/A1** (explicit arm→base reaction, A-/B+ still-whitespace) are the least-commoditizable bets in the Capability axis and are commit-grade *as formulation papers*; **Whole-Body D1** (contact-fidelity→SR regression, B+, conf 7.8) is the highest-confidence single direction in that doc. **Embodied-AI B2** (cross-episode memory + cause-attributed recovery, A-, conf 8.0) is the single highest-confidence direction in the corpus but is graded partially-pre-empted, so it lands in DE-RISK, not COMMIT — its safe core (diagnosis > uniform rollback, GTP-FA 11.2→76.8%) is endorsed by all five perspectives and stands even if H1 fails.

## The RESHAPE list — the 13 toughest-graded directions

These 13 got the lowest peer grades (B / B-). On a ground-truth re-check, the *specific* defect the review attributed to almost every one was a **review-grounding artifact** — the flagged paper is not in the card (it was pulled in by the analyst's literature probe), or the flagged number is actually correct — so **few of these need any card change**. The table gives the verified status and the only genuinely-actionable residual per row. (The one real source-doc item, Whole-Body A2's feasibility framing, has already been fixed in `Whole-Body.md`.)

| Direction | Doc | Grade | Verified status | Genuinely-actionable residual |
|---|---|---|---|---|
| **A4** manip-vs-loco latent split | Whole-Body | B | **Clean — not a reshape target.** Every WholeBodyVLA number (78.0% vs shared-LAM 66.0% = 12.0 pp; +38.7%; +24.0%; "not the primary factor") is confirmed in the real paper; the review trusted a sparse KH note that omits them | none |
| **A2** convex-hull frozen-primitive feasibility | Whole-Body | B- | **Fixed in source.** The "stays feasible" claim is re-grounded on SkillBlender's softmax ablation (convexity ≠ dynamic feasibility now noted); the "X-Loco 94.8%" keystone was review-introduced (not in the card) | none — done |
| **A2** physics-grounded reward framing | Sim2Real | B | **Card correct.** The card already benches TRIRL / **FLORA** / Robometer and names FLORA the falsifier — the "strawman foil" charge was the review's error | none |
| **C3** shared-channel bimanual force | Manipulation | B | **Card correct.** The card labels UME's 3.3× as "data-collection efficiency" (not sample-efficiency); the review's Finding 5 mis-used it | optional research idea: add a closed-form analytic internal-force projection as a comparator arm |
| **D1** cross-embodiment imitation transfer | Manipulation | B | **Artifact (favorable).** DIAL / LUCID are not in the card; correcting the mis-grounding *raises* D1 ("principle is consensus, cross-hand-cycle instantiation is unpre-empted") | none — re-reads as stronger than B |
| **D2** egocentric whole-body capture | Whole-Body | B | **Artifact.** The "80% vs 0%" / 2509.03222 is not in the card (review-introduced) | if you ever cite that result, mark it preliminary (N=5) |
| **B1** conditional-factoring stratification | Whole-Body | B | **Artifact.** EBench is not in the card; the briefing also mischaracterized it (it is 5-dimensional, not a binary flag) | optional: narrow the whitespace to continuous base-travel binning |
| **B2** 4D-consistency attribution | Spatial-4D | B | **Artifact.** 2606.01095 is not in the card (review-introduced phantom, cited there as if in-vault) | none to the card |
| **A2** occupancy world-model | Spatial-4D | B | **Artifact.** PointWorld (2601.03782) is not in the card; the ~8× latency misread was the briefing's, not the card's | none to the card |
| **B1** discrete dynamics-switch tactile WAM | Manipulation | B | **Artifact.** FAWAM (2606.08555) / T-Rex (2606.17055) are not in the card (review-introduced) | optional: add a genuinely-reactive baseline to the kill-test |
| **B3** multi-room out-of-view memory scaling law | Whole-Body | B | **Artifact (unverified pre-emption).** SOMA (2605.22283) is not in the card; the pre-emption was never read at granularity | optional: a quick SOMA read before treating B3 as pre-empted |
| **A2** causal-importance step weight | Embodied-AI | B- | **Artifact.** 2509.21154 / 2602.09331 are not in the card; the "citation inversion" and "thin margin" were in the briefing, not the card | none to the card |
| **E2** cross-sensor scaling law | Manipulation | B- | **Artifact.** The "five scaling-law papers" are not in the card (review-introduced) | optional: lead with the H2 "perception ≠ policy-SR" negative over the count-based scaling framing |

## Commit / de-risk / reshape ranking — all 78 directions

| # | Direction | Doc | Novelty | Grade | Conf | Tier | Lead de-risk move |
|---|---|---|---|---|---|---|---|
| 1 | C2 | Embodied-AI | still-whitespace | A- | 7.8 | **COMMIT** | Add a sim-RL-tuning control to the de-risk gate BEFORE the interpolation control: re-derive AnyBody's 0% with a properly tuned joint-space baseline |
| 2 | A4 | Locomotion | still-whitespace | A- | 7.6 | **COMMIT** | Retire the "conditioning is necessary to map the front" headline up front; lead with the amortization thesis (1× vs N specialists) |
| 3 | A3 | WAM | still-whitespace | A- | 7.4 | **COMMIT** | Stop asserting the tie direction: demote finding (iv) to "genuinely open," commit to the pre-registered protocol |
| 4 | B4 | Embodied-AI | still-whitespace | A- | 7.4 | **COMMIT** | Promote external validity to a first-class step: measure subspace overlap on a CORRELATED continual stream |
| 5 | A1 | Locomotion | still-whitespace | A- | 7.4 | **COMMIT** | Ingest/verify T-GMP 2606.06944; disambiguate map-attention from gaze-generation |
| 6 | B2 | WAM | still-whitespace | B+ | 7.8 | **DE-RISK** | Re-type H2: 0.822/0.94 are aggregate cross-policy correlations, not within-run monotonicity |
| 7 | D1 | Whole-Body | still-whitespace | B+ | 7.8 | **DE-RISK** | Harden the novelty check (GMR/BeyondMimic citation graph, confirm HDMI/2602.20220 off-axis) |
| 8 | A1 | Sim2Real | still-whitespace | B+ | 7.4 | **DE-RISK** | Run a minimum-detectable-effect / power analysis before any experiment (20 pp delta vs real-eval noise) |
| 9 | A2 | Locomotion | still-whitespace | B+ | 7.4 | **DE-RISK** | Correct headline number (OmniXtreme 91.08% overall, not 96.36%); resolve the rejection-vs-scale dichotomy |
| 10 | B1 | Embodied-AI | still-whitespace | B+ | 7.2 | **DE-RISK** | Verify 2605.07514 AUC 0.88 and MiraBench 48.7→12.8% before they anchor the recommendation |
| 11 | C1 | Spatial-4D | still-whitespace | B+ | 7.2 | **DE-RISK** | Confirm 2605.06388 is latent-only (preempts premise not head-to-head); demote scoop urgency |
| 12 | A2 | Manipulation | still-whitespace | B+ | 7.2 | **DE-RISK** | Add the H1 protocol-validity gate BEFORE H2 (FAAS-vs-joint-space on the exact held-out split) |
| 13 | A1 | Whole-Body | still-whitespace | B+ | 7.2 | **DE-RISK** | Source or down-rate the HEX "11/12→6/12" ablation (keystone of Finding 1, absent from vault) |
| 14 | D2 | Spatial-4D | still-whitespace | B+ | 6.8 | **DE-RISK** | Promote H4 (generated-object→sim-policy transfer) to a co-equal FIRST experiment |
| 15 | A3 | Sim2Real | still-whitespace | B+ | 6.8 | **DE-RISK** | Fix F3's phantom citation: ingest/verify 2604.14484 or drop the "formal failure theory" pillar |
| 16 | A3 | Manipulation | still-whitespace | B+ | 6.8 | **DE-RISK** | Stop citing twin-fidelity numbers (EMPM Chamfer 0.0082, PhysWorld 47×) as evidence for the bet |
| 17 | B2 | Whole-Body | still-whitespace | B+ | 6.8 | **DE-RISK** | Quantify the H3 in-view-dynamic-relocation regime BEFORE treating it as the escape hatch vs Mobi-π |
| 18 | C1 | Whole-Body | still-whitespace | B+ | 6.8 | **DE-RISK** | Re-anchor the latency claim (drop "WT-UMI 68 ms" as estimator-floor evidence) |
| 19 | C2 | Whole-Body | still-whitespace | B+ | 6.8 | **DE-RISK** | Verify or strike the F_ext formula: pull FAME's text or downgrade Finding 5 |
| 20 | D1 | Sim2Real | still-whitespace | B+ | 6.6 | **DE-RISK** | Cite GRAM's omitted L41 result (100% far-OOD hardware SR with robust-fallback engaged) |
| 21 | A5 | Locomotion | still-whitespace | B+ | 6.4 | **DE-RISK** | Verify/quarantine 2604.19102 before it carries the recommendation (single Gaussian policy?) |
| 22 | C3 | Manipulation | still-whitespace | B | 5.8 | **RESHAPE** | Re-attribute/drop the 3.3× (teleop speed not sample-efficiency); add analytic internal-force baseline |
| 23 | B2 | Embodied-AI | partially-pre-empted | A- | 8.0 | **DE-RISK** | Read SOMA's PDF (2603.24060): confirm memory is cross-EPISODE recurrence-keyed and attribution TYPED |
| 24 | FOCUS | Focus-Direction | partially-pre-empted | A- | 7.8 | **DE-RISK** | Verify ADAPT (2606.16542) with an actual paper read before recommending COMMIT/narrow |
| 25 | D3 | Manipulation | partially-pre-empted | A- | 7.8 | **DE-RISK** | Operationalize "emergent multi-phase dexterity" with a measurable threshold before committing |
| 26 | C1 | Embodied-AI | partially-pre-empted | A- | 7.6 | **DE-RISK** | Verify or drop the UniWM (2510.08713) comparator (benchmark scope, is memory online?) |
| 27 | B4 | Sim2Real | partially-pre-empted | A- | 7.6 | **DE-RISK** | Re-characterize RAFL as a STRUCTURED residual; restate as conservation-structure vs equivariance |
| 28 | D4 | Manipulation | partially-pre-empted | A- | 7.6 | **DE-RISK** | Decide explicitly: benchmark contribution (F3's tie kills it) or certification/guarantee (tie is the paper) |
| 29 | D3 | Whole-Body | partially-pre-empted | A- | 7.6 | **DE-RISK** | Rewrite H5's falsifier against the FINE-TUNED generalist (XHugWBC "fine-tune +10%"), not the frozen one |
| 30 | A1 | WAM | partially-pre-empted | A- | 7.4 | **DE-RISK** | Demote the Pri4R 'lean' to prior: +8.3 vs +13.2 is RoboCasa SR (not LIBERO-Plus OOD) |
| 31 | B2 | Manipulation | partially-pre-empted | A- | 7.2 | **DE-RISK** | Re-status F4 to recommendation; confirm CONTACT Disassembly exposes a distinct reversibility metric |
| 32 | A3 | Embodied-AI | partially-pre-empted | A- | 7.0 | **DE-RISK** | Ingest/verify PACT 2606.08414; demote finding #2 from "high reliability" to "needs verification" |
| 33 | A2 | WAM | partially-pre-empted | A- | 6.8 | **DE-RISK** | Correct Finding 2: FAWAM-w/o-Res is a with-sensor baseline; keep FD-VLA (61.1%) as sensorless |
| 34 | B1 | Sim2Real | partially-pre-empted | A- | 6.8 | **DE-RISK** | Promote causation from footnote to headline (within-object controlled reconstruction-degradation) |
| 35 | B3 | Sim2Real | partially-pre-empted | A- | 6.8 | **DE-RISK** | Promote gate metric-validity (Finding 5) to the primary endpoint (Δr vs ΔSR rank-correlation) |
| 36 | C1 | Manipulation | partially-pre-empted | A- | 6.8 | **DE-RISK** | Close provenance gap: Co-VLA / SAI+MonoDuo carry the aggressive claims but aren't in the vault |
| 37 | B3 | Embodied-AI | partially-pre-empted | B+ | 8.2 | **DE-RISK** | Rewrite finding #3: 2602.10377 = roofline+KKT template (LLM, NOT a VLA law) |
| 38 | A1 | Manipulation | partially-pre-empted | B+ | 7.6 | **DE-RISK** | Flag the unsourced "0.5-16.1% degradation" — cite the UniMorphGrasp table or mark as external |
| 39 | D2 | Manipulation | partially-pre-empted | B+ | 7.6 | **DE-RISK** | Re-ground finding 5 against the actual H1 test (goal-state-error on 2001.03070), not '+182% rotation' |
| 40 | B1 | Locomotion | partially-pre-empted | B+ | 7.6 | **DE-RISK** | Repair finding #2's "matched supervision": TERT-vs-RMA is also a supervision-target swap, not clean |
| 41 | B3 | Locomotion | partially-pre-empted | B+ | 7.6 | **DE-RISK** | Ingest LRN (2504.13149); cite as the reactive-mapless comparator row |
| 42 | A1 | Spatial-4D | partially-pre-empted | B+ | 7.4 | **DE-RISK** | Source Sparse2Act decoder-ablation numbers; is it a capacity sweep or an identity swap? |
| 43 | B2 | Sim2Real | partially-pre-empted | B+ | 7.4 | **DE-RISK** | Correct factual error: SLAT-Phys (2603.23973) IS cited 5×, not "does not cite" |
| 44 | C2 | Spatial-4D | partially-pre-empted | B+ | 7.2 | **DE-RISK** | Stop asserting GEM-4D delivers 'the same class of SR gains' (deltas over TesserAct, different base) |
| 45 | E1 | Sim2Real | partially-pre-empted | B+ | 7.2 | **DE-RISK** | Ingest SLowRL 2603.17092 — the single closest prior work the card is unaware of |
| 46 | E3 | Sim2Real | partially-pre-empted | B+ | 7.2 | **DE-RISK** | Vault 2605.28726 or stop citing; downgrade finding #2 (in-vault only TDQC action/logit) |
| 47 | E1 | Manipulation | partially-pre-empted | B+ | 7.2 | **DE-RISK** | Source-discipline finding (iv): promote FTF (2506.01944) to a real row or demote to hypothesis |
| 48 | A3 | Whole-Body | partially-pre-empted | B+ | 7.2 | **DE-RISK** | Vary α-schedule and base-state estimator JOINTLY, not estimation-fixed |
| 49 | D4 | Whole-Body | partially-pre-empted | B+ | 7.2 | **DE-RISK** | Resolve the D1/D4 OmniRetarget collision (D4-H4 treats it as pre-empting D1's surviving core) |
| 50 | B1 | WAM | partially-pre-empted | B+ | 7.0 | **DE-RISK** | Fix Finding 3 (3mm result not 0.1mm); make gate-vs-no-gate at 0.1mm the first deliverable |
| 51 | B3 | WAM | partially-pre-empted | B+ | 7.0 | **DE-RISK** | Resolve H5/WAM-RL contradiction: WAM-RL says pixel-MSE is the BEST reconstruction reward |
| 52 | B1 | Spatial-4D | partially-pre-empted | B+ | 7.0 | **DE-RISK** | Re-read VSP 2407.01863: it is "dual challenge," not "perception dominates"; H5 stays live |
| 53 | C3 | Spatial-4D | partially-pre-empted | B+ | 7.0 | **DE-RISK** | Resolve H5 self-contradiction (RGB-D "structurally disfavored" vs "RGB-D beats point-flow") |
| 54 | C1 | Sim2Real | partially-pre-empted | B+ | 7.0 | **DE-RISK** | Run per-cell variance/power check BEFORE the H1 correlation (bootstrap-CI width at REALM's N) |
| 55 | C2 | Sim2Real | partially-pre-empted | B+ | 7.0 | **DE-RISK** | Re-scope finding 2: pre-empts the budget heuristic, not the provable-CI estimand |
| 56 | C2 | Manipulation | partially-pre-empted | B+ | 7.0 | **DE-RISK** | Demote "structure = diversity" to a hypothesis; test with cheap coverage/entropy first |
| 57 | D2 | Sim2Real | partially-pre-empted | B+ | 6.8 | **DE-RISK** | Ingest/read Neural-Fly (2205.06908) before treating it as a missing baseline |
| 58 | E2 | Sim2Real | partially-pre-empted | B+ | 6.8 | **DE-RISK** | Run the decisive experiment first: fixed PACS/RAIL filter over frozen vs online-adapting policy |
| 59 | A1 | Embodied-AI | partially-pre-empted | B+ | 6.6 | **DE-RISK** | Resolve codebook-vs-continuous-latent confound (is CoLA-World's collapse VQ-specific?) |
| 60 | A3 | Spatial-4D | partially-pre-empted | B+ | 6.6 | **DE-RISK** | Reconcile CEO vs body on 3D-MIX (2603.24393); does its 9-scheme sweep nearly close H1? |
| 61 | C4 | Spatial-4D | partially-pre-empted | B+ | 6.6 | **DE-RISK** | Verify/down-rank F3: are Mem-World 2606.18960 / MEM action-conditioned control loops? |
| 62 | D3 | Sim2Real | partially-pre-empted | B+ | 6.6 | **DE-RISK** | Stop treating TacForeSight (2606.11184) as a second frozen-policy-correction witness |
| 63 | A3 | Locomotion | partially-pre-empted | B+ | 6.6 | **DE-RISK** | Correct CEO over-claim: PTDL (2606.08922)/Lu (2605.18611) don't run H4's inject-and-measure |
| 64 | B2 | Locomotion | partially-pre-empted | B+ | 6.6 | **DE-RISK** | Ingest Biased Dreams (2604.25416); soften "now contradicted" to "now threatened" |
| 65 | D1 | Spatial-4D | partially-pre-empted | B+ | 6.4 | **DE-RISK** | Verify SimRecon (2603.02133) / SPARK (2512.01629) — both KH-absent, single-source |
| 66 | B4 | WAM | partially-pre-empted | B+ | 6.2 | **DE-RISK** | Add a statistical-power calc before the 2×2 (n for a 15 pp inter-filter difference) |
| 67 | D2 | Whole-Body | partially-pre-empted | B | 7.6 | **RESHAPE** | Downgrade 2509.03222 from "80%-vs-0% settles H1" to "preliminary, underpowered (N=5)" |
| 68 | A2 | Sim2Real | partially-pre-empted | B | 7.2 | **RESHAPE** | Retract/verify the strawman: card already benches TRIRL/FLORA/Robometer, names FLORA falsifier |
| 69 | B1 | Whole-Body | partially-pre-empted | B | 7.0 | **RESHAPE** | Re-ground EBench novelty: it is five-dimensional, not a binary mode flag; restate as continuous binning |
| 70 | A4 | Whole-Body | partially-pre-empted | B | 6.8 | **RESHAPE** | Source or retract finding-#2 WholeBodyVLA quotes (66.0% / 12.0 pp / 'not primary factor') |
| 71 | B2 | Spatial-4D | partially-pre-empted | B | 6.6 | **RESHAPE** | Fix phantom citation 2606.01095 (cited as in-vault, absent from KH); ingest+verify |
| 72 | B1 | Manipulation | partially-pre-empted | B | 6.6 | **RESHAPE** | Verify FAWAM (2606.08555) / T-Rex (2606.17055) before commit; is T-Rex compositional/predictive? |
| 73 | A2 | Spatial-4D | partially-pre-empted | B | 6.4 | **RESHAPE** | Correct PointWorld latency (0.12s/10-step, not 0.1s/step); demote Finding 4 to hypothesis |
| 74 | B3 | Whole-Body | partially-pre-empted | B | 6.2 | **RESHAPE** | Read SOMA 2605.22283 at SERF granularity before treating as pre-emptor; revise Finding 3 |
| 75 | D1 | Manipulation | partially-pre-empted | B | 6.0 | **RESHAPE** | Correct finding (iii): DIAL off-axis, LUCID hand-to-gripper non-cycle — "partially pre-empted" mis-grounded |
| 76 | A2 | Whole-Body | partially-pre-empted | B- | 7.0 | **RESHAPE** | Ground or retract 94.8% X-Loco (2603.03733); confirm specialist-relative SR under single distillation loss |
| 77 | A2 | Embodied-AI | partially-pre-empted | B- | 6.6 | **RESHAPE** | Correct 2509.21154 citation inversion (it supports better-than-uniform); re-source the ~1pp margin |
| 78 | E2 | Manipulation | partially-pre-empted | B- | 6.4 | **RESHAPE** | Stop claiming "five scaling-law papers" (3 of 5 absent from vault, none cited); lead with H2 negative |

### Cluster-level grades (25 clusters)

| Cluster | Doc | Novelty | Grade | Conf | Lead fix |
|---|---|---|---|---|---|
| A | Embodied-AI | still-whitespace | B+ | 6.6 | Resolve the synergy premise before calling A a single cluster: run the three-loss co-training interference probe |
| B | Embodied-AI | partially-pre-empted | A- | 7.4 | Demote the Agia 2603.11400 pre-emption to 'unverified, conclusion-independent' (single-sourced, out-of-vault) |
| C | Embodied-AI | still-whitespace | B+ | 6.8 | Repair Finding 4: verify UniWM (2510.08713) imagines latent vs pixel; stop grouping with UNeMo/AstraNav |
| A | Locomotion | partially-pre-empted | B+ | 7.0 | Resolve the A4 contradiction (demote-to-theme vs promote-to-spine) by splitting A4 |
| B | Locomotion | partially-pre-empted | B+ | 6.4 | Correct Finding 1: TAR/SLR are B1-only, PrivilegedDreamer is B2-only — they do not span both tables |
| A | Manipulation | partially-pre-empted | B+ | 6.4 | Verify Dexonomy (2504.18829) before it carries verdict-weight (cross-hand transfer vs single-hand synthesis) |
| B | Manipulation | partially-pre-empted | B+ | 6.8 | Split finding 3: B1 = measurement/conjunction, B2 = genuine method delta (5-state + reversibility gate) |
| C | Manipulation | partially-pre-empted | B+ | 6.6 | Re-ground the SAI pre-emption: it is two-robot mobile collaboration, not single-platform bimanual |
| D | Manipulation | partially-pre-empted | B+ | 6.8 | Correct the D4 over-reach: rewrite the open cell to fragile gentle-force kPa/N ceiling over a learned policy |
| E | Manipulation | partially-pre-empted | B+ | 6.8 | Source or remove the "90-120% retention" figure (untraceable; makes E2 internally contradictory) |
| A | Sim2Real | still-whitespace | B- | 6.8 | Kill or fix finding 3: verify M3A 2512.01446 / GSWorld 2510.20813 do per-episode in-loop semantic re-sampling |
| B | Sim2Real | still-whitespace | B+ | 5.8 | Demote Findings 4 (throughput-binding) and 5 (open-loop fails) from declarative findings to labeled hypotheses |
| C | Sim2Real | partially-pre-empted | A- | 7.0 | Make the DE-RISK experiment attribution-grade: add source-heterogeneity-vs-physics-bias decomposition |
| D | Sim2Real | still-whitespace | B+ | 6.6 | Size the post-Cluster-B residual on the target legged task before committing to D1 |
| E | Sim2Real | partially-pre-empted | B+ | 7.2 | Fix the 2606.15366 framing: re-pose from "parameter vs action shift" (covered) to closed-loop FPR-preservation |
| A | Spatial-4D | partially-pre-empted | A- | 7.8 | Do not pre-decide A1→A3; make the Frontier comparison (explicit-point-head vs VLA-JEPA-latent) the experiment |
| B | Spatial-4D | still-whitespace | B- | 6.6 | Verify/retract the 2605.24642 "null result": its own KH note says geometry HELPS (75.2% vs 71.7%) |
| C | Spatial-4D | partially-pre-empted | A- | 7.4 | Wire Kairos into the Cluster C card as the latent-with-structured-persistence necessity-falsifier row |
| D | Spatial-4D | partially-pre-empted | B+ | 7.0 | Promote H3 (readiness sufficiency threshold below sim-accurate fidelity) to the headline |
| A | WAM | partially-pre-empted | B+ | 7.0 | Downgrade finding 2 to "table gap": add FAWAM (2606.08555, uncited + not-in-KH) to A2's Related table |
| B | WAM | partially-pre-empted | A- | 6.2 | Fix Fast-WAM provenance: the '91.8 vs 91.3 RoboTwin, 4× latency' corroboration is mis-attributed |
| A | Whole-Body | still-whitespace | A- | 7.6 | Promote the Frontier Question to gate: make contact-state instrumentation the PRIMARY arm (inertial vs contact) |
| B | Whole-Body | partially-pre-empted | B+ | 7.2 | Verify ESCAPE (2604.13633) against the actual paper before committing B3; add to the B3 Related table |
| C | Whole-Body | still-whitespace | A- | 7.6 | Quantify finding iv: put a bounded number on the expected sim anticipatory CoM-excursion reduction |
| D | Whole-Body | partially-pre-empted | B+ | 7.6 | Resolve F4: read GMR (2510.02252) / DreamGen Bench (2505.12705) — do they already report the fidelity→SR slope? |

## Global contradiction map

Six tensions recur *across* docs (not local to one card). Each is the same disagreement re-instantiated in different vocabulary, which is what makes them worth resolving once.

1. **Benchmark-saturation vs OOD-as-the-only-signal.** When in-distribution LIBERO-family sits at 97-98% (Embodied-AI §8; Spatial-4D, Manipulation, WAM all flag it), all discriminative power has migrated to OOD/real columns — but those columns are themselves either already-beaten by cited baselines (Embodied-AI A1's 79.5% target < World Pilot 84.7% / MoLA 92.7%), unanchored (B2's +5pp-over-HELM where HELM was never run), or below the binomial SE at n≈30-50 (Sim2Real A1/B3/C1/E1; WAM A1/A3/B4). The corpus leans on OOD as the deciding instrument while half the docs concede the OOD instrument cannot resolve the effect it is asked to decide.
2. **Single-mechanism-winner vs task-contingency (discrete-beats-continuous).** Manipulation A2 stakes its headline on "discrete grasp-taxonomy beats continuous FAAS," while Manipulation's own Historian voice (in B2, D4, A1) argues discrete/structured *always* loses on raw SR once continuous methods get data — and Locomotion A5's "Gaussian under-fits multimodal contact" is refuted by Cluster A's own "structure is the lever" thesis (Multi-Gait Gaussian humanoid, 2604.19102). The doc contains both the bet and its refutation and never reconciles them; the honest resolution (hybrid: discrete prior + continuous residual) is named in A2 finding (v) but rated lowest-confidence.
3. **In-imagination-rollout vs consumed-signal (does the dream pay its own freight).** Embodied-AI C1 asks whether online self-evolution is the *same computation* as latent dreaming (double-counting); WAM B3 finds WAM-RL's own ablation says pixel-MSE is the best reconstruction reward, contradicting its IDM-reward bet; A-cluster's whole synergy premise (stack A1+A2+A3 losses) is untested and may gradient-conflict because A3's physics loss lives in action-coordinate world space while A1/A2 ride latent tokens. The recurring question: when you compose imagination + evolution + memory, do they add, or is one already computing the other's output?
4. **Train-dense / deploy-light vs in-line latency.** Every doc agrees the latent substrate buys deployable latency (universal, §8) — but B2/B3/C1 (Embodied-AI), C1 (Whole-Body), A4/A1/A5 (Locomotion) all assert deployability without budgeting the integrated loop (cross-episode retrieval + diagnosis model + state machine, or fused dream+evolution+memory) against the 3-5 Hz control ceiling. The signal is dense at train time and the substrate is light, but the *integrated runtime* is never priced at control rate.
5. **Open-loop fidelity-correlation vs closed-loop feedback-gain (which estimand is binding).** Sim2Real A/B/C treat sim-real correlation (fidelity→transfer slope, per-factor r) as the binding object; D/E treat closed-loop feedback gain as the thing that makes that correlation irrelevant (a reactive policy insensitive to moderate inversion error → the open-loop monotone law measures the wrong quantity; a policy-agnostic conformal/reachability filter → a slowly-adapting policy injects no hazard and H1 vanishes). The same split appears as Embodied-AI's "is this a reward problem or an architecture problem" frontier. Half the corpus builds on open-loop correlation; the other half argues feedback dissolves it.
6. **Transfer-vs-generalist crossover (structured prior vs scale).** Whole-Body A1 bets explicit structure (analytic + learned arm→base coupling) beats HEX's implicit end-to-end MoE on fixed data; Whole-Body D3's own Historian argues every "cheap structured transfer beats scale" bet (LoRA, modular SLAM, hand features) wins briefly on a compute budget then loses to the foundation model (XHugWBC +10% fine-tune already shows the generalist is the cheap-transfer substrate). Focus-Direction is the same bet at program scale, and its Skeptic argues ADAPT (2606.16542) may already own the slot. The corpus repeatedly commits to the structured-prior side of a pendulum that its own reviewers say is swinging back.

## Universal agreements (likely true)

Findings that every perspective across every doc endorsed — treat these as the corpus's settled floor, not as bets:

- **LIBERO / in-distribution is saturated; score on OOD + latency.** Universal across Embodied-AI, Spatial-4D, Manipulation, WAM, Locomotion. In-distribution success rate no longer separates methods; the live axes are OOD generalization and deployable latency.
- **A latent (not pixel) substrate is what buys deployable latency.** The single most-endorsed first principle (WAM's capsule, Embodied-AI A1, Locomotion B2): what you imagine should be a compact control-relevant latent, and the imagination's grounding lives at train time.
- **Dense local per-step signal beats sparse outcome supervision.** Endorsed wherever it appears (Embodied-AI A1/A2/A3, Manipulation, WAM B): a per-step reward / per-LAW physics predicate / per-contact mode outperforms terminal success supervision — the contested part is only the *form* of the dense signal, never that dense beats sparse.
- **Diagnosis beats uniform rollback.** Embodied-AI B2's safe core (cause-attributed recovery, GTP-FA 11.2→76.8%) is endorsed by all five perspectives with real-hardware evidence; the field-wide reliability lesson is that *typed* failure attribution + targeted recovery beats blanket reset.
- **Constraints / physics-structure generalize OOD better than learned correlations.** Embodied-AI A3, Sim2Real A2 (R²=0.99 real-hardware GRF), Whole-Body C2 — a constraint or conservation law transfers where a fitted estimator does not. (This is the *floor*; the contested part is whether the explicit structure beats a well-tuned implicit baseline on a fixed budget — see contradiction 6.)
- **Own the protocol, not the commodity method.** Every doc's reviewers independently route durable value to the matched-comparison benchmark / diagnostic, because the mechanism cell fills within 6-12 months by compute-rich labs. This is the corpus's strongest cross-doc consensus and the spine of section 4's commit logic.

## Field-wide blind spots

This is the highest-value section: what NO direction in the corpus addresses, framed as opportunity. These are the systemic "missing 6th perspectives" the 103 reviews independently reinvented — counts are how many reviews flagged each.

1. **The Hardware/Sensor-Realist: "who pays for the sensor / what is the installed base" (flagged 37×, the single most recurring gap).** The entire corpus assumes geometry/force/tactile arrives clean and free, yet the sensing tax is worst exactly on the contact-rich/textureless/specular/occluded tail where every Finding-1 says geometry matters most (Spatial-4D §cross-pattern; Manipulation D4/E1/E2 force-observability; WAM A2 sensorless). **Opportunity:** a paper that *prices* the geometry-source — measures the SR-vs-sensing-cost frontier, or asks whether the explicit-geometry recommendation inverts once you charge for the second network/sensor that produces it — would underwrite a dozen directions and is itself novel.
2. **The Statistician / Power-realist: are the OOD margins even resolvable (21×, with statistical-power specifically 14×).** A1, B3, C1, E1 (Sim2Real) and A1/A3/B4 (WAM) all hinge on a >20pp / monotone-trend / per-cell-r effect that a feasible 10-50-trial real-robot budget cannot clear above binomial SE. **Opportunity:** a minimum-detectable-effect / design-of-experiments paper for embodied OOD eval — "how many trials to falsify a 15pp claim" — is a metrology contribution the field lacks and that every direction would cite.
3. **The Deployment-economist (21×).** B2/B3/C1 (Embodied-AI), C1 (Whole-Body), A1/A4/A5 (Locomotion) assert deployability without budgeting the integrated loop against the 3-5 Hz control ceiling; the deploy-relevant cost axis is repeatedly the wrong one (scan-FLOPs vs perception latency; heat-on-hours vs noise-on-per-step). **Opportunity:** an honest control-rate latency/compute budget for the *composed* system (retrieval + diagnosis + dreaming + memory) — most cards measure a component the robot never feels as a whole.
4. **The Safety/Calibration theorist: "what does the policy do when its imagination is confidently wrong" (14× safety + 14× calibration).** No direction in WAM, Embodied-AI, or Locomotion carries an uncertainty/abstention instrument; the dangerous failures are the unimaginable ones (recovery off the imagined-failure manifold), and a mis-calibrated train-time WM fails *silently* (collisions/drops with no halt). This is the same FPR-bound-preserved-through-the-loop hole flagged across the vault's runtime-monitoring audits. **Opportunity:** a calibration-under-self-induced-drift instrument is genuinely unbuilt and would be the natural companion to any dreaming/evolution direction.
5. **The Benchmark-validity metrologist: "is LIBERO saturated / is AnyBody's 0% a real floor" (11×).** AnyBody's 0% extrapolation may be an architecture artifact not a law (Embodied-AI C2); saturated LIBERO ID (~97%) and floored AnyBody (0%) may be unable to separate the very H4/H5 hypotheses the cards bet on. **Opportunity:** a benchmark-validity audit that establishes which existing suites can actually resolve the OOD hypotheses in play — this is the meta-instrument the whole COMMIT logic depends on.
6. **The Publication/Reviewer-economist (10×).** Several directions' true risk is not being wrong but being *second* on the mechanism; the corpus rarely reasons about reviewer incentives or scoop-timing explicitly. **Opportunity:** structuring each direction so its citable asset (the protocol/benchmark/diagnostic) is scoop-immune — exactly the move section 8 endorses — is both the safest publication strategy and under-instrumented across the corpus.

Two further cross-doc hazards, not "missing perspectives" but systemic flaws to fix before any commit:
- **Citation hygiene / phantom load-bearing papers.** In nearly every doc, a verdict-critical finding rests on a paper that is KH-absent, card-absent, or mis-identified (Sim2Real A2/A3/C2/D2/E1/E3; Spatial-4D B/B2/D1; Manipulation A1/B1/E2; Locomotion A1/A2/A3/A5/B2/B3; WAM A2/B4; Whole-Body A2/A4/B3/D2). Several "pre-empted" and several "still-whitespace" verdicts will move once the cited paper is actually read.
- **Closed-loop / post-contact / horizon-compounding regime.** The doc-wide bottleneck of Manipulation (and echoed in Sim2Real D/E, Spatial-4D C3/C4, Whole-Body): every direction optimizes a one-shot/steady-state quantity and is blind to the closed-loop regime where embodied tasks actually fail. No direction instruments *where in the trajectory* the imagined signal diverges under action feedback.

## Per-doc capsules

- **Embodied-AI — grade A- (quality 9.3).** A coherent, exceptionally self-aware nine-direction portfolio (dense per-step signal on a co-evolving latent / trained-VLA reliability loop / world-model dreaming + cross-embodiment invariants). Its signature flaw is that the headline is always a *mechanism* but the moat is always the *instrument*, and the cards bet on the mechanism. Held from a clean A by two shared bets: that composed cluster mechanisms cooperate rather than double-count or gradient-conflict, and that saturated/artifact-prone benchmarks can carry the headlines. Resolve those (run the interference ablation, promote the artifacts) and most of the portfolio is A-grade.
- **WAM — grade B+ (quality 9.3).** A tightly-themed agenda on one durable principle (imagine a compact control-relevant latent, grounded at train time) split into substrate-encoding (A) and train-time-signal (B). Uniformly *partially-pre-empted*: in six of seven units the mechanism is conceded and a single uncited 2026 paper sits on the cell, so value concentrates in the matched-capacity/iso-latency measurement apparatus. Shared calibration blind spot (nobody asks what the policy does when its imagination is confidently wrong) and pervasive unfalsifiable-margin risk. A3 and reframed-B3 are commit-clean; the rest need reshape.
- **Locomotion — grade B+ (quality 8.6).** Two clusters: humanoid whole-body skill acquisition (A) and quadruped state-inference + mapless navigation (B). Every direction sits on an uncontested mechanism floor and makes a narrow second-order bet that a fresh 2026 paper contests in every single case, so the durable value lives in the benchmark/diagnostic, not the method. Two A- directions (A1, A4); systematic safety/hardware-survival blind spot; load-bearing threats sit un-vaulted in over half the directions.
- **Sim2Real — grade B+ (quality 8.4).** The most coherent causal decomposition in the set: forward semantic randomization (A) → real-to-sim inversion (B) → sim-as-evaluator validity (C) → deploy-time residual adaptation (D) → safety wrappers (E). Three A- clusters (B1, B3, B4) where the framing is already disciplined to defensible whitespace. Held below A- by a systemic pattern: load-bearing claims are unmeasured statistical/identifiability premises, the Metrologist voice is missing nearly everywhere, and downgrades rest on un-vaulted phantom citations.
- **Manipulation — grade B+ (quality 8.4).** The most mechanically self-aware Capability doc: one honest meta-thesis (the continuous substrate is settled; only discrete/hard/structural wedges are live), nineteen units each staking the paper on a single un-run A/B. Two genuinely strong bets (D3, D4) and a clear repeated insight (own the protocol). Held below A- by three liabilities: the closed-loop/post-contact blind spot, verdict-critical findings resting on unsourced/mis-identified external papers, and a self-contradiction it states but never resolves (half its discrete/hard bets are predicted to lose by its own Historian).
- **Whole-Body — grade B+ (quality 8.2).** The most physically-grounded Capability doc: four clusters all attacking base/leg ↔ arm dynamic coupling (explicit reaction A / factored mobile-manip B / certified balance-under-load C / cross-embodiment transfer D). Two strong still-whitespace anchors (C/C2, A/A1) and the highest-confidence single direction in the review (D1, 7.8). Held below A- by a contact-and-actuation blind spot (the "whole-body" object is repeatedly formalized as a rigid-body/kinematic floating-base-manipulator with the legs assumed away) and an evidentiary-sourcing problem (load-bearing numbers in the card, not the vault).
- **Spatial-4D — grade B+ (quality 8.1).** The highest-ceiling doc: one thesis (externalized geometry, not appearance, is the durable substrate for action) pressed through twelve directions, almost all B+ with two A- clusters (A, C). Taste is good and questions are sharp, but novelty has thinned — every direction is partially-pre-empted, each shadowed by a single 2026 paper. Real risk: it repeatedly recommends a strategic shift (A1→A3, "geometry is settled") *ahead of* the one experiment it concedes would decide it, and several load-bearing citations are miscited or phantom. The unpriced geometry-source/sensing tax is the hidden variable deciding every bet.
- **Focus-Direction — grade A-.** A single-bet document collapsing the whole program into one wager: the off-diagonal inertia cross-term (arm reach *is* a base disturbance) should be an explicitly predicted feedforward quantity, not a residual the part-wise policy absorbs. Physically textbook-correct with a genuinely cheap self-falsifying M0-6 sim experiment — that falsifier is the real asset. Held from A by an over-claimed headline (41%→62% is borrowed from a different comparison; true delta ~+3pp), a novelty core possibly pre-empted by ADAPT (2606.16542, anticipatory-vs-reactive being the surviving sliver), and an inherited hardware-contact-dynamics blind spot.

## Closing note

`Focus-Direction-Paper-Code-Index.md` is an **infrastructure paper↔code index**, not a research-direction document: it carries no thesis sentence, no first-principles bet, and no falsifier, so it was excluded from this thesis stress-test by design. It is a navigation artifact for the corpus, not a unit of it, and its quality should be judged as a maintained index (coverage, accuracy of the paper↔repo mapping), not against the research-direction format. The 103 units stress-tested here are the 25 clusters + 77 directions + 1 Focus synthesis; the repo map is correctly outside that count.
