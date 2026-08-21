---
title: How to Build a Self-Evolving WAM
tags:
  - self-evolving
  - WAM
  - robotics
  - DreamZero
  - VLA-JEPA
  - continual-learning
aliases:
  - Self-Evolving WAM Blueprint
---

# How to Build a Self-Evolving WAM

> [!abstract] One-Line Summary
> A 3-loop architecture for adding self-evolution to a trained [[2602.15922|DreamZero]] or [[2602.10098|VLA-JEPA]]: an ==Inner Loop== (test-time adaptation), a ==Middle Loop== (training-time co-evolution of Imaginer + Actor), and an ==Outer Loop== (auto-curriculum + environment generation) — stabilized by continual learning across all layers.

> [!info] Prerequisite Reading
> [[16_Self-Evolving-VLA-WAM]] | [[06_WAM]] | [[07_Latent-World-Models]]

---

## Why Self-Evolving WAM?

> [!danger] The Core Problem
> Today's best VLAs and WAMs are **static**: they learn once during training and deploy as frozen policies. This creates fundamental failure modes that no amount of pre-training data can fully resolve.

### The Five Walls of Static Models

| Failure Mode | Evidence | Impact |
|-------------|----------|--------|
| **Visual brittleness** | VLAs fail under camera/lighting/background perturbations; WAMs are robust but ==4.8× slower== ([[2603.22078\|WAM-vs-VLA-Robustness]]) | Deployed robots break in new lighting conditions |
| **Spatial overfitting** | VLAs map object names to ==fixed training locations==, not abstract identities — only 9% on novel compositions ([[2505.03500\|TLI]]) | Cannot generalize to rearranged workspaces |
| **Stage hallucination** | VLAs report false progress based on superficial visual cues, not actual task completion ([[2511.16166\|EvoVLA]]) | Multi-step tasks silently fail partway through |
| **Detail-task ceiling** | Best VLA achieves ==only 24.9%== on detail-oriented manipulation tasks ([[2601.11421\|GM-100]]) | Precision tasks (assembly, tool-use) remain unsolved |
| **Data scaling plateau** | RT-1 required ==17 months of 13-robot data== for 76% unseen success; π0 needed 10,000+ hours ([[2212.06817\|RT-1]], [[2410.24164\|π0]]) | More data → diminishing returns without adaptation |

### Why More Data Is Not Enough

Two deeper structural problems emerge even with abundant data:

1. **World model over-optimism**: [[2602.12063|VLAW]] showed that world models trained only on successful demonstrations generate ==overly optimistic synthetic rollouts==, failing to predict failure modes. The world model must experience and learn from failures — which requires ongoing interaction, not just more training data.

2. **Catastrophic forgetting under task expansion**: Even with diverse pre-training, VLAs still lose capabilities when fine-tuned on new tasks. [[2603.03818|VLA-Continual-Learning]] found that ==experience replay is still required== to maintain past skills, and [[2505.23705|Knowledge-Insulation-VLA]] showed that gradient interference during fine-tuning actively degrades the VLM backbone's knowledge.

### The Self-Evolution Thesis

> [!tip] The Shift
> Instead of collecting more data, build systems that ==generate their own learning signal==. A self-evolving WAM can: (1) adapt at test time to novel physics, (2) bootstrap training data through imagination, (3) generate its own curriculum of increasing difficulty, and (4) protect past knowledge while acquiring new capabilities.

The evidence is already here: [[2502.05907|EvoAgent]] showed that a continual world model contributes ==72% of total performance gain==; [[2603.09030|PlayWorld]] achieved ==65% real-world improvement== through autonomous self-play; and [[2511.16166|EvoVLA]] demonstrated that self-evolution reduces stage hallucination by ==23.7 percentage points==.

---

## Starting Point: Pick Your Base WAM

> [!tip] Model-First Wins
> For embodied AI, ==start with a trained world model and add self-evolution== (not the other way around). A world model already has a robust latent space for generating synthetic future states — the challenge shifts to data quality within the model's own imagination. [[2502.05907|EvoAgent]] validated this: the continual world model contributed ==72% of total performance gains==.

| | [[2602.15922\|DreamZero]] | [[2602.10098\|VLA-JEPA]] | [[2603.19312\|LeWM]] |
|---|---|---|---|
| **Architecture** | 14B autoregressive diffusion transformer (DiT) | Latent-space predictive encoder (JEPA) | ==15M end-to-end JEPA== (ViT-Tiny encoder + Transformer predictor) |
| **How it models dynamics** | Flow-matching: jointly predicts video + continuous actions | Leakage-free state prediction in latent space, not raw pixels | SIGReg-stabilized latent prediction; no pixel generation |
| **Self-evolution signal** | Denoising / flow-matching loss spike on novel physics | JEPA alignment loss between target and student encoders | Prediction error + ==SIGReg divergence== on novel physics; VoE detects physical violations |
| **Strength** | Internet-scale visual dynamics, zero-shot generalization | Noise-invariant (ignores lighting/camera changes), cleaner latent space | ==Collapse-proof== (2-term loss only); 48× faster planning; single-GPU trainable |
| **Weakness** | Inference speed, massive compute for continuous fine-tuning | World model quality bounded by latent abstraction capacity | Struggles with high 3D visual complexity; no video generation capacity |

