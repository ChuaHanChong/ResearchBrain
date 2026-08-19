---
title: "TL;DR: Whole-Body Coordination, Loco-Manipulation, Mobile Manipulation, Force-Adaptive Control"
aliases:
  - "Whole-Body TL;DR"
  - "Whole-Body skim"
tags:
  - tldr
  - humanoid
  - manipulation
  - loco-manipulation
  - sim-to-real
---

# TL;DR: Whole-Body Coordination, Loco-Manipulation, Mobile Manipulation, Force-Adaptive Control

> [!info] What this is
> A quick TL;DR of [[Whole-Body|Whole-Body Coordination]]. Each direction gives **the bet**, the reasoning, the sharpest questions, and risks. Full detail (related-work, hypotheses, benchmarks) is in the source. Plain-language version: [[__ELI5-EN__/Whole-Body-ELI5|ELI5]].

> [!abstract] Overview
> A humanoid that manipulates *while it moves* faces one fact: arm and legs are mechanically linked. An arm reach pushes back as a torque on the base. Whole-body skill is not "an arm controller plus a leg controller." The bet across 12 directions and 4 clusters: **the link is structure to *predict*, not data to *collect*.** Make it explicit (A). Coordinate it with a moving base (B). Hold it under outside force (C). Get the demo data to learn it (D). Directions that model the link win on a fixed data budget.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A: Whole-Body Loco-Manipulation | A1–A4 | Arm and legs cannot be split. An arm reach is a balance push the legs must expect. Flat RL fails on the linked high-DoF action space |
| B: Mobile Manipulation (Nav↔Manip Coupling) | B1–B2 | A moving base keeps changing what's visible and reachable. The target can leave the frame, and out-of-view state must be remembered, not just factored into the action |
| C: Force-Adaptive Coordination Under Load | C1–C3 | An outside hand wrench travels through the chain to the support polygon. The legs make up for what the arms feel, and the task reward leaves out the force |
| D: Whole-Body Teleoperation & Human-Motion Retargeting | D1, D2–D3 | The data wall. Demos of *coupled* loco-manipulation are scarce, embodiment-mismatched, and per-platform |

## A: Whole-Body Loco-Manipulation
*Linked arm–leg dynamics on a single floating base. Model the coupling term itself (A1). Combine feasible primitives so the action never leaves the feasible set (A2). Close the precision loop in the world frame, base as active transport (A3). Send joint loco+manip commands through one latent interface (A4).*

### A1: Coupled-Dynamics Whole-Body Action Models
> [!abstract] The bet
> Predict the base reaction *explicitly*: $\hat\delta_{\text{base}}=\hat M_{\text{base,arm}}\ddot q_{\text{arm}}$, analytic term plus learned residual, fed as an auxiliary-loss target. Beats HEX's implicit MoE *on the same fixed dataset*, widening the 41.0→61.8 OOD margin by ≥ +3 pp into the mid-60s, most in the top arm-acceleration quartile where SEEC's "arms-are-light" assumption is wrong. Two gates first. *Frontier gate:* check whether the destabilizing arm→base coupling is really *inertial* ($M_{\text{base,arm}}$, which this predicts) or *contact-wrench / support-polygon* (single↔double support, impending slip, which it ignores), by instrumenting contact-state before committing the inertial predictor; if the contact share dominates at the worst instant the term must be reframed as contact-constrained hybrid dynamics. *De-risk gate:* run the arm-acceleration-stratified explicit-vs-implicit ablation on a controllable baseline (FALCON's emergent-coupling policy, or a self-trained MoE) *before* the possibly-closed HEX backbone. Falsifiable: if explicit ≤ 61.8% at matched latency, leave the coupling to the MoE. Regime caveat (mirrors D2): explicit structure likely wins only in the low-data tail, the fine-tuned generalist may win at scale, so publish the crossover boundary rather than claim structure always wins.

**Why**: Separate arm/leg control drops the arm-reach base reaction. We challenge SEEC's "arm→base coupling negligible."

**First-principles**: *Principle:* $M(q)$ is non-block-diagonal, so an arm acceleration *is* a leg-balance push. *Challenged:* SEEC predicts only base→arm; HEX's UPP-removal is its biggest drop (Pouring 11/12 → 6/12), bigger than 12M-frame pretraining. *Wager:* no one predicts arm→base explicitly.

**Sharpest questions**: 1) Is the destabilizing arm→base coupling inertial ($M_{\text{base,arm}}$) or contact-wrench / support-polygon, when you instrument contact-state on a walking biped? 2) On a controllable baseline (FALCON / self-trained MoE), is the explicit-over-implicit margin significant in the top arm-acceleration quartile and ~0 in the bottom, before porting to HEX? 3) Does an explicit base-reaction target on HEX's backbone + dataset lift OOD past 61.8% at matched params, and where is the data/compute crossover past which the generalist overtakes the explicit term?

