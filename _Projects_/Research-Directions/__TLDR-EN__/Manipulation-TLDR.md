---
title: "TL;DR: Manipulation — Grasping, Contact, Coordination, Dexterity"
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

# TL;DR: Manipulation — Grasping, Contact, Coordination, Dexterity

> [!info] What this is
> A skimmable TL;DR of [[Manipulation|Manipulation — Grasping, Contact, Coordination, Dexterity]]. Per direction: **the bet**, the reasoning, the sharpest open questions, the risks. Full detail (related-work tables, all hypotheses, benchmarks) stays in the source. Plain-language version: [[Manipulation-ELI5|ELI5]].

> [!abstract] Overview
> What separates manipulation from every other robot skill is the **contact state** — which surfaces press the object, with what force, in what mode — a latent the policy must *regulate*, not a label it reads off vision. The field's reflex is to scale (more grasp data, more demos, bigger policies), but contact has structure that scaling moves the wrong axis on: a stable grasp is not a functional one, force arrives too late to react to, contact dynamics jump at the friction-cone edge, and two arms coordinate through forces vision cannot see. The editorial bet: **contact is structure to model, compose, and bound — not data to collect.** Directions that put the contact state into the loss, the action space, or the constraint win where more teleoperation does not.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A — Grasping & Grasp Synthesis | A1–A3 | Generating *task-relevant, feasible* grasps that transfer across objects and morphologies |
| B — Contact-Rich Assembly & Precision | B1–B2 | Sub-millimeter contact where vision is blind and the policy is open-loop |
| C — Bimanual & Dual-Arm Coordination | C1–C3 | Two-arm coupling is non-factorizable and bimanual data is scarce |
| D — Dexterous & In-Hand Control | D1–D4 | Multi-fingered contact is high-DoF, discontinuous, sim-to-real-fragile |
| E — Tactile Foundations & Data Substrates | E1–E2 | Contact-rich, multi-modal data scarcity (4-order gap vs OXE) — the substrate A–D consume tactile *from* |

## A — Grasping & Grasp Synthesis
*Generating task-relevant, physically feasible grasp poses that transfer across object categories and hand morphologies — including the case where the grasp-pose itself is ill-defined and the gripper must create the contact rather than find it.*

### A1 — Task-Affordance-Conditioned Grasp Synthesis
> [!abstract] The bet
> Task-affordance is the cross-morphology invariant and grasp quality is product-separable. (1) An affordance-conditioned generator transfers parallel-jaw→dexterous (SynGrasp-1B→Dex1B) with ≥10 pp less degradation than the stable-grasp geometry; (2) a product scorer $Q(g)=Q_{\text{stable}}(g)\cdot Q_{\text{task}}(g)$ recovers ≥93% of manual-annotation success (AffordSim's oracle) with zero per-object labels, at Dex1B-class stability (86.0% DexGraspNet). Falsifier: if affordance transfer degrades as much as geometry, *or* the product score lands <93% of the oracle, affordance is just a selection signal.

**Why** — The grasp that *holds* a hammer is not the grasp that *uses* it, yet the dominant recipe optimizes only a stable hold and scales it, so functionally-wrong grasps stay stable and get selected. Affordance-as-conditioning is now settled (AffordDexGrasp, AffordGrasp, Grasp-as-You-Say all condition the generator); what is unproven is *what affordance buys that geometry cannot*. It challenges the assumption that conditioning's gain is mere task-specific selection — versus being morphology-invariant and separable.

**First-principles** — *Principle:* a grasp's correctness is fixed by the task, and *what an object is for* is hand-agnostic while the geometry realizing a hold is hand-specific. *Challenged:* the conditioning crowd (AffordDexGrasp, AffordGrasp) treats affordance as per-task selection, never as the invariant or as separable $Q$. *Wager:* a hammer is gripped by the handle whether the hand has two fingers or five, so task-affordance should transfer across hands and factor out the oracle label-free.

**Sharpest questions** — 1) Does a product score $Q_{\text{stable}}\cdot Q_{\text{task}}$ recover ≥93% of manual annotation with zero per-object labels? 2) Does an affordance-conditioned generator transfer parallel-jaw→dexterous with less degradation than stable geometry? 3) Can language reasoning (GraspMAS/PALM) supply the affordance map as well as a trained VoxAfford, closing the open-vocab loop with no grasp labels?

> [!warning] Risks
> - Affordance accuracy is the ceiling (VoxAfford accuracy is the primary success factor) → bound to tasks where the affordance model is reliable; report the affordance-quality vs grasp-success curve.
> - Stable-grasp regression is already strong (~90% generic) → score on affordance-critical tasks (pouring, hanging, tool-use) where the 15%→79% gap lives, not averaged over easy tasks.
> - Affordance and stability can conflict → make $Q$ a tunable product, not a hard constraint; expose the trade-off as a Pareto front.

