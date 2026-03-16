---
title: World Action Models — Survey
tags:
  - robotics
  - world-models
  - VLA
  - WAM
  - survey
---

%%
PROMPT:
Based on @VLA-WAM/KnowledgeHub_VLA-WAM.json, briefly explain the differences between world action models derived from video generation, world action models derived from vision-language models, and world action models trained from scratch. Then, for each category, briefly explain the key ideas of the papers. You may group the papers if they share similar ideas, and you can also highlight the papers that you find most interesting.

You may only refer to the papers in the list below and should not refer to any other papers.

World Action Models from VideoGen (12 papers)
- https://arxiv.org/abs/2602.15922  # DreamZero
- https://arxiv.org/abs/2601.16163  # Cosmos Policy
- https://arxiv.org/abs/2601.21998  # Lingbot-VA
- https://arxiv.org/abs/2512.15692  # mimic-video
- https://arxiv.org/abs/2508.00795  # Video Policy
- https://arxiv.org/abs/2505.12705  # DreamGen
- https://arxiv.org/abs/2504.15369  # Inverse Probabilistic Adaptation
- https://arxiv.org/abs/2412.14803  # VPP
- https://arxiv.org/abs/2410.06158  # GR-2
- https://arxiv.org/abs/2312.13139  # GR-1
- https://arxiv.org/abs/2310.10625  # VLP
- https://arxiv.org/abs/2302.00111  # UniPi

World Action Models from VLM (11 papers)
- https://arxiv.org/abs/2602.12063  # VLAW
- https://arxiv.org/abs/2602.22010  # WoG
- https://arxiv.org/abs/2602.10098  # VLA-JEPA
- https://arxiv.org/abs/2512.00975  # MM-ACT
- https://arxiv.org/abs/2511.17502  # RynnVLA-002
- https://arxiv.org/abs/2509.06951  # F1
- https://arxiv.org/abs/2508.18269  # FlowVLA
- https://arxiv.org/abs/2507.04447  # DreamVLA
- https://arxiv.org/abs/2506.21539  # WorldVLA
- https://arxiv.org/abs/2503.22020  # CoT-VLA
- https://arxiv.org/abs/2501.18867  # UP-VLA

World Action Models from Scratch (7 papers)
- https://arxiv.org/abs/2504.02792  # Unified World Models
- https://arxiv.org/abs/2503.00200  # UVAM
- https://arxiv.org/abs/2412.15109  # Seer
- https://arxiv.org/abs/2310.08576  # AVDC
- https://arxiv.org/abs/2310.06114  # UniSim
- https://arxiv.org/abs/2206.14176  # DayDreamer
- https://arxiv.org/abs/2205.09991  # Diffusers
%%

# World Action Models (WAM) — Survey

> [!abstract] Overview
> World Action Models (WAMs) jointly predict future world states and robot actions, giving robots physical grounding that pure Vision-Language-Action (VLA) models lack. Three distinct paradigms have emerged, differing in **where the world knowledge comes from**.

## Three Paradigms at a Glance

