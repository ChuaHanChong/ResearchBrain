---
title: "Robotics & Embodied AI — Topic Overview"
tags:
  - robotics
  - VLA
  - WAM
  - embodied-AI
  - world-model
  - self-evolving
  - manipulation
aliases:
  - Robotics Overview
---

# Robotics & Embodied AI

> [!abstract] Overview
> Embodied AI sits at the convergence of all other topics: foundation models provide the backbone, VLMs provide perception, RL provides learning, and world models provide physics understanding. This note maps the landscape from VLAs through WAMs to self-evolving systems — the full path toward autonomous robots.

## Evolution Graph

```mermaid
graph TD
    subgraph "Foundations"
        A0["RT-1<br/><i>2022</i>"]
        B["Diffusion Policy<br/><i>2023</i>"]
    end

    subgraph "VLAs"
        D["RT-2<br/><i>2023</i>"]
        E["OXE / RT-X<br/><i>2023</i>"]
        F["OpenVLA<br/><i>2024</i>"]
        G["π0<br/><i>2024</i>"]
        D1["GR-1<br/><i>2023</i>"]
        D2["GR-2<br/><i>2024</i>"]
    end

    subgraph "WAMs"
        H["DreamZero<br/><i>2026</i>"]
        H1["VLAW<br/><i>2026</i>"]
        H2["VLA-JEPA<br/><i>2026</i>"]
    end

    subgraph "Self-Evolving"
        K["EvoAgent<br/><i>2025</i>"]
        L["SPIRAL<br/><i>2026</i>"]
    end

    A0 --> D --> E --> F --> G
    B --> G
    D1 --> D2 --> H1
    G --> H
    G --> H1
    G --> H2
    G --> K
    H --> L
    K --> L

    style A0 fill:#e8f4fd,stroke:#4a90d9
    style G fill:#e8f4fd,stroke:#4a90d9
    style H fill:#f0e8fd,stroke:#9b59b6
    style K fill:#e8fde8,stroke:#27ae60
```

| Node | Paper |
|------|-------|
| RT-1 | [[2212.06817\|RT-1]] |
| Diffusion Policy | [[2303.04137\|Diffusion Policy]] |
| RT-2 | [[2307.15818\|RT-2]] |
| OXE / RT-X | [[2310.08864\|OXE / RT-X]] |
| OpenVLA | [[2406.09246\|OpenVLA]] |
| π0 | [[2410.24164\|π0]] |
| GR-1 | [[2312.13139\|GR-1]] |
| GR-2 | [[2410.06158\|GR-2]] |
| DreamZero | [[2602.15922\|DreamZero]] |
| VLAW | [[2602.12063\|VLAW]] |
| VLA-JEPA | [[2602.10098\|VLA-JEPA]] |
| EvoAgent | [[2502.05907\|EvoAgent]] |
| SPIRAL | [[2603.08403\|SPIRAL]] |

---

## 1. Robotic Policy Foundations & Manipulation

How robots learn to act from demonstrations. The field evolved from perception-based agents (PerAct) through diffusion-based action generation to spatial and language-conditioned policies. Manipulation is the proving ground — if a method works for dexterous object interaction, it can generalize to broader embodied tasks.

**Diffusion-Based Policies** — Treat robot actions as a noise-removal process, generating smooth multi-step trajectories that handle multimodal action distributions (e.g., reaching from the left vs. right) better than regression.
- [[2303.04137|Diffusion Policy]], [[2403.03954|DP3]], [[2407.05996|MDT]], [[2502.02316|DIME]], [[2503.02881|Reactive Diffusion Policy]]

> [!star] Key Papers
> - [[2303.04137|Diffusion Policy]] — Pioneered action diffusion for robotics; proved denoising beats regression for multimodal distributions
> - [[2403.03954|DP3]] — Extended to 3D point clouds, enabling sim-to-real transfer without camera calibration

**Foundational Manipulation Architectures** — Transformer and perception-based agents that established how robots can learn multi-task manipulation from language instructions and visual observations.
- [[2209.05451|PerAct]], [[2306.10007|RPT]], [[2405.12213|Octo]], [[2412.11974|EMMA-X]], [[2410.07864|RDT-1B]]