> [!warning] Risks
> - Inertia model off → residual over a nominal analytic model; report sim-vs-real error.
> - Explicit may not beat implicit → run head-to-head at matched latency, keep the MoE if it wins.
> - Gains platform-specific (79.8%/61.8% is one humanoid) → report margin by motion-aggressiveness class.
> - Explicit coupling adds latency → bound to HiWET-class single-digit-ms; fall back to the MoE.

### A2: Skill-Blending vs Monolithic Whole-Body Control
> [!abstract] The bet
> Run the pipeline-location head-to-head no one has run: three options on one shared 8-task / 3-embodiment skill set with *zero* per-task reward tuning, online convex-blend (SkillBlender), upstream feasible prior (DreamControl-v2), distilled-experts monolith (Experts-to-Generalist 66.84% / HANDOFF 0.31 m³). Prediction: the feasibility-by-construction blend matches SkillBlender's outperformance while the monolith reward-hacks; the upstream prior, as a downstream-RL reference, lifts valid-trajectory rate toward 68% (vs 8%) and RL success toward 0.925 (vs 0.101) *more* than blend-during-control. Falsifiable: a reward-tuned monolith matches the blend without hacking, or location makes no difference.

**Why**: A high-DoF monolith rediscovers feasibility each time; SkillBlender shows per-task reward engineering causes reward hacking. We challenge that whole-body skill needs it.

**First-principles**: *Principle:* a convex combination of feasible primitives never leaves their span, feasibility from the rule, not a reward. *Challenged:* HumanoidBench's "flat RL fails, hierarchy helps"; SkillBlender's softmax-removal collapses feasibility. *Wager:* the pipeline *location* of feasibility is the un-run variable.

**Sharpest questions**: 1) Does a convex-hull blend match both monoliths with one shared reward, over short *and* 8 s episodes? 2) Does an upstream feasible prior beat during-control blending *and* OMG-style post-hoc filtering? 3) Does primitive-library size amortize sub-linearly, and does a learned set beat a hand-designed one?

> [!warning] Risks
> - Frozen primitives cap behavior → norm-bounded learned residual; report how large before reward hacking returns.
> - Primitive-library design is itself engineering → test learned vs hand-designed; report tasks-per-set.
> - Sim-to-real gap (SkillBlender is sim-only) → borrow the diffusion-prior recipe (Bionic runs 125 real trials).
> - Blending may jump → SkillBlender's softmax smooths weights; report jerk/limit diagnostics per AGILE.

### A3: World-Frame End-Effector Tracking with the Base as an Active DoF
> [!abstract] The bet
> Take a *bipedal humanoid with a walking gait* and use a world-frame Commander/Tracker hierarchy with a *learned continuous α-schedule*. Holds HiWET's 12.4 mm sim / 12–15 mm real error over long horizons. Two things follow: (i) a matched body-centric controller's error grows with locomotion distance while world-frame stays flat; (ii) the learned α reaches more out-of-static-range targets than HiWET's tuned-constant α and Spatial Brain Cerebellum's discrete trigger. Falsifiable: a body-centric baseline stays flat with distance, or a tuned-constant α ties the learned schedule.

**Why**: A humanoid placing a hand while walking has its target in the world frame, but most controllers are robot-centric. World-frame-through-base-motion is consensus *on quadrupeds*, unproven on bipeds. We challenge that body-centric control suffices and base motion is a disturbance.

**First-principles**: *Principle:* a manipulation target lives in the world frame, so world-frame closure decouples precision from base-travel distance, and the mobile base brings out-of-static-reach targets into reach. *Challenged:* HiWET's constant α and discrete reach-extenders; its KMP-removal doubles hand error (12.4 → 25.2 mm). *Wager:* the drift is a *frame* problem, not capacity.

**Sharpest questions**: 1) Does body-centric EE error rise with base-travel distance while world-frame stays flat? 2) Does a learned α-schedule reach more out-of-static-range targets than fixed-α and a discrete solver? 3) Does world-frame closure just move the bottleneck into base-state estimation?

