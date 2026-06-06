---
title: "Promising Research Directions: Manipulation — Grasping, Contact, Coordination, Dexterity"
aliases:
  - "Manipulation Research Directions"
  - "Manipulation Promising Directions"
tags:
  - research-directions
  - manipulation
  - dexterous
  - grasping
  - tactile
---

# Promising Research Directions: Manipulation — Grasping, Contact, Coordination, Dexterity

> [!abstract] Overview
> Fourteen manipulation research directions across five clusters — *Grasping & Grasp Synthesis* (A), *Contact-Rich Assembly & Precision* (B), *Bimanual & Dual-Arm Coordination* (C), *Dexterous & In-Hand Control* (D), and *Tactile Foundations & Data Substrates* (E). Synthesized from ~20 manipulation/dexterous/tactile surveys and benchmarks plus the frontier methods that set each bet's bar ([[2506.17198|Dex1B]], [[2604.11674|AffordSim]], [[2602.23253|SPARR]], [[2512.23864|DreamTacVLA]], [[2511.05275|TwinVLA]], [[2603.04531|PTLD]], [[2603.15789|OmniReset]], [[2602.16710|EgoScale]]). Clusters A–D treat touch as an in-task signal (predicted, coupled, bounded); Cluster E is the foundation layer beneath them — where sensor-free force-awareness (E1) and the cross-sensor representation (E2) come from before any task. This is the **Manipulation subsystem** (arms + hands on objects) of a 2-axis doc family. It excludes locomotion and whole-body loco-manipulation (sibling Locomotion and Whole-Body docs own those) and cross-references the mechanism docs ([[Embodied-AI|Embodied-AI]], [[WAM|WAM]], [[Sim2Real|Sim2Real]]) for tool-use, policy learning, imagination, and physics-grounding. Each direction states the irreducible truth, the assumption it breaks, and a measurable bet — chosen where impactful work deviates from "more data / more scale." Every number is sourced from a cited `_KnowledgeHub_/{ID}.md` note, never invented.

---

## Methodology

**Scope.** Corpus: ~20 manipulation/dexterous/tactile/bimanual surveys and benchmarks plus ~70 method papers from `_KnowledgeHub_/`, cross-checked against [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] and the `Embodied-AI/` deep-dives ([[02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]], [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]], [[05_VLA|05_VLA]]). Surveys name the open problems, benchmarks fix what is measurable, frontier methods fix what is currently achievable. **Subsystem boundary**: locomotion and loco-manipulation coupling belong to sibling docs; tool-use and policy learning (BC/diffusion/VLA) are cross-referenced to the umbrella, not re-clustered; deformables are a single direction inside Grasping (A3), not their own cluster.

