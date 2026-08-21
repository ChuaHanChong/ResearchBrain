---
title: "Embodied AI — 101"
tags:
  - VLA
  - WAM
  - robotics
  - embodied-AI
aliases:
  - "Embodied AI 101"
  - "VLA vs WAM"
  - "VLA 101"
  - "WAM 101"
---

# Embodied AI — 101

Embodied AI gives intelligent systems physical presence — robots that manipulate objects, navigate environments, drive vehicles, and interact with the real world. The two core model families are **Vision-Language-Action (VLA)** models that learn from demonstrations, and **World Action Models (WAM)** that learn to predict the future. This note covers both paradigms and how they fit together.

> [!abstract] One-Line Summary
> **VLAs** copy what they've seen. **WAMs** imagine what will happen next. **Self-evolving systems** improve from experience. See [[04_VLA]], [[06_WAM]], and [[16_Self-Evolving-VLA-WAM]] for deep dives.

## Evolution Graph

The embodied-AI field evolved through four phases — from single-task imitation foundations, to generalist VLAs, to world-model-augmented systems, to self-evolving agents.

```text
1. Learning Foundations   (the RL and control ideas underneath)
· model-free to model-based RL
╔════════════╗
║ DQN (2013) ║─┐
╚════════════╝ │
               │    +stable policy
               │    gradient          +max entropy
               │    ┌────────────┐    ┌────────────┐
               ├───►│ PPO (2017) │───►│ SAC (2018) │
               │    └────────────┘    └────────────┘
               │                       +latent
               │    +learned model     imagination
               │    ┌─────────────┐    ┌────────────────┐
               └───►│ MBPO (2019) │───►│ Dreamer (2019) │
                    └─────────────┘    └────────────────┘

2. Vision-Language-Action   (one model from pixels to motors)
· the VLA line
                   +web knowledge
╔═════════════╗    ┌─────────────┐
║ RT-1 (2022) ║───►│ RT-2 (2023) │─┐
╚═════════════╝    └─────────────┘ │
                                   │    +open weights
                                   │    ┌────────────────┐
                                   ├───►│ OpenVLA (2024) │
                                   │    └────────────────┘
                                   │    +flow
                                   │    matching         +open-world
                                   │    ┌───────────┐    ┌─────────────┐
                                   └───►│ π0 (2024) │───►│ π0.5 (2025) │
                                        └───────────┘    └─────────────┘

· action representation
╔═════════════════════════╗
║ Diffusion-Policy (2023) ║─┐
╚═════════════════════════╝ │
                            │    +generalist
                            │    transformer
                            │    ┌─────────────┐
                            ├───►│ Octo (2024) │
                            │    └─────────────┘
                            │    +action
                            │    tokenizer          +atomic skills
                            │    ┌─────────────┐    ┌──────────────────┐
                            └───►│ FAST (2025) │───►│ AtomicVLA (2026) │
                                 └─────────────┘    └──────────────────┘

3. World Models   (learning to predict what happens next)
· predictive backbones
╔═══════════════╗
║ Cosmos (2025) ║─┐
╚═══════════════╝ │
                  │    +zero-shot dreams       +real-time WAM
                  │    ┌──────────────────┐    ┌─────────────────┐
                  ├───►│ DreamZero (2026) │───►│ Fast-WAM (2026) │
                  │    └──────────────────┘    └─────────────────┘
                  │    +latent prediction
                  │    ╔═════════════════╗
                  └───►║ V-JEPA-2 (2025) ║
                       ╚═════════════════╝

4. Self-Evolving   (improving after deployment)
· lifelong improvement
                       +semantic
                       curiosity            +self-play           +continual VLA
╔═════════════════╗    ┌───────────────┐    ┌───────────────┐    ┌───────────────────────────────┐
║ EvoAgent (2025) ║───►│ SENSEI (2025) │───►│ SPIRAL (2025) │───►│ VLA-Continual-Learning (2026) │
╚═════════════════╝    └───────────────┘    └───────────────┘    └───────────────────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

Four lanes, read in order. **Learning Foundations** shows the fork that still organises everything: [[1312.5602|DQN]] split into model-free policy gradients ([[1707.06347|PPO]], [[1801.01290|SAC]]) and learning a model to plan inside ([[1906.08253|MBPO]], [[1912.01603|Dreamer]]). **Vision-Language-Action** carries two threads — the backbone line from [[2212.06817|RT-1]] to [[2504.16054|π0.5]], and how an action is represented at all, from [[2303.04137|Diffusion-Policy]] to [[2603.07648|AtomicVLA]]. **World Models** is what a robot predicts before acting; **Self-Evolving** is what it does after deployment.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2013 | [[1312.5602\|DQN]] | RL Foundations | Introduced the Deep Q-Network (DQN), which approximates the Q-function using a deep convolutional neural network that takes |
| 2017 | [[1707.06347\|PPO]] | RL Foundations | PPO introduces a family of policy gradient methods that reuse collected data through multiple optimization steps |
| 2018 | [[1801.01290\|SAC]] | RL Foundations | Develops an off-policy actor-critic algorithm that incorporates the maximum entropy objective |
| 2019 | [[1906.08253\|MBPO]] | RL Foundations | A method using branched short-horizon rollouts (k-step) from real replay states with a probabilistic dynamics ensemble |
| 2019 | [[1912.01603\|Dreamer]] | RL Foundations | A latent-imagination agent via RSSM: an actor-critic trained purely in imagination by propagating analytic gradients |
| 2022 | [[2212.06817\|RT-1]] | VLA | The **Robotics Transformer 1 (RT-1)** is a 35M parameter Transformer-based policy that takes image sequences and natural |
| 2023 | [[2303.04137\|Diffusion-Policy]] | Action Representation | The framework formulates visuomotor policies as conditional denoising diffusion probabilistic models (DDPMs) that learn |
| 2023 | [[2307.15818\|RT-2]] | VLA | Google DeepMind's **RT-2** introduces Vision-Language-Action (VLA) models |
| 2024 | [[2405.12213\|Octo]] | Action Representation | **Octo** employs a modular, transformer-first architecture with a conditional denoising diffusion process for action |
| 2024 | [[2406.09246\|OpenVLA]] | VLA | Develops and releases **OpenVLA**, a 7B-parameter |
| 2024 | [[2410.24164\|π0]] | VLA | Developed **π0**, integrating a pre-trained PaliGemma VLM backbone with a novel action expert based on conditional flow |
| 2025 | [[2501.03575\|Cosmos]] | World Model | An open-source World Foundation Model Platform from NVIDIA that curates **20M hr** raw video → **100M** clips and pre-trains |
| 2025 | [[2501.09747\|FAST]] | Action Representation | A DCT+Huffman action tokenization scheme exploiting that adjacent action timesteps are highly correlated |
| 2025 | [[2502.05907\|EvoAgent]] | Self-Evolving | A method that builds a self-planning + self-control + self-reflection loop on DreamerV3 |
| 2025 | [[2503.01584\|SENSEI]] | Self-Evolving | A Semantic uncertainty + Go-Explore method targeting the agent's hardest states via VLM-derived novelty signals |
| 2025 | [[2504.16054\|π0.5]] | VLA | **π0.5** employs a co-training framework that leverages multiple data types including mobile manipulator data |
| 2025 | [[2506.09985\|V-JEPA-2]] | World Model | A video-scale JEPA that scales I-JEPA to **1M+ hours** of video with a mask-denoising objective |
| 2025 | [[2506.24119\|SPIRAL]] | Self-Evolving | The SPIRAL framework implements a fully online, multi-turn |
| 2026 | [[2602.15922\|DreamZero]] | World Model | The canonical pixel-space generative WM whose autoregressive diffusion transformer spends most of its capacity on visual |
| 2026 | [[2603.03818\|VLA-Continual-Learning]] | Self-Evolving | A study proving pretrained VLAs are *naturally* resistant to forgetting |
| 2026 | [[2603.07648\|AtomicVLA]] | Action Representation | A think/act mode-switching method with a Skill-Guided MoE (SG-MoE) routing over atomic skill abstractions |
| 2026 | [[2603.16666\|Fast-WAM]] | World Model | A Mixture-of-Transformer that decouples video co-training (train) from future-imagination (inference) |

> [!star] Start Here — Suggested Reading Order
> A path into the field, not the lineage's landmarks — the Evolution Graph above marks those with a double border (`╔═╗`), and the two lists differ on purpose.
> - [[2212.06817|RT-1]] — Proof that Transformers work for robot control; the foundational VLA
> - [[2307.15818|RT-2]] — Web-scale VLM knowledge transfers to robots; defined the modern VLA paradigm
> - [[2406.09246|OpenVLA]] — Open-source 7B VLA that democratized VLA research; the easiest one to actually run
> - [[2410.24164|π0]] — Flow-matching action expert + VLM; the dominant continuous-action recipe
> - [[2602.15922|DreamZero]] — Joint video + action prediction (14B WAM); zero-shot robot policies
> - [[2506.09985|V-JEPA-2]] — Video-scale latent prediction; the bridge from world models into policies

---

## Part A — Concepts

*Start here. The intuitive primer, the two paradigms (VLA & WAM), and how they compare side-by-side.*

### 1. ELI5

> [!example] Catching a Ball
> Imagine you are teaching a robot how to catch a ball. Here is how the two robot brains would learn:

#### The VLA Brain (The Memorizer)

This robot learns by playing **"Simon Says."** You throw the ball exactly the same way 100 times, and you move the robot's arm to the exact right spot to catch it. The robot memorizes, "When I hear 'catch' and see the ball right *here*, I move my arm exactly like *this*."

It is really good at following instructions and recognizing the ball, but it doesn't actually understand how gravity works. If the wind blows the ball a little to the left, or you use a heavier ball, the robot will probably miss because it only knows the exact movements it memorized.

#### The WAM Brain (The Imaginer)

This robot learns by **daydreaming**. Instead of just memorizing arm movements, it watches videos of balls flying through the air and bouncing. When you throw the ball to this robot, its brain actually imagines the future. It thinks, "If the ball is moving this fast, it will land over *there* in two seconds."

Because it actually understands the rules of the world (like gravity and momentum) and can picture what is about to happen, it can figure out how to move its arm to catch the ball — even if it's a brand new bouncy ball or the wind is blowing.

> [!summary] The Short Version
> - **VLAs** learn by copying exactly what they have seen before.
> - **WAMs** learn by imagining what will happen next and acting based on that picture.

---

### 2. Vision-Language-Action (VLA) Models

VLAs are essentially multimodal large language models fine-tuned for robotic control. Well-known examples include [[2307.15818|RT-2]] and [[2406.09246|OpenVLA]].

**How They Work:** They ingest visual observations (images of the environment) and language instructions (the goal), and directly output a sequence of discrete ==action tokens== (motor commands or waypoints).

**The Learning Paradigm:** VLAs primarily learn through ==behavioral cloning== — dense state-action imitation. They look at what an expert did in a specific situation and learn to map that exact visual state to that exact action.

> [!success] Strengths
> Built on robust vision-language backbones, VLAs excel at **semantic generalization**. If you tell a VLA to "pick up the red apple," it deeply understands what an apple is and what red looks like, even if the apple is slightly different from training data.

> [!warning] Limitations
> VLAs are effectively **"blind" to physics**. Because they only output an action, they do not inherently understand its physical consequences. This makes them struggle in novel environments with unseen physical dynamics, and they require thousands of carefully collected, repetitive expert demonstrations to learn a single task.

---

### 3. World Action Models (WAM)

WAMs are an emerging class of foundation models (such as [[2602.15922|DreamZero]]) that unify action generation with a predictive "world model."

**How They Work:** Built on advanced ==video diffusion backbones== or autoregressive transformers, WAMs take in visual context and language instructions, but jointly predict ==future video frames== and the corresponding actions.

**The Learning Paradigm:** WAMs shift the learning process from imitation to ==inverse dynamics==. By forcing the model to generate the future visual state of the world (e.g., predicting exactly how an object will fall or deform when pushed), the model naturally learns "world physics priors." Motor commands are then aligned with these predicted visual futures.

> [!success] Strengths
> - **Zero-Shot Generalization:** WAMs can successfully execute unseen physical motions in novel environments on the first try.
> - **Data Efficiency:** They can learn from heterogeneous sources, including passive, video-only data (e.g., 10 minutes of a human performing a task), enabling cross-embodiment transfer without action labels.

> [!warning] Limitations
> WAMs are computationally expensive. Generating future video states alongside actions introduces high latency, requiring significant optimizations (decoupled noise schedules, KV-caching) to reach real-time control frequencies.

---

### 4. Head-to-Head Comparison

| Feature | Vision-Language-Action (VLA) | World Action Models (WAM) |
| --- | --- | --- |
| Primary Output | Actions | Future visual states (video) + Actions |
| Learning Objective | Imitate expert actions | Predict world evolution + inverse dynamics |
| Physical Understanding | Implicit and often brittle | Explicit, grounded in physics priors |
| Data Reliance | Repetitive, action-labeled demonstrations | Diverse data, including passive video |
| Generalization | High semantic, low physical | Zero-shot task, environment, and embodiment |

**When to Choose VLA**: Your task is language-heavy (complex instructions), you have abundant demonstration data, and inference speed matters (real-time control at 10-50Hz). VLAs inherit semantic understanding from web-scale VLM pre-training, making them strong at understanding novel instructions. **When to Choose WAM**: You need robustness to visual perturbations (lighting, camera, background changes), your task requires physics-aware planning (predicting consequences of actions), or real-world training data is limited (world model imagination compensates). **When to Combine**: The 2026 consensus is converging on integration — [[2603.16666|Fast-WAM]] and [[2602.10098|VLA-JEPA]] show you can get WAM-level robustness with VLA-level speed by using world model objectives during training only.

> [!tip] Decision Rule
> - **VLA** — language-heavy tasks, abundant demos, real-time control (10–50 Hz)
> - **WAM** — visual-perturbation robustness, physics-aware planning, data scarcity
> - **Both** — train with world-model objectives ([[2602.10098|VLA-JEPA]]), deploy without test-time imagination ([[2603.16666|Fast-WAM]])

^insight-4

---

## Part B — Implementation

*From taxonomy to working code: the formal architecture map, then the open-source stack you can build with today.*

### 5. Robotic Foundation Model Architectures

#### Four Learning Strategies

| Strategy | How It Works | Limitation |
| --- | --- | --- |
| ==Model-Free== | Task-specific policy network maps states → actions | Poor semantic generality |
| ==Model-Based== | Explicit dynamics models decompose the task | Requires accurate dynamics; configuration-specific |
| ==WAM== | Predicts future goal-images, derives actions via inverse dynamics | Hard to learn for complex interactions (doors, deformables) |
| ==VLA== | Pre-trained VLMs encode state, predict actions directly | High compute for history-dependent processing |

**Model-Free** approaches ([[1312.5602|DQN]], [[1801.01290|SAC]], [[1707.06347|PPO]]) learn a direct mapping from observations to actions through trial and error. They are powerful for specific tasks but require millions of environment interactions and don't transfer well to new tasks. **Model-Based** approaches (MPC, [[1906.08253|MBPO]]) learn an explicit dynamics model and use it for planning. They are sample-efficient but require accurate dynamics — errors in the model compound during long-horizon planning. **WAMs** take model-based to the extreme: learn dynamics from internet-scale video, then derive actions via inverse dynamics. The video backbone provides rich physics priors but makes the model large and slow. **VLAs** bypass explicit dynamics entirely: the VLM backbone provides implicit physical understanding from web-scale pre-training, and the model directly predicts actions. This is simpler and faster, but the physical understanding is brittle — it hasn't truly 'learned' physics, just correlated visual patterns with actions.

> [!tip] WAM vs VLA — The Key Differentiator
> WAMs predict a future goal-state then calculate actions via inverse dynamics — powerful but hard to learn for complex physics. VLAs bypass explicit world-modeling by inheriting spatial reasoning from web-scale VLM pre-training, mapping observations directly to control signals.

^insight-5

#### VLA Architecture Taxonomy

VLA design choices break into three axes:

**History Modeling:**
- ==One-Step== — current observation only (fast, but no temporal context)
- ==History Aggregation== — sliding window of past observations

**History Fusion:**
- ==Interleaved== — observations + actions in one multi-modal stream (effective but expensive)
- ==Policy Head== — VLM processes each step, dedicated head (Transformer/RNN) handles history (more efficient)

**Action Space:**
- ==Discrete== — action tokens predicted auto-regressively (compounding errors over long horizons)
- ==Continuous== — floating-point values via MSE, BCE, or ==Flow Matching== (better temporal coherence)

==Flow Matching== has emerged as the dominant continuous-action recipe: [[2410.24164|π0]] established it for VLAs, [[2503.20314|Wan]] scaled it for video-conditioned generation, [[2504.18471|Action-Flow-Matching]] adapted it for continual robot learning, and [[2505.05470|Flow-GRPO]] showed RL fine-tuning works directly on flow-matching policies — closing the loop between flow-matching SFT and RL post-training.

> [!abstract] Current SOTA Configuration (2026)
> ==Policy Head fusion + Continuous Action Space + Flow-Matching action expert + MoE backbone== — best trade-off between reasoning capacity, throughput, and zero-shot generalization. Frontier exemplars: [[2604.15483|π0.7]] (steerable generalist), [[2602.15922|DreamZero]] (joint video+action 14B WAM), [[2602.10098|VLA-JEPA]] (latent world model + flow head), and [[2603.16666|Fast-WAM]] (training-time video, deployment-time speed).

**Representative models:** [[2310.08864|RT-2-X]], [[2406.09246|OpenVLA]] (one-step/discrete) · [[2405.12213|Octo]], [[2312.13139|GR-1]] (interleaved) · [[2311.01378|RoboFlamingo]] (policy head) · [[2604.07430|HY-Embodied-0.5]] (MoT-MoE multi-embodiment)

#### Data Strategy

Three training recipes for bridging sim-to-real:

1. **Co-training** — simultaneous in-domain + cross-embodiment ([[2310.08864|OXE]]) data
2. **Post-training** — co-train on diverse data, then refine on in-domain only
3. **Fine-tuning** — in-domain data exclusively

> [!warning] In-domain data is non-negotiable
> Even task-agnostic data from the *same robot* outperforms massive cross-embodiment datasets for target tasks. ==Post-training== (diverse pre-train → in-domain refinement) yields the best generalization.

#### Key Empirical Findings

1. **Generalization** — VLAs achieved a **30.3%** improvement on 5-task chains in unseen [[2112.03227|CALVIN]] scenes
2. **Backbone matters** — [[2306.14824|KOSMOS-2]] and [[2407.07726|PaliGemma]] outperform others due to stronger vision-language alignment from larger pre-training datasets
3. **Continuous > Discrete** — continuous actions avoid compounding discretization errors; Flow Matching offers slight gains over MSE
4. **Emergent self-correction** — top VLAs re-locate handles after a missed grasp without explicit error-recovery training; ==Mixture-of-Experts (MoE)== improves zero-shot generalization. Frontier MoE/MoT examples: [[2604.07430|HY-Embodied-0.5]] (MoT for multi-embodiment), [[2603.15169|ForceVLA2]] (Cross-Scale MoE for force fusion), [[2603.07648|AtomicVLA]] (SG-MoE for skill abstraction).

> [!success] Ideal VLA Design Spec
> ==KosMos/[[2407.07726|PaliGemma]] backbone== + ==Policy Head fusion== + ==Continuous actions (Flow Matching)== + ==MoE== + ==Post-training on in-domain data==

---

### 6. How to Build: The Open-Source Stack

The open-source robotics ecosystem now provides every component needed to build, train, and deploy both VLAs and WAMs — from data to deployment on a $100 robot arm.

#### The Pipeline

```
Researcher → Data → Training → Simulation → Deployment
             OXE    LeRobot    Genesis       SO-100