> [!warning] Risks
> - Needs accurate base-state estimation → HiWET shows removing the estimator costs ~10 mm; report EE error vs estimation error.
> - Active base transport can destabilize → stack A1's predictor under the tracker; schedule α so reach and balance don't fight.
> - 12.4 mm may not generalize → test over horizon and embodiments; report error by task class and distance.

### A4: Unified-Latent Policy for Joint Loco-Manipulation Commands
> [!abstract] The bet
> The load-bearing test isolates the *command interface*, not the codebook split. A unified loco+manip latent policy beats the strongest decoupled stack (a π0.5/GR00T-class manipulation policy bolted onto a separate velocity controller) at a matched low-level controller: ≥78.0% unified vs ≤56.7% same-LMO decoupled on Bag/Box/Cart, clearing LeVERB's 58.5% (7.8× over naive hierarchical). The mechanism carrying that win is WholeBodyVLA's +24.0% learned-LMO-over-velocity driver, concentrated on tasks with precise locomotion subgoals (squat-to-place) and near-zero on coarse locomotion. The visual-dynamics split is a secondary probe, not the headline: WholeBodyVLA ranks it third behind pretraining and the LMO interface, calling it "beneficial but not the primary factor," though that verdict rests on an aggregate 12.0 pp margin (78.0% vs 66.0%) that could hide a loco-heavy regime where the split matters, the camera-motion stratification against MotionWAM's external unified latent that could overturn it. Falsifiable: the decoupled stack ties the unified policy at a matched controller, or the LMO gain is uniform across subgoal precision.

**Why**: Policies "confined to limited workspaces" "lack integrated humanoid locomotion," and bolting on a velocity controller causes "decision-execution misalignment." "Unified beats decoupled" is consensus; the non-consensus part is that *visual statistics force the architecture*, manipulation video has a near-static camera, locomotion a gait-moving one, needing *separate* latents. We challenge MotionWAM's and Fast-Slow WB VLA's single-latent bet.

**First-principles**: *Principle:* manipulation and locomotion have different visual dynamics, so one shared latent underfits one; yet the next action is a joint over both, and separate stacks re-introduce misalignment. *Challenged:* not the single-shared-latent bet (settled, WholeBodyVLA's separate VQ-VAE latents already beat a shared model, 78.0% vs 66.0%) but whether WholeBodyVLA's own aggregate ranking, the split third behind pretraining and the LMO interface, is trustworthy when neither the +24.0% interface gain nor the split is stratified by the variable that should decide where each is load-bearing. *Wager:* the command interface, not the codebook split, is the load-bearing lever.

**Sharpest questions**: 1) Does a learned loco command interface beat a velocity controller most on precise locomotion subgoals (squat-to-place)? 2) Once stratified by camera motion, does the visual-dynamics split still add anything beyond the interface, or does an external unified latent (MotionWAM-style) tie it on loco-heavy bins? 3) Does action-free human-video pretraining replace an embodiment-gap-capped fraction of teleop data?

> [!warning] Risks
> - Two latents double training cost → action-free human video amortizes it (Psi0 runs on 30 h robot data).
> - Joint prediction can re-mix the modalities → test separate-vs-shared head; factor it if it leaks.
> - Latent vocabularies can collapse → separate codebooks + LeVERB's kinematic-reconstruction regularizer; report codebook utilization.

## B: Mobile Manipulation (Nav↔Manip Coupling)
*A moving base and an arm together, where base velocity is a manipulation DoF. The moving base shows up as two couplings now: what the moving camera keeps in view (B1), what scene state lasts once the base turns away (B2), both riding on BRS's autoregressive base→torso→arm decoding as established infrastructure.*

### B1: Active-Perception Coupling in Mobile Manipulation
> [!abstract] The bet
> Use a *learned* active-gaze policy that predicts a look-at point *conditioned on the base trajectory BRS's autoregressive base→torso→arm policy chooses*. It recovers the perception slice of HomeRobot's 5–15%→0.4–0.6% collapse, gain largest when the base is moving, near-zero when stationary. Matches Visibility-Aware Mobile Grasping's +18.0%-over-decoupled while beating its planner on demo tasks, and recovers dynamic-object relocations to DynaMem's 70% (vs 30% static, locate-failure 53.3%→6.7%) for in-view relocations where gaze beats re-driving. Falsifiable: a fixed forward camera matches learned gaze on moving-base tasks, or independently-predicted gaze matches base-coupled gaze.

