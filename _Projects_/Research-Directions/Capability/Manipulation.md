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
> What separates manipulation from every other robot skill is the **contact state** — which surfaces press the object, with what force, in what mode — and that state is a latent the policy must *regulate*, not a label it can read off vision. The field's reflex is to scale: more grasp data, more demonstrations, bigger policies. But contact has structure that scaling moves the wrong axis on — a stable grasp is not a functional one, force arrives too late to react to, contact dynamics jump discontinuously at the friction-cone edge, and two arms coordinate through forces vision cannot see.
> These **14 directions across 5 clusters** organize the bets around that contact structure: generate grasps that are *task-feasible* not just stable (A), model contact as a *predicted* quantity not a consumed one (B), treat two-arm *coupling* as the scarce term not the whole policy (C), make dexterous *intent* hand-agnostic and bound its force (D), and get force-competence to deployment with *no runtime tactile sensor* (E).
> The editorial bet: **contact is structure to model, compose, and bound — not data to collect.** The directions that put the contact state into the loss, the action space, or the constraint win where more teleoperation does not.

---

## Methodology

**Scope.** This doc reads ~20 manipulation / dexterous / tactile / bimanual surveys and benchmarks (the Survey Landscape below) plus ~70 method papers from `_KnowledgeHub_/`, cross-checked against [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] and the `Embodied-AI/` deep-dives [[02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]], [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]], and [[05_VLA|05_VLA]]. It owns the **Manipulation subsystem** — arms and hands acting on objects: grasp synthesis, contact-rich assembly, bimanual coordination, dexterous in-hand control, and the tactile data substrate beneath them. Locomotion and whole-body loco-manipulation coupling belong to the sibling [[Locomotion|Locomotion]] and [[Whole-Body|Whole-Body]] docs; tool-use and general policy learning (BC / diffusion / VLA) are cross-referenced to the [[Embodied-AI|Embodied-AI]] umbrella, not re-clustered; world-model imagination and physics-grounding live in [[WAM|WAM]] and [[Sim2Real|Sim2Real]]. Deformables are a single direction inside Grasping (A3), not their own cluster; a non-prehensile cluster was assessed and dropped (only [[2503.16806|DyWA]] has a note — it folds into B as a dynamics-adaptive anchor).

---

## Manipulation Survey Landscape

| Survey / Benchmark | The open problem it names (surveys) / what it measures (benchmarks) | Fuels |
|---|---|---|
| [[2504.03515\|Dexterous IL Survey]] | Data sparsity, generalization gaps, sim-to-real, real-time control, safety; hand-design × tactile coupling under-explored | A1, A2, A3, D1, D2, D3, D4 |
| [[2506.18448\|GraspMAS]] | Language-driven grasp detection is brittle; zero-shot open-vocab grasp reasoning; no contact-quality grounding | A1 |
| [[2507.10672\|VLA Manipulation Survey]] | Scarcity of datasets combining high task complexity + multimodal richness; sim physics-fidelity vs throughput trade-off | A1, B1 |
| [[2508.13073\|Large VLM-based VLA Survey]] | Monolithic-vs-hierarchical fragmentation; RL / world-model / human-video integration immature; force/tactile under-specified | A2, D1 |
| [[2604.04974\|Video-to-Control Survey]] | The integration layer is the critical gap; latent-action identifiability; pre-execution verification; tactile/force integration named | B1, B2 |
| [[2511.02097\|WM Manipulation Survey]] | Structured object-centric representations; physics-awareness ranked 3rd of 13 capabilities; hierarchical long-horizon | A3, B1, B2 |
| [[2502.05086\|REASSEMBLE]] | Insert is the hardest action (highest failure); force-torque reveals phase-distinct patterns; no standardized contact-rich assembly benchmark | B1, B2 |
| [[2603.15469\|RoCo Challenge]] | Sim-to-Real Cliff; sub-millimeter precision; coordinated bimanual; failure-recovery curriculum data > parameter count | C1, C2 |
| [[2604.05831\|BiCoord]] | Long-horizon tightly-coupled spatial-temporal coordination (4× integral); precise alignment; later-stage degradation | C1, C2, C3 |
| [[2407.07788\|BiGym]] | Long-horizon multi-object bimanual; sparse-reward; IL/RL near-0% on stacking + long sequences | C1, C2, C3 |
| [[2506.18088\|RoboTwin 2.0]] | Synthetic-data quality control; superficial domain randomization; embodiment-aware grasp adaptation for heterogeneous dual-arm | C2 |
| [[2605.16257\|DexJoCo]] | Limited multi-fingered task diversity; multi-task training degrades vs transfers; language grounding lacks true generalization | A2, D1, D2, D3, D4 |
| [[2510.25725\|HumanoidVTA]] | Dense tactile is discriminative but current optimization can't leverage it; soft-object contact control unsolved | A3, B1, C3, D2 |
| [[2604.27621\|Robot Learning from Human Videos Survey]] | Action-oriented transfer; tactile/audio/gaze incorporation (1 of 7 open problems); low-quality-video robustness; continual learning | E1, E2 |
| [[2604.15395\|Foundation Models in Robotics Survey]] | Tactile/failure-data scarcity (top-3 bottleneck); embodiment-agnostic action spaces; physics-informed world models | E1, E2 |
| [[2510.24795\|Efficient VLA Survey]] | Data-collection cost; internet-scale human video as a dominant data lever; self-sustaining data; embodiment-agnostic | E1 |
| [[2604.16592\|Cognition WM Survey]] | Tactile-perception under-represented; epistemic world models over structured knowledge; meta-cognition under-developed | E2 |

