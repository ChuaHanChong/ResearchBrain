---
title: "Latent World Models — Deep Dive"
tags:
  - JEPA
  - self-supervised-learning
  - world-model
  - VLA
  - video-understanding
  - reasoning
aliases:
  - "Latent World Models"
  - "JEPA Deep Dive"
---

# Latent World Models — Deep Dive

> [!abstract] Overview
> Latent world models predict future states in representation space rather than pixel space — faster, more robust to visual noise, and better suited for real-time robot control. This note covers the JEPA family (the dominant latent prediction architecture), other latent approaches ([[2411.04983|DINO-WM]], [[2504.02792|UWM]], [[2512.13030|Motus]]), and **latent reasoning for embodied AI** — using continuous thought and latent planning to enable smarter, faster robot decision-making.

## Evolution Graph

```text
1. JEPA Foundations   (predict in representation space)
· the JEPA line
                     +video               +robot transfer        +refined
╔═══════════════╗    ┌───────────────┐    ╔═════════════════╗    ┌───────────────────┐
║ I-JEPA (2023) ║───►│ V-JEPA (2025) │───►║ V-JEPA-2 (2025) ║───►│ V-JEPA-2.1 (2026) │
╚═══════════════╝    └───────────────┘    ╚═════════════════╝    └───────────────────┘

· self-supervised objectives
┌────────────┐
│ IWM (2024) │─┐
└────────────┘ │
               │    +sequential
               │    ┌─────────────────┐
               ├───►│ seq-JEPA (2025) │
               │    └─────────────────┘
               │    +language              +provable            +kernel view
               │    ┌─────────────────┐    ┌───────────────┐    ┌────────────────┐
               └───►│ LLM-JEPA (2025) │───►│ LeJEPA (2025) │───►│ KerJEPA (2025) │
                    └─────────────────┘    └───────────────┘    └────────────────┘

2. JEPA for Control   (latent prediction that drives a policy)
· latent prediction for RL
┌────────────────────┐
│ JEPA-for-RL (2025) │─┐
└────────────────────┘ │
                       │    +temporal
                       │    difference            +action grounding
                       │    ┌────────────────┐    ╔═════════════════╗
                       ├───►│ TD-JEPA (2025) │───►║ VLA-JEPA (2026) ║
                       │    └────────────────┘    ╚═════════════════╝
                       │    +reasoning
                       │    ┌──────────────────┐
                       └───►│ ThinkJEPA (2026) │
                            └──────────────────┘

3. Latent World Models   (roll the future forward in latent)
· latent dynamics for policy
                       +frozen features
┌─────────────────┐    ╔════════════════╗
│ OccWorld (2023) │───►║ DINO-WM (2024) ║─┐
└─────────────────┘    ╚════════════════╝ │
                                          │    +adaptable
                                          │    ┌─────────────────┐
                                          ├───►│ AdaWorld (2025) │
                                          │    └─────────────────┘
                                          │    +diffusion latent     +motion latent
                                          │    ┌────────────────┐    ┌──────────────┐
                                          └───►│ LaDi-WM (2025) │───►│ Motus (2025) │
                                               └────────────────┘    └──────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

Three lanes. The JEPA line is a version chain — [[2301.08243|I-JEPA]] to [[2603.14482|V-JEPA-2.1]], each release superseding the last — while the objectives thread forks at [[2403.00504|IWM]] into one short offshoot and a three-paper theory line ending at [[2512.19605|KerJEPA]]. JEPA for control grounds the idea in actions ([[2602.10098|VLA-JEPA]]) or in reasoning ([[2603.22281|ThinkJEPA]]). Latent world models roll the future forward for a policy, forking at [[2411.04983|DINO-WM]] into adaptable and generative latents.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2023 | [[2301.08243\|I-JEPA]] | JEPA · Foundations | The foundational JEPA architecture predicting masked image-patch embeddings from visible-patch context via a context encoder |
| 2023 | [[2311.16038\|OccWorld]] | Latent World Model | The autonomous-driving 3D occupancy world model origin of the recipe RoboOccWorld adapts indoors: a sel |
| 2024 | [[2403.00504\|IWM]] | JEPA · Objectives | A LeCun-coauthored JEPA extension predicting photometric transformations in latent space via an encoder + EMA target |
| 2024 | [[2411.04983\|DINO-WM]] | Latent World Model | A task-agnostic latent dynamics model on frozen DINOv2 features via latent consistency loss, where MPC+ |
| 2025 | [[2502.11831\|V-JEPA]] | JEPA · Foundations | The original video JEPA predicting masked video regions in abstract representation space |
| 2025 | [[2503.18938\|AdaWorld]] | Latent World Model | A Latent Action Autoencoder that extracts context-invariant latent actions from action-free videos via beta-VAE information |
| 2025 | [[2504.16591\|JEPA-for-RL]] | JEPA · Control | A JEPA adapted for image-based RL: separate context/target ViT encoders combined with actor-critic gradient back-propagation |
| 2025 | [[2505.03176\|seq-JEPA]] | JEPA · Objectives | An Action-conditioned sequence JEPA with a transformer sequence aggregator whose aggregate output is invariant |
| 2025 | [[2505.11528\|LaDi-WM]] | Latent World Model | A latent WM combining DINOv2+SigLIP features with imagination-guided iterative action refinement |
| 2025 | [[2506.09985\|V-JEPA-2]] | JEPA · Foundations | A video-scale JEPA that scales I-JEPA to **1M+ hours** of video with a mask-denoising objective |
| 2025 | [[2509.14252\|LLM-JEPA]] | JEPA · Objectives | An LLM JEPA adding a JEPA loss on multi-view text-code pairs alongside autoregressive LM loss |
| 2025 | [[2510.00739\|TD-JEPA]] | JEPA · Control | A JEPA adapted to a temporal-difference framework for multi-step policy-conditioned latent dynamics with asymmetric state |
| 2025 | [[2511.08544\|LeJEPA]] | JEPA · Objectives | A Provable and scalable SSL framework based on Euclidean latent geometry and SIGReg |
| 2025 | [[2512.13030\|Motus]] | Latent World Model | A Mixture-of-Transformer unifying VLM understanding + video generation + an Action Expert via Tri-model Joint Attention |
| 2025 | [[2512.19605\|KerJEPA]] | JEPA · Objectives | A kernel-discrepancy JEPA generalizing LeJEPA's regularization to kernel discrepancies (MMD + Kernel St |
| 2026 | [[2602.10098\|VLA-JEPA]] | JEPA · Control | A full Vision-Language-Action stack pairing the JEPA principle with a flow-matching action head |
| 2026 | [[2603.14482\|V-JEPA-2.1]] | JEPA · Foundations | A dense-feature JEPA re-acquiring local detail via dense predictive loss (masked + unmasked tokens) |
| 2026 | [[2603.22281\|ThinkJEPA]] | JEPA · Control | A VLM-thinker + JEPA latent WM with dual-temporal perception + hierarchical pyramid feature injection |

---

## Part A — The JEPA Family

*The foundational principle and its evolution across V-JEPA 2 → 2.1 → VL-JEPA → VLA-JEPA — the dominant latent-world-model lineage.*

### 1. The JEPA Principle

The Joint Embedding Predictive Architecture (JEPA) was proposed by Yann LeCun as an alternative to both contrastive learning and generative models. The core insight — *predict in representation space, not pixel space* — sits in opposition to both other self-supervised paradigms: generative models pay the full cost of pixel reconstruction; contrastive models only learn similarity invariances; JEPA splits the difference by learning forward dynamics in a compressed embedding.

The three families correspond to three different bets on *what is worth predicting*: rendering quality (generative), pair distinctness (contrastive), or future-state semantics (JEPA). For robot control where the bottleneck is "what matters for manipulation, not how it looks", the JEPA bet pays off — but at the cost of opacity and a learned target that can collapse without careful design.

#### 1.1 Generative Self-Supervision

==Reconstruct pixels or tokens== from a corrupted input. Maximally rich and human-interpretable but wastes capacity modeling textures, shadows, and lighting irrelevant to control.

- **[[2607.06856|Gen4U]]** — Extracts ==intermediate spatiotemporal activations== from frozen ==Veo3==/==Wan 2.2== video diffusion at a ==~60% noise semantic bottleneck== via one forward pass; **72.6%** SSv2 (beats V-JEPA-H), **0.075** AbsRel depth — complicates the "wasted capacity" framing below.
- **[[2602.15922|DreamZero]]** (14B Video DiT) — The canonical pixel-space generative WM whose ==autoregressive diffusion transformer== spends most of its capacity on visual fidelity the policy never uses for action selection; ~**150 ms/forward**.
- **MAE / latent-diffusion family** — masked-autoencoder reconstruction; produces strong visual features but no dynamics signal.

#### 1.2 Contrastive Self-Supervision

==Pull positive pairs together, push negatives apart== via InfoNCE / SimCLR / DINO objectives. Learns view-invariant features cheaply but contains no forward-dynamics signal — useless on its own for prediction-based planning.

- **[[2304.07193|DINOv2]]** — A model doing ==discriminative SSL with Sinkhorn-Knopp centering + KoLeo regularizer== on automatically-curated ==LVD-142M== (**142M** images), with ViT-g/14 reaching **86.5%** ImageNet linear probe (**+4.2%** over prior SSL) and **+34% mAP** on Oxford-Hard retrieval; the "no dynamics, rich invariances" substrate [[2411.04983|DINO-WM]] later built on.
- **CLIP / SigLIP** — vision-language contrastive alignment; pairs naturally with JEPA targets in [[2605.06388|Semantic-LDM-WM]] (see [[06_WAM#3.2 Unified Latent Diffusion]]).

#### 1.3 JEPA (Joint Embedding Predictive Architecture)

==Predict future embeddings of an EMA-updated target encoder== from a partial-view context encoder. Splits the difference: dynamics signal without pixel cost, semantic compression without losing forward-prediction structure.

- **[[2301.08243|I-JEPA]]** — The foundational JEPA architecture predicting masked image-patch embeddings from visible-patch context via a ==context encoder==, a ==predictor== on positional masks, and an EMA ==target encoder==; **81.1%** ImageNet-1K linear probe at **10x less** pretraining compute than MAE, the EMA asymmetry blocking collapse without negative pairs.
- **[[2502.11831|V-JEPA]]** — The original video JEPA predicting masked video regions in ==abstract representation space==, evaluated via a ==violation-of-expectation== framework; **98%** IntPhys physics-violation accuracy from just **1 week** of video — the first demonstration that intuitive physics emerges from latent prediction without hard-coded core-knowledge priors.
- **[[2506.09985|V-JEPA-2]]** — A video-scale JEPA that scales I-JEPA to **1M+ hours** of video with a mask-denoising objective; **80%** pick-and-place from **62 hours** of unlabeled robot video proves the latent space captures action-relevant structure (object positions, orientations, dynamics) without ever reconstructing a pixel.
- **[[2602.10098|VLA-JEPA]]** (2026) — A full Vision-Language-Action stack pairing the JEPA principle with a ==flow-matching action head==; **97.2%** [[2306.03310|LIBERO]] in-distribution, **79.5%** [[2510.13626|LIBERO-Plus]] OOD, **65.2%** SimplerEnv real robot.
- **[[2601.14354|VJEPA-Probabilistic]]** — A probabilistic JEPA with explicit ==probabilistic semantics==: a ==variational objective== over future-latent distributions as a ==predictive information bottleneck==, plus a ==Bayesian Product-of-Experts== (BJEPA) for modular priors; holds signal **R²>0.84** under a noisy-TV distractor where VAE/pixel-AR collapse to ~**0.50**.
- **[[2211.10831|JEPA-Slow-Features]]** — An early empirical JEPA study (VICReg/SimCLR, LeCun co-authored, predates I-JEPA) probing latent prediction under visual distractors: JEPA filters ==changing== noise but collapses onto ==fixed slow-feature== backgrounds (RMSE near random baseline) where ==inverse dynamics modeling== stays robust; the first documented JEPA failure mode.

**Paradigm — Decision Matrix**

| Need | Paradigm | Exemplar |
|---|---|---|
| Visual fidelity / human-inspectable rollouts | Generative | [[2602.15922\|DreamZero]] (~150 ms/forward) |
| Frozen visual features for downstream stacks | Contrastive | [[2304.07193\|DINOv2]] |
| Forward dynamics without pixel cost | JEPA | [[2301.08243\|I-JEPA]] / [[2506.09985\|V-JEPA-2]] |
| Real-time robot control (MPC at 10–20 Hz) | JEPA | [[2602.10098\|VLA-JEPA]] (**~10 ms/step** vs **~150 ms** for pixel-space) |
| Cross-embodiment video priors | Generative | [[2602.15922\|DreamZero]] (**+42%** cross-embodiment, see [[06_WAM#2. VideoGen WAMs]]) |
| Compose with VLM for reasoning | JEPA (+VLM) | [[2603.22281\|ThinkJEPA]] (see §4) |
| Learn from limited robot data | JEPA | [[2506.09985\|V-JEPA-2]] (**62 hr** unlabeled → **80%** pick-and-place) |

^dm-1

> [!star] Key Papers
> - [[2301.08243|I-JEPA]] — Foundational masked-embedding-prediction architecture; the EMA target trick that blocks collapse without negative pairs and inspires every downstream JEPA variant
> - [[2506.09985|V-JEPA-2]] — Scales JEPA to **1M+ hours** video; **80%** pick-and-place with only **62 hours** of unlabeled robot data — proves latent prediction captures manipulation-relevant structure end-to-end
> - [[2602.10098|VLA-JEPA]] — Full VLA + JEPA stack: **97.2%** [[2306.03310|LIBERO]], **79.5%** [[2510.13626|LIBERO-Plus]] OOD, **65.2%** real robot — turns the JEPA principle into a deployable controller

^key-papers-1

> [!tip] Why JEPA Wins for Robots
> Generative world models ([[2602.15922|DreamZero]], Cosmos) produce inspectable video but spend ~150 ms/forward modeling textures and shadows that the policy never uses for action selection. JEPA's latent prediction filters those out at ~10 ms/step ([[2602.10098|VLA-JEPA]]) — fast enough for real-time MPC. The choice is between *interpretable but slow* (generative — see [[06_WAM#2. VideoGen WAMs]] for the VideoGen lineage and [[06_WAM#5. VLM-Integrated WAMs]] for VLM-integrated hybrids) and *opaque but fast* (JEPA — used as backbone for the WAM-augmented VLA stack in [[04_VLA#5. World-Model-Augmented VLAs]] and for reasoning insertion in [[05_VLA-Reasoning-and-CoT#3. Latent Reasoning — Token-Free CoT]]). For physics-aware deployment ([[08_Physics-Aware-Embodied-AI#5. Physics-Aware Reasoning]]), the latent opacity becomes a verification problem covered in §6. The navigation instantiation — latent rollouts inside the control loop — is [[12_Navigation-and-Mobile-Manipulation#4.1 World-Model-in-the-Loop Planning]].

^insight-1

---

### 2. JEPA Evolution: Visual-Only → Dense → Vision-Language → Vision-Language-Action

The JEPA lineage walks a four-step ladder: visual-only self-supervision → dense local features → vision-language alignment → full action conditioning. Each step adds one missing capability needed for robot control, and each step is a single architectural change to its predecessor — not a from-scratch redesign. This matters because it makes the ladder *composable*: you can pick the rung that matches your deployment constraint without inheriting irrelevant complexity from the higher rungs.

The progression is also a story of *what JEPA loses and re-acquires*: V-JEPA 2's global pooling sacrifices local detail (re-acquired by V-JEPA 2.1's dense loss); the vision-only objective sacrifices language grounding (re-acquired by VL-JEPA's InfoNCE); the action-free supervision sacrifices control signal (re-acquired by VLA-JEPA's flow-matching head).

#### 2.1 Visual-Only JEPA (Pretraining Substrate)

==Internet-scale video pretraining without robot data or language==. Establishes the "predict future embeddings from masked context" recipe and re-acquires local detail via dense supervision when downstream tasks need it. Both members keep encoder-only training; neither conditions on action.

- **[[2506.09985|V-JEPA-2]]** — The lineage's scale anchor that scales JEPA to video with a ==mask-denoising objective== on **1M+ hours** internet video, reaching **77.3%** SSv2 and **84.0%** PerceptionTest, while ==zero-shot MPC== achieves **80%** pick-and-place from only **62 hours** of unlabeled robot video; its one limit is ==global== pooling that fragments local structure, so dense tasks lag.
- **[[2603.14482|V-JEPA-2.1]]** — A dense-feature JEPA re-acquiring local detail via ==dense predictive loss== (masked + unmasked tokens), ==deep self-supervision== (objective at multiple intermediate layers), and ==modality-specific tokenizers== (2D/3D; **ViT-G**, VisionMix-163M); **RMSE 0.307** depth on NYUv2 (SOTA), **+20%** grasping over V-JEPA 2, **10× faster** navigation planning.

> [!success] V-JEPA's Latent-Prediction Advantage is Now Empirically Established
> [[2605.15618|V-JEPA-Robustness-Study]] runs a matched-capacity ViT-Large head-to-head — **V-JEPA 2.1 vs V-JEPA 2 vs VideoPrism vs VideoMAEv2** — across **5 robustness axes** (feature discriminability, corruption, fine-grained action discrimination, occlusion, temporal). Findings:
> - Latent-prediction JEPAs ==consistently dominate== pixel-reconstruction (VideoMAE) and contrastive (VideoPrism) under perturbation
> - V-JEPA models achieve a ==Directional Semantic Coherence Score several times higher== than the others under video reversal — a direct probe of internalized temporal causality
> - ==Frozen V-JEPA 2 backbones outperform task-adapted fine-tuned== VideoMAE / TimeSformer on corruption + occlusion robustness
> - But: high representational stability ≠ downstream utility — geometrically stable features are not automatically functionally useful
>
> This is the first independent, capacity-matched empirical validation of the rung-2.1 design choice. It says: *predicting in latent space isn't just faster — it builds qualitatively better world models.* It also bounds the claim: stability under corruption is a necessary but not sufficient condition for downstream task performance.

#### 2.2 Multi-Modal JEPA (Language and Action Conditioning)

==Add language alignment, then action conditioning, to the visual JEPA substrate==. Both members extend the prediction-not-generation bet across modalities: VL-JEPA via InfoNCE-aligned text embeddings, VLA-JEPA via a flow-matching action head on a VLM backbone. Together they close the loop from "JEPA understands video" to "JEPA controls robots".

- **[[2512.10942|VL-JEPA]]** — A vision-language JEPA that predicts ==abstract semantic embeddings== via ==InfoNCE loss==, with selective decoding cutting operations **~2.85×** for video streams; excels at discriminative tasks (classification, retrieval, real-time streaming) but **does not generate open-ended text** by design — the price of the prediction-not-generation bet.
- **[[2602.10098|VLA-JEPA]]** — A full VLA stack with a ==JEPA-style latent world model==, ==leakage-free state prediction== (future frames supervision-only), ==unified two-stage pretraining== (human + robot), and a ==flow-matching action head== on Qwen3-VL; **97.2%** [[2306.03310|LIBERO]] in-distribution, **79.5%** [[2510.13626|LIBERO-Plus]] OOD, **65.2%** SimplerEnv (SOTA).
- **[[2605.25313|UWM-JEPA]]** — A belief-augmented JEPA that adds an explicit ==belief== to the latent: a ==density-matrix== state evolved by a ==learned unitary predictor== preserving spectrum / purity / von-Neumann entropy during blind rollout (drift **<2.4e-7**), plus ==counterfactual targets== for action sensitivity; **0.770** hidden-velocity accuracy where matched LSTM-JEPA is at chance.
- **[[2605.20811|Demo-JEPA]]** — A *one-shot cross-embodiment* JEPA imitator: an action-conditioned ==world model== plus a ==Dreamer Predictor== translating a single source demonstration into target-compatible future latent goals; **0.36** sim / **0.25** real zero-shot SR (vs VPP **0.04/0.00**, XSkill **0.03/0.05**), approaching an oracle (**0.45** vs **0.55** sim).
- **[[2512.24497|JEPA-WM]]** — A ==component-wise empirical study== isolating ==Joint-Embedding Predictive World Model== design choices (encoder, rollout loss, planner); proprioception always helps, **2-step** rollout loss optimal in sim vs **6-step** for real DROID, and tuning-free Nevergrad matches CEM; beats DINO-WM and V-JEPA-2-AC.

**Evolution Step — Decision Matrix**

| Need | Rung | Rationale |
|---|---|---|
| Self-supervised video pretraining (no robots, no language) | [[2506.09985\|V-JEPA-2]] | Largest pretraining corpus (**1M+ hours**); cheapest entry to JEPA family |
| Dense per-token features for depth/segmentation | [[2603.14482\|V-JEPA-2.1]] | Dense predictive loss + deep self-supervision; SOTA **RMSE 0.307** NYUv2 |
| Real-time discriminative vision-language (retrieval, streaming) | [[2512.10942\|VL-JEPA]] | InfoNCE objective; **~2.85x** operation reduction vs autoregressive VLMs |
| Cannot give up open-ended text generation | Skip JEPA → use generative VLM | [[2512.10942\|VL-JEPA]] is discriminative-only by design |
| Full robot control with language conditioning | [[2602.10098\|VLA-JEPA]] | Adds flow-matching action head on Qwen3-VL; SOTA across [[2306.03310\|LIBERO]] + OOD + real robot |
| Few-step in-domain fine-tune from a strong starting point | [[2506.09985\|V-JEPA-2]] → action head | Skip rungs 2.2-2.4 if dense features and language are not needed |

^dm-2

> [!star] Key Papers
> - [[2506.09985|V-JEPA-2]] — **1M+ hours** video pretraining; **80%** pick-and-place with only **62 hours** unlabeled robot video — anchors the scale tier of the JEPA family
> - [[2603.14482|V-JEPA-2.1]] — Dense predictive loss + deep self-supervision; unlocks depth (**RMSE 0.307** NYUv2), grasping (**+20%**), navigation planning (**10x faster**)
> - [[2602.10098|VLA-JEPA]] — Full VLA + JEPA stack: **97.2%** [[2306.03310|LIBERO]], **79.5%** [[2510.13626|LIBERO-Plus]] OOD, **65.2%** SimplerEnv — closes the loop from understanding to control

^key-papers-2

> [!tip] Each Rung Pays For One Capability
> The ladder is composable: pick the lowest rung that meets your deployment constraint. [[2506.09985|V-JEPA-2]] alone is enough for zero-shot MPC ([[06_WAM#3.1 JEPA Family]]); [[2603.14482|V-JEPA-2.1]] is the right pick when you need dense features for depth/segmentation; [[2512.10942|VL-JEPA]] adds language only at the price of losing generation; [[2602.10098|VLA-JEPA]] is the full controller. The lineage also pairs naturally with the WAM-augmented VLA stack in [[04_VLA#5. World-Model-Augmented VLAs]] and with the latent reasoning insertion patterns in [[05_VLA-Reasoning-and-CoT#3. Latent Reasoning — Token-Free CoT]] — both use the JEPA encoder as the latent substrate. For the broader non-JEPA latent landscape (DINO-WM, UWM, Motus), see §3.

^insight-2

---

## Part B — Beyond JEPA

*The wider latent-prediction landscape (DINO-WM, UWM, Motus, …) and latent reasoning for embodied AI.*

### 3. Broader Latent Prediction Landscape

Beyond the JEPA lineage, other architectures also predict in latent space for embodied AI.

#### 3.1 JEPA for Embodied Control & Robotics

Papers that extend the JEPA framework toward acting agents: each adds one missing control axis (action conditioning, causal intervention, test-time adaptation, RL value learning, multi-camera driving).

- **[[2608.07409|Unified JEPA]]** — ==Unified prediction objective== casts photometric transforms and actions as one conditioning signal, one predictor, one latent space, with a ==Gaussian latent regularizer== + anti-collapse theorem; latent-MPC planning hits **75.8%** SR at **44x** speedup vs DINO-WM (**74.6%**, 12x) / LeWorldModel (**68.9%**, 48x), plus **74.9** ImageNet linear probe.
- **[[2607.06925|PrismWM]]** — A JEPA factoring state into global latent + ==sparse metric point anchors== + goal embedding, diagnosing ==instruction leakage== (predicted-anchor accuracy collapses **0.895→0.262** goal-withheld) and fixing it via a ==GoalFree== dynamics variant restoring **0.88** accuracy regardless of goal.
- **[[2607.04978|Qantara]]** — A **~21M**-param JEPA trained with joint ==bridge-flow matching== (Brownian-bridge latents + flow-matching actions) via ==edge-aligned (τ_a,τ_z) sampling==, serving planning/BC/video-inverse from **one checkpoint**; **93.7%** OGBench-Cube SOTA, goal-blind paths **15–65×** faster (17–24ms vs 0.4–1.2s).
- **[[2606.32026|AdaJEPA]]** — A LeCun-coauthored ==test-time adaptation== JEPA running a "plan-execute-adapt-replan" MPC loop that recalibrates encoder/predictor layers from an ==online buffer== of executed transitions; nearly doubles SR on unseen PushObj shapes at **0.01–0.03s** overhead/step.
- **[[2603.22281|ThinkJEPA]]** — A VLM-thinker + JEPA latent WM with ==dual-temporal perception== + ==hierarchical pyramid feature injection==; **ADE 0.061 / FDE 0.056** on EgoDex (beats six trajectory baselines), stable recursive rollouts at **H=32**.
- **[[2603.19312|LeWM]]** — A ==Two-term end-to-end JEPA== (==MSE prediction + Sketched-Isotropic-Gaussian Regularizer==) over a ViT-Tiny encoder with ==AdaLN Transformer predictor==, trained without stop-gradients or EMA; **+18%** Push-T over PLDM and **48×** faster MPC-CEM planning (<**1 s**/cycle) than foundation-model WMs, with provable anti-collapse guarantees from one tunable hyperparameter.
- **[[2603.15381|Autonomous-Learning-Framework]]** — A LeCun-Malik-Dupoux cognitive-science blueprint for self-improving AI: ==System A== (observation → JEPA-style world model) + ==System B== (action) + ==System M== (meta-control), bootstrapped by ==Evolutionary-Developmental bilevel optimization==; positions latent world models as the substrate action-learning consumes.
- **[[2602.11832|JEPA-VLA]]** — A fusion study demonstrating ==video predictive embedding is necessary== for VLA models, fusing ==V-JEPA 2== features via ==Early Fusion== or ==Gated Fusion== (cross-attention); **+7.4%** LIBERO / **+6.7%** LIBERO-plus / **+15.2%** LIBERO-Long over DINOv2/SigLIP, one-fifth of the data beating a full-data baseline (**100%** under layout/lighting shifts).
- **[[2602.11389|Causal-JEPA]]** — An ==Object-centric world model== with ==object-level latent interventions== for causal reasoning; **+20%** counterfactual VQA accuracy on CLEVRER, **8x faster** MPC planning on **1.02%** of the input features vs. patch-based world models.
- **[[2511.19221|Percept-WAM]]** — A ==Perception-enhanced world-awareness-action model== embedding explicit 2D (World-PV) + 3D (World-BEV) metric world states into one VLM backbone via ==grid-conditioned dense perception== + ==World-Action tokens==; **51.7 mAP** COCO 2D / **0.589 mAP** nuScenes BEV 3D, **0.36 m** L2 planning error / **90.2 PMDS** NAVSIM at a **40%** speedup.
- **[[2510.00739|TD-JEPA]]** — A JEPA adapted to a ==temporal-difference framework== for multi-step policy-conditioned latent dynamics with ==asymmetric state (ϕ) + task (ψ) encoders==, distilling ==zero-shot policies parameterized by task embeddings==; matches/beats SOTA across **65 tasks / 13 datasets** (ExoRL + OGBench), especially strong from ==pixel observations==.
- **[[2504.16591|JEPA-for-RL]]** — A JEPA adapted for image-based RL: ==separate context/target ViT encoders== combined with ==actor-critic gradient back-propagation through the encoder== plus regularization to prevent collapse, and ==learnable classification tokens== compressing to low-dim representations; demonstrates joint JEPA+RL beats either alone on Cart Pole from pixels.
- **[[2607.28443|CS-JEPA]]** (One Future, Every Robot) — A recurrent JEPA for decentralized multi-robot state prediction: each robot's ==GRU== processes local + neighbor messages, while a ==permutation-invariant tokenizer== compresses future robot embeddings into a fixed **17-token** target; self-supervised via stopped-gradient L2 + a training-only ==receiver-anchor== loss dropped at deployment.

#### 3.2 JEPA Theory, SSL Regularizers & LLM-Side Variants

Papers that treat JEPA itself as the object of study: identifiability and anti-collapse theory, regularizer design (isotropic-Gaussian, kernel, sparse-code, variational), and JEPA objectives ported into LLM and MLLM training.

- **[[2608.11174|VIScore]]** — Same-authors follow-up to [[2606.02572|VISReg]]: swaps ==SIGReg== for ==VISReg== inside LeWorldModel (VIS-WM), then proposes **VIScore** = ==veracity== x ==influence== (capped ==empowerment==) x ==sobriety==; **+0.91** pooled Spearman / **7.0** calibration error on held-out checkpoints vs empowerment's **+0.49** / **15.6**.
- **[[2606.02572|VISReg]]** — Decouples JEPA collapse-prevention into ==scale, shape, centering== objectives, replacing VICReg's covariance term with a ==Sliced Wasserstein Distance== to an isotropic Gaussian; fixes SIGReg's vanishing-gradient-at-collapse failure at **O(NDK)**, beating DINO/VICReg/SIGReg on **6** OOD datasets, matching DINOv2 accuracy from **10x less** data.
- **[[2605.26379|LeJEPA-World-Model]]** — A result proving *when* a JEPA is a world model: ==linear identifiability== of the true latents (up to orthogonal transform) ==iff== the latents are ==isotropic Gaussian== — the distribution its ==SIGReg== regularizer targets; **R²>0.999** recovery to 1024 dims (Lean-4-verified), the formal justification for [[2603.19312|LeWM]]'s regularizer.
- **[[2603.20111|Var-JEPA]]** — A ==variational reformulation== of JEPA re-deriving it as a coupled latent-variable generative model under a unified ==ELBO==, whose ==KL-divergence terms== intrinsically prevent representational collapse without EMA/SIGReg; Var-T-JEPA beats deterministic T-JEPA on tabular data and yields principled per-sample uncertainty for selective prediction.
- **[[2602.02381|AdaSSL]]** — Models the conditional uncertainty JEPA-style predictors discard via a latent variable ==r== (variational KL or L0-sparse), proving heteroscedasticity is unavoidable when mapping to a normalized embedding sphere; on stochastic Moving-MNIST world modeling it recovers both digit identity and velocity, sampling diverse futures where BYOL stays deterministic.
- **[[2602.01456|LpJEPA]]** — A JEPA regularizer inducing ==sparse, non-negative, maximum-entropy== latent codes via ==Rectified Distribution Matching Regularization== aligning `ReLU(z)` features to ==Rectified Generalized Gaussian== targets (sliced 2-Wasserstein), giving analytical control over the expected L0 norm; empirical L0 tracks theory at competitive ImageNet-100/1K linear-probe accuracy.
- **[[2512.15885|JARVIS]]** — First integration of an ==I-JEPA masked-prediction objective== directly into LLaVA-style MLLM alignment, using early LLM layers as the ==predictor== against a frozen DINOv2 target; **+0.7–1.6** average points on vision-centric benchmarks across five LLM backbones with no general-task trade-off.
- **[[2511.08544|LeJEPA]]** — A ==Provable and scalable SSL== framework based on ==Euclidean latent geometry== and ==SIGReg==; stable across **50+** architectures up to **1.8B** params, hitting **78.5%** ImageNet-1K linear probe (ConvNeXtV2-Huge) while beating larger DINOv2/v3 in-domain — gives JEPA a theoretical convergence story.
- **[[2509.14252|LLM-JEPA]]** — An LLM JEPA adding a ==JEPA loss on multi-view text-code pairs== alongside autoregressive LM loss, with a ==`[PRED]` token + custom attention mask== reusing the LLM's transformer layers as encoder/predictor; ==loss dropout== cuts compute up to **50%**, with consistent gains across Llama-3.2/Gemma-2/OpenELM on NL-RX-SYNTH, GSM8K, Spider and reduced overfitting.
- **[[2509.12249|P-JEPA]]** — Proves a ==No Unhealthy Representation Collapse== theorem: a JEPA trained with ==latent-dynamics + auxiliary regression loss== cannot collapse observations that are non-bisimilar under the auxiliary function; a counting-environment probe confirms **9** distinct latent clusters matching object count, formalizing why MBRL JEPAs (TD-MPC2, PLDM) need auxiliary heads.
- **[[2505.05626|PERCEPTLLM]]** — Injects an I-JEPA/AIM-v2 ==VISUALLOSS== auxiliary target plus ==BLANKTOKENS== masking and a ==disentangled vision/text pathway== into an LLaVA-style MLLM; **+1.52** normalized accuracy on SpatialEval, beating Llama-3.2-11B from an **8B** model at lower input resolution.
- **[[2505.03176|seq-JEPA]]** — An ==Action-conditioned sequence JEPA== with a ==transformer sequence aggregator== whose aggregate output is invariant, encoder equivariant; resolves the invariance-equivariance trade-off without dual losses, reaching **R² 0.71** on 3DIEBench rotation and **86.14%** classification (vs. **80.40%** equivariant baseline) plus **83.44%** STL-10 saccade-prediction.
- **[[2512.19605|KerJEPA]]** — A kernel-discrepancy JEPA generalizing [[2511.08544|LeJEPA]]'s regularization to ==kernel discrepancies== (MMD + ==Kernel Stein Discrepancy==) with ==closed-form analytical slicing== eliminating ==Monte Carlo variance==; an ==IMQ== kernel reaches **91.90%** ImageNette (vs LeJEPA's **91.13%**) with better stability, faster convergence, non-Gaussian (Laplace) priors.
- **[[2403.00504|IWM]]** — A LeCun-coauthored JEPA extension predicting ==photometric transformations== in latent space via an encoder + EMA target + reusable ==world-model predictor==, tuning representations along an ==equivariant-to-invariant== spectrum; fine-tuning only the predictor matches full-encoder tuning on ImageNet/ADE20k at a fraction of the parameters.

#### 3.3 Non-JEPA Latent Models

Alternative architectures achieving latent prediction without the JEPA framework — divided across algebraic-structured LAMs, dual-branch training, frozen-feature dynamics, and unified diffusion.

- **[[2608.13556|V-RAE]]** — Frozen ==DINOv3/SigLIP2/V-JEPA-2.1== VFM features (not a learned VAE) form the generative latent, compressed **4x** via 3M-param ==Temporal Attention Pooling== + spatiotemporal ViT decoder; **2.13** rFVD K600 (**40.5%** better than best VAE), **5-6x** faster DiT convergence, Cityscapes forecasting gFVD **144.47→111.36** over Wan2.2 VAE.
- **[[2608.10744|Latent-to-4D]]** — Treats a video diffusion model's final denoised ==VAE latent== as a shared cross-generator interface via the ==L4AR== module (trilinear resample + 3D conv + frame/global attention) feeding a frozen 4D reconstructor; **+5.81** DINO-F1 over matched Wan2.2+4RC, drift **0.0053** vs **0.3827** for RGB-decode — one checkpoint serves three generators.
- **[[2607.21576|SDM]]** — A ==Structured Dynamics Model== predicting future frozen ==[[2304.07193|DINOv2]] features== via ==two-stage compensation==, disentangling ==primary (camera)== from ==residual (object-centric)== motion; beats [[2604.04913|DeltaWorld]]'s DeltaTok on **5/7** ProbeMotion tasks (**+9.6 pp** SSv2-110k), rivaling supervised VGGT-1B/Pi3X at **215M** params.
- **[[2607.11427|EDAR]]** — Learns ==environment-dependent latent action tokens== via a Transformer encoding action chunks, visual context, and register tokens, with a ==dual-target decoder== (reconstruction + future-visual-consequence prediction); **+4.5 pp** LIBERO (91.8%), CALVIN length 3.34→3.80 — frozen DINOv3 targets beat JEPA-based ones (I-JEPA/V-JEPA-2.1) for shaping the action latent.
- **[[2607.01166|Structured 4D Latent]]** — A ==sparse 3D voxel latent== (decodable to 3D Gaussians) predicted via two-step ==conditional flow-matching== (coarse geometry + detail features), paired with a ==goal-conditioned inverse-dynamics== planner; **61.3%** ManiSkill3 SR (vs UniPi **29.3%**), **78–85%** zero-shot visual-shift SR, **80%** real block-in-basket.
- **[[2606.18208|LoopWM]]** — First ==looped-transformer== world model: a ==parameter-shared recurrent block== + ==spectrally-constrained residual dynamics== (contractive state matrix) with ==adaptive early exit== + ==deferred decoding==; **1B**-param model beats **100×**-larger Claude-Opus-4-6-Max (**68.4%** vs **47.2%** EM) on ScienceWorld.
- **[[2607.04714|GeoMoLa]]** — Learns discrete ==VQ-VAE motion latents== via self-supervised ==future 3D pointmap prediction== (RGB-D diffusion) rather than 2D-appearance prediction, then conditions a ==diffusion action transformer== on them; **84.7%** RLBench (1st on 8/10 tasks), **3.60** avg CALVIN sequence length, **+13.3pp** real-world over 3D Diffuser Actor.
- **[[2606.05555|MR.Q]]** — A model-free ==TD3== actor-critic shaped by ==auxiliary predictive latent objectives== (forecast future latent/reward/termination, no planning) on a frozen ==DINOv2== encoder; matches/beats world-model+MPC ==Newt== across **200**-task MTRL (**+37%** at 2M steps), **50%** stronger zero-shot transfer — representation learning, not planning, drives scalability.
- **[[2606.04130|CLAW-Latent-Action-WM]]** — An end-to-end ==self-supervised== framework that jointly trains a ==Latent Action Model== and a ==diffusion world model== from action-free video, with ==adversarial latent regularization== preventing the LAM from leaking future visual information into latent actions; wins **7/10** visual-planning tasks across VP2/Crafter/Procgen.
- **[[2606.02486|AHEAD]]** — A lightweight (**4.9M**-param) ==latent-space world model== that wraps a frozen VLA via ==language-and-motion saliency masking== + conditional ==flow matching== at **158 ms/step**; **87–93.7%** SR in high-acceleration regimes (vs **30.7–48%**), **>95%** on fast conveyor tasks, and 19/30 on projectile-catching where all baselines score **0/30**.
- **[[2606.02280|LDG]]** — An ==outcome-centric framework== that discovers ==latent dynamics geometries== from interaction histories (no physical-parameter supervision) via ==multi-positive contrastive learning==; highest mean reward on Hopper (**3239.2**) / Walker2d (**4883.7**), and uniquely survives structural-failure (disabled actuator) where parameter-centric methods fail.
- **[[2605.10819|ALAM]]** — An algebraic latent-action model imposing ==algebraic structure on latent actions== via ==composition== + ==reversal== constraints, with latent transitions as auxiliary targets in a ==flow-matching policy==; additivity/reversibility errors **25–85×** smaller, MetaWorld MT50 **47.9% → 85.0%** (**+37.1 pp**), [[2306.03310|LIBERO]] **94.1% → 98.1%**, real-world **+45 pp**.
- **[[2605.03413|NEO-Theorizer]]** — A program-learning world model recovering ==executable compositional programs== ("theories") from observation pairs via a ==Neural Theorizer== with a ==VQ-VAE Language of Thought== + ==Minimum Description Length== prior; **0.933** compositional / **0.845** length OOD on GridWorld, recovering ground-truth primitives — modeling as explanation, not reconstruction.
- **[[2605.01694|Latent-State-Design-WM]]** — A framework reframing world modeling as ==latent-state design under sufficiency constraints==, giving a ==functional taxonomy== of six latent-state roles + seven-axis evaluation and Preserve/Discard/Enable matrix; proves ==predictive sufficiency ≠ control sufficiency== — strategic compression, not maximal preservation, makes a state usable.
- **[[2605.00078|Being-H0.7]]** — A ==Dual-branch latent world-action model== with ==Mixture-of-Transformers==: a deployable "prior" branch whose hidden states are aligned at training to a "posterior" branch receiving privileged future embeddings; **99.2%** [[2306.03310|LIBERO]], **62.1%** [[2406.02523|RoboCasa]], **67.5%** real-world Dynamic Scene, **3–4 ms/step**.
- **[[2604.10333|ZWM]]** — A ==Sparse Temporally-Factored Prediction== ViT trained on **868 hours** of uncurated egocentric child video (BabyZWM) that disentangles appearance from motion; ==Approximate Causal Inference + Compositional Prompting== extract zero-shot optical flow (rivals supervised TAP-Vid-DAVIS), **>90%** relative depth, object discovery matching Mask2Former; aligns with human fMRI.
- **[[2604.04913|DeltaWorld]]** — Extends the [[2507.19468|DINO-world]] recipe to diverse generative forecasting via ==DeltaTok== (compresses consecutive VFM-feature differences into one token) + a ==Best-of-Many== training objective; **35×** fewer params / **2,000×** fewer FLOPs than Cosmos-4B/12B for 20 samples, **+5.6 mIoU** Cityscapes over DINO-world's single deterministic prediction.
- **[[2603.29090|HCLSM]]** — A ==Hierarchical causal latent state machine== unifying object-centric ==dynamic Slot Attention== + multi-timescale dynamics (==selective SSMs==, ==Event Transformer==, ==Goal Compression==) + a GNN-learned ==causal adjacency matrix==, trained two-stage (SBD reconstruction → ==JEPA loss==); **0.008** next-state MSE on PushT, **38×** Triton-kernel speedup.
- **[[2602.06130|SWIRL]]** — A reciprocal-RL framework co-training a ==Forward World Model== + ==Inverse Dynamics Model== from state-only video/text via ==GRPO==, treating actions as latent variables optimized by Conditional-Mutual-Information (FWM) and ELBO (IDM) objectives; **+16%** AURORA-BENCH, **+26.4%** BYTEMORPH, **+4.03** BLEU STABLETOOLBENCH — no action labels needed.
- **[[2512.08411|PRISM-WM]]** — A ==context-aware Mixture-of-Experts== latent world model factorizing hybrid dynamics (continuous motion + discrete contacts) into composable primitives, with a ==gating mechanism== identifying the physical mode and ==latent orthogonalization== preventing expert ==mode collapse==; a higher-fidelity ==TD-MPC== substrate cutting rollout drift on Humanoid-Bench.
- **[[2512.13030|Motus]]** — A ==Mixture-of-Transformer== unifying VLM understanding + ==video generation== + an ==Action Expert== via ==Tri-model Joint Attention==, with ==optical-flow latent actions==; **88.66%** clean / **87.02%** randomized RoboTwin-2.0 SR (>**45%** over π0.5, >**15%** over X-VLA), **63.22%** / **59.30%** real dual-arm partial SR (**+48.43%** / **+10.7%** over π0.5).
- **[[2511.05963|NextLat]]** — A lightweight ==latent-dynamics MLP== shaping transformer hidden states into ==belief states== via multi-step Smooth-L1 + KL losses (no EMA/masking); **3×** more compact latent (rank **52.7**), **58.7%** Countdown reasoning (beats MTP/JTP/BST/GPT), **3.3×** inference speedup via self-speculative decoding.
- **[[2507.19468|DINO-world]]** — A two-stage video WM on frozen ==[[2304.07193|DINOv2]] ViT-B/14== features with a ==lightweight cross-attention predictor + RoPE==; **47.0%** mIoU on VSPW dense forecasting (vs. **40.7%** for COSMOS), **91.3%** IntPhys intuitive physics, and action-conditioned planning lifts Wall environment from **87.1%** (scratch) to **93.8%** (pretrained).
- **[[2505.15659|FLARE]]** — A ==Future Latent Representation Alignment== policy predicting compact future-state embeddings rather than full frames via an ==action-aware observation embedding + diffusion transformer policy==, with ==co-training== ingesting action-free human video; **+26%** over baselines on multitask IL and **95%** real-world SR with only **100** trajectories/task.
- **[[2505.13696|ESWM]]** — An ==Episodic Spatial World Model== meta-trained to infer missing components of sparse one-step (state, action, end-state) tuples from an ==external editable memory bank==; ESWM-T explores **+16.8%** more unique states than EPN, navigates at **96.8%** SR (**+18%** vs EPN) with **99.2%** path optimality, adapts to new obstacles (**93%** vs **72%** EPN, **56%** RL).
- **[[2505.11528|LaDi-WM]]** — A latent WM combining [[2304.07193|DINOv2]]+SigLIP features with ==imagination-guided iterative action refinement==; **68.7%** on LIBERO-LONG with only **10 demos**.
- **[[2505.05512|RoboOccWorld]]** — A two-stage indoor ==occupancy world model== whose ==VQ-VAE== Occupancy Scene Tokenizer compresses 3D occupancy into a discrete latent space, then an ==autoregressive transformer== predicts future occupancy tokens from history + next camera pose (==HSTA== + ==CCSA==); **+22.34 IoU** next-state and **+19.48 IoU** autoregressive over prior methods.
- **[[2504.02792|UWM]]** — A ==Unified World Models== ==diffusion transformer== with ==independent action / observation diffusion timesteps== that toggle policy / forward-dynamics / inverse-dynamics / video-prediction modes at inference; up to **+20%** real DROID SR, with action-free co-training lifting Stack-Bowls **0.86 → 0.92** ID and **0.76 → 0.84** OOD.
- **[[2503.18938|AdaWorld]]** — A ==Latent Action Autoencoder== that extracts context-invariant latent actions from action-free videos via ==beta-VAE information bottleneck==, then pretrains an autoregressive WM (from ==Stable Video Diffusion==) on them; **FVD 767.0** vs **1545.2** baseline, **70.5%** vs **20%** human SR on LIBERO; transfers to Habitat / Minecraft / DMLab / nuScenes / VP2.
- **[[2411.04983|DINO-WM]]** — A task-agnostic world model on ==frozen [[2304.07193|DINOv2]] features== whose lightweight dynamics module learns how frozen features change given an action, enabling ==zero-shot planning== via goal-feature search without per-environment retraining; **+45%** avg planning over IRIS (**0.90** PushT SR vs **0.32**), **0.82** WallRandom SR.
- **[[2311.16038|OccWorld]]** — The autonomous-driving ==3D occupancy world model== origin of the recipe [[2505.05512|RoboOccWorld]] adapts indoors: a self-supervised ==VQ-VAE Scene Tokenizer== + ==GPT-like spatial-temporal transformer== jointly forecasting 4D occupancy + ego trajectory; **17.14%** mIoU / **26.63%** IoU (3s), **1.17m** planning L2 without HD-map/box supervision.
- **[[2407.21126|LOPR]]** — Learns a low-dimensional latent space for LiDAR occupancy-grid maps via a combined ==β-VAE + GAN==, then a ==transformer== does stochastic multi-future prediction in that space, with a fast single-step decoder plus an optional ==diffusion-based batch decoder==— same recipe as [[2311.16038|OccWorld]]/[[2505.05512|RoboOccWorld]] for real-time futures.
- **[[2307.00972|MoVie]]** — Test-time-only view adaptation: fine-tunes a ==Spatial Adaptive Encoder== (Spatial Transformer Networks in shallow layers) online at deployment, using the base RL agent's frozen pretrained latent dynamics model as the self-supervisory signal to keep latent representations consistent under novel camera views — no reward, no policy retraining, just a small replay buffer.

#### 3.4 Latent-WM Surveys

Field-defining surveys that taxonomize the latent-prediction landscape — one architectural (decoupled vs unified), one cognitive (perception vs meta-cognition) — plus the training-data resource that operationalizes what "interactive world modeling" requires.

- **[[2608.09449|Sekai2]]** — A real-world ==interactive-world-modeling== video corpus pairing every clip with ==ViPE-estimated camera trajectories== + ==hierarchical Kimi-K2.6 captions==; **128,892** clips (**2,826** hours, 113 countries) plus 982 loop-rich panoramic sequences for revisit-consistency supervision.
- **[[2605.00080|WM-Robot-Learning-Survey]]** — A ==Multi-dimensional taxonomy== of world models for robot learning that documents the architectural evolution from decoupled "predict-then-act" to ==unified VLA/MoE/MoT backbones==, with **latent-space world modeling** as the dominant integration pattern.
- **[[2604.16592|Cognition-WM-Survey]]** — A ==Cognitive-Architecture-Theory taxonomy== spanning Video, Embodied, and Epistemic WMs that identifies ==motivation== and ==meta-cognition== as the most under-developed cognitive functions in current latent WMs.
- **[[2601.15533|Actionable-Simulators]]** — A position paper arguing generative WMs suffer ==dynamical hallucinations== and should be reframed as ==actionable simulators== built on four imperatives — ==structured 4D interfaces==, ==self-evolution==, ==physical anchoring==, ==structured imagination== — evaluated by ==closed-loop decision metrics==, not pixel fidelity; a physical-grounding mandate.

#### 3.5 Alternative-Latent-Models Thread

Beyond the JEPA lineage, a parallel thread builds latent world models on different SSL substrates. The threads converge on the same insight (predict in latent space) via different routes.

```text
╔═════════════════════════════╗    ╔═════════════════╗    ┌────────────┐    ╔═══════════════╗    ╔═════════════════╗
║ DINOv2 (Frozen visual SSL)  ║───►║ DINO-WM (2024)  ║───►│ UWM (2025) │───►║ Motus (2025)  ║───►║ LaDi-WM (2025)  ║
╚═════════════════════════════╝    ╚═════════════════╝    └────────────┘    ╚═══════════════╝    ╚═════════════════╝
                                            ▲                    ▲
                                            │                    │
                                  ┌───────────────────┐  ┌─────────────────┐
                                  │ DINO-world (2025) │  │ AdaWorld (2025) │
                                  └───────────────────┘  └─────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