### A2 — Cross-Morphology Grasp Transfer
> [!abstract] The bet
> A discrete grasp-taxonomy latent (power/precision/lateral type + continuous force) transfers grasp-establishment to unseen hands *better* than continuous FAAS at matched data, beating UniDex's 60%/40% zero-shot, because the discrete bottleneck strips the hand-specific residue continuous spaces retain — at ≥5× lower per-hand cost (UniDex 5.2×) and DexUMI-class in-domain SR (86%). Falsifiable two ways: if the discrete latent loses to continuous FAAS on the held-out hand, continuous function-space already captures the invariant; and if a joint-space policy with equal data matches *either* on a held-out hand, the invariant is not function at all.

**Why** — A grasp's *function* (oppose, enclose, pinch) is the same across hands; only the joint-space geometry differs. Function-space transfer is no longer the open question (Cross-Embodiment DexGrasp's eigengrasps, DexGrasp-Zero's 85%/82% zero-shot, DexUMI's 86% all establish it). It challenges the live assumption that *continuous* function-space is the right invariant — Sparse Taxonomy Grasp built a discrete-taxonomy stack but only for controllability, never as a transfer bottleneck.

**First-principles** — *Principle:* a grasp is defined by which surfaces press the object at what force, not by joint angles; grasp *type* is the low-dimensional invariant. *Challenged:* the continuous-function-space consensus (UniDex's FAAS, eigengrasps) never tested whether a discrete bottleneck transfers better. *Wager:* a discrete grasp-taxonomy forces out hand-specific residue that continuous spaces retain, so it should be the cleaner cross-hand carrier.

**Sharpest questions** — 1) Does a discrete power/precision/lateral latent beat continuous FAAS on zero-shot transfer to a held-out hand (Oymotion/Wuji) at matched data? 2) Does re-parameterizing DexJoCo's degrading multi-task setup in function-space convert the 50.4%→20.0% degradation into a positive transfer curve? 3) Do exoskeleton-normalized demos (DexUMI) beat kinematic retargeting for cross-hand SR at matched volume?

> [!warning] Risks
> - Function-space loses fine dexterity → use function-space for grasp-establishment, a joint-space residual for fine in-hand (couples to D1).
> - 40–60% transfer is not deployment-ready (UniDex's Wuji 40%) → frame as a few-shot seed; report the few-shot curve from the 40% baseline.
> - Negative-transfer risk (DexJoCo shows multi-hand training can degrade) → the degradation-vs-transfer test is the go/no-go before scaling to many hands.

### A3 — Deformable-Object Grasping under Ill-Defined Contact
> [!abstract] The bet
> Dense tactile + a differentiable soft-body world model *beats the vision-only stress-RL solution* (Stress-Guided RL) on **held-out / unseen** deformables, not just the training set: (H1) it holds where rigid-grasp estimators have no target; (H2) dense tactile beats sparse on *control SR* (not just discrimination) by ≥10 pp; (H3) the differentiable soft-body model beats model-free stress-RL on unseen objects; matching DexSkin's 90% pressure reduction / 20%→60% integrity in-distribution. Falsifier: if vision-only stress-RL ties dense-tactile+soft-body on held-out deformables, the distinctive substrate buys nothing over reactive vision.

**Why** — A towel, sponge, or blueberry has no canonical grasp-pose — contact is something the gripper *produces*, so the "right" grasp is force you regulate, not geometry you localize. Force-regulation-beats-pose-selection is now settled (Stress-Guided RL, Force-Regulated Manipulation, DexSkin). It challenges the live assumption that vision + simulated stress is enough: Stress-Guided RL deliberately omits tactile sensors and any differentiable soft-body control model, untested on held-out deformables.

**First-principles** — *Principle:* for a deformable, the contact state is a continuum the effector *produces*; shape under contact is a function of the applied force field. *Challenged:* Stress-Guided RL bets reactive vision (RGB-D + PointNet, MPM only as a train-time stress oracle) suffices, with no tactile and no soft-body control model. *Wager:* dense tactile measures the force field directly and a differentiable model predicts where it heads — both upstream of vision, so they should extrapolate where reactive vision does not.

**Sharpest questions** — 1) Does dense tactile translate to *control SR* (≥10 pp on held-out deformables), not just t-SNE separation, beating the vision-only solution? 2) Does a differentiable MPM/soft-body twin beat model-free stress-RL on unseen soft objects? 3) Where does folding-as-task-completion (Instant-Fold, 60.9% zero-shot) sidestep force-regulation entirely?

> [!warning] Risks
> - No canonical success metric ("did it grasp" is ill-defined for cloth) → adopt task-completion (fold, pack) + force-bound (integrity) jointly; do not report grasp-SR.
> - Dense tactile optimization is unsolved (HumanoidVTA shows dense barely beats sparse) → the dense-vs-sparse *control* test is the go/no-go; if it does not translate, the bet narrows to force-regulation without dense tactile.
> - Soft-body sim is slow/inaccurate (ManiSkill2 runs ~80 FPS vs ~2000 rigid) → bound physics claims to validated twins (r > 0.9, Real-to-Sim GS).

