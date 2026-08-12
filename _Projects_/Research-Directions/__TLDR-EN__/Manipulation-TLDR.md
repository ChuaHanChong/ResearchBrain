---
title: "TL;DR: Manipulation, Grasping, Contact, Coordination, Dexterity"
aliases:
  - "Manipulation TL;DR"
  - "Manipulation skim"
tags:
  - tldr
  - manipulation
  - dexterous
  - grasping
  - tactile
---

# TL;DR: Manipulation, Grasping, Contact, Coordination, Dexterity

> [!info] What this is
> A skimmable TL;DR of [[Manipulation| Manipulation: Grasping, Contact, Coordination, Dexterity]]. For each direction: **the bet**, the reasoning, the sharpest open questions, the risks. Full detail (related-work tables, all hypotheses, benchmarks) stays in the source. Plain-language version: [[__ELI5-EN__/Manipulation-ELI5|ELI5]].

> [!abstract] Overview
> One thing sets manipulation apart from every other robot skill: the **contact state**: which surfaces press the object, with what force, in what mode. It is a hidden variable the policy must *control*, not a label it reads off vision. The field's first reflex is to scale up, more grasp data, more demos, bigger policies. But contact has structure, and scaling pushes the wrong axis. A stable grasp is not a useful one. Force arrives too late to react to. Contact dynamics jump at the edge of the friction cone. Two arms coordinate through forces vision cannot see. The editorial bet: **contact is structure to model, compose, and bound, not data to collect.** The directions that put the contact state into the loss, action space, or constraint win where more teleoperation does not.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A: Grasping & Grasp Synthesis | A1–A3 | Making *task-relevant, feasible* grasps that transfer across objects and morphologies |
| B: Contact-Rich Assembly & Precision | B1–B2 | Sub-millimeter contact where vision is blind and the policy is open-loop |
| C: Bimanual & Dual-Arm Coordination | C1–C2 | Two-arm coupling cannot be split apart, and bimanual data is scarce |
| D: Dexterous & In-Hand Control | D1–D5 | Multi-fingered contact is high-DoF, jumpy, and breaks under sim-to-real |
| E: Tactile Foundations & Data Substrates | E1–E2 | Contact-rich, multi-modal data is scarce (4-order gap vs OXE), the substrate A–D pull tactile *from* |

## A: Grasping & Grasp Synthesis
*Task-fit, feasible grasps that transfer across objects and hands, including where the gripper must create the contact, not find it.*

### A1: Task-Affordance-Conditioned Grasp Synthesis
> [!abstract] The bet
> Claim 1: task-affordance (what the object is *for*) stays the same across hand shapes, an affordance-conditioned generator transfers parallel-jaw→dexterous (SynGrasp-1B→Dex1B), dropping ≥10 pp less than stable-grasp geometry.
> Claim 2: grasp quality splits into a stable score times a task score, a product scorer $Q(g)=Q_{\text{stable}}(g)\cdot Q_{\text{task}}(g)$ recovers ≥93% of hand-labeled success (AffordSim's oracle), zero per-object labels, at Dex1B-class stability (86.0% DexGraspNet).
> Falsifier: if affordance transfer drops as much as geometry, *or* the product score lands below 93% of the oracle, affordance is just a selection signal.

**Why**: The grasp that *holds* an object is not the one that *uses* it. Affordance-as-conditioning is settled (AffordDexGrasp, AffordGrasp, Grasp-as-You-Say); unproven is what it buys over geometry.

**First-principles**: *Principle:* the task fixes correctness, hand-independently. *Challenged:* GraspVLA/SynGrasp-1B is the real "just scale" holder (billion-frame synthetic pretrain, zero affordance term, its own clean scaling law) — but AffordSim's 15%→79% hard-tier jump shows that recipe collapses exactly where task, not object, decides correctness; the deeper live assumption is that affordance's gain is selection, never the invariant or a separable $Q$. *Wager:* it transfers and factors out label-free.

**Sharpest questions**: 1) Does the product score recover ≥93% of annotation with zero per-object labels? 2) Does the generator transfer parallel-jaw→dexterous with less drop than geometry? 3) Can language reasoning (GraspMAS/PALM) supply the affordance map as well as a trained VoxAfford?

> [!warning] Risks
> - Affordance accuracy sets the ceiling → report affordance-quality vs success.
> - Stable-grasp regression is already ~90% generic → score on affordance-critical tasks (pouring, hanging, tool-use), the 15%→79% gap.
> - Affordance and stability can conflict → make $Q$ tunable; show the Pareto front.

### A2: Cross-Morphology Grasp Transfer
> [!abstract] The bet
> The durable asset is the *protocol*, not an inequality: the field's first matched-data discrete-vs-continuous-vs-hybrid grasp-taxonomy shoot-out on a fixed held-out hand (Cross-Embodiment DexGrasp's 45-object YCB split, 4 seen → held-out LEAP/Inspire), which nobody has run. The predicted headline finding is the **hybrid**: a discrete grasp-type prior (power / precision / lateral) over a *continuous force residual* beats *both* pure-discrete and pure-continuous FAAS at matched data, because the discrete prior is a coarse mode-selector while the residual restores the hand-specific dexterity a hard 3-way code throws away, at ≥5× lower per-hand cost (UniDex 5.2×), with DexUMI-class in-domain SR (86%).
> Falsifiers: if the matched-data ablation cannot reproduce the FAAS-beats-joint-space margin on this split, the protocol does not discriminate coordinates; if pure-continuous FAAS ties the hybrid on the held-out hand, the discrete prior buys nothing and the invariant is just continuous function-space.