The thread walks four convergent steps — each substituting a different missing capability into the same latent-prediction skeleton.

- **[[2411.04983|DINO-WM]]** — A frozen-feature world model establishing that ==frozen== [[2304.07193|DINOv2]] features are rich enough for world modeling; its dynamics module operates entirely in feature space, enabling ==zero-shot planning== via goal-feature search without per-environment retraining — **+45%** avg planning over IRIS (**0.90** PushT SR vs **0.32**), **0.82** WallRandom SR.
- **[[2504.02792|UWM]]** — A single ==diffusion transformer== unifying three tasks (action-conditioned, action-free, video prediction) via ==independent action/observation diffusion timesteps==; up to **+20%** real DROID SR, with action-free co-training adding **+0.06–0.08** SR in/out of distribution — richer dynamics than any single-task model.
- **[[2512.13030|Motus]]** — A ==unified latent diffusion== MoT pushing further with ==optical-flow latent actions== in a ==Tri-model Joint Attention== backbone; **88.66%** RoboTwin-2.0 SR (>**45%** over π0.5) — latent action modeling from action-free video at scale.
- **[[2505.11528|LaDi-WM]]** — A latent WM combining [[2304.07193|DINOv2]]+SigLIP features with ==imagination-guided iterative action refinement==; **68.7%** on LIBERO-LONG with only **10 demos**.
- **[[2602.10102|VideoWorld-2]]** — A ==dynamics-enhanced Latent Dynamics Model (dLDM)== ==decoupling action dynamics from visual appearance==: a pretrained ==Video Diffusion Model== handles appearance while compact latent codes carry task-relevant dynamics, planned by an ==autoregressive transformer==; **72.3%** step-7 paper-folding (~**70%** gain), **2.88** CALVIN cross-domain length.

