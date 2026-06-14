---
title: "TL;DR: Whole-Body Coordination — Loco-Manipulation, Mobile Manipulation, Force-Adaptive Control"
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

# TL;DR: Whole-Body Coordination — Loco-Manipulation, Mobile Manipulation, Force-Adaptive Control

> [!info] What this is
> A skimmable TL;DR of [[Whole-Body|Whole-Body Coordination]]. Per direction: **the bet**, the reasoning, the sharpest open questions, the risks. Full detail (related-work tables, all hypotheses, benchmarks) stays in the source. Plain-language version: [[Whole-Body-ELI5|ELI5]].

> [!abstract] Overview
> A humanoid that manipulates *while it moves* faces one structural fact: the arm and the legs are mechanically coupled — an arm reach is a reaction torque on the base, so whole-body competence does not factor into "an arm controller plus a leg controller." The editorial bet across 13 directions / 4 clusters: **the coupling is structure to *predict*, not data to *collect*** — make it explicit (A), coordinate it with a moving base (B), hold it under external force (C), and get the demonstration data to learn it (D). Directions that model the coupling win on a fixed data budget, where more teleop does not.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A — Whole-Body Loco-Manipulation | A1–A4 | Arm–leg coupling is non-separable: an arm reach is a balance disturbance the legs must anticipate; flat RL fails on the coupled high-DoF action space |
| B — Mobile Manipulation (Nav↔Manip Coupling) | B1–B3 | Base velocity is a manipulation DoF; nav-then-manipulate discards the in-task repositioning that extends the workspace |
| C — Force-Adaptive Coordination Under Load | C1–C2 | An external hand wrench propagates through the chain to the support polygon; the legs compensate for what the arms feel, and the task reward omits the force |
| D — Whole-Body Teleoperation & Human-Motion Retargeting | D1–D4 | The data wall — demonstrations of *coupled* loco-manipulation are scarce, embodiment-mismatched, and per-platform |

## A — Whole-Body Loco-Manipulation
*Coupled arm–leg dynamics on a single floating base: model the coupling term itself (A1), compose feasible primitives so the action never leaves the feasible set (A2), close the precision loop in the world frame with the base as active transport (A3), and emit joint loco+manip commands through one latent interface (A4).*

### A1 — Coupled-Dynamics Whole-Body Action Models
> [!abstract] The bet
> An *explicit* predicted base-reaction $\hat\delta_{\text{base}}=\hat M_{\text{base,arm}}\ddot q_{\text{arm}}$ (analytic term + learned residual) fed as an auxiliary-loss target beats HEX's implicit MoE *on the same fixed dataset* — widening the 41.0→61.8 OOD margin by ≥ +3 pp (into the mid-60s), with the gain concentrated on the top arm-acceleration quartile where SEEC's "arms-are-light" assumption is false. Falsifiable: if explicit ≤ 61.8% at matched latency, the coupling is better left to the MoE.

**Why** — A whole-body policy must account for the base/leg reaction an arm reach induces, but most stacks control the parts separately and let that coupling term vanish. The first principle: the inertia matrix $M(q)$ is non-block-diagonal, so an arm acceleration *is* a leg-balance disturbance. The challenged assumption is SEEC's: that arm→base back-coupling is "negligible because arms are dynamically light," so only the base→arm direction needs an explicit term.

**First-principles** — *Principle:* $M(q)$ is non-block-diagonal — the whole-body value cannot be split into an arm part plus a leg part. *Challenged:* SEEC assumes the arm→base reaction is negligible (it predicts only base→arm); HEX's UPP-removal ablation is the largest single drop (Pouring 11/12 → 6/12) vs second-order 12M-frame pretraining. *Wager:* the coupling is the lever, and no one predicts the arm→base reaction explicitly yet — borrow SEEC's analytic+residual recipe for the *reverse* direction.

**Sharpest questions** — 1) Does an explicit base-reaction auxiliary target on HEX's exact backbone + dataset lift OOD past 61.8% at matched parameter count? 2) Does the gain concentrate in the top arm-acceleration quartile (where SEEC's premise breaks) and vanish in the bottom quartile? 3) Does a shared *predictor* carry more coupling than FALCON's shared *observation* at equal capacity?