**Why**: A moving base keeps changing what is visible. "Active gaze beats fixed camera" is consensus; contested between planners and learned gaze. We challenge the un-run combination: a *learned* look-at policy *conditioned on the base trajectory*.

**First-principles**: *Principle:* observability is a controllable function of the base+head action; an unobserved state cannot be recovered from the current frame by any capacity. *Challenged:* planners couple gaze to base as receding-horizon search with a see-for-safety objective, never a learned demo policy, and never split gaze-vs-exploration. *Wager:* HoMMI's relaxed "3D look-at point" makes gaze an explicit DoF (copying human 6-DoF head poses is kinematically infeasible).

**Sharpest questions**: 1) Does a learned base-coupled gaze policy beat the gaze-as-planner baseline, the gap opening during base motion? 2) Does gaze-driven re-observation beat exploration-driven re-observation for objects that move *within* the viewpoint? 3) Is the perception coupling separable and *additive* relative to BRS's action coupling (a 2×3 grid)?

> [!warning] Risks
> - Active gaze can destabilize manipulation → report precision during vs between active-looks; couple to A1.
> - Look-at is ambiguous → HoMMI learns a *relaxed* 3D look-at point from demos; report accuracy vs SR.
> - Active perception may not pay off → bound gaze frequency to the perception need; let the decomposition say which tasks earn it.
> - Gain may be a re-observation artifact, not gaze (DynaMem re-drives) → separate gaze-driven from exploration-driven.

### B2: Large-Workspace Memory for Mobile Manipulation
> [!abstract] The bet
> Build an *in-policy* memory that fuses persistent scene + episodic task-history *and* purges dynamic relocated objects. Beats *both* static-scene-memory policies (3D Latent Mapping 0.31, mindmap 76%) *and* modular dynamic maps (DynaMem 70% relocated, DovSG 35% long-term) on *multi-room relocated-object* tasks. The margin scales with the number of out-of-view returns, near-zero single-room, maximal multi-room; dynamic purging is required where the object moves between visits. Falsifiable: a static-scene-memory policy holds on relocated objects, or a memoryless long-window policy matches in-policy memory on multi-room tasks.

**Why**: A mobile manipulator's workspace is far bigger than its field of view: it sets an object down, turns away, returns. We challenge that a static scene-memory policy, or a modular dynamic map, suffices.

**First-principles**: *Principle:* the current frame is not a sufficient statistic; task-relevant state spans a workspace bigger than the FOV, so a Markovian policy structurally cannot return to an out-of-view target. *Challenged:* static-scene and modular-map adequacy. EchoVLA's 0.11→0.44 gap and 0.10 long-horizon result both vanish under memory ablation. *Wager:* the multi-room scaling law no external paper sweeps is the surviving lever.

**Sharpest questions**: 1) Do both scene and episodic memory contribute, with *episodic* carrying the long horizon? 2) Is dynamic (ray-cast-purged) memory required when objects move between visits, while a static map fails? 3) Does the in-policy dynamic scene+episodic advantage scale with multi-room extent?

> [!warning] Risks
> - Memory can go stale → adopt DynaMem's online ray-cast purging; report relocated-object SR.
> - Memory grows with workspace → prune to task-relevant state; report footprint-vs-SR.
> - Memory and perception interact → a 2×2 separates write-quality (active vs passive) from mechanism.
> - A long window may be cheaper → sweep window length against declarative memory; the claim holds only if a window stays below memory.

## C: Force-Adaptive Coordination Under Load
*Whole-body control under outside wrench, payload, and contact. A hand force travels through the chain to the support polygon, and the task reward leaves it out. Three parts: perform under a force you must model and anticipate (C1), certify you cannot fall or collide when the load drifts OOD (C2), and let the policy choose how compliant to be, region by region, instead of setting it from outside (C3).*

