---
title: "Promising Research Directions: Sim-to-Real & Real-to-Sim Transfer"
aliases:
  - "Sim2Real Research Directions"
  - "Sim-to-Real Promising Directions"
  - "Reality-Gap Research Directions"
tags:
  - research-directions
  - sim-to-real
  - real-to-sim
  - embodied-AI
---

# Promising Research Directions: Sim-to-Real & Real-to-Sim Transfer

> [!abstract] Overview
> Fifteen research directions across five clusters, ordered by *when* each acts on the reality gap: **train** (A — robustness beyond domain randomization), **reconstruct** (B — invert reality into the simulator), **measure** (C — treat the gap as statistical inference), **deploy** (D — close the residual online), and **bound** (E — act safely under what is left). The framing makes two moves the field usually skips. First, real→sim is a *first-class* gap, not a sub-topic — how well you run reality backward into the simulator now caps how well it predicts forward. Second, the residual gap that survives the first four stages is a *safety* problem at deploy-time, not just a performance one. Each direction states a measurable bet against the consensus, and every number is sourced from a cited `_KnowledgeHub_/{ID}.md` note — never invented. Anchors: the real2sim2real frontier ([[2503.17973|PhysTwin]], [[2511.07416|PhysWorld]], [[2510.11689|Phys2Real]], [[2604.27367|DOT-Sim]], [[2511.04665|Real-to-Sim GS]], [[2605.26638|HyperSim]]) and the online-adaptation + runtime-safety literature ([[2107.04034|RMA]], [[2409.16578|FLaRe]], [[2508.21065|Learning on the Fly]], [[2602.20057|AdaWorldPolicy]], [[2503.10949|SCDA]], [[2409.19190|RAIL]], [[2506.09937|SAFE]]).

## Methodology

**Corpus.** 6 sim-real surveys + 17 sim-real correlation/evaluation benchmarks + ~25 anchor methods (real2sim2real, DR-beyond, online adaptation, runtime safety) from `_KnowledgeHub_/`, cross-checked against [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]], [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]], and [[08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]]. Directions are ordered by when each acts on the gap: **train → reconstruct → measure → deploy → bound**.

- **Survey scan**: `survey` × {`sim-to-real`, `robotics`, `world-model`, `domain-adaptation`, `manipulation`} across `_KnowledgeHub_/`.
- **Deep-dive mining**: full read of [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]], plus [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] and [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]] for the physics/tactile threads.
- **Baseline anchoring**: each direction's bet must beat a named frontier method ([[2511.04665|Real-to-Sim GS]], [[2605.26638|HyperSim]], [[2604.27367|DOT-Sim]], [[2510.11689|Phys2Real]], [[2511.07416|PhysWorld]], [[2512.19562|REALM]]) or an online-adaptation/safety anchor ([[2107.04034|RMA]], [[2409.16578|FLaRe]], [[2508.21065|Learning on the Fly]], [[2602.20057|AdaWorldPolicy]], [[2503.10949|SCDA]], [[2409.19190|RAIL]], [[2506.09937|SAFE]], [[2503.08558|FAIL-Detect]]).
- **Filter**: kept directions with 3–10 attacking papers but no consensus solution; dropped saturated (more-DR-only) and premature (sim-from-scratch-with-full-causality) framings; favored intersections (rendering×physics, real2sim×differentiable-ID, twin×co-training, eval×provable-inference).

---

## Sim-to-Real Survey Landscape

| Survey | Sub-theme | Key open problems |
|---|---|---|
| [[2604.26509\|3D Generation for Embodied AI Survey]] | A: Forward S2R | Simulation-readiness over visual fidelity; scarcity of physical annotations; geometry-vs-physical-validity trade-off; deformable-asset generation; persistent sim-to-real domain gap; generative digital twins as the real2sim bridge |
| [[2601.07823\|Video Generation in Robotics Survey]] | A: Forward S2R | Hallucinations + physics violations; uncertainty quantification; long-video generation; compute cost; robotics-centric benchmarks; physics priors as the integration fix |
| [[2507.10087\|Foundation Robotics Review]] | A: Forward S2R | Scarcity of robot-specific embodied data; sim2real gap via semantic alignment + generative simulation; physical-grounding-data limits; safety from model hallucinations |
| [[2604.04974\|Video-to-Control Survey]] | B: Real2Sim2Real | Robotics integration layer is the critical gap; latent-action identifiability; physical-consistency / hallucinated-physics; pre-execution verification; lack of standardized comparable eval protocols |
| [[2605.00080\|WM Robot Learning Survey]] | B: Real2Sim2Real | world models as learned simulators/evaluators; sim2real gap in long-horizon; eval beyond visual fidelity (action faithfulness + physical consistency); open-loop vs closed-loop divergence |
| [[2502.10694\|UDA Simulation Study]] | C: Gap measurement | Domain-shift degradation; method effectiveness is context-dependent (backbone, shift type, domain); "negative adaptation" under noisy source — DA can do worse than no DA |

