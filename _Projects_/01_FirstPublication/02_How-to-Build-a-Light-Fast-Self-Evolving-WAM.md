---
title: "How to Build a Light & Fast Self-Evolving WAM"
tags:
  - self-evolving
  - WAM
  - robotics
  - LeWM
  - Fast-WAM
  - JEPA
  - methodology
aliases:
  - LeWM++ Methodology
  - Light Self-Evolving WAM
---

# How to Build a Light & Fast Self-Evolving WAM

> [!abstract] One-Line Summary
> A revised methodology for self-evolving World Action Models that starts from ==a lightweight JEPA core== (~15-45M inference params) instead of a 14B DiT, builds and validates ==each self-evolution loop independently== before combining them, and uses ==video co-training as a training-only auxiliary== to enrich latent representations without paying inference cost.

> [!info] Context
> This methodology is informed by [[00_How-to-Build-Self-Evolving-WAM|the original Self-Evolving WAM Blueprint]] and its two adversarial critiques ([[01_Critique-Self-Evolving-WAM|domain transfer critique]], [[01_Critique-Methodology-Self-Evolving-WAM|methodology critique]]). It retains the thesis that static WAMs need self-evolution, but replaces the 3-nested-loop architecture with a sequential, independently validated approach that avoids the structural contradictions identified in the critiques.

---

## Why Light & Fast Matters

The original blueprint proposed [[2602.15922|DreamZero]] (14B parameters) as the base Imaginer. The methodology critique exposed why this is impractical for self-evolution:

| Problem | Evidence | Consequence |
|---------|----------|-------------|
| **CEM planning doesn't scale** | [[2603.19312\|LeWM]]'s CEM requires 30,000-50,000 forward passes per action. At 14B, each pass costs ~150ms → ==2 hours per action== | Test-time adaptation via imagination is computationally impossible at 14B |
| **Curiosity ensemble is intractable** | [[2005.05960\|Plan2Explore]]'s ensemble of $k=5$ copies of 14B = ==70B parameters== | No lab can maintain 70B for curiosity alone |
| **Co-evolution requires repeated training** | [[2602.12063\|VLAW]]'s iterative alternation requires retraining the world model ==every round== | Fine-tuning 14B per co-evolution round demands cluster-scale compute |
| **Inference speed blocks deployment** | WAMs are already ==4.8x slower== than VLAs ([[2603.22078\|WAM vs VLA Robustness]]) | A 14B WAM at real-time control frequency is infeasible on a single GPU |

> [!tip] The Insight
> Self-evolution needs a model you can ==train repeatedly, plan through rapidly, and deploy at real-time speed==. A 15-45M model running at 50+ Hz enables all three. The question is whether a model this small can capture enough physics to be useful — and whether the training signal can be enriched without adding inference cost.

---

## Architecture: LeWM++

The core idea is a hybrid of two papers:

1. **[[2603.19312|LeWM]]** — a 15M JEPA world model that is ==collapse-proof== (SIGReg regularizer), ==48x faster== than foundation-model WMs, and trainable on a single GPU. Proved on Push-T and Reacher.

2. **[[2603.16666|Fast-WAM]]** — showed that ==video co-training during training== enriches action representations even when video generation is ==entirely removed at inference==. Proved on LIBERO (97.6%) and RoboTwin (91.8%).

The hybrid takes LeWM's lightweight JEPA core and adds Fast-WAM's video decoder as a ==training-only auxiliary head==:

```
                        ┌─────────────────────────┐
  Observation ────────► │  Encoder (ViT-Tiny/Small)│ ──► Latent z_t
                        └─────────────────────────┘
                                                          │
                                          z_t + action a_t│
                                                          ▼
                        ┌─────────────────────────────────────┐
                        │  Latent Predictor (MLP + AdaLN)     │ ──► Predicted ẑ_{t+1}
                        └─────────────────────────────────────┘
                              │                          │
                              ▼                          ▼
                   ┌──────────────────┐      ┌────────────────────┐
                   │  Video Decoder   │      │    Action Head     │
                   │  (TRAINING ONLY) │      │  (MLP: z → action) │
                   └──────────────────┘      └────────────────────┘
                   Stripped at inference      Used for direct policy
```

