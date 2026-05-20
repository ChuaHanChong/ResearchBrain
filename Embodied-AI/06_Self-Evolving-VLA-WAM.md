---
title: "Self-Evolving VLAs & WAMs — Deep Dive"
tags:
  - self-evolving
  - world-model
  - WAM
  - VLA
  - robotics
  - continual-learning
aliases:
  - "Self-Evolving VLA-WAM"
  - "Self-Evolving WAM"
---

# Self-Evolving VLAs & WAMs — Deep Dive

> [!abstract] Overview
> Self-evolving embodied AI systems autonomously discover failure modes, generate new experience, and improve through real-world or simulated interaction. This note covers three paths to self-evolution: **VLAs** that self-evolve via RL fine-tuning (no world model needed), **WAMs** that self-evolve via imagination loops (world model generates synthetic experience), and **embodied agents** that combine both with persistent memory and curiosity-driven exploration. The key insight: start with a trained world model and add self-evolution — not the other way around.

## Evolution Graph

```mermaid
graph TD
    subgraph "Foundations"
        A["STaR<br/><i>2022</i>"]
        B["Dreamer<br/><i>2019</i>"]
    end

    subgraph "Self-Evolving WAMs"
        C["EvoAgent<br/><i>2025</i>"]
        D["SPIRAL<br/><i>2026</i>"]
        E["PlayWorld<br/><i>2026</i>"]
        F["VAMPO<br/><i>2026</i>"]
    end

    subgraph "Self-Evolving VLAs"
        G["EvoVLA<br/><i>2025</i>"]
        H["VLA CL<br/><i>2026</i>"]
        I["EVOLVE-VLA<br/><i>2025</i>"]
    end

    subgraph "Self-Evolving Agents"
        J["EVOLVER<br/><i>2025</i>"]
        K["ECHO<br/><i>2026</i>"]
        L["SE-Agent<br/><i>2025</i>"]
    end

    B --> C
    C --> D
    C --> E
    D --> F
    A --> J
    J --> K
    G --> H
    I --> H
    J --> L

    style D fill:#f0e8fd,stroke:#9b59b6
    style F fill:#f0e8fd,stroke:#9b59b6
    style H fill:#e8fde8,stroke:#27ae60
    style K fill:#e8fde8,stroke:#27ae60
```

> [!info] Graph Legend
> - **Blue (foundations)** — pre-2024 foundational papers ([[2203.14465|STaR]], Dreamer)
> - **Purple (WAM thread)** — world-model-driven self-evolution; agent imagines/dreams
> - **Green (VLA + Agent threads)** — VLA RL post-training and agent-level behavior evolution
> - Arrows indicate intellectual lineage, not architectural inheritance

Three threads converge: **WAM self-evolution** (Dreamer → [[2502.05907|EvoAgent]] → [[2506.24119|SPIRAL]] → [[2603.19370|VAMPO]]) leverages world model imagination; **VLA self-evolution** ([[2511.16166|EvoVLA]] → [[2512.14666|EVOLVE-VLA]] → [[2603.03818|VLA CL]]) uses RL fine-tuning without explicit world models; **agent self-evolution** ([[2203.14465|STaR]] → [[2510.16079|EVOLVER]] → [[2601.06794|ECHO]] → [[2508.02085|SE-Agent]]) operates at the behavior level with persistent experience.

---

## Part A — Conceptual Framework

*The key question, the agent/VLA/WAM taxonomy, core mechanisms, and the failure-detection/diagnosis/recovery loop.*

### 1. The Key Question

> [!question] What's the best starting point?
> **Option 1:** Train a self-evolving agent, then add "dreaming" (future state prediction).
> **Option 2:** Take a trained [[04_WAM|world action model]], then add self-evolution.

==Option 2 wins.== A world model already has a robust latent space for generating synthetic future states. Adding memory and continual learning to a system that can already "imagine" is *easier than teaching a reactive agent to dream from scratch* — and the dominant 2025–2026 research output validates this: the strongest self-evolving systems all start from a pretrained dynamics model, a pretrained VLA backbone, or a pretrained agent with persistent memory. A model-free agent's neural pathways map states → actions only; bolting on a world model means rebuilding the architecture.

The "starting point" decision splits the research landscape into three paths — *agent-, VLA-, and WAM-side self-evolution* — each with different data, compute, and integration trade-offs. The remainder of this section maps these three paths and surfaces the canonical paper for each.

#### 1.1 Self-Evolving Agent (Behavior-Level)

Start from a pretrained agent with persistent experience memory; evolve *behavior* (strategies, skill libraries, prompts) rather than weights. Cheapest to bootstrap, but the agent never internalizes the improvement — it relies on external memory at deployment.

- **[[2510.16079|EVOLVER]]** — distills raw interaction trajectories into ==strategic principles== stored in a persistent experience bank; behavior evolves without weight updates.
- **[[2601.06794|ECHO]]** — policy and environment co-evolve via ==saturation-aware reward==; the canonical agent-side closed loop.
- **[[2203.14465|STaR]]** — the foundational self-training pattern: ==generate → filter → retrain== on successes.

#### 1.2 Self-Evolving VLA (Policy-Level)

Start from a pretrained VLA backbone; evolve weights via RL post-training, continual learning, or self-correction. The pretrained VLM priors confer ==natural resistance to catastrophic forgetting==, making the VLA path more practical than NLP literature suggested.

- **[[2511.16166|EvoVLA]]** — first end-to-end self-evolving VLA; overcomes ==stage hallucination==; **+10.2pp** sim, **+11.0pp** Sim2Real, **1.5×** sample efficiency.
- **[[2603.03818|VLA Continual Learning]]** — proves pretrained VLAs are *naturally* resistant to forgetting; **2–4×** lower NBT with only **2%** replay data.
- **[[2605.08879|ConSFT]]** — exponential conservative weight bounds parameter disruption; **34%** LIBERO retention vs vanilla-SFT collapse.

#### 1.3 Self-Evolving WAM (Dynamics-Level)

Start from a pretrained world action model; evolve via imagination loops (synthetic rollouts) + RL on the dynamics. The model can *rehearse failure modes in imagination* before they cost real-world interactions — the dream-fidelity bottleneck replaces the data-collection bottleneck.

- **[[2502.05907|EvoAgent]]** — built on [[2301.04104|DreamerV3]]; ==self-planning + self-control + self-reflection== loop; **+105%** on long-horizon tasks.
- **[[2603.08403|SPIRAL]]** — ==CriticAgent== verifies dream quality before training; **58.72%** EgoPlan, **+3.94%** over GPT-5.1.
- **[[2603.19370|VAMPO]]** — re-frames video denoising as MDP; GRPO with ==latent-consistency reward== ties visual quality to action quality.

**Key Question — Decision Matrix**

| Need | Starting Point |
|---|---|
| Cheap bootstrap, no weight updates | Agent path: [[2510.16079\|EVOLVER]] (experience principles) |
| Persistent open-ended curriculum | Agent path: [[2601.06794\|ECHO]] (policy + env co-evolve) |
| Real-robot RL post-training (preserve VLM priors) | VLA path: [[2603.03818\|VLA CL]] + LoRA |
| Bound parameter disruption during SFT | VLA path: [[2605.08879\|ConSFT]] |
| Imagination-driven exploration (no real-world cost) | WAM path: [[2502.05907\|EvoAgent]] or [[2603.08403\|SPIRAL]] |
| RL over video-generation steps | WAM path: [[2603.19370\|VAMPO]] |
| No pretrained backbone available (limited data) | WAM path: [[2301.04104\|DreamerV3]] from scratch |
| Multi-step agent tasks with verifiable rewards | Agent path: [[2506.21669\|SEEA-R1]] (tree-RL + MGRM, **+24%** via MCTS) |

> [!star] Key Papers
> - [[2502.05907|EvoAgent]] — Canonical *WAM path*: continual world model + self-planning/control/reflection; **+105%** long-horizon. The clearest evidence Option 2 wins on dynamics-heavy tasks.
> - [[2511.16166|EvoVLA]] — Canonical *VLA path*: end-to-end self-evolving VLA solving stage hallucination + fragile memory; **+10.2pp** sim SR, **+11.0pp** Sim2Real.
> - [[2510.16079|EVOLVER]] — Canonical *agent path*: experience-distillation lifecycle; behavior evolves without weight updates — the cheapest entry to self-evolution.