### C1: Force-Adaptive Whole-Body Control Under Unknown Wrench
> [!abstract] The bet
> Build a humanoid policy that estimates an *unknown outside* wrench, then *learns to forward-model* its whole-body reaction, a learned residual through $J_{\text{ext}}^{\top}$ feeding pre-emptive leg compensation. Holds balance under a *step-applied* load with a measurable advantage in the first ~100 ms after onset, where FALCON's reactive compensation lags; the sudden-onset CoM-excursion advantage at matched force is the headline metric. Sustains UAN-class loads (113 N cart, 8 kg lift) and clears IO-WBC's largest-load-envelope bar (80% success carrying an 18 kg tire vs 0% baseline, 65 kg crate push vs 50 kg baseline fail, no F/T sensor) — the new strongest reactive baseline the anticipatory bet must beat — while extending ALMA's anticipatory mechanism from self-induced-known to unknown-external on a tight support polygon. Falsifiable: anticipation matches reactive at the same step load on a humanoid, or the wrench is too noisy to forward-model.

**Why**: A humanoid opening a heavy door meets "significant, dynamic, multi-directional 3D end-effector forces," but the standard stack compensates late or never models force. The humanoid cluster is *reactive*; the one anticipatory paper (ALMA) predicts only the *self-induced known* wrench, on a quadruped. We challenge ALMA's scope, not "anticipation beats reactive" (proved, 208%).

**First-principles**: *Principle:* a hand force travels via $J_{\text{ext}}^{\top}$ to the support legs, so force adaptation is a whole-body balance problem, not local arm stiffness. *Challenged:* ALMA's self-induced-known/quadruped/model-based scope, and SplitAdapter's finding that a unified latent loses robustness under heavy load. *Wager:* FALCON's torque-limit-aware curriculum earns 0.60→0.37, so feasibility is the structure.

**Sharpest questions**: 1) Does anticipating an unknown external step load beat reactive in the first ~100 ms (CoM excursion at matched force)? 2) Does the *torque-limit-aware* curriculum, not raw force exposure, earn the gain? 3) Is explicit force sensing (WT-UMI's wearable tactile, 1.05 N RMSE) sub-linear on curriculum-covered tasks but super-linear on bulky/deformable contact-rich tasks (Bucket 60%→80%)?

> [!warning] Risks
> - Inertia/torque model off → treat the predictor as a residual over a nominal model; lean on UAN's actuator net.
> - Force adaptation can cost precision → report the force-vs-tracking-error Pareto front.
> - Large loads stress hardware + balance (113 N / 8 kg) → bound claims to validated platforms; couple to C2's certified filter.
> - Implicit handling may already suffice (FALCON, SplitAdapter) → run anticipatory vs implicit at matched load.

### C2: Safety-Bounded Whole-Body Control Under Load
> [!abstract] The bet
> Add a *wrench-aware* certified layer, a barrier whose safe set carries the external-payload equilibrium term. Holds collision-free single-leg balance under an unknown payload, where SHIELD-Humanoid's and ISSf-CBF WBC's kinematics-only barriers, tuned without a force term, violate the support polygon. In a *certified-vs-reward head-to-head under load*, it lifts OOD whole-body survival to CMP's 86.7% extreme / 93.3% moderate real (at 2.99 ms), which a reward-penalty-only policy of equal capacity (HWC-class robustness-by-training) cannot. Falsifiable: a kinematics-only barrier holds balance under load, or reward shaping matches the certified layer on OOD survival and collision under mass mismatch.

**Why**: An in-distribution policy gives no guarantee under OOD geometry/payload/sensor drift, and under load the failures are physical: fall, self-collision, boundary violation. The "certified barrier over a learned policy" mechanism is no longer novel (SHIELD-Humanoid, CBF-RL), but *both are for locomotion/obstacle-avoidance, no payload or external-wrench term*. We challenge that a kinematics-only barrier and robustness-by-training suffice under OOD load.

**First-principles**: *Principle:* balance (CoM inside the support polygon) and collision-freeness are *hard constraints*; a learned policy optimizes an expectation and carries no per-step guarantee under OOD shift. *Challenged:* DR + reward-shaping adequacy. CMP's 4.7% unshielded OOD-geometry survival and ISSf-CBF's ~50% baseline collision under mass mismatch mark the boundary. *Wager:* CMP's O(1) reduction (2.99 ms) makes a certified check loop-feasible; the novelty is the *payload/wrench-aware* barrier.

**Sharpest questions**: 1) Does a certified layer beat reward-shaped safety *under load*, the advantage concentrated under payload OOD where SHIELD/CBF-RL has no term? 2) Does a wrench-aware barrier hold balance under unknown load where a kinematics-only one fails? 3) Does best-effort projection (CMP) preserve more task success than a hard stop (RAPT) on identical OOD episodes?