### Why This Combination Works

> [!warning] The Problem with JEPA Alone
> LeWM's MSE-only prediction loss produces latent spaces that are "correct but impoverished" — they predict future states accurately but don't necessarily encode ==rich visual features==. The latent space captures what it needs for prediction error minimization, which may be a low-dimensional summary that discards visual detail useful for downstream tasks.

> [!success] Fast-WAM's Key Finding
> Fast-WAM demonstrated that video co-training forces the latent space to encode ==spatiotemporal dynamics at pixel level==. The critical insight: the performance drop from removing video co-training during *training* was ==consistently larger== than the drop from removing video generation during *inference*. The training-time video objective is what matters, not test-time generation.

> [!success] The Hybrid
> By adding a video decoder that reconstructs future frames from predicted latent states ==only during training==, we force LeWM's JEPA latent space to encode visual dynamics (richer gradients from reconstruction loss) while keeping inference lightweight (decoder is stripped). SIGReg ensures the latent space remains stable even under continuous self-evolution fine-tuning.

### Module Details

| Module | Architecture | Params | Role |
|--------|-------------|--------|------|
| **Encoder** | ViT-Tiny → ViT-Small (scales with task complexity) | 6-22M | Maps RGB observations → latent vectors |
| **Latent Predictor** | Feed-forward blocks with ==AdaLN== (Adaptive Layer Normalization) conditioned on action | 8-20M | Predicts next latent state given current state + action |
| **Video Decoder** | 4-layer transposed CNN | 15-30M | Reconstructs frames from predicted latents — ==training-only== |
| **Action Head** | 2-layer MLP | 1-2M | Direct latent → action mapping for fast inference |

### Training Objective

$$L_{\text{total}} = L_{\text{pred}} + \lambda_{\text{sig}} \cdot L_{\text{SIGReg}} + \lambda_{\text{vid}} \cdot L_{\text{video}} + \lambda_{\text{act}} \cdot L_{\text{action}}$$

| Term | Purpose | Source |
|------|---------|--------|
| $L_{\text{pred}}$ (MSE) | Latent prediction accuracy — the JEPA core objective | [[2603.19312\|LeWM]] |
| $L_{\text{SIGReg}}$ | Prevents representation collapse by regularizing toward isotropic Gaussian (variance → 1, covariance → 0). Only 1 tunable hyperparameter ($\lambda$) | [[2603.19312\|LeWM]], [[2511.08544\|LeJEPA]] |
| $L_{\text{video}}$ | Forces latent space to encode visual dynamics — ==richer than MSE alone== | [[2603.16666\|Fast-WAM]] insight |
| $L_{\text{action}}$ | Trains the direct policy head for fast inference | Standard behavioral cloning |

### Two Inference Modes

1. **CEM Planning** ([[2603.19312|LeWM]]-style): Sample action sequences → forward-simulate through Predictor → score against goal latent → resample elites. No Action Head needed. Slower but generalizes to novel goals.
2. **Direct Policy** ([[2603.16666|Fast-WAM]]-style): Encoder → Predictor → Action Head in one forward pass. Faster for trained tasks.

Both modes run ==without the Video Decoder== — inference cost is only 15-45M parameters.

### Scale Targets

| Benchmark | Encoder | Training Params | Inference Params | Target Hz |
|-----------|---------|----------------|-----------------|-----------|
| Push-T / Reacher | ViT-Tiny (6M) | ~30M | ~15M | 50+ Hz |
| LIBERO / RoboTwin | ViT-Small (22M) | ~75M | ~45M | 15+ Hz |

---

## The Key Methodological Shift: Sequential Loop Validation

The original blueprint proposed ==three nested loops running simultaneously==. The methodology critique showed this creates destructive interference:

- Inner Loop forward-updates (ms) are overwritten by Middle Loop backprop (hours)
- Inner Loop's ephemeral adaptations corrupt Middle Loop's training distribution
- Outer Loop environment changes invalidate both Inner and Middle Loop progress
- The system has no external ground truth — every metric is self-assessed

> [!danger] The Original Failure
> Nesting the loops assumes they ==compose gracefully==. No evidence exists that they do. Each loop was validated in isolation in its source paper, and no paper tested the interaction between any two loops, let alone all three.

> [!success] The Fix: Build Each Loop Independently
> Instead of nesting, ==build and test each loop in isolation==. Each becomes a falsifiable experiment with its own held-out evaluation. Only combine loops after each has independently demonstrated value. This transforms an unfalsifiable architecture into a sequence of testable hypotheses.

---

## Phase 0-1: Build the Base Model

**Goal**: Prove that the LeWM++ hybrid architecture works — that video co-training improves latent quality over JEPA alone.

### Benchmark Progression

Following the papers that demonstrated each component:

| Phase | Benchmark | Following | Why |
|-------|-----------|-----------|-----|
| 0 | Push-T, Reacher | [[2603.19312\|LeWM]] | Simple 2D tasks where LeWM proved the JEPA core works |
| 1 | LIBERO, RoboTwin | [[2603.16666\|Fast-WAM]] | 3D manipulation where Fast-WAM proved video co-training works |

### The Critical Ablation

Before adding any self-evolution, validate the ==architecture itself== via ablation:

| Variant | Training Objective | What It Tests |
|---------|-------------------|---------------|
| **Baseline** (LeWM) | $L_{\text{pred}} + L_{\text{SIGReg}}$ | JEPA core alone |
| **+ Video Aux** | $L_{\text{pred}} + L_{\text{SIGReg}} + L_{\text{video}}$ | Does video co-training improve latent quality? |
| **+ Full** (LeWM++) | All four terms | Does the action head complement or interfere? |

**Success criterion**: `+ Video Aux` should show measurably better latent quality than `Baseline` — either via better linear probing of physical quantities from the latent space, or faster CEM convergence to goal states.

> [!question] Why not skip to self-evolution?
> If the base architecture doesn't work — if the video auxiliary doesn't improve the latent space — then self-evolution loops built on top of it will inherit the same limitation. Validating the foundation first avoids building a complex system on unverified assumptions. This is the mistake the original blueprint made: it assumed every component worked and focused on integration, without ever testing the components.

---

## Phase 2: Co-Evolution Loop (Middle Loop)

**Goal**: The world model and policy iteratively improve each other, following [[2602.12063|VLAW]]'s empirically validated mechanism.

### The Mechanism

```
Round N:
  1. Policy π_n rolls out in sim → trajectories T_n (including failures)
  2. World Model fine-tunes on T_n (L_pred + L_SIGReg + L_video)
  3. World Model generates dream trajectories, filtered by prediction error
  4. Policy fine-tunes on α·dreams + (1-α)·replay → becomes π_{n+1}
  5. Evaluate π_{n+1} on held-out tasks
  → Repeat
```

### What Changed from the Original Blueprint

| Original Blueprint | This Methodology | Reasoning |
|-------------------|------------------|-----------|
| Plan2Explore curiosity ensemble ($k \times 14B$) | ==No curiosity ensemble== | At 15-45M, the model is small enough to train frequently. Curiosity is valuable but not needed for v1 — VLAW showed co-evolution works without it |
| EWC + Replay + Gradient Projection (triple CL stack) | ==Replay buffer only== | [[2603.11653\|VLA RL Continual Learning]] showed <2% forgetting with simple LoRA fine-tuning. [[2603.03818\|VLA Continual Learning]] confirmed only 2% replay buffer needed. ==Test the simple approach first== |
| SPIRAL CriticAgent for dream quality | ==Self-consistency filtering== (keep dreams with lowest prediction error) | SPIRAL's CriticAgent evaluates ==video quality, not physics validity== ([[01_Critique-Self-Evolving-WAM#Specific Miscitations\|domain transfer critique]]). Prediction error is a direct, domain-appropriate quality signal |
| No fallback if success drops | ==Automatic fallback==: if success rate drops between rounds, reduce dream ratio | The original blueprint had one-directional phase transitions with no recovery mechanism |