## B — Contact-Rich Assembly & Precision
*Sub-millimeter contact — insertion, assembly, precision — where vision is blind to the contact state, the policy is open-loop, and the in-distribution benchmark is already saturated, so the bet moves onto the prediction delta and out-of-distribution transfer.*

### B1 — Predictive-Tactile Contact Imagination
> [!abstract] The bet
> The world-model gain over a *matched* reactive policy is concentrated at contact-onset and survives sensor removal. (H1) ablating prediction at matched capacity yields DreamTacVLA's +22.3% delta concentrated at onset steps, not flat; (H3) deploying with *imagined* tactile in place of the sensor recovers most of sensor-on SR on vision/action-correlated contact; under perturbation, OmniVTA-class 60 Hz holds 60–63% SR — not the saturated 95.0% absolute. Falsifier: if a matched reactive policy ties the world-model policy on the delta *and* the gain is flat across phases, prediction adds nothing reaction cannot.

**Why** — The field consumes force as a *current* observation, but reactive feedback arrives only *after* contact — by the time bad force is felt, the misalignment already happened (three surveys name this unresolved). Predict-then-act is now co-discovered consensus (VT-WM, VTAM, the 2019 Deep Tactile MPC root). It challenges the assumption that the WM's gain is *uniform* and *sensor-bound* — no predict-then-act paper isolates whether the gain concentrates at onset and whether imagined tactile can replace the absent sensor.

**First-principles** — *Principle:* the next-step tactile signal is a deterministic consequence of the action given the contact state — it is forecastable. *Challenged:* the action-conditioned-tactile-WM crowd (VT-WM, VTAM, Deep Tactile MPC) plans toward goal tactile states but never runs the matched reactive-vs-predictive delta, phase-stratified at onset. *Wager:* a policy that predicts force can pick the action with the better imagined outcome *before* committing.

**Sharpest questions** — 1) Is the +22.3% world-model gain concentrated at contact-onset steps rather than flat across phases? 2) Does a policy trained with tactile but deployed using *imagined* tactile recover most of sensor-on SR (couples to E1)? 3) Does forecasting a sensor-agnostic latent (TaF-VLA / Sparsh-X) keep the delta across different deployment sensors?

> [!warning] Risks
> - Prediction may plateau at the noise floor (micro-slip is not in the action-conditioned model) → bound the claim to vision/action-correlated contact; report where imagined tactile diverges from measured.
> - World-model latency vs reflexive budget (must fit OmniVTA's 60 Hz loop) → the horizon-vs-frequency ablation is the feasibility gate; cap the horizon to what runs in-budget.
> - Sim tactile is non-standard → use OmniVTA's OmniViTac + SPARR-style real residual; cross-ref Sim2Real.

### B2 — Contact-Mode-Conditional Precision & Reversibility
> [!abstract] The bet
> A policy that reads a 5-state *physical* contact-mode latent ($c_t \in \{\text{free, making, in-contact, sliding, breaking}\}$) and switches *dynamics* per mode (a) transfers to *unseen* tasks beyond MATCH's single-task in-distribution result — at SPARR's +74.5% relative SR / 36.5% cycle-time cut on held-out NIST, below FAVLA's 7.7 N peak — and (b) exposes a **mode-derived reversibility gate** that cuts wedge-failures a binary-contact or mode-blind policy cannot. Falsifier: if a binary-contact policy (MATCH-class) with equal capacity ties the 5-state one on unseen NIST *and* matches its wedge-failure rate, the physical-mode latent is redundant over a contact bit.

**Why** — Insertion *is* a sequence through discrete contact modes (REASSEMBLE shows force-torque reveals phase-distinct patterns), yet most policies treat it as one continuous map. Discrete-mode structure is partly explored (MATCH switches control law via a binary bit, PhaForce schedules a phase belief), but none expose a 5-state physical-mode latent that switches *dynamics*, nor a reversibility gate. It challenges the assumption that a *binary* contact/free switch is enough.

**First-principles** — *Principle:* contact dynamics jump at boundaries (friction-cone edge, force spike, stick→slip), so the right latent is a physical-mode label that switches the *dynamics model*, not a controller. *Challenged:* MATCH collapses contact to one bit and avoids breaks via force control, never modeling slip-stick/wedge or reversibility. *Wager:* only a physical-mode label tells you whether a corrective retreat is reversible — a `making` retreat is safe, an `in-contact` one may be wedged.

**Sharpest questions** — 1) Does a 5-state mode latent beat MATCH's binary bit and FAVLA's implicit frequency on *unseen* NIST transfer? 2) Does gating corrective retreats on the mode cut wedge-failures a binary/mode-blind policy cannot avoid? 3) Can a mode classifier distilled from REASSEMBLE phase annotations + sim reach usable accuracy without dense real mode labels?

