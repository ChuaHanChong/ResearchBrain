---
title: "Promising Research Directions: VLA × WAM × Embodied AI"
tags:
  - project
  - planning
  - VLA
  - WAM
  - embodied-AI
  - self-evolving
aliases:
  - "VLA-WAM Promising Directions"
---

# Promising Research Directions: VLA × WAM × Embodied AI

> [!info] Scope
> Eight directions across three thematic clusters (*Foundations / Architecture & Training / Evaluation, Robustness & Deployment*), synthesized from 54 VLA / WAM / embodied-AI surveys + 10 `Embodied-AI/` deep-dives. 11 central surveys verified against alphaxiv overview reports. Each direction is actionable enough that a PhD student could start within a week.

---

## Methodology

- **Survey enumeration**: 54 unique surveys from `_KnowledgeHub_/` tag-scans + reference sweeps of [[03_VLA]], [[04_WAM]], [[07_Physics-Aware-Embodied-AI]]; cross-checked against [[08_Benchmarks-and-Surveys|General/08]] §4/§5/§7.
- **alphaxiv verification**: open-problem cells for 11 central surveys verified against `https://www.alphaxiv.org/overview/{ID}.md`.
- **Deep-dive mining**: full reads of the 5 deep-dives directly aligned with the directions ([[04_WAM]], [[06_Self-Evolving-VLA-WAM]], [[07_Physics-Aware-Embodied-AI]], [[08_VLA-Reasoning-and-CoT]], [[10_Force-Aware-and-Tactile-Policies]], [[11_Sim-to-Real-Transfer]]); others consulted for taxonomy framing.
- **Filter**: kept directions with 3–10 attacking papers but no consensus solution; excluded saturated (more-compute) and premature (hypothetical-AGI) framings; prioritized intersections (VLA×WAM, VLA×RL, WAM×egocentric, tactile×VLA, physics×RL).

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **I — Foundations** | 1, 2 | Contact-rich, multi-modal data scarcity (4-order gap vs OXE) | D2's cross-sensor tactile encoder is the deployment substrate D1 needs to make ego-pretrained policies transferable across platforms |
| **II — Architecture & Training** | 3, 4, 5 | Training objectives don't match causal structure of physical reasoning | D3's latent co-evolving substrate exposes the intermediate tokens D4 needs for step rewards; D5's physics-verifiable rewards stabilize D3's joint loop |
| **III — Evaluation, Robustness & Deployment** | 6, 7, 8 | Lab-to-real deployment gap (3–5 Hz ceiling, no joint metrics, no recovery loops) | D6's joint causal-consistency metric measures whether D3/D5 gains transfer; D7's memory + recovery loop needs D8's efficiency co-design |

---

## Survey Landscape