#### 3.6 Historical Precursors to Latent Prediction

Before JEPA formalized "predict embeddings, not pixels" as a named architecture, several independent lines of work arrived at the same core idea — latent-space forward prediction, prediction-error-driven exploration, and unsupervised discrete action discovery — using autoencoders, RNNs, and clustering rather than the EMA-target/context-encoder machinery of modern JEPA.

- **[[2101.12195|CADDY]]** — An unsupervised ==Clustering for Action Decomposition and DiscoverY== framework learning ==discrete latent actions== via Gumbel-Softmax + mutual-information loss and a ConvLSTM dynamics model from unlabeled video; **0.469** Fleiss' kappa vs **≤0.072** baselines on Tennis — a direct precursor to modern Latent Action Models (cf. [[2606.04130|CLAW-Latent-Action-WM]]).
- **[[1809.01999|World Models]]** — The seminal ==VAE + MDN-RNN== latent world model: VAE encodes pixels, MDN-RNN predicts the next latent state, and a linear Controller trained via ==CMA-ES== acts entirely inside the dreamed rollout; **906±21** CarRacing-v0 SOTA, policy trained in DoomRNN transfers to real VizDoom (**1092±556**) — ancestor of Dreamer-style and JEPA-style latent rollouts.
- **[[1507.00814|Predictive Exploration Bonus]]** — An early latent dynamics model: an ==autoencoder== compresses pixels, a ==dynamics network== predicts the next encoded state, and prediction error becomes an intrinsic exploration bonus; beats epsilon-greedy/Boltzmann/Thompson-sampling on **7/14** Atari games — anticipates latent-prediction error as a training signal, not just a controller input.
- **[[1504.08023|Visual Representation Anticipation]]** — The historical root of "predict representations, not pixels": a ==deep regression network== anticipates future ==fc7 (AlexNet) features== from unlabeled video via a multi-modal EM-style objective; **+19%** action-forecasting, **+30%** object-anticipation mAP over static baselines — the direct conceptual precursor to §1's JEPA principle.