> [!tip] Three Models, Three Roles
> **DreamZero** = rich imagination (14B, video generation, internet-scale priors). **VLA-JEPA** = robust perception (leakage-free, noise-invariant, human video pretraining). **LeWM** = fast self-evolution (15M, collapse-proof, 48× planning speed). For a production self-evolving WAM, use DreamZero or VLA-JEPA as the primary Imaginer and ==LeWM as the fast Inner Loop planner== that adapts in real time.

---

## The Core Insight: Decouple Imaginer from Actor

> [!warning] Critical Architectural Boundary
> ==A self-evolving agent is not the same as a self-evolving world action model.== The world model's job is to predict and imagine future states; the agent's job is to execute actions. The agent itself does not need the capacity to imagine the future — it only needs to figure out how to act based on the world model's predictions.

**Coevolution does not mean merging their functions.** It means mathematically linking their loss functions so that an upgrade in the Imaginer immediately forces an upgrade in the Actor, and vice versa.

---

## Architecture: Three Nested Loops

The self-evolving WAM operates as three nested loops at different timescales, with continual learning as a cross-cutting concern:

```
┌─────────────────────────────────────────────────────────────┐
│  OUTER LOOP (weeks-months): Auto-Curriculum                 │
│  Generates increasingly difficult environments              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  MIDDLE LOOP (hours-days): Co-Evolution               │  │
│  │  Imaginer + Actor bootstrap each other                │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  INNER LOOP (milliseconds): Test-Time Adapt     │  │  │
│  │  │  Forward updates, no backprop, during inference │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ↕ Continual Learning (protects all three loops)
```

| Loop | Timescale | What Evolves | Key Mechanism | Papers |
|------|-----------|--------------|---------------|--------|
| **Inner** | ms–seconds | Deployed policy | Forward-update CEM, adaptive imagination depth | [[2506.23468\|NavMorph]], [[2602.08236\|AVIC]] |
| **Middle** | hours–days | World model + policy weights | Iterative co-improvement, curiosity-driven exploration | [[2602.12063\|VLAW]], [[2603.08403\|SPIRAL]], [[2502.05907\|EvoAgent]] |
| **Outer** | weeks–months | Environment complexity | Auto-curriculum, adversarial environment generation | [[1901.01753\|POET]], [[2502.05726\|ACCEL]] |

> [!tip] Why Three Loops?
> Prior work treats self-evolution as purely a training-time phenomenon (Middle Loop). But [[2506.23468|NavMorph]] showed 2.1x faster test-time adaptation via forward updates without backprop, and [[2602.08236|AVIC]] showed that deciding *when and how much* to imagine at test time dramatically improves efficiency. A production self-evolving WAM needs all three timescales.

---

## Inner Loop: Test-Time Self-Evolution

**Goal**: Adapt the deployed WAM to novel physics *during inference* without expensive retraining.

This is the most practical innovation missing from current WAM architectures. All existing self-evolving WAMs (EvoAgent, SPIRAL, PlayWorld) only evolve during training. But real-world deployment encounters distribution shifts constantly.

**Mechanism 1: Contextual Evolution Memory (from [[2506.23468|NavMorph]])**
- Maintain a lightweight memory bank of recent latent experiences
- When prediction error spikes (novel physics), retrieve similar past experiences and perform ==forward-update== (not backprop) to adapt world model parameters
- 2.1x faster than gradient-based adaptation; no catastrophic forgetting risk

**Mechanism 2: Adaptive Imagination Depth (from [[2602.08236|AVIC]])**
- Don't always imagine the same number of future steps
- Use prediction confidence to decide ==when and how much== to imagine
- High confidence → skip imagination, act directly (VLA-speed)
- Low confidence → deep imagination (WAM-quality)
- This bridges the speed-quality gap identified in [[2603.22078|WAM-vs-VLA-Robustness]]

**Mechanism 3: Fast-WAM Inference (from [[2603.16666|Fast-WAM]])**
- Use video generation objectives at ==training time only==
- At test time, deploy without video generation → VLA-speed inference
- The spatiotemporal priors are baked into the weights; you don't need to regenerate video at deployment

**Mechanism 4: Ultra-Fast Latent Planning (from [[2603.19312|LeWM]])**
- LeWM's CEM-based MPC plans ==48× faster== than foundation-model WMs (sub-second full planning cycle)
- 15M parameters with ==200× fewer tokens== than frozen-encoder JEPAs
- Trained with only 2 loss terms (prediction MSE + SIGReg) — no collapse risk during online adaptation
- VoE (Violation-of-Expectation) framework naturally detects when deployed physics diverge from training

> [!success] Inner Loop Recipe
> ==NavMorph CEM== for online adaptation + ==AVIC adaptive depth== for speed control + ==LeWM ultra-fast planning== for real-time CEM at 48× speed + ==Fast-WAM== fallback when imagination isn't needed.

---

## Middle Loop: Training-Time Co-Evolution

### Track 1 — Evolve the World Model (The Imaginer)

**Goal**: Continuously improve physics understanding without human labels.

**For DreamZero**: Track the denoising/flow-matching loss. When the robot encounters a new physical interaction, the loss spikes. Use this spike as an intrinsic learning signal to continuously fine-tune the DiT backbone.

**For VLA-JEPA**: Continuously train the target encoder against the student pathway using the JEPA alignment loss. As the robot experiences new environments, the world model updates its latent abstractions.

