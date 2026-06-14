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
> The reality gap is usually treated as one forward problem — train a policy in a simulator, lose performance on hardware — and attacked with more domain randomization. That framing hides two facts. First, how faithfully you can run reality *backward* into the simulator sets a ceiling on how well the simulator predicts reality forward, so real→sim is a gap in its own right, not a side-topic. Second, whatever gap survives every offline fix is observable only at deploy-time, and an un-handled residual there is a *safety* failure, not just a lost success.
> These **15 directions across 5 clusters** are ordered by *when* each one acts on the gap: **train** (A — robustness beyond domain randomization), **reconstruct** (B — run reality backward into a grounded twin), **measure** (C — treat the gap as statistical inference), **deploy** (D — close the residual online), and **bound** (E — act safely under what remains). Each cluster's output is the next's input.
> The editorial bet: **the realism you optimize is not the transfer you want** — on the load-bearing axes (controller gains, domain-randomization marginalization, fidelity proxies) the two are anti-correlated, so the field that *estimates and inverts* beats the field that *randomizes and renders*.

---

## Methodology

**Scope.** This doc reads 6 sim-real surveys + ~17 correlation/evaluation benchmarks (the Survey Landscape below) plus ~25 anchor methods — real2sim2real, robustness-beyond-DR, online adaptation, runtime safety — from `_KnowledgeHub_/`, cross-checked against the deep-dives [[../../../Embodied-AI/14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]], [[../../../Embodied-AI/11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]], and [[../../../Embodied-AI/09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]], and the topic files [[../../../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] and [[../../../General/08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]]. It owns the reality gap as a *mechanism* — forward transfer, real-to-sim reconstruction, gap measurement, deploy-time adaptation, and runtime safety under the residual — across embodiments. The directions are ordered by when they act: train → reconstruct → measure → deploy → bound. Kept where 3–10 papers back a problem with no agreed solution; dropped the saturated (just add more domain randomization) and the premature (a sim from scratch with full causal physics). Force-adaptive whole-body deployment and retargeting sim-to-real are cross-referenced ([[Whole-Body|Whole-Body]]), not re-clustered; world-models-as-simulators are cross-referenced ([[WAM|WAM]]).

---

## Sim-to-Real Survey Landscape

| Survey / Benchmark | The open problem it names (surveys) / what it measures (benchmarks) | Fuels |
|---|---|---|
| [[2604.26509\|3D Generation for Embodied AI Survey]] | Simulation-readiness over visual fidelity; scarcity of physical annotations; geometry-vs-physical-validity trade-off; generative digital twins as the real2sim bridge | A1, B1, B2, B4 |
| [[2601.07823\|Video Generation in Robotics Survey]] | Hallucinations + physics violations; uncertainty quantification; physics priors as the integration fix; robotics-centric benchmarks | A1, A2, D3 |
| [[2507.10087\|Foundation Robotics Review]] | Scarcity of robot-specific embodied data; sim2real gap via semantic alignment + generative simulation; safety from model hallucinations | A1, A3, D1, E1, E2, E3 |
| [[2604.04974\|Video-to-Control Survey]] | The "robotics integration layer" is the critical gap; latent-action identifiability; physical-consistency / hallucinated-physics; pre-execution verification; no standardized eval | A3, B1, B2, B4, C1, D2, D3, E2, E3 |
| [[2605.00080\|WM Robot Learning Survey]] | World models as learned simulators/evaluators; sim2real in long-horizon; eval beyond visual fidelity (action faithfulness + physical consistency); open- vs closed-loop divergence | A2, A3, B1, B3, C2, D1, D3 |
| [[2502.10694\|UDA Simulation Study]] | Domain-shift degradation is context-dependent (backbone, shift type); "negative adaptation" — DA can do worse than no DA under noisy source | C1, C2, E1, E3 |
| [[2402.08191\|THE COLOSSEUM]] | 20 tasks × 14 perturbation axes; 30–50% single-perturbation SR drop, ≥75% combined; R̄²=0.614 sim↔real; distractor/color/lighting worst | A1, C1, E2 |
| [[2405.05941\|SIMPLER]] | Pearson r + MMRV as the sim-real correlation/ranking proxy; r>0.85 (Google Robot) / 0.890 (BridgeData), in-distribution only | C1, C2 |
| [[2605.06311\|VISER]] | Ray-traced PBR visual-realism benchmark; r=0.92, 1,000+ assets, yet "drops drastically" under distractors / OOD | A1, B1, C1 |
| [[2604.24018\|Sim2Real Betting]] | Reframes evaluation as sequential betting over a *bank* of biased simulators; 70–100% win rate over Monte Carlo, tolerates bias with an informative edge | C1, C2 |
| [[2510.04354\|SureSim]] | Prediction-Powered Inference with finite-sample-valid CIs; 20–25% fewer real trials, 14.4% CI tightening with 700 sims | C2 |
| [[2512.19562\|REALM]] | Names the *real-to-sim* gap ("low visual fidelity and misaligned control dynamics"); 15 perturbations with real-to-sim validation; r=0.92 overall / 0.88 default | B1, C1, C2 |
| [[2604.21686\|WorldMark]] | Control-alignment leaders are not visual-quality or world-consistency leaders; ρ>0.9 vs human judgment, no single proxy ranks correctly | C1 |
| [[2604.02523\|Tune to Learn]] | Stiff gains give lowest sysID error yet worst sim-to-real transfer; RL reaches 99%+ only with per-gain tuning | A3 |
| [[2604.10856\|BridgeSim]] | Decomposes the open-loop→closed-loop gap into observational shift + objective mismatch; +19.1 DS via test-time calibration | A3, C2, D2 |
| [[2510.17950\|RoboChallenge]] | Table30 real suite, 30 tasks, contact/soft-body splits (soft-body 8% SR / 27% progress); cross-condition real eval substrate | A2, A3, B3, C2, D1, D2, D3, E1, E2, E3 |
| [[2509.15273\|Embodied Arena]] | Unified evolving evaluation across 22+ benchmarks / 30+ models; the multi-source eval platform | C1, C2 |
| [[2506.10133\|Offline Domain Randomization]] | Formalizes DR as maximum-likelihood estimation of a sim-parameter distribution from offline data, with consistency proofs + α-informativeness | B2 |

> [!tip] Convergence patterns
> - **The reality gap is bidirectional; real→sim is the newer, less-measured edge** (3-way): [[2512.19562|REALM]] explicitly names a *real-to-sim gap* ("low visual fidelity and misaligned control dynamics") distinct from the forward gap; [[2604.26509|3D Generation for Embodied AI Survey]] frames *generative digital twins* as the real2sim bridge and names "scarcity of physical annotations" as the bottleneck; [[2605.00080|WM Robot Learning Survey]] calls for world models as *learned simulators* whose physical consistency, not visual realism, is the ceiling. Three independent sources converge: *how well you run reality backward into the simulator* now gates *how well it predicts reality forward* — the empirical mandate for Cluster B's inversion directions.
> - **Sim fidelity ≠ transfer quality; the proxy you optimize is mis-specified** (4-way): [[2604.02523|Tune to Learn]] shows stiff gains yield the *lowest* system-identification error yet the *worst* transfer — the optimized objective is the wrong one; [[2604.10856|BridgeSim]] decomposes the open-loop→closed-loop gap into observational shift + objective mismatch, naming the proxy mismatch directly; [[2604.21686|WorldMark]] finds control-alignment leaders are not visual-quality or world-consistency leaders, so no single proxy ranks correctly; [[2502.10694|UDA Simulation Study]] names "negative adaptation" — under shift, the adaptation that should help can do *worse* than none. Four benchmarks converge: the quantity we minimize is not the quantity that transfers — the empirical mandate for Cluster A's transfer-what-is-invariant directions and Cluster C's measure-transfer-directly directions.
> - **Sim-to-real evaluation is becoming statistical inference, not accuracy engineering** (4-way): [[2604.24018|Sim2Real Betting]] reframes evaluation as sequential betting over a *bank of biased simulators* (70–100% win rate over Monte Carlo); [[2510.04354|SureSim]] formalizes it as Prediction-Powered Inference with finite-sample-valid confidence intervals (20–25% fewer real trials); [[2509.15273|Embodied Arena]] builds a unified evolving evaluation system across 22+ benchmarks; [[2405.05941|SIMPLER]] establishes Pearson r + MMRV as the correlation/ranking proxy that the others now stress and bound. Four benchmarks converge: the question is shifting from "is the sim accurate?" to "what can I provably infer about real performance from imperfect sims?" — the empirical mandate for Cluster C.
> - **Domain randomization is being re-cast as estimation, not hand-tuning** (3-way): [[2506.10133|Offline Domain Randomization]] proves DR is maximum-likelihood estimation of a sim-parameter distribution, with weak/strong consistency and α-informativeness — the randomization should be *learned*, not set; [[2502.10694|UDA Simulation Study]] shows hand-set adaptation is context-dependent and can invert under shift; [[2604.04974|Video-to-Control Survey]] names "latent-action identifiability" as the unresolved recovery problem under the integration layer. Three sources converge on the same shift: stop hand-setting the nuisance distribution, start identifying it — the empirical mandate for Cluster B's differentiable-recovery directions.

---

## Formal Framing

The reality gap is a divergence between two distributions over trajectories. Let $\tau = (o_0, a_0, o_1, \dots)$ be a rollout. A policy $\pi$ induces a real distribution $p_{\text{real}}(\tau \mid \pi)$ on hardware and a simulated distribution $p_{\text{sim}}(\tau \mid \pi)$ in a simulator parameterized by $\phi$ (appearance) and $\psi$ (dynamics). The **forward (sim-to-real) gap** is the performance divergence when a policy trained under $p_{\text{sim}}$ is deployed under $p_{\text{real}}$; the **inverse (real-to-sim) gap** is the reconstruction error in recovering $(\phi^\star, \psi^\star)$ such that $p_{\text{sim}}(\cdot \mid \phi^\star, \psi^\star) \approx p_{\text{real}}$:

$$\text{Gap}_{\text{S2R}}(\pi) = J_{\text{real}}(\pi) - J_{\text{sim}}(\pi), \qquad \text{Gap}_{\text{R2S}} = \min_{\phi, \psi}\; \mathcal{D}\!\left(p_{\text{real}} \,\|\, p_{\text{sim}}(\cdot \mid \phi, \psi)\right)$$

**The inversion-bound.** The forward map is a function of the recovered $(\phi^\star, \psi^\star)$, so a lossy inversion is an error no amount of forward training can repair: $\text{Gap}_{\text{S2R}}$ is lower-bounded by $\text{Gap}_{\text{R2S}}$. The transfer operator that closes $\text{Gap}_{\text{R2S}}$ and re-opens $\text{Gap}_{\text{S2R}}$ for free is the real2sim2real loop — recover $(\phi^\star, \psi^\star)$ from real data, train/evaluate in the grounded twin, deploy back. Cluster B is the engineering of that operator; Cluster A attacks $\text{Gap}_{\text{S2R}}$ directly without inverting; Cluster C measures both as inference problems; Clusters D and E act on the residual the first three leave behind.

**Four reality-gap objects** organize the directions, each a measurable quantity the clusters build on:

| Object | What it measures | Canonical instrument | Cluster |
|---|---|---|---|
| **Correlation** $\rho$ | Does sim SR track real SR? | Pearson r — [[2405.05941\|SIMPLER]] r≥0.85, [[2605.06311\|VISER]] r=0.92 | A, C |
| **Ranking fidelity** | Does sim order policies correctly? | MMRV (Mean Maximum Rank Violation) — [[2405.05941\|SIMPLER]], [[2512.19562\|REALM]] | C |
| **Reconstruction fidelity** $\text{Gap}_{\text{R2S}}$ | How well does real run backward into sim? | r vs [[2511.04831\|Isaac Lab]] baseline — [[2511.04665\|Real-to-Sim GS]] 0.915 vs 0.649 | B |
| **Provable real bound** | What confidence interval can I assert on real SR? | PPI / sequential betting — [[2510.04354\|SureSim]], [[2604.24018\|Sim2Real Betting]] | C, E |

The **residual gap** is what survives $\text{Gap}_{\text{S2R}}$ after the offline machinery (A, B, C) runs: a time-varying, deployment-only disturbance $\delta(t)$ observable only on hardware. Clusters D and E act on $\delta(t)$ — D estimates and corrects it online, E bounds the cost of whatever remains. The robotics-integration-layer framing is the survey-canonical statement of why the residual exists:

> "The most critical unresolved gaps reside in the 'robotics integration layer,' which involves reliably connecting video-derived predictions to dependable robot behavior, encompassing grounding, loop closure, and physical feasibility." — [[2604.04974|Video-to-Control Survey]]

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Forward Sim-to-Real: Robustness Beyond DR** | A1, A2, A3 | DR randomizes appearance, not the *causes* of outcomes — semantics, physics rewards, and control structure are what transfer | A1's neural-rendering semantics and A2's transferable physics rewards both attack what DR's pixel-shuffle misses; A3's controller-gain insight is the unrecognized hyperparameter that decides whether A1/A2 even transfer. [[2604.02523\|Tune to Learn]]'s gains-vs-sysID inversion and [[2604.11674\|AffordSim]]'s ~24%-average ceiling set the bar |
| **B — Real-to-Sim-to-Real: Grounding the Simulator** | B1, B2, B3, B4 | Recovering $(\phi^\star, \psi^\star)$ from real data is the new bottleneck — and a *chosen* law caps it | B2 recovers the *parameters* of a fixed law; B4 recovers the *law itself*, generalizing the $\psi^\star$ that B1's joint reconstruction needs; B3's co-training loop is the deployment engine that consumes both. [[2511.04665\|Real-to-Sim GS]] is the joint-fidelity substrate, [[2304.14369\|NCLaw]] the generalizable-dynamics model B4 feeds back into it |
| **C — Reality-Gap Measurement as Inference** | C1, C2 | High in-distribution r, untested under deliberate shift, no provable bound | C1 stress-tests whether each sim's per-factor correlation survives shift, then turns the diagnosis into a routing gate; C2's portfolio of biased sims is the estimator C1's gate feeds per-factor weights into. [[2604.24018\|Sim2Real Betting]] supplies both C2's estimator and C1's routing target; both reframe eval from accuracy to inference |
| **D — Deployment-Time Adaptation: Closing the Residual Online** | D1, D2, D3 | The residual $\delta(t)$ that survives A/B/C is time-varying and observable only at deploy-time | D1's proprioception-only latent-extrinsics estimator, D2's exact-gradient differentiable-sim TTA, and D3's learned-world-model prediction-error correction are three online engines split by *which model is on hand* — privileged extrinsics, an analytical model, or only a learned one. [[2603.04029\|Self-Adapting RL]] is the shared residual-trigger primitive |
| **E — Risk-Bounded Sim-to-Real Deployment: Safety Under the Irreducible Gap** | E1, E2, E3 | C measures the residual; an un-handled residual is a *safety* failure, not just a performance one | E1 bounds the *update* (safe continual adaptation), E2 bounds the *action* (reachability shield), E3 *flags* the failure neither can rule out (conformal detection) — three distinct safety surfaces over Cluster D's online updates, each working without failure labels or a hand-built dense reward |

---

## Cluster A — Forward Sim-to-Real: Robustness Beyond Domain Randomization

*Attack the forward gap directly — transfer what is invariant (object semantics, physics-grounded rewards, control structure) rather than randomizing what is not (pixels around an unchanged cause).*

### A1 — Hybrid Neural-Rendering + Physics Simulators for Semantic Sim-to-Real

| | |
|---|---|
| **Cluster** | A — Forward Sim-to-Real |
| **Thesis** | Affordance tasks fail on hardware because domain randomization shuffles pixels but never the object's *function* — a mug's handle-affordance survives every lighting and texture change, so it is never randomized. The first principle: task success depends on appearance-invariant causes (affordance, material response), and randomizing the downstream effect cannot cover variation in the cause. The field assumes visual robustness implies semantic robustness; it does not. The bet is in First-principles below. |
| **Anchor papers** | [[2604.11674\|AffordSim]] (benchmark), [[2604.25459\|GS-Playground]] (method), [[2605.26638\|HyperSim]] (method), [[2604.26509\|3D Generation for Embodied AI Survey]] (survey), [[2605.06311\|VISER]] (benchmark) |
| **Key targets** | Affordance-task real SR from ~24% average / 25% best-policy ([[2604.11674\|AffordSim]] zero-shot, mug-hang ~10%) up by >20 pp; match [[2605.26638\|HyperSim]]'s 75%→95% zero-shot-to-few-shot trajectory; hold [[2604.25459\|GS-Playground]]'s 90% real SR at 10,000-FPS render throughput; [[2605.06311\|VISER]] r=0.92 visual-realism floor |

**Why it matters.**
- **The gap**: domain randomization perturbs lighting, texture, and pose, but a mug's handle-affordance is a *semantic* property that survives every appearance change — so the nuisance axis DR covers and the task axis the policy needs are orthogonal, and affordance tasks fall through.
- **Today's answers**: [[2604.11674|AffordSim]] is the clean diagnostic — even with affordance-aware data and 3DGS-randomized backgrounds, the best zero-shot policy ([[2504.16054|π0.5]]) reaches only 25% (24% averaged), mug-hang ~10%; the rendering frontier supplies the substrate ([[2604.25459|GS-Playground]] runs batch 3DGS at 10,000 FPS / 90% real SR, [[2605.06311|VISER]] hits r=0.92 with ray-traced PBR) — but every one randomizes *appearance*, never semantics. [[2410.07408|Digital Cousins]] already proves the cause-not-effect principle at the *asset* level — varying semantic "digital cousins" of an object beats per-twin reconstruction 90% vs 25% zero-shot SR — so the question is no longer *whether* to randomize the cause but whether doing it *per-episode inside a physics loop* beats it.
- **The opening**: [[2605.26638|HyperSim]] shows reconstruction + constraint-aware foreground moves zero-shot SR from 75% to 95% with 35 demos, and [[2604.26509|3D Generation for Embodied AI Survey]] names the exact missing axis — "interaction readiness, physical grounding, and simulator compatibility" over visual fidelity, bottlenecked by "scarcity of physical annotations."

**First-principles framing.**
- **First principle**: Task success depends on appearance-invariant properties — affordances, mass distribution, and material response are the *causes* of manipulation outcomes; pixels are downstream effects. Randomizing effects cannot cover variation in causes. [[2604.11674|AffordSim]] makes the structure visible: its affordance-aware *data collection* hits 98/79/64% (Easy/Medium/Hard) vs [[2212.08333|AnyGrasp]] 67/15/3%, yet zero-shot real SR still caps at ~24% — the appearance pipeline cannot carry the semantic property the collector encoded.
- **Assumption being challenged**: *Not* "randomize the cause not the effect" — that is already consensus ([[2410.07408|Digital Cousins]]'s 90%-vs-25% asset-level result). The live assumption is that the cause is best varied *offline, at asset-generation time* (Digital Cousins picks a fixed semantic cousin set; [[2604.15805|WorldComposer]] generates a fixed digital-cousin scene), so that appearance is the only thing left to randomize *in the loop* ([[2506.18088|RoboTwin 2.0]]'s 5-axis DR, [[2604.11138|ViserDex]]'s SH-coefficient augmentation). [[2603.22876|Grounding Sim2Real Study]] complicates the realism-doesn't-matter leg ([[2603.16861|MolmoBot]] 79.2% no-photoreal): across 10,000 real trials it finds *frame-wise* perturbation and spatial DR carry transfer, and fidelity *does* help — so the bet must out-perform a strong in-loop appearance pipeline, not a strawman.
- **The bet**: A 3DGS-in-the-loop simulator that re-samples affordance and material *semantics per episode* (not once at asset time, and not appearance) lifts affordance-task real SR **>20 pp over [[2604.11674|AffordSim]]'s ~24% appearance-only ceiling** *and* beats [[2410.07408|Digital Cousins]]-style fixed-cousin asset randomization at matched render budget — pushing mug-hang-class tasks toward [[2605.26638|HyperSim]]'s 95%-with-few-real regime at [[2604.25459|GS-Playground]]-class throughput (10,000 FPS). Falsifiable: if fixed-cousin asset-level semantic randomization ([[2410.07408|Digital Cousins]]) or matched-budget appearance-DR closes the same gap, the *per-episode in-loop* axis is not the lever.

**Related research papers.** One comparison table on the axis the direction turns on — *what each pipeline randomizes / grounds* (appearance only / semantics / in-loop render substrate / reconstruction-then-co-train / task-diversity-not-realism) — plus key result and what each leaves open:

| System | What it randomizes / grounds | Key result | What's missing |
|---|---|---|---|
| [[2604.11674\|AffordSim]] | affordance-aware *data*, 3DGS-randomized backgrounds | collection 98/79/64% vs [[2212.08333\|AnyGrasp]] 67/15/3%; ~24% avg zero-shot real, mug-hang ~10% | the affordance lives in the data, not randomized *in sim* — the appearance-DR ceiling to break |
| [[2604.25459\|GS-Playground]] | appearance, via batch 3DGS bound to rigid bodies | 10,000 FPS, 90% real SR | renders semantics-agnostic — the in-the-loop substrate, no affordance/material randomization |
| [[2605.06311\|VISER]] | appearance, via ray-traced PBR (1,000+ assets) | r=0.92 in-distribution; "drops drastically" under distractors | realism without semantic randomization — the visual-realism floor, not the lever |
| [[2605.26638\|HyperSim]] | 3DGS background + constraint-aware foreground + adversarial trajectories | 75%→95% with 35 demos, +35% first-attempt | grounds foreground structure but not affordance/material *semantics* explicitly |
| [[2604.11138\|ViserDex]] | appearance, via in-loop 3DGS + SH-coefficient augmentation | 37.6 reorientations nominal / ~25 adversarial-lighting, 1.6× faster than tiled | structured DR *inside* the Gaussians — still appearance, not affordance |
| [[2506.18088\|RoboTwin 2.0]] | 5-axis appearance + MLLM-generated tasks | +24.4% real few-shot, +21% zero-shot | the strong appearance-DR baseline a semantic axis must beat on affordance tasks |
| [[2603.16861\|MolmoBot]] | task diversity (1.8M procedural MuJoCo traj), DR *without* photoreal | 79.2% real pick-place vs π0.5-DROID 39.2% | contrarian proof realism isn't the driver — but no affordance/material structure either |
| [[2410.07408\|Digital Cousins]] | semantic *digital-cousin* assets (vary the object's function, fixed at scene-gen time) | 90% vs 25% zero-shot SR over per-twin reconstruction | proves cause-not-effect, but *asset-level* and *fixed-per-scene* — never re-sampled per episode in a physics loop |
| [[2603.22876\|Grounding Sim2Real Study]] | empirical factorial: spatial DR × frame-wise perturbation × fidelity (10,000 real trials) | RL+DR lifts real SR 5.6%→42.8%; fidelity *helps*, frame-wise beats episode-wise | maps *which* DR axis transfers but never adds an affordance/material-semantic axis — the H2/H4 prior to confront |
| [[2510.10637\|RoboSimGS]] | 3DGS photorealism + MLLM-inferred articulation/material props (inferred-then-fixed) | zero-shot Sim2Real + boosts policy when augmenting limited real data | infers physical semantics once per object (like GaussianProperty), randomizes only appearance — no in-loop semantic re-sampling |
| [[2510.15352\|GaussGym]] | real-to-sim 3DGS locomotion-from-pixels, open-source in-loop renderer | learns locomotion directly from rendered pixels | a throughput substrate for in-loop 3DGS (locomotion), semantics-agnostic — the manipulation analog A1 builds on |
| [[2605.09789\|DRIS]] | a *set* of N physical-parameter instances propagated under shared action (not one per episode) | 68% real flat-plate catching vs hand-crafted 5% / sim-trained 13%, lower VRAM | randomizes *physical-parameter uncertainty*, not affordance/material semantics — the structured-DR axis orthogonal to appearance |
| [[2412.11258\|GaussianProperty]] | material *semantics* via LMM reasoning → 3D-Gaussian property tags (not randomized) | 55.83% mIoU material seg vs Nerf2Physics 25.59%; 100% adaptive grasp on 16 objects | material semantics inferred-then-fixed for force-adaptive grasping — the grounded-semantics cousin of Explicit-WM, no in-sim randomization |
| [[2511.23369\|SimScale]] | appearance, via 3DGS-reconstruction + sim-real co-training of perturbed OOD scenes | >20% relative gain for weak baselines, EPDMS 48.0 navhard | appearance-only OOD co-training (driving) — the in-loop reconstruction substrate at scene scale, semantics-agnostic |
| [[2603.13825\|Explicit-WM Manipulation]] | digital-twin geometry + VLM semantics (not randomized) | 75%+ on 6/9 tasks, 90.91% mug-free vs 27.27% direct | semantics via a VLM checker, not randomized in sim — the grounded-but-fixed alternative |
| [[2502.20396\|Humanoid Sim2Real Dex]] | appearance + dynamics DR + distillation (autotuned) | 80% box-lift, 60–80% zero-shot unseen objects, two-hand | strong appearance+dynamics-DR recipe with no semantic axis |
| [[2511.04831\|Isaac Lab]] | nothing semantic — GPU physics + RTX rendering | 900K–1.6M FPS | the physics backbone a semantic in-the-loop renderer attaches to |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (randomizing affordance/material *semantics* beats appearance-only DR), with the experiment and the Related-table row it lands on.
1. **H1 — Affordance-randomized 3DGS-in-the-loop beats appearance-only DR on affordance tasks.**
   - *Prediction*: coupling [[2604.25459|GS-Playground]]'s renderer to a physics engine and randomizing affordance labels + material parameters per episode lifts [[2604.11674|AffordSim]]-class real SR >20 pp over appearance-only DR at matched render budget, with the gain concentrated on the hardest affordance task (mug-hang ~10%).
   - *Test*: train affordance-randomized vs appearance-randomized policies at equal render compute; report real SR per affordance-task tier.
   - *Row*: AffordSim (affordance in data) vs GS-Playground (appearance substrate).
   - *Falsifier*: appearance-DR closes the same gap at matched budget → the semantic axis is not the lever.
2. **H2 — Semantic randomization adds real-SR *on top of* the fidelity gain Grounding-Study found.**
   - *Prediction*: in a 2×2 {PBR low/high} × {semantic-randomization off/on}, the semantic main-effect is non-zero *even at high PBR* — i.e. it survives the fidelity-helps finding of [[2603.22876|Grounding Sim2Real Study]] rather than being absorbed by it.
   - *Test*: run the 2×2 at matched render budget; report semantic main-effect and the semantic×PBR interaction, not just whether semantics beats realism.
   - *Row*: VISER (realism floor) / Grounding Sim2Real Study (fidelity-helps factorial) vs AffordSim (semantic gap).
   - *Falsifier*: the semantic main-effect vanishes at high PBR → semantics is redundant once fidelity is high and the gain was confounded with rendering.
3. **H3 — Auto-labeled affordances from generated assets close the annotation bottleneck.**
   - *Prediction*: [[2604.11674|AffordSim]]'s VoxAfford scorer auto-labels [[2604.26509|3D Generation for Embodied AI Survey]]-style generated assets accurately enough that policies trained on auto-labeled semantics match hand-annotated ones, removing the "physical-annotation scarcity" the survey flags.
   - *Test*: train on auto-labeled vs hand-labeled affordance assets; report the real-SR gap and label-noise sensitivity.
   - *Row*: AffordSim (affordance in data) / Explicit-WM Manipulation (VLM semantics).
   - *Falsifier*: auto-labeled semantics underperform hand-labeled by a wide margin → annotation cannot be bootstrapped and the bottleneck stands.
4. **H4 — Per-episode semantic re-sampling beats fixed-cousin asset randomization.**
   - *Prediction*: re-sampling affordance/material semantics *per episode* in the physics loop recovers more affordance-task real SR than [[2410.07408|Digital Cousins]]-style fixed-per-scene semantic cousins or [[2603.16861|MolmoBot]]'s no-photoreal task diversity, because per-episode variation covers the cause continuously rather than via a discrete cousin set.
   - *Test*: ablate {fixed-cousin asset randomization} vs {per-episode in-loop semantic re-sampling} at matched diversity budget; report affordance-task SR and the [[2603.22876|Grounding Sim2Real Study]] frame-wise-vs-episode-wise contrast on the *semantic* axis.
   - *Row*: Digital Cousins (fixed-cousin) / Grounding Sim2Real Study (frame-wise>episode-wise) vs RoboTwin 2.0 (appearance-DR).
   - *Falsifier*: fixed-cousin randomization matches per-episode re-sampling → the in-loop continuity is not the lever and Digital Cousins' asset-level recipe suffices.
5. **H5 — In-the-loop rendering fits the training budget at affordance scale.**
   - *Prediction*: [[2604.25459|GS-Playground]]'s point-pruning + batch rendering keeps an affordance-randomized physics+3DGS loop within the training-time budget (≥ several thousand FPS), so the semantic gain comes at no throughput cost vs appearance-only DR.
   - *Test*: profile FPS of the semantic-randomized loop vs appearance-only at matched policy quality; report the throughput–SR frontier.
   - *Row*: GS-Playground (in-loop substrate) / ViserDex (in-loop appearance).
   - *Falsifier*: the semantic loop blows the budget → fall back to appearance-DR + a VLM semantic checker (Explicit-WM style).

> [!warning] Risks
> - **Neural rendering in the loop is compute-heavy** — physics + 3DGS per step may blow the training budget. → Use [[2604.25459|GS-Playground]]'s point-pruning + batch rendering (10,000 FPS shows it is tractable, H5 bounds it) and discard auxiliary heads at deploy.
> - **Semantic randomization needs semantic ground truth the field lacks at scale** — affordance labels are scarce. → Bootstrap from [[2604.11674|AffordSim]]'s VoxAfford auto-labeling on [[2604.26509|3D Generation for Embodied AI Survey]]-style generated assets (H3), not hand annotation.
> - **Gains may be confounded with realism** — a richer renderer could improve SR for reasons unrelated to semantics. → H2's semantics-vs-appearance ablation at fixed PBR is the go/no-go; report the semantic main-effect separately.

### A2 — Reward-Signal Sim-to-Real: Transferring PINN-Estimated Physics Rewards, Not Actions

| | |
|---|---|
| **Cluster** | A — Forward Sim-to-Real |
| **Thesis** | Sim-to-real almost always transfers *actions* — a policy or its distilled student. Transferring the *reward* instead is no longer novel: learned reward functions cross embodiments and tasks already. But every learned reward is fit to a data distribution and drifts under dynamics shift, whereas a reward grounded in a physical law is a function of physical *state*, so it scores any trajectory correctly on hardware the policy never saw. The field assumes a transferable reward must be *learned*. The bet is in First-principles below. |
| **Anchor papers** | [[2604.23702\|QuietWalk]] (method), [[2511.15200\|VIRAL]] (method), [[2603.15956\|ExpertGen]] (method), [[2605.00080\|WM Robot Learning Survey]] (survey), [[2510.17950\|RoboChallenge]] (benchmark) |
| **Key targets** | GRF-predictor R²=0.99/0.99 sensor-free ([[2604.23702\|QuietWalk]], up from 0.39/0.67 supervised; 82–86% error reduction from the inverse-dynamics constraint); −7.17 dBA mean / −4.98 dB peak noise transferred across 4 footwear types + outdoor terrains; cross-condition reward stability where DR action policies plateau |

**Why it matters.**
- **The gap**: most sim-to-real pipelines harden the *action* mapping — [[2511.15200|VIRAL]] distills a teacher into a vision student, [[2603.15956|ExpertGen]] distills experts into visuomotor policies, [[2210.13702|DeXtreme]] transfers a PPO policy — so the thing crossing the gap inherits the *simulated* dynamics it was hardened on. Transferring the *reward* instead is a mature alternative ([[2106.03911|XIRL]] cross-embodiment reward since 2021, [[2206.00238|DARL]] dynamics-agnostic discriminator, [[2405.19988|Video-Language Critic]], [[2406.01967|DrEureka]]) — but each reward is *learned* from data, so it drifts under the dynamics shift it was meant to survive.
- **Today's answers**: [[2604.23702|QuietWalk]] grounds the reward in a *law* instead of data — an inverse-dynamics PINN estimates per-foot ground-reaction force from proprioception alone (R²=0.99/0.99), the *frozen predictor* is dropped into the reward as a critic, and the policy then generalizes across barefoot / skate-shoes / sneakers / high-heels and outdoor terrains it never trained on. The PINN encodes a physical law, so its output is invariant to the appearance and contact-dynamics changes that drift a learned reward like [[2405.19988|Video-Language Critic]]'s.
- **The opening**: the inverse-dynamics *constraint* is the lever, not the network — enforcing it cuts GRF error 82–86% vs a purely supervised predictor and lifts R² from 0.39/0.67 to 0.99/0.99, exactly the fidelity a reward needs to hold off-distribution. [[2605.00080|WM Robot Learning Survey]] frames the rationale: a model's value is "its utility for action and physical consistency, not visual realism."

**First-principles framing.**
- **First principle**: A reward grounded in a physical law (momentum, Newton's third law, contact mechanics) is a function of physical *state*, not of training distribution — it scores any trajectory correctly, on hardware the policy never saw. Actions are distribution-bound; physics-grounded rewards are distribution-free. [[2604.23702|QuietWalk]] supplies the load-bearing evidence: the inverse-dynamics constraint — a physical law, not data — is what drives the 82–86% error reduction and the R²=0.99, so the reward is invariant precisely because the constraint is.
- **Assumption being challenged**: That a transferable reward must be *learned* — the learned-reward orthodoxy ([[2106.03911|XIRL]], [[2206.00238|DARL]], [[2405.19988|Video-Language Critic]], [[2406.01967|DrEureka]]) that crosses the gap with a visual-embedding / discriminator / video-language / LLM-designed reward. Each is fit to a distribution, so it drifts under appearance and dynamics shift; a PINN-estimated force reward is a function of physical state, so the high-heels contact-dynamics shift that drifts a learned reward leaves the law-grounded reward intact. (The "reward not policy" framing itself is already consensus — the novelty is *distribution-free*, not *reward-instead-of-action*.)
- **The bet**: A physics-law-grounded reward (GRF, contact wrench) retains its objective across *contact-dynamics* shifts where a *learned* transferable reward drifts — holding [[2604.23702|QuietWalk]]'s **R²=0.99 sensor-free** accuracy and the **−7.17 dBA** objective across **4 footwear types** and outdoor terrains, while a [[2405.19988|Video-Language Critic]]-style learned reward and a [[2511.15200|VIRAL]]-style DR action policy both lose retention under the same shift. The lever is the inverse-dynamics *constraint* (H2): removing it collapses R² toward 0.39/0.67. Cross-*embodiment* portability (robot A's PINN as robot B's reward) is the speculative extension H3 probes — no existence proof yet. Falsifiable: if a learned transferable reward matches the physics-law reward on cross-footwear retention, the law-grounded signal is not the more distribution-free object.

**Related research papers.** One comparison table on the axis the direction turns on — *what crosses the gap, and whether it is a physical law* (physics reward / action policy / hand-designed reward / physics-as-input / transferable representation) — plus key result and what each leaves open:

| System | What crosses the gap | Key result | What's missing |
|---|---|---|---|
| [[2604.23702\|QuietWalk]] | a frozen PINN *force reward* (inverse-dynamics-constrained) | R²=0.99/0.99 sensor-free, −7.17 dBA, 4-footwear + outdoor robust | single-robot cross-*condition* only — cross-embodiment reward portability untested |
| [[2511.15200\|VIRAL]] | the *action* (teacher→vision student) | 54/59 real loco-manip cycles; RSI ablation 95% vs <10% | the canonical action-transfer pipeline — inherits the simulated dynamics it hardened on |
| [[2603.15956\|ExpertGen]] | the *action* (behavior prior + DSRL + distillation) | 90.5% [[2407.08028\|AutoMate]] | action transfer; reward stays sparse, never re-grounded in real physics |
| [[2210.13702\|DeXtreme]] | the *action* (VADR + PPO), hand-designed reward | 27.8 vs 14.8 reorientations (VADR vs manual DR) | reward is hand-engineered, not a physical law — not transferable as a signal |
| [[2106.03911\|XIRL]] | a *learned reward* (visual-embedding IRL), cross-embodiment | self-supervised reward transfers across embodiments | reward is learned from video embeddings, not a law — drifts under appearance/dynamics shift; the foil for "distribution-free" |
| [[2206.00238\|DARL]] | a *learned reward* (dynamics-agnostic discriminator ensemble) | transfers reward across dynamics gaps | discriminator is fit to data — invariance is empirical, not law-grounded |
| [[2405.19988\|Video-Language Critic]] | a *learned reward* (contrastive + sequential-ranking video-language) | 72% avg SR unseen tasks, 2× sample efficiency cross-embodiment | dense learned reward, transferable but distribution-bound — the closest learned-reward competitor |
| [[2406.01967\|DrEureka]] | a *learned reward* (LLM-designed) + DR config for sim2real | LLM-authored reward enables zero-shot sim2real | reward designed by an LLM from task text, not a physical law — no invariance guarantee under contact shift |
| [[2511.07416\|PhysWorld]] | the *reward*, but grounded in a *reconstructed twin* | 82% real, object-centric residual RL | reward is twin-bound (per-object), not a portable physical law |
| [[2510.11689\|Phys2Real]] | physics *as policy input* (CoM, friction) | 57% vs 23% (weight-top T-block) | physics conditions the policy; it is not a transferable reward |
| [[2601.02778\|Force-Based Sim2Real]] | force *via the policy* (tactile feedback) | 25.1 vs 1.1 rotations with/without contact sensing | force is the transferable quantity but rides the policy, not the reward |
| [[2605.28812\|CoP Tactile]] | a physics-grounded contact *representation* (Center-of-Pressure) | 0.78 peg-in-hole zero-shot, latents cluster by mass | a transferable *representation*, not a reward — the input-side cousin |
| [[2603.04029\|Self-Adapting RL]] | a prediction-residual adaptation *trigger* | [[2301.04104\|DreamerV3]] residual → online fine-tune | the online loop a transferable reward would drive — not itself a transfer signal |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a physics-grounded reward transfers across conditions where action policies don't), with the experiment and the Related-table row it lands on.
1. **H1 — Physics-law reward beats a *learned* reward (and action transfer) on cross-condition retention.**
   - *Prediction*: training one contact task three ways — a [[2604.23702|QuietWalk]]-style PINN-force reward, a [[2405.19988|Video-Language Critic]]-style *learned* reward, and a DR+distillation action policy ([[2511.15200|VIRAL]]-style) — and evaluating across held-out conditions (footwear/terrain/payload), the physics-law reward retains the most real SR, with the gap over the *learned* reward widest under the hardest contact-dynamics shift (high heels).
   - *Test*: matched task + base RL, swap only the transferable object across all three; report cross-condition SR retention by shift severity.
   - *Row*: QuietWalk (physics reward) vs Video-Language Critic (learned reward) vs VIRAL (action transfer).
   - *Falsifier*: a learned reward matches the physics-law reward across conditions → law-grounding is not the distribution-free lever, only "reward not policy" is.
2. **H2 — The inverse-dynamics constraint, not the network, is the transfer lever.**
   - *Prediction*: removing the inverse-dynamics constraint (purely supervised GRF predictor) collapses R² from 0.99 toward 0.39/0.67 *and* the resulting reward fails to hold the −7.17 dBA objective off-distribution — so the constraint is what makes the reward distribution-free.
   - *Test*: ablate the inverse-dynamics term; measure GRF R² and cross-footwear objective retention with vs without it.
   - *Row*: QuietWalk (physics reward).
   - *Falsifier*: the supervised predictor's reward transfers equally → the physical constraint is decorative.
3. **H3 — Reward portability across embodiments (the speculative extension).**
   - *Prediction*: a GRF/contact-wrench PINN trained on robot A's proprioception gives a usable reward on robot B without re-collecting demos, within a measurable morphology-distance envelope beyond which R² degrades below a usable threshold.
   - *Test*: transfer the frozen PINN reward A→B; map cross-embodiment SR vs morphology distance.
   - *Row*: QuietWalk (physics reward) / CoP Tactile (transferable representation).
   - *Falsifier*: the cross-embodiment reward is unusable at any morphology distance → portability is single-robot only, as QuietWalk currently shows.
4. **H4 — Sensor-free reward holds where the policy lacks force sensors.**
   - *Prediction*: using the PINN-estimated force as the *only* reward on hardware without force sensors recovers most of the on-sensor SR, with a measurable trust envelope where R² stays above threshold and beyond which the reward misleads.
   - *Test*: deploy sensor-free PINN reward vs ground-truth-force reward; map R² degradation off-manifold and the SR cliff.
   - *Row*: QuietWalk (physics reward) / Force-Based Sim2Real (force via policy).
   - *Falsifier*: sensor-free reward degrades immediately off the training distribution → the reward needs the sensor it was meant to replace.
5. **H5 — Physics-reward generalizes only on conservation/inverse-dynamics tasks.**
   - *Prediction*: the transfer advantage holds on contact/force-dominated tasks where a conservation law or inverse-dynamics constraint exists, and vanishes on semantic tasks where no physical law grounds the reward — so the bet is bounded to the physics regime.
   - *Test*: contrast cross-condition retention on force-dominated vs semantic tasks; report where the physics-reward advantage disappears.
   - *Row*: QuietWalk (physics reward) vs DeXtreme (hand-designed reward).
   - *Falsifier*: the physics-reward transfers on semantic tasks too → the conservation-law boundary is not real and the claim under-scopes.

> [!warning] Risks
> - **PINN rewards exist for few physical quantities** — GRF is clean; arbitrary task rewards are not physical laws. → Bound the claim to contact/force-dominated tasks where a conservation law or inverse-dynamics constraint actually exists (H5); do not over-claim to semantic tasks.
> - **Reward transfer ≠ policy transfer** — a transferable reward still needs an on-hardware optimization loop. → Pair with [[2603.04029|Self-Adapting RL]]'s online fine-tune so the transferable reward drives fast real adaptation rather than from-scratch RL.
> - **PINN degrades off-manifold** — R²=0.99 holds on the training distribution; far OOD it may mislead the reward. → H4 measures the trust envelope explicitly; gate reward use on residual magnitude, and fall back where R² drops below threshold.

### A3 — Controller-Gain-Aware Sim-to-Real: Co-Optimizing Dynamics and Control

| | |
|---|---|
| **Cluster** | A — Forward Sim-to-Real |
| **Thesis** | Randomizing PD gains is already routine DR practice, and runtime adaptive-gain prediction already beats fixed gains on contact tasks. What no one tests is whether the gain and the dynamics *interact* — whether co-optimizing them jointly captures a super-additive term that the standard "tune gains for sysID, then randomize dynamics around them" recipe structurally misses. The field assumes gain and dynamics randomization are separable. The bet is in First-principles below. |
| **Anchor papers** | [[2604.02523\|Tune to Learn]] (method), [[2602.23253\|SPARR]] (method), [[2606.06218\|TAM (Torque Adaptation)]] (method), [[2604.04974\|Video-to-Control Survey]] (survey), [[2510.17950\|RoboChallenge]] (benchmark) |
| **Key targets** | Recover the transfer SR stiff gains destroy *despite* lowest sysID error ([[2604.02523\|Tune to Learn]]); reach RL's 99%+ regime across gain settings without per-gain hand-tuning; beat best-fixed-gain DR on [[2407.08028\|AutoMate]]-class contact tasks (95–100% via [[2602.23253\|SPARR]]) |

**Why it matters.**
- **The gap**: the field treats gains as a fixed robot property, or tunes them for low tracking error during sysID — but the gain is really an unrecognized sim-to-real hyperparameter, setting the dynamics distribution the policy trains against, the action-space smoothness, and the deployment oscillation spectrum all at once.
- **Today's answers**: [[2604.02523|Tune to Learn]] is the result almost nobody has internalized — the gains with the *lowest* sysID error (stiff, overdamped) give the *worst* transfer, amplifying high-frequency oscillation on hardware; RL can reach 99%+ across all gain regimes, but only with per-gain tuning. The competing fix is *runtime* adaptive gains: [[2505.00991|DexCtrl]] jointly learns action + adaptive gains and beats fixed-gain baselines on contact-rich dexterity "without excessive randomization", [[2311.07499|Dynamic Compliance Tuning]] tunes compliance online for industrial insertion, [[2502.14457|Watch Less Feel More]] adapts motion + impedance for articulated objects — all *predict gains at runtime* rather than co-optimizing them into the training distribution.
- **The opening**: [[2604.02523|Tune to Learn]]'s own pairing of per-gain sysID error against sim2real SR *and* oscillation spectrum is the legible metric — the low-sysID-error gains are precisely the high-oscillation, worst-transferring ones, so the objective the field minimizes is anti-correlated with the goal.

**First-principles framing.**
- **First principle**: The controller is part of the plant the policy controls — gains set the closed-loop dynamics, action smoothness, and high-frequency response, so they belong in the transfer distribution, not a separate pre-tuning step. Tuning gains for tracking error optimizes the wrong closed-loop. [[2604.02523|Tune to Learn]] demonstrates it directly: lowest-sysID-error gains are the worst-transferring, so the gain is a *transfer* variable, not a fidelity one.
- **Assumption being challenged**: *Not* "gains belong in the randomization" — PD-gain randomization is routine DR and runtime adaptive gains ([[2505.00991|DexCtrl]], [[2311.07499|Dynamic Compliance Tuning]], [[2502.14457|Watch Less Feel More]]) already beat fixed gains. The live assumption is that gain and dynamics randomization are *separable* — that you can pre-tune (or runtime-adapt) the gain independently of the dynamics distribution. [[2604.02523|Tune to Learn]]'s sysID-vs-transfer inversion implies the closed-loop couples them, so a sequential recipe (or a runtime residual patching a fixed-gain policy) leaves a joint term on the table.
- **The bet**: Co-optimizing $(K_p, K_d)$ *jointly with* the dynamics distribution captures a non-empty **gain×dynamics interaction term** — joint beats (gain-only + dynamics-only) by **more than their sum** on [[2407.08028|AutoMate]]-class contact tasks, *and* the co-optimized DR variable beats a [[2505.00991|DexCtrl]]/[[2606.06218|TAM (Torque Adaptation)]]-style runtime gain residual at matched SR (preventing the mismatch beats patching it). Falsifiable: if joint = gain-only + dynamics-only (additive) **or** the runtime residual matches co-optimization, the interaction term is empty and co-optimization buys nothing.

**Related research papers.** One comparison table on the axis the direction turns on — *how control gains are treated relative to the transfer distribution* (fixed/sysID-tuned / residual-absorbed / co-optimized / implicit-via-action-structure / named-but-unaddressed) — plus key result and what each leaves open:

| System | How gains relate to transfer | Key result | What's missing |
|---|---|---|---|
| [[2604.02523\|Tune to Learn]] | studied across BC/RL/sim2real; lowest-sysID-error = worst transfer | stiff gains worst transfer; RL 99%+ only with per-gain tuning | diagnoses the inversion but never *co-optimizes* gains with DR — the gap this fills |
| [[2602.23253\|SPARR]] | residual absorbs gain/dynamics mismatch after the base policy | 95–100% [[2407.08028\|AutoMate]], 74.5% NIST assembly | the residual patches mismatch post-hoc; gains never enter the randomization |
| [[2606.06218\|TAM (Torque Adaptation)]] | policy-agnostic 1 kHz torque residual (multi-robot pretrain) | Franka pushing 47.6%→76.2%, zero-shot Google Robot (1.05° vs 4.69°) | actuation-residual absorbs gain mismatch, not a co-optimized gain variable |
| [[2505.00991\|DexCtrl]] | *runtime* adaptive gains jointly with action, "without excessive randomization" | beats fixed-gain baselines on contact-rich dexterity | the H4 alternative — predicts gains at *deploy-time*, never co-optimizes them into the training distribution |
| [[2311.07499\|Dynamic Compliance Tuning]] | *runtime* online compliance tuning for industrial insertion | bridges sim2real on insertion via online compliance | runtime gain adaptation, not a training-distribution variable — the residual-side competitor |
| [[2502.14457\|Watch Less Feel More]] | *runtime* motion-adaptation + impedance control (generalizable articulated) | sim-to-real RL on articulated objects via adapted impedance | adapts impedance online; gain never enters the DR distribution as a co-optimized variable |
| [[2210.13702\|DeXtreme]] | action-smoothness reward (implicit gain proxy) | 27.8 vs 14.8 reorientations | smoothness penalty acknowledges gains matter but never makes it a first-class co-optimization |
| [[2511.15200\|VIRAL]] | delta action space flagged critical in ablation | RSI 95% vs <10% | action structure governs transfer, gains not co-optimized |
| [[2603.15956\|ExpertGen]] | DSRL preserves the motion manifold while optimizing reward | 90.5% [[2407.08028\|AutoMate]] | manifold-preservation is gain-adjacent, not a gain×dynamics co-optimization |
| [[2510.11689\|Phys2Real]] | conditions on friction/CoM (the dynamics half) | 57% vs 23% OOD weight-top | the dynamics side of the coupling, no control-gain term |
| [[2604.04974\|Video-to-Control Survey]] | names control-loop closure + physical inconsistency | survey | names the gap, doesn't spot gains as the lever |
| [[2605.00080\|WM Robot Learning Survey]] | open-loop vs closed-loop divergence | survey | the closed-loop is where gains bite, but unnamed as a variable |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (co-optimizing gains with DR beats best-fixed-gain DR), with the experiment and the Related-table row it lands on.
1. **H1 — Gain-randomization beats dynamics-only DR on contact tasks.**
   - *Prediction*: sampling $K_p, K_d$ from a learned/randomized range during training beats fixing them and randomizing only dynamics, on [[2407.08028|AutoMate]]-class contact-task real SR, recovering the transfer [[2604.02523|Tune to Learn]] shows stiff gains destroy.
   - *Test*: gain-randomized vs dynamics-only DR, matched everything else; report contact-task real SR.
   - *Row*: Tune to Learn (gains-vs-sysID).
   - *Falsifier*: dynamics-only DR matches gain-randomization → gains add nothing to the transfer distribution.
2. **H2 — There is a non-empty gain×dynamics interaction term fixed-then-randomize misses.**
   - *Prediction*: jointly co-optimizing $(K_p, K_d, \psi)$ via differentiable sim or bilevel search beats both gain-only and dynamics-only randomization by more than their sum — an interaction term the sequential recipe cannot capture.
   - *Test*: full-factorial {gain rand} × {dynamics rand} × {joint}; test for super-additivity.
   - *Row*: Tune to Learn (gains-vs-sysID) / Phys2Real (dynamics side).
   - *Falsifier*: joint = gain-only + dynamics-only (additive) → there is no interaction and co-optimization is unnecessary.
3. **H3 — Co-optimized gains suppress the deployment oscillation spectrum stiff gains amplify.**
   - *Prediction*: a deployment-time oscillation-spectrum metric shows co-optimized gains have lower high-frequency energy than the low-sysID-error stiff gains [[2604.02523|Tune to Learn]] flags, and the SR gain tracks the oscillation reduction.
   - *Test*: measure oscillation spectrum + SR for co-optimized vs stiff vs compliant gains; regress SR on high-frequency energy.
   - *Row*: Tune to Learn (gains-vs-sysID).
   - *Falsifier*: oscillation energy is uncorrelated with SR → oscillation is not the transfer mechanism.
4. **H4 (deciding) — Co-optimized DR-variable gains beat a runtime adaptive-gain residual.**
   - *Prediction*: making the gain a co-optimized DR variable recovers more transfer SR than a [[2505.00991|DexCtrl]]-style *runtime* adaptive-gain predictor (or a [[2602.23253|SPARR]]/[[2606.06218|TAM (Torque Adaptation)]] residual) at matched SR — preventing the mismatch in the training distribution beats predicting/patching it at deploy-time. This is the front-line falsifier now that runtime adaptive gains are established.
   - *Test*: head-to-head {co-optimized gains, no runtime adapter} vs {fixed gains + DexCtrl-style runtime gain prediction} vs {fixed gains + torque residual} on AutoMate; report SR and adaptation/residual magnitude.
   - *Row*: DexCtrl (runtime adaptive gains) / SPARR (residual) / TAM (torque residual) vs Tune to Learn (gains-vs-sysID).
   - *Falsifier*: the runtime adaptive-gain predictor matches co-optimization → the mismatch is better adapted at runtime than prevented in training, and A3 reduces to DexCtrl.
5. **H5 — The effect is contact-specific; free-space shows a null.**
   - *Prediction*: the co-optimization advantage concentrates on contact-rich tasks (where gains shape the contact-force response) and is near-zero on free-space reaches, so the claim is scoped to contact.
   - *Test*: stratify by contact vs free-space; report the gain-co-optimization margin per regime.
   - *Row*: Tune to Learn (gains-vs-sysID) / SPARR (contact residual).
   - *Falsifier*: free-space tasks show the same margin → gains are not the contact-specific lever the bet claims.

> [!warning] Risks
> - **Gain co-optimization explodes the search space** — adding $(K_p, K_d)$ to DR multiplies training cost. → Use [[2604.02523|Tune to Learn]]'s finding to seed a narrow compliant/overdamped prior rather than searching the full grid.
> - **Hardware gain limits** — real controllers cap achievable gains; co-optimized values may be infeasible. → Constrain the co-optimization to the hardware's admissible gain box and validate on the real controller.
> - **Effect may be task-specific** — gains matter most for contact; free-space tasks may show little gain. → Scope the claim to contact-rich tasks ([[2407.08028|AutoMate]]/NIST) and report the free-space null result honestly (H5).

---

## Cluster B — Real-to-Sim-to-Real: Grounding the Simulator in Deployment

*Invert reality into the simulator first — recover appearance and dynamics from real data — then the forward transfer comes nearly for free, because a simulator predicts reality forward no better than it captured reality backward.*

### B1 — Closing the Real-to-Sim Gap: Reconstruction Fidelity as the New Bottleneck

| | |
|---|---|
| **Cluster** | B — Real-to-Sim-to-Real |
| **Thesis** | [[2512.19562\|REALM]] is the first to name the *real-to-sim* gap as a distinct object. Once named, the arrow flips: forward sim-real correlation is upper-bounded by how faithfully reality was inverted into the simulator. Joint appearance+physics inversion is now a crowded engine, so the open science is not *whether* to invert jointly but *how reconstruction fidelity maps to forward transfer* — a law nobody has measured, and one the navigation literature shows is not even monotone. The field still treats this as solved by better engines. The bet is in First-principles below. |
| **Anchor papers** | [[2511.04665\|Real-to-Sim GS]] (method), [[2512.19562\|REALM]] (benchmark), [[2503.17973\|PhysTwin]] (method), [[2605.26638\|HyperSim]] (method), [[2207.10821\|Lower-Fidelity Sim2Real]] (method), [[2604.26509\|3D Generation for Embodied AI Survey]] (survey) |
| **Key targets** | A monotone fidelity→forward-r law per object class, with deformable Δr (rope 0.901 vs [[2511.04831\|Isaac Lab]] 0.237) exceeding rigid Δr (push-T 0.915 vs 0.649) — [[2511.04665\|Real-to-Sim GS]] supplies the joint-inversion substrate; the law must hold where [[2207.10821\|Lower-Fidelity Sim2Real]]'s navigation counter-example does not; [[2512.19562\|REALM]] r=0.92 overall / 0.88 default; [[2605.26638\|HyperSim]] 75%→95% from reconstruction fidelity |

**Why it matters.**
- **The gap**: the field invests in *forward* realism — better engines, more domain randomization — but once you name a real-to-sim gap distinct from the forward one, the causal arrow flips: forward correlation is capped by inversion fidelity, and no forward training can lift a lossy inversion.
- **Today's answers**: [[2512.19562|REALM]] is the first benchmark to name the real-to-sim gap ("low visual fidelity and misaligned control dynamics"); [[2511.04665|Real-to-Sim GS]] proves the consequence — joint 3DGS-appearance + physics optimization hits r=0.915 on push-T (0.901 on soft-body rope) where [[2511.04831|Isaac Lab]] manages 0.649 (0.237 on rope), and its ablation collapses correlation when *either* color alignment or physics optimization is removed.
- **The opening**: the gap closes only when *both* appearance and dynamics are inverted together (the joint-ablation result), and [[2605.26638|HyperSim]] confirms the leverage — better reconstruction moves zero-shot SR from 75% to 95% with 35 demos. But the joint-inversion *engine* is now consensus ([[2506.04120|Splatting Physical Scenes]] and [[2412.00259|One-Shot Real-to-Sim]] both jointly optimize geometry+appearance+physics end-to-end; [[2512.19390|TwinAligner]] adds visual+dynamic alignment; [[2603.01151|D-REX]] adds a policy) — so the bottleneck is not building the engine but establishing the *law* that maps reconstruction fidelity to forward r, which [[2207.10821|Lower-Fidelity Sim2Real]] shows is not even universally monotone (lower fidelity *helped* navigation transfer).

**First-principles framing.**
- **First principle**: A simulator predicts reality forward no better than it captured reality backward — $\text{Gap}_{\text{S2R}}$ is lower-bounded by $\text{Gap}_{\text{R2S}}$. The forward map is a function of the recovered $(\phi^\star, \psi^\star)$; a lossy inversion is a ceiling no forward training raises. [[2511.04665|Real-to-Sim GS]]'s ablation is the proof: removing color *or* physics alignment collapses the correlation, so the bound is *joint*-reconstruction-bound, not appearance- or physics-alone.
- **Assumption being challenged**: *Not* "invert jointly" — that mechanism is consensus ([[2506.04120|Splatting Physical Scenes]], [[2412.00259|One-Shot Real-to-Sim]], [[2512.19390|TwinAligner]], [[2603.01151|D-REX]] all jointly invert geometry+appearance+physics). The live assumption is that reconstruction fidelity *monotonically* predicts forward transfer, so "reconstruct better" is the recipe. [[2207.10821|Lower-Fidelity Sim2Real]] breaks it head-on — lower-fidelity simulation gave *higher* sim2real transfer in navigation — so the fidelity→r map is task-dependent and must be *measured*, not assumed, before it can bound anything.
- **The bet**: Across rigid/articulated/deformable object classes there is a **monotone, measurable fidelity→r law** — degrading reconstruction error in controlled steps predicts forward r per object class — and the joint-inversion advantage is **widest on deformables** ([[2511.04665|Real-to-Sim GS]] 0.901 vs [[2511.04831|Isaac Lab]] 0.237 on rope, vs 0.915 vs 0.649 push-T), the regime [[2207.10821|Lower-Fidelity Sim2Real]]'s navigation counter-example does *not* cover. Falsifiable: if forward r is insensitive to reconstruction error (flat law) *or* the deformable Δr equals the rigid Δr, the arrow does not flip and one number generalizes.

**Related research papers.** One comparison table on the axis the direction turns on — *what is inverted and how jointly* (joint appearance+physics / continuous correction / twin via alignment / generative single-view / deformable-specialized / video-to-asset) — plus key result and what each leaves open:

| System | What is inverted (how jointly) | Key result | What's missing |
|---|---|---|---|
| [[2511.04665\|Real-to-Sim GS]] | 3DGS appearance + soft-body physics, *jointly* | r=0.915 push-T / 0.901 rope vs [[2511.04831\|Isaac Lab]] 0.649 / 0.237; ablation collapses on removing either | per-scene cost; control-dynamics misalignment is a separate term it doesn't close |
| [[2512.19562\|REALM]] | [[2403.12945\|DROID]]-aligned sysID, names the real-to-sim gap | r=0.92 overall / 0.88 default; unseen objects drop most | names + measures the gap but supplies sysID alignment, not joint appearance+physics inversion |
| [[2503.17973\|PhysTwin]] | geometry + physical params + appearance from video | generalizes to unseen interactions | the inversion *engine* [[2511.04665\|Real-to-Sim GS]] builds on — not itself a forward-correlation benchmark |
| [[2605.09538\|PhysHanDI]] | dense hand + *deformable*-object twin from sparse-view RGB-D, *reciprocally* refined | 2× / >7× lower spring RRD than [[2503.17973\|PhysTwin]]; Hand Chamfer 7.57→7.17 mm | sharpens the deformable-inversion [[2503.17973\|PhysTwin]] leaves coarse, but hand-object-contact-specific — no forward-correlation measurement |
| [[2504.03597\|Real-is-Sim]] | dynamic twin ([[2406.10788\|Embodied Gaussians]]) corrected at 60 Hz by real RGB | 57%→80%, 82% best PushT | continuous *correction*, not an offline joint inversion — the runtime-grounding alternative |
| [[2512.16881\|PolaRiS]] | interactive sim from wrist-camera real-video scans | r=0.9 avg / 0.98 best vs RoboArena, <20 min/scene | reconstruction → forward correlation at scale, but appearance-led; physics inversion lighter |
| [[2604.15805\|WorldComposer]] | generative real-to-sim from one panorama → 3DGS + collision mesh | r=0.91 sim-real SR | generative single-view inversion — the cheap route to r>0.9, fidelity bounded by the generator |
| [[2604.08544\|SIM1]] | deformable data engine, sub-mm geometric + AVBD-stable dynamic alignment | 76% zero-shot from de-novo init where real-data baselines hit 0% | joint inversion *where the gap is widest* (deformables) — but a data engine, not a correlation benchmark |
| [[2512.14696\|CRISP]] | real-to-sim from monocular human-scene video (planar fit + contact completion) | 93.1% real-to-sim vs VideoMimic 44.8% at 23K FPS | the video-to-asset inversion route; scene-level, not object-physics joint inversion |
| [[2404.09833\|Video2Game]] | single-video → NeRF + mesh + physics twin | 100+ FPS browser | appearance-heavy, lighter physics — the unbalanced-inversion contrast |
| [[2603.13825\|Explicit-WM Manipulation]] | twin via [[2501.12202\|Hunyuan3D]] + [[2304.07193\|DINOv2]]/ICP alignment | 90.91% mug-free vs 27.27% direct | alignment fidelity gates SR, confirming the bound — but per-object, not joint photoreal+physics |
| [[2506.04120\|Splatting Physical Scenes]] | geometry + appearance + physics, *jointly* end-to-end from imperfect robot data | end-to-end real-to-sim from imperfect data | joint-inversion engine — proves the mechanism is consensus, but never runs the forward-correlation benchmark |
| [[2412.00259\|One-Shot Real-to-Sim]] | geometry + appearance + physics, *jointly* via differentiable sim+rendering, one shot | one-shot end-to-end differentiable inversion | the joint-inversion mechanism B1's bet rests on — but no fidelity→r law, no per-object-class sweep |
| [[2512.19390\|TwinAligner]] | visual + dynamic alignment (physics-aware real2sim2real) | high sim-real policy consistency | aligns both channels and reports consistency — but consistency, not a measured fidelity→correlation law |
| [[2603.01151\|D-REX]] | mass + appearance jointly (GS + differentiable physics) → policy | mass error 4.8–12.0%, 86% avg policy SR | joint inversion *plus a policy* — the engine extended downstream, but no forward-correlation sweep |
| [[2207.10821\|Lower-Fidelity Sim2Real]] | *lowers* fidelity deliberately (navigation) | lower-fidelity sim → higher sim2real transfer | the contrarian counter-example — fidelity→transfer is non-monotone in navigation, breaking the "reconstruct better" assumption |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (joint appearance+physics inversion is the forward-correlation ceiling), with the experiment and the Related-table row it lands on.
1. **H1 — The fidelity→r law is monotone on contact manipulation, where the navigation counter-example does not reach.**
   - *Prediction*: on contact-rich manipulation, degrading reconstruction fidelity in controlled steps *monotonically* lowers forward r — i.e. [[2207.10821|Lower-Fidelity Sim2Real]]'s lower-fidelity-helps result is navigation-specific and does *not* generalize to manipulation, where the joint-inversion engines ([[2506.04120|Splatting Physical Scenes]], [[2412.00259|One-Shot Real-to-Sim]]) operate.
   - *Test*: controlled fidelity-degradation sweep on manipulation tasks; regress forward r on reconstruction error and compare the sign to the navigation result.
   - *Row*: Real-to-Sim GS (joint) vs Lower-Fidelity Sim2Real (non-monotone navigation).
   - *Falsifier*: forward r is flat or *rises* as manipulation fidelity drops → the fidelity→r map is non-monotone for manipulation too and the arrow does not flip.
2. **H2 — The monotone law is an offline twin-ranker (predicts forward r per object class).**
   - *Prediction*: the fidelity→r regression from H1 generalizes across rigid/articulated/deformable well enough to *rank* twins by predicted forward transfer before any forward rollout — so $\text{Gap}_{\text{R2S}}$ predicts forward transferability offline.
   - *Test*: fit the law on a held-out object subset; predict forward r on new objects and measure rank correlation against the realized forward r.
   - *Row*: Real-to-Sim GS (joint) / SIM1 (deformable).
   - *Falsifier*: predicted forward r does not rank twins → the law is descriptive, not predictive, and offline twin selection fails.
3. **H3 — Improving unseen-object inversion beats forward DR for novel objects.**
   - *Prediction*: [[2512.19562|REALM]] shows unseen objects drop most; generative-prior reconstruction ([[2604.15805|WorldComposer]]-style) closes that drop *more* than forward domain randomization does, because the drop is an inversion failure, not a forward-coverage failure.
   - *Test*: on unseen objects, compare {better inversion} vs {more forward DR} at matched compute; report the recovered correlation.
   - *Row*: REALM (unseen-object drop) vs WorldComposer (generative inversion).
   - *Falsifier*: forward DR closes the unseen-object drop as well → the drop is a coverage problem, not an inversion one.
4. **H4 — The widest inversion advantage is on deformables, not rigid.**
   - *Prediction*: the joint-inversion advantage over [[2511.04831|Isaac Lab]] is larger on soft-body rope (0.901 vs 0.237) than rigid push-T (0.915 vs 0.649), because forward engines model deformables worst — so the r>0.9 bet must be reported per object-class.
   - *Test*: report the inversion advantage (Δr vs Isaac Lab) stratified by rigid / articulated / deformable.
   - *Row*: Real-to-Sim GS (joint) / SIM1 (deformable).
   - *Falsifier*: rigid and deformable show equal Δr → the deformable-specific advantage is illusory and one number generalizes.
5. **H5 — Control-dynamics misalignment is a residual term inversion alone leaves open.**
   - *Prediction*: even at r>0.9 from joint appearance+physics inversion, [[2512.19562|REALM]]'s control-dynamics misalignment caps the remaining correlation — co-optimizing control alignment (links to A3) recovers the residual that appearance+physics inversion cannot.
   - *Test*: measure correlation with appearance+physics inversion alone vs + control-alignment; report the residual closed by the control term.
   - *Row*: REALM (real-to-sim gap) / Real-to-Sim GS (joint).
   - *Falsifier*: control alignment adds nothing past joint inversion → appearance+physics inversion fully closes the gap and the control term is redundant.

> [!warning] Risks
> - **Reconstruction is per-scene expensive** — joint 3DGS + physics fitting per object/scene may not scale to open worlds. → Amortize with generative reconstruction priors ([[2604.26509|3D Generation for Embodied AI Survey]], [[2604.15805|WorldComposer]]) and reuse twins across tasks.
> - **The gap to [[2511.04831|Isaac Lab]] is widest on deformables** — the r=0.915 headline is rigid push-T, but the largest advantage is soft-body rope (0.901 vs 0.237). → Scope the >0.9 bet across rigid and deformable, reporting the per-object-class delta separately (H4) rather than assuming one number generalizes.
> - **Inversion fidelity may not be the *only* bound** — control-dynamics misalignment ([[2512.19562|REALM]]) is a separate term. → Co-optimize control alignment (links to A3, H5) alongside appearance+physics rather than assuming reconstruction alone closes the gap.

### B2 — Amortized Differentiable System-ID: Zero-Per-Object Gradient sysID in Clutter

| | |
|---|---|
| **Cluster** | B — Real-to-Sim-to-Real |
| **Thesis** | Recovering a constitutive parameter by gradient descent through a differentiable simulator is now a solved engine — a real-to-sim-to-real loop already identifies an object's physics from interaction and feeds a policy that beats domain randomization out-of-distribution. But every such loop runs *per object*: it re-optimizes from interaction demos for each new item. The first principle is that the observation→parameter map is itself a learnable function, so once trained on differentiable-sim rollouts it should infer parameters for a *novel* object in clutter at zero per-object demos. The field assumes per-object gradient recovery is the unit of sysID. The bet is in First-principles below. |
| **Anchor papers** | [[2603.01151\|D-REX]] (method), [[2604.27367\|DOT-Sim]] (method), [[2510.11689\|Phys2Real]] (method), [[2503.17973\|PhysTwin]] (method), [[2506.10133\|Offline Domain Randomization]] (benchmark), [[2604.04974\|Video-to-Control Survey]] (survey) |
| **Key targets** | Beat per-object gradient sysID ([[2603.01151\|D-REX]] mass error 4.8–12.0%, 86% avg policy SR, but ≥20 demos/object) at **zero per-object demos** via an amortized inference net; reproduce the gradient-sysID-vs-DR-on-OOD advantage ([[2603.01151\|D-REX]] 9–10/10 vs DR 4–9/10 below the DR support; [[2510.11689\|Phys2Real]] 57% vs 23% weight-top) while extrapolating to *unseen objects in clutter* |

**Why it matters.**
- **The gap**: gradient sysID through a differentiable simulator is no longer the open problem — [[2603.01151|D-REX]] (a "Differentiable Real-to-Sim-to-Real Engine") already recovers an object's mass by gradient descent on a trajectory-reconstruction loss and drives a force-aware policy that beats DR on OOD mass. What survives is *scale*: every such loop re-runs from scratch for each object, so it cannot identify a *novel* object in clutter without fresh interaction demos.
- **Today's answers**: [[2603.01151|D-REX]] recovers mass to 4.8–12.0% error "without object-specific tuning" and beats a mass-randomized DR baseline below the DR support (9–10/10 vs 4–9/10), but needs 20+ demos per object and identifies *only mass* (friction/stiffness/Young's/Poisson deferred); [[2510.11689|Phys2Real]] quantifies the same DR-vs-estimation gap (57% vs 23% OOD weight-top) but estimates per-object online; [[2604.27367|DOT-Sim]] recovers Young's modulus and Poisson's ratio per object by differentiable MPM.
- **The opening**: [[2506.10133|Offline Domain Randomization]] proves DR *is* maximum-likelihood estimation of a parameter distribution from offline data — so the same offline data could instead train an *amortized* observation→parameter network, turning per-object gradient recovery into a single forward pass at deploy-time (the card's own Risk-3, now the front-line bet).

**First-principles framing.**
- **First principle**: The map from observations (RGB-D, interaction history) to constitutive parameters is a *function*, and a function can be amortized — trained once on differentiable-sim rollouts, it infers parameters for a novel object in a single forward pass, no per-object gradient loop. The differentiable simulator that recovers parameters per object ([[2603.01151|D-REX]]) is exactly the data generator for that network's supervision. [[2506.10133|Offline Domain Randomization]]'s reframing of DR as estimation-from-offline-data is the evidence that the offline corpus carries enough signal to *learn the inverse map*, not just average over it.
- **Assumption being challenged**: That per-object gradient recovery is the unit of sysID — the differentiable-sysID orthodoxy ([[2603.01151|D-REX]], [[2604.27367|DOT-Sim]], [[2503.17973|PhysTwin]], [[2412.00259|One-Shot Real-to-Sim]]) that re-optimizes from interaction demos for *each* object. D-REX's own 20+-demos-per-object cost and mass-only scope show the per-object loop does not scale to clutter or to a full constitutive vector; an amortized net trades a per-object loop for a one-time training cost.
- **The bet**: An amortized observation→parameter network, trained on differentiable-sim rollouts, recovers constitutive parameters for **unseen objects in clutter at zero per-object demos** and reproduces the gradient-sysID-vs-DR-on-OOD advantage ([[2603.01151|D-REX]] 9–10/10 vs DR 4–9/10 below the DR support) **on objects it never saw** — making the falsifiable measurement the *SR-vs-parameter-distance frontier* (real SR as a function of how far the test parameter sits from the prior mean) for {amortized inference} vs {per-object gradient sysID} vs {DR}. Falsifiable: if the amortized net needs per-object demos to match D-REX's recovery, or DR matches it across the OOD frontier, amortization buys nothing over the per-object loop.

**Related research papers.** One comparison table on the axis the direction turns on — *how the parameter is recovered and whether it amortizes across objects* (per-object differentiable recovery / VLM-prior + online estimation / DR marginalization / distill-around-the-sim / amortizable substrate) — plus key result and what each leaves open:

| System | How parameters are obtained | Key result | What's missing |
|---|---|---|---|
| [[2603.01151\|D-REX]] | *per-object* gradient mass recovery (GS + differentiable physics, VLM-seeded) → policy | mass error 4.8–12.0%; 86% avg SR; beats DR 9–10/10 vs 4–9/10 below DR support | the topThreat — solves per-object gradient sysID beating DR on OOD, but ≥20 demos/object, mass only, no amortization to unseen objects |
| [[2604.27367\|DOT-Sim]] | *per-object* differentiable MPM recovery from few demos (FEA pseudo-GT) | 1.71 mm Chamfer, PSNR 30.48, 96.55% zero-shot tumor | optical-tactile/deformable per-object fit; never amortizes the inverse map across objects |
| [[2104.02646\|gradSim]] | *per-object* gradient recovery of mass/friction/elasticity by backprop from video | recovers physical params from video by differentiable rendering+physics | the 2021 root that proves the gradient-sysID first principle — per-object, no amortization |
| [[2404.12308\|ASID]] | *few-demo* exploration-driven differentiable sysID, beats DR | few-real-interaction sysID beats domain randomization | few-demo per-object loop (ICLR'24 Oral) — confirms the bet's mechanism, leaves amortization open |
| [[2412.00259\|One-Shot Real-to-Sim]] | *one-shot* joint geometry+appearance+physics via differentiable sim+rendering | one-shot end-to-end differentiable inversion | one-shot but still *per object* — the closest to amortization, but re-runs per item |
| [[2411.00554\|DPSI]] | *single-interaction* recovery of Young's/Poisson/yield (= DOT-Sim's quantities) | single-interaction constitutive ID | single-interaction per-object recovery (IJRR), not a learned cross-object inference net |
| [[2204.03139\|DiffCloud]] | *per-object* differentiable point-cloud sysID for cloth | differentiable cloth parameter recovery from point clouds | deformable per-object fit — no amortized inverse map |
| [[2510.11689\|Phys2Real]] | VLM prior + online inverse-variance-weighted *per-object* estimation | 57% vs 23% (weight-top), 100% vs 79% (weight-bottom) | per-object online estimation of a *chosen* law — the DR-vs-estimation evidence, not amortized |
| [[2506.10133\|Offline Domain Randomization]] | DR *as* maximum-likelihood estimation of a parameter distribution | consistency proofs + α-informativeness | the statistical case that offline data carries the inverse map — the amortization substrate |
| [[2603.04531\|PTLD]] | distill real privileged tactile, *bypassing* sysID | +182% rotation, 50% lower 6D pose error | distill-around-the-gap — no parameter, no amortization, cannot extrapolate to unseen values |
| [[2605.28812\|CoP Tactile]] | differentiable calibration of taxel orientations (no GT force) | 0.78 peg-in-hole zero-shot | per-sensor differentiable calibration, not a cross-object constitutive inference net |
| [[2604.10856\|BridgeSim]] | flow-matching observational calibrator + truncated Q-estimator | +19.1 DS for OL→CL | test-time *observational* calibration, adjacent to amortized parameter inference |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (an amortized inference net recovers parameters for unseen objects in clutter at zero per-object demos and reproduces the DR-on-OOD advantage), with the experiment and the Related-table row it lands on.
1. **H1 — Amortized inference matches per-object gradient sysID at zero per-object demos.**
   - *Prediction*: an amortized observation→parameter net trained on differentiable-sim rollouts recovers parameters for *unseen* objects at zero per-object demos within the accuracy [[2603.01151|D-REX]] reaches with 20+ demos/object (4.8–12.0% mass error), so the per-object loop is replaceable by a forward pass.
   - *Test*: hold out object instances; compare amortized-net recovery error vs D-REX per-object recovery error at matched parameter set.
   - *Row*: D-REX (per-object gradient) vs Offline Domain Randomization (amortization substrate).
   - *Falsifier*: the amortized net needs per-object demos to match D-REX → amortization fails and per-object recovery is the irreducible unit.
2. **H2 — The SR-vs-parameter-distance frontier: amortized estimation beats DR off the prior support.**
   - *Prediction*: plotting real SR against test-parameter distance from the prior mean, amortized inference tracks [[2603.01151|D-REX]]'s estimation advantage over DR (9–10/10 vs 4–9/10 below the DR support; [[2510.11689|Phys2Real]] 57% vs 23%) *on unseen objects* — the gap widening with distance.
   - *Test*: sweep test parameters across and beyond the DR support; report SR vs parameter distance for {amortized}, {per-object gradient}, {DR}.
   - *Row*: D-REX (estimation>DR off-support) vs Offline Domain Randomization (marginalization).
   - *Falsifier*: DR matches amortized estimation across the frontier → marginalizing is as good as estimating and the OOD advantage is illusory.
3. **H3 — Amortization scales to clutter where per-object loops cannot.**
   - *Prediction*: in a multi-object scene, the amortized net identifies every object's parameters in one pass while a per-object gradient loop ([[2603.01151|D-REX]]/[[2604.27367|DOT-Sim]]-style) costs N optimizations — so the amortized real SR at fixed deploy-time budget exceeds the per-object loop's once N>1.
   - *Test*: vary scene object count; report real SR and wall-clock for {amortized one-pass} vs {N per-object loops} at matched compute budget.
   - *Row*: D-REX (per-object loop) / DOT-Sim (per-object MPM).
   - *Falsifier*: per-object loops keep pace with amortization in clutter → the per-object cost is not the binding constraint.
4. **H4 — A full constitutive vector amortizes, not just mass.**
   - *Prediction*: the amortized net recovers a *vector* (mass + friction + stiffness/Young's) for unseen objects where [[2603.01151|D-REX]] identifies only mass and [[2411.00554|DPSI]] needs a fresh single-interaction per object — so the inverse map generalizes across the constitutive dimensions D-REX defers.
   - *Test*: train the amortized net on multi-parameter differentiable-sim rollouts; report per-parameter recovery error on unseen objects vs D-REX (mass-only) and DPSI (single-interaction).
   - *Row*: D-REX (mass only) / DPSI (single-interaction Young's/Poisson/yield).
   - *Falsifier*: only mass amortizes, the rest needs per-object recovery → the inverse map is parameter-specific and the vector claim fails.
5. **H5 — Amortized parameters beat a distilled around-the-sim policy on OOD generalization.**
   - *Prediction*: training in a sim corrected by amortized parameters generalizes to OOD physics better than [[2603.04531|PTLD]]'s distill-the-real-privileged-signal route, which never identifies a parameter and so cannot extrapolate to unseen values.
   - *Test*: {amortized sysID + sim training} vs {distill-around-the-gap} on OOD physical-parameter generalization for unseen objects.
   - *Row*: PTLD (distill-around) vs D-REX (identified-parameter).
   - *Falsifier*: distillation matches identified-parameter generalization → recovering the parameter (amortized or not) buys no OOD advantage.

> [!warning] Risks
> - **Amortized inference may not transfer past its training distribution of objects** — the net learns the inverse map only over the object/parameter range it was trained on. → Train on a wide differentiable-sim object/parameter corpus and report recovery error vs distance from the training distribution (H1/H2); fall back to a per-object [[2603.01151|D-REX]] loop where the amortized estimate is low-confidence.
> - **Differentiable sims exist for few physics regimes** — MPM/soft-body yes, rich contact + friction transients less so. → Generate the amortization corpus in [[2604.27367|DOT-Sim]]/[[2503.17973|PhysTwin]]'s deformable/soft-contact regime where differentiability is mature; expand to rigid contact cautiously (H4 scopes which parameters amortize).
> - **Clutter breaks the observation→parameter map** — occlusion and contact between objects corrupt the per-object observation the net conditions on. → Condition the amortized net on segmented per-object observations and report recovery error vs occlusion level (H3); gate on segmentation confidence.

### B3 — Bidirectional Sim↔Real Co-Training: The Twin as a Data Engine, Not a Sandbox

| | |
|---|---|
| **Cluster** | B — Real-to-Sim-to-Real |
| **Thesis** | A reconstructed twin generates training-valid data, and closing a real→sim→real loop that folds deployment data back beats one-shot training — both already shown at the lifecycle scale. What no one has measured on a *per-task object-grounded* twin is whether folding back keeps improving *monotonically across rounds* rather than drifting, and how the per-round gain scales with reconstruction fidelity. The first principle: an ungated fold-back loop can amplify reconstruction error, so monotone improvement requires a fidelity gate. The field assumes the closed loop is unconditionally self-improving. The bet is in First-principles below. |
| **Anchor papers** | [[2403.03949\|RialTo]] (method), [[2512.00076\|Arcadia]] (method), [[2605.26638\|HyperSim]] (method), [[2504.03597\|Real-is-Sim]] (method), [[2605.00080\|WM Robot Learning Survey]] (survey), [[2510.17950\|RoboChallenge]] (benchmark) |
| **Key targets** | A fidelity-gated per-task fold-back loop that is **monotone across rounds** where an ungated loop drifts; the reconstruction-fidelity *exchange rate* ([[2504.03597\|Real-is-Sim]] 30 sim ≈ 30 real, 57%→80%) rising with twin fidelity (link to B1); reproduce [[2403.03949\|RialTo]]'s 90% (target twin) vs 10% (generic) grounding advantage and [[2605.26638\|HyperSim]] 75%→95% on a per-task object twin, beating [[2512.00076\|Arcadia]]'s single feedback-on/off lifecycle delta (LIBERO 88.5 vs 86.9) over successive rounds |

**Why it matters.**
- **The gap**: most of the corpus uses twins as sandboxes — places to evaluate policies cheaply ([[2504.03597|Real-is-Sim]], [[2511.04665|Real-to-Sim GS]] are evaluation frameworks) — which discards the twin's generative capacity entirely.
- **Today's answers**: the highest-leverage results use twins as *data engines* — [[2403.03949|RialTo]] reconstructs a twin from real data, runs RL inside it, distills back (91% pose-rand real), and its decisive ablation shows a policy trained on the *target-specific* twin hits 90% on the real drawer while a generic-asset one manages 10%; [[2605.26638|HyperSim]]'s co-training (abundant synthetic + 35 real demos) lifts 75% to 95%; [[2506.18088|RoboTwin 2.0]] gets +24.4% real few-shot.
- **The closed loop is now claimed**: [[2512.00076|Arcadia]] operationalizes a real→sim→real lifecycle that re-grounds both reconstructed assets and policy from deployment feedback, and states B3's H1 falsifier verbatim — "removing any stage reverts to one-shot training" — reporting feedback-on > feedback-off (LIBERO 88.5 vs 86.9, BridgeData V2 52.4 vs 47.3). But its evidence is a *single* feedback-on/off pass at the *scene/lifecycle* level (room reconstruction + a shared VLN+VLA backbone), not a *per-task object-grounded* twin run over *successive* re-grounding rounds — so the headline is conceded, the per-round monotone-improvement question is untouched.
- **The opening**: [[2504.03597|Real-is-Sim]] quantifies the exchange rate — 30 sim demos ≈ 30 real on PushT (57%→80%) — so a grounded twin's data has a measurable real-data value that *should* rise with twin fidelity (link to B1), and [[2605.00080|WM Robot Learning Survey]] frames exactly this: world models as "data amplification" and "learned environments for RL."

**First-principles framing.**
- **First principle**: A twin grounded in real reconstruction generates data from the *correct* distribution $p_{\text{sim}}(\cdot \mid \phi^\star, \psi^\star) \approx p_{\text{real}}$ — so its samples are training-valid, not just test-valid. Evaluation discards the twin's generative capacity; data generation uses it. [[2403.03949|RialTo]]'s 90%-vs-10% (target-twin vs generic) is the proof that only a *grounded* twin produces target-distribution training data.
- **Assumption being challenged**: *Not* "the closed loop beats one-shot" — [[2512.00076|Arcadia]] already claims and (qualitatively) shows that. The live assumption is that fold-back is *unconditionally* self-improving — that you can re-ground every round without a gate. Because each fold re-reconstructs from imperfect deployment data, an ungated loop can lower sim-real fidelity round-over-round and drift; [[2504.03597|Real-is-Sim]]'s continuous 60 Hz *correction* exists precisely because uncorrected twin error compounds. The conditional version — fold back *only when a B1 fidelity check passes* — is what no one has tested.
- **The bet**: A per-task object-grounded fold-back loop **gated on a B1 reconstruction-fidelity check** improves *monotonically across N rounds* on unseen-object generalization, where the same loop *ungated* drifts (a round-over-round SR trajectory that diverges) — and the per-round gain *scales with the reconstruction-fidelity exchange rate* ([[2504.03597|Real-is-Sim]] 30 sim ≈ 30 real rising with twin fidelity). Reproduce [[2403.03949|RialTo]]'s 90%-vs-10% grounding advantage and [[2605.26638|HyperSim]] 75%→95% per round. Falsifiable: if the *ungated* loop never drifts (gate redundant), or the exchange rate is flat in fidelity, the conditional-fold-back mechanism buys nothing over [[2512.00076|Arcadia]]'s one-pass result.

**Related research papers.** One comparison table on the axis the direction turns on — *how the twin is used* (data engine / co-training source / continuous-correction sandbox / generated-video twin / planning sandbox / distribution-alignment) — plus key result and what each leaves open:

| System | How the twin is used | Key result | What's missing |
|---|---|---|---|
| [[2403.03949\|RialTo]] | data engine: RL in twin + inverse distillation back | 91% pose-rand real; 90% (target twin) vs 10% (generic) | open-loop (no deployment-data fold-back) — the closed loop B3 proposes |
| [[2605.26638\|HyperSim]] | co-training source: synthetic + 35 real demos | 75%→95%, +35% first-attempt from adversarial twin data | one-shot co-train, not a closed loop folding deployment data back |
| [[2504.03597\|Real-is-Sim]] | continuous-correction sandbox; data-substitution evidence | 30 sim ≈ 30 real (57%→80%) | used as evaluator/corrector; the exchange-rate evidence the loop scales |
| [[2506.18088\|RoboTwin 2.0]] | twin data generator + 5-axis DR | +24.4% real few-shot, +21% zero-shot, 71.3% auto-codegen | twin data as augmentation, not a deployment-grounded closed loop |
| [[2511.07416\|PhysWorld]] | twin built from *generated* video → residual RL | 82% real | twin grounded in generated, not real, video — the synthesis-side variant |
| [[2509.24948\|RehearseVLA]] | world-model post-training + VLM reflector | 79.6% LIBERO from 5 demos, real 20%→30% | world-model-as-data-engine for VLA — learned model, not a reconstructed twin |
| [[2601.02078\|Genie Sim 3.0]] | LLM-driven sim + 3DGS-reconstruction *platform* as a data engine | 1,500 synthetic episodes beat real-data baselines zero-shot; R²=0.94 sim-real | synthetic-beats-real proof at platform scale (humanoid), but scenes are LLM-composed, not deployment-grounded per task — no real-fold-back loop |
| [[2606.12604\|EgoEngine]] | object-centric twin from *egocentric human video* as a data engine | synthetic-only training beats teleop (60% vs 25% Hammer); 83% TACO / 90% Aria | turns free human video into target-distribution training data, but open-loop per video — no deployment-grounded fold-back |
| [[2606.08828\|Video2Sim2Real]] | single-human-video twin → *decoupled* IL (geometry) + residual-RL (physics) data | 95.7% real avg over 7 tasks vs pure IL/RL 3–45.7% | full-stack single-video data engine, but per-video and open-loop — the closed re-grounding loop B3 proposes |
| [[2604.08544\|SIM1]] | grounded deformable data engine | synthetic-only +50%/+13%/+47% over real baselines at 27× lower cost | data-engine for deformables; no closed real-fold-back loop |
| [[2604.11386\|ComSim]] | DiT neural sim turns classical-sim videos into "pseudo-real" data | 10 real + 200 pseudo-real → 28/30 vs 17/30 from 20 real | classical+neural one engine, but not deployment-grounded co-training |
| [[2604.15805\|WorldComposer]] | "Digital Cousins" from one panorama for augmentation | 50 real + 1,000 sim → 85% real SR (r=0.91) | generative-cousins augmentation, not a single grounded closed loop |
| [[2509.18631\|Sim-Real OT Co-Training]] | distribution-alignment co-train (unbalanced optimal transport) | 0.73 image / 0.77 point-cloud real SR, unseen-texture | aligns the sim:real distribution but no twin-grounding or fold-back |
| [[2512.00076\|Arcadia]] | *closed lifecycle loop*: deployment feedback re-grounds scene assets + a shared VLN+VLA backbone | feedback-on > off (LIBERO 88.5 vs 86.9, BridgeData V2 52.4 vs 47.3) | the topThreat — states "removing any stage reverts to one-shot" but only a *single* feedback pass at *scene/lifecycle* level; no per-task object twin, no successive-round trajectory, no fidelity gate |
| [[2503.10118\|RSR Loop]] | closed loop tuning *sim parameters* (differentiable sim) per round | generalizable policy transfer via real-sim-real param tuning | re-grounds *parameters* not assets+policy, and no per-round monotone-improvement or fidelity-gate analysis |
| [[2510.20813\|GSWorld]] | reconstructed twin data engine + DAgger policy-only loop (*fixed* twin) | closed-loop photo-realistic sim suite, policy-only DAgger | the twin is fixed (un-re-grounded) — isolates the policy half of the loop, not asset re-grounding or drift |
| [[2602.12628\|RL-Co]] | *single-pass* RL-based sim-real co-training for VLA | RL co-train beats imitation-only sim-real co-train | one SFT-RL pass, not an iterated re-grounding loop — the one-shot baseline B3's rounds must beat |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a closed deployment-grounded co-training loop beats one-shot and pure-source training), with the experiment and the Related-table row it lands on.
1. **H1 — On a *per-task object* twin, fold-back beats one-shot over rounds (Arcadia only showed it at lifecycle scale, one pass).**
   - *Prediction*: at the per-task object-grounded twin scale (not [[2512.00076|Arcadia]]'s room+backbone lifecycle), folding deployment data back over *successive* rounds beats a one-shot [[2605.26638|HyperSim]]-style co-train and [[2602.12628|RL-Co]]'s single SFT-RL pass on unseen-object generalization, the gap widening each round — replicating Arcadia's feedback-on/off direction (88.5 vs 86.9) as a *trajectory* rather than a single delta.
   - *Test*: closed-loop vs one-shot over N rounds on a per-task object twin; report unseen-object SR per round.
   - *Row*: Arcadia (one-pass lifecycle) / HyperSim (one-shot co-train) vs RialTo (data engine).
   - *Falsifier*: the closed loop ties one-shot at per-task scale → fold-back's lifecycle result does not transfer to object twins and a single co-train suffices.
2. **H2 — Twin-data value scales with reconstruction fidelity (the exchange rate).**
   - *Prediction*: [[2504.03597|Real-is-Sim]]'s 30 sim ≈ 30 real exchange rate improves with twin fidelity (link to B1) — a higher-fidelity twin makes each sim demo worth more real demos.
   - *Test*: vary reconstruction fidelity; measure the sim:real exchange rate (sim demos to match N real).
   - *Row*: Real-is-Sim (exchange rate) / RialTo (data engine).
   - *Falsifier*: the exchange rate is flat in fidelity → twin data value is independent of grounding and B1's fidelity is irrelevant here.
3. **H3 — Grounding, not quantity, drives the target-twin advantage.**
   - *Prediction*: replicating [[2403.03949|RialTo]]'s 90%-vs-10% across object classes, *grounding* the twin in real reconstruction (not the *amount* of twin data) is what carries the advantage — generic-asset data at any volume stays near 10%.
   - *Test*: vary {grounded vs generic twin} × {twin-data volume}; report which main-effect carries SR.
   - *Row*: RialTo (data engine).
   - *Falsifier*: enough generic-asset data closes the gap → quantity substitutes for grounding and the twin need not be target-specific.
4. **H4 — Co-training balance is a tunable, not a fixed ratio.**
   - *Prediction*: there is a sim:real ratio that maximizes unseen-object SR, and too much twin data swamps the few real demos — the optimum tracks [[2504.03597|Real-is-Sim]]'s ~1:1 and [[2605.26638|HyperSim]]'s 35-demo regime.
   - *Test*: sweep the sim:real ratio; report unseen-object SR vs ratio.
   - *Row*: Real-is-Sim (1:1) / HyperSim (35-demo).
   - *Falsifier*: SR is flat in the ratio → balance is not delicate and any mix works.
5. **H5 — Closed-loop drift is gated by a fidelity check.**
   - *Prediction*: folding deployment data back can amplify reconstruction errors over rounds, but gating each fold on a B1 reconstruction-fidelity check (reject folds that lower sim-real r) keeps the loop monotone-improving rather than drifting.
   - *Test*: run the closed loop with vs without a per-fold fidelity gate; report SR trajectory and drift over rounds.
   - *Row*: RialTo (data engine) / Real-is-Sim (correction).
   - *Falsifier*: the ungated loop never drifts → the fidelity gate is unnecessary and closed-loop is unconditionally safe.

> [!warning] Risks
> - **Closed-loop can drift** — folding deployment data back may amplify reconstruction errors over rounds. → Gate each fold on a B1 reconstruction-fidelity check (H5); reject folds that lower sim-real r.
> - **Co-training balance is delicate** — too much twin data swamps the few real demos. → Tune the sim:real ratio per [[2504.03597|Real-is-Sim]]'s 1:1 finding and [[2605.26638|HyperSim]]'s 35-demo regime (H4); treat the ratio as a hyperparameter.
> - **Grounding cost per object** — every new object needs reconstruction before it can be a data source. → Amortize via B2's differentiable sysID + generative reconstruction priors; reuse twins across tasks.

### B4 — Generalizable Constitutive-Law Inversion: Learning the Physics, Not Just the Parameters

| | |
|---|---|
| **Cluster** | B — Real-to-Sim-to-Real |
| **Thesis** | B2 recovers the *parameters* of a constitutive law the engineer chose; learning the functional *form* from video is now also done — material-agnostic neural constitutive sysID exists. But every such result is shown for *recovery generalization* (more materials, longer sequences), not for the two things that would make a learned law matter for robotics: that it extrapolates to *unseen geometry* a parameter fit cannot, and that it survives a *closed robot real→sim→real loop*. The first principle: the constitutive form, not its parameters, is the binding constraint on geometry extrapolation. The field assumes learning the form from video is itself the contribution. The bet is in First-principles below. |
| **Anchor papers** | [[2304.14369\|NCLaw]] (method), [[2505.16971\|UniPhy]] (method), [[2503.17973\|PhysTwin]] (method), [[2604.27367\|DOT-Sim]] (method), [[2511.04665\|Real-to-Sim GS]] (method), [[2604.04974\|Video-to-Control Survey]] (survey) |
| **Key targets** | Match [[2304.14369\|NCLaw]]'s reconstruction loss <1e-3 + generalization to unseen geometries up to 1M particles from real 2D video; beat parameter-only sysID ([[2604.27367\|DOT-Sim]], [[2503.17973\|PhysTwin]]) on held-out material/geometry; supply a generalizable dynamics model to [[2511.04665\|Real-to-Sim GS]]'s r=0.915 joint-inversion loop |

**Why it matters.**
- **The gap**: B2 recovers the *parameters* of a law the engineer picked — Young's modulus and Poisson's ratio for a neo-Hookean solid ([[2604.27367|DOT-Sim]]), stiffness and friction for a spring-mass deformable ([[2503.17973|PhysTwin]]) — which works when the chosen law matches the material but caps generalization at the functional form.
- **Today's answers**: [[2304.14369|NCLaw]] shows the move — embed a *neural* constitutive law inside a differentiable Material Point Method simulator, let the simulator enforce conservation (momentum, mass) structurally, and have the network learn only the material-specific stress-strain map under physics-aware priors (rotation equivariance, undeformed-state equilibrium); it generalizes by *orders of magnitude* over data-driven baselines, real 2D dough video, loss <1e-3. [[2508.01112|MASIV]] makes the *learn-the-form-from-video* half consensus — the first material-agnostic neural-constitutive sysID, learning both elasticity and plasticity from video with *no* material prior, explicitly inspired by NCLaw — so "learn the functional form" is no longer the open frontier the card once treated it as.
- **The opening**: NCLaw's generalization to unseen boundary conditions, geometries up to 1M particles, longer horizons, and multi-physics — from a *learned law* not a parameter fit — is the existence proof that the functional form, not its parameters, is the binding constraint. But [[2508.01112|MASIV]]'s generalization is across material *types* and added training sequences of the same object, *not* the unseen-geometry-to-1M-particles extrapolation, and like NCLaw/[[2505.16971|UniPhy]] it has no robot sim2real loop. So the two unattacked deltas remain: (1) isolating the learned-law-vs-parameter-fit advantage *on held-out geometry* (H1), which MASIV never does, and (2) the closed robot loop (H2/H3) — where the robot-side dynamics-learning work ([[2407.07889|AdaptiGraph]], [[2601.17251|EMPM]], [[2506.15680|Particle-Grid Neural Dynamics]], [[2512.13214|Differentiable MPM Control]]) all sit on black-box dynamics or parameter-fit axes, *not* a learned constitutive law in the loop.

**First-principles framing.**
- **First principle**: The cause of a material's motion is its constitutive law — the stress-strain map — not the scalars of any one parameterization. Conservation laws are universal and belong in the simulator; the constitutive law is material-specific, the only degree of freedom that varies across materials, so it is what must be *learned*. [[2304.14369|NCLaw]]'s orders-of-magnitude generalization from a learned law is the evidence that the functional form is the binding constraint on extrapolation, not the parameter values.
- **Assumption being challenged**: *Not* "learn the functional form from video" — [[2508.01112|MASIV]], [[2511.06299|Physics-Informed Deformable GS]], [[2406.04155|Lagrangian Particle Optimization]] and [[2505.16971|UniPhy]] already do that. The live assumption is that learning the form is *itself* the contribution, so a learned-law paper stops at recovery generalization (more materials, longer sequences). That leaves untested whether the learned form actually beats a parameter fit *on unseen geometry* (the form's whole claimed advantage) and whether it survives a *robot* loop — the two deltas MASIV's material-agnostic recovery does not touch.
- **The bet**: A learned constitutive law beats a parameter-only fit (e.g. [[2503.17973|PhysTwin]]) **on held-out geometry up to 1M particles** — reproducing [[2304.14369|NCLaw]]'s order-of-magnitude extrapolation advantage and <1e-3 loss — *and* survives a **closed robot real→sim→real loop**: dropped into [[2511.04665|Real-to-Sim GS]]'s pipeline in place of the fixed soft-body model, it holds forward correlation across material variation a single parameter fit cannot cover (the missing proof neither NCLaw nor MASIV supplies). Falsifiable: if parameter-only sysID matches the learned law on held-out geometry, the functional form is not the binding constraint and MASIV-style recovery generalization is the whole story.

**Related research papers.** One comparison table on the axis the direction turns on — *what is recovered* (the law itself / parameters of a chosen law / parameters jointly with appearance / fixed rigid physics) — plus key result and what each leaves open:

| System | What is recovered | Key result | What's missing |
|---|---|---|---|
| [[2304.14369\|NCLaw]] | the constitutive *law* (neural stress-strain in differentiable MPM) | <1e-3 loss, generalizes to 1M particles / unseen geometry / multi-physics, real dough video | demonstrated for *recovery* generalization, not a closed sim2real loop on a robot |
| [[2505.16971\|UniPhy]] | a *unified* neural law (latent-conditioned MPM functions, frozen; per-scene latent inferred) | elastic reconstruction 5.2e-6 vs [[2304.14369\|NCLaw]] 2.4e-4; generalizes to unseen geometry / velocity / horizon | one law spanning *all* materials via a latent, no preset material type — beats [[2304.14369\|NCLaw]] on recovery but still no robot sim2real loop |
| [[2508.01112\|MASIV]] | the constitutive *law*, *material-agnostic* (elasticity + plasticity, no prior, from video) | first material-agnostic neural-constitutive sysID, inspired by [[2304.14369\|NCLaw]] | the topThreat — makes "learn the form from video" consensus, but generalizes across material *types* not unseen *geometry*, and no robot loop |
| [[2511.06299\|Physics-Informed Deformable GS]] | a *unified* constitutive law over a time-evolving Gaussian material field | physics-informed deformable GS, unified constitutive laws | learned-law-from-video for deformable GS — recovery generalization, no unseen-geometry isolation, no robot loop |
| [[2406.04155\|Lagrangian Particle Optimization]] | *geometry-agnostic* continuum sysID (physics-augmented NeRF + particle optimization) | improves geometry-agnostic physics-from-video sysID | confirms geometry-agnostic recovery is solved — but recovery, not the learned-law-vs-parameter-fit extrapolation test |
| [[2407.07889\|AdaptiGraph]] | a *black-box* learned graph dynamics model (no constitutive law) | material-adaptive graph dynamics for manipulation | robot-side dynamics learning, but black-box GNN not a constitutive law — the robot-loop contrast on the wrong axis |
| [[2506.15680\|Particle-Grid Neural Dynamics]] | a learned *particle-grid* neural dynamics model (data-driven) | learns deformable dynamics for manipulation | learned dynamics in a robot loop, but not a conservation-structured constitutive law — black-box, caps extrapolation |
| [[2601.17251\|EMPM]] | learned *elastoplastic* MPM dynamics for manipulation | elastoplastic dynamics model for robot deformable manipulation | closer to MPM but parameter/dynamics-fit, not a learned constitutive *form* generalizing across geometry |
| [[2512.13214\|Differentiable MPM Control]] | differentiable MPM for *control* (fixed/parameterized law) | differentiable-MPM control of deformables | uses differentiable MPM in the loop but with a fixed law — the robot-loop slot B4's learned law would fill |
| [[2503.17973\|PhysTwin]] | *parameters* of a chosen spring-mass law from video | generalizes to unseen interactions | the parameter-only baseline B4 generalizes past — caps at the functional form |
| [[2604.27367\|DOT-Sim]] | *parameters* (Young's modulus, Poisson's ratio) of a fixed form | 96.55% zero-shot, 1.71 mm Chamfer | fixed form, point-parameter recovery — the per-object fit B4 replaces |
| [[2511.04665\|Real-to-Sim GS]] | *parameters* of a soft-body law jointly with 3DGS appearance | r=0.915 | the joint-inversion loop a learned law would slot into (B1) |
| [[2510.11689\|Phys2Real]] | *priors* over a fixed law (VLM-inferred) + online estimation | 57% vs 23% OOD | priors over a fixed law, not a learned functional form |
| [[2404.09833\|Video2Game]] | fixed rigid physics + NeRF/mesh appearance | 100+ FPS browser | fixed rigid physics — the contrast for learned-deformable-law generalization |
| [[2604.04974\|Video-to-Control Survey]] | — (names physical-consistency + latent-identifiability gaps) | survey | the integration-layer gaps a learned-law inversion fills |
| [[2605.00080\|WM Robot Learning Survey]] | — (world models as learned simulators needing physical consistency) | survey | the rationale for learning the law, not just parameters |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (the learned law, not its parameters, is the extrapolation lever), with the experiment and the Related-table row it lands on.
1. **H1 (front line) — Learned-law extrapolation beats parameter-fit on held-out geometry — the delta MASIV never isolates.**
   - *Prediction*: fitting a [[2503.17973|PhysTwin]]-style chosen-law recovery and an [[2304.14369|NCLaw]]/[[2508.01112|MASIV]]-style neural law to the *same* real video, the learned law's extrapolation to *unseen* geometries reproduces the order-of-magnitude advantage while the parameter fit degrades — the geometry-extrapolation comparison MASIV's material-type generalization does not run.
   - *Test*: both fit on identical data; test on held-out geometries up to 1M particles; report extrapolation error for {learned law} vs {parameter fit}.
   - *Row*: NCLaw (the law) / MASIV (material-agnostic recovery) vs PhysTwin (parameters of a chosen law).
   - *Falsifier*: parameter-only sysID matches the learned law on held-out geometry → the functional form is not the binding constraint and MASIV-style recovery generalization is the whole story.
2. **H2 — A learned law survives the full real→sim→real loop (the missing proof).**
   - *Prediction*: dropping an [[2304.14369|NCLaw]]-recovered law into [[2511.04665|Real-to-Sim GS]]'s pipeline in place of the fixed soft-body model holds forward correlation across material variation a single parameter fit cannot cover — supplying the closed-loop evidence NCLaw alone lacks.
   - *Test*: swap the learned law into the joint-inversion loop; report forward r across materials vs the fixed-law baseline.
   - *Row*: NCLaw (the law) / Real-to-Sim GS (joint inversion).
   - *Falsifier*: the learned law does not preserve forward correlation across materials → recovery-generalization does not transfer to a sim2real loop.
3. **H3 — Real-video-only law recovery works for manipulation deformables.**
   - *Prediction*: [[2304.14369|NCLaw]]'s recovery runs on cloth, cable, or food from a single RGB-D interaction, supplying B3's co-training engine a transferable dynamics model per material class.
   - *Test*: recover laws for cloth/cable/food from single interactions; report reconstruction loss and downstream co-training value.
   - *Row*: NCLaw (the law).
   - *Falsifier*: single-view recovery is under-constrained for manipulation deformables → multi-view/RGB-D is required and the cheap-recovery claim narrows.
4. **H4 — Structural priors are load-bearing for off-distribution physicality.**
   - *Prediction*: keeping [[2304.14369|NCLaw]]'s rotation-equivariance + undeformed-equilibrium priors as hard constraints is what keeps the learned law physical off-distribution — dropping them yields non-physical extrapolation despite low reconstruction loss.
   - *Test*: ablate the structural priors; gate on conservation-law residuals, not just reconstruction loss; report off-distribution physicality.
   - *Row*: NCLaw (the law).
   - *Falsifier*: the law stays physical without the priors → the inductive biases are decorative.
5. **H5 — The learned law degrades gracefully to a parameter fit when unidentifiable.**
   - *Prediction*: where the material is in-distribution for a known law, the learned law matches the parameter fit (no over-flexibility cost), and only on novel materials does it pull ahead — so the learned law dominates without a downside.
   - *Test*: compare learned-law vs parameter-fit on in-distribution materials; report any over-flexibility penalty.
   - *Row*: NCLaw (the law) vs DOT-Sim (fixed-form fit).
   - *Falsifier*: the learned law underperforms the parameter fit on in-distribution materials → flexibility costs accuracy where the law is known.

> [!warning] Risks
> - **Recovery is solved; the robot loop is not** — the learn-the-law case now has multiple recovery existence proofs ([[2304.14369|NCLaw]], [[2508.01112|MASIV]], [[2505.16971|UniPhy]], [[2511.06299|Physics-Informed Deformable GS]]), all demonstrating *generalizable law recovery from video* but none a closed sim2real loop on a robot. The remaining novelty is *not* "learn the form" (consensus) but the geometry-extrapolation delta (H1) and the missing robot loop (H2) — the most speculative slice in Cluster B (consistent with A2's "no existence proof yet" hedge). → Treat 1M-particle generalization as transfer-of-recovery evidence, not sim2real-loop evidence; H2 (learned law into [[2511.04665|Real-to-Sim GS]]'s loop) is the go/no-go that supplies the missing proof.
> - **Learned laws can violate physics off-distribution** despite priors — a neural stress-strain map may extrapolate non-physically. → Keep [[2304.14369|NCLaw]]'s structural priors as hard constraints and gate on conservation-law residuals (H4), not just reconstruction loss.
> - **Differentiable MPM is mature for soft bodies, not rich contact** — the learn-the-law regime is deformables. → Scope the 1M-particle generalization bet to elastoplastic/fluid materials where MPM differentiability holds; treat rigid-contact laws as a separate, harder problem.
> - **Real-video-only recovery is under-constrained** — a single 2D view may not identify the full law. → Use multi-view or RGB-D interaction (H3) and report identification variance; fall back to B2's parameter fit when the learned law is unidentifiable (H5).

---

## Cluster C — Reality-Gap Measurement as Statistical Inference

*Stop asking "is the sim accurate?" Ask "what can I provably infer about real performance from imperfect, possibly-adversarial sims?" — treating a correlation number as a validity claim and a portfolio of biased sims as a variance-reduction estimator.*

### C1 — Per-Factor Correlation Validity as a Deployment Gate: Stress-Test, Then Route

| | |
|---|---|
| **Cluster** | C — Reality-Gap Measurement as Inference |
| **Thesis** | That a sim-real correlation holds only on its measured conditions is now consensus — controlled per-factor variation against real is already run, and the statistics literature treats the gap as a *distribution*, not a scalar. What no one does is re-measure the *correlation itself* per perturbation factor and turn that per-(sim, factor) trust map into a deployment *router* that picks which biased sim to trust under each shift. The first principle: trustworthiness is factor-resolved, so a per-factor validity map can route deployment where one global r cannot. The field measures per-factor *success drops* but never re-measures per-factor *correlation*, nor routes on it. The bet is in First-principles below. |
| **Anchor papers** | [[2402.08191\|THE COLOSSEUM]] (benchmark), [[2405.05941\|SIMPLER]] (benchmark), [[2604.24018\|Sim2Real Betting]] (benchmark), [[2502.10694\|UDA Simulation Study]] (survey), [[2512.19562\|REALM]] (benchmark) |
| **Key targets** | Diagnose current high-r sims ([[2405.05941\|SIMPLER]] r≥0.85, [[2605.06311\|VISER]] r=0.92, [[2604.21686\|WorldMark]] ρ>0.9) as falling below r<0.7 under deliberate OOD shift over [[2402.08191\|THE COLOSSEUM]]'s 14 factors (30–50% single-perturbation SR drop, R̄²=0.614); route [[2604.24018\|Sim2Real Betting]]'s biased-bank weights per factor to beat its 70–100% single-global-edge win rate; halve the real-trial spend [[2510.04354\|SureSim]] needs (20–25%) by trusting only validated-per-factor sims |

**Why it matters.**
- **The gap**: two questions share one mechanism. First — is a benchmark's high r a real property of the sim or an artifact of the nominal conditions it was measured on? Second — once you have a per-factor table, can you *act* on it, routing which sim to trust per shift rather than deploying with one global scalar?
- **Today's answers**: [[2405.05941|SIMPLER]] reports r≥0.85/0.890, [[2605.06311|VISER]] r=0.92, [[2604.21686|WorldMark]] ρ>0.9 — every one an *in-distribution* correlation; [[2402.08191|THE COLOSSEUM]] shows single perturbations cause 30–50% SR drops (R̄²=0.614), *differently per factor*. But the diagnosis half is now partly run: [[2602.11337|MolmoSpaces]] does one-factor-at-a-time controlled variation against 752 real tasks and reports a *high* global correlation (R=0.96) with per-factor SR sensitivities — landing on the falsifier side of "does r survive shift" — and [[2512.05024|Simulator Fidelity Quantile Curves]] and [[1912.06321|Sim2Real Predictivity]] make the "gap is a distribution / correlation is a fragile measured property" point rigorous.
- **The opening**: nobody re-measures the *correlation* per factor (MolmoSpaces reports per-factor SR sensitivities, not per-factor r) and nobody turns the result into a *router*; [[2512.19562|REALM]]'s per-perturbation real-to-sim validation supplies pre-validated rows the gate can ingest, so the per-(sim, factor) routing gate — the unattacked half — is buildable from existing data.

**First-principles framing.**
- **First principle**: A sim-real correlation number only vouches for the sim under the exact conditions it was measured on; whether it holds out-of-distribution is a *different* number you have to measure, not assume. And a sim's trustworthiness is one number *per perturbation factor* — different physics shortcuts break under different shifts, so checking each factor separately catches structure one overall score hides. [[2402.08191|THE COLOSSEUM]]'s 30–50% spread across factors (R̄²=0.614) is the direct evidence that the per-factor detail decides which sim to deploy.
- **Assumption being challenged**: *Not* "one in-distribution r proves the sim usable" — that the validity is conditional is conceded ([[2602.11337|MolmoSpaces]] runs controlled per-factor variation; [[1912.06321|Sim2Real Predictivity]] showed correlation is fragile/tuning-dependent in 2019; [[2512.05024|Simulator Fidelity Quantile Curves]] formalizes the gap as a distribution). The live assumption is that the per-factor diagnosis ends at *success-drop sensitivities* and a *global* edge — that nobody re-measures the *correlation* per factor or *routes* on it. The portfolio work ([[2604.24018|Sim2Real Betting]]) still weights sims by one aggregate edge; VSDR routes *policies*, not sims-per-factor.
- **The bet**: A per-(sim, factor) trust map — the *correlation* re-measured under each [[2402.08191|THE COLOSSEUM]] factor, ingesting [[2512.19562|REALM]]'s validated rows — used as a deployment *router* lifts [[2604.24018|Sim2Real Betting]]'s **70–100% win rate** over its single-global-edge baseline on shift-mixed deployment, and recovers [[2510.04354|SureSim]]'s **20–25%** real-trial reduction by skipping do-not-trust cells, with the gain largest on the factors where r collapses hardest. Falsifiable: if per-factor routing ties the single global edge (and [[2602.11337|MolmoSpaces]]'s R=0.96 robustness holds per factor so there is nothing to route around), the per-factor detail is not deployment-relevant.

**Related research papers.** One comparison table on the axis the direction turns on — *how the sim's trustworthiness is characterized* (single in-distribution r / per-factor SR drop / per-factor validated / proxy-disagreement / cross-sim failure discovery / portfolio router) — plus key result and what each leaves open:

| System | How trustworthiness is characterized | Key result | What's missing |
|---|---|---|---|
| [[2402.08191\|THE COLOSSEUM]] | per-factor SR drop across 14 axes | 30–50% single / ≥75% combined, R̄²=0.614 | the OOD shift harness + factor decomposition — but never re-measures *correlation* per factor |
| [[2405.05941\|SIMPLER]] | single in-distribution r + MMRV | r>0.85 / 0.890, low MMRV | one in-distribution scalar tuned via sysID — the number whose validity is stress-tested |
| [[2605.06311\|VISER]] | single in-distribution r, self-flags OOD | r=0.92, "drops drastically" under distractors | shows the in/OOD split exists but reports one global r, not a per-factor gate |
| [[2604.24018\|Sim2Real Betting]] | aggregate predictive edge over a biased bank | 70–100% win with a *single* aggregate edge | the portfolio router the gate weights per factor — currently one global edge |
| [[2502.10694\|UDA Simulation Study]] | context-dependent effectiveness + negative adaptation | shift can *invert* a relationship | warns validity is per-axis but supplies no per-factor map |
| [[2512.19562\|REALM]] | per-perturbation real-to-sim validation (15 factors) | r=0.92 overall / 0.88 default | pre-validated per-factor rows the gate ingests — not yet a routing mechanism |
| [[2604.21686\|WorldMark]] | proxy disagreement vs human judgment | ρ>0.9, control-alignment ≠ visual-quality leaders | proxies disagree, so the deploy decision is multi-dimensional — but no gate |
| [[2603.22126\|ROBOGATE]] | cross-simulator boundary failure discovery | LIBERO 97.65% → 0/68 Isaac Sim industrial (97.65 pp gap), AUC 0.780 | sharpest proof one benchmark's r doesn't transfer across sims — diagnosis, not routing |
| [[2606.10366\|Sim-Real VLA Eval]] | ranking correlation re-measured under 4 *perturbation types*, across 3 sims | [[2512.19562\|REALM]] alone preserves severity hierarchy (ρ=0.700→0.875 w/ post-train); 10-demo data optimum | ranks *which sim* survives perturbation (the per-factor diagnosis C1 needs), but does not turn the result into a per-(sim,factor) routing gate |
| [[2510.23571\|RobotArena Infinity]] | real-to-sim-translated eval, perturbed along background/color/pose | 6 VLAs drop sharply under OOD shift; VLM scores align with 8,500+ human judgments | a scalable per-factor OOD harness (real-to-sim), but reports per-policy drops, not a re-measured *correlation* gate per factor |
| [[2501.16389\|Sim2Real Encoder Eval]] | offline per-component transfer diagnostic | manipulation-pretrained encoders top Domain-Invariance + Action scores | predicts transfer before training, per-component — a validity check, not a deployment gate |
| [[2512.16881\|PolaRiS]] | high-r evaluator from real-video scans | r=0.9 avg / 0.98 best, <20 min/scene | a high-r evaluator the gate must still stress-test per factor |
| [[2602.11337\|MolmoSpaces]] | one-factor-at-a-time controlled variation vs 752 real tasks (per-factor SR sensitivity) | R=0.96 global correlation, per-factor SR sensitivities | the strongest pre-run of H1, but lands on the *falsifier* side (r robust) and reports per-factor *SR*, never per-factor *correlation* or a router |
| [[1912.06321\|Sim2Real Predictivity]] | sim-real correlation as a predictivity property (the lineage root, 2019) | shows correlation is fragile and tuning-dependent | the root that makes "correlation is a fragile measured property" consensus — diagnosis, not a per-factor gate |
| [[2512.05024\|Simulator Fidelity Quantile Curves]] | the sim-real gap as a *distribution* (quantile curves), model-free | model-free fidelity via quantile curves | makes the first-principle rigorous (gap is a distribution, not a scalar) but LLM-survey domain, no robotics routing gate |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (per-factor validity stress-test + routing gate beats one global r), with the experiment and the Related-table row it lands on.
1. **H1 (diagnosis, MolmoSpaces frames the null) — Per-factor *correlation* falls below r<0.7 for the worst factors, even where global r is high.**
   - *Prediction*: re-measuring the *correlation* (not just SR sensitivity) under each [[2402.08191|THE COLOSSEUM]] factor applied to *both* sim and real, at least the worst factors (distractors, color, lighting) drop below 0.7 — i.e. [[2602.11337|MolmoSpaces]]'s high *global* R=0.96 masks per-factor collapse that only a per-factor *correlation* re-measurement exposes.
   - *Test*: per-factor paired sim+real correlation re-measurement; report the per-factor r table and contrast it with MolmoSpaces's per-factor SR sensitivities.
   - *Row*: MolmoSpaces (high global R, per-factor SR) / SIMPLER (in-distribution r) / THE COLOSSEUM (per-factor harness).
   - *Falsifier*: per-factor *correlation* stays >0.7 under every factor (MolmoSpaces's robustness holds at the correlation level) → there is nothing to route around and the gate's input is empty (still publishable as a null).
2. **H2 — A per-(sim, factor) routing gate beats single-global-edge selection.**
   - *Prediction*: populating a trust map from H1 + [[2512.19562|REALM]]'s validated rows and routing each deployment query (task, factor) → trusted sim(s) lifts [[2604.24018|Sim2Real Betting]]'s win rate over its single-aggregate-edge baseline on shift-mixed deployment.
   - *Test*: feed per-factor weights vs one aggregate edge to the betting estimator; report win rate on multi-shift deployments.
   - *Row*: Sim2Real Betting (aggregate edge) / REALM (validated rows).
   - *Falsifier*: per-factor routing ties the global edge → the per-factor detail is not deployment-relevant.
3. **H3 — Under some perturbation, sim r goes *negative* (ranks policies backward).**
   - *Prediction*: following [[2502.10694|UDA Simulation Study]]'s negative-adaptation warning, there is at least one [[2402.08191|THE COLOSSEUM]] factor under which a high-r sim's correlation goes negative — the sim ranks policies *backward*, the strongest case for the gate.
   - *Test*: scan all 14 factors for sign-flips in the re-measured correlation.
   - *Row*: UDA Simulation Study (negative adaptation) / THE COLOSSEUM (factors).
   - *Falsifier*: r never goes negative → the failure is only degradation, not inversion, and routing matters less.
4. **H4 — Cross-sim transfer of r is the failure ROBOGATE already shows, generalized.**
   - *Prediction*: [[2603.22126|ROBOGATE]]'s 97.65 pp LIBERO→Isaac-Sim gap is not an outlier — re-measuring any sim's r on a *different* simulator's task distribution drops it sharply, so the gate must be per-(sim, factor, target-sim), not per-sim.
   - *Test*: measure r-transfer across simulator pairs; report the cross-sim r drop distribution.
   - *Row*: ROBOGATE (cross-sim failure) / PolaRiS (high-r evaluator).
   - *Falsifier*: r transfers across sims → cross-sim is not a separate axis and per-sim gating suffices.
5. **H5 — The gate halves real-trial spend by trusting only validated-per-factor sims.**
   - *Prediction*: routing real trials only to sim-factor cells the stress-test validated (and skipping do-not-trust cells) recovers [[2510.04354|SureSim]]'s 20–25% real-trial reduction *on top of* the portfolio, because untrusted-cell trials are wasted.
   - *Test*: compare real-trial budget for {gate-routed} vs {uniform} at matched CI coverage.
   - *Row*: REALM (validated rows) / Sim2Real Betting (router).
   - *Falsifier*: gating doesn't cut real-trial spend → untrusted-cell trials were not wasted and the gate adds no efficiency.

> [!warning] Risks
> - **Stress-test and gate both need paired sim+real OOD data** — combinatorially expensive per (sim, factor). → Reuse [[2512.19562|REALM]]'s 15-perturbation real-to-sim-validated pairs and [[2510.17950|RoboChallenge]]'s real fleet; populate the gate incrementally on [[2509.15273|Embodied Arena]] rather than collecting fresh.
> - **A null result (r survives shift) is still informative** — but reframes the diagnosis half. → Pre-register the r<0.7 bet (H1); if r holds, "high-r sims are robust to shift X" is itself publishable, and the gate routes on the validated-robust cells.
> - **Routing on a stale gate mis-deploys the portfolio** — sims and factors drift, so a once-trusted cell can go bad. → Tie gate refresh to [[2509.15273|Embodied Arena]]'s evolving-eval cadence; expire trust cells past a staleness window before they route a deployment.

### C2 — Sim-to-Real as Provable Statistical Inference: Banks of Biased Simulators

| | |
|---|---|
| **Cluster** | C — Reality-Gap Measurement as Inference |
| **Thesis** | That a portfolio of cheap biased sims beats one accurate sim — on provable confidence intervals and fewer real trials — is no longer the contrarian inversion: control-variates over biased auxiliary sources, with a provable variance bound and the fewer-real-samples result, is already published on robotics. What no one has characterized is *what makes the bank informative* — whether bias *diversity* tightens the bound more than bias *count*, and where on the compute-budget curve the portfolio wins. The field treats the portfolio result as the contribution. The bet is in First-principles below. |
| **Anchor papers** | [[2604.24018\|Sim2Real Betting]] (benchmark), [[2510.04354\|SureSim]] (benchmark), [[2509.15273\|Embodied Arena]] (benchmark), [[2502.10694\|UDA Simulation Study]] (survey), [[2510.17950\|RoboChallenge]] (benchmark) |
| **Key targets** | [[2604.24018\|Sim2Real Betting]] 70–100% win rate over Monte Carlo from a *bank* of biased sims; [[2510.04354\|SureSim]] 20–25% real-trial reduction + 14.4% CI tightening (700 sims); finite-sample-valid CI coverage at equal compute vs a single accurate sim |

**Why it matters.**
- **The gap**: real-performance estimation is variance reduction, and a bank of cheap biased sims beating a single accurate one is no longer the open question — it is published. The open question is *bank composition*: which property of the bank (diversity vs count) tightens the bound, and when the portfolio is worth it.
- **Today's answers**: [[2506.20553|Sim2Val]] (NVIDIA/Pavone) does control-variates over cheap abundant *biased* sources for variance-reduced *real-world* metric estimation, with a *provable variance bound* and the "significantly fewer real samples for a confidence bound" outcome, validated on quadruped robotics — exactly C2's headline; [[2507.20068|PERRY]] uses doubly-robust prediction-powered inference for valid CIs from biased simulator data; [[2604.24018|Sim2Real Betting]] (70–100% win over Monte Carlo) and [[2510.04354|SureSim]] (20–25% fewer real trials, 14.4% CI tightening) are the betting/PPI instances; [[2206.05165|MFMCRL]]'s multifidelity control variates is the 2022 machinery predating all of them.
- **The opening**: *none* of these characterizes the bank — [[2502.10694|UDA Simulation Study]] only says no single method is universally best (so a bias is a signal to *weight*); whether bias *diversity* beats bias *count* and where the compute crossover sits are untouched, and C1's per-factor trust map is the natural selector for *informative* bias.

**First-principles framing.**
- **First principle**: Estimating real performance is a statistics problem on a small number of real trials — what matters is how much the estimate jitters and whether its confidence interval is trustworthy, not how accurate any single sim is on its own. A biased sim is fine to use, as long as the bias carries useful signal and you correct for it. [[2604.24018|Sim2Real Betting]]'s 70–100% win from a *bank* of biased sims is the direct evidence that averaging-to-reduce-jitter beats squeezing-accuracy-from-one.
- **Assumption being challenged**: *Not* "the goal is one high-fidelity sim" — the statistical-inference camp ([[2506.20553|Sim2Val]], [[2507.20068|PERRY]], [[2510.04354|SureSim]], [[2604.24018|Sim2Real Betting]], [[2206.05165|MFMCRL]]) already won that argument. The live assumption is that the portfolio *result* is the contribution, so nobody asks what *property of the bank* drives the bound. The unattacked claim: bias *diversity* (different physics approximations), not bias *count*, is the lever, and there is a compute crossover below which one accurate sim still wins.
- **The bet**: (i) Diversifying simulator bias tightens [[2510.04354|SureSim]]'s PPI bound / widens [[2506.20553|Sim2Val]]'s variance reduction **more than adding copies of the same biased sim** at matched bank size — a measurable CI-width gap Δ from diversity at fixed count. (ii) There is a compute-budget **crossover** below which one accurate sim gives tighter CIs and above which the biased portfolio wins, which the experiment maps. Reproduce [[2604.24018|Sim2Real Betting]]'s **70–100% win** and [[2506.20553|Sim2Val]]'s fewer-real-samples result *only as the regime where diversity is present*. Falsifiable: if redundant copies tighten the bound as much as diverse bias (no Δ), or the portfolio wins/loses at every budget (no crossover), bank composition is not the lever.

**Related research papers.** One comparison table on the axis the direction turns on — *how real performance is estimated* (portfolio of biased sims / PPI from imperfect sims / single high-fidelity / cross-sim TTA / multi-source platform / real-sample source) — plus key result and what each leaves open:

| System | How real performance is estimated | Key result | What's missing |
|---|---|---|---|
| [[2604.24018\|Sim2Real Betting]] | sequential betting over a *biased-sim bank* (Cover/Kelly) | 70–100% win over Monte Carlo, tolerates bias w/ edge | the portfolio-estimator anchor — provable-CI characterization vs single-sim at equal compute is open |
| [[2510.04354\|SureSim]] | PPI + Waudby-Smith-Ramdas, finite-sample-valid CIs | 20–25% fewer real trials, 14.4% CI tightening (700 sims) | provable bounds from imperfect sims — bias-diversity vs count trade-off unmapped |
| [[2506.20553\|Sim2Val]] | *control variates* over cheap biased auxiliary sources, provable variance bound | variance-reduced real metric estimation, fewer real samples for a confidence bound (quadruped) | the topThreat — does C2's headline (biased portfolio, provable bound, fewer real trials) on robotics, but never sweeps bias-diversity vs count or maps the compute crossover |
| [[2507.20068\|PERRY]] | doubly-robust prediction-powered inference from biased auxiliary data | valid CIs from biased simulator data | DR-PPI confidence intervals from biased sims — confirms the headline, leaves bank composition unexamined |
| [[2206.05165\|MFMCRL]] | *multifidelity* RL with control variates (the 2022 machinery root) | variance reduction via multifidelity control variates | predates Sim2Val/SureSim — proves the estimator class, but RL-internal, no bank-composition or crossover map |
| [[2502.10694\|UDA Simulation Study]] | (no method) names no universally-best estimator | context-dependent effectiveness | the rationale for portfolios over single estimators |
| [[2604.10856\|BridgeSim]] | cross-simulator CL evaluation + TTA | +19.1 DS | multi-sim evaluation infrastructure, not a provable-CI estimator |
| [[2509.15273\|Embodied Arena]] | unified evolving multi-benchmark eval | 22+ benchmarks / 30+ models | the multi-source substrate a portfolio extends, not an estimator |
| [[2510.17950\|RoboChallenge]] | real fleet (10 robots, Table30) | 30 tasks, contact/soft-body splits | the scarce real-sample source PPI/betting pair with |
| [[2605.00080\|WM Robot Learning Survey]] | (no method) world models as evaluators | survey | the inference-over-fidelity rationale |
| [[2512.19562\|REALM]] | real-to-sim-validated paired real/sim outcomes | r=0.92 overall | supplies the paired outcomes the estimators consume |
| [[2405.05941\|SIMPLER]] | Pearson r as a single-sim ranking proxy | r>0.85, low MMRV | the single-sim baseline the portfolio must beat at equal compute |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a biased-sim portfolio gives tighter provable CIs than a single accurate sim at equal compute), with the experiment and the Related-table row it lands on.
1. **H1 (confirmatory — Sim2Val ran it) — Portfolio beats single-accurate-sim CI width at equal compute.**
   - *Prediction*: replicating [[2506.20553|Sim2Val]]'s control-variate result under [[2604.24018|Sim2Real Betting]]'s estimator, a bank of cheap biased sims yields tighter CIs at equal coverage than one high-fidelity sim at matched compute — confirming the now-consensus headline as the baseline H2/H5 build on.
   - *Test*: equal-compute allocation; compare CI width + coverage on held-out real SR for {biased bank} vs {single accurate sim}.
   - *Row*: Sim2Val (control-variate portfolio) / Sim2Real Betting (betting estimator) vs SIMPLER (single-sim proxy).
   - *Falsifier*: the single accurate sim matches the portfolio's CI at equal compute → even the conceded headline fails to reproduce and the direction collapses.
2. **H2 — Bias-diversity tightens the bound more than bias-count.**
   - *Prediction*: diversifying simulator bias (different physics approximations) tightens [[2510.04354|SureSim]]'s PPI bound more than adding copies of the same biased sim — diversity, not count, is the lever.
   - *Test*: sweep {bias-diverse bank} vs {redundant copies} at matched count; report CI width.
   - *Row*: SureSim (PPI bound).
   - *Falsifier*: redundant copies tighten the bound as much → diversity is not the value and count suffices.
3. **H3 — Adaptive Kelly allocation beats uniform real-trial spending.**
   - *Prediction*: using [[2604.24018|Sim2Real Betting]]'s Kelly weights to route real trials to policies where the bank is least certain beats uniform real-trial spending (link to C1's per-factor trust map).
   - *Test*: adaptive vs uniform real-trial allocation at matched budget; report CI width on the uncertain policies.
   - *Row*: Sim2Real Betting (portfolio).
   - *Falsifier*: uniform allocation matches adaptive → routing real trials by bank-uncertainty adds nothing.
4. **H4 — Informative bias beats adversarial bias; C1's gate selects it.**
   - *Prediction*: a bank of uniformly-wrong sims gives no edge, so the portfolio's gain depends on *informative* bias — using C1's per-factor trust map to select sims with informative bias (and exclude those failing under the relevant shift) recovers more of the 70–100% win than an unfiltered bank.
   - *Test*: {C1-gated bank} vs {unfiltered bank} on shift-mixed deployment; report win rate.
   - *Row*: Sim2Real Betting (portfolio) / UDA Simulation Study (no universally-best).
   - *Falsifier*: the unfiltered bank matches the gated one → bias informativeness doesn't matter and any bank works.
5. **H5 — The portfolio wins only past a compute-budget crossover.**
   - *Prediction*: there is a compute-budget crossover below which one accurate sim wins and above which the biased portfolio wins — mapping it tells you when to use which.
   - *Test*: sweep total compute; report the portfolio-vs-single CI-width crossover.
   - *Row*: Sim2Real Betting (portfolio) vs SIMPLER (single-sim).
   - *Falsifier*: the portfolio wins (or loses) at every budget → there is no crossover and the choice is unconditional.

> [!warning] Risks
> - **PPI/betting need a few paired real outcomes** — provable bounds still require some real data. → Pair with [[2510.17950|RoboChallenge]]'s remote fleet to keep the real-sample cost minimal while preserving validity.
> - **Bias must be informative, not adversarial** — a bank of uniformly-wrong sims gives no edge. → Use C1's per-factor trust map to *select* sims with informative bias and exclude those that fail under the relevant shift (H4).
> - **Portfolio overhead** — managing many sims adds engineering cost. → Quantify the compute-allocation frontier (H5) so the portfolio is only used where it provably beats the single-sim baseline.

---

## Cluster D — Deployment-Time Adaptation: Closing the Residual Gap Online

*Close the residual $\delta(t)$ at deploy-time — a time-varying disturbance observable only on hardware, that survives every train-, reconstruct-, and measure-time fix. The three directions split by which model is on hand: privileged extrinsics, an analytical model, or only a learned one.*

### D1 — Latent-Extrinsics Online Adaptation

| | |
|---|---|
| **Cluster** | D — Deployment-Time Adaptation |
| **Thesis** | Inferring a deployment latent from proprioceptive history and conditioning on it is now a built architecture — and the latest version, facing the question of what happens *outside* the training range, *gives up* and falls back to a robust feature. The contrarian bet is the inverse: inference *extends accurately* past the randomization range, so the gain concentrates exactly where robustification stalls. The first principle: the true dynamics are a deploy-time latent revealed only by on-robot history. The field assumes inference becomes unreliable OOD and you should robustify there instead. The bet is in First-principles below. |
| **Anchor papers** | [[2107.04034\|RMA]] (method), [[2412.04323\|GRAM]] (method), [[2409.16578\|FLaRe]] (method), [[2606.02280\|LDG]] (method), [[2212.07740\|TERT]] (method), [[2510.17950\|RoboChallenge]] (benchmark) |
| **Key targets** | [[2107.04034\|RMA]] zero-real-fine-tune adaptation across sand/mud/rocky/slippery + 12 kg payload (100% of body weight); [[2409.16578\|FLaRe]] real Stretch RE-1 SR 50%→80.7% (+30.7%), +23.6% sim, 72% LoCoBot embodiment transfer (6 h new-behavior); latent-extrinsics inference at deploy-time where fixed-DR plateaus |

**Why it matters.**
- **The gap**: a fixed domain-randomized policy is one bet placed at train-time — pick a range, hope deployment falls inside it — but the dynamics revealed on hardware don't exist until deployment, so no train-time randomization observes them.
- **Today's answers**: [[2107.04034|RMA]] trains a base policy on a privileged "extrinsics vector," then an adaptation module that *infers* it online from proprioceptive history alone (10 Hz, base policy at 100 Hz) — walking on sand/mud/rocky/slippery with a 12 kg payload (100% of body weight), *no* real fine-tuning; [[2409.16578|FLaRe]] makes the manipulation case — large-scale RL fine-tuning lifts a pre-trained BC policy from 50% real Stretch RE-1 SR to 80.7% (+30.7%) and transfers to LoCoBot (72% ObjectNav) by action-masking.
- **The boundary is now litigated**: [[2412.04323|GRAM]] builds the same proprioception-history latent-context architecture and answers D1's own boundary question on a real quadruped — but unifies adapt+robust and *concedes* inference becomes unreliable OOD, falling back to a robust latent feature. D1's surviving edge is the *inverse* of GRAM's conclusion: that continued inference *beats* robust-fallback outside the range.
- **The opening**: [[2606.02280|LDG]] shows the latent context can be *outcome-centric* (a learned dynamics context from interaction history, robust to unmodeled / time-varying / disabled-actuator shifts that break parameter-centric methods), and [[2212.07740|TERT]] shows it can be skipped entirely (history→action directly, 100% sand / 60% stairs where the RMA/TCN baseline scores 0%) — so the latent-extrinsics family has headroom the fixed policy cannot reach. On manipulation, [[2210.04887|In-Hand RMA]] and [[2011.11270|COCOI]] already close the contact residual via proprioception/force-history extrinsics inference *with no real reward* — so D1's manipulation claim is a baseline to beat, not an open target.

**First-principles framing.**
- **First principle**: The deployment environment's true dynamics are a latent variable revealed only by the robot's own proprioceptive history — no train-time randomization observes them, because they don't exist until deployment. The estimable quantity is the *posterior over extrinsics given on-robot history*, a deploy-time object by construction. [[2107.04034|RMA]]'s zero-fine-tune adaptation across radically different terrains is the proof that inferring the latent online beats marginalizing over it at train-time.
- **Assumption being challenged**: *Not* "infer-then-condition beats robustify" inside the range — that is settled ([[2107.04034|RMA]], [[2409.16578|FLaRe]]). The live assumption is [[2412.04323|GRAM]]'s: that inference becomes *unreliable* outside the randomization range, so you should give up and fall back to a robust latent there. D1 bets the inverse — that the latent-extrinsics estimate *extends accurately* some measurable distance past the range, so continued inference beats robust-fallback exactly where GRAM hands off. [[2606.02280|LDG]] supports the headroom (outcome-centric latents survive shifts no parameterization represents).
- **The bet**: Outside the train-time randomization range, a proprioception-only latent-extrinsics estimator **beats a [[2412.04323|GRAM]]-style robust-fallback** head-to-head — the real-SR gap *growing* with distance past the range (and vanishing inside it) — over a measurable envelope, reproducing [[2107.04034|RMA]]'s zero-real-fine-tune adaptation (sand/mud/12 kg) and [[2409.16578|FLaRe]]'s 50%→80.7% (+30.7%) *as the in-range baseline*. Falsifiable: if GRAM's robust-fallback matches or beats continued inference as deployment leaves the range, GRAM's give-up-OOD conclusion holds and the inverse bet fails.

**Related research papers.** One comparison table on the axis the direction turns on — *how the deployment latent is obtained* (privileged-extrinsics inference / RL fine-tune / outcome-centric latent / history-to-action direct / world-model supervision / parameter-level estimation) — plus key result and what each leaves open:

| System | How the deployment latent is obtained | Key result | What's missing |
|---|---|---|---|
| [[2107.04034\|RMA]] | proprioception-only inference of a *privileged extrinsics vector* (10 Hz) | zero real fine-tune across sand/mud/rocky/slippery + 12 kg | locomotion-shown; never tests whether inference *extends past* the DR range vs robust-fallback — the GRAM boundary question |
| [[2409.16578\|FLaRe]] | large-scale RL fine-tuning of a pre-trained BC policy | 80.7% real (+30.7%), 79.5% sim, 72% LoCoBot (6 h) | needs RL fine-tuning + reward — heavier than proprioception-only inference |
| [[2606.02280\|LDG]] | *outcome-centric* latent dynamics context (contrastive VI) | robust to unmodeled / time-varying / disabled-actuator shifts | RMA's context from parameters → outcomes; the parameter-free generalization |
| [[2212.07740\|TERT]] | history → action *directly* (no latent-vector estimation) | 100% sand / 60% stairs where RMA/TCN scores 0% | skips the explicit extrinsics — the no-latent alternative to RMA |
| [[2602.20057\|AdaWorldPolicy]] | world-model prediction error (4 Hz) | OOD recovery, LoRA test-time updates | a *learned*-model adaptation engine (the D3 regime), not proprioception-only |
| [[2510.11689\|Phys2Real]] | online inverse-variance-weighted *parameter* adaptation | 57% vs 23% OOD | parameter-level cousin — estimates named physics, not a latent extrinsics posterior |
| [[2603.04029\|Self-Adapting RL]] | prediction-residual OOD detection → online fine-tune | [[2301.04104\|DreamerV3]] residual trigger | the trigger a latent-extrinsics loop can gate on, not the estimator |
| [[2412.04323\|GRAM]] | proprioception-history latent context, *unified adapt + robust* | adapts in-range, falls back to a robust latent OOD (real quadruped) | the topThreat — builds D1's architecture and answers the boundary question, but *concedes* inference is unreliable OOD; D1 bets the inverse |
| [[2210.04887\|In-Hand RMA]] | proprioception-history extrinsics inference for *in-hand rotation* (no real reward) | zero-shot in-hand object rotation across objects | pre-answers H1 on manipulation — extrinsics inference already closes the contact residual without reward |
| [[2011.11270\|COCOI]] | *contact-aware* online context inference from interaction history | generalizable non-planar pushing via online context | the manipulation contact-residual baseline — context inference, not the OOD-envelope question D1 isolates |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (online latent-extrinsics inference beats a fixed-DR policy outside the range), with the experiment and the Related-table row it lands on.
1. **H1 — Latent-extrinsics *extends past the range* on manipulation, beyond the HORA/COCOI in-range baseline.**
   - *Prediction*: extrinsics inference already closes the *in-range* contact residual without real reward ([[2210.04887|In-Hand RMA]], [[2011.11270|COCOI]]); the open delta is that it keeps tracking *outside* the train-time range on contact-rich manipulation, recovering SR where [[2409.16578|FLaRe]] needs RL fine-tuning — so the claim moves from "closes the residual" (done) to "extends the envelope".
   - *Test*: latent-extrinsics inference vs In-Hand RMA/COCOI baselines vs RL fine-tune, pushing the contact task *outside* the DR range; report SR vs distance from the range.
   - *Row*: In-Hand RMA / COCOI (in-range manipulation baseline) vs FLaRe (RL fine-tune).
   - *Falsifier*: inference matches the in-range baseline but does not extend past the range → latent-extrinsics adds nothing beyond what HORA/COCOI already do on manipulation.
2. **H2 — The estimate stays accurate only within a measurable envelope past the DR range.**
   - *Prediction*: the latent-extrinsics estimate tracks the true dynamics some measurable distance outside the train-time DR range, then stops — mapping the envelope tells you when to trust it.
   - *Test*: push deployment progressively outside the DR range; report estimation error vs distance from the range.
   - *Row*: RMA (extrinsics inference).
   - *Falsifier*: the estimate is accurate everywhere or nowhere → there is no envelope and the deploy-time gain is illusory.
3. **H3 (front line) — Continued inference beats GRAM's robust-fallback outside the range.**
   - *Prediction*: matched policies — one [[2412.04323|GRAM]]-style adapt-in-range/robust-fallback-OOD, one continued-inference — show a real-SR gap that *grows* as deployment moves outside the range, the inverse of GRAM's give-up-OOD conclusion; inside the range they tie.
   - *Test*: both on the same task; sweep deployment distance from the DR range; report the SR gap and where GRAM hands off to its robust feature.
   - *Row*: GRAM (robust-fallback OOD) vs RMA (continued extrinsics inference).
   - *Falsifier*: GRAM's robust-fallback matches or beats continued inference outside the range → inference *is* unreliable OOD and GRAM's conclusion stands.
4. **H4 — Outcome-centric latent beats parameter-centric on unmodeled shifts.**
   - *Prediction*: [[2606.02280|LDG]]'s outcome-centric latent recovers more SR than [[2107.04034|RMA]]'s parameter-extrinsics on shifts no parameterization represents (disabled actuator, time-varying disturbance), and ties on in-model shifts.
   - *Test*: {outcome-centric} vs {parameter-extrinsics} on disabled-actuator + time-varying shifts; report SR per shift type.
   - *Row*: LDG (outcome-centric) vs RMA (parameter extrinsics).
   - *Falsifier*: parameter-extrinsics matches on unmodeled shifts → the outcome-centric latent adds nothing.
5. **H5 — History-to-action matches explicit extrinsics without the latent vector.**
   - *Prediction*: [[2212.07740|TERT]]'s direct history→action recovers RMA-class adaptation (100% sand) without an explicit extrinsics vector, so the latent representation is optional where the policy can read history directly.
   - *Test*: {history→action} vs {explicit extrinsics} on the same terrains; report SR and adaptation latency.
   - *Row*: TERT (history-to-action) vs RMA (explicit extrinsics).
   - *Falsifier*: the explicit extrinsics beats history→action → the latent vector is load-bearing, not optional.

> [!warning] Risks
> - **Proprioception under-determines extrinsics for some tasks** — vision-dominant manipulation may not expose dynamics in proprioceptive history (though [[2210.04887|In-Hand RMA]]/[[2011.11270|COCOI]] show force/proprio history suffices in-range). → Augment the estimator with force/tactile history (links to A2's GRF reward) where proprioception alone is uninformative (H1); report the observability boundary.
> - **Online adaptation can chase noise** — a too-fast estimator may track sensor noise as dynamics change. → Use [[2107.04034|RMA]]'s slow-module (10 Hz) / fast-policy (100 Hz) separation and gate updates on [[2603.04029|Self-Adapting RL]]'s residual magnitude.
> - **Unsafe adaptation during exploration** — online updates can drive unsafe actions before convergence. → Hand off to E1's safety-constrained continual adaptation rather than adapting reward-only.

### D2 — Differentiable-Sim Test-Time Adaptation

| | |
|---|---|
| **Cluster** | D — Deployment-Time Adaptation |
| **Thesis** | Online gradient-based test-time adaptation beating sampled RL on speed is, for an *analytical* controller, already done — single-trajectory non-episodic tuning of a geometric controller through an analytical model adapts to wind+payload more data-efficiently than model-free RL. But that route can only *tolerate* model error; it cannot *capture* it, because it has no learned residual and no neural policy. The first principle: if the dynamics model is differentiable, adapting is gradient descent on a known loss. The field assumes the analytical-controller-tuning result settles the question. The bet is in First-principles below. |
| **Anchor papers** | [[2508.21065\|Learning on the Fly]] (method), [[2507.10914\|M-GAPS]] (method), [[2603.04029\|Self-Adapting RL]] (method), [[2310.09053\|DATT]] (method), [[2604.04974\|Video-to-Control Survey]] (survey), [[2510.17950\|RoboChallenge]] (benchmark) |
| **Key targets** | [[2508.21065\|Learning on the Fly]] 81% hover-error reduction vs L1-MPC (55% vs [[2310.09053\|DATT]]) under large OOD disturbance, adaptation in 3 steps / 4.5 s wall-clock; beat [[2603.04029\|Self-Adapting RL]]'s minutes-long [[2301.04104\|DreamerV3]] fine-tune latency at equal safety risk |

**Why it matters.**
- **The gap**: when a quadrotor hits unmodeled wind or added mass, the residual must be corrected *now* — seconds, not minutes — but the standard recipe (RL fine-tuning of a learned world model) is slow because it re-learns from sampled rollouts.
- **Today's answers**: [[2603.04029|Self-Adapting RL]] detects OOD via [[2301.04104|DreamerV3]] prediction residuals and fine-tunes online, but a model-based RL fine-tune is slow; [[2508.21065|Learning on the Fly]] shows the alternative — a *differentiable* hybrid dynamics model (low-fidelity analytical core + learned residual MLP) lets policy gradients flow by Back-Propagation-Through-Time, so adaptation is a first-order step, not an RL loop: 81% hover-error reduction vs L1-MPC, 55% vs [[2310.09053|DATT]], meaningful improvement after only 3 steps (4.5 s wall-clock).
- **The general claim is taken**: [[2507.10914|M-GAPS]] does single-trajectory non-episodic online gradient-based policy adaptation on a *real* quadrotor, adapts to heavy unmodeled wind+payload, is "more data-efficient than model-free RL", and runs the DiffTune head-to-head that *is* D2's H1 — but it tunes the gain vector of a hand-designed geometric controller through a *purely analytical* model ("the dynamics model used by M-GAPS is unchanged from nominal"), so it is robust-*to* model error, not learning it. [[2202.09834|Differentiable-Physics Online MPC+SysID]] does the same online differentiable-physics adaptation via adaptive MPC since 2022.
- **The opening**: D2's distinctive regime is what M-GAPS structurally cannot do — BPTT through a *learned-residual hybrid* differentiable model ("low-fidelity analytical core + learned residual MLP") to adapt a *learned neural* policy, where the residual *captures* the disturbance M-GAPS can only tolerate. [[2508.21065|Learning on the Fly]] owns exactly this (81% hover-error reduction, 3-step / 4.5-s correction); [[2604.04974|Video-to-Control Survey]] names "control-loop closure" as the gap it closes.

**First-principles framing.**
- **First principle**: If the dynamics model is differentiable, adapting the policy to a new disturbance is just gradient descent on a known loss — the disturbance shows up as an error term the gradient fixes directly, so a few gradient steps suffice without the many trial-and-error rollouts model-free or model-based RL require. [[2508.21065|Learning on the Fly]]'s 3-step / 4.5-s correction is the evidence that exact gradients shrink adaptation to a handful of steps.
- **Assumption being challenged**: *Not* "online gradient adaptation is unavoidably slow" — that fell to the [[2210.12320|GAPS]] / [[2209.10021|DiffTune+]] / [[2202.09834|Differentiable-Physics Online MPC+SysID]] lineage by ~2022, and [[2507.10914|M-GAPS]] settles it for an analytical controller. The live assumption is that an *analytical-model* gradient route settles the whole question. It does not: a learned-residual hybrid model can *capture* a disturbance the analytical controller can only *tolerate* — and then BPTT adapts a *learned neural* policy, not a gain vector, so it works where no clean analytical form exists.
- **The bet**: BPTT through a *learned-residual hybrid* differentiable model adapting a *learned neural* policy corrects an OOD disturbance **in ≤3 steps / 4.5 s with 81% hover-error reduction** (vs L1-MPC; 55% vs [[2310.09053|DATT]]) — *and* recovers SR on a disturbance the residual captures but [[2507.10914|M-GAPS]]'s analytical-only model cannot represent, at matched wall-clock. Falsifiable: if M-GAPS's analytical-gradient route (no learned residual) matches the learned-residual loop on a disturbance off the nominal model, the learned residual buys nothing and the analytical route suffices.

**Related research papers.** One comparison table on the axis the direction turns on — *how the online adaptation gradient is obtained* (exact via differentiable sim / sampled via model-based RL / world-model self-supervision / robust-control baseline / parameter estimation / differentiable machinery reused) — plus key result and what each leaves open:

| System | How the adaptation gradient is obtained | Key result | What's missing |
|---|---|---|---|
| [[2508.21065\|Learning on the Fly]] | *exact* BPTT through a hybrid analytical+residual model | 81% vs L1-MPC, 55% vs [[2310.09053\|DATT]], 3 steps / 4.5 s | needs an analytical core — contact/friction transients hard to differentiate stably |
| [[2507.10914\|M-GAPS]] | *exact* online gradient, but tunes a geometric controller's gains through a *purely analytical* model | adapts to wind+payload on a real quadrotor, "more data-efficient than model-free RL", DiffTune head-to-head | the topThreat — settles online-gradient-beats-RL for an analytical controller, but no learned residual / no neural policy, so it *tolerates* not *captures* model error |
| [[2202.09834\|Differentiable-Physics Online MPC+SysID]] | *exact* online differentiable-physics gradient (adaptive MPC + sysID) | real-time online sysID + MPC via differentiable physics (RA-L'22) | the 2022 root proving online gradient adaptation is fast — analytical/parametric, no learned residual or neural policy |
| [[2603.27313\|MetaTune]] | adjoint-based *meta-tuning* via differentiable robot dynamics | meta-tuned adaptation through differentiable dynamics | adjoint gradients for parameter/gain meta-tuning, not BPTT adapting a learned neural policy with a learned residual |
| [[2602.20057\|AdaWorldPolicy]] | world-model prediction-error self-supervision (4 Hz) | OOD recovery, LoRA updates | a *learned*-model engine (D3 regime), no differentiable analytical dynamics |
| [[2310.09053\|DATT]] | adaptive control baseline (no differentiable sim) | the trajectory-tracking baseline Learning-on-the-Fly beats by 55% | classical adaptive control, not gradient-based test-time adaptation |
| [[2510.11689\|Phys2Real]] | online IVW *parameter* estimation | 57% vs 23% OOD | gradient-adjacent online estimation, not policy adaptation by BPTT |
| [[2604.27367\|DOT-Sim]] | differentiable MPM (for *parameter recovery*) | 96.55% zero-shot | the differentiable machinery TTA reuses at deploy-time — not yet a TTA loop |
| [[2604.10856\|BridgeSim]] | flow-matching observational calibrator (OL→CL) | +19.1 DS | test-time *observational* calibration, adjacent to policy-gradient TTA |
| [[2604.04974\|Video-to-Control Survey]] | (no method) names control-loop-closure gap | survey | the loop a fast differentiable TTA closes |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (exact-gradient differentiable TTA beats sampled model-based-RL fine-tune on speed at equal risk), with the experiment and the Related-table row it lands on.
1. **H1 (front line) — Learned-residual BPTT captures a disturbance M-GAPS's analytical route can only tolerate.**
   - *Prediction*: on a disturbance *off* the nominal analytical model (e.g. an unmodeled aerodynamic or contact effect), [[2508.21065|Learning on the Fly]]'s learned-residual-hybrid BPTT recovers more SR than [[2507.10914|M-GAPS]]'s analytical-only gain tuning, because the residual *represents* what the analytical model cannot — and both still beat [[2603.04029|Self-Adapting RL]]'s sampled fine-tune on wall-clock.
   - *Test*: inject a disturbance off the nominal model; compare SR + steps-to-correct for {learned-residual BPTT} vs {M-GAPS analytical gradient} vs {model-based-RL fine-tune}.
   - *Row*: Learning on the Fly (learned-residual BPTT) vs M-GAPS (analytical-only gradient) vs Self-Adapting RL (sampled RL).
   - *Falsifier*: M-GAPS's analytical route matches the learned-residual loop off the nominal model → the residual buys nothing and the analytical gradient suffices.
2. **H2 — Residual expressiveness trades adaptation speed against disturbance range.**
   - *Prediction*: [[2508.21065|Learning on the Fly]] backprops only through the analytical core; enlarging the learned residual captures a wider disturbance range but slows adaptation — a measurable speed/range frontier.
   - *Test*: sweep residual-network size; report adaptation speed vs the range of disturbances captured.
   - *Row*: Learning on the Fly (exact BPTT).
   - *Falsifier*: residual size changes neither speed nor range → expressiveness is irrelevant.
3. **H3 — The 3-step correction degrades on contact-rich ground manipulation.**
   - *Prediction*: the BPTT speed advantage holds where the analytical core is accurate (aerial) and erodes on contact-rich ground manipulation where richer contact forces more adaptation steps — so the bet is scoped to analytical-core regimes.
   - *Test*: compare steps-to-correct on aerial vs contact-rich tasks; report where the latency advantage shrinks.
   - *Row*: Learning on the Fly (exact BPTT) / DOT-Sim (differentiable contact machinery).
   - *Falsifier*: the 3-step correction holds on contact-rich tasks → the analytical-core boundary is not real.
4. **H4 — Exact gradients beat world-model self-supervision on latency where both apply.**
   - *Prediction*: where an analytical model exists, [[2508.21065|Learning on the Fly]]'s exact BPTT corrects faster than [[2602.20057|AdaWorldPolicy]]'s learned-world-model prediction-error supervision — exactness beats self-supervision on speed, marking the D2/D3 boundary.
   - *Test*: on a task with an analytical model, {exact BPTT} vs {world-model supervision}; report steps-to-correct.
   - *Row*: Learning on the Fly (exact BPTT) vs AdaWorldPolicy (world-model supervision).
   - *Falsifier*: world-model supervision matches exact BPTT on speed → the analytical model adds no latency advantage and D2 collapses into D3.
5. **H5 — A bounded per-step update keeps fast adaptation safe.**
   - *Prediction*: a bad gradient step can destabilize the platform, but bounding the per-step update (and handing execution-safety to E2's shield during the adaptation window) keeps the 3-step correction within the safety spec at no meaningful speed cost.
   - *Test*: {unbounded} vs {bounded per-step update + E2 shield}; report stability + adaptation speed.
   - *Row*: Learning on the Fly (exact BPTT).
   - *Falsifier*: bounding the update destroys the speed advantage → fast and safe trade off and the bet over-claims safety.

> [!warning] Risks
> - **Differentiable dynamics may not exist for the regime** — rich contact / friction transients are hard to differentiate stably. → Start in [[2508.21065|Learning on the Fly]]'s aerial/analytical-core regime where the hybrid model is accurate (H3); expand to contact via B2/B4's differentiable-MPM machinery cautiously.
> - **Fast overfitting to transient noise** — a 3-step adapt can lock onto a momentary disturbance. → Gate adaptation on [[2603.04029|Self-Adapting RL]]'s residual-magnitude trigger and decay the residual when the disturbance clears.
> - **Adaptation during flight is safety-critical** — a bad gradient step destabilizes the platform. → Bound the per-step update (H5) and hand execution-safety to E2's reachability shield during the adaptation window.

### D3 — World-Model-Supervised Online Policy Correction

| | |
|---|---|
| **Cluster** | D — Deployment-Time Adaptation |
| **Thesis** | Driving reward-free online policy correction from a world model's prediction error is no longer novel — per-step prediction-error supervision of a VLA, with an adaptive update filter, already recovers OOD without reward in sim. What survives is the *real-robot* instantiation: a unified world-model + force + action backbone that adapts at 4 Hz on hardware and adds a *force*-prediction-error term for contact OOD that an image-foresight head cannot supply. The first principle: physical consistency and task reward optimize different things, and prediction error is observable on hardware while reward is not. The field assumes prediction-error correction is the contribution. The bet is in First-principles below. |
| **Anchor papers** | [[2602.20057\|AdaWorldPolicy]] (method), [[2605.08215\|T3VF]] (method), [[2007.04309\|PAD]] (method), [[2604.18107\|PDF]] (method), [[2605.00080\|WM Robot Learning Survey]] (survey), [[2601.07823\|Video Generation in Robotics Survey]] (survey) |
| **Key targets** | [[2602.20057\|AdaWorldPolicy]] 0.96 [[2306.03310\|LIBERO]]-10 + 48.0% [[2112.03227\|CALVIN]] 5-task, online adaptation at 4 Hz on real robots via world-model prediction error (LoRA), recovering performance under visual+physical OOD where offline-only policies degrade |

**Why it matters.**
- **The gap**: the blocker on deploy-time correction is that *real reward is not available* — you cannot run RL on hardware against a reward you can't compute.
- **Today's answers**: [[2602.20057|AdaWorldPolicy]] resolves it by making the world model an *active supervisor* — it unifies a world model, an action expert, and a force predictor under a flow-matching DiT, and uses the world model's *prediction error* as a self-supervised signal to drive test-time LoRA updates, at 4 Hz on real robots, with no environment reward — holding 0.96 on [[2306.03310|LIBERO]]-10 and recovering under visual and physical OOD where an offline-only policy degrades.
- **The mechanism is now consensus**: [[2605.08215|T3VF]] drives online reward-free per-step weight updates of a VLA from a prediction-error supervision pair (predicted future image vs actual observation), with an adaptive update *filter* that is precisely D3's H5 calibration-gate, and explicitly positions itself against the reward-model/online-RL route — so "prediction error stands in for reward" is settled, not novel; [[2007.04309|PAD]] already broke the "needs reward" assumption in 2021 with self-supervised deploy-time adaptation on a real robot.
- **The opening**: T3VF runs in *sim* (LIBERO-Plus) with a *visual-foresight* head; D3's surviving territory is the *real-robot* 4 Hz regime via [[2602.20057|AdaWorldPolicy]]'s unified WM+force+action DiT, where a *force*-prediction-error term sharpens contact OOD that image foresight misses. [[2604.18107|PDF]] shows the reward-free family extends even without prediction-error supervision (verifier-free test-time perturbation learning, +8 pp LIBERO over OpenVLA) — the route H4 compares against.

**First-principles framing.**
- **First principle**: Training a policy toward physical consistency and toward task reward optimize *two different things*. A world model's prediction error measures how far the policy has drifted from the dynamics the model knows — and you can see that error on hardware, whereas you cannot see the task reward there; when the dynamics shift, the prediction error grows, so following it down corrects the right thing without any reward. [[2602.20057|AdaWorldPolicy]]'s 4 Hz real adaptation with *no* reward is the evidence that prediction error can stand in for the reward you can't observe.
- **Assumption being challenged**: *Not* "online correction needs reward" — [[2007.04309|PAD]] broke that in 2021, and [[2605.08215|T3VF]] makes prediction-error-as-reward consensus in sim. The live assumption is that an image-foresight prediction-error head is the whole signal. It is not on a real robot under *contact* OOD: a *force*-prediction-error term (which [[2602.20057|AdaWorldPolicy]]'s unified WM+force+action DiT supplies and T3VF's visual-foresight head cannot) carries the contact-drift direction visual prediction misses.
- **The bet**: An [[2602.20057|AdaWorldPolicy]]-style unified WM+force+action loop drives **4 Hz real-robot** online adaptation to unseen dynamics with no real reward, holding **0.96 [[2306.03310|LIBERO]]-10** under OOD where a static policy degrades, *and* its **force-prediction-error term beats a [[2605.08215|T3VF]]-style image-foresight-only head on contact-rich OOD** (the regime image foresight is blind to). Falsifiable: if image-foresight prediction-error supervision matches the force-augmented loop on contact OOD (or a static policy holds 0.96 under the same OOD), the force term — and the real-robot unified backbone — buys nothing over T3VF's sim result.

**Related research papers.** One comparison table on the axis the direction turns on — *what supplies the adaptation signal with no real reward* (world-model prediction error / prediction-residual trigger / learned-residual / verifier-free perturbation / parameter estimation / twin-grounded offline) — plus key result and what each leaves open:

| System | Adaptation signal (no real reward) | Key result | What's missing |
|---|---|---|---|
| [[2602.20057\|AdaWorldPolicy]] | world-model *prediction error* (flow-matching DiT) → 4 Hz LoRA | 0.96 [[2306.03310\|LIBERO]]-10, 48.0% [[2112.03227\|CALVIN]], OOD recovery | prediction-error-supervised proof — whether it matches a true-reward loop is open |
| [[2603.04029\|Self-Adapting RL]] | prediction-*residual* OOD detection → online fine-tune | [[2301.04104\|DreamerV3]] residual trigger | the precursor signal; uses the residual to *trigger*, not to supervise the whole update |
| [[2508.21065\|Learning on the Fly]] | learned-*residual* dynamics (the D2 differentiable cousin) | 3-step correction | analytical-model regime (D2), not learned-world-model supervision |
| [[2605.08215\|T3VF]] | *visual-foresight* prediction-error (predicted vs actual future image) → per-step VLA update + adaptive filter | OOD recovery on LIBERO-Plus, no reward, explicitly vs RL-route | the topThreat — owns the sim/image-foresight case incl. D3's H5 update-filter, but no real-robot 4 Hz, no unified WM+force DiT, no force-prediction-error term |
| [[2007.04309\|PAD]] | self-supervised auxiliary loss at deploy-time (the 2021 root) | self-supervised policy adaptation during deployment on a real robot | broke "online correction needs reward" in 2021 — but a hand-chosen auxiliary task, not world-model prediction-error supervision |
| [[2510.11689\|Phys2Real]] | online *parameter* estimation | 57% vs 23% OOD | parameter-level online correction, not prediction-error supervision |
| [[2511.07416\|PhysWorld]] | residual RL on a *reconstructed* world model (offline) | 82% real | world-model-grounded correction, but offline, not online prediction-error |
| [[2604.10856\|BridgeSim]] | truncated Q-estimator + observational calibrator (OL→CL) | +19.1 DS | closed-loop correction adjacent, not prediction-error self-supervision |
| [[2601.07823\|Video Generation in Robotics Survey]] | (no method) names hallucination/physics-violation risk | survey | the supervision risk a prediction-error loop must gate against |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (world-model prediction-error supervision drives reward-free online correction), with the experiment and the Related-table row it lands on.
1. **H1 — Prediction-error supervision matches a true-reward loop (or corrects a different objective).**
   - *Prediction*: where both are computable, [[2602.20057|AdaWorldPolicy]]'s prediction-error self-supervision either matches a true real-reward RL loop or corrects a measurably *different* (consistency, not task) objective — quantifying the gap tells which.
   - *Test*: {prediction-error} vs {true-reward RL} where reward is computable; report the SR gap and what each optimizes.
   - *Row*: AdaWorldPolicy (prediction error).
   - *Falsifier*: prediction-error supervision matches the reward loop exactly with no objective gap → consistency and task reward coincide and the distinction is moot.
2. **H2 — Prediction error detects some OOD shifts and is blind to others.**
   - *Prediction*: world-model prediction error gives a usable correction gradient for physical/dynamics OOD but is blind to visual-only OOD that doesn't change predicted dynamics — mapping which shifts it catches bounds the method.
   - *Test*: visual vs physical vs dynamics OOD; report where prediction error gives a usable gradient.
   - *Row*: AdaWorldPolicy (prediction error).
   - *Falsifier*: prediction error catches all OOD equally → there is no blind spot and the signal is universal.
3. **H3 (front line) — Force-prediction error beats a T3VF-style image-foresight head on contact-rich OOD.**
   - *Prediction*: [[2602.20057|AdaWorldPolicy]]'s unified world-model + force predictor lets a *force*-prediction-error term (links to A2's GRF reward, B2's tactile sysID) recover contact-rich OOD that [[2605.08215|T3VF]]'s visual-foresight prediction-error head is blind to — the force signal carries the contact-drift direction image foresight cannot see.
   - *Test*: {T3VF-style visual prediction error} vs {visual + force-prediction error} on contact-rich OOD; report correction quality and recovered SR.
   - *Row*: AdaWorldPolicy (force-augmented prediction error) vs T3VF (image-foresight only).
   - *Falsifier*: the image-foresight head matches the force-augmented loop on contact OOD → visual prediction error suffices and the force term (D3's surviving wedge) buys nothing.
4. **H4 — Prediction-error supervision beats verifier-free perturbation on dynamics OOD.**
   - *Prediction*: where the dynamics shift, [[2602.20057|AdaWorldPolicy]]'s prediction-error supervision recovers more SR than [[2604.18107|PDF]]'s verifier-free perturbation, because the prediction error carries the *direction* of the dynamics drift that blind perturbation must search for.
   - *Test*: {prediction-error supervision} vs {verifier-free perturbation} on dynamics OOD; report SR and steps-to-recover.
   - *Row*: AdaWorldPolicy (prediction error) vs PDF (verifier-free perturbation).
   - *Falsifier*: verifier-free perturbation matches prediction-error supervision → the directional signal is not worth the world model.
5. **H5 — World-model hallucination poisons the gradient unless calibration-gated.**
   - *Prediction*: when the world model is itself OOD, its prediction error supervises toward the *wrong* correction — gating updates on prediction-error *calibration* (links to E3's conformal detector) and rejecting corrections when the model is OOD prevents the poisoning [[2601.07823|Video Generation in Robotics Survey]] flags.
   - *Test*: inject world-model OOD; {ungated} vs {calibration-gated} updates; report corrupted-correction rate.
   - *Row*: AdaWorldPolicy (prediction error) / Video Generation in Robotics Survey (physics-violation flag).
   - *Falsifier*: the ungated loop never degrades under model OOD → hallucination doesn't poison the gradient and gating is unnecessary.

> [!warning] Risks
> - **World-model hallucination poisons the gradient** — a wrong prediction supervises toward the wrong correction. → Gate updates on prediction-error *calibration* (links to E3's conformal detector, H5) and reject corrections when the world model is itself OOD per [[2601.07823|Video Generation in Robotics Survey]]'s physics-violation flag.
> - **Prediction error ≠ task error** — minimizing consistency may not improve task success. → H1 measures the consistency-vs-task gap; pair prediction-error supervision with sparse real success checks where available.
> - **Unsafe correction under no-reward adaptation** — without reward, the loop may drift into unsafe regions. → Hand off to E1's safety-cost-constrained continual adaptation so the no-reward update stays inside safe limits.

---

## Cluster E — Risk-Bounded Sim-to-Real Deployment: Safety Under the Irreducible Gap

*Bound the irreducible residual gap at runtime — an un-handled gap is a safety failure, not just a performance loss, so it must be bounded, not assumed away. Three distinct surfaces: bound the update (E1), bound the action (E2), flag the failure (E3).*

### E1 — Zero-Violation Continual Adaptation

| | |
|---|---|
| **Cluster** | E — Risk-Bounded Sim-to-Real Deployment |
| **Thesis** | That reward-only continual adaptation goes unsafe, and that EWC alone fails to preserve safety, is now a measured published result. What no one has shown is whether a zero-violation continual-adaptation constraint *composes* — whether it wraps an arbitrary Cluster-D online engine on real hardware while preserving both the adaptation gain and the safety guarantee across successive domains. The first principle: an unsafe action on hardware has a consequence the reward cannot undo, so safety is a constraint set, not a reward term. The field assumes the safe×continual-RL framing settles it. The bet is in First-principles below. |
| **Anchor papers** | [[2503.10949\|SCDA]] (method), [[2604.19737\|Safe Continual RL (NSCMDP)]] (method), [[2509.18648\|SPiDR]] (method), [[2409.19190\|RAIL]] (method), [[2502.10694\|UDA Simulation Study]] (survey), [[2507.10087\|Foundation Robotics Review]] (survey) |
| **Key targets** | Hold [[2503.10949\|SCDA]]'s real grasp SR 20%→60% at *zero* violations *when wrapping a [[2107.04034\|RMA]]/[[2602.20057\|AdaWorldPolicy]] Cluster-D engine* (not just SCDA's own grasp loop); the safety-budget / adaptation-rate knee; zero forgetting × zero violations across *successive* domains where [[2604.19737\|Safe Continual RL (NSCMDP)]] shows online-EWC violates and CPO catastrophically forgets |

**Why it matters.**
- **The gap**: Cluster D's online engines all share a hazard — an exploratory update on real hardware can drive an unsafe action before it converges to a useful one — and the field's default (reward-only online RL fine-tuning) has no mechanism to keep exploration safe.
- **Today's answers**: [[2503.10949|SCDA]] documents that reward-only adaptation "led to unsafe behaviors" and makes safety a *constraint* — Policy-Constrained Reward and Cost Policy Optimization (PCRPO) for safe RL plus Elastic Weight Consolidation (EWC) for continual learning, with a Fisher Information Matrix computed in randomized-sim pretraining to protect important parameters, then adaptation under *stricter* safety limits on hardware: real grasp SR rises 20%→60% *at zero safety cost*, the only strategy that improves across an entire domain without catastrophic forgetting.
- **The assumption is now measured**: [[2604.19737|Safe Continual RL (NSCMDP)]] (and its ICRA'25 predecessor [[2502.15922|Safe EWC]]) defines the safe×continual-RL intersection and empirically shows online-EWC *violates* constraints while CPO *catastrophically forgets* — E1's two-axis tension as a published result; [[2604.09452|SafeAdapt]] restates the EWC critique near-verbatim. So "is unconstrained adaptation unsafe" is settled, and E1's front line must move to *composition*.
- **The opening**: the surviving gap is whether the zero-violation constraint *wraps arbitrary Cluster-D engines* on hardware. [[2509.18648|SPiDR]] shows safety can also be enforced at *transfer-time* (DR + pessimistic ensemble cost penalty as a CMDP, safe transfer to a real race car + Go1), so transfer-time and adaptation-time faces *compose* — and [[2507.10087|Foundation Robotics Review]] names "safety from model hallucinations" as a core open problem.

**First-principles framing.**
- **First principle**: On hardware, an action's safety cost is a hard constraint with no recovery — an unsafe exploratory update has a consequence the reward cannot undo. Adaptation must optimize reward *subject to* a safety-cost bound; safety is a constraint set, not a reward term. [[2503.10949|SCDA]]'s direct comparison (reward-only goes unsafe; cost-constrained hits zero violations at the same 60% SR) is the evidence that safety must be an explicit constraint.
- **Assumption being challenged**: *Not* "unconstrained adaptation is unsafe" — [[2604.19737|Safe Continual RL (NSCMDP)]]/[[2502.15922|Safe EWC]]/[[2604.09452|SafeAdapt]] made that a measured result. The live assumption is that the safe×continual-RL methods *are the deliverable* — demonstrated in isolation on their own loops. Whether the zero-violation constraint *composes* with an arbitrary Cluster-D online engine ([[2107.04034|RMA]], [[2602.20057|AdaWorldPolicy]]) on real hardware, and holds across *successive* domains, is untested — that composition is the open question.
- **The bet**: [[2503.10949|SCDA]]'s PCRPO+EWC, **wrapping a Cluster-D engine** ([[2107.04034|RMA]]/[[2602.20057|AdaWorldPolicy]]), holds the **20%→60% gain at zero violations** *and* keeps both zero forgetting and zero violations across **N successive domains** — where [[2604.19737|Safe Continual RL (NSCMDP)]] shows online-EWC violates and CPO forgets when run alone. Falsifiable: if wrapping a Cluster-D engine destroys the gain or admits violations, or successive-domain forgetting/safety trade off, the constraint does not compose and SCDA is a standalone result, not a wrapper.

**Related research papers.** One comparison table on the axis the direction turns on — *when and how safety is enforced during adaptation* (constrained continual adaptation / pessimistic transfer-time CMDP / execution-time shield / unconstrained engine / negative-adaptation warning) — plus key result and what each leaves open:

| System | When/how safety is enforced | Key result | What's missing |
|---|---|---|---|
| [[2503.10949\|SCDA]] | constrained *continual adaptation* (PCRPO + EWC + Fisher) | 20%→60% at *zero* cost, no forgetting | the adaptation-time anchor — wrapping arbitrary Cluster-D engines is open |
| [[2604.19737\|Safe Continual RL (NSCMDP)]] | *continual* safe RL in non-stationary envs (method-comparative) | online-EWC *violates* constraints while CPO *catastrophically forgets* | the topThreat — makes E1's two-axis tension a measured result, but MuJoCo/control-bench and comparative, not a real-hardware wrapper over Cluster-D engines |
| [[2502.15922\|Safe EWC]] | safe continual RL design for nonlinear control (ICRA'25 predecessor) | characterizes the safety×forgetting tension for control | the lineage root that settles "is unconstrained adaptation unsafe" — diagnosis, not a composition result |
| [[2604.09452\|SafeAdapt]] | *provably safe* policy updates in deep RL | provably safe policy-update scheme, restates the EWC critique | provable safe updates in isolation — never wraps an arbitrary online engine across successive domains |
| [[2509.18648\|SPiDR]] | *transfer-time* CMDP (pessimistic ensemble cost penalty) | safe transfer to real race car + Go1 where DR violates | transfer-time safety, not continual on-hardware adaptation — the complementary face |
| [[2409.19190\|RAIL]] | *execution-time* reachability shield | 0% collisions vs 5–35% | bounds the *action* (E2), not the *update* — complementary surface |
| [[2602.20057\|AdaWorldPolicy]] | none (4 Hz online LoRA under OOD) | OOD recovery | the unconstrained engine E1 hardens with a safety cost |
| [[2107.04034\|RMA]] | none (fast online latent-extrinsics) | zero-fine-tune, 12 kg payload | the D1 loop that needs a safety bound |
| [[2409.16578\|FLaRe]] | none (reward-driven RL fine-tuning) | +30.7% real | the reward-driven adaptation E1 makes safe |
| [[2603.04029\|Self-Adapting RL]] | none (residual-triggered fine-tune) | DreamerV3 residual trigger | the trigger that should fire under a safety constraint |
| [[2502.10694\|UDA Simulation Study]] | (no method) names "negative adaptation" | adaptation can do *worse* than none | the warning that unconstrained adaptation is unsafe |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (cost-constrained continual adaptation hits zero violations where reward-only goes unsafe), with the experiment and the Related-table row it lands on.
1. **H1 — The zero-violation result holds when wrapping Cluster-D engines.**
   - *Prediction*: wrapping [[2107.04034|RMA]]-style (D1) and [[2602.20057|AdaWorldPolicy]]-style (D3) adaptation in [[2503.10949|SCDA]]'s PCRPO+EWC holds the zero-violation result while preserving the adaptation gain.
   - *Test*: {unconstrained D-engine} vs {SCDA-wrapped} on the same OOD; report violations and SR.
   - *Row*: SCDA (constrained adaptation) over AdaWorldPolicy / RMA (unconstrained engines).
   - *Falsifier*: wrapping destroys the gain or admits violations → the constraint doesn't compose with Cluster D.
2. **H2 — There is a safety-budget / adaptation-rate Pareto frontier.**
   - *Prediction*: tightening the safety-cost limit erodes the 20%→60% gain past a measurable point — a budget/rate frontier where the loosest limit that still guarantees zero violations maximizes SR.
   - *Test*: sweep the safety-cost limit; report SR vs limit, find the zero-violation knee.
   - *Row*: SCDA (constrained adaptation).
   - *Falsifier*: SR is flat in the budget → there is no trade-off and the limit can be set arbitrarily tight.
3. **H3 — EWC keeps zero forgetting *and* zero violations across successive domains.**
   - *Prediction*: across successive domains, [[2503.10949|SCDA]]'s Fisher-protected adaptation keeps both zero violations and zero forgetting — or the two trade off as domains accumulate, which the experiment reveals.
   - *Test*: chain N domain shifts; report violations + forgetting per domain.
   - *Row*: SCDA (constrained adaptation).
   - *Falsifier*: forgetting and safety stay both zero indefinitely *or* one collapses — either way the frontier is characterized.
4. **H4 — Transfer-time and adaptation-time safety compose.**
   - *Prediction*: combining [[2509.18648|SPiDR]]'s transfer-time CMDP with [[2503.10949|SCDA]]'s continual safe adaptation yields fewer total violations than either alone, because they bound different windows (initial transfer vs ongoing adaptation).
   - *Test*: {SPiDR only} vs {SCDA only} vs {both}; report violations across the transfer + adaptation timeline.
   - *Row*: SPiDR (transfer-time) + SCDA (adaptation-time).
   - *Falsifier*: combining adds no safety over the better single method → the windows overlap and one suffices.
5. **H5 — A model-free backstop covers safety-cost misspecification.**
   - *Prediction*: a wrong safety-cost function permits unsafe actions it doesn't penalize, but pairing with E2's reachability shield as a model-free backstop catches them — so safety doesn't rest on the learned cost alone.
   - *Test*: inject cost-model misspecification; {SCDA only} vs {SCDA + E2 shield}; report residual violations.
   - *Row*: SCDA (constrained adaptation) / RAIL (execution-time shield).
   - *Falsifier*: SCDA alone never admits violations under misspecification → the learned cost is sufficient and the backstop is redundant.

> [!warning] Risks
> - **Tight safety cost can stall adaptation** — an over-strict limit may freeze the 20%→60% gain. → H2 maps the budget/rate frontier; set the limit at the loosest value that still guarantees zero violations.
> - **EWC protection can over-rigidify** — too-strong Fisher penalties block needed adaptation. → Tune the EWC weight per [[2503.10949|SCDA]]'s schedule and monitor the forgetting/adaptation balance across domains (H3).
> - **Cost model misspecification** — a wrong safety-cost function permits unsafe actions it doesn't penalize. → Pair with E2's reachability shield as a model-free backstop (H5) so safety doesn't rest on the learned cost alone.

### E2 — Reachability-Filtered Sim-to-Real Execution

| | |
|---|---|
| **Cluster** | E — Risk-Bounded Sim-to-Real Deployment |
| **Thesis** | That a hard reachability filter beats a soft penalty — at preserved success rate, even raising SR for weak policies — is now executed and won, on diffusion policies, on a real arm. What no filter does is shield a policy that is *itself changing*: a Cluster-D online-adapting policy whose actions shift mid-deployment, where a fixed-geometry occupancy model provably misses residual-gap hazards. The first principle: collision-freeness is a reachability property of forward occupancy, verifiable independent of the policy. The field assumes the static-policy hard-filter result settles safe execution. The bet is in First-principles below. |
| **Anchor papers** | [[2409.19190\|RAIL]] (method), [[2511.06385\|Path-Consistent Safety Filter]] (method), [[2505.00779\|Uncertainty Latent Safety Filter]] (method), [[2303.04137\|Diffusion Policy]] (method), [[2604.04974\|Video-to-Control Survey]] (survey), [[2507.10087\|Foundation Robotics Review]] (survey) |
| **Key targets** | Hold [[2409.19190\|RAIL]]'s 0%-collision guarantee (vs 5–35% baseline IL) over a *changing* [[2508.21065\|Learning on the Fly]]/[[2602.20057\|AdaWorldPolicy]] policy mid-adaptation, at bounded SR cost; match [[2511.06385\|Path-Consistent Safety Filter]]'s +68% SR over soft CBF on a real Franka as the *static* baseline; close the residual-gap hazards a fixed-geometry filter misses ([[2505.00779\|Uncertainty Latent Safety Filter]]) |

**Why it matters.**
- **The gap**: when a sim-trained imitation-learning policy hits the residual gap, it produces compounding errors and OOD actions — and the field's usual safety is *soft*: penalty terms or probabilistic constraints that bound risk in expectation, not absolutely.
- **Today's answers**: [[2409.19190|RAIL]] makes safety a *hard* guarantee — a continuous-time reachability filter checks whether the IL policy's plan is collision-free (computing the robot's forward occupancy), and if not, a model-based backup planner executes a guaranteed-safe alternative: 0% collision rate across all tasks vs 5–35% for baseline IL (Pick-Place RAIL+DP 0% vs [[2303.04137|Diffusion Policy]] 27.2%), ~10-pp cost (68% vs 78% SR), 0.42 s/plan on a real Franka.
- **The headline is now won**: [[2511.06385|Path-Consistent Safety Filter]] (RAIL's diffusion-policy successor) runs set-based reachability over the action chunk with a formal guarantee on a real Franka FR3, preserves SR, beats soft CBF baselines by up to +68% SR, and explicitly fixes the "external safety alters actions unseen in training → degradation" gap via path-consistent braking; [[2502.00935|Latent Safety Filters]] pre-runs the weak-policy boost ("makes a suboptimal IL policy safer"). So hard-vs-soft and the +16-pp weak-policy boost are confirmatory.
- **The opening**: [[2505.00779|Uncertainty Latent Safety Filter]] owns the on-thesis residual-gap version — and shows a *fixed-geometry* reachability filter is *insufficient* under the gap — but no filter shields a policy that is *itself adapting* mid-deployment; [[2604.04974|Video-to-Control Survey]] names "physical feasibility" and "loop closure" as the exact gaps a runtime guarantee supplies.

**First-principles framing.**
- **First principle**: Collision-freeness is a reachability property of the robot's forward occupancy — verifiable in continuous time independent of the policy, so safety can be a hard runtime filter, not a learned objective. A guarantee that holds requires verification, not a penalty in expectation. [[2409.19190|RAIL]]'s 0%-vs-5–35% result is the evidence that only verification eliminates collisions under OOD actions.
- **Assumption being challenged**: *Not* "learned soft safety suffices" — [[2511.06385|Path-Consistent Safety Filter]]'s +68% SR over CBF and [[2505.00779|Uncertainty Latent Safety Filter]] already won the hard-vs-soft argument over IL/diffusion policies. The live assumption is that the *static-policy* hard-filter result settles safe execution. It does not: a Cluster-D online-adapting policy changes its actions mid-deployment, and a *fixed-geometry* occupancy model provably misses residual-gap hazards ([[2505.00779|Uncertainty Latent Safety Filter]]) — so the guarantee must hold over a *moving* policy and an *uncertain* geometry.
- **The bet**: A reachability shield holds the **0%-collision guarantee over a *changing* policy mid-adaptation** ([[2508.21065|Learning on the Fly]]/[[2602.20057|AdaWorldPolicy]]), at a bounded SR cost during the adaptation window — where the static-policy baseline ([[2409.19190|RAIL]] 0% vs 5–35%; [[2511.06385|Path-Consistent Safety Filter]] +68% over CBF on a real Franka) is the confirmatory floor — *and* an uncertainty-aware occupancy model closes the residual-gap hazards a fixed-geometry filter misses. Falsifiable: if collisions appear while the policy adapts (the guarantee assumed a fixed policy), or a fixed-geometry filter already catches the residual-gap hazards, the adapting-policy / uncertainty-aware extension buys nothing.

**Related research papers.** One comparison table on the axis the direction turns on — *what kind of safety guarantee is provided* (hard reachability verification / unshielded soft IL / detect-then-shield conformal / adaptation-time constraint / pre-action verification / changing-policy target) — plus key result and what each leaves open:

| System | Kind of safety guarantee | Key result | What's missing |
|---|---|---|---|
| [[2409.19190\|RAIL]] | *hard* continuous-time reachability filter + backup planner | 0% collisions (vs 5–35% IL), ~10-pp cost, 0.42 s/plan real Franka | the hard-guarantee anchor — shielding a *changing* (adapting) policy is open |
| [[2303.04137\|Diffusion Policy]] | none (soft IL) | 78% Pick-Place SR / 27.2% collisions | the unshielded IL whose OOD actions the shield bounds |
| [[2511.06385\|Path-Consistent Safety Filter]] | *hard* set-based reachability over the diffusion-policy action chunk + path-consistent braking | formal guarantee on real Franka FR3, +68% SR over soft CBF | the topThreat — wins hard-vs-soft on E2's own anchor policy class, but shields a *static* policy; the adapting-policy case (H1) is untouched |
| [[2505.00779\|Uncertainty Latent Safety Filter]] | *uncertainty-aware* latent-space reachability for OOD failures | avoids OOD failures a fixed-geometry filter misses | the on-thesis residual-gap version — shows fixed-geometry reachability is insufficient under the gap, but still a static policy |
| [[2506.09937\|SAFE]] | conformal runtime *detection* (not prevention) | <1 ms, zero-shot to unseen tasks | flags failure (E3), doesn't prevent collision — the detect half of detect-then-shield |
| [[2503.10949\|SCDA]] | adaptation-time safety *constraint* | 20%→60% at zero cost | bounds the *update* (E1), not the *action* — complementary surface |
| [[2605.22446\|Pre-VLA]] | *pre-action* verification of candidate chunks | F1 0.8303, +6.83 pp LIBERO closed-loop | pre-action verification complementing post-hoc shielding |
| [[2604.05484\|CoEnv]] | *twin-grounded* swept-collision verification before execution | 49% across 5 real multi-agent tasks; verification ablation 50%→20% | a geometric pre-check in a reconstructed twin — softer than [[2409.19190\|RAIL]]'s continuous-time guarantee, and twin-fidelity-bound (links to B1) |
| [[2604.17896\|Physical-Feasibility VLA]] | *training-time* differentiable geometric feasibility loss (no runtime check) | SSR 22.00%→43.50% under perturbation; 40 demos beat 120 | bakes feasibility into the policy as a soft inductive bias — the train-time contrast to a hard runtime shield, with no deploy-time guarantee |
| [[2508.21065\|Learning on the Fly]] | none (fast online adaptation) | 3-step correction | the changing policy E2 must shield mid-adaptation |
| [[2602.20057\|AdaWorldPolicy]] | none (online-adapting policy) | OOD recovery | shield target during no-reward updates |
| [[2604.04974\|Video-to-Control Survey]] | (no method) names physical-feasibility gap | survey | the gap E2 fills with a hard guarantee |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a hard reachability shield drives collisions to 0% where soft penalties can't), with the experiment and the Related-table row it lands on.
1. **H1 — The 0%-collision guarantee survives an *adapting* policy.**
   - *Prediction*: running [[2409.19190|RAIL]]'s filter over a [[2508.21065|Learning on the Fly]] (D2) or [[2602.20057|AdaWorldPolicy]] (D3) online-adapting policy keeps the 0%-collision guarantee while the policy is *changing*, at a bounded SR cost during adaptation.
   - *Test*: shield an adapting policy; report collisions + SR cost during the adaptation window.
   - *Row*: RAIL (hard shield) over Learning on the Fly / AdaWorldPolicy (changing policies).
   - *Falsifier*: collisions appear while the policy adapts → the shield's guarantee assumes a fixed policy.
2. **H2 — There is an intervention-rate / SR-cost frontier set by the reachability margin.**
   - *Prediction*: tightening the reachability margin trades intervention rate against the ~10-pp SR cost across task families, and intervention falls as the policy improves across epochs ([[2409.19190|RAIL]] already reports this).
   - *Test*: sweep the reachability margin; report intervention rate vs SR cost per task family.
   - *Row*: RAIL (hard shield).
   - *Falsifier*: intervention and SR-cost are uncoupled from the margin → the margin is not the control knob.
3. **H3 — The shield *raises* SR for weak policies, *costs* SR for strong ones.**
   - *Prediction*: characterizing the +16 pp SSucc boost, hard safety improves weak-policy SR (by pruning doomed trajectories) and costs ~10 pp for strong policies — a policy-strength-dependent sign on the SR effect.
   - *Test*: stratify by policy strength; report the SR effect (boost vs cost) per strength bin.
   - *Row*: RAIL (hard shield) over Diffusion Policy (unshielded IL).
   - *Falsifier*: the shield always costs SR → it never boosts weak policies and the +16 pp is an artifact.
4. **H4 (confirmatory — PACS won it) — Hard verification beats a soft penalty on collisions under the same OOD.**
   - *Prediction*: under the OOD-action generator ([[2402.08191|THE COLOSSEUM]]'s 14 factors), a soft safety penalty cannot reach 0% collisions while a hard filter does — reproducing [[2511.06385|Path-Consistent Safety Filter]]'s +68% SR over soft CBF as the static baseline the adapting-policy bet (H1) builds on.
   - *Test*: {soft penalty} vs {hard shield} under COLOSSEUM-perturbed deployment on a static policy; report collision rate.
   - *Row*: Path-Consistent Safety Filter (hard, +68% over CBF) / RAIL (hard shield) vs Diffusion Policy (soft IL).
   - *Falsifier*: the soft penalty reaches 0% collisions → even the conceded hard-vs-soft result fails to reproduce.
5. **H5 — Pre-action verification + reachability shield beats either alone.**
   - *Prediction*: combining [[2605.22446|Pre-VLA]]'s pre-action chunk verification with [[2409.19190|RAIL]]'s reachability shield catches more unsafe actions than either alone — pre-screening reduces shield interventions and the shield catches what pre-screening misses.
   - *Test*: {Pre-VLA only} vs {RAIL only} vs {both}; report collisions + intervention rate.
   - *Row*: Pre-VLA (pre-action) + RAIL (hard shield).
   - *Falsifier*: combining adds nothing → the two catch the same actions and one suffices.

> [!warning] Risks
> - **Reachability filtering adds latency** — continuous-time occupancy checks may slow the control loop. → [[2409.19190|RAIL]] runs at 0.42 s per plan on a real Franka, so it is tractable; precompute occupancy and bound the per-step check budget.
> - **Conservative shields over-intervene** — too-tight margins freeze the robot. → H2 maps the intervention/SR-cost frontier; set the margin at the loosest value that preserves 0% collisions.
> - **Shield needs a model of obstacles** — reachability requires environment geometry the residual gap may misestimate. → Ground the occupancy model in B1's reconstruction fidelity and fall back to E3's conformal detector where geometry is uncertain.

### E3 — Conformal Runtime Failure Detection

| | |
|---|---|
| **Cluster** | E — Risk-Bounded Sim-to-Real Deployment |
| **Thesis** | Detecting failures from successful runs alone, via a conformal threshold with an FPR guarantee, zero-shot to unseen tasks, is now consensus — the field dropped failure-labeled datasets years ago. What no one has shown is a *closed* detect-then-act loop that provably *preserves* the conformal false-positive bound while cutting user-facing failures, nor that internal-feature detectors transfer *across architectures* with a policy-agnostic backstop. The first principle: a failure is an OOD event against the success manifold, so success-modeling plus a sound cutoff suffices. The field assumes detection needs failure-labeled data — a habit it already abandoned. The bet is in First-principles below. |
| **Anchor papers** | [[2510.09459\|FIPER]] (method), [[2410.04640\|Sentinel]] (method), [[2506.09937\|SAFE]] (method), [[2503.08558\|FAIL-Detect]] (method), [[2602.01515\|RAPT]] (method), [[2510.17950\|RoboChallenge]] (benchmark) |
| **Key targets** | A detect-then-act loop (flag → [[2409.19190\|RAIL]] backup / [[2503.10949\|SCDA]] safe-adapt) that *preserves* the conformal FPR bound while cutting user-facing failures; cross-architecture transfer of [[2506.09937\|SAFE]]'s internal-feature detector backstopped by [[2503.08558\|FAIL-Detect]]'s success-only density; reproduce [[2510.09459\|FIPER]]'s no-failure-data conformal detection (beating the FAIL-Detect lineage on earlier + more accurate prediction) as the settled baseline |

**Why it matters.**
- **The gap**: detecting failures from successes alone is settled, so a detector *trained on labeled failures* is the wrong-distribution mistake the field already corrected — the open problem is what to *do* with the flag while keeping the guarantee, and whether the strongest internal-feature detectors transfer across policies.
- **Today's answers**: [[2510.09459|FIPER]] does the bet near-verbatim — no failure-labeled data, conformal calibration on successful rollouts only, OOD + action-uncertainty scores — and explicitly beats the FAIL-Detect lineage on *earlier* and *more accurate* prediction; [[2410.04640|Sentinel]] is the success-only root (runtime monitoring of consistency + progress, CoRL'24); [[2503.08558|FAIL-Detect]] (~78% sim / ~72% real, success-only logpZO) and [[2506.09937|SAFE]] (internal-feature conformal, <1 ms, zero-shot, FPR guarantee) are the now-settled instances.
- **The opening**: the surviving leverage is *structural* — (1) a detect-then-*act* loop that provably *preserves* the conformal FPR bound while cutting failures (closing the loop, not just flagging), and (2) cross-architecture transfer of [[2506.09937|SAFE]]'s internal features with a policy-agnostic density backstop; [[2602.01515|RAPT]]'s root-cause diagnosis (AUROC 0.92 sim, 1.63 ms) and [[2605.30834|Hide-and-Seek]]'s step-level localization (0.852 bACC) point at the targeted-response half H5 probes.

**First-principles framing.**
- **First principle**: A failure is just anything that looks unlike a successful run — an OOD event — so you can spot it from successful runs alone; pairing that with a conformal threshold (a calibration that caps how often you cry wolf, with a guarantee that holds even on a small calibration set) bounds the false-alarm rate. Detection needs a model of what success looks like plus a sound cutoff, not examples of failures. [[2503.08558|FAIL-Detect]]'s ~78%/72% from successes only is the evidence that success-modeling generalizes where failure-labeling cannot.
- **Assumption being challenged**: *Not* "detection needs failure-labeled data" — the field dropped that by [[2410.04640|Sentinel]] (CoRL'24) and [[2510.09459|FIPER]] (NeurIPS'25), so the success-only detect-from-OOD result is settled. The live assumption is that *detection is the deliverable* — that flagging, with a conformal guarantee, is the end. It is not: closing a detect-then-*act* loop generally *breaks* the FPR bound (the action changes the distribution the conformal calibration assumed), and internal-feature detectors are policy-internal so they may not transfer across architectures — both untested.
- **The bet**: (i) A detect-then-act loop wiring the conformal flag to [[2409.19190|RAIL]]'s backup or [[2503.10949|SCDA]]'s safe-adapt **preserves the FPR guarantee** while cutting user-facing failures (the bound holds *through* the action, not just at the flag). (ii) [[2506.09937|SAFE]]'s internal-feature detector **does not transfer across architectures**, and pairing it with [[2503.08558|FAIL-Detect]]'s policy-agnostic density score recovers detection on the architectures the internal features miss. Reproduce [[2510.09459|FIPER]]'s no-failure-data conformal detection as the settled baseline. Falsifiable: if the detect-then-act loop preserves the bound *trivially* (action never shifts the distribution) or internal features transfer across architectures unchanged, neither structural sub-claim is real and the settled detection result is the whole story.

**Related research papers.** One comparison table on the axis the direction turns on — *what the detector learns from and what it outputs* (success-only density / internal-feature conformal / step-level localization / detection + root-cause / prediction-error / action+state anomaly / pre-action verification) — plus key result and what each leaves open:

| System | What it learns from / outputs | Key result | What's missing |
|---|---|---|---|
| [[2510.09459\|FIPER]] | *no failure data* (conformal on successes, OOD + action-uncertainty) | beats the FAIL-Detect lineage on *earlier* + *more accurate* prediction | the topThreat — does E3's bet near-verbatim, leaving only the detect-then-act FPR-preservation (H3) and cross-arch transfer (H4) open |
| [[2410.04640\|Sentinel]] | *successes only* (runtime monitoring of consistency + progress, STAC) | success-only failure monitoring (CoRL'24) | the success-only root that settled "no failure labels needed" — diagnosis, not a closed detect-then-act loop |
| [[2506.09937\|SAFE]] | policy *internal features* + functional Conformal Prediction | <1 ms overhead, zero-shot unseen-task, FPR guarantee | features are policy-internal — may not transfer across architectures (H4) |
| [[2503.08558\|FAIL-Detect]] | *successes only* (flow-based logpZO + conformal) | ~78% sim / ~72% real, top in 10/16 sim & 8/12 hardware | the policy-agnostic density backstop for H4 — coarser than internal-feature |
| [[2605.30834\|Hide-and-Seek]] | trajectory-only labels → step-level *localization* (LSTM + contrastive) | 0.852 bACC, +11.7% bACC / +15.0% TWA unseen real, 2,000× faster than VLM | step-level localization sharpens SAFE's label noise — coarse supervision, not success-only |
| [[2602.01515\|RAPT]] | model-predictive OOD detection + *root-cause diagnosis* | AUROC 0.92 sim / 75% real recall at zero nominal FP, 1.63 ms | detection *plus* diagnosis — humanoid sim-to-real specific |
| [[2604.16677\|ReconVLA]] | conformal action-level + Mahalanobis state-level anomaly over frozen VLA | AUC 0.922 (π₀), halts 16/20 before hardware limits | detection without touching the policy — two-level, not internal-feature |
| [[2603.11106\|RC-NF]] | *successes only* (robot-conditioned normalizing flow) | <100 ms, +8% AUC / +10% AP on LIBERO-Anomaly-10 | the success-only density detector, RC-NF's flow to FAIL-Detect's logpZO |
| [[2602.20057\|AdaWorldPolicy]] | world-model *prediction error* as an OOD signal | OOD recovery | the detector D3 uses, complementary to internal-feature detection |
| [[2605.22446\|Pre-VLA]] | *pre-action* chunk verification | F1 0.8303, +6.83 pp LIBERO closed-loop | pre-action verification complementing post-hoc detection (links to E2) |
| [[2603.04029\|Self-Adapting RL]] | prediction-residual OOD detection | DreamerV3 residual | the trigger E3 generalizes with a conformal guarantee |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a conformal success-only detector flags sim2real failures at <1 ms with no failure labels), with the experiment and the Related-table row it lands on.
1. **H1 (confirmatory — FIPER/Sentinel settled it) — Success-only detection beats failure-labeled on held-out sim2real failures.**
   - *Prediction*: success-only OOD detection ([[2510.09459|FIPER]], [[2503.08558|FAIL-Detect]]) beats a failure-labeled detector on *held-out sim2real-induced* failures (the ones the labeled set can't contain) — reproducing FIPER's edge over the FAIL-Detect lineage as the settled baseline H3/H4 build on.
   - *Test*: {success-only} vs {failure-labeled} on held-out sim2real failures; report balanced accuracy.
   - *Row*: FIPER (no-failure-data conformal) / FAIL-Detect (success-only) / Sentinel (success-only root).
   - *Falsifier*: the failure-labeled detector wins on held-out failures → even the conceded success-only result fails to reproduce.
2. **H2 — Internal-feature detection fires earlier than prediction-error at lower overhead.**
   - *Prediction*: [[2506.09937|SAFE]]'s internal-feature signal detects failures earlier and at lower overhead than [[2602.20057|AdaWorldPolicy]]'s world-model prediction error on the same failures.
   - *Test*: {internal-feature} vs {prediction-error} on the same failures; report detection lead-time and overhead.
   - *Row*: SAFE (internal-feature) vs AdaWorldPolicy (prediction-error).
   - *Falsifier*: prediction-error detects earlier/cheaper → internal features are not the better signal.
3. **H3 — A detect-then-act loop preserves the FPR guarantee while cutting failures.**
   - *Prediction*: wiring E3's conformal flag to E2's reachability backup or E1's safe-adaptation trigger keeps the FPR guarantee while reducing the failures that reach the user.
   - *Test*: {detection only} vs {detect-then-act}; report FPR + user-facing failure rate.
   - *Row*: SAFE (internal-feature) / RAIL (the act half) / SCDA (the adapt half).
   - *Falsifier*: detect-then-act breaks the FPR guarantee → the loop cannot preserve the conformal bound.
4. **H4 — A policy-agnostic density score backstops architecture-specific internal features.**
   - *Prediction*: [[2506.09937|SAFE]]'s internal features don't transfer across architectures, but pairing with [[2503.08558|FAIL-Detect]]'s/[[2603.11106|RC-NF]]'s policy-agnostic density score recovers detection on the architectures SAFE's features miss.
   - *Test*: transfer SAFE's detector across architectures; {internal-feature only} vs {+ density backstop}; report detection.
   - *Row*: SAFE (internal-feature) / FAIL-Detect (policy-agnostic density) / RC-NF (flow density).
   - *Falsifier*: internal features transfer across architectures → no backstop is needed.
5. **H5 — Step-level localization + root-cause beats binary detection for response.**
   - *Prediction*: [[2605.30834|Hide-and-Seek]]'s step-level localization and [[2602.01515|RAPT]]'s root-cause diagnosis enable a *targeted* response (which step, which cause) that recovers more SR than binary detect-then-halt.
   - *Test*: {binary detect} vs {localize + diagnose → targeted response}; report recovered SR.
   - *Row*: Hide-and-Seek (localization) / RAPT (root-cause) vs FAIL-Detect (binary success-only).
   - *Falsifier*: targeted response matches binary halt → localization/diagnosis add no actionable value.

> [!warning] Risks
> - **Conformal validity needs a calibration set of successes** — the FPR guarantee rests on representative success data. → Calibrate per [[2503.08558|FAIL-Detect]]'s success-only protocol on the deployment distribution and re-calibrate on domain shift to keep coverage.
> - **Internal-feature detectors are model-specific** — [[2506.09937|SAFE]]'s features are policy-internal and may not transfer across architectures. → Pair with [[2503.08558|FAIL-Detect]]'s/[[2603.11106|RC-NF]]'s policy-agnostic density score as a model-independent fallback (H4).
> - **Detection without response is inert** — flagging a failure the system can't avoid adds no safety. → H3's detect-then-act loop wires the flag to E2's shield or E1's safe adaptation so detection drives a bounded response.

---

## Cross-Cutting Themes

> [!tip] The Reality Gap Is Bidirectional — and Real→Sim Is Now the Binding Constraint
> B1, B2, B4, and A1 all turn on the same inversion: the forward gap Cluster A attacks is lower-bounded by how faithfully reality was run *backward* into the simulator. [[2512.19562|REALM]] names the real-to-sim gap as a distinct object; [[2511.04665|Real-to-Sim GS]] measures it (r=0.915 vs [[2511.04831|Isaac Lab]] 0.649) and its ablation shows the gap closes only when appearance ($\phi^\star$, B1) and dynamics ($\psi^\star$, B2) are inverted *together*; B4 pushes the inversion one level deeper, recovering the constitutive *law* not its parameters; A1's neural-rendering-in-the-loop is the same inversion applied to semantics. The field spent a decade making sims transfer forward (Cluster A); the leverage has migrated to inversion (Cluster B), and even C1's correlation stress-test and C2's portfolio depend on how well each sim inverts reality.

> [!tip] Sim Fidelity Is Not Transfer Quality — the Proxy You Optimize Is *Anti-Correlated* With the Goal
> This is the sharpest contrarian result in the doc, and it ties A3, B2, and C1 to one claim: **optimizing fidelity actively destroys transfer.** A3's [[2604.02523|Tune to Learn]] is the cleanest case — the controller gains with the *lowest* system-identification error produce the *worst* sim-to-real transfer, so minimizing the standard sysID objective moves you away from the goal. B2's [[2510.11689|Phys2Real]] shows the same inversion for randomization — DR's distribution-*marginalizing* fidelity reaches only 23% on OOD mass while *estimating* the single true parameter hits 57%, so averaging over the physics you could have identified is strictly worse. C1's [[2502.10694|UDA Simulation Study]] names the failure outright as "negative adaptation" — under shift, the adaptation that should help can do *worse than no adaptation*, flipping the sign of the relationship. The cross-cutting lesson is not the mild "fidelity is a confounded surrogate" — it is the strong claim that **the realism you optimize is, on these axes, negatively coupled to the transfer you actually want; measure transfer directly, because the proxy points the wrong way.**

> [!tip] Sim-to-Real Evaluation Is Becoming Statistical Inference, Not Accuracy Engineering
> C1 and C2 form one diagnose-and-route → infer pipeline, and B3 inherits the reframing for data. C1 *diagnoses and routes* — it shows in-distribution r ([[2405.05941|SIMPLER]] >0.85, [[2605.06311|VISER]] 0.92) is a validity artifact that must be re-measured per factor under shift, then turns the per-factor result into a deployment gate that routes which biased sim to trust per perturbation. C2 *infers* — [[2604.24018|Sim2Real Betting]] (70–100% win rate) and [[2510.04354|SureSim]] (provable CIs, 20–25% fewer real trials) extract provable real bounds from *imperfect* sims by treating estimation as variance reduction, consuming C1's per-factor weights. The question shifts from "how accurate is my sim?" to "is this correlation valid and which sim do I deploy per factor (C1), and what can I provably infer from it (C2)?" — and B3's twin becomes a data engine under the same inference logic.

> [!tip] Differentiable Rendering + Physics Collapse System-ID Into Gradient Descent
> A1, B1, B2, and B4 all ride the same capability: appearance and dynamics are now recovered end-to-end by gradient, not hand-tuning. [[2503.17973|PhysTwin]] and [[2511.04665|Real-to-Sim GS]] jointly optimize geometry + physical parameters + appearance from video; B2's [[2604.27367|DOT-Sim]] makes the optical-tactile simulator differentiable and calibrates constitutive parameters from few demos; [[2510.11689|Phys2Real]] fuses VLM priors with online estimation; B4's [[2304.14369|NCLaw]] pushes the same differentiable-MPM machinery one level deeper, learning the constitutive *law* rather than its parameters. A1's neural-rendering-in-the-loop, B1's joint reconstruction, B2's differentiable sysID, and B4's learned-law inversion are four faces of the same collapse — manual sysID is being replaced by differentiable recovery of $\phi$, $\psi$, and now the functional form of the dynamics itself, and D2 reuses the same differentiable machinery for exact-gradient test-time adaptation.

> [!tip] The Reality Gap Has a Temporal Axis — Train, Reconstruct, Measure, Deploy, Bound
> The five clusters are not parallel attacks on one gap; they are ordered in *time* by when each acts, and A through E pass the residual down a pipeline. A1–A3 act at **train-time** (robustify the policy before deployment); B1–B4 act at **reconstruct-time** (invert reality into the simulator offline); C1–C2 act at **measure-time** (infer what the gap is and where each sim is trustworthy); D1–D3 act at **deploy-time** (close the residual the first three leave behind, online on hardware — [[2107.04034|RMA]] infers extrinsics, [[2508.21065|Learning on the Fly]] adapts by differentiable TTA, [[2602.20057|AdaWorldPolicy]] corrects by world-model supervision); E1–E3 act at **deploy-time under a safety constraint** (bound the residual that adaptation cannot remove). Each cluster's output is the next's input: B's reconstruction feeds C's measurement and D's adaptation; C1's trust map routes the sims D and E rely on; D's online updates are exactly what E1's [[2503.10949|SCDA]] and E2's [[2409.19190|RAIL]] must keep safe. The residual gap is not eliminated — it is moved down the timeline until only a *bounded* remainder reaches the user.

> [!tip] An Un-Handled Residual Gap Is a Safety Failure, Not Just a Performance Loss
> Cluster E reframes what C measures: the residual gap that survives A/B/C/D is not merely lost success — at deploy-time it is a *risk surface*. E1, E2, and E3 are the three ways to bound it. E1's [[2503.10949|SCDA]] constrains the *adaptation* (zero safety violations while D1/D3's online updates run, 20%→60% real grasp SR); E2's [[2409.19190|RAIL]] bounds the *action* (0% collisions vs 5–35% unshielded, ~10-pp SR cost: 68% vs 78%); E3's [[2506.09937|SAFE]] and [[2503.08558|FAIL-Detect]] flag the *failure* the other two can't rule out (<1 ms overhead, ~78%/72% detection, no failure labels). All three convert C1's per-factor untrustworthiness into a runtime guarantee — and crucially, each provides safety *without* failure-labeled data or a hand-crafted dense reward, because the sim2real failures you can label are not the ones the residual gap produces.

> [!tip] Online Adaptation Beats Robustification When Deployment Leaves the Randomization Range
> D1, D2, and D3 share one bet against Cluster A's train-time orthodoxy: a policy that *infers-then-conditions* on the true deployment dynamics beats one that *marginalizes* over them by domain randomization, precisely when deployment falls outside the train-time range. [[2107.04034|RMA]] proves it in locomotion (zero-real-fine-tune across sand/mud/12 kg payload); [[2409.16578|FLaRe]] in manipulation (+30.7% real SR from adapting, not robustifying); [[2508.21065|Learning on the Fly]] in aerial control (81% hover-error reduction in 3 gradient steps); [[2602.20057|AdaWorldPolicy]] with no real reward at all (0.96 [[2306.03310|LIBERO]]-10 under OOD via prediction-error supervision). The three split by which model is on hand — privileged extrinsics (D1), an analytical differentiable model (D2), or only a learned world model (D3) — but the common engine is a deploy-time signal that observes the latent the train-time policy could only guess at. This is the same estimation-over-marginalization principle B2/C2 apply offline, now running online on hardware.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| *Per-episode in-loop* affordance/material semantic randomization vs *fixed-cousin* asset-level semantic randomization, and vs appearance-only DR | A1 | [[2410.07408\|Digital Cousins]] (asset-level semantic cousins, 90% vs 25%, fixed per scene) + [[2604.11674\|AffordSim]] (~24%-avg zero-shot ceiling) + [[2604.25459\|GS-Playground]] (in-loop 3DGS, semantics-agnostic) |
| Physics-*law*-grounded (distribution-free) reward retention across contact-dynamics shift vs a *learned* transferable reward (and action transfer) | A2 | [[2604.23702\|QuietWalk]] (PINN-force reward, R²=0.99, single robot) + [[2405.19988\|Video-Language Critic]] (learned transferable reward, distribution-bound) + [[2511.15200\|VIRAL]] (action transfer) |
| Gain×dynamics *interaction term* via co-optimization (super-additivity) + co-optimized DR-variable beating a *runtime* adaptive-gain residual | A3 | [[2604.02523\|Tune to Learn]] (gains-vs-sysID finding, no co-optimization) + [[2505.00991\|DexCtrl]] (runtime adaptive gains beat fixed, the H4 alternative) |
| *Monotone* reconstruction-fidelity → forward-correlation law across rigid/articulated/deformable (where the navigation counter-example does not reach) | B1 | [[2511.04665\|Real-to-Sim GS]] (joint inversion, push-T r=0.915 / rope 0.901 vs [[2511.04831\|Isaac Lab]] 0.649 / 0.237) + [[2207.10821\|Lower-Fidelity Sim2Real]] (lower fidelity → higher transfer in navigation — non-monotone) |
| Amortized observation→parameter sysID for *unseen objects in clutter at zero per-object demos* vs per-object gradient sysID, on the SR-vs-parameter-distance OOD frontier | B2 | [[2603.01151\|D-REX]] (per-object gradient mass recovery, 86% SR, beats DR off-support, but ≥20 demos/object) + [[2506.10133\|Offline Domain Randomization]] (DR-as-estimation, the amortization substrate) |
| *Fidelity-gated* per-task fold-back loop that is monotone across rounds (drift control) + reconstruction-fidelity exchange rate, vs a single feedback pass | B3 | [[2512.00076\|Arcadia]] (closed lifecycle, single feedback-on/off pass, scene-level) + [[2403.03949\|RialTo]] (90% vs 10% target-twin, open-loop) |
| Learned constitutive *law* beating a parameter fit on *unseen geometry* (the delta MASIV's material-type recovery skips) + surviving a *closed robot* real→sim→real loop | B4 | [[2508.01112\|MASIV]] (material-agnostic learned-law recovery, no geometry-extrap isolation, no robot loop) + [[2304.14369\|NCLaw]] (learned law, 1M particles) + [[2503.17973\|PhysTwin]] (parameter-only fit) |
| Per-factor *correlation* (not SR sensitivity) re-measured under OOD, routed as a per-(sim,factor) trust gate vs one global edge | C1 | [[2602.11337\|MolmoSpaces]] (per-factor SR sensitivity, high global R=0.96, no per-factor r, no router) + [[2402.08191\|THE COLOSSEUM]] (14-factor SR drop) + [[2604.24018\|Sim2Real Betting]] (aggregate-edge routing) |
| Bank *composition* — bias-diversity vs bias-count CI-tightening + the compute-budget crossover map (portfolio-vs-single is taken) | C2 | [[2506.20553\|Sim2Val]] (control-variates over biased sources, provable bound, fewer real samples) + [[2510.04354\|SureSim]] (PPI CIs, 20–25% fewer trials) |
| Continued latent-extrinsics inference *beating robust-fallback OUTSIDE the DR range* (the inverse of GRAM's give-up-OOD conclusion) | D1 | [[2412.04323\|GRAM]] (same architecture, but falls back to a robust latent OOD on a real quadruped) + [[2107.04034\|RMA]] (zero-fine-tune in-range baseline) |
| *Learned-residual* BPTT adapting a *learned neural* policy on a disturbance the residual captures, vs M-GAPS's analytical-only gradient route | D2 | [[2507.10914\|M-GAPS]] (analytical-controller online gradient, beats RL on data-efficiency, no learned residual / no neural policy) + [[2508.21065\|Learning on the Fly]] (learned-residual BPTT, 81% hover-error, 3-step) |
| *Real-robot* 4 Hz unified-WM+force prediction-error correction with a *force*-prediction-error term for contact OOD, vs an image-foresight-only head | D3 | [[2605.08215\|T3VF]] (sim/image-foresight prediction-error + adaptive filter, no force term, no real-robot 4 Hz) + [[2602.20057\|AdaWorldPolicy]] (0.96 [[2306.03310\|LIBERO]]-10, 4 Hz real, unified WM+force DiT) |
| Zero-violation continual-adaptation constraint *wrapping an arbitrary Cluster-D engine* on real hardware across successive domains (composition, not isolation) | E1 | [[2604.19737\|Safe Continual RL (NSCMDP)]] (online-EWC violates, CPO forgets — measured, but isolated/control-bench) + [[2503.10949\|SCDA]] (20%→60% at zero cost on its own grasp loop) |
| Hard reachability shield over a *changing* (online-adapting) policy mid-update + uncertainty-aware geometry (hard-vs-soft is taken) | E2 | [[2511.06385\|Path-Consistent Safety Filter]] (hard reachability over diffusion policy, +68% over CBF, real Franka — but static policy) + [[2505.00779\|Uncertainty Latent Safety Filter]] (fixed-geometry filter insufficient under the gap) |
| Detect-then-*act* loop that *preserves* the conformal FPR bound + cross-architecture transfer of internal-feature detectors (success-only detection is taken) | E3 | [[2510.09459\|FIPER]] (no-failure-data conformal, beats FAIL-Detect lineage — but flags, no closed loop) + [[2410.04640\|Sentinel]] (success-only root) + [[2506.09937\|SAFE]] (internal-feature, policy-internal) |

---

## Cross-References

- [[../../../Embodied-AI/14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]] — Reality-gap diagnostics, learned simulators, real2sim2real strategies, domain randomization (the deep-dive underpinning every cluster)
- [[../../../Embodied-AI/11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] — Physics priors, PINN-grounded learning, physical-consistency design space (anchors A2, B1, B2, B4)
- [[../../../Embodied-AI/09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]] — Tactile/force sensing + differentiable tactile sim (anchors A2's GRF reward, B2's [[2604.27367|DOT-Sim]])
- [[../../../Embodied-AI/13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]] — Online/continual adaptation and self-improving policies (anchors D1, D3, E1)
- [[../../../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Robotics & embodied-AI topic overview; canonical paper index
- [[../../../General/08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — Canonical survey + benchmark index
- [[../../../General/04_Reinforcement-Learning|04_Reinforcement-Learning]] — Online RL fine-tuning, safe RL, continual adaptation (anchors D1, D2, E1)
- [[../../../General/12_Diffusion-and-Generation|12_Diffusion-and-Generation]] — Diffusion/generative simulators + 3DGS rendering (anchors A1, B1's reconstruction)
- [[WAM|WAM]] — Sibling WAM mechanism; world-models-as-learned-simulators connect to this doc's B3 (twin co-training) and D2/D3 (world-model-supervised adaptation)
- [[Embodied-AI|Embodied-AI]] — Umbrella embodied-AI directions; its physics-consistency and world-model-as-simulator directions border this doc's Cluster B (real-to-sim grounding) and Cluster D (deploy-time adaptation)
- [[Whole-Body|Whole-Body]] — Sibling Whole-Body Coordination capability; owns force-adaptive whole-body deployment (its Cluster C) and human-motion retargeting (its Cluster D) that consume this doc's domain-randomization-vs-real-residual machinery
- [[Spatial-4D|Spatial-4D]] — Sibling geometry-native mechanism; its reconstruction-for-embodied-perception directions share B1's 3DGS/twin-fidelity substrate