JEPA-family models trade off three axes: encoder freezing, modality count, and action conditioning. Choose by deployment constraints.

**Latent Landscape — Decision Matrix**

| Variant | Encoder | Modalities | Action-Conditioned | Best For |
|---------|---------|-----------|-------------------|----------|
| [[2301.08243\|I-JEPA]] | Trainable | Image | No | Image SSL pretraining |
| [[2506.09985\|V-JEPA-2]] | Trainable | Video | No | Video SSL + zero-shot MPC |
| [[2603.14482\|V-JEPA-2.1]] | Trainable | Video (dense) | No | Depth, navigation, dense tasks |
| [[2512.10942\|VL-JEPA]] | Trainable | Vision + Lang | No | Discriminative VL retrieval |
| [[2602.10098\|VLA-JEPA]] | Trainable | Vision + Lang + Action | Yes | Full robot control via latent prediction |
| [[2602.11832\|JEPA-VLA]] | Trainable | Vision + Action | Yes | Action-conditioned video embedding |
| [[2510.00739\|TD-JEPA]] | Trainable | Vision + Reward | Yes (zero-shot RL) | Value learning in latent space |
| [[2511.19221\|Percept-WAM]] | Trainable | Vision (multi-cam) + Action | Yes | End-to-end autonomous driving |
| [[2411.04983\|DINO-WM]] | Frozen ([[2304.07193\|DINOv2]]) | Vision + Action | Yes | Zero-shot planning, transfer |
| [[2602.11389\|Causal-JEPA]] | Trainable | Object-centric | Yes | Counterfactual reasoning |

