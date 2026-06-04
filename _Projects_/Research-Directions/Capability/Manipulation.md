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
> Thirteen manipulation research directions across four clusters — *Grasping & Grasp Synthesis* (A), *Contact-Rich Assembly & Precision* (B), *Bimanual & Dual-Arm Coordination* (C), and *Dexterous & In-Hand Control* (D) — synthesized from ~20 manipulation/dexterous/tactile surveys and benchmarks plus the frontier methods that set each bet's bar ([[2506.17198|Dex1B]], [[2604.11674|AffordSim]], [[2602.23253|SPARR]], [[2512.23864|DreamTacVLA]], [[2511.05275|TwinVLA]], [[2603.04531|PTLD]], [[2603.15789|OmniReset]]). This doc is the **embodiment-axis Manipulation subsystem** (arms + hands acting on objects) of a 2-axis doc family — it deliberately excludes locomotion (legs/wheels) and whole-body loco-manipulation coupling, which live in the sibling Locomotion and Whole-Body docs, and it cross-references rather than re-clusters the cross-cutting mechanism docs ([[Embodied-AI|Embodied-AI]], [[WAM|WAM]], [[Sim2Real|Sim2Real]]) for tool-use, visuomotor-policy-learning, world-model-imagination, and physics-grounding. Each direction carries an explicit **first-principles framing** (the irreducible structure of the problem, the conventional assumption it breaks, and the measurable bet) and a **non-consensus thesis** chosen for where impactful work deviates from "more data / more scale." Every metric anchor is sourced from a cited `_KnowledgeHub_/{ID}.md` note, never invented.

---

## Methodology

