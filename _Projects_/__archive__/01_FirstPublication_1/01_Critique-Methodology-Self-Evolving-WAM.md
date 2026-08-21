---
title: "Methodology Critique: Why the Proposed Methods Can't Build a Self-Evolving WAM"
tags:
  - self-evolving
  - WAM
  - critique
  - robotics
  - methodology
aliases:
  - WAM Methodology Critique
  - Self-Evolving WAM Methodology Failure
---

# Methodology Critique: Why the Proposed Methods Can't Build a Self-Evolving WAM

> [!abstract] Purpose
> A structural analysis of [[00_How-to-Build-Self-Evolving-WAM|the Self-Evolving WAM Blueprint]], arguing that even if every cited paper's results transferred perfectly to manipulation, the proposed methodology still cannot produce a self-evolving WAM. This critique targets the mechanisms themselves, not domain transfer gaps.
>
> See also: [[01_Critique-Self-Evolving-WAM]] for the domain transfer and miscitation critique.

> [!info] Methodology
> Every claim below has been verified against the corresponding `_KnowledgeHub_` note. The critique assumes the *best case* for every component — full domain transfer, unlimited compute, perfect implementation — and shows that the architecture still breaks at the methodology level.

---

## Part I: Why the Inner Loop Breaks

The Inner Loop proposes four mechanisms for test-time self-evolution: NavMorph CEM (forward-update memory), AVIC adaptive depth, Fast-WAM inference, and LeWM ultra-fast planning. These mechanisms are internally contradictory.

### 1.1 Fast-WAM Contradicts Test-Time Adaptation

> [!danger] The Inner Loop's two core mechanisms are architecturally incompatible.

[[2603.16666|Fast-WAM]]'s key insight, verified from the paper: the video generation branch is ==entirely removed at inference==. The spatiotemporal priors are baked into weights during training. This yields 4x faster inference (190ms vs. 810ms).

But the Inner Loop's entire purpose is ==test-time adaptation== — adapting the deployed WAM to novel physics *during inference*. NavMorph CEM adapts by retrieving past latent experiences and performing forward updates. This requires the world model to ==generate and compare imagined futures== with reality.

If Fast-WAM removes the generation capacity at test time, the world model cannot:

1. Generate dream rollouts for the Actor to adapt to
2. Compare predicted vs. observed futures (the self-evolution signal)
3. Provide the prediction error spike that triggers CEM adaptation

The blueprint's Inner Loop Recipe says: "NavMorph CEM for online adaptation + ... ==Fast-WAM fallback when imagination isn't needed==." But the recipe is backwards: ==adaptation IS imagination==. When imagination isn't needed, adaptation isn't happening — and the system is not self-evolving, just a static VLA running fast.

**The blueprint wants test-time adaptation AND test-time speed. Fast-WAM showed these are a tradeoff, not a combination.**

### 1.2 Forward-Update Can Only Interpolate, Not Extrapolate

[[2506.23468|NavMorph]]'s Contextual Evolution Memory works by storing latent experiences and retrieving ==similar== past experiences when prediction error spikes.

This has a fundamental limitation for self-evolution: it can only adapt to situations that ==resemble ones already seen==. The retrieval mechanism finds nearest neighbors in latent space. If the robot encounters genuinely novel physics (which is the entire point of self-evolution), the memory bank has no similar experiences to retrieve.

- NavMorph demonstrated this in VLN-CE navigation, where "novel environments" means ==new arrangements of familiar rooms== (Matterport3D scans). The physics (walking, collision) are identical — only the visual layout changes.
- For manipulation, "novel physics" means new contact dynamics, new material properties, new object geometries. These change the ==dynamics model itself==, not just the visual observations. Retrieving a "similar" past experience doesn't help because the physics have changed.

**Forward-update without backprop can adapt representations (what the model sees). It cannot adapt dynamics (what the model predicts will happen).**

### 1.3 The Adaptive Depth Gatekeeper Is Circular

[[2602.08236|AVIC]]'s policy model acts as a gatekeeper, deciding when and how much to imagine. But training this gatekeeper requires knowing ==which situations benefit from deeper imagination== — which you can only learn by ==trying different imagination depths in those situations first==.

The gatekeeper needs:

1. Training data mapping situations → optimal imagination depth
2. A reward signal for correct depth decisions
3. Its own training loop (separate from the Actor and Imaginer)