> [!warning] Risks
> - Discrete-latent optimization variance (Gumbel-softmax/REINFORCE is high-variance) → anneal soft→hard; start continuous, harden over training.
> - Mode supervision needs ground truth → distill from REASSEMBLE's phase annotations + sim contact; report mode-classification accuracy first (the gate).
> - Saturated headline (SPARR is already 95–100% on AutoMate) → show the win on *unseen* NIST transfer + peak-force bound + reversibility, never on in-distribution SR.

## C — Bimanual & Dual-Arm Coordination
*Two-arm manipulation where the cross-arm coupling is non-factorizable and bimanual demonstration data is scarce — composing single-arm priors, generating data with coordination structure, and sensing the inter-arm force that vision cannot see.*

### C1 — Coordination-Native Bimanual Policies
> [!abstract] The bet
> The coupling has measurable structure and a localizable breakdown that composition exposes and a monolith cannot. (H2) the coupling's data-floor stays near TwinVLA's ~50 episodes even on BiCoord's 4×-harder tightly-coupled tasks; (H3) a DexMimicGen-typed (async/sync/ordered) coupling beats one Joint-Attention layer on tightly-coupled subtasks; (H4) BiCoord's later-stage degradation localizes to the *coupling* (single-arm skill stays strong) — at composition's data-cost (TwinVLA 76% / ~25 H100-days). Falsifier: if the coupling's data-floor rises sharply on harder tasks *and* typed coupling ties one layer, the coupling is unstructured and the story ends at the settled headline.

**Why** — Two-arm value is non-additive, but each arm's *skill* is an abundant transferable single-arm prior. Composition-beats-monolith is now settled across different coupling primitives (TwinVLA's attention, EnergyAction's energy functions, SkillVLA's skill-recompose, Decoupled Bimanual already ran the falsifier at +23.5% / 1/6 size). It challenges the live assumption that the coupling is *structureless and cheap everywhere*.

**First-principles** — *Principle:* the whole splits into a transferable single-arm skill and a two-arm coupling; only the coupling needs two-arm data. *Challenged:* the composition consensus shows the factorization works but no paper has shown whether the coupling's data-floor holds on 4×-harder tasks, whether typed coupling beats one layer, or whether late-degradation is coupling- or skill-localized. *Wager:* the coupling has its own data-floor, type-structure, and failure mode, separable from the skill.

**Sharpest questions** — 1) Does the coupling reach TwinVLA's ~50-episode result even on BiCoord's 4×-harder tightly-coupled tasks? 2) Does conditioning the coupling on DexMimicGen's async/sync/ordered subtask type beat one Joint-Attention layer? 3) Does BiCoord's later-stage degradation localize to the coupling (freeze single-arm priors, vary only the coupling)?

> [!warning] Risks
> - Composition may cap the coordination ceiling (handover + force balance may exceed composed priors) → bound to loosely-to-moderately-coupled tasks; report the coupling-tightness-vs-SR curve.
> - Joint Attention is one design (TwinVLA's causal-masked attention may not be optimal) → the typed-coupling ablation tests alternatives.
> - Single-arm priors must be strong → validate base SR first; the bet assumes π0/RDT-class priors exist.

### C2 — Scalable Bimanual Data Generation with Coordination Structure
> [!abstract] The bet
> Stripping coordination structure at matched volume collapses the result — the front-line *prediction*, not the achieved SR. (H1) raw SE(3) replay at the same trajectory count drops DexMimicGen's 90%-from-40 by ≥30 pp, with the cleanest isolation on a *differentiable* generator (D-CODA / CRAFT, whose Canny-conditioning ablation already shows 21.6% vs 10.3%); structured generation otherwise reaches RoboTwin 2.0's +24.4% few-shot. Falsifier: if raw SE(3) replay at matched volume keeps the 90% from 40 demos, the structure adds nothing volume could not, and the consensus result was a volume effect mislabeled as structure.

**Why** — RoboTwin 2.0 names the dual-arm data wall, and structure-aware generation is now settled (MoMaGen subsumes the X-Gen family and deploys from one demo; DexMimicGen, BiDemoSyn, CRAFT instantiate it). But the SR numbers are *achieved*, not predicted — no generator isolates whether the gain comes from coordination *structure* or simply the *volume* the structure unlocks. It challenges the assumption that the achieved SR *proves* structure-carries-generalization.

**First-principles** — *Principle:* bimanual generalization comes from coordination structure (per-arm subtasks with sync/ordering), not sheer volume. *Challenged:* MoMaGen and the X-Gen family assert structure-carries-generalization but never strip structure at matched volume; the causal claim is asserted, not measured. *Wager:* if the principle holds, raw SE(3) replay at matched volume must collapse the result; if SR holds without it, the gain was volume all along.

**Sharpest questions** — 1) Does stripping sync/ordering (raw SE(3) replay) at matched volume drop the 90%-from-40 by ≥30 pp, cleanest on a differentiable generator? 2) Does MLLM expert-code (RoboTwin 2.0) capture *coordinated* trajectories better than demo-replay on tightly-coupled tasks? 3) Does physics-grounded generation (PGDG) beat kinematic replay where contact validity matters?

