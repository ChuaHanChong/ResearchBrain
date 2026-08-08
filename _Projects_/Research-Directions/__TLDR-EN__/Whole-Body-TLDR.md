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
> A humanoid that manipulates *while it moves* faces one fact: arm and legs are mechanically linked. An arm reach pushes back as a torque on the base. Whole-body skill is not "an arm controller plus a leg controller." The bet across 13 directions and 4 clusters: **the link is structure to *predict*, not data to *collect*.** Make it explicit (A). Coordinate it with a moving base (B). Hold it under outside force (C). Get the demo data to learn it (D). Directions that model the link win on a fixed data budget.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A: Whole-Body Loco-Manipulation | A1–A4 | Arm and legs cannot be split. An arm reach is a balance push the legs must expect. Flat RL fails on the linked high-DoF action space |
| B: Mobile Manipulation (Nav↔Manip Coupling) | B1–B3 | Base velocity is a manipulation DoF. Nav-then-manipulate throws away the in-task repositioning that grows the workspace |
| C: Force-Adaptive Coordination Under Load | C1–C2 | An outside hand wrench travels through the chain to the support polygon. The legs make up for what the arms feel, and the task reward leaves out the force |
| D: Whole-Body Teleoperation & Human-Motion Retargeting | D1–D4 | The data wall. Demos of *coupled* loco-manipulation are scarce, embodiment-mismatched, and per-platform |

## A: Whole-Body Loco-Manipulation
*Linked arm–leg dynamics on a single floating base. Model the coupling term itself (A1). Combine feasible primitives so the action never leaves the feasible set (A2). Close the precision loop in the world frame, base as active transport (A3). Send joint loco+manip commands through one latent interface (A4).*

