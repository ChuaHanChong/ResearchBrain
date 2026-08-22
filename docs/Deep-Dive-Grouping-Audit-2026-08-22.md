# Deep-Dive Grouping Audit — 2026-08-22

**Status: FIXED (2026-08-22).** All 15 files' findings below were applied — ~150 relocations, ~15 subsection splits/adds, 3 cross-file paper moves, EVOLVER factual-error corrected, TOC resynced, verification pass clean (sequence integrity, KH links, cross-file anchors all confirmed).

Full content audit of all 15 in-scope `Embodied-AI/NN_*.md` deep-dive files (`02`–`16`; `01_Embodied-AI-101.md` excluded per convention). 15 parallel research-assistant subagents, each KH-verifying borderline bullets against `_KnowledgeHub_/{id}.md` Problem/Method sections rather than trusting curated bullet text. Read-only — no files edited.

**Verdict summary**

| File | Verdict | Headline issue |
|---|---|---|
| 02 Dataset-Benchmark-Environment | NEEDS-REWORK | 13 mismatches (tactile simulators, safety benchmarks, non-humanoid leaks) |
| 03 Imitation-Learning-and-RL | NEEDS-REWORK | §4.1 (62 papers) merges throughput-RL with scattered safety-filter/CBF papers |
| 04 VLA | NEEDS-REWORK | §5 (World-Model-Augmented) misfiles by surface vocabulary, not inference-time behavior; 4 orphan `[!star]` citations with no backing bullet |
| 05 VLA-Reasoning-and-CoT | NEEDS-REWORK | §1.1 (35 papers) doesn't match its own "same backbone, one pass" axis; 9 confirmed moves |
| 06 WAM | NEEDS-REWORK | 16 mismatches; §6.3 conflates agent-side abstention with WM-as-policy-evaluator (8 papers) |
| 07 Latent-World-Models | NEEDS-REWORK | §3.3 (32 papers) never implements its own stated 4-way sub-axis split |
| 08 Physics-Aware-Embodied-AI | NEEDS-REWORK | 13-paper asset-generation cluster has no `####` heading of its own; §4.2 bundles 2 mechanisms |
| 09 Robot-Memory | NEEDS-REWORK | 16 relocations, concentrated in §1.3, §3.2, §6.1 (recently-added papers, not the reworked §4/§5/§7) |
| 10 Manipulation-Skill-Learning | **MINOR** | Cleanest file — 8/774 bullets (~1%) mismatched |
| 11 Contact-Rich-and-Tactile-Control | NEEDS-REWORK | Confirmed stale orphan `[!tip]` callout (6 tips, 5 sections) from prior memory; §3.1/§4.5 oversized |
| 12 Whole-Body-and-Locomotion-Control | NEEDS-REWORK | §2.8 has swelled to 122 papers vs. its own documented ~48; 9-paper cluster belongs in `03` per the file's own routing rule |
| 13 Navigation-and-Mobile-Manipulation | NEEDS-REWORK | §2.1 (47 papers) claims "map-based" but ~11 members carry no map; SPINE has a `[!star]` slot but no bullet anywhere |
| 14 Egocentric-Pretraining-and-Human-Video | NEEDS-REWORK | 11 perception/forecasting **methods** mis-housed under a "Datasets" section |
| 15 Sim-to-Real-Transfer | NEEDS-REWORK | 16 mismatches; cross-embodiment-transfer papers leaking in via keyword overlap |
| 16 Self-Evolving-VLA-WAM | NEEDS-REWORK | EVOLVER's weight-update status misrepresented at 3 of 4 citation sites (factual error, not just placement) |

**14 of 15 files: NEEDS-REWORK.** Only `10_Manipulation-Skill-Learning.md` is MINOR. Total confirmed paper-level relocations across the vault: **~150+**. This is real regrouping work, not a cosmetic pass — every finding below was KH-verified against the paper's actual Problem/Method text, not inferred from bullet wording alone.

---

## 02 — Dataset-Benchmark-Environment

**13 MISMATCH**: CGP (§2.1, no dataset, drop), UniSim (§3.8→§3.6, delete empty §3.8), PyRoki (§4.1, kinematics not physics), DMC-VB + RL-ViGen (§5.1→§5.7), TacSL + DIFFTACTILE + Taxim (§6.2→new §6.3 "Tactile Simulators"), MetaFold (§7.1→§3.6), RoboFactory (§8.2, multi-robot not bimanual), MV-RoboBench (§9.1→§9.2), MonoArt (§9.1, pure 3D-recon method, remove), SafeRelBench (§9.4→§5.5).