> [!warning] Risks
> - Coupling model needs an accurate inertia model → treat it as a learned residual over a nominal analytic model; report sim-vs-real prediction error.
> - Explicit may not beat implicit (HEX's MoE may already capture it) → that is the falsifier; run head-to-head at matched latency and keep the MoE if it wins.
> - Gains may be platform-specific (79.8%/61.8% is one humanoid) → report margin by motion-aggressiveness class, not a single average.
> - Explicit coupling adds latency → bound the predictor to the HiWET-class single-digit-ms budget; fall back to the MoE if it cannot fit.

### A2 — Skill-Blending vs Monolithic Whole-Body Control
> [!abstract] The bet
> The pipeline-location head-to-head no one has run: online convex-blend (SkillBlender) vs upstream feasible prior (DreamControl-v2) vs a distilled-experts monolith (Experts-to-Generalist 66.84% / HANDOFF 0.31 m³) on one shared 8-task / 3-embodiment skill set with *zero* per-task reward tuning. Prediction: the feasibility-by-construction blend matches SkillBlender's outperformance while the monolith reward-hacks, and the upstream prior used as a downstream-RL reference lifts the valid-trajectory rate toward 68% (vs 8%) and RL success toward 0.925 (vs 0.101) *more* than blend-during-control. Falsifiable: if a reward-tuned monolith matches the blend without hacking, or pipeline location makes no difference, composition buys nothing.

**Why** — The reflexive recipe for a new whole-body task is "tune the reward until the monolith does it," but a high-DoF monolith rediscovers feasibility from scratch every time, and SkillBlender shows task-specific reward engineering causes reward hacking and unnatural behaviors. The first principle: a softmax-weighted blend of frozen feasible primitives stays inside their convex hull — feasibility comes from the combination rule, not a per-task reward. Challenged assumption: that whole-body competence needs task-specific reward engineering on a monolith.

**First-principles** — *Principle:* a convex combination of feasible primitives never leaves the set they span, so any mix is feasible for free. *Challenged:* the standard RL recipe (and HumanoidBench's "flat RL fails, hierarchy helps" framing) — SkillBlender's softmax-removal ablation collapses feasibility, relocating the binding constraint to feasibility-preserving composition. *Wager:* pipeline *location* of the feasibility (during-control / upstream prior / distilled monolith) is the un-run variable.

**Sharpest questions** — 1) Does a convex-hull blend match both the reward-tuned RL/MPC monolith *and* the distilled-experts monolith with one shared reward, over short *and* 8 s episodes (where monoliths destabilize)? 2) Does an upstream feasible prior beat during-control blending *and* OMG-style post-hoc generation-filtering as the downstream-RL reference? 3) Does primitive-library size amortize sub-linearly across tasks (tasks-per-primitive-set), and does a learned set beat a hand-designed one?

> [!warning] Risks
> - Frozen primitives cap achievable behavior → allow a norm-bounded learned residual outside the hull; report how large it can grow before reward hacking returns.
> - Primitive-library design is itself engineering → test learned vs hand-designed; the win is amortization, so report tasks-per-primitive-set.
> - Sim-to-real gap on the blend (SkillBlender is state-based, sim-only) → borrow the diffusion-prior hardware recipe (Bionic runs 125 real trials).
> - Blending may produce discontinuous transitions → SkillBlender's softmax smooths weights; report jerk/limit motion-quality diagnostics per AGILE.

### A3 — World-Frame End-Effector Tracking with the Base as an Active DoF
> [!abstract] The bet
> On a *bipedal humanoid with a walking gait*, a world-frame Commander/Tracker hierarchy with a *learned continuous α-schedule* holds HiWET's 12.4 mm sim / 12–15 mm real error over long horizons, where (i) a matched body-centric controller's error grows monotonically with locomotion distance while the world-frame one stays flat, and (ii) the learned α reaches more out-of-static-range targets than HiWET's tuned-constant α and Spatial Brain Cerebellum's discrete trigger. Falsifiable: if a body-centric baseline stays flat with distance, or a tuned-constant α ties the learned schedule, closure buys nothing.

**Why** — When a humanoid places a hand precisely while walking, the target is in the world frame, but most controllers are robot-centric, which HiWET shows "leads to cumulative world-frame drift and high-frequency oscillations." Error accumulates with distance, not capacity. World-frame-through-base-motion is emerging consensus *on quadrupeds*; the frame distinction is mostly unproven on bipedal humanoids. Challenged assumption: that body-centric control suffices for task-space precision and that base motion is a disturbance to reject (HiWET treats reach-vs-balance as a *tuned constant* α, never a learned schedule).

**First-principles** — *Principle:* a manipulation target lives in the world frame; world-frame closure is the only formulation where precision is decoupled from how far the base has walked, and the mobile base is the DoF that brings out-of-static-reach targets into reach. *Challenged:* HiWET's constant α and the discrete go/no-go reach-extenders — its KMP-removal ablation doubles hand error (12.4 → 25.2 mm). *Wager:* the drift is a *frame* problem, not a capacity problem; scaling the body-centric policy cannot fix it.

**Sharpest questions** — 1) Does body-centric EE error rise monotonically with cumulative base-travel distance while world-frame stays flat — the curve no quadruped precedent has plotted on a bipedal gait? 2) Does a learned α-schedule reach more out-of-static-range targets than fixed-α and a discrete solver? 3) Does world-frame closure just move the bottleneck into base-state estimation (EE error ~linear in estimation noise)?

> [!warning] Risks
> - World-frame closure needs accurate base-state estimation → HiWET's ablation shows removing the estimator costs ~10 mm; report EE error vs estimation error.
> - Active base transport can destabilize manipulation → stack A1's coupling-aware predictor under the tracker; schedule α so reach-extension and balance don't fight.
> - 12.4 mm may not generalize across tasks/embodiments → test over horizon and across embodiments; report error by task class and locomotion distance.