> [!warning] Risks
> - A safety filter can over-constrain → CMP's best-effort projection preserves continuation; report completion-under-shield.
> - A safety check needs good geometry → MIF's confidence-aware 3DGS + on-demand mesh recovery; report survival vs fidelity.
> - A barrier needs an accurate model → ISSf-CBF tolerates 20% mass mismatch; report the mismatch survived.
> - Latency can break the loop → bound to 2.99 ms (CMP) / 1.63 ms (RAPT); the latency-vs-coverage sweep is the gate.

### C3: Compliance Allocation as an Explicit Policy Action
> [!abstract] The bet
> Make joint-region impedance a policy output, not a value set from outside. A policy that emits per-region impedance (shoulder/elbow group vs hip/ankle group) alongside the reach reference should dominate TOP's global arm-speed cap on the CoM-excursion-vs-tracking-error Pareto, at matched completion time. Not a free lunch: softening a joint changes how far it deviates under load, not the commanded $M_{\text{base,arm}}\ddot q_{\text{arm}}$ term itself, so this is a different instrument on the same axis as a speed cap, with its own trade-off. Falsifiable: the impedance-allocation curve sits on or below TOP's curve.

**Why**: Every humanoid compliance system (GentleHumanoid's τ_safe, SoftMimic's K_cmd, CHIP's 1/k, CoTaP's specified compliance) treats stiffness as an input the policy conditions on, never an output it chooses. The one system that makes stiffness a policy output at all is a quadruped with no arm (arXiv:2502.09436): its RL policy autonomously stiffens the legs opposite a push and relaxes the legs toward it, with no reward term written for that asymmetry. We challenge the field's shared assumption that compliance is a dial to tune.

**First-principles**: *Principle:* impedance is a free parameter of a rigid-actuator control law, not fixed by the dynamics, so a compliance channel fits the action space without contradicting $\ddot q = M(q)^{-1}(\tau - C\dot q - g + J_{\text{ext}}^\top F_{\text{ext}})$. *Challenged:* that compliance is a human-set hyperparameter, held by GentleHumanoid, SoftMimic, CHIP, CoTaP, and Unified-Force-Position-Control alike. *Wager:* region-differentiated softening is a different instrument than a global speed cap, not a strictly better one.

**Sharpest questions**: 1) Does per-region impedance allocation dominate TOP's global speed cap on the CoM-excursion-vs-tracking-error Pareto? 2) Does the quadruped's per-leg stiffening mechanism transfer to a humanoid's arm-base coupling? 3) Do existing certified safety layers (ISSf-CBF WBC, CMP) already have enough margin for a variable-impedance policy, or does the safe set need re-deriving?

> [!warning] Risks
> - Softening doesn't shrink the commanded coupling term, only how far the joint deviates → report the full excursion trajectory, not just the peak.
> - A certified layer built for fixed gains may not cover a variable-impedance policy → test whether existing margins have slack before re-deriving.
> - The only precedent is a quadruped with no arm → test the leg-only-to-arm-base transfer directly before scaling up the humanoid instantiation.

## D: Whole-Body Teleoperation & Human-Motion Retargeting
*The whole-body data wall, coupled demos are scarce, mismatched, per-platform. Three verbs: retarget existing human motion so its contact survives the morphology gap, or capture new coupled demos directly with a human in the loop (both D1), transfer a trained policy onto a new body without retraining (D2), synthesize coupled demos with the human removed from the loop (D3). Sharpest line: D1 vs D3, capture/retarget vs synthesis.*

