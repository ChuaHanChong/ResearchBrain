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
> **VLAs** copy what they've seen. **WAMs** imagine what will happen next. **Self-evolving systems** improve from experience. See [[03_VLA]], [[04_WAM]], and [[06_Self-Evolving-VLA-WAM]] for deep dives.

---

## 1. Vision-Language-Action (VLA) Models

VLAs are essentially multimodal large language models fine-tuned for robotic control. Well-known examples include [[2307.15818|RT-2]] and [[2406.09246|OpenVLA]].

**How They Work:** They ingest visual observations (images of the environment) and language instructions (the goal), and directly output a sequence of discrete ==action tokens== (motor commands or waypoints).

**The Learning Paradigm:** VLAs primarily learn through ==behavioral cloning== — dense state-action imitation. They look at what an expert did in a specific situation and learn to map that exact visual state to that exact action.

> [!success] Strengths
> Built on robust vision-language backbones, VLAs excel at **semantic generalization**. If you tell a VLA to "pick up the red apple," it deeply understands what an apple is and what red looks like, even if the apple is slightly different from training data.

> [!warning] Limitations
> VLAs are effectively **"blind" to physics**. Because they only output an action, they do not inherently understand its physical consequences. This makes them struggle in novel environments with unseen physical dynamics, and they require thousands of carefully collected, repetitive expert demonstrations to learn a single task.

---

## 2. World Action Models (WAM)

WAMs are an emerging class of foundation models (such as [[2602.15922|DreamZero]]) that unify action generation with a predictive "world model."

**How They Work:** Built on advanced ==video diffusion backbones== or autoregressive transformers, WAMs take in visual context and language instructions, but jointly predict ==future video frames== and the corresponding actions.

**The Learning Paradigm:** WAMs shift the learning process from imitation to ==inverse dynamics==. By forcing the model to generate the future visual state of the world (e.g., predicting exactly how an object will fall or deform when pushed), the model naturally learns "world physics priors." Motor commands are then aligned with these predicted visual futures.

> [!success] Strengths
> - **Zero-Shot Generalization:** WAMs can successfully execute unseen physical motions in novel environments on the first try.
> - **Data Efficiency:** They can learn from heterogeneous sources, including passive, video-only data (e.g., 10 minutes of a human performing a task), enabling cross-embodiment transfer without action labels.

> [!warning] Limitations
> WAMs are computationally expensive. Generating future video states alongside actions introduces high latency, requiring significant optimizations (decoupled noise schedules, KV-caching) to reach real-time control frequencies.

---

## 3. Head-to-Head Comparison

| Feature | Vision-Language-Action (VLA) | World Action Models (WAM) |
| --- | --- | --- |
| Primary Output | Actions | Future visual states (video) + Actions |
| Learning Objective | Imitate expert actions | Predict world evolution + inverse dynamics |
| Physical Understanding | Implicit and often brittle | Explicit, grounded in physics priors |
| Data Reliance | Repetitive, action-labeled demonstrations | Diverse data, including passive video |
| Generalization | High semantic, low physical | Zero-shot task, environment, and embodiment |

**When to Choose VLA**: Your task is language-heavy (complex instructions), you have abundant demonstration data, and inference speed matters (real-time control at 10-50Hz). VLAs inherit semantic understanding from web-scale VLM pre-training, making them strong at understanding novel instructions. **When to Choose WAM**: You need robustness to visual perturbations (lighting, camera, background changes), your task requires physics-aware planning (predicting consequences of actions), or real-world training data is limited (world model imagination compensates). **When to Combine**: The 2026 consensus is converging on integration — Fast-WAM and VLA-JEPA show you can get WAM-level robustness with VLA-level speed by using world model objectives during training only.

---

## 4. Robotic Foundation Model Architectures

### Four Learning Strategies

| Strategy | How It Works | Limitation |
| --- | --- | --- |
| ==Model-Free== | Task-specific policy network maps states → actions | Poor semantic generality |
| ==Model-Based== | Explicit dynamics models decompose the task | Requires accurate dynamics; configuration-specific |
| ==WAM== | Predicts future goal-images, derives actions via inverse dynamics | Hard to learn for complex interactions (doors, deformables) |
| ==VLA== | Pre-trained VLMs encode state, predict actions directly | High compute for history-dependent processing |

**Model-Free** approaches (DQN, SAC, PPO) learn a direct mapping from observations to actions through trial and error. They are powerful for specific tasks but require millions of environment interactions and don't transfer well to new tasks. **Model-Based** approaches (MPC, MBPO) learn an explicit dynamics model and use it for planning. They are sample-efficient but require accurate dynamics — errors in the model compound during long-horizon planning. **WAMs** take model-based to the extreme: learn dynamics from internet-scale video, then derive actions via inverse dynamics. The video backbone provides rich physics priors but makes the model large and slow. **VLAs** bypass explicit dynamics entirely: the VLM backbone provides implicit physical understanding from web-scale pre-training, and the model directly predicts actions. This is simpler and faster, but the physical understanding is brittle — it hasn't truly 'learned' physics, just correlated visual patterns with actions.

