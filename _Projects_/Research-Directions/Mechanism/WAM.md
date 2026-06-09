---
title: "Promising Research Directions: World Action Models"
aliases:
  - "WAM Promising Directions"
  - "WAM Research Directions"
tags:
  - research-directions
  - WAM
  - embodied-AI
  - world-model
---

# Promising Research Directions: World Action Models

> [!abstract] Overview
> Seven World Action Model (WAM) research directions across two clusters — *Theory & Architecture* (A, three directions) and *Training & Grounding* (B, four directions). They are synthesized from 35 WAM/embodied surveys, ten Embodied-AI deep-dive readings, and the frontier methods that set each bet's bar ([[2605.20752|GaussianDream]], [[2605.06388|Semantic-LDM-WM]], [[2604.16484|DexWorldModel]], [[2604.01985|WAV]], [[2504.16680|RWM-U]], [[2606.02577|RoboDream]]).
>
> This doc covers WAM machinery only: the latent/representation and architecture choices (A), plus training-time grounding and calibration (B). Two related topics live elsewhere. The model-agnostic geometric representations — natively-4D imagination and persistent geometric memory, framed as representations any policy can reuse — live in [[Spatial-4D|Spatial-4D]] (Cluster C). Directions that span model families — joint WAM–policy co-evolution, physics checks, joint causal-consistency evaluation, real-time deployment, cross-embodiment transfer — live in the umbrella [[Embodied-AI|Embodied-AI]].
>
> Each direction carries a **first-principles framing** (problem / assumption broken / measurable bet) and a non-consensus thesis. Every metric anchor comes from a cited `_KnowledgeHub_/{ID}.md` note.

---

## Methodology

**Scope.** Corpus: 35 pure-WAM + adjacent surveys and ~70 WAM-method/benchmark papers from `_KnowledgeHub_/`, cross-checked against [[08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] and ten `Embodied-AI/` deep-dives. Method: survey-grounded ideation — surveys name open problems, benchmarks fix what's measurable, frontier methods fix what's achievable now. **De-duplication**: five directions the umbrella [[Embodied-AI|Embodied-AI]] already covers (B1, B3, C1, C3, D2 there) were removed — see Cross-References.

- **Survey enumeration**: scanned papers tagged `survey` together with each of `world-model`, `VLA`, `embodied-AI`, `robotics`, `physics-aware`, and `sim-to-real`, then pulled the open problems each survey names.
- **Deep-dive mining**: full reads of [[07_WAM|07_WAM]], [[08_Latent-World-Models|08_Latent-World-Models]], [[13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]], [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]], [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]]; 3+-way convergence seeded A1 (hybrid substrate), A2 (tactile), B1 (contact).
- **Closest-baseline anchoring**: each bet is pinned to the strongest paper it must beat — [[2604.16484|DexWorldModel]], [[2605.20752|GaussianDream]], [[2604.01985|WAV]], [[2504.16680|RWM-U]] set the bar for A1, B3.
- **Filter**: kept directions with 3–10 papers attacking them but no agreed-on fix; dropped the saturated ones (just add more compute) and the premature ones (hypothetical AGI); favored where two areas meet — tactile and WAM, contact and WAM, physics and WAM.
- **First-principles framing**: each direction states the problem's irreducible structure, the assumption it breaks, and the non-consensus bet.

---

## WAM Survey Landscape

| Survey | Sub-theme | Key open problems |
|---|---|---|
| [[2605.12090\|WAM Survey]] | A: Core WAM | Causal-consistency joint metrics; data-ecosystem mixing; WM-vs-action eval gap; tactile/force/acoustic extension; long-horizon drift; closed-loop latency |
| [[2605.00080\|WM Robot Learning Survey]] | A: Core WAM | Eval beyond visual fidelity; closed-loop vs open-loop; latent WM dominance; causal conditioning; failure-recovery datasets; cross-embodiment |
| [[2510.16732\|World Models for Embodied AI Survey]] | A: Core WAM | Unified datasets; physically-consistent metrics beyond FID/FVD; long-horizon temporal consistency; SSM/hybrid AR-global; WM × LLM-CoT synergy |
| [[2511.02097\|WM Manipulation Survey]] | A: Core WAM | Structured task-relevant representations; hierarchical architectures for long-horizon |
| [[2411.14499\|World Models Survey]] | A: Core WAM | Physical-rule adherence; standardized benchmarks; sim2real; ethics/safety; interactive 3D action-conditioned WMs |
| [[2604.16592\|Cognition WM Survey]] | A: Core WAM | Motivation + meta-cognition drastically under-developed; epistemic WMs over structured knowledge |
| [[2604.04707\|OpenWorldLib]] | A: Core WAM | Definition fragmentation; 3D geometric consistency under camera motion; modular pipeline composition |
| [[2602.01630\|Unified World Model Framework]] | A: Core WAM | Fragmentation; integrated module architecture; holistic understanding gap |
| [[2604.22748\|Agentic World Modeling Survey]] | A: Core WAM | Counterfactual reasoning; constraint adherence; autonomous self-revision (L3 Evolver); decision-centric metrics (ASR + COD) |
| [[2604.28185\|Visual Generation Survey]] | A: Core WAM | Five-level atomic-mapping→agentic-WM taxonomy; spatial reasoning + causal understanding gaps under stress test |
| [[2604.15395\|Foundation Models in Robotics Survey]] | A: Core WAM | Five-phase FM evolution; dataset/challenge mapping; design-learning-deployment integration |
| [[2506.20134\|3D World Models Survey]] | A: Core WAM | 3D spatial understanding under-developed |
| [[2503.04641\|Multimodal Generative Models Survey]] | A: Core WAM | Cross-modal dependency; sparse 4D integration; comprehensive simulators |
| [[2509.20021\|Embodied AI LLM-WM Survey]] | A: Core WAM | MLLM-WM unified architecture; integration patterns |
| [[2604.26509\|3D Generation for Embodied AI Survey]] | A: Core WAM | 3D-asset generation for simulation; geometric fidelity for robot learning |
| [[2503.21765\|Physics Cognition Survey]] | B: Physics-as-WAM | Sub-human physics (multi-object/fluid); limited physical coverage; computational inefficiency; sim2real; physics foundation + neuro-symbolic |
| [[2510.04978\|Physical AI Survey]] | B: Physics-as-WAM | Causal understanding missing; compositional/causal structure; hybrid Neural Physics |
| [[2501.10928\|Generative Physical AI Survey]] | B: Physics-as-WAM | Functional vs visual realism; physical plausibility metrics; material fidelity |
| [[2601.15533\|Actionable Simulators]] | B: Physics-as-WAM | Dynamical hallucinations; structured 4D interfaces; self-evolution; closed-loop decision-oriented eval |
| [[2601.07823\|Video Generation in Robotics Survey]] | B: Physics-as-WAM | Hallucinations + physics violations; uncertainty; long videos; compute; robotics-centric benchmarks |
| [[2604.04974\|Video-to-Control Survey]] | B: Video-as-WAM | Integration layer is critical gap; interface trade-offs; tracking-error; latent-action identifiability; pre-execution verification; tactile/force integration |
| [[2603.28489\|Video Gen as WM Survey]] | C: Eval & Deploy | Efficiency as prerequisite; distillation/sparse attention/quantization; integrated efficiency |
| [[2604.15911\|Efficient Video Diffusion Survey]] | C: Eval & Deploy | KV cache movement; 1–4 step distillation; sparse attention; QAT/PTQ |
| [[2602.04411\|Self-evolving Embodied AI]] | C: Eval & Deploy | "Human-crafted settings" limit; multi-timescale closed-loop co-evolution; integration of WM/memory/embodiment |
| [[2604.02029\|Latent Space Survey]] | C: Eval & Deploy | Evaluability/controllability/interpretability; theory gap; modality-native integration; governable latent AI |
| [[2504.21853\|Interactive Generative Video Survey]] | C: Eval & Deploy | Real-time vs quality; persistent memory; dynamics fidelity; cross-domain transferability |
| [[2507.00917\|Embodied Intelligence Survey]] | C: Eval & Deploy | Sim2Real gap; unified capability framework; WMs as neural simulators |
| [[2605.03941\|iWorld-Bench]] | C: Eval & Deploy | Standardized interactive evaluation across WAM types |
| [[2511.05936\|10 VLA Challenges]] | C: Eval & Deploy | OOD brittleness; data quality; resource efficiency; safety as 3 of 10 named bottlenecks |
| [[2604.23775\|VLA Safety Survey]] | C: Eval & Deploy | Threat taxonomy; adversarial/jailbreak robustness; safe-deployment mechanisms |
| [[2505.07634\|Neural Brain Framework]] | C: Eval & Deploy | Multimodal active sensing; closed-loop perception-cognition-action; neuroplasticity memory; neuromorphic co-design |
| [[2505.05108\|Multi-agent Embodied AI Survey]] | C: Eval & Deploy | Async decisions; heterogeneous teams; self-evolution in open environments; nascent benchmarks |
| [[2508.07407\|Self-Evolving AI Agents Survey]] | C: Eval & Deploy | Continuous self-improvement w/o forgetting; evolution-evaluation gap; safety + alignment under self-modification |
| [[2507.21046\|Self-Evolving Agents Survey]] | C: Eval & Deploy | Adaptivity / retention / generalization / efficiency / safety as 5 eval gaps; emergent risks |
| [[2310.06253\|Objective Mismatch MBRL Survey]] | C: Eval & Deploy | Decision-aware MBRL; predictive-loss vs return alignment; cross-family fragmentation |

> [!tip] Convergence patterns
> - **Joint WAM-action evaluation gap** (5-way): [[2605.12090|WAM Survey]], [[2605.00080|WM Robot Learning Survey]], [[2510.16732|World Models for Embodied AI Survey]], [[2601.15533|Actionable Simulators]], [[2601.07823|Video Generation in Robotics Survey]] — same diagnosis under different vocabulary (causal consistency / closed-loop / physically-consistent metrics). Now empirically confirmed by [[2604.19092|RoboWM-Bench]] (visual plausibility ≠ executability) and operationalized by [[2604.22152|dWorldEval]] (ρ ≈ 0.9–0.92 with real-fleet SR).
> - **Physical grounding / dynamical hallucinations** (5-way): [[2503.21765|Physics Cognition Survey]], [[2510.04978|Physical AI Survey]], [[2601.15533|Actionable Simulators]], [[2411.14499|World Models Survey]], [[2501.10928|Generative Physical AI Survey]] — converge on hybrid neural-symbolic + verifiable-physics. [[2605.08567|ACWM-Phys]] now quantifies the InD→OOD physical-generalization cliff; [[2603.19607|Physion-Eval]] shows 83% exo / 94% ego of generated videos carry physical glitches.
> - **Efficiency as deployment prerequisite** (3-way): [[2510.24795|Efficient VLA Survey]], [[2603.28489|Video Gen as WM Survey]], [[2604.15911|Efficient Video Diffusion Survey]] — KV-cache movement is the major DiT bottleneck; the 3–5 Hz AR ceiling is the quantitative anchor. [[2604.16484|DexWorldModel]]'s O(1) TTT memory + speculative async inference now attacks both levers at once.
> - **Runtime verification & WAM security** (4-way, *new this pass*): [[2604.04974|Video-to-Control Survey]] (pre-execution verification), [[2605.22446|Pre-VLA]] (preemptive action verification), [[2604.05498|JailWAM]] (84% attack success on WAMs), [[2604.23775|VLA Safety Survey]] — the field is converging on the realization that a WAM's *imagination is a safety surface*, not just a planning substrate, and must be verified before either execution or further rollout.
> - **Definition fragmentation** (meta): [[2604.04707|OpenWorldLib]], [[2510.16732|World Models for Embodied AI Survey]], [[2411.14499|World Models Survey]], [[2602.01630|Unified World Model Framework]] — field still pre-paradigmatic; empirical convergence outpaces terminology.

---

## Formal Framing

**Probabilistic** — [[2605.12090|WAM Survey]]:

> "WAMs are defined as embodied foundation models that integrate predictive state modeling with action generation, moving beyond merely predicting actions to predicting a joint distribution over future states and actions." — [[2605.12090|WAM Survey]]

$$\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o,l,o',a) \sim \mathcal{D}} \big[ -\log p(o', a \mid o, l) \big]$$