### A4 — Unified-Latent Policy for Joint Loco-Manipulation Commands
> [!abstract] The bet
> The *two-LAM-vs-one-LAM* ablation no one external has run: WholeBodyVLA's two visual-dynamics-split VQ-VAE latents beat a single shared latent — using MotionWAM's *unified* whole-body motion latent as the negative control — at matched capacity, with the separate-over-shared margin scaling with camera motion (largest on loco-heavy splits, near-zero on manip-heavy). Prediction: ≥78.0% unified-split vs ≤56.7% same-LMO decoupled on Bag/Box/Cart, gain traced to +38.7% action-free pretraining and +24.0% loco-RL, reaching LeVERB's 58.5% (7.8× over naive hierarchical). Falsifiable: if a single shared latent matches the split, or the margin is flat across camera-motion bins, the visual-dynamics-split is not the lever even though unification is.

**Why** — Most policies are implicitly manipulation models "confined to limited workspaces" because they "lack integrated humanoid locomotion"; bolting a velocity controller underneath causes "decision-execution misalignment." "Unified beats decoupled" is now consensus; the still-non-consensus part is that the *visual statistics force the architecture* — manipulation video (near-static camera) vs locomotion video (gait-moving camera) need *separate* latent models. Challenged assumption: that one shared latent suffices (the bet MotionWAM's single motion latent and Fast-Slow WB VLA's single action token both make).

**First-principles** — *Principle:* manipulation and locomotion have different visual dynamics, so a single shared latent underfits one — yet the next action is a joint over both, and separate stacks re-introduce decision-execution misalignment. *Challenged:* the single-shared-latent bet — WholeBodyVLA's separate VQ-VAE latents beat a shared model (+38.7% pretraining, +24.0% loco-RL; same-LMO baselines trail 78.0%). *Wager:* the *split by visual statistics*, not unification itself, earns the win.

**Sharpest questions** — 1) Do two visual-dynamics-split LAMs beat a single shared LAM, with the gap scaling with camera motion? 2) Does a learned loco command interface beat a velocity controller most on precise locomotion subgoals (squat-to-place)? 3) Does action-free human-video pretraining replace a measurable, embodiment-gap-capped fraction of teleop data?

> [!warning] Risks
> - Two latent models double training complexity → the data-efficiency curve via action-free human video amortizes the cost (Psi0 runs on 30 h robot data).
> - Joint prediction can entangle the modalities it separated → test separate-vs-shared prediction head; factor the head if it leaks (the dynamics coupling is real, the *representation* should stay split).
> - Latent action vocabularies can collapse (VQ-VAE codebooks under-utilize; verb degenerates to a discrete vocabulary) → separate codebooks + LeVERB's kinematic-reconstruction regularizer; report codebook utilization.

## B — Mobile Manipulation (Nav↔Manip Coupling)
*Jointly controlling a moving base and an arm, where base velocity is itself a manipulation DoF. The moving base surfaces as three couplings: how base and arm actions are factored (B1), what the moving camera keeps in view (B2), and what scene state persists once the base turns away (B3).*

### B1 — Joint Base-Arm Action vs Sequential Decomposition
> [!abstract] The bet
> The coordination-structure margin (unidirectional AC-DiT / bidirectional InCoM / flat Mobile ALOHA) is *concentrated on reach-extension tasks where the base moves mid-grasp* and near-zero on fixed-base reaches, and bidirectional beats unidirectional *only* when the arm action feeds back to constrain the base. Prediction: the structure gap tracks in-task base-travel demand, holding BRS's 88%/58% and 13×/21× on reach-extension tasks and matching InCoM's 83.8% ManiSkill-HAB, while collapsing to ≤ flat-concat on fixed-base tasks. Falsifiable: if the structure margin is flat across in-task base motion — or bidirectional never beats unidirectional — any single factoring suffices.

**Why** — The reflexive pipeline drives to a pose and *then* runs a fixed-base manipulation policy, freezing the base before the arm acts — but a mobile manipulator grasps *while* repositioning, because base velocity changes the reachable workspace mid-grasp. The "go base-first" claim — and even the naive "go bidirectional" refinement — is now taken (AC-DiT's directional ablation, InCoM's head-to-head). Challenged assumption: not the factoring itself but *which* coordination structure wins *and when*, as a function of in-task base motion (Causal WBMM established the canonical "dependencies are causal not flat" prior years earlier).

**First-principles** — *Principle:* base velocity is a manipulation DoF, so the right arm action is conditional on the base action chosen for that instant ($p(a_{\text{base}})\,p(a_{\text{torso}}\mid a_{\text{base}})\,p(a_{\text{arm}}\mid a_{\text{base}},a_{\text{torso}})$). *Challenged:* the un-answered sub-question of which structure (unidirectional / bidirectional / flat) wins when — BRS's autoregressive-vs-naive-joint swap collapses its 13×/21× margin. *Wager:* the structure margin is conditional on in-task base-travel demand, not uniform.

