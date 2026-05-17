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
> Synthesized from 54 surveys spanning VLA, WAM, embodied AI, latent-space methodology, physics-aware video generation, efficient video diffusion, embodied-AI privacy, embodied navigation, spatial intelligence, self-evolving agents (LLM + embodied), foundation agents, and physical world simulation, plus 10 curated topic notes across `Embodied-AI/`, drawing on ~3,000 papers in the vault's `_KnowledgeHub_/`. The goal is a planning artifact: **8 directions organized into 3 thematic clusters (Foundations / Architecture & Training / Evaluation, Robustness & Deployment)**, each actionable enough that a PhD student could pick one and start within a week. The survey enumeration was extended through four audit passes — from an initial canonical-index sweep (34) to a comprehensive `_KnowledgeHub_/` tag-scan (47), then an adjacent-survey sweep (50), a duplicate-row dedup, and a finalization audit (final count 54 unique surveys) — with content verified against alphaxiv overview reports for 11 central surveys driving each direction (WAM Survey, WM Robot Survey 2026, World Models for Embodied AI Survey, Actionable Simulators, Video Generation in Robotics Survey, Agentic World Modeling Survey, Cognition WM Survey, Self-evolving Embodied AI, Physics Cognition Survey, Foundation Models in Robotics Survey, and Robot Learning from Human Videos Survey).

---

## TOC

