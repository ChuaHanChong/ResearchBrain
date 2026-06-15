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
| **Thesis** | Generate the gait reference *online* against the terrain seen at runtime *and* learn where to look — fuse online reference synthesis with an active-gaze module in one perceptive policy, not a fixed gait library nor a full passive height-scan. The reason it must work: feasible foot-placement for a 75 cm box depends on the *perceived* local geometry ahead of the swing foot, but a fixed-horizon scan of the whole terrain wastes capacity where it doesn't matter. The field now agrees perception beats blindness on obstacle terrain; what it has not settled is *what to look at, over what horizon*. The bet is in First-principles below. |
| **Anchor papers** | [[2403.10506\|HumanoidBench]] (benchmark), [[2603.20147\|AGILE]] (benchmark), [[2408.14472\|DWL]] (method), [[2604.17335\|G1 WBC-Gen+Track]] (method), [[2602.15827\|PHP]] (method), [[2606.05880\|TAGA]] (method) |
| **Key targets** | [[2604.17335\|G1 WBC-Gen+Track]] 80 cm box-climb SR 0.962 (Tracker+Gen) vs 0.230 (Tracker-Only), 75 cm box + stairs + hurdles real; [[2606.05880\|TAGA]] 120 cm gap on a real G1 (+50% over prior perceptive max) at 65.2% lower training cost; [[2602.15827\|PHP]] 1.25 m wall (96% height) in 3.63 s + cat-vault 3.41 m/s + ~0.5 m perturbation recovery; [[2408.14472\|DWL]] zero-shot snowy-incline/stairs from proprioception alone |

**Why it matters.**
- **The gap**: a humanoid clearing a 75 cm box must commit its swing trajectory *before* the foot touches, so the policy needs the local geometry ahead of it — but the cheap perceptive answer is a fixed full height-scan over a fixed horizon, which neither prioritizes the sparse footholds that matter nor adapts its reference to disturbance, and [[2403.10506|HumanoidBench]] sets the wall that flat RL "generally fails" on whole-body locomotion.
- **Today's answers**: the perceptive-beats-blind battle is now settled — [[2603.18979|PRIOR-Loco]] hits 100% traversal on Pyramid Stairs / Inverted Stairs / Boxes with a parametric gait generator + self-supervised depth→height-map terrain reconstruction, [[2604.17335|G1 WBC-Gen+Track]] closes the 0.230→0.962 box-climb gap with an online diffusion-generated reference, and [[2601.07701|Deep WB Parkour]] reaches 100% over a 1.2 m OOD start range by folding depth into a whole-body tracking policy. All anticipate; what none does is decide *where* to look — they pay for a full terrain scan over a fixed horizon.
- **The opening**: [[2606.05880|TAGA]] shows the perceptive ceiling is still rising on the *attention* axis — an *emergent* active-gaze module that learns where to look matches full-height-scan performance at 65.2% lower training cost and clears a 120 cm gap (+50% over the prior perceptive max). The unclaimed cell is the combination: online reference *generation* fused with *learned gaze*, which no perceptive parkour policy has yet built.

**First-principles framing.**
- **First principle**: On obstacle terrain, feasible foot-placement depends on the *local geometry ahead of the swing foot*, but that geometry is *sparse* — a few load-bearing footholds carry the placement decision, while most of the height-scan is irrelevant. A fixed full scan over a fixed horizon spends equal capacity everywhere and equal staleness under disturbance. [[2606.05880|TAGA]] demonstrates the first half: a learned gaze matches the full scan at 65.2% lower cost, proving most of the scan is wasted; [[2604.17335|G1 WBC-Gen+Track]]'s 0.962 vs 0.230 ablation proves the anticipatory half — the signal must be perceived, not felt.
- **Assumption being challenged**: That a fixed full height-scan over a fixed receding horizon is the right perceptive interface. The consensus perceptive policies — [[2603.18979|PRIOR-Loco]] (100% traversal via reconstructed terrain), [[2604.17335|G1 WBC-Gen+Track]] (0.5 s fixed generation horizon), [[2601.07701|Deep WB Parkour]] (whole-body depth tracking) — all consume the whole scan over a fixed horizon and have *won* against blind trackers; that battle is over. [[2606.05880|TAGA]] bets the opposite about the *interface* — that learned where-to-look + an adapted horizon beats the fixed full scan — and proves the attention half cheap.
- **The bet**: A policy that *fuses* online reference generation ([[2604.17335|G1 WBC-Gen+Track]]-style) with learned active gaze ([[2606.05880|TAGA]]-style) beats both gaze-alone and generation-alone, and concentrates its win where the height-scan is sparse: on stepping-stone / wide-gap tasks (≥70 cm spacing) the fused policy holds ≥0.95 SR at ≤40% of the full-scan compute, while on dense rough terrain it ties full-scan within 2 pp; and there is an *interior-optimal reference horizon* — SR is non-monotone in horizon under ~0.5 m perturbation ([[2602.15827|PHP]]-class). Falsifiable: if generation-alone (G1 WBC-Gen+Track at full scan) matches the fused gaze+generation policy on sparse-foothold SR-at-fixed-compute, learned gaze adds nothing over a fixed scan; if SR rises monotonically with horizon, there is no staleness penalty.

**Related research papers.** One comparison table — the axis is *what perceptual signal conditions the gait and over what horizon* (blind / height-scan / depth / active-gaze / motion-matched), with what each leaves missing:

| System | Perceptual signal → gait | Reference horizon | Key result | What's missing |
|---|---|---|---|---|
| [[2604.17335\|G1 WBC-Gen+Track]] | terrain height-scan → diffusion-generated reference, RL-tracked | online, 0.5 s receding | 0.962 vs 0.230 (80 cm box), real box/stairs/hurdles | fixed 0.5 s horizon, no learned where-to-look — feeds the active-gaze bet |
| [[2606.05880\|TAGA]] | egocentric depth + height-scan + proprioception, **emergent active gaze** | online | 120 cm gap on real G1 (+50%), 65.2% cheaper than full scan | gaze is emergent but the reference is policy-implicit, not a generated clip — the gaze half the fused bet needs |
| [[2603.18979\|PRIOR-Loco]] | self-supervised depth→height-map reconstruction + **parametric** gait generator | online (parametric reference) | **100%** traversal on Pyramid/Inverted Stairs + Boxes (sim), 3× training speedup, 1024 envs on one 4090 | the consensus near-miss — its reference is a *parametric* gait prior, not synthesized from the live scan, and the full scan is passive (no learned gaze) |
| [[2601.07701\|Deep WB Parkour]] | exteroceptive depth folded into whole-body motion *tracking* | online (full scan) | **100%** within a 1.2 m × 1.2 m OOD start range on real G1, robust to unseen distractors | tracks retargeted parkour clips over the full scan; no online reference *generation* and no where-to-look — perception won, attention unaddressed |
| [[2601.07718\|Hiking-in-the-Wild]] | single-stage depth→action, edge-aware foothold penalization | reactive (full scan) | **2.5 m/s** max run, 100% on box/ramp/platform/stair-up/gap, real G1 zero-shot | depth-reactive without a generated reference or active gaze — the full-scan reactive baseline the fused bet must beat at lower compute |
| [[2512.07464\|Gait]] | 50 Hz under-base depth height-map (self-occlusion-filling) + **scalar gait-frequency** output | online (full scan) | zero-shot stair traversal (fwd/back/side) + 46 cm gap on real Limx Oli | adapts step *timing* to terrain over a full scan, but no foothold-level generated reference and no gaze — timing-adaptive, not attention-adaptive |
| [[2606.05873\|LadderMan]] | onboard depth (VFM stereo + rung-focused masking) → motion-tracked climb | reactive (per-rung) | >95% sim SR vs 49% tracking baseline, 3.4 s/rung real G1, 9/10 vs 0–3/10 ablation | vertical-mobility extreme (ladder), but a single reference motion distilled — no terrain-conditioned *generation* like the box/stair row above |
| [[2602.15827\|PHP]] | onboard depth → motion-matched skill chain | online (chained skills) | 1.25 m wall (96%) in 3.63 s, cat-vault 3.41 m/s, ~0.5 m perturbation | skill graph is fixed/pre-composed — cannot synthesize a reference for an unseen obstacle |
| [[2408.14472\|DWL]] | none (proprioception, denoised) | reactive | zero-shot snow/stairs, robust to pushes + motor failure | blind — cannot anticipate a box; the robustness floor to retain, not the ceiling |
| [[2606.04718\|CoRe-MoE]] | terrain → contrastive-reweighted MoE gait selection | reactive (gait switch) | 99.13% flat SR, walk↔run zero-shot to 2.5 m/s real G1 | selects among gaits, doesn't generate a foot-placement reference for vertical terrain |
| [[2107.03996\|LocoTransformer]] | depth + proprioception fusion (quadruped) | reactive | 92% farther real, 290.5–663% fewer collisions sim | perception-fusion precedent, but obstacle *avoidance*, not vertical traversal |
| [[2503.10626\|NIL]] | video-diffusion reference (no real demos) | offline-generated | matches mocap-trained humanoid + quadruped locomotion | generates references but not *conditioned on perceived terrain* at runtime |
| [[2403.10506\|HumanoidBench]] | benchmark (12 locomotion tasks, 151D proprio) | — | flat RL fails; the exploration-wall framing | a difficulty suite, not a perceptive method |
| [[2603.20147\|AGILE]] | height-controlled locomotion in a deployment workflow | workflow | velocity-tracking + height-controlled + stand-up across 5 G1/T1 skills | standardizes deployment, leaves the perceptive-reference formulation open |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (fused gaze+generation beats either alone, with its win concentrated where the height-scan is sparse and at an interior-optimal horizon).
1. **H1 — Gaze + generation beats either alone on sparse-foothold tasks at fixed compute.**
   - *Prediction*: a policy fusing [[2604.17335|G1 WBC-Gen+Track]]'s online generation with [[2606.05880|TAGA]]'s learned gaze holds ≥0.95 SR on ≥70 cm stepping-stones at ≤40% of the full-scan compute, beating both generation-alone (full-scan [[2603.18979|PRIOR-Loco]]/G1 WBC-Gen+Track) and gaze-alone (TAGA without a generated reference) — the unclaimed combination, not the settled perceptive-vs-blind gap.
   - *Test*: four-arm comparison — blind / gaze-alone / generation-alone / gaze+generation — at matched compute on the [[2502.10363|BeamDojo]] sparse-foothold suite (stepping-stones/beams/gaps; BeamDojo itself hits 91.67% SR on hard Stepping Stones, 4/5 Stepping Stones + 5/5 Gaps real G1, 7.79% foothold error), reporting SR and FLOPs per stratum.
   - *Row*: G1 WBC-Gen+Track (generation) + TAGA (gaze) vs PRIOR-Loco (full-scan generation).
   - *Falsifier*: generation-alone at full scan matches the fused policy on sparse-foothold SR-at-fixed-compute → learned gaze adds nothing over a fixed scan.
2. **H2 — There is an optimal reference horizon under perturbation.**
   - *Prediction*: sweeping [[2604.17335|G1 WBC-Gen+Track]]'s 0.5 s generation horizon against [[2602.15827|PHP]]'s ~0.5 m perturbation, anticipation improves with horizon up to a point, then stale references hurt under disturbance — a non-monotone curve with an interior optimum.
   - *Test*: vary horizon length, measure SR under fixed perturbation magnitude.
   - *Row*: G1 WBC-Gen+Track (0.5 s receding) / PHP (chained).
   - *Falsifier*: SR rises monotonically with horizon → no staleness penalty, longer is always better.
3. **H3 — Active gaze matches full perception more cheaply as obstacles sparsify.**
   - *Prediction*: [[2606.05880|TAGA]]'s emergent active gaze closes the most cost gap (vs full height-scan) precisely on tasks needing *distant* foothold planning (sparse stepping stones, 70 cm spacing), and ties full-scan on dense terrain — the 65.2%-cheaper win concentrates where coverage matters.
   - *Test*: stratify by foothold sparsity / terrain difficulty on the [[2504.09997|GenTe]] benchmark (VLM-generated geometric + physical terrains, difficulty-graded); report gaze-vs-full-scan cost and SR per stratum.
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
| **Thesis** | Project a *fixed, pre-recorded mocap clip* onto the robot's dynamically-feasible manifold *offline, before* imitation, and *reject* what stays untrackable — a one-time fix plus an explicit accept/reject gate, distinct from A1's per-step generation against live terrain. The reason it must work: the tracking objective is ill-posed when the reference breaks the robot's torque/contact/balance limits, so the policy chases a target it can never reach. Feasibility-projection at scale is now the norm; what is unsettled is whether *rejection* and *adaptive tolerance* on extreme agile-bipedal skills beat simply projecting-then-tracking everything. The bet is in First-principles below. |
| **Anchor papers** | [[2403.10506\|HumanoidBench]] (benchmark), [[2603.20147\|AGILE]] (benchmark), [[2602.13656\|KungFuAthlete]] (benchmark), [[2506.12851\|KungfuBot]] (method), [[2605.06593\|ReActor]] (method), [[2605.10063\|EFGCL]] (method), [[2511.09484\|SPIDER]] (method), [[2510.14454\|Adaptive Motion Tracking]] (method) |
| **Key targets** | [[2506.12851\|KungfuBot]] 53.25 mm global mean body-position error (easy) vs OmniH2O/ExBody2 >233 mm, untrackable-motion rejection (max 54% episode-length ratio); [[2605.06593\|ReActor]] 0.00% penetration + 0.17 cm/s foot-slide + 97.45% (G1) / 95.07% (Lima) downstream RL (+15.22 pp); [[2511.09484\|SPIDER]] 2.4 M feasible frames / 9 embodiments at 100% task SR (the projection-at-scale bar); [[2605.10063\|EFGCL]] backflip/lateral-flip unlearnable by PPO + 2× faster jump; [[2602.13656\|KungFuAthlete]] the missing extreme-skill corpus — Side Flip/Air Spin/Backflip dataset with Jump-subset joint velocity 0.02384 / body angular velocity 0.18017 (above LAFAN1/AMASS), tracking + fall-recovery protocol, 100% (6/6) single-leg standing vs 0% tracking-only baseline |