| Survey | Scope | Stated open problems |
|---|---|---|
| [[2605.12090\|WAM Survey]] | Formal WAM def; Cascaded vs Joint taxonomy | Causal-consistency joint metrics; data-ecosystem mixing; separate WM-vs-action eval gap; tactile/force/acoustic extension; long-horizon drift; closed-loop latency |
| [[2605.00080\|WM Robot Survey 2026]] | Multi-dim taxonomy; decoupled → unified VLA/MoE/MoT | Eval beyond visual fidelity; closed-loop vs open-loop; latent WM dominance; causal conditioning; failure-recovery datasets; cross-embodiment |
| [[2605.03941\|iWorld-Bench]] | Interactive WM eval | Standardized interactive evaluation across WAM types |
| [[2605.05017\|Privacy-Utility Trade-off]] | Life-cycle privacy; SPINE + L1–L4 | Compositional leakage; regulatory-technical gap; non-linear utility trade-off (~30% SR drop); adaptive orchestration |
| [[2604.27621\|Robot Learning from Human Videos Survey]] | Task/observation/action LfHV taxonomy | Action-oriented transfer; physically-grounded WMs; physics-aware affordance; continual learning; multi-agent; tactile/audio/gaze; low-quality-video robustness |
| [[2604.15395\|Foundation Models in Robotics Survey]] | 435 papers; 6-criteria taxonomy; 5-phase evolution | Tactile/failure-data scarcity; embodiment-agnostic action spaces; latency; long-horizon memory; physics-informed WMs; formal verification |
| [[2604.16592\|Cognition WM Survey]] | CAT taxonomy: Video / Embodied / Epistemic WMs | Motivation + meta-cognition drastically under-developed; epistemic WMs over structured knowledge |
| [[2604.04974\|Video-to-Control Survey]] | Robotics integration layer; interface-centric taxonomy | Integration layer is critical gap; interface trade-offs; tracking-error; latent-action identifiability; pre-execution verification; tactile/force integration |
| [[2604.23775\|VLA Safety Survey]] | Training/inference threats | Multi-layered defense; fragmented evaluation methodology |
| [[2604.26509\|3D Generation for Embodied AI Survey]] | Conventional vs embodied-oriented 3D gen | Physical-annotation scarcity; geometry-vs-physics; deformables; sim-to-real |
| [[2604.22748\|Agentic World Modeling Survey]] | L1/L2/L3 × physical/digital/social/scientific laws; ASR + COD | Counterfactual reasoning; constraint adherence; autonomous self-revision (L3); decision-centric metrics |
| [[2604.04707\|OpenWorldLib]] | Unified WM framework | Definition fragmentation; 3D geometric consistency under camera motion; modular pipeline composition |
| [[2604.00061\|R2X Multi-Robot MLLM Survey]] | MLLM-driven multi-robot | Bandwidth; open-vocab perception; joint sensing/comms/compute |
| [[2604.28185\|Visual Generation Survey]] | 5-level visual intelligence + in-the-wild stress tests | Spatial reasoning + physical-law gaps in frontier models; multi-turn editing degradation; L4 agentic frontier |
| [[2604.15911\|Efficient Video Diffusion Survey]] | 4-category acceleration taxonomy | KV cache movement; 1–4 step distillation; sparse attention; QAT/PTQ |
| [[2604.02029\|Latent Space Survey]] | 5-aspect framework | Evaluability/controllability/interpretability; theory gap; modality-native integration; governable latent AI |
| [[2603.28489\|Video Gen as WM Survey]] | Efficiency-focused 3D taxonomy | Efficiency as prerequisite; distillation/sparse attention/quantization; integrated efficiency |
| [[2602.01630\|WM Research Critical Assessment]] | 5-module unified framework | Fragmentation; need integrated module architecture; holistic understanding gap |
| [[2511.02097\|WM Manipulation Survey]] | Step-toward-WMs for manipulation | Structured task-relevant representations; hierarchical architectures for long-horizon |
| [[2510.24795\|Efficient VLA Survey]] | First efficient-VLA survey; three-pillar taxonomy | Latency/control freq incompatible w/ edge; pre-training cost; data collection; embodiment-agnostic; self-sustaining data |
| [[2510.16732\|World Models for Embodied AI Survey]] | Three-axis taxonomy (Functionality × Temporal × Spatial) | Unified datasets; physically-consistent metrics beyond FID/FVD; long-horizon temporal consistency; SSM/hybrid AR-global; WM × LLM-CoT synergy |
| [[2510.07077\|VLA Robotics Review 2025]] | Full-stack VLA review | Embodiment transfer; data scarcity; computational cost; eval+safety; gradient insulation/PEFT/inference optimization |
| [[2510.04978\|Physical AI Survey]] | Hierarchical physics-aware AI taxonomy | Causal understanding missing; compositional/causal structure; hybrid Neural Physics |
| [[2509.20021\|Embodied AI LLM-WM Survey]] | Joint MLLM + WM roadmap | MLLM-WM unified architecture; integration patterns |
| [[2509.19012\|Pure VLA Survey]] | 5-paradigm action generation | Data scarcity; architectural heterogeneity; real-time inference; eval fragmentation; world modeling + causal reasoning |
| [[2508.13073\|VLA Survey 2025]] | VLA landscape | Partially superseded by later 2025 reviews |
| [[2508.07407\|Self-Evolving AI Agents Survey]] | Unified self-evolution framework | Continuous self-improvement w/o forgetting; evolution-evaluation gap; safety + alignment under self-modification |
| [[2507.21046\|Self-Evolving Agents Survey]] | What/When/How/Where to Evolve | Adaptivity / retention / generalization / efficiency / safety as 5 eval gaps; emergent risks |
| [[2507.21045\|4D Spatial Intelligence Survey]] | 5-level hierarchical taxonomy | Cross-level eval; physics-aware 4D reconstruction; interactive 4D editing |
| [[2507.10672\|VLA Manipulation Survey]] | 102 models + 26 datasets + 12 simulators | Multimodal × high-complexity data gap; simulator fidelity-vs-throughput; native language-grounding APIs |
| [[2507.00917\|Embodied Intelligence Survey]] | IR-L0/L4 grading + simulators × WMs | Sim2Real gap; unified capability framework; WMs as neural simulators |
| [[2506.20966\|VLA Post-Training Survey]] | RL/SFT post-training | Generalization-vs-precision; knowledge insulation during RL |
| [[2506.20134\|3D World Models Survey]] | 2D → 3D WMs | 3D spatial understanding under-developed |
| [[2505.07634\|Neural Brain Framework]] | 4-component neuro-inspired | Multimodal active sensing; closed-loop perception-cognition-action; neuroplasticity memory; neuromorphic co-design |
| [[2505.05108\|Multi-agent Embodied AI Survey]] | First systematic multi-agent EAI | Async decisions; heterogeneous teams; self-evolution in open environments; nascent benchmarks |
| [[2505.04769\|VLA Survey]] | 80+ models across 6 domains | Real-time inference (AR 3–5 Hz); safety (~82% collision); generalization gap (~40%); dual-system + LoRA |
| [[2504.21853\|Interactive Generative Video Survey]] | 5-module IGV decomposition | Real-time vs quality; persistent memory; dynamics fidelity; cross-domain transferability |
| [[2504.01990\|Foundation Agents Survey]] | Brain-inspired agent framework | Autonomous + adaptive + safe agents; AI-cognition mapping; collaboration |
| [[2503.21765\|Physics Cognition Survey]] | Basic / Passive / Active cognitive tiers | Sub-human physics (multi-object/fluid); limited physical coverage; computational inefficiency; sim2real; physics foundation + neuro-symbolic |
| [[2503.04641\|Multimodal Generative World Simulators Survey]] | 2D → 4D unified framework | Cross-modal dependency; sparse 4D integration; comprehensive simulators |
| [[2602.04411\|Self-evolving Embodied AI]] | 5 co-evolving modules | "Human-crafted settings" limit; multi-timescale closed-loop co-evolution; integration of WM/memory/embodiment |
| [[2601.15533\|Actionable Simulators]] | Actionable WMs; 4 imperatives | Dynamical hallucinations; structured 4D interfaces; self-evolution; closed-loop decision-oriented eval |
| [[2601.07823\|Video Generation in Robotics Survey]] | Video gen as embodied WM; 10 challenges | Hallucinations + physics violations; uncertainty; long videos; compute; robotics-centric benchmarks |
| [[2501.10928\|Generative Physical AI Survey]] | 6-paradigm physics-aware gen | Functional vs visual realism; physical plausibility metrics; material fidelity |
| [[2512.24385\|Spatial Intelligence Pre-training Roadmap]] | Multi-modal pre-training roadmap | Single → unified pre-training; 3D data scarcity; generative WM × spatial reasoning |
| [[2504.09848\|LLM Spatial Intelligence Survey]] | Cross-scale spatial framework | Fragmented research; unsystematized LLM cognitive foundations; deployment limits |
| [[2504.15037\|MLLM Spatial Reasoning Position Paper]] | Position paper | Scaling won't fix spatial gaps; data/architecture/objective/eval limits; spatial-specific recipes |
| [[2509.25373\|VLM Perception-Cognition Survey]] | Perception → Cognition framework | Shallow perception-cognition integration; pixel-to-world-model translation; hallucination from disjoint coupling |
| [[2411.14499\|World Models Survey 2024]] | Implicit vs future-prediction across games/robotics/AD/social | Physical-rule adherence; standardized benchmarks; sim2real; ethics/safety; interactive 3D action-conditioned WMs |
| [[2407.06886\|ARIO]] | Comprehensive EAI survey + dataset | Sim2Real gap; data heterogeneity; MLM + WM integration |
| [[2404.14387\|LLM Self-Evolution Survey]] | 4-phase iterative cycle | Lifelong-learning forgetting; self-generated experience quality; alignment under self-evolution |
| [[2311.00530\|LLM Embodied Navigation Survey]] | LLM-in-navigation taxonomy | Long-horizon planning grounding; context-window limits; multimodal grounding |
| [[2310.06253\|Objective-Mismatch Survey]] | MBRL objective-mismatch survey | Decision-aware MBRL; predictive-loss vs return alignment; cross-family fragmentation |
| [[2103.04918\|Embodied AI Simulators Survey]] | 9 simulators × 7 features × 3 tasks | Simulator-task interconnections; realistic-physics + interactive-objects; cross-simulator benchmarking |