**Why**: Function-space transfer is settled (Cross-Embodiment DexGrasp's eigengrasps, DexGrasp-Zero's 85%/82% zero-shot, DexUMI's 86%), so "discrete beats continuous" is a single inequality the Historian predicts loses. Sparse Taxonomy Grasp built a discrete taxonomy for controllability only, never as a cross-hand transfer carrier, and no continuous anchor runs the hybrid arm.

**First-principles**: *Principle:* a grasp is which surfaces press at what force, not joint angles; *type* is the low-dim invariant, but the force detail is continuous and hand-specific, so neither pure pole is obviously the carrier. *Challenged:* not "function-space transfers" (consensus). No paper defends discrete-taxonomy for *cross-hand* transfer specifically — Sparse Taxonomy Grasp's own taxonomy win is single-hand, novel-*object* generalization only — so this is a genuine first-measurement gap, not an inequality to overturn; the eigengrasp/taxonomy debate has oscillated 30 years without this exact test. *Wager:* the matched-data shoot-out is the contribution, and the hybrid is the live resolution.

**Sharpest questions**: 1) On one fixed protocol, does the hybrid (discrete prior + continuous force residual) beat *both* pure-discrete and pure-continuous FAAS zero-shot to a held-out hand (Oymotion/Wuji) at matched data? 2) Does re-parameterizing DexJoCo in function-space turn the 50.4%→20.0% degradation positive? 3) Do exoskeleton-normalized demos (DexUMI) beat kinematic retargeting for cross-hand SR at matched volume?

> [!warning] Risks
> - A pure-discrete code loses fine dexterity, a wrong type on a novel hand fails catastrophically → this is why the headline is the *hybrid* (discrete prior + continuous residual), not pure-discrete; report the held-out-hand type-misclassification rate.
> - 40–60% transfer is not deployment-ready (UniDex's Wuji 40%) → frame as a few-shot seed; report the curve.
> - Negative-transfer risk (DexJoCo) → run the degradation-vs-transfer test before scaling up.

### A3: Deformable-Object Grasping under Ill-Defined Contact
> [!abstract] The bet
> Dense tactile sensing plus a differentiable soft-body world model beat the vision-only stress-RL solution (Stress-Guided RL) on **unseen** deformables, not just the training set. Three sub-claims:
> - It works where rigid-grasp estimators have no target to aim at.
> - Dense tactile beats sparse on *control success rate* (not just separation) by ≥10 pp.
> - The differentiable soft-body model beats model-free stress-RL on unseen objects.
>
> In-distribution it matches DexSkin's 90% pressure cut and 20%→60% integrity.
> Falsifier: if vision-only stress-RL ties dense-tactile-plus-soft-body on unseen deformables, the extra machinery buys nothing over reactive vision.

**Why**: A towel or blueberry has no canonical grasp pose; the gripper *produces* the contact, so the right grasp is force you regulate. Force-regulation-beats-pose-selection is settled (Stress-Guided RL, Force-Regulated Manipulation, DexSkin), but Stress-Guided RL omits tactile and any differentiable soft-body model, untested on held-out deformables.

**First-principles**: *Principle:* for a deformable, the contact state is a continuum the effector *produces*, shape is a function of the force field. *Challenged:* Stress-Guided RL bets reactive vision (RGB-D + PointNet, MPM as a train-time oracle) suffices. *Wager:* dense tactile measures the field; a differentiable model predicts where it heads.

**Sharpest questions**: 1) Does dense tactile translate to *control SR* (≥10 pp on held-out deformables), not just t-SNE separation? 2) Does a differentiable MPM/soft-body twin beat model-free stress-RL on unseen soft objects? 3) Where does folding-as-task-completion (Instant-Fold, 60.9% zero-shot) sidestep force-regulation entirely?

> [!warning] Risks
> - No canonical success metric for cloth → use task-completion (fold, pack) plus a force-bound, not grasp-SR.
> - Dense tactile optimization is unsolved (HumanoidVTA: dense barely beats sparse) → the dense-vs-sparse *control* test is the go/no-go; if it fails, narrow to force-regulation.
> - Soft-body sim is slow and inaccurate (ManiSkill2 ~80 FPS vs ~2000 rigid) → keep physics claims to validated twins (r > 0.9, Real-to-Sim GS).

## B: Contact-Rich Assembly & Precision
*Sub-millimeter contact, insertion, assembly, precision, where vision is blind, the policy is open-loop, and the in-distribution benchmark is saturated. The bet moves onto the prediction delta and OOD transfer.*