### A1: Coupled-Dynamics Whole-Body Action Models
> [!abstract] The bet
> Predict the base reaction *explicitly*: $\hat\delta_{\text{base}}=\hat M_{\text{base,arm}}\ddot q_{\text{arm}}$, analytic term plus learned residual, fed as an auxiliary-loss target. Beats HEX's implicit MoE *on the same fixed dataset*, widening the 41.0→61.8 OOD margin by ≥ +3 pp into the mid-60s, most in the top arm-acceleration quartile where SEEC's "arms-are-light" assumption is wrong. Two gates first. *Frontier gate:* check whether the destabilizing arm→base coupling is really *inertial* ($M_{\text{base,arm}}$, which this predicts) or *contact-wrench / support-polygon* (single↔double support, impending slip, which it ignores), by instrumenting contact-state before committing the inertial predictor; if the contact share dominates at the worst instant the term must be reframed as contact-constrained hybrid dynamics. *De-risk gate:* run the arm-acceleration-stratified explicit-vs-implicit ablation on a controllable baseline (FALCON's emergent-coupling policy, or a self-trained MoE) *before* the possibly-closed HEX backbone. Falsifiable: if explicit ≤ 61.8% at matched latency, leave the coupling to the MoE. Regime caveat (mirrors D3): explicit structure likely wins only in the low-data tail, the fine-tuned generalist may win at scale, so publish the crossover boundary rather than claim structure always wins.

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
*A moving base and an arm together, where base velocity is a manipulation DoF. The moving base shows up as three couplings: how base and arm actions are factored (B1), what the moving camera keeps in view (B2), what scene state lasts once the base turns away (B3).*

### B1: Joint Base-Arm Action vs Sequential Decomposition
> [!abstract] The bet
> The coordination-structure margin (unidirectional AC-DiT / bidirectional InCoM / flat Mobile ALOHA) is *concentrated on reach-extension tasks where the base moves mid-grasp* and near-zero on fixed-base reaches; bidirectional beats unidirectional *only* when the arm action feeds back to constrain the base. Prediction: the structure gap tracks in-task base-travel demand, holds BRS's 88%/58% and 13×/21× on reach-extension tasks, matches InCoM's 83.8% ManiSkill-HAB, collapses to ≤ flat-concat on fixed-base tasks. Falsifiable: the structure margin is flat across in-task base motion, or bidirectional never beats unidirectional.

**Why**: The reflex pipeline drives to a pose and *then* runs a fixed-base policy, but a mobile manipulator grasps *while* repositioning. We challenge not the factoring but *which* structure wins, *when*.

**First-principles**: *Principle:* base velocity is a manipulation DoF, so the right arm action depends on the base action chosen for that instant ($p(a_{\text{base}})\,p(a_{\text{torso}}\mid a_{\text{base}})\,p(a_{\text{arm}}\mid a_{\text{base}},a_{\text{torso}})$). *Challenged:* which structure wins when; BRS's autoregressive-vs-naive-joint swap collapses its 13×/21× margin. *Wager:* the structure margin tracks in-task base-travel demand.

**Sharpest questions**: 1) Does bidirectional beat unidirectional *only* where optimal arm motion forces a base correction? 2) Does the structured-over-flat margin concentrate on reach-extension and vanish on fixed-base reaches? 3) Is autoregressive factoring, not a safety filter, what suppresses OOD whole-body states (BRS's near-zero violations)?

> [!warning] Risks
> - Autoregressive decoding adds latency → bound to control-loop budget at BRS's chunk size; fall back to a flat head with a coupling-aware loss.
> - Conditioning order may be task-dependent → stratify by in-task base motion; let it adapt.
> - Perception is often the real bottleneck (HomeRobot 5–15%→0.4–0.6% with a real detector) → couple to B2; report SR with GT vs real perception.
> - Co-training transfer may not hold across morphologies → report the arm-skill-vs-base-coupling split.

### B2: Active-Perception Coupling in Mobile Manipulation
> [!abstract] The bet
> Use a *learned* active-gaze policy that predicts a look-at point *conditioned on B1's chosen base trajectory*. It recovers the perception slice of HomeRobot's 5–15%→0.4–0.6% collapse, gain largest when the base is moving, near-zero when stationary. Matches Visibility-Aware Mobile Grasping's +18.0%-over-decoupled while beating its planner on demo tasks, and recovers dynamic-object relocations to DynaMem's 70% (vs 30% static, locate-failure 53.3%→6.7%) for in-view relocations where gaze beats re-driving. Falsifiable: a fixed forward camera matches learned gaze on moving-base tasks, or independently-predicted gaze matches base-coupled gaze.

**Why**: A moving base keeps changing what is visible. "Active gaze beats fixed camera" is consensus; contested between planners and learned gaze. We challenge the un-run combination: a *learned* look-at policy *conditioned on the base trajectory*.

**First-principles**: *Principle:* observability is a controllable function of the base+head action; an unobserved state cannot be recovered from the current frame by any capacity. *Challenged:* planners couple gaze to base as receding-horizon search with a see-for-safety objective, never a learned demo policy, and never split gaze-vs-exploration. *Wager:* HoMMI's relaxed "3D look-at point" makes gaze an explicit DoF (copying human 6-DoF head poses is kinematically infeasible).

**Sharpest questions**: 1) Does a learned base-coupled gaze policy beat the gaze-as-planner baseline, the gap opening during base motion? 2) Does gaze-driven re-observation beat exploration-driven re-observation for objects that move *within* the viewpoint? 3) Is the perception coupling separable and *additive* relative to B1's action coupling (a 2×3 grid)?

> [!warning] Risks
> - Active gaze can destabilize manipulation → report precision during vs between active-looks; couple to A1.
> - Look-at is ambiguous → HoMMI learns a *relaxed* 3D look-at point from demos; report accuracy vs SR.
> - Active perception may not pay off → bound gaze frequency to the perception need; let the decomposition say which tasks earn it.
> - Gain may be a re-observation artifact, not gaze (DynaMem re-drives) → separate gaze-driven from exploration-driven.

### B3: Large-Workspace Memory for Mobile Manipulation
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
*Whole-body control under outside wrench, payload, and contact. A hand force travels through the chain to the support polygon, and the task reward leaves it out. Two halves: perform under a force you must model and anticipate (C1), and certify you cannot fall or collide when the load drifts OOD (C2).*

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

## D: Whole-Body Teleoperation & Human-Motion Retargeting
*The whole-body data wall, coupled demos are scarce, mismatched, per-platform. Four verbs: retarget existing human motion so its contact survives the morphology gap (D1), capture new coupled demos with a human in the loop (D2), transfer a trained policy onto a new body without retraining (D3), synthesize coupled demos with the human removed from the loop (D4). Sharpest line: D2 vs D4, capture vs synthesis.*

