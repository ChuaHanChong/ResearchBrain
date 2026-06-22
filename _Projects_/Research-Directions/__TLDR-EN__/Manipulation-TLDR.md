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
| C: Bimanual & Dual-Arm Coordination | C1–C3 | Two-arm coupling cannot be split apart, and bimanual data is scarce |
| D: Dexterous & In-Hand Control | D1–D4 | Multi-fingered contact is high-DoF, jumpy, and breaks under sim-to-real |
| E: Tactile Foundations & Data Substrates | E1–E2 | Contact-rich, multi-modal data is scarce (4-order gap vs OXE), the substrate A–D pull tactile *from* |

## A: Grasping & Grasp Synthesis
*Task-fit, feasible grasps that transfer across objects and hands, including where the gripper must create the contact, not find it.*

### A1: Task-Affordance-Conditioned Grasp Synthesis
> [!abstract] The bet
> Claim 1: task-affordance (what the object is *for*) stays the same across hand shapes, an affordance-conditioned generator transfers parallel-jaw→dexterous (SynGrasp-1B→Dex1B), dropping ≥10 pp less than stable-grasp geometry.
> Claim 2: grasp quality splits into a stable score times a task score, a product scorer $Q(g)=Q_{\text{stable}}(g)\cdot Q_{\text{task}}(g)$ recovers ≥93% of hand-labeled success (AffordSim's oracle), zero per-object labels, at Dex1B-class stability (86.0% DexGraspNet).
> Falsifier: if affordance transfer drops as much as geometry, *or* the product score lands below 93% of the oracle, affordance is just a selection signal.

**Why**: The grasp that *holds* an object is not the one that *uses* it. Affordance-as-conditioning is settled (AffordDexGrasp, AffordGrasp, Grasp-as-You-Say); unproven is what it buys over geometry.

**First-principles**: *Principle:* the task fixes correctness, hand-independently. *Challenged:* the crowd treats affordance as selection, never the invariant or a separable $Q$. *Wager:* it transfers and factors out label-free.

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

**First-principles**: *Principle:* a grasp is which surfaces press at what force, not joint angles; *type* is the low-dim invariant, but the force detail is continuous and hand-specific, so neither pure pole is obviously the carrier. *Challenged:* not "function-space transfers" (consensus) but the idea that discrete-vs-continuous has one winner, the eigengrasp/taxonomy debate has oscillated 30 years. *Wager:* the matched-data shoot-out is the contribution, and the hybrid is the live resolution.

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

**First-principles**: *Principle:* next-step tactile is a forecastable consequence of the action given the contact state. *Challenged:* the WM crowd plans toward goal tactile states but never runs the reactive-vs-predictive delta by onset. *Wager:* predicting force picks the better outcome *before* committing.

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
> The two-arm coupling has real structure, and its failure can be pinned down where a single big policy cannot. Three sub-claims, all at composition's data cost (TwinVLA 76% / ~25 H100-days):
> - The coupling needs little data, near TwinVLA's ~50 episodes, even on BiCoord's 4×-harder tightly-coupled tasks.
> - A typed coupling (async / sync / ordered, from DexMimicGen) beats one Joint-Attention layer on tightly-coupled subtasks.
> - BiCoord's late-stage failures come from the *coupling*, not the single-arm skill (which stays strong).
>
> Falsifier: if the coupling's data need rises sharply on harder tasks *and* a typed coupling only ties one layer, the coupling has no structure and the story ends at the settled headline.

**Why**: Each arm's *skill* is a transferable single-arm prior. Composition-beats-monolith is settled (TwinVLA's attention, EnergyAction's energy functions, SkillVLA's skill-recompose; Decoupled Bimanual ran the falsifier, +23.5% / 1/6 size).

**First-principles**: *Principle:* the whole splits into a transferable single-arm skill and a coupling; only the coupling needs two-arm data. *Challenged:* the consensus shows it works but never tested the coupling's data-floor, type, or failure mode. *Wager:* it has all three.

**Sharpest questions**: 1) Does the coupling reach TwinVLA's ~50-episode result even on BiCoord's 4×-harder tightly-coupled tasks? 2) Does conditioning the coupling on DexMimicGen's async/sync/ordered subtask type beat one Joint-Attention layer? 3) Does BiCoord's later-stage degradation localize to the coupling (freeze single-arm priors, vary only the coupling)?