**Sharpest questions** — 1) Does bidirectional beat unidirectional *only* where the optimal arm motion forces a base correction? 2) Does the structured-over-flat margin concentrate on reach-extension tasks and vanish on fixed-base reaches? 3) Is autoregressive factoring — not a safety filter — what suppresses OOD whole-body states (BRS's near-zero violations)?

> [!warning] Risks
> - Autoregressive decoding adds inference latency → bound to the control-loop budget at BRS's real-time chunk size; fall back to a flat head with a coupling-aware loss.
> - The conditioning order may be task-dependent (base-first wrong for fine in-place adjustment) → stratify by in-task base motion; let the factoring order adapt.
> - Perception is often the real bottleneck (HomeRobot 5–15%→0.4–0.6% with a real detector) → couple to B2; report SR with GT vs real perception to separate the factoring gain.
> - Co-training transfer may not hold across morphologies → report the arm-skill-vs-base-coupling decomposition.

### B2 — Active-Perception Coupling in Mobile Manipulation
> [!abstract] The bet
> A *learned* active-gaze policy that predicts a look-at point *conditioned on B1's chosen base trajectory* recovers the perception slice of HomeRobot's 5–15%→0.4–0.6% collapse, with the gain largest when the base is moving (near-zero stationary), matches Visibility-Aware Mobile Grasping's +18.0%-over-decoupled while beating its planner on demo tasks, and recovers dynamic-object relocations to DynaMem's 70% (vs 30% static, locate-failure 53.3%→6.7%) for in-view relocations where gaze beats re-driving. Falsifiable: if a fixed forward camera matches learned gaze on moving-base tasks, or independently-predicted gaze matches base-coupled gaze, the planner suffices.

**Why** — Most stacks read a fixed forward camera, but a moving base continuously changes what is visible, so the target, contact, and next subgoal can leave the frame when they matter — and an unobserved state cannot be acted on, no matter the policy capacity. "Active gaze beats fixed camera" is now consensus, contested between runtime planners (gaze+base joint optimization) and learned gaze policies (mostly fixed-base). Challenged assumption: the un-run conjunction of a *learned* look-at policy *conditioned on the base trajectory the action policy chooses*, with perception-coupling isolated from action-coupling.

**First-principles** — *Principle:* observability is a controllable function of the base+head action, not a given; an unobserved state is unrecoverable from the current frame by any capacity. *Challenged:* the planners couple gaze to base as receding-horizon search with a see-for-safety objective, not a learned demo policy, and never decompose gaze-vs-exploration or during-vs-between stability. *Wager:* HoMMI's relaxed "3D look-at point" makes gaze an explicitly controlled DoF (copying human 6-DoF head poses is kinematically infeasible).

**Sharpest questions** — 1) Does a learned base-coupled gaze policy beat the gaze-as-planner baseline, with the gap opening during base-motion phases? 2) Does gaze-driven re-observation beat exploration-driven re-observation for objects that move *within* the current viewpoint? 3) Is the perception coupling separable and *additive* relative to B1's action coupling (a 2×3 factoring×perception grid)?

> [!warning] Risks
> - Active gaze can destabilize manipulation → report precision during vs between active-look maneuvers; couple to A1's coupling-aware control.
> - Predicting where to look needs supervision (look-at is ambiguous; copying human head poses is infeasible) → HoMMI learns a *relaxed* 3D look-at point from demos; report look-at accuracy vs downstream SR.
> - Active perception adds a control loop that may not pay off → bound gaze frequency to the perception need; let the perception-vs-action decomposition say which tasks earn it.
> - The gain may be a re-observation artifact, not gaze (DynaMem already re-drives) → separate gaze-driven from exploration-driven re-observation on in-view vs out-of-view relocations.

### B3 — Large-Workspace Memory for Mobile Manipulation
> [!abstract] The bet
> An *in-policy* memory fusing persistent scene + episodic task-history *and* dynamic relocated-object purging beats *both* static-scene-memory policies (3D Latent Mapping 0.31, mindmap 76%) *and* modular dynamic maps (DynaMem 70% relocated, DovSG 35% long-term) on *multi-room relocated-object* tasks, with the margin scaling monotonically with the number of out-of-view returns (near-zero single-room, maximal multi-room) and dynamic purging required where the object moves between visits. Falsifiable: if a static-scene-memory policy holds on relocated objects, or a memoryless long-window policy matches in-policy memory on multi-room tasks, the dynamic/in-policy/multi-room combination is not the lever.

**Why** — A mobile manipulator's relevant workspace far exceeds its field of view — it walks between rooms, sets an object down, turns away, and must return — so a Markovian policy re-perceiving from the current frame has no record of where it left the basket or that the object moved. The scene-memory-beats-memoryless half is taken; no one combines *scene + episodic in one learned policy*, makes that in-policy memory *dynamic* (relocated-object-aware), and sweeps *multi-room* scale. Challenged assumption: that a static scene-memory policy or a modular dynamic map (outside the policy) is enough.

**First-principles** — *Principle:* the current frame is not a sufficient statistic — task-relevant state spans a workspace larger than the instantaneous FOV, so a Markovian policy is structurally unable to return to an out-of-view target. *Challenged:* static-scene and modular-map adequacy — EchoVLA's 0.11→0.44 gap and 0.10 long-horizon result both vanish under memory ablation; a static map confidently returns the stale location when objects move. *Wager:* the multi-room scaling law no external paper sweeps is the surviving lever.