> [!star] Key Papers
> - [[2209.05451|PerAct]] — First to use Perceiver Transformer on voxelized observations for 6-DoF multi-task manipulation
> - [[2405.12213|Octo]] — Open-source generalist policy with strong zero-shot transfer across robot morphologies

**Bimanual & Teleoperation** — Hardware platforms and methods for dual-arm manipulation and human-guided data collection, which are critical for scaling real-world demonstrations.
- [[2304.13705|ALOHA]], [[2309.13037|GELLO]], [[2507.07969|Q-chunking]]

> [!star] Key Papers
> - [[2304.13705|ALOHA]] — Low-cost open-source bimanual system; proved co-training on diverse data dramatically improves performance

**Spatial Reasoning for Manipulation** — Leverage 3D point clouds, depth maps, or learned spatial features to improve generalization across camera viewpoints and object arrangements.
- [[2501.10074|SpatialCoT]], [[2510.12276|Spatial Forcing]], [[2509.18644|State-Free Visuomotor Policy]], [[2602.18374|ZS-IP]]

> [!star] Key Papers
> - [[2501.10074|SpatialCoT]] — Chain-of-thought reasoning in 3D space; bridges VLM reasoning with spatial manipulation

**Language-Conditioned & Multi-Stage** — Plan and execute complex, multi-step tasks from natural language instructions by composing LLM planning with robot execution.
- [[2201.07207|LLM Zero-Shot Planners]], [[2307.05973|VoxPoser]], [[2409.01652|ReKep]], [[2507.17520|InstructVLA]], [[2603.02511|Unveiler]]

> [!star] Key Papers
> - [[2307.05973|VoxPoser]] — LLMs generate 3D value maps that guide robot actions; no robot training data needed
> - [[2409.01652|ReKep]] — Automatic keypoint discovery from VLMs for constraint-based manipulation planning

**World Model Studies** — Empirical studies of predictive models in manipulation contexts.
- [[2512.24497|JEPA-WM]]

> [!tip] The Diffusion Policy Shift
> Regression → diffusion → flow matching. If you're building a manipulation policy today, start with Diffusion Policy or DP3 and add 3D/spatial features for viewpoint invariance.

---

## 2. Vision-Language-Action Models (VLAs)

VLAs are the current mainstream approach to robot control: take a pre-trained vision-language model, fine-tune it to output robot actions directly. The field has exploded from RT-1/RT-2 (2022-2023) to 80+ models spanning efficient deployment, spatial awareness, reasoning, world-model augmentation, and self-evolution.

> [!success] Ideal VLA Recipe (from RoboVLMs)
> ==KosMos/[[2407.07726|PaliGemma]] backbone== + ==Policy Head fusion== + ==Continuous actions== + ==MoE== + ==Post-training on in-domain data==

**Foundation & Generalist** — The pioneering VLA architectures that established the paradigm: fine-tune a VLM to output robot actions as tokens or flow-matching trajectories.
- [[2212.06817|RT-1]], [[2307.15818|RT-2]], [[2310.08864|OXE / RT-X]], [[2406.09246|OpenVLA]], [[2410.24164|π0]], [[2312.13139|GR-1]], [[2410.06158|GR-2]], [[2405.12213|Octo]], [[2311.01378|RoboFlamingo]], [[2503.20020|Gemini Robotics]], [[2512.22414|π0.5 + ego]]

> [!star] Key Papers
> - [[2212.06817|RT-1]] — Google's first VLA: 130K demonstrations, 700 tasks, Transformer-based; proved the paradigm works
> - [[2307.15818|RT-2]] — Scaled to PaLI-X/PaLM-E backbones; first to show internet-scale VLM knowledge transfers to robot control
> - [[2406.09246|OpenVLA]] — Open-source 7B VLA; democratized VLA research
> - [[2410.24164|π0]] — Flow matching for continuous actions; current SOTA for generalist robot control