> [!tip] Convergence patterns
> - **Joint WM-action evaluation gap** (5-way): [[2605.12090|WAM Survey]], [[2605.00080|WM Robot Learning Survey]], [[2510.16732|World Models for Embodied AI Survey]], [[2601.15533|Actionable Simulators]], [[2601.07823|Video Generation in Robotics Survey]] — same diagnosis under different vocabulary (causal consistency / closed-loop / physically-consistent metrics).
> - **Physical grounding / dynamical hallucinations** (5-way): [[2503.21765|Physics Cognition Survey]], [[2510.04978|Physical AI Survey]], [[2601.15533|Actionable Simulators]], [[2411.14499|World Models Survey]], [[2501.10928|Generative Physical AI Survey]] — converge on hybrid neural-symbolic + verifiable-physics.
> - **Data scarcity** (6-way): [[2604.15395|Foundation Models in Robotics Survey]], [[2604.27621|Robot Learning from Human Videos Survey]], [[2509.19012|Pure VLA Survey]], [[2507.10672|VLA Manipulation Survey]], [[2407.06886|ARIO]], [[2512.24385|Spatial Intelligence Pre-training Roadmap]] — internet-scale human video + massively-parallel sim + self-exploration as dominant scaling levers.
> - **Efficiency as prerequisite** (3-way): [[2510.24795|Efficient VLA Survey]], [[2603.28489|Video Gen as WM Survey]], [[2604.15911|Efficient Video Diffusion Survey]] — KV-cache movement is the major DiT bottleneck; [[2505.04769|VLA Concepts Survey]]'s 3–5 Hz AR ceiling is the quantitative anchor.
> - **Self-evolution / autonomous adaptation** (6-way): [[2602.04411|Self-evolving Embodied AI]], [[2604.16592|Cognition WM Survey]], [[2604.22748|Agentic World Modeling Survey]], [[2508.07407|Self-Evolving AI Agents Survey]], [[2507.21046|Self-Evolving Agents Survey]], [[2404.14387|LLM Self-Evolution Survey]] — meta-cognition / autonomous self-revision is the missing function.
> - **Definition fragmentation** (meta): [[2604.04707|OpenWorldLib]], [[2510.16732|World Models for Embodied AI Survey]], [[2411.14499|World Models Survey]], [[2602.01630|WM Research Critical Assessment]] — field still pre-paradigmatic; empirical convergence outpaces terminology.

---

## Cluster I — Foundations: Data, Sensors, Substrates

### Direction 1 — Tactile-Egocentric Pretraining: From Hand Video Alone to Force-Aware VLA

**Thesis.** Train a VLA's force-aware components using *only* egocentric human hand video — no force sensors in the loop — by exploiting vision-to-tactile prediction + the EgoScale log-linear scaling law.

#### Why it matters

[[2505.22159|ForceVLA]]'s 244-trajectory dataset is 4 orders of magnitude smaller than [[2310.08864|OXE]] ([[2604.15395|Foundation Models in Robotics Survey]]'s named bottleneck). [[2602.16710|EgoScale]] shows a 20,854-hour log-linear curve up to **+54%** on 22-DoF dexterous hands; [[2603.15257|HapticVLA]] proves tactile-awareness can be transferred *without* inference-time sensors via distillation. [[2510.24795|Efficient VLA Survey]] explicitly names internet-scale human video as one of three dominant data-collection levers.

#### Current state of evidence

- [[2605.13083|TouchAnything]] — First multi-view ego + bimanual dense tactile dataset (20 hr); view dropout cuts ego-only drop from **−27.20% → −5.78%**.
- [[2603.15257|HapticVLA]] — Teacher-student distillation; **86.7%** SR on fragile-object; **+45 pp** on egg manipulation over SmolVLA.
- [[2601.20321|TaF-VLA]] — 10M tactile-force pairs + VQ-VAE latent; **60.3%** cross-sensor zero-shot.
- [[2410.24090|Sparsh]] / [[2506.14754|Sparsh-X]] — SSL touch foundation (460k–1M unlabeled), **>500%** plug-insertion gain.
- [[2507.15597|Being-H0]] / [[2605.00078|Being-H0.7]] — Full VLA pretraining on UniHand (150M instruction-motion pairs).

Gap: no paper trains a force-aware VLA from egocentric video *alone* (zero force sensors at any stage). HapticVLA distills from tactile teacher; TouchAnything uses tactile as supervision.

#### Concrete sub-problems

1. **Vision-to-tactile prediction at scale.** Extend TouchAnything's view-dropout to EgoScale volume (~20k hr); generate synthetic tactile via Sparsh-X teacher on small tactile-instrumented fraction.
2. **Force-aware MoE consuming *predicted* tactile.** Predict tactile from vision; feed prediction into [[2505.22159|ForceVLA]]-style FVLMoE. Compare against same architecture with real tactile.
3. **Compositional pretraining mixture.** Ablate egocentric video ([[2110.07058|Ego4D]] + UniHand + [[2505.11709|EgoDex]]) + force-conditioned video ([[2505.19386|Force Prompting]]) + small tactile-instrumented set.
4. **Cross-embodiment force transfer.** Human hand → gripper. Compare explicit ([[2507.15597|Being-H0]] MANO + GRQ-VAE), keypoint ([[2512.22414|π0.5 + ego]]), and learned projections.
5. **Contact-rich benchmark suite.** Re-run [[2505.22159|ForceVLA]] + [[2603.15169|ForceVLA2]] sets with ego-only pretrained policies.

#### Related papers

- [[2605.13083|TouchAnything]], [[2603.15257|HapticVLA]], [[2601.20321|TaF-VLA]], [[2506.14754|Sparsh-X]], [[2602.16710|EgoScale]], [[2605.00078|Being-H0.7]], [[2505.19386|Force Prompting]], [[2507.15597|Being-H0]], [[2512.22414|π0.5 + ego]]

#### Benchmark coverage

**Existing**: TacBench, ForceVLA-Data (244 traj), [[2510.25725|HumanoidVTA]]. **Gap**: no benchmark isolates "ego-only policy vs real-tactile policy" on ForceVLA's 5 contact-rich tasks.

#### Risk

- **Vision-to-tactile noise floor**: subtle slip needs fingertip pressure, not vision — policy may plateau.
- **Scaling cost**: 20k+ hr ego data is expensive; tactile labels scarcer.
- **Embodiment mismatch**: 22-DoF human vs 1–7-DoF grippers leaves an action-space gap.

### Direction 2 — Cross-Sensor Tactile Foundation Models for Plug-And-Play Force-Aware VLAs

**Thesis.** Build the [[2304.07193|DINOv2]] analog for tactile — a *cross-sensor* SSL representation enabling force-aware VLAs trained on one sensor type ([[2509.18830|DexSkin]]) to transfer to another ([[2604.28156|FlexiTac]], [[2604.20689|FingerEye]]) without re-collection.

