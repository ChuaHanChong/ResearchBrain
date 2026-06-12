---
title: "Promising Research Directions: Locomotion — Bipedal & Quadruped"
aliases:
  - "Locomotion Research Directions"
  - "Locomotion Promising Directions"
tags:
  - research-directions
  - locomotion
  - humanoid
  - quadruped
  - sim-to-real
---

# Promising Research Directions: Locomotion — Bipedal & Quadruped

> [!abstract] Overview
> A legged robot that moves through the real world faces one structural fact: **it must act on what it cannot directly sense.** The privileged physical state that makes a gait work — terrain friction, ground height ahead of the swing foot, payload, contact, model error — is available in simulation and absent on hardware, so a deployable policy has to recover or bound it from proprioception, exteroception, or a learned model.
> These **8 directions across 2 clusters** organize the bets around that recovery problem and the agile skills it unlocks: the humanoid's legs and dynamic skills under partial observation (A), and the quadruped's real-world adaptation when the unobserved state shifts (B).
> The non-consensus bet: across both clusters, the lever is the *mechanism that extracts more from each step* — feasible references over more demonstrations, anticipatory perception over reactive recovery, off-policy reuse and world-model imagination over PPO rollout-discard — not more data, more scale, or more domain randomization.

---

## Methodology

**Scope.** Corpus: ~12 humanoid/quadruped/legged-locomotion surveys, benchmarks, and simulators plus ~25 locomotion-method papers from `_KnowledgeHub_/`, cross-checked against [[../../../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] and the `Embodied-AI/` deep-dives [[../../../Embodied-AI/02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]] and [[../../../Embodied-AI/14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]]. **Subsystem boundary**: locomotion only — commands that move the body via legs/wheels (gait and velocity tracking, terrain traversal, balance and push-recovery, agile skills via motion imitation, fall-recovery, proprioceptive-vs-perceptive locomotion, mapless mobility-to-goal). Loco-manipulation coupling, mobile manipulation (arm + base), and arm/hand manipulation belong to the sibling [[Manipulation|Manipulation]] and [[Whole-Body|Whole-Body]] docs; if a paper manipulates an *object*, it is out of scope here. A **Wheeled Mobility & Navigation cluster was considered and dropped** — the vault's wheeled/mapless papers are platform-agnostic locomotion-to-goal control, not a distinct wheeled frontier, leaving fewer than two distinct non-VLN wheeled directions; the strongest ([[2506.05997|SRU]]) folds into B3. VLN goal-*reasoning* and the world-model substrate are cross-referenced to the umbrella and WAM docs, not re-clustered.

---

## Locomotion Survey Landscape

| Survey / Benchmark | The open problem it names (surveys) / what it measures (benchmarks) | Fuels |
|---|---|---|
| [[2403.10506\|HumanoidBench]] | Flat RL fails most whole-body tasks; the high-DoF *action* space (not observation) is the exploration bottleneck; hierarchical structure needed | A1, A2, A3, A4, A5 |
| [[2603.20147\|AGILE]] | Workflow gap (late env-bug discovery) + transfer gap (fragile hardware deployment); no standardized I/O contract; motion-quality (jerk/limit) diagnostics missing | A1, A2, A3, A4, A5 |
| [[2502.08844\|MuJoCo Playground]] | Sim-efficiency vs fidelity; a unified GPU pipeline for legged + humanoid + arm; vision-based policy training without separate nets | A1, A2, A5 |
| [[2408.14472\|DWL]] | Robust locomotion on uneven terrain from *noisy proprioception alone*; partial observability; zero-shot sim-to-real without fine-tuning | A1, B1, B2 |
| [[2502.12152\|HUMANUP]] | Getting-up is non-periodic, rich-contact, sparse-reward — not a locomotion variant; unpredictable post-fall configs; terrain diversity | A3 |
| [[2604.23702\|QuietWalk]] | Ground-reaction-force is unmodeled; footwear/contact variation breaks gaits; acoustic cost is ignored by the reward | A4 |
| [[2107.04034\|RMA]] | Sim-to-real contact/deformable-surface gap; online adaptation without real-world fine-tuning; payload + friction shift | B1, B2 |
| [[2212.07740\|TERT]] | Cross-terrain generalization; TCN-style adaptation (RMA) fails on stairs; smooth/energy-efficient control | B1 |
| [[2206.14176\|DayDreamer]] | DRL needs millions of interactions impractical on hardware; sim-to-real gap; learning skills in hours not weeks | B2, A5 |
| [[2504.16680\|RWM-U]] | Offline-MBRL distribution shift + compounding error; long-horizon dynamics inaccuracy; real-robot deployability of MBRL | B2 |
| [[2506.05997\|SRU]] | Long-range mapless-navigation memory; spatial recall over hundreds of steps; zero-shot transfer to legged-wheel hardware | B3 |
| [[2403.13358\|QUARD-Auto]] | Generalist quadruped skill breadth (99 sub-tasks); compute-efficient capacity (MoE active params); emergent path planning | B1, B3 |

> [!tip] Convergence patterns
> - **The privileged-state gap, not the policy, is the deployment bottleneck** (4-way): [[2107.04034|RMA]] (the deployable policy must *infer* the privileged extrinsics — friction, payload, contact — from proprioception, carrying **12 kg** zero-fine-tune), [[2408.14472|DWL]] (a *denoising* world model estimates the true state + terrain from noisy proprioception for zero-shot snow/stairs), [[2504.16680|RWM-U]] (an epistemic-uncertainty penalty *bounds* reliance on the model exactly where the unobserved state is unknown), [[2403.10506|HumanoidBench]] (flat RL "generally fails" because high-DoF exploration is the wall) — four suites name the same wall under different words: the hard part is recovering or bounding the unobserved physical state, not generating the gait, the empirical mandate for A1/B1/B2's three recovery routes.
> - **Real-world adaptation is bottlenecked by interaction budget, not policy class** (3-way): [[2206.14176|DayDreamer]] (DRL needs *millions* of interactions impractical on hardware — the named motivation for learning skills in hours not weeks), [[2107.04034|RMA]] (online adaptation *without* real-world fine-tuning, since on-robot trials are the cost), [[2504.16680|RWM-U]] (offline MBRL on sim+real beats *online* model-free at **0.91** on ANYmal D precisely by not collecting more real rollouts) — three suites name the same wall: the binding constraint is how much real-world interaction a deployable policy demands, the empirical mandate for B2 and A5's sample-efficiency bets.
> - **Cross-terrain generalization is unsolved — flat and TCN-style methods collapse on hard terrain** (3-way): [[2212.07740|TERT]] (TCN-style adaptation fails on stairs, **0%** for the RMA baseline, motivating a terrain-representation architecture), [[2408.14472|DWL]] (robust traversal of uneven terrain from *noisy proprioception alone* under partial observability is unsolved), [[2403.10506|HumanoidBench]] (flat RL fails most whole-body tasks because the high-DoF action space is the exploration bottleneck) — three suites name the same wall: existing policies generalize poorly across terrains and need structure (terrain representation, denoising, hierarchy), the empirical mandate for A1's perceptive and B1's proprioceptive terrain bets.
> - **No standardized whole-body protocol localizes *where* a gait fails** (3-way): [[2603.20147|AGILE]] (no standardized I/O contract, late environment-bug discovery, and missing motion-quality diagnostics), [[2502.08844|MuJoCo Playground]] (a unified GPU sim, but the cross-legged/humanoid evaluation protocol is still per-platform), [[2403.13358|QUARD-Auto]] (a 99-sub-task generalist suite that measures skill breadth but not the embodiment cost — heat, noise, force — a gait pays) — three suites name the same missing layer: a shared protocol that reports *how* a gait succeeds (jerk, force, temperature, energy), not only *whether*, which the Benchmark Gaps section enumerates per direction.

---

## Formal Framing

**The locomotion control object.** A locomotion policy maps an observation $o$ — proprioception $q$ (joint angles, IMU, contact), optionally exteroception $e$ (depth / height-scan) — and a command $c$ (target velocity $v^*$, heading, gait, or a reference motion clip) to a joint action $a$:

$$\pi: (q, e, c) \mapsto a, \qquad a = \tau \text{ or } q^{\text{des}}$$

Locomotion differs from manipulation in what the action regulates: not an object–effector **contact-state**, but the body's **base trajectory and balance** — the centre-of-mass path, the foot-placement sequence, and dynamic stability against gravity and disturbance. The body is moved, not an external object via a grasp.

**The privileged-state / proprioception split.** Every legged method faces a partially-observed physical state. Let $z$ be the **privileged context** — terrain friction $\mu$, ground height $h(\cdot)$, payload $m$, contact forces, actuator state — available in sim but not on hardware. The deployable policy must act on $o$ alone:

| Regime | Policy input | Privileged $z$ | Exemplar |
|---|---|---|---|
| **Privileged (sim oracle)** | $(q, e, z)$ | observed | [[2107.04034\|RMA]] base policy (trains with extrinsics) |
| **Proprioceptive (blind, deployable)** | $q$ only | inferred from history $\hat{z}(q_{t-H:t})$ | [[2107.04034\|RMA]] adaptation module, [[2408.14472\|DWL]] denoising WM |
| **Perceptive (deployable + exteroception)** | $(q, e)$ | partially observed via $e$ | [[2604.17335\|G1 WBC-Gen+Track]], [[2602.15827\|PHP]] (depth) |

The central question is **how the unobserved $z$ is recovered or bounded**. Three operators answer it: an *inference* operator regresses $\hat z = f(q_{t-H:t})$ from proprioceptive history; a *perception* operator reads the anticipatory part of $z$ that lives in exteroception, $\hat z = g(e)$; and a *bounding* operator $u_{\text{epi}}(s,a)$ estimates how unreliable the learned dynamics are at $(s,a)$ and discounts the reward, $r \leftarrow r - \beta\, u_{\text{epi}}$, so the policy avoids acting where $z$ is effectively unknown. A1's perceptive bet, B1's proprioceptive bet, and B2's dreaming bet are three instantiations of this same recovery problem.

**The reference as a feasibility-constrained command.** When the command $c$ is a reference clip $\xi_{1:T}$, the tracking objective $\min_a \sum_t \lVert q_t - \xi_t \rVert$ is only well-posed if every $\xi_t$ lies on the robot's *dynamically-feasible manifold* $\mathcal{F}$ — the set of configurations and transitions the robot's torque, contact-timing, and balance limits actually permit. Raw human mocap violates $\mathcal{F}$ (a human backflip exceeds the robot's torque margins), so the imitation target must first be projected, $\xi \mapsto \Pi_{\mathcal F}(\xi)$, before the policy can track it. There are two places to apply $\Pi_{\mathcal F}$: *offline*, projecting a fixed pre-recorded clip once before any rollout (A2's regime), or *online*, generating a fresh reference each control window against the terrain seen at runtime and filtering it with an RL tracker (A1's regime). This reframing — feasibility of the *target*, not quantity of *data* — is the inverse of the "collect more demonstrations" reflex, and it is what A1 and A2 build on at opposite ends of the timeline.

**Cross-morphology portability.** A quadruped (12 DoF, ANYmal/Go2) and a humanoid (≥23 DoF, G1/H1) share *gait structure* — a phase-clocked foot-contact schedule and a velocity-tracking objective — even though their joint-space realization differs. This makes the locomotion control object more morphology-portable than the manipulation grasp object: [[2504.16680|RWM-U]] and [[2501.10100|RWM]] run the *same* world-model + MBRL pipeline across ANYmal D and Unitree G1 unchanged. The lever B2 and Cluster A both rest on is that the gait's *phase* is already a low-dimensional cross-morphology invariant, where a grasp needs a function-aligned action space to bridge hands.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Bipedal Locomotion & Dynamic Skills** | A1, A2, A3, A4, A5 | High-DoF whole-body balance under partial observation, where flat RL fails and the reference/constraint structure is the lever | A1's perceptive terrain policy needs the dynamic skills A2 makes feasible; A3's fall-recovery is the boundary case A1/A2 must survive when balance is lost; A4 grounds all three in real GRF/thermal limits; A5 supplies the off-policy/flow training substrate every other A-direction trains on. [[2604.17335\|G1 WBC-Gen+Track]] and [[2602.15827\|PHP]] set the bar for A1; [[2506.12851\|KungfuBot]] and [[2605.06593\|ReActor]] for A2 |
| **B — Quadruped Locomotion & Real-World Adaptation** | B1, B2, B3 | Recovering or bounding the unobserved physical state ($\mu$, $h$, payload, model error) for deployable locomotion | B1's proprioceptive inference is the floor B2's world model improves on by dreaming; B2's pretrained dynamics is what B3 plans through over long horizons; B3 adds the perceptive goal-reaching layer B1/B2 lack. [[2107.04034\|RMA]] and [[2604.02911\|DreamTIP]] are the shared levers across the cluster |

---

## Cluster A — Bipedal Locomotion & Dynamic Skills

*The humanoid's legs — whole-body balance and locomotion under partial observation, plus the dynamic agile skills (terrain traversal, parkour, dance, fall-recovery) that make a humanoid more than a slow walker. Where flat RL fails and the reference/constraint structure is the lever.*

### A1 — Perceptive Terrain Traversal & Vertical Mobility

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Generate the gait reference *online* against the terrain seen at runtime — a fresh reference each control window from the live height-scan, not a fixed gait library. The reason it must work: feasible foot-placement for a 75 cm box or a stair depends on the *perceived* local geometry ahead of the swing foot, information that no pre-computed reference can encode in advance. The field assumes a robust blind/flat-terrain tracker plus reactive recovery is enough for obstacle terrain. The bet is in First-principles below. |
| **Anchor papers** | [[2403.10506\|HumanoidBench]] (benchmark), [[2603.20147\|AGILE]] (benchmark), [[2408.14472\|DWL]] (method), [[2604.17335\|G1 WBC-Gen+Track]] (method), [[2602.15827\|PHP]] (method), [[2606.05880\|TAGA]] (method) |
| **Key targets** | [[2604.17335\|G1 WBC-Gen+Track]] 80 cm box-climb SR 0.962 (Tracker+Gen) vs 0.230 (Tracker-Only), 75 cm box + stairs + hurdles real; [[2606.05880\|TAGA]] 120 cm gap on a real G1 (+50% over prior perceptive max) at 65.2% lower training cost; [[2602.15827\|PHP]] 1.25 m wall (96% height) in 3.63 s + cat-vault 3.41 m/s + ~0.5 m perturbation recovery; [[2408.14472\|DWL]] zero-shot snowy-incline/stairs from proprioception alone |

**Why it matters.**
- **The gap**: a humanoid clearing a 75 cm box must commit its swing trajectory *before* the foot touches, so the policy needs the local geometry ahead of it — but the field's robust answer is a blind tracker that can only react after contact, and [[2403.10506|HumanoidBench]] sets the wall that flat RL "generally fails" on whole-body locomotion.
- **Today's answers**: [[2408.14472|DWL]] is the apex blind tracker — a denoising world model gives zero-shot snow/stairs from proprioception alone — but by the time a box is felt, the swing is committed; [[2604.17335|G1 WBC-Gen+Track]] closes that gap with a perceptive diffusion generator producing terrain-aware references over a 0.5 s horizon (0.962 vs 0.230 box-climb). Both walk; only one anticipates, and even it generates over a fixed horizon with no learned where-to-look.
- **The opening**: [[2604.17335|G1 WBC-Gen+Track]]'s 0.230→0.962 box-climb gap *is* the cost of blindness, and [[2606.05880|TAGA]] shows the perceptive ceiling is still rising — an *emergent* active-gaze module that learns where to look matches full-height-scan performance at 65.2% lower training cost and clears a 120 cm gap (+50% over the prior perceptive max).

**First-principles framing.**
- **First principle**: On obstacle terrain, feasible foot-placement and centre-of-mass trajectory depend on the *local geometry ahead of the swing foot* — information that lives in exteroception (depth / height-scan), not in proprioceptive history. By the time a blind policy feels a 75 cm box, the swing is already committed; the anticipatory signal is simply absent from $q$. [[2604.17335|G1 WBC-Gen+Track]] demonstrates this directly: removing the perceptive generator collapses 80 cm box-climbing from 0.962 to 0.230, a gap that exists no matter how robust the tracker.
- **Assumption being challenged**: That a robust blind tracker plus reactive recovery suffices for obstacle terrain. [[2408.14472|DWL]] (proprioception-only) is the strongest instance of that bet, and its boundary is exactly the anticipatory tasks; scaling proprioceptive robustness cannot close the 0.230→0.962 gap because the information is not in the proprioception. [[2606.05880|TAGA]] bets the opposite — perception is worth its cost — and proves it cheap (65.2% below full height-scan) once the policy learns *where* to look rather than processing everything.
- **The bet**: A perceptive gen+track policy with learned active gaze lifts 80 cm box SR from [[2604.17335|G1 WBC-Gen+Track]]'s Tracker-Only 0.230 to ≥0.95, chains into [[2602.15827|PHP]]-class parkour (1.25 m wall, peak 3.41 m/s) under ~0.5 m live perturbation, and *retains* [[2408.14472|DWL]]-class blind robustness on flat/rough terrain as the floor — anticipation added, robustness not traded. Falsifiable: if a blind [[2408.14472|DWL]]-style tracker + reactive recovery matches the perceptive policy on graded box heights, perception buys nothing.

**Related research papers.** One comparison table — the axis is *what perceptual signal conditions the gait and over what horizon* (blind / height-scan / depth / active-gaze / motion-matched), with what each leaves missing:

| System | Perceptual signal → gait | Reference horizon | Key result | What's missing |
|---|---|---|---|---|
| [[2604.17335\|G1 WBC-Gen+Track]] | terrain height-scan → diffusion-generated reference, RL-tracked | online, 0.5 s receding | 0.962 vs 0.230 (80 cm box), real box/stairs/hurdles | fixed 0.5 s horizon, no learned where-to-look — feeds the active-gaze bet |
| [[2606.05880\|TAGA]] | egocentric depth + height-scan + proprioception, **emergent active gaze** | online | 120 cm gap on real G1 (+50%), 65.2% cheaper than full scan | gaze is emergent but the reference is policy-implicit, not a generated clip |
| [[2602.15827\|PHP]] | onboard depth → motion-matched skill chain | online (chained skills) | 1.25 m wall (96%) in 3.63 s, cat-vault 3.41 m/s, ~0.5 m perturbation | skill graph is fixed/pre-composed — cannot synthesize a reference for an unseen obstacle |
| [[2408.14472\|DWL]] | none (proprioception, denoised) | reactive | zero-shot snow/stairs, robust to pushes + motor failure | blind — cannot anticipate a box; the robustness floor to retain, not the ceiling |
| [[2606.04718\|CoRe-MoE]] | terrain → contrastive-reweighted MoE gait selection | reactive (gait switch) | 99.13% flat SR, walk↔run zero-shot to 2.5 m/s real G1 | selects among gaits, doesn't generate a foot-placement reference for vertical terrain |
| [[2107.03996\|LocoTransformer]] | depth + proprioception fusion (quadruped) | reactive | 92% farther real, 290.5–663% fewer collisions sim | perception-fusion precedent, but obstacle *avoidance*, not vertical traversal |
| [[2503.10626\|NIL]] | video-diffusion reference (no real demos) | offline-generated | matches mocap-trained humanoid + quadruped locomotion | generates references but not *conditioned on perceived terrain* at runtime |
| [[2403.10506\|HumanoidBench]] | benchmark (12 locomotion tasks, 151D proprio) | — | flat RL fails; the exploration-wall framing | a difficulty suite, not a perceptive method |
| [[2603.20147\|AGILE]] | height-controlled locomotion in a deployment workflow | workflow | velocity-tracking + height-controlled + stand-up across 5 G1/T1 skills | standardizes deployment, leaves the perceptive-reference formulation open |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (anticipatory perception beats reactive recovery on obstacle terrain, robustness retained).
1. **H1 — The perceptive gain widens with obstacle height.**
   - *Prediction*: ablating [[2604.17335|G1 WBC-Gen+Track]]'s generator against a blind [[2408.14472|DWL]]-style tracker + recovery on graded box heights (20→80 cm), the 0.230→0.962 gap widens monotonically with height, confirming anticipation (not recovery) is the lever.
   - *Test*: sweep box height; report perceptive-minus-blind SR per height.
   - *Row*: G1 WBC-Gen+Track (online generated) vs DWL (blind).
   - *Falsifier*: a flat gap across heights → recovery suffices and perception isn't the lever.
2. **H2 — There is an optimal reference horizon under perturbation.**
   - *Prediction*: sweeping [[2604.17335|G1 WBC-Gen+Track]]'s 0.5 s generation horizon against [[2602.15827|PHP]]'s ~0.5 m perturbation, anticipation improves with horizon up to a point, then stale references hurt under disturbance — a non-monotone curve with an interior optimum.
   - *Test*: vary horizon length, measure SR under fixed perturbation magnitude.
   - *Row*: G1 WBC-Gen+Track (0.5 s receding) / PHP (chained).
   - *Falsifier*: SR rises monotonically with horizon → no staleness penalty, longer is always better.
3. **H3 — Active gaze matches full perception more cheaply as obstacles sparsify.**
   - *Prediction*: [[2606.05880|TAGA]]'s emergent active gaze closes the most cost gap (vs full height-scan) precisely on tasks needing *distant* foothold planning (sparse stepping stones, 70 cm spacing), and ties full-scan on dense terrain — the 65.2%-cheaper win concentrates where coverage matters.
   - *Test*: stratify by foothold sparsity; report gaze-vs-full-scan cost and SR per stratum.
   - *Row*: TAGA (active gaze).
   - *Falsifier*: gaze underperforms full-scan on sparse footholds → learned attention drops task-critical regions.
4. **H4 — A generated reference library chains into a multi-obstacle course no fixed graph covers.**
   - *Prediction*: composing [[2602.15827|PHP]]'s motion-matching skill graph with [[2604.17335|G1 WBC-Gen+Track]]'s online generation clears a multi-obstacle course that PHP's fixed skill graph alone fails, because the generator synthesizes transitions for obstacle combinations absent from the graph.
   - *Test*: build a course mixing seen skills in unseen order; compare chained-generation vs fixed-graph SR.
   - *Row*: PHP (fixed skill chain) + G1 WBC-Gen+Track (online generated).
   - *Falsifier*: the fixed graph matches chained generation → composition over a fixed library suffices.
5. **H5 — Blind robustness survives as a fallback under perception dropout.**
   - *Prediction*: when exteroception degrades (occlusion, darkness), a perceptive policy with a [[2408.14472|DWL]]-style proprioceptive safety mode underneath falls back gracefully on flat/rough terrain rather than catastrophically, where a perception-only policy fails.
   - *Test*: inject depth dropout mid-traverse on flat terrain; compare fall rate with vs without the proprioceptive fallback.
   - *Row*: DWL (blind floor) under G1 WBC-Gen+Track (perceptive).
   - *Falsifier*: the fallback doesn't recover flat-terrain stability under dropout → perception failure is unavoidably catastrophic.

> [!warning] Risks
> - **Perception failure is catastrophic, not graceful** — a depth dropout mid-vault can be fatal where a blind policy would have stumbled and recovered. → H5 is the go/no-go; require a [[2408.14472|DWL]]-class proprioceptive safety mode underneath the perceptive policy (couples to A3's recovery layer) and report fall rate under induced dropout.
> - **Generated references can be infeasible** — the generator may propose what the tracker cannot execute. → [[2604.17335|G1 WBC-Gen+Track]]'s RL fine-tuning filters them; report the tracker's reject/clamp rate, not just headline SR.
> - **Parkour-class skills risk hardware damage** — 1.25 m walls and 3.41 m/s vaults stress real humanoids. → Bound aggressive-skill claims to validated platforms; report contact-force and motor-temperature (couples to A4).

### A2 — Dynamic Agile Skills via Physically-Feasible Motion Imitation

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Project a *fixed, pre-recorded mocap clip* onto the robot's dynamically-feasible manifold *offline, before* imitation — a one-time fix of a given motion, distinct from A1's per-step generation against live terrain. The reason it must work: the tracking objective is ill-posed when the reference breaks the robot's torque/contact/balance limits, so the policy chases a target it can never reach. The field's reflex is "collect more demonstrations," as if data quantity were the bottleneck. The bet is in First-principles below. |
| **Anchor papers** | [[2403.10506\|HumanoidBench]] (benchmark), [[2603.20147\|AGILE]] (benchmark), [[2506.12851\|KungfuBot]] (method), [[2605.06593\|ReActor]] (method), [[2605.10063\|EFGCL]] (method) |
| **Key targets** | [[2506.12851\|KungfuBot]] 53.25 mm global mean body-position error (easy) vs OmniH2O/ExBody2 >233 mm, untrackable-motion rejection (max 54% episode-length ratio); [[2605.06593\|ReActor]] 0.00% penetration + 0.17 cm/s foot-slide + 97.45% (G1) / 95.07% (Lima) downstream RL (+15.22 pp); [[2605.10063\|EFGCL]] backflip/lateral-flip unlearnable by PPO + 2× faster jump |

**Why it matters.**
- **The gap**: a human backflip breaks the robot's torque limits, contact timing, and balance margins, so a policy asked to imitate raw mocap optimizes toward a target it physically cannot reach — yet the reflexive recipe for a new agile skill is "imitate more human motion."
- **Today's answers**: [[2506.12851|KungfuBot]] fixes the target instead of the data — a physics pipeline filters untrackable sequences and corrects contact, hitting 53.25 mm where deployable baselines (OmniH2O, ExBody2) exceed 233 mm, a 4× cut; [[2605.06593|ReActor]] makes the same move via RL physics-aware retargeting (zero penetration, 97.45% downstream RL, +15.22 pp). Both correct feasibility, but each fixes a clip in isolation and neither *expands* the feasible set.
- **The opening**: [[2506.12851|KungfuBot]]'s rejection statistic is the legible mechanism — accepted motions yield high episode-length ratios while rejected ones collapse (max 54%) — and [[2605.10063|EFGCL]] shows feasibility is not a hard ceiling: a force-guided curriculum *grows* the feasible manifold to reach backflips a PPO baseline cannot learn at all.

**First-principles framing.**
- **First principle**: Asking a policy to track a reference only makes sense if that reference lies on what the robot can physically do — its torque, contact-timing, and balance limits. Raw human mocap does not, so the first operation is the projection $\xi \mapsto \Pi_{\mathcal F}(\xi)$ onto the dynamically-feasible manifold; only then is the imitation loss well-posed. This is prior to any question of how much data you have. [[2506.12851|KungfuBot]] demonstrates it: *filtering* untrackable motions (not adding data) delivers the 233→53 mm cut.
- **Assumption being challenged**: That agile-skill competence scales with demonstration quantity. The field collects ever-larger mocap corpora ([[2606.03985|Humanoid-GPT]]'s 2B frames, [[2511.07820|SONIC]]'s 100M); [[2506.12851|KungfuBot]]'s 4× error cut from *rejection* and [[2605.06593|ReActor]]'s +15.22 pp from *zero-penetration retargeting* show the binding constraint is reference feasibility, not volume — the data-scale line and the feasibility-first line bet opposite things about what's scarce.
- **The bet**: A physics-corrected reference pipeline cuts tracking error to [[2506.12851|KungfuBot]]'s 53.25 mm (vs >233 mm OmniH2O/ExBody2) and lifts downstream RL to [[2605.06593|ReActor]]'s 97.45% (G1) at zero ground/self-penetration, enabling [[2605.10063|EFGCL]]-class extreme skills (backflips) on small data — feasibility-first, not data-scale. Falsifiable: if a data-scaled tracker on raw mocap ([[2606.03985|Humanoid-GPT]]-style) matches the feasibility-filtered pipeline at equal compute, feasibility correction buys nothing scale cannot.

**Related research papers.** One comparison table — the axis is *how the reference is made feasible* (filter / retarget / curriculum-expand / generate / data-scale), with what each leaves missing:

| System | Feasibility operation | When applied | Key result | What's missing |
|---|---|---|---|---|
| [[2506.12851\|KungfuBot]] | filter untrackable mocap + adaptive tracking factor | offline, per-clip | 53.25 mm vs >233 mm OmniH2O/ExBody2; max 54% rejection ratio | discards expressive-but-infeasible clips rather than expanding feasibility |
| [[2605.06593\|ReActor]] | RL physics-aware retargeting (bilevel) | offline, per-clip | 0.00% penetration, 0.17 cm/s slide, 97.45% (G1) downstream RL (+15.22 pp) | corrects penetration but doesn't reject fundamentally untrackable dynamics |
| [[2605.10063\|EFGCL]] | external-force curriculum *expands* the feasible set | during training | backflip/lateral-flip unlearnable by PPO, 2× faster jump | grows feasibility for one skill at a time, no reusable manifold |
| [[2606.03476\|Human2Humanoid]] | unsupervised cross-morphology retarget + EE-consistency loss | offline, per-clip | 88.5% SR, 0.05 cm penetration, 4.7% foot-slide | retargets across bodies but no adaptive tracking-tolerance schedule |
| [[2603.22201\|NMR]] | transformer retargeting filters jitter/self-collision | offline, per-clip | zero joint jumps, 54% fewer self-collisions (0.87% of frames) | smooths motion, no downstream-RL trainability metric |
| [[2606.03536\|Bionic Whole-Body Control]] | physics-regularized latent-diffusion → executable reference | offline (generate) | 96.0% real-G1 SR, 0.004722 m/frame foot-slide | feasibility for *style transfer*, not the full agile-skill range |
| [[2606.01851\|PHASOR]] | phase-anchored universal action representation | representation | 1.62 mm MPJPE, 90.3% R@1 cross-embodiment retrieval | structures the imitation target by phase, doesn't filter infeasibility |
| [[2511.07820\|SONIC]] | scale tracking to 100M frames / 42M params | data-scale | 99.6% OOD-tracking SR sim, real-G1 zero-shot on all 50 trajectories | the data-scale counterpoint — feasibility-first claims it's over-scaled |
| [[2606.03985\|Humanoid-GPT]] | GPT-style tracking on a 2B-frame corpus | data-scale | 92.58% SR, <1.5 ms inference | the strongest data-scale bet — the head-to-head H1 must beat |
| [[2504.11054\|Meta Motivo]] | FB-CPR behavioral foundation model, no per-task reward | learned latent | preferred over reward-optimized agents, natural motion | empirical feasibility, not an explicit projection onto $\mathcal F$ |
| [[2405.18418\|Puppeteer]] | hierarchical TD-MPC2 tracking abstract mocap (56-DoF) | two-level | 97.8% naturalness (51 participants), zero-shot to 3× larger gaps | tracks abstract references, no physics-feasibility filter on the clip |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (reference feasibility, not data quantity, is the lever for agile skills).
1. **H1 — Filter-then-track beats track-raw and rivals data-scale at equal compute.**
   - *Prediction*: pre-filtering untrackable mocap ([[2506.12851|KungfuBot]]-style) delivers the 233→53 mm cut over raw mocap and *matches or beats* a data-scaled tracker ([[2606.03985|Humanoid-GPT]]-style) at equal training compute, with the gain concentrated on dynamic (not quasi-static) skills.
   - *Test*: three-arm comparison — raw-track / filter-then-track / data-scale — at fixed FLOPs; stratify by skill dynamism.
   - *Row*: KungfuBot (filter) vs Humanoid-GPT (data-scale).
   - *Falsifier*: data-scale matches filter-then-track at equal compute on dynamic skills → feasibility correction is redundant with scale.
2. **H2 — An adaptive tracking factor learns skills a fixed tolerance cannot.**
   - *Prediction*: [[2506.12851|KungfuBot]]'s adaptive reward-tolerance curriculum learns dynamic skills (martial-arts, flips) that a fixed-tolerance reward fails to acquire, because early-loose / late-tight tolerance escapes the local optima a fixed reward traps in.
   - *Test*: ablate adaptive vs fixed tracking factor on a dynamic-skill set; report learnability and final error.
   - *Row*: KungfuBot (adaptive tracking factor).
   - *Falsifier*: fixed tolerance matches adaptive on dynamic skills → the curriculum isn't the lever.
3. **H3 — Retargeting feasibility predicts downstream trainability.**
   - *Prediction*: [[2605.06593|ReActor]]'s penetration/foot-slide metrics are monotone predictors of downstream RL success — cleaner retargeting → higher SR — so feasibility quality, not data quantity, sets the +15.22 pp ceiling.
   - *Test*: sweep retargeting quality (degrade penetration/slide deliberately); plot the feasibility→RL-SR curve.
   - *Row*: ReActor (retarget) → Human2Humanoid (cross-morphology retarget).
   - *Falsifier*: SR is flat across feasibility quality → trainability is decoupled from retargeting fidelity.
4. **H4 — A force curriculum expands feasibility to skills filtering would reject.**
   - *Prediction*: [[2605.10063|EFGCL]]'s force-guided curriculum acquires backflips/lateral-flips that [[2506.12851|KungfuBot]]'s filter would discard as untrackable, and the two *compose* — filter the trackable clips, expand the rest — covering more of the agile-skill range than either alone.
   - *Test*: classify a skill set by KungfuBot's rejection; apply EFGCL to the rejected set; report recovered-skill fraction.
   - *Row*: EFGCL (expand) + KungfuBot (filter).
   - *Falsifier*: EFGCL fails to recover rejected skills → feasibility is a hard ceiling, not an expandable set.
5. **H5 — Phase-structured references retarget across bodies without re-filtering.**
   - *Prediction*: anchoring the reference on motion *phase* ([[2606.01851|PHASOR]]) lets a feasibility-corrected clip transfer across embodiments ([[2606.03476|Human2Humanoid]]-style) with the feasibility property preserved, so one projection amortizes across bodies rather than re-filtering per platform.
   - *Test*: project a clip on body A, retarget to body B via phase anchoring, measure penetration/slide on B without re-filtering.
   - *Row*: PHASOR (phase representation) + Human2Humanoid (cross-morphology).
   - *Falsifier*: feasibility degrades on body B → the projection is body-specific, no amortization.

> [!warning] Risks
> - **Physics-filtering needs an accurate robot model** — correction is only as good as the URDF/dynamics. → Validate the feasibility manifold against hardware; report the sim-vs-real tracking-error gap ([[2506.12851|KungfuBot]] reports a close match).
> - **Filtering discards expressive motions** — rejecting "untrackable" mocap may cut the most striking skills. → Couple filtering with [[2605.10063|EFGCL]]-style force-guidance that *expands* feasibility (H4); report the recovered-skill fraction, not just rejection rate.
> - **Downstream-RL gains may be task-specific** — +15.22 pp may not transfer to novel skills. → H3's feasibility→trainability curve tests generality; report across skill classes, not a single average.

### A3 — Autonomous Fall Recovery as Non-Periodic Whole-Body Control

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Treat getting-up as its own non-periodic, rich-contact, sparse-reward control problem, not a degenerate gait. The reason it must work: fall-recovery has no phase clock and no nominal contact schedule, so the periodicity and foot-contact priors that make locomotion learnable actively mislead it. The field assumes a locomotion policy plus a scripted recovery routine is enough for autonomy. The bet is in First-principles below. |
| **Anchor papers** | [[2502.12152\|HUMANUP]] (method), [[2403.10506\|HumanoidBench]] (benchmark), [[2603.20147\|AGILE]] (benchmark) |
| **Key targets** | [[2502.12152\|HUMANUP]] 78.3% getting-up (supine) + 98.3% roll-over real on 6 terrains (concrete/muddy-grass/snow), ~6 s vs manufacturer 11 s, 20,000 randomized initial postures, lower arm-motor temperature; single-stage training fails to converge; [[2603.20147\|AGILE]] stand-up among its 5 demonstrated G1/T1 skills as the workflow baseline |

**Why it matters.**
- **The gap**: a humanoid that cannot stand up after a fall is not autonomous — it needs a human — yet getting-up has no gait cycle, an arbitrary post-fall configuration, and a single binary reward at the end, so the locomotion playbook's inductive biases work *against* it.
- **Today's answers**: manufacturer controllers *script* recovery and fail on most challenging terrains; [[2502.12152|HUMANUP]] instead learns it with a two-stage curriculum — a Discovery Policy finds a fast trajectory through the sparse-reward landscape, a Deployable Policy refines it over 20,000 lying postures — reaching 78.3% supine / 98.3% roll-over on a real G1 across 6 terrains in ~6 s (vs 11 s). A learned recovery exists, but only for one platform and one fall distribution.
- **The opening**: [[2502.12152|HUMANUP]] reports the load-bearing fact directly — *single-stage training fails to converge* — so motion *discovery*, not refinement, is the bottleneck on the sparse-reward landscape, and that is the structural lever a script can never have.

**First-principles framing.**
- **First principle**: Fall-recovery has no phase clock and no nominal contact schedule — the initial state is an arbitrary post-fall configuration and the contact set is unknown. The phase-clocked, foot-contact-prior structure that makes locomotion well-shaped is *absent*; imposing it biases the policy away from the contact-rich ground transitions recovery needs. [[2502.12152|HUMANUP]] shows the consequence: a single-stage policy (the locomotion default) fails to converge, and only separating discovery from deployment makes the sparse-reward landscape tractable.
- **Assumption being challenged**: That a locomotion policy plus a scripted recovery routine yields autonomy. Manufacturer controllers script recovery and fail on most terrains ([[2502.12152|HUMANUP]] reports this); a script cannot cover the continuum of post-fall configurations, and a periodic policy carries the wrong bias for non-periodic ground-up motion — the two failure modes share a root: imposing locomotion structure where none exists.
- **The bet**: A two-stage discover-then-deploy curriculum recovers from arbitrary fall configurations at [[2502.12152|HUMANUP]]'s 78.3% supine / 98.3% roll-over in ~6 s (vs manufacturer 11 s and most-terrain failure) across ≥6 terrains, with single-stage training failing to converge — confirming motion *discovery*, not refinement, is the load-bearing stage. Falsifiable: if a single-stage policy or a scripted routine matches the two-stage curriculum across terrains, the discovery stage is not the lever.

**Related research papers.** One comparison table — the axis is *how the recovery / contact-rich motion is acquired* (two-stage discovery / scripted / workflow / generated / push-robust precursor), with what each leaves missing:

| System | Recovery acquisition | Periodicity assumption | Key result | What's missing |
|---|---|---|---|---|
| [[2502.12152\|HUMANUP]] | two-stage discover-then-deploy RL curriculum | none (non-periodic by design) | 78.3% supine / 98.3% roll-over, 6 terrains, ~6 s vs 11 s, 20,000 postures | single platform, single fall distribution |
| [[2603.20147\|AGILE]] | stand-up via deployment workflow (value-bootstrapped terminations + virtual harness) | workflow-stabilized | stand-up among 5 G1/T1 skills, sim-validated | no arbitrary-config robustness; stand-up is one workflow skill, not a recovery study |
| [[2604.17335\|G1 WBC-Gen+Track]] | RL-filtered *generated* contact-rich motion | reference-driven | 0.962 vs 0.230 box-climb, real | generation-side analogue, but for terrain traversal not arbitrary post-fall states |
| [[2605.10063\|EFGCL]] | force-guided curriculum for high-risk contact-rich skills | none (flips/jumps) | backflip/lateral-flip unlearnable by PPO | the contact-rich-skill-acquisition precedent, not recovery-specific |
| [[2502.08844\|MuJoCo Playground]] | GPU sim for large-scale posture randomization | — | minutes/hours training, vision-based policies | the 20,000-posture training substrate, not a recovery method |
| [[2512.01996\|Humanoid Loco 15min]] | push-robust locomotion (the disturbance preceding a fall) | periodic | 15-min sim-to-real G1+T1, push-robust | the *pre-fall* balance layer recovery backstops, not recovery itself |
| [[2505.22642\|FastTD3]] | off-policy RL on sparse-reward HumanoidBench tasks | — | solves HumanoidBench <3 hrs | the sample-efficient substrate for sparse recovery (feeds A5), not recovery-specific |
| [[2403.10506\|HumanoidBench]] | benchmark with sparse-reward whole-body tasks | — | flat RL fails; high-DoF exploration wall | the difficulty diagnostic, not a recovery method |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (recovery is a distinct non-periodic problem needing discovery, not a recovery bolt-on).
1. **H1 — The discovery stage is the load-bearing stage.**
   - *Prediction*: ablating [[2502.12152|HUMANUP]]'s Discovery Policy (training Stage II directly) fails to converge or yields drastically lower SR, confirming motion *discovery* on the sparse-reward landscape — not refinement — carries the result.
   - *Test*: train single-stage vs two-stage on identical posture/terrain distributions; report convergence and SR.
   - *Row*: HUMANUP (two-stage discovery).
   - *Falsifier*: single-stage converges to comparable SR → the discovery stage is dispensable.
2. **H2 — Posture coverage sets arbitrary-config robustness.**
   - *Prediction*: sweeping the number of randomized lying postures toward [[2502.12152|HUMANUP]]'s 20,000, success on held-out post-fall configurations rises sub-linearly to a coverage threshold beyond which more postures add little.
   - *Test*: vary posture count; report held-out-config SR per count.
   - *Row*: HUMANUP (two-stage discovery).
   - *Falsifier*: SR scales linearly with postures with no saturation → coverage is unbounded and the 20,000 figure is arbitrary.
3. **H3 — Terrain-conditioned recovery beats terrain-blind on extreme surfaces.**
   - *Prediction*: conditioning the Deployable Policy on perceived terrain (slope, compliance) beats [[2502.12152|HUMANUP]]'s terrain-blind policy specifically on snow/mud, where ground compliance changes the feasible push-off, and ties on rigid concrete.
   - *Test*: compare terrain-conditioned vs blind recovery, stratified by surface compliance.
   - *Row*: HUMANUP (two-stage discovery).
   - *Falsifier*: terrain conditioning doesn't help on compliant surfaces → recovery is compliance-invariant.
4. **H4 — A periodic prior actively hurts non-periodic recovery.**
   - *Prediction*: injecting a phase-clock / foot-contact prior (the locomotion inductive bias) into the recovery policy *lowers* SR versus the prior-free [[2502.12152|HUMANUP]] formulation, because it biases toward gait-like transitions the ground-up motion doesn't use.
   - *Test*: add a periodicity prior to the recovery policy; report SR delta vs prior-free.
   - *Row*: HUMANUP (non-periodic) vs [[2512.01996|Humanoid Loco 15min]] (periodic locomotion).
   - *Falsifier*: the periodic prior is neutral or helps → locomotion structure transfers to recovery.
5. **H5 — A unified locomotion+recovery stack reaches end-to-end autonomy.**
   - *Prediction*: wiring fall-recovery as the fallback when A1's perceptive policy loses balance (perception dropout, push beyond recovery margin) yields a stack that completes a multi-obstacle course *including* falls without human intervention, where locomotion-only fails on the first fall.
   - *Test*: run a course with induced falls; compare end-to-end completion with vs without the recovery fallback.
   - *Row*: HUMANUP (recovery) under [[2604.17335|G1 WBC-Gen+Track]] (perceptive locomotion).
   - *Falsifier*: the unified stack doesn't improve end-to-end completion → recovery and locomotion don't compose into autonomy.

> [!warning] Risks
> - **Recovery motions stress hardware** — flailing limbs and ground impacts risk motor/joint damage. → [[2502.12152|HUMANUP]]'s strong regularization lowers arm-motor temperature; report contact-force and temperature, treat smoothness as a first-class objective (couples to A4).
> - **Discovery may find unsafe trajectories** — weak regularization can produce violent motions infeasible for hardware. → The two-stage design refines discovery into a deployable policy; report the discovery→deployment safety-margin gap.
> - **Real falls exceed simulation coverage** — 20,000 postures may miss adversarial real falls. → H2's coverage curve bounds the claim; report failure modes by initial-configuration class, not a single average.

### A4 — Embodiment-Grounded Locomotion Constraints (Force, Acoustic, Thermal)

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Make the *physical cost* of a gait — ground-reaction force, noise, motor heat — a first-class predicted-and-regulated quantity, not an ignored externality. The reason it must work: a real robot's gait is bounded by hard embodiment limits (motor temperature, contact force, noise budgets) that exist *off* the sim reward surface, so a task-only reward saturates them invisibly until the hardware fails. The field assumes task-success rewards alone yield deployable gaits, and no existing policy regulates more than one such cost at once. The bet is in First-principles below. |
| **Anchor papers** | [[2604.23702\|QuietWalk]] (method), [[2605.27046\|Thermal-Aware Residual]] (method), [[2603.20147\|AGILE]] (benchmark), [[2403.10506\|HumanoidBench]] (benchmark) |
| **Key targets** | [[2604.23702\|QuietWalk]] GRF-predictor RMSE 14.49/14.00 N (R²=0.9887/0.9899), noise reduction 7.17 dBA mean / 4.98 dBA peak across 4 footwear types (barefoot→high heels) + outdoor terrains; [[2605.27046\|Thermal-Aware Residual]] motor-overheating 70%→<10%, 650 m outdoor + 3 kg payload, peak temp <50 °C |

**Why it matters.**
- **The gap**: simulation rewards task success — reach the velocity, climb the box — and silently omits the physical cost the real robot pays: motors overheat, gaits are loud, contact forces spike, and these are deployment-fatal, not cosmetic.
- **Today's answers**: [[2605.27046|Thermal-Aware Residual]] takes the heat axis — overheating hits 70% on hot terrain without thermal management (a robot that shuts down has zero success regardless of policy), and a residual thermal policy drops it to <10% while completing 650 m outdoor with a 3 kg payload below 50 °C; [[2604.23702|QuietWalk]] takes the acoustic + contact axis — a physics-informed GRF predictor (R²≈0.99) drives a quiet RL policy cutting noise 7.17 dBA mean across 4 footwear types. Each regulates *one* cost in isolation.
- **The opening**: [[2604.23702|QuietWalk]]'s GRF predictor hits R²≈0.99 from proprioception alone, so the force signal needed to *trade off* costs is already predictable — the missing piece is one head regulating heat, noise, and force jointly, not two policies each blind to the other's objective.

**First-principles framing.**
- **First principle**: A real robot's gait is bounded by hard embodiment limits — motor-temperature ceilings, actuator force limits, and (around people) noise budgets — that exist *off* the sim reward surface. A policy optimizing only task success saturates these limits because nothing penalizes them; the cost is invisible until the hardware fails or the gait is unacceptable. [[2605.27046|Thermal-Aware Residual]]'s 70% overheating under standard policies is the direct evidence: the embodiment cost is load-bearing for deployment, not a second-order concern.
- **Assumption being challenged**: That task-success rewards alone yield deployable gaits. The field tunes velocity-tracking and terrain rewards; [[2605.27046|Thermal-Aware Residual]] (a thermally-blind policy is undeployable on hot terrain regardless of its tracking reward) and [[2604.23702|QuietWalk]] (a standard RL policy is unacceptably loud near people) both bet the opposite — that an embodiment-cost objective is a *distinct* lever from task success, and a quiet/cool/low-impact gait is a different objective, not a free byproduct of a good tracker.
- **The bet**: A *single* physics-informed residual cost-head, driven by a GRF predictor at [[2604.23702|QuietWalk]]'s R²≈0.99, *jointly* holds overheating below [[2605.27046|Thermal-Aware Residual]]'s <10% (from 70%) **and** noise within +1 dBA of [[2604.23702|QuietWalk]]'s quiet-policy mean, at ≤5% task-SR loss versus the cost-blind base — one head trading the costs off, not two policies in isolation. Falsifiable: if joint regulation costs more than +5% task-SR or cannot hold both bounds simultaneously, the costs are irreducibly separate objectives.

**Related research papers.** One comparison table — the axis is *which embodiment cost is regulated and how* (predict-then-regulate / residual / hard-constraint / diagnostics / temperature-precedent), with what each leaves missing:

| System | Cost regulated | Mechanism | Key result | What's missing |
|---|---|---|---|---|
| [[2604.23702\|QuietWalk]] | acoustic + contact (GRF) | PINN GRF predictor folded into the RL reward | R²=0.9887/0.9899, 7.17 dBA mean / 4.98 dBA peak, 4 footwear | single-cost (no thermal); the GRF predictor is the joint-cost enabler |
| [[2605.27046\|Thermal-Aware Residual]] | motor temperature | residual thermal policy over a base controller | 70%→<10% overheating, 650 m + 3 kg, <50 °C | single-cost (no acoustic/GRF); the residual structure the joint head extends |
| [[2605.25546\|ISSf-CBF WBC]] | hard joint/workspace limits | input-to-state-safe control-barrier filter | collision-free vs ~50% standard CBF at 20% mass mismatch | enforces hard limits, doesn't *optimize* soft costs like heat/noise |
| [[2502.12152\|HUMANUP]] | motor temperature (incidental) | strong control regularization | lower/safer arm-motor temperature during recovery | temperature is a byproduct of regularization, not a predicted-and-regulated objective |
| [[2603.20147\|AGILE]] | motion-quality (jerk/limit/accel) | L2C2 regularization + HTML diagnostics | lowers RMS joint acceleration/jerk; cost diagnostics | *measures* cost (the diagnostics A4 reports) but doesn't predict-and-regulate force/heat/noise |
| [[2604.24916\|asRoBallet]] | friction / contact (underactuated) | friction-aware MuJoCo modeling | 0.05 m/s MAE, recovers from 0.3 m pushes | models contact physics for one underactuated platform, not a cost-objective |
| [[2512.01996\|Humanoid Loco 15min]] | none (long-duration deployment) | fast off-policy training | 15-min sim-to-real, 2-min dance on real G1 | the long-deployment substrate where thermal/wear costs compound, no cost regulation |
| [[2403.10506\|HumanoidBench]] | none (high-DoF actuator stress) | benchmark | flat RL fails on whole-body tasks | scores task success, not the embodiment cost a gait pays |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (embodiment costs are a distinct, jointly-regulable lever, not a free byproduct of a good tracker).
1. **H1 — Predicting force regulates contact better than penalizing it after the fact.**
   - *Prediction*: [[2604.23702|QuietWalk]]'s GRF-predictor-driven policy (R²≈0.99) regulates contact noise better than a penalty-only quiet policy that penalizes *measured* force, because prediction acts before the impact rather than after.
   - *Test*: compare predictor-in-reward vs measured-force-penalty at matched noise budget; report contact-force peaks and noise.
   - *Row*: QuietWalk (predict-then-regulate).
   - *Falsifier*: penalty-only matches predict-then-regulate → prediction adds nothing over reactive penalty.
2. **H2 — A residual cost-head preserves terrain adaptability where a monolith doesn't.**
   - *Prediction*: [[2605.27046|Thermal-Aware Residual]]'s residual structure preserves terrain adaptability that a monolithic cost-policy loses (the paper notes monoliths respond slowly and fail complex terrain), so decoupling cost-regulation from the base policy is the load-bearing design choice.
   - *Test*: compare residual vs monolithic cost-policy on complex terrain at matched thermal bound; report terrain SR.
   - *Row*: Thermal-Aware Residual (residual).
   - *Falsifier*: a monolithic cost-policy matches the residual on complex terrain → decoupling is unnecessary.
3. **H3 — GRF prediction generalizes to unseen contact interfaces.**
   - *Prediction*: [[2604.23702|QuietWalk]]'s GRF predictor, trained across barefoot→high-heels, generalizes to *unseen* interfaces (ice, soft ground) with R² degrading gracefully, and the noise/force objective transfers with it.
   - *Test*: hold out a footwear/surface class; report predictor R² and noise on the held-out interface.
   - *Row*: QuietWalk (acoustic + GRF).
   - *Falsifier*: R² collapses on unseen interfaces → the predictor is interface-specific, not a transferable cost model.
4. **H4 — One joint cost-head dominates two single-cost policies.**
   - *Prediction*: a unified head regulating heat + acoustic + force holds overheating <10% **and** noise within +1 dBA of QuietWalk's mean at ≤5% task-SR loss, dominating the two single-cost policies run independently — and the costs trade off measurably (a quieter gait runs hotter).
   - *Test*: train the joint head; compare its Pareto frontier against QuietWalk and Thermal-Aware Residual run separately.
   - *Row*: QuietWalk (acoustic) + Thermal-Aware Residual (thermal).
   - *Falsifier*: the joint head cannot hold both bounds at ≤5% SR loss → the costs are irreducibly separate objectives.
5. **H5 — Cost-aware training preserves task SR within a bounded budget.**
   - *Prediction*: there is a measurable cost-regulation budget below which task SR loss stays ≤5% (the bet's threshold), and above which a quiet/cool gait becomes meaningfully slower — a Pareto front, not a single operating point.
   - *Test*: sweep the cost-regulation weight; report the task-SR-vs-cost Pareto front.
   - *Row*: Thermal-Aware Residual (residual) / QuietWalk (predict-then-regulate).
   - *Falsifier*: any cost regulation collapses task SR past 5% → embodiment costs cannot be regulated at deployable performance.

> [!warning] Risks
> - **Cost-regulation can degrade task performance** — a quiet/cool gait may be slower or less agile. → [[2605.27046|Thermal-Aware Residual]] keeps performance via a residual; report the cost-vs-task Pareto front (H5), not a single number.
> - **GRF/thermal models are platform-specific** — R²≈0.99 on one robot may not transfer. → H3 tests generalization; treat cost predictors as per-platform-calibrated and report the transfer gap.
> - **Acoustic metrics are environment-dependent** — dBA depends on surface and room. → [[2604.23702|QuietWalk]] reports across 4 surfaces; report noise per surface, not a single average.

### A5 — Sample-Efficient Off-Policy & Flow Locomotion Learning

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Replace PPO — the field's reflexive default — with off-policy and flow-based RL for humanoid locomotion. The reason it must work: locomotion's dense reward and massively-parallel sim make sample-reuse and large-batch off-policy updates strictly more efficient than on-policy rollout-discard. The field assumes PPO's stability is worth its sample-inefficiency for high-DoF control. The bet is in First-principles below. |
| **Anchor papers** | [[2403.10506\|HumanoidBench]] (benchmark), [[2502.08844\|MuJoCo Playground]] (benchmark), [[2603.20147\|AGILE]] (benchmark), [[2505.22642\|FastTD3]] (method), [[2512.01996\|Humanoid Loco 15min]] (method), [[2602.02481\|FPO++]] (method) |
| **Key targets** | [[2505.22642\|FastTD3]] solves HumanoidBench tasks <3 hrs on one A100 (beats PPO/SAC/SimbaV2/TDMPC2/DreamerV3 wall-clock), real Booster T1, batch 32,768 + distributional critic; [[2512.01996\|Humanoid Loco 15min]] sim-to-real G1+T1 in 15 min on one RTX 4090; [[2602.02481\|FPO++]] first sim-to-real flow-policy RL for humanoid locomotion |

**Why it matters.**
- **The gap**: almost every locomotion paper above trains with PPO — chosen for stability — but locomotion has a *dense* reward (velocity tracking signals every step) and *massively-parallel* sim (thousands of environments), the two conditions that make on-policy rollout-discard most wasteful.
- **Today's answers**: [[2505.22642|FastTD3]] proves the cost — a simple off-policy TD3 with batch 32,768 and a distributional critic solves HumanoidBench tasks in under 3 hours on one A100, beating PPO, SAC, SimbaV2, TDMPC2, *and* DreamerV3 on wall-clock, transferring to a real Booster T1; [[2512.01996|Humanoid Loco 15min]] reaches a deployable G1/T1 gait in 15 minutes on one RTX 4090; [[2602.02481|FPO++]] opens the flow-policy axis (first sim-to-real flow-policy RL for humanoid locomotion). Each beats PPO, but the wall-clock dominance is shown task-by-task, not yet across the full locomotion suite.
- **The opening**: [[2505.22642|FastTD3]] reports that "complex architectural stabilizers were found unnecessary" — the off-policy win comes from sample-reuse and large batches, not heavy machinery — so the PPO habit is leaving an order of magnitude on the table for a stability premium the dense-reward regime doesn't need.

**First-principles framing.**
- **First principle**: Sample efficiency is governed by how often each environment step informs a gradient update. Off-policy replay reuses every transition many times; on-policy PPO discards each rollout after one update. With locomotion's dense reward and parallel sim (cheap, individually-informative transitions), the off-policy advantage compounds. [[2505.22642|FastTD3]] demonstrates it: large-batch off-policy updates with a distributional critic — and *no* complex stabilizers — beat PPO, DreamerV3, and TDMPC2 on wall-clock.
- **Assumption being challenged**: That PPO's stability is worth its sample-inefficiency for high-DoF locomotion. The field defaults to PPO nearly everywhere in this doc; [[2505.22642|FastTD3]]'s wall-clock win over PPO *and* the model-based DreamerV3/TDMPC2, plus [[2604.04539|FlashSAC]]'s ~order-of-magnitude cut over PPO across 60+ tasks, show the stability premium is overpriced when transitions are dense and plentiful — the opposite bet to the PPO consensus.
- **The bet**: An off-policy/flow learner solves [[2403.10506|HumanoidBench]] tasks in [[2505.22642|FastTD3]]'s <3 hours (beating DreamerV3/TDMPC2/PPO on wall-clock) and trains a deployable humanoid gait in [[2512.01996|Humanoid Loco 15min]]'s 15 minutes on a single consumer GPU — off-policy/flow dominance on wall-clock-to-deployment, PPO left behind. Falsifiable: if PPO matches off-policy wall-clock on dense-reward locomotion at equal environment count, the sample-reuse advantage isn't real.

**Related research papers.** One comparison table — the axis is *the learning substrate* (off-policy / flow / model-based / pretrain-finetune / real-world / MPC) and its wall-clock-to-deployable cost:

| System | Learning substrate | Wall-clock claim | Key result | What's missing |
|---|---|---|---|---|
| [[2505.22642\|FastTD3]] | off-policy TD3, batch 32,768 + distributional critic | <3 hrs on one A100 | beats PPO/SAC/SimbaV2/TDMPC2/DreamerV3, real Booster T1 | shown task-by-task, not across the full HumanoidBench locomotion suite |
| [[2604.04539\|FlashSAC]] | off-policy SAC + parallel sim + 10M replay | ~1 order-of-magnitude vs PPO | 60+ locomotion + manipulation tasks, sim-to-real humanoid | the off-policy peer corroborating FastTD3, not a flow comparison |
| [[2512.01996\|Humanoid Loco 15min]] | massively-parallel off-policy | 15 min on RTX 4090 | sim-to-real G1+T1, push-robust + 2-min dance | state-based; vision-based wall-clock not characterized |
| [[2602.02481\|FPO++]] | flow-policy gradients | first flow sim-to-real | stable gaits, first flow-policy RL humanoid locomotion | no head-to-head flow-vs-Gaussian gait-quality study |
| [[2408.00342\|MuJoCo MPC HumanoidBench]] | sampling-based MPC (model-based, no learning) | — | beats DreamerV3/TD-MPC2/SAC/PPO on Stand/Walk/Push, 8 s episodes | the MPC counterpoint — no learned policy to deploy/finetune |
| [[2601.21363\|Pretrain-Finetune Bridge RL]] | SAC pretrain + physics WM, safe finetune | 80–590 s real data | zero-shot Booster T1, safe finetune from minimal real data | the pretrain+safe-finetune route, not a from-scratch wall-clock claim |
| [[2508.12252\|Robot Trains Robot]] | teacher-arm + dynamics-latent real-world RL | 15–20 min real | doubles walking speed in 20 min, swing-up from scratch in 15 min | real-world fast-adaptation, not the sim wall-clock comparison |
| [[2502.08844\|MuJoCo Playground]] | GPU-parallel sim substrate | minutes/hours | zero-shot to Go1 + Berkeley Humanoid | the parallel-sim substrate off-policy exploits, not a learner |
| [[2603.20147\|AGILE]] | scalable RL infra + L2C2, 6–25 hrs/task | 6–25 hrs/task | unified deployment workflow, motion-quality diagnostics | the workflow baseline off-policy methods undercut on wall-clock |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (off-policy/flow beats PPO on wall-clock for dense-reward parallel-sim locomotion).
1. **H1 — The off-policy advantage scales with reward density and environment count.**
   - *Prediction*: reproducing [[2505.22642|FastTD3]]'s win across HumanoidBench locomotion tasks, the off-policy-over-PPO wall-clock margin grows with environment count and shrinks as the reward is artificially sparsified — confirming the dense-reward/parallel-sim mechanism.
   - *Test*: sweep environment count and reward density; report off-policy-minus-PPO time-to-solve.
   - *Row*: FastTD3 (off-policy) vs AGILE (PPO workflow).
   - *Falsifier*: the margin is flat across density/count → the advantage isn't from sample-reuse under dense parallel transitions.
2. **H2 — Large batch + distributional critic is the load-bearing component.**
   - *Prediction*: ablating [[2505.22642|FastTD3]]'s batch 32,768 and distributional critic, one of the two carries most of the stability/speed and dropping it degrades high-DoF off-policy control toward instability.
   - *Test*: factorial ablation (batch size × distributional vs scalar critic); report convergence and final SR.
   - *Row*: FastTD3 (off-policy).
   - *Falsifier*: neither ablation matters → the speed comes from elsewhere (e.g. raw parallelism alone).
3. **H3 — Flow policies help where contact is multimodal.**
   - *Prediction*: [[2602.02481|FPO++]]'s flow policy beats a Gaussian policy on gait quality and sim-to-real robustness specifically on multimodal-contact skills (agile transitions, motion tracking) and ties on smooth walking, where a unimodal Gaussian suffices.
   - *Test*: compare flow vs Gaussian on walking vs agile-contact tasks; report gait quality and sim-to-real SR.
   - *Row*: FPO++ (flow).
   - *Falsifier*: flow ties Gaussian on multimodal-contact tasks → the richer distribution adds nothing.
4. **H4 — Sub-hour training enables reward/curriculum iteration PPO cannot.**
   - *Prediction*: [[2512.01996|Humanoid Loco 15min]]'s 15-minute loop enables a rapid reward/curriculum search that converges to a better final gait than a single PPO run of equal *total* wall-clock, because many fast iterations beat one slow one.
   - *Test*: fix total wall-clock; compare N fast off-policy iterations vs one PPO run; report final gait quality.
   - *Row*: Humanoid Loco 15min (15-min off-policy) vs AGILE (6–25 hrs PPO).
   - *Falsifier*: the single PPO run matches the iterated search → fast training doesn't buy better iteration.
5. **H5 — Off-policy degrades on sparse-reward locomotion sub-tasks.**
   - *Prediction*: the off-policy wall-clock win *narrows or reverses* on sparse-reward locomotion sub-tasks (fall-recovery-like, A3), bounding the bet to the dense-reward regime where the mechanism holds.
   - *Test*: run off-policy vs PPO on dense vs sparse locomotion tasks; report where the advantage holds.
   - *Row*: FastTD3 (off-policy) vs MuJoCo MPC HumanoidBench (model-based, sparse-robust).
   - *Falsifier*: off-policy also dominates sparse tasks → the dense-reward boundary on the bet is unnecessary.

> [!warning] Risks
> - **Off-policy instability on sparse-reward skills** — the dense-reward advantage may not hold for sparse fall-recovery (A3). → Bound the bet to dense-reward locomotion (H5); report where off-policy degrades vs PPO on sparse tasks.
> - **Fast-trained policies may be brittle** — 15-min policies may overfit sim. → [[2512.01996|Humanoid Loco 15min]] and [[2505.22642|FastTD3]] both deploy real; report the sim-to-real SR gap, not just sim wall-clock.
> - **Consumer-GPU results may not scale to perception** — vision-based policies (A1) cost more. → Report wall-clock separately for state-based vs vision-based; the 15-min number is state-based.

---

## Cluster B — Quadruped Locomotion & Real-World Adaptation

*Recovering or bounding the unobserved physical state — terrain friction, ground height, payload, model error — that separates a sim-trained quadruped policy from a deployable one. Proprioceptive robustness, world-model dreaming for few-shot adaptation, and perceptive mapless mobility-to-goal.*

### B1 — Proprioceptive-Only Robustness under Disturbance & Payload

| | |
|---|---|
| **Cluster** | B — Quadruped Locomotion & Real-World Adaptation |
| **Thesis** | Infer the unobserved environment context from proprioceptive *history* alone, without exteroception or online real-world fine-tuning. The reason it must work: the privileged state (friction, payload, terrain) leaves a recoverable signature in the recent proprioceptive trajectory, so a supervised module can read it back out without ever sensing it directly. The field assumes robust deployment needs either vision or real-world adaptation trials. The bet is in First-principles below. |
| **Anchor papers** | [[2107.04034\|RMA]] (method), [[2212.07740\|TERT]] (method), [[2403.13358\|QUARD-Auto]] (method), [[2403.10506\|HumanoidBench]] (benchmark) |
| **Key targets** | [[2107.04034\|RMA]] 12 kg payload (80% body weight) on sand/mud/rocky/slippery, 100 Hz base / 10 Hz adaptation, zero real-world fine-tuning; [[2212.07740\|TERT]] 100% sand / 60% stairs vs RMA 0% across 9 terrains; [[2403.13358\|QUARD-Auto]] 71–90.5% across 99 quadruped sub-tasks at 39.31M active params |

**Why it matters.**
- **The gap**: a quadruped's deployable policy must act on proprioception alone — joint angles, IMU, contact — because the privileged context sim provides (friction $\mu$, payload $m$, ground compliance) is unavailable on hardware, and the field's two escape routes (a camera, or on-robot fine-tuning) both add cost.
- **Today's answers**: [[2107.04034|RMA]] shows neither escape is needed — a base policy trained with a privileged extrinsics vector, paired with an adaptation module that *infers that vector from recent proprioceptive history* at 10 Hz, crosses sand/mud/rocky/slippery terrain carrying 12 kg (80% body weight) with zero fine-tuning; [[2212.07740|TERT]] sharpens it — a Terrain Transformer hits 100% sand / 60% stairs *where RMA's TCN gets 0%*. Both infer context, but the architecture gap shows the inference is far from solved.
- **The opening**: [[2212.07740|TERT]]'s 60%-vs-0% stair result with the *same* privileged supervision but a Transformer backbone proves the bottleneck is the *inference architecture*, not the availability of the signal — the proprioceptive signature is there; recovering it on discontinuous terrain is the open problem.

**First-principles framing.**
- **First principle**: The privileged context — friction, payload, terrain — cannot be read directly off the hardware, but it shapes how the robot's joints and IMU respond, so it leaves a recoverable fingerprint in the recent proprioceptive history. A supervised module can regress that history into a context estimate, making the privileged state inferable without ever sensing it directly. [[2107.04034|RMA]] demonstrates it: an adaptation module reading proprioceptive history at 10 Hz sustains a 12 kg payload across four terrains, zero fine-tuning.
- **Assumption being challenged**: That robust deployment requires exteroception or online real-world fine-tuning. The field reaches for cameras ([[2107.03996|LocoTransformer]]-style) or on-robot adaptation; [[2107.04034|RMA]]'s 12 kg-payload, zero-fine-tuning result on four terrain types shows proprioceptive inference *alone* covers a wide context range, and [[2212.07740|TERT]]'s Transformer extends it to discontinuous terrain — the vision/fine-tuning requirement comes from *not exploiting* the proprioceptive signature, not from its absence.
- **The bet**: A proprioceptive context-inference module sustains locomotion under [[2107.04034|RMA]]'s 12 kg payload (80% body weight) and lifts stair traversal to [[2212.07740|TERT]]'s 60% where TCN-style RMA scores 0%, at 100 Hz control / 10 Hz adaptation with zero real-world fine-tuning — robustness from inference architecture, not added sensors or real trials. Falsifiable: if an exteroceptive policy beats proprioceptive inference across the full friction × payload range (not just on geometry), proprioception alone is insufficient.

**Related research papers.** One comparison table — the axis is *how the unobserved context is recovered* (regress-from-history / Transformer-context / in-context / exteroceptive / meta-learned / MoE-capacity), with what each leaves missing:

| System | Context-recovery mechanism | Sensing | Key result | What's missing |
|---|---|---|---|---|
| [[2107.04034\|RMA]] | adaptation module regresses extrinsics from proprio history (10 Hz) | proprioceptive | 12 kg payload, 4 terrains, zero fine-tuning | TCN backbone fails on discontinuous terrain (stairs) |
| [[2212.07740\|TERT]] | Terrain Transformer predicts teacher actions from proprio history | proprioceptive | 100% sand / 60% stairs vs RMA 0%, 9 terrains | no payload-range study; terrain-focused |
| [[2509.23745\|LocoFormer]] | Transformer-XL long-context in-context adaptation | proprioceptive | 0.96 displacement on 10 morphologies; zero-shot to locked limbs / wheel failure / payload | in-context, but no explicit privileged-context inference target |
| [[2403.13358\|QUARD-Auto]] | MoE generalist over 99 sub-tasks | proprioceptive | 71–90.5%, 39.31M active params, emergent path planning | scales *skill* breadth; whether MoE helps *context* breadth is open |
| [[2107.03996\|LocoTransformer]] | depth + proprioception fusion | exteroceptive | 92% farther real, 290.5–663% fewer collisions sim | the vision-augmented counterpoint B1 argues is unnecessary for dynamics context |
| [[2003.01239\|Evolutionary Meta-Learning Legged]] | ES-MAML fast real-world meta-adaptation | proprioceptive | Minitaur +100% velocity in 50 rollouts / 150 s | needs real-world rollouts — the fine-tuning route B1 avoids |
| [[2605.27046\|Thermal-Aware Residual]] | payload + thermal context (residual) | proprioceptive | 650 m + 3 kg, overheating 70%→<10% | regulates *cost* under payload, not context *inference* (cross-list A4) |
| [[2403.10506\|HumanoidBench]] | benchmark (high-DoF context-inference difficulty) | — | flat RL fails; the difficulty framing | a difficulty suite, not a context-inference method |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (proprioceptive context-inference covers the dynamics range without vision or real trials).
1. **H1 — Proprioception suffices for dynamics context; vision is needed only for geometry.**
   - *Prediction*: comparing [[2107.04034|RMA]]'s adaptation against an exteroceptive policy ([[2107.03996|LocoTransformer]]-style) across friction/payload ranges, proprioception matches vision on *dynamics* context (friction, payload) and only loses on *anticipatory geometry* (gaps, steps) — drawing a clean boundary.
   - *Test*: stratify tasks into dynamics-context vs geometry-anticipation; report proprio-vs-vision SR per stratum.
   - *Row*: RMA (proprioceptive) vs LocoTransformer (exteroceptive).
   - *Falsifier*: vision beats proprioception even on pure dynamics context → proprioceptive inference is insufficient.
2. **H2 — The inference backbone, not the signal, sets discontinuous-terrain context.**
   - *Prediction*: [[2212.07740|TERT]]'s Transformer beats [[2107.04034|RMA]]'s TCN on stairs (60% vs 0%) under *identical* privileged supervision, so backbone capacity — not added sensing — recovers discontinuous-terrain context.
   - *Test*: hold privileged supervision fixed; swap TCN ↔ Transformer ↔ Transformer-XL; report stair/gap SR.
   - *Row*: TERT (Transformer) vs RMA (TCN).
   - *Falsifier*: backbone choice doesn't change stair SR under fixed supervision → the signal, not the architecture, is the limit.
3. **H3 — Adaptation rate must track disturbance bandwidth.**
   - *Prediction*: sweeping [[2107.04034|RMA]]'s 10 Hz adaptation rate against disturbance bandwidth, there is a minimum rate below which fast payload/terrain shifts are not tracked, and above which gains saturate — a bandwidth-matched optimum.
   - *Test*: vary adaptation frequency; inject payload/terrain steps at varying bandwidth; report tracking error.
   - *Row*: RMA (10 Hz adaptation).
   - *Falsifier*: SR is flat across adaptation rate → the inference rate is not bandwidth-limited.
4. **H4 — MoE capacity helps skill breadth but not context breadth.**
   - *Prediction*: [[2403.13358|QUARD-Auto]]'s MoE capacity, which raises *skill* breadth across 99 sub-tasks, does *not* proportionally raise *context-inference* breadth (many terrains/payloads), because context inference is a separate bottleneck from skill capacity.
   - *Test*: scale MoE active params; report skill-breadth vs context-breadth gains separately.
   - *Row*: QUARD-Auto (MoE capacity).
   - *Falsifier*: MoE capacity lifts context breadth as much as skill breadth → they share one bottleneck.
5. **H5 — In-context adaptation matches supervised inference without a privileged target.**
   - *Prediction*: [[2509.23745|LocoFormer]]'s long-context in-context adaptation matches [[2107.04034|RMA]]'s supervised extrinsics inference on payload/terrain robustness *without* a privileged-context training target, trading supervision for context length.
   - *Test*: compare in-context (no privileged target) vs supervised-inference on matched friction/payload tasks.
   - *Row*: LocoFormer (in-context) vs RMA (supervised inference).
   - *Falsifier*: in-context underperforms supervised inference → the privileged target is necessary, length doesn't substitute.

> [!warning] Risks
> - **Proprioception cannot anticipate geometry** — a step or gap is invisible until contact. → Bound B1 to dynamics-context inference (friction/payload); anticipatory geometry is A1's job — the two are complementary, not competing (H1 draws the boundary).
> - **Adaptation supervision needs privileged sim** — the inference target requires simulation extrinsics. → Standard for the RMA family; cross-ref [[Sim2Real|Sim2Real]] for the privileged-to-proprioceptive distillation machinery.
> - **TCN-vs-Transformer gap may be task-specific** — TERT's stair win may not generalize. → H2's backbone ablation tests generality; report per-terrain, not a single average.

### B2 — World-Model Dreaming for Few-Shot Real-World Adaptation

| | |
|---|---|
| **Cluster** | B — Quadruped Locomotion & Real-World Adaptation |
| **Thesis** | Pretrain a world model in sim and adapt it with a *handful* of real trajectories, instead of the field's million-step on-robot RL or pure domain randomization. The reason it must work: a learned dynamics model lets the policy *imagine* action consequences, so each real interaction updates a model that generates thousands of synthetic ones. The field assumes closing the sim-to-real dynamics gap needs exhaustive randomization or extensive real rollouts. The bet is in First-principles below. |
| **Anchor papers** | [[2206.14176\|DayDreamer]] (method), [[2504.16680\|RWM-U]] (method), [[2604.02911\|DreamTIP]] (method), [[2603.15759\|SimDist]] (method), [[2403.10506\|HumanoidBench]] (benchmark) |
| **Key targets** | [[2604.02911\|DreamTIP]] 28.1% avg transfer gain + Go2 100% on 52 cm Climb (vs WMP 10%) and 16 cm Stair (WMP ties 100%), stable adaptation from ~5 real trajectories; [[2206.14176\|DayDreamer]] A1 walks in 1 hr real + recovers from pushes in 10 min; [[2603.15759\|SimDist]] 1.5–2× throughput + 15–30 min real adaptation; [[2504.16680\|RWM-U]] 0.91 normalized reward on ANYmal D (offline sim+real), beats online model-free |

**Why it matters.**
- **The gap**: deep RL needs millions of interactions — impractical on hardware — and the field's two answers (exhaustive domain randomization, extensive on-robot RL) are both inefficient ways to close the sim-to-real dynamics gap.
- **Today's answers**: world-model dreaming is a third route — [[2206.14176|DayDreamer]] proved it (an A1 learns to walk in 1 hour and recovers from pushes in 10 minutes via a Dreamer latent world model, no simulator); [[2604.02911|DreamTIP]] modernizes it for transfer (a task-invariant latent hits 28.1% avg transfer gain and 100% on a 52 cm climb on a real Go2 vs a WMP baseline's 10%, from ~5 trajectories). Both dream, but neither bounds *where* the imagination is unreliable.
- **The opening**: [[2504.16680|RWM-U]] supplies the safety valve and the existence proof together — an epistemic-uncertainty penalty steers away from where the model is blind, hitting 0.91 on ANYmal D and *beating online model-free baselines* from offline sim+real data, showing a bounded dreamed model needs neither randomization nor on-robot RL.

**First-principles framing.**
- **First principle**: A learned dynamics model is a *multiplier* on real data — each real transition updates the model and, through imagination, generates many synthetic transitions for policy optimization. Sample efficiency is governed by model accuracy per real interaction, not raw interaction count; a good model makes 5 trajectories worth thousands. [[2604.02911|DreamTIP]] demonstrates the multiplier: ~5 real trajectories yield 100% on a 52 cm climb where a non-dreaming baseline gets 10%.
- **Assumption being challenged**: That closing the sim-to-real dynamics gap requires exhaustive randomization or extensive real rollouts. Domain randomization (the [[2107.04034|RMA]]/[[2408.14472|DWL]] line) and on-robot RL are the defaults; [[2604.02911|DreamTIP]]'s 5-trajectory 100%-vs-10% and [[2206.14176|DayDreamer]]'s 1-hour walking bet the opposite — the gap is a *model-adaptation* problem, not a data-volume one — and [[2504.16680|RWM-U]] shows offline dreaming can even beat *online* model-free RL.
- **The bet**: A sim-pretrained world model adapts to real quadruped locomotion in [[2604.02911|DreamTIP]]'s ~5 trajectories (100% on a 52 cm climb vs 10% baseline) and [[2603.15759|SimDist]]'s 15–30 minutes, with an epistemic-uncertainty penalty ([[2504.16680|RWM-U]], 0.91 on ANYmal D) bounding model-blind exploitation — dreaming-driven few-shot adaptation, not randomization or extensive real RL. Falsifiable: if a domain-randomized blind policy matches the dreamed model at a ~5-trajectory budget, the world model adds no multiplier.

**Related research papers.** One comparison table — the axis is *the world-model role* (real-from-scratch / transfer-latent / sim-pretrain / uncertainty-bound / cross-embodiment / context-aligned / online-continual / foundation), with what each leaves missing:

| System | World-model role | Real-data budget | Key result | What's missing |
|---|---|---|---|---|
| [[2604.02911\|DreamTIP]] | task-invariant transfer latent | ~5 trajectories | 28.1% avg gain, Go2 100% on 52 cm climb vs WMP 10% | no explicit uncertainty bound on the imagination |
| [[2206.14176\|DayDreamer]] | real-world Dreamer from scratch (no sim) | 1 hr walking / 10 min push | A1 walks in 1 hr, recovers from pushes in 10 min | from-scratch, no sim pretraining to amortize |
| [[2603.15759\|SimDist]] | sim-pretrained world model + rapid real adapt | 15–30 min | 1.5–2× throughput, quadruped + manipulation | freezes core components; no epistemic bound |
| [[2504.16680\|RWM-U]] | uncertainty-aware MBRL (MOPO-PPO penalty) | offline sim+real | 0.91 ANYmal D, beats online model-free | offline, not few-shot-*online* adaptation |
| [[2501.10100\|RWM]] | neural-simulator world model, cross-embodiment | offline | zero-shot velocity tracking, ANYmal D + G1, beats DreamerV3/SHAC | the cross-embodiment substrate, no real-adaptation few-shot study |
| [[2508.20294\|DALI]] | dynamics-aligned latent context from short histories | short histories | +96.4% over context-unaware Dreamer | context-aligned, but evaluated in sim control suites not real legged |
| [[2603.04029\|Self-Adapting RL]] | online continual world-model feedback | 4–8 min real | ANYmal actuator-failure recovery 4 min, real F1Tenth 8 min | fault-recovery face, not terrain/payload few-shot transfer |
| [[1912.01603\|Dreamer]] | latent-imagination MBRL foundation | — | 20× data-efficiency, ~3 hrs/million steps | the progenitor — not a real-robot adaptation method itself |
| [[2003.01239\|Evolutionary Meta-Learning Legged]] | model-free meta-adaptation (no world model) | 50 rollouts / 150 s | Minitaur +100% velocity | the model-free fast-adaptation counterpoint dreaming must beat |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a dreamed model is a data multiplier that beats randomization at a few-trajectory budget).
1. **H1 — Dreaming overtakes domain randomization at a measurable data budget.**
   - *Prediction*: comparing [[2604.02911|DreamTIP]]'s ~5-trajectory adaptation against a domain-randomized blind policy ([[2408.14472|DWL]]-style), dreaming overtakes randomization above a small real-data budget, and the 100%-vs-10% gap *widens* with task difficulty (52 cm climb harder than 16 cm stair).
   - *Test*: sweep real-trajectory budget; report dreamed-vs-randomized SR per difficulty level.
   - *Row*: DreamTIP (transfer latent) vs (DWL-style randomization, B1 cross-ref).
   - *Falsifier*: randomization matches dreaming at the ~5-trajectory budget → the world model adds no multiplier.
2. **H2 — The epistemic penalty coefficient tracks long-horizon prediction error.**
   - *Prediction*: [[2504.16680|RWM-U]]'s epistemic penalty $\beta$ has a calibration where the discount matches measured long-horizon prediction error — too small exploits model-blind regions, too large over-conserves — an interior optimum.
   - *Test*: sweep $\beta$; correlate the penalty against held-out long-horizon model error; report the trade-off curve.
   - *Row*: RWM-U (uncertainty-bound).
   - *Falsifier*: SR is flat across $\beta$ → the penalty isn't bounding model-blind exploitation.
3. **H3 — The task-invariant latent transfers across terrains, not just tasks.**
   - *Prediction*: [[2604.02911|DreamTIP]]'s task-invariant latent transfers across *terrains* (not only tasks) and *composes* with B1's proprioceptive context-inference, so the invariant captures dynamics shared across surfaces.
   - *Test*: adapt on terrain A, evaluate held-out terrain B; test with vs without B1-style context inference.
   - *Row*: DreamTIP (transfer latent) + RMA (B1 context inference).
   - *Falsifier*: the latent fails to transfer across terrains → it's task-invariant but terrain-specific.
4. **H4 — The dynamics model is morphology-portable across legged embodiments.**
   - *Prediction*: a quadruped-pretrained world model ([[2501.10100|RWM]]/[[2504.16680|RWM-U]] run the same pipeline on ANYmal D + G1) transfers a measurable fraction of its dynamics to a humanoid, more than a manipulation grasp model would, confirming the gait object's portability.
   - *Test*: pretrain on quadruped, measure zero-shot/few-shot humanoid transfer vs from-scratch.
   - *Row*: RWM (cross-embodiment) / DALI (context-aligned).
   - *Falsifier*: quadruped→humanoid transfer is near-zero → the dynamics model is morphology-specific.
5. **H5 — Few-shot dreaming overfits the test terrain without held-out validation.**
   - *Prediction*: [[2604.02911|DreamTIP]]'s 5-trajectory adaptation risks overfitting the adapted terrain — held-out-terrain SR drops measurably below adapted-terrain SR — bounding the few-shot claim and motivating the epistemic penalty.
   - *Test*: report adapted-terrain vs held-out-terrain SR after 5-trajectory adaptation, with and without [[2504.16680|RWM-U]]'s penalty.
   - *Row*: DreamTIP (transfer latent) + RWM-U (uncertainty-bound).
   - *Falsifier*: held-out SR matches adapted SR → 5 trajectories generalize without overfitting.

> [!warning] Risks
> - **Model error compounds over horizon** — long imagined rollouts drift. → [[2504.16680|RWM-U]]'s epistemic penalty bounds this; report prediction error vs horizon and cap rollout length where uncertainty spikes (H2).
> - **5-trajectory adaptation may overfit the test terrain** — tiny real data risks narrow adaptation. → H5 tests cross-terrain transfer; report held-out-terrain SR, not just the adapted terrain.
> - **Dreaming needs a good simulator for pretraining** — garbage-in poisons the model. → [[2603.15759|SimDist]] stresses diverse large-scale pretraining; cross-ref [[WAM|WAM]] for substrate quality and [[Sim2Real|Sim2Real]] for the sim side.

### B3 — Perceptive Mapless Locomotion-to-Goal & Traversability

| | |
|---|---|
| **Cluster** | B — Quadruped Locomotion & Real-World Adaptation |
| **Thesis** | Reach a spatial goal by *learned* mapless memory + self-supervised traversability, not a pre-built metric map or a high-level VLN planner. The reason it must work: long-range locomotion-to-goal needs a recurrent spatial state that survives hundreds of control steps and a tight coupling to the gait — something an explicit SLAM map handles brittly on unstructured terrain. The field assumes goal-reaching factors cleanly into map-build → plan → track. The bet is in First-principles below. |
| **Anchor papers** | [[2506.05997\|SRU]] (method), [[2604.26504\|HiPAN]] (method), [[2605.28442\|COTRATE]] (method) |
| **Key targets** | [[2506.05997\|SRU]] 23.5% higher long-range mapless SR vs LSTM/GRU + 29.6% over EMHP / 105.0% over GTRL, zero-shot 100+ m on a real Unitree B2W legged-wheel robot; [[2604.26504\|HiPAN]] 94.7% SR / 83.6 SPL in Complex-2, Go1 onboard depth in cluttered/dead-end/outdoor; [[2605.28442\|COTRATE]] cross-platform traversability (Spot + Husky), ≥2.5 pp mIoU (Spot) / ≥2.1 pp (Husky) over baselines |

**Why it matters.**
- **The gap**: long-range goal-reaching is the locomotion-to-goal problem — distinct from VLN goal *reasoning* and from manipulation — and the classical map-build → plan → track pipeline is brittle on unstructured terrain (drift, dynamic obstacles, no GPS) because the explicit metric map is the weakest link.
- **Today's answers**: [[2506.05997|SRU]] takes the memory axis — a Spatially-enhanced Recurrent Unit gives an end-to-end RL policy a spatial state that survives hundreds of steps, lifting mapless SR 23.5% over LSTM/GRU and transferring zero-shot 100+ m on a real B2W legged-wheel robot; [[2604.26504|HiPAN]] takes the traversal axis — hierarchical posture-adaptive navigation reaches 94.7% SR / 83.6 SPL in the hardest Complex-2, on a Go1 from onboard depth. Both replace the map, but neither shares perception across platforms.
- **The opening**: [[2605.28442|COTRATE]] supplies the missing substrate — self-supervised online traversability that transfers *across platforms* (Spot, Husky), with zero-shot models sometimes beating platform-specific continually-learned ones — so the perception-gait coupling can be amortized across embodiments rather than rebuilt per robot.

**First-principles framing.**
- **First principle**: Long-range locomotion-to-goal needs a spatial state that persists across hundreds of control steps (where have I been, where is the goal relative to me) *and* a coupling between that state and the gait. An explicit metric map is one lossy realization — brittle under drift and dynamics — and the map-build → plan → track factoring severs the perception-gait coupling the policy could exploit. [[2506.05997|SRU]] demonstrates the alternative: a learned recurrent spatial state lifts mapless SR 23.5% over LSTM/GRU and transfers zero-shot 100+ m.
- **Assumption being challenged**: That goal-reaching factors cleanly into map-build → plan → track. Classical navigation and even modular learned stacks assume this; [[2506.05997|SRU]]'s 23.5% mapless gain over recurrent baselines and zero-shot 100+ m transfer, plus [[2604.26504|HiPAN]]'s 94.7% SR in dead-end environments, bet the opposite — an end-to-end policy with *learned* spatial memory beats the factored pipeline on unstructured terrain, where the map breaks first.
- **The bet**: An end-to-end mapless policy with spatial memory lifts long-range success by [[2506.05997|SRU]]'s 23.5% over LSTM/GRU and transfers zero-shot 100+ m to a real legged-wheel robot, with self-supervised traversability ([[2605.28442|COTRATE]]) cutting path effort cross-platform and [[2604.26504|HiPAN]]-class 94.7% SR in cluttered/dead-end environments — learned memory, not a built map. Falsifiable: if a SLAM-map + planner matches the mapless policy on long-range unstructured courses, the learned memory buys nothing the map doesn't.

**Related research papers.** One comparison table — the axis is *how the spatial state and goal-reaching are represented* (recurrent-memory / hierarchical-posture / traversability-substrate / vision-to-goal / cross-embodiment / emergent-planning / dynamic-scene), with what each leaves missing:

| System | Goal-reaching representation | Map / memory | Key result | What's missing |
|---|---|---|---|---|
| [[2506.05997\|SRU]] | spatially-enhanced recurrent unit, end-to-end RL | learned mapless memory | 23.5% over LSTM/GRU, 29.6% over EMHP, 105.0% over GTRL, 100+ m real B2W | single platform per run; no cross-platform traversability |
| [[2604.26504\|HiPAN]] | hierarchical posture-adaptive locomotion + path-guided curriculum | implicit (no metric map) | 94.7% SR / 83.6 SPL Complex-2, Go1 depth, cluttered/dead-end/outdoor | posture-adaptive but quadruped-specific, no cross-platform transfer |
| [[2605.28442\|COTRATE]] | self-supervised online traversability prediction | perception substrate | cross-platform (Spot + Husky), ≥2.5 pp mIoU (Spot), path-effort cut | a perception layer, not a full goal-reaching policy |
| [[2107.03996\|LocoTransformer]] | vision-guided end-to-end locomotion to goal | reactive (attention) | 92% farther real, attends to obstacles + distant goal | no persistent spatial memory over hundreds of steps |
| [[2509.23203\|CE-Nav]] | flow geometric expert + RL dynamics-refiner | mapless, cross-embodiment | mSR 0.745–0.860 on 5 embodiments, 8× faster, real Go2 | local navigation focus, no long-range spatial-memory study |
| [[2403.13358\|QUARD-Auto]] | MoE generalist with emergent path planning | emergent | 71–90.5%, emergent adaptive path planning unseen scenes | path planning is emergent, not a designed spatial-memory mechanism |
| [[2605.21935\|MIF]] | multi-modal interactive fields for humanoid nav | scene field | 94% interaction-pose safety, 0% collision, dynamic scenes | scene-field for *interaction*, not long-range mapless goal-reaching |
| [[2604.24916\|asRoBallet]] | precise base velocity tracking + station-keeping | reactive | 0.05 m/s MAE, 3–5 cm station-keeping | low-level mobility-control precedent, no goal-reaching layer |
| [[2604.02911\|DreamTIP]] | world model the mapless policy can plan through | learned dynamics | 100% vs 10% (52 cm climb), 5 trajectories | the dreaming substrate (feeds B2), not a spatial-memory navigator |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (learned mapless memory + cross-platform traversability beats the map → plan → track stack).
1. **H1 — The mapless-memory gain widens as terrain becomes less map-friendly.**
   - *Prediction*: comparing [[2506.05997|SRU]]'s mapless memory against a SLAM-map + planner on long-range courses, the 23.5% gain *widens* as terrain becomes less map-friendly (drift, dynamic obstacles, featureless), because the map degrades where the learned memory doesn't.
   - *Test*: grade courses by map-friendliness (feature density, dynamics); report mapless-minus-mapped SR per grade.
   - *Row*: SRU (mapless memory) vs (SLAM-map + planner baseline).
   - *Falsifier*: the gain is constant or shrinks on hard terrain → the map isn't the weakest link.
2. **H2 — Recurrent structure governs spatial retention over horizon.**
   - *Prediction*: [[2506.05997|SRU]]'s spatial-memory structure beats LSTM/GRU more as goal distance grows, because the spatially-enhanced state retains relative-goal information over hundreds of steps where vanilla recurrence forgets.
   - *Test*: ablate memory structure against goal distance; report SR vs distance per memory type.
   - *Row*: SRU (recurrent memory).
   - *Falsifier*: SRU ties LSTM/GRU at long distances → the spatial enhancement isn't the retention lever.
3. **H3 — Posture-conditioned locomotion extends the traversable space.**
   - *Prediction*: [[2604.26504|HiPAN]]'s posture adaptation (crouch, squeeze) extends the traversable space beyond fixed-posture navigation in confined geometry, measurably raising SPL in dead-end/cluttered scenes where a fixed posture gets stuck.
   - *Test*: compare posture-adaptive vs fixed-posture navigation in confined courses; report SPL delta.
   - *Row*: HiPAN (hierarchical posture).
   - *Falsifier*: posture adaptation doesn't raise SPL in confined geometry → fixed posture suffices.
4. **H4 — Robot-agnostic traversability improves cross-embodiment goal-reaching.**
   - *Prediction*: plugging [[2605.28442|COTRATE]]'s cross-platform traversability into the mapless policy improves cross-embodiment goal-reaching over platform-specific perception, with zero-shot transfer (Spot→Husky) sometimes beating per-platform continual learning.
   - *Test*: swap platform-specific perception for COTRATE; report cross-embodiment SR and path effort.
   - *Row*: COTRATE (traversability substrate) + SRU (mapless memory).
   - *Falsifier*: robot-agnostic traversability underperforms platform-specific perception → perception must be per-robot.
5. **H5 — SPL exposes mapless looping the SR number hides.**
   - *Prediction*: mapless policies without a map risk revisiting dead-ends, so [[2604.26504|HiPAN]]'s SPL drops below SR more on loop-prone courses, exposing inefficiency the SR number alone hides — and path-guided curriculum narrows the SPL–SR gap.
   - *Test*: report SPL alongside SR on loop-prone vs open courses, with and without path-guided curriculum.
   - *Row*: HiPAN (hierarchical posture) / SRU (mapless memory).
   - *Falsifier*: SPL tracks SR on loop-prone courses → mapless policies don't loop and the SPL caveat is moot.

> [!warning] Risks
> - **Mapless policies can loop or get stuck** — without a map, the policy may revisit dead-ends. → [[2604.26504|HiPAN]]'s SPL catches this; report SPL alongside SR, not SR alone (H5).
> - **Overlap with the umbrella's VLN direction** — high-level goal *reasoning* is VLN territory. → This direction is scoped to low-level mapless *control + traversability*; language-instruction goal-reasoning is cross-referenced to [[Embodied-AI|Embodied-AI]], not duplicated.
> - **Traversability self-supervision needs experience** — [[2605.28442|COTRATE]] learns from robot rollouts. → It transfers cross-platform (Spot→Husky) zero-shot in places; report where transfer holds vs needs continual learning (H4).

---

## Cross-Cutting Themes

> [!tip] The Privileged-State Gap Is the Bottleneck — Inference, Perception, and Dreaming Are the Three Answers
> A1, B1, and B2 face the same problem the surveys name under different words: the policy must act without the privileged physical state (terrain $\mu/h$, payload, contact, model error) that simulation provides. They answer at three points of the recovery operator: B1 *infers* the context from proprioceptive history ([[2107.04034|RMA]]'s 10 Hz adaptation module, 12 kg payload), A1 *perceives* the anticipatory geometry exteroception exposes ([[2604.17335|G1 WBC-Gen+Track]] 0.962 vs 0.230 box-climb), and B2 *dreams* — a world model imagines consequences so 5 real trajectories suffice ([[2604.02911|DreamTIP]] 100% vs 10%). [[2408.14472|DWL]]'s denoising world model and [[2504.16680|RWM-U]]'s epistemic penalty share the move: recover or bound the unobserved state, don't pretend it's observed.

> [!tip] Real-World Adaptation in Minutes, Not Millions — Sample Efficiency Through the Right Substrate
> A5 and B2 converge on the same lever for deployable locomotion: sample efficiency through the right substrate, not more compute or more real data. A5 shows off-policy/flow RL beats PPO on wall-clock ([[2505.22642|FastTD3]] <3 hrs, [[2512.01996|Humanoid Loco 15min]] 15 min); B2 shows world-model pretraining + tiny real adaptation ([[2206.14176|DayDreamer]] 1 hr, [[2603.15759|SimDist]] 15–30 min) displaces both exhaustive domain randomization and extensive on-robot RL. The shared move is biological: the brain learns from few interactions because it has a model — favor the mechanism (off-policy reuse, world-model imagination) that extracts more from each step over the one that discards rollouts or randomizes blindly.

> [!tip] The Imitation Target, Not the Imitation Data, Is the Lever for Dynamic Skills
> A1 and A2 share one discipline — make the reference feasible, don't collect more demonstrations — but apply it at opposite ends of the timeline, and that split is why they stay separate. **A2 fixes a clip offline**: a one-time projection of pre-recorded mocap onto the feasible manifold *before* any rollout ([[2506.12851|KungfuBot]] 53.25 mm vs >233 mm, [[2605.06593|ReActor]] 97.45% downstream RL). **A1 generates a fresh reference online** against the terrain seen at runtime — a new reference each control window, filtered by an RL tracker ([[2604.17335|G1 WBC-Gen+Track]] 0.962 box-climb). A2 asks "is *this clip* trackable?"; A1 asks "what does *this terrain ahead* demand?" [[2605.10063|EFGCL]]'s force-guided curriculum even *expands* A2's feasible manifold to reach backflips. Same lever, different *when* — complementary directions, not two phrasings of one idea.

> [!tip] Deployability Is Bounded by Embodiment Costs the Task Reward Ignores
> A3, A4, and B1 all hit real limits the standard task reward omits. A4 makes GRF, acoustic, and thermal cost first-class predicted-and-regulated quantities ([[2604.23702|QuietWalk]] R²≈0.99, 7.17 dBA; [[2605.27046|Thermal-Aware Residual]] 70%→<10% overheating); A3 treats fall-recovery as the non-periodic embodiment-stress boundary case ([[2502.12152|HUMANUP]] lower motor temperature, ~6 s recovery); B1 sustains locomotion under real payload ([[2107.04034|RMA]] 12 kg). The insight: task success is necessary but not sufficient — a gait that overheats, deafens, or cannot recover from a fall is undeployable regardless of its tracking reward.

> [!tip] The Locomotion Control Object Is More Morphology-Portable Than the Manipulation Grasp Object
> B2, A5, A1, and A2 share one representational bet: the locomotion control object (phase-clocked gait + velocity-tracking) transfers across embodiments more readily than the manipulation grasp object does. B2's [[2501.10100|RWM]]/[[2504.16680|RWM-U]] run the *same* world-model + MBRL pipeline across ANYmal D (quadruped) and Unitree G1 (humanoid); A5's off-policy/flow methods ([[2505.22642|FastTD3]], [[2602.02481|FPO++]]) span both unchanged; A1's perception-fusion precedent ([[2107.03996|LocoTransformer]], quadruped) transfers to bipedal terrain. A2 supplies the direct evidence that the gait's *phase* is the invariant: [[2606.01851|PHASOR]] anchors a universal action representation on motion phase for cross-embodiment transfer (90.3% R@1 Human→Robot retrieval), and [[2606.03476|Human2Humanoid]] bridges morphology gaps with a morphology-invariant end-effector loss. This is the locomotion counterpart to the morphology-invariance direction in [[Embodied-AI|Embodied-AI]] — but where manipulation needs a function-aligned action space to bridge hands, locomotion's gait structure is *already* a low-dimensional cross-morphology invariant.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Perceptive online-reference *generation* for vertical/obstacle terrain at parkour-class skill chaining | A1 | [[2604.17335\|G1 WBC-Gen+Track]] (gen+track 0.962 vs 0.230 box-climb, single-obstacle focus) + [[2602.15827\|PHP]] (parkour chaining 1.25 m wall, fixed skill graph) |
| Physics-feasibility-filtered imitation at fidelity × downstream-RL parity for extreme skills | A2 | [[2506.12851\|KungfuBot]] (53.25 mm via filtering, no downstream-RL metric) + [[2605.06593\|ReActor]] (97.45% downstream, retargeting not full filtering) |
| Non-periodic fall-recovery from arbitrary configurations across diverse real terrains | A3 | [[2502.12152\|HUMANUP]] (78.3%/98.3%, 6 terrains, single humanoid) + [[2603.20147\|AGILE]] (stand-up skill, sim-validated, no arbitrary-config robustness) |
| Embodiment-cost (GRF + acoustic + thermal) *jointly* regulated at full locomotion performance | A4 | [[2604.23702\|QuietWalk]] (acoustic + GRF, R²≈0.99, no thermal) + [[2605.27046\|Thermal-Aware Residual]] (thermal 70%→<10%, no acoustic/GRF) |
| Off-policy/flow RL wall-clock dominance over PPO across the full HumanoidBench locomotion suite | A5 | [[2505.22642\|FastTD3]] (<3 hrs, beats DreamerV3, state-based) + [[2512.01996\|Humanoid Loco 15min]] (15 min, single GPU, locomotion-focused) |
| Proprioceptive context-inference architecture matching exteroception across friction × payload × terrain | B1 | [[2107.04034\|RMA]] (proprioceptive, 12 kg, TCN fails stairs) + [[2212.07740\|TERT]] (Transformer 60% stairs vs RMA 0%, no payload-range study) |
| World-model dreaming for few-shot (~5 traj) real adaptation with calibrated epistemic bounding | B2 | [[2604.02911\|DreamTIP]] (5-traj, 100% vs 10%, no uncertainty bound) + [[2504.16680\|RWM-U]] (epistemic penalty 0.91 ANYmal D, offline not few-shot-online) |
| End-to-end mapless locomotion-to-goal with learned spatial memory + cross-platform traversability | B3 | [[2506.05997\|SRU]] (mapless memory, 23.5% over LSTM, single platform per run) + [[2604.26504\|HiPAN]] (posture-adaptive 94.7% SR, quadruped, no cross-platform) |

---

## Cross-References

- [[../../../Embodied-AI/02_Dataset-Benchmark-Environment#1. Cross-Embodiment Scale Datasets|02_Dataset-Benchmark-Environment §1]] — Cross-embodiment scale datasets (the locomotion-portability substrate for B2 + Cluster A)
- [[../../../Embodied-AI/02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02_Dataset-Benchmark-Environment §8]] — Humanoid evaluation suites (HumanoidBench and whole-body benchmarks feeding Cluster A)
- [[../../../Embodied-AI/02_Dataset-Benchmark-Environment#12. Sim-to-Real Transfer Evaluation|02_Dataset-Benchmark-Environment §12]] — Sim-to-real transfer evaluation (the deployment gate for every direction here)
- [[../../../Embodied-AI/14_Sim-to-Real-Transfer#3. Policy-Side: Robustness & Domain Randomization|14_Sim-to-Real-Transfer §3]] — Policy-side robustness + domain randomization (the proprioceptive-robustness machinery feeding B1)
- [[../../../Embodied-AI/14_Sim-to-Real-Transfer#4. Real2Sim2Real Loops & Digital Twins|14_Sim-to-Real-Transfer §4]] — Real2Sim2Real loops (the world-model adaptation machinery feeding B2)
- [[../../../Embodied-AI/14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]] — Sim-to-real design space; the transfer deep-dive underpinning Clusters A + B
- [[../../../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Robotics & embodied-AI topic overview
- [[Manipulation|Manipulation]] — Sibling Manipulation subsystem (arms + hands on objects); this doc's legs/mobility complement its grasping/dexterity — the humanoid's two embodiment halves.
- [[Whole-Body|Whole-Body]] — Sibling Whole-Body subsystem; owns the loco-manipulation coupling and mobile manipulation (arm + base) that this doc and the Manipulation doc exclude.
- [[Embodied-AI|Embodied-AI]] — Umbrella directions; its VLN direction owns the goal *reasoning* B3 cross-references, and its morphology-invariance direction is the counterpart to Cluster B's portability theme.
- [[WAM|WAM]] — World-action-model substrate; B2's dreaming borrows the WAM imagination and calibration threads.
- [[Sim2Real|Sim2Real]] — Sim-to-real transfer; owns the privileged-to-proprioceptive distillation (B1), the world-model real-adaptation machinery (B2), and the domain-randomization vs real-residual story under every direction.

> [!example] Humanoid reading path
> **Cluster A** is the humanoid's legs — whole-body balance, perceptive terrain traversal (A1), agile skills (A2), fall-recovery (A3), gait costs (A4), and the off-policy/flow training substrate (A5). For the humanoid's **upper-body manipulation** (two-arm coordination, in-hand control), read the [[Manipulation|Manipulation]] doc's **Bimanual** and **Dexterous** clusters. For the **loco-manipulation coupling** (legs stabilizing and extending the arms' workspace), read the [[Whole-Body|Whole-Body]] doc.