> [!tip] WAM vs VLA — The Key Differentiator
> WAMs predict a future goal-state then calculate actions via inverse dynamics — powerful but hard to learn for complex physics. VLAs bypass explicit world-modeling by inheriting spatial reasoning from web-scale VLM pre-training, mapping observations directly to control signals.

### VLA Architecture Taxonomy

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

==Flow Matching== has emerged as the dominant continuous-action recipe: [[2410.24164|π0]] established it for VLAs, [[2503.20314|Wan]] scaled it for video-conditioned generation, [[2504.18471|Action Flow Matching]] adapted it for continual robot learning, and [[2505.05470|Flow-GRPO]] showed RL fine-tuning works directly on flow-matching policies — closing the loop between flow-matching SFT and RL post-training.

> [!abstract] Current SOTA Configuration (2026)
> ==Policy Head fusion + Continuous Action Space + Flow-Matching action expert + MoE backbone== — best trade-off between reasoning capacity, throughput, and zero-shot generalization. Frontier exemplars: [[2604.15483|π0.7]] (steerable generalist), [[2602.15922|DreamZero]] (joint video+action 14B WAM), [[2602.10098|VLA-JEPA]] (latent world model + flow head), and [[2603.16666|Fast-WAM]] (training-time video, deployment-time speed).

**Representative models:** [[2310.08864|RT-2-X]], [[2406.09246|OpenVLA]] (one-step/discrete) · [[2405.12213|Octo]], [[2312.13139|GR-1]] (interleaved) · [[2311.01378|RoboFlamingo]] (policy head) · [[2604.07430|HY-Embodied-0.5]] (MoT-MoE multi-embodiment)

### Data Strategy

Three training recipes for bridging sim-to-real:

1. **Co-training** — simultaneous in-domain + cross-embodiment (OXE) data
2. **Post-training** — co-train on diverse data, then refine on in-domain only
3. **Fine-tuning** — in-domain data exclusively

> [!warning] In-domain data is non-negotiable
> Even task-agnostic data from the *same robot* outperforms massive cross-embodiment datasets for target tasks. ==Post-training== (diverse pre-train → in-domain refinement) yields the best generalization.

### Key Empirical Findings

1. **Generalization** — VLAs achieved a **30.3%** improvement on 5-task chains in unseen CALVIN scenes
2. **Backbone matters** — KosMos and [[2407.07726|PaliGemma]] outperform others due to stronger vision-language alignment from larger pre-training datasets
3. **Continuous > Discrete** — continuous actions avoid compounding discretization errors; Flow Matching offers slight gains over MSE
4. **Emergent self-correction** — top VLAs re-locate handles after a missed grasp without explicit error-recovery training; ==Mixture-of-Experts (MoE)== improves zero-shot generalization. Frontier MoE/MoT examples: [[2604.07430|HY-Embodied-0.5]] (MoT for multi-embodiment), [[2603.15169|ForceVLA2]] (Cross-Scale MoE for force fusion), [[2603.07648|AtomicVLA]] (SG-MoE for skill abstraction).

> [!success] Ideal VLA Design Spec
> ==KosMos/[[2407.07726|PaliGemma]] backbone== + ==Policy Head fusion== + ==Continuous actions (Flow Matching)== + ==MoE== + ==Post-training on in-domain data==

---

## 5. ELI5

> [!example] Catching a Ball
> Imagine you are teaching a robot how to catch a ball. Here is how the two robot brains would learn:

### The VLA Brain (The Memorizer)

This robot learns by playing **"Simon Says."** You throw the ball exactly the same way 100 times, and you move the robot's arm to the exact right spot to catch it. The robot memorizes, "When I hear 'catch' and see the ball right *here*, I move my arm exactly like *this*."

It is really good at following instructions and recognizing the ball, but it doesn't actually understand how gravity works. If the wind blows the ball a little to the left, or you use a heavier ball, the robot will probably miss because it only knows the exact movements it memorized.

### The WAM Brain (The Imaginer)

This robot learns by **daydreaming**. Instead of just memorizing arm movements, it watches videos of balls flying through the air and bouncing. When you throw the ball to this robot, its brain actually imagines the future. It thinks, "If the ball is moving this fast, it will land over *there* in two seconds."

Because it actually understands the rules of the world (like gravity and momentum) and can picture what is about to happen, it can figure out how to move its arm to catch the ball — even if it's a brand new bouncy ball or the wind is blowing.

> [!summary] The Short Version
> - **VLAs** learn by copying exactly what they have seen before.
> - **WAMs** learn by imagining what will happen next and acting based on that picture.

---

## 6. How to Build: The Open-Source Stack

The open-source robotics ecosystem now provides every component needed to build, train, and deploy both VLAs and WAMs — from data to deployment on a $100 robot arm.

### The Pipeline

```
Researcher → Data → Training → Simulation → Deployment
             OXE    LeRobot    Genesis       SO-100
```