> [!tip] Convergence patterns
> - **The reality gap is bidirectional; real→sim is the newer, less-measured edge** (4-way): [[2512.19562|REALM]] explicitly names a *real-to-sim gap* ("low visual fidelity and misaligned control dynamics") distinct from the forward gap; [[2604.26509|3D Generation for Embodied AI Survey]] frames *generative digital twins* as the real2sim bridge; [[2511.04665|Real-to-Sim GS]] measures it directly (r=0.915 vs [[2511.04831|Isaac Lab]]'s r=0.649 on the same T-block task); [[2605.26638|HyperSim]] treats reconstruction fidelity as the lever that moves zero-shot SR from 75% to 95%. The field is realizing that *how well you can run reality backward into the simulator* now gates *how well the simulator predicts reality forward*.
> - **Sim fidelity ≠ transfer quality; optimized proxies are mis-specified** (4-way): [[2604.02523|Tune to Learn]] shows stiff gains yield the *lowest* system-identification error yet the *worst* sim-to-real transfer — the optimized objective is the wrong one; [[2604.10856|BridgeSim]] decomposes the open-loop→closed-loop gap into observational shift + objective mismatch; [[2604.11674|AffordSim]] shows the best affordance-aware policy reaches only ~24% average zero-shot real SR (mug-hang ~10%) even with 3DGS-randomized backgrounds (a low ceiling); [[2604.21686|WorldMark]] finds control-alignment leaders are not visual-quality or world-consistency leaders — no single proxy ranks correctly. The quantity we minimize is not the quantity that transfers.
> - **Sim-to-real evaluation is becoming statistical inference** (4-way): [[2604.24018|Sim2Real Betting]] reframes evaluation as sequential betting over a *bank of biased simulators* (70–100% win rate over Monte Carlo); [[2510.04354|SureSim]] formalizes it as Prediction-Powered Inference with finite-sample-valid confidence intervals (20–25% fewer real trials); [[2509.15273|Embodied Arena]] builds a unified evolving evaluation system across 22+ benchmarks; [[2405.05941|SIMPLER]] establishes Pearson r + MMRV as the correlation/ranking proxy. The question is shifting from "is the sim accurate?" to "what can I provably infer about real performance from imperfect sims?"
> - **Differentiable rendering + physics collapse system-ID into gradient descent** (4-way): [[2604.27367|DOT-Sim]] calibrates sensor constitutive parameters via differentiable MPM from few real demos; [[2510.11689|Phys2Real]] fuses VLM physical priors with online inverse-variance-weighted adaptation; [[2503.17973|PhysTwin]] jointly optimizes geometry + physical parameters + appearance from video; [[2511.04665|Real-to-Sim GS]] optimizes 3DGS appearance + soft-body physical parameters jointly. Manual sysID is being replaced by end-to-end gradient recovery of both appearance and dynamics.

---

## Formal Framing

The reality gap is a divergence between two distributions over trajectories. Let $\tau = (o_0, a_0, o_1, \dots)$ be a rollout. A policy $\pi$ induces a real distribution $p_{\text{real}}(\tau \mid \pi)$ on hardware and a simulated distribution $p_{\text{sim}}(\tau \mid \pi)$ in a simulator parameterized by $\phi$ (appearance) and $\psi$ (dynamics). The **forward (sim-to-real) gap** is the performance divergence when a policy trained under $p_{\text{sim}}$ is deployed under $p_{\text{real}}$; the **inverse (real-to-sim) gap** is the reconstruction error in recovering $(\phi^\star, \psi^\star)$ such that $p_{\text{sim}}(\cdot \mid \phi^\star, \psi^\star) \approx p_{\text{real}}$.

$$\text{Gap}_{\text{S2R}}(\pi) = J_{\text{real}}(\pi) - J_{\text{sim}}(\pi), \qquad \text{Gap}_{\text{R2S}} = \min_{\phi, \psi}\; \mathcal{D}\!\left(p_{\text{real}} \,\|\, p_{\text{sim}}(\cdot \mid \phi, \psi)\right)$$

**Robotics-centered world-model definition** — [[2605.00080|WM Robot Learning Survey]]:

> "The true value of a world model in embodied AI is contingent on its utility for action and physical consistency, not solely on visual realism or generic perceptual prediction quality." — [[2605.00080|WM Robot Learning Survey]]

| Object | What it measures | Canonical instrument |
|---|---|---|
| **Correlation** $\rho$ | Does sim SR track real SR? | Pearson r — [[2405.05941\|SIMPLER]] r≥0.85, [[2605.06311\|VISER]] r=0.92 |
| **Ranking fidelity** | Does sim order policies correctly? | MMRV (Mean Maximum Rank Violation) — [[2405.05941\|SIMPLER]], [[2512.19562\|REALM]] |
| **Reconstruction fidelity** $\text{Gap}_{\text{R2S}}$ | How well does real run backward into sim? | r vs [[2511.04831\|Isaac Lab]] baseline — [[2511.04665\|Real-to-Sim GS]] 0.915 vs 0.649 |
| **Provable real bound** | What CI can I assert on real SR? | PPI / betting — [[2510.04354\|SureSim]], [[2604.24018\|Sim2Real Betting]] |

**Interface taxonomy** — [[2604.04974|Video-to-Control Survey]]:

> "The most critical unresolved gaps reside in the 'robotics integration layer,' which involves reliably connecting video-derived predictions to dependable robot behavior, encompassing grounding, loop closure, and physical feasibility." — [[2604.04974|Video-to-Control Survey]]

The transfer operator that closes $\text{Gap}_{\text{R2S}}$ then re-opens $\text{Gap}_{\text{S2R}}$ for free is the real2sim2real loop: recover $(\phi^\star, \psi^\star)$ from real data, train/evaluate in the grounded twin, deploy back. Cluster B is exactly the engineering of that operator; Cluster A attacks $\text{Gap}_{\text{S2R}}$ directly without inverting; Cluster C measures both as inference problems.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Forward Sim-to-Real: Robustness Beyond DR** | A1, A2, A3 | DR randomizes appearance, not semantics or dynamics structure | A1's neural-rendering semantics + A2's transferable physics rewards both attack what DR misses; A3's controller-gain insight is the unrecognized hyperparameter governing whether A1/A2 even transfer; [[2604.02523\|Tune to Learn]]'s gains-vs-sysID finding is the shared warning |
| **B — Real-to-Sim-to-Real: Grounding the Simulator** | B1, B2, B3, B4 | Recovering $(\phi^\star, \psi^\star)$ from real data is the new bottleneck | B2 recovers the *parameters* of a fixed law while B4 recovers the *law itself*, generalizing the $\psi^\star$ that B1's reconstruction needs; B3's co-training loop is the deployment engine that consumes both; [[2511.04665\|Real-to-Sim GS]] is the joint-fidelity substrate, [[2304.14369\|NCLaw]] the generalizable-dynamics model B4 feeds back into it |
| **C — Reality-Gap Measurement as Inference** | C1, C2 | High in-distribution r, untested under deliberate shift, no provable bound | C1 stress-tests whether each sim's per-factor correlation is valid, then turns that diagnosis into a deployment gate that routes which sim to trust per factor; C2's portfolio of biased sims is the estimator C1's gate feeds per-factor weights into; [[2604.24018\|Sim2Real Betting]] supplies both C2's estimator and C1's routing target; both reframe eval from accuracy to inference |
| **D — Deployment-Time Adaptation: Closing the Residual Gap Online** | D1, D2, D3 | The residual gap that survives A/B/C is time-varying and only observable at deploy-time | D1's proprioception-only latent-extrinsics estimator, D2's differentiable-sim TTA, and D3's world-model-supervised correction are three online engines that consume A/B/C's offline products and adapt the residual that none of them can pre-remove; [[2603.04029\|Self-Adapting RL]] is the shared residual-trigger primitive |
| **E — Risk-Bounded Sim-to-Real Deployment: Safety Under the Irreducible Gap** | E1, E2, E3 | C measures the residual; an un-handled residual is a *safety* failure, not just a performance one | E1's safety-constrained continual adaptation hardens D1/D3's online updates against unsafe exploration, E2's reachability shield bounds execution under the residual, and E3's conformal runtime detector flags residual-induced failure with no failure labels; all three convert C's per-factor untrustworthiness into a runtime guarantee |

---

## Cluster A — Forward Sim-to-Real: Robustness Beyond Domain Randomization

*Attack the forward gap directly — transfer what is invariant (semantics, physics rewards, control structure) rather than randomizing what is not.*

### A1 — Hybrid Neural-Rendering + Physics Simulators for Semantic Sim-to-Real

| | |
|---|---|
| **Cluster** | A — Forward Sim-to-Real |
| **Thesis** | Affordance tasks fail in the real world because domain randomization shuffles pixels but never the object's *function* — a mug's handle-affordance survives every lighting and texture change, so it is never randomized. The field assumes visual robustness implies semantic robustness; it does not. The bet: a neural-rendering-in-the-loop simulator (3DGS + physics) that randomizes affordance and material *semantics* — not appearance — lifts affordance-task real SR by >20 pp over [[2604.11674\|AffordSim]]'s ~24%-average zero-shot ceiling, where appearance-only DR has plateaued. |
| **Anchor surveys** | [[2604.26509\|3D Generation for Embodied AI Survey]], [[2601.07823\|Video Generation in Robotics Survey]], [[2507.10087\|Foundation Robotics Review]] |
| **Key targets** | Affordance-task real SR from ~24% average / 25% best-policy ([[2604.11674\|AffordSim]] zero-shot), mug-hang ~10%, by >20 pp; match [[2605.26638\|HyperSim]]'s 75%→95% zero-shot-to-few-shot trajectory; [[2605.06311\|VISER]] r=0.92 visual-realism floor; [[2604.25459\|GS-Playground]] 90% real SR throughput reference |

**Why it matters.** [[2604.11674|AffordSim]] is the clean diagnostic: even with affordance-aware data and 3DGS-randomized backgrounds, the best zero-shot policy ([[2504.16054|π0.5]]) reaches only 25% (24% averaged), and the hardest task — mug hanging — sits at ~10% (pour ~30%, place ~40%). The reason is structural: DR perturbs lighting, texture, and pose, but a mug's handle-affordance is a *semantic* property that survives every appearance change, so it never gets randomized. [[2604.26509|3D Generation for Embodied AI Survey]] names the same shift — "interaction readiness, physical grounding, and simulator compatibility" matter more than visual fidelity, and the bottleneck is "scarcity of physical annotations." The rendering frontier supplies the substrate ([[2604.25459|GS-Playground]] runs batch 3DGS at 10,000 FPS, 90% real SR; [[2605.06311|VISER]] hits r=0.92 with ray-traced PBR) — but neither randomizes semantics. The open move: put rendering in the loop with a physics engine and randomize affordance and material structure, not the pixels on top.

**First-principles framing.**
- **First principle**: Task success depends on appearance-invariant properties — affordances, mass distribution, material response are the *causes* of manipulation outcomes; pixels are downstream effects. Randomizing effects cannot cover variation in causes.
- **Assumption being challenged**: That appearance-DR is the right axis of robustness. Every appearance-randomized pipeline believes "randomize enough nuisance variation and the policy generalizes" — but [[2604.11674|AffordSim]]'s ~24%-average ceiling (mug-hang ~10%) shows the nuisance axis and the task axis are orthogonal.
- **The bet**: A 3DGS-in-the-loop simulator that randomizes affordance and material *semantics* lifts affordance-task real SR >20 pp over appearance-only DR — pushing [[2604.11674|AffordSim]]-class tasks above the ~24% ceiling toward [[2605.26638|HyperSim]]'s 95%-with-few-real regime, at [[2604.25459|GS-Playground]]-class throughput.

**Evidence.**
- [[2604.11674|AffordSim]] — Best zero-shot policy ([[2504.16054|π0.5]]) 25% (24% averaged); affordance tasks degrade most (mug-hang ~10%, pour ~30%, place ~40%) even with 3DGS backgrounds — the appearance-DR ceiling.
- [[2604.25459|GS-Playground]] — Batch 3DGS at 10,000 FPS, 90% real SR, Gaussians bound to rigid bodies — the in-the-loop rendering substrate.
- [[2605.06311|VISER]] — Ray-traced PBR raises correlation to r=0.92 with 1,000+ assets; realism, not semantics.
- [[2604.26509|3D Generation for Embodied AI Survey]] — "Simulation readiness" over visual fidelity; names physical-annotation scarcity as the bottleneck.

**Concrete research questions.**
1. **Q1 — Affordance-randomized 3DGS-in-the-loop.** Couple [[2604.25459|GS-Playground]]'s renderer to a physics engine, randomize affordance labels + material parameters per episode, and compare affordance-task real SR vs appearance-only DR at matched render budget.
2. **Q2 — Semantic-vs-appearance ablation.** Hold [[2605.06311|VISER]]-class PBR fixed, vary only the semantic axis; isolate how much gain is semantics vs realism.
3. **Q3 — Affordance labels from generation.** Can [[2604.11674|AffordSim]]'s VoxAfford scorer auto-label [[2604.26509|3D Generation for Embodied AI Survey]]-style assets, closing the annotation bottleneck?

**Related research papers.**
- [[2604.11674|AffordSim]] — Affordance-aware data generator; collection SR 98/79/64% (Easy/Medium/Hard) vs [AnyGrasp](https://arxiv.org/abs/2212.08333) 67/15/3%; ~24% zero-shot real ceiling.
- [[2604.25459|GS-Playground]] — Batch-3DGS simulator + Image-to-Physics real2sim; 90% real SR; renders semantics-agnostic.
- [[2605.06311|VISER]] — Ray-traced PBR benchmark, r=0.92, 1,000+ assets; realism without semantic randomization.
- [[2605.26638|HyperSim]] — 3DGS background + constraint-aware foreground + adversarial trajectories; 75%→95% with 35 demos.
- [[2511.04831|Isaac Lab]] — GPU sim at 900K–1.6M FPS with RTX rendering; the physics backbone an in-the-loop renderer attaches to.
- [[2506.18088|RoboTwin 2.0]] — MLLM-generated tasks + 5-axis DR; +24.4% real few-shot; the strong DR baseline to beat on semantic tasks.
- [[2604.26509|3D Generation for Embodied AI Survey]] — Simulation-readiness taxonomy; survey, no method.
- [[2603.13825|Explicit-WM Manipulation]] — Digital-twin construction ([Hunyuan3D](https://arxiv.org/abs/2501.12202) + [[2304.07193|DINOv2]] alignment); 75%+ on 6/9 tasks; semantics via VLM, not randomized in sim.

**Benchmarks & metrics.**
- [[2604.11674|AffordSim]] — 50-task affordance benchmark; ~24%-average zero-shot real (best 25%, mug-hang ~10%); the ceiling to break.
- [[2605.06311|VISER]] — r=0.92 correlation, OOD degradation under scene complexity; visual-realism floor.
- [[2402.08191|THE COLOSSEUM]] — 20 tasks × 14 perturbation factors; 30–50% single-perturbation SR drop, R²=0.614 sim↔real; semantic perturbation coverage to extend.

> [!warning] Risks
> - **Neural rendering in the loop is compute-heavy** — physics + 3DGS per step may blow the training budget. → Mitigate via [[2604.25459|GS-Playground]]'s point-pruning + batch rendering (10,000 FPS shows it is tractable) and discard auxiliary heads at deploy.
> - **Semantic randomization needs semantic ground truth** the field lacks at scale. → Bootstrap from [[2604.11674|AffordSim]]'s VoxAfford auto-labeling on [[2604.26509|3D Generation for Embodied AI Survey]]-style generated assets rather than hand-annotating.
> - **Gains may be confounded with realism** — a richer renderer could improve SR for reasons unrelated to semantics. → Q2's semantics-vs-appearance ablation at fixed PBR rendering is the go/no-go.

### A2 — Reward-Signal Sim-to-Real: Transferring PINN-Estimated Physics Rewards, Not Actions

| | |
|---|---|
| **Cluster** | A — Forward Sim-to-Real |
| **Thesis** | Sim-to-real almost always transfers *actions* — a policy or its distilled student. But physical laws hold identically in sim and real while action distributions do not, so the policy is not the only thing that can cross the gap. The bet: a PINN-estimated physics *reward* (e.g. ground-reaction force) transfers across *conditions* — footwear, terrain, payload — where action policies fail. Target: match [[2604.23702\|QuietWalk]]'s R²>0.98 sensor-free GRF accuracy as a reward that holds the −7.17 dBA objective across all 4 footwear types and outdoor terrains the policy never trained on. (Cross-*embodiment* reward portability is the open extension, Q2 — no existence proof yet.) |
| **Anchor surveys** | [[2601.07823\|Video Generation in Robotics Survey]], [[2507.10087\|Foundation Robotics Review]], [[2605.00080\|WM Robot Learning Survey]] |
| **Key targets** | GRF-predictor R²>0.9887/0.9899 sensor-free ([[2604.23702\|QuietWalk]]); −7.17 dBA noise reduction transferred across 4 footwear types; cross-condition reward stability where DR action policies plateau |

**Why it matters.** Every sim-to-real pipeline in the corpus transfers *actions* — [[2511.15200|VIRAL]] distills a teacher into a vision student, [[2603.15956|ExpertGen]] distills experts into visuomotor policies, [[2210.13702|DeXtreme]] transfers a PPO policy. The thing crossing the gap is always the policy. [[2604.23702|QuietWalk]] does something else: a PINN estimates per-foot ground-reaction force from proprioception alone at R²=0.9887/0.9899, the frozen predictor is dropped *into the reward*, and the policy then generalizes across four footwear types and outdoor terrains it never trained on. The PINN encodes inverse dynamics — a physical law — so its output is invariant to the appearance and embodiment changes that wreck action transfer. [[2605.00080|WM Robot Learning Survey]] says a model's value is "its utility for action and physical consistency, not visual realism." A transferable reward *is* the physical law, and the law holds in real even when the trained action distribution does not.

**First-principles framing.**
- **First principle**: A reward grounded in a physical law (momentum, Newton's third law, contact mechanics) is a function of physical state, not of training distribution — it scores *any* trajectory correctly, on hardware the policy never saw. Actions are distribution-bound; physics-grounded rewards are distribution-free.
- **Assumption being challenged**: That the policy is the transferable object. The teacher-student / DR-distillation orthodoxy ([[2511.15200|VIRAL]], [[2603.15956|ExpertGen]], [[2210.13702|DeXtreme]]) hardens the action mapping against the gap — but a policy hardened on *simulated* dynamics still inherits the dynamics gap, whereas a PINN-estimated force reward re-grounds in real physics at deployment.
- **The bet**: A PINN-estimated physics reward (GRF, contact wrench) transfers and generalizes across *conditions* where action policies don't — matching [[2604.23702|QuietWalk]]'s R²>0.98 sensor-free accuracy as a reward holding the −7.17 dBA objective across 4 footwear types and outdoor terrains. (Cross-*embodiment* portability — robot A's PINN as robot B's reward — is the speculative extension Q2 probes; [[2604.23702|QuietWalk]] shows only single-robot cross-condition transfer.)

**Evidence.**
- [[2604.23702|QuietWalk]] — Inverse-dynamics PINN estimates GRF from proprioception (R²=0.9887/0.9899, RMSE 14.49/14.00 N); frozen predictor → reward; generalizes across 4 footwear + outdoor terrains — the transferable-reward existence proof.
- [[2511.15200|VIRAL]] — Teacher-student visual sim-to-real (54/59 cycles); RSI ablation 95% vs <10% — the canonical *action*-transfer pipeline this contrasts with.
- [[2603.15956|ExpertGen]] — Behavior prior + DSRL + distillation; 90.5% [AutoMate](https://arxiv.org/abs/2407.08028) — action transfer, reward stays sparse.
- [[2605.00080|WM Robot Learning Survey]] — Model value is "utility for action and physical consistency, not visual realism" — the rationale for physics-grounded transfer.

**Concrete research questions.**
1. **Q1 — Physics-reward vs action transfer head-to-head.** Train two policies on the same contact task — one with [[2604.23702|QuietWalk]]-style PINN-force reward, one with DR + distillation ([[2511.15200|VIRAL]]-style); compare cross-condition real SR retention.
2. **Q2 — Reward portability across embodiments.** Does a GRF/contact-wrench PINN trained on robot A's proprioception give a usable reward on robot B without re-collecting demos? Map the transfer envelope.
3. **Q3 — Sensor-free reward at deployment.** Use the estimated force as the *only* reward on hardware lacking force sensors; measure how far R² degrades off-manifold and where the reward stops being trustworthy.

**Related research papers.**
- [[2604.23702|QuietWalk]] — PINN GRF predictor (R²>0.98) frozen into RL reward; −7.17 dBA, 4-footwear robust; the transferable-reward anchor.
- [[2511.15200|VIRAL]] — Visual sim-to-real, teacher→student; 54/59 cycles; action transfer.
- [[2603.15956|ExpertGen]] — Behavior prior + DSRL + distillation; 90.5% [AutoMate](https://arxiv.org/abs/2407.08028); action transfer.
- [[2210.13702|DeXtreme]] — VADR + PPO in-hand reorientation; 27.8 vs 14.8 (VADR vs manual DR); action transfer, hand-designed reward.
- [[2511.07416|PhysWorld]] — Object-centric residual RL on a reconstructed world model; 82% real; reward grounded in twin physics, not transferred.
- [[2510.11689|Phys2Real]] — Conditions policy on physical params (CoM, friction); 57% vs 23% (weight-top T-block); physics as input, not transferable reward.
- [[2603.04029|Self-Adapting RL]] — [[2301.04104|DreamerV3]] residual OOD detection → online fine-tune; adaptation trigger adjacent to a transferable physics signal.
- [[2601.07823|Video Generation in Robotics Survey]] — Lists "integrating physics priors" as a top direction; survey, no reward-transfer method.

**Benchmarks & metrics.**
- [[2604.23702|QuietWalk]] — GRF R²=0.9887/0.9899, RMSE 14.49/14.00 N, −7.17 dBA; the sensor-free reward-fidelity target.
- [[2510.17950|RoboChallenge]] — Table30 real suite, 30 tasks, contact/soft-body splits (soft-body 8% SR / 27% progress); cross-condition real eval substrate.
- [[2511.15200|VIRAL]] — Real loco-manipulation cycle SR (54/59); the action-transfer baseline to beat on cross-condition generalization.

> [!warning] Risks
> - **PINN rewards exist for few physical quantities** — GRF is clean; arbitrary task rewards are not physical laws. → Bound the claim to contact/force-dominated tasks where a conservation law or inverse-dynamics constraint actually exists; do not over-claim to semantic tasks.
> - **Reward transfer ≠ policy transfer** — a transferable reward still needs an on-hardware optimization loop. → Pair with [[2603.04029|Self-Adapting RL]]'s online fine-tune so the transferable reward drives fast real adaptation rather than from-scratch RL.
> - **PINN degrades off-manifold** — R²>0.98 holds on the training distribution; far OOD it may mislead the reward. → Q3 measures the trust envelope explicitly; gate reward use on residual magnitude.

### A3 — Controller-Gain-Aware Sim-to-Real: Co-Optimizing Dynamics and Control

| | |
|---|---|
| **Cluster** | A — Forward Sim-to-Real |
| **Thesis** | The field tunes controller gains to minimize system-identification error. But the gains that best-fit sim dynamics are *not* the gains that best-transfer — stiff, low-sysID-error gains produce high-frequency oscillation on real hardware and the worst transfer. The bet: co-optimizing gains *jointly with* domain randomization — instead of fixing gains then randomizing around them — beats best-fixed-gain DR on contact-rich tasks, reaching RL's 99%+ regime without per-gain hand-tuning by recovering the SR that stiff gains silently destroy. |
| **Anchor surveys** | [[2605.00080\|WM Robot Learning Survey]], [[2604.04974\|Video-to-Control Survey]], [[2507.10087\|Foundation Robotics Review]] |
| **Key targets** | Recover the SR that stiff gains destroy despite lowest sysID error ([[2604.02523\|Tune to Learn]]); RL 99%+ achievable across gain regimes only with per-gain hyperparameter tuning; beat best-fixed-gain DR on [AutoMate](https://arxiv.org/abs/2407.08028)-class contact tasks |

**Why it matters.** [[2604.02523|Tune to Learn]] is the result almost nobody has internalized: the gains with the *lowest* sysID error — stiff, overdamped — give the *worst* sim-to-real transfer, amplifying high-frequency oscillation on hardware. RL can reach 99%+ across *all* gain regimes, but only with per-gain tuning. The field treats gains as a fixed robot property, or tunes them for low tracking error during sysID — the wrong objective. The gain is really an unrecognized sim-to-real hyperparameter: it sets the dynamics distribution the policy trains against, the action-space smoothness, and the deployment oscillation spectrum all at once. [[2604.04974|Video-to-Control Survey]] names "control-loop closure" and "physical inconsistencies" as gaps without spotting gains as the lever. Co-optimizing gains jointly with the DR distribution treats control and dynamics as one coupled transfer problem.

**First-principles framing.**
- **First principle**: The controller is part of the plant the policy controls — gains set the closed-loop dynamics, action smoothness, and high-frequency response, so they belong in the transfer distribution, not a separate pre-tuning step. Tuning gains for tracking error optimizes the wrong closed-loop.
- **Assumption being challenged**: That gains should minimize sysID error. [[2604.02523|Tune to Learn]] shows the low-sysID-error gains are precisely the worst-transferring — so "tune gains for fidelity, then randomize the rest" optimizes a metric anti-correlated with the goal.
- **The bet**: Co-optimizing gains jointly with the DR distribution beats best-fixed-gain DR on contact-rich tasks — recovering the transfer SR stiff gains destroy, and reaching RL's 99%+ regime without per-gain hand-tuning by making the gain a learned variable of the randomization.

**Evidence.**
- [[2604.02523|Tune to Learn]] — Stiff/overdamped gains: lowest sysID error, worst transfer, high-frequency oscillation; RL hits 99%+ only with per-gain tuning; compliant/overdamped best for BC — the gain-is-a-transfer-hyperparameter result.
- [[2210.13702|DeXtreme]] — Reward adds action-delta + joint-velocity penalties — implicit acknowledgment that action smoothness governs transfer, never made a first-class gain co-optimization.
- [[2602.23253|SPARR]] — Asymmetric real residual corrects base actions; 95–100% [AutoMate](https://arxiv.org/abs/2407.08028); the residual absorbs gain/dynamics mismatch the base policy can't.
- [[2604.04974|Video-to-Control Survey]] — Names control-loop closure + physical inconsistency; doesn't spot gains as the lever — the gap this fills.

**Concrete research questions.**
1. **Q1 — Gains in the randomization distribution.** Sample $K_p, K_d$ from a learned/randomized range during training instead of fixing them; does gain-randomization beat dynamics-only DR on contact-task real SR?
2. **Q2 — Joint gain × dynamics optimization.** Treat $(K_p, K_d, \psi)$ as one co-optimized vector via differentiable sim or bilevel search; isolate the gain×dynamics interaction term that fixed-then-randomize misses.
3. **Q3 — Oscillation-spectrum transfer metric.** Build a deployment-time oscillation-spectrum metric and test whether co-optimized gains suppress the high-frequency oscillation [[2604.02523|Tune to Learn]] flags, where low-sysID-error gains amplify it.

**Related research papers.**
- [[2604.02523|Tune to Learn]] — Systematic $K_p/K_d$ study across BC/RL/sim2real; stiff gains lowest sysID error, worst transfer; the anchor.
- [[2210.13702|DeXtreme]] — VADR + action-smoothness reward; 27.8 vs 14.8 reorientations; smoothness as implicit gain proxy.
- [[2602.23253|SPARR]] — Sim base + real residual; 95–100% [AutoMate](https://arxiv.org/abs/2407.08028), 74.5% [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly); residual absorbs gain mismatch.
- [[2511.15200|VIRAL]] — Delta action space flagged critical in ablation; action structure governs transfer, gains not co-optimized.
- [[2603.15956|ExpertGen]] — DSRL preserves the motion manifold while optimizing reward; manifold-preservation is gain-adjacent.
- [[2510.11689|Phys2Real]] — Conditions on friction/CoM; the dynamics side of the gain×dynamics coupling.
- [[2604.04974|Video-to-Control Survey]] — Control-loop-closure gap; survey, gains unnamed.
- [[2605.00080|WM Robot Learning Survey]] — Open-loop vs closed-loop divergence; the closed-loop is where gains bite; survey.

**Benchmarks & metrics.**
- [AutoMate](https://arxiv.org/abs/2407.08028) (8–10 tasks via [[2602.23253|SPARR]] / [[2603.15956|ExpertGen]]) — Contact-rich insertion/assembly; 90.5–100% SR; where gains most affect transfer.
- [[2604.02523|Tune to Learn]] — Per-gain sysID error vs sim2real SR + oscillation; the metric pairing defining the co-optimization objective.
- [[2510.17950|RoboChallenge]] — Table30 contact/precision splits (precise 3D localization 18% SR); real-robot stress test for oscillation-prone gains.

> [!warning] Risks
> - **Gain co-optimization explodes the search space** — adding $(K_p, K_d)$ to DR multiplies training cost. → Use [[2604.02523|Tune to Learn]]'s finding to seed a narrow compliant/overdamped prior rather than searching the full grid.
> - **Hardware gain limits** — real controllers cap achievable gains; co-optimized values may be infeasible. → Constrain the co-optimization to the hardware's admissible gain box and validate on the real controller.
> - **Effect may be task-specific** — gains matter most for contact; free-space tasks may show little gain. → Scope the claim to contact-rich tasks ([AutoMate](https://arxiv.org/abs/2407.08028)/[NIST](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly)) and report the free-space null result honestly.

---

## Cluster B — Real-to-Sim-to-Real: Grounding the Simulator in Deployment

*Invert reality into the simulator first — recover appearance and dynamics from real data — then the forward transfer comes nearly for free.*

### B1 — Closing the Real-to-Sim Gap: Reconstruction Fidelity as the New Bottleneck

| | |
|---|---|
| **Cluster** | B — Real-to-Sim-to-Real |
| **Thesis** | [[2512.19562\|REALM]] is the first to name the *real-to-sim* gap as a distinct object. Once named, the arrow flips: forward sim-real correlation is capped by how faithfully reality was inverted into the simulator — yet the field still treats forward fidelity (better engines, more DR) as the bottleneck. The bet: jointly optimizing photoreal 3DGS appearance *and* physical parameters raises push-T sim-real correlation from [[2511.04831\|Isaac Lab]]'s r=0.649 to r>0.9 ([[2511.04665\|Real-to-Sim GS]] hits r=0.915 on push-T, 0.901 on soft-body rope vs [[2511.04831\|Isaac Lab]] 0.237), where appearance-only or physics-only reconstruction cannot. |
| **Anchor surveys** | [[2604.26509\|3D Generation for Embodied AI Survey]], [[2604.04974\|Video-to-Control Survey]], [[2605.00080\|WM Robot Learning Survey]] |
| **Key targets** | Sim-real correlation r=0.649 ([[2511.04831\|Isaac Lab]], push-T) → r>0.9 ([[2511.04665\|Real-to-Sim GS]] 0.915 push-T, 0.901 soft-body rope vs [[2511.04831\|Isaac Lab]] 0.237); [[2512.19562\|REALM]] r=0.92 overall (5 perturbations) / r=0.88 no-perturbation default; [[2605.26638\|HyperSim]] 75%→95% from reconstruction fidelity |

**Why it matters.** [[2512.19562|REALM]] is the first benchmark to name a real-to-sim gap distinct from the forward gap — "low visual fidelity and misaligned control dynamics." Once you name it, the causal arrow flips: forward correlation is upper-bounded by inversion fidelity. [[2511.04665|Real-to-Sim GS]] proves it — joint 3DGS-appearance + physics optimization hits r=0.915 on push-T (and 0.901 on soft-body rope) where [[2511.04831|Isaac Lab]] manages r=0.649 (and 0.237 on rope), and the ablation shows removing *either* color alignment *or* physics optimization collapses the correlation. Appearance alone or physics alone is not enough; the gap closes only when both are inverted together. [[2605.26638|HyperSim]] confirms the leverage — better reconstruction moves zero-shot SR from 75% to 95% with 35 demos. The bottleneck has moved: not "make the sim transfer forward," but "reconstruct reality faithfully enough that forward transfer is automatic."

**First-principles framing.**
- **First principle**: A simulator predicts reality forward no better than it captured reality backward — $\text{Gap}_{\text{S2R}}$ is lower-bounded by $\text{Gap}_{\text{R2S}}$. The forward map is a function of recovered $(\phi^\star, \psi^\star)$; a lossy inversion no forward training can fix.
- **Assumption being challenged**: That forward fidelity is the bottleneck. The simulator-engineering orthodoxy invests in forward realism — but [[2511.04665|Real-to-Sim GS]]'s 0.649→0.915 (push-T) and 0.237→0.901 (rope) jumps come from *inversion*, not a better engine, and the gap to [[2511.04831|Isaac Lab]] is widest on deformables.
- **The bet**: Jointly optimizing 3DGS appearance and physical parameters raises correlation from r=0.649 ([[2511.04831|Isaac Lab]] push-T) to r>0.9 — reproducing [[2511.04665|Real-to-Sim GS]]'s 0.915 push-T / 0.901 rope (vs 0.237) — and the ablation shows appearance-only or physics-only inversion cannot reach it, confirming the gap is *joint*-reconstruction-bound.

**Evidence.**
- [[2511.04665|Real-to-Sim GS]] — Joint 3DGS + [[2503.17973|PhysTwin]] soft-body optimization; r=0.915 vs [[2511.04831|Isaac Lab]] 0.649 (T-block); removing color *or* physics alignment collapses correlation — the joint-inversion proof.
- [[2512.19562|REALM]] — Names the real-to-sim gap; [[2403.12945|DROID]]-aligned sysID, 7 skills/10 scenes/3,500+ objects/15 perturbations; r=0.92 overall (5 perturbations), r=0.88 default; unseen objects drop most.
- [[2605.26638|HyperSim]] — Reconstruction fidelity drives 75% zero-shot → 95% with 35 demos — fidelity-to-SR leverage.
- [[2503.17973|PhysTwin]] — Joint geometry + physical-parameter + appearance optimization from video; the engine [[2511.04665|Real-to-Sim GS]] builds on.

**Concrete research questions.**
1. **Q1 — Joint vs disjoint inversion ablation.** On a deformable benchmark, compare appearance-only, physics-only, and joint [[2511.04665|Real-to-Sim GS]]-style optimization; how much of the 0.649→0.915 gain is the *joint* term vs either marginal?
2. **Q2 — Reconstruction-fidelity → correlation law.** Across rigid/articulated/deformable, is there a monotone law from reconstruction error to forward r? If so, $\text{Gap}_{\text{R2S}}$ *predicts* forward transferability.
3. **Q3 — Unseen-object inversion.** [[2512.19562|REALM]] shows unseen objects drop most; does improving inversion for novel objects (generative-prior reconstruction) close that drop more than forward DR does?

**Related research papers.**
- [[2511.04665|Real-to-Sim GS]] — Joint 3DGS + soft-body sysID; r=0.915 vs 0.649; the reconstruction-fidelity anchor.
- [[2512.19562|REALM]] — Names the real-to-sim gap; r=0.92 overall / r=0.88 default; [[2410.24164|π0]]/[π0-FAST](https://arxiv.org/abs/2501.09747)/[GR00T-N1.5](https://huggingface.co/nvidia/GR00T-N1.5-3B) degrade most on unseen objects.
- [[2605.26638|HyperSim]] — Reconstruction + co-training; 75%→95%; fidelity-driven SR.
- [[2503.17973|PhysTwin]] — Physics-informed deformable reconstruction from video; the inversion engine.
- [[2504.03597|Real-is-Sim]] — Dynamic twin ([Embodied Gaussians](https://arxiv.org/abs/2406.10788)) corrected at 60 Hz by real RGB; 57%→80%, 82% best PushT; continuous real→sim correction.
- [[2603.13825|Explicit-WM Manipulation]] — Twin via [Hunyuan3D](https://arxiv.org/abs/2501.12202) + [[2304.07193|DINOv2]]/ICP alignment; 90.91% mug-free vs 27.27% direct — alignment fidelity gates SR.
- [[2404.09833|Video2Game]] — Single-video → interactive NeRF+mesh+physics twin; 100+ FPS browser; appearance-heavy, lighter physics.
- [[2604.26509|3D Generation for Embodied AI Survey]] — Generative digital twins as the real2sim bridge; survey, names the bottleneck.

**Benchmarks & metrics.**
- [[2511.04665|Real-to-Sim GS]] — r=0.915 (push-T) / 0.901 (rope) vs [[2511.04831|Isaac Lab]] 0.649 / 0.237; the headline gap.
- [[2512.19562|REALM]] — r=0.88 across 7 tasks/5 perturbation types; largest drops on unseen objects.
- [[2511.04831|Isaac Lab]] — r=0.649 deformable baseline (per [[2511.04665|Real-to-Sim GS]]); the forward-engine reference to beat by inversion.

> [!warning] Risks
> - **Reconstruction is per-scene expensive** — joint 3DGS + physics fitting per object/scene may not scale to open worlds. → Amortize with generative reconstruction priors ([[2604.26509|3D Generation for Embodied AI Survey]]) and reuse twins across tasks.
> - **The gap to [[2511.04831|Isaac Lab]] is widest on deformables** — the r=0.915 headline is on rigid push-T, but the largest inversion advantage is on soft-body rope (0.901 vs [[2511.04831|Isaac Lab]] 0.237). → Scope the >0.9 bet across rigid and deformable, reporting the per-object-class delta separately rather than assuming one number generalizes.
> - **Inversion fidelity may not be the *only* bound** — control-dynamics misalignment ([[2512.19562|REALM]]) is a separate term. → Co-optimize control alignment (links to A3) alongside appearance+physics rather than assuming reconstruction alone closes the gap.

### B2 — Differentiable Real-to-Sim Calibration: System-ID as Gradient Descent

| | |
|---|---|
| **Cluster** | B — Real-to-Sim-to-Real |
| **Thesis** | The field does system identification by hand-tuning, or skips it and lets domain randomization average over the unknown physics. But a differentiable simulator turns constitutive-parameter recovery into plain gradient descent — neither hand-tuning nor DR is necessary. The bet: differentiable / VLM-inferred recovery matches hand-tuned sysID with ≤5 real demos *and* beats DR on OOD physical properties, where DR's averaged behavior breaks down ([[2510.11689\|Phys2Real]] 57% vs DR's 24% on the weight-top T-block). |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2605.00080\|WM Robot Learning Survey]], [[2604.26509\|3D Generation for Embodied AI Survey]] |
| **Key targets** | Match hand-tuned sysID with ≤5 real demos ([[2604.27367\|DOT-Sim]] few-demo calibration); beat DR on OOD physical params ([[2510.11689\|Phys2Real]] 57% vs 23% weight-top, 100% vs 79% weight-bottom); [[2604.27367\|DOT-Sim]] 96.55% zero-shot tumor detection |

**Why it matters.** System identification gates the whole real2sim2real loop, and the field still does it badly — manual tuning or, worse, DR as a substitute. DR's failure mode is precise: on a T-block with weight at the top (OOD mass), DR reaches 23.81% while parameter-conditioned [[2510.11689|Phys2Real]] hits 57.14% — averaged behavior fails exactly where the physical parameter is far from the training mean. The alternative is shown: [[2604.27367|DOT-Sim]] makes the optical-tactile simulator *differentiable* and recovers Young's modulus and Poisson's ratio from a few demos by gradient descent on FEA pseudo-ground-truth, then zero-shot transfers at 96.55% tumor detection. [[2503.17973|PhysTwin]] and [[2511.04665|Real-to-Sim GS]] recover physical parameters by gradient optimization from video; [[2510.11689|Phys2Real]] even seeds priors from a VLM and fuses them by inverse-variance weighting. The common move: stop tuning, start differentiating — sysID becomes gradient recovery, both cheaper (few demos) and more accurate (per-object, not averaged).

**First-principles framing.**
- **First principle**: Constitutive parameters (stiffness, friction, mass, Young's modulus) are point estimates the real data identifies — with a differentiable simulator, recovering them is gradient descent on a reconstruction loss, not a search. The parameter has a true value; DR replaces estimation with marginalization and loses it.
- **Assumption being challenged**: That sysID needs hand-tuning, or that DR can substitute. The DR orthodoxy randomizes over unknown physics as nuisance — but [[2510.11689|Phys2Real]]'s 57% vs 23% on OOD mass shows marginalizing is strictly worse than estimating when the test value is far from the prior mean.
- **The bet**: Differentiable / VLM-inferred recovery matches hand-tuned sysID with ≤5 real demos *and* beats DR on OOD physical properties — reproducing [[2510.11689|Phys2Real]]'s 57% vs 23% (weight-top) and 100% vs 79% (weight-bottom) advantage, at [[2604.27367|DOT-Sim]]'s few-demo cost.

**Evidence.**
- [[2604.27367|DOT-Sim]] — Differentiable MPM recovers Young's modulus + Poisson's ratio from few demos via FEA pseudo-GT; 1.71 mm Chamfer, PSNR 30.48, 96.55% zero-shot tumor detection — the sysID-as-gradient-descent proof.
- [[2510.11689|Phys2Real]] — VLM priors + online inverse-variance-weighted adaptation; 57% vs 23% (DR) on OOD weight-top T-block — estimation beats marginalization.
- [[2503.17973|PhysTwin]] — Joint geometry + physical-parameter recovery from video; generalizes to unseen interactions — gradient sysID for deformables.
- [[2511.04665|Real-to-Sim GS]] — Physical parameters optimized from interaction video jointly with appearance; physics-optimization is load-bearing for correlation.

**Concrete research questions.**
1. **Q1 — Differentiable sysID vs DR on OOD physics.** Sweep a parameter (mass, friction, stiffness) across an OOD range; compare gradient-recovered per-object sysID ([[2604.27367|DOT-Sim]]/[[2503.17973|PhysTwin]]-style) against DR marginalization on real SR — generalize the [[2510.11689|Phys2Real]] gap.
2. **Q2 — Demo-efficiency frontier.** How few real demos let differentiable recovery match hand-tuned sysID? Map the SR-vs-#demos curve and find the ≤5-demo regime.
3. **Q3 — VLM prior + gradient refinement.** Seed parameters from a [[2510.11689|Phys2Real]]-style VLM guess, then refine by differentiable-sim gradient; does the prior cut the demo count or stabilize convergence vs random init?

**Related research papers.**
- [[2604.27367|DOT-Sim]] — Differentiable optical-tactile MPM; few-demo constitutive calibration; 96.55% zero-shot; the differentiable-sysID anchor.
- [[2510.11689|Phys2Real]] — VLM priors + IVW online adaptation; 57% vs 23% OOD; estimation over marginalization.
- [[2503.17973|PhysTwin]] — Gradient sysID for deformables from video; generalizes to unseen interactions.
- [[2511.04665|Real-to-Sim GS]] — Physical-param optimization from interaction video; physics-ablation load-bearing.
- [[2604.10856|BridgeSim]] — Flow-matching observational calibrator + truncated Q-estimator for OL→CL; +19.1 DS; test-time calibration adjacent to differentiable sysID.
- [[2603.04029|Self-Adapting RL]] — Prediction-residual OOD detection → online fine-tune; residual-driven recalibration.
- [[2604.04974|Video-to-Control Survey]] — Latent-action identifiability gap; survey, names the recovery problem.
- [[2605.00080|WM Robot Learning Survey]] — World models as learned simulators whose parameters must be identified; survey.

**Benchmarks & metrics.**
- [[2510.11689|Phys2Real]] — OOD T-block SR: 57% vs 23% (weight-top), 100% vs 79% (weight-bottom); the estimation-vs-DR headline.
- [[2604.27367|DOT-Sim]] — 1.71 mm Chamfer (vs 1.74 [Taxim](https://arxiv.org/abs/2109.04027)), PSNR 30.48, 96.55% tumor zero-shot, 0.896 mm trajectory error; differentiable-calibration fidelity.
- [[2511.04665|Real-to-Sim GS]] — Physics-ablation correlation collapse; the value of identified (vs randomized) parameters.

> [!warning] Risks
> - **Differentiable sims exist for few physics regimes** — MPM/soft-body yes, rich contact + friction transients less so. → Start in [[2604.27367|DOT-Sim]]/[[2503.17973|PhysTwin]]'s deformable/soft-contact regime where differentiability is mature; expand to rigid contact cautiously.
> - **Few-demo recovery can overfit** — ≤5 demos may identify the wrong local optimum. → Use the [[2510.11689|Phys2Real]] VLM prior as a regularizer (Q3) and report identification variance, not just point estimates.
> - **Per-object sysID doesn't scale to clutter** — recovering parameters for every object is expensive in open scenes. → Amortize with a learned amortized-inference network mapping observations → parameters, trained on differentiable-sim rollouts.

### B3 — Bidirectional Sim↔Real Co-Training: The Twin as a Data Engine, Not a Sandbox

| | |
|---|---|
| **Cluster** | B — Real-to-Sim-to-Real |
| **Thesis** | The field uses digital twins as evaluation sandboxes. But a grounded twin's highest-value output is *training data*, not a test environment — so most twins are under-used. The bet: a closed real→sim→real co-training loop (abundant twin data + few real demos, with deployment data folded back) beats both pure-forward-sim and pure-twin training on unseen-object generalization, matching [[2605.26638\|HyperSim]]'s 75%→95% and [[2403.03949\|RialTo]]'s 90%-vs-10% target-twin advantage. |
| **Anchor surveys** | [[2605.00080\|WM Robot Learning Survey]], [[2604.26509\|3D Generation for Embodied AI Survey]], [[2604.04974\|Video-to-Control Survey]] |
| **Key targets** | [[2605.26638\|HyperSim]] 75% zero-shot → 95% with 35 real demos via co-training; [[2403.03949\|RialTo]] 90% (twin) vs 10% (generic) on target real task; [[2506.18088\|RoboTwin 2.0]] +24.4% real few-shot from twin data |

**Why it matters.** Most of the corpus uses twins as sandboxes — places to evaluate policies cheaply ([[2504.03597|Real-is-Sim]], [[2511.04665|Real-to-Sim GS]] are evaluation frameworks). The highest-leverage results come from twins used as *data engines*. [[2403.03949|RialTo]] reconstructs a twin from real data, runs RL inside it, and distills back — 91% real SR on pose randomization, and the decisive ablation: a policy trained on the *target-specific* twin hits 90% on the real drawer while one trained on generic assets manages 10%. [[2605.26638|HyperSim]]'s co-training (abundant synthetic + 35 real demos) lifts 75% to 95%; [[2506.18088|RoboTwin 2.0]] gets +24.4% real few-shot from twin data. The pattern: the twin's value is the data it generates conditioned on real reconstruction, not the evaluation it provides. A closed loop — reconstruct, generate, co-train, deploy, fold deployment data back — treats the twin as a perpetual data engine. [[2605.00080|WM Robot Learning Survey]] frames exactly this: world models as "data amplification" and "learned environments for RL."

**First-principles framing.**
- **First principle**: A twin grounded in real reconstruction generates data from the *correct* distribution $p_{\text{sim}}(\cdot \mid \phi^\star, \psi^\star) \approx p_{\text{real}}$ — so its samples are training-valid, not just test-valid. Evaluation discards the twin's generative capacity; data generation uses it.
- **Assumption being challenged**: That twins are evaluation sandboxes. The eval-framework framing ([[2504.03597|Real-is-Sim]], [[2511.04665|Real-to-Sim GS]] as evaluators) under-uses the twin — [[2403.03949|RialTo]]'s 90%-vs-10% shows the twin's *data* is where the value concentrates, and only a grounded twin produces target-distribution data.
- **The bet**: A closed real→sim→real co-training loop beats *both* pure-forward-sim *and* pure-twin training on unseen-object generalization — reproducing [[2605.26638|HyperSim]]'s 75%→95% and [[2403.03949|RialTo]]'s 90%-vs-10% target-twin advantage, with deployment data folded back to keep the twin current.

**Evidence.**
- [[2403.03949|RialTo]] — Real→sim→real with inverse distillation + RL in twins; 91% pose-rand real SR; 90% (target twin) vs 10% (generic) — the twin-as-data-engine proof.
- [[2605.26638|HyperSim]] — Sim+real co-training; 75% → 95% with 35 demos; adversarial trajectories add +35% first-attempt robustness.
- [[2506.18088|RoboTwin 2.0]] — Twin data generator + 5-axis DR; +24.4% real few-shot, +21% zero-shot, 71.3% auto-codegen SR.
- [[2504.03597|Real-is-Sim]] — Twin co-training: 30 real + 30 sim demos match 60 real (57%→80%) — the data-substitution result.

**Concrete research questions.**
1. **Q1 — Closed-loop vs open-loop co-training.** Does folding deployment data back (re-reconstruct, regenerate, re-co-train) beat a one-shot [[2605.26638|HyperSim]]-style co-train on unseen-object generalization over successive rounds?
2. **Q2 — Twin-data vs real-data exchange rate.** [[2504.03597|Real-is-Sim]] shows 30 sim ≈ 30 real on PushT; how does the exchange rate scale with reconstruction fidelity (link to B1) — does a higher-fidelity twin raise the sim-demo value?
3. **Q3 — Target-specific vs generic twin data.** Replicate [[2403.03949|RialTo]]'s 90%-vs-10% across object classes; how much does *grounding* vs *quantity* of twin data drive the advantage?

**Related research papers.**
- [[2403.03949|RialTo]] — Real→sim→real, RL in twin + co-train; 91% pose-rand, 90% vs 10% target-vs-generic; the data-engine anchor.
- [[2605.26638|HyperSim]] — Sim+real co-training; 75%→95%; adversarial-trajectory robustness.
- [[2506.18088|RoboTwin 2.0]] — Twin data generator; +24.4% real few-shot.
- [[2504.03597|Real-is-Sim]] — Twin co-training; 30 sim ≈ 30 real; exchange-rate evidence.
- [[2511.07416|PhysWorld]] — Generated video → reconstructed twin → residual RL; 82% real; twin built from generated, not real, video.
- [[2603.13825|Explicit-WM Manipulation]] — Per-object twin + sim sampling + VLM checker; 6/9 zero-shot tasks ≥75%; twin as planning sandbox, not data engine.
- [[2511.04665|Real-to-Sim GS]] — Grounded twin used as evaluator; the substrate this repurposes for data.
- [[2605.00080|WM Robot Learning Survey]] — World models as data amplification + learned RL environments; survey rationale.

**Benchmarks & metrics.**
- [[2605.26638|HyperSim]] — 75% → 95% (35 demos), +35% first-attempt from adversarial twin data; the co-training target.
- [[2506.18088|RoboTwin 2.0]] — +24.4% real few-shot, +21% zero-shot from twin data; twin-data-value benchmark.
- [[2510.17950|RoboChallenge]] — Table30 real eval, 30 tasks; the unseen-task real measurement for closed-loop gains.

> [!warning] Risks
> - **Closed-loop can drift** — folding deployment data back may amplify reconstruction errors over rounds. → Gate each fold on a B1 reconstruction-fidelity check; reject folds that lower sim-real r.
> - **Co-training balance is delicate** — too much twin data swamps the few real demos. → Tune the sim:real ratio per [[2504.03597|Real-is-Sim]]'s 1:1 finding and [[2605.26638|HyperSim]]'s 35-demo regime; treat the ratio as a hyperparameter.
> - **Grounding cost per object** — every new object needs reconstruction before it can be a data source. → Amortize via B2's differentiable sysID + generative reconstruction priors; reuse twins across tasks.

### B4 — Generalizable Constitutive-Law Inversion: Learning the Physics, Not Just the Parameters

| | |
|---|---|
| **Cluster** | B — Real-to-Sim-to-Real |
| **Thesis** | B2 recovers the *parameters* of a constitutive law the engineer chose in advance. But a hand-chosen law caps generalization at the expressiveness of its functional form — a wrong law, fit perfectly, still extrapolates wrong. The bet: learning the constitutive *law* end-to-end inside a differentiable simulator generalizes to unseen geometries up to 1M particles where parameter-only sysID fails — matching [[2304.14369\|NCLaw]]'s <1e-3 reconstruction loss from real 2D video, and feeding [[2503.17973\|PhysTwin]]/[[2511.04665\|Real-to-Sim GS]] a *generalizable* dynamics model instead of a per-object fit. |
| **Anchor surveys** | [[2604.26509\|3D Generation for Embodied AI Survey]], [[2604.04974\|Video-to-Control Survey]], [[2605.00080\|WM Robot Learning Survey]] |
| **Key targets** | Match [[2304.14369\|NCLaw]]'s reconstruction loss <1e-3 + generalization to unseen geometries up to 1M particles from real 2D video; beat parameter-only sysID ([[2604.27367\|DOT-Sim]], [[2503.17973\|PhysTwin]]) on held-out material/geometry; supply a generalizable dynamics model to [[2511.04665\|Real-to-Sim GS]]'s r=0.915 joint-inversion loop |

**Why it matters.** B2 recovers the *parameters* of a law the engineer picked — Young's modulus and Poisson's ratio for a neo-Hookean solid ([[2604.27367|DOT-Sim]]), stiffness and friction for a spring-mass deformable ([[2503.17973|PhysTwin]]). That works when the chosen law matches the material, but caps generalization at the functional form: a wrong law fit perfectly still extrapolates wrong. [[2304.14369|NCLaw]] shows the deeper move — embed a *neural* constitutive law inside a differentiable Material Point Method simulator, let the simulator enforce conservation (momentum, mass) structurally, and have the network learn only the material-specific stress-strain map under physics-aware priors (rotation equivariance, undeformed-state equilibrium). The result generalizes by orders of magnitude over data-driven baselines — to unseen boundary conditions, geometries up to 1M particles, longer horizons, and multi-physics — and learns the law from real 2D dough video at reconstruction loss below 1e-3. [[2604.04974|Video-to-Control Survey]] names "physical consistency" and "latent-action identifiability" as integration-layer gaps; a learned-law inversion makes the recovered dynamics itself the transferable object B1's reconstruction and B3's co-training loop consume.

**First-principles framing.**
- **First principle**: The cause of a material's motion is its constitutive law — the stress-strain map — not the scalars of any one parameterization. Conservation laws are universal and belong in the simulator; the constitutive law is material-specific, and it is the only degree of freedom that varies across materials, so it is what must be *learned*.
- **Assumption being challenged**: That recovering point parameters of a fixed law is enough inversion — B2's own framing. The differentiable-sysID orthodoxy ([[2604.27367|DOT-Sim]], [[2503.17973|PhysTwin]], [[2511.04665|Real-to-Sim GS]]) fits parameters of a chosen law; [[2304.14369|NCLaw]]'s orders-of-magnitude generalization shows the law's *functional form*, not its parameters, is the binding constraint on extrapolation to unseen geometry.
- **The bet**: Learning the constitutive law end-to-end inside a differentiable MPM simulator generalizes to unseen geometries up to 1M particles where parameter-only sysID fails — matching [[2304.14369|NCLaw]]'s <1e-3 reconstruction loss from real 2D video, and feeding [[2503.17973|PhysTwin]]/[[2511.04665|Real-to-Sim GS]] a model that transfers across geometry, not a per-object fit.

**Evidence.**
- [[2304.14369|NCLaw]] — Neural constitutive law inside differentiable MPM; conservation enforced structurally, stress-strain learned with rotation-equivariance + undeformed-equilibrium priors; <1e-3 loss, generalizes to 1M particles / unseen geometry / multi-physics, learns from real 2D dough video — the learn-the-law proof.
- [[2503.17973|PhysTwin]] — Joint geometry + physical-parameter + appearance recovery from video; recovers *parameters* of a chosen model — the parameter-only baseline B4 generalizes past.
- [[2604.27367|DOT-Sim]] — Differentiable MPM recovering Young's modulus + Poisson's ratio from few demos; fixed form, point-parameter recovery — the per-object fit B4 replaces.
- [[2511.04665|Real-to-Sim GS]] — Joint 3DGS + soft-body parameter optimization; r=0.915; the joint-inversion loop a learned law would slot into.

**Concrete research questions.**
1. **Q1 — Learned-law vs parameter-fit on held-out geometry.** Fit a [[2503.17973|PhysTwin]]-style chosen-law recovery and an [[2304.14369|NCLaw]]-style neural law to the same real video; test both on *unseen* geometries — does the learned law's extrapolation advantage replicate the orders-of-magnitude gap?
2. **Q2 — Learned law into the real2sim2real loop.** Drop an [[2304.14369|NCLaw]]-recovered law into [[2511.04665|Real-to-Sim GS]]'s pipeline in place of the fixed soft-body model; does forward correlation hold across material variation a single parameter fit can't cover?
3. **Q3 — Real-video-only law recovery for manipulation deformables.** Can [[2304.14369|NCLaw]]'s recovery run on cloth, cable, or food from a single RGB-D interaction, supplying B3's co-training engine a transferable dynamics model per material class?

**Related research papers.**
- [[2304.14369|NCLaw]] — Generalizable neural constitutive law via differentiable MPM; <1e-3 loss, 1M particles, real dough video; the learn-the-law anchor.
- [[2503.17973|PhysTwin]] — Chosen-law parameter recovery from video for deformables; the parameter-only baseline.
- [[2604.27367|DOT-Sim]] — Differentiable optical-tactile MPM; fixed-form constitutive calibration; point-parameter recovery.
- [[2511.04665|Real-to-Sim GS]] — Joint appearance + soft-body parameter inversion; r=0.915; the loop a learned law feeds.
- [[2510.11689|Phys2Real]] — VLM-inferred priors + online estimation; priors over a fixed law, not a learned law.
- [[2404.09833|Video2Game]] — Single-video interactive twin (NeRF + mesh + physics); appearance-heavy, fixed rigid physics — contrast for learned-deformable-law generalization.
- [[2604.04974|Video-to-Control Survey]] — Names physical-consistency + latent-action-identifiability gaps; survey, no learned-law method.
- [[2605.00080|WM Robot Learning Survey]] — World models as learned simulators needing physical consistency; survey rationale for learning the law, not just parameters.

**Benchmarks & metrics.**
- [[2304.14369|NCLaw]] — Reconstruction loss <1e-3; generalization to 1M particles / unseen geometry / multi-physics; real 2D dough-video recovery — the headline B4 targets.
- [[2604.27367|DOT-Sim]] — 1.71 mm Chamfer, PSNR 30.48, 96.55% zero-shot tumor detection; the fixed-form-fit fidelity to beat on held-out geometry.
- [[2511.04665|Real-to-Sim GS]] — r=0.915 (push-T) / 0.901 (soft-body rope) vs [[2511.04831|Isaac Lab]] 0.649 / 0.237; the forward-correlation substrate a generalizable law must preserve across materials.

> [!warning] Risks
> - **Learned laws can violate physics off-distribution** despite priors — a neural stress-strain map may extrapolate non-physically. → Keep [[2304.14369|NCLaw]]'s structural priors (rotation equivariance, undeformed-state equilibrium) as hard constraints and gate on conservation-law residuals, not just reconstruction loss.
> - **Differentiable MPM is mature for soft bodies, not rich contact** — the learn-the-law regime is deformables. → Scope the 1M-particle generalization bet to elastoplastic/fluid materials where MPM differentiability holds; treat rigid-contact laws as a separate, harder problem.
> - **Real-video-only recovery is under-constrained** — a single 2D view may not identify the full law. → Use multi-view or RGB-D interaction (Q3) and report identification variance; fall back to B2's parameter fit when the learned law is unidentifiable.

---

## Cluster C — Reality-Gap Measurement as Statistical Inference

*Stop asking "is the sim accurate?" Ask "what can I provably infer about real performance from imperfect, possibly-adversarial sims?"*

### C1 — Per-Factor Correlation Validity as a Deployment Gate: Stress-Test, Then Route

| | |
|---|---|
| **Cluster** | C — Reality-Gap Measurement as Inference |
| **Thesis** | A high sim-real correlation is a *measurement-validity* claim that holds only on the conditions it was measured on — so [[2405.05941\|SIMPLER]]/[[2605.06311\|VISER]]'s r>0.85–0.92 does not mean the sim predicts real performance under shift, and one global r cannot gate a sim wholesale because reliability is *factor-resolved* (trust dynamics-sim A here, appearance-sim B there). The bet has two halves. First, a perturbation-stress-test diagnoses every current high-r sim as in-distribution-only, dropping its r below a usable r<0.7 under deliberate OOD shift. Second, the resulting per-(sim, factor) trust map, used as a routing gate, beats single-scalar selection — feeding [[2604.24018\|Sim2Real Betting]]'s portfolio per-factor weights that lift its 70–100% win rate over the global-edge baseline on shift-mixed deployment. |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2605.00080\|WM Robot Learning Survey]], [[2502.10694\|UDA Simulation Study]] |
| **Key targets** | Diagnose current high-r sims ([[2405.05941\|SIMPLER]] r≥0.85, [[2605.06311\|VISER]] r=0.92, [[2604.21686\|WorldMark]] ρ>0.9) as falling below r<0.7 under deliberate OOD shift over [[2402.08191\|THE COLOSSEUM]]'s 14 factors (30–50% single-perturbation SR drop, R²=0.614 sim↔real); route [[2604.24018\|Sim2Real Betting]]'s biased-bank weights per factor to beat its 70–100% single-global-edge win rate; halve the real-trial spend [[2510.04354\|SureSim]] needs (20–25%) by trusting only validated-per-factor sims |

**Why it matters.** Two questions, one mechanism. *First*, when a benchmark reports a high sim-real correlation, is that number a real property of the sim or an artifact of the nominal conditions it was measured on? [[2405.05941|SIMPLER]] reports r≥0.85 / 0.890, [[2605.06311|VISER]] r=0.92, [[2604.21686|WorldMark]] ρ>0.9 — every one is an *in-distribution* correlation, measured on the conditions the sim was tuned for. [[2502.10694|UDA Simulation Study]] warns that method effectiveness is "highly context-dependent" and some methods show "negative adaptation" — doing *worse* than nothing under shift. [[2402.08191|THE COLOSSEUM]] already shows single perturbations cause 30–50% SR drops with only R²=0.614 sim↔real degradation. So re-measure: shift each factor (lighting, dynamics, object, viewpoint) on both sim and real, re-measure r, report which high-r sims fall below a usable threshold. *Second*, once you have that per-factor table, you can *act* on it. The field picks which sim to deploy with one global scalar — as if the deploy-or-not call were wholesale. It is not: [[2402.08191|THE COLOSSEUM]]'s 14 factors each drop SR 30–50% *differently*, so a sim worth trusting under appearance shift may be the wrong sim under dynamics shift. The deliverable is a routing gate — a per-(sim, factor) trust map (rows from the stress-test, plus [[2512.19562|REALM]]'s per-perturbation validation) wired into [[2604.24018|Sim2Real Betting]]'s portfolio so the estimator gets per-factor weights instead of one aggregate edge. Stress-test produces the diagnosis; the gate routes on it.

**First-principles framing.**
- **First principle**: A correlation coefficient certifies the evaluator only for the conditions it was computed on — OOD validity is a *separate* quantity that must be measured, never inherited. And because a sim's reliability is a *function over perturbation factors* (different physics approximations break under different shifts), the optimal sim-to-trust changes with the factor; a per-factor gate exploits structure a single scalar throws away.
- **Assumption being challenged**: That one in-distribution r ([[2405.05941|SIMPLER]], [[2605.06311|VISER]], [[2604.21686|WorldMark]]) certifies a usable evaluator *and* can gate a sim wholesale. The benchmark community reads r>0.85 as "this sim predicts real performance," and the portfolio literature ([[2604.24018|Sim2Real Betting]]) weights sims by aggregate edge — but no one has shown r survives intentional shift, and [[2402.08191|THE COLOSSEUM]]'s factor-wise 30–50% spread (R²=0.614) shows a global score averages over exactly the per-factor structure that should *decide* which sim to deploy when.
- **The bet**: (i) A perturbation-stress-test diagnoses every current high-r sim as in-distribution-only — dropping measured r below a usable r<0.7 under deliberate OOD shift, proving the published r>0.85–0.92 are validity artifacts. (ii) The resulting per-factor trust map, used as a routing gate, lifts [[2604.24018|Sim2Real Betting]]'s 70–100% win rate over the single-global-edge baseline on shift-mixed deployment, with the gain largest on the factors where (i) found the sharpest r-collapse. (Whether dynamics or appearance factors dominate the routing gain is an empirical output of the gate, not assumed.)

**Evidence.**
- [[2405.05941|SIMPLER]] — r=0.855 / 0.890 + low MMRV, but an in-distribution correlation tuned via sysID + visual matching — the high-r number whose validity is stress-tested.
- [[2605.06311|VISER]] — r=0.92 in-distribution, yet *itself* reports performance "suboptimal on most OOD tasks" and "drops drastically" under distractors — the in/OOD validity split visible inside the benchmark.
- [[2402.08191|THE COLOSSEUM]] — 14 perturbation factors; 30–50% single-perturbation SR drop, R²=0.614 sim↔real (distractor/color/lighting worst) — the shift generator and the per-factor SR structure the gate indexes.
- [[2502.10694|UDA Simulation Study]] — Context-dependent effectiveness + "negative adaptation" — shift can *invert*, not just weaken, a relationship, and the deploy decision is per-axis, not wholesale.

**Concrete research questions.**
1. **Q1 — Perturbation-stress-tested r.** Re-measure [[2405.05941|SIMPLER]] / [[2605.06311|VISER]] sim-real r under each [[2402.08191|THE COLOSSEUM]] factor applied to *both* sim and real; for which factors does r fall below 0.7? The per-factor r table is the diagnostic finding.
2. **Q2 — Build the (sim, factor) routing gate.** Populate a per-cell trust map from Q1's diagnoses over each sim and each [[2402.08191|THE COLOSSEUM]] / [[2512.19562|REALM]] factor; flag r<0.7 cells as "do-not-trust"; define the gate routing a deployment query (task, factor) → trusted sim(s).
3. **Q3 — Per-factor vs global routing at deploy-time.** Feed the gate to [[2604.24018|Sim2Real Betting]] as per-factor weights vs a single aggregate edge; does per-factor routing raise the win rate on shift-mixed deployment, and on which factors does the gain concentrate? Following [[2502.10694|UDA Simulation Study]], is there a perturbation under which sim r goes *negative* (ranks policies backward)?

**Related research papers.**
- [[2405.05941|SIMPLER]] — r=0.855/0.890 in-distribution; visual matching + sysID; the headline evaluator under test.
- [[2605.06311|VISER]] — r=0.92; flags own OOD weakness; in/OOD validity split visible; the in-distribution scalar a per-factor gate replaces.
- [[2402.08191|THE COLOSSEUM]] — 14 perturbation factors, R²=0.614; the OOD shift harness and factor decomposition the gate is built on.
- [[2604.24018|Sim2Real Betting]] — Biased-bank betting; 70–100% win with a single aggregate edge; the portfolio router the gate weights per factor.
- [[2502.10694|UDA Simulation Study]] — Context-dependent effectiveness + negative adaptation; the validity-under-shift and per-axis-deploy warning.
- [[2512.19562|REALM]] — 15 perturbation factors with real-to-sim validation; r=0.92 overall vs r=0.88 default — pre-validated rows for the gate's trust map.
- [[2604.21686|WorldMark]] — ρ>0.9 vs human judgment, but control-alignment leaders ≠ visual-quality leaders — proxy disagreement showing the deploy decision is multi-dimensional.
- [[2509.15273|Embodied Arena]] — Unified evolving eval across 22+ benchmarks; the platform the stress-test and gate can be hosted and refreshed on.

**Benchmarks & metrics.**
- [[2402.08191|THE COLOSSEUM]] — 30–50% single-perturbation / ≥75% combined SR drop; R²=0.614 — the validated shift generator and per-factor degradation the gate indexes.
- [[2604.24018|Sim2Real Betting]] — 70–100% win rate over Monte Carlo with a single global edge; the routing baseline the per-factor gate must beat.
- [[2512.19562|REALM]] — r=0.92 overall (5 perturbations) / r=0.88 default, largest drops on unseen objects; real-to-sim-validated per-factor rows the gate ingests.

> [!warning] Risks
> - **Stress-test and gate both need paired sim+real OOD data** — combinatorially expensive per (sim, factor). → Reuse [[2512.19562|REALM]]'s 15-perturbation real-to-sim-validated pairs and [[2510.17950|RoboChallenge]]'s real fleet; populate the gate incrementally on [[2509.15273|Embodied Arena]] rather than collecting fresh.
> - **A null result (r survives shift) is still informative** — but reframes the diagnosis half. → Pre-register the r<0.7 bet; if r holds, "high-r sims are robust to shift X" is itself publishable, and the gate routes on the validated-robust cells.
> - **Routing on a stale gate mis-deploys the portfolio** — sims and factors drift, so a once-trusted cell can go bad. → Tie gate refresh to [[2509.15273|Embodied Arena]]'s evolving-eval cadence; expire trust cells past a staleness window before they route a deployment.

### C2 — Sim-to-Real as Provable Statistical Inference: Banks of Biased Simulators

| | |
|---|---|
| **Cluster** | C — Reality-Gap Measurement as Inference |
| **Thesis** | The field's instinct is to build one expensive, accurate simulator and trust it. But estimating real performance is a *variance-reduction* problem, not a fidelity problem — so a bank of cheap *biased* sims can beat a single accurate one. The bet: a portfolio of biased simulators yields tighter *provable* confidence intervals on real performance than one expensive accurate sim at equal compute, matching [[2604.24018\|Sim2Real Betting]]'s 70–100% win rate and [[2510.04354\|SureSim]]'s 20–25% real-trial reduction. |
| **Anchor surveys** | [[2605.00080\|WM Robot Learning Survey]], [[2502.10694\|UDA Simulation Study]], [[2604.04974\|Video-to-Control Survey]] |
| **Key targets** | [[2604.24018\|Sim2Real Betting]] 70–100% win rate over Monte Carlo from a *bank* of biased sims; [[2510.04354\|SureSim]] 20–25% real-trial reduction + 14.4% CI tightening (700 sims); finite-sample-valid CI coverage at equal compute vs single accurate sim |

**Why it matters.** Build one accurate sim and trust it — that is the instinct, and it optimizes the wrong thing. Real-performance estimation is variance reduction, and a bank of cheap biased sims can beat a single accurate one. [[2604.24018|Sim2Real Betting]] proves it: sequential betting over a *bank of diverse sims* (Cover's universal portfolio, Kelly bets) wins 70–100% over Monte Carlo, *tolerating bias when an informative predictive edge is present*. [[2510.04354|SureSim]] formalizes the same idea as Prediction-Powered Inference — pair a few real outcomes with abundant sim predictions to get finite-sample-valid confidence intervals, cutting real trials 20–25% and tightening CIs 14.4% with 700 extra sims. A single sim's bias is not a bug to eliminate; it is a signal to weight. [[2502.10694|UDA Simulation Study]] adds that no single method is universally best, so a portfolio of biased estimators dominates committing to one. The open work: make "portfolio of biased sims" a first-class estimator with *provable* real-performance bounds, and characterize when it beats the single-accurate-sim baseline at equal compute.

**First-principles framing.**
- **First principle**: Estimating real performance is finite-sample inference — what matters is the estimator's variance and the validity of its confidence interval, not the point-fidelity of any one sim. Bias is admissible if it is informative and corrected for.
- **Assumption being challenged**: That a single high-fidelity sim is the goal. The accuracy-maximizing orthodoxy spends compute making one sim better — but [[2604.24018|Sim2Real Betting]]'s 70–100% win from a biased bank shows portfolio variance reduction beats marginal fidelity, and [[2510.04354|SureSim]]'s PPI gets provable bounds from imperfect sims directly.
- **The bet**: A portfolio of cheap biased sims yields tighter *provable* (finite-sample-valid) CIs on real performance than one expensive accurate sim at equal compute — reproducing [[2604.24018|Sim2Real Betting]]'s 70–100% win and [[2510.04354|SureSim]]'s 20–25% real-trial reduction, and mapping the compute-allocation frontier where the portfolio wins.

**Evidence.**
- [[2604.24018|Sim2Real Betting]] — Sequential betting over a biased-sim bank (Cover's portfolio, Kelly bets); 70–100% win over Monte Carlo; tolerates bias with predictive edge — the portfolio-beats-single proof.
- [[2510.04354|SureSim]] — PPI + Waudby-Smith-Ramdas; finite-sample-valid CIs; 20–25% fewer real trials, 14.4% CI tightening with 700 sims; provable bounds from imperfect sims.
- [[2502.10694|UDA Simulation Study]] — No single adaptation method universally best — the case for portfolios over single estimators.
- [[2509.15273|Embodied Arena]] — Unified evolving eval across 22+ benchmarks + 30+ models — the multi-source substrate a sim portfolio extends.

**Concrete research questions.**
1. **Q1 — Portfolio vs single-accurate-sim at equal compute.** Allocate a fixed budget to one high-fidelity sim or to a bank of cheap biased sims under [[2604.24018|Sim2Real Betting]]'s estimator; compare CI width and coverage on held-out real performance.
2. **Q2 — Bias-diversity as portfolio value.** Does diversifying simulator bias (different physics approximations) tighten the [[2510.04354|SureSim]] PPI bound more than adding copies of the same biased sim? Map the diversity-vs-count trade-off.
3. **Q3 — Adaptive sim selection.** Use [[2604.24018|Sim2Real Betting]]'s Kelly weights to route real trials to policies where the bank is least certain; does adaptive allocation beat uniform real-trial spending (link to C1's per-factor trust map)?

**Related research papers.**
- [[2604.24018|Sim2Real Betting]] — Betting over a biased-sim bank; 70–100% win; the portfolio-estimator anchor.
- [[2510.04354|SureSim]] — PPI + WSR finite-sample-valid CIs; 20–25% real-trial reduction; the provable-bound anchor.
- [[2502.10694|UDA Simulation Study]] — Context-dependent method effectiveness; portfolio rationale.
- [[2509.15273|Embodied Arena]] — Unified evolving multi-benchmark eval; portfolio substrate.
- [[2604.10856|BridgeSim]] — Cross-simulator CL evaluation platform; +19.1 DS via TTA — multi-sim evaluation infrastructure.
- [[2510.17950|RoboChallenge]] — Real fleet (10 robots, Table30) for the scarce real samples PPI/betting pair with.
- [[2605.00080|WM Robot Learning Survey]] — World models as evaluators; argues eval must move beyond visual fidelity — the inference-over-fidelity rationale.
- [[2512.19562|REALM]] — Real-to-sim-validated benchmark; supplies paired real/sim outcomes the estimators consume.

**Benchmarks & metrics.**
- [[2604.24018|Sim2Real Betting]] — 70–100% win rate across synthetic + pick-and-place + locomotion; portfolio-estimator performance.
- [[2510.04354|SureSim]] — 20–25% real-trial reduction, 14.4% CI tightening (700 sims), valid coverage where control variates miscover; provable-CI metrics.
- [[2509.15273|Embodied Arena]] — 22+ benchmarks / 30+ models standardized; the multi-source eval scale a sim portfolio targets.

> [!warning] Risks
> - **PPI/betting need a few paired real outcomes** — provable bounds still require some real data. → Pair with [[2510.17950|RoboChallenge]]'s remote fleet to keep the real-sample cost minimal while preserving validity.
> - **Bias must be informative, not adversarial** — a bank of uniformly-wrong sims gives no edge. → Use C1's per-factor trust map to *select* sims with informative bias and exclude those that fail under the relevant shift.
> - **Portfolio overhead** — managing many sims adds engineering cost. → Quantify the compute-allocation frontier (Q1) so the portfolio is only used where it provably beats the single-sim baseline.

---

## Cluster D — Deployment-Time Adaptation: Closing the Residual Gap Online

*Closing the residual gap at deploy-time — a time-varying disturbance observable only on hardware, that survives train-, reconstruct-, and measure-time fixes.*

### D1 — Latent-Extrinsics Online Adaptation

| | |
|---|---|
| **Cluster** | D — Deployment-Time Adaptation |
| **Thesis** | The field handles the residual dynamics gap with one fixed domain-randomized policy chosen at train-time. But the true environment parameters are only revealed *on the hardware, during deployment* — so a single robustified policy cannot span the whole deployment envelope. The bet: a proprioception-only latent-extrinsics estimator closes the residual online where fixed-DR policies stall, reproducing [[2107.04034\|RMA]]'s zero-real-fine-tune adaptation to sand/mud/12 kg payload and [[2409.16578\|FLaRe]]'s +30.7% real SR jump (50%→80.7% on [Stretch RE-1](https://hello-robot.com/)) that a frozen policy cannot reach. |
| **Anchor surveys** | [[2507.10087\|Foundation Robotics Review]], [[2605.00080\|WM Robot Learning Survey]], [[2604.04974\|Video-to-Control Survey]] |
| **Key targets** | [[2107.04034\|RMA]] zero-real-fine-tune adaptation across sand/mud/rocky/slippery + 12 kg payload (100% of body weight); [[2409.16578\|FLaRe]] real [Stretch RE-1](https://hello-robot.com/) SR 50%→80.7% (+30.7%), +23.6% sim, 72% [LoCoBot](http://www.locobot.org/) embodiment transfer (6 h for new-behavior adaptation); latent-extrinsics inference at deploy-time where fixed-DR plateaus |

**Why it matters.** A fixed domain-randomized policy is one bet placed at train-time: pick a range, hope deployment falls inside it. [[2107.04034|RMA]] showed the alternative — train a base policy on a privileged "extrinsics vector" of the true environment properties, then train an adaptation module to *infer* that vector online from proprioceptive history alone, at 10 Hz, while the base policy runs at 100 Hz. The robot walks on sand, mud, rocky, and slippery terrain with a 12 kg payload — 100% of its body weight — with *no* real-world fine-tuning, because the latent-extrinsics estimate tracks the dynamics the policy was conditioned on. [[2409.16578|FLaRe]] makes the manipulation case: large-scale RL fine-tuning lifts a pre-trained BC policy from 50% real [Stretch RE-1](https://hello-robot.com/) SR to 80.7% (+30.7%), transfers to a new embodiment ([LoCoBot](http://www.locobot.org/), 72% ObjectNav SR) by action-masking, and shapes new behaviors in 6 hours. [[2507.10087|Foundation Robotics Review]] names physical-grounding-data limits and the sim2real gap as the open bottlenecks. The residual that A, B, and C leave behind is exactly what a proprioception-only estimator can close — online, on hardware, with no real reward.

**First-principles framing.**
- **First principle**: The deployment environment's true dynamics are a latent variable revealed only by the robot's own proprioceptive history — no train-time randomization observes them, because they don't exist until deployment. The estimable quantity is the *posterior over extrinsics given on-robot history*, a deploy-time object by construction.
- **Assumption being challenged**: That a fixed robustified policy spans the deployment envelope. The DR orthodoxy picks one policy for all conditions — but [[2107.04034|RMA]]'s zero-fine-tune adaptation across radically different terrains, and [[2409.16578|FLaRe]]'s +30.7% from *adapting* rather than *robustifying*, show infer-then-condition beats marginalize-over-the-unknown.
- **The bet**: A proprioception-only latent-extrinsics estimator closes the residual online where fixed-DR policies stall — reproducing [[2107.04034|RMA]]'s zero-real-fine-tune adaptation (sand/mud/12 kg) and [[2409.16578|FLaRe]]'s 50%→80.7% (+30.7%), with the gain concentrated outside the train-time range.

**Evidence.**
- [[2107.04034|RMA]] — Base policy on privileged extrinsics + proprioception-only adaptation module (10 Hz) inferring extrinsics online; zero real fine-tune across sand/mud/rocky/slippery + 12 kg payload — the latent-extrinsics proof.
- [[2409.16578|FLaRe]] — Large-scale RL fine-tuning of a pre-trained BC policy; 80.7% real [Stretch RE-1](https://hello-robot.com/) (+30.7%), 79.5% sim (+23.6%), 72% [LoCoBot](http://www.locobot.org/) transfer (6 h new-behavior) — deploy-time adaptation beating a frozen policy.
- [[2602.20057|AdaWorldPolicy]] — Online adaptive learning at 4 Hz via world-model prediction error; OOD recovery — adjacent online-adaptation engine.
- [[2603.04029|Self-Adapting RL]] — [[2301.04104|DreamerV3]] residual OOD detection → online fine-tune; the residual-trigger primitive a latent-extrinsics loop can gate on.

**Concrete research questions.**
1. **Q1 — Latent-extrinsics for manipulation, not just locomotion.** Can a proprioception/force-history estimator close the residual on contact-rich manipulation where [[2409.16578|FLaRe]] needs RL fine-tuning, *without* real reward?
2. **Q2 — Adaptation envelope vs randomization range.** How far outside the train-time DR range does the estimate stay accurate, and where does it stop tracking the true dynamics?
3. **Q3 — Estimator-then-condition vs robustify head-to-head.** Train matched policies — one fixed-DR-robust, one [[2107.04034|RMA]]-style infer-then-condition — and measure the real SR gap as deployment moves outside the range.

**Related research papers.**
- [[2107.04034|RMA]] — Proprioception-only latent-extrinsics online adaptation; zero real fine-tune, 12 kg payload; the anchor.
- [[2409.16578|FLaRe]] — RL fine-tuning to masterful policies; +30.7% real, 72% [LoCoBot](http://www.locobot.org/) transfer (6 h); deploy-time adaptation in manipulation.
- [[2602.20057|AdaWorldPolicy]] — World-model-supervised online adaptation at 4 Hz; OOD recovery; LoRA test-time updates.
- [[2603.04029|Self-Adapting RL]] — Prediction-residual OOD detection → online fine-tune; the adaptation trigger.
- [[2511.15200|VIRAL]] — Teacher-student visual sim-to-real; the fixed-policy baseline an online estimator augments.
- [[2510.11689|Phys2Real]] — Online inverse-variance-weighted parameter adaptation; parameter-level cousin of latent-extrinsics inference.
- [[2507.10087|Foundation Robotics Review]] — Names physical-grounding-data limits + sim2real gap; survey, no online-extrinsics method.
- [[2605.00080|WM Robot Learning Survey]] — World models as online adaptable simulators; survey rationale for deploy-time inference.

**Benchmarks & metrics.**
- [[2107.04034|RMA]] — Zero-real-fine-tune SR across sand/mud/rocky/slippery + 12 kg payload; time-to-failure / distance vs fixed-DR — the locomotion target.
- [[2409.16578|FLaRe]] — Real [Stretch RE-1](https://hello-robot.com/) 80.7% (+30.7%), sim 79.5% (+23.6%); the manipulation deploy-time headline.
- [[2510.17950|RoboChallenge]] — Table30 real suite, 30 tasks; cross-condition real eval for adaptation-envelope mapping.

> [!warning] Risks
> - **Proprioception under-determines extrinsics for some tasks** — vision-dominant manipulation may not expose dynamics in proprioceptive history. → Augment the estimator with force/tactile history (links to A2's GRF reward) where proprioception alone is uninformative; report the observability boundary.
> - **Online adaptation can chase noise** — a too-fast estimator may track sensor noise as dynamics change. → Use [[2107.04034|RMA]]'s slow-module (10 Hz) / fast-policy (100 Hz) separation and gate updates on [[2603.04029|Self-Adapting RL]]'s residual magnitude.
> - **Unsafe adaptation during exploration** — online updates can drive unsafe actions before convergence. → Hand off to E1's safety-constrained continual adaptation rather than adapting reward-only.

### D2 — Differentiable-Sim Test-Time Adaptation

| | |
|---|---|
| **Cluster** | D — Deployment-Time Adaptation |
| **Thesis** | The field does test-time adaptation by online RL fine-tuning of a world model — which is sample-hungry and slow. But a differentiable simulator turns adaptation into a first-order gradient step, so online adaptation need not be slow. The bet: differentiable-sim TTA corrects OOD disturbance in ≤3 steps / 4.5 s with 81% hover-error reduction, beating [[2603.04029\|Self-Adapting RL]]'s ~8-min [[2301.04104\|DreamerV3]] online fine-tune at equal risk via BPTT through a hybrid analytical+residual model. |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2605.00080\|WM Robot Learning Survey]], [[2507.10087\|Foundation Robotics Review]] |
| **Key targets** | [[2508.21065\|Learning on the Fly]] 81% hover-error reduction vs L1-MPC (55% vs [DATT](https://arxiv.org/abs/2310.09053)) under large OOD disturbance, adaptation in 3 steps / 4.5 s wall-clock; beat [[2603.04029\|Self-Adapting RL]]'s ~8-min [[2301.04104\|DreamerV3]] fine-tune latency at equal safety risk |

**Why it matters.** When a quadrotor hits unmodeled wind or added mass, the residual must be corrected *now* — seconds, not minutes. The standard recipe is RL fine-tuning of a learned world model: [[2603.04029|Self-Adapting RL]] detects OOD via [[2301.04104|DreamerV3]] prediction residuals and fine-tunes online, but a model-based RL fine-tune is slow. [[2508.21065|Learning on the Fly]] shows the alternative — a *differentiable* hybrid dynamics model (low-fidelity analytical core + learned residual) lets policy gradients flow by Back-Propagation-Through-Time, so adaptation is a first-order step, not an RL loop. The result: 81% hover-error reduction vs L1-MPC, 55% vs [DATT](https://arxiv.org/abs/2310.09053) under large OOD disturbance, with meaningful improvement after only 3 steps — 4.5 s of wall-clock training. The internal model overfits to the current environment fast because the gradient is exact through the analytical dynamics. [[2604.04974|Video-to-Control Survey]] names "control-loop closure" and "pre-execution verification" as the gaps; differentiable TTA closes the loop at the speed the disturbance demands.

**First-principles framing.**
- **First principle**: If the dynamics model is differentiable, adapting the policy to a new disturbance is gradient descent on a known loss — the disturbance enters as a residual the gradient corrects directly, so adaptation cost is *first-order*, not the sample complexity of model-free or model-based RL.
- **Assumption being challenged**: That online test-time adaptation is inherently slow. The online-RL-fine-tune orthodoxy ([[2603.04029|Self-Adapting RL]]'s [[2301.04104|DreamerV3]] loop) treats adaptation as re-learning — but [[2508.21065|Learning on the Fly]]'s 3-step / 4.5-s correction shows BPTT through a hybrid model collapses adaptation into a handful of gradient steps.
- **The bet**: Differentiable-sim TTA corrects OOD disturbance in ≤3 steps / 4.5 s with 81% hover-error reduction (vs L1-MPC) — beating [[2603.04029|Self-Adapting RL]]'s ~minutes-scale [[2301.04104|DreamerV3]] online fine-tune at equal deployment risk, with the speedup from first-order BPTT rather than sampled rollouts.

**Evidence.**
- [[2508.21065|Learning on the Fly]] — Hybrid analytical+residual differentiable dynamics; BPTT policy gradients; 81% vs L1-MPC, 55% vs [DATT](https://arxiv.org/abs/2310.09053), improvement in 3 steps / 4.5 s; real quadrotor mass+wind — the differentiable-TTA proof.
- [[2603.04029|Self-Adapting RL]] — [[2301.04104|DreamerV3]] residual OOD detection → online fine-tune; the model-based-RL baseline to beat on latency.
- [[2602.20057|AdaWorldPolicy]] — World-model prediction-error self-supervision for 4 Hz online LoRA updates; OOD recovery — adjacent fast engine without differentiable dynamics.
- [[2510.11689|Phys2Real]] — Online inverse-variance-weighted parameter adaptation; gradient-adjacent online estimation.

**Concrete research questions.**
1. **Q1 — Differentiable TTA vs model-based-RL fine-tune latency.** Match [[2508.21065|Learning on the Fly]]-style BPTT adaptation against [[2603.04029|Self-Adapting RL]]'s [[2301.04104|DreamerV3]] online fine-tune on the same OOD disturbance; quantify the steps-to-correct and wall-clock gap at equal final error.
2. **Q2 — Residual-network expressiveness vs adaptation speed.** [[2508.21065|Learning on the Fly]] backprops only through the analytical core; how does enlarging the learned residual trade adaptation speed against the range of disturbances it can capture?
3. **Q3 — Differentiable TTA beyond aerial.** Does the 3-step correction hold on contact-rich ground manipulation where the analytical core is less accurate, or does richer contact force more adaptation steps and erode the latency advantage?

**Related research papers.**
- [[2508.21065|Learning on the Fly]] — Differentiable-sim BPTT TTA; 81%/55% hover-error reduction, 3-step / 4.5-s adaptation; the anchor.
- [[2603.04029|Self-Adapting RL]] — [[2301.04104|DreamerV3]] residual OOD detection + online fine-tune; the model-based-RL baseline.
- [[2602.20057|AdaWorldPolicy]] — World-model-supervised 4 Hz online adaptation; OOD recovery without differentiable dynamics.
- [[2510.11689|Phys2Real]] — Online IVW parameter adaptation; gradient-adjacent online estimation.
- [[2604.27367|DOT-Sim]] — Differentiable MPM for parameter recovery; the machinery TTA reuses at deploy-time.
- [[2604.10856|BridgeSim]] — Flow-matching observational calibrator for OL→CL; test-time calibration adjacent to differentiable TTA.
- [[2604.04974|Video-to-Control Survey]] — Names control-loop-closure + pre-execution-verification gaps; survey, no differentiable-TTA method.
- [[2605.00080|WM Robot Learning Survey]] — World models as online-adaptable models; survey rationale for fast deploy-time correction.

**Benchmarks & metrics.**
- [[2508.21065|Learning on the Fly]] — 81% hover-error reduction vs L1-MPC, 55% vs [DATT](https://arxiv.org/abs/2310.09053); 3 steps / 4.5 s — the speed+accuracy target.
- [[2510.17950|RoboChallenge]] — Table30 real suite, 30 tasks; ground-manipulation stress test for Q3.
- [[2602.20057|AdaWorldPolicy]] — 4 Hz real-robot online adaptation, OOD recovery vs offline-only; the online-adaptation rate reference.

> [!warning] Risks
> - **Differentiable dynamics may not exist for the regime** — rich contact / friction transients are hard to differentiate stably. → Start in [[2508.21065|Learning on the Fly]]'s aerial/analytical-core regime where the hybrid model is accurate; expand to contact via B2/B4's differentiable-MPM machinery cautiously.
> - **Fast overfitting to transient noise** — a 3-step adapt can lock onto a momentary disturbance. → Gate adaptation on [[2603.04029|Self-Adapting RL]]'s residual-magnitude trigger and decay the residual when the disturbance clears.
> - **Adaptation during flight is safety-critical** — a bad gradient step destabilizes the platform. → Bound the per-step update and hand execution-safety to E2's reachability shield during the adaptation window.

### D3 — World-Model-Supervised Online Policy Correction

| | |
|---|---|
| **Cluster** | D — Deployment-Time Adaptation |
| **Thesis** | Online policy correction under unseen dynamics stalls because real reward is unavailable at deploy-time. But a world model's *prediction error* is a self-supervised reward surrogate — no environment reward needed — so the field's assumption that online correction requires a reward signal is wrong. The bet: a world-model-supervised loop drives 4 Hz real-robot online adaptation to unseen dynamics with no real reward, holding [[2602.20057\|AdaWorldPolicy]]'s 0.96 [[2306.03310\|LIBERO]]-10 under OOD where a static policy degrades. |
| **Anchor surveys** | [[2605.00080\|WM Robot Learning Survey]], [[2604.04974\|Video-to-Control Survey]], [[2601.07823\|Video Generation in Robotics Survey]] |
| **Key targets** | [[2602.20057\|AdaWorldPolicy]] 0.96 [[2306.03310\|LIBERO]]-10 + 48.0% [[2112.03227\|CALVIN]] 5-task, online adaptation at 4 Hz on real robots via world-model prediction error (LoRA), recovering performance under visual+physical OOD where offline-only policies degrade |

**Why it matters.** The blocker on deploy-time correction: *real reward is not available* — you cannot run RL on hardware against a reward you can't compute. [[2602.20057|AdaWorldPolicy]] resolves it by making the world model an *active supervisor* — it unifies a world model, an action expert, and a force predictor under a flow-matching DiT, and uses the world model's *prediction error* as a self-supervised signal to drive test-time LoRA updates, at 4 Hz on real robots, with no environment reward. The result holds 0.96 on [[2306.03310|LIBERO]]-10 and recovers under visual and physical OOD where an offline-only policy degrades. This is the deploy-time face of B3's twin-as-data-engine and D2's differentiable TTA: instead of a differentiable analytical model (D2) or a privileged-extrinsics estimator (D1), the *learned* world model supplies the gradient, because the mismatch between predicted and observed next-state is itself the correction target. [[2605.00080|WM Robot Learning Survey]] frames it: world models as evaluators whose value is "utility for action and physical consistency." A prediction-error-supervised loop turns physical consistency into a deploy-time reward.

**First-principles framing.**
- **First principle**: Physical-consistency supervision and task-reward supervision are *different objective surfaces*. A world model's prediction error against observed transitions measures the policy's deviation from the dynamics the model encodes — and that surface is observable on hardware exactly where the task-reward surface is not. When the dynamics shift, the deviation is what moves, so descending the consistency surface corrects the right thing without touching reward.
- **Assumption being challenged**: That online policy correction needs a reward signal. The online-RL orthodoxy requires real reward (or a hand-crafted dense proxy) — but [[2602.20057|AdaWorldPolicy]]'s prediction-error self-supervision drives 4 Hz real adaptation with *no* reward, showing the consistency surface substitutes for the unobservable reward surface.
- **The bet**: A world-model-supervised loop drives 4 Hz real-robot online adaptation to unseen dynamics with no real reward — holding [[2602.20057|AdaWorldPolicy]]'s 0.96 [[2306.03310|LIBERO]]-10 under OOD where a static policy degrades, the recovery driven by prediction-error supervision rather than environment reward.

**Evidence.**
- [[2602.20057|AdaWorldPolicy]] — World model + action expert + force predictor (flow-matching DiT); prediction-error self-supervision, 4 Hz real-robot LoRA updates; 0.96 [[2306.03310|LIBERO]]-10, 48.0% [[2112.03227|CALVIN]] 5-task, OOD recovery — the prediction-error-supervised proof.
- [[2603.04029|Self-Adapting RL]] — [[2301.04104|DreamerV3]] prediction-residual OOD detection → online fine-tune; prediction error as the adaptation trigger, the precursor signal.
- [[2508.21065|Learning on the Fly]] — Online residual-dynamics learning; the learned residual is a prediction-error signal driving fast correction — D2's differentiable cousin.
- [[2605.00080|WM Robot Learning Survey]] — World-model value is "utility for action and physical consistency"; the rationale for consistency-as-supervision.

**Concrete research questions.**
1. **Q1 — Prediction-error reward vs real reward.** Does [[2602.20057|AdaWorldPolicy]]'s prediction-error self-supervision match a true real-reward RL loop, or correct a different (consistency, not task) objective? Quantify the gap where both are computable.
2. **Q2 — Which OOD shifts prediction error detects.** Visual vs physical vs dynamics OOD — for which does world-model prediction error give a usable correction gradient, and where is it blind?
3. **Q3 — Force vs visual supervision.** [[2602.20057|AdaWorldPolicy]] unifies world model + force predictor; does adding force-prediction error (links to A2's GRF reward, B2's tactile sysID) sharpen correction on contact-rich OOD over visual prediction alone?

**Related research papers.**
- [[2602.20057|AdaWorldPolicy]] — World-model-supervised online adaptation; 0.96 [[2306.03310|LIBERO]]-10, 4 Hz real; the anchor.
- [[2603.04029|Self-Adapting RL]] — Prediction-residual OOD detection + fine-tune; the trigger precursor.
- [[2508.21065|Learning on the Fly]] — Online residual learning via differentiable sim; learned-residual supervision.
- [[2510.11689|Phys2Real]] — Online parameter estimation; parameter-level online correction.
- [[2604.10856|BridgeSim]] — Truncated Q-estimator + observational calibrator for OL→CL; +19.1 DS; closed-loop correction adjacent.
- [[2511.07416|PhysWorld]] — Residual RL on a reconstructed world model; 82% real; world-model-grounded correction, offline.
- [[2601.07823|Video Generation in Robotics Survey]] — Video world models + physics priors; names hallucination/physics-violation as the supervision risk; survey.
- [[2605.00080|WM Robot Learning Survey]] — World models as active supervisors/evaluators; survey rationale.

**Benchmarks & metrics.**
- [[2602.20057|AdaWorldPolicy]] — 0.96 [[2306.03310|LIBERO]]-10, 48.0% [[2112.03227|CALVIN]] 5-task, 4 Hz real-robot online adaptation, OOD recovery vs offline-only; the prediction-error-supervised headline.
- [[2510.17950|RoboChallenge]] — Table30 real suite, contact-rich/soft-body splits; cross-condition real eval for Q2's OOD-coverage map.
- [[2511.04665|Real-to-Sim GS]] — r=0.915 grounded-twin correlation; the fidelity a world-model supervisor needs for a correct prediction-error gradient.

> [!warning] Risks
> - **World-model hallucination poisons the gradient** — a wrong prediction supervises toward the wrong correction. → Gate updates on prediction-error *calibration* (links to E3's conformal detector) and reject corrections when the world model is itself OOD per [[2601.07823|Video Generation in Robotics Survey]]'s physics-violation flag.
> - **Prediction error ≠ task error** — minimizing consistency may not improve task success. → Q1 measures the consistency-vs-task gap; pair prediction-error supervision with sparse real success checks where available.
> - **Unsafe correction under no-reward adaptation** — without reward, the loop may drift into unsafe regions. → Hand off to E1's safety-cost-constrained continual adaptation so the no-reward update stays inside safe limits.

---

## Cluster E — Risk-Bounded Sim-to-Real Deployment: Safety Under the Irreducible Gap

*Bounding the irreducible residual gap at runtime — an un-handled gap is a safety failure, not just a performance loss, so it must be bounded, not assumed away.*

### E1 — Zero-Violation Continual Adaptation

| | |
|---|---|
| **Cluster** | E — Risk-Bounded Sim-to-Real Deployment |
| **Thesis** | The field does continual real-world adaptation after sim2real with reward-only online RL. But an exploratory update on hardware can be *unsafe* before it is *useful* — so adaptation cannot just optimize reward. The bet: a safety-cost-constrained continual-adaptation scheme raises real grasp SR 20%→60% at *zero* safety violations where reward-only goes unsafe, preventing catastrophic forgetting via [[2503.10949\|SCDA]]'s EWC-regularized PCRPO. |
| **Anchor surveys** | [[2507.10087\|Foundation Robotics Review]], [[2502.10694\|UDA Simulation Study]], [[2605.00080\|WM Robot Learning Survey]] |
| **Key targets** | [[2503.10949\|SCDA]] real grasp SR 20% (zero-shot transfer) → 60% at *zero* safety violations; improvement across the whole target domain without catastrophic forgetting; reward-only adaptation goes unsafe at equal SR |

**Why it matters.** Cluster D's online engines all share a hazard: an exploratory update on real hardware can drive an unsafe action before it converges to a useful one. The field's default — reward-only online RL fine-tuning — has no mechanism to keep exploration safe, and [[2503.10949|SCDA]] documents that reward-only adaptation "led to unsafe behaviors." [[2503.10949|SCDA]]'s fix makes safety a *constraint*, not a hope: it combines Policy-Constrained Reward and Cost Policy Optimization (PCRPO) for safe RL with Elastic Weight Consolidation (EWC) for continual learning, computes a Fisher Information Matrix in randomized-sim pretraining to protect important parameters, then adapts under *stricter* safety limits on hardware. The result is decisive: real grasp SR rises from 20% (zero-shot transfer) to 60% *at zero safety cost*, and [[2503.10949|SCDA]] is the only strategy that improves across an entire domain without catastrophic forgetting. [[2507.10087|Foundation Robotics Review]] names "safety from model hallucinations" as a core open problem. E1 makes the residual that survives A/B/C/D *safe* to adapt against — turning Cluster D's updates from a deployment risk into a bounded one.

**First-principles framing.**
- **First principle**: On hardware, an action's safety cost is a hard constraint with no recovery — an unsafe exploratory update has a consequence the reward cannot undo. Adaptation must optimize reward *subject to* a safety-cost bound; safety is a constraint set, not a reward term.
- **Assumption being challenged**: That continual adaptation can optimize reward alone. The reward-only orthodoxy treats safety as emergent from good reward design — but [[2503.10949|SCDA]]'s direct comparison (reward-only goes unsafe; cost-constrained hits zero violations at the same 60% SR) shows safety must be an explicit constraint, and EWC is needed so adaptation doesn't forget the safe general policy.
- **The bet**: A safety-cost-constrained continual-adaptation scheme raises real grasp SR 20%→60% at *zero* safety violations where reward-only goes unsafe — reproducing [[2503.10949|SCDA]]'s zero-cost result and its no-catastrophic-forgetting improvement across the full target domain.

**Evidence.**
- [[2503.10949|SCDA]] — PCRPO safe-RL + EWC continual learning + Fisher-Information protection; real grasp SR 20%→60% at *zero* safety cost, no forgetting, reward-only goes unsafe — the zero-violation proof.
- [[2602.20057|AdaWorldPolicy]] — 4 Hz online LoRA adaptation under OOD; the unconstrained engine E1 hardens with a safety cost.
- [[2107.04034|RMA]] — Online latent-extrinsics adaptation; fast but unconstrained — the D1 loop that needs a safety bound.
- [[2502.10694|UDA Simulation Study]] — "Negative adaptation" — adaptation can do *worse* than none under shift; the warning that unconstrained adaptation is unsafe.

**Concrete research questions.**
1. **Q1 — Safety-constrained vs reward-only on Cluster-D engines.** Wrap [[2107.04034|RMA]]-style (D1) and [[2602.20057|AdaWorldPolicy]]-style (D3) adaptation in [[2503.10949|SCDA]]'s PCRPO+EWC; does the zero-violation result hold while preserving the gain?
2. **Q2 — Cost-budget vs adaptation-rate frontier.** How tight can the safety-cost limit be set before the 20%→60% gain erodes? Map the safety-budget / adaptation-speed Pareto frontier.
3. **Q3 — Forgetting under repeated domain shift.** Across successive domains, does EWC's Fisher-protected adaptation keep zero violations *and* zero forgetting, or do the two trade off as domains accumulate?

**Related research papers.**
- [[2503.10949|SCDA]] — Safe continual domain adaptation post-sim2real; 20%→60% at zero cost, no forgetting; the anchor.
- [[2602.20057|AdaWorldPolicy]] — Online LoRA adaptation; the engine to constrain.
- [[2107.04034|RMA]] — Online latent-extrinsics adaptation; unconstrained fast adaptation needing a safety bound.
- [[2409.16578|FLaRe]] — RL fine-tuning to masterful policies; the reward-driven adaptation E1 makes safe.
- [[2603.04029|Self-Adapting RL]] — Residual-triggered online fine-tune; the trigger that should fire under a safety constraint.
- [[2409.19190|RAIL]] — Reachability safety filter; execution-time safety (E2) complementing E1's adaptation-time safety.
- [[2502.10694|UDA Simulation Study]] — Negative adaptation; the case for constrained adaptation.
- [[2507.10087|Foundation Robotics Review]] — Names safety-from-hallucination as open; survey rationale.

**Benchmarks & metrics.**
- [[2503.10949|SCDA]] — Real grasp SR 20%→60% at zero safety cost, whole-domain improvement, no catastrophic forgetting; the zero-violation headline.
- [[2510.17950|RoboChallenge]] — Table30 real suite, 30 tasks; cross-condition real adaptation substrate for the safety-budget frontier.
- [[2602.20057|AdaWorldPolicy]] — 4 Hz real online adaptation, OOD recovery; the unconstrained-adaptation baseline to make zero-violation.

> [!warning] Risks
> - **Tight safety cost can stall adaptation** — an over-strict limit may freeze the 20%→60% gain. → Q2 maps the budget/rate frontier; set the limit at the loosest value that still guarantees zero violations.
> - **EWC protection can over-rigidify** — too-strong Fisher penalties block needed adaptation. → Tune the EWC weight per [[2503.10949|SCDA]]'s schedule and monitor the forgetting/adaptation balance across domains (Q3).
> - **Cost model misspecification** — a wrong safety-cost function permits unsafe actions it doesn't penalize. → Pair with E2's reachability shield as a model-free backstop so safety doesn't rest on the learned cost alone.

### E2 — Reachability-Filtered Sim-to-Real Execution

| | |
|---|---|
| **Cluster** | E — Risk-Bounded Sim-to-Real Deployment |
| **Thesis** | The field pursues safe execution of sim-trained policies with soft or probabilistic safety penalties. But the residual sim-to-real gap produces OOD actions a soft constraint cannot hard-bound — learned safety does not suffice. The bet: a reachability shield drives collision rate to *0%* (vs 5–35% unshielded; [[2409.19190\|RAIL]]+DP 0% vs [[2303.04137\|Diffusion Policy]] 27.2% on Pick-Place) at a ~10-pp SR cost (68% vs 78%) — a guarantee no soft penalty provides. |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2507.10087\|Foundation Robotics Review]], [[2605.00080\|WM Robot Learning Survey]] |
| **Key targets** | [[2409.19190\|RAIL]] collision rate 0% (vs 5–35% baseline IL), Pick-Place [[2409.19190\|RAIL]]+DP 68% SR / 0% collisions vs [[2303.04137\|Diffusion Policy]] 78% / 27.2% (~10-pp cost), real-time at 0.42 s/plan on a real [Franka](https://franka.de/); hard reachability guarantee under the residual gap |

**Why it matters.** When a sim-trained imitation-learning policy hits the residual gap, it produces compounding errors and OOD actions — and the field's usual safety is *soft*: penalty terms or probabilistic constraints that bound risk in expectation, not absolutely. [[2409.19190|RAIL]] makes safety a *hard* guarantee: a continuous-time reachability filter checks whether the IL policy's plan is collision-free (computing the robot's forward occupancy), and if not, a model-based backup planner executes a guaranteed-safe alternative. The numbers are unambiguous — 0% collision rate across all tasks vs 5–35% for baseline IL (on Pick-Place, [[2409.19190|RAIL]]+DP 0% vs [[2303.04137|Diffusion Policy]] 27.2%), at a ~10-pp cost (68% vs 78% SR), and on a real [Franka](https://franka.de/) arm it solves the task safely while the vanilla diffusion policy fails the safety spec, at 0.42 s per plan. Counterintuitively, the hard constraint sometimes *raises* SR for weaker policies by steering them off doomed trajectories (up to +16 pp SSucc on low-performing seeds). This is the execution-time face of E1's adaptation-time safety: E1 bounds the *update*, E2 bounds the *action*. [[2604.04974|Video-to-Control Survey]] names "physical feasibility" and "loop closure" as gaps; a reachability shield supplies physical feasibility as a runtime guarantee under exactly the residual the gap leaves open.

**First-principles framing.**
- **First principle**: Collision-freeness is a reachability property of the robot's forward occupancy — verifiable in continuous time independent of the policy, so safety can be a hard runtime filter, not a learned objective. A guarantee that holds requires verification, not a penalty in expectation.
- **Assumption being challenged**: That learned (soft/probabilistic) safety suffices for sim-to-real deployment. The soft-constraint orthodoxy bounds risk in expectation — but [[2409.19190|RAIL]]'s 0%-vs-5–35% result shows only a hard reachability filter eliminates collisions under the OOD actions the residual gap produces.
- **The bet**: A reachability shield drives collision rate to 0% (vs 5–35% unshielded; [[2409.19190|RAIL]]+DP 0% vs [[2303.04137|Diffusion Policy]] 27.2% on Pick-Place) at a ~10-pp SR cost (68% vs 78%) — a hard guarantee no soft penalty matches, and on weaker policies the filter can *raise* SR (up to +16 pp SSucc) by pruning doomed trajectories.

**Evidence.**
- [[2409.19190|RAIL]] — Continuous-time reachability filter + model-based backup planner over an IL policy; 0% collisions (vs 5–35% IL; [[2409.19190|RAIL]]+DP 0% vs [[2303.04137|Diffusion Policy]] 27.2% on Pick-Place at 68% vs 78% SR — Table III, Can Pick-Place), 0.42 s/plan on a real [Franka](https://franka.de/) — the reachability-shield proof.
- [[2503.10949|SCDA]] — Safety-cost-constrained adaptation; the adaptation-time safety E2's execution-time shield complements.
- [[2603.04029|Self-Adapting RL]] — Residual-triggered adaptation; the residual a reachability shield must bound during the adaptation window.
- [[2604.04974|Video-to-Control Survey]] — Names physical-feasibility + loop-closure gaps; the gap E2 fills with a hard guarantee.

**Concrete research questions.**
1. **Q1 — Shield over Cluster-D online adaptation.** Run [[2409.19190|RAIL]]'s filter over a [[2508.21065|Learning on the Fly]] (D2) or [[2602.20057|AdaWorldPolicy]] (D3) online-adapting policy; does the 0%-collision guarantee survive while the policy is *changing*, and what is the SR cost during adaptation?
2. **Q2 — Intervention-rate vs SR-cost frontier.** [[2409.19190|RAIL]] reports a ~10-pp cost (68% vs 78%) and finds intervention falls as the policy improves across epochs; how does tightening the reachability margin trade intervention rate against the SR cost across task families?
3. **Q3 — When the shield raises SR.** [[2409.19190|RAIL]] sometimes *improves* weak-policy SR (up to +16 pp SSucc); characterize which policy/task regimes get a boost from hard safety vs pay the ~10-pp cost.

**Related research papers.**
- [[2409.19190|RAIL]] — Reachability filter + backup planner; 0% collisions, ~10-pp SR cost (68% vs 78%); the anchor.
- [[2503.10949|SCDA]] — Adaptation-time safety constraint; the complement to execution-time shielding.
- [[2506.09937|SAFE]] — Conformal runtime failure detection; the detect-then-shield pairing (E3) to E2's prevent-by-construction.
- [[2508.21065|Learning on the Fly]] — Fast online adaptation; the changing policy E2 must shield mid-adaptation.
- [[2602.20057|AdaWorldPolicy]] — Online-adapting policy; shield target during no-reward updates.
- [[2511.15200|VIRAL]] — Teacher-student sim-to-real; the IL policy class whose OOD actions a shield bounds.
- [[2604.04974|Video-to-Control Survey]] — Physical-feasibility + loop-closure gaps; survey rationale.
- [[2507.10087|Foundation Robotics Review]] — Safety-from-hallucination open problem; survey.

**Benchmarks & metrics.**
- [[2409.19190|RAIL]] — 0% collision rate (vs 5–35% IL; Pick-Place [[2409.19190|RAIL]]+DP 68% SR / 0% collisions vs [[2303.04137|Diffusion Policy]] 78% / 27.2%), 0.42 s/plan on a real [Franka](https://franka.de/) — the hard-guarantee headline.
- [[2510.17950|RoboChallenge]] — Table30 real suite with contact-rich/precision splits; the real-robot stress test for intervention-rate mapping.
- [[2402.08191|THE COLOSSEUM]] — 14 perturbation factors, 30–50% SR drop; the OOD-action generator a shield must keep collision-free.

> [!warning] Risks
> - **Reachability filtering adds latency** — continuous-time occupancy checks may slow the control loop. → [[2409.19190|RAIL]] runs at 0.42 s per plan on a real [Franka](https://franka.de/), so it is tractable; precompute occupancy and bound the per-step check budget.
> - **Conservative shields over-intervene** — too-tight margins freeze the robot. → Q2 maps the intervention/SR-cost frontier; set the margin at the loosest value that preserves 0% collisions.
> - **Shield needs a model of obstacles** — reachability requires environment geometry the residual gap may misestimate. → Ground the occupancy model in B1's reconstruction fidelity and fall back to E3's conformal detector where geometry is uncertain.

### E3 — Conformal Runtime Failure Detection

| | |
|---|---|
| **Cluster** | E — Risk-Bounded Sim-to-Real Deployment |
| **Thesis** | The field builds runtime failure detectors from datasets of labeled failures. But sim2real-induced failures are unanticipated OOD events you cannot enumerate in advance — so detection cannot depend on failure-labeled data. The bet: a conformal runtime detector flags sim2real-induced failures at *<1 ms* overhead with *no* failure-labeled data, recovering [[2503.08558\|FAIL-Detect]]'s 78%/72% sim/real detection from successful rollouts alone via [[2506.09937\|SAFE]]'s conformal threshold on internal features. |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2605.00080\|WM Robot Learning Survey]], [[2502.10694\|UDA Simulation Study]] |
| **Key targets** | [[2506.09937\|SAFE]] failure flagging at <1 ms policy-inference overhead, zero-shot to unseen tasks; [[2503.08558\|FAIL-Detect]] ~78% sim / ~72% real balanced accuracy with *no* failure data (logpZO top in 10/16 sim, 8/12 hardware); conformal threshold with FPR guarantee |

**Why it matters.** The failures the sim-to-real gap produces are, by definition, the ones you didn't anticipate — so a detector trained on labeled failures is trained on the wrong distribution. [[2503.08558|FAIL-Detect]] makes the key move: detect failures *without failure data* by framing detection as OOD against successful rollouts only — its flow-based `logpZO` density score, calibrated by functional Conformal Prediction on successes, hits ~78% balanced accuracy in sim and ~72% on hardware, topping baselines in 10/16 sim and 8/12 hardware scenarios. [[2506.09937|SAFE]] sharpens this for policies: it reads the model's *internal hidden-state features* (which hold a task-generic "failure zone"), maps them to a scalar with a tiny MLP/LSTM, and applies functional Conformal Prediction for a time-varying threshold with a false-positive-rate guarantee — at *under 1 ms* of added inference, generalizing zero-shot to unseen tasks. This is the detect face of Cluster E: E2 *prevents* collisions by construction, E1 *bounds* adaptation, E3 *flags* the residual-induced failures neither can rule out — with a statistical guarantee and no failure labels. [[2502.10694|UDA Simulation Study]]'s negative-adaptation warning is exactly the silent failure E3 surfaces at runtime.

**First-principles framing.**
- **First principle**: A failure is an out-of-distribution event relative to successful execution — so it is detectable from successful rollouts alone, with a conformal threshold supplying a finite-sample false-positive-rate guarantee. Detection needs a model of success and a valid threshold, not failure examples.
- **Assumption being challenged**: That runtime failure detection needs failure-labeled data. The supervised-detection orthodoxy collects failure datasets — but [[2503.08558|FAIL-Detect]]'s ~78%/72% from successes-only and [[2506.09937|SAFE]]'s internal-feature conformal detector show the failures you can label are not the sim2real failures you'll hit, so success-only detection generalizes where labeled detection cannot.
- **The bet**: A conformal runtime detector flags sim2real-induced failures at <1 ms overhead with *no* failure-labeled data — recovering [[2503.08558|FAIL-Detect]]'s ~78% sim / ~72% real detection from successful rollouts via [[2506.09937|SAFE]]'s conformal threshold on internal policy features, the FPR guarantee holding zero-shot on unseen tasks.

**Evidence.**
- [[2506.09937|SAFE]] — Failure detection from policy internal hidden-state features (task-generic failure zone) + functional Conformal Prediction; <1 ms overhead, zero-shot to unseen tasks, top/matched ROC-AUC — the low-overhead conformal anchor.
- [[2503.08558|FAIL-Detect]] — Two-stage failure detection with no failure data; flow-based logpZO density + conformal threshold; ~78% sim / ~72% real, top in 10/16 sim & 8/12 hardware — the no-failure-data proof.
- [[2602.20057|AdaWorldPolicy]] — World-model prediction error as an OOD/failure signal; the detector D3 uses, complementary to internal-feature detection.
- [[2502.10694|UDA Simulation Study]] — Negative adaptation as a silent failure mode; the kind of runtime failure E3 must surface.

**Concrete research questions.**
1. **Q1 — Success-only vs labeled-failure detectors.** Does [[2503.08558|FAIL-Detect]]'s success-only OOD detection actually beat a failure-labeled detector on *held-out sim2real-induced* failures (the ones the labeled set can't contain)? Quantify the generalization gap.
2. **Q2 — Internal-feature vs prediction-error detection.** Compare [[2506.09937|SAFE]]'s internal-feature signal against [[2602.20057|AdaWorldPolicy]]'s world-model prediction error on the same failures; which detects earlier and at lower overhead?
3. **Q3 — Detect-then-act loop.** Wire E3's conformal flag to E2's reachability backup or E1's safe-adaptation trigger; does detection + bounded response keep the FPR guarantee while reducing the failures that reach the user?

**Related research papers.**
- [[2506.09937|SAFE]] — Internal-feature conformal policy failure detection; <1 ms, zero-shot; the anchor.
- [[2503.08558|FAIL-Detect]] — No-failure-data runtime detection; logpZO + conformal; ~78%/72%.
- [[2602.20057|AdaWorldPolicy]] — Prediction-error OOD signal; complementary detector.
- [[2603.04029|Self-Adapting RL]] — Prediction-residual OOD detection; the trigger E3 generalizes with a conformal guarantee.
- [[2409.19190|RAIL]] — Reachability shield; the act half of a detect-then-act loop.
- [[2503.10949|SCDA]] — Safe adaptation; the response E3's flag can trigger.
- [[2604.04974|Video-to-Control Survey]] — Names pre-execution-verification as a gap; survey, no conformal-detection method.
- [[2605.00080|WM Robot Learning Survey]] — World models as evaluators detecting physical inconsistency; survey rationale.

**Benchmarks & metrics.**
- [[2506.09937|SAFE]] — <1 ms added inference, top/matched ROC-AUC across policy models, zero-shot unseen-task detection — the low-overhead conformal headline.
- [[2503.08558|FAIL-Detect]] — ~78% sim / ~72% real balanced accuracy, logpZO top in 10/16 sim & 8/12 hardware, no failure data; the success-only-detection benchmark.
- [[2510.17950|RoboChallenge]] — Table30 real suite, 30 tasks; the real-robot substrate for held-out sim2real-failure detection.

> [!warning] Risks
> - **Conformal validity needs a calibration set of successes** — the FPR guarantee rests on representative success data. → Calibrate per [[2503.08558|FAIL-Detect]]'s success-only protocol on the deployment distribution and re-calibrate on domain shift to keep coverage.
> - **Internal-feature detectors are model-specific** — [[2506.09937|SAFE]]'s features are policy-internal and may not transfer across architectures. → Pair with [[2503.08558|FAIL-Detect]]'s policy-agnostic logpZO density score as a model-independent fallback.
> - **Detection without response is inert** — flagging a failure the system can't avoid adds no safety. → Q3's detect-then-act loop wires the flag to E2's shield or E1's safe adaptation so detection drives a bounded response.

---

## Cross-Cutting Themes

> [!tip] The Reality Gap Is Bidirectional — and Real→Sim Is Now the Binding Constraint
> B1, B2, and B3 all turn on the same inversion: the forward gap A1–A3 attack is lower-bounded by how faithfully reality was run *backward* into the simulator. [[2512.19562|REALM]] names the real-to-sim gap as a distinct object; [[2511.04665|Real-to-Sim GS]] measures it (r=0.915 vs [[2511.04831|Isaac Lab]] 0.649); B2 recovers the dynamics ($\psi^\star$) and B1 the appearance ($\phi^\star$) that B3's co-training loop then consumes. The field spent a decade making sims transfer forward (Cluster A); the leverage has migrated to inversion (Cluster B), and even C1's correlation stress-test and C2's portfolio depend on how well each sim inverts reality.

> [!tip] Sim Fidelity Is Not Transfer Quality — the Proxy You Optimize Is *Anti-Correlated* With the Goal
> This is the sharpest contrarian result in the doc, and three papers converge on it independently: **optimizing fidelity actively destroys transfer.** A3's [[2604.02523|Tune to Learn]] is the cleanest case — the controller gains with the *lowest* system-identification error produce the *worst* sim-to-real transfer; minimizing the standard sysID objective moves you away from the goal, not toward it. B2's [[2510.11689|Phys2Real]] shows the same inversion for randomization — DR's distribution-*marginalizing* fidelity reaches only 23% on OOD mass while *estimating* the single true parameter hits 57%, so averaging over the physics you could have identified is strictly worse. C1's [[2502.10694|UDA Simulation Study]] names the failure outright as "negative adaptation" — under shift, the adaptation that should help can do *worse than no adaptation*, flipping the sign of the relationship. [[2604.21686|WorldMark]] caps the warning: control-alignment leaders are not visual-quality or world-consistency leaders, so no single fidelity proxy even *ranks* policies correctly. The cross-cutting lesson is not the mild "fidelity is a confounded surrogate" — it is the strong claim that **the realism you are optimizing is, on these axes, negatively coupled to the transfer you actually want; measure transfer directly, because the proxy points the wrong way.**

> [!tip] Sim-to-Real Evaluation Is Becoming Statistical Inference, Not Accuracy Engineering
> C1 and C2 form one diagnose-and-route → infer pipeline, and B3 inherits the reframing for data. C1 *diagnoses and routes* — it shows in-distribution r ([[2405.05941|SIMPLER]] 0.855, [[2605.06311|VISER]] 0.92) is a validity artifact that must be re-measured per factor under shift, then turns the per-factor result into a deployment gate that routes which biased sim to trust per perturbation. C2 *infers* — [[2604.24018|Sim2Real Betting]] (70–100% win rate) and [[2510.04354|SureSim]] (provable CIs, 20–25% fewer real trials) extract provable real bounds from *imperfect* sims by treating estimation as variance reduction, consuming C1's per-factor weights. The question shifts from "how accurate is my sim?" to "is this correlation valid and which sim do I deploy per factor (C1), and what can I provably infer from it (C2)?" — and B3's twin becomes a data engine under the same inference logic.

> [!tip] Differentiable Rendering + Physics Collapse System-ID Into Gradient Descent
> A1, B1, B2, and B4 all ride the same capability: appearance and dynamics are now recovered end-to-end by gradient, not hand-tuning. [[2503.17973|PhysTwin]] and [[2511.04665|Real-to-Sim GS]] jointly optimize geometry + physical parameters + appearance from video; [[2604.27367|DOT-Sim]] makes the optical-tactile simulator differentiable and calibrates constitutive parameters from few demos; [[2510.11689|Phys2Real]] fuses VLM priors with online estimation; B4's [[2304.14369|NCLaw]] pushes the same differentiable-MPM machinery one level deeper, learning the constitutive *law* rather than its parameters. A1's neural-rendering-in-the-loop, B1's joint reconstruction, B2's differentiable sysID, and B4's learned-law inversion are four faces of the same collapse — manual sysID is being replaced by differentiable recovery of $\phi$, $\psi$, and now the functional form of the dynamics itself.

> [!tip] The Reality Gap Has a Temporal Axis — Train, Reconstruct, Measure, Deploy, Bound
> The five clusters are not parallel attacks on one gap; they are ordered in *time* by when each acts. A1–A3 act at **train-time** (robustify the policy before deployment); B1–B4 act at **reconstruct-time** (invert reality into the simulator offline); C1–C2 act at **measure-time** (infer what the gap is and where each sim is trustworthy); D1–D3 act at **deploy-time** (close the residual the first three leave behind, online on hardware — [[2107.04034|RMA]] infers extrinsics, [[2508.21065|Learning on the Fly]] adapts by differentiable TTA, [[2602.20057|AdaWorldPolicy]] corrects by world-model supervision); E1–E3 act at **deploy-time under a safety constraint** (bound the residual that adaptation cannot remove). Each cluster's output is the next's input: B's reconstruction feeds C's measurement and D's adaptation; C1's trust map routes the sims D and E rely on; D's online updates are exactly what E1's [[2503.10949|SCDA]] and E2's [[2409.19190|RAIL]] must keep safe. The residual gap is not eliminated — it is moved down the timeline until only a *bounded* remainder reaches the user.

> [!tip] An Un-Handled Residual Gap Is a Safety Failure, Not Just a Performance Loss
> Cluster E reframes what C measures: the residual gap that survives A/B/C/D is not merely lost success — at deploy-time it is a *risk surface*. E1, E2, and E3 are the three ways to bound it. E1's [[2503.10949|SCDA]] constrains the *adaptation* (zero safety violations while D1/D3's online updates run, 20%→60% real grasp SR); E2's [[2409.19190|RAIL]] bounds the *action* (0% collisions vs 5–35% unshielded, ~10-pp SR cost: 68% vs 78%); E3's [[2506.09937|SAFE]] and [[2503.08558|FAIL-Detect]] flag the *failure* the other two can't rule out (<1 ms overhead, ~78%/72% detection, no failure labels). All three convert C1's per-factor untrustworthiness into a runtime guarantee — and crucially, each provides safety *without* failure-labeled data or a hand-crafted dense reward, because the sim2real failures you can label are not the ones the residual gap produces.

> [!tip] Online Adaptation Beats Robustification When Deployment Leaves the Randomization Range
> D1, D2, and D3 share one bet against Cluster A's train-time orthodoxy: a policy that *infers-then-conditions* on the true deployment dynamics beats one that *marginalizes* over them by domain randomization, precisely when deployment falls outside the train-time range. [[2107.04034|RMA]] proves it in locomotion (zero-real-fine-tune across sand/mud/12 kg payload); [[2409.16578|FLaRe]] in manipulation (+30.7% real SR from adapting, not robustifying); [[2508.21065|Learning on the Fly]] in aerial control (81% hover-error reduction in 3 gradient steps); [[2602.20057|AdaWorldPolicy]] with no real reward at all (0.96 [[2306.03310|LIBERO]]-10 under OOD via prediction-error supervision). The common engine is a deploy-time signal — proprioceptive history (D1), differentiable-sim residual (D2), or world-model prediction error (D3) — that observes the latent the train-time policy could only guess at. This is the same estimation-over-marginalization principle B2/C2 apply offline, now running online on hardware.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Semantic (affordance/material) randomization in a neural-rendering-in-the-loop sim, vs appearance-only DR | A1 | [[2604.11674\|AffordSim]] (affordance generated, ~24%-avg zero-shot real ceiling) + [[2604.25459\|GS-Playground]] (in-the-loop 3DGS, semantics-agnostic) |
| Physics-grounded *reward* transfer across embodiments/conditions, vs action/policy transfer | A2 | [[2604.23702\|QuietWalk]] (PINN-force reward, R²>0.98, single robot) + [[2511.15200\|VIRAL]] (action transfer baseline) |
| Controller gains co-optimized *with* DR distribution, vs gains tuned for sysID error | A3 | [[2604.02523\|Tune to Learn]] (gains-vs-sysID finding, no co-optimization) + [[2602.23253\|SPARR]] (residual absorbs gain mismatch) |
| Reconstruction-fidelity → forward-correlation law across rigid/articulated/deformable | B1 | [[2511.04665\|Real-to-Sim GS]] (joint inversion, push-T r=0.915 / soft-body rope 0.901 vs [[2511.04831\|Isaac Lab]] 0.649 / 0.237) + [[2512.19562\|REALM]] (names real-to-sim gap) |
| Differentiable per-object sysID vs DR marginalization on OOD physical params, demo-efficiency frontier | B2 | [[2604.27367\|DOT-Sim]] (differentiable, few-demo) + [[2510.11689\|Phys2Real]] (estimation 57% vs DR 24% OOD) |
| Closed real→sim→real co-training loop (deployment data folded back) vs one-shot co-train or pure sandbox | B3 | [[2403.03949\|RialTo]] (90% vs 10% target-twin, open-loop) + [[2605.26638\|HyperSim]] (75%→95% one-shot co-train) |
| Learned constitutive *law* (not parameters) generalizing to unseen geometry up to 1M particles vs parameter-only sysID | B4 | [[2304.14369\|NCLaw]] (learned law, <1e-3 loss, real dough video) + [[2503.17973\|PhysTwin]] (parameter-only fit) |
| Sim-real correlation re-measured per-factor under OOD perturbation (does r survive?), then routed as a factor-resolved trust gate vs one global r per sim | C1 | [[2402.08191\|THE COLOSSEUM]] (14-factor SR drop, R²=0.614) + [[2405.05941\|SIMPLER]] (in-distribution r only) + [[2604.24018\|Sim2Real Betting]] (aggregate-edge routing) |
| Portfolio of biased sims with provable real-performance CIs vs single accurate sim at equal compute | C2 | [[2604.24018\|Sim2Real Betting]] (biased bank, 70–100% win) + [[2510.04354\|SureSim]] (PPI CIs, 20–25% fewer trials) |
| Proprioception-only latent-extrinsics online adaptation vs fixed domain-randomized policy | D1 | [[2107.04034\|RMA]] (zero-fine-tune, 12 kg payload) + [[2409.16578\|FLaRe]] (50%→80.7% real, +30.7%) |
| Differentiable-sim test-time adaptation (≤3 steps / 4.5 s) vs model-based-RL online fine-tune | D2 | [[2508.21065\|Learning on the Fly]] (81% hover-error, 3-step) + [[2603.04029\|Self-Adapting RL]] ([[2301.04104\|DreamerV3]] fine-tune) |
| World-model-prediction-error online correction with no real reward vs reward-dependent online RL | D3 | [[2602.20057\|AdaWorldPolicy]] (0.96 [[2306.03310\|LIBERO]]-10, 4 Hz, no reward) + [[2603.04029\|Self-Adapting RL]] (residual trigger) |
| Safety-cost-constrained continual adaptation at zero violations vs reward-only online adaptation | E1 | [[2503.10949\|SCDA]] (20%→60% at zero cost, no forgetting) + reward-only (goes unsafe at equal SR) |
| Hard reachability shield (0% collisions) under the residual gap vs soft/probabilistic safety penalty | E2 | [[2409.19190\|RAIL]] (0% vs 5–35% collisions, ~10-pp cost: 68% vs 78%) + soft-constraint IL baselines (5–35% collisions) |
| Conformal runtime failure detection with no failure-labeled data vs supervised failure-trained detector | E3 | [[2506.09937\|SAFE]] (<1 ms, zero-shot) + [[2503.08558\|FAIL-Detect]] (~78%/72%, success-only) |

---

## Cross-References

- [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]] — Reality-gap diagnostics, learned simulators, real2sim2real strategies, domain randomization
- [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] — Physics priors, PINN-grounded learning, physical-consistency design space (anchors A2, B1, B2)
- [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]] — Tactile/force sensing + differentiable tactile sim (anchors A2's GRF reward, B2's [[2604.27367|DOT-Sim]])
- [[07_WAM|07_WAM]] — World models as learned simulators and evaluators (anchors B3, C2, D2, D3)
- [[13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]] — Online/continual adaptation and self-improving policies (anchors D1, D3, E1)
- [[04_Reinforcement-Learning|04_Reinforcement-Learning]] — Online RL fine-tuning, safe RL, continual adaptation (anchors D1, D2, E1)
- [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Canonical robotics + embodied-AI paper index
- [[08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — Canonical survey + benchmark index
- [[Embodied-AI|Embodied-AI]] — Umbrella embodied-AI sibling; its physics-consistency (B3) and world-model-as-simulator directions border this doc's Cluster B (real-to-sim grounding) and D (deploy-time adaptation).
- [[WAM|WAM]] — Focused WAM sibling; world-models-as-learned-simulators connect to this doc's B3 (twin co-training) and D2/D3 (world-model-supervised adaptation).