**Scope.** Corpus: ~20 manipulation/dexterous/tactile/bimanual surveys and benchmarks and ~70 manipulation-method papers from `_KnowledgeHub_/`, cross-checked against [[../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] and the `Embodied-AI/` deep-dives ([[../Embodied-AI/02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]], [[../Embodied-AI/10_Force-Aware-and-Tactile-Policies|10_Force-Aware-and-Tactile-Policies]], [[../Embodied-AI/03_VLA|03_VLA]]). The method is survey-grounded ideation — surveys enumerate open problems, benchmarks fix what is measurable, frontier methods fix what is currently achievable, and each direction is filtered and framed by the bullets below. **Subsystem boundary**: legs/wheels locomotion and loco-manipulation coupling are owned by sibling docs and excluded here; tool-use and BC/diffusion/VLA visuomotor-policy-learning are cross-cutting and cross-referenced to the umbrella, not re-clustered; deformable/cloth is a single direction inside Grasping (A3), not its own cluster.

- **Survey enumeration**: tag-scan over `survey` × {`manipulation`, `dexterous`, `tactile`, `VLA`, `world-model`} surfaced [[2504.03515|Dexterous IL Survey]], [[2511.02097|WM Manipulation Survey]], [[2604.04974|Video-to-Control Survey]], [[2507.10672|VLA Manipulation Survey]], [[2508.13073|Large VLM-based VLA Survey]] — each scanned for its named open problems.
- **Deep-dive mining**: full reads of [[../Embodied-AI/10_Force-Aware-and-Tactile-Policies#3. Force-Conditioned VLA Architectures|10_Force-Aware-and-Tactile-Policies §3]], [[../Embodied-AI/10_Force-Aware-and-Tactile-Policies#5. Open Problems & Failure Modes|10 §5]], [[../Embodied-AI/02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks|02_Dataset-Benchmark-Environment §6]], [[../Embodied-AI/02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02 §8]], [[../Embodied-AI/03_VLA#8. Humanoid & Bimanual VLAs|03_VLA §8]]; 3+-way open-problem convergence seeded B1 (contact imagination), C3 (tactile-coupled bimanual), D2 (in-hand sim-to-real).
- **Closest-baseline anchoring**: each direction's bet is pinned to the strongest existing instance it must beat — grasp-synthesis, contact-imagination, coordination-native, and tactile-in-hand papers ([[2506.17198|Dex1B]], [[2604.11674|AffordSim]], [[2512.23864|DreamTacVLA]], [[2602.23253|SPARR]], [[2511.05275|TwinVLA]], [[2603.04531|PTLD]], [[2603.15789|OmniReset]]) set the bar.
- **Filter (maximal, quality-gated)**: admitted every direction that passes all four gates — distinct sub-problem (not a re-slice of a sibling/umbrella direction), KH-sourced measurable bet, non-consensus framing, ≥1 vault anchor with a note. **Cluster C (Non-Prehensile) was assessed and dropped**: only [[2503.16806|DyWA]] carries a note, so the ≥2-anchored-directions gate fails — DyWA is instead folded into B as a dynamics-adaptive contact anchor and cross-referenced.
- **First-principles framing**: each direction states the irreducible structure of the problem, the conventional assumption being challenged, and the non-consensus bet — to surface where impactful work deviates from incremental refinement, not where it follows the herd.

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

> [!tip] Convergence patterns
> - **The integration layer, not the policy, is the bottleneck** (5-way): [[2604.04974|Video-to-Control Survey]] (robotics integration layer is the critical gap), [[2603.15469|RoCo Challenge]] (Sim-to-Real Cliff; modular pipelines brittle), [[2502.05086|REASSEMBLE]] (insert action dominates failures), [[2604.05831|BiCoord]] (degradation in later coordination stages), [[2407.07788|BiGym]] (near-0% on long-horizon) — same diagnosis under different vocabulary: the hard part is connecting a prediction to dependable contact behavior, not generating the prediction. Empirically confirmed by [[2602.23253|SPARR]] (sim base + real residual → 95–100% [AutoMate](https://arxiv.org/abs/2407.08028) where sim-only fails) and [[2407.16677|ResiP]] (residual RL lifts peg-in-hole 5%→99%).
> - **Force/tactile is treated as a consumed input, never a modeled output** (4-way): [[2604.04974|Video-to-Control Survey]], [[2511.02097|WM Manipulation Survey]] (physics-awareness 3rd of 13 capabilities), [[2504.03515|Dexterous IL Survey]] (tactile under-leveraged), [[2510.25725|HumanoidVTA]] (dense tactile discriminative but optimization can't use it) — the field consumes force as a policy feature but rarely predicts it. Now being inverted by predictive-tactile work: [[2512.23864|DreamTacVLA]] (Think–Dream–Act, 95.0% Peg-in-Hole) and [[2603.19201|OmniVTA]] (visuo-tactile world model + 60 Hz reflexive controller) imagine the contact future.
> - **Bimanual data scarcity forces a choice: generate it or avoid needing it** (4-way): [[2506.18088|RoboTwin 2.0]], [[2410.24185|DexMimicGen]] (replay-in-sim data generation), [[2604.05831|BiCoord]], [[2407.07788|BiGym]] (demo-driven benchmarks) all diagnose the dual-arm data wall. Two responses now exist: scale generation ([[2506.18088|RoboTwin 2.0]] +24.4% real few-shot) vs compose single-arm priors ([[2511.05275|TwinVLA]] 76% on ~50 episodes, [[2507.23523|H-RDT]] human-video transfer).
> - **Dexterity emerges from exploration breadth + privileged-to-real distillation, not bigger nets** (3-way): [[2603.15789|OmniReset]] (diverse resets beat exploration saturation; 25% real peg insertion vs 4% DP), [[2603.04531|PTLD]] (privileged tactile latent distillation; +182% rotation), [[2210.13702|DeXtreme]] (automatic domain randomization; 27.8 vs 14.8 reorientations) — the lever is reset/randomization diversity and the privileged→deployable distillation interface, not parameter count.

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

The grasp generator $p(g \mid v)$ must satisfy a **feasibility constraint** (SDF non-penetration + force-closure) that the loss can enforce directly — this is why generation + post-optimization beats pure regression, and why A1 makes the *task-affordance* score $Q(g)$ (not just stability) the conditioning target.

**Contact as a first-class predicted quantity** — [[2603.05687|CGP]]:

> "[Models] often predict kinematic trajectories without explicit contact semantics … CGP … predicts coupled future trajectories of both actual robot state and expected tactile feedback … translated into physically consistent, executable target robot states." — [[2603.05687|CGP]]

This reframes contact-rich manipulation from "predict actions, hope contact works out" to "predict the *contact-state trajectory* $c_{1:T}$ jointly with the action" — the formalism B1 and B2 build on, and the inverse of the field's force-as-input convention.

**Coordination as a non-factorizable joint** — [[2604.05831|BiCoord]]:

> "Tasks specifically designed for long-horizon and tightly coordinated bimanual manipulation … a 4× increase in spatial-temporal integral values vs prior benchmarks; policy performance consistently degraded in later stages." — [[2604.05831|BiCoord]]

Two-arm coordination carries a joint action $a = (a_L, a_R)$ whose value is *not* $V(a_L) + V(a_R)$ — the cross-arm coupling (handover timing, force balance) is the load-bearing term, which is why C1 treats coordination as native structure rather than two independent policies.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Grasping & Grasp Synthesis** | A1, A2, A3 | Generating *task-relevant, feasible* grasps that transfer across objects/morphologies | A1's affordance-scored grasp distribution is the conditioning A2 must keep invariant across hand morphologies; A3 stresses both on deformable objects where the grasp-pose itself is ill-defined; [[2506.17198\|Dex1B]]'s feasibility-constrained generation is the substrate all three scale |
| **B — Contact-Rich Assembly & Precision** | B1, B2, B3 | Sub-millimeter contact behavior where vision is blind and the policy is open-loop | B1's predicted contact-state trajectory is the signal B2 conditions its discrete contact-mode dynamics on; B3 distills B1/B2's tactile-aware behavior into a sensor-free deployable policy; [[2602.23253\|SPARR]]'s real-residual and [[2512.23864\|DreamTacVLA]]'s tactile imagination are the trust valves all three share |
| **C — Bimanual & Dual-Arm Coordination** | C1, C2, C3 | Two arms' coupling is non-factorizable and bimanual data is scarce | C1's coordination-native policy needs the data C2 generates; C2's replay-in-sim pipeline must respect the coupling C1 models; C3 adds the tactile channel that makes force-balanced handovers observable; [[2511.05275\|TwinVLA]]'s composed single-arm priors and [[2506.18088\|RoboTwin 2.0]]'s generation set the bar for C1 and C2 |
| **D — Dexterous & In-Hand Control** | D1, D2, D3, D4 | Multi-fingered contact is high-DoF, discontinuous, and sim-to-real-fragile | D1's cross-morphology action space is what D2's tactile-in-hand policy must deploy onto; D3's exploration-driven dexterity supplies the behaviors D1 unifies; D4 bounds all three with QP/force-safety; [[2603.04531\|PTLD]]'s privileged-to-real distillation and [[2603.15789\|OmniReset]]'s reset diversity are the shared training levers |

---

## Cluster A — Grasping & Grasp Synthesis

*Generating task-relevant, physically feasible grasp poses that transfer across object categories and hand morphologies — including where the grasp-pose itself is ill-defined (deformables).*

### A1 — Task-Affordance-Conditioned Grasp Synthesis

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | Grasp synthesis conditioned on *task affordance* rather than grasp stability — which the field skips because billion-scale generators optimize for stable-but-functionally-blind grasps — has the irreducible truth that the correct grasp is a function of what the object is *for*, not just its geometry, which breaks the assumption that scaling stable-grasp data ([[2506.17198\|Dex1B]]'s 1B demos) eventually yields task-competent grasping, and I bet an affordance-scored grasp generator beats generic stable-grasp estimators by the [[2604.11674\|AffordSim]] margin (79% vs 15% medium / 64% vs 3% hard) while recovering ≥93% of manual-annotation success without per-object labels. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2507.10672\|VLA Manipulation Survey]], [[2506.18448\|GraspMAS]] |
| **Key targets** | [[2604.11674\|AffordSim]] affordance-guided 79% (medium) / 64% (hard) vs AnyGrasp 15% / 3%, ≥93% of manual-annotation success without annotation; match [[2506.17198\|Dex1B]] 86.0% DexGraspNet at task-relevance parity; [[2505.03233\|SynGrasp-1B]] ~90% real zero-shot grasp as the open-vocab reference |

**Why it matters.** The dominant grasp-foundation-model recipe scales stable-grasp data: [[2506.17198|Dex1B]] generates one billion physically-plausible grasps and [[2505.03233|SynGrasp-1B]] pre-trains on a billion synthetic frames to hit ~90% real zero-shot grasping. But [[2604.11674|AffordSim]] shows the limit — generic grasp estimators "select stable but functionally irrelevant grasps," and on affordance-critical tasks AnyGrasp collapses to 15% (medium) / 3% (hard) where affordance-guided collection reaches 79% / 64%. The grasp that holds a hammer is not the grasp that *uses* it. [[2601.07060|PALM]] and [[2506.18448|GraspMAS]] both reach for affordance/language reasoning to pick the grasp, but treat affordance as a separate reasoning stage rather than the generative conditioning. The first-principles move: make the task-affordance score $Q(g)$ the conditioning variable of the grasp generator $p(g \mid v, l)$, not a post-hoc filter — so the generator never proposes functionally-wrong grasps in the first place.

**First-principles framing.**
- **First principle**: A grasp's correctness is defined by the downstream task, not by force-closure alone — the same mug affords a rim-grasp for drinking and a handle-grasp for carrying. Grasp quality is therefore a *conditional* $Q(g \mid \text{task})$, and a generator that marginalizes over task is structurally optimizing the wrong objective.
- **Assumption being challenged**: That scaling stable-grasp data closes the task-competence gap. [[2506.17198|Dex1B]] (1B grasps) and [[2505.03233|SynGrasp-1B]] (1B frames) bet on scale; [[2604.11674|AffordSim]]'s 15%→79% affordance gap shows scale of *stable* grasps does not transfer to *functional* grasps — the data axis is orthogonal to the difficulty.
- **The bet**: An affordance-scored grasp generator beats generic stable-grasp estimators by the [[2604.11674|AffordSim]] margin (79% vs 15% medium, 64% vs 3% hard) and recovers ≥93% of manual-annotation success without per-object annotation, at [[2506.17198|Dex1B]]-class stable-grasp quality (86.0% DexGraspNet) — i.e., task-relevance for free, no stability loss.

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
- [[2604.11674|AffordSim]] — Affordance-aware data generator + 50-task benchmark; 79%/64% vs 15%/3%; the affordance-conditioning anchor.
- [[2506.17198|Dex1B]] — 1B-demo feasibility-constrained generative grasp synthesis; 86.0% DexGraspNet; scalable stable-grasp substrate.
- [[2505.03233|SynGrasp-1B]] — Billion-frame synthetic grasp pre-training, open-vocab; ~90% real zero-shot; stability-scaling reference to beat on task-relevance.
- [[2601.07060|PALM]] — Affordance reasoning + progress-aware policy; +17.7 pp CALVIN; affordance as separate stage, not generative conditioning.
- [[2506.18448|GraspMAS]] — Zero-shot language-driven grasp via multi-agent reasoning; no contact-quality grounding.
- [[2604.11320|CLASP]] — Dual-pathway (semantic + geometric) open-vocab grasping; 87.0% pick SR; mitigates spatial hallucination but stability-centric.
- [[2511.04357|GraSP-VLA]] — Graph-based symbolic action representation for long-horizon grasp planning; symbolic, no generative grasp synthesis.
- [[2605.05925|DexSynRefine]] — HOI generative prior + task-space residual RL; 68.1% sim, real +50–70 pp over retargeting; synthesis-then-ground, complementary refinement.
- [[2506.17198|Dex1B]]'s DexGraspNet baseline — the stable-grasp ceiling A1 must match while adding task-relevance.

**Benchmarks & metrics.**
- [[2604.11674|AffordSim]] — 50-task affordance benchmark; affordance-guided 79%/64% vs generic 15%/3%, real zero-shot 24% avg (Pi 0.5 25%); the affordance-difficulty gradient (placing 40% → hanging 10%).
- DexGraspNet (via [[2506.17198|Dex1B]]) — 86.0% SR, Q1-score 0.125; the stable-grasp-quality floor A1 must not sacrifice.
- [[2604.11320|CLASP]] — 87.0% pick SR in clutter; open-vocab grasp baseline with geometric grounding.

> [!warning] Risks
> - **Affordance-prediction accuracy is the ceiling** — [[2604.11674|AffordSim]] notes VoxAfford accuracy is the primary success factor. → Bound the bet to tasks where the affordance model is reliable; report the affordance-quality vs grasp-success curve, not a single number.
> - **Stable-grasp regression already strong** — [[2505.03233|SynGrasp-1B]] hits ~90% on generic grasping. → Score on affordance-critical tasks (pouring, hanging, tool-use), not headline pick-SR, where the 15%→79% gap lives.
> - **Affordance + stability can conflict** — the functionally-correct grasp may be less stable. → Make $Q$ a tunable product, not a hard constraint; expose the stability-affordance trade-off as a Pareto front.

### A2 — Cross-Morphology Grasp Transfer

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | Grasp policies that transfer zero-shot across hand morphologies via a function-aligned action space — which the field skips because grasp data is collected per-hand and VLAs target parallel-jaw — has the irreducible truth that grasp *function* (oppose-and-close) is morphology-invariant while joint-space grasp *geometry* is not, which breaks the assumption that each new dexterous hand needs its own dataset and policy, and I bet a function-aligned action space achieves zero-shot transfer to unseen hands at [[2603.22264\|UniDex]]'s 60% (Oymotion) / 40% (Wuji) levels while cutting per-hand data cost ≥5×. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2508.13073\|Large VLM-based VLA Survey]], [[2605.16257\|DexJoCo]] |
| **Key targets** | [[2603.22264\|UniDex]] 81% task progress + zero-shot 60% (Oymotion) / 40% (Wuji), 5.2× data-cost reduction; [[2505.21864\|DexUMI]] 86% cross-hand SR + 3.2× collection efficiency; [[2605.16257\|DexJoCo]] cross-hand multi-task transfer (DP-T 50.4%→20.0% under randomization) as the negative-transfer floor |

**Why it matters.** [[2504.03515|Dexterous IL Survey]] names the embodiment gap — "wide variation in DoFs, morphology, and kinematics prevents data and policy transfer" — as a top obstacle, and [[2603.22264|UniDex]] confirms "existing robot foundation policies predominantly cater to parallel-jaw grippers, leaving dexterous manipulation underserved." Every new hand (Allegro, Inspire, XHand, Oymotion, Wuji) today restarts data collection. [[2603.22264|UniDex]]'s Function-Actuator-Aligned Space (FAAS) and [[2505.21864|DexUMI]]'s exoskeleton-mediated human-hand interface both show the gap is bridgeable — FAAS achieves 60%/40% zero-shot transfer to unseen hands and 5.2× data-cost reduction; DexUMI hits 86% across underactuated and fully-actuated hands with 3.2× collection efficiency. The non-consensus claim: the *function* of a grasp (opposition, enclosure, precision-pinch) is a low-dimensional morphology-invariant, and a policy parameterized in function-space transfers where a joint-space policy cannot.

**First-principles framing.**
- **First principle**: A grasp is defined by its functional configuration (which surfaces oppose the object, with what force), not by the specific joint angles that realize it. Functional grasp taxonomy (power / precision / lateral) is a low-dimensional invariant across hands; joint-space realization is the high-dimensional hand-specific projection. The invariant is in the function, the variance is in the kinematics.
- **Assumption being challenged**: That each dexterous hand needs its own dataset and policy. The field collects per-hand because it parameterizes in joint-space; [[2603.22264|UniDex]]'s FAAS and [[2505.21864|DexUMI]]'s relative-finger-action result show function-space (or exoskeleton-normalized) representations transfer — the per-hand-data assumption is an artifact of the wrong parameterization.
- **The bet**: A function-aligned action space achieves zero-shot transfer to unseen hands at [[2603.22264|UniDex]]'s 60% (Oymotion) / 40% (Wuji) levels and cuts per-hand data cost ≥5× ([[2603.22264|UniDex]] 5.2×, [[2505.21864|DexUMI]] 3.2× collection), at [[2505.21864|DexUMI]]-class in-domain SR (86%) — transfer for free, no in-domain regression.

**Evidence.**
- [[2603.22264|UniDex]] — Function-Actuator-Aligned Space unifies control across hands; 81% task progress, zero-shot 60%/40% to unseen hands, 5.2× data-cost cut; the function-space transfer anchor.
- [[2505.21864|DexUMI]] — Human-hand-as-interface via robot-specific exoskeleton + visual inpainting; 86% across Inspire (underactuated) + XHand (fully-actuated), 3.2× efficiency; relative-finger-action transfers better than absolute.
- [[2506.17198|Dex1B]] — 1B grasps across three dexterous hands; cross-hand data substrate, but per-hand policies.
- [[2605.05925|DexSynRefine]] — HOI generative prior + task-space residual; 68.1% sim, +50–70 pp real over retargeting; task-space (not joint-space) action representation is the transfer enabler.
- [[2605.16257|DexJoCo]] — 11-task dexterous benchmark; multi-task training *degrades* (not transfers) for current policies — the negative result motivating function-space.

**Concrete research questions.**
1. **Q1 — Function-space vs joint-space transfer ablation.** Train a grasp policy in [[2603.22264|UniDex]]'s FAAS vs raw joint-space; measure zero-shot SR on a held-out hand — does function-space recover the 60%/40% transfer where joint-space yields ~0%?
2. **Q2 — Functional grasp taxonomy as the latent.** Parameterize the action by a power/precision/lateral grasp-type latent + continuous force; does the discrete grasp-type bottleneck improve cross-morphology transfer over continuous FAAS?
3. **Q3 — Exoskeleton-normalized vs retarget-based data.** Compare [[2505.21864|DexUMI]]'s exoskeleton interface against kinematic retargeting ([[2605.05925|DexSynRefine]]'s max-5.8% retarget baseline) for cross-hand data quality.
4. **Q4 — Why does multi-task dexterous training degrade?** [[2605.16257|DexJoCo]] reports negative transfer; test whether function-space parameterization converts the degradation into transfer.

**Related research papers.**
- [[2603.22264|UniDex]] — Universal dexterous hand control via FAAS from egocentric video; 60%/40% zero-shot, 5.2× cost cut; the function-space anchor.
- [[2505.21864|DexUMI]] — Human hand as universal manipulation interface; 86%, 3.2× efficiency; exoskeleton-normalized transfer.
- [[2605.05925|DexSynRefine]] — Task-space residual RL grounds HOI; +50–70 pp real over retargeting; task-space action representation.
- [[2506.17198|Dex1B]] — 1B grasps over three hands; cross-hand data, per-hand policies.
- [[2605.16257|DexJoCo]] — 11-task dexterous benchmark; multi-task degradation negative result.
- [[2604.20689|FingerEye]] — Per-finger eye-in-hand perception for dexterous control; morphology-specific sensing channel.
- [[2603.04531|PTLD]] — Privileged tactile latent distillation; +182% rotation; the deployable interface a transferred policy needs (feeds D2).
- [[2512.24653|RoboMIND 2.0]] — 310K trajectories across six embodiments; cross-embodiment generalization data substrate.

**Benchmarks & metrics.**
- [[2603.22264|UniDex]] — 81% task progress on 5 tool-use tasks, zero-shot 60% (Oymotion) / 40% (Wuji); the cross-morphology transfer metric.
- [[2605.16257|DexJoCo]] — 11-task MuJoCo dexterous suite; DP-T 50.4%→20.0% under visual randomization, π0.5 highest; multi-task degradation diagnostic.
- [[2505.21864|DexUMI]] — 86% across underactuated + fully-actuated hands; the in-domain SR floor.

> [!warning] Risks
> - **Function-space loses hand-specific dexterity** — fine manipulation may need joint-level control a function-abstraction discards. → Use function-space for the grasp-establishment phase, joint-space residual for fine in-hand (couples to D1).
> - **Transfer rates (40–60%) are not deployment-ready** — [[2603.22264|UniDex]]'s Wuji 40% is a research result. → Frame as few-shot-adaptation seed, not zero-shot deployment; report the few-shot curve from 40% baseline.
> - **Negative-transfer risk** — [[2605.16257|DexJoCo]] shows multi-hand training can degrade. → Q4's degradation-vs-transfer test is the go/no-go before scaling to more hands.

### A3 — Deformable-Object Grasping under Ill-Defined Contact

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | Grasping deformable objects where the grasp-pose itself is ill-defined — which the field skips because grasp synthesis assumes a rigid object with a well-defined 6-DoF pose — has the irreducible truth that for cloth/rope/soft objects the contact configuration is a continuum the gripper *creates* rather than a pose it *finds*, which breaks the assumption that grasp synthesis = pose selection, and I bet a contact-creation policy grounded in dense tactile + differentiable soft-body physics holds where rigid-grasp estimators fail, matching [[2509.18830\|DexSkin]]'s 90% contact-pressure reduction and 20%→60% real-fruit integrity. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2511.02097\|WM Manipulation Survey]], [[2510.25725\|HumanoidVTA]] |
| **Key targets** | [[2509.18830\|DexSkin]] 90% contact-pressure reduction (14.5→1.53 kPa) + blueberry integrity 20%→60%, 19/20 perturbed reorientation; cross-ref [[Sim2Real\|Sim2Real]] for differentiable soft-body physics; [[2510.25725\|HumanoidVTA]] dense-tactile soft-object discrimination |

**Why it matters.** Grasp synthesis (A1, A2) assumes a rigid object with a recoverable 6-DoF pose. Deformables break the premise: a towel, sponge, or blueberry has no canonical grasp-pose — the contact configuration is something the gripper *creates* by how it closes, and the "right" grasp depends on force you must regulate, not geometry you can localize. [[2510.25725|HumanoidVTA]] documents that soft-object manipulation "induces dynamic, complex, time-varying tactile patterns" unlike the stable patterns of rigid contact, and that dense tactile is far more discriminative than sparse — but current optimization can't fully leverage it. [[2509.18830|DexSkin]] demonstrates the payoff of getting it right: high-coverage conformable skin enables a residual-RL policy to cut contact pressure on artificial berries by 90% (14.5→1.53 kPa) and improve real blueberry integrity from 20% to 60%. This is a single direction inside Grasping (not its own cluster); the physics substrate — differentiable soft-body simulation — is owned by [[Sim2Real|Sim2Real]] and cross-referenced.

**First-principles framing.**
- **First principle**: For a deformable object the contact state is a continuum the effector *produces*, not a discrete pose it *selects* — the object's shape under contact is a function of the applied force field, so grasping is closed-loop force regulation, not open-loop pose planning. There is no ground-truth grasp-pose to regress to.
- **Assumption being challenged**: That grasp synthesis = pose selection on a rigid geometry. [[2506.17198|Dex1B]] and [[2505.03233|SynGrasp-1B]] generate grasp *poses*; for deformables the pose is ill-defined, so the entire pose-selection paradigm — and the rigid-body SDF feasibility loss — does not apply. The field treats deformables as a hard special case of rigid grasping; it is a different problem.
- **The bet**: A contact-creation policy grounded in dense tactile + differentiable soft-body physics holds where rigid-grasp estimators fail, matching [[2509.18830|DexSkin]]'s 90% contact-pressure reduction and 20%→60% real-fruit integrity, and beating sparse-tactile baselines on [[2510.25725|HumanoidVTA]]'s soft-object discrimination — i.e., force-regulation succeeds where pose-selection has no defined target.

**Evidence.**
- [[2509.18830|DexSkin]] — High-coverage conformable capacitive skin (60 taxels, 294° coverage); residual RL cuts berry pressure 90% (14.5→1.53 kPa), blueberry integrity 20%→60%, 19/20 perturbed pen reorientation; the deformable-force-regulation anchor.
- [[2510.25725|HumanoidVTA]] — 2,124-sensor humanoid soft-object dataset; dense tactile separates pressure conditions where sparse fails; the dense-tactile-for-soft substrate.
- [[2604.07335|TAMEn]] — Closed-loop tactile + AR recovery for contact-rich bimanual; 75% SR; soft-object recovery data (feeds C3).
- [[2511.04665|Real-to-Sim GS]] (cross-ref Sim2Real) — 3DGS + soft-body twin; ρ > 0.9 sim-real; the differentiable-soft-body evaluation substrate.
- [[2511.02097|WM Manipulation Survey]] — Names structured/object-centric representations and physics-awareness as open; deformables stress both.

**Concrete research questions.**
1. **Q1 — Force-regulation policy vs pose-selection baseline on deformables.** Compare a closed-loop force-regulation policy ([[2509.18830|DexSkin]]-style residual RL) against a rigid-grasp estimator on towel/sponge/fruit — does force-regulation succeed where pose-selection has no target?
2. **Q2 — Dense vs sparse tactile for contact-creation.** Quantify the [[2510.25725|HumanoidVTA]] dense-vs-sparse discrimination gap on a *control* (not classification) task — does dense tactile translate to higher soft-object SR, or does current optimization bottleneck it?
3. **Q3 — Differentiable soft-body physics as the dynamics model.** Use a differentiable MPM/soft-body twin (cross-ref [[Sim2Real|Sim2Real]]) as the world model for deformable contact; does physics-grounded prediction beat model-free force-regulation?
4. **Q4 — Contact-pressure as the reward, not task-success.** [[2509.18830|DexSkin]] derives interpretable force from skin output; test contact-pressure-bounded reward as the objective for fragile-object grasping (couples to D4's safety bounding).

**Related research papers.**
- [[2509.18830|DexSkin]] — Conformable high-coverage skin + residual RL; 90% pressure reduction, 20%→60% berry integrity; the deformable-force anchor.
- [[2510.25725|HumanoidVTA]] — Dense humanoid tactile for soft objects; dense > sparse discrimination; substrate.
- [[2604.07335|TAMEn]] — Closed-loop tactile recovery data; 75% SR; soft-object recovery.
- [[2604.20444|VTouch++]] — 120K-episode synchronized vision+tactile+proprioception; contact-mode-axis data including soft contact.
- [[2511.04665|Real-to-Sim GS]] — 3DGS + soft-body twin; ρ > 0.9; differentiable-soft-body eval (cross-ref Sim2Real).
- [[2603.05687|CGP]] — Contact-grounded policy predicting coupled state+tactile; real-time; contact as predicted trajectory (feeds B1).
- [[2302.04659|ManiSkill2]] — Real-time rigid-MPM soft-body sim (80–84 FPS); the soft-body simulation throughput baseline.
- [[2605.13083|TouchAnything]] — Multi-view egocentric + dense tactile; soft-contact data, no deformable policy.

**Benchmarks & metrics.**
- [[2509.18830|DexSkin]] — 90% contact-pressure reduction (14.5→1.53 kPa), blueberry integrity 20%→60%, 19/20 perturbed; the deformable-grasping metric.
- [[2510.25725|HumanoidVTA]] — Dense vs sparse tactile t-SNE separation on soft objects; the discrimination-vs-control gap diagnostic.
- [[2302.04659|ManiSkill2]] — Soft-body environments at 80–84 FPS; low IL/RL SR on soft-body tasks reveals the algorithmic gap.

> [!warning] Risks
> - **No canonical success metric for deformable grasping** — "did it grasp" is ill-defined for cloth. → Adopt task-completion (fold, pack) + force-bound (integrity) jointly, per [[2509.18830|DexSkin]]'s integrity metric; don't report grasp-SR.
> - **Dense tactile optimization is unsolved** — [[2510.25725|HumanoidVTA]] shows dense tactile barely beats sparse in current policies. → Q2's dense-vs-sparse *control* test is the go/no-go; if the gap doesn't translate to control, the bet narrows to force-regulation without dense tactile.
> - **Soft-body sim is slow / inaccurate** — [[2302.04659|ManiSkill2]] runs soft-body at 80 FPS vs 2000 FPS rigid. → Bound differentiable-physics claims to tasks where the twin is validated (ρ > 0.9, [[2511.04665|Real-to-Sim GS]]); cross-ref Sim2Real for the physics.

---

## Cluster B — Contact-Rich Assembly & Precision

*Sub-millimeter contact behavior — insertion, assembly, precision tasks — where vision is blind to the contact state and open-loop policies fail. Reframing contact as a first-class predicted quantity.*

### B1 — Predictive-Tactile Contact Imagination

| | |
|---|---|
| **Cluster** | B — Contact-Rich Assembly & Precision |
| **Thesis** | Policies that *imagine the tactile future* before acting — which the field skips because tactile is consumed as a current observation, never predicted — has the irreducible truth that in contact the next-step force is a deterministic consequence of the action that the policy can forecast and exploit, which breaks the assumption that reactive tactile feedback is sufficient (force arrives only after contact), and — since the Peg-in-Hole absolute is already saturated at [[2512.23864\|DreamTacVLA]]'s 95.0% — I bet the gain lives in the *prediction delta*: an action-conditioned tactile world model adds [[2512.23864\|DreamTacVLA]]'s +22.3% over its matched no-Dream ablation, the margin a reactive-tactile policy structurally cannot recover, and holds [[2603.19201\|OmniVTA]]'s 60–63% SR under perturbation where reactive control degrades. |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2511.02097\|WM Manipulation Survey]], [[2510.25725\|HumanoidVTA]] |
| **Key targets** | **Headline (prediction delta + OOD robustness, where the absolute is saturated):** [[2512.23864\|DreamTacVLA]] +22.3% over its no-Dream ablation; [[2603.19201\|OmniVTA]] 60–63% SR *under perturbation* at 60 Hz reflexive correction. **Saturated in-distribution reference:** [[2512.23864\|DreamTacVLA]] 95.0% Peg-in-Hole / 85.7% USB / 81.1% Gear. **Consumed-force floor:** [[2505.22159\|ForceVLA]] 23.2 pp over π0-with-force |

**Why it matters.** Three surveys diagnose the same gap under different vocabulary: [[2604.04974|Video-to-Control Survey]] names "tactile/force integration" as an unresolved interface property, [[2511.02097|WM Manipulation Survey]] ranks Physics-Awareness 3rd of 13 capabilities, and [[2510.25725|HumanoidVTA]] shows dense tactile is discriminative but under-leveraged. The field consumes force as a *current* observation — [[2505.22159|ForceVLA]] (force-aware MoE, +23.2 pp), [[2601.20321|TaF-VLA]] (tactile-force alignment, 64.8%), [[2509.07962|TA-VLA]] (torque tokens) — but reactive feedback arrives only *after* contact, too late to prevent a bad insertion. The inversion now has two existence proofs: [[2512.23864|DreamTacVLA]]'s "Think–Dream–Act" loop (a tactile world model predicts future tactile states, the policy refines the draft action) hits 95.0% Peg-in-Hole and +22.3% over ablations, and [[2603.19201|OmniVTA]]'s Visuo-Tactile World Model + 60 Hz reflexive controller anticipates contact dynamics. The first-principles claim: the next-step force is a *predictable* function of the action, so a policy that imagines it acts anticipatorily, not reactively.

**First-principles framing.**
- **First principle**: In a contact-rich task the next-step tactile signal is a deterministic consequence of the chosen action given the contact state — it is forecastable. A policy that only reads current force is reactive by construction (force arrives after contact); a policy that *predicts* force can choose actions whose imagined contact outcome is good before committing.
- **Assumption being challenged**: That reactive tactile feedback suffices for contact-rich manipulation. [[2505.22159|ForceVLA]], [[2601.20321|TaF-VLA]], [[2509.07962|TA-VLA]] all consume force as input; the boundary they hit is latency — by the time bad force is felt, the misalignment has happened. [[2512.23864|DreamTacVLA]]'s +22.3% Dream-ablation shows prediction adds what reaction cannot.
- **The bet**: An action-conditioned tactile world model that anticipates contact outcomes beats reactive-tactile policies on the axis where in-distribution SR is saturated — the headline is the *prediction delta* ([[2512.23864|DreamTacVLA]]'s +22.3% over its matched no-Dream ablation, concentrated at contact onset) and robustness under perturbation ([[2603.19201|OmniVTA]]-class 60 Hz reflexive correction, 60–63% SR under perturbation where reactive control degrades) — not the saturated 95.0% Peg-in-Hole absolute, which sits at [[2505.22159|ForceVLA]]-class consumed-force SR only as the floor.

**Evidence.**
- [[2512.23864|DreamTacVLA]] — Think–Dream–Act: tactile world model predicts future tactile, policy refines draft action; 95.0% Peg-in-Hole, 85.7% USB, 81.1% Gear, +22.3% over ablations; the contact-imagination anchor.
- [[2603.19201|OmniVTA]] — Visuo-Tactile World Model + 60 Hz Reflexive Latent Tactile Controller; 21K-trajectory OmniViTac dataset; 60–63% under perturbation; predictive + reflexive contact control.
- [[2603.05687|CGP]] — Predicts coupled robot-state + tactile trajectories, maps to controller targets; real-time; contact as a jointly-predicted quantity.
- [[2505.22159|ForceVLA]] — Force-aware MoE, force as first-class modality; 60.5% (+23.2 pp over π0-with-force), 90% under occlusion; the consumed-force ceiling to beat.
- [[2601.20321|TaF-VLA]] — Tactile-force alignment (VQ-VAE, 10M pairs); 64.8% (vs 37.1% vision-only), 60.3% cross-sensor; force grounded but consumed, not predicted.

**Concrete research questions.**
1. **Q1 — Tactile world model vs reactive-tactile ablation.** Isolate [[2512.23864|DreamTacVLA]]'s Dream component: does predicting the tactile future add the +22.3% over a matched reactive-tactile policy, and does the gain concentrate at the contact-onset moment?
2. **Q2 — Forecast horizon vs reflexive frequency trade.** [[2603.19201|OmniVTA]] runs 60 Hz reflexive; ablate prediction horizon (1-step vs N-step) against control frequency — what horizon maximizes anticipatory benefit before drift dominates?
3. **Q3 — Imagined tactile as proprioceptive forecast when sensors absent.** Train the tactile world model with sensors, deploy using *imagined* tactile as a forecast (couples to B3's sensor-free deployment) — does imagined contact recover sensor-on SR?
4. **Q4 — Shared tactile latent across sensors for the world model.** Use [[2601.20321|TaF-VLA]]'s force-aligned latent or [[2506.14754|Sparsh-X]]'s multisensory representation as the prediction target so the world model is sensor-agnostic.

**Related research papers.**
- [[2512.23864|DreamTacVLA]] — Think–Dream–Act tactile world model; 95.0% Peg-in-Hole, +22.3%; the anchor.
- [[2603.19201|OmniVTA]] — Visuo-tactile world model + 60 Hz reflexive controller; predictive + reflexive.
- [[2603.05687|CGP]] — Coupled state+tactile trajectory prediction → controller targets; real-time contact grounding.
- [[2505.22159|ForceVLA]] — Force-aware MoE; +23.2 pp; consumed-force ceiling.
- [[2601.20321|TaF-VLA]] — Tactile-force alignment, cross-sensor; consumed, not predicted.
- [[2506.14754|Sparsh-X]] — Multisensory (image/audio/motion/pressure) tactile backbone, 1M contacts; 90% plug-insertion; the sensor-agnostic prediction target.
- [[2503.02881|RDP]] — Reactive Diffusion Policy (slow-fast visuo-tactile); reactive, no prediction.
- [[2503.08548|TLA]] — Tactile-Language-Action model; tactile-conditioned, no world model.
- [[2509.19696|Diffusion Impedance Learning]] — Diffusion-based impedance for contact-rich; impedance, not tactile prediction.
- [[2503.16806|DyWA]] — Dynamics-adaptive world action model jointly predicting future object state; 82.2%/75.0% seen/unseen; state-prediction analog (non-prehensile).

**Benchmarks & metrics.**
- [[2512.23864|DreamTacVLA]] — 95.0% Peg-in-Hole / 85.7% USB / 81.1% Gear / 74.6% Tool-Stab; +22.3% over ablations; the contact-imagination benchmark.
- [[2603.19201|OmniVTA]] — 6 real contact-rich tasks; RLTC 60% (Wipe) / 63% (Peel) under perturbation, tangential deformation 0.35 avg; predictive-reflexive metric.
- [[2502.05086|REASSEMBLE]] — NIST board multimodal assembly; insert is hardest, DMP 70% insertion; force-torque phase patterns — the contact-dynamics ground truth.

> [!warning] Risks
> - **Tactile prediction may plateau at the noise floor** — micro-slip not in the action-conditioned model. → Bound the bet to vision/action-correlated contact; report where imagined tactile diverges from measured.
> - **World-model latency vs reflexive budget** — predicting tactile must fit the [[2603.19201|OmniVTA]] 60 Hz loop. → Q2's horizon-vs-frequency ablation is the feasibility gate; a slow world model defeats the anticipatory gain.
> - **Sim tactile is non-standard** — training a tactile world model needs tactile data at scale. → Use [[2603.19201|OmniVTA]]'s 21K-trajectory OmniViTac + [[2602.23253|SPARR]]-style real residual; cross-ref [[Sim2Real|Sim2Real]] for tactile sim-to-real.

### B2 — Contact-Mode-Conditional Precision & Reversibility

| | |
|---|---|
| **Cluster** | B — Contact-Rich Assembly & Precision |
| **Thesis** | Precision assembly via a *discrete contact-mode* latent with mode-conditional dynamics — which the field skips by scaling smooth continuous policies — has the irreducible truth that contact physics is locally discontinuous (make/break, slip-stick, friction-cone) so the dynamics are piecewise, which breaks the assumption that more policy capacity closes the sub-millimeter gap, and — because in-distribution [AutoMate](https://arxiv.org/abs/2407.08028) is already saturated at [[2602.23253\|SPARR]]'s 95–100% — I bet a contact-mode-conditional policy wins where the smooth baseline cannot: on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer at [[2602.23253\|SPARR]]'s +74.5% relative SR / 36.5% cycle-time cut and below [[2602.23648\|FAVLA]]'s 7.7 N peak contact force, with mode-derived reversibility the continuous policy structurally lacks. |
| **Anchor surveys** | [[2511.02097\|WM Manipulation Survey]], [[2604.04974\|Video-to-Control Survey]], [[2502.05086\|REASSEMBLE]] |
| **Key targets** | **Headline (OOD / unseen-task, where in-distribution is saturated):** [[2602.23253\|SPARR]] +74.5% relative SR / 36.5% cycle-time cut on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic); [[2407.16677\|ResiP]] perturbation drop only 12% (vs 19–26% baselines). **Saturated in-distribution reference:** [[2602.23253\|SPARR]] 95–100% [AutoMate](https://arxiv.org/abs/2407.08028). **Force bound:** [[2602.23648\|FAVLA]] 80.8% at peak-force 7.7 N (Gear) |

**Why it matters.** [[2502.05086|REASSEMBLE]] empirically establishes that "Insert is the hardest action, accounting for the highest number of failures due to its multi-step nature and demand for precise alignment and force application," and that force-torque "reveals distinct patterns corresponding to action phases (free-space, contact, pushing, twisting)" — i.e., the task *is* a sequence through discrete contact modes. Yet the dominant fixes scale continuous policies or add residuals: [[2602.23253|SPARR]] (sim base + real residual, 95–100% [AutoMate](https://arxiv.org/abs/2407.08028), +74.5% on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic)), [[2407.16677|ResiP]] (residual RL, peg-in-hole 5%→99%), [[2602.23648|FAVLA]] (force-adaptive fast-slow, 80.8%). All improve, none model the contact *mode* as a first-class discrete latent. The non-consensus claim: contact physics is piecewise — Coulomb friction holds only in-contact, ballistic dynamics only in free-space — so a policy with mode-conditional dynamics gets the structural granularity that a smooth approximator pays exponentially for at the friction-cone boundary. This also unlocks *reversibility*: knowing you are in `making` vs `in-contact` tells you whether a corrective retreat is safe.

**First-principles framing.**
- **First principle**: Contact dynamics are locally discontinuous — friction-cone boundaries, normal-force singularities, and slip-stick are discrete state changes. The true dynamics are piecewise (mode-conditional), so a smooth continuous policy approximating a piecewise function is structurally mismatched and gets expensive exactly at the precision-critical boundary.
- **Assumption being challenged**: That more policy capacity / more residual correction closes the sub-millimeter gap. [[2602.23253|SPARR]] and [[2407.16677|ResiP]] add residuals; [[2602.23648|FAVLA]] adds force-adaptive frequency — all trade expressivity for accuracy but never address the *structural* discontinuity. [[2502.05086|REASSEMBLE]]'s phase-distinct force patterns show the modes are real and observable; the field smooths over them.
- **The bet**: A contact-mode-conditional policy ($c_t \in \{\text{free, making, in-contact, sliding, breaking}\}$ with mode-conditional dynamics) beats monolithic continuous policies *where in-distribution SR is saturated* — the contribution lives on the OOD axis, not the in-distribution [AutoMate](https://arxiv.org/abs/2407.08028) number ([[2602.23253|SPARR]] already 95–100% there). The headline target is unseen-task transfer: [[2602.23253|SPARR]]'s +74.5% relative SR / 36.5% cycle-time cut on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic), at lower peak contact force than [[2602.23648|FAVLA]]'s 7.7 N — precision *and* reversibility from the mode structure, on the tasks the smooth policy has not seen.

**Evidence.**
- [[2602.23253|SPARR]] — Sim base policy + vision-conditioned real residual; 95–100% [AutoMate](https://arxiv.org/abs/2407.08028), +74.5% relative / 36.5% cycle-time on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic), no human supervision; the assembly-SR ceiling.
- [[2407.16677|ResiP]] — Frozen BC + residual PPO for closed-loop correction; peg-in-hole 5%→99%, 12% perturbation drop (vs 19–26%); residual reactivity, continuous.
- [[2602.23648|FAVLA]] — Force-adaptive fast-slow VLA, force-variance head gates AE frequency; 80.8%, peak force 7.7 N (Gear) / 9.9 N (Box); adaptive frequency ≈ implicit mode-awareness, not explicit modes.
- [[2502.05086|REASSEMBLE]] — NIST board; insert hardest, force-torque phase-distinct patterns; the contact-mode ground truth.
- [[2603.05687|CGP]] — Coupled state+tactile prediction → controller targets; predicts contact evolution, continuous.

**Concrete research questions.**
1. **Q1 — Discrete contact-mode latent.** Add a categorical $c_t \in \{\text{free, making, in-contact, sliding, breaking}\}$ predicted from force-torque ([[2502.05086|REASSEMBLE]]-supervised); condition continuous dynamics on $c_t$; does explicit mode beat [[2602.23648|FAVLA]]'s implicit frequency-adaptation?
2. **Q2 — Mode-conditional physics losses.** Apply Coulomb friction only in `in-contact`, ballistic only in `free` — does mode-gated physics improve sub-millimeter insertion over a single dynamics head?
3. **Q3 — Reversibility from mode.** Use the contact-mode to decide whether a corrective retreat is safe (`making` reversible, `in-contact` may be wedged); does mode-aware reversibility cut failures on [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer?
4. **Q4 — Mode-conditional residual.** Combine with [[2602.23253|SPARR]]/[[2407.16677|ResiP]]: a mode-specific residual policy per contact mode — does per-mode residual beat a single residual?

**Related research papers.**
- [[2602.23253|SPARR]] — Sim base + real residual assembly; 95–100% [AutoMate](https://arxiv.org/abs/2407.08028), +74.5% NIST; the ceiling.
- [[2407.16677|ResiP]] — Residual RL for precise assembly; peg-in-hole 5%→99%; continuous residual.
- [[2602.23648|FAVLA]] — Force-adaptive fast-slow VLA; 80.8%, peak-force reduction; implicit mode-awareness.
- [[2603.15169|ForceVLA2]] — Hybrid force-position control with force awareness; 66% avg; position/force switching, no discrete mode latent.
- [[2502.05086|REASSEMBLE]] — NIST multimodal assembly dataset; phase-distinct force patterns; mode ground truth.
- [[2509.19696|Diffusion Impedance Learning]] — Diffusion-based impedance for contact-rich; impedance regulation, continuous.
- [[2605.05172|Q2RL]] — Extract Q from BC for on-robot RL; 3.75× on peg insertion / pipe assembly in 1–2 hrs; the on-robot fine-tuning loop for mode-policies.
- [[2503.16806|DyWA]] — Dynamics-adaptive world action model (FiLM on inferred physics); 82.2%/75.0%; mode-adjacent dynamics adaptation.
- [[2602.15549|VLM-DEWM]] — External world model + verification for assembly planning; 94.0% assembly TSR; high-level state-verification layer.

**Benchmarks & metrics.**
- [AutoMate](https://arxiv.org/abs/2407.08028) (8–10 tasks) — Insertion/assembly SR; [[2602.23253|SPARR]] 95–100%, the contact-mode ceiling.
- [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) industrial assembly — Cross-task transfer; [[2602.23253|SPARR]] +74.5% relative SR / 36.5% cycle-time on unseen tasks.
- [[2502.05086|REASSEMBLE]] — NIST board, 4,551 demos, F1@50 44.1% TAS; insertion 70% DMP; the contact-phase + anomaly benchmark.

> [!warning] Risks
> - **Discrete-latent optimization variance** — Gumbel-softmax / REINFORCE for $c_t$. → Anneal soft→hard temperature; start continuous, harden over training.
> - **Mode supervision needs a sim/force ground truth** — real mode labels scarce. → Distill modes from [[2502.05086|REASSEMBLE]]'s phase annotations + sim contact ground truth; report mode-classification accuracy first.
> - **Saturated headline** — [[2602.23253|SPARR]] already 95–100% [AutoMate](https://arxiv.org/abs/2407.08028). → Contribution must show on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer + peak-force + reversibility, not in-distribution [AutoMate](https://arxiv.org/abs/2407.08028) SR.

### B3 — Sensor-Free Tactile-Aware Deployment via Distillation

| | |
|---|---|
| **Cluster** | B — Contact-Rich Assembly & Precision |
| **Thesis** | Tactile-aware policies deployed *without* tactile sensors at inference — which the field skips because tactile awareness is assumed to require tactile hardware at runtime — has the irreducible truth that tactile awareness is a *learned behavior* separable from the sensor that taught it, which breaks the assumption that sensor-free = contact-blind, and — because the easy-object average is already saturated — I bet the contribution shows on the *hardest objects and the largest behavior gains*: a teacher-student distillation matches [[2603.15257\|HapticVLA]]'s +45 pp delta on the fragile egg (vs SmolVLA) and [[2603.04531\|PTLD]]'s +182% rotation / +57% reorientation goals over proprioception-only, eliminating per-platform tactile hardware where it actually changes the outcome. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2511.02097\|WM Manipulation Survey]], [[2604.04974\|Video-to-Control Survey]] |
| **Key targets** | **Headline (novel/fragile-object + behavior deltas, where the average is saturated):** [[2603.15257\|HapticVLA]] +45 pp on the fragile egg vs SmolVLA; [[2603.04531\|PTLD]] +182% rotation / +57% reorientation goals via privileged-to-real distillation; [[2601.02778\|Force-Based Sim2Real]] 25.1 vs 1.1 in-hand rotations (contact vs no-contact). **Saturated easy-object reference:** [[2603.15257\|HapticVLA]] 86.7% sensor-free mean |

**Why it matters.** [[2504.03515|Dexterous IL Survey]] names hardware cost and reproducibility as deployment blockers, and integrating tactile sensors "leads to increased hardware cost, reduced reproducibility, and compatibility issues across platforms" ([[2603.15257|HapticVLA]]). The field assumes tactile *awareness* requires tactile *hardware* at runtime. But three results show the awareness and the sensor are separable: [[2603.15257|HapticVLA]] distills a tactile-aware teacher into a sensor-free student that predicts a tactile token from vision (86.7%, +45 pp on egg vs SmolVLA), [[2603.04531|PTLD]] distills privileged-sensor oracle policies into a deployable tactile state estimator (+182% rotation, +57% reorientation goals) — notably *without ever simulating tactile sensors*, and [[2603.15169|ForceVLA2]]/[[2603.15257|HapticVLA]] both deploy without inference-time tactile. The first-principles claim: tactile competence is a behavior the policy internalizes during training; the sensor is the teacher, not a runtime dependency — so the student can be sensor-free. This is the deployment twin of B1/B2's training-time contact modeling.

**First-principles framing.**
- **First principle**: Tactile awareness is a learned behavior — a mapping from (vision, state, action) to contact-appropriate force-modulation — that is *separable* from the sensor that supervised it. The sensor provides training signal; at deployment the behavior can be driven by a learned tactile-token prediction. Sensor-free does not imply contact-blind.
- **Assumption being challenged**: That tactile awareness requires tactile hardware at inference. [[2603.15257|HapticVLA]] (sensor-free student) and [[2603.04531|PTLD]] (privileged-to-real distillation, no tactile sim) both refute it; the per-platform-tactile-hardware assumption is a training/deployment conflation.
- **The bet**: A teacher-student distillation transfers tactile competence into a sensor-free student where it matters most — the headline is the novel/fragile-object delta and the behavior-gain delta, not the saturated easy-object average ([[2603.15257|HapticVLA]] already 86.7% mean). The targets: [[2603.15257|HapticVLA]]'s +45 pp on the fragile egg vs SmolVLA and [[2603.04531|PTLD]]'s +182% rotation / +57% reorientation goals over proprioception-only, eliminating per-platform tactile hardware — full tactile behavior at zero runtime tactile cost, demonstrated on the objects where contact-blindness actually fails.

**Evidence.**
- [[2603.15257|HapticVLA]] — Safety-Aware Reward-Weighted Flow Matching teacher + Tactile Distillation into sensor-free student (predicts tactile token from vision); 86.7%, +45 pp egg vs SmolVLA; the sensor-free anchor.
- [[2603.04531|PTLD]] — Privileged-sensor oracle in sim → deployable tactile state estimator from real paired data, *no tactile simulation*; +182% rotation, +57% reorientation goals; the privileged-to-real distillation anchor.
- [[2601.02778|Force-Based Sim2Real]] — Distance-field tactile sim + current-to-torque calibration; 25.1 vs 1.1 in-hand rotations (contact vs no-contact); efficient tactile-sim teacher.
- [[2603.15169|ForceVLA2]] — Hybrid force-position; 66% avg; deploys without inference-time tactile sensing.
- [[2509.07962|TA-VLA]] — Sensorless torque from motor current; charger 0/20→17/20; "sensorless" deployment via current-derived torque.

**Concrete research questions.**
1. **Q1 — Tactile-token prediction vs imagined-tactile-from-world-model.** Compare [[2603.15257|HapticVLA]]'s direct tactile-token prediction against B1's tactile-world-model forecast as the sensor-free signal — which transfers more teacher competence?
2. **Q2 — Privileged-to-real without tactile sim.** Replicate [[2603.04531|PTLD]]'s no-tactile-sim distillation on assembly (vs in-hand): does the privileged-oracle → real-estimator route avoid the tactile sim-to-real gap on [AutoMate](https://arxiv.org/abs/2407.08028)?
3. **Q3 — Sensorless torque as a cheap tactile proxy.** [[2509.07962|TA-VLA]]'s current-derived torque needs no sensor at all; how much of [[2603.15257|HapticVLA]]'s 86.7% is recoverable from motor-current torque alone?
4. **Q4 — Safety-aware distillation reward.** [[2603.15257|HapticVLA]]'s SA-RWFM penalizes excess force; does distilling the *safety* behavior (not just task) preserve fragile-object integrity (couples to D4)?

**Related research papers.**
- [[2603.15257|HapticVLA]] — Tactile distillation to sensor-free student; 86.7%, +45 pp egg; the anchor.
- [[2603.04531|PTLD]] — Privileged tactile latent distillation, no tactile sim; +182% rotation; the privileged-to-real anchor.
- [[2601.02778|Force-Based Sim2Real]] — Efficient distance-field tactile sim + calibration; 25.1 vs 1.1 rotations; tactile-sim teacher.
- [[2603.15169|ForceVLA2]] — Hybrid force-position, deploys sensor-free; 66% avg.
- [[2509.07962|TA-VLA]] — Sensorless current-derived torque; charger 0→17/20; no-sensor proxy.
- [[2506.14754|Sparsh-X]] — Multisensory tactile backbone; the teacher representation to distill from.
- [[2605.05172|Q2RL]] — BC-to-RL on-robot; 3.75× peg insertion; the on-robot refinement after distillation.
- [[2510.25725|HumanoidVTA]] — Dense tactile teacher data; the high-resolution signal to distill into a sparse/sensor-free student.

**Benchmarks & metrics.**
- [[2603.15257|HapticVLA]] — 86.7% on jar/waffle/egg, +45 pp egg vs SmolVLA, 75% with sensor (SA-RWFM); the sensor-free metric.
- [[2603.04531|PTLD]] — +182% in-hand rotation, +57% reorientation goals, robust to slip/mass/wrist; privileged-to-real metric.
- [[2601.02778|Force-Based Sim2Real]] — 25.1 vs 1.1 rotations (contact vs no-contact), 10–100% force tracking; the tactile-value metric.

> [!warning] Risks
> - **Distillation gap on novel objects** — sensor-free student may fail where the teacher's tactile was load-bearing. → Bound to in-distribution contact; report the teacher-student gap per object class, not an average.
> - **Sensorless torque is coarse** — [[2509.07962|TA-VLA]]'s current-derived torque misses fine slip. → Q3's torque-only ablation sets the floor; if too coarse, the bet narrows to predicted-tactile-token, not sensorless.
> - **Safety behavior may not distill** — task-success distills but force-safety might not. → Q4's safety-distillation test is the gate; couple to D4's explicit force-bounding if safety doesn't transfer.

---

## Cluster C — Bimanual & Dual-Arm Coordination

*Two-arm manipulation where the cross-arm coupling is non-factorizable and bimanual demonstration data is scarce — coordination-native policies, scalable data generation, and the tactile channel that makes force-balanced cooperation observable.*

### C1 — Coordination-Native Bimanual Policies

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Bimanual policies built on *composed single-arm priors with explicit cross-arm coupling* — which the field skips by training monolithic bimanual models from scarce two-arm data — has the irreducible truth that two-arm value is non-additive (the coupling term carries the coordination) yet each arm's *skill* is a transferable single-arm prior, which breaks the assumption that bimanual competence requires bimanual-scale pretraining, and I bet a coordination-native composition matches monolithic bimanual SR on ~50 episodes — [[2511.05275\|TwinVLA]] 76% (vs RDT-1B 45%, ≈π0 80%) at ~25 GPU-days. |
| **Anchor surveys** | [[2604.05831\|BiCoord]], [[2407.07788\|BiGym]], [[2603.15469\|RoCo Challenge]] |
| **Key targets** | [[2511.05275\|TwinVLA]] 76% on ~50 episodes / ~25 H100-days (vs RDT-1B 45%, π0 80%); [[2604.05831\|BiCoord]] 4× spatial-temporal-integral coordination + later-stage degradation; [[2507.23523\|H-RDT]] 41.6% few-shot (vs RDT 16.0%) + 87.2% RoboTwin 2.0 |

**Why it matters.** [[2604.05831|BiCoord]] quantifies the coordination problem — its tasks carry a 4× spatial-temporal-integral increase and "policy performance consistently degraded in later stages of long-horizon tasks" — and [[2407.07788|BiGym]] shows IL/RL hit near-0% on stacking and long bimanual sequences. The dominant response trains monolithic bimanual models needing thousands of hours of proprietary two-arm data. [[2511.05275|TwinVLA]] inverts this: it composes *two pre-trained single-arm VLAs* with a Joint-Attention coupling mechanism, matching monolithic systems on ~50 bimanual episodes and ~25 H100-days (76% vs RDT-1B 45%, ≈π0 80% which uses vastly more). [[2507.23523|H-RDT]] similarly transfers single-hand human-video priors into bimanual policies (41.6% few-shot vs RDT 16.0%). The first-principles claim: the *skill* of each arm is a single-arm prior (abundant), and only the *coupling* — handover timing, force balance — is bimanual-specific (scarce), so the right architecture composes abundant priors + learns only the cheap coupling term.

**First-principles framing.**
- **First principle**: The bimanual value function is non-additive — $V(a_L, a_R) \neq V(a_L) + V(a_R)$ — because the cross-arm coupling (handover, force balance, mutual constraint) is the load-bearing term. But each arm's *skill* is a marginal single-arm policy. So the joint factors as (transferable single-arm skill) × (bimanual coupling), and only the latter needs two-arm data.
- **Assumption being challenged**: That bimanual competence requires bimanual-scale pretraining. Monolithic bimanual VLAs assume the whole joint must be learned from two-arm data; [[2511.05275|TwinVLA]] (composed single-arm + Joint Attention) and [[2507.23523|H-RDT]] (single-hand human-video transfer) show the skill is reusable and only the coupling is bimanual-specific — the bimanual-data wall is partly self-imposed by monolithic design.
- **The bet**: A coordination-native composition matches monolithic bimanual SR on ~50 episodes — [[2511.05275|TwinVLA]] 76% (vs RDT-1B 45%, ≈π0 80%) at ~25 H100-days — and holds [[2604.05831|BiCoord]]'s later-stage coordination where monolithic policies degrade, i.e., bimanual competence at single-arm data cost.

**Evidence.**
- [[2511.05275|TwinVLA]] — Composes two pre-trained single-arm VLAs via Joint Attention (causal-masked cross-arm self-attention); 76% on ~50 episodes / ~25 H100-days, vs RDT-1B 45%, ≈π0 80%; the composition anchor.
- [[2507.23523|H-RDT]] — Single-hand human-video (EgoDex 338K) → bimanual DiT via flow matching; 41.6% few-shot (vs RDT 16.0%), 87.2% RoboTwin 2.0, 52% towel-fold; human-prior-to-bimanual transfer.
- [[2604.05831|BiCoord]] — Long-horizon bimanual benchmark; 4× spatial-temporal integral, MRD/ARD/SMT/SMP/STI metrics, later-stage degradation; the coordination-quantification anchor.
- [[2603.15469|RoCo Challenge]] — Collaborative assembly; end-to-end VLA beats modular for recovery; coordination + Sim-to-Real Cliff.
- [[2410.24185|DexMimicGen]] — Subtask taxonomy (async per-arm + sync coordination + ordering constraints); 90% real humanoid; the coordination-structure substrate (feeds C2).

**Concrete research questions.**
1. **Q1 — Joint-Attention coupling vs monolithic.** Ablate [[2511.05275|TwinVLA]]'s cross-arm Joint Attention against a monolithic bimanual policy at matched data — does the composed prior + explicit coupling beat monolithic on [[2604.05831|BiCoord]]'s coordination metrics (SMT/SMP)?
2. **Q2 — Coupling-term data efficiency.** How few bimanual episodes does the coupling term need given strong single-arm priors — replicate [[2511.05275|TwinVLA]]'s ~50-episode result on [[2604.05831|BiCoord]]'s 4×-harder tasks?
3. **Q3 — Coordination-type-conditional coupling.** [[2410.24185|DexMimicGen]] distinguishes async/sync/ordered subtasks; condition the coupling mechanism on coordination type — does typed coupling beat a single Joint-Attention layer?
4. **Q4 — Later-stage degradation diagnosis.** [[2604.05831|BiCoord]] shows degradation in later stages; is it a coupling failure or a single-arm-skill failure — does the composition isolate which arm/coupling breaks?

**Related research papers.**
- [[2511.05275|TwinVLA]] — Twin single-arm VLA composition + Joint Attention; 76% on ~50 episodes; the anchor.
- [[2507.23523|H-RDT]] — Human-video-to-bimanual transfer; 41.6% few-shot; single-prior transfer.
- [[2604.05831|BiCoord]] — Long-horizon bimanual benchmark; 4× coordination, later-stage degradation; the metric.
- [[2603.15469|RoCo Challenge]] — Collaborative assembly, VLA > modular for recovery; coordination + Sim-to-Real.
- [[2410.24185|DexMimicGen]] — Bimanual subtask taxonomy (async/sync/ordered); 90% real; coordination structure.
- [[2511.21264|MPPI-Bimanual]] — Sampling-based MPC for bimanual coordination; model-based coordination baseline.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual/mobile trajectories, MIND-2 dual-system + IQL; up to 1.0 multi-robot collaborative SR; data + framework.
- [[2407.07788|BiGym]] — 40 mobile bimanual tasks; near-0% on long-horizon; the difficulty-establishing benchmark.

**Benchmarks & metrics.**
- [[2604.05831|BiCoord]] — 4× spatial-temporal integral, MRD/ARD/SMT/SMP/STI; later-stage degradation; the coordination-quality benchmark.
- [[2511.05275|TwinVLA]] — 76% on Anubis (vs RDT-1B 45%, π0 80%), 75.8% vs 61.6% Tabletop-Sim Easy, ~50 episodes / ~25 GPU-days; the data-efficiency metric.
- [[2407.07788|BiGym]] — 40 mobile bimanual tasks; ACT/DP up to 100% simple, 0% on stack-blocks/long sequences; the long-horizon coordination floor.

> [!warning] Risks
> - **Composition may cap coordination ceiling** — tightly-coupled tasks (handover with force balance) may exceed what composed single-arm priors reach. → Bound the bet to loosely-to-moderately-coupled tasks; report the [[2604.05831|BiCoord]] coupling-tightness vs SR curve.
> - **Joint Attention is one coupling design** — [[2511.05275|TwinVLA]]'s causal-masked attention may not be optimal. → Q3's typed-coupling ablation tests alternatives before claiming composition is general.
> - **Single-arm priors must be strong** — composition fails if base VLAs are weak. → Validate base single-arm SR first; the bet assumes π0/RDT-class single-arm priors exist.

### C2 — Scalable Bimanual Data Generation with Coordination Structure

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Bimanual data generation that *replays human demos through a coordination-structured simulator* — which the field skips by collecting two-arm teleoperation directly — has the irreducible truth that coordination structure (per-arm subtask decomposition + ordering constraints) is what makes a few demos generalize to many configurations, which breaks the assumption that bimanual data must be teleoperated at scale, and I bet structure-aware generation lifts real bimanual SR by [[2506.18088\|RoboTwin 2.0]]'s 24.4% (few-shot) / 21.0% (zero-shot) and [[2410.24185\|DexMimicGen]]'s 90% from 40 sim demos (vs 0% from 4 source). |
| **Anchor surveys** | [[2506.18088\|RoboTwin 2.0]], [[2604.05831\|BiCoord]], [[2603.15469\|RoCo Challenge]] |
| **Key targets** | [[2410.24185\|DexMimicGen]] 90% real (40 sim demos vs 0% from 4 source), 76.0% vs 0.7% Drawer-Cleanup; [[2506.18088\|RoboTwin 2.0]] +24.4% few-shot / +21.0% zero-shot real, 71.3% auto-code SR; [[2504.13059\|RoboTwin]] same SR with 300 sim + 20 real as 300 real |

**Why it matters.** [[2506.18088|RoboTwin 2.0]] names the dual-arm data wall — "prohibitive cost of real bimanual data" plus "existing synthetic datasets lack automated quality control" and "superficial domain randomization." Direct teleoperation of two coordinated arms is the bottleneck [[2407.07788|BiGym]] and [[2604.05831|BiCoord]] both run into. Two structure-aware generators show the way out: [[2410.24185|DexMimicGen]] replays a *few* human demos in sim using a subtask taxonomy (async per-arm, sync coordination, ordering constraints) to generate large datasets — 90% real humanoid SR from 40 generated demos vs 0% from the 4 source demos — and [[2506.18088|RoboTwin 2.0]] adds MLLM expert-code generation + 5-axis domain randomization + embodiment-aware grasp adaptation for +24.4% few-shot / +21.0% zero-shot real. The first-principles claim: the *coordination structure* (which subtasks are independent, which must synchronize, what order) is the generalization-carrying prior — encode it and a handful of demos covers the configuration space; ignore it and you must teleoperate every variation.

**First-principles framing.**
- **First principle**: Bimanual generalization comes from coordination structure, not data volume — a task decomposed into per-arm subtasks with explicit sync/ordering constraints can be SE(3)-replayed across object configurations, so a few demos span many scenes. The structure is the prior that turns $N$ demos into $N \times K$ feasible trajectories.
- **Assumption being challenged**: That bimanual data must be teleoperated at scale. The field collects two-arm demos directly because it lacks a coordination-aware replay; [[2410.24185|DexMimicGen]] (90% from 40 generated vs 0% from 4 source) and [[2506.18088|RoboTwin 2.0]] (MLLM-generated + randomized) show structure-aware generation replaces most teleoperation — the data wall is a missing-structure problem.
- **The bet**: Structure-aware generation lifts real bimanual SR by [[2506.18088|RoboTwin 2.0]]'s 24.4% (few-shot) / 21.0% (zero-shot) and reaches [[2410.24185|DexMimicGen]]'s 90% from 40 sim demos (vs 0% from 4 source), matching the data efficiency of [[2504.13059|RoboTwin]]'s "300 sim + 20 real = 300 real" — bimanual policies from a handful of demos.

**Evidence.**
- [[2410.24185|DexMimicGen]] — Subtask taxonomy (async/sync/ordered) replays few human demos in sim; 90% real humanoid from 40 demos (vs 0% from 4), 76.0% vs 0.7% Drawer-Cleanup; the coordination-structured generation anchor.
- [[2506.18088|RoboTwin 2.0]] — MLLM expert-code + sim-in-the-loop + 5-axis domain randomization + embodiment-aware grasp; +24.4% few-shot / +21.0% zero-shot real, 71.3% auto-code; the quality-controlled generator.
- [[2504.13059|RoboTwin]] — Generative digital twin + LLM task decomposition; 300 sim + 20 real ≈ 300 real, +40% dual-arm SR; the data-efficiency anchor.
- [[2604.07335|TAMEn]] — Feasibility-aware acquisition + closed-loop recovery data; 100% replay (vs 12–39%); the executability-filter for generated data.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual trajectories + 20K-traj digital twin in Isaac Sim; the cross-embodiment generation scale.

**Concrete research questions.**
1. **Q1 — Coordination-structure ablation on generation.** Strip [[2410.24185|DexMimicGen]]'s sync/ordering constraints — how much of the 90%-from-40-demos depends on coordination structure vs raw SE(3) replay?
2. **Q2 — MLLM code-gen vs replay for coordination.** Compare [[2506.18088|RoboTwin 2.0]]'s MLLM expert-code against [[2410.24185|DexMimicGen]]'s demo-replay for generating *coordinated* (not parallel) bimanual trajectories — which captures tight coupling better?
3. **Q3 — Feasibility filtering on generated bimanual data.** Apply [[2604.07335|TAMEn]]'s online feasibility validation to generated dual-arm trajectories — does filtering unexecutable coordinations raise downstream SR?
4. **Q4 — Generated-data coordination quality on [[2604.05831|BiCoord]].** Train [[2511.05275|TwinVLA]]/[[2507.23523|H-RDT]] on generated data; does it close [[2604.05831|BiCoord]]'s later-stage degradation, or does generation under-represent tight coupling?

**Related research papers.**
- [[2410.24185|DexMimicGen]] — Coordination-structured replay; 90% from 40 demos; the anchor.
- [[2506.18088|RoboTwin 2.0]] — MLLM-generated + randomized bimanual data; +24.4% few-shot; quality-controlled generator.
- [[2504.13059|RoboTwin]] — Generative digital twin + LLM decomposition; 300 sim + 20 real ≈ 300 real; data efficiency.
- [[2604.07335|TAMEn]] — Feasibility-aware + recovery data; 100% replay; executability filter.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual + digital twin; cross-embodiment scale.
- [[2507.00833|HumanoidGen]] — Auto data generation for humanoid manipulation; generation engine for bimanual humanoid.
- [[2603.15469|RoCo Challenge]] — 300+ demos collaborative assembly; failure-recovery curriculum data > param count.
- [[2604.20444|VTouch++]] — 120K-episode bimanual vision+tactile+proprioception; multimodal generation target (feeds C3).

**Benchmarks & metrics.**
- [[2410.24185|DexMimicGen]] — 90% real humanoid (40 demos vs 0% from 4), 76.0% vs 0.7% / 80.7% vs 3.3% generated-vs-source; the generation-efficacy metric.
- [[2506.18088|RoboTwin 2.0]] — +24.4% few-shot / +21.0% zero-shot real, +31.9% sim generalization, 71.3% auto-code; the domain-randomized-generation metric.
- [[2504.13059|RoboTwin]] — 300 sim + 20 real ≈ 300 real, +40% dual-arm SR; the data-efficiency metric.

> [!warning] Risks
> - **Generated data under-represents tight coupling** — replay may produce parallel-but-not-coordinated trajectories. → Q4's [[2604.05831|BiCoord]] coordination-quality test is the gate; couple generation to C1's coupling-aware training.
> - **Sim-to-Real Cliff** — [[2603.15469|RoCo Challenge]] shows generated/sim policies are brittle in real. → Use [[2506.18088|RoboTwin 2.0]]'s 5-axis randomization + [[2604.07335|TAMEn]] feasibility filtering; cross-ref [[Sim2Real|Sim2Real]].
> - **MLLM code-gen reliability** — [[2506.18088|RoboTwin 2.0]]'s 71.3% auto-code SR means ~29% needs refinement. → Keep human-in-the-loop verification ([[2604.05831|BiCoord]]'s annotation model); report generation-yield, not just downstream SR.

### C3 — Tactile-Coupled Bimanual Cooperation

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Bimanual policies with a *shared tactile channel* across both arms — which the field skips because tactile is integrated per-arm and bimanual benchmarks are vision-only — has the irreducible truth that force-balanced cooperation (holding-while-manipulating, bimanual handover) requires inter-arm force observability that vision cannot provide, which breaks the assumption that bimanual coordination is a vision-and-proprioception problem, and I bet tactile-coupled bimanual reaches [[2604.07335\|TAMEn]]'s 75% contact-rich SR where vision-only bimanual fails, using [[2604.20444\|VTouch++]]'s 120K synchronized vision+tactile+proprioception episodes. |
| **Anchor surveys** | [[2604.05831\|BiCoord]], [[2510.25725\|HumanoidVTA]], [[2504.03515\|Dexterous IL Survey]] |
| **Key targets** | [[2604.07335\|TAMEn]] 75% contact-rich bimanual + 100% replay (vs 12–39%); [[2604.20444\|VTouch++]] 120K episodes / 36M frames / 380 tasks synchronized vision+tactile+proprioception; [[2512.24653\|RoboMIND 2.0]] tactile improves VLA contact-task SR (XR-1 gains) |

**Why it matters.** Bimanual coordination benchmarks ([[2604.05831|BiCoord]], [[2407.07788|BiGym]]) are vision-and-proprioception only, yet the hardest bimanual tasks — one arm holds while the other manipulates, force-balanced handovers, bimanual assembly — depend on *inter-arm force* that vision cannot see. [[2510.25725|HumanoidVTA]] shows dense tactile is discriminative for contact, and the bimanual data bottleneck for tactile has just been removed: [[2604.20444|VTouch++]] provides 120K synchronized vision+tactile+proprioception episodes (36M frames, 380 bimanual tasks), [[2604.07335|TAMEn]] adds closed-loop tactile + recovery data for contact-rich bimanual (75% SR, 100% replay vs 12–39%), and [[2512.24653|RoboMIND 2.0]] confirms tactile lifts VLA contact-task SR (XR-1 gains on fine-grained tasks). The first-principles claim: force-balanced cooperation is fundamentally an *inter-arm force observability* problem — the two arms must sense each other's contribution through the object — so a shared tactile channel is not an add-on but the missing observation that makes cooperative force-control possible.

**First-principles framing.**
- **First principle**: Force-balanced bimanual cooperation requires inter-arm force observability — when one arm holds and the other manipulates, the coordination is governed by the force each transmits through the object, which is invisible to vision. The shared force state is the coordination variable; without sensing it, the policy coordinates blind.
- **Assumption being challenged**: That bimanual coordination is a vision-and-proprioception problem. [[2604.05831|BiCoord]] and [[2407.07788|BiGym]] are vision-only; their later-stage degradation on contact-coupled tasks is partly *force-blindness*. [[2604.07335|TAMEn]]'s 75% contact-rich bimanual SR with tactile shows the missing modality is force, not more vision.
- **The bet**: Tactile-coupled bimanual reaches [[2604.07335|TAMEn]]'s 75% contact-rich SR where vision-only bimanual fails, using [[2604.20444|VTouch++]]'s 120K synchronized episodes, with tactile lifting VLA contact-task SR per [[2512.24653|RoboMIND 2.0]] — cooperative force-control from a shared tactile channel.

**Evidence.**
- [[2604.07335|TAMEn]] — Tactile-aware engine for closed-loop contact-rich bimanual + AR recovery; 75% SR, 100% replay (vs 12–39%), object-tracking 100% (vs 32–78%); the contact-rich bimanual anchor.
- [[2604.20444|VTouch++]] — 120K-episode synchronized vision+tactile+proprioception (36M frames, 380 bimanual tasks); contrastive cross-modal alignment; the bimanual tactile data substrate.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual trajectories incl. tactile + MIND-2 dual-system; tactile improves VLA contact-task SR (XR-1 fine-grained gains); tactile-bimanual at scale.
- [[2510.25725|HumanoidVTA]] — 2,124-sensor humanoid tactile; dense tactile discriminative; the dense-tactile bimanual-relevant substrate.
- [[2604.05831|BiCoord]] — Vision-only bimanual benchmark; later-stage degradation on coupled tasks; the force-blindness diagnosis.

**Concrete research questions.**
1. **Q1 — Shared vs per-arm tactile channel.** Compare a *shared* inter-arm tactile representation against per-arm tactile fusion on holding-while-manipulating tasks — does shared force-state improve force-balanced cooperation?
2. **Q2 — Tactile on [[2604.05831|BiCoord]]'s degrading stages.** Add [[2604.20444|VTouch++]]/[[2604.07335|TAMEn]] tactile to a [[2604.05831|BiCoord]] policy — does tactile arrest the documented later-stage degradation on contact-coupled subtasks?
3. **Q3 — Force-balance as an explicit objective.** Make inter-arm force-balance a loss term (not just an observation); does explicit balance beat tactile-as-input on bimanual handover?
4. **Q4 — Tactile-coupled composition.** Add the shared tactile channel to C1's [[2511.05275|TwinVLA]] composition — does tactile coupling beat vision-only Joint Attention on contact-coupled bimanual?

**Related research papers.**
- [[2604.07335|TAMEn]] — Closed-loop tactile contact-rich bimanual + recovery; 75% SR; the anchor.
- [[2604.20444|VTouch++]] — 120K synchronized vision+tactile+proprioception bimanual; the data substrate.
- [[2512.24653|RoboMIND 2.0]] — 310K bimanual incl. tactile, MIND-2; tactile lifts contact-task SR.
- [[2510.25725|HumanoidVTA]] — Dense humanoid tactile; discriminative for contact.
- [[2604.05831|BiCoord]] — Vision-only bimanual; force-blindness diagnosis.
- [[2603.05687|CGP]] — Multi-point contact-grounded policy (coupled state+tactile); per-hand multi-contact, extensible to inter-arm.
- [[2602.19764|Multi-Sensory Sparse Experts]] — RGB+depth+6-axis-force fusion (DeMUSE); 83.2% MT50, 80 ms compliance; the multi-sensory fusion substrate for two-arm force.
- [[2605.13083|TouchAnything]] — Multi-view egocentric + dense tactile; bimanual tactile data.

**Benchmarks & metrics.**
- [[2604.07335|TAMEn]] — 75% contact-rich bimanual, 100% replay (vs 12–39%), 100% object-tracking (vs 32–78%); the contact-rich bimanual metric.
- [[2604.20444|VTouch++]] — 120K episodes / 36M frames / 380 tasks; cross-modal retrieval R@1 2.16% vs 0.29% baseline, real-robot MAE 0.022; the synchronized-tactile-data metric.
- [[2510.25725|HumanoidVTA]] — Dense vs sparse tactile separation; the inter-arm dense-tactile discriminability reference.

> [!warning] Risks
> - **Inter-arm tactile is hard to instrument** — both arms need synchronized tactile. → [[2604.20444|VTouch++]]/[[2604.07335|TAMEn]] data exist; bound the bet to platforms with bimanual tactile, report the instrumentation requirement.
> - **Dense tactile optimization unsolved** — [[2510.25725|HumanoidVTA]] shows dense tactile barely beats sparse in current policies. → Use [[2602.19764|Multi-Sensory Sparse Experts]]' AdaMN normalization to stop force being suppressed; report the dense-vs-sparse bimanual control gap.
> - **Force-balance reward can over-constrain** — penalizing imbalance may block legitimate asymmetric grasps. → Q3 makes balance tunable, not hard; expose the balance-vs-flexibility trade-off.

---

## Cluster D — Dexterous & In-Hand Control

*Multi-fingered hands performing high-DoF, contact-discontinuous, sim-to-real-fragile manipulation — universal cross-morphology control, tactile in-hand reorientation, exploration-driven emergent dexterity, and force-safety bounding.*

### D1 — Universal Cross-Morphology Hand Control

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | A single dexterous policy controlling *any* multi-fingered hand via a unified action space — which the field skips because dexterous policies are trained per-hand on parallel-jaw-centric foundations — has the irreducible truth that dexterous *control intent* (which contacts to form, what in-hand motion) is hand-agnostic while actuation is hand-specific, which breaks the assumption that each hand needs a bespoke policy, and I bet a unified-action-space policy drives the *full in-hand control cycle* zero-shot at [[2512.13644\|DexWM]]'s 72% Reach / 58% Grasp / 28% Place (vs Diffusion-Policy 16% / 0% / 8%) — a control margin A2's grasp-transfer cannot reach — learnt 5.2× cheaper than per-hand collection. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2508.13073\|Large VLM-based VLA Survey]], [[2605.16257\|DexJoCo]] |
| **Key targets** | **Headline (control cycle, A2 cannot claim):** [[2512.13644\|DexWM]] zero-shot 72% Reach / 58% Grasp / 28% Place (vs DP 16% / 0% / 8%) + 83% real-world zero-shot grasp (Allegro) from human video. **Shared cross-morphology evidence (also A2's headline):** [[2603.22264\|UniDex]] 81% task progress + zero-shot 60% (Oymotion) / 40% (Wuji) + 5.2× data-cost cut. **Scaling:** [[2602.19764\|Multi-Sensory Sparse Experts]] 83.2% MT50 (vs RDT-1B 77.9%) + 42.6% compute cut |

**Why it matters.** This is the *control* counterpart to A2's grasp-transfer: A2 transfers the *grasp*, D1 transfers the full *in-hand control* policy. [[2504.03515|Dexterous IL Survey]] and [[2508.13073|Large VLM-based VLA Survey]] both note dexterous manipulation is underserved by parallel-jaw-centric foundation models, and [[2605.16257|DexJoCo]] shows multi-task dexterous training *degrades*. [[2603.22264|UniDex]]'s Function-Actuator-Aligned Space already controls diverse hands (81% task progress, 60%/40% zero-shot transfer, 5.2× cheaper), [[2512.13644|DexWM]] reaches 83% zero-shot grasp by learning hand-keypoint dynamics from human video, and [[2602.19764|Multi-Sensory Sparse Experts]] (DeMUSE) scales capacity via sparse MoE (83.2% MT50, 42.6% compute cut) where "experts specialize in different aspects without increasing latency." The first-principles claim: dexterous *control intent* — the sequence of contacts to form and the in-hand object motion to produce — is hand-agnostic, while only the actuation that realizes it is hand-specific; a policy parameterized by intent transfers, a policy parameterized by joint commands does not.

**First-principles framing.**
- **First principle**: Dexterous control intent (which fingers contact where, what in-hand object motion to produce) is a hand-agnostic plan; the joint torques that realize it are the hand-specific projection. The intent is the invariant — a hammer is held and swung the same way regardless of finger count — and the actuation is the variance.
- **Assumption being challenged**: That each dexterous hand needs a bespoke policy on a parallel-jaw-centric foundation. The field trains per-hand because it parameterizes by joint commands; [[2603.22264|UniDex]] (FAAS, 60%/40% transfer) and [[2512.13644|DexWM]] (hand-keypoint dynamics, 83% zero-shot) show intent-level control transfers — the per-hand assumption is a parameterization artifact, and [[2605.16257|DexJoCo]]'s negative transfer is what joint-space parameterization yields.
- **The bet**: A unified-action-space policy drives the full in-hand control cycle on unseen hands at [[2512.13644|DexWM]]'s 72% Reach / 58% Grasp / 28% Place zero-shot (vs DP 16% / 0% / 8%) and 83% real-world zero-shot grasp — a *control*-phase margin A2's grasp-transfer bet cannot make. It does so learnt 5.2× cheaper than per-hand collection, recovering the same cross-morphology transfer A2 headlines ([[2603.22264|UniDex]]'s 60%/40% to unseen hands — here shared evidence, not the headline) at [[2603.22264|UniDex]]'s 81% in-domain task progress, while sparse-MoE scaling ([[2602.19764|Multi-Sensory Sparse Experts]]' 83.2% MT50, 42.6% compute cut) keeps inference real-time — universal dexterity without per-hand cost or latency blowup.

**Evidence.**
- [[2603.22264|UniDex]] — Function-Actuator-Aligned Space + 3D VLA from egocentric video; 81% task progress, zero-shot 60%/40%, 5.2× cost cut; the unified-control anchor.
- [[2512.13644|DexWM]] — Latent world model on hand-keypoint dynamics from human video + MPC; 83% zero-shot grasp (Allegro), +34% PCK from Hand Consistency Loss; hand-agnostic dynamics from human video.
- [[2602.19764|Multi-Sensory Sparse Experts]] — DeMUSE sparse-MoE multi-sensory DiT; 83.2% MT50 (vs RDT-1B 77.9%), 42.6% compute cut, 80 ms compliance; scalable capacity without latency.
- [[2505.21864|DexUMI]] — Human-hand interface across underactuated + fully-actuated; 86%, 3.2× efficiency; cross-hand control via relative finger actions.
- [[2605.16257|DexJoCo]] — 11-task dexterous benchmark; multi-task degradation; the negative result motivating intent-space.

**Concrete research questions.**
1. **Q1 — Intent-space vs joint-space control transfer.** Parameterize in [[2603.22264|UniDex]]'s FAAS (intent) vs raw joint commands; measure zero-shot in-hand-reorientation SR on a held-out hand — does intent-space recover 60%/40% transfer where joint-space gives negative transfer?
2. **Q2 — Hand-keypoint dynamics as the shared world model.** Use [[2512.13644|DexWM]]'s hand-keypoint world model as the cross-hand dynamics; does a hand-agnostic dynamics model + per-hand actuation beat per-hand end-to-end policies?
3. **Q3 — Sparse-MoE expert specialization by hand.** Does [[2602.19764|Multi-Sensory Sparse Experts]]' MoE naturally route per-hand (one expert per morphology) — and does that beat a dense cross-hand policy at equal latency?
4. **Q4 — Intent + joint-residual.** Use intent-space for the contact plan, a small per-hand joint-residual for fine actuation (couples to A2's grasp-establishment + joint-residual split).

**Related research papers.**
- [[2603.22264|UniDex]] — Universal dexterous control via FAAS; 81% progress, 60%/40% transfer; the anchor.
- [[2512.13644|DexWM]] — Hand-keypoint world model from human video; 83% zero-shot grasp; hand-agnostic dynamics.
- [[2602.19764|Multi-Sensory Sparse Experts]] — DeMUSE sparse-MoE multi-sensory; 83.2% MT50, 42.6% compute cut; scalable capacity.
- [[2505.21864|DexUMI]] — Human-hand interface, cross-hand; 86%; relative-finger transfer.
- [[2605.16257|DexJoCo]] — 11-task benchmark; multi-task degradation; negative result.
- [[2604.20689|FingerEye]] — Per-finger eye-in-hand perception; morphology-specific sensing.
- [[2603.04531|PTLD]] — Privileged tactile latent distillation; +182% rotation; the deployable estimator (feeds D2).
- [[2512.24653|RoboMIND 2.0]] — 310K trajectories, six embodiments; cross-embodiment generalization data.

**Benchmarks & metrics.**
- [[2512.13644|DexWM]] — zero-shot 72% Reach / 58% Grasp / 28% Place (vs DP 16% / 0% / 8%), 83% real-world zero-shot grasp (Allegro), +34% PCK from Hand Consistency Loss; the full-control-cycle metric A2's grasp-transfer cannot claim (the D1 headline).
- [[2603.22264|UniDex]] — 81% in-domain task progress, zero-shot 60% (Oymotion) / 40% (Wuji), 5.2× cost cut; the cross-morphology transfer metric **shared with A2's grasp-transfer headline** (here demoted to evidence, not D1's headline).
- [[2605.16257|DexJoCo]] — 11-task MuJoCo dexterous; DP-T 50.4%→20.0% under randomization, π0.5 highest; the multi-task degradation diagnostic.
- [[2602.19764|Multi-Sensory Sparse Experts]] — 83.2% MT50 (vs RDT-1B 77.9%, RT-2 52.2%), MoE-4E 42.6% compute cut; the scalable-dexterity metric.

> [!warning] Risks
> - **Intent-space abstraction loses fine dexterity** — the contact plan may discard joint-level precision. → Q4's intent + joint-residual split; bound intent-space to the contact-establishment phase.
> - **Transfer 40–60% not deployment-ready** — [[2603.22264|UniDex]]'s Wuji 40%. → Frame as few-shot seed; report the few-shot adaptation curve from the zero-shot baseline.
> - **Sparse-MoE routing may not specialize by hand** — Q3's assumption may fail. → Test routing-by-hand empirically before claiming MoE solves cross-morphology scaling.

### D2 — Tactile In-Hand Reorientation with Sim-to-Real

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | In-hand reorientation policies that learn tactile competence *without simulating tactile sensors* — which the field skips because tactile sim is non-standard and high-gap — has the irreducible truth that real privileged sensors (object pose/shape) can substitute for simulated tactile as the distillation interface, which breaks the assumption that tactile sim-to-real requires accurate tactile simulation, and I bet privileged-to-real tactile distillation beats proprioception-only by [[2603.04531\|PTLD]]'s +182% (rotation) / +57% (reorientation goals) and reaches [[2210.13702\|DeXtreme]]'s 27.8-vs-14.8 reorientations without modeling the sensor. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2510.25725\|HumanoidVTA]], [[2605.16257\|DexJoCo]] |
| **Key targets** | [[2603.04531\|PTLD]] +182% rotation / +57% reorientation goals, robust to slip/mass/wrist; [[2210.13702\|DeXtreme]] 27.8 (VADR) vs 14.8 (manual DR) reorientations at 15 Hz; [[2604.11138\|ViserDex]] 37.6 consecutive reorientations, ~25 under adversarial lighting; [[2601.02778\|Force-Based Sim2Real]] 25.1 vs 1.1 (contact vs no-contact) |

**Why it matters.** In-hand reorientation is the canonical dexterous benchmark, and the standing blocker is tactile sim-to-real: [[2603.04531|PTLD]] notes "accurately simulating tactile sensors is difficult — existing tactile simulators are non-standardized, rely on rigid-body models, and incur a large sim-to-real gap." The dominant approaches either avoid tactile (vision/proprioception only — [[2210.13702|DeXtreme]] 27.8 reorientations, [[2604.11138|ViserDex]] 37.6) or build elaborate tactile sim. [[2603.04531|PTLD]] resolves it differently: train privileged-sensor oracles in sim (object pose/shape as privileged), deploy them in an *instrumented real cell* to collect paired tactile, and distill a deployable tactile state estimator from real data — **never simulating tactile** — for +182% rotation / +57% reorientation goals robust to slip/mass/wrist. [[2601.02778|Force-Based Sim2Real]] confirms the value (25.1 vs 1.1 rotations contact-vs-no-contact). The first-principles claim: the sim-to-real bridge for tactile is the *privileged real sensor* (object pose), not a tactile simulator — so you collect real tactile against a privileged oracle and skip the sim-tactile gap entirely.

**First-principles framing.**
- **First principle**: The hard part of tactile sim-to-real is the *tactile simulator*, but tactile is only an interface — what the policy needs is the privileged state (object pose/shape) the tactile encodes. A *real* privileged sensor (instrumented cell measuring object pose) can supply that interface, so the policy can be distilled from real tactile-vs-privileged pairs without ever simulating a tactile sensor.
- **Assumption being challenged**: That tactile sim-to-real requires accurate tactile simulation. The field either avoids tactile or builds tactile sims; [[2603.04531|PTLD]]'s no-tactile-sim distillation (privileged-real interface) shows the tactile simulator is avoidable — the gap is a self-imposed consequence of insisting on simulating the sensor.
- **The bet**: Privileged-to-real tactile distillation beats proprioception-only by [[2603.04531|PTLD]]'s +182% (rotation) / +57% (reorientation goals), reaches [[2210.13702|DeXtreme]]'s 27.8-vs-14.8 reorientations, and holds under [[2604.11138|ViserDex]]'s adversarial lighting (~25 reorientations) — tactile-level in-hand performance without modeling the sensor.

**Evidence.**
- [[2603.04531|PTLD]] — Privileged tactile latent distillation, no tactile sim; +182% rotation, +57% reorientation goals, robust to slip/mass/wrist, single asymmetric actor-critic step; the no-tactile-sim anchor.
- [[2210.13702|DeXtreme]] — Vectorized Automatic Domain Randomization + Isaac Gym; 27.8 (VADR) vs 14.8 (manual DR) reorientations, 15 Hz vision pose estimator; the sim-to-real reorientation anchor.
- [[2604.11138|ViserDex]] — 3DGS in-the-loop + pre-rasterization augmentation for monocular RGB in-hand; 37.6 consecutive (nominal) / ~25 (adversarial lighting), single-GPU; visual sim-to-real for reorientation.
- [[2601.02778|Force-Based Sim2Real]] — Distance-field tactile sim + current-to-torque calibration; 25.1 vs 1.1 rotations (contact vs no-contact); the contact-vs-no-contact value proof.
- [[2509.18830|DexSkin]] — Conformable skin + pneumatic calibration; 19/20 perturbed reorientation, 5/20→14/20 cross-sensor transfer; real-tactile-hardware reference.

**Concrete research questions.**
1. **Q1 — Privileged-real vs tactile-sim distillation.** Compare [[2603.04531|PTLD]]'s privileged-real interface against a tactile-sim → real pipeline on the same reorientation task — does avoiding the tactile sim recover or exceed the +182%?
2. **Q2 — Tactile vs visual sim-to-real for reorientation.** Compare [[2603.04531|PTLD]] (tactile) vs [[2604.11138|ViserDex]] (monocular RGB 3DGS) on robustness to perturbation — which modality holds better under slip/lighting?
3. **Q3 — Cross-sensor tactile transfer for in-hand.** [[2509.18830|DexSkin]]'s pneumatic calibration transfers across skin instances (5/20→14/20); does calibration-based transfer generalize the [[2603.04531|PTLD]] estimator across tactile hardware?
4. **Q4 — VADR + privileged-tactile combination.** Combine [[2210.13702|DeXtreme]]'s automatic domain randomization with [[2603.04531|PTLD]]'s privileged-tactile distillation — does randomization + real-tactile beat either alone past 27.8 reorientations?

**Related research papers.**
- [[2603.04531|PTLD]] — Privileged tactile latent distillation, no tactile sim; +182% rotation; the anchor.
- [[2210.13702|DeXtreme]] — VADR + Isaac Gym in-hand reorientation; 27.8 vs 14.8; sim-to-real anchor.
- [[2604.11138|ViserDex]] — 3DGS-in-the-loop monocular RGB reorientation; 37.6 / ~25 adversarial; visual sim-to-real.
- [[2601.02778|Force-Based Sim2Real]] — Distance-field tactile sim + calibration; 25.1 vs 1.1; contact-value proof.
- [[2509.18830|DexSkin]] — Conformable skin + pneumatic calibration; 19/20 perturbed, cross-sensor transfer; real-tactile reference.
- [[2605.09789|DRIS]] — Domain-Randomized Instance Set (belief propagation); 68% reactive catching zero-shot; uncertainty-aware sim-to-real (couples to D3).
- [[2603.15257|HapticVLA]] — Sensor-free tactile via distillation; 86.7%; the deployment twin (feeds B3).
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
| **Thesis** | Dexterity that *emerges* from diverse simulator resets + large-scale RL rather than task-specific reward engineering — which the field skips by hand-crafting curricula and demonstrations per task — has the irreducible truth that long-horizon exploration is gated by the *initial-state diversity* the agent sees, not by reward shaping, which breaks the assumption that more compute on a fixed reset distribution closes the exploration gap (it saturates), and I bet diverse-reset RL with one task-agnostic reward yields emergent multi-phase dexterity transferring zero-shot at [[2603.15789\|OmniReset]]'s 25% real peg insertion (vs 4% demo-DP). |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2605.16257\|DexJoCo]], [[2510.25725\|HumanoidVTA]] |
| **Key targets** | [[2603.15789\|OmniReset]] 25% real peg insertion (vs 4% demo-DP), emergent multi-phase from one task-agnostic reward; [[2605.03363\|Hierarchical RL-QP Grasp]] 81.4% sim (vs 13.2% end-to-end RL) + 22/26 unseen real; [[2605.09789\|DRIS]] 68% reactive catching zero-shot (vs 5% hand-crafted, 13% sim-trained) |

**Why it matters.** [[2603.15789|OmniReset]] names the core failure: "standard exploration in parallel sims suffers performance saturation, agents stuck in local optima despite increased compute," and dexterous RL "requires extensive task-specific engineering for rewards, curricula, demonstrations." The dominant fix throws compute at a fixed setup; [[2603.15789|OmniReset]] inverts it — systematically diverse initial-state resets (reaching, near-object, stable grasps, near-goal) with a *single task-agnostic reward* yield emergent multi-phase behaviors and 25% real peg insertion vs 4% for demo-trained DP. [[2605.03363|Hierarchical RL-QP Grasp]] decomposes task-space RL planning from joint-space QP control to escape the monolithic-RL burden (81.4% sim vs 13.2% end-to-end RL, 22/26 unseen real), and [[2605.09789|DRIS]] propagates uncertainty through randomized instance sets for 68% zero-shot reactive catching (vs 5%/13% baselines). The first-principles claim: exploration is gated by *initial-state diversity*, not reward shaping — the agent can only discover a behavior whose precursor states it visits, so broadening the reset distribution (not the reward) is what unlocks emergent dexterity. This is the Hinton-tenet move — favor the mechanism (broad exploration → emergent skill) over the engineering convention (per-task reward shaping).

**First-principles framing.**
- **First principle**: Long-horizon exploration coverage is determined by the initial-state distribution the agent samples, not by reward shaping — a behavior is only discoverable if its precursor states are visited, so reset diversity (not reward density) sets the reachable-behavior ceiling. Emergence is a coverage phenomenon.
- **Assumption being challenged**: That more compute on a fixed reset distribution closes the exploration gap. The field scales parallel envs on a fixed setup and hits saturation ([[2603.15789|OmniReset]]); diverse resets break saturation where compute alone does not — the bottleneck is the reset distribution, not the compute or the reward.
- **The bet**: Diverse-reset RL with one task-agnostic reward yields emergent multi-phase dexterity transferring zero-shot at [[2603.15789|OmniReset]]'s 25% real peg insertion (vs 4% demo-DP), and hierarchical task-space/joint-space decomposition reaches [[2605.03363|Hierarchical RL-QP Grasp]]'s 81.4% sim (vs 13.2% monolithic RL) / 22-26 unseen-object real — dexterity from exploration breadth, not reward engineering.

**Evidence.**
- [[2603.15789|OmniReset]] — Diverse simulator resets + large-scale PPO + gSDE, one task-agnostic reward; emergent multi-phase, 25% real peg insertion (vs 4% demo-DP); the reset-diversity anchor.
- [[2605.03363|Hierarchical RL-QP Grasp]] — Multi-agent task-space RL planner + GPU-parallel joint-space QP; 81.4% sim (vs 13.2% end-to-end RL), 22/26 unseen real, zero-shot steerable; the decomposition anchor.
- [[2605.09789|DRIS]] — Domain-Randomized Instance Set (particle belief propagation); 68% reactive catching zero-shot (vs 5% hand-crafted, 13% sim-trained); uncertainty-aware exploration.
- [[2210.13702|DeXtreme]] — VADR breaks manual-DR saturation; 27.8 vs 14.8; automatic randomization as exploration breadth.
- [[2601.02778|Force-Based Sim2Real]] — Asymmetric actor-critic PPO + randomized actuator; 25.1 rotations; large-scale RL sim-to-real.

**Concrete research questions.**
1. **Q1 — Reset-diversity vs reward-shaping ablation.** Fix the reward task-agnostic, vary only reset diversity ([[2603.15789|OmniReset]]'s reaching/near-object/grasp/near-goal); does diversity alone produce the emergent multi-phase behavior, or is reward shaping needed?
2. **Q2 — Hierarchical decomposition vs monolithic RL.** Compare [[2605.03363|Hierarchical RL-QP Grasp]]'s task-space-RL + joint-QP against end-to-end RL at matched compute — does decomposition recover the 81.4% vs 13.2% gap, and does it transfer better?
3. **Q3 — Uncertainty-propagation as exploration robustness.** Does [[2605.09789|DRIS]]'s instance-set belief propagation (68% vs 13% reactive catching) generalize beyond catching to in-hand reorientation under uncertainty?
4. **Q4 — Emergent dexterity → policy distillation.** Distill the emergent multi-phase RL policy into a deployable visuomotor policy ([[2603.15789|OmniReset]]'s 25% real); does the emergent behavior survive distillation, and does it beat demo-cloning?

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
| **Thesis** | Dexterous policies with *explicit force/kinematic safety constraints* enforced at control time — which the field skips by hoping learned policies stay safe — has the irreducible truth that safety is a hard constraint on the contact-force state that a learned policy cannot guarantee but a physics-based filter can, which breaks the assumption that safety emerges from reward penalties, and I bet a QP/force-bounded controller delivers guaranteed-safe dexterity at [[2605.03363\|Hierarchical RL-QP Grasp]]'s 81.4% (vs 13.2% unconstrained RL) while bounding contact force below [[2602.19764\|Multi-Sensory Sparse Experts]]' ~10 N and [[2509.18830\|DexSkin]]'s 1.53 kPa fragile-object limits. |
| **Anchor surveys** | [[2504.03515\|Dexterous IL Survey]], [[2510.25725\|HumanoidVTA]], [[2605.16257\|DexJoCo]] |
| **Key targets** | [[2605.03363\|Hierarchical RL-QP Grasp]] 81.4% sim + 22/26 unseen real with QP-enforced collision/joint/velocity limits + zero-shot steerability; [[2602.19764\|Multi-Sensory Sparse Experts]] ~10 N stable force + 80 ms compliance (vs baseline force surges); [[2509.18830\|DexSkin]] 90% pressure reduction to 1.53 kPa on fragile objects |

**Why it matters.** Dexterous policies (D1–D3) contact objects with high-DoF hands; without explicit safety, emergent or transferred policies can apply damaging force — [[2602.19764|Multi-Sensory Sparse Experts]] documents baselines suffering "hazardous force surges," and fragile-object tasks ([[2509.18830|DexSkin]]'s blueberries, [[2603.15257|HapticVLA]]'s eggs) fail without force-bounding. The field largely *hopes* learned policies stay safe via reward penalties. [[2605.03363|Hierarchical RL-QP Grasp]] does it properly: a GPU-parallel Quadratic Programming controller "strictly enforces collision avoidance, joint position, and velocity limits," keeping the RL policy "within kinematically feasible and safe regions" (81.4% sim vs 13.2% unconstrained RL, 22/26 unseen real, zero-shot steerable speed-safety trade-off). [[2602.19764|Multi-Sensory Sparse Experts]] maintains stable ~10 N force with 80 ms compliance, and [[2509.18830|DexSkin]] derives interpretable contact force for a pressure-bounded reward (90% reduction to 1.53 kPa). The first-principles claim: safety is a *hard constraint* on the contact-force/kinematic state — a learned policy can only softly penalize violations, but a physics-based filter (QP, impedance, force-bound) can *guarantee* them, so safety belongs in the controller, not the reward.

**First-principles framing.**
- **First principle**: Safety is a hard constraint on the contact-force and kinematic state (force ≤ object tolerance, joints within limits, no collision) — a constraint that must hold *every* step, not in expectation. A learned policy optimizing expected reward cannot guarantee a per-step constraint; a physics-based projection (QP / force-bound) can.
- **Assumption being challenged**: That safety emerges from reward penalties. The field penalizes excess force in the reward and hopes; [[2605.03363|Hierarchical RL-QP Grasp]]'s QP-enforced limits show a learned policy operating *inside* a hard-constraint filter both is safer and trains better (81.4% vs 13.2%) — reward-penalty safety is neither guaranteed nor optimal.
- **The bet**: A QP/force-bounded controller delivers guaranteed-safe dexterity at [[2605.03363|Hierarchical RL-QP Grasp]]'s 81.4% (vs 13.2% unconstrained RL), bounds contact force below [[2602.19764|Multi-Sensory Sparse Experts]]' ~10 N and [[2509.18830|DexSkin]]'s 1.53 kPa fragile-object limits, and adds zero-shot steerability (post-hoc speed-safety adjustment without retraining) — safety as a controller guarantee, not a reward hope.

**Evidence.**
- [[2605.03363|Hierarchical RL-QP Grasp]] — Task-space RL + GPU-parallel QP enforcing collision/joint/velocity limits; 81.4% sim (vs 13.2% end-to-end RL), 22/26 unseen real, zero-shot steerability; the hard-constraint-controller anchor.
- [[2602.19764|Multi-Sensory Sparse Experts]] — Multi-sensory DiT with 6-axis force; stable ~10 N, 80 ms compliance (vs baseline force surges); the force-stability anchor.
- [[2509.18830|DexSkin]] — Interpretable contact force for pressure-bounded reward; 90% reduction to 1.53 kPa, 20%→60% fragile-fruit integrity; the fragile-object force-bound anchor.
- [[2603.15257|HapticVLA]] — Safety-Aware Reward-Weighted Flow Matching penalizing excess force/slip; 86.7%, +45 pp egg; safety-aware training (soft, complementary to hard QP).
- [[2509.19696|Diffusion Impedance Learning]] — Diffusion-based impedance for compliant contact; impedance as the soft-constraint mechanism.

**Concrete research questions.**
1. **Q1 — Hard QP constraint vs soft reward penalty.** Compare [[2605.03363|Hierarchical RL-QP Grasp]]'s QP-filter against [[2603.15257|HapticVLA]]'s reward-penalty on force-violation rate and SR — does the hard filter guarantee safety *and* improve SR (81.4% vs 13.2%)?
2. **Q2 — Force-bound as a control-time projection.** Project policy actions onto a contact-force-bounded feasible set ([[2509.18830|DexSkin]]'s 1.53 kPa) at control time; does projection preserve fragile-object integrity better than penalty-trained policies?
3. **Q3 — Zero-shot steerability of the safety-speed trade-off.** [[2605.03363|Hierarchical RL-QP Grasp]] adjusts speed-safety post-training; quantify how far the trade-off can move without retraining — is the QP-filter the enabler?
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

## Cross-Cutting Themes

> [!tip] Contact Is a First-Class Predicted Quantity, Not a Consumed Observation
> B1, B2, C3, and D2 all invert the field's force-as-input convention into force-as-modeled-quantity, at four points in the stack: B1 predicts the tactile *future* ([[2512.23864|DreamTacVLA]] Think–Dream–Act, 95.0% Peg-in-Hole), B2 makes contact *mode* a discrete predicted latent ($c_t \in$ {free, making, in-contact, sliding, breaking}), C3 makes inter-arm *force* the bimanual coordination variable ([[2604.20444|VTouch++]]'s synchronized channel), and D2 distills *privileged* contact state into a deployable estimator ([[2603.04531|PTLD]] +182%). [[2603.05687|CGP]]'s coupled state+tactile prediction and [[2603.19201|OmniVTA]]'s visuo-tactile world model are the shared mechanism — model the contact, don't just react to it.

> [!tip] The Privileged-to-Deployable Distillation Interface Is the Sim-to-Real Workhorse
> B3, D1, and D2 all route competence through a teacher-student gap where the teacher has privileged access the student lacks: B3 distills tactile-aware behavior into a sensor-free student ([[2603.15257|HapticVLA]] 86.7%), D2 distills privileged object-pose oracles into real tactile estimators *without tactile sim* ([[2603.04531|PTLD]] +182%), and D1 distills cross-morphology intent from privileged multi-hand training ([[2603.22264|UniDex]] 60%/40% transfer). The non-obvious coupling: the *interface* (what privileged signal the teacher exposes) matters more than the policy — [[2603.04531|PTLD]]'s insight that a *real* privileged sensor beats a *simulated* tactile sensor reframes the whole sim-to-real problem, and B3/D1 inherit it. This is the deployment counterpart to [[Sim2Real|Sim2Real]]'s teacher-student threads.

> [!tip] Morphology-Invariant Structure Is the Lever for Cross-Hand Transfer
> A2 and D1 share a representational bet that pixel-and-joint-space approaches miss: grasp *function* and dexterous control *intent* are low-dimensional morphology-invariants, while joint-space geometry is the high-dimensional hand-specific projection. A2 transfers the grasp ([[2603.22264|UniDex]]'s FAAS, [[2505.21864|DexUMI]]'s relative-finger actions), D1 transfers the full in-hand control policy ([[2512.13644|DexWM]]'s hand-keypoint dynamics) — both succeed where [[2605.16257|DexJoCo]]'s joint-space multi-task training *degrades*. They are *separable* contributions, not one bet stated twice, because they own different phases of the manipulation cycle: A2 transfers the **grasp-establishment** phase (form a stable, task-appropriate contact set) and is scored on grasp-transfer SR, while D1 transfers the **in-hand-control** phase (regulate object motion *after* the grasp is established) and is scored on the control cycle ([[2512.13644|DexWM]]'s reach/grasp/place SR, which A2's grasp-transfer cannot claim) — a policy can transfer the grasp without transferring the subsequent reorientation, so the two phases need distinct invariants and distinct bets. The Hinton-tenet move: favor the representation the *task* makes invariant (functional grasp type, contact intent) over the one the *hardware* imposes (joint angles), because a hand is a hand regardless of finger count.
>
> Composition over monolithic scale (C1's [[2511.05275|TwinVLA]]) is the same lever at the bimanual scale: the transferable single-arm *skill* is the invariant, the cross-arm *coupling* is the scarce specific term.

> [!tip] Exploration Breadth and Reset Diversity Beat Reward Engineering and Parameter Count
> D3, D4, and B2 converge on the finding that the lever for hard contact-rich behavior is *coverage and constraint structure*, not scale: D3 shows diverse simulator resets break exploration saturation ([[2603.15789|OmniReset]] 25% real vs 4% demo-DP) where compute alone saturates, D4 shows a hard QP/force constraint both guarantees safety and improves training ([[2605.03363|Hierarchical RL-QP Grasp]] 81.4% vs 13.2% unconstrained), and B2 shows discrete contact-mode structure beats a bigger smooth policy at the friction-cone boundary. [[2210.13702|DeXtreme]]'s automatic-domain-randomization (27.8 vs 14.8) is the shared mechanism — engineer the *exploration distribution and constraint set*, not the reward or the parameter count.

> [!tip] The Integration Layer Is the Bottleneck — Generated Data and Real Residuals Are the Fix
> C2, B2, and C1 all confront the Sim-to-Real Cliff and bimanual data wall that the surveys ([[2604.04974|Video-to-Control Survey]], [[2603.15469|RoCo Challenge]], [[2604.05831|BiCoord]]) name as the central gap — and answer with structure, not raw data: C2 generates bimanual data with coordination structure ([[2410.24185|DexMimicGen]] 90% from 40 demos), B2 closes the assembly cliff with a real-world residual ([[2602.23253|SPARR]] 95–100% [AutoMate](https://arxiv.org/abs/2407.08028)), and C1 sidesteps the data wall by composing single-arm priors ([[2511.05275|TwinVLA]] 76% on ~50 episodes). The shared insight: the hard part is connecting a prediction to dependable contact behavior, and the fixes are coordination-structured generation + real residuals + prior composition — not more teleoperation. Cross-ref [[Sim2Real|Sim2Real]] for the residual/real-to-sim machinery and [[WAM|WAM]] for the imagination-as-data thread.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Affordance-*conditioned* (not post-filtered) grasp generation at task-relevance × stability parity | A1 | [[2604.11674\|AffordSim]] (affordance-guided collection, 79%/64% vs 15%/3%, but generation conditions on affordance separately) + [[2506.17198\|Dex1B]] (scalable stable-grasp, no task-affordance) |
| Function-space cross-morphology *grasp* transfer at in-domain parity | A2 | [[2603.22264\|UniDex]] (FAAS control transfer, 60%/40%, but not grasp-synthesis) + [[2505.21864\|DexUMI]] (cross-hand 86%, exoskeleton-mediated, not zero-shot) |
| Deformable grasping as force-regulation (no defined grasp-pose) with differentiable soft-body | A3 | [[2509.18830\|DexSkin]] (force-regulation, 90% pressure reduction, but rigid skin not soft-body physics) + [[2510.25725\|HumanoidVTA]] (dense soft tactile, no control policy) |
| Tactile-*future* prediction (world model) vs reactive tactile on contact-rich SR | B1 | [[2512.23864\|DreamTacVLA]] (Think–Dream–Act, 95.0% Peg-in-Hole, single system) + [[2603.19201\|OmniVTA]] (visuo-tactile WM + 60 Hz reflexive) |
| Discrete contact-mode latent + reversibility on sub-millimeter insertion | B2 | [[2602.23253\|SPARR]] (95–100% [AutoMate](https://arxiv.org/abs/2407.08028) via real residual, continuous) + [[2502.05086\|REASSEMBLE]] (phase-distinct force patterns, no mode-latent policy) |
| Sensor-free tactile-aware deployment matching sensor-on SR via distillation | B3 | [[2603.15257\|HapticVLA]] (sensor-free 86.7%, tactile-token prediction) + [[2603.04531\|PTLD]] (privileged-to-real, no tactile sim, in-hand only) |
| Coordination-native bimanual at single-arm data cost on tightly-coupled tasks | C1 | [[2511.05275\|TwinVLA]] (composed single-arm, 76% on ~50 episodes, moderate coupling) + [[2604.05831\|BiCoord]] (coordination metrics, vision-only, later-stage degradation) |
| Coordination-*structured* bimanual generation closing later-stage degradation | C2 | [[2410.24185\|DexMimicGen]] (90% from 40 demos via subtask taxonomy) + [[2506.18088\|RoboTwin 2.0]] (MLLM-gen + randomization, +24.4% few-shot) |
| Shared inter-arm tactile channel for force-balanced bimanual cooperation | C3 | [[2604.07335\|TAMEn]] (closed-loop tactile bimanual, 75% SR, per-arm) + [[2604.20444\|VTouch++]] (synchronized bimanual tactile data, no shared-channel policy) |
| Universal cross-morphology *in-hand control* (not just grasp) at real-time latency | D1 | [[2603.22264\|UniDex]] (FAAS, 81% progress, 60%/40% transfer) + [[2602.19764\|Multi-Sensory Sparse Experts]] (sparse-MoE scaling, 83.2% MT50, single-hand) |
| Tactile in-hand reorientation *without tactile simulation* under perturbation | D2 | [[2603.04531\|PTLD]] (privileged-to-real, no tactile sim, +182% rotation) + [[2210.13702\|DeXtreme]] (VADR 27.8 vs 14.8, vision/proprioception only) |
| Emergent multi-phase dexterity from reset-diversity (not reward shaping) transferring real | D3 | [[2603.15789\|OmniReset]] (diverse resets, 25% real peg, single reward) + [[2605.03363\|Hierarchical RL-QP Grasp]] (decomposition 81.4% vs 13.2%, no emergence claim) |
| Hard force/kinematic safety *guarantee* (not reward penalty) at task parity | D4 | [[2605.03363\|Hierarchical RL-QP Grasp]] (QP-enforced limits, 81.4%, no fragile-object force bound) + [[2509.18830\|DexSkin]] (1.53 kPa pressure bound, reward-based not guaranteed) |

---

## Cross-References

- [[../Embodied-AI/02_Dataset-Benchmark-Environment#2. Multi-Modal & Specialist Datasets|02_Dataset-Benchmark-Environment §2]] — Multi-modal manipulation datasets (grasping, dexterous, bimanual)
- [[../Embodied-AI/02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks|02_Dataset-Benchmark-Environment §6]] — Tactile & contact-rich benchmarks (feeds A3, B1–B3, C3, D2)
- [[../Embodied-AI/02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02_Dataset-Benchmark-Environment §8]] — Bimanual & humanoid evaluation (feeds C1–C3)
- [[../Embodied-AI/10_Force-Aware-and-Tactile-Policies#3. Force-Conditioned VLA Architectures|10_Force-Aware-and-Tactile-Policies §3]] / [[../Embodied-AI/10_Force-Aware-and-Tactile-Policies#4. Contact-Rich Manipulation Benchmarks and Visuotactile Policies|§4]] — Force-conditioned VLA architectures + visuotactile policies (feeds B-cluster)
- [[../Embodied-AI/10_Force-Aware-and-Tactile-Policies|10_Force-Aware-and-Tactile-Policies]] — Force-aware design space; the tactile/sensor-substrate deep-dive feeding Cluster D
- [[../Embodied-AI/03_VLA#7. Multi-Sensor & Force-Aware VLAs|03_VLA §7]] / [[../Embodied-AI/03_VLA#8. Humanoid & Bimanual VLAs|§8]] — Multi-sensor + humanoid/bimanual VLAs (feeds B, C)
- [[../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Robotics & embodied-AI topic overview
- [[Embodied-AI|Embodied-AI]] — Umbrella embodied-AI directions; its tactile/sensor-substrate and visuomotor-policy-learning directions feed Cluster D (Dexterous & In-Hand); tool-use and BC/diffusion/VLA policy-learning are developed there, not re-clustered here.
- [[WAM|WAM]] — World-action-model imagination; B1's tactile world model and A3's deformable dynamics borrow the WAM imagination-as-data and substrate threads.
- [[Sim2Real|Sim2Real]] — Sim-to-real / real-to-sim transfer; owns the deformable soft-body physics (A3), the real-residual machinery (B2), and the tactile sim-to-real story (B3, D2).

> [!example] Humanoid reading path
> For a humanoid robot, this doc's **Bimanual (Cluster C)** + **Dexterous (Cluster D)** clusters are the upper-body manipulation subsystem — two-arm coordination (C1–C3) and multi-fingered in-hand control (D1–D4) are what the humanoid's arms and hands do. The humanoid's **legs and locomotion** live in the forthcoming **Locomotion** doc, and the **loco-manipulation coupling** (how the legs stabilize and extend the manipulation workspace, whole-body balance during reaching) lives in the forthcoming **Whole-Body** doc. Read C+D here for the upper body; read the sibling subsystem docs for the lower body and the coupling.