> [!tip] Convergence patterns
> - **The integration layer, not the policy, is the bottleneck** (5-way): [[2604.04974|Video-to-Control Survey]] (the integration layer is the critical gap, with tactile/force integration named explicitly), [[2603.15469|RoCo Challenge]] (the Sim-to-Real Cliff between a sim policy and dependable real contact), [[2502.05086|REASSEMBLE]] (insert dominates failures because of its multi-step precise-alignment nature), [[2604.05831|BiCoord]] (policy performance degrades in the *later stages* of long-horizon coordination), [[2407.07788|BiGym]] (IL and RL collapse to near-**0%** on long-horizon sequences and stacking) — five suites name the same wall in different words: the hard part is connecting a prediction to dependable contact, not making the prediction, the empirical mandate for Clusters B and C.
> - **Force is consumed as input, never modeled as output** (4-way): [[2604.04974|Video-to-Control Survey]] (tactile/force integration unresolved as a modeling target), [[2511.02097|WM Manipulation Survey]] (physics-awareness ranked **3rd of 13** capabilities, still mostly read not predicted), [[2504.03515|Dexterous IL Survey]] (tactile under-leveraged in the hand-design × tactile coupling), [[2510.25725|HumanoidVTA]] (dense tactile is discriminative but current optimization cannot use it) — four surveys/benchmarks converge that touch is read at the current step, never forecast as a future quantity, the empirical mandate for B1/B2's contact-as-predicted-quantity inversion.
> - **Bimanual data scarcity forces a choice: generate it or avoid needing it** (4-way): [[2506.18088|RoboTwin 2.0]] (prohibitive real bimanual cost; synthetic data lacks quality control), [[2604.05831|BiCoord]] (the 4× coordination integral that monolithic data must cover), [[2407.07788|BiGym]] (the long-horizon dual-arm wall), [[2603.15469|RoCo Challenge]] (failure-recovery curriculum data matters more than parameter count) — four benchmarks hit the same dual-arm data wall, the empirical mandate for C1's compose-priors and C2's structured-generation answers.
> - **Dexterity is bottlenecked by exploration/transfer, not network size** (3-way): [[2605.16257|DexJoCo]] (multi-task dexterous training *degrades* rather than transfers; language grounding lacks true generalization), [[2510.25725|HumanoidVTA]] (the discriminative tactile signal current optimization can't exploit), [[2504.03515|Dexterous IL Survey]] (real-time control, sim-to-real, and safety as the named dexterous blockers) — three sources agree the lever is the exploration distribution, the cross-morphology interface, and the safety constraint, not parameter count, the empirical mandate for Cluster D.

---

## Formal Framing

**The manipulation action-generation object.** A manipulation policy maps observation $o$ (vision $v$, proprioception $q$, optionally tactile $\tau$) and instruction $l$ to an action $a$ (arm pose / joint command, plus finger commands for dexterous hands):

$$\pi: (v, q, \tau, l) \mapsto a, \qquad a = (a_{\text{arm}}, a_{\text{hand}})$$

What distinguishes manipulation from locomotion is the **contact state** $\mathcal{C}$ — the set of object–effector contact points, their forces, and their modes — the latent the action must regulate. Three cluster-specific contact formalisms organize this doc:

| Object | Formalism | Cluster |
|---|---|---|
| **Grasp-pose distribution** | $G \sim p(g \mid v, l)$ — a distribution over 6-DoF (parallel-jaw) or high-DoF (dexterous) grasp poses, scored by a quality + task-affordance metric $Q(g)$ | A |
| **Contact-mode sequence** | $c_{1:T}$, $c_t \in \{\text{free, making, in-contact, sliding, breaking}\}$ — a discrete trajectory through contact modes, each with mode-conditional continuous dynamics; assembly is reaching a target $c_T$ | B |
| **In-hand contact state** | $s_t = (R_{\text{obj}}, \{f_i\}_{i=1}^{n})$ — object orientation $R_{\text{obj}}$ and per-fingertip force/contact $f_i$, evolving under finger-gaiting; reorientation drives $R_{\text{obj}} \to R_{\text{goal}}$ while maintaining stable $\{f_i\}$ | D |

**Grasp synthesis as constrained conditional generation.** The grasp generator $p(g \mid v, l)$ must satisfy a **feasibility constraint** — SDF non-penetration plus force-closure — that the loss can enforce *directly* during training, which is why generation with a feasibility loss plus a light post-optimization step ([[2506.17198|Dex1B]]'s recipe — a seed dataset from optimization, scaled by a generative model, with an SDF loss and post-hoc plausibility correction) beats pure pose regression. A1's move is to make the *task-affordance* score $Q(g)$, not just stability, the conditioning target — because a stable grasp and a functional grasp optimize different objectives.

**Contact as a first-class predicted quantity.** The inverse of force-as-input is to predict the *contact-state trajectory* $c_{1:T}$ jointly with the action, rather than predicting kinematic targets and hoping contact works out. A policy that forecasts the coupled future of robot state *and* expected tactile feedback — then maps it to a physically-consistent executable target ([[2603.05687|CGP]]'s formulation) — can pick the action with the better imagined contact outcome *before* committing. This is what B1 and B2 build on, and the formal content of "model the contact, don't just react to it."

**Coordination as a non-factorizable joint.** Two-arm manipulation carries a joint action $a = (a_L, a_R)$ whose value is *not* $V(a_L) + V(a_R)$. The cross-arm coupling — handover timing, force balance — is the load-bearing term, and benchmarks that target tight coordination measure it directly ([[2604.05831|BiCoord]]'s **4×** spatial-temporal-integral increase over prior suites, with policy performance degrading in the later stages of long-horizon coordination). This is why C1 treats coordination as native structure rather than two independent policies, and why only that coupling — not each arm's transferable single-arm skill — is the scarce bimanual-specific quantity.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Grasping & Grasp Synthesis** | A1, A2, A3 | Generating *task-relevant, feasible* grasps that transfer across objects and morphologies | A1's affordance-scored grasp distribution is what A2 keeps invariant across hands; A3 stresses both on deformables where the grasp-pose is ill-defined. [[2506.17198\|Dex1B]]'s feasibility-constrained generation is the shared substrate, and A2 owns grasp-*establishment* while D1 (Cluster D) owns the in-hand control cycle that follows — distinct phases |
| **B — Contact-Rich Assembly & Precision** | B1, B2 | Sub-millimeter contact where vision is blind and the policy is open-loop | B1's predicted contact-state trajectory is what B2 conditions its discrete-mode dynamics on; sensor-free deployment of both lives in [[#E1 — Sensor-Free Force-Aware Policies\|E1]]. [[2602.23253\|SPARR]]'s real residual and [[2512.23864\|DreamTacVLA]]'s tactile imagination are the shared anchors |
| **C — Bimanual & Dual-Arm Coordination** | C1, C2, C3 | Two-arm coupling is non-factorizable and bimanual data is scarce | C1's coordination-native policy needs C2's generated data; C2 must respect the coupling C1 models; C3 adds the tactile channel that makes force-balanced handovers observable. [[2511.05275\|TwinVLA]] and [[2506.18088\|RoboTwin 2.0]] set the bar |
| **D — Dexterous & In-Hand Control** | D1, D2, D3, D4 | Multi-fingered contact is high-DoF, discontinuous, sim-to-real-fragile | D1's cross-morphology action space is what D2 deploys onto; D3 supplies the behaviors D1 unifies; D4 bounds all three with QP / force-safety. [[2603.04531\|PTLD]]'s distillation and [[2603.15789\|OmniReset]]'s reset diversity are the shared levers |
| **E — Tactile Foundations & Data Substrates** | E1, E2 | Contact-rich, multi-modal data scarcity (4-order gap vs [[2310.08864\|OXE]]) — the substrate A–D consume tactile *from* | E1 deploys force-awareness with no runtime tactile sensor (ego-video pretraining or teacher-distillation); E2's cross-sensor encoder makes any such policy portable across platforms, and is what D2's deployable estimator inherits |

---

## Cluster A — Grasping & Grasp Synthesis

*Generating task-relevant, physically feasible grasp poses that transfer across object categories and hand morphologies — including the case where the grasp-pose itself is ill-defined and the gripper must create the contact rather than find it.*

### A1 — Task-Affordance-Conditioned Grasp Synthesis

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | The right grasp depends on what the object is *for*, not just its shape — a stable hold and a functional hold are different objectives. The field assumes that scaling stable-grasp data eventually yields task-competent grasping. It does not: adding stable grasps moves the wrong axis. The bet is in First-principles below. |
| **Anchor papers** | [[2504.03515\|Dexterous IL Survey]] (survey), [[2507.10672\|VLA Manipulation Survey]] (survey), [[2506.18448\|GraspMAS]] (method), [[2604.11674\|AffordSim]] (method), [[2506.17198\|Dex1B]] (method) |
| **Key targets** | [[2604.11674\|AffordSim]] 79% (medium) / 64% (hard) vs AnyGrasp 15% / 3%, ≥93% of manual-annotation success without annotation; match [[2506.17198\|Dex1B]] 86.0% DexGraspNet at task-relevance parity; [[2505.03233\|SynGrasp-1B]] ~90% real zero-shot as the open-vocab reference |

**Why it matters.**
- **The gap**: the grasp that *holds* a hammer is not the grasp that *uses* it, but the dominant recipe optimizes only for a stable hold and scales that — so functionally-wrong grasps remain stable and get selected.
- **Today's answers**: affordance-as-the-generator's-conditioning is now *settled* — [[2503.07360|AffordDexGrasp]]'s Affordance Flow Matching → Grasp Flow Matching is $p(g \mid v, \text{affordance})$ verbatim (45.1% open-set SR, beating prior methods), [[2603.08021|AffordGrasp]] conditions a latent diffusion model on a predicted affordance map (80.08% OakInk), and [[2512.03874|OmniDexVLG]] / [[2511.09602|ScaleADFG]] generate functional grasps from semantic conditioning; [[2506.17198|Dex1B]] / [[2505.03233|SynGrasp-1B]] only scale *stability*.
- **The opening**: with conditioning settled, the unanswered mechanism is *what affordance buys that geometry cannot* — [[2604.11674|AffordSim]]'s 15%→79% hard-tier jump and ≥93% manual-annotation recovery show the gain is real, but no paper isolates whether task-affordance is the **cross-morphology invariant** (transfers parallel-jaw→dexterous where stable geometry does not) or whether grasp quality **separates** into $Q_{\text{stable}}\cdot Q_{\text{task}}$ recovering the oracle label-free.

**First-principles framing.**
- **First principle**: A grasp's correctness is fixed by the task, not by a firm hold alone — and *what an object is for* is hand-agnostic (a hammer is gripped by the handle whether the hand has two fingers or five), while the stable geometry that realizes a hold is hand-specific. So task-affordance is a candidate cross-morphology invariant; force-closure geometry is not.
- **Assumption being challenged**: Not "scaling stable-grasp data closes the gap" (refuted) nor "conditioning beats filtering" (now *consensus* — [[2503.07360|AffordDexGrasp]], [[2603.08021|AffordGrasp]], [[2405.19291|Grasp-as-You-Say]] all condition the generator on affordance). The live wrong assumption is that conditioning's gain is *task-specific selection*: if it is really the morphology-invariant + separable structure of $Q$, the affordance latent should transfer across hands and factor out the oracle label-free — neither tested by the conditioning crowd.
- **The bet**: Task-affordance is the cross-morphology invariant and grasp quality is product-separable. (1) An affordance-conditioned generator transfers parallel-jaw→dexterous ([[2505.03233|SynGrasp-1B]]→[[2506.17198|Dex1B]]) with ≥10 pp less degradation than the stable-grasp geometry; (2) a product scorer $Q(g)=Q_{\text{stable}}(g)\cdot Q_{\text{task}}(g)$ recovers ≥93% of manual-annotation success ([[2604.11674|AffordSim]]'s oracle) with zero per-object labels, at [[2506.17198|Dex1B]]-class stability (86.0% DexGraspNet). Falsifiable: if affordance transfer degrades as much as geometry, *or* the product score lands <93% of the oracle, affordance is neither the invariant nor separable — it is just a selection signal the conditioning crowd already exploits.

**Related research papers.**

The axis is *how the task-affordance enters the grasp* — as generative conditioning, a post-hoc filter, a separate reasoning stage, or not at all:

| System | Where affordance enters | Key result | What's missing |
|---|---|---|---|
| [[2503.07360\|AffordDexGrasp]] | **generative conditioning** — Affordance Flow Matching → Grasp Flow Matching, $p(g\mid v,\text{affordance})$ | 45.1% open-set SR, sim+real, beats prior on novel categories | conditioning settled, but affordance is *per-task selection* — never tested as the cross-morphology invariant (H3) or as a separable $Q$ (H2) |
| [[2603.08021\|AffordGrasp]] | generative conditioning — cross-modal latent diffusion on a predicted affordance map | 80.08% OakInk semantic accuracy, SOTA zero-shot on HO-3D/AffordPose | same-hand single-arm; no cross-morphology transfer, no product-score factoring |
| [[2405.19291\|Grasp-as-You-Say]] | generative conditioning — progressive diffusion (intention+diversity, then quality) | SOTA intention alignment + diversity, Allegro real-world | proves conditioning works; affordance not framed as invariant or separable |
| [[2512.03874\|OmniDexVLG]] | generative conditioning — diffusion VLM on LMM-reasoned taxonomy/contact/affordance | 0.80 sim / 0.71 real SR, 0.97 coarse taxonomy accuracy | semantic conditioning at scale; single-hand, no morphology-invariance claim |
| [[2511.09602\|ScaleADFG]] | affordance-optimized synthesis → scale-adaptive CVAE | 94.58% functional SR, 76.0% real Allegro across 15 novel objects | scale-invariant within one hand; multi-hand *dataset* but per-hand prediction |
| [[2505.12294\|PartDexTOG]] | part-level conditional diffusion (LLM part-analysis) | lowest P-FID 14.24, +3.58% penetration on OakInk, 47 unseen objects | part-affordance conditioning; no transfer-vs-geometry or product-separability test |
| [[2604.11674\|AffordSim]] | open-vocab 3D affordance (VoxAfford) guides a two-stage grasp selection | 79% / 64% vs AnyGrasp 15% / 3%; recovers 93% of manual annotation | affordance *guides selection*, not the generator's conditioning distribution |
| [[2506.17198\|Dex1B]] | none — feasibility-constrained generation (CVAE + SDF loss + post-opt) | 86.0% DexGraspNet, 96% sim-to-real over three hands | scales *stability*; no task-affordance term — the substrate A1 conditions |
| [[2505.03233\|SynGrasp-1B]] | none — billion-frame synthetic pre-training (2D box → 3D grasp CoT) | ~90% real zero-shot, 93.3% language-conditioned | open-vocab but stability-centric; the scaling reference A1 must beat on function |
| [[2212.08333\|AnyGrasp]] | none — pure 7-DoF stable-grasp perception (geometry + stable-score) | 93.3% bin-picking (≈human 93.9%), >900 MPPH | the field's stable-grasp reference whose hard-task collapse (15%/3% per [[2604.11674\|AffordSim]]) is the gap A1 fills; no task term at all |
| [[2606.09314\|KPGrasp]] | none — all-Euclidean keypoint flow-matching, implicit data priors (no contact loss / no test-time refinement) | 76.3% Dexonomy GSR, 2.4 mm penetration, 87× faster inference | scales *stability* from data like [[2506.17198\|Dex1B]] but with a cleaner keypoint param; no task-affordance — the generator A1 conditions |
| [[2601.07060\|PALM]] | separate affordance predictor (relevance + contact geom + motion) + progress signal | +17.7 pp CALVIN ABC→D | affordance as reasoning, not generative conditioning — a candidate map source |
| [[2606.02551\|AFUN]] | affordance foundation model predicting functional masks + post-contact motion | 90% real SR, no fine-tuning | the affordance-map source A1's generator could condition on, still upstream of generation |
| [[2606.02432\|NDPP-Grasp]] | non-differentiable plausibility guidance *inside* task-aligned grasp diffusion | 395.8 ms → 17.7 ms per grasp | feasibility-during-generation, but plausibility not task-affordance — the mechanism A1 borrows for $Q(g)$ |
| [[2606.03385\|GTP-FA]] | grasp-then-plan with failure attribution for stable-but-unusable grasps | +65.6 pp real Franka (π0.5 11.2% → 76.8%) | treats the stable-vs-functional gap as *attribution*, not conditioning |
| [[2604.11320\|CLASP]] | dual-pathway open-vocab grasping | 87.0% pick SR in clutter | geometric/stability-centric; no functional-affordance objective |
| [[2511.04357\|GraSP-VLA]] | graph-based symbolic long-horizon grasp planning | symbolic plan over grasps | symbolic, no generative synthesis, no contact-quality grounding |
| [[2506.18448\|GraspMAS]] | multi-agent zero-shot language-driven grasp reasoning | zero-shot open-vocab detection | reasoning-heavy, no contact-quality grounding — the open-vocab reasoning route |
| [[2605.05925\|DexSynRefine]] | HOI prior + task-space residual RL grounds the grasp | 68.1% sim, +50–70 pp real over retargeting | synthesis-then-ground, complementary; affordance not the generative condition |

**Hypotheses & tests.** The FP bet — task-affordance is the morphology-invariant, separable term, beyond the now-settled conditioning headline — decomposed (H3/H2 carry the surviving novelty):
1. **H1 — Conditioning still beats post-filtering on the hard tier (settled-background check).**
   - *Prediction*: conditioning [[2506.17198|Dex1B]]'s CVAE on [[2604.11674|AffordSim]]'s VoxAfford latent so $p(g \mid v, \text{affordance})$ proposes only task-relevant grasps beats affordance-as-filter most on the hard tier (the 3%→64% gap), by ≥10 pp — the result [[2503.07360|AffordDexGrasp]] / [[2603.08021|AffordGrasp]] already imply, re-confirmed here as the baseline the novel claims build on.
   - *Test*: ablate conditioning vs filtering at matched affordance model on AffordSim's 50-task hard split.
   - *Row*: [[2503.07360|AffordDexGrasp]] (generative conditioning) vs [[2604.11674|AffordSim]] (guides selection).
   - *Falsifier*: filtering ties conditioning on the hard tier → even the settled premise fails on this benchmark and the cluster's consensus is benchmark-fragile.
2. **H2 — A product score recovers manual annotation without labels.**
   - *Prediction*: a unified scorer $Q(g) = Q_{\text{stable}}(g)\cdot Q_{\text{task}}(g)$ (force-closure × affordance relevance) recovers ≥93% of manual-annotation success with zero per-object grasp labels.
   - *Test*: train the product scorer; compare against the manual-annotation oracle on AffordSim.
   - *Row*: [[2606.02551|AFUN]] (functional-mask source) feeding [[2506.17198|Dex1B]] (no affordance term).
   - *Falsifier*: the product score lands <93% of the oracle → affordance + stability is not separable into a product.
3. **H3 — Task-affordance is morphology-invariant where stable geometry is not.**
   - *Prediction*: an affordance-conditioned generator transfers from parallel-jaw ([[2505.03233|SynGrasp-1B]]) to high-DoF hands ([[2506.17198|Dex1B]]) with less degradation than the stable-grasp geometry, because *what the object is for* is hand-agnostic.
   - *Test*: train on parallel-jaw, evaluate the affordance-conditioned vs stable-only generator zero-shot on a dexterous hand. (Feeds Cluster D's D1 / A2.)
   - *Row*: [[2505.03233|SynGrasp-1B]] (parallel-jaw) vs [[2506.17198|Dex1B]] (dexterous).
   - *Falsifier*: affordance transfer degrades as much as geometry → affordance is not the invariant.
4. **H4 — Plausibility-during-generation extends to affordance-during-generation.**
   - *Prediction*: replacing [[2606.02432|NDPP-Grasp]]'s non-differentiable plausibility guidance with a non-differentiable *affordance* score inside the diffusion sampler keeps its 17.7 ms latency while adding task-relevance.
   - *Test*: swap the guidance signal; report task-SR and per-grasp latency.
   - *Row*: [[2606.02432|NDPP-Grasp]] (plausibility-during-generation).
   - *Falsifier*: affordance guidance blows past the latency budget or fails to lift task-SR → guidance must stay plausibility-only.
5. **H5 — Language reasoning can supply the affordance map with no grasp labels.**
   - *Prediction*: [[2506.18448|GraspMAS]] / [[2601.07060|PALM]]-style language reasoning produces an affordance map that conditions generation as well as a trained VoxAfford, closing the open-vocab loop with zero grasp annotation.
   - *Test*: condition the generator on reasoning-derived vs trained affordance maps; compare hard-tier SR.
   - *Row*: [[2506.18448|GraspMAS]] (reasoning) and [[2601.07060|PALM]] (reasoning + progress).
   - *Falsifier*: reasoning-derived maps under-condition (>10 pp below VoxAfford) → the affordance map must be learned from grasp supervision.

> [!warning] Risks
> - **Affordance accuracy is the ceiling** — [[2604.11674|AffordSim]] notes VoxAfford accuracy is the primary success factor. → Bound the claim to tasks where the affordance model is reliable; report the affordance-quality vs grasp-success curve (H1's denominator).
> - **Stable-grasp regression is already strong** — [[2505.03233|SynGrasp-1B]] hits ~90% on generic grasping, so an average over easy tasks hides the gain. → Score on affordance-critical tasks (pouring, hanging, tool-use), where the 15%→79% gap lives.
> - **Affordance and stability can conflict** — the functional grasp may be less stable. → Make $Q$ a tunable product (H2), not a hard constraint; expose the trade-off as a Pareto front so the operating point is explicit.

### A2 — Cross-Morphology Grasp Transfer

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | A grasp's *function* — oppose, enclose, pinch — is the same across hands; only the joint-space geometry that realizes it differs. The field assumes each new dexterous hand needs its own dataset and policy. That per-hand cost is a parameterization artifact, not a law. The bet is in First-principles below. (A2 transfers the *grasp*; Cluster D's D1 transfers the in-hand *control cycle* that follows — distinct phases, distinct bets.) |
| **Anchor papers** | [[2504.03515\|Dexterous IL Survey]] (survey), [[2508.13073\|Large VLM-based VLA Survey]] (survey), [[2605.16257\|DexJoCo]] (benchmark), [[2603.22264\|UniDex]] (method), [[2505.21864\|DexUMI]] (method) |
| **Key targets** | [[2603.22264\|UniDex]] 81% task progress + zero-shot 60% (Oymotion) / 40% (Wuji), 5.2× data-cost cut; [[2505.21864\|DexUMI]] 86% cross-hand SR + 3.2× collection efficiency; [[2605.16257\|DexJoCo]] DP-T 50.4%→20.0% under randomization as the negative-transfer floor |

**Why it matters.**
- **The gap**: function-space-transfers is no longer the open question — [[2410.02479|Cross-Embodiment DexGrasp]]'s human-eigengrasp universal action space (ICLR'25) transfers grasping zero-shot to unseen hands, predating [[2603.22264|UniDex]], and [[2603.16806|DexGrasp-Zero]] reaches 85% sim / 82% real zero-shot on unseen hands. The *new* open question: which cross-hand parameterization is the right invariant — continuous function-space, or a discrete grasp-taxonomy bottleneck?
- **Today's answers**: continuous function-space wins broadly — [[2603.22264|UniDex]]'s FAAS (60%/40% zero-shot, 5.2× cost cut), [[2410.02479|Cross-Embodiment DexGrasp]]'s eigengrasps (80% in-domain over 4 hands, 35.2% zero-shot on 2 unseen), [[2505.21864|DexUMI]]'s relative-finger actions (86%); [[2502.16420|AnyDexGrasp]] cuts per-hand data from millions of labels to ~hundreds of attempts (75–95% across 3/4/5-finger hands).
- **The opening**: [[2604.04138|Sparse Taxonomy Grasp]] builds the discrete-taxonomy→continuous-policy stack (30 templates, 87.9% Objaverse, +28.57% contact precision via multiplicative reward) but only for *controllability*, never as a *transfer* bottleneck — leaving open whether stripping hand-specific detail through a discrete grasp-type latent transfers cross-hand *better* than continuous function-space.

**First-principles framing.**
- **First principle**: A grasp is defined by what it does — which surfaces press the object, at what force — not by the joint angles that produce it. The grasp *type* (power / precision / lateral) is the low-dimensional invariant; a *continuous* function-space still carries hand-specific residue, whereas a *discrete* grasp-taxonomy bottleneck forces it out entirely — so the discrete latent should be the cleaner cross-hand carrier.
- **Assumption being challenged**: Not "each hand needs its own data/policy" (refuted) nor "function-space transfers" (now consensus — [[2410.02479|Cross-Embodiment DexGrasp]], [[2603.16806|DexGrasp-Zero]], [[2505.21864|DexUMI]]). The live wrong assumption is that *continuous* function-space is the right invariant: [[2604.04138|Sparse Taxonomy Grasp]] uses a discrete taxonomy only for control, never testing whether the discrete bottleneck transfers *better* than continuous FAAS — the comparison no one has run.
- **The bet**: A discrete grasp-taxonomy latent (power/precision/lateral type + continuous force) transfers grasp-establishment to unseen hands *better* than continuous FAAS at matched data, beating [[2603.22264|UniDex]]'s 60%/40% zero-shot, because the discrete bottleneck strips the hand-specific residue continuous spaces retain — at ≥5× lower per-hand cost ([[2603.22264|UniDex]] 5.2×) and [[2505.21864|DexUMI]]-class in-domain SR (86%). Falsifiable two ways: if the discrete latent loses to continuous FAAS on the held-out hand, continuous function-space already captures the invariant; and if a joint-space policy with equal data matches *either* on a held-out hand, the invariant is not function at all.

**Related research papers.**

The axis is *what coordinate the policy is parameterized in* — function/intent space, exoskeleton-normalized, task-space residual, or raw joint-space (and the data source feeding it):

| System | Action parameterization | Key result | What's missing |
|---|---|---|---|
| [[2603.22264\|UniDex]] | continuous Function-Actuator-Aligned Space from ego video | 81% progress, zero-shot 60% / 40%, 5.2× cost cut | continuous space retains hand-specific residue; never compared against a discrete taxonomy bottleneck (H2) |
| [[2410.02479\|Cross-Embodiment DexGrasp]] | continuous human-eigengrasp universal action space + neural retargeting (ICLR'25) | 80% over 4 trained hands, 35.2% zero-shot on 2 unseen, 87.2%/64.3% after finetune | the foundational continuous-invariant predating UniDex; eigengrasp is continuous, not a discrete grasp-type latent |
| [[2603.16806\|DexGrasp-Zero]] | morphology-aligned graph + hand-agnostic motion-primitive space (URDF injection) | 85% sim / 82% real zero-shot unseen hands (+59.5 pp over CrossDex) | strongest continuous transfer; primitive-space still continuous — the bar the discrete-taxonomy bet must beat |
| [[2502.16420\|AnyDexGrasp]] | contact-centric universal rep + hand-specific decision stage | 75–95% across 3/4/5-finger hands, 40 objects / hundreds of attempts | dwarfs the ≥5× data-cut target; two-stage but continuous contact rep, no discrete-vs-continuous transfer test |
| [[2604.04138\|Sparse Taxonomy Grasp]] | **discrete** grasp-taxonomy (30 templates) → taxonomy-conditioned control | 87.9% Objaverse, +28.57% contact precision (multiplicative reward), real humanoid | builds the discrete-taxonomy stack but for *controllability* — never tests it as a cross-hand *transfer* bottleneck (the exact gap A2 fills) |
| [[2505.21864\|DexUMI]] | relative-finger actions via robot-specific exoskeleton + visual inpainting | 86% across Inspire + XHand, 3.2× efficiency | exoskeleton-mediated, not zero-shot to a hand with no exoskeleton |
| [[2509.22149\|DemoGrasp]] | single-step-MDP RL editing of one grasp demo | 86.5% on 110 unseen real, 84.6% cross-dataset, cross-embodiment | one-demo transfer, but per-grasp editing rather than a function-space policy |
| [[2606.03268\|EaDex]] | MANO retargeting + contact-reward annealing from single RGB-D human demo | 36.5% across 9 tasks, +55.3% over fixed-weight | low-cost cross-hand data, but lower SR — a data source, not the transfer policy |
| [[2511.09484\|SPIDER]] | physics-informed dexterous retargeting | 2.4M feasible frames across 5 hands + 4 humanoids, +18% from virtual-contact | the cross-hand retargeting-data *engine*, upstream of the policy |
| [[2605.05925\|DexSynRefine]] | task-space residual RL grounding an HOI prior | 68.1% sim, +50–70 pp real over retargeting | task-space action is the transfer enabler; not a function-space taxonomy |
| [[2602.09013\|VIDEOMANIP]] | 3D hand-object trajectory reconstruction from RGB human video | 62.86% real (LEAP Hand), contact-opt 30.7% → 63.75% | human-video cross-hand source, single-hand target |
| [[2606.10614\|Dexterous Point Policy]] | unified 6-keypoint (wrist + 5 fingertips) abstraction over human + robot, AR transformer + contact-prediction | 75.0% over 8 dexterous tasks (vs VITRA 1.0%), +71.3 pp from contact head | a keypoint-space transfer cousin of FAAS; demonstrated single-hand, not yet a cross-hand taxonomy |
| [[2505.11709\|EgoDex]] | large-scale egocentric-video dexterous learning | goal-conditioning −22% distance, scales with data | the ego-video cross-hand data substrate, not the action space |
| [[2403.07788\|DexCap]] | portable mocap for dexterous manipulation | 0.8 cm drift (vs 11.3 cm IMU), 72% from 30 min human data | the human-mocap collection system, upstream of transfer |
| [[2506.17198\|Dex1B]] | per-hand policies over cross-hand data | 1B grasps across three hands | cross-hand *data* but per-hand *policies* — the negative of the bet |
| [[2604.20689\|FingerEye]] | per-finger eye-in-hand perception | morphology-specific fingertip sensing | morphology-specific by design — the opposite of function-invariant |
| [[2603.04531\|PTLD]] | privileged tactile latent distillation | +182% rotation | the deployable estimator a transferred policy needs (feeds D2) |
| [[2605.16257\|DexJoCo]] | joint-space multi-task training (benchmark) | DP-T 50.4% → 20.0% under randomization | the negative-transfer floor that function-space must convert into transfer |

**Hypotheses & tests.** The FP bet — the discrete grasp-taxonomy bottleneck is the better cross-hand invariant, beyond now-settled function-space transfer — decomposed (H2 carries the surviving novelty):
1. **H1 — Function-space recovers zero-shot transfer where joint-space gives ~0% (settled-background check).**
   - *Prediction*: a grasp policy in [[2603.22264|UniDex]]'s FAAS recovers 60% / 40% zero-shot on a held-out hand where the same policy in raw joint-space yields near-0% — the result [[2410.02479|Cross-Embodiment DexGrasp]] / [[2603.16806|DexGrasp-Zero]] already establish, re-run as the baseline H2 builds on.
   - *Test*: matched-data ablation, FAAS vs joint-space, on Oymotion + Wuji held out.
   - *Row*: [[2603.22264|UniDex]] (continuous FAAS) vs [[2506.17198|Dex1B]] (per-hand joint-space).
   - *Falsifier*: joint-space matches FAAS on the held-out hand → the invariant is not function and the cluster's consensus is benchmark-fragile.
2. **H2 — A discrete grasp-taxonomy latent beats continuous FAAS on transfer.**
   - *Prediction*: parameterizing by a power/precision/lateral grasp-type latent + continuous force transfers *better* than continuous FAAS on a held-out hand, because the discrete bottleneck strips the hand-specific residue continuous spaces retain — the comparison [[2604.04138|Sparse Taxonomy Grasp]] never ran (it tested the taxonomy for control, not transfer).
   - *Test*: train the taxonomy-latent policy and continuous FAAS on the same hands; compare zero-shot SR on Oymotion + Wuji held out.
   - *Row*: [[2604.04138|Sparse Taxonomy Grasp]] (discrete taxonomy, control-only) vs [[2603.22264|UniDex]] (continuous FAAS).
   - *Falsifier*: the discrete latent loses to FAAS → continuous function-space already captures the invariant and the discrete bottleneck buys nothing.
3. **H3 — Exoskeleton-normalized data beats kinematic retargeting for transfer quality.**
   - *Prediction*: [[2505.21864|DexUMI]]'s exoskeleton-normalized demos yield higher cross-hand SR than kinematic retargeting (e.g. [[2605.05925|DexSynRefine]]'s retargeting baseline) at matched volume.
   - *Test*: train identical policies on exoskeleton vs retargeted data; compare cross-hand SR.
   - *Row*: [[2505.21864|DexUMI]] (exoskeleton) vs [[2605.05925|DexSynRefine]] (task-space residual on retargeting).
   - *Falsifier*: retargeting ties the exoskeleton → the normalization is not the lever.
4. **H4 — Function-space parameterization converts negative transfer into transfer.**
   - *Prediction*: re-parameterizing [[2605.16257|DexJoCo]]'s degrading multi-task setup in function-space turns the 50.4%→20.0% degradation into a positive transfer curve.
   - *Test*: re-run DexJoCo multi-task training in FAAS vs joint-space.
   - *Row*: [[2605.16257|DexJoCo]] (joint-space, degrades).
   - *Falsifier*: function-space also degrades on DexJoCo → multi-task degradation is not a parameterization problem.
5. **H5 — One demo amortizes across hands when edited in function-space.**
   - *Prediction*: [[2509.22149|DemoGrasp]]'s single-demo RL editing, lifted into function-space, holds its 86.5% on 110 unseen objects *and* transfers to an unseen hand without a new demo.
   - *Test*: edit one demo in function-space, evaluate cross-object and cross-hand.
   - *Row*: [[2509.22149|DemoGrasp]] (single-step-MDP editing).
   - *Falsifier*: cross-hand SR collapses → single-demo editing is hand-specific.

> [!warning] Risks
> - **Function-space loses fine dexterity** — fine manipulation may need joint-level control. → Use function-space for grasp-establishment, a joint-space residual for fine in-hand (couples to D1); H2 bounds where the abstraction holds.
> - **40–60% transfer is not deployment-ready** — [[2603.22264|UniDex]]'s Wuji 40% is a research result. → Frame as a few-shot seed; report the few-shot curve from the 40% zero-shot baseline.
> - **Negative-transfer risk** — [[2605.16257|DexJoCo]] shows multi-hand training can degrade. → H4's degradation-vs-transfer test is the go/no-go before scaling to many hands.

### A3 — Deformable-Object Grasping under Ill-Defined Contact

| | |
|---|---|
| **Cluster** | A — Grasping & Grasp Synthesis |
| **Thesis** | For cloth, rope, and soft objects there is no canonical grasp-pose — the contact configuration is a continuum the gripper *creates*, not a pose it *finds*. The field assumes grasp synthesis equals pose selection on a rigid geometry. For a deformable, the pose is ill-defined and the rigid-body feasibility loss does not apply. The bet is in First-principles below. |
| **Anchor papers** | [[2504.03515\|Dexterous IL Survey]] (survey), [[2511.02097\|WM Manipulation Survey]] (survey), [[2510.25725\|HumanoidVTA]] (benchmark), [[2509.18830\|DexSkin]] (method) |
| **Key targets** | [[2509.18830\|DexSkin]] 90% pressure reduction (14.5→1.53 kPa) + blueberry integrity 20%→60%, 19/20 perturbed reorientation; cross-ref [[Sim2Real\|Sim2Real]] for differentiable soft-body physics; [[2510.25725\|HumanoidVTA]] dense-tactile soft-object discrimination |

**Why it matters.**
- **The gap**: a towel, sponge, or blueberry has no canonical grasp-pose — the contact is something the gripper produces by *how* it closes, so the "right" grasp is force you regulate, not geometry you localize, and pose-selection has no target to optimize.
- **Today's answers**: force-regulation-beats-pose-selection is now *settled* — [[2510.25405|Stress-Guided RL]]'s closed-loop stress-penalized SAC cuts internal stress 36.5% vs vanilla RL, transfers zero-shot sim-to-real to tofu (foam water-loss 41.9%→10.0% at 100% pick-up), and [[2602.10013|Force-Regulated Manipulation]]'s decoupled 80 Hz force-adaptation policy raises stable-grasp rate 38%→68% — both regulate force without a canonical pose; [[2509.18830|DexSkin]]'s conformable skin cuts berry pressure 90% (14.5→1.53 kPa), integrity 20%→60%, 19/20 perturbed.
- **The opening**: the settled solutions are deliberately *vision-only / model-free* — [[2510.25405|Stress-Guided RL]] is RGB-D + PointNet (no tactile) and uses MPM only as a train-time stress oracle, not a control model. So the unanswered mechanism: does **dense tactile + a differentiable soft-body world model** beat the vision-only stress-RL solution on *held-out / unseen* deformables, where [[2510.25725|HumanoidVTA]] shows dense tactile is discriminative but current optimization cannot use it?

**First-principles framing.**
- **First principle**: For a deformable object the contact state is a continuum the effector *produces*, not a pose it *selects* — shape under contact is a function of the applied force field. A vision-only stress-RL policy regulates that field reactively *through one observation modality*; dense tactile measures the field directly at the contact, and a differentiable soft-body model predicts where the field is heading — both are upstream of vision, so they should extrapolate to unseen deformables where reactive vision-only regulation does not.
- **Assumption being challenged**: Not "grasp synthesis = pose selection" (refuted) nor "force-regulation beats pose-selection" (now *consensus* — [[2510.25405|Stress-Guided RL]], [[2602.10013|Force-Regulated Manipulation]], [[2509.18830|DexSkin]]). The live wrong assumption is that *vision + simulated stress is enough*: [[2510.25405|Stress-Guided RL]] explicitly omits tactile sensors and any differentiable soft-body control model, betting reactive vision suffices — untested on held-out deformables where the force field is unfamiliar.
- **The bet**: Dense tactile + a differentiable soft-body world model *beats the vision-only stress-RL solution* ([[2510.25405|Stress-Guided RL]]) on **held-out / unseen** deformables, not just on the training set. (H1) it holds where rigid-grasp estimators have no target; (H2) dense tactile beats sparse on *control SR* (not just discrimination) by ≥10 pp; (H3) the differentiable soft-body model beats model-free stress-RL on unseen objects; matching [[2509.18830|DexSkin]]'s 90% pressure reduction / 20%→60% integrity in-distribution. Falsifiable: if the vision-only stress-RL policy ties dense-tactile+soft-body on held-out deformables, the distinctive substrate buys nothing over reactive vision.

**Related research papers.**

The axis is *how the policy represents the deformable contact* — force-regulation, dense-tactile sensing, or a differentiable soft-body dynamics model (and where each falls short):

| System | Deformable-contact representation | Key result | What's missing |
|---|---|---|---|
| [[2510.25405\|Stress-Guided RL]] | **vision-only** stress-penalized SAC (RGB-D + PointNet; MPM as train-time stress oracle) | 36.5% stress cut vs vanilla RL, zero-shot tofu, foam water-loss 41.9%→10.0% at 100% pick-up | the topThreat — owns force-regulation + H4, but no tactile sensor + no differentiable-soft-body control model; never tested on held-out deformables (the wedge A3 attacks) |
| [[2602.10013\|Force-Regulated Manipulation]] | decoupled base policy + 80 Hz reactive force-adaptation (sparse tactile + wrist vision) | stable-grasp rate 38%→68%, 60% task SR over 5 force-sensitive tasks | residual force-control architecture; sparse tactile, model-free — the dense-vs-sparse + model-based comparators A3 runs |
| [[2509.18830\|DexSkin]] | conformable capacitive skin + residual RL (force-regulation) | berry pressure 90% cut (14.5→1.53 kPa), integrity 20%→60%, 19/20 perturbed | force-regulation anchor; rigid skin, not a soft-body physics model |
| [[2510.25725\|HumanoidVTA]] | 2,124-sensor dense tactile on soft objects | dense separates pressure conditions where sparse fails | dense-tactile substrate, but no control policy — discrimination only |
| [[2604.20444\|VTouch++]] | 120K-episode synchronized vision+tactile+proprioception | soft-contact data at scale | a data substrate; no deformable force-regulation policy |
| [[2511.04665\|Real-to-Sim GS]] | 3DGS + soft-body digital twin | r=0.915 (push-T) / 0.901 (rope) sim-real | the differentiable-soft-body *eval* substrate (cross-ref [[Sim2Real|Sim2Real]]) |
| [[2510.21447\|PhysWorld-Deformable]] | deformable-object world model from real videos | 799 FPS (47× PhysTwin), Chamfer 0.010, MPPI planning | the deformable dynamics-model route, not closed-loop force-regulation |
| [[2604.08544\|SIM1]] | physics-aligned simulator as zero-shot data scaler | 76% zero-shot (vs 0% real-data), 27× cost cut, 70% on unseen polo | the deformable synthetic-data engine, upstream of the policy |
| [[2603.05687\|CGP]] | coupled robot-state + tactile trajectory prediction | real-time, physically-consistent targets | contact-as-trajectory (feeds B1); rigid-contact, not deformable-specific |
| [[2606.04269\|Instant-Fold]] | in-context IL from one human folding demo | 60.9% real zero-shot on 8 unseen garments | folding-as-task-completion, sidesteps the grasp-pose entirely |
| [[2605.09538\|PhysHanDI]] | physics-based reconstruction of hand-deformable interaction | sparse-view RGB-D reconstruction | the deformable-HOI dynamics substrate (cross-ref [[Sim2Real|Sim2Real]]) |
| [[2604.20841\|DeVI]] | physics-based dexterous HOI from synthetic-video imitation | 25–41 mm MPJPE (vs 91–142 mm), 50.0% GRAB success ratio | physics-grounded soft-contact HOI, not a deployable grasp policy |
| [[2312.00583\|DeformGS]] | scene-flow tracking in highly deformable scenes | 27.75 mm MTE (76% below DynaGS) on cloth/duvet | the deformable-state perception substrate, not control |
| [[2302.04659\|ManiSkill2]] | real-time rigid-MPM soft-body simulation | 80–84 FPS; low IL/RL SR | the soft-body throughput baseline; reveals the algorithmic gap |
| [[2210.13066\|DaXBench]] | differentiable-physics deformable benchmark (rope/cloth/fluid) | differentiable RL/IL/planning baselines | a benchmark, not a method — the differentiable-physics test bed |
| [[2011.07215\|SoftGym]] | image-RL deformable benchmark (cloth/rope/fluid) | image-RL struggles vs state oracle | the cloth-RL difficulty floor |
| [[2104.03311\|PlasticineLab]] | soft-body benchmark with differentiable physics | gradient methods beat RL via softened contact | the soft-body differentiable-gradient benchmark |

**Hypotheses & tests.** The FP bet — dense-tactile + differentiable-soft-body beats the vision-only stress-RL solution on held-out deformables — decomposed (H1/H2/H3 are the front-line falsifiers vs [[2510.25405|Stress-Guided RL]]):
1. **H1 — Force-regulation wins where pose-selection has no target (settled-background check).**
   - *Prediction*: a force-regulation policy ([[2510.25405|Stress-Guided RL]] / [[2509.18830|DexSkin]]-style) beats a rigid-grasp estimator on towel/sponge/fruit, because the estimator has no defined pose to regress to — the premise now settled by the stress-RL crowd, re-confirmed as the floor H2/H3 build on.
   - *Test*: head-to-head force-regulation vs rigid-grasp estimator on deformable grasping.
   - *Row*: [[2510.25405|Stress-Guided RL]] (force-regulation) vs the rigid-pose generators ([[2506.17198|Dex1B]]-class).
   - *Falsifier*: the rigid estimator matches force-regulation → deformables are a hard case of rigid grasping.
2. **H2 — Dense tactile translates to control SR, not just discrimination, beating the vision-only solution.**
   - *Prediction*: dense tactile beats [[2510.25405|Stress-Guided RL]]'s vision-only (and sparse-tactile [[2602.10013|Force-Regulated Manipulation]]) on a *control* task by ≥10 pp SR on held-out deformables; if optimization bottlenecks it, the gain disappears.
   - *Test*: dense vs sparse vs vision-only on a deformable force-regulation task; report SR, not t-SNE separation.
   - *Row*: [[2510.25725|HumanoidVTA]] (dense-tactile discrimination) vs [[2510.25405|Stress-Guided RL]] (vision-only).
   - *Falsifier*: dense ties vision-only/sparse on control SR → the discriminative gap does not transfer to control.
3. **H3 — Differentiable soft-body physics beats model-free stress-RL on unseen deformables.**
   - *Prediction*: a differentiable MPM/soft-body twin ([[2511.04665|Real-to-Sim GS]], cross-ref [[Sim2Real|Sim2Real]]) used as the world model gives physics-grounded prediction that beats model-free [[2510.25405|Stress-Guided RL]] (which uses MPM only as a train-time oracle) on *held-out* soft objects.
   - *Test*: model-based (differentiable twin) vs model-free stress-RL on held-out soft objects.
   - *Row*: [[2510.21447|PhysWorld-Deformable]] (deformable world model) vs [[2510.25405|Stress-Guided RL]] (model-free oracle).
   - *Falsifier*: model-based ties model-free → the soft-body model adds no value over reactive regulation.
4. **H4 — Contact-pressure is a usable fragile-object reward.**
   - *Prediction*: a pressure-bounded reward derived from [[2509.18830|DexSkin]]'s interpretable force preserves fragile-object integrity better than a success-only reward (couples to D4).
   - *Test*: train with vs without a pressure-bound term; report integrity + SR on fruit.
   - *Row*: [[2509.18830|DexSkin]] (interpretable force).
   - *Falsifier*: the pressure bound does not improve integrity over success-only → force is not the right reward channel.
5. **H5 — Folding-as-completion sidesteps the need for force-regulation on some tasks.**
   - *Prediction*: [[2606.04269|Instant-Fold]]'s task-completion framing reaches its 60.9% zero-shot on garments *without* dense tactile, marking the regime where deformable manipulation does not need force-regulation at all.
   - *Test*: compare task-completion (no tactile) vs force-regulation on folding; map where each wins.
   - *Row*: [[2606.04269|Instant-Fold]] (task-completion).
   - *Falsifier*: task-completion fails without tactile → even folding needs force-regulation.

> [!warning] Risks
> - **No canonical success metric** — "did it grasp" is ill-defined for cloth. → Adopt task-completion (fold, pack) + force-bound (integrity) jointly, per [[2509.18830|DexSkin]]; do not report grasp-SR.
> - **Dense tactile optimization is unsolved** — [[2510.25725|HumanoidVTA]] shows dense barely beats sparse. → H2's dense-vs-sparse *control* test is the go/no-go; if it does not translate, the bet narrows to force-regulation without dense tactile.
> - **Soft-body sim is slow / inaccurate** — [[2302.04659|ManiSkill2]] runs soft-body at 80 FPS vs ~2000 FPS rigid. → Bound physics claims to validated twins (r > 0.9, [[2511.04665|Real-to-Sim GS]]); cross-ref [[Sim2Real|Sim2Real]].

---

## Cluster B — Contact-Rich Assembly & Precision

*Sub-millimeter contact — insertion, assembly, precision — where vision is blind to the contact state, the policy is open-loop, and the in-distribution benchmark is already saturated, so the bet moves onto the prediction delta and out-of-distribution transfer.*

### B1 — Predictive-Tactile Contact Imagination

| | |
|---|---|
| **Cluster** | B — Contact-Rich Assembly & Precision |
| **Thesis** | In contact, the next-step force is a deterministic consequence of the action, so a policy can forecast it and act *before* contact rather than react after. The field assumes reactive tactile feedback is enough — but force arrives too late to prevent a bad insertion. The bet is in First-principles below. |
| **Anchor papers** | [[2604.04974\|Video-to-Control Survey]] (survey), [[2511.02097\|WM Manipulation Survey]] (survey), [[2510.25725\|HumanoidVTA]] (benchmark), [[2512.23864\|DreamTacVLA]] (method), [[2603.19201\|OmniVTA]] (method) |
| **Key targets** | **Headline (prediction delta + OOD, where the absolute is saturated):** [[2512.23864\|DreamTacVLA]] +22.3% over its no-Dream ablation; [[2603.19201\|OmniVTA]] 60–63% SR *under perturbation* at 60 Hz. **Saturated in-distribution reference:** [[2512.23864\|DreamTacVLA]] 95.0% Peg-in-Hole / 85.7% USB / 81.1% Gear. **Consumed-force floor:** [[2505.22159\|ForceVLA]] +23.2 pp over π0-with-force |

**Why it matters.**
- **The gap**: the field consumes force as a *current* observation, but reactive feedback arrives only *after* contact — by the time bad force is felt, the misalignment has already happened, and three surveys name this unresolved ([[2604.04974|Video-to-Control Survey]], [[2511.02097|WM Manipulation Survey]] ranking physics 3rd of 13, [[2510.25725|HumanoidVTA]] on under-used discriminative tactile).
- **Today's answers**: predict-then-act is now *co-discovered consensus*, not contrarian — [[2602.06001|VT-WM]] fuses visuo-tactile latents *with actions* in a 12-layer AR Transformer and plans-in-imagination (35% real SR over vision-WMs), [[2603.23481|VTAM]] hits 90/85/95% via a visuo-tactile WAM, and the *root* [[1903.04128|Deep Tactile MPC]] forecast GelSight images for CEM planning back in 2019; meanwhile [[2505.22159|ForceVLA]] (+23.2 pp) / [[2601.20321|TaF-VLA]] (64.8%) only consume force.
- **The opening**: the existence proofs ([[2512.23864|DreamTacVLA]] 95.0% Peg-in-Hole, +22.3% no-Dream ablation; [[2603.19201|OmniVTA]] 60–63% under perturbation) show prediction adds a margin reaction cannot recover — but *none* run the controlled comparison that would prove *why*: a matched reactive-vs-predictive ablation on the delta, phase-stratified at contact-onset, with imagined-tactile substituting the absent sensor. That measurement is the unfilled slot.

**First-principles framing.**
- **First principle**: The next-step tactile signal is a deterministic consequence of the action given the contact state — it is forecastable. A policy that only reads current force is reactive by construction; one that *predicts* force can pick the action with the better imagined outcome before committing.
- **Assumption being challenged**: Not "reactive tactile suffices" (refuted) nor "an action-conditioned tactile WM helps" (now consensus — [[2602.06001|VT-WM]], [[2603.23481|VTAM]], [[1903.04128|Deep Tactile MPC]] all build one). The live wrong assumption is that the WM's gain is *uniform* and *sensor-bound*: if the gain is really concentrated at contact-onset and the *imagined* tactile can substitute the absent sensor, a predict-then-act policy beats a matched reactive one *at deployment with no tactile hardware* — the conjunction no predict-then-act paper has isolated.
- **The bet**: The world-model gain over a *matched* reactive policy is concentrated at contact-onset and survives sensor removal. (H1) ablating prediction at matched capacity yields [[2512.23864|DreamTacVLA]]'s +22.3% delta concentrated at onset steps, not flat; (H3) deploying with *imagined* tactile in place of the sensor recovers most of sensor-on SR on vision/action-correlated contact; under perturbation, [[2603.19201|OmniVTA]]-class 60 Hz holds 60–63% SR — not the saturated 95.0% absolute. Falsifiable: if a matched reactive policy ties the world-model policy on the delta *and* the gain is flat across phases, prediction adds nothing reaction cannot.

**Related research papers.**

The axis is *whether force is predicted or consumed* — and, for the predictors, the prediction target and control frequency:

| System | Force used as | Key result | What's missing |
|---|---|---|---|
| [[2512.23864\|DreamTacVLA]] | predicted future (tactile world model in a Think–Dream–Act loop) | 95.0% Peg-in-Hole, 85.7% USB, 81.1% Gear, +22.3% over no-Dream ablation | the contact-imagination anchor; tactile-data hungry, single platform |
| [[2603.19201\|OmniVTA]] | predicted + reflexive (visuo-tactile WM + 60 Hz controller) | 60–63% under perturbation, 21K-trajectory OmniViTac dataset | predictive + reflexive, but horizon-vs-frequency trade unquantified |
| [[2602.06001\|VT-WM]] | predicted future (12-layer AR Transformer fusing visuo-tactile latents *with actions*, CEM plan-in-imagination) | 35% real-robot SR over V-WMs, 33%/29% Fréchet cut, 77% after 20-demo finetune | the action-conditioned tactile-WM root the bet rests on — but plans toward *goal tactile states*, never runs the matched reactive-vs-predictive **delta** with phase-stratified contact-onset isolation (H1), nor H3/H4 |
| [[2603.23481\|VTAM]] | predicted future (multi-view visuo-tactile diffusion WAM + virtual-force regularization) | 90% chip / 85% peel / 95% wipe (0%/10% w/o WM + force-reg) | predict-then-act co-discovered again; no reactive-baseline delta, no imagined-tactile-substitution test |
| [[2603.05687\|CGP]] | predicted (coupled robot-state + tactile trajectory → controller targets) | real-time, physically-consistent executable targets | contact-as-jointly-predicted-quantity; not yet an action-refinement loop |
| [[2606.08737\|Dream-Tac]] | predicted future (unified tactile world *action* model jointly forecasting vision + tactile + action) | 83.3% over 6 tasks (+31.6% over Cosmos-Policy), 2.9× train / 1.8× inference | the DreamTacVLA sibling that predicts action *with* the contact future; Contact-Aware Self-Attention amplifies sparse tactile, single platform |
| [[2606.11184\|TacForeSight]] | predicted future (wrist force/torque → short-horizon tactile latent, ~200 ms lead) | 79.0% nominal / 86.7% under perturbation, MSE 0.017 at 20 Hz | grounds the forecast in a *leading* force signal where Dream-Tac forecasts the joint future; tactile latent only, no action-imagination |
| [[1903.04128\|Deep Tactile MPC]] | predicted future (recurrent conv net forecasts GelSight image + CEM/MPC) — the 2019 root precedent | 86.6% die-rolling, 2.10 mm ball reposition, tactile-only | action-conditioned tactile prediction + planning since 2019 — the bet's mechanism is decade-old; goal-image MPC, no matched reactive-vs-predictive delta |
| [[2506.15953\|ViTacFormer]] | predicted future (ACT-CVAE + cross-attention + AR tactile-prediction head, curriculum) | ~50% over SOTA short-horizon, 11-stage hamburger 80% | autoregressive tactile head proves the predict-then-act gain; never isolates the delta vs a matched reactive policy or substitutes imagined tactile for the sensor |
| [[2505.22159\|ForceVLA]] | consumed (force-aware MoE, force as first-class modality) | 60.5% (+23.2 pp over π0-with-force), 90% under occlusion | the consumed-force ceiling to beat; reactive by construction |
| [[2601.20321\|TaF-VLA]] | consumed (tactile-force alignment, VQ-VAE, 10M pairs) | 64.8% (vs 37.1% vision-only), 60.3% cross-sensor | force grounded but consumed; the sensor-agnostic prediction *target* B1 could reuse |
| [[2506.14754\|Sparsh-X]] | consumed (multisensory tactile backbone, 1M contacts) | 90% plug-insertion | the sensor-agnostic prediction target, not itself predictive |
| [[2605.07308\|AT-VLA]] | consumed (adaptive contact-gated tactile injection on a pretrained VLA) | +17% from preserved knowledge, +11% from fast contact response, reliable when tactile absent | gated-fusion, not predicted — the absent-tactile robustness B1 wants to exceed |
| [[2606.09337\|TORL-VLA]] | consumed + *future-wrench reference* (wrench-aware MoE VLA, online RL refines actions) | full-task 12/30 → 28/30 real latch-box (beats TA-VLA, ForceVLA) | emits a future-wrench reference (a partial prediction) but refines reactively online; the bridge between consumed and Dream-Tac's full imagination |
| [[2603.12665\|TacVLA]] | consumed (contact-aware tactile fusion VLA) | 83.75% avg disassembly (vs π0.5 63.75%), 70% in-box vs 10% | consumed-tactile fusion, not predicted |
| [[2507.09160\|Tactile-VLA]] | consumed (unlocks VLA physical knowledge for tactile) | 90% Charger, force-adverb generalization (2.94 N vs 2.57 N), 80% zero-shot wiping | consumed-force reasoning, reactive |
| [[2503.08548\|TLA]] | consumed (tactile-language-action for assembly) | >85% on unseen clearances/peg shapes (+50%), 0.3–1.2 mm | tactile-conditioned but reactive |
| [[2503.02881\|RDP]] | consumed (slow-fast visual-tactile reactive diffusion) | +35% over DP, 0.8 vs 0.15 under perturbation, sub-mm | explicitly reactive, not predictive |
| [[2510.13324\|FARM]] | consumed (tactile-conditioned diffusion for force-aware control) | 100% screw-tightening, 95% static-force, W1 0.75 N | consumed-tactile diffusion |
| [[2509.19696\|Diffusion Impedance Learning]] | consumed (diffusion-based impedance) | contact-rich impedance regulation | impedance, not tactile prediction |
| [[2503.16806\|DyWA]] | predicted state (dynamics-adaptive world action model) | 82.2% / 75.0% seen/unseen object-state | predicts object state (non-prehensile), not tactile — the state-prediction analog |
| [[2502.05086\|REASSEMBLE]] | benchmark (NIST board, force-torque phase patterns) | insert hardest, DMP 70% insertion | the contact-dynamics ground truth, not a method |

**Hypotheses & tests.** The FP bet — predicting force beats consuming it where the absolute is saturated — decomposed:
1. **H1 — The world model adds its +22.3% concentrated at contact onset.**
   - *Prediction*: isolating [[2512.23864|DreamTacVLA]]'s Dream component (or [[2602.06001|VT-WM]]'s action-conditioned predictor) adds +22.3% over a matched reactive policy, with the gain concentrated at contact-onset steps (where pre-commitment matters), not uniformly — the phase-stratified delta VT-WM/VTAM never report.
   - *Test*: ablate Dream on/off at matched capacity; stratify the margin by phase (approach / onset / settled).
   - *Row*: [[2602.06001|VT-WM]] (action-conditioned WM, no delta reported) vs [[2512.23864|DreamTacVLA]] (predicted future).
   - *Falsifier*: a flat or near-zero margin across phases → the world model is not buying anticipation.
2. **H2 — There is an optimal forecast horizon below the reflexive frequency.**
   - *Prediction*: sweeping prediction horizon (1-step vs N-step) against [[2603.19201|OmniVTA]]'s 60 Hz control, anticipation peaks at a short horizon and degrades as prediction drift dominates past it.
   - *Test*: horizon sweep at fixed 60 Hz; report SR-vs-horizon.
   - *Row*: [[2603.19201|OmniVTA]] (predicted + reflexive).
   - *Falsifier*: SR is flat across horizons → horizon is not a live knob and 1-step suffices.
3. **H3 — Imagined tactile recovers sensor-on SR when the sensor is absent.**
   - *Prediction*: a policy trained with tactile but deployed using *imagined* tactile (a forecast in place of the sensor) recovers most of sensor-on SR on contact that is vision/action-correlated (couples to [[#E1 — Sensor-Free Force-Aware Policies|E1]]).
   - *Test*: deploy with sensor vs imagined-tactile; report the gap by contact type.
   - *Row*: [[2512.23864|DreamTacVLA]] (predicted future) vs [[2605.07308|AT-VLA]] (absent-tactile-robust baseline).
   - *Falsifier*: imagined tactile collapses vs sensor-on → the forecast cannot substitute for the sensor.
4. **H4 — A sensor-agnostic prediction target keeps the gain across sensors.**
   - *Prediction*: predicting [[2601.20321|TaF-VLA]]'s force-aligned latent (or [[2506.14754|Sparsh-X]]'s representation) instead of raw tactile keeps the +22.3% delta when the deployment sensor differs from training.
   - *Test*: train the world model to forecast the aligned latent; evaluate cross-sensor.
   - *Row*: [[2601.20321|TaF-VLA]] (sensor-agnostic target) and [[2506.14754|Sparsh-X]] (multisensory backbone).
   - *Falsifier*: the cross-sensor delta vanishes → the prediction target is sensor-specific.
5. **H5 — Action-conditioned tactile beats object-state prediction on contact-rich SR.**
   - *Prediction*: forecasting *tactile* ([[2512.23864|DreamTacVLA]]) beats forecasting *object state* ([[2503.16806|DyWA]]) on sub-millimeter insertion, because tactile is the latent the contact regulates while object-state is downstream.
   - *Test*: matched world-model policies, tactile-target vs state-target, on insertion.
   - *Row*: [[2512.23864|DreamTacVLA]] (tactile prediction) vs [[2503.16806|DyWA]] (state prediction).
   - *Falsifier*: state-prediction ties tactile-prediction on insertion → the prediction target does not matter.

> [!warning] Risks
> - **Prediction may plateau at the noise floor** — micro-slip is not in the action-conditioned model. → Bound the claim to vision/action-correlated contact; report where imagined tactile diverges from measured (H1's residual).
> - **World-model latency vs reflexive budget** — predicting tactile must fit the [[2603.19201|OmniVTA]] 60 Hz loop. → H2's horizon-vs-frequency ablation is the feasibility gate; cap the horizon to what runs in-budget.
> - **Sim tactile is non-standard** — a tactile world model needs tactile data at scale. → Use [[2603.19201|OmniVTA]]'s OmniViTac + [[2602.23253|SPARR]]-style real residual; cross-ref [[Sim2Real|Sim2Real]].

### B2 — Contact-Mode-Conditional Precision & Reversibility

| | |
|---|---|
| **Cluster** | B — Contact-Rich Assembly & Precision |
| **Thesis** | Contact physics is locally discontinuous — make/break, slip-stick, the friction-cone edge — so the dynamics are piecewise, but the field smooths over them by scaling one continuous policy. Knowing the contact *mode* also tells you whether a corrective retreat is safe. The bet is in First-principles below. |
| **Anchor papers** | [[2511.02097\|WM Manipulation Survey]] (survey), [[2604.04974\|Video-to-Control Survey]] (survey), [[2502.05086\|REASSEMBLE]] (benchmark), [[2602.23253\|SPARR]] (method), [[2407.16677\|ResiP]] (method) |
| **Key targets** | **Headline (unseen-task, where in-distribution is saturated):** [[2602.23253\|SPARR]] +74.5% relative SR / 36.5% cycle-time cut on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic); [[2407.16677\|ResiP]] perturbation drop only 12% (vs 19–26%). **Saturated in-distribution reference:** [[2602.23253\|SPARR]] 95–100% [[2407.08028\|AutoMate]]. **Force bound:** [[2602.23648\|FAVLA]] 80.8% at 7.7 N peak (Gear) |

**Why it matters.**
- **The gap**: [[2502.05086|REASSEMBLE]] shows "Insert is the hardest action … due to its multi-step nature and demand for precise alignment and force application," and that force-torque "reveals distinct patterns corresponding to action phases (free-space, contact, pushing, twisting)" — so the task *is* a sequence through discrete contact modes, yet most policies treat it as one continuous map.
- **Today's answers**: discrete-mode structure is now partly explored — [[2604.19677|MATCH]] switches *control law* (position-vs-force per dimension, supervised by a *binary* contact bit) for 97% SR / 0% peg-breaks, [[2603.08342|PhaForce]] schedules a soft *contact-phase belief* (86% over 5 tasks, 85% OOD), and [[2410.00841|Diffusion Contact Search]] A*-searches over *mode sequences* (+12–23% screwdriver turning) — but none expose a 5-state physical-mode latent that switches *dynamics*, nor a reversibility gate.
- **The opening**: with in-distribution [[2407.08028|AutoMate]] saturated, the headroom is on *unseen* transfer ([[2602.23253|SPARR]]'s +74.5% relative SR / 36.5% cycle-time cut on held-out [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic)) and on a **mode-derived reversibility** property — a `making` retreat is safe, an `in-contact` one may be wedged — that neither continuous nor binary-contact policies expose (MATCH has zero occurrences of "reversib" or "unseen-task").

**First-principles framing.**
- **First principle**: Contact dynamics jump at the boundaries — the friction-cone edge, the moment force spikes, the switch from stick to slip are all sudden changes, not smooth ones. The real dynamics come in distinct *physical* pieces (make/break/slip-stick), so the right latent is a physical-mode label that switches the *dynamics model*, not a binary contact bit that switches the *controller* — and only a physical-mode label tells you whether a corrective retreat is reversible.
- **Assumption being challenged**: Not "more capacity closes the gap" (refuted) nor "discrete modes help" (now partly settled — [[2604.19677|MATCH]] switches control law, [[2603.08342|PhaForce]] schedules a phase belief). The live wrong assumption is that a *binary* contact/free switch is enough: [[2604.19677|MATCH]] collapses contact to one bit and avoids breaks via *force control*, never modeling slip-stick/wedge or deriving a reversibility decision — exactly the 5-state physical structure [[2502.05086|REASSEMBLE]]'s phase-distinct force patterns show is real.
- **The bet**: A policy that reads a 5-state *physical* contact-mode latent ($c_t \in \{\text{free, making, in-contact, sliding, breaking}\}$) and switches *dynamics* per mode (a) transfers to *unseen* tasks beyond [[2604.19677|MATCH]]'s single-task in-distribution result — at [[2602.23253|SPARR]]'s +74.5% relative SR / 36.5% cycle-time cut on held-out [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic), below [[2602.23648|FAVLA]]'s 7.7 N peak — and (b) exposes a **mode-derived reversibility gate** that cuts wedge-failures a binary-contact or mode-blind policy cannot, with per-mode classification accuracy ≥ usable on REASSEMBLE phases. Falsifiable: if a binary-contact policy ([[2604.19677|MATCH]]-class) with equal capacity ties the 5-state one on unseen NIST *and* matches its wedge-failure rate, the physical-mode latent is redundant over a contact bit.

**Related research papers.**

The axis is *how contact discontinuity is handled* — explicit discrete mode, continuous residual, adaptive frequency, or smoothed-over:

| System | Discontinuity handling | Key result | What's missing |
|---|---|---|---|
| [[2602.23253\|SPARR]] | sim base + real residual (continuous) | 95–100% [[2407.08028\|AutoMate]], +74.5% relative SR / 36.5% cycle-time on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) | the assembly-SR ceiling; no discrete contact-mode |
| [[2407.16677\|ResiP]] | frozen BC + residual PPO (continuous) | peg-in-hole 5%→99%, 12% perturbation drop (vs 19–26%) | residual reactivity, continuous — no mode structure |
| [[2602.23648\|FAVLA]] | force-variance head gates action-expert frequency | 80.8%, peak force 7.7 N (Gear) / 9.9 N (Box) | adaptive frequency ≈ *implicit* mode-awareness, not explicit modes |
| [[2604.19677\|MATCH]] | **binary** contact bit gates position-vs-force *control law* per dimension (SSL-supervised) | 97.0% SR / 0.0% peg-breaks, +35% sim-to-real, ~30% less force | the closest threat — switches *controller* not dynamics, 2-way not 5-state, single-task in-distribution (no unseen transfer, no reversibility); B2's H1 baseline-to-beat |
| [[2603.08342\|PhaForce]] | soft contact-aware *phase* schedule (slow planner + fast residual) | 86% over 5 tasks (+40 pp), 85% OOD raised-board, 0.85 wipe score | phase as a soft belief, not a discrete dynamics-switching latent; no reversibility gate |
| [[2410.00841\|Diffusion Contact Search]] | A* search over discrete *contact-mode sequences* (diffusion predictor + optimizer) | +12% / +23% screwdriver rotation, 41% further on hardware | plans mode *sequences* offline, not a runtime per-step physical-mode latent; no reversibility decision |
| [[2603.15169\|ForceVLA2]] | hybrid force-position control switching | 66% avg | position/force switching, no discrete contact-mode latent |
| [[2502.05086\|REASSEMBLE]] | benchmark — phase-distinct force-torque patterns | insert hardest, 4,551 demos, 70% DMP insertion | the mode ground truth, not a mode-conditional policy |
| [[2603.05687\|CGP]] | predicts coupled state + tactile (continuous) | real-time controller targets | predicts contact evolution continuously, no discrete mode |
| [[2509.19696\|Diffusion Impedance Learning]] | continuous impedance regulation | compliant contact | continuous, no mode |
| [[2605.05172\|Q2RL]] | Q from BC for fast on-robot RL | 3.75× on peg/pipe in 1–2 hrs | the fine-tuning loop for mode-policies, not a mode model |
| [[2503.16806\|DyWA]] | FiLM on inferred physics (mode-adjacent adaptation) | 82.2% / 75.0% | adapts to physics but does not expose a discrete mode |
| [[2605.02600\|CoRAL]] | LLM-mediated online refinement in contact | +50% avg in unseen contact-rich (vs OpenVLA / π0.5) | LLM adaptation, no discrete mode |
| [[2505.18472\|ManiFeel]] | benchmark — visuotactile value of contact | tactile +26 pp peg / +17 pp search; +14 pp gear sim-to-real | the contact-rich tactile-value benchmark, not a method |
| [[2505.06451\|Adaptive Wiping]] | few-shot IL with force-torque (continuous) | 100% contact / 96% reference force across 40 unseen (vs 4% open-loop) | contact-force adaptation, continuous |
| [[2604.18161\|DDCG]] | detects contact/friction discontinuity, switches 0th/1st-order gradient estimators (differentiable sim) | robust across Friction/Wall/Tennis with one hyperparameter (c=0.3) | handles the discontinuity at the *gradient* level, not a policy-side mode latent — the optimization analog of B2's bet |
| [[2210.10765\|PAINT]] | learned *reversibility* classifier penalizing irreversible states (mode-blind) | 80 resets vs 3000+, O(log T) labels/trajectory | supplies the reversibility decision generically, but blind to the contact mode that makes a retreat (un)safe — the prior B2 grounds in $c_t$ |
| [[2603.12185\|ComFree-Sim]] | GPU-parallel analytical contact engine | ~3× faster, near-linear contact scaling, torsional/rolling friction | the contact-rich *simulation* substrate, upstream of the policy |

**Hypotheses & tests.** The FP bet — a 5-state *physical* mode latent beats a binary-contact / implicit policy on *unseen* transfer + supplies a reversibility gate — decomposed (H1 unseen-transfer and H3 reversibility carry the surviving novelty):
1. **H1 — A 5-state physical mode beats a binary-contact / implicit policy on unseen tasks.**
   - *Prediction*: predicting a categorical 5-state $c_t$ from force-torque ([[2502.05086|REASSEMBLE]]-supervised) and conditioning *dynamics* on it beats [[2604.19677|MATCH]]'s binary contact-bit controller-switch and [[2602.23648|FAVLA]]'s implicit frequency on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) — the held-out-task transfer MATCH never tests (single-task in-distribution only).
   - *Test*: 5-state mode-conditional vs MATCH (binary) vs FAVLA on held-out NIST; report SR and per-mode error.
   - *Row*: [[2604.19677|MATCH]] (binary contact bit) and [[2602.23648|FAVLA]] (implicit frequency).
   - *Falsifier*: the binary bit ties the 5-state latent on unseen NIST → a contact/free switch already captures what matters.
2. **H2 — Mode-gated physics losses improve sub-millimeter insertion.**
   - *Prediction*: applying Coulomb-friction dynamics only in `in-contact` and ballistic only in `free` beats a single dynamics head on sub-millimeter insertion, because each mode's loss is correct only in its region.
   - *Test*: mode-gated vs single-head dynamics; report insertion precision.
   - *Row*: [[2603.05687|CGP]] (continuous prediction) as the single-head baseline.
   - *Falsifier*: mode-gating does not beat the single head → the piecewise structure is not exploitable.
3. **H3 — The mode supplies a reversibility decision that cuts wedge-failures.**
   - *Prediction*: using the 5-state mode to gate corrective retreats (`making` reversible, `in-contact` possibly wedged) cuts wedge-failures on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer that a binary-contact ([[2604.19677|MATCH]], which avoids breaks via *force control*, not reversibility) or mode-blind policy cannot avoid.
   - *Test*: enable/disable mode-gated retreat; report wedge-failure rate on transfer.
   - *Row*: [[2604.19677|MATCH]] (avoids breaks by force control, no reversibility) and [[2602.23253|SPARR]] (the ceiling, mode-blind).
   - *Falsifier*: mode-gated retreat does not reduce failures → reversibility is not mode-derivable in practice.
4. **H4 — A per-mode residual beats a single residual.**
   - *Prediction*: a residual policy *per contact mode* combined with [[2602.23253|SPARR]] / [[2407.16677|ResiP]] beats a single residual on unseen-task SR, because the correction needed differs by mode.
   - *Test*: per-mode vs single residual on held-out NIST.
   - *Row*: [[2407.16677|ResiP]] (single continuous residual).
   - *Falsifier*: per-mode ties single residual → the residual does not need mode structure.
5. **H5 — Mode supervision is learnable from phase annotations + sim.**
   - *Prediction*: a mode classifier distilled from [[2502.05086|REASSEMBLE]]'s phase annotations + sim contact reaches usable mode-classification accuracy, enabling H1–H4 without dense real mode labels.
   - *Test*: train the classifier on REASSEMBLE + [[2603.12185|ComFree-Sim]] contact; report mode-classification accuracy before any policy gain.
   - *Row*: [[2502.05086|REASSEMBLE]] (phase ground truth) and [[2603.12185|ComFree-Sim]] (sim contact).
   - *Falsifier*: mode-classification accuracy is too low to condition on → the discrete latent is not observable enough to supervise.

> [!warning] Risks
> - **Discrete-latent optimization variance** — Gumbel-softmax / REINFORCE for $c_t$ is high-variance. → Anneal soft→hard; start continuous, harden over training (a stability path H5 reports before policy gains).
> - **Mode supervision needs ground truth** — real mode labels are scarce. → Distill from [[2502.05086|REASSEMBLE]]'s phase annotations + sim contact; report mode-classification accuracy first (H5 is the gate).
> - **Saturated headline** — [[2602.23253|SPARR]] is already 95–100% on [[2407.08028|AutoMate]]. → Show the win on *unseen* [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer + peak-force bound + reversibility, never on in-distribution SR.

---

## Cluster C — Bimanual & Dual-Arm Coordination

*Two-arm manipulation where the cross-arm coupling is non-factorizable and bimanual demonstration data is scarce — composing single-arm priors, generating data with coordination structure, and sensing the inter-arm force that vision cannot see.*

### C1 — Coordination-Native Bimanual Policies

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Two-arm value is non-additive — the cross-arm coupling carries the coordination — but each arm's *skill* is an abundant, transferable single-arm prior. The field assumes bimanual competence requires bimanual-scale pretraining. Only the coupling is bimanual-specific. The bet is in First-principles below. |
| **Anchor papers** | [[2604.05831\|BiCoord]] (benchmark), [[2407.07788\|BiGym]] (benchmark), [[2603.15469\|RoCo Challenge]] (benchmark), [[2511.05275\|TwinVLA]] (method), [[2507.23523\|H-RDT]] (method) |
| **Key targets** | [[2511.05275\|TwinVLA]] 76% on ~50 episodes / ~25 H100-days (vs RDT-1B 45%, π0 80%); [[2604.05831\|BiCoord]] 4× spatial-temporal-integral + later-stage degradation; [[2507.23523\|H-RDT]] 41.6% few-shot (vs RDT 16.0%) + 87.2% RoboTwin 2.0 |

**Why it matters.**
- **The gap**: [[2604.05831|BiCoord]] quantifies the problem — a 4× spatial-temporal-integral increase, "policy performance consistently degraded in later stages of long-horizon tasks" — and [[2407.07788|BiGym]] shows IL/RL near-0% on stacking and long sequences. The composition-vs-monolith headline is now *settled*; what is unmapped is the coupling's *structure and breakdown*.
- **Today's answers**: composition-of-single-arm-priors is consensus — [[2511.05275|TwinVLA]] (76% / ~50 episodes via Joint-Attention), [[2603.20236|EnergyAction]] composes unimanual *energy functions* (86.4% RLBench2, +32.5% data-efficiency at 20 demos), [[2603.03836|SkillVLA]] recomposes per-arm skills (0%→51% on unseen left-right pairings), and [[2503.09186|Decoupled Bimanual]] already ran the H1 falsifier — decoupled-per-arm + interaction module beats integrated control by +23.5% at 1/6 the model size.
- **The opening**: with composition-beats-monolith settled across *different* coupling primitives (attention, energy, skill-recompose), the bet's contrarian content moves to the coupling itself — does the coupling's *data-floor* stay flat on 4×-harder tightly-coupled tasks, does *typed* coupling beat one attention layer, and does [[2604.05831|BiCoord]]'s later-stage degradation localize to the coupling (which a monolith cannot separate)?

**First-principles framing.**
- **First principle**: Two arms working together are worth more than the two arms scored separately — the coordination between them carries the extra value. But each arm's *skill* is just a single-arm policy, so the whole splits into a transferable single-arm skill and the two-arm coupling, and only that coupling needs two-arm data — which means the coupling has its own data-floor, type-structure, and failure mode, separable from the skill.
- **Assumption being challenged**: Not "bimanual needs bimanual-scale pretraining" (refuted) nor "composition matches a monolith" (now consensus — [[2511.05275|TwinVLA]], [[2603.20236|EnergyAction]], [[2603.03836|SkillVLA]], and [[2503.09186|Decoupled Bimanual]] all show it across different coupling primitives). The live wrong assumption is that the coupling is *structureless and cheap everywhere*: no paper has shown whether its data-floor stays flat on 4×-harder tasks, whether typed coupling beats one attention layer, or whether late-degradation is coupling- or skill-localized.
- **The bet**: The coupling has measurable structure and a localizable breakdown that composition exposes and a monolith cannot. (H2) the coupling's data-floor stays near [[2511.05275|TwinVLA]]'s ~50 episodes even on [[2604.05831|BiCoord]]'s 4×-harder tightly-coupled tasks; (H3) a [[2410.24185|DexMimicGen]]-typed (async/sync/ordered) coupling beats one Joint-Attention layer on tightly-coupled subtasks; (H4) [[2604.05831|BiCoord]]'s later-stage degradation localizes to the *coupling* (single-arm skill stays strong) — at composition's data-cost ([[2511.05275|TwinVLA]] 76% / ~25 H100-days). Falsifiable: if the coupling's data-floor rises sharply on harder tasks *and* typed coupling ties one layer, the coupling is unstructured and the composition story ends at the settled headline.

**Related research papers.**

The axis is *where bimanual competence comes from* — composed single-arm priors, transferred human priors, or monolithic two-arm pretraining (and what coupling mechanism each uses):

| System | Source of competence | Key result | What's missing |
|---|---|---|---|
| [[2511.05275\|TwinVLA]] | two single-arm policies + Joint-Attention coupling | 76% on ~50 episodes / ~25 H100-days (vs RDT-1B 45%, ≈π0 80%) | the composition anchor; causal-masked attention is one coupling design |
| [[2507.23523\|H-RDT]] | single-hand human-video prior → bimanual DiT (flow matching) | 41.6% few-shot (vs RDT 16.0%), 87.2% RoboTwin 2.0 | human-prior-to-bimanual transfer; coupling implicit in the DiT |
| [[2606.13279\|Dual-Level Bimanual VLA]] | Interaction-Aware Action MoE splitting generation into *coordinated* vs *arm-wise* pathways inside one VLA | +37% sim / +50% real "hard"-setting SR over monolithic (IAMoE +30% on interaction-dominant tasks) | the architectural cousin of TwinVLA's Joint-Attention — makes the coupling an explicit MoE branch, but within a monolith rather than composing single-arm priors |
| [[2603.20236\|EnergyAction]] | composes unimanual *energy functions* (flow-matching velocity field as −∇energy) + temporal-spatial coordination | 86.4% RLBench2 (13 tasks), +32.5% data-efficiency at 20 demos | confirms the factorization under a *different* coupling primitive — proving the thesis mechanism-independent (now consensus); never tests the coupling's data-floor on 4×-harder tasks (H2) or late-degradation localization (H4) |
| [[2603.03836\|SkillVLA]] | composes per-arm skills with an adaptive cooperation estimator (scalar α gates cross-attention) | 0%→51% on unseen left-right skill pairings, ~21% faster long-horizon, 5-demo new skills | recomposes single-arm skills (composition's strongest form); α is a single scalar, never a *typed* async/sync/ordered coupling (H3) |
| [[2503.09186\|Decoupled Bimanual]] | per-arm model + selective interaction module (scaling/bias modulation) | 78.9% RoboTwin (+23.5% over DP3) at 1/6 model size, +28% three-arm | already runs C1's H1 falsifier — decoupled-per-arm + interaction module beats integrated at 1/6 capacity; coupling left structureless, no breakdown analysis |
| [[2410.07864\|RDT-1B]] | monolithic two-arm diffusion foundation model | +56% over SOTA on real ALOHA, zero-shot to unseen objects | the monolithic baseline composition is measured against — needs the full two-arm data |
| [[2604.05831\|BiCoord]] | benchmark — long-horizon tightly-coupled coordination | 4× spatial-temporal integral, MRD/ARD/SMT/SMP/STI, later-stage degradation | the coordination-quantification target, vision-only — not a method |
| [[2410.24185\|DexMimicGen]] | subtask taxonomy (async/sync/ordered) | 90% real humanoid | the coordination-*structure* substrate (feeds C2), not a policy |
| [[2606.02274\|Dexterity-BEV]] | 3D-aligned bimanual policy | 89.9% LIBERO (vs <10% 2D), Handover-Book 93.3% (vs X-VLA 70.0%), Fold-Mailer 76.7% | 3D-grounded coordination; not a composed-prior framing |
| [[2511.21264\|MPPI-Bimanual]] | sampling-based MPC for bimanual coordination | model-based coordination baseline | model-based, no learned single-arm prior |
| [[2512.24653\|RoboMIND 2.0]] | 310K bimanual/mobile trajectories + IQL | up to 1.0 multi-robot SR | a data + framework substrate, not a coupling model |
| [[2304.13705\|ALOHA]] | low-cost bimanual hardware + ACT | threading / Ziploc / insertion | the foundational bimanual imitation substrate, single-task scope |
| [[2603.15469\|RoCo Challenge]] | benchmark — collaborative assembly | end-to-end beats modular for recovery | coordination + Sim-to-Real Cliff, not a method |
| [[2407.07788\|BiGym]] | benchmark — 40 mobile bimanual tasks | ACT/DP up to 100% simple, 0% on long sequences | the long-horizon difficulty floor |

**Hypotheses & tests.** The FP bet — the coupling has structure + a localizable breakdown, beyond the settled composition-beats-monolith headline — decomposed (H2/H3/H4 carry the surviving novelty):
1. **H1 — Composed prior + explicit coupling beats a matched-data monolith (settled-background check).**
   - *Prediction*: [[2511.05275|TwinVLA]]'s cross-arm Joint Attention over two single-arm priors beats a monolithic policy at *matched* data on [[2604.05831|BiCoord]]'s SMT/SMP coordination metrics — the result [[2503.09186|Decoupled Bimanual]] already established (+23.5% at 1/6 size), re-run on BiCoord's coordination metrics as the floor H2–H4 build on.
   - *Test*: composition vs monolith at equal episodes; report SMT/SMP, not just SR.
   - *Row*: [[2503.09186|Decoupled Bimanual]] (H1 already run, +23.5% at 1/6 size) and [[2511.05275|TwinVLA]] (composed) vs [[2410.07864|RDT-1B]] (monolithic).
   - *Falsifier*: the matched-data monolith ties the composition → the skill is not separable from the coupling and the cluster's consensus is benchmark-fragile.
2. **H2 — The coupling term needs only ~50 episodes given strong priors.**
   - *Prediction*: with strong single-arm priors, the coupling reaches [[2511.05275|TwinVLA]]'s ~50-episode result even on [[2604.05831|BiCoord]]'s 4×-harder tasks, because only the coupling is being learned.
   - *Test*: sweep bimanual-episode count on BiCoord; find the coupling's data floor.
   - *Row*: [[2511.05275|TwinVLA]] (composed, ~50 episodes).
   - *Falsifier*: the floor rises sharply on harder tasks → the coupling is not cheap.
3. **H3 — Coordination-type-conditional coupling beats a single attention layer.**
   - *Prediction*: conditioning the coupling on [[2410.24185|DexMimicGen]]'s async/sync/ordered subtask type beats one Joint-Attention layer on tightly-coupled subtasks.
   - *Test*: typed-coupling vs single-layer attention; stratify by subtask type.
   - *Row*: [[2410.24185|DexMimicGen]] (coordination taxonomy) feeding [[2511.05275|TwinVLA]] (single-layer coupling).
   - *Falsifier*: typed coupling ties one layer → the coupling does not need type structure.
4. **H4 — Composition isolates whether late degradation is coupling or skill.**
   - *Prediction*: [[2604.05831|BiCoord]]'s later-stage degradation localizes to the *coupling* in a composed policy (single-arm skill stays strong), which a monolith cannot separate.
   - *Test*: freeze single-arm priors, vary only the coupling; measure where late-stage SR drops.
   - *Row*: [[2604.05831|BiCoord]] (later-stage degradation).
   - *Falsifier*: degradation tracks single-arm skill, not coupling → the failure is not coupling-localized.
5. **H5 — A 3D-aligned action space lifts the coupling further.**
   - *Prediction*: composing single-arm priors in [[2606.02274|Dexterity-BEV]]'s 3D-aligned space beats 2D composition on handover-style coupled tasks, because the inter-arm geometry is explicit.
   - *Test*: 3D-aligned vs 2D composition on Handover-Book / Fold-Mailer.
   - *Row*: [[2606.02274|Dexterity-BEV]] (3D-aligned).
   - *Falsifier*: 2D composition ties 3D → the coupling does not need 3D grounding.

> [!warning] Risks
> - **Composition may cap the coordination ceiling** — tightly-coupled tasks (handover + force balance) may exceed what composed priors reach. → Bound to loosely-to-moderately-coupled tasks; report the [[2604.05831|BiCoord]] coupling-tightness-vs-SR curve (H2's denominator).
> - **Joint Attention is one design** — [[2511.05275|TwinVLA]]'s causal-masked attention may not be optimal. → H3's typed-coupling ablation tests alternatives.
> - **Single-arm priors must be strong** — composition fails on weak base policies. → Validate base SR first; the bet assumes π0/RDT-class priors exist.

### C2 — Scalable Bimanual Data Generation with Coordination Structure

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Coordination structure — per-arm subtask decomposition plus ordering constraints — is what makes a few demos generalize to many configurations, not data volume. The field assumes bimanual data must be teleoperated at scale. The data wall is a missing-structure problem. The bet is in First-principles below. |
| **Anchor papers** | [[2506.18088\|RoboTwin 2.0]] (benchmark), [[2604.05831\|BiCoord]] (benchmark), [[2603.15469\|RoCo Challenge]] (benchmark), [[2410.24185\|DexMimicGen]] (method), [[2504.13059\|RoboTwin]] (method) |
| **Key targets** | [[2410.24185\|DexMimicGen]] 90% real (40 sim demos vs 0% from 4), 76.0% vs 0.7% Drawer-Cleanup; [[2506.18088\|RoboTwin 2.0]] +24.4% few-shot / +21.0% zero-shot, 71.3% auto-code SR; [[2504.13059\|RoboTwin]] 300 sim + 20 real ≈ 300 real |

**Why it matters.**
- **The gap**: [[2506.18088|RoboTwin 2.0]] names the dual-arm data wall, but structure-aware generation is now *settled* as the answer — the open question is whether the gain comes from the *coordination structure* or simply the *volume* the structure unlocks, an isolation no generator runs.
- **Today's answers**: the X-Gen paradigm is consensus and generalized one level up — [[2510.18316|MoMaGen]] writes a unified constrained-optimization framework that *subsumes* MimicGen/SkillMimicGen/DexMimicGen and deploys a policy from one demo (π0 60% real after pretrain); [[2410.24185|DexMimicGen]] (90% from 40 vs 0% from 4), [[2506.18088|RoboTwin 2.0]] (+24.4% few-shot), [[2512.09297|BiDemoSyn]] (86.7% ID / 66.7% OOD from one demo) and [[2604.03552|CRAFT]] (89.3% cross-embodiment via video diffusion) instantiate it across replay, code-gen, and generation.
- **The opening**: the SR numbers are *achieved*, not predicted — so the salvageable contrarian core is H1's controlled ablation: strip the coordination structure (raw SE(3) replay) and does the 90%-from-40 hold? [[2410.24185|DexMimicGen]] only reports +8–9% coordinated-skill gains and a 16.2% hand-position-removal drop — never a clean structure-vs-volume isolation, least of all on a *differentiable* generator ([[2505.04860|D-CODA]], [[2604.03552|CRAFT]]).

**First-principles framing.**
- **First principle**: Bimanual generalization comes from coordination structure, not sheer volume — break a task into per-arm subtasks with sync and ordering rules, and each demo can be re-placed at new object positions across many scenes. If the principle is true, *stripping* the structure (raw SE(3) replay at matched volume) must collapse the result; if the SR holds without it, the gain was volume all along.
- **Assumption being challenged**: Not "data must be teleoperated at scale" (refuted) nor "structure-aware generation works" (now consensus — [[2510.18316|MoMaGen]] subsumes the whole X-Gen family; [[2512.09297|BiDemoSyn]], [[2604.03552|CRAFT]], [[2505.04860|D-CODA]] instantiate it). The live wrong assumption is that the achieved SR *proves* structure-carries-generalization: no paper isolates structure from the volume it produces, so the causal claim is asserted, not measured.
- **The bet**: Stripping coordination structure at matched volume collapses the result — the front-line *prediction*, not the achieved SR. (H1) raw SE(3) replay at the same trajectory count drops [[2410.24185|DexMimicGen]]'s 90%-from-40 by ≥30 pp, with the cleanest isolation on a *differentiable* generator ([[2505.04860|D-CODA]] / [[2604.03552|CRAFT]], whose Canny-conditioning ablation already shows 21.6% vs 10.3%); structured generation otherwise reaches [[2506.18088|RoboTwin 2.0]]'s +24.4% few-shot. Falsifiable: if raw SE(3) replay at matched volume keeps the 90% from 40 demos, the structure adds nothing volume could not, and the consensus result was a volume effect mislabeled as structure.

**Related research papers.**

The axis is *how the generator encodes coordination* — subtask taxonomy, MLLM code-gen, generative twin, or feasibility-filtered replay (and what each leaves under-covered):

| System | Coordination-generation mechanism | Key result | What's missing |
|---|---|---|---|
| [[2510.18316\|MoMaGen]] | unified constrained-optimization framework *subsuming* MimicGen/SkillMimicGen/DexMimicGen, one-demo → deployable policy | 63% gen-success on D0, π0 60% real after pretrain + 40 real demos | the topThreat — generalizes structure-aware generation one level up (consensus), but never runs the strip-structure → raw-SE(3)-replay ablation (H1) |
| [[2410.24185\|DexMimicGen]] | subtask taxonomy (async/sync/ordered) replays demos in sim | 90% real humanoid from 40 demos (vs 0% from 4), 76.0% vs 0.7% Drawer-Cleanup | the structured-generation anchor; reports +8–9% coordinated-skill gains, 16.2% hand-position-removal drop — never a clean structure-vs-volume isolation |
| [[2506.18088\|RoboTwin 2.0]] | MLLM expert-code + sim-in-loop + 5-axis randomization + embodiment-aware grasp | +24.4% few-shot / +21.0% zero-shot, 71.3% auto-code | the quality-controlled generator; ~29% auto-code needs refinement |
| [[2604.03552\|CRAFT]] | **differentiable** — video-diffusion + Canny-edge control over replayed sim trajectories | 89.3% cross-embodiment (vs 2–6% baseline); Canny ablation 21.6% vs 10.3% | the differentiable generator where H1's structure-vs-volume isolation is cleanest; structure-causality ablation only on Canny, not coordination |
| [[2505.04860\|D-CODA]] | **differentiable** — conditional diffusion of viewpoint-consistent wrist images + constrained-action sampling | 77.3% Coordinated-Lift (vs 61.3% VISTA), 14/20 vs 0/20 real Lift-Drawer | differentiable coordination-constrained generation; constraint ablated, structure-vs-volume not isolated |
| [[2512.09297\|BiDemoSyn]] | one-demo decomposition into invariant primitives + variable execution blocks (collision-validated) | 86.7% ID / 66.7% OOD (EquiBot), ~5 s/sample, zero-shot cross-embodiment | structure carries OOD generalization in the real world from one demo — but volume effect not separated from structure |
| [[2504.13059\|RoboTwin]] | generative digital twin + LLM decomposition | 300 sim + 20 real ≈ 300 real, +40% dual-arm SR | the data-efficiency anchor; coupling fidelity to tight coordination unverified |
| [[2604.07335\|TAMEn]] | feasibility-aware acquisition + recovery data | 100% replay (vs 12–39%) | the executability *filter* for generated data (feeds C3) |
| [[2512.24653\|RoboMIND 2.0]] | 310K bimanual trajectories + 20K-traj digital twin (Isaac Sim) | cross-embodiment generation scale | scale, but no explicit coordination taxonomy |
| [[2507.00833\|HumanoidGen]] | auto data generation for humanoid manipulation | the bimanual-humanoid generation engine | humanoid-focused; coordination-structure ablation absent |
| [[2605.21710\|PGDG]] | physics-grounded recovery-behavior generation from one demo | sim 38%→93%, real zero-shot 35%→82%, lifts GR00T N1.6 | physics-validity where kinematic replay fails; recovery-specific |
| [[2511.17441\|RoboCOIN]] | hierarchical annotation + RTML quality filter | +23% GR00T-N1.5, complex-task 20%→70% | the quality-filtered collection pipeline, not a generator |
| [[2505.12748\|TeleOpBench]] | simulator-centric dual-arm teleop benchmark | four modalities, sim-real completion-time correlation | the data-collection *eval*, not a generation method |
| [[2403.19417\|OAKINK2]] | bimanual hands-object dataset + task decomposition | 627 seqs / 4.01M frames / 100 objects | the human bimanual-HOI data substrate |
| [[2204.13662\|ARCTIC]] | dexterous bimanual articulated-object dataset | pretraining +9.2% on rigid manipulation | the articulated bimanual-HOI substrate |
| [[2401.08399\|TACO]] | bimanual tool-action-object benchmark | compound generalization 86.15% → 44.00% | the bimanual tool-use generalization data |

**Hypotheses & tests.** The FP bet — coordination structure, not the volume it unlocks, causally carries generalization (the unrun isolation) — decomposed (H1 is the front-line falsifiable prediction):
1. **H1 — Coordination structure, not raw replay, causally carries the 90%-from-40 result.**
   - *Prediction*: stripping [[2410.24185|DexMimicGen]]'s sync/ordering constraints (raw SE(3) replay) at *matched* trajectory volume drops the 90%-from-40 result by ≥30 pp — cleanest on a differentiable generator ([[2604.03552|CRAFT]] / [[2505.04860|D-CODA]]) where the structure term can be toggled continuously, as CRAFT's Canny ablation (21.6% vs 10.3%) already hints.
   - *Test*: ablate the taxonomy at matched volume; compare structured vs raw-replay downstream SR, on both replay (DexMimicGen) and a differentiable generator.
   - *Row*: [[2604.03552|CRAFT]] (differentiable, partial ablation) and [[2410.24185|DexMimicGen]] (subtask taxonomy).
   - *Falsifier*: raw replay at matched volume holds 90% → the structure is redundant and the consensus result was a volume effect.
2. **H2 — MLLM code-gen captures tight coupling better than demo-replay.**
   - *Prediction*: [[2506.18088|RoboTwin 2.0]]'s MLLM expert-code captures *coordinated* (not merely parallel) trajectories better than [[2410.24185|DexMimicGen]]'s demo-replay on tightly-coupled tasks.
   - *Test*: code-gen vs replay on tight-coupling subtasks; compare downstream coordination SR.
   - *Row*: [[2506.18088|RoboTwin 2.0]] (MLLM code) vs [[2410.24185|DexMimicGen]] (replay).
   - *Falsifier*: replay ties code-gen on tight coupling → the generation mechanism does not matter for coupling.
3. **H3 — Feasibility filtering raises downstream SR.**
   - *Prediction*: applying [[2604.07335|TAMEn]]'s online feasibility validation to generated dual-arm data (filtering unexecutable coordinations) raises downstream SR over unfiltered generation.
   - *Test*: filtered vs unfiltered generated data, same downstream policy.
   - *Row*: [[2604.07335|TAMEn]] (feasibility filter).
   - *Falsifier*: filtering does not raise SR → unexecutable coordinations are harmless to training.
4. **H4 — Generated data closes BiCoord's later-stage degradation.**
   - *Prediction*: training [[2511.05275|TwinVLA]] / [[2507.23523|H-RDT]] on structure-generated data closes [[2604.05831|BiCoord]]'s later-stage degradation more than training on raw-replay data.
   - *Test*: structured-generated vs raw-replay training; measure late-stage SR.
   - *Row*: [[2604.05831|BiCoord]] (later-stage degradation).
   - *Falsifier*: generated data under-represents tight coupling and late degradation persists → generation misses the coupling.
5. **H5 — Physics-grounded generation beats kinematic replay where contact matters.**
   - *Prediction*: [[2605.21710|PGDG]]'s physics-grounded recovery generation beats kinematic replay on contact-coupled bimanual, because kinematic replay produces physically-invalid contact.
   - *Test*: physics-grounded vs kinematic-replay generation on contact-rich bimanual; report real zero-shot SR.
   - *Row*: [[2605.21710|PGDG]] (physics-grounded) vs [[2410.24185|DexMimicGen]] (kinematic replay).
   - *Falsifier*: kinematic replay ties physics-grounded → contact validity does not affect downstream SR.

> [!warning] Risks
> - **Generated data may miss tight coupling** — replay can produce parallel-but-not-coordinated trajectories. → H4's [[2604.05831|BiCoord]] test is the gate; couple generation to C1's coupling-aware training.
> - **Sim-to-Real Cliff** — [[2603.15469|RoCo Challenge]] shows sim policies are brittle in real. → Use [[2506.18088|RoboTwin 2.0]]'s 5-axis randomization + [[2604.07335|TAMEn]] filtering; cross-ref [[Sim2Real|Sim2Real]].
> - **MLLM code-gen reliability** — [[2506.18088|RoboTwin 2.0]]'s 71.3% auto-code means ~29% needs refinement. → Keep human-in-the-loop verification; report generation-yield, not just downstream SR.

### C3 — Tactile-Coupled Bimanual Cooperation

| | |
|---|---|
| **Cluster** | C — Bimanual & Dual-Arm Coordination |
| **Thesis** | Force-balanced cooperation — holding-while-manipulating, bimanual handover — needs inter-arm force observability vision cannot provide; the two arms sense each other through the object. The field treats bimanual coordination as a vision-and-proprioception problem. The bet is in First-principles below. |
| **Anchor papers** | [[2604.05831\|BiCoord]] (benchmark), [[2510.25725\|HumanoidVTA]] (benchmark), [[2504.03515\|Dexterous IL Survey]] (survey), [[2604.07335\|TAMEn]] (method), [[2604.20444\|VTouch++]] (method) |
| **Key targets** | [[2604.07335\|TAMEn]] 75% contact-rich bimanual + 100% replay (vs 12–39%); [[2604.20444\|VTouch++]] 120K episodes / 36M frames / 380 tasks synchronized vision+tactile+proprioception; [[2512.24653\|RoboMIND 2.0]] tactile improves contact-task SR (XR-1 gains) |

**Why it matters.**
- **The gap**: that *tactile beats vision* on contact-coupled bimanual is now demonstrated — [[2510.14930|VT-Refine]] shows synchronized per-arm tactile lets two arms coordinate 2 mm-clearance assembly where vision-only fails (~40% RL-finetune lift). The *unanswered* question is whether the inter-arm force needs a **shared** representation or a per-arm one, and whether force-*balance* should be an explicit objective.
- **Today's answers**: tactile-coupled bimanual works per-arm — [[2510.14930|VT-Refine]] (per-arm tactile fused into one policy, coordination *emergent*), [[2604.07335|TAMEn]] (closed-loop per-arm tactile + recovery, 75% SR), [[2602.13689|Symmetry-Aware VT Fusion]] (explicit force-balance loss, 96.59% insertion) — but VT-Refine's coordination is emergent with no shared force channel, and Symmetry-Aware's balance loss is for *two fingers of one gripper*, not two arms.
- **The opening**: [[2604.20444|VTouch++]]'s 120K synchronized episodes now make a *shared inter-arm* channel learnable — and no paper has compared a shared channel against per-arm fusion ([[2510.14930|VT-Refine]]/[[2604.07335|TAMEn]]) on holding-while-manipulating, nor lifted [[2602.13689|Symmetry-Aware VT Fusion]]'s force-balance loss from two fingers to two arms.

**First-principles framing.**
- **First principle**: When one arm holds and the other manipulates, the cooperation is governed by the force *each arm transmits to the other through the object* — a single shared quantity, not two independent per-arm forces. A per-arm fusion observes each arm's contact in isolation; only a shared representation captures the transmitted coupling, and only an explicit force-*balance* objective optimizes the quantity the task is actually about.
- **Assumption being challenged**: Not "bimanual is a vision-only problem" (refuted by [[2510.14930|VT-Refine]]) — that contrast is now near-consensus. The live wrong assumption is that *per-arm* tactile fusion is enough: [[2510.14930|VT-Refine]] fuses tactile per-arm with *emergent* coordination and no shared force channel, and [[2602.13689|Symmetry-Aware VT Fusion]]'s force-balance loss is a two-finger result never lifted to two arms — so whether the inter-arm force must be *shared* and *balanced* is untested.
- **The bet**: A *shared* inter-arm force channel beats per-arm fusion on holding-while-manipulating by ≥10 pp SR, and an explicit force-*balance* loss beats tactile-as-input on force-balanced handover. (H1) shared > per-arm ([[2510.14930|VT-Refine]]/[[2604.07335|TAMEn]]-class) on hold-and-manipulate; (H3) lifting [[2602.13689|Symmetry-Aware VT Fusion]]'s balance loss from two fingers to two arms beats tactile-as-input on handover; reaching [[2604.07335|TAMEn]]'s 75% contact-rich SR using [[2604.20444|VTouch++]]'s synchronized data. Falsifiable: if per-arm fusion ties the shared channel on holding-while-manipulating *and* the balance loss ties tactile-as-input on handover, neither sharing nor balance is the missing structure.

**Related research papers.**

The axis is *how inter-arm force is represented* — shared channel, per-arm fusion, dense-tactile substrate, or absent (and where each falls short for cooperation):

| System | Inter-arm force representation | Key result | What's missing |
|---|---|---|---|
| [[2604.07335\|TAMEn]] | closed-loop tactile engine + AR recovery (per-arm) | 75% SR, 100% replay (vs 12–39%), 100% object-tracking (vs 32–78%) | the contact-rich bimanual anchor; per-arm, not a *shared* channel |
| [[2510.14930\|VT-Refine]] | per-arm tactile fused into one policy (real-to-sim-to-real RL), coordination *emergent* | ~40% real lift over vision-only, up to 0.98 sim, 2 mm-clearance bimanual assembly | the topThreat — proves tactile > vision on contact-coupled bimanual (H2 now near-consensus), but coordination is emergent with *no shared inter-arm force channel* and no force-balance objective (H1/H3 open) |
| [[2602.13689\|Symmetry-Aware VT Fusion]] | explicit bilateral force-symmetry regularization loss (residual forces) | 96.59% insertion (vs 93.23% vision-only), straighter trajectories | takes C3's explicit force-balance-loss mechanism (H3) — but for *two fingers of one gripper*, never lifted to two arms |
| [[2604.20444\|VTouch++]] | 120K-episode synchronized vision+tactile+proprioception | cross-modal R@1 2.16% vs 0.29%, real-robot MAE 0.022 | the bimanual tactile data substrate, no shared-channel policy |
| [[2606.11743\|TacCoRL]] | tactile injected into a pretrained VLA via a sim-to-real pipeline — dual-path tactile fusion + contact-aware gate, RL post-trained on simulated near-failure states | real 50.0% → 72.5% (sim 40.5% → 78.5%) over 4 bimanual contact-rich tasks where vision-only fails | per-arm contact correction, not a *shared* inter-arm-force channel; the sim-to-real route to the tactile data C3 wants (cross-ref [[Sim2Real\|Sim2Real]]) |
| [[2512.24653\|RoboMIND 2.0]] | 310K bimanual incl. tactile + MIND-2 dual-system | tactile improves contact-task SR (XR-1 gains) | tactile-bimanual at scale, but not an inter-arm-force objective |
| [[2510.25725\|HumanoidVTA]] | 2,124-sensor dense humanoid tactile | dense > sparse discrimination | the dense-tactile substrate; discrimination, not cooperation |
| [[2602.19764\|Multi-Sensory Sparse Experts]] | RGB+depth+6-axis-force fusion (DeMUSE) | 83.2% MT50, 80 ms compliance | the fusion substrate for two-arm force; not bimanual-specific |
| [[2603.17851\|DexViTac]] | synchronized human visuo-tactile-kinematic demos | 85.8% avg, 248 demos/hr, pretraining ablation 83.3% → 43.3% | the synchronized visuo-tactile bimanual data |
| [[2605.13083\|TouchAnything]] | multi-view egocentric + dense tactile | bimanual tactile data (20 hr) | a data source, not a cooperation policy |
| [[2603.05687\|CGP]] | multi-point contact-grounded policy (coupled state+tactile) | per-hand real-time | per-hand, extensible to inter-arm but not yet shared |
| [[2603.06987\|Foundational WM]] | world model detects bimanual failures via uncertainty | +3.8% detection at ~20× fewer params | force-blind-failure *detection*, not force-aware control |
| [[2604.05831\|BiCoord]] | benchmark — vision-only bimanual | later-stage degradation on coupled tasks | the force-blindness diagnosis, no tactile channel |

**Hypotheses & tests.** The FP bet — a *shared* inter-arm channel + explicit force-*balance*, beyond the now-settled tactile-vs-vision contrast — decomposed (H1 shared-vs-per-arm and H3 balance-loss carry the surviving novelty):
1. **H1 — A shared channel beats per-arm fusion on holding-while-manipulating.**
   - *Prediction*: a *shared* inter-arm tactile representation beats [[2510.14930|VT-Refine]]/[[2604.07335|TAMEn]]-class per-arm fusion by ≥10 pp SR on holding-while-manipulating, because the cooperation depends on the force *each arm transmits to the other*, not each arm's force in isolation.
   - *Test*: shared vs per-arm tactile representation at matched data on a hold-and-manipulate task.
   - *Row*: [[2510.14930|VT-Refine]] (per-arm, emergent) and [[2604.07335|TAMEn]] (per-arm tactile) as the per-arm baselines.
   - *Falsifier*: per-arm fusion ties the shared channel → inter-arm sharing is unnecessary.
2. **H2 — Tactile arrests BiCoord's later-stage degradation on coupled subtasks (settled-background check).**
   - *Prediction*: adding [[2604.20444|VTouch++]] / [[2604.07335|TAMEn]] tactile to a [[2604.05831|BiCoord]] policy arrests the later-stage degradation specifically on contact-coupled subtasks, not on vision-only ones — the tactile-beats-vision contrast [[2510.14930|VT-Refine]] already settled on 2 mm-clearance assembly, re-run here as the floor H1/H3 build on.
   - *Test*: tactile on/off on BiCoord; measure late-stage SR by subtask contact-coupling.
   - *Row*: [[2510.14930|VT-Refine]] (tactile > vision, contact-coupled) and [[2604.05831|BiCoord]] (vision-only, later-stage degradation).
   - *Falsifier*: degradation persists with tactile → late-stage failure is not force-blindness.
3. **H3 — Explicit force-balance loss, lifted from two fingers to two arms, beats tactile-as-input on handover.**
   - *Prediction*: lifting [[2602.13689|Symmetry-Aware VT Fusion]]'s bilateral force-symmetry loss from two fingers to a two-*arm* inter-arm balance objective beats tactile-as-input on bimanual handover, where the balance is the task objective.
   - *Test*: inter-arm force-balance loss vs tactile-as-input on handover; report success + force-imbalance.
   - *Row*: [[2602.13689|Symmetry-Aware VT Fusion]] (two-finger balance loss) vs [[2604.07335|TAMEn]] (tactile-as-input).
   - *Falsifier*: explicit balance ties tactile-as-input → the channel suffices without an explicit objective.
4. **H4 — Tactile coupling beats vision-only Joint Attention.**
   - *Prediction*: adding the shared tactile channel to C1's [[2511.05275|TwinVLA]] beats vision-only Joint Attention on contact-coupled bimanual.
   - *Test*: TwinVLA with vs without the shared tactile channel on contact-coupled tasks.
   - *Row*: [[2604.20444|VTouch++]] (synchronized tactile) feeding [[2511.05275|TwinVLA]] (vision-only coupling).
   - *Falsifier*: tactile coupling ties vision-only → the coupling does not need force.
5. **H5 — A WM uncertainty signal flags force-blind failures the policy misses.**
   - *Prediction*: [[2603.06987|Foundational WM]]'s uncertainty detects force-blind bimanual failures that a vision-only policy does not anticipate, providing a cheap force-blindness monitor.
   - *Test*: compare WM-uncertainty failure detection vs policy confidence on force-coupled failures.
   - *Row*: [[2603.06987|Foundational WM]] (force-blind-failure detection).
   - *Falsifier*: WM uncertainty does not beat policy confidence → force-blindness is not detectable from the WM.

> [!warning] Risks
> - **Inter-arm tactile is hard to instrument** — both arms need synchronized tactile. → [[2604.20444|VTouch++]] / [[2604.07335|TAMEn]] data exist; bound to platforms with bimanual tactile, report the requirement.
> - **Dense tactile optimization is unsolved** — [[2510.25725|HumanoidVTA]] shows dense barely beats sparse. → Use [[2602.19764|Multi-Sensory Sparse Experts]]' AdaMN normalization to stop force being suppressed; report the gap.
> - **Force-balance reward can over-constrain** — penalizing imbalance may block legitimate asymmetric grasps. → H3 makes balance tunable; expose the balance-vs-flexibility trade-off.

---

## Cluster D — Dexterous & In-Hand Control

*Multi-fingered hands performing high-DoF, contact-discontinuous, sim-to-real-fragile manipulation — making control intent hand-agnostic, bridging tactile sim-to-real without a tactile simulator, unlocking emergent dexterity through exploration, and bounding contact force with a hard constraint.*

### D1 — Universal Cross-Morphology Hand Control

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | Dexterous *control intent* — which contacts to form, what in-hand motion to produce — is hand-agnostic; only the actuation that realizes it is hand-specific. The field trains a bespoke policy per hand on parallel-jaw-centric foundations. That per-hand cost follows from parameterizing by joint commands. The bet is in First-principles below. (D1 owns the in-hand *control cycle* after the grasp; A2 owns the *grasp* — distinct phases.) |
| **Anchor papers** | [[2504.03515\|Dexterous IL Survey]] (survey), [[2508.13073\|Large VLM-based VLA Survey]] (survey), [[2605.16257\|DexJoCo]] (benchmark), [[2512.13644\|DexWM]] (method), [[2603.22264\|UniDex]] (method) |
| **Key targets** | **Headline (control cycle, A2 cannot claim):** [[2512.13644\|DexWM]] zero-shot 72% Reach / 58% Grasp / 28% Place (vs DP 16% / 0% / 8%) + 83% real-world zero-shot grasp (Allegro). **Shared cross-morphology evidence (A2's headline):** [[2603.22264\|UniDex]] 81% progress + 60% / 40% zero-shot + 5.2× cost cut. **Scaling:** [[2602.19764\|Multi-Sensory Sparse Experts]] 83.2% MT50 (vs RDT-1B 77.9%) + 42.6% compute cut |

**Why it matters.**
- **The gap**: single-weight policies *already* transfer across hand morphologies — [[2407.15002|GET]] (Jul 2024) distills per-hand experts into one graph-aware policy that zero-shot generalizes in-hand rotation to 10 unseen hand configs, and [[2602.08278|DexFormer]] controls 32 unseen hand variants from a shared canonical finger-action space. The open question is *which parameterization* (explicit intent, implicit history, or graph structure) carries the **full reach→grasp→reorient→place cycle**, which no system unifies across distinct hands.
- **Today's answers**: the cross-hand parameterizations divide — [[2602.08278|DexFormer]] uses *implicit history-conditioning* over a canonical finger space (77.5% over 32 variants), [[2407.15002|GET]] uses *graph-structure joint-space* (explicitly rejecting unified action space), [[2603.22264|UniDex]]'s FAAS is *explicit intent* (81% progress, 60%/40% transfer), and [[2512.13644|DexWM]] hand-keypoint dynamics reach 83% zero-shot grasp — but each covers a *partial* phase (rotation, or grasp), not the full cycle.
- **The opening**: [[2512.13644|DexWM]]'s 72%/58%/28% reach/grasp/place zero-shot (vs DP 16%/0%/8%) is the only existence proof spanning the full *control cycle* — and [[2602.08278|DexFormer]]'s implicit-history success shows you may not even *need* an explicit intent space, which is exactly the parameterization head-to-head no one has run on the reorientation phase.

**First-principles framing.**
- **First principle**: Control intent (which fingers touch where, what in-hand motion to make) is a plan that does not depend on the hand; the joint torques that carry it out do. But *how that intent is parameterized* — explicit intent space, implicit history-conditioning, or graph structure — is itself an open choice, and the right one may differ across the reach/grasp/reorient/place phases of the control cycle.
- **Assumption being challenged**: Not "each hand needs a bespoke policy" (refuted) nor "intent-level control transfers" (now consensus — [[2602.08278|DexFormer]] states it verbatim, [[2407.15002|GET]] and [[2603.22264|UniDex]] both transfer). The live wrong assumption is that *explicit* intent (FAAS) is necessary: [[2602.08278|DexFormer]]'s *implicit* history-conditioning transfers without it, and [[2407.15002|GET]] transfers via *graph-joint-space* — so which parameterization carries the full cycle is genuinely open, especially at the reorientation phase.
- **The bet**: One backbone unifies the *full* reach→grasp→reorient→place cycle across distinct hands (which [[2407.15002|GET]] cannot — it is in-hand rotation across configs of *one* hand; [[2512.13644|DexWM]] spans the cycle but on one hand family), and at the reorientation phase explicit-intent (FAAS), implicit-history ([[2602.08278|DexFormer]]), and graph-structure ([[2407.15002|GET]]) parameterizations differ measurably — best matching [[2512.13644|DexWM]]'s 72%/58%/28% zero-shot and 83% real grasp, 5.2× cheaper than per-hand collection, at real-time latency ([[2602.19764|Multi-Sensory Sparse Experts]] 42.6% compute cut). Falsifiable: if a joint-space/graph policy ([[2407.15002|GET]]-class) with equal data matches the cycle transfer on an unseen *distinct* hand, intent is not the invariant; if the three parameterizations tie at reorientation, the choice does not matter.

**Related research papers.**

The axis is *what the cross-hand policy is parameterized by* — control intent, hand-keypoint dynamics, sparse-MoE capacity, or joint commands (and the data source):

| System | Cross-hand parameterization | Key result | What's missing |
|---|---|---|---|
| [[2512.13644\|DexWM]] | hand-keypoint latent world model from human video + MPC | zero-shot 72% / 58% / 28% reach/grasp/place, 83% real grasp (Allegro), +34% PCK | the control-cycle anchor; keypoint dynamics, single backbone |
| [[2603.22264\|UniDex]] | Function-Actuator-Aligned Space + 3D policy from ego video | 81% progress, zero-shot 60% / 40%, 5.2× cost cut | the shared cross-morphology evidence (A2's headline), not the *control cycle* |
| [[2602.19764\|Multi-Sensory Sparse Experts]] | sparse-MoE multi-sensory DiT (DeMUSE) | 83.2% MT50 (vs RDT-1B 77.9%), 42.6% compute cut, 80 ms compliance | scalable capacity without latency; not itself a cross-morphology interface |
| [[2505.21864\|DexUMI]] | relative-finger actions across hands | 86%, 3.2× efficiency | cross-hand control via exoskeleton, in-domain not zero-shot |
| [[2603.10158\|XL-VLA]] | frozen embodiment-invariant latent action space (multi-headed VAE) + per-hand encoders/decoders on a VLA backbone | 0.72 mean SR over 4 hands × 10 tasks (+40% over π0 0.32), never underperforms kinematic retargeting zero-shot | the VLA-native instantiation of intent-invariance — policy lives in the frozen latent, hand identity only selects the codec; single-backbone, fine-grained gains uneven |
| [[2603.00732\|UniHM]] | morphology-agnostic VQ-VAE tokenizer → shared latent + physics-guided optimization | 65% real "Grab" (seen), 61.40 MPJPE DexYCB-seen across hand setups | the VQ-VAE cousin of FAAS/XL-VLA; HOI-retargeted generation, lower real SR than control-cycle anchors |
| [[2407.15002\|GET]] | **graph-structure joint-space** (kinematic graph in self-attention, FK self-modeling) — explicitly *rejects* unified action space | +20% zero-shot on new graph/link-length, 99% of expert, 0.82 mm FK error | the topThreat *and* D1's own H1 falsifier baseline — but only across configs of *one* LEAP hand, in-hand rotation only, never the full reach/grasp/place cycle on a distinct hand |
| [[2602.08278\|DexFormer]] | **implicit history-conditioning** over a shared canonical finger-action space (5-step obs-action window) | 77.5% over 32 unseen hand variants (vs LSTM 58.72%), real LEAP w/ removed joints | confirms intent-transfer is consensus and shows you may not need *explicit* intent — but grasping-only, the parameterization head-to-head at reorientation unrun |
| [[2606.05699\|DexFuture]] | hierarchical future-*state* targeting for bimanual dexterous tools | 59.69% (≈90% of privileged 66.52%), 60 Hz, ~250× faster than action-conditioned WM | the future-state sibling of DexWM; bimanual-tool-specific |
| [[2602.16863\|SimToolReal]] | object-centric zero-shot tool manipulation | 98.0% Task Progress (vs 0–10.8% retargeting) across 24 tasks / 6 tool categories | object-centric cross-task transfer, not cross-*hand* |
| [[2507.05331\|LBM TRI]] | large behavior models for multitask dexterous | OOD benefit grows (10/16 sim vs 3/16 nominal), <30% sim / 15% real data | the multitask-dexterous scaling examination; not intent-parameterized |
| [[2604.24681\|MoT-HRA]] | human-intention priors from large-scale human demos | 66.1% SimplerEnv (+22.3 pp), 0.136 m ADE on Ego4D | the human-prior intent source for cross-hand control |
| [[2603.04531\|PTLD]] | privileged tactile latent distillation | +182% rotation | the deployable estimator the policy needs (feeds D2) |
| [[2512.24653\|RoboMIND 2.0]] | 310K trajectories, six embodiments | cross-embodiment data | a data substrate, not a cross-hand policy |
| [[2604.20689\|FingerEye]] | per-finger eye-in-hand perception | morphology-specific sensing | morphology-specific — the opposite of intent-invariant |
| [[2605.16257\|DexJoCo]] | joint-space multi-task (benchmark) | DP-T 50.4% → 20.0% under randomization | the negative-transfer floor intent-space must beat |

**Hypotheses & tests.** The FP bet — full-cycle unification + the parameterization head-to-head, beyond now-settled intent-transfer — decomposed (H1 the GET-graph falsifier and the cycle-unification carry the surviving novelty):
1. **H1 — Intent-space transfers the full cycle where graph-joint-space (GET-class) does not.**
   - *Prediction*: an explicit-intent ([[2603.22264|UniDex]] FAAS) or implicit-history ([[2602.08278|DexFormer]]) policy recovers 60%/40% zero-shot on the *full reach/grasp/place cycle* on a held-out *distinct* hand where [[2407.15002|GET]]'s graph-joint-space — which transfers in-hand rotation across configs of one hand — does not span the cycle or the cross-hand-model gap.
   - *Test*: intent/history vs graph-joint-space at matched data on a held-out distinct hand, scored on the full cycle (not rotation only).
   - *Row*: [[2603.22264|UniDex]] (intent) and [[2602.08278|DexFormer]] (implicit history) vs [[2407.15002|GET]] (graph-joint-space) / [[2605.16257|DexJoCo]] (joint-space, degrades).
   - *Falsifier*: GET-class graph-joint-space matches intent on the full-cycle distinct-hand transfer → intent is not the invariant.
2. **H2 — Hand-agnostic dynamics + per-hand actuation beats per-hand end-to-end.**
   - *Prediction*: using [[2512.13644|DexWM]]'s hand-keypoint model as cross-hand dynamics with a thin per-hand actuation head beats a per-hand end-to-end policy on the control cycle.
   - *Test*: shared keypoint-dynamics + per-hand head vs per-hand end-to-end on reach/grasp/place.
   - *Row*: [[2512.13644|DexWM]] (hand-keypoint dynamics).
   - *Falsifier*: per-hand end-to-end ties the shared dynamics → the dynamics is not hand-agnostic.
3. **H3 — Sparse-MoE routes per-hand and beats a dense cross-hand policy at equal latency.**
   - *Prediction*: [[2602.19764|Multi-Sensory Sparse Experts]]' MoE routes one expert per morphology and beats a dense cross-hand policy at equal inference latency.
   - *Test*: inspect routing by hand; compare MoE vs dense at matched latency.
   - *Row*: [[2602.19764|Multi-Sensory Sparse Experts]] (sparse-MoE).
   - *Falsifier*: routing is hand-agnostic or MoE ties dense → MoE does not solve cross-morphology scaling.
4. **H4 — Future-state targeting matches action-conditioned WM at a fraction of the cost.**
   - *Prediction*: [[2606.05699|DexFuture]]'s future-state targeting reaches ≈90% of a privileged action-conditioned world model on the control cycle at ~250× lower cost, making the cross-hand controller real-time.
   - *Test*: future-state vs action-conditioned WM on reach/grasp/place; report SR and latency.
   - *Row*: [[2606.05699|DexFuture]] (future-state) vs [[2512.13644|DexWM]] (action-conditioned).
   - *Falsifier*: future-state loses too much SR → the cheap target cannot carry the control cycle.
5. **H5 — Intent for the plan + a joint-residual for fine actuation beats either alone.**
   - *Prediction*: intent-space for the contact plan plus a small per-hand joint-residual for fine actuation beats pure intent-space and pure joint-space (couples to A2's grasp-establishment + residual split).
   - *Test*: intent-only vs joint-only vs intent+residual on fine in-hand tasks.
   - *Row*: [[2603.22264|UniDex]] (intent) + [[2505.21864|DexUMI]] (relative-finger actuation).
   - *Falsifier*: the residual does not help → intent-space already captures fine actuation.

> [!warning] Risks
> - **Intent-space loses fine dexterity** — the contact plan may discard joint-level precision. → H5's intent + joint-residual split; bound intent-space to contact-establishment.
> - **40–60% transfer is not deployment-ready** — [[2603.22264|UniDex]]'s Wuji 40%. → Frame as a few-shot seed; report the few-shot curve from the zero-shot baseline.
> - **MoE may not specialize by hand** — H3's routing assumption may fail. → Test routing-by-hand empirically before claiming MoE solves cross-morphology scaling.

### D2 — Tactile In-Hand Reorientation with Sim-to-Real

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | Tactile is only an interface to the privileged state — object pose and shape — it encodes, so a *real* privileged sensor can replace a *simulated* tactile sensor as the distillation target. The field assumes tactile sim-to-real requires accurate tactile simulation. The gap is self-imposed by insisting on simulating the sensor. The bet is in First-principles below. (D2 is the in-hand sibling of [[#E1 — Sensor-Free Force-Aware Policies\|E1]]'s Route-2 distillation, specialized to reorientation.) |
| **Anchor papers** | [[2504.03515\|Dexterous IL Survey]] (survey), [[2510.25725\|HumanoidVTA]] (benchmark), [[2605.16257\|DexJoCo]] (benchmark), [[2603.04531\|PTLD]] (method), [[2210.13702\|DeXtreme]] (method) |
| **Key targets** | [[2603.04531\|PTLD]] +182% rotation / +57% reorientation goals, robust to slip/mass/wrist; [[2210.13702\|DeXtreme]] 27.8 (VADR) vs 14.8 (manual DR) at 15 Hz; [[2604.11138\|ViserDex]] 37.6 consecutive, ~25 under adversarial lighting; [[2601.02778\|Force-Based Sim2Real]] 25.1 vs 1.1 (contact vs no-contact) |

**Why it matters.**
- **The gap**: that tactile sim-to-real can *avoid* simulating the sensor is now settled — [[2405.07391|AnyRotate]] (CoRL'24, two years before PTLD) does multi-axis gravity-invariant reorientation with *no tactile sim*, training the bridge on *real* tactile from an instrumented rig. The open question: which *privileged interface* the bridge should target — a contact-feature (AnyRotate) or the object-pose-state (PTLD)?
- **Today's answers**: two no-tactile-sim interfaces compete — [[2405.07391|AnyRotate]] distills a *contact-feature* representation (contact pose + force, real-data observation model), while [[2603.04531|PTLD]] distills the privileged *object-pose-state* oracle (+182% rotation / +57% goals); both beat tactile-sim pipelines like [[2601.02778|Force-Based Sim2Real]] (25.1 vs 1.1 contact-vs-no-contact), but neither runs the head-to-head.
- **The opening**: with the simulator-is-avoidable assumption settled by AnyRotate, the unfilled measurement is the clean interface-controlled comparison — object-pose-state vs contact-feature vs tactile-sim, same task, same perturbations — which neither AnyRotate nor PTLD ran.

**First-principles framing.**
- **First principle**: The hard part of tactile sim-to-real is the *simulator*, but tactile is only an interface — the policy needs the privileged *state* it encodes. *Which* privileged state matters: the object-pose-state (PTLD) is task-complete but harder to instrument; the contact-feature (AnyRotate) is cheaper but lossier. The interface choice, not the simulator, is the live variable.
- **Assumption being challenged**: Not "tactile sim-to-real needs accurate tactile simulation" — [[2405.07391|AnyRotate]] refuted that in 2024 by bridging with no tactile sim. The live wrong assumption is that the *contact-feature* interface AnyRotate distills is the only no-sim option: PTLD's object-pose-state interface is a distinct, untested alternative, and no paper has compared the two against a tactile-sim baseline.
- **The bet**: The privileged object-pose-state interface ([[2603.04531|PTLD]]) beats both the contact-feature interface ([[2405.07391|AnyRotate]]) and a tactile-sim pipeline ([[2601.02778|Force-Based Sim2Real]]) on the *same* reorientation task under matched perturbations — reaching PTLD's +182% rotation / +57% goals, [[2210.13702|DeXtreme]]'s 27.8-vs-14.8, and holding under [[2604.11138|ViserDex]]'s adversarial lighting (~25). Falsifiable two ways: if the contact-feature interface ties the object-pose-state one, the cheaper interface wins; if a tactile-sim pipeline matches either, the simulator was never the bottleneck.

**Related research papers.**

The axis is *how the sim-to-real gap for in-hand contact is bridged* — privileged-real distillation, no-tactile vision/proprioception, intermediate physics-grounded representation, or tactile-sim:

| System | Sim-to-real bridge | Key result | What's missing |
|---|---|---|---|
| [[2603.04531\|PTLD]] | no-tactile-sim, **object-pose-state** privileged interface → real-pair estimator | +182% rotation, +57% reorientation goals, slip/mass/wrist robust | the object-pose-state anchor; needs an instrumented real cell, never compared to a contact-feature interface |
| [[2405.07391\|AnyRotate]] | no-tactile-sim, **contact-feature** interface (contact pose + force, real-data observation model), CoRL'24 | zero-shot multi-axis gravity-invariant reorientation, emergent re-stabilization | the topThreat — establishes the no-tactile-sim route two years before PTLD, but distills a *contact-feature* (lossier) interface, never the object-pose-state, and runs no interface head-to-head |
| [[2210.13702\|DeXtreme]] | Vectorized Automatic Domain Randomization (no tactile) | 27.8 (VADR) vs 14.8 (manual DR), 15 Hz pose estimator | avoids tactile entirely — the sim-to-real reorientation baseline |
| [[2604.11138\|ViserDex]] | 3DGS-in-the-loop + pre-rasterization aug (monocular RGB) | 37.6 consecutive / ~25 (adversarial lighting), single-GPU | visual sim-to-real, no contact channel |
| [[2601.02778\|Force-Based Sim2Real]] | distance-field tactile sim + current-to-torque calibration | 25.1 vs 1.1 rotations (contact vs no-contact) | builds a tactile sim — the contact-value proof, the route PTLD avoids |
| [[2605.28812\|CoP Tactile]] | physics-grounded Center-of-Pressure contact representation | 0.78 peg-in-hole, emergent reorientation, OOD-pose robust | an *intermediate* representation; not yet a full reorientation policy |
| [[2606.11767\|Blind Dexterous Grasping]] | Real2Sim *binary-contact-event* calibration (onset/offset timing) + privileged-supervised tactile encoder | 27% real over 20 objects (LEAP, no vision/pose), sim seen 36.2% → 60.4% | bridges the gap at the binary contact-event level (vs PTLD's privileged-real) — cheap calibration, but grasping not reorientation |
| [[2509.18830\|DexSkin]] | conformable skin + pneumatic calibration | 19/20 perturbed, 5/20 → 14/20 cross-sensor transfer | the real-tactile-hardware reference; calibration, not distillation |
| [[2605.09789\|DRIS]] | domain-randomized instance set (belief propagation) | 68% reactive catching zero-shot | uncertainty-aware sim-to-real (couples to D3), not in-hand reorientation |
| [[2603.15257\|HapticVLA]] | sensor-free distillation (vision → tactile token) | 86.7% | the deployment twin (feeds [[#E1 — Sensor-Free Force-Aware Policies\|E1]] Route 2); not reorientation-specific |
| [[2602.19764\|Multi-Sensory Sparse Experts]] | multi-sensory fusion incl. force | 83.2% MT50 | the multi-sensory in-hand substrate, not a sim-to-real bridge |
| [[2502.20396\|Humanoid Sim2Real Dex]] | vision-based dexterous sim-to-real RL on humanoids | 80% box-lift / 62.3% grasp-reach, 60–80% zero-shot unseen across two hands | cross-embodiment vision sim-to-real; no tactile channel |

**Hypotheses & tests.** The FP bet — the object-pose-state interface beats the contact-feature interface and tactile-sim, beyond the now-settled simulator-is-avoidable claim — decomposed (H1 is the three-way interface comparison carrying the surviving novelty):
1. **H1 — Object-pose-state interface beats contact-feature *and* tactile-sim (three-way).**
   - *Prediction*: [[2603.04531|PTLD]]'s object-pose-state interface recovers or exceeds +182% rotation vs both [[2405.07391|AnyRotate]]'s contact-feature interface and a tactile-sim → real pipeline on the *same* task, because the pose-state is task-complete where the contact-feature is lossy and the sim is biased.
   - *Test*: object-pose-state vs contact-feature vs tactile-sim distillation, one reorientation task, matched perturbations.
   - *Row*: [[2603.04531|PTLD]] (object-pose-state) vs [[2405.07391|AnyRotate]] (contact-feature) vs [[2601.02778|Force-Based Sim2Real]] (tactile-sim).
   - *Falsifier*: the contact-feature interface ties the object-pose-state one → the cheaper interface wins; or tactile-sim matches either → the simulator was not the bottleneck.
2. **H2 — Tactile beats vision under slip; vision beats tactile under lighting.**
   - *Prediction*: comparing [[2603.04531|PTLD]] (tactile) vs [[2604.11138|ViserDex]] (monocular RGB 3DGS) under perturbation, tactile holds better under slip while vision holds better under lighting — a modality-vs-perturbation split, not a universal winner.
   - *Test*: both modalities across slip and lighting perturbations; report the split.
   - *Row*: [[2603.04531|PTLD]] (tactile) vs [[2604.11138|ViserDex]] (vision).
   - *Falsifier*: one modality dominates across all perturbations → there is a universal winner and the split is wrong.
3. **H3 — Cross-sensor calibration generalizes the PTLD estimator across tactile hardware.**
   - *Prediction*: [[2509.18830|DexSkin]]'s calibration (5/20 → 14/20 cross-sensor) generalizes the [[2603.04531|PTLD]] estimator across tactile hardware without re-collecting privileged pairs.
   - *Test*: transfer the PTLD estimator across skin instances via DexSkin calibration; report SR.
   - *Row*: [[2509.18830|DexSkin]] (cross-sensor calibration).
   - *Falsifier*: the estimator does not transfer → privileged-real distillation is sensor-specific.
4. **H4 — VADR + privileged-tactile beats either alone past 27.8 reorientations.**
   - *Prediction*: combining [[2210.13702|DeXtreme]]'s VADR with [[2603.04531|PTLD]]'s distillation beats either alone, pushing past 27.8 consecutive reorientations.
   - *Test*: VADR-only vs PTLD-only vs combined; report consecutive reorientations.
   - *Row*: [[2210.13702|DeXtreme]] (VADR) + [[2603.04531|PTLD]] (privileged-tactile).
   - *Falsifier*: the combination ties the better single method → randomization and tactile are redundant.
5. **H5 — A physics-grounded intermediate representation transfers more robustly than raw tactile.**
   - *Prediction*: [[2605.28812|CoP Tactile]]'s Center-of-Pressure representation degrades less under OOD object pose than a raw-tactile estimator, because the physics-grounded intermediate is sensor-detail-invariant.
   - *Test*: CoP vs raw-tactile estimator under OOD pose; report degradation.
   - *Row*: [[2605.28812|CoP Tactile]] (physics-grounded intermediate).
   - *Falsifier*: raw tactile ties CoP under OOD → the intermediate adds no robustness.

> [!warning] Risks
> - **Instrumented real cell needed** — [[2603.04531|PTLD]] requires a privileged-sensor real setup. → This is a one-time data-collection cost, not a deployment dependency; report the instrumentation requirement explicitly.
> - **Privileged-real distillation may not generalize beyond training objects** — the estimator is trained on instrumented objects. → Bound to the object distribution; H3 tests cross-hardware, and cross-ref [[Sim2Real|Sim2Real]] for the broader story.
> - **Tactile vs visual may be task-dependent** — H2 may show no universal winner. → Report the modality-vs-perturbation-type split (slip favors tactile, lighting favors vision), not a single number.

### D3 — Exploration-Driven Emergent Dexterity

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | Long-horizon exploration is gated by the *initial-state diversity* the agent sees, not by reward shaping — a behavior is discoverable only if its precursor states are visited. The field hand-crafts curricula and rewards per task, then throws compute at a fixed reset distribution that saturates. The bet is in First-principles below. |
| **Anchor papers** | [[2504.03515\|Dexterous IL Survey]] (survey), [[2605.16257\|DexJoCo]] (benchmark), [[2510.25725\|HumanoidVTA]] (benchmark), [[2603.15789\|OmniReset]] (method), [[2605.03363\|Hierarchical RL-QP Grasp]] (method) |
| **Key targets** | [[2603.15789\|OmniReset]] 25% real peg insertion (vs 4% demo-DP), emergent multi-phase from one reward; [[2605.03363\|Hierarchical RL-QP Grasp]] 81.4% sim (vs 13.2% end-to-end RL) + 22/26 unseen real; [[2605.09789\|DRIS]] 68% reactive catching zero-shot (vs 5% hand-crafted, 13% sim-trained) |

**Why it matters.**
- **The gap**: the reset-distribution-as-exploration-lever principle is *old* — [[1707.05300|Reverse Curriculum Generation]] (2017) made learning intractable tasks tractable "without reward shaping or demonstrations" by adapting the start-state distribution, and [[2405.03379|RFCL]] / [[2204.02041|Example-based Resets]] re-instantiate it. What is *un*done: demonstration-free, task-agnostic, *high-DoF* dexterity emerging multi-phase at scale, where [[2603.15789|OmniReset]] names the wall ("performance saturation despite increased compute").
- **Today's answers**: [[2603.15789|OmniReset]] is the high-DoF instantiation — systematically diverse resets (reaching, near-object, grasp, near-goal) with a *single task-agnostic reward* yield emergent multi-phase behaviors and 25% real peg insertion vs 4% demo-DP; [[2605.03363|Hierarchical RL-QP Grasp]] / [[2509.01044|Hierarchical Reactive Grasping]] (same MIT lab) decompose task-space RL from joint-space QP (81.4% vs 13.2%; 100% concave-object grasp); [[2605.09789|DRIS]] propagates uncertainty for 68% zero-shot catching.
- **The opening**: OmniReset's 25%-vs-4% with one task-agnostic reward is the existence proof that broadening the reset distribution unlocks *emergent multi-phase dexterity* the curriculum lineage produced only as curriculum-to-single-goal — emergence at high DoF is the new coverage phenomenon, not the principle itself.

**First-principles framing.**
- **First principle** *(credit the lineage)*: Exploration coverage is set by the initial-state distribution, not reward shaping — a behavior is discoverable only if its precursor states are visited. This is the [[1707.05300|Reverse Curriculum Generation]] (2017) / [[2405.03379|RFCL]] / [[2204.02041|Example-based Resets]] principle, *not* a fresh discovery; D3's novelty is its instantiation, not the principle.
- **Assumption being challenged**: Not "reset diversity matters" (consensus since 2017) but that the principle only yields *curriculum-to-single-goal* — the lineage produces a curriculum toward one task. The live wrong assumption is that high-DoF dexterity needs hand-crafted curricula/rewards: demonstration-free task-agnostic *diverse* resets ([[2603.15789|OmniReset]]) instead yield *emergent multi-phase* behavior at scale, which the curriculum lineage never demonstrated.
- **The bet**: At high DoF, demonstration-free task-agnostic diverse-reset RL yields *emergent multi-phase* dexterity (not curriculum-to-single-goal) transferring zero-shot at [[2603.15789|OmniReset]]'s 25% real (vs 4% demo-DP), and task-space/joint-space decomposition ([[2605.03363|Hierarchical RL-QP Grasp]] / [[2509.01044|Hierarchical Reactive Grasping]]) reaches 81.4% sim (vs 13.2% monolithic) with 22/26 unseen-object real. Falsifiable: if a fixed-reset policy with matched compute and a shaped reward matches diverse-reset *emergence at high DoF*, the lever is reward/compute after all, not reset diversity.

**Related research papers.**

The axis is *what unlocks the behavior* — reset diversity, task/joint decomposition, uncertainty propagation, or reward/curriculum engineering:

| System | Behavior-unlock lever | Key result | What's missing |
|---|---|---|---|
| [[2603.15789\|OmniReset]] | diverse simulator resets + large-scale PPO, one task-agnostic reward | emergent multi-phase, 25% real peg insertion (vs 4% demo-DP) | the reset-diversity anchor at high DoF; 25% real is a zero-shot floor |
| [[1707.05300\|Reverse Curriculum Generation]] | adapt start-state distribution, learn 'in reverse' from goal (2017) | solves key-insertion intractable for standard RL, "without reward shaping or demonstrations" | the FP *root* — but curriculum-to-single-goal on low-DoF arms, never emergent multi-phase high-DoF dexterity |
| [[2405.03379\|RFCL]] | per-demo reverse curriculum → forward curriculum (SAC + Q-ensemble) | only method non-zero on all 21 tasks, solves PegInsertionSide/PlugCharger from 1–5 demos | re-instantiates the reset-distribution lever; still demonstration-seeded and goal-directed, not task-agnostic emergence |
| [[2204.02041\|Example-based Resets]] | self-supervised reset agent from initial-state examples (no reward engineering) | matches/beats oracle dense-reset reward (19.51 vs 10.38), real UR3 85% | proves resets impose an implicit curriculum — the FP's autonomy half; low-DoF, no emergent multi-phase |
| [[2605.03363\|Hierarchical RL-QP Grasp]] | task-space RL planner + GPU-parallel joint-space QP | 81.4% sim (vs 13.2% end-to-end RL), 22/26 unseen real, zero-shot steerable | the decomposition anchor; safety enforcement (also D4) |
| [[2509.01044\|Hierarchical Reactive Grasping]] | task-space velocity-field guidance + joint-space QP (same MIT lab as the anchor) | 100% concave-object grasp (vs 30.7% linear), real-time reactive to pushes | the *uncited decomposition predecessor* of the anchor — H2's true baseline, not the anchor's sole-owner claim |
| [[2605.09789\|DRIS]] | domain-randomized instance set (particle belief propagation) | 68% reactive catching zero-shot (vs 5% hand-crafted, 13% sim-trained) | uncertainty-aware exploration; catching-specific |
| [[2210.13702\|DeXtreme]] | Vectorized Automatic Domain Randomization | 27.8 vs 14.8; breaks manual-DR saturation | automatic randomization as exploration breadth; vision-only |
| [[2601.02778\|Force-Based Sim2Real]] | asymmetric actor-critic PPO + randomized actuator | 25.1 rotations | large-scale RL sim-to-real, fixed reset distribution |
| [[2506.19212\|VLM Dexterous Scaffolding]] | off-the-shelf VLM coarse 3D keypoint/wrist scaffolds + task-agnostic RL | 81% over 8 sim tasks (vs 19% pre-recorded), 90% zero-shot real Allegro | reward-free emergent dexterity; relies on VLM scaffold quality |
| [[2410.21845\|HIL-SERL]] | human-in-the-loop sample-efficient real RL | sample-efficient real-world RL | the real-RL baseline emergent policies compete with |
| [[2605.05172\|Q2RL]] | Q from BC for fast on-robot RL | 3.75× on peg/pipe in 1–2 hrs | real-world RL refinement of emergent policies |
| [[2602.01789\|RFS]] | residual flow steering for dexterous RL | 0.861 sim avg (vs DPPO 0.178), 74% real grasp with 50 corrections | joint local+global modulation for real-world refinement |
| [[2605.30226\|BORA]] | offline RL + online residual adaptation for dexterous VLA | 86% overall / 70% unseen, 1–2 interventions per task | the offline-to-online dexterous refinement loop |
| [[2605.27114\|VR-DAgger]] | immersive-VR data + uncertainty-guided on-policy correction | 97% Drawer / 89% Valve-Hard, −40% supervision time | the uncertainty-guided dexterous data engine |
| [[2605.15157\|HandITL]] | interventional correction for dexterous VLA | 99.8% fewer gesture jumps, 87.5% fewer grasp failures | the seamless-correction dexterous loop |
| [[2605.16257\|DexJoCo]] | benchmark — 11-task dexterous | evaluation suite for emergent multi-task dexterity | a benchmark, not a method |

**Hypotheses & tests.** The FP bet — reset diversity, not reward shaping, gates emergent dexterity — decomposed:
1. **H1 — Task-agnostic reset diversity produces *emergent multi-phase* behavior the curriculum lineage does not.**
   - *Prediction*: fixing the reward task-agnostic and varying *only* reset diversity ([[2603.15789|OmniReset]]'s reaching/near-object/grasp/near-goal) produces emergent multi-phase behavior at high DoF, where the goal-directed curriculum lineage ([[1707.05300|Reverse Curriculum Generation]], [[2405.03379|RFCL]]) yields only curriculum-to-single-goal.
   - *Test*: sweep reset diversity at fixed task-agnostic reward; check for emergent phases vs a goal-directed reverse curriculum at matched compute.
   - *Row*: [[2603.15789|OmniReset]] (diverse resets, emergent) vs [[1707.05300|Reverse Curriculum Generation]] (goal-directed curriculum).
   - *Falsifier*: multi-phase behavior appears at a single/goal-directed reset distribution → diversity is not the lever for emergence.
2. **H2 — Decomposition recovers the 81.4%-vs-13.2% gap and transfers better.**
   - *Prediction*: task-RL + joint-QP decomposition beats end-to-end RL at matched compute (81.4% vs 13.2%) and transfers better to unseen objects — the structure [[2509.01044|Hierarchical Reactive Grasping]] established (100% concave grasp) and [[2605.03363|Hierarchical RL-QP Grasp]] inherits.
   - *Test*: decomposition vs end-to-end at matched compute; report sim SR + unseen-object transfer.
   - *Row*: [[2605.03363|Hierarchical RL-QP Grasp]] (decomposition) vs [[2509.01044|Hierarchical Reactive Grasping]] (the predecessor baseline).
   - *Falsifier*: end-to-end ties decomposition at matched compute → the gap is compute, not structure.
3. **H3 — Uncertainty propagation generalizes beyond catching.**
   - *Prediction*: [[2605.09789|DRIS]]'s instance-set belief propagation (68% vs 13%) generalizes from catching to in-hand reorientation under uncertainty.
   - *Test*: apply DRIS belief propagation to reorientation; report zero-shot SR.
   - *Row*: [[2605.09789|DRIS]] (uncertainty propagation).
   - *Falsifier*: it does not transfer to reorientation → the gain is catching-specific.
4. **H4 — Emergent behavior survives distillation and beats demo-cloning.**
   - *Prediction*: distilling the emergent RL policy into a deployable visuomotor policy preserves [[2603.15789|OmniReset]]'s 25% real and beats demo-cloning on the same task.
   - *Test*: distill emergent policy vs clone demos; compare real SR.
   - *Row*: [[2603.15789|OmniReset]] (emergent) vs demo-cloning baseline.
   - *Falsifier*: distillation loses the behavior or ties cloning → emergence does not survive deployment.
5. **H5 — A VLM scaffold replaces reset-design with off-the-shelf priors.**
   - *Prediction*: [[2506.19212|VLM Dexterous Scaffolding]]'s VLM keypoint/wrist scaffolds + task-agnostic RL reach 81% over 8 tasks without hand-designed resets *or* rewards, marking the regime where the scaffold substitutes for both.
   - *Test*: VLM-scaffold + task-agnostic RL vs hand-designed reset diversity; compare SR and design effort.
   - *Row*: [[2506.19212|VLM Dexterous Scaffolding]] (VLM scaffold).
   - *Falsifier*: the scaffold underperforms designed resets → reset design cannot be off-loaded to a VLM.

> [!warning] Risks
> - **Reset diversity may need task knowledge** — defining "near-object/near-goal" resets is itself a design choice. → H1 tests whether generic reset diversity suffices; report the reset-design effort vs reward-design effort it replaces.
> - **Sim-to-real for emergent policies is fragile** — [[2603.15789|OmniReset]]'s 25% real is low. → Frame as a zero-shot floor; couple to [[2605.09789|DRIS]] / [[2210.13702|DeXtreme]] randomization and [[2605.05172|Q2RL]] on-robot refinement to lift it.
> - **Emergent behaviors may be unsafe** — unconstrained exploration can produce damaging contacts. → Bound with D4's QP / force-safety; report contact-force statistics during emergent rollouts.

### D4 — Force-Safety-Constrained Dexterous Control

| | |
|---|---|
| **Cluster** | D — Dexterous & In-Hand Control |
| **Thesis** | Safety is a hard constraint on the contact-force state that must hold *every* step — a learned policy can only softly penalize violations, while a physics-based filter can guarantee them. The field hopes learned policies stay safe via reward penalties. A per-step constraint and an expected-reward objective are different things. The bet is in First-principles below. |
| **Anchor papers** | [[2504.03515\|Dexterous IL Survey]] (survey), [[2510.25725\|HumanoidVTA]] (benchmark), [[2605.16257\|DexJoCo]] (benchmark), [[2605.03363\|Hierarchical RL-QP Grasp]] (method), [[2509.18830\|DexSkin]] (method) |
| **Key targets** | [[2605.03363\|Hierarchical RL-QP Grasp]] 81.4% sim + 22/26 unseen real with QP-enforced collision/joint/velocity limits + zero-shot steerability; [[2602.19764\|Multi-Sensory Sparse Experts]] ~10 N stable force + 80 ms compliance; [[2509.18830\|DexSkin]] 90% pressure reduction to 1.53 kPa on fragile objects |

**Why it matters.**
- **The gap**: the *generic* hard-filter-beats-soft-penalty claim is now settled — [[2605.21811|Safe Steerable Geometric Policy]] (Stanford+TRI) hard-enforces collision/kinematic/force-*closure* via QP+pullback-CBF with zero-shot steerability (92.5% grasp, first model-based in-hand reorientation). The *unfilled* slot: bounding contact-force *magnitude* to a fragile-object tolerance as a hard projection over a *learned* policy — force-closure (grasp non-slip) is the opposite of a force ceiling.
- **Today's answers**: hard safety filters work — [[2605.21811|Safe Steerable Geometric Policy]] (force-closure ECBF + residual-action steering), [[2605.03363|Hierarchical RL-QP Grasp]] (QP enforces collision/joint/velocity limits, 81.4% vs 13.2%) — but neither bounds *gentle* force; the fragile-object force ceiling is handled only *softly* by [[2510.25405|Stress-Guided RL]] (stress-penalty reward) and [[2509.18830|DexSkin]] (pressure-bounded reward, 1.53 kPa).
- **The opening**: the QP result shows a policy *inside* a hard filter trains better (81.4% vs 13.2%); the unrun bet is whether a *fragile gentle-force* hard projection over a learned policy beats the soft-penalty ([[2510.25405|Stress-Guided RL]]) at matched SR — the one head-to-head the consensus hard-filter work skips.

**First-principles framing.**
- **First principle**: A *gentle*-force constraint (contact force ≤ a fragile-object tolerance, e.g. 1.53 kPa / ~10 N) is an *upper* bound that must hold every step — the opposite of force-*closure* (which pushes force toward the maximum needed to hold a grasp). An upper bound can be guaranteed only by a hard projection over the learned action, never by an expected-reward penalty.
- **Assumption being challenged**: Not "safety needs a hard filter" (now consensus — [[2605.21811|Safe Steerable Geometric Policy]] states the soft-vs-hard dichotomy verbatim; the [[2512.11908|Contact-Rich Safe Learning Survey]] catalogs CBF-QP filters as a mature sub-field). The live wrong assumption is that the existing hard filters cover *gentle* force: they enforce force-*closure* and collision, never a force-magnitude *ceiling* for fragile objects, which remains handled only by *soft* penalties ([[2510.25405|Stress-Guided RL]]).
- **The bet**: A fragile gentle-force *hard projection* over a learned dexterous policy bounds contact force below [[2509.18830|DexSkin]]'s 1.53 kPa / [[2602.19764|Multi-Sensory Sparse Experts]]' ~10 N with *zero* force-violation, and beats the soft-penalty [[2510.25405|Stress-Guided RL]] (36.5% stress cut) at *matched* SR — keeping [[2605.03363|Hierarchical RL-QP Grasp]]'s 81.4% (vs 13.2% unconstrained) and zero-shot steerability. Falsifiable: if a soft-penalty policy ([[2510.25405|Stress-Guided RL]]-class) matches the hard projection on *both* SR and force-violation rate at matched fragile-object integrity, the hard projection buys nothing over a penalty.

**Related research papers.**

The axis is *how safety is enforced* — hard QP/projection, force-stability fusion, pressure-bounded reward, or soft penalty:

| System | Safety enforcement | Key result | What's missing |
|---|---|---|---|
| [[2605.21811\|Safe Steerable Geometric Policy]] | pullback-CBF + two-stage QP, hard **force-closure** + collision/kinematic; residual-action steering | 92.5% grasp (20 objects), 94.4% 3-finger, first model-based in-hand reorient >360° | the topThreat — owns the *generic* hard-filter + steerability framing, but enforces force-*closure* (max grasp force), the opposite of a fragile force *ceiling*; 20 rigid objects, no kPa bound |
| [[2510.25405\|Stress-Guided RL]] | **soft** stress-penalized reward (R_stress) over a learned policy | 36.5% stress cut vs vanilla RL, zero-shot tofu, foam water-loss 41.9%→10.0% | the soft-penalty comparator the hard-projection bet must beat at matched SR — no per-step guarantee, force can spike between gradient updates |
| [[2512.11908\|Contact-Rich Safe Learning Survey]] | survey — CBF-QP filters / barrier action-projection / verifiable force bounds | catalogs the hard-filter sub-field as mature | shows the *generic* hard-filter framing is consensus — the reason D4 must re-aim at the fragile gentle-force ceiling specifically |
| [[2605.03363\|Hierarchical RL-QP Grasp]] | GPU-parallel QP, hard collision/joint/velocity limits | 81.4% sim (vs 13.2% end-to-end RL), 22/26 unseen real, zero-shot steerable | the hard-constraint anchor; no explicit fragile-object force bound |
| [[2602.19764\|Multi-Sensory Sparse Experts]] | multi-sensory DiT with 6-axis force (stability) | stable ~10 N, 80 ms compliance (vs baseline force surges) | the force-stability anchor; not a hard per-step guarantee |
| [[2509.18830\|DexSkin]] | pressure-bounded reward from interpretable force | 90% reduction to 1.53 kPa, 20%→60% fragile-fruit integrity | the fragile-object bound; reward-based, not guaranteed |
| [[2603.15257\|HapticVLA]] | safety-aware reward-weighted flow matching (soft) | 86.7%, +45 pp egg | soft safety, complementary to a hard QP |
| [[2509.19696\|Diffusion Impedance Learning]] | diffusion-based impedance (soft compliance) | compliant contact regulation | impedance as the soft-constraint mechanism |
| [[2601.02778\|Force-Based Sim2Real]] | fingertip-force + joint-torque rewards | force-adaptive grasping | force-reward design, not a hard filter |
| [[2605.05172\|Q2RL]] | auxiliary BC loss for safe on-robot RL | safer exploration, avoids robot faults | training-time safety, not a deployment guarantee |
| [[2605.09789\|DRIS]] | uncertainty propagation for robust control | 68% reactive catching | the uncertainty-aware safety substrate |

**Hypotheses & tests.** The FP bet — a fragile gentle-force *hard projection* over a learned policy beats the soft-penalty at matched SR (the generic hard-filter being already consensus) — decomposed (H1/H2 the soft-vs-hard fragile-force head-to-head carry the surviving novelty):
1. **H1 — The fragile gentle-force hard projection guarantees the ceiling *and* matches SR vs a soft penalty.**
   - *Prediction*: a hard force-magnitude projection over a learned policy drives force-violation to zero on fragile objects while matching [[2510.25405|Stress-Guided RL]]'s soft-penalty SR — the head-to-head no hard-filter paper runs (they enforce force-*closure*/collision, not a ceiling).
   - *Test*: hard-projection vs soft stress-penalty on the same fragile task; report violation rate and SR.
   - *Row*: [[2510.25405|Stress-Guided RL]] (soft penalty) vs a [[2605.03363|Hierarchical RL-QP Grasp]]-style hard projection.
   - *Falsifier*: the soft penalty ties the projection on *both* violation rate and SR → the hard ceiling is redundant over a penalty.
2. **H2 — Force-bound projection preserves fragile-object integrity better than penalty-training at matched SR.**
   - *Prediction*: projecting policy actions onto a force-bounded feasible set ([[2509.18830|DexSkin]]'s 1.53 kPa) preserves fragile-object integrity better than the soft-penalty-trained [[2510.25405|Stress-Guided RL]] at matched SR.
   - *Test*: projection vs soft penalty on fragile-fruit tasks; report integrity at matched SR.
   - *Row*: [[2510.25405|Stress-Guided RL]] (soft stress-penalty) and [[2509.18830|DexSkin]] (pressure-bounded reward) as the penalty baselines.
   - *Falsifier*: penalty-training matches projection on integrity → the projection adds nothing.
3. **H3 — The QP-filter is the enabler of zero-shot steerability.**
   - *Prediction*: [[2605.03363|Hierarchical RL-QP Grasp]]'s post-training speed-safety tuning moves the trade-off measurably without retraining, and removing the QP-filter removes the steerability.
   - *Test*: sweep the speed-safety knob with the QP-filter on/off; quantify the trade-off range.
   - *Row*: [[2605.03363|Hierarchical RL-QP Grasp]] (hard QP).
   - *Falsifier*: steerability survives without the filter → the QP is not the enabler.
4. **H4 — A safety filter makes emergent/transferred policies deployable without retraining.**
   - *Prediction*: wrapping D3's emergent or D1's transferred policy in the QP/force-bound filter makes unconstrained exploration/transfer deployable with no retraining.
   - *Test*: wrap an emergent policy in the filter; report deployability + violation rate.
   - *Row*: [[2605.03363|Hierarchical RL-QP Grasp]] (hard QP) over an emergent-policy input.
   - *Falsifier*: the filter blocks task-necessary force and SR collapses → the constraint over-restricts.
5. **H5 — Force-stability fusion bounds force without a QP where collision is not the issue.**
   - *Prediction*: [[2602.19764|Multi-Sensory Sparse Experts]]' 6-axis-force fusion holds ~10 N stable on force-bounded (non-collision) tasks where a full QP is unnecessary, giving a lighter-weight safety route.
   - *Test*: force-fusion vs QP on force-bounded tasks without collision risk; compare force stability + cost.
   - *Row*: [[2602.19764|Multi-Sensory Sparse Experts]] (force-stability fusion).
   - *Falsifier*: force-fusion cannot bound force without the QP → the hard filter is always required.

> [!warning] Risks
> - **QP clamping can hurt task SR** — [[2605.03363|Hierarchical RL-QP Grasp]] notes tracking errors from clamping infeasible velocities. → Report the safety-vs-SR trade-off; the filter should clamp rarely on feasible tasks.
> - **Force tolerances are object-specific** — 1.53 kPa for berries differs from rigid assembly. → Make the bound a per-object parameter (couples to A1's affordance / A3's deformable); do not use a single global force limit.
> - **Hard constraints may over-restrict emergent behavior** — D3's emergent dexterity might need transient high forces. → H4 tests the filter over emergent policies; tune the constraint to allow task-necessary force while blocking damage.

---

## Cluster E — Tactile Foundations & Data Substrates

*The foundation layer beneath force-aware manipulation that needs no runtime tactile hardware — getting force-awareness to deployment with the sensor dropped, and a cross-sensor representation that makes any such policy portable across the sensor ecosystem.*

### E1 — Sensor-Free Force-Aware Policies

| | |
|---|---|
| **Cluster** | E — Tactile Foundations & Data Substrates |
| **Thesis** | Tactile-awareness is a learned behavior grounded in force — the object moves *because* of force, so the awareness is separable from the sensor that taught it. The field assumes contact-competent policies need tactile hardware at deployment. The sensor is the teacher signal, not a runtime dependency. The bet is in First-principles below. (Two routes reach it: pretrain force-awareness from ego video, or distill a tactile teacher and drop the sensor.) |
| **Anchor papers** | [[2604.27621\|Robot Learning from Human Videos Survey]] (survey), [[2604.15395\|Foundation Models in Robotics Survey]] (survey), [[2510.24795\|Efficient VLA Survey]] (survey), [[2603.15257\|HapticVLA]] (method), [[2603.04531\|PTLD]] (method), [[2602.16710\|EgoScale]] (method) |
| **Key targets** | **Route 1 (ego-video pretraining, no tactile at any stage):** ≥80% of tactile-instrumented SR on [[2505.22159\|ForceVLA]] 5 tasks; [[2602.16710\|EgoScale]] +54% on 22-DoF dexterous. **Route 2 (teacher-distillation, sensor dropped at inference):** [[2603.15257\|HapticVLA]] 86.7% sensor-free + +45 pp on the egg vs [[2506.01844\|SmolVLA]]; [[2603.04531\|PTLD]] +182% rotation / +57% reorientation goals; [[2601.02778\|Force-Based Sim2Real]] 25.1 vs 1.1 in-hand rotations |

**Why it matters.**
- **The gap**: Route 2 (distill a tactile teacher, drop the sensor) is now *settled* — [[2602.02142|FD-VLA]] distils a force token from vision+state and at inference *beats* the with-sensor baseline (61.1% vs raw-force 38.9%), [[2510.14117|ViTacGen]] generates tactile from vision for 86% zero-shot visual-only deploy, and [[2603.15257|HapticVLA]] hits 86.7% sensor-free. The genuinely *unattacked* half is Route 1: a force-aware *full policy* pretrained from ego video alone, no force/tactile at any stage.
- **Today's answers**: every ego-video backbone *omits* the force objective — [[2602.16710|EgoScale]] (20,854-hr log-linear curve, +54% on 22-DoF dexterous), [[2507.15597|Being-H0]], [[2512.13644|DexWM]] all pretrain ego backbones with *no* force head; meanwhile Route 2's distillation crowd ([[2602.02142|FD-VLA]], [[2510.14117|ViTacGen]], [[2603.15257|HapticVLA]]) has settled the drop-the-sensor question from the instrumented end.
- **The opening**: force is *upstream* of vision in contact (the object moves *because* of force), so vision→force is a well-posed inverse — and no paper yet trains a force-*objective* policy from ego video alone, despite every backbone and benchmark ([[2505.22159|ForceVLA]]'s 5 tasks, [[2506.14754|Sparsh-X]] synthetic-tactile teacher) now existing to do it.

**First-principles framing.**
- **First principle**: Tactile-awareness is a learned behavior grounded in force — force is *upstream* of vision in contact (the object moves *because* of force), so vision→force is a well-posed inverse, and that behavior is *separable* from the sensor that supervised it. If true, the supervising signal can be removed not just at deployment (Route 2, settled) but *at every stage* — a force *objective* learnable from ego video that never touches a sensor (Route 1).
- **Assumption being challenged**: Not "policies need tactile hardware at deployment" (Route 2 refuted it — [[2602.02142|FD-VLA]] even beats the with-sensor baseline). The live wrong assumption is that force-awareness needs a tactile *teacher cell* at training: Route 2 still requires an instrumented teacher (FD-VLA's F/T rig, HapticVLA's tactile teacher), and *no* paper learns force-awareness from ego video alone — every ego backbone ([[2602.16710|EgoScale]], [[2507.15597|Being-H0]], [[2512.13644|DexWM]]) omits the force head.
- **The bet** *(Route 1 is the front-line falsifiable claim)*: A force-*objective* policy pretrained on ~20k hr of ego *video alone* — no force/tactile at any stage — reaches ≥80% of a tactile-instrumented policy's SR on [[2505.22159|ForceVLA]]'s 5 tasks, riding [[2602.16710|EgoScale]]'s curve to +54% on 22-DoF dexterous, *clearing the instrumented bar that the settled Route-2 distillers ([[2602.02142|FD-VLA]] 61.1%, [[2603.15257|HapticVLA]] 86.7%) already replicate as the parity baseline*. Falsifiable: if the ego-video-only force-objective policy cannot clear 80% of the instrumented baseline, force-awareness is not learnable without a teacher signal — and Route 2 was the only viable route.

**Related research papers.**

The axis is *where the force-competence is supplied and whether the sensor is present at runtime* — Route 1 (ego-video pretraining, no sensor ever), Route 2 (teacher-distillation, sensor dropped), or consumed (sensor required):

| System | Route / sensor status | Key result | What's missing |
|---|---|---|---|
| [[2602.02142\|FD-VLA]] | Route 2 — distil force token from vision+state (F/T teacher at train), drop sensor at inference | 61.1% sensor-free mean, *beats* raw-force input (38.9%) on 3 contact-rich tasks | the Route-2 result that *settles* drop-the-sensor (a distilled token > the sensor) — but needs an instrumented teacher cell, zero ego-video, no Route-1 contribution |
| [[2510.14117\|ViTacGen]] | Route 2 — generate tactile depth from vision (VT-Gen) → RL policy, sim-only train | 86% real mug-push (vs 10% vision-only), 75.2% unseen, zero-shot visual-only deploy | settles Route 2 from the generation end; still uses tactile (generated) in the loop, not an ego-video force objective |
| [[2603.15257\|HapticVLA]] | Route 2 — tactile teacher → sensor-free student (vision → tactile token) | 86.7% mean, +45 pp egg vs [[2506.01844\|SmolVLA]], 75% with sensor | the Route-2 anchor; in-distribution contact only |
| [[2603.04531\|PTLD]] | Route 2 — privileged-sensor oracle → real-pair estimator, no tactile sim | +182% rotation, +57% goals | the privileged-to-real anchor (shared with D2); needs an instrumented cell |
| [[2602.16710\|EgoScale]] | Route 1 — ego-video scaling law | 20,854-hr log-linear curve, +54% on 22-DoF dexterous | no force head — the exact gap Route 1 attacks |
| [[2605.13083\|TouchAnything]] | Route 1 — multi-view ego + dense tactile substrate | view dropout cuts ego-only drop −27.20% → −5.78% | the vision-to-tactile substrate, not a full policy |
| [[2601.02778\|Force-Based Sim2Real]] | Route 2 — distance-field tactile-sim teacher | 25.1 vs 1.1 in-hand rotations | the efficient tactile-sim teacher; tactile sim still built |
| [[2410.24090\|Sparsh]] / [[2506.14754\|Sparsh-X]] | representation both routes distill toward (SSL touch) | 500% plug-insertion gain (to 90% SR), 460k–1M unlabeled | per-sensor SSL; the encoder, not a sensor-free policy |
| [[2507.15597\|Being-H0]] / [[2605.00078\|Being-H0.7]] | Route 1 — ego backbone (UniHand, 150M pairs) | full policy pretraining on instruction-motion pairs | no force head — the Route-1 backbone awaiting a force objective |
| [[2605.29564\|VE2VF]] | Route 2, inverse-modality — vision teacher → vision-free student | 95.0% overall, 100% OOD where the teacher scores 0% | drops vision keeps force; the mirror-image distillation |
| [[2606.06194\|ActiveMimic]] | Route 1 — ego-video active-perception pretraining (27D action) | 90.1% Restocking, 79.0% under flashing light | no force head — a Route-1 substrate, not force-aware |
| [[2605.06747\|HumanNet]] | Route 1 — 1M-hour ego+exo corpus | 1,000 hr ego ≈ 100 hr real-robot; narrows to a 20,000-hr robot model | no force head — the Route-1 scaling substrate |
| [[2510.21571\|VITRA]] | Route 1 — unstructured video → 1M-episode VLA dataset | 1.2K real trajectories generalize to unseen objects | the in-the-wild data engine, no force channel |
| [[2503.13441\|PH2D]] | Route 1 — task-oriented VR ego demos (~3.02M frames) | ~100% relative OOD gain vs robot-only, ~5× faster collection | the cheap-demo substrate, no force head |
| [[2505.22566\|Universal Visuo-Tactile]] | Route 1 — vision-to-tactile semantic understanding (VTV-LLM) | 60.4% tactile reasoning (vs GPT-4o 28.0%), VTV150K dataset | semantic vision-to-tactile substrate Route 1 leans on, not a policy |
| [[2505.22159\|ForceVLA]] | consumed — uses real tactile | 60.5% (+23.2 pp), the instrumented baseline both routes target | requires the runtime sensor — the bar to clear at 80% |
| [[2601.20321\|TaF-VLA]] | consumed — tactile-force alignment | 64.8%, 60.3% cross-sensor | neither ego-predicted nor distilled-away; the consumed-force contrast |
| [[2509.07962\|TA-VLA]] | Route-2-adjacent — sensorless torque from motor current | charger 0/20 → 17/20 | a cheap no-sensor proxy; current-derived torque misses fine slip |
| [[2606.12406\|FACTR 2]] | Route-2-adjacent — sensorless external joint-torque estimation (NEXT inverse-dynamics) + contact-phase re-sampling (FIRST) | 0.547 Nm L1 (87.6% below FILIC), highest avg progress over 5 contact-rich tasks | a learned no-F/T-sensor proxy stronger than TA-VLA's motor-current torque; estimates external force, still not fine fingertip slip |

**Hypotheses & tests.** The FP bet — force-awareness is learnable from ego video alone (Route 1), beyond the now-settled drop-the-sensor distillation (Route 2) — decomposed (H1 the Route-1-clears-the-bar claim carries the surviving novelty):
1. **H1 — The ego-video-only Route 1 clears the instrumented bar that settled Route 2 already replicates.**
   - *Prediction*: a force-objective policy from ego video alone clears ≥80% of the instrumented baseline on [[2505.22159|ForceVLA]]'s 5 tasks, with its failures concentrated on vision-uncorrelated slip — distinct from Route 2's ([[2602.02142|FD-VLA]]) novel-object failures, which already clear the bar from the instrumented end.
   - *Test*: run the ego-video Route-1 policy and the settled Route-2 distiller against the *same* sensor-free target; characterize per-route failure by contact type.
   - *Row*: [[2602.16710|EgoScale]] (Route 1, no force head — the gap) vs [[2602.02142|FD-VLA]] (Route 2, settled, beats with-sensor).
   - *Falsifier*: Route 1 cannot clear 80% → force-awareness is not learnable without a teacher signal and only Route 2 is viable.
2. **H2 — Predicted tactile from ego video recovers real-tactile SR (Route 1).**
   - *Prediction*: extending [[2605.13083|TouchAnything]]'s view-dropout to [[2602.16710|EgoScale]] volume and generating synthetic tactile via a [[2506.14754|Sparsh-X]] teacher on a small instrumented fraction recovers real-tactile SR in a [[2505.22159|ForceVLA]]-style policy.
   - *Test*: predicted-tactile vs real-tactile SR on ForceVLA's 5 tasks.
   - *Row*: [[2605.13083|TouchAnything]] (vision-to-tactile substrate).
   - *Falsifier*: predicted tactile underperforms real → ego-video force-awareness has a hard floor.
3. **H3 — Tactile-token prediction transfers teacher competence as well as a world model (Route 2).**
   - *Prediction*: [[2603.15257|HapticVLA]]'s vision→tactile-token prediction transfers as much teacher competence as B1's world-model forecast (see [[#B1 — Predictive-Tactile Contact Imagination|B1]]).
   - *Test*: token-prediction vs world-model distillation from the same teacher; compare student SR.
   - *Row*: [[2603.15257|HapticVLA]] (token prediction).
   - *Falsifier*: one transfers far more → the distillation target matters and the cheaper one loses.
4. **H4 — Privileged-to-real distillation avoids the tactile sim-to-real gap on assembly (Route 2).**
   - *Prediction*: replicating [[2603.04531|PTLD]]'s no-tactile-sim distillation on assembly (vs in-hand) avoids the tactile sim-to-real gap on [[2407.08028|AutoMate]].
   - *Test*: privileged-real distillation on assembly; compare to a tactile-sim pipeline.
   - *Row*: [[2603.04531|PTLD]] (privileged-real).
   - *Falsifier*: the assembly gap persists → the privileged-real route is in-hand-specific.
5. **H5 — Ego-video force-awareness survives the human-to-robot embodiment gap (Route 1).**
   - *Prediction*: carrying ego-video force-awareness from a 22-DoF human hand onto a 1–7-DoF gripper, explicit ([[2507.15597|Being-H0]] MANO + GRQ-VAE) and keypoint ([[2512.22414|π0.5 + ego]]) projections retain more force-competence than a learned projection.
   - *Test*: compare projection types for cross-embodiment force transfer.
   - *Row*: [[2507.15597|Being-H0]] (explicit projection).
   - *Falsifier*: the embodiment gap erases the force-awareness regardless of projection → Route 1 cannot cross embodiments.

> [!warning] Risks
> - **Vision-to-tactile noise floor (Route 1)** — subtle slip needs fingertip pressure, not vision. → Bound the claim to vision-correlated force; report the floor explicitly (H1's Route-1 failure regime).
> - **Distillation gap on novel objects (Route 2)** — the student may fail where the teacher's tactile was load-bearing. → Bound to in-distribution contact; report the teacher-student gap per object class.
> - **Scaling / instrumentation cost** — Route 1's 20k+ hr is expensive; Route 2 needs an instrumented teacher cell. → For Route 1, use [[2506.14754|Sparsh-X]] as a synthetic-tactile teacher on a small fraction; for Route 2, treat the cell as a one-time cost.
> - **Sensorless torque is coarse / embodiment mismatch** — [[2509.07962|TA-VLA]]'s current-derived torque misses fine slip, and 22-DoF human vs 1–7-DoF grippers leaves an action-space gap. → H1 and H5 set which regimes each route owns.

### E2 — Cross-Sensor Tactile Foundation Models for Plug-And-Play Force-Aware Policies

| | |
|---|---|
| **Cluster** | E — Tactile Foundations & Data Substrates |
| **Thesis** | Force is a physical quantity whose representation differs across sensors only in measurement basis — and a force-grounded encoder ([[2602.01153\|UniForce]]) now *exists*, transferring zero-shot across vision-based and magnetic sensors. So the open question is no longer "can it transfer?" but the *scaling law*: how much held-out-policy-SR retention does training-sensor *diversity* buy, and is the ceiling fundamental? The bet is in First-principles below. |
| **Anchor papers** | [[2604.27621\|Robot Learning from Human Videos Survey]] (survey), [[2604.15395\|Foundation Models in Robotics Survey]] (survey), [[2604.16592\|Cognition WM Survey]] (survey), [[2602.01153\|UniForce]] (method), [[2506.14754\|Sparsh-X]] (method) |
| **Key targets** | ≥80% held-out-*policy*-SR retention under a *leave-one-sensor-out* (N−1) protocol as training-sensor diversity scales (current: [[2602.01153\|UniForce]] 90–120% retention but only with all 3 sensors seen jointly; [[2601.20321\|TaF-VLA]] 60.3% family-level ceiling) |

**Why it matters.**
- **The gap**: the force-grounded "DINOv2-for-touch" now *exists* — [[2602.01153|UniForce]] grounds a label-free latent in the physical force vector (z5↔Fz r=−0.74) and transfers zero-shot across vision-based *and* magnetic sensors. So the open question is no longer existence but the *scaling law*: under a strict leave-one-sensor-out protocol, how much deployable-policy-SR survives, and does training-sensor diversity raise the ceiling or is it fundamental?
- **Today's answers**: cross-sensor invariance is converging fast — [[2602.01153|UniForce]] lifts wiping policy-SR 20%→80% via zero-shot cross-*type* transfer, [[2502.19638|Sensor-Invariant Tactile]] hits 81.94% inter-sensor classification (+33 pp over ViT), [[2406.13640|Transferable Tactile Transformer]] gets +24% median classification and 25% higher insertion SR across 13 sensors — but all report *perception* accuracy or *single-task* SR with the encoder seeing all sensors *jointly*, never a leave-one-out *policy-SR retention curve*.
- **The opening**: the convergence is the positive signal that the problem matters — and it leaves exactly one un-asked mechanism question: train on N−1 sensors, hold one out *for the encoder*, sweep N, and measure deployable-policy-SR retention. UniForce's 90–120% retention is encouraging but its encoder saw all 3 sensors, so the *scaling* claim is unproven.

**First-principles framing.**
- **First principle**: Force is a *physical quantity*; a force-grounded encoder is invariant by construction — [[2602.01153|UniForce]] confirms the principle (force-equilibrium supervision, z5↔Fz r=−0.74). So invariance is *settled*; the live unknown is whether it *scales* — does adding training sensors monotonically raise held-out-policy-SR retention, or does a fundamental ceiling cap it regardless of diversity?
- **Assumption being challenged**: Not "cross-sensor transfer needs per-sensor data" (refuted by UniForce) nor "a force-grounded encoder exists" (it does). The live wrong assumption is that the *retention scaling law* is already known: every prior result ([[2602.01153|UniForce]], [[2502.19638|Sensor-Invariant Tactile]], [[2406.13640|Transferable Tactile Transformer]]) trains with the test sensor *seen*, or reports perception accuracy — none runs a strict encoder-held-out N−1 sweep against deployable policy-SR.
- **The bet**: Under a *leave-one-sensor-out* (N−1) protocol where the held-out sensor is unseen *by the encoder*, deployable-policy-SR retention rises with training-sensor *diversity* and clears ≥80% by a small N — beyond UniForce's 90–120% (which saw all 3 sensors) and the [[2601.20321|TaF-VLA]] 60.3% family-level ceiling. Falsifiable: if held-out-sensor *policy-SR* retention plateaus below 80% regardless of how many sensors the encoder trains on, the ceiling is fundamental (a visual-to-tactile floor), not data-limited — and cross-sensor deployment is bounded.

**Related research papers.**

The axis is *what the representation is grounded in* — a sensor-invariant force vector, multi-sensor SSL (in-set), per-sensor, or a single physical sensor (and how far each transfers):

| System | Representation grounding | Key result | What's missing |
|---|---|---|---|
| [[2602.01153\|UniForce]] | **force-equilibrium-supervised** latent force (CVAE inverse/forward dyn), spans vision-based + magnetic | z5↔Fz r=−0.74; wiping policy-SR 20%→80% zero-shot cross-*type*; beats T3/AnyTouch | the topThreat — *is* the force-grounded encoder the card said "does not yet exist", but its encoder sees all 3 sensors jointly, so the strict N−1 retention scaling law (H3) is unrun |
| [[2502.19638\|Sensor-Invariant Tactile]] | sensor-invariant rep (calibration images + synthetic 100-sensor pretrain, normal-map + contrastive) | 81.94% inter-sensor classification (+33 pp over ViT), 0.80 mm pose RMSE | strong cross-sensor *perception* invariance, but reports classification/pose accuracy, never deployable policy-SR under N−1 |
| [[2406.13640\|Transferable Tactile Transformer]] | shared trunk + per-sensor encoders/decoders over 13 sensors (FoTa, 3M images) | +24% median classification, 25% higher insertion SR, 53% over vision-only | the multi-sensor SSL backbone closest to a foundation encoder — per-sensor encoders, not a single force-invariant latent; no retention-vs-diversity sweep |
| [[2601.20321\|TaF-VLA]] | VQ-VAE force latent across sensor families | 60.3% cross-sensor | the cross-sensor ceiling; not deployment-ready, families not all sensors |
| [[2506.14754\|Sparsh-X]] | multisensory SSL (1M contacts) | within-set multi-sensor representation | multi-sensor SSL but not cross-sensor *invariant* — the in-set baseline |
| [[2410.24090\|Sparsh]] | SSL touch foundation (460k images) | MAE/DINO/JEPA touch encoder | per-sensor only — the negative of the bet |
| [[2603.15169\|ForceVLA2]] | cross-scale MoE + force prompts (per-sensor) | 66% avg SR, +48 pp over [[2410.24164\|π0]] | consumes per-sensor tactile; the converged architecture to make portable |
| [[2603.15257\|HapticVLA]] | distillation to a sensor-free student | 86.7% sensor-free | distills, does not represent invariantly — the deploy twin E2 serves |
| [[2605.14571\|MTNet]] | visuo-tactile alignment | CKA ~0.74 | an alignment *metric*, not a transferable encoder |
| [[2509.18830\|DexSkin]] | capacitive tactile sensor (294° coverage) + calibration | 5/20 → 14/20 cross-sensor transfer | single-sensor hardware; calibration, not a foundation encoder |
| [[2604.28156\|FlexiTac]] | $30 piezoresistive + Kelvin-Voigt sim-to-real | low-cost sensor with a sim-to-real protocol | single-sensor; the deployment-chain reference |
| [[2604.20689\|FingerEye]] | vision-tactile fingertip sensor | per-finger eye-in-hand sensing | single-sensor |
| [[2605.24642\|GFM-VLA Study]] | geometric foundation models × policy | Early Fusion +5.56 pp on G1 | the foundation-model-integration playbook E2 borrows for the tactile case |
| [[2606.04825\|HapTile]] | vision-tactile-language-action dataset | 1,726 demos / 38 tasks, peg-insert 0% → 90% V+T | the contact-grounded dataset a cross-sensor encoder trains on |
| [[2408.06506\|TacSL]] | visuotactile sensor simulation + learning library | 200× tactile-image / 428× force-field speedup, 91.4% sim-to-real peg-place | the visuotactile-sim substrate for cross-sensor data |
| [[2604.27367\|DOT-Sim]] | differentiable optical tactile sim + real-to-sim calibration | 90.48% zero-shot indenter / 96.55% tumor, PSNR 30.48 | the calibrated optical-tactile sim source |
| [[2512.04884\|Hoi!]] | force-grounded cross-view articulated-manipulation dataset | Sparsh force RMSE 3.86–4.11 N (exposes the cross-domain gap) | the force-grounded held-out benchmark |

**Hypotheses & tests.** The reframed bet — held-out-*policy*-SR retention scales with training-sensor diversity under a strict N−1 protocol — decomposed (H1 the retention scaling law is the front-line falsifier):
1. **H1 — Held-out-policy-SR retention rises monotonically with training-sensor diversity.**
   - *Prediction*: training [[2602.01153|UniForce]]'s force-equilibrium encoder on N−1 sensors (held-out sensor *unseen by the encoder*) and sweeping N, deployable policy-SR retention rises monotonically and clears ≥80% by a small N — the curve UniForce never ran (it saw all 3 sensors jointly).
   - *Test*: leave-one-sensor-out, sweep N, report *policy*-SR retention vs sensor count.
   - *Row*: [[2602.01153|UniForce]] (force-grounded, all-sensors-seen) vs [[2512.04884|Hoi!]] (force-grounded held-out benchmark).
   - *Falsifier*: retention plateaus below 80% regardless of N → the ceiling is fundamental (a visual-to-tactile floor), not data-limited.
2. **H2 — Policy-SR is the load-bearing metric, not perception accuracy.**
   - *Prediction*: a held-out sensor that clears [[2502.19638|Sensor-Invariant Tactile]]'s 81.94% inter-sensor *classification* still loses deployable *policy*-SR — perception invariance over-states task invariance, so the retention law must be measured on policy-SR.
   - *Test*: correlate held-out classification accuracy vs held-out policy-SR across sensors.
   - *Row*: [[2502.19638|Sensor-Invariant Tactile]] (perception accuracy) vs [[2602.01153|UniForce]] (policy-SR).
   - *Falsifier*: classification and policy-SR retention track tightly → perception accuracy is a valid proxy and the policy-SR protocol is unnecessary.
3. **H3 — A single force-invariant latent beats a per-sensor-encoder trunk on the held-out sensor.**
   - *Prediction*: [[2602.01153|UniForce]]'s single force-grounded latent retains more held-out policy-SR than [[2406.13640|Transferable Tactile Transformer]]'s per-sensor-encoder + shared-trunk design, because per-sensor encoders need the held-out sensor's encoder.
   - *Test*: single-latent vs per-sensor-encoder trunk on the held-out sensor at matched data.
   - *Row*: [[2602.01153|UniForce]] (single force latent) vs [[2406.13640|Transferable Tactile Transformer]] (per-sensor encoders).
   - *Falsifier*: the per-sensor-encoder trunk ties the single latent → the architectural choice does not drive retention.
4. **H4 — Foundation-model integration lessons transfer to the tactile case.**
   - *Prediction*: bolting the force-invariant encoder onto [[2603.15169|ForceVLA2]]'s Cross-Scale MoE, [[2605.24642|GFM-VLA Study]]'s Early-Fusion finding (+5.56 pp) transfers to the tactile-foundation case and lifts held-out policy-SR.
   - *Test*: early vs late fusion of the force-invariant encoder into ForceVLA2; compare held-out SR.
   - *Row*: [[2605.24642|GFM-VLA Study]] (integration playbook) into [[2603.15169|ForceVLA2]] (per-sensor architecture).
   - *Falsifier*: early fusion does not help → the geometric-FM lesson does not carry to tactile.
5. **H5 — Train-one-deploy-another holds along the full deployment chain.**
   - *Prediction*: training on one sensor and deploying on another (via [[2604.28156|FlexiTac]]'s Kelvin-Voigt sim-to-real protocol as reference) holds end-task policy-SR within the ≥80% retention bound on [[2606.04825|HapTile]].
   - *Test*: full train-one-deploy-another chain on [[2606.04825|HapTile]]; report end-task SR.
   - *Row*: [[2604.28156|FlexiTac]] (deployment-chain reference) and [[2606.04825|HapTile]] (contact-grounded dataset).
   - *Falsifier*: the chain loses too much SR → cross-sensor invariance does not survive deployment.

> [!warning] Risks
> - **Fundamental sensor incompatibility** — capacitive vs piezoresistive vs vision-tactile may require discarding task-relevant detail to be invariant. → Ground the representation to the physical force vector (H2) rather than raw output; report what detail is lost.
> - **Recursive data problem** — SSL needs many sensors' data, but data is missing *because* transfer is the bottleneck. → Bootstrap from [[2602.01153|UniForce]]'s force-equilibrium corpus and [[2506.14754|Sparsh-X]]'s multi-sensor set; treat new sensors as encoder-held-out, not training targets.
> - **Retention may plateau below 80% regardless of diversity** — the policy-SR ceiling could be a fundamental visual-to-tactile floor, not data-limited. → Run H1's N−1 *policy-SR* retention sweep first as a go/no-go; UniForce's 90–120% with all-sensors-seen does not settle the encoder-held-out case.

---

## Cross-Cutting Themes

> [!tip] Contact Is a First-Class Predicted Quantity, Not a Consumed Observation
> B1, B2, C3, and D2 all invert the force-as-input convention into force-as-modeled-quantity at four points in the stack: B1 predicts the tactile *future* ([[2512.23864|DreamTacVLA]] +22.3% over its no-Dream ablation), B2 makes contact *mode* a discrete predicted latent ([[2502.05086|REASSEMBLE]]'s phase-distinct patterns), C3 makes inter-arm *force* the bimanual coordination variable ([[2604.20444|VTouch++]]'s synchronized channel), and D2 distills *privileged* contact state into a deployable estimator ([[2603.04531|PTLD]] +182%). [[2603.05687|CGP]]'s coupled state+tactile prediction and [[2603.19201|OmniVTA]]'s world model are the shared mechanism — model the contact, don't just react to it.

> [!tip] The Privileged-to-Deployable Distillation Interface Is the Sim-to-Real Workhorse
> E1 (Route 2), D1, and D2 route competence through a teacher-student gap where the teacher has privileged access the student lacks: E1 turns a tactile teacher into a sensor-free student ([[2603.15257|HapticVLA]] 86.7%), D2 distills privileged object-pose oracles into real estimators *without tactile sim* ([[2603.04531|PTLD]] +182%), and D1 distills cross-morphology intent from privileged multi-hand training ([[2603.22264|UniDex]] 60%/40%). The non-obvious point: the *interface* (what privileged signal the teacher exposes) matters more than the policy — [[2603.04531|PTLD]]'s insight that a *real* privileged sensor beats a *simulated* tactile one reframes sim-to-real, and E1 and D1 inherit it. The deployment counterpart to [[Sim2Real|Sim2Real]]'s teacher-student threads.

> [!tip] Morphology-Invariant Structure Is the Lever for Cross-Hand Transfer
> A2 and D1 share a bet pixel-and-joint-space approaches miss: grasp *function* and control *intent* are low-dimensional morphology-invariants, while joint-space geometry is the hand-specific projection. A2 transfers the grasp ([[2603.22264|UniDex]]'s FAAS, [[2505.21864|DexUMI]]'s relative-finger actions), D1 transfers the in-hand control policy ([[2512.13644|DexWM]]'s hand-keypoint dynamics) — both succeed where [[2605.16257|DexJoCo]]'s joint-space multi-task training *degrades*. They are *separable* bets, not one stated twice: A2 owns the **grasp-establishment** phase (scored on grasp-transfer SR), D1 owns the **in-hand-control** phase after the grasp (scored on [[2512.13644|DexWM]]'s reach/grasp/place, which A2 cannot claim). A policy can transfer the grasp without the subsequent reorientation, so each phase needs a distinct invariant. The Hinton move: favor the representation the *task* makes invariant over the one the *hardware* imposes — a hand is a hand regardless of finger count.
>
> Composition over monolithic scale (C1's [[2511.05275|TwinVLA]]) is the same lever at the bimanual scale: the single-arm *skill* is the invariant, the cross-arm *coupling* the scarce specific term.

> [!tip] Exploration Breadth and Reset Diversity Beat Reward Engineering and Parameter Count
> D3, D4, and B2 converge that the lever for hard contact-rich behavior is *coverage and constraint structure*, not scale: D3's diverse resets break exploration saturation ([[2603.15789|OmniReset]] 25% real vs 4% demo-DP) where compute alone saturates, D4's hard QP/force constraint both guarantees safety and improves training ([[2605.03363|Hierarchical RL-QP Grasp]] 81.4% vs 13.2%), and B2's discrete contact-mode structure beats a bigger smooth policy at the friction-cone boundary. [[2210.13702|DeXtreme]]'s automatic-domain-randomization (27.8 vs 14.8) is the shared mechanism — engineer the *exploration distribution and constraint set*, not the reward or the parameter count.

> [!tip] The Integration Layer Is the Bottleneck — Structure Beats More Teleoperation
> C2, B2, and C1 confront the Sim-to-Real Cliff and bimanual data wall the surveys ([[2604.04974|Video-to-Control Survey]], [[2603.15469|RoCo Challenge]], [[2604.05831|BiCoord]]) name as central — and answer with structure, not raw data: C2 generates bimanual data with coordination structure ([[2410.24185|DexMimicGen]] 90% from 40 demos), B2 closes the assembly cliff with a real residual ([[2602.23253|SPARR]] 95–100% [[2407.08028|AutoMate]]), C1 sidesteps the data wall by composing single-arm priors ([[2511.05275|TwinVLA]] 76% on ~50 episodes). The shared insight: the hard part is connecting a prediction to dependable contact, and the fixes are structured generation + real residuals + composition — not more teleoperation. Cross-ref [[Sim2Real|Sim2Real]] for residual/real-to-sim and [[WAM|WAM]] for imagination-as-data.

> [!tip] Force Is a Foundation Modality With Its Own Scarcity, Not Just an In-Task Signal
> Clusters A–D consume tactile *inside* a phase — B1 predicts the contact future, C3 shares it across two arms, D2 reorients in-hand. Cluster E asks the upstream question: where does the competence come from before any task, and does it ride along to deployment? E1 and E2 are the two unsolved halves — E1 gets force-awareness to deployment with *no runtime tactile sensor* (pretraining from ego video where robot tactile is 4 orders short of [[2310.08864|OXE]], *or* distilling a tactile teacher into a sensor-free student), and E2 builds the sensor-invariant encoder ([[2304.07193|DINOv2]]-for-touch) that makes any force-aware policy portable. The coupling that makes E cross-cutting: E1's distillation route is the sensor-free deployment of B1/B2's training-time contact modeling, and E2's encoder is what E1's student and D2's estimator both inherit. [[2505.22159|ForceVLA]] / [[2603.15169|ForceVLA2]] / [[2603.15257|HapticVLA]] established the in-task architecture; E1 and E2 deploy it without per-platform tactile hardware, with [[2605.21429|roto 2.0]] the shared benchmark.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Task-affordance as the cross-*morphology* invariant + product-separable $Q$ (conditioning itself now settled) | A1 | [[2503.07360\|AffordDexGrasp]] (affordance *conditions* the generator, but per-task selection — not invariance/separability) + [[2604.11674\|AffordSim]] (79%/64% vs 15%/3% oracle target, no morphology-transfer test) |
| Discrete grasp-taxonomy vs continuous function-space as the cross-hand invariant (continuous transfer now settled) | A2 | [[2604.04138\|Sparse Taxonomy Grasp]] (discrete taxonomy→control, never tested as a *transfer* bottleneck) + [[2410.02479\|Cross-Embodiment DexGrasp]] (continuous eigengrasp transfer, no discrete comparator) |
| Dense-tactile + differentiable-soft-body beating vision-only stress-RL on *held-out* deformables (force-regulation now settled) | A3 | [[2510.25405\|Stress-Guided RL]] (vision-only stress-penalty, zero-shot tofu, no tactile + no soft-body model, in-distribution only) + [[2509.18830\|DexSkin]] (force-regulation, rigid skin not soft-body) |
| Tactile-*future* prediction (world model) vs reactive tactile on contact-rich SR | B1 | [[2512.23864\|DreamTacVLA]] (Think–Dream–Act, 95.0% Peg-in-Hole, single system) + [[2603.19201\|OmniVTA]] (visuo-tactile WM + 60 Hz reflexive) |
| 5-state *physical* contact-mode latent + reversibility on *unseen* insertion (binary control-switch now settled) | B2 | [[2604.19677\|MATCH]] (binary contact bit switches *controller*, 97% in-distribution, no 5-state/unseen/reversibility) + [[2602.23253\|SPARR]] (95–100% [[2407.08028\|AutoMate]], continuous, mode-blind) |
| Coupling *structure* + localizable breakdown on tightly-coupled tasks (composition-vs-monolith now settled) | C1 | [[2603.20236\|EnergyAction]] (composition under a *different* primitive — proves the thesis, no coupling data-floor/breakdown test) + [[2511.05275\|TwinVLA]] (composed single-arm, 76% on ~50 episodes) |
| Structure-vs-volume *isolation* (strip structure → does SR hold?) — generation itself now settled | C2 | [[2510.18316\|MoMaGen]] (subsumes the X-Gen family, one-demo→policy, no strip-structure ablation) + [[2410.24185\|DexMimicGen]] (90% from 40 demos, +8–9% coordinated-skill, never a clean structure-vs-volume isolation) |
| *Shared* inter-arm force channel + force-balance loss for two arms (tactile-vs-vision now settled) | C3 | [[2510.14930\|VT-Refine]] (per-arm tactile, *emergent* coordination, no shared channel) + [[2602.13689\|Symmetry-Aware VT Fusion]] (force-balance loss, but two fingers not two arms) |
| Full reach→grasp→reorient→place cycle across distinct hands + parameterization head-to-head (cross-hand transfer now settled) | D1 | [[2407.15002\|GET]] (graph-joint-space, one-hand configs, rotation only — D1's own falsifier) + [[2602.08278\|DexFormer]] (implicit-history transfer, grasping-only, no reorient head-to-head) |
| Three-way interface head-to-head: object-pose-state vs contact-feature vs tactile-sim (no-tactile-sim route now settled) | D2 | [[2405.07391\|AnyRotate]] (no-tactile-sim *contact-feature* interface, CoRL'24, no head-to-head) + [[2603.04531\|PTLD]] (no-tactile-sim *object-pose-state* interface, +182%, never compared to contact-feature) |
| *High-DoF emergent* multi-phase dexterity from task-agnostic reset-diversity (the reset-as-lever principle dates to 2017) | D3 | [[2603.15789\|OmniReset]] (diverse resets, 25% real peg, single reward — the high-DoF instantiation) + [[1707.05300\|Reverse Curriculum Generation]] (the FP root, but curriculum-to-single-goal, no emergence) |
| Fragile *gentle-force* hard projection over a *learned* policy, head-to-head vs soft-penalty (generic hard-filter now consensus) | D4 | [[2605.21811\|Safe Steerable Geometric Policy]] (hard force-*closure* + steerability, the *opposite* of a force ceiling, rigid objects) + [[2510.25405\|Stress-Guided RL]] (soft stress-penalty, 36.5% cut, no per-step guarantee) |
| Force-aware policy from ego *video alone* (Route 1), no teacher cell — teacher-distillation (Route 2) now settled | E1 | [[2602.02142\|FD-VLA]] (Route 2 settled — distilled token beats with-sensor, but needs an F/T teacher cell, no ego video) + [[2602.16710\|EgoScale]] (ego curve, *no force head* — the Route-1 gap) + [[2505.22159\|ForceVLA]] (instrumented bar to clear) |
| Held-out-*policy*-SR retention *scaling law* under leave-one-sensor-out N−1 (a force-grounded encoder now exists) | E2 | [[2602.01153\|UniForce]] (force-grounded zero-shot cross-*type*, 90–120% retention but encoder saw all 3 sensors — no N−1 sweep) + [[2601.20321\|TaF-VLA]] (60.3% family-level ceiling) |

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
- [[Locomotion|Locomotion]] — Sibling Locomotion subsystem; the legs whose balance the manipulation disturbs.
- [[Whole-Body|Whole-Body]] — Sibling Whole-Body subsystem; the loco-manipulation coupling that integrates these arms and hands with the legs.

> [!example] Humanoid reading path
> For a humanoid, this doc's **Bimanual (Cluster C)** + **Dexterous (Cluster D)** are the upper-body manipulation subsystem — two-arm coordination (C1–C3) and in-hand control (D1–D4). The **legs and locomotion** live in the [[Locomotion|Locomotion]] doc, and the **loco-manipulation coupling** (legs stabilizing the manipulation workspace, whole-body balance during reaching) in the [[Whole-Body|Whole-Body]] doc. Read C+D here for the upper body; the sibling docs for the lower body and the coupling.
