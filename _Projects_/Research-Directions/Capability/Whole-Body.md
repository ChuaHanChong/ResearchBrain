---
title: "Promising Research Directions: Whole-Body Coordination — Loco-Manipulation, Mobile Manipulation, Force-Adaptive Control"
aliases:
  - "Whole-Body Coordination Research Directions"
  - "Whole-Body Coordination Promising Directions"
tags:
  - research-directions
  - humanoid
  - manipulation
  - loco-manipulation
  - sim-to-real
---

# Promising Research Directions: Whole-Body Coordination — Loco-Manipulation, Mobile Manipulation, Force-Adaptive Control

> [!abstract] Overview
> Thirteen whole-body-coordination research directions in four clusters: *Whole-Body Loco-Manipulation* (A, coupled arm–leg dynamics), *Mobile Manipulation* (B, nav↔manip coupling), *Force-Adaptive Coordination Under Load* (C), and *Whole-Body Teleoperation & Human-Motion Retargeting* (D). The bars come from ~14 humanoid / loco-manipulation / mobile-manipulation surveys, benchmarks, and frontier systems — [[2604.07993|HEX]], [[2505.06776|FALCON (Loco-Manipulation)]], [[2512.11047|WholeBodyVLA]], [[2602.06341|HiWET]], [[2506.09366|SkillBlender]], [[2503.05652|BRS]], [[2604.07457|CMP]], [[2509.26633|OmniRetarget]].
> 
> This doc covers the *coupling* — the problems that exist only because one body must walk and manipulate at the same time. It is the third of three siblings. [[Manipulation|Manipulation]] owns the arms and hands acting on objects. [[Locomotion|Locomotion]] owns the legs that move the body. This doc owns what links them, and the whole-body-coupling direction is its Cluster A. It points to the mechanism docs ([[WAM|WAM]], [[Sim2Real|Sim2Real]]) rather than re-clustering them.
> 
> Each direction states an explicit **first-principles framing** — the structure of the problem, the assumption it breaks, and the measurable bet — plus a non-consensus thesis aimed at where impactful work goes beyond "more data / more scale." Every number is sourced from a cited `_KnowledgeHub_/{ID}.md` note, never invented.

---

## Methodology

**Scope.** Corpus: ~14 humanoid / loco-manipulation / mobile-manipulation / teleoperation surveys, benchmarks, and frontier systems plus ~40 whole-body method papers from `_KnowledgeHub_/`, cross-checked against [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] and the `Embodied-AI/` deep-dives ([[02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]], [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]], [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]]). The method is survey-grounded ideation: surveys give open problems, benchmarks give what is measurable, frontier systems give what is currently achievable. **Subsystem boundary**: this doc covers the coupling of locomotion and manipulation. A direction is admitted **only if both base/leg motion AND manipulation are essential** — whole-body loco-manipulation, mobile manipulation (moving base + arm together vs nav-then-manipulate), force-adaptive control under external load, and whole-body teleoperation / retargeting. Pure locomotion goes to the Locomotion doc; fixed-base or arm-only manipulation goes to the Manipulation doc; world-model and sim-to-real substrates are cross-referenced, not re-clustered.