| | VideoGen-based | VLM-based | From Scratch |
| --- | --- | --- | --- |
| **World model source** | Pre-trained video generator | Future-state prediction added to VLM | Purpose-built joint architecture |
| **Strength** | Internet-scale visual dynamics | Semantic + physical reasoning | Flexible data, clean design |
| **Weakness** | Inference speed; fine-tuning complexity | World model quality limited by VLM | Requires joint training from scratch |
| **Key example** | [[#DreamZero]] | [[#VLAW]] | [[#Unified World Models]] |

---

## World Action Models from VideoGen

> [!tip] Core Idea
> Large video generation models have already learned how the physical world works from millions of internet videos. Rather than teaching a robot physics from scratch, fine-tune or repurpose a video backbone that already understands visual dynamics.

### Group 1 — Planning as Video Generation (Foundational)

**[[UniPi]]** (2302) and **[[VLP]]** (2310) establish the paradigm: treat a robot policy as a text-conditioned video generator. Generate a plausible future video, then extract actions from it. UniPi demonstrated combinatorial generalization and multi-environment transfer; VLP extended this to long-horizon tree-search. Conceptually elegant but slow — video generation at inference isn't real-time.

### Group 2 — GPT-Style Video Pretraining

**[[GR-1]]** (2312) and **[[GR-2]]** (2410) from ByteDance use a GPT-style transformer pretrained on large egocentric video datasets. Video pretraining acts as world-model initialization that dramatically improves data efficiency. GR-2 added web-scale knowledge and hit 97.7% on multi-task tabletop manipulation.

### Group 3 — Fine-Tuning Video Diffusion Models

**[[Cosmos Policy]]** (2601), **[[mimic-video]]** (2512), **[[VPP]]** (2412), and **[[Lingbot-VA]]** (2601) all fine-tune pre-trained video diffusion models into robot policies.

- **Cosmos Policy** fine-tunes NVIDIA's Cosmos-Predict2 latent diffusion model, achieving 98.5% on LIBERO — among the highest scores in the field.
- **VPP** extracts predictive visual representations from a video diffusion model in a *single forward pass* (no iterative denoising at inference), keeping latency low.
- **mimic-video** reports 10× sample efficiency and 2× faster convergence vs. VLAs.

### Group 4 — Video Models as Data Engines

**[[DreamGen]]** (2505) and **[[Inverse Probabilistic Adaptation]]** (2504) use video models not as policies, but as synthetic data generators. DreamGen synthesizes demonstrations for 22 novel behaviors without additional teleoperation. Inverse Probabilistic Adaptation adapts internet video knowledge to solve new robot tasks, improving success rates up to 3×.

### ⭐ DreamZero (2602)

> [!star] Most Interesting
> NVIDIA's **DreamZero** is a 14B WAM that *jointly* generates future video frames and actions in a single autoregressive diffusion transformer — not sequentially. It achieves 39.5% on completely unseen tasks (vs. 16.3% for VLA baselines), enables cross-embodiment transfer from just 10–20 minutes of video-only demonstrations, and runs at 7Hz real-time via decoupled noise schedules and async execution (DreamZero-Flash).

---

## World Action Models from VLM

> [!tip] Core Idea
> VLMs are excellent at semantic reasoning but blind to physical consequence. Augment the VLA architecture with a world model component — forcing the model to predict what will happen next grounds language reasoning in physical prediction.

### Group 1 — Visual Chain-of-Thought (Subgoal Image Prediction)

**[[CoT-VLA]]** (2503), **[[F1]]** (2509), and **[[UP-VLA]]** (2501) add "visual chain-of-thought" — predict a future subgoal image before generating actions.

- **CoT-VLA** uses large-scale action-less video data to train the subgoal predictor, boosting performance by 17% over VLA baselines.
- **UP-VLA** achieves 33% improvement on CALVIN ABC→D generalization tasks.
- **F1** adds "explicit visual foresight," improving robustness in dynamic environments.

### Group 2 — Compact Motion Representations

**[[FlowVLA]]** (2508) and **[[WoG]]** (2602) use efficient intermediate representations rather than full image generation.

- **FlowVLA** reasons about optical flow before generating future frames — physically coherent predictions without full video synthesis cost.
- **WoG** compresses future observations into a compact "condition space," resolving the efficiency-vs-quality tradeoff.

### Group 3 — Unified Policy + World Model

**[[WorldVLA]]** (2506), **[[RynnVLA-002]]** (2511), and **[[VLAW]]** (2602) fully unify the policy and world model in a single autoregressive framework.

- **WorldVLA** jointly models robot actions and environmental state forecasting in one autoregressive model.
- **RynnVLA-002** integrates environmental dynamics learning with action planning in a unified VLA-WM.

### Group 4 — Latent World Models

**[[VLA-JEPA]]** (2602) and **[[DreamVLA]]** (2507) predict future *embeddings* rather than images, reducing computational cost significantly.

- **VLA-JEPA** integrates a Joint-Embedding Predictive Architecture (JEPA), learning robust dynamics abstractions from human videos and robot data.
- **DreamVLA** forecasts multi-modal future knowledge (dynamic regions, depth, semantics) rather than just RGB frames.

**[[MM-ACT]]** (2512) takes a different angle: a shared token space for text, image, and robot actions, enabling efficient parallel generation at 96.3% success rate on LIBERO.

### ⭐ VLAW (2602)

> [!star] Most Interesting
> **VLAW's** iterative co-improvement loop is architecturally elegant: the VLA policy and world model bootstrap each other. The world model generates synthetic rollouts to train the policy; the policy's real-world experience grounds the world model. Only limited real-world interaction is needed, yet achieves a 39% performance improvement.

---

## World Action Models from Scratch

> [!tip] Core Idea
> Design a unified architecture where video and action are co-equal first-class citizens from day one — no borrowed backbone. These models can train on heterogeneous data (labeled and unlabeled) and define the cleanest abstractions.

### Group 1 — The Foundational Papers

**[[Diffuser]]** (2205) and **[[DayDreamer]]** (2206) are the intellectual ancestors of the field.

- **Diffuser** (Janner et al., Berkeley/MIT) is the key conceptual paper: treat robot planning as *trajectory denoising* — apply DDPM to entire state-action sequences rather than step-by-step. This unified dynamics, reward, and planning in a single model. A warm-start trick reduced inference from 256 to 25 diffusion steps.
- **DayDreamer** adapts Dreamer (latent world model via RSSM) to physical robots — no simulator, no demonstrations, learning from scratch in a compact latent space.

### Group 2 — Learning from Actionless Video

**[[AVDC]]** (2310) and **[[UniSim]]** (2310) tackle a specific problem: most internet video has no action labels.

- **AVDC** synthesizes future video plans via diffusion, then extracts 3D robot actions from dense optical flow — no action labels needed during training.
- **UniSim** trains a universal video diffusion model on heterogeneous datasets and uses it as an interactive simulator to train downstream RL policies with zero-shot sim-to-real transfer.

### Group 3 — Modern Unified Architectures

**[[UWM]]** (Unified World Models, 2504), **[[UVAM]]** (2503), and **[[Seer]]** (2412) are the contemporary "from scratch" approaches.

- **UWM** uses a single diffusion transformer with *shared weights* for both policy and world model, training on action-labeled and unlabeled robot data simultaneously.
- **UVAM** (Stanford) jointly models video and action in a unified framework with competitive performance and efficient inference.
- **Seer** uses a predictive inverse dynamics model: predict future visual states, then infer actions from the visual change.

### ⭐ Diffuser (2205) and UWM (2504)

> [!star] Most Interesting
> **Diffuser** deserves credit for the paradigm shift — treating trajectory optimization as denoising is conceptually beautiful and technically generative of most subsequent work. **UWM** is the most architecturally clean modern approach: one shared-weight transformer handles both policy and world model, trained on heterogeneous data without requiring action labels on all samples.