**For LeWM**: The ==SIGReg regularizer prevents representation collapse== during continuous fine-tuning — the primary risk for any JEPA updated repeatedly. Track the prediction MSE: spikes indicate novel physics. SIGReg's 2-term loss (vs. 6+ for other JEPAs) yields smooth, monotonic training curves even under distribution shift, making it the most stable option for self-evolution.

**Papers to borrow from:**

| Paper | What to Borrow | Why |
|-------|----------------|-----|
| [[2506.09985\|V-JEPA-2]] | Action-free pretraining → action-conditioned fine-tuning | Learn general physics from massive unlabeled datasets before conditioning on agent actions |
| [[2603.23376\|ABot-PhysWorld]] | ==Diffusion-DPO== for physics alignment | Explicitly suppress physically impossible predictions (object penetration, anti-gravity) |
| [[2409.18964\|PhysGen]] | Physics simulation pipeline | Infers physical parameters from video, simulates with rigid-body engine, refines with diffusion — provides grounding for physically plausible motion |
| [[2310.06114\|UniSim]] | Universal interactive simulation | Provides grounding for what physically plausible futures look like |
| [[2603.19312\|LeWM]] | ==SIGReg anti-collapse regularizer== | Prevents representation collapse during continuous JEPA fine-tuning; only 1 tunable hyperparameter |

### Track 2 — Evolve the Agent (The Actor)

**Goal**: Improve the policy using the world model's imagination as a training ground.

> [!warning] Gradients vs Evolution: When to Use Each
> The draft originally proposed "~50 evolutionary variants." But this is only appropriate for discovering ==novel behaviors== in unexplored action spaces. For refining known behaviors, gradient descent is faster and cheaper.

| Situation | Method | Why |
|-----------|--------|-----|
| Refining known manipulation skills | ==Gradient descent== (actor-critic in latent space, like DreamerV3) | Converges faster, less compute |
| Discovering novel action strategies | ==Population-based evolution== (5-10 variants, not 50) | Escapes local optima, finds unconventional solutions |
| Adapting to new embodiment | ==Knowledge insulation== ([[2505.23705\|Knowledge-Insulation-VLA]]) | Preserves backbone knowledge while adapting action head |
| Online deployment | ==Forward-update== (Inner Loop) | No training compute needed |

**The Actor-Critic Design (from [[2301.04104|DreamerV3]]):**
1. Actor takes compressed latent state from Imaginer
2. Critic evaluates expected return of imagined trajectories
3. Both train entirely in latent space — no real-world interaction needed during training
4. Continual learning (Track 4) protects against forgetting

### Track 3 — Wire the Curiosity-Driven Feedback Loop

**Goal**: Create an autonomous drive that pushes the Agent to seek the unknown, so the World Model can learn from what it finds.

**Core mechanism** (from [[2005.05960|Plan2Explore]]): Train a lightweight ensemble of $k$ dynamics networks. The intrinsic reward is ensemble disagreement:

$$R_{\text{intrinsic}} = \text{Var}\left(\hat{s}_{t+1}^{(1)}, \ldots, \hat{s}_{t+1}^{(k)}\right)$$

**The Loop:**
1. World Model calculates prediction error (how badly it predicted the future)
2. Error → intrinsic reward → given to Agent
3. Agent evolves to maximize this reward (actively seeks edge cases)
4. World Model observes novel states, trains on them, reduces error
5. Reward disappears → Agent must find the next unknown frontier
6. → GOTO 1

**Enhanced with semantic guidance (from [[2503.01584|SENSEI]]):**
- Pure prediction error causes the "noisy TV problem" — agent explores visual noise, not meaningful physics
- SENSEI uses a foundation model to provide ==semantic guidance== to curiosity
- Only reward exploration of *physically meaningful* novelty

**Enhanced with physics violation detection (from [[2603.19312|LeWM]]):**
- LeWM's ==VoE (Violation-of-Expectation) framework== measures "surprise" as prediction error on physically implausible events (teleportation, interpenetration)
- Higher surprise on physical violations vs. visual changes (color shifts) → the model distinguishes physics from appearance
- Use as a ==single-model curiosity signal== complementing Plan2Explore's ensemble approach — no ensemble overhead

