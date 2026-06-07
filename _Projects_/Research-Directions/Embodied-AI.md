---
title: "Promising Research Directions: VLA × WAM × Embodied AI"
aliases:
  - "VLA-WAM Promising Directions"
  - "Embodied-AI Research Directions"
tags:
  - research-directions
  - VLA
  - WAM
  - embodied-AI
  - self-evolving
---

# Promising Research Directions: VLA × WAM × Embodied AI

> [!abstract] Overview
> Nine **cross-cutting, embodiment-agnostic** research directions at the VLA × World-Action-Model × Embodied-AI intersection. Each one is a *mechanism* — a training objective, an evaluation, a way to move or transfer — that holds for **any** robot body. They group into three clusters: *Architecture & Training* (A), *Evaluation, Robustness & Deployment* (B), and *Mobility & Embodiment Generalization* (C). Three sources feed them: ~56 VLA/WAM/embodied surveys, ten `Embodied-AI/` deep-dives, and the **frontier methods and benchmarks that set each bet's bar** ([[2605.08567|ACWM-Phys]], [[2605.21800|stable-worldmodel]], [[2605.06311|VISER]], [[2605.20774|VLA-REPLICA]], [[2605.21429|roto 2.0]], [[2603.29165|LatentPilot]], [[2505.14986|AnyBody]]).
> Clusters A–B treat the model as a fixed-base tabletop arm. Cluster C moves it through the world (navigation) and transfers it across bodies (cross-embodiment, morphology-invariance). For a **single embodiment broken down by physical subsystem**, see the sibling docs [[Manipulation|Manipulation]] (arms + hands), [[Locomotion|Locomotion]] (legs + wheels), and [[Whole-Body|Whole-Body]] (the loco-manipulation coupling).
> Each direction states a **first-principles framing** (the irreducible structure, the assumption it breaks, a **measurable bet**) and a **non-consensus thesis**. Every metric anchor comes from a cited `_KnowledgeHub_/{ID}.md` note — never invented.

---

## Methodology

**Scope.** Corpus: ~56 VLA/WAM/embodied/physics/safety surveys and ~120 method + benchmark papers from `_KnowledgeHub_/`, cross-checked against [[08_Benchmarks-and-Surveys#4. Robotics & Embodied AI Surveys|08_Benchmarks-and-Surveys §4]]/[[08_Benchmarks-and-Surveys#5. Self-Evolving AI Surveys|§5]]/[[08_Benchmarks-and-Surveys#7. Specialized Domain Surveys|§7]] and ten `Embodied-AI/` deep-dives. **Filter**: kept directions with 3–10 papers attacking them but no agreed solution; dropped saturated (more-compute-only) and premature (hypothetical-AGI) framings; favored intersections (VLA×WAM, VLA×RL, WAM×egocentric, tactile×VLA, physics×RL, safety×deployment). The recipe: surveys name the open problem, benchmarks say what's measurable, the closest methods say what's reachable today, and each direction states where it bets against the crowd.

- **Survey enumeration**: tag-scans (`survey` × {`VLA`, `world-model`, `embodied-AI`, `robotics`, `physics-aware`, `sim-to-real`, `safety`, `self-evolving`}) over `_KnowledgeHub_/` + reference sweeps of [[05_VLA|05_VLA]], [[07_WAM|07_WAM]], [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]].
- **Deep-dive mining**: full reads of the six deep-dives directly aligned with the directions ([[07_WAM|07_WAM]], [[13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]], [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]], [[06_VLA-Reasoning-and-CoT|06_VLA-Reasoning-and-CoT]], [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]], [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]]); others consulted for taxonomy framing.
- **Closest-baseline anchoring**: physics-generalization, reproducible-eval, and sim-realism benchmarks ([[2605.08567|ACWM-Phys]], [[2605.21800|stable-worldmodel]], [[2605.06311|VISER]], [[2605.20774|VLA-REPLICA]], [[2605.21429|roto 2.0]]) and the named-bottleneck roadmaps ([[2511.05936|10 VLA Challenges]], [[2605.02900|Safety in Embodied AI Survey]]) set the bar A3, B1, B2, B3 must beat or measure against.
- **First-principles framing**: each direction names the irreducible structure, the assumption it breaks, and a falsifiable bet — to surface where impactful work deviates from the herd.

---

## Survey Landscape

| Survey | Sub-theme | Key open problems |
|---|---|---|
| [[2605.12090\|WAM Survey]] | A: WAM | Causal-consistency joint metrics; data-ecosystem mixing; separate WM-vs-action eval gap; tactile/force/acoustic extension; long-horizon drift; closed-loop latency |
| [[2605.00080\|WM Robot Learning Survey]] | A: WAM | Eval beyond visual fidelity; closed-loop vs open-loop; latent WM dominance; causal conditioning; failure-recovery datasets; cross-embodiment |
| [[2604.04974\|Video-to-Control Survey]] | A: WAM | Integration layer is critical gap; interface trade-offs; tracking-error; latent-action identifiability; pre-execution verification; tactile/force integration |
| [[2604.22748\|Agentic World Modeling Survey]] | A: WAM | Counterfactual reasoning; constraint adherence; autonomous self-revision (L3 Evolver); decision-centric metrics (ASR + COD) |
| [[2604.04707\|OpenWorldLib]] | A: WAM | Definition fragmentation; 3D geometric consistency under camera motion; modular pipeline composition |
| [[2604.02029\|Latent Space Survey]] | A: WAM | Evaluability/controllability/interpretability; theory gap; modality-native integration; governable latent AI |
| [[2602.01630\|Unified World Model Framework]] | A: WAM | Fragmentation; need integrated module architecture; holistic understanding gap |
| [[2511.02097\|WM Manipulation Survey]] | A: WAM | Structured task-relevant representations; hierarchical architectures for long-horizon |
| [[2510.16732\|World Models for Embodied AI Survey]] | A: WAM | Unified datasets; physically-consistent metrics beyond FID/FVD; long-horizon temporal consistency; SSM/hybrid AR-global; WM × LLM-CoT synergy |
| [[2506.20134\|3D World Models Survey]] | A: WAM | 3D spatial understanding under-developed |
| [[2504.21853\|Interactive Generative Video Survey]] | A: WAM | Real-time vs quality; persistent memory; dynamics fidelity; cross-domain transferability |
| [[2503.04641\|Multimodal Generative Models Survey]] | A: WAM | Cross-modal dependency; sparse 4D integration; comprehensive simulators |
| [[2601.15533\|Actionable Simulators]] | A: WAM | Dynamical hallucinations; structured 4D interfaces; self-evolution; closed-loop decision-oriented eval |
| [[2411.14499\|World Models Survey]] | A: WAM | Physical-rule adherence; standardized benchmarks; sim2real; ethics/safety; interactive 3D action-conditioned WMs |
| [[2604.15395\|Foundation Models in Robotics Survey]] | A: Embodied AI | Tactile/failure-data scarcity; embodiment-agnostic action spaces; latency; long-horizon memory; physics-informed WMs; formal verification |
| [[2509.20021\|Embodied AI LLM-WM Survey]] | A: Embodied AI | MLLM-WM unified architecture; integration patterns |
| [[2507.00917\|Embodied Intelligence Survey]] | A: Embodied AI | Sim2Real gap; unified capability framework; WMs as neural simulators |
| [[2505.07634\|Neural Brain Framework]] | A: Embodied AI | Multimodal active sensing; closed-loop perception-cognition-action; neuroplasticity memory; neuromorphic co-design |
| [[2504.01990\|Foundation Agents Survey]] | A: Embodied AI | Autonomous + adaptive + safe agents; AI-cognition mapping; collaboration |
| [[2407.06886\|ARIO]] | A: Embodied AI | Sim2Real gap; data heterogeneity; MLM + WM integration |
| [[2311.00530\|LLM Embodied Navigation Survey]] | A: Embodied AI | Long-horizon planning grounding; context-window limits; multimodal grounding |
| [[2510.07077\|VLA Robotics Real-World Review]] | A: VLA | Embodiment transfer; data scarcity; computational cost; eval+safety; gradient insulation/PEFT/inference optimization |
| [[2509.19012\|Pure VLA Survey]] | A: VLA | Data scarcity; architectural heterogeneity; real-time inference; eval fragmentation; world modeling + causal reasoning |
| [[2508.13073\|Large VLM-based VLA Survey]] | A: VLA | Partially superseded by later 2025 reviews |
| [[2507.10672\|VLA Manipulation Survey]] | A: VLA | Multimodal × high-complexity data gap; simulator fidelity-vs-throughput; native language-grounding APIs |
| [[2506.20966\|VLA Post-Training Survey]] | A: VLA | Generalization-vs-precision; knowledge insulation during RL |
| [[2505.04769\|VLA Concepts Survey]] | A: VLA | Real-time inference (AR 3–5 Hz); safety (~82% collision); generalization gap (~40%); dual-system + LoRA |
| [[2604.27621\|Robot Learning from Human Videos Survey]] | B: Modalities & Data | Action-oriented transfer; physically-grounded WMs; physics-aware affordance; continual learning; multi-agent; tactile/audio/gaze; low-quality-video robustness |
| [[2604.26509\|3D Generation for Embodied AI Survey]] | B: Modalities & Data | Physical-annotation scarcity; geometry-vs-physics; deformables; sim-to-real |
| [[2604.28185\|Visual Generation Survey]] | B: Modalities & Data | Spatial reasoning + physical-law gaps in frontier models; multi-turn editing degradation; L4 agentic frontier |
| [[2504.03515\|Dexterous IL Survey]] | B: Modalities & Data | Tactile integration; cross-embodiment transfer; demo scaling |
| [[2604.16592\|Cognition WM Survey]] | B: Physics & Cognition | Motivation + meta-cognition drastically under-developed; epistemic WMs over structured knowledge |
| [[2510.04978\|Physical AI Survey]] | B: Physics & Cognition | Causal understanding missing; compositional/causal structure; hybrid Neural Physics |
| [[2503.21765\|Physics Cognition Survey]] | B: Physics & Cognition | Sub-human physics (multi-object/fluid); limited physical coverage; computational inefficiency; sim2real; physics foundation + neuro-symbolic |
| [[2601.07823\|Video Generation in Robotics Survey]] | B: Physics & Cognition | Hallucinations + physics violations; uncertainty; long videos; compute; robotics-centric benchmarks |
| [[2501.10928\|Generative Physical AI Survey]] | B: Physics & Cognition | Functional vs visual realism; physical plausibility metrics; material fidelity |
| [[2509.25373\|VLM Perception-Cognition Survey]] | B: Physics & Cognition | Shallow perception-cognition integration; pixel-to-world-model translation; hallucination from disjoint coupling |
| [[2604.00061\|R2X Multi-Robot MLLM Survey]] | B: Multi-agent | Bandwidth; open-vocab perception; joint sensing/comms/compute |
| [[2505.05108\|Multi-agent Embodied AI Survey]] | B: Multi-agent | Async decisions; heterogeneous teams; self-evolution in open environments; nascent benchmarks |
| [[2508.07407\|Self-Evolving AI Agents Survey]] | B: Self-Evolution | Continuous self-improvement w/o forgetting; evolution-evaluation gap; safety + alignment under self-modification |
| [[2507.21046\|Self-Evolving Agents Survey]] | B: Self-Evolution | Adaptivity / retention / generalization / efficiency / safety as 5 eval gaps; emergent risks |
| [[2602.04411\|Self-evolving Embodied AI]] | B: Self-Evolution | "Human-crafted settings" limit; multi-timescale closed-loop co-evolution; integration of WM/memory/embodiment |
| [[2404.14387\|LLM Self-Evolution Survey]] | B: Self-Evolution | Lifelong-learning forgetting; self-generated experience quality; alignment under self-evolution |
| [[2507.21045\|4D Spatial Intelligence Survey]] | B: Spatial Intelligence | Cross-level eval; physics-aware 4D reconstruction; interactive 4D editing |
| [[2512.24385\|Spatial Intelligence Roadmap]] | B: Spatial Intelligence | Single → unified pre-training; 3D data scarcity; generative WM × spatial reasoning |
| [[2504.09848\|LLM Spatial Intelligence Survey]] | B: Spatial Intelligence | Fragmented research; unsystematized LLM cognitive foundations; deployment limits |
| [[2504.15037\|MLLM Spatial Reasoning Position Paper]] | B: Spatial Intelligence | Scaling won't fix spatial gaps; data/architecture/objective/eval limits; spatial-specific recipes |
| [[2605.03941\|iWorld-Bench]] | C: Eval & Benchmarking | Standardized interactive evaluation across WAM types |
| [[2511.05936\|10 VLA Challenges]] | C: Eval & Benchmarking | OOD brittleness; data quality; resource efficiency; safety assurances; cross-robot generalization; whole-body coordination as named bottlenecks |
| [[2310.06253\|Objective Mismatch MBRL Survey]] | C: Eval & Benchmarking | Decision-aware MBRL; predictive-loss vs return alignment; cross-family fragmentation |
| [[2103.04918\|Embodied AI Survey]] | C: Eval & Benchmarking | Simulator-task interconnections; realistic-physics + interactive-objects; cross-simulator benchmarking |
| [[2605.05017\|SPINE]] | C: Safety | Compositional leakage; regulatory-technical gap; non-linear utility trade-off (~30% SR drop); adaptive orchestration |
| [[2605.02900\|Safety in Embodied AI Survey]] | C: Safety | Five-layer attack taxonomy (perception→cognition→planning→action); cascade propagation; agentic risks (tool misuse, memory poisoning, data leakage); self-evolving misalignment |
| [[2604.23775\|VLA Safety Survey]] | C: Safety | Multi-layered defense; fragmented evaluation methodology |
| [[2604.15911\|Efficient Video Diffusion Survey]] | C: Efficiency | KV cache movement; 1–4 step distillation; sparse attention; QAT/PTQ |
| [[2603.28489\|Video Gen as WM Survey]] | C: Efficiency | Efficiency as prerequisite; distillation/sparse attention/quantization; integrated efficiency |
| [[2510.24795\|Efficient VLA Survey]] | C: Efficiency | Latency/control freq incompatible w/ edge; pre-training cost; data collection; embodiment-agnostic; self-sustaining data |