1. [Methodology](#methodology-how-this-synthesis-was-built)
2. [Cluster Overview](#cluster-overview)
3. [Survey landscape](#survey-landscape)
4. **[Cluster I — Foundations: Data, Sensors, Substrates](#cluster-i--foundations-data-sensors-substrates)**
   - [Direction 1 — Tactile-Egocentric Pretraining](#direction-1--tactile-egocentric-pretraining-from-hand-video-alone-to-force-aware-vla)
   - [Direction 2 — Cross-Sensor Tactile Foundation Models](#direction-2--cross-sensor-tactile-foundation-models-for-plug-and-play-force-aware-vlas)
5. **[Cluster II — Architecture & Training](#cluster-ii--architecture--training-how-the-model-learns)**
   - [Direction 3 — Single-Loop Co-Evolving VLA + WM in Latent Space](#direction-3--single-loop-co-evolving-vla--world-model-in-latent-space)
   - [Direction 4 — Causally-Important Step Rewards for Latent Reasoning](#direction-4--causally-important-step-rewards-for-latent-vla-reasoning)
   - [Direction 5 — Verifiable Physics-Consistent Training](#direction-5--verifiable-physics-consistent-training-for-open-world-vla-generation)
6. **[Cluster III — Evaluation, Robustness & Deployment](#cluster-iii--evaluation-robustness--deployment)**
   - [Direction 6 — Joint VLA/WAM Evaluation](#direction-6--joint-vlawam-evaluation-causal-consistency-between-imagination-and-action)
   - [Direction 7 — Long-Horizon Memory + Failure Recovery](#direction-7--long-horizon-memory--failure-recovery-loops-for-real-world-deployment)
   - [Direction 8 — Real-Time-Deployable VLAs](#direction-8--real-time-deployable-vlas-via-architectural-algorithmic-data-co-design)
7. [Cross-cutting themes](#cross-cutting-themes)
8. [Benchmark gaps (consolidated)](#benchmark-gaps-consolidated)

---

## Methodology (how this synthesis was built)

1. **Enumerated surveys** — Exhaustively scanned the canonical survey index [[08_Benchmarks-and-Surveys#4. Robotics & Embodied AI Surveys|§4 — Robotics & Embodied AI Surveys]] (specifically the *VLA & World Model Architectures* subsection), [[08_Benchmarks-and-Surveys#5. Self-Evolving AI Surveys|§5 — Self-Evolving AI Surveys]], and [[08_Benchmarks-and-Surveys#7. Specialized Domain Surveys|§7 — Specialized Domain Surveys]] (specifically the *Physics-Cognition for Generation Surveys* subsection). Cross-referenced against the reference sections of [[03_VLA]], [[04_WAM]], and [[07_Physics-Aware-Embodied-AI]]. Then grep-filtered `_KnowledgeHub_/` for *all* `tags: - survey` files matching VLA/WAM/embodied/robot/physics/self-evolving keywords and ran an exhaustive sweep to catch adjacent surveys (latent-space methodology, efficient video diffusion, embodied-AI privacy, visual-generation taxonomy, embodied navigation, foundation agents, self-evolving LLM agents, interactive generative video, spatial intelligence, world-model meta-assessment, MLLM spatial reasoning, perception-cognition VLM) that the canonical index missed. The final enumeration covers 54 unique surveys after a finalization audit added LLM-Spatial-Intelligence, MLLM-Spatial-Reasoning, and VLM-Perception-Cognition surveys identified as in-scope through the `_KnowledgeHub_/` tag-scan, then merged a duplicate row for [[2602.01630|WM Research Critical Assessment]].
2. **Extracted open problems** — Read the "Takeaways" / "Key Insights" callouts of each survey directly from KH notes. For the 7 surveys driving each direction (WAM Survey, WM Robot Survey, LfHV Survey, Foundation Models in Robotics, World Models for Embodied AI, Video-to-Control, Efficient VLA), verified content against alphaxiv-hosted overview reports to ensure the open-problem cells reflect authors' stated positions, not paraphrase drift. For older surveys, cross-referenced against newer papers in the same area to identify which open problems are already partially solved.
3. **Mined existing synthesis** — Drew on all 10 active `Embodied-AI/` deep-dives — [[02_Dataset-Benchmark-Environment]], [[03_VLA]], [[04_WAM]], [[05_Latent-World-Models]], [[06_Self-Evolving-VLA-WAM]], [[07_Physics-Aware-Embodied-AI]], [[08_VLA-Reasoning-and-CoT]], [[09_Egocentric-Pretraining-and-Human-Video]], [[10_Force-Aware-and-Tactile-Policies]], [[11_Sim-to-Real-Transfer]] — totaling ~4,200 lines of curated content. The primer [[01_Embodied-AI-101]] was treated as a navigational index. Mining was partial-not-uniform: deep-dives directly aligned with a Direction were read in full (e.g., [[04_WAM]] and [[06_Self-Evolving-VLA-WAM]] for Directions 3 and 6; [[10_Force-Aware-and-Tactile-Policies]] for Directions 1 and 2; [[07_Physics-Aware-Embodied-AI]] for Direction 5; [[08_VLA-Reasoning-and-CoT]] for Direction 4; [[11_Sim-to-Real-Transfer]] for Direction 5's transfer chain and Direction 8's deployment claims); other deep-dives were consulted for taxonomy framing, "Open Problems" callouts, and paper citations rather than full end-to-end re-reading. The deep-dives are the **vault's working taxonomy** — they encode which sub-areas the curator already separates and where the explicit "unresolved" annotations live.
4. **Filtered by saturation** — Excluded "more compute, bigger backbone" directions (saturated) and "hypothetical AGI" directions (premature). Kept directions with 3-10 recent papers attacking them but no consensus solution.
5. **Prioritized intersections** — VLA × WAM, VLA × RL, WAM × egocentric, tactile × VLA, physics × RL — where the survey-stated open problems concentrate.

---

## Cluster Overview

The 8 research directions group into three thematic clusters along the natural ML lifecycle pipeline:

> [!info] Cluster I — Foundations: Data, Sensors, Substrates
> *What the model is built on.* Two directions (1, 2) attack the upstream data + sensing bottleneck that constrains everything downstream. Both surface from the [[2604.15395|Foundation Models in Robotics Survey]] and [[2604.27621|Robot Learning from Human Videos Survey]] convergence on contact-rich + multi-modal data scarcity.

> [!info] Cluster II — Architecture & Training: How the Model Learns
> *How the VLA learns to act.* Three directions (3, 4, 5) restructure training objectives to match the causal structure of physical reasoning — joint state-action prediction (per the [[2605.12090|WAM Survey]]'s formal definition), causally-faithful reasoning (per [[2604.22074|CIR/SR Reasoning]]), and physics-verifiable rewards (per the [[2604.04974|Video-to-Control Survey]]).

> [!info] Cluster III — Evaluation, Robustness & Deployment
> *What the model does in the world.* Three directions (6, 7, 8) bridge the gap from "works in the lab" to "works in deployment" — measuring what matters (joint causal-consistency), detecting and recovering from failures (memory + recovery loops), and hitting real-time control budgets (efficient architectures + training + data co-design).

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **I — Foundations** | 1, 2 | Contact-rich, multi-modal data scarcity (4-orders-of-magnitude gap vs OXE) | D2's cross-sensor tactile encoder is the deployment substrate D1 needs to make its sensor-free, ego-pretrained policy transferable across robot platforms |
| **II — Architecture & Training** | 3, 4, 5 | Training objectives don't match the causal structure of physical reasoning | D3's latent co-evolving substrate exposes the intermediate reasoning tokens D4 needs for step rewards; D5's physics-verifiable rewards stabilize D3's joint loop against latent collapse and physics-violating imagination |
| **III — Evaluation, Robustness & Deployment** | 6, 7, 8 | Lab-to-real-world deployment gap (3–5 Hz ceiling, no joint metrics, no recovery loops) | D6's joint causal-consistency metric is what measures whether D3's joint-loop gains and D5's physics rewards actually transfer; D7's memory + recovery loop needs D8's efficiency co-design to fit a real-time budget |

---

## Survey landscape

The recent VLA/WAM survey wave defines current open problems. Older surveys are partially obsolete — many of their "future directions" are now well-trodden. Open-problem cells for the 7 surveys driving each direction have been verified against the alphaxiv-hosted overview report; minor cell enrichments are noted inline where alphaxiv content added detail (e.g., expanded modalities in WAM Survey, "tracking-error problem" in Video-to-Control).

| Survey | Scope | Stated open problems |
|---|---|---|
| [[2605.12090\|WAM Survey]] | Formal WAM definition; Cascaded vs Joint architectural taxonomy | (1) Joint metrics for **causal consistency** between imagined futures and generated actions; (2) Mixing diverse data ecosystems (robot/human/sim/internet video) — no principled methodology yet; (3) Separate WM-vs-action evaluation does not measure WAM utility; (4) Extension beyond RGB to **tactile, force, and acoustic** state representation; (5) Long-horizon distributional drift + compounding error; (6) Inference latency for closed-loop control |
| [[2605.00080\|WM Robot Survey 2026]] | Multi-dimensional taxonomy; transition from decoupled "predict-then-act" to unified VLA/MoE/MoT | (1) Evaluation must move beyond visual fidelity to **action faithfulness + physical consistency + downstream task utility**; (2) Closed-loop vs open-loop evaluation gap; (3) Latent-space world modeling is becoming dominant integration pattern; (4) **Causal conditioning gaps** on semantic intent and commands; (5) **Failure recovery coverage**: datasets lack error states + recovery behaviors; (6) Cross-embodiment generalization |
| [[2605.03941\|iWorld-Bench]] | Interactive world-model evaluation benchmark | (1) Standardized interactive evaluation across WAM types |
| [[2605.05017\|Privacy-Utility Trade-off]] | Position paper: privacy as life-cycle architectural constraint, not stage-local feature; SPINE framework + L1–L4 privacy classification matrix | (1) **Component-level privacy patches insufficient** — leakage is compositional across the EAI life cycle; (2) Regulatory-technical gap for closed-loop systems; (3) **Non-linear privacy-utility trade-off** (~30% SR drop, ~43% SPL drop under perceptual obfuscation); (4) Adaptive privacy orchestration based on real-time contextual sensitivity |
| [[2604.27621\|Robot Learning from Human Videos Survey]] | Task/observation/action-oriented LfHV taxonomy | (1) **Action-oriented transfer** is the direct deployment pathway but underexplored vs observation-only; (2) **Physically-grounded world models** moving beyond visual imitation to anticipate physical-interaction states; (3) **Physics-aware affordance extraction** beyond geometric cues; (4) **Continual learning** integration for absorbing new human video data; (5) Multi-agent interaction modeling; (6) **Multimodal signal incorporation** (audio, gaze, tactile); (7) Low-quality-video robustness at internet scale |
| [[2604.15395\|Foundation Models in Robotics Survey]] | 435 papers across 6-criteria taxonomy; 5-phase evolution | (1) **Tactile / failure-data scarcity** is the chief bottleneck; (2) **Embodiment-agnostic action spaces** with hardware-specific modulation; (3) Computational latency limits real-time deployment; (4) Hardware-agnostic architectures are missing; (5) **Long-horizon memory frameworks** preventing catastrophic forgetting; (6) **Physics-informed generative world models** reducing sim-to-real gaps; (7) Formal-verification frameworks for safety |
| [[2604.16592\|Cognition WM Survey]] | Cognitive-Architecture-Theory taxonomy spanning Video/Embodied/Epistemic WMs | (1) **Motivation and meta-cognition** (especially intrinsic motivation) are drastically under-developed; (2) Epistemic WMs over structured knowledge spaces are a new paradigm |
| [[2604.04974\|Video-to-Control Survey]] | Robotics integration layer between video prediction and dependable behavior; interface-centric taxonomy along explicitness × distance-from-actions | (1) **Robotics integration layer** is the critical gap — connecting video predictions to dependable robot behavior, including grounding, loop closure, and physical feasibility; (2) Implicit/abstract/explicit interface trade-offs unresolved; (3) **Tracking-error problem** — controllers struggle realizing visual targets; (4) **Latent-action identifiability** — ensuring representations capture controllable changes, not exogenous factors; (5) Pre-execution verification missing in direct policy methods; (6) Tactile + force/torque + proprioceptive integration with video interfaces |
| [[2604.23775\|VLA Safety Survey]] | Training-time and inference-time threats to VLA | (1) Multi-layered defense balancing alignment + guardrails; (2) Evaluation methodologies remain fragmented |
| [[2604.26509\|3D Generation for Embodied AI Survey]] | Conventional 3D generation vs embodied-oriented (interaction-ready, physically grounded) | (1) Scarcity of physical annotations; (2) Geometry-vs-physics trade-off; (3) Deformable asset complexity; (4) Persistent sim-to-real gap |
| [[2604.22748\|Agentic World Modeling Survey]] | L1 Predictor / L2 Simulator / L3 Evolver capability hierarchy crossed with 4 governing-law regimes (physical / digital / social / scientific); proposes ASR (Action Success Rate) + COD (Counterfactual Outcome Deviation) decision-centric metrics | (1) **Counterfactual reasoning** at the world-model level (L2 intervention sensitivity); (2) **Constraint adherence** to governing laws; (3) **Autonomous self-revision based on evidence** (L3 Evolver capability) — physical-world L3 is "emerging" not mature; (4) Shift from generative metrics (FVD/PSNR) to decision-centric evaluation (ASR/COD) — 10 open problems enumerated overall |
| [[2604.04707\|OpenWorldLib]] | Unified framework + standardized world-model definition spanning interactive video gen, 3D gen, VLA, multimodal reasoning | (1) **Lack of universally-accepted definition** fragments the field; (2) 3D generation geometric consistency under significant camera motion still poor (VGGT, FlashWorld); (3) Modular pipeline composition (Operator/Synthesis/Reasoning/Representation/Memory) as research substrate |
| [[2604.00061\|R2X Multi-Robot MLLM Survey]] | Robot-to-Everything paradigm — MLLM-driven multi-robot sensing/communication/computation | (1) Bandwidth bottleneck for transmitting multimodal sensor data to central MLLM; (2) Open-vocabulary perception with on-device compute; (3) Joint optimization of sensing/communication/computation under heterogeneous teams |
| [[2604.28185\|Visual Generation Survey]] | Five-level taxonomy of visual intelligence (atomic generation → agentic world modeling); in-the-wild stress tests on frontier models | (1) **Precise spatial reasoning + physical-law understanding** are the primary diagnosed gaps in frontier visual generators; (2) Multi-turn editing consistency degradation; (3) **L4 agentic generation** (VLM + external control loops for planning/verification) as the emerging frontier architecture |
| [[2604.15911\|Efficient Video Diffusion Survey]] | Deployment-oriented review of video-diffusion acceleration; 4-category taxonomy (step distillation / efficient attention / model compression / cache-trajectory optimization) | (1) **KV cache movement** is the major DiT bottleneck — pure FLOPs reduction is insufficient; (2) **1–4 step distribution distillation** enables real-time streaming generation; (3) Sparse attention as quality/speed balanced lever; (4) **Quantization (QAT / PTQ with timestep compensation)** is the most deployment-ready technique |
| [[2604.02029\|Latent Space Survey]] | Comprehensive survey of the latent-space paradigm in language-based models; 5-aspect framework (Foundation / Evolution / Mechanism / Ability / Outlook) | (1) **Evaluability / controllability / interpretability** due to latent opacity; (2) Theoretical foundations missing; (3) **Modality-native multimodal integration** of latent spaces; (4) Governable latent AI systems |
| [[2603.28489\|Video Gen as WM Survey]] | Efficiency-focused 3D taxonomy (paradigm × architecture × inference) for video-based WMs | (1) **Efficiency is a prerequisite** (not optimization) for real-time WM deployment; (2) Diffusion distillation, sparse attention, quantization are the levers; (3) Need integrated efficiency across modeling/architecture/inference dimensions |
| [[2602.01630\|WM Research Critical Assessment]] | Position paper: world-model research is fragmented; proposes unified 5-module framework (Interaction / Reasoning / Memory / Environment / Multimodal Generation) | (1) Fragmentation — narrow tasks (video gen, MBRL, autonomous driving) treated independently; (2) Need integrated module-level architecture spanning perception + cognition + action; (3) Lack of holistic understanding of physical world as evaluation gap |
| [[2511.02097\|WM Manipulation Survey]] | Step-toward-world-models survey on manipulation | (1) Structured task-relevant representations (object-centric); (2) Hierarchical architectures for long-horizon |
| [[2510.24795\|Efficient VLA Survey]] | First survey dedicated to efficient VLAs; three-pillar taxonomy (model design / training / data collection) | (1) **Inference latency / control frequency** incompatible with edge deployment; (2) **Pre-training cost** (OpenVLA's 21,500 A100-GPU hours); (3) Data collection labor (shift to massively-parallel sim + internet-scale human video + self-exploration); (4) **Adaptive embodiment-agnostic architectures**; (5) **Self-sustaining generative data ecosystems**; (6) Resolving compactness/expressivity, scalability/stability, data-quality/accessibility tensions |
| [[2510.16732\|World Models for Embodied AI Survey]] | Three-axis taxonomy (Functionality × Temporal Modeling × Spatial Representation); the canonical comprehensive WM-Embodied survey | (1) **Unified datasets** across robotics/AD/video; (2) **Physically-consistent metrics** beyond FID/FVD; (3) Long-horizon temporal consistency; (4) Architectural evolution from latent vectors → token sequences → explicit 3D rendering (NeRF, Gaussian Splatting); (5) **SSMs and hybrid autoregressive-global paradigms** remain under-explored; (6) Deeper WM × LLM-CoT synergy |
| [[2510.07077\|VLA Robotics Review 2025]] | Full-stack VLA review (software + hardware + data + platforms) for real-world deployment | (1) **Embodiment transfer** across morphologies; (2) Data scarcity; (3) Computational cost; (4) Rigorous evaluation & safety mechanisms; (5) Gradient insulation, PEFT, inference optimization as deployment levers |
| [[2510.04978\|Physical AI Survey]] | Hierarchical taxonomy of physics-aware AI (perception → reasoning → modeling → interaction); 300+ papers | (1) **Causal physical understanding** missing — models learn statistical correlations only; (2) Compositional/causal structure of physical laws not internalized; (3) Hybrid "Neural Physics" (explicit laws + neural learning) is the emerging pattern |
| [[2509.20021\|Embodied AI LLM-WM Survey]] | Joint MLLM + WM architecture roadmap | (1) MLLM-WM unified architecture; (2) Integration patterns |
| [[2509.19012\|Pure VLA Survey]] | 5-paradigm action-generation taxonomy (autoregression/diffusion/RL/hybrid/specialized); 300+ studies | (1) Data scarcity; (2) Architectural heterogeneity; (3) **Real-time inference constraints**; (4) Evaluation benchmark fragmentation; (5) World modeling + **causal reasoning** as the path to trustworthy VLA |
| [[2508.13073\|VLA Survey 2025]] | VLA landscape | (Partially superseded — see later 2025 VLA reviews) |
| [[2508.07407\|Self-Evolving AI Agents Survey]] | Unified framework + taxonomy of self-evolution techniques bridging static foundation models and lifelong agentic systems | (1) **Continuous self-improvement** without catastrophic forgetting; (2) Evolution-evaluation gap; (3) Safety + alignment under self-modification |
| [[2507.21046\|Self-Evolving Agents Survey]] | "What, When, How, Where to Evolve" 4-dimensional decomposition of self-evolution paths to ASI | (1) **Adaptivity / retention / generalization / efficiency / safety** are the five critical evaluation gaps; (2) Emergent risks and mitigation strategies for dynamic agents under-developed |
| [[2507.21045\|4D Spatial Intelligence Survey]] | 5-level hierarchical taxonomy (low-level reconstruction → 4D dynamic scene → physics-aware → interactive) | (1) Cross-level evaluation lacking; (2) Physics-aware 4D reconstruction; (3) Interactive 4D scene editing |
| [[2507.10672\|VLA Manipulation Survey]] | 102 VLA models + 26 datasets + 12 simulators quantitatively benchmarked | (1) **Multimodal × high-complexity dataset gap** (only Kaiwu is an outlier); (2) Simulator visual-fidelity vs throughput trade-offs; (3) Native language-grounding APIs missing in simulators |
| [[2507.00917\|Embodied Intelligence Survey]] | 5-level IR-L0/L4 grading + physical simulators × world models synergy | (1) **Sim2Real gap** as central challenge; (2) Lack of unified framework to assess robot capability progression; (3) World models as "neural simulators" generating controllable synthetic data |
| [[2506.20966\|VLA Post-Training Survey]] | VLA RL/SFT post-training taxonomy | (1) Generalization-vs-precision; (2) Knowledge insulation during RL |
| [[2506.20134\|3D World Models Survey]] | 2D → 3D world models transition | (1) 3D spatial understanding still underdeveloped |
| [[2505.07634\|Neural Brain Framework]] | Neuroscience-inspired 4-component embodied-agent architecture (sensing/PCA/memory/neuromorphic HW) | (1) Multimodal **active sensing** strategies; (2) Closed-loop perception-cognition-action integration; (3) **Neuroplasticity-driven memory** with consolidation; (4) Energy-efficient neuromorphic HW/SW co-design |
| [[2505.05108\|Multi-agent Embodied AI Survey]] | First systematic multi-agent embodied AI review | (1) Asynchronous decision-making; (2) Heterogeneous team composition; (3) **Self-evolution in open environments**; (4) Multi-agent benchmarks are nascent with idealized assumptions |
| [[2505.04769\|VLA Survey]] | 80+ VLA models across 6 application domains; concepts/progress/applications/challenges | (1) **Real-time inference** (autoregressive limits to 3–5 Hz); (2) Safety (collision prediction ~82%); (3) Generalization gap (up to 40% degradation on unseen tasks); (4) Dual-system architectures + co-fine-tuning + LoRA as levers |
| [[2504.21853\|Interactive Generative Video Survey]] | 5-module decomposition (Generation / Control / Memory / Dynamics / Intelligence) of IGV across gaming, embodied AI, autonomous driving | (1) Real-time interactivity vs generation quality trade-off; (2) Persistent memory across episodes; (3) **Dynamics fidelity** (physics, causality); (4) Cross-domain transferability of generative video controllers |
| [[2504.01990\|Foundation Agents Survey]] | Brain-inspired framework unifying foundation-agent architecture, collaboration, and safety | (1) **Autonomous + adaptive + safe** agents under one architecture; (2) Mapping AI capabilities to human cognition exposes systematic gaps; (3) Collaboration patterns under-explored |
| [[2503.21765\|Physics Cognition Survey]] | Three-tier cognitive-science taxonomy (Basic Schema / Passive / Active Cognition) of physics in video gen | (1) **Models still fall short of human-level physics understanding** — esp. multi-object & fluid; (2) Limited physical coverage (mechanics/optics/thermal/material); (3) Computational inefficiency; (4) Sim2Real gap; (5) **Physics foundation models** and **neuro-symbolic approaches** as the path forward |
| [[2503.04641\|Multimodal Generative World Simulators Survey]] | Unified framework spanning 2D appearance → 4D representations integrating appearance + dynamics + geometry | (1) Cross-modal dependency unmodeled; (2) 4D integration of appearance/dynamics/geometry is sparse; (3) Towards comprehensive world simulators |
| [[2602.04411\|Self-evolving Embodied AI]] | New paradigm with 5 co-evolving modules (memory / task / environment / embodiment / model self-evolution) | (1) Confined to "human-crafted settings" — needs in-the-wild autonomy; (2) **Multi-timescale closed-loop co-evolution** across 5 modules; (3) Existing WM/memory/embodiment work as foundational components but not yet integrated |
| [[2601.15533\|Actionable Simulators]] | Reframes WMs as actionable simulators with physical grounding + causal reasoning (4 imperatives) | (1) **Dynamical hallucinations** — visual realism ≠ physical understanding; (2) Structured 4D interfaces; (3) Self-evolution for consistency; (4) **Closed-loop, decision-oriented evaluation** replacing perceptual metrics |
| [[2601.07823\|Video Generation in Robotics Survey]] | Video gen as embodied WMs for imitation/RL/policy-eval/visual-planning; 10 challenges enumerated | (1) Hallucinations & physics violations; (2) Uncertainty quantification; (3) Long video generation; (4) Prohibitive compute; (5) Need **robotics-centric evaluation benchmarks** (vs visual-fidelity metrics) |
| [[2501.10928\|Generative Physical AI Survey]] | 6-paradigm taxonomy of physics-aware generation (explicit vs implicit physics integration in 3D/4D synthesis) | (1) Functional vs visual realism gap; (2) Evaluation metrics for physical plausibility; (3) Material-behavior fidelity (rigid/soft/fluid) |
| [[2512.24385\|Spatial Intelligence Pre-training Roadmap]] | Roadmap for multi-modal data pre-training in autonomous systems → robust spatial intelligence | (1) Single-modality → unified pre-training transition; (2) 3D perception data scarcity; (3) Generative WM × spatial-reasoning integration |
| [[2504.09848\|LLM Spatial Intelligence Survey]] | Cross-scale spatial-intelligence framework (embodied agents / smart cities / Earth science) grounded in cognitive-science principles | (1) Fragmented spatial-intelligence research across scales lacks a unified framework; (2) Cognitive foundations of LLM spatial reasoning are unsystematized; (3) **Limits of current LLM spatial capabilities** in embodied agent deployment |
| [[2504.15037\|MLLM Spatial Reasoning Position Paper]] | Position paper diagnosing spatial-reasoning deficiencies in MLLMs across training data / architecture / objectives / evaluation | (1) **Scaling existing architectures will not resolve spatial-reasoning gaps**; (2) Critical limitations in data, architecture, training objectives, and evaluation jointly bottleneck embodied AI + autonomous driving deployment; (3) Need for spatial-specific recipes beyond model scaling |
| [[2509.25373\|VLM Perception-Cognition Survey]] | "From Perception to Cognition" framework decomposing MLLM vision-language reasoning into interdependent layers | (1) **Shallow / incoherent perception-cognition integration** is the bottleneck for current MLLMs; (2) Models struggle to translate low-level pixel processing into coherent internal world models for higher-order reasoning; (3) Hallucination and biases stem from disjointed perception-reasoning coupling |
| [[2411.14499\|World Models Survey 2024]] | Dual categorization (implicit representation vs future-state prediction) across games/robotics/AD/social | (1) Robust **physical-rule adherence**; (2) Standardized benchmarks; (3) Sim2Real gap; (4) Ethics/safety (data privacy, unsafe simulations, AI-content accountability); (5) Trend toward interactive 3D + first-person + action-conditioned WMs |
| [[2407.06886\|ARIO]] | Comprehensive embodied-AI survey + ARIO dataset standard (3M episodes, 321K tasks) | (1) **Sim2Real gap** as central challenge; (2) Data heterogeneity / cross-platform incompatibility; (3) MLM + WM integration as foundational |
| [[2404.14387\|LLM Self-Evolution Survey]] | Four-phase iterative cycle (experience acquisition / refinement / updating / evaluation) for autonomous LLM development | (1) Lifelong-learning catastrophic forgetting; (2) Quality of self-generated experience; (3) Alignment of self-evolved models with human preferences |
| [[2311.00530\|LLM Embodied Navigation Survey]] | LLM-in-navigation taxonomy comparing LLM-based vs non-LLM navigation models | (1) Long-horizon planning grounded in language; (2) LLM-context-window limits in dynamic environments; (3) Multimodal grounding (language × image × map) |
| [[2310.06253\|Objective-Mismatch Survey]] | Taxonomic survey of solution categories for the model-based RL "objective mismatch" — WM predictive accuracy fails to correlate with policy action quality | (1) **Decision-aware MBRL** unifying WM training and policy training; (2) Objective alignment between predictive loss and downstream return; (3) Conceptual fragmentation across MBRL solution families |
| [[2103.04918\|Embodied AI Simulators Survey]] | 9 simulators × 7 features × 3 tasks (visual exploration / navigation / EQA) — foundational | (1) Simulator–task interconnections; (2) Realistic-physics + interactive-object support; (3) Cross-simulator benchmarking |

**Patterns across the survey wave:**
- **Joint WM-action evaluation gap** is now a 5-way convergence: [[2605.12090|WAM Survey]], [[2605.00080|WM Robot Survey 2026]], [[2510.16732|World Models for Embodied AI Survey]], [[2601.15533|Actionable Simulators]], and [[2601.07823|Video Generation in Robotics Survey]] all independently call out **separate WM-vs-action evaluation does not measure WAM utility**. World Models for Embodied AI Survey terms it "physically-consistent metrics beyond FID/FVD"; Actionable Simulators calls it "closed-loop, decision-oriented evaluation"; the recent WAM surveys call it "causal consistency / action faithfulness". Same diagnosis, different vocabulary — the strongest signal in the survey wave. The objective-mismatch literature ([[2310.06253|Objective-Mismatch Survey]]) provides the underlying MBRL framing: WM predictive accuracy fails to correlate with policy action quality.
- **Physical grounding / dynamical hallucinations** is a parallel 5-way convergence: [[2503.21765|Physics Cognition Survey]], [[2510.04978|Physical AI Survey]], [[2601.15533|Actionable Simulators]], [[2411.14499|World Models Survey 2024]], and [[2501.10928|Generative Physical AI Survey]] all identify the gap between **visual realism and physical understanding**. Physical AI Survey is most explicit: "Models learn statistical correlations only — causal physical understanding missing." All five reach the same conclusion: hybrid neural-symbolic / verifiable-physics approaches are needed.
- **Data scarcity** (tactile, failure, contact-rich, multimodal-high-complexity) is a 6-way convergence: [[2604.15395|Foundation Models in Robotics Survey]], [[2604.27621|Robot Learning from Human Videos Survey]], [[2509.19012|Pure VLA Survey]], [[2507.10672|VLA Manipulation Survey]], [[2407.06886|ARIO]], and [[2512.24385|Spatial Intelligence Pre-training Roadmap]] all flag this. Recent surveys add that **internet-scale human video + massively-parallel simulation + self-exploration** are the dominant scaling levers — converging on the Direction 1 recipe.
- **Efficiency as prerequisite** is a 3-way convergence: [[2510.24795|Efficient VLA Survey]], [[2603.28489|Video Gen as WM Survey]], and [[2604.15911|Efficient Video Diffusion Survey]] all reframe efficiency from "optimization" to "prerequisite for deployment". The most concrete diagnostic — **KV cache movement** is the major DiT bottleneck, with quantization (QAT/PTQ) the most deployment-ready lever. Combined with the [[2505.04769|VLA Survey]]'s "3–5 Hz autoregressive ceiling" diagnosis, this is the dominant deployment bottleneck.
- **Physical-reasoning gaps in visual generators** add a 4th independent signal to the physical-grounding convergence: [[2604.28185|Visual Generation Survey]]'s in-the-wild stress tests on frontier models explicitly diagnosed **precise spatial reasoning and physical-law understanding** as the primary failure modes — converging with [[2503.21765|Physics Cognition Survey]], [[2510.04978|Physical AI Survey]], and [[2601.15533|Actionable Simulators]] on the same diagnosis, but with concrete per-model failure data rather than survey aggregation. Reinforces **Direction 5**.
- **Latent-space methodology has its own emerging survey signal**: [[2604.02029|Latent Space Survey]] consolidates the latent-space paradigm in language-based models and flags **evaluability / controllability / interpretability** as primary open problems. The opacity diagnosis directly motivates **Direction 4's latent-utilization probing** sub-problem and adds methodological grounding to **Direction 3's latent-space co-evolution** thesis.
- **Self-evolution / autonomous adaptation** is now a 6-way convergence: [[2602.04411|Self-evolving Embodied AI]], [[2604.16592|Cognition WM Survey]], [[2604.22748|Agentic World Modeling Survey]], [[2508.07407|Self-Evolving AI Agents Survey]], [[2507.21046|Self-Evolving Agents Survey]], and [[2404.14387|LLM Self-Evolution Survey]] all identify **meta-cognition / autonomous self-revision / model self-evolution** as the missing cognitive function. The 5-module embodied self-evolving survey provides the most concrete decomposition (memory / task / environment / embodiment / model); the "What/When/How/Where" framework adds the 5 evaluation gaps (adaptivity / retention / generalization / efficiency / safety).
- **Unified-definition fragmentation** is itself a meta-pattern: [[2604.04707|OpenWorldLib]], [[2510.16732|World Models for Embodied AI Survey]], [[2411.14499|World Models Survey 2024]], and [[2602.01630|WM Research Position]] all explicitly bemoan the lack of a universally accepted WM definition. The position paper [[2602.01630|WM Research Position]] is the most critical: research is fragmented across narrow tasks (video gen, MBRL, autonomous driving) treated independently. This signals the field is still pre-paradigmatic — empirical convergence is outpacing terminological convergence.
- The **older surveys** ([[2411.14499|World Models Survey 2024]], [[2508.13073|VLA Survey 2025]], [[2506.20966|VLA Post-Training Survey]], [[2103.04918|Embodied AI Simulators Survey]]) are partially superseded — their "future work" sections are substantially addressed by recent work, though their **physics-grounding** and **sim2real** sub-problems remain unresolved.

---

## Cluster I — Foundations: Data, Sensors, Substrates

*What the model is built on.* These two directions attack the upstream data + sensing bottleneck that constrains everything downstream — converting hand video and heterogeneous tactile sensors into the substrate that the architecture-and-training work in Cluster II can stand on.
### Direction 1 — Tactile-Egocentric Pretraining: From Hand Video Alone to Force-Aware VLA

**Thesis.** Train a VLA's force-aware components using *only* egocentric human hand video — no force sensors in the loop — by exploiting recent vision-to-tactile prediction work and the EgoScale log-linear scaling law.

#### Why it matters

Two convergent constraints make this direction live:
- **The contact-rich data gap** ([[2604.15395|Foundation Models in Robotics Survey]]): "Force-aware policy performance is bounded by data scale, not architecture. Until we have an OXE for contact-rich tasks, force-aware VLAs will be data-limited." [[2505.22159|ForceVLA]]'s ForceVLA-Data (244 trajectories) is 4 orders of magnitude smaller than [[2310.08864|OXE]].
- **The egocentric scaling law** ([[2602.16710|EgoScale]]): 20,854-hour log-linear curve up to **+54%** on 22-DoF dexterous hands. Combined with [[2603.15257|HapticVLA]]'s teacher-student distillation showing tactile-awareness can be transferred *without* inference-time tactile sensors, the path is clear: scale egocentric pretraining and use distillation to inject force-awareness.

This connects to the user's investment in egocentric work (`09_Egocentric-Pretraining-and-Human-Video.md` is the user's most-recently-enriched deep-dive) and addresses the **most-emphasized open problem from the Robot Learning from Human Videos Survey**: "44% of action-oriented methods now deployable from human videos alone — but reasoning and contact-rich transfer remain underexplored." [[2510.24795|Efficient VLA Survey]] reinforces this — it explicitly names "internet-scale human video" as one of three dominant data-collection levers for efficient VLAs, alongside massively-parallel simulation and self-exploration. [[2510.07077|VLA Robotics Review 2025]] adds that embodiment-transfer (human hand → gripper) remains a top-3 unresolved deployment challenge.

#### Current state of evidence

- [[2605.13083|TouchAnything]] is the foundational bridge — **first multi-view egocentric + bimanual dense tactile dataset** (20 hr, head + wrist + pressure maps). View dropout training reduces ego-only drop from **−27.20% → −5.78%**.
- [[2603.15257|HapticVLA]] is the deployment proof — teacher uses tactile sensors, student distills to inference *without* them. **86.7%** SR on fragile-object tasks; **45pp** absolute gain on egg manipulation over SmolVLA.
- [[2601.20321|TaF-VLA]] provides the alignment substrate — **10M synchronized tactile-force pairs** + VQ-VAE force latent; cross-sensor zero-shot at **60.3%** SR.
- [[2410.24090|Sparsh]] / [[2506.14754|Sparsh-X]] — SSL touch foundation models (460k-1M unlabeled contacts), with **>500%** plug-insertion gain.
- [[2507.15597|Being-H0]] / [[2605.00078|Being-H0.7]] — Full VLA pretraining on UniHand (150M instruction-motion pairs); the egocentric VLA backbone.

What's missing: **No paper yet trains a force-aware VLA from egocentric hand video alone** (i.e., zero force sensors). HapticVLA distills from a tactile-equipped teacher; TouchAnything has tactile sensors but uses them as supervision. The clean test: pretrain on egocentric video → predict tactile signals as auxiliary supervision → distill to deployment without sensors.

#### Concrete sub-problems

1. **Vision-to-tactile prediction at scale.** Extend TouchAnything's view-dropout recipe to the EgoScale data volume (20,854 hours). The dataset needs synthetic tactile labels — generate them by running Sparsh-X on the small fraction of EgoScale that has tactile, then use Sparsh as a teacher for the rest.
2. **A force-aware MoE that consumes predicted (not measured) tactile.** Architecture: predict tactile from vision via a learned head, feed prediction into the [[2505.22159|ForceVLA]]-style FVLMoE. Compare against the same architecture with real tactile signals.
3. **Compositional pretraining mixture.** Combine egocentric video ([[2110.07058|Ego4D]] + UniHand + [[2505.11709|EgoDex]]) + force-conditioned video pretraining ([[2505.19386|Force Prompting]]) + small tactile-instrumented dataset ([[2605.13083|TouchAnything]] when scaled). Ablate which mixture maximizes contact-rich transfer.
4. **Cross-embodiment force transfer.** Train on human hand → transfer to gripper. Compare three projection strategies: explicit ([[2507.15597|Being-H0]]'s MANO + GRQ-VAE), keypoint-based ([[2512.22414|π0.5 + ego]]), or learned ("treat humans as another embodiment"). [[2602.16710|EgoScale]] suggests data volume matters more than projection form — verify on force tasks.
5. **Contact-rich benchmark suite.** Re-run [[2505.22159|ForceVLA]]'s 5-task contact-rich benchmark and [[2603.15169|ForceVLA2]]'s set, using only egocentric-pretrained policies. Currently no published numbers exist for this configuration.

#### Related papers

- [[2605.13083|TouchAnything]] — First multi-view ego + dense tactile dataset; the foundational bridge
- [[2603.15257|HapticVLA]] — Sensor-free deployment via distillation; the existence proof for "no tactile at inference"
- [[2601.20321|TaF-VLA]] — VQ-VAE force latent + 10M tactile-force pairs; the alignment substrate
- [[2506.14754|Sparsh-X]] — Multisensory touch foundation model (1M contacts); the encoder backbone
- [[2602.16710|EgoScale]] — Log-linear scaling law (+54% dexterous); the scaling target
- [[2605.00078|Being-H0.7]] — Latent dual-branch egocentric pretraining; the recipe template
- [[2505.19386|Force Prompting]] — Force-conditioned video generation; provides physics priors via pretrained video models
- [[2507.15597|Being-H0]] — Physical Instruction Tuning + GRQ-VAE motion tokens
- [[2512.22414|π0.5 + ego]] — "Treat humans as another embodiment" — the simplest recipe

#### Benchmark coverage

**Existing**: TacBench ([[2410.24090|Sparsh]]) for tactile representation, ForceVLA-Data (244 trajectories) for policies, [[2510.25725|HumanoidVTA]] for soft-object tactile.
**Gap**: No benchmark currently isolates the question "can a policy trained from egocentric video alone match a policy trained with real tactile sensors?" A direct comparison on ForceVLA's 5 contact-rich tasks would settle this.

#### Risk / what could fizzle

- **Vision-to-tactile prediction has a noise floor.** Some tactile information is fundamentally not in the visual signal (e.g., subtle slip detection requires fingertip pressure, not visual cues). The policy may plateau below a sensor-equipped baseline.
- **Scaling cost.** 20,000+ hours of egocentric data is expensive to curate even for pretraining; tactile-labeled data is even scarcer.
- **Embodiment mismatch.** Human hands (22-DoF) vs grippers (1-7 DoF) creates a large action-space gap that force prediction doesn't directly address.
- **Cross-sensor brittleness.** TaF-VLA's 60.3% cross-sensor zero-shot is encouraging but not deployment-ready.
### Direction 2 — Cross-Sensor Tactile Foundation Models for Plug-And-Play Force-Aware VLAs

**Thesis.** Build the [[2304.07193|DINOv2]] analog for tactile — a *cross-sensor* SSL representation that lets a force-aware VLA trained on one tactile sensor type ([[2509.18830|DexSkin]]) transfer to another ([[2604.28156|FlexiTac]], [[2604.20689|FingerEye]]) without re-collection.

#### Why it matters

[[2604.15395|Foundation Models in Robotics Survey]] flagged **tactile data scarcity** as one of the top 3 bottlenecks. [[2604.27621|Robot Learning from Human Videos Survey]] independently names "Multimodal signal incorporation (audio, gaze, **tactile**)" as one of 7 open problems — tactile sensing is structurally under-represented in the cross-embodiment data stack. [[2604.16592|Cognition WM Survey]] (alphaxiv-verified) generalizes this from the cognitive side: among the 7 cognitive functions it surveys, *perception* innovations are documented mostly in vision/language modalities, with tactile-as-perception under-represented — Embodied WMs need "precise physical grounding, including encoding contact geometry, 6-DoF pose, and persistent environmental models." The cluster has converged architecturally — [[2603.15169|ForceVLA2]] (66% avg SR, +48pp over π0) has demonstrated that force-aware MoE works — but every new robot platform restarts data collection from scratch because policies are sensor-specific. [[2509.18830|DexSkin]]'s pneumatic calibration partially solves cross-instance transfer for the *same* sensor type, but cross-sensor-modality transfer (DexSkin → FlexiTac) is essentially untested.

[[2410.24090|Sparsh]] / [[2506.14754|Sparsh-X]] established the SSL touch foundation model idea (460k-1M unlabeled contacts), but Sparsh trains *per-sensor* — different encoders for DIGIT, GelSight Mini, etc. The next frontier is a single encoder that handles all sensors.

[[2601.20321|TaF-VLA]]'s 60.3% cross-sensor zero-shot SR is the closest existing result — using force as the grounding signal (VQ-VAE on 10M tactile-force pairs). But 60.3% is not deployment-ready.

#### Current state of evidence

- **Sensor diversity**: [[2509.18830|DexSkin]] (capacitive, 294° coverage), [[2604.28156|FlexiTac]] ($30 FPC piezoresistive), [[2604.20689|FingerEye]] (binocular vision-tactile fingertip), plus older GelSight/DIGIT
- **SSL foundation models**: [[2410.24090|Sparsh]] (460k images, MAE/DINO/JEPA across 4 sensors), [[2506.14754|Sparsh-X]] (1M contacts, multisensory: image + audio + IMU + pressure)
- **Cross-sensor work**: [[2601.20321|TaF-VLA]] (VQ-VAE force latent, 60.3% zero-shot), [[2509.18830|DexSkin]] (pneumatic calibration for cross-instance)
- **Touch foundation alignment**: [[2605.14571|MTNet]] (visuo-tactile alignment via probabilistic + feature + geometric constraints, Centered Kernel Alignment ~0.74)
- **Deployment without sensors**: [[2603.15257|HapticVLA]] (teacher-student distillation, 86.7% SR)

What's missing: **No paper trains an SSL tactile encoder that achieves >80% cross-sensor zero-shot SR**. The closest, TaF-VLA at 60.3%, is plug-and-play but operates only in trained sensor families. A true tactile DINOv2 would treat sensor heterogeneity as augmentation, learning sensor-invariant representations.

#### Concrete sub-problems

1. **Sensor-invariant SSL objective.** Extend Sparsh-X's attention-bottleneck multi-modal fusion to *cross-sensor* fusion — treat sensor type as an auxiliary input, train with a cross-sensor MAE-style objective (mask one sensor's signal, predict from another). The DINOv2-style EMA-teacher pattern naturally extends here.
2. **Force-as-bridge grounding.** TaF-VLA showed force is the unifying signal across sensor types — extend its VQ-VAE alignment to *all* sensor types simultaneously, not just within tactile families.
3. **A cross-sensor benchmark.** Currently no benchmark exists. The cleanest test: train on N-1 sensors, evaluate on the held-out sensor across [[2410.24090|Sparsh]]'s TacBench tasks. Target >80% retention of in-distribution SR.
4. **Cross-sensor VLA fine-tuning.** Bolt the cross-sensor encoder onto [[2603.15169|ForceVLA2]]'s Cross-Scale MoE. Demonstrate that fine-tuning on one sensor type generalizes to another.
5. **Deployment chain validation.** Train on sim (or one real sensor) → deploy on a different real sensor → measure performance loss. [[2604.28156|FlexiTac]]'s Kelvin-Voigt sim-to-real calibration provides a reference protocol.

#### Related papers

- [[2410.24090|Sparsh]] / [[2506.14754|Sparsh-X]] — Per-sensor SSL touch foundation models; the architectural starting point
- [[2601.20321|TaF-VLA]] — Force-grounded tactile alignment via VQ-VAE; the closest cross-sensor existing work
- [[2509.18830|DexSkin]] — Pneumatic calibration for cross-instance transfer
- [[2604.28156|FlexiTac]] — $30 open-source piezoresistive skin
- [[2604.20689|FingerEye]] — Binocular vision-tactile fingertip
- [[2603.15169|ForceVLA2]] — Cross-Scale MoE + force prompts (66% avg SR, +48pp over π0); deployment target
- [[2603.15257|HapticVLA]] — Sensor-free deployment via distillation
- [[2605.14571|MTNet]] — Visuo-tactile cortical-alignment principles

#### Benchmark coverage

**Existing**: TacBench (Sparsh, 6 tasks across 4 sensors), ForceVLA-Data (244 trajectories), [[2510.25725|HumanoidVTA]] (2,124-sensor humanoid).
**Gap**: No benchmark specifically tests **cross-sensor transfer** — held-out-sensor zero-shot evaluation. Building one would be the natural first paper in this direction.

#### Risk / what could fizzle

- **Physical sensor differences may be fundamentally incompatible.** Capacitive vs piezoresistive vs vision-tactile have different signal distributions and noise floors. A truly sensor-invariant encoder may need to discard task-relevant fine detail to be invariant.
- **The cross-sensor data problem is recursive.** To train cross-sensor SSL, you need data from many sensors — but you don't have data from many sensors precisely *because* cross-sensor transfer is the bottleneck.
- **TaF-VLA's 60.3% may be near the ceiling.** If the visual-to-tactile information bottleneck is fundamental, no SSL alone can break it.

---

## Cluster II — Architecture & Training: How the Model Learns

*How the VLA learns to act.* These three directions restructure the training objective itself — joint state-action prediction, causally-faithful latent reasoning, and physics-verifiable rewards — so the gradients shape the policy along the causal structure of physical reasoning rather than statistical correlation.
### Direction 3 — Single-Loop Co-Evolving VLA + World Model in Latent Space

**Thesis.** Move beyond the alternating co-improvement loop ([[2602.12063|VLAW]]'s pattern) toward a unified, single-step gradient flow where action and imagination losses jointly update both the policy and the world model in the *same* optimizer step — operating in **latent space** to keep the loop real-time.

#### Why it matters

The [[2605.12090|WAM Survey]] (alphaxiv-verified) **formally defines WAMs** as a class of foundation models that must satisfy two criteria: (1) *Forward Predictive Modeling* — forecasting environment evolution via $o'$ (visual predictions or implicit physical representations); (2) *Coupled Action Generation* — deducing motor commands $a$ "by strictly aligning them with the anticipated future states $o'$". The survey crystallizes this as a joint objective:
$$\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o,l,o',a)\sim\mathcal{D}}\big[-\log p(o', a \mid o, l)\big]$$
"By moving beyond observation-to-action mapping towards joint state-action prediction" — but explicitly organizes existing methods into a **Cascaded vs Joint** taxonomy, identifying Joint WAMs as the architectural frontier. [[2605.00080|WM Robot Survey 2026]] (alphaxiv-verified) corroborates the trajectory: "the design space has progressively expanded toward single-backbone, unified VLA, and latent world-modeling approaches with tighter integration between prediction and action generation." [[2602.04411|Self-evolving Embodied AI]] generalizes this into a 5-module framework (memory / task / environment / embodiment / model self-evolution) — the joint VLA+WM loop here is the "environment self-prediction × model self-evolution" intersection. [[2510.16732|World Models for Embodied AI Survey]] flags evolution from latent vectors → token sequences → explicit 3D rendering as the architectural trajectory.

Most current "joint" implementations fall short of the WAM Survey's joint-distribution criterion:
- [[2602.12063|VLAW]] alternates: train VLA, train WM, repeat — gives the WM stale data each cycle (cascaded co-improvement, not joint distribution).
- [[2603.16666|Fast-WAM]] trains jointly but only at training time, dropping the WM at deployment — sacrifices test-time imagination benefit.
- [[2605.15153|Pelican-Unified]] shows the cleanest *architectural* unification (shared latent z), but training is still multi-stage rather than single-step.

The literature gap is concrete and survey-stated: a **single GRPO loop on the joint (action, imagination) log-prob** $p(o', a \mid o, l)$ with cooperative gradient flow has not yet been demonstrated end-to-end in latent space. The architectural substrate (latent WAMs per [[2510.16732|World Models for Embodied AI Survey]]'s trajectory) and the optimization substrate (GRPO variants from [[2506.20966|VLA Post-Training Survey]]) both exist; their integration into one optimizer step is the unattacked frontier the WAM Survey names.

#### Current state of evidence

**Single-loop co-training papers (closest existing work):**
- [[2603.19370|VAMPO]] — Re-frames video denoising as MDP, applies GRPO over denoising-as-MDP with latent-consistency reward — joint but operates in pixel space, expensive.
- [[2602.13977|WoVR]] — Masked GRPO + KIR + PACE in RLinf — explicit co-evolution, but PACE not shipped in code.
- [[2511.09515|WMPO]] — On-policy GRPO in imagination, but WM is frozen during inner GRPO (joint co-evolution lives in outer lifelong loop only).
- [[2511.15605|SRPO]] — Frozen V-JEPA-2 latent WM; the cleanest *latent-space* attempt but the WM doesn't update at all.

**The convergence pattern** ([[03_VLA]] §5 + [[04_WAM]] §5): Latent prediction WAMs ([[2602.10098|VLA-JEPA]], [[2602.11832|JEPA-VLA]], [[2605.00078|Being-H0.7]]) achieve VLA-level speed because they predict in 256-dim embedding space (~10ms) rather than 256×256×3 pixel space (~150ms). A joint co-training loop in this latent space is computationally feasible *and* could close the WM-vs-VLA latency gap.

#### Concrete sub-problems

1. **Unified GRPO formulation in latent space.** Concretely: given a frozen pretrained latent WAM ([[2504.02792|UWM]] or [[2602.10098|VLA-JEPA]]), define a single advantage-weighted log-prob loss $\mathcal{L} = \mathbb{E}[A \cdot \log \pi(a, \hat{z}_{t+1} | s_t)]$ where the joint policy emits both action and predicted next-state latent. Single backward pass updates both heads.
2. **Reward decomposition for joint training.** Task reward (sparse, terminal) + latent-consistency reward (does $\hat{z}_{t+1}$ match the encoder's true $z_{t+1}$?) + action-quality reward (e.g., success probability). The latent-consistency reward provides the dense signal that scalar RL alone cannot.
3. **Knowledge insulation in joint loops.** [[2505.23705|Knowledge Insulation VLA]] showed stop-gradient from action expert to VLM backbone preserves visual representations during RL. In a joint loop, stop-gradient from action gradients to the WM encoder is the natural extension — preserving the WM's pretrained physics priors.
4. **Failure-finder co-evolution.** A [[2412.02818|RoboMD]]-style failure-finder modified to GRPO could select adversarial perturbations in the same optimizer step, providing an automatic curriculum. The open question is whether the failure-finder needs its own advantage signal or can share the main policy's — and how to regret-align the finder's reward so it surfaces *informative* failures, not pathological ones.
5. **Real-robot transfer**. Most existing self-evolving methods (EvoAgent, SPIRAL) operate in simulation. The joint latent loop needs to demonstrate transfer — using only the deployed policy (LoRA on frozen WM base) on real hardware, since both the WM and failure-finder are sim-only.

#### Related papers

- [[2602.12063|VLAW]] — Iterative VLA+WM co-improvement; the alternating baseline to beat
- [[2603.19370|VAMPO]] — GRPO over video-denoising-as-MDP; pixel-space precedent for joint RL
- [[2511.09515|WMPO]] — WM-PO with inner-loop frozen WM; the closest single-loop attempt
- [[2511.15605|SRPO]] — Frozen V-JEPA-2 latent WM + trajectory clustering reward
- [[2605.15153|Pelican-Unified]] — Single-model unification of understanding+reasoning+imagination+action via shared latent z; **64.7** VLM avg, **93.5%** RoboTwin, **1st** WorldArena — the architectural target
- [[2605.10942|HarmoWAM]] — Dual predictive+reactive experts with process-adaptive gating; **89%** in-domain, only **−7.9%** OOD drop
- [[2602.10098|VLA-JEPA]] / [[2602.11832|JEPA-VLA]] / [[2605.00078|Being-H0.7]] — Latent prediction backbones suitable as joint-loop substrates
- [[2504.02792|UWM]] — Unified World Models; single architecture for action-conditioned + action-free + video prediction
- [[2505.23705|Knowledge Insulation VLA]] — Stop-gradient pattern for preserving backbone during RL

#### Benchmark coverage

**Existing**: [[2306.03310|LIBERO]] (basic), [[2510.13626|LIBERO-Plus]] (visual robustness), [[2602.06556|LIBERO-X]] (cross-task), [[2603.28301|LIBERO-Para]] (instruction paraphrase).
**Gap**: No benchmark specifically measures *whether joint training delivers gains over alternating training* on the same backbone. A joint-vs-alternating ablation grid on a fixed backbone (UWM or Cosmos Policy) would be the first.

#### Risk / what could fizzle

- **Optimization instability**: Joint losses over discrete action + continuous latent + adversarial failure-finder can have conflicting gradient directions. Careful reward scaling, gradient-norm balancing, and per-head learning-rate tuning are the standard mitigations — none guaranteed to suffice.
- **The "chasing" problem**: When both networks update simultaneously, the WM models an obsolete policy. Mitigation: small per-step updates with EMA target networks.
- **Insufficient signal**: The latent-consistency reward may be too dense for sample-efficient learning if it dominates the task reward.
- **Reward hacking on the latent-consistency term**: Easy to hack by collapsing the latent space. [[2511.08544|LeJEPA]]'s Euclidean latent-geometry regularization is the obvious defense; [[2604.27998|Latent-GRPO]]'s three failure-mode patches are also relevant.
### Direction 4 — Causally-Important Step Rewards for Latent VLA Reasoning

**Thesis.** Combine [[2604.18486|OneVL]]-style latent reasoning (answer-only latency) with [[2604.22074|CIR/SR Reasoning]]-style step rewards (causally important reasoning) — closing the "outcome rewards alone don't guarantee causal reasoning" gap at the cost of training-time supervision only.

#### Why it matters

The most surprising recent VLA reasoning result is [[2604.22074|CIR/SR Reasoning]]'s finding that **outcome rewards alone are insufficient** — RL-trained reasoning VLAs develop traces that are "factually correct via reasoning paths that aren't causally connected to the answer." Combined with [[2604.18486|OneVL]]'s demonstration that **latent reasoning beats explicit CoT** at answer-only latency (**88.84** PDM-score on NAVSIM, **+2.64 pts** over prior 8B models), and [[2510.16281|SEAL]]'s documentation of the CoT-faithfulness gap (reasoning VLAs generate sensible plans but execute inconsistent actions under OOD), the field is converging on a clear unsolved problem: **how to train latent reasoning to be causally faithful, not just outcome-correct.** [[2509.19012|Pure VLA Survey]] reinforces this — it lists "causal reasoning" alongside "world modeling" as the two opportunities to bridge the perception-understanding-action gap; [[2510.04978|Physical AI Survey]] generalizes the same gap to all of Physical AI: "AI models primarily learn statistical correlations, lacking genuine causal physical understanding."

#### Current state of evidence

The relevant works are all very recent:
- [[2604.18486|OneVL]] — Dual-decoder latent CoT: answer-only latency beats explicit CoT
- [[2604.22709|Abstract-CoT]] — Pre-allocated K reasoning tokens; token-free CoT
- [[2604.28192|LaST-R1]] — Adaptive physical latent reasoning + RL with task-success reward
- [[2604.27998|Latent-GRPO]] — GRPO stabilization for latent reasoning (3 failure-mode patches)
- [[2604.20328|HyLaR]] — vMF distribution + decoupled clipping for hybrid discrete-continuous latent reasoning
- [[2605.02735|Silenced Visual Latents]] — Diagnostic: latent reasoning can be **semantically rich but functionally ignored** during answer prediction
- [[2604.22074|CIR/SR Reasoning]] — Outcome rewards don't guarantee causal reasoning; needs Causally Important Reasoning + Step-Reward supervision
- [[2509.25852|REVER]] — Reinforced embodied planning with verifiable rewards
- [[2604.21396|VG-CoT]] — Grounded CoT tied to visual evidence

What's missing: **No paper combines latent CoT + step-reward training for VLA reasoning**. CIR/SR works on language outcomes (text-based reasoning), not VLA action sequences. Closing this gap requires:
1. A latent CoT architecture that exposes intermediate reasoning steps for supervision (OneVL's dual decoders work)
2. A step-level causal-importance reward that operates on action sequences (CIR/SR's predicate-checking generalized to physical state changes)
3. RL stabilization that doesn't collapse latent diversity ([[2604.27998|Latent-GRPO]]'s three patches + [[2509.15194|EVOL-RL]]'s novelty diversity)

#### Concrete sub-problems

1. **Causal-importance predicates for manipulation.** CIR/SR's text-domain predicates ("is fact F entailed by step S_i?") need physical analogs: "does intermediate state S_i achieve subgoal G_i?" **Concrete pipeline**: decompose all 130 [[2306.03310|LIBERO]] tasks into 3-7 verifiable subgoals each (~600-900 subgoals total); auto-generate predicates via [[2503.15558|Cosmos-Reason1]] as LLM-as-judge, then validate with a 100-subgoal human-labeled gold set targeting **inter-annotator agreement κ > 0.7**. **Deliverable**: LIBERO-Subgoals annotation set + predicate code. **Baseline to beat**: [[2510.16281|SEAL]]'s post-hoc VLM critic (which scores plan-action alignment but doesn't supervise training).
2. **Step-reward training on latent reasoning tokens.** Architecture: take [[2604.18486|OneVL]]'s dual auxiliary decoders (D_text + D_action), expose the K=8 latent reasoning tokens during training. Loss: $\mathcal{L} = \lambda_a \mathcal{L}_{\text{action}} + \lambda_s \sum_i r_{\text{step},i}(z_i)$ where $r_{\text{step},i}$ is the verifiable subgoal predicate evaluated on the decoded intermediate state. **Hyperparameters** (starting point from [[2604.27998|Latent-GRPO]]): $\lambda_a=1.0$, $\lambda_s \in \{0.1, 0.3, 1.0\}$, K=8 latent tokens, clip ratio 0.2. **Baselines**: vanilla OneVL (no step rewards), [[2604.18486|OneVL]] + outcome-only RL, explicit CoT VLAs ([[2503.22020|CoT-VLA]]). **Target**: ≥**+5 pp** SR on LIBERO-Long over vanilla OneVL at matched inference latency.
3. **Latent utilization probing as gating diagnostic.** [[2605.02735|Silenced Visual Latents]]'s diagnostic must run before claiming success. **Metric**: action $L_2$ distance between original-latent prediction $a(\mathbf{z})$ and Gaussian-noise-perturbed latent $a(\mathbf{z}+\epsilon)$, normalized by action variance — call it the *Latent Utilization Index* (LUI). **Pass threshold**: LUI > 0.3 (matches Silenced Visual Latents' "active latent" regime). **Failure mode**: LUI ≈ 0 means model has learned the "shortcut pathology" — answer head ignores reasoning tokens.
4. **Compositional step rewards on benchmarks.** [[2510.16281|SEAL]]'s **+15pp** improvement is specifically on novel compositional tasks. **Concrete benchmark**: [[2603.28301|LIBERO-Para]] (instruction paraphrase, 130×K paraphrases) + [[2510.13626|LIBERO-Plus]] (10,030 perturbations) + [[2507.10548|EmbRACE-3K]] (3K embodied reasoning episodes). **Compositional split protocol**: train on simple-instruction tasks, test on compositions of seen primitives (e.g., "open drawer + place red mug inside"). **Target**: ≥**+10 pp** on compositional split, ≤**−3 pp** on in-distribution split. **Baselines**: OneVL (no step rewards), VG-CoT (visually-grounded CoT), CoT-VLA (explicit CoT).
5. **Inference cost ablation.** **Concrete sweep**: explicit CoT (~120ms/token, ~10 tokens = ~1.2s) vs Abstract-CoT (~50ms) vs OneVL (~0ms) vs OneVL+CIR/SR (~0ms). **Test set**: LIBERO-Para + LIBERO-Plus + EmbRACE-3K. **Cost metric**: end-to-end latency on a single A100, 224×224 image. **Result table**: 4 methods × 3 benchmarks × {ID, OOD, Compositional} = 36 cells. **Headline finding to validate**: OneVL+CIR/SR achieves OneVL's latency at ≥SEAL's robustness.

#### Related papers

- [[2604.18486|OneVL]] — Latent CoT > explicit CoT at answer-only latency; the architectural template
- [[2604.22074|CIR/SR Reasoning]] — Outcome reward insufficient; step rewards needed for causal reasoning
- [[2604.27998|Latent-GRPO]] — RL stabilization for continuous latent reasoning
- [[2510.16281|SEAL]] — Runtime CoT faithfulness verifier; +15pp on novel compositional tasks
- [[2604.21396|VG-CoT]] — Grounded CoT tied to visual evidence (the visual-domain analog of step rewards)
- [[2509.25852|REVER]] — Reinforced embodied planning with verifiable rewards
- [[2605.02735|Silenced Visual Latents]] — Diagnostic for latent utilization (must accompany any latent-reasoning paper)
- [[2503.15558|Cosmos-Reason1]] — Physical commonsense + embodied reasoning; complementary substrate

#### Benchmark coverage

**Existing**: NAVSIM (driving CoT), [[2510.13626|LIBERO-Plus]] (visual robustness), [[2603.28301|LIBERO-Para]] (instruction paraphrase), [[2507.10548|EmbRACE-3K]] (embodied reasoning).
**Gap**: No benchmark specifically tests **causal faithfulness of latent reasoning to action sequences** under compositional novelty. The benchmark proposed here would be the first.

#### Risk / what could fizzle

- **Predicate scaling**: Hand-authoring subgoal predicates for hundreds of tasks is brittle. Use LLM-as-judge as a fallback, but this re-introduces the verification cost CIR/SR was trying to avoid.
- **Reward hacking**: Models can learn to satisfy step predicates trivially. Mitigation: novelty-based diversity ([[2509.15194|EVOL-RL]]).
- **Compositional generalization is unsolved**: Even if step rewards work on training tasks, they may not transfer to compositional novelty — the exact failure mode SEAL documented.
### Direction 5 — Verifiable Physics-Consistent Training for Open-World VLA Generation

**Thesis.** Bridge the [[2604.04974|Video-to-Control Survey]]'s identified "robotics integration layer" gap — connecting physics-aligned video generation ([[2509.21309|NewtonGen]], [[2509.20570|PIRF]], [[2512.00425|NewtonRewards]]) to deployable robot behavior — by training VLAs with verifiable physics rewards applied at the *action* level, not just the video-generation level.

#### Why it matters

The Video-to-Control Survey explicitly identifies this as **the critical unresolved gap**: "Different interface designs—implicit (direct policies), abstract (latent actions), or explicit (visual targets)—present distinct trade-offs in transparency, physical consistency, and robustness." Four other surveys converge on the same diagnostic: [[2503.21765|Physics Cognition Survey]] documents that "even state-of-the-art video generation models fall short of human-level physics understanding" via its three-tier cognitive taxonomy; [[2510.04978|Physical AI Survey]] names the entire problem class — "causal physical understanding missing across perception/reasoning/modeling/interaction"; [[2601.15533|Actionable Simulators]] calls the failure mode "dynamical hallucinations" and demands physical anchoring + closed-loop evaluation; [[2601.07823|Video Generation in Robotics Survey]] enumerates 10 challenges including hallucinations and physics violations as top-2. The wave of physics-aware video generators ([[2509.21309|NewtonGen]], [[2510.13809|PhysMaster]], [[2512.00425|NewtonRewards]], [[2603.13770|PhysAlign]]) made enormous progress on the *generation* side — Sora-class models now produce physics-consistent video with explicit verifiable rewards. But none of these have been tested for *deployment* — does the physics-consistency of the imagination actually transfer to physics-consistent robot actions?

The [[2604.17896|Physical-Feasibility VLA]] paper is the closest existing attempt: differentiable geometric feasibility loss on VLA actions, raising SSR from **22% → 43.50%** under small perturbations. But geometric feasibility is a tiny slice of physics (just collision avoidance) — Newton's laws are not enforced.

#### Current state of evidence

- **Video-side**: [[2509.20570|PIRF]] (PDE residual rewards), [[2509.21309|NewtonGen]] (neural Newtonian dynamics in T2V), [[2512.00425|NewtonRewards]] (RL with verifiable physics rewards), [[2510.13809|PhysMaster]] (RL fine-tuning of video diffusion), [[2603.13770|PhysAlign]] (feature + 3D-rep alignment), [[2603.26285|PhysVid]] (physics-aware local conditioning).
- **VLA-side**: [[2604.17896|Physical-Feasibility VLA]] (geometric feasibility on actions), [[2503.15558|Cosmos-Reason1]] (physical commonsense + embodied reasoning at WAM scale), [[2511.07416|PhysWorld]] (policy trained against learned physical world model), [[2605.06593|ReActor]] (bilevel RL + physics simulation for motion retargeting).
- **Bridge**: [[2603.23376|ABot-PhysWorld]] uses Diffusion-DPO with physics-rejected negatives — suppresses object penetration / anti-gravity outputs. This is the closest existing physics-on-WAM-on-VLA bridge.

What's missing: **A unified training recipe that applies verifiable physics rewards at the action level** while the WM provides the imagination. The Video-to-Control Survey's "interface design" question is the right framing — three interface designs need head-to-head evaluation under physics-verifiable rewards.

#### Concrete sub-problems

1. **Physics predicates over robot action sequences.** **Predicate set** (each yields a binary verifiable reward, computed in MuJoCo/Isaac Sim):
   - **P1 — momentum conservation**: $|\Delta p_{\text{total}}| < 0.05 \cdot p_{\max}$ over a 1s window (excluding contact frames)
   - **P2 — no inter-object penetration**: signed-distance > 0 for all object pairs at every timestep
   - **P3 — no anti-gravity motion**: free-flight phase Δz consistent with $-\frac{1}{2}gt^2$ within ±10% tolerance
   - **P4 — contact-force consistency**: Newton's 3rd law check, $|F_{a \to b} + F_{b \to a}| / |F_{a \to b}| < 0.1$
   - **P5 — Coulomb friction bound**: $|F_{\text{tangential}}| \leq \mu |F_{\text{normal}}|$ where $\mu$ comes from the asset metadata.
   **Dataset**: instrument 50 [[2306.03310|LIBERO]] tasks + 30 [[2502.16707|RoboMamba]] long-horizon tasks, ~50 rollouts each = ~4,000 trajectories with per-step predicate labels. **Deliverable**: an open `physics-predicates` package + benchmark labels.
2. **Three-way ablation: implicit vs abstract vs explicit interfaces** (per [[2604.04974|Video-to-Control Survey]]'s taxonomy). Same backbone [[2504.02792|UWM]] or [[2602.10098|VLA-JEPA]], three variants matched on FLOPs:
   - **Implicit**: physics reward $\sum_i w_i P_i$ applied to action output only ([[2604.17896|Physical-Feasibility VLA]] pattern extended from P2 alone to all 5 predicates)
   - **Abstract**: physics-residual loss applied to latent prediction ([[2511.08544|LeJEPA]]'s Euclidean latent regularization + a learned linear physics-readout head trained to predict predicate satisfaction from latents)
   - **Explicit**: physics reward applied to predicted visual subgoal ([[2503.22020|CoT-VLA]]'s subgoal output, scored via [[2509.21309|NewtonGen]]-style PDE residual on optical-flow-extracted dynamics).
   **Headline metric**: SSR (subgoal success rate) on LIBERO-Plus + a 20-task physics-violation gauntlet drawn from [[2410.05363|PhyGenBench]] paradigms. **Target**: implicit Physical-Feasibility VLA goes from **43.50%** (geometric-only) to **>55%** SSR; latent variant should match within ±2pp at lower latency.
3. **Open-world test via [[2603.23376|ABot-PhysWorld]] negatives.** **Concrete protocol**: ABot's physics-rejected counterfactuals (object penetration + anti-gravity motion) give ~10k preference pairs; train Diffusion-DPO on these. **Pass criterion**: post-training, score gap $\beta(\log p_{\theta}(a_+) - \log p_{\theta}(a_-)) > 0$ on a held-out 1,000-pair test set with ≥90% accuracy. **Baseline**: WAM-only physics-DPO (no action-side rejection) ABot reports at ~74%.
4. **Sim-to-real validation.** [[2511.04665|Real-to-Sim GS]] provides Gaussian-splat soft-body twins for 12 cloth/rope/dough tasks. **Transfer chain protocol**: train policy in sim with physics rewards; eval on (a) sim, (b) GS-twin (high-fidelity rendering, learned dynamics), (c) real robot at single physical lab. **Metric**: SR retention = SR_real / SR_sim. **Target**: ≥**0.70** retention (current physics-naive policies typically retain 0.50-0.60).
5. **Reward hacking diagnostics.** **Three diagnostic checks** before claiming success:
   - **D1 — static-output detection**: if action variance σ over a task drops >2× compared to the imitation-only baseline, flag as hack (model is freezing).
   - **D2 — predicate-vs-task-success regression**: track $\rho(\sum P_i, \text{task SR})$ over training. If ρ drops over time (model gaming predicates without improving task), apply layer-wise truncation ([[2509.20570|PIRF]] pattern).
   - **D3 — adversarial probing**: every 1k training steps run [[2412.02818|RoboMD]]'s failure-finder on the current policy; if it finds a >10% drop perturbation, fold those examples back into training.
   **Defense stack**: novelty diversity ([[2509.15194|EVOL-RL]]) prevents collapse; per-task adversarial probing prevents distributional gaming.

#### Related papers

- [[2604.04974|Video-to-Control Survey]] — Names the gap; the canonical reference
- [[2604.17896|Physical-Feasibility VLA]] — Geometric feasibility loss on actions; the closest existing work
- [[2603.23376|ABot-PhysWorld]] — Diffusion-DPO with physics-rejected negatives; suppression mechanism
- [[2509.21309|NewtonGen]] / [[2512.00425|NewtonRewards]] / [[2509.20570|PIRF]] / [[2510.13809|PhysMaster]] / [[2603.13770|PhysAlign]] — The video-side foundation
- [[2503.15558|Cosmos-Reason1]] — Physics-aware reasoning; complementary to physics-aware action
- [[2511.07416|PhysWorld]] — Policy against learned physical WM
- [[2605.06593|ReActor]] — Bilevel RL + physics sim for motion retargeting
- [[2511.04665|Real-to-Sim GS]] — Sim-to-real for physics-aware policies on soft body

#### Benchmark coverage

**Existing**: [[2410.05363|PhyGenBench]], [[2503.06800|VideoPhy-2]], [[2501.09038|Physics-IQ]], [[2504.02918|Morpheus]] (all measure video-generation physics quality). [[2509.07962|TA-VLA]] (torque-aware design study).
**Gap**: No benchmark scores **physics-consistency of VLA action sequences** against a verifiable simulator ground truth. A new benchmark with adversarial physics-violating tasks (e.g., "stack blocks against gravity") would expose this.

#### Risk / what could fizzle

- **Verifiable physics scales poorly** ([[2509.20570|PIRF]]'s open problem): writing predicates for cluttered kitchens is hard. Mitigation: learned physics verifiers — but those generalize poorly.
- **Physics-consistent imagination doesn't imply physics-consistent action**: even if the WM predicts correct physics, the action head might not respect them. This is exactly the gap to test, but if it's *only* small, the direction collapses.
- **Reward hacking**: NewtonRewards already documented this on the generation side. The action-side analog (model "freezes" to game the conservation predicates) is a likely failure mode.

---

## Cluster III — Evaluation, Robustness & Deployment

*What the model does in the world.* These three directions close the lab-to-deployment loop — measuring whether the cluster-II gains are real (joint causal-consistency), surviving failures over long horizons (memory + recovery), and fitting the real-time compute budget that deployment demands.
### Direction 6 — Joint VLA/WAM Evaluation: Causal Consistency Between Imagination and Action

**Thesis.** Build the first standardized benchmark suite that jointly measures whether a WAM's *imagined future* actually matches the *action it then takes* — closing the dominant evaluation gap identified by both major WAM surveys.

#### Why it matters

Five surveys now flag the same problem: [[2605.12090|WAM Survey]], [[2605.00080|WM Robot Survey 2026]], [[2510.16732|World Models for Embodied AI Survey]], [[2601.15533|Actionable Simulators]], and [[2601.07823|Video Generation in Robotics Survey]] independently call out that current evaluation protocols measure world-modeling quality (FVD, PSNR, prediction error) and action-policy quality (LIBERO success rate) **separately**. The World Models for Embodied AI Survey explicitly names "physically-consistent metrics beyond FID/FVD" as an open problem; Actionable Simulators calls it "dynamical hallucinations" and demands closed-loop decision-oriented evaluation; the alphaxiv-verified WAM Survey adds "absence of joint metrics establishing causal linkage between predicted futures and executed actions" as its evaluation open problem. A WAM can score high on each axis while its imagination and actions are causally disconnected. The "CoT faithfulness gap" identified by [[2510.16281|SEAL]] for reasoning VLAs is exactly this problem one level down. The deeper objective-mismatch framing ([[2310.06253|Objective-Mismatch Survey]]) provides the MBRL substrate: predictive WM loss is well-known to fail to correlate with downstream return.

[[2603.22078|WAM vs VLA Robustness]] showed WAMs outperform VLAs on visual perturbations *but are 4.8x slower* — the speed cost would only be worth paying if the imagination actually helps action quality, which current metrics cannot certify.

#### Current state of evidence

- [[2603.22212|Omni-WorldBench]] is the first interaction-centric evaluation, testing causal consistency via counterfactual action probes — but it tests world models in isolation, not in their downstream VLA role.
- [[2506.00613|WorldGym]] takes a step further: it evaluates by training policies *inside* the world model and measuring downstream transfer — closer to the joint metric needed but limited to specific game-style environments.
- [[2510.10125|CTRL-WORLD]] provides controllability evaluation infrastructure for robot manipulation.
- [[2603.23497|WildWorld]] introduced Action Following + State Alignment metrics on 108M frames from Monster Hunter — concrete metric definitions exist but haven't been generalized to manipulation.
- [[2510.16281|SEAL]] is the closest *runtime* attempt — verifying semantic alignment between predicted outcomes and the VLA's text plan — but it's a verifier, not a benchmark.

What's missing: a **standardized, manipulation-oriented joint metric** that scores `corr(imagined_outcome, achieved_outcome | action)` across a diagnostic task suite.

#### Concrete sub-problems

1. **Define a causal-consistency metric for action-conditioned imagination.** Concretely: given $(s_t, a_t)$, the model outputs imagined $\hat{s}_{t+1}$ and executes $a_t$ yielding observed $s_{t+1}$. **Metric**: [[2304.07193|DINOv2]] (ViT-L/14) cosine similarity between $\hat{s}_{t+1}$ and $s_{t+1}$, augmented with a counterfactual probe — sample $a'_t \sim \pi$, generate $\hat{s}'_{t+1}$, and require the divergence $\|\hat{s}_{t+1} - \hat{s}'_{t+1}\|$ to scale monotonically with $\|a_t - a'_t\|$. **Target baselines to beat**: [[2603.22212|Omni-WorldBench]] (interaction-centric WM eval) and [[2510.10125|CTRL-WORLD]] (controllability) — both score WM in isolation. **Deliverable**: 1 metric definition + reference implementation that runs on the [[2603.13966|vla-eval]] harness.
2. **Build a 50-100 task diagnostic suite** layered on top of [[2306.03310|LIBERO]] (4 task suites, 130 tasks) + [[2510.13626|LIBERO-Plus]] (10,030 perturbed variants) + [[2603.28301|LIBERO-Para]] (instruction paraphrases). Each task instrumented to record (predicted_state, achieved_state, action) triples at every step. **Target scale**: 50 tasks × 100 rollouts × 8 timesteps = 40,000 (predict, achieve) pairs per WAM. **Existing closest**: [[2603.23497|WildWorld]]'s Action Following + State Alignment metrics on 108M Monster Hunter frames — adapt to manipulation. **Deliverable**: LIBERO-Causal benchmark + ~40k-rollout reference dataset.
3. **Decompose WAM utility into 3 sub-scores per [[2604.22748|Agentic World Modeling Survey]]'s L1 Predictor / L2 Simulator / L3 Evolver hierarchy.** (a) **L1 Predictor local-prediction accuracy**: 1-step MSE in DINOv2 feature space — target retention >90% of [[2510.10125|CTRL-WORLD]]'s controllability metric. (b) **L2 Simulator multi-step rollout consistency**: cumulative drift over 8 steps — target <2x linear growth; aligns with the survey's "long-horizon coherence" boundary condition. (c) **L3 Evolver action-causal counterfactual accuracy**: instantiate the survey's proposed COD (Counterfactual Outcome Deviation) metric as AUROC of "swapped-action detection" — score 0.5 = no causal binding (chance), 1.0 = perfect causal binding. Pair with the survey's ASR (Action Success Rate) for the action-side anchor. Baselines: [[2603.22078|WAM vs VLA Robustness]] (currently no L3 score reported), [[2602.10098|VLA-JEPA]], [[2511.15605|SRPO]] (frozen V-JEPA-2).
4. **Quantify the speed-quality Pareto frontier.** Re-run [[2603.22078|WAM vs VLA Robustness]]'s WAM-vs-VLA grid (~12 model configs) with the new joint metric. **Specific question**: does WAM augmentation's 4.8x latency cost translate to ≥X percentage-point improvement on the L3 counterfactual metric? Threshold X to be determined empirically. **Baselines**: π0, [[2412.14058|RoboVLMs]], [[2411.19650|CogACT]], [[2504.02792|UWM]].
5. **Add a "deployment readiness" axis.** Cross-reference [[2506.18123|RoboArena]] real-robot scores (8 robot platforms, ~120 tasks) with the joint metric. **Concrete test**: does the joint metric predict RoboArena real-world SR with Spearman ρ > 0.7? Separate sub-scores (FVD-only, LIBERO-only) currently achieve ρ < 0.4 per published RoboArena leaderboard. **Deliverable**: a regression analysis paper + open metric leaderboard with [[2602.06556|LIBERO-X]] cross-task slot.

#### Related papers

- [[2603.22212|Omni-WorldBench]] — Interaction-centric WM eval; the conceptual parent for a manipulation-oriented benchmark
- [[2506.00613|WorldGym]] — World-model-as-environment; the policy-fidelity-via-WM evaluation primitive
- [[2510.10125|CTRL-WORLD]] — Controllable WM evaluation harness
- [[2603.22078|WAM vs VLA Robustness]] — The systematic WAM-vs-VLA comparison that documented the 4.8x latency cost
- [[2510.16281|SEAL]] — Runtime alignment verifier (training-free K-candidate verification via VLM critic)
- [[2603.13966|vla-eval]] — Unified eval harness; 47x LIBERO speedup; the technical substrate for adding new metrics

#### Benchmark coverage

**Existing**: LIBERO + LIBERO-Plus (action), Omni-WorldBench + WildWorld (WM in isolation), WorldGym (WM-as-env), RoboArena (real fleet).
**Gap**: No benchmark currently scores `joint(WM_quality, action_quality, causal_consistency)` on a single task set. The benchmark proposed here would be the first.

#### Risk / what could fizzle

- **Metric noise**: Learned similarity scores in feature space are themselves trained — embedding the same blind spots they measure. Mitigation: pair learned similarity with explicit physical predicates (e.g., did the cup move?) where possible.
- **Sample size for counterfactual probes**: Each task may need 100+ rollouts per metric instance to get statistically stable causal scores.
- **Selection bias**: If the benchmark is built around current WAMs, it may flatter the architectures that match its assumptions. Mitigation: include adversarial WAM examples ([[2604.05498|JailWAM]]) and physics-violating baselines ([[2603.23376|ABot-PhysWorld]]'s rejected outputs).
### Direction 7 — Long-Horizon Memory + Failure Recovery Loops for Real-World Deployment

**Thesis.** Combine the long-horizon memory architectures ([[2605.10993|ECHO-VLA]], [[2508.19236|MemoryVLA]], [[2603.03596|MEM]]) with the proactive failure-recovery mechanisms ([[2601.02295|CycleVLA]], [[2512.24426|CF-VLA]], [[2509.04018|FPC-VLA]]) into a unified deployment loop — addressing the most-cited deployment gap.

#### Why it matters

Two open problems converge here:
- **The long-horizon memory gap** ([[2605.10921|RoboMemArena]]): "**68.9%** of subtasks genuinely require historical information; current VLAs collapse on memory-dependent tasks." The benchmark is recent and no method has been systematically evaluated on it yet. [[2505.07634|Neural Brain Framework]] generalizes this — its 4-component architecture lists "neuroplasticity-driven memory with consolidation" as a top-tier requirement for embodied agents. [[2604.16592|Cognition WM Survey]] (alphaxiv-verified) hits the same gap from the cognitive-architecture side: among the 7 CAT cognitive functions it taxonomizes (memory / perception / language / reasoning / imagining / motivation / meta-cognition), **meta-cognition** — "self-monitoring, self-evaluation, and self-control of internal computations" — is explicitly identified as one of two "drastically under-researched" functions. Failure detection + recovery *is* the embodied operationalization of meta-cognition; building it bridges the survey's named gap.
- **The failure-recovery gap** ([[06_Self-Evolving-VLA-WAM]] §4): Detection, diagnosis, and recovery are documented in isolation, but no published deployment loop integrates them end-to-end. [[2602.04411|Self-evolving Embodied AI]] provides the canonical decomposition — 5 co-evolving modules including **memory self-updating** and **model self-evolution** — that Direction 7's deployment loop instantiates. [[2505.05108|Multi-agent Embodied AI Survey]] adds that "self-evolution in open environments" remains the top unresolved capability gap. [[2508.07407|Self-Evolving AI Agents Survey]] and [[2507.21046|Self-Evolving Agents Survey]] further break down the "When/How/Where to Evolve" framework, naming **adaptivity, retention, generalization, efficiency, safety** as the five canonical evaluation gaps.

These two are linked: failure recovery *requires* memory ("did I already try this approach?"). [[2605.10993|ECHO-VLA]] is the closest existing attempt — hierarchical hyperbolic memory + autonomous memory consolidation, **+12.8pp** on LIBERO-Long — but it doesn't integrate failure detection.

This direction is the natural pre-deployment layer for any VLA aiming at real-world long-horizon tasks: detection, diagnosis, and recovery are documented individually but no published deployment loop integrates them with the memory substrate that makes recovery decisions actually trustworthy.

#### Current state of evidence

**Memory architectures:**
- [[2605.10993|ECHO-VLA]] — Hierarchical hyperbolic memory; **+12.8pp** LIBERO-Long
- [[2508.19236|MemoryVLA]] — Bio-inspired dual-memory PCMB; **+26pp** on long-horizon temporal tasks, only +3.6% latency
- [[2603.03596|MEM]] — Dense short-term + compressed long-term LLM summaries; up to 15-minute memory
- [[2603.12942|ReMem-VLA]] — Dual-level recurrent queries; 94.5% on memory-dependent simulation

**Failure detection** (8 complementary methods documented in [[06_Self-Evolving-VLA-WAM]] §4.1):
- [[2506.09937|SAFE]] (internal feature monitoring + conformal prediction)
- [[2509.16072|I-FailSense]] (semantic misalignment via VLM)
- [[2510.09459|FIPER]] (predictive failure via OOD + action uncertainty)
- [[2603.11106|RC-NF]] (density-based OOD via normalizing flows, <100ms)
- [[2503.08558|FAIL-Detect]] (logpZO flow + Conformal Prediction, 78% accuracy without failure data)
- [[2410.04640|Sentinel]] (STAC + VLM ensemble, +18% over single detectors)
- [[2407.08735|AESOP]] (fast embedding + slow LLM, 100% recovery in simulation)
- [[2510.02298|ARMADA]] (FLOAT detector, 95% accuracy, 23.3% reduction in human intervention)

**Proactive correction:**
- [[2601.02295|CycleVLA]] — Subtask backtracking with MBR decoding
- [[2512.24426|CF-VLA]] — Counterfactual reasoning
- [[2604.02965|SV-VLA]] — Speculative verification
- [[2511.14148|AsyncVLA]] — Confidence-based async re-planning
- [[2509.04018|FPC-VLA]] — Failure prediction + corrective action in single model

**Recovery:**
- [[2505.12224|RoboFAC]] — Full failure-analysis + correction framework
- [[2603.13528|Counterfactual Failure Synthesis]] — Generative recovery plans

What's missing: **No paper integrates memory + detection + correction + recovery into a single deployment loop on a long-horizon real-world benchmark**. The components exist; the integration doesn't.

#### Concrete sub-problems

1. **Memory-grounded failure detection.** Use ECHO-VLA / MemoryVLA hierarchical memory to detect failures that require *historical* context — "I've tried this 3 times already" or "this state was wrong last episode." Stack-based detection should outperform single-frame detection on RoboMemArena tasks.
2. **Recovery with memory.** When CycleVLA backtracks, the recovery path should consult memory — don't re-try the failed approach. The memory bank becomes a *failure exclusion buffer*.
3. **Real-world deployment loop architecture.** A stack: (a) memory layer (PCMB / hierarchical hyperbolic), (b) parallel detectors (SAFE + I-FailSense + FIPER ensemble per [[2410.04640|Sentinel]]'s pattern), (c) corrective head (CycleVLA backtracking + CF-VLA counterfactual), (d) recovery generator ([[2603.13528|Counterfactual Failure Synthesis]] when novel failures encountered).
4. **Compute-vs-robustness trade-off.** Each component adds latency. Run an ablation grid on [[2605.10921|RoboMemArena]] + [[2510.13626|LIBERO-Plus]] + real-robot ([[2506.18123|RoboArena]]) to identify which combinations are deployable.
5. **Continual update from corrections.** Each successful recovery becomes a training example. Use [[2510.02298|ARMADA]]'s pooled-intervention pattern — multiple robots share corrective demos.

#### Related papers

- [[2605.10921|RoboMemArena]] — First comprehensive memory benchmark; the evaluation target
- [[2605.10993|ECHO-VLA]] — Hierarchical hyperbolic memory; **+12.8pp** LIBERO-Long
- [[2508.19236|MemoryVLA]] — PCMB dual-memory; **+26pp** with +3.6% latency
- [[2510.09459|FIPER]] / [[2506.09937|SAFE]] / [[2410.04640|Sentinel]] / [[2603.11106|RC-NF]] — The detector arsenal
- [[2601.02295|CycleVLA]] / [[2512.24426|CF-VLA]] / [[2509.04018|FPC-VLA]] — Proactive correction
- [[2505.12224|RoboFAC]] / [[2603.13528|Counterfactual Failure Synthesis]] — Recovery generators
- [[2510.02298|ARMADA]] — Human-shared-control scaling with FLOAT detection

#### Benchmark coverage

**Existing**: [[2605.10921|RoboMemArena]] (memory-dependent tasks), LIBERO/LIBERO-Plus/LIBERO-PRO (visual robustness), [[2506.18123|RoboArena]] (real fleet). [[2502.09560|EmbodiedBench]] (capability disentangling).
**Gap**: No benchmark scores **integrated detect-diagnose-recover loops** on long-horizon tasks. The closest is RoboMemArena's memory tasks combined with LIBERO-Plus's perturbations — but they're not unified.

#### Risk / what could fizzle

- **Latency stacking**: Each component adds 10-100ms; the full loop may not be real-time. Mitigation: parallelize detectors; only invoke recovery when detection fires.
- **Component interactions**: Detectors may fire on each other's corrections, creating oscillating policies. Need careful state-machine design.
- **Memory may be irrelevant for short tasks**: If your deployment target is sub-30-second tasks, memory adds cost without benefit. The direction is fundamentally a long-horizon bet.
- **Real-robot evaluation is expensive**: Validating on [[2506.18123|RoboArena]] requires multi-lab coordination.
### Direction 8 — Real-Time-Deployable VLAs via Architectural-Algorithmic-Data Co-design

**Thesis.** Treat efficiency as a primary research target, not an optimization afterthought — build VLAs that hit ≥30 Hz control on edge hardware by co-designing the architecture (linear-attention / Mamba / parallel decoding), the training algorithm (PEFT + KD + co-training), and the data pipeline (massively-parallel sim + internet-scale human video + self-exploration) as a single system.

#### Why it matters

[[2510.24795|Efficient VLA Survey]] and [[2603.28489|Video Gen as WM Survey]] explicitly reframe **efficiency from "optimization" to "fundamental prerequisite"** for deployment. The [[2505.04769|VLA Survey]] quantified the bottleneck: "autoregressive decoding limits speed to 3–5 Hz" — far below the 20–50 Hz needed for closed-loop manipulation. [[2510.07077|VLA Robotics Review 2025]] adds that "computational latency limits real-time deployment" is a top-3 unresolved practical concern alongside data scarcity and embodiment transfer.

None of Directions 1–7 tackle efficiency as a *primary* thesis — they all implicitly assume real-time deployment is feasible. But the survey convergence is clear: efficiency is itself a frontier research problem requiring system-level co-design. The three pillars from [[2510.24795|Efficient VLA Survey]] (model design × training × data) map onto three concrete sub-problems below.

#### Current state of evidence

**Model-side efficiency:**
- Linear-time attention backbones: SARA-RT, [[2502.16707|RoboMamba]]-style Mamba architectures
- Parallel action decoding: avoids the autoregressive 3–5 Hz ceiling
- Quantization + pruning + distillation: standard but rarely co-optimized

**Training-side efficiency:**
- [[2505.23705|Knowledge Insulation VLA]] — stop-gradient PEFT preserving backbone during RL
- LoRA / adapter-based VLA fine-tuning across the OpenVLA / π0 lineage
- Mixed data co-training (egocentric + sim + robot trajectories)

**Data-side efficiency:**
- [[2602.16710|EgoScale]] — log-linear scaling on internet-scale human video, +54% on dexterous tasks
- Massively-parallel simulation: Isaac Sim / Genesis (per [[2507.00917|Embodied Intelligence Survey]])
- Self-exploration / autonomous data collection ([[2602.04411|Self-evolving Embodied AI]]'s environment-self-prediction module)

What's missing: **No paper co-designs across all three pillars simultaneously**. Efficient VLA work typically optimizes one pillar in isolation (e.g., RoboMamba changes the backbone but uses standard data); EgoScale scales data but uses a standard π0-class backbone. A unified efficiency budget — "deliver 30 Hz control on a Jetson Orin given budget $B in compute and $D in data" — has not been published.

#### Concrete sub-problems

1. **Compute-vs-control-frequency Pareto frontier.** Sweep backbone (Transformer / linear-attention / Mamba) × decoding (autoregressive / parallel / diffusion) × precision (FP16 / INT8 / INT4) on a fixed task suite ([[2306.03310|LIBERO]] + a single real-robot task). The output is a Pareto curve; the question is whether **30 Hz on edge hardware** is reachable without unacceptable success-rate loss.
2. **Knowledge-insulated RL on efficient backbones.** Take a Mamba VLA, fine-tune with [[2505.23705|Knowledge Insulation VLA]]'s stop-gradient pattern, evaluate on [[2510.13626|LIBERO-Plus]] perturbations. Test whether efficient backbones can retain RL robustness gains.
3. **Data-efficient pretraining via human-video co-training.** Combine [[2602.16710|EgoScale]] scaling with [[2510.24795|Efficient VLA Survey]]'s "mixed data co-training" recipe. Measure: how much robot-trajectory data is needed to match a baseline trained with 10x more robot data?
4. **Real-time joint VLA+WM in latent space.** Direction 3's joint loop is currently bottlenecked by WM latency. A Mamba-based latent WM ([[2511.15605|SRPO]]-style V-JEPA-2 substrate) inside the joint loop should run at >30 Hz. Verify on a fixed simulation testbed.
5. **Edge deployment chain.** Train on cluster → quantize → distill → deploy on Jetson Orin / Apple M-series. Measure end-to-end success-rate retention at each stage. This is plumbing, but no published benchmark currently measures it end-to-end.

#### Related papers

- [[2510.24795|Efficient VLA Survey]] — Names the gap; the canonical reference for the three-pillar taxonomy
- [[2603.28489|Video Gen as WM Survey]] — Three-dimensional efficiency taxonomy for video-based WMs
- [[2505.04769|VLA Survey]] — Documents the 3–5 Hz autoregressive ceiling
- [[2510.07077|VLA Robotics Review 2025]] — Names computational latency + gradient insulation + PEFT as deployment levers
- [[2502.16707|RoboMamba]] — Mamba-based efficient VLA backbone
- [[2505.23705|Knowledge Insulation VLA]] — Stop-gradient PEFT preserving backbone during RL
- [[2602.16710|EgoScale]] — Data-side scaling lever (log-linear, internet-scale)
- [[2511.15605|SRPO]] — Latent-space WM substrate (V-JEPA-2 frozen, ~10ms inference)
- [[2603.16666|Fast-WAM]] — Video at training, latent at deployment; the efficiency-pattern template
- [[2507.00917|Embodied Intelligence Survey]] — Physical-simulator landscape (Isaac/SAPIEN/Genesis) for parallel data generation

#### Benchmark coverage

**Existing**: [[2306.03310|LIBERO]] for success-rate (no latency budget), [[2603.13966|vla-eval]] for 47x simulation speedup (training-side efficiency), [[2502.09560|EmbodiedBench]] for capability disentangling.
**Gap**: No benchmark currently scores **VLA success-rate × control frequency × edge-hardware compute budget** as a single Pareto-front evaluation. A new benchmark with explicit latency budgets per task (e.g., "must hit 30 Hz on Jetson Orin") would be the first.

#### Risk / what could fizzle

- **Linear-attention / Mamba may underperform Transformers on long-context VLA tasks.** The efficiency gain only matters if success rate is retained.
- **Edge-hardware diversity** — Jetson Orin vs Apple M-series vs custom NPUs have different acceleration patterns. Cross-platform deployment may require per-platform tuning.
- **Real-time joint VLA+WM may need quantization-aware training** to stay within latency budgets; quantization-aware joint loops are uncharted.
- **Saturation risk**: if the field converges on "Mamba + LoRA + co-training" as the dominant recipe, the research contribution shrinks to engineering. Mitigation: focus on the *Pareto frontier* and *system-level* insights, not individual lever choices.

---

## Cross-cutting themes

Six themes recur across the 8 directions, suggesting they are the load-bearing technical primitives for the next 12-24 months:

1. **Latent-space prediction beats pixel-space.** Directions 3, 4, 6, 7, 8 all rely on it. The consensus from 2026 is [[2603.16666|Fast-WAM]]'s insight: video generation at training time, latent at deployment. Bet on JEPA-family or DiT-on-latent backbones, not pixel-space WAMs. The [[2510.16732|World Models for Embodied AI Survey]] taxonomy explicitly tracks this trajectory (latent vector → token sequence → explicit 3D rendering).
2. **Step-level verifiable rewards.** Directions 4, 5, 7 use them. [[2604.22074|CIR/SR Reasoning]]'s finding that outcome rewards don't guarantee causal reasoning is the most actionable result of 2026. [[2510.04978|Physical AI Survey]] generalizes this — "statistical correlations ≠ causal understanding" across all of physical AI.
3. **Egocentric pretraining as the dominant data substrate.** Directions 1, 7 (memory built from human video), 8 (data-side efficiency). The [[2602.16710|EgoScale]] log-linear scaling law is the first predictable axis for robot pretraining; [[2510.24795|Efficient VLA Survey]] confirms internet-scale human video as one of three dominant data-collection levers.
4. **Detection-diagnosis-recovery as a unified stack.** Direction 7 explicitly; Directions 3 (failure-finder), 4 (CoT faithfulness), 5 (physics violation detection) implicitly. The diagnostic stack is becoming as important as the policy. [[2602.04411|Self-evolving Embodied AI]]'s 5-module framework formalizes this.
5. **Force/tactile as a first-class modality with dedicated experts.** Directions 1, 2 explicitly. [[2505.22159|ForceVLA]] / [[2603.15169|ForceVLA2]] / [[2603.15257|HapticVLA]] established the architecture; data and cross-sensor transfer are the remaining bottlenecks.
6. **Efficiency as a prerequisite, not optimization.** Direction 8 explicitly; Directions 3, 6, 7 implicitly (joint loops, recovery loops, and memory stacks all need real-time budgets). [[2510.24795|Efficient VLA Survey]] and [[2603.28489|Video Gen as WM Survey]] both reframe efficiency from "nice to have" to "deployment-blocking". The [[2505.04769|VLA Survey]]'s 3–5 Hz ceiling diagnosis is the quantitative anchor.

---

## Benchmark gaps (consolidated)

From across the 8 directions, these benchmark gaps would enable significant progress if filled:

| Gap | Direction | Existing closest |
|---|---|---|
| Joint WM-action causal-consistency metric on manipulation | 1 | [[2603.22212\|Omni-WorldBench]] (WM-only) + [[2603.22078\|WAM vs VLA Robustness]] (separate axes) |
| Joint-vs-alternating co-training ablation on a fixed backbone | 2 | None — would be the first |
| Egocentric-only force-aware VLA evaluation | 3 | [[2505.22159\|ForceVLA]]'s 5-task set (uses real tactile) |
| Causal faithfulness of latent reasoning to actions, under compositional novelty | 4 | NAVSIM (driving CoT only) + [[2510.16281\|SEAL]] (runtime, not benchmark) |
| Physics-consistency of VLA action sequences | 5 | [[2410.05363\|PhyGenBench]] (video) + [[2604.17896\|Physical-Feasibility VLA]] (geometric only) |
| Cross-sensor tactile zero-shot transfer | 6 | TacBench (Sparsh, per-sensor) + [[2601.20321\|TaF-VLA]] (60.3% in trained families) |
| Integrated detect-diagnose-recover loops on long-horizon real tasks | 7 | [[2605.10921\|RoboMemArena]] (memory only) + [[2506.18123\|RoboArena]] (no recovery stack) |
| VLA success-rate × control-frequency × edge-compute-budget Pareto evaluation | 8 | [[2306.03310\|LIBERO]] (success only) + [[2603.13966\|vla-eval]] (training-side speedup only) |

These gaps are all addressable with current vault paper substrate plus a few hundred trajectories of data collection — none require massive scaling.

---

## Cross-References

- [[../Embodied-AI/03_VLA]] — VLA design space ([[2412.14058|RoboVLMs]] recipe, efficient/spatial/RL/force-aware/humanoid)
- [[../Embodied-AI/04_WAM]] — WAM taxonomy (VideoGen / latent / Dreamer / VLM-integrated / efficient / self-evolving)
- [[../Embodied-AI/05_Latent-World-Models]] — JEPA evolution + alternative latent models
- [[../Embodied-AI/06_Self-Evolving-VLA-WAM]] — Failure detection, diagnosis, recovery primitives
- [[../Embodied-AI/07_Physics-Aware-Embodied-AI]] — Physics-aware design space (implicit/explicit-loss/external-simulator)
- [[../Embodied-AI/08_VLA-Reasoning-and-CoT]] — Reasoning insertion slots (input/latent/output/external)
- [[../Embodied-AI/09_Egocentric-Pretraining-and-Human-Video]] — Egocentric scaling laws + transfer mechanisms
- [[../Embodied-AI/10_Force-Aware-and-Tactile-Policies]] — Force-aware VLA architectures + tactile sensors
- [[../Embodied-AI/02_Dataset-Benchmark-Environment]] — Data + sim + benchmark stacks
- [[../General/08_Benchmarks-and-Surveys]] — Canonical survey index

---

*Multi-survey enumeration covers §4 / §5 / §7 of `General/08_Benchmarks-and-Surveys.md`, with Direction 8 on real-time-deployable VLAs added after the efficiency-focused survey wave. Re-read after each major batch ingest and re-evaluate which directions remain non-saturated.*