> [!warning] Risks
> - Generated data may miss tight coupling (replay can produce parallel-but-not-coordinated trajectories) → the BiCoord late-degradation test is the gate; couple generation to C1's coupling-aware training.
> - Sim-to-Real Cliff (RoCo Challenge shows sim policies are brittle) → use RoboTwin 2.0's 5-axis randomization + TAMEn filtering; cross-ref Sim2Real.
> - MLLM code-gen reliability (RoboTwin 2.0's 71.3% auto-code → ~29% needs refinement) → keep human-in-the-loop verification; report generation-yield, not just downstream SR.

### C3 — Tactile-Coupled Bimanual Cooperation
> [!abstract] The bet
> A *shared* inter-arm force channel beats per-arm fusion on holding-while-manipulating by ≥10 pp SR, and an explicit force-*balance* loss beats tactile-as-input on force-balanced handover. (H1) shared > per-arm (VT-Refine/TAMEn-class) on hold-and-manipulate; (H3) lifting Symmetry-Aware VT Fusion's balance loss from two fingers to two arms beats tactile-as-input on handover; reaching TAMEn's 75% contact-rich SR using VTouch++'s synchronized data. Falsifier: if per-arm fusion ties the shared channel on holding-while-manipulating *and* the balance loss ties tactile-as-input on handover, neither sharing nor balance is the missing structure.

**Why** — Force-balanced cooperation needs inter-arm force observability vision cannot provide; the two arms sense each other through the object. That tactile beats vision on contact-coupled bimanual is now demonstrated (VT-Refine, 2 mm-clearance assembly). It challenges the live assumption that *per-arm* tactile fusion is enough — VT-Refine's coordination is emergent with no shared force channel, and Symmetry-Aware's balance loss is for two fingers of one gripper, never lifted to two arms.

**First-principles** — *Principle:* when one arm holds and the other manipulates, the cooperation is governed by the force *each arm transmits to the other through the object* — a single shared quantity. *Challenged:* per-arm fusion observes each arm in isolation (VT-Refine emergent, no shared channel); whether the force must be shared and balanced is untested. *Wager:* only a shared representation captures the transmitted coupling, and only an explicit force-balance objective optimizes what the task is about.

**Sharpest questions** — 1) Does a *shared* inter-arm tactile representation beat per-arm fusion by ≥10 pp on holding-while-manipulating? 2) Does lifting the two-finger force-symmetry loss to a two-*arm* balance objective beat tactile-as-input on handover? 3) Does adding the shared tactile channel to C1's TwinVLA beat vision-only Joint Attention on contact-coupled bimanual?

> [!warning] Risks
> - Inter-arm tactile is hard to instrument (both arms need synchronized tactile) → VTouch++ / TAMEn data exist; bound to platforms with bimanual tactile.
> - Dense tactile optimization is unsolved (HumanoidVTA shows dense barely beats sparse) → use Multi-Sensory Sparse Experts' AdaMN normalization to stop force being suppressed.
> - Force-balance reward can over-constrain (penalizing imbalance may block legitimate asymmetric grasps) → make balance tunable; expose the balance-vs-flexibility trade-off.

## D — Dexterous & In-Hand Control
*Multi-fingered hands performing high-DoF, contact-discontinuous, sim-to-real-fragile manipulation — making control intent hand-agnostic, bridging tactile sim-to-real without a tactile simulator, unlocking emergent dexterity through exploration, and bounding contact force with a hard constraint.*

### D1 — Universal Cross-Morphology Hand Control
> [!abstract] The bet
> One backbone unifies the *full* reach→grasp→reorient→place cycle across distinct hands (which GET cannot — it is in-hand rotation across configs of *one* hand; DexWM spans the cycle but on one hand family), and at the reorientation phase explicit-intent (FAAS), implicit-history (DexFormer), and graph-structure (GET) parameterizations differ measurably — best matching DexWM's 72%/58%/28% zero-shot reach/grasp/place and 83% real grasp, 5.2× cheaper than per-hand collection, at real-time latency (Multi-Sensory Sparse Experts 42.6% compute cut). Falsifier: if a joint-space/graph policy (GET-class) with equal data matches the cycle transfer on an unseen *distinct* hand, intent is not the invariant; if the three parameterizations tie at reorientation, the choice does not matter.

**Why** — Dexterous *control intent* (which contacts to form, what in-hand motion) is hand-agnostic; only the actuation is hand-specific. Single-weight policies already transfer across morphologies (GET zero-shots to 10 hand configs, DexFormer controls 32 variants). It challenges the live assumption that *explicit* intent (FAAS) is necessary — DexFormer's implicit history-conditioning transfers without it, and GET transfers via graph-joint-space. (D1 owns the in-hand control cycle after the grasp; A2 owns the grasp — distinct phases.)