**Efficient & Open-Source** — Smaller, faster, or quantized VLAs optimized for real-world deployment where inference speed and cost matter.
- [[2502.19645|OpenVLA-OFT]], [[2501.09747|FAST]], [[2504.19854|NORA]], [[2506.01844|SmolVLA]], [[2409.12514|TinyVLA]], [[2602.18224|SimVLA]], [[2601.22153|DynamicVLA]], [[2602.13710|HBVLA]], [[2509.04996|FLOWER]], [[2511.14148|AsyncVLA]], [[2506.19816|CronusVLA]]

> [!star] Key Papers
> - [[2501.09747|FAST]] — Compression-based action tokenization; makes VLAs 5x faster by compactly encoding continuous actions
> - [[2506.01844|SmolVLA]] — 450M params achieving competitive performance; proves VLAs don't need to be massive

**Spatial & 3D-Aware** — Inject depth, 3D coordinate embeddings, or volumetric features into VLAs for better spatial generalization.
- [[2501.15830|SpatialVLA]], [[2403.09631|3D-VLA]], [[2505.05800|3D-CAVLA]], [[2506.22242|4D-VLA]]

> [!star] Key Papers
> - [[2501.15830|SpatialVLA]] — Novel spatial representations that let VLAs understand object arrangements without explicit 3D supervision

**Reasoning & Chain-of-Thought** — VLAs that think before they act: predict subgoals, search over plans, or use MCTS for test-time reasoning.
- [[2503.22020|CoT-VLA]], [[2601.11404|ACoT-VLA]], [[2509.22643|VLA-Reasoner]], [[2507.16815|ThinkAct]], [[2512.24125|GenieReasoner]], [[2411.19650|CogACT]]

> [!star] Key Papers
> - [[2503.22020|CoT-VLA]] — Predicts visual subgoals as chain-of-thought before acting; bridges language reasoning with physical planning
> - [[2509.22643|VLA-Reasoner]] — Online MCTS for test-time reasoning; trades compute for better decisions

**World-Model-Augmented** — VLAs that also predict future states, combining action generation with physics simulation for more robust policies.
- [[2602.12063|VLAW]], [[2602.22010|WoG]], [[2506.21539|WorldVLA]], [[2508.18269|FlowVLA]], [[2507.04447|DreamVLA]], [[2602.10098|VLA-JEPA]], [[2511.17502|RynnVLA-002]], [[2501.18867|UP-VLA]], [[2512.13030|Motus]], [[2509.06951|F1]], [[2601.16163|Cosmos Policy]], [[2601.21998|LingBot-VA]]

> [!star] Key Papers
> - [[2602.12063|VLAW]] — Iterative co-improvement loop between VLA policy and world model; each bootstraps the other
> - [[2602.10098|VLA-JEPA]] — JEPA-style latent prediction for leakage-free future state modeling in robot control
> - [[2601.16163|Cosmos Policy]] — Fine-tunes NVIDIA's Cosmos video diffusion model; 98.5% on LIBERO

**RL-Enhanced** — VLAs improved via reinforcement learning post-training, pushing performance beyond what imitation alone achieves.
- [[2505.18719|VLA-RL]], [[2505.17016|RIPT-VLA]], [[2509.09674|SimpleVLA-RL]], [[2506.08440|TGRPO]], [[2411.19309|GRAPE]], [[2511.15605|SRPO]], [[2511.14759|RECAP]]

> [!star] Key Papers
> - [[2505.18719|VLA-RL]] — First systematic RL framework for VLAs; showed RL post-training consistently improves over SFT
> - [[2505.17016|RIPT-VLA]] — Adds a "third stage" of RL training that bridges the gap between simulation and real-world

**Self-Evolving & Continual** — VLAs that can adapt, merge, or evolve autonomously from ongoing experience without catastrophic forgetting.
- [[2511.16166|EvoVLA]], [[2512.14666|EVOLVE-VLA]], [[2511.18810|MergeVLA]], [[2509.24948|RehearseVLA]]

