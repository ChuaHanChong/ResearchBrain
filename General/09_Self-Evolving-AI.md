---
title: "Self-Evolving AI — Topic Overview"
tags:
  - self-evolving
  - self-improvement
  - continual-learning
  - meta-learning
aliases:
  - "Self-Evolving Overview"
---

# Self-Evolving AI

> [!abstract] Overview
> AI systems that improve themselves through experience — from self-taught reasoning (STaR) to self-evolving agents (EvoAgent) to self-improving world models (SPIRAL). This topic bridges RL, continual learning, and meta-learning into autonomous self-improvement. The field has matured from simple bootstrapping loops (2022) to fully autonomous, zero-data self-play systems (2025-2026).

## Evolution Graph

```text
1. Self-Training on Own Outputs   (bootstrap from what you got right)
· rationale bootstrapping
                   +token-level             +slow-thinking        +latent thought
                   rationales               distillation          bootstrapping
╔═════════════╗    ┌───────────────────┐    ┌────────────────┐    ┌─────────────┐
║ STaR (2022) ║───►│ Quiet-STaR (2024) │───►│ STILL-2 (2024) │───►│ BoLT (2025) │
╚══════┬══════╝    └───────────────────┘    └────────────────┘    └─────────────┘
       │    correct-filter → learned
       │    judge
       │    ┌──────────────────────────┐
       ├───►│ Self-Rewarding-LM (2024) │
       │    └──────────────────────────┘
       │    +step-level reward
       │    ┌─────────────────────────────────────┐
       └───►│ Process-based-Self-Rewarding (2025) │
            └─────────────────────────────────────┘

2. Zero-Data Self-Play   (who supplies reward when nobody does)
· label-free reward
                   +entropy-collapse
                   guard                 unlabeled data → no data
┌─────────────┐    ┌────────────────┐    ╔══════════════════════╗
│ TTRL (2025) │───►│ EVOL-RL (2025) │───►║ Absolute-Zero (2025) ║─┐
└─────────────┘    └────────────────┘    ╚══════════════════════╝ │
                                                                  │    +self-debate, no
                                                                  │    environment
                                                                  │    ┌──────────────────────┐
                                                                  ├───►│ Socratic-Zero (2025) │
                                                                  │    └──────────────────────┘
                                                                  │    +VLM gamified
                                                                  │    self-play
                                                                  │    ┌────────────────────┐
                                                                  ├───►│ Vision-Zero (2025) │
                                                                  │    └────────────────────┘
                                                                  │    +abstraction
                                                                  │    discovery
                                                                  │    ┌─────────────┐
                                                                  └───►│ RLAD (2025) │
                                                                       └─────────────┘

3. Curriculum and Adaptive Training   (order the tasks)
· shape the difficulty
                     +curriculum as    +verifiable            +self-evolving
                     tasks             environment scaling    curriculum
┌───────────────┐    ┌────────────┐    ┌─────────────────┐    ┌────────────┐
│ ADARFT (2025) │───►│ CaT (2025) │───►│ RLVE (2025)     │───►│ SEC (2025) │
└───────────────┘    └────────────┘    └─────────────────┘    └────────────┘

4. Self-Evolving Agents   (multi-step behavior, not single answers)
· experience into policy
                       +trajectory →         +real-codebase    +environment
                       principle             experience        co-evolves
┌─────────────────┐    ┌────────────────┐    ┌────────────┐    ╔═════════════╗
│ AgentGym (2024) │───►│ EVOLVER (2025) │───►│ SSR (2025) │───►║ ECHO (2026) ║
└─────────────────┘    └────────┬───────┘    └────────────┘    ╚═════════════╝
                                │    +self-improving
                                │    oversight
                                │    ┌─────────────┐
                                ├───►│ SOAR (2025) │
                                │    └─────────────┘
                                │    +agent-world co-design
                                │    ┌────────────────────┐
                                └───►│ Agent-World (2026) │
                                     └────────────────────┘

5. Self-Evolving Embodied   (close the loop on a robot)
· policy and model co-improve
                     +continual world       +VLA                 +embodied R1          +closed-loop
                     model                  self-evolution       recipe                long-horizon
┌───────────────┐    ┌─────────────────┐    ┌───────────────┐    ┌────────────────┐    ┌───────────────┐
│ RoboMD (2024) │───►│ EvoAgent (2025) │───►│ EvoVLA (2025) │───►│ SEEA-R1 (2025) │───►│ SPIRAL (2026) │
└───────────────┘    └─────────────────┘    └───────────────┘    └────────────────┘    └───────────────┘

6. Meta-Learning   (learn how to adapt)
· adapt the adaptation
                                    +detection
                                    meta-learning
┌──────────────────────────────┐    ┌───────────────────┐
│ Prototypical-Networks (2017) │───►│ Meta-R-CNN (2019) │─┐
└──────────────────────────────┘    └───────────────────┘ │
                                                          │    +in-context meta-optimization
                                                          │    ┌───────────────────────────────────────┐
                                                          ├───►│ Mesa-Optimization-Transformers (2023) │
                                                          │    └───────────────────────────────────────┘
                                                          │    +self-adapting
                                                          │    weights
                                                          │    ┌─────────────┐
                                                          └───►│ SEAL (2025) │
                                                               └─────────────┘

7. VLM Self-Improvement   (the multimodal case)
· self-check the vision
                     +self-reflection loop             +consistency signal
┌───────────────┐    ┌────────────────────────────┐    ┌───────────────────────────────┐
│ M-STAR (2024) │───►│ Self-Reflection-VLM (2025) │───►│ Triangular-Consistency (2025) │
└───────┬───────┘    └────────────────────────────┘    └───────────────────────────────┘
        │    +field map
        │    ┌─────────────────────────────────────┐
        └───►│ MLLM-Self-Improvement-Survey (2025) │
             └─────────────────────────────────────┘

8. Continual and Experiential   (persistence across deployment)
· lifelong memory
                            +reusable reasoning         +deployment-time,    +visually-grounded
                            memory                      no forgetting        transfer
┌──────────────────────┐    ┌──────────────────────┐    ┌───────────────┐    ╔════════════════╗
│ ELL-Framework (2025) │───►│ ReasoningBank (2025) │───►│ OEL (2026)    │───►║ XSkill (2026)  ║
└───────────┬──────────┘    └──────────────────────┘    └───────────────┘    ╚════════════════╝
            │    +when self-evolution
            │    fails
            │    ┌─────────────────────┐
            └───►│ Misevolution (2025) │
                 └─────────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

The eight lanes divide on **what supervises the self-improvement** once a human stops labelling. **Self-training on own outputs** bootstraps from what the model already got right, STaR to Quiet-STaR to STILL-2 to BoLT, with Self-Rewarding-LM and Process-based-Self-Rewarding branching to replace the correctness filter with a learned judge. **Zero-data self-play** removes the label entirely, TTRL scoring unlabelled test data, EVOL-RL guarding the entropy collapse, Absolute-Zero dropping the data itself, after which Socratic-Zero, Vision-Zero, and RLAD transplant the recipe into dialogue, vision, and abstraction independently. **Curriculum and adaptive training** orders the tasks instead, ADARFT to CaT to RLVE to SEC. **Self-evolving agents** move the unit of improvement from an answer to a trajectory, AgentGym to EVOLVER to SSR to ECHO, with SOAR and Agent-World branching on oversight and co-design. **Self-evolving embodied** closes the loop on a robot, RoboMD to EvoAgent to EvoVLA to SEEA-R1 to SPIRAL. **Meta-learning** adapts the adaptation itself, Prototypical-Networks to Meta-R-CNN, with Mesa-Optimization-Transformers and SEAL branching to in-context and weight-level self-adaptation. **VLM self-improvement** handles the multimodal case, M-STAR to Self-Reflection-VLM to Triangular-Consistency, with MLLM-Self-Improvement-Survey branching off as the field map. **Continual and experiential** keeps the gains across deployment, ELL-Framework to ReasoningBank to OEL to XSkill, with Misevolution branching to document how the loop fails.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2017 | [[1703.05175\|Prototypical-Networks]] | Meta-Learning · Adapt the Adaptation | Simple mean-based class prototypes in embedding space; established episodic training as the few-shot learning standard |
| 2019 | [[1909.13032\|Meta-R-CNN]] | Meta-Learning · Adapt the Adaptation | General meta-learning framework for few-shot detection; class-attentive vectors modulate features per novel category |
| 2022 | [[2203.14465\|STaR]] | Self-Training · Rationale Bootstrapping | Pioneered iterative self-improvement: generate rationales, keep correct ones, retrain; the self-training flywheel |
| 2023 | [[2309.05858\|Mesa-Optimization-Transformers]] | Meta-Learning · Adapt the Adaptation | Mechanistic explanation of how Transformers implicitly learn optimization algorithms (mesa-optimization) in-context |
| 2024 | [[2401.10020\|Self-Rewarding-LM]] | Self-Training · Rationale Bootstrapping | Single model acts as both generator and judge via iterative DPO; broke the human-feedback bottleneck |
| 2024 | [[2403.09629\|Quiet-STaR]] | Self-Training · Rationale Bootstrapping | Extended STaR to think before every token via internal rationales; generalized to token-level self-training |
| 2024 | [[2406.04151\|AgentGym]] | Agents · Experience into Policy | Multi-environment agent evolution via behavioral cloning + self-evolution for generalist agents |
| 2024 | [[2412.02818\|RoboMD]] | Embodied · Policy and Model Co-Improve | RL adversary that actively discovers policy failure modes; finds what the agent can't do |
| 2024 | [[2412.09413\|STILL-2]] | Self-Training · Rationale Bootstrapping | Open-source framework reproducing o1-like slow-thinking; distillation + RL pipeline for chain-of-thought |
| 2024 | [[2412.17451\|M-STAR]] | VLM · Self-Check the Vision | Self-evolving training framework for large multimodal models; iterative self-improvement across vision-language benchmarks |
| 2025 | [[2502.05907\|EvoAgent]] | Embodied · Policy and Model Co-Improve | Self-evolving agent with continual world model; self-planning + self-control + self-reflection achieves +105% improvement on long-horizon tasks |
| 2025 | [[2503.03746\|Process-based-Self-Rewarding]] | Self-Training · Rationale Bootstrapping | Extends self-rewarding from outcome-level to step-level process rewards; finer-grained self-supervision |
| 2025 | [[2503.18866\|BoLT]] | Self-Training · Rationale Bootstrapping | "Reasoning to Learn": models use test-time reasoning chains as training signal, closing the loop between inference and learning |
| 2025 | [[2504.05520\|ADARFT]] | Curriculum · Shape the Difficulty | Adaptive curriculum for RLVR that selects training problems matching the model's current capability frontier |
| 2025 | [[2504.16084\|TTRL]] | Zero-Data · Label-Free Reward | Proved LLMs can self-improve on unlabeled test data via majority-vote rewards; 211% on AIME 2024 |
| 2025 | [[2505.03335\|Absolute-Zero]] | Zero-Data · Label-Free Reward | Zero-data self-play: model proposes tasks, solves, verifies via code, and retrains with no human data |
| 2025 | [[2505.14970\|SEC]] | Curriculum · Shape the Difficulty | Self-Evolving Curriculum: the training data distribution co-evolves with the model, ensuring the curriculum never becomes stale |
| 2025 | [[2506.10943\|SEAL]] | Meta-Learning · Adapt the Adaptation | Models autonomously generate optimized fine-tuning data and adaptation strategies; outperforms GPT-4.1-generated synthetic data |
| 2025 | [[2506.21669\|SEEA-R1]] | Embodied · Policy and Model Co-Improve | Tree-structured RL for self-evolving embodied agents; +24% via MCTS + generative reward |
| 2025 | [[2507.14172\|SOAR]] | Agents · Experience into Policy | Self-improving operators for automated program refinement; LLMs iteratively improve their own code transformations |
| 2025 | [[2508.19005\|ELL-Framework]] | Continual · Lifelong Memory | Experience-driven Lifelong Learning framework and StuLife benchmark for continual self-improvement |
| 2025 | [[2509.14234\|CaT]] | Curriculum · Shape the Difficulty | Compute as Teacher: uses more capable model runs to generate supervision for less capable configurations; compute itself becomes the curriculum |
| 2025 | [[2509.15194\|EVOL-RL]] | Zero-Data · Label-Free Reward | Evolutionary RL preventing entropy collapse in label-free self-improvement; balances selection and novelty |
| 2025 | [[2509.23236\|Self-Reflection-VLM]] | VLM · Self-Check the Vision | Uses binary self-consistency signals to reduce hallucinations without external supervision |
| 2025 | [[2509.24726\|Socratic-Zero]] | Zero-Data · Label-Free Reward | Data-free Socratic dialogue where the model debates itself to improve reasoning without any environment |
| 2025 | [[2509.25140\|ReasoningBank]] | Continual · Lifelong Memory | Memory-aware test-time scaling: stores and retrieves reasoning patterns for efficient reuse across problems |
| 2025 | [[2509.25541\|Vision-Zero]] | Zero-Data · Label-Free Reward | Extended the zero-data self-play paradigm to Vision-Language Models via gamified self-play |
| 2025 | [[2509.26354\|Misevolution]] | Continual · Lifelong Memory | Identifies "misevolution" as a novel safety risk: self-evolving models can drift from intended values during autonomous improvement |
| 2025 | [[2510.02263\|RLAD]] | Zero-Data · Label-Free Reward | Models self-discover high-level reasoning abstractions and learn to apply them; meta-cognitive self-improvement |
| 2025 | [[2510.02665\|MLLM-Self-Improvement-Survey]] | VLM · Self-Check the Vision | First comprehensive survey of self-improvement methods for multimodal LLMs; maps the taxonomy and open challenges |
| 2025 | [[2510.10487\|Triangular-Consistency]] | VLM · Self-Check the Vision | Cross-checks visual, textual, and reasoning outputs for mutual consistency; self-refinement through multi-modal agreement |
| 2025 | [[2510.16079\|EVOLVER]] | Agents · Experience into Policy | Agents distill raw interaction trajectories into strategic principles; experience-driven lifecycle |
| 2025 | [[2511.07317\|RLVE]] | Curriculum · Shape the Difficulty | Procedurally generates an unbounded supply of verifiable environments; the challenges grow as the model grows |
| 2025 | [[2511.16166\|EvoVLA]] | Embodied · Policy and Model Co-Improve | Self-evolving VLA framework that overcomes stage hallucination and fragile memory; the first end-to-end self-evolving VLA |
| 2025 | [[2512.18552\|SSR]] | Agents · Experience into Policy | Meta's Self-play SWE-RL: agents generate learning experiences from real codebases; +10.4 on SWE-bench |
| 2026 | [[2601.06794\|ECHO]] | Agents · Experience into Policy | Policy and environment co-evolve: harder challenges as policy improves, and vice versa |
| 2026 | [[2603.08403\|SPIRAL]] | Embodied · Policy and Model Co-Improve | Closed-loop self-improvement for action world models via reflective planning; the system critiques its own failures and adapts |
| 2026 | [[2603.12056\|XSkill]] | Continual · Lifelong Memory | Dual-stream framework for continual learning from visually-grounded experience; cross-task skill transfer |
| 2026 | [[2603.16856\|OEL]] | Continual · Lifelong Memory | Microsoft's Online Experiential Learning: LLMs continuously learn from deployment without forgetting |
| 2026 | [[2604.18292\|Agent-World]] | Agents · Experience into Policy | ByteDance/Renmin's framework unifying real-world environment synthesis with continuous self-evolution; 14B agent evaluated on 23 benchmarks, with average tool-use scores more than doubling as environment diversity scales from 0 to 1,978 |

---

## 1. Self-Training & Bootstrapping

The original self-improvement paradigm: models generate their own training data by sampling reasoning chains, filtering correct ones, and retraining on successes. Each iteration bootstraps quality beyond the original training distribution. This is the foundation on which all later self-evolving methods build.

**Iterative Rationale Bootstrapping** — Generate candidate reasoning traces, keep the ones that reach correct answers, retrain, repeat. The simplest form of self-improvement, requiring only a verifier (ground-truth or model-based).
- [[2605.14733|Video-Zero]], [[2604.12002|SD-ZERO]], [[2512.02389|Synthetic-Error-Self-Correct]], [[2506.00467|SST]], [[2504.08672|Genius]], [[2403.09629|Quiet-STaR]], [[2203.14465|STaR]]

> [!star] Key Papers
> - [[2203.14465|STaR]] — Pioneered iterative self-improvement: generate rationales, keep correct ones, retrain; each round improves reasoning beyond the original distribution
> - [[2403.09629|Quiet-STaR]] — Extended STaR to think before every token, not just prompted questions; implicit self-reasoning at every position
> - [[2504.08672|Genius]] — Purely unsupervised self-training without external labels; uses self-generated solutions as implicit reward signal

**Self-Rewarding & Self-Judging** — Models learn to evaluate their own outputs, creating an internal reward signal that replaces human annotators. The model is simultaneously generator and judge, enabling iterative DPO or RL without external feedback.
- [[2605.12741|RESD]], [[2508.03682|SQLM]], [[2503.03746|Process-based-Self-Rewarding]], [[2502.08922|SCIR]], [[2412.01951|Sharpening-Mechanism]], [[2401.10020|Self-Rewarding-LM]], [[2309.16797|PromptBreeder]]

> [!star] Key Papers
> - [[2401.10020|Self-Rewarding-LM]] — Single model acts as both instruction-follower and judge via iterative DPO; breaks the human-feedback bottleneck
> - [[2503.03746|Process-based-Self-Rewarding]] — Extends self-rewarding from outcome-level to step-level process rewards; finer-grained self-supervision
> - [[2412.01951|Sharpening-Mechanism]] — Formalizes self-improvement as "sharpening": theoretical framework explaining when and why self-training converges

**Slow-Thinking & Test-Time Reasoning** — Train models to use extended reasoning chains at inference time (o1-style), where longer thinking leads to better answers. Self-improvement happens by learning to allocate more compute to harder problems.
- [[2511.01191|Self-Harmony]], [[2509.26626|RSA]], [[2503.18866|BoLT]], [[2501.01478|MCTS-Process-Supervision]], [[2412.09413|STILL-2]]

> [!star] Key Papers
> - [[2412.09413|STILL-2]] — Open-source framework reproducing o1-like slow-thinking; distillation + RL pipeline for chain-of-thought enhancement
> - [[2501.01478|MCTS-Process-Supervision]] — Uses Monte Carlo Tree Search to generate fine-grained process supervision signals without human annotation
> - [[2503.18866|BoLT]] — "Reasoning to Learn": models use test-time reasoning chains as training signal, closing the loop between inference and learning

> [!tip] The Self-Improvement Ladder
> Start with STaR (simple self-training) --> add self-judging (Self-Rewarding LM) --> extend to process rewards (Process-based Self-Rewarding) --> scale with slow-thinking (STILL-2/BoLT). Each rung removes a human bottleneck.

---

## 2. Zero-Data & Self-Play RL

The most radical branch of self-evolution: models that improve with zero human-curated data. They either generate their own training problems (Absolute Zero), derive reward from consensus (TTRL), or use evolutionary self-play (EVOL-RL). This eliminates the last human bottleneck — the training dataset itself.

**Task Self-Generation** — The model both proposes and solves its own problems — including on unlabeled test data via self-consistency, and by optimizing its own inference/sampling hyperparameters — using only a code executor, environment, or majority-vote signal for verification. No human data at any stage.
- [[2604.14144|SpatialEvo]], [[2603.09206|MM-Zero]], [[2603.01771|HTI]], [[2602.01619|SUSD]], [[2512.11114|TAMO]], [[2510.02752|Self-Aware-RL-for-LLMs]], [[2510.02263|RLAD]], [[2509.25541|Vision-Zero]], [[2509.24726|Socratic-Zero]], [[2509.15194|EVOL-RL]], [[2506.24119|SPIRAL]], [[2506.08989|SwS]], [[2506.06499|SPARQ]], [[2506.05980|AMPED]], [[2506.05634|AutoQD]], [[2506.00103|Writing-Zero]], [[2505.24726|Reflect-Retry-Reward]], [[2505.03335|Absolute-Zero]], [[2504.16084|TTRL]], [[2502.05234|TURN]]

> [!star] Key Papers
> - [[2505.03335|Absolute-Zero]] — The defining paper: model proposes tasks, solves them, verifies via code execution, and retrains; SOTA on coding and math with literally zero human data
> - [[2509.24726|Socratic-Zero]] — Data-free Socratic dialogue where the model debates itself to improve reasoning; no environment needed
> - [[2509.25541|Vision-Zero]] — Extends the zero-data paradigm to Vision-Language Models via gamified self-play
> - [[2504.16084|TTRL]] — Proved LLMs can self-improve on unlabeled test data via majority-vote rewards; 211% improvement on AIME 2024
> - [[2509.15194|EVOL-RL]] — Evolutionary RL that prevents entropy collapse in label-free self-improvement; balances selection pressure with novelty-driven diversity
> - [[2502.05234|TURN]] — Automatically discovers near-optimal sampling temperature for self-improvement; removes a key manual tuning step
> - [[2510.02263|RLAD]] — Models self-discover high-level reasoning abstractions and learn to apply them; meta-cognitive self-improvement

**Self-Play & Multi-Agent Competition** — Multiple model instances compete or cooperate, driving improvement through adversarial pressure or consensus-seeking dynamics.
- [[2605.27276|SIA]], [[2603.15255|SAGE]], [[2510.24684|SPICE]], [[2510.23595|MAE]], [[2509.15172|MACA]], [[2509.07414|LSP]], [[2506.07468|SELF-REDTEAM]]

> [!star] Key Papers
> - [[2509.07414|LSP]] — Language Self-Play from Meta: models improve through self-play dialogue without external reward models

> [!tip] The Zero-Data Frontier
> Absolute Zero and TTRL proved the concept; EVOL-RL solved the entropy collapse problem. The next challenge is scaling zero-data self-play to open-ended domains beyond math and code, where verification is harder.

---

## 3. Curriculum Learning & Adaptive Training

Self-evolving systems need to practice on the right problems at the right difficulty. These methods automatically generate, select, and sequence training data so that each batch maximally improves the model — adaptive curricula that co-evolve with the learner.

**Adaptive Difficulty & Reweighting** — Dynamically adjust which training examples the model sees based on current capability, focusing compute on problems at the frontier of what the model can almost solve.
- [[2512.02472|R-FEW]], [[2510.09001|DARO]], [[2510.01135|PCL]], [[2504.13161|Nemotron-CLIMB]], [[2504.05520|ADARFT]]

> [!star] Key Papers
> - [[2504.05520|ADARFT]] — Adaptive curriculum for RLVR that selects training problems matching the model's current capability frontier
> - [[2510.09001|DARO]] — Dynamic reweighting for RL with verifiable rewards; prevents the model from wasting compute on too-easy or too-hard problems

**Self-Evolving Curricula** — The curriculum itself evolves: a synthesizer or environment generates new, capability-aligned challenges as the model improves, creating an unbounded supply of training signal — including curricula specialized for vision-language models and multi-stage reasoning pipelines.
- [[2604.26707|CurEvo]], [[2601.22628|TTCS]], [[2512.06835|DoGe]], [[2511.07317|RLVE]], [[2509.14234|CaT]], [[2507.22607|VL-Cogito]], [[2505.14970|SEC]], [[2502.05726|ACCEL]], [[1901.01753|POET]]

> [!star] Key Papers
> - [[2505.14970|SEC]] — Self-Evolving Curriculum: the training data distribution co-evolves with the model, ensuring the curriculum never becomes stale
> - [[2511.07317|RLVE]] — Procedurally generates an unbounded supply of verifiable environments; the challenges grow as the model grows
> - [[2507.22607|VL-Cogito]] — Progressive curriculum for VLMs that sequences visual reasoning tasks from simple to complex
> - [[2509.14234|CaT]] — Compute as Teacher: uses more capable model runs to generate supervision for less capable configurations; compute itself becomes the curriculum

> [!tip] Curriculum as Co-Evolution
> The most effective curricula are not pre-designed but co-evolve with the model. SEC and RLVE show that an adaptive problem generator paired with the learner outperforms any fixed dataset, no matter how large.

---

## 4. Self-Evolving Agents

When self-improvement meets agentic AI: systems that autonomously explore environments, accumulate experience, distill lessons, and evolve their own capabilities across tasks. These go beyond single-turn reasoning to multi-step, tool-using, environment-interacting agents that learn from deployment.

**General Agent Self-Evolution Frameworks** — End-to-end frameworks where a fixed agent's own reasoning, RL, or reflection loop directly drives capability growth across diverse domains — no separate curated artifact (skill library, memory store, or synthetic environment) sits between experience and improvement.
- [[2605.07465|SEIF]], [[2604.18131|Native-Evolution]], [[2604.15034|Autogenesis]], [[2604.07799|ECM]], [[2604.01658|CORAL]], [[2603.19461|HyperAgents]], [[2603.08561|RetroAgent]], [[2603.04029|Self-Adapting-RL]], [[2603.02224|Subspace-Geometry-Forgetting]], [[2602.00359|A-EVOLVE]], [[2511.16166|EvoVLA]], [[2511.00758|ATM]], [[2510.20685|C-Nav]], [[2510.12710|Reflective-Self-Adaptation]], [[2510.08558|Early-Experience]], [[2508.04700|SEAgent]], [[2507.13152|SE-VLN]], [[2506.21669|SEEA-R1]], [[2506.01716|SCA]], [[2406.04151|AgentGym]], [[2403.02334|GCSL]]

> [!star] Key Papers
> - [[2406.04151|AgentGym]] — Multi-environment agent evolution via behavioral cloning + self-evolution (AGENTEVOL); showed agents can generalize across diverse tasks
> - [[2506.01716|SCA]] — Self-Challenging Agent: generates its own hard problems to practice on, driving continuous capability growth

**Skill, Memory & Environment Curation** — Frameworks that build their self-evolution around an explicit external artifact — a skill library, episodic memory store, evolving harness/scaffold, or synthetic environment/benchmark — that accumulates across rounds and feeds back into the agent, including self-play on real software repositories.
- [[2607.28568|Frontis-MA1]], [[2607.00272|ASPIRE]], [[2606.09498|Self-Harness]], [[2606.08671|SkillHone]], [[2605.15188|FutureSim]], [[2605.15155|SDAR]], [[2605.06614|SkillOS]], [[2604.25850|Agentic-Harness-Engineering]], [[2604.18292|Agent-World]], [[2601.03192|MemRL]], [[2512.18552|SSR]], [[2510.16079|EVOLVER]], [[2510.04618|ACE]], [[2509.19349|ShinkaEvolve]], [[2507.14172|SOAR]], [[2409.00872|SAGE]], [[2305.16291|Voyager]]

> [!star] Key Papers
> - [[2604.18292|Agent-World]] — ByteDance/Renmin's framework unifying real-world environment synthesis with continuous self-evolution; 14B agent evaluated on 23 benchmarks, with average tool-use scores more than doubling as environment diversity scales from 0 to 1,978
> - [[2510.16079|EVOLVER]] — Agents distill raw interaction trajectories into strategic principles; experience-driven lifecycle closes the self-improvement loop
> - [[2512.18552|SSR]] — Meta's Self-play SWE-RL: agents autonomously generate learning experiences from real codebases; +10.4 on SWE-bench Verified without human issue descriptions
> - [[2507.14172|SOAR]] — Self-improving operators for automated program refinement; LLMs iteratively improve their own code transformations

**Co-Evolutionary & Multi-Agent** — Multiple agents or model components (policy + environment, actor + critic) evolve together, each improving the other in a virtuous cycle.
- [[2605.13775|RoboEvolve]], [[2604.20987|Co-Evolve-Agents]], [[2603.28386|COvolve]], [[2603.17621|Complementary-RL]], [[2603.08403|SPIRAL]], [[2602.23413|EvoX]], [[2602.20057|AdaWorldPolicy]], [[2601.10402|ML-Master-2.0]], [[2601.06794|ECHO]], [[2510.26433|CoLA-World]], [[2509.03771|Co-Evolving-MARL]], [[2507.16518|C2-Evo]], [[2506.23468|NavMorph]], [[2504.21024|WebEvolver]], [[2502.05907|EvoAgent]], [[2302.01877|AdaptDiffuser]]

> [!star] Key Papers
> - [[2601.06794|ECHO]] — Policy and environment co-evolve: the environment generates harder challenges as the policy improves, and vice versa

> [!tip] From Models to Agents
> Self-improving models optimize weights; self-evolving agents optimize behavior. The key difference is persistent experience: EVOLVER and ACE show that distilling interaction history into reusable principles is what turns a self-improving model into a self-evolving agent.

---

## 5. Self-Evolving Embodied AI

When self-evolution meets physical agents: VLAs, WAMs, and robots that autonomously discover failure modes, generate new experience, and improve through real-world or simulated interaction. The embodied setting adds unique challenges — physical safety, sensor noise, and the cost of real-world data collection — making world-model-based imagination particularly valuable.

**Self-Evolving VLAs** — VLAs that improve through RL post-training, continual learning, or self-play without requiring an explicit world model.
- [[2607.15275|RoboTTT]], [[2605.10993|ECHO-VLA]], [[2605.01191|Sentinel-VLA]], [[2603.11653|VLA-RL-Continual-Learning]], [[2603.09030|PlayWorld]], [[2603.03818|VLA-Continual-Learning]], [[2602.21633|SC-VLA]], [[2602.10503|Long-Lived-Robots]], [[2602.03445|CRL-VLA]], [[2601.09512|CLARE]], [[2512.14666|EVOLVE-VLA]], [[2511.16166|EvoVLA]], [[2510.05580|MetaVLA]], [[2509.22195|Actions-as-Language]]

> [!star] Key Papers
> - [[2511.16166|EvoVLA]] — Self-evolving VLA framework that overcomes stage hallucination and fragile memory; the first end-to-end self-evolving VLA
> - [[2603.03818|VLA-Continual-Learning]] — Showed pre-trained VLAs are naturally resistant to catastrophic forgetting; simple sequential fine-tuning works

**Self-Evolving WAMs** — World models that autonomously improve through imagination, self-play, or co-evolution with their policy. The world model generates synthetic experience, enabling self-improvement without costly real-world interaction.
- [[2607.06988|WAM-TTT]], [[2606.32026|AdaJEPA]], [[2603.19370|VAMPO]], [[2603.08403|SPIRAL]], [[2602.14351|WIMLE]], [[2509.19292|SOE]], [[2506.23468|NavMorph]], [[2504.21024|WebEvolver]], [[2503.01584|SENSEI]], [[2502.05907|EvoAgent]], [[2401.16650|WMAR]]

> [!star] Key Papers
> - [[2603.08403|SPIRAL]] — Closed-loop self-improvement for action world models via reflective planning; the system critiques its own failures and adapts
> - [[2502.05907|EvoAgent]] — Self-evolving agent with continual world model; self-planning + self-control + self-reflection achieves +105% improvement on long-horizon tasks
> - [[2603.19370|VAMPO]] — RL optimization of visual dynamics in video action models via GRPO; bridges world model quality and action quality

**Self-Evolving Robots & Navigation** — Embodied agents that discover their own failure modes and improve through real-world or simulated experience, combining exploration, curiosity, and RL.
- [[2607.20110|Extreme-RGMT]], [[2607.12114|GaitSpan]], [[2607.04764|SLAM (Lifelong VPR)]], [[2607.01111|FAR]], [[2605.09387|NEXUS]], [[2604.07392|ERA]], [[2603.04029|Self-Adapting-RL]], [[2602.20057|AdaWorldPolicy]], [[2510.12693|ERA]], [[2508.12252|Robot-Trains-Robot]], [[2508.04700|SEAgent]], [[2507.13152|SE-VLN]], [[2506.21669|SEEA-R1]], [[2506.06658|SILVR]], [[2503.10949|SCDA]], [[2409.02561|VLNCL]]

> [!star] Key Papers
> - [[2506.21669|SEEA-R1]] — Tree-structured RL for self-evolving embodied agents; +24% via MCTS + generative reward
> - [[2603.04029|Self-Adapting-RL]] — World model residuals detect OOD states, triggering targeted self-adaptation

**Self-Discovery & Failure Detection** — Before self-evolution can happen, the agent must detect WHERE and WHY it's failing. These methods enable the detection step.
- [[2604.02965|SV-VLA]], [[2603.13528|Counterfactual-Failure-Synthesis]], [[2601.02295|CycleVLA]], [[2512.24426|CF-VLA]], [[2512.01119|World-Model-Surprise-Robustness]], [[2511.14148|AsyncVLA]], [[2510.09459|FIPER]], [[2510.01642|FailSafe]], [[2509.16072|I-FailSense]], [[2509.04018|FPC-VLA]], [[2506.09937|SAFE]], [[2505.12224|RoboFAC]], [[2503.01584|SENSEI]], [[2412.02818|RoboMD]], [[2410.00371|AHA]], [[2409.03966|VLM-Failure-Recovery]], [[2404.00756|Recover]], [[2005.05960|Plan2Explore]], [[1705.05363|ICM]]

> [!star] Key Papers
> - [[2510.09459|FIPER]] — Runtime failure prediction combining OOD detection with action uncertainty; predicts failures before they happen
> - [[2412.02818|RoboMD]] — RL adversary that actively discovers policy failure modes; finds what the agent can't do

> [!tip] Self-Evolving VLA vs Self-Evolving WAM
> VLAs self-evolve via RL fine-tuning (no world model needed) — simple, fast, and surprisingly resistant to forgetting. WAMs self-evolve via imagination loops — richer but more complex. The two converge when a VLA gains a world model: VLAW and VLA-JEPA + self-evolution represent this frontier.

---

## 6. Meta-Learning & Self-Adaptation

Learning to learn: models that adapt their own learning process, discover optimization algorithms, or rapidly adjust to new tasks from minimal data. While self-training improves outputs, meta-learning improves the learning procedure itself.

**Foundational Meta-RL & Representation Transfer** — Classic algorithmic families for rapid task adaptation: gradient-based meta-learning (MAML-style), context-conditioned policies (PEARL-style), model-based fast adaptation (GrBAL-style), and representation-based zero-shot transfer (successor features, forward-backward representations, option/behavior bases) — mostly evaluated on continuous-control and robotics benchmarks.
- [[2607.26370|Self-Adaptive-Learning-and-MPC]], [[2607.26345|MetaKoopman]], [[2604.24532|MORL-FB]], [[2604.11768|GC-PFO]], [[2602.19134|Mapping-Networks]], [[2601.19810|ULEE]], [[2512.19154|Adaptive-Stacking]], [[2510.20264|OpTI-BFM]], [[2506.13690|MASP]], [[2506.07259|ALINE]], [[2505.00787|Option-Keyboard-Basis]], [[2503.18684|OMLA]], [[2502.03752|SISL]], [[2410.05975|ConML]], [[2301.08028|Meta-RL-Tutorial]], [[2210.05639|DPO]], [[2112.15402|RER]], [[2111.09793|Robotic-Interestingness]], [[2103.07945|Forward-Backward-Representation]], [[2003.01239|Evolutionary-Meta-Learning-Legged]], [[1910.10897|Meta-World]], [[1903.08254|PEARL]], [[1803.11347|GrBAL]], [[1703.07326|One-Shot-Imitation-Learning]], [[1703.03400|MAML]], [[1606.05312|Successor-Features]]

> [!star] Key Papers
> - [[2301.08028|Meta-RL-Tutorial]] — Definitive survey structuring the meta-RL landscape: context-based, task-inference, and black-box approaches

**In-Context & Foundation-Model Meta-RL** — Recent methods where meta-RL emerges implicitly inside a large sequence model's forward pass — mesa-optimization in Transformers, in-context RL via meta-training on randomized worlds, and LLM/VLM agents that adapt at test time without an explicit outer meta-gradient loop.
- [[2606.29082|EFT]], [[2605.10899|RubricEM]], [[2512.16848|LAMER]], [[2506.10085|VITA-Value]], [[2502.02869|OmniRL]], [[2309.05858|Mesa-Optimization-Transformers]]

> [!star] Key Papers
> - [[2309.05858|Mesa-Optimization-Transformers]] — Mechanistic explanation of how Transformers implicitly learn optimization algorithms (mesa-optimization) in-context

**Self-Adapting Language Models** — LLMs that generate their own fine-tuning data and adaptation strategies, optimizing internal parameters without external supervision.
- [[2607.15314|Cura-1T]], [[2604.06169|In-Place-TTT]], [[2510.16932|Prompt-MII]], [[2510.03259|MASA]], [[2506.10943|SEAL]], [[1902.00751|Adapters]]

> [!star] Key Papers
> - [[2506.10943|SEAL]] — Models autonomously generate optimized fine-tuning data and adaptation strategies; outperforms GPT-4.1-generated synthetic data
> - [[2510.03259|MASA]] — Meta-Awareness via Self-Alignment: RL framework enabling models to develop self-awareness of their own capabilities and limitations

**Few-Shot Object Detection** — Meta-learning applied to visual recognition: learn to detect new object categories from very few examples by leveraging learned priors.
- [[2401.07629|FPD]], [[2105.01294|Feature-Hallucinator]], [[1909.13032|Meta-R-CNN]], [[1908.01998|Attention-RPN]], [[1812.01866|Feature-Reweighting-Detector]]

> [!star] Key Papers
> - [[1909.13032|Meta-R-CNN]] — General meta-learning framework for few-shot detection; class-attentive vectors modulate features per novel category
> - [[2401.07629|FPD]] — Fine-grained prototype distillation from mid-level features; state-of-the-art few-shot detection

**Few-Shot Classification & Cross-Domain Generalization** — Metric-based classifiers and task-augmentation strategies that generalize few-shot learning across domain shift, from the original prototype-based episodic training to adversarial and self-training extensions.
- [[2607.08374|JAM]], [[2104.14385|ATA]], [[2010.07734|STARTUP]], [[2001.08735|LTL-FWT]], [[1904.02239|Hyperbolic-ProtoNet]], [[1703.05175|Prototypical-Networks]]

> [!star] Key Papers
> - [[1703.05175|Prototypical-Networks]] — Simple mean-based class prototypes in embedding space; established episodic training as the few-shot learning standard
> - [[2104.14385|ATA]] — Adversarial task augmentation during meta-training; consistently improves cross-domain generalization across eight target domains

> [!tip] Meta-Learning vs Self-Training
> Self-training improves answers; meta-learning improves the learning algorithm. SEAL and MASA represent the convergence: models that meta-learn how to self-train more effectively.

---

## 7. Vision-Language Model Self-Improvement

Extending self-evolution beyond text-only LLMs to multimodal models that process both images and text. VLMs face unique challenges: hallucination, visual grounding errors, and cross-modal consistency — requiring self-improvement methods tailored to multimodal reasoning.

**Hallucination Reduction via Self-Consistency** — VLMs detect and correct their own hallucinations by checking internal consistency across different modalities or question framings.
- [[2606.03598|PHASER]], [[2605.29562|VLA-Pro]], [[2605.26820|VLA-Continual-Forgetting]], [[2605.20914|RISE-Self-Evolving-VLM]], [[2603.02556|VC-STaR]], [[2510.24285|ViPER]], [[2510.10487|Triangular-Consistency]], [[2509.23236|Self-Reflection-VLM]], [[2503.10705|ConDU]]

> [!star] Key Papers
> - [[2509.23236|Self-Reflection-VLM]] — Uses binary self-consistency signals to reduce hallucinations without external supervision
> - [[2510.10487|Triangular-Consistency]] — Cross-checks visual, textual, and reasoning outputs for mutual consistency; self-refinement through multi-modal agreement

**Multimodal Self-Evolution Frameworks** — End-to-end pipelines for VLM self-improvement covering data generation, training, and evaluation across vision-language tasks.
- [[2602.22859|DPE]], [[2601.03193|UniCorn]], [[2510.10606|ViSurf]], [[2510.02665|MLLM-Self-Improvement-Survey]], [[2509.15155|Self-Improving-EFM]], [[2508.19652|Vision-SR1]], [[2508.12137|Fine-Grained-VLM-Tuning]], [[2507.16663|MLLM-Self-Improvement]], [[2412.17451|M-STAR]], [[2410.08202|Mono-InternVL]]

> [!star] Key Papers
> - [[2412.17451|M-STAR]] — Self-evolving training framework for large multimodal models; iterative self-improvement across vision-language benchmarks
> - [[2510.02665|MLLM-Self-Improvement-Survey]] — First comprehensive survey of self-improvement methods for multimodal LLMs; maps the taxonomy and open challenges

> [!tip] The Multimodal Gap
> Text-only self-improvement is well-understood (STaR, Absolute Zero). The frontier is extending these methods to vision-language models, where verification is harder and hallucination is the central failure mode. Vision-Zero and M-STAR point the way.

---

## 8. Continual & Experiential Learning

Self-evolution over time: systems that accumulate knowledge from ongoing experience without catastrophic forgetting. While sections 1-4 focus on improving within a training run, continual learning ensures improvements persist across deployment episodes and new environments.

**Memory-Augmented Agent Systems** — LLM and multimodal agents that build persistent, retrievable memory banks of past experience, distilling raw interaction trajectories into reusable knowledge that improves future performance.
- [[2607.01988|Identity-Stable-Consolidation]], [[2605.10663|Evolving-RL]], [[2604.13074|PersonaVLM]], [[2604.04503|MIA]], [[2604.01007|Omni-SimpleMem]], [[2603.16856|OEL]], [[2510.04618|ACE]], [[2509.25140|ReasoningBank]], [[2508.19005|ELL-Framework]]

> [!star] Key Papers
> - [[2508.19005|ELL-Framework]] — Experience-driven Lifelong Learning: introduces the framework and StuLife benchmark for measuring continual self-improvement in realistic settings
> - [[2603.16856|OEL]] — Microsoft's Online Experiential Learning: LLMs continuously learn from deployment interactions without forgetting prior knowledge
> - [[2509.25140|ReasoningBank]] — Memory-aware test-time scaling: stores and retrieves reasoning patterns for efficient reuse across problems

**Embodied Continual Learning** — Physical robots and VLA policies that must retain manipulation, locomotion, and control skills across morphology changes, deployments, and new tasks without forgetting.
- [[2607.24207|FloAff-Kitchen]], [[2607.10350|ABot-AgentOS]], [[2607.06740|SMPL]], [[2605.15735|UAM]], [[2604.15814|Continual-Hand-Eye-Calibration]], [[2604.11306|Hierarchical-Episodic-Memory]], [[2604.10892|HECTOR]], [[2604.10096|ABot-Claw]], [[2603.24576|Chameleon-Episodic-Memory]], [[2603.24350|Emergent-Self]], [[2602.10503|Long-Lived-Robots]], [[2510.20328|MemER]], [[2501.10395|t-DGR]]

**Continual-Learning Theory & Forgetting Mechanisms** — Theoretical and mechanistic analyses of catastrophic forgetting: stability-plasticity tradeoffs, replay-buffer design, gradient orthogonalization, and architectural fixes.
- [[2607.24996|CPR]], [[2607.24031|UnSPC]], [[2607.21366|HOPE-Hilbert]], [[2607.05609|Predictive-Continual-Learning]], [[2605.29548|Capacity-Interference-Retention]], [[2605.15220|OP-MIX]], [[2605.14938|Octopus]], [[2605.12484|FST]], [[2604.27063|FADE]], [[2603.17684|AFSS]], [[2603.00903|Continual-RL-Theory]], [[2602.08040|FIRE]], [[2512.24695|Hope]], [[2512.09441|MoP-CIL]], [[2509.22562|Activation-Plasticity]], [[2507.10434|CLA]], [[2507.09177|Online-Agent-OA]], [[2507.07712|GDR-Federated]], [[2411.13852|ESRM]], [[2410.07812|TD-VCL]], [[2402.15109|MU-Mis]], [[2305.13622|SER]], [[2211.15944|Continual-Dreamer]]

**Multimodal Continual Skill Acquisition** — Agents that continually learn new skills from visual and language grounding, building an expanding repertoire without losing prior capabilities.
- [[2607.14852|LifelongVLA]], [[2607.07574|Context-Aware Force Estimation]], [[2607.00302|Splash]], [[2606.30988|MuSe]], [[2606.05395|VASO]], [[2604.18075|DPW]], [[2604.08532|SelfEvo]], [[2603.18743|Memento-Skills]], [[2603.17621|Complementary-RL]], [[2603.12056|XSkill]], [[2603.08763|SPREAD]], [[2603.07648|AtomicVLA]], [[2603.04560|MEMO]], [[2603.02951|CGL]], [[2602.03445|CRL-VLA]], [[2511.18085|Stellar-VLA]], [[2504.21024|WebEvolver]], [[2504.18471|AFM]], [[2410.04891|LoRA-Continual-Diffusion]]

> [!star] Key Papers
> - [[2603.12056|XSkill]] — Dual-stream framework for continual learning from visually-grounded experience; skills transfer across tasks and modalities

**Safety & Alignment Under Self-Evolution** — Investigating and mitigating the risks that arise when models evolve autonomously, including value drift, capability misalignment, and emergent unsafe behaviors.
- [[2606.15366|Robust-Conformal-CBF/CLF]], [[2602.23478|refineCBF]], [[2512.05356|Co-Improving-AI]], [[2509.26354|Misevolution]], [[2506.07468|SELF-REDTEAM]]

> [!star] Key Papers
> - [[2509.26354|Misevolution]] — Identifies "misevolution" as a novel safety risk: self-evolving models can drift from intended values during autonomous improvement
> - [[2506.07468|SELF-REDTEAM]] — Self-adversarial testing to catch safety regressions during evolution; the model red-teams itself after each improvement cycle

> [!tip] The Forgetting Problem
> Self-improvement without continual learning is a leaky bucket. ELL and OEL show that persistent experience memory is essential — otherwise, gains from one round of self-improvement are lost when the model encounters a new domain.

---

## 9. Surveys & Theoretical Foundations

Comprehensive reviews and theoretical analyses that map the self-evolving AI landscape, formalize when self-improvement converges, and identify open challenges.

- [[2603.25681|LLM-Self-Improvement-Survey]] — Unified closed-loop lifecycle framework for LLM self-improvement; covers data acquisition, selection, optimization, inference, and evaluation
- [[2404.14387|LLM-Self-Evolution-Survey]] — Structured taxonomy of self-evolution approaches: self-training, self-rewarding, RL-based, and evolutionary methods
- [[2510.02665|MLLM-Self-Improvement-Survey]] — First survey focused on multimodal LLM self-improvement; maps methods from text to vision-language
- [[2412.01951|Sharpening-Mechanism]] — Theoretical framework formalizing when and why self-improvement converges; identifies conditions for guaranteed improvement
- [[2408.07666|Model-Merging-in-LLMs/MLLMs]] — Comprehensive survey of model merging methods for combining knowledge across fine-tuned models
- [[2504.13173|Miras]] — Unified framework connecting test-time memorization, attentional bias, retention, and online optimization
- [[2506.21872|Continual-RL-Survey]] — Survey of continual reinforcement learning methods across environments and tasks
- [[2105.10919|Continual-World]] — Robotic benchmark suite of sequential Meta-World manipulation tasks for measuring forward transfer and forgetting in continual RL
- [[2507.21046|Self-Evolving-Agents-Survey]] — Comprehensive survey on self-evolving LLM-based agents
- [[2508.04227|VLM-Continual-Learning-Survey]] — Taxonomy of continual learning challenges specific to vision-language models
- [[2508.07407|Self-Evolving-AI-Agents-Survey]] — Survey on self-evolving AI agent architectures and methods
- [[2602.04411|Self-evolving-Embodied-AI]] — Survey on self-evolving systems in embodied AI settings
- [[2601.10679|Augmented-HRM]] — Mechanistic analysis of whether self-improving reasoning models truly develop hierarchical reasoning
- [[2603.15381|Autonomous-Learning-Framework]] — Lessons from cognitive science on why AI systems don't learn autonomously and how to address it

> [!tip] Starting Points
> New to self-evolving AI? Read the LLM Self-Evolution Survey (2024) for the taxonomy, then STaR and Absolute Zero for the two bookends of the field (simple bootstrapping vs. zero-data self-play).


---

## Cross-References

- [[08_Reinforcement-Learning]] — RL as the self-improvement engine
- [[10_Agents-and-Tool-Use]] — Self-evolving agents
- [[11_Robotics-and-Embodied-AI]] — Self-evolving embodied AI

---

*Next: [[10_Agents-and-Tool-Use]] for how self-improving agents use tools and multi-step plans.*