**First-principles** — *Principle:* control intent is a plan independent of the hand; the joint torques that carry it out are not. *Challenged:* the intent-transfer consensus (DexFormer states it verbatim, GET and UniDex transfer) leaves open which parameterization carries the full cycle, especially at reorientation. *Wager:* the right parameterization may differ across reach/grasp/reorient/place phases, and no system unifies the full cycle across distinct hands.

**Sharpest questions** — 1) Does intent-space transfer the full reach/grasp/place cycle on a held-out *distinct* hand where GET's graph-joint-space (rotation, one hand) does not? 2) Do explicit-intent, implicit-history, and graph-structure parameterizations differ measurably *at reorientation*? 3) Does intent for the plan + a per-hand joint-residual for fine actuation beat either alone?

> [!warning] Risks
> - Intent-space loses fine dexterity → intent + joint-residual split; bound intent-space to contact-establishment.
> - 40–60% transfer is not deployment-ready (UniDex's Wuji 40%) → frame as a few-shot seed; report the few-shot curve.
> - MoE may not specialize by hand → test routing-by-hand empirically before claiming MoE solves cross-morphology scaling.

### D2 — Tactile In-Hand Reorientation with Sim-to-Real
> [!abstract] The bet
> The privileged object-pose-state interface (PTLD) beats both the contact-feature interface (AnyRotate) and a tactile-sim pipeline (Force-Based Sim2Real) on the *same* reorientation task under matched perturbations — reaching PTLD's +182% rotation / +57% goals, DeXtreme's 27.8-vs-14.8, and holding under ViserDex's adversarial lighting (~25). Falsifiable two ways: if the contact-feature interface ties the object-pose-state one, the cheaper interface wins; if a tactile-sim pipeline matches either, the simulator was never the bottleneck.

**Why** — Tactile is only an interface to the privileged state (object pose, shape) it encodes, so a *real* privileged sensor can replace a *simulated* tactile sensor as the distillation target. That tactile sim-to-real can avoid simulating the sensor is now settled (AnyRotate, CoRL'24, bridges with no tactile sim). It challenges the assumption that AnyRotate's contact-feature interface is the only no-sim option — PTLD's object-pose-state interface is a distinct, untested alternative. (D2 is the in-hand sibling of E1's Route-2 distillation, specialized to reorientation.)

**First-principles** — *Principle:* the hard part of tactile sim-to-real is the *simulator*, but tactile is only an interface — the policy needs the privileged *state* it encodes. *Challenged:* AnyRotate refuted "needs accurate tactile sim" in 2024; the live wrong assumption is that the contact-feature interface is the only no-sim route. *Wager:* the object-pose-state is task-complete where the contact-feature is lossy and the sim is biased, so the interface choice — not the simulator — is the live variable.

**Sharpest questions** — 1) Does object-pose-state beat contact-feature *and* tactile-sim three-way on the same reorientation task under matched perturbations? 2) Under perturbation, does tactile hold better under slip while vision holds better under lighting (a modality-vs-perturbation split, not a universal winner)? 3) Does DexSkin's cross-sensor calibration generalize the PTLD estimator across tactile hardware without re-collecting privileged pairs?

> [!warning] Risks
> - Instrumented real cell needed (PTLD requires a privileged-sensor setup) → this is a one-time data-collection cost, not a deployment dependency; report it explicitly.
> - Privileged-real distillation may not generalize beyond training objects → bound to the object distribution; H3 tests cross-hardware.
> - Tactile vs visual may be task-dependent → report the modality-vs-perturbation-type split (slip favors tactile, lighting favors vision), not a single number.

### D3 — Exploration-Driven Emergent Dexterity
> [!abstract] The bet
> At high DoF, demonstration-free task-agnostic diverse-reset RL yields *emergent multi-phase* dexterity (not curriculum-to-single-goal) transferring zero-shot at OmniReset's 25% real (vs 4% demo-DP), and task-space/joint-space decomposition (Hierarchical RL-QP Grasp / Hierarchical Reactive Grasping) reaches 81.4% sim (vs 13.2% monolithic) with 22/26 unseen-object real. Falsifier: if a fixed-reset policy with matched compute and a shaped reward matches diverse-reset *emergence at high DoF*, the lever is reward/compute after all, not reset diversity.

**Why** — Long-horizon exploration is gated by the *initial-state diversity* the agent sees, not by reward shaping — a behavior is discoverable only if its precursor states are visited. The reset-as-lever principle is old (Reverse Curriculum Generation, 2017). What is undone: demonstration-free, task-agnostic, *high-DoF* dexterity emerging multi-phase at scale, where OmniReset names the wall ("performance saturation despite increased compute"). It challenges the assumption that high-DoF dexterity needs hand-crafted curricula/rewards.