^dm-3

> [!star] Key Papers
> - [[2602.11832|JEPA-VLA]] — Closes the JEPA → VLA loop; demonstrates action-conditioned video predictive embedding is *necessary* for VLA models
> - [[2411.04983|DINO-WM]] — The frozen-[[2304.07193|DINOv2]] baseline; proves a lightweight dynamics module on frozen features enables zero-shot planning without retraining
> - [[2605.00078|Being-H0.7]] — Dual-branch latent world-action model; deployable prior aligned to a future-informed posterior; **99.2%** [[2306.03310|LIBERO]] at 3–4 ms/step
> - [[2504.02792|UWM]] — Unified diffusion transformer spanning action-conditioned / action-free / video prediction in one backbone
> - [[2605.00080|WM-Robot-Learning-Survey]] — The field map: documents the shift from decoupled "predict-then-act" to unified latent-space backbones

^key-papers-3

> [!tip] Frozen Features Are Powerful — and the Variant Choice Follows Your Constraint
> [[2411.04983|DINO-WM]] showed you don't even need to train a new encoder — frozen [[2304.07193|DINOv2]] features are rich enough for world modeling, with the dynamics model operating entirely in frozen feature space for zero-shot planning. From there the variant choice is constraint-driven: need **action conditioning** → [[2602.10098|VLA-JEPA]] / [[2602.11832|JEPA-VLA]] / [[2411.04983|DINO-WM]]; need **zero-shot transfer** → freeze the encoder ([[2411.04983|DINO-WM]]); need **dense local features** → [[2603.14482|V-JEPA-2.1]]; need **multi-camera driving** → [[2511.19221|Percept-WAM]]; need **value learning** → [[2510.00739|TD-JEPA]]. The non-JEPA thread ([[2504.02792|UWM]] → [[2512.13030|Motus]] → [[2505.11528|LaDi-WM]]) reaches the same latent-prediction insight by a different route. This same frozen-vs-trainable-encoder choice reappears on the WAM deployment side in [[06_WAM#3.1 JEPA Family]], which catalogues the same JEPA variants as backbone options for world-action models. The tactile counterpart, where the frozen encoder is pretrained on touch streams rather than pixels, is [[10_Contact-Rich-and-Tactile-Control#2.2 Touch Foundation Models — SSL Representations on Tactile Streams]].