### D1: Interaction-Preserving Whole-Body Retargeting
> [!abstract] The bet
> Stack NMR's learned-feasibility-manifold regularizer *under* OmniRetarget's interaction-mesh objective as one joint retargeting loss, a composite no system currently trains. NMR's own data pipeline already filters candidate motions for gross foot-ground contact defects and self-intersection, so the two systems are not cleanly split by "which failure mode each owns" the way the naive framing suggests: the real difference is mechanism. NMR's contact handling is a discard-then-learn gate baked into a fixed, morphology-specific training corpus, generalizing only statistically to new motions; OmniRetarget's constraint is re-solved fresh for every new demonstration and scene, with no training-distribution dependence. The causal wager: NMR's residual self-collision (0.87% of frames) concentrates on motions unlike its training clusters, a learned-generalization-gap failure that OmniRetarget's per-query hard constraint is structurally positioned to close, since it doesn't degrade on novel inputs the way a learned mapping does. Since neither paper reports OmniRetarget's own self-collision rate on a shared benchmark, "beats 0.87%" is a mechanism-level prediction, not an extrapolated number, first measurement is OmniRetarget's own baseline. On a *legged* platform, the card also ports the controlled isolation no system paper runs there: whole-body-captured demos (Mobile ALOHA / HMI / HumanoidExo) beat fixed-base-arm-demos + a separate locomotion controller on the balance-critical stratum, porting EMMA's wheeled +30 pp result to legs, where balance coupling exists to isolate. Falsifiable: OmniRetarget alone already matches or beats the joint loss's self-collision number, an unweighted sum of both losses reaches the same frontier with no cross-term, or the capture-isolation margin on the balance-critical stratum is ~0 (EMMA's wheeled result is a ceiling, not a floor).

**Why**: A human's loco-manipulation is defined by its *interactions*: hand on object, foot on floor, body against scene. A joint-accurate retargeter can be contact-broken, and the policy inherits it. Interaction-preservation is consensus (OmniRetarget, Human2Humanoid, MeshMimic); we challenge that feasibility-regularization (NMR) and interaction-preservation (OmniRetarget) are separate techniques a retargeter picks *one* of, rather than a joint objective, and note that they already touch overlapping ground (both check foot-ground contact) through different mechanisms.

**First-principles**: *Principle:* the information in a reference is the contact graph, which surfaces touch and with what geometry, not the absolute joint angles. *Challenged:* not that the two split failure modes cleanly (NMR's own pipeline filters foot-ground contact and self-collision too), but that a discard-then-learn gate over a fixed training corpus and a per-query hard-constrained optimization are the same kind of mechanism; nobody trains both as one loss. *Wager:* the two are complementary because they fail differently, NMR degrades on out-of-distribution motions, OmniRetarget doesn't, so stacking should close specifically NMR's OOD residual violations; separately, whether an explicit retarget is even needed once the coupling is captured directly (EMMA) is un-tested on legs.

**Sharpest questions**: 1) Does stacking NMR's feasibility manifold under OmniRetarget's interaction objective cut self-collisions below NMR's solo 0.87%, and below OmniRetarget's own (currently unmeasured) solo rate, while holding OmniRetarget's contact fidelity? 2) Is the penetration/foot-skating → downstream-SR curve monotone across methods (slope + R²), a supporting measurement, not the headline? 3) Do whole-body-captured demos beat fixed-base demos + a controller on the balance-critical stratum of a *legged* platform, porting EMMA's wheeled +30 pp isolation?

> [!warning] Risks
> - Needs the contact graph specified → OmniRetarget infers contact from human–object–scene data; report quality vs annotation quality.
> - The morphology gap can exceed any retarget → Human2Humanoid's physics-aware constraints bound infeasible targets; report the range covered.
> - Contact-fidelity need not equal task success → tie fidelity to downstream RL SR.
> - An RL-in-the-loop retargeter is costly (per-reference RL like ReActor) → prefer optimization-based preservation (OmniRetarget); report cost-per-ref.
> - The capture isolation may not transfer to legs → EMMA's wheeled +30 pp may be a ceiling, not a floor; run the subtraction on a bipedal platform directly.

### D2: Cross-Embodiment Whole-Body Policy Transfer
> [!abstract] The bet
> On *whole-body loco-MANIPULATION* (not locomotion), a cross-embodiment adapter transfers a pretrained policy at Any2Any's ~1% of from-scratch compute/data. It works across 4 humanoids via a PHASOR-class phase-anchored representation (90.3% R@1, 1.62 mm next-frame). Front-line falsifier: it *beats a one-time-trained generalist* (XHugWBC ~85% of specialists / Embodiment-Aware Distillation) on cost below a measurable crossover, with the transferable structure *localized* to the dynamics-sensitive pathway. Falsifiable: joint-space transfer at equal budget matches the phase-anchored representation, or a one-time generalist beats cheap transfer at equal cost on loco-manipulation.

**Why**: Whole-body-tracking policies are trained per-platform; a new humanoid restarts from scratch even though the coordination is largely the same. The space splits into *cheap transfer* (Any2Any PEFT, PHASOR) and *generalist scale* (XHugWBC, EAGLE), but per-platform avoidance is consensus *only on locomotion*. We challenge that it holds for loco-MANIPULATION, and that cheap localized transfer beats generalist scale below a crossover.

**First-principles**: *Principle:* whole-body coordination splits into a morphology-invariant structure (phase-clocked balance + end-effector goals) and a body-specific joint realization; the structure is the transferable invariant. *Challenged:* the locomotion-only scope of H-Zero/XHugWBC/scaling-laws, and the Any2Any-vs-generalist tension on manipulation-coupled tasks; PHASOR's phase manifold is "intrinsic to the behavior rather than to the body." *Wager:* Any2Any's ablation localizes the lever to the dynamics-sensitive pathway.

**Sharpest questions**: 1) Does phase-anchored transfer beat joint-space transfer at equal budget on a held-out humanoid? 2) Is the transferable structure localized to the dynamics-sensitive pathway (PEFT placement matters)? 3) Does cheap localized transfer beat a one-time generalist below a crossover on loco-manipulation?