**Sharpest questions** — 1) Do both scene and episodic memory contribute, with *episodic* carrying the long horizon? 2) Is dynamic (ray-cast-purged) memory required when objects move between visits, while a static map fails? 3) Does the in-policy dynamic scene+episodic advantage scale monotonically with multi-room extent, where single-scene memories saturate?

> [!warning] Risks
> - Memory can accumulate stale/wrong state → adopt DynaMem's online ray-cast purging; report SR on relocated objects as a measured failure mode.
> - Memory scales with workspace (multi-room state can blow up linearly) → prune to task-relevant state; report the footprint-vs-SR curve.
> - Memory and perception interact (bad active perception writes bad memory) → a 2×2 separates write-quality (active vs passive) from the memory mechanism.
> - A long observation window may be the cheaper baseline → sweep window length against declarative memory on multi-room tasks; the claim only holds if a long window stays below memory.

## C — Force-Adaptive Coordination Under Load
*Whole-body control under external wrench, payload, and contact force — where a hand force propagates through the chain to the support polygon and the task reward silently omits it. Two halves: perform under a force you must model and anticipate (C1), and certify you cannot fall or collide when the load drifts OOD (C2).*

### C1 — Force-Adaptive Whole-Body Control Under Unknown Wrench
> [!abstract] The bet
> A humanoid policy that estimates an *unknown external* wrench then *learns to forward-model* its whole-body reaction (a learned residual through $J_{\text{ext}}^{\top}$ feeding pre-emptive leg compensation) holds balance under a *step-applied* load with a measurable advantage in the first ~100 ms after onset where FALCON's reactive compensation lags — the sudden-onset CoM-excursion advantage at matched force is the headline metric — while sustaining UAN-class loads (113 N cart, 8 kg lift), and extends ALMA's anticipatory mechanism from self-induced-known to unknown-external on a tight support polygon. Falsifiable: if anticipation matches reactive at the same step load on a humanoid, or the wrench is too noisy to forward-model, force is adequately handled reactively.

**Why** — A humanoid opening a heavy door or carrying a variable payload meets "significant, dynamic, multi-directional 3D end-effector forces," but the standard stack solves the upper body with kinematic IK that compensates force late, or trains a monolith that never models force — the wrench is an unmodelled disturbance. The humanoid force-adaptive cluster is *reactive* (estimate-then-compensate from the past); the one anticipatory paper (ALMA) predicts only the *self-induced known* wrench, on a quadruped, with a model-based predictor. Challenged assumption: not "anticipation beats reactive" (ALMA proved it, 208%) but ALMA's narrow scope — self-induced-known only.

**First-principles** — *Principle:* a hand force does not stay at the hand — it propagates via $J_{\text{ext}}^{\top}$ to the support legs, so force adaptation is a whole-body balance problem, not local arm stiffness. *Challenged:* the self-induced-known/quadruped/model-based scope of ALMA, and SplitAdapter's finding that a unified latent conflating load with dynamics mismatch loses robustness under heavy load. *Wager:* FALCON's torque-limit-aware curriculum (physically feasible forces via inverse dynamics) earns the 0.60→0.37 gain, so feasibility is the structure; extend ALMA's feedforward to unknown-external on a humanoid.