^insight-3

---

### 4. Latent Reasoning for Embodied AI

The frontier: combining latent world models with *reasoning in representation space* — enabling robots to plan, reason about spatial relationships, and "think ahead" without generating explicit text or video. This is where latent prediction meets the broader "continuous thought" paradigm ([[2412.06769|Coconut]], [[2502.05171|Huginn]]), applied specifically to physical agents.

The space splits along *where the reasoning happens*: in the planning loop (substitute amortized inverse dynamics for online search), in the spatial representation (reason on metric cognitive maps rather than raw embeddings), or in the autoregressive token stream itself (continuous visual / abstract tokens replacing discrete text). Each axis trades expressiveness for latency, and each maps to a different bottleneck in the VLA stack.

#### 4.1 Latent Planning

==Plan trajectories in embedding space rather than generating video or running iterative search==. Orders of magnitude faster than pixel-space MPC ([[2602.15922|DreamZero]]: ~150 ms/forward; [[2602.10098|VLA-JEPA]]: ~10 ms/step), enabling real-time control at 10–20 Hz.

- **[[2605.08732|GC-IDM]]** — An amortized goal-conditioned inverse-dynamics model: a **1.5M-parameter 3-layer MLP** mapping (current latent, goal latent, remaining horizon) directly to next action, replacing iterative CEM/MPPI search via ==multi-step horizon supervision==; **100–130× faster** than CEM at matched/superior SR in 7/8 settings, action jerk **15–36× lower**.
- **[[2605.00078|Being-H0.7]]** — A ==dual-branch latent world-action model==: a deployable "prior" branch aligned at training to a "posterior" branch receiving privileged future embeddings (Mixture-of-Transformers), with the posterior dropped at deploy; **99.2%** [[2306.03310|LIBERO]], **62.1%** [[2406.02523|RoboCasa]], **67.5%** real-world Dynamic Scene at **3–4 ms/step**.
- **[[2603.22281|ThinkJEPA]]** — A VLM-thinker + JEPA latent WM with ==dual-temporal perception== (dense for JEPA, sparse for VLM) + ==hierarchical pyramid feature injection== via FiLM; **ADE 0.061 / FDE 0.056** on EgoDex (vs **6** trajectory baselines), maintaining best performance at recursive rollout horizons up to **H=32** — VLM semantic conditioning stabilizes long-horizon latent rollouts.
- **[[2601.21598|ATP-Latent]]** — A two-stage latent planner: a VAE produces smooth probabilistic latent tokens + stop head, then ==GRPO== with ==unsupervised coherence reward== plans in that space; **47.7%** avg / **8.4 tokens** across four math benchmarks (**+4.1%** SR / **−3.3%** tokens vs SIM-CoT) — RL beats imitation in latent space when the space is well-conditioned.
- **[[2604.03208|HWM]]** — A planner doing ==Top-down hierarchical planning in shared latent space==: ==latent macro-actions== set subgoals while primitives run under ==receding-horizon MPC==; **70%** real pick-and-place (vs **0%** single-level VJEPA2-AC), **61%** Push-T at d=75 (vs **17%** flat DINO-WM, **~3×** less compute), **83%** hard maze (vs **44%** flat PLDM, **4×** less compute).
- **[[2411.04983|DINO-WM]]** — A task-agnostic dynamics model on ==frozen [[2304.07193|DINOv2]] features== with a ==ViT transition model trained via latent consistency loss==, where ==MPC + CEM== searches actions whose feature trajectory ends at goal features; **+56%** LPIPS over SOTA (**0.007** PushT), **+45%** avg planning over IRIS (**0.90** PushT SR vs **0.32**), **0.82** WallRandom SR.

#### 4.2 Spatial Latent Reasoning

==Reason about 3D space and physical relationships in latent representations== rather than running explicit geometric computation. Bridges perception and action through a spatial substrate the policy can directly consume.