> [!star] Key Papers
> - [[2512.14666|EVOLVE-VLA]] — Continuous adaptation from environmental feedback; addresses the deploy-and-forget problem

**Humanoid & Platform-Specific** — VLAs designed for humanoid robots, loco-manipulation, or domain-specific applications.
- [[2502.14795|Humanoid-VLA]], [[2503.14734|GR00T N1]], [[2603.12263|Psi0]], [[2503.09527|CombatVLA]]

> [!star] Key Papers
> - [[2503.14734|GR00T N1]] — NVIDIA's open foundation model for humanoid whole-body control
> - [[2603.12263|Psi0]] — Decoupled locomotion + manipulation for humanoids; practical loco-manipulation

**Multi-Sensor & Force-Aware** — VLAs that go beyond vision by integrating tactile, force, or proprioceptive feedback for contact-rich tasks.
- [[2507.09160|Tactile-VLA]], [[2505.22159|ForceVLA]], [[2511.18960|AVA-VLA]], [[2502.14420|ChatVLA]], [[2508.10333|ReconVLA]]

> [!star] Key Papers
> - [[2507.09160|Tactile-VLA]] — First to integrate 6-axis force feedback into VLAs; critical for assembly and insertion tasks

**Architecture Studies** — Systematic explorations of VLA design choices, scaling laws, and novel architectures.
- [[2412.14058|RoboVLMs]], [[2601.18692|LingBot-VLA]], [[2601.02456|InternVLA-A1]], [[2602.11236|ABot-M0]], [[2511.18085|Stellar VLA]], [[2510.10274|X-VLA]], [[2510.13054|VLA-0]], [[2506.19850|UniVLA]], [[2603.12772|PVI]], [[2510.19430|GigaBrain-0]], [[2506.00123|VeBrain]], [[2508.19236|MemoryVLA]], [[2409.03299|RT-1-X SCARA Transfer]], [[2412.10345|TraceVLA]], [[2509.09372|2509.09372]], [[2511.05275|TwinVLA]]

> [!star] Key Papers
> - [[2412.14058|RoboVLMs]] — 600+ experiments systematically testing VLA design choices; the definitive recipe paper

> [!tip] The VLA Stack
> Pick a VLM backbone (PaliGemma) → add action head (flow matching) → fine-tune on in-domain data → post-train with RL. This is the proven recipe from RoboVLMs.

---

## 3. World Action Models (WAMs)

WAMs go beyond VLAs by jointly predicting future states and actions — they learn the physics of the world, not just how to imitate demonstrations. The key architectural question is *where* to predict: in pixel space (video generation), latent space (JEPA-style), or action space only (efficient WAMs).

**Dreamer Lineage** — The original model-based RL approach: learn world dynamics in compressed latent space via recurrent state-space models, then plan entirely in "imagination."
- [[2206.14176|DayDreamer]], [[2502.05907|EvoAgent]]

> [!star] Key Papers
> - [[2206.14176|DayDreamer]] — First to deploy Dreamer on real robots; proved sample-efficient learning from imagination works physically

**Video Generation as World Models** — Use pre-trained video diffusion models as physics simulators: generate future video frames conditioned on actions, then extract policies from the generated futures.
- [[2602.15922|DreamZero]], [[2310.06114|UniSim]], [[2512.15692|mimic-video]], [[2412.14803|VPP]], [[2508.00795|Video Policy]], [[2505.12705|DreamGen]], [[2510.01183|EvoWorld]], [[2512.24766|Dream2Flow]], [[2601.20540|LingBot-World]], [[2310.10625|VLP]]

> [!star] Key Papers
> - [[2602.15922|DreamZero]] — 14B parameter WAM from NVIDIA; zero-shot robot policies via joint video+action prediction; 39.5% on unseen tasks
> - [[2310.06114|UniSim]] — Universal simulator from video diffusion; learns interaction dynamics from heterogeneous data
> - [[2412.14803|VPP]] — Extracts visual representations from video diffusion in a single forward pass (no iterative denoising at test time)