**Sharpest questions** — 1) Does anticipating an unknown external step load beat reactive compensation in the first ~100 ms (CoM excursion at matched force)? 2) Does the *torque-limit-aware* curriculum, not raw force exposure, earn the gain? 3) Is explicit force sensing (e.g. WT-UMI's wearable tactile, 1.05 N RMSE) sub-linear on curriculum-covered tasks but super-linear on bulky/deformable contact-rich tasks (Bucket 60%→80%)?

> [!warning] Risks
> - Anticipation needs an accurate inertia/torque model → treat the reaction predictor as a learned residual over a nominal model; lean on UAN's actuator net where the model is uncertain.
> - Force adaptation can trade off precision → report the force-magnitude vs tracking-error Pareto front, not a single number.
> - Large loads stress hardware + balance (113 N / 8 kg push the support polygon) → bound load claims to validated platforms; couple to C2's certified filter.
> - Implicit handling may already suffice (FALCON's curriculum, SplitAdapter's context) → that is the falsifier; run anticipatory vs implicit at matched load and keep the curriculum if implicit wins.

### C2 — Safety-Bounded Whole-Body Control Under Load
> [!abstract] The bet
> A *wrench-aware* certified layer — a barrier whose safe set carries the external-payload equilibrium term — holds collision-free single-leg balance under an unknown payload where SHIELD-Humanoid's and ISSf-CBF WBC's kinematics-only barriers (tuned without a force term) violate the support polygon, and in a *certified-vs-reward head-to-head under load* lifts OOD whole-body survival to CMP's 86.7% extreme / 93.3% moderate real (at 2.99 ms) where a reward-penalty-only policy of equal capacity (HWC-class robustness-by-training) cannot. Falsifiable: if a kinematics-only barrier holds balance under load, or reward shaping matches the certified layer on OOD survival and collision under mass mismatch, the wrench term and the guarantee buy nothing.

**Why** — A policy that works in-distribution gives no guarantee when geometry, payload, or sensor noise drifts OOD — and under load the failure modes are physical (fall, self-collision, workspace-boundary violation), each unrecoverable. The "certified barrier over a black-box learned policy on a real humanoid" mechanism is no longer novel (SHIELD-Humanoid, CBF-RL) — but *both for locomotion/obstacle-avoidance, with no payload or external-wrench term*. Challenged assumption: that a kinematics-only barrier and robustness-by-training suffice when the load drifts OOD.

**First-principles** — *Principle:* balance (CoM inside the support polygon) and collision-freeness are *hard constraints* with no soft trade-off — a learned policy optimizes an expectation and carries no per-step guarantee under OOD shift. *Challenged:* DR + reward-shaping adequacy — CMP's 4.7% unshielded OOD-geometry survival and ISSf-CBF's ~50% baseline collision under mass mismatch mark the boundary; RAPT shows sim-robust policies "execute confidently in OOD states." *Wager:* CMP's O(1) reduction (2.99 ms) makes a certified check loop-feasible; the survival novelty is the *payload/wrench-aware* barrier, not the barrier-over-learned-policy mechanism.

**Sharpest questions** — 1) Does a certified layer beat reward-shaped safety *under load*, with the advantage concentrated under payload OOD where SHIELD/CBF-RL's locomotion-only certification has no term? 2) Does a wrench-aware barrier hold balance under unknown load where a kinematics-only one fails? 3) Does best-effort projection (CMP) preserve more task success than a hard stop (RAPT) on identical OOD episodes?

> [!warning] Risks
> - A safety filter can over-constrain and block valid actions → CMP's best-effort projection to the closest feasible intention preserves continuation; report task-completion-under-shield.
> - A safety check is only as good as the geometry it sees → MIF's confidence-aware 3DGS + on-demand mesh recovery raises fidelity before the check; report survival vs percept fidelity.
> - A formal barrier needs an accurate model → ISSf-CBF's input-to-state-safe formulation tolerates a 20% mass mismatch; report the mismatch level the guarantee survives.
> - Latency can break the control loop → the latency-vs-coverage sweep is the feasibility gate; bound to the 2.99 ms (CMP) / 1.63 ms (RAPT) class.

## D — Whole-Body Teleoperation & Human-Motion Retargeting
*The whole-body data wall — coupled demos are scarce, embodiment-mismatched, per-platform. Four verbs: retarget existing human motion so its contact survives the morphology gap (D1), capture new coupled demos with a human in the per-demo loop (D2), transfer a trained policy onto a new body without retraining (D3), and synthesize coupled demos with the human removed from the loop (D4). The sharpest line is D2 vs D4 — capture vs synthesis.*

### D1 — Interaction-Preserving Whole-Body Retargeting
> [!abstract] The bet
> Across retargeting methods (OmniRetarget, Human2Humanoid, NMR, DynaRetarget, ULTRA), the penetration/foot-skating → downstream-RL-SR regression is *monotone with a measurable slope and R²* on a shared task suite — so contact-fidelity is a *designed-against quantitative predictor*, not a correlate — and the per-contact-term ablation (object-only vs object+scene at *fixed* joint accuracy) shows a measurable SR delta isolating the load-bearing relationship. Falsifiable: if SR is flat or non-monotone in contact violation, or a pose-matching retarget of equal joint accuracy reaches the same downstream SR, the contact graph is not the load-bearing quantity and the metric is decorative.

**Why** — Loco-manipulation references come from human motion, but a human's loco-manipulation is defined by its *interactions* (hand on object, foot on floor, body against scene), and a retargeter minimizing joint-space pose error can be joint-accurate yet contact-broken — the hand floats off, the foot skates, the reference penetrates the ground, and the policy inherits the violation. Interaction-preservation is now consensus (OmniRetarget, Human2Humanoid, MeshMimic). Challenged assumption: that contact-fidelity merely *correlates* with trainability rather than *predicting* it monotonically, and that all contact relationships are equally load-bearing.

**First-principles** — *Principle:* the information in a reference is the contact graph (which surfaces touch and with what geometry), not the absolute joint angles, which are a morphology-specific realization. *Challenged:* OmniRetarget/MeshMimic preserve interaction but never test whether fidelity *predicts* trainability or *which* contact term matters — OmniRetarget's interaction-mesh objective enables 82.20–94.73% downstream RL from a minimal reward set. *Wager:* a joint-accurate-but-contact-broken reference trains worse than a joint-loose-but-contact-true one, and the relationship is monotone with a measurable slope.

**Sharpest questions** — 1) At equal joint accuracy, does interaction-preservation beat pose-matching downstream on object-transport/climbing? 2) Is the penetration/foot-skating → downstream-SR curve monotone across methods (slope + R²)? 3) Is scene-contact preservation needed beyond object-contact for body-against-scene tasks (climbing while carrying), near-zero on tabletop?