### D1: Interaction-Preserving Whole-Body Retargeting
> [!abstract] The bet
> Look across retargeting methods (OmniRetarget, Human2Humanoid, NMR, DynaRetarget, ULTRA). The penetration/foot-skating → downstream-RL-SR regression is *monotone with a measurable slope and R²* on a shared task suite, so contact-fidelity is a *designed-against quantitative predictor*, not just a correlate. The per-contact-term ablation (object-only vs object+scene at *fixed* joint accuracy) shows a measurable SR delta. Falsifiable: SR is flat or non-monotone in contact violation, or a pose-matching retarget of equal joint accuracy reaches the same downstream SR, then the contact graph is decorative.

**Why**: A human's loco-manipulation is defined by its *interactions*: hand on object, foot on floor, body against scene. A joint-accurate retargeter can be contact-broken, and the policy inherits it. Interaction-preservation is consensus (OmniRetarget, Human2Humanoid, MeshMimic); we challenge that contact-fidelity merely *correlates* with trainability rather than *predicting* it monotonically, and that all contacts are equally load-bearing.

**First-principles**: *Principle:* the information in a reference is the contact graph, which surfaces touch and with what geometry, not the absolute joint angles. *Challenged:* OmniRetarget/MeshMimic preserve interaction but never test whether fidelity *predicts* trainability or *which* term matters; OmniRetarget's interaction-mesh objective enables 82.20–94.73% downstream RL. *Wager:* a joint-accurate-but-contact-broken reference trains worse than a joint-loose-but-contact-true one, monotonically.

**Sharpest questions**: 1) At equal joint accuracy, does interaction-preservation beat pose-matching on object-transport/climbing? 2) Is the penetration/foot-skating → downstream-SR curve monotone across methods (slope + R²)? 3) Is scene-contact preservation needed beyond object-contact for body-against-scene tasks (climbing while carrying), near-zero on tabletop?

> [!warning] Risks
> - Needs the contact graph specified → OmniRetarget infers contact from human–object–scene data; report quality vs annotation quality.
> - The morphology gap can exceed any retarget → Human2Humanoid's physics-aware constraints bound infeasible targets; report the range covered.
> - Contact-fidelity need not equal task success → tie fidelity to downstream RL SR.
> - An RL-in-the-loop retargeter is costly (per-reference RL like ReActor) → prefer optimization-based preservation (OmniRetarget); report cost-per-ref.

### D2: Whole-Body Teleoperation Interfaces & Robot-Free Demonstration
> [!abstract] The bet
> Run the controlled isolation no system paper runs. Whole-body-captured demos (Mobile ALOHA / HMI) beat fixed-base-arm-demos + a separate locomotion controller on coupled tasks; the gap is near-zero on fixed-base tasks where no coupling is demonstrated either way. On TeleOpBench's 4 modalities, MoCap/exoskeleton capture *locomotion* coupling better while VR/vision capture *manipulation* dexterity better, no single interface dominates. Prediction: the head-to-head reproduces EgoHumanoid's +51 pp generalization (82% vs 31%) and HumanoidExo's 5%→80% only on the coupled stratum, scaling like SUGAR's 32.7%→76.0% in human demos. Falsifiable: fixed-base + controller matches whole-body-captured demos on coupled tasks, or one modality dominates both halves.

**Why**: Whole-body loco-manipulation is "bottlenecked by the scarcity of diverse, large-scale demonstration data." Fixed-base arm teleoperation cannot produce a loco-manip demo, the operator never commands base and arms together. We challenge that simultaneous capture supplies coupling decoupled data cannot, each modality a *different half*.

**First-principles**: *Principle:* the coupling exists only in a joint trajectory where locomotion and manipulation are commanded together; the *interface* decides whether the coupling is in the data, independent of policy capacity. *Challenged:* the rigs assume the coupling lands in the data but none isolates it by subtraction; EgoHumanoid's +51 pp shows the coupling lives in the data. *Wager:* two levers are un-run, the fixed-base-vs-whole-body head-to-head, and the per-modality decomposition.

**Sharpest questions**: 1) Do whole-body-captured demos beat fixed-base demos + a controller on coupled tasks, near-zero on fixed-base? 2) Does teleop modality change which half is captured well (MoCap/exo for loco, VR/vision for manip)? 3) Does generalization scale with *human* demos while in-domain SR saturates on *robot* demos?