| Component | Tool | Role |
|-----------|------|------|
| **Data** | [[2310.08864\|Open X-Embodiment]] | 1M+ cross-embodiment trajectories for pre-training |
| **Training Framework** | [LeRobot (HuggingFace)](https://github.com/huggingface/lerobot) | End-to-end training pipeline for VLAs (OpenVLA, ACT, Diffusion Policy) |
| **Simulation** | [Genesis](https://genesis-world.readthedocs.io/en/latest/), [Newton (NVIDIA)](https://developer.nvidia.com/newton-physics) | Physics-accurate simulation for verification before real-world deployment |
| **Hardware** | [SO-100](https://github.com/TheRobotStudio/SO-ARM100) (~$100) | Low-cost robot arm for real-world testing and deployment |

### Building a VLA (Quick Recipe)

1. **Pick a VLM backbone** — [[2407.07726\|PaliGemma]] or KosMos (best vision-language alignment)
2. **Add an action head** — Policy Head with continuous actions via ==Flow Matching==
3. **Pre-train on OXE** — cross-embodiment data for broad priors
4. **Post-train on in-domain data** — fine-tune on your specific robot + tasks
5. **Deploy** — use ==FAST== tokenization for real-time inference

> See [[03_VLA#2. Design-Space Principles]] for the full design-space analysis.

### Building a WAM (Quick Recipe)

1. **Choose your prediction space** — Pixel (richest but slowest), Latent (fastest), or Action-only (most efficient)
2. **Pick a backbone** — Video diffusion (Cosmos/DreamZero), JEPA (V-JEPA 2), or RSSM (Dreamer lineage)
3. **Pre-train on video** — internet-scale video teaches physics priors
4. **Decide test-time strategy** — Full imagination (robust but 4.8x slower) or training-only video (Fast-WAM approach)
5. **Add action decoding** — Flow matching or inverse dynamics from predicted states

> See [[04_WAM#1. The Design Space]] for the three-axis trade-off analysis.

> [!tip] Start Simple, Add Complexity
> Begin with a VLA (simpler, faster to iterate). Add world model augmentation only if you need robustness to visual perturbations or physics-aware planning. The [[2603.16666|Fast-WAM]] finding: you can get WAM-level robustness with VLA-level speed by using video objectives at training time only.

### The Self-Evolving Frontier

Both VLAs and WAMs can be made self-evolving — autonomously discovering failure modes and improving through experience. Three paths to self-evolution:

1. **RL Fine-Tuning** (VLA path): Apply reinforcement learning after initial imitation learning. The VLA explores, receives task-success reward, and adapts its policy. Simple and effective — VLAs are naturally resistant to catastrophic forgetting ([[2603.03818|VLA Continual Learning]]). Best for: in-domain improvement.
2. **Imagination Loops** (WAM path): The world model generates synthetic "dream" rollouts. The policy trains on dreams, improving without real-world interaction. SPIRAL and EvoAgent show this creates positive feedback loops. Best for: safe exploration, data-scarce settings.
3. **Curiosity-Driven Exploration**: The agent actively seeks states where its world model is uncertain (SENSEI) or where an adversary finds failures (RoboMD). This creates a self-directed curriculum that focuses practice on the agent's weaknesses.

The critical prerequisite for all three paths: **the agent must first detect that it IS failing**. See [[06_Self-Evolving-VLA-WAM]] for how failure detection, self-correction, and active probing enable the self-evolution loop.

### Key Challenges in Embodied AI

| Challenge | Why It's Hard | Current Best Approach |
|-----------|--------------|----------------------|
| **Sim-to-real gap** | Physics simulators approximate reality; policies that work in sim break on real robots | Domain randomization + real-world fine-tuning (SimplerEnv for evaluation) |
| **Data scarcity** | Real robot data is expensive (RT-1: 17 months, 13 robots for 130K demos) | Cross-embodiment pre-training (OXE) + world model imagination |
| **Real-time control** | Robots need actions at 10-50 Hz; large models are slow | Efficient VLAs (SmolVLA: 450M params), Fast-WAM (strip video at deploy) |
| **Safety** | Robots operate near humans; catastrophic failures are physical | Failure prediction (FIPER), uncertainty-aware planning (RWM-U) |
| **Generalization** | Novel objects, new environments, unseen instructions | Self-evolving systems that adapt from deployment experience |

---

*For a deep dive into VLA design, see [[03_VLA]]. For WAM papers by category, see [[04_WAM]]. For latent world models, see [[05_Latent-World-Models]]. For datasets and benchmarks, see [[02_Dataset-Benchmark-Environment]]. For self-evolving systems, see [[06_Self-Evolving-VLA-WAM]]. For physics-aware embodied AI, see [[07_Physics-Aware-Embodied-AI]]. For VLA reasoning and CoT, see [[08_VLA-Reasoning-and-CoT]]. For egocentric pretraining, see [[09_Egocentric-Pretraining-and-Human-Video]].*