> [!warning] Risks
> - Interaction preservation needs the contact graph specified → OmniRetarget infers contact from human–object–scene data; report quality vs contact-annotation quality.
> - Morphology gap can exceed what any retarget can bridge → Human2Humanoid's physics-aware constraints bound infeasible targets; report the morphology range covered.
> - Contact-fidelity metrics need not equal task success → tie fidelity to downstream RL SR as a measured curve, not penetration/skating alone.
> - An RL-in-the-loop retargeter is costly (per-reference RL like ReActor) → prefer optimization-based preservation (OmniRetarget) on large corpora; report cost-per-reference.

### D2 — Whole-Body Teleoperation Interfaces & Robot-Free Demonstration
> [!abstract] The bet
> The controlled isolation no system paper runs: whole-body-captured demos (Mobile ALOHA / HMI) beat fixed-base-arm-demos + a separate locomotion controller on coupled tasks, with the gap near-zero on fixed-base tasks where no coupling is demonstrated either way; and on TeleOpBench's 4 modalities, MoCap/exoskeleton capture *locomotion* coupling better while VR/vision capture *manipulation* dexterity better, so no single interface dominates. Prediction: the head-to-head reproduces EgoHumanoid's +51 pp generalization (82% vs 31%) and HumanoidExo's 5%→80% only on the coupled stratum, and scales like SUGAR's 32.7%→76.0% in human demos. Falsifiable: if fixed-base + controller matches whole-body-captured demos on coupled tasks, or one modality dominates both halves, the coupling is not data-bound.

**Why** — Whole-body loco-manipulation is "bottlenecked by the scarcity of diverse, large-scale demonstration data," and the standard fix — fixed-base arm teleoperation — structurally cannot produce a loco-manip demonstration, because the operator never commands base and arms together, so the coupling is absent from every demo. The robot-free whole-body capture *pipeline* is now consensus (HMI, HumanoidExo, EgoHumanoid). Challenged assumption: not "build a capture rig" but the unproven claim underneath — that simultaneous capture supplies coupling decoupled data structurally cannot, and that each modality captures a *different half*.

**First-principles** — *Principle:* the coupling exists only in a joint trajectory where locomotion and manipulation are commanded together; the *interface* determines whether the coupling is in the data, independent of policy capacity. *Challenged:* the rigs assume the coupling lands in the data but none isolates it by controlled subtraction — EgoHumanoid's +51 pp shows the coupling lives in the data, not the policy. *Wager:* the fixed-base-vs-whole-body head-to-head and the per-modality "which interface captures which half" decomposition are the un-run levers.

**Sharpest questions** — 1) Do whole-body-captured demos beat fixed-base demos + a controller on coupled tasks, with the gap near-zero on fixed-base tasks? 2) Does teleop modality change which half of the coupling is captured well (MoCap/exo for loco, VR/vision for manip)? 3) Does generalization scale with *human* demos while in-domain SR saturates on *robot* demos?

> [!warning] Risks
> - The human–humanoid embodiment gap can break alignment → EgoHumanoid's alignment pipeline + co-training bridges it; report in-domain vs generalization by alignment quality.
> - Whole-body teleop is cognitively hard (base + two arms taxes the operator) → novices reach expert level in ~5 trials; the throughput ceiling is exactly what D4's synthesis removes.
> - Human demos lack proprioception and force → co-train with robot data for precision; report which tasks need robot-demo refinement.
> - Capture is bounded by human hours → the clean line to D4: report demos-per-human-hour for capture vs demos-per-seed for synthesis.

### D3 — Cross-Embodiment Whole-Body Policy Transfer
> [!abstract] The bet
> On *whole-body loco-MANIPULATION* (not locomotion), a cross-embodiment adapter transfers a pretrained policy at Any2Any's ~1% of from-scratch compute/data across 4 humanoids via a PHASOR-class phase-anchored representation (90.3% R@1, 1.62 mm next-frame), and — the promoted front-line falsifier — *beats a one-time-trained generalist* (XHugWBC ~85% of specialists / Embodiment-Aware Distillation) on cost below a measurable crossover, with the transferable structure *localized* to the dynamics-sensitive pathway. Falsifiable: if joint-space transfer at equal budget matches the phase-anchored representation, or a one-time generalist beats cheap transfer at equal cost on loco-manipulation, neither the structure nor the cheap-transfer regime is the lever.

**Why** — Whole-body-tracking policies are trained per-platform — a new humanoid restarts training from scratch, paying the full data + compute bill, even though the coordination it learns is largely the same. The space has split into *cheap transfer* (Any2Any PEFT, PHASOR phase invariant) and *generalist scale* (XHugWBC, EAGLE, embodiment scaling laws), but per-platform avoidance is consensus *only on locomotion* (H-Zero, the scaling line stop there). Challenged assumption: that the result holds for whole-body loco-MANIPULATION, and that cheap localized transfer beats one-time generalist scale below a crossover.