> [!tip] Pick Your Substrate Before Your Mechanism
> The starting point dictates the failure mode. *Agent path*: cheap but external memory dominates inference cost; *VLA path*: weights internalize improvement but RL signal is noisy without ground-truth reward; *WAM path*: imagination compounds gains but ==hallucinated dynamics== can corrupt the policy (see §8). Three substrates, three risk profiles — and the 2026 frontier is hybrid: WAM-pretrained backbone + VLA-style RL post-training + agent-style experience memory. Cross-reference [[04_WAM#1. The Design Space]] for the WAM design space the dynamics path inherits, [[03_VLA#9. Self-Evolving & Continual VLAs]] for the VLA path's continual-learning recipes, and [[11_Self-Evolving-AI#4. Self-Evolving Agents]] for the broader self-evolving landscape beyond embodied AI.

---

### 2. Self-Evolving Agent vs VLA vs WAM

The three substrates are *not* mutually exclusive — they're orthogonal points in the dynamics-richness × prior-richness plane. A self-evolving WAM is a *subset* of self-evolving agents (it has a world model on top); a self-evolving VLA sits between (rich VLM priors but may or may not include a world model). ==Not all self-evolving agents can predict the future==, and that asymmetry is what creates the design tension: imagination buys safe exploration but costs latency and risks ==dream hallucination==; pure-policy evolution stays grounded but loses the rehearsal benefit.

This section forces the comparison along three concrete substrates so the rest of Part B (§5 WAM, §6 VLA, §7 Agent) reads as parallel deep-dives rather than overlapping clusters.

#### 2.1 Agent-Side (Model-Free, Behavior-Level)

The broadest substrate. Maps state → action via trial and error with no explicit dynamics model. Evolution operates at the *behavior* level: experience banks, skill libraries, prompts, reasoning traces — not raw weights. Domain-agnostic but lacks imagination.

- **[[2510.16079|EVOLVER]]** — ==offline experience self-distillation== + online interaction + policy evolution; closes the loop without weight updates.
- **[[2601.06794|ECHO]]** — ==Cascaded Evolutionary Rollout== generates multi-view diagnostic critiques + ==saturation-aware reward== that non-linearly weights "last-mile" improvements; policy and critic co-optimize synchronously to defeat critic staleness; **+7.28 pts** avg over GRPO across 4 open-world benchmarks and **+42%** relative on DeepSearch.
- **[[2506.21669|SEEA-R1]]** — tree-structured RL with ==self-trained MGRM== reward model; **+24%** via MCTS; **46.27%** ALFWorld vs GPT-4o's **24%**.
- **[[2601.07055|Dr. Zero]]** — Meta's search agent self-evolves without human training data; ==HRPO== cuts rollout cost **~4×**.

#### 2.2 VLA-Side (Policy-Level, VLM-Pretrained)

A VLM-pretrained policy fine-tuned for embodied action. Self-evolution applies RL post-training + continual learning to *weights*. The pretrained backbone confers a ==broad parameter basin== that LoRA stays within — the surprising-but-replicated result that VLAs resist forgetting.

- **[[2511.16166|EvoVLA]]** — first end-to-end self-evolving VLA; ==Stage-Aligned Reward (SAR)== module using ==LLM-generated hard negatives== + ==image-text contrastive scoring== combats stage hallucination; **+10.2pp** sim SR (**69.2%** avg), **+11.0pp** Sim2Real, hallucination **38.5% → 14.8%**.
- **[[2603.03818|VLA Continual Learning]]** — pretrained VLAs *naturally* resist forgetting; near-zero NBT, **2–4×** lower than non-pretrained, **2%** replay buffer enough.
- **[[2605.08879|ConSFT]]** — bounds parameter disruption via exponential conservative weight; **34%** LIBERO / **28%** RoboTwin retention vs vanilla-SFT collapse.
- **[[2603.11653|VLA RL CL]]** — ==Sequential Fine-Tuning + LoRA + GRPO== on-policy across 5 lifelong RL benchmarks; **<2%** NBT and oracle-beating zero-shot generalization across OpenVLA / π-0; ==implicit regularization + blessing of dimensionality + low-rank constraint== combine so new-task gradients are near-orthogonal to pretrained knowledge.

#### 2.3 WAM-Side (Model-Based, Dynamics-Level)

A world model that maps $(S_t, A_t) \to (S_{t+1}, R_{t+1})$ — explicit dynamics enable *imagination*: simulate futures in latent or pixel space, rehearse risky actions safely, generate thousands of synthetic rollouts per real interaction. The richest path but bottlenecked on dream fidelity.

- **[[2502.05907|EvoAgent]]** — [[2301.04104|DreamerV3]] backbone + ==continual world model== with closed-loop ==self-planning + self-control + self-reflection==; ==Multimodal Experience Pool== fed by two-stage curriculum + ==LoRA== on failure cases + regularization against catastrophic forgetting; **+105%** avg SR on 67 long-horizon Minecraft tasks (**21.69%** Gold vs Optimus-1 **10.62%**), **6×** fewer ineffective actions, continual WM contributes **72%** of total gain.
- **[[2603.08403|SPIRAL]]** — ==PlanAgent + Action-Conditioned WM + CriticAgent==; CriticAgent rejects bad dreams before training; **58.72%** EgoPlan.
- **[[2603.19370|VAMPO]]** — video denoising as MDP; GRPO over generation steps with ==latent-consistency reward==.
- **[[2506.23468|NavMorph]]** — ==RSSM-based world model== with ==Contextual Evolution Memory== that updates online via forward passes (no gradient) + ==feature-level future prediction== in latent space (not pixel); **+4.1% SR** / **+2.73% SPL** on RxR-CE unseen, CEM is **2.1×** faster than gradient-based alternatives at test time.

**Substrate — Decision Matrix**

| | Self-Evolving Agent | Self-Evolving VLA | Self-Evolving WAM |
|---|---|---|---|
| **Type** | Model-free (broadest) | VLM-based policy | Model-based (world model) |
| **Learns** | State → Action via trial and error | Language-conditioned manipulation via RL | Transition dynamics: $S_t, A_t \rightarrow S_{t+1}, R_{t+1}$ |
| **Can "dream"?** | No — reacts after the fact | No (unless WAM-augmented) | Yes — simulates futures in latent/pixel space |
| **Self-evolution** | Improve policy directly | RL post-training + continual learning | Minimize prediction error + policy improvement |
| **Key advantage** | General, domain-agnostic | Rich VLM priors, resistant to forgetting | Imagination for safe exploration |
| **Key risk** | Sample-inefficient; needs many real-world trials | Reward signal noisy without ground-truth | Hallucinated dynamics corrupt policy |
| **Best For** | Open-ended curriculum + verifiable rewards | Real-robot RL with pretrained backbone | Imagination-heavy rehearsal of failure modes |
| **Canonical paper** | [[2510.16079\|EVOLVER]] / [[2601.06794\|ECHO]] | [[2511.16166\|EvoVLA]] / [[2603.03818\|VLA CL]] | [[2502.05907\|EvoAgent]] / [[2603.08403\|SPIRAL]] |

> [!example] The Button Test
> A model-free agent learns "pressing button → reward" but has no concept of the gears behind the button. If the button jams, it's surprised *after* pressing. A VLA might generalize from similar buttons it's seen in training. A WAM *imagines* the jam scenario and plans accordingly.

> [!star] Key Papers
> - [[2510.16079|EVOLVER]] — Defines the agent-side substrate: distill raw trajectories into strategic principles; the cheapest self-evolution loop.
> - [[2603.03818|VLA Continual Learning]] — Defines the VLA-side surprise: pretrained VLAs are *naturally* forgetting-resistant; **2–4×** lower NBT, only **2%** replay needed.
> - [[2502.05907|EvoAgent]] — Defines the WAM-side blueprint: DreamerV3 + self-planning/control/reflection; **+105%** long-horizon improvement validates Option 2.

> [!tip] Three Substrates, Three Failure Modes
> The substrate decision dictates the failure mode you inherit. Agent-side: sample-inefficient — real-world trials dominate the cost curve unless you have verifiable rewards ([[2506.21669|SEEA-R1]]). VLA-side: RL signal is noisy and the backbone can degrade if SFT is unconservative ([[2605.08879|ConSFT]] mitigates). WAM-side: dream hallucination corrupts policy unless filtered ([[2603.08403|SPIRAL]]'s CriticAgent, [[2603.23376|ABot-PhysWorld]]'s Diffusion-DPO). Cross-reference [[03_VLA#9. Self-Evolving & Continual VLAs]] for the VLA self-evolution recipes in depth, [[04_WAM#7. Self-Evolving WAMs]] for the WAM self-evolution paradigms, and [[11_Self-Evolving-AI#5. Self-Evolving Embodied AI]] for the broader landscape beyond embodied AI.

---

### 3. Core Mechanisms of Self-Evolution

A ==self-evolving world action model== simultaneously learns to predict environmental dynamics (world model) and optimize decision-making (action model) through continuous, self-supervised interaction. These are the five core mechanisms:

#### 3.1 World Models as Internal Simulators

The agent maintains a learned dynamics model that simulates trajectories without physical execution — enabling safe exploration, sample-efficient learning via synthetic rollouts, and planning by evaluating many action sequences. The bottleneck is ==dream fidelity==: if the model hallucinates physically impossible transitions, the policy exploits artifacts that don't exist.

- **[[2502.05907|EvoAgent]]** — ==DreamerV3 backbone== + continual WM with self-planning/self-control/self-reflection loop; **+105%** on long-horizon tasks.
- **[[2301.04104|DreamerV3]]** — Universal ==RSSM== + latent imagination; **150+** tasks with *fixed hyperparameters*; the canonical dynamics-model substrate.
- **[[2005.05960|Plan2Explore]]** — Self-supervised exploration via ==ensemble disagreement==; zero-shot adaptation by pre-training the world model purely through curiosity.

#### 3.2 Co-Evolutionary Loops

Policy and world model improve each other in alternating rounds — better WMs produce more realistic synthetic data; better policies explore more diverse states; the cycle compounds. The risk is ==chasing==: the WM models the *previous* policy's distribution, destabilizing training if updates outpace WM retraining.

- **[[2602.12063|VLAW]]** — Canonical alternating loop: ==policy acts → WM trains on real trajectories → WM generates dreams → policy trains on dreams==; the field's most-copied co-evolution recipe.
- **[[2605.13775|RoboEvolve]]** — Planner + simulator co-evolution via ==CLS-inspired "daytime exploration / nighttime consolidation"==; learns from near-miss failures; **+36.4 abs pts** on EB-ALFRED with only **300** unlabeled seeds vs SFT on **25K** annotated trajectories.
- **[[2603.08403|SPIRAL]]** — Adds a ==CriticAgent== that filters hallucinated dynamics before they corrupt the policy; the dream-quality gate inside the co-evolution loop.
- **[[2601.06794|ECHO]]** — Environment ↔ policy co-evolution via ==saturation-aware reward==; tasks retire and harden as success rate crosses threshold.
- **[[2504.21024|WebEvolver]]** — Co-trains agent policy + dedicated world-model LLM that acts as a ==virtual web server== synthesizing diverse multi-step trajectories; ==Multi-Step Look-Ahead (WMLA)== at depth 2 lifts WebVoyager to **51.37%** SR (**+10%** over OpenWebVoyager) and Mind2Web-Live from **18.86% → 24.53%**; the web-domain instantiation of the VLAW co-evolution pattern.

#### 3.3 Self-Training and Self-Critique

==Generate candidate solutions → filter for correctness → retrain on successes.== Unlike code generation, embodied "correctness" requires either ground-truth reward or a ==learned verifier== (VLM-as-judge) — the bottleneck that makes self-critique harder than in language tasks.

- **[[2203.14465|STaR]]** — Foundational loop: ==generate → filter → retrain on successes==; the pattern underlying all later self-critique methods.
- **[[2603.16856|OEL]]** — Reward-free online loop: ==knowledge extraction== from interaction trajectories without ground-truth labels, then ==on-policy context distillation== via ==token-level reverse KL== consolidates into weights server-side; Frozen Lake response length **−30%** while accuracy improves and IF-Eval OOD accuracy preserved better than off-policy distillation.
- **[[2403.09629|Quiet-STaR]]** — Internalizes critique by generating ==reasoning traces within the forward pass==, eliminating the separate evaluation stage.
- **[[2510.16079|EVOLVER]]** — Distills raw trajectories into ==strategic principles== persisting across episodes; weights stay frozen, behavior evolves via memory.

#### 3.4 Curiosity-Driven Exploration

The agent self-estimates uncertainty and targets exploration where the model is worst — a self-directed curriculum. The critical pitfall: confusing ==aleatoric uncertainty== (irreducible randomness) with ==epistemic uncertainty== (reducible ignorance) wastes exploration budget on inherently stochastic states.

- **[[2503.01584|SENSEI]]** — ==Semantic uncertainty + Go-Explore==; targets the agent's hardest states via VLM-derived novelty signals.
- **[[2005.05960|Plan2Explore]]** — ==Ensemble disagreement== as curiosity signal; the prototype zero-shot exploration recipe.
- **[[2602.20057|AdaWorldPolicy]]** — Uses ==WM prediction error== directly as a self-improvement signal; policy updates focus on states with highest WM uncertainty.
- **[[2007.07853|gamma-Progress]]** — Weights curiosity by ==temporal discount==; focuses on uncertainties that matter for long-horizon tasks.

#### 3.5 RL Post-Training

After SFT on demonstrations, RL optimizes for task success. ==GRPO== (no critic network, compares trajectory groups) is the canonical recipe for flow-matching VLAs with continuous action spaces. The signal can come from sparse ground-truth, VLM-as-judge, or WM prediction error.

- **[[2603.19370|VAMPO]]** — Re-frames ==denoising as an MDP==; policy gradient over video generation steps with a ==latent-consistency reward== tying visual quality to action quality.
- **[[2509.19292|SOE]]** — ==Variational information bottleneck== identifies which action dimensions most need improvement; focuses RL compute where it matters; **50.8%** relative SR gain.
- **[[2603.11653|VLA RL Continual Learning]]** — Sequential RL fine-tuning with ==LoRA==; minimal forgetting across a task stream.
- **[[2505.05470|Flow-GRPO]]** — GRPO extension for ==flow-matching policies==; handles the continuous-time formulation.

> [!star] Key Papers
> - [[2602.12063|VLAW]] — Iterative co-improvement of VLA + world model; the canonical co-evolutionary loop
> - [[2503.01584|SENSEI]] — Semantic uncertainty + Go-Explore for curiosity-driven exploration; targets the agent's hardest states
> - [[2203.14465|STaR]] — Foundational self-training loop: generate → filter → retrain; the pattern that underlies all self-critique methods

> [!tip] The Five Levers
> Self-evolution combines all five mechanisms: the world model **imagines** scenarios, curiosity **targets** the hardest ones, RL **optimizes** the policy, self-critique **filters** bad solutions, and co-evolution **compounds** the gains. Each lever alone helps; together they create positive feedback loops.

---

### 4. Failure Detection, Diagnosis & Recovery

Self-evolution requires self-awareness. Before an agent can improve, it must first know *what* went wrong, *where* its policy is weak, and *when* to abandon a failing plan. This section covers the prerequisite layer that makes Sections 5-7 possible: the mechanisms by which agents **detect** failures, **diagnose** their root cause, and **recover** with corrective action.

#### 4.1 Runtime Failure Detection

VLMs and learned classifiers detect task failure in real-time so the agent can abort early. The cluster splits along the *signal type* — internal features, semantic misalignment, OOD score, density-based, multi-detector, calibration, LLM-driven, or human-shared.

- **[[2510.09459|FIPER]]** — ==Predictive failure detection== via OOD + action uncertainty; catches failures *before* they happen, giving the agent a window to intervene.
- **[[2506.09937|SAFE]]** — VLA's own hidden-state activations + ==conformal prediction==; provable false-positive guarantees with no external sensor.
- **[[2410.00371|AHA]]** — ==Instruction-tuned VLM== generating ==free-form natural-language failure explanations==; ==FailGen== procedurally perturbs successful trajectories to label diverse failure modes (49K+ examples mixed with 765K VQA); AHA-13B beats GPT-4o on AHA-Test (**0.446** ROUGE-L) and RoboFail (**0.280**); integrating its feedback adds **+22.34%** RL reward synthesis, **+36.7%** TAMP, **+5%** zero-shot data-gen SR.
- **[[2509.16072|I-FailSense]]** — VLMs compare observed outcomes against ==language-described expected outcomes==; detects semantic-misalignment failures.
- **[[2510.01642|FailSafe]]** — ==Automatic failure-action data pipeline== generating ==7-DoF delta recovery actions== via perturbed-trajectory rollouts; LLaVA-OneVision-7B fine-tuned to FailSafe-VLM hits **0.9094** failure-detect SR + **0.6522** action cosine similarity (general VLMs near zero); integrated as external assistant lifts OpenVLA **+22.6%**, OpenVLA-OFT **+8.0%**, π-FAST **+4.0%**, and Stack-Cube on unseen xArm6 from **56% → 76%**.
- **[[2603.11106|RC-NF]]** — ==Robot-conditioned normalizing flows== learn joint distribution of successful execution; flags deviations in **<100ms**.
- **[[2503.08558|FAIL-Detect]]** — ==logpZO== flow-based density + Conformal Prediction; **78%** balanced accuracy *without any failure data*.
- **[[2410.14868|Diff-DAgger]]** — Repurposes ==diffusion-policy training loss== as uncertainty signal; **+39%** F1 over ensemble baselines.
- **[[2410.04640|Sentinel]]** — Multi-detector ensemble: ==STAC== (temporal action consistency) for erratic failures + VLM for task-progression failures; catches **+18%** more failures than either alone.
- **[[2507.17383|VLA Confidence Calibration]]** — ==Action-Wise Platt Scaling==; reduces Expected Calibration Error by **>20%**.
- **[[2407.08735|AESOP]]** — Fast embedding anomaly detector + slow LLM for deliberative intervention; ==latency-aware MPC==; **100%** recovery on simulated anomalies.
- **[[2510.02298|ARMADA]]** — ==FLOAT detector== (**95%** accuracy) pooled across multiple robots; cuts human intervention by **23.3%**.

#### 4.2 Proactive Self-Correction

Detect and correct errors mid-task — three strategies: subtask backtracking, counterfactual reasoning, speculative verification.

- **[[2601.02295|CycleVLA]]** — Decomposes tasks into ==subtask cycles==; detects subtask failure and ==backtracks to last known good state== rather than restarting from scratch.
- **[[2512.24426|CF-VLA]]** — ==Counterfactual reasoning==: generates "what if I had done differently?" action sequences and compares predicted outcomes against the current trajectory.
- **[[2511.14148|AsyncVLA]]** — ==Asynchronous Flow Matching (AFM)==: SFM generates initial action chunk, then a ==confidence rater== masks low-confidence tokens for regeneration using unmasked context; unified SFM+AFM training enables ==KV-cache reuse==; **97.4%** LIBERO avg, **70.8%** WidowX, **74.9%** Google Robot visual-matching with faster convergence under limited data.
- **[[2604.02965|SV-VLA]]** — ==Speculative verification==: open-loop action plans verified step-by-step against reality before committing.
- **[[2602.21633|SC-VLA]]** — Self-correction head continuously monitors execution and ==suggests corrective micro-actions==.

#### 4.3 OOD & Surprise Detection

WM prediction error as a failure signal — when the world model's prediction diverges from reality, the agent is in uncharted territory. The practical challenge: distinguishing genuine surprises from noise and stochastic dynamics.

- **[[2603.04029|Self-Adapting RL]]** — Monitors ==residuals== between predicted and observed next-states; triggers ==targeted self-adaptation== for novel regions instead of global retraining; adapts F1Tenth to friction shift in **8 min**.
- **[[2512.01119|WM Surprise Robustness]]** — Filters noisy prediction errors to distinguish ==genuine novelty== from sensor noise + stochastic dynamics; avoids false-alarm adaptation triggers.
- **[[2602.20057|AdaWorldPolicy]]** — Uses ==WM prediction error== directly as a gradient signal; focuses policy updates on states where the WM is least confident.

#### 4.4 Active Probing for Weaknesses

Deliberately search for policy failure modes during training rather than waiting for production failures — adversarial probing, information-bottleneck action analysis, or curiosity-driven coverage.

- **[[2412.02818|RoboMD]]** — Trains an ==RL adversary== to find the conditions under which the target policy fails; systematically maps the failure landscape.
- **[[2509.19292|SOE]]** — ==Variational information bottleneck== identifies action dimensions lacking confidence; surfaces skills needing improvement.
- **[[2503.01584|SENSEI]]** — Epistemic uncertainty + ==Go-Explore==; systematically visits states where WM predictions are worst.
- **[[2005.05960|Plan2Explore]]** — Extends curiosity to ==zero-shot task adaptation== via WM pretrained purely through exploration.
- **[[1705.05363|ICM]]** — Intrinsic curiosity module; uses ==forward-model prediction error as exploration reward==; the foundational curiosity recipe.

#### 4.5 Failure Recovery

After detection, generate recovery plans and learn from failures so they don't recur — combining failure prediction with corrective generation, root-cause analysis, or synthetic failure injection.

- **[[2509.04018|FPC-VLA]]** — Combines ==failure prediction + corrective action generation== in one model; corrective head fires when the failure predictor activates, steering back to a recoverable state.
- **[[2404.00756|Recover]]** — ==Neuro-symbolic== integration of ==OntoThor ontology== (taxonomy of failures + logical rules) with LLM planning via an online cyclical loop (action → scene-graph + audio → ontological reasoning → LLM plan); **100%** rule-based failure-detection accuracy vs ~50% LLM-only, **~70%** recovery rate, **100%** safety-issue detection with **93%** recovery, **59% / 33%** task-completion SR on simple/complex tasks.
- **[[2505.12224|RoboFAC]]** — Full ==failure analysis + correction framework==: classifies failure type (perceptual / planning / execution), diagnoses root cause, generates targeted corrections per category.
- **[[2409.03966|VLM Failure Recovery]]** — Black-box GPT-4o as VLM controller with ==prompt engineering== (visual markers + ==relative-position language prompts==) and decomposed reasoning (detection vs correction; 1D spatial sub-queries); Lego Assembly 3D error **0.005m** (vs **0.016m** OpenVLA), Target Reach coverage **0% → 65.78%**, **116/120** task-level detection / **110/120** analysis without fine-tuning.
- **[[2603.13528|Counterfactual Failure Synthesis]]** — Generative approach: synthesizes ==new failure scenarios + actionable recovery plans== as synthetic training data; inoculates the policy without real-world experience.

> [!star] Key Papers
> - [[2510.09459|FIPER]] — Predictive failure detection via OOD + action uncertainty; catches failures *before* they happen, giving the agent time to intervene
> - [[2412.02818|RoboMD]] — Active adversarial probing: trains an RL adversary to systematically discover where the policy fails, mapping the failure landscape
> - [[2601.02295|CycleVLA]] — Proactive mid-task correction via subtask cycling and backtracking; detects and recovers from errors without restarting the entire task

> [!tip] Detection Before Correction
> Self-evolution requires self-awareness. An agent that can't detect failure can't improve from it. The detection mechanism determines what the agent can learn: [[2510.09459|FIPER]] detects WHEN tasks fail, [[2412.02818|RoboMD]] discovers WHERE policies are weak, and [[2503.01584|SENSEI]] finds WHAT the world model doesn't know. Together they form a complete diagnostic stack — temporal detection, spatial localization, and epistemic coverage — that feeds the self-improvement loops in Sections 5-7.

```mermaid
graph LR
    A["Detect<br/>FIPER, SAFE"] --> B["Diagnose<br/>RoboMD, SOE"]
    B --> C["Recover<br/>CycleVLA, FPC-VLA"]
    C --> D["Learn<br/>LoRA fine-tune"]
    D --> E["Verify<br/>Benchmark eval"]
    E -->|"still failing"| A

    style A fill:#fde8e8,stroke:#e74c3c
    style C fill:#e8f4fd,stroke:#4a90d9
    style E fill:#e8fde8,stroke:#27ae60
```

---

## Part B — Self-Evolving Systems by Subject

*Three concrete instantiations: self-evolving WAMs, VLAs, and embodied agents.*

### 5. Self-Evolving WAMs

WAMs have a unique advantage for self-evolution: they already have a learned dynamics model that can generate synthetic experience. The agent "rehearses" in imagination, discovers failure modes, and improves without costly real-world interaction. The cluster splits along *how* the model uses its imagination to drive improvement — reflective planning loops, RL over dynamics, self-play data engines, or continual learning with replay.

#### 5.1 Reflective Planning Loops

The world model generates a plan or rollout; a separate critic (or the agent itself) evaluates the plan against dynamics fidelity or task completeness; failed plans are rejected and regenerated. The critic stage is the load-bearing innovation — without it, hallucinated dynamics propagate into the policy.

- **[[2603.08403|SPIRAL]]** — ==PlanAgent + Action-Conditioned WM + CriticAgent==; CriticAgent evaluates plans for *temporal coherence* (do frames flow smoothly?) and *action completeness* (does the video show the full task?), rejecting bad dreams pre-training; **58.72%** EgoPlan-Bench, **+3.94%** over GPT-5.1, **+6.89%** over fine-tuned Video-LLaMA.
- **[[2502.05907|EvoAgent]]** — DreamerV3 backbone + continual WM; three-part loop — ==self-planning== (propose plan via WM), ==self-control== (monitor prediction error during execution), ==self-reflection== (compare predicted vs actual after execution, update WM + policy); **+105%** on long-horizon tasks.
- **[[2506.23468|NavMorph]]** — ==RSSM-based== self-evolving WM for VLN-CE; World-aware Navigator + Foresight Action Planner; **+4.1% SR** / **+2.73% SPL** on RxR-CE unseen.

#### 5.2 RL on Dynamics & Co-Evolving Loops

Apply policy-gradient RL directly to the world model's generation steps, or co-train policy and world model in alternating rounds so each improves the other. The risk is ==chasing== — the WM models a policy that no longer exists between updates.

- **[[2603.19370|VAMPO]]** — re-frames ==video denoising as an MDP==; GRPO over generation steps with ==latent-consistency reward== ties visual quality to action quality.
- **[[2504.21024|WebEvolver]]** — Co-evolving web agent + ==world-model LLM as virtual web server== with ==Multi-Step Look-Ahead (WMLA)== at inference; **+10%** over OpenWebVoyager and **51.37%** WebVoyager SR (depth-2 WMLA); canonical alternating co-evolution recipe in the web-agent setting.
- **[[2602.20057|AdaWorldPolicy]]** — ==world model prediction error== as a self-improvement gradient signal; policy updates focus on states where the WM is least confident.
- **[[2511.18810|MergeVLA]]** — cross-skill model merging toward a generalist VLA; **90.2%** LIBERO cross-skill, **62.5%** LIBERO-Plus; direct merging baselines score **0%**.

#### 5.3 Self-Play & Continual Replay

Autonomous data engines that generate their own training data via self-play, plus replay strategies that prevent catastrophic forgetting in long-running continual RL. The substrate for *long-lived* WAM training without curated data.

- **[[2603.09030|PlayWorld]]** — autonomous self-play data collection → world model training; Pearson **0.8766** sim-real correlation, **+65%** real-world SR via in-model fine-tuning.
- **[[2503.01584|SENSEI]]** — ==semantic uncertainty + Go-Explore==; pre-trains a world model purely through curiosity-driven exploration.
- **[[2401.16650|WMAR]]** — ==memory-efficient augmented replay== (FIFO + reservoir) on top of [[2301.04104|DreamerV3]]; forgetting **0.071 vs 0.665** baseline.

**Self-Evolving WAM — Decision Matrix**

| Need | Recommendation |
|---|---|
| Reflective video-plan generation with built-in critic | [[2603.08403\|SPIRAL]] (**58.72%** EgoPlan, **+3.94%** over GPT-5.1) |
| Continual DreamerV3 + self-planning/control/reflection | [[2502.05907\|EvoAgent]] (**+105%** long-horizon) |
| Self-evolving WM for VLN-CE | [[2506.23468\|NavMorph]] (**+4.1% SR** RxR-CE unseen) |
| RL over video-generation steps (denoising as MDP) | [[2603.19370\|VAMPO]] |
| WM prediction error as self-improvement signal | [[2602.20057\|AdaWorldPolicy]] |
| Co-evolving agent + WM in alternating rounds | [[2504.21024\|WebEvolver]] |
| Cross-skill merging toward generalist VLA | [[2511.18810\|MergeVLA]] (**90.2%** cross-skill, **62.5%** LIBERO-Plus) |
| Self-play data engine for WM training | [[2603.09030\|PlayWorld]] (**+65%** real SR via in-model fine-tune) |
| Curiosity-driven WM pretraining (semantic uncertainty) | [[2503.01584\|SENSEI]] |
| Continual RL replay without forgetting | [[2401.16650\|WMAR]] (forgetting **0.071 vs 0.665**) |

> [!star] Key Papers
> - [[2603.08403|SPIRAL]] — Canonical reflective loop: ==PlanAgent + Action-Conditioned WM + CriticAgent== closes the dream-fidelity gap; **58.72%** EgoPlan-Bench beats GPT-5.1 by **+3.94%**.
> - [[2502.05907|EvoAgent]] — Canonical DreamerV3-derived self-evolving WM; the **+105%** long-horizon result is the strongest evidence that Option 2 (start from WAM) works.
> - [[2603.19370|VAMPO]] — Canonical RL-on-dynamics: denoising-as-MDP + ==latent-consistency reward==; ties visual quality directly to action quality during generation.
> - [[2511.18810|MergeVLA]] — Canonical model-merging path to self-evolution: **90.2%** LIBERO cross-skill where naive merging scores **0%**.

> [!tip] Imagination Buys Rehearsal, Critics Buy Safety
> WAMs let the agent rehearse without real-world cost — but raw imagination is dangerous. [[2603.08403|SPIRAL]]'s CriticAgent and [[2502.05907|EvoAgent]]'s self-reflection both add an ==explicit dream-quality gate== before the policy learns from the rollout. Without that gate, ==hallucinated dynamics== (see §8) compound into entropy collapse or value drift. The 2026 pattern: every self-evolving WAM has a critic, replay buffer, or DPO-style filter between dream and policy update. Cross-reference [[04_WAM#7. Self-Evolving WAMs]] for the broader WAM self-evolution paradigms, [[05_Latent-World-Models#3. Broader Latent Prediction Landscape]] for the latent-prediction substrate these imagination loops run over, and [[07_Physics-Aware-Embodied-AI#3. Explicit Physics Losses for Video Generation]] for physics-priors that further reduce dream hallucination.

---

### 6. Self-Evolving VLAs

VLAs can self-evolve *without* an explicit world model — their rich VLM representations from large-scale pretraining provide enough structure for RL-based self-improvement and continual learning. The empirical surprise: pretraining on diverse cross-embodiment data ([[2310.08864|OXE]]: 1M+ trajectories from 22 robot types) creates a broad, well-structured parameter basin. Sequential task fine-tuning with ==LoRA== stays within this basin — the ==low-rank constraint== confines updates to a small subspace, preserving the vast majority of pre-trained parameters. This is the *opposite* of what the NLP literature suggested, and it makes VLA self-evolution far more practical than expected.

The cluster splits along *which side of the SFT-RL recipe* it stabilizes — the conservative-SFT lineage prevents the policy from collapsing under fine-tuning, the continual-RL lineage prevents forgetting across a task stream, and the memory-augmented lineage adds persistent experience storage on top.

#### 6.1 Conservative SFT & Stable Fine-Tuning

Stabilize the SFT side of the recipe to bound parameter disruption — the policy can't self-evolve if downstream fine-tuning collapses the pretrained backbone. The axis: *constrain weight updates without sacrificing target-task performance*.

- **[[2605.08879|ConSFT]]** — ==exponential conservative importance weight== ω(θ) = exp(−L_SFT(θ) / τ) with ==stop-gradient operator== + ==annealing schedule== on τ; analytically bounds parameter-disruption risk for unfamiliar high-loss transitions; mimics RL's bounded-trust-region dynamics without likelihood evaluation; **34%** LIBERO / **28%** RoboTwin retention vs vanilla SFT's collapse. *No prior data, no architectural mods.*
- **[[2501.16664|iRe-VLA]]** — two-stage alternation between online RL and SFT with ==LoRA + frozen VLM==; canonical stable RL recipe.
- **[[2602.21633|Self-Correcting VLA]]** — Two-stage ==Sparse World Imagination + Online Action Refinement==: SPI augments policy input with short-horizon physical-state predictions; OAR runs ==residual RL== with ==intrinsic dense rewards== from SPI; **86%** ManiSkill3 avg (vs **72%** GR00T N1.5 / **55%** π-0), **−43%** completion steps vs π-0, **71%** real-world ARX5 SR (vs **57%** GR00T N1.5).
- **[[2511.00091|PLD]]** — self-improving VLA via ==residual RL data generation==; bootstraps RL with policy-aligned data.

#### 6.2 Continual RL Across Task Streams

Sequential RL fine-tuning across a stream of tasks without forgetting prior skills — the operational form of self-evolution for a long-lived robot.

- **[[2603.03818|VLA Continual Learning]]** — pretrained VLAs are *naturally* resistant to forgetting; near-zero NBT, **2–4×** lower than non-pretrained, **2%** replay buffer enough. Forgotten skills recovered in **<10%** of original training steps.
- **[[2603.11653|VLA RL Continual Learning]]** — ==Sequential FT + LoRA + GRPO== on-policy RL with **<2%** NBT and oracle-beating zero-shot generalization across 5 lifelong RL benchmarks (OpenVLA + π-0); proves the surprising-but-replicated result that pretrained VLAs are naturally forgetting-resistant.
- **[[2603.07648|AtomicVLA]]** — ==atomic skill abstraction + SG-MoE==; scalable continual learning across many sequential tasks.
- **[[2602.03445|CRL-VLA]]** — ==Dual-critic architecture==: frozen ==Goal-Conditioned Value (GCV) critic== for stability + trainable ==Monte Carlo critic== for plasticity, regulated by ==PPO + KL== and GCV-consistency; **+0.17** positive Backward Transfer (learning new tasks improves old ones) and **0.74** Final Average Return — diagnoses forgetting as caused by goal-conditioned advantage magnitude.
- **[[2602.10503|Long-Lived Robots]]** — ==LifeLong-RFT==: ==interaction-free chunking-level GRPO== with ==Multi-Dimensional Process Reward== (Quantized Action Consistency + Continuous Trajectory Alignment + Format Compliance); **+8.7%** real Franka SR, **+4.4%** Google Robot, **+19.6%** forward transfer with NBT cut to **1.5** (vs SFT's **6.8**), and adapts with only **20%** of the SFT data.
- **[[2511.16166|EvoVLA]]** — first end-to-end self-evolving VLA; ==explicit stage tracker== verifies subtask completion before advancing (preventing *stage hallucination* — reporting subtask done based on superficial visual cues); evolutionary strategy generates multiple candidate plans and selects most reliable; **+10.2pp** sim, **+11.0pp** Sim2Real, hallucination **38.5% → 14.8%**, **1.5×** sample efficiency.
- **[[2512.14666|EVOLVE-VLA]]** — ==Test-time training== via online ==GRPO== with a ==learned task-progress estimator== replacing oracle rewards; ==accumulative progress estimation + progressive horizon extension== mitigate reward noise; **+6.5%** abs LIBERO avg (**89.2% → 95.8%**), **+8.6%** long-horizon, **+17.7%** in 1-shot settings (**43.6% → 61.3%**), and breaks the 0% barrier for cross-task (**20.8%** unseen-task SR with zero demos).

#### 6.3 Memory-Augmented & Failure-Driven Evolution

Add persistent memory and failure-driven data collection on top of the VLA backbone — evolution operates over external memory + replay rather than weight updates alone. The axis: *trade architectural complexity for sample efficiency*.

- **[[2605.10993|ECHO-VLA]]** — ==hierarchical hyperbolic memory (HAE)== + autonomous memory consolidation; cone-tree retrieval + virtual-memory interpolation; **+12.8pp** LIBERO-Long.
- **[[2510.02298|ARMADA]]** — autonomous failure detection + multi-robot shared control; ==adaptive rewinding== collects high-quality corrective demos.
- **[[2603.09030|PlayWorld]]** — autonomous ==VLM Task Proposer + VLA Executer== self-play loop + ==Stable-Video-Diffusion== backbone finetuned via ==curriculum learning== on diverse contact-rich play; captures failure modes (slips, missed grasps) absent in human data, **Pearson 0.8766** predicted-vs-real SR correlation, **+65%** real-world SR via in-model fine-tune.

**Self-Evolving VLA — Decision Matrix**

| Need | Recommendation |
|---|---|
| End-to-end self-evolving VLA (with stage verification) | [[2511.16166\|EvoVLA]] (**+10.2pp** sim, **+11.0pp** Sim2Real) |
| Sequential RL without forgetting (proven baseline) | [[2603.03818\|VLA CL]] (near-zero NBT, **2%** replay) |
| Conservative SFT for full-param fine-tune | [[2605.08879\|ConSFT]] (**34%** LIBERO retention vs collapse) |
| Online RL + SFT alternation with LoRA | [[2501.16664\|iRe-VLA]] |
| Persistent hierarchical memory (hyperbolic) | [[2605.10993\|ECHO-VLA]] (**+12.8pp** LIBERO-Long) |
| Multi-robot shared-control corrective demos | [[2510.02298\|ARMADA]] |
| Skill abstraction + SG-MoE for many tasks | [[2603.07648\|AtomicVLA]] |
| Lifetime continual deployment | [[2602.10503\|Long-Lived Robots]] / [[2602.03445\|CRL-VLA]] |
| Residual RL data generation | [[2511.00091\|PLD]] |
| Self-play data engine for VLA training | [[2603.09030\|PlayWorld]] |

> [!star] Key Papers
> - [[2511.16166|EvoVLA]] — First end-to-end self-evolving VLA; solves ==stage hallucination== (**38.5% → 14.8%**) + fragile memory; **+10.2pp** sim, **+11.0pp** Sim2Real, **1.5×** sample efficiency.
> - [[2603.03818|VLA Continual Learning]] — The continual-learning surprise: pretrained VLAs are *naturally* forgetting-resistant; **2–4×** lower NBT, only **2%** replay needed; skills recovered in **<10%** of original training steps.
> - [[2605.08879|ConSFT]] — Closes the SFT-side gap: exponential conservative weight bounds parameter disruption; **34%** LIBERO / **28%** RoboTwin retention with no prior data and no architectural mods.
> - [[2605.10993|ECHO-VLA]] — Canonical memory-augmented path: hyperbolic HAE + cone-tree retrieval; **+12.8pp** LIBERO-Long without weight updates.

> [!tip] The Continual Learning Surprise (and How to Compose It)
> Two independent studies ([[2603.03818|VLA CL]], [[2603.11653|VLA RL CL]]) found the same result: VLAs pretrained on diverse data are *naturally* resistant to catastrophic forgetting. You don't need complex continual-learning algorithms — simple sequential RL fine-tuning with ==LoRA== works. This is the opposite of what the NLP literature suggests, and makes VLA self-evolution much more practical than expected. Compose it with [[2605.08879|ConSFT]] for the SFT side and [[2605.10993|ECHO-VLA]] for memory; the three together cover the loop without rebuilding the VLA backbone. Cross-reference [[03_VLA#9. Self-Evolving & Continual VLAs]] for the VLA-side continual recipes in depth, [[04_WAM#7. Self-Evolving WAMs]] for the WAM-side dynamics-evolution counterparts, and [[09_Egocentric-Pretraining-and-Human-Video#1. Why Egocentric Pretraining Now]] for the egocentric pretraining that produces the broad parameter basin in the first place.

---

### 7. Self-Evolving Embodied Agents

Agents that go beyond weight updates to evolve their *behavior* — distilling interaction trajectories into reusable strategies, building skill libraries, and co-evolving with their environments. The cluster organizes by *what gets evolved*: distilled experience principles (memory-only, no weight updates), policy-environment co-evolution (curriculum-driven), or curriculum-guided structural evolution (tree search, environment synthesis).

#### 7.1 Experience Distillation & Memory-Driven Evolution

Distill raw interaction history into reusable structures — strategic principles, experience cards, skill libraries — and condition future behavior on retrieved memory. Weights stay frozen; the agent evolves through accumulated knowledge.

- **[[2510.16079|EVOLVER]]** — extracts structured ==experience cards== per episode (*what happened / what worked / what failed / strategic principle*); cards accumulate in a persistent bank that conditions future behavior on retrieved principles — *weights stay frozen, behavior evolves through accumulated knowledge*.
- **[[2508.02085|SE-Agent]]** — Treats reasoning trajectories as ==genotypes==: ==Revision== (multi-planning + mutation + reflection), ==Recombination== (crossover + transfer + global restructuring), ==Refinement== (multi-dimensional reward selection); SOTA on SWE-bench Verified across 5 LLMs with **+112% Pass@1** for Llama-3.1-70b (**15.4% → 32.6%**) and **+80%** for GPT-4o (**22.4% → 40.4%**).
- **[[2604.11306|Hierarchical Episodic Memory]]** — hierarchical episodic memory with ==relevance-based forgetting==; long-horizon agent memory.
- **[[2409.00872|SAGE]]** — ==Three-agent architecture (User / Assistant / Checker)== + ==dual-memory (Short / Long-Term)== with ==MemorySyntax== optimization (==Ebbinghaus forgetting curve== prioritizes retention); iterative feedback converges to ==Nash equilibrium==; GPT-3.5 Database **2.26×** gain, Qwen-1.8B **+57.7%–100%**, HotpotQA **+20.8%**, ALFWorld Mistral-7b **+17.3%**, RAG memory **−50%** without latency hit.
- **[[2603.18743|Memento-Skills]]** — Externalizes learning into a ==structured-markdown skill library== with ==closed-loop Read–Write Reflective Learning (SRDP)==; ==behavior-aligned skill router (Memento-Qwen)== trained via ==one-step offline RL + multi-positive InfoNCE==; GAIA **+13.7pp** (**52.3% → 66.0%**), HLE **17.9% → 38.7%**; router **Recall@1 0.60** (vs **0.32** BM25).
- **[[2603.05218|KARL]]** — Databricks knowledge agent + ==KARLBench== (6 enterprise search regimes); trained via ==OAPL== (Optimal Advantage-based Policy Optimization with Lagged Inference, large-batch off-policy RL) on an ==agentic synthesis pipeline==; Pareto-optimal vs Claude 4.6 / GPT 5.2 at lower cost/latency, **−37%** search trajectory length, **+37%** unique-document retrieval on BrowseComp-Plus.

#### 7.2 Policy ↔ Environment Co-Evolution

Policy and environment evolve together — environment generates tasks calibrated to the agent's capability frontier; as the agent improves, the environment ramps difficulty. Creates an ==open-ended curriculum== without manual task design.

- **[[2601.06794|ECHO]]** — environment + policy co-evolve via ==saturation-aware reward==; environment generates tasks calibrated to the agent's *current capability frontier* — hard enough to challenge, easy enough to be solvable; tasks retire and harden once SR crosses threshold; canonical co-evolution loop.
- **[[2604.18292|Agent-World]]** — ==Agentic Environment-Task Discovery==; mines themes, generates verifiable tools, synthesizes tasks. **65.4%** τ²-Bench, **55.8%** BFCL V4, **38.1%** MCP-Mark; scaling 0 → 1,978 envs lifts score **18.4% → 38.5%**.
- **[[2604.18131|Native Evolution]]** — spontaneous ==reward-free self-evolution== via world-knowledge exploration; **+19% abs** SR (40.91% vs 22.04% on WebWalker), **17%** efficiency gain.
- **[[2604.10096|ABot-Claw]]** — Alibaba's OpenClaw extension: ==decoupled 3-layer architecture (OpenClaw / Shared Service / Robot Embodiment)== with ==unified ROS-based interface== for heterogeneous embodiments, ==visual-centric cross-embodiment multimodal memory== (keyframes + object-centric + place anchors), and ==generalist-reward critic== closed-loop feedback; demonstrates cross-embodiment task reassignment when one robot fails (humanoid → quadruped).
- **[[2604.10892|HECTOR]]** — Three-layer human-fleet framework with ==receding-horizon, automaton-guided search tree== for joint task decomposition / team formation + ==MILP== for robot instantiation + ==bidirectional multimodal GUI==; **34.6s** avg mission response with **100%** SR over 8 baselines, **<2.0s** planning time scaling to **170 robots / 100 missions / 1509 subtasks**.

#### 7.3 Curriculum & Structural Self-Evolution

Evolve the *training process itself* — tree-search RL, curriculum-guided exploration, governed module versioning. The structural axis: agents modify what they learn next, not just how they act now.

- **[[2506.21669|SEEA-R1]]** — tree-structured RL with self-trained ==MGRM== reward model; **+24%** via MCTS; **46.27%** ALFWorld MLLM (vs GPT-4o's **24%**), **85.07%** text-only.
- **[[2604.26707|CurEvo]]** — Iterative loop with ==Curriculum-Guided Self-Evolution + Multi-Dimensional Question Generation + Type-Adaptive Evaluation== over 3 cognitive dimensions (==structural perception / semantic recognition / reasoning understanding==); ==adaptive sampling ratios + sample weighting== shift retention from perception → reasoning across iterations; **+4.05%** acc on LLaVA-OneVision/NExT-QA across 7 Video-LLM backbones / 4 VideoQA benchmarks.
- **[[2601.07055|Dr. Zero]]** — Meta's data-free search agent; ==HRPO== cuts rollout cost **~4×** vs GRPO; **+22.9%** EM on Natural Questions.
- **[[2604.07799|ECM]]** — modular, versioned ==capability modules== with runtime governance; **32.4% → 91.3%** SR over 20 evolution iterations, blocks **100%** unsafe actions at **2.3 ms** overhead.
- **[[2603.24350|Emergent Self]]** — Columbia quadruped trained with ==Soft Actor-Critic== sequentially on (walk / wiggle / bob); ==neuron co-activation analysis== reveals a dominant first-hidden-layer subnetwork with **+16.9 pp** higher mean persistence across behaviors (p < **0.001**) vs constant-task baselines — the "self" emerges spontaneously as the invariant cognitive substrate that survives behavior switches with smaller reorganization than task-specific regions.
- **[[2603.04029|Self-Adapting RL]]** — WM ==residuals== trigger targeted self-adaptation; real F1Tenth adapts to friction shift in **10K** real-world steps (**8 min**).
- **[[2509.19292|SOE]]** — action-level probing via ==variational information bottleneck==; **50.8%** relative SR improvement, fewer rollouts than baselines.

**Self-Evolving Agent — Decision Matrix**

| Need | Recommendation |
|---|---|
| Experience-driven lifecycle (no weight updates) | [[2510.16079\|EVOLVER]] (strategic-principle distillation) |
| Open-ended curriculum via env co-evolution | [[2601.06794\|ECHO]] (saturation-aware reward) |
| Scaled environment synthesis (0 → 2K envs) | [[2604.18292\|Agent-World]] (**+~2×** score from env scaling) |
| Reward-free self-evolution via world knowledge | [[2604.18131\|Native Evolution]] (**+19% abs** SR, **17%** efficiency) |
| Tree-RL with verifiable reward + MCTS | [[2506.21669\|SEEA-R1]] (**46.27%** ALFWorld vs GPT-4o's **24%**) |
| Data-free search-agent self-evolution | [[2601.07055\|Dr. Zero]] (HRPO **4×** cheaper than GRPO) |
| Modular versioned capabilities + safety governance | [[2604.07799\|ECM]] (**91.3%** SR, **100%** unsafe blocked, **2.3 ms**) |
| Curriculum-guided video understanding | [[2604.26707\|CurEvo]] |
| Hierarchical episodic memory (forgetting-aware) | [[2604.11306\|Hierarchical Episodic Memory]] |
| Real-world targeted self-adaptation from WM residual | [[2603.04029\|Self-Adapting RL]] (F1Tenth in **8 min**) |
| Action-level VIB probing for self-improvement | [[2509.19292\|SOE]] (**50.8%** relative SR gain) |
| Multi-agent / fleet-scale co-evolution | [[2604.10096\|ABot-Claw]] / [[2604.10892\|HECTOR]] |
| Reflective + memory-augmented agent | [[2409.00872\|SAGE]] |
| External skill / knowledge storage | [[2603.18743\|Memento-Skills]] / [[2603.05218\|KARL]] |

> [!star] Key Papers
> - [[2510.16079|EVOLVER]] — Canonical experience-distillation lifecycle: raw trajectories → strategic principles → behavior evolution without weight updates. The cleanest illustration of agent-side self-evolution.
> - [[2601.06794|ECHO]] — Canonical environment co-evolution: ==saturation-aware reward== ramps difficulty automatically; open-ended curriculum without manual task design.
> - [[2604.18292|Agent-World]] — Canonical scaling result: 0 → 1,978 environments lifts representative tool-use score **18.4% → 38.5%** — the data substrate for agent-level self-evolution.
> - [[2506.21669|SEEA-R1]] — Canonical tree-RL path: MGRM + MCTS beats GPT-4o on ALFWorld (**46.27% vs 24%**); **+34.72% abs** in real-world physical experiments.
> - [[2604.18131|Native Evolution]] — Recent paradigm shift: spontaneous ==reward-free== self-evolution via world-knowledge exploration; **+19% abs** SR on WebWalker.

> [!tip] From Weight Updates to Behavior Evolution
> Self-improving models optimize weights; self-evolving agents optimize *behavior*. The key difference is persistent experience: [[2510.16079|EVOLVER]] and [[2601.06794|ECHO]] show that distilling interaction history into reusable principles is what turns a self-improving model into a self-evolving agent. [[2603.18743|Memento-Skills]] and [[2603.05218|KARL]] extend this with external skill/knowledge storage; [[2604.18292|Agent-World]] proves the substrate scales with environment count, not just model size; [[2604.18131|Native Evolution]] removes the reward-signal requirement entirely. The 2026 arc: from "RL self-improvement" to "world-knowledge-driven evolution" — and the bridge is *memory*, not gradient. Cross-reference [[11_Self-Evolving-AI#4. Self-Evolving Agents]] for the broader self-evolving landscape beyond embodied agents, [[04_WAM#7. Self-Evolving WAMs]] for WAM-driven self-evolution, and [[03_VLA#9. Self-Evolving & Continual VLAs]] for the VLA continual-learning counterpart.

---

## Part C — Open Problems & Failure Modes

*Where self-evolution fails: misevolution, reward hacking, capability drift.*

### 8. Open Problems & Failure Modes

Self-evolution is not guaranteed to converge or remain aligned. The failure modes documented in the literature cluster along two axes: *what goes wrong inside the policy* (forgetting, collapse, drift) versus *what goes wrong in the imagination substrate the policy trains on* (hallucinated dynamics, artifact exploitation). Each cluster has a different remediation path — alignment safeguards for the first, dream-quality filters for the second.

#### 8.1 Value Drift & Alignment Failures

The agent's reward signal silently diverges from designer intent during autonomous improvement — invisible until deployment failure. The axis: *the reward, not the policy, is what fails*.

- **[[2509.26354|Misevolution]]** — identifies ==value drift during autonomous self-improvement== as a novel safety-risk class; systematic biases in the self-reward model (e.g., rewarding confident-looking actions over cautious ones) amplify over improvement rounds until the agent optimizes a proxy that diverges from the true goal — *invisible until deployment failure*.
- **[[2506.07468|SELF-REDTEAM]]** — ==adversarial self-play== as a pre-deployment safety check; the model red-teams itself after each improvement cycle to catch safety regressions before deployment.

#### 8.2 Policy Pathologies (Collapse & Forgetting)

The policy itself degenerates — either narrowing to a brittle deterministic mode (entropy collapse) or losing prior skills as new ones are learned (catastrophic forgetting). The axis: *RL pressure without counter-pressure*.

- **[[2509.15194|EVOL-RL]]** — ==novelty-driven diversity== alongside performance-based selection prevents *entropy collapse* (RL convergence on a narrow high-reward mode; policy becomes deterministic and brittle to variation) during RL-based self-improvement.
- **Catastrophic forgetting** — gains from one round of self-improvement are lost in the next domain; mitigated by LoRA ([[2603.11653|VLA RL CL]]) and experience replay ([[2401.16650|WMAR]]: forgetting **0.071 vs 0.665** baseline). See §6 for the surprising-but-replicated VLA-side result that pretraining alone provides ==natural== forgetting resistance.

#### 8.3 Imagination Pathologies (Hallucinated Dynamics)

The world model the agent trains on predicts physically impossible futures; the policy exploits artifacts that don't exist in the real world. The axis: *dream fidelity gates self-evolution gains*.

- **[[2603.23376|ABot-PhysWorld]]** — ==Diffusion-DPO== on physics-preference pairs suppresses implausible predictions (object penetration, anti-gravity); the canonical dream-quality filter for VideoGen WAMs. See [[07_Physics-Aware-Embodied-AI#1. Design-Space Principles]] for the full physics-aware design space.
- **Artifact exploitation** — without a critic, agents find unrealistic shortcuts in generated rollouts; [[2603.08403|SPIRAL]]'s ==CriticAgent== (§5.1) and [[2502.05907|EvoAgent]]'s self-reflection (§5.1) are the two operational fixes.

**Failure Mode — Decision Matrix**

| Failure Mode | Risk | Remediation |
|---|---|---|
| Value drift / misevolution | Reward model bias amplifies over rounds; deployment-time failure | [[2506.07468\|SELF-REDTEAM]] (adversarial self-play after each cycle) |
| Catastrophic forgetting | Prior-skill loss across task stream | LoRA + replay ([[2603.11653\|VLA RL CL]]); [[2401.16650\|WMAR]] for [[2301.04104\|DreamerV3]] (forgetting **0.071 vs 0.665**) |
| Entropy collapse | Policy narrows to brittle deterministic mode | [[2509.15194\|EVOL-RL]] (novelty-driven diversity pressure) |
| Hallucinated dynamics | WM predicts physically impossible futures | [[2603.23376\|ABot-PhysWorld]] (Diffusion-DPO); see [[07_Physics-Aware-Embodied-AI#3. Explicit Physics Losses for Video Generation]] |
| Artifact exploitation | Policy exploits unrealistic dream artifacts | Critic in loop: [[2603.08403\|SPIRAL]]'s CriticAgent / [[2502.05907\|EvoAgent]]'s self-reflection |
| Reward hacking | Self-play finds reward shortcuts | [[2506.07468\|SELF-REDTEAM]] (adversarial self-play detection) |
| Inference latency (WM at deploy time) | Imagination loops too slow for real-time control | Strip WM at deploy ([[2603.16666\|Fast-WAM]]); see [[04_WAM#6. Efficient & Action-Centered WAMs]] |
| Cross-domain forgetting | Skills lost when moving to new env | Persistent experience memory ([[2510.16079\|EVOLVER]], [[2605.10993\|ECHO-VLA]]) |

> [!star] Key Papers
> - [[2509.26354|Misevolution]] — Identifies ==value drift during autonomous self-improvement== as a novel safety-risk class; the first paper to name the phenomenon.
> - [[2506.07468|SELF-REDTEAM]] — Canonical pre-deployment safety check: model red-teams itself via adversarial self-play after each improvement cycle.
> - [[2509.15194|EVOL-RL]] — Novelty-driven diversity prevents ==entropy collapse== during RL-based self-improvement; the operational fix for policy narrowing.
> - [[2603.23376|ABot-PhysWorld]] — Canonical dream-quality filter: ==Diffusion-DPO== on physics-preference pairs suppresses implausible WM predictions; the physics-aware safeguard.

> [!tip] The Safety Imperative — Two Distinct Layers
> Self-evolving systems need built-in safety checks at *two* layers: the *reward layer* (detect value drift via [[2509.26354|Misevolution]]; mitigate via [[2506.07468|SELF-REDTEAM]] adversarial self-play) and the *imagination layer* (filter hallucinated dynamics via [[2603.23376|ABot-PhysWorld]] DPO, [[2603.08403|SPIRAL]]'s CriticAgent, or [[2502.05907|EvoAgent]]'s self-reflection). Skipping either layer means a self-evolving system that *appears* to improve until deployment exposes the drift. Cross-reference [[07_Physics-Aware-Embodied-AI#6. Physics Commonsense Benchmarks]] for physics-aware methods that target imagination quality at the source, [[04_WAM#9. Open Problems & Failure Modes]] for the WAM-specific failure modes, and [[11_Self-Evolving-AI#5. Self-Evolving Embodied AI]] for the broader safety-evolution literature beyond embodied AI.

---

## Quick-Reference Matrix

| Question | Answer |
|----------|--------|
| Self-evolving via imagination (WAM path)? | [[2506.24119\|SPIRAL]] + [[2502.05907\|EvoAgent]] |
| Self-evolving via RL post-training (VLA path)? | [[2511.16166\|EvoVLA]] + [[2512.14666\|EVOLVE-VLA]] |
| Self-evolving with persistent memory (Agent path)? | [[2510.16079\|EVOLVER]] + [[2601.06794\|ECHO]] |
| Need curiosity-driven exploration? | [[2503.01584\|SENSEI]] or [[2602.20057\|AdaWorldPolicy]] |
| Need denoising-as-MDP for video WAMs? | [[2603.19370\|VAMPO]] |
| Need failure detection / self-diagnosis? | [[2412.02818\|RoboMD]] + [[2510.09459\|FIPER]] |
| Need continual learning without forgetting? | [[2603.03818\|VLA Continual Learning]] (LoRA + replay) |
| Need safety red-teaming during evolution? | [[2506.07468\|SELF-REDTEAM]] |
| Need to avoid entropy collapse? | [[2509.15194\|EVOL-RL]] (novelty-driven diversity) |
| Best starting point? | Train a WAM first, *then* add self-evolution (Option 2) |

---

## Cross-References

- [[01_Embodied-AI-101]] — VLA vs WAM basics and four learning strategies
- [[03_VLA]] — VLA deep-dive (Section 9 covers self-evolving VLAs)
- [[04_WAM]] — WAM deep-dive (Section 7 covers self-evolving WAMs)
- [[05_Latent-World-Models]] — JEPA evolution lineage; latent world models as self-evolution substrate
- [[07_Physics-Aware-Embodied-AI]] — Physics priors as a stabilizer for self-evolving WAM dreams
- [[08_VLA-Reasoning-and-CoT]] — Reasoning insertion patterns relevant to self-critique and self-correction
- [[09_Egocentric-Pretraining-and-Human-Video]] — Egocentric pretraining provides robust priors that resist forgetting
- [[10_Force-Aware-and-Tactile-Policies]] — Force/tactile policies deep-dive; complements failure recovery via force feedback
- [[11_Sim-to-Real-Transfer]] — Sim-to-Real Transfer deep-dive; covers continual adaptation methods
- [[02_Dataset-Benchmark-Environment]] — Benchmarks for evaluating self-evolution

---

*See [[11_Self-Evolving-AI]] for the broader self-evolving AI landscape, or [[05_Latent-World-Models]] for how latent prediction enables imagination loops.*