**First-principles** — *Principle (credit the lineage):* exploration coverage is set by the initial-state distribution, not reward shaping — the 2017 Reverse Curriculum / RFCL / Example-based Resets principle, not a fresh discovery. *Challenged:* the assumption that the principle only yields curriculum-to-single-goal; OmniReset's diverse resets instead yield emergent multi-phase behavior. *Wager:* D3's novelty is the instantiation (emergence at high DoF), not the principle.

**Sharpest questions** — 1) Does task-agnostic reset diversity produce *emergent multi-phase* behavior the goal-directed curriculum lineage does not, at matched compute? 2) Does task-RL + joint-QP decomposition recover the 81.4%-vs-13.2% gap and transfer better to unseen objects? 3) Can a VLM scaffold (keypoint/wrist priors) replace reset-design *and* reward-design (81% over 8 tasks)?

> [!warning] Risks
> - Reset diversity may need task knowledge (defining "near-object/near-goal" is itself a design choice) → test whether generic reset diversity suffices; report reset-design vs reward-design effort.
> - Sim-to-real for emergent policies is fragile (OmniReset's 25% real is low) → frame as a zero-shot floor; couple to DRIS/DeXtreme randomization and Q2RL on-robot refinement.
> - Emergent behaviors may be unsafe (unconstrained exploration can damage contacts) → bound with D4's QP/force-safety; report contact-force statistics during emergent rollouts.

### D4 — Force-Safety-Constrained Dexterous Control
> [!abstract] The bet
> A fragile gentle-force *hard projection* over a learned dexterous policy bounds contact force below DexSkin's 1.53 kPa / Multi-Sensory Sparse Experts' ~10 N with *zero* force-violation, and beats the soft-penalty Stress-Guided RL (36.5% stress cut) at *matched* SR — keeping Hierarchical RL-QP Grasp's 81.4% (vs 13.2% unconstrained) and zero-shot steerability. Falsifier: if a soft-penalty policy (Stress-Guided RL-class) matches the hard projection on *both* SR and force-violation rate at matched fragile-object integrity, the hard projection buys nothing over a penalty.

**Why** — Safety is a hard constraint on the contact-force state that must hold *every* step; a learned policy can only softly penalize violations, a physics-based filter can guarantee them. The *generic* hard-filter-beats-soft-penalty claim is now settled (Safe Steerable Geometric Policy hard-enforces force-*closure*). It challenges the live assumption that existing hard filters cover *gentle* force — they enforce force-closure and collision, never a force-magnitude *ceiling* for fragile objects (handled only by soft penalties).

**First-principles** — *Principle:* a gentle-force constraint (force ≤ a fragile tolerance, ~1.53 kPa / ~10 N) is an *upper* bound — the opposite of force-*closure*, which pushes force toward the max needed to hold a grasp. *Challenged:* the consensus hard filters (Safe Steerable Geometric Policy) enforce force-closure, never a ceiling; the fragile ceiling stays soft-penalized (Stress-Guided RL). *Wager:* an upper bound can be guaranteed only by a hard projection over the learned action, never by an expected-reward penalty.

**Sharpest questions** — 1) Does a hard force-magnitude projection drive force-violation to zero on fragile objects *while matching* the soft-penalty SR? 2) Does projecting onto a force-bounded set (1.53 kPa) preserve fragile-object integrity better than penalty-training at matched SR? 3) Can the QP/force-bound filter make D3's emergent or D1's transferred policies deployable without retraining?

> [!warning] Risks
> - QP clamping can hurt task SR (tracking errors from clamping infeasible velocities) → report the safety-vs-SR trade-off; the filter should clamp rarely on feasible tasks.
> - Force tolerances are object-specific (1.53 kPa for berries ≠ rigid assembly) → make the bound a per-object parameter (couples to A1/A3); no single global limit.
> - Hard constraints may over-restrict emergent behavior (transient high forces may be needed) → test the filter over emergent policies; tune to allow task-necessary force while blocking damage.

## E — Tactile Foundations & Data Substrates
*The foundation layer beneath force-aware manipulation that needs no runtime tactile hardware — getting force-awareness to deployment with the sensor dropped, and a cross-sensor representation that makes any such policy portable across the sensor ecosystem.*

### E1 — Sensor-Free Force-Aware Policies
> [!abstract] The bet
> (Route 1 is the front-line falsifiable claim) A force-*objective* policy pretrained on ~20k hr of ego *video alone* — no force/tactile at any stage — reaches ≥80% of a tactile-instrumented policy's SR on ForceVLA's 5 tasks, riding EgoScale's curve to +54% on 22-DoF dexterous, clearing the instrumented bar that the settled Route-2 distillers (FD-VLA 61.1%, HapticVLA 86.7%) already replicate as the parity baseline. Falsifier: if the ego-video-only force-objective policy cannot clear 80% of the instrumented baseline, force-awareness is not learnable without a teacher signal — and Route 2 was the only viable route.