The blueprint proposes this as a solved component ("AVIC adaptive depth for speed control") but never addresses how the gatekeeper is trained, what data it uses, or how it adapts as the Imaginer improves. As the Imaginer gets better, situations that previously needed deep imagination may no longer need it — the gatekeeper must co-evolve with the Imaginer, creating a fourth co-evolution target the blueprint doesn't account for.

### 1.4 LeWM's CEM Planning Doesn't Scale to the Proposed Imaginer

[[2603.19312|LeWM]]'s Cross-Entropy Method MPC works by sampling action sequences, forward-simulating through the world model, scoring outcomes, and resampling. This requires many forward passes per planning step.

CEM typically requires ~1000 samples per iteration, ~3-5 iterations per planning step, and a planning horizon of ~10 steps. This means ==30,000-50,000 forward passes of the world model per action==.

For LeWM's 15M ViT-Tiny on Push-T, this is fast. For [[2602.15922|DreamZero]]'s 14B DiT (the blueprint's proposed Imaginer), each forward pass takes ~150ms even with Flash optimization. At 50,000 forward passes:

$$50{,}000 \times 150\text{ms} = 7{,}500\text{s} \approx 2\text{ hours per action}$$

This is why LeWM achieves "48x faster planning" — it's fast because the ==model is tiny==, not because CEM is efficient. The 48x speedup is relative to other methods on the ==same small model==. Replacing LeWM with DreamZero in the CEM loop would be 1000x slower than LeWM, not 48x faster than anything.

The blueprint suggests using "LeWM as the fast Inner Loop planner" alongside DreamZero as the Imaginer. But if LeWM is the planner, it uses ==LeWM's own world model== for planning — not DreamZero's. The Actor would then be optimizing actions based on a ==15M model's predictions== while the Imaginer generates dreams with a ==14B model's dynamics==. These two models predict different futures for the same actions.

---

## Part II: Why the Middle Loop Breaks

### 2.1 The Co-Evolution Chasing Problem

[[2602.12063|VLAW]]'s iterative alternation:

```
Round N:
  Actor generates real trajectories (using current policy πₙ)
  → World Model trains on πₙ's trajectories
  → World Model generates dreams (based on πₙ's behavior)
  → Actor trains on dreams → becomes πₙ₊₁

Round N+1:
  Actor generates real trajectories (using πₙ₊₁ — DIFFERENT from πₙ)
  → World Model trains on πₙ₊₁'s trajectories
  → But World Model was previously trained on πₙ's data...
```

The World Model is always one step behind the Actor. In Round N+1, the World Model must predict consequences of $\pi_{n+1}$'s actions, but it was trained on $\pi_n$'s trajectories. As the gap between $\pi_n$ and $\pi_{n+1}$ accumulates across rounds, the World Model increasingly models a ==policy that no longer exists==.

VLAW showed this works for a bounded number of rounds (success rate 0.46 → 0.868). But the blueprint proposes ==indefinite co-evolution==. Two outcomes are possible:

1. **Convergence**: The Actor stops changing, the World Model catches up, both stabilize. But then self-evolution has stopped — the system is static again.
2. **Divergence**: The gap between Actor and World Model grows, dreams become increasingly misaligned with real behavior, dream-trained Actor degrades.

There is no regime where the system both ==keeps evolving indefinitely== AND ==maintains alignment between Actor and World Model==. VLAW's bounded improvement demonstrates (1), not open-ended self-evolution.

### 2.2 The Curiosity Ensemble Is Computationally Intractable

[[2005.05960|Plan2Explore]]'s curiosity signal uses an ensemble of $k$ dynamics networks:

$$R_{\text{intrinsic}} = \text{Var}\left(\hat{s}_{t+1}^{(1)}, \ldots, \hat{s}_{t+1}^{(k)}\right)$$

Plan2Explore used this with ==Dreamer's RSSM== (a compact recurrent world model, ~10-50M parameters). The blueprint proposes applying this to a 14B DreamZero.

Maintaining an ensemble of $k = 5$ copies of a 14B model requires ==70B parameters==. Even $k = 2$ is 28B. The ensemble must all perform forward passes on every observation to compute disagreement.

Alternatives exist (single-model uncertainty estimation, dropout-based approximations), but Plan2Explore's specific mechanism — the one the blueprint's equations reference — requires a literal ensemble. The blueprint inherits Plan2Explore's formulation without addressing its compute implications at the proposed scale.

### 2.3 The Noisy TV "Solution" Creates a Static Dependency

The blueprint acknowledges the noisy TV problem (curiosity agent explores visual noise) and proposes [[2503.01584|SENSEI]]'s semantic guidance: a foundation model filters exploration for "physically meaningful" novelty.

This creates a new problem: ==the semantic filter is static==. The foundation model has its own training distribution and its own biases about what counts as "meaningful." As the WAM evolves and encounters increasingly exotic scenarios, the static foundation model may:

1. Reject genuinely novel physics as "noise" (false negatives — missed learning opportunities)
2. Accept familiar-looking but physics-violating scenarios as "meaningful" (false positives — wrong learning signals)

The blueprint's curiosity system now depends on a ==frozen external oracle== to decide what's worth exploring. This oracle doesn't co-evolve — it's a fixed bottleneck on the system's ability to discover genuinely novel phenomena.

### 2.4 The Three CL Mechanisms Conflict

The blueprint proposes three simultaneous continual learning mechanisms:

| Mechanism | What It Does | Gradient Effect |
| --------- | ------------ | --------------- |
| **EWC** ([[1612.00796\|EWC]]) | Penalizes changes to weights important for past tasks (Fisher information) | ==Resists change== to critical weights |
| **Latent Experience Replay** | Replays compressed past trajectories | Pushes toward ==past data distribution== |
| **Task-Aware Gradient Projection** | Projects new gradients orthogonally to past-critical weight directions | ==Constrains direction== of change |

These mechanisms interfere:

- EWC says "don't change weight $w_i$" (via quadratic penalty). Gradient Projection says "change $w_i$, but only in directions orthogonal to past tasks." If the orthogonal subspace for $w_i$ is empty (all directions are important for some past task), the system is ==frozen== — it can never learn anything new.
- Experience Replay pushes the model toward past data distributions. The Middle Loop pushes it toward ==novel== distributions via curiosity. These are opposing gradients. The net effect depends on the replay ratio, which the blueprint sets at "start 50%, decay to 5%" — but the decay schedule is arbitrary, not derived from any principle.
- All three mechanisms add ==regularization penalties== to the loss function. Combined, they may over-regularize, preventing the plasticity needed for self-evolution. The entire self-evolution thesis requires the model to ==change== — but CL mechanisms exist to ==prevent change==.

**And the strongest evidence from the blueprint's own sources suggests none of this is necessary:** [[2603.11653|VLA-RL-Continual-Learning]] showed that simple Sequential Fine-Tuning with LoRA achieves ==less than 2% forgetting==, and [[2603.03818|VLA-Continual-Learning]] found VLAs need only ==2% replay buffer== for near-zero forgetting. Both suggest the complex CL machinery solves a problem that may not exist for pretrained models.

### 2.5 The Imaginer-Actor Decoupling Creates a Representation Mismatch

> [!warning] The "Critical Architectural Boundary"
> The blueprint insists: "the world model's job is to predict and imagine future states; the agent's job is to execute actions."

This decoupling is clean in theory. In practice, it means the Actor receives ==compressed latent states from the Imaginer==. The Actor-Critic Design (from [[2301.04104|DreamerV3]]) trains both actor and critic "entirely in latent space."

But [[2505.23705|Knowledge-Insulation-VLA]] discovered that gradient flow between action modules and the VLM backbone ==degrades the backbone's knowledge==. They had to ==stop gradients== from the action expert to prevent corruption.

If the Actor-Critic trains in the Imaginer's latent space, critic gradients flow through the Imaginer's representations. The same gradient interference that Knowledge Insulation VLA documented will corrupt the Imaginer's physics understanding. The blueprint proposes "mathematically linking their loss functions so that an upgrade in the Imaginer immediately forces an upgrade in the Actor, and vice versa" — but Knowledge Insulation showed that linked gradients between action and perception modules are precisely what causes degradation.

**You cannot simultaneously decouple them (for clean architecture) and couple their loss functions (for co-evolution). These are contradictory requirements.**

---

## Part III: Why the Outer Loop Breaks

### 3.1 Manipulation Difficulty Is Non-Monotonic

[[1901.01753|POET]] and [[2502.05726|ACCEL]] generate environments along smooth difficulty gradients. POET mutates terrain parameters (stump height, gap width) continuously. The Goldilocks zone ("just beyond the Actor's current ability") assumes a ==monotonic relationship== between parameter values and difficulty.

In manipulation, difficulty has ==cliff edges==:

| Parameter | Below Threshold | Above Threshold |
| --------- | --------------- | --------------- |
| Object mass | Trivial grasp | Exceeds gripper force limit → impossible |
| Friction coefficient | Stable grasp | Object slides → fundamentally different strategy needed |
| Object size | Normal manipulation | Below gripper minimum → task is physically impossible |
| Compliance | Rigid-body physics | Deformable physics → different dynamics model |

A small parameter mutation can cause a ==discontinuous jump== from "solvable" to "impossible" or from "one strategy works" to "completely different strategy needed." The Goldilocks zone doesn't exist as a continuous band — it's a ==fractal boundary== in high-dimensional parameter space.

The blueprint's difficulty controller uses a simple threshold: "When success > 80%, increase difficulty; when < 20%, decrease." But manipulation difficulty is ==multi-dimensional==: a task can be easy in reach but hard in grasp. Which dimension should the controller increase? The scalar threshold collapses a multi-dimensional difficulty landscape into a single number.

### 3.2 The Environment Generator Can't Generate What It Doesn't Know

The Outer Loop requires generating environments "just beyond the Actor's current ability." But the environment generator is itself a learned or programmed system. It can only generate environments within ==its own parameterization space==.

- POET parameterizes environments with ~5 terrain features. It generates novel combinations of known features.
- For manipulation, the space of possible environments includes object geometries, material properties, tool shapes, articulated objects, deformable bodies, fluids, granular materials. Parameterizing this space requires ==a complete physics simulator== — which is itself the sim-to-real problem.

The generator cannot generate scenarios involving physics it doesn't model. If the system has never encountered cloth, the generator cannot create cloth-manipulation challenges. The Outer Loop can only generate ==recombinations of known scenarios==, not genuinely novel physics.

**Self-evolution requires encountering the unknown. But the Outer Loop can only generate the known in new arrangements.**

---

## Part IV: Why the Three Loops Can't Be Nested

### 4.1 Timescale Conflicts

The blueprint assigns:

| Loop | Timescale |
| ---- | --------- |
| Inner | milliseconds–seconds |
| Middle | hours–days |
| Outer | weeks–months |

The Inner Loop adapts at test time. The Middle Loop trains at training time. But the blueprint proposes running all three simultaneously in a deployed system. This creates conflicts:

- The Inner Loop's forward-updates modify world model representations in ==milliseconds==. The Middle Loop's backprop training updates world model weights over ==hours==. These two update mechanisms operate on the ==same model parameters== at incompatible timescales.
- When the Middle Loop performs a weight update (hours of gradient descent), it overwrites whatever adaptations the Inner Loop made (milliseconds of forward updates). The Inner Loop's work is destroyed every time the Middle Loop trains.
- When the Outer Loop generates a new, harder environment (weeks of curriculum evolution), both Inner and Middle Loops must restart their adaptation from scratch on the new environment. But the Middle Loop was in the middle of co-evolution on the old environment.

There is no mechanism for ==synchronizing== these timescales. The blueprint draws nested boxes but never specifies how the Inner Loop's forward-updates interact with the Middle Loop's gradient updates on the same weights.

### 4.2 The Inner Loop Undermines the Middle Loop's Training Distribution

The Middle Loop's co-evolution ([[2602.12063|VLAW]]) requires the Actor to generate ==real trajectories== that the World Model trains on. But the Inner Loop adapts the Actor at test time before these trajectories are recorded.

This means the Middle Loop sees trajectories from an ==Inner-Loop-adapted Actor==, not the base Actor. The World Model learns to predict consequences of an adapted policy — but the adaptation is ephemeral (it was a forward-update, not a weight change). In the next deployment, the Inner Loop may adapt differently, and the World Model's predictions are wrong again.

The Inner Loop's test-time adaptation ==corrupts the training signal== for the Middle Loop's co-evolution.

### 4.3 Internal Inconsistency in the Blueprint

The blueprint's complete pipeline diagram (lines 473-514) labels the Outer Loop as:

> "OUTER LOOP: Auto-Curriculum (==ECHO + POET==)"

But [[2601.06794|ECHO]] is about ==critic co-evolution== (co-evolving the critic alongside the policy), which the blueprint's own text places in the ==Middle Loop== (lines 280-282: "Co-Evolving Critics (from ECHO)"). ECHO doesn't generate environments — it adapts the critic's reward signal.

The same mechanism is assigned to two different loops with different timescales. This is not just a labeling error — it reflects confusion about what ECHO actually does in the architecture.

---

## Part V: Why the Data Strategy Is Self-Defeating

### 5.1 The Phase Transition Metrics Measure the Wrong Thing

The data strategy advances through 4 phases based on:

| Phase Transition | Gating Metric |
| ---------------- | ------------- |
| Bootstrap → Grounding | FVD < 300 |
| Grounding → Co-evolution | FVD < 150 + real-world anchoring passes |
| Co-evolution → Autonomous | SimplerEnv correlation > 0.85 |

**FVD (Frechet Video Distance)** measures ==visual quality of generated video==, not physics accuracy. A world model can produce visually beautiful videos that systematically violate physics (objects drifting through each other at high visual fidelity). [[2603.23376|ABot-PhysWorld]] explicitly identified this problem: "current evaluation benchmarks for world models frequently ==overemphasize visual quality== or in-distribution accuracy, ==failing to adequately assess physical consistency==."

The blueprint uses the metric that ABot-PhysWorld says is inadequate as the gate for advancing to higher dream ratios.

**SimplerEnv** (r > 0.85) was validated for a ==narrow set of tabletop manipulation tasks==. Using it to gate the transition to 90% dream data assumes the correlation holds for arbitrary manipulation scenarios — an untested extrapolation.

### 5.2 No Fallback Mechanism

The phases are ==one-directional==. The data mix goes 80% → 50% → 20% → 5% real. What happens if:

- The world model regresses during co-evolution? (Middle Loop instability)
- A new task domain is encountered that the current dream distribution doesn't cover?
- The CriticAgent fails to catch a systematic bias that corrupts the dream distribution?

There is no mechanism to ==fall back== from Phase 4 (5% real) to Phase 2 (50% real). The system can detect failure only through its own internal metrics (which are the same metrics that approved the phase transition), and it has no procedure for reversing course.

### 5.3 The 5% Anchoring Claim Has No Precedent

The Phase 4 target of ==5% real / 90% dream== is presented as the natural endpoint of the data strategy. But:

- [[2602.12063|VLAW]] used real-world rollouts at ==every co-evolution round== and never tested a 90% dream regime
- [[2603.09030|PlayWorld]]'s 65% improvement came from ==adding 30 hours of real autonomous play data==
- [[2411.13852|ESRM]] (cited for replay buffer filtering) was tested in online continual learning settings, not 90% synthetic regimes
- No paper in the blueprint's citation list tested or endorsed a real-data ratio below 20%

The 5% number is ==entirely conjectural==. The blueprint acknowledges this nowhere.

---

## Part VI: Why Convergence Is Undefinable

### 6.1 The Self-Grading Problem

The architecture evaluates itself using exclusively ==internal== metrics:

```
World Model measures → prediction error (own accuracy)
Curiosity Module measures → ensemble disagreement (own uncertainty)
Co-Evolution measures → round-over-round gain (own improvement)
CriticAgent measures → dream quality (trained on own data)
Difficulty Controller measures → Actor success rate (in own dreams)
```

At no point does an ==external, independent== signal enter the evaluation loop. This is structurally identical to a student who:

1. Writes their own exam questions (Outer Loop generates scenarios)
2. Takes the exam (Actor attempts scenarios)
3. Grades the exam (CriticAgent evaluates performance)
4. Decides when they've graduated (Convergence Monitor)

A system that grades itself will always converge — the question is whether it converges to ==correctness== or to ==confident incorrectness==. Without an external oracle (which defeats the purpose of autonomous self-evolution), premature convergence to a local optimum is the ==default outcome==.

### 6.2 The Overconfident Ensemble

The convergence criterion "ensemble disagreement → 0" is dangerous. Ensembles can reach ==unanimous agreement on wrong predictions== when:

- All ensemble members share the same architectural bias
- The training data has systematic gaps (same blind spots)
- The models converge to the same local optimum (lack of diversity)

Low disagreement signals "we're all confident" — not "we're all correct." In high-dimensional latent spaces, this is especially problematic because ==most dimensions are irrelevant==, and the ensemble may agree on the irrelevant dimensions while disagreeing on the critical ones, with the variance signal dominated by the irrelevant agreement.

### 6.3 Convergence and Self-Evolution Are Contradictory Goals

The blueprint wants the system to ==keep evolving== (the thesis) but also to ==know when to stop== (convergence). These are in tension:

- If the system has genuine convergence criteria, it will eventually meet them and ==stop evolving== — becoming the static model the blueprint argues against.
- If the system never converges, it ==never stabilizes== — making deployment dangerous (the policy keeps changing during operation).

The blueprint attempts a middle ground: "Convergence signals should ==reduce evolution rate==, not stop it entirely." But reducing the evolution rate based on internal metrics that may be wrong (6.1) using an ensemble that may be overconfident (6.2) produces a system that ==slows down for the wrong reasons== — either too early (premature convergence) or too late (continued evolution past the point of stability).

---

## Part VII: The Compound Integration Problem

Each individual mechanism has its own failure mode. But the blueprint proposes running ==all of them simultaneously==. The compound system faces integration challenges that no subset has ever been tested for:

| Integration | Conflict |
| ----------- | -------- |
| Fast-WAM + NavMorph CEM | No-imagination inference vs. imagination-based adaptation |
| EWC + Gradient Projection + Replay | Three CL mechanisms with opposing gradient effects |
| LeWM planner + DreamZero Imaginer | 15M model plans, 14B model imagines → different predicted futures |
| Inner Loop forward-update + Middle Loop backprop | Millisecond adaptation overwritten by hour-long training |
| Curiosity ensemble + 14B world model | $k \times 14B$ parameter overhead for disagreement signal |
| Co-evolution + CL | System must change (co-evolve) but also not change (continual learning) |
| AVIC gatekeeper + evolving Imaginer | Meta-policy must track a non-stationary world model |
| Outer Loop + Inner Loop | Generated environments reset Inner Loop adaptation |

Each row is a two-component interaction. The full system has ==dozens of such interactions==, and not one has been tested, even in simulation.

---

## Summary: Five Structural Reasons This Methodology Can't Work

> [!failure] 1. The Inner Loop's components are mutually contradictory
> Fast-WAM removes test-time imagination. NavMorph CEM requires test-time imagination. LeWM's CEM plans in a 15M model while the Imaginer predicts in a 14B model. These cannot coexist in one system — the blueprint's Inner Loop is ==architecturally self-contradicting==.

> [!failure] 2. The Middle Loop's co-evolution has no stability guarantee
> VLAW showed bounded co-evolution works (0.46 → 0.868 over fixed rounds). But the blueprint proposes ==indefinite== co-evolution, where the World Model perpetually chases a changing Actor. Either the system converges (and stops evolving) or diverges (and breaks). There is no stable, perpetually-improving regime.

> [!failure] 3. The CL machinery fights the self-evolution objective
> EWC + Replay + Gradient Projection resist parameter changes. Self-evolution requires parameter changes. The blueprint's own citations show simple LoRA fine-tuning achieves <2% forgetting ([[2603.11653|VLA-RL-Continual-Learning]]), making the complex CL stack both ==unnecessary and counterproductive==.

> [!failure] 4. The three loops cannot synchronize
> Inner Loop forward-updates (ms) are overwritten by Middle Loop backprop (hours). Middle Loop's training distribution is corrupted by Inner Loop's ephemeral adaptations. Outer Loop's environment changes invalidate both Inner and Middle Loop progress. The nesting diagram implies hierarchical control, but the update mechanisms ==interfere destructively==.

> [!failure] 5. The system has no external ground truth
> Every evaluation metric is internal. Every convergence criterion measures the system's assessment of itself. Without an external oracle, the system can converge to ==confidently wrong== states and have no mechanism to detect this.

---

## What Would Fix This

> [!success] Tractable alternative: One loop at a time
> Instead of three nested loops with 15+ interacting mechanisms, test ==one loop in isolation== as a publishable contribution:
>
> **Option A — Inner Loop only**: Deploy a pretrained WAM ([[2602.15922|DreamZero]] or [[2603.16666|Fast-WAM]]) with ==one== test-time adaptation mechanism (NavMorph-style CEM or online gradient updates, not both). Measure whether test-time adaptation improves real-world manipulation success on novel objects/scenes. This is falsifiable, implementable, and novel.
>
> **Option B — Middle Loop only**: Run VLAW-style co-evolution with PlayWorld-style autonomous data collection on a real robot. Measure whether ==each additional round of co-evolution improves real-world success==, and at what round diminishing returns begin. This directly tests the blueprint's central mechanism.
>
> **Option C — Publish the critique**: The failure analysis itself (why static WAMs fail, why naive self-evolution approaches break, what the structural barriers are) is a publishable contribution if grounded in experiments showing concrete failure modes.

---

*Critique of [[00_How-to-Build-Self-Evolving-WAM]]. Companion to [[00_Critique-Self-Evolving-WAM]]. See also: [[16_Self-Evolving-VLA-WAM]] | [[06_WAM]] | [[04_VLA]]*