> [!tip] Beyond Variance: Alternative Curiosity Signals
> When ensemble disagreement saturates (all models agree, even on wrong predictions), switch to:
> - **Empowerment** — mutual information $I(A; S')$ between actions and outcomes (correlates with human-like exploration)
> - **Causal curiosity** — reward for discovering *causal links* between actions and environmental changes
> - **RKHS skill disentanglement** — force different evolutionary branches to learn fundamentally distinct behaviors

### Track 4 — Stabilize with Continual Learning (Cross-Cutting)

**Goal**: Prevent catastrophic forgetting as both Imaginer and Actor continuously update.

> [!danger] The Synthetic Data Trap
> Because the agent trains inside the world model's "dreams," it relies on ==synthetic data for representation learning==. If the diffusion backbone hallucinates during continuous training, it introduces leakage, biases, and artifacts. The agent will learn to ==exploit generative artifacts (reward hacking)== rather than real-world dynamics, causing **policy collapse**.

**Concrete Validation Pipeline** (addressing Gap 3):

| Stage | Mechanism | Source |
|-------|-----------|--------|
| 1. Physics constraint check | ==Diffusion-DPO==: discriminator rejects physically impossible predictions | [[2603.23376\|ABot-PhysWorld]] |
| 2. CriticAgent scoring | Reflective agent scores dream quality via ==GRPO== | [[2603.08403\|SPIRAL]] (video generation domain; mechanism transfers to WAM) |
| 3. Real-world anchoring | Interleave real self-play data at ==decreasing ratios== (start 50%, decay to 5%) | [[2603.09030\|PlayWorld]] |
| 4. Replay buffer filtering | Entropy selection + real-synthetic similarity maximization | [[2411.13852\|ESRM]] |

**Memory Protection:**
- ==Latent Experience Replay Buffer==: store compressed latent trajectories of past successes
- ==Elastic Weight Consolidation (EWC)==: identify critical weights via Fisher information matrix, apply mathematical "spring" to protect them
- ==Task-Aware Prompt Gradient Projection==: project new gradients orthogonally to weights critical for past tasks

> [!tip] The VLA Surprise
> Two independent studies ([[2603.11653|VLA-RL-Continual-Learning]], [[2603.03818|VLA-Continual-Learning]]) found that VLAs pre-trained on diverse data are *naturally resistant* to catastrophic forgetting. Simple sequential fine-tuning works. This suggests WAMs with diverse pre-training may also resist forgetting more than expected — ==test this assumption empirically before adding complex CL mechanisms==.

---

## Middle Loop: Coevolution (The Core Innovation)

**Goal**: Mathematically link the loss functions of Imaginer and Actor so upgrades in one force upgrades in the other — without merging their distinct roles.

### The VLAW Mechanism (Empirically Validated)

[[2602.12063|VLAW]] demonstrated the only empirically validated co-evolution loop for VLA + world model. The mechanism is ==iterative alternation==, not joint optimization:

```
Round N:
  1. Actor generates trajectories in real environment
  2. World Model trains on Actor's trajectories (improves dynamics prediction)
  3. World Model generates synthetic rollouts
  4. Actor trains on synthetic rollouts (improves policy)
  → Repeat with improved models

Result: 39% improvement over non-co-evolved baseline
```

> [!warning] VLAW is Iterative, Not Joint
> The draft originally implied tightly coupled joint optimization. VLAW's actual mechanism is simpler: alternate between training phases. This is more stable and easier to implement than differentiable trust-region approaches.

### The Adaptive Difficulty Pattern (POET + ACCEL)

[[1901.01753|POET]] and [[2502.05726|ACCEL]] show a complementary pattern: the ==environment== co-evolves with the policy via unsupervised environment design. As the Actor improves, the environment generator creates harder challenges. Applied to WAMs:

1. The Imaginer generates scenarios ==just beyond the Actor's current skill level==
2. The Actor evolves to solve these scenarios
3. The Actor's new behaviors generate novel physics in the real world
4. The Imaginer updates to model these new dynamics
5. The Imaginer generates harder scenarios → GOTO 1

### Co-Evolving Critics (from [[2601.06794|ECHO]])

ECHO demonstrated that the ==critic must co-evolve with the policy== to avoid "stale feedback." As the Actor improves, its failure patterns shift — a frozen critic provides increasingly irrelevant feedback. ECHO's saturation-aware reward design ensures the critic adapts its diagnostic focus in lockstep with the Actor, achieving +7.28 points over standard GRPO. Applied to the WAM: the CriticAgent (Track 4) should be co-trained alongside the Actor, not frozen after initial training.

### Formalized Co-Evolution Framework

| Component | Loss Signal | How It Links |
|-----------|-------------|--------------|
| **Imaginer** | Prediction error on Actor's real trajectories | Actor's improving actions create harder prediction targets |
| **Actor** | Task success in Imaginer's dreams + curiosity reward | Imaginer's improving dreams provide higher-quality training signal |
| **Difficulty Controller** | Actor's success rate in current dreams | When success > 80%, increase difficulty; when < 20%, decrease |

> [!success] The Co-Evolution Recipe
> ==VLAW iterative alternation== (proven mechanism) + ==POET/ACCEL difficulty scaling== (adaptive curriculum) + ==SPIRAL CriticAgent== (quality gate) + ==ECHO critic co-evolution== (prevents stale feedback). The key insight: don't optimize jointly — alternate, and let a co-evolving critic gate data quality at each handoff.

### Borrowing from Self-Evolving Agents

Ideas that translate to WAMs:

| Agent Mechanism | WAM Translation | Source |
|-----------------|-----------------|--------|
| Self-rewarding (model judges own output) | Imaginer judges own prediction quality via consistency checks | [[2401.10020\|Self-Rewarding-LM]] |
| Zero-data self-play (model proposes + solves tasks) | Imaginer proposes novel physics scenarios, Actor solves them | [[2505.03335\|Absolute-Zero]] |
| Experience lifecycle (distill trajectories into principles) | Distill successful co-evolution rounds into "physics principles" stored in memory | [[2510.16079\|EVOLVER]] |
| Stage-aligned reward (different rewards per learning phase) | Different curiosity signals for exploration vs exploitation phases | [[2511.16166\|EvoVLA]] |
| Socratic self-debate (model debates itself) | Imaginer ensemble debates physics predictions; disagreement = learning signal | [[2509.24726\|Socratic-Zero]] |

---

## Outer Loop: Auto-Curriculum

**Goal**: If the model is in a static environment, it will eventually learn everything and stop evolving. The system must generate its own increasingly difficult environments.

**The POET-WAM Pattern:**

1. **Environment Generator** (secondary network) creates new physical scenarios
2. Scenarios are ==just beyond the Actor's current ability== (Goldilocks zone)
3. Actor attempts scenarios inside Imaginer's dreams
4. Success/failure feedback tunes the generator's difficulty level
5. Both Actor and Imaginer evolve on the harder scenarios
6. Generator increases difficulty → repeat

**Papers to borrow from:**

| Paper | What to Borrow |
|-------|----------------|
| [[1901.01753\|POET]] | Open-ended coevolution of environments and solutions |
| [[2502.05726\|ACCEL]] | Unsupervised Environment Design: evolve environment complexity via regret-based curation |
| [[2504.21024\|WebEvolver]] | Co-evolving agent + world model for synthetic training data |
| DriveDreamer-2 | LLM as scenario injector — generate diverse edge-case conditions |

> [!tip] From LLM Auto-Curriculum to Robotics
> [[2505.03335|Absolute-Zero]] showed models can propose their own tasks, solve them, and verify via code — with zero human data. The WAM equivalent: the Imaginer proposes novel physics scenarios (e.g., "what happens if this object is heavier?"), the Actor attempts them, and a physics engine verifies plausibility. This creates a fully autonomous curriculum.

---

## Convergence: When to Stop Evolving

> [!question] The Missing Criteria
> No existing self-evolving WAM paper addresses convergence. When has the system "learned enough"? When should self-evolution stop or slow down?

### Proposed Convergence Signals

| Signal | Measure | Threshold |
|--------|---------|-----------|
| **World model plateau** | Ensemble prediction disagreement → 0 across all explored states | Disagreement < ε for N consecutive rounds |
| **Curiosity saturation** | Intrinsic reward drops below task reward ratio | $R_{\text{intrinsic}} < 0.01 \times R_{\text{task}}$ |
| **Co-evolution diminishing returns** | One more Imaginer update improves Actor by < δ | Improvement < 1% per co-evolution round |
| **Environment exhaustion** | Auto-curriculum generator cannot produce scenarios that fail the Actor | Success rate > 95% on all generated scenarios |
| **Real-world validation** | Sim-to-real transfer gap stops shrinking | SimplerEnv correlation plateau |

> [!tip] Convergence ≠ Stopping
> Convergence signals should ==reduce evolution rate==, not stop it entirely. Switch from active exploration to maintenance mode: lower curiosity weight, increase replay ratio, decrease learning rate. The system stays ready to re-activate when encountering genuinely novel physics (loss spike → restart Inner Loop).

**Borrowing from LLM self-evolution:**
- [[2504.16084|TTRL]]: Majority-vote consensus as pseudo-reward — when all sampled rollouts agree, the model has converged on that scenario
- [[2412.01951|Sharpening-Mechanism]]: Formalizes self-improvement as "sharpening" — theoretical framework explaining when and why self-training converges

---

## Data & Simulation Strategy

> [!question] The Core Trade-Off
> A self-evolving WAM generates most of its training data through imagination (world model dreams). But ==dreams are only as good as the world model==. How do you bootstrap a system that must learn from its own imagination before that imagination is trustworthy?

### The Three Data Sources

| Source | Cost | Fidelity | Coverage | Role in Self-Evolution |
|--------|------|----------|----------|----------------------|
| **Real-world demonstrations** | Very high (teleoperation) | Ground truth | Limited to human scenarios | Bootstrap + periodic anchoring |
| **Simulation** | Medium (engineering) | Controllable but gapped | Unlimited procedural generation | Edge cases + domain randomization |
| **World model dreams** | Low (compute only) | Improves over time | Unbounded, self-directed | Primary training source after bootstrap |

### Phase 1: Bootstrap with Real Data

**Start small, start diverse.** The world model needs an initial grounding in real physics before it can dream reliably.

| Dataset | Scale | Why Use It |
|---------|-------|-----------|
| [[2310.08864\|OXE-/-RT-X]] | 1M+ trajectories, 22 embodiments | Cross-embodiment foundation; positive transfer across platforms |
| [[2405.12213\|Octo]] | 800K trajectories (OXE subset) | Proven generalist baseline; ~100 in-domain demos for fine-tuning |
| [[2307.00595\|RH20T]] | 110K+ sequences, 147 tasks | Multi-modal (RGB, depth, tactile, force-torque, audio) — critical for contact-rich world modeling |
| [[2412.13877\|RoboMIND]] | 107K trajectories, 479 tasks | ==5,000 failure demonstrations with documented causes== — failure data is essential for honest world models |

> [!warning] Failure Data Is Non-Negotiable
> [[2602.12063|VLAW]] showed world models trained only on successes generate ==overly optimistic rollouts==. [[2603.09030|PlayWorld]] demonstrated that autonomous play captures diverse failure modes (missed grasps, slips) that human-collected data misses. Budget ==at least 5% of training data as explicit failure demonstrations==.

### Phase 2: Simulation for Edge Cases

Pure real-world data cannot cover the long tail of physical interactions. Simulation fills three roles: (1) procedural generation of scenarios impossible to stage in reality, (2) domain randomization for robustness, and (3) cheap evaluation via sim-to-real correlation.

**Simulation Stack:**

| Component | Recommended | Why |
|-----------|------------|-----|
| **Physics engine** | MuJoCo (contact accuracy) + PhysX (parallel scale) | MuJoCo for contact-rich fidelity; PhysX via Isaac for GPU-parallel training |
| **Task generation** | [[2406.02523\|RoboCasa]] (procedural kitchens) + [[2603.16861\|MolmoBot]] (1.8M procedural trajectories) | RoboCasa's LLM-generated composite tasks + MolmoBot's proof that ==sim-only training enables 79.2% real-world zero-shot transfer== |
| **Robustness eval** | [[2405.05941\|SimplerEnv]] (r > 0.85 sim-real correlation) | Cheap policy ranking without hardware; validates world model fidelity |
| **Domain randomization** | 5-dimension approach from RoboTwin 2.0 | Camera, lighting, background, height, language — systematic coverage |

**When is simulation enough?**

| Scenario | Simulation Alone? | Why |
|----------|-------------------|-----|
| Rigid-body pick-and-place | ==Yes== — MolmoBot achieved 79.2% real-world zero-shot | Rigid dynamics are well-modeled; domain randomization bridges the visual gap |
| Contact-rich insertion/assembly | ==No== — FurnitureBench shows 0-20% SOTA on insertion | Contact dynamics are hard to simulate; real tactile data needed for calibration |
| Deformable objects (cloth, rope) | ==No== — Simulation physics diverge significantly | Deformable simulation is inaccurate; need real demonstrations + sim-to-real adaptation |
| Navigation in structured environments | ==Yes== — [[2506.23468\|NavMorph]] + sim-to-real works | Environmental layout is easy to simulate; visual domain randomization sufficient |
| Long-horizon multi-stage tasks | ==Partially== — sim for sub-skills, real for integration | Sub-skills transfer well; full-chain requires real-world sequential execution |
| Novel object manipulation | ==No== — [[2505.03500\|TLI]] showed spatial overfitting at 9% | Novel objects need real visual diversity; simulation can't capture all material properties |

### Phase 3: World Model Dreams (The Self-Evolving Source)

Once the world model is bootstrapped on real + sim data, it becomes the ==primary data source== for the Middle Loop. This is where self-evolution happens.

**The Dream Quality Ladder:**

| Stage | Data Mix | World Model Quality | When to Advance |
|-------|----------|-------------------|-----------------|
| **1. Bootstrap** | 80% real + 20% sim | Untrained — dreams are noise | After initial training (FVD < 300) |
| **2. Grounding** | 50% real + 30% sim + 20% dreams | Basic physics — dreams are plausible | FVD < 150 and real-world anchoring passes |
| **3. Co-evolution** | 20% real + 10% sim + 70% dreams | Good physics — dreams drive improvement | VLAW-style loop shows positive gain per round |
| **4. Autonomous** | 5% real + 5% sim + 90% dreams | Strong physics — dreams are trustworthy | SimplerEnv correlation > 0.85 |

> [!success] The Data Strategy Recipe
> ==Real data for bootstrap== (OXE + RH20T + failure demos) → ==Simulation for edge cases== (MuJoCo contact-rich + RoboCasa procedural) → ==World model dreams as primary source== (VLAW co-evolution loop with PlayWorld self-play). Decay real data ratio from 80% → 5% as world model improves, validated by [[2405.05941\|SimplerEnv]] correlation.

### Phase 4: Handling Edge Cases

Edge cases are where self-evolving WAMs differentiate from static models — the system must ==actively seek and learn from its own failure modes==.

**Contact-Rich Tasks (Insertion, Assembly, Tool Use):**
- Simulation alone is insufficient — contact dynamics are hard to model accurately
- [[2505.22159|ForceVLA]] showed integrating 6-axis force feedback improves contact-rich tasks by ==23.2%==; force sensing is not optional
- Strategy: Use simulation for coarse policy learning, then ==real-world fine-tuning with force/tactile feedback== (as in [[2307.00595|RH20T]])

**Deformable Objects (Cloth, Rope, Soft Bodies):**
- Current physics engines poorly model deformable dynamics
- Strategy: ==Separate dynamics module== for deformable objects, trained primarily on real demonstrations
- The world model should learn to ==detect deformable objects and switch prediction modes==

**Precision Tasks (<1mm tolerance):**
- Current VLAs achieve only 24.9% on detail-oriented tasks ([[2601.11421|GM-100]])
- Strategy: High control frequency (>30Hz) + ==task-specific action heads== with continuous flow-matching outputs (not discrete tokens)
- World model must predict at sub-millimeter spatial resolution for these scenarios

**Out-of-Distribution Environments:**
- Camera/lighting/background shifts cause >65% performance drops ([[2603.22078|WAM-vs-VLA-Robustness]])
- Strategy: The ==Outer Loop auto-curriculum== should explicitly generate visual perturbations as training scenarios
- Domain randomization in simulation covers known perturbation axes; the world model handles novel ones through test-time adaptation (Inner Loop)

> [!tip] The Edge Case Discovery Loop
> The curiosity mechanism (Track 3, Middle Loop) naturally pushes the Actor toward edge cases — high prediction error = high intrinsic reward. But curiosity alone finds *interesting* states, not necessarily *useful* states. Augment with:
> 1. ==Failure replay== — explicitly re-train on past failures at 3× weight
> 2. ==Task-conditioned adversarial generation== — the Outer Loop generates scenarios targeting known weakness categories (contact-rich, deformable, precision)
> 3. ==SimplerEnv diagnostic layer== — periodically evaluate on perturbation benchmarks to detect regression

### Summary: What Data You Need

| Data Type | Source | Scale Target | Purpose |
|-----------|--------|-------------|---------|
| Real demonstrations | Teleoperation (GELLO-style) | 50K-100K trajectories | Bootstrap + periodic anchoring |
| Real failures | Autonomous play ([[2603.09030\|PlayWorld]]) | 5-10% of total | World model honesty |
| Sim rigid-body | MuJoCo + domain randomization | 1M+ (procedural) | Policy pre-training + edge cases |
| Sim procedural tasks | [[2406.02523\|RoboCasa]] + LLM generation | 100K+ (procedural) | Long-horizon composition |
| World model dreams | VLAW co-evolution loop | Unbounded (primary source) | Self-evolving improvement |
| Multi-modal (force, tactile) | Real sensors ([[2307.00595\|RH20T]]) | 10-20% of real data | Contact-rich task fidelity |

---

## The Complete Self-Evolving Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│  OUTER LOOP: Auto-Curriculum (ECHO + POET)                   │
│  Generates harder environments when Actor succeeds           │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  MIDDLE LOOP: Co-Evolution (VLAW + SPIRAL)             │  │
│  │                                                        │  │
│  │  ┌──────────────┐    prediction    ┌──────────────┐    │  │
│  │  │  World Model │ ── error ──────▶ │  Intrinsic   │    │  │
│  │  │  (Imaginer)  │                  │   Reward     │    │  │
│  │  └──────┬───────┘                  └──────┬───────┘    │  │
│  │         │                                 │            │  │
│  │    generates                        drives actor       │  │
│  │      dreams                         evolution          │  │
│  │         │                                 │            │  │
│  │         ▼                                 ▼            │  │
│  │  ┌──────────────┐   gradient/evo   ┌────────────┐      │  │
│  │  │    Agent     │◀───────────────-─│  Actor-    │      │  │
│  │  │   (Actor)    │                  │  Critic    │      │  │
│  │  └──────┬───────┘                  └────────────┘      │  │
│  │         │                                              │  │
│  │    finds edge cases ──▶ Imaginer trains on them        │  │
│  │                                                        │  │
│  │  ┌────────────────────────────────────────────────┐    │  │
│  │  │  INNER LOOP: Test-Time Adaptation              │    │  │
│  │  │  NavMorph CEM + AVIC adaptive depth            │    │  │
│  │  │  (forward updates, no backprop, during deploy) │    │  │
│  │  └────────────────────────────────────────────────┘    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  CONTINUAL LEARNING (cross-cutting)                    │  │
│  │  Replay Buffer + EWC + Synthetic Data Validation       │  │
│  │  (ABot-PhysWorld DPO + SPIRAL CriticAgent + PlayWorld) │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  CONVERGENCE MONITOR                                   │  │
│  │  Prediction plateau + Curiosity saturation +           │  │
│  │  Co-evolution gain ratio → reduce evolution rate       │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Safety: Misevolution Risks

> [!danger] Misevolution
> As agents become capable of autonomous evolution, they present novel risks. Misevolution is the phenomenon where an agent's self-evolution deviates in unintended or harmful ways.

| Pathway | Emergent Risk | Mitigation |
|---------|---------------|------------|
| **Model** | Degradation of safety alignment | CriticAgent (SPIRAL) gates all training data |
| **Memory** | Biased knowledge accumulation | Replay buffer diversity constraints |
| **Synthetic** | Hallucinated physics → reward hacking | Diffusion-DPO (ABot-PhysWorld) + real-world anchoring |
| **Convergence** | Premature convergence to local optima | Multi-signal convergence monitor (not single metric) |

---

## Key Papers Reference Table

### Self-Evolving WAMs

| Paper | Key Contribution |
|-------|-----------------|
| [[2603.09030\|PlayWorld]] | Autonomous self-play data → world model; 65% real-world improvement |
| [[2603.08403\|SPIRAL]] | Think-act-reflect + GRPO; CriticAgent for quality gating (video generation domain; mechanism transfers) |
| [[2502.05907\|EvoAgent]] | Continual world model = 72% of total gain; curriculum learning |
| [[2506.23468\|NavMorph]] | Test-time CEM; 2.1x faster than gradient-based adaptation |
| [[2602.12063\|VLAW]] | Iterative co-improvement loop; 39% improvement |

### Self-Evolving Agents (Ideas to Borrow)

| Paper | Borrowable Insight |
|-------|-------------------|
| [[2505.03335\|Absolute-Zero]] | Zero-data self-play: propose + solve + verify with no human data |
| [[2504.16084\|TTRL]] | Majority-vote consensus as pseudo-reward for RL self-improvement |
| [[2601.06794\|ECHO]] | Policy + critic co-evolve; saturation-aware reward prevents stale feedback |
| [[2510.16079\|EVOLVER]] | Distill trajectories into strategic principles |
| [[2401.10020\|Self-Rewarding-LM]] | Model judges own output quality |
| [[2509.24726\|Socratic-Zero]] | Data-free self-debate for reasoning improvement |
| [[2511.16166\|EvoVLA]] | Stage-aligned reward + long-horizon memory |

### Continual Learning & Safety

| Paper | Role |
|-------|------|
| [[2603.11653\|VLA-RL-Continual-Learning]] | VLAs naturally resist forgetting under sequential fine-tuning |
| [[2603.03818\|VLA-Continual-Learning]] | Confirms forgetting resistance; simple methods suffice |
| [[2603.23376\|ABot-PhysWorld]] | Diffusion-DPO for physics-aligned generation |
| [[2602.08236\|AVIC]] | Adaptive imagination: when and how much to imagine |
| [[2603.16666\|Fast-WAM]] | Training-time video, test-time speed |

### Foundational

| Paper | Role |
|-------|------|
| [[1803.10122\|World-Models]] | Encoder + dynamics + controller architecture (Ha & Schmidhuber) |
| [[2301.04104\|DreamerV3]] | Actor-critic in latent space; fixed hyperparameters across 150+ tasks |
| [[2005.05960\|Plan2Explore]] | Ensemble disagreement as curiosity signal |
| [[2412.01951\|Sharpening-Mechanism]] | Formalizes when and why self-training converges |
| [[1901.01753\|POET]] | Open-ended coevolution of environments + solutions |
| [[2603.19312\|LeWM]] | Stable end-to-end JEPA; SIGReg prevents collapse; 48× faster planning; single-GPU; VoE for physics understanding |
| [[1612.00796\|EWC]] | Elastic Weight Consolidation; protect critical weights via Fisher information |
| [[1705.05363\|ICM]] | Intrinsic Curiosity Module; prediction error as intrinsic reward |
| [[1810.12894\|RND]] | Random Network Distillation; scalable curiosity alternative |

### Curriculum & Environment Design

| Paper | Role |
|-------|------|
| [[2502.05726\|ACCEL]] | Unsupervised Environment Design for curriculum generation |
| [[2503.01584\|SENSEI]] | Semantic curiosity guidance via foundation models |
| [[2403.06845\|DriveDreamer-2]] | LLM as scenario injector for world model imagination |

### Continual Learning & Data Quality

| Paper | Role |
|-------|------|
| [[2603.11653\|VLA-RL-Continual-Learning]] | VLAs naturally resist forgetting under sequential fine-tuning |
| [[2603.03818\|VLA-Continual-Learning]] | Confirms forgetting resistance; simple methods suffice |
| [[2305.13622\|SER]] | Strong Experience Replay; uses current data as "future experiences" via forward consistency loss |
| [[2112.15402\|RER]] | Relational Experience Replay; bi-level stability-plasticity |
| [[2411.13852\|ESRM]] | Entropy selection + similarity maximization for synthetic data quality in online CL |
| [[2211.15944\|Continual-Dreamer]] | World models for continual RL; persistent replay + task-agnostic exploration |
| [[2603.23376\|ABot-PhysWorld]] | Diffusion-DPO for physics-aligned generation |
| [[2602.08236\|AVIC]] | Adaptive imagination: when and how much to imagine |
| [[2603.16666\|Fast-WAM]] | Training-time video, test-time speed |

### Motivation (Why Self-Evolution)

| Paper | What It Shows |
|-------|--------------|
| [[2603.22078\|WAM-vs-VLA-Robustness]] | VLAs brittle to perturbations; WAMs robust but 4.8× slower — static models face speed-quality tradeoff |
| [[2505.03500\|TLI]] | VLAs spatially overfit: 9% on novel compositions → 83% with latent intervention |
| [[2511.16166\|EvoVLA]] | Stage hallucination + fragile memory in long-horizon tasks; self-evolution reduces hallucination by 23.7pp |
| [[2601.11421\|GM-100]] | Best VLA achieves only 24.9% on detail-oriented tasks |
| [[2212.06817\|RT-1]] | 17 months of 13-robot data → 76% on unseen tasks; data scaling plateaus |
| [[2505.23705\|Knowledge-Insulation-VLA]] | Gradient interference degrades VLM knowledge during fine-tuning |

### Data & Simulation

| Paper | Role |
|-------|------|
| [[2310.08864\|OXE-/-RT-X]] | 1M+ cross-embodiment trajectories; foundation dataset for VLA pre-training |
| [[2405.12213\|Octo]] | Generalist robot policy on OXE; ~100 in-domain demos for fine-tuning |
| [[2307.00595\|RH20T]] | 110K multi-modal sequences (RGB, depth, tactile, force-torque); contact-rich grounding |
| [[2412.13877\|RoboMIND]] | 107K trajectories with 5,000 failure demos + frame-level language annotations |
| [[2406.02523\|RoboCasa]] | 120 kitchen scenes, LLM-generated composite tasks; procedural data generation |
| [[2603.16861\|MolmoBot]] | 1.8M sim trajectories; 79.2% real-world zero-shot via domain randomization |
| [[2405.05941\|SimplerEnv]] | r > 0.85 sim-to-real correlation; cheap policy ranking without hardware |
| [[2505.22159\|ForceVLA]] | Force-aware MoE for contact-rich tasks; +23.2% with 6-axis force feedback |
| [[2310.06114\|UniSim]] | Universal simulator via video diffusion; zero-shot sim-to-real transfer |

---

*See [[16_Self-Evolving-VLA-WAM]] for conceptual foundations, [[06_WAM]] for the WAM landscape, and [[04_VLA]] for VLA design principles.*