> [!warning] Risks
> - Composition may cap the coordination ceiling (handover + force balance may exceed composed priors) → keep to loosely-to-moderately-coupled tasks; report tightness-vs-SR.
> - Joint Attention is one design (TwinVLA's causal-masked attention) → the typed-coupling ablation tests it.
> - Single-arm priors must be strong → validate base SR first; assumes π0/RDT.

### C2: Scalable Bimanual Data Generation with Coordination Structure
> [!abstract] The bet
> Strip the coordination structure but keep the data volume the same, and the result should collapse, a front-line *prediction*, not a reported number. The claim: raw SE(3) replay at the same trajectory count drops DexMimicGen's 90%-from-40 by ≥30 pp. Cleanest test is on a *differentiable* generator (D-CODA / CRAFT); CRAFT's Canny-conditioning ablation already shows 21.6% vs 10.3%. Structured generation otherwise reaches RoboTwin 2.0's +24.4% few-shot.
> Falsifier: if raw SE(3) replay at matched volume still keeps the 90%-from-40, structure adds nothing volume could not, the consensus result would be a volume effect mislabeled as structure.

**Why**: RoboTwin 2.0 names the dual-arm data wall; structure-aware generation is settled (MoMaGen subsumes the X-Gen family; DexMimicGen, BiDemoSyn, CRAFT instantiate it). But no generator isolates whether the gain is *structure* or *volume*.

**First-principles**: *Principle:* bimanual generalization comes from coordination structure (per-arm subtasks with sync/ordering), not volume. *Challenged:* MoMaGen and the X-Gen family assert it but never strip structure at matched volume. *Wager:* if so, matched-volume SE(3) replay collapses.

**Sharpest questions**: 1) Does stripping sync/ordering (raw SE(3) replay) at matched volume drop the 90%-from-40 by ≥30 pp, cleanest on a differentiable generator? 2) Does MLLM expert-code (RoboTwin 2.0) capture *coordinated* trajectories better than demo-replay on tightly-coupled tasks? 3) Does physics-grounded generation (PGDG) beat kinematic replay where contact validity matters?

> [!warning] Risks
> - Generated data may miss tight coupling (parallel-but-not-coordinated) → the BiCoord late-degradation test gates it; couple to C1.
> - Sim-to-Real Cliff (RoCo Challenge: sim policies brittle) → use RoboTwin 2.0's 5-axis randomization plus TAMEn filtering.
> - MLLM code-gen reliability (RoboTwin 2.0's 71.3% auto-code, ~29% needs refinement) → human-in-the-loop; report generation-yield.

### C3: Tactile-Coupled Bimanual Cooperation
> [!abstract] The bet
> Two claims about two-arm touch. First, a *shared* force channel between the arms beats per-arm fusion (VT-Refine / TAMEn-class), winning holding-while-manipulating by ≥10 pp SR. Second, lifting Symmetry-Aware VT Fusion's force-*balance* loss from two fingers to two *arms* beats tactile-as-input on a force-balanced handover. This reaches TAMEn's 75% contact-rich SR, using VTouch++'s synchronized data.
> Falsifier: if per-arm fusion ties the shared channel on holding-while-manipulating *and* the balance loss ties tactile-as-input on handover, neither sharing nor balance is the missing piece.

**Why**: Force-balanced cooperation needs inter-arm force observability vision lacks. Tactile beats vision on contact-coupled bimanual (VT-Refine, 2 mm-clearance assembly), but VT-Refine's coordination is emergent with no shared channel, and Symmetry-Aware's balance loss is for two fingers, not two arms.

**First-principles**: *Principle:* when one arm holds and the other manipulates, cooperation is the force *each transmits through the object*, one shared quantity. *Challenged:* per-arm fusion observes each arm in isolation. *Wager:* only a shared representation captures the coupling; only an explicit balance objective optimizes it.

**Sharpest questions**: 1) Does a *shared* inter-arm tactile representation beat per-arm fusion by ≥10 pp on holding-while-manipulating? 2) Does lifting the two-finger force-symmetry loss to a two-*arm* balance objective beat tactile-as-input on handover? 3) Does adding the shared tactile channel to C1's TwinVLA beat vision-only Joint Attention?

> [!warning] Risks
> - Inter-arm tactile is hard to instrument → VTouch++ / TAMEn data exist; use bimanual-tactile rigs.
> - Dense tactile optimization is unsolved (HumanoidVTA: dense barely beats sparse) → use Multi-Sensory Sparse Experts' AdaMN normalization.
> - Force-balance reward can over-constrain (may block asymmetric grasps) → make it tunable; show the trade-off.