- **Survey enumeration**: tag-scan over `survey` × {`manipulation`, `dexterous`, `tactile`, `VLA`, `world-model`} surfaced [[2504.03515|Dexterous IL Survey]], [[2511.02097|WM Manipulation Survey]], [[2604.04974|Video-to-Control Survey]], [[2507.10672|VLA Manipulation Survey]], [[2508.13073|Large VLM-based VLA Survey]].
- **Deep-dive mining**: full reads of [[09_Contact-Rich-and-Whole-Body-Control#3. Force-Conditioned VLA Architectures|09_Contact-Rich-and-Whole-Body-Control §3]], [[09_Contact-Rich-and-Whole-Body-Control#8. Open Problems & Failure Modes|10 §8]], [[02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks|02_Dataset-Benchmark-Environment §6]], [[02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02 §8]], [[05_VLA#8. Humanoid & Bimanual VLAs|05_VLA §8]]; 3+-way convergence seeded B1, C3, D2.
- **Closest-baseline anchoring**: each bet is pinned to the strongest existing method it must beat ([[2506.17198|Dex1B]], [[2604.11674|AffordSim]], [[2512.23864|DreamTacVLA]], [[2602.23253|SPARR]], [[2511.05275|TwinVLA]], [[2603.04531|PTLD]], [[2603.15789|OmniReset]]).
- **Filter (quality-gated)**: a direction is admitted only if it is a distinct sub-problem, has a KH-sourced measurable bet, a non-consensus framing, and ≥1 vault anchor. **A non-prehensile cluster was assessed and dropped**: only [[2503.16806|DyWA]] has a note, failing the ≥2-anchored gate — DyWA is folded into B as a dynamics-adaptive anchor instead.

---

## Manipulation Survey Landscape

| Survey | Sub-theme | Key open problems |
|---|---|---|
| [[2504.03515\|Dexterous IL Survey]] | A: Grasping & dexterity | Data sparsity; generalization gaps; sim-to-real; real-time control; safety; hand-design × tactile coupling under-explored |
| [[2506.18448\|GraspMAS]] | A: Grasping & dexterity | Language-driven grasp detection brittle; zero-shot open-vocab grasp reasoning; no contact-quality grounding |
| [[2507.10672\|VLA Manipulation Survey]] | A/B: VLA manipulation | Scarcity of datasets combining high task complexity + multimodal richness; simulation physics-fidelity vs throughput trade-off |
| [[2508.13073\|Large VLM-based VLA Survey]] | A/B: VLA manipulation | Monolithic-vs-hierarchical fragmentation; RL / world-model / human-video integration immature; force/tactile under-specified |
| [[2604.04974\|Video-to-Control Survey]] | B: Contact & control interface | Integration layer is the critical gap; latent-action identifiability; pre-execution verification; tactile/force integration named explicitly |
| [[2511.02097\|WM Manipulation Survey]] | B: Contact & precision | Structured task-relevant (object-centric) representations; physics-awareness ranked 3rd of 13 capabilities; hierarchical long-horizon |
| [[2502.05086\|REASSEMBLE]] | B: Contact & precision | Insert is the hardest action (highest failure); long-horizon contact-rich assembly lacks standardized multimodal benchmarks |
| [[2603.15469\|RoCo Challenge]] | B/C: Assembly & coordination | Sim-to-Real Cliff; sub-millimeter precision; coordinated bimanual; failure-recovery curriculum data > parameter count |
| [[2604.05831\|BiCoord]] | C: Bimanual coordination | Long-horizon tightly-coupled spatial-temporal coordination; precise alignment; degradation in later stages of multi-stage tasks |
| [[2407.07788\|BiGym]] | C: Bimanual coordination | Long-horizon multi-object bimanual; sparse-reward; IL/RL near-0% on stacking + long sequences |
| [[2506.18088\|RoboTwin 2.0]] | C: Bimanual data | Synthetic-data quality control; superficial domain randomization; embodiment-aware grasp adaptation for heterogeneous dual-arm kinematics |
| [[2605.16257\|DexJoCo]] | D: Dexterous & in-hand | Limited task diversity for multi-fingered hands; multi-task training degrades vs transfers; language grounding lacks true generalization |
| [[2510.25725\|HumanoidVTA]] | D: Dexterous & in-hand | Dense tactile is discriminative but current optimization can't leverage it; soft-object contact control unsolved |
| [[2604.27621\|Robot Learning from Human Videos Survey]] | E: Tactile foundations & data | Action-oriented transfer; tactile/audio/gaze incorporation named (1 of 7 open problems); low-quality-video robustness; continual learning |
| [[2604.15395\|Foundation Models in Robotics Survey]] | E: Tactile foundations & data | Tactile/failure-data scarcity (top-3 bottleneck); embodiment-agnostic action spaces; physics-informed WMs |
| [[2510.24795\|Efficient VLA Survey]] | E: Tactile foundations & data | Data-collection cost; internet-scale human video named as a dominant data lever; self-sustaining data; embodiment-agnostic |
| [[2604.16592\|Cognition WM Survey]] | E: Tactile foundations & data | Tactile-perception under-represented; epistemic WMs over structured knowledge; meta-cognition under-developed |

> [!tip] Convergence patterns
> - **The integration layer, not the policy, is the bottleneck** (5-way): [[2604.04974|Video-to-Control Survey]] (integration is the critical gap), [[2603.15469|RoCo Challenge]] (Sim-to-Real Cliff), [[2502.05086|REASSEMBLE]] (insert dominates failures), [[2604.05831|BiCoord]] (late-stage degradation), [[2407.07788|BiGym]] (near-0% on long-horizon). Same diagnosis, different words: the hard part is connecting a prediction to dependable contact, not making the prediction. Confirmed by [[2602.23253|SPARR]] (sim + real residual → 95–100% [AutoMate](https://arxiv.org/abs/2407.08028)) and [[2407.16677|ResiP]] (residual RL, peg-in-hole 5%→99%).
> - **Force is consumed as input, never modeled as output** (4-way): [[2604.04974|Video-to-Control Survey]], [[2511.02097|WM Manipulation Survey]] (physics 3rd of 13 capabilities), [[2504.03515|Dexterous IL Survey]] (tactile under-leveraged), [[2510.25725|HumanoidVTA]] (dense tactile discriminative but unused). Now being inverted: [[2512.23864|DreamTacVLA]] (95.0% Peg-in-Hole) and [[2603.19201|OmniVTA]] imagine the contact future.
> - **Bimanual data scarcity forces a choice: generate it or avoid needing it** (4-way): [[2506.18088|RoboTwin 2.0]], [[2410.24185|DexMimicGen]], [[2604.05831|BiCoord]], [[2407.07788|BiGym]] all hit the dual-arm data wall. Two answers: scale generation ([[2506.18088|RoboTwin 2.0]] +24.4% few-shot) vs compose single-arm priors ([[2511.05275|TwinVLA]] 76% on ~50 episodes).
> - **Dexterity comes from exploration breadth + distillation, not bigger nets** (3-way): [[2603.15789|OmniReset]] (diverse resets, 25% real vs 4% DP), [[2603.04531|PTLD]] (privileged distillation, +182% rotation), [[2210.13702|DeXtreme]] (auto domain randomization, 27.8 vs 14.8). The lever is reset/randomization diversity and the privileged→deployable interface, not parameter count.

---

## Formal Framing

**The manipulation action-generation object.** A manipulation policy maps observation $o$ (vision $v$, proprioception $q$, optionally tactile $\tau$) and instruction $l$ to an action $a$ (arm pose / joint command, plus finger commands for dexterous hands):

$$\pi: (v, q, \tau, l) \mapsto a, \qquad a = (a_{\text{arm}}, a_{\text{hand}})$$

Manipulation is distinguished from locomotion by the **contact-state** $\mathcal{C}$ — the set of object–effector contact points, their forces, and modes — which is the latent the action must regulate. Three cluster-specific contact formalisms organize this doc:

| Object | Formalism | Cluster |
|---|---|---|
| **Grasp-pose distribution** | $G \sim p(g \mid v, l)$ — a distribution over 6-DoF (parallel-jaw) or high-DoF (dexterous) grasp poses, scored by a quality + task-affordance metric $Q(g)$ | A |
| **Contact-mode sequence** | $c_{1:T}$, $c_t \in \{\text{free, making, in-contact, sliding, breaking}\}$ — a discrete trajectory through contact modes, each with mode-conditional continuous dynamics; assembly is reaching a target $c_T$ | B |
| **In-hand contact state** | $s_t = (R_{\text{obj}}, \{f_i\}_{i=1}^{n})$ — object orientation $R_{\text{obj}}$ and per-fingertip force/contact $f_i$, evolving under finger-gaiting; reorientation is driving $R_{\text{obj}} \to R_{\text{goal}}$ while maintaining stable $\{f_i\}$ | D |

**Grasp synthesis as conditional generation** — [[2506.17198|Dex1B]]:

> "An iterative data generation pipeline … combining an efficient optimization method to create a high-quality seed dataset with a generative model for massive data scaling … incorporates geometric constraints (SDF-based loss) during training and employs a lightweight post-optimization step to ensure the physical plausibility and success of generated hand poses." — [[2506.17198|Dex1B]]

The grasp generator $p(g \mid v)$ must satisfy a **feasibility constraint** (SDF non-penetration + force-closure) the loss can enforce directly — why generation + post-optimization beats pure regression, and why A1 makes the *task-affordance* score $Q(g)$, not just stability, the conditioning target.

**Contact as a first-class predicted quantity** — [[2603.05687|CGP]]:

> "[Models] often predict kinematic trajectories without explicit contact semantics … CGP … predicts coupled future trajectories of both actual robot state and expected tactile feedback … translated into physically consistent, executable target robot states." — [[2603.05687|CGP]]

This reframes contact-rich manipulation from "predict actions, hope contact works out" to "predict the *contact-state trajectory* $c_{1:T}$ jointly with the action" — what B1 and B2 build on, and the inverse of force-as-input.

**Coordination as a non-factorizable joint** — [[2604.05831|BiCoord]]:

> "Tasks specifically designed for long-horizon and tightly coordinated bimanual manipulation … a 4× increase in spatial-temporal integral values vs prior benchmarks; policy performance consistently degraded in later stages." — [[2604.05831|BiCoord]]

Two-arm coordination carries a joint action $a = (a_L, a_R)$ whose value is *not* $V(a_L) + V(a_R)$ — the cross-arm coupling (handover timing, force balance) is the load-bearing term, why C1 treats coordination as native structure, not two independent policies.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Grasping & Grasp Synthesis** | A1, A2, A3 | Generating *task-relevant, feasible* grasps that transfer across objects/morphologies | A1's affordance-scored grasp distribution is what A2 keeps invariant across hands; A3 stresses both on deformables where the grasp-pose is ill-defined; [[2506.17198\|Dex1B]]'s feasibility-constrained generation is the shared substrate |
| **B — Contact-Rich Assembly & Precision** | B1, B2 | Sub-millimeter contact where vision is blind and the policy is open-loop | B1's predicted contact-state trajectory is what B2 conditions its discrete-mode dynamics on; sensor-free deployment of both lives in [[#E1 — Sensor-Free Force-Aware Policies\|E1]]; [[2602.23253\|SPARR]]'s real residual and [[2512.23864\|DreamTacVLA]]'s tactile imagination are shared |
| **C — Bimanual & Dual-Arm Coordination** | C1, C2, C3 | Two-arm coupling is non-factorizable and bimanual data is scarce | C1's coordination-native policy needs C2's generated data; C2 must respect the coupling C1 models; C3 adds the tactile channel that makes force-balanced handovers observable; [[2511.05275\|TwinVLA]] and [[2506.18088\|RoboTwin 2.0]] set the bar |
| **D — Dexterous & In-Hand Control** | D1, D2, D3, D4 | Multi-fingered contact is high-DoF, discontinuous, sim-to-real-fragile | D1's cross-morphology action space is what D2 deploys onto; D3 supplies the behaviors D1 unifies; D4 bounds all three with QP/force-safety; [[2603.04531\|PTLD]]'s distillation and [[2603.15789\|OmniReset]]'s reset diversity are the shared levers |
| **E — Tactile Foundations & Data Substrates** | E1, E2 | Contact-rich, multi-modal data scarcity (4-order gap vs [[2310.08864\|OXE]]) — the substrate A–D consume tactile *from* | E1 deploys force-awareness with no runtime tactile sensor (ego-video pretraining or teacher-distillation); E2's cross-sensor encoder makes any such policy portable across platforms, and is what D2's deployable estimator inherits |

---

## Cluster A — Grasping & Grasp Synthesis

*Generating task-relevant, physically feasible grasp poses that transfer across object categories and hand morphologies — including where the grasp-pose itself is ill-defined (deformables).*

### A1 — Task-Affordance-Conditioned Grasp Synthesis

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | The right grasp depends on what the object is *for*, not just its shape. The field assumes scaling stable-grasp data ([[2506.17198\|Dex1B]]'s 1B demos) eventually yields task-competent grasping; it does not — stable and functional are different objectives. The bet: condition the grasp generator on a task-affordance score $Q(g)$ and beat generic stable-grasp estimators by [[2604.11674\|AffordSim]]'s margin (79% vs 15% medium / 64% vs 3% hard), recovering ≥93% of manual-annotation success without per-object labels. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2507.10672\|VLA Manipulation Survey]], [[2506.18448\|GraspMAS]] |
| **Key targets** | [[2604.11674\|AffordSim]] 79% (medium) / 64% (hard) vs AnyGrasp 15% / 3%, ≥93% of manual-annotation success without annotation; match [[2506.17198\|Dex1B]] 86.0% DexGraspNet at task-relevance parity; [[2505.03233\|SynGrasp-1B]] ~90% real zero-shot as the open-vocab reference |

**Why it matters.** The dominant recipe scales stable-grasp data: [[2506.17198|Dex1B]] generates a billion physically-plausible grasps, [[2505.03233|SynGrasp-1B]] pre-trains on a billion synthetic frames for ~90% real zero-shot. But [[2604.11674|AffordSim]] shows the limit — generic estimators "select stable but functionally irrelevant grasps," and AnyGrasp collapses to 15% / 3% (medium/hard) where affordance-guided collection reaches 79% / 64%. The grasp that *holds* a hammer is not the grasp that *uses* it. [[2601.07060|PALM]] and [[2506.18448|GraspMAS]] reason about affordance to pick a grasp, but as a separate stage, not as the generative conditioning. The move: make the task-affordance score $Q(g)$ the conditioning variable of $p(g \mid v, l)$, so the generator never proposes functionally-wrong grasps.

**First-principles framing.**
- **First principle**: A grasp's correctness is set by the task, not force-closure alone — the same mug affords a rim-grasp for drinking and a handle-grasp for carrying. Quality is a *conditional* $Q(g \mid \text{task})$; a generator that ignores the task optimizes the wrong objective.
- **Assumption being challenged**: That scaling stable-grasp data closes the task-competence gap. [[2506.17198|Dex1B]] and [[2505.03233|SynGrasp-1B]] bet on scale; [[2604.11674|AffordSim]]'s 15%→79% gap shows more *stable* grasps don't make *functional* grasps — the data axis is orthogonal to the difficulty.
- **The bet**: An affordance-scored generator beats generic estimators by [[2604.11674|AffordSim]]'s margin (79% vs 15% medium, 64% vs 3% hard) and recovers ≥93% of manual-annotation success without annotation, at [[2506.17198|Dex1B]]-class stability (86.0% DexGraspNet) — task-relevance for free, no stability loss.

**Evidence.**
- [[2604.11674|AffordSim]] — Open-vocab 3D affordance (VoxAfford) guides two-stage grasp selection; 79%/64% medium/hard vs AnyGrasp 15%/3%, recovers 93% of manual-annotation success; the affordance-vs-stable existence proof.
- [[2506.17198|Dex1B]] — Feasibility-constrained generative grasp synthesis (CVAE + SDF loss + post-optimization); 86.0% DexGraspNet, 96% sim-to-real; the scalable stable-grasp substrate to condition.
- [[2505.03233|SynGrasp-1B]] — Billion-frame synthetic grasp pre-training with Progressive Action Generation (2D box → 3D grasp CoT); ~90% real zero-shot, 93.3% language-conditioned; open-vocab reference.
- [[2601.07060|PALM]] — Affordance predictor (object relevance + contact geometry + motion) + progress signal; +17.7 pp CALVIN ABC→D; affordance as reasoning, not generative conditioning.
- [[2506.18448|GraspMAS]] — Multi-agent zero-shot language-driven grasp detection; reasoning-heavy, no contact-quality grounding.

**Concrete research questions.**
1. **Q1 — Affordance as generator conditioning vs post-filter.** Condition [[2506.17198|Dex1B]]'s CVAE on [[2604.11674|AffordSim]]'s VoxAfford latent so $p(g \mid v, \text{affordance})$ proposes only task-relevant grasps; ablate vs affordance-as-filter — does conditioning beat filtering on the hard-tier 3%→64% gap?
2. **Q2 — Joint quality $Q(g) = Q_{\text{stable}}(g) \cdot Q_{\text{task}}(g)$.** Train a unified scorer combining force-closure ([[2506.17198|Dex1B]]'s Q1-score) and affordance relevance; does the product score recover ≥93% manual-annotation success without annotation?
3. **Q3 — Dexterous vs parallel-jaw affordance transfer.** Does an affordance-conditioned generator transfer from parallel-jaw ([[2505.03233|SynGrasp-1B]]) to high-DoF hands ([[2506.17198|Dex1B]]) — i.e., is task-affordance morphology-invariant while stable-grasp geometry is not? (Feeds A2.)
4. **Q4 — Language-to-affordance grounding without grasp labels.** Use [[2506.18448|GraspMAS]] / [[2601.07060|PALM]]-style language reasoning to produce the affordance map that conditions generation — closing the open-vocab loop with zero grasp annotation.

**Related research papers.**
- [[2604.11674|AffordSim]] — Affordance-aware generator + 50-task benchmark; 79%/64% vs 15%/3%; the affordance-conditioning anchor.
- [[2506.17198|Dex1B]] — 1B-demo feasibility-constrained generation; 86.0% DexGraspNet; the stable-grasp substrate to condition.
- [[2505.03233|SynGrasp-1B]] — Billion-frame synthetic pre-training, open-vocab; ~90% real zero-shot; the stability-scaling reference to beat.
- [[2601.07060|PALM]] — Affordance reasoning + progress signal; +17.7 pp CALVIN; affordance as a separate stage, not conditioning.
- [[2506.18448|GraspMAS]] — Zero-shot language-driven grasp via multi-agent reasoning; no contact-quality grounding.
- [[2604.11320|CLASP]] — Dual-pathway open-vocab grasping; 87.0% pick SR; stability-centric.
- [[2511.04357|GraSP-VLA]] — Graph-based symbolic long-horizon grasp planning; symbolic, no generative synthesis.
- [[2605.05925|DexSynRefine]] — HOI prior + task-space residual RL; 68.1% sim, +50–70 pp real over retargeting; complementary synthesis-then-ground.

**Benchmarks & metrics.**
- [[2604.11674|AffordSim]] — 50-task benchmark; 79%/64% vs 15%/3%, real zero-shot 24% avg; the affordance-difficulty gradient (placing 40% → hanging 10%).
- DexGraspNet (via [[2506.17198|Dex1B]]) — 86.0% SR, Q1-score 0.125; the stable-grasp floor A1 must not sacrifice.
- [[2604.11320|CLASP]] — 87.0% pick SR in clutter; the open-vocab geometric-grounding baseline.

> [!warning] Risks
> - **Affordance accuracy is the ceiling** — [[2604.11674|AffordSim]] notes VoxAfford accuracy is the primary success factor. → Bound to tasks where the affordance model is reliable; report the affordance-quality vs grasp-success curve.
> - **Stable-grasp regression is already strong** — [[2505.03233|SynGrasp-1B]] hits ~90% on generic grasping. → Score on affordance-critical tasks (pouring, hanging, tool-use), where the 15%→79% gap lives.
> - **Affordance and stability can conflict** — the functional grasp may be less stable. → Make $Q$ a tunable product, not a hard constraint; expose the trade-off as a Pareto front.

### A2 — Cross-Morphology Grasp Transfer

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | A grasp's *function* (oppose-and-close) is the same across hands; only its joint-space geometry differs. The field assumes each new dexterous hand needs its own dataset and policy. The bet: a function-aligned action space transfers grasp-establishment zero-shot to unseen hands at [[2603.22264\|UniDex]]'s 60% (Oymotion) / 40% (Wuji), at ≥5× lower per-hand data cost and [[2505.21864\|DexUMI]]-class in-domain SR (86%). (A2 transfers the *grasp*; D1 transfers the *in-hand control cycle* that follows — distinct phases, distinct bets.) |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2508.13073\|Large VLM-based VLA Survey]], [[2605.16257\|DexJoCo]] |
| **Key targets** | [[2603.22264\|UniDex]] 81% task progress + zero-shot 60% (Oymotion) / 40% (Wuji), 5.2× data-cost cut; [[2505.21864\|DexUMI]] 86% cross-hand SR + 3.2× collection efficiency; [[2605.16257\|DexJoCo]] DP-T 50.4%→20.0% under randomization as the negative-transfer floor |

**Why it matters.** [[2504.03515|Dexterous IL Survey]] names the embodiment gap — "wide variation in DoFs, morphology, and kinematics prevents data and policy transfer" — and [[2603.22264|UniDex]] confirms foundation policies "predominantly cater to parallel-jaw grippers, leaving dexterous manipulation underserved." Every new hand restarts data collection. But the gap is bridgeable: [[2603.22264|UniDex]]'s Function-Actuator-Aligned Space (FAAS) reaches 60%/40% zero-shot at 5.2× lower cost, and [[2505.21864|DexUMI]]'s exoskeleton interface hits 86% across underactuated and fully-actuated hands. The claim: a grasp's *function* (opposition, enclosure, precision-pinch) is a low-dimensional invariant, and a policy parameterized in function-space transfers where a joint-space policy cannot. This direction owns the **grasp-establishment** phase — forming a stable, task-appropriate contact set — scored on grasp-transfer SR.

**First-principles framing.**
- **First principle**: A grasp is defined by its functional configuration (which surfaces oppose the object, at what force), not the joint angles that realize it. Grasp taxonomy (power / precision / lateral) is a low-dimensional invariant across hands; joint-space realization is the high-dimensional hand-specific projection.
- **Assumption being challenged**: That each dexterous hand needs its own dataset and policy. The field collects per-hand because it parameterizes in joint-space; [[2603.22264|UniDex]]'s FAAS and [[2505.21864|DexUMI]]'s relative-finger actions show function-space representations transfer — the per-hand-data assumption is a parameterization artifact.
- **The bet**: A function-aligned action space transfers zero-shot to unseen hands at [[2603.22264|UniDex]]'s 60% / 40% and cuts per-hand data cost ≥5× ([[2603.22264|UniDex]] 5.2×, [[2505.21864|DexUMI]] 3.2×), at [[2505.21864|DexUMI]]-class in-domain SR (86%) — transfer for free, no in-domain regression.

**Evidence.**
- [[2603.22264|UniDex]] — Function-Actuator-Aligned Space unifies control across hands; 81% task progress, zero-shot 60%/40%, 5.2× cost cut; the function-space anchor.
- [[2505.21864|DexUMI]] — Human-hand-as-interface via robot-specific exoskeleton + visual inpainting; 86% across Inspire + XHand, 3.2× efficiency; relative-finger actions transfer.
- [[2506.17198|Dex1B]] — 1B grasps across three hands; cross-hand data, but per-hand policies.
- [[2605.05925|DexSynRefine]] — HOI prior + task-space residual; 68.1% sim, +50–70 pp real over retargeting; task-space action is the transfer enabler.
- [[2605.16257|DexJoCo]] — 11-task benchmark; multi-task training *degrades* for current policies — the negative result motivating function-space.

**Concrete research questions.**
1. **Q1 — Function-space vs joint-space ablation.** Train a grasp policy in [[2603.22264|UniDex]]'s FAAS vs raw joint-space; does function-space recover 60%/40% zero-shot on a held-out hand where joint-space yields ~0%?
2. **Q2 — Grasp taxonomy as the latent.** Parameterize by a power/precision/lateral grasp-type latent + continuous force; does the discrete bottleneck beat continuous FAAS on transfer?
3. **Q3 — Exoskeleton-normalized vs retargeted data.** Compare [[2505.21864|DexUMI]]'s exoskeleton against kinematic retargeting ([[2605.05925|DexSynRefine]]'s max-5.8% baseline) for cross-hand data quality.
4. **Q4 — Why does multi-task dexterous training degrade?** [[2605.16257|DexJoCo]] reports negative transfer; test whether function-space parameterization converts it into transfer.

**Related research papers.**
- [[2603.22264|UniDex]] — Universal hand control via FAAS from ego video; 60%/40% zero-shot, 5.2× cost cut; the function-space anchor.
- [[2505.21864|DexUMI]] — Human hand as universal interface; 86%, 3.2× efficiency; exoskeleton-normalized transfer.
- [[2605.05925|DexSynRefine]] — Task-space residual RL grounds HOI; +50–70 pp real over retargeting; task-space action.
- [[2506.17198|Dex1B]] — 1B grasps over three hands; cross-hand data, per-hand policies.
- [[2605.16257|DexJoCo]] — 11-task benchmark; multi-task degradation negative result.
- [[2604.20689|FingerEye]] — Per-finger eye-in-hand perception; morphology-specific sensing.
- [[2603.04531|PTLD]] — Privileged tactile latent distillation; +182% rotation; the deployable interface a transferred policy needs (feeds D2).
- [[2512.24653|RoboMIND 2.0]] — 310K trajectories, six embodiments; cross-embodiment data substrate.

**Benchmarks & metrics.**
- [[2603.22264|UniDex]] — 81% task progress on 5 tool-use tasks, zero-shot 60% / 40%; the cross-morphology transfer metric.
- [[2605.16257|DexJoCo]] — 11-task MuJoCo dexterous suite; DP-T 50.4%→20.0% under randomization, π0.5 highest; the degradation diagnostic.
- [[2505.21864|DexUMI]] — 86% across underactuated + fully-actuated hands; the in-domain SR floor.

> [!warning] Risks
> - **Function-space loses fine dexterity** — fine manipulation may need joint-level control. → Use function-space for grasp-establishment, joint-space residual for fine in-hand (couples to D1).
> - **40–60% transfer is not deployment-ready** — [[2603.22264|UniDex]]'s Wuji 40% is a research result. → Frame as a few-shot seed; report the few-shot curve from the 40% baseline.
> - **Negative-transfer risk** — [[2605.16257|DexJoCo]] shows multi-hand training can degrade. → Q4's degradation-vs-transfer test is the go/no-go before scaling.

### A3 — Deformable-Object Grasping under Ill-Defined Contact

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | For cloth, rope, and soft objects there is no canonical grasp-pose — the contact configuration is a continuum the gripper *creates*, not a pose it *finds*. The field assumes grasp synthesis = pose selection on a rigid geometry. The bet: a closed-loop force-regulation policy with dense tactile + differentiable soft-body physics holds where rigid-grasp estimators fail, matching [[2509.18830\|DexSkin]]'s 90% contact-pressure cut and 20%→60% real-fruit integrity. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2511.02097\|WM Manipulation Survey]], [[2510.25725\|HumanoidVTA]] |
| **Key targets** | [[2509.18830\|DexSkin]] 90% pressure reduction (14.5→1.53 kPa) + blueberry integrity 20%→60%, 19/20 perturbed reorientation; cross-ref [[Sim2Real\|Sim2Real]] for differentiable soft-body physics; [[2510.25725\|HumanoidVTA]] dense-tactile soft-object discrimination |

**Why it matters.** Grasp synthesis (A1, A2) assumes a rigid object with a recoverable 6-DoF pose. Deformables break that: a towel, sponge, or blueberry has no canonical grasp-pose — the contact is something the gripper *creates* by how it closes, and the "right" grasp is force you regulate, not geometry you localize. [[2510.25725|HumanoidVTA]] documents that soft-object manipulation "induces dynamic, complex, time-varying tactile patterns" unlike rigid contact, and dense tactile is far more discriminative than sparse — yet current optimization can't use it. [[2509.18830|DexSkin]] shows the payoff: conformable skin + residual RL cuts artificial-berry pressure 90% (14.5→1.53 kPa) and lifts real blueberry integrity 20%→60%. This is one direction inside Grasping; the differentiable soft-body physics substrate belongs to [[Sim2Real|Sim2Real]].

**First-principles framing.**
- **First principle**: For a deformable object the contact state is a continuum the effector *produces*, not a pose it *selects* — shape under contact is a function of the applied force field, so grasping is closed-loop force regulation. There is no ground-truth grasp-pose to regress to.
- **Assumption being challenged**: That grasp synthesis = pose selection on a rigid geometry. [[2506.17198|Dex1B]] and [[2505.03233|SynGrasp-1B]] generate grasp *poses*; for deformables the pose is ill-defined, so pose-selection — and the rigid-body SDF feasibility loss — doesn't apply. It is a different problem, not a hard case of rigid grasping.
- **The bet**: A force-regulation policy with dense tactile + differentiable soft-body physics holds where rigid-grasp estimators fail, matching [[2509.18830|DexSkin]]'s 90% pressure reduction and 20%→60% fruit integrity, and beating sparse-tactile baselines on [[2510.25725|HumanoidVTA]]'s soft-object discrimination.

**Evidence.**
- [[2509.18830|DexSkin]] — Conformable capacitive skin (60 taxels, 294°) + residual RL; berry pressure 90% cut (14.5→1.53 kPa), blueberry integrity 20%→60%, 19/20 perturbed reorientation; the force-regulation anchor.
- [[2510.25725|HumanoidVTA]] — 2,124-sensor humanoid soft-object dataset; dense tactile separates pressure conditions where sparse fails; the dense-tactile substrate.
- [[2604.07335|TAMEn]] — Closed-loop tactile + AR recovery for contact-rich bimanual; 75% SR; soft-object recovery data (feeds C3).
- [[2511.04665|Real-to-Sim GS]] (cross-ref Sim2Real) — 3DGS + soft-body twin; ρ > 0.9 sim-real; the differentiable-soft-body eval substrate.
- [[2511.02097|WM Manipulation Survey]] — Names object-centric representations and physics-awareness as open; deformables stress both.

**Concrete research questions.**
1. **Q1 — Force-regulation vs pose-selection on deformables.** Compare [[2509.18830|DexSkin]]-style residual RL against a rigid-grasp estimator on towel/sponge/fruit — does force-regulation win where pose-selection has no target?
2. **Q2 — Dense vs sparse tactile for contact-creation.** Quantify [[2510.25725|HumanoidVTA]]'s dense-vs-sparse gap on a *control* (not classification) task — does dense tactile translate to higher SR, or does optimization bottleneck it?
3. **Q3 — Differentiable soft-body physics as the dynamics model.** Use a differentiable MPM/soft-body twin (cross-ref [[Sim2Real|Sim2Real]]) as the world model — does physics-grounded prediction beat model-free force-regulation?
4. **Q4 — Contact-pressure as the reward.** [[2509.18830|DexSkin]] derives interpretable force from skin; test a pressure-bounded reward for fragile-object grasping (couples to D4).

**Related research papers.**
- [[2509.18830|DexSkin]] — Conformable skin + residual RL; 90% pressure reduction, 20%→60% berry integrity; the force-regulation anchor.
- [[2510.25725|HumanoidVTA]] — Dense humanoid tactile; dense > sparse discrimination; the substrate.
- [[2604.07335|TAMEn]] — Closed-loop tactile recovery data; 75% SR; soft-object recovery.
- [[2604.20444|VTouch++]] — 120K-episode synchronized vision+tactile+proprioception; soft-contact data.
- [[2511.04665|Real-to-Sim GS]] — 3DGS + soft-body twin; ρ > 0.9; differentiable-soft-body eval (cross-ref Sim2Real).
- [[2603.05687|CGP]] — Contact-grounded coupled state+tactile prediction; real-time; contact as trajectory (feeds B1).
- [[2302.04659|ManiSkill2]] — Real-time rigid-MPM soft-body sim (80–84 FPS); the soft-body throughput baseline.
- [[2605.13083|TouchAnything]] — Multi-view ego + dense tactile; soft-contact data, no deformable policy.

**Benchmarks & metrics.**
- [[2509.18830|DexSkin]] — 90% pressure reduction (14.5→1.53 kPa), blueberry integrity 20%→60%, 19/20 perturbed; the deformable-grasping metric.
- [[2510.25725|HumanoidVTA]] — Dense vs sparse t-SNE separation on soft objects; the discrimination-vs-control diagnostic.
- [[2302.04659|ManiSkill2]] — Soft-body environments at 80–84 FPS; low IL/RL SR reveals the algorithmic gap.

> [!warning] Risks
> - **No canonical success metric** — "did it grasp" is ill-defined for cloth. → Adopt task-completion (fold, pack) + force-bound (integrity) jointly, per [[2509.18830|DexSkin]]; don't report grasp-SR.
> - **Dense tactile optimization is unsolved** — [[2510.25725|HumanoidVTA]] shows dense barely beats sparse. → Q2's dense-vs-sparse *control* test is the go/no-go; if it doesn't translate, the bet narrows to force-regulation without dense tactile.
> - **Soft-body sim is slow / inaccurate** — [[2302.04659|ManiSkill2]] runs soft-body at 80 FPS vs 2000 FPS rigid. → Bound physics claims to validated twins (ρ > 0.9, [[2511.04665|Real-to-Sim GS]]); cross-ref Sim2Real.

---

## Cluster B — Contact-Rich Assembly & Precision

*Sub-millimeter contact — insertion, assembly, precision — where vision is blind to the contact state and open-loop policies fail.*

### B1 — Predictive-Tactile Contact Imagination

| | |
|---|---|
| **Cluster** | B — Contact-Rich Assembly & Precision |
| **Thesis** | In contact, the next-step force is a deterministic consequence of the action — so a policy can forecast it and act before contact, not just react after. The field assumes reactive tactile feedback is enough, but force arrives too late to prevent a bad insertion. Since the Peg-in-Hole absolute is already saturated ([[2512.23864\|DreamTacVLA]] 95.0%), the bet is the *prediction delta*: an action-conditioned tactile world model adds [[2512.23864\|DreamTacVLA]]'s +22.3% over its no-Dream ablation — a margin reaction cannot recover — and holds [[2603.19201\|OmniVTA]]'s 60–63% SR under perturbation. |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2511.02097\|WM Manipulation Survey]], [[2510.25725\|HumanoidVTA]] |
| **Key targets** | **Headline (prediction delta + OOD, where the absolute is saturated):** [[2512.23864\|DreamTacVLA]] +22.3% over no-Dream ablation; [[2603.19201\|OmniVTA]] 60–63% SR *under perturbation* at 60 Hz. **Saturated in-distribution reference:** [[2512.23864\|DreamTacVLA]] 95.0% Peg-in-Hole / 85.7% USB / 81.1% Gear. **Consumed-force floor:** [[2505.22159\|ForceVLA]] +23.2 pp over π0-with-force |