- **Survey/benchmark enumeration**: scanning the `{humanoid, robotics, manipulation, imitation-learning, sim-to-real}` tags crossed with `{benchmark, survey}` surfaced [[2403.10506|HumanoidBench]] (whole-body loco + manip suite), [[2505.12748|TeleOpBench]] (30-task dual-arm teleop benchmark), [[2503.05652|BRS]] (real whole-body mobile-manip suite), [[2407.07788|BiGym]] (mobile bimanual benchmark), and [[2603.20147|AGILE]] (workflow) — each read for its open problems and what its evaluation makes measurable.
- **Deep-dive mining**: reads of [[02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02_Dataset-Benchmark-Environment §8]], [[02_Dataset-Benchmark-Environment#1. Cross-Embodiment Scale Datasets|02 §1]], [[09_Contact-Rich-and-Whole-Body-Control#3. Force-Conditioned VLA Architectures|09_Contact-Rich-and-Whole-Body-Control §3]], and [[14_Sim-to-Real-Transfer#3. Policy-Side: Robustness & Domain Randomization|14_Sim-to-Real-Transfer §3]] seeded A1 (coupled dynamics), B1 (joint base-arm), C1 (force adaptation), D1 (retargeting).
- **Closest-baseline anchoring**: each bet is pinned to the strongest existing system it must beat ([[2604.07993|HEX]], [[2506.09366|SkillBlender]], [[2602.06341|HiWET]], [[2503.05652|BRS]], [[2505.06776|FALCON (Loco-Manipulation)]], [[2604.07457|CMP]], [[2509.26633|OmniRetarget]], [[2605.23733|Any2Any]]).
- **Filter (keep generously, gate on quality)**: a direction stays only if it passes all four gates — a distinct sub-problem (not a re-slice of a sibling), a KH-sourced measurable bet, a non-consensus framing, and ≥1 vault anchor. Cluster D was the drop-candidate but survived with three distinct directions: retargeting that preserves *object + scene* contact (D1, unlike Locomotion's pure motion-imitation), teleop + robot-free demos (D2), and cross-embodiment transfer (D3). [[2104.11181|H2O]] is excluded as a miscitation trap — it does interaction *recognition*, not retargeting.
- **First-principles framing**: each direction states the structure of the problem, the assumption it challenges, and the non-consensus bet.

---

## Whole-Body Coordination Survey Landscape

| Survey / Benchmark | Sub-theme | Key open problems |
|---|---|---|
| [[2403.10506\|HumanoidBench]] | A: Whole-body benchmark | Flat RL fails most whole-body loco-manipulation tasks; high-DoF action space is the exploration bottleneck; hierarchical decomposition needed |
| [[2506.09366\|SkillBlender]] | A: Skill composition | Task-specific reward engineering causes reward hacking + unnatural behaviors; high-DoF instability; no reusable primitive substrate |
| [[2603.20147\|AGILE]] | A: Loco-manip workflow | Workflow gap (late env-bug discovery) + transfer gap (fragile hardware deployment); no standardized I/O contract; motion-quality diagnostics missing |
| [[2602.06341\|HiWET]] | A: World-frame tracking | Robot-centric control accumulates world-frame drift; aggressive arm motion destabilizes gait; base must actively transport to extend workspace |
| [[2503.05652\|BRS]] | B: Mobile manipulation | High-DoF mobile manipulators amplify end-effector drift + OOD states + safety violations; teleop interfaces cause embodiment mismatch; whole-body action modeling unsolved |
| [[2407.07788\|BiGym]] | B: Mobile bimanual | Long-horizon multi-object mobile bimanual; demo-driven; IL/RL near-0% on long sequences + stacking |
| [[2306.11565\|HomeRobot]] | B: Open-vocab mobile manip | Open-vocab perception is the bottleneck (5–15% → 0.4–0.6% SR with real detector); skill-perception integration brittle |
| [[2505.06776\|FALCON (Loco-Manipulation)]] | C: Force-adaptive | Whole-body control under dynamic 3D end-effector forces; kinematically-limited force compensation; entangled whole-body objectives |
| [[2512.01061\|Sim-to-Real Door]] | C: Contact-rich force | Vision-only zero-shot sim-to-real for forceful contact; partial observability; no depth / object-centric features / motion primitives |
| [[2604.07457\|CMP]] | C: Safety under disturbance | Whole-body tracking collapses under OOD geometry / sensor noise; need best-effort continuation, not hard failure; low-latency safety filtering |
| [[2505.12748\|TeleOpBench]] | D: Teleoperation benchmark | Teleop evaluation couples hardware + software + tasks, blocking cross-method comparison; no shared simulator-centric platform; interface modality trade-offs unquantified |
| [[2509.26633\|OmniRetarget]] | D: Interaction-preserving retargeting | Retargeting destroys human–object–scene interaction; foot-skating + penetration; downstream-RL trainability tied to reference quality |
| [[2412.17730\|Mimicking-Bench]] | D: Humanoid-scene interaction | No large-scale human-demo benchmark for scene-geometry generalization; small manual demos limit study; precise hand control unsolved even with human data |
| [[2602.10106\|EgoHumanoid]] | D: Robot-free demonstration | Loco-manip bottlenecked by teleop data cost; human–humanoid embodiment gap; lab-confined collection blocks real-world generalization |
| [[2510.08807\|Humanoid Everyday]] | D: Open-world humanoid dataset | Existing datasets are stationary-arm-centric; humanoid sets neglect full-body locomotion + human-humanoid interaction; no standardized loco-manip eval — SOTA IL hits 0% on hard loco-manip |
| [[2605.23733\|Any2Any]] | D: Cross-embodiment transfer | Whole-body-tracking policies are per-platform; retraining from scratch is data/compute-expensive; kinematic alignment across humanoids unsolved |

> [!tip] Convergence patterns
> - **The coupling, not either subsystem, is the bottleneck** (5-way): [[2602.06341|HiWET]] (aggressive arm motion destabilizes gait), [[2505.06776|FALCON (Loco-Manipulation)]] (entangled whole-body objectives under force), [[2503.05652|BRS]] (high-DoF mobile manipulators amplify end-effector drift), [[2604.07993|HEX]] (treating body parts independently yields unstable behavior), [[2512.11047|WholeBodyVLA]] ("decision-execution misalignment" between intent and loco control) — one diagnosis in five vocabularies: a humanoid is not an arm bolted to legs, and the arm–leg / base–arm coupling is the term a part-wise policy throws away. Confirmed by [[2604.07993|HEX]] (79.8% ID / 61.8% OOD beating part-wise GR00T N1.5 at 70.2% / 41.0%) and [[2602.06341|HiWET]]'s active base-modulation (12.4 mm world-frame error).
> - **The action target must be feasible before the policy can use it** (4-way): [[2509.26633|OmniRetarget]] (near-zero penetration, zero foot-skating → 82.20–94.73% downstream RL), [[2606.03476|Human2Humanoid]] (0.05 cm penetration, 88.5% SR), [[2603.22201|NMR]] (54% self-collision reduction, zero joint jumps), [[2604.00202|DreamControl-v2]] (68% valid trajectories vs 8% → 0.925 vs 0.101 downstream RL) — human-motion references violate the robot's torque/contact/balance constraints and must be projected onto the feasible manifold before imitation, inverting the "collect more demonstrations" reflex.
> - **Decompose into reusable structure, don't monolithically scale** (4-way): [[2506.09366|SkillBlender]] (per-joint blend of frozen skills; avoids reward hacking), [[2505.06776|FALCON (Loco-Manipulation)]] (dual-agent lower/upper; faster convergence than monolithic RL), [[2602.06341|HiWET]] (Commander/Tracker hierarchy), [[2503.05652|BRS]] (autoregressive base → torso → arm) — the field is moving to structured decomposition over monolithic end-to-end policies, because the coupled high-DoF action space is where flat RL fails.
> - **Human video is the scalable substrate, if the embodiment gap is bridged** (4-way): [[2602.10106|EgoHumanoid]] (robot-free egocentric demos co-trained with robot data; +19 pp in-domain, +51 pp generalization), [[2512.11047|WholeBodyVLA]] (action-free egocentric video pretraining; +38.7%), [[2605.20373|SUGAR]] (32.7%→76.0% data scaling), [[2605.03452|BifrostUMI]] (robot-free UMI demos → whole-body humanoid) — human video is the route past the teleop-data wall, given a human-to-humanoid alignment pipeline that bridges the embodiment gap.

---

## Formal Framing

**The whole-body coupled-dynamics object.** A whole-body system carries a configuration $q = (q_{\text{base}}, q_{\text{leg}}, q_{\text{arm}}, q_{\text{hand}})$ on a single floating base. Its dynamics couple every subsystem through the shared inertia matrix and the external-wrench Jacobian:

$$\ddot q = M(q)^{-1}\!\left(\tau - C(q,\dot q)\,\dot q - g(q) + J_{\text{ext}}^{\top} F_{\text{ext}}\right)$$

The coupling is structural: $M(q)$ is **not block-diagonal** across (base, leg, arm). An arm acceleration induces a base/leg reaction torque (the off-diagonal $M_{\text{arm,leg}}$ term), and an external hand wrench $F_{\text{ext}}$ propagates through $J_{\text{ext}}^{\top}$ to *every* joint, including the legs that keep the centre-of-mass over the support polygon. So a part-wise policy that factors $\pi = (\pi_{\text{leg}}, \pi_{\text{arm}})$ with independent value $V(a_{\text{leg}}) + V(a_{\text{arm}})$ throws away the load-bearing cross-term — the central reframing of Cluster A.

Three coupling formalisms organize this doc:

| Object | Formalism | Cluster |
|---|---|---|
| **Arm-as-disturbance** | An arm command $a_{\text{arm}}$ injects a reaction $\delta_{\text{base}} = M_{\text{base,arm}}\,\ddot q_{\text{arm}}$ the leg policy must reject *anticipatorily*; the whole-body value is non-separable across subsystems | A |
| **Base-as-manipulation-DoF** | The mobile-manipulation action is a joint $a = (a_{\text{base}}, a_{\text{arm}}) \sim \pi(a \mid o, l)$ where base velocity is a *manipulation* degree of freedom — repositioning extends the reachable workspace mid-task, not before it | B |
| **External wrench under load** | A payload / contact force $F_{\text{ext}}$ at the hand sets a whole-body equilibrium constraint $J_{\text{ext}}^{\top} F_{\text{ext}} + g(q) \in$ feasible-torque $\times$ support-polygon; the legs compensate for what the arms feel | C |

**The mobile-manipulation joint action distribution** — [[2503.05652|BRS]]:

> "WB-VIMA … employs autoregressive whole-body action decoding and multi-modal observation attention to learn coordinated and safe actions … predicting mobile base, torso, and arm movements hierarchically … essential for mitigating error propagation and achieving coordinated movements in high-DoF mobile manipulators." — [[2503.05652|BRS]]

The mobile-manipulation action is a single joint $p(a_{\text{base}}, a_{\text{torso}}, a_{\text{arm}} \mid o)$, and its factoring is *not* arbitrary: BRS shows the order base → torso → arm (each action conditioned on the chosen upstream action) mitigates the drift an independent factorization amplifies. This is the formal content of "base is a manipulation DoF" — the base action is the *condition* the arm action is drawn under, not a separate phase. B1 builds on this.

**Skill-blending as a feasibility-preserving composition** — [[2506.09366|SkillBlender]]:

> "A high-level controller learns to blend these frozen primitive skills for complex tasks by outputting subgoals and novel per-joint weight vectors … the final action is a weighted sum of primitive actions, where weights are determined per-joint and normalized by a softmax … crucial for preventing reward hacking and maintaining motion feasibility." — [[2506.09366|SkillBlender]]

Composing whole-body behavior as a per-joint softmax-weighted blend of frozen feasible primitives $a = \sum_k w_k(q)\,\pi_k^{\text{prim}}(q)$ confines the action to the convex hull of those primitives — which is *why* it resists reward hacking without per-task reward tuning. This is the inverse of monolithic RL, which must rediscover feasibility from scratch on every task. A2 builds on this.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Whole-Body Loco-Manipulation** | A1, A2, A3, A4 | The arm–leg coupling is non-separable: an arm reach is a balance disturbance the legs must anticipate, and flat RL fails on the coupled high-DoF action space | **A1 is the lead** — it makes the arm→leg coupling an *explicit* predicted quantity ([[2604.07993\|HEX]]'s ablation: removing the coupling architecture costs −5/12 on Pouring, the largest single-component drop, vs +1/12 for its 12M-frame pretraining). **A4's unified-latent interface is the high-level command surface that grounds into A1's coupling**, drawing on Cluster D's demos for breadth. A1's predictor is the balance model A2's blended skills and A3's tracker both need; A3's active base is the workspace-extension A4 commands. [[2604.07993\|HEX]] and [[2506.09366\|SkillBlender]] set the bar for A1 and A2 |
| **B — Mobile Manipulation (Nav↔Manip Coupling)** | B1, B2, B3 | The base velocity is a manipulation DoF; nav-then-manipulate discards the in-task repositioning that extends the workspace | B1's joint base-arm policy is the action substrate B2's active perception and B3's memory both ride on; B2's where-to-look decision feeds the observation B3 must remember. [[2503.05652\|BRS]] and [[2401.02117\|Mobile ALOHA]] set the bar for B1 |
| **C — Force-Adaptive Coordination Under Load** | C1, C2 | An external hand wrench propagates through the kinematic chain to the support polygon; the legs compensate for what the arms feel, and the task reward omits the force | C1's force-adaptive policy is the performance layer C2 bounds with safety; C2's CBF/QP filter is the guarantee C1's learned compensation lacks. Both share the external-wrench formalism and the anchors [[2505.06776\|FALCON (Loco-Manipulation)]] (0.37 vs 0.60) and [[2604.07457\|CMP]] (86.7% extreme-OOD) |
| **D — Whole-Body Teleoperation & Human-Motion Retargeting** | D1, D2, D3, D4 | The data wall — demonstrations of *coupled* loco-manipulation are scarce, embodiment-mismatched, and per-platform | **D2 is the breadth substrate**: coupled demos buy generalization breadth ([[2602.10106\|EgoHumanoid]]'s +51 pp) that explicit coupling on fixed data cannot manufacture, but on a fixed budget the architecture is the lever — so D2 *complements* Cluster A, it doesn't stand upstream of it. **D4 attacks the same wall from the other side** — synthesizing coupled demos ([[2605.27724\|HumanoidMimicGen]]'s 0.89 vs 0.33, [[2606.05160\|GRAIL]]'s 20,000+ from assets) instead of capturing them, removing the per-demo human D2 still needs. D1's interaction-preserving retargeting is the feasible reference D2/D4 and A1–A4 all consume; D3 amortizes whatever D1/D2/D4 produce across bodies. [[2509.26633\|OmniRetarget]] and [[2605.23733\|Any2Any]]'s ~1%-compute transfer are the shared levers |

---

## Cluster A — Whole-Body Loco-Manipulation

*Coupled arm–leg dynamics on a single floating base — where an arm reach is a balance disturbance, the whole-body value is non-separable, and flat RL fails on the coupled high-DoF action space.*

### A1 — Coupled-Dynamics Whole-Body Action Models

| | |
|---|---|
| **Cluster** | A — Whole-Body Loco-Manipulation |
| **Thesis** | Build a whole-body policy that predicts the base/leg reaction an arm reach induces, instead of treating the body parts independently. The reason it must work: the inertia matrix $M(q)$ is non-block-diagonal, so an arm acceleration *is* a leg-balance disturbance. The field assumes you can bolt an arm policy onto a leg policy. The bet: a coupling-aware predictor beats part-wise control by the [[2604.07993\|HEX]] margin (79.8% ID / 61.8% OOD vs GR00T N1.5's 70.2% / 41.0%) and cuts upper-body tracking error toward [[2505.06776\|FALCON (Loco-Manipulation)]]'s 0.37 (vs 0.60 monolithic). |
| **Anchor surveys** | [[2403.10506\|HumanoidBench]], [[2603.20147\|AGILE]], [[2602.06341\|HiWET]] |
| **Key targets** | [[2604.07993\|HEX]] 79.8% ID (7 tasks) / 61.8% OOD (8 scene-variation) vs GR00T N1.5 70.2% / 41.0% and π0.5 OOD 44.3%, 100% initial + 53.3% Place-Box on long-horizon box-convey; [[2505.06776\|FALCON (Loco-Manipulation)]] 0.37 vs 0.60 upper-body tracking error under large force (~2× over best baseline), 100 N cart-pull + 1.2 kg/hand payload; [[2602.06341\|HiWET]] 12.4 mm world-frame end-effector error compensating base disturbance |

**Why it matters.** The dominant recipe treats a humanoid's body parts independently, and it produces "uncoordinated and unstable behaviors on high-DoF humanoid platforms," as [[2604.07993|HEX]] diagnoses. The cause is the dynamics, not the data: $M(q)$ is non-block-diagonal, so an arm acceleration injects a reaction torque on the base and legs, and a policy that doesn't model this can only *react* to the balance error after it appears. [[2604.07993|HEX]]'s answer is a structured-proprioceptive Mixture-of-Experts that models the cross-body dependencies explicitly, plus a review-and-forecast scheme that predicts future proprioceptive state — lifting in-distribution success to 79.8% (vs GR00T N1.5 at 70.2%) and, more tellingly, OOD to 61.8% (vs 41.0%), where the coupling matters most. [[2505.06776|FALCON (Loco-Manipulation)]] adds the force angle: jointly-trained lower/upper agents with shared proprioception cut upper-body tracking error to 0.37 under large forces, ~2× better than a monolithic baseline's 0.60. [[2602.06341|HiWET]] closes the loop on precision: a hierarchical world-frame tracker modulates the base to compensate locomotion oscillation, reaching 12.4 mm end-effector error. The move: make the reaction the arm induces on the base a predicted quantity the policy plans against, not a disturbance it rejects after the fact.

**First-principles framing.**
- **First principle**: The inertia matrix $M(q)$ is non-block-diagonal — in plain terms, the arm, the legs, and the base are mechanically linked, so by the equations of motion an arm acceleration *is* a reaction torque on the base and legs. This link holds no matter what the policy was trained on. So the value of a whole-body action can't be split into an arm part plus a leg part — they have to be scored together.
- **Assumption being challenged**: That a humanoid policy can split into an arm policy plus a leg/balance policy. Part-wise baselines ([[2604.07993|HEX]] beats GR00T N1.5, ACT, π0.5) bet on this; the 41.0%→61.8% OOD gap is the cost of ignoring the cross-body link, and more per-part data cannot recover it — the missing information is in the coupling, not the parts.
- **The bet**: A coupling-aware predictor beats part-wise control by the [[2604.07993|HEX]] margin (79.8% ID / 61.8% OOD vs 70.2% / 41.0%), with the gap widening under OOD and long-horizon, and cuts upper-body tracking error toward [[2505.06776|FALCON (Loco-Manipulation)]]'s 0.37 (vs 0.60 monolithic) — coordination from the coupling, not more demonstrations.

**Evidence.**
- [[2604.07993|HEX]] — Structured-proprioceptive MoE (Unified Proprioceptive Predictor) + review-and-forecast; 79.8% ID / 61.8% OOD vs GR00T N1.5 70.2% / 41.0%, 12M-frame humanoid pretraining; the coupling-aware-policy anchor.
- [[2505.06776|FALCON (Loco-Manipulation)]] — Dual-agent lower/upper RL with shared proprioception + torque-limit-aware force curriculum; 0.37 vs 0.60 tracking error under force, 100 N cart, 1.2 kg/hand; the force-coupled decomposition anchor.
- [[2602.06341|HiWET]] — Commander/Tracker hierarchy + Kinematic Manifold Prior; 12.4 mm world-frame error, actively modulates base to compensate base disturbance; the precision-under-coupling anchor.
- [[2512.11047|WholeBodyVLA]] — Unified latent policy jointly predicting loco + manip latents; 78.0%, names "decision-execution misalignment" as the coupling failure mode (feeds A4).
- [[2605.21133|Spatial Brain Cerebellum]] — Active-spatial-brain + action-cerebellum with end-effector-reachable-space solver; 60.0% vs 0% OOD-hard; the reachable-workspace-aware coupling complement.
- [[2605.14417|DAJI]] — Joint-intent latent that anticipates coming support shifts + momentum to prepare early; 94.42% rollout SR, 4.71 ms; the anticipatory angle on the coupling (feeds A4).

**Concrete research questions.**
1. **Q1 — Explicit coupling term vs implicit.** Add an explicit predicted base-reaction $\hat\delta_{\text{base}} = \hat M_{\text{base,arm}}\ddot q_{\text{arm}}$ as input/auxiliary loss vs [[2604.07993|HEX]]'s implicit MoE — does it widen the 41.0%→61.8% OOD margin, and does the gain concentrate on fast arm motions where the reaction is largest?
2. **Q2 — Forecast horizon vs balance margin.** Sweep [[2604.07993|HEX]]'s review-and-forecast horizon against post-reach balance recovery — what horizon maximizes anticipatory compensation before prediction drift hurts?
3. **Q3 — Shared vs separate proprioception across agents.** Ablate [[2505.06776|FALCON (Loco-Manipulation)]]'s shared whole-body proprioception vs siloed — is mutual awareness the mechanism behind the 0.60→0.37 error drop?
4. **Q4 — Coupling-aware tracking at world-frame precision.** Combine [[2602.06341|HiWET]]'s Commander/Tracker with an explicit coupling predictor — can base-modulation plus coupling-anticipation push world-frame error below 12.4 mm under aggressive reaches?

**Related research papers.**
- [[2604.07993|HEX]] — Cross-embodiment whole-body manipulation via structured-proprioceptive MoE; 79.8%/61.8%; the anchor.
- [[2505.06776|FALCON (Loco-Manipulation)]] — Force-adaptive dual-agent loco-manipulation; 0.37 vs 0.60; the force-coupled decomposition (also Cluster C).
- [[2602.06341|HiWET]] — World-frame end-effector tracking with base-disturbance compensation; 12.4 mm; precision-under-coupling.
- [[2512.11047|WholeBodyVLA]] — Unified latent loco-manip policy; 78.0%; decision-execution-misalignment framing (feeds A4).
- [[2605.21133|Spatial Brain Cerebellum]] — Active spatial brain + reachable-space-aware action cerebellum; 60.0% vs 0% OOD-hard.
- [[2502.14795|Humanoid-VLA]] — First humanoid policy, egocentric vision + goal-conditioned RL; <40 mm position error, 10/10 turn-to-object; the egocentric-coupling precedent.
- [[2507.06905|ULC]] — One unified policy for locomotion + 3-DoF torso + dual-arm; beats decoupled and hierarchical designs; unified-coordination-beats-decoupled (feeds A4).
- [[2603.12263|Psi0]] — Open foundation model for universal humanoid loco-manipulation; >40% over GR00T N1.6 across 8 long-horizon tasks; the foundation-scale coupling reference.
- [[2605.14417|DAJI]] — 64D latent that predicts the body's reaction (support shifts, momentum) *before it moves*; 94.42% rollout SR; the anticipatory-coupling complement (feeds A4).
- [[2604.07457|CMP]] — Competence-manifold-projection whole-body tracking robust to OOD; 86.7% extreme OOD real; the robustness layer (feeds C2).

**Benchmarks & metrics.**
- [[2604.07993|HEX]] — 7 ID + 8 OOD real-robot tasks; 79.8% / 61.8% vs GR00T N1.5 70.2% / 41.0%, 100% initial + 53.3% Place-Box long-horizon; the coupling-vs-part-wise metric.
- [[2505.06776|FALCON (Loco-Manipulation)]] — Upper-body tracking error under large force 0.37 vs 0.60, 100 N cart + 1.2 kg payload on G1/T1; the force-coupled-tracking metric.
- [[2403.10506|HumanoidBench]] — 27-task whole-body suite (locomotion + manipulation) on H1; flat RL fails, hierarchical helps; the coupled-action-space difficulty gradient.

> [!warning] Risks
> - **Coupling model needs an accurate inertia model** — predicting $M_{\text{base,arm}}$ depends on the URDF/mass distribution. → Treat the coupling predictor as learned-residual over a nominal model; report sim-vs-real coupling-prediction error, and lean on [[2604.07993|HEX]]'s learned MoE where analytic terms are uncertain.
> - **Gains may be platform-specific** — 79.8%/61.8% is on one humanoid. → Q1/Q4 test across reach speeds and at world-frame precision; report the margin by motion-aggressiveness class, not a single average ([[2604.07993|HEX]] is already cross-embodiment-pretrained).
> - **Explicit coupling adds latency** — predicting the reaction must fit the control loop. → Bound the predictor to the [[2602.06341|HiWET]]-class real-time budget; if explicit coupling can't fit, fall back to HEX's implicit MoE and report the latency–accuracy trade.

### A2 — Skill-Blending vs Monolithic Whole-Body Control

| | |
|---|---|
| **Cluster** | A — Whole-Body Loco-Manipulation |
| **Thesis** | Compose whole-body loco-manipulation as a per-joint blend of *frozen, individually-feasible* primitive skills, not as one monolithic policy retrained per task. The reason it must work: a softmax-weighted blend stays in the feasible convex hull, so feasibility and reward-hacking-avoidance come for free. The field assumes whole-body competence needs per-task reward engineering on a monolith. The bet: a skill-blending controller matches [[2506.09366\|SkillBlender]]'s outperformance on all 8 loco-manip tasks across 3 embodiments (H1/G1/H1-2) with zero per-task reward tuning while a monolithic baseline reward-hacks, and lifts downstream RL toward [[2604.00202\|DreamControl-v2]]'s 0.925 (vs 0.101 zero-shot). |
| **Anchor surveys** | [[2403.10506\|HumanoidBench]], [[2506.09366\|SkillBlender]], [[2603.20147\|AGILE]] |
| **Key targets** | [[2506.09366\|SkillBlender]] consistently outperforms vanilla-RL + hierarchical baselines across 8 loco-manip tasks (3 embodiments H1/G1/H1-2, 4 primitive skills) while avoiding reward hacking; [[2604.00202\|DreamControl-v2]] RL success 0.925 vs 0.101 zero-shot on complex Group-1, 68% valid-trajectory rate vs 8%, 8 real G1 skills; [[2602.06341\|HiWET]] Kinematic-Manifold-Prior halves hand error as the primitive-prior precedent |

**Why it matters.** The reflexive recipe for a new whole-body task is "tune the reward until the monolithic policy does it." [[2506.09366|SkillBlender]] diagnoses why this won't scale: task-specific reward engineering "leads to reward hacking and unnatural behaviors," and a high-DoF monolith must rediscover feasibility from scratch every time. Its answer is structural: pretrain goal-conditioned primitives (walking, reaching, squatting, stepping) once, freeze them, then learn a controller that blends them with *per-joint* softmax weights. The action is a convex combination of feasible primitives, so it stays in their feasible hull — which is *why* the softmax "is crucial for preventing reward hacking and maintaining motion feasibility," and why SkillBlender outperforms vanilla-RL and hierarchical baselines on all 8 SkillBench tasks across three Unitree embodiments without per-task reward surgery. [[2604.00202|DreamControl-v2]] adds the feasible-prior case: a pre-retargeting diffusion prior yields 68% valid trajectories (vs 8% for inference-time calibration) and lifts downstream RL to 0.925 (vs 0.101 zero-shot) across 8 real G1 skills. [[2606.03536|Bionic Whole-Body Control]] generalizes the feasible-prior idea to expressive motion: a physics-aware latent diffusion model with contact-consistency and temporal-smoothness regularizers generates *physically-executable* style-transferred references (lowest foot-sliding 0.004722 m/frame), then a cluster-and-distill RL tracker executes them without per-style retraining — 96.0% hardware success across 125 trials on a real G1. [[2606.06139|MotionDisco]] takes the demonstration-free route: an LLM-guided evolutionary search over discrete contact plans coupled to a kinodynamic optimizer *discovers* feasible whole-body motions (no demos, no per-task reward), solving all 8 long-horizon scenarios and deploying zero-shot to real hardware. The claim: whole-body competence is a *composition* problem over feasible primitives and references, not a reward-tuning problem on a monolith — fix the substrate (frozen primitives, feasible diffusion priors, or planner-discovered motions) and the blend, and per-task reward engineering disappears.

**First-principles framing.**
- **First principle**: If you blend frozen, individually-feasible primitive skills with softmax weights, the blended action is a weighted average that never leaves the set the primitives span — so any mix of feasible skills stays feasible, for free, with no per-task feasibility reward. Feasibility comes from *how you combine the skills*, not from per-task tuning.
- **Assumption being challenged**: That whole-body competence needs task-specific reward engineering on a monolith. [[2506.09366|SkillBlender]]'s reward-hacking diagnosis shows the binding constraint is *feasibility-preserving composition*, not reward design — a monolith without the primitive substrate rediscovers feasibility and hacks the reward to do it.
- **The bet**: A skill-blending controller matches [[2506.09366|SkillBlender]]'s outperformance of vanilla-RL + hierarchical baselines on all 8 loco-manip tasks across 3 embodiments with zero per-task reward tuning while a monolith reward-hacks, and lifts downstream RL toward [[2604.00202|DreamControl-v2]]'s 0.925 (vs 0.101) — competence from composition, not reward surgery.

**Evidence.**
- [[2506.09366|SkillBlender]] — Hierarchical RL blending frozen primitives with per-joint softmax weights; outperforms all baselines on 8 SkillBench tasks across H1/G1/H1-2 while avoiding reward hacking; the skill-blending anchor.
- [[2604.00202|DreamControl-v2]] — Trainable guided diffusion priors + pre-retargeting; 0.925 vs 0.101 RL, 68% vs 8% valid trajectories, 8 real G1 skills; the feasible-prior anchor.
- [[2602.06341|HiWET]] — Kinematic Manifold Prior halves hand error by constraining the action to a kinematically-consistent manifold; the primitive-prior-as-feasibility precedent.
- [[2606.03536|Bionic Whole-Body Control]] — Physics-aware latent diffusion (contact + smoothness regularizers) generating physically-executable references + cluster-and-distill RL tracker; 96.0% hardware; the feasible-reference-via-diffusion anchor.
- [[2606.06139|MotionDisco]] — Discovers feasible whole-body motion demonstration-free via LLM-guided evolutionary contact-plan search + kinodynamic optimization; 8/8 long-horizon, zero-shot real; the planner-discovered-motion evidence (also D4).
- [[2505.06776|FALCON (Loco-Manipulation)]] — Decomposed lower/upper agents converge faster than monolithic whole-body RL; the decomposition-beats-monolith evidence.
- [[2604.24833|MotionBricks]] — Modular latent generative model with smart primitives for scalable real-time motion; the modular-primitive composition analogue.
- [[2506.12851|KungfuBot]] — Filters raw mocap into physically-feasible references + adaptive-tracking RL; 53.25 mm vs >233 mm baselines; feasibility-first imitation (fix the reference, not the reward).
- [[2405.18418|Puppeteer]] — Hierarchical world model splitting visual whole-body control into a frozen tracker + high-level commander; 97.8% naturalness; hierarchical-decomposition-over-monolith.

**Concrete research questions.**
1. **Q1 — Per-joint vs scalar blending.** Ablate [[2506.09366|SkillBlender]]'s per-joint weights against scalar per-skill weighting — does per-joint resolution deliver the coordination, and where does scalar break (e.g., reach-while-stepping)?
2. **Q2 — Softmax convex-hull vs unconstrained blend.** Remove the softmax normalization — does the reward-hacking [[2506.09366|SkillBlender]] reports re-appear, confirming convex-hull confinement is the feasibility mechanism?
3. **Q3 — Primitive-library coverage vs task breadth.** Sweep the number of frozen primitives (beyond the 4 SkillBench skills) against composable-task breadth — what set spans the loco-manip task space, and do learned vs hand-designed primitives differ?
4. **Q4 — Blended skills as feasible RL references.** Use the blended-skill output as the downstream-RL reference (à la [[2604.00202|DreamControl-v2]]'s pre-retargeting or [[2606.03536|Bionic Whole-Body Control]]'s physics-aware diffusion prior) — does it raise the valid-trajectory rate toward 68%+ and RL toward 0.925, and does generating *feasible* references up front beat inference-time feasibility repair?

**Related research papers.**
- [[2506.09366|SkillBlender]] — Per-joint softmax skill-blending of frozen primitives; 8 tasks / 3 embodiments, avoids reward hacking; the anchor.
- [[2604.00202|DreamControl-v2]] — Guided-diffusion feasible priors + pre-retargeting; 0.925 vs 0.101 RL; the feasible-prior anchor.
- [[2602.06341|HiWET]] — Kinematic-Manifold-Prior feasibility; halves hand error; primitive-prior precedent.
- [[2606.03536|Bionic Whole-Body Control]] — Physics-aware diffusion feasible references + RL tracker; 96.0% hardware; feasible-reference-via-diffusion anchor.
- [[2606.06139|MotionDisco]] — Demonstration-free LLM-evolutionary motion discovery + kinodynamic optimization; 8/8 long-horizon, zero-shot real; planner-discovered-feasible-motion (also D4).
- [[2604.01158|SMASH]] — Whole-body striking skill from motion-prior-augmented mocap + motion-matching RL; 93.7% contact / 59.7% return; the motion-prior-regularized skill analogue.
- [[2604.24833|MotionBricks]] — Modular latent primitives for real-time motion; modular-composition analogue.
- [[2604.11251|CLAW]] — Composable language-annotated whole-body motion generation; language-driven composition of whole-body motion primitives.
- [[2506.12851|KungfuBot]] — Filters raw video into physically-feasible references + adaptive-tracking RL; 53.25 mm vs >233 mm baselines; the feasibility-filtering-before-imitation complement.
- [[2505.06776|FALCON (Loco-Manipulation)]] — Decomposed agents beat monolithic RL convergence; decomposition evidence.
- [[2504.11054|Meta Motivo]] — Behavioral foundation model (FB-CPR) for zero-shot whole-body control; natural motion without per-task reward; the reusable-substrate analogue to frozen primitives.
- [[2405.18418|Puppeteer]] — Hierarchical world model (frozen tracker + high-level agent) for 56-DoF visual whole-body control; 97.8% naturalness, zero-shot to 3× larger gaps; the hierarchical-decomposition complement.
- [[2403.10506|HumanoidBench]] — Whole-body benchmark where flat/monolithic RL fails and hierarchy helps; the monolith-failure framing.
- [[2603.20147|AGILE]] — Loco-manip workflow with motion-quality (jerk/limit) diagnostics; the feasibility-diagnostics substrate for blended skills.

**Benchmarks & metrics.**
- [[2506.09366|SkillBlender]] / SkillBench — 8 loco-manip tasks on 3 embodiments (H1/G1/H1-2), accuracy + feasibility metrics; outperforms all baselines while avoiding reward hacking; the composition-vs-monolith metric.
- [[2604.00202|DreamControl-v2]] — 0.925 vs 0.101 RL success (Group-1), 68% vs 8% valid trajectories, 8 real G1 skills; the feasible-prior-to-RL metric.
- [[2606.03536|Bionic Whole-Body Control]] — 96.0% hardware success (125 trials, real G1), 96.02% sim closed-loop, foot-sliding 0.004722 m/frame; the physically-executable-reference metric.
- [[2403.10506|HumanoidBench]] — Whole-body locomotion + manipulation tasks; flat-RL failure rate; the monolith-difficulty diagnostic.

> [!warning] Risks
> - **Frozen primitives cap the achievable behavior** — a behavior outside the primitive hull is unreachable by blending. → Allow a learned residual outside the convex hull for novel skills (couples to A1's coupling residual); report the fraction of tasks needing residual vs pure blend.
> - **Primitive library design is itself engineering** — picking the right primitives replaces reward tuning with primitive design. → Q3 tests learned vs hand-designed primitives; the win is amortization across many tasks, so report tasks-per-primitive-set, not single-task SR.
> - **Blending may produce discontinuous transitions** — switching weights mid-motion can jerk. → [[2506.09366|SkillBlender]]'s softmax smooths weights; report motion-quality (jerk/limit) diagnostics per [[2603.20147|AGILE]], treat smoothness as first-class.

### A3 — World-Frame End-Effector Tracking with the Base as an Active DoF

| | |
|---|---|
| **Cluster** | A — Whole-Body Loco-Manipulation |
| **Thesis** | Formulate loco-manipulation as world-frame end-effector tracking where the base is an *actively-commanded* transport DoF, not a robot-centric controller that drifts. The reason it must work: a task target lives in the world frame, but a robot-centric policy folds base motion into cumulative drift, so long-horizon precision needs the loop closed in world coordinates and the base used to extend reach. The field assumes body-centric control suffices for task-space precision. The bet: a world-frame Commander/Tracker hierarchy holds [[2602.06341\|HiWET]]'s 12.4 mm sim / 12–15 mm real end-effector error over long horizons by actively modulating the base, where body-centric control accumulates drift. |
| **Anchor surveys** | [[2602.06341\|HiWET]], [[2403.10506\|HumanoidBench]], [[2603.20147\|AGILE]] |
| **Key targets** | [[2602.06341\|HiWET]] 12.4 mm sim / 12–15 mm real world-frame end-effector RMSE, Kinematic-Manifold-Prior halves hand error, active base + waist modulation to extend reachable workspace; [[2603.03279\|ULTRA]] 73% dense-reference tracking + 50–90% sparse-goal real G1, RL finetuning +200% OOD position-only; [[2503.05652\|BRS]] 88% sub-task via autoregressive base→torso→arm decoding as the drift-mitigation precedent |

**Why it matters.** When a humanoid places a hand precisely while walking, the target is in the *world frame*, but most command-driven controllers are *robot-centric* — which, as [[2602.06341|HiWET]] documents, "leads to cumulative world-frame drift and high-frequency oscillations in end-effector precision during humanoid locomotion." Worse, a static reachable workspace is too small for many tasks: the base must *actively transport* the target into reach, so base motion is part of the manipulation, not a separate navigation phase. [[2602.06341|HiWET]]'s solution decouples a world-frame Commander (global reasoning) from a whole-body Tracker (execution), with a Kinematic Manifold Prior that halves hand error by holding the upper body to consistent configurations — reaching 12.4 mm in sim and 12–15 mm on a real G1 while modulating base and waist for reachability. [[2603.03279|ULTRA]] pushes the multimodal version: physics-driven retargeting + RL finetuning lifts OOD goal-following up to 200% (position-only) and transfers to 73% dense / 50–90% sparse on a real G1. The move: close the loop in world coordinates and treat the base as an active DoF that extends the workspace, not a source of drift to suppress.

**First-principles framing.**
- **First principle**: A manipulation target is in the world frame; a robot-centric controller folds the floating base's motion into the end-effector estimate, so error accumulates with locomotion distance. World-frame closure is the only formulation where precision is decoupled from how far the base has walked — and the mobile base is the DoF that brings out-of-static-reach targets into reach.
- **Assumption being challenged**: That body-centric whole-body control suffices for task-space precision. Body-centric baselines ([[2602.06341|HiWET]] beats them) bet on this; the world-frame drift HiWET measures is a *frame* problem, not a capacity problem, so scaling the body-centric policy cannot fix it.
- **The bet**: A world-frame Commander/Tracker hierarchy holds [[2602.06341|HiWET]]'s 12.4 mm sim / 12–15 mm real error over long horizons by actively modulating the base, where a matched body-centric controller drifts with locomotion distance — precision from world-frame closure + active base transport, not a bigger policy.

**Evidence.**
- [[2602.06341|HiWET]] — World-frame Commander/Tracker + Kinematic Manifold Prior; 12.4 mm sim / 12–15 mm real, active base + waist modulation; the world-frame-tracking anchor.
- [[2603.03279|ULTRA]] — Unified multimodal control + physics-driven retargeting + RL finetuning; 73% dense / 50–90% sparse real G1, +200% OOD position-only; the multimodal-command tracking anchor.
- [[2503.05652|BRS]] — Autoregressive whole-body decoding (base → torso → arm) mitigates end-effector drift; 88% sub-task; the drift-mitigation-by-factoring precedent (feeds B1).
- [[2605.21133|Spatial Brain Cerebellum]] — End-effector-reachable-space solver decides when base transport is needed; 60.0% vs 0% OOD-hard; the reachability-aware base-transport complement.
- [[2604.07457|CMP]] — Competence-manifold projection keeps world-frame tracking feasible under OOD; 86.7% extreme OOD; the safety layer for world-frame tracking (feeds C2).

**Concrete research questions.**
1. **Q1 — World-frame vs body-centric drift over horizon.** Track end-effector error vs locomotion distance for a [[2602.06341|HiWET]] world-frame controller vs a body-centric baseline — does the body-centric error grow with distance while world-frame stays flat at 12.4 mm, isolating the frame as the lever?
2. **Q2 — Active base modulation vs fixed-base reach.** Ablate [[2602.06341|HiWET]]'s base/waist modulation — how much reachable-workspace extension does active base transport buy, and on which tasks is it necessary (target outside static reach)?
3. **Q3 — Kinematic Manifold Prior contribution.** [[2602.06341|HiWET]] reports KMP halves hand error; quantify the KMP's role in accelerating RL and improving precision — is constraining the action to a kinematic manifold the mechanism, and does it transfer across embodiments?
4. **Q4 — Sparse-goal vs dense-reference command interface.** [[2603.03279|ULTRA]] handles both dense tracking (73%) and sparse goals (50–90%); test which command granularity best balances operator effort against world-frame precision under base transport.

**Related research papers.**
- [[2602.06341|HiWET]] — Hierarchical world-frame end-effector tracking; 12.4 mm; the anchor.
- [[2603.03279|ULTRA]] — Unified multimodal humanoid loco-manip control; 73% dense / 50–90% sparse; multimodal-command tracking.
- [[2503.05652|BRS]] — Autoregressive whole-body decoding; 88% sub-task; drift-mitigation precedent (feeds B1).
- [[2605.21133|Spatial Brain Cerebellum]] — Reachable-space solver + active perception; 60.0% vs 0%; reachability-aware base transport.
- [[2604.07457|CMP]] — Competence-manifold-projection safety for whole-body tracking; 86.7% extreme OOD (feeds C2).
- [[2508.16943|LHM-Humanoid]] — Unified long-horizon loco-manip policy in messy environments; 71.14% / 61.60% unseen / 18.07% five-object; the long-horizon world-frame substrate.
- [[2604.07993|HEX]] — Coupling-aware whole-body manipulation; 79.8%/61.8%; the coupled-dynamics layer beneath the tracker (feeds A1).
- [[2603.20147|AGILE]] — Loco-manip workflow with height-controlled locomotion + motion-quality diagnostics; the deployment-workflow substrate.

**Benchmarks & metrics.**
- [[2602.06341|HiWET]] — World-frame end-effector RMSE 12.4 mm sim / 12–15 mm real on G1, KMP halving hand error; the world-frame-precision metric.
- [[2603.03279|ULTRA]] — 73% dense-reference / 50–90% sparse-goal real G1, +200% OOD position-only; the multimodal-command-tracking metric.
- [[2503.05652|BRS]] — 88% sub-task / 58% entire-task across 5 tasks via autoregressive decoding; the drift-mitigated whole-body metric.

> [!warning] Risks
> - **World-frame closure needs accurate base state estimation** — drift moves from the controller into the estimator. → [[2602.06341|HiWET]] reports accurate state estimation is necessary to compensate oscillation; report end-effector error vs state-estimation error, treat estimation as a first-class dependency.
> - **Active base transport can destabilize manipulation** — moving the base mid-reach is itself a disturbance (couples to A1). → Use A1's coupling-aware predictor under the tracker; report tracking error during vs between base-transport phases.
> - **12.4 mm may not generalize across tasks/embodiments** — one platform, specific tasks. → Q1/Q3 test over horizon and across embodiments; report error by task class and locomotion distance, not a single average.

### A4 — Unified-Latent Policy for Joint Loco-Manipulation Commands

| | |
|---|---|
| **Cluster** | A — Whole-Body Loco-Manipulation |
| **Thesis** | Build a single policy that emits *joint* locomotion + manipulation latent actions, not a manipulation policy stuck in a fixed workspace plus a separate locomotion stack. The reason it must work: manipulation and locomotion have *different visual dynamics*, so they need distinct latent action models, yet must be predicted jointly to avoid decision-execution misalignment. The field assumes the policy is a manipulation model and locomotion is a downstream controller. The bet: a unified-latent policy beats the best decoupled stack head-to-head — a [[2504.16054\|π0.5]] / GR00T-class manipulation policy plus a separate velocity controller (the strongest modular baseline, which [[2512.11047\|WholeBodyVLA]]'s 78.0% already tops) — on the same Bag/Box/Cart tasks, and reaches [[2506.13751\|LeVERB]]'s 58.5% whole-body semantic control (7.8× over a naive hierarchical policy's 7.5%). |
| **Anchor surveys** | [[2511.05936\|10 VLA Challenges]], [[2403.10506\|HumanoidBench]], [[2603.20147\|AGILE]] |
| **Key targets** | [[2512.11047\|WholeBodyVLA]] 78.0% (Bag/Box/Cart) beating modular + end-to-end policies, +38.7% latent pretraining, +24.0% LMO-RL over velocity-RL; [[2506.13751\|LeVERB]] 58.5% on 10 task categories = 7.8× over naive hierarchical policy (7.5%), zero-shot sim-to-real G1; [[2603.12263\|Psi0]] >40% over GR00T N1.6 on 8 long-horizon loco-manip tasks, 800 h human + 30 h robot data |

**Why it matters.** Most policies are implicitly *manipulation* models — "confined to limited workspaces" because they "lack integrated humanoid locomotion," as [[2512.11047|WholeBodyVLA]] puts it. Bolting a locomotion controller underneath causes the failure WholeBodyVLA names: "decision-execution misalignment," where high-level manipulation intent and a velocity-tracking controller disagree. The fix is a policy that *jointly* predicts loco and manip — but the two have different visual dynamics (manipulation is local and contact-driven; locomotion is global and terrain-driven), so WholeBodyVLA learns *separate* VQ-VAE latent action models and grounds both through a loco-manip-oriented RL policy, reaching 78.0% (beating modular and end-to-end baselines), with action-free human-video pretraining adding 38.7% and the LMO policy adding 24.0% over a velocity controller. [[2506.13751|LeVERB]] makes the semantic-control case: a latent "verb" bridging a 10 Hz reasoner and a 50 Hz whole-body controller reaches 58.5% across 10 task categories (7.8× over a naive hierarchical policy's 7.5%), zero-shot sim-to-real on a G1. [[2603.12263|Psi0]] scales it: >40% over GR00T N1.6 on 8 long-horizon tasks. The claim: loco and manip need distinct latent representations but a *joint* prediction interface — the policy is a whole-body model, not a manipulation model with a locomotion bolt-on.

**First-principles framing.**
- **First principle**: Manipulation and locomotion have different visual dynamics (local-contact vs global-terrain), so a single shared latent model underfits one — yet the next whole-body action is a *joint* over both, and predicting them separately re-introduces the decision-execution misalignment. The right structure is distinct latent models with a joint prediction head.
- **Assumption being challenged**: That the policy is a manipulation model and locomotion is a downstream controller. In-place manipulation policies bet on this; [[2512.11047|WholeBodyVLA]]'s misalignment diagnosis and its +24.0% LMO-over-velocity-controller result show the boundary — a velocity controller cannot honor fine-grained loco-manip intent, so locomotion must be *inside* the action interface.
- **The bet**: A unified-latent policy beats the best decoupled stack head-to-head — a [[2504.16054|π0.5]] / GR00T-class manipulation policy plus a separate velocity controller (the strongest modular baseline, which [[2512.11047|WholeBodyVLA]]'s 78.0% already tops) — run on the *same* Bag/Box/Cart tasks, with the joint-latent gain traced to +38.7% from action-free human-video pretraining and +24.0% from the loco-oriented RL policy, and reaches [[2506.13751|LeVERB]]'s 58.5% (7.8× over naive hierarchical). The decoupled-stack SR is the comparator, not asserted here.

**Evidence.**
- [[2512.11047|WholeBodyVLA]] — Separate VQ-VAE latent action models for manip + loco, loco-manipulation-oriented RL policy; 78.0%, +38.7% latent pretraining, +24.0% LMO; the unified-latent anchor.
- [[2506.13751|LeVERB]] — Dual-process hierarchy (10 Hz policy reasoner / 50 Hz WBC) bridged by a latent verb; 58.5% on 10 tasks = 7.8× over naive hierarchical (7.5%), zero-shot G1; the latent-semantic-control anchor.
- [[2603.12263|Psi0]] — Open foundation model for universal humanoid loco-manipulation; >40% over GR00T N1.6, 800 h human + 30 h robot; the foundation-scale unified anchor.
- [[2502.14795|Humanoid-VLA]] — First humanoid policy bridging language, egocentric vision, whole-body control; <40 mm error, 10/10 turn-to-object; the egocentric-whole-body precedent.
- [[2604.07993|HEX]] — Coupling-aware whole-body policy; 79.8%/61.8%; the coupled-dynamics layer the latent interface commands (feeds A1).

**Concrete research questions.**
1. **Q1 — Separate vs shared latent action models.** [[2512.11047|WholeBodyVLA]] uses two VQ-VAE LAMs; ablate against a single shared LAM — does the different-visual-dynamics argument hold quantitatively (separate beats shared), and on which task split (loco-heavy vs manip-heavy)?
2. **Q2 — Loco-oriented RL policy vs velocity-tracking controller.** Isolate the +24.0% LMO gain — does a discrete task-oriented command interface honor loco-manip intent where a velocity controller induces decision-execution misalignment, and where is the gap largest (precise locomotion subgoals)?
3. **Q3 — Action-free human-video latent pretraining yield.** [[2512.11047|WholeBodyVLA]] reports +38.7% from action-free egocentric-video pretraining; quantify the data-efficiency curve — how much teleop data does latent pretraining replace (couples to D2)?
4. **Q4 — Latent verb granularity vs whole-body semantic coverage.** [[2506.13751|LeVERB]]'s verb bridges reasoning and control; sweep the latent dimension against the 10-task semantic coverage — what verb capacity captures whole-body intent without collapsing to a discrete action vocabulary?

**Related research papers.**
- [[2512.11047|WholeBodyVLA]] — Unified-latent loco-manip policy; 78.0%, +38.7%/+24.0%; the anchor.
- [[2506.13751|LeVERB]] — Latent-verb dual-process whole-body policy; 58.5% = 7.8× naive hierarchical; latent-semantic-control anchor.
- [[2603.12263|Psi0]] — Foundation-scale universal loco-manip; >40% over GR00T N1.6; foundation-scale anchor.
- [[2502.14795|Humanoid-VLA]] — First humanoid policy; <40 mm; egocentric-whole-body precedent.
- [[2604.07993|HEX]] — Coupling-aware whole-body policy; 79.8%/61.8%; coupled-dynamics layer (feeds A1).
- [[2603.08572|MetaWorld-X]] — Hierarchical world modeling via VLM-orchestrated experts for humanoid loco-manip; the world-model-orchestrated unified-control variant.
- [[2605.21133|Spatial Brain Cerebellum]] — Active-spatial-brain + action-cerebellum split; 60.0% vs 0% OOD-hard; the perception-action whole-body split.
- [[2511.15200|VIRAL]] — Vision-based unified loco-manipulation (privileged-RL teacher → vision student); 54/59 near-expert real G1 (20.2 s vs 21.4 s human), RSI 95% vs <10%; the vision-grounded unified-policy complement.
- [[2507.06905|ULC]] — One curriculum-RL controller for locomotion + 3-DoF torso + dual-arm; 0.06 rad arm error, robust to 2 kg wrist loads; the unified-command-interface complement.
- [[2511.05936|10 VLA Challenges]] — Enumerates whole-body integration + locomotion as open policy challenges; the open-problem framing.

**Benchmarks & metrics.**
- [[2512.11047|WholeBodyVLA]] — Bag Packing / Box Loading / Cart Pushing 78.0% beating modular + end-to-end, +38.7% latent / +24.0% LMO; the unified-latent metric.
- [[2506.13751|LeVERB]] — 58.5% across 10 task categories = 7.8× over naive hierarchical (7.5%), zero-shot sim-to-real G1; the latent-semantic-control metric.
- [[2603.12263|Psi0]] — >40% over GR00T N1.6 on 8 long-horizon loco-manip tasks, 800 h human + 30 h robot; the foundation-scale loco-manip metric.

> [!warning] Risks
> - **Two latent models double the training complexity** — separate manip/loco LAMs need their own data. → Q3's data-efficiency curve via action-free human video amortizes the cost; report teleop-data replaced per latent model.
> - **Joint prediction can entangle the modalities it separated** — a shared head may leak. → Q1 tests separate-vs-shared; if the joint head entangles, factor the prediction (couples to A1's non-separable-value insight) and report per-modality accuracy.
> - **Latent action vocabularies can collapse** — VQ-VAE codebooks may under-utilize. → [[2512.11047|WholeBodyVLA]]'s separate codebooks mitigate; report codebook utilization and the loco-vs-manip split, not just aggregate SR.

---

## Cluster B — Mobile Manipulation (Nav↔Manip Coupling)

*Jointly controlling a moving base + arm, where the base velocity is itself a manipulation degree of freedom — repositioning extends the reachable workspace mid-task, not before it. These problems exist because nav-then-manipulate decomposition discards the coupling.*

### B1 — Joint Base-Arm Action vs Sequential Decomposition

| | |
|---|---|
| **Cluster** | B — Mobile Manipulation (Nav↔Manip Coupling) |
| **Thesis** | Predict the mobile-manipulation action as a *single coupled joint* over base + torso + arm, not a navigate-then-manipulate pipeline. The reason it must work: the base velocity is a manipulation DoF (repositioning brings out-of-reach targets into reach mid-grasp), so the optimal arm action is *conditional* on the chosen base action, and a sequential split discards that conditioning. The field assumes mobile manipulation = navigation then fixed-base manipulation. The bet: an autoregressive whole-body policy (base → torso → arm) beats decomposed and naive-joint baselines at [[2503.05652\|BRS]]'s 88% sub-task / 58% entire-task (13×/21× over DP3/RGB-DP) and [[2511.18112\|EchoVLA]]'s 0.44 real (vs π0.5 0.33, Diffusion-Policy 0.32 real). |
| **Anchor surveys** | [[2503.05652\|BRS]], [[2407.07788\|BiGym]], [[2306.11565\|HomeRobot]] |
| **Key targets** | [[2503.05652\|BRS]] WB-VIMA 88% sub-task / 58% entire-task across 5 tasks, 13×/21× over DP3/RGB-DP, near-zero safety violations via autoregressive base→torso→arm decoding; [[2401.02117\|Mobile ALOHA]] >90% on 7 bimanual mobile tasks, 50%→95% Wipe-Wine with 50 demos (40–60% fewer demos via co-training); [[2511.18112\|EchoVLA]] 0.44 real (TidyBot++) / 0.31 sim (RoboCasa) vs WB-VIMA 0.11, π0.5 0.20 |

**Why it matters.** The default pipeline navigates to a pose, then runs a fixed-base manipulation policy — discarding the coupling. A humanoid or mobile manipulator doesn't drive-then-grasp; it grasps *while* repositioning, because the base velocity is a manipulation DoF that extends the workspace mid-task. [[2503.05652|BRS]] makes the case: high-DoF mobile manipulators suffer "amplified end-effector drift, out-of-distribution states, and safety violations," and the fix is WB-VIMA's *autoregressive* decoding — base, then torso, then arm, each conditioned on the upstream choice — "essential for mitigating error propagation." WB-VIMA reaches 88% sub-task / 58% entire-task across 5 real household tasks, 13× and 21× over DP3 and RGB-DP, near-zero safety violations. [[2401.02117|Mobile ALOHA]] shows the data-efficiency payoff of whole-body teleop + co-training: >90% on 7 bimanual mobile tasks, lifting Wipe-Wine 50%→95% with 50 demos. [[2511.18112|EchoVLA]] confirms the architecture gap on another platform: 0.44 real (vs WB-VIMA 0.11, π0.5 0.20). The claim: mobile manipulation is a *coupled joint* over base and arm, and the autoregressive factoring base→torso→arm is the structure a sequential split throws away.

**First-principles framing.**
- **First principle**: The base velocity is a manipulation degree of freedom — it changes the reachable workspace continuously during the task. So the right arm action depends on the base action chosen for that moment: pick the base motion first, then choose the arm action that fits it. A pipeline that commits the base pose up front can't exploit in-task repositioning, and predicting base and arm independently lets the two drift apart.
- **Assumption being challenged**: That mobile manipulation = navigation then fixed-base manipulation. Sequential decomposition and naive joint policies bet on this; [[2503.05652|BRS]]'s amplified-drift diagnosis and the 13×/21× margin over DP3/RGB-DP show the coupling is in the *conditioning order*, which both splits discard.
- **The bet**: An autoregressive policy (base → torso → arm, each conditioned on the upstream action) beats decomposed and naive-joint baselines at [[2503.05652|BRS]]'s 88% sub-task / 58% entire-task (13×/21× over DP3/RGB-DP) and [[2511.18112|EchoVLA]]'s 0.44 real (vs π0.5 0.33, Diffusion-Policy 0.32 real) — coordination from respecting the base-as-manipulation-DoF coupling, not a bigger base controller plus a bigger arm policy.

**Evidence.**
- [[2503.05652|BRS]] — WB-VIMA autoregressive base→torso→arm decoding + multimodal observation attention on a wheeled dual-arm + 4-DoF-torso R1; 88% sub-task / 58% entire-task, 13×/21× over DP3/RGB-DP; the autoregressive-whole-body anchor.
- [[2401.02117|Mobile ALOHA]] — Whole-body mobile teleoperation + static-data co-training; >90% on 7 bimanual mobile tasks, 50%→95% with 50 demos; the whole-body-teleop + co-training anchor.
- [[2511.18112|EchoVLA]] — Mobile-manipulation policy with declarative memory; 0.44 real / 0.31 sim vs WB-VIMA 0.11, π0.5 0.20; the mobile-manip-policy architecture anchor (memory feeds B3).
- [[2603.03243|HoMMI]] — Whole-body mobile manipulation from human demonstrations with active head control; 90%/85%/80% real; the human-demo mobile-manip complement (look-at feeds B2).
- [[2512.24653|RoboMIND 2.0]] — Multimodal bimanual mobile-manipulation dataset; multi-robot collaborative SR up to 1.0, cross-embodiment; the mobile-manip data substrate.

**Concrete research questions.**
1. **Q1 — Autoregressive vs independent-joint vs sequential factoring.** Compare [[2503.05652|BRS]]'s base→torso→arm autoregressive decoding against an independent joint head and a navigate-then-manipulate pipeline on the same tasks — does autoregressive deliver the 13×/21× drift-mitigation, and is the conditioning order (base first) the lever?
2. **Q2 — In-task base repositioning vs fixed-base reach.** Quantify how often the optimal policy repositions the base *during* manipulation (not before) — on which tasks does in-task base motion extend the reachable workspace, and does suppressing it cost SR?
3. **Q3 — Co-training with static manipulation data.** [[2401.02117|Mobile ALOHA]] shows static-data co-training lifts 50%→95%; quantify the data-efficiency curve — how much mobile demonstration does static co-training replace, and does it transfer the arm skill while the base policy learns the coupling?
4. **Q4 — Safety under whole-body action.** [[2503.05652|BRS]] reports near-zero safety violations from autoregressive decoding; test whether the factoring is what prevents OOD whole-body states, or whether an explicit safety filter (couples to C2) is still needed.

**Related research papers.**
- [[2503.05652|BRS]] — Autoregressive whole-body mobile manipulation; 88% sub-task; the anchor.
- [[2401.02117|Mobile ALOHA]] — Whole-body teleop + co-training bimanual mobile manip; >90%, 50%→95%; the teleop+co-training anchor.
- [[2511.18112|EchoVLA]] — Declarative-memory mobile-manip policy; 0.44 real vs WB-VIMA 0.11; architecture anchor (feeds B3).
- [[2603.03243|HoMMI]] — Whole-body mobile manip from human demos + active head; 90%/85%/80%; human-demo complement (feeds B2).
- [[2512.24653|RoboMIND 2.0]] — Bimanual mobile-manipulation dataset; up to 1.0 multi-robot; data substrate.
- [[2407.07788|BiGym]] — Demo-driven mobile bimanual benchmark; long-horizon near-0% for baselines; the long-horizon mobile-bimanual difficulty.
- [[2306.11565|HomeRobot]] — Open-vocab mobile manipulation; SR collapses 5–15%→0.4–0.6% with real perception; the perception-coupling difficulty.
- [[2504.16054|π0.5]] — Open-world mobile-manipulation policy; a strong cross-embodiment mobile-manip baseline EchoVLA/HEX beat.

**Benchmarks & metrics.**
- [[2503.05652|BRS]] — 5 real whole-body tasks; 88% sub-task / 58% entire-task, 13×/21× over DP3/RGB-DP, near-zero safety violations; the autoregressive-whole-body metric.
- [[2401.02117|Mobile ALOHA]] — 7 bimanual mobile tasks; >90%, Wipe-Wine 50%→95% with 50 demos (40–60% fewer demos); the whole-body-teleop data-efficiency metric.
- [[2511.18112|EchoVLA]] — RoboCasa sim 0.31 / TidyBot++ real 0.44 across 6 tasks vs WB-VIMA 0.11, π0.5 0.20; the mobile-manip-policy metric.

> [!warning] Risks
> - **Autoregressive decoding adds inference latency** — sequential base→torso→arm prediction is slower than a single head. → Report inference latency vs SR; [[2503.05652|BRS]] runs it real-time, so bound the chunk size to the control loop.
> - **The conditioning order may be task-dependent** — base-first is right for reach-extension, wrong for fine in-place adjustment. → Q1 tests factoring orders; report SR by task type, allow order to adapt.
> - **Perception is often the real bottleneck** — [[2306.11565|HomeRobot]] shows mobile-manip SR collapses with real open-vocab perception. → Couple to B2's active perception; report SR with ground-truth vs real perception to separate the action-coupling gain from the perception gap.

### B2 — Active-Perception Coupling in Mobile Manipulation

| | |
|---|---|
| **Cluster** | B — Mobile Manipulation (Nav↔Manip Coupling) |
| **Thesis** | Treat *where to look* as a coupled base + head + arm decision — actively steering gaze to keep the manipulation target and contact in view while the base moves — instead of assuming a fixed forward camera. The reason it must work: a moving base continuously changes what is visible, so observability is an action the policy must take, not a given. The field assumes mobile-manipulation perception is a passive fixed-camera stream. The bet: an active-gaze policy driven by a predicted look-at point beats fixed-camera baselines at [[2603.03243\|HoMMI]]'s 90%/85%/80% on active-search and precise-placement tasks, and recovers dynamic-object mobile manipulation to [[2411.04999\|DynaMem]]'s 70% (vs 30% static). |
| **Anchor surveys** | [[2306.11565\|HomeRobot]], [[2503.05652\|BRS]], [[2407.07788\|BiGym]] |
| **Key targets** | [[2603.03243\|HoMMI]] 90% laundry / 85% delivery / 80% tablescaping, active head control via predicted look-at-point critical for active search + precise placement + observability; [[2411.04999\|DynaMem]] 70% dynamic pick-drop vs 30% static (2×), locate-failure 6.7% vs 53.3%, 74.5% DynaBench hybrid-query; [[2306.11565\|HomeRobot]] 5–15%→0.4–0.6% SR drop with real perception as the perception-bottleneck floor |

**Why it matters.** Mobile-manipulation systems usually assume a fixed forward camera — but a moving base continuously changes what is visible, so the target, the contact, and the next subgoal can leave the frame exactly when they matter. [[2306.11565|HomeRobot]] quantifies the cost: sim SR collapses from 5–15% with ground-truth perception to 0.4–0.6% with a real open-vocab detector — perception is *the* mobile-manipulation bottleneck. [[2603.03243|HoMMI]] makes the active-perception case: a policy that predicts a "look-at point" and actively controls the head reaches 90%/85%/80% on laundry/delivery/tablescaping, and active head control "proved critical for successfully performing tasks requiring active search, precise placement, and maintaining policy observability." [[2411.04999|DynaMem]] extends it to dynamic scenes: an online spatio-semantic memory drives 70% dynamic pick-and-drop (2× over a 30% static baseline) and cuts locate-failures from 53.3% to 6.7%. The claim: observability is an *action* — where to look couples to where the base goes and what the arm does — and a policy that actively maintains it beats one that hopes the target stays in a fixed frame.

**First-principles framing.**
- **First principle**: A mobile base changes the camera's viewpoint continuously, so what is observable is a function of the base + head action — a controllable quantity, not a given. To keep the target and contact in view the policy must *act* (gaze, head, base orientation), coupling perception to the whole-body action.
- **Assumption being challenged**: That mobile-manipulation perception is a passive fixed-camera stream. Fixed-camera systems bet on this; [[2306.11565|HomeRobot]]'s 5–15%→0.4–0.6% collapse and [[2603.03243|HoMMI]]'s "active head control is critical for observability" show the boundary — when the base moves, a passive camera loses the target, and no policy capacity recovers an unobserved state.
- **The bet**: An active-gaze policy driven by a predicted look-at point beats fixed-camera baselines at [[2603.03243|HoMMI]]'s 90%/85%/80% on active-search + precise-placement tasks, and recovers dynamic-object mobile manipulation to [[2411.04999|DynaMem]]'s 70% (vs 30% static), locate-failure 53.3%→6.7% — success from actively maintaining observability, not a wider passive camera.

**Evidence.**
- [[2603.03243|HoMMI]] — Whole-body mobile manipulation with predicted look-at-point active head control; 90%/85%/80%, active head critical for search + placement + observability; the active-perception anchor.
- [[2411.04999|DynaMem]] — Online dynamic spatio-semantic memory for open-world mobile manip; 70% dynamic vs 30% static, locate-failure 6.7% vs 53.3%; the dynamic-observability anchor.
- [[2306.11565|HomeRobot]] — Open-vocab mobile manipulation; 5–15%→0.4–0.6% SR with real perception; the perception-bottleneck floor.
- [[2605.21133|Spatial Brain Cerebellum]] — Active spatial brain (98.84% spatial understanding, 94.11% active localization) + reachable-space solver; 60.0% vs 0% OOD-hard; the active-spatial-perception complement.
- [[2511.18112|EchoVLA]] — Declarative scene + episodic memory for mobile manip; 0.44 real; the memory channel active perception writes to (feeds B3).

**Concrete research questions.**
1. **Q1 — Active look-at vs fixed camera on observability-critical tasks.** Ablate [[2603.03243|HoMMI]]'s predicted look-at head control against a fixed forward camera — does active gaze deliver the SR on active-search/precise-placement tasks, and where does the fixed camera lose the target (during base motion)?
2. **Q2 — Gaze as a coupled base+head action.** Formulate where-to-look as a joint decision with base orientation — does coupling gaze to the base action (vs independent head control) improve observability while repositioning (couples to B1)?
3. **Q3 — Active perception for dynamic objects.** [[2411.04999|DynaMem]] handles non-stationary objects; test whether active gaze + dynamic memory recovers the 53.3%→6.7% locate-failure on moving targets where a passive camera fails to re-acquire.
4. **Q4 — Perception-gain vs action-gain decomposition.** Run B1's autoregressive policy with ground-truth vs active vs passive perception — how much of mobile-manip SR is the action coupling (B1) vs the perception coupling (B2), separating the two levers?

**Related research papers.**
- [[2603.03243|HoMMI]] — Predicted-look-at active head control for mobile manip; 90%/85%/80%; the anchor.
- [[2411.04999|DynaMem]] — Dynamic spatio-semantic memory; 70% vs 30%, 6.7% vs 53.3% locate-failure; dynamic-observability anchor.
- [[2306.11565|HomeRobot]] — Open-vocab mobile manip; real-perception collapse; perception-bottleneck floor.
- [[2605.21133|Spatial Brain Cerebellum]] — Active spatial brain + reachable-space; 98.84%/94.11% perception, 60.0% vs 0%; active-spatial complement.
- [[2511.18112|EchoVLA]] — Scene + episodic memory mobile-manip policy; 0.44 real; memory channel (feeds B3).
- [[2604.08534|ActiveGlasses]] — Active vision from egocentric human demonstration for manipulation; the human-active-vision precedent for gaze policies.
- [[2407.07788|BiGym]] — Mobile bimanual benchmark with egocentric observation; the observability-stressed mobile-bimanual benchmark.
- [[2504.16054|π0.5]] — Open-world mobile-manip policy; the passive-perception baseline active perception must beat.

**Benchmarks & metrics.**
- [[2603.03243|HoMMI]] — Laundry/delivery/tablescaping 90%/85%/80% real, active-head ablation; the active-perception metric.
- [[2411.04999|DynaMem]] — 70% dynamic pick-drop vs 30% static, locate-failure 6.7% vs 53.3%, DynaBench 74.5% hybrid query; the dynamic-observability metric.
- [[2306.11565|HomeRobot]] — 5–15% (GT perception) → 0.4–0.6% (real detector), 15–20% real overall; the perception-bottleneck diagnostic.

> [!warning] Risks
> - **Active gaze can destabilize manipulation** — moving the head/base to look couples back into balance (A1) and the manipulation frame. → Couple to A1's coupling-aware control; report manipulation precision during vs between active-look maneuvers.
> - **Predicting where to look needs supervision** — the look-at target may be ambiguous. → [[2603.03243|HoMMI]] learns it from demonstrations; report look-at prediction accuracy vs downstream SR, and where the predicted gaze diverges from the optimal.
> - **Active perception adds a control loop** — gaze + base + arm is more to coordinate. → Bound the gaze-control frequency to the perception need; Q4's perception-vs-action decomposition tells you whether the added loop is worth it per task class.

### B3 — Large-Workspace Memory for Mobile Manipulation

| | |
|---|---|
| **Cluster** | B — Mobile Manipulation (Nav↔Manip Coupling) |
| **Thesis** | Equip a mobile manipulator with persistent spatio-semantic memory of objects and scene state it can no longer see, instead of a Markovian policy that re-perceives from scratch each step. The reason it must work: the workspace exceeds the instantaneous field of view, so task-relevant state is partly *outside* the current observation and must be remembered. The field assumes the current camera frame is a sufficient statistic. The bet: a declarative-memory policy cuts the relocated-object locate-failure to [[2411.04999\|DynaMem]]'s 6.7% (vs 53.3% memoryless), driving 70% pick-and-drop on relocated/dynamic objects (vs 30% static) on long-horizon multi-room tasks, while beating memoryless baselines at [[2511.18112\|EchoVLA]]'s 0.44 real (vs π0.5 0.33, Diffusion-Policy 0.32 real). |
| **Anchor surveys** | [[2503.05652\|BRS]], [[2407.07788\|BiGym]], [[2306.11565\|HomeRobot]] |
| **Key targets** | [[2411.04999\|DynaMem]] relocated-object locate-failure 6.7% vs 53.3% memoryless, 70% dynamic vs 30% static, 74.5% DynaBench; [[2511.18112\|EchoVLA]] 0.44 real (TidyBot++) / 0.31 sim (RoboCasa) vs WB-VIMA 0.11 / π0.5 0.20, 0.10 on long-horizon where baselines fail, scene + episodic memory both ablation-critical; [[2407.07788\|BiGym]] long-horizon multi-object near-0% for memoryless baselines as the long-horizon floor |

**Why it matters.** A mobile manipulator's relevant workspace is far larger than its field of view — it walks between rooms, sets an object down, turns away, and must return. A Markovian policy that re-perceives from the current frame has no memory of where it left the laundry basket or that the object has moved. [[2511.18112|EchoVLA]] makes the case: a declarative memory (scene + episodic) drives 0.44 real (TidyBot++) and 0.31 sim (RoboCasa), beating memoryless WB-VIMA at 0.11 and π0.5 at 0.20, and reaches 0.10 on a long-horizon task "where baselines largely failed," with ablations confirming both memory types are necessary. [[2411.04999|DynaMem]] extends it to *dynamic* memory: an online map of non-stationary objects yields 70% pick-and-drop (vs 30% static) and cuts locate-failures from 53.3% to 6.7%. [[2407.07788|BiGym]] shows the floor: long-horizon multi-object mobile-bimanual tasks drive memoryless baselines near 0%. The claim: the current frame is not a sufficient statistic — the workspace exceeds the field of view, so persistent memory of out-of-view state is required, not optional.

**First-principles framing.**
- **First principle**: The task-relevant state spans a workspace larger than the instantaneous field of view — at any moment, relevant objects and scene structure are partly outside the current observation. So the current frame is *not* a sufficient statistic; the policy must carry persistent memory of out-of-view state to act correctly.
- **Assumption being challenged**: That the current camera frame is a sufficient statistic. Markovian / memoryless policies (WB-VIMA, π0.5 baselines) bet on this; [[2511.18112|EchoVLA]]'s 0.11→0.44 gap and [[2411.04999|DynaMem]]'s 53.3%→6.7% locate-failure reduction show the boundary — when the target leaves the frame, a memoryless policy cannot re-acquire it from the current observation alone.
- **The bet**: A declarative-memory policy (scene + episodic) beats memoryless baselines at [[2511.18112|EchoVLA]]'s 0.44 real (vs π0.5 0.33, Diffusion-Policy 0.32 real) and recovers [[2411.04999|DynaMem]]'s 70% on relocated/dynamic objects (vs 30% static, locate-failure 6.7% vs 53.3%) on long-horizon multi-room tasks — success from remembering out-of-view state, not a wider instantaneous view.

**Evidence.**
- [[2511.18112|EchoVLA]] — Synergistic scene + episodic declarative memory for mobile-manip policy; 0.44 real / 0.31 sim vs WB-VIMA 0.11, 0.10 long-horizon where baselines fail; the declarative-memory anchor.
- [[2411.04999|DynaMem]] — Online dynamic spatio-semantic memory; 70% dynamic vs 30% static, locate-failure 6.7% vs 53.3%, 74.5% DynaBench; the dynamic-memory anchor.
- [[2407.07788|BiGym]] — Demo-driven mobile bimanual benchmark; long-horizon multi-object near-0% for memoryless baselines; the long-horizon-memory floor.
- [[2306.11565|HomeRobot]] — Open-vocab mobile manip; perception + memory of unseen objects limits SR; the open-world memory-stress substrate.
- [[2605.21133|Spatial Brain Cerebellum]] — Active spatial brain maintaining spatial state across base motion; 60.0% vs 0% OOD-hard; the spatial-memory complement (active perception feeds B2).

**Concrete research questions.**
1. **Q1 — Scene + episodic memory vs memoryless.** Ablate [[2511.18112|EchoVLA]]'s two memory types — does each contribute the 0.11→0.44 gain, and is episodic memory what enables the long-horizon 0.10 where memoryless collapses?
2. **Q2 — Static vs dynamic memory for relocated objects.** [[2411.04999|DynaMem]] handles non-stationary objects; test whether a *dynamic* memory (vs a static map) is required to recover the 53.3%→6.7% locate-failure when objects move between visits.
3. **Q3 — Memory horizon vs multi-room task length.** Sweep the memory capacity/horizon against task length (single-room → multi-room) — what memory is needed before the policy can return to a previously-seen-but-now-out-of-view target?
4. **Q4 — Memory + active perception synergy.** Combine B2's active gaze (what to look at now) with B3's memory (what was seen before) — does writing active-perception observations into persistent memory dominate either alone on long-horizon mobile manipulation?

**Related research papers.**
- [[2511.18112|EchoVLA]] — Scene + episodic declarative memory; 0.44 real vs WB-VIMA 0.11; the anchor.
- [[2411.04999|DynaMem]] — Dynamic spatio-semantic memory; 70% vs 30%, 6.7% vs 53.3%; dynamic-memory anchor.
- [[2407.07788|BiGym]] — Long-horizon mobile-bimanual benchmark; near-0% memoryless; the memory floor.
- [[2306.11565|HomeRobot]] — Open-vocab mobile manip; open-world memory stress; substrate.
- [[2605.21133|Spatial Brain Cerebellum]] — Active spatial brain maintaining spatial state; 60.0% vs 0%; spatial-memory complement (feeds B2).
- [[2503.05652|BRS]] — Whole-body mobile manipulation across extensive reach; 88% sub-task; the large-workspace whole-body substrate (feeds B1).
- [[2512.24653|RoboMIND 2.0]] — Bimanual mobile-manip dataset across embodiments; up to 1.0; the multi-room data substrate.
- [[2504.16054|π0.5]] — Open-world mobile-manip policy; the memoryless cross-embodiment baseline EchoVLA beats.

**Benchmarks & metrics.**
- [[2511.18112|EchoVLA]] — RoboCasa 0.31 / TidyBot++ 0.44 vs WB-VIMA 0.11, 0.10 long-horizon, scene + episodic ablation; the declarative-memory metric.
- [[2411.04999|DynaMem]] — 70% dynamic vs 30% static, locate-failure 6.7% vs 53.3%, DynaBench 74.5%; the dynamic-memory metric.
- [[2407.07788|BiGym]] — Long-horizon multi-object mobile-bimanual tasks; memoryless near-0%; the long-horizon-memory difficulty gradient.

> [!warning] Risks
> - **Memory can accumulate stale/wrong state** — a remembered object location goes invalid when the world changes. → [[2411.04999|DynaMem]]'s dynamic memory updates online; report SR on relocated objects, treat memory staleness as a measured failure mode.
> - **Memory scales with workspace** — multi-room state can blow up. → Q3 tests memory-horizon vs task length; report the memory footprint vs SR curve, prune to task-relevant state.
> - **Memory and perception interact** — bad active perception (B2) writes bad memory. → Q4 tests the synergy; report SR with active-vs-passive perception feeding memory, to separate write-quality from memory-mechanism.

---

## Cluster C — Force-Adaptive Coordination Under Load

*Whole-body control under external wrench, payload, and contact force — where a force at the hand propagates through the kinematic chain to the support polygon, the legs compensate for what the arms feel, and the standard task reward silently omits the force.*

### C1 — Force-Adaptive Whole-Body Control Under Unknown Wrench

| | |
|---|---|
| **Cluster** | C — Force-Adaptive Coordination Under Load |
| **Thesis** | Build a whole-body policy that *actively adapts* to unknown external end-effector forces — predicting and compensating the wrench's whole-body reaction — rather than a stiff tracker that treats force as a disturbance. The reason it must work: an external hand wrench $F_{\text{ext}}$ propagates through $J_{\text{ext}}^{\top}$ to every joint including the support legs, so force adaptation is a whole-body equilibrium problem, not an arm problem. The field assumes whole-body controllers can be force-agnostic. The bet: a torque-limit-aware force-adaptive policy cuts upper-body tracking error under large force to [[2505.06776\|FALCON (Loco-Manipulation)]]'s 0.37 (~2× over the 0.60 monolithic baseline) and sustains [[2502.10894\|UAN]]-class loads (113 N cart, 8 kg lift) while keeping balance. |
| **Anchor surveys** | [[2505.06776\|FALCON (Loco-Manipulation)]], [[2512.01061\|Sim-to-Real Door]], [[2403.10506\|HumanoidBench]] |
| **Key targets** | [[2505.06776\|FALCON (Loco-Manipulation)]] 0.37 vs 0.60 upper-body tracking error under large force (~2×), 100 N cart-pull + 1.2 kg/hand payload, torque-limit-aware 3D force curriculum; [[2502.10894\|UAN]] real 113 N cart-drag + 8 kg lift + 20 m throw via unsupervised actuator net; [[2606.03297\|SplitAdapter]] sim-real 26/27 full-task vs 16/27 base under varying mass/height + OOD 6 kg loads (86/90 sim); [[2512.01061\|Sim-to-Real Door]] 83% real door-opening (vision-only, contact-rich force) + 23.8% faster than human teleop |

**Why it matters.** A humanoid opening a heavy door or carrying a variable payload faces "significant, dynamic, and multi-directional 3D end-effector forces," and as [[2505.06776|FALCON (Loco-Manipulation)]] diagnoses, current RL is "either kinematically limited in force compensation or suffer[s] from training inefficiency and entangled control objectives." The reason is whole-body: a hand wrench $F_{\text{ext}}$ propagates through $J_{\text{ext}}^{\top}$ to *every* joint, so the legs compensate for what the arms feel — an equilibrium problem over the whole body, not a local arm-stiffness problem. FALCON's answer is a dual-agent decomposition with a *torque-limit-aware 3D force curriculum* that applies physically-feasible forces respecting joint limits, cutting upper-body tracking error to 0.37 under large forces (~2× over a monolithic 0.60) and letting a real G1/T1 pull a 100 N cart and carry 1.2 kg per hand. [[2502.10894|UAN]] shows the athletic extreme on a quadruped-plus-arm: an unsupervised actuator net drags a 113 N cart, lifts 8 kg, and throws 20 m. [[2606.03297|SplitAdapter]] adds the adaptation angle: it factorizes the adaptation signal into a load/object context and a dynamics-mismatch context (unified latents conflate the two and lose robustness under heavy loads), lifting real G1 full-task success to 26/27 (vs 16/27 base) across varying masses and pickup/placement heights, with the load context cleanly organizing the latent space for OOD 6 kg payloads. [[2512.01061|Sim-to-Real Door]] proves vision-only contact-rich handling: 83% real door-opening, 23.8% faster than human teleoperation. The claim: force adaptation is a whole-body equilibrium problem, and a policy that anticipates the wrench's reaction (rather than stiffly rejecting it) is what makes forceful interaction stable.

**First-principles framing.**
- **First principle**: A force at the hand (an external wrench $F_{\text{ext}}$) doesn't stay at the hand — it spreads through the kinematic chain to every joint, including the support legs that keep the body's centre of mass over its feet. So force adaptation is a whole-body balance problem: the legs have to compensate for what the arms feel, while keeping every joint torque within limits and the centre of mass over the support polygon. It is not a local arm problem.
- **Assumption being challenged**: That whole-body controllers can be force-agnostic. Force-agnostic trackers (the monolithic baseline FALCON beats) bet on this; FALCON's "kinematically limited force compensation" diagnosis and the 0.60→0.37 gap show the boundary — a force-agnostic policy compensates only with arm kinematics and loses balance under a large force, because the force is a balance term it never modeled.
- **The bet**: A torque-limit-aware force-adaptive policy cuts upper-body tracking error under large force to [[2505.06776|FALCON (Loco-Manipulation)]]'s 0.37 (~2× over 0.60 monolithic) and sustains [[2502.10894|UAN]]-class loads (113 N cart, 8 kg) while keeping balance — stability from modeling the wrench's whole-body reaction, not stiffer arm tracking.

**Evidence.**
- [[2505.06776|FALCON (Loco-Manipulation)]] — Dual-agent lower/upper RL + torque-limit-aware 3D force curriculum; 0.37 vs 0.60 under force, 100 N cart, 1.2 kg/hand; the force-adaptive-whole-body anchor.
- [[2502.10894|UAN]] — Unsupervised actuator net bridging sim-to-real for athletic loco-manip; 113 N cart-drag, 8 kg lift, 20 m throw; the high-load athletic anchor (quadruped + arm).
- [[2606.03297|SplitAdapter]] — Splits the adaptation signal into a load/object context and a dynamics-mismatch context (unified latents conflate them); 26/27 sim-real vs 16/27 base under varying mass; the load-aware-adaptation anchor.
- [[2512.01061|Sim-to-Real Door]] — Vision-only contact-rich door-opening via massive-randomization sim + GRPO; 83% real, 23.8% faster than human; the contact-rich-force anchor.
- [[2604.07457|CMP]] — Competence-manifold-projection whole-body tracking robust to OOD geometry/sensor; 86.7% extreme OOD; the robustness layer for force (feeds C2).
- [[2603.03279|ULTRA]] — Unified multimodal control + RL finetuning robust to OOD goals; 73% dense / 50–90% sparse; the multimodal-command force-tracking complement (feeds A3).

**Concrete research questions.**
1. **Q1 — Torque-limit-aware curriculum vs naive force training.** Isolate [[2505.06776|FALCON (Loco-Manipulation)]]'s torque-limit-aware 3D force curriculum — does respecting joint limits during force application deliver the 0.60→0.37 error drop and the stable exploration, vs naive (limit-blind) force training?
2. **Q2 — Wrench prediction vs reactive compensation.** Predict the external wrench's whole-body reaction (forward model through $J_{\text{ext}}^{\top}$) and compensate anticipatorily vs reacting to measured force — does anticipation improve balance under sudden load (couples to A1's coupling prediction)?
3. **Q3 — Shared-proprioception decomposition vs monolithic.** [[2505.06776|FALCON (Loco-Manipulation)]] shares whole-body proprioception between lower/upper agents; ablate against monolithic whole-body RL — is the decomposition the source of faster convergence + lower error under force?
4. **Q4 — Factorized vs unified load adaptation.** [[2606.03297|SplitAdapter]] disentangles a load/object context from a dynamics-mismatch context (unified latents conflate them); ablate the factorization against a unified adapter under OOD payloads — is disentangling load from dynamics what delivers the 16/27→26/27 robustness, and does explicit force sensing ([[2512.01061|Sim-to-Real Door]] uses vision only) further help under heavy load?

**Related research papers.**
- [[2505.06776|FALCON (Loco-Manipulation)]] — Force-adaptive dual-agent loco-manipulation; 0.37 vs 0.60; the anchor.
- [[2502.10894|UAN]] — Unsupervised actuator net for athletic loco-manip; 113 N / 8 kg / 20 m; high-load anchor.
- [[2606.03297|SplitAdapter]] — Factorized load/object + dynamics adaptation; 26/27 vs 16/27 sim-real under varying mass; the load-aware-adaptation anchor.
- [[2512.01061|Sim-to-Real Door]] — Vision-only contact-rich door-opening; 83% real; contact-rich-force anchor.
- [[2604.07457|CMP]] — Competence-manifold-projection robustness; 86.7% extreme OOD; robustness layer (feeds C2).
- [[2603.03279|ULTRA]] — Unified multimodal force-tracking; 73% dense; multimodal-command complement (feeds A3).
- [[2604.07993|HEX]] — Coupling-aware whole-body manipulation; 79.8%/61.8%; the coupled-dynamics layer force adaptation rides on (feeds A1).
- [[2602.06341|HiWET]] — World-frame tracking compensating base disturbance; 12.4 mm; the precision-under-disturbance complement (feeds A3).
- [[2605.10063|EFGCL]] — External-force-guided curriculum learning; the force-as-training-signal precedent (cross-ref [[Locomotion|Locomotion]] A2).

**Benchmarks & metrics.**
- [[2505.06776|FALCON (Loco-Manipulation)]] — Upper-body tracking error under large force 0.37 vs 0.60, 100 N cart + 1.2 kg/hand on G1/T1; the force-adaptive-tracking metric.
- [[2502.10894|UAN]] — Real 113 N cart-drag (10 m), 8 kg lift, 20 m throw; the high-load athletic metric.
- [[2606.03297|SplitAdapter]] — 26/27 sim-real full-task vs 16/27 base across varying mass/height, 86/90 sim with OOD 6 kg loads; the load-aware-adaptation metric.
- [[2512.01061|Sim-to-Real Door]] — 83% real door-opening across diverse doors, 83% vs 80% human, 23.8% faster; the contact-rich-force metric.

> [!warning] Risks
> - **Torque-limit-aware curriculum needs an accurate torque model** — the feasible-force envelope depends on the actuator model. → [[2502.10894|UAN]]'s unsupervised actuator net learns the discrepancy without torque sensors; report sim-vs-real torque-tracking, lean on UAN where the model is uncertain.
> - **Force adaptation can trade off precision** — compliant force-following may drift the end-effector. → Report the force-magnitude vs tracking-error Pareto front, per [[2505.06776|FALCON (Loco-Manipulation)]]'s under-force error curve, not a single number.
> - **Large loads stress hardware + balance** — 113 N / 8 kg push the support polygon. → Bound load claims to validated platforms; couple to C2's safety filter for the balance guarantee under load.

### C2 — Safety-Bounded Whole-Body Control Under Load

| | |
|---|---|
| **Cluster** | C — Force-Adaptive Coordination Under Load |
| **Thesis** | Wrap whole-body loco-manipulation in a *certified safety filter* — a control-barrier-function / competence-manifold projection that smoothly projects unsafe commands onto the closest feasible action — instead of hoping a learned policy stays safe under load. The reason it must work: a learned policy has no formal guarantee under OOD wrench/geometry, while balance and collision are hard physical boundaries. The field assumes domain randomization + reward shaping yield safe-enough behavior. The bet: a low-latency filter lifts OOD whole-body survival to [[2604.07457\|CMP]]'s 86.7% extreme-OOD / 93.3% moderate-OOD real (vs unshielded baselines, at 2.99 ms latency) and holds collision-free behavior under [[2605.25546\|ISSf-CBF WBC]]'s 20% mass mismatch where standard CBF collides ~50%. |
| **Anchor surveys** | [[2604.07457\|CMP]], [[2605.25546\|ISSf-CBF WBC]], [[2403.10506\|HumanoidBench]] |
| **Key targets** | [[2604.07457\|CMP]] OOD-survival 46.9% vs 4.7% (geometry, ~10×) / 40.3% vs 6.9% (sensor noise, ~6×) sim, real 100% in-dist / 93.3% moderate / 86.7% extreme OOD, 2.99 ms latency (best-effort projection to closest feasible intention); [[2605.25546\|ISSf-CBF WBC]] 20% mass-mismatch → collision-free vs standard/eCBF ~50% collision, real TOCABI single-leg balance + teleop collision-avoidance; [[2512.01061\|Sim-to-Real Door]] 83% as the unshielded contact-rich baseline |

**Why it matters.** A policy that works in-distribution gives no formal guarantee when geometry, payload, or sensor noise drifts OOD — and under load the failure modes are *physical*: loss of balance, self-collision, workspace-boundary violation. The standard answer is domain randomization plus reward shaping, but [[2604.07457|CMP]] shows the gap: unshielded whole-body tracking survives only 4.7% of OOD-geometry tasks and 6.9% under OOD sensor noise. CMP's Competence Manifold Projection — "smoothly projects unsafe commands to the closest feasible intention" — lifts these to 46.9% (geometry, ~10×) and 40.3% (sensor, ~6×) in sim, and to 100% in-distribution / 93.3% moderate / 86.7% extreme OOD on a real robot, all at 2.99 ms (comparable to unshielded). [[2605.25546|ISSf-CBF WBC]] gives the formal version: an input-to-state-safe control barrier function stays collision-free under a 20% mass mismatch where standard CBF and eCBF collide ~50% of the time, validated on a real TOCABI humanoid during single-leg balancing and teleoperated obstacle avoidance. The claim: balance and collision are *hard constraints*, and a certified projection that enforces them — not a reward that softly discourages violation — is what makes whole-body control under load deployable.

**First-principles framing.**
- **First principle**: Balance (centre-of-mass in the support polygon) and collision-freeness are hard constraints with no soft trade-off — a violation is a fall or a crash. A learned policy optimizes an expectation and carries no per-step guarantee under OOD load/geometry; a control-barrier / projection filter enforces the constraint set as a hard boundary, projecting any unsafe command to the closest feasible one.
- **Assumption being challenged**: That domain randomization + reward shaping yield safe-enough behavior. The DR + reward-shaping approach (the unshielded baselines CMP/ISSf-CBF beat) bets on this; [[2604.07457|CMP]]'s 4.7% OOD-geometry survival and [[2605.25546|ISSf-CBF WBC]]'s ~50% baseline collision under mass mismatch show the boundary — a soft reward cannot guarantee a hard constraint under distribution shift.
- **The bet**: A low-latency filter lifts OOD whole-body survival to [[2604.07457|CMP]]'s 86.7% extreme / 93.3% moderate real (vs unshielded, at 2.99 ms) and holds collision-free behavior under [[2605.25546|ISSf-CBF WBC]]'s 20% mass mismatch where standard CBF collides ~50% — safety from certified projection, not softer reward shaping.

**Evidence.**
- [[2604.07457|CMP]] — Competence Manifold Projection safety layer projecting unsafe whole-body commands to closest feasible; 46.9% vs 4.7% OOD-geometry, 86.7% extreme OOD real, 2.99 ms; the best-effort-projection anchor.
- [[2605.25546|ISSf-CBF WBC]] — Input-to-state-safe CBF for whole-body control; collision-free under 20% mass mismatch vs ~50% baseline collision, real TOCABI; the certified-barrier anchor.
- [[2512.01061|Sim-to-Real Door]] — Vision-only contact-rich door-opening; 83% real; the unshielded contact-rich baseline a safety filter would bound (feeds C1).
- [[2505.06776|FALCON (Loco-Manipulation)]] — Torque-limit-aware force curriculum (a soft feasibility constraint); 0.37 vs 0.60; the learned-feasibility precedent a hard filter complements (feeds C1).
- [[2602.06341|HiWET]] — Kinematic Manifold Prior constraining action to feasible configurations; 12.4 mm; the kinematic-feasibility-prior complement (feeds A3).

**Concrete research questions.**
1. **Q1 — Certified projection vs reward-shaped safety.** Compare [[2604.07457|CMP]]'s competence-manifold projection / [[2605.25546|ISSf-CBF WBC]]'s CBF against a reward-penalty-only policy on OOD geometry + mass mismatch — does the certified filter deliver the 4.7%→46.9% survival / ~50%→0% collision where reward shaping cannot guarantee it?
2. **Q2 — Latency vs safety coverage.** [[2604.07457|CMP]] runs at 2.99 ms; sweep the filter's computational budget against the OOD coverage — what latency is needed for best-effort projection within the whole-body control loop?
3. **Q3 — Safety under load (wrench-aware barrier).** Extend the barrier to include the external-wrench equilibrium constraint (couples to C1) — does a wrench-aware CBF maintain balance under unknown payload where a kinematics-only barrier fails?
4. **Q4 — Best-effort continuation vs hard stop.** [[2604.07457|CMP]] does "best-effort" continuation by projecting to the closest feasible intention rather than halting; quantify task-completion-under-projection vs a hard-stop safety scheme — does graceful projection preserve more SR?

**Related research papers.**
- [[2604.07457|CMP]] — Competence-manifold-projection whole-body safety; 86.7% extreme OOD, 2.99 ms; the anchor.
- [[2605.25546|ISSf-CBF WBC]] — Input-to-state-safe CBF whole-body control; collision-free under 20% mass mismatch; the certified-barrier anchor.
- [[2512.01061|Sim-to-Real Door]] — Unshielded contact-rich door-opening; 83%; the baseline to bound (feeds C1).
- [[2505.06776|FALCON (Loco-Manipulation)]] — Torque-limit-aware soft feasibility; 0.37 vs 0.60; learned-feasibility complement (feeds C1).
- [[2602.06341|HiWET]] — Kinematic-Manifold-Prior feasibility; 12.4 mm; kinematic-feasibility complement (feeds A3).
- [[2603.03279|ULTRA]] — Robust whole-body tracking under OOD goals; 73% dense; the OOD-robustness complement (feeds A3).
- [[2604.07993|HEX]] — Coupling-aware whole-body control; 79.8%/61.8%; the policy a safety filter wraps (feeds A1).
- [[2403.10506|HumanoidBench]] — Whole-body benchmark stressing high-DoF control; the safety-stress framing.

**Benchmarks & metrics.**
- [[2604.07457|CMP]] — OOD-survival 46.9% vs 4.7% (geometry) / 40.3% vs 6.9% (sensor) sim, 100%/93.3%/86.7% in-dist/moderate/extreme OOD real, 2.99 ms; the safety-projection metric.
- [[2605.25546|ISSf-CBF WBC]] — Collision-free under 20% mass mismatch vs ~50% standard/eCBF collision, real TOCABI single-leg balance; the certified-barrier metric.
- [[2512.01061|Sim-to-Real Door]] — 83% unshielded contact-rich real door-opening; the baseline safety-coverage reference.

> [!warning] Risks
> - **Safety filter can over-constrain and block valid actions** — an aggressive projection may refuse feasible commands. → [[2604.07457|CMP]]'s best-effort projection to closest feasible (not hard stop) preserves task continuation; report task-completion-under-projection (Q4), not just safety.
> - **CBF needs an accurate model** — the barrier's guarantee depends on dynamics fidelity. → [[2605.25546|ISSf-CBF WBC]]'s input-to-state-safe formulation tolerates a 20% mass mismatch; report the model-mismatch level the guarantee survives.
> - **Latency can break the control loop** — a slow filter defeats real-time whole-body control. → Q2's latency-vs-coverage sweep is the feasibility gate; bound to the 2.99 ms-class budget.

---

## Cluster D — Whole-Body Teleoperation & Human-Motion Retargeting

*The whole-body data wall — demonstrations of coupled loco-manipulation are scarce, embodiment-mismatched, and per-platform — addressed by retargeting, capturing, transferring, and synthesizing coupled demonstrations.*

### D1 — Interaction-Preserving Whole-Body Retargeting

| | |
|---|---|
| **Cluster** | D — Whole-Body Teleoperation & Human-Motion Retargeting |
| **Thesis** | Retarget human motion to a humanoid by preserving the *interaction* — object contact, scene constraints, foot–ground contact — as a hard objective, instead of minimizing joint-space pose error. The reason it must work: a loco-manipulation reference's value is in the contact relationships (hand-on-object, foot-on-floor), not the joint angles, so a pose-error-minimizing retarget can be joint-accurate yet contact-broken. The field assumes retargeting = kinematic pose matching. The bet: an interaction-preserving retargeter lifts downstream-RL success to [[2509.26633\|OmniRetarget]]'s 82.20–94.73% (near-zero penetration, zero foot-skating) and matches [[2606.03476\|Human2Humanoid]]'s 88.5% SR / 0.05 cm penetration via a morphology-invariant end-effector consistency objective. |
| **Anchor surveys** | [[2509.26633\|OmniRetarget]], [[2505.12748\|TeleOpBench]], [[2403.10506\|HumanoidBench]] |
| **Key targets** | [[2509.26633\|OmniRetarget]] downstream-RL 82.20–94.73% with near-zero penetration (0.00–0.01) + zero foot-skating (0 duration, 0 max-velocity), interaction-preserving (object + scene); [[2606.03476\|Human2Humanoid]] 88.5% SR / 0.12 tracking-error / 0.05 cm penetration / 4.7% foot-skating, morphology-invariant end-effector consistency loss; [[2603.22201\|NMR]] 54% self-collision reduction (0.87% frames) + zero joint jumps |

**Why it matters.** Loco-manipulation references come from human motion — but a human's loco-manipulation is defined by its *interactions*: hand on object, foot on floor, body against scene. A retargeter that minimizes joint-space pose error can be joint-accurate yet contact-broken — the hand floats off the object, the foot skates, the reference penetrates the ground — and the policy inherits the violation. [[2509.26633|OmniRetarget]] makes the case: it generates references for "whole-body loco-manipulation *and scene interaction*," reaching near-zero penetration (0.00–0.01) and *eliminating foot-skating* (0 duration, 0 max velocity), lifting downstream RL to 82.20–94.73% with lower variance — tying reference contact-fidelity to trainability. [[2606.03476|Human2Humanoid]] formalizes the morphology side: a *morphology-invariant end-effector consistency loss* plus physics-aware constraints yields 88.5% SR, the lowest 0.05 cm penetration, and 4.7% foot-skating, with ablations confirming the loss preserves the semantic interaction. [[2603.22201|NMR]] adds smoothness: neural retargeting cuts self-collisions 54% (to 0.87% of frames) with zero joint jumps. The claim: a reference's value is in its contact relationships, and a retargeter that preserves interaction (not pose) is what makes it trainable.

**First-principles framing.**
- **First principle**: The information in a loco-manipulation reference is the contact graph — which surfaces touch (hand–object, foot–floor, body–scene) and with what relative geometry — not the absolute joint angles, which are a morphology-specific realization. A pose-error-minimizing retarget optimizes the wrong quantity: it can match joints while breaking the contact that defines the task.
- **Assumption being challenged**: That retargeting = kinematic pose matching. Pose-matching retargeters (OmniRetarget/Human2Humanoid beat PHC, GMR, Unitree Retarget) bet on this; OmniRetarget's foot-skating elimination → 82–94% downstream and Human2Humanoid's end-effector-consistency ablation show that pose accuracy does not imply the contact fidelity the policy needs.
- **The bet**: An interaction-preserving retargeter lifts downstream-RL success to [[2509.26633|OmniRetarget]]'s 82.20–94.73% (near-zero penetration, zero foot-skating) and matches [[2606.03476|Human2Humanoid]]'s 88.5% SR / 0.05 cm penetration via a morphology-invariant end-effector consistency objective — trainability from the contact graph, not joint-pose error.

**Evidence.**
- [[2509.26633|OmniRetarget]] — Interaction-preserving retargeting for whole-body loco-manip + scene interaction; near-zero penetration, zero foot-skating, 82.20–94.73% downstream RL; the interaction-preserving anchor.
- [[2606.03476|Human2Humanoid]] — Physics-aware cross-morphology retargeting with morphology-invariant end-effector consistency loss; 88.5% SR, 0.05 cm penetration, 4.7% foot-skating; the morphology-invariant-contact anchor.
- [[2603.22201|NMR]] — Neural motion retargeting; 54% self-collision reduction (0.87% frames), zero joint jumps; the smoothness/feasibility anchor.
- [[2604.00202|DreamControl-v2]] — Pre-retargeting diffusion prior; 68% valid trajectories vs 8% inference-time, 0.925 vs 0.101 RL; the pre-retargeting-feasibility complement (feeds A2).
- [[2603.03279|ULTRA]] — Physics-driven neural retargeting with lowest foot-skating + minimal penetration; 73% dense tracking; the physics-fidelity retargeting complement (feeds A3).

**Concrete research questions.**
1. **Q1 — Interaction-preserving vs pose-matching downstream.** Compare [[2509.26633|OmniRetarget]]'s interaction objective against a pose-error-minimizing retarget on the *same* human motions — does preserving contact deliver the 82–94% downstream RL where pose-matching breaks contact, and does foot-skating predict downstream SR?
2. **Q2 — Morphology-invariant end-effector consistency.** Isolate [[2606.03476|Human2Humanoid]]'s end-effector consistency loss — is morphology-invariant contact preservation the mechanism behind 88.5% SR + 0.05 cm penetration, and does it transfer across humanoid morphologies?
3. **Q3 — Scene-interaction preservation, not just object.** [[2509.26633|OmniRetarget]] preserves scene interaction (climbing, wall-flips); test whether preserving body–scene contact (not just hand–object) is needed for whole-body tasks like climbing onto a platform while carrying a load.
4. **Q4 — Retargeting feasibility → trainability curve.** Quantify the penetration/foot-skating → downstream-RL-SR curve across retargeting methods — is contact-fidelity a *predictor* of trainability (couples to A2's feasibility-first imitation)?

**Related research papers.**
- [[2509.26633|OmniRetarget]] — Interaction-preserving loco-manip + scene retargeting; 82.20–94.73% downstream; the anchor.
- [[2606.03476|Human2Humanoid]] — Cross-morphology physics-aware retargeting; 88.5% SR, 0.05 cm penetration; morphology-invariant-contact anchor.
- [[2603.22201|NMR]] — Neural retargeting; 54% self-collision reduction; smoothness anchor.
- [[2604.00202|DreamControl-v2]] — Pre-retargeting diffusion prior; 68% vs 8% valid; feasibility complement (feeds A2).
- [[2603.03279|ULTRA]] — Physics-driven retargeting + multimodal control; 73% dense; physics-fidelity complement (feeds A3).
- [[2511.09484|SPIDER]] — Scalable physics-informed dexterous retargeting; 2.4 M frames / 800 h across 5 hands + 4 humanoids, up to 100% SR; the scaled-retargeting data engine (feeds D2).
- [[2605.06593|ReActor]] — RL physics-aware motion retargeting; zero penetration, 97.45% downstream RL; the RL-retargeting complement (cross-ref [[Locomotion|Locomotion]] A2).
- [[2606.01851|PHASOR]] — Phase-anchored universal action representation; 1.62 mm next-frame, 90.3% R@1; the universal-representation retargeting complement (feeds D3).
- [[2412.17730|Mimicking-Bench]] — Benchmark for humanoid-*scene* interaction via human mimicking; 54% over 6 household tasks; the scene-interaction-preservation benchmark (Q3).

**Benchmarks & metrics.**
- [[2509.26633|OmniRetarget]] — Penetration 0.00–0.01 + foot-skating 0 (duration + max-velocity), downstream RL 82.20–94.73%; the interaction-preserving metric.
- [[2606.03476|Human2Humanoid]] — 88.5% SR, 0.12 tracking error, 0.05 cm penetration, 4.7% foot-skating vs PHC/GMR/Unitree-Retarget; the morphology-invariant-contact metric.
- [[2603.22201|NMR]] — 54% self-collision reduction (0.87% frames), zero joint jumps vs optimization baselines; the retargeting-smoothness metric.
- [[2412.17730|Mimicking-Bench]] — 6 household humanoid-scene interaction tasks, 54% best-combination SR, ~log-linear scaling with data, over 20K synthetic + 3K real interactions / 11K objects; the humanoid-scene-interaction-via-mimicking metric.

> [!warning] Risks
> - **Interaction preservation needs interaction annotation** — knowing the contact graph requires labeled or inferred contact. → [[2509.26633|OmniRetarget]] infers it from human–object–scene data; report retargeting quality vs contact-annotation quality.
> - **Morphology gap can be too large** — a very different humanoid may have no feasible interaction-preserving retarget. → [[2606.03476|Human2Humanoid]]'s physics-aware constraints bound infeasible targets; report the morphology range the consistency loss covers (couples to D3).
> - **Contact-fidelity metrics ≠ task success** — zero foot-skating doesn't guarantee task completion. → Q1/Q4 tie contact-fidelity to downstream RL SR; report the trainability curve, not just penetration/skating.

### D2 — Whole-Body Teleoperation Interfaces & Robot-Free Demonstration

| | |
|---|---|
| **Cluster** | D — Whole-Body Teleoperation & Human-Motion Retargeting |
| **Thesis** | Capture *simultaneous* loco + manip demonstrations — via whole-body teleoperation that commands base and arms at once, or robot-free egocentric human demos aligned to the humanoid — instead of scaling fixed-base arm teleoperation. The reason it must work: the coupling can only be demonstrated if locomotion and manipulation are commanded together; a fixed-base interface never produces a loco-manip demonstration. The field assumes whole-body data is fixed-base demos plus a locomotion controller. The bet: a robot-free egocentric pipeline with principled human-to-humanoid alignment lifts loco-manip generalization by [[2602.10106\|EgoHumanoid]]'s +51 pp (82% vs 31% robot-only) and +19 pp in-domain, and scales data like [[2605.20373\|SUGAR]]'s 32.7%→76.0% as human demonstrations grow. |
| **Anchor surveys** | [[2505.12748\|TeleOpBench]], [[2602.10106\|EgoHumanoid]], [[2403.10506\|HumanoidBench]] |
| **Key targets** | [[2602.10106\|EgoHumanoid]] +19 pp in-domain (78% vs 59%) + 51 pp generalization (82% vs 31%) from co-training robot-free egocentric demos, 100% navigation-dominated subtasks, ~2× faster than teleop; [[2605.20373\|SUGAR]] 32.7%→76.0% Kick-Box data scaling (20→100 traj) over 6 loco-manip tasks; [[2401.02117\|Mobile ALOHA]] whole-body teleop >90% + 50%→95% with 50 demos; [[2505.12748\|TeleOpBench]] 30 tasks / 4 modalities / 3 humanoids with sim-real correlation |

**Why it matters.** Whole-body loco-manipulation is "bottlenecked by the scarcity of diverse, large-scale demonstration data," as [[2602.10106|EgoHumanoid]] states — and the standard fix, fixed-base arm teleoperation, structurally cannot produce a loco-manip demonstration, because the operator never commands base and arms together. Two routes break the wall. First, *whole-body teleoperation*: [[2401.02117|Mobile ALOHA]] lets one operator command base and both arms at once, producing genuine bimanual mobile-manip demos (>90% on 7 tasks, 50%→95% with 50 demos via co-training), and [[2505.12748|TeleOpBench]] standardizes the comparison — 30 bimanual tasks across 4 teleop modalities (MoCap, VR, exoskeleton, vision) on 3 humanoids, with strong sim-real correlation. Second, *robot-free egocentric demonstration*: [[2602.10106|EgoHumanoid]] captures human loco-manip with a portable VR rig and a human-to-humanoid alignment pipeline (depth-based view alignment + unified 6-DoF delta-EE + discrete locomotion commands), lifting in-domain SR +19 pp (78% vs 59%) and *generalization +51 pp* (82% vs 31%) over robot-only training, with human-only models hitting 100% on navigation-dominated subtasks. [[2605.20373|SUGAR]] confirms the scaling: 32.7%→76.0% as human-video data grows from 20 to 100 trajectories. The claim: the coupling can only be *demonstrated* if both subsystems are commanded together — so the data interface is a binding bottleneck, the breadth substrate the coupling-aware policy consumes.

**First-principles framing.**
- **First principle**: A loco-manipulation demonstration requires commanding locomotion and manipulation *simultaneously* — the coupling (base motion that extends reach, balance during manipulation) exists only in the joint trajectory. A fixed-base interface cannot generate it: with the base static, no coupling is ever demonstrated. The interface determines whether the coupling is in the data.
- **Assumption being challenged**: That whole-body data is fixed-base demos plus a separate locomotion controller. Fixed-base-teleop pipelines bet on this; [[2602.10106|EgoHumanoid]]'s +51 pp generalization from whole-body human demos shows a policy trained on decoupled data cannot learn the coupling, because the coupling isn't in the demonstrations.
- **The bet**: A robot-free egocentric pipeline with principled human-to-humanoid alignment lifts loco-manip generalization by [[2602.10106|EgoHumanoid]]'s +51 pp (82% vs 31%) and +19 pp in-domain, and scales data like [[2605.20373|SUGAR]]'s 32.7%→76.0% as human demonstrations grow — coupling learned from demos that contain it, not decoupled data plus a controller.

**Evidence.**
- [[2602.10106|EgoHumanoid]] — Robot-free egocentric demos + human-to-humanoid alignment (depth view + 6-DoF delta-EE + discrete loco); +19 pp in-domain / +51 pp generalization, 100% nav-dominated, ~2× faster than teleop; the robot-free-demo anchor.
- [[2401.02117|Mobile ALOHA]] — Whole-body mobile teleoperation commanding base + bimanual arms simultaneously; >90%, 50%→95% with 50 demos; the whole-body-teleop anchor (also B1).
- [[2505.12748|TeleOpBench]] — Simulator-centric teleop benchmark; 30 bimanual tasks × 4 modalities × 3 humanoids, sim-real correlation; the teleop-evaluation anchor.
- [[2605.20373|SUGAR]] — Human-video-driven generalizable loco-manip; 32.7%→76.0% data scaling, autonomous failure recovery, zero-shot G1; the human-video-scaling anchor.
- [[2605.03452|BifrostUMI]] — Robot-free UMI demonstrations → whole-body humanoid (stepping, torso bending, knee flexion from sparse keypoints); the robot-free-UMI complement.

**Concrete research questions.**
1. **Q1 — Whole-body teleop vs fixed-base + controller.** Compare policies trained on [[2401.02117|Mobile ALOHA]] whole-body teleop demos against fixed-base arm demos + a locomotion controller — does the simultaneously-commanded data deliver the coupling the decoupled data lacks?
2. **Q2 — Human-to-humanoid alignment ablation.** Isolate [[2602.10106|EgoHumanoid]]'s alignment pipeline (view + action alignment) — which component drives the +51 pp generalization, and how much robot data does human-demo co-training replace?
3. **Q3 — Teleop modality trade-offs for loco-manip.** [[2505.12748|TeleOpBench]] compares MoCap/VR/exoskeleton/vision; quantify which modality best captures *simultaneous* loco + manip (vs in-place dexterity), and the data-quality vs cost trade.
4. **Q4 — Optimal human-to-robot sampling ratio.** [[2602.10106|EgoHumanoid]] notes the optimal ratio varies by task precision; characterize the curve — when does precision manipulation need robot demos vs human demos for the loco part?

**Related research papers.**
- [[2602.10106|EgoHumanoid]] — Robot-free egocentric loco-manip demos + alignment; +19/+51 pp; the anchor.
- [[2401.02117|Mobile ALOHA]] — Whole-body mobile teleoperation; >90%, 50%→95%; the whole-body-teleop anchor (also B1).
- [[2505.12748|TeleOpBench]] — Simulator-centric dual-arm teleop benchmark; 30 tasks / 4 modalities / 3 humanoids; teleop-evaluation anchor.
- [[2605.20373|SUGAR]] — Human-video-driven loco-manip; 32.7%→76.0% scaling; human-video-scaling anchor.
- [[2605.03452|BifrostUMI]] — Robot-free UMI → whole-body humanoid; robot-free-UMI complement.
- [[2512.11047|WholeBodyVLA]] — Action-free human egocentric video latent pretraining; +38.7%; the action-free-video complement (feeds A4).
- [[2510.08807|Humanoid Everyday]] — Large humanoid loco-manip dataset (10.3k trajectories / 260 tasks, full-body locomotion + dexterous hands) via Vision-Pro teleop (500 ms→2 ms latency); GR00T N1.5 struggles on loco-manip; the coupled-demo-dataset substrate.
- [[2503.13441|PH2D]] — Robot-free egocentric human demos (~27k via VR) + a transformer co-trained on a shared 54-D human-humanoid space; ~100% relative OOD gain; the human-as-humanoid co-training complement (feeds D3).
- [[2511.09484|SPIDER]] — Physics-informed dexterous retargeting data engine; 2.4 M frames / 800 h; the scaled-data complement (feeds D1).
- [[2603.20147|AGILE]] — Loco-manip workflow standardizing the deployment pipeline; the workflow-substrate for teleop-collected data.

**Benchmarks & metrics.**
- [[2602.10106|EgoHumanoid]] — +19 pp in-domain (78% vs 59%) / +51 pp generalization (82% vs 31%), 100% nav-dominated, ~2× faster collection; the robot-free-demo metric.
- [[2605.20373|SUGAR]] — Kick-Box 32.7%→76.0% (20→100 traj) over 6 loco-manip tasks; the human-video-scaling metric.
- [[2505.12748|TeleOpBench]] — 30 bimanual tasks × 4 modalities × 3 humanoids, sim-real completion-time correlation; the teleop-modality metric.
- [[2510.08807|Humanoid Everyday]] — 10.3k trajectories / 260 tasks / 3 M+ frames with full-body locomotion + dexterous hands; cloud eval shows GR00T N1.5 at 0% on hard loco-manip; the open-world humanoid-loco-manip-data metric.

> [!warning] Risks
> - **Human-humanoid embodiment gap can break alignment** — different proportions and DoF limit transfer. → [[2602.10106|EgoHumanoid]]'s alignment pipeline + co-training bridges it; report the in-domain vs generalization split by alignment quality (couples to D1).
> - **Whole-body teleop is cognitively hard** — commanding base + two arms taxes the operator. → [[2401.02117|Mobile ALOHA]] shows novices reach expert level in ~5 trials; report teleop learning curve + data quality per modality (Q3).
> - **Human demos lack proprioception/force** — egocentric video omits the robot's internal state. → [[2602.10106|EgoHumanoid]] co-trains with robot data for precision; report which tasks need robot-demo refinement (Q4).

### D3 — Cross-Embodiment Whole-Body Policy Transfer

| | |
|---|---|
| **Cluster** | D — Whole-Body Teleoperation & Human-Motion Retargeting |
| **Thesis** | Transfer a whole-body loco-manipulation policy across humanoid morphologies via a phase-anchored or kinematically-aligned shared representation, instead of retraining a per-platform policy from scratch. The reason it must work: whole-body coordination has a morphology-invariant *structure* (phase-clocked balance + end-effector goals) separable from each body's joint realization. The field assumes every new humanoid needs its own whole-body-tracking policy. The bet: a cross-embodiment adapter transfers a pretrained policy at [[2605.23733\|Any2Any]]'s ~1% of from-scratch compute/data across 4 humanoids while matching specialist tracking, via a [[2606.01851\|PHASOR]]-class phase-anchored representation (90.3% R@1, 1.62 mm next-frame). |
| **Anchor surveys** | [[2605.23733\|Any2Any]], [[2606.03476\|Human2Humanoid]], [[2403.10506\|HumanoidBench]] |
| **Key targets** | [[2605.23733\|Any2Any]] adapts pretrained whole-body-tracking across LimX Oli / LimX Luna / G1 / H1 using ~1% of from-scratch compute + data, matching/beating specialists, LoRA into actor backbone; [[2606.01851\|PHASOR]] 90.3% R@1 + 93.9% MRR human→robot retrieval, 1.62 mm next-frame, only method beating raw-kinematics teleop (64.75 mm); [[2606.03985\|Humanoid-GPT]] 92.58% tracking SR / 40.99 mm MPKPE (2 B frames), <1.5 ms inference |

**Why it matters.** Whole-body-tracking policies are trained per-platform — a new humanoid (LimX Oli, LimX Luna, G1, H1) restarts training. But whole-body coordination has a morphology-invariant *structure*: a phase-clocked balance schedule plus end-effector goals that any humanoid shares, separable from the joint angles that realize it on a specific body. [[2605.23733|Any2Any]] proves the transfer is cheap: it adapts pretrained whole-body-tracking policies across four humanoids "using only ~1% of the compute and data required for training from scratch," with comparable or superior tracking and faster convergence, via LoRA into the dynamics-aware actor backbone. [[2606.01851|PHASOR]] supplies the representation: a phase-anchored universal action representation reaches 90.3% R@1, 93.9% MRR on human→robot retrieval, 1.62 mm next-frame pose error, and is "the only approach to outperform a raw-kinematics baseline in teleoperation" (64.75 mm) — the phase embedding is a cross-embodiment invariant. [[2606.03985|Humanoid-GPT]] shows the scaling payoff: trained on 2 billion frames, 92.58% tracking SR and 40.99 mm MPKPE with zero-shot transfer to a real G1 at <1.5 ms inference. The claim: whole-body coordination structure is morphology-invariant, and a shared phase-anchored representation lets a policy amortize across bodies instead of restarting per-platform.

**First-principles framing.**
- **First principle**: Whole-body coordination decomposes into a morphology-invariant structure (a phase-clocked balance schedule + end-effector goals any humanoid shares) and a body-specific joint realization. The structure is the transferable invariant; the joint angles are the per-body projection. A representation anchored to the structure (phase, end-effector) transfers where a joint-space policy cannot.
- **Assumption being challenged**: That every new humanoid needs its own whole-body-tracking policy. The per-platform convention (the from-scratch baseline Any2Any beats) bets on this; Any2Any's ~1%-compute transfer and PHASOR's phase-invariant retrieval show the per-platform assumption is an artifact of joint-space parameterization — the structure is shared, only the realization differs.
- **The bet**: A cross-embodiment adapter transfers a pretrained policy at [[2605.23733|Any2Any]]'s ~1% of from-scratch compute/data across 4 humanoids while matching specialist tracking, via a [[2606.01851|PHASOR]]-class phase-anchored representation (90.3% R@1, 1.62 mm next-frame) — amortization from a morphology-invariant structure, not per-platform retraining.

**Evidence.**
- [[2605.23733|Any2Any]] — Cross-embodiment whole-body-tracking transfer via kinematic alignment + LoRA into the actor backbone; ~1% of from-scratch compute/data across 4 humanoids, matches specialists; the cross-embodiment-transfer anchor.
- [[2606.01851|PHASOR]] — Phase-anchored universal action representation; 90.3% R@1, 1.62 mm next-frame, only method beating raw-kinematics teleop; the phase-invariant-representation anchor.
- [[2606.03985|Humanoid-GPT]] — 2 B-frame scaling for zero-shot motion tracking; 92.58% SR, 40.99 mm MPKPE, <1.5 ms inference, real G1; the scaled-tracking anchor.
- [[2606.03476|Human2Humanoid]] — Morphology-invariant end-effector consistency loss; 88.5% SR, 0.05 cm penetration; the morphology-invariant-objective complement (feeds D1).
- [[2509.26633|OmniRetarget]] — Interaction-preserving retargeting generalizing across tasks/embodiments; 82.20–94.73% downstream; the cross-task-reference complement (feeds D1).

**Concrete research questions.**
1. **Q1 — Phase-anchored vs joint-space transfer.** Compare a [[2606.01851|PHASOR]] phase-anchored representation against joint-space transfer across humanoids — does phase-anchoring deliver the 90.3% R@1 cross-embodiment retrieval where joint-space fails, isolating the structure as the invariant?
2. **Q2 — Adapter (LoRA) injection point.** [[2605.23733|Any2Any]] finds LoRA into the dynamics-aware actor backbone outperforms other PEFT placements; characterize which whole-body pathway (perception / dynamics / output) carries the transferable structure.
3. **Q3 — Transfer cost vs morphology distance.** Sweep the source–target morphology distance against the adaptation cost — does the ~1% compute hold as bodies diverge (G1↔H1 vs G1↔a very different humanoid), and where does it break (couples to D1's morphology-range limit)?
4. **Q4 — Scaling vs transfer.** [[2606.03985|Humanoid-GPT]] scales to 2 B frames for zero-shot; compare scaled-from-scratch vs transfer-from-pretrained — when is cross-embodiment transfer cheaper than scaling a universal model?

**Related research papers.**
- [[2605.23733|Any2Any]] — Cross-embodiment whole-body-tracking transfer; ~1% compute across 4 humanoids; the anchor.
- [[2606.01851|PHASOR]] — Phase-anchored universal action representation; 90.3% R@1, 1.62 mm; phase-invariant anchor.
- [[2606.03985|Humanoid-GPT]] — 2 B-frame scaled zero-shot tracking; 92.58% SR, <1.5 ms; scaled-tracking anchor.
- [[2604.19734|UniT]] — Shared RQ-VAE token space aligning human + humanoid behaviors for cross-embodiment policy; 66.7% RoboCasa, 10× data efficiency, 60% zero-shot stacking; the shared-representation complement to PHASOR.
- [[2606.03476|Human2Humanoid]] — Morphology-invariant end-effector consistency; 88.5% SR; morphology-invariant-objective complement (feeds D1).
- [[2511.07820|SONIC]] — Supersized motion tracking (100 M frames, universal token space); 99.6% OOD tracking, 50/50 zero-shot real G1, 95% mobile-manip with GR00T N1.5; the scaling-end-of-transfer comparator (Q4).
- [[2509.26633|OmniRetarget]] — Cross-task/embodiment interaction-preserving retargeting; 82–94% downstream; cross-task-reference complement (feeds D1).
- [[2511.09484|SPIDER]] — Physics-informed retargeting across 5 hands + 4 humanoids; 2.4 M frames; the cross-embodiment data engine (feeds D1).
- [[2604.07993|HEX]] — Cross-embodiment whole-body manipulation via structured proprioception; 79.8%/61.8%; the cross-embodiment coupling complement (feeds A1).
- [[2602.06341|HiWET]] — Kinematic-Manifold-Prior generalizing across configurations; 12.4 mm; the kinematic-structure complement (feeds A3).

**Benchmarks & metrics.**
- [[2605.23733|Any2Any]] — ~1% of from-scratch compute/data across LimX Oli / Luna / G1 / H1, matches/beats specialist tracking; the cross-embodiment-transfer metric.
- [[2606.01851|PHASOR]] — 90.3% R@1, 93.9% MRR human→robot retrieval, 1.62 mm next-frame, 64.75 mm teleop (only method beating raw-kinematics); the phase-invariant metric.
- [[2606.03985|Humanoid-GPT]] — 92.58% tracking SR, 40.99 mm MPKPE (2 B frames), <1.5 ms inference real G1; the scaled-tracking metric.
- [[2511.07820|SONIC]] — 99.6% OOD tracking (100 M frames / 32k GPU-h / 42 M params), 50/50 zero-shot real-G1 trajectories, 95% mobile-manip via GR00T N1.5 integration; the supersized-tracking-as-foundation metric.

> [!warning] Risks
> - **Morphology distance bounds transfer** — a body too different may share too little structure. → Q3 sweeps morphology distance vs cost; report where ~1% transfer breaks (couples to D1's morphology-range limit).
> - **Phase anchoring may not capture manipulation** — phase is natural for locomotion, less so for fine manipulation. → [[2606.01851|PHASOR]] reports next-frame + teleop precision; report transfer quality on loco-heavy vs manip-heavy tasks separately.
> - **Transfer can underperform a scaled universal model** — at enough scale, one model may beat per-body transfer. → Q4 compares scaling vs transfer; report the crossover, treat transfer as the data/compute-efficient regime, not universally dominant.

### D4 — Whole-Body Synthetic Data Generation

| | |
|---|---|
| **Cluster** | D — Whole-Body Teleoperation & Human-Motion Retargeting |
| **Thesis** | *Synthesize* coupled loco-manipulation demonstrations automatically — adapting a small human seed through whole-body planning, or generating them from 3D assets and video priors — instead of hand-collecting each demo by teleoperation. The reason it must work: a demonstration is just a physically-feasible coupled trajectory, and feasibility (dynamic stability + contact) is something a generator can *enforce*, not something only a human can produce. The field assumes coupled-demo quantity is bounded by the human collection rate. The bet: a whole-body-aware synthesis engine trains to [[2605.27724\|HumanoidMimicGen]]'s 0.89 PSR (vs 0.33 for a manipulation-only generator that ignores whole-body dynamics) and [[2606.05160\|GRAIL]]'s 81.4% manipulation SR (vs 48.5% baseline), with synthetic-only egocentric policies reaching 90% real-world (stair-climb) and sim-and-real co-training lifting real SR 0.51→0.71. |
| **Anchor surveys** | [[2403.10506\|HumanoidBench]], [[2603.20147\|AGILE]], [[2505.12748\|TeleOpBench]] |
| **Key targets** | [[2605.27724\|HumanoidMimicGen]] PSR 0.89 across 9 loco-manip tasks (1,000 generated demos) vs 0.33 DexMimicGen+, sim-and-real co-training 0.51→0.71, ablations drop 0.89→0.49 (no motion noise) / 0.51 (no init randomization); [[2606.05160\|GRAIL]] 81.4% manipulation SR vs 48.5–49.2% baselines (124 motions), 88.9% sim tracking vs 15.8–24.0%, 20,000+ synthesized sequences, real G1 90% stair-climb / 84% seen / 80% unseen pick-up; [[2410.24185\|DexMimicGen]] 90% real humanoid from 40 sim demos vs 0% from 4 source as the bimanual-data-engine precedent |

**Why it matters.** The whole-body data wall (D2) has two exits. D2 takes the first — *capture* coupled demos faster, via whole-body teleoperation or robot-free egocentric rigs — but every demo still costs a human in the loop. The second exit removes the human from the per-demo loop entirely: *synthesize* the coupled trajectory. [[2605.27724|HumanoidMimicGen]] makes the seed-amplification case — it adapts a small set of human-collected whole-body skills to new object poses through whole-body planning (a learned locomotion controller for base motion plus a joint-space upper-body controller), generating 1,000 demos that train to 0.89 PSR across 9 loco-manip tasks, versus 0.33 for an extended **DexMimicGen+** baseline that generates manipulation data without accounting for whole-body dynamics — the whole-body planning is the difference. [[2606.05160|GRAIL]] makes the from-scratch case — it generates robot-compatible 4D human-object-interaction data from 3D assets and video-foundation-model priors, no teleoperation at all, with joint human-object trajectory optimization enforcing contact and depth alignment; egocentric policies trained *solely* on its 20,000+ synthesized sequences hit 81.4% manipulation SR (vs 48.5% baseline) and transfer to a real G1 at 90% (stair-climb) / 84% (seen objects) / 80% (unseen). [[2410.24185|DexMimicGen]] is the precedent the whole-body versions extend: SE(3)-equivariant replay of a few demos in sim drove a real humanoid to 90% from 40 generated demos (vs 0% from 4 source). The claim: a coupled demonstration is a feasible trajectory, feasibility is enforceable by a generator, so the per-demo human is removable — and synthesis is the breadth substrate D1–D2 and Cluster A consume, manufactured rather than collected.

**First-principles framing.**
- **First principle**: A loco-manipulation demonstration is just a physically-feasible coupled trajectory — the same body dynamics ($M(q)$) and contact constraints hold whether a human or a planner authored it. Feasibility (dynamic stability, contact consistency, no penetration) is a *property of the trajectory*, checkable and enforceable, not a property of who made it. So a generator that enforces whole-body feasibility produces training-valid demos — and arbitrarily more than a human can teleoperate.
- **Assumption being challenged**: That coupled-demo quantity is capped by how fast humans collect it. Teleop-fleet and egocentric-rig efforts (D2's route) bet on this; [[2605.27724|HumanoidMimicGen]]'s 1,000-from-a-seed and [[2606.05160|GRAIL]]'s 20,000-from-assets show the cap is artificial — the scarce ingredient is a *feasibility-enforcing generator*, not human hours, and the manipulation-only generator's 0.33 (vs 0.89) shows the generator must model whole-body dynamics to make valid coupled demos.
- **The bet**: A whole-body-aware synthesis engine trains to [[2605.27724|HumanoidMimicGen]]'s 0.89 PSR (vs 0.33 for a manipulation-only generator) and [[2606.05160|GRAIL]]'s 81.4% manipulation SR (vs 48.5% baseline), with synthetic-only egocentric policies reaching 90% real (stair-climb) and sim-and-real co-training lifting real SR 0.51→0.71 — breadth from enforced-feasibility synthesis, not human collection.

**Evidence.**
- [[2605.27724|HumanoidMimicGen]] — Whole-body-planning data generation that adapts a human seed (learned locomotion + joint-space manipulation); 0.89 PSR vs 0.33 DexMimicGen+, co-train 0.51→0.71; the whole-body-MimicGen anchor.
- [[2606.05160|GRAIL]] — Fully-digital pipeline generating robot-ready 4D HOI from 3D assets + video priors; 81.4% manipulation vs 48.5%, 90% real stair-climb from synthetic-only data; the asset-and-video-prior synthesis anchor.
- [[2410.24185|DexMimicGen]] — SE(3)-equivariant demo-replay generating bimanual/dexterous data in sim; 90% real humanoid from 40 generated vs 0% from 4 source; the bimanual-data-engine precedent the whole-body versions extend.
- [[2601.02078|Genie Sim 3.0]] — LLM-driven high-fidelity humanoid simulator with automated scene + task generation; 10,000+ h synthetic data, R²=0.94 sim-real correlation; the simulation substrate whole-body synthesis runs in.
- [[2511.09484|SPIDER]] — Scalable physics-informed dexterous retargeting; 2.4 M frames / 800 h across 5 hands + 4 humanoids, up to 100% SR; the scaled-retargeting data engine that feeds synthesis (also D1/D2).

**Concrete research questions.**
1. **Q1 — Whole-body-aware vs manipulation-only generation.** Isolate [[2605.27724|HumanoidMimicGen]]'s whole-body planning against a manipulation-only generator (DexMimicGen+) on the *same* seed — does modeling whole-body dynamics during generation deliver the 0.33→0.89 PSR, confirming the generator must respect the coupling to produce valid coupled demos?
2. **Q2 — Synthetic-only vs co-trained transfer.** [[2606.05160|GRAIL]] transfers from synthetic-only data while [[2605.27724|HumanoidMimicGen]] co-trains real+synthetic (0.51→0.71); characterize when synthetic-only suffices vs when a real-data anchor is needed, and which task properties (contact precision, dynamics) drive the gap.
3. **Q3 — Randomization yield in synthesis.** [[2605.27724|HumanoidMimicGen]]'s ablations show removing motion noise or initialization randomization drops 0.89→0.49/0.51; sweep randomization breadth against generalization — how much synthesized diversity does a fixed seed support before feasibility breaks?
4. **Q4 — Feasibility enforcement → trainability.** [[2606.05160|GRAIL]]'s contact/depth-aligned optimization yields 0.90% penetration and 88.9% sim tracking; quantify the synthesized-feasibility → downstream-SR curve (couples to D1's interaction-preservation and A2's feasibility-first imitation) — is enforced contact-fidelity what makes synthetic demos trainable?

**Related research papers.**
- [[2605.27724|HumanoidMimicGen]] — Whole-body-planning loco-manip data generation; 0.89 PSR vs 0.33, co-train 0.51→0.71; the anchor.
- [[2606.05160|GRAIL]] — 4D-HOI synthesis from 3D assets + video priors; 81.4% manip, 90% real; the from-scratch-synthesis anchor.
- [[2410.24185|DexMimicGen]] — SE(3)-equivariant bimanual data generation; 90% real from 40 demos; the data-engine precedent.
- [[2604.27711|ExoActor]] — Exocentric video generation as imagined demos → whole-body + hand motion estimation → tracker, no explicit retargeting; the video-generation-as-demo-synthesis route (parallel to GRAIL).
- [[2601.02078|Genie Sim 3.0]] — LLM-driven humanoid sim platform; 10,000+ h, R²=0.94; the simulation substrate.
- [[2511.09484|SPIDER]] — Physics-informed dexterous retargeting data engine; 2.4 M frames / 800 h; the scaled-retargeting engine (feeds D1/D2).
- [[2602.10106|EgoHumanoid]] — Robot-free egocentric demos + alignment; +51 pp generalization; the capture-route counterpart synthesis complements (D2).
- [[2605.20373|SUGAR]] — Human-video-driven loco-manip with data scaling; 32.7%→76.0%; the human-video-as-prior complement (feeds D2).
- [[2605.03452|BifrostUMI]] — Robot-free UMI demos → whole-body humanoid; the low-cost-capture complement to synthesis (D2).
- [[2512.24653|RoboMIND 2.0]] — Bimanual mobile-manipulation dataset across embodiments; up to 1.0; the real-data substrate synthesis augments.
- [[2606.06139|MotionDisco]] — LLM-guided evolutionary contact-plan search + kinodynamic optimization, demonstration-free; 8/8 long-horizon, zero-shot real; the planner-as-data-source route (also A2).

**Benchmarks & metrics.**
- [[2605.27724|HumanoidMimicGen]] — 9-task G1 loco-manip simulation benchmark, 0.89 PSR (1,000 demos) vs 0.33 DexMimicGen+, real co-training 0.51→0.71, randomization ablation 0.89→0.49/0.51; the synthesis-quality metric.
- [[2606.05160|GRAIL]] — 124-motion benchmark, 81.4% manipulation vs 48.5–49.2%, 88.9% sim tracking vs 15.8–24.0%, 0.90% penetration, real G1 90%/84%/80%; the synthetic-only-transfer metric.
- [[2601.02078|Genie Sim 3.0]] — 100,000+ evaluation scenarios, R²=0.94 sim-real (slope 1.025), π0.5 0.67/0.77/0.53 instruction/robustness/complex; the synthesis-platform sim-real-fidelity metric.

> [!warning] Risks
> - **A feasibility-enforcing generator is itself hard to build** — synthesis replaces collection cost with generator-engineering cost. → [[2605.27724|HumanoidMimicGen]] reuses a learned locomotion controller + classical IK/planning; report demos-per-seed and seed-collection cost, so the amortization (one generator, many demos) is the measured win.
> - **Synthetic demos can carry a sim-to-real gap the policy inherits** — generated feasibility ≠ real feasibility. → [[2606.05160|GRAIL]]'s contact/depth alignment + [[2601.02078|Genie Sim 3.0]]'s R²=0.94 bound it; report synthetic-only vs co-trained real SR (Q2), treat the gap as a measured quantity.
> - **Generation diversity is capped by the seed / asset pool** — a narrow seed limits coverage. → Q3 sweeps randomization breadth; [[2606.05160|GRAIL]] widens it with video-prior assets; report generalization vs seed/asset breadth, not single-task SR.

---
## Cross-Cutting Themes

> [!tip] The Coupling Is the Object — Part-Wise Factoring Discards the Load-Bearing Term
> A1, B1, and C1 are three faces of one fact: a humanoid is not an arm bolted to legs. A1 makes the arm–leg inertial coupling ($M(q)$ non-block-diagonal) a predicted quantity; B1 makes the base velocity a manipulation DoF the arm action is conditioned on (autoregressive base→torso→arm); C1 makes the external wrench a whole-body equilibrium term the legs compensate. All three beat part-wise / sequential baselines by modeling the cross-subsystem coupling the factored approach discards — [[2604.07993|HEX]]'s 41.0%→61.8% OOD, [[2503.05652|BRS]]'s 13×/21× over DP3/RGB-DP, [[2505.06776|FALCON (Loco-Manipulation)]]'s 0.60→0.37 — so the coupling, not either subsystem, is the load-bearing term. A4's unified-latent policy is the interface that commands all three couplings jointly.

> [!tip] The Action Target Must Be Feasible Before the Policy Can Use It
> A2, D1, and A3 converge on feasibility-of-the-reference as the binding constraint, inverting the "collect more demonstrations" reflex. A2 composes behavior from frozen *feasible* primitives (softmax convex-hull confinement avoids reward hacking); D1 retargets human motion by preserving *interaction* contact so the reference is realizable; A3 closes the loop in the world frame so the tracked target is drift-free. The evidence is a feasibility→trainability chain: [[2509.26633|OmniRetarget]]'s zero foot-skating → 82–94% downstream RL, [[2604.00202|DreamControl-v2]]'s 68%-vs-8% valid trajectories → 0.925-vs-0.101 RL, [[2606.03476|Human2Humanoid]]'s 0.05 cm penetration → 88.5% SR — fix the target manifold and small data suffices, the same inversion [[Locomotion|Locomotion]]'s motion-imitation direction reaches for pure locomotion.

> [!tip] Structured Decomposition Beats Monolithic Whole-Body Scaling
> A2, A3, B1, and C1 all reject monolithic end-to-end whole-body policies for structured decomposition, because the coupled high-DoF action space is where flat RL fails ([[2403.10506|HumanoidBench]]). A2 blends frozen primitives; A3 splits a world-frame Commander from a whole-body Tracker; B1 factors autoregressively base→torso→arm; C1 decomposes lower/upper agents with shared proprioception. Each reports the decomposition as the source of the win — [[2506.09366|SkillBlender]] avoids reward hacking, [[2602.06341|HiWET]]'s Commander/Tracker hits 12.4 mm, [[2503.05652|BRS]]'s autoregressive factoring mitigates drift, [[2505.06776|FALCON (Loco-Manipulation)]]'s decomposition converges faster than monolithic — the field is converging on structure over scale for the coupled action space.

> [!tip] The Whole-Body Data Wall Is Crossed by Human Video, Synthesis, and Cross-Embodiment Amortization
> A4, B3, D2, D3, and D4 all confront the scarcity of *coupled* loco-manip data, and converge on three levers: human video, automatic synthesis, and cross-body transfer. A4 pretrains on action-free human egocentric video (+38.7%); D2 captures simultaneous loco+manip via whole-body teleop or robot-free egocentric demos (+51 pp generalization); D4 *synthesizes* coupled demos through whole-body planning or from 3D assets + video priors, removing the per-demo human; D3 amortizes a pretrained policy across humanoids at ~1% compute; B3's memory lets one traversal cover a workspace larger than the view. The shared insight — [[2602.10106|EgoHumanoid]]'s +51 pp, [[2512.11047|WholeBodyVLA]]'s +38.7%, [[2605.20373|SUGAR]]'s 32.7%→76.0%, [[2605.27724|HumanoidMimicGen]]'s 0.89 vs 0.33, [[2605.23733|Any2Any]]'s ~1% — is that the coupling must be *in the demonstrations*, whether captured (D2), synthesized with whole-body feasibility enforced (D4), or *transferred from a body that has it* (D3), never assembled from decoupled data, the same human-video substrate the [[Embodied-AI|Embodied-AI]] umbrella's egocentric-pretraining and morphology-invariance directions develop.

> [!tip] Whole-Body Deployment Is Bounded by Hard Physical Constraints the Task Reward Omits
> C2, A3, and B2 surface deployment limits that live *off* the task-success surface. C2 enforces balance + collision as hard constraints via certified projection (the task reward only softly discourages violation); A3's Kinematic Manifold Prior keeps the action kinematically feasible; B2 treats observability as an action because a moving base loses sight of the target. The evidence — [[2604.07457|CMP]]'s 4.7%→46.9% OOD survival from projection, [[2605.25546|ISSf-CBF WBC]]'s collision-free-under-20%-mass-mismatch vs ~50% baseline, [[2306.11565|HomeRobot]]'s 5–15%→0.4–0.6% perception collapse — shows deployability is bounded by constraints (balance, collision, observability) the task reward silently ignores, the same embodiment-cost insight [[Locomotion|Locomotion]]'s force/thermal direction raises for pure locomotion.

> [!tip] Data Is the Breadth Substrate, Explicit Coupling Is the Build — on a Fixed Budget the Idea Beats the Data
> On a *fixed* data budget, the architectural idea moves whole-body capability more than data volume, and the sharpest evidence is internal to this doc's anchors. [[2604.07993|HEX]]'s ablation: removing the coupling component (UPP) costs **−5/12** on Pouring (the largest single-component drop), while its 12M-frame pretraining adds only **+1/12** at convergence — "pretraining mainly improves optimization efficiency rather than the final converged performance." [[2503.05652|BRS]] reports up to a **53%** drop from removing autoregressive decoding *on identical JoyLo data*. [[2505.06776|FALCON (Loco-Manipulation)]] gets its **~2×** tracking gain from dual-agent decomposition with *zero* demonstration data. Two head-to-head tests put the idea above the data: [[2603.12263|Psi0]] beats a competitor trained on **>10×** more data by **+40%** via a *data recipe*, and [[2511.05275|TwinVLA]] beats proprietary bimanual data with a cheap coordination term and *zero* bimanual pretraining. What data uniquely buys is generalization *breadth* — [[2602.10106|EgoHumanoid]]'s **+51 pp** (82% vs 31%) from adding robot-free human demos to a fixed policy is real and architecture-on-fixed-data cannot manufacture it — but breadth is a *substrate*, not the contribution. The reorder: **A1's thin explicit coupling is the build, A4 the interface that grounds into it, D2/D1 the breadth substrate the method consumes** — the scarce, idea-bound contribution is making the coupling *explicit*, not collecting more demos. ([[2511.05275|TwinVLA]] proves the coupling is thin: a cheap explicit term beats a coupling-is-everything model trained on far more data.)

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| No benchmark isolates the *arm-as-balance-disturbance* coupling — measuring balance error as a function of reach aggressiveness | A1 | [[2604.07993\|HEX]] (7 ID + 8 OOD whole-body tasks, but coupling not isolated from task SR) |
| No standardized loco-manip skill-composition suite separating reward-hacking from feasibility across embodiments | A2 | [[2506.09366\|SkillBlender]] / SkillBench (8 tasks / 3 embodiments, but accuracy+feasibility not decomposed by primitive coverage) |
| No long-horizon world-frame end-effector-precision benchmark with base-disturbance-vs-distance breakdown | A3 | [[2602.06341\|HiWET]] (12.4 mm world-frame, but no error-vs-locomotion-distance curve) |
| No benchmark measuring loco-vs-manip latent separation in a unified policy (different-visual-dynamics claim untested) | A4 | [[2512.11047\|WholeBodyVLA]] (78.0% on 3 tasks, but separate-vs-shared-LAM not benchmarked) |
| No mobile-manip benchmark separating action-coupling gain from perception gain (GT-vs-real perception ablation) | B1 | [[2503.05652\|BRS]] (88% sub-task, but action-coupling vs perception not factored) |
| No benchmark for active-gaze-vs-fixed-camera on observability-critical mobile-manip tasks | B2 | [[2603.03243\|HoMMI]] (90%/85%/80%, active-head ablation, but not a standardized active-perception suite) |
| No long-horizon multi-room mobile-manip memory benchmark with relocated-object protocol | B3 | [[2411.04999\|DynaMem]] / DynaBench (70% dynamic, 74.5% query, but single-room scope) |
| No whole-body force-adaptation benchmark with a torque-limit-aware-curriculum-vs-naive ablation under graded wrench | C1 | [[2505.06776\|FALCON (Loco-Manipulation)]] (0.37 vs 0.60 under force, but curriculum ablation not standardized) |
| No certified-safety-vs-reward-shaping benchmark for whole-body control under OOD load + model mismatch | C2 | [[2604.07457\|CMP]] (86.7% extreme OOD, 2.99 ms, but no shared safety-coverage protocol) |
| No interaction-preservation benchmark tying contact-fidelity (penetration/foot-skating) to downstream-RL trainability | D1 | [[2509.26633\|OmniRetarget]] (82–94% downstream, zero foot-skating, but feasibility→trainability curve not standardized) |
| No simultaneous-loco+manip teleop-modality benchmark (vs in-place dexterity) with data-quality-vs-cost | D2 | [[2505.12748\|TeleOpBench]] (30 tasks / 4 modalities / 3 humanoids, but in-place-dexterity-focused) |
| No cross-embodiment whole-body-transfer benchmark with morphology-distance-vs-adaptation-cost sweep | D3 | [[2605.23733\|Any2Any]] (~1% compute across 4 humanoids, but morphology-distance not swept) |
| No whole-body synthetic-data benchmark tying generated feasibility (penetration/stability) to downstream SR, with synthetic-only-vs-co-trained and whole-body-vs-manipulation-only-generator ablations | D4 | [[2605.27724\|HumanoidMimicGen]] (0.89 vs 0.33 on a 9-task suite, but feasibility→trainability curve and generator-type ablation not standardized) |

---

## Cross-References

- [[02_Dataset-Benchmark-Environment#8. Bimanual & Humanoid Evaluation|02_Dataset-Benchmark-Environment §8]] — Bimanual & humanoid evaluation (HumanoidBench, BRS, BiGym and whole-body suites feeding all four clusters)
- [[02_Dataset-Benchmark-Environment#1. Cross-Embodiment Scale Datasets|02_Dataset-Benchmark-Environment §1]] — Cross-embodiment scale datasets (the whole-body-portability substrate for D3 + Cluster A)
- [[02_Dataset-Benchmark-Environment#12. Sim-to-Real Transfer Evaluation|02_Dataset-Benchmark-Environment §12]] — Sim-to-real transfer evaluation (the deployment gate for every direction here)
- [[09_Contact-Rich-and-Whole-Body-Control#3. Force-Conditioned VLA Architectures|09_Contact-Rich-and-Whole-Body-Control §3]] — Force-conditioned VLA architectures (the force-modeling machinery feeding Cluster C)
- [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]] — Force-aware design space; the force/contact deep-dive underpinning Cluster C
- [[14_Sim-to-Real-Transfer#3. Policy-Side: Robustness & Domain Randomization|14_Sim-to-Real-Transfer §3]] — Policy-side robustness + domain randomization (the safety/robustness machinery feeding C1, C2)
- [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]] — Sim-to-real design space; the transfer deep-dive underpinning Clusters C + D
- [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Robotics & embodied-AI topic overview
- [[Manipulation|Manipulation]] — Sibling Manipulation subsystem; its **Bimanual & Dual-Arm Coordination** and **Dexterous & In-Hand Control** clusters are the arms + hands this doc coordinates with the legs — the upper-body manipulation this whole-body coupling integrates.
- [[Locomotion|Locomotion]] — Sibling Locomotion subsystem; its **Bipedal Locomotion & Dynamic Skills** cluster is the legs this doc couples to the arms — the lower body whose balance the manipulation disturbs.
- [[Embodied-AI|Embodied-AI]] — Umbrella embodied-AI directions; this doc cross-references its policy and morphology-invariance directions (A4 grounds the policy interface; D3 is the whole-body face of morphology-invariance).
- [[WAM|WAM]] — World-action-model substrate; A1's coupling prediction and A4's latent loco-manip imagination borrow the world-model imagination and calibration threads.
- [[Sim2Real|Sim2Real]] — Sim-to-real / real-to-sim transfer; owns the domain-randomization vs real-residual machinery under C1/C2's force-adaptive deployment and D1/D3's retargeting-and-transfer sim-to-real.

> [!example] Humanoid reading path
> The humanoid is read across all three subsystem docs. Its **legs** — whole-body balance, terrain traversal, dynamic agile skills, fall-recovery — are in [[Locomotion|Locomotion]] (the **Bipedal** cluster). Its **arms + hands** — two-arm coordination and multi-fingered in-hand control — are in [[Manipulation|Manipulation]] (the **Bimanual** + **Dexterous** clusters). And the **whole-body coupling that integrates them** — the arm reach that disturbs balance (A), the base that extends the manipulation workspace (B), the legs that compensate for the force the arms feel (C), and the human motion retargeted onto the coupled body (D) — is **this** doc (Loco-Manipulation + Mobile Manipulation + Force-Adaptive Control). Read Locomotion for the legs, Manipulation for the arms, and this doc for the coordination that makes them one body.