#### Why it matters

[[2604.15395|Foundation Models in Robotics Survey]] flags tactile scarcity as top-3 bottleneck; [[2604.27621|Robot Learning from Human Videos Survey]] names tactile incorporation as one of 7 open problems; [[2604.16592|Cognition WM Survey]] (alphaxiv-verified) names tactile-perception as under-represented. Architecturally converged ([[2603.15169|ForceVLA2]] reaches 66% avg SR, +48 pp over π0) but every new platform restarts data collection. [[2410.24090|Sparsh]] / [[2506.14754|Sparsh-X]] train *per-sensor*; [[2601.20321|TaF-VLA]]'s 60.3% cross-sensor SR is not deployment-ready.

#### Current state of evidence

- **Sensors**: [[2509.18830|DexSkin]] (capacitive, 294° coverage), [[2604.28156|FlexiTac]] ($30 piezoresistive), [[2604.20689|FingerEye]] (vision-tactile fingertip), GelSight/DIGIT
- **SSL foundations**: [[2410.24090|Sparsh]] (460k images, MAE/DINO/JEPA), [[2506.14754|Sparsh-X]] (1M contacts, multisensory)
- **Cross-sensor work**: [[2601.20321|TaF-VLA]] (VQ-VAE; **60.3%** zero-shot), [[2509.18830|DexSkin]] (pneumatic calibration)
- **Alignment**: [[2605.14571|MTNet]] (visuo-tactile, CKA ~0.74)
- **Sensor-free deploy**: [[2603.15257|HapticVLA]] (distillation; **86.7%** SR)

Gap: no SSL encoder achieves >80% cross-sensor zero-shot SR.

#### Concrete sub-problems

1. **Sensor-invariant SSL objective.** Extend Sparsh-X attention-bottleneck to *cross-sensor* fusion — mask one sensor, predict from another (DINOv2-style EMA teacher).
2. **Force-as-bridge grounding.** Extend [[2601.20321|TaF-VLA]]'s VQ-VAE alignment across *all* sensor types, not just families.
3. **Cross-sensor benchmark.** Train on N−1 sensors, evaluate held-out across [[2410.24090|Sparsh]] TacBench. Target >80% in-dist retention.
4. **Cross-sensor VLA fine-tuning.** Bolt encoder onto [[2603.15169|ForceVLA2]] Cross-Scale MoE.
5. **Deployment chain validation.** Train one sensor → deploy another; [[2604.28156|FlexiTac]] Kelvin-Voigt sim-to-real protocol as reference.

#### Related papers

- [[2410.24090|Sparsh]] / [[2506.14754|Sparsh-X]], [[2601.20321|TaF-VLA]], [[2509.18830|DexSkin]], [[2604.28156|FlexiTac]], [[2604.20689|FingerEye]], [[2603.15169|ForceVLA2]], [[2603.15257|HapticVLA]], [[2605.14571|MTNet]]

#### Benchmark coverage

**Existing**: TacBench, ForceVLA-Data, [[2510.25725|HumanoidVTA]]. **Gap**: no benchmark tests held-out-sensor zero-shot.

#### Risk

- **Fundamental sensor incompatibility**: capacitive vs piezoresistive vs vision-tactile may require discarding task-relevant detail to be invariant.
- **Recursive data problem**: SSL needs many sensors' data, but data is missing *because* transfer is the bottleneck.
- **60.3% ceiling**: visual-to-tactile bottleneck may be fundamental.

---

## Cluster II — Architecture & Training: How the Model Learns

### Direction 3 — Single-Loop Co-Evolving VLA + World Model in Latent Space

**Thesis.** Move beyond alternating co-improvement ([[2602.12063|VLAW]] pattern) to a unified single-step gradient where action and imagination losses jointly update both networks in the same optimizer step, in **latent space** for real-time feasibility.

#### Why it matters

[[2605.12090|WAM Survey]] (alphaxiv-verified) formally defines WAMs via $\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o,l,o',a)\sim\mathcal{D}}[-\log p(o', a \mid o, l)]$ and identifies Joint over Cascaded as the frontier; [[2605.00080|WM Robot Learning Survey]] corroborates "single-backbone, unified VLA, latent world-modeling."

Current "joint" implementations fall short: [[2602.12063|VLAW]] alternates; [[2603.16666|Fast-WAM]] drops the WM at deployment; [[2605.15153|Pelican-Unified]] unifies architecturally but trains multi-stage. Gap: a single GRPO loop on joint $(action, imagination)$ log-prob with cooperative gradient flow is undemonstrated.

#### Current state of evidence

