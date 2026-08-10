---
title: "Reinforcement Learning — Topic Overview"
tags:
  - RL
  - world-model
  - RLHF
  - policy-optimization
  - robotics
aliases:
  - "RL Overview"
---

# Reinforcement Learning

> [!abstract] Overview
> RL has evolved from tabular methods to the backbone of modern AI reasoning. This note traces the major threads: foundational methods and theory, model-based RL with learned world models, policy optimization algorithms, RL for LLM reasoning (the post-DeepSeek-R1 paradigm), visual and multimodal RL, reward modeling, agentic RL, RL for robotics, and self-evolving systems. Each thread feeds into the next — world models enable sample-efficient robotics; RLHF enables reasoning LLMs; and agentic RL combines both.

## Evolution Graph

```text
1. Model-Based RL   (learn a world, imagine inside it)
· latent imagination
                      +one architecture,      +scalable latent      +JEPA latent
                      many domains            MPC                   dynamics
╔════════════════╗    ┌──────────────────┐    ┌────────────────┐    ┌────────────────┐
║ Dreamer (2019) ║───►│ DreamerV3 (2023) │───►│ TD-MPC2 (2023) │───►│ TD-JEPA (2025) │
╚════════┬═══════╝    └──────────────────┘    └────────────────┘    └────────────────┘
         │    +disagreement
         │    exploration
         │    ┌─────────────────────┐
         ├───►│ Plan2Explore (2020) │
         │    └─────────────────────┘
         │    +real robots
         │    ┌───────────────────┐
         └───►│ DayDreamer (2022) │
              └───────────────────┘

2. Exploration   (what to try when reward is silent)
· intrinsic motivation
                            +curiosity from     +random network    novelty →
                            prediction error    distillation       semantic interest
┌──────────────────────┐    ┌──────────────┐    ┌─────────────┐    ┌───────────────┐
│ Pseudo-Counts (2016) │───►│ ICM (2017)   │───►│ RND (2018)  │───►│ SENSEI (2025) │
└──────────────────────┘    └──────────────┘    └─────────────┘    └───────────────┘

3. Policy Optimization   (how the update is computed)
· off-policy to offline
                  online →                +implicit         +flow
                  conservative offline    Q-learning        Q-learning
╔════════════╗    ┌──────────────────┐    ┌────────────┐    ┌────────────┐
║ SAC (2018) ║───►│ CQL (2020)       │───►│ IQL (2021) │───►│ FQL (2025) │
╚══════┬═════╝    └──────────────────┘    └────────────┘    └────────────┘
       │    +balanced policy
       │    optimization
       │    ┌──────────────┐
       └───►│ BAPO (2025)  │
            └──────────────┘

4. RL for LLM Reasoning   (reward the chain of thought)
· who scores the rationale
                   +token-level
                   rationales               +model judges itself            SFT then RL → RL only
┌─────────────┐    ┌───────────────────┐    ┌──────────────────────────┐    ╔════════════════════╗
│ STaR (2022) │───►│ Quiet-STaR (2024) │───►│ Self-Rewarding-LM (2024) │───►║ DeepSeek-R1 (2025) ║
└─────────────┘    └───────────────────┘    └─────────────┬────────────┘    ╚════════════════════╝
                                                          │    +decoupled clip
                                                          │    at scale
                                                          │    ┌─────────────┐
                                                          ├───►│ DAPO (2025) │
                                                          │    └─────────────┘
                                                          │    +zero-data self-play
                                                          │    ┌──────────────────────┐
                                                          ├───►│ Absolute-Zero (2025) │
                                                          │    └──────────────────────┘
                                                          │    +open zero recipe
                                                          │    ┌───────────────────────────┐
                                                          └───►│ Open-Reasoner-Zero (2025) │
                                                               └───────────────────────────┘

5. Reward Modeling   (where the reward itself comes from)
· outcome to process
                                                                       outcome → process
                                             +RLHF at scale            reward
┌───────────────────────────────────────┐    ┌────────────────────┐    ┌────────────────┐
│ Deep RL from Human Preferences (2017) │───►│ InstructGPT (2022) │───►│ PRM800K (2023) │
└───────────────────────────────────────┘    └──────────┬─────────┘    └────────────────┘
                                                        │    +generative
                                                        │    verifier
                                                        │    ┌─────────────────┐
                                                        ├───►│ THINKPRM (2025) │
                                                        │    └─────────────────┘
                                                        │    +reward-hacking analysis
                                                        │    ┌────────────────────────────┐
                                                        └───►│ RM-Overoptimization (2022) │
                                                             └────────────────────────────┘

6. Visual and Multimodal RL   (reward over pixels)
· perception in the loop
                       +multimodal             +perception-aware
                       reasoning RL            policy opt           +VLM RL at scale
┌─────────────────┐    ┌──────────────────┐    ┌───────────────┐    ┌────────────────┐
│ DeepEyes (2025) │───►│ MM-Eureka (2025) │───►│ PAPO (2025)   │───►│ MiMo-VL (2025) │
└─────────────────┘    └──────────────────┘    └───────────────┘    └────────────────┘

7. Agentic RL   (credit across many turns)
· beyond one response
                       +multi-turn
                       agent RL            +self-play search              +agents co-evolve
┌─────────────────┐    ┌──────────────┐    ┌─────────────────────────┐    ┌─────────────────────────┐
│ AgentGym (2024) │───►│ RAGEN (2025) │───►│ Search-Self-play (2025) │───►│ Complementary-RL (2026) │
└────────┬────────┘    └──────────────┘    └─────────────────────────┘    └─────────────────────────┘
         │    +skill library as memory
         │    ┌───────────────────────┐
         └───►│ Memento-Skills (2026) │
              └───────────────────────┘

8. RL plus Robotics   (the reward lands on hardware)
· sim to real hardware
                             +domain randomization                +real legged deployment
┌───────────────────────┐    ┌───────────────────────────────┐    ┌──────────────────────────┐
│ Visuomotor GPS (2015) │───►│ Dynamics Randomization (2017) │───►│ ANYmal-Locomotion (2020) │
└───────────────────────┘    └───────────────┬───────────────┘    └──────────────────────────┘
                                             │    +agile perceptive
                                             │    locomotion
                                             │    ┌────────────────────────┐
                                             ├───►│ Extreme Parkour (2023) │
                                             │    └────────────────────────┘
                                             │    locomotion → VLA
                                             │    post-training
                                             │    ┌─────────────────┐
                                             └───►│ RIPT-VLA (2025) │
                                                  └─────────────────┘

9. Theory and Scaling   (what the recipe actually buys)
· diagnose the recipe
┌─────────────────────────────────────┐
│ SFT-Memorizes-RL-Generalizes (2025) │─┐
└─────────────────────────────────────┘ │
                                        │    +compute-optimal recipe
                                        │    ┌───────────────────────────────────┐
                                        ├───►│ Compute-Optimal-RL-Scaling (2025) │
                                        │    └───────────────────────────────────┘
                                        │    +entropy collapse diagnosis
                                        │    ┌───────────────────────────────┐
                                        ├───►│ Entropy-Collapse-in-RL (2025) │
                                        │    └───────────────────────────────┘
                                        │    gradient →
                                        │    evolutionary search
                                        │    ┌─────────────────┐
                                        └───►│ EvoRL (2025)    │
                                             └─────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

The nine lanes divide on **what the agent is learning from**. **Model-based RL** learns a world and imagines inside it, Dreamer to DreamerV3 to TD-MPC2 to TD-JEPA, with Plan2Explore and DayDreamer branching to disagreement-driven exploration and real hardware. **Exploration** covers what to try when reward is silent, Pseudo-Counts to ICM to RND, until SENSEI swaps raw novelty for semantic interest. **Policy optimization** is about how the update is computed, SAC to CQL to IQL to FQL as the setting moves off-policy then fully offline, with BAPO branching on balance. **RL for LLM reasoning** turns on who scores the rationale, STaR using correctness, Quiet-STaR going token-level, Self-Rewarding-LM making the model its own judge, after which DAPO, Absolute-Zero, and Open-Reasoner-Zero fork three ways while the main line runs to DeepSeek-R1's pure-RL recipe. **Reward modeling** asks where the reward itself comes from, Deep RL from Human Preferences to InstructGPT to PRM800K as supervision moves from outcome to process, with THINKPRM and RM-Overoptimization branching to generative verification and reward hacking. **Visual and multimodal RL** puts perception in the loop, DeepEyes to MM-Eureka to PAPO to MiMo-VL. **Agentic RL** assigns credit across many turns, AgentGym to RAGEN to Search-Self-play to Complementary-RL, with Memento-Skills branching to a skill library as memory. **RL plus robotics** lands the reward on hardware, Visuomotor GPS to Dynamics Randomization to ANYmal-Locomotion, with Extreme Parkour and RIPT-VLA branching to agile locomotion and VLA post-training. **Theory and scaling** diagnoses the recipe rather than extending it, and the four papers are independent diagnoses rather than a succession, EvoRL among them replacing gradient descent with evolutionary search. RL-Overview sits in the table as a field reference, since it descends from nothing.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2015 | [[1504.00702\|Visuomotor GPS]] | Robotics · Sim to Real Hardware | foundational: first to fold trajectory optimization (linear-Gaussian iLQG, MPC's local cousin) into an RL loop training an end-to-end deep policy, establishing the guided-policy-search template this group builds on |
| 2016 | [[1606.01868\|Pseudo-Counts]] | Exploration · Intrinsic Motivation | Unified count-based exploration with intrinsic motivation via density-model pseudo-counts; gave novelty bonuses formal information-gain grounding |
| 2017 | [[1705.05363\|ICM]] | Exploration · Intrinsic Motivation | Defined curiosity as forward-model prediction error in a learned feature space; the most widely-cited curiosity template |
| 2017 | [[1706.03741\|Deep RL from Human Preferences]] | Reward Modeling · Outcome to Process | the origin of the paradigm: first to show a reward model learned from pairwise human preferences can drive deep RL, cutting feedback cost ~1000x |
| 2017 | [[1710.06537\|Dynamics Randomization]] | Robotics · Sim to Real Hardware | foundational method establishing training-time randomization of physical parameters combined with a recurrent policy as the classic recipe for zero-shot sim-to-real transfer |
| 2018 | [[1801.01290\|SAC]] | Policy Optimization · Off-Policy to Offline | The maximum-entropy off-policy actor-critic baseline every later method in this section is compared against; combines sample efficiency with stability on continuous control |
| 2018 | [[1810.12894\|RND]] | Exploration · Intrinsic Motivation | Random Network Distillation solved Montezuma's Revenge (22/24 rooms); resolved the "noisy-TV problem" plaguing earlier curiosity methods |
| 2019 | [[1912.01603\|Dreamer]] | Model-Based · Latent Imagination | Learned behaviors by latent imagination; pioneered training RL policies entirely within a learned world model |
| 2020 | [[2005.05960\|Plan2Explore]] | Model-Based · Latent Imagination | Self-supervised exploration via world model disagreement; zero-shot task adaptation without task-specific training |
| 2020 | [[2006.04779\|CQL]] | Policy Optimization · Off-Policy to Offline | Regularizes Q-values to be conservative on out-of-distribution actions, achieving 2-5x higher returns on multi-modal D4RL benchmarks and solving previously intractable domains like AntMaze |
| 2020 | [[2010.11251\|ANYmal-Locomotion]] | Robotics · Sim to Real Hardware | foundational teacher-student RL controller pioneering zero-shot sim-to-real proprioceptive locomotion, validated with zero failures in the DARPA Subterranean Challenge |
| 2021 | [[2110.06169\|IQL]] | Policy Optimization · Off-Policy to Offline | Never queries out-of-distribution actions at all, using expectile regression to implicitly estimate max Q-values; excels at stitching suboptimal trajectories on long-horizon navigation |
| 2022 | [[2203.02155\|InstructGPT]] | Reward Modeling · Outcome to Process | the canonical SFT to reward model to PPO recipe the field still cites, where a 1.3B aligned model beat a 175B unaligned one |
| 2022 | [[2203.14465\|STaR]] | LLM Reasoning · Who Scores the Rationale | Self-taught reasoner bootstrapping its own rationales; created a self-improvement flywheel for LLM reasoning |
| 2022 | [[2206.14176\|DayDreamer]] | Model-Based · Latent Imagination | First deployment of Dreamer on real robots; proved sample-efficient learning from imagination works physically |
| 2022 | [[2210.10760\|RM-Overoptimization]] | Reward Modeling · Outcome to Process | derives scaling laws for Goodhart's Law in RLHF, showing exactly how optimizing against a proxy reward model degrades true performance |
| 2023 | [[2301.04104\|DreamerV3]] | Model-Based · Latent Imagination | Mastered diverse domains with a single world model architecture; fixed-hyperparameter generalist agent |
| 2023 | [[2305.20050\|PRM800K]] | Reward Modeling · Outcome to Process | the founding paper of process supervision itself, still the clearest case for why step-level feedback beats final-answer-only reward |
| 2023 | [[2309.14341\|Extreme Parkour]] | Robotics · Sim to Real Hardware | landmark end-to-end vision-to-action policy (dual distillation, self-inferred heading) that pushed legged parkour to 2x-body jumps and handstands on cheap hardware, defining the paradigm most later parkour work builds on |
| 2023 | [[2310.16828\|TD-MPC2]] | Model-Based · Latent Imagination | Scalable model-based RL: a single world model architecture masters 300+ continuous control tasks across domains |
| 2024 | [[2401.10020\|Self-Rewarding-LM]] | LLM Reasoning · Who Scores the Rationale | Single model acts as both generator and judge via iterative DPO; broke the human-feedback bottleneck |
| 2024 | [[2403.09629\|Quiet-STaR]] | LLM Reasoning · Who Scores the Rationale | Extended STaR to think before every token via internal rationales; token-level self-improvement |
| 2024 | [[2406.04151\|AgentGym]] | Agentic RL · Beyond One Response | Multi-environment agent evolution via behavioral cloning + self-evolution; generalist agent training |
| 2024 | [[2412.05265\|RL-Overview]] | Reference · Field Overview | Kevin Murphy's comprehensive modern overview; the definitive reference for RL fundamentals |
| 2025 | [[2501.12948\|DeepSeek-R1]] | LLM Reasoning · Who Scores the Rationale | Showed reasoning emerges from pure outcome-based RL alone; established the multi-stage SFT+RL+distillation pipeline the field now builds on |
| 2025 | [[2501.15129\|EvoRL]] | Theory · Diagnose the Recipe | JAX-based GPU-accelerated framework achieving 60x speedup for evolutionary RL |
| 2025 | [[2501.17161\|SFT-Memorizes-RL-Generalizes]] | Theory · Diagnose the Recipe | Landmark finding: SFT makes models memorize training distributions, while RL makes them generalize to unseen problems |
| 2025 | [[2502.02538\|FQL]] | Policy Optimization · Off-Policy to Offline | Foundational flow-matching offline RL method; one-step distillation from a BC flow policy avoids BPTT, the baseline every other paper here compares against |
| 2025 | [[2503.01584\|SENSEI]] | Exploration · Intrinsic Motivation | Semantic exploration with epistemic uncertainty + Go-Explore for versatile world models |
| 2025 | [[2503.07365\|MM-Eureka]] | Visual RL · Perception in the Loop | strongest reported results in the group (74.8 MathVista, 73.4 WeMath) via rule-based RL with online filtering, plus a fully open-sourced dataset/model/code release |
| 2025 | [[2503.14476\|DAPO]] | LLM Reasoning · Who Scores the Rationale | Open-source RL system at scale for LLM reasoning; decoupled clip-higher and dynamic sampling |
| 2025 | [[2503.24290\|Open-Reasoner-Zero]] | LLM Reasoning · Who Scores the Rationale | First comprehensive open-source reproduction of R1-Zero; reference implementation for the field |
| 2025 | [[2504.16828\|THINKPRM]] | Reward Modeling · Outcome to Process | Generative PRM enabling LLMs to provide verbalized, step-level evaluation |
| 2025 | [[2504.20073\|RAGEN]] | Agentic RL · Beyond One Response | Multi-turn RL training for LLM agents; established the paradigm for sustained agent-environment interaction |
| 2025 | [[2505.03335\|Absolute-Zero]] | LLM Reasoning · Who Scores the Rationale | Zero-data self-play RL; model proposes tasks, solves, verifies via code, and retrains with no human data |
| 2025 | [[2505.14362\|DeepEyes]] | Visual RL · Perception in the Loop | VLMs perform "thinking with images" by dynamically integrating visual re-observation into reasoning |
| 2025 | [[2505.17016\|RIPT-VLA]] | Robotics · Sim to Real Hardware | first in this group to formalize interactive post-training as a third training stage, turning near-zero single-demonstration SFT into 80-90% success via critic-free RLOO+PPO |
| 2025 | [[2505.22617\|Entropy-Collapse-in-RL]] | Theory · Diagnose the Recipe | Identifies universal policy entropy collapse in RL for LLMs; a key failure mode to watch for |
| 2025 | [[2506.03569\|MiMo-VL]] | Visual RL · Perception in the Loop | Xiaomi's 7B model achieving SOTA visual reasoning; proves small models can reason |
| 2025 | [[2507.06448\|PAPO]] | Visual RL · Perception in the Loop | traced 67% of MLLM reasoning errors to bad perception and folded a perception-aware KL loss directly into GRPO/DAPO |
| 2025 | [[2508.14881\|Compute-Optimal-RL-Scaling]] | Theory · Diagnose the Recipe | Establishes compute-optimal power laws for value-based deep RL and identifies TD-overfitting |
| 2025 | [[2510.00739\|TD-JEPA]] | Model-Based · Latent Imagination | Temporal-difference JEPA learns policy-conditioned multi-step latents for zero-shot RL; SOTA across 65 tasks, strong on pixel-based observations |
| 2025 | [[2510.18821\|Search-Self-play]] | Agentic RL · Beyond One Response | +26.4 points average for Qwen2.5-7B-Base via a genuine proposer/solver co-evolution loop |
| 2025 | [[2510.18927\|BAPO]] | Policy Optimization · Off-Policy to Offline | Adaptive clipping re-balances positive/negative gradient signals to preserve entropy under off-policy staleness, hitting SOTA 87.1 on AIME 2024 among open-source models |
| 2026 | [[2603.17621\|Complementary-RL]] | Agentic RL · Beyond One Response | Co-evolutionary RL framework where multiple agents improve each other through complementary objectives |
| 2026 | [[2603.18743\|Memento-Skills]] | Agentic RL · Beyond One Response | Skill library as external memory; agents evolve without parameter updates, +13.7pp on GAIA |

---

## 1. Foundations, Surveys & Theory

The theoretical bedrock of RL — comprehensive overviews, taxonomies, and fundamental theoretical contributions that define the field's vocabulary, scope, and open problems.

**LLM Reasoning & Post-Training Surveys** — Surveys mapping RL-driven reasoning, self-improvement, fine-tuning, and distillation methods for LLMs.
- [[2604.00626|On-Policy-Distillation-Survey]], [[2603.25681|LLM-Self-Improvement-Survey]], [[2601.12538|Agentic-Reasoning-Survey]], [[2512.16301|Agentic-AI-Adaptation-Survey]], [[2511.18538|Code-Intelligence-Survey]], [[2509.08827|RL-for-LRM-Survey]], [[2509.02547|Agentic-RL-Landscape-Survey]], [[2505.02665|Slow-Thinking-LLM-Survey]], [[2505.00551|DeepSeek-R1-Replication-Survey]], [[2504.09037|LLM-Reasoning-Frontiers-Survey]], [[2501.09686|Large-Reasoning-Models-Survey]], [[2501.09223|LLM-Foundations]], [[2410.19878|PEFT-Methodologies-Survey]], [[2408.13296|LLM-Fine-Tuning-Guide]], [[2303.18223|LLM-Survey]]

> [!star] Key Papers
> - [[2501.09686|Large-Reasoning-Models-Survey]] — First survey to formalize the "Large Reasoning Model" paradigm right after OpenAI's o1; frames the field's train-time and test-time scaling axes
> - [[2509.08827|RL-for-LRM-Survey]] — Most comprehensive post-DeepSeek-R1 synthesis of RL for reasoning; decomposes the pipeline into reward design, policy optimization, and sampling strategy
> - [[2603.25681|LLM-Self-Improvement-Survey]] — Clearest unifying framework for self-improvement, proposing a closed-loop lifecycle tying fine-tuning and distillation into one picture
> - [[2501.09686|Large-Reasoning-Models-Survey]] — First systematic survey of RL-based reasoning in LLMs; maps the post-DeepSeek-R1 landscape

**Multimodal, Robotics & Foundational RL Surveys** — Surveys spanning multimodal reasoning, robot learning, and core RL theory/tooling.
- [[2608.02433|SAC-MRAC]], [[2607.06935|Mathematical Methods of RL]], [[2607.06706|VLA for UAVs and Bimanual Manipulation Review]], [[2603.24517|AVO]], [[2510.12403|Robot-Learning-Tutorial]], [[2510.02665|MLLM-Self-Improvement-Survey]], [[2508.08189|RL-for-Large-Models-Survey]], [[2506.06981|ForageWorld]], [[2505.04921|LMRM-Survey]], [[2504.21277|Reinforced-MLLM-Survey]], [[2504.03151|Multimodal-Reasoning-Survey]], [[2503.14576|SocialJax]], [[2502.08938|exp-a-spiel]], [[2501.02189|VLM-SOTA-Survey]], [[2412.06531|RL-Memory-Taxonomy]], [[2412.05265|RL-Overview]], [[2408.07666|Model-Merging-in-LLMs/MLLMs]]

> [!star] Key Papers
> - [[2412.05265|RL-Overview]] — Sutton's comprehensive modern overview; the definitive reference for RL fundamentals
> - [[2508.08189|RL-for-Large-Models-Survey]] — Comprehensive mapping of visual RL applied to large multimodal models

**Causal RL** — Connecting causal inference with RL to enable more principled and generalizable decision-making.
- [[2607.26336|Implicit Causal WM]], [[2507.14901|Causal-Model-Reduction]], [[2307.01452|Causal-RL-Roadmap]], [[2302.05209|Causal-RL-Methods-Survey]], [[2210.13066|DaXBench]], [[2104.03311|PlasticineLab]]

> [!star] Key Papers
> - [[2302.05209|Causal-RL-Methods-Survey]] — First comprehensive taxonomy connecting causal inference with RL

**Continual & Lifelong RL** — Agents that learn across sequential tasks without catastrophic forgetting.
- [[2607.24996|CPR]], [[2607.05609|Predictive Continual Learning]], [[2605.12484|FST]], [[2603.24350|Emergent-Self]], [[2603.00903|Continual-RL-Theory]], [[2506.21872|Continual-RL-Survey]], [[2503.18684|OMLA]], [[2503.10949|SCDA]], [[2502.15922|Safe-EWC]], [[2410.19925|MLLM-Continual-Learning]], [[2410.07812|TD-VCL]], [[2105.10919|Continual-World]], [[1612.00796|EWC]]

> [!star] Key Papers
> - [[1612.00796|EWC]] — Foundational method for overcoming catastrophic forgetting; Elastic Weight Consolidation remains the baseline for all continual learning
> - [[2506.21872|Continual-RL-Survey]] — First comprehensive survey dedicated to continual RL; defines the taxonomy and open problems

**Classic & Foundational Meta-RL** — Gradient-based fast adaptation, task representations, and successor-feature methods for learning-to-learn.
- [[2509.01297|DMCM]], [[2506.10085|VITA-Value]], [[2505.00787|Option-Keyboard-Basis]], [[2305.17250|RaMP]], [[2301.08028|Meta-RL-Tutorial]], [[2103.07945|Forward-Backward-Representation]], [[1910.10897|Meta-World]], [[1903.08254|PEARL (Probabilistic Context Meta-RL)]], [[1803.11347|GrBAL]], [[1703.03400|MAML]], [[1606.05312|Successor Features]]

> [!star] Key Papers
> - [[1703.03400|MAML]] — Foundational gradient-based meta-learning algorithm; learns an initialization that adapts to new tasks in 1-3 gradient steps
> - [[1903.08254|PEARL (Probabilistic Context Meta-RL)]] — Clearest exemplar of task-representation meta-RL; probabilistic latent context gives 20-100x sample-efficiency over MAML
> - [[1606.05312|Successor Features]] — Classic framework decoupling dynamics from reward via Generalized Policy Improvement for instant reward-transfer
> - [[2301.08028|Meta-RL-Tutorial]] — Definitive tutorial unifying meta-RL definitions and algorithms; essential reference for the sub-field
> - [[2305.17250|RaMP]] — Random-feature Q-basis decoupling reward from dynamics; rapid online task adaptation via linear combination of pre-learned Q-bases

**In-Context, Multi-Objective & Constrained Meta-RL** — Transformer/in-context meta-RL plus multi-objective and constrained task-adaptation variants.
- [[2605.10899|RubricEM]], [[2604.24532|MORL-FB]], [[2604.05112|Vintix-II]], [[2601.21845|Constrained-Meta-RL]], [[2512.16848|LAMER]], [[2510.20264|OpTI-BFM]], [[2509.24923|Meta-Bandit-Exploitation-Bias]], [[2509.18389|ICRL-Emergence]], [[2508.16027|Transformer-Non-Stationary-RL]], [[2506.13690|MASP]], [[2506.06303|LLM-In-Context-RL]], [[2506.05426|T2MIR]], [[2506.01299|In-Context-Q-Learning]], [[2502.04979|Bandit-Prompt-Tuning-DT]], [[2502.03752|SISL]], [[2502.02869|OmniRL]]

**Evolutionary Strategies vs Deep RL** — Comparative analysis of gradient-free vs gradient-based approaches to policy optimization.
- [[2606.29082|EFT]], [[2604.07725|Squeeze-Evolve]], [[2602.00170|Blessing-of-Dimensionality-LLM]], [[2509.26354|Misevolution]], [[2509.24372|Evolution-Strategies-at-Scale]], [[2501.15129|EvoRL]], [[2402.06912|ES-Linear-Policy]], [[2110.01411|DRL-vs-ES-Survey]], [[1803.07055|ARS]], [[1703.03864|OpenAI ES]]

> [!star] Key Papers
> - [[2501.15129|EvoRL]] — JAX-based GPU-accelerated framework achieving 60x speedup for evolutionary RL
> - [[2602.00170|Blessing-of-Dimensionality-LLM]] — Explains why evolution strategies work for LLM fine-tuning with small populations

**RL Scaling Laws & Compute-Optimal Training** — Empirical scaling laws and compute-allocation studies for RL and RLHF training.
- [[2607.16097|Pretraining-RL Scaling Law]], [[2510.13786|Scaling-RL-Compute]], [[2508.14881|Compute-Optimal-RL-Scaling]], [[2503.22230|RLHF-Data-Scaling]], [[2412.11979|AlphaZero-Scaling-Laws]], [[2104.08212|MT-Opt]], [[1812.06162|Large-Batch-Training]], [[1507.04296|Gorila]]

> [!star] Key Papers
> - [[2510.13786|Scaling-RL-Compute]] — First predictive sigmoidal compute-performance framework for LLM RL, validated at 100,000 GPU-hours
> - [[2607.16097|Pretraining-RL Scaling Law]] — First joint pretraining-RL scaling law; shows optimal RL compute share grows with total budget
> - [[2508.14881|Compute-Optimal-RL-Scaling]] — Establishes compute-optimal power laws for value-based deep RL and identifies TD-overfitting
> - [[1812.06162|Large-Batch-Training]] — OpenAI's gradient noise scale; foundational for understanding batch size in deep RL

**Training Dynamics, Plasticity & Failure Modes** — What happens inside the optimizer during RL training — plasticity loss, entropy collapse, gradient stability, and SFT/RL spectral differences.
- [[2607.16051|Loopie]], [[2604.01913|Plasticity-Sample-Weight-Decay]], [[2510.11495|RL-After-NTP]], [[2510.00553|RL-Dynamics-Predictability]], [[2509.21128|RL-Squeezes-SFT-Expands]], [[2508.16546|SFT-vs-RL-Spectral-Analysis]], [[2507.06187|Delta-Learning-Hypothesis]], [[2506.15544|Stable-Gradients-RL]], [[2505.24061|GraMa]], [[2505.22617|Entropy-Collapse-in-RL]], [[2505.17749|Pixel-RL-Scale-GAP]], [[2412.01951|Sharpening-Mechanism]], [[2410.17517|Maynard-Cross-Learning]], [[2407.10490|LLM-Finetuning-Dynamics]], [[2405.16158|BRO]], [[2402.12479|Pruned-Networks-in-Deep-RL]], [[2310.19668|DrM]]

> [!star] Key Papers
> - [[2505.22617|Entropy-Collapse-in-RL]] — Identifies universal policy entropy collapse in RL for LLMs; a key failure mode to watch for
> - [[2508.16546|SFT-vs-RL-Spectral-Analysis]] — Reveals that SFT causes OOD generalization issues that RL avoids, via spectral lens

**SFT vs RL Generalization** — Why RL generalizes where supervised fine-tuning memorizes — a central question for post-training.
- [[2605.11739|EffOPD]], [[2602.10815|RL-vs-SFT-VLM-Study]], [[2512.17636|TRAPO]], [[2512.12690|SFT-vs-RL-VLM-Study]], [[2501.17161|SFT-Memorizes-RL-Generalizes]]

> [!star] Key Papers
> - [[2501.17161|SFT-Memorizes-RL-Generalizes]] — Landmark finding: SFT makes models memorize training distributions, while RL makes them generalize to unseen problems
> - [[2512.17636|TRAPO]] — Unifies SFT and RL within a single trajectory-level preference optimization framework

**Test-Time Scaling & Compute** — Trading inference compute for better reasoning — search, verification, and adaptive depth at test time.
- [[2606.31132|ELASTIC]], [[2601.06748|TT-VLA]], [[2510.08189|R-Horizon]], [[2505.21236|RL-Inference-Strategies]], [[2503.24235|Test-Time-Scaling-Survey]], [[2408.03314|Test-Time Compute Scaling]], [[2407.14414|System-1.x]]

> [!star] Key Papers
> - [[2503.24235|Test-Time-Scaling-Survey]] — Unified four-axis taxonomy for the rapidly growing test-time scaling field
> - [[2407.14414|System-1.x]] — Dynamic balancing between fast System-1 and deliberate System-2 processing in LLMs

> [!tip] The SFT vs RL Divide
> The key insight from 2025: SFT teaches models to *reproduce* patterns, RL teaches them to *solve* problems. For reasoning tasks, RL generalizes where SFT memorizes. But SFT remains essential for format/instruction following — the best pipelines use SFT then RL.

**Safe & Risk-Sensitive RL** — Constrained RL, safety filters, shielding, and risk-averse objectives for safety-critical deployment.
- [[2607.01794|Lightweight Safe RL for UAV Navigation]], [[2606.31993|OopsieVerse]], [[2606.31320|AutoSafe]], [[2605.14174|VIA]], [[2605.09772|GP-Safe-Exploration]], [[2605.01195|TAIL-Safe]], [[2602.13040|TCRL]], [[2602.11437|DrIGM]], [[2602.05089|Daze]], [[2512.01228|BARPO]], [[2511.09681|SEBA]], [[2510.03471|Quadcopter-Control-Eval-Suite]], [[2508.02948|f-MORNAVI]], [[2507.20068|PERRY]], [[2506.21683|Risk-Averse-Total-Reward-RL]], [[2506.11033|Adaptive-Shielding]], [[2502.16816|Robust-Avg-Reward-RL]], [[2404.13009|M-GAPS-Online-Policy-Opt]], [[2310.12567|Safety-Gymnasium]]

> [!star] Key Papers
> - [[2310.12567|Safety-Gymnasium]] — The field's unifying benchmark suite (54 environments + 16 validated baselines); the standard testbed for constrained RL
> - [[2606.31320|AutoSafe]] — Makes hard-constraint intervention differentiable, resolving the soft-constraint vs hard-filter dilemma; validated on real hardware
> - [[2506.21683|Risk-Averse-Total-Reward-RL]] — First model-free Q-learning with proven convergence for risk-averse objectives in the undiscounted setting
> - [[2602.13040|TCRL]] — Temporal-coupled adversarial training for constrained RL; reduces safety costs by orders of magnitude under worst-case attacks

**Adversarial Robustness, Attacks & Domain Generalization** — Attacks, backdoors, targeted perturbations, and cross-domain/cross-dynamics generalization for RL policies.
- [[2510.15382|Robust-Zero-Shot-RL]], [[2510.14246|DR-RPO]], [[2510.11824|MARL-Robustness-Study]], [[2509.24130|Sharpness-Aware-Prompt]], [[2509.23846|AD-RRL]], [[2509.16950|Multi-Vehicle-Backdoor]], [[2507.07348|Context-Generalization-RL]], [[2506.16590|EBTL]], [[2506.12815|TrojanTO]], [[2506.12622|DR-SAC]], [[2412.18781|Offline-RL-Action-Perturbation-Eval]], [[2412.10713|RAT]], [[2409.18330|DMC-VB]], [[2406.09976|RMBPO]], [[2406.03862|Behavior-Imitation-Attack]], [[2312.17116|SAM-G]], [[2307.10224|RL-ViGen]], [[2307.00972|MoVie]], [[2206.00238|DARL]], [[2204.12581|RAMBO-RL]]

> [!star] Key Papers
> - [[2412.10713|RAT]] — Preference-based targeted attacks on DRL; bi-level intention-policy + adversary + state-weighting; doubles as adversarial-training tool

---

## 2. Model-Based RL & World Models

The Dreamer lineage: learning a latent world model, then "dreaming" in it to train a policy. This is the foundation for World Action Models (WAMs) in robotics.

**Dreamer Lineage** — The core trajectory from latent imagination through scalable general agents to real-robot deployment.
- [[2607.19719|Koopman Dreamer]], [[2605.04709|ELVIS]], [[2604.02911|DreamTIP]], [[2604.02260|Time-Varying-MBRL]], [[2603.18202|R2-Dreamer]], [[2509.24804|DyMoDreamer]], [[2503.21047|CBET-DreamerV3]], [[2502.00466|EDELINE]], [[2501.16443|OC-STORM]], [[2301.04104|DreamerV3]], [[2211.15944|Continual-Dreamer]], [[2206.14176|DayDreamer]], [[1912.01603|Dreamer]], [[1809.01999|World Models]]

> [!star] Key Papers
> - [[1912.01603|Dreamer]] — Pioneered latent imagination: learn a world model in latent space, generate synthetic rollouts, train the policy entirely in imagination
> - [[2301.04104|DreamerV3]] — Generalized Dreamer to 130+ diverse domains with a single set of hyperparameters; introduced symlog predictions for stable learning
> - [[2206.14176|DayDreamer]] — First to deploy Dreamer on physical robots (A1 quadruped, UR5 arm), learning from scratch in hours

**Classic Intrinsic Motivation & Novelty-Seeking** — Foundational curiosity, novelty, and disagreement-based exploration bonuses.
- [[2503.23631|Intrinsic-Motivation-Human-Agent-Study]], [[2503.01584|SENSEI]], [[2502.07279|Exploratory-Diffusion-RL]], [[2502.05726|ACCEL]], [[2411.13852|ESRM]], [[2408.05804|Single-Goal-Contrastive-RL]], [[2305.13622|SER]], [[2112.15402|RER]], [[2007.07853|γ-Progress]], [[2005.05960|Plan2Explore]], [[1901.01753|POET]], [[1810.12894|RND]], [[1806.03335|Randomized Prior Functions]], [[1705.05363|ICM]], [[1606.01868|Pseudo-Counts]], [[1605.09674|VIME]], [[1507.00814|Predictive Exploration Bonus]]

> [!star] Key Papers
> - [[1810.12894|RND]] — Random Network Distillation solved Montezuma's Revenge (22/24 rooms); resolved the "noisy-TV problem" plaguing earlier curiosity methods
> - [[1705.05363|ICM]] — Defined curiosity as forward-model prediction error in a learned feature space; the most widely-cited curiosity template
> - [[1606.01868|Pseudo-Counts]] — Unified count-based exploration with intrinsic motivation via density-model pseudo-counts; gave novelty bonuses formal information-gain grounding
> - [[2005.05960|Plan2Explore]] — Curiosity-driven exploration in world model latent space; explores to maximize world model improvement, then adapts zero-shot
> - [[2503.01584|SENSEI]] — Semantic exploration with epistemic uncertainty + Go-Explore for versatile world models

**Modern Goal-Conditioned, Curriculum & Multi-Agent Exploration** — Recent goal-conditioned, curriculum, and multi-agent/social exploration methods (2025-2026).
- [[2607.18433|Learnable Novelty]], [[2605.22814|Remember-to-be-Curious]], [[2605.03782|GLANCE]], [[2603.28386|COvolve]], [[2603.15789|OmniReset]], [[2603.02008|C-TeC]], [[2602.01619|SUSD]], [[2601.19810|ULEE]], [[2601.19707|QFLEX]], [[2510.24482|COMBRL]], [[2510.14129|Emergent-Exploration-GCRL]], [[2509.20648|CERMIC]], [[2509.09675|CDE]], [[2509.03771|Co-Evolving-MARL]], [[2506.22401|MEX-Primal-Dual]], [[2506.16396|GoalLadder]], [[2506.05980|AMPED]], [[2506.05634|AutoQD]], [[2506.00138|Virtual-Zebrafish-RL]], [[2505.19850|DISCOVER]]

**Flow-Matching Policies & Critics** — RL methods built on flow matching rather than diffusion, for policies, critics, and value functions.
- [[2607.26460|RLMM-Flow]], [[2607.10369|VINE]], [[2606.29934|RoamFlow]], [[2605.13435|Q-Flow]], [[2603.11470|NFPO]], [[2603.05296|LPS]], [[2603.04333|floq]], [[2602.18015|Flow-Actor-Critic]], [[2602.01156|PolicyFlow]], [[2512.03973|Guided-Flow-Policy]], [[2510.07650|Value-Flows]], [[2509.25756|SAC-Flow]], [[2509.06863|floq-Flow]], [[2508.13904|OFQL]], [[2506.12811|FlowRL-Online]], [[2505.23062|COMPFLOW]], [[2502.02538|FQL]]

> [!star] Key Papers
> - [[2502.02538|FQL]] — Foundational flow-matching offline RL method; one-step distillation from a BC flow policy avoids BPTT, the baseline every other paper here compares against
> - [[2509.06863|floq-Flow]] — Extends flow matching to the critic side, parameterizing Q-values as a flow process with dense step-wise supervision for ~1.8x gains over FQL
> - [[2605.13435|Q-Flow]] — Cleanest fix for the stability-expressivity tradeoff via a flow-consistent intermediate value function; beats FQL by 10.6% offline and 23% online
> - [[2603.04333|floq]] — Explains the empirical success of flow-matching critics in Temporal Difference learning

**Diffusion Planning & Trajectory Generation** — Denoising-diffusion planners that generate or condition trajectories directly.
- [[2607.25798|Transformer Transformer]], [[2606.19656|DF-ExpEnse]], [[2605.28293|ProRL-Recommendation]], [[2605.20758|g-car]], [[2605.04568|Dream-MPC]], [[2604.00202|DreamControl-v2]], [[2603.14245|GoldenStart]], [[2602.08032|Horizon-Imagination]], [[2602.05051|ReFORM]], [[2601.00898|DIPOLE]], [[2508.12166|B-COD]], [[2505.20922|DIMA]], [[2505.10881|Prior-Guided-Diffusion-Planning]], [[2304.12824|QGPO]], [[2210.15629|LCD]], [[2208.06193|Diffusion-QL]], [[2205.09991|Diffuser]]

> [!star] Key Papers
> - [[2210.15629|LCD]] — Hierarchical diffusion planner extending Diffuser to pixel/language-conditioned long-horizon control; 3.3-15x faster inference
> - [[2505.10881|Prior-Guided-Diffusion-Planning]] — Learns a latent prior to concentrate sampling on high-value trajectories; SOTA on long-horizon D4RL
> - [[2604.00202|DreamControl-v2]] — Diffusion model trained directly in a robot's motion space for whole-body loco-manipulation, validated on a real Unitree-G1
> - [[2205.09991|Diffuser]] — Planning as diffusion over trajectories; reframed RL as iterative denoising, enabling flexible conditioning on rewards, constraints, and skills

**Value & Sample-Efficient Diffusion/Flow RL Methods** — Diffusion/flow methods applied to value estimation, sample-efficient TD learning, and hybrid RL objectives.
- [[2607.10892|ESM]], [[2607.06262|OTQL]], [[2606.21646|ECD]], [[2606.06049|L-SDPPO]], [[2604.23380|V-GRPO]], [[2604.19730|FASTER]], [[2510.01068|GPC-RL]], [[2509.21942|SIHD]], [[2509.04063|ARFM]], [[2506.21427|SSCP]], [[2506.08902|InFOM]], [[2506.07822|RACTD]], [[2506.00895|SCoTS]], [[2505.23527|NF-for-RL]], [[2505.01822|AEPO]]

**JEPA & Latent Prediction for RL** — Joint-Embedding Predictive Architectures adapted for RL, predicting future states in latent space rather than pixel space.
- [[2607.26712|ActSWM]], [[2607.26056|INTACT]], [[2606.14418|COMET]], [[2601.19336|EAWM]], [[2512.07733|SpatialDreamer]], [[2511.05963|NextLat]], [[2510.00739|TD-JEPA]], [[2508.20294|DALI]], [[2504.16591|JEPA-for-RL]], [[2502.14819|PLDM]], [[2407.01570|Ego-Foresight]]

> [!star] Key Papers
> - [[2502.14819|PLDM]] — Planning with Latent Dynamics Models from NYU/Meta FAIR; leveraging reconstruction-free latent dynamics for control
> - [[2510.00739|TD-JEPA]] — Temporal-difference JEPA learns policy-conditioned multi-step latents for zero-shot RL; SOTA across 65 tasks, strong on pixel-based observations

**World Model Architectures & Latent Representations** — Model designs for latent-action, latent-state, and joint-embedding world models.
- [[2607.28415|QQWorld]], [[2606.21173|P-learning]], [[2606.04130|CLAW-Latent-Action-WM]], [[2606.02027|World-Task-Factorization]], [[2605.29564|VE2VF]], [[2605.25313|UWM-JEPA]], [[2605.22123|FLORA]], [[2605.12771|PASTA]], [[2604.03208|HWM]], [[2604.01985|WAV]], [[2603.29090|HCLSM]], [[2603.28963|AutoWorld]], [[2603.28955|WAM]], [[2503.00653|DC-MPC]], [[2408.14472|DWL]], [[2403.04253|R2I]], [[2402.19161|MemoNav]]

> [!star] Key Papers
> - [[2403.04253|R2I]] — Foundational latent-state architecture integrating State Space Models into Dreamer; superhuman on Memory Maze with 9x faster training than DreamerV3
> - [[2606.04130|CLAW-Latent-Action-WM]] — Clearest latent-action world model design; adversarial gradient-reversal regularization prevents information leakage from action-free video
> - [[2605.25313|UWM-JEPA]] — Most novel joint-embedding architecture, replacing vector latents with a density-matrix belief state and a unitary predictor for uncertainty-preserving imagination

**World Model Theory, Control & Sample-Efficient Planning** — Formal generalization results, free-energy/active-inference grounding, and planning algorithms built on world models.
- [[2608.02993|InK]], [[2605.06732|Training-in-Imagination]], [[2605.01694|Latent-State-Design-WM]], [[2602.06130|SWIRL]], [[2602.05842|RWML]], [[2512.09929|OWM]], [[2512.03556|RoboScape-R]], [[2510.21232|Confusing-World-Models]], [[2510.18135|World-in-World]], [[2506.01622|General-Agents-World-Models]], [[2501.10100|RWM]], [[2310.16828|TD-MPC2]], [[2206.02072|VSRL]], [[2203.04955|TD-MPC]], [[2112.01506|REVI]], [[2106.02039|Trajectory-Transformer]], [[2103.10369|RH-UCRL]], [[1911.10601|Scaling-Active-Inference]], [[1805.12114|PETS]]

> [!star] Key Papers
> - [[2506.01622|General-Agents-World-Models]] — Google DeepMind formally proves that agents capable of generalizing to multi-step, goal-directed tasks must build world models
> - [[2310.16828|TD-MPC2]] — Scalable model-based RL: a single world model architecture masters 300+ continuous control tasks across domains
> - [[1911.10601|Scaling-Active-Inference]] — First to scale active inference to continuous control domains; bridges free energy theory with practical deep RL

**Offline World Model Architectures & Benchmarks** — Model designs, action representations, and evaluation suites for learning world models from fixed datasets.
- [[2603.08118|RVL]], [[2602.23770|MAGE]], [[2602.01270|Mixture-of-World-Models]], [[2512.08108|Action-Chunk-MBRL]], [[2512.04341|NEUBAY]], [[2511.19584|MMBench-World-Models]], [[2509.19080|World4RL]], [[2509.13095|SeqWM]], [[2506.08460|MOBODY]], [[2505.15754|Temporally-Extended-Actions]], [[2505.15589|Reflexive-World-Models]]

> [!star] Key Papers
> - [[2512.08108|Action-Chunk-MBRL]] — Action-chunk dynamics + flow-matching policies solve the rollout-length/model-error trade-off; SOTA on the long-horizon OGBench suite
> - [[2602.23770|MAGE]] — Multi-scale trajectory autoencoder with coarse-to-fine autoregressive generation; SOTA across five offline RL benchmarks
> - [[2512.04341|NEUBAY]] — Non-conservative Bayesian world-model design overturns the field's default conservatism assumption; new SOTA on 7 of 33 D4RL/NeoRL datasets

**Offline MBRL Algorithms & Policy Adaptation** — Policy optimization, objective-mismatch mitigation, and robustness for offline model-based RL.
- [[2505.13709|Policy-Driven-WM-Adaptation]], [[2504.16680|RWM-U]], [[2502.19544|Generalist-to-Specialist]], [[2410.00564|JOWA]], [[2406.09976|RMBPO]], [[2310.06253|Objective-Mismatch-MBRL-Survey]], [[2302.03086|DITTO]], [[2204.12581|RAMBO-RL]], [[1906.08253|MBPO]], [[1803.10122|World-Models]]

> [!star] Key Papers
> - [[2504.16680|RWM-U]] — Uncertainty-aware world model for real-robot offline RL; bridges sim-to-real with calibrated uncertainty
> - [[2505.13709|Policy-Driven-WM-Adaptation]] — Joint WM-policy optimization via Stackelberg dynamics; resolves objective mismatch with state-of-the-art robustness
> - [[2310.06253|Objective-Mismatch-MBRL-Survey]] — Unified taxonomy for decision-aware MBRL; foundational reference for the objective-mismatch problem

**Continual & Online World Models** — World models that update online without catastrophic forgetting, supporting lifelong learning.
- [[2604.08958|WOMBET]], [[2603.04029|Self-Adapting-RL]], [[2602.14351|WIMLE]], [[2602.00475|GRASP]], [[2510.04507|WISDOM]], [[2507.09177|Online-Agent-OA]]

> [!star] Key Papers
> - [[2602.00475|GRASP]] — Gradient-based planning enabling world models to solve long-horizon control tasks

> [!tip] Why This Matters for Robotics
> The Dreamer to DayDreamer to DreamerV3 lineage directly enables WAMs like DreamZero. The key insight: learning in imagination is orders of magnitude more sample-efficient than real-world trial-and-error. JEPA-based latent prediction is the next frontier — faster and more robust than pixel-space generation.

---

## 3. Policy Optimization

Direct methods for optimizing policies — from classic PPO through modern GRPO variants, KL-regularized objectives, and tree-structured search. This is the algorithmic engine behind both LLM reasoning and robot control.

**Domain-Specific & Multimodal GRPO Applications** — GRPO adapted to specific modalities and domains — video, flow-matching, diffusion, navigation, and MoE.
- [[2605.27079|TRQAM]], [[2605.21429|roto-2.0]], [[2605.15726|NUDGERL]], [[2605.15458|VideoRLVR]], [[2605.15012|FEST]], [[2605.14539|CIPO]], [[2605.06139|LPO]], [[2604.27998|Latent-GRPO]], [[2604.02288|SRPO]], [[2603.24984|MoE-GRPO]], [[2511.06411|SofT-GRPO]], [[2510.19807|Scaf-GRPO]], [[2510.08554|GDPO-Diffusion-LM]], [[2509.06040|BranchGRPO]], [[2507.21848|EDGE-GRPO]], [[2506.16141|GRPO-CARE]], [[2506.13923|Guide-GRPO]], [[2505.05470|Flow-GRPO]], [[2301.13261|Blind-Nav-Agents]], [[2101.05181|MemAug-Image-Goal-Nav]]

> [!star] Key Papers
> - [[2505.05470|Flow-GRPO]] — First method to integrate online GRPO into flow-matching models via an ODE-to-SDE conversion; pushed SD3.5-M GenEval accuracy from 63% to 95%
> - [[2605.15458|VideoRLVR]] — Extends the SDE-GRPO recipe from images to video diffusion, teaching rule-verifiable visual reasoning with ~40% training-latency cut
> - [[2603.24984|MoE-GRPO]] — Pioneers GRPO for a structural target, treating expert routing itself as the RL policy; boosts VLM OOD generalization by up to 4.1%

**Core GRPO Algorithm & Theory** — Foundational GRPO variants addressing credit assignment, sampling, off-policy extension, and risk-sensitivity.
- [[2607.16850|GECPO]], [[2602.05547|MT-GRPO]], [[2601.20614|DGPO-Difficulty]], [[2510.20150|Rank-GRPO]], [[2510.04072|SFPO]], [[2509.25849|Knapsack-GRPO]], [[2509.24261|Risk-Sensitive-GRPO]], [[2508.09726|GFPO]], [[2505.22257|Off-Policy-GRPO]], [[2505.12929|Advantage-Reweighting]], [[2505.12366|DisCO-RL]], [[2504.02546|GPG]], [[2504.00883|vsGRPO]], [[2503.20783|Dr.-GRPO]], [[2503.14476|DAPO]], [[2502.10550|MIKASA]], [[2402.03300|DeepSeekMath]]

> [!star] Key Papers
> - [[2402.03300|DeepSeekMath]] — Introduced GRPO, the group-relative policy optimization algorithm underlying nearly all post-DeepSeek-R1 reasoning RL
> - [[2503.14476|DAPO]] — Open-source large-scale GRPO system; demonstrated that RL at scale produces reasoning capabilities that SFT cannot
> - [[2503.20783|Dr.-GRPO]] — Critical analysis of R1-Zero-like training; identifies and fixes key failure modes in GRPO
> - [[2505.22257|Off-Policy-GRPO]] — Formalized off-policy extension for GRPO; enables more sample-efficient training

**PPO & Proximal Methods** — PPO-family algorithms adapted for LLM and multimodal model training, with emphasis on credit assignment and stability.
- [[2607.10169|RIPO]], [[2605.11473|TOPPO]], [[2605.04470|CRAFT-Driving]], [[2605.03846|SigLoMa]], [[2605.03363|Hierarchical-RL-QP-Grasp]], [[2604.20328|DePO]], [[2602.04879|DPPO]], [[2602.02454|World-Gymnast]], [[2511.01331|RobustVLA]], [[2510.03817|TROLL]], [[2510.01656|AsyPPO]], [[2508.17784|PSFT]], [[2508.08221|Lite-PPO]], [[2506.15050|T-PPO]], [[2410.01679|VinePPO]], [[2409.16578|FLaRe]], [[1707.06347|PPO]], [[1502.05477|TRPO]]

> [!star] Key Papers
> - [[2604.20328|DePO]] — Decoupled PPO for hybrid discrete-continuous action spaces; vMF distribution and hyperspherical KL enable stable MLLM latent-reasoning RL
> - [[2410.01679|VinePPO]] — Replaces PPO's learned value function with vine-based credit assignment; more precise step-level rewards
> - [[2506.15050|T-PPO]] — Truncated PPO significantly enhances training efficiency for LLM reasoning

**Multimodal & VLM Preference Alignment** — DPO-family preference optimization applied to vision-language and VLA models.
- [[2509.26346|EditReward]], [[2504.16801|DeGLA]], [[2504.15619|AdaViP]], [[2504.12717|RaFA]], [[2503.03480|SafeVLA]], [[2411.19309|GRAPE]], [[2411.10442|MPO]], [[2408.01800|MiniCPM-V]]

> [!star] Key Papers
> - [[2411.19309|GRAPE]] — First trajectory-wise DPO-style preference optimization for VLA robot policies; automated cost-based pipeline yields large gains over OpenVLA-DPO
> - [[2411.10442|MPO]] — Foundational study combining DPO+BCO+SFT losses for MLLM reasoning; an 8B model matches a 76B model on MathVista
> - [[2504.15619|AdaViP]] — Clearest vision-grounded DPO variant, building preference pairs from perturbed images with adaptive vision/language weighting
> - [[2411.10442|MPO]] — Mixed Preference Optimization with scalable automated pipeline for constructing multimodal preferences

**Core DPO Objective Variants** — Algorithmic reformulations of the DPO loss — reweighting, groupwise, and generalized objectives.
- [[2606.16856|VOTP]], [[2604.02349|OPRIDE]], [[2604.01840|PGPO]], [[2603.28618|PRCO]], [[2603.28204|ERPO]], [[2603.19835|FIPO]], [[2602.22703|GEODPO]], [[2602.21346|Alignment-Weighted-DPO]], [[2509.23802|STAIR]], [[2509.23102|MNPO]], [[2507.13579|PLUS]], [[2507.08068|QRPO]], [[2506.10054|Uni-DPO]], [[2506.07127|APO]], [[2506.01183|DRPO]], [[2502.16852|ONPO]], [[2411.04109|SCPO]]

> [!star] Key Papers
> - [[2509.23102|MNPO]] — Generalizes two-player Nash preference learning to an N-player game; its Time-Dependent variant provably unifies DPO, IPO, SPIN, and INPO
> - [[2506.10054|Uni-DPO]] — Cleanest reweighting variant, jointly weighting pairs by data quality and evolving model fit; Gemma-2-9B beats Claude 3 Opus on Arena-Hard
> - [[2507.08068|QRPO]] — Solves DPO's relative-preference-only limitation by transforming pointwise rewards into quantile rewards, reducing policy fitting to plain regression

**Classic & Theoretical Preference Optimization** — The DPO lineage's foundational and theoretically-grounded variants.
- [[2502.08922|SCIR]], [[2411.00361|DIPPER]], [[2410.23223|COMAL]], [[2410.12735|CREAM]], [[2410.02355|AlphaEdit]], [[2407.13399|χPO]], [[2405.16436|RPO]], [[2405.14734|SimPO]], [[2405.12961|Energy-Rank-Alignment]], [[2210.05639|DPO]]

> [!star] Key Papers
> - [[2405.14734|SimPO]] — Widely-adopted reference-free simplification of DPO, fixing its reward/generation-likelihood mismatch; SOTA among sub-10B open models
> - [[2407.13399|χPO]] — Strongest theoretically-grounded variant, replacing KL-regularization with mixed χ²-divergence for provable overoptimization guarantees
> - [[2410.23223|COMAL]] — Extends the lineage beyond the Bradley-Terry assumption; first algorithm proven to reach the exact Nash equilibrium under general preferences

**Alignment Data Curation & Training Efficiency** — Data-selection, curation, and compute-efficient recipes for preference training.
- [[2602.10388|FAC Synthesis]], [[2512.16626|SLHF]], [[2511.20629|MapReduce-LoRA]], [[2511.10985|DPO-Data-Curation-Study]], [[2510.20413|AuxDPO]], [[2510.16333|PIVOT]], [[2510.11194|CDRA]], [[2510.03269|GEB]], [[2509.26074|LENS]], [[2506.09508|Efficient-Preference-RL]], [[2506.08681|IS-DAAs]], [[2502.07193|One-Pass-RLHF]]

> [!star] Key Papers
> - [[2511.10985|DPO-Data-Curation-Study]] — Systematic cross-analysis of five open-source DPO datasets that curates UltraMix, 30% smaller yet outperforming across 14 benchmarks while cutting training compute by 30%
> - [[2509.26074|LENS]] — Synthesizes preference data directly in latent embedding space, an 18x faster alternative to text-based synthesis for reward model training under limited preference data
> - [[2502.07193|One-Pass-RLHF]] — Provably O(1) per-iteration compute and storage for online reward modeling via mirror descent, with a proven √κ statistical efficiency gain over MLE

**Alignment Theory, Safety & Multi-Objective Optimization** — Directional, multi-objective, and safety-oriented alignment theory beyond the core DPO objective.
- [[2605.02087|MSM]], [[2603.25077|ToR]], [[2603.23355|ReVal]], [[2603.22117|RLVR-Direction]], [[2603.21383|PivotRL]], [[2603.12595|SPL-Swap]], [[2511.15605|SRPO]], [[2509.14234|CaT]], [[2509.11452|Multi-Objective-RL-Alignment]], [[2509.07414|LSP]], [[2506.21495|Offline-Online-RL-for-LLMs]], [[2506.16895|STRUCTURE-Alignment]], [[2505.15456|RLPA]], [[2503.09561|Strategyproof-RLHF]]

> [!star] Key Papers
> - [[2506.21495|Offline-Online-RL-for-LLMs]] — Shows DPO adapted to online or hybrid settings matches full RL performance at lower cost

**LLM/RLHF-Oriented Value & Advantage Methods** — Value and advantage estimation designed specifically for LLM RL post-training and reasoning.
- [[2608.03068|CVPO]], [[2606.20008|VIMPO]], [[2604.28005|KAE]], [[2604.22074|CIR/SR-Reasoning]], [[2604.14265|VGF]], [[2507.20673|GMPO]], [[2505.20686|A*-PO]], [[2505.15311|TBRM]], [[2504.19599|GVPO]], [[2504.05118|VAPO]], [[2502.20548|Q-sharp]], [[2502.16944|DVPO]]

> [!star] Key Papers
> - [[2504.19599|GVPO]] — Zero-sum-weight gradient design gives a provable unique convergence guarantee; scores 20.72 on AIME2024 versus GRPO's 14.79 with strong hyperparameter robustness

**Value Function Representation Learning** — Representation-learning approaches to value functions — successor features, hyperbolic embeddings, and Eikonal/proto representations.
- [[2602.10539|DAWN (Residual RL Value Learning)]], [[2512.14202|Hyperbolic-Deep-RL]], [[2512.12046|Eik-QRL]], [[2510.06714|Dual-Goal-Representations]], [[2509.18714|GBSM]], [[2509.12026|RDM-RL]], [[2509.06782|Eikonal-Value-Learner]], [[2509.05193|k-Shifted-Successor]], [[2505.16217|Reward-Aware-Proto-Representations]], [[2505.12737|OTA-Value-Learning]]

> [!star] Key Papers
> - [[2512.14202|Hyperbolic-Deep-RL]] — Formal gradient analysis of hyperbolic RL's optimization instabilities yields HYPER++, beating prior hyperbolic agents by 52.3% on ProcGen and outperforming Euclidean baselines
> - [[2509.06782|Eikonal-Value-Learner]] — Eikonal PDE regularizer shapes goal-conditioned value functions into distance fields, improving GCVF accuracy by over 100% on 7 of 31 OGbench navigation/locomotion tasks
> - [[2509.05193|k-Shifted-Successor]] — Shows low-rank structure emerges naturally in temporally-shifted successor measures, with the first finite-sample guarantees for their entry-wise estimation

**Theoretical Value-Function & Sample-Complexity Analysis** — Formal analysis of value estimation, regret bounds, and distributional/average-reward theory.
- [[2607.01880|DySEL]], [[2604.23056|K-Score]], [[2601.20071|Distributional-Sobolev-RL]], [[2510.06647|Gap-Dependent-Q-Regret]], [[2507.13181|Spectral-Bellman-Method]], [[2506.20904|Avg-Reward-Sample-Complexity]], [[2506.20048|Fitted-Distributional-Evaluation]], [[2505.23150|Categorical-Q-Learning]], [[2505.21391|Linear-TD-Finite-Sample]], [[2505.16548|TC-lambda]], [[2505.15544|differential-TD]], [[2505.10007|DR-Avg-Reward-Complexity]], [[2502.14172|Linear-CTD]], [[2105.05347|Return-based Scaling]], [[1706.05374|EPG]], [[1707.06887|C51]]

> [!star] Key Papers
> - [[1707.06887|C51]] — DeepMind's foundational distributional Bellman equation, learning full return distributions instead of expectations; Categorical DQN scores 701% mean human-normalized on 57 Atari games
> - [[2510.06647|Gap-Dependent-Q-Regret]] — First rigorous fine-grained gap-dependent regret bounds for model-free Q-learning, improving UCB-Hoeffding's dependence and fixing flaws in the prior AMB algorithm
> - [[2506.20904|Avg-Reward-Sample-Complexity]] — First fully single-policy sample-complexity guarantee for average-reward offline RL, proven statistically optimal and requiring no unlearnable environment parameters

**Q-Learning, Offline & MDP-Structured Value Methods** — Applied Q-learning variants, offline value estimation, and structured-MDP value methods.
- [[2605.11479|Discounted Liveness OPE]], [[2605.05812|LQL]], [[2604.20627|Occupancy-Reward-Shaping]], [[2603.00716|Frozen-Policy-Iteration]], [[2602.17062|S2Q]], [[2602.02710|MaxRL]], [[2601.14234|QAM]], [[2512.15405|EUBRL]], [[2511.07730|MQE]], [[2510.06649|ARQ]], [[2510.06540|Superstate-MDP-RL]], [[2510.02590|MINTO]], [[2509.23962|CANON]], [[2509.22611|QAE]], [[2509.19800|ALP-MDP]], [[2506.04398|iS-QL]], [[2505.21119|UVU]], [[2503.03660|Transformer-Critic-SAC]]


**Tree Search & MCTS** — Monte Carlo Tree Search integrated with RL for structured exploration during training and inference.
- [[2607.03751|SVA]], [[2604.01434|VOIMCP]], [[2602.20809|RGSC]], [[2510.24302|LATR]], [[2509.25454|DeepSearch]], [[2509.15929|MCTS-Symbolic-Regression]], [[2509.09284|Tree-OPO]], [[2508.17445|TreePO]], [[2506.11902|TreeRL]], [[2410.11234|BA-MCTS]], [[2406.06592|OmegaPRM]], [[2406.03816|ReST-MCTS*]]


**Classic Offline RL & Actor-Critic Algorithms** — The foundational offline/off-policy algorithm lineage: conservative Q-learning, implicit Q-learning, and actor-critic baselines.
- [[2311.03351|Uni-O4]], [[2310.20587|LaMo]], [[2306.09459|RATE]], [[2110.06169|IQL]], [[2106.01345|Decision Transformer]], [[2103.06326|S4RL]], [[2006.04779|CQL]], [[2004.07219|D4RL]], [[1906.00949|BEAR]], [[1806.10293|QT-Opt]], [[1806.05635|SIL]], [[1805.07914|ILPO]], [[1801.01290|SAC]], [[1509.02971|DDPG]]

> [!star] Key Papers
> - [[1801.01290|SAC]] — The maximum-entropy off-policy actor-critic baseline every later method in this section is compared against; combines sample efficiency with stability on continuous control
> - [[2006.04779|CQL]] — Regularizes Q-values to be conservative on out-of-distribution actions, achieving 2-5x higher returns on multi-modal D4RL benchmarks and solving previously intractable domains like AntMaze
> - [[2110.06169|IQL]] — Never queries out-of-distribution actions at all, using expectile regression to implicitly estimate max Q-values; excels at stitching suboptimal trajectories on long-horizon navigation

**Experience Replay, Data Reuse & Off-Policy Evaluation Theory** — Replay-buffer design, data attribution, and the theory of off-policy evaluation and function approximation.
- [[2601.19030|Linear-OPE-Coverage]], [[2601.18795|Reuse-FLOPs]], [[2509.04501|RL-for-Model-Training-Survey]], [[2507.11269|Data-Recycling-RL]], [[2506.21039|Frontier-Experience-Replay]], [[2506.18482|Reliability-Adjusted-PER]], [[2506.00131|DT-CORL]], [[2505.19281|Online-RL-Data-Attribution]], [[2503.02269|Experience-Replay-Random-Reshuffling]], [[2502.08021|LSTD-Tournament]], [[2502.07523|CrossQ+WN]], [[2501.15910|Online-RL-Multi-Model-Complexity]], [[2501.01774|Off-Policy-LFA-Unifying-View]], [[2412.09858|RLDG]], [[2412.00798|CRUCB]], [[2407.20230|SAPG]]

> [!star] Key Papers
> - [[2501.01774|Off-Policy-LFA-Unifying-View]] — Unifies TD, FQI, and PFQI as matrix-splitting solvers of the same fixed-point equation, establishing necessary-and-sufficient convergence conditions and correcting prior literature
> - [[2507.11269|Data-Recycling-RL]] — Causal upper-bound loss recycles discarded value-network outputs to bridge on- and off-policy learning, lifting mean reward ratio by 383% on Atari with negligible overhead
> - [[2505.19281|Online-RL-Data-Attribution]] — Local influence-based filtering for PPO rollout buffers cuts training rounds by 20-67% and runtime by up to 69%, with RLHF gains transferring to LLM fine-tuning

**LLM Reasoning Off-Policy & Sample-Efficient RL** — Off-policy and data-reuse techniques specifically for LLM RLVR/reasoning training.
- [[2608.01418|PNPO]], [[2605.30056|CGPO]], [[2604.23073|RLT]], [[2604.20733|NPO]], [[2604.18978|LoRA-Critic]], [[2602.20722|BAPO-RL]], [[2510.18927|BAPO]], [[2510.13328|TOSFIT]], [[2510.07730|DEAS]], [[2510.02245|ExGRPO]], [[2510.01161|M2PO]], [[2509.24748|RPEX]], [[2509.24067|ICQL]], [[2509.22601|SPEAR]], [[2509.15981|Uncertainty-Policy-Regularisation]], [[2509.15965|RLinf]], [[2509.01720|SoLS]], [[2509.01321|DEPO]]

> [!star] Key Papers
> - [[2510.02245|ExGRPO]] — Replay-buffer prioritization by question difficulty and trajectory entropy lifts OOD reasoning by +7.6 points and rescues weaker models from RLVR collapse (1.3 to 30.8 OOD score)
> - [[2510.18927|BAPO]] — Adaptive clipping re-balances positive/negative gradient signals to preserve entropy under off-policy staleness, hitting SOTA 87.1 on AIME 2024 among open-source models
> - [[2510.01161|M2PO]] — Second-moment trust-region masking matches on-policy GRPO performance even with data stale by 256 model updates, across model scales from 1.7B to 32B

**Efficient RL Algorithms & Auxiliary Techniques** — Auxiliary tricks and lightweight algorithmic variants that improve RL/RLVR sample efficiency.
- [[2508.19900|ASPC]], [[2508.11143|AC3]], [[2507.07986|EXPO]], [[2507.06892|ReMix-RL]], [[2506.06964|Refit]], [[2506.00917|PSQL]], [[2505.11081|ShiQ]], [[2503.19612|AGRO]], [[2503.05453|SPO]]

> [!star] Key Papers
> - [[2507.07986|EXPO]] — Pairs a frozen imitation-learned expressive policy with a lightweight edit policy for on-the-fly Q-maximizing refinement, stabilizing online RL for diffusion policies on sparse-reward tasks
> - [[2506.06964|Refit]] — Recasts offline RL as reward-weighted fine-tuning with a lower-bound objective, beating SFT and DPO baselines on 7 of 12 multi-turn conversational reasoning benchmarks
> - [[2505.11081|ShiQ]] — Modified Bellman equations bring token-wise off-policy Q-learning back to LLM fine-tuning, matching on-policy performance on UltraFeedback and BFCL-V3 without new sampling

**VLA & Robotics-Applied Off-Policy Methods** — Off-policy and sample-efficient RL applied to vision-language-action and embodied control.
- [[2608.05989|OG-SPR]], [[2606.05555|MR.Q]], [[2606.02313|VLA-Aerial-Nav-GRPO]], [[2605.28527|VLA-Value-Probing]], [[2605.19282|Pion]], [[2605.14779|CPQL]], [[2605.12236|TMRL]], [[2605.11009|ACSAC]], [[2605.03821|RoboAlign-R1]], [[2605.03065|OGPO]], [[2605.01663|FAN]], [[2605.00416|LWD]], [[2605.00159|E²DT]], [[2603.16860|DreamPlan]], [[2603.12087|QAvatar]], [[2510.06710|RLinf-VLA]]

> [!star] Key Papers
> - [[2605.03065|OGPO]] — Bi-level MDP decouples off-policy critic learning from on-policy denoising updates, full-finetuning generative control policies with roughly 10x fewer environment steps than on-policy baselines
> - [[2510.06710|RLinf-VLA]] — Unified framework spanning VLA architectures, RL algorithms, and simulators; delivers 20-85% higher success rates and up to 2.27x training speedups via hybrid GPU pipelining
> - [[2605.00159|E²DT]] — Active, model-cooperative experience selection for Decision Transformers via k-DPP sampling, boosting real-robot success rates (e.g. 82.1% vs 52.4% on shelf placement) with fewer episodes

**Novel & Efficient Off-Policy Algorithms** — Recent off-policy algorithm proposals spanning ranking, uncertainty, and offline data settings.
- [[2606.04968|ForesightFlow]], [[2605.30226|BORA]], [[2605.11151|RankQ]], [[2605.08202|Diffusion-OOD-Detection]], [[2604.26504|HiPAN]], [[2602.18117|FINO]], [[2602.01962|ZOL]], [[2602.00629|OSO-DecQN]], [[2601.20765|C4-Offline-RL]], [[2601.07821|FARL]], [[2601.04441|SPIN-RL]], [[2512.19154|Adaptive-Stacking]], [[2512.02486|DROCO]], [[2509.08660|Replicable-RL]]


**Entropy Collapse Mitigation** — Regularization techniques that directly target policy entropy collapse during RL training.
- [[2604.02355|Entropy-Guided-Synthesis-RL]], [[2603.11682|Entropy-Preserving-RL]], [[2511.07738|Two-Stage-Entropy-GRPO]], [[2510.08549|ERA-Entropy-Activation]], [[2510.05837|EEPO]], [[2510.03222|Lp-Reg]], [[2509.04784|DQO]], [[2506.07085|State-Entropy-Regularization]], [[2506.01939|High-Entropy-Token-RLVR]]

> [!star] Key Papers
> - [[2506.01939|High-Entropy-Token-RLVR]] — Qwen Team's foundational finding that only ~20% of high-entropy "fork" tokens drive effective RLVR gradients; restricting updates to them sets SOTA on AIME'24/'25
> - [[2510.03222|Lp-Reg]] — Selectively protects valuable low-probability "reasoning sparks" via forward-KL regularization, sustaining stable on-policy training for 3,000 steps where prior methods collapse
> - [[2510.08549|ERA-Entropy-Activation]] — Bakes entropy constraints directly into activation functions rather than the reward, boosting HumanoidBench control by 30%+ and AIME'25 by 37.4% across domains

**Diversity-Aware & Multi-Solution RL** — Objectives and audits that preserve solution diversity and mitigate mode collapse across rollouts.
- [[2604.17654|Poly-EPO]], [[2604.16027|Diversity-Collapse-Audit]], [[2603.30036|CoT-Monitorability]], [[2603.01741|CPO-Ensemble]], [[2602.11779|TAMPO]], [[2510.20817|MARA]], [[2509.26209|DIVER]], [[2509.25424|Set-RL]], [[2509.25133|SIREN]], [[2509.07430|DPH-RL]], [[2509.02534|Darling]], [[2505.23433|Diversity-Aware-PO]]

> [!star] Key Papers
> - [[2509.25133|SIREN]] — Selective entropy regularization to mitigate entropy collapse; targets high-uncertainty tokens
> - [[2509.02534|Darling]] — Diversity-Aware RL from Meta FAIR; integrates diversity directly into the RL objective

**KL Divergence & Regularization Theory** — Theoretical and practical work on KL-regularized policy gradients, a fundamental tool in RLHF.
- [[2602.11523|Dual-KL-RLHF]], [[2602.01685|WPR]], [[2506.09477|KL-Divergence-Gradient-Pitfalls]], [[2505.17508|RPG]], [[2503.01067|Online-Offline-PFT-Equivalence]], [[2502.06051|KL-PCB]], [[2502.01203|Multi-Reference-RLHF]], [[2411.04625|KL-RLHF-Bandit-Analysis]]

> [!star] Key Papers
> - [[2506.09477|KL-Divergence-Gradient-Pitfalls]] — Meta FAIR identifies widespread implementation errors in KL divergence gradient estimation; critical for correct RLHF

**Multi-Turn & Agentic Policy Optimization** — Extending RLVR beyond single-turn QA to multi-step, multi-turn, and agentic settings.
- [[2606.05468|FlowPRO]], [[2605.06595|CRONA]], [[2605.02730|PFlowNet]], [[2604.28182|Exploration-Hacking]], [[2602.22817|HGPO]], [[2511.02303|Dr.-MAMR]], [[2510.14967|IGPO-Info-Gain]], [[2510.11062|AT-GRPO]], [[2510.05592|AgentFlow]], [[2509.22638|FCP]], [[2509.21826|ResT-RL]], [[2509.21240|Tree-GRPO]], [[2509.07980|Parallel-R1]], [[2509.02333|DCPO]], [[2506.00539|ARIA]], [[2505.10978|GiGPO]], [[2504.20571|1-shot-RLVR]], [[2504.20073|RAGEN]]

> [!star] Key Papers
> - [[2504.20073|RAGEN]] — Showed that single-turn RLVR doesn't transfer to multi-step tasks; introduced StarPO for multi-turn RL
> - [[2504.20571|1-shot-RLVR]] — Achieves competitive reasoning with just 1 rollout per sample; extreme sample efficiency

**Rollout Speedup, Precision & Compression** — Speculative rollouts, low-precision training, and pruning/compression tricks for faster RL iteration.
- [[2607.07508|SAO]], [[2607.01232|Single-Layer RL Training]], [[2606.18967|EfficientRollout]], [[2606.12370|MTP-RS]], [[2605.15855|AdaScope]], [[2604.26779|Speculative-RL-Rollouts]], [[2603.01639|RL-Speculative-Decoding]], [[2602.01601|VIP-Rollout]], [[2510.26788|FP16-RL-Training]], [[2510.11696|QeRL]], [[2509.23931|AutoPrune]], [[2509.23791|CaRe-BN]], [[2509.22566|Policy-Space-Compression]], [[2509.01920|DSP-Speculative]], [[2505.15345|Hadamax]], [[2311.12244|muLV-Rep]]

> [!star] Key Papers
> - [[2510.26788|FP16-RL-Training]] — Traces the training-inference mismatch to BF16 rounding error; switching to FP16 cuts the mismatch 24x and lets GRPO/PG-Seq-IS converge stably where BF16 collapses
> - [[2510.11696|QeRL]] — NVFP4 hardware quantization plus adaptive quantization noise as an exploration signal gives 1.5x rollout speedup and enables 32B LLM RL training on a single GPU
> - [[2604.26779|Speculative-RL-Rollouts]] — NVIDIA's system-integrated speculative decoding for rollout generation delivers up to 1.41x RL step speedup with verifier-exact training semantics preserved
> - [[2510.26788|FP16-RL-Training]] — Demonstrates FP16 precision works for RL training; halves memory cost

**Distributed Training Infrastructure & Stability** — Distributed/async RL systems and algorithmic stability fixes for scaling RL training to production.
- [[2607.18722|Staleness-Adaptive Trust Region]], [[2604.03489|FAB]], [[2510.01764|Octax]], [[2510.00819|Stable-PG-LLM]], [[2509.25762|OPPO]], [[2509.25174|XQC]], [[2509.24305|Async-Policy-Gradient]], [[2509.21792|FastGRPO]], [[2509.19846|BoreaRL]], [[2508.17850|GEPO]], [[2507.19234|Virne]], [[2506.02177|GRESO]], [[2505.24034|LlamaRL]], [[2505.07291|INTELLECT-2]], [[2503.18929|TBA]], [[2404.08233|GPBT-PL]], [[1803.00933|Ape-X]]

**Unified & Single-Stage SFT+RL Training** — Methods that fuse SFT and RL into one training objective or stage rather than sequencing them.
- [[2510.10606|ViSurf]], [[2508.11408|CHORD]], [[2507.01679|Prefix-RFT]], [[2506.19767|SRFT]], [[2506.13056|Metis-RISE]], [[2506.07527|ReLIFT]], [[2505.18917|Behavior-Injection]], [[2505.18116|NFT]], [[2505.03181|AFSFT]]

> [!star] Key Papers
> - [[2510.10606|ViSurf]] — Fuses SFT and RLVR into one stage for vision-language models via gradient-similarity-informed reward control, gaining 38.6% on average while mitigating catastrophic forgetting
> - [[2506.19767|SRFT]] — Entropy-aware weighting unifies demonstration learning and self-exploration in a single GRPO objective, reaching 59.5% average accuracy and beating LUFFY and TAPO by 3-4 points
> - [[2505.18116|NFT]] — Reframes RL as pure supervised learning by re-parameterizing an implicit negative policy from correctness rates, matching DAPO (51.7% vs 51.2%) without any RL machinery
> - [[2510.10606|ViSurf]] — Unified single-stage post-training integrating SFT and RL; avoids the two-stage overhead

**Staged SFT-RL Pipelines, Diagnostics & Theory** — Sequenced SFT-then-RL recipes plus empirical/theoretical studies of how the two stages interact.
- [[2605.12483|Teacher-First-OPD]], [[2605.10889|OPD-Diagnostic]], [[2605.03677|Uni-OPD]], [[2605.03269|RLDX-1]], [[2604.28123|PRISM]], [[2604.23747|SFT-then-RL-Reaudit]], [[2604.14258|GFT]], [[2603.12248|EBFT]], [[2602.01058|PEAR]], [[2601.21363|Pretrain-Finetune-Bridge-RL]], [[2601.06993|ReFine-RFT]], [[2512.12690|SFT-vs-RL-VLM-Study]], [[2510.01624|SFT-RL-Quagmires]], [[2509.23753|Anchored-SFT]], [[2504.14945|LUFFY]], [[2504.11343|RAFT++]]

> [!star] Key Papers
> - [[2601.06993|ReFine-RFT]] — Identifies the "Cost of Thinking" where excessive textual reasoning hurts; balances verbal and visual reasoning

**Multi-Agent RL** — Multi-agent credit assignment, mean-field, and inverse-RL methods within the policy-optimization family.
- [[2606.30893|CIMORL]], [[2602.02722|Entity-Centric-HRL]], [[2601.05407|HINT]], [[2509.16412|STAF]], [[2509.09135|VIP-CT-MARL]], [[2508.01522|Cable-Suspended MARL]], [[2507.18059|Multi-Agent-GPO]], [[2506.09434|MARL-Diversity-Theory]], [[2505.22760|Best-Response-Flow]], [[2505.13834|Quadrupedal Robot Soccer]], [[2505.04317|HCSP]], [[2502.09762|AT-Drone]], [[2502.00560|CAMS]], [[2501.06058|CASH]], [[2412.04426|Marvel]], [[2412.04233|HyperMARL]], [[2412.00661|SUBSAMPLE-MFQ]], [[2411.15046|Multi-Agent-IRL-Rewards]], [[2405.08036|POW-QMIX]]

> [!star] Key Papers
> - [[2506.09434|MARL-Diversity-Theory]] — Proves via Schur-convexity of the reward aggregation operators exactly when behavioral diversity helps cooperative teams, validated across embodied multi-agent environments
> - [[2412.04233|HyperMARL]] — Agent-conditioned hypernetworks decouple observation and agent gradients, matching No-Parameter-Sharing diversity and Full-Parameter-Sharing efficiency without altering the RL objective
> - [[2606.30893|CIMORL]] — Sampling-based Pareto-frontier search with distributed dynamic weight prediction for multi-objective multi-robot RL, validated with real-world collision-free Crazyflie drone coordination

**Information-Theoretic, Variational & Formal RL Theory** — Principled probabilistic and information-theoretic treatments of policies, latent reasoning, and value geometry.
- [[2509.22637|Variational-Reasoning]], [[2509.15999|IO-LVM]], [[2507.18391|IBRO]], [[2506.16016|Dual-Objective-HJB-RL]], [[2506.10138|Planning-Mechanistic-Description]], [[2506.02385|Markov-Entanglement]], [[2506.01597|Policy-Newton-RKHS]], [[2505.18454|HRPO]], [[2410.03119|Ring-Attractor-RL]], [[2409.17411|Semantic-Clustering-DRL]], [[2006.13566|DISK]]

> [!star] Key Papers
> - [[2507.18391|IBRO]] — Grounds RL post-training in the Information Bottleneck principle; clearest information-theoretic account of the entropy/exploration trade-off via a near-free regularizer
> - [[2506.02385|Markov-Entanglement]] — Most rigorous formal contribution, proving necessary-and-sufficient conditions for exact value decomposition via a novel quantum-entanglement analogy

**Novel LLM/Reasoning-RL Hybrid Algorithms** — New algorithmic proposals bridging classic RL machinery and LLM RLVR training.
- [[2512.03759|ESPO]], [[2512.01374|MiniRL]], [[2512.01047|AutoSpec]], [[2510.09541|SPG]], [[2510.02180|GRACE]], [[2510.00911|RiskPO]], [[2509.25055|AlphaSAGE]], [[2509.24981|ROVER]], [[2509.24207|Humanline]], [[2509.21880|RL-ZVP]], [[2509.16606|BayesG]], [[2509.15207|FlowRL-Reward-Matching]], [[2509.03646|HICRA]], [[2508.17696|FCGrad]], [[2506.19997|TRACED]], [[2506.16608|DA-MDP]], [[2505.18763|GenPO]], [[2404.15617|dfPO]], [[2306.05353|Negotiated-Reasoning]]

> [!star] Key Papers
> - [[2509.24981|ROVER]] — Paradigm-shifting bridge to classic RL theory; proves optimal reasoning actions are recoverable from a fixed uniform-random policy's Q-function
> - [[2509.15207|FlowRL-Reward-Matching]] — Reframes LLM RLVR as GFlowNet-style reward-distribution matching rather than reward maximization, +10% over GRPO at 32B while countering mode collapse
> - [[2512.01374|MiniRL]] — First principled theoretical justification for why token-level RL objectives validly optimize sequence-level LLM rewards, validated at 30B MoE scale
> - [[2509.24207|Humanline]] — Explains why online RL outperforms offline methods from a human cognitive science perspective

**Applied, Hierarchical & Domain-Specific Policy Methods** — Domain-specific and hierarchical policy-optimization applications outside the mainstream algorithm families.
- [[2607.23726|HRL-SAC]], [[2606.04923|CHERRL]], [[2603.17925|SPRUCE]], [[2603.11346|Human-Human-Assist-RL]], [[2602.03086|Neural-Predictor-Corrector]], [[2601.19452|APC-RL]], [[2601.00116|GRL-SNAM]], [[2512.13607|Nemotron-Cascade]], [[2512.00915|PI-MDP]], [[2511.17367|R2PS]], [[2511.08234|Geometric-Action-Control]], [[2511.05005|MAC-Flow]], [[2505.03586|Rainbow-Delay-Compensation]], [[2001.06782|PCGrad]], [[1312.5602|DQN]]

> [!success] The Post-R1 RL Recipe
> ==SFT warm-up== (instruction following + format compliance) → ==GRPO with verifiable rewards== (math/code execution as signal) → ==Distillation== to smaller models. Stable large-scale GRPO training with decoupled clip-higher and dynamic sampling. Even 1.5B models gain reasoning; zero-data bootstrapping works via self-play RL.

> [!tip] The GRPO Revolution
> Post-DeepSeek-R1, GRPO replaced PPO as the default RL algorithm for LLM reasoning. Key improvements: Dr. GRPO fixes training instabilities, DAPO scales to production, and Off-Policy GRPO enables sample reuse. For new projects, start with DAPO or GRPO-CARE.

---

## 4. RL for LLM Reasoning

The post-DeepSeek-R1 paradigm: using RL (especially GRPO) to teach LLMs to reason step-by-step, often surpassing supervised fine-tuning. This section covers the reasoning methods themselves; policy optimization algorithms are in Section 3.

**Bootstrapped Self-Training** — The STaR lineage: iterative self-improvement where the model generates, filters, and fine-tunes on its own reasoning traces.
- [[2605.28814|BES]], [[2605.27276|SIA]], [[2605.25832|AUTO-ROBOTIST]], [[2605.22217|Survive-or-Collapse]], [[2605.21931|EvoVid]], [[2605.20246|GROW]], [[2605.20025|AutoResearchClaw]], [[2512.15687|G2RL]], [[2505.21444|SRT]], [[2505.17746|Fast-Quiet-STaR]], [[2505.03335|Absolute-Zero]], [[2403.09629|Quiet-STaR]], [[2312.06585|ReST-EM]], [[2203.14465|STaR]]

> [!star] Key Papers
> - [[2203.14465|STaR]] — Iterative bootstrapping: LLM generates rationales, keeps correct ones, fine-tunes, repeat. 6B GPT-J matches 175B GPT-3
> - [[2403.09629|Quiet-STaR]] — Extends STaR to think before every token, learning internal rationales from general text
> - [[2505.03335|Absolute-Zero]] — Zero-data RL: model proposes its own problems, solves them, uses verifiable answers as reward — no human data at all

**Self-Distillation & On-Policy Distillation** — Distilling a model's own on-policy rollouts back into itself for self-improvement.
- [[2608.06296|U-OPSD]], [[2608.04788|OCSD]], [[2605.11182|On-Policy-Distillation-Study]], [[2604.27083|CoPD]], [[2604.03128|Self-Distilled-RLVR]], [[2604.03098|Self-Guide]], [[2602.12275|OPCD]], [[2601.20802|SDPO]], [[2601.19897|SDFT]], [[2601.18734|OPSD]]

> [!star] Key Papers
> - [[2601.18734|OPSD]] — Foundational on-policy self-distillation recipe, using the same model as teacher (conditioned on ground truth) and student on its own rollouts; matches GRPO at 4-8x higher token efficiency
> - [[2601.20802|SDPO]] — Strongest reported results in the group, using a self-teacher over rich feedback to beat GRPO by large margins, outperforming Claude Opus/Sonnet 4 on LiveCodeBench
> - [[2605.11182|On-Policy-Distillation-Study]] — Clearest mechanistic account of when and why on-policy self-distillation succeeds or collapses, with concrete fixes

**Self-Rewarding Signal Generation** — Models that construct their own reward or verification signal without external reward models.
- [[2607.23802|SpyRL]], [[2509.05489|Self-Aligned-Reward]], [[2508.14460|DuPO]], [[2508.05004|R-Zero]], [[2508.00410|Co-rewarding]], [[2506.10139|ICM]], [[2506.08745|CoVo]], [[2506.07468|SELF-REDTEAM]], [[2506.01369|Self-Verify-RL]], [[2505.19590|INTUITOR]], [[2401.10020|Self-Rewarding-LM]]

> [!star] Key Papers
> - [[2401.10020|Self-Rewarding-LM]] — Foundational paper establishing the self-rewarding paradigm: a single LLM acts as both generator and judge via iterative DPO, no external reward model
> - [[2506.10139|ICM]] — Strongest reported result, validated at production scale where a Claude 3.5 Haiku assistant trained without human labels beat its human-supervised counterpart
> - [[2505.19590|INTUITOR]] — Clearest exposition of a purely intrinsic reward signal (self-certainty) driving RL, with strong out-of-domain generalization and no external verifier
> - [[2401.10020|Self-Rewarding-LM]] — LLM generates its own reward signal; eliminates the need for a separate reward model
> - [[2508.05004|R-Zero]] — LLMs self-evolve reasoning via self-generated problems and rewards; fully autonomous

**Self-Improvement Pipelines & Applications** — End-to-end self-improvement systems and their applications across modalities.
- [[2607.14777|SEED]], [[2605.20914|RISE-Self-Evolving-VLM]], [[2604.20209|SGS]], [[2601.21343|Self-Improving-Pretraining]], [[2512.05356|Co-Improving-AI]], [[2510.14943|LaSeR-RL]], [[2510.14420|Instructions-RL]], [[2510.02172|RESTRAIN]], [[2509.23863|SPELL]], [[2509.23236|Self-Reflection-VLM]], [[2509.15155|Self-Improving-EFM]], [[2508.14029|SvS]], [[2507.16663|MLLM-Self-Improvement]], [[2504.05812|EMPO]], [[2410.15639|Self-Developing]]

**Chain-of-Thought Reasoning** — Training LLMs to produce explicit step-by-step reasoning, with RL as the training signal.
- [[2606.03937|VEPO]], [[2605.28774|AXPO]], [[2506.07751|AbstRaL]], [[2505.20561|BARL]], [[2505.14631|LHRM]], [[2505.13308|LATENTSEEK]], [[2505.11896|AdaCoT]], [[2505.10425|L2T]], [[2503.24290|Open-Reasoner-Zero]], [[2503.10460|Light-R1]]

> [!star] Key Papers
> - [[2503.24290|Open-Reasoner-Zero]] — First comprehensive open-source reproduction of R1-Zero; reference implementation for the field

**Adaptive Compute Allocation & When-to-Think** — Methods that decide when and how much to reason at inference time, optimizing the compute-accuracy tradeoff.
- [[2604.05355|ETR]], [[2601.22628|TTCS]], [[2512.01127|Mode-Conditioning]], [[2510.09001|DARO]], [[2510.06557|Markovian-Thinker]], [[2510.01135|PCL]], [[2506.18110|AdaBack]], [[2505.19862|REA-RL]], [[2505.13438|AnytimeReasoner]], [[2505.13379|Thinkless]], [[2503.16188|Think-or-Not-Think]], [[2503.04697|L1]], [[2502.04463|Efficient-Reasoning-RL]]

> [!star] Key Papers
> - [[2503.04697|L1]] — Foundational method (LCPO) giving explicit control over reasoning length via a tunable target-token-budget prompt; a 1.5B model beats GPT-4o at matched token budgets
> - [[2505.13379|Thinkless]] — Clearest embodiment of the group's thesis, an LLM that learns to autonomously emit `<think>`/`<no_think>` and skip reasoning when unnecessary, cutting token use 50-90%
> - [[2505.13438|AnytimeReasoner]] — Decouples thinking from answer summarization to optimize accuracy across all compute budgets at once via dense verifiable rewards
> - [[2505.13379|Thinkless]] — RL-based framework that teaches LLMs to skip reasoning when unnecessary; optimizes compute allocation
> - [[2505.13438|AnytimeReasoner]] — Produces usable reasoning at any compute budget; true anytime behavior

**Length Compression & Curriculum-Difficulty RL** — Shortening reasoning traces and pacing training difficulty to control the length-accuracy tradeoff.
- [[2601.19280|GDRO]], [[2601.18067|EvolVE]], [[2512.06835|DoGe]], [[2512.02472|R-FEW]], [[2511.07317|RLVE]], [[2510.27419|DeepCompress]], [[2510.25992|SRL]], [[2510.24832|Reasoning-Tree-Scheduling]], [[2510.23486|Discounted-RL-Reasoning]], [[2510.01037|CurES]], [[2509.25827|DECS]], [[2505.19217|DIET]], [[2505.17312|AdaReasoner-RL]], [[2505.14970|SEC]], [[2505.14140|RL-of-Thoughts]], [[2505.02391|GVM-RAFT]], [[2504.21370|ShorterBetter]], [[2504.05520|ADARFT]], [[2504.01296|ThinkPrune]]

> [!star] Key Papers
> - [[2504.05520|ADARFT]] — Foundational curriculum-difficulty method; pacing training around a ~50% success rate maximizes learning signal and cuts training steps up to 2x
> - [[2510.01037|CurES]] — Strongest reported result in the group, up to 5.5x faster convergence via a gradient-variance-optimal curriculum
> - [[2510.23486|Discounted-RL-Reasoning]] — Clearest theoretical grounding (Blackwell optimality) for why shorter reasoning need not sacrifice accuracy

**Applied Reasoning-Efficiency Methods** — Domain-applied and specialized adaptive-reasoning recipes.
- [[2605.25477|EXPO-FT]], [[2605.17807|CGPO-RL]], [[2604.01658|CORAL]], [[2603.28730|SOLE-R1]], [[2603.27866|Wan-R1]], [[2603.10887|DPS]], [[2602.12113|ARLCP]], [[2510.04474|DRPO-Decoupled]], [[2508.02150|Self-Supervised-RL-IF]], [[2507.22607|VL-Cogito]], [[2506.03295|CFT]], [[2505.20258|ARM]], [[2505.16315|ACPO]], [[2505.15612|LASER]], [[2505.10832|AutoThink]]

**RL Pre-Training** — Applying RL during pre-training rather than just post-training, fundamentally changing how models learn from data.
- [[2606.17024|ExpRL]], [[2512.07203|MMRPT]], [[2512.03442|PretrainZero]], [[2510.01265|RLP]], [[2509.25810|RA3]], [[2509.24375|Reinforcement-Mid-Training]], [[2506.08007|RPT]]

> [!star] Key Papers
> - [[2506.08007|RPT]] — Reinforcement Pre-Training: reframes next-token prediction as RL; models learn reasoning during pre-training
> - [[2512.03442|PretrainZero]] — Self-supervised reinforcement active pretraining without human data

**Flagship Reasoning Models** — Complete, named reasoning-model training pipelines from major labs.
- [[2607.15314|Cura 1T]], [[2607.12395|Ring-Zero]], [[2507.12507|Nemotron]], [[2506.13585|MiniMax-M1]], [[2506.13284|AceReason-Nemotron]], [[2505.00949|Llama-Nemotron]], [[2504.21318|Phi-4-reasoning]], [[2504.21233|Phi-4-Mini-Reasoning]], [[2501.12948|DeepSeek-R1]], [[2501.12599|Kimi k1.5]], [[2501.11223|RLM-Blueprint]]

> [!star] Key Papers
> - [[2501.12948|DeepSeek-R1]] — Showed reasoning emerges from pure outcome-based RL alone; established the multi-stage SFT+RL+distillation pipeline the field now builds on
> - [[2501.12599|Kimi k1.5]] — Proved long-context RL scaling as a viable axis for LLM improvement, matching OpenAI o1 with a simplistic RL framework that drops the value network, MCTS, and PRMs
> - [[2607.12395|Ring-Zero]] — Scaled zero RL to a full trillion parameters; strongest reported results in this group, decisively beating its own 104B counterpart
> - [[2501.12948|DeepSeek-R1]] — Pure outcome-based RL incentivizes emergent chain-of-thought reasoning; the paper that launched the post-R1 RL-for-reasoning paradigm
> - [[2505.00949|Llama-Nemotron]] — NVIDIA's open-source reasoning models achieving state-of-the-art across benchmarks
> - [[2501.11223|RLM-Blueprint]] — ETH Zurich's comprehensive modular blueprint for Reasoning Language Models

**Training Recipes, Curricula & Data for Reasoning** — Data synthesis, curricula, and multi-hop/multi-lingual training recipes for reasoning RL.
- [[2603.02146|LongRLVR]], [[2603.02091|Synthetic-Multi-Hop-RL]], [[2510.19363|LoongRL]], [[2510.16614|MERCI]], [[2510.15414|MARSHAL]], [[2510.11686|RepExp]], [[2510.04140|MENTOR]], [[2510.02173|RL4HS]], [[2509.25666|NuRL]], [[2509.23657|RL-Cross-Lingual]], [[2509.23330|SIE]], [[2509.10396|IGPO]], [[2509.06949|TraceRL]], [[2507.13266|QuestA]], [[2506.08672|RuleReasoner]], [[2506.06632|Easy-to-Hard-Curriculum-RL]], [[2505.24630|FSPO]], [[2505.19914|Enigmata]], [[2505.19641|SynLogic]], [[2504.13828|Cognition-Engineering]]

> [!star] Key Papers
> - [[2603.02091|Synthetic-Multi-Hop-RL]] — Shows RL on purely rule-generated, fictional synthetic data teaches a transferable "knowledge composition" skill, lifting real-world multi-hop QA F1 by 56-131%
> - [[2510.19363|LoongRL]] — KeyChain data-synthesis recipe inducing an emergent plan-retrieve-reason-recheck pattern; a 14B model rivals o3-mini/DeepSeek-R1 on long multi-hop reasoning at 128K
> - [[2509.23657|RL-Cross-Lingual]] — Definitive multilingual training-recipe study, showing RL (unlike SFT) generalizes cross-lingually and trains better on non-English data

**Reward & Objective Design for Reasoning** — Reward-shaping and objective-function innovations for reasoning RL.
- [[2605.29198|GCPO]], [[2605.22817|VPO]], [[2605.21467|DelTA]], [[2605.16787|RLVR-Unlearnability]], [[2605.12227|dGRPO]], [[2605.11609|AntiSD]], [[2512.13106|TraPO-RL]], [[2510.22543|FAPO]], [[2506.18485|MeRF]], [[2506.17238|ether0]], [[2506.05997|SRU]], [[2506.01413|Instruction-Following-RL]], [[2505.21908|DRG-SAPPHIRE]], [[2505.21097|Thinker-RL]], [[2505.16368|SATURN]], [[2505.11792|SIRL]]

> [!star] Key Papers
> - [[2605.11609|AntiSD]] — Reframes self-distillation's per-token signal as conditional PMI, then reverses and JSD-bounds it to reward deliberation over shortcuts; 2-10x faster convergence and up to +11.5pts over GRPO
> - [[2605.29198|GCPO]] — Repurposes classifier-free guidance contrast into a per-token advantage weight, replacing GRPO's uniform credit assignment; beats GRPO/DAPO/VPPO across benchmarks
> - [[2510.22543|FAPO]] — Adaptively penalizes "flawed-positive" rollouts (correct answer, unreliable reasoning) via a lightweight GenRM, cutting flawed-positive rates by half+ while improving AIME accuracy

**Structured, Graph & Domain-Specific Reasoning** — Reasoning RL over structured representations, graphs, roles, and specialized domains.
- [[2605.31228|EchoRL]], [[2605.31159|TRB]], [[2605.28421|DenoiseRL]], [[2605.10663|Evolving-RL]], [[2603.07197|Re-squared]], [[2602.11549|NRT]], [[2512.18857|CORE-Concept]], [[2512.01925|Rectifying-LLM-Thought]], [[2510.12264|Belief-Deviation-Active-Reasoning]], [[2507.20187|MultiRole-R1]], [[2506.18841|LongWriter-Zero]], [[2505.20948|CtrlHGen]], [[2505.18499|G1-Graph-Reasoning]], [[2505.18098|PNLC]], [[2505.10446|DCoLT]], [[2503.09501|ReMA]], [[2502.06772|ReasonFlux]]

**Search-Augmented Reasoning** — Teaching LLMs to interleave reasoning with external search and retrieval, learned end-to-end via RL.
- [[2603.22293|TIPS-RL]], [[2602.21728|Explore-on-Graph]], [[2510.07958|A2Search]], [[2510.00861|Erasable-RL]], [[2509.24869|Retro-Star]], [[2505.04588|ZeroSearch]], [[2504.21776|WebThinker]], [[2503.19470|ReSearch]], [[2503.09516|Search-R1]], [[2503.05592|R1-Searcher]], [[2109.13202|MiniHack]]

> [!star] Key Papers
> - [[2503.09516|Search-R1]] — RL trains LLMs to autonomously interleave reasoning with search; outperforms pipeline RAG approaches
> - [[2505.04588|ZeroSearch]] — Trains LLMs to use search by simulating search engines with LLMs; zero real search calls needed

**Verification & Process Rewards** — Learning to verify reasoning steps and assign process-level rewards for more reliable training signals.
- [[2605.30290|STV]], [[2601.14209|InT]], [[2512.16917|GAR-Reasoner]], [[2510.24320|Critique-RL]], [[2509.26628|AttnRL]], [[2508.13755|DARS-Breadth]], [[2506.14245|CoT-Pass@K]], [[2506.09026|e3]], [[2506.05316|DOTS]], [[2504.19162|SPC]], [[2410.08146|PAV]], [[2408.15240|GenRM]], [[2011.07215|SoftGym]]

> [!star] Key Papers
> - [[2408.15240|GenRM]] — Reframes reward modeling as next-token prediction; generative verifiers outperform discriminative ones
> - [[2410.08146|PAV]] — Process Advantage Verifiers measure step-level progress; fine-grained credit assignment

**Failure Modes, Spurious Signals & Reward Hacking** — Cases where RLVR rewards mislead training or where the policy exploits shortcuts.
- [[2604.03993|Noisy-Supervision-Reasoning]], [[2512.20760|RLCausal]], [[2512.16912|RLVR-Clipping-Entropy]], [[2510.09259|Self-Critique-Contamination]], [[2509.04259|RL's-Razor]], [[2506.17219|RLIF-No-Free-Lunch]], [[2506.10947|Spurious-Rewards-RLVR]], [[2506.01347|Negative-Reinforcement-RLVR]], [[2505.18830|GRPO-Negative-Gradient]]

> [!star] Key Papers
> - [[2506.10947|Spurious-Rewards-RLVR]] — Foundational, most surprising finding: random or deliberately incorrect rewards drive Qwen-Math gains nearly matching ground-truth RLVR, revealing RLVR can amplify a pre-existing shortcut rather than teach anything new
> - [[2512.16912|RLVR-Clipping-Entropy]] — Strongest mechanistic evidence explaining spurious-reward gains; proves GRPO's clipping term acts as an implicit entropy minimizer rather than a real learning signal
> - [[2505.18830|GRPO-Negative-Gradient]] — Clearest exposition of a subtler failure, "Lazy Likelihood Displacement," where naive negative-gradient penalization suppresses correct reasoning tokens
> - [[2506.10947|Spurious-Rewards-RLVR]] — Shows RLVR can improve reasoning even with partially spurious rewards; robustness result

**Generalization, Transfer & Reasoning-Boundary Theory** — When and why RLVR generalizes beyond the training distribution, and where its reasoning-capability ceiling lies.
- [[2604.15306|Shortest-Path-Generalization]], [[2603.08660|Unsupervised-RLVR-Scale]], [[2510.11653|MATH-Beyond]], [[2509.21124|Reasoning-Potential]], [[2509.21016|RL-Grokking-DELTA]], [[2508.21188|Model-Task-Alignment]], [[2507.10532|RandomCalculation]], [[2506.19733|RL-Transfer-Study]], [[2505.11711|RL-Sparse-Subnetwork]], [[2504.13837|RLVR-Reasoning-Boundary]], [[2408.15332|RL-Math-Hardness-Study]]

> [!star] Key Papers
> - [[2504.13837|RLVR-Reasoning-Boundary]] — Shows RLVR raises pass@1 but shrinks pass@k at large k below the base model, revealing the ceiling is the base model's own support rather than new reasoning
> - [[2509.21016|RL-Grokking-DELTA]] — A staged dense-to-binary reward can carry a pass@K=0 task family to 100% via a grokking transition, but pins the ceiling precisely: transformative generalization near zero
> - [[2506.19733|RL-Transfer-Study]] — Largest-scale evidence (18 models) that RL gains transfer only across domains sharing reasoning structure and fail or reverse otherwise
> - [[2505.11711|RL-Sparse-Subnetwork]] — RL fine-tuning consistently activates sparse subnetworks; reveals structural changes in LLMs

**Training Dynamics & Mechanistic Analysis** — Mechanistic and empirical analysis of what happens inside the model during RLVR training.
- [[2603.22446|Token-Level-Shift-Analysis]], [[2601.22595|Uncertainty-Consistency-RLVR]], [[2512.23165|PEFT-for-RLVR]], [[2512.05962|DMVR]], [[2510.03669|Token-Hidden-Reward]], [[2509.24203|Group-Relative-REINFORCE-Analysis]], [[2509.22613|RL-Planning-Theory]], [[2509.21044|RL-Activation-Intensity]], [[2506.09967|Resa]], [[2506.04723|SPARKLE]], [[2506.04695|RL-Training-Dynamics-Analysis]], [[2505.20268|Outcome-Based-Online-RL]], [[2505.16826|KTAE]], [[1910.11956|Franka-Kitchen]]

**Internalized Reasoning & Latent Thought** — Moving reasoning from explicit text to internal latent representations, enabling faster and more efficient inference.
- [[2601.21598|ATP-Latent]], [[2601.18631|AdaReasoner]], [[2601.13562|Reasoning-as-Modality]], [[2601.05877|iReasoner]], [[2512.17206|Reasoning-Palette]], [[2512.07558|ReLaX]], [[2509.24251|LVR]], [[2509.19170|Noisy-Soft-Thinking]], [[2509.06160|REER]], [[2505.19092|LatentR3]], [[2505.16552|CoLaR]]

> [!star] Key Papers
> - [[2509.24251|LVR]] — Latent Visual Reasoning: autoregressive reasoning directly within visual representations, bypassing text
> - [[2601.13562|Reasoning-as-Modality]] — Treats reasoning traces as a separate modality; novel role-separated transformer architecture

> [!tip] The Self-Improving Loop
> The frontier is self-sustaining improvement: STaR to Quiet-STaR to Absolute Zero to R-Zero. Each step removes more human supervision. The endgame is models that propose their own problems, solve them, verify solutions, and improve — no human data at all.

---

## 5. Visual & Multimodal RL

Applying RL (especially GRPO) to teach VLMs to reason visually — a direct extension of the LLM reasoning paradigm to multimodal models. The largest and fastest-growing thread in RL research.

**Video & Temporal Visual R1** — R1-style RL for video/temporal reasoning.
- [[2603.26599|VGGRPO]], [[2511.13054|ViSS-R1]], [[2508.04416|VITAL]], [[2507.01949|Kwai-Keye-VL]], [[2505.13934|RLVR-World]], [[2505.12434|VIDEORFT]], [[2503.21776|Video-R1]]

> [!star] Key Papers
> - [[2503.21776|Video-R1]] — First framework to apply rule-based R1-style RL to video, introducing T-GRPO's contrastive temporal reward as the foundation others build on
> - [[2505.12434|VIDEORFT]] — Strongest reported results, beating GPT-4o on VSI-Bench and outranking contemporary R1 video models on most benchmarks
> - [[2511.13054|ViSS-R1]] — Clearest fix for the field's text-centric shortcut-learning problem, using self-supervised visual pretext tasks to force genuine visual grounding

**Spatial & Embodied Visual R1** — R1-style RL for spatial/embodied reasoning.
- [[2512.04069|SpaceTools]], [[2510.08531|SpatialLadder]], [[2508.11737|Ovis2.5]], [[2505.07062|Seed1.5-VL]], [[2503.20752|Reason-RFT]], [[2503.18470|MetaSpatial]], [[2503.12797|DeepPerception]]

> [!star] Key Papers
> - [[2503.18470|MetaSpatial]] — First RL framework to give VLMs inherent 3D spatial reasoning, eliminating costly post-hoc layout correction
> - [[2503.20752|Reason-RFT]] — Clearest exposition of the SFT-then-GRPO recipe, showing it generalizes far better than pure SFT under domain shift
> - [[2512.04069|SpaceTools]] — Strongest reported result, translating tool-augmented RL into an 86% real-robot manipulation success rate
> - [[2505.07062|Seed1.5-VL]] — ByteDance's production-grade multimodal reasoning model; SOTA on 38/60 benchmarks

**GUI & Mobile Agent R1** — R1-style RL for GUI grounding and mobile-agent control.
- [[2509.18119|MobileRL]], [[2508.04389|GuirlVG]], [[2505.15810|GUI-G1]], [[2505.12493|GUI-Shift]], [[2505.12370|SE-GUI]]

> [!star] Key Papers
> - [[2509.18119|MobileRL]] — sets new SOTA on full agentic mobile-task benchmarks (80.2% AndroidWorld, 53.6% AndroidLab), the strongest end-to-end task-automation result in the group
> - [[2505.12370|SE-GUI]] — highest grounding accuracy in the group (47.3% ScreenSpot-Pro), beating a 72B model with only a 7B model via dense rewards and self-evolutionary fine-tuning
> - [[2505.15810|GUI-G1]] — clearest diagnostic account of why naive R1-Zero-style RL fails for GUI grounding, giving the group's foundational mechanistic understanding

**Tool-Use, Multi-Agent & Long-Horizon R1** — R1-style RL for tool-calling, multi-agent routing, and long-horizon agentic tasks.
- [[2605.15198|ATLAS]], [[2604.02268|SKILL0]], [[2601.09667|MATTRL]], [[2601.07055|Dr.-Zero]], [[2601.03872|ATLAS]], [[2506.09033|Router-R1]], [[2505.08617|OpenThinkIMG]], [[2504.16129|MARFT]], [[2504.04736|SWiRL]]

> [!star] Key Papers
> - [[2504.04736|SWiRL]] — earliest and foundational: step-wise RL for multi-step tool use, showing process-based filtering drives strong cross-task, cross-tool generalization
> - [[2506.09033|Router-R1]] — foundational RL framework for multi-round LLM-as-router orchestration, beating 10+ baselines across seven QA benchmarks
> - [[2504.16129|MARFT]] — gives multi-agent LLM fine-tuning a principled RL-theoretic foundation, the clearest explanation of why single-agent RFT doesn't transfer to LaMAS

**Video Agent, Search & Interactive-Tool R1** — R1-style RL for video agents, search, and interactive tool environments.
- [[2603.22918|EVA-Video-Agent]], [[2603.02951|CGL]], [[2511.20785|LongVT]], [[2511.19773|VISTA-Gym]], [[2510.08480|Video-STAR]], [[2509.02479|SimpleTIR]], [[2509.01656|ReV-PT]], [[2507.19849|ARPO]], [[2506.24119|SPIRAL]]

> [!star] Key Papers
> - [[2507.19849|ARPO]] — earliest and broadest agentic RL algorithm here, using entropy-based adaptive rollout to beat GRPO/DAPO/Reinforce++ on 13 reasoning/search benchmarks with half the tool-call budget
> - [[2509.02479|SimpleTIR]] — diagnoses and fixes the core training-instability problem (distributional drift from tool feedback) underlying stable multi-turn tool-integrated RL across this whole group
> - [[2511.20785|LongVT]] — strongest video-agent-specific results, SOTA among open-source LMMs on long-video reasoning, narrowing the gap to proprietary models like GPT-4o and Gemini

**Foundational Visual RLVR Methods** — The core algorithmic lineage that established R1-style visual RL.
- [[2604.20328|HyLaR]], [[2603.23500|UniGRPO]], [[2603.22847|PEPO]], [[2603.09206|MM-Zero]], [[2504.07615|VLM-R1]], [[2503.23905|Hint-GRPO]], [[2503.17352|OpenVLThinker]], [[2503.07523|VisRL]], [[2503.07365|MM-Eureka]], [[2503.06749|Vision-R1]], [[2503.01785|Visual-RFT]]

> [!star] Key Papers
> - [[2503.01785|Visual-RFT]] — one of the earliest works adapting GRPO-based reinforcement fine-tuning with verifiable rewards from language to vision, establishing the paradigm the rest of the group builds on
> - [[2503.06749|Vision-R1]] — introduced the cold-start SFT + RL two-phase recipe extending DeepSeek-R1's reasoning-emergence paradigm to MLLMs, reaching 73.5% on MathVista with only 7B parameters
> - [[2503.07365|MM-Eureka]] — strongest reported results in the group (74.8 MathVista, 73.4 WeMath) via rule-based RL with online filtering, plus a fully open-sourced dataset/model/code release
> - [[2503.06749|Vision-R1]] — First R1-style RL for VLMs with visual CoT; opened the floodgate
> - [[2504.07615|VLM-R1]] — Stable, generalizable R1-style VLM training; the reference open-source implementation

**Production VLMs & Generation-Oriented Visual RL** — Named production-grade VLMs and image/generation-oriented RLVR models.
- [[2507.01006|GLM-4.5V]], [[2506.03569|MiMo-VL]], [[2505.15809|MMaDA]], [[2505.14677|Visionary-R1]], [[2505.13031|MindOmni]], [[2505.03981|X-Reasoner]], [[2505.00703|T2I-R1]], [[2504.18397|UV-CoT]], [[2504.16656|Skywork-R1V2]], [[2504.07491|Kimi-VL]]

> [!star] Key Papers
> - [[2507.01006|GLM-4.5V]] — production-grade VLM from Zhipu/Tsinghua achieving SOTA on 42 public benchmarks via a three-stage RLVR+RLHF pipeline, the strongest and broadest benchmark showing in the group
> - [[2504.07491|Kimi-VL]] — Moonshot's efficient MoE VLM matches or beats GPT-4o with only 2.8B activated parameters, showing RL-driven reasoning scales down to production-viable compute budgets
> - [[2505.15809|MMaDA]] — first unified diffusion architecture jointly handling text reasoning, understanding, and image generation via a diffusion-native GRPO, the paradigm-shifting foundation for generation-oriented RLVR here
> - [[2506.03569|MiMo-VL]] — Xiaomi's 7B model achieving SOTA visual reasoning; proves small models can reason

**Self-Improvement, Training-Free & Efficient Visual RLVR** — Label-free, test-time, and compute-efficient visual RLVR training strategies.
- [[2511.01191|Self-Harmony]], [[2510.03259|MASA]], [[2510.02752|Self-Aware-RL-for-LLMs]], [[2510.02263|RLAD]], [[2509.25541|Vision-Zero]], [[2509.15194|EVOL-RL]], [[2507.08838|wd1]], [[2506.08989|SwS]], [[2504.16084|TTRL]]

> [!star] Key Papers
> - [[2504.16084|TTRL]] — foundational method establishing test-time RL from majority-vote pseudo-rewards, spawning the whole self-improvement lineage this group builds on and critiques
> - [[2509.15194|EVOL-RL]] — diagnoses and fixes TTRL's core failure mode (majority-vote-induced entropy collapse) with a theoretically grounded novelty reward, recovering diversity and pass@16
> - [[2511.01191|Self-Harmony]] — strongest reported results (SOTA in 28/30 configs) via a harmonic-mean pseudo-label selector that solves the same majority-vote trap through cooperative self-play

**Reasoning Quality, Reward Design & Perception RL** — Reward-shaping, reflection, and perception-quality improvements for visual RLVR.
- [[2602.07605|Fine-R1]], [[2602.03120|QES]], [[2601.10094|V-Zero]], [[2601.09536|Omni-R1]], [[2509.12132|Reflection-V]], [[2507.20766|RRVF]], [[2507.16814|SOPHIA]], [[2507.16518|C2-Evo]], [[2506.07218|Perception-R1]], [[2506.04207|ReVisual-R1]], [[2505.24726|Reflect-Retry-Reward]], [[2505.17018|SophiaVL-R1]], [[2505.16854|TON]], [[2504.08837|VL-Rethinker]], [[2504.08672|Genius]]

**Visual Grounding & Referring Expression RL** — RL that grounds language in precise visual regions, points, and referring expressions.
- [[2603.22435|CaP-X]], [[2603.03197|SpeciaRL]], [[2602.23959|NV-CoT]], [[2602.23615|HART]], [[2602.21655|CCCaption]], [[2602.03733|RegionReasoner]], [[2601.21634|RSGround-R1]], [[2601.08834|FD-RL]], [[2601.04777|GeM-VG]], [[2512.10554|GETok]], [[2509.22647|CapRL]], [[2505.19702|Point-RFT]], [[2505.19255|VTool-R1]], [[2505.14231|UniVG-R1]]

> [!star] Key Papers
> - [[2505.14231|UniVG-R1]] — foundational reasoning-guided grounding RL (CoT-SFT cold-start + difficulty-aware GRPO) that later work like GeM-VG directly builds on and benchmarks against
> - [[2602.03733|RegionReasoner]] — strongest reported results (up to 80.7 AP) via reference-citation and global-local consistency rewards that curb hallucination and drift
> - [[2602.23615|HART]] — clearest diagnosis of the core RL-for-grounding failure mode (reward misspecification), halving incorrect-grounding-yet-correct-answer cases

**Spatial Reasoning & 3D/4D Understanding** — RL for 3D spatial relations, multi-view understanding, and spatial-reasoning benchmarks.
- [[2512.20617|SpatialTree]], [[2510.27606|Spatial-SSRL]], [[2507.13362|VLM-Spatial-Reasoning-RL]], [[2507.08306|M2-Reasoning]], [[2506.21656|SpatialReasoner-R1]], [[2506.21458|MINDCUBE]], [[2506.09965|VILASR]], [[2505.19094|SATORI]], [[2505.15879|GRIT]], [[2505.15804|STAR-R1]], [[2504.07954|Perception-R1-RL]]

> [!star] Key Papers
> - [[2512.20617|SpatialTree]] — first capability-centric hierarchical taxonomy unifying fragmented spatial benchmarks, with an "auto-think" RL strategy that lifts scores across every level
> - [[2506.21458|MINDCUBE]] — exposes VLMs' near-random performance on spatial mental modeling from limited views and shows SFT+RL cognitive-map training lifts accuracy from 47.62% to 70.67%
> - [[2506.09965|VILASR]] — paradigm-shifting "drawing to reason in space" approach interleaving visual drawing operations with text, reaching SOTA with an 18.4% average gain across five spatial-reasoning benchmarks
> - [[2505.15804|STAR-R1]] — State-of-the-art spatial reasoning by anchoring each CoT step to visual regions

**Video/Temporal Grounding, Segmentation & GUI-Document Spatial RL** — RL for temporal video grounding, pixel-level segmentation, and document/sketch spatial understanding.
- [[2607.02490|VRRL]], [[2605.15951|Group-Revision]], [[2605.14742|EARL]], [[2603.26499|AIRA2]], [[2603.25629|LanteRn]], [[2602.20630|TraqPoint]], [[2602.11730|STVG-R1]], [[2601.15224|PROGRESSLM]], [[2601.05688|SketchVL]], [[2512.15160|EagleVision]], [[2512.12633|DiG]], [[2511.05491|VST]], [[2507.05920|MGPO]], [[2507.05255|OVR]], [[2506.22624|Seg-R1]]

**Dynamic Visual Attention** — Teaching VLMs to adaptively look at images — zooming, cropping, and selecting visual regions via RL-learned policies.
- [[2603.27494|RL-Cropping]], [[2602.11858|ZwZ]], [[2602.08241|SAYO]], [[2601.13942|GoG]], [[2512.03794|AdaptVision]], [[2511.19820|CropVLM]], [[2509.21991|ERGO]], [[2508.06259|SIFThinker]], [[2507.13348|VisionThink]], [[2506.17218|Mirage]], [[2505.24025|DINO-R1]], [[2505.23727|PixelThink]], [[2505.21457|ACTIVE-O3]], [[2505.16192|VLM-R3]], [[2505.15436|Adaptive-CoF]]

> [!star] Key Papers
> - [[2505.16192|VLM-R3]] — Dynamic visual region selection via RL; models learn where to look
> - [[2602.11858|ZwZ]] — "Zooming without Zooming": RL teaches VLMs to mentally zoom without changing input resolution
> - [[2505.24025|DINO-R1]] — Group Relative Query Optimization for vision foundation models; extends RL beyond language heads

**Visual Reasoning Segmentation** — Zero-shot and reasoning-guided segmentation driven by RL rather than supervised masks.
- [[2603.24322|HeuSCM]], [[2603.04002|DPAD]], [[2602.09463|SpotAgent]], [[2510.21311|FineRS]], [[2505.22596|SAM-R1]], [[2505.12081|VisionReasoner]], [[2503.06520|Seg-Zero]]

> [!star] Key Papers
> - [[2503.06520|Seg-Zero]] — Pure RL framework for reasoning segmentation; emergent CoT for segmentation without supervised masks

**Temporal Localization & Long-Video Understanding** — RL for locating events in time and reasoning over long-form video.
- [[2605.01324|VideoThinker]], [[2603.25942|SDRL]], [[2602.22932|MSJoE]], [[2602.20913|LongVideo-R1]], [[2601.19686|Video-KTR]], [[2512.06810|MMDuet2]], [[2512.03963|TempR1]], [[2511.19524|VideoChat-M1]], [[2511.16669|VANS]], [[2511.05489|TimeSearch-R]], [[2510.23473|Video-Thinker]], [[2510.20470|Conan]], [[2508.07388|Invert4TVG]]

> [!star] Key Papers
> - [[2512.03963|TempR1]] — unified multi-task RL achieving SOTA temporal localization across five distinct tasks simultaneously, showing joint optimization generalizes better than single-task RL
> - [[2511.19524|VideoChat-M1]] — multi-agent collaborative-policy-planning framework, beating Gemini 2.5 Pro by 3.6% and GPT-4o by 15.6% on LongVideoBench with far fewer frames and parameters
> - [[2511.05489|TimeSearch-R]] — reformulates temporal search as interleaved text-video RL with self-verification, more than tripling the prior best F1 on Haystack-LVBench

**Video Evidence, Frame-Selection, Egocentric & Anomaly Reasoning** — RL for evidence grounding, frame selection, egocentric video, and anomaly/4D scene reasoning.
- [[2604.16893|EasyVideoR1]], [[2604.04379|RLER]], [[2603.00515|MLLM-4D]], [[2603.00461|ReMoT]], [[2512.22315|VideoZoomer]], [[2511.06281|VideoSSR]], [[2510.23569|EgoThinker]], [[2510.15440|Evidence-Purity-Video]], [[2510.07915|MARC]], [[2510.06077|VER-Video-Evidence]], [[2509.24304|FrameThinker]], [[2509.23652|ReWatch-R1]], [[2508.06317|URPA]], [[2506.09079|VidBridge-R1]], [[2506.03340|ArrowRL]], [[2505.19877|Vad-R1]], [[2505.19000|VerIPO]], [[2504.01805|SpaceR]]


**Multi-Image & Document Reasoning** — RL for reasoning across multiple images, documents, and complex visual inputs.
- [[2605.01882|Chart-FR1]], [[2602.00574|Modal-Mixed-CoT]], [[2512.24297|FIGR]], [[2510.09733|EVisRAG]], [[2507.00748|Multi-Image-Grounding-RL]], [[2506.22434|MiCo]], [[2506.14907|PeRL]], [[2505.22019|VRAG-RL]], [[2505.14362|DeepEyes]]

> [!star] Key Papers
> - [[2505.22019|VRAG-RL]] — RL teaches VLMs to understand visually rich documents via retrieval-augmented generation
> - [[2505.14362|DeepEyes]] — VLMs perform "thinking with images" by dynamically integrating visual re-observation into reasoning

**Self-Rewarding & Self-Play** — Self-reward, self-play, and self-critique loops.
- [[2603.08403|SPIRAL]], [[2602.04837|GEA]], [[2512.22545|SR-MCR]], [[2512.18552|SSR]], [[2510.24684|SPICE]], [[2510.23595|MAE]], [[2509.25787|Self-Evolving-IQA]], [[2505.23380|UniRL]]

> [!star] Key Papers
> - [[2510.24684|SPICE]] — foundational corpus-grounded self-play paradigm that solves the hallucination-amplification and information-symmetry failures plaguing prior ungrounded self-play methods
> - [[2512.18552|SSR]] — strongest reported results, using adversarial bug-injection/bug-solving self-play on real repositories to beat human-curated-data RL baselines by +10.4 pts on SWE-bench Verified
> - [[2512.22545|SR-MCR]] — clearest articulation of the self-rewarding idea, combining five intrinsic tool-based process signals to avoid the "self-delusion" of LLM-as-judge rewards

**Embodied, Spatial & Action-Oriented Visual RL** — RL for physically/spatially grounded visual tasks — panoramic navigation, video segmentation, and embodied action.
- [[2602.21992|PanoEnv]], [[2601.19099|m2sv]], [[2601.02356|Talk2Move]], [[2511.16077|VideoSeg-R1]], [[2511.11113|VIDEOP2R]], [[2510.09606|SpaceVista]], [[2507.16815|ThinkAct]], [[2505.23747|Spatial-MLLM]], [[2505.23678|ViGoRL]], [[2505.23590|Jigsaw-R1]]

> [!star] Key Papers
> - [[2507.16815|ThinkAct]] — dual-system RL framework directly grounds reasoning in robot actions, driving the strongest embodied results (84.4% LIBERO) and emergent self-correction
> - [[2505.23678|ViGoRL]] — foundational grounded-RL paradigm anchoring each reasoning step to explicit image coordinates, inducing human-like visual behaviors absent from vanilla GRPO
> - [[2505.23747|Spatial-MLLM]] — first to fuse a visual geometry foundation model with an MLLM for RL-tuned spatial reasoning, setting SOTA on VSI-Bench purely from 2D video

**General & Applied Visual Reasoning Methods** — Broader visual reasoning RL methods spanning coding, editing, and general multimodal tasks.
- [[2604.20705|SSL-R1]], [[2603.19370|VAMPO]], [[2603.03857|DeepScan]], [[2603.02511|Unveiler]], [[2512.23169|REVEALER]], [[2512.17312|CodeDance]], [[2511.18373|MASS]], [[2510.24285|ViPER]], [[2510.23925|LaCoT]], [[2509.07969|Mini-o3]], [[2506.02096|SynthRL]], [[2505.14246|Visual-ARFT]]

> [!star] Key Papers
> - [[2505.14246|Visual-ARFT]] — earliest and foundational work establishing verifiable-reward GRPO fine-tuning for visual agentic tool use, introducing the MAT benchmark that later methods build on
> - [[2509.07969|Mini-o3]] — sets the open-source state of the art for multi-turn visual search via its thought-action-observation loop, with "over-turn masking" enabling test-time scaling to tens of interaction turns
> - [[2603.03857|DeepScan]] — training-free bottom-up scanning paradigm that most clearly demonstrates the group's core idea, beating even RL-trained and much larger models while being faster

**Agentic Multimodal RL Frameworks** — Multi-turn, tool-using, and driving/shopping/search agent frameworks trained with multimodal RL.
- [[2511.18437|PEARL]], [[2510.23038|TIR-Judge]], [[2510.22832|HRM-Agent]], [[2510.19245|See-Think-Act-Shopper]], [[2510.01132|Multi-turn-Agentic-RL-Guide]], [[2509.26626|RSA]], [[2509.22643|VLA-Reasoner]], [[2509.01055|VerlTool]], [[2508.20722|rStar2-Agent]], [[2508.13167|CoA]], [[2508.09736|M3-Agent]], [[2508.07976|ASearcher]], [[2508.03680|Agent-Lightning]], [[2507.20879|DriveAgent-R1]], [[2506.21669|SEEA-R1]], [[2506.06122|ROLL]]

> [!star] Key Papers
> - [[2509.01055|VerlTool]] — foundational open-source framework unifying agentic RL with tool use, fixing the fragmented, synchronous, text-only infrastructure that held back the whole ecosystem
> - [[2508.20722|rStar2-Agent]] — strongest reported result in the group: a 14B model trained with GRPO-RoC beats 671B DeepSeek-R1 on AIME24 in just 510 RL steps
> - [[2508.03680|Agent-Lightning]] — clearest, most paradigm-shifting core idea: fully decouples RL training from agent execution, letting any existing agent be trained with near-zero code changes

**Reward Design, Calibration & Uncertainty for Multimodal RL** — Reward-shaping, confidence calibration, and boundary/uncertainty-aware objectives for multimodal RL.
- [[2603.12149|CDRL-Confidence]], [[2602.21628|RuCL]], [[2602.21158|SELAUR]], [[2602.20197|CalibRL]], [[2602.13949|ERL]], [[2602.11241|Active-Zero]], [[2512.20675|VLM-Reward-Objectives]], [[2510.20607|Compositional-Energy-Minimization]], [[2510.02240|RewardMap]], [[2509.25848|VAPO-Vision-Anchored]], [[2507.21053|FPO]], [[2507.06448|PAPO]], [[2506.01713|SRPO-Reflection]], [[2505.23585|OPO]], [[2505.23224|MMBoundary]]

> [!star] Key Papers
> - [[2507.06448|PAPO]] — traced 67% of MLLM reasoning errors to bad perception and folded a perception-aware KL loss directly into GRPO/DAPO
> - [[2509.25848|VAPO-Vision-Anchored]] — names "visual forgetting" (attention to the image decays over long CoT) and fixes it with verifiable visual-anchor claims
> - [[2603.12149|CDRL-Confidence]] — strongest reported results (79.5% MathVista, 66.3% MMMU), closing the loop between training-time calibration and confidence-driven test-time scaling

**Self-Evolving, Memory & Experience-Driven Multimodal Agents** — Multimodal agents that bootstrap curricula, build memory, or self-evolve through experience.
- [[2603.29493|MemFactory]], [[2602.23802|EMO-R3]], [[2602.08234|SkillRL]], [[2602.02488|RLAnything]], [[2601.10825|Societies-of-Thought]], [[2601.01483|ADPO]], [[2512.19133|WorldRFT]], [[2512.18215|MSSR]], [[2511.16166|EvoVLA]], [[2511.14759|RECAP]], [[2511.11007|VisMem]], [[2510.16079|EVOLVER]], [[2510.08558|Early-Experience]], [[2509.24527|Dreamer-4]]

> [!star] Key Papers
> - [[2511.14759|RECAP]] — Physical Intelligence's π*0.6 doubles throughput and halves failure rates from deployed-robot experience, 13 hours of unattended real-world espresso-making
> - [[2511.16166|EvoVLA]] — fixes "stage hallucination" with an explicit long-horizon memory module and shows real sim-to-real transfer
> - [[2511.11007|VisMem]] — cognitively-grounded dual short-term/long-term latent vision memory that recovers visual grounding lost over long generations

**World-Model, VLA & Embodied-Adjacent Multimodal RL** — Multimodal RL tied to world models, VLA action generation, and embodied energy-based objectives.
- [[2512.14666|EVOLVE-VLA]], [[2512.13644|DexWM]], [[2512.09924|ReViSE]], [[2510.19307|RIL]], [[2510.12693|ERA]], [[2510.11369|Reasoning-as-Representation]], [[2510.10603|EA4LLM]], [[2510.09285|VPPO]], [[2510.08191|Training-Free-GRPO]], [[2507.07969|Q-chunking]], [[2507.02092|EBT]], [[2506.10943|SEAL]]

> [!star] Key Papers
> - [[2507.07969|Q-chunking]] — redefines the Q-function over action chunks for unbiased n-step backups, now a building block under many VLA training recipes
> - [[2512.13644|DexWM]] — 83% zero-shot real-world dexterous grasping with zero real robot training data, via a world model over human egocentric video
> - [[2512.14666|EVOLVE-VLA]] — replaces the oracle reward RL needs with a learned progress estimator for test-time training, breaking the 0% barrier on unseen tasks

**Named Multimodal Models & Reasoning-Quality Enhancements** — Flagship multimodal models and reasoning/hallucination-robustness enhancements.
- [[2605.13467|PDCR]], [[2604.03179|Hallucination-as-Cue]], [[2604.00479|MUPO]], [[2603.25720|R-C2]], [[2603.24139|TSRL-Deepfake]], [[2603.18886|RLLM]], [[2603.17693|SynRL]], [[2603.05256|Wiki-R1]], [[2603.01106|DIVA-GRPO]], [[2602.02150|ECHO]], [[2601.06794|ECHO]], [[2512.24330|SenseNova-MARS]], [[2510.26583|Emu3.5]], [[2508.11630|Thyme]], [[2507.20534|Kimi-K2]], [[2506.01078|GThinker]], [[2505.19223|LLaDA-1.5]]

> [!star] Key Papers
> - [[2510.26583|Emu3.5]] — flagship native next-token-prediction model (34.1B params, 13T tokens of video) beating Gemini 2.5 Flash Image 65.5-67.1% of the time
> - [[2508.11630|Thyme]] — lets the MLLM write and execute Python code to manipulate its own image input, beating larger closed models across ~20 benchmarks
> - [[2512.24330|SenseNova-MARS]] — interleaves image search, text search, and image-crop tools in one reasoning loop via a novel BN-GSPO algorithm, matching Gemini-3-Flash on HR-MMSearch

**Applied & Domain-Specific Multimodal Reasoning** — Code, editing, auditing, and cold-start applications of multimodal RL.
- [[2601.02825|SketchThinker-R1]], [[2512.19554|CARE]], [[2512.16921|AuditDM]], [[2512.03746|CodeVision]], [[2511.16334|OpenMMReasoner]], [[2510.17045|V-Reason]], [[2509.21871|AesCoT]], [[2508.10874|SSRL]], [[2508.05612|Shuffle-R1]], [[2506.18369|RePIC]], [[2505.22651|Sherlock]], [[2505.22453|MM-UPT]], [[2505.22334|Multimodal-RL-Cold-Start]], [[2505.18600|CoZ]]


**RL-Distilled Compact Models** — Distilling RL-trained reasoning into smaller, deployable models.
- [[2510.12798|Rex-Omni]], [[2505.11221|LVLM2P]], [[2504.15777|Tina]], [[2504.11468|VLAA-Thinker]], [[2504.07934|ThinkLite-VL]]

> [!star] Key Papers
> - [[2504.07934|ThinkLite-VL]] — Visual reasoning models achieving SOTA with significantly fewer parameters via distillation
> - [[2504.15777|Tina]] — Highly cost-effective approach to visual reasoning; proves RL-distilled small models are viable

**Visual Planning & Tool Use** — RL teaches VLMs to plan visually, use tools, and generate executable visual programs.
- [[2607.12800|UniVR]], [[2604.01600|MM-ReCoder]], [[2603.14117|SIEVE]], [[2602.11073|VILAVT]], [[2511.19661|CodeV]], [[2508.13587|Chart-to-Code-RL]], [[2505.20289|VisTA]], [[2505.11409|VPRL]]

> [!star] Key Papers
> - [[2505.11409|VPRL]] — Visual Planning via RL: multi-step reasoning solely through sequences of images
> - [[2511.19661|CodeV]] — Code-based visual agent with Tool-Aware Policy Optimization; addresses unfaithful visual reasoning

**Embodied Visual Reasoning** — RL for visual reasoning in physically grounded, 3D settings — bridging perception and action.
- [[2602.00795|DVLA-RL]], [[2512.13660|RoboTracer]], [[2511.20814|SPHINX]], [[2511.20351|HVS]], [[2508.07804|Pose-RFT]], [[2507.10548|EmbRACE-3K]], [[2506.08011|ViGaL]], [[2504.12680|Embodied-R]]

> [!star] Key Papers
> - [[2504.12680|Embodied-R]] — Enables foundation models to perform embodied spatial reasoning by combining CoT with physical grounding
> - [[2507.10548|EmbRACE-3K]] — 3,000 embodied reasoning tasks in photorealistic environments; benchmark for embodied visual RL

**Multimodal Benchmarks for RL** — Benchmarks specifically designed to evaluate RL-trained visual reasoning.
- [[2602.08346|ThinkWithImages-PRMBENCH]], [[2509.26601|MENLO]], [[2506.14965|GURU]], [[2505.24760|REASONING-GYM]], [[2505.15966|Pixel-Reasoner]], [[2504.15279|VisuLogic]]

> [!star] Key Papers
> - [[2504.15279|VisuLogic]] — Evaluates true visual reasoning (not text shortcuts) through carefully designed visual logic puzzles
> - [[2505.24760|REASONING-GYM]] — 100+ procedurally generated environments with verifiable rewards; the gym for RL reasoning research

**General Multimodal RL Infrastructure** — Cross-cutting tools, frameworks, and analysis for multimodal RL research.
- [[2604.24661|ACO-MoE]], [[2603.18656|SCALe-SFT]], [[2602.20739|PyVision-RL]], [[2602.14697|E-SPL]], [[2602.12395|Frankenstein-RL-Analysis]], [[2602.04145|BIS]], [[2601.05242|GDPO]], [[2601.00215|Sight-to-Insight]]

> [!star] Key Papers
> - [[2602.12395|Frankenstein-RL-Analysis]] — Mechanistic analysis of how RL improves VLMs; reveals which components change and why
> - [[2601.00215|Sight-to-Insight]] — Identifies that visual perception, not reasoning, primarily limits multimodal LLM performance

> [!tip] The Visual RL Explosion
> After Vision-R1 (March 2025), visual RL papers appeared at a rate of 10+ per week. The core recipe is simple: GRPO + VLM + verifiable visual task. The frontier is dynamic visual attention (learning *where* to look) and latent visual reasoning (reasoning without generating text).

---

## 6. Reward Modeling & Verification

Learning and designing reward signals for RL training — from hand-crafted rewards through learned reward models to reasoning-based verification. The quality of the reward model is the ceiling for RL performance.

**Foundational RLHF Papers** — The landmark 2022-2023 papers that established RLHF as the standard technique for aligning LLMs with human preferences, and first quantified its failure modes.
- [[2303.08774|GPT-4]], [[2210.10760|RM-Overoptimization]], [[2204.05862|HH-RLHF]], [[2203.02155|InstructGPT]], [[1706.03741|Deep RL from Human Preferences]]

> [!star] Key Papers
> - [[1706.03741|Deep RL from Human Preferences]] — the origin of the paradigm: first to show a reward model learned from pairwise human preferences can drive deep RL, cutting feedback cost ~1000x
> - [[2203.02155|InstructGPT]] — the canonical SFT to reward model to PPO recipe the field still cites, where a 1.3B aligned model beat a 175B unaligned one
> - [[2210.10760|RM-Overoptimization]] — derives scaling laws for Goodhart's Law in RLHF, showing exactly how optimizing against a proxy reward model degrades true performance

**Text/LLM Process Reward Models** — Step-level reward models for text-based LLM reasoning.
- [[2604.24583|Perceval]], [[2604.03037|ARM]], [[2601.18533|RLVRR]], [[2505.11227|RL-Induces-PRM]], [[2505.02387|RM-R1]], [[2504.16828|THINKPRM]], [[2504.15275|PURE]], [[2504.02495|DeepSeek-GRM]], [[2503.13551|HRM]], [[2305.20050|PRM800K]], [[2110.14168|GSM8K]]

> [!star] Key Papers
> - [[2305.20050|PRM800K]] — the founding paper of process supervision itself, still the clearest case for why step-level feedback beats final-answer-only reward
> - [[2505.11227|RL-Induces-PRM]] — shows pure outcome-based RL implicitly induces strong PRM capability, challenging the assumption that explicit process supervision is necessary
> - [[2504.15275|PURE]] — pinpoints the mechanistic root cause of PRM-based RL instability (summation-form vs. min-form credit assignment), with a 3x training-efficiency gain
> - [[2305.20050|PRM800K]] — "Let's Verify Step by Step": the foundational process supervision result, showing step-level reward beats outcome-level supervision on MATH
> - [[2504.02495|DeepSeek-GRM]] — Self-Principled Critique Tuning: point-wise reward models with self-generated principles
> - [[2504.16828|THINKPRM]] — Generative PRM enabling LLMs to provide verbalized, step-level evaluation

**Multimodal & Applied Process Reward Models** — Step-level reward models for vision-language, web, and applied domains.
- [[2605.02073|Search-Driven-Reward-RL]], [[2601.21872|WebArbiter]], [[2512.03126|SymVAE]], [[2510.06217|TaTToo]], [[2509.26578|CRM-Conditional-Reward]], [[2509.23250|VL-PRM]], [[2509.19199|iStar]], [[2506.23235|EndoRM]], [[2506.13888|VL-GenRM]], [[2506.02095|CycleReward]], [[2503.10291|VisualPRM]]

> [!star] Key Papers
> - [[2506.23235|EndoRM]] — Reveals powerful reward models are already latent within any LLM; no separate training needed

**Reward Model Surveys & Analysis** — Understanding what reward models learn, how they fail, and how to improve them.
- [[2604.07480|Active-RM-Inference]], [[2512.23461|DIR-Reward]], [[2510.17793|Foundational-Evaluators]], [[2510.15839|Correlated-Reward-Models]], [[2510.02850|BayesianRouter]], [[2509.21798|CARB]], [[2506.07326|Reward-Model-Interpretability]], [[2504.12328|Reward-Model-Survey]], [[2504.06020|Reward-Decomposition-RLHF]], [[2503.15477|Reward-Model-Teacher-Analysis]], [[2306.05685|MT-Bench]]

> [!star] Key Papers
> - [[2504.12328|Reward-Model-Survey]] — Comprehensive survey consolidating RM research in the LLM era; introduces unified taxonomy
> - [[2306.05685|MT-Bench]] — Established LLM-as-a-judge as a valid proxy for human preference, now a standard reward-quality benchmark

**General & Text Outcome Reward Models** — Reward models that evaluate full reasoning chains and final outcomes for text-based tasks, including reward-free/verifier-free alternatives.
- [[2607.24900|PARED]], [[2509.21319|RLBFF]], [[2507.18624|RLCF]], [[2507.07375|SMORM]], [[2507.03112|RLVER]], [[2507.01352|Skywork-Reward-V2]], [[2506.18254|RLPR]], [[2506.10128|ViCrit]], [[2506.03637|RewardAnything]], [[2505.22338|Text2Grad]], [[2505.21493|VeriFree]], [[2505.15801|VerifyBench]], [[2505.15034|RL-Tango]], [[2505.14674|RRM]], [[2505.03318|UNIFIEDREWARD-THINK]], [[2503.17338|Reward-Features-Model]], [[2502.00814|Rc-BT]], [[2408.10858|CenRA]]

> [!star] Key Papers
> - [[2507.01352|Skywork-Reward-V2]] — an 8B model trained on 40M curated preference pairs beats a 70B model by 14.8 points across seven RM benchmarks
> - [[2507.18624|RLCF]] — contrarian, paradigm-shifting angle: automatically generated instruction-specific checklists outperform reward models entirely, with zero human annotation
> - [[2509.21319|RLBFF]] — bridges RLHF's flexibility and RLVR's precision via binary, principle-based feedback, matching proprietary-model alignment at a fraction of inference cost
> - [[2505.03318|UNIFIEDREWARD-THINK]] — First unified reasoning reward model; evaluates all modalities with explicit chain-of-thought
> - [[2506.03637|RewardAnything]] — Reward models that follow natural language principles; infinitely customizable
> - [[2505.21493|VeriFree]] — Trains LLMs for general reasoning without any verifier; uses self-generated training signal
> - [[2506.18254|RLPR]] — Verifier-free RL that enables reasoning without external verification

**Agentic, Tool-Use & Self-Evolving Reward Models** — Reward/verifier models embedded in agent loops that use tools or evolve through self-generated experience.
- [[2607.05391|LLM-as-a-Verifier]], [[2606.03980|Skill-RM]], [[2604.16004|AgentV-RL]], [[2604.11626|RationalRewards]], [[2512.21919|SWE-RM]], [[2512.05111|ARM-Thinker]], [[2511.19900|Agent0-VL]], [[2511.16672|EvoLMM]], [[2511.01758|RLAC]], [[2510.23596|BR-RM]], [[2510.14176|ARM-FM]], [[2510.08696|LENS]], [[2510.07242|HERO]]

> [!star] Key Papers
> - [[2607.05391|LLM-as-a-Verifier]] — a single verification framework spanning coding, robotics, and medical benchmarks, with a novel O(Nk) tournament algorithm replacing pairwise comparison
> - [[2511.16672|EvoLMM]] — fully self-evolving Proposer-Solver loop with zero human supervision and no external reward model, via a continuous self-consistency signal
> - [[2604.16004|AgentV-RL]] — a 4B agentic, Python-interpreter-grounded verifier beats a 70B reward model by 25.2 points on MATH500
> - [[2604.16004|AgentV-RL]] — Forward/Backward bidirectional agentic verifier with Python-tool integration; beats 70B INF-ORM by 25.2pp on MATH500 with only 4B params
> - [[2510.07242|HERO]] — Integrates sparse verifier signals with dense generative rewards; best of both worlds
> - [[2511.19900|Agent0-VL]] — Self-evolving vision-language agent integrating tool usage into reward learning

**Domain-Specific & Applied Reward Models** — Reward models specialized to particular application domains — editing, robotics, recommendation, and evaluation.
- [[2607.21655|Progress Reward Modeling Survey]], [[2603.16253|EVPV]], [[2603.02115|Robometer]], [[2602.16802|RefEval]], [[2602.12116|P-GenRM]], [[2511.10648|SCS]], [[2511.09158|CRM]], [[2510.15242|DWRL]], [[2509.22807|MTRec]], [[2508.01539|HALO-Nav]], [[2406.16258|MEReQ]]

**Image/Editing & Generation Reward Models** — Reward models for image generation, editing, and multi-modal generative quality.
- [[2607.00483|VLM-AR3L]], [[2604.27505|Edit-R1]], [[2510.01010|ImageDoctor]], [[2509.23909|EditScore]], [[2506.06970|MAPLE]], [[2505.18531|Generative-RLHF-V]], [[2505.02835|R1-Reward]], [[2503.21745|3DGen-Bench]]

> [!star] Key Papers
> - [[2509.23909|EditScore]] — model + EditReward-Bench benchmark + RL recipe together; EditScore-72B beats even GPT-5 on preference prediction
> - [[2510.01010|ImageDoctor]] — shifts from scalar-only scoring to a "look-think-predict" process that outputs pixel-level flaw heatmaps for dense, spatially-grounded reward
> - [[2604.27505|Edit-R1]] — first to make a non-differentiable, verifier-based reasoning reward model work inside RLHF via an adapted GRPO

**Spatial, Motion & Physical Reward Design** — Reward signals grounded in spatial relations, motion, and physical plausibility.
- [[2605.06507|MARBLE-RL]], [[2603.25108|MSRL]], [[2603.22228|SpatialReward-Verifiable]], [[2603.01694|MVR]], [[2602.24233|SpatialReward]], [[2602.11393|Visual-Motion-Pref-Modeling]], [[2602.11124|PhyCritic]], [[2601.04033|REACT-Video]]

> [!star] Key Papers
> - [[2602.24233|SpatialReward]] — 95.77% accuracy beating GPT-5 on spatial preference prediction, lifting FLUX.1-dev's in-domain spatial score from 2.18 to 7.81
> - [[2602.11124|PhyCritic]] — two-stage RLVR physics-aware critic with self-referential finetuning; judging physics also improves the model's own physical reasoning as a policy
> - [[2603.01694|MVR]] — multi-view video-text similarity with automatically-decaying reward shaping, solving occlusion issues that plague single-image VLM rewards

**Preference, Perception & Video Reward Models** — Perceptual-quality and preference-modeling rewards for images and video.
- [[2512.22647|FinPercep-RM]], [[2512.08889|VALOR]], [[2511.00609|PreferThinker]], [[2509.16127|BaseReward]], [[2509.15607|PRIMT]], [[2306.00958|LIV]], [[2302.08242|Reward-Tuning-CV]]

> [!star] Key Papers
> - [[2302.08242|Reward-Tuning-CV]] — Pioneered applying RL reward tuning to computer vision tasks

**Calibration & Safety** — Reward models that are well-calibrated, safe, and resistant to reward hacking.
- [[2607.18966|Contrastive SDF]], [[2605.12474|Rubric-RL-Diagnostic]], [[2604.12086|Robust-Reward-Hacking]], [[2604.04648|Caution-BoN]], [[2602.04755|LLM-Abstention]], [[2511.17879|GAPT]], [[2507.16806|RLCR]], [[2505.16186|SafeKey]], [[2503.02623|Rewarding-Doubt]], [[2412.09544|POWER-DL]]

> [!star] Key Papers
> - [[2505.16186|SafeKey]] — Enhances safety for Large Reasoning Models without sacrificing reasoning performance
> - [[2507.16806|RLCR]] — Calibration Rewards: trains LLMs to know what they know and express appropriate confidence

> [!tip] The Reward Model Hierarchy
> Outcome rewards (right/wrong) are simple but coarse. Process rewards (step-by-step) are precise but expensive. Reasoning reward models (UNIFIEDREWARD-THINK, RRM) get the best of both: dense step-level signal from a model that reasons about reasoning. The endgame is EndoRM — the reward model is already inside the LLM.

---

## 7. Agentic RL

RL for multi-turn, tool-using, and self-evolving agents — the bridge between reasoning models and autonomous systems. These agents don't just answer questions; they take actions, observe results, and adapt.

**Multi-Turn Training Foundations & Coordination** — Core multi-turn RL training frameworks, environments, and multi-agent coordination/memory mechanisms.
- [[2604.06268|RAGEN-2]], [[2603.17621|Complementary-RL]], [[2603.05218|KARL]], [[2602.23008|EMPO-squared]], [[2602.17930|MIRA-RL]], [[2602.14926|MAC-AMP]], [[2512.20092|Memory-T1]], [[2512.09706|CrossHA]], [[2512.04388|Conductor]], [[2511.22235|CES-Scheduler]], [[2511.07327|IterResearch]], [[2510.10197|Environment-Tuning]], [[2509.08755|AgentGym-RL]], [[2507.21046|Self-Evolving-Agents-Survey]], [[2504.20997|LLM-PSRL]], [[2504.20073|RAGEN]], [[2504.16078|LLM-Greedy-Agents]], [[2406.04151|AgentGym]]

> [!star] Key Papers
> - [[2504.20073|RAGEN]] — introduces StarPO and identifies the "Echo Trap" instability that motivated most later multi-turn RL work, including RAGEN-2 in this same list
> - [[2504.16078|LLM-Greedy-Agents]] — systematically isolates three failure modes (greediness, frequency bias, knowing-doing gap) in RL-fine-tuned decision-making
> - [[2512.04388|Conductor]] — a 7B orchestrator trained end-to-end with RL to direct multi-agent workflows, hitting SOTA above any single frontier model
> - [[2406.04151|AgentGym]] — Cross-environment agent training with behavioral cloning + reward-weighted RL
> - [[2603.17621|Complementary-RL]] — Co-evolutionary loop between policy actor and experience extractor; 1.3x performance with 2x fewer actions
> - [[2603.05218|KARL]] — Off-policy RL for knowledge agents; Pareto-optimal on enterprise search, 37% shorter trajectories

**Web/Browser & Applied Agent Domains** — Multi-turn agentic RL applied to web browsing, computer use, shopping, and other applied domains.
- [[2604.23626|GraphPlanner]], [[2603.05044|WebFactory]], [[2510.18798|WebSeer]], [[2508.14040|ComputerRL]], [[2507.17842|Shop-R1]], [[2507.04103|LLM-Web-Agent-Diagnosis]], [[2505.23885|OWL-Workforce]], [[2505.22648|WebDancer]], [[2505.19591|Puppeteer-Agent]], [[2504.03206|CURIO]], [[2503.11739|CoLLMLight]]

**Skill/Memory-Based & Self-Play Evolution** — Self-evolving agents that use skill libraries, external memory, or self-play to improve.
- [[2607.22529|Skill-SP]], [[2605.15155|SDAR]], [[2605.06614|SkillOS]], [[2603.25111|SEVerA]], [[2603.18743|Memento-Skills]], [[2602.21633|SC-VLA]], [[2602.20133|AdaEvolve]], [[2602.06508|World-VLA-Loop]], [[2602.00359|A-EVOLVE]], [[2601.03192|MemRL]], [[2510.18821|Search-Self-play]], [[2510.13220|EvoTest]], [[2510.09577|Dyna-Mind]], [[2510.08529|CoMAS]]

> [!star] Key Papers
> - [[2605.06614|SkillOS]] — an RL-trained skill curator (not just a zero-shot LLM curator) that learns to insert/update/delete skills, giving rise to emergent "meta-strategy skills"
> - [[2601.03192|MemRL]] — decouples a frozen LLM from a plastic episodic memory, casting retrieval itself as an RL problem to solve the stability-plasticity dilemma
> - [[2510.18821|Search-Self-play]] — +26.4 points average for Qwen2.5-7B-Base via a genuine proposer/solver co-evolution loop
> - [[2603.18743|Memento-Skills]] — Skill library as external memory; agents evolve without parameter updates, +13.7pp on GAIA

**Applied Self-Evolving Agents** — Self-evolving agents applied to specific domains — UI control, scientific discovery, and presentation generation.
- [[2607.21461|AREX]], [[2606.03963|AgenticRL]], [[2604.20987|Co-Evolve-Agents]], [[2603.24533|UI-Voyager]], [[2603.07642|Helix-Scientific]], [[2511.16043|Agent0]], [[2511.10395|AgentEvolver]], [[2511.03773|Experience-Synthesis-Mexp]], [[2510.05571|EvoPresent]], [[2508.04700|SEAgent]], [[2506.11442|ReVeal-Agent]]

> [!star] Key Papers
> - [[2511.16043|Agent0]] — Fully autonomous agent that self-improves through experience without human feedback

**Retrieval-Augmented Agents** — RL teaches agents to effectively retrieve and reason over external knowledge.
- [[2511.07328|Q-RAG]], [[2510.27566|Interact-RAG]], [[2510.07794|HiPRAG]], [[2509.01092|REFRAG]], [[2505.24332|DeepDiver]], [[2505.20046|REARANK]], [[2505.14069|ReasonRAG]], [[2505.09316|InForage]], [[2505.07233|DynamicRAG]], [[2505.04588|ZeroSearch]], [[2504.21776|WebThinker]], [[2503.19470|ReSearch]], [[2503.09516|Search-R1]], [[2503.05592|R1-Searcher]], [[2501.15228|MMOA-RAG]]


**Navigation & Path Planning RL** — RL for embodied navigation, vision-language navigation, and path planning.
- [[2607.13461|JOP-VLN]], [[2607.01044|CommNav]], [[2606.31260|SymPlan]], [[2604.08883|HTNav]], [[2602.12351|LongNav-R1]], [[2602.00551|APEX-Aerial]], [[2510.10181|Dejavu]], [[2509.23203|CE-Nav]], [[2507.22028|S2E-Navigation]], [[2301.11575|ARiADNE]], [[1905.12255|CLS]], [[1811.10092|RCM+SIL]]

> [!star] Key Papers
> - [[1811.10092|RCM+SIL]] — the foundational method: Reinforced Cross-Modal Matching + Self-Supervised Imitation Learning, the canonical RL recipe later VLN work still builds on
> - [[2301.11575|ARiADNE]] — first attention-based DRL policy for non-myopic frontier exploration, replacing the local-receptive-field limits of CNN-based planners
> - [[2607.13461|JOP-VLN]] — strongest current results: new SOTA 69.9% SR on R2R Val-Unseen from single-view RGB alone, with real quadruped deployment

**Manipulation, Planning & LLM-Guided Embodied Control** — RL for embodied manipulation and planning, including LLM-guided test-time planning.
- [[2607.23515|LEACL]], [[2607.18060|RoboHarness]], [[2607.13818|Agentic Execution RL]], [[2607.13653|REAL]], [[2607.13524|COLMAR]], [[2607.01925|SPLC]], [[2606.29222|CORE Planner]], [[2604.21232|ReCAPA]], [[2603.30022|Hybrid-LLM-RL-Manipulation]], [[2602.21198|Reflective-Test-Time-Planning]], [[2601.16175|TTT-Discover]], [[2511.01107|SLAP]], [[2506.00070|Robot-R1]], [[2412.05718|RLZero]]

> [!star] Key Papers
> - [[2511.01107|SLAP]] — foundational integration of classical TAMP abstract planning with RL, autonomously discovering low-level "shortcut" policies that cut plan length by 32-73% while holding 100% success where pure RL scores 0%
> - [[2607.18060|RoboHarness]] — strongest and most comprehensive result: an agentic framework orchestrating heterogeneous VLA/RL/TAMP policies via memory-driven handoffs to hit 98.7% on LIBERO and 95.2% on long-horizon LIBERO-LoHo, validated on 135 real-robot tasks

**Perception, Memory & Multi-Sensor Embodied RL** — RL for embodied perception, memory, and multi-sensor fusion.
- [[2607.08504|Hindsight Gating]], [[2607.06563|AcoustoBots]], [[2607.05957|Delay-Aware Active Triangulation for Counter-UAS]], [[2602.23320|ParamMem]], [[2601.10744|LMEE]], [[2511.21083|Dual-Agent-VIO]], [[2510.09951|Hippocampus-Actor-Critic]], [[2506.23061|DyME]], [[2505.06182|APPLE-Active-Perception]]


**Agent Infrastructure & Benchmarks** — Frameworks, environments, and evaluation tools for agentic RL.
- [[2607.21653|Molt]], [[2602.04118|TinyLoRA]], [[2511.21395|Monet]], [[2511.17473|MR-RLVR]], [[2511.15661|VisPlay]], [[2505.24760|REASONING-GYM]], [[2406.18505|LLM-Xavier]]


**Code Generation, Compilation & Systems RL** — RL for code generation, decompilation, compiler optimization, and low-level systems code.
- [[2510.23272|AesCoder]], [[2509.22114|SK2Decompile]], [[2507.14111|CUDA-L1]], [[2507.11948|Kevin]], [[2507.00417|ASTRO]], [[2506.15701|Compiler-R1]], [[2505.22704|REAL-Code]], [[2504.08600|SQL-R1]]

> [!star] Key Papers
> - [[2507.14111|CUDA-L1]] — strongest reported results in the group (×3.12 avg / ×120 peak speedup, generalizes across GPU architectures); contrastive-RL scheme embeds performance scores directly into prompts to autonomously discover non-obvious optimizations
> - [[2509.22114|SK2Decompile]] — foundational reframing of decompilation as two RL-tuned phases (structure then naming), the first LLM-based decompiler to break the correctness-vs-readability trade-off (~70% re-executability on HumanEval, beating GPT-5-mini by over 20%)
> - [[2504.08600|SQL-R1]] — strongest reward-engineering recipe for code-adjacent generation; a four-component progressive reward pushes a 7B model to 88.7% Spider-Test / 66.6% BIRD-Dev, beating larger closed-source baselines

**Code Agent Tools, Interpreters & Tool-Use RL** — RL for tool-calling, code-interpreter use, and applied coding-agent workflows.
- [[2603.13348|AutoTool]], [[2512.08511|SubagentVL]], [[2512.04563|COOPER]], [[2511.01618|Actial]], [[2510.14635|ATGen]], [[2510.01832|SCRIBES]], [[2509.22824|Critique-Coder]], [[2509.22644|WebGen-Agent]], [[2509.17325|CodeGym]], [[2509.01684|ML-Engineering-RL-Agents]], [[2508.21107|UTRL]], [[2508.05433|MLES]], [[2508.04865|Agnostics]], [[2506.09820|CoRT]], [[2505.23387|Afterburner]], [[2505.21668|R1-Code-Interpreter]], [[2505.16053|RLAF]], [[2505.12723|OORL]], [[2505.12285|CALM-Heuristic-Design]], [[2505.07773|ZeroTIR]]


**Additional Methods** — Cognitive-modeling and other agentic RL methods that cross section boundaries — human decision explanation, EEG-based reward, and policy-to-language translation.
- [[2607.14393|NEURO-LOOP]], [[2603.25968|EEG-Reward-AV]], [[2505.11614|RL-for-Human-Decision-Explanation]], [[2502.12530|Policy-to-Language]]

> [!star] Key Papers
> - [[2505.11614|RL-for-Human-Decision-Explanation]] — Novel use of RL to train LLMs as cognitive models of human decision-making; bridges AI and cognitive science

**Adversarial Multi-Agent RL & Red-Teaming** — RL where agents are trained as adversaries — to mine failures, induce targeted behaviors, or stress-test other policies. Companion to robust RL; closely related to [[11_Robotics-and-Embodied-AI|adversarial robustness in VLAs]].
- [[2607.10630|AWM]], [[2607.05939|PFSP-CTBR]], [[2604.05595|DAERT]], [[2602.06854|SEMA]], [[2602.00528|LLM-Poker-Study]], [[2510.10937|Neutral-Adversarial-Policy]], [[2510.08255|ShapeLLM-Opponent]], [[2510.02286|DialTree]], [[2510.01264|HARL-A]], [[2509.18891|Point-Prompt-Defender]], [[2508.02027|Dual-DM]], [[2503.21983|RL-Trust-Attacks]], [[2501.01830|Auto-RT]], [[1903.10654|FAILMAKER-ADVRL]]

> [!star] Key Papers
> - [[2604.05595|DAERT]] — RL-based diversity-aware red-teaming against VLAs; bridges adversarial RL with VLA failure-mining (5.85% π0 success under attack)
> - [[1903.10654|FAILMAKER-ADVRL]] — Foundational MADDPG-based adversarial RL; balances adversarial and personal rewards to produce realistic failure scenarios
> - [[2510.01264|HARL-A]] — Heterogeneous multi-agent adversarial RL framework in IsaacLab; team-specific critics resolve zero-sum value collapse

> [!tip] The Self-Evolving Connection
> Agentic RL connects directly to self-evolving AI: agents that use RL to improve their own strategies, generate their own curricula, and bootstrap their own training data. The trajectory: AgentGym to RAGEN to Agent0 to Memento-Skills.

---

## 8. RL + Robotics

RL methods designed for or applied to physical robot learning — sample efficiency, safety, and real-world deployment constraints make robotics RL fundamentally different from LLM RL.

**Foundational VLA RL Frameworks & Algorithms** — The core algorithmic frameworks establishing RL post-training for VLA models.
- [[2607.29172|CLIFT]], [[2607.26513|EKG-VLA]], [[2607.20345|DEED]], [[2606.31958|SARL]], [[2604.17706|OmniVLA-RL]], [[2603.21341|RoboAlign]], [[2603.15600|Active-Critic-RL]], [[2602.12281|Scaling-Verification-VLA]], [[2602.01789|RFS]], [[2509.09674|SimpleVLA-RL]], [[2506.08440|TGRPO]], [[2505.19789|RL-for-VLA-Study]], [[2505.18719|VLA-RL]], [[2505.17016|RIPT-VLA]]

> [!star] Key Papers
> - [[2509.09674|SimpleVLA-RL]] — canonical GRPO-based framework porting LLM outcome-reward RL to VLA, pushing LIBERO to 99.1% and revealing emergent policies human demonstrations never showed
> - [[2505.17016|RIPT-VLA]] — first in this group to formalize interactive post-training as a third training stage, turning near-zero single-demonstration SFT into 80-90% success via critic-free RLOO+PPO
> - [[2505.19789|RL-for-VLA-Study]] — systematic study proving RL's edge over SFT is not uniform, beating the strongest SFT baseline by 42.6% on unseen objects/tables through semantics and execution robustness gains
> - [[2604.17706|OmniVLA-RL]] — Flow-GSPO: reformulates flow matching as SDE for stable online RL; 97.6% on LIBERO with faster convergence than PPO/GRPO
> - [[2505.18719|VLA-RL]] — First systematic RL framework for VLAs; showed RL post-training consistently improves over SFT
> - [[2506.08440|TGRPO]] — Trajectory-wise GRPO adapted for VLA fine-tuning; bridges LLM RL and robot RL

**Flow/Chunk-Based & Action-Representation VLA RL** — RL over flow-matching, action-chunking, and structured action representations for VLAs.
- [[2607.27782|RedFlow]], [[2607.26991|RL2-VLA]], [[2607.12992|ChunkFlow]], [[2607.12931|ExToken]], [[2607.10383|ABot-N1]], [[2607.04681|Pinocchio]], [[2607.04591|S2C]], [[2607.02092|Guided Action Flow]], [[2605.13276|D-VLA]], [[2605.13105|PAIR-VLA]], [[2605.09410|RePO-VLA]], [[2604.05614|GPLA]], [[2508.18269|FlowVLA]]

> [!star] Key Papers
> - [[2607.12992|ChunkFlow]] — foundational unified framework baking seam-aware continuity losses directly into AWAC-based RL fine-tuning for chunked VLA policies, the best success-smoothness trade-off (93.4% LIBERO-Long, lowest jitter) at no extra inference latency
> - [[2607.02092|Guided Action Flow]] — paradigm-shifting approach that steers a frozen flow-matching policy's reverse-time denoising with a Q-critic's value gradients, boosting success up to +14pp with zero policy retraining
> - [[2607.12931|ExToken]] — strongest reported results (98.2% avg LIBERO, beating RLinf-GRPO), using clustered demonstration embeddings as discrete action-representation tokens to solve action-mode-collapse in VLA-RL exploration

**Driving, Model-Specific & Infrastructure VLA RL** — VLA RL for autonomous driving/surgical domains, named models, and training infrastructure.
- [[2607.01658|DriveTeach-VLA]], [[2606.31846|Z-1]], [[2606.29892|T2VLA]], [[2605.13959|WarmPrior]], [[2604.08168|ViVa]], [[2604.02523|Tune-to-Learn]], [[2603.28116|AutoDrive-P3]], [[2603.27670|ProgressVLA]], [[2603.27164|daVinci-LLM]], [[2603.26666|VLA-OPD]], [[2603.25406|MMaDA-VLA]], [[2603.13925|SmoothVLA]], [[2602.00919|Green-VLA]], [[2510.10975|RoVer]], [[2509.25852|REVER]]

> [!star] Key Papers
> - [[2603.28116|AutoDrive-P3]] — unifies perception, prediction, and planning through a single hierarchical GRPO reward, fixing the gap where RL only supervised final planning metrics and yielding the lowest collision rate (0.06%) in the group
> - [[2606.29892|T2VLA]] — replaces external environmental reward entirely with intrinsic generation confidence, an architecture-agnostic self-bootstrapping signal delivering the group's largest gains (+24.2% for π₀, +21.3% on RoboTwin 2.0)
> - [[2602.00919|Green-VLA]] — most complete infrastructure recipe, a five-stage curriculum from web pretraining through RL refinement plus a unified-action-space pipeline, taking a VLA to multi-embodiment real humanoid deployment

**Manipulation & Embodiment-Specific VLA RL** — VLA RL specialized to manipulation, dexterous hands, and specific robot embodiments.
- [[2509.23745|LocoFormer]], [[2509.19301|ResFiT]], [[2505.16517|ManipLVM-R1]], [[2505.15206|EndoVLA]], [[2505.03238|RobotxR1]], [[2504.04259|ORCA-Hand]], [[2503.16806|DyWA]], [[2502.14795|Humanoid-VLA]], [[2212.07740|TERT]], [[2107.03996|LocoTransformer]]

**Model-Based Robot RL** — World-model-based approaches for sample-efficient robot learning.
- [[2608.07468|SimWAM]], [[2607.06018|RoboTALES]], [[2607.04265|HALO-WA]], [[2607.02431|WorldSample]], [[2605.12084|QOED]], [[2604.18161|DDCG]], [[2604.02260|Time-Varying-MBRL]], [[2603.18336|ManiDreams]], [[2602.09022|WorldCompass]], [[2509.00215|DMO]], [[2509.00178|Poke and Strike]], [[2508.19172|URSA]], [[2508.15755|NeRD]], [[2505.16394|Raw2Drive]], [[2505.13925|TR-DRL]], [[2504.16680|RWM-U]], [[2502.13144|RAD]], [[2501.10100|RWM]], [[2410.00564|JOWA]], [[2207.07560|SkiMo]], [[2206.14176|DayDreamer]], [[1909.11652|PDDM]], [[1812.00568|Visual MPC]]

> [!star] Key Papers
> - [[2603.18336|ManiDreams]] — World model generates diverse manipulation scenarios; dream-based RL for dexterous tasks

**MPC + RL for Control** — Combining Model Predictive Control with learned RL policies for structured, physically-grounded control, including runtime safety filters and control barrier functions.
- [[2608.04732|Integrated-Safe-AC]], [[2607.23930|FAOC]], [[2607.20665|DGPPO]], [[2607.14488|Acc-CBF-QP]], [[2607.13938|DBF]], [[2607.12784|ATACOM-DC]], [[2607.07252|Safe RL via MPC]], [[2607.02472|Quad APG]], [[2607.01281|WaveLander]], [[2607.00066|Endovascular RL-NMPC]], [[2606.31562|Stabilization Learning]], [[2606.24039|TurboMPC]], [[2604.21456|TSMC]], [[2603.14469|PIPER]], [[2510.06179|DiffMPC]], [[2507.21533|MPAIL]], [[2507.19151|ReCoDe]], [[2505.20829|Unified-Force-Position-Control]], [[2504.06662|RAMBO]], [[2502.02133|MPC-RL-Survey]], [[2310.10509|Online Admittance Residual Learning]], [[2309.15462|DTC]], [[1504.00702|Visuomotor GPS]]

> [!star] Key Papers
> - [[1504.00702|Visuomotor GPS]] — foundational: first to fold trajectory optimization (linear-Gaussian iLQG, MPC's local cousin) into an RL loop training an end-to-end deep policy, establishing the guided-policy-search template this group builds on
> - [[2502.02133|MPC-RL-Survey]] — clearest articulation of the field, giving the actor/critic/deployed-policy taxonomy that every other paper in this group instantiates a slice of
> - [[2309.15462|DTC]] — strongest reported results, a Science Robotics hybrid TO+RL controller hitting 2.3cm foothold accuracy while crossing gaps, beams, and slippery terrain that pure MPC or pure RL baselines fail on

**Control-Theoretic, Constraint-Aware & Benchmark Infrastructure** — Control-theoretic RL (Koopman/CBF), constraint-aware planning, and benchmark/simulation infrastructure for LLM-guided robotics.
- [[2607.23473|PRISM-Motor]], [[2605.26452|Koopman-CBF-SAC]], [[2604.03023|Behavior-Constrained-RL]], [[2604.02021|Discrete-Continuous-Planning-Bridge]], [[2603.13707|REFINE-DP]], [[2603.02203|T3RL]], [[2602.15827|PHP]], [[2602.06556|LIBERO-X]], [[2602.02605|ESMA]], [[2602.02481|FPO++]], [[2509.09863|LSAC]], [[2407.07788|BiGym]], [[2302.04659|ManiSkill2]], [[2107.04034|RMA]]

> [!star] Key Papers
> - [[2605.26452|Koopman-CBF-SAC]] — clearest paradigm-shifting approach for control-theoretic RL, bridging model-free SAC with data-driven Koopman-CBF safety filters and a novel residual margin giving pointwise safety guarantees
> - [[2604.02021|Discrete-Continuous-Planning-Bridge]] — strongest reported results for constraint-aware planning, lifting RL path-planner success from 56-70% to 100% and cutting joint-increment norms by an order of magnitude
> - [[2302.04659|ManiSkill2]] — foundational benchmark/simulation infrastructure paper, establishing real-time two-way rigid-soft coupling and ~2000 FPS visual RL that later manipulation benchmarks build on

**LLM/VLM-Guided Reward & Task Specification** — Using LLM/VLM reasoning to specify rewards, tasks, and goals for robot RL.
- [[2605.22986|ASQ]], [[2602.01166|LaRA-VLA]], [[2512.01996|Humanoid-Loco-15min]], [[2512.00961|GenReward]], [[2511.17855|QuickLAP]], [[2506.08052|ReCogDrive]], [[2502.13130|Magma]], [[2502.10894|UAN]], [[2403.13358|QUARD-Auto]], [[2309.00709|TrafficRLHF]], [[2306.08647|L2R]]

> [!star] Key Papers
> - [[2512.00961|GenReward]] — clearest instantiation of the group's core idea: a pretrained video diffusion model generates goal videos whose alignment with the agent's trajectory becomes the RL reward, delivering the group's strongest measured gains
> - [[2309.00709|TrafficRLHF]] — foundational method, first to transplant RLHF's reward-model-from-preferences paradigm into reward specification for a robotics-adjacent simulation domain, generalizing across model architectures
> - [[2506.08052|ReCogDrive]] — paradigm-shifting case for VLM-guided RL: cognitive tokens from a driving-tuned VLM condition a diffusion planner that DiffGRPO optimizes against closed-loop reward, achieving new SOTA (90.8 PDMS)

**Applied Manipulation, Locomotion & Mobile Robot Control** — LLM-guided RL applied to specific manipulation, locomotion, and mobile-robot control tasks.
- [[2607.25985|Physics-Aware DRL Quadcopter Control]], [[2607.21227|FORGE-plus]], [[2606.31106|AD Internal Prediction Probing]], [[2606.03441|PerchRL]], [[2606.03335|DGPO]], [[2605.27046|Thermal-Aware-Residual]], [[2605.26478|SDPG]], [[2605.21688|Microfiber-Shape-Control]], [[2605.19924|RoHIL]], [[2605.19919|ZPRL]], [[2509.02754|LLM Modules for AD]], [[2506.07876|ReLIC]], [[2505.22642|FastTD3]], [[2505.06776|FALCON-Loco-Manipulation]], [[2504.17838|CaRL]], [[2504.13818|PODS]], [[2502.01143|ASAP]], [[2405.07991|SPIN-Mobile-Manip]], [[2003.01239|Evolutionary-Meta-Learning-Legged]]


**Classic Sim-to-Real Theory & Domain Randomization** — Foundational domain-randomization and theoretical results underpinning sim-to-real transfer.
- [[2411.14251|NLRL]], [[2307.12074|MRLM]], [[2201.02373|Mirror-Learning]], [[2003.02471|BayRn]], [[1903.11774|DR Parameter Optimization]], [[1804.10332|Minitaur Sim-to-Real]], [[1710.06537|Dynamics Randomization]], [[1702.02453|UP-OSI]]

> [!star] Key Papers
> - [[1710.06537|Dynamics Randomization]] — foundational method establishing training-time randomization of physical parameters combined with a recurrent policy as the classic recipe for zero-shot sim-to-real transfer
> - [[1804.10332|Minitaur Sim-to-Real]] — strongest reported real-world result, directly transferring agile galloping/trotting to a physical quadruped with no fine-tuning while beating handcrafted gaits by up to 35% in energy efficiency
> - [[1702.02453|UP-OSI]] — earliest and most paradigm-shifting approach, pairing a dynamics-conditioned universal policy with online system identification so one simulation-trained controller adapts to unknown physical parameters at runtime
> - [[2201.02373|Mirror-Learning]] — Unifying theoretical framework for diverse policy optimization methods; connects RL algorithms under one roof

**Legged, Humanoid & Manipulation Sim2Real** — Sim-to-real transfer for legged locomotion, humanoid control, and dexterous manipulation.
- [[2607.23268|Sling2Sim2Real]], [[2607.04940|Dexterous Force-Based Grasping Sim-to-Real]], [[2604.24916|asRoBallet]], [[2604.23702|QuietWalk]], [[2601.22550|Exo-Plore]], [[2512.05094|GenMimic]], [[2508.12252|Robot-Trains-Robot]], [[2506.05168|Fabrica]], [[2505.07096|X-SIM]], [[2505.06883|FACET]], [[2503.10949|SCDA]], [[2502.20396|Humanoid-Sim2Real-Dex]], [[2411.06782|QuadWBG]], [[2409.16451|ARCH]], [[2409.10319|Catch It!]], [[2403.20328|Visual Quadrupedal Loco-Manipulation]], [[2403.17367|RoboDuet]], [[2403.16967|VBC]], [[2305.17110|IndustReal]]

> [!star] Key Papers
> - [[2305.17110|IndustReal]] — first end-to-end sim-to-real transfer for contact-rich assembly (detect, grasp, align, insert) with zero real-world fine-tuning, its SAPU/SDF-reward/PLAI toolkit now a reference recipe for contact-rich transfer
> - [[2403.16967|VBC]] — foundational hierarchical framework for autonomous vision-based whole-body legged loco-manipulation trained entirely in sim, the baseline that RoboDuet and QuadWBG in this group build on and outperform
> - [[2508.12252|Robot-Trains-Robot]] — paradigm-shifting departure from pure sim2real: a compliant robot-arm teacher enables safe, fully automated real-world RL on a physical humanoid, doubling walking speed in 20 minutes

**Benchmarks, Simulation Platforms & Applied Sim2Real Methods** — Simulation infrastructure, benchmarks, and applied sim-to-real algorithmic methods.
- [[2607.04972|HOLA]], [[2607.02037|Cross-Platform ASV RL]], [[2607.01410|BIFROST]], [[2607.00160|Phase-Decomposed RL]], [[2606.31043|Warp RL]], [[2606.30268|ConCent]], [[2606.05880|TAGA]], [[2605.19033|RLFTSim]], [[2605.09789|DRIS]], [[2604.24018|Sim2Real-Betting]], [[2604.07457|CMP]], [[2602.23253|SPARR]], [[2602.00678|RoboGauge]], [[2510.18060|SPACeR-RL]], [[2509.18648|SPiDR]], [[2508.21065|Learning-on-the-Fly]], [[2508.10538|MLM]], [[2507.06905|ULC]], [[2505.06771|JaxRobotarium]], [[2504.18904|RoboVerse]], [[2502.17666|IC-QL]], [[2502.07380|Wheeled Lab]]

**RL Infrastructure & Scaling** — Engineering and scaling RL systems for real-world robot deployment.
- [[2607.26985|SymmGrid]], [[2604.08706|RL-Experience-Replay-for-LLMs]], [[2604.06943|Sustainable-Transfer-RL]], [[2604.04539|FlashSAC]], [[2604.01158|SMASH]], [[2603.03279|ULTRA]], [[2602.07837|USER]], [[2512.20605|Internal-RL]], [[2510.22512|TRL]], [[2510.11103|SO3-Action-Representations]], [[2505.24864|ProRL]], [[2412.13211|MS-HAB]], [[2108.10470|Isaac-Gym]], [[2108.03332|BEHAVIOR]], [[2106.14405|Habitat-2.0]], [[2009.12293|robosuite]]


**Contrastive & Self-Supervised RL** — Self-supervised methods that learn useful representations for RL without labeled rewards.
- [[2606.29834|STEAM]], [[2606.11525|IWR]], [[2604.11805|Sim2Reason]], [[2604.05931|Saliency-Guided-Policy]], [[2603.17305|Contrastive-Reasoning-Alignment]], [[2602.11832|JEPA-VLA]], [[2511.16407|LAOF]], [[2511.04131|BFM-Zero]], [[2510.16416|SSL4RL]], [[2510.13704|Simplicial-Embeddings]], [[2508.07452|SCORER]], [[2507.14748|Identifiable-Skill-Learning]], [[2506.11967|Annotation-Bootstrapping]], [[2505.04619|MAD]], [[2505.00500|INR-DOM]], [[2503.14858|CRL]], [[2502.05454|TRA]], [[2310.01404|H-InDex]], [[2212.05749|LfS (+aug) Baseline]], [[2210.07241|Self-Supervised 3D RL]], [[2106.05526|SSRL]]

> [!star] Key Papers
> - [[2510.16416|SSL4RL]] — Reinterprets self-supervised learning tasks as intrinsic verifiable rewards for RL
> - [[2506.11967|Annotation-Bootstrapping]] — Recasts visual pre-training as RL; learns annotation policies that improve downstream performance

**Offline RL Algorithms & Theory** — Core offline RL algorithms addressing distribution shift, partial observability, and static-buffer learning.
- [[2608.01205|ReBRAC-v2]], [[2606.17551|RQL]], [[2603.22201|NMR]], [[2505.23871|ADG]], [[2505.22866|SORL]], [[2505.22151|Oryx]], [[2505.18595|MisoDICE]], [[2505.15418|GPO-Partial-Obs]], [[2505.14975|SAW]], [[2505.08078|Batch-Online-RL-Study]], [[2504.11453|Clean-Slate-Offline-RL]]

> [!star] Key Papers
> - [[2606.17551|RQL]] — foundational flow-reversal technique solving the curse-of-horizon in off-policy value learning from static buffers, highest average score across 50 OGBench tasks against 18 baselines
> - [[2505.15418|GPO-Partial-Obs]] — clearest paradigm shift for partial observability, replacing the standard "impossibly good" teacher-student setup with a co-trained, theoretically-grounded guider/learner scheme that provably converges to RL-optimal
> - [[2504.11453|Clean-Slate-Offline-RL]] — most foundational theory contribution, exposing evaluation inconsistencies across the field and unifying prior distribution-shift-mitigation components into one framework yielding new SOTA algorithms

**Applied, Benchmark & Cross-Embodiment Offline RL** — Offline RL benchmarks, datasets, and cross-embodiment applications.
- [[2602.18025|Cross-Embodiment-Offline-RL]], [[2511.07820|SONIC]], [[2509.26605|BRIDGE-RL]], [[2509.06870|AggLM]], [[2508.03100|AVATAR]], [[2410.21151|BraVE]], [[2410.20092|OGBench]], [[2410.18252|Asynchronous-RLHF]], [[2410.01735|LASeR]], [[2209.08959|TACO-RL]], [[2108.03298|Robomimic]]


**Tactile, Contact-Rich & Teleoperation-Guided Manipulation** — Manipulation learning grounded in tactile sensing, contact signals, and teleoperated human demonstrations.
- [[2607.23782|N0-VTLA]], [[2607.11481|TELEDEXTER]], [[2607.08742|ContactMimic]], [[2607.06438|WristMimic]], [[2607.03723|OmniTacTune]], [[2607.00033|CHORD (Contact Wrench Guidance)]], [[2603.10971|ContactExplorer]], [[2603.00446|HydroShear]], [[2509.12741|FMVP]], [[2506.10968|EyeRobot]], [[2505.23175|LocoTouch]], [[2409.15095|MoMa-Teleop]], [[2310.03478|RGBManip]], [[2207.10763|Tactile-Gym-2.0]], [[2207.09450|WHIRL]], [[2105.14455|TacTip]]

> [!star] Key Papers
> - [[2105.14455|TacTip]] — foundational biomimetic optical tactile sensor whose decade-long design lineage and shear-sensing principle underpin most tactile-guided manipulation work in this group
> - [[2607.11481|TELEDEXTER]] — clearest advance in teleoperation-guided dexterity, replacing kinematic retargeting with a learned hand-object co-tracking controller that hits 75.2% success where prior teleoperation baselines fail near zero

**In-Hand, Grasping & Residual Manipulation RL** — In-hand reorientation, grasping, and residual-RL structuring of the dexterous action space.
- [[2607.28198|UniCross]], [[2607.12105|Physics-Priors In-Hand Rotation]], [[2607.11874|REGRIND]], [[2607.06323|LAMP]], [[2607.01651|AutoSERL]], [[2606.31909|CoDex]], [[2606.30474|GOMP]], [[2606.28323|DexCompose]], [[2509.09671|Dexplore]], [[2508.17547|LodeStar]], [[2505.05287|SYMDEX]], [[2502.15442|Privileged Actions]], [[2304.08488|VRB]], [[2304.04150|RoboPianist]], [[2303.03486|SBRL]], [[2008.03285|Residual-Hand-Pose-RL]], [[1812.03201|Residual RL]], [[1803.09956|VPG]]

> [!star] Key Papers
> - [[2607.06323|LAMP]] — Latent motion prior structures the high-dimensional hand-action space, enabling near-perfect success on complex dexterous tasks

**Parkour, Terrain Traversal & Extreme Locomotion** — RL for traversing extreme and irregular terrain — parkour, stairs, and sparse-contact footholds.
- [[2607.25541|P3-VAE]], [[2607.12114|GaitSpan]], [[2606.08253|π_FT]], [[2603.19305|PhyGile]], [[2508.08982|SDAX]], [[2505.12222|CAV Reward]], [[2504.09997|GenTe]], [[2502.10363|BeamDojo]], [[2404.19173|Single-Contact++-RL]], [[2309.14341|Extreme Parkour]], [[2309.05665|Robot Parkour]], [[2306.14874|ANYmal Parkour]], [[2305.14654|Barkour]], [[2205.02824|Rapid-Locomotion]], [[2105.08328|Blind-Bipedal-Stair-Climbing]]

> [!star] Key Papers
> - [[2105.08328|Blind-Bipedal-Stair-Climbing]] — foundational proof that a human-scale biped can traverse stairs from proprioception alone via terrain-randomized sim-to-real RL, no vision or reward re-engineering needed
> - [[2309.14341|Extreme Parkour]] — landmark end-to-end vision-to-action policy (dual distillation, self-inferred heading) that pushed legged parkour to 2x-body jumps and handstands on cheap hardware, defining the paradigm most later parkour work builds on
> - [[2502.10363|BeamDojo]] — first learning-based method for fine-grained humanoid foothold control on sparse terrain, pairing a sampling-based foothold reward with double-critic RL to hit 90%+ sim success and robust zero-shot real-world transfer

**Humanoid Whole-Body Control & Teleoperation** — Whole-body humanoid control, heavy-payload teleoperation, and novel gaits.
- [[2607.24083|HMP]], [[2607.20399|VR-RL Humanoid Tele-Loco-Manipulation]], [[2607.19903|YAHMP]], [[2607.15163|Humanoid Transformer]], [[2607.11624|SKooP]], [[2607.11041|PAKE]], [[2607.07830|HumoSlope]], [[2607.07370|ABot-C0]], [[2607.04837|Athena-WBC]], [[2607.02332|HEFT]], [[2606.31807|Skating Humanoid RL]], [[2606.29209|AnyBody (Whole-Body Humanoid Control)]], [[2603.02856|Rhythm]], [[2602.13656|KungFuAthlete]], [[2511.01774|MOBIUS]]

> [!star] Key Papers
> - [[2607.15163|Humanoid Transformer]] — strongest reported results (up to 82% MPKPE reduction), establishing a principled scaling recipe for humanoid Behavior Foundation Models
> - [[2607.19903|YAHMP]] — clearest account of which modeling/training choices actually matter in humanoid motion tracking pipelines
> - [[2607.02332|HEFT]] — strongest teleoperation-specific results, letting a full-size humanoid teleoperate under noisy VR input while carrying up to 24kg payloads
> - [[2606.31807|Skating Humanoid RL]] — Emergent stroke-and-glide propulsion on consumer inline skates; zero-shot sim-to-real with 50% lower Cost of Transport
> - [[2607.02332|HEFT]] — Single policy handles 24kg heavy-payload teleoperation on a full-size humanoid via privileged motion guidance and payload curriculum

**Quadruped & Perceptive Locomotion Control** — Quadruped locomotion policies and perceptive/blind terrain-aware control, including the ANYmal lineage.
- [[2607.26434|LSTM-CPG Quadruped Policy]], [[2607.24036|WARL]], [[2607.20110|Extreme-RGMT]], [[2607.18365|Torque-Driven Quadruped RL]], [[2607.18135|Isaac Sim-to-Real Quadruped RL]], [[2606.31691|FastDSAC]], [[2606.30362|ReactiveBFM]], [[2606.00637|GLAD]], [[2509.01765|PEGrad]], [[2508.11849|LocoMamba]], [[2506.09588|Attention-Map-Encoding]], [[2505.16084|ANYmal Motion Priors]], [[2404.02887|Differentiable Locomotion Control]], [[2211.07638|Egocentric-Legged-Locomotion]], [[2209.12827|Position-Based-Locomotion]], [[2201.08117|ANYmal-Perceptive-Locomotion]], [[2010.11251|ANYmal-Locomotion]]

> [!star] Key Papers
> - [[2010.11251|ANYmal-Locomotion]] — foundational teacher-student RL controller pioneering zero-shot sim-to-real proprioceptive locomotion, validated with zero failures in the DARPA Subterranean Challenge
> - [[2201.08117|ANYmal-Perceptive-Locomotion]] — defined the modern perceptive-locomotion paradigm via belief-state fusion of proprioception and exteroception, proven on a 2.2km alpine hike with zero falls
> - [[2211.07638|Egocentric-Legged-Locomotion]] — replaced noisy elevation-map pipelines with direct end-to-end egocentric depth vision, hitting 94-100% real-world success on stairs, gaps, and stepping stones

**Gait, Reference-Motion & Morphology-Agnostic Control** — Gait/reference-motion tracking and policies that generalize across robot morphologies.
- [[2607.00442|STL Gait-Aware Locomotion]], [[2606.31912|Foot-Centric Proximity Locomotion]], [[2606.30290|X-Morph]], [[2603.24047|PCHC]], [[2602.23832|OmniTrack]], [[2602.20375|Multi-Task Reference-Goal RL]], [[2510.02252|GMR]], [[2507.09371|ConsMimic]], [[2506.11470|Multi-Loco]], [[2102.02202|DERL]], [[2010.01856|AMORPHEUS]], [[2007.04976|SMP]], [[2004.00784|Imitating Animals]]

**Robot Navigation RL** — End-to-end RL navigation policies for mobile robots and autonomous agents — crowd and social navigation, unsteady-flow fields, and low-latency trajectory generation.
- [[2607.28560|X-NavDP]], [[2607.24292|HYPER-GNC]], [[2607.20785|Robostral Navigate]], [[2607.18794|LANav]], [[2607.15036|VOP-Nav]], [[2607.14643|NavCMPO]], [[2607.13553|Flow-Aware RL Navigation]], [[2607.10991|HUMA]], [[2508.03027|CogniPlan]]

> [!star] Key Papers
> - [[2607.20785|Robostral Navigate]] — sets a new SOTA on both R2R-CE and RxR-CE using only a monocular RGB camera, showing minimal-sensor navigation can beat multi-sensor systems
> - [[2607.15036|VOP-Nav]] — bridges the safety/agility trade-off by fusing classical Velocity-Obstacle reasoning into end-to-end RL, validated with 100% collision-free real-world trials on a quadruped
> - [[2607.18794|LANav]] — shows a linear-attention navigation backbone beats Transformers in both success rate and compute efficiency

**VLM & Learned Reward Design for Robot RL** — Using vision-language model feedback or dense reward extraction from demonstration video to automatically construct reward functions for robot RL, reducing manual reward engineering.
- [[2607.13033|DenseReward]], [[2607.12466|PREC]], [[2607.01721|CoRe]], [[2606.32027|FPL]], [[2606.31377|STDR]], [[2606.30698|VL-PR]], [[2606.28320|WARP-RM]], [[2603.16065|LRM]], [[2509.00271|HAVE]], [[2505.10911|ReWiND]], [[2503.03921|CREStE]], [[2502.04692|STRIDE]], [[2410.11571|SDS]], [[2407.01903|TADPoLe]], [[2312.14134|Diffusion Reward]]

> [!star] Key Papers
> - [[2607.01721|CoRe]] — Combines formal and residual reward components with VLM feedback; 99.0% success on MetaWorld with 3-40x fewer labels
> - [[2606.32027|FPL]] — Freeform natural-language preference axes yield 38pp higher success than baselines with compositional generalization
> - [[2502.04692|STRIDE]] — LLM agent closes the loop between automated reward design and DRL training feedback for humanoid locomotion

**Physics-Based Character Animation Control** — Adversarial and diffusion-based motion imitation for controllable, physically simulated character animation, bridging graphics and RL.
- [[2310.04582|PULSE]], [[2306.00416|A-MDM]], [[2305.02195|CALM]], [[2302.00883|Physical-Character-Scene-Interactions]], [[2301.13868|PADL]], [[1905.09808|MCP]]

> [!star] Key Papers
> - [[2310.04582|PULSE]] — Distills a physics-based motion imitator into a universal, reusable humanoid motion latent space
> - [[2305.02195|CALM]] — Adversarial latent motion model producing controllable, diverse physics-based character behaviors from unstructured demonstrations

> [!tip] The RL for Robotics Recipe
> The proven pipeline: pre-train with imitation learning, then post-train with RL (VLA-RL, TGRPO). For sample efficiency, use a world model (DayDreamer, RWM-U). For deployment, combine MPC structure with learned RL policies.

> [!success] Failure-Mining ↔ Avoidance ↔ WAM-Eval Cross-Recipe
> The same loop appears in robotics and driving:
> - RL failure-search: [[2412.02818|RoboMD]] (manipulation), [[2604.05595|DAERT]] (VLA linguistic), [[2509.03771|Co-Evolving-MARL]] (curiosity), [[1903.10654|FAILMAKER-ADVRL]] (driving NPCs)
> - Failure-avoidance: [[2601.07821|FARL]] regularizes the policy to avoid mined failures
> - WAM-as-eval: [[2506.00613|WorldGym]] turns the world model into the evaluator; [[2510.21232|Confusing-World-Models]] formalizes when WMs themselves are confusable
> - Non-RL VLA red-team: [[2604.22591|RedVLA]], [[2603.12510|Q-DIG]], [[2604.01618|Tex3D]], [[2511.12149|AttackVLA]], [[2510.13237|EDPA]], [[2506.03350|GCG-VLA]], [[2411.18676|ERT]], [[2411.13587|VLA-Adversarial-Vulnerabilities]] — see [[11_Robotics-and-Embodied-AI|11 §4 Adversarial Robustness]]

> [!note] Open Research Wedge
> Two intersection cells are conspicuously empty:
> - **(RL scene-adversary) × (VLA target)**: DAERT trains an RL adversary on language; RedVLA / Tex3D attack the scene without RL. No paper yet trains a *physics-grounded RL adversary that perturbs the 3D scene* against a VLA target.
> - **(RL failure-search) × (WAM target)**: WorldGym evaluates inside a WAM; Confusing World Models perturbs WM dynamics statically. No paper closes the loop with an RL adversary that searches the WAM's latent state space for confusing trajectories at training time. Natural intersection of the two cells above and a candidate research direction.

---

## 9. Miscellaneous RL Applications

RL methods applied to specialized domains and cross-cutting applications that span multiple categories.

**Distillation & Efficiency-Focused Post-Training** — On-policy/teacher-student distillation and compute-efficient post-training recipes.
- [[2607.15161|OPD^2]], [[2607.05394|Direct-OPD]], [[2607.05339|TREK]], [[2607.04751|TOP-D]], [[2604.11297|MEDS]], [[2604.08865|SPPO]], [[2512.22238|Mask-Teacher-Distill]], [[2512.00536|Dataset-Distillation-RL]], [[2511.00091|PLD]], [[2509.26226|ThinkingFree]], [[2509.23958|RLIR]], [[2509.19292|SOE]], [[2509.16965|TVKD]], [[2505.16581|Distilled-Policy-Ensembles]]

> [!star] Key Papers
> - [[2607.04751|TOP-D]] — fixes the root-cause instability of on-policy distillation (unbounded log-ratio reward) with a theoretically-grounded trust-region fix, the largest single reported gain in the group (+25.84pp AIME24) at zero extra compute
> - [[2607.05394|Direct-OPD]] — reframes a weak model's RL training as a reusable "policy shift" that can be transplanted onto stronger students, cutting post-training compute by ~50%
> - [[2607.15161|OPD^2]] — isolates a teacher's reasoning-specific delta from its base model rather than its full output distribution, with the broadest, most consistent gains across model sizes/domains

**Robotics, Tool-Use & Agentic Post-Training** — Post-training methods applied to VLA/robotics and agentic tool-use settings.
- [[2512.16918|AdaTooler-V]], [[2512.04072|SkillFactory]], [[2512.02834|TACO]], [[2511.14565|Masked-IRL]], [[2511.09515|WMPO]], [[2510.00406|VLA-RFT]], [[2509.18830|DexSkin]], [[2509.15937|VLAC]], [[2506.12851|KungfuBot]], [[2505.01441|ARTIST]], [[2505.00024|Nemotron-Research-Tool-N1]], [[2504.13958|ToolRL]], [[2503.07572|MRT]], [[2501.01478|MCTS-Process-Supervision]], [[2412.02818|RoboMD]], [[2405.10292|VLM-RL-Fine-Tuning]]

> [!star] Key Papers
> - [[2405.10292|VLM-RL-Fine-Tuning]] — the foundational template of end-to-end RL fine-tuning of a VLM as an acting agent with CoT, which every later robotics/tool/agentic-RL paper in this group varies
> - [[2504.13958|ToolRL]] — clearest statement that reward design, not architecture or SFT, is the real lever for tool-use RL
> - [[2511.09515|WMPO]] — paradigm shift for robotics post-training: on-policy RL run entirely inside a learned pixel-space world model, eliminating real-world interaction while still yielding real-robot gains

**Reasoning-Efficiency, Reflection & Reward-Shaping Post-Training** — Post-training recipes that reshape rewards, add reflection, or manage reasoning-token budgets.
- [[2512.18552|SSR]], [[2510.25889|piRL]], [[2510.25801|Metis-SPECS]], [[2510.15047|SPA]], [[2510.12710|Reflective-Self-Adaptation]], [[2508.12790|Rubicon]], [[2508.05629|DFT]], [[2508.02298|CAPO]], [[2507.17746|RaR]], [[2505.22094|ReinFlow]], [[2504.13055|NoisyRollout]], [[2504.12216|d1]], [[2504.11536|ReTool]], [[2503.23383|ToRL]], [[2503.03746|Process-based-Self-Rewarding]], [[2502.02316|DIME]]

> [!star] Key Papers
> - [[2508.05629|DFT]] — reframes SFT as RL with an ill-posed inverse-probability reward and rectifies it in a single line, beating PPO/GRPO by +15.66 points
> - [[2504.11536|ReTool]] — RL-learned strategic code-interpreter use lifts AIME24 from 40.0% to 67.0% in 400 steps while cutting response length 40%, with emergent self-correction

**Generation, Multimodal & Theory Post-Training** — Post-training for generative/multimodal outputs plus surveys and theoretical framing of the field.
- [[2604.01193|SSD-Code-Generation]], [[2603.19266|Explanatory-Inversion]], [[2603.10160|ReMix]], [[2512.17636|TRAPO]], [[2512.13043|GTR-Turbo]], [[2512.01119|World-Model-Surprise-Robustness]], [[2505.07538|Selftok]], [[2504.18471|AFM]], [[2504.18053|DREAM]], [[2502.21321|LLM-Post-Training-Survey]], [[2501.13926|CoT-Image-Generation]], [[2409.18869|Emu3]], [[2403.12884|HYDRA]], [[2401.05946|TDB]], [[2310.06114|UniSim]], [[2203.03485|Self-directed-Exploratory-Planning]]

> [!star] Key Papers
> - [[2502.21321|LLM-Post-Training-Survey]] — Comprehensive survey of post-training for LLMs; maps the full SFT-to-RL pipeline

**RL for Structured Prediction** — RL applied to ranking, retrieval, and other structured output tasks.
- [[2604.08545|Metis]], [[2604.02035|RL-Speculative-Trading]], [[2603.07020|RESCHED]], [[2602.11057|PRAM]], [[2512.23333|CME-CAD]], [[2510.11121|RFTHGS]], [[2510.10509|MARS-Sep]], [[2510.04080|PoLi-RL]], [[2510.03257|Triple-BERT]], [[2509.22558|StepORLM]], [[2509.15927|AIGB-Pearl]], [[2508.14313|AIRL-S]], [[2506.16931|MMFL]], [[2506.08898|POCCO]], [[2506.04195|MACS]], [[2505.23131|DOPPLER]], [[2505.20046|REARANK]], [[2505.19053|Structured-RL-CO]], [[2505.13445|RISE]]


**Safe RL & Constrained Control Theory** — Formal safety constraints, temporal-logic specifications, and robustness theory for RL.
- [[2602.19532|VDPPO]], [[2602.17078|Safe-CT-MARL]], [[2602.05323|GAS-Safe-RL]], [[2508.01561|GenZ-LTL]], [[2506.08062|FairDICE]], [[2506.01167|Differentiable-LTL]], [[2505.10947|Lyapunov-RL-Stability]], [[2504.04675|HypRL]], [[2503.18991|DR-IRL]], [[2502.10138|OPSE-LCMDP]], [[1901.09184|Action-Robust-RL]]

> [!star] Key Papers
> - [[1901.09184|Action-Robust-RL]] — earliest work in the group, formalizing action-space robustness via PR-MDP/NR-MDP two-player games with convergence guarantees, whose AR-DDPG became a reference robust-RL baseline
> - [[2505.10947|Lyapunov-RL-Stability]] — bridges classical constrained-control theory and RL, relaxing the pointwise Lyapunov decrease condition to a multi-step average that nearly doubles formally verified regions of attraction
> - [[2502.10138|OPSE-LCMDP]] — first computationally efficient linear-CMDP algorithm proven to achieve both sublinear regret and episode-wise zero constraint violation

**Truthfulness, Alignment & Human-Values RL** — RL methods that improve model truthfulness, opinion diversity, and alignment with human values.
- [[2606.24014|Beneficial Trait RL]], [[2603.01214|Opinion-Alignment-Reasoning]], [[2509.20357|RLMT]], [[2509.03518|LLM-Lying]], [[2507.14987|AlphaAlign]], [[2507.00971|TARS]], [[2506.19807|KnowRL]], [[2506.04245|CI-CoT]], [[2505.15795|RLRE]], [[2410.19933|RePO]]

> [!star] Key Papers
> - [[2606.24014|Beneficial Trait RL]] — training on just 5% beneficial-trait data drove 83% out-of-distribution alignment wins and far greater resilience to adversarial prompting
> - [[2507.00971|TARS]] — three-stage recipe gives the clearest, ablation-backed explanation of why naive safety RL collapses into blanket refusal and how to avoid it
> - [[2410.19933|RePO]] — foundational reframing showing "expected" safety constraints let models statistically compensate for individual unsafe outputs, proposing per-instance "critical safety constraints" as the fix

**Safety Filters, Robustness & Reward-Hacking Defense** — Runtime safety filters and defenses against reward hacking and unsafe exploration.
- [[2603.23889|COX]], [[2602.15817|FGE]], [[2601.19612|SOOPER]], [[2512.11391|NSPO]], [[2510.12312|Deep-SPI]], [[2510.08240|WaltzRL]], [[2509.25727|B2R]], [[2509.15172|MACA]], [[2507.16806|RLCR]], [[2505.21852|PLS]], [[2505.20065|SafeDPO]], [[2505.16186|SafeKey]]


**RL-Enhanced Multimodal Architectures** — Novel architectures that fundamentally integrate RL into their design rather than using it as post-training.
- [[2604.08539|OpenVLThinkerV2]], [[2603.01696|CIM]], [[2602.04884|RAL]], [[2602.03806|COBALT]], [[2602.03143|SAGE]], [[2602.02605|ESMA]], [[2511.10279|PROPA]], [[2507.00432|Math-Reasoning-Transferability]], [[2506.13351|DRO]], [[2506.08388|RLTs]], [[2505.18129|V-Triune]], [[2505.16673|R1-ShareVL]], [[1705.03633|IEP]], [[1704.05526|N2NMN]]


**Diffusion/Flow GRPO for Image & Video Generation** — GRPO and flow-matching variants adapted to diffusion-based image/video generation.
- [[2604.10962|ScoRe-Flow]], [[2603.28718|Stepwise-Flow-GRPO]], [[2603.16769|GDPO-SR]], [[2603.01163|BeautyGRPO]], [[2512.21514|DiverseGRPO]], [[2512.18766|MaskFocus]], [[2512.08153|TreeGRPO]], [[2512.04784|PaCo-RL]], [[2511.20256|Adv-GRPO]], [[2510.13418|Mask-GRPO]], [[2510.08425|DGPO-Diffusion]], [[2510.02880|MaskGRPO]], [[2510.01982|G2RPO-Flow]], [[2510.01540|Diffusion-LPO]], [[2510.00502|Diffusion-EM-Alignment]], [[2509.22485|GCPO-RL]], [[2509.16117|DiffusionNFT]], [[2508.04324|TempFlow-GRPO]]

> [!star] Key Papers
> - [[2508.04324|TempFlow-GRPO]] — foundational: shows flow-GRPO's uniform per-step credit assignment is the core inefficiency, an insight later Stepwise-Flow-GRPO, G²RPO-Flow, and TreeGRPO all build on
> - [[2509.16117|DiffusionNFT]] — ditches policy-gradient RL entirely by optimizing the forward process via flow matching, beating much larger CFG-based models (SD3.5-L, FLUX.1-Dev) with 3-25x efficiency
> - [[2510.08425|DGPO-Diffusion]] — eliminates the need for a stochastic policy altogether, hitting 97% GenEval with up to 30x faster training than Flow-GRPO

**Image/Video Editing & Preference RL** — RL for image/video editing, poster/motion generation, and preference-driven creative outputs.
- [[2604.19406|HP-Edit]], [[2509.15031|AutoEdit]], [[2508.01119|RL-Image-Editing]], [[2506.10741|PosterCraft]], [[2506.10353|Motion-R1]], [[2506.08011|ViGaL]], [[2505.21478|FlowRL-T2I-Pipeline]], [[2505.20793|Rendering-Aware-RL-SVG]], [[2505.18547|Diffusion-Blend]], [[2505.17540|RePrompt]], [[2505.17534|CoRL-Multimodal]], [[2505.17017|Image-Gen-RL-Study]], [[2407.08737|VADER]]

> [!star] Key Papers
> - [[2407.08737|VADER]] — first to align video diffusion models via differentiable reward gradients, founding the reward-gradient approach this group builds on
> - [[2508.01119|RL-Image-Editing]] — first RL post-training for autoregressive image editing, beating the strongest prior diffusion SOTA (Omnigen) with 5x less data and 4x faster inference
> - [[2505.17017|Image-Gen-RL-Study]] — clearest systematic account of the group's core preference-RL tradeoff (DPO's in-domain strength vs. GRPO's out-of-domain generalization)
> - [[2407.08737|VADER]] — Direct backpropagation through differentiable reward functions to fine-tune video diffusion models

**Molecular, 3D & Domain-Specific Generation** — RL for molecule design, 3D/mesh generation, and text/diagram/code rendering.
- [[2603.15616|GlyphPrinter]], [[2603.06043|Understanding-Driven-Reward]], [[2603.05900|RePO-Molecular]], [[2603.03072|TikZilla]], [[2603.00526|Mesh-Pro]], [[2512.10949|RL-Text-to-3D-Study]], [[2512.07733|SpatialDreamer]], [[2511.18378|CompGen]], [[2511.00511|ID-Crafter]], [[2510.00430|PromptLoop]], [[2505.20131|MolEditRL]], [[2505.04831|Steerable Scene Generation]], [[1810.08678|MolDQN]], [[1805.11973|MolGAN]]

> [!star] Key Papers
> - [[1805.11973|MolGAN]] — first GAN to generate molecular graphs directly, establishing the foundational graph+RL paradigm for molecule design that MolDQN, MolEditRL, and RePO-Molecular all build on
> - [[2603.00526|Mesh-Pro]] — strongest reported results in the 3D/mesh sub-area (SOTA Chamfer distance, broken ratio, quad ratio) via an asynchronous online RL framework for autoregressive mesh generation
> - [[2603.03072|TikZilla]] — clearest demonstration of data+RL with a domain-specific visual reward applied to text/diagram/code rendering, with small open models beating GPT-5/GPT-4o

**General RL+Generation Algorithms & Theory** — Broader algorithmic and theoretical contributions to RL for generative modeling.
- [[2605.15055|DiffusionOPD]], [[2605.10759|RAM]], [[2604.24171|POCA]], [[2603.21175|RSA-FT]], [[2603.21138|Generative-ZSL-RL]], [[2603.18991|CRAFT-Diff]], [[2602.16548|RIDER]], [[2601.02256|VAR-RL]], [[2601.02036|GDRO-Diff]], [[2512.24146|D2-Align]], [[2511.18719|ViPO]], [[2510.22319|GRPO-Guard]], [[2510.14255|IPRO]], [[2510.01399|DISCO-T2I]], [[2509.25774|PCPO]], [[2509.16500|RLGF]], [[2506.17007|Soft-Operators-Robust-RL]], [[2505.20107|MVC-ZigAL]], [[2502.01384|SEPO]], [[2502.00639|RLR-Optimizer]]

> [!star] Key Papers
> - [[2512.07733|SpatialDreamer]] — Uses active mental imagery via RL to incentivize spatial reasoning in generative models
> - [[2506.08011|ViGaL]] — RL-based game play for learning generalizable visual reasoning; bridges generation and understanding

**Continual & Test-Time RL** — RL methods that continue learning at deployment time or adapt to distribution shifts.
- [[2607.01111|FAR]], [[2604.11768|GC-PFO]], [[2604.11138|ViserDex]], [[2603.02203|T3RL]], [[2602.21198|Reflective-Test-Time-Planning]], [[2601.16175|TTT-Discover]], [[2502.03369|PVP (Proxy Value Propagation)]]

> [!star] Key Papers
> - [[2601.16175|TTT-Discover]] — Test-time training enabling LLMs to learn and adapt to novel patterns during inference

**RL + Program Synthesis** — RL for theorem proving, code generation, and formal verification.
- [[2510.11769|GAR]], [[2509.23285|Tool-Light]], [[2504.21801|DeepSeek-Prover-V2]], [[2504.11354|Kimina-Prover]], [[2503.16219|Open-RS]], [[2502.07640|Goedel-Prover]]

> [!star] Key Papers
> - [[2504.21801|DeepSeek-Prover-V2]] — RL-enhanced formal theorem proving with recursive proof search and subgoal decomposition

> [!tip] RL is Everywhere
> RL is no longer just a training method — it's becoming an architectural principle. From attention optimization (RAL) to pre-training (RPT) to test-time adaptation (TTT-Discover), RL permeates every layer of modern AI systems.


---

## Cross-References

- [[11_Robotics-and-Embodied-AI]] — VLAs, WAMs, and embodied systems (RL is the training backbone)
- [[09_Self-Evolving-AI]] — Broader self-evolving paradigm
- [[04_Video-and-Temporal]] — Video generation as world modeling
- [[01_Foundation-Models]] — Transformer/LLM foundations that RL fine-tunes

---

*Next: [[09_Self-Evolving-AI]] for self-improving systems built on these RL foundations.*