### B1: Predictive-Tactile Contact Imagination
> [!abstract] The bet
> A world model that predicts touch beats a matched reactive policy, mostly at contact-onset, and it survives dropping the sensor. Three sub-claims:
> - Turn off prediction at matched capacity and you lose DreamTacVLA's +22.3% gain, which sits at contact-onset steps, not flat across the task.
> - Deploy with *imagined* tactile instead of the real sensor and keep most sensor-on SR, on contact vision and action can predict.
> - Under disturbance, an OmniVTA-class 60 Hz loop holds 60–63% SR, not the saturated 95.0% headline.
>
> Falsifier: if a matched reactive policy ties the world-model policy *and* the gain is flat across phases, prediction adds nothing reaction cannot.

**Why**: Reactive feedback arrives only *after* contact, by then the misalignment already happened. Predict-then-act is co-discovered consensus (VT-WM, VTAM, the 2019 Deep Tactile MPC root), but no paper isolates whether the gain concentrates at onset, or whether imagined tactile replaces the sensor.

**First-principles**: *Principle:* next-step tactile is a forecastable consequence of the action given the contact state. *Challenged:* RDP is the real reactive-suffices holder — a high-frequency reactive fast-policy with no forecast at all, backed by +35% over Diffusion Policy and 0.8 vs 0.15 disturbance-recovery — but it was never run against a matched predictor on its own tasks; the WM crowd plans toward goal tactile states but still never runs that reactive-vs-predictive delta by onset. *Wager:* predicting force picks the better outcome *before* committing.

**Sharpest questions**: 1) Is the +22.3% world-model gain concentrated at contact-onset steps rather than flat? 2) Does a policy trained with tactile but deployed using *imagined* tactile recover most of sensor-on SR (couples to E1)? 3) Does forecasting a sensor-agnostic latent (TaF-VLA / Sparsh-X) keep the delta across deployment sensors?

> [!warning] Risks
> - Prediction may plateau at the noise floor (micro-slip not in the model) → keep the claim to vision/action-correlated contact.
> - World-model latency vs the reflex budget (must fit OmniVTA's 60 Hz loop) → horizon-vs-frequency ablation gates it.
> - Sim tactile is non-standard → use OmniVTA's OmniViTac plus a SPARR-style residual.

### B2: Contact-Mode-Conditional Precision & Reversibility
> [!abstract] The bet
> Give the policy a 5-state contact-mode label: free, making, in-contact, sliding, breaking ($c_t$), switching the *dynamics* per mode. It does two things.
> First, it transfers to *unseen* tasks beyond MATCH's single-task in-distribution result, hitting SPARR's +74.5% relative SR and 36.5% cycle-time cut on held-out NIST, below FAVLA's 7.7 N peak force.
> Second, it gives a **reversibility gate** read off the mode, cutting wedge-failures a binary-contact or mode-blind policy cannot.
> Falsifier: if a binary-contact policy (MATCH-class) with equal capacity ties the 5-state one on unseen NIST *and* matches its wedge-failure rate, the 5-state label adds nothing over a single contact bit.

**Why**: Insertion *is* a sequence through discrete contact modes (REASSEMBLE: force-torque reveals phase-distinct patterns), yet most policies treat it as one continuous map. Discrete-mode structure is partly explored (MATCH: binary bit; PhaForce: phase belief), but none expose a 5-state mode latent switching *dynamics*, or a reversibility gate.

**First-principles**: *Principle:* contact dynamics jump at boundaries (friction-cone edge, force spike, stick→slip), so the right latent is a mode label switching the *dynamics model*. *Challenged:* MATCH collapses contact to one bit. *Wager:* only a mode label says if a retreat is reversible.

**Sharpest questions**: 1) Does a 5-state mode latent beat MATCH's binary bit and FAVLA's implicit frequency on *unseen* NIST transfer? 2) Does gating corrective retreats on the mode cut wedge-failures a mode-blind policy cannot avoid? 3) Can a mode classifier distilled from REASSEMBLE phase annotations + sim reach usable accuracy without dense real labels?

> [!warning] Risks
> - Discrete-latent optimization variance (Gumbel-softmax/REINFORCE) → anneal soft→hard.
> - Mode supervision needs ground truth → distill from REASSEMBLE's phase annotations plus sim; report accuracy.
> - Saturated headline (SPARR already 95–100% on AutoMate) → show the win on *unseen* NIST transfer plus a peak-force bound plus reversibility, not in-distribution SR.

## C: Bimanual & Dual-Arm Coordination
*Two-arm manipulation where the coupling cannot be split apart and data is scarce, composing single-arm priors, generating data with coordination structure, and sensing inter-arm force vision cannot see.*

### C1: Coordination-Native Bimanual Policies
> [!abstract] The bet
> The two-arm coupling has real structure, and its failure can be pinned down where a single big policy cannot — and the same structure-over-volume logic holds one level up, in the data that trains it. Four sub-claims, the first three at composition's data cost (TwinVLA 76% / ~25 H100-days):
> - The coupling needs little data, near TwinVLA's ~50 episodes, even on BiCoord's 4×-harder tightly-coupled tasks.
> - A typed coupling (async / sync / ordered, from DexMimicGen) beats one Joint-Attention layer on tightly-coupled subtasks.
> - BiCoord's late-stage failures come from the *coupling*, not the single-arm skill (which stays strong).
> - Stripping DexMimicGen's coordination structure from generated training data, at matched trajectory volume, drops its 90%-from-40-demos result by ≥30 pp.
>
> Falsifier, on either leg: if the coupling's data need rises sharply on harder tasks *and* a typed coupling only ties one layer, the *policy*-side coupling has no structure and the story ends at the settled headline; if raw-replay at matched volume holds DexMimicGen's result, the *data*-side structure claim fails on its own — one leg can fall without the other.