- **Closest single-loop attempts**: [[2603.19370|VAMPO]] (GRPO over video-denoising-as-MDP; pixel-space, expensive), [[2602.13977|WoVR]] (masked GRPO + KIR + PACE; PACE not in code), [[2511.09515|WMPO]] (on-policy GRPO; WM frozen in inner loop), [[2511.15605|SRPO]] (frozen V-JEPA-2; WM doesn't update).
- **Latent feasibility** ([[03_VLA]] §5 + [[04_WAM]] §5): [[2602.10098|VLA-JEPA]], [[2602.11832|JEPA-VLA]], [[2605.00078|Being-H0.7]] predict in 256-dim latent (~10 ms) vs pixel ~150 ms.

#### Concrete sub-problems

1. **Unified GRPO in latent space.** Given pretrained latent WAM ([[2504.02792|UWM]] or [[2602.10098|VLA-JEPA]]), $\mathcal{L} = \mathbb{E}[A \cdot \log \pi(a, \hat{z}_{t+1} \mid s_t)]$; single backward updates both heads.
2. **Reward decomposition.** Task + latent-consistency ($\hat{z}_{t+1}$ vs encoder's $z_{t+1}$) + action-quality; latent provides the dense signal task reward cannot.
3. **Knowledge insulation in joint loops.** Extend [[2505.23705|Knowledge Insulation VLA]]'s stop-gradient from action expert→VLM to action→WM encoder; preserves pretrained physics priors.
4. **Failure-finder co-evolution.** [[2412.02818|RoboMD]]-style adversary modified to GRPO; selects perturbations in same optimizer step.
5. **Real-robot transfer**. Deploy only the policy (LoRA on frozen WM base) since WM + failure-finder remain sim-only.

#### Related papers

- [[2602.12063|VLAW]], [[2603.19370|VAMPO]], [[2511.09515|WMPO]], [[2511.15605|SRPO]], [[2605.15153|Pelican-Unified]] (93.5% RoboTwin), [[2605.10942|HarmoWAM]] (89% in-domain, −7.9% OOD), [[2602.10098|VLA-JEPA]] / [[2602.11832|JEPA-VLA]] / [[2605.00078|Being-H0.7]], [[2504.02792|UWM]], [[2505.23705|Knowledge Insulation VLA]]

#### Benchmark coverage

**Existing**: [[2306.03310|LIBERO]] + LIBERO-Plus + [[2602.06556|LIBERO-X]] + [[2603.28301|LIBERO-Para]]. **Gap**: no joint-vs-alternating ablation grid on a fixed backbone (UWM / Cosmos Policy).

#### Risk

- **Optimization instability**: discrete action + continuous latent + adversarial finder have conflicting gradients — careful balancing required.
- **Chasing problem**: simultaneous updates → WM models obsolete policy; EMA target networks mitigate.
- **Reward hacking on latent consistency**: gameable by collapsing the latent. [[2511.08544|LeJEPA]] Euclidean regularization defends; [[2604.27998|Latent-GRPO]] failure-mode patches relevant.

### Direction 4 — Causally-Important Step Rewards for Latent VLA Reasoning

**Thesis.** Combine [[2604.18486|OneVL]]-style latent reasoning (answer-only latency) with [[2604.22074|CIR/SR Reasoning]]-style step rewards (causally important reasoning) — closing the "outcome rewards alone don't guarantee causal reasoning" gap at training-time supervision cost only.

#### Why it matters

[[2604.22074|CIR/SR Reasoning]] finds outcome rewards insufficient — RL-trained traces become "factually correct via causally disconnected paths." [[2604.18486|OneVL]] shows latent reasoning beats explicit CoT at answer-only latency (**88.84** PDM-score, **+2.64 pts** over prior 8B). [[2510.16281|SEAL]] documents the CoT-faithfulness gap. [[2509.19012|Pure VLA Survey]] names causal reasoning alongside world modeling; [[2510.04978|Physical AI Survey]] generalizes to all of Physical AI.

#### Current state of evidence

- [[2604.18486|OneVL]] — Dual-decoder latent CoT; answer-only latency
- [[2604.22709|Abstract-CoT]] — Pre-allocated K reasoning tokens
- [[2604.28192|LaST-R1]] — Adaptive physical latent reasoning + RL
- [[2604.27998|Latent-GRPO]] — RL stabilization (3 failure-mode patches)
- [[2604.20328|HyLaR]] — vMF distribution + decoupled clipping
- [[2605.02735|Silenced Visual Latents]] — Diagnostic: latents can be "semantically rich but functionally ignored"
- [[2604.22074|CIR/SR Reasoning]] — Step-reward training for causal reasoning
- [[2509.25852|REVER]] — Verifiable reward RL planning
- [[2604.21396|VG-CoT]] — Visually-grounded CoT

Gap: no paper combines latent CoT + step-reward training for VLA reasoning.

#### Concrete sub-problems

1. **Causal-importance predicates for manipulation.** Decompose 130 [[2306.03310|LIBERO]] tasks into 3–7 verifiable subgoals (~600–900); auto-generate via [[2503.15558|Cosmos-Reason1]] LLM-as-judge, validate on 100-subgoal gold set (κ > 0.7). Deliverable: LIBERO-Subgoals + predicate code.
2. **Step-reward training on latent reasoning tokens.** Expose [[2604.18486|OneVL]]'s K=8 latent tokens; $\mathcal{L} = \lambda_a \mathcal{L}_{\text{action}} + \lambda_s \sum_i r_{\text{step},i}(z_i)$ with per-token subgoal predicates. Baselines: vanilla OneVL, OneVL + outcome-only RL, [[2503.22020|CoT-VLA]]. Target: ≥+5 pp SR on LIBERO-Long at matched latency.
3. **Latent utilization probing.** [[2605.02735|Silenced Visual Latents]]-style: define Latent Utilization Index (LUI) = action $L_2$ distance between $a(\mathbf{z})$ and $a(\mathbf{z}+\epsilon)$, normalized. Pass: LUI > 0.3.
4. **Compositional step rewards.** Train on simple instructions, test compositions ("open drawer + place red mug"). Benchmarks: [[2603.28301|LIBERO-Para]] + [[2510.13626|LIBERO-Plus]] + [[2507.10548|EmbRACE-3K]]. Target: ≥+10 pp on compositional, ≤−3 pp in-dist.
5. **Inference cost ablation.** Explicit CoT (~1.2s) vs Abstract-CoT (~50ms) vs OneVL (~0ms) vs OneVL+CIR/SR (~0ms) across {ID, OOD, Compositional}.

#### Related papers

- [[2604.18486|OneVL]], [[2604.22074|CIR/SR Reasoning]], [[2604.27998|Latent-GRPO]], [[2510.16281|SEAL]] (+15 pp compositional), [[2604.21396|VG-CoT]], [[2509.25852|REVER]], [[2605.02735|Silenced Visual Latents]], [[2503.15558|Cosmos-Reason1]]

#### Benchmark coverage

**Existing**: NAVSIM, LIBERO-Plus, LIBERO-Para, [[2507.10548|EmbRACE-3K]]. **Gap**: no benchmark tests causal faithfulness of latent reasoning to action sequences under compositional novelty.

#### Risk

- **Predicate scaling**: hand-authoring subgoals is brittle; LLM-as-judge fallback re-introduces verification cost CIR/SR avoids.
- **Reward hacking**: models can satisfy predicates trivially — [[2509.15194|EVOL-RL]] novelty diversity defends.
- **Compositional generalization unsolved**: SEAL documented this exact failure mode.

### Direction 5 — Verifiable Physics-Consistent Training for Open-World VLA Generation

**Thesis.** Bridge [[2604.04974|Video-to-Control Survey]]'s "robotics integration layer" gap by training VLAs with verifiable physics rewards at the *action* level — not only at the video-generation level.

#### Why it matters

5-way diagnosis: [[2604.04974|Video-to-Control Survey]] (physical feasibility as missing layer), [[2503.21765|Physics Cognition Survey]] (sub-human physics), [[2510.04978|Physical AI Survey]] ("causal understanding missing"), [[2601.15533|Actionable Simulators]] (*dynamical hallucinations*), [[2601.07823|Video Generation in Robotics Survey]] (hallucinations + physics violations as top-2). Physics-aware video generators ([[2509.21309|NewtonGen]], [[2510.13809|PhysMaster]], [[2512.00425|NewtonRewards]], [[2603.13770|PhysAlign]]) made progress on the *generation* side but the imagination → policy chain is untested. Closest: [[2604.17896|Physical-Feasibility VLA]] (geometric loss on actions; 22% → **43.50%** SSR — geometric only).

#### Current state of evidence

- **Video-side**: [[2509.20570|PIRF]], [[2509.21309|NewtonGen]], [[2512.00425|NewtonRewards]], [[2510.13809|PhysMaster]], [[2603.13770|PhysAlign]], [[2603.26285|PhysVid]]
- **VLA-side**: [[2604.17896|Physical-Feasibility VLA]], [[2503.15558|Cosmos-Reason1]], [[2511.07416|PhysWorld]], [[2605.06593|ReActor]]
- **Bridge**: [[2603.23376|ABot-PhysWorld]] (Diffusion-DPO with physics-rejected negatives)

#### Concrete sub-problems

1. **Physics predicates over action sequences.** Five binary verifiable predicates:
   - **P1 momentum**: $|\Delta p_{\text{total}}| < 0.05 \cdot p_{\max}$ over 1s (excluding contact)
   - **P2 no inter-object penetration**: signed-distance > 0 at every step
   - **P3 anti-gravity check**: free-flight $\Delta z \sim -\frac{1}{2}gt^2 \pm 10\%$
   - **P4 Newton's 3rd law on contact wrenches**
   - **P5 Coulomb friction**: $|F_t| \leq \mu |F_n|$
   Instrument 50 LIBERO + 30 [[2502.16707|RoboMamba]] long-horizon tasks; ~4,000 labeled trajectories.
2. **Implicit vs abstract vs explicit interface ablation** (per [[2604.04974|Video-to-Control Survey]] taxonomy). Same backbone, matched FLOPs; SSR on LIBERO-Plus + 20-task physics gauntlet. Target: implicit 43.50% → >55%; latent within ±2 pp at lower latency.
3. **Open-world test via [[2603.23376|ABot-PhysWorld]] negatives.** ~10k preference pairs; Diffusion-DPO. Pass: $\beta(\log p_\theta(a_+) - \log p_\theta(a_-)) > 0$ with ≥90% on 1k held-out (baseline ~74%).
4. **Sim-to-real chain.** [[2511.04665|Real-to-Sim GS]] soft-body twins (12 cloth/rope/dough); eval sim → twin → real. Target SR retention $\geq 0.70$ (physics-naive: 0.50–0.60).
5. **Reward-hacking diagnostics**: D1 static-output detection (σ drop > 2×); D2 $\rho(\sum P_i, \text{task SR})$ regression; D3 periodic [[2412.02818|RoboMD]] adversarial probing. Defense: [[2509.15194|EVOL-RL]] novelty diversity.

#### Related papers

- [[2604.04974|Video-to-Control Survey]], [[2604.17896|Physical-Feasibility VLA]], [[2603.23376|ABot-PhysWorld]], [[2509.21309|NewtonGen]] / [[2512.00425|NewtonRewards]] / [[2509.20570|PIRF]] / [[2510.13809|PhysMaster]] / [[2603.13770|PhysAlign]], [[2503.15558|Cosmos-Reason1]], [[2511.07416|PhysWorld]], [[2605.06593|ReActor]], [[2511.04665|Real-to-Sim GS]]

#### Benchmark coverage

**Existing**: [[2410.05363|PhyGenBench]], [[2503.06800|VideoPhy-2]], [[2501.09038|Physics-IQ]], [[2504.02918|Morpheus]] (all measure video physics). **Gap**: no benchmark scores physics-consistency of VLA action sequences against verifiable simulator.

#### Risk

- **Verifiable physics scales poorly** ([[2509.20570|PIRF]]) — predicates for cluttered scenes are hard.
- **Physics-consistent imagination ≠ physics-consistent action**: this is the gap to test; if small, direction collapses.
- **Reward hacking**: NewtonRewards documented it on generation side; action-side analog (model freezes) is likely.

---

## Cluster III — Evaluation, Robustness & Deployment

### Direction 6 — Joint VLA/WAM Evaluation: Causal Consistency Between Imagination and Action

**Thesis.** Build the first standardized benchmark suite that jointly measures whether a WAM's *imagined future* matches the *action it then takes* — closing the dominant evaluation gap (5-way survey convergence).

#### Why it matters

[[2605.12090|WAM Survey]], [[2605.00080|WM Robot Learning Survey]], [[2510.16732|World Models for Embodied AI Survey]], [[2601.15533|Actionable Simulators]], [[2601.07823|Video Generation in Robotics Survey]] independently call out that current protocols measure WM quality (FVD/PSNR) and action quality (LIBERO SR) **separately** — a WAM can score high on each while imagination and actions are causally disconnected. [[2310.06253|Objective-Mismatch Survey]] provides the MBRL substrate: predictive WM loss fails to correlate with downstream return. [[2603.22078|WAM vs VLA Robustness]] showed WAMs win on visual perturbations *but are 4.8× slower* — the cost is only worth paying if imagination helps action quality, which current metrics cannot certify.

#### Current state of evidence

- [[2603.22212|Omni-WorldBench]] — First interaction-centric WM eval via counterfactual probes (WM-only)
- [[2506.00613|WorldGym]] — Policies trained inside WM (closer to joint, game-style)
- [[2510.10125|CTRL-WORLD]] — Controllability eval for manipulation
- [[2603.23497|WildWorld]] — Action Following + State Alignment on 108M Monster Hunter frames
- [[2510.16281|SEAL]] — Runtime verifier (not benchmark)

#### Concrete sub-problems

1. **Causal-consistency metric.** Given $(s_t, a_t) \to \hat{s}_{t+1}, s_{t+1}$, [[2304.07193|DINOv2]] (ViT-L/14) cosine plus counterfactual probe — sample $a'_t$, generate $\hat{s}'_{t+1}$, require $\|\hat{s}_{t+1} - \hat{s}'_{t+1}\|$ to scale monotonically with $\|a_t - a'_t\|$. Reference on [[2603.13966|vla-eval]].
2. **50–100 task diagnostic suite.** Layer on [[2306.03310|LIBERO]] (130 tasks) + [[2510.13626|LIBERO-Plus]] (10,030 perturbations) + [[2603.28301|LIBERO-Para]]; record (predicted, achieved, action) at every step. Scale: ~40k pairs per WAM.
3. **L1/L2/L3 sub-scores per [[2604.22748|Agentic World Modeling Survey]]**: L1 = 1-step MSE (>90% [[2510.10125|CTRL-WORLD]] controllability); L2 = 8-step drift (<2× linear); L3 = COD as AUROC of swapped-action detection (0.5 = chance, 1.0 = perfect). Pair with ASR.
4. **Speed-quality Pareto.** Re-run [[2603.22078|WAM vs VLA Robustness]] ~12-config grid with joint metric. Does the 4.8× cost translate to ≥X pp on L3?
5. **Deployment-readiness axis.** Cross-reference [[2506.18123|RoboArena]] (8 platforms, ~120 tasks). Does joint metric predict real SR at Spearman ρ > 0.7? Current separate sub-scores: ρ < 0.4.

#### Related papers

- [[2603.22212|Omni-WorldBench]], [[2506.00613|WorldGym]], [[2510.10125|CTRL-WORLD]], [[2603.22078|WAM vs VLA Robustness]], [[2510.16281|SEAL]], [[2603.13966|vla-eval]]

#### Benchmark coverage

**Existing**: LIBERO + LIBERO-Plus, Omni-WorldBench + WildWorld (WM-only), WorldGym, [[2506.18123|RoboArena]]. **Gap**: no benchmark scores joint(WM_quality, action_quality, causal_consistency) on a single suite.

#### Risk

- **Metric noise**: feature-space similarity embeds blind spots; pair with explicit physical predicates.
- **Sample size**: counterfactual probes may need 100+ rollouts per task instance.
- **Selection bias**: benchmark may flatter current WAMs; include adversarial ([[2604.05498|JailWAM]]) + physics-violating ([[2603.23376|ABot-PhysWorld]] rejects) baselines.

### Direction 7 — Long-Horizon Memory + Failure Recovery Loops for Real-World Deployment

**Thesis.** Combine long-horizon memory architectures ([[2605.10993|ECHO-VLA]], [[2508.19236|MemoryVLA]], [[2603.03596|MEM]]) with proactive failure-recovery ([[2601.02295|CycleVLA]], [[2512.24426|CF-VLA]], [[2509.04018|FPC-VLA]]) into a unified deployment loop.

#### Why it matters

[[2605.10921|RoboMemArena]]: **68.9%** of subtasks need historical info. [[2604.16592|Cognition WM Survey]] (alphaxiv-verified) names *meta-cognition* as one of two drastically under-researched cognitive functions — failure detection + recovery is the embodied operationalization. [[2602.04411|Self-evolving Embodied AI]] (5-module framework) and [[2505.05108|Multi-agent Embodied AI Survey]] (open-environment self-evolution as top unresolved) decompose it further. Recovery requires memory — [[2605.10993|ECHO-VLA]] (**+12.8 pp** LIBERO-Long) is closest but no detection integration.

#### Current state of evidence

**Memory**: [[2605.10993|ECHO-VLA]] (+12.8 pp), [[2508.19236|MemoryVLA]] (+26 pp temporal, +3.6% latency), [[2603.03596|MEM]] (15-min memory), [[2603.12942|ReMem-VLA]] (94.5% on memory-dependent sim).

**Detection** (8 methods per [[06_Self-Evolving-VLA-WAM]] §4.1): [[2506.09937|SAFE]], [[2509.16072|I-FailSense]], [[2510.09459|FIPER]], [[2603.11106|RC-NF]] (<100 ms), [[2503.08558|FAIL-Detect]] (78% w/o failure data), [[2410.04640|Sentinel]] (+18% over single), [[2407.08735|AESOP]] (100% sim recovery), [[2510.02298|ARMADA]] (95% accuracy, 23.3% intervention reduction).

**Proactive correction**: [[2601.02295|CycleVLA]], [[2512.24426|CF-VLA]], [[2604.02965|SV-VLA]], [[2511.14148|AsyncVLA]], [[2509.04018|FPC-VLA]].

**Recovery**: [[2505.12224|RoboFAC]], [[2603.13528|Counterfactual Failure Synthesis]].

Gap: no paper integrates memory + detection + correction + recovery into a single loop on a long-horizon real benchmark.

#### Concrete sub-problems

1. **Memory-grounded failure detection.** Use ECHO-VLA / MemoryVLA hierarchical memory to detect history-dependent failures ("tried this 3× already").
2. **Recovery with memory.** When CycleVLA backtracks, consult memory — memory bank as *failure exclusion buffer*.
3. **Real-world deployment loop stack**: (a) memory (PCMB / hyperbolic), (b) parallel detectors ([[2410.04640|Sentinel]] pattern), (c) corrective head (CycleVLA + CF-VLA), (d) recovery generator ([[2603.13528|Counterfactual Failure Synthesis]]).
4. **Compute-vs-robustness trade-off**. Ablation on [[2605.10921|RoboMemArena]] + LIBERO-Plus + real-robot [[2506.18123|RoboArena]]; identify deployable combinations.
5. **Continual update from corrections.** Each successful recovery → training example; [[2510.02298|ARMADA]] pooled-intervention pattern.

#### Related papers

- [[2605.10921|RoboMemArena]], [[2605.10993|ECHO-VLA]], [[2508.19236|MemoryVLA]], [[2510.09459|FIPER]] / [[2506.09937|SAFE]] / [[2410.04640|Sentinel]] / [[2603.11106|RC-NF]], [[2601.02295|CycleVLA]] / [[2512.24426|CF-VLA]] / [[2509.04018|FPC-VLA]], [[2505.12224|RoboFAC]] / [[2603.13528|Counterfactual Failure Synthesis]], [[2510.02298|ARMADA]]

#### Benchmark coverage

**Existing**: [[2605.10921|RoboMemArena]], LIBERO-Plus / -PRO, [[2506.18123|RoboArena]], [[2502.09560|EmbodiedBench]]. **Gap**: no benchmark scores integrated detect-diagnose-recover loops on long-horizon tasks.

#### Risk

- **Latency stacking**: each component adds 10–100 ms; full loop may not be real-time. Parallelize detectors; invoke recovery only on firing.
- **Component oscillation**: detectors may fire on each other's corrections — need state-machine design.
- **Memory irrelevant for short tasks**: sub-30-second deployment doesn't benefit; this is a long-horizon bet.

### Direction 8 — Real-Time-Deployable VLAs via Architectural-Algorithmic-Data Co-design

**Thesis.** Treat efficiency as a primary research target — build VLAs hitting ≥30 Hz control on edge by co-designing architecture (linear-attn / Mamba / parallel decoding) × training (PEFT + KD + co-training) × data (massive-parallel sim + internet ego video + self-exploration).

#### Why it matters

[[2510.24795|Efficient VLA Survey]] and [[2603.28489|Video Gen as WM Survey]] reframe efficiency from "optimization" to "fundamental prerequisite." [[2505.04769|VLA Concepts Survey]] quantifies: AR decoding limits speed to 3–5 Hz vs 20–50 Hz needed. [[2510.07077|VLA Robotics Real-World Review]] names latency as top-3 deployment concern. None of D1–D7 tackle efficiency as primary thesis — they implicitly assume real-time is feasible.

#### Current state of evidence

- **Model-side**: SARA-RT, [[2502.16707|RoboMamba]] (linear-time / Mamba), parallel action decoding, quantization + pruning + distillation (rarely co-optimized).
- **Training-side**: [[2505.23705|Knowledge Insulation VLA]] (stop-gradient PEFT), LoRA across OpenVLA/π0 lineage, mixed data co-training.
- **Data-side**: [[2602.16710|EgoScale]] (+54% dexterous; log-linear ego scaling), Isaac/Genesis parallel sim, self-exploration via [[2602.04411|Self-evolving Embodied AI]] env-self-prediction.

Gap: no paper co-designs across all three pillars; unified efficiency budget ("30 Hz on Jetson Orin given $B compute + $D data") not published.

#### Concrete sub-problems

1. **Pareto frontier sweep**: backbone (Transformer / linear-attn / Mamba) × decoding (AR / parallel / diffusion) × precision (FP16 / INT8 / INT4) on LIBERO + 1 real task. Is 30 Hz on edge reachable without unacceptable SR loss?
2. **Knowledge-insulated RL on efficient backbones.** Mamba VLA + [[2505.23705|Knowledge Insulation VLA]] stop-gradient on LIBERO-Plus.
3. **Data-efficient pretraining via ego co-training.** Combine [[2602.16710|EgoScale]] with [[2510.24795|Efficient VLA Survey]]'s mixed-data recipe; measure robot-data needed to match a 10×-data baseline.
4. **Real-time joint VLA+WM in latent space.** D3's joint loop with Mamba latent WM ([[2511.15605|SRPO]] V-JEPA-2 substrate) should run >30 Hz.
5. **Edge deployment chain**: train → quantize → distill → deploy on Jetson Orin / Apple M; measure SR retention at each stage.

#### Related papers

- [[2510.24795|Efficient VLA Survey]], [[2603.28489|Video Gen as WM Survey]], [[2505.04769|VLA Concepts Survey]], [[2510.07077|VLA Robotics Real-World Review]], [[2502.16707|RoboMamba]], [[2505.23705|Knowledge Insulation VLA]], [[2602.16710|EgoScale]], [[2511.15605|SRPO]], [[2603.16666|Fast-WAM]], [[2507.00917|Embodied Intelligence Survey]]

#### Benchmark coverage

**Existing**: LIBERO (SR no latency), [[2603.13966|vla-eval]] (47× training speedup), [[2502.09560|EmbodiedBench]]. **Gap**: no benchmark scores SR × control freq × edge-compute as joint Pareto.

#### Risk

- **Linear-attn / Mamba may underperform Transformers on long-context VLA** — gain only matters if SR holds.
- **Edge-hardware diversity**: Jetson vs Apple M vs custom NPUs need per-platform tuning.
- **Quantization-aware joint loops uncharted** — may break latent-consistency reward.
- **Saturation risk**: if "Mamba + LoRA + co-training" becomes dominant recipe, contribution shrinks to engineering; focus on Pareto and system-level insights.

---

## Cross-Cutting Themes

1. **Latent-space prediction beats pixel-space** — D3, D4, D6, D7, D8. Consensus: video at training, latent at deployment ([[2603.16666|Fast-WAM]]); bet on JEPA / DiT-on-latent.
2. **Step-level verifiable rewards** — D4, D5, D7. [[2604.22074|CIR/SR Reasoning]]'s "outcome rewards don't guarantee causal reasoning" is the most actionable 2026 result.
3. **Egocentric pretraining as dominant data substrate** — D1, D7 (memory from human video), D8 (data efficiency). [[2602.16710|EgoScale]] log-linear law is the first predictable axis.
4. **Detection-diagnosis-recovery as unified stack** — D7 explicitly; D3 (failure-finder), D4 (CoT faithfulness), D5 (physics violation) implicitly. [[2602.04411|Self-evolving Embodied AI]]'s 5-module framework formalizes this.
5. **Force/tactile as first-class modality with dedicated experts** — D1, D2. [[2505.22159|ForceVLA]] / [[2603.15169|ForceVLA2]] / [[2603.15257|HapticVLA]] established the architecture; data + cross-sensor transfer remain.
6. **Efficiency as prerequisite, not optimization** — D8 explicitly; D3, D6, D7 implicitly. [[2505.04769|VLA Concepts Survey]] 3–5 Hz ceiling is the quantitative anchor.

---

## Benchmark Gaps (Consolidated)

| Gap | Direction | Existing closest |
|---|---|---|
| Joint WM-action causal-consistency metric on manipulation | 6 | [[2603.22212\|Omni-WorldBench]] (WM-only) + [[2603.22078\|WAM vs VLA Robustness]] (separate axes) |
| Joint-vs-alternating co-training ablation on fixed backbone | 3 | None |
| Egocentric-only force-aware VLA evaluation | 1 | [[2505.22159\|ForceVLA]] 5-task set (uses real tactile) |
| Causal faithfulness of latent reasoning under compositional novelty | 4 | NAVSIM (driving CoT) + [[2510.16281\|SEAL]] (runtime) |
| Physics-consistency of VLA action sequences | 5 | [[2410.05363\|PhyGenBench]] (video) + [[2604.17896\|Physical-Feasibility VLA]] (geometric only) |
| Cross-sensor tactile zero-shot transfer | 2 | TacBench (per-sensor) + [[2601.20321\|TaF-VLA]] (60.3%) |
| Integrated detect-diagnose-recover loops on long-horizon real tasks | 7 | [[2605.10921\|RoboMemArena]] (memory) + [[2506.18123\|RoboArena]] (no recovery stack) |
| VLA SR × control freq × edge-compute Pareto | 8 | [[2306.03310\|LIBERO]] (SR only) + [[2603.13966\|vla-eval]] (training speedup) |

---

## Cross-References

- [[../Embodied-AI/03_VLA]] — VLA design space
- [[../Embodied-AI/04_WAM]] — WAM taxonomy (VideoGen / latent / Dreamer / VLM-integrated / efficient / self-evolving)
- [[../Embodied-AI/05_Latent-World-Models]] — JEPA evolution + alternative latents
- [[../Embodied-AI/06_Self-Evolving-VLA-WAM]] — Failure detection, diagnosis, recovery
- [[../Embodied-AI/07_Physics-Aware-Embodied-AI]] — Physics-aware design space
- [[../Embodied-AI/08_VLA-Reasoning-and-CoT]] — Reasoning insertion slots
- [[../Embodied-AI/09_Egocentric-Pretraining-and-Human-Video]] — Egocentric scaling + transfer
- [[../Embodied-AI/10_Force-Aware-and-Tactile-Policies]] — Force-aware architectures + tactile sensors
- [[../Embodied-AI/02_Dataset-Benchmark-Environment]] — Data + sim + benchmark stacks
- [[../General/08_Benchmarks-and-Surveys]] — Canonical survey index