### Why This Should Work at Small Scale

The original blueprint assumed co-evolution needs a 14B model for rich enough imagination. But VLAW's mechanism doesn't depend on model scale — it depends on the ==quality of the alternation cycle==:

1. The world model must improve its predictions when given new trajectory data → LeWM++ can do this (standard supervised fine-tuning)
2. The world model must generate plausible dream trajectories → LeWM++ generates in latent space (fast) and the video decoder (still attached during training) provides reconstruction quality signal
3. The policy must improve when trained on filtered dreams → Standard behavioral cloning on dreams

The key insight from [[2602.12063|VLAW]]: the world model started with FVD 225.13 and dropped to 64.12 after real-world grounding. The improvement came from ==seeing failure trajectories==, not from model scale. A smaller model that sees the same failures should improve similarly.

> [!tip] The Real Question
> Can a 15-45M model generate dreams that are ==diverse enough== for meaningful policy improvement? VLAW used a much larger model. This is the testable hypothesis of Phase 2. If dreams lack diversity, the solution is better data (more rollouts, more diverse initial states), not a bigger model.

### Success Criterion

Measurable success rate improvement over co-evolution rounds. [[2602.12063|VLAW]] showed 0.46 → 0.868 (39.2% absolute gain). At smaller model scale, expect a smaller but positive gain. **Done when**: positive slope for $\geq 3$ consecutive rounds, $> 10\%$ total gain.

---

## Phase 3: Test-Time Adaptation (Inner Loop)

**Goal**: The deployed model adapts to novel physics during inference without retraining.

### What Changed from the Original Blueprint

The original Inner Loop combined four mechanisms: NavMorph CEM, AVIC adaptive depth, Fast-WAM inference, and LeWM planning. The methodology critique showed these are ==internally contradictory==:

> [!danger] The Original Contradiction
> [[2603.16666|Fast-WAM]] removes video generation at inference (4x speedup). But test-time adaptation ==requires imagination== — comparing predicted vs. observed futures. If imagination is removed, the adaptation signal disappears. The blueprint wanted test-time adaptation AND test-time speed. Fast-WAM proved these are a tradeoff, not a combination.

> [!danger] NavMorph Can Only Interpolate
> [[2506.23468|NavMorph]]'s Contextual Evolution Memory retrieves ==similar past experiences== when prediction error spikes. For genuinely novel physics (the point of self-evolution), the memory has no similar experience to retrieve. Forward-update without backprop can adapt ==representations== (what the model sees) but not ==dynamics== (what the model predicts will happen).

### The Simpler Mechanism: Prediction-Error-Triggered Gradient Steps

Instead of NavMorph's memory bank or AVIC's gatekeeper, use a direct signal:

```
During inference on a new episode:
  for each timestep t:
    1. Encode observation → z_t
    2. Predict: ẑ_{t+1} = Predictor(z_t, a_t)
    3. Execute action, observe, encode → z_{t+1}
    4. Compute prediction error: e_t = ||ẑ_{t+1} - z_{t+1}||²

    if e_t > threshold (rolling mean + 2σ):
      → "Surprise" — physics mismatch detected
      → Run 3-5 gradient steps on Predictor's LAST 2 LAYERS only
        using recent buffer of 32 (z, a, z') triplets

  After episode: RESET predictor weights to pre-episode checkpoint
```

### Why Only Last 2 Layers + Reset

The methodology critique identified that Inner Loop forward-updates corrupt the Middle Loop's training distribution:

> Inner Loop's test-time adaptation corrupts the training signal for the Middle Loop's co-evolution. — [[01_Critique-Methodology-Self-Evolving-WAM#4.2 The Inner Loop Undermines the Middle Loop's Training Distribution|Part IV.2]]

The fix addresses this directly:

1. **Only last 2 layers**: Adapting the predictor's final layers changes ==how it combines features== to predict dynamics, without changing ==what features the encoder extracts==. The encoder's representation remains stable for the Middle Loop.
2. **Reset after episode**: Adaptations are ==ephemeral== — they help during the current episode but don't persist. The Middle Loop sees trajectories from the base model, not the adapted model.

This avoids the timescale conflict: Inner Loop adaptations (milliseconds) no longer interfere with Middle Loop training (hours) because they don't persist.

### Evaluation Protocol

1. Train base model on standard LIBERO tasks (from Phase 1)
2. Create ==perturbed variants==: modify object mass ($0.5\times$-$2\times$), friction ($0.5\times$-$2\times$), table height ($\pm 5$cm)
3. Compare success rate: base model vs. base + test-time adaptation
4. **Target**: $>15\%$ improvement on perturbed tasks, $<20$ms per adaptation step (maintains $>10$Hz control)

> [!tip] Phases 2 and 3 Are Independent
> Co-evolution (Phase 2) and test-time adaptation (Phase 3) do not depend on each other. They can be developed and validated ==in parallel== after Phase 1. This is another departure from the original blueprint, which required all three loops to be nested.

---

## Phase 4: Auto-Curriculum (Outer Loop)

**Goal**: The system generates its own harder tasks when current ones are solved.

### What Changed from the Original Blueprint

The original Outer Loop used [[1901.01753|POET]] and [[2502.05726|ACCEL]] for environment co-evolution. The critiques identified two problems:

1. **POET operates in 2D bipedal walker domains** ([[01_Critique-Self-Evolving-WAM#Specific Miscitations|domain transfer critique]]). Real manipulation environments have infinite-dimensional variation (geometry, material, friction, lighting). POET's terrain parameterization doesn't transfer.

2. **Manipulation difficulty is non-monotonic** ([[01_Critique-Methodology-Self-Evolving-WAM#3.1 Manipulation Difficulty Is Non-Monotonic|methodology critique]]). A small change in object mass can cause a ==discontinuous jump== from "solvable" to "impossible." The Goldilocks zone isn't a smooth gradient — it's a fractal boundary.

### The Simpler Mechanism: Physics Parameter Bandit

Instead of learning an environment generator, ==parameterize the physics== directly. MuJoCo (LIBERO's backend) exposes all relevant parameters:

$$P = \{\text{mass}: [0.5\times, 3.0\times], \; \text{friction}: [0.3\times, 2.0\times], \; \text{size}: [0.7\times, 1.5\times], \; \text{damping}: [0.5\times, 2.0\times]\}$$

The curriculum controller:

1. **Sample** $N$ parameter vectors from $P$
2. **Evaluate** policy success/failure on each parameterization
3. **Identify frontier**: parameter settings where success rate $\in [20\%, 80\%]$ (Goldilocks zone)
4. **Train** on frontier tasks via one co-evolution round (Phase 2)
5. **Re-evaluate** → frontier shifts outward
6. **Repeat**

### What This Can and Cannot Do

| Can Do | Cannot Do |
|--------|-----------|
| Vary ==how hard== existing tasks are | Generate ==new task types== |
| Discover physics regimes the model fails on | Create novel object geometries or scene layouts |
| Expand competence within the parameterized space | Explore truly open-ended environments |

This is explicitly narrower than POET. But it's ==implementable, testable, and avoids the parameterization problem== — you don't need to learn an environment generator when the physics engine already exposes the parameters.

### Success Criterion

The system autonomously solves physics regimes not in the original training data. Plot the frontier boundary over curriculum rounds — it should shift outward, indicating expanding competence.

---

## Loop Interaction Rules

> [!warning] Why the Original Nesting Failed
> The original blueprint drew nested boxes but never specified how the loops synchronize. The methodology critique showed that Inner Loop forward-updates (ms) are overwritten by Middle Loop backprop (hours), Middle Loop's training distribution is corrupted by Inner Loop's adaptations, and Outer Loop's environment changes invalidate both. — [[01_Critique-Methodology-Self-Evolving-WAM#Part IV: Why the Three Loops Can't Be Nested|Part IV]]

When loops are eventually combined (after independent validation), these rules prevent the identified interference patterns:

| Rule | Prevents |
|------|----------|
| Inner Loop adaptations ==reset after each episode== | Corrupting Middle Loop's training data (Part IV.2) |
| Middle Loop ==freezes during Inner Loop evaluation== | Weight updates during adaptation measurement |
| Outer Loop ==only advances after Middle Loop converges== | Shifting environment while co-evolution is in progress (Part IV.1) |
| Each loop uses ==its own held-out evaluation set== | Circular self-grading (Part VI) |

The last rule directly addresses the convergence critique: ==every metric is external to the loop being evaluated==. No loop grades its own performance.

---

## Why Simple Continual Learning Suffices

The original blueprint proposed three simultaneous CL mechanisms: EWC, Latent Experience Replay, and Task-Aware Gradient Projection. The methodology critique showed these ==fight each other==:

> EWC says "don't change weight $w_i$." Gradient Projection says "change $w_i$, but only orthogonally." If the orthogonal subspace is empty, the system is frozen — it can never learn anything new. — [[01_Critique-Methodology-Self-Evolving-WAM#2.4 The Three CL Mechanisms Conflict|Part II.4]]

The strongest counter-evidence comes from the blueprint's own citations:

- [[2603.11653|VLA RL Continual Learning]]: Simple Sequential Fine-Tuning with LoRA achieves ==$<2\%$ forgetting==. Complex CL methods (regularization, replay, parameter isolation) were consistently ==outperformed== by this simple recipe.
- [[2603.03818|VLA Continual Learning]]: Pretrained VLAs achieve "near-zero to positive Negative Backward Transfer" with only ==$2\%$ replay buffer==.

> [!success] The Principle
> ==Test the simple approach first.== Start with replay-only continual learning. Add complexity only if forgetting actually occurs during co-evolution. The evidence suggests it won't — pretrained models with sufficient capacity naturally resist catastrophic forgetting, especially with LoRA's low-rank constraint.

---

## What Survives from the Original Blueprint

| Retained | Changed | Dropped |
|----------|---------|---------|
| The thesis: static WAMs need self-evolution | 14B DreamZero → 15-45M LeWM++ hybrid | NavMorph CEM (can only interpolate) |
| VLAW co-evolution (39.2% gain, real manipulation) | Three nested loops → three sequential, independent loops | AVIC adaptive depth (miscited for manipulation) |
| Fast-WAM inference insight (video co-training) | Triple CL stack → replay-only | SPIRAL CriticAgent (evaluates video, not physics) |
| PlayWorld autonomous data collection | POET environment generator → physics parameter bandit | Plan2Explore curiosity ensemble (70B overhead) |
| The three-loop structure (Inner, Middle, Outer) | Convergence via held-out eval → no circular self-grading | EvoAgent's "72% gain" (was in Minecraft) |
| Failure data is non-negotiable | | ECHO's co-evolving critics (text-agent domain) |
| | | Absolute Zero's verifier (requires physics oracle) |

---

## Summary: Five Design Principles

> [!tip] 1. Start light, prove the architecture
> A 15-45M model that runs at 50+ Hz enables rapid iteration. Validate the LeWM++ hybrid (JEPA + video auxiliary) with ablation before building on it. If the foundation doesn't work, scaling up won't fix it.

> [!tip] 2. Build loops independently, not nested
> Each self-evolution loop is a testable hypothesis. Co-evolution (VLAW-style), test-time adaptation (prediction-error-triggered), and auto-curriculum (physics parameter bandit) should each demonstrate value alone before combination.

> [!tip] 3. Use the simplest mechanism that could work
> Replay-only CL instead of triple stack. Prediction-error filtering instead of CriticAgent. Physics parameter bandit instead of learned environment generator. Complexity is earned by evidence, not assumed by design.

> [!tip] 4. Every evaluation metric must be external
> No loop grades itself. Each loop has a held-out test set independent of its training signal. This prevents the "student writes and grades their own exam" failure mode identified in the convergence critique.

> [!tip] 5. If it fails, the failure is publishable
> Each phase is independently falsifiable. If the video auxiliary doesn't help → that's a finding about JEPA latent richness. If co-evolution doesn't work at small scale → that's a finding about model capacity requirements for dream quality. If test-time adaptation doesn't help on perturbed physics → that's a finding about the limits of gradient-based online adaptation. Every negative result informs the field.

---

## Key Papers Referenced

### Architecture Sources

| Paper | What We Use |
|-------|-------------|
| [[2603.19312\|LeWM]] | JEPA core: ViT encoder + Transformer predictor + SIGReg anti-collapse + CEM planning. 15M params, 48x faster, collapse-proof |
| [[2603.16666\|Fast-WAM]] | Video co-training insight: train with video objective, deploy without video decoder. 97.6% LIBERO, 4x faster inference |
| [[2511.08544\|LeJEPA]] | SIGReg theoretical foundation: provable anti-collapse via isotropic Gaussian regularization. Scales to 1.8B |
| [[2301.04104\|DreamerV3]] | Actor-critic in latent space pattern. Single hyperparameter set across 150+ tasks |

### Self-Evolution Mechanisms

| Paper | What We Use |
|-------|-------------|
| [[2602.12063\|VLAW]] | Co-evolution loop: iterative alternation between world model and policy training. 39.2% gain on contact-rich tasks |
| [[2603.09030\|PlayWorld]] | Autonomous data collection via self-play. 65% improvement from 30h of real play data |
| [[2603.11653\|VLA RL Continual Learning]] | Evidence that simple LoRA fine-tuning achieves <2% forgetting. Complex CL unnecessary for pretrained models |
| [[2603.03818\|VLA Continual Learning]] | Confirms forgetting resistance: only 2% replay buffer needed for near-zero backward transfer |

### Motivation (Why Self-Evolution)

| Paper | What It Shows |
|-------|---------------|
| [[2603.22078\|WAM vs VLA Robustness]] | VLAs brittle to perturbations; WAMs robust but 4.8x slower — static models face speed-quality tradeoff |
| [[2505.03500\|TLI]] | VLAs spatially overfit: only 9% on novel compositions |
| [[2511.16166\|EvoVLA]] | Self-evolution reduces stage hallucination by 23.7 percentage points |
| [[2601.11421\|GM-100]] | Best VLA achieves only 24.9% on detail-oriented manipulation |

### Critiques Informing This Design

| Document | Key Contribution |
|----------|-----------------|
| [[01_Critique-Self-Evolving-WAM]] | Domain transfer analysis: only 6 of ~15 core papers demonstrated on real manipulation. Critical miscitations (EvoAgent = Minecraft, SPIRAL CriticAgent = video quality, AVIC = spatial VQA) |
| [[01_Critique-Methodology-Self-Evolving-WAM]] | Structural analysis: Inner Loop self-contradicting (Fast-WAM removes imagination, CEM requires it), Middle Loop unstable (indefinite co-evolution either converges or diverges), CL fights self-evolution, loops can't synchronize, no external ground truth |

---

*Revision of [[00_How-to-Build-Self-Evolving-WAM]]. Informed by [[01_Critique-Self-Evolving-WAM]] and [[01_Critique-Methodology-Self-Evolving-WAM]]. See also: [[04-2_Self-Evolving-WAM-101]] | [[04_WAM]] | [[03_VLA]]*