> [!tip] Convergence patterns
> - **Joint WM-action evaluation gap** (5-way): [[2605.12090|WAM Survey]], [[2605.00080|WM Robot Learning Survey]], [[2510.16732|World Models for Embodied AI Survey]], [[2601.15533|Actionable Simulators]], [[2601.07823|Video Generation in Robotics Survey]] — same diagnosis under different vocabulary (causal consistency / closed-loop / physically-consistent metrics). Now operationalized: [[2605.06311|VISER]] reports sim-real Pearson **r = 0.92** and [[2605.21800|stable-worldmodel]] shows planning SR decays sharply under mild perturbation even when in-dist SR is 92–94%.
> - **Physical grounding / dynamical hallucinations** (5-way): [[2503.21765|Physics Cognition Survey]], [[2510.04978|Physical AI Survey]], [[2601.15533|Actionable Simulators]], [[2411.14499|World Models Survey]], [[2501.10928|Generative Physical AI Survey]] — converge on hybrid neural-symbolic + verifiable-physics. [[2605.08567|ACWM-Phys]] now *quantifies* the InD→OOD physical-generalization cliff (InD SSIM 0.988 → OOD ΔM-MSE up to +40 on robot-arm / +30 on cloth).
> - **Data scarcity** (6-way): [[2604.15395|Foundation Models in Robotics Survey]], [[2604.27621|Robot Learning from Human Videos Survey]], [[2509.19012|Pure VLA Survey]], [[2507.10672|VLA Manipulation Survey]], [[2407.06886|ARIO]], [[2512.24385|Spatial Intelligence Roadmap]] — internet-scale human video + massively-parallel sim + self-exploration as dominant scaling levers.
> - **Efficiency as prerequisite** (3-way): [[2510.24795|Efficient VLA Survey]], [[2603.28489|Video Gen as WM Survey]], [[2604.15911|Efficient Video Diffusion Survey]] — KV-cache movement is the major DiT bottleneck; [[2505.04769|VLA Concepts Survey]]'s 3–5 Hz AR ceiling is the quantitative anchor; [[2511.05936|10 VLA Challenges]] names resource efficiency as one of ten named bottlenecks.
> - **Self-evolution / autonomous adaptation** (6-way): [[2602.04411|Self-evolving Embodied AI]], [[2604.16592|Cognition WM Survey]], [[2604.22748|Agentic World Modeling Survey]], [[2508.07407|Self-Evolving AI Agents Survey]], [[2507.21046|Self-Evolving Agents Survey]], [[2404.14387|LLM Self-Evolution Survey]] — meta-cognition / autonomous self-revision is the missing function.
> - **Safety as a deployment-blocking axis** (4-way, *strengthened this pass*): [[2605.02900|Safety in Embodied AI Survey]] (five-layer attack taxonomy + cascade propagation), [[2604.23775|VLA Safety Survey]], [[2605.05017|SPINE]], [[2511.05936|10 VLA Challenges]] (safety assurances named explicitly) — the field is converging on the realization that adversarial/jailbreak robustness and self-evolving misalignment are not separable from the evaluation and memory loops they corrupt.
> - **Definition fragmentation** (meta): [[2604.04707|OpenWorldLib]], [[2510.16732|World Models for Embodied AI Survey]], [[2411.14499|World Models Survey]], [[2602.01630|Unified World Model Framework]] — field still pre-paradigmatic; empirical convergence outpaces terminology.

---

## Formal Framing

**Probabilistic** — three families of conditional distributions:

| Family | Joint distribution | Predicts |
|---|---|---|
| **VLA** (Vision-Language-Action) | $p(a \mid o, l)$ | Action conditioned on observation + language; no dynamics |
| **WM** (World Model) | $p(o' \mid o, a)$ | Next observation conditioned on action; no action policy |
| **WAM** (World Action Model) | $p(o', a \mid o, l)$ | Both — the unifying frontier |

Per [[2605.12090|WAM Survey]]:

> "WAMs are defined as embodied foundation models that integrate predictive state modeling with action generation, moving beyond merely predicting actions to predicting a joint distribution over future states and actions." — [[2605.12090|WAM Survey]]

Joint loss:

$$\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o,l,o',a) \sim \mathcal{D}} \big[ -\log p(o', a \mid o, l) \big]$$

WAMs split into **Cascaded** (predict state, derive action via inverse dynamics) vs **Joint** (unified end-to-end). Most "joint" methods are actually Cascaded — Joint is the architectural frontier.

**By I/O modality** — the same families seen through what each model *consumes* and *emits*:

| Input modality | Output modality | Application | Joint distribution |
|---|---|---|---|
| Text \| Image \| Video | Video | **Video Model** | $p(o' \mid o, l)$ |
| Text \| Video | Text | **Vision-Language Model (VLM)** | $p(l' \mid o, l)$ |
| Action \| Image \| Text | Video | **Forward Dynamics Model** | $p(o' \mid o, a)$ |
| Text \| Video | Action | **Inverse Dynamics Model** | $p(a \mid o, o')$ |
| Image \| Text | Video & Action | **Policy Model** | $p(o', a \mid o, l)$ |

where $o$ = observation (image/video), $a$ = action, $l$ = language/text, and a prime marks the predicted output ($o'$ a future observation, $l'$ generated text) — the same symbols as the **VLA / WM / WAM** families above. **Forward Dynamics Model** is exactly the **WM** row ($p(o' \mid o, a)$) and **Policy Model** is exactly the **WAM** row ($p(o', a \mid o, l)$); the modality view and the probabilistic view are two cuts of one taxonomy.

- **Video Model** — generates future video from a text / image / video prompt with *no action conditioning*; a pure generative simulator of *what could happen*, not *what happens if I act*. The substrate that Forward Dynamics and Policy models become once an action input is added.
- **Vision-Language Model (VLM)** — consumes vision + language and emits language (captioning, VQA, embodied reasoning); perception and understanding only — it neither renders pixels nor outputs actions, so it sits *upstream* of control.
- **Forward Dynamics Model** — predicts the next observation given the current one *plus an action*; the action-conditioned learned simulator that lets a policy "imagine forward" (the **WM** row above).
- **Inverse Dynamics Model** — infers the action(s) that explain an observed transition (video) toward a goal (text); the lever that recovers action labels from action-free human video and underwrites the Cascaded WAM route.
- **Policy Model** — given an observation + instruction, emits *both* an imagined future (video) *and* the action to take, fusing Forward Dynamics' imagination with the policy's control in one pass (the **WAM** / Joint frontier, A1).

**Architectural** — per [[2510.16732|World Models for Embodied AI Survey]]:

> "The world models are categorized along three axes: Functionality (Decision-Coupled vs General-Purpose), Temporal Modeling (Sequential Simulation vs Global Difference Prediction), and Spatial Representation (Global Latent Vector, Token Feature Sequence, Spatial Latent Grid, Decomposed Rendering Representation)." — [[2510.16732|World Models for Embodied AI Survey]]

Spatial axis trajectory: latent vectors → token sequences → explicit 3D rendering (NeRF, 3DGS).

**Capability hierarchy** — per [[2604.22748|Agentic World Modeling Survey]]:

> "We introduce three capability levels: L1 Predictor, which learns one-step local transition operators; L2 Simulator, which composes them into multi-step, action-conditioned rollouts that respect domain laws; and L3 Evolver, which autonomously revises its own model when predictions fail against new evidence." — [[2604.22748|Agentic World Modeling Survey]]

L3 Evolver is "emerging not mature" for physical-world policies — the target for B2 (memory + recovery) and the constraint B1 (joint eval) must measure. ASR (Action Success Rate) + COD (Counterfactual Outcome Deviation) are the survey's proposed decision-centric metrics, anchoring B1.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Architecture & Training** | A1, A2, A3 | Training objectives don't match causal structure of physical reasoning | A1's latent co-evolving substrate exposes the intermediate tokens A2 needs for step rewards; A3's physics-verifiable rewards stabilize A1's joint loop |
| **B — Evaluation, Robustness & Deployment** | B1, B2, B3, B4 | Lab-to-real deployment gap (3–5 Hz ceiling, no joint metrics, no recovery loops, forgetting under fine-tune) | B1's joint causal-consistency metric measures whether A1/A3 gains transfer; B2's memory + recovery loop needs B3's efficiency co-design; B4's forgetting-free fine-tune is the precondition for B2's continual recovery updates not to erase prior skills; safety ([[2605.02900\|Safety in Embodied AI Survey]]) cuts across all four |
| **C — Mobility & Embodiment Generalization** | C1, C2 | Policies assume a fixed base + fixed body; moving through the world and across morphologies breaks both (drift, 0% extrapolation) | C1's latent dream-ahead is the navigation analog of A1's latent loop; C2's morphology-invariant representation carries the *structure-preserving* lens — per-morphology retraining doesn't survive the OOD body. |

---

## Cluster A — Architecture & Training: How the Model Learns

*Training objectives and architectural choices that align with the causal structure of physical reasoning.*

### A1 — Single-Loop Co-Evolving Policy + World Model in Latent Space

| | |
|---|---|
| **Cluster** | A — Architecture & Training |
| **Thesis** | Train the policy and world model in one loop, not cascaded or alternating. The data carries $p(o',a\mid o,l)$ as one joint distribution, so a joint objective is the natural loss. The field assumes WM↔policy alternation is needed for stability. The bet: a single-step joint gradient on a unified latent backbone beats alternating training on *both* in-dist SR (≥97.2% [[2306.03310\|LIBERO]]) and OOD SR (≥79.5% [[2510.13626\|LIBERO-Plus]]), at no latency cost (latent ~10 ms vs pixel ~150 ms). |
| **Anchor surveys** | [[2605.12090\|WAM Survey]], [[2605.00080\|WM Robot Learning Survey]], [[2604.22748\|Agentic World Modeling Survey]] |
| **Key targets** | [[2306.03310\|LIBERO]] 97.2% in-dist; [[2510.13626\|LIBERO-Plus]] 79.5% OOD; latent ~10 ms inference (vs pixel ~150 ms) |

**Why it matters.** [[2605.12090|WAM Survey]] defines WAMs via $\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o,l,o',a)\sim\mathcal{D}}[-\log p(o', a \mid o, l)]$ and names Joint over Cascaded as the frontier; [[2605.00080|WM Robot Learning Survey]] agrees on "single-backbone, unified VLA, latent world-modeling." Current "joint" methods fall short: [[2602.12063|VLAW]] alternates, [[2603.16666|Fast-WAM]] drops the WM at deployment, [[2605.15153|Pelican-Unified]] unifies the architecture but trains multi-stage, and [[2511.09515|WMPO]] / [[2511.15605|SRPO]] freeze the WM during inner RL. The gap: a single GRPO loop on joint $(action, imagination)$ log-prob with cooperative gradient flow has not been shown.

**First-principles framing.**
- **First principle**: One stream of data already pairs each future observation with the action that caused it, given the current view and the instruction — the world model and the policy are learning two halves of the *same* distribution. Train them with separate losses and you throw away that link. So one joint loss is the natural choice; training them in stages is the exception that needs a reason.
- **Assumption being challenged**: That you must alternate world-model and policy updates to keep training stable. Modern latent backbones — with a slow-moving target copy and a geometry term that stops the latent from collapsing ([[2511.08544|LeJEPA]]) — may make a single joint update stable enough that alternation is just a leftover from the pixel-space era.
- **The bet**: One backward pass over a shared latent backbone beats alternating training on *both* in-distribution SR (≥97.2%) and OOD SR (≥79.5% [[2510.13626|LIBERO-Plus]]), at no extra latency.

**Evidence.**
- **Closest single-loop attempts**: [[2603.19370|VAMPO]] (GRPO over video-denoising-as-MDP; pixel-space, expensive), [[2602.13977|WoVR]] (masked GRPO + KIR + PACE; PACE not in code), [[2511.09515|WMPO]] (on-policy GRPO; WM frozen in inner loop), [[2511.15605|SRPO]] (frozen [[2506.09985|V-JEPA 2]]; WM doesn't update). The inverse case — [[2606.02486|AHEAD]] freezes the *policy* and trains only a 4.9M-param latent WM around it (>**95%** sim conveyor SR) — shows even the opposite freeze isn't co-evolution: one side is always held fixed.
- **Latent feasibility** ([[05_VLA#5. World-Model-Augmented VLAs|05_VLA §5]] + [[07_WAM#5. VLM-Integrated WAMs|07_WAM §5]]): [[2602.10098|VLA-JEPA]], [[2602.11832|JEPA-VLA]], [[2605.00078|Being-H0.7]] predict in 256-dim latent (~10 ms) vs pixel ~150 ms.
- **Stability substrate**: [[2511.08544|LeJEPA]]'s provable Euclidean geometry (anti-collapse regularization) is the candidate that lets single-step joint updates avoid the latent-collapse failure mode.

**Concrete research questions.**
1. **Q1 — Unified GRPO in latent space.** Given a pretrained latent WAM ([[2504.02792|UWM]] or [[2602.10098|VLA-JEPA]]), $\mathcal{L} = \mathbb{E}[A \cdot \log \pi(a, \hat{z}_{t+1} \mid s_t)]$; one backward pass updates both heads.
2. **Q2 — Reward decomposition.** Task + latent-consistency ($\hat{z}_{t+1}$ vs encoder's $z_{t+1}$) + action-quality; the latent gives the dense signal task reward can't.
3. **Q3 — Knowledge insulation in joint loops.** Extend [[2505.23705|Knowledge Insulation VLA]]'s stop-gradient from action→VLM to action→WM encoder, preserving pretrained physics priors.
4. **Q4 — Failure-finder co-evolution.** A [[2412.02818|RoboMD]]-style adversary recast as GRPO; picks perturbations in the same optimizer step.
5. **Q5 — Real-robot transfer.** Deploy only the policy (LoRA on a frozen WM base), since WM + failure-finder stay sim-only.

**Related research papers.**
- [[2602.12063|VLAW]] — WM+policy alternating; WM trains on stale policy data.
- [[2603.19370|VAMPO]] — GRPO over video-denoising-as-MDP; pixel-space, expensive.
- [[2511.09515|WMPO]] — On-policy GRPO in imagination; WM frozen in inner loop.
- [[2511.15605|SRPO]] — Frozen [[2506.09985|V-JEPA 2]] + trajectory clustering; WM never updates.
- [[2605.15153|Pelican-Unified]] — Shared latent z; **93.5%** [[2504.13059|RoboTwin]]; multi-stage.
- [[2602.10098|VLA-JEPA]] / [[2602.11832|JEPA-VLA]] / [[2605.00078|Being-H0.7]] — Pure latent JEPA WMs; **97.2%** [[2306.03310|LIBERO]]; separate heads.
- [[2504.02792|UWM]] — Unified action-conditioned + video diffusion; high latency.
- [[2606.01027|τ₀-WM]] — Shared video-diffusion backbone for both a video-action model and a simulator; **+17%** unseen-task SR; pixel-space, not a single latent gradient.
- [[2606.01955|WALL-WM]] — Layer-coupled video-action denoiser; learns semantic action events, not fixed chunks (Task Progress **53.75**); joint but multi-stage, pixel-space.
- [[2602.10717|SDA]] — Distilled-Cosmos video WM imagines keyframes for an in-context action model; **98.1%** [[2306.03310|LIBERO]]; imagine-then-act (cascaded), not joint.
- [[2511.07732|ViPRA]] — Jointly predicts future visual states + latent actions from action-free video, then flow-matches control (22 Hz); A1's joint objective, but learned offline.
- [[2605.13775|RoboEvolve]] — Co-evolves a planner + a video simulator, beating a 25K-demo SFT baseline from 300 seed images; co-evolution but *alternating* — the schedule A1 replaces.
- [[2606.04130|CLAW]] — Joint latent-action + diffusion-WM training with reciprocal supervision; adversarial regularization blocks collapse — the anti-collapse substrate (with [[2511.08544|LeJEPA]]).
- [[2606.05979|WLA]] — Joint action + world-model + language objective (World/Action Experts); world prediction acts *implicitly*; **56.5%** RMBench, ~40 ms latent — joint-loss and latent-cheap, but one-pass.
- [[2505.23705|Knowledge Insulation VLA]] — Stop-gradient PEFT preserves pretrained priors during RL.
- [[2605.06732|Training in Imagination]] — MBRL imagination theory + budget allocation; not in a latent joint loop.

**Benchmarks & metrics.**
- [[2306.03310|LIBERO]] + [[2510.13626|LIBERO-Plus]] + [[2602.06556|LIBERO-X]] + [[2603.28301|LIBERO-Para]] — Joint test suite for in-dist + OOD + compositional.
- [[2510.13626|LIBERO-Plus]] — 10,030 OOD perturbations; the OOD axis the joint loop must improve over alternating.
- [[2605.21800|stable-worldmodel]] — Reproducible WM harness; [[2603.19312|LeWM]] **94%** / [[2411.04983|DINO-WM]] **92%** [[2109.00137|Push-T]] baselines with sharp planning decay under perturbation — substrate to check the joint loop's latent doesn't collapse under shift.

> [!warning] Risks
> - **Optimization instability** — discrete action + continuous latent + adversarial finder have conflicting gradients. → Balance with separate loss weights + EMA targets; run Q1 on a frozen WM first to isolate the action-head gradient.
> - **Chasing problem** — simultaneous updates → WM models an obsolete policy. → EMA target networks decouple the imagination target from the live policy.
> - **Reward hacking on latent consistency** — gameable by collapsing the latent. → [[2511.08544|LeJEPA]] Euclidean regularization defends; [[2604.27998|Latent-GRPO]]'s failure-mode patches apply.

### A2 — Causally-Important Step Rewards for Latent Policy Reasoning

| | |
|---|---|
| **Cluster** | A — Architecture & Training |
| **Thesis** | Put step rewards on *latent* reasoning tokens. Outcome rewards only care about the result, not the path — they can't tell a causally-correct reasoning path from a lucky one that lands the same outcome. The field assumes you must pick between latency-free latent CoT and step-level supervision. The bet: latent CoT + step rewards lifts LIBERO-Long SR by ≥+5 pp at matched latency and ≥+10 pp on compositional, closing the CoT-faithfulness gap [[2510.16281\|SEAL]] documented. |
| **Anchor surveys** | [[2509.19012\|Pure VLA Survey]], [[2510.04978\|Physical AI Survey]], [[2509.25373\|VLM Perception-Cognition Survey]] |
| **Key targets** | ≥+5 pp SR on LIBERO-Long at matched latency; ≥+10 pp on compositional (vs [[2510.16281\|SEAL]]'s **+15 pp** novel-behavior-composition gain to 53%) |

**Why it matters.** [[2604.22074|CIR/SR Reasoning]] finds outcome rewards insufficient — RL-trained traces become "factually correct via causally disconnected paths." [[2604.18486|OneVL]] shows latent reasoning beats explicit CoT at answer-only latency (**88.84** PDM-score, **+2.64 pts** over prior 8B). [[2510.16281|SEAL]] documents the CoT-faithfulness gap. [[2509.19012|Pure VLA Survey]] names causal reasoning alongside world modeling; [[2510.04978|Physical AI Survey]] extends it to all of Physical AI. No paper yet pairs latent CoT with step-reward training for policy reasoning.

**First-principles framing.**
- **First principle**: Outcome rewards bind the agent to the *result*, not the *reasoning path*. Two paths that reach the same outcome score the same, even if only one is causally correct. To shape reasoning, the reward must act on intermediate states, not just the terminal one.
- **Assumption being challenged**: That you need an explicit, written-out chain-of-thought to supervise reasoning. [[2604.22074|CIR/SR Reasoning]]'s step rewards work on *latent* (unwritten) reasoning tokens too, so [[2604.18486|OneVL]]'s latent CoT can take the same step-by-step supervision without the extra tokens — and the latency — that spelling the reasoning out would cost at inference.
- **The bet**: Latent CoT + step rewards gets ≥+5 pp SR on LIBERO-Long at matched latency and ≥+10 pp on compositional benchmarks, closing the gap [[2510.16281|SEAL]] documented.

**Evidence.**
- [[2604.18486|OneVL]] — Dual-decoder latent CoT; answer-only latency; the substrate step rewards bolt onto.
- [[2604.22074|CIR/SR Reasoning]] — Step-reward training for causal reasoning; outcome rewards insufficient.
- [[2604.28192|LaST-R1]] — Adaptive physical latent reasoning + RL.
- [[2604.27998|Latent-GRPO]] — RL stabilization (3 failure-mode patches).
- [[2604.22709|Abstract-CoT]] / [[2604.20328|HyLaR]] — Pre-allocated K tokens; vMF + decoupled clipping.
- [[2605.02735|Silenced Visual Latents]] — Diagnostic: latents can be "semantically rich but functionally ignored."

**Concrete research questions.**
1. **Q1 — Causal-importance predicates for manipulation.** Break 130 [[2306.03310|LIBERO]] tasks into 3–7 verifiable subgoals each (~600–900); auto-generate via [[2503.15558|Cosmos-Reason1]] LLM-as-judge, validate on a 100-subgoal gold set (κ > 0.7). Deliverable: LIBERO-Subgoals + predicate code.
2. **Q2 — Step-reward training on latent reasoning tokens.** Expose [[2604.18486|OneVL]]'s K=8 latent tokens; $\mathcal{L} = \lambda_a \mathcal{L}_{\text{action}} + \lambda_s \sum_i r_{\text{step},i}(z_i)$ with per-token subgoal predicates. Baselines: vanilla [[2604.18486|OneVL]], + outcome-only RL, [[2503.22020|CoT-VLA]]. Target: ≥+5 pp SR on LIBERO-Long at matched latency.
3. **Q3 — Latent utilization probing.** [[2605.02735|Silenced Visual Latents]]-style: Latent Utilization Index (LUI) = normalized action $L_2$ distance between $a(\mathbf{z})$ and $a(\mathbf{z}+\epsilon)$. Pass: LUI > 0.3.
4. **Q4 — Compositional step rewards.** Train on simple instructions, test compositions ("open drawer + place red mug") on [[2603.28301|LIBERO-Para]] + [[2510.13626|LIBERO-Plus]] + [[2507.10548|EmbRACE-3K]]. Target: ≥+10 pp on compositional, ≤−3 pp in-dist.
5. **Q5 — Inference cost ablation.** Explicit CoT (~1.2s) vs [[2604.22709|Abstract-CoT]] (~50ms) vs [[2604.18486|OneVL]] (~0ms) vs [[2604.18486|OneVL]]+CIR/SR (~0ms), across {ID, OOD, Compositional}.

**Related research papers.**
- [[2604.18486|OneVL]] — Dual-decoder latent CoT; **88.84** PDM-score; answer-only latency.
- [[2604.22074|CIR/SR Reasoning]] — Step-reward training; outcome rewards insufficient.
- [[2604.27998|Latent-GRPO]] — RL stabilization via 3 failure-mode patches.
- [[2510.16281|SEAL]] — Runtime CoT-faithfulness verifier; **+15 pp** compositional.
- [[2604.21396|VG-CoT]] — Visually-grounded chain-of-thought.
- [[2509.25852|REVER]] — Verifiable-reward RL planning.
- [[2605.02735|Silenced Visual Latents]] — Latents can be "semantically rich but functionally ignored."
- [[2503.15558|Cosmos-Reason1]] — Physical commonsense + embodied reasoning; LLM-as-judge for subgoals.
- [[2604.28192|LaST-R1]] — Adaptive physical latent reasoning + RL; the substrate step rewards bolt onto.
- [[2606.02277|RoboSemanticBench]] — Diagnostic of the reasoning-following gap: **89.93%** of grasp-success/task-failure cases reasoned right yet acted wrong; A2's "causally-disconnected path" in benchmark form.
- [[2606.03784|ERVLA]] — 226M-sample embodied CoT corpus + CoT-dropout (reason at train, act direct at test); explicit autoregressive CoT *doesn't* scale — empirical backing for A2's latent direction.
- [[2509.22643|VLA-Reasoner]] — Test-time MCTS over a learned WM with a vision value network scoring intermediate states; **+19 pp** real SR; A2's dense-intermediate-feedback move via search.
- [[2506.21669|SEEA-R1]] — MCTS turns sparse outcome signals into dense step-wise Q-values for a self-evolving agent; A2's "sparse → dense reward" mechanism at the agent level.
- [[2509.25681|dVLA]] — Discrete-diffusion VLA with multimodal CoT (visual subgoals + text + action co-masked); **+6.6 pp** from CoT at ~2× speed; reasoning in one diffusion objective.
- [[2605.13632|GTA-VLA]] — Async "slow reasoning, fast action" with Guide-Think-Act spatial CoT; **98.6%** [[2306.03310|LIBERO]]; the reasoning/latency decoupling A2 targets.
- [[2601.01618|Action-Sketcher]] — Visual-sketch intermediate (See-Think-Sketch-Act) with token-gating between reasoning and fast action; **96.0%** LIBERO-Long; visual-intermediate variant.
- [[2604.17800|ReFineVLA]] — Teacher-distilled language rationales via selective fine-tuning; **+9.6%** SimplerEnv; the explicit-CoT-distillation baseline A2's latent approach must beat.
- [[2606.04436|3DThinkVLA]] — Distills 3D spatial *thinking* into the action prompt via a latent reasoning-anchor token (no CoT text); **98.7%** LIBERO; the anchor mechanism A2 is built on.

**Benchmarks & metrics.**
- [[2406.15349|NAVSIM]] — Driving CoT benchmark; cross-domain reasoning-faithfulness anchor.
- [[2606.02277|RoboSemanticBench]] — Semantic-grounding diagnostic (Task vs Grasp SR, nSG) isolating the reasoning-into-action gap; the faithfulness benchmark for the step-reward gain.
- [[2510.13626|LIBERO-Plus]] — 10,030 OOD perturbations; OOD axis for the step-reward gain.
- [[2603.28301|LIBERO-Para]] — Paraphrase compositional; compositional-novelty axis.
- [[2507.10548|EmbRACE-3K]] — Embodied reasoning + action correlation; faithfulness-to-action axis.

> [!warning] Risks
> - **Predicate scaling** — hand-authoring subgoals is brittle; LLM-as-judge fallback re-introduces the verification cost CIR/SR avoids. → Validate the auto-generated predicates against a κ > 0.7 gold set (Q1) before scaling.
> - **Reward hacking** — models can satisfy predicates trivially. → [[2509.15194|EVOL-RL]] novelty diversity + the LUI probe (Q3) catch trivial satisfaction.
> - **Compositional generalization may be unsolved at this scale** — [[2510.16281|SEAL]] documented this exact failure mode. → Bound the compositional claim to [[2603.28301|LIBERO-Para]]-style paraphrase novelty rather than unbounded composition.

### A3 — Verifiable Physics-Consistent Training for Open-World Policy Generation

| | |
|---|---|
| **Cluster** | A — Architecture & Training |
| **Thesis** | Enforce verifiable physics predicates at the *action* level. Physical laws hold the same for held-out and OOD data, so a loss enforcing them extrapolates without distribution shift. The field assumes physics-aware video generation transfers for free into physics-aware policy. The bet: action-level predicates lift obstacle-perturbation Safe-SR from **43.50% → >55%** (extending [[2604.17896\|Physical-Feasibility VLA]]'s geometric-only ceiling) and reach ≥0.70 sim-to-real SR retention, with a non-trivial Pearson ρ between predicate satisfaction and downstream SR. |
| **Anchor surveys** | [[2604.04974\|Video-to-Control Survey]], [[2503.21765\|Physics Cognition Survey]], [[2510.04978\|Physical AI Survey]] |
| **Key targets** | obstacle-perturbation Safe-SR **43.50% → >55%** ([[2604.17896\|Physical-Feasibility VLA]] baseline; the action-level physics ceiling A3 extends); sim-to-real SR retention **≥0.70**; DPO pass-target **≥90%** on held-out via [[2603.23376\|ABot-PhysWorld]] physics-rejected negatives; [[2605.08567\|ACWM-Phys]] OOD ΔM-MSE reduced vs naive |

**Why it matters.** Five surveys converge on the same gap: [[2604.04974|Video-to-Control Survey]] (physical feasibility as missing layer), [[2503.21765|Physics Cognition Survey]] (sub-human physics), [[2510.04978|Physical AI Survey]] ("causal understanding missing"), [[2601.15533|Actionable Simulators]] (*dynamical hallucinations*), [[2601.07823|Video Generation in Robotics Survey]] (hallucinations + physics violations as top-2). [[2605.08567|ACWM-Phys]] now *quantifies* the cliff: action-conditioned video WMs are crisp in-distribution (SSIM **0.988**) but degrade sharply OOD (ΔM-MSE up to **+40** on robot-arm, **+30** on cloth). Physics-aware video generators ([[2509.21309|NewtonGen]], [[2510.13809|PhysMaster]], [[2512.00425|NewtonRewards]], [[2603.13770|PhysAlign]]) progress on the *generation* side, but the imagination → policy chain is untested. Closest: [[2604.17896|Physical-Feasibility VLA]] — a differentiable geometric loss on actions lifts obstacle-perturbation Safe-SR — Pr(d_min > α ∧ d_tgt < β) — from 22% → **43.50%**; geometric only, no verifiable physics predicates and no [[2510.13626|LIBERO-Plus]] eval.

**First-principles framing.**
- **First principle**: Physical laws (momentum, gravity, friction, contact) are universal and checkable, and they don't depend on the training set — they hold for held-out and OOD data alike. A loss that enforces them keeps working off-distribution, unlike ordinary losses that only trust the samples they saw.
- **Assumption being challenged**: That a video generator which respects physics hands you a *policy* that respects physics for free. That hand-off — from physics in the generated video to physics in the chosen action — is assumed but never measured end-to-end; [[2605.08567|ACWM-Phys]] shows even the first step already leaks OOD, so the rest can't be assumed intact.
- **The bet**: Physics predicates at the *action* level lift obstacle-perturbation Safe-SR from **43.50% → >55%** ([[2604.17896|Physical-Feasibility VLA]]'s geometric-only Safe-SR is the baseline) and reach ≥0.70 sim-to-real SR retention (physics-naive: 0.50–0.60), making physics-consistent action a measurable axis, not a generation-side correlate.

**Evidence.**
- **Video-side**: [[2509.20570|PIRF]], [[2509.21309|NewtonGen]], [[2512.00425|NewtonRewards]], [[2510.13809|PhysMaster]], [[2603.13770|PhysAlign]], [[2603.26285|PhysVid]].
- **VLA-side**: [[2604.17896|Physical-Feasibility VLA]], [[2503.15558|Cosmos-Reason1]], [[2511.07416|PhysWorld]], [[2605.06593|ReActor]].
- **Bridge**: [[2603.23376|ABot-PhysWorld]] (Diffusion-DPO with physics-rejected negatives).
- **Measurement substrate**: [[2605.08567|ACWM-Phys]] quantifies the InD→OOD physics cliff on action-conditioned WM rollouts — the first benchmark that scores physics on *action-conditioned* generation, exactly the chain A3 must fix.

**Concrete research questions.**
1. **Q1 — Physics predicates over action sequences.** Five binary verifiable predicates:
   - **P1 momentum**: $|\Delta p_{\text{total}}| < 0.05 \cdot p_{\max}$ over 1s (excluding contact)
   - **P2 no inter-object penetration**: signed-distance > 0 at every step
   - **P3 anti-gravity check**: free-flight $\Delta z \sim -\frac{1}{2}gt^2 \pm 10\%$
   - **P4 Newton's 3rd law on contact wrenches**
   - **P5 Coulomb friction**: $|F_t| \leq \mu |F_n|$
   Instrument 50 [[2306.03310|LIBERO]] + 30 [[2502.16707|ReflectVLM]] multi-stage long-horizon tasks; ~4,000 labeled trajectories.
2. **Q2 — Implicit vs abstract vs explicit interface ablation** (per [[2604.04974|Video-to-Control Survey]] taxonomy). Same backbone, matched FLOPs; report Safe-SR on a [[2604.17896|Physical-Feasibility VLA]]-style obstacle gauntlet + a new 20-task physics gauntlet + [[2605.08567|ACWM-Phys]] OOD splits, and track plain SR on [[2510.13626|LIBERO-Plus]] separately. Target: lift the Safe-SR ceiling from 43.50% → >55%; latent within ±2 pp at lower latency.
3. **Q3 — Open-world test via [[2603.23376|ABot-PhysWorld]] negatives.** ~10k preference pairs, Diffusion-DPO. Pass: $\beta(\log p_\theta(a_+) - \log p_\theta(a_-)) > 0$ on ≥90% of 1k held-out (baseline ~74%).
4. **Q4 — Sim-to-real chain.** [[2511.04665|Real-to-Sim GS]] soft-body twins (12 cloth/rope/dough); eval sim → twin → real. Target SR retention $\geq 0.70$ (physics-naive: 0.50–0.60).
5. **Q5 — Reward-hacking diagnostics.** Static-output detection (σ drop > 2×); $\rho(\sum P_i, \text{task SR})$ regression; periodic [[2412.02818|RoboMD]] adversarial probing. Defense: [[2509.15194|EVOL-RL]] novelty diversity.

**Related research papers.**
- [[2605.08567|ACWM-Phys]] — Physical-generalization benchmark + ACWM-DiT baseline; quantifies the InD→OOD physics cliff; eval substrate, not a training fix.
- [[2604.17896|Physical-Feasibility VLA]] — Geometric loss on actions; **22 → 43.50%** SSR; geometric only.
- [[2603.23376|ABot-PhysWorld]] — Diffusion-DPO with physics-rejected negatives; the bridge to action.
- [[2509.21309|NewtonGen]] / [[2512.00425|NewtonRewards]] / [[2510.13809|PhysMaster]] / [[2603.13770|PhysAlign]] — Physics-aware video generation; generation side, no action chain.
- [[2509.20570|PIRF]] — PDE residual rewards; generation; no WAM-state path.
- [[2511.07416|PhysWorld]] — Policy vs learned physical WM; **82%** real SR; positions/velocities only.
- [[2605.06593|ReActor]] — Bilevel RL + physics sim; **+15.22 pp**; motion retargeting only.
- [[2511.04665|Real-to-Sim GS]] — 3DGS + soft-body PhysTwin; **r=0.915** (push-T) / **0.901** (rope) sim-real.
- [[2605.15298|PhysBrain]] — Physics-aware policy from egocentric; closest physics-grounded policy, no verifiable predicate set.

**Benchmarks & metrics.**
- [[2605.08567|ACWM-Phys]] — Action-conditioned video-WM physics generalization; InD SSIM **0.988**, OOD ΔM-MSE up to **+40**; first benchmark scoring physics on action-conditioned WM rollouts.
- [[2410.05363|PhyGenBench]] — Physical commonsense (video); best T2V **0.51/3.0** PCA.
- [[2503.06800|VideoPhy-2]] — Action-centric physical reasoning; best **32.6%** joint.
- [[2501.09038|Physics-IQ]] — Whether models *understand* physics; visual-quality vs physics-correctness gap.
- [[2504.02918|Morpheus]] — Real-physical-experiment benchmark.
- Obstacle-perturbation Safe-SR gauntlet ([[2604.17896|Physical-Feasibility VLA]] protocol) + 20-task physics gauntlet — action-level physics Safe-SR; target: 43.50% → >55%. [[2510.13626|LIBERO-Plus]] tracked separately as a plain-SR robustness axis (the 43.50% is *not* a [[2510.13626|LIBERO-Plus]] number).

> [!warning] Risks
> - **Verifiable physics scales poorly** ([[2509.20570|PIRF]]) — predicates for cluttered scenes are hard. → Start with [[2605.08567|ACWM-Phys]]'s low-dimensional clean-structure tasks where predicates are tractable, then expand.
> - **Physics-consistent imagination ≠ physics-consistent action** — this is the gap to test; if small, the direction collapses. → Q5's Pearson ρ between $\sum P_i$ and SR is the go/no-go before scaling.
> - **Reward hacking** — [[2512.00425|NewtonRewards]] documented it on the generation side; the action-side analog (model freezes) is likely. → C1 static-output detection + [[2509.15194|EVOL-RL]] novelty diversity defend.

---

## Cluster B — Evaluation, Robustness & Deployment

*Measurement instruments, recovery loops, and efficiency co-design that turn lab gains into real-world capability.*

### B1 — Joint Policy/World-Model Evaluation: Causal Consistency Between Imagination and Action

| | |
|---|---|
| **Cluster** | B — Evaluation, Robustness & Deployment |
| **Thesis** | Measure WM and policy on one joint causal-consistency axis, not two separate ones (WM quality via FVD/PSNR, action quality via [[2306.03310\|LIBERO]] SR). A WM and policy are causally bound only when actions in imagined futures match executed ones. The field assumes visual fidelity of WM-generated futures predicts policy success. The bet: ASR + COD *jointly* predict real-fleet SR at Pearson **ρ > 0.7** (vs ρ < 0.4 for separate axes), replacing FID-style WM eval. |
| **Anchor surveys** | [[2605.12090\|WAM Survey]], [[2604.22748\|Agentic World Modeling Survey]], [[2310.06253\|Objective Mismatch MBRL Survey]] |
| **Key targets** | ASR + COD AUROC **≥ 0.7**; joint metric → real SR Pearson **ρ > 0.7** (current separate axes: ρ < 0.4) |

**Why it matters.** [[2605.12090|WAM Survey]], [[2605.00080|WM Robot Learning Survey]], [[2510.16732|World Models for Embodied AI Survey]], [[2601.15533|Actionable Simulators]], and [[2601.07823|Video Generation in Robotics Survey]] all flag that current protocols measure WM quality (FVD/PSNR) and action quality ([[2306.03310|LIBERO]] SR) **separately** — a joint model can score high on each while imagination and actions are causally disconnected. [[2310.06253|Objective Mismatch MBRL Survey]] gives the MBRL substrate: predictive WM loss doesn't correlate with downstream return. [[2603.22078|WAM vs VLA Robustness]] showed world-action models win on visual perturbations *but run 4.8× slower* — a cost worth paying only if imagination helps action quality, which current metrics can't certify. [[2605.06311|VISER]] shows the sim-real correlation *can* hit Pearson **r = 0.92** when visual fidelity is controlled — proof the joint-axis signal is there once you measure it right.

**First-principles framing.**
- **First principle**: A world model and a policy are truly linked only when the actions taken in *imagined* futures match the actions taken in *executed* ones. If you never measure that link directly, the "world-model quality" score and the "policy SR" score can both climb while the combined skill goes nowhere — each metric gets gamed on its own.
- **Assumption being challenged**: That how real the generated futures *look* (FID, FVD) tells you whether the policy will succeed. [[2604.21686|WorldMark]] shows it's *wrong* — looking good and being physically consistent are unrelated — and [[2605.21800|stable-worldmodel]] shows planning SR collapses under perturbation even when in-distribution visual SR is 92–94%; yet FID-style metrics persist. A sharper version: maybe the success signal needn't come from a *separate* world model at all. [[2605.28527|VLA Value Probing]] reads a value-like signal straight from a *frozen* policy's features (R² ≈ 0.55, 94.22% pairwise-order, value-guided selection +17.67 pp) — so the policy may already carry what the joint metric certifies.
- **The bet**: ASR + COD *jointly* predict real-fleet SR at Pearson **ρ > 0.7**, far above the ρ < 0.4 ceiling of separate-axes evaluation (ρ < 0.4 is the contrast baseline the experiment must establish, not a paper-reported number) — making the pair the practical replacement for current WM eval.

**Evidence.**
- [[2603.22212|Omni-WorldBench]] — First interaction-centric WM eval via counterfactual probes (WM-only).
- [[2506.00613|WorldGym]] — Policies trained inside WM (closer to joint, game-style).
- [[2510.10125|CTRL-WORLD]] — Controllability eval for manipulation.
- [[2603.23497|WildWorld]] — Action Following + State Alignment on 108M Monster Hunter frames.
- [[2606.05773|PiL-World]] — Closed-loop WM feeding imagined futures back to the policy; imagined-vs-real SR gap **63.2% → 12.0%**, Pearson **0.94**; the correlation is measurable closed-loop.
- [[2606.04463|OSCAR]] — Skeleton-conditioned video WM; virtual policy rankings track real-fleet at Pearson **r = +0.852** (MAE **1.73 pp**); the joint-eval correlation B1 must reach.
- [[2605.21800|stable-worldmodel]] — Reproducible OOD harness; [[2603.19312|LeWM]] 94% / [[2411.04983|DINO-WM]] 92% [[2109.00137|Push-T]], planning decays under occlusion; the perturbation substrate.
- [[2605.06311|VISER]] — Sim-real Pearson **r = 0.92** with 1,000+ PBR objects; existence proof the joint-axis correlation is recoverable.
- [[2606.05015|Quadrotor World Model Study]] — Self-supervised reconstruction quality predicts real deployability *better than* sim SR (OOD win-rate >**72.0%**); the SR proxy is the wrong predictor.

**Concrete research questions.**
1. **Q1 — Causal-consistency metric.** Given $(s_t, a_t) \to \hat{s}_{t+1}, s_{t+1}$, [[2304.07193|DINOv2]] (ViT-L/14) cosine plus a counterfactual probe: sample $a'_t$, generate $\hat{s}'_{t+1}$, require $\|\hat{s}_{t+1} - \hat{s}'_{t+1}\|$ to scale monotonically with $\|a_t - a'_t\|$. Reference on [[2603.13966|vla-eval]].
2. **Q2 — 50–100 task diagnostic suite.** Layer on [[2306.03310|LIBERO]] (130 tasks) + [[2510.13626|LIBERO-Plus]] (10,030 perturbations) + [[2603.28301|LIBERO-Para]]; record (predicted, achieved, action) at every step. ~40k pairs per WAM.
3. **Q3 — L1/L2/L3 sub-scores** (per [[2604.22748|Agentic World Modeling Survey]]): L1 Predictor = 1-step MSE (>90% [[2510.10125|CTRL-WORLD]] controllability); L2 Simulator = 8-step drift (<2× linear); L3 Evolver = COD as AUROC of swapped-action detection (0.5 chance, 1.0 perfect). Pair with ASR.
4. **Q4 — Speed-quality Pareto.** Re-run [[2603.22078|WAM vs VLA Robustness]]'s ~12-config grid with the joint metric. Does the 4.8× cost buy ≥X pp on L3?
5. **Q5 — Deployment-readiness axis.** Cross-check [[2506.18123|RoboArena]] (8 platforms, ~120 tasks) + [[2605.20774|VLA-REPLICA]] (reproducible real eval). Does the joint metric predict real SR at Spearman ρ > 0.7? Separate sub-scores: ρ < 0.4.

**Related research papers.**
- [[2603.22212|Omni-WorldBench]] — First interaction-centric WM eval w/ counterfactual probes; WM-only.
- [[2506.00613|WorldGym]] — Policies trained inside WM; game-style.
- [[2510.10125|CTRL-WORLD]] — Controllability eval for manipulation.
- [[2603.22078|WAM vs VLA Robustness]] — Grid; **4.8×** latency cost; separate axes.
- [[2603.13966|vla-eval]] — Unified eval harness; **47×** [[2306.03310|LIBERO]] speedup; no joint causal metric.
- [[2605.21800|stable-worldmodel]] — Reproducible OOD WM platform; [[2603.19312|LeWM]] 94% / [[2411.04983|DINO-WM]] 92% [[2109.00137|Push-T]]; planning decay under perturbation.
- [[2605.06311|VISER]] — Visually-realistic sim; sim-real **r = 0.92**; 1,000+ PBR objects; visual fidelity, not yet causal consistency.
- [[2605.25874|WBench]] — Multi-turn interactive video-WM benchmark; 289 cases, 22 sub-metrics; navigation drops 33 pts Turn-1→Turn-4+; the substrate B1 adds an action-causality axis to.
- [[2606.05773|PiL-World]] — Chunk-wise closed-loop WM; Pearson r **0.94**, gap 63.2→12.0%; closed-loop correlation but evaluates, doesn't certify causal binding.
- [[2606.04463|OSCAR]] — Skeleton-conditioned video WAM; r **+0.852** with real rankings; correlation via conditioning, not an action-causality metric.
- [[2605.26379|LeJEPA World Model]] — Proves a JEPA recovers true latents *iff* they are isotropic-Gaussian, enabling oracle-level planning (R² > 0.999); the theory of *when* B1's latent encodes the real world.
- [[2606.05159|X4Val]] — Variance-reduced policy eval via transferable surrogates; **38.4%** variance cut from non-paired data; the statistical-validity layer a joint metric needs.
- [[2605.20774|VLA-REPLICA]] — Reproducible real-world eval; reproducibility validated (ID 0.49 vs 0.48); real-fleet anchor.
- [[2606.04233|Manipulation Benchmark Audit]] — A 0.09B [[2304.07193|DINOv2]]+MLP probe hits **99.0%** on LIBERO-Spatial (shortcut-solvable); only **19.8%** of LIBERO / **19.7%** of SimplerEnv SOTA claims are significant; current SR certifies the wrong thing.
- [[2605.29710|PhAIL]] — Real-robot benchmark with a time-to-success CDF + KS test (**80%** detection at N=25-30 vs binary failure at N=30); the statistical-rigor layer (with [[2606.05159|X4Val]]).
- [[2601.04137|WoW-World-Eval]] / [[2602.08971|WorldArena]] — Comprehensive embodied-WM eval (Turing test; perception + functional utility).

**Benchmarks & metrics.**
- [[2306.03310|LIBERO]] + [[2510.13626|LIBERO-Plus]] — Action SR baseline; ~40k pairs.
- [[2603.22212|Omni-WorldBench]] + [[2603.23497|WildWorld]] — WM-only baselines to extend with the action axis.
- [[2605.06311|VISER]] — Sim-real Pearson **r = 0.92**; the correlation the joint metric must match or beat on action quality.
- [[2506.18123|RoboArena]] + [[2605.20774|VLA-REPLICA]] — Real-world anchor; reproducibility validated for cross-lab comparison.

> [!warning] Risks
> - **Metric noise** — feature-space similarity embeds blind spots. → Pair with explicit physical predicates from A3; cross-validate against [[2605.06311|VISER]]'s measured sim-real correlation.
> - **Sample size** — counterfactual probes may need 100+ rollouts per task instance. → Use [[2603.13966|vla-eval]]'s 47× speedup to amortize the rollout cost.
> - **Selection bias** — the benchmark may flatter current WAMs. → Include adversarial ([[2604.05498|JailWAM]], [[2606.03556|VLA Patch Attack]] — a partially-observable physical patch reaching **90.7%** attack SR, [[2605.02900|Safety in Embodied AI Survey]] attack layers) + physics-violating ([[2603.23376|ABot-PhysWorld]] rejects) baselines.

### B2 — Long-Horizon Memory + Failure Recovery Loops for Real-World Deployment

| | |
|---|---|
| **Cluster** | B — Evaluation, Robustness & Deployment |
| **Thesis** | Build one integrated detect-diagnose-recover loop with memory, not four separate modules. An agent that can't remember can't notice repeated failure; one that notices it must change behavior or it isn't learning. The field assumes these four parts compose trivially. The bet: a unified loop lifts long-horizon SR on [[2306.03310\|LIBERO]]-Long memory-dependent tasks by ≥+15 pp over [[2605.10993\|ECHO-VLA]]'s memory-only +12.8 pp (end-to-end on [[2605.10921\|RoboMemArena]], 68.9% memory-dependent subtasks), and cuts oscillation incidents ≥50% via state-machine integration. |
| **Anchor surveys** | [[2604.16592\|Cognition WM Survey]], [[2602.04411\|Self-evolving Embodied AI]], [[2505.05108\|Multi-agent Embodied AI Survey]] |
| **Key targets** | ≥+15 pp SR on [[2306.03310\|LIBERO]]-Long memory-dependent tasks (baseline: [[2605.10993\|ECHO-VLA]] **+12.8 pp** on LIBERO-Long); end-to-end eval on the [[2605.10921\|RoboMemArena]] suite (**68.9%** memory-dependent subtasks); oscillation incidents **−50%**; [[2510.02298\|ARMADA]] **23.3%** intervention reduction |

**Why it matters.** [[2605.10921|RoboMemArena]]: **68.9%** of subtasks need historical info. [[2604.16592|Cognition WM Survey]] names *meta-cognition* as one of two drastically under-researched cognitive functions — failure detection + recovery is its embodied form. [[2602.04411|Self-evolving Embodied AI]] (5-module framework) and [[2505.05108|Multi-agent Embodied AI Survey]] (open-environment self-evolution) decompose it further. Recovery needs memory — [[2605.10993|ECHO-VLA]] (**+12.8 pp** LIBERO-Long) is closest but has no detection integration. [[2605.02900|Safety in Embodied AI Survey]] adds a warning: memory itself is an attack surface (poisoning), so the loop must be defended, not just built.

**First-principles framing.**
- **First principle**: An agent that can't remember has no basis for recognizing repeated failure; one that recognizes it must change behavior or it isn't learning. Memory + detection + recovery are three faces of one capability, not three independent modules.
- **Assumption being challenged**: That memory, failure detection, correction, and recovery are independent problems. The field has 5+ memory papers, 8+ detection papers, 6+ correction papers — but no system integrates them. That they compose trivially has never been tested; oscillation, dropout, and latency stacking suggest they don't.
- **The bet**: An integrated detect-diagnose-recover loop with memory lifts long-horizon SR on [[2306.03310|LIBERO]]-Long memory-dependent tasks by ≥+15 pp over [[2605.10993|ECHO-VLA]]'s +12.8 pp on memory alone (both on LIBERO-Long), end-to-end on [[2605.10921|RoboMemArena]] where **68.9%** of subtasks need history, and cuts oscillation incidents ≥50% via state-machine integration.

**Evidence.**
- **Memory**: [[2605.10993|ECHO-VLA]] (+12.8 pp), [[2508.19236|MemoryVLA]] (+26 pp temporal, +3.6% latency), [[2603.03596|MEM]] (15-min memory), [[2603.12942|ReMem-VLA]] (**94.5%** on memory-dependent sim), [[2606.03374|eMEM]] (tiered spatio-temporal memory, **80.8%** eMEM-Bench, 100% recall to 1-year simulated delay).
- **Detection** (per [[13_Self-Evolving-VLA-WAM#4.1 Runtime Failure Detection|13_Self-Evolving-VLA-WAM §4.1]]): [[2506.09937|SAFE]], [[2509.16072|I-FailSense]], [[2510.09459|FIPER]], [[2603.11106|RC-NF]] (<100 ms), [[2503.08558|FAIL-Detect]] (**78%** w/o failure data), [[2410.04640|Sentinel]] (**+18%** over single), [[2407.08735|AESOP]] (**100%** sim recovery), [[2510.02298|ARMADA]] (**95%** accuracy, **23.3%** intervention reduction), [[2605.30834|Hide-and-Seek]] (trajectory-only supervision, bACC **0.852**, **2,000×** faster than a VLM judge).
- **Diagnosis / failure attribution**: [[2606.03385|GTP-FA]] — attributes a failure to grasp vs planning before updating (real Franka **11.2% → 76.8%**); the "diagnose" face B2's loop needs between detection and recovery.
- **Proactive correction**: [[2601.02295|CycleVLA]], [[2512.24426|CF-VLA]], [[2604.02965|SV-VLA]], [[2511.14148|AsyncVLA]], [[2509.04018|FPC-VLA]].
- **Recovery**: [[2505.12224|RoboFAC]], [[2603.13528|Counterfactual Failure Synthesis]].
- **Failure discovery (test-time)**: [[2606.02307|FATE-VLA]] — adaptive, learning-guided test generation surfaces **+29.7 pp** more failures than random sampling; the adversary that stress-tests whether the detect-recover loop actually fires.

**Concrete research questions.**
1. **Q1 — Memory-grounded failure detection.** Use [[2605.10993|ECHO-VLA]] / [[2508.19236|MemoryVLA]] hierarchical memory to catch history-dependent failures ("tried this 3× already").
2. **Q2 — Recovery with memory.** When [[2601.02295|CycleVLA]] backtracks, consult memory — the memory bank as a *failure-exclusion buffer*.
3. **Q3 — Real-world loop stack**: (a) memory (PCMB / hyperbolic), (b) parallel detectors ([[2410.04640|Sentinel]] pattern), (c) corrective head ([[2601.02295|CycleVLA]] + [[2512.24426|CF-VLA]]), (d) recovery generator ([[2603.13528|Counterfactual Failure Synthesis]]).
4. **Q4 — Compute-vs-robustness trade-off.** Ablate on [[2605.10921|RoboMemArena]] + [[2510.13626|LIBERO-Plus]] + real-robot [[2506.18123|RoboArena]]; find the deployable combinations.
5. **Q5 — Continual update from corrections.** Each successful recovery → a training example ([[2510.02298|ARMADA]] pooled-intervention pattern), with memory-poisoning defense per [[2605.02900|Safety in Embodied AI Survey]].

**Related research papers.**
- [[2605.10921|RoboMemArena]] — Memory benchmark; **68.9%** subtasks need history.
- [[2605.10993|ECHO-VLA]] — Hierarchical memory; **+12.8 pp** LIBERO-Long.
- [[2508.19236|MemoryVLA]] — **+26 pp** temporal, **+3.6%** latency.
- [[2603.03596|MEM]] / [[2603.12942|ReMem-VLA]] — 15-min memory bank; **94.5%** on memory-dependent sim.
- [[2510.09459|FIPER]] / [[2506.09937|SAFE]] / [[2410.04640|Sentinel]] / [[2603.11106|RC-NF]] — Detection (predictive, internal-feature, ensemble, real-time conformal).
- [[2503.08558|FAIL-Detect]] — Failure detection without failure data; **78%**.
- [[2605.30834|Hide-and-Seek]] — Trajectory-only failure localization from internal action embeddings; bACC **0.852**, **2,000×** faster than a VLM monitor; the cheap detection front-end.
- [[2510.02298|ARMADA]] — FLOAT detector; **95%** accuracy; **23.3%** intervention reduction.
- [[2606.03385|GTP-FA]] — Closed execute-diagnose-update loop with grasp-vs-planning failure attribution; real Franka **11.2% → 76.8%**; the diagnosis step detection-only work skips.
- [[2606.02307|FATE-VLA]] — Adaptive learning-guided test generation; **+29.7 pp** failure discovery over random sampling; the harness that validates the loop, not static benchmarks.
- [[2601.02295|CycleVLA]] / [[2512.24426|CF-VLA]] / [[2509.04018|FPC-VLA]] — Proactive correction.
- [[2602.21633|SC-VLA]] — Self-correcting policy: sparse imagination predicts short-horizon evolution, a residual-RL head refines actions online; **86%** ManiSkill3, **71%** real; imagination-driven correction.
- [[2602.20057|AdaWorldPolicy]] — WM prediction error as a self-supervised signal for test-time LoRA updates at **4 Hz**; recovers SR under OOD shift; the online-adaptation recover step, label-free.
- [[2505.12224|RoboFAC]] / [[2603.13528|Counterfactual Failure Synthesis]] / [[2605.14539|CIPO]] — Recovery from failure traces (last is RL with verifiable rewards).
- [[2606.03374|eMEM]] — Tiered (Working/Short/Long/Archived) spatio-temporal memory; **80.8%** eMEM-Bench, no forgetting to 1-year delay; the long-horizon memory substrate.
- [[2511.16166|EvoVLA]] — Self-evolving policy: stage-aligned intrinsic reward (stage-hallucination **38.5% → 14.8%**) + gated long-horizon memory; **69.2%** sim; the memory-plus-self-evolution variant.
- [[2506.21669|SEEA-R1]] — Self-evolving agent; MCTS-derived dense rewards train a generative reward model for replay-free improvement (**+34.72 pp** real); the "recovery → training example" engine.
- [[2606.05395|VASO]] — Formally-verifiable self-evolving skills: LTL counterexamples become textual gradients refining the skill contract (**89% → 97%** feasibility, ~**95%** safety); verification-gated correction.
- [[2605.15735|UAM]] — Policy forgetting under fine-tune; the catastrophic-forgetting risk the continual loop must avoid (now B4).

**Benchmarks & metrics.**
- [[2605.10921|RoboMemArena]] — Memory-dependent SR; **68.9%** subtasks need history.
- [[2510.13626|LIBERO-Plus]] / [[2510.03827|LIBERO-PRO]] — OOD perturbations.
- [[2506.18123|RoboArena]] — Real-fleet across 8 platforms.
- [[2502.09560|EmbodiedBench]] — General embodied AI eval.

> [!warning] Risks
> - **Latency stacking** — each component adds 10–100 ms; the full loop may not be real-time. → Parallelize detectors ([[2410.04640|Sentinel]] pattern) and invoke recovery only on firing; co-design with B3's efficiency budget.
> - **Component oscillation** — detectors may fire on each other's corrections. → State-machine integration with explicit mode transitions is the mitigation the bet measures (≥50% oscillation reduction).
> - **Memory as attack surface** — [[2605.02900|Safety in Embodied AI Survey]] flags memory poisoning. → Gate memory writes behind a recovery-success check; treat the failure-exclusion buffer as untrusted input.

### B3 — Real-Time-Deployable Policies via Architectural-Algorithmic-Data Co-design

| | |
|---|---|
| **Cluster** | B — Evaluation, Robustness & Deployment |
| **Thesis** | Treat efficiency as a primary research target, not "engineering to sort out after publication." Inference cost has three independent levers — what / how often / how precisely you predict — and their Pareto frontier needs co-design. The field assumes single-lever tuning or faster silicon will suffice. The bet: a co-designed (architecture + training + data + quantization) policy hits ≥30 Hz on edge ([Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) / Apple M, vs the AR 3–5 Hz ceiling) while keeping ≥95% of base-policy SR — showing the latency-quality curve moves with method, not just hardware. |
| **Anchor surveys** | [[2510.24795\|Efficient VLA Survey]], [[2510.07077\|VLA Robotics Real-World Review]], [[2603.28489\|Video Gen as WM Survey]] |
| **Key targets** | ≥30 Hz on [Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) / Apple M (vs AR 3–5 Hz ceiling); ≥95% of base-policy [[2306.03310\|LIBERO]] SR retained; matched-FLOPs Pareto sweep |

**Why it matters.** [[2510.24795|Efficient VLA Survey]] and [[2603.28489|Video Gen as WM Survey]] reframe efficiency from "optimization" to "prerequisite." [[2505.04769|VLA Concepts Survey]] quantifies it: AR decoding caps speed at 3–5 Hz vs the 20–50 Hz needed. [[2510.07077|VLA Robotics Real-World Review]] names latency a top-3 deployment concern; [[2511.05936|10 VLA Challenges]] names resource efficiency one of ten core bottlenecks. No other direction here treats efficiency as a primary thesis — they all assume real-time is feasible.

**First-principles framing.**
- **First principle**: A contact-rich policy runs as a feedback loop on discrete time steps, so it has a *stability* floor, not just a speed preference. Stiff contacts shake the robot at high frequencies. The Nyquist sampling rule says a loop has to run at least ~2× faster than the fastest motion it's trying to control; run it slower and it *cannot* be stabilized, no matter how well tuned. That floor doesn't care about the data or the hardware: a manipulator whose contacts ring at tens of Hz simply *cannot* be held steady by a 3–5 Hz loop.
- **Assumption being challenged**: That efficiency is "engineering, not research," something faster chips will fix on their own. In contact-rich manipulation, the gap between 3–5 Hz and 30 Hz isn't a tuning knob — it's the line between sitting below the stability floor and above it, between a policy that flies apart and one that settles. Efficiency is a first-class control constraint, not an afterthought.
- **The bet**: Co-designed (architecture + training + data + quantization) policies hit ≥30 Hz on edge ([Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) / Apple M) while keeping ≥95% of base-policy SR — showing the latency-quality curve can be moved by method, not just hardware. (The 95% bar is a design-chosen target, not a paper-reported figure.)

**Evidence.**
- **Model-side**: [[2312.01990|SARA-RT]], [[2406.04339|RoboMamba]] (linear-time / Mamba), [[2605.14598|DSSP]] (diffusion state-space policy), [[2606.05737|One-Step VLA]] (one-step decoding matches 10-step; **95.6%** LIBERO-Long, no distillation), [[2605.29438|ElegantVLA]] (RL "when to think" scheduler, **3.77×** FLOPs, 16.64→35.03 Hz), parallel decoding, quantization + pruning + distillation (rarely co-optimized).
- **Training-side**: [[2505.23705|Knowledge Insulation VLA]] (stop-gradient PEFT), LoRA across [[2406.09246|OpenVLA]]/[[2410.24164|π0]] lineage, mixed data co-training.
- **Data-side**: [[2602.16710|EgoScale]] (+54% dexterous; log-linear ego scaling), [[2605.28634|PrimitiveVLA]] (full-data SR at **50%** of the data via reusable primitives), [Isaac](https://developer.nvidia.com/isaac/lab)/[Genesis](https://github.com/Genesis-Embodied-AI/Genesis) parallel sim, self-exploration via [[2602.04411|Self-evolving Embodied AI]] env-self-prediction.
- **Distillation-side**: [[2606.05254|Flash-WAM]] — modality-aware distillation drops a WAM's per-chunk latency **8.1 s → 348 ms** (**23×**) into the ~500 ms real-time budget; shows the latency-quality curve moves with method, the core B3 claim.

**Concrete research questions.**
1. **Q1 — Pareto frontier sweep**: backbone (Transformer / linear-attn / Mamba) × decoding (AR / parallel / diffusion) × precision (FP16 / INT8 / INT4) on [[2306.03310|LIBERO]] + 1 real task. Is 30 Hz on edge reachable without unacceptable SR loss?
2. **Q2 — Knowledge-insulated RL on efficient backbones.** Mamba VLA + [[2505.23705|Knowledge Insulation VLA]] stop-gradient on [[2510.13626|LIBERO-Plus]].
3. **Q3 — Data-efficient pretraining via ego co-training.** [[2602.16710|EgoScale]] + [[2510.24795|Efficient VLA Survey]]'s mixed-data recipe; measure robot data needed to match a 10×-data baseline.
4. **Q4 — Real-time joint policy+world-model in latent space.** A1's joint loop with a Mamba latent WM ([[2511.15605|SRPO]] [[2506.09985|V-JEPA 2]] substrate) should run >30 Hz.
5. **Q5 — Edge deployment chain**: train → quantize → distill → deploy on [Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) / Apple M; measure SR retention per stage; validate cross-lab via [[2605.20774|VLA-REPLICA]].

**Related research papers.**
- [[2510.24795|Efficient VLA Survey]] — Three-pillar taxonomy (model / training / data); survey only.
- [[2603.28489|Video Gen as WM Survey]] — 3D efficiency taxonomy; survey only.
- [[2505.04769|VLA Concepts Survey]] — Quantitative anchor: AR 3–5 Hz vs 20–50 Hz needed.
- [[2510.07077|VLA Robotics Real-World Review]] — Names latency a top-3 deployment concern.
- [[2511.05936|10 VLA Challenges]] — Names resource efficiency among ten bottlenecks; backs the first-class-axis framing.
- [[2605.14598|DSSP]] — Diffusion state-space policy; **62.30%** [[2506.18088|RoboTwin 2.0]] at a smaller footprint; the in-vault linear-time-backbone exemplar.
- [[2606.05737|One-Step VLA]] — High-noise-biased conditional flow matching; one-step decoding matches 10-step (**95.6%** LIBERO-Long); the decoding-side lever, no distillation or teacher needed.
- [[2605.29438|ElegantVLA]] — Phase-adaptive RL compute scheduler ("when to think"); **3.77×** FLOPs sim / **2.18×** real, control freq 16.64→35.03 Hz; per-phase compute, not a fixed rule.
- [[2606.05254|Flash-WAM]] — Modality-aware distillation; **23×** speedup to **348 ms**/chunk on RoboTwin 2.0; WAM-side proof that real-time is a method choice.
- [[2603.16195|S-VAM]] — Self-distills geometric + semantic foresight into a single pass, holding **25 Hz** at **+15.8%** latency over the teacher; resolves foresight-vs-real-time by method.
- [[2605.28634|PrimitiveVLA]] — Reusable motion primitives; matches full-data SR at **50%** data, **6×** zero-shot; the data-efficiency lever in the co-design.
- [[2505.23705|Knowledge Insulation VLA]] — Stop-gradient PEFT pattern.
- [[2602.16710|EgoScale]] — Log-linear ego scaling; **+54%** dexterous.
- [[2511.15605|SRPO]] / [[2603.16666|Fast-WAM]] — Frozen [[2506.09985|V-JEPA 2]] ~10 ms inference; train-video / test-latent.

**Benchmarks & metrics.**
- [[2306.03310|LIBERO]] — SR with no latency penalty; the quality anchor.
- [[2603.13966|vla-eval]] — **47×** training speedup; amortizes the Pareto-sweep cost.
- [[2605.20774|VLA-REPLICA]] — Low-cost reproducible real eval; validates the edge-deployed SR cross-lab (ID 0.49 vs 0.48).
- [[2502.09560|EmbodiedBench]] — General embodied AI eval.

> [!warning] Risks
> - **Linear-attn / Mamba may underperform Transformers on long-context policies** — the speed gain only matters if SR holds. → Gate every Pareto point on an SR-retention threshold; report points that fail it.
> - **Edge-hardware diversity** — [Jetson](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) vs Apple M vs custom NPUs need per-platform tuning. → Validate cross-platform via [[2605.20774|VLA-REPLICA]]'s reproducibility protocol rather than a single device.
> - **Saturation risk** — if "Mamba + LoRA + co-training" becomes the dominant recipe, the contribution shrinks to engineering. → Frame the deliverable as the Pareto curve + system-level insights, not a single point estimate.

### B4 — Continual Policy Learning Without Catastrophic Forgetting

| | |
|---|---|
| **Cluster** | B — Evaluation, Robustness & Deployment |
| **Thesis** | Protect selective subspaces during continual policy fine-tuning instead of defaulting to data-replay. In an over-parameterized policy, the parameter directions a new skill needs and those an old skill occupies are *mostly disjoint* — so forgetting-vs-plasticity is a subspace-overlap problem, not a storage one. The field assumes replaying old trajectories is the price of retention. The bet: a replay-free dual-path / subspace method beats data-replay by ≥+9.7 pp old-task SR ([[2510.20685\|C-Nav]] **42.61% vs 32.9%** on [[2109.08238\|HM3D]]) at lower storage, holding the embodiment tax <5% ([[2605.15735\|UAM]]). |
| **Anchor surveys** | [[2508.07407\|Self-Evolving AI Agents Survey]], [[2404.14387\|LLM Self-Evolution Survey]], [[2602.04411\|Self-evolving Embodied AI]] |
| **Key targets** | ≥+9.7 pp old-task SR over Data Replay ([[2510.20685\|C-Nav]] **42.61% vs 32.9%** [[2109.08238\|HM3D]]); embodiment tax **<5%** ([[2605.15735\|UAM]]); ≤−3 pp new-task SR vs full fine-tune |

**Why it matters.** Forgetting shows up elsewhere in this doc only as a *risk* — B2 names catastrophic forgetting as the hazard its recovery-update loop must avoid, citing [[2605.15735|UAM]] in passing. The deployment reality is sharper: a fielded policy is fine-tuned again and again (new objects, new tasks, new corrections from B2's loop), and every fine-tune erodes prior skill. [[2605.15735|UAM]] quantifies the "embodiment tax" — unfreezing a VLM for action fine-tuning degrades >5% of multimodal competence, but freezing it cripples action learning, a lose-lose. [[2510.20685|C-Nav]] shows the nav analog: learning new object categories forgets old ones, and naive [[1612.00796|EWC]]-style or replay mitigation carries heavy storage + privacy cost. Fresh manipulation evidence is sharper still: [[2605.26820|VLA Continual Forgetting]] shows naive sequential real-world fine-tuning collapses earlier-task score from 99.2 to 17.8, [[2606.03598|PHASER]] shows even *replay* is brittle unless budget is allocated per sub-skill phase (**+31%** when it is), and [[2605.29562|VLA-Pro]] shows weight-space adapter transfer can lift real unseen-task SR from 5.8% to 65.0% without replay. The field's reflex is replay; what's missing is a direction that treats forgetting as a *first-class* objective with a replay-free mechanism — and [[2605.29548|Capacity Interference Retention]] supplies the why: forgetting is inter-task *interference*, which scale and selective protection both reduce.

**First-principles framing.**
- **First principle**: A large policy has far more weights than any one skill needs. The handful of weight directions a new skill leans on barely overlap with the ones an old skill already uses — so forgetting happens only where they *do* overlap, in a small set of shared directions, not because the model ran out of room. The fix is therefore to *protect those shared directions*, not to re-show the old data; the clash is about which directions collide, not about missing information.
- **Assumption being challenged**: That data-replay is the safe, near-free default. [[2510.20685|C-Nav]] shows replay carries real storage + privacy cost (whole trajectories) and *still loses* to a dual-path design; [[2605.15735|UAM]] shows a dual-stream beats freeze-or-unfreeze with no replay. "Replay is the price of retention" is borrowed from supervised continual learning and never re-checked for action policies.
- **The bet**: A replay-free selective-subspace / dual-path method beats data-replay by ≥+9.7 pp old-task SR (matching [[2510.20685|C-Nav]]'s [[2109.08238|HM3D]] 42.61% vs 32.9% gain) at strictly lower storage, holding the embodiment tax <5% ([[2605.15735|UAM]]) and new-task SR within −3 pp of full fine-tune — making forgetting a controllable axis, not an accepted loss.

**Evidence.**
- [[2605.15735|UAM]] — Dual-stream (Semantic + Dorsal Expert) retains **>95%** VLM competence (embodiment tax **<5%**) without freezing or replay; biological ventral/dorsal prior.
- [[2510.20685|C-Nav]] — Dual-Path Anti-Forgetting + LOF keyframe selection beats Data Replay by **+9.7 pp** old-task SR (**42.61%** vs **32.9%**) on [[2109.08238|HM3D]], replay-free, half the data.
- [[2605.26820|VLA Continual Forgetting]] — Naive sequential fine-tune crashes earlier-task score **99.2 → 17.8** (NBT +80.0); configured replay + fixed action-norm holds within **10 pp**; the replay baseline to beat.
- [[2606.03598|PHASER]] — Phase-aware semantic experience replay; **+31%** Average SR over standard ER by guaranteeing replay budget per sub-skill phase; replay *content* matters, not just storage.
- [[2605.29562|VLA-Pro]] — Per-task procedural memory as LoRA adapters fused at inference; unseen-task SR **+207%** (RoboTwin), real **5.8% → 65.0%**; weight-space transfer, the replay-free alternative.
- [[1612.00796|EWC]] — Fisher-weighted parameter protection; the canonical subspace-importance prior B4 generalizes from classification/Atari to action policies.
- [[2605.29548|Capacity Interference Retention]] — Why larger models forget less: features learn in utility order, capacity *cuts inter-task interference*; the theory behind B4's "forgetting is interference, not capacity."
- [[2211.15944|Continual-Dreamer]] — Replay + Plan2Explore in a world model mitigates forgetting on [[2109.13202|MiniHack]]; the WM-side analog showing latent rollouts can carry continual structure.
- [[2408.07666|Model Merging in LLMs/MLLMs]] — Weight-space merging as a replay-free consolidation operator; candidate for fusing per-task policy adapters.
- [[2405.09673|LoRA-Learns-Less]] — Documents that PEFT under-fits *and* forgets less; the plasticity-vs-retention trade-off B4 must navigate explicitly.

**Concrete research questions.**
1. **Q1 — Subspace-overlap measurement.** For a sequence of [[2510.13626|LIBERO-Plus]] / object-nav tasks, measure gradient-subspace overlap between consecutive fine-tunes (principal-angle / Fisher-overlap). Hypothesis: overlap < 0.3 for most task pairs — the precondition for selective protection. Deliverable: an overlap matrix predicting which pairs forget.
2. **Q2 — Replay-free dual-path fine-tune.** [[2605.15735|UAM]]'s Semantic/Dorsal split + [[2510.20685|C-Nav]]'s representation-drift + policy-degradation losses; protect only the high-overlap (Q1) directions via [[1612.00796|EWC]]-style Fisher penalties. Baselines: full fine-tune, replay, LoRA. Target: ≥+9.7 pp old-task SR vs replay at lower storage.
3. **Q3 — Embodiment-tax probe.** After each fine-tune, re-run the frozen VLM's multimodal suite ([[2311.16502|MMMU]]/[[2306.13394|MME]]/[[2307.06281|MMBench]]). Pass: tax stays <5% across ≥5 sequential tasks.
4. **Q4 — Continual recovery integration (B2 bridge).** Feed B2's recovery-success examples as a task stream; does the subspace method stop those updates from erasing base skills? Measure old-task SR before/after 100 recovery updates.
5. **Q5 — Storage Pareto.** Sweep keyframe budget ([[2510.20685|C-Nav]] LOF) × protection strength; plot retention vs storage. Find the replay-free point that dominates replay on both axes.

**Related research papers.**
- [[2605.15735|UAM]] — Dual-stream policy; **>95%** VLM retention, **<5%** embodiment tax; architectural, no continual-task sequence.
- [[2510.20685|C-Nav]] — Continual object-nav benchmark + Dual-Path Anti-Forgetting; **+9.7 pp** old-task SR replay-free; nav-only.
- [[1612.00796|EWC]] — Fisher-weighted elastic weight consolidation; classification/Atari, predates action policies.
- [[2211.15944|Continual-Dreamer]] — Continual model-based RL with replay + Plan2Explore; world-model side, game benchmarks.
- [[2408.07666|Model Merging in LLMs/MLLMs]] — Weight-merging as a replay-free consolidation operator; not validated on action policies.
- [[2405.09673|LoRA-Learns-Less]] — PEFT under-fits but forgets less; quantifies the plasticity-retention trade-off.
- [[2605.10993|ECHO-VLA]] / [[2508.19236|MemoryVLA]] — External / activation-level memory (**+12.8 pp** LIBERO-Long; **+26 pp** temporal); complementary to weight-space protection.
- [[2602.04411|Self-evolving Embodied AI]] — 5-module framework; names continual improvement *without forgetting* as a core unsolved function.
- [[2602.10503|Long-Lived Robots]] — Interaction-free RFT (GRPO + process reward) for continual VLA: negative backward transfer **1.5 vs SFT's 6.8**, **+19.6%** forward transfer at **20%** data; the RFT continual baseline to beat.
- [[2603.24350|Emergent Self]] — In continual quadruped RL, a behavior-invariant subnetwork forms and persists (**+16.9 pp**, p<0.001) while task-specific parts reorganize; evidence for B4's "stable shared subspace" principle.
- [[2505.06111|UniVLA]] — Unified cross-task policy; the multi-skill backbone B4's protection bolts onto.

**Benchmarks & metrics.**
- [[2510.20685|C-Nav]] continual object-nav benchmark — first continual-nav suite; old-task SR **42.61%** vs **32.9%** (Data Replay) on [[2109.08238|HM3D]] final stage; the head-to-head B4 extends to manipulation.
- [[2510.13626|LIBERO-Plus]] — 10,030 OOD perturbations; sequence [[2306.03310|LIBERO]] task suites to measure forgetting under distribution shift.
- [[2502.09560|EmbodiedBench]] — General embodied eval; whole-capability retention check after a continual fine-tune sequence.
- [[2311.16502|MMMU]] / [[2306.13394|MME]] / [[2307.06281|MMBench]] (via [[2605.15735|UAM]]) — multimodal-competence suite for the embodiment-tax measurement.

> [!warning] Risks
> - **Subspaces may not be disjoint for *similar* tasks** — two manipulation skills sharing contact dynamics could overlap heavily, collapsing the geometric premise. → Q1's overlap matrix is the go/no-go: if overlap >0.5 dominates, fall back to memory ([[2605.10993|ECHO-VLA]]) rather than subspace protection.
> - **Plasticity collapse** — protecting too many directions freezes new-task learning (the [[2405.09673|LoRA-Learns-Less]] failure mode). → Bound protection strength by the ≤−3 pp new-task-SR target; report the retention/plasticity frontier, not a single point.
> - **Replay quietly wins at scale** — if storage is cheap and privacy a non-issue, replay may stay competitive. → Frame the deliverable as the storage-vs-retention Pareto (Q5); the claim is *dominance on both axes*, not merely matching replay.

---

## Cluster C — Mobility & Embodiment Generalization

*Moving the robot through the world (navigation) and across bodies (cross-embodiment, morphology-invariance) — where the fixed-base and fixed-body assumptions break.*

### C1 — Latent In-Policy Dreaming for Vision-and-Language Navigation

| | |
|---|---|
| **Cluster** | C — Mobility & Embodiment Generalization |
| **Thesis** | Put a latent dream-ahead head *inside* the navigation policy instead of bolting on an external world model. Foresight needs only the *control-relevant* slice of the future, which a latent token carries far more cheaply than a rendered frame. The field assumes anticipatory VLN needs an external pixel-space world model. The bet: an in-policy latent dream head matches or beats external-WM VLN SOTA at a fraction of the cost — [[2603.29165\|LatentPilot]] **62.0% SR / 58.0% SPL** on [[2004.02857\|R2R-CE]] Val-Unseen at **130 ms / 22.8 GB**, with [[2506.23468\|NavMorph]] adding **+4.1% SR** at **2.1× faster** than gradient adaptation. |
| **Anchor surveys** | [[2311.00530\|LLM Embodied Navigation Survey]], [[2605.00080\|WM Robot Learning Survey]], [[2504.21853\|Interactive Generative Video Survey]] |
| **Key targets** | ≥62.0% SR / 58.0% SPL [[2004.02857\|R2R-CE]] Val-Unseen at ≤130 ms / 22.8 GB ([[2603.29165\|LatentPilot]]); **+4.1% SR** online adaptation at **2.1×** speed ([[2506.23468\|NavMorph]]) |

**Why it matters.** VLN agents decide myopically from current observations alone; the obvious fix — an external world model rendering candidate futures — adds compounding prediction error, memory, and latency ([[2603.29165|LatentPilot]]'s critique). This is the same latent-beats-external bet A1 makes for manipulation, but navigation has its own evidence: [[2603.29165|LatentPilot]] internalizes anticipatory reasoning as a single "Pilot Token" and reaches **62.0% SR** on [[2004.02857|R2R-CE]] Val-Unseen at **130 ms / 22.8 GB**, beating external world models on *both* accuracy and efficiency. [[2506.23468|NavMorph]] adds the other half — a compact RSSM that self-evolves online via a Contextual Evolution Memory, **2.1× faster** than gradient adaptation and **+4.1% SR** on unseen [[2010.07954|RxR-CE]]. The gap: no work fuses in-policy latent dreaming ([[2603.29165|LatentPilot]]) with online self-evolution ([[2506.23468|NavMorph]]) and measures the joint efficiency-accuracy frontier against reasoning-heavy VLN ([[2605.22816|AwareVLN]] hits **73.5% SR** with an explicit reasoning data engine).

**First-principles framing.**
- **First principle**: A navigation decision needs only the *control-relevant* slice of the future — "will this action open a path to the goal?" — not a photorealistic render of the next viewpoint. That slice is low-dimensional and lives naturally in a latent token; rendering pixels to recover it wastes compute on a per-step closed loop.
- **Assumption being challenged**: That anticipatory VLN needs an external pixel-space world model. The explicit-lookahead work ([[2309.17080|GAIA-1]]-style simulators, candidate-future rendering) treats foresight and generation as one problem; [[2603.29165|LatentPilot]]'s Pilot Token and [[2506.23468|NavMorph]]'s RSSM already carry the control-relevant future in latent space for far less — yet external-WM VLN is still the default.
- **The bet**: An in-policy latent dream head, optionally self-evolving online, matches or beats external-WM VLN SOTA — ≥62.0% SR / 58.0% SPL on [[2004.02857|R2R-CE]] Val-Unseen at ≤130 ms / 22.8 GB ([[2603.29165|LatentPilot]]) and ≥+4.1% online-adaptation SR at 2.1× the speed of gradient adaptation ([[2506.23468|NavMorph]]) — proving foresight is a representation choice, not an external module.

**Evidence.**
- [[2603.29165|LatentPilot]] — Pilot Token in-policy latent dreaming; **62.0% SR / 58.0% SPL** [[2004.02857|R2R-CE]] Val-Unseen at **130 ms / 22.8 GB**; future obs as privileged supervision (PilotLoop).
- [[2606.04907|WAM-Nav]] — Asymmetric latent WAM: long-horizon action + 1-step latent visual foresight in one DiT; **+15.7% SR** over NavDP on Image-Goal, real **85%** on a Unitree G1; the joint-action-plus-foresight design.
- [[2506.23468|NavMorph]] — Self-evolving RSSM + Contextual Evolution Memory; **+4.1% SR / +2.73% SPL** [[2010.07954|RxR-CE]] unseen, **2.1×** faster than gradient adaptation, no test-time backprop.
- [[2605.22816|AwareVLN]] — Reasoning-augmented VLN; **73.5% SR / 65.4% SPL** [[2004.02857|R2R-CE]] Val-Unseen, monocular RGB, strong sim-to-real; the reasoning-heavy alternative to justify against on efficiency.
- [[2606.03682|GN0]] — Unified generation + eval + policy VLN pipeline (3DGS data); **67.7% SR / 63.4% SPL** R2R Val-Unseen with **zero** real-world training; the rendered-data alternative to latent foresight.
- [[2411.04983|DINO-WM]] — Latent world model planning in [[2304.07193|DINOv2]] feature space; the manipulation-side proof that latent rollouts plan without pixel decoding.
- [[2402.19161|MemoNav]] — Goal-aware working memory for image-goal navigation; the memory-as-foresight precursor [[2506.23468|NavMorph]]'s CEM generalizes.

**Concrete research questions.**
1. **Q1 — Fuse in-policy dreaming with online self-evolution.** Bolt [[2506.23468|NavMorph]]'s Contextual Evolution Memory onto [[2603.29165|LatentPilot]]'s Pilot Token: does a test-time CEM update improve the dreamed latent without the gradient-adaptation cost? Target: stay ≤130 ms while gaining [[2506.23468|NavMorph]]'s +4.1% online-adaptation SR.
2. **Q2 — Latent dream horizon ablation.** Vary the imagined horizon (1-step vs k-step Pilot-Token rollout); measure SR/SPL vs latency. Where does deeper dreaming stop paying off on [[2004.02857|R2R-CE]] / [[2010.07954|RxR-CE]]?
3. **Q3 — Privileged-supervision transfer.** [[2603.29165|LatentPilot]]'s PilotLoop uses future observations as privileged supervision in sim — does this signal transfer to real deployment ([[2507.13019|VLN-PE]] Fall/Stuck rate) without sim-only collapse?
4. **Q4 — Latent vs reasoning-token foresight.** Head-to-head: latent Pilot Token ([[2603.29165|LatentPilot]]) vs explicit reasoning trace ([[2605.22816|AwareVLN]]) at matched backbone. Is the accuracy gap worth the latency cost on closed-loop nav?
5. **Q5 — Cross-embodiment nav deployment.** Does the latent dream head transfer zero-shot to a new mobile base, or does it need C2-style morphology-invariance?

**Related research papers.**
- [[2603.29165|LatentPilot]] — In-policy Pilot Token latent dreaming; **62.0% SR** [[2004.02857|R2R-CE]]; SOTA accuracy + efficiency; no online self-evolution.
- [[2606.04907|WAM-Nav]] — Joint long-horizon action + latent foresight in one DiT; **+15.7%** Image-Goal SR, real **85%**; multi-task but single-step foresight, no online evolution.
- [[2506.23468|NavMorph]] — Self-evolving RSSM + CEM; online adaptation **2.1×** faster than gradient; not fused with in-policy dreaming.
- [[2605.22816|AwareVLN]] — Reasoning-data-engine VLN; **73.5% SR**; explicit reasoning, heavier than latent dreaming.
- [[2606.03682|GN0]] — Unified data-gen + sim/eval + policy VLN; **67.7%** R2R Val-Unseen, zero real-world training; solves transfer with rendered data, orthogonal to in-policy foresight.
- [[2604.08509|Visually-grounded Humanoid Agents]] — Humanoid VLN agents; the embodiment C1's nav head must eventually drive ([[Whole-Body|Whole-Body]]).
- [[2311.00530|LLM Embodied Navigation Survey]] — Names long-horizon grounding + context limits; the open-problem frame.
- [[2411.04983|DINO-WM]] — Latent world-model planning; manipulation-side latent-rollout proof.
- [[2402.19161|MemoNav]] — Working-memory image-goal nav; CEM precursor.
- [[2603.25981|PiJEPA]] — Policy-guided MPPI planning over a JEPA latent WM ([[2506.09985|V-JEPA 2]]/[[2304.07193|DINOv2]]); the policy warm-starts the planner's prior; **1.65 m** RMSE; policy-plus-latent-WM fusion.
- [[2603.07799|MWM]] — Mobile WM trained for action-conditioned *consistency* via distillation (**4×** rollout speedup, real goal-image SR **0.30** vs NoMaD **0.08**); the external nav-WM C1 sidesteps.
- [[2603.02772|ASER]] — Agentic self-evolutionary replanning that adapts the action model online from feedback (**+10%** SR, **20-40%** fewer tokens); the runtime self-evolution C1 pairs with dreaming.
- [[2604.24391|FreqCache]] — Frequency-guided token caching cuts VLN per-step latency **637 → 401 ms** (**1.59×**) at **76.0%** Oracle SR; the inference-acceleration lever on C1's frontier.
- [[2309.17080|GAIA-1]] — Generative driving world model; the external-pixel-WM paradigm C1 bets against.
- [[2403.09631|3D-VLA]] — 3D world model for embodied planning; the heavier generative alternative.

**Benchmarks & metrics.**
- [[2004.02857|R2R-CE]] Val-Unseen — Continuous-environment VLN; [[2603.29165|LatentPilot]] **62.0% SR / 58.0% SPL**, [[2605.22816|AwareVLN]] **73.5% SR**; the headline efficiency-vs-accuracy battleground.
- [[2010.07954|RxR-CE]] Val-Unseen — Multilingual long-instruction VLN; [[2506.23468|NavMorph]] **+4.1% SR / +2.73% SPL** online adaptation; the self-evolution axis.
- [[2507.13019|VLN-PE]] — Physical-embodiment VLN; [[2603.29165|LatentPilot]] **10.65%** Fall Rate / **0.97%** Stuck Rate; the sim-to-real robustness axis.

> [!warning] Risks
> - **Latent dreaming may not help on long-horizon [[2010.07954|RxR-CE]]** — Pilot Token foresight could plateau where explicit reasoning ([[2605.22816|AwareVLN]]) still wins. → Q4's head-to-head bounds the claim to the regimes where latent foresight is cost-competitive; report where it loses.
> - **Online self-evolution can drift** — CEM updates at test time risk catastrophic adaptation to a misleading episode. → Gate CEM writes behind a confidence check; borrow B4's forgetting-aware protection for the test-time update.
> - **Sim-only privileged supervision** — PilotLoop's future-obs supervision exists only in sim; real deployment loses it. → Q3 validates [[2507.13019|VLN-PE]] transfer before claiming real-world foresight; fall back to [[2506.23468|NavMorph]]'s unsupervised CEM if it collapses.

### C2 — Morphology-Invariant Action Representations for Cross-Embodiment Zero-Shot Transfer

| | |
|---|---|
| **Cluster** | C — Mobility & Embodiment Generalization |
| **Thesis** | Use a morphology-invariant action representation instead of tokenizing actions in each robot's native joint space. "Pick up the cup" names the same *task intent* regardless of the arm executing it, so an embodiment-agnostic action space is the natural representation and per-morphology tokenization is the accidental one. The field assumes cross-embodiment transfer needs per-robot fine-tuning. The bet: a morphology-invariant representation breaks [[2505.14986\|AnyBody]]'s extrapolation wall — it reports **0%** zero-shot SR on novel link structures, while [[2602.10556\|LAP]]'s language-action space hits **>50%** zero-shot (**2×** prior policies) and [[2605.20811\|Demo-JEPA]] reaches **0.36 vs 0.04** one-shot — target **>30%** on [[2505.14986\|AnyBody]]'s extrapolation split. |
| **Anchor surveys** | [[2510.07077\|VLA Robotics Real-World Review]], [[2504.03515\|Dexterous IL Survey]], [[2604.04707\|OpenWorldLib]] |
| **Key targets** | >30% extrapolation SR on [[2505.14986\|AnyBody]] novel-morphology split (current **0%**); >50% zero-shot cross-embodiment ([[2602.10556\|LAP]], **2×** prior policies); **0.36** one-shot ([[2605.20811\|Demo-JEPA]], vs **0.04** [[2412.14803\|VPP]]) |

**Why it matters.** [[2505.14986|AnyBody]] is the brutal diagnostic: multi-embodiment policies match single-embodiment baselines on *seen* robots and *interpolation*, but collapse to **0%** SR on *extrapolation* to very different link structures. [[2510.07077|VLA Robotics Real-World Review]] names embodiment transfer a top open problem; [[2504.03515|Dexterous IL Survey]] names it a core barrier. The counter-evidence is about *representation choice*: [[2602.10556|LAP]] parses continuous actions into *natural language* ("language-actions"), aligning the action space with the VLM's pretraining, and hits **>50%** zero-shot across unseen embodiments (**2×** prior policies, 2.5× fewer demos); [[2605.20811|Demo-JEPA]] abstracts demonstrations into *target-compatible latent goals*, reaching **0.36** one-shot SR vs [[2412.14803|VPP]]'s **0.04**. Both replace native-joint tokenization with an invariant intermediate — but neither has faced [[2505.14986|AnyBody]]'s extrapolation wall, still the unbeaten 0% benchmark.

**First-principles framing.**
- **First principle**: "Pick up the cup" denotes the same *task intent* for a 7-DoF arm, a parallel gripper, or a humanoid hand. The intent is morphology-invariant; the joint-space trajectory is morphology-specific. A representation grounded in intent (language, latent goal, or task-space) is invariant *by construction*; native-joint tokenization is the accidental one that couples policy to body.
- **Assumption being challenged**: That cross-embodiment transfer needs per-robot fine-tuning — the norm ([[2212.06817|RT-1]] / [[2409.20537|HPT]] / [[2510.10274|X-VLA]] all retrain or adapt per body). [[2602.10556|LAP]]'s language-actions and [[2605.20811|Demo-JEPA]]'s latent goals already get *zero-shot* transfer from an invariant intermediate — yet [[2505.14986|AnyBody]] shows the best multi-embodiment policies still hit 0% on true extrapolation, because they tokenize in joint space.
- **The bet**: A morphology-invariant action representation reaches >30% zero-shot SR on [[2505.14986|AnyBody]]'s extrapolation split (current best: **0%**), consistent with [[2602.10556|LAP]]'s **>50%** zero-shot and [[2605.20811|Demo-JEPA]]'s **0.36** one-shot — turning extrapolation to novel link structures from an impossibility into a measurable transfer rate.

**Evidence.**
- [[2505.14986|AnyBody]] — 18-robot cross-embodiment benchmark; interpolation transfers, extrapolation/composition collapse to **0%**; the wall C2 must break.
- [[2602.10556|LAP]] — Language-action pre-training; **>50%** zero-shot across unseen embodiments (**2×** prior policies), **2.5×** fewer demos; intent-grounded action space.
- [[2605.20811|Demo-JEPA]] — JEPA target-compatible latent goals; **0.36** sim / **0.25** real one-shot (vs [[2412.14803|VPP]] **0.04** / [[2307.09955|XSkill]] **0.03**); demonstration-as-latent-goal abstraction.
- [[2409.20537|HPT]] — Heterogeneous pre-training with shared trunk + per-embodiment stems; **10–30%** transfer gain; the stem-tokenizes-per-robot baseline C2 challenges.
- [[2510.10274|X-VLA]] — Soft-prompt cross-embodiment policy; SOTA on 5/6 benchmarks, **93%** [[2306.03310|LIBERO]] at 1% params; strong but still adapts per platform.
- [[2505.06111|UniVLA]] — Unified cross-task/embodiment policy; **95.2%** [[2306.03310|LIBERO]], **47.1%** [[2004.02857|R2R]]; latent-action backbone.

**Concrete research questions.**
1. **Q1 — Invariant-representation bake-off on [[2505.14986|AnyBody]].** Run [[2602.10556|LAP]] (language-action), [[2605.20811|Demo-JEPA]] (latent goal), and task-space tokenization head-to-head on [[2505.14986|AnyBody]]'s extrapolation/composition splits. Which invariant beats 0%? Target: >30% extrapolation SR.
2. **Q2 — Why does joint-space tokenization fail at 0%?** Probe whether [[2409.20537|HPT]]-style per-embodiment stems memorize morphology rather than learn invariant control. Measure representation overlap across morphologies (low overlap → memorization).
3. **Q3 — Composing language-action + latent-goal.** Do [[2602.10556|LAP]]'s language intermediate and [[2605.20811|Demo-JEPA]]'s latent goal compose (language for *what*, latent for *how-on-this-body*)? Target: beat either alone on [[2505.14986|AnyBody]] composition.
4. **Q4 — Invariance vs precision trade-off.** Invariant spaces may lose fine control. Measure precision (EE error) of invariant-space vs native-joint policies on seen robots; bound the invariance tax.
5. **Q5 — Transfer to mobile / whole-body bodies.** Does the invariant representation extend from fixed arms to the humanoid whole-body ([[Whole-Body|Whole-Body]]), or does whole-body coupling break intent-invariance?

**Related research papers.**
- [[2505.14986|AnyBody]] — 18-robot benchmark; **0%** extrapolation; the unbeaten morphology wall.
- [[2602.10556|LAP]] — Language-action pre-training; **>50%** zero-shot; intent-grounded invariant space.
- [[2605.20811|Demo-JEPA]] — Latent-goal one-shot imitation; **0.36 vs 0.04**; JEPA abstraction.
- [[2409.20537|HPT]] — Heterogeneous pre-training; **10–30%** transfer; per-embodiment stems (joint-space, the baseline).
- [[2510.10274|X-VLA]] — Soft-prompt cross-embodiment; **93%** [[2306.03310|LIBERO]] at 1% params; per-platform adaptation.
- [[2505.06111|UniVLA]] — Unified latent-action policy; **95.2%** [[2306.03310|LIBERO]]; cross-task + cross-embodiment.
- [[2212.06817|RT-1]] — Foundational cross-embodiment robot transformer; native action tokens.
- [[2507.23682|villa-X]] — Latent-action cross-embodiment policy; the lineage [[2605.20811|Demo-JEPA]] extends.
- [[2606.03943|PointAction]] — 3D pointmaps as an embodiment-agnostic action interface (universal 4D WM + lightweight per-robot decoder); real transfer **43.0%** xArm7, **2-2.5×** over baselines; a *third* invariant intermediate beside language and latent goals.
- [[2605.25044|X-DiffVLA]] — Single diffusion head generalizing across grippers and dexterous hands *after* training (no per-embodiment head), via morphological-tree diffusion; **+15.3 pp** over π0.5 on RoboCasa; attacks the "per-robot fine-tuning" assumption.
- [[2605.30280|Qwen-VLA]] — Unifies manipulation + navigation + embodiments via embodiment-aware prompts; **97.9%** [[2306.03310|LIBERO]], **76.9%** ALOHA OOD, R2R **57.5%**; the cross-embodiment generalist baseline.
- [[2606.02745|SeeTraceAct]] — One-shot cross-embodiment skill learning via a visibility-aware visual latent plan (EE-trace supervised); **+12.5 pp** real over baselines; the demo-as-latent-intermediate route.
- [[2509.00576|G0]] / [[2512.13030|Motus]] — Latent-action staged / multi-stage pretraining; >50% planner gain; **+10%** SR from latent actions.

**Benchmarks & metrics.**
- [[2505.14986|AnyBody]] extrapolation/composition splits — novel link structures; **0%** current SR; the primary go/no-go (target >30%).
- [[2602.10556|LAP]] zero-shot suite — 3 unseen embodiments × 6 tasks; **>50%** zero-shot SR (**2×** prior policies); the cross-embodiment headline.
- [[2605.20811|Demo-JEPA]] one-shot cross-embodiment — sim **0.36** / real **0.25** vs [[2412.14803|VPP]] **0.04** / [[2307.09955|XSkill]] **0.03**; the one-shot imitation axis.

> [!warning] Risks
> - **Invariance may cost precision** — a language/latent action space could blur fine-grained control native joints capture. → Q4 bounds the invariance tax on seen robots before claiming extrapolation gains; report the precision floor.
> - **[[2505.14986|AnyBody]]'s 0% may be partly task-hardness, not pure morphology** — extrapolation tasks could be intrinsically harder. → Control with interpolation SR on the *same* tasks; attribute the gap to morphology only if interpolation succeeds.
> - **Language-actions discretize continuous control** — [[2602.10556|LAP]]'s parsing may lose high-frequency detail. → Pair the language intermediate with a knowledge-insulated continuous action expert ([[2602.10556|LAP]]'s own design) rather than acting in language directly.

---

## Cross-Cutting Themes

> [!tip] Latent-Space Prediction Is the Default Substrate
> A1, A2, B1, and B3 share one substrate decision: supervise on video/pixel at training, predict in latent at deployment. A1's joint loop is tractable only because latent rollout is ~10 ms vs pixel ~150 ms; A2's latent CoT keeps step-reward supervision latency-free; B3 makes this the *primary* thesis (latent + Mamba for >30 Hz); B1 must score causal consistency in that same latent space. [[2603.16666|Fast-WAM]] and [[2511.08544|LeJEPA]] are the shared anchors — the latent must be both cheap and non-collapsing.

> [!tip] Step-Level Verifiable Rewards Beat Outcome-Only Signals
> A2, A3, and B2 all reject the sufficiency of terminal reward. A2 applies [[2604.22074|CIR/SR Reasoning]]'s "outcome rewards don't guarantee causal reasoning" to latent tokens; A3 turns physical laws into per-step verifiable predicates over action sequences; B2 turns each successful recovery into a verified training example. The shared move — swap a single sparse outcome signal for a dense stream of locally-checkable predicates — is the most actionable 2026 result the three share.

> [!tip] Detection-Diagnosis-Recovery as a Unified Stack
> B2 builds the loop explicitly; A1, A2, and B1 each supply one face. A1's failure-finder adversary surfaces the perturbations that should trigger detection; A2's CoT-faithfulness probe is a diagnosis instrument; B1's joint causal metric certifies recovery actually closed the loop. [[2602.04411|Self-evolving Embodied AI]]'s 5-module framework is the formalization all four point at.

> [!tip] Efficiency and Safety Are Deployment-Blocking, Not Optional
> B3 makes efficiency a first-class axis; A1, B1, and B2 all assume real-time, so B3's Pareto curve is the enabling condition for the rest. Safety cuts the same way: [[2605.02900|Safety in Embodied AI Survey]]'s five-layer attack taxonomy means B1's joint metric must include adversarial baselines and B2's memory loop must defend against poisoning. [[2505.04769|VLA Concepts Survey]]'s 3–5 Hz ceiling and the Safety survey's cascade-propagation finding are the two anchors that turn "nice to have" into "blocks deployment."

> [!tip] Latent-Beats-External Generalizes From the Bench to the World
> The doc's central architectural bet — predict the control-relevant future in latent space, not pixels — was scoped to fixed-base manipulation in A1 and B3. C1 carries it into *navigation*: [[2603.29165|LatentPilot]]'s in-policy Pilot Token beats external pixel-space world models on [[2004.02857|R2R-CE]] at **130 ms / 22.8 GB** — the same latent-is-cheaper argument A1 makes for the joint loop and B3 makes its primary thesis. [[2506.23468|NavMorph]]'s feature-level RSSM is the navigation analog of [[2411.04983|DINO-WM]]'s manipulation latent planner. The lesson: foresight is a representation choice across mobility *and* manipulation — external-world-model framing is a pixel-space legacy in both.

> [!tip] Structure-Preserving Beats Structure-Discarding
> Don't discard the structure the data carries — the principle A1 and A3 exploit, and the one C2 extends to *bodies*. C2 keeps the *morphology-invariant* task intent that native-joint tokenization throws away ([[2602.10556|LAP]] **>50%** zero-shot, [[2605.20811|Demo-JEPA]] **0.36** one-shot vs [[2505.14986|AnyBody]]'s 0% wall). Its twin — keeping the *coupled* whole-body dynamics part-independent policies throw away ([[2604.07993|HEX]] **61.8% OOD** by modeling cross-part proprioception) — is the load-bearing claim of the sibling [[Whole-Body|Whole-Body]] doc. Coupling and invariance are one lens: the same move as A1's "the joint $p(o',a)$ is the natural loss" and A3's "physical laws are invariant by construction" — refusing to factor away load-bearing structure, whether that's coupled dynamics or morphology-invariant intent.

> [!tip] Forgetting Is the Tax on Every Loop That Updates Weights
> B4 promotes catastrophic forgetting from a B2 risk-footnote to a direction, and it underwrites every other update loop here. B2's continual recovery updates ([[2510.02298|ARMADA]] pooled-intervention pattern) erase base skills unless B4's subspace protection holds; C1's online CEM self-evolution ([[2506.23468|NavMorph]]) can drift catastrophically at test time; C2's per-embodiment fine-tuning is forgetting across *bodies*, not tasks. [[2605.15735|UAM]]'s **<5%** embodiment tax and [[2510.20685|C-Nav]]'s **+9.7 pp** replay-free retention show the tax is controllable — but only if forgetting is a first-class objective.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Joint-vs-alternating co-training ablation on a fixed latent backbone | A1 | None ([[2605.21800\|stable-worldmodel]] supplies the OOD harness but not the joint-vs-alternating grid) |
| Causal faithfulness of latent reasoning under compositional novelty | A2 | [[2406.15349\|NAVSIM]] (driving CoT) + [[2510.16281\|SEAL]] (runtime verifier, not benchmark) |
| Physics-consistency of policy *action* sequences against a verifiable simulator | A3 | [[2605.08567\|ACWM-Phys]] (WM rollouts) + [[2604.17896\|Physical-Feasibility VLA]] (geometric only) |
| Joint WM-action causal-consistency metric on manipulation | B1 | [[2603.22212\|Omni-WorldBench]] (WM-only) + [[2603.22078\|WAM vs VLA Robustness]] (separate axes) + [[2605.06311\|VISER]] (sim-real r, no action causality) |
| Integrated detect-diagnose-recover loops on long-horizon real tasks | B2 | [[2605.10921\|RoboMemArena]] (memory) + [[2506.18123\|RoboArena]] (no recovery stack) |
| Policy SR × control freq × edge-compute Pareto | B3 | [[2306.03310\|LIBERO]] (SR only) + [[2603.13966\|vla-eval]] (training speedup) + [[2605.20774\|VLA-REPLICA]] (real SR, no compute axis) |
| Replay-free continual policy fine-tuning with bounded embodiment tax | B4 | [[2510.20685\|C-Nav]] (continual object-nav, **+9.7 pp** replay-free) + [[2605.15735\|UAM]] (**<5%** tax, no task sequence) + [[1612.00796\|EWC]] (classification/Atari, pre-action-policy) |
| Joint in-policy latent-dreaming + online self-evolution for VLN | C1 | [[2603.29165\|LatentPilot]] (in-policy dreaming, no online evolution) + [[2506.23468\|NavMorph]] (online CEM, not fused with dreaming) |
| Zero-shot extrapolation to novel link structures (morphology-invariant) | C2 | [[2505.14986\|AnyBody]] (**0%** extrapolation wall) + [[2602.10556\|LAP]] (**>50%** zero-shot, untested on [[2505.14986\|AnyBody]]) + [[2605.20811\|Demo-JEPA]] (**0.36** one-shot) |

---

## Cross-References

- [[05_VLA|05_VLA]] — VLA design space
- [[07_WAM|07_WAM]] — WAM taxonomy (VideoGen / latent / Dreamer / VLM-integrated / efficient / self-evolving)
- [[08_Latent-World-Models|08_Latent-World-Models]] — JEPA evolution + alternative latents
- [[13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]] — Failure detection, diagnosis, recovery
- [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] — Physics-aware design space
- [[06_VLA-Reasoning-and-CoT|06_VLA-Reasoning-and-CoT]] — Reasoning insertion slots
- [[12_Egocentric-Pretraining-and-Human-Video|12_Egocentric-Pretraining-and-Human-Video]] — Egocentric scaling + transfer
- [[09_Contact-Rich-and-Whole-Body-Control|09_Contact-Rich-and-Whole-Body-Control]] — Force-aware architectures + tactile sensors
- [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]] — Zero-shot sim-to-real for humanoid loco-manipulation (see [[Whole-Body|Whole-Body]]) + cross-embodiment transfer (C2)
- [[02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]] — Data + sim + benchmark stacks ([[2505.14986|AnyBody]], [[2403.10506|HumanoidBench]], VLN-CE)
- [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Navigation, humanoid, and cross-embodiment paper index (Cluster C)
- [[08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — Canonical survey index
- [[WAM|WAM]] — Focused WAM deep-dive sibling. Hosts the WAM-specific directions (representation substrate, contact-mode latent, calibrated imagination); this umbrella doc develops the cross-family directions WAM hands off (A1, A3, B1, B3, C2).
- [[Sim2Real|Sim2Real]] — Sibling doc on sim-to-real / real-to-sim transfer; borders this doc's physics-consistency (A3) and world-model-as-simulator directions.
- [[Manipulation|Manipulation]] — Subsystem sibling (arms + hands): grasping, contact-rich assembly, bimanual, dexterous/in-hand. Its Cluster E (E1/E2) develops the tactile-substrate foundations — egocentric force pretraining, cross-sensor tactile.
- [[Locomotion|Locomotion]] — Subsystem sibling (legs + wheels): bipedal + quadruped locomotion. Consumes this doc's C1 (VLN) and C2 (morphology-invariance) directions.
- [[Whole-Body|Whole-Body]] — Subsystem sibling (the coupling): whole-body loco-manipulation, mobile manipulation, force-adaptive control.
