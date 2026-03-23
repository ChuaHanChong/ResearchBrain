---
title: "Self-Evolving AI — Topic Overview"
tags:
  - self-evolving
  - self-improvement
  - continual-learning
  - meta-learning
aliases:
  - Self-Evolving Overview
---

# Self-Evolving AI

> [!abstract] Overview
> AI systems that improve themselves through experience — from self-taught reasoning (STaR) to self-evolving agents (EvoAgent) to self-improving world models (SPIRAL). This topic bridges RL, continual learning, and meta-learning into autonomous self-improvement.

## Key Papers

| Paper | Year | Contribution |
| --- | --- | --- |
| [[2203.14465\|STaR]] | 2022 | Iterative bootstrapping of LLM reasoning |
| [[2403.09629\|Quiet-STaR]] | 2024 | Learning internal reasoning from general text |
| [[2401.10020\|Self-Rewarding LM]] | 2024 | LLM generates its own reward signal |
| [[2505.03335\|Absolute Zero]] | 2025 | Zero-data RL: model proposes and solves its own problems |
| [[2502.05907\|EvoAgent]] | 2025 | Self-evolving agent with continual world model |
| [[2603.08403\|SPIRAL]] | 2026 | Self-improving action world models via reflective planning |

> [!tip] Deep Dive
> See [[01_Self-Evolving|Self-Evolving 101]] and [[04-2_Self-Evolving-WAM-101]] for architectural blueprints.

## Cross-References

- [[04_Reinforcement-Learning]] — RL as the self-improvement engine
- [[10_Agents-and-Tool-Use]] — Self-evolving agents
- [[07_Robotics-and-Embodied-AI]] — Self-evolving embodied AI

---

## Complete Paper Listing

### Curriculum Learning (9)

| Paper | Year | Summary |
| --- | --- | --- |
| [[2504.05520\|ADARFT]] | 2025 | Researchers at USC and the University of Maryland developed ADARFT, a method that uses adaptive curriculum learning t... |
| [[2505.14970\|SEC]] | 2025 | Researchers at Mila, ServiceNow AI Research, and other institutions developed the Self-Evolving Curriculum (SEC), an ... |
| [[2507.22607\|VL-Cogito]] | 2025 | VL-Cogito, developed by researchers from DAMO Academy, Alibaba Group, Hupan Lab, and Fudan University, introduces a P... |
| [[2510.01135\|PCL]] | 2025 | Researchers from Meta Superintelligence Labs and Cornell University developed Prompt Curriculum Learning (PCL), an ef... |
| [[2510.09001\|DARO]] | 2025 | DARO introduces an adaptive reweighting algorithm for Reinforcement Learning with Verifiable Rewards (RLVR) that dyna... |
| [[2511.07317\|RLVE]] | 2025 | RLVE introduces adaptive verifiable environments that procedurally generate an unbounded supply of dynamically challe... |
| [[2512.02472\|R-FEW]] | 2025 | The R-FEW framework introduces a method for Large Language Models to self-evolve stably and controllably using minima... |
| [[2512.06835\|DoGe]] | 2025 | The DoGe framework from Shanghai Artificial Intelligence Laboratory and collaborators introduces a context-first self... |
| [[2601.22628\|TTCS]] | 2026 | A co-evolving framework, TTCS, introduces a Synthesizer policy to dynamically generate a curriculum of capability-ali... |

### Meta-Learning (9)

| Paper | Year | Summary |
| --- | --- | --- |
| [[1908.01998\|Attention-RPN]] | 2019 | Researchers from the Hong Kong University of Science and Technology and Tencent developed a few-shot object detection... |
| [[1909.13032\|Meta R-CNN]] | 2019 | Meta R-CNN, developed by researchers at Sun Yat-sen University and DarkMatter AI Research, introduces a general meta-... |
| [[2112.15402\|RER]] | 2021 | Relational Experience Replay (RER) introduces a bi-level learning framework that dynamically adjusts sample weights t... |
| [[2210.05639\|DPO]] | 2022 | Researchers at FLAIR Oxford, UC Berkeley, and Google Brain discovered a new reinforcement learning algorithm, Discove... |
| [[2301.08028\|Meta-RL Tutorial]] | 2023 | This tutorial comprehensively structures the field of Meta-Reinforcement Learning, categorizing diverse algorithms an... |
| [[2309.05858\|Mesa-Optimization Transformers]] | 2023 | Researchers at Google's Paradigms of Intelligence Team and ETH Zürich provide a mechanistic explanation for emergent ... |
| [[2401.07629\|FPD]] | 2024 | FPD introduces a method for few-shot object detection that distills fine-grained prototypes from mid-level features a... |
| [[2506.10943\|SEAL]] | 2025 | Researchers from MIT's Improbable AI Lab developed Self-Adapting Language Models (SEAL), a framework enabling LLMs to... |
| [[2510.03259\|MASA]] | 2025 | Researchers from KAIST and AITRICS developed Meta-Awareness via Self-Alignment (MASA), a reinforcement learning frame... |