**STRUCTURE**: MERGE §3.4→§3.2 (duplicate bullet), MERGE §10.2→§10.1 (1-paper subsection), fix §10.4's "§5.3"→"§5.4" cross-reference typo, rename §5.6 axis (currently Minecraft-only framing, holds non-Minecraft VisGym).

No file-scope issue — all 17 sections correctly data/sim/benchmark-scoped.

---

## 03 — Imitation-Learning-and-RL

**MISMATCH**: MMCD (1.1, off-domain driving-perception), Episodic-Memory-Manipulation (1.1, likely `09_Robot-Memory` multi-home), PARED (3.2, LLM-alignment IRL not robotics), Action-Flow-Matching (4.8→5.2), Agentic Execution RL (4.1→`16_Self-Evolving`), Laser-Tag-MARL / ClutterDexGrasp / Instant-Fold / SPADE / FTL-IGM (all 1.3, privileged-teacher-RL or zero-interaction methods that never clone a human demo — 1.3's core axis).

**STRUCTURE — SPLIT §4.1** (62 papers): the file's own Evolution Graph already separates "throughput" (SAC→BRO→FastTD3) from "cost-of-interaction/safety" (Recovery-RL→CBF-shielding) lanes, but the prose bucket doesn't. ~13 safety-filter/CBF papers scattered across 4.1+4.4 should consolidate into one new sub-axis.

**STALE-GROUPING**: 1.1's axis ("what matters for demo learning") doesn't cover ~8 single-task domain applications now filed there; 2.3's axis ("manufacture data") doesn't cover its curation/selection papers.

---

## 04 — VLA (largest file, 1821 lines, ~600 papers)

**Section 5 (World-Model-Augmented VLAs) is the worst offender in the vault**: ~1/3 of §5.3 and ~1/2 of §5.4 are misfiled by the same failure mode — filed on surface vocabulary ("video," "world model") rather than whether video-generation actually runs at inference. Cosmos-Policy, VideoVLA, DiT4DiT, VAG, MCSWIM, SDA, STARRY, MotuBrain all belong in §5.5 (joint denoising at inference) but sit in §5.3/§5.4 (deployment strips the video head). ViVa belongs in §6.2 (it's a value function, no action head). Duplicate bullet: FASTER appears verbatim in both §5.3 and §6.2 — delete the §5.3 copy.

**Data-integrity gaps (4 found)** — a `[!star]` Key Paper or decision-matrix citation with no backing L3 bullet anywhere in the section:
- DreamZero (§5, starred, zero bullets)
- Phys2Real (§11, starred + dm-11 headline, zero bullets)
- AwareVLN (§15, dm-15 + tip citation, zero bullets, no navigation subsection exists to hold it)
- VLA-0 (§18, starred as "Failure Frontier," never actually discussed in a failure-mode bullet)

**Other MISMATCH**: LA4VLA + AVP + BehaviorVLA (§1.4→§13.2/§4.6/§1.2), GuidedVLA + CRR-VLA + Semantic Anchoring (§3.3→§3.1/§1.2/§13.2), VLA-RFT + RIPT-VLA (§6.3→§6.2, both also incorrectly starred), EVOLVE-VLA (§9.3→§12.1).

**STRUCTURE — SPLIT §4.6** (15 papers, definition already lists 3-4 mechanisms in one sentence): 4 papers → §4.4 (VLA-as-tool-orchestrator), remaining 11 → "Affordance-Centric Prediction" vs "Symbolic Long-Horizon Planning."

**Coverage gap**: §13 (Safety/Robustness, ~62 papers, largest section) got no fresh KH sampling this pass — flag for dedicated follow-up.

---

## 05 — VLA-Reasoning-and-CoT

**§1.1 (35 papers)** claims "same backbone, zero new parameters, one forward pass" but is dominated by external LLM/VLM task planners (SayCan-lineage) — architecturally the opposite. 5 confirmed MISMATCH papers actually belong elsewhere (LLMPC→§4.2 model-based search, GLIMO/RoboBrain/World-Modeling-Makes-Better/Ro-SLM→training-time methods in §5 or §1.3). Two 5+ paper clusters inside §1.1 warrant their own subsections: **Safety-Aware Planning** and **Multi-Agent/Multi-Robot Orchestration**.

**§2.1 SPLIT**: bifurcates into discrete future-frame subgoal prediction vs. continuous visual-trace/trajectory CoT (3D HAMSTER, TrackVLA++, MolmoAct belong in the latter).

**Other moves**: Overthink-Triggered Slowdown Attack (§5.5→§7, it's an attack not a training method), R&B-EnCoRe (§6.1→§6.2, latency number contradicts its own tier).

---

## 06 — WAM (1276 lines, ~450 papers)

**16 confirmed MISMATCH**, most consequential: **§6.3 SPLIT** — 8 of its papers (RoboWorld, SC3-Eval, PiL-World, GE-Sim-2.0, StressDream, Video-WM-Policy-Eval, RefFree-PhysConsist, Admissibility Ladder) are WM-as-policy-evaluator / sim-free-ranking tools, a fundamentally different mechanism from the agent-side runtime-abstention papers §6.3 is named for (~40% of that subsection).

Other relocations: WorldDreamer (§2.1, pure video-gen, no home), ImageWAM + Mask2Real-WM (§2.2 wrong axis), GenReward + TADPoLe (§2.3, reward-shaping not data-gen), RISE-Video + Cosmos-Reason1 (§2.4, benchmark/MLLM not video-gen), GAIA-2 (§2.6), LLM-JEPA (§3.3, pure-language, arguably not WAM at all), EmbodiedVAE (§3.2, tokenizer not unified model), RigidFormer + MTS3 (§4.5, no planning component), Embodied-AI-LLM-WM-Survey (§5.1→§1.1), PhyAI + Embodied.cpp (§6.2, systems papers not planning/transfer methods), NavMorph (§7.2, test-time adaptation not self-play).

**STALE-GROUPING**: §4.7 (34 papers) has drifted into a broad MBRL catch-all spanning multi-agent RL, power-grid control, driving — tighten definition.

---

## 07 — Latent-World-Models

**§3.3 SPLIT** (32 papers): the section's own intro already names 4 sub-axes (algebraic-structured LAMs / dual-branch training / frozen-feature dynamics / unified diffusion) but implements none as headers — flat list contradicts its own stated taxonomy.

**6 MISMATCH**: JEPA-Slow-Features (§1.3→§3.6, pre-EMA precursor), Gen4U (§1.1, self-aware placement, needs reword not move), JEPA-WM (§2.2→§3.2, ablation study not new-capability paper), Autonomous-Learning-Framework (§3.1→§3.4, zero experiments), Percept-WAM (§3.1, zero JEPA content, already correctly homed in `06_WAM`), ATP-Latent (§4.1→§4.3, zero embodied eval), IDPP (§5.1→§5.3, cross-paradigm probe not latent-side method).

**Data-quality footnote**: §3.5's mini evolution-graph orders Motus→LaDi-WM, contradicting both arxiv chronology and the file's own top-level Evolution Graph.

---

## 08 — Physics-Aware-Embodied-AI

**STRUCTURE**: a 13-paper physics-grounded 3D asset-generation cluster sits inside §2.1 with no `####` heading of its own — promote to `2.2`, renumber current 2.2→2.3. **SPLIT §4.2**: bundles "LLM/VLM-proposer + simulator-verifier loops" (7 papers) with "bilevel-RL retargeting inside a simulator" (2 papers) under one mismatched definition.

**MISMATCH**: PhysiFormer + NeuROK (§2.1, self-flagged in their own bullet text as not-actually-Gaussian+MPM), Digital-Gene (§1.1, 4th "symbolic" axis value not covered by the section's own "Three Axes" callout).

**STALE-GROUPING**: §4.3/§4.4 (Koopman surrogates, statistical safety wrappers) don't match §4's "external simulator in the loop" framing — they replace or wrap around a simulator, not run one.

---

## 09 — Robot-Memory

**16 relocations**, concentrated in §1.3 (Manipulation Episodic Memory, 8 papers), §3.2 (VLA-backbone memory, 3 papers), and §6.1 (Failure-Driven Self-Evolution, 3 papers) — i.e., papers added since the last full pass, not the recently content-axis-reworked §4/§5/§7 (which held up well, except for 2 fresh §5 freshness-sweep additions: Language-Memory VLA and WorldScape Policy 2.0, both misfiled).

Notable: Kim Episodic Memory and IWR flagged as possibly not belonging in this file's control/planning-memory framing at all (conversational-HRI and training-time data-curation respectively).

**STALE-GROUPING**: §1.2 conflates pure-retrieval vs. dynamic-map-update (13 papers, split candidate); §6.1/§6.2's failure-triggered vs. general-trigger split is violated by 3-4 papers each direction.

---

## 10 — Manipulation-Skill-Learning — **MINOR**

Only file to clear the CLEAN/MINOR bar. 8 confirmed mismatches out of ~774 bullets (~1%): 5 generic grasp-perception papers wrongly filed under §2.3 "View-Robust &amp; Object-Centric" (recommend new `2.4 Generic Grasp-Pose &amp; Pick-Success Detection`), 3 supervised/imitation-trained motion planners violating §6.4's own explicit "auxiliary only, never the deployed policy" rule. §1.1's title should broaden beyond "diffusion &amp; flow-matching" to acknowledge its autoregressive/VQ-tokenized members (CARP, OAT).

25 of 30 sub-sections showed zero mismatches, including several fully-read small ones.

---

## 11 — Contact-Rich-and-Tactile-Control

**Confirmed a prior-memory finding still unresolved**: 6 `[!tip]` callouts vs. 5 `### N.` sections — the orphan tip ("Three Phases, One Architectural Convergence") lacks the `^insight-N` block-ID pattern every other tip uses.

**SPLIT §3.1** (33 papers, 3-30× larger than siblings): dedicated-sensor injection vs. sensorless/proxy (motor-current, torque-residual) force estimation — the bullets already make this distinction, structure doesn't. **SPLIT §4.5** (43 papers, largest subsection): in-hand dexterous reorientation vs. arm/bimanual visuotactile manipulation.

**MISMATCH**: CGP (§1.1, mischaracterized as sensor-free — KH confirms 4 Digit360 tactile sensors used), In-Hand-RMA (§4.5, paper's own claim is explicitly *proprioception-only*, no vision/touch), CTAM Soft Tail (§2.5, quadruped-tail gripper, not a dexterous hand).

---

## 12 — Whole-Body-and-Locomotion-Control (largest by paper count, 2610-word Evolution Graph, ~691 bullets)

**Single largest structural anomaly in the whole audit**: §2.8 "Legged Gait Learning &amp; Control Methods" has swelled to **122 papers — 2.5× its own documented size**. A 9-paper cluster of generic RL-algorithm contributions (evaluated only on HumanoidBench/MuJoCo gym, no locomotion-specific mechanism — one, a "humanoid" paper, is actually evaluated on Walker2d-v4) violates the file's *own stated routing rule* sending such papers to `03_Imitation-Learning-and-RL#6`.

**§1's intro names only 3 axes for 11 actual `#### N.N` sub-sections** — never updated as 1.4–1.11 were added.

**4 SPLITs** confirmed necessary: §1.1 (cooperative/multi-agent loco-manipulation cluster, 9 papers), §1.9 (conflates 3 mechanisms: generative-motion-tracker / FM-task-planner / reward-design), §1.10 (co-design vs. fixed-mechanism control), §1.11 (hardware platforms vs. flight-control-only research), §2's own top-level split (agile-skill-acquisition §2.1-2.6 vs. locomotion-substrate §2.7-2.10, different registers the current intro conflates), §3.3 (wearable data-collection hardware vs. standardized train→deploy workflows — only 3/15 papers match the stated axis).

**Confirmed cross-section MISMATCH**: HuBE (§1.4→§3.1, retargeting solver not zero-shot morphology policy).

Clean sections: §1.5, §1.8, §2.3, §2.4, §2.7, §2.9, and all of §4 (Open Problems).

---

## 13 — Navigation-and-Mobile-Manipulation

**§2.1 "Grounding &amp; Map-Based VLN" (47 papers) claims map-based grounding but ~11 members carry no persistent spatial representation at all** — SPLIT into explicit-map vs. grounding-without-a-map.

**Data-integrity**: SPINE has a `[!star]`/decision-matrix slot but **no canonical L3 bullet anywhere in the file**.

**Multi-touch move**: GN0 (§2.4→§4.4) has 5 dependent references (star, decision-matrix row, tip, §6.1 discussion, quick-reference matrix) — not a single-line fix.

**ADD-NEW-SUBSECTION**: 9-paper off-road/terrain-traversability cluster currently scattered across §1.2 and misfiled into §3.1 (COTRATE, CAT-Nav have zero LLM/language content despite sitting in "Semantic &amp; Cognitive Maps").

**Other**: RoboOcc (§3.4, zero humanoid-specific content, no clean file-internal home), Wheeled-Legged-NavLoco (§5.2, zero manipulation content, belongs in `12_Whole-Body`).

---

## 14 — Egocentric-Pretraining-and-Human-Video

**Largest structural finding**: **11 perception/forecasting method papers are mis-housed under Section 2 "Egocentric Datasets"** (subsections 2.6, 2.8, 2.9 — FRAME, EgoPoser, EgoPHI, Whareformer, EARL, Uni-Hand, EgoLoc, plus EgoHTR) despite Section 2's stated axis being "scale-modality-coverage trade-off" for actual datasets. Recommend renaming Section 2 and splitting into Datasets vs. Perception-Primitives clusters.

**5 confirmed MISMATCH in §5** (Hand→Gripper transfer): ImMimic + MimicDroid (§5.2, both explicit projection layers, contradicting "no projection layer" axis), SeeTraceAct (§5.2→§5.5, latent-trace family), Act-Sense-Act (§5.4, zero camera/viewpoint control despite "active vision" axis — the file's own cross-reference to `09_Robot-Memory` already half-admits this), HandEdit (§5.6, pure benchmark, no downstream policy SR reported).

**Orca (§6.2→§6.1)**: KH confirms zero action-prior training objective, action capability is emergent/zero-shot — directly contradicts §6.2's "run both objectives" axis.

---

## 15 — Sim-to-Real-Transfer (~430 papers)

**16 confirmed MISMATCH** across 8 of 24 subsections. Two new subsections warranted: "Event-Camera &amp; Non-RGB Sensor Simulators" (EVIS, EsaacSim, FracEvent, TIDES — currently split incoherently across §2.1/§2.2) and "Controller-Gain &amp; Parameter-Aware Adaptation" (Tune-to-Learn, DexCtrl, CoRMA — currently scattered, zero vision/DR content despite sitting in vision-focused §3.4/§3.1).

**Recurring pattern flagged**: cross-embodiment-transfer papers (Any2Any, Cross-Embodiment-Offline-RL) are leaking into this sim↔real file via keyword overlap ("transfer," "generalization") — below the 5-paper threshold for a dedicated fix, but worth a filing-discipline note.

§4.1 (Video/Scan→Twin Reconstruction, ~50 papers) is the largest subsection in the file — only lightly sampled, flagged as a watch-item for a deeper follow-up pass.

---

## 16 — Self-Evolving-VLA-WAM

**Cross-cutting factual error, not just misplacement**: EVOLVER (2510.16079) is described 4 different — mutually contradictory — ways across §1.1, §2.1, §3.3, §7.1. Three of the four claim "no weight updates occur"; the KH note confirms it explicitly runs GRPO (weight-level RL) as part of its method. Only §7.1's description is accurate. This propagates into §2.1's core definitional claim ("agent-side evolution... not raw weights") — **all 4 of §2.1's members actually contradict that claim** once checked (EVOLVER, ECHO, SEEA-R1, Dr.-Zero all do weight-level RL).

**Other MISMATCH**: SENSEI (§5.3, no self-play/replay, already correctly covered in §3.4/§4.4 — remove), Emergent-Self (§8.2, reports the *opposite* of a policy pathology — persistence, not collapse).

**SPLIT §5.3**: self-play data engines vs. continual-replay-against-forgetting, two distinct mechanisms bundled under one axis.

**STALE-GROUPING**: §4.2/§4.3's named strategies don't cover all their members (need a 4th/5th named strategy or broader framing).

---

## Recommended next step

This is too large to fix in one pass — ~150+ relocations, ~10 subsection splits, 2 confirmed structural bugs (11's orphan callout, several files' orphan `[!star]` citations), across 14 files. Suggest prioritizing by:
1. **Data-integrity bugs first** (cheap, high-value): 4 orphan-star citations in `04_VLA`, 1 orphan tip in `11`, 1 orphan star in `13` (SPINE), 1 duplicate bullet in `04` (FASTER).
2. **Factual-correctness bug**: EVOLVER's weight-update misdescription in `16` (affects reader understanding, not just filing).
3. **High-mismatch-density files**: `06_WAM` (16), `09_Robot-Memory` (16), `15_Sim-to-Real-Transfer` (16), `04_VLA` §5 (heaviest single-section rework).
4. **Structural splits**: `12`'s §2.8 (122 vs. documented 48 papers) is the largest single anomaly in the vault.
5. Everything else, file by file.