**First-principles** — *Principle:* whole-body coordination decomposes into a morphology-invariant structure (phase-clocked balance + end-effector goals) and a body-specific joint realization; the structure is the transferable invariant. *Challenged:* the locomotion-only scope of H-Zero/XHugWBC/scaling-laws, and the unresolved Any2Any-PEFT-vs-generalist tension on manipulation-coupled tasks — PHASOR's phase manifold is "intrinsic to the behavior rather than to the body." *Wager:* Any2Any's ablation localizes the lever to the dynamics-sensitive pathway, so the structure is a specific pathway, not a coincidence of scale.

**Sharpest questions** — 1) Does phase-anchored transfer beat joint-space transfer at equal adaptation budget on a held-out humanoid? 2) Is the transferable structure localized to the dynamics-sensitive pathway (PEFT placement matters)? 3) Does cheap localized transfer beat a one-time generalist below a crossover on whole-body loco-manipulation, beyond which the generalist matches?

> [!warning] Risks
> - Morphology distance bounds transfer → sweep distance vs cost and locate the cliff where ~1% transfer breaks.
> - Phase anchoring may not capture manipulation (natural for cyclic locomotion, less so for fine manipulation) → route non-periodic skills through a shared token space (UniT) where phase underfits.
> - Transfer can underperform a scaled universal model → locate the crossover; treat transfer as the data/compute-efficient regime below it, not universally dominant.
> - A discrete shared codebook can under-utilize (dead codes on a distant body) → report codebook utilization vs morphology distance; prefer a continuous phase manifold (PHASOR).

### D4 — Whole-Body Synthetic Data Generation
> [!abstract] The bet
> (i) From-scratch generation (GRAIL 81.4% SR, synthetic-only 90% real) breaks the *diversity ceiling* a single-seed route (HumanoidMimicGen 0.89 PSR, DemoHLM) hits — sweeping seed/asset breadth, generalization rises then plateaus for the seed route while from-scratch keeps climbing; and (ii) enforced synthesized contact-fidelity → downstream-SR is *monotone* (GRAIL's 0.90% penetration / 88.9% tracking), so feasibility-enforcement during generation is a quantitative trainability predictor, with co-training lifting real SR 0.51→0.71 (+20%). Falsifiable: if the seed route's diversity does not plateau below from-scratch, or downstream SR is flat in synthesized feasibility, neither the ceiling nor the feasibility-curve is the lever.

**Why** — The data wall has two exits: D2 captures coupled demos faster, but every captured demo still costs a human, so capture cannot reach VLA-scale corpora. The second exit removes the human from the per-demo loop: *synthesize* the coupled trajectory. The seed-amplification route is now multiply-instantiated (HumanoidMimicGen, DemoHLM, MoMaGen); from-scratch (GRAIL) and feasibility-enforced generation (VisualMimic) also exist. The "whole-body feasibility is the lever" claim is answered yes. Challenged assumption: not "the human rate caps quantity" but the un-measured next-order questions — whether a fixed seed caps synthesized diversity, and whether enforced contact-fidelity predicts trainability monotonically.

**First-principles** — *Principle:* a demonstration is just a physically-feasible coupled trajectory; feasibility (dynamic stability + contact, no penetration) is a checkable property of the trajectory, not of who made it — so a generator that enforces it produces training-valid demos, arbitrarily more than a human can teleoperate. *Challenged:* the diversity-ceiling and feasibility→trainability questions the crowd left un-measured — HumanoidMimicGen's manipulation-only 0.33 (vs 0.89) shows feasibility must be enforced *as whole-body dynamics*. *Wager:* from-scratch breaks the seed's diversity ceiling, and enforced contact-fidelity is a monotone trainability predictor.

**Sharpest questions** — 1) Does from-scratch generation break the seed's diversity ceiling that DemoHLM and HumanoidMimicGen share (seed route plateaus, from-scratch keeps climbing)? 2) Does enforced contact-fidelity predict synthetic-demo trainability monotonically? 3) Is synthetic-only sufficient for dynamics-dominated tasks while contact-precision tasks need a real-data co-training anchor?

> [!warning] Risks
> - A feasibility-enforcing generator is itself hard to build → HumanoidMimicGen reuses a learned locomotion controller + classical IK/planning; report demos-per-seed so amortization is the measured win.
> - Synthetic demos can carry a sim-to-real gap the policy inherits → GRAIL's contact/depth alignment + Genie Sim 3.0's R²=0.94 bound it; report synthetic-only vs co-trained real SR.
> - Generation diversity is capped by the seed / asset pool → sweep randomization breadth; GRAIL widens it with video-prior assets; report generalization vs seed/asset breadth.
> - Generated video is plausible but not dynamically feasible → never train directly on generated video; pass it through 4D-retarget + a feasibility-enforcing tracker (GenMimic absorbs the noise).

## Cross-References
- Source: [[Whole-Body|Whole-Body Coordination Research Directions]]
- Plain-language: [[Whole-Body-ELI5|ELI5]]
- Sibling capability axes: [[Locomotion]], [[Manipulation]]
- Substrate cross-refs: [[WAM]], [[Sim2Real]]
- Umbrella: [[Embodied-AI]] · [[Focus-Direction]]