### Self-Improvement (51)

| Paper | Year | Summary |
| --- | --- | --- |
| [[2403.09629\|Quiet-STaR]] | 2024 | Quiet-STaR enables language models to self-supervise the learning of internal reasoning processes, or 'thoughts,' by ... |
| [[2404.14387\|LLM Self-Evolution Survey 2024]] | 2024 | This survey paper by Tao et al. provides a structured overview of self-evolution approaches for Large Language Models... |
| [[2406.04151\|AgentGym]] | 2024 | AGENTGYM provides a framework for evolving Large Language Model-based agents across diverse environments by integrati... |
| [[2412.01951\|Sharpening Mechanism]] | 2024 | This research introduces "sharpening" as a theoretical framework to explain and formalize self-improvement in languag... |
| [[2412.09413\|STILL-2]] | 2024 | Researchers at Renmin University of China introduce STILL-2, an open-source framework that reproduces o1-like "slow-t... |
| [[2412.17451\|M-STAR]] | 2024 | Researchers at HKUST and collaborating institutions present M-STAR, a self-evolving training framework for large mult... |
| [[2501.01478\|MCTS Process Supervision]] | 2025 | Researchers at AI Lab, Giant Network developed an iterative self-training approach that uses Monte Carlo Tree Search ... |
| [[2502.05234\|TURN]] | 2025 | A method called TURN is introduced to automatically identify the near-optimal sampling temperature for large language... |
| [[2502.08922\|SCIR]] | 2025 | The Self-Consistent Internal Rewards (SCIR) framework improves Large Language Model alignment by enforcing consistenc... |
| [[2503.03746\|Process-based Self-Rewarding]] | 2025 | Researchers from Nanjing University and Microsoft Research Asia introduce a breakthrough "Process-based Self-Rewardin... |
| [[2503.18866\|BoLT]] | 2025 | Researchers at Stanford University, the University of Toronto, and the Vector Institute introduced "Reasoning to Lear... |
| [[2504.08672\|Genius]] | 2025 | Genius is a purely unsupervised self-training framework designed to enhance Large Language Model reasoning without ex... |
| [[2504.16084\|TTRL]] | 2025 | TTRL is a framework enabling Large Language Models to self-improve through Reinforcement Learning on unlabeled test d... |
| [[2504.21024\|WebEvolver]] | 2025 | The WebEvolver framework from Tencent AI Lab boosts self-improving web agents by co-evolving a world model that gener... |
| [[2505.24726\|Reflect Retry Reward]] | 2025 | Writer, Inc. researchers develop a reinforcement learning framework that trains LLMs to generate more effective self-... |
| [[2506.01716\|SCA]] | 2025 | The Self-Challenging Agent (SCA) framework enables Large Language Model (LLM) agents to self-improve by generating hi... |
| [[2506.06499\|SPARQ]] | 2025 | SPARQ introduces an algorithm for generating high-quality and diverse synthetic math problems by leveraging Quality-D... |
| [[2506.07468\|SELF-REDTEAM]] | 2025 | Researchers from the University of Washington and Stanford University developed SELF-REDTEAM, an online multi-agent r... |
| [[2506.08989\|SwS]] | 2025 | The SwS framework enhances Large Language Model reasoning by enabling self-aware, weakness-driven problem synthesis f... |
| [[2506.24119\|SPIRAL]] | 2025 | The SPIRAL framework trains Large Language Models (LLMs) to acquire transferable reasoning skills by engaging in self... |
| [[2507.14172\|SOAR]] | 2025 | SOAR (Self-improving Operators for Automated program Refinements) is a framework that enables large language models (... |
| [[2507.16518\|C2-Evo]] | 2025 | The C |
| [[2508.19005\|ELL Framework]] | 2025 | The research introduces the Experience-driven Lifelong Learning (ELL) framework and the StuLife benchmark to advance ... |
| [[2509.07414\|LSP]] | 2025 | Meta Superintelligence Labs developed Language Self-Play (LSP), a reinforcement learning framework that enables large... |
| [[2509.14234\|CaT]] | 2025 | A new method, Compute as Teacher (CaT), generates supervision signals for large language models in post-training scen... |
| [[2509.15155\|Self-Improving EFM]] | 2025 | Researchers from Google DeepMind developed a two-stage post-training framework that integrates online reinforcement l... |
| [[2509.15172\|MACA]] | 2025 | Researchers at Meta AI and collaborating institutions developed Multi-Agent Consensus Alignment (MACA), a post-traini... |
| [[2509.15194\|EVOL-RL]] | 2025 | EVOL-RL introduces an evolutionary, label-free reinforcement learning framework for large language models, mitigating... |
| [[2509.19349\|ShinkaEvolve]] | 2025 | ShinkaEvolve combines large language models with advanced evolutionary computation to create an open-source framework... |
| [[2509.23236\|Self-Reflection VLM]] | 2025 | A method for reducing hallucinations in Vision-Language Models leverages internal self-consistency, using simple bina... |
| [[2509.24726\|Socratic-Zero]] | 2025 | SOCRATIC-ZERO introduces a data-free framework enabling large language models to autonomously improve their reasoning... |
| [[2509.25140\|ReasoningBank]] | 2025 | A novel memory framework, ReasoningBank, coupled with Memory-aware Test-Time Scaling (MaTTS), enables large language ... |
| [[2509.25541\|Vision-Zero]] | 2025 | VISION-ZERO introduces a zero-human-in-the-loop, gamified self-play framework for Vision-Language Models, enabling th... |
| [[2509.26354\|Misevolution]] | 2025 | Researchers from Shanghai AI Lab and Shanghai Jiao Tong University identify 'misevolution' as a novel safety challeng... |
| [[2509.26626\|RSA]] | 2025 | This research introduces Recursive Self-Aggregation (RSA), an inference-time method for Large Language Models that en... |
| [[2510.02263\|RLAD]] | 2025 | The RLAD framework enables large language models to self-discover and leverage high-level reasoning abstractions, lea... |
| [[2510.02665\|MLLM Self-Improvement Survey]] | 2025 | Researchers from UT Dallas, University of Toronto, University of Notre Dame, and MBZUAI present the first comprehensi... |
| [[2510.02752\|Self-Aware RL for LLMs]] | 2025 | Researchers at Pennsylvania State University and Shanghai Artificial Intelligence Laboratory developed a self-aware R... |
| [[2510.04618\|ACE]] | 2025 | The Agentic Context Engineering (ACE) framework dynamically evolves and curates comprehensive 'playbook' contexts for... |
| [[2510.10487\|Triangular Consistency]] | 2025 | This research introduces a self-refinement framework for Vision-Language Models (VLMs) that utilizes a "Triangular Co... |
| [[2510.16079\|EVOLVER]] | 2025 | EVOLVER enables large language model agents to autonomously learn and improve from their own experiences by distillin... |
| [[2510.23595\|MAE]] | 2025 | A framework called Multi-Agent Evolve (MAE) enables large language models (LLMs) to improve their reasoning abilities... |
| [[2510.24285\|ViPER]] | 2025 | ViPER, a self-evolutionary framework, iteratively enhances Vision-Language Models' fine-grained visual perception by ... |
| [[2510.24684\|SPICE]] | 2025 | A research team from FAIR at Meta and NUS developed SPICE, a reinforcement learning framework that enables large lang... |
| [[2511.01191\|Self-Harmony]] | 2025 | The Self-Harmony framework enhances Large Language Model reasoning at test-time without external supervision by lever... |
| [[2512.18552\|SSR]] | 2025 | Meta FAIR researchers developed Self-play SWE-RL (SSR), a training paradigm for software agents that autonomously gen... |
| [[2601.06794\|ECHO]] | 2026 | ECHO, a framework for training Large Language Model agents, introduces a co-evolutionary paradigm where the policy an... |
| [[2602.23413\|EvoX]] | 2026 | EvoX is a meta-evolutionary framework that enables LLM-driven optimization systems to dynamically adapt and improve t... |
| [[2603.12056\|XSkill]] | 2026 | XSKILL introduces a dual-stream framework that enables multimodal agents to continually learn from visually-grounded ... |
| [[2603.16856\|OEL]] | 2026 | Microsoft Research introduced an Online Experiential Learning (OEL) framework that allows large language models to co... |
| [[2603.17621\|Complementary RL]] | 2026 | Complementary Reinforcement Learning introduces a framework where a policy actor and an experience extractor co-evolv... |

### Self-Training & Bootstrapping (2)

| Paper | Year | Summary |
| --- | --- | --- |
| [[2203.14465\|STaR]] | 2022 | The STaR (Self-Taught Reasoner) algorithm enables large language models to iteratively improve their reasoning capabi... |
| [[2506.00467\|SST]] | 2025 | The SST framework introduces an efficient and robust approach to semi-supervised learning that leverages Self-Adaptiv... |