**Why**: Each arm's *skill* is a transferable single-arm prior. Composition-beats-monolith is settled (TwinVLA's attention, EnergyAction's energy functions, SkillVLA's skill-recompose; Decoupled Bimanual ran the falsifier, +23.5% / 1/6 size).

**First-principles**: *Principle:* the whole splits into a transferable single-arm skill and a coupling; only the coupling needs two-arm data. *Challenged:* RDT-1B is the real monolithic-scale holder — 1.2B params, 46-dataset/1M-trajectory pretrain, +56% over SOTA, and its own size ablation (166M vs 1.2B) shows scale itself is load-bearing — but Decoupled-Bimanual already refutes it at matched data (+23.5% at 1/6 the size); the remaining consensus shows composition works but never tested the coupling's data-floor, type, or failure mode. *Wager:* it has all three.

**Sharpest questions**: 1) Does the coupling reach TwinVLA's ~50-episode result even on BiCoord's 4×-harder tightly-coupled tasks? 2) Does conditioning the coupling on DexMimicGen's async/sync/ordered subtask type beat one Joint-Attention layer? 3) Does BiCoord's later-stage degradation localize to the coupling (freeze single-arm priors, vary only the coupling)? 4) On the data-generation side, does stripping DexMimicGen's coordination structure (raw SE(3) replay) at matched trajectory volume drop its 90%-from-40-demos result by ≥30 pp, cleanest on a differentiable generator (CRAFT, whose own Canny-conditioning ablation already shows 21.6% vs 10.3%)?

> [!warning] Risks
> - Composition may cap the coordination ceiling (handover + force balance may exceed composed priors) → keep to loosely-to-moderately-coupled tasks; report tightness-vs-SR.
> - Joint Attention is one design (TwinVLA's causal-masked attention) → the typed-coupling ablation tests it.
> - Single-arm priors must be strong → validate base SR first; assumes π0/RDT.
> - Generated data may miss tight coupling (parallel-but-not-coordinated) → the structure-vs-volume ablation (question 4) is the gate; couple generation to this direction's coupling-aware training.

### C2: Tactile-Coupled Bimanual Cooperation
> [!abstract] The bet
> Two claims about two-arm touch. First, a *shared* force channel between the arms beats per-arm fusion (VT-Refine / TAMEn-class), winning holding-while-manipulating by ≥10 pp SR. Second, lifting Symmetry-Aware VT Fusion's force-*balance* loss from two fingers to two *arms* beats tactile-as-input on a force-balanced handover. This reaches TAMEn's 75% contact-rich SR, using VTouch++'s synchronized data.
> Falsifier: if per-arm fusion ties the shared channel on holding-while-manipulating *and* the balance loss ties tactile-as-input on handover, neither sharing nor balance is the missing piece.

**Why**: Force-balanced cooperation needs inter-arm force observability vision lacks. Tactile beats vision on contact-coupled bimanual (VT-Refine, 2 mm-clearance assembly), but VT-Refine's coordination is emergent with no shared channel, and Symmetry-Aware's balance loss is for two fingers, not two arms.

**First-principles**: *Principle:* when one arm holds and the other manipulates, cooperation is the force *each transmits through the object*, one shared quantity. *Challenged:* Coordinated-Bimanual-State-Diffusion is the real vision-only holder — zero force/tactile sensing, 15/15 vs 0/15 on Laundry-Cleanup's second pillow — but VT-Refine refutes it only on contact-*coupled*, tight-tolerance tasks; on those, per-arm fusion still observes each arm in isolation. *Wager:* only a shared representation captures the coupling; only an explicit balance objective optimizes it.

**Sharpest questions**: 1) Does a *shared* inter-arm tactile representation beat per-arm fusion by ≥10 pp on holding-while-manipulating? 2) Does lifting the two-finger force-symmetry loss to a two-*arm* balance objective beat tactile-as-input on handover? 3) Does adding the shared tactile channel to C1's TwinVLA beat vision-only Joint Attention?

> [!warning] Risks
> - Inter-arm tactile is hard to instrument → VTouch++ / TAMEn data exist; use bimanual-tactile rigs.
> - Dense tactile optimization is unsolved (HumanoidVTA: dense barely beats sparse) → use Multi-Sensory Sparse Experts' AdaMN normalization.
> - Force-balance reward can over-constrain (may block asymmetric grasps) → make it tunable; show the trade-off.

## D: Dexterous & In-Hand Control
*Multi-fingered hands doing high-DoF, contact-jumpy, sim-to-real-fragile work, making intent hand-agnostic, bridging tactile sim-to-real without a tactile simulator, unlocking emergent dexterity through exploration, bounding contact force with a hard constraint, and asking whether that per-instant bound is even the right constraint class for damage that accumulates across repeated contact.*