> [!warning] Risks
> - The embodiment gap can break alignment → EgoHumanoid's alignment + co-training bridges it; report in-domain vs generalization by alignment quality.
> - Whole-body teleop taxes the operator → novices reach expert level in ~5 trials; the throughput ceiling is what D4 removes.
> - Human demos lack proprioception/force → co-train with robot data; report which tasks need robot refinement.
> - Capture is bounded by human hours → demos-per-human-hour (capture) vs demos-per-seed (synthesis, D4).

### D3: Cross-Embodiment Whole-Body Policy Transfer
> [!abstract] The bet
> On *whole-body loco-MANIPULATION* (not locomotion), a cross-embodiment adapter transfers a pretrained policy at Any2Any's ~1% of from-scratch compute/data. It works across 4 humanoids via a PHASOR-class phase-anchored representation (90.3% R@1, 1.62 mm next-frame). Front-line falsifier: it *beats a one-time-trained generalist* (XHugWBC ~85% of specialists / Embodiment-Aware Distillation) on cost below a measurable crossover, with the transferable structure *localized* to the dynamics-sensitive pathway. Falsifiable: joint-space transfer at equal budget matches the phase-anchored representation, or a one-time generalist beats cheap transfer at equal cost on loco-manipulation.

**Why**: Whole-body-tracking policies are trained per-platform; a new humanoid restarts from scratch even though the coordination is largely the same. The space splits into *cheap transfer* (Any2Any PEFT, PHASOR) and *generalist scale* (XHugWBC, EAGLE), but per-platform avoidance is consensus *only on locomotion*. We challenge that it holds for loco-MANIPULATION, and that cheap localized transfer beats generalist scale below a crossover.

**First-principles**: *Principle:* whole-body coordination splits into a morphology-invariant structure (phase-clocked balance + end-effector goals) and a body-specific joint realization; the structure is the transferable invariant. *Challenged:* the locomotion-only scope of H-Zero/XHugWBC/scaling-laws, and the Any2Any-vs-generalist tension on manipulation-coupled tasks; PHASOR's phase manifold is "intrinsic to the behavior rather than to the body." *Wager:* Any2Any's ablation localizes the lever to the dynamics-sensitive pathway.

**Sharpest questions**: 1) Does phase-anchored transfer beat joint-space transfer at equal budget on a held-out humanoid? 2) Is the transferable structure localized to the dynamics-sensitive pathway (PEFT placement matters)? 3) Does cheap localized transfer beat a one-time generalist below a crossover on loco-manipulation?

> [!warning] Risks
> - Morphology distance bounds transfer → sweep distance vs cost; locate the cliff where ~1% transfer breaks.
> - Phase anchoring may not capture manipulation → route non-periodic skills through a shared token space (UniT).
> - Transfer can underperform a scaled universal model → locate the crossover; transfer is the efficient regime below it.
> - A discrete shared codebook can under-utilize on a distant body → report utilization vs morphology distance; prefer a continuous phase manifold (PHASOR).

### D4: Whole-Body Synthetic Data Generation
> [!abstract] The bet
> Two claims. (i) From-scratch generation (GRAIL 81.4% SR, synthetic-only 90% real) breaks the *diversity ceiling* a single-seed route (HumanoidMimicGen 0.89 PSR, DemoHLM) hits: sweep seed/asset breadth and generalization rises then plateaus for the seed route while from-scratch keeps climbing. (ii) Enforced synthesized contact-fidelity → downstream-SR is *monotone* (GRAIL's 0.90% penetration / 88.9% tracking), so feasibility-enforcement during generation is a quantitative trainability predictor. Co-training lifts real SR 0.51→0.71 (+20%). Falsifiable: the seed route's diversity does not plateau below from-scratch, or downstream SR is flat in synthesized feasibility.

**Why**: The data wall has two exits. D2 captures coupled demos faster, but every demo still costs a human, so capture cannot reach VLA-scale. The second exit removes the human and *synthesizes* the trajectory. We challenge the un-measured questions: does a fixed seed cap synthesized diversity? does enforced contact-fidelity predict trainability monotonically?

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
- Umbrella: [[Embodied-AI]] · [[Focus-Direction]]