> [!warning] Risks
> - Morphology distance bounds transfer, and kinematic distance alone mis-ranks it → sweep kinematic *and* inertial distance vs cost; test the rank inversion; locate where ~1% transfer breaks on each axis.
> - Phase anchoring may not capture manipulation → route non-periodic skills through a shared token space (UniT).
> - Transfer can underperform a scaled universal model → locate the crossover; transfer is the efficient regime below it.
> - A discrete shared codebook can under-utilize on a distant body → report utilization vs morphology distance; prefer a continuous phase manifold (PHASOR).

### D3: Whole-Body Synthetic Data Generation
> [!abstract] The bet
> Two claims. (i) From-scratch generation (GRAIL 81.4% SR, synthetic-only 90% real) breaks the *diversity ceiling* a single-seed route (HumanoidMimicGen 0.89 PSR, DemoHLM) hits: sweep seed/asset breadth and generalization rises then plateaus for the seed route while from-scratch keeps climbing. (ii) Enforced synthesized contact-fidelity → downstream-SR is *monotone* (GRAIL's 0.90% penetration / 88.9% tracking), so feasibility-enforcement during generation is a quantitative trainability predictor. Co-training lifts real SR 0.51→0.71 (+20%). Falsifiable: the seed route's diversity does not plateau below from-scratch, or downstream SR is flat in synthesized feasibility.

**Why**: The data wall has two exits. D1 captures or retargets coupled demos with a human still in the loop, but every demo still costs a human, so that route cannot reach VLA-scale. The second exit removes the human and *synthesizes* the trajectory. We challenge the un-measured questions: does a fixed seed cap synthesized diversity? does enforced contact-fidelity predict trainability monotonically?

**First-principles**: *Principle:* a demonstration is just a physically-feasible coupled trajectory. Feasibility (dynamic stability + contact, no penetration) is a checkable property of the trajectory, not of who made it, so a generator that enforces it produces training-valid demos. *Challenged:* the diversity-ceiling and feasibility→trainability questions left un-measured; HumanoidMimicGen's manipulation-only 0.33 (vs 0.89) shows feasibility must be enforced *as whole-body dynamics*. *Wager:* from-scratch breaks the seed's diversity ceiling, and enforced contact-fidelity is a monotone predictor.

**Sharpest questions**: 1) Does from-scratch generation break the seed's diversity ceiling DemoHLM and HumanoidMimicGen share (seed plateaus, from-scratch climbs)? 2) Does enforced contact-fidelity predict synthetic-demo trainability monotonically? 3) Is synthetic-only enough for dynamics-dominated tasks while contact-precision tasks need a real-data anchor?

> [!warning] Risks
> - A feasibility-enforcing generator is hard to build → HumanoidMimicGen reuses a learned locomotion controller + classical IK/planning; report demos-per-seed.
> - Synthetic demos can carry a sim-to-real gap → GRAIL's contact/depth alignment + Genie Sim 3.0's R²=0.94 bound it; report synthetic-only vs co-trained SR.
> - Diversity is capped by the seed/asset pool → sweep randomization breadth; GRAIL widens it with video-prior assets; report generalization vs breadth.
> - Generated video is plausible but not dynamically feasible → never train on it directly; pass through 4D-retarget + a feasibility-enforcing tracker (GenMimic absorbs the noise).

## Cross-References
- Source: [[Whole-Body|Whole-Body Coordination Research Directions]]
- Plain-language: [[__ELI5-EN__/Whole-Body-ELI5|ELI5]]
- Sibling capability axes: [[Locomotion]], [[Manipulation]]
- Substrate cross-refs: [[WAM]], [[Sim2Real]]
- Umbrella: [[Embodied-AI]]