### D1: Universal Cross-Morphology Hand Control
> [!abstract] The bet
> One backbone runs the *full* reach→grasp→reorient→place cycle across different hands, no existing system does this: GET only does in-hand rotation across configs of *one* hand; DexWM spans the cycle, but on one hand family.
> Second claim: at the reorient step, how you encode intent matters, three ways differ measurably: explicit-intent (FAAS), implicit-history (DexFormer), graph-structure (GET).
> Targets: match DexWM's 72%/58%/28% zero-shot reach/grasp/place and its 83% real grasp, 5.2× cheaper than collecting data per hand, real-time (Multi-Sensory Sparse Experts cuts compute 42.6%).
> Falsifiers: if a joint-space/graph policy (GET-class) with equal data matches the cycle transfer on an unseen distinct hand, intent is not the invariant; if the three encodings tie at reorient, the choice does not matter.

**Why**: Single-weight policies already transfer across morphologies (GET zero-shots to 10 hand configs, DexFormer controls 32 variants), DexFormer via implicit history-conditioning, GET via graph-joint-space. (D1: the cycle; A2: the grasp.)

**First-principles**: *Principle:* control intent is a plan independent of the hand; the torques are not. *Challenged:* GET is the real holder of the opposing case, and says so explicitly — its paper calls unified action spaces "often not sufficient" for precise joint control and, for varying-finger hands, says forming one "is not possible" at all, so it routes around intent representations entirely and gets 99% of expert performance plus +20% zero-shot from graph-structure alone; which parameterization (intent, history, or graph) carries the full cycle is still open, especially at reorientation. *Wager:* it may vary by phase; none unifies the cycle across hands.

**Sharpest questions**: 1) Does intent-space transfer the full reach/grasp/place cycle on a held-out *distinct* hand where GET's graph-joint-space does not? 2) Do explicit-intent, implicit-history, and graph-structure parameterizations differ measurably *at reorientation*? 3) Does intent for the plan plus a per-hand joint-residual for fine actuation beat either alone?

> [!warning] Risks
> - Intent-space loses fine dexterity → split into intent plus joint-residual; keep intent to contact-establishment.
> - 40–60% transfer is not deployment-ready (UniDex's Wuji 40%) → frame as a few-shot seed.
> - MoE may not specialize by hand → test routing-by-hand before claiming cross-morphology scaling.

### D2: Tactile In-Hand Reorientation with Sim-to-Real
> [!abstract] The bet
> Three distillation targets compete: object pose-and-shape (PTLD), contact features (AnyRotate), or a simulated tactile sensor (Force-Based Sim2Real). Run all three on the *same* reorientation task under the same disturbances. Pose-and-shape should win.
> Targets: PTLD's +182% rotation and +57% goals, DeXtreme's 27.8-vs-14.8, holding up under ViserDex's harsh lighting (~25).
> Falsifiers: if contact features tie pose-and-shape, the cheaper target wins; if simulating the sensor matches either, the simulator was never the bottleneck.

**Why**: Tactile is only an interface to the privileged state it encodes, so a *real* privileged sensor can replace a *simulated* one as the distillation target. Avoiding the sensor sim is demonstrated but not settled (AnyRotate, CoRL'24, no tactile sim — but Force-Based Sim2Real, 2026, still builds one and gets 25.1 vs 1.1 rotations); PTLD's object-pose-state interface is a distinct, untested third alternative. (D2 is E1's Route-2 specialized to reorientation.)

**First-principles**: *Principle:* tactile is only an interface, the policy needs the privileged *state* it encodes. *Challenged:* Force-Based Sim2Real (2026) is the real, still-live "needs a tactile sim" holder (25.1 vs 1.1 rotations with vs without) — even though AnyRotate showed it avoidable back in 2024, the field hasn't converged; and among the no-sim routes, contact-features (AnyRotate) is not the only option. *Wager:* object-pose-state is task-complete; contact-features are lossy.

**Sharpest questions**: 1) Does object-pose-state beat contact-feature *and* tactile-sim three-way on the same reorientation task under matched perturbations? 2) Under perturbation, does tactile hold better under slip while vision holds better under lighting (a modality-vs-perturbation split)? 3) Does DexSkin's cross-sensor calibration generalize the PTLD estimator across tactile hardware without re-collecting privileged pairs?

> [!warning] Risks
> - Instrumented real cell needed (PTLD requires a privileged sensor) → a one-time cost, not a deployment dependency.
> - Privileged-real distillation may not generalize beyond training objects → keep to distribution; H3 tests cross-hardware.
> - Tactile vs visual may be task-dependent → report the modality-vs-perturbation split (slip favors tactile, lighting vision).