## D: Dexterous & In-Hand Control
*Multi-fingered hands doing high-DoF, contact-jumpy, sim-to-real-fragile work, making intent hand-agnostic, bridging tactile sim-to-real without a tactile simulator, unlocking emergent dexterity through exploration, and bounding contact force with a hard constraint.*

### D1: Universal Cross-Morphology Hand Control
> [!abstract] The bet
> One backbone runs the *full* reach→grasp→reorient→place cycle across different hands, no existing system does this: GET only does in-hand rotation across configs of *one* hand; DexWM spans the cycle, but on one hand family.
> Second claim: at the reorient step, how you encode intent matters, three ways differ measurably: explicit-intent (FAAS), implicit-history (DexFormer), graph-structure (GET).
> Targets: match DexWM's 72%/58%/28% zero-shot reach/grasp/place and its 83% real grasp, 5.2× cheaper than collecting data per hand, real-time (Multi-Sensory Sparse Experts cuts compute 42.6%).
> Falsifiers: if a joint-space/graph policy (GET-class) with equal data matches the cycle transfer on an unseen distinct hand, intent is not the invariant; if the three encodings tie at reorient, the choice does not matter.

**Why**: Single-weight policies already transfer across morphologies (GET zero-shots to 10 hand configs, DexFormer controls 32 variants), DexFormer via implicit history-conditioning, GET via graph-joint-space. (D1: the cycle; A2: the grasp.)

**First-principles**: *Principle:* control intent is a plan independent of the hand; the torques are not. *Challenged:* the consensus leaves open which parameterization carries the cycle, especially at reorientation. *Wager:* it may vary by phase; none unifies the cycle across hands.

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

**Why**: Tactile is only an interface to the privileged state it encodes, so a *real* privileged sensor can replace a *simulated* one as the distillation target. Sim-to-real avoiding the sensor sim is settled (AnyRotate, CoRL'24, no tactile sim); PTLD's object-pose-state interface is a distinct, untested alternative. (D2 is E1's Route-2 specialized to reorientation.)

**First-principles**: *Principle:* tactile is only an interface, the policy needs the privileged *state* it encodes. *Challenged:* AnyRotate refuted "needs accurate tactile sim" in 2024; the wrong assumption is contact-features are the only no-sim route. *Wager:* object-pose-state is task-complete; contact-features are lossy.

**Sharpest questions**: 1) Does object-pose-state beat contact-feature *and* tactile-sim three-way on the same reorientation task under matched perturbations? 2) Under perturbation, does tactile hold better under slip while vision holds better under lighting (a modality-vs-perturbation split)? 3) Does DexSkin's cross-sensor calibration generalize the PTLD estimator across tactile hardware without re-collecting privileged pairs?

> [!warning] Risks
> - Instrumented real cell needed (PTLD requires a privileged sensor) → a one-time cost, not a deployment dependency.
> - Privileged-real distillation may not generalize beyond training objects → keep to distribution; H3 tests cross-hardware.
> - Tactile vs visual may be task-dependent → report the modality-vs-perturbation split (slip favors tactile, lighting vision).

### D3: Exploration-Driven Emergent Dexterity
> [!abstract] The bet
> For high-DoF hands, RL with diverse start states, no demos, no task-specific reward, produces *emergent multi-phase* dexterity, not a curriculum aimed at one goal. It transfers zero-shot at OmniReset's 25% real (vs 4% for demo-DP).
> Also split the action into task-space and joint-space (Hierarchical RL-QP Grasp / Hierarchical Reactive Grasping), reaching 81.4% in sim (vs 13.2% for a monolithic policy), with 22/26 unseen objects in the real world.
> Falsifier: if a fixed-reset policy with the same compute and a shaped reward matches the diverse-reset *emergence at high DoF*, the real lever is reward and compute, not reset diversity.

**Why**: Long-horizon exploration is gated by *initial-state diversity*, not reward shaping; a behavior is discoverable only if its precursor states are visited. The reset-as-lever principle is old (Reverse Curriculum Generation, 2017). Undone: demonstration-free, task-agnostic, *high-DoF* multi-phase dexterity at scale, where OmniReset names the wall (saturation despite more compute).

**First-principles**: *Principle (credit the lineage):* exploration coverage is set by the initial-state distribution, not reward shaping, the 2017 Reverse Curriculum / RFCL / Example-based Resets principle. *Challenged:* the assumption that it only yields curriculum-to-single-goal. *Wager:* the novelty is the instantiation at high DoF.