- **[[2604.02097|LatentUM]]** — A ==Mixture-of-Modal-Experts== unified model reasoning over ==semantic-token visual features== (no pixel-decoding mediation) via ==Model-Behavior-Aligned Quantization==; **0.99** avg Visual-Spatial-Planning accuracy (beats ThinkMorph's **0.76**), **1.34** ATE / **0.34** RPE action-conditioned world modeling.
- **[[2601.11442|Map2Thought]]** — A ==Metric Cognitive Map== representation unifying ==discrete symbolic grids== with ==continuous metric-scale data==, where ==Cognitive Chain-of-Thought== runs deterministic geometric computations on the map for verifiable inference traces; **61.0%** average on VSI-Bench (top open-source VLM, beats proprietary), **59.9%** at half the training data.
- **[[2510.00855|DyVA]]** — A dynamics-injection method feeding ==dynamics-aware latents== from a frozen ==Stable Video Diffusion== "Generative Encoder" (a single Euler step, no full video) alongside SigLIP static features into a frozen LLM; trained only on single images it shows ==emergent zero-shot multi-frame reasoning==, **+28.3%** on MindCube subtasks over GPT-4o.

#### 4.3 Continuous Thought for Embodied Agents

==Reason by iterating on continuous embeddings== rather than generating discrete text tokens. Extends the [[2412.06769|Coconut]] / [[2502.05171|Huginn]] "thinking in latent space" paradigm to physical agents. For the full reasoning-insertion taxonomy see [[05_VLA-Reasoning-and-CoT#3. Latent Reasoning — Token-Free CoT]].

- **[[2604.22709|Abstract-CoT]]** — A latent-CoT method where discrete ==abstract tokens== from a reserved vocabulary replace verbalized rationales, via two-stage post-training (==policy iteration warm-up== + ==warm-started GRPO==) with an attention-mask bottleneck; **Up to 12x fewer reasoning tokens** vs verbalized CoT at comparable / superior MATH / AlpacaEval / HotpotQA, across Qwen3 / Granite.
- **[[2509.25681|dVLA]]** — A unified discrete ==diffusion== VLA over vision + language + action tokens with ==multimodal CoT== (visual subgoals + textual reasoning + action interleaved); **96.4%** [[2306.03310|LIBERO]] avg, **65%** real-world, CoT adds **+6.6 pp** sim / **+12.5 pp** real, **~2×** speedup via prefix attention mask + dLLM-Cache.
- **[[2511.19418|COVT]]** — A continuous-visual-token method distilling ==continuous visual tokens== from vision experts (SAM, DepthAnything v2, PIDINet, [[2304.07193|DINOv2]]) into the VLM's autoregressive stream via a four-stage pipeline; **+5.5%** CV-Bench / **+14.0%** Depth sub-task with Qwen2.5-VL-7B, **+26.6%** BLINK count on LLaVA-v1.5-13B — beats text-only CoT on vision-centric tasks.
- **[[2601.05877|iReasoner]]** — A ==trajectory-aware intrinsic reasoning supervision== method where cross-rollout step agreement, quantified via embedding-space cosine similarity to dynamic prototypes, acts as a self-supervised step-level reward; **+1.32** general visual / **+1.64** visual math across 8 benchmarks (beats outcome-only EvoLMM).
- **[[2503.15558|Cosmos-Reason1]]** — A multimodal LLM family (**7B + 56B** with hybrid Mamba-MLP-Transformer for 56B), SFT + ==RL with rule-based verifiable rewards== over ~**4M** annotations; 56B hits **60.2%** physical commonsense / **63.7%** embodied reasoning, 7B reaches **74.5%** intuitive physics after SFT (**+32.4%** over backbone) → **81.5%** post-RL — physics-aware reasoning at scale.

**Latent Reasoning — Decision Matrix**

| Need | Mechanism | Exemplar |
|---|---|---|
| Eliminate planning-loop search (real-time MPC) | Amortized inverse dynamics | [[2605.08732\|GC-IDM]] (**100–130×** vs CEM) |
| Long-horizon latent rollout stability | VLM-guided JEPA prediction | [[2603.22281\|ThinkJEPA]] (**H=32** stable) |
| Future-informed training, fast deployment | Dual-branch privileged-future | [[2605.00078\|Being-H0.7]] (**3–4 ms/step**) |
| RL beyond imitation in latent space | VAE + GRPO + coherence reward | [[2601.21598\|ATP-Latent]] (**+4.1%** SR, **−3.3%** tokens) |
| 3D spatial reasoning with verifiable traces | Metric cognitive map + Cog-CoT | [[2601.11442\|Map2Thought]] (**61.0%** VSI-Bench) |
| Replace verbal CoT with compact tokens | Discrete abstract tokens | [[2604.22709\|Abstract-CoT]] (**12×** token reduction) |
| Visual reasoning without text bottleneck | Continuous visual tokens | [[2511.19418\|COVT]] (**+5.5%** CV-Bench) |
| Multimodal CoT inside diffusion policy | Discrete unified diffusion + CoT | [[2509.25681\|dVLA]] (**96.4%** LIBERO, **+12.5 pp** real) |
| Self-supervised step-level reasoning reward | Cross-rollout agreement | [[2601.05877\|iReasoner]] (**+1.32 / +1.64** avg) |
| Physics-grounded embodied reasoning | SFT + RL with verifiable rewards | [[2503.15558\|Cosmos-Reason1]] (**81.5%** intuitive physics, 7B) |

^dm-4

> [!star] Key Papers
> - [[2605.08732|GC-IDM]] — Amortized goal-conditioned inverse dynamics in a frozen latent world model; **100–130×** faster planning than CEM at matched/superior SR — proves search is amortizable in well-organized latent spaces
> - [[2605.00078|Being-H0.7]] — Future-informed dual-branch latent reasoning: privileged-future supervision at training, implicit prediction at deployment; SOTA on [[2306.03310|LIBERO]]/[[2406.02523|RoboCasa]] at **3–4 ms/step**
> - [[2601.11442|Map2Thought]] — Unifies discrete symbolic grids with continuous metric-scale data for explicit 3D latent reasoning; metric cognitive maps yield verifiable inference traces (**61.0%** VSI-Bench)
> - [[2604.22709|Abstract-CoT]] — Token-free latent CoT in abstract embedding space; eliminates the discrete-token bottleneck (**12×** token reduction) while preserving reasoning quality
> - [[2511.19418|COVT]] — Chain-of-Visual-Thought: continuous visual tokens let VLMs reason about vision without the text bottleneck (**+5.5%** CV-Bench)

^key-papers-4

> [!tip] Why Latent Reasoning Matters for Robots
> Pixel-level reasoning is expensive: [[2602.15922|DreamZero]]'s 14B Video DiT takes ~150 ms per forward pass. Latent reasoning removes the generation bottleneck — plan in embedding space, act in real-time. [[2602.10098|VLA-JEPA]]'s MPC uses [[2506.09985|V-JEPA-2]]'s latent predictor in a single forward pass; [[2605.08732|GC-IDM]] amortizes the search loop itself (**100–130×** faster than CEM); [[2605.00078|Being-H0.7]] eliminates the pixel-WAM tax entirely with **3–4 ms/step**. Each row above swaps one form of expensive computation for a learned latent shortcut — the constraint determines which shortcut to use. Cross-reference [[05_VLA-Reasoning-and-CoT#3. Latent Reasoning — Token-Free CoT]] for the full reasoning-insertion taxonomy these papers exemplify, [[04_VLA#5. World-Model-Augmented VLAs]] for how latent reasoning composes with WAM-augmented VLAs, and [[15_Self-Evolving-VLA-WAM#3. Core Mechanisms of Self-Evolution]] for how amortized planning enables self-evolution loops in latent space. For the manipulation-side deployment of these latent predictors as policies, see [[09_Manipulation-Skill-Learning#3.1 World-Action Models for Manipulation]].

^insight-4

---

## Part C — Analysis & Open Problems

*Latent-vs-pixel trade-offs and what the latent-world-model program has not yet solved.*

### 5. Latent vs Pixel Comparison

The central tension that organizes this whole note: *predict in pixels (rich but slow) or in embeddings (fast but opaque)?* Every architectural choice in §1–§4 sits somewhere on that axis. The 2026 frontier is hybridization — train with pixel objectives to absorb spatiotemporal priors, then deploy without test-time imagination ([[2603.16666|Fast-WAM]], [[2602.10098|VLA-JEPA]]) — but the underlying trade-off remains: each paradigm dominates one axis and loses the others.

This section frames the binary so that the right paradigm gets chosen for the constraint that *actually binds at deployment*. Speed-bottlenecked tasks (real-time control, dense MPC) pull toward latent; robustness-bottlenecked tasks (zero-shot novel environments, cross-embodiment) pull toward pixel; the rest hybridize. The choice is now less "which is best" and more "which axis is sacrificed least cheaply".

#### 5.1 Latent Side

==Predict in embedding space. Single forward pass per prediction. Opaque but fast.== Wins when inference latency is the binding constraint (real-time MPC, 10–20 Hz control loops, dense planning queries).

- **[[2608.05523|HERA]]** — A parameter-efficient adapter (==Register-Routed Patch Memory==, **3.00M** params) bolting a ==Structured Memory Bank== + gated Memory/Workspace Registers onto a frozen V-JEPA 2-G predictor for occlusion-robust physical prediction; **54.35%** IntPhys2 pairwise AvgSurprise (**+1.78pp** over baseline), **+17.31pp** on Immutability (Fixed Camera).
- **[[2602.10098|VLA-JEPA]]** — A latent-side anchor defining the speed-quality Pareto frontier; **~10 ms/step** at **97.2%** [[2306.03310|LIBERO]] in-distribution, **79.5%** [[2510.13626|LIBERO-Plus]] OOD, **65.2%** real robot.
- **[[2510.02311|IDPP]]** — Introduces **PhysVid**, a quantitative elasticity/viscosity/friction benchmark, and probes frozen V-JEPA-2 (latent) vs DynamiCrafter (generative) via lightweight visual prompting; both hit **ROC AUC 1.00** on synthetic data but trail physics-informed oracles on absolute-value prediction and real-world friction generalization.
- **[[2506.09985|V-JEPA-2]]** — A self-supervised JEPA on **1M+ hours** internet video; **80%** pick-and-place from only **62 hours** unlabeled robot video — the sample-efficiency anchor.
- **[[2411.04983|DINO-WM]]** — A task-agnostic latent dynamics model on ==frozen [[2304.07193|DINOv2]] features== via ==latent consistency loss==, where ==MPC+CEM== over feature-space rollouts achieves **+45%** average planning improvement (e.g., **0.90** PushT SR vs **0.32** IRIS) and **0.82** WallRandom OOD SR — no per-task retraining.
- **[[2603.14482|V-JEPA-2.1]]** — A dense-feature JEPA combining ==Dense Predictive Loss== (masked + unmasked tokens) + ==Deep Self-Supervision== + ==modality-specific tokenizers== (2D/3D), ViT-G on VisionMix-163M, restoring local detail JEPA loses; **RMSE 0.307** depth NYUv2 (SOTA), **7.71 mAP** Ego4D STA (**~35%** gain), **+20%** grasp SR, **10× faster** navigation planning.
- **[[2605.00078|Being-H0.7]]** — A dual-branch privileged-future latent reasoner at **3–4 ms/step**; **99.2%** [[2306.03310|LIBERO]] — proves latent prediction matches pixel-WAM SR at orders-of-magnitude lower latency.

#### 5.2 Pixel Side

==Predict full video frames via iterative denoising. Rich and human-inspectable but slow (~150 ms/forward) and expensive.== Wins when robustness or cross-embodiment transfer is the binding constraint (zero-shot novel environments, internet-scale video priors needed).

- **[[2602.15922|DreamZero]]** — A pixel-side anchor defining the robustness ceiling: **14B** joint video+action; **39.5%** unseen tasks, **42%** cross-embodiment improvement, **7 Hz** real-time at deployment cost.
- **Cosmos / [[2601.16163|Cosmos-Policy]]** — NVIDIA's pretrained video diffusion fine-tuned as a visuomotor policy; **98.5%** [[2306.03310|LIBERO]] proves pixel-space pretraining transfers cleanly to control.
- **[[2310.06114|UniSim]]** — A ==Conditional video diffusion== model (**5.6B** params) with ==dataset orchestration== over robot logs + human activity + panoramas + internet text/video, plus a ==unified T5-embedding action space==; policies trained entirely in UniSim achieve **3-4×** better goal reduction for VLMs with zero-shot sim-to-real transfer — the foundational learned-sim baseline.
- **[[2302.00111|UniPi]]** — A ==Unified Predictive Decision Process== formulating actions as ==text-to-video diffusion==, paired with a small ==inverse-dynamics model==; **60.1%** vs **12.5%** novel-language "Place" SR, **51.6%** vs **14.8%** "Place Bowl" CLIPort transfer, **77.1%** real SR with internet pretraining (vs **72.6%**) — introduced the "video IS the plan" formulation.

#### 5.3 Interpretability of Physical Representations

Do latent (JEPA) or pixel (diffusion) world models actually encode physics, or just pattern-match training statistics? Two 2026 interpretability studies probe both sides of the latent-vs-pixel divide with linear probes and causal interventions, converging on a shared, deflationary answer: physical understanding emerges as a distributed, high-dimensional population code — not a compact, reusable "physics engine" variable — regardless of architecture.

- **[[2606.05328|Invisible-Hand-of-Physics]]** — Inverts video-diffusion denoising (==reverse sampling==) to linearly probe physical plausibility from internal states; diffusion models (WAN/CogVideoX/LTX) hit **81.27%** avg probe accuracy vs V-JEPA-2's **71.36%**, **R²≥0.99** for position — physics lives in the flow, not the VAE latent.
- **[[2602.07050|Interpreting-Physics-Video-WM]]** — Layerwise probes + causal ablations on V-JEPA 2/VideoMAE-v2 locate a ==Physics Emergence Zone== (~1/3 depth) where motion direction forms a **40–80**-dim ==circular population code==, nearly orthogonal to IntPhys-judgment subspaces — no compact shared "physics engine," just distributed local-attention-built features.

**Latent vs Pixel — Decision Matrix**

| Axis | Latent | Pixel | Best For |
|---|---|---|---|
| **Speed** | Fast (**~10 ms/step**, [[2602.10098\|VLA-JEPA]]) | Slow (**~150 ms/forward**, [[2602.15922\|DreamZero]]; **7 Hz** at deploy) | **Latent** when real-time control is the constraint |
| **Interpretability** | Opaque embeddings; needs learned evaluators | Visual video; human-inspectable rollouts | **Pixel** when debugging, safety verification, or oracle review matters |
| **Sample Efficiency** | High (**62 hr** unlabeled → **80%** pick-and-place, [[2506.09985\|V-JEPA-2]]) | Moderate (needs internet-scale video to converge) | **Latent** when robot data is scarce |
| **Physics Priors** | Learned from video SSL targets | Learned from internet-video generation; strongest internet-video → robot transfer | **Pixel** when physics fidelity matters and latency is acceptable |
| **Fine-Grained Detail** | Moderate ([[2603.14482\|V-JEPA-2.1]] adds dense loss to recover local structure) | High (pixel-level by construction) | **Pixel** for dense tasks (depth from pixels, fine geometry); **Latent + dense loss** for compressed alternative |
| **Cross-Embodiment** | Limited (latent space tied to encoder) | Strong (video priors transfer across robot platforms, **+42%** in [[2602.15922\|DreamZero]]) | **Pixel** when targeting new embodiments not in robot pretraining data |
| **Deployment Cost** | Single forward pass; fits real-time MPC | Iterative denoising; needs distillation or test-time skipping ([[2603.16666\|Fast-WAM]]) | **Latent** for production deployment; **Pixel** for offline planning |
| **Reasoning Insertion** | Continuous-thought CoT in embedding stream ([[2604.22709\|Abstract-CoT]], [[2511.19418\|COVT]]) | VLM-guided pixel critic ([[2603.08403\|SPIRAL]] in [[06_WAM#7. Self-Evolving WAMs]]) | **Latent** for tight VLA reasoning loops; **Pixel** for plan-then-critique |

^dm-5

> [!star] Key Papers
> - [[2602.10098|VLA-JEPA]] — Latent-side anchor; **97.2%** [[2306.03310|LIBERO]] at **~10 ms/step** defines the speed-quality Pareto frontier — proves latent rivals pixel SR at orders-of-magnitude lower latency
> - [[2506.09985|V-JEPA-2]] — Latent-side scale anchor; **80%** pick-and-place from only **62 hours** unlabeled robot video shows latent prediction transfers from internet video without per-task retraining
> - [[2411.04983|DINO-WM]] — Latent-side zero-shot baseline; frozen [[2304.07193|DINOv2]] + lightweight dynamics enables planning in new environments without retraining
> - [[2602.15922|DreamZero]] — Pixel-side anchor; **14B** joint video+action defines the robustness ceiling; **39.5%** unseen tasks, **42%** cross-embodiment, **7 Hz** real-time at deployment cost
> - [[2601.16163|Cosmos-Policy]] — Pixel-side proof point; **98.5%** [[2306.03310|LIBERO]] from fine-tuned video diffusion shows pretrained pixel models transfer cleanly to control
> - [[2603.16666|Fast-WAM]] — The hybridization recipe — train with video objectives, deploy without test-time imagination — that resolves the binary by ==training pixel, deploying latent==

^key-papers-5

> [!tip] The 2026 Consensus — Train Pixel, Deploy Latent
> The binary collapses at deployment but not at training. You need video generation at **training time** (to absorb spatiotemporal priors and physics fidelity that internet video provides) but NOT at **test time** (where it adds **~150 ms/forward** of latency that breaks real-time control). [[2603.16666|Fast-WAM]] proved this works: train with video objectives, deploy with a slim action expert. [[2602.10098|VLA-JEPA]] takes the same insight further — operate entirely in latent space at deployment while still benefiting from video-SSL pretraining targets. The 2026 frontier is no longer "latent vs pixel" but "*which* pixel objective stays at training and *which* latent shortcut runs at deployment". Cross-reference [[06_WAM#6. Efficient & Action-Centered WAMs]] for the broader train-with-video, deploy-without-video recipe, [[06_WAM#8. Cross-Paradigm Comparison]] for the five-paradigm framing that places latent and pixel as two of the five, [[04_VLA#6. RL Post-Training for VLAs]] for how the train-pixel-deploy-latent split shapes the WAM-augmented VLA stack, and [[08_Physics-Aware-Embodied-AI#5. Physics-Aware Reasoning]] for the physics-fidelity dimension that pixel training is uniquely positioned to absorb. The evaluation suites that make the pixel-vs-latent claim falsifiable are in [[02_Dataset-Benchmark-Environment#11. World Model Benchmarks]].

^insight-5

---

### 6. Open Problems

Latent world models are powerful but face fundamental limitations that remain unsolved. All four problems below share a common compression-opacity root — but they manifest at different levels of the stack (sensor, representation, evaluation, trust), and the remediation papers attack different levels.

- **==Fine-grained contact physics==** — Latent prediction excels at object trajectories and coarse dynamics, but struggles with contact-rich manipulation (insertion, assembly, surface following) where sub-millimeter accuracy matters. Pixel-space models capture contact better, but at prohibitive cost. The right fix is likely hybrid (latent global, pixel-attention contact) — undemonstrated.
- **==Novel object generalization==** — JEPA models trained on internet video encode priors about common objects, but struggle with novel materials (deformable, transparent, articulated) not well-represented in training data. [[2411.04983|DINO-WM]]'s ==frozen DINO features== partially address this for geometry, but material properties remain challenging.
- **==Interpretability gap==** — Latent predictions are opaque — a human cannot inspect whether the model's "imagined future" makes physical sense, limiting debugging and safety verification. [[2603.22281|ThinkJEPA]]'s ==VLM-guided latent grounding== partially bridges this by grounding latent predictions in natural language descriptions.
- **==Latent-pixel alignment / trust==** — When is a latent prediction "wrong enough" to warrant concern? Unlike pixel-space models where humans can visually inspect dreams, latent-space errors require learned evaluators — creating a recursive trust problem (the evaluator itself may be miscalibrated).

**Latent World Model Failure Modes — Decision Matrix**

| Problem | Remediation Path |
|---|---|
| Contact-rich manipulation needs sub-mm accuracy | Hybrid latent + local pixel attention — currently undemonstrated; fall back to pixel WAMs for the contact stage ([[06_WAM#2. VideoGen WAMs]]) |
| Novel-object / novel-material generalization | [[2411.04983\|DINO-WM]] (frozen DINO for geometry); material properties still open |
| Need to inspect latent rollouts for plausibility | [[2603.22281\|ThinkJEPA]] (VLM grounds latent state in language) |
| Need calibrated uncertainty on latent predictions | No clean solution — closest is [[2603.22281\|ThinkJEPA]] + a latent-space [[2410.05363\|PhyGenBench]] equivalent (research gap) |
| Want a higher-level latent reasoning substrate | See [[05_VLA-Reasoning-and-CoT#3. Latent Reasoning — Token-Free CoT]] for the reasoning-side companion |

^dm-6

> [!star] Key Papers — Latent Failure Frontier
> - [[2603.22281|ThinkJEPA]] — First system to ground latent rollouts in natural language via VLM; the canonical interpretability bridge for opaque JEPA dynamics
> - [[2411.04983|DINO-WM]] — Demonstrates that *frozen* pretrained features (DINO) can substitute for learned latent dynamics on novel-object geometry; the strongest evidence that the JEPA-style latent space generalizes when the encoder is held fixed
> - [[2602.10098|VLA-JEPA]] — Production JEPA-based VLA that exposes the contact-physics gap concretely (excels at trajectory, weakens on insertion); the load-bearing benchmark for "does latent prediction work for robots?"

^key-papers-6

> [!tip] The Common Root Is Opacity — Not Compression
> Three of the four problems (contact physics, interpretability, latent-pixel alignment) trace to the same root: latent prediction *compresses away* the very details — contact transients, material textures, fine geometry — that humans use to verify "is this physically plausible?". The fix is *not* reverting to pixel space (too expensive) but building learned evaluators that operate in latent space and report calibrated uncertainty. [[2603.22281|ThinkJEPA]] is the first step; the harder problem is a latent-space [[2410.05363|PhyGenBench]] equivalent — currently absent from the literature. Cross-reference [[06_WAM#9. Open Problems & Failure Modes]] (the pixel-space companion failure modes — same calibration root, different surface) and [[05_VLA-Reasoning-and-CoT#7. Open Problems]] (latent reasoning faithfulness, which has identical opacity-to-the-human-inspector dynamics).

^insight-6

---

## Quick-Reference Matrix

| Question | Answer |
|----------|--------|
| Need self-supervised video pretraining? | [[2506.09985\|V-JEPA-2]] (or [[2301.08243\|I-JEPA]] for static images) |
| Need dense local + global features? | [[2603.14482\|V-JEPA-2.1]] (deep self-supervision) |
| Need vision-language without generation? | [[2512.10942\|VL-JEPA]] (efficient InfoNCE alignment) |
| Need a full robot controller in latent space? | [[2602.10098\|VLA-JEPA]] or [[2602.11832\|JEPA-VLA]] |
| Need world model as planning substrate? | [[2510.00739\|TD-JEPA]] or [[2511.19221\|Percept-WAM]] |
| Need latent reasoning / continuous thought? | [[2603.22281\|ThinkJEPA]] or [[2601.21598\|ATP-Latent]] |
| Need non-JEPA latent dynamics? | [[2411.04983\|DINO-WM]] (frozen DINO) or [[2504.02792\|UWM]] |
| Need probabilistic / belief-space latent prediction? | [[2601.14354\|VJEPA-Probabilistic]] or [[2605.25313\|UWM-JEPA]] (uncertainty-aware) |
| Need pretraining without action labels? | [[2512.13030\|Motus]] (latent motion priors) |
| Want pixel-space WAM instead? | See [[06_WAM#2. VideoGen WAMs]] for VideoGen lineage |

---

## Cross-References

- [[06_WAM]] — WAM deep-dive (Section 3 covers latent prediction WAMs)
- [[04_VLA]] — VLA deep-dive (Section 5 covers WAM-augmented VLAs)
- [[02_Dataset-Benchmark-Environment]] — Benchmarks for evaluating latent world models
- [[15_Self-Evolving-VLA-WAM]] — Self-evolving VLAs & WAMs ([[2602.10098|VLA-JEPA]] as a self-evolving target)
- [[08_Physics-Aware-Embodied-AI]] — Physics-aware latent dynamics and physical commonsense
- [[05_VLA-Reasoning-and-CoT]] — Latent reasoning insertion patterns ([[2604.22709|Abstract-CoT]], [[2509.25681|dVLA]])
- [[13_Egocentric-Pretraining-and-Human-Video]] — Egocentric pretraining substrates for latent models
- [[10_Contact-Rich-and-Tactile-Control]] — Force/tactile policies deep-dive; complements latent representation for multi-sensor inputs
- [[01_Embodied-AI-101]] — Embodied AI basics

---

*See [[06_WAM]] for the full WAM taxonomy, [[05_VLA-Reasoning-and-CoT]] for latent reasoning insertion, or [[15_Self-Evolving-VLA-WAM]] for how latent world models enable self-evolution.*