### D3: Operationalizing Emergent Multi-Phase Dexterity
> [!abstract] The bet
> Papers in this cluster call a behavior "emergent" by eyeballing a rollout — no shared definition, no common yardstick across exploration levers (reset-diversity, reward-shaping, intrinsic-coverage). The bet: state-conditioned exploration coverage and task-agnostic reward structure are the causal drivers behind emergence's two conditions (cross-task reuse, phase-count) — not exploration volume or scale. ContactExplorer's own ablation already shows state-conditioning prevents saturation and lets contact patterns reuse across different object configurations (100% vs 18% on its Box-Push diagnostic); the bet extends that to cross-task reuse. Given both mechanisms hold, a metric built on them, tested in one fixed-task, fixed-compute study that sweeps only the lever, ranks OmniReset (diverse-reset), Retrieval-Dexterity (potential-shaping), ContactExplorer (intrinsic-coverage), and SBRL (planner-generated reset) in the same order as their own zero-shot SR, at rank correlation ρ ≥ 0.7.
> OmniReset's own 85.37%-vs-~2% reset-diversity margin over a demo-cloning baseline (real peg insertion vs aggregate DP baseline) stays as settled background, not the bet.
> Falsifier: if state-conditioning doesn't predict the reuse sub-score, if reward structure doesn't predict phase-count, or if the ranking scrambles relative to SR (ρ < 0.7) despite both mechanisms holding, the mechanisms don't compose into a valid metric.

**Why**: "Emergent" is asserted by video, not measured — OmniReset, Retrieval-Dexterity, and VLM-Dexterous-Scaffolding each call their own lever's output "emergent" on a different task, with no shared instrument to compare the claims.

**First-principles**: *Principle:* a behavior recombines across tasks only if the exploration process stores what it discovers in a form indexed by context, not by the task's own reward; it has a discoverable phase count only if the reward doesn't pre-commit to a fixed sequence of stages. *Challenged:* not "reset diversity beats reward shaping" (OmniReset already shows that against a fixed baseline) — the wrong assumption is that emergence is a byproduct of exploration volume or scale rather than of these two identifiable design properties, and that eyeballing a rollout substitutes for measuring them. *Wager:* the two mechanisms are real and compose into a valid, discriminating metric, not a bookkeeping label.

**Sharpest questions**: 1) Does the metric rank OmniReset, Retrieval-Dexterity, ContactExplorer, and SBRL in the same order as their own zero-shot SR (ρ ≥ 0.7)? 2) Do two SR-matched levers still register a phase-count gap ≥1? 3) Does state-conditioned exploration coverage, not exploration volume alone, drive the cross-task-reuse sub-score (extending ContactExplorer's 100%-vs-18% configuration-level ablation)? 4) Does task-agnostic reward structure, not curriculum orchestration, drive phase-count — OmniReset's single reward vs Reset's task-graph curriculum-to-goal? 5) Is the ranking stable across different phase-detection thresholds (Kendall's τ ≥ 0.7)?

> [!warning] Risks
> - Reset-diversity-vs-reward-shaping is not this direction's open question (OmniReset already settles it against a fixed baseline) → keep the bet on the metric's validity and the mechanism behind it, not on re-litigating which lever wins.
> - The metric's two conditions (un-rewarded + cross-task reuse) are themselves a design choice → the threshold-robustness question directly tests this.
> - Sim-to-real for emergent policies is task-dependent, not uniformly fragile (OmniReset's real SR spans 85.37% Peg down to 15.38% Drawer) → run the correlation across the full task spread, not just Peg; couple to DRIS/DeXtreme randomization to lift the floor on weaker tasks.
> - Emergent behaviors may be unsafe (exploration can damage contacts) → bound with D4's QP/force-safety; report contact-force statistics.

### D4: Force-Safety-Constrained Dexterous Control
> [!abstract] The bet
> Put a hard gentle-force filter, a CBF/QP feasible-set projection, on top of a learned dexterous policy. FORGE-plus already gets a decoupled hard clamp to 100% SR / 0% breakage on fragile objects, but at its own oracle force ceiling that same clamp still breaks 49.8% of objects under closed-loop impedance overshoot.
> The bet: a continuous CBF/QP projection over the same learned-policy class holds breakage at ≤10% under that same stress test. It should also beat the soft-penalty approach (Stress-Guided RL, 36.5% stress cut) on fragile-object integrity at matched SR, scored on SoGraB's standardized deformation metric, while keeping Hierarchical RL-QP Grasp's 81.4% (vs 13.2% unconstrained) and staying steerable zero-shot.
> Falsifier: if the CBF/QP projection breaks fragile objects at a rate statistically indistinguishable from FORGE-plus's 49.8% oracle-bound clamp breakage (≥30%), the clamp-vs-projection distinction is architectural noise, not a real mechanism difference, and the projection buys nothing over a clamp.

**Why**: Safety is a hard constraint on contact-force that must hold *every* step; a learned policy only softly penalizes violations, a physics-based filter guarantees them. The *generic* hard-filter-beats-soft-penalty claim is settled (Safe Steerable Geometric Policy hard-enforces force-*closure*). FORGE-plus now closes most of the SR/breakage gap on a fragile-force ceiling over a *learned* policy, narrowing the open bet to what a continuous projection buys that a decoupled hard clamp does not: avoiding the impedance-overshoot breakage that shows up even at FORGE-plus's own oracle bound.

**First-principles**: *Principle:* a gentle-force constraint (force ≤ a fragile tolerance, e.g. DexSkin's 1.53 kPa or Multi-Sensory-Sparse-Experts' ~10 N) is an *upper* bound, the opposite of force-*closure*. Refinement, not a retraction: fragile-object damage is really a *stress* phenomenon (force per contact area) — DOBCBF-Grasping's own hard force-ceiling (Eq. 11) bounds raw Newtons with no area term anywhere, so a CBF that copies its form inherits the same wrong variable; the mechanism (hard bound beats soft penalty) still holds, what it bounds needs correcting from force to stress. *Challenged:* the consensus filters enforce closure; the fragile ceiling stays soft-penalized (Stress-Guided RL) or, now, only a decoupled clamp (FORGE-plus) rather than a continuous projection. *Wager:* an upper bound that must hold under closed-loop overshoot needs a feasible-set projection over the correct variable, not a one-shot force-only clamp.

**Sharpest questions**: 1) Does a CBF/QP feasible-set projection over a learned policy avoid the impedance-overshoot breakage a decoupled hard clamp does not, holding fragile-object breakage at ≤10% where FORGE-plus's clamp broke 49.8%? 2) Does projecting onto an *area-converted* force-bound set (DexSkin's 1.53 kPa pressure threshold times an estimated contact-patch area, not the kPa value dropped directly into a Newton-valued CBF) preserve fragile-object integrity better than penalty-training at matched SR — and, re-running FORGE-plus's oracle-bound stress test with contact-area logged, does breakage actually concentrate in the lowest-area quartile at roughly double the highest-area quartile's rate, or does force alone already explain it? 3) Can the QP/force-bound filter make D3's emergent or D1's transferred policies deployable without retraining?