**Why it matters.**
- **The gap**: a human backflip breaks the robot's torque limits, contact timing, and balance margins, so a policy asked to imitate raw mocap optimizes toward a target it physically cannot reach — yet the reflexive recipe for a new agile skill is "imitate more human motion."
- **Today's answers**: feasibility-projection is now a mature toolkit run *at scale* — [[2511.09484|SPIDER]] projects 2.4 M frames across 9 embodiments by constrained optimization (100% task SR, +18% from virtual contact guidance), [[2409.20514|Opt2Skill]] generates torque- and contact-force-feasible references by trajectory optimization (2.0 cm hand / 5.23 cm foot tracking), and [[2603.09956|Kinodynamic Retargeting]] recovers heel-toe contact and GRF magnitudes — so projection-onto-$\mathcal F$ and data-scale are *complements*, not opposites. What none of them does is *reject* the residue that stays untrackable on extreme agile-bipedal skills, or schedule tracking tolerance to learn what a fixed tolerance cannot.
- **The opening**: [[2506.12851|KungfuBot]]'s rejection statistic is the legible mechanism missing from the scaled pipelines — accepted motions yield high episode-length ratios while rejected ones collapse (max 54%) — it hits 53.25 mm where deployable baselines (OmniH2O, ExBody2) exceed 233 mm; [[2510.14454|Adaptive Motion Tracking]] confirms the tolerance half (adaptive phase/tracking adapters beat fixed-tolerance baselines on 7 agile tasks), and [[2605.10063|EFGCL]] shows feasibility is not a hard ceiling — a force-guided curriculum *grows* the manifold to reach backflips a PPO baseline cannot learn at all.

**First-principles framing.**
- **First principle**: Asking a policy to track a reference only makes sense if that reference lies on what the robot can physically do — its torque, contact-timing, and balance limits. Raw human mocap does not, so the first operation is the projection $\xi \mapsto \Pi_{\mathcal F}(\xi)$ onto the dynamically-feasible manifold; only then is the imitation loss well-posed. This is prior to any question of how much data you have. [[2506.12851|KungfuBot]] demonstrates it: *filtering* untrackable motions (not adding data) delivers the 233→53 mm cut.
- **Assumption being challenged**: *Not* that feasibility beats scale — [[2511.09484|SPIDER]] (2.4 M frames, 9 embodiments) and [[2509.15443|Implicit Kinodynamic Retargeting]] (5000 fps, dynamics-aware fine-tuning) prove projection scales, so they are complements. The challenged assumption is narrower: that *projecting-then-tracking everything* is enough. SPIDER, Opt2Skill, and KDMR project and track; none exposes a *rejection* gate or an *adaptive tolerance* on the residue that stays untrackable. [[2506.12851|KungfuBot]]'s 233→53 mm from rejection and [[2510.14454|Adaptive Motion Tracking]]'s adaptive-tolerance win bet the opposite — that an explicit accept/reject decision plus a tolerance schedule is the lever on extreme bipedal skills, beyond what projecting-then-tracking at scale delivers.
- **The bet**: On extreme agile-bipedal skills (flips, martial-arts), KungfuBot-style *rejection* + an *adaptive tracking tolerance* ([[2510.14454|Adaptive Motion Tracking]]-style) beats a scaled projection-then-track pipeline ([[2511.09484|SPIDER]]/[[2409.20514|Opt2Skill]]-style) that tracks every projected clip — cutting tracking error to [[2506.12851|KungfuBot]]'s 53.25 mm (vs >233 mm OmniH2O/ExBody2) and lifting downstream RL to [[2605.06593|ReActor]]'s 97.45% (G1) at zero penetration, with the gain concentrated on the high-rejection (>30% episode-collapse) tail where a project-everything pipeline silently chases infeasible targets. Falsifiable: if a scaled projection-then-track pipeline on the same skill set matches rejection + adaptive-tolerance at equal compute on the high-rejection tail, the accept/reject gate buys nothing scale-plus-projection cannot.

**Related research papers.** One comparison table — the axis is *how the reference is made feasible* (filter / retarget / curriculum-expand / generate / data-scale), with what each leaves missing:

| System | Feasibility operation | When applied | Key result | What's missing |
|---|---|---|---|---|
| [[2506.12851\|KungfuBot]] | filter untrackable mocap + adaptive tracking factor | offline, per-clip | 53.25 mm vs >233 mm OmniH2O/ExBody2; max 54% rejection ratio | discards expressive-but-infeasible clips rather than expanding feasibility |
| [[2605.06593\|ReActor]] | RL physics-aware retargeting (bilevel) | offline, per-clip | 0.00% penetration, 0.17 cm/s slide, 97.45% (G1) downstream RL (+15.22 pp) | corrects penetration but doesn't reject fundamentally untrackable dynamics |
| [[2605.10063\|EFGCL]] | external-force curriculum *expands* the feasible set | during training | backflip/lateral-flip unlearnable by PPO, 2× faster jump | grows feasibility for one skill at a time, no reusable manifold |
| [[2606.03476\|Human2Humanoid]] | unsupervised cross-morphology retarget + EE-consistency loss | offline, per-clip | 88.5% SR, 0.05 cm penetration, 4.7% foot-slide | retargets across bodies but no adaptive tracking-tolerance schedule |
| [[2603.22201\|NMR]] | transformer retargeting filters jitter/self-collision | offline, per-clip | zero joint jumps, 54% fewer self-collisions (0.87% of frames) | smooths motion, no downstream-RL trainability metric |
| [[2606.03536\|Bionic Whole-Body Control]] | physics-regularized latent-diffusion → executable reference | offline (generate) | 96.0% real-G1 SR, 0.004722 m/frame foot-slide | feasibility for *style transfer*, not the full agile-skill range |
| [[2604.00202\|DreamControl-v2]] | guided diffusion trained *directly in G1 motion space* (not human) + error-heuristic filtering | offline (generate-in-manifold) | 68% valid-trajectory rate vs 8% inference-time prompting, FID 0.265, 0.925 SR (vs 0.101 zero-shot), 8 real G1 skills | generates feasible refs but for loco-manipulation skills, no adaptive tracking-tolerance like KungfuBot |
| [[2606.10340\|OMG]] | omni-modal diffusion → G1 trajectories, **simulation-in-the-loop dynamic-feasibility filtering** | offline (generate + sim-filter) | 0.00% audio-to-motion fall rate, FID 6.03 text-to-motion, 51.7 ms sampling, 1%-data finetune parity | filters for feasibility at generation time, but no *rejection* statistic exposing which inputs are untrackable |
| [[2604.11251\|CLAW]] | compose parameterized primitives **inside MuJoCo physics** → feasible-by-construction reference | offline (generate-in-physics) | directly G1-compatible (no retarget), 8 annotation styles, walk→squat→crawl stitched | feasible by construction but only over the primitive library — cannot reach dynamic flips outside it (where EFGCL's curriculum is needed) |
| [[2606.01851\|PHASOR]] | phase-anchored universal action representation | representation | 1.62 mm MPJPE, 90.3% R@1 cross-embodiment retrieval | structures the imitation target by phase, doesn't filter infeasibility |
| [[2511.09484\|SPIDER]] | constrained-optimization projection onto $\mathcal F$ + virtual contact guidance | offline, **at scale** (2.4 M frames, 9 embodiments) | 100% task SR (manip), +18% from contact guidance, 1.5–2.5 fps vs RL's 0.05–0.1 | the scale counterpoint to feasibility-first — projects-then-tracks everything, *no rejection* gate or adaptive tolerance on the untrackable residue |
| [[2409.20514\|Opt2Skill]] | whole-body trajectory optimization (torque + contact-force references) | offline, per-clip | 2.0 cm hand / 5.23 cm foot tracking, real Digit loco-manip | generates feasible-by-construction references, but tracks all of them — no accept/reject on extreme bipedal flips |
| [[2603.09956\|Kinodynamic Retargeting]] | multi-contact TO recovering heel-toe contact + rescaled GRF | offline, per-clip | eliminates foot-float/penetration, faster downstream-IL convergence | corrects contact/GRF feasibility, but no rejection statistic and no adaptive tolerance schedule |
| [[2410.01968\|Bi-Level Motion Imitation]] | alternating policy ↔ motion-generator (self-consistent auto-encoder) | during training | acquires kick/jump where baselines fail, sparser structured latent | *adjusts* the reference toward feasibility but has no explicit accept/reject of the untrackable |
| [[2510.14454\|Adaptive Motion Tracking]] | adaptive phase + tracking adapters from a single reference | during training | beats fixed-tolerance baselines on 7 agile tasks, real G1 | supplies the adaptive-tolerance half (H2) but no rejection gate — tolerance without an accept/reject decision |
| [[2511.07820\|SONIC]] | scale tracking to 100M frames / 42M params | data-scale | 99.6% OOD-tracking SR sim, real-G1 zero-shot on all 50 trajectories | the data-scale counterpoint — projects nothing, scales tracking instead |
| [[2606.03985\|Humanoid-GPT]] | GPT-style tracking on a 2B-frame corpus | data-scale | 92.58% SR, <1.5 ms inference | the strongest data-scale bet — the head-to-head H1 must beat |
| [[2504.11054\|Meta Motivo]] | FB-CPR behavioral foundation model, no per-task reward | learned latent | preferred over reward-optimized agents, natural motion | empirical feasibility, not an explicit projection onto $\mathcal F$ |
| [[2511.04131\|BFM-Zero]] | FB-CPR + asymmetric training + domain randomization, promptable latent (motion/goal/reward) | learned latent (sim-to-real) | zero-shot real-G1 tracking + goal-reaching, natural kick/push recovery, few-shot single-leg balance >15 s under 4 kg (vs <5 s zero-shot) | same empirical-feasibility latent as Meta Motivo, now sim-to-real — but still no explicit projection onto $\mathcal F$ or rejection statistic |
| [[2405.18418\|Puppeteer]] | hierarchical TD-MPC2 tracking abstract mocap (56-DoF) | two-level | 97.8% naturalness (51 participants), zero-shot to 3× larger gaps | tracks abstract references, no physics-feasibility filter on the clip |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (rejection + adaptive tolerance, not more projection-then-tracking, is the lever on the extreme-skill tail).
1. **H1 — Rejection + adaptive tolerance beats scaled projection-then-track on the high-rejection tail.**
   - *Prediction*: on the extreme-skill subset where [[2506.12851|KungfuBot]]'s episode-collapse exceeds 30%, a rejection + adaptive-tolerance pipeline cuts tracking error below a scaled projection-then-track pipeline ([[2511.09484|SPIDER]]/[[2409.20514|Opt2Skill]]-style that tracks every projected clip) at equal compute, while the two tie on the easily-trackable bulk — the gain is tail-concentrated, not uniform.
   - *Test*: split the [[2602.13656|KungFuAthlete]] flip/martial-arts corpus by KungfuBot's rejection ratio; three-arm comparison — track-raw / scaled-projection-then-track / rejection+adaptive-tolerance — at fixed FLOPs on the standardized [[2511.17925|Switch-JustDance]] cross-controller protocol (JDS + MPJPE/MPKPE, already run on GMT/TWIST/Any2Track; JDS inversely correlates with PA-MPJPE r −0.76 to −0.42), reporting error per rejection stratum on a shared head-to-head substrate.
   - *Row*: KungfuBot (filter + adaptive tolerance) vs SPIDER (scaled projection-then-track), measured on Switch-JustDance.
   - *Falsifier*: scaled projection-then-track matches rejection+adaptive-tolerance on the high-rejection tail → the accept/reject gate buys nothing scale-plus-projection cannot.
2. **H2 — An adaptive tracking factor learns skills a fixed tolerance cannot.**
   - *Prediction*: an adaptive reward-tolerance schedule ([[2506.12851|KungfuBot]] / [[2510.14454|Adaptive Motion Tracking]]) learns dynamic skills (martial-arts, flips) that a fixed-tolerance reward fails to acquire, because early-loose / late-tight tolerance escapes the local optima a fixed reward traps in.
   - *Test*: ablate adaptive vs fixed tracking factor on a dynamic-skill set, scored on [[2502.01143|ASAP]]'s agile-skill tracking protocol (E_g-mpjpe / E_mpjpe on kick / jump-forward / step / single-foot-balance — e.g. kick E_g-mpjpe 61.2 mm → 50.2 mm); report learnability and final error.
   - *Row*: Adaptive Motion Tracking (adaptive phase/tracking adapters) / KungfuBot (adaptive tracking factor), under ASAP's tracking-error convention.
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
| **Thesis** | Treat getting-up as its own non-periodic, rich-contact, sparse-reward control problem, not a degenerate gait. The reason it must work: fall-recovery has no phase clock and no nominal contact schedule, so the periodicity and foot-contact priors that make locomotion learnable actively mislead it. That a *learned, curriculum-shaped* recovery beats a scripted routine is now consensus; what is unsettled is *which* structural prior makes the sparse-reward skill discoverable — and whether a locomotion phase-clock prior actively hurts. The bet is in First-principles below. |
| **Anchor papers** | [[2502.12152\|HUMANUP]] (method), [[2502.08378\|HoST]] (method), [[2606.12814\|Stubborn]] (method), [[2403.10506\|HumanoidBench]] (benchmark), [[2603.20147\|AGILE]] (benchmark) |
| **Key targets** | [[2502.12152\|HUMANUP]] 78.3% getting-up (supine) + 98.3% roll-over real on 6 terrains, ~6 s vs manufacturer 11 s, 20,000 randomized postures, single-stage training fails to converge; [[2502.08378\|HoST]] 100% standing on real G1 across flat/platform/wall/slope via multi-critic + vertical-force curriculum, multi-critic ablation **0%** without it, robust to 12 kg payload; [[2603.08619\|Classical Balance RL]] 93.4% recovery (sim), 10/10 zero-shot H1-2, balance-structure ablation fails to lift off |

**Why it matters.**
- **The gap**: a humanoid that cannot stand up after a fall is not autonomous — it needs a human — yet getting-up has no gait cycle, an arbitrary post-fall configuration, and a single binary reward at the end, so the locomotion playbook's inductive biases work *against* it.
- **Today's answers**: learned recovery is now multiply-instantiated, and crucially *via different structural priors* — [[2502.12152|HUMANUP]] separates a Discovery Policy from a Deployable Policy over 20,000 postures (78.3% supine / 98.3% roll-over, 6 terrains, ~6 s vs 11 s), while [[2502.08378|HoST]] reaches 100% standing on the same real G1 with **no** discover/refine split — a multi-critic architecture (0% without it) plus a vertical-force curriculum. Two decompositions reach parity, so the lever is *curriculum-shaped exploration generally*, not HUMANUP's specific discovery stage.
- **The opening**: the structural-prior question is sharpened, not closed — [[2603.08619|Classical Balance RL]] runs A3's own ablation (remove the balance-metric structure → the policy fails to lift off, 93.4% with it) and [[2602.16511|VIGOR]] beats HoST/FIRM by up to 5× on safe recovery, so what each prior *buys* is now measurable. The one untested claim is the cleanest: that a *periodic / phase-clock* prior — the locomotion default — actively *lowers* recovery SR, which no recovery paper has injected and measured.

**First-principles framing.**
- **First principle**: Fall-recovery has no phase clock and no nominal contact schedule — the initial state is an arbitrary post-fall configuration and the contact set is unknown. The phase-clocked, foot-contact-prior structure that makes locomotion well-shaped is *absent*; imposing it biases the policy away from the contact-rich ground transitions recovery needs. Two independent results show the sparse-reward landscape needs *some* structural scaffold: [[2502.12152|HUMANUP]] (single-stage fails to converge → discover/refine split) and [[2502.08378|HoST]] (no single critic suffices → 0% without multi-critic). What kind of scaffold is open; that a *gait-like* prior is the wrong one is the sharp claim.
- **Assumption being challenged**: *Not* that learned curriculum-shaped recovery beats a script — [[2502.08378|HoST]], [[2602.16511|VIGOR]] (89.5% stand-up / 90.5% recovery, beats HoST/FIRM up to 5×), [[2502.20061|HiFAR]] (100% supine/prone on Booster T1), and [[2410.08655|FRASA]] all demonstrate it, so that is consensus. The challenged assumption is finer: that imposing the *locomotion phase-clock / foot-contact prior* on a recovery policy is neutral. It is not — the gait prior should *bias against* the non-periodic ground-up transitions and *lower* SR, a prediction no recovery paper has tested.
- **The bet**: Injecting a phase-clock / periodic foot-contact prior into a prior-free recovery policy *lowers* arbitrary-config getting-up SR by a measurable margin (≥10 pp) versus the prior-free [[2502.12152|HUMANUP]] / [[2502.08378|HoST]] formulations; and HUMANUP's two-stage discover/refine and HoST's single-stage multi-critic reach *parity* (within 5 pp) on a matched posture/terrain distribution — confirming the lever is curriculum-shaped exploration, not a specific decomposition, and that gait structure actively hurts. Falsifiable: if the periodic prior is neutral-or-helpful, locomotion structure transfers to recovery; if multi-critic and two-stage differ by >5 pp at matched data, one decomposition *is* the lever after all.

**Related research papers.** One comparison table — the axis is *how the recovery / contact-rich motion is acquired* (two-stage discovery / scripted / workflow / generated / push-robust precursor), with what each leaves missing:

| System | Recovery acquisition | Periodicity assumption | Key result | What's missing |
|---|---|---|---|---|
| [[2502.12152\|HUMANUP]] | two-stage discover-then-deploy RL curriculum | none (non-periodic by design) | 78.3% supine / 98.3% roll-over, 6 terrains, ~6 s vs 11 s, 20,000 postures | single platform, single fall distribution |
| [[2606.12814\|Stubborn]] | **recovery emerges** from one tracking policy via Bernoulli probabilistic termination (episodes run *through* falls) | none (unstable states explored, not terminated) | 48.85 mm MPBPE (LAFAN1), 100% recovery from 5 m/s pushes (vs 77.5–85% no-PT), real 29-DoF G1 | recovery is implicit in a tracking reward — no explicit *discovery* of the ground-up trajectory HUMANUP isolates; no arbitrary-supine-config sweep |
| [[2502.08378\|HoST]] | **co-discovery: a different decomposition** — multi-critic (per-reward-group) + vertical-force curriculum, no discover/refine split | none (non-periodic) | **100%** standing on real G1 (flat/platform/wall/slope), multi-critic ablation **0%**, robust to 12 kg | reaches HUMANUP-parity *without* a discovery stage — the head-to-head proving the lever is curriculum-shaped exploration, not one decomposition |
| [[2603.08619\|Classical Balance RL]] | balance-metric structure (capture point, CoM, centroidal momentum) in reward + privileged critic | none (non-periodic) | 93.4% recovery (sim), 10/10 zero-shot H1-2, ablating the structure fails to lift off | runs A3's H1 ablation directly — *which* structural prior, not whether one is needed; still no periodic-prior test |
| [[2602.16511\|VIGOR]] | unified fall-mitigation + recovery, egocentric-depth-conditioned, sparse human pose priors | none (terrain-adaptive) | 89.5% stand-up / 90.5% recovery, beats HoST/FIRM up to 5×, 19/20 safe on stones real G1 | adds vision + safety, but still no isolation of *what each structural prior buys* nor the periodic-prior test |
| [[2511.07407\|Fall-Safety Policy]] | unified prevent + mitigate + recover from sparse human demos, diffusion + online adapter | none (multi-modal) | 93.20% uneven / 55.86% wave terrain (sim), 8/10 slippery real G1, lowest peak impulse | unifies the fall-safety lifecycle but doesn't sweep posture coverage or test the phase-clock prior |
| [[2502.20061\|HiFAR]] | 2D→3D staged curriculum + Key-State Initialization | none (staged) | **100%** supine/prone on Booster T1, 2.7 s recovery, 5 kg load, 150–200 N pushes | staged curriculum (the discover/refine precedent) but cross-platform fall distribution untested for the periodic-prior claim |
| [[2410.08655\|FRASA]] | CrossQ/SAC unified recovery + stand-up on 5 symmetric DoF | none (symmetry-exploited) | trains in 13–37 min, supine recovery 2.678 s (53% of champion KFB time) | fast + symmetry-efficient, but no arbitrary-config sweep and no structural-prior comparison |
| [[2512.12230\|Get-Up Across Morphologies]] | single morphology-agnostic recovery policy over 7 humanoids | none (morphology-shared) | 72% zero-shot to unseen Wolfgang, +61% over specialist on NUGUS | cross-morphology recovery (extends H5's autonomy reach), but no terrain/posture-coverage study |
| [[2604.17335\|G1 WBC-Gen+Track]] | RL-filtered *generated* contact-rich motion | reference-driven | 0.962 vs 0.230 box-climb, real | generation-side analogue, but for terrain traversal not arbitrary post-fall states |
| [[2605.10063\|EFGCL]] | force-guided curriculum for high-risk contact-rich skills | none (flips/jumps) | backflip/lateral-flip unlearnable by PPO | the contact-rich-skill-acquisition precedent, not recovery-specific |
| [[2502.08844\|MuJoCo Playground]] | GPU sim for large-scale posture randomization | — | minutes/hours training, vision-based policies | the 20,000-posture training substrate, not a recovery method |
| [[2512.01996\|Humanoid Loco 15min]] | push-robust locomotion (the disturbance preceding a fall) | periodic | 15-min sim-to-real G1+T1, push-robust | the *pre-fall* balance layer recovery backstops, not recovery itself |
| [[2505.22642\|FastTD3]] | off-policy RL on sparse-reward HumanoidBench tasks | — | solves HumanoidBench <3 hrs | the sample-efficient substrate for sparse recovery (feeds A5), not recovery-specific |
| [[2403.10506\|HumanoidBench]] | benchmark with sparse-reward whole-body tasks | — | flat RL fails; high-DoF exploration wall | the difficulty diagnostic, not a recovery method |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (recovery needs a structural scaffold but *not* a gait-like one; the scaffold's *kind* — not a specific decomposition — is the lever).
1. **H1 — Two-stage discovery and multi-critic reach parity — the lever is curriculum-shaped exploration, not one decomposition.**
   - *Prediction*: [[2502.12152|HUMANUP]]'s discover/refine split and [[2502.08378|HoST]]'s single-stage multi-critic + vertical-force curriculum reach arbitrary-config getting-up SR within 5 pp on a matched posture/terrain distribution, while an unstructured single-critic single-stage baseline fails to converge — confirming *some* curriculum-shaped scaffold is load-bearing but no specific decomposition is uniquely so.
   - *Test*: train discover/refine, multi-critic, and unstructured-single-stage on identical posture/terrain distributions; report convergence + SR; separately test [[2606.12814|Stubborn]]'s emergent recovery on arbitrary supine configs.
   - *Row*: HUMANUP (two-stage discovery) vs HoST (multi-critic) vs Stubborn (emergent).
   - *Falsifier*: the two decompositions differ by >5 pp at matched data → one decomposition *is* the lever, contra the parity claim.
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
   - *Test*: add a periodicity prior to the recovery policy; report SR delta vs prior-free. The phase-clock prior's effect at the *balance boundary* (the pre-fall margin the recovery policy backstops) is probed on the [[2404.19173|Single Contact++ RL]] repeatable impulse-perturbation protocol (Digit, fixed-magnitude/duration base pushes — its own controller rejects up to 258 N @ 500 ms), the only method-agnostic disturbance-recovery suite; ground-up arbitrary-config getting-up remains hand-built (no named suite).
   - *Row*: HUMANUP (non-periodic) vs [[2512.01996|Humanoid Loco 15min]] (periodic locomotion); disturbance flank on Single Contact++ RL.
   - *Falsifier*: the periodic prior is neutral or helps → locomotion structure transfers to recovery.
5. **H5 — A unified locomotion+recovery stack reaches end-to-end autonomy.**
   - *Prediction*: wiring fall-recovery as the fallback when A1's perceptive policy loses balance (perception dropout, push beyond recovery margin) yields a stack that completes a multi-obstacle course *including* falls without human intervention, where locomotion-only fails on the first fall.
   - *Test*: run a course with induced falls; compare end-to-end completion with vs without the recovery fallback. The no-reset, no-intervention autonomy axis is measured on [[2508.16943|LHM-Humanoid]] (350 scenes, completion-rate over object-sequence length within one continuous episode — 61.60% Success-All on 66 unseen tasks, 18.07% of five-object tasks, where end-to-end RL baselines hit 0.00%); LHM-Humanoid is the closest standardized no-reset course-completion substrate but chains loco-manip tasks rather than inducing falls, so the induced-fall course stays hand-built on top of it.
   - *Row*: HUMANUP (recovery) under [[2604.17335|G1 WBC-Gen+Track]] (perceptive locomotion); autonomy substrate [[2508.16943|LHM-Humanoid]].
   - *Falsifier*: the unified stack doesn't improve end-to-end completion → recovery and locomotion don't compose into autonomy.

> [!warning] Risks
> - **Recovery motions stress hardware** — flailing limbs and ground impacts risk motor/joint damage. → [[2502.12152|HUMANUP]]'s strong regularization lowers arm-motor temperature; report contact-force and temperature, treat smoothness as a first-class objective (couples to A4).
> - **Discovery may find unsafe trajectories** — weak regularization can produce violent motions infeasible for hardware. → The two-stage design refines discovery into a deployable policy; report the discovery→deployment safety-margin gap.
> - **Real falls exceed simulation coverage** — 20,000 postures may miss adversarial real falls. → H2's coverage curve bounds the claim; report failure modes by initial-configuration class, not a single average.

### A4 — Embodiment-Grounded Locomotion Constraints (Force, Acoustic, Thermal)

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Make a gait *trade off* its physical costs — ground-reaction force, noise, motor heat — under one regulated head, not regulate each in isolation. The reason it must work: a real robot's gait is bounded by hard embodiment limits (motor temperature, contact force, noise budgets) that exist *off* the sim reward surface and that *compete* — a quieter gait runs hotter. Single conditional cost-heads and two-cost couplings now exist, but no policy regulates the heat∧noise∧force triple jointly nor maps the *cross-cost* trade-off between them. The bet is in First-principles below. |
| **Anchor papers** | [[2604.23702\|QuietWalk]] (method), [[2605.27046\|Thermal-Aware Residual]] (method), [[2503.05035\|QuietPaw]] (method), [[2510.09543\|IMF Reward]] (method), [[2603.20147\|AGILE]] (benchmark), [[2403.10506\|HumanoidBench]] (benchmark) |
| **Key targets** | [[2604.23702\|QuietWalk]] GRF-predictor RMSE 14.49/14.00 N (R²=0.9887/0.9899), noise 7.17 dBA mean / 4.98 dBA peak across 4 footwear; [[2605.27046\|Thermal-Aware Residual]] overheating 70%→<10%, 650 m + 3 kg, <50 °C; [[2503.05035\|QuietPaw]] single conditional-cost head (CNCP) — Pareto hypervolume 10.416×10⁻², cost-violation 0.107 on real Go2; [[2510.09543\|IMF Reward]] two-cost coupling — 35% peak-power + 18–32% joint-torque cut |

**Why it matters.**
- **The gap**: simulation rewards task success — reach the velocity, climb the box — and silently omits the physical cost the real robot pays: motors overheat, gaits are loud, contact forces spike, and these are deployment-fatal, not cosmetic.
- **Today's answers**: each cost axis is now solved in isolation, and one paper even couples *two* — [[2605.27046|Thermal-Aware Residual]] drops overheating 70%→<10% (650 m + 3 kg), [[2603.01631|Thermal-Aware Locomotion]] independently quadruples thermal-safe runtime (7→27 min) on the same heat axis, [[2604.23702|QuietWalk]] cuts noise 7.17 dBA via a GRF predictor (R²≈0.99), and [[2510.09543|IMF Reward]] genuinely couples energy + impact (35% peak-power, 18–32% torque cut). But IMF's coupled pair is energy + impact, not heat + noise, and nobody regulates the full triple.
- **The opening**: [[2503.05035|QuietPaw]] supplies the mechanism — a *single conditional cost-head* (CNCP) that takes a desired cost threshold ε and produces a whole Pareto front (hypervolume 10.416×10⁻²) on a real Go2, proving one head can sweep a cost trade-off. The unclaimed step is feeding that head heat *and* noise *and* force at once and measuring the *cross-cost* surface — does a quieter gait provably run hotter under one regulated policy?

**First-principles framing.**
- **First principle**: A real robot's gait is bounded by hard embodiment limits — motor-temperature ceilings, actuator force limits, and (around people) noise budgets — that exist *off* the sim reward surface. A policy optimizing only task success saturates these limits because nothing penalizes them; the cost is invisible until the hardware fails or the gait is unacceptable. [[2605.27046|Thermal-Aware Residual]]'s 70% overheating under standard policies is the direct evidence: the embodiment cost is load-bearing for deployment, not a second-order concern.
- **Assumption being challenged**: *Not* that embodiment cost is a distinct lever — that is settled (QuietWalk, Thermal-Aware Residual, [[2503.05035|QuietPaw]], [[2510.09543|IMF Reward]] all show it). The challenged assumption is that costs are regulated *one-at-a-time* (or, at most, as the energy+impact pair IMF couples). QuietPaw's single conditional head sweeps a noise-vs-agility Pareto but never touches heat; IMF couples energy+impact but never noise. The bet is that the costs are *jointly* regulable under one head and that their *cross-trade-off* (thermal vs acoustic) is real and measurable, not that any single cost matters.
- **The bet**: A *single* conditional cost-head ([[2503.05035|QuietPaw]]-style CNCP) fed heat + noise + GRF (predicted at [[2604.23702|QuietWalk]]'s R²≈0.99) *jointly* holds overheating below [[2605.27046|Thermal-Aware Residual]]'s <10% **and** noise within +1 dBA of [[2604.23702|QuietWalk]]'s quiet-policy mean at ≤5% task-SR loss; **and** it traces a non-trivial *thermal-vs-acoustic* Pareto front — pushing noise down by ≥3 dBA provably raises peak motor temperature by a measurable margin — that two single-cost heads run independently cannot map. Falsifiable: if the joint head cannot hold both bounds at ≤5% SR loss, the costs are irreducibly separate; if the thermal-vs-acoustic front is flat (no measurable trade-off), the cross-cost coupling the bet rests on does not exist.

**Related research papers.** One comparison table — the axis is *which embodiment cost is regulated and how* (predict-then-regulate / residual / hard-constraint / diagnostics / temperature-precedent), with what each leaves missing:

| System | Cost regulated | Mechanism | Key result | What's missing |
|---|---|---|---|---|
| [[2604.23702\|QuietWalk]] | acoustic + contact (GRF) | PINN GRF predictor folded into the RL reward | R²=0.9887/0.9899, 7.17 dBA mean / 4.98 dBA peak, 4 footwear | single-cost (no thermal); the GRF predictor is the joint-cost enabler |
| [[2605.27046\|Thermal-Aware Residual]] | motor temperature | residual thermal policy over a base controller | 70%→<10% overheating, 650 m + 3 kg, <50 °C | single-cost (no acoustic/GRF); the residual structure the joint head extends |
| [[2503.05035\|QuietPaw]] | acoustic (conditioned on threshold ε) | **single conditional cost-head** (CNCP) + successor-feature decomposition | Pareto hypervolume 10.416×10⁻², cost-violation 0.107, real Go2 noise sweep | owns the single-head-sweeps-a-Pareto *mechanism* but for noise-vs-agility only — never heat, no cross-cost trade-off (the H4/H5 baseline the joint head extends) |
| [[2510.09543\|IMF Reward]] | impact + energy (**genuinely coupled**) | physics-informed Impact-Mitigation-Factor as a reward signal | 35% peak-power, 18–32% joint-torque, 18.4% CoT cut | the only true *two-cost coupling* here — but the pair is energy+impact, not heat+noise, and no conditional head to sweep the trade-off |
| [[2603.01631\|Thermal-Aware Locomotion]] | motor temperature (CBF-constrained) | whole-body thermal model in the reward, CBF temperature constraint | 7→27 min thermal-safe runtime (4×) on Unitree A1 + 3 kg, lower RMS torque | thermal co-twin of the residual row — confirms the heat axis is single-cost-solvable, still no acoustic or joint sweep |
| [[2502.10983\|Quiet Walking]] | acoustic (foot-contact velocity) | adaptive-PD + contact-sensor reward, DR-tunable quiet↔robust | 0.123 vs 0.417 m/s foot-contact velocity, beats Sony aibo controller | quiet via a fixed reward, not a conditional head — single operating point, no Pareto and no other cost |
| [[2506.23114\|Quiet Quadruped]] | acoustic (tunable quiet-factor β) | foot-velocity-minimizing gait + scalar β trade-off | ~8 dBA cut (64.80 dBA MNL at β=1), 68.25 dBA over 91.7 m | a *single* tunable cost-scalar (the QuietPaw idea on noise only) — confirms one-cost tunability, not joint regulation |
| [[2510.10851\|Preference-Conditioned MORL]] | force-compliance (preference-weighted) | preference-conditioned MORL, sensorless force inference via velocity-resistance model | 10 N guidance force (vs >25 N baseline), 50% SR under 50 N impact | preference-conditioned *multi-objective* head — the closest structural cousin, but trades tracking vs compliance, not the heat/noise/force triple |
| [[2012.06644\|CAPS]] | actuator power + control oscillation | temporal + spatial action-smoothness **loss terms** (not reward) | 80% lower power, 96% smoother control on a real quadrotor, simpler reward | regulates smoothness/power but is signal-blind — no GRF/thermal *prediction* feeding the trade-off the joint head needs |
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
4. **H4 — One conditional cost-head dominates separate single-cost heads on the joint bound.**
   - *Prediction*: extending [[2503.05035|QuietPaw]]'s single conditional head (CNCP) to take heat + acoustic + force thresholds holds overheating <10% **and** noise within +1 dBA of [[2604.23702|QuietWalk]]'s mean at ≤5% task-SR loss, dominating QuietPaw-on-noise and [[2605.27046|Thermal-Aware Residual]]-on-heat run independently — one head beats the union of two.
   - *Test*: train the conditional joint head; compare its joint-bound Pareto against QuietPaw (noise) + Thermal-Aware Residual (heat) run separately.
   - *Row*: QuietPaw (single conditional head) + Thermal-Aware Residual (thermal).
   - *Falsifier*: the joint head cannot hold both bounds at ≤5% SR loss → the costs are irreducibly separate objectives.
5. **H5 — The thermal-vs-acoustic trade-off is real and only one head can map it.**
   - *Prediction*: under the joint head, pushing noise down ≥3 dBA provably raises peak motor temperature by a measurable margin (a downward-sloping thermal-vs-acoustic Pareto front) — a *cross-cost* surface that two single-cost policies, each blind to the other's objective, cannot trace; [[2510.09543|IMF Reward]]'s energy+impact coupling is the only precedent and it omits both heat and noise.
   - *Test*: sweep the noise threshold under fixed heat budget; report the thermal-vs-acoustic front; compare against IMF's energy+impact coupling for a cross-cost baseline.
   - *Row*: IMF Reward (two-cost coupling) / QuietPaw (single conditional head).
   - *Falsifier*: the thermal-vs-acoustic front is flat (no measurable trade-off) → the cross-cost coupling the bet rests on does not exist and single-cost heads suffice.

> [!warning] Risks
> - **Cost-regulation can degrade task performance** — a quiet/cool gait may be slower or less agile. → [[2605.27046|Thermal-Aware Residual]] keeps performance via a residual; report the cost-vs-task Pareto front (H5), not a single number.
> - **GRF/thermal models are platform-specific** — R²≈0.99 on one robot may not transfer. → H3 tests generalization; treat cost predictors as per-platform-calibrated and report the transfer gap.
> - **Acoustic metrics are environment-dependent** — dBA depends on surface and room. → [[2604.23702|QuietWalk]] reports across 4 surfaces; report noise per surface, not a single average.

### A5 — Sample-Efficient Off-Policy & Flow Locomotion Learning

| | |
|---|---|
| **Cluster** | A — Bipedal Locomotion & Dynamic Skills |
| **Thesis** | Given that off-policy already beats PPO on wall-clock, the open question is whether *flow* policies beat Gaussian ones on multimodal-contact locomotion and whether *fast iteration* beats one slow run. The reason it must work: locomotion's dense reward and massively-parallel sim make sample-reuse efficient, but a unimodal Gaussian under-fits multimodal contact and a single long PPO run forgoes the reward/curriculum search that minutes-long off-policy training enables. The field has settled that off-policy is faster; what flow buys, and what sub-hour iteration buys, is not settled. The bet is in First-principles below. |
| **Anchor papers** | [[2403.10506\|HumanoidBench]] (benchmark), [[2502.08844\|MuJoCo Playground]] (benchmark), [[2603.20147\|AGILE]] (benchmark), [[2505.22642\|FastTD3]] (method), [[2512.01996\|Humanoid Loco 15min]] (method), [[2602.02481\|FPO++]] (method), [[2602.01156\|PolicyFlow]] (method) |
| **Key targets** | [[2505.22642\|FastTD3]] solves HumanoidBench tasks <3 hrs on one A100 (beats PPO/SAC/SimbaV2/TDMPC2/DreamerV3 wall-clock), batch 32,768 + distributional critic; [[2512.01996\|Humanoid Loco 15min]] sim-to-real G1+T1 in 15 min on one RTX 4090; [[2602.02481\|FPO++]] first sim-to-real flow-policy RL for humanoid locomotion; [[2602.01156\|PolicyFlow]] flow policy matches/beats PPO on IsaacLab at <50% extra training time, prevents mode collapse |

**Why it matters.**
- **The gap**: off-policy-beats-PPO-on-wall-clock is now established, so the live questions move downstream — does a *flow* policy's richer action distribution help on multimodal-contact skills, and does *sub-hour* training change how you search rewards and curricula?
- **Today's answers (settled background)**: the off-policy win is multiply-proven — [[2307.12983|Parallel Q-Learning]] (ICML'23) already beat PPO/DDPG/SAC on wall-clock on 5/6 Isaac Gym tasks, [[2605.24975|SAC Legged Locomotion]] *closes the PPO gap entirely* across 7 quadruped/humanoid platforms, and [[2505.22642|FastTD3]] solves HumanoidBench <3 hrs beating PPO/SAC/SimbaV2/TDMPC2/DreamerV3. The contrarian premium on "off-policy beats PPO" is gone.
- **The opening**: the two genuinely-open edges are the flow axis and the iteration axis — [[2602.01156|PolicyFlow]] shows a flow policy prevents mode collapse where Gaussian baselines fail and matches PPO at <50% extra training time, [[2505.22094|ReinFlow]] shows flow-RL with 82.63% wall-time savings over diffusion-RL, and [[2512.01996|Humanoid Loco 15min]]'s 15-minute loop makes a reward/curriculum search PPO's hours-long run cannot afford. Whether flow beats Gaussian *on multimodal contact* and whether N fast iterations beat one slow run are unresolved.

**First-principles framing.**
- **First principle**: Sample efficiency is governed by how often each environment step informs a gradient update. Off-policy replay reuses every transition many times; on-policy PPO discards each rollout after one update. With locomotion's dense reward and parallel sim (cheap, individually-informative transitions), the off-policy advantage compounds. [[2505.22642|FastTD3]] demonstrates it: large-batch off-policy updates with a distributional critic — and *no* complex stabilizers — beat PPO, DreamerV3, and TDMPC2 on wall-clock.
- **Assumption being challenged**: *Not* that off-policy beats PPO — [[2307.12983|Parallel Q-Learning]] (2023) and [[2605.24975|SAC Legged Locomotion]] settled that; it is now background. The challenged assumption is the *Gaussian* policy default: that a unimodal Gaussian suffices for locomotion's action distribution. Multimodal contact (which foot, which transition) is exactly where a Gaussian under-fits; [[2602.01156|PolicyFlow]]'s anti-mode-collapse result and [[2602.02481|FPO++]]'s sim-to-real flow gait bet the opposite — that a flow policy's expressive distribution is the next lever, on multimodal-contact skills specifically.
- **The bet**: A flow policy ([[2602.02481|FPO++]]/[[2602.01156|PolicyFlow]]-style) beats a matched Gaussian off-policy learner on gait quality and sim-to-real SR *specifically* on multimodal-contact skills (agile transitions, motion tracking) by a measurable margin, while tying on smooth walking where a Gaussian suffices; **and** at fixed total wall-clock, N fast [[2512.01996|Humanoid Loco 15min]]-style (15-min) iterations of reward/curriculum search converge to a better final gait than one [[2603.20147|AGILE]]-style (6–25 hr) PPO run. Falsifiable: if flow ties Gaussian on multimodal-contact tasks at matched compute, the richer distribution adds nothing; if one slow PPO run matches the iterated fast search, sub-hour training buys no better iteration.

**Related research papers.** One comparison table — the axis is *the learning substrate* (off-policy / flow / model-based / pretrain-finetune / real-world / MPC) and its wall-clock-to-deployable cost:

| System | Learning substrate | Wall-clock claim | Key result | What's missing |
|---|---|---|---|---|
| [[2505.22642\|FastTD3]] | off-policy TD3, batch 32,768 + distributional critic | <3 hrs on one A100 | beats PPO/SAC/SimbaV2/TDMPC2/DreamerV3, real Booster T1 | shown task-by-task, not across the full HumanoidBench locomotion suite |
| [[2604.04539\|FlashSAC]] | off-policy SAC + parallel sim + 10M replay | ~1 order-of-magnitude vs PPO | 60+ locomotion + manipulation tasks, sim-to-real humanoid | the off-policy peer corroborating FastTD3, not a flow comparison |
| [[2307.12983\|Parallel Q-Learning]] | decoupled actor/V-learner/P-learner off-policy (GPU replay) | beats PPO/DDPG/SAC wall-clock, 5/6 Isaac Gym | superior sample efficiency + robustness to env count | the *root* result settling off-policy-beats-PPO (2023) — but manipulation/quadruped, not the humanoid-flow question |
| [[2605.24975\|SAC Legged Locomotion]] | re-parameterized SAC (tight action bounds, N-step, timeout fix) | **closes the PPO gap entirely** | comparable/higher reward across 7 quadruped+humanoid platforms | proves PPO has no quality moat — but a wall-clock gap persists and it's Gaussian, not flow |
| [[2512.01996\|Humanoid Loco 15min]] | massively-parallel off-policy | 15 min on RTX 4090 | sim-to-real G1+T1, push-robust + 2-min dance | the fast-iteration substrate (H4) — state-based; vision-based wall-clock not characterized |
| [[2602.02481\|FPO++]] | flow-policy gradients | first flow sim-to-real | stable gaits, first flow-policy RL humanoid locomotion | no head-to-head flow-vs-Gaussian gait-quality study (the H3 gap) |
| [[2602.01156\|PolicyFlow]] | continuous-normalizing-flow policy + Brownian regularizer | <50% extra training time vs PPO | prevents mode collapse on MultiGoal, matches/beats PPO on IsaacLab | the flow-vs-Gaussian evidence (H3) — but evaluated on MuJoCo Playground/IsaacLab, not deployed humanoid contact |
| [[2505.22094\|ReinFlow]] | flow-matching policy fine-tuned via PPO (learnable noise injection) | 82.63% wall-time savings vs diffusion-RL | +135.36% episode reward (Gym locomotion), few-step denoising | flow-RL wall-clock peer — Gym locomotion, no multimodal-contact humanoid head-to-head |
| [[2604.10962\|ScoRe-Flow]] | flow-matching RL via closed-form score + variance predictor | 22× vs diffusion DPPO | 5100±47 Humanoid-v3, 2.4× faster convergence, 92.5% Robomimic | the flow-RL wall-clock peer FPO++ lacks — but shown on Humanoid-v3, not deployed sim-to-real like FPO++ |
| [[2502.15280\|Hyperspherical Normalization]] | off-policy with hyperspherical feature/weight normalization (no resets) | high-UTD scaling | 0.911 avg over 57 control tasks (UTD 8), beats Simba 0.780 | the off-policy *scaling* recipe — DMC/control suites, no humanoid sim-to-real or flow comparison |
| [[2502.17322\|TDMPBC]] | TD-MPC2 + self-imitative behavior cloning | +5% overhead | +120% return on HumanoidBench, 8/14 loco tasks in 2M steps | model-based off-policy peer — solves HumanoidBench loco but Gaussian-policy, no flow axis |
| [[2502.03550\|TD-M(PC)²]] | TD-MPC2 + policy regularization toward the MPC plan | no extra overhead | +100% on 14 61-DoF HumanoidBench loco tasks, cuts value error | model-based peer fixing TD-MPC2's policy — same Gaussian-policy limitation as TDMPBC |
| [[2502.07523\|CrossQ+WN]] | CrossQ + weight normalization (BN-based, high UTD) | high-UTD scaling | competitive at ~600k params (vs ~5M BRO), no resets | off-policy efficiency at tiny param count — DMC/MyoSuite only, not locomotion sim-to-real |
| [[2605.26478\|SDPG]] | stochastic-smoothing decoupled policy gradient (no full-traj differentiability) | hours on one RTX 4080 | matches state-based on visual MuJoCo, beats DreamerV3, zero-shot Go2 depth-nav | a third substrate (visual on-policy) — but not benchmarked on HumanoidBench wall-clock vs FastTD3 |
| [[2408.00342\|MuJoCo MPC HumanoidBench]] | sampling-based MPC (model-based, no learning) | — | beats DreamerV3/TD-MPC2/SAC/PPO on Stand/Walk/Push, 8 s episodes | the MPC counterpoint — no learned policy to deploy/finetune |
| [[2601.21363\|Pretrain-Finetune Bridge RL]] | SAC pretrain + physics WM, safe finetune | 80–590 s real data | zero-shot Booster T1, safe finetune from minimal real data | the pretrain+safe-finetune route, not a from-scratch wall-clock claim |
| [[2508.12252\|Robot Trains Robot]] | teacher-arm + dynamics-latent real-world RL | 15–20 min real | doubles walking speed in 20 min, swing-up from scratch in 15 min | real-world fast-adaptation, not the sim wall-clock comparison |
| [[2502.08844\|MuJoCo Playground]] | GPU-parallel sim substrate | minutes/hours | zero-shot to Go1 + Berkeley Humanoid | the parallel-sim substrate off-policy exploits, not a learner |
| [[2603.20147\|AGILE]] | scalable RL infra + L2C2, 6–25 hrs/task | 6–25 hrs/task | unified deployment workflow, motion-quality diagnostics | the workflow baseline off-policy methods undercut on wall-clock |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (flow beats Gaussian on multimodal contact, and fast iteration beats one slow run — off-policy-beats-PPO is settled background).
1. **H1 — Flow beats Gaussian specifically where contact is multimodal.**
   - *Prediction*: a flow policy ([[2602.02481|FPO++]]/[[2602.01156|PolicyFlow]]-style) beats a matched Gaussian off-policy learner ([[2605.24975|SAC Legged Locomotion]]-style) on gait quality + sim-to-real SR on multimodal-contact skills (agile transitions, motion tracking) and ties on smooth walking — the win concentrates where a unimodal Gaussian under-fits, not uniformly.
   - *Test*: at matched compute, compare flow vs Gaussian on walking vs agile-contact tasks; stratify by contact multimodality; report gait quality + sim-to-real SR.
   - *Row*: FPO++ (flow sim-to-real) / PolicyFlow (anti-mode-collapse flow) vs SAC Legged Locomotion (Gaussian).
   - *Falsifier*: flow ties Gaussian on multimodal-contact tasks at matched compute → the richer distribution adds nothing.
2. **H2 — Large batch + distributional critic is the load-bearing off-policy component.**
   - *Prediction*: ablating [[2505.22642|FastTD3]]'s batch 32,768 and distributional critic, one of the two carries most of the stability/speed and dropping it degrades high-DoF off-policy control toward instability.
   - *Test*: factorial ablation (batch size × distributional vs scalar critic); report convergence and final SR.
   - *Row*: FastTD3 (off-policy) vs Hyperspherical Normalization (alternative scaling recipe).
   - *Falsifier*: neither ablation matters → the speed comes from elsewhere (e.g. raw parallelism alone).
3. **H3 — Flow's wall-clock cost stays bounded as the distribution gets richer.**
   - *Prediction*: a flow policy's training-time overhead over a Gaussian off-policy learner stays within [[2602.01156|PolicyFlow]]'s <50% (and [[2505.22094|ReinFlow]]'s few-step denoising keeps inference real-time), so the H1 gait-quality win is not paid back in wall-clock — flow is a net Pareto improvement, not a quality-for-speed trade.
   - *Test*: measure flow-vs-Gaussian training time + inference latency at matched final SR; report the cost of the richer distribution.
   - *Row*: PolicyFlow (<50% extra training) / ReinFlow (few-step denoising).
   - *Falsifier*: flow's overhead exceeds its quality win → the richer distribution is not worth its wall-clock.
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
| **Thesis** | Infer the unobserved environment context from proprioceptive *history* alone, without exteroception or online real-world fine-tuning. The reason it must work: the privileged state (friction, payload, terrain) leaves a recoverable signature in the recent proprioceptive trajectory, so a supervised module can read it back out without ever sensing it directly. That proprioceptive inference *works* is now consensus; the open question is whether *one* context module holds the heavy-payload × discontinuous-terrain conjunction at once, and which backbone trades the two axes. The bet is in First-principles below. |
| **Anchor papers** | [[2107.04034\|RMA]] (method), [[2212.07740\|TERT]] (method), [[2301.10602\|DreamWaQ]] (method), [[2312.11460\|HIM]] (method), [[2507.07825\|LoadAdapt]] (method), [[2403.13358\|QUARD-Auto]] (method), [[2305.14654\|Barkour]] (benchmark), [[2403.10506\|HumanoidBench]] (benchmark) |
| **Key targets** | [[2107.04034\|RMA]] 12 kg payload (80% body weight) on 4 terrains, 100 Hz base / 10 Hz adaptation, zero fine-tuning; [[2212.07740\|TERT]] 100% sand / 60% stairs vs RMA 0% across 9 terrains; [[2312.11460\|HIM]] 100% real stairs / 176.5 steps long-range (vs RMA 75.35), 8 kg payload, contrastive internal-model embedding; [[2507.07825\|LoadAdapt]] zero-shot 4/6 kg loads on uneven terrain from proprioception alone; [[2301.10602\|DreamWaQ]] 95.23% survival + 430 m/465 m real outdoor courses, context-aided estimator |

**Why it matters.**
- **The gap**: a quadruped's deployable policy must act on proprioception alone — joint angles, IMU, contact — because the privileged context sim provides (friction $\mu$, payload $m$, ground compliance) is unavailable on hardware, and the field's two escape routes (a camera, or on-robot fine-tuning) both add cost.
- **Today's answers**: proprioceptive context inference is now mature and *backbone-diverse* — [[2107.04034|RMA]] regresses extrinsics with a TCN (12 kg, zero fine-tuning), [[2301.10602|DreamWaQ]] infers a latent context via a Beta-VAE estimator (95.23% survival, 430 m real outdoor), [[2312.11460|HIM]] learns a contrastive internal-model embedding (100% real stairs, 8 kg), and [[2507.07825|LoadAdapt]] adds an explicit Load-Characteristics Estimator (zero-shot 4/6 kg on uneven terrain). The mechanism is settled; what each backbone *trades* is not.
- **The opening**: [[2212.07740|TERT]]'s 60%-vs-0% stair result with the *same* privileged supervision but a Transformer instead of RMA's TCN proves backbone choice — not signal availability — sets discontinuous-terrain context, while [[2507.07825|LoadAdapt]] caps near 8 kg without running the stair contrast. No single system reports *both* RMA's 80%-body-weight payload *and* TERT's stairs-where-TCN-fails under one controlled backbone swap — the conjunction is the open cell.

**First-principles framing.**
- **First principle**: The privileged context — friction, payload, terrain — cannot be read directly off the hardware, but it shapes how the robot's joints and IMU respond, so it leaves a recoverable fingerprint in the recent proprioceptive history. A supervised module can regress that history into a context estimate, making the privileged state inferable without ever sensing it directly. [[2107.04034|RMA]] demonstrates it: an adaptation module reading proprioceptive history at 10 Hz sustains a 12 kg payload across four terrains, zero fine-tuning.
- **Assumption being challenged**: *Not* that proprioceptive inference works at all — [[2301.10602|DreamWaQ]], [[2312.11460|HIM]], and [[2507.07825|LoadAdapt]] settled that, none needing vision or fine-tuning. The challenged assumption is that a single backbone holds *both* heavy payload *and* discontinuous terrain at once: the payload line (RMA/LoadAdapt) and the discontinuous-terrain line (TERT/HIM) are studied *separately*, and the field tacitly assumes one module covers both. The bet is that they *trade* — a backbone tuned for one axis pays on the other unless capacity is allocated for the conjunction.
- **The bet**: Under a controlled backbone swap (TCN / contrastive-IMC / Transformer / Transformer-XL) at *identical* privileged supervision, *no single backbone* simultaneously matches [[2107.04034|RMA]]'s 12 kg (80% body weight) payload *and* [[2312.11460|HIM]]/[[2212.07740|TERT]]'s discontinuous-terrain ceiling (≥60% stairs where TCN scores 0%) — there is a measurable payload-vs-terrain trade-off curve, and only an attention/long-context backbone with allocated capacity holds the conjunction at 100 Hz control / 10 Hz adaptation, zero fine-tuning. Falsifiable: if one off-the-shelf backbone holds both axes at once with no trade-off, the conjunction is free and the controlled ablation is unnecessary; if an exteroceptive policy beats proprioceptive inference on *dynamics* context (friction/payload, not geometry), proprioception alone is insufficient.

**Related research papers.** One comparison table — the axis is *how the unobserved context is recovered* (regress-from-history / Transformer-context / in-context / exteroceptive / meta-learned / MoE-capacity), with what each leaves missing:

| System | Context-recovery mechanism | Sensing | Key result | What's missing |
|---|---|---|---|---|
| [[2107.04034\|RMA]] | adaptation module regresses extrinsics from proprio history (10 Hz) | proprioceptive | 12 kg payload, 4 terrains, zero fine-tuning | TCN backbone fails on discontinuous terrain (stairs) |
| [[2212.07740\|TERT]] | Terrain Transformer predicts teacher actions from proprio history | proprioceptive | 100% sand / 60% stairs vs RMA 0%, 9 terrains | terrain-focused — no 80%-payload number under the same backbone |
| [[2301.10602\|DreamWaQ]] | context-aided estimator (Beta-VAE latent + velocity) | proprioceptive | 95.23% survival, 430 m/465 m real KAIST outdoor (mud/stairs/gravel) | infers latent context richly but doesn't headline heavy payload or the stair-vs-TCN contrast |
| [[2312.11460\|HIM]] | **contrastive** hybrid-internal-model embedding (no regression target) | proprioceptive | 100% real stairs, 176.5 steps long-range (vs RMA 75.35), 8 kg | discontinuous-terrain SUBSTANTIAL via contrastive backbone — caps at 8 kg, no 80%-body-weight payload sweep |
| [[2507.07825\|LoadAdapt]] | explicit Load-Characteristics Estimator (mass/friction/position) | proprioceptive | zero-shot 4/6 kg loads on uneven terrain, near-Oracle | heavy-payload SUBSTANTIAL — but ≤~8 kg and no stair-SR-vs-RMA contrast (the conjunction's other axis) |
| [[2507.04039\|ROLT]] | Robust Locomotion **Transformer** (body tokenization + consistent dropout) | proprioceptive + elevation | zero-shot Go1, beats RMA on weakened-limb/box-drag/skates OOD | the Transformer-backbone OOD candidate for the ablation — robustness-focused, no controlled payload×terrain conjunction sweep |
| [[2407.04224\|PA-LOCO]] | **multi-encoder** decoupling of force/terrain/state privileged features | proprioceptive | 90% recovery from 4.6 kg lateral impact (vs 43%), 0.75 s | decoupled-feature backbone — impulse-robust but not the standing payload×stair conjunction |
| [[2509.23745\|LocoFormer]] | Transformer-XL long-context in-context adaptation | proprioceptive | 0.96 displacement on 10 morphologies; zero-shot to locked limbs / wheel failure / payload | in-context (the 4th backbone in the ablation), but no explicit privileged-context inference target |
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
2. **H2 — Backbone trades the payload axis against the discontinuous-terrain axis — no single one holds both.**
   - *Prediction*: under *identical* privileged supervision, swapping TCN ([[2107.04034|RMA]]) ↔ contrastive-IMC ([[2312.11460|HIM]]) ↔ Transformer ([[2212.07740|TERT]]/[[2507.04039|ROLT]]) ↔ Transformer-XL ([[2509.23745|LocoFormer]]), each backbone's payload ceiling (toward 80% body weight) and discontinuous-terrain ceiling (stairs where TCN=0%) trade off — a measurable Pareto curve — and only an attention/long-context backbone with allocated capacity holds RMA's payload *and* HIM's stairs at once.
   - *Test*: hold supervision fixed; for each backbone sweep payload (0→80% body weight) × terrain (flat→stairs) on the [[2602.00678|RoboGauge]] graded proprioceptive-quadruped suite (10 difficulty levels × 7 tasks across terrain × domain-randomization; its own MoE policy scores 0.6713 overall, terrain level 7.85, 4.01 m/s flat + 17/20 over a 30 cm obstacle on real Go2); report the joint SR surface and the payload-vs-terrain Pareto, adding an 80%-body-weight payload sweep RoboGauge does not itself include.
   - *Row*: HIM (contrastive-IMC) / TERT (Transformer) / RMA (TCN) / LocoFormer (Transformer-XL), graded on RoboGauge.
   - *Falsifier*: one off-the-shelf backbone holds both axes with no trade-off → the conjunction is free and the controlled ablation is unnecessary.
3. **H3 — Adaptation rate must track disturbance bandwidth.**
   - *Prediction*: sweeping [[2107.04034|RMA]]'s 10 Hz adaptation rate against disturbance bandwidth, there is a minimum rate below which fast payload/terrain shifts are not tracked, and above which gains saturate — a bandwidth-matched optimum.
   - *Test*: vary adaptation frequency; inject calibrated disturbances at varying bandwidth via the [[2308.14636|Linear Impactor]] protocol (a pneumatic linear impactor characterizing disturbances by impact *momentum*, <0.1 m/s repeatability, withstood up to 26.376 kg·m/s on Digit) — a reproducible, fair injection apparatus replacing ad-hoc hand-pushes — and report tracking error vs injected bandwidth.
   - *Row*: RMA (10 Hz adaptation), disturbance-injection via Linear Impactor.
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
| **Thesis** | Adapt a sim-pretrained *learned latent* world model with a handful of real trajectories *by dreaming* — not by reconstructing a digital-twin sim and retraining the policy in it. The reason it must work: a learned dynamics model lets the policy *imagine* action consequences, so each real interaction updates a model that generates thousands of synthetic ones, and an epistemic bound keeps the imagination honest. Anti-DR few-shot adaptation is now consensus; what is unsettled is whether latent *dreaming* beats *reconstructed-sim retraining* at a matched real-data budget, and whether the imagination is bounded. The bet is in First-principles below. |
| **Anchor papers** | [[2206.14176\|DayDreamer]] (method), [[2504.16680\|RWM-U]] (method), [[2604.02911\|DreamTIP]] (method), [[2603.15759\|SimDist]] (method), [[2409.17992\|LoopSR]] (method), [[2403.10506\|HumanoidBench]] (benchmark) |
| **Key targets** | [[2604.02911\|DreamTIP]] 28.1% avg transfer gain + Go2 100% on 52 cm Climb (vs WMP 10%), ~5 real trajectories; [[2206.14176\|DayDreamer]] A1 walks in 1 hr real + push-recovers in 10 min; [[2603.15759\|SimDist]] 1.5–2× throughput + 15–30 min real adaptation; [[2504.16680\|RWM-U]] 0.91 on ANYmal D (offline sim+real), beats online model-free; [[2409.17992\|LoopSR]] real→sim digital-twin retrain at <5 min data — 100% Stair-Up vs 70% origin (the reconstructed-sim baseline dreaming must beat) |

**Why it matters.**
- **The gap**: deep RL needs millions of interactions — impractical on hardware — and the field's two answers (exhaustive domain randomization, extensive on-robot RL) are both inefficient ways to close the sim-to-real dynamics gap.
- **Today's answers**: anti-DR few-shot adaptation is now a crowded field with *two distinct mechanisms* — the *reconstruct-then-retrain* line ([[2409.17992|LoopSR]] rebuilds a digital twin from <5 min real data and retrains the policy: 100% Stair-Up vs 70%; [[2604.11090|Simulator Adaptation Loco]] identifies sim parameters via Wasserstein matching, cutting drift 80% from <5 min data) and the *latent-dreaming* line ([[2604.02911|DreamTIP]] adapts a task-invariant latent: 100% vs 10% on a 52 cm climb from ~5 trajectories; [[2206.14176|DayDreamer]] walks in 1 hr). Both beat DR at a tiny budget — but nobody has run them head-to-head.
- **The opening**: the surviving wedge is *which* mechanism wins at a matched budget, plus a bound none of them carries — [[2504.16680|RWM-U]] supplies the missing epistemic penalty (0.91 on ANYmal D, beats online model-free from offline data), and [[2502.11377|PrivilegedDreamer]] shows latent dreaming with hidden-parameter estimation adapts in a few steps (+41% off-legged). LoopSR and Simulator Adaptation both *lack* an epistemic bound, so a bounded dreamer is the distinct bet.

**First-principles framing.**
- **First principle**: A learned dynamics model is a *multiplier* on real data — each real transition updates the model and, through imagination, generates many synthetic transitions for policy optimization. Sample efficiency is governed by model accuracy per real interaction, not raw interaction count; a good model makes 5 trajectories worth thousands. [[2604.02911|DreamTIP]] demonstrates the multiplier: ~5 real trajectories yield 100% on a 52 cm climb where a non-dreaming baseline gets 10%.
- **Assumption being challenged**: *Not* that few-shot adaptation beats DR — [[2409.17992|LoopSR]] and [[2604.11090|Simulator Adaptation Loco]] settled that via reconstruction, on the same No-Free-Lunch anti-DR framing. The challenged assumption is that *reconstructing a digital-twin sim and retraining* is the way to spend those few trajectories. Reconstruct-then-retrain (LoopSR) needs a faithful sim rebuild and carries no uncertainty estimate; the bet is that *latent dreaming* extracts more per trajectory and that an epistemic bound — which LoopSR and Simulator Adaptation both lack — is what makes the tiny budget safe.
- **The bet**: At a matched ≤5-trajectory / 15–30-min real budget, a *bounded latent dreamer* ([[2604.02911|DreamTIP]] + [[2504.16680|RWM-U]]'s epistemic penalty, 0.91 ANYmal D) reaches DreamTIP's 100%-vs-10% on a 52 cm climb *and beats reconstruct-then-retrain* ([[2409.17992|LoopSR]]'s 100% Stair-Up via digital-twin) on held-out terrain by a measurable margin, because dreaming generalizes across the latent where a reconstructed sim overfits the rebuilt geometry. Falsifiable: if reconstruct-then-retrain (LoopSR/Simulator-Adaptation) matches the bounded dreamer at the matched budget on held-out terrain, latent dreaming adds no multiplier over rebuilding the sim; if a DR-blind policy matches both, neither adapts.

**Related research papers.** One comparison table — the axis is *the world-model role* (real-from-scratch / transfer-latent / sim-pretrain / uncertainty-bound / cross-embodiment / context-aligned / online-continual / foundation), with what each leaves missing:

| System | World-model role | Real-data budget | Key result | What's missing |
|---|---|---|---|---|
| [[2604.02911\|DreamTIP]] | task-invariant transfer latent | ~5 trajectories | 28.1% avg gain, Go2 100% on 52 cm climb vs WMP 10% | no explicit uncertainty bound on the imagination |
| [[2206.14176\|DayDreamer]] | real-world Dreamer from scratch (no sim) | 1 hr walking / 10 min push | A1 walks in 1 hr, recovers from pushes in 10 min | from-scratch, no sim pretraining to amortize |
| [[2603.15759\|SimDist]] | sim-pretrained world model + rapid real adapt | 15–30 min | 1.5–2× throughput, quadruped + manipulation | freezes core components; no epistemic bound |
| [[2409.17992\|LoopSR]] | **reconstruct-then-retrain**: real→sim digital twin via latent param estimation, lifelong loop | <5 min real | 100% Stair-Up vs 70%, 4.33 s vs 5.01 s, real A1 | the reconstruct-not-dream alternative (anti-DR, same No-Free-Lunch framing) — needs a faithful sim rebuild, no epistemic bound on the imagination |
| [[2604.11090\|Simulator Adaptation Loco]] | **sim-parameter ID** via 1D-Wasserstein proprio matching (CMA-ES) | <5 min real | 80% drift cut on Go2 bipedal-walk/spring-joint, 18.7% vs 86.3% error at high noise | identifies a sim, doesn't dream — proprioception-only and time-alignment-free, but still reconstruct-then-deploy with no uncertainty estimate |
| [[2502.11377\|PrivilegedDreamer]] | latent dreaming + dual-recurrent hidden-parameter estimation (DreamerV2-like) | few env steps | +41% avg reward over best baseline across 5 HIP-MDP tasks | proves dreaming-for-rapid-adaptation with explicit context — but off-legged (no real quadruped few-shot transfer) and no epistemic penalty |
| [[2504.16680\|RWM-U]] | uncertainty-aware MBRL (MOPO-PPO penalty) | offline sim+real | 0.91 ANYmal D, beats online model-free | offline, not few-shot-*online* adaptation — supplies the epistemic bound LoopSR/Simulator-Adaptation lack |
| [[2005.13239\|MOPO]] | reward penalized by dynamics-ensemble uncertainty (the epistemic-bound progenitor) | offline dataset | 4016.6 OOD return on halfcheetah-jump from max-1808.6 data, beats model-free offline | the uncertainty-penalty *root* RWM-U adapts to legged — D4RL only, no real-robot or few-shot legged transfer |
| [[2501.10100\|RWM]] | neural-simulator world model, cross-embodiment | offline | zero-shot velocity tracking, ANYmal D + G1, beats DreamerV3/SHAC | the cross-embodiment substrate, no real-adaptation few-shot study |
| [[2604.08780\|Hardware-Agnostic Quadruped WM]] | morphology-conditioned DreamerV3 WM (physical-morphology encoder) | offline | zero-shot loco on unseen real Go1 + ANYmal-D, zero falls | demonstrates the morphology-portable WM H4 predicts — but zero-shot, not the few-shot dreaming-vs-reconstruction head-to-head |
| [[2508.20294\|DALI]] | dynamics-aligned latent context from short histories | short histories | +96.4% over context-unaware Dreamer | context-aligned, but evaluated in sim control suites not real legged |
| [[2603.04029\|Self-Adapting RL]] | online continual world-model feedback | 4–8 min real | ANYmal actuator-failure recovery 4 min, real F1Tenth 8 min | fault-recovery face, not terrain/payload few-shot transfer |
| [[1912.01603\|Dreamer]] | latent-imagination MBRL foundation | — | 20× data-efficiency, ~3 hrs/million steps | the progenitor — not a real-robot adaptation method itself |
| [[2003.01239\|Evolutionary Meta-Learning Legged]] | model-free meta-adaptation (no world model) | 50 rollouts / 150 s | Minitaur +100% velocity | the model-free fast-adaptation counterpoint dreaming must beat |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a bounded latent dreamer beats reconstruct-then-retrain at a matched few-trajectory budget, especially on held-out terrain).
1. **H1 — Latent dreaming beats reconstruct-then-retrain at a matched real-data budget.**
   - *Prediction*: at a matched ≤5-trajectory budget, [[2604.02911|DreamTIP]]-style latent dreaming beats [[2409.17992|LoopSR]]-style reconstruct-then-retrain (and [[2604.11090|Simulator Adaptation Loco]]'s param-ID) on *held-out* terrain by a measurable margin, because dreaming generalizes across the latent while a reconstructed sim overfits the rebuilt geometry — both beat a DR-blind policy.
   - *Test*: three-arm comparison at fixed real-data budget — DR-blind / reconstruct-then-retrain / latent-dreaming — adapt on terrain A, evaluate held-out terrain B.
   - *Row*: DreamTIP (latent dreaming) vs LoopSR (reconstruct-then-retrain) vs Simulator Adaptation Loco (param-ID).
   - *Falsifier*: reconstruct-then-retrain matches the dreamer on held-out terrain at the matched budget → latent dreaming adds no multiplier over rebuilding the sim.
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
   - *Prediction*: a morphology-conditioned world model ([[2604.08780|Hardware-Agnostic Quadruped WM]] zero-shots unseen Go1 + ANYmal-D; [[2501.10100|RWM]] runs one pipeline on ANYmal D + G1) transfers a measurable fraction of its dynamics to a humanoid, more than a manipulation grasp model would, confirming the gait object's portability.
   - *Test*: pretrain on quadruped, measure zero-shot/few-shot humanoid transfer vs from-scratch.
   - *Row*: Hardware-Agnostic Quadruped WM (morphology-conditioned) / RWM (cross-embodiment).
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
| **Anchor papers** | [[2506.05997\|SRU]] (method), [[2604.26504\|HiPAN]] (method), [[2605.28442\|COTRATE]] (method), [[2512.02851\|SwarmDiffusion]] (method), [[2405.01792\|Wheeled-Legged NavLoco]] (method) |
| **Key targets** | [[2506.05997\|SRU]] 23.5% higher long-range mapless SR vs LSTM/GRU + 29.6% over EMHP / 105.0% over GTRL, zero-shot 100+ m on a real Unitree B2W legged-wheel robot; [[2604.26504\|HiPAN]] 94.7% SR / 83.6 SPL in Complex-2, Go1 onboard depth in cluttered/dead-end/outdoor; [[2605.28442\|COTRATE]] cross-platform traversability (Spot + Husky), ≥2.5 pp mIoU (Spot) / ≥2.1 pp (Husky); [[2405.01792\|Wheeled-Legged NavLoco]] kilometer-scale urban nav via a *map-using* hierarchical planner (1.68 m/s, 0.16 CoT, 0 collisions) — the map→plan→track incumbent the mapless bet must beat |

**Why it matters.**
- **The gap**: long-range goal-reaching is the locomotion-to-goal problem — distinct from VLN goal *reasoning* and from manipulation — and the classical map-build → plan → track pipeline is brittle on unstructured terrain (drift, dynamic obstacles, no GPS) because the explicit metric map is the weakest link, yet that brittleness is *asserted*, not measured against a graded map-friendliness axis.
- **Today's answers**: [[2506.05997|SRU]] takes the memory axis — a Spatially-enhanced Recurrent Unit gives an end-to-end RL policy a spatial state that survives hundreds of steps, lifting mapless SR 23.5% over LSTM/GRU and transferring zero-shot 100+ m on a real B2W; [[2604.26504|HiPAN]] takes the traversal axis (94.7% SR / 83.6 SPL in Complex-2, Go1 depth); and the SRU authors' own follow-on [[2603.13888|Path-Conditioned Local Planner]] adds long-range path guidance (SPL 0.82, +7.02%, robust to degraded paths) — the recurrent-memory core none of these displaces.
- **The opening**: two narrowing results sharpen the bet rather than take it — [[2512.02851|SwarmDiffusion]] *jointly* infers traversability + generates a trajectory in one diffusion model (80–100% SR, 0.09 s, adapts to new embodiments from a few hundred samples), going beyond [[2605.28442|COTRATE]]'s perception-only substrate, while [[2405.01792|Wheeled-Legged NavLoco]]'s kilometer-scale *map-using* hierarchical planner is the strong incumbent the mapless claim must beat *where the map should be at its best*.

**First-principles framing.**
- **First principle**: Long-range locomotion-to-goal needs a spatial state that persists across hundreds of control steps (where have I been, where is the goal relative to me) *and* a coupling between that state and the gait. An explicit metric map is one lossy realization — brittle under drift and dynamics — and the map-build → plan → track factoring severs the perception-gait coupling the policy could exploit. [[2506.05997|SRU]] demonstrates the alternative: a learned recurrent spatial state lifts mapless SR 23.5% over LSTM/GRU and transfers zero-shot 100+ m.
- **Assumption being challenged**: That goal-reaching factors cleanly into map-build → plan → track — held strongest by map-using stacks like [[2405.01792|Wheeled-Legged NavLoco]] (kilometer-scale urban nav, 0 collisions). [[2506.05997|SRU]]'s 23.5% mapless gain and [[2604.26504|HiPAN]]'s 94.7% dead-end SR bet the opposite — *learned* spatial memory beats the factored pipeline where the map breaks first. The open question the incumbents force is *where exactly* it breaks: the mapless advantage should be a function of map-friendliness, not a constant.
- **The bet**: The mapless-memory advantage is *graded by map-friendliness* — the [[2506.05997|SRU]]-style mapless-minus-mapped SR gap is near-zero on feature-rich static courses (where [[2405.01792|Wheeled-Legged NavLoco]]'s map→plan→track is at its best) and *widens monotonically* to ≥20 pp as feature density drops, dynamics rise, and drift accumulates; with [[2512.02851|SwarmDiffusion]]-style joint traversability+trajectory and [[2605.28442|COTRATE]] cross-platform perception holding the advantage across embodiments. Falsifiable: if the mapless-minus-mapped gap is *constant or shrinks* as terrain becomes less map-friendly, the explicit metric map is not the weakest link and learned memory buys nothing the map doesn't.

**Related research papers.** One comparison table — the axis is *how the spatial state and goal-reaching are represented* (recurrent-memory / hierarchical-posture / traversability-substrate / vision-to-goal / cross-embodiment / emergent-planning / dynamic-scene), with what each leaves missing:

| System | Goal-reaching representation | Map / memory | Key result | What's missing |
|---|---|---|---|---|
| [[2506.05997\|SRU]] | spatially-enhanced recurrent unit, end-to-end RL | learned mapless memory | 23.5% over LSTM/GRU, 29.6% over EMHP, 105.0% over GTRL, 100+ m real B2W | single platform per run; no cross-platform traversability |
| [[2301.13261\|Blind Nav Agents]] | point-goal RL from egomotion only, generic LSTM | **emergent** metric map in recurrent state | 95.1% SR / 62.9% SPL, memory useful to 1,000 steps (~89 m), 32.5% IoU map decode | the existence proof SRU rests on — but egomotion-only in sim, no terrain-coupled gait or hardware deployment |
| [[2604.02829\|STRNet]] | graph spatial aggregation + temporal-shift fusion of visual frames | implicit (richer encoding, no map) | 100% SR / 0 collisions basic, 98% SR / 0.02 collisions long-range, real-time, fewer params | a representation upgrade, not a *recurrent spatial state* — no explicit hundreds-of-steps relative-goal memory like SRU |
| [[2604.26504\|HiPAN]] | hierarchical posture-adaptive locomotion + path-guided curriculum | implicit (no metric map) | 94.7% SR / 83.6 SPL Complex-2, Go1 depth, cluttered/dead-end/outdoor | posture-adaptive but quadruped-specific, no cross-platform transfer |
| [[2605.28442\|COTRATE]] | self-supervised online traversability prediction | perception substrate | cross-platform (Spot + Husky), ≥2.5 pp mIoU (Spot), path-effort cut | a perception layer, not a full goal-reaching policy |
| [[2512.02851\|SwarmDiffusion]] | **joint** traversability inference + trajectory generation (one diffusion model) | implicit (no map) | 80–100% SR quadruped+aerial, 0.09 s latency, new embodiment from a few hundred samples | jointly does perception + planning (beyond COTRATE's perception-only) but has no *recurrent long-range spatial memory* — local generation, not hundreds-of-steps relative-goal recall |
| [[2603.13888\|Path-Conditioned Local Planner]] | RL conditioned on the *whole encoded global path* + shortcut reward | implicit (path-guided, no map) | SPL 0.82 (+7.02%) optimal path, robust to degraded paths, real B2W | the SRU authors' own follow-on — adds path guidance (sharpens H5) but offloads long-range memory to the given path rather than learning it |
| [[2405.01792\|Wheeled-Legged NavLoco]] | hierarchical HLC navigation + privileged LLC locomotion, **uses a map** | metric map → plan → track | kilometer-scale urban nav, 1.68 m/s, 0.16 CoT, 0 collisions, 0.34 ms planning | the map→plan→track incumbent (the H1 baseline) — strong where features are dense, the brittleness the mapless bet must expose on unstructured terrain |
| [[2107.03996\|LocoTransformer]] | vision-guided end-to-end locomotion to goal | reactive (attention) | 92% farther real, attends to obstacles + distant goal | no persistent spatial memory over hundreds of steps |
| [[2509.23203\|CE-Nav]] | flow geometric expert + RL dynamics-refiner | mapless, cross-embodiment | mSR 0.745–0.860 on 5 embodiments, 8× faster, real Go2 | local navigation focus, no long-range spatial-memory study |
| [[2403.13358\|QUARD-Auto]] | MoE generalist with emergent path planning | emergent | 71–90.5%, emergent adaptive path planning unseen scenes | path planning is emergent, not a designed spatial-memory mechanism |
| [[2605.21935\|MIF]] | multi-modal interactive fields for humanoid nav | scene field | 94% interaction-pose safety, 0% collision, dynamic scenes | scene-field for *interaction*, not long-range mapless goal-reaching |
| [[2604.24916\|asRoBallet]] | precise base velocity tracking + station-keeping | reactive | 0.05 m/s MAE, 3–5 cm station-keeping | low-level mobility-control precedent, no goal-reaching layer |
| [[2604.02911\|DreamTIP]] | world model the mapless policy can plan through | learned dynamics | 100% vs 10% (52 cm climb), 5 trajectories | the dreaming substrate (feeds B2), not a spatial-memory navigator |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (the mapless-memory advantage is graded by map-friendliness, and joint traversability+memory beats the map → plan → track stack where the map breaks).
1. **H1 — The mapless-memory advantage is graded — near-zero on map-friendly courses, ≥20 pp where the map breaks.**
   - *Prediction*: [[2506.05997|SRU]]'s mapless-minus-mapped SR gap against the [[2405.01792|Wheeled-Legged NavLoco]] map→plan→track incumbent is near-zero on feature-rich static courses (the incumbent's best case) and *widens monotonically* to ≥20 pp as feature density drops, dynamics rise, and drift accumulates — a graded curve, not a constant gain.
   - *Test*: grade courses by map-friendliness (feature density, dynamics, drift); report SRU-minus-Wheeled-Legged-NavLoco SR per grade.
   - *Row*: SRU (mapless memory) vs Wheeled-Legged NavLoco (map → plan → track).
   - *Falsifier*: the gap is constant or shrinks on less-map-friendly terrain → the map isn't the weakest link and learned memory buys nothing the map doesn't.
2. **H2 — Recurrent structure governs spatial retention over horizon.**
   - *Prediction*: [[2506.05997|SRU]]'s spatial-memory structure beats LSTM/GRU more as goal distance grows, because the spatially-enhanced state retains relative-goal information over hundreds of steps where vanilla recurrence forgets.
   - *Test*: ablate memory structure against goal distance on the [[2012.03912|MultiON]] benchmark — the one named suite isolating explicit-map-memory vs implicit-recurrence with controlled task complexity (1-ON → 3-ON ordered goals: OracleMap SR 94%→48% as horizon grows, OracleMap 48% vs NoMap-RNN 10% on 3-ON); report SR vs distance per memory type, treating MultiON as the map-memory-vs-implicit abstraction substrate (photorealistic indoor object-nav with perfect localization, so it backs the memory-horizon axis only, not the legged-terrain coupling).
   - *Row*: SRU (recurrent memory) vs Blind Nav Agents (generic LSTM, emergent map to 1,000 steps); abstraction substrate [[2012.03912|MultiON]].
   - *Falsifier*: SRU ties a generic LSTM ([[2301.13261|Blind Nav Agents]]) at long distances → the explicit spatial enhancement isn't the retention lever, the recurrence alone suffices.
3. **H3 — Posture-conditioned locomotion extends the traversable space.**
   - *Prediction*: [[2604.26504|HiPAN]]'s posture adaptation (crouch, squeeze) extends the traversable space beyond fixed-posture navigation in confined geometry, measurably raising SPL in dead-end/cluttered scenes where a fixed posture gets stuck.
   - *Test*: compare posture-adaptive vs fixed-posture navigation in confined courses; report SPL delta.
   - *Row*: HiPAN (hierarchical posture).
   - *Falsifier*: posture adaptation doesn't raise SPL in confined geometry → fixed posture suffices.
4. **H4 — Joint traversability+trajectory beats a perception-only substrate for cross-embodiment goal-reaching.**
   - *Prediction*: a [[2512.02851|SwarmDiffusion]]-style head that *jointly* infers traversability and generates the trajectory improves cross-embodiment goal-reaching over a perception-only substrate ([[2605.28442|COTRATE]]) plugged into the mapless policy, with zero-shot transfer (Spot→Husky) sometimes beating per-platform continual learning, because joint inference couples where-is-traversable to where-to-go.
   - *Test*: compare SwarmDiffusion-style joint head vs COTRATE-perception-then-plan inside the mapless policy; report cross-embodiment SR + path effort.
   - *Row*: SwarmDiffusion (joint traversability+trajectory) vs COTRATE (perception-only substrate) + SRU (mapless memory).
   - *Falsifier*: the joint head underperforms perception-then-plan → coupling traversability to trajectory adds nothing over a separate perception layer.
5. **H5 — SPL exposes mapless looping the SR number hides, and path conditioning narrows the gap.**
   - *Prediction*: mapless policies without a map risk revisiting dead-ends, so [[2604.26504|HiPAN]]'s SPL drops below SR more on loop-prone courses, exposing inefficiency the SR number alone hides — and adding [[2603.13888|Path-Conditioned Local Planner]]-style global-path conditioning narrows the SPL–SR gap (its SPL 0.82 vs baseline holds even under degraded paths).
   - *Test*: report SPL alongside SR on loop-prone vs open courses, with and without path conditioning.
   - *Row*: Path-Conditioned Local Planner (path-guided) / HiPAN (hierarchical posture) / SRU (mapless memory).
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
| Perceptive online-reference *generation* for vertical/obstacle terrain at parkour-class skill chaining | A1 | [[2502.10363\|BeamDojo]] (the de-facto sparse-foothold humanoid SR-under-disturbance protocol — 91.67% hard Stepping Stones, 4/5 + 5/5 real G1) + [[2504.09997\|GenTe]] (stratifiable 100+ VLM-generated geometric/physical bipedal terrains) are the closest eval substrates; residual hole: no humanoid suite reports SR-at-fixed-FLOPs (H1 compute axis) or multi-obstacle COURSE-chaining SR over unseen skill orderings (H4) — both remain hand-built ([[2604.17335\|G1 WBC-Gen+Track]] is single-obstacle, [[2602.15827\|PHP]] is a fixed skill graph) |
| Physics-feasibility-filtered imitation at fidelity × downstream-RL parity for extreme skills | A2 | [[2602.13656\|KungFuAthlete]] (martial-arts/flip dataset — Side Flip/Air Spin/Backflip, higher-velocity than LAFAN1, tracking + fall-recovery protocol: the missing extreme-skill corpus) + [[2511.17925\|Switch-JustDance]] (standardized cross-controller SR + MPJPE/MPKPE protocol: the shared H1 head-to-head substrate); neither pairs the rejection/feasibility-filter axis with a downstream-RL-trainability curve on the same flip/martial-arts corpus — the unfilled gap is a rejection-stratified fidelity × downstream-RL-parity protocol on KungFuAthlete-class skills ([[2506.12851\|KungfuBot]] filters with no downstream-RL metric, [[2605.06593\|ReActor]] gives downstream but retargets rather than fully filters) |
| Non-periodic fall-recovery from arbitrary configurations across diverse real terrains | A3 | No standardized arbitrary-config getting-up suite exists field-wide (every recovery method rolls its own posture distribution): [[2502.12152\|HUMANUP]] (78.3%/98.3%, 6 terrains, single humanoid — method self-report) + [[2603.20147\|AGILE]] (qualitative stand-up transfer, no arbitrary-config robustness); for the disturbance/push-margin flank the closest real protocol is [[2404.19173\|Single Contact++ RL]] (repeatable impulse-perturbation disturbance recovery on Digit, not ground-up getting-up) and for the no-reset autonomy flank [[2508.16943\|LHM-Humanoid]] (continuous-episode course completion, no induced falls) |
| Embodiment-cost (GRF + acoustic + thermal) *jointly* regulated at full locomotion performance | A4 | No cost-regulation benchmark exists for the heat/noise/GRF triple — every cost number is reported per-method on ad-hoc single-platform setups ([[2604.23702\|QuietWalk]] 7.17 dBA + R²≈0.99 GRF, no thermal; [[2605.27046\|Thermal-Aware Residual]] 70%→<10% overheating, no acoustic/GRF) and the cross-cost thermal-vs-acoustic Pareto front (H5) has never been measured; the closest standardized eval *structure* is [[2310.12567\|Safety-Gymnasium]] (constrained-RL cost-under-bound at task-SR loss) but its cost is a safety-violation cost, not an embodiment cost; [[2403.10506\|HumanoidBench]] backs only the task-SR-loss measurement |
| Flow-vs-Gaussian gait quality + sim-to-real SR stratified by contact multimodality (the H1 core falsifier), and N-fast-iterations-vs-one-slow-PPO-run final gait quality | A5 | [[2403.10506\|HumanoidBench]] (in-sim SR + sample-efficiency + wall-clock across 12 loco skills spanning smooth→contact-rich, but sim-only with no contact-multimodality split) + [[2603.20147\|AGILE]] (motion-quality diagnostics — jerk/accel/joint-limit + 6–25 hr slow-PPO baseline, but a workflow not a contact-stratified SR suite); no standardized benchmark stratifies humanoid locomotion by contact multimodality or reports sim-to-real SR on agile-contact gaits (every method reports ad-hoc ~10-trial real SR) — exactly what makes H1 hard to validate |
| Proprioceptive context-inference architecture matching exteroception across friction × payload × terrain | B1 | [[2602.00678\|RoboGauge]] (proprioceptive quadruped, 10 levels × 7 tasks, terrain × difficulty × domain-randomization sim-to-real metrics — graded but no explicit 80%-body-weight payload sweep) + [[2305.14654\|Barkour]] (standardized quadruped agility/terrain course, time-scored — no payload or context-inference axis) + [[2308.14636\|Linear Impactor]] (calibrated disturbance-rejection protocol — disturbance bandwidth, not payload × terrain conjunction); residual hole: no suite reports the full payload(0→80%) × discontinuous-terrain JOINT surface under a controlled backbone swap ([[2107.04034\|RMA]] 12 kg but TCN fails stairs, [[2212.07740\|TERT]] 60% stairs but no payload-range study) |
| World-model dreaming for few-shot (~5 traj) real adaptation with calibrated epistemic bounding | B2 | No shared/named few-shot real-world legged adaptation benchmark exists (field-acknowledged open problem) — adapted-terrain SR, held-out-terrain SR, and real-data-budget all rest on ad-hoc per-paper protocols ([[2604.02911\|DreamTIP]] 5-traj, 100% vs 10%, no uncertainty bound; [[2409.17992\|LoopSR]]'s 5-terrain set), which is why H1's latent-dreaming-vs-reconstruct-then-retrain falsifier has no common yardstick; the one real benchmark backing a Hypothesis is D4RL (standardized offline-MBRL suite — halfcheetah/hopper/walker2d + RWM-U's Velocity-ANYmal-D/Velocity-G1 tasks) behind H2's epistemic-penalty calibration via [[2504.16680\|RWM-U]] / [[2005.13239\|MOPO]] (D4RL is currently unnamed in the doc and not in KH — ingest candidate) |
| End-to-end mapless locomotion-to-goal with learned spatial memory + cross-platform traversability | B3 | [[2012.03912\|MultiON]] (benchmark — explicit-map vs implicit-memory in goal-reaching, OracleMap 48% vs NoMap-RNN 10% on 3-ON, but indoor object-nav with perfect localization: backs the map-memory-vs-implicit axis only) — NO standardized legged-locomotion-to-goal-over-terrain suite exists that stratifies courses by map-friendliness (feature density / dynamics / drift), so H1's graded curve and H3/H4's confined-geometry + cross-platform terrain axes have no named benchmark ([[2506.05997\|SRU]] is single-platform mapless memory, [[2604.26504\|HiPAN]] posture-adaptive quadruped with no cross-platform) |

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