**Sharpest questions**: 1) Does task-agnostic reset diversity produce *emergent multi-phase* behavior the goal-directed curriculum lineage does not, at matched compute? 2) Does task-RL + joint-QP decomposition recover the 81.4%-vs-13.2% gap and transfer better to unseen objects? 3) Can a VLM scaffold (keypoint/wrist priors) replace reset-design *and* reward-design (81% over 8 tasks)?

> [!warning] Risks
> - Reset diversity may need task knowledge (defining "near-object/near-goal") → test whether generic diversity suffices; report reset-vs-reward design.
> - Sim-to-real for emergent policies is fragile (OmniReset's 25% real) → frame as a zero-shot floor; couple to DRIS/DeXtreme and Q2RL refinement.
> - Emergent behaviors may be unsafe (exploration can damage contacts) → bound with D4's QP/force-safety; report contact-force statistics.

### D4: Force-Safety-Constrained Dexterous Control
> [!abstract] The bet
> Put a hard gentle-force filter on top of a learned dexterous policy. It clamps contact force below DexSkin's 1.53 kPa / Multi-Sensory Sparse Experts' ~10 N, with *zero* force violations.
> It also beats the soft-penalty approach (Stress-Guided RL, 36.5% stress cut) at *matched* SR, keeps Hierarchical RL-QP Grasp's 81.4% (vs 13.2% unconstrained), and stays steerable zero-shot.
> Falsifier: if a soft-penalty policy (Stress-Guided RL-class) matches the hard filter on *both* SR and force-violation rate at matched fragile-object integrity, the hard filter buys nothing over a penalty.

**Why**: Safety is a hard constraint on contact-force that must hold *every* step; a learned policy only softly penalizes violations, a physics-based filter guarantees them. The *generic* hard-filter-beats-soft-penalty claim is settled (Safe Steerable Geometric Policy hard-enforces force-*closure*), but existing filters enforce closure and collision, never a force-magnitude *ceiling* for fragile objects.

**First-principles**: *Principle:* a gentle-force constraint (force ≤ a fragile tolerance, ~1.53 kPa / ~10 N) is an *upper* bound, the opposite of force-*closure*. *Challenged:* the consensus filters enforce closure; the fragile ceiling stays soft-penalized (Stress-Guided RL). *Wager:* an upper bound holds only by hard projection.

**Sharpest questions**: 1) Does a hard force-magnitude projection drive force-violation to zero on fragile objects *while matching* the soft-penalty SR? 2) Does projecting onto a force-bounded set (1.53 kPa) preserve fragile-object integrity better than penalty-training at matched SR? 3) Can the QP/force-bound filter make D3's emergent or D1's transferred policies deployable without retraining?

> [!warning] Risks
> - QP clamping can hurt task SR → report the safety-vs-SR trade-off; clamp rarely.
> - Force tolerances are object-specific (1.53 kPa for berries ≠ rigid assembly) → make the bound per-object (A1/A3); no global limit.
> - Hard constraints may over-restrict emergent behavior (transient high forces may be needed) → test over emergent policies; allow needed force, block damage.

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

**First-principles**: *Principle:* force is a physical quantity, so a force-grounded encoder is invariant by construction (UniForce confirms it, z5↔Fz r=−0.74). *Challenged:* invariance is settled, but every prior result tests with the sensor seen or reports perception accuracy. *Wager:* unknown is whether it *scales* with added sensors.

**Sharpest questions**: 1) Does held-out-policy-SR retention rise monotonically with training-sensor diversity under a strict N−1 sweep, clearing ≥80% by a small N? 2) Is policy-SR the load-bearing metric (does a sensor clearing 81.94% inter-sensor *classification* still lose deployable policy-SR)? 3) Does a single force-invariant latent (UniForce) beat a per-sensor-encoder trunk (Transferable Tactile Transformer) on the held-out sensor?

> [!warning] Risks
> - Fundamental sensor incompatibility (capacitive vs piezoresistive vs vision-tactile) → ground to the physical force vector, not raw output; report what is lost.
> - Recursive data problem (SSL needs many sensors, missing *because* transfer is the bottleneck) → bootstrap from UniForce's force-equilibrium corpus plus Sparsh-X.
> - Retention may plateau below 80% (a visual-to-tactile floor) → run the N−1 *policy-SR* sweep first as the go/no-go.