**Why it matters.** Three surveys name the same gap: [[2604.04974|Video-to-Control Survey]] (tactile/force integration unresolved), [[2511.02097|WM Manipulation Survey]] (physics 3rd of 13 capabilities), [[2510.25725|HumanoidVTA]] (dense tactile discriminative but under-used). The field consumes force as a *current* observation — [[2505.22159|ForceVLA]] (+23.2 pp), [[2601.20321|TaF-VLA]] (64.8%), [[2509.07962|TA-VLA]] (torque tokens) — but reactive feedback arrives only *after* contact, too late to prevent a bad insertion. Two existence proofs invert it: [[2512.23864|DreamTacVLA]]'s "Think–Dream–Act" loop (a tactile world model predicts the future, the policy refines its draft) hits 95.0% Peg-in-Hole and +22.3% over ablations, and [[2603.19201|OmniVTA]]'s visuo-tactile world model + 60 Hz reflexive controller anticipates contact. The claim: next-step force is *predictable* from the action, so a policy that imagines it acts anticipatorily. The WAM-architecture form of this same bet — a wrench head on the imagination backbone, or a discrete contact-mode latent — is [[WAM|WAM]]-A2/B1; this direction is the manipulation-task application and the prediction-delta bet.

**First-principles framing.**
- **First principle**: The next-step tactile signal is a deterministic consequence of the action given the contact state — it is forecastable. A policy that only reads current force is reactive by construction; one that *predicts* force can pick actions with a good imagined outcome before committing.
- **Assumption being challenged**: That reactive tactile feedback suffices. [[2505.22159|ForceVLA]], [[2601.20321|TaF-VLA]], [[2509.07962|TA-VLA]] consume force as input; their limit is latency — by the time bad force is felt, the misalignment has happened. [[2512.23864|DreamTacVLA]]'s +22.3% Dream-ablation shows prediction adds what reaction cannot.
- **The bet**: An action-conditioned tactile world model beats reactive-tactile policies on the axis where in-distribution SR is saturated — the headline is the *prediction delta* ([[2512.23864|DreamTacVLA]]'s +22.3% over its no-Dream ablation, concentrated at contact onset) and robustness under perturbation ([[2603.19201|OmniVTA]]-class 60 Hz, 60–63% SR) — not the saturated 95.0% absolute, which sits at [[2505.22159|ForceVLA]]-class consumed-force SR as the floor.

**Evidence.**
- [[2512.23864|DreamTacVLA]] — Think–Dream–Act: tactile world model predicts future tactile, policy refines draft action; 95.0% Peg-in-Hole, 85.7% USB, 81.1% Gear, +22.3% over ablations; the contact-imagination anchor.
- [[2603.19201|OmniVTA]] — Visuo-Tactile World Model + 60 Hz Reflexive Latent Tactile Controller; 21K-trajectory OmniViTac dataset; 60–63% under perturbation; predictive + reflexive contact control.
- [[2603.05687|CGP]] — Predicts coupled robot-state + tactile trajectories, maps to controller targets; real-time; contact as a jointly-predicted quantity.
- [[2505.22159|ForceVLA]] — Force-aware MoE, force as first-class modality; 60.5% (+23.2 pp over π0-with-force), 90% under occlusion; the consumed-force ceiling to beat.
- [[2601.20321|TaF-VLA]] — Tactile-force alignment (VQ-VAE, 10M pairs); 64.8% (vs 37.1% vision-only), 60.3% cross-sensor; force grounded but consumed, not predicted.

**Concrete research questions.**
1. **Q1 — World model vs reactive-tactile ablation.** Isolate [[2512.23864|DreamTacVLA]]'s Dream component: does predicting the tactile future add +22.3% over a matched reactive policy, concentrated at contact onset?
2. **Q2 — Forecast horizon vs reflexive frequency.** [[2603.19201|OmniVTA]] runs 60 Hz; ablate prediction horizon (1-step vs N-step) against control frequency — what horizon maximizes anticipation before drift dominates?
3. **Q3 — Imagined tactile when sensors absent.** Train with sensors, deploy using *imagined* tactile as a forecast (couples to [[#E1 — Sensor-Free Force-Aware Policies|E1]]) — does imagined contact recover sensor-on SR?
4. **Q4 — Sensor-agnostic prediction target.** Use [[2601.20321|TaF-VLA]]'s force-aligned latent or [[2506.14754|Sparsh-X]]'s multisensory representation as the prediction target so the world model is sensor-agnostic.

**Related research papers.**
- [[2512.23864|DreamTacVLA]] — Think–Dream–Act tactile world model; 95.0% Peg-in-Hole, +22.3%; the anchor.
- [[2603.19201|OmniVTA]] — Visuo-tactile world model + 60 Hz reflexive controller; predictive + reflexive.
- [[2603.05687|CGP]] — Coupled state+tactile trajectory prediction → controller targets; real-time contact grounding.
- [[2505.22159|ForceVLA]] — Force-aware MoE; +23.2 pp; the consumed-force ceiling.
- [[2601.20321|TaF-VLA]] — Tactile-force alignment, cross-sensor; consumed, not predicted.
- [[2506.14754|Sparsh-X]] — Multisensory tactile backbone, 1M contacts; 90% plug-insertion; the sensor-agnostic prediction target.
- [[2509.19696|Diffusion Impedance Learning]] — Diffusion-based impedance for contact-rich; impedance, not tactile prediction.
- [[2503.16806|DyWA]] — Dynamics-adaptive world action model predicting future object state; 82.2%/75.0% seen/unseen; the state-prediction analog (non-prehensile).

**Benchmarks & metrics.**
- [[2512.23864|DreamTacVLA]] — 95.0% Peg-in-Hole / 85.7% USB / 81.1% Gear / 74.6% Tool-Stab; +22.3% over ablations; the contact-imagination benchmark.
- [[2603.19201|OmniVTA]] — 6 real contact-rich tasks; 60% (Wipe) / 63% (Peel) under perturbation; the predictive-reflexive metric.
- [[2502.05086|REASSEMBLE]] — NIST board; insert hardest, DMP 70% insertion; force-torque phase patterns as the contact-dynamics ground truth.

> [!warning] Risks
> - **Prediction may plateau at the noise floor** — micro-slip isn't in the action-conditioned model. → Bound to vision/action-correlated contact; report where imagined tactile diverges from measured.
> - **World-model latency vs reflexive budget** — predicting tactile must fit the [[2603.19201|OmniVTA]] 60 Hz loop. → Q2's horizon-vs-frequency ablation is the feasibility gate.
> - **Sim tactile is non-standard** — a tactile world model needs tactile data at scale. → Use [[2603.19201|OmniVTA]]'s OmniViTac + [[2602.23253|SPARR]]-style real residual; cross-ref [[Sim2Real|Sim2Real]].

### B2 — Contact-Mode-Conditional Precision & Reversibility

| | |
|---|---|
| **Cluster** | B — Contact-Rich Assembly & Precision |
| **Thesis** | Contact physics is locally discontinuous (make/break, slip-stick, friction-cone), so the dynamics are piecewise — but the field smooths over them by scaling continuous policies. Since in-distribution [AutoMate](https://arxiv.org/abs/2407.08028) is already saturated ([[2602.23253\|SPARR]] 95–100%), the bet is on the OOD axis: a discrete contact-mode policy wins on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer at [[2602.23253\|SPARR]]'s +74.5% relative SR / 36.5% cycle-time cut, below [[2602.23648\|FAVLA]]'s 7.7 N peak force, with mode-derived reversibility a smooth policy lacks. |
| **Anchor surveys** | [[2511.02097\|WM Manipulation Survey]], [[2604.04974\|Video-to-Control Survey]], [[2502.05086\|REASSEMBLE]] |
| **Key targets** | **Headline (unseen-task, where in-distribution is saturated):** [[2602.23253\|SPARR]] +74.5% relative SR / 36.5% cycle-time cut on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic); [[2407.16677\|ResiP]] perturbation drop only 12% (vs 19–26%). **Saturated in-distribution reference:** [[2602.23253\|SPARR]] 95–100% [AutoMate](https://arxiv.org/abs/2407.08028). **Force bound:** [[2602.23648\|FAVLA]] 80.8% at 7.7 N peak (Gear) |

**Why it matters.** [[2502.05086|REASSEMBLE]] shows "Insert is the hardest action … due to its multi-step nature and demand for precise alignment and force application," and force-torque "reveals distinct patterns corresponding to action phases (free-space, contact, pushing, twisting)" — the task *is* a sequence through discrete contact modes. Yet the dominant fixes scale continuous policies or add residuals: [[2602.23253|SPARR]] (95–100% [AutoMate](https://arxiv.org/abs/2407.08028), +74.5% unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic)), [[2407.16677|ResiP]] (5%→99%), [[2602.23648|FAVLA]] (80.8%) — none model the contact *mode* as a discrete latent. The claim: contact physics is piecewise (Coulomb friction only in-contact, ballistic only in free-space), so a mode-conditional policy gets structural granularity a smooth approximator pays exponentially for at the friction-cone boundary. It also unlocks *reversibility*: `making` vs `in-contact` tells you whether a corrective retreat is safe.

**First-principles framing.**
- **First principle**: Contact dynamics are locally discontinuous — friction-cone boundaries, normal-force singularities, slip-stick are discrete state changes. The true dynamics are piecewise, so a smooth continuous policy approximating them is structurally mismatched, and gets expensive exactly at the precision-critical boundary.
- **Assumption being challenged**: That more capacity or more residual closes the sub-millimeter gap. [[2602.23253|SPARR]] and [[2407.16677|ResiP]] add residuals; [[2602.23648|FAVLA]] adds force-adaptive frequency — none address the *structural* discontinuity. [[2502.05086|REASSEMBLE]]'s phase-distinct force patterns show the modes are real and observable; the field smooths over them.
- **The bet**: A contact-mode-conditional policy ($c_t \in \{\text{free, making, in-contact, sliding, breaking}\}$) beats monolithic continuous policies *where in-distribution SR is saturated* — the contribution is on the OOD axis, not the in-distribution [AutoMate](https://arxiv.org/abs/2407.08028) number ([[2602.23253|SPARR]] already 95–100%). The target is unseen-task transfer: [[2602.23253|SPARR]]'s +74.5% relative SR / 36.5% cycle-time on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic), below [[2602.23648|FAVLA]]'s 7.7 N — precision *and* reversibility from the mode structure.

**Evidence.**
- [[2602.23253|SPARR]] — Sim base policy + vision-conditioned real residual; 95–100% [AutoMate](https://arxiv.org/abs/2407.08028), +74.5% relative / 36.5% cycle-time on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic), no human supervision; the assembly-SR ceiling.
- [[2407.16677|ResiP]] — Frozen BC + residual PPO for closed-loop correction; peg-in-hole 5%→99%, 12% perturbation drop (vs 19–26%); residual reactivity, continuous.
- [[2602.23648|FAVLA]] — Force-adaptive fast-slow VLA, force-variance head gates AE frequency; 80.8%, peak force 7.7 N (Gear) / 9.9 N (Box); adaptive frequency ≈ implicit mode-awareness, not explicit modes.
- [[2502.05086|REASSEMBLE]] — NIST board; insert hardest, force-torque phase-distinct patterns; the contact-mode ground truth.
- [[2603.05687|CGP]] — Coupled state+tactile prediction → controller targets; predicts contact evolution, continuous.

**Concrete research questions.**
1. **Q1 — Discrete contact-mode latent.** Predict a categorical $c_t \in \{\text{free, making, in-contact, sliding, breaking}\}$ from force-torque ([[2502.05086|REASSEMBLE]]-supervised) and condition dynamics on it — does explicit mode beat [[2602.23648|FAVLA]]'s implicit frequency-adaptation?
2. **Q2 — Mode-conditional physics losses.** Apply Coulomb friction only in `in-contact`, ballistic only in `free` — does mode-gated physics improve sub-millimeter insertion over a single dynamics head?
3. **Q3 — Reversibility from mode.** Use the mode to decide whether a corrective retreat is safe (`making` reversible, `in-contact` may be wedged) — does this cut failures on [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer?
4. **Q4 — Per-mode residual.** Combine with [[2602.23253|SPARR]]/[[2407.16677|ResiP]] — does a residual policy per contact mode beat a single residual?

**Related research papers.**
- [[2602.23253|SPARR]] — Sim base + real residual; 95–100% [AutoMate](https://arxiv.org/abs/2407.08028), +74.5% NIST; the ceiling.
- [[2407.16677|ResiP]] — Residual RL for precise assembly; 5%→99%; continuous residual.
- [[2602.23648|FAVLA]] — Force-adaptive fast-slow VLA; 80.8%; implicit mode-awareness.
- [[2603.15169|ForceVLA2]] — Hybrid force-position control; 66% avg; position/force switching, no discrete mode.
- [[2502.05086|REASSEMBLE]] — NIST multimodal assembly; phase-distinct force patterns; the mode ground truth.
- [[2509.19696|Diffusion Impedance Learning]] — Diffusion-based impedance; continuous regulation.
- [[2605.05172|Q2RL]] — Q from BC for on-robot RL; 3.75× on peg/pipe in 1–2 hrs; the fine-tuning loop for mode-policies.
- [[2503.16806|DyWA]] — Dynamics-adaptive world action model (FiLM on inferred physics); 82.2%/75.0%; mode-adjacent adaptation.

**Benchmarks & metrics.**
- [AutoMate](https://arxiv.org/abs/2407.08028) (8–10 tasks) — Insertion/assembly SR; [[2602.23253|SPARR]] 95–100%, the saturated ceiling.
- [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) industrial assembly — Cross-task transfer; [[2602.23253|SPARR]] +74.5% relative SR / 36.5% cycle-time on unseen tasks.
- [[2502.05086|REASSEMBLE]] — NIST board, 4,551 demos, 70% DMP insertion; the contact-phase + anomaly benchmark.

> [!warning] Risks
> - **Discrete-latent optimization variance** — Gumbel-softmax / REINFORCE for $c_t$. → Anneal soft→hard; start continuous, harden over training.
> - **Mode supervision needs ground truth** — real mode labels are scarce. → Distill from [[2502.05086|REASSEMBLE]]'s phase annotations + sim contact; report mode-classification accuracy first.
> - **Saturated headline** — [[2602.23253|SPARR]] already 95–100% [AutoMate](https://arxiv.org/abs/2407.08028). → Show on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer + peak-force + reversibility, not in-distribution SR.

---

## Cluster C — Bimanual & Dual-Arm Coordination

*Two-arm manipulation where the cross-arm coupling is non-factorizable and bimanual demonstration data is scarce — coordination-native policies, scalable data generation, and the tactile channel that makes force-balanced cooperation observable.*

### C1 — Coordination-Native Bimanual Policies

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Two-arm value is non-additive — the cross-arm coupling carries the coordination — but each arm's *skill* is a transferable single-arm prior. The field assumes bimanual competence requires bimanual-scale pretraining; it doesn't, because only the coupling is bimanual-specific. The bet: a coordination-native composition of single-arm priors matches monolithic SR on ~50 episodes — [[2511.05275\|TwinVLA]] 76% (vs RDT-1B 45%, ≈π0 80%) at ~25 GPU-days. |
| **Anchor surveys** | [[2604.05831\|BiCoord]], [[2407.07788\|BiGym]], [[2603.15469\|RoCo Challenge]] |
| **Key targets** | [[2511.05275\|TwinVLA]] 76% on ~50 episodes / ~25 H100-days (vs RDT-1B 45%, π0 80%); [[2604.05831\|BiCoord]] 4× spatial-temporal-integral + later-stage degradation; [[2507.23523\|H-RDT]] 41.6% few-shot (vs RDT 16.0%) + 87.2% RoboTwin 2.0 |

**Why it matters.** [[2604.05831|BiCoord]] quantifies the problem — a 4× spatial-temporal-integral increase, "policy performance consistently degraded in later stages of long-horizon tasks" — and [[2407.07788|BiGym]] shows IL/RL near-0% on stacking and long sequences. The dominant response trains monolithic models needing thousands of hours of proprietary two-arm data. [[2511.05275|TwinVLA]] inverts it: compose *two pre-trained single-arm policies* with a Joint-Attention coupling, matching monolithic systems on ~50 episodes / ~25 H100-days (76% vs RDT-1B 45%, ≈π0 80% at far more compute), and [[2507.23523|H-RDT]] transfers single-hand human-video priors into bimanual. The claim: each arm's *skill* is an abundant single-arm prior, and only the *coupling* — handover timing, force balance — is the scarce bimanual-specific term, so compose the priors and learn only the cheap coupling.

**First-principles framing.**
- **First principle**: The bimanual value is non-additive — $V(a_L, a_R) \neq V(a_L) + V(a_R)$ — because cross-arm coupling is the load-bearing term. But each arm's skill is a marginal single-arm policy, so the joint factors as (transferable skill) × (bimanual coupling), and only the latter needs two-arm data.
- **Assumption being challenged**: That bimanual competence requires bimanual-scale pretraining. Monolithic policies learn the whole joint from two-arm data; [[2511.05275|TwinVLA]] and [[2507.23523|H-RDT]] show the skill is reusable and only the coupling is bimanual-specific — the data wall is partly self-imposed by monolithic design.
- **The bet**: A coordination-native composition matches monolithic SR on ~50 episodes — [[2511.05275|TwinVLA]] 76% (vs RDT-1B 45%, ≈π0 80%) at ~25 H100-days — and holds [[2604.05831|BiCoord]]'s later-stage coordination where monolithic policies degrade.

**Evidence.**
- [[2511.05275|TwinVLA]] — Composes two single-arm policies via Joint Attention (causal-masked cross-arm self-attention); 76% on ~50 episodes / ~25 H100-days, vs RDT-1B 45%, ≈π0 80%; the composition anchor.
- [[2507.23523|H-RDT]] — Single-hand human-video (EgoDex 338K) → bimanual DiT via flow matching; 41.6% few-shot (vs RDT 16.0%), 87.2% RoboTwin 2.0; human-prior-to-bimanual transfer.
- [[2604.05831|BiCoord]] — Long-horizon bimanual benchmark; 4× spatial-temporal integral, MRD/ARD/SMT/SMP/STI metrics, later-stage degradation; the coordination-quantification anchor.
- [[2603.15469|RoCo Challenge]] — Collaborative assembly; end-to-end beats modular for recovery; coordination + Sim-to-Real Cliff.
- [[2410.24185|DexMimicGen]] — Subtask taxonomy (async/sync/ordered); 90% real humanoid; the coordination-structure substrate (feeds C2).

**Concrete research questions.**
1. **Q1 — Joint-Attention vs monolithic.** Ablate [[2511.05275|TwinVLA]]'s cross-arm Joint Attention against a monolithic policy at matched data — does the composed prior + explicit coupling win on [[2604.05831|BiCoord]]'s SMT/SMP?
2. **Q2 — Coupling-term data efficiency.** Given strong single-arm priors, how few bimanual episodes does the coupling need — replicate [[2511.05275|TwinVLA]]'s ~50-episode result on [[2604.05831|BiCoord]]'s 4×-harder tasks?
3. **Q3 — Coordination-type-conditional coupling.** [[2410.24185|DexMimicGen]] distinguishes async/sync/ordered subtasks; condition the coupling on type — does typed coupling beat one Joint-Attention layer?
4. **Q4 — Later-stage degradation diagnosis.** [[2604.05831|BiCoord]] degrades late; is it a coupling or single-arm-skill failure — does composition isolate which breaks?

**Related research papers.**
- [[2511.05275|TwinVLA]] — Twin single-arm composition + Joint Attention; 76% on ~50 episodes; the anchor.
- [[2507.23523|H-RDT]] — Human-video-to-bimanual transfer; 41.6% few-shot; single-prior transfer.
- [[2604.05831|BiCoord]] — Long-horizon bimanual benchmark; 4× coordination, later-stage degradation; the metric.
- [[2603.15469|RoCo Challenge]] — Collaborative assembly, policy > modular for recovery; coordination + Sim-to-Real.
- [[2410.24185|DexMimicGen]] — Bimanual subtask taxonomy (async/sync/ordered); 90% real; coordination structure.
- [[2511.21264|MPPI-Bimanual]] — Sampling-based MPC for bimanual coordination; model-based baseline.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual/mobile trajectories, MIND-2 + IQL; up to 1.0 multi-robot SR; data + framework.
- [[2407.07788|BiGym]] — 40 mobile bimanual tasks; near-0% on long-horizon; the difficulty-establishing benchmark.

**Benchmarks & metrics.**
- [[2604.05831|BiCoord]] — 4× spatial-temporal integral, MRD/ARD/SMT/SMP/STI, later-stage degradation; the coordination-quality benchmark.
- [[2511.05275|TwinVLA]] — 76% on Anubis (vs RDT-1B 45%, π0 80%), 75.8% vs 61.6% Tabletop-Sim Easy, ~50 episodes / ~25 GPU-days; the data-efficiency metric.
- [[2407.07788|BiGym]] — 40 tasks; ACT/DP up to 100% simple, 0% on stack-blocks/long sequences; the long-horizon floor.

> [!warning] Risks
> - **Composition may cap the coordination ceiling** — tightly-coupled tasks (handover + force balance) may exceed what composed priors reach. → Bound to loosely-to-moderately-coupled tasks; report the [[2604.05831|BiCoord]] coupling-tightness vs SR curve.
> - **Joint Attention is one design** — [[2511.05275|TwinVLA]]'s causal-masked attention may not be optimal. → Q3's typed-coupling ablation tests alternatives.
> - **Single-arm priors must be strong** — composition fails on weak base policies. → Validate base SR first; the bet assumes π0/RDT-class priors exist.

### C2 — Scalable Bimanual Data Generation with Coordination Structure

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Coordination structure (per-arm subtask decomposition + ordering constraints) is what makes a few demos generalize to many configurations — not data volume. The field assumes bimanual data must be teleoperated at scale. The bet: replaying human demos through a coordination-structured simulator lifts real bimanual SR by [[2506.18088\|RoboTwin 2.0]]'s 24.4% (few-shot) / 21.0% (zero-shot) and reaches [[2410.24185\|DexMimicGen]]'s 90% from 40 sim demos (vs 0% from 4 source). |
| **Anchor surveys** | [[2506.18088\|RoboTwin 2.0]], [[2604.05831\|BiCoord]], [[2603.15469\|RoCo Challenge]] |
| **Key targets** | [[2410.24185\|DexMimicGen]] 90% real (40 sim demos vs 0% from 4), 76.0% vs 0.7% Drawer-Cleanup; [[2506.18088\|RoboTwin 2.0]] +24.4% few-shot / +21.0% zero-shot, 71.3% auto-code SR; [[2504.13059\|RoboTwin]] 300 sim + 20 real ≈ 300 real |

**Why it matters.** [[2506.18088|RoboTwin 2.0]] names the dual-arm data wall — "prohibitive cost of real bimanual data," "synthetic datasets lack automated quality control," "superficial domain randomization" — the bottleneck [[2407.07788|BiGym]] and [[2604.05831|BiCoord]] both hit. Two structure-aware generators show the way out: [[2410.24185|DexMimicGen]] replays a *few* human demos in sim via a subtask taxonomy (async per-arm, sync, ordering) — 90% real humanoid SR from 40 generated demos vs 0% from the 4 source — and [[2506.18088|RoboTwin 2.0]] adds MLLM expert-code + 5-axis randomization + embodiment-aware grasp. The claim: coordination structure (which subtasks are independent, which synchronize, what order) is the generalization-carrying prior — encode it and a handful of demos covers the configuration space; ignore it and you teleoperate every variation.

**First-principles framing.**
- **First principle**: Bimanual generalization comes from coordination structure, not volume — a task decomposed into per-arm subtasks with sync/ordering constraints can be SE(3)-replayed across configurations, so a few demos span many scenes. The structure turns $N$ demos into $N \times K$ feasible trajectories.
- **Assumption being challenged**: That bimanual data must be teleoperated at scale. The field collects two-arm demos directly for lack of coordination-aware replay; [[2410.24185|DexMimicGen]] (90% from 40 vs 0% from 4) and [[2506.18088|RoboTwin 2.0]] show structure-aware generation replaces most teleoperation — the data wall is a missing-structure problem.
- **The bet**: Structure-aware generation lifts real bimanual SR by [[2506.18088|RoboTwin 2.0]]'s 24.4% / 21.0% and reaches [[2410.24185|DexMimicGen]]'s 90% from 40 sim demos (vs 0% from 4), matching [[2504.13059|RoboTwin]]'s "300 sim + 20 real ≈ 300 real."

**Evidence.**
- [[2410.24185|DexMimicGen]] — Subtask taxonomy (async/sync/ordered) replays few human demos in sim; 90% real humanoid from 40 demos (vs 0% from 4), 76.0% vs 0.7% Drawer-Cleanup; the structured-generation anchor.
- [[2506.18088|RoboTwin 2.0]] — MLLM expert-code + sim-in-the-loop + 5-axis randomization + embodiment-aware grasp; +24.4% few-shot / +21.0% zero-shot, 71.3% auto-code; the quality-controlled generator.
- [[2504.13059|RoboTwin]] — Generative digital twin + LLM decomposition; 300 sim + 20 real ≈ 300 real, +40% dual-arm SR; the data-efficiency anchor.
- [[2604.07335|TAMEn]] — Feasibility-aware acquisition + recovery data; 100% replay (vs 12–39%); the executability filter for generated data.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual trajectories + 20K-traj digital twin in Isaac Sim; the cross-embodiment generation scale.

**Concrete research questions.**
1. **Q1 — Coordination-structure ablation.** Strip [[2410.24185|DexMimicGen]]'s sync/ordering constraints — how much of 90%-from-40-demos depends on structure vs raw SE(3) replay?
2. **Q2 — MLLM code-gen vs replay.** Compare [[2506.18088|RoboTwin 2.0]]'s MLLM expert-code against [[2410.24185|DexMimicGen]]'s demo-replay for *coordinated* (not parallel) trajectories — which captures tight coupling?
3. **Q3 — Feasibility filtering.** Apply [[2604.07335|TAMEn]]'s online feasibility validation to generated dual-arm data — does filtering unexecutable coordinations raise downstream SR?
4. **Q4 — Coordination quality on [[2604.05831|BiCoord]].** Train [[2511.05275|TwinVLA]]/[[2507.23523|H-RDT]] on generated data; does it close [[2604.05831|BiCoord]]'s later-stage degradation, or under-represent tight coupling?

**Related research papers.**
- [[2410.24185|DexMimicGen]] — Coordination-structured replay; 90% from 40 demos; the anchor.
- [[2506.18088|RoboTwin 2.0]] — MLLM-generated + randomized data; +24.4% few-shot; quality-controlled generator.
- [[2504.13059|RoboTwin]] — Generative digital twin + LLM decomposition; 300 sim + 20 real ≈ 300 real; data efficiency.
- [[2604.07335|TAMEn]] — Feasibility-aware + recovery data; 100% replay; executability filter.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual + digital twin; cross-embodiment scale.
- [[2507.00833|HumanoidGen]] — Auto data generation for humanoid manipulation; the bimanual-humanoid generation engine.
- [[2603.15469|RoCo Challenge]] — 300+ demos collaborative assembly; failure-recovery curriculum > param count.
- [[2604.20444|VTouch++]] — 120K-episode bimanual vision+tactile+proprioception; the multimodal generation target (feeds C3).

**Benchmarks & metrics.**
- [[2410.24185|DexMimicGen]] — 90% real humanoid (40 demos vs 0% from 4), 76.0% vs 0.7% generated-vs-source; the generation-efficacy metric.
- [[2506.18088|RoboTwin 2.0]] — +24.4% few-shot / +21.0% zero-shot, +31.9% sim generalization, 71.3% auto-code; the randomized-generation metric.
- [[2504.13059|RoboTwin]] — 300 sim + 20 real ≈ 300 real, +40% dual-arm SR; the data-efficiency metric.

> [!warning] Risks
> - **Generated data may miss tight coupling** — replay can produce parallel-but-not-coordinated trajectories. → Q4's [[2604.05831|BiCoord]] test is the gate; couple generation to C1's coupling-aware training.
> - **Sim-to-Real Cliff** — [[2603.15469|RoCo Challenge]] shows sim policies are brittle in real. → Use [[2506.18088|RoboTwin 2.0]]'s 5-axis randomization + [[2604.07335|TAMEn]] filtering; cross-ref [[Sim2Real|Sim2Real]].
> - **MLLM code-gen reliability** — [[2506.18088|RoboTwin 2.0]]'s 71.3% auto-code means ~29% needs refinement. → Keep human-in-the-loop verification; report generation-yield, not just downstream SR.

### C3 — Tactile-Coupled Bimanual Cooperation

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Force-balanced cooperation (holding-while-manipulating, bimanual handover) needs inter-arm force observability vision can't provide — the two arms sense each other through the object. The field treats bimanual coordination as a vision-and-proprioception problem. The bet: a shared tactile channel reaches [[2604.07335\|TAMEn]]'s 75% contact-rich SR where vision-only bimanual fails, using [[2604.20444\|VTouch++]]'s 120K synchronized vision+tactile+proprioception episodes. |
| **Anchor surveys** | [[2604.05831\|BiCoord]], [[2510.25725\|HumanoidVTA]], [[2504.03515\|Dexterous IL Survey]] |
| **Key targets** | [[2604.07335\|TAMEn]] 75% contact-rich bimanual + 100% replay (vs 12–39%); [[2604.20444\|VTouch++]] 120K episodes / 36M frames / 380 tasks synchronized vision+tactile+proprioception; [[2512.24653\|RoboMIND 2.0]] tactile improves contact-task SR (XR-1 gains) |

**Why it matters.** Bimanual benchmarks ([[2604.05831|BiCoord]], [[2407.07788|BiGym]]) are vision-and-proprioception only, yet the hardest tasks — one arm holds while the other manipulates, force-balanced handovers, bimanual assembly — depend on *inter-arm force* vision can't see. The bimanual-tactile data bottleneck has just lifted: [[2604.20444|VTouch++]] provides 120K synchronized episodes (36M frames, 380 tasks), [[2604.07335|TAMEn]] adds closed-loop tactile + recovery data (75% SR), and [[2512.24653|RoboMIND 2.0]] confirms tactile lifts contact-task SR. The claim: force-balanced cooperation is an *inter-arm force observability* problem — a shared tactile channel is not an add-on but the missing observation that makes cooperative force-control possible.

**First-principles framing.**
- **First principle**: Force-balanced cooperation requires inter-arm force observability — when one arm holds and the other manipulates, the coordination is governed by the force each transmits through the object, invisible to vision. The shared force state is the coordination variable; without it the policy coordinates blind.
- **Assumption being challenged**: That bimanual coordination is a vision-and-proprioception problem. [[2604.05831|BiCoord]] and [[2407.07788|BiGym]] are vision-only; their later-stage degradation on contact-coupled tasks is partly *force-blindness*. [[2604.07335|TAMEn]]'s 75% with tactile shows the missing modality is force.
- **The bet**: Tactile-coupled bimanual reaches [[2604.07335|TAMEn]]'s 75% contact-rich SR where vision-only fails, using [[2604.20444|VTouch++]]'s 120K synchronized episodes, with tactile lifting contact-task SR per [[2512.24653|RoboMIND 2.0]].

**Evidence.**
- [[2604.07335|TAMEn]] — Tactile-aware engine for closed-loop contact-rich bimanual + AR recovery; 75% SR, 100% replay (vs 12–39%), 100% object-tracking (vs 32–78%); the contact-rich bimanual anchor.
- [[2604.20444|VTouch++]] — 120K-episode synchronized vision+tactile+proprioception (36M frames, 380 tasks); contrastive cross-modal alignment; the bimanual tactile data substrate.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual trajectories incl. tactile + MIND-2 dual-system; tactile improves contact-task SR; tactile-bimanual at scale.
- [[2510.25725|HumanoidVTA]] — 2,124-sensor humanoid tactile; dense tactile discriminative; the dense-tactile substrate.
- [[2604.05831|BiCoord]] — Vision-only bimanual benchmark; later-stage degradation on coupled tasks; the force-blindness diagnosis.

**Concrete research questions.**
1. **Q1 — Shared vs per-arm tactile channel.** Compare a *shared* inter-arm tactile representation against per-arm fusion on holding-while-manipulating — does shared force-state improve cooperation?
2. **Q2 — Tactile on [[2604.05831|BiCoord]]'s degrading stages.** Add [[2604.20444|VTouch++]]/[[2604.07335|TAMEn]] tactile to a [[2604.05831|BiCoord]] policy — does it arrest the later-stage degradation on contact-coupled subtasks?
3. **Q3 — Force-balance as an explicit objective.** Make inter-arm force-balance a loss term, not just an observation — does explicit balance beat tactile-as-input on handover?
4. **Q4 — Tactile-coupled composition.** Add the shared channel to C1's [[2511.05275|TwinVLA]] — does tactile coupling beat vision-only Joint Attention on contact-coupled bimanual?

**Related research papers.**
- [[2604.07335|TAMEn]] — Closed-loop tactile contact-rich bimanual + recovery; 75% SR; the anchor.
- [[2604.20444|VTouch++]] — 120K synchronized vision+tactile+proprioception bimanual; the data substrate.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual incl. tactile, MIND-2; tactile lifts contact-task SR.
- [[2510.25725|HumanoidVTA]] — Dense humanoid tactile; discriminative for contact.
- [[2604.05831|BiCoord]] — Vision-only bimanual; the force-blindness diagnosis.
- [[2603.05687|CGP]] — Multi-point contact-grounded policy (coupled state+tactile); per-hand, extensible to inter-arm.
- [[2602.19764|Multi-Sensory Sparse Experts]] — RGB+depth+6-axis-force fusion (DeMUSE); 83.2% MT50, 80 ms compliance; the fusion substrate for two-arm force.
- [[2605.13083|TouchAnything]] — Multi-view egocentric + dense tactile; bimanual tactile data.

**Benchmarks & metrics.**
- [[2604.07335|TAMEn]] — 75% contact-rich bimanual, 100% replay (vs 12–39%), 100% object-tracking (vs 32–78%); the contact-rich bimanual metric.
- [[2604.20444|VTouch++]] — 120K episodes / 36M frames / 380 tasks; cross-modal retrieval R@1 2.16% vs 0.29%, real-robot MAE 0.022; the synchronized-tactile metric.
- [[2510.25725|HumanoidVTA]] — Dense vs sparse tactile separation; the inter-arm discriminability reference.

> [!warning] Risks
> - **Inter-arm tactile is hard to instrument** — both arms need synchronized tactile. → [[2604.20444|VTouch++]]/[[2604.07335|TAMEn]] data exist; bound to platforms with bimanual tactile, report the requirement.
> - **Dense tactile optimization is unsolved** — [[2510.25725|HumanoidVTA]] shows dense barely beats sparse. → Use [[2602.19764|Multi-Sensory Sparse Experts]]' AdaMN normalization to stop force being suppressed; report the gap.
> - **Force-balance reward can over-constrain** — penalizing imbalance may block legitimate asymmetric grasps. → Q3 makes balance tunable; expose the balance-vs-flexibility trade-off.

---

## Cluster D — Dexterous & In-Hand Control

*Multi-fingered hands performing high-DoF, contact-discontinuous, sim-to-real-fragile manipulation — universal cross-morphology control, tactile in-hand reorientation, exploration-driven emergent dexterity, and force-safety bounding.*

### D1 — Universal Cross-Morphology Hand Control

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | Dexterous *control intent* — which contacts to form, what in-hand motion to produce — is hand-agnostic; only the actuation that realizes it is hand-specific. The field trains a bespoke policy per hand on parallel-jaw-centric foundations. The bet: a unified-action-space policy drives the *full in-hand control cycle* zero-shot at [[2512.13644\|DexWM]]'s 72% Reach / 58% Grasp / 28% Place (vs DP 16% / 0% / 8%), learnt 5.2× cheaper than per-hand collection. (D1 owns the in-hand *control cycle* after the grasp; A2 owns the *grasp* — distinct phases.) |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2508.13073\|Large VLM-based VLA Survey]], [[2605.16257\|DexJoCo]] |
| **Key targets** | **Headline (control cycle, A2 cannot claim):** [[2512.13644\|DexWM]] zero-shot 72% Reach / 58% Grasp / 28% Place (vs DP 16% / 0% / 8%) + 83% real-world zero-shot grasp (Allegro). **Shared cross-morphology evidence (A2's headline):** [[2603.22264\|UniDex]] 81% progress + 60% / 40% zero-shot + 5.2× cost cut. **Scaling:** [[2602.19764\|Multi-Sensory Sparse Experts]] 83.2% MT50 (vs RDT-1B 77.9%) + 42.6% compute cut |

**Why it matters.** This is the *control* counterpart to A2: A2 transfers the *grasp*, D1 transfers the full *in-hand control* policy after the grasp is established. [[2504.03515|Dexterous IL Survey]] and [[2508.13073|Large VLM-based VLA Survey]] note dexterous manipulation is underserved by parallel-jaw-centric foundations, and [[2605.16257|DexJoCo]] shows multi-task dexterous training *degrades*. [[2603.22264|UniDex]]'s Function-Actuator-Aligned Space controls diverse hands (81% progress, 60%/40% transfer), [[2512.13644|DexWM]] reaches 83% zero-shot grasp via hand-keypoint dynamics from human video, and [[2602.19764|Multi-Sensory Sparse Experts]] scales via sparse MoE (83.2% MT50, 42.6% compute cut) without latency growth. The claim: control intent — the contacts to form and the in-hand motion to produce — is hand-agnostic, while only the actuation is hand-specific; a policy parameterized by intent transfers, one parameterized by joint commands does not.

**First-principles framing.**
- **First principle**: Control intent (which fingers contact where, what in-hand motion) is a hand-agnostic plan; the joint torques are the hand-specific projection. A hammer is held and swung the same way regardless of finger count — intent is the invariant, actuation the variance.
- **Assumption being challenged**: That each dexterous hand needs a bespoke policy on a parallel-jaw-centric foundation. The field trains per-hand because it parameterizes by joint commands; [[2603.22264|UniDex]] (FAAS, 60%/40%) and [[2512.13644|DexWM]] (hand-keypoint dynamics, 83% zero-shot) show intent-level control transfers — the per-hand assumption is a parameterization artifact, and [[2605.16257|DexJoCo]]'s negative transfer is what joint-space yields.
- **The bet**: A unified-action-space policy drives the full in-hand control cycle on unseen hands at [[2512.13644|DexWM]]'s 72% / 58% / 28% zero-shot (vs DP 16% / 0% / 8%) and 83% real-world grasp — a *control*-phase margin A2's grasp-transfer cannot make — learnt 5.2× cheaper than per-hand collection, recovering A2's shared cross-morphology transfer ([[2603.22264|UniDex]] 60%/40%) at 81% in-domain progress, while sparse-MoE scaling ([[2602.19764|Multi-Sensory Sparse Experts]] 83.2% MT50, 42.6% compute cut) keeps inference real-time.

**Evidence.**
- [[2512.13644|DexWM]] — Latent world model on hand-keypoint dynamics from human video + MPC; zero-shot 72%/58%/28% reach/grasp/place, 83% real grasp (Allegro), +34% PCK from Hand Consistency Loss; the control-cycle anchor.
- [[2603.22264|UniDex]] — Function-Actuator-Aligned Space + 3D policy from ego video; 81% progress, zero-shot 60%/40%, 5.2× cost cut; the shared cross-morphology evidence (A2's headline).
- [[2602.19764|Multi-Sensory Sparse Experts]] — DeMUSE sparse-MoE multi-sensory DiT; 83.2% MT50 (vs RDT-1B 77.9%), 42.6% compute cut, 80 ms compliance; scalable capacity without latency.
- [[2505.21864|DexUMI]] — Human-hand interface across underactuated + fully-actuated; 86%, 3.2× efficiency; cross-hand control via relative finger actions.
- [[2605.16257|DexJoCo]] — 11-task dexterous benchmark; multi-task degradation; the negative result motivating intent-space.

**Concrete research questions.**
1. **Q1 — Intent-space vs joint-space transfer.** Parameterize in [[2603.22264|UniDex]]'s FAAS (intent) vs raw joint commands; does intent-space recover 60%/40% zero-shot reorientation on a held-out hand where joint-space gives negative transfer?
2. **Q2 — Hand-keypoint dynamics as shared world model.** Use [[2512.13644|DexWM]]'s hand-keypoint model as cross-hand dynamics — does hand-agnostic dynamics + per-hand actuation beat per-hand end-to-end policies?
3. **Q3 — Sparse-MoE specialization by hand.** Does [[2602.19764|Multi-Sensory Sparse Experts]]' MoE route per-hand (one expert per morphology), and beat a dense cross-hand policy at equal latency?
4. **Q4 — Intent + joint-residual.** Intent-space for the contact plan, a small per-hand joint-residual for fine actuation (couples to A2's grasp-establishment + residual split).

**Related research papers.**
- [[2512.13644|DexWM]] — Hand-keypoint world model from human video; 72%/58%/28% control cycle, 83% real grasp; the anchor.
- [[2603.22264|UniDex]] — Universal control via FAAS; 81% progress, 60%/40% transfer; the shared cross-morphology evidence.
- [[2602.19764|Multi-Sensory Sparse Experts]] — DeMUSE sparse-MoE; 83.2% MT50, 42.6% compute cut; scalable capacity.
- [[2505.21864|DexUMI]] — Human-hand interface, cross-hand; 86%; relative-finger transfer.
- [[2605.16257|DexJoCo]] — 11-task benchmark; multi-task degradation; the negative result.
- [[2604.20689|FingerEye]] — Per-finger eye-in-hand perception; morphology-specific sensing.
- [[2603.04531|PTLD]] — Privileged tactile latent distillation; +182% rotation; the deployable estimator (feeds D2).
- [[2512.24653|RoboMIND 2.0]] — 310K trajectories, six embodiments; cross-embodiment data.

**Benchmarks & metrics.**
- [[2512.13644|DexWM]] — zero-shot 72%/58%/28% reach/grasp/place (vs DP 16%/0%/8%), 83% real grasp, +34% PCK; the full-control-cycle metric A2 cannot claim (the D1 headline).
- [[2603.22264|UniDex]] — 81% progress, zero-shot 60%/40%, 5.2× cost cut; the cross-morphology metric **shared with A2** (here evidence, not D1's headline).
- [[2605.16257|DexJoCo]] — 11-task MuJoCo; DP-T 50.4%→20.0% under randomization, π0.5 highest; the degradation diagnostic.
- [[2602.19764|Multi-Sensory Sparse Experts]] — 83.2% MT50 (vs RDT-1B 77.9%, RT-2 52.2%), 42.6% compute cut; the scalable-dexterity metric.

> [!warning] Risks
> - **Intent-space loses fine dexterity** — the contact plan may discard joint-level precision. → Q4's intent + joint-residual split; bound intent-space to contact-establishment.
> - **40–60% transfer not deployment-ready** — [[2603.22264|UniDex]]'s Wuji 40%. → Frame as a few-shot seed; report the few-shot curve from the zero-shot baseline.
> - **MoE may not specialize by hand** — Q3's assumption may fail. → Test routing-by-hand empirically before claiming MoE solves cross-morphology scaling.

### D2 — Tactile In-Hand Reorientation with Sim-to-Real

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | Tactile is only an interface to the privileged state (object pose/shape) it encodes, so a *real* privileged sensor can replace a simulated tactile sensor as the distillation target. The field assumes tactile sim-to-real requires accurate tactile simulation. The bet: privileged-to-real distillation beats proprioception-only by [[2603.04531\|PTLD]]'s +182% rotation / +57% reorientation goals and reaches [[2210.13702\|DeXtreme]]'s 27.8-vs-14.8 reorientations — without ever modeling the sensor. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2510.25725\|HumanoidVTA]], [[2605.16257\|DexJoCo]] |
| **Key targets** | [[2603.04531\|PTLD]] +182% rotation / +57% reorientation goals, robust to slip/mass/wrist; [[2210.13702\|DeXtreme]] 27.8 (VADR) vs 14.8 (manual DR) at 15 Hz; [[2604.11138\|ViserDex]] 37.6 consecutive, ~25 under adversarial lighting; [[2601.02778\|Force-Based Sim2Real]] 25.1 vs 1.1 (contact vs no-contact) |

**Why it matters.** In-hand reorientation is the canonical dexterous benchmark, and the blocker is tactile sim-to-real: [[2603.04531|PTLD]] notes "accurately simulating tactile sensors is difficult — existing tactile simulators are non-standardized, rely on rigid-body models, and incur a large sim-to-real gap." Most approaches either avoid tactile ([[2210.13702|DeXtreme]], [[2604.11138|ViserDex]]) or build elaborate tactile sim. [[2603.04531|PTLD]] does neither: train privileged-sensor oracles in sim (object pose as privileged), deploy in an *instrumented real cell* to collect paired tactile, distill a deployable estimator from real data — **never simulating tactile** — for +182% rotation / +57% goals, with [[2601.02778|Force-Based Sim2Real]] confirming the value. The claim: the sim-to-real bridge for tactile is the *privileged real sensor* (object pose), not a simulator. D2 is the **in-hand sibling of [[#E1 — Sensor-Free Force-Aware Policies|E1]]** — E1's Route 2 distillation specialized to reorientation, with the deployed estimator running from proprioception.

**First-principles framing.**
- **First principle**: The hard part of tactile sim-to-real is the *simulator*, but tactile is only an interface — the policy needs the privileged state (object pose) it encodes. A *real* privileged sensor (instrumented cell) supplies that interface, so the policy distills from real tactile-vs-privileged pairs without ever simulating tactile.
- **Assumption being challenged**: That tactile sim-to-real requires accurate tactile simulation. The field avoids tactile or builds tactile sims; [[2603.04531|PTLD]]'s no-tactile-sim distillation shows the simulator is avoidable — the gap is self-imposed by insisting on simulating the sensor.
- **The bet**: Privileged-to-real distillation beats proprioception-only by [[2603.04531|PTLD]]'s +182% / +57%, reaches [[2210.13702|DeXtreme]]'s 27.8-vs-14.8 reorientations, and holds under [[2604.11138|ViserDex]]'s adversarial lighting (~25) — tactile-level in-hand performance without modeling the sensor.

**Evidence.**
- [[2603.04531|PTLD]] — Privileged tactile latent distillation, no tactile sim; +182% rotation, +57% reorientation goals, robust to slip/mass/wrist; the no-tactile-sim anchor.
- [[2210.13702|DeXtreme]] — Vectorized Automatic Domain Randomization + Isaac Gym; 27.8 (VADR) vs 14.8 (manual DR), 15 Hz vision pose estimator; the sim-to-real reorientation anchor.
- [[2604.11138|ViserDex]] — 3DGS-in-the-loop + pre-rasterization augmentation for monocular RGB; 37.6 consecutive / ~25 (adversarial lighting), single-GPU; visual sim-to-real.
- [[2601.02778|Force-Based Sim2Real]] — Distance-field tactile sim + current-to-torque calibration; 25.1 vs 1.1 rotations (contact vs no-contact); the contact-value proof.
- [[2509.18830|DexSkin]] — Conformable skin + pneumatic calibration; 19/20 perturbed, 5/20→14/20 cross-sensor transfer; the real-tactile-hardware reference.

**Concrete research questions.**
1. **Q1 — Privileged-real vs tactile-sim distillation.** Compare [[2603.04531|PTLD]]'s privileged-real interface against a tactile-sim → real pipeline — does avoiding the sim recover or exceed +182%?
2. **Q2 — Tactile vs visual sim-to-real.** Compare [[2603.04531|PTLD]] (tactile) vs [[2604.11138|ViserDex]] (monocular RGB 3DGS) on perturbation — which modality holds better under slip/lighting?
3. **Q3 — Cross-sensor tactile transfer.** [[2509.18830|DexSkin]]'s calibration transfers across skin instances (5/20→14/20); does it generalize the [[2603.04531|PTLD]] estimator across tactile hardware?
4. **Q4 — VADR + privileged-tactile.** Combine [[2210.13702|DeXtreme]]'s randomization with [[2603.04531|PTLD]]'s distillation — does it beat either alone past 27.8 reorientations?

**Related research papers.**
- [[2603.04531|PTLD]] — Privileged tactile latent distillation, no tactile sim; +182% rotation; the anchor.
- [[2210.13702|DeXtreme]] — VADR + Isaac Gym in-hand reorientation; 27.8 vs 14.8; sim-to-real anchor.
- [[2604.11138|ViserDex]] — 3DGS-in-the-loop monocular RGB reorientation; 37.6 / ~25 adversarial; visual sim-to-real.
- [[2601.02778|Force-Based Sim2Real]] — Distance-field tactile sim + calibration; 25.1 vs 1.1; contact-value proof.
- [[2509.18830|DexSkin]] — Conformable skin + pneumatic calibration; 19/20 perturbed, cross-sensor transfer; real-tactile reference.
- [[2605.09789|DRIS]] — Domain-Randomized Instance Set (belief propagation); 68% reactive catching zero-shot; uncertainty-aware sim-to-real (couples to D3).
- [[2603.15257|HapticVLA]] — Sensor-free tactile via distillation; 86.7%; the deployment twin (feeds [[#E1 — Sensor-Free Force-Aware Policies|E1]] Route 2).
- [[2602.19764|Multi-Sensory Sparse Experts]] — Multi-sensory fusion incl. force; 83.2% MT50; the multi-sensory in-hand substrate.

**Benchmarks & metrics.**
- [[2603.04531|PTLD]] — +182% rotation, +57% reorientation goals, slip/mass/wrist robust; the tactile-in-hand metric.
- [[2210.13702|DeXtreme]] — 27.8 (VADR) vs 14.8 (manual) reorientations, 15 Hz pose; the sim-to-real reorientation metric.
- [[2604.11138|ViserDex]] — 37.6 consecutive / ~25 adversarial, 65.4%/56.3% pose accuracy, single-GPU; the visual-robustness metric.

> [!warning] Risks
> - **Instrumented real cell needed** — [[2603.04531|PTLD]] requires a privileged-sensor real setup. → This is a one-time data-collection cost, not a deployment dependency; report the instrumentation requirement explicitly.
> - **Privileged-real distillation may not generalize beyond training objects** — the estimator is trained on instrumented objects. → Bound to the object distribution; cross-ref [[Sim2Real|Sim2Real]] for the broader sim-to-real story.
> - **Tactile vs visual may be task-dependent** — Q2 may show no universal winner. → Report the modality-vs-perturbation-type split (slip favors tactile, occlusion favors neither), not a single number.

### D3 — Exploration-Driven Emergent Dexterity

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | Long-horizon exploration is gated by the *initial-state diversity* the agent sees, not by reward shaping — a behavior is only discoverable if its precursor states are visited. The field hand-crafts curricula and rewards per task, then throws compute at a fixed reset distribution (which saturates). The bet: diverse-reset RL with one task-agnostic reward yields emergent multi-phase dexterity transferring zero-shot at [[2603.15789\|OmniReset]]'s 25% real peg insertion (vs 4% demo-DP). |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2605.16257\|DexJoCo]], [[2510.25725\|HumanoidVTA]] |
| **Key targets** | [[2603.15789\|OmniReset]] 25% real peg insertion (vs 4% demo-DP), emergent multi-phase from one reward; [[2605.03363\|Hierarchical RL-QP Grasp]] 81.4% sim (vs 13.2% end-to-end RL) + 22/26 unseen real; [[2605.09789\|DRIS]] 68% reactive catching zero-shot (vs 5% hand-crafted, 13% sim-trained) |

**Why it matters.** [[2603.15789|OmniReset]] names the failure: "standard exploration in parallel sims suffers performance saturation, agents stuck in local optima despite increased compute," and dexterous RL "requires extensive task-specific engineering for rewards, curricula, demonstrations." The dominant fix throws compute at a fixed setup; [[2603.15789|OmniReset]] inverts it — systematically diverse resets (reaching, near-object, grasp, near-goal) with a *single task-agnostic reward* yield emergent multi-phase behaviors and 25% real peg insertion vs 4% demo-DP. [[2605.03363|Hierarchical RL-QP Grasp]] decomposes task-space RL from joint-space QP (81.4% vs 13.2%), and [[2605.09789|DRIS]] propagates uncertainty for 68% zero-shot catching. The claim: exploration is gated by *initial-state diversity*, not reward shaping — an agent discovers only behaviors whose precursor states it visits, so broadening the reset distribution unlocks emergent dexterity. The Hinton move: favor the mechanism (broad exploration → emergent skill) over the convention (per-task reward shaping).

**First-principles framing.**
- **First principle**: Exploration coverage is set by the initial-state distribution, not reward shaping — a behavior is discoverable only if its precursor states are visited, so reset diversity (not reward density) sets the reachable-behavior ceiling. Emergence is a coverage phenomenon.
- **Assumption being challenged**: That more compute on a fixed reset distribution closes the gap. The field scales parallel envs on a fixed setup and saturates ([[2603.15789|OmniReset]]); diverse resets break saturation where compute alone cannot — the bottleneck is the reset distribution, not compute or reward.
- **The bet**: Diverse-reset RL with one task-agnostic reward yields emergent multi-phase dexterity transferring zero-shot at [[2603.15789|OmniReset]]'s 25% real (vs 4% demo-DP), and task-space/joint-space decomposition reaches [[2605.03363|Hierarchical RL-QP Grasp]]'s 81.4% sim (vs 13.2% monolithic) / 22-26 unseen-object real.

**Evidence.**
- [[2603.15789|OmniReset]] — Diverse simulator resets + large-scale PPO + gSDE, one task-agnostic reward; emergent multi-phase, 25% real peg insertion (vs 4% demo-DP); the reset-diversity anchor.
- [[2605.03363|Hierarchical RL-QP Grasp]] — Task-space RL planner + GPU-parallel joint-space QP; 81.4% sim (vs 13.2% end-to-end RL), 22/26 unseen real, zero-shot steerable; the decomposition anchor.
- [[2605.09789|DRIS]] — Domain-Randomized Instance Set (particle belief propagation); 68% reactive catching zero-shot (vs 5% hand-crafted, 13% sim-trained); uncertainty-aware exploration.
- [[2210.13702|DeXtreme]] — VADR breaks manual-DR saturation; 27.8 vs 14.8; automatic randomization as exploration breadth.
- [[2601.02778|Force-Based Sim2Real]] — Asymmetric actor-critic PPO + randomized actuator; 25.1 rotations; large-scale RL sim-to-real.

**Concrete research questions.**
1. **Q1 — Reset-diversity vs reward-shaping.** Fix the reward task-agnostic, vary only reset diversity ([[2603.15789|OmniReset]]'s reaching/near-object/grasp/near-goal) — does diversity alone produce emergent multi-phase behavior?
2. **Q2 — Decomposition vs monolithic RL.** Compare [[2605.03363|Hierarchical RL-QP Grasp]]'s task-RL + joint-QP against end-to-end RL at matched compute — does decomposition recover the 81.4% vs 13.2% gap and transfer better?
3. **Q3 — Uncertainty-propagation as robustness.** Does [[2605.09789|DRIS]]'s instance-set belief propagation (68% vs 13%) generalize beyond catching to in-hand reorientation under uncertainty?
4. **Q4 — Emergent → distillation.** Distill the emergent RL policy into a deployable visuomotor policy ([[2603.15789|OmniReset]]'s 25% real) — does the behavior survive distillation and beat demo-cloning?

**Related research papers.**
- [[2603.15789|OmniReset]] — Diverse resets + large-scale RL; 25% real peg insertion; the anchor.
- [[2605.03363|Hierarchical RL-QP Grasp]] — Task-space RL + joint-space QP; 81.4% sim, 22/26 real; decomposition.
- [[2605.09789|DRIS]] — Domain-randomized instance set; 68% reactive catching; uncertainty-aware exploration.
- [[2210.13702|DeXtreme]] — VADR breaks DR saturation; 27.8 vs 14.8; automatic randomization.
- [[2601.02778|Force-Based Sim2Real]] — Asymmetric PPO + randomized actuator; 25.1 rotations; large-scale RL.
- [[2605.05172|Q2RL]] — BC-to-RL on-robot self-improvement; 3.75× in 1–2 hrs; real-world RL refinement of emergent policies.
- [[2410.21845|HIL-SERL]] — Human-in-the-loop sample-efficient real RL; the real-RL baseline emergent policies compete with.
- [[2605.16257|DexJoCo]] — 11-task dexterous benchmark; the evaluation suite for emergent multi-task dexterity.

**Benchmarks & metrics.**
- [[2603.15789|OmniReset]] — 25% real peg insertion (vs 4% demo-DP), emergent multi-phase across 6 tasks; the reset-diversity metric.
- [[2605.03363|Hierarchical RL-QP Grasp]] — 81.4% sim (vs 13.2% end-to-end RL), 22/26 unseen real; the decomposition metric.
- [[2605.09789|DRIS]] — 68% reactive catching zero-shot (vs 5% hand-crafted, 13% sim-trained); the uncertainty-robustness metric.

> [!warning] Risks
> - **Reset diversity may need task knowledge** — defining "near-object/near-goal" resets is itself a design choice. → Q1 tests whether generic reset diversity suffices; report the reset-design effort vs reward-design effort it replaces.
> - **Sim-to-real for emergent policies is fragile** — [[2603.15789|OmniReset]]'s 25% real is low. → Frame as a zero-shot floor; couple to [[2605.09789|DRIS]]/[[2210.13702|DeXtreme]] randomization and [[2605.05172|Q2RL]] on-robot refinement to lift it.
> - **Emergent behaviors may be unsafe** — unconstrained exploration can produce damaging contacts. → Bound with D4's QP/force-safety; report contact-force statistics during emergent rollouts.

### D4 — Force-Safety-Constrained Dexterous Control

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | Safety is a hard constraint on the contact-force state that must hold *every* step — a learned policy can only softly penalize violations, but a physics-based filter can guarantee them. The field hopes learned policies stay safe via reward penalties. The bet: a QP/force-bounded controller delivers guaranteed-safe dexterity at [[2605.03363\|Hierarchical RL-QP Grasp]]'s 81.4% (vs 13.2% unconstrained RL), bounding contact force below [[2602.19764\|Multi-Sensory Sparse Experts]]' ~10 N and [[2509.18830\|DexSkin]]'s 1.53 kPa fragile-object limits. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2510.25725\|HumanoidVTA]], [[2605.16257\|DexJoCo]] |
| **Key targets** | [[2605.03363\|Hierarchical RL-QP Grasp]] 81.4% sim + 22/26 unseen real with QP-enforced collision/joint/velocity limits + zero-shot steerability; [[2602.19764\|Multi-Sensory Sparse Experts]] ~10 N stable force + 80 ms compliance; [[2509.18830\|DexSkin]] 90% pressure reduction to 1.53 kPa on fragile objects |

**Why it matters.** Dexterous policies (D1–D3) contact objects with high-DoF hands; without explicit safety, emergent or transferred policies apply damaging force — [[2602.19764|Multi-Sensory Sparse Experts]] documents baselines with "hazardous force surges," and fragile-object tasks ([[2509.18830|DexSkin]]'s blueberries, [[2603.15257|HapticVLA]]'s eggs) fail without force-bounding. The field largely *hopes* learned policies stay safe via reward penalties. [[2605.03363|Hierarchical RL-QP Grasp]] does it properly: a GPU-parallel QP controller "strictly enforces collision avoidance, joint position, and velocity limits," keeping the RL policy "within kinematically feasible and safe regions" (81.4% vs 13.2% unconstrained, zero-shot steerable). [[2602.19764|Multi-Sensory Sparse Experts]] holds ~10 N, and [[2509.18830|DexSkin]] derives interpretable force for a pressure-bounded reward. The claim: safety is a *hard constraint* — a learned policy softly penalizes, a physics-based filter guarantees — so safety belongs in the controller, not the reward.

**First-principles framing.**
- **First principle**: Safety is a hard constraint on the contact-force and kinematic state (force ≤ tolerance, joints within limits, no collision) that must hold *every* step, not in expectation. A policy optimizing expected reward can't guarantee a per-step constraint; a physics-based projection (QP / force-bound) can.
- **Assumption being challenged**: That safety emerges from reward penalties. The field penalizes excess force and hopes; [[2605.03363|Hierarchical RL-QP Grasp]]'s QP-enforced limits show a policy operating *inside* a hard-constraint filter is both safer and trains better (81.4% vs 13.2%) — reward-penalty safety is neither guaranteed nor optimal.
- **The bet**: A QP/force-bounded controller delivers guaranteed-safe dexterity at [[2605.03363|Hierarchical RL-QP Grasp]]'s 81.4% (vs 13.2% unconstrained RL), bounds force below [[2602.19764|Multi-Sensory Sparse Experts]]' ~10 N and [[2509.18830|DexSkin]]'s 1.53 kPa, and adds zero-shot steerability (post-hoc speed-safety tuning without retraining).

**Evidence.**
- [[2605.03363|Hierarchical RL-QP Grasp]] — Task-space RL + GPU-parallel QP enforcing collision/joint/velocity limits; 81.4% sim (vs 13.2% end-to-end RL), 22/26 unseen real, zero-shot steerability; the hard-constraint-controller anchor.
- [[2602.19764|Multi-Sensory Sparse Experts]] — Multi-sensory DiT with 6-axis force; stable ~10 N, 80 ms compliance (vs baseline force surges); the force-stability anchor.
- [[2509.18830|DexSkin]] — Interpretable contact force for pressure-bounded reward; 90% reduction to 1.53 kPa, 20%→60% fragile-fruit integrity; the fragile-object force-bound anchor.
- [[2603.15257|HapticVLA]] — Safety-Aware Reward-Weighted Flow Matching penalizing excess force/slip; 86.7%, +45 pp egg; safety-aware training (soft, complementary to hard QP).
- [[2509.19696|Diffusion Impedance Learning]] — Diffusion-based impedance for compliant contact; impedance as the soft-constraint mechanism.

**Concrete research questions.**
1. **Q1 — Hard QP vs soft reward penalty.** Compare [[2605.03363|Hierarchical RL-QP Grasp]]'s QP-filter against [[2603.15257|HapticVLA]]'s reward-penalty on force-violation rate and SR — does the hard filter guarantee safety *and* improve SR (81.4% vs 13.2%)?
2. **Q2 — Force-bound as control-time projection.** Project policy actions onto a force-bounded feasible set ([[2509.18830|DexSkin]]'s 1.53 kPa) — does projection preserve fragile-object integrity better than penalty-trained policies?
3. **Q3 — Zero-shot steerability.** [[2605.03363|Hierarchical RL-QP Grasp]] tunes speed-safety post-training; quantify how far the trade-off moves without retraining — is the QP-filter the enabler?
4. **Q4 — Safety filter over emergent/transferred policies.** Wrap D3's emergent or D1's transferred policy in the QP/force-bound filter — does it make unconstrained exploration/transfer deployable without retraining?

**Related research papers.**
- [[2605.03363|Hierarchical RL-QP Grasp]] — Task-space RL + joint-space QP hard constraints; 81.4% vs 13.2%; the anchor.
- [[2602.19764|Multi-Sensory Sparse Experts]] — 6-axis force fusion; ~10 N stable, 80 ms compliance; force-stability.
- [[2509.18830|DexSkin]] — Pressure-bounded reward from interpretable force; 1.53 kPa, 20%→60% integrity; fragile-object bound.
- [[2603.15257|HapticVLA]] — Safety-aware reward-weighted flow matching; soft safety (complementary).
- [[2509.19696|Diffusion Impedance Learning]] — Diffusion-based impedance; compliant-contact soft constraint.
- [[2601.02778|Force-Based Sim2Real]] — Fingertip-force + joint-torque rewards; force-adaptive grasping; force-reward design.
- [[2605.05172|Q2RL]] — Auxiliary BC loss for safe on-robot RL; safer exploration; avoids robot faults.
- [[2605.09789|DRIS]] — Uncertainty propagation for robust control; the uncertainty-aware safety substrate.

**Benchmarks & metrics.**
- [[2605.03363|Hierarchical RL-QP Grasp]] — 81.4% sim (vs 13.2% unconstrained), 22/26 unseen real, QP-enforced limits, zero-shot steerability; the hard-constraint metric.
- [[2602.19764|Multi-Sensory Sparse Experts]] — ~10 N stable force, 80 ms compliance (vs baseline surges); the force-stability metric.
- [[2509.18830|DexSkin]] — 90% pressure reduction (14.5→1.53 kPa), blueberry integrity 20%→60%; the fragile-object safety metric.

> [!warning] Risks
> - **QP clamping can hurt task SR** — [[2605.03363|Hierarchical RL-QP Grasp]] notes tracking errors from clamping infeasible velocities. → Report the safety-vs-SR trade-off; the filter should clamp rarely on feasible tasks.
> - **Force tolerances are object-specific** — 1.53 kPa for berries differs from rigid assembly. → Make the bound a per-object parameter (couples to A1's affordance/A3's deformable); don't use a single global force limit.
> - **Hard constraints may over-restrict emergent behavior** — D3's emergent dexterity might need transient high forces. → Q4 tests the filter over emergent policies; tune the constraint to allow task-necessary force while blocking damage.

---

## Cluster E — Tactile Foundations & Data Substrates

*The foundation layer for force-aware manipulation that needs no runtime tactile hardware — sensor-free force-awareness and a cross-sensor (sensor-invariant) representation.*

### E1 — Sensor-Free Force-Aware Policies

| | |
|---|---|
| **Cluster** | E — Tactile Foundations & Data Substrates |
| **Thesis** | Tactile-awareness is a learned behavior grounded in force — the object moves *because* of force, so the awareness is separable from the sensor that taught it. The field assumes contact-competent policies need tactile hardware at deployment. The bet: both routes clear ≥80% of a tactile-instrumented policy at zero runtime tactile cost — ego-video pretraining reaches ≥80% of its SR on [[2505.22159\|ForceVLA]]'s 5 tasks while riding [[2602.16710\|EgoScale]]'s curve to **+54%** on 22-DoF dexterous, and teacher-distillation matches [[2603.15257\|HapticVLA]]'s **86.7%** sensor-free mean (**+45 pp** on the fragile egg vs [[2506.01844\|SmolVLA]]) and [[2603.04531\|PTLD]]'s **+182%** rotation / **+57%** reorientation gain. |
| **Anchor surveys** | [[2604.27621\|Robot Learning from Human Videos Survey]], [[2604.15395\|Foundation Models in Robotics Survey]], [[2510.24795\|Efficient VLA Survey]], [[2504.03515\|Dexterous IL Survey]], [[2511.02097\|WM Manipulation Survey]] |
| **Key targets** | **Route 1 (ego-video pretraining, no tactile at any stage):** ≥80% of tactile-instrumented SR on [[2505.22159\|ForceVLA]] 5 tasks; [[2602.16710\|EgoScale]] **+54%** on 22-DoF dexterous. **Route 2 (teacher-distillation, sensor dropped at inference):** [[2603.15257\|HapticVLA]] **86.7%** sensor-free + **+45 pp** on the egg vs SmolVLA; [[2603.04531\|PTLD]] **+182%** rotation / **+57%** reorientation goals; [[2601.02778\|Force-Based Sim2Real]] 25.1 vs 1.1 in-hand rotations |

**Why it matters.** The field assumes tactile *awareness* needs tactile *hardware* at runtime — and pays in hardware cost and per-platform irreproducibility. [[2504.03515|Dexterous IL Survey]] names it: tactile sensors "lead to increased hardware cost, reduced reproducibility, and compatibility issues across platforms" ([[2603.15257|HapticVLA]]). But awareness and sensor are separable, and two routes prove it from opposite ends of the pipeline.

*Route 1 — pretrain force-awareness, never touch a tactile sensor.* [[2505.22159|ForceVLA]]'s 244-trajectory dataset is 4 orders smaller than [[2310.08864|OXE]] ([[2604.15395|Foundation Models in Robotics Survey]]'s named bottleneck), while [[2602.16710|EgoScale]] shows a 20,854-hour log-linear curve up to **+54%** on 22-DoF dexterous, and [[2510.24795|Efficient VLA Survey]] names internet-scale human video as a dominant data lever. No paper yet trains a force-aware policy from ego video *alone* — the unattacked gap.

*Route 2 — keep a tactile teacher at training, drop the sensor at inference.* [[2603.15257|HapticVLA]] distills a tactile teacher into a sensor-free student predicting a tactile token from vision (86.7%, +45 pp on egg vs SmolVLA), and [[2603.04531|PTLD]] distills privileged-sensor oracles into a deployable estimator (+182% rotation, +57% goals) *without ever simulating tactile*.

The unification: force is causally upstream of contact behavior, so tactile competence is a behavior internalized during training — the sensor is the *teacher signal*, not a runtime dependency. Route 1 supplies it implicitly from ego video's force-consequences; Route 2 supplies it explicitly from an instrumented teacher whose sensor is then dropped. Both land on sensor-free, contact-competent deployment, and both are the deployment twin of B1/B2's training-time contact modeling. E2 (see [[#E2 — Cross-Sensor Tactile Foundation Models for Plug-And-Play Force-Aware Policies|E2]]) makes either route portable across platforms; D2 (see [[#D2 — Tactile In-Hand Reorientation with Sim-to-Real|D2]]) is the in-hand sibling on the reorientation task.

**First-principles framing.**
- **First principle** *(both routes)*: Tactile-awareness is a learned behavior grounded in force — force is *upstream* of vision in contact (the object moves *because* of force), and the awareness maps (vision, state, action) to contact-appropriate force-modulation. That behavior is *separable* from the sensor that supervised it: the sensor is a training signal, not a runtime input. Vision-to-tactile is a well-posed inverse problem because force leaves visible consequences.
- **Assumption being challenged**: That contact-competent policies need tactile data at training *and* tactile hardware at deployment. Route 1 refutes the training half — [[2602.16710|EgoScale]]'s log-linear curve shows vision-only training transfers to tactile-rich tasks at scale. Route 2 refutes the deployment half — [[2603.15257|HapticVLA]] and [[2603.04531|PTLD]] both deploy contact-competent behavior with the sensor removed.
- **The bet** *(both routes, one bar)*: Both clear ≥80% of a tactile-instrumented policy at zero runtime tactile cost. Route 1 — a policy pretrained on ~20k hr of ego *video alone* reaches ≥80% of tactile-instrumented SR on [[2505.22159|ForceVLA]]'s 5 tasks, riding [[2602.16710|EgoScale]]'s curve to **+54%** on 22-DoF dexterous. Route 2 — teacher-distillation matches [[2603.15257|HapticVLA]]'s **86.7%** sensor-free mean (**+45 pp** egg vs SmolVLA) and [[2603.04531|PTLD]]'s **+182%** rotation / **+57%** goals — the sensor never rides along at inference either way.

**Evidence.**
- [[2603.15257|HapticVLA]] *(Route 2 anchor)* — Safety-Aware Reward-Weighted Flow Matching teacher + tactile distillation into a sensor-free student predicting a tactile token from vision; **86.7%** mean, **+45 pp** on the egg vs SmolVLA, 75% with sensor; the distillation anchor.
- [[2603.04531|PTLD]] *(Route 2 anchor)* — Privileged-sensor oracle in sim → deployable estimator from real pairs, *no tactile simulation*; **+182%** rotation, **+57%** goals; the privileged-to-real anchor (also D2's).
- [[2602.16710|EgoScale]] *(Route 1 anchor)* — 20,854-hr log-linear curve; **+54%** on 22-DoF dexterous; the ego-video scaling law (no force head — the gap Route 1 attacks).
- [[2605.13083|TouchAnything]] *(Route 1 substrate)* — First multi-view ego + bimanual dense tactile dataset (20 hr); view dropout cuts ego-only drop **−27.20% → −5.78%**; the vision-to-tactile substrate.
- [[2601.02778|Force-Based Sim2Real]] *(Route 2 teacher)* — Distance-field tactile sim + calibration; 25.1 vs 1.1 in-hand rotations; the efficient tactile-sim teacher.
- [[2410.24090|Sparsh]] / [[2506.14754|Sparsh-X]] — SSL touch foundation (460k–1M unlabeled), **500%** plug-insertion gain (to 90% SR); the representation both routes distill toward.
- [[2507.15597|Being-H0]] / [[2605.00078|Being-H0.7]] — Full policy pretraining on UniHand (150M instruction-motion pairs); Route 1's ego backbone.

**Concrete research questions.**
1. **Q1 — Route comparison at matched SR.** Run both routes against the *same* sensor-free target — which recovers more tactile-instrumented SR on [[2505.22159|ForceVLA]]'s 5 tasks, and where do failure modes differ (Route 1 weak on vision-uncorrelated slip, Route 2 weak on novel objects)?
2. **Q2 — Vision-to-tactile at scale (Route 1).** Extend [[2605.13083|TouchAnything]]'s view-dropout to [[2602.16710|EgoScale]] volume; generate synthetic tactile via a [[2506.14754|Sparsh-X]] teacher on a small instrumented fraction, feed into a [[2505.22159|ForceVLA]]-style FVLMoE — does predicted-tactile recover real-tactile SR?
3. **Q3 — Tactile-token prediction vs world model (Route 2).** Compare [[2603.15257|HapticVLA]]'s vision→tactile-token prediction against B1's world-model forecast (see [[#B1 — Predictive-Tactile Contact Imagination|B1]]) — which transfers more teacher competence?
4. **Q4 — Privileged-to-real on assembly (Route 2).** Replicate [[2603.04531|PTLD]]'s no-tactile-sim distillation on assembly (vs in-hand) — does it avoid the tactile sim-to-real gap on [AutoMate](https://arxiv.org/abs/2407.08028)?
5. **Q5 — Cross-embodiment force transfer (Route 1).** Human hand → gripper: compare explicit ([[2507.15597|Being-H0]] MANO + GRQ-VAE), keypoint ([[2512.22414|π0.5 + ego]]), and learned projections for carrying ego-video force-awareness onto a robot.
6. **Q6 — Shared sensor-free benchmark.** Re-run [[2505.22159|ForceVLA]] + [[2603.15169|ForceVLA2]] with *both* routes head-to-head against a tactile-instrumented baseline — the comparison no benchmark isolates.

**Related research papers.**
- [[2603.15257|HapticVLA]] — Teacher-student distillation to a sensor-free student; **86.7%** mean, **+45 pp** egg; the Route-2 anchor.
- [[2603.04531|PTLD]] — Privileged tactile latent distillation, no tactile sim; **+182%** rotation; the Route-2 privileged-to-real anchor (shared with D2).
- [[2602.16710|EgoScale]] — 20,854-hr ego log-linear curve; **+54%** dexterous; the Route-1 scaling law, no force head.
- [[2605.13083|TouchAnything]] — Multi-view ego + bimanual dense tactile (20 hr); view dropout closes the ego-only gap; the Route-1 data substrate.
- [[2601.02778|Force-Based Sim2Real]] — Distance-field tactile sim + calibration; 25.1 vs 1.1 rotations; the Route-2 tactile-sim teacher.
- [[2601.20321|TaF-VLA]] — 10M tactile-force pairs + VQ-VAE; **60.3%** cross-sensor; the consumed-force contrast (neither ego-predicted nor distilled-away).
- [[2506.14754|Sparsh-X]] — Multisensory touch foundation (1M contacts); the SSL encoder both routes distill toward.
- [[2603.15169|ForceVLA2]] — Hybrid force-position; **66%** avg; deploys without inference-time tactile (Route-2-adjacent).
- [[2509.07962|TA-VLA]] — Sensorless torque from motor current; charger 0/20→17/20; the no-sensor proxy (a cheap Route-2 floor).
- [[2507.15597|Being-H0]] / [[2605.00078|Being-H0.7]] — Full policy pretraining on UniHand (150M pairs); the Route-1 ego backbone.

**Benchmarks & metrics.**
- ForceVLA-Data (244 traj) — Contact-rich 5-task; the shared head-to-head (both routes vs tactile-instrumented), the comparison no benchmark currently isolates.
- [[2603.15257|HapticVLA]] — 86.7% on jar/waffle/egg, +45 pp egg vs SmolVLA, 75% with sensor; the Route-2 metric.
- [[2603.04531|PTLD]] — +182% in-hand rotation, +57% goals, slip/mass/wrist robust; the Route-2 privileged-to-real metric.
- [[2605.21429|roto 2.0]] — Tactile RL olympiad; blind-agent SOTA (Baoding 13 rotations) sets the no-tactile ceiling.
- [[2510.25725|HumanoidVTA]] — 2,124-sensor humanoid tactile; the cross-embodiment substrate for imagined-vs-measured force.

> [!warning] Risks
> - **Vision-to-tactile noise floor (Route 1)** — subtle slip needs fingertip pressure, not vision. → Bound the claim to vision-correlated force; report the floor explicitly.
> - **Distillation gap on novel objects (Route 2)** — the student may fail where the teacher's tactile was load-bearing. → Bound to in-distribution contact; report the teacher-student gap per object class.
> - **Scaling / instrumentation cost** — Route 1's 20k+ hr is expensive; Route 2 needs an instrumented teacher cell. → For Route 1, use [[2506.14754|Sparsh-X]] as a synthetic-tactile teacher on a small fraction; for Route 2, treat the cell as a one-time cost.
> - **Sensorless torque is coarse / embodiment mismatch** — [[2509.07962|TA-VLA]]'s current-derived torque misses fine slip, and 22-DoF human vs 1–7-DoF grippers leaves an action-space gap. → Q1 and Q5 set which regimes each route owns.

### E2 — Cross-Sensor Tactile Foundation Models for Plug-And-Play Force-Aware Policies

| | |
|---|---|
| **Cluster** | E — Tactile Foundations & Data Substrates |
| **Thesis** | Force is a physical quantity whose representation differs across sensors only in measurement basis, not in signal. The field assumes each new sensor is a data-collection restart. The bet: a force-grounded SSL encoder retains ≥80% of its in-distribution SR when zero-shot transferred to a held-out sensor (current ceiling: [[2601.20321\|TaF-VLA]] **60.3%**), making tactile-aware policies deployable across the sensor ecosystem without per-platform fine-tuning. |
| **Anchor surveys** | [[2604.27621\|Robot Learning from Human Videos Survey]], [[2604.15395\|Foundation Models in Robotics Survey]], [[2604.16592\|Cognition WM Survey]] |
| **Key targets** | >80% cross-sensor zero-shot SR (current ceiling: [[2601.20321\|TaF-VLA]] **60.3%**); **86.7%** sensor-free deploy ([[2603.15257\|HapticVLA]]) |

**Why it matters.** [[2604.15395|Foundation Models in Robotics Survey]] flags tactile scarcity as a top-3 bottleneck, [[2604.27621|Robot Learning from Human Videos Survey]] names tactile incorporation as one of 7 open problems, and [[2604.16592|Cognition WM Survey]] names tactile-perception under-represented. The architecture has converged ([[2603.15169|ForceVLA2]] 66% avg SR, +48 pp over [[2410.24164|π0]]) but every new platform restarts data collection: [[2410.24090|Sparsh]] / [[2506.14754|Sparsh-X]] train *per-sensor*, and [[2601.20321|TaF-VLA]]'s 60.3% cross-sensor SR is not deployment-ready. The [[2304.07193|DINOv2]] analog for touch — invariant to sensor basis — does not yet exist. E2 is the **deployment-substrate** twin of E1: E1 gets force-awareness to deployment with no runtime tactile sensor (see [[#E1 — Sensor-Free Force-Aware Policies|E1]]), E2 makes the resulting policy portable across sensors — the encoder D2's estimator and E1's distilled student both inherit.

**First-principles framing.**
- **First principle**: Force is a *physical quantity*; its representation across sensors (capacitive, piezoresistive, vision-tactile) differs only in measurement basis, not signal. A representation aligned to the physical force vector — not the raw output — is invariant by construction.
- **Assumption being challenged**: That cross-sensor transfer requires per-sensor data. The field treats each new sensor as a restart; [[2506.14754|Sparsh-X]] showed multi-sensor SSL works within its training set — the open question is whether it generalizes to *unseen* sensors.
- **The bet**: A force-grounded SSL encoder retains ≥80% of its in-distribution SR when zero-shot transferred to a held-out sensor (ceiling: 60.3% via [[2601.20321|TaF-VLA]]), making tactile-aware policies deployable across the sensor ecosystem without per-platform fine-tuning.

**Evidence.**
- **Sensors**: [[2509.18830|DexSkin]] (capacitive, 294° coverage), [[2604.28156|FlexiTac]] ($30 piezoresistive), [[2604.20689|FingerEye]] (vision-tactile fingertip), GelSight/DIGIT.
- **SSL foundations**: [[2410.24090|Sparsh]] (460k images, MAE/DINO/JEPA), [[2506.14754|Sparsh-X]] (1M contacts, multisensory).
- **Cross-sensor work**: [[2601.20321|TaF-VLA]] (VQ-VAE; **60.3%** zero-shot), [[2509.18830|DexSkin]] (pneumatic calibration).
- **Alignment**: [[2605.14571|MTNet]] (visuo-tactile, CKA ~0.74).
- **Sensor-free deploy**: [[2603.15257|HapticVLA]] (distillation; **86.7%** SR).

**Concrete research questions.**
1. **Q1 — Sensor-invariant SSL objective.** Extend [[2506.14754|Sparsh-X]]'s attention-bottleneck to *cross-sensor* fusion — mask one sensor, predict from another (DINOv2-style EMA teacher).
2. **Q2 — Force-as-bridge grounding.** Extend [[2601.20321|TaF-VLA]]'s VQ-VAE alignment across *all* sensor types, not just families.
3. **Q3 — Cross-sensor benchmark.** Train on N−1 sensors, evaluate held-out across [[2410.24090|Sparsh]] TacBench. Target >80% in-dist retention.
4. **Q4 — Cross-sensor policy fine-tuning.** Bolt encoder onto [[2603.15169|ForceVLA2]] Cross-Scale MoE; test whether the geometric-foundation-model integration lessons of [[2605.24642|GFM-VLA Study]] transfer to the tactile-foundation case.
5. **Q5 — Deployment chain validation.** Train one sensor → deploy another; [[2604.28156|FlexiTac]]'s Kelvin-Voigt sim-to-real protocol as reference.

**Related research papers.**
- [[2410.24090|Sparsh]] — SSL touch foundation (460k images); per-sensor only.
- [[2506.14754|Sparsh-X]] — Multisensory (1M contacts); multi-sensor SSL but not cross-sensor invariant.
- [[2601.20321|TaF-VLA]] — VQ-VAE force latent; **60.3%** cross-sensor ceiling.
- [[2509.18830|DexSkin]] — Capacitive tactile sensor (294° coverage); single-sensor.
- [[2604.28156|FlexiTac]] — $30 piezoresistive; Kelvin-Voigt sim-to-real; single-sensor.
- [[2604.20689|FingerEye]] — Vision-tactile fingertip sensor; single-sensor.
- [[2603.15169|ForceVLA2]] — Cross-scale MoE + force prompts; **66%** avg SR; **+48 pp** over [[2410.24164|π0]]; consumes per-sensor tactile.
- [[2603.15257|HapticVLA]] — Teacher-student distillation; **86.7%** sensor-free; distills, doesn't represent invariantly.
- [[2605.14571|MTNet]] — Visuo-tactile alignment; CKA ~0.74; alignment metric, not a transferable encoder.
- [[2605.24642|GFM-VLA Study]] — Geometric foundation models × policy; Early Fusion **+5.56 pp** on G1; the foundation-model-integration playbook E2 borrows for the tactile case.

**Benchmarks & metrics.**
- [[2605.21429|roto 2.0]] — Tactile RL olympiad; cross-morphology blind-agent benchmark; substrate for held-out-sensor evaluation.
- ForceVLA-Data — Contact-rich 5-task set; end-task SR for the cross-sensor encoder.
- [[2510.25725|HumanoidVTA]] — 2,124-sensor humanoid tactile; multi-sensor zero-shot test bed.

> [!warning] Risks
> - **Fundamental sensor incompatibility** — capacitive vs piezoresistive vs vision-tactile may require discarding task-relevant detail to be invariant. → Ground the representation to the physical force vector (Q2) rather than raw output; report what detail is lost.
> - **Recursive data problem** — SSL needs many sensors' data, but data is missing *because* transfer is the bottleneck. → Bootstrap from [[2506.14754|Sparsh-X]]'s existing multi-sensor corpus and treat new sensors as held-out, not training targets.
> - **60.3% ceiling may be the visual-to-tactile floor** — the bottleneck could be fundamental, not data-limited. → Run Q3's N−1 held-out protocol first as a go/no-go before committing to a full encoder.

---

## Cross-Cutting Themes

> [!tip] Contact Is a First-Class Predicted Quantity, Not a Consumed Observation
> B1, B2, C3, and D2 all invert the force-as-input convention into force-as-modeled-quantity at four points in the stack: B1 predicts the tactile *future* ([[2512.23864|DreamTacVLA]] 95.0% Peg-in-Hole), B2 makes contact *mode* a discrete predicted latent, C3 makes inter-arm *force* the bimanual coordination variable ([[2604.20444|VTouch++]]'s synchronized channel), and D2 distills *privileged* contact state into a deployable estimator ([[2603.04531|PTLD]] +182%). [[2603.05687|CGP]]'s coupled state+tactile prediction and [[2603.19201|OmniVTA]]'s world model are the shared mechanism — model the contact, don't just react to it.

> [!tip] The Privileged-to-Deployable Distillation Interface Is the Sim-to-Real Workhorse
> E1 (Route 2), D1, and D2 route competence through a teacher-student gap where the teacher has privileged access the student lacks: E1 turns a tactile teacher into a sensor-free student ([[2603.15257|HapticVLA]] 86.7%), D2 distills privileged object-pose oracles into real estimators *without tactile sim* ([[2603.04531|PTLD]] +182%), and D1 distills cross-morphology intent from privileged multi-hand training ([[2603.22264|UniDex]] 60%/40%). The non-obvious point: the *interface* (what privileged signal the teacher exposes) matters more than the policy — [[2603.04531|PTLD]]'s insight that a *real* privileged sensor beats a *simulated* tactile one reframes sim-to-real, and E1 and D1 inherit it. The deployment counterpart to [[Sim2Real|Sim2Real]]'s teacher-student threads.

> [!tip] Morphology-Invariant Structure Is the Lever for Cross-Hand Transfer
> A2 and D1 share a bet pixel-and-joint-space approaches miss: grasp *function* and control *intent* are low-dimensional morphology-invariants, while joint-space geometry is the hand-specific projection. A2 transfers the grasp ([[2603.22264|UniDex]]'s FAAS, [[2505.21864|DexUMI]]'s relative-finger actions), D1 transfers the in-hand control policy ([[2512.13644|DexWM]]'s hand-keypoint dynamics) — both succeed where [[2605.16257|DexJoCo]]'s joint-space multi-task training *degrades*. They are *separable* bets, not one stated twice: A2 owns the **grasp-establishment** phase (scored on grasp-transfer SR), D1 owns the **in-hand-control** phase after the grasp (scored on [[2512.13644|DexWM]]'s reach/grasp/place, which A2 cannot claim). A policy can transfer the grasp without the subsequent reorientation, so each phase needs a distinct invariant. The Hinton move: favor the representation the *task* makes invariant over the one the *hardware* imposes — a hand is a hand regardless of finger count.
>
> Composition over monolithic scale (C1's [[2511.05275|TwinVLA]]) is the same lever at the bimanual scale: the single-arm *skill* is the invariant, the cross-arm *coupling* the scarce specific term.

> [!tip] Exploration Breadth and Reset Diversity Beat Reward Engineering and Parameter Count
> D3, D4, and B2 converge that the lever for hard contact-rich behavior is *coverage and constraint structure*, not scale: D3's diverse resets break exploration saturation ([[2603.15789|OmniReset]] 25% real vs 4% demo-DP) where compute alone saturates, D4's hard QP/force constraint both guarantees safety and improves training ([[2605.03363|Hierarchical RL-QP Grasp]] 81.4% vs 13.2%), and B2's discrete contact-mode structure beats a bigger smooth policy at the friction-cone boundary. [[2210.13702|DeXtreme]]'s automatic-domain-randomization (27.8 vs 14.8) is the shared mechanism — engineer the *exploration distribution and constraint set*, not the reward or the parameter count.

> [!tip] The Integration Layer Is the Bottleneck — Generated Data and Real Residuals Are the Fix
> C2, B2, and C1 confront the Sim-to-Real Cliff and bimanual data wall the surveys ([[2604.04974|Video-to-Control Survey]], [[2603.15469|RoCo Challenge]], [[2604.05831|BiCoord]]) name as central — and answer with structure, not raw data: C2 generates bimanual data with coordination structure ([[2410.24185|DexMimicGen]] 90% from 40 demos), B2 closes the assembly cliff with a real residual ([[2602.23253|SPARR]] 95–100% [AutoMate](https://arxiv.org/abs/2407.08028)), C1 sidesteps the data wall by composing single-arm priors ([[2511.05275|TwinVLA]] 76% on ~50 episodes). The shared insight: the hard part is connecting a prediction to dependable contact, and the fixes are structured generation + real residuals + composition — not more teleoperation. Cross-ref [[Sim2Real|Sim2Real]] for residual/real-to-sim and [[WAM|WAM]] for imagination-as-data.

> [!tip] Force Is a Foundation Modality With Its Own Scarcity, Not Just an In-Task Signal
> Clusters A–D consume tactile *inside* a phase — B1 predicts the contact future, C3 shares it across two arms, D2 reorients in-hand. Cluster E asks the upstream question: where does the competence come from before any task, and does it ride along to deployment? E1 and E2 are the two unsolved halves — E1 gets force-awareness to deployment with *no runtime tactile sensor* (pretraining from ego video where robot tactile is 4 orders short of [[2310.08864|OXE]], *or* distilling a tactile teacher into a sensor-free student), and E2 builds the sensor-invariant encoder ([[2304.07193|DINOv2]]-for-touch) that makes any force-aware policy portable. The coupling that makes E cross-cutting: E1's distillation route is the sensor-free deployment of B1/B2's training-time contact modeling, and E2's encoder is what E1's student and D2's estimator both inherit. [[2505.22159|ForceVLA]] / [[2603.15169|ForceVLA2]] / [[2603.15257|HapticVLA]] established the in-task architecture; E1 and E2 deploy it without per-platform tactile hardware, with [[2605.21429|roto 2.0]] the shared benchmark.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Affordance-*conditioned* (not post-filtered) grasp generation at task-relevance × stability parity | A1 | [[2604.11674\|AffordSim]] (affordance-guided collection, 79%/64% vs 15%/3%, but generation conditions on affordance separately) + [[2506.17198\|Dex1B]] (scalable stable-grasp, no task-affordance) |
| Function-space cross-morphology *grasp* transfer at in-domain parity | A2 | [[2603.22264\|UniDex]] (FAAS control transfer, 60%/40%, but not grasp-synthesis) + [[2505.21864\|DexUMI]] (cross-hand 86%, exoskeleton-mediated, not zero-shot) |
| Deformable grasping as force-regulation (no defined grasp-pose) with differentiable soft-body | A3 | [[2509.18830\|DexSkin]] (force-regulation, 90% pressure reduction, but rigid skin not soft-body physics) + [[2510.25725\|HumanoidVTA]] (dense soft tactile, no control policy) |
| Tactile-*future* prediction (world model) vs reactive tactile on contact-rich SR | B1 | [[2512.23864\|DreamTacVLA]] (Think–Dream–Act, 95.0% Peg-in-Hole, single system) + [[2603.19201\|OmniVTA]] (visuo-tactile WM + 60 Hz reflexive) |
| Discrete contact-mode latent + reversibility on sub-millimeter insertion | B2 | [[2602.23253\|SPARR]] (95–100% [AutoMate](https://arxiv.org/abs/2407.08028) via real residual, continuous) + [[2502.05086\|REASSEMBLE]] (phase-distinct force patterns, no mode-latent policy) |
| Coordination-native bimanual at single-arm data cost on tightly-coupled tasks | C1 | [[2511.05275\|TwinVLA]] (composed single-arm, 76% on ~50 episodes, moderate coupling) + [[2604.05831\|BiCoord]] (coordination metrics, vision-only, later-stage degradation) |
| Coordination-*structured* bimanual generation closing later-stage degradation | C2 | [[2410.24185\|DexMimicGen]] (90% from 40 demos via subtask taxonomy) + [[2506.18088\|RoboTwin 2.0]] (MLLM-gen + randomization, +24.4% few-shot) |
| Shared inter-arm tactile channel for force-balanced bimanual cooperation | C3 | [[2604.07335\|TAMEn]] (closed-loop tactile bimanual, 75% SR, per-arm) + [[2604.20444\|VTouch++]] (synchronized bimanual tactile data, no shared-channel policy) |
| Universal cross-morphology *in-hand control* (not just grasp) at real-time latency | D1 | [[2603.22264\|UniDex]] (FAAS, 81% progress, 60%/40% transfer) + [[2602.19764\|Multi-Sensory Sparse Experts]] (sparse-MoE scaling, 83.2% MT50, single-hand) |
| Tactile in-hand reorientation *without tactile simulation* under perturbation | D2 | [[2603.04531\|PTLD]] (privileged-to-real, no tactile sim, +182% rotation) + [[2210.13702\|DeXtreme]] (VADR 27.8 vs 14.8, vision/proprioception only) |
| Emergent multi-phase dexterity from reset-diversity (not reward shaping) transferring real | D3 | [[2603.15789\|OmniReset]] (diverse resets, 25% real peg, single reward) + [[2605.03363\|Hierarchical RL-QP Grasp]] (decomposition 81.4% vs 13.2%, no emergence claim) |
| Hard force/kinematic safety *guarantee* (not reward penalty) at task parity | D4 | [[2605.03363\|Hierarchical RL-QP Grasp]] (QP-enforced limits, 81.4%, no fragile-object force bound) + [[2509.18830\|DexSkin]] (1.53 kPa pressure bound, reward-based not guaranteed) |
| Sensor-free force-aware deployment matching sensor-on SR — via ego-only pretraining and via teacher-distillation | E1 | [[2505.22159\|ForceVLA]] (uses real tactile) + [[2602.16710\|EgoScale]] (ego curve, no force head) + [[2603.15257\|HapticVLA]] (sensor-free 86.7%) + [[2603.04531\|PTLD]] (privileged-to-real, in-hand only) + [[2605.21429\|roto 2.0]] (blind-agent ceiling) |
| Cross-sensor tactile held-out-sensor zero-shot transfer | E2 | TacBench (per-sensor, via [[2410.24090\|Sparsh]]) + [[2601.20321\|TaF-VLA]] (60.3% cross-sensor, not deployment-ready) |

---

## Cross-References

- [[02_Dataset-Benchmark-Environment#2. Multi-Modal & Specialist Datasets|02_Dataset-Benchmark-Environment §2]] — Multi-modal manipulation datasets (grasping, dexterous, bimanual)
- [[02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks|02_Dataset-Benchmark-Environment §6]] — Tactile & contact-rich benchmarks (feeds A3, B1–B2, C3, D2, E1)
- [[02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02_Dataset-Benchmark-Environment §8]] — Bimanual & humanoid evaluation (feeds C1–C3)
- [[09_Contact-Rich-and-Whole-Body-Control#3. Force-Conditioned VLA Architectures|09_Contact-Rich-and-Whole-Body-Control §3]] / [[09_Contact-Rich-and-Whole-Body-Control#4. Contact-Rich Manipulation Benchmarks and Visuotactile Policies|§4]] — Force-conditioned VLA architectures + visuotactile policies (feeds B-cluster)
- [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]] — Force-aware design space; the tactile/sensor-substrate deep-dive feeding Cluster D
- [[05_VLA#7. Multi-Sensor & Force-Aware VLAs|05_VLA §7]] / [[05_VLA#8. Humanoid & Bimanual VLAs|§8]] — Multi-sensor + humanoid/bimanual policies (feeds B, C)
- [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Robotics & embodied-AI topic overview
- [[Embodied-AI|Embodied-AI]] — Umbrella directions; develops tool-use and BC/diffusion/policy learning, not re-clustered here.
- [[WAM|WAM]] — World-action-model imagination; B1's tactile world model and A3's deformable dynamics borrow the WAM imagination-as-data and substrate threads.
- [[Sim2Real|Sim2Real]] — Sim-to-real / real-to-sim transfer; owns the deformable soft-body physics (A3), the real-residual machinery (B2), and the tactile sim-to-real story (E1 Route 2, D2).

> [!example] Humanoid reading path
> For a humanoid, this doc's **Bimanual (Cluster C)** + **Dexterous (Cluster D)** are the upper-body manipulation subsystem — two-arm coordination (C1–C3) and in-hand control (D1–D4). The **legs and locomotion** live in the **Locomotion** doc, and the **loco-manipulation coupling** (legs stabilizing the manipulation workspace, whole-body balance during reaching) in the **Whole-Body** doc. Read C+D here for the upper body; the sibling docs for the lower body and the coupling.
