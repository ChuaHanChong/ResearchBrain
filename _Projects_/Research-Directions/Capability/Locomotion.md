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
> Eight locomotion research directions across two clusters — *Bipedal Locomotion & Dynamic Skills* (A, the humanoid's legs) and *Quadruped Locomotion & Real-World Adaptation* (B) — synthesized from ~12 humanoid/quadruped/legged surveys, benchmarks, and simulators plus the frontier methods that set each bet's bar ([[2602.15827|PHP]], [[2604.17335|G1 WBC-Gen+Track]], [[2506.12851|KungfuBot]], [[2502.12152|HUMANUP]], [[2604.23702|QuietWalk]], [[2604.02911|DreamTIP]], [[2212.07740|TERT]], [[2506.05997|SRU]]). This doc is the **embodiment-axis Locomotion subsystem** (legs + wheels — *moving the body*) of a 2-axis doc family; it deliberately excludes arm/hand manipulation, mobile manipulation, and whole-body loco-manipulation coupling, which live in the sibling [[Manipulation|Manipulation]] and [[Whole-Body|Whole-Body]] docs, and it cross-references rather than re-clusters the mechanism docs ([[Embodied-AI|Embodied-AI]], [[WAM|WAM]], [[Sim2Real|Sim2Real]]) for VLN goal-reasoning, world-model imagination, and sim-to-real machinery. Each direction carries an explicit **first-principles framing** (the irreducible structure of the problem, the conventional assumption it breaks, and the measurable bet) and a **non-consensus thesis** chosen for where impactful work deviates from "more data / more scale." Every metric anchor is sourced from a cited `_KnowledgeHub_/{ID}.md` note, never invented.

---

## Methodology

**Scope.** Corpus: ~12 humanoid/quadruped/legged-locomotion surveys, benchmarks, and simulators and ~25 locomotion-method papers from `_KnowledgeHub_/`, cross-checked against [[../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] and the `Embodied-AI/` deep-dives ([[../Embodied-AI/02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]], [[../Embodied-AI/11_Sim-to-Real-Transfer|11_Sim-to-Real-Transfer]]). The method is survey-grounded ideation — surveys enumerate open problems, benchmarks fix what is measurable, frontier methods fix what is currently achievable, and each direction is filtered and framed by the bullets below. **Subsystem boundary**: this doc is locomotion *only* — generating commands that move the body via legs/wheels (gait & velocity tracking, terrain traversal, balance & push-recovery, dynamic agile skills via motion imitation, fall-recovery, proprioceptive-vs-perceptive locomotion, mapless mobility-to-goal). Whole-body loco-manipulation coupling, mobile manipulation (arm + base), and arm/hand manipulation are owned by the sibling docs and excluded here; if a paper manipulates an *object*, it is not this doc. VLN goal-*reasoning* and the world-model substrate are cross-cutting and cross-referenced to the umbrella and WAM docs, not re-clustered.

- **Survey enumeration**: tag-scan over {`humanoid`, `robotics`, `world-model`, `sim-to-real`} × {`benchmark`, `survey`} surfaced [[2403.10506|HumanoidBench]] (27-task whole-body suite), [[2502.08844|MuJoCo Playground]] (efficient sim substrate), and the workflow paper [[2603.20147|AGILE]] (five humanoid skills, locomotion subset) — each scanned for its named open problems and what its evaluation makes measurable.
- **Deep-dive mining**: reads of [[../Embodied-AI/02_Dataset-Benchmark-Environment#1. Cross-Embodiment Scale Datasets|02_Dataset-Benchmark-Environment §1]], [[../Embodied-AI/02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02 §8]], [[../Embodied-AI/11_Sim-to-Real-Transfer#3. Policy-Side: Robustness & Domain Randomization|11_Sim-to-Real-Transfer §3]]; the proprioceptive-vs-perceptive and world-model-for-adaptation threads seeded A1 (perceptive terrain), B1 (proprioceptive robustness), B2 (dreaming for adaptation).
- **Closest-baseline anchoring**: each direction's bet is pinned to the strongest existing instance it must beat — perceptive-terrain, motion-imitation, fall-recovery, embodiment-constraint, proprioceptive-robustness, and dreaming-adaptation papers ([[2602.15827|PHP]], [[2604.17335|G1 WBC-Gen+Track]], [[2506.12851|KungfuBot]], [[2502.12152|HUMANUP]], [[2604.23702|QuietWalk]], [[2107.04034|RMA]], [[2212.07740|TERT]], [[2604.02911|DreamTIP]]) set the bar.
- **Filter (maximal, quality-gated)**: admitted every direction that passes all four gates — distinct sub-problem (not a re-slice of a sibling/umbrella direction), KH-sourced measurable bet, non-consensus framing, ≥1 vault anchor with a note. **Cluster C (Wheeled Mobility & Navigation) was assessed and dropped**: the vault's wheeled/mapless-mobility control papers ([[2506.05997|SRU]] on a Unitree B2W legged-wheel platform, [[2604.26504|HiPAN]] quadruped, [[2605.28442|COTRATE]] on Husky) are platform-agnostic *locomotion-to-goal control* rather than a distinct wheeled-mobility research frontier, and the blueprint's starting anchor [[2104.11213|ManipulaTHOR]] manipulates objects (ArmPointNav = navigate-then-pick) so it is excluded by the subsystem boundary. With fewer than two distinct, non-VLN-duplicating wheeled directions, the ≥2-anchored-directions gate fails — the strongest mapless-mobility paper ([[2506.05997|SRU]]) is folded into B3 as a perceptive-locomotion-to-goal anchor and cross-referenced to the umbrella's VLN direction.
- **First-principles framing**: each direction states the irreducible structure of the problem, the conventional assumption being challenged, and the non-consensus bet — to surface where impactful work deviates from incremental refinement, not where it follows the herd.

---

## Locomotion Survey Landscape

| Survey / Benchmark | Sub-theme | Key open problems |
|---|---|---|
| [[2403.10506\|HumanoidBench]] | A: Bipedal benchmark | Flat RL fails most whole-body tasks; high-DoF action space (not observation) is the exploration bottleneck; hierarchical structure needed |
| [[2603.20147\|AGILE]] | A: Bipedal workflow | Workflow gap (late env-bug discovery) + transfer gap (fragile hardware deployment); no standardized I/O contract; motion-quality (jerk/limit) diagnostics missing |
| [[2502.08844\|MuJoCo Playground]] | A/B: Sim substrate | Sim-efficiency vs fidelity; unified GPU pipeline for legged + humanoid + arm; vision-based policy training without separate nets |
| [[2408.14472\|DWL]] | A: Perceptive bipedal | Robust locomotion on uneven terrain from *noisy proprioception alone*; partial observability; zero-shot sim-to-real without fine-tuning |
| [[2502.12152\|HUMANUP]] | A: Fall recovery | Getting-up is non-periodic, rich-contact, sparse-reward — not a locomotion variant; unpredictable post-fall configs; terrain diversity |
| [[2604.23702\|QuietWalk]] | A: Embodiment grounding | Ground-reaction-force is unmodeled; footwear/contact variation breaks gaits; acoustic + thermal cost ignored by reward |
| [[2107.04034\|RMA]] | B: Proprioceptive quadruped | Sim-to-real contact/deformable-surface gap; online adaptation without real-world fine-tuning; payload + friction shift |
| [[2212.07740\|TERT]] | B: Terrain adaptation | Cross-terrain generalization; TCN-style adaptation (RMA) fails on stairs; smooth/energy-efficient control |
| [[2206.14176\|DayDreamer]] | B: Dreaming adaptation | DRL needs millions of interactions impractical on hardware; sim-to-real gap; learning skills in hours not weeks |
| [[2504.16680\|RWM-U]] | B: World-model adaptation | Offline-MBRL distribution shift + compounding error; long-horizon dynamics inaccuracy; real-robot deployability of MBRL |
| [[2506.05997\|SRU]] | B: Mapless mobility-to-goal | Long-range mapless navigation memory; spatial recall over hundreds of steps; zero-shot transfer to legged-wheel hardware |
| [[2403.13358\|QUARD-Auto]] | B: Quadruped multi-task | Generalist quadruped skill breadth (99 sub-tasks); compute-efficient capacity (MoE active params); emergent path planning |

> [!tip] Convergence patterns
> - **The privileged-state gap, not the policy, is the locomotion bottleneck** (4-way): [[2107.04034|RMA]] (adaptation module infers privileged extrinsics from proprioception), [[2408.14472|DWL]] (denoising world model estimates true state + terrain from noisy proprioception), [[2504.16680|RWM-U]] (epistemic-uncertainty penalty steers the policy away from where the model is blind), [[2403.10506|HumanoidBench]] (flat RL fails because exploration in the high-DoF state is the wall) — same diagnosis under different vocabulary: the hard part is recovering or bounding the unobserved physical state (terrain friction, contact, payload, model error), not generating the gait. Confirmed by [[2212.07740|TERT]] (terrain-representation learning lifts stairs from RMA's 0% to 60%) and [[2604.02911|DreamTIP]] (task-invariant latent recovers 100% on a 52cm climb where the baseline gets 10%).
> - **Real-world adaptation in minutes, not millions of steps** (4-way): [[2206.14176|DayDreamer]] (A1 walks in 1 hour, recovers from pushes in 10 minutes), [[2604.02911|DreamTIP]] (5 real trajectories for stable adaptation), [[2603.15759|SimDist]] (rapid monotonic improvement in 15–30 minutes), [[2512.01996|Humanoid Loco 15min]] (sim-to-real humanoid in 15 minutes on one GPU) — the field is converging on world-model pretraining + tiny real-data adaptation as the route past the sample-efficiency wall, displacing both pure domain randomization and pure on-robot RL.
> - **Dynamic agile skills require physically-feasible references, not raw mocap** (3-way): [[2506.12851|KungfuBot]] (physics-based motion filtering rejects untrackable mocap; 53.25mm error vs >233mm baselines), [[2605.06593|ReActor]] (RL retargeting yields zero penetration + 97.45% downstream RL), [[2602.15827|PHP]] (motion-matching chains feasible skills into parkour; 1.25m wall) — converge on the insight that the imitation *target* must be physics-corrected before the policy can track it, inverting the "collect more demonstrations" reflex.
> - **Off-policy and flow RL beat the on-policy PPO default on wall-clock** (3-way): [[2505.22642|FastTD3]] (off-policy solves HumanoidBench tasks in <3 hrs, beats DreamerV3/TDMPC2/PPO in wall-clock), [[2602.02481|FPO++]] (first sim-to-real flow-policy RL for humanoid locomotion), [[2512.01996|Humanoid Loco 15min]] (massively-parallel off-policy in 15 min) — the algorithmic substrate for locomotion is shifting away from PPO, the field's reflexive default, toward off-policy/flow methods with large batches.

---

## Formal Framing

**The locomotion control object.** A locomotion policy maps observation $o$ — proprioception $q$ (joint angles, IMU, contact), optionally exteroception $e$ (depth / height-scan) — and a command $c$ (target velocity $v^*$, heading, gait, or a reference motion clip) to a joint action $a$:

$$\pi: (q, e, c) \mapsto a, \qquad a = \tau \text{ or } q^{\text{des}}$$

Locomotion is distinguished from manipulation by what the action regulates: not an object–effector **contact-state**, but the body's **base trajectory and balance** — the centre-of-mass path, foot-placement sequence, and the maintenance of dynamic stability against gravity and disturbance. The object is moved *by* the body, not *by* a grasp on an external object.

**The privileged-state / proprioception split.** Every legged-locomotion method confronts a partially-observed physical state. Let $z$ be the **privileged context** — terrain friction $\mu$, ground height field $h(\cdot)$, payload $m$, contact forces, actuator state — available in simulation but not on hardware. The deployable policy must act on $o$ alone:

| Regime | Policy input | Privileged $z$ | Exemplar |
|---|---|---|---|
| **Privileged (sim oracle)** | $(q, e, z)$ | observed | [[2107.04034\|RMA]] base policy (trains with extrinsics) |
| **Proprioceptive (blind, deployable)** | $q$ only | inferred from history $\hat{z}(q_{t-H:t})$ | [[2107.04034\|RMA]] adaptation module, [[2408.14472\|DWL]] denoising WM |
| **Perceptive (deployable + exteroception)** | $(q, e)$ | partially observed via $e$ | [[2604.17335\|G1 WBC-Gen+Track]], [[2602.15827\|PHP]] (depth) |

The central design question is **how the unobserved $z$ is recovered or bounded**: RMA *infers* $\hat z$ via a supervised adaptation module at 10 Hz; DWL *denoises* it through a world model; RWM-U *bounds* the policy's reliance on $z$ via an epistemic-uncertainty penalty $r \leftarrow r - \beta\,u_{\text{epi}}$. A1's perceptive bet, B1's proprioceptive bet, and B2's dreaming bet are three answers to the same recovery problem.

**Cross-morphology action space** — the locomotion analogue of the manipulation morphology problem (developed in [[Embodied-AI|Embodied-AI]]'s morphology-invariance direction). A quadruped (12 DoF, ANYmal/Go2) and a humanoid (≥23 DoF, G1/H1) share *gait structure* — a phase-clocked foot-contact schedule and a velocity-tracking objective — while their joint-space realization differs. [[2504.16680|RWM-U]] and [[2501.10100|RWM]] deploy the *same* world-model + MBRL pipeline across ANYmal D and Unitree G1, evidence that the locomotion control object is more morphology-portable than the manipulation grasp object — the cross-cutting lever B2 and Cluster A both rest on.

**Reference motion as a feasibility-constrained command** — [[2506.12851|KungfuBot]]:

> "A multi-step physics-based motion processing pipeline converts raw human videos into physically feasible robot reference motions, filtering unstable sequences and correcting contact issues … an adaptive motion tracking mechanism dynamically adjusts the reward's tracking factor." — [[2506.12851|KungfuBot]]

When the command $c$ is a reference clip $\xi_{1:T}$, the policy can only track what is *dynamically feasible* for the robot. Raw human mocap violates the robot's torque, contact, and balance constraints, so the tracking objective is ill-posed until $\xi$ is projected onto the feasible manifold — the reframing A2 builds on, and the inverse of the "collect more demonstrations" reflex.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Bipedal Locomotion & Dynamic Skills** | A1, A2, A3, A4, A5 | High-DoF whole-body balance under partial observation, where flat RL fails and the reference/constraint structure is the lever | A1's perceptive terrain policy needs the dynamic skills A2 imitates; A3's non-periodic fall-recovery is the boundary case A1/A2 must survive; A4 grounds all three in real GRF/thermal limits; A5 supplies the off-policy/flow training substrate the others ride on; [[2604.17335\|G1 WBC-Gen+Track]]'s gen+track and [[2602.15827\|PHP]]'s skill-chaining set the bar for A1 and A2 |
| **B — Quadruped Locomotion & Real-World Adaptation** | B1, B2, B3 | Recovering or bounding the unobserved physical state ($\mu$, $h$, payload, model error) for deployable real-world locomotion | B1's proprioceptive state-inference is the deployable floor B2's world model improves on with dreaming; B2's pretrained dynamics is what B3's mapless-to-goal policy plans through; B3 adds the perceptive goal-reaching layer B1/B2 lack; [[2107.04034\|RMA]]'s privileged-to-proprioceptive distillation and [[2604.02911\|DreamTIP]]'s dreaming-for-transfer are the shared levers across all three |

---

## Cluster A — Bipedal Locomotion & Dynamic Skills

*The humanoid's legs — whole-body balance and locomotion under partial observation, plus the dynamic agile skills (terrain traversal, parkour, dance, fall-recovery) that make a humanoid more than a slow walker. Where flat RL fails and the reference/constraint structure is the lever.*

### A1 — Perceptive Terrain Traversal & Vertical Mobility

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | *Online* reference *generation against the terrain perceived at runtime* (a fresh reference synthesized each control window from the live height-scan — not a fixed gait library, and distinct from A2's *offline* projection of a pre-recorded clip) for vertical bipedal mobility has the irreducible truth that the feasible foot-placement for a 75 cm box or a stair is a function of the *perceived* local geometry that no pre-computed reference — however feasible — can pre-encode, which breaks the field's assumption that a robust blind/flat-terrain tracker plus reactive recovery suffices for obstacle terrain, and I bet a perceptive gen+track policy lifts vertical-obstacle success from [[2604.17335\|G1 WBC-Gen+Track]]'s Tracker-Only 0.230 to ≥0.95 on an 80 cm box and chains it into [[2602.15827\|PHP]]-class parkour (1.25 m wall, peak 3.41 m/s) under live perturbation. |
| **Anchor surveys** | [[2403.10506\|HumanoidBench]], [[2408.14472\|DWL]], [[2603.20147\|AGILE]] |
| **Key targets** | [[2604.17335\|G1 WBC-Gen+Track]] 80 cm box-climb SR 0.962 (Tracker+Gen) vs 0.230 (Tracker-Only), 75 cm box + stairs + hurdles real; [[2602.15827\|PHP]] 1.25 m wall (96% height) in 3.63 s + cat-vault 3.41 m/s + 0.5 m perturbation recovery; [[2408.14472\|DWL]] zero-shot snowy-incline/stairs from proprioception alone |

**Why it matters.** [[2403.10506|HumanoidBench]] establishes the wall: flat RL "generally fails" on whole-body locomotion, and the high-dimensional action space is the exploration bottleneck. The field's robust answer is a blind, flat-terrain velocity tracker hardened by domain randomization — [[2408.14472|DWL]] is the apex of that line, achieving zero-shot snowy-incline and stair traversal from *proprioception alone* via a denoising world model. But proprioception cannot anticipate a 75 cm box: by the time the foot contacts it, the swing is already committed. [[2604.17335|G1 WBC-Gen+Track]] proves the gap quantitatively — a perceptive diffusion *generator* that produces terrain-aware references over a 0.5 s horizon lifts 80 cm box-climbing from 0.230 (tracker-only) to 0.962, and traverses 75 cm boxes, stairs, and hurdles on a real G1. [[2602.15827|PHP]] then shows the ceiling: motion-matching chains feasible skills into real parkour — a 1.25 m wall in 3.63 s, a cat-vault at 3.41 m/s, adapting to ~0.5 m obstacle displacement from onboard depth. The first-principles move: stop treating terrain as a disturbance to *reject* and start treating it as a geometry to *generate a reference against* — perception conditions the reference, not just the recovery.

**First-principles framing.**
- **First principle**: For vertical/obstacle terrain the feasible foot-placement and CoM trajectory are a function of the *local geometry ahead of the swing foot* — information that exists only in exteroception (depth/height-scan), not in proprioceptive history. A blind policy is anticipation-free by construction: it can only react after contact, and a 75 cm box punishes reaction.
- **Assumption being challenged**: That a robust blind tracker plus reactive recovery suffices for obstacle terrain. [[2408.14472|DWL]] (proprioception-only) is the strongest instance of this view; its boundary is exactly the anticipatory tasks — [[2604.17335|G1 WBC-Gen+Track]]'s 0.230→0.962 box-climb gap is the cost of blindness, which scaling proprioceptive robustness cannot close because the information is not in $q$.
- **The bet**: A perceptive gen+track policy lifts 80 cm vertical-obstacle SR from [[2604.17335|G1 WBC-Gen+Track]]'s Tracker-Only 0.230 to ≥0.95, chains it into [[2602.15827|PHP]]-class parkour (1.25 m wall, 3.41 m/s) under ~0.5 m live perturbation, while retaining [[2408.14472|DWL]]-class blind robustness on flat/rough terrain as the floor — anticipation added, robustness not lost.

**Evidence.**
- [[2604.17335|G1 WBC-Gen+Track]] — Diffusion terrain-aware motion generator + PPO tracker, receding-horizon 0.5 s references; 0.962 vs 0.230 on 80 cm box, 75 cm box + stairs + hurdles real; the perceptive-generation anchor.
- [[2602.15827|PHP]] — Motion-matching chains dynamic skills into parkour; 1.25 m wall (96% height) in 3.63 s, cat-vault 3.41 m/s, 0.5 m perturbation from depth; the dynamic-terrain ceiling.
- [[2408.14472|DWL]] — Denoising world model estimates state + terrain from noisy proprioception; zero-shot snowy/stairs/irregular, robust to pushes + partial motor failure; the proprioceptive-robustness floor to retain.
- [[2403.10506|HumanoidBench]] — 27-task MuJoCo H1 suite (12 locomotion); flat RL fails, hierarchical helps; the benchmark that frames the exploration wall.
- [[2603.20147|AGILE]] — NVIDIA workflow demonstrating velocity-tracking + height-controlled locomotion + stand-up among 5 G1/T1 skills, 6–25 hrs/task; the deployment-workflow substrate for perceptive locomotion.

**Concrete research questions.**
1. **Q1 — Perceptive reference generation vs reactive recovery on anticipatory terrain.** Ablate [[2604.17335|G1 WBC-Gen+Track]]'s generator against a blind [[2408.14472|DWL]]-style tracker + reactive recovery on graded box heights (20→80 cm) — does the 0.230→0.962 gap widen with obstacle height, confirming anticipation (not recovery) is the lever?
2. **Q2 — Receding-horizon length vs perturbation robustness.** [[2604.17335|G1 WBC-Gen+Track]] generates over 0.5 s; sweep the horizon against [[2602.15827|PHP]]'s 0.5 m perturbation — what horizon maximizes anticipatory benefit before stale references hurt under disturbance?
3. **Q3 — Skill-chaining a generated-reference library.** Combine [[2602.15827|PHP]]'s motion-matching skill graph with [[2604.17335|G1 WBC-Gen+Track]]'s online generation — can chained, perceptively-generated skills traverse a multi-obstacle course no single fixed reference covers?
4. **Q4 — Retaining blind robustness as a fallback.** When exteroception is degraded (occlusion, dark), does the perceptive policy gracefully fall back to [[2408.14472|DWL]]-class proprioceptive robustness, or does it catastrophically depend on depth?

**Related research papers.**
- [[2604.17335|G1 WBC-Gen+Track]] — Perceptive diffusion gen + RL track; 0.962 vs 0.230 box-climb; the anchor.
- [[2602.15827|PHP]] — Perceptive parkour via motion-matching; 1.25 m wall, 3.41 m/s; dynamic-terrain ceiling.
- [[2408.14472|DWL]] — Denoising-WM proprioceptive locomotion; zero-shot rough terrain; robustness floor.
- [[2107.03996|LocoTransformer]] — Cross-modal Transformer fusing depth + proprioception end-to-end; 92% farther real, 290.5–663% fewer collisions sim; the perception-fusion precedent (quadruped, transfers to bipedal).
- [[2403.10506|HumanoidBench]] — 27-task whole-body benchmark; flat RL fails; the exploration-wall framing.
- [[2603.20147|AGILE]] — Workflow with velocity-tracking + height-controlled + stand-up skills; deployment substrate.
- [[2512.01996|Humanoid Loco 15min]] — Rough-terrain + push-robust humanoid locomotion in 15 min; fast-iteration substrate for perceptive policies.
- [[2502.08844|MuJoCo Playground]] — GPU sim with vision-based policy training; the perceptive-training simulator.

**Benchmarks & metrics.**
- [[2604.17335|G1 WBC-Gen+Track]] — 80 cm box-climb SR 0.962 vs 0.230, generalization across obstacle heights/orientations; the perceptive-vertical-mobility metric.
- [[2602.15827|PHP]] — 0.95 on 76 cm wall at 1.0 m/s, 0.90 on 94 cm wall at 2.0 m/s, real 1.25 m wall; the dynamic-parkour metric.
- [[2403.10506|HumanoidBench]] — 12 locomotion tasks on H1 with 151D proprioception; flat-RL failure rate; the whole-body-locomotion difficulty gradient.

> [!warning] Risks
> - **Perception failure is catastrophic, not graceful** — a depth dropout mid-vault can be fatal where a blind policy would have stumbled and recovered. → Q4's fallback test is the go/no-go; require a proprioceptive safety mode underneath the perceptive policy (couples to A3 fall-recovery).
> - **Generated references can be infeasible** — a diffusion generator may propose a reference the tracker cannot execute. → [[2604.17335|G1 WBC-Gen+Track]]'s RL fine-tuning filters infeasible references; report the tracker's reject/clamp rate, not just headline SR.
> - **Parkour-class skills risk hardware damage** — 1.25 m walls and 3.41 m/s vaults stress real humanoids. → Bound aggressive-skill claims to validated platforms; report contact-force and motor-temperature during dynamic skills (couples to A4).

### A2 — Dynamic Agile Skills via Physically-Feasible Motion Imitation

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | *Offline* projection of a *fixed, pre-recorded mocap clip* onto the robot's *dynamically-feasible* manifold *before* imitation — a one-time correction of a given motion, not A1's per-step generation against live terrain — has the irreducible truth that the tracking objective is ill-posed when the reference violates the robot's torque/contact/balance constraints, which breaks the field's reflex to "collect more demonstrations" as if data quantity were the bottleneck, and I bet a physics-corrected reference pipeline cuts tracking error to [[2506.12851\|KungfuBot]]'s 53.25 mm (vs >233 mm for OmniH2O/ExBody2) and lifts downstream RL success to [[2605.06593\|ReActor]]'s 97.45% (G1) at zero ground/self-penetration. |
| **Anchor surveys** | [[2403.10506\|HumanoidBench]], [[2603.20147\|AGILE]], [[2502.08844\|MuJoCo Playground]] |
| **Key targets** | [[2506.12851\|KungfuBot]] 53.25 mm global mean body-position error (easy) vs OmniH2O/ExBody2 >233 mm, untrackable-motion rejection (max 54% episode-length ratio); [[2605.06593\|ReActor]] 0.00% penetration + 0.17 cm/s foot-slide + 97.45% (G1) / 95.07% (Lima) downstream RL (+15.22 pp); [[2605.10063\|EFGCL]] backflip/lateral-flip unlearnable by PPO + 2× faster jump |

**Why it matters.** The reflexive recipe for agile humanoid skills is "imitate more human motion." But raw mocap is *physically infeasible* for the robot — a human's backflip violates the robot's torque limits, contact timing, and balance margins, so the tracking reward is optimizing toward a target the robot can never reach. [[2506.12851|KungfuBot]] diagnoses this precisely: a physics-based motion-processing pipeline *filters untrackable sequences and corrects contact issues* before RL, achieving a 53.25 mm global mean body-position error on easy motions where deployable baselines (OmniH2O, ExBody2) exceed 233 mm — a 4× error reduction from fixing the *target*, not the policy. [[2605.06593|ReActor]] makes the same move with RL-based physics-aware retargeting: zero ground/self-penetration, 0.17 cm/s foot-sliding, and 97.45% downstream RL on G1 (vs 79.85–95.51% baselines, +15.22 pp). [[2605.10063|EFGCL]] shows the payoff at the extreme — external-force-guided curriculum learns backflips and lateral-flips that a PPO baseline simply cannot, and accelerates jump-learning 2×. The non-consensus claim: agile-skill quality is bottlenecked by the *feasibility of the reference*, not the *quantity of demonstrations* — fix the target manifold and small data suffices.

**First-principles framing.**
- **First principle**: A tracking objective $\min \|\,x_{\text{robot}} - \xi_{\text{ref}}\,\|$ is only well-posed if $\xi_{\text{ref}}$ lies on the robot's dynamically-feasible manifold. Raw human mocap does not — it violates torque, contact-timing, and balance constraints — so the irreducible first step is *projection onto feasibility*, after which imitation is tractable. The infeasible-reference problem is upstream of any data-quantity question.
- **Assumption being challenged**: That agile-skill competence scales with demonstration quantity. The field collects ever-larger mocap corpora; [[2506.12851|KungfuBot]]'s rejection of untrackable motions (max 54% episode-length ratio) and 4× error reduction from *filtering* show the binding constraint is reference feasibility, not data volume — more infeasible demonstrations do not help.
- **The bet**: A physics-corrected reference pipeline cuts tracking error to [[2506.12851|KungfuBot]]'s 53.25 mm (vs >233 mm OmniH2O/ExBody2) and lifts downstream RL success to [[2605.06593|ReActor]]'s 97.45% (G1) at zero ground/self-penetration, enabling [[2605.10063|EFGCL]]-class extreme skills (backflips) on small data — feasibility-first imitation, not data-scale imitation.

**Evidence.**
- [[2506.12851|KungfuBot]] — Physics-based motion filtering + adaptive tracking factor; 53.25 mm vs >233 mm baselines, zero-shot martial-arts/dance on G1; the feasibility-filtering anchor.
- [[2605.06593|ReActor]] — RL physics-aware motion retargeting; 0.00% penetration, 0.17 cm/s slide, 97.45% (G1) / 95.07% (Lima) downstream RL, +15.22 pp; the retargeting anchor.
- [[2605.10063|EFGCL]] — External-force-guided curriculum; backflip/lateral-flip unlearnable by PPO, 2× faster jump, physical KLEIYN; the extreme-skill enabler.
- [[2604.17335|G1 WBC-Gen+Track]] — Generated references filtered by an RL tracker for feasibility; the gen-side complement to filter-side feasibility (feeds A1).
- [[2603.20147|AGILE]] — Motion-imitation among its 5 demonstrated skills + motion-quality (jerk/limit) diagnostics; the imitation-deployment substrate.

**Concrete research questions.**
1. **Q1 — Filter-then-track vs track-raw on error and stability.** Isolate [[2506.12851|KungfuBot]]'s physics filter: does pre-filtering untrackable motions deliver the 233→53 mm error reduction over tracking raw mocap, and does the gain concentrate on dynamic (vs quasi-static) skills?
2. **Q2 — Adaptive tracking factor vs fixed tolerance.** [[2506.12851|KungfuBot]] dynamically adjusts the reward's tracking factor; ablate against a fixed tolerance — does curriculum on tolerance learn dynamic skills a fixed reward cannot?
3. **Q3 — Retargeting-quality → downstream-RL-success transfer.** [[2605.06593|ReActor]]'s zero-penetration retargeting yields +15.22 pp downstream; quantify the retargeting-feasibility → RL-SR curve — is penetration/foot-slide a predictor of trainability?
4. **Q4 — External-force curriculum for unlearnable skills.** [[2605.10063|EFGCL]] uses guiding forces to bootstrap backflips; test whether the force-curriculum generalizes across extreme skills (flips, spins) and how feasibility-filtering and force-guidance compose.

**Related research papers.**
- [[2506.12851|KungfuBot]] — Physics-based motion processing + adaptive tracking; 53.25 mm; the anchor.
- [[2605.06593|ReActor]] — RL physics-aware retargeting; 97.45% downstream, zero penetration; the retargeting anchor.
- [[2605.10063|EFGCL]] — Force-guided curriculum; backflips unlearnable by PPO; extreme-skill enabler.
- [[2604.17335|G1 WBC-Gen+Track]] — Generated + RL-filtered references; gen-side feasibility (feeds A1).
- [[2403.10506|HumanoidBench]] — Whole-body benchmark including dynamic tasks; the difficulty framing.
- [[2603.20147|AGILE]] — Motion-imitation skill + motion-quality diagnostics; deployment substrate.
- [[2604.24916|asRoBallet]] — Friction-aware RL on underactuated spherical dynamics; zero-shot sim2real (0.05 m/s MAE), recovers from 0.3 m pushes; the underactuated-dynamics feasibility precedent.
- [[2502.08844|MuJoCo Playground]] — Efficient sim for motion-tracking + dance sequences; the agile-skill training substrate.

**Benchmarks & metrics.**
- [[2506.12851|KungfuBot]] — 53.25 mm global mean body-position error (easy) vs >233 mm OmniH2O/ExBody2, episode-length-ratio rejection (max 54% for untrackable); the imitation-fidelity metric.
- [[2605.06593|ReActor]] — 0.00% penetration time/depth, 0.17 cm/s foot-slide, 97.45% (G1) downstream RL (vs 79.85–95.51%); the retargeting-quality metric.
- [[2605.10063|EFGCL]] — Backflip/lateral-flip learnability vs PPO (unlearnable), 2× jump-learning speedup; the extreme-skill metric.

> [!warning] Risks
> - **Physics-filtering needs an accurate robot model** — feasibility correction is only as good as the URDF/dynamics. → Validate the feasibility manifold against hardware; report sim-tracking vs real-tracking error gap ([[2506.12851|KungfuBot]] reports close real-sim match).
> - **Filtering discards expressive motions** — rejecting "untrackable" mocap may cut the most striking skills. → Couple filtering with [[2605.10063|EFGCL]]-style force-guidance that *expands* feasibility rather than only pruning; report the recovered-skill fraction.
> - **Downstream-RL gains may be task-specific** — +15.22 pp on tracked motions may not transfer to novel skills. → Q3's feasibility→trainability curve tests generality; report across skill classes, not a single average.

### A3 — Autonomous Fall Recovery as Non-Periodic Whole-Body Control

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Treating getting-up as its own non-periodic, rich-contact, sparse-reward control problem — not a degenerate gait — has the irreducible truth that fall-recovery has no phase clock and no nominal contact schedule, so the inductive biases that make locomotion learnable (periodicity, foot-contact priors) actively mislead it, which breaks the field's assumption that a locomotion policy plus a scripted recovery routine is enough for autonomy, and I bet a two-stage discover-then-deploy curriculum recovers from arbitrary fall configurations at [[2502.12152\|HUMANUP]]'s 78.3% supine / 98.3% roll-over success in ~6 s (vs the manufacturer's 11 s and most-terrain failure) across ≥6 terrains. |
| **Anchor surveys** | [[2502.12152\|HUMANUP]], [[2403.10506\|HumanoidBench]], [[2603.20147\|AGILE]] |
| **Key targets** | [[2502.12152\|HUMANUP]] 78.3% getting-up (supine) + 98.3% roll-over real on 6 terrains (concrete/muddy-grass/snow), ~6 s vs manufacturer 11 s, 20,000 randomized initial postures, lower arm-motor temperature; [[2603.20147\|AGILE]] stand-up among its 5 demonstrated G1/T1 skills as the workflow baseline |

**Why it matters.** A humanoid that cannot stand up after a fall is not autonomous — it needs a human. Yet [[2502.12152|HUMANUP]] identifies why getting-up resists the locomotion playbook: it is *non-periodic* (no gait cycle), involves *rich whole-body contact* (the robot is lying on the ground in an unknown configuration), and has *sparse reward* (success is a single binary at the end). The periodicity priors and foot-contact schedules that make walking learnable do not apply — they mislead. [[2502.12152|HUMANUP]]'s solution is a two-stage RL curriculum: a *Discovery Policy* in simplified simulation with weak regularization finds a high-speed trajectory through the sparse-reward landscape, then a *Deployable Policy* refines it over 20,000 randomized initial lying postures and diverse terrains with strong regularization for sim-to-real. The result: 78.3% supine getting-up and 98.3% roll-over on a real G1 across 6 terrains (concrete, muddy grass, snow), recovering in ~6 s — more than twice as fast as the manufacturer's 11 s, with smoother motion and lower (safer) arm-motor temperatures. The first-principles claim: fall-recovery is a *distinct* control problem whose structure (no phase, arbitrary initial state) demands a discovery-then-deploy curriculum, not a locomotion policy with a recovery bolt-on.

**First-principles framing.**
- **First principle**: Fall-recovery has no phase clock and no nominal contact schedule — the initial state is an arbitrary post-fall configuration and the contact set is unknown. The phase-clocked, foot-contact-prior structure that makes locomotion a well-shaped RL problem is *absent*; worse, imposing it biases the policy away from the contact-rich ground transitions recovery requires.
- **Assumption being challenged**: That a locomotion policy plus a scripted recovery routine yields autonomy. Manufacturer controllers script recovery and fail on most terrains ([[2502.12152|HUMANUP]] reports this directly); the assumption breaks because a script cannot cover the continuum of post-fall configurations, and a periodic locomotion policy has the wrong inductive bias for non-periodic ground-up motion.
- **The bet**: A two-stage discover-then-deploy curriculum recovers from arbitrary fall configurations at [[2502.12152|HUMANUP]]'s 78.3% supine / 98.3% roll-over success in ~6 s (vs manufacturer 11 s and most-terrain failure) across ≥6 terrains, with single-stage training failing to converge — confirming that motion *discovery* (not just refinement) is the load-bearing stage.

**Evidence.**
- [[2502.12152|HUMANUP]] — Two-stage discover-then-deploy RL curriculum; 78.3% supine / 98.3% roll-over real, 6 terrains, ~6 s vs 11 s, 20,000 randomized postures; the fall-recovery anchor.
- [[2403.10506|HumanoidBench]] — Establishes whole-body RL difficulty and the high-DoF exploration wall that sparse-reward recovery exemplifies; the difficulty framing.
- [[2603.20147|AGILE]] — Demonstrates a stand-up skill among 5 G1/T1 behaviors with value-bootstrapped terminations + virtual harness for early stabilization; the workflow-stabilization complement.
- [[2604.17335|G1 WBC-Gen+Track]] — RL-filtered generated motion as a route to robust contact-rich behavior; the generation-side analogue for recovery references.
- [[2512.01996|Humanoid Loco 15min]] — Push-robust locomotion (the disturbance that precedes a fall); the upstream balance layer recovery backstops.

**Concrete research questions.**
1. **Q1 — Discovery stage vs single-stage training.** [[2502.12152|HUMANUP]] reports single-stage training fails to converge; quantify how much the simplified-sim weak-regularization discovery stage contributes — is motion *discovery* the load-bearing stage on the sparse-reward landscape?
2. **Q2 — Posture-randomization breadth vs recovery generality.** Sweep the number of randomized initial lying postures (toward [[2502.12152|HUMANUP]]'s 20,000) against recovery success on held-out configurations — what coverage is needed for arbitrary-config robustness?
3. **Q3 — Terrain-conditioned recovery.** [[2502.12152|HUMANUP]] recovers on 6 terrains; does conditioning the recovery policy on perceived terrain (slope, compliance) improve success on extreme surfaces (snow, mud) over a terrain-blind policy?
4. **Q4 — Recovery as a safety mode under A1's perceptive policy.** Wire fall-recovery as the fallback when A1's perceptive terrain policy fails (perception dropout, lost balance) — does a unified locomotion+recovery stack achieve end-to-end autonomy on a multi-obstacle course?

**Related research papers.**
- [[2502.12152|HUMANUP]] — Two-stage getting-up curriculum; 78.3%/98.3%, ~6 s; the anchor.
- [[2403.10506|HumanoidBench]] — Whole-body benchmark; the sparse-reward-difficulty framing.
- [[2603.20147|AGILE]] — Stand-up skill + virtual-harness stabilization; workflow complement.
- [[2604.17335|G1 WBC-Gen+Track]] — RL-filtered generated motion for contact-rich behavior; generation-side analogue.
- [[2512.01996|Humanoid Loco 15min]] — Push-robust locomotion; the pre-fall balance layer.
- [[2505.22642|FastTD3]] — Off-policy RL solving sparse-reward HumanoidBench tasks fast; the sample-efficient substrate for sparse-reward recovery (feeds A5).
- [[2602.02481|FPO++]] — Stable flow-policy RL for humanoid whole-body; the policy-class option for non-periodic control.
- [[2502.08844|MuJoCo Playground]] — Efficient sim for the 20,000-posture randomization; the recovery-training substrate.

**Benchmarks & metrics.**
- [[2502.12152|HUMANUP]] — 78.3% supine getting-up / 98.3% roll-over, ~6 s vs 11 s manufacturer, 6 terrains, arm-motor temperature; the fall-recovery metric.
- [[2403.10506|HumanoidBench]] — Sparse-reward whole-body tasks where flat RL fails; the exploration-difficulty diagnostic for non-periodic control.
- [[2603.20147|AGILE]] — Stand-up among 5 demonstrated skills, motion-quality (jerk/acceleration/joint-limit) diagnostics; the deployment-quality metric.

> [!warning] Risks
> - **Recovery motions stress hardware** — flailing limbs and ground impacts risk motor/joint damage. → [[2502.12152|HUMANUP]]'s strong regularization lowers arm-motor temperature; report contact-force and temperature, treat smoothness as a first-class objective.
> - **Discovery may find unsafe trajectories** — weak-regularization discovery can produce violent motions infeasible for hardware. → The two-stage design refines discovery into a deployable policy; report the discovery→deployment safety-margin gap.
> - **Real fall configurations exceed simulation coverage** — 20,000 postures may miss adversarial real falls. → Q2's coverage curve bounds the claim; report failure modes by initial-configuration class, not a single average.

### A4 — Embodiment-Grounded Locomotion Constraints (Force, Acoustic, Thermal)

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Making the *physical cost* of a gait — ground-reaction force, acoustic emission, motor thermal load — a first-class predicted-and-regulated quantity, not an ignored externality, has the irreducible truth that a real robot's gait is bounded by embodiment limits (motor temperature, contact force, noise) that simulation reward functions silently omit, which breaks the field's assumption that task-success rewards alone yield deployable gaits, and — since no existing policy regulates more than one such cost at once — I bet a *single* physics-informed residual cost-head, driven by a GRF predictor at [[2604.23702\|QuietWalk]]'s R²≈0.99, *jointly* holds motor-overheating below [[2605.27046\|Thermal-Aware Residual]]'s <10% (from 70%) **and** acoustic emission within +1 dBA of [[2604.23702\|QuietWalk]]'s quiet-policy mean, at ≤5% task-SR loss versus the cost-blind base policy. |
| **Anchor surveys** | [[2604.23702\|QuietWalk]], [[2603.20147\|AGILE]], [[2403.10506\|HumanoidBench]] |
| **Key targets** | [[2604.23702\|QuietWalk]] GRF-predictor RMSE 14.49/14.00 N (R²=0.9887/0.9899), noise reduction 7.17 dBA mean / 4.98 dBA peak across 4 footwear types (barefoot→high heels) + outdoor terrains; [[2605.27046\|Thermal-Aware Residual]] motor-overheating 70%→<10%, 650 m outdoor + 3 kg payload, peak temp <50 °C |

**Why it matters.** Simulation rewards task success — reach the velocity, climb the box — and silently omit the *physical cost* the real robot pays: motors overheat, gaits are loud, contact forces spike. These are not cosmetic. [[2605.27046|Thermal-Aware Residual]] shows motor overheating reaches 70% in high-temperature terrain traversal without thermal management — a robot that thermally shuts down mid-task has zero success regardless of its policy; a residual thermal policy drops this to <10% while completing a 650 m outdoor path with a 3 kg payload at peak temperatures below 50 °C, *without* sacrificing terrain adaptability. [[2604.23702|QuietWalk]] addresses the acoustic + contact axis: a physics-informed GRF predictor (RMSE ~14 N, R²≈0.99) drives a quiet RL policy that cuts gait noise by 7.17 dBA mean / 4.98 dBA peak across four footwear types — barefoot, sneakers, skate shoes, even high heels — and outdoor terrains, approaching an engineered-controller noise baseline. The non-consensus claim: deployability is bounded by embodiment *costs* that the standard task reward ignores, and predicting-then-regulating those costs (GRF, noise, temperature) is a distinct lever from improving task success — a quiet, cool, low-impact gait is a *different* objective, not a free byproduct of a good tracker.

**First-principles framing.**
- **First principle**: A real robot's gait is bounded by hard embodiment limits — motor temperature ceilings, actuator force limits, and (for deployment around people) acoustic budgets — that exist *off* the simulation reward surface. A policy optimizing only task success will saturate these limits because nothing in its objective penalizes them; the cost is invisible until the hardware fails or the gait is unacceptable.
- **Assumption being challenged**: That task-success rewards alone yield deployable gaits. The field tunes velocity-tracking and terrain rewards; [[2605.27046|Thermal-Aware Residual]]'s 70% overheating rate under standard policies shows the embodiment cost is *load-bearing for deployment* — a thermally-blind policy is undeployable on hot terrain regardless of its tracking reward.
- **The bet**: The gap is not hitting one paper's number — [[2604.23702|QuietWalk]] already cuts noise (7.17 dBA) and [[2605.27046|Thermal-Aware Residual]] already drops overheating (70%→<10%), but each as a *separate* single-cost policy. The bet is *joint* regulation: a single residual cost-head, driven by a GRF predictor at [[2604.23702|QuietWalk]]'s R²≈0.99, simultaneously holds overheating <10% **and** acoustic emission ≤+1 dBA over [[2604.23702|QuietWalk]]'s quiet-policy mean, at ≤5% task-SR loss versus the cost-blind base — one head trading the costs against each other, not two policies optimizing in isolation.

**Evidence.**
- [[2604.23702|QuietWalk]] — Physics-informed GRF predictor (R²=0.989) + quiet RL policy; 7.17 dBA mean / 4.98 dBA peak noise cut across 4 footwear + outdoor terrains; the acoustic/contact-cost anchor.
- [[2605.27046|Thermal-Aware Residual]] — Residual thermal policy; overheating 70%→<10%, 650 m + 3 kg, <50 °C; the thermal-cost anchor.
- [[2502.12152|HUMANUP]] — Strong regularization yields lower (safer) arm-motor temperatures during recovery; the temperature-as-objective precedent (feeds A3).
- [[2603.20147|AGILE]] — Motion-quality diagnostics (acceleration, jerk, joint-limit violations) as deployment-critical metrics; the cost-diagnostics substrate.
- [[2403.10506|HumanoidBench]] — High-DoF action space where unregulated control stresses actuators; the embodiment-stress framing.

**Concrete research questions.**
1. **Q1 — Predict-then-regulate vs penalty-only.** Compare [[2604.23702|QuietWalk]]'s GRF-predictor-driven policy against a reward-penalty-only quiet policy — does explicit force *prediction* (R²≈0.99) regulate contact better than penalizing measured force after the fact?
2. **Q2 — Residual cost-policy vs monolithic.** [[2605.27046|Thermal-Aware Residual]] notes monolithic thermal policies respond slowly and fail complex terrain; quantify the residual-vs-monolithic trade-off — does decoupling cost-regulation from the base locomotion policy preserve terrain adaptability?
3. **Q3 — Footwear/contact generalization.** [[2604.23702|QuietWalk]] spans barefoot→high heels; test whether GRF prediction generalizes to unseen contact interfaces (ice, soft ground) and whether the noise/force objective transfers.
4. **Q4 — Joint cost objective.** Combine thermal + acoustic + force into a single cost-aware reward; does a unified embodiment-cost objective dominate single-cost policies, and where do the costs trade off (a quiet gait may be hotter)?

**Related research papers.**
- [[2604.23702|QuietWalk]] — Physics-informed GRF-aware quiet locomotion; R²=0.989, 7.17 dBA; the acoustic/force anchor.
- [[2605.27046|Thermal-Aware Residual]] — Residual thermal-safety policy; 70%→<10% overheating; the thermal anchor.
- [[2502.12152|HUMANUP]] — Temperature-lowering regularization; the motor-temperature precedent.
- [[2603.20147|AGILE]] — Motion-quality (jerk/limit) diagnostics; cost-diagnostics substrate.
- [[2403.10506|HumanoidBench]] — Whole-body actuator-stress benchmark; the embodiment-cost framing.
- [[2512.01996|Humanoid Loco 15min]] — Extended-duration deployment where thermal/wear costs compound; the long-deployment substrate.
- [[2603.20147|AGILE]] — L2C2 regularization reducing RMS joint acceleration/jerk; the smoothness-as-cost mechanism.
- [[2502.08844|MuJoCo Playground]] — Efficient sim for training cost-aware policies with physics-informed predictors.

**Benchmarks & metrics.**
- [[2604.23702|QuietWalk]] — GRF RMSE 14.49/14.00 N (R²=0.9887/0.9899), 7.17 dBA mean noise cut across 4 footwear; the acoustic/contact-cost metric.
- [[2605.27046|Thermal-Aware Residual]] — Overheating 70%→<10%, 650 m + 3 kg at <50 °C; the thermal-cost metric.
- [[2603.20147|AGILE]] — Acceleration/jerk/joint-limit-violation diagnostics with HTML reports; the motion-cost diagnostic.

> [!warning] Risks
> - **Cost-regulation can degrade task performance** — a quiet/cool gait may be slower or less agile. → [[2605.27046|Thermal-Aware Residual]] preserves locomotion performance via a residual; report the cost-vs-task Pareto front, not a single number.
> - **GRF/thermal models are platform-specific** — R²≈0.99 on one robot may not transfer. → Q3 tests generalization; treat cost predictors as per-platform-calibrated, report the transfer gap.
> - **Acoustic metrics are environment-dependent** — dBA depends on surface and room. → [[2604.23702|QuietWalk]] reports across 4 surfaces; report noise distribution per surface, not a single average.

### A5 — Sample-Efficient Off-Policy & Flow Locomotion Learning

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Replacing PPO — the field's reflexive default — with off-policy and flow-based RL for humanoid locomotion has the irreducible truth that locomotion's dense reward and massively-parallel simulation make sample-reuse and large-batch off-policy updates strictly more efficient than on-policy rollout-discard, which breaks the assumption that PPO's stability is worth its sample-inefficiency for high-DoF control, and I bet an off-policy/flow learner solves [[2403.10506\|HumanoidBench]] tasks in [[2505.22642\|FastTD3]]'s <3 hours (beating DreamerV3/TDMPC2/PPO on wall-clock) and trains a deployable humanoid gait in [[2512.01996\|Humanoid Loco 15min]]'s 15 minutes on a single GPU. |
| **Anchor surveys** | [[2403.10506\|HumanoidBench]], [[2502.08844\|MuJoCo Playground]], [[2603.20147\|AGILE]] |
| **Key targets** | [[2505.22642\|FastTD3]] solves HumanoidBench tasks <3 hrs on one A100 (beats PPO/SAC/SimbaV2/TDMPC2/DreamerV3 wall-clock), real Booster T1, batch 32,768 + distributional critic; [[2512.01996\|Humanoid Loco 15min]] sim-to-real G1+T1 in 15 min on one RTX 4090; [[2602.02481\|FPO++]] first sim-to-real flow-policy RL for humanoid locomotion |

**Why it matters.** Almost every locomotion paper above trains with PPO — it is the field's reflexive default, chosen for stability. But locomotion has two properties that make on-policy rollout-discard wasteful: a *dense* reward (velocity tracking gives signal every step, unlike sparse manipulation) and *massively-parallel* simulation (thousands of environments). [[2505.22642|FastTD3] proves the cost of the default: a simple off-policy TD3 variant with large batches (32,768) and a distributional critic solves HumanoidBench tasks in under 3 hours on a single A100, beating PPO, SAC, SimbaV2, TDMPC2, *and* DreamerV3 on wall-clock — and it transfers to a real Booster T1, a documented full-size-humanoid off-policy deployment. [[2512.01996|Humanoid Loco 15min]] pushes further: a deployable G1/T1 gait (push-robust, dance-capable) in 15 minutes on a single RTX 4090. [[2602.02481|FPO++]] opens a third axis — the first sim-to-real flow-policy RL for humanoid locomotion, robust gaits from flow-based action distributions. The non-consensus claim: PPO's stability is *not* worth its sample-inefficiency for dense-reward, parallel-sim locomotion — off-policy and flow methods dominate on the metric that matters for iteration (wall-clock to a deployable gait), and the field's PPO habit is leaving an order of magnitude on the table.

**First-principles framing.**
- **First principle**: Sample efficiency is governed by how often each environment step informs a gradient update. Off-policy replay reuses every transition many times; on-policy PPO discards each rollout after one update. With locomotion's dense reward (informative gradient every step) and parallel sim (cheap transitions), the off-policy advantage compounds — sample-reuse is strictly more efficient when transitions are plentiful and individually informative.
- **Assumption being challenged**: That PPO's stability is worth its sample-inefficiency for high-DoF locomotion. The field defaults to PPO across nearly every paper here; [[2505.22642|FastTD3]]'s wall-clock win over PPO *and* DreamerV3/TDMPC2 — with "complex architectural stabilizers found unnecessary" — shows the stability premium is overpriced for this regime.
- **The bet**: An off-policy/flow learner solves [[2403.10506|HumanoidBench]] tasks in [[2505.22642|FastTD3]]'s <3 hours (beating DreamerV3/TDMPC2/PPO on wall-clock) and trains a deployable humanoid gait in [[2512.01996|Humanoid Loco 15min]]'s 15 minutes on a single consumer GPU — off-policy/flow dominance on wall-clock-to-deployment, with the PPO default left behind.

**Evidence.**
- [[2505.22642|FastTD3]] — Off-policy TD3 with batch 32,768 + distributional critic; HumanoidBench tasks <3 hrs, beats PPO/SAC/SimbaV2/TDMPC2/DreamerV3 wall-clock, real Booster T1; the off-policy anchor.
- [[2512.01996|Humanoid Loco 15min]] — Massively-parallel sim-to-real humanoid locomotion in 15 min on RTX 4090, push-robust + dance; the fast-training anchor.
- [[2602.02481|FPO++]] — Flow policy gradients; first sim-to-real flow-policy RL for humanoid locomotion + motion tracking; the flow-policy anchor.
- [[2502.08844|MuJoCo Playground]] — GPU-parallel sim, training in minutes/hours, zero-shot to Go1 + Berkeley Humanoid; the parallel-sim substrate the off-policy advantage exploits.
- [[2403.10506|HumanoidBench]] — The benchmark on which wall-clock-to-solve is measured; the difficulty reference.

**Concrete research questions.**
1. **Q1 — Off-policy vs PPO wall-clock on locomotion.** Reproduce [[2505.22642|FastTD3]]'s wall-clock win across HumanoidBench locomotion tasks — does the off-policy advantage scale with reward density and environment count, confirming the dense-reward/parallel-sim thesis?
2. **Q2 — Batch size + distributional critic ablation.** [[2505.22642|FastTD3]] credits batch 32,768 + a distributional critic; ablate each — which is the load-bearing component for stable high-DoF off-policy control?
3. **Q3 — Flow vs Gaussian policy for locomotion.** [[2602.02481|FPO++]] uses flow policies; compare flow vs Gaussian action distributions on gait quality and sim-to-real robustness — does the richer distribution help multimodal contact?
4. **Q4 — 15-minute training as an iteration loop.** [[2512.01996|Humanoid Loco 15min]] trains in 15 min; quantify how sub-hour training changes the *research* loop — can it enable rapid reward/curriculum iteration that PPO's hours-to-days cannot?

**Related research papers.**
- [[2505.22642|FastTD3]] — Fast off-policy humanoid RL; <3 hrs, beats DreamerV3; the anchor.
- [[2512.01996|Humanoid Loco 15min]] — 15-min sim-to-real humanoid locomotion; fast-training anchor.
- [[2602.02481|FPO++]] — Flow policy gradients; first flow-policy sim-to-real locomotion; flow anchor.
- [[2502.08844|MuJoCo Playground]] — GPU-parallel sim; the substrate exploiting off-policy reuse.
- [[2403.10506|HumanoidBench]] — Wall-clock-to-solve benchmark; the difficulty reference.
- [[2603.20147|AGILE]] — Scalable RL infrastructure + L2C2 regularization, 6–25 hrs/task; the workflow baseline off-policy methods undercut.
- [[2604.02911|DreamTIP]] — Dreamer-based transfer as the model-based alternative; the MBRL comparison point (feeds B2).
- [[2504.16680|RWM-U]] — Uncertainty-aware MBRL for legged control; the model-based-RL counterpoint to model-free off-policy (feeds B2).

**Benchmarks & metrics.**
- [[2505.22642|FastTD3]] — HumanoidBench/IsaacLab/MuJoCo-Playground wall-clock to solve (<3 hrs), beats PPO/SAC/TDMPC2/DreamerV3; the wall-clock-efficiency metric.
- [[2512.01996|Humanoid Loco 15min]] — 15-min sim-to-real on RTX 4090; the training-time metric.
- [[2403.10506|HumanoidBench]] — 27-task suite where flat-RL training cost is the baseline; the algorithmic-efficiency diagnostic.

> [!warning] Risks
> - **Off-policy instability on sparse-reward skills** — the dense-reward advantage may not hold for sparse fall-recovery (A3). → Bound the bet to dense-reward locomotion; report where off-policy degrades vs PPO on sparse tasks.
> - **Sim-to-real of fast-trained policies may be brittle** — 15-min policies may overfit sim. → [[2512.01996|Humanoid Loco 15min]] and [[2505.22642|FastTD3]] both deploy real; report the sim-to-real SR gap, not just sim wall-clock.
> - **Consumer-GPU results may not scale to perception** — vision-based perceptive policies (A1) cost more. → Report wall-clock separately for state-based vs vision-based locomotion; the 15-min number is state-based.

---

## Cluster B — Quadruped Locomotion & Real-World Adaptation

*Recovering or bounding the unobserved physical state — terrain friction, ground height, payload, model error — that separates a sim-trained quadruped policy from a deployable one. Proprioceptive robustness, world-model dreaming for few-shot adaptation, and perceptive mapless mobility-to-goal.*

### B1 — Proprioceptive-Only Robustness under Disturbance & Payload

| | |
|---|---|
| **Cluster** | B — Quadruped Locomotion & Real-World Adaptation |
| **Thesis** | Inferring the unobserved environment context from proprioceptive *history* alone — rather than depending on exteroception or online real-world fine-tuning — has the irreducible truth that the privileged state (friction, payload, terrain) leaves a recoverable signature in the recent proprioceptive trajectory, which breaks the field's assumption that robust deployment needs either vision or real-world adaptation trials, and I bet a proprioceptive context-inference module sustains locomotion under [[2107.04034\|RMA]]'s 12 kg payload (80% body weight) and lifts stair traversal to [[2212.07740\|TERT]]'s 60% where TCN-style RMA scores 0%, at 100 Hz control / 10 Hz adaptation with zero real-world fine-tuning. |
| **Anchor surveys** | [[2107.04034\|RMA]], [[2212.07740\|TERT]], [[2403.10506\|HumanoidBench]] |
| **Key targets** | [[2107.04034\|RMA]] 12 kg payload (80% body weight) on sand/mud/rocky/slippery, 100 Hz base / 10 Hz adaptation, zero real-world fine-tuning; [[2212.07740\|TERT]] 100% sand / 60% stairs vs RMA 0% across 9 terrains; [[2403.13358\|QUARD-Auto]] 71–90.5% across 99 quadruped sub-tasks at 39.31M active params |

**Why it matters.** A quadruped's deployable policy must act on proprioception alone — joint angles, IMU, contact — because the privileged context that simulation provides (terrain friction $\mu$, payload $m$, ground compliance) is unavailable on hardware. The field's two escape routes are exteroception (add a camera) or online adaptation (fine-tune on the real robot). [[2107.04034|RMA]] shows neither is necessary: a base policy trained with a privileged "extrinsics vector," paired with an adaptation module that *infers that vector from the recent proprioceptive history* at 10 Hz, lets a Unitree A1 traverse sand, mud, rocky, and slippery terrain carrying 12 kg (80% of its body weight) — with *zero* real-world fine-tuning. The privileged state leaves a signature in proprioception, and a supervised module recovers it. [[2212.07740|TERT]] sharpens the terrain axis: a Terrain Transformer learns distinct terrain representations and traverses 9 terrains at 100% on sand and 60% on stairs *where RMA's TCN adaptation fails completely (0% on stairs)* — showing the *architecture* of context-inference matters. [[2403.13358|QUARD-Auto]] scales the skill breadth: an MoE generalist hits 71–90.5% across 99 sub-tasks at only 39.31M active parameters. The first-principles claim: the unobserved context is *recoverable from proprioceptive history*, so robust deployment needs neither vision nor real-world trials — just the right inference architecture.

**First-principles framing.**
- **First principle**: The privileged environment context $z$ (friction, payload, terrain) is not directly observable on hardware, but it deterministically shapes the robot's proprioceptive response — so $z$ leaves a recoverable signature in the recent history $q_{t-H:t}$. A supervised module $\hat z(q_{t-H:t})$ can invert this, making the privileged state inferable without sensing it.
- **Assumption being challenged**: That robust real-world deployment requires exteroception or online real-world fine-tuning. The field reaches for cameras or on-robot adaptation; [[2107.04034|RMA]]'s 12 kg-payload, zero-fine-tuning result on 4 terrain types shows proprioceptive inference *alone* suffices for a wide context range — the vision/fine-tuning requirement is an artifact of not exploiting the proprioceptive signature.
- **The bet**: A proprioceptive context-inference module sustains locomotion under [[2107.04034|RMA]]'s 12 kg payload (80% body weight) and lifts stair traversal to [[2212.07740|TERT]]'s 60% where TCN-style RMA scores 0%, at 100 Hz control / 10 Hz adaptation with zero real-world fine-tuning — robustness from inference architecture, not added sensors or real trials.

**Evidence.**
- [[2107.04034|RMA]] — Privileged-extrinsics base policy + proprioceptive adaptation module (10 Hz); 12 kg payload, sand/mud/rocky/slippery, zero fine-tuning; the proprioceptive-inference anchor.
- [[2212.07740|TERT]] — Terrain Transformer two-stage training; 100% sand / 60% stairs vs RMA 0%, 9 terrains, lower energy; the architecture-matters anchor.
- [[2403.13358|QUARD-Auto]] — MoE generalist quadruped; 71–90.5% across 99 sub-tasks, 39.31M active params, emergent path planning; the skill-breadth anchor.
- [[2107.03996|LocoTransformer]] — Cross-modal Transformer (the exteroceptive alternative); 92% farther real; the vision-augmented counterpoint B1 argues is unnecessary for context-inference.
- [[2403.10506|HumanoidBench]] — High-DoF whole-body benchmark; the difficulty framing for context-inference at scale.

**Concrete research questions.**
1. **Q1 — Proprioceptive inference vs exteroception on context range.** Compare [[2107.04034|RMA]]'s proprioceptive adaptation against an exteroceptive policy ([[2107.03996|LocoTransformer]]-style) across friction/payload ranges — where does proprioception alone suffice, and where is vision genuinely required?
2. **Q2 — Context-inference architecture ablation.** [[2212.07740|TERT]]'s Transformer beats RMA's TCN on stairs (60% vs 0%); ablate the inference backbone — what representational capacity is needed to recover discontinuous terrain context?
3. **Q3 — Adaptation-module frequency vs disturbance bandwidth.** [[2107.04034|RMA]] runs base at 100 Hz / adaptation at 10 Hz; sweep the adaptation frequency against disturbance bandwidth — what update rate tracks fast payload/terrain shifts?
4. **Q4 — Generalist proprioceptive context across 99 skills.** Does [[2403.13358|QUARD-Auto]]'s MoE capacity help *context-inference* breadth (many terrains) the way it helps skill breadth, or is context-inference a separate bottleneck?

**Related research papers.**
- [[2107.04034|RMA]] — Proprioceptive rapid motor adaptation; 12 kg, zero fine-tuning; the anchor.
- [[2212.07740|TERT]] — Terrain Transformer; 100% sand / 60% stairs vs RMA 0%; the architecture anchor.
- [[2403.13358|QUARD-Auto]] — MoE quadruped generalist; 99 sub-tasks; the skill-breadth anchor.
- [[2107.03996|LocoTransformer]] — Cross-modal depth+proprioception fusion; the exteroceptive counterpoint.
- [[2003.01239|Evolutionary Meta-Learning Legged]] — Fast real-world adaptation (Minitaur +100% velocity in 50 rollouts / 150 s); the meta-learning route to context adaptation.
- [[2605.27046|Thermal-Aware Residual]] — Payload + thermal locomotion (650 m + 3 kg); the embodiment-constraint context (cross-list A4).
- [[2403.10506|HumanoidBench]] — Whole-body context-inference difficulty; the framing.
- [[2502.08844|MuJoCo Playground]] — Go1 zero-shot sim; the proprioceptive-training substrate.

**Benchmarks & metrics.**
- [[2107.04034|RMA]] — 12 kg payload (80% body weight) on 4 terrain types, success/time-to-failure/distance vs baselines, zero fine-tuning; the proprioceptive-robustness metric.
- [[2212.07740|TERT]] — 100% sand / 60% stairs vs RMA 0% across 9 terrains; the terrain-context metric.
- [[2403.13358|QUARD-Auto]] — 71–90.5% across 99 sub-tasks at 39.31M active params; the skill-breadth metric.

> [!warning] Risks
> - **Proprioception cannot anticipate geometry** — a step or gap is invisible to proprioception until contact. → Bound B1 to dynamics-context inference (friction/payload); anticipatory geometry is A1's perceptive job — the two are complementary, not competing.
> - **Adaptation-module supervision needs privileged sim** — the inference target requires simulation extrinsics. → Standard for the RMA family; cross-ref [[Sim2Real|Sim2Real]] for the privileged-to-proprioceptive distillation machinery.
> - **TCN-vs-Transformer gap may be task-specific** — TERT's stair win may not generalize. → Q2's backbone ablation tests generality; report per-terrain, not a single average.

### B2 — World-Model Dreaming for Few-Shot Real-World Adaptation

| | |
|---|---|
| **Cluster** | B — Quadruped Locomotion & Real-World Adaptation |
| **Thesis** | Pretraining a world model in simulation and adapting it with a *handful* of real trajectories — rather than the field's million-step on-robot RL or pure domain randomization — has the irreducible truth that a learned dynamics model lets the policy *imagine* the consequences of actions, so each real interaction updates a model that generates thousands of synthetic ones, which breaks the assumption that closing the sim-to-real dynamics gap needs either exhaustive randomization or extensive real rollouts, and I bet a sim-pretrained world model adapts to real quadruped locomotion in [[2604.02911\|DreamTIP]]'s ~5 trajectories (Go2 100% on the 52 cm Climb vs WMP's 10%, the gap that matters; the 16 cm Stair is a 100% tie) and [[2603.15759\|SimDist]]'s 15–30 minutes, with an epistemic-uncertainty penalty ([[2504.16680\|RWM-U]]) bounding model-blind exploitation. |
| **Anchor surveys** | [[2206.14176\|DayDreamer]], [[2504.16680\|RWM-U]], [[2403.10506\|HumanoidBench]] |
| **Key targets** | [[2604.02911\|DreamTIP]] 28.1% avg transfer gain + Go2 100% on 52 cm Climb (vs WMP 10%) and 16 cm Stair (WMP ties 100%), stable adaptation from ~5 real trajectories; [[2206.14176\|DayDreamer]] A1 walks in 1 hr real + recovers from pushes in 10 min; [[2603.15759\|SimDist]] 1.5–2× throughput + 15–30 min real adaptation; [[2504.16680\|RWM-U]] 0.91 normalized reward on ANYmal D (offline sim+real), beats online model-free |

**Why it matters.** Deep RL needs millions of interactions — impractical on hardware. The field's two answers are exhaustive domain randomization (train so broadly that real is in-distribution) or extensive on-robot RL (just collect a lot of real data). Both are inefficient. World-model dreaming offers a third route: learn a dynamics model so the policy can *imagine* action consequences, turning each real interaction into thousands of synthetic ones. [[2206.14176|DayDreamer]] proved the principle — an A1 quadruped learns to walk in *1 hour* of real-world training and recovers from physical pushes in *10 minutes*, via the Dreamer world model in latent space, no simulator. [[2604.02911|DreamTIP]] modernizes it for transfer: a task-invariant Dreamer latent achieves 28.1% average transfer gain and 100% on a 52 cm climb on a real Go2 (vs a WMP baseline's 10%) from as few as *5 real trajectories*. [[2603.15759|SimDist]] pretrains the world model in simulation then adapts with 15–30 minutes of real interaction at 1.5–2× throughput. [[2504.16680|RWM-U]] adds the safety valve: an epistemic-uncertainty penalty steers the policy away from where the model is unreliable, achieving 0.91 normalized reward on ANYmal D from offline sim+real data and *surpassing online model-free baselines*. The non-consensus claim: the sim-to-real dynamics gap closes not by randomizing harder or collecting more real data, but by *dreaming* — a pretrained dynamics model plus tiny real adaptation, with uncertainty bounding the imagination.

**First-principles framing.**
- **First principle**: A learned dynamics model is a *multiplier* on real data — each real transition both updates the model and, through imagination, generates many synthetic transitions for policy optimization. Sample efficiency is therefore governed by model accuracy per real interaction, not by raw real-interaction count; a good model makes 5 trajectories worth thousands.
- **Assumption being challenged**: That closing the sim-to-real dynamics gap requires exhaustive randomization or extensive real rollouts. Domain randomization (the [[2107.04034|RMA]]/[[2408.14472|DWL]] line) and on-robot RL are the field's defaults; [[2604.02911|DreamTIP]]'s 5-trajectory / 100%-vs-10% result and [[2206.14176|DayDreamer]]'s 1-hour walking show a pretrained-then-dreamed model needs *neither* — the gap is a model-adaptation problem, not a data-volume problem.
- **The bet**: A sim-pretrained world model adapts to real quadruped locomotion in [[2604.02911|DreamTIP]]'s ~5 trajectories (100% on a 52 cm climb vs 10% baseline) and [[2603.15759|SimDist]]'s 15–30 minutes, with an epistemic-uncertainty penalty ([[2504.16680|RWM-U]], 0.91 on ANYmal D) bounding model-blind exploitation — dreaming-driven few-shot adaptation, not randomization or extensive real RL.

**Evidence.**
- [[2604.02911|DreamTIP]] — Task-invariant Dreamer latent for transfer; 28.1% avg gain, Go2 100% on 52 cm climb vs WMP 10%, 5 real trajectories; the dreaming-for-transfer anchor.
- [[2206.14176|DayDreamer]] — Dreamer world model on physical robots; A1 walks in 1 hr, recovers from pushes in 10 min, no simulator; the real-world-dreaming progenitor.
- [[2603.15759|SimDist]] — Sim-pretrained world model + rapid real adaptation; 1.5–2× throughput, 15–30 min, quadruped + manipulation; the sim-pretrain anchor.
- [[2504.16680|RWM-U]] — Uncertainty-aware world model + MOPO-PPO penalty; 0.91 normalized reward ANYmal D, beats online model-free; the uncertainty-bounding anchor.
- [[2501.10100|RWM]] — Neural-simulator world model deployed across ANYmal D + G1; zero-shot velocity tracking, beats DreamerV3/SHAC; the cross-embodiment world-model substrate.

**Concrete research questions.**
1. **Q1 — Dreaming vs domain randomization on real-trajectory budget.** Compare [[2604.02911|DreamTIP]]'s 5-trajectory dreaming adaptation against a domain-randomized blind policy ([[2408.14472|DWL]]-style) — at what real-data budget does dreaming overtake randomization, and how does the 100%-vs-10% gap scale with task difficulty?
2. **Q2 — Epistemic-uncertainty penalty calibration.** [[2504.16680|RWM-U]] penalizes reward by epistemic uncertainty; quantify how the penalty coefficient $\beta$ trades off model-blind exploitation against exploration — is there a calibration that reliably matches long-horizon prediction error?
3. **Q3 — Task-invariant latent for transfer.** [[2604.02911|DreamTIP]] learns task-invariant properties; test whether the invariant latent transfers across *terrains* (not just tasks) and whether it composes with B1's proprioceptive context-inference.
4. **Q4 — Cross-embodiment world model.** [[2501.10100|RWM]]/[[2504.16680|RWM-U]] run the same pipeline on ANYmal D + G1; quantify how much of a quadruped-pretrained world model transfers to a humanoid (cross-ref Cluster A) — is the locomotion dynamics model morphology-portable?

**Related research papers.**
- [[2604.02911|DreamTIP]] — Task-invariant Dreamer transfer; 5-traj, 100% vs 10%; the anchor.
- [[2206.14176|DayDreamer]] — Real-world Dreamer; 1-hr walking, 10-min push recovery; the progenitor.
- [[2603.15759|SimDist]] — Sim-pretrained world-model adaptation; 15–30 min; sim-pretrain anchor.
- [[2504.16680|RWM-U]] — Uncertainty-aware MBRL; 0.91 ANYmal D; uncertainty-bounding anchor.
- [[2501.10100|RWM]] — Neural-simulator world model; ANYmal D + G1; cross-embodiment substrate.
- [[2003.01239|Evolutionary Meta-Learning Legged]] — Meta-learned fast adaptation (50 rollouts / 150 s); the model-free fast-adaptation counterpoint.
- [[2502.08844|MuJoCo Playground]] — GPU sim for world-model pretraining data; the pretraining substrate.

**Benchmarks & metrics.**
- [[2604.02911|DreamTIP]] — Go2 100% on 52 cm Climb (vs WMP 10%) and 16 cm Stair (WMP ties 100%), 28.1% avg transfer gain, 5-trajectory adaptation; the dreaming-transfer metric.
- [[2206.14176|DayDreamer]] — A1 walks in 1 hr, push recovery in 10 min; the real-world-sample-efficiency metric.
- [[2504.16680|RWM-U]] — 0.91 normalized reward on ANYmal D (offline sim+real) beating online model-free; the uncertainty-bounded-MBRL metric.

> [!warning] Risks
> - **Model error compounds over horizon** — long imagined rollouts drift. → [[2504.16680|RWM-U]]'s epistemic penalty bounds this; report prediction error vs horizon and cap rollout length where uncertainty spikes.
> - **5-trajectory adaptation may overfit the test terrain** — tiny real data risks narrow adaptation. → Q3 tests cross-terrain transfer; report held-out-terrain SR, not just the adapted terrain.
> - **Dreaming needs a good simulator for pretraining** — garbage-in pretraining poisons the model. → [[2603.15759|SimDist]] stresses diverse large-scale pretraining; cross-ref [[WAM|WAM]] for world-model substrate quality and [[Sim2Real|Sim2Real]] for the sim side.

### B3 — Perceptive Mapless Locomotion-to-Goal & Traversability

| | |
|---|---|
| **Cluster** | B — Quadruped Locomotion & Real-World Adaptation |
| **Thesis** | Reaching a spatial goal by *learned* mapless memory + self-supervised traversability — not a pre-built metric map or a high-level VLN planner — has the irreducible truth that long-range locomotion-to-goal needs a recurrent spatial state that survives hundreds of control steps, a representation an explicit SLAM map handles brittly under unstructured terrain, which breaks the assumption that goal-reaching factors cleanly into map-build → plan → track, and I bet an end-to-end mapless policy with spatial memory lifts long-range success by [[2506.05997\|SRU]]'s 23.5% over LSTM/GRU and transfers zero-shot 100+ m to a real legged-wheel robot, with self-supervised traversability ([[2605.28442\|COTRATE]]) cutting path effort cross-platform. |
| **Anchor surveys** | [[2506.05997\|SRU]], [[2604.26504\|HiPAN]], [[2605.28442\|COTRATE]] |
| **Key targets** | [[2506.05997\|SRU]] 23.5% higher long-range mapless SR vs LSTM/GRU + 29.6% over EMHP / 105.0% over GTRL, zero-shot 100+ m on a real Unitree B2W legged-wheel robot; [[2604.26504\|HiPAN]] 94.7% SR / 83.6 SPL in Complex-2, Go1 onboard depth in cluttered/dead-end/outdoor; [[2605.28442\|COTRATE]] cross-platform traversability (Spot + Husky), ≥2.1–2.5 pp mIoU over baselines |

**Why it matters.** Reaching a spatial goal over long range is the locomotion-to-goal problem — distinct from VLN goal *reasoning* (which the umbrella owns) and from manipulation. The classical pipeline factors it into build-a-map → plan-a-path → track-the-path. But explicit metric maps are brittle in unstructured terrain (drift, dynamic obstacles, no GPS), and the factoring discards the tight coupling between perception and gait. [[2506.05997|SRU]] attacks the memory axis: a Spatially-enhanced Recurrent Unit gives an end-to-end RL navigation policy a spatial state that survives hundreds of steps, lifting long-range mapless success 23.5% over LSTM/GRU (29.6% over EMHP, 105.0% over GTRL) and transferring *zero-shot* 100+ m on a real Unitree B2W legged-wheel robot. [[2604.26504|HiPAN]] attacks the embodiment-aware-traversal axis: hierarchical posture-adaptive navigation reaches 94.7% SR / 83.6 SPL in the hardest "Complex-2" environment and validates on a Go1 in cluttered, dead-end, and outdoor scenes from onboard depth alone. [[2605.28442|COTRATE]] supplies the substrate: self-supervised online traversability that transfers across platforms (Spot, Husky) and cuts path effort. The non-consensus claim: long-range goal-reaching is better solved as an *end-to-end mapless policy with learned spatial memory + self-supervised traversability* than as a brittle map-build → plan → track stack — the perception-gait coupling is the value, and the map is a lossy intermediate. (This direction absorbs the dropped wheeled-mobility cluster; goal *reasoning* / language instruction is cross-referenced to [[Embodied-AI|Embodied-AI]]'s VLN direction.)

**First-principles framing.**
- **First principle**: Long-range locomotion-to-goal requires a spatial state that persists across hundreds of control steps (where have I been, where is the goal relative to me) *and* a coupling between that state and the gait that traverses the terrain. An explicit metric map is one lossy realization of this state — brittle under drift and dynamics — and the map-build → plan → track factoring severs the perception-gait coupling the policy could exploit.
- **Assumption being challenged**: That goal-reaching factors cleanly into map-build → plan → track. Classical navigation and even modular learned stacks assume this; [[2506.05997|SRU]]'s 23.5% mapless gain over recurrent baselines and zero-shot 100+ m transfer show an end-to-end policy with *learned* spatial memory beats the factored pipeline on unstructured terrain, where the map is the weakest link.
- **The bet**: An end-to-end mapless policy with spatial memory lifts long-range success by [[2506.05997|SRU]]'s 23.5% over LSTM/GRU and transfers zero-shot 100+ m to a real legged-wheel robot, with self-supervised traversability ([[2605.28442|COTRATE]]) cutting path effort cross-platform and [[2604.26504|HiPAN]]-class 94.7% SR in cluttered/dead-end environments — mapless learned memory, not a built map.

**Evidence.**
- [[2506.05997|SRU]] — Spatially-enhanced recurrent memory for end-to-end RL mapless navigation; 23.5% over LSTM/GRU, zero-shot 100+ m on Unitree B2W legged-wheel; the mapless-memory anchor.
- [[2604.26504|HiPAN]] — Hierarchical posture-adaptive navigation; 94.7% SR / 83.6 SPL Complex-2, Go1 onboard depth, cluttered/dead-end/outdoor; the embodiment-aware-traversal anchor.
- [[2605.28442|COTRATE]] — Self-supervised online robot-agnostic traversability; cross-platform (Spot + Husky), ≥2.1–2.5 pp mIoU, cuts path effort; the traversability substrate.
- [[2107.03996|LocoTransformer]] — End-to-end vision-guided locomotion to goal; 92% farther, attends to obstacles + distant goal; the perception-to-goal precedent.
- [[2403.13358|QUARD-Auto]] — Emergent dynamic adaptive path planning in unseen scenarios; the emergent-planning evidence within a quadruped generalist.

**Concrete research questions.**
1. **Q1 — Learned spatial memory vs explicit map on unstructured terrain.** Compare [[2506.05997|SRU]]'s mapless memory against a SLAM-map + planner stack on long-range unstructured courses — does the 23.5% mapless gain widen as terrain becomes less map-friendly (drift, dynamics)?
2. **Q2 — Recurrent-unit capacity vs horizon.** [[2506.05997|SRU]] beats LSTM/GRU; ablate spatial-memory capacity against goal distance — what memory structure is needed to retain spatial state over hundreds of steps?
3. **Q3 — Posture-adaptive traversal in confined geometry.** [[2604.26504|HiPAN]] adapts posture for dead-ends; test whether posture-conditioned locomotion (crouch, squeeze) extends the traversable space beyond fixed-posture navigation, and by how much SPL.
4. **Q4 — Self-supervised traversability as the perception layer.** Plug [[2605.28442|COTRATE]]'s cross-platform traversability into the mapless policy — does robot-agnostic traversability improve cross-embodiment goal-reaching over platform-specific perception?

**Related research papers.**
- [[2506.05997|SRU]] — Spatially-enhanced recurrent mapless navigation; 23.5% over LSTM/GRU, 100+ m real; the anchor.
- [[2604.26504|HiPAN]] — Hierarchical posture-adaptive navigation; 94.7% SR / 83.6 SPL; the traversal anchor.
- [[2605.28442|COTRATE]] — Self-supervised cross-platform traversability; the perception substrate.
- [[2107.03996|LocoTransformer]] — Vision-guided locomotion to goal; the perception-to-goal precedent.
- [[2403.13358|QUARD-Auto]] — Emergent adaptive path planning; emergent-planning evidence.
- [[2107.04034|RMA]] — Proprioceptive robustness underneath goal-reaching; the locomotion floor (feeds B1).
- [[2604.24916|asRoBallet]] — Precise base velocity tracking (0.05 m/s MAE) + station-keeping (3–5 cm) on a mobile platform; the low-level mobility-control precedent.
- [[2604.02911|DreamTIP]] — World-model the mapless policy can plan through; the dreaming substrate (feeds B2).

**Benchmarks & metrics.**
- [[2506.05997|SRU]] — 23.5% over LSTM/GRU, 29.6% over EMHP, 105.0% over GTRL, zero-shot 100+ m real; the mapless-navigation metric.
- [[2604.26504|HiPAN]] — 94.7% SR / 83.6 SPL in Complex-2, Go1 real in cluttered/dead-end/outdoor; the posture-adaptive-traversal metric.
- [[2605.28442|COTRATE]] — Cross-platform mIoU (≥2.1–2.5 pp over baselines) + path-effort reduction (Spot ~0.7, Husky ~2.1); the traversability metric.

> [!warning] Risks
> - **Mapless policies can loop or get stuck** — without a map, the policy may revisit dead-ends. → [[2604.26504|HiPAN]]'s SPL (path efficiency) catches this; report SPL alongside SR, not SR alone.
> - **Overlap with the umbrella's VLN direction** — high-level goal *reasoning* is VLN territory. → This direction is scoped to low-level mapless *control + traversability*; language-instruction goal-reasoning is cross-referenced to [[Embodied-AI|Embodied-AI]], not duplicated.
> - **Traversability self-supervision needs experience** — COTRATE learns from robot rollouts. → It transfers cross-platform (Spot→Husky) zero-shot in places; report where cross-platform transfer holds vs needs continual learning.

---

## Cross-Cutting Themes

> [!tip] The Privileged-State Gap Is the Locomotion Bottleneck — Inference, Denoising, and Dreaming Are the Three Answers
> A1, B1, and B2 all confront the same irreducible problem the surveys name under different vocabulary: the policy must act without the privileged physical state (terrain $\mu/h$, payload, contact, model error) that simulation provides. They answer at three points: B1 *infers* the context from proprioceptive history ([[2107.04034|RMA]]'s 10 Hz adaptation module, 12 kg payload), A1 *perceives* the anticipatory geometry exteroception exposes ([[2604.17335|G1 WBC-Gen+Track]] 0.962 vs 0.230 box-climb), and B2 *dreams* — a world model imagines consequences so 5 real trajectories suffice ([[2604.02911|DreamTIP]] 100% vs 10%). [[2408.14472|DWL]]'s denoising world model and [[2504.16680|RWM-U]]'s epistemic-uncertainty penalty are the shared mechanism — recover or bound the unobserved state, don't pretend it's observed.

> [!tip] Real-World Adaptation in Minutes, Not Millions — World-Model Pretraining Displaces Both Randomization and On-Robot RL
> A5 and B2 converge on the finding that the lever for deployable locomotion is *sample efficiency through the right substrate*, not more compute or more real data: A5 shows off-policy/flow RL beats PPO on wall-clock ([[2505.22642|FastTD3]] <3 hrs, [[2512.01996|Humanoid Loco 15min]] 15 min), and B2 shows world-model pretraining + tiny real adaptation ([[2206.14176|DayDreamer]] 1 hr, [[2603.15759|SimDist]] 15–30 min) displaces both exhaustive domain randomization and extensive on-robot RL. The shared Hinton-tenet move: the brain learns from few interactions because it has a model — favor the learning mechanism (off-policy reuse, world-model imagination) that extracts more from each step over the one that discards rollouts or randomizes blindly.

> [!tip] The Imitation Target, Not the Imitation Data, Is the Lever for Dynamic Skills
> A1 and A2 share the discipline of "make the reference feasible, don't collect more demonstrations" but apply it at *opposite ends of the timeline*, and the split is the point: **A2 corrects a fixed clip offline** — a one-time projection of a pre-recorded mocap sequence onto the dynamically-feasible manifold *before* any rollout ([[2506.12851|KungfuBot]] 53.25 mm vs >233 mm, [[2605.06593|ReActor]] 97.45% downstream RL), whereas **A1 synthesizes a fresh reference online against the terrain perceived at runtime** — a new reference every control window, conditioned on the live height-scan, filtered by an RL tracker ([[2604.17335|G1 WBC-Gen+Track]] 0.962 box-climb). A2 answers "is *this given motion* trackable?"; A1 answers "what motion does *this terrain ahead* demand?" — feasibility-of-a-clip vs feasibility-against-geometry. [[2605.10063|EFGCL]]'s force-guided curriculum even *expands* A2's feasible manifold to reach backflips. The non-consensus lever both share: agile-skill quality is bounded by reference feasibility, not demonstration quantity — but the *when* (offline clip-fix vs online terrain-gen) makes them complementary directions, not two phrasings of one idea.

> [!tip] Deployability Is Bounded by Embodiment Costs the Task Reward Ignores
> A3, A4, and B1 share the recognition that a sim-trained policy meets real limits the standard task reward omits: A4 makes GRF, acoustic, and thermal cost first-class predicted-and-regulated quantities ([[2604.23702|QuietWalk]] R²≈0.99, 7.17 dBA; [[2605.27046|Thermal-Aware Residual]] 70%→<10% overheating), A3 treats fall-recovery as the non-periodic embodiment-stress boundary case ([[2502.12152|HUMANUP]] lower motor temperature, ~6 s recovery), and B1 sustains locomotion under real payload the sim ignores ([[2107.04034|RMA]] 12 kg). The convergent insight: task success is necessary but not sufficient — a gait that overheats, deafens, or cannot recover from a fall is undeployable regardless of its tracking reward.

> [!tip] The Locomotion Control Object Is More Morphology-Portable Than the Manipulation Grasp Object
> B2, A5, and A1 rest on a representational bet that distinguishes locomotion from manipulation: the locomotion control object (phase-clocked gait + velocity-tracking) transfers across embodiments more readily than the manipulation grasp object does. B2's [[2501.10100|RWM]]/[[2504.16680|RWM-U]] deploy the *same* world-model + MBRL pipeline across ANYmal D (quadruped) and Unitree G1 (humanoid); A5's off-policy/flow methods ([[2505.22642|FastTD3]], [[2602.02481|FPO++]]) span quadruped and humanoid locomotion unchanged; A1's perception-fusion precedent ([[2107.03996|LocoTransformer]], quadruped) transfers to bipedal terrain. This is the locomotion counterpart to the morphology-invariance direction in [[Embodied-AI|Embodied-AI]] — but where manipulation needs a function-aligned action space to bridge hands, locomotion's gait structure is *already* a low-dimensional cross-morphology invariant.

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

- [[../Embodied-AI/02_Dataset-Benchmark-Environment#1. Cross-Embodiment Scale Datasets|02_Dataset-Benchmark-Environment §1]] — Cross-embodiment scale datasets (the locomotion-portability substrate for B2 + Cluster A)
- [[../Embodied-AI/02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02_Dataset-Benchmark-Environment §8]] — Humanoid evaluation suites (HumanoidBench and whole-body benchmarks feeding Cluster A)
- [[../Embodied-AI/02_Dataset-Benchmark-Environment#12. Sim-to-Real Transfer Evaluation|02_Dataset-Benchmark-Environment §12]] — Sim-to-real transfer evaluation (the deployment gate for every direction here)
- [[../Embodied-AI/11_Sim-to-Real-Transfer#3. Policy-Side: Robustness & Domain Randomization|11_Sim-to-Real-Transfer §3]] — Policy-side robustness + domain randomization (the proprioceptive-robustness machinery feeding B1)
- [[../Embodied-AI/11_Sim-to-Real-Transfer#4. Real2Sim2Real Loops & Digital Twins|11_Sim-to-Real-Transfer §4]] — Real2Sim2Real loops (the world-model adaptation machinery feeding B2)
- [[../Embodied-AI/11_Sim-to-Real-Transfer|11_Sim-to-Real-Transfer]] — Sim-to-real design space; the transfer deep-dive underpinning Clusters A + B
- [[../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Robotics & embodied-AI topic overview
- [[Manipulation|Manipulation]] — Sibling Manipulation subsystem (arms + hands on objects); this doc's legs/mobility complement its grasping/dexterity — together they are the humanoid's two embodiment halves.
- [[Whole-Body|Whole-Body]] — Sibling Whole-Body subsystem (forthcoming); owns the loco-manipulation coupling (how the legs stabilize and extend the manipulation workspace) and mobile manipulation (arm + base) that both this doc and the Manipulation doc exclude.
- [[Embodied-AI|Embodied-AI]] — Umbrella embodied-AI directions; its VLN direction owns goal *reasoning* / language-instructed navigation that B3 cross-references for the high-level layer, and its morphology-invariance direction is the cross-morphology counterpart to this doc's locomotion-portability theme (Cluster B).
- [[WAM|WAM]] — World-action-model substrate; B2's dreaming-for-adaptation and the world-model quality it needs borrow the WAM imagination and calibration threads.
- [[Sim2Real|Sim2Real]] — Sim-to-real / real-to-sim transfer; owns the privileged-to-proprioceptive distillation (B1), the world-model real-adaptation machinery (B2), and the domain-randomization vs real-residual story underneath every direction.

> [!example] Humanoid reading path
> For a humanoid robot, this doc's **Bipedal cluster (A)** is the humanoid's legs — whole-body balance, perceptive terrain traversal (A1), dynamic agile skills (A2), fall-recovery (A3), embodiment-grounded gait costs (A4), and the off-policy/flow training substrate (A5) are what the humanoid's lower body does. For the humanoid's **upper-body manipulation** — two-arm coordination and multi-fingered in-hand control — read the [[Manipulation|Manipulation]] doc's **Bimanual** and **Dexterous** clusters. For the **loco-manipulation coupling** — how the legs stabilize and extend the arms' workspace, whole-body balance during reaching — read the [[Whole-Body|Whole-Body]] doc. Read A here for the legs; read the sibling docs for the arms and the coupling.