**Efficient / Action-Centered** — WAMs optimized for speed: focus compute on action prediction rather than full video generation. Key insight: you need video modeling at *training time* for learning physics, but not at *test time* for acting.
- [[2603.16666|Fast-WAM]], [[2603.17240|GigaWorld-Policy]], [[2503.16806|DyWA]], [[2512.19133|WorldRFT]], [[2412.15109|Seer]]

> [!star] Key Papers
> - [[2603.16666|Fast-WAM]] — Proved training-time video modeling is what matters, not test-time imagination; 97.6% on LIBERO
> - [[2603.17240|GigaWorld-Policy]] — 9x speedup over DreamZero via action-centered design with training-only video supervision

**Latent Prediction** — Predict future states in a learned latent space (JEPA-style) rather than reconstructing pixels. Faster, more robust to visual noise, and better suited for real-time control.
- [[2504.02792|UWM]], [[2503.00200|UVA]], [[2506.23468|NavMorph]], [[2507.13340|LPS]], [[2403.08321|ManiGaussian]], [[2603.19312|LeWM]]

> [!star] Key Papers
> - [[2504.02792|UWM]] — Unified World Models: a single architecture handling action-conditioned, action-free, and video prediction tasks
> - [[2506.23468|NavMorph]] — Self-evolving world model for navigation; Contextual Evolution Memory updates latent representations online

**VLM-Integrated** — Combine the semantic reasoning of VLMs with the physics simulation of world models for high-level planning + low-level control.
- [[2603.14497|WorldVLM]], [[2403.06845|DriveDreamer-2]]

> [!star] Key Papers
> - [[2603.14497|WorldVLM]] — Hybrid VLM + world model for autonomous driving; contextual reasoning meets physics prediction

**Self-Evolving WAMs** — WAMs designed to continuously improve through experience-driven loops, curiosity, and reflective planning.
- [[2602.04411|Self-evolving Embodied AI]], [[2603.15381|Autonomous Learning Framework]]

> [!star] Key Papers
> - [[2602.04411|Self-evolving Embodied AI]] — Defines the paradigm: agents that autonomously acquire, refine, and transfer skills across environments

**Surveys** — Comprehensive reviews of world model architectures, taxonomies, and design principles.
- [[2411.14499|World Models Survey 2024]], [[2509.20021|Embodied AI LLM-WM Survey]], [[2510.16732|World Models for Embodied AI Survey]], [[2407.06886|ARIO]]

> [!tip] Video vs Latent
> DreamZero proves video generation works at scale, but Fast-WAM shows you only need video at *training time*. For deployment, latent prediction (UWM, VLA-JEPA) is faster and more practical.

---

## 4. Self-Evolving Embodied AI

The frontier of embodied AI: robots that improve themselves through experience without human intervention. These systems combine world models (for imagination), continual learning (for memory), curiosity (for exploration drive), and evolutionary algorithms (for policy improvement). See [[11_Self-Evolving-AI]].

- [[2502.05907|EvoAgent]] (2025) — ==self-evolving agent== with continual world model for long-horizon tasks; **+105%** improvement
- [[2506.21669|SEEA-R1]] (2025) — ==tree-structured RL== for self-evolving embodied agents; **+24%** via MCTS + generative reward
- [[2503.01584|SENSEI]] (2025) — ==semantic exploration== with epistemic uncertainty + Go-Explore for versatile world models
- [[2510.16079|EVOLVER]] (2025) — LLM agents self-evolving through experience-driven lifecycle
- [[2603.08403|SPIRAL]] (2026) — ==closed-loop framework== for self-improving action world models via reflective planning

> [!star] Key Papers
> - [[2502.05907|EvoAgent]] — Built on DreamerV3 with continual world model; demonstrated self-planning + self-control + self-reflection loop
> - [[2603.08403|SPIRAL]] — Closed-loop self-improvement for WAMs via reflective planning; the system critiques its own failures and adapts

> [!tip] The Self-Evolving WAM Path
> The ideal trajectory: train a WAM → add continual learning → add curiosity-driven exploration → self-evolving robot.

---

## 5. Navigation & Autonomous Driving

