---
title: VLA vs WAM — 101
tags:
  - VLA
  - WAM
  - robotics
  - embodied-AI
aliases:
  - VLA vs WAM
  - VLA 101
  - WAM 101
---

# Vision-Language-Action (VLA) vs World Action Model (WAM)

The shift from ==Vision-Language-Action (VLA)== models to ==World Action Models (WAM)== represents a fundamental evolution in how AI agents and robots learn to interact with their environments. While VLAs rely heavily on imitating past actions, WAMs are designed to predict the future.

> [!abstract] One-Line Summary
> **VLAs** copy what they've seen. **WAMs** imagine what will happen next.

---

## Vision-Language-Action (VLA) Models

VLAs are essentially multimodal large language models fine-tuned for robotic control. Well-known examples include [[2307.15818|RT-2]] and [[2406.09246|OpenVLA]].

**How They Work:** They ingest visual observations (images of the environment) and language instructions (the goal), and directly output a sequence of discrete ==action tokens== (motor commands or waypoints).

**The Learning Paradigm:** VLAs primarily learn through ==behavioral cloning== — dense state-action imitation. They look at what an expert did in a specific situation and learn to map that exact visual state to that exact action.

> [!success] Strengths
> Built on robust vision-language backbones, VLAs excel at **semantic generalization**. If you tell a VLA to "pick up the red apple," it deeply understands what an apple is and what red looks like, even if the apple is slightly different from training data.

> [!warning] Limitations
> VLAs are effectively **"blind" to physics**. Because they only output an action, they do not inherently understand its physical consequences. This makes them struggle in novel environments with unseen physical dynamics, and they require thousands of carefully collected, repetitive expert demonstrations to learn a single task.

---

## World Action Models (WAM)

WAMs are an emerging class of foundation models (such as [[2602.15922|DreamZero]]) that unify action generation with a predictive "world model."

**How They Work:** Built on advanced ==video diffusion backbones== or autoregressive transformers, WAMs take in visual context and language instructions, but jointly predict ==future video frames== and the corresponding actions.

**The Learning Paradigm:** WAMs shift the learning process from imitation to ==inverse dynamics==. By forcing the model to generate the future visual state of the world (e.g., predicting exactly how an object will fall or deform when pushed), the model naturally learns "world physics priors." Motor commands are then aligned with these predicted visual futures.

> [!success] Strengths
> - **Zero-Shot Generalization:** WAMs can successfully execute unseen physical motions in novel environments on the first try.
> - **Data Efficiency:** They can learn from heterogeneous sources, including passive, video-only data (e.g., 10 minutes of a human performing a task), enabling cross-embodiment transfer without action labels.

> [!warning] Limitations
> WAMs are computationally expensive. Generating future video states alongside actions introduces high latency, requiring significant optimizations (decoupled noise schedules, KV-caching) to reach real-time control frequencies.

---

## Head-to-Head Comparison

| Feature | Vision-Language-Action (VLA) | World Action Models (WAM) |
| --- | --- | --- |
| Primary Output | Actions | Future visual states (video) + Actions |
| Learning Objective | Imitate expert actions | Predict world evolution + inverse dynamics |
| Physical Understanding | Implicit and often brittle | Explicit, grounded in physics priors |
| Data Reliance | Repetitive, action-labeled demonstrations | Diverse data, including passive video |
| Generalization | High semantic, low physical | Zero-shot task, environment, and embodiment |

---

## Deep Dive: Robotic Foundation Model Architectures

### Four Learning Strategies

| Strategy | How It Works | Limitation |
| --- | --- | --- |
| ==Model-Free== | Task-specific policy network maps states → actions | Poor semantic generality |
| ==Model-Based== | Explicit dynamics models decompose the task | Requires accurate dynamics; configuration-specific |
| ==WAM== | Predicts future goal-images, derives actions via inverse dynamics | Hard to learn for complex interactions (doors, deformables) |
| ==VLA== | Pre-trained VLMs encode state, predict actions directly | High compute for history-dependent processing |

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

> [!abstract] Current SOTA Configuration
> ==Policy Head fusion + Continuous Action Space== — best trade-off between reasoning capacity and inference efficiency.

**Representative models:** [[2310.08864|RT-2-X]], [[2406.09246|OpenVLA]] (one-step/discrete) · [[2405.12213|Octo]], [[2312.13139|GR-1]] (interleaved) · [[2311.01378|RoboFlamingo]] (policy head)

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
4. **Emergent self-correction** — top VLAs re-locate handles after a missed grasp without explicit error-recovery training; ==Mixture-of-Experts (MoE)== improves zero-shot generalization

> [!success] Ideal VLA Design Spec
> ==KosMos/[[2407.07726|PaliGemma]] backbone== + ==Policy Head fusion== + ==Continuous actions== + ==MoE== + ==Post-training on in-domain data==

---

## ELI5

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

## How to Build: The Open-Source Stack

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

---

*For a deep dive into VLA design, see [[03_VLA]]. For WAM papers by category, see [[04_WAM]].*