> [!warning] Risks
> - QP clamping can hurt task SR → report the safety-vs-SR trade-off; clamp rarely.
> - Force tolerances are object-specific (1.53 kPa for berries ≠ rigid assembly) → make the bound per-object (A1/A3); no global limit.
> - Hard constraints may over-restrict emergent behavior (transient high forces may be needed) → test over emergent policies; allow needed force, block damage.
> - Force-observability tax: a ceiling assumes per-fingertip force is measurable at control rate, not free on a 23-DoF hand → report the projection's behavior when force is *estimated*, not measured; a ceiling the policy can't observe can't be guaranteed.
> - One-shot bound, not closed-loop regulation: every result scores a per-step force magnitude, never reactive regulation over the post-contact horizon → instrument where the projected force diverges under closed-loop feedback (contact-onset vs settled-hold vs re-grasp), not just worst-case single-step violation.

### D5: Cumulative-Damage-Constrained Repeated-Contact Control
> [!abstract] The bet
> Re-run FORGE-plus's exact fragile-object task and oracle-$F_\text{max}$ setup as a 10-regrasp stress test on the *same* object instance, scoring SoGraB's deformation metric cumulatively after each regrasp. Cumulative deformation should cross a real damage threshold (≥0.1 points on SoGraB's 0.517→0.940 scale) within those 10 regrasps in at least half of fragile-object trials, even when *every* individual regrasp clears FORGE-plus's own oracle force bound (0% per-step violations) — the same bound whose one-shot breakage rate is 49.8% under impedance overshoot.
> Falsifier: if fewer than half of the trials where every regrasp clears the per-step bound cross that threshold, path-dependence is not load-bearing, and the per-step framing was fine all along.

**Why**: Every safety filter in this cluster — Safe Steerable Geometric Policy's force-closure CBF, DOBCBF-Grasping's min/max ceiling, FORGE-plus's own clamp — bounds force at the current instant only; none carries a state for prior load. Real contact is not like that: friction has static/kinetic hysteresis, viscoelastic materials relax and creep, and repeated sub-yield loading accumulates damage below any single-instant threshold, the same mechanism that snaps a paperclip from many gentle bends none of which alone would break it.

**First-principles**: *Principle:* damage from repeated loading is an integral over the load history, $\int D(f(\tau))\,d\tau$, not a function of the current instant. *Challenged:* every hard-filter paper in this cluster treats a tight-enough per-step bound as a damage guarantee; none augments its barrier function with an accumulated-load state. *Wager:* the integral crosses a real threshold before any per-step bound is ever violated.

**Sharpest questions**: 1) Does cumulative SoGraB deformation cross threshold within 10 regrasps while every individual regrasp clears FORGE-plus's oracle bound? 2) Does a damage-state-augmented CBF beat a simply-tightened static bound at matched cumulative-damage flatness, or is a smaller per-step number all that was needed? 3) Does the within-episode force-divergence signal this cluster's own risk notes already call for actually predict the cross-episode damage slope, or is it a different, uninformative quantity?

> [!warning] Risks
> - Re-deriving CBFs may be unnecessary complexity if a tighter static bound works just as well → gate the full re-derivation on the matched-flatness test.
> - The 10-regrasp protocol assumes the object survives to trial 10 → pre-screen for a fragility band that survives repeated regrasps, per FORGE-plus's own object choice (ABS gears/bottles).
> - If this holds, every tactile-forecasting world model in this doc (B1) is trained on the wrong prediction target for repeated handling → scope the initial claim to the safety layer before generalizing to world-model retraining.
> - The imported 49.8% breakage figure this direction leans on may itself be a contact-area artifact, not pure force → D4's new test checks whether breakage concentrates by contact-area quartile; if it does, this direction's damage integral should run on stress (force/area), not raw force.