Both navigation and driving reduce to the same core problem: perceive the environment, predict its future state, and plan a trajectory. Navigation operates at room/building scale with discrete goals; driving operates at city scale with continuous safety constraints.

**Indoor Object-Goal Navigation** — Find and navigate to target objects in unseen environments using visual reasoning, cognitive maps, or LLM-based planning.
- [[2401.05946|TDB]], [[2412.10439|CogNav]], [[2510.20685|C-Nav]]

> [!star] Key Papers
> - [[2412.10439|CogNav]] — Models human-like cognitive processes for navigation; outperforms reactive policies on complex layouts

**Vision-Language Navigation** — Follow natural language instructions through visual environments, requiring grounding of spatial language to visual observations.
- [[2506.15757|WPCL]]

**Autonomous Driving (World Model Perspective)** — Driving as a world model problem: predict the scene's future, then plan safe trajectories.
- [[2403.06845|DriveDreamer-2]], [[2603.14497|WorldVLM]], [[2409.18964|PhysGen]], [[2505.17685|FSDrive]], [[2512.24331|LVLDrive]]

> [!star] Key Papers
> - [[2403.06845|DriveDreamer-2]] — LLM-enhanced driving video generation; creates diverse scenarios for world model training
> - [[2603.14497|WorldVLM]] — Hybrid VLM + world model architecture; combines semantic reasoning with physics prediction for driving

**Surveys & Roadmaps** — Reviews of embodied navigation and spatial intelligence.
- [[2311.00530|LLM Embodied Navigation Survey]], [[2512.24385|Spatial Intelligence Roadmap]]

> [!tip] Navigation → Driving
> Both reduce to "predict the future scene, then plan a trajectory." The difference is scale and safety constraints. World model approaches transfer between them.

---

## 6. Imitation Learning & RL for Robotics

The training paradigm question: pure imitation learning (behavior cloning) is simple but plateaus at the demonstration distribution ceiling. Adding RL post-training pushes policies beyond what demonstrations alone can teach — handling novel situations, recovering from errors, and optimizing long-horizon objectives.

**RL-Augmented Imitation** — Combine imitation learning with RL reward signals to overcome the limitations of pure behavior cloning.
- [[2505.03181|AFSFT]], [[2510.19307|RIL]], [[2510.25992|SRL]]

> [!star] Key Papers
> - [[2505.03181|AFSFT]] — Advantage-filtered SFT: uses RL advantage estimates to select which demonstrations to learn from

**Reward Learning** — Learn reward functions from visual feedback or human preferences to guide robot training without hand-crafted reward engineering.
- [[2512.20675|VLM Reward Objectives]], [[2601.16973|VisGym]]

> [!star] Key Papers
> - [[2512.20675|VLM Reward Objectives]] — Simple triplet loss on VLMs produces effective reward signals for robot learning

**Continual & Experience-Driven** — Agents that improve from ongoing real-world interaction without catastrophic forgetting.
- [[2510.08558|Early Experience]], [[2603.03818|VLA Continual Learning]]

> [!star] Key Papers
> - [[2603.03818|VLA Continual Learning]] — Showed pre-trained VLAs have surprising resistance to catastrophic forgetting during continual adaptation

> [!tip] When to Add RL
> Pure imitation plateaus at the demonstration distribution. Add RL post-training (RIPT-VLA, VLA-RL) to improve robustness beyond what demonstrations alone can teach.

---

## 7. Embodied AI — General

Cross-cutting research that doesn't fit neatly into manipulation, VLAs, or navigation — but addresses fundamental challenges like cross-embodiment transfer, scene understanding, and domain adaptation that all embodied AI systems face.

**Generalist Architectures** — Modular frameworks designed to work across different robot types, sensor configurations, and task domains.
- [[2409.20537|HPT]], [[2410.02742|GLIMO]], [[2412.07755|SAT]]

> [!star] Key Papers
> - [[2409.20537|HPT]] — Heterogeneous Pre-trained Transformers: modular architecture that handles diverse robot embodiments through shared trunk + task-specific heads