**Why** — Tactile-awareness is a learned behavior grounded in force — the object moves *because* of force, so the awareness is separable from the sensor that taught it. Route 2 (distill a tactile teacher, drop the sensor) is now settled (FD-VLA even beats the with-sensor baseline; ViTacGen, HapticVLA). The unattacked half is Route 1: a force-aware *full policy* pretrained from ego video alone — every ego backbone (EgoScale, Being-H0, DexWM) omits the force head. It challenges the assumption that force-awareness needs a tactile *teacher cell* at training.

**First-principles** — *Principle:* force is *upstream* of vision in contact (the object moves because of force), so vision→force is a well-posed inverse, and the behavior is separable from the supervising sensor. *Challenged:* Route 2 still requires an instrumented teacher; no paper learns force-awareness from ego video alone. *Wager:* if the inverse is well-posed, the supervising signal can be removed not just at deployment (Route 2) but at *every* stage (Route 1).

**Sharpest questions** — 1) Can an ego-video-only force-objective policy clear ≥80% of the instrumented baseline on ForceVLA's 5 tasks, with failures concentrated on vision-uncorrelated slip? 2) Does predicted tactile from ego video (TouchAnything view-dropout + Sparsh-X teacher on a small instrumented fraction) recover real-tactile SR? 3) Does ego-video force-awareness survive the 22-DoF-human → 1–7-DoF-gripper embodiment gap, and which projection (explicit MANO vs keypoint) retains most?

> [!warning] Risks
> - Vision-to-tactile noise floor (Route 1) — subtle slip needs fingertip pressure, not vision → bound to vision-correlated force; report the floor.
> - Distillation gap on novel objects (Route 2) — student may fail where the teacher's tactile was load-bearing → bound to in-distribution contact; report the teacher-student gap per object class.
> - Scaling / instrumentation cost (Route 1's 20k+ hr is expensive; Route 2 needs a teacher cell) → for Route 1, use Sparsh-X as a synthetic-tactile teacher on a small fraction; for Route 2, treat the cell as a one-time cost.

### E2 — Cross-Sensor Tactile Foundation Models for Plug-And-Play Force-Aware Policies
> [!abstract] The bet
> Under a *leave-one-sensor-out* (N−1) protocol where the held-out sensor is unseen *by the encoder*, deployable-policy-SR retention rises with training-sensor *diversity* and clears ≥80% by a small N — beyond UniForce's 90–120% (which saw all 3 sensors) and the TaF-VLA 60.3% family-level ceiling. Falsifier: if held-out-sensor *policy-SR* retention plateaus below 80% regardless of how many sensors the encoder trains on, the ceiling is fundamental (a visual-to-tactile floor), not data-limited — and cross-sensor deployment is bounded.

**Why** — Force is a physical quantity whose representation differs across sensors only in measurement basis, and a force-grounded encoder (UniForce) now exists, transferring zero-shot across vision-based and magnetic sensors. So the open question is no longer "can it transfer?" but the *scaling law*. It challenges the assumption that the *retention scaling law* is already known — every prior result trains with the test sensor *seen*, or reports perception accuracy, never a strict encoder-held-out N−1 sweep against deployable policy-SR.

**First-principles** — *Principle:* force is a physical quantity; a force-grounded encoder is invariant by construction (UniForce confirms it, z5↔Fz r=−0.74). *Challenged:* invariance is settled, but every prior result (UniForce, Sensor-Invariant Tactile, Transferable Tactile Transformer) tests with the sensor seen or reports perception accuracy — the retention scaling law is unproven. *Wager:* the live unknown is whether invariance *scales* — does adding training sensors monotonically raise held-out-policy-SR retention, or does a fundamental ceiling cap it?

**Sharpest questions** — 1) Does held-out-policy-SR retention rise monotonically with training-sensor diversity under a strict N−1 sweep, clearing ≥80% by a small N? 2) Is policy-SR the load-bearing metric (does a sensor clearing 81.94% inter-sensor *classification* still lose deployable policy-SR)? 3) Does a single force-invariant latent (UniForce) beat a per-sensor-encoder trunk (Transferable Tactile Transformer) on the held-out sensor?

> [!warning] Risks
> - Fundamental sensor incompatibility (capacitive vs piezoresistive vs vision-tactile may require discarding task-relevant detail) → ground the representation to the physical force vector rather than raw output; report what detail is lost.
> - Recursive data problem (SSL needs many sensors' data, but data is missing *because* transfer is the bottleneck) → bootstrap from UniForce's force-equilibrium corpus + Sparsh-X's multi-sensor set; treat new sensors as encoder-held-out.
> - Retention may plateau below 80% regardless of diversity (could be a fundamental visual-to-tactile floor) → run the N−1 *policy-SR* retention sweep first as a go/no-go.