## E: Tactile Foundations & Data Substrates
*The foundation layer beneath force-aware manipulation, needing no runtime tactile hardware, getting force-awareness to deployment with the sensor dropped, and a cross-sensor representation that makes any such policy portable across sensors.*

### E1: Sensor-Free Force-Aware Policies
> [!abstract] The bet
> Route 1 is the front-line claim. Train a force-aware policy on ~20k hr of ego *video alone*, no force or tactile data at any stage. It should reach ≥80% of a tactile-instrumented policy's SR on ForceVLA's 5 tasks.
> EgoScale shows ego-video scaling already adds +54% on 22-DoF dexterous. The bar to clear is the instrumented policy; the settled Route-2 distillers (FD-VLA 61.1%, HapticVLA 86.7%) already match it, the parity baseline.
> Falsifier: if the ego-video-only policy cannot clear 80% of the instrumented baseline, force-awareness cannot be learned without a teacher signal, and Route 2 was the only way.

**Why**: The object moves *because* of force, so tactile-awareness is separable from the sensor that taught it. Route 2 (distill a tactile teacher, drop the sensor) is settled (FD-VLA even beats the with-sensor baseline; ViTacGen, HapticVLA). Route 1 is unattacked: a force-aware *full policy* from ego video alone, every ego backbone (EgoScale, Being-H0, DexWM) omits the head.

**First-principles**: *Principle:* force is *upstream* of vision in contact, so vision→force is a well-posed inverse, separable from the supervising sensor. *Challenged:* Route 2 still needs an instrumented teacher; none learns it from ego video alone. *Wager:* if well-posed, the signal drops at *every* stage, not just deployment.

**Sharpest questions**: 1) Can an ego-video-only force-objective policy clear ≥80% of the instrumented baseline on ForceVLA's 5 tasks, failures concentrated on vision-uncorrelated slip? 2) Does predicted tactile from ego video (TouchAnything view-dropout + Sparsh-X teacher on a small instrumented fraction) recover real-tactile SR? 3) Does ego-video force-awareness survive the 22-DoF-human → 1–7-DoF-gripper embodiment gap, and which projection (explicit MANO vs keypoint) retains most?

> [!warning] Risks
> - Vision-to-tactile noise floor (Route 1), subtle slip needs fingertip pressure → keep to vision-correlated force.
> - Distillation gap on novel objects (Route 2), the student may fail where the teacher's tactile was load-bearing → keep to in-distribution contact; report the gap per object class.
> - Scaling / instrumentation cost (Route 1's 20k+ hr; Route 2 needs a teacher cell) → for Route 1, use Sparsh-X as a synthetic-tactile teacher on a small fraction; the cell is one-time.

### E2: Cross-Sensor Tactile Foundation Models for Plug-And-Play Force-Aware Policies
> [!abstract] The bet
> A *leave-one-sensor-out* (N−1) test: hold out one sensor the encoder has never seen, deploy a policy, and measure retained success rate. The claim: retained SR rises as you train on *more kinds* of sensors, clearing ≥80% with only a small number of training sensors.
> This goes past two prior results. UniForce gets 90–120%, but it saw all 3 sensors. TaF-VLA tops out at 60.3% at the sensor-family level.
> Falsifier: if held-out-sensor *policy SR* stays below 80% no matter how many sensors the encoder trains on, the ceiling is fundamental, a visual-to-tactile floor, not a data problem, and cross-sensor deployment is capped.

**Why**: A force-grounded encoder (UniForce) now exists, transferring zero-shot across vision-based and magnetic sensors, so the question is not "can it transfer?" but the *scaling law*: every prior result trains with the test sensor *seen*, or reports perception accuracy, never an encoder-held-out N−1 sweep against policy-SR.

**First-principles**: *Principle:* force is a physical quantity, so a force-grounded encoder is invariant by construction (UniForce confirms it, z5↔Fz r=−0.74). *Challenged:* no paper argues perception invariance should certify policy transfer — RCT calls it a field-wide methodological blind spot, not a defended position — but every prior result (UniForce, SITR, T3) still tests with the sensor seen or reports perception accuracy, never a strict held-out policy-SR sweep. *Wager:* unknown is whether it *scales* with added sensors.

**Sharpest questions**: 1) Does held-out-policy-SR retention rise monotonically with training-sensor diversity under a strict N−1 sweep, clearing ≥80% by a small N? 2) Is policy-SR the load-bearing metric (does a sensor clearing 81.94% inter-sensor *classification* still lose deployable policy-SR)? 3) Does a single force-invariant latent (UniForce) beat a per-sensor-encoder trunk (Transferable Tactile Transformer) on the held-out sensor?

> [!warning] Risks
> - Fundamental sensor incompatibility (capacitive vs piezoresistive vs vision-tactile) → ground to the physical force vector, not raw output; report what is lost.
> - Recursive data problem (SSL needs many sensors, missing *because* transfer is the bottleneck) → bootstrap from UniForce's force-equilibrium corpus plus Sparsh-X.
> - Retention may plateau below 80% (a visual-to-tactile floor) → run the N−1 *policy-SR* sweep first as the go/no-go.