```

| Component | Tool | Role |
|-----------|------|------|
| **Data** | [[2310.08864\|Open-X-Embodiment]] | 1M+ cross-embodiment trajectories for pre-training |
| **Training Framework** | [LeRobot (HuggingFace)](https://github.com/huggingface/lerobot) | End-to-end training pipeline for VLAs ([[2406.09246\|OpenVLA]], ACT, [[2303.04137\|Diffusion-Policy]]) |
| **Simulation** | [Genesis](https://genesis-world.readthedocs.io/en/latest/), [Newton (NVIDIA)](https://developer.nvidia.com/newton-physics) | Physics-accurate simulation for verification before real-world deployment |
| **Hardware** | [SO-100](https://github.com/TheRobotStudio/SO-ARM100) (~$100) | Low-cost robot arm for real-world testing and deployment |

#### Building a VLA (Quick Recipe)

1. **Pick a VLM backbone** — [[2407.07726|PaliGemma]] or [[2306.14824|KOSMOS-2]] (best vision-language alignment)
2. **Add an action head** — Policy Head with continuous actions via ==Flow Matching==
3. **Pre-train on [[2310.08864|OXE]]** — cross-embodiment data for broad priors
4. **Post-train on in-domain data** — fine-tune on your specific robot + tasks
5. **Deploy** — use ==[[2501.09747|FAST]]== tokenization for real-time inference

> See [[04_VLA#1. Design-Space Principles]] for the full design-space analysis.

#### Building a WAM (Quick Recipe)

1. **Choose your prediction space** — Pixel (richest but slowest), Latent (fastest), or Action-only (most efficient)
2. **Pick a backbone** — Video diffusion ([[2501.03575|Cosmos]] / [[2602.15922|DreamZero]]), JEPA ([[2506.09985|V-JEPA-2]]), or RSSM ([[1912.01603|Dreamer]] lineage)
3. **Pre-train on video** — internet-scale video teaches physics priors
4. **Decide test-time strategy** — Full imagination (robust but 4.8x slower) or training-only video ([[2603.16666|Fast-WAM]] approach)
5. **Add action decoding** — Flow matching or inverse dynamics from predicted states

> See [[06_WAM#1. The Design Space]] for the three-axis trade-off analysis.

> [!tip] Start Simple, Add Complexity
> Begin with a VLA (simpler, faster to iterate). Add world model augmentation only if you need robustness to visual perturbations or physics-aware planning. The [[2603.16666|Fast-WAM]] finding: you can get WAM-level robustness with VLA-level speed by using video objectives at training time only.

^insight-6

#### The Self-Evolving Frontier

Both VLAs and WAMs can be made self-evolving — autonomously discovering failure modes and improving through experience. Three paths to self-evolution:

1. **RL Fine-Tuning** (VLA path): Apply reinforcement learning after initial imitation learning. The VLA explores, receives task-success reward, and adapts its policy. Simple and effective — VLAs are naturally resistant to catastrophic forgetting ([[2603.03818|VLA-Continual-Learning]]). Best for: in-domain improvement.
2. **Imagination Loops** (WAM path): The world model generates synthetic "dream" rollouts. The policy trains on dreams, improving without real-world interaction. [[2506.24119|SPIRAL]] and [[2502.05907|EvoAgent]] show this creates positive feedback loops. Best for: safe exploration, data-scarce settings.
3. **Curiosity-Driven Exploration**: The agent actively seeks states where its world model is uncertain ([[2503.01584|SENSEI]]) or where an adversary finds failures ([[2412.02818|RoboMD]]). This creates a self-directed curriculum that focuses practice on the agent's weaknesses.

The critical prerequisite for all three paths: **the agent must first detect that it IS failing**. See [[16_Self-Evolving-VLA-WAM]] for how failure detection, self-correction, and active probing enable the self-evolution loop.

---

## Part C — Frontier & Open Problems

*The open problems that still bound embodied-AI progress — the load-bearing constraints any new system must address.*

### 7. Open Problems & Key Challenges

| Challenge | Why It's Hard | Current Best Approach |
|-----------|--------------|----------------------|
| **Sim-to-real gap** | Physics simulators approximate reality; policies that work in sim break on real robots | Domain randomization + real-world fine-tuning ([[2405.05941\|SimplerEnv]] for evaluation) |
| **Data scarcity** | Real robot data is expensive ([[2212.06817\|RT-1]]: 17 months, 13 robots for 130K demos) | Cross-embodiment pre-training ([[2310.08864\|OXE]]) + world model imagination |
| **Real-time control** | Robots need actions at 10-50 Hz; large models are slow | Efficient VLAs ([[2506.01844\|SmolVLA]]: 450M params), [[2603.16666\|Fast-WAM]] (strip video at deploy) |
| **Safety** | Robots operate near humans; catastrophic failures are physical | Failure prediction ([[2510.09459\|FIPER]]), uncertainty-aware planning ([[2504.16680\|RWM-U]]) |
| **Generalization** | Novel objects, new environments, unseen instructions | Self-evolving systems that adapt from deployment experience |

---

> [!tip] Use This as a Reading Compass
> Each challenge points to the deep-dive note that treats it:
> sim-to-real → [[15_Sim-to-Real-Transfer]];
> data scarcity → [[02_Dataset-Benchmark-Environment]] + [[14_Egocentric-Pretraining-and-Human-Video]];
> real-time control → [[04_VLA]] §2 (efficient VLAs) + [[06_WAM]] §6 (efficient WAMs);
> safety → [[16_Self-Evolving-VLA-WAM]] §4 (failure detection);
> generalization → [[16_Self-Evolving-VLA-WAM]] §5–7 (self-evolving systems).

^insight-7

## Surveys & Further Reading

Landscape reviews for going deeper, grouped by theme. These broad surveys span the whole field rather than any single mechanism deep-dive — start here when you want a wide map before drilling into a specific note.

**The embodied field**
- [[2507.10087|Foundation-Robotics-Review]] — comprehensive review of foundation models (LLMs/VLMs/VLAs) across the robotics stack, from perception to control.
- [[2605.02900|Safety-in-Embodied-AI-Survey]] — multi-level taxonomy of risks, attacks, and defenses unique to AI that acts in the physical world.
- [[2510.04978|Physical-AI-Survey]] — surveys physical understanding across perception, reasoning, modeling, and interaction, asking why models learn correlation rather than causal physics.
- [[2407.06886|Aligning-Cyber-Space-with-Physical-World]] — broad post-2023 embodied-AI survey covering MLMs, world models, datasets, simulators, and embodied agents.
- [[2602.04411|Self-evolving-Embodied-AI]] — reviews agents that adapt autonomously in open, in-the-wild settings beyond fixed human-crafted configurations.
- [[2505.07634|Neural-Brain-Framework]] — neuroscience-inspired blueprint for a central intelligence system unifying perception, memory, and control in embodied agents.
- [[2212.14020|System-Level-OOD-Robotics]] — frames out-of-distribution data as a whole-stack robotics problem of safety in feedback loops, not just per-model robustness.
- [[2301.11972|Social-Cues-HRI-Survey]] — how robots can recognize their own task failures from human social cues during interaction — the prerequisite for self-correction.
- [[2508.10399|Large-Model-Embodied-AI-Survey]] — surveys large-model-empowered embodied AI across hierarchical and end-to-end decision-making and embodied-learning paradigms, naming data scarcity and the sim-to-real gap.
- [[2506.24044|VLA4AD-Survey]] — first structured overview of Vision-Language-Action models for autonomous driving (VLA4AD), categorizing 20+ models with their architectures, datasets, and challenges.
- [[2504.02477|Multimodal-Fusion-&-VLM-Survey]] — reviews multimodal fusion and VLMs for robot vision across 3D object detection, navigation, SLAM, and manipulation.
- [[2502.15336|Embodied-Multimodal-LLMs-Survey]] — full-stack review of Embodied Multimodal Large Models (EMLMs), spanning foundation models, embodied perception/navigation/interaction, datasets, and simulators.
- [[2408.03539|Deep-RL-for-Robotics-Survey]] — surveys real-world deep-RL successes in robotics with a novel taxonomy and a "Level of Real-World Success" metric assessing DRL maturity.
- [[2606.07017|FM-Agent-Sim-to-Real-Gap]] — recasts foundation-model agent robustness as a classical sim-to-real gap, dissecting observation/action/transition/reward discrepancies under a unified MDP perspective.
- [[2504.09848|LLM-Spatial-Intelligence-Survey]] — surveys LLM-powered spatial intelligence across scales, leading with embodied agents and linking cognitive-science principles to spatial-reasoning implementations.

**Manipulation & skill learning**
- [[2504.08438|Diffusion-for-Manipulation-Survey]] — first comprehensive survey of diffusion models in robotic manipulation, classifying applications, architectures, and adaptations for multi-modal distribution modeling.
- [[2503.09829|SE3-Equivariant-Survey]] — tutorial survey of SE(3)-equivariant methods in robot learning, showing how 3D symmetries improve data efficiency, generalization, and robustness in manipulation.
- [[2503.03464|GenAI-in-Manipulation-Survey]] — surveys generative AI in robotic manipulation, covering data synthesis, LLM task decomposition, and grasp/trajectory policy generation across operational layers.
- [[2507.05906|Feature-vs-GAN-LfD-Survey]] — compares feature-based vs GAN-based learning-from-demonstration, framing principled method selection by task priorities like fidelity vs diversity.
- [[2408.11537|Object-Centric-Manipulation-Survey]] — surveys embodied learning for object-centric manipulation, categorizing methods into perceptual, policy, and task-oriented learning.
- [[2510.10903|Manipulation-Survey-2025]] — unifies the fragmented robot-manipulation field under new taxonomies for high-level planning, low-level learning-based control, and key data/generalization bottlenecks.
- [[2512.11908|Contact-Rich-Safe-Learning-Survey]] — first safety-centric survey of learning-based contact-rich manipulation, with a taxonomy over learning phase, sensing modality, and enforcement space spanning classical control to safe foundation models.

**Navigation & mapping**
- [[2505.01458|Nav-&-Manip-Physics-Sim-Survey]] — analyzes how low-level physics-simulator properties shape robotic navigation and manipulation performance and sim-to-real transfer, guiding simulator selection.
- [[2504.15643|Goal-Oriented-Nav-Survey]] — introduces "inference domains" to categorize multimodal perception for goal-oriented navigation (PointNav, ObjectNav), highlighting sim-to-real challenges.
- [[2501.05750|Semantic-Mapping-Survey]] — systematic survey of semantic mapping in indoor embodied AI with a two-axis taxonomy over map structures and semantic encodings.
- [[2108.11544|VLN-Survey-&-Taxonomy]] — introduces a taxonomy for Vision-Language Navigation (VLN) that classifies tasks by language-instruction characteristics, mapping methodologies and open directions.

**World models & video-as-policy**
- [[2511.02097|WM-Manipulation-Survey]] — pins down what "world model" means for robotic manipulation, covering definitions, architectures, and a capability taxonomy.
- [[2604.04974|Video-to-Control-Survey]] — surveys interfaces that translate action-free temporal video into robot control, sidestepping costly action-labeled demos.
- [[2603.28489|Video-Gen-as-WM-Survey]] — efficiency-focused review of video generation models as world simulators, spanning paradigms, architectures, and algorithms for scalable video WMs.
- [[2604.22748|Agentic-World-Modeling-Survey]] — unifies "world model" across fields into foundations, capabilities, and scaling laws, with emphasis on agentic applications.
- [[2411.14499|World-Models-Survey]] — broad survey framed around the central debate: does a world model understand the present state or predict the future?
- [[2506.20134|3D-World-Models-Survey]] — traces the shift from 2D-visual world models to 3D-cognitive ones that simulate motion, contact, and causal reasoning.
- [[2602.01630|Unified-World-Model-Framework]] — argues world-model research is more than injecting knowledge into task-specific systems; proposes a unified, exploration-driven framing.
- [[2504.21853|Interactive-Generative-Video-Survey]] — frames interactive generative video across gaming, embodied AI, and autonomous driving via five modules (Generation, Control, Memory, Dynamics, Intelligence) — a video-as-controllable-policy taxonomy.

**3D & simulation for robotics**
- [[2512.03422|3D-Scene-Rep-Survey]] — compares geometric, neural (NeRF/3DGS), and foundation-model 3D scene representations across robotic perception, mapping, and manipulation.
- [[2604.26509|3D-Generation-for-Embodied-AI-Survey]] — surveys 3D content generation for simulation-ready, physically accurate assets, not just visual realism or static geometry.
- [[2504.13159|Digital-Twin-Survey]] — reviews digital-twin generation from visual data, centering 3D Gaussian Splatting as a unifying representation that captures geometry, appearance, dynamics, physics, and semantics.

**Multi-robot**
- [[2604.00061|R2X-Multi-Robot-MLLM-Survey]] — surveys multi-robot networks driven by MLLMs, joining sensing, communication, and computation for language-grounded coordination.

## Cross-References

The Embodied-AI deep-dives are organized in five blocks: substrate (02–03), model families (04–08), physical capabilities (09–12), scaling data (13), and deployment lifecycle (14–15). Read each note when its question is yours.

**Substrate: what you learn from**
- [[02_Dataset-Benchmark-Environment]] — Datasets, benchmarks, and simulation platforms; the data foundation for everything that follows
- [[03_Imitation-Learning-and-RL]] — Behavioral cloning, reward and inverse RL, and policy optimization; the core policy-learning paradigms

**Model families: the policy brain**
- [[04_VLA]] — Vision-Language-Action models; design-space principles, efficiency frontier, 3D-awareness, RL post-training, failure modes
- [[05_VLA-Reasoning-and-CoT]] — Reasoning insertion points in VLA pipelines; latent CoT, MCTS, draft-and-verify
- [[06_WAM]] — World Action Models; VideoGen, VLM-based, and from-scratch WAM architectures
- [[07_Latent-World-Models]] — JEPA evolution lineage; latent prediction as the bridge between video-WAMs and VLAs
- [[08_Physics-Aware-Embodied-AI]] — Physics priors for embodied AI; PINN integration, contact dynamics, physics-coupled pipelines

**Physical capabilities: the body**
- [[10_Manipulation-Skill-Learning]] — Manipulation policies; diffusion/flow backbones, 3D representations, dexterous grasping, planning, demo data
- [[11_Contact-Rich-and-Tactile-Control]] — Multi-sensor and force-aware control; tactile hardware, force-conditioned architectures, dexterous hands
- [[12_Whole-Body-and-Locomotion-Control]] — Humanoid whole-body control, legged locomotion, agile skills, motion retargeting, physics-based character motion
- [[13_Navigation-and-Mobile-Manipulation]] — Vision-language navigation, object-goal search, exploration, mobile manipulation

**Scaling data**
- [[14_Egocentric-Pretraining-and-Human-Video]] — Egocentric data → robot policy; scaling laws, hand→gripper transfer

**Deployment lifecycle**
- [[15_Sim-to-Real-Transfer]] — The reality gap; learned simulators, robust policies, digital twins, evaluation benchmarks
- [[16_Self-Evolving-VLA-WAM]] — Self-evolving systems; failure detection, RL post-training, imagination loops, persistent memory

---

*For a deep dive into VLA design, see [[04_VLA]]. For WAM papers by category, see [[06_WAM]]. For latent world models, see [[07_Latent-World-Models]]. For datasets and benchmarks, see [[02_Dataset-Benchmark-Environment]]. For self-evolving systems, see [[16_Self-Evolving-VLA-WAM]]. For physics-aware embodied AI, see [[08_Physics-Aware-Embodied-AI]]. For VLA reasoning and CoT, see [[05_VLA-Reasoning-and-CoT]]. For egocentric pretraining, see [[14_Egocentric-Pretraining-and-Human-Video]].*
