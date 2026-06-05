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
> Five World Action Model (WAM) research directions across two clusters — *Theory & Architecture* (A) and *Training & Grounding* (B) — synthesized from 35 WAM/embodied surveys, ten Embodied-AI deep-dive readings, and the frontier methods that set each bet's bar ([[2605.20752|GaussianDream]], [[2604.16484|DexWorldModel]], [[2604.01985|WAV]], [[2504.16680|RWM-U]]). The scope is *WAM-specific machinery*: the latent/representation substrate and architecture choices (A), plus training-time grounding and calibration (B). The model-agnostic geometric representations — natively-4D imagination and persistent geometric memory, framed as substrates any VLA / WAM / policy can stand on — live in [[Spatial-4D|Spatial-4D]] (Cluster C). Cross-cutting directions that span model families — joint WAM–policy co-evolution, physics-consistency verification, joint causal-consistency evaluation, real-time deployment, cross-embodiment transfer — live in the umbrella [[Embodied-AI|Embodied-AI]]. Each direction carries a **first-principles framing** (problem / assumption broken / measurable bet) and a non-consensus thesis. Every metric anchor comes from a cited `_KnowledgeHub_/{ID}.md` note.

---

## Methodology

**Scope.** Corpus: 35 pure-WAM + adjacent surveys and ~70 WAM-method/benchmark papers from `_KnowledgeHub_/`, cross-checked against [[08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] and ten `Embodied-AI/` deep-dives. The method is survey-grounded ideation: surveys name open problems, benchmarks fix what is measurable, frontier methods fix what is achievable now. **De-duplication**: five directions the umbrella [[Embodied-AI|Embodied-AI]] already covers (B1, B3, C1, C3, D2 there) were removed — see Cross-References.

- **Survey enumeration**: tag-scan over `survey` × {`world-model`, `VLA`, `embodied-AI`, `robotics`, `physics-aware`, `sim-to-real`} for each survey's named open problems.
- **Deep-dive mining**: full reads of [[04_WAM|04_WAM]], [[05_Latent-World-Models|05_Latent-World-Models]], [[06_Self-Evolving-VLA-WAM|06_Self-Evolving-VLA-WAM]], [[07_Physics-Aware-Embodied-AI|07_Physics-Aware-Embodied-AI]], [[11_Sim-to-Real-Transfer|11_Sim-to-Real-Transfer]]; 3+-way convergence seeded A1 (hybrid substrate), A2 (tactile), B1 (contact).
- **Closest-baseline anchoring**: each bet is pinned to the strongest paper it must beat — [[2604.16484|DexWorldModel]], [[2605.20752|GaussianDream]], [[2604.01985|WAV]], [[2504.16680|RWM-U]] set the bar for A1, B3.
- **Filter**: kept directions with 3–10 attacking papers but no consensus solution; dropped saturated (more-compute) and premature (hypothetical-AGI) framings; prioritized intersections (tactile×WAM, contact×WAM, physics×WAM).
- **First-principles framing**: each direction states the problem's irreducible structure, the assumption it challenges, and the non-consensus bet.

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

Spatial axis trajectory: latent vectors → token sequences → explicit 3D rendering (NeRF, 3DGS). [[2605.20752|GaussianDream]] sits at the rendering end as a train-dense, inference-light hybrid (A1's substrate); [[2604.16484|DexWorldModel]] anchors the token-feature end on semantic [DINOv3](https://arxiv.org/abs/2508.10104) latents. The explicit-4D end ([[2604.26694|X-WAM]], a deploy-time 4D substrate) is owned by [[Spatial-4D|Spatial-4D]]-C3.

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
| **A — Theory & Architecture** | A1, A2 | Right substrate for joint imagination + action | A1's hybrid latent+pixel/3DGS backbone is the deploy substrate; A2 extends it into tactile/force imagination; [[2605.26379\|LeJEPA World Model]]'s identifiability criterion governs A1's latent half, and A2's wrench head is the modality A1's backbone does not yet imagine |
| **B — Training & Grounding** | B1, B2, B3 | Imagination diverges from physical reality | B1's discrete contact-mode latent stabilizes B2's self-evolution in contact-rich regimes; B3's forward-inverse calibration is the train-time signal that keeps B2's imagined-vs-real ρ high; [[2604.01985\|WAV]]'s asymmetry signal and [[2605.22446\|Pre-VLA]]'s runtime verifier are the trust valves all three share |

---

## Cluster A — WAM Theory & Architecture

*Latent representation + architecture choices that close the gap between dynamics prediction and action generation.*

### A1 — Hybrid Latent+Pixel WAM Architectures

| | |
|---|---|
| **Cluster** | A — Theory & Architecture |
| **Thesis** | The field treats latent-vs-pixel as a one-time binary that locks both training and inference. But training density and inference density are independent — nothing forces a model to predict at the same density it trains at. The bet: a hybrid backbone (dense pixel/3DGS supervision at train, latent rollout at deploy) Pareto-dominates pure-latent and pure-pixel WAMs on the OOD × latency × interpretability cube. |
| **Anchor surveys** | [[2510.16732\|World Models for Embodied AI Survey]], [[2511.02097\|WM Manipulation Survey]], [[2604.02029\|Latent Space Survey]] |
| **Key targets** | Latent ~10 ms vs pixel ~150 ms inference; match [[2605.20752\|GaussianDream]]'s 98.4% [[2306.03310\|LIBERO]] / 34.4→50% real at lower deploy cost; [[2510.13626\|LIBERO-Plus]] OOD retention from dense co-training |

**Why it matters.** [[2510.16732|World Models for Embodied AI Survey]] tracks a trend from latent vectors → token sequences → explicit 3D rendering. Hybrids span multiple axis points and stay under-explored; single-paradigm WAMs hit the latency-vs-robustness or speed-vs-interpretability trade-off. [[04_WAM#6. Efficient & Action-Centered WAMs|04_WAM §6]] finds VideoGen 4.8× slower but most robust, latent fast but opaque. Two existence proofs show the hybrid recipe works. [[2605.20752|GaussianDream]] supervises a renderable 3D-Gaussian future at train time, then *drops the auxiliary heads at inference* (34.4→50% real, 531 ms/chunk). [[2604.16484|DexWorldModel]] uses semantic [DINOv3](https://arxiv.org/abs/2508.10104) latents as targets to separate interaction from visual noise (94% [[2504.13059|RoboTwin]], zero-shot sim-to-real). Both confirm: train on dense signal, deploy on a cheap representation.

**First-principles framing.**
- **First principle**: Training density and inference density are independent — nothing requires them to match. A model can absorb pixel-/3DGS-density signal at training and emit latent-density signal at deployment, the way humans rehearse with full sensory detail but act on compressed predictions.
- **Assumption being challenged**: That latent-vs-pixel is binary, picked once, and locks both train and inference. The field thinks hybrids are architecturally complex. [[2605.20752|GaussianDream]] and [[2604.16484|DexWorldModel]] show they are really one shared backbone with dense train-time heads that get dropped at deploy.
- **The bet**: A hybrid backbone Pareto-dominates pure-latent and pure-pixel WAMs on the OOD × latency × interpretability cube — not on any single axis (latent wins latency, pixel wins interpretability) but on their joint frontier, at [[2605.20752|GaussianDream]]-class real SR with lower deploy cost.

**Evidence.**
- [[2510.16732|World Models for Embodied AI Survey]]: "An evolutionary trend from compact global latent vector representations (e.g., RSSMs) towards token feature sequences (e.g., Transformers with LLMs) and explicit 3D rendering representations (e.g., NeRF, 3D Gaussian Splatting) is observed."
- [[2605.20752|GaussianDream]]: dense 3D-Gaussian supervision at train, heads discarded at inference; 98.4% [[2306.03310|LIBERO]], 34.4→50% real, 531 ms/chunk — the canonical train-dense/deploy-light hybrid.
- [[2604.16484|DexWorldModel]]: [DINOv3](https://arxiv.org/abs/2508.10104) semantic latents as targets separate interaction from visual noise; 94% [[2504.13059|RoboTwin]]; semantic-latent half of the axis.
- [[2605.06388|Semantic-LDM-WM]]: semantic-aligned latents beat reconstruction VAEs by +9.8 pp closed-loop and +13.6 pp OOD — encoding quality matters more than the latent-vs-pixel split.
- [[05_Latent-World-Models#6. Open Problems|05_Latent-World-Models §6]] names interpretability + latent-pixel alignment as 2 of 4 open problems.

**Concrete research questions.**
1. **Q1 — Hybrid training, single-branch deployment.** Extend [[2603.16666|Fast-WAM]] / [[2605.20752|GaussianDream]]: joint pixel/3DGS + latent objectives at train, latent-only at deploy (~10 ms vs ~150 ms). Measure OOD retention from dense co-training.
2. **Q2 — Shared latent z across modalities.** Can [[2605.15153|Pelican-Unified]]'s shared z anchor a hybrid where imagination decodes to pixel/3DGS (interpretable) and action decodes to latent (fast)?
3. **Q3 — Process-adaptive gating beyond [[2605.10942|HarmoWAM]].** Gate latent-only (transit) vs pixel/3DGS-aided (interaction) based on contact prediction.
4. **Q4 — Semantic vs reconstruction latents under hybrid training.** Does [[2605.06388|Semantic-LDM-WM]] / [[2604.16484|DexWorldModel]]'s semantic-latent result persist when a dense pixel/3DGS branch supervises training?

**Related research papers.**
- [[2605.20752|GaussianDream]] — Feed-forward 3DGS WM; dense train, light deploy; 98.4% [[2306.03310|LIBERO]], 34.4→50% real; the train-dense/deploy-light exemplar.
- [[2604.16484|DexWorldModel]] — Causal latent WM on [DINOv3](https://arxiv.org/abs/2508.10104) targets; O(1) TTT memory; 94% [[2504.13059|RoboTwin]]; semantic-latent axis.
- [[2603.16666|Fast-WAM]] — Train video, test latent; drops WM at test, no test-time imagination.
- [[2605.06388|Semantic-LDM-WM]] — Semantic vs reconstruction; +9.8 pp closed-loop; single-branch only.
- [[2605.10942|HarmoWAM]] — Dual experts + adaptive gating; 89% in-domain; both experts in latent.
- [[2602.10098|VLA-JEPA]] — Pure latent: 97.2% [[2306.03310|LIBERO]]; no pixel decoder for interpretation.
- [[2605.15153|Pelican-Unified]] — Shared latent z; 93.5% [[2504.13059|RoboTwin]]; pixel-side generator, deployment latency open.
- [[2511.08544|LeJEPA]] — Provable Euclidean latent geometry; pure latent, regularization anchor.
- [[2411.04983|DINO-WM]] — Frozen [[2304.07193|DINOv2]] + lightweight dynamics; no pixel verification.
- [[2605.00078|Being-H0.7]] — Dual-branch deployable+privileged; 3–4 ms/step; both branches latent.
- [[2605.15618|Latent Video Prediction Study]] — Systematic latent-vs-pixel SSL eval under perturbations; pretrain-only, no policy joint.

**Benchmarks & metrics.**
- [[2510.13626|LIBERO-Plus]] — 10,030 OOD perturbations; match pure-latent in-dist; gain OOD over latent-only.
- Inference latency (Hz) — A100 forward latency; latent ~10 ms vs pixel ~150 ms; [[2605.20752|GaussianDream]] 531 ms/chunk real-robot reference.
- [[2605.21800|stable-worldmodel]] — Reproducible OOD-robustness harness; [[2411.04983|DINO-WM]] 92% / [[2603.19312|LeWM]] 94% [Push-T](https://arxiv.org/abs/2109.00137) baselines, sharp planning decay under perturbation — substrate for the hybrid OOD claim.
- [[2603.22078|WAM vs VLA Robustness]] — 4.8× latency cost; hybrid must show <2× cost vs pure latent at pixel-WAM OOD.

> [!warning] Risks
> - **Two-branch training cost** dominates compute. → Mitigate by distilling a pre-trained pixel/3DGS WM into the latent encoder (the [[2605.20752|GaussianDream]] discard-at-inference pattern).
> - **Latent-pixel divergence** without shared parameters. → Need explicit alignment loss; [[2604.16484|DexWorldModel]]'s [DINOv3](https://arxiv.org/abs/2508.10104)-target anchoring is one recipe.
> - **Saturated regime**: pure latent already at 97% [[2306.03310|LIBERO]] and [[2605.20752|GaussianDream]] at 98.4%. → Contribution must show on OOD + interpretability + deploy-cost, not headline [[2306.03310|LIBERO]] SR.

### A2 — Tactile/Force-Integrated WAM Imagination

| | |
|---|---|
| **Cluster** | A — Theory & Architecture |
| **Thesis** | The field treats force as a policy *input* but never models it as an *output*, so WAMs imagine visual futures but not wrench futures. Yet in contact, force is the generative cause and vision the consequence — a WM that predicts only consequences is incomplete. The bet: a WAM that imagines wrench futures recovers ≥50% of the measured-tactile→no-tactile contact-task drop ([[2603.17851\|DexViTac]]'s 83.3%→43.3% pipetting ablation) even with no force sensors at deployment, approaching the with-real-tactile [[2603.17851\|DexViTac]] ceiling of 85.8%. |
| **Anchor surveys** | [[2605.12090\|WAM Survey]], [[2511.02097\|WM Manipulation Survey]], [[2604.16592\|Cognition WM Survey]] |
| **Key targets** | Cross-sensor transfer >60.3% ([[2601.20321\|TaF-VLA]] baseline); recover ≥50% of [[2603.17851\|DexViTac]]'s measured-tactile→no-tactile drop (83.3%→43.3% pipetting ablation) using imagined rather than measured tactile; approach the [AutoMate](https://arxiv.org/abs/2407.08028) no-WAM ceiling ([[2603.15956\|ExpertGen]] 90.5%) |

**Why it matters.** Current WAMs imagine visual + proprioceptive futures but rarely tactile/force futures, even though force is the dominant signal in contact-rich manipulation. [[2605.12090|WAM Survey]] names the modality gap; [[2511.02097|WM Manipulation Survey]]'s 13 capabilities rank Multimodal Perception first and Physics Awareness third. All existing tactile work consumes force as policy input, never imagines it as WAM output. The data bottleneck is now gone ([[2604.20444|VTouch++]], [[2603.17851|DexViTac]], [[2604.07335|TAMEn]]), so the modeling gap is exposed. The manipulation-task application of imagined tactile is [[Manipulation|Manipulation]]-B1.

**First-principles framing.**
- **First principle**: In contact-rich manipulation, force is the *generative* signal and vision the consequence — the object moves *because* of force, not the reverse. A WM that predicts consequences but not generators is under-determined in contact regimes.
- **Assumption being challenged**: That force can be consumed (as policy input) without being predicted (as WM output). This treats force as a measurement, not a modeled quantity, throwing away half the inferential machinery and making the policy learn dynamics implicitly. [[2603.17851|DexViTac]]'s kinematics-grounded tactile pretraining shows tactile *can* be modeled, but stops at perception.
- **The bet**: A WAM that imagines wrench trajectories at training time beats a visual-only WAM on contact-task error — *even with no force sensors at deployment* (the imagined wrench acts as a proprioceptive forecast), at [[2603.17851|DexViTac]]-class contact-rich SR.

**Evidence.**
- [[2604.27621|Robot Learning from Human Videos Survey]] and [[2604.16592|Cognition WM Survey]] independently name tactile as the contact-grounding modality.
- The data bottleneck is now resolved: [[2604.20444|VTouch++]] (120K episodes, 1000+ hrs, 36M frames, synchronized vision+tactile+proprioception), [[2603.17851|DexViTac]] (visuo-tactile-kinematic, 85.8% SR, 248 demos/hr), [[2604.07335|TAMEn]] (closed-loop tactile + recovery data, 75% SR).
- All existing tactile work treats force as *policy input*, never *WAM imagined output*: [[2603.15169|ForceVLA2]], [[2601.20321|TaF-VLA]] (60.3% cross-sensor), [[2506.14754|Sparsh-X]] (encoder only), [[2603.15257|HapticVLA]] (distillation sidesteps the problem).

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
- [AutoMate](https://arxiv.org/abs/2407.08028) assembly — 8 industrial tasks; [[2603.15956|ExpertGen]] 90.5%; contact-rich tasks where imagined force matters.

> [!warning] Risks
> - **Noise floor**: subtle slip / microvibration not in vision — imagined force may plateau below measured. → Bound the claim to regimes where force is vision-correlated; report the floor explicitly.
> - **Cross-sensor brittleness**: 60.3% zero-shot ([[2601.20321|TaF-VLA]]) is not deployment-ready. → Use [[2603.17851|DexViTac]]'s kinematics grounding to stabilize the cross-sensor latent.
> - **No published WAM with tactile prediction head** — genuinely unattacked. → Treat the prediction-head ablation (imagined vs no-tactile) as the first-paper deliverable.

---

## Cluster B — WAM Training & Grounding

*Training-time objectives and grounding losses that keep imagination aligned with physical reality.*

### B1 — Contact-Aware WAM for Fine Manipulation

| | |
|---|---|
| **Cluster** | B — Training & Grounding |
| **Thesis** | The field tries to close the contact gap by scaling smooth continuous latents. But contact physics is locally discontinuous (slip-stick, friction-cone, normal-force singularities), so no amount of latent capacity reaches it. The bet: a *discrete* contact-mode latent achieves >90.5% [AutoMate](https://arxiv.org/abs/2407.08028) and sub-millimeter assembly that pure-continuous WAMs cannot reach at any scale. |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2510.04978\|Physical AI Survey]], [[2511.02097\|WM Manipulation Survey]] |
| **Key targets** | [AutoMate](https://arxiv.org/abs/2407.08028) beyond 90.5% with contact-aware imagination; sub-millimeter assembly; beat [[2602.23253\|SPARR]]'s +74.5% relative SR improvement on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer |

**Why it matters.** Latent WAMs handle trajectories well but fail at insertion/assembly, because contact physics is locally non-smooth (make/break, slip, normal-force singularities). Three deep-dives converge ([[05_Latent-World-Models#6. Open Problems|05_Latent-World-Models §6]], [[07_Physics-Aware-Embodied-AI#8. Open Problems|07_Physics-Aware-Embodied-AI §8]], [[11_Sim-to-Real-Transfer#7. Open Problems|11_Sim-to-Real-Transfer §7]]): latent WAMs miss sub-millimeter contact, verifiable physics scales poorly to clutter, learned sims blur on contact. [[2604.16484|DexWorldModel]]'s causal latent ([DINOv3](https://arxiv.org/abs/2508.10104) semantic targets that separate interaction from appearance) is the closest substrate, but its contact transitions stay continuous.

**First-principles framing.**
- **First principle**: Contact physics is locally *discontinuous* — friction-cone boundaries, normal-force singularities, slip-stick transitions are all discrete state changes. A smooth continuous latent cannot represent these without internal discretization; the discreteness is in the physics, not a modeling choice.
- **Assumption being challenged**: That more latent capacity (more dimensions, layers, parameters) eventually closes the contact gap. It never touches the *structural* discontinuity — a smooth model approximating a discontinuous function gets exponentially expensive at the boundary. Even [[2604.16484|DexWorldModel]]'s causal-latent gains keep contact continuous.
- **The bet**: A *discrete* contact-mode latent $c_t \in \{\text{no-contact, making, in-contact, breaking, slipping}\}$ with mode-conditional continuous dynamics achieves >90.5% [AutoMate](https://arxiv.org/abs/2407.08028) (the policy-side WAM-naive ceiling) and sub-millimeter assembly that pure-continuous WAMs cannot reach at any scale.

**Evidence.**
- "Learned sims blur on contact: [[2310.06114|UniSim]] and [[2501.03575|Cosmos]] produce stunning visuals but physical contact regions (collisions, friction transients) look implausible to robots." — [[11_Sim-to-Real-Transfer#7. Open Problems|11_Sim-to-Real-Transfer §7]]
- Closest substrates: [[2604.16484|DexWorldModel]] (causal latent, [DINOv3](https://arxiv.org/abs/2508.10104) targets, 94% [[2504.13059|RoboTwin]]; continuous contact); [[2503.17973|PhysTwin]] (deformable digital twin; no discrete events); [[2511.07416|PhysWorld]] (continuous physical WM; 82% real SR); [[2604.27367|DOT-Sim]] (differentiable optical tactile; contact ground truth but no WAM consumer).
- Pattern: [[2602.23253|SPARR]] 95–100% [AutoMate](https://arxiv.org/abs/2407.08028); [[2603.15956|ExpertGen]] 90.5% [AutoMate](https://arxiv.org/abs/2407.08028). All policy-side improvements; contact events as first-class WAM latent has not been explored.

**Concrete research questions.**
1. **Q1 — Discrete contact-mode latent** $c_t \in \{\text{no-contact, making, in-contact, breaking, slipping}\}$; predict $c_t$; condition continuous latent dynamics on $c_t$ atop a [[2604.16484|DexWorldModel]]-style causal latent.
2. **Q2 — Contact-mode-conditional physics losses**: Coulomb only in `in-contact`; ballistic only in `no-contact`.
3. **Q3 — Contact-event time prediction** as auxiliary regression head $\hat{t}_{\text{contact}}$ with simulator supervision.
4. **Q4 — Distillation from [[2604.27367|DOT-Sim]]** as teacher; distill contact dynamics into WAM latent.
5. **Q5 — Sim-to-real on [AutoMate](https://arxiv.org/abs/2407.08028) / [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic)**: train on [[2511.04665|Real-to-Sim GS]] twins; eval on real [AutoMate](https://arxiv.org/abs/2407.08028).

**Related research papers.**
- [[2604.16484|DexWorldModel]] — Causal latent WM ([DINOv3](https://arxiv.org/abs/2508.10104) targets); 94% [[2504.13059|RoboTwin]], zero-shot sim2real; continuous contact, no discrete mode.
- [[2503.17973|PhysTwin]] — Physics-informed deformable twin from video; no discrete contact mode.
- [[2511.07416|PhysWorld]] — Policy vs learned physical WM; 82% real SR; continuous, no event discretization.
- [[2604.27367|DOT-Sim]] — Differentiable MPM + tactile; 96.6% tumor detection zero-shot; no WAM consumer.
- [[2603.15956|ExpertGen]] — Generative prior + [DSRL](https://arxiv.org/abs/2506.15799) + distillation; 90.5% [AutoMate](https://arxiv.org/abs/2407.08028); policy-side.
- [[2602.23253|SPARR]] — Sim + vision-conditioned real residual; 95–100% [AutoMate](https://arxiv.org/abs/2407.08028); policy-side, no WAM.
- [[2603.16861|MolmoBot]] — 232K-env procedural [MuJoCo](https://github.com/google-deepmind/mujoco); 79.2% real [Franka FR3](https://franka.de/franka-research-3); domain randomization only.
- [[2511.04665|Real-to-Sim GS]] — 3DGS + soft-body [[2503.17973|PhysTwin]]; ρ > 0.9 sim-real; evaluation substrate.
- [[2604.24916|asRoBallet]] — Friction-aware [MuJoCo](https://github.com/google-deepmind/mujoco) + RL; prior for contact-mode losses.
- [[2604.23702|QuietWalk]] — PINN GRF predictor + curriculum; analog of contact-force prediction.

**Benchmarks & metrics.**
- [AutoMate](https://arxiv.org/abs/2407.08028) (8 tasks) — Insertion / assembly SR; 90.5% is the WAM-naive baseline.
- [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) industrial assembly — Cross-task assembly; [[2602.23253|SPARR]] reports +74.5% relative SR improvement (and 36.5% cycle-time reduction) on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) tasks.
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
| **Anchor surveys** | [[2604.22748\|Agentic World Modeling Survey]], [[2602.04411\|Self-evolving Embodied AI]], [[2508.07407\|Self-Evolving AI Agents Survey]] |
| **Key targets** | Imagined-vs-real SR Pearson ρ > 0.7 + continual per-cycle SR improvement; [[2605.22446\|Pre-VLA]]-style verifier ≥0.83 F1 on bad-rollout filtering; forgetting held to [[2401.16650\|WMAR]]-class 0.071 (vs 0.665 baseline) |

**Why it matters.** [[2604.22748|Agentic World Modeling Survey]] defines L1 Predictor / L2 Simulator / L3 Evolver and calls physical L3 Evolver the gap ("emerging not mature"). The pieces exist — failure detection, GRPO, recovery, memory, and now runtime rollout verification ([[2605.22446|Pre-VLA]], which filters unsafe actions and *truncates unreliable WM imaginations*) — but no system integrates them under a WAM-driven imagination loop. The newly exposed piece: imagination is also a *safety surface* ([[2604.05498|JailWAM]]: 84% attack success on WAMs), so the loop must verify its own dreams, not just learn from them.

**First-principles framing.**
- **First principle**: Preparation is bounded by imagination. An agent can only learn to recover from failure modes it can generate internally, because the recovery policy trains against the failures it sees. So a self-improvement loop's reachable competence is capped by the WM's *generative* coverage of failure, not by logged real interaction. The WM's job is to be the failure-generator.
- **Assumption being challenged**: That self-evolution requires real-world exploration because real experience beats imagined rehearsal. Real failure-finding is expensive and irreversible (robot time, safety). For a WAM accurate enough, imagined failures can drive real improvement with only *periodic* real-world calibration — provided a verifier ([[2605.22446|Pre-VLA]]) gates the unreliable dreams.
- **The bet**: A closed loop — failure-finder → WAM imagines failure → GRPO over (action, imagination) → recovery — achieves continual per-cycle SR improvement at imagined-vs-real Pearson $\rho > 0.7$, *without* catastrophic forgetting ([[2401.16650|WMAR]]-style FIFO + reservoir, +0.071 vs 0.665 baseline).

**Evidence.**
- [[2602.04411|Self-evolving Embodied AI]]'s 5-module framework (memory / task / environment / embodiment / model) is canonical; [[2508.07407|Self-Evolving AI Agents Survey]], [[2507.21046|Self-Evolving Agents Survey]], [[2505.05108|Multi-agent Embodied AI Survey]] all name open-environment self-evolution as the top unresolved capability.
- 2026 components: [[2506.24119|SPIRAL]] (CriticAgent filters dreams), [[2502.05907|EvoAgent]] (+105% [Minecraft](https://www.minecraft.net/en-us)), [[2511.16166|EvoVLA]] (first end-to-end self-evolving VLA), [[2510.16079|EVOLVER]] (trajectory → principles), [[2604.18131|Native Evolution]] (reward-free self-evolution), [[2605.22446|Pre-VLA]] (preemptive verifier that truncates unreliable WM imaginations; +6.83 pp [[2306.03310|LIBERO]]).
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
- [[2506.24119|SPIRAL]] — CriticAgent filters dreams; critic filter only, no full loop.
- [[2511.16166|EvoVLA]] — First end-to-end self-evolving VLA; no WAM imagination driving evolution.
- [[2510.16079|EVOLVER]] — Trajectory → strategic principles; behavior-level, no WAM imagination.
- [[2412.02818|RoboMD]] — RL adversary for failure discovery; probes real robot, not WAM-driven.
- [[2510.09459|FIPER]] — Predictive failure via OOD + uncertainty; detection only, no recovery.
- [[2506.09937|SAFE]] — Internal-feature + conformal prediction; detection only, no recovery.
- [[2509.26354|Misevolution]] — Identifies the risk class; diagnosis only, no in-loop mitigation.
- [[2506.07468|SELF-REDTEAM]] — Adversarial self-play; pre-deployment check, not in-loop.
- [[2509.15194|EVOL-RL]] — Novelty prevents entropy collapse; standalone regularizer, not in-loop.

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
| **Anchor surveys** | [[2604.22748\|Agentic World Modeling Survey]], [[2310.06253\|Objective Mismatch MBRL Survey]], [[2602.04411\|Self-evolving Embodied AI]] |
| **Key targets** | ≥2× WM sample-efficiency + 22% downstream reward ([[2604.01985\|WAV]]); epistemic-uncertainty gating 0.91 reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/) ([[2504.16680\|RWM-U]]); imagined-vs-real ρ as the calibration metric (links to B2) |

**Why it matters.** B2 detects and recovers from failure at *runtime*; B3 asks whether the WM can be made trustworthy at *training time* so the runtime loop has less to clean up. [[2604.22748|Agentic World Modeling Survey]]'s L3 Evolver "revises its own model when predictions fail" — but the usual tool for knowing *when* a prediction failed is uncertainty estimation, which [[2604.01985|WAV]] shows "often fails in under-explored data regions where new information is most needed," exactly where calibration matters. [[2310.06253|Objective Mismatch MBRL Survey]] generalizes it: low predictive WM loss does not imply high downstream return, so the WM's own training signal is miscalibrated against policy need. Two results reframe the problem. [[2604.01985|WAV]] exploits a structural *asymmetry* — verifying a transition (inverse) is cheaper and more robust than generating it (forward) — to turn verification into a self-improving training cycle. [[2504.16680|RWM-U]] shows an ensemble's epistemic uncertainty, used to *penalize* imagined rollouts, makes offline MBRL work on real quadrupeds and humanoids. Calibration of imagination is a train-time lever, not a runtime patch.

**First-principles framing.**
- **First principle**: Forward generation and inverse verification are not symmetric. Action-free video is abundant, so state-plausibility is cheap to learn; action-relevant features are low-dimensional, so action-reachability can be verified robustly from little labeled data. A verifier built on this asymmetry is *structurally* cheaper and more sample-efficient than the generator it checks — independent of model scale.
- **Assumption being challenged**: That the WM-reliability gap closes by estimating uncertainty better. [[2604.01985|WAV]] shows naive uncertainty fails exactly in the under-explored regions where it is needed; [[2504.16680|RWM-U]] shows uncertainty is useful only when it *gates* the objective (penalizing reward), not when it merely reports confidence. The field treats verification as a runtime filter on a finished dream; B3 treats it as the training signal that shapes the dream.
- **The bet**: A forward-inverse asymmetry signal (subgoal-plausibility checked by an action-free generator + action-reachability checked by a sparse inverse model) yields ≥2× WM sample-efficiency and +22% downstream reward with *no extra action labels* ([[2604.01985|WAV]]'s result, here as a verifier-in-the-training-loop bet), with epistemic-uncertainty gating reaching 0.91 normalized reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/) ([[2504.16680|RWM-U]]). Distinct from B2: B2 is the runtime detect→recover loop; B3 is the train-time calibration that makes imagination trustworthy in the first place.

**Evidence.**
- [[2604.01985|WAV]] — Splits verification into state-plausibility (action-free subgoal generator) + action-reachability (sparse inverse dynamics); the cycle prioritizes data where plausible-future and predicted-future disagree most; 2× WM sample-efficiency, +22% reward across six manipulation tasks.
- [[2504.16680|RWM-U]] — Ensemble epistemic uncertainty penalizes imagined rollouts ([MOPO-PPO](https://arxiv.org/abs/2005.13239)); uncertainty tracks true long-horizon error; 0.91 normalized reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/), deployed on [Unitree G1](https://www.unitree.com/g1/).
- [[2310.06253|Objective Mismatch MBRL Survey]] — Predictive WM loss does not correlate with downstream return; the training signal is miscalibrated against policy need — the gap B3 closes.
- [[2604.22748|Agentic World Modeling Survey]] — L3 Evolver revises its model when predictions fail; B3 supplies the *when-it-failed* signal as a train-time objective, not a runtime probe.
- [[2605.22446|Pre-VLA]] — Runtime verifier that truncates unreliable imaginations (+6.83 pp [[2306.03310|LIBERO]]); B3 is its train-time complement — calibrate so there is less to truncate.

**Concrete research questions.**
1. **Q1 — Forward-inverse verifier on a latent WAM.** Wrap [[2604.01985|WAV]]'s subgoal-generator + sparse-inverse decomposition around a JEPA WAM ([[2602.10098|VLA-JEPA]] / [[2605.25313|UWM-JEPA]]); measure sample-efficiency vs uncertainty-only baseline.
2. **Q2 — Epistemic-uncertainty gating as a dense reward.** Adapt [[2504.16680|RWM-U]]'s [MOPO](https://arxiv.org/abs/2005.13239) penalty to a latent-consistency reward on A1's hybrid backbone; does penalizing high-uncertainty imagined states stabilize the latent-rollout objective?
3. **Q3 — Calibration metric = imagined-vs-real ρ.** Treat the B2 ρ > 0.7 gate as B3's *objective*, not just a stop condition: train the WM to maximize imagined-vs-real SR correlation directly.
4. **Q4 — Active data collection from verifier disagreement.** Use [[2604.01985|WAV]]'s discrepancy signal to drive which real-robot interactions to collect next; close the loop with B2's failure-finder.
5. **Q5 — Sparse-vs-dense inverse ablation.** Does the sparse inverse model's OOD robustness ([[2604.01985|WAV]]) hold on contact-rich tasks (shared substrate with B1's discrete contact modes)?

**Related research papers.**
- [[2604.01985|WAV]] — Forward-inverse asymmetry self-improving cycle; 2× sample-eff, +22% reward; no extra labels; the calibration-as-training exemplar.
- [[2504.16680|RWM-U]] — Uncertainty-aware WM + [MOPO-PPO](https://arxiv.org/abs/2005.13239); 0.91 reward real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/); uncertainty must gate the objective, not just report.
- [[2310.06253|Objective Mismatch MBRL Survey]] — Decision-aware MBRL; predictive loss ⊥ return; names the miscalibration B3 targets.
- [[2605.22446|Pre-VLA]] — Preemptive runtime verifier; +6.83 pp [[2306.03310|LIBERO]]; runtime filter, not train-time calibration.
- [[2510.09459|FIPER]] — Predictive failure via OOD + uncertainty; detection only, no calibration training signal.
- [[2506.09937|SAFE]] — Internal-feature + conformal prediction; calibrated detection, but post-hoc not in WM training.
- [[2510.16281|SEAL]] — Runtime CoT-faithfulness verifier; +15 pp; verifies plan↔outcome, not WM imagination.
- [[2604.22748|Agentic World Modeling Survey]] — L3 Evolver framework; survey, no calibration method proposed.
- [[2603.04029|Self-Adapting RL]] — Outer-loop WM adaptation; complements B3's inner calibration signal.
- [[2604.19092|RoboWM-Bench]] — Visual plausibility ≠ executability; the gap a calibrated WM must close, measured.

**Benchmarks & metrics.**
- WM sample-efficiency curve — prediction error vs labeled-interaction budget; [[2604.01985|WAV]] reports 2× improvement; the headline calibration metric.
- Downstream reward across manipulation tasks — [[2604.01985|WAV]] +22% over strong baselines on six tasks.
- Real-robot normalized reward — [[2504.16680|RWM-U]] 0.91 on [ANYmal D](https://www.anybotics.com/robotics/anymal/), deployed on [Unitree G1](https://www.unitree.com/g1/); sim-to-real validity of calibration.
- Imagined-vs-real SR Pearson ρ — shared with B2; B3 maximizes it directly rather than gating on it.

> [!warning] Risks
> - **Sparse inverse model misses subtle dynamics**: low-dimensional action features may drop contact transients. → Bound the claim to where action-relevant features are recoverable; pair with B2's discrete contact modes for contact-rich regimes.
> - **Uncertainty gating too conservative**: penalizing all high-uncertainty states kills exploration ([[2504.16680|RWM-U]]'s penalty coefficient is a critical hyperparameter). → Tune the penalty on a held-out real-robot calibration set, not in simulation alone.
> - **Calibration ≠ correctness**: a WM can be well-calibrated about being wrong. → Validate against B2's imagined-vs-real ρ AND the joint causal-binding metric developed in the umbrella [[Embodied-AI|Embodied-AI]], not calibration alone.

---

## Cross-Cutting Themes

> [!tip] Latent Prediction Is the Dominant Substrate — and Now Has a Formal Membership Test
> A1, A2, and B2 all assume "video at training, latent at deployment" with JEPA / DiT-on-latent backbones. The field has lacked a test for *when* a learned latent is actually a world model. [[2605.26379|LeJEPA World Model]] supplies it (identifiable iff isotropic-Gaussian, then latent planning matches an oracle); [[2605.25313|UWM-JEPA]] extends the substrate to belief space. So A1's hybrid latents, A2's tactile-imagination latent, and B2's self-evolution rollouts answer to one membership test instead of convention — as do the deploy-time memory latents of [[Spatial-4D|Spatial-4D]]-C4.

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
| Hybrid latent+pixel/3DGS vs pure-latent vs pure-pixel WAM at matched FLOPs (OOD × latency × interpretability cube) | A1 | [[2605.20752\|GaussianDream]] (train-dense/deploy-light, single point on the cube) + [[2605.06388\|Semantic-LDM-WM]] (semantic vs reconstruction latent, no pixel branch) |
| WAM with a tactile/force *prediction* head (imagined wrench, not consumed force) | A2 | [[2506.14754\|Sparsh-X]] (touch encoder, no prediction head) + [[2604.20444\|VTouch++]] (synchronized dataset, no WAM consumer) |
| Discrete contact-mode latent; sub-millimeter assembly SR with contact-aware imagination | B1 | [[2604.16484\|DexWorldModel]] (causal latent but continuous contact) + [[2604.27367\|DOT-Sim]] (contact ground truth, no WAM consumer) |
| Integrated detection→diagnosis→recovery loop with WAM-driven imagination + rollout verification | B2 | [[2605.22446\|Pre-VLA]] (verifier only, no full loop) + [[2605.10921\|RoboMemArena]] (memory-dependent recovery, no imagination loop) |
| Forward-inverse calibration as a *training* signal (not a runtime filter) tied to imagined-vs-real ρ | B3 | [[2604.01985\|WAV]] (asymmetry cycle, not ρ-objective) + [[2504.16680\|RWM-U]] (uncertainty gating, locomotion only) |

---

## Cross-References

- [[04_WAM|04_WAM]] — WAM taxonomy (VideoGen / latent / Dreamer / VLM-integrated / efficient / self-evolving)
- [[05_Latent-World-Models|05_Latent-World-Models]] — JEPA + alternative latent models; latent reasoning
- [[06_Self-Evolving-VLA-WAM|06_Self-Evolving-VLA-WAM]] — Failure detection, diagnosis, recovery; self-evolution mechanisms
- [[07_Physics-Aware-Embodied-AI|07_Physics-Aware-Embodied-AI]] — Physics-aware design space; physics commonsense benchmarks
- [[11_Sim-to-Real-Transfer|11_Sim-to-Real-Transfer]] — Sim-to-real strategies; learned simulators; reality-gap diagnostics
- [[08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — Canonical survey index
- [[Embodied-AI|Embodied-AI]] — Umbrella directions. Joint WAM–policy co-evolution, physics-consistency verification, joint causal-consistency evaluation, real-time deployment, and cross-embodiment transfer live there (B1, B3, C1, C3, D2) — omitted here to avoid duplication.
- [[Spatial-4D|Spatial-4D]] — Sibling doc on the model-agnostic 3D/4D representation — occupancy & 4D world models, geometric memory ([[2604.26694|X-WAM]], [[2603.17117|MosaicMem]]).
- [[Sim2Real|Sim2Real]] — Sibling doc on sim-to-real / real-to-sim transfer; borders this doc's physics-grounding (B-cluster) and world-model-as-simulator themes.