**Hardware & Simulation Platforms** — Robotic hardware designs and simulation environments that enable large-scale data collection and policy evaluation.
- [[2504.04259|ORCA Hand]], [[2506.18088|RoboTwin 2.0]], [[2602.21992|PanoEnv]]

> [!star] Key Papers
> - [[2504.04259|ORCA Hand]] — Open-source anthropomorphic hand; bridges the gap between simulation and real dexterous manipulation

**Spatial & Scene Understanding** — Understanding 3D scenes, layouts, and spatial relationships as a prerequisite for embodied reasoning.
- [[2511.16160|Video2Layout]], [[2603.18892|MultihopSpatial]]

**Domain Adaptation** — Transfer policies across visual domains without retraining from scratch.
- [[2407.13771|Training-Free Model Merging MTDA]]

> [!tip] Cross-Embodiment Transfer
> The key challenge: policies trained on one robot must work on others. HPT and OXE show that modular architectures + diverse training data are the path.

---

## 8. Datasets, Benchmarks & Simulators

The data and evaluation infrastructure that makes all the above research possible. Datasets provide training signal, benchmarks measure progress, and simulators enable safe, scalable experimentation.

**Large-Scale Cross-Robot Datasets** — Massive datasets spanning multiple robot types and environments.
- [[2310.08864|OXE]], [[2403.12945|DROID]], [[2503.06669|AgiBot World]], [[2307.00595|RH20T]]

> [!star] Key Papers
> - [[2310.08864|OXE]] — Open X-Embodiment: 1M+ trajectories from 22 embodiments; the ImageNet moment for robotics
> - [[2403.12945|DROID]] — In-the-wild data across 16 institutions; proved diverse data beats curated data

**Multi-Modal & Bimanual Datasets** — Datasets with rich sensor modalities (tactile, force) or bimanual manipulation focus.
- [[2412.13877|RoboMIND]], [[2512.24653|RoboMIND 2.0]], [[2511.17441|RoboCOIN]], [[2509.00576|G0]]

**Benchmarks — Simulation** — Standardized simulation environments for reproducible evaluation.
- [[1909.12271|RLBench]], [[2112.03227|CALVIN]], [[2306.03310|LIBERO]], [[2405.05941|SIMPLER]], [[2406.02523|RoboCasa]], [[2510.13626|LIBERO-Plus]]

> [!star] Key Papers
> - [[2306.03310|LIBERO]] — Lifelong robot learning benchmark; tests continual learning and long-horizon capability
> - [[2405.05941|SIMPLER]] — Bridges sim and real; evaluates whether simulation performance predicts real-world success

**Benchmarks — Diagnostic** — Targeted benchmarks that expose specific failure modes.
- [[2305.12821|FurnitureBench]], [[2601.11421|GM-100]], [[2505.15660|AGNOSTOS]], [[2506.18088|RoboTwin 2.0]]

> [!star] Key Papers
> - [[2601.11421|GM-100]] — 100 detail-oriented tasks; current VLAs achieve very low success rates, exposing real capability gaps

**Surveys:**
- [[2103.04918|Embodied AI Survey 2021]] — simulators and research tasks
- [[2407.06886|ARIO / Embodied AI Survey 2024]] — comprehensive survey with ARIO dataset standard
- [[2509.20021|Embodied AI LLM-WM Survey]] — joint MLLM-WM architecture roadmap
- [[2405.14093|VLA Survey]] — survey of VLA models for embodied AI
- [[2505.04769|VLA Survey 2025]] — updated VLA landscape review

> [!tip] The Dataset Hierarchy
> Start with simulation (RLBench, CALVIN) → scale with in-the-wild data (DROID, OXE) → diagnose with targeted benchmarks (GM-100, LIBERO-Plus).

---

## Cross-References

- [[11_Self-Evolving-AI]] — Broader self-evolving paradigm
- [[04_Reinforcement-Learning]] — RL as the training backbone
- [[06_Video-and-Temporal]] — Video generation as world modeling

---

*Next: [[08_Benchmarks-and-Surveys]] for a cross-cutting view of evaluation resources.*