| Family | Joint distribution | Predicts |
|---|---|---|
| **VLA** | $p(a \mid o, l)$ | Action only; no dynamics |
| **WM** | $p(o' \mid o, a)$ | Dynamics only; no action |
| **WAM** | $p(o', a \mid o, l)$ | Both; the unifying frontier |

WAMs split into **Cascaded** (predict state, derive action via inverse dynamics) vs **Joint** (unified end-to-end). Most "joint" methods are really Cascaded; Joint is the architectural frontier (the joint-optimization question lives in the umbrella [[Embodied-AI|Embodied-AI]]). This doc keeps the WAM-internal *substrate* question: whatever the optimizer, the imagined state has to be represented somewhere, and that latent/architecture choice is what A1 attacks.

**Architectural** — [[2510.16732|World Models for Embodied AI Survey]]:

> "The world models are categorized along three axes: Functionality (Decision-Coupled vs General-Purpose), Temporal Modeling (Sequential Simulation vs Global Difference Prediction), and Spatial Representation (Global Latent Vector, Token Feature Sequence, Spatial Latent Grid, Decomposed Rendering Representation)." — [[2510.16732|World Models for Embodied AI Survey]]

Spatial axis trajectory: latent vectors → token sequences → explicit 3D rendering (NeRF, 3DGS). [[2605.20752|GaussianDream]] sits at the rendering end as a train-dense, inference-light hybrid (A1's substrate); [[2604.16484|DexWorldModel]] anchors the token-feature end on semantic [[2508.10104|DINOv3]] latents. The explicit-4D end ([[2604.26694|X-WAM]], a deploy-time 4D substrate) is owned by [[Spatial-4D|Spatial-4D]]-C3.

**Capability hierarchy** — [[2604.22748|Agentic World Modeling Survey]]:

> "We introduce three capability levels: L1 Predictor, which learns one-step local transition operators; L2 Simulator, which composes them into multi-step, action-conditioned rollouts that respect domain laws; and L3 Evolver, which autonomously revises its own model when predictions fail against new evidence." — [[2604.22748|Agentic World Modeling Survey]]

Physical-law L3 Evolver is "emerging not mature" — the target for B2's self-evolution loop. The survey's decision-centric metrics, ASR (Action Success Rate) + COD (Counterfactual Outcome Deviation), anchor the joint causal-consistency evaluation in the umbrella [[Embodied-AI|Embodied-AI]].

**Identifiability** — [[2605.26379|LeJEPA World Model]]:

> "[[2511.08544|LeJEPA]] achieves linear identifiability — recovering true latent variables up to an orthogonal transformation — if and only if the underlying latent variables follow an isotropic Gaussian distribution." — [[2605.26379|LeJEPA World Model]]

This gives A1's latent substrate a formal "when is a learned latent a world model?" test: identifiable iff isotropic-Gaussian, at which point latent-space planning matches an oracle controller (R² > 0.999 to 1024 dims).

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Theory & Architecture** | A1, A2, A3 | Right substrate for joint imagination + action | A1's hybrid latent+pixel/3DGS backbone is the deploy substrate; A2 extends it into tactile/force imagination; A3 fixes *what* A1's latent encodes (semantic / continuous-disentangled over reconstruction / VQ), so A1 chooses the density and A3 chooses the encoding on the same backbone; [[2605.26379\|LeJEPA World Model]]'s identifiability criterion governs A1's latent half and is A3's encoding-geometry target, and A2's wrench head is the modality A1's backbone does not yet imagine |
| **B — Training & Grounding** | B1, B2, B3, B4 | Imagination diverges from physical reality | B1's discrete contact-mode latent stabilizes B2's self-evolution in contact-rich regimes; B3's forward-inverse calibration is the train-time signal that keeps B2's imagined-vs-real ρ high; B4 turns the same imagination into a training corpus, and B3's physics calibration is what makes B4's synthesized demos executable rather than plausible-looking; [[2604.01985\|WAV]]'s asymmetry signal and [[2605.22446\|Pre-VLA]]'s runtime verifier are the trust valves all four share |

---

## Cluster A — WAM Theory & Architecture

*Latent representation + architecture choices that close the gap between dynamics prediction and action generation.*

### A1 — Hybrid Latent+Pixel WAM Architectures

| | |
|---|---|
| **Cluster** | A — Theory & Architecture |
| **Thesis** | The field treats latent-vs-pixel as a one-time binary that locks both training and inference. But training density and inference density are independent — nothing forces a model to predict at the same density it trains at. The bet: a hybrid backbone (dense pixel/3DGS supervision at train, latent rollout at deploy) reaches [[2605.20752\|GaussianDream]]-class real SR *and* keeps pure-latent OOD retention on [[2510.13626\|LIBERO-Plus]], at lower deploy latency than a pixel WAM. (Interpretability is a qualitative bonus — the dense branch is inspectable — not part of the measurable bet.) |
| **Anchor papers** | [[2510.16732\|World Models for Embodied AI Survey]], [[2511.02097\|WM Manipulation Survey]], [[2604.02029\|Latent Space Survey]], [[2605.20752\|GaussianDream]], [[2604.16484\|DexWorldModel]] |
| **Key targets** | Latent ~10 ms vs pixel ~150 ms inference; match [[2605.20752\|GaussianDream]]'s 98.4% [[2306.03310\|LIBERO]] / 34.4→50% real at lower deploy cost; [[2510.13626\|LIBERO-Plus]] OOD retention from dense co-training |

**Why it matters.** [[2510.16732|World Models for Embodied AI Survey]] tracks a trend from latent vectors → token sequences → explicit 3D rendering. Hybrids span multiple axis points and stay under-explored; single-paradigm WAMs hit the latency-vs-robustness or speed-vs-interpretability trade-off. [[07_WAM#6. Efficient & Action-Centered WAMs|07_WAM §6]] finds VideoGen 4.8× slower but most robust, latent fast but opaque. Two existence proofs show the hybrid recipe works. [[2605.20752|GaussianDream]] supervises a renderable 3D-Gaussian future at train time, then *drops the auxiliary heads at inference* (34.4→50% real, 531 ms/chunk). [[2604.16484|DexWorldModel]] uses semantic [[2508.10104|DINOv3]] latents as targets to separate interaction from visual noise (94% [[2504.13059|RoboTwin]], zero-shot sim-to-real). Both confirm: train on dense signal, deploy on a cheap representation.

**First-principles framing.**
- **First principle**: Train density and deploy density are independent. A model can learn from pixel/3DGS-dense signal yet act on latent-dense signal — like humans rehearsing in full detail but acting on compressed predictions.
- **Assumption being challenged**: That latent-vs-pixel is a one-time binary that locks both train and deploy, and hybrids are too complex. [[2605.20752|GaussianDream]] and [[2604.16484|DexWorldModel]] show a hybrid is one backbone with dense train-time heads dropped at deploy.
- **The bet**: A hybrid backbone reaches [[2605.20752|GaussianDream]]-class real SR *and* matches or beats pure-latent OOD retention on [[2510.13626|LIBERO-Plus]], at lower deploy latency than a pixel WAM — one measurable inequality, not a three-way tie. Interpretability (the dense branch stays inspectable) is a qualitative aside, not a falsifiable claim.

**Evidence.**
- [[2510.16732|World Models for Embodied AI Survey]]: "An evolutionary trend from compact global latent vector representations (e.g., RSSMs) towards token feature sequences (e.g., Transformers with LLMs) and explicit 3D rendering representations (e.g., NeRF, 3D Gaussian Splatting) is observed."
- [[2605.20752|GaussianDream]]: dense 3D-Gaussian supervision at train, heads discarded at inference; 98.4% [[2306.03310|LIBERO]], 34.4→50% real, 531 ms/chunk — the canonical train-dense/deploy-light hybrid.
- [[2604.16484|DexWorldModel]]: [[2508.10104|DINOv3]] semantic latents as targets separate interaction from visual noise; 94% [[2504.13059|RoboTwin]]; semantic-latent half of the axis.
- [[2605.06388|Semantic-LDM-WM]]: semantic latents beat reconstruction VAEs by +9.8 pp closed-loop, +13.6 pp OOD — encoding quality beats the latent-vs-pixel split.
- [[2606.03188|GeoSem-WAM]]: geometry + semantic supervision on train-time latent tokens, branches dropped at test; 98.55% [[2306.03310|LIBERO]], +6.6 pp real — train-dense/deploy-light on a second signal.
- [[2606.05979|WLA]]: AR backbone predicts next state as text intentions + latent actions, no test-time image gen; 56.5% RMBench SOTA, ~40 ms — one unified model.
- [[2606.05254|Flash-WAM]]: modality-aware distillation cuts a two-stage WAM 8.1 s → 348 ms (23×), keeping 81.41% [[2504.13059|RoboTwin]] of the 91.25% teacher — deploy-light without dropping the WM.
- [[08_Latent-World-Models#6. Open Problems|08_Latent-World-Models §6]] names interpretability + latent-pixel alignment as 2 of 4 open problems.

**Concrete research questions.**
1. **Q1 — Hybrid training, single-branch deployment.** Extend [[2603.16666|Fast-WAM]] / [[2605.20752|GaussianDream]]: joint pixel/3DGS + latent objectives at train, latent-only at deploy (~10 ms vs ~150 ms). Measure OOD retention from dense co-training.
2. **Q2 — Shared latent z across modalities.** Can [[2605.15153|Pelican-Unified]]'s shared z anchor a hybrid where imagination decodes to pixel/3DGS (interpretable) and action decodes to latent (fast)?
3. **Q3 — Process-adaptive gating beyond [[2605.10942|HarmoWAM]].** Gate latent-only (transit) vs pixel/3DGS-aided (interaction) based on contact prediction.
4. **Q4 — Semantic vs reconstruction latents under hybrid training.** Does [[2605.06388|Semantic-LDM-WM]] / [[2604.16484|DexWorldModel]]'s semantic-latent result persist when a dense pixel/3DGS branch supervises training?

**Related research papers.**
- [[2605.20752|GaussianDream]] — Feed-forward 3DGS WM; dense train, light deploy; 98.4% [[2306.03310|LIBERO]], 34.4→50% real; the train-dense/deploy-light exemplar.
- [[2604.16484|DexWorldModel]] — Causal latent WM on [[2508.10104|DINOv3]] targets; O(1) TTT memory; 94% [[2504.13059|RoboTwin]]; semantic-latent axis.
- [[2603.16666|Fast-WAM]] — Train video, test latent; drops WM at test, no test-time imagination.
- [[2605.10942|HarmoWAM]] — Dual experts + adaptive gating; 89% in-domain; both experts in latent.
- [[2602.10098|VLA-JEPA]] — Pure latent: 97.2% [[2306.03310|LIBERO]]; no pixel decoder for interpretation.
- [[2605.15153|Pelican-Unified]] — Shared latent z; 93.5% [[2504.13059|RoboTwin]]; pixel-side generator, deployment latency open.
- [[2511.08544|LeJEPA]] — Provable Euclidean latent geometry; pure latent, regularization anchor.
- [[2411.04983|DINO-WM]] — Frozen [[2304.07193|DINOv2]] + lightweight dynamics; no pixel verification.
- [[2605.00078|Being-H0.7]] — Dual-branch deployable+privileged; 3–4 ms/step; both branches latent.
- [[2606.05979|WLA]] — Unified world+language+action AR model; world prediction steers action with no test-time image gen; 56.5% RMBench SOTA, ~40 ms; train-dense/deploy-light exemplar.
- [[2606.03188|GeoSem-WAM]] — Geometry + semantic supervision on latent tokens, branches dropped at test; 98.55% [[2306.03310|LIBERO]], +6.6 pp real; second-signal train-dense/deploy-light proof.
- [[2606.05645|Discrete-WAM]] — World + policy in one shared *discrete* token space via discrete diffusion; 90.4 EPDMS NAVSIM-v2 (AV; cited for the mechanism only); the discrete-token substrate counterpoint.
- [[2606.01955|WALL-WM]] — Learning unit is action *events*, not fixed chunks; layer-coupled video-action denoiser; Task Progress 32.6→71.6; the representation-granularity axis.
- [[2606.02800|Cosmos 3]] — Omnimodal MoT WM (lang/img/video/audio/action) generating video + policy; 39.7% RoboLab, #1 RoboArena; the unified-generative-substrate end.
- [[2606.04130|CLAW (Latent Action WM)]] — Continuous latent-action WM from action-free video; adversarial regularization stops leakage/collapse; 7/10 visual-planning tasks; latent-action from unlabeled video.
- [[2605.28816|Gamma-World]] — Latent video-diffusion WM; Sparse Hub Attention (linear scaling) + KV-cached streaming; FVD 184.1 vs 333.8; the efficient real-time substrate.
- [[2605.21862|EvoScene-VLA]] — Latent scene interface co-denoised with the action chunk; geometric anchor + scene predictor *dropped at inference*; 88.5% RoboTwin (+2.4 pp), 42.0% real (+4.7 pp); train-dense/deploy-light.
- [[2602.11832|JEPA-VLA]] — Video-predictive embedding (V-JEPA 2) *is needed* for VLA; +7.4% [[2306.03310|LIBERO]] + better real robustness; dense predictive supervision transfers to a cheap policy.
- [[2603.14482|V-JEPA 2.1]] — Dense predictive loss + deep self-supervision on masked + unmasked tokens; RMSE 0.307 NYUv2 depth, +20% grasp, 10× faster nav; the dense train-time supervision A1 reuses.
- [[2606.04907|WAM-Nav]] — Asymmetric latent WAM co-modeling action trajectories + short-horizon latent visual foresight in one DiT; 50.2% image-goal SR, 0.26 s latency (nav; cited for the mechanism only); latent foresight without pixel rollout.
- [[2412.14803|VPP]] — Frozen SVD video predictor used as a single-forward-pass visual encoder feeding a DiffPolicy head, no test-time video gen; CALVIN ABC→D length 4.33 (+41.5% over GR-1); train-dense-video/deploy-light exemplar.
- [[2412.15109|Seer]] — Predictive IDM unifying conditional visual foresight + action under unidirectional attention so action tokens read predicted-future tokens; +13% LIBERO-LONG, +43% real; future-state prediction at train, action at deploy.
- [[2505.15659|FLARE]] — Aligns compact future latent representations (not pixels) + action-aware embedding + DiT policy, co-trained on action-free human video; +26% over baselines, 95% real at 100 traj/task; dense-latent supervision, no pixel decoder.
- [[2603.29409|CLaD]] — Predicts grounded proprioceptive + semantic future latents (asymmetric cross-attn) then conditions a diffusion policy; 94.7% LIBERO-LONG at 0.66B params, 25 Hz; latent-foresight train signal, fast deploy.
- [[2512.15692|mimic-video]] — Action decoder reads partially-denoised latent states from a Cosmos-Predict2 video backbone, no full video gen at test; 93.9% LIBERO, 10× sample efficiency; deploy-light read off a video backbone.
- [[2512.16023|CoVAR]] — Video + action co-generator: OpenSora video diffusion + parallel Action DiT coupled by Bridge Attention under multi-modal rectified flow; 1.000 CALVIN Drawer, 0.74 real UR5; the dual-branch co-generation point.

**Benchmarks & metrics.**
- [[2510.13626|LIBERO-Plus]] — 10,030 OOD perturbations; match pure-latent in-dist; gain OOD over latent-only.
- Inference latency (Hz) — A100 forward latency; latent ~10 ms vs pixel ~150 ms; [[2605.20752|GaussianDream]] 531 ms/chunk real-robot reference.
- [[2605.21800|stable-worldmodel]] — Reproducible OOD harness; [[2411.04983|DINO-WM]] 92% / [[2603.19312|LeWM]] 94% [[2109.00137|Push-T]], sharp planning decay under perturbation; substrate for the hybrid OOD claim.
- [[2603.22078|WAM vs VLA Robustness]] — 4.8× latency cost; hybrid must show <2× cost vs pure latent at pixel-WAM OOD.

> [!warning] Risks
> - **Two-branch training cost** dominates compute. → Mitigate by distilling a pre-trained pixel/3DGS WM into the latent encoder (the [[2605.20752|GaussianDream]] discard-at-inference pattern).
> - **Latent-pixel divergence** without shared parameters. → Need explicit alignment loss; [[2604.16484|DexWorldModel]]'s [[2508.10104|DINOv3]]-target anchoring is one recipe.
> - **Saturated regime**: pure latent already at 97% [[2306.03310|LIBERO]] and [[2605.20752|GaussianDream]] at 98.4%. → Contribution must show on OOD + interpretability + deploy-cost, not headline [[2306.03310|LIBERO]] SR.

### A2 — Tactile/Force-Integrated WAM Imagination

| | |
|---|---|
| **Cluster** | A — Theory & Architecture |
| **Thesis** | The field treats force as a policy *input* but never models it as an *output*, so WAMs imagine visual futures but not wrench futures. Yet in contact, force is the generative cause and vision the consequence — a WM that predicts only consequences is incomplete. The bet: a WAM that imagines wrench futures recovers ≥50% of the measured-tactile→no-tactile contact-task drop ([[2603.17851\|DexViTac]]'s 83.3%→43.3% pipetting ablation) even with no force sensors at deployment, approaching the with-real-tactile [[2603.17851\|DexViTac]] ceiling of 85.8%. |
| **Anchor papers** | [[2605.12090\|WAM Survey]], [[2511.02097\|WM Manipulation Survey]], [[2604.16592\|Cognition WM Survey]], [[2603.17851\|DexViTac]], [[2601.20321\|TaF-VLA]] |
| **Key targets** | Cross-sensor transfer >60.3% ([[2601.20321\|TaF-VLA]] baseline); recover ≥50% of [[2603.17851\|DexViTac]]'s measured-tactile→no-tactile drop (83.3%→43.3% pipetting ablation) using imagined rather than measured tactile; approach the [[2407.08028\|AutoMate]] no-WAM ceiling ([[2603.15956\|ExpertGen]] 90.5%) |

**Why it matters.** Current WAMs imagine visual + proprioceptive futures but rarely tactile/force futures, even though force is the dominant signal in contact-rich manipulation. [[2605.12090|WAM Survey]] names the modality gap; [[2511.02097|WM Manipulation Survey]]'s 13 capabilities rank Multimodal Perception first and Physics Awareness third. All existing tactile work consumes force as policy input, never imagines it as WAM output. The data bottleneck is now gone ([[2604.20444|VTouch++]], [[2603.17851|DexViTac]], [[2604.07335|TAMEn]]), so the modeling gap is exposed. The manipulation-task application of imagined tactile is [[Manipulation|Manipulation]]-B1.

**First-principles framing.**
- **First principle**: In contact, force is the *cause* and what you see is the effect — the object moves *because* of force. A WM that predicts only the effect, never the cause, can't fully pin down what happens.
- **Assumption being challenged**: That force can be fed in (as policy input) without being predicted (as WM output). That treats force as something you measure, not something the model forecasts, so the policy has to pick up the dynamics by itself. [[2603.17851|DexViTac]] shows tactile *can* be modeled, but stops at sensing it.
- **The bet**: A WAM that imagines wrench (force + torque) at train time beats a vision-only WAM on contact-task error — *even with no force sensors at deploy*, where the imagined wrench stands in for a force reading — at [[2603.17851|DexViTac]]-class contact-rich SR.

**Evidence.**
- [[2604.27621|Robot Learning from Human Videos Survey]] and [[2604.16592|Cognition WM Survey]] independently name tactile as the contact-grounding modality.
- The data bottleneck is now resolved: [[2604.20444|VTouch++]] (120K episodes, 1000+ hrs, 36M frames, synchronized vision+tactile+proprioception), [[2603.17851|DexViTac]] (visuo-tactile-kinematic, 85.8% SR, 248 demos/hr), [[2604.07335|TAMEn]] (closed-loop tactile + recovery data, 75% SR).
- All existing tactile work treats force as *policy input*, never *WAM imagined output*: [[2603.15169|ForceVLA2]], [[2601.20321|TaF-VLA]] (60.3% cross-sensor), [[2506.14754|Sparsh-X]] (encoder only), [[2603.15257|HapticVLA]] (distillation sidesteps the problem).
- **Tactile is modelable** — the precondition for the bet: [[2603.17851|DexViTac]]'s kinematics-grounded tactile pretraining resolves the semantic ambiguity of raw touch and reaches 85.8% contact-rich SR, with the pretraining ablation (pipetting 83.3%→43.3%) proving the tactile representation is load-bearing — so a WAM head that *imagines* that representation has a tractable target.

**Concrete research questions.**
1. **Q1 — Wrench-trajectory prediction head.** Add 6-DoF wrench head to a JEPA WAM; train on [[2506.14754|Sparsh-X]]'s 1M contacts and [[2604.20444|VTouch++]]'s 36M synchronized frames.
2. **Q2 — Tactile latent as cross-sensor bridge.** Use [[2601.20321|TaF-VLA]]'s VQ-VAE force latent (or [[2603.17851|DexViTac]]'s kinematics-grounded latent) as WAM imagination target; decode per-sensor on demand.
3. **Q3 — Imagined-vs-measured force as auxiliary loss.** Train-time supervised; deploy-time used as proprioceptive forecast.
4. **Q4 — Contact-event as discrete latent transition.** Make/break as categorical; continuous force only in contact regime (shared substrate with B1's discrete contact-mode latent).
5. **Q5 — Force-conditioned video prediction inverse.** Run [[2505.19386|Force Prompting]] backward: predict force from frames, condition next-step on predicted force.

**Related research papers.**
- [[2605.12090|WAM Survey]] — Names the modality gap; survey only, no method proposed.
- [[2604.20444|VTouch++]] — Bimanual vision+tactile+proprioception dataset (120K episodes); data substrate, no WAM consumer.
- [[2603.17851|DexViTac]] — Visuo-tactile-kinematic demos + kinematics-grounded tactile pretraining; 85.8% SR; perception, not imagination.
- [[2604.07335|TAMEn]] — Closed-loop tactile data + AR recovery; 75% SR; collection engine, no WAM prediction.
- [[2506.14754|Sparsh-X]] — Multisensory touch foundation (1M contacts); encoder only, no prediction head.
- [[2601.20321|TaF-VLA]] — VQ-VAE force latent; 60.3% cross-sensor; latent is policy-consumed, not WM-predicted.
- [[2603.15257|HapticVLA]] — Teacher-student tactile distillation; 86.7% SR; sensor-free deployment, force not modeled in WM.
- [[2603.15169|ForceVLA2]] — Cross-scale MoE + force prompts; 66% avg SR; force is policy input, not predicted output.
- [[2605.13083|TouchAnything]] — Multi-view egocentric + dense tactile; dataset only, no WAM consumer.
- [[2505.19386|Force Prompting]] — Force-conditioned video generation; generation side.
- [[2509.07962|TA-VLA]] — Torque-aware VLA design study; policy-side only.

**Benchmarks & metrics.**
- [[2510.25725|HumanoidVTA]] — 2,124-sensor humanoid tactile; substrate for imagined-vs-measured force.
- ForceVLA-Data (244 traj) — Contact-rich 5-task; test WAM imagination on existing force-aware benchmark.
- [[2407.08028|AutoMate]] assembly — 8 industrial tasks; [[2603.15956|ExpertGen]] 90.5%; contact-rich tasks where imagined force matters.

> [!warning] Risks
> - **Noise floor**: subtle slip / microvibration not in vision — imagined force may plateau below measured. → Bound the claim to regimes where force is vision-correlated; report the floor explicitly.
> - **Cross-sensor brittleness**: 60.3% zero-shot ([[2601.20321|TaF-VLA]]) is not deployment-ready. → Use [[2603.17851|DexViTac]]'s kinematics grounding to stabilize the cross-sensor latent.
> - **No published WAM with tactile prediction head** — genuinely unattacked. → Treat the prediction-head ablation (imagined vs no-tactile) as the first-paper deliverable.

### A3 — Latent-Encoding Quality for WAM Imagination

| | |
|---|---|
| **Cluster** | A — Theory & Architecture |
| **Thesis** | The field spends its effort on the latent-vs-pixel question and treats the encoder, once you go latent, as a detail. But the encoder's *training objective* is the bigger lever: a reconstruction VAE optimizes pixel fidelity, which the policy never uses, while a semantic or continuous-disentangled latent keeps the action-relevant structure the policy does use. The bet: at matched architecture and matched deploy cost, a semantic / continuous latent beats a reconstruction / VQ latent by ≥9.8 pp closed-loop SR and ≥13.6 pp OOD ([[2605.06388\|Semantic-LDM-WM]]'s measured margins), reproduced on a second backbone. |
| **Anchor papers** | [[2604.02029\|Latent Space Survey]], [[2511.02097\|WM Manipulation Survey]], [[2605.06388\|Semantic-LDM-WM]], [[2605.15725\|DiLA]], [[2604.16484\|DexWorldModel]] |
| **Key targets** | Match [[2605.06388\|Semantic-LDM-WM]]'s +9.8 pp closed-loop / +13.6 pp OOD margin of semantic over reconstruction; continuous bottleneck beats VQ/VAE on generation quality + training stability ([[2605.15725\|DiLA]]); hold the gain on [[2510.13626\|LIBERO-Plus]] OOD at fixed deploy latency |

**Why it matters.** A1 decides *how dense* the imagined state is at train vs deploy; A3 decides *what the latent encodes* once you commit to one. The two are orthogonal, and the second is the under-examined one. [[2604.02029|Latent Space Survey]] names evaluability and controllability of the latent as open; [[2511.02097|WM Manipulation Survey]] ranks structured task-relevant representation above raw capacity. The cleanest evidence is a controlled study: [[2605.06388|Semantic-LDM-WM]] holds the action-conditioned LDM fixed and swaps only the latent's training objective — reconstruction-aligned (SD3 VAE, VA-VAE) vs semantic-aligned (V-JEPA 2.1, Web-DINO, SigLIP 2) — and finds semantic latents lift VLA closed-loop SR by 9.8 pp and OOD by 13.6 pp, with a stronger IDM Pearson r, *even when reconstruction latents win on pixel fidelity*. Two more results sharpen the encoding axis. [[2605.15725|DiLA]] shows a *continuous* information bottleneck beats discrete VQ and variational VAE on both generation quality and training stability. [[2604.16484|DexWorldModel]] uses DINOv3 semantic targets so the latent separates interaction semantics from visual noise (94% [[2504.13059|RoboTwin]], zero-shot sim-to-real). The pattern: the latent's training objective, not its density, sets how useful imagination is for control.

**First-principles framing.**
- **First principle**: A policy consumes dynamics, not pixels. A latent trained to reconstruct appearance spends capacity on detail the controller discards; a latent trained to predict future semantics keeps exactly the action-relevant structure. What the encoder is *told to preserve* fixes a ceiling on downstream control that no amount of architecture downstream can lift.
- **Assumption being challenged**: That once you pick latent over pixel, the encoder is interchangeable — pick any pretrained VAE / VQ tokenizer and move on. [[2605.06388|Semantic-LDM-WM]] shows the encoder objective swings closed-loop SR more than most architecture changes do; [[2605.15725|DiLA]] shows the *type* of bottleneck (continuous vs VQ vs VAE) is itself load-bearing, not a free choice.
- **The bet**: At matched architecture and matched deploy latency, swapping a reconstruction / VQ latent for a semantic / continuous-disentangled latent yields ≥9.8 pp closed-loop SR and ≥13.6 pp OOD ([[2605.06388|Semantic-LDM-WM]]), and the continuous bottleneck beats VQ/VAE on generation quality + stability ([[2605.15725|DiLA]]) — reproduced on a second WAM backbone to show the lever is the encoding, not the paper.

**Evidence.**
- [[2605.06388|Semantic-LDM-WM]] — Controlled reconstruction-vs-semantic study at fixed architecture: semantic latents +9.8 pp closed-loop, +13.6 pp OOD, stronger IDM Pearson r; the headline encoding-quality result.
- [[2605.15725|DiLA]] — Continuous information bottleneck beats discrete VQ and variational VAE on generation quality + training stability; SSIM/LPIPS gains on SSv2 / RT-1; the encoding *type* matters.
- [[2604.16484|DexWorldModel]] — DINOv3 semantic targets separate interaction from visual noise; 94% [[2504.13059|RoboTwin]], zero-shot sim-to-real; causal-semantic latent as the encoding choice.
- [[2602.10102|VideoWorld 2]] — dLDM explicitly decouples action dynamics from visual appearance so the latent carries only task-relevant dynamics; 72.3% step-7 folding; disentangled-encoding evidence.
- [[2601.14354|VJEPA-Probabilistic]] — Variational predictive bottleneck + Bayesian Product-of-Experts holds signal R²>0.84 under a noisy-TV distractor where VAE/pixel-AR collapse to ~0.50; uncertainty-aware encoding that knows what to discard.

**Concrete research questions.**
1. **Q1 — Reproduce the encoding swing on a second backbone.** Re-run [[2605.06388|Semantic-LDM-WM]]'s reconstruction-vs-semantic swap on a non-LDM WAM ([[2602.10098|VLA-JEPA]] or [[2604.16484|DexWorldModel]]); does the +9.8 pp / +13.6 pp hold, isolating the encoding as the lever rather than the LDM?
2. **Q2 — Continuous vs discrete vs variational at matched dimension.** Hold latent dimension fixed and ablate [[2605.15725|DiLA]]'s continuous bottleneck vs a VQ tokenizer vs a VAE; measure closed-loop SR + training stability, not just SSIM/LPIPS.
3. **Q3 — Disentangled appearance/dynamics under action conditioning.** Does [[2602.10102|VideoWorld 2]]'s dynamics/appearance split survive action conditioning, and does keeping only the dynamics latent for the policy beat the entangled latent at fixed deploy cost?
4. **Q4 — Encoding quality × identifiability.** Test whether the latents that win control (semantic / continuous) are also the ones that pass [[2605.26379|LeJEPA World Model]]'s isotropic-Gaussian identifiability test — i.e., is encoding quality a proxy for the membership criterion?
5. **Q5 — Encoding choice under the hybrid (A1) training regime.** Does the semantic-latent advantage persist when a dense pixel/3DGS branch supervises training (A1's hybrid), or does dense pixel supervision wash out the encoding gap?

**Related research papers.**
- [[2605.06388|Semantic-LDM-WM]] — Reconstruction-vs-semantic controlled study; +9.8 pp closed-loop, +13.6 pp OOD; the encoding-quality exemplar; single-backbone only.
- [[2605.15725|DiLA]] — Disentangled latent-action WM; continuous bottleneck beats VQ/VAE on quality + stability; SSIM/LPIPS gains on SSv2 / RT-1; the bottleneck-type lever.
- [[2604.16484|DexWorldModel]] — Causal latent on DINOv3 semantic targets; 94% [[2504.13059|RoboTwin]], zero-shot sim-to-real; causal-semantic encoding choice.
- [[2602.10102|VideoWorld 2]] — dLDM decouples dynamics from appearance; pretrained VDM renders appearance, compact latent carries dynamics; 72.3% step-7 folding; disentangled-encoding axis.
- [[2601.14354|VJEPA-Probabilistic]] — Variational predictive bottleneck + Bayesian PoE; R²>0.84 under noisy-TV where VAE/pixel-AR hit ~0.50; uncertainty-aware encoding that discards nuisance.
- [[2602.10098|VLA-JEPA]] — Full JEPA latent stack: 97.2% [[2306.03310|LIBERO]], 79.5% [[2510.13626|LIBERO-Plus]] OOD; semantic-predictive latent that wins control, no reconstruction objective.
- [[2606.04130|CLAW (Latent Action WM)]] — Continuous latent-action from action-free video; adversarial regularization stops leakage/collapse; 7/10 visual-planning tasks; the regularized continuous-action encoding.
- [[2411.04983|DINO-WM]] — Frozen [[2304.07193|DINOv2]] features as the latent + lightweight dynamics; zero-shot planning; the frozen-semantic-feature encoding baseline.
- [[2511.08544|LeJEPA]] — Provably optimal isotropic-Gaussian embedding via SIGReg; the encoding-geometry criterion an encoding-quality study is judged against.

**Benchmarks & metrics.**
- [[2510.13626|LIBERO-Plus]] — 10,030 OOD perturbations; the OOD axis where [[2605.06388|Semantic-LDM-WM]]'s +13.6 pp semantic advantage must reproduce at matched architecture.
- IDM action recoverability (Pearson r) — how much action-relevant signal the latent retains; [[2605.06388|Semantic-LDM-WM]] reports semantic > reconstruction; the encoding-quality diagnostic before downstream SR.
- Generation quality (SSIM / LPIPS) at matched latent dimension — [[2605.15725|DiLA]]'s continuous bottleneck beats VQ/VAE on SSv2 / RT-1; controls that quality gains are not just architecture.
- Noisy-distractor signal R² — [[2601.14354|VJEPA-Probabilistic]] holds R²>0.84 where VAE/pixel-AR collapse to ~0.50; tests whether the encoding discards nuisance.

> [!warning] Risks
> - **Encoding gain is dataset-specific**: the +9.8 pp / +13.6 pp swing may not transfer off [[2605.06388|Semantic-LDM-WM]]'s Bridge-V2 setup. → Q1 reproduces on a second backbone + dataset before claiming the lever is general; report per-dataset deltas.
> - **Semantic latents need architectural adaptation**: high-dimensional SSL/VL latents historically destabilize diffusion training. → Reuse [[2605.06388|Semantic-LDM-WM]]'s wide-head DiT + S-VAE compression recipe rather than feeding raw high-dim latents.
> - **Encoding quality ≠ controllability**: a latent that recovers actions well may still be hard to plan in. → Pair the IDM-recoverability metric with closed-loop SR and [[2605.26379|LeJEPA World Model]]'s identifiability test, not action-recovery alone.

---

## Cluster B — WAM Training & Grounding

*Training-time objectives and grounding losses that keep imagination aligned with physical reality.*

### B1 — Contact-Aware WAM for Fine Manipulation

| | |
|---|---|
| **Cluster** | B — Training & Grounding |
| **Thesis** | The field tries to close the contact gap by scaling up smooth, continuous latents. But contact physics jumps sharply (slip-stick, friction-cone, normal-force singularities), so no amount of latent capacity reaches it. The bet: a *discrete* contact mode achieves >90.5% [[2407.08028\|AutoMate]] and sub-millimeter assembly that purely smooth WAMs cannot reach at any scale. |
| **Anchor papers** | [[2604.04974\|Video-to-Control Survey]], [[2510.04978\|Physical AI Survey]], [[2511.02097\|WM Manipulation Survey]], [[2604.16484\|DexWorldModel]], [[2604.27367\|DOT-Sim]] |
| **Key targets** | [[2407.08028\|AutoMate]] beyond 90.5% with contact-aware imagination; sub-millimeter assembly; beat [[2602.23253\|SPARR]]'s +74.5% relative SR improvement on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer |

**Why it matters.** Latent WAMs handle trajectories well but fail at insertion/assembly, because contact physics is locally non-smooth (make/break, slip, normal-force singularities). Three deep-dives converge ([[08_Latent-World-Models#6. Open Problems|08_Latent-World-Models §6]], [[11_Physics-Aware-Embodied-AI#8. Open Problems|11_Physics-Aware-Embodied-AI §8]], [[14_Sim-to-Real-Transfer#7. Open Problems|14_Sim-to-Real-Transfer §7]]): latent WAMs miss sub-millimeter contact, verifiable physics scales poorly to clutter, learned sims blur on contact. [[2604.16484|DexWorldModel]]'s causal latent ([[2508.10104|DINOv3]] semantic targets that separate interaction from appearance) is the closest substrate, but its contact transitions stay continuous.

**First-principles framing.**
- **First principle**: Contact physics jumps sharply — friction-cone boundaries, normal-force singularities, and slip-stick are abrupt, discrete state changes. The jumps are in the physics itself; a smooth latent can only represent them by splitting into discrete pieces internally.
- **Assumption being challenged**: That adding latent capacity (more dimensions, layers, or parameters) closes the contact gap. It never touches the *structural* jump — a smooth model trying to approximate a hard step gets exponentially more expensive right at the boundary. Even [[2604.16484|DexWorldModel]] keeps contact smooth.
- **The bet**: A discrete contact mode (no-contact, making, in-contact, breaking, slipping) and switch dynamics per mode hits >90.5% [[2407.08028|AutoMate]] (the best a contact-naive WAM reaches) and sub-millimeter assembly that purely smooth WAMs can't reach at any scale.

**Evidence.**
- "Learned sims blur on contact: [[2310.06114|UniSim]] and [[2501.03575|Cosmos]] produce stunning visuals but physical contact regions (collisions, friction transients) look implausible to robots." — [[14_Sim-to-Real-Transfer#7. Open Problems|14_Sim-to-Real-Transfer §7]]
- Closest substrates: [[2604.16484|DexWorldModel]] (causal latent, [[2508.10104|DINOv3]] targets, 94% [[2504.13059|RoboTwin]]; continuous contact); [[2503.17973|PhysTwin]] (deformable digital twin; no discrete events); [[2511.07416|PhysWorld]] (continuous physical WM; 82% real SR); [[2604.27367|DOT-Sim]] (differentiable optical tactile; contact ground truth but no WAM consumer).
- Pattern: [[2602.23253|SPARR]] 95–100% [[2407.08028|AutoMate]]; [[2603.15956|ExpertGen]] 90.5% [[2407.08028|AutoMate]]. All policy-side improvements; contact events as first-class WAM latent has not been explored.
- **Discrete-token world-policy is already viable** — the precedent that a *discrete* shared latent works for joint world + policy: [[2606.05645|Discrete-WAM]] runs world modeling and policy in one shared discrete token space via discrete diffusion (90.4 EPDMS NAVSIM-v2). It is AV-domain, where the discrete tokens are scene/maneuver units, not contact modes — so it proves the discrete substrate is trainable and stable, but whether discrete tokens transfer to make/break/slip *contact* modes is exactly B1's open question.
- **Contact ground truth is now simulable** — the supervision the discrete modes need: [[2604.27367|DOT-Sim]]'s differentiable MPM tactile sim calibrates soft-sensor physics from a few real demos and transfers zero-shot (96.55% tumor detection, 0.896 mm trajectory error), giving make/break/slip labels a smooth-latent WAM can't manufacture for itself — the distillation teacher Q4 draws on.

**Concrete research questions.**
1. **Q1 — Discrete contact-mode latent** $c_t \in \{\text{no-contact, making, in-contact, breaking, slipping}\}$; predict $c_t$; condition continuous latent dynamics on $c_t$ atop a [[2604.16484|DexWorldModel]]-style causal latent.
2. **Q2 — Contact-mode-conditional physics losses**: Coulomb only in `in-contact`; ballistic only in `no-contact`.
3. **Q3 — Contact-event time prediction** as auxiliary regression head $\hat{t}_{\text{contact}}$ with simulator supervision.
4. **Q4 — Distillation from [[2604.27367|DOT-Sim]]** as teacher; distill contact dynamics into WAM latent.
5. **Q5 — Sim-to-real on [[2407.08028|AutoMate]] / [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic)**: train on [[2511.04665|Real-to-Sim GS]] twins; eval on real [[2407.08028|AutoMate]].

**Related research papers.**
- [[2604.16484|DexWorldModel]] — Causal latent WM ([[2508.10104|DINOv3]] targets); 94% [[2504.13059|RoboTwin]], zero-shot sim2real; continuous contact, no discrete mode.
- [[2503.17973|PhysTwin]] — Physics-informed deformable twin from video; no discrete contact mode.
- [[2511.07416|PhysWorld]] — Policy vs learned physical WM; 82% real SR; continuous, no event discretization.
- [[2604.27367|DOT-Sim]] — Differentiable MPM + tactile; 96.55% tumor detection zero-shot; no WAM consumer.
- [[2603.15956|ExpertGen]] — Generative prior + [[2506.15799|DSRL]] + distillation; 90.5% [[2407.08028|AutoMate]]; policy-side.
- [[2602.23253|SPARR]] — Sim + vision-conditioned real residual; 95–100% [[2407.08028|AutoMate]]; policy-side, no WAM.
- [[2603.16861|MolmoBot]] — 232K-env procedural [MuJoCo](https://github.com/google-deepmind/mujoco); 79.2% real [Franka FR3](https://franka.de/franka-research-3); domain randomization only.
- [[2511.04665|Real-to-Sim GS]] — 3DGS + soft-body [[2503.17973|PhysTwin]]; r=0.915 (push-T) / 0.901 (rope) sim-real; evaluation substrate.
- [[2604.24916|asRoBallet]] — Friction-aware [MuJoCo](https://github.com/google-deepmind/mujoco) + RL; prior for contact-mode losses.
- [[2604.23702|QuietWalk]] — PINN GRF predictor + curriculum; analog of contact-force prediction.
- [[2512.13644|DexWM]] — Diffusion-transformer WM on frozen DINOv2 + 3D hand-keypoint actions + hand-consistency loss; 83% zero-shot real Franka+Allegro grasping, 0 real training data; contact-rich dexterous WM, but continuous contact.
- [[2503.16806|DyWA]] — Dynamics-adaptive WAM jointly predicting actions + future object states from single-view point cloud, with a FiLM dynamics-adaptation module inferring physical properties; +31.5% SR, 68% zero-shot real across friction levels; adapts contact dynamics but stays continuous.

**Benchmarks & metrics.**
- [[2407.08028|AutoMate]] (8 tasks) — Insertion / assembly SR; 90.5% is the WAM-naive baseline.
- [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) industrial assembly — Cross-task assembly; [[2602.23253|SPARR]] reports +74.5% relative SR and 36.5% cycle-time cut on unseen tasks.
- [[2511.04665|Real-to-Sim GS]] deformable — Plush packing, rope routing, T-block pushing; soft-body contact where latent WAMs fail hardest.
- Contact-mode classification accuracy — $c_t$ vs simulator; internal diagnostic before downstream gains.

> [!warning] Risks
> - **Discrete latent optimization**: Gumbel-softmax / REINFORCE variance. → Start soft, harden over training (annealed temperature).
> - **Contact-mode supervision requires simulator**: real labels not available. → Distill from [[2604.27367|DOT-Sim]] / [[2511.04665|Real-to-Sim GS]] twins where contact ground truth exists.
> - **No published WAM with discrete contact-event latent** — genuinely unattacked. → Q1 contact-mode classification accuracy is the first internal milestone before downstream gains.

### B2 — WAM-Driven Self-Evolution & Recovery

| | |
|---|---|
| **Cluster** | B — Training & Grounding |
| **Thesis** | The field assumes self-evolution needs real-world exploration. But an agent's reachable competence is bounded by the failures its WM can *generate*, not by how much real interaction it logs — so imagined rehearsal is not strictly inferior to real experience. The bet: a closed failure-finder→imagine→GRPO→recover loop yields per-cycle SR gains at imagined-vs-real ρ > 0.7, with forgetting held to WMAR-class 0.071. |
| **Anchor papers** | [[2604.22748\|Agentic World Modeling Survey]], [[2602.04411\|Self-evolving Embodied AI]], [[2508.07407\|Self-Evolving AI Agents Survey]], [[2603.08403\|SPIRAL]], [[2605.22446\|Pre-VLA]] |
| **Key targets** | Imagined-vs-real SR Pearson ρ > 0.7 + continual per-cycle SR improvement; [[2605.22446\|Pre-VLA]]-style verifier ≥0.83 F1 on bad-rollout filtering; forgetting held to [[2401.16650\|WMAR]]-class 0.071 (vs 0.665 baseline) |

**Why it matters.** [[2604.22748|Agentic World Modeling Survey]] defines L1 Predictor / L2 Simulator / L3 Evolver and calls physical L3 Evolver the gap ("emerging not mature"). The pieces exist — failure detection, GRPO, recovery, memory, and now runtime rollout verification ([[2605.22446|Pre-VLA]], which filters unsafe actions and *truncates unreliable WM imaginations*) — but no system integrates them under a WAM-driven imagination loop. The newly exposed piece: imagination is also a *safety surface* ([[2604.05498|JailWAM]]: 84% attack success on WAMs), so the loop must verify its own dreams, not just learn from them. **Boundary vs the umbrella's B2:** this direction owns the WAM-imagination-driven failure *generation* half — using the WAM to dream the failures the recovery policy trains on — while the memory-integrated recovery half (long-horizon memory consult, cross-task retention) lives in the umbrella [[Embodied-AI|Embodied-AI]]; the two compose but are scoped apart to avoid dup.

**First-principles framing.**
- **First principle**: How well an agent prepares is limited by what it can imagine. An agent only learns to recover from failures it can generate for itself, because the recovery policy trains on the failures it sees. So a self-improvement loop is capped by how widely the WM can *imagine* failure, not by how much real interaction it logs.
- **Assumption being challenged**: That self-evolution needs real exploration because real experience beats imagined. Real failure-finding is costly and can't be undone (robot time, safety). A good-enough WAM can drive real improvement from imagined failures with only *occasional* real-world checking — as long as a verifier ([[2605.22446|Pre-VLA]]) screens out bad dreams.
- **The bet**: A closed loop — failure-finder → WAM imagines failure → GRPO over (action, imagination) → recovery — gives steady per-cycle SR gains, with imagined and real success rates correlating above 0.7 (Pearson ρ), *without* forgetting ([[2401.16650|WMAR]]-style FIFO + reservoir, +0.071 vs 0.665).

**Evidence.**
- [[2602.04411|Self-evolving Embodied AI]]'s 5-module framework (memory / task / environment / embodiment / model) is canonical; [[2508.07407|Self-Evolving AI Agents Survey]], [[2507.21046|Self-Evolving Agents Survey]], [[2505.05108|Multi-agent Embodied AI Survey]] all name open-environment self-evolution as the top unresolved capability.
- 2026 components: [[2603.08403|SPIRAL]] (closed-loop think-act-reflect over an Action-Conditioned WM; CriticAgent filters dreams, GRPO internalizes the reflection), [[2502.05907|EvoAgent]] (+105% [Minecraft](https://www.minecraft.net/en-us)), [[2511.16166|EvoVLA]] (first end-to-end self-evolving VLA), [[2510.16079|EVOLVER]] (trajectory → principles), [[2604.18131|Native Evolution]] (reward-free self-evolution), [[2605.22446|Pre-VLA]] (preemptive verifier that truncates unreliable WM imaginations; +6.83 pp [[2306.03310|LIBERO]]).
- **Closest existence proof for the loop**: [[2603.08403|SPIRAL]] already closes a think-act-reflect cycle — a PlanAgent decomposes goals, an Action-Conditioned WM imagines, and a CriticAgent verifies and feeds GRPO that *internalizes* the reflection (58.72% EgoPlan-Bench, +3.94 pp over GPT-5.1) — showing the imagine→verify→GRPO spine works, but it self-improves *generation* fidelity rather than driving detect→recover.
- The gap: **none integrates detection + diagnosis + recovery + memory + WAM-driven imagination + rollout verification end-to-end** under the L3 Evolver framing.

**Concrete research questions.**
1. **Q1 — WAM-driven failure-finder.** Recast [[2412.02818|RoboMD]] as adversary; failure-finder proposes initial states; WAM rolls forward; policy judged on imagined outcomes.
2. **Q2 — GRPO over joint (action, imagination) log-prob.** The single-loop joint optimizer (developed in the umbrella [[Embodied-AI|Embodied-AI]]) provides the inner step; B2 wraps it in the outer self-evolution loop. Reward = task SR in imagination + COD + [[2509.15194|EVOL-RL]] novelty.
3. **Q3 — Recovery via WAM-imagined alternatives.** On [[2510.09459|FIPER]] / [[2506.09937|SAFE]] detection, WAM dreams N candidates; [[2605.22446|Pre-VLA]] verifier filters unreliable ones; pick highest imagined SR.
4. **Q4 — [[2509.26354|Misevolution]] prevention**: [[2506.07468|SELF-REDTEAM]] in imagination; [[2509.15194|EVOL-RL]] for entropy collapse; [[2604.05498|JailWAM]]-style red-team probe each cycle.
5. **Q5 — Continual update from recoveries**: [[2401.16650|WMAR]]-style FIFO + reservoir; +0.071 vs 0.665 baseline forgetting.

**Related research papers.**
- [[2604.22748|Agentic World Modeling Survey]] — L1/L2/L3 framework; physical L3 emerging not mature; survey only.
- [[2605.22446|Pre-VLA]] — Preemptive runtime verifier; filters bad actions + truncates unreliable WM imaginations; +6.83 pp [[2306.03310|LIBERO]]; verification only.
- [[2502.05907|EvoAgent]] — Continual WM; +105% [Minecraft](https://www.minecraft.net/en-us); [Minecraft](https://www.minecraft.net/en-us)-only, no physical manipulation.
- [[2603.08403|SPIRAL]] — Closed-loop think-act-reflect (PlanAgent + Action-Conditioned WM + CriticAgent) self-improves the WM via GRPO; 58.72% EgoPlan-Bench; closest precedent, but improves *generation* fidelity, not detect→recover.
- [[2603.13528|Counterfactual Failure Synthesis]] — Dream2Fix perturbs actions in a generative WM for *counterfactual failures* + recovery labels (58.1% kept, 120K pairs); 46% real / 40% OpenVLA recovery; imagine-then-recover, but offline.
- [[2606.05395|VASO]] — Formal-verification counterexamples as "textual gradients" refine self-evolving skills; 89→97% feasibility, ~95% safety; formal-verifier-in-the-loop variant (skill-level LTL, no WM imagination).
- [[2511.16166|EvoVLA]] — First end-to-end self-evolving VLA; no WAM imagination driving evolution.
- [[2510.16079|EVOLVER]] — Trajectory → strategic principles; behavior-level, no WAM imagination.
- [[2412.02818|RoboMD]] — RL adversary for failure discovery; probes real robot, not WAM-driven.
- [[2510.09459|FIPER]] — Predictive failure via OOD + uncertainty; detection only, no recovery.
- [[2506.09937|SAFE]] — Internal-feature + conformal prediction; detection only, no recovery.
- [[2509.26354|Misevolution]] — Identifies the risk class; diagnosis only, no in-loop mitigation.
- [[2506.07468|SELF-REDTEAM]] — Adversarial self-play; pre-deployment check, not in-loop.
- [[2509.15194|EVOL-RL]] — Novelty prevents entropy collapse; standalone regularizer, not in-loop.
- [[2606.05773|PiL-World]] — Chunk-wise closed-loop policy-in-the-loop WM; imagined-vs-real gap 63.2→12.0%, Pearson r 0.94; supplies the ρ stop-condition, but evaluates rather than recovers.
- [[2606.03385|GTP-FA]] — Closed-loop execute-diagnose-update with a Failure Attribution Discriminator; +54.0 pp terminal SR ManiSkill3, real Franka π0.5 11.2→76.8%; the detect→diagnose→recover loop B2 wraps.
- [[2509.04018|FPC-VLA]] — Dual-model VLA + VLM supervisor: failure prediction + corrective action generation; 86.0% real SR, disturbance drop 31.3→16%; the recovery half of the loop.
- [[2603.17808|EVA]] — GRPO post-training aligns a video WM with executability via a pretrained IDM dense reward; kinematic plausibility +20.9% (→91.4%), 52.6% sim / 64.0% real; RL-on-imagination inner step.
- [[2509.19080|World4RL]] — PPO inside imagined rollouts of a frozen diffusion transition WM; 67.5% MetaWorld, 93.3% real Franka (+25 pp over BC); diffusion-WM imagination is sharper than RSSM rollouts.
- [[2605.13775|RoboEvolve]] — Planner+simulator co-evolution ("daytime explore / nighttime consolidate") learning from near-miss failures; +36.4 abs pts EB-ALFRED from 300 unlabeled seeds vs SFT on 25K; the simulator-driven co-evolution outer loop.
- [[2602.21633|SC-VLA]] — Sparse World Imagination (short-horizon physical-state prediction) + Online Action Refinement via residual RL on intrinsic dense rewards; 86% ManiSkill3, 71% real ARX5; imagination-driven recovery from self-predicted error.
- [[2509.15155|Self-Improving EFM]] — Online RL using a self-predicted steps-to-go signal as reward, no oracle labels; real LanguageTable 62→88%, 10% demos + 1% interaction beats 80%-data BC; the no-oracle self-improvement signal.
- [[2510.01642|FailSafe]] — Auto-generates verified failure→7-DoF recovery pairs by perturbing successful trajectories; FailSafe-VLM 0.91 detect SR, lifts OpenVLA +22.6%; the failure-recovery data pipeline the loop consumes.
- [[2606.03598|PHASER]] — Phase-aware semantic experience replay with interference-aware routing for continual VLA; +31% ASR over standard replay, 85.8% LIBERO-Long; the forgetting lever for per-cycle recovery updates.
- [[2603.25685|Persistent Robot World Models]] — RL post-training (reward-contrasted denoising + autoregressive protocol) fixes exposure bias in video-WM rollouts; +4.09 dB PSNR external cams, 80% human-preferred, stable to 11 s; keeps imagined rollouts trustworthy across cycles.

**Benchmarks & metrics.**
- [[2605.10921|RoboMemArena]] — Memory-dependent SR; 68.9% subtasks need history; recovery must consult memory.
- Continual improvement curves — per-cycle SR; per [[2507.21046|Self-Evolving Agents Survey]] rubric.
- Catastrophic forgetting probes — SR retention across sequential tasks; [[2401.16650|WMAR]] +0.071 vs 0.665 baseline.
- WAM-imagined-vs-real SR Pearson $\rho$ — predictive validity; validates loop is grounded; [[2605.22446|Pre-VLA]] verifier F1 ≥0.83 as the rollout-filtering gate.

> [!warning] Risks
> - **[[2509.26354|Misevolution]] drift**: self-reward biases amplify. → Red-team after each cycle ([[2604.05498|JailWAM]] / [[2506.07468|SELF-REDTEAM]] probes).
> - **Reward hacking on imagined SR**: model games WAM not real. → Periodic real-robot validation + novelty bonuses + [[2605.22446|Pre-VLA]]'s rollout truncation.
> - **WAM drifts from real dynamics**: imagination diverges over cycles. → Outer-loop WAM updates ([[2603.04029|Self-Adapting RL]]) + the ρ > 0.7 imagined-vs-real gate as a stop condition.

### B3 — Self-Verifying / Calibrated-Imagination WAM

| | |
|---|---|
| **Cluster** | B — Training & Grounding |
| **Thesis** | The field verifies a WAM's imagination at runtime — filter the dream after it's generated — instead of training on it. But forward generation and inverse verification are *asymmetric*: action-free video is abundant and action-relevant features are low-dimensional, so verifying is structurally cheaper than generating. The bet: a forward-inverse asymmetry signal yields ≥2× WM sample-efficiency and +22% downstream reward with no extra action labels, where epistemic-uncertainty gating ([[2504.16680\|RWM-U]]) reaches 0.91 normalized reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/). |
| **Anchor papers** | [[2604.22748\|Agentic World Modeling Survey]], [[2310.06253\|Objective Mismatch MBRL Survey]], [[2602.04411\|Self-evolving Embodied AI]], [[2604.01985\|WAV]], [[2504.16680\|RWM-U]] |
| **Key targets** | ≥2× WM sample-efficiency + 22% downstream reward ([[2604.01985\|WAV]]); epistemic-uncertainty gating 0.91 reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/) ([[2504.16680\|RWM-U]]); imagined-vs-real ρ as the calibration metric (links to B2) |

**Why it matters.** B2 detects and recovers from failure at *runtime*; B3 asks whether the WM can be made trustworthy at *training time* so the runtime loop has less to clean up. [[2604.22748|Agentic World Modeling Survey]]'s L3 Evolver "revises its own model when predictions fail" — but the usual tool for knowing *when* a prediction failed is uncertainty estimation, which [[2604.01985|WAV]] shows "often fails in under-explored data regions where new information is most needed," exactly where calibration matters. [[2310.06253|Objective Mismatch MBRL Survey]] generalizes it: low predictive WM loss does not imply high downstream return, so the WM's own training signal is miscalibrated against policy need. Two results reframe the problem. [[2604.01985|WAV]] exploits a structural *asymmetry* — verifying a transition (inverse) is cheaper and more robust than generating it (forward) — to turn verification into a self-improving training cycle. [[2504.16680|RWM-U]] shows an ensemble's epistemic uncertainty, used to *penalize* imagined rollouts, makes offline MBRL work on real quadrupeds and humanoids. Calibration of imagination is a train-time lever, not a runtime patch.

**First-principles framing.**
- **First principle**: Making a prediction and checking one are not equally hard. Video without action labels is plentiful, so judging whether an imagined future *looks* plausible is cheap; and the action-relevant part of a state is small, so judging whether a future is *reachable* by some action needs little labeled data. A checker that exploits this gap is fundamentally cheaper than the generator it checks — at any scale.
- **Assumption being challenged**: That the reliability gap closes by estimating uncertainty better. [[2604.01985|WAV]] shows plain uncertainty estimates fail right where they're needed; [[2504.16680|RWM-U]] shows uncertainty helps only when it *steers* the training objective, not when it merely reports a confidence number. The field filters a finished dream at runtime; B3 shapes the dream while training.
- **The bet**: Using this make-vs-check gap as a training signal — judge whether a subgoal looks plausible (from an action-free generator) and whether it is reachable (from a small inverse model) — yields at least 2× better WM sample-efficiency and +22% downstream reward with *no extra action labels* ([[2604.01985|WAV]]); and uncertainty-based gating reaches 0.91 reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/) ([[2504.16680|RWM-U]]). Unlike B2's runtime detect→recover, B3 calibrates while training, so imagination is trustworthy first.

**Evidence.**
- [[2604.01985|WAV]] — Splits verification into state-plausibility (action-free generator) + action-reachability (sparse inverse); prioritizes where plausible and predicted futures disagree; 2× sample-efficiency, +22% reward over six tasks.
- [[2504.16680|RWM-U]] — Ensemble epistemic uncertainty penalizes imagined rollouts ([[2005.13239|MOPO-PPO]]); uncertainty tracks long-horizon error; 0.91 reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/), deployed on [Unitree G1](https://www.unitree.com/g1/).
- [[2310.06253|Objective Mismatch MBRL Survey]] — Predictive WM loss does not correlate with downstream return; the training signal is miscalibrated against policy need — the gap B3 closes.
- [[2604.22748|Agentic World Modeling Survey]] — L3 Evolver revises its model when predictions fail; B3 supplies the *when-it-failed* signal as a train-time objective, not a runtime probe.
- [[2605.22446|Pre-VLA]] — Runtime verifier that truncates unreliable imaginations (+6.83 pp [[2306.03310|LIBERO]]); B3 is its train-time complement — calibrate so there is less to truncate.
- [[2606.02486|AHEAD]] — Latent WM for *dynamic* scenes; adaptive horizon-halting stops predicting when uncertainty rises; 93.7% vs 48% under acceleration — calibration in action where uncalibrated imagination fails.

**Concrete research questions.**
1. **Q1 — Forward-inverse verifier on a latent WAM.** Wrap [[2604.01985|WAV]]'s subgoal-generator + sparse-inverse decomposition around a JEPA WAM ([[2602.10098|VLA-JEPA]] / [[2605.25313|UWM-JEPA]]); measure sample-efficiency vs uncertainty-only baseline.
2. **Q2 — Epistemic-uncertainty gating as a dense reward.** Adapt [[2504.16680|RWM-U]]'s [[2005.13239|MOPO]] penalty to a latent-consistency reward on A1's hybrid backbone; does penalizing high-uncertainty imagined states stabilize the latent-rollout objective?
3. **Q3 — Calibration metric = imagined-vs-real ρ.** Treat the B2 ρ > 0.7 gate as B3's *objective*, not just a stop condition: train the WM to maximize imagined-vs-real SR correlation directly.
4. **Q4 — Active data collection from verifier disagreement.** Use [[2604.01985|WAV]]'s discrepancy signal to drive which real-robot interactions to collect next; close the loop with B2's failure-finder.
5. **Q5 — Sparse-vs-dense inverse ablation.** Does the sparse inverse model's OOD robustness ([[2604.01985|WAV]]) hold on contact-rich tasks (shared substrate with B1's discrete contact modes)?

**Related research papers.**
- [[2604.01985|WAV]] — Forward-inverse asymmetry self-improving cycle; 2× sample-eff, +22% reward; no extra labels; the calibration-as-training exemplar.
- [[2504.16680|RWM-U]] — Uncertainty-aware WM + [[2005.13239|MOPO-PPO]]; 0.91 reward real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/); uncertainty must gate, not just report.
- [[2605.04709|ELVIS]] — Ensemble-calibrated latent imagination; UCB-gated λ-return truncates uncertain futures in learning *and* planning; SOTA vs TD-MPC2 / DreamerV3 on 14 DMC, sim-to-real Rrms 2.2±0.4 mm; the latent sibling of RWM-U's gating.
- [[2310.06253|Objective Mismatch MBRL Survey]] — Decision-aware MBRL; predictive loss ⊥ return; names the miscalibration B3 targets.
- [[2605.22446|Pre-VLA]] — Preemptive runtime verifier; +6.83 pp [[2306.03310|LIBERO]]; runtime filter, not train-time calibration.
- [[2510.09459|FIPER]] — Predictive failure via OOD + uncertainty; detection only, no calibration training signal.
- [[2506.09937|SAFE]] — Internal-feature + conformal prediction; calibrated detection, but post-hoc not in WM training.
- [[2510.16281|SEAL]] — Runtime CoT-faithfulness verifier; +15 pp; verifies plan↔outcome, not WM imagination.
- [[2604.22748|Agentic World Modeling Survey]] — L3 Evolver framework; survey, no calibration method proposed.
- [[2603.04029|Self-Adapting RL]] — Outer-loop WM adaptation; complements B3's inner calibration signal.
- [[2606.02486|AHEAD]] — Uncertainty-gated adaptive horizon over a 4.9M-param latent WM; 93.7% vs 48% under acceleration; calibrated imagination at speed.
- [[2606.05773|PiL-World]] — Chunk-wise closed-loop policy-in-the-loop WM; imagined-vs-real Pearson r 0.94, gap 63.2→12.0%, Hallucination-Free 41.5→70.1%; the ρ-calibration target B3 maximizes.
- [[2606.04463|OSCAR]] — Skeleton-conditioned (URDF/MANO) video WAM; precise action-following drives Pearson r +0.852 with RoboArena rankings (MAE 1.73 pp); conditioning keeps imagined-vs-real correlation high.
- [[2604.19092|RoboWM-Bench]] — Visual plausibility ≠ executability; the gap a calibrated WM must close, measured.
- [[2512.01119|World Model Surprise Robustness]] — Filters noisy prediction errors to separate genuine OOD novelty from sensor noise + stochastic dynamics; avoids false-alarm adaptation; calibrates *when* a surprise is real.
- [[2511.11520|Video WM Policy Eval]] — Action-conditional video WM scores policies without real rollouts (VLM judge); Pearson r 0.833–0.879 sim / 0.687 real; the imagined-vs-real ρ B3 maximizes, measured.
- [[2602.20057|AdaWorldPolicy]] — Flow-matching DiT WM + action expert using WM prediction error as a self-supervised LoRA signal; 0.96 LIBERO-10, OOD recovery at 4 Hz; uncertainty steers training, not just reports.
- [[2509.23958|RLIR]] — Post-trains a WM with GRPO on an inverse-dynamics frame-level reward (inferred-vs-ground-truth actions); +5–10% action-classification accuracy across AR (MineWorld) + diffusion (NFD) WMs; IDM reward beats human-preference + pixel rewards.
- [[2602.09022|WorldCompass]] — RL post-training with a 3D-foundation-model Interaction-Following reward + visual-quality reward over clip-level rollouts; composite-action following 20→55% to 381-frame horizons; calibrates imagination to action adherence.
- [[2601.14354|VJEPA-Probabilistic]] — Probabilistic JEPA (variational predictive bottleneck + Bayesian Product-of-Experts) holds signal R²>0.84 under a noisy-TV distractor where VAE/pixel-AR collapse to ~0.50; uncertainty-aware latent that knows what to ignore.
- [[2605.06732|Training in Imagination]] — Decomposes the return-gap bound into separate dynamics + reward error terms; reward error decays fast (exponent 0.96) vs dynamics (0.11), so the residual is dynamics; tells calibration where to spend the data budget.

**Benchmarks & metrics.**
- WM sample-efficiency curve — prediction error vs labeled-interaction budget; [[2604.01985|WAV]] reports 2× improvement; the headline calibration metric.
- Downstream reward across manipulation tasks — [[2604.01985|WAV]] +22% over strong baselines on six tasks.
- Real-robot normalized reward — [[2504.16680|RWM-U]] 0.91 on [ANYmal D](https://www.anybotics.com/robotics/anymal/), deployed on [Unitree G1](https://www.unitree.com/g1/); sim-to-real validity of calibration.
- Imagined-vs-real SR Pearson ρ — shared with B2; B3 maximizes it directly rather than gating on it.

> [!warning] Risks
> - **Sparse inverse model misses subtle dynamics**: low-dimensional action features may drop contact transients. → Bound the claim to where action-relevant features are recoverable; pair with B2's discrete contact modes for contact-rich regimes.
> - **Uncertainty gating too conservative**: penalizing all high-uncertainty states kills exploration ([[2504.16680|RWM-U]]'s penalty coefficient is a critical hyperparameter). → Tune the penalty on a held-out real-robot calibration set, not in simulation alone.
> - **Calibration ≠ correctness**: a WM can be well-calibrated about being wrong. → Validate against B2's imagined-vs-real ρ AND the joint causal-binding metric developed in the umbrella [[Embodied-AI|Embodied-AI]], not calibration alone.

### B4 — WAM-as-Data-Engine

| | |
|---|---|
| **Cluster** | B — Training & Grounding |
| **Thesis** | A policy can only get as good as the data it trains on, and real robot data is scarce, expensive, and narrow. A generative WAM can manufacture demonstrations far cheaper and far wider than teleoperation — so its highest-value output is a *training corpus*, not a rollout or a safety check. The field treats WAM output as something you plan or verify in-episode; here the durable product is data. The bet: a physics-validated WAM data engine trains a downstream policy to beat real-data-only collection by ≥25 pp SR ([[2606.02577\|RoboDream]] Gen-Mix 62.5% vs real-only 36.3%) at ≥2× lower collection cost, and the physics-validation filter is load-bearing not optional ([[2606.04708\|VISTA]] validated subset 0.65 vs unfiltered-low 0.00). |
| **Anchor papers** | [[2605.12090\|WAM Survey]], [[2601.15533\|Actionable Simulators]], [[2604.15395\|Foundation Models in Robotics Survey]], [[2606.02577\|RoboDream]], [[2606.01027\|τ0-WM]], [[2606.04708\|VISTA]] |
| **Key targets** | Downstream SR over real-only by ≥25 pp ([[2606.02577\|RoboDream]] 62.5% vs 36.3%); collection cost ≥2× lower ([[2606.02577\|RoboDream]] 2.2×); zero-shot lift from imagined-corpus pretraining ([[2606.01027\|τ0-WM]] 0.55 vs 0.14); test-time rectification on the same backbone ([[2606.01027\|τ0-WM]] 0.43→0.60) |

**Why it matters.** B1–B3 treat the WAM's imagination as something consumed *inside* an episode — contact dynamics to roll out (B1), failures to recover from (B2), dreams to calibrate and verify (B3). But [[2605.12090|WAM Survey]] names "data-ecosystem mixing" as an open problem, and [[2604.15395|Foundation Models in Robotics Survey]] names dataset/challenge mapping — both point at the WAM's most underexploited output: *training data*. Real robot data is the binding constraint on policy competence, and teleoperation does not scale. Three 2026 results show the WAM as a data engine already beats real collection. [[2606.02577|RoboDream]] decouples robot motion from scene/object context and synthesizes demonstrations compositionally — its Gen-Mix data trains policies to 62.5% vs 36.3% real-only, at 2.2× faster collection. [[2606.01027|τ0-WM]] pretrains on ~27,300 hours of heterogeneous imagined-plus-real data and triples zero-shot SR on unseen tasks (0.55 vs 0.14). [[2606.04708|VISTA]] adds the missing discipline: physics-validate every synthesized trajectory, because raw human-collected (UMI) data is often kinematically infeasible — its validated subset trains to 0.65 OSR while the unfiltered-low subset trains to 0.00. The manipulation-task application of synthesized demos is [[Manipulation|Manipulation]]-B1; here the contribution is the *engine* and its validation discipline.

**First-principles framing.**
- **First principle**: How good a policy can get is set by how much variety its training data covers and how physically correct that data is — not by where the data came from. A generative WAM can manufacture variety — new objects, scenes, camera views, robot bodies — that real collection can't afford to reach. The WAM is a variety-widening machine for whatever policy consumes its data.
- **Assumption being challenged**: That a WAM's outputs are rollouts or dreams — short-lived, used up within one episode. The field treats the WAM as a runtime tool. [[2606.02577|RoboDream]], [[2505.12705|DreamGen]], and [[2606.01027|τ0-WM]] flip this: the lasting product is a *dataset*, and the WAM is a data engine that feeds a separate policy.
- **The bet**: A physics-validated WAM data engine beats real-data-only collection by ≥25 pp SR ([[2606.02577|RoboDream]] 62.5% vs 36.3% = +26.2 pp) at ≥2× lower cost (2.2×) — *and* the physics filter does real work, not decoration ([[2606.04708|VISTA]]: validated 0.65 vs unfiltered 0.00). Unlike B2 (imagines *failures* to improve a policy that already exists), B4 imagines *demonstrations* to bootstrap a policy that doesn't exist yet.

**Evidence.**
- [[2606.02577|RoboDream]] — Compositional video-diffusion WM decouples robot motion from scene/object; Gen-Mix 62.5% vs 36.3% real-only, 0% raw-retrieved; 2.2× faster collection; the data-engine existence proof.
- [[2606.01027|τ0-WM]] — Unified video-action WM on ~27,300 hrs; imagined-corpus pretraining lifts zero-shot 0.55 vs 0.14, fine-tuned 0.83 vs 0.70; same backbone rectifies actions at test (0.43→0.60).
- [[2606.04708|VISTA]] — Physics-validated UMI-data adaptation; scores continuity / self-collision / execution fidelity; validated subset 0.65 OSR vs 0.00 low-score; the validation-discipline anchor.
- [[2505.12705|DreamGen]] — Video WMs as scalable synthetic data generators; 22 novel behaviors, 10 unseen environments from a minimal real seed; the video-WM-as-data-engine precedent.
- [[2412.14957|DREMA]] — Compositional WM (3DGS + physics) generates training data via imagination; better low-data imitation + novel-configuration generalization.

**Concrete research questions.**
1. **Q1 — Physics-validation as a first-class filter on synthesized demos.** Put [[2606.04708|VISTA]]'s continuity / self-collision / execution-fidelity scoring downstream of [[2606.02577|RoboDream]]'s compositional generator; ablate validated-vs-unfiltered downstream SR (VISTA's 0.65 vs 0.00 is the headline to reproduce on a second generator).
2. **Q2 — Mixing ratio of imagined-to-real.** [[2606.02577|RoboDream]]'s Gen-Mix beats both extremes; sweep the synthesized:real ratio and find where downstream SR peaks per task family.
3. **Q3 — Cross-embodiment data synthesis.** Use [[2606.05979|WLA]]'s action-free cross-embodiment video learning as a source: can the engine synthesize demos for an embodiment with *zero* real demos of the target task?
4. **Q4 — One backbone, two jobs.** [[2606.01027|τ0-WM]] uses the same WM for data generation and test-time rectification — measure whether co-training the engine on its own rectification signal improves synthesized-data quality (closes B3's calibration into B4's generation).
5. **Q5 — Prop-free teleoperation at scale.** Extend [[2606.02577|RoboDream]]'s kinematic-only collection (imaginary objects, visual synthesis later) — what fraction of a manipulation curriculum can be collected prop-free without downstream SR loss?

**Related research papers.**
- [[2606.02577|RoboDream]] — Compositional world model for robot data synthesis; Gen-Mix 62.5% vs 36.3% real-only, 2.2× faster; the data-engine exemplar.
- [[2606.01027|τ0-WM]] — Unified video-action WM; heterogeneous-corpus pretraining triples zero-shot SR (0.55 vs 0.14); engine + test-time rectifier in one backbone.
- [[2606.04708|VISTA]] — Vision-grounded, physics-validated UMI-data adaptation; validated subset 0.65 vs 0.00; the validation discipline B4 makes mandatory.
- [[2505.12705|DreamGen]] — Video WMs as synthetic data generators; 22 novel behaviors / 10 unseen environments; precedent for the engine but no physics-validation filter.
- [[2511.19861|GigaWorld-0]] — Production-scale data engine: 2B-MoE video + 3DGS 3D + inferred physics + executable trajectories; a VLA trained *exclusively* on its data works real; 82.07 PBench; the large-scale B4 existence proof.
- [[2412.14957|DREMA]] — Compositional WM (3DGS + physics) generating training data via imagination; low-data-regime imitation; digital-twin generator, not a video diffusion engine.
- [[2603.16861|MolmoBot]] — Policies trained exclusively on procedurally generated sim data; 79.2% real Franka FR3; procedural generation, not a learned WM engine.
- [[2511.04665|Real-to-Sim GS]] — 3DGS + soft-body twins; r=0.915 (push-T) / 0.901 (rope) sim-real; supplies the validation substrate B4 needs but does not synthesize demos.
- [[2606.05979|WLA]] — Learns novel tasks from action-free same- and cross-embodiment videos, nearly tripling unseen-task SR; the cross-embodiment data source for Q3.
- [[2602.23253|SPARR]] — Sim + vision-conditioned real residual; 95–100% [[2407.08028|AutoMate]]; a data-augmentation point, not a generative engine.
- [[2604.16484|DexWorldModel]] — Causal latent WM with zero-shot sim-to-real; the kind of downstream consumer a B4 engine would feed.
- [[2603.08546|Interactive World Simulator]] — Consistency-model AE + action-conditioned latent dynamics; policies trained purely on its data reach 87.9% vs 90.3% real, 0.85–0.99 sim-real correlation; the data-engine-with-fidelity-check precedent.
- [[2512.00961|GenReward]] — Frozen video diffusion (CogVideoX) turned into a multi-granular RL reward generator; beats DreamerV3 with dense rewards (Bin-Picking 398→822); the imagination-as-reward-signal variant of the engine.
- [[2512.24766|Dream2Flow]] — Image-to-video gen → 3D object flow (depth+seg+point-track lifted to 3D) → optimization-based action inference; up to 8/10 real tasks across rigid/articulated/deformable; the flow-extraction data-engine variant.
- [[2602.12099|GigaBrain-0.5M*]] — World-model-conditioned policy (RAMP) + Human-in-the-Loop Rollout + continual joint VLA/WM training; 100% Juice-Prep, +30 pp over RECAP, GigaBrain-0.1 tops RoboChallenge 51.67%; self-improving closed-loop data engine.
- [[2506.22007|RoboEnvision]] — Hierarchical KeyframeDiff + FillingDiff long-horizon video generator; a policy trained on its videos hits 67.4% on 45 LHMM tasks vs UniPi 23.5% / RDT-1B 34.1%; the long-horizon synthetic-data source.
- [[2510.26583|Emu3.5]] — 34.1B decoder-only native next-state predictor pretrained on ~63M videos under one next-token objective; 67.1% win-rate vs Gemini-2.5-Flash on embodied manipulation; the internet-scale generative substrate a data engine can draw on.

**Benchmarks & metrics.**
- [[2406.02523|RoboCasa]] — Large-scale kitchen manipulation suite; the downstream-policy eval where [[2606.02577|RoboDream]]'s Gen-Mix reports 62.5% vs 36.3% real-only.
- [[2306.03310|LIBERO]] / [[2504.13059|RoboTwin]] — Standard downstream manipulation suites; train a fixed policy on synthesized-vs-real data and compare SR at matched policy and budget.
- [[2510.13626|LIBERO-Plus]] — 10,030 OOD perturbations; the generalization claim — synthesized data should widen OOD coverage beyond what real-only collection reaches.
- Collection cost (episodes/hr) — [[2606.02577|RoboDream]] 50 episodes in 55 min vs 2 hrs teleoperation (2.2×); the cost half of the bet.

> [!warning] Risks
> - **Synthesized data looks plausible but is not executable**: physically infeasible demos teach the wrong dynamics. → Make [[2606.04708|VISTA]]'s physics-validation filter mandatory, not optional; report validated-vs-unfiltered downstream SR as the first ablation.
> - **Distribution narrows to the engine's biases**: the WM only synthesizes what it has seen, so apparent diversity may be shallow. → Sweep the imagined:real mixing ratio ([[2606.02577|RoboDream]] Gen-Mix beats both extremes) and keep a real-data anchor; never train on synthesized data alone.
> - **Compounding error**: a policy trained on a WM's data inherits the WM's failure modes silently. → Validate downstream on a real-robot held-out set and on [[2510.13626|LIBERO-Plus]] OOD, not only on in-distribution synthesized evals.

---

## Cross-Cutting Themes

> [!tip] Latent Prediction Is the Dominant Substrate — and Now Has a Formal Membership Test
> A1, A2, A3, and B2 all assume "video at training, latent at deployment" with JEPA / DiT-on-latent backbones. The field has lacked a test for *when* a learned latent is actually a world model. [[2605.26379|LeJEPA World Model]] supplies it (identifiable iff isotropic-Gaussian, then latent planning matches an oracle); [[2605.25313|UWM-JEPA]] extends the substrate to belief space. So A1's hybrid latents, A2's tactile-imagination latent, A3's encoding-quality choice, and B2's self-evolution rollouts answer to one membership test instead of convention — and A3 makes the sharpest use of it, asking whether the semantic / continuous latents that win control are exactly the ones that pass the isotropic-Gaussian test — as do the deploy-time memory latents of [[Spatial-4D|Spatial-4D]]-C4.

> [!tip] Verifiable Predicates over Imagined State Turn Diagnosis into Action
> B1, B2, and B3 each make the recurring "statistical correlations ≠ causal understanding" diagnosis enforceable on the *imagination* itself: B1 makes contact a discrete verifiable transition ($c_t \in$ {no-contact, making, in-contact, breaking, slipping}), B2 makes recovery contingent on a verified imagined rollout, B3 makes forward-inverse asymmetry a train-time calibration signal. [[2604.01985|WAV]]'s asymmetry and [[2605.22446|Pre-VLA]]'s rollout truncation are the shared mechanism — score the *imagination*, not just the pixels.

> [!tip] Calibrated Imagination Is the Training-Time Twin of Runtime Verification
> B3, B2, and A2 form a trust stack at three different times. B3 calibrates imagination at *training* time (forward-inverse asymmetry, [[2604.01985|WAV]] 2× sample-eff; epistemic gating, [[2504.16680|RWM-U]] 0.91 real-robot reward). B2 verifies and recovers at *runtime* ([[2605.22446|Pre-VLA]] truncates unreliable dreams). A2's imagined-vs-measured wrench loss is a train-time forecast the same machinery can score. The coupling: B3's calibration raises the imagined-vs-real ρ that B2 uses as its stop condition, so investing in B3 shrinks B2's recovery work — and A2's force imagination is one more channel calibration must keep honest.

> [!tip] The Substrate Is Task-Conditional — Latent for Transit, 4D Geometry for Contact
> [[Spatial-4D|Spatial-4D]]-C3 looks like it contradicts Cluster A: A1 leans on "latent at deployment" as efficiency-optimal, yet C3 keeps explicit 4D geometry *at deployment* ([[2604.26694|X-WAM]], 15 Hz). Neither is a global winner — the substrate is **task-conditional**, a cross-doc reconciliation between WAM's latent backbone (A) and Spatial-4D's geometry substrate (C3). For appearance- and trajectory-bound segments (transit, reaching, free-space motion), latent wins: A1's deploy-light latent ~10 ms dominates, and [[2602.10098|VLA-JEPA]] already hits 97.2% [[2306.03310|LIBERO]]. For contact- and spatial-bound segments (insertion, stacking, pouring), the action depends on geometry the policy cannot re-infer from pixels, so C3's explicit 4D earns its cost — and [[2604.26694|X-WAM]]'s asynchronous denoising shows 4D need not break the real-time budget. The open design is a **process-adaptive substrate** (A1's Q3 contact-gated switching, generalized, plus the wrench channel A2 imagines on top): run latent in transit, switch to Spatial-4D-C3's 4D geometry on predicted contact. The question is not latent-vs-4D but *when* to use each.

*Geometry-as-memory cross-ref:* the synthesis that the imagined world should be parameterized by *geometry* (explicit 4D structure + world-frame patches), with persistent memory living in that geometric frame, now spans [[Spatial-4D|Spatial-4D]]-C3 (natively-4D substrate) and [[Spatial-4D|Spatial-4D]]-C4 (persistent geometric memory).

> [!tip] Efficiency Is a Deployment Prerequisite That Couples to Every Direction in This Doc
> No direction here owns efficiency, yet A1 and B2 both need real-time budgets to be feasible at all — the 3–5 Hz AR ceiling and 4.8× WAM latency cost are the anchors ([[2604.16484|DexWorldModel]]'s O(1) memory + async inference shows the levers are co-designable; full real-time co-design lives in the umbrella [[Embodied-AI|Embodied-AI]]). A1's train-dense/deploy-light hybrid is itself an efficiency move; B2's evolution cycle is infeasible if each imagined rollout is too slow to iterate. The same latency budget bounds the [[Spatial-4D|Spatial-4D]]-C4 persistent memory, which earns its place only if coherence gain beats footprint cost. Any method that ignores the latency budget cannot be deployed, whatever its SR.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Hybrid latent+pixel/3DGS vs pure-latent vs pure-pixel WAM at matched FLOPs (OOD × latency, at matched real SR) | A1 | [[2605.20752\|GaussianDream]] (train-dense/deploy-light, single point on the plane) + [[2603.22078\|WAM vs VLA Robustness]] (4.8× latency cost, no hybrid) |
| WAM with a tactile/force *prediction* head (imagined wrench, not consumed force) | A2 | [[2506.14754\|Sparsh-X]] (touch encoder, no prediction head) + [[2604.20444\|VTouch++]] (synchronized dataset, no WAM consumer) |
| Encoding-quality ablation at matched architecture: semantic / continuous latent vs reconstruction / VQ, scored by closed-loop SR + OOD | A3 | [[2605.06388\|Semantic-LDM-WM]] (reconstruction-vs-semantic, single backbone) + [[2605.15725\|DiLA]] (continuous-vs-VQ/VAE, scored on SSIM/LPIPS not closed-loop SR) |
| Discrete contact-mode latent; sub-millimeter assembly SR with contact-aware imagination | B1 | [[2604.16484\|DexWorldModel]] (causal latent but continuous contact) + [[2604.27367\|DOT-Sim]] (contact ground truth, no WAM consumer) |
| Integrated detection→diagnosis→recovery loop with WAM-driven imagination + rollout verification | B2 | [[2605.22446\|Pre-VLA]] (verifier only, no full loop) + [[2605.10921\|RoboMemArena]] (memory-dependent recovery, no imagination loop) |
| Forward-inverse calibration as a *training* signal (not a runtime filter) tied to imagined-vs-real ρ | B3 | [[2604.01985\|WAV]] (asymmetry cycle, not ρ-objective) + [[2504.16680\|RWM-U]] (uncertainty gating, locomotion only) |
| Physics-validated WAM data engine with the validation filter ablated against downstream SR | B4 | [[2606.02577\|RoboDream]] (compositional synthesis, no physics-validation filter) + [[2606.04708\|VISTA]] (physics-validated UMI adaptation, not a generative engine) |

---

## Cross-References

- [[07_WAM|07_WAM]] — WAM taxonomy (VideoGen / latent / Dreamer / VLM-integrated / efficient / self-evolving)
- [[08_Latent-World-Models|08_Latent-World-Models]] — JEPA + alternative latent models; latent reasoning
- [[13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]] — Failure detection, diagnosis, recovery; self-evolution mechanisms
- [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] — Physics-aware design space; physics commonsense benchmarks
- [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]] — Sim-to-real strategies; learned simulators; reality-gap diagnostics
- [[08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — Canonical survey index
- [[Embodied-AI|Embodied-AI]] — Umbrella directions. Joint WAM–policy co-evolution, physics-consistency verification, joint causal-consistency eval, real-time deployment, and cross-embodiment transfer live there (B1, B3, C1, C3, D2) — omitted here to avoid dup.
- [[Spatial-4D|Spatial-4D]] — Sibling doc on the model-agnostic 3D/4D representation — occupancy & 4D world models, geometric memory ([[2604.26694|X-WAM]], [[2603.17117|MosaicMem]]).
- [[Sim2Real|Sim2Real]] — Sibling doc on sim-to-real / real-to-sim transfer; borders this doc's physics-grounding (B-cluster) and world-model-as-simulator themes.
