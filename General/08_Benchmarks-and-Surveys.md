---
title: "Benchmarks & Surveys — Topic Overview"
tags:
  - benchmark
  - dataset
  - survey
  - evaluation
aliases:
  - Benchmarks Overview
---

# Benchmarks & Surveys

> [!abstract] Overview
> A cross-cutting index of benchmarks, datasets, and survey papers organized by domain. Surveys map the landscape and define taxonomies; benchmarks measure progress and expose capability gaps; dataset papers address how to collect, curate, and select training data at scale.

---

## 1. Foundation Model & Transformer Surveys

Surveys that chart the Transformer architecture landscape — from efficient attention mechanisms through training recipes to parameter-efficient adaptation. Together they define the "how to build" side of modern AI.

**Efficient Architectures & Attention** — How to make Transformers faster without sacrificing quality, covering sparse attention, linear attention, and compact ViT designs.
- [[2009.06732|Efficient Transformers Survey]], [[2508.09834|Efficient LLM Architectures Survey]], [[2505.03113|Lightweight ViT Survey]]

> [!star] Key Papers
> - [[2009.06732|Efficient Transformers Survey]] — The foundational taxonomy from Google Research; classifies all efficient attention variants
> - [[2508.09834|Efficient LLM Architectures Survey]] — Updated 2025 taxonomy unifying efficient architectural designs and optimization strategies for LLMs

**Training Recipes & Scaling** — Practical guidance on mixed precision, distillation, pruning, and the full training pipeline for large models.
- [[2302.01107|Efficient Transformer Training Survey]], [[2501.09223|LLM Foundations]], [[2505.13840|EfficientLLM]]

> [!star] Key Papers
> - [[2302.01107|Efficient Transformer Training Survey]] — First comprehensive categorization of training efficiency techniques
> - [[2505.13840|EfficientLLM]] — Empirical evaluation framework assessing efficiency techniques across architecture, training, and inference dimensions

**Parameter-Efficient Fine-Tuning (PEFT)** — LoRA, adapters, prompt tuning, and their systematic comparison. The PEFT landscape evolved rapidly from 2023 to 2025.
- [[2312.12148|PEFT Survey]], [[2501.13787|PEFT Survey (2025)]], [[2504.14117|PEFT A2Z]], [[2603.01097|LoRA Knowledge Memory]]

> [!star] Key Papers
> - [[2312.12148|PEFT Survey]] — The original comprehensive review of PEFT methods for pre-trained models
> - [[2603.01097|LoRA Knowledge Memory]] — Audits LoRA as a parametric knowledge store, revealing what fine-tuning actually memorizes

**Model Merging & Composition** — Combining multiple fine-tuned models into a single improved model without retraining.
- [[2408.07666|Model Merging Survey]]

**LLM Fine-Tuning Practice** — End-to-end guides for practitioners covering method selection, hyperparameter tuning, and deployment.
- [[2408.13296|LLM Fine-Tuning Guide]]

> [!tip] The PEFT Evolution
> Three PEFT surveys in two years (2023, 2025 survey, 2025 A2Z) reflect how fast this field moves. The LoRA Knowledge Memory paper adds a critical new dimension: understanding *what* LoRA actually stores. Start with the 2023 survey for foundations, then read the A2Z paper for the latest taxonomy.

---

## 2. Vision-Language & Multimodal Surveys

Surveys covering multimodal LLMs, open-vocabulary learning, hallucination, and the emerging field of multimodal reasoning.

**Multimodal LLM Architecture & Efficiency** — How to build and deploy multimodal models that understand both images and text.
- [[2306.13549|MLLM Survey]], [[2405.10739|Efficient MLLM Survey]]

> [!star] Key Papers
> - [[2306.13549|MLLM Survey]] — The definitive 2023 survey mapping the multimodal LLM landscape
> - [[2405.10739|Efficient MLLM Survey]] — Focuses specifically on making multimodal LLMs practical for deployment

**Open-Vocabulary & Hallucination** — Extending VLMs to recognize novel categories and mitigating their tendency to hallucinate.
- [[2306.15880|Open Vocabulary Learning]], [[2402.00253|LVLM Hallucination Survey]]

> [!star] Key Papers
> - [[2402.00253|LVLM Hallucination Survey]] — Categorizes hallucination types, root causes, and mitigation strategies for VLMs

**Multimodal Reasoning** — Surveys on how multimodal models reason across modalities, combining visual and textual information for complex inference.
- [[2504.03151|Multimodal Reasoning Survey]]

> [!tip] The Hallucination Problem
> VLM hallucination remains one of the biggest barriers to deployment. The LVLM Hallucination Survey provides the taxonomy; the Efficient MLLM Survey shows how architectural choices affect both hallucination rates and inference cost.

---

## 3. Reinforcement Learning Surveys

Surveys spanning classical RL, its intersection with causal inference, continual learning, and the emerging field of RL-based reasoning in LLMs.

**RL Fundamentals & Paradigms** — Foundational overviews and comparisons of deep RL approaches.
- [[2412.05265|RL Overview]], [[2110.01411|DRL vs ES Survey]]

> [!star] Key Papers
> - [[2412.05265|RL Overview]] — Sutton's modern RL overview; the authoritative reference for the field

**Causal & Continual RL** — Extending RL with causal reasoning and lifelong learning capabilities.
- [[2302.05209|Causal RL Survey]], [[2506.21872|Continual RL Survey]]

> [!star] Key Papers
> - [[2302.05209|Causal RL Survey]] — Maps the intersection of causal inference and RL; crucial for sample-efficient policy learning
> - [[2506.21872|Continual RL Survey]] — Covers lifelong learning in RL, addressing catastrophic forgetting in sequential task settings

**RL for Reasoning** — How RL drives chain-of-thought and multi-step reasoning in large language models.
- [[2501.09686|Large Reasoning Models Survey]]

> [!tip] The RL-Reasoning Connection
> The Large Reasoning Models Survey bridges two worlds: RL researchers studying reward optimization and LLM researchers studying chain-of-thought. Post-DeepSeek-R1, this intersection is where much of the field's energy is focused.

---

## 4. Robotics & Embodied AI Surveys

Surveys mapping the robotics landscape from embodied AI simulators through VLA architectures to world-model-augmented control. This domain has the highest survey density, reflecting rapid growth from 2021 to 2025.

**Embodied AI Foundations** — Broad surveys covering simulators, task hierarchies, and the overall embodied AI research landscape.
- [[2103.04918|Embodied AI Survey 2021]], [[2407.06886|ARIO]]

> [!star] Key Papers
> - [[2407.06886|ARIO]] — Comprehensive 2024 survey introducing the ARIO dataset standard for cross-study comparison
> - [[2103.04918|Embodied AI Survey 2021]] — Established the simulator-task-agent pyramid that later work builds on

**VLA & World Model Architectures** — Surveys focused specifically on vision-language-action models and world models for robot control.
- [[2405.14093|VLA Survey]], [[2411.14499|World Models Survey 2024]], [[2509.20021|Embodied AI LLM-WM Survey]], [[2506.20134|3D World Models Survey]]

> [!star] Key Papers
> - [[2509.20021|Embodied AI LLM-WM Survey]] — Maps the joint MLLM + world model architecture roadmap; the most forward-looking survey in this space
> - [[2506.20134|3D World Models Survey]] — Reviews the transition from 2D to 3D world models with spatial understanding

**Control & Planning** — Surveys on combining model-predictive control with RL for robot manipulation and locomotion.
- [[2502.02133|MPC-RL Survey]]

> [!tip] Survey Progression
> Read embodied AI surveys chronologically: 2021 survey for foundations, ARIO (2024) for the current landscape and dataset standards, then the LLM-WM Survey (2025) for the architectural roadmap ahead.

---

## 5. Self-Evolving AI Surveys

Surveys covering AI systems that improve themselves through experience, self-play, or evolutionary mechanisms — spanning both LLMs and embodied agents.

**LLM Self-Evolution** — How language models improve autonomously through self-training, self-play, and feedback loops.
- [[2404.14387|LLM Self-Evolution Survey]], [[2510.02665|MLLM Self-Improvement Survey]]

> [!star] Key Papers
> - [[2404.14387|LLM Self-Evolution Survey]] — Defines the taxonomy: self-training, self-play, and self-refinement as distinct mechanisms

**Self-Evolving Agents** — Broader agent paradigm where systems evolve their own capabilities toward increasingly general intelligence.
- [[2507.21046|Self-Evolving Agents Survey]]

> [!star] Key Papers
> - [[2507.21046|Self-Evolving Agents Survey]] — Maps the path from self-improving agents to ASI; the most ambitious survey in this space

> [!tip] Self-Evolution Maturity
> The LLM Self-Evolution Survey covers text-only self-improvement. The MLLM Self-Improvement Survey extends to multimodal settings. The Self-Evolving Agents Survey goes furthest, considering agents that evolve across environments.

---

## 6. Context Engineering & Agent Memory Surveys

An emerging survey domain covering how to optimize the information supplied to LLMs and how agents maintain memory across interactions.

**Context Engineering** — Formalizing the discipline of structuring, selecting, and optimizing context windows for LLMs.
- [[2507.13334|Context Engineering Survey]], [[2510.26493|Context Engineering 2.0]]

> [!star] Key Papers
> - [[2507.13334|Context Engineering Survey]] — First to formalize "Context Engineering" as a systematic discipline beyond prompt engineering
> - [[2510.26493|Context Engineering 2.0]] — Redefines context engineering with dynamic, adaptive context management strategies

**Agent Memory Systems** — How AI agents store, retrieve, and manage information across interactions and tasks.
- [[2512.13564|AI Agent Memory Survey]]

> [!star] Key Papers
> - [[2512.13564|AI Agent Memory Survey]] — Introduces a "Forms-Functions-Dynamics" framework for analyzing memory in AI agents

> [!tip] Beyond Prompt Engineering
> Context engineering is the 2025 evolution of prompt engineering. The first survey defines the field; the 2.0 version adds dynamic adaptation. Combined with agent memory systems, these surveys define how future AI systems will manage their information flow.

---

## 7. Evolutionary & Self-Supervised Learning Surveys

Surveys at the intersection of evolutionary computation and self-supervised learning, plus specialized visual architecture surveys.

- [[2504.07213|E-SSL Survey]]

> [!star] Key Papers
> - [[2504.07213|E-SSL Survey]] — First systematic review combining evolutionary machine learning with self-supervised learning; maps a largely unexplored intersection

> [!tip] Underexplored Territory
> The E-SSL survey reveals that evolutionary methods and self-supervised learning are rarely combined despite natural synergies. This intersection may yield novel training paradigms as both fields mature.

---

## 8. Robotics Benchmarks & Datasets

The data and evaluation infrastructure for embodied AI. Datasets provide training signal, benchmarks measure progress, and together they define what the field considers solved vs. open.

**Cross-Embodiment Datasets** — Large-scale datasets spanning multiple robot types, enabling training of generalist policies.
- [[2310.08864|OXE]], [[2503.06669|AgiBot World]], [[2307.00595|RH20T]], [[2412.13877|RoboMIND]]

> [!star] Key Papers
> - [[2310.08864|OXE]] — Open X-Embodiment: 1M+ trajectories from 22 robot types; the ImageNet moment for robotics
> - [[2503.06669|AgiBot World]] — Large-scale manipulation platform with diverse environments and embodiments

**Simulation Benchmarks** — Standardized simulation environments for reproducible policy evaluation.
- [[1909.12271|RLBench]], [[2112.03227|CALVIN]], [[2306.03310|LIBERO]], [[2405.05941|SIMPLER]]

> [!star] Key Papers
> - [[2306.03310|LIBERO]] — Lifelong robot learning benchmark with 5 suites and 130 tasks; tests continual learning
> - [[2405.05941|SIMPLER]] — Evaluates whether simulation performance predicts real-world success; bridges the sim-to-real gap

> [!tip] Benchmark Selection
> Start with LIBERO or CALVIN for standardized simulation evaluation. Use OXE for cross-embodiment pretraining. SIMPLER tells you whether your sim results will hold up in the real world.

---

## 9. Spatial & 3D Reasoning Benchmarks

Benchmarks that test whether models truly understand spatial relationships, 3D structure, and multi-hop compositional spatial reasoning.

**Visual Spatial Reasoning** — Binary and multi-choice spatial relationship evaluation for VLMs.
- [[2205.00363|VSR]], [[2401.12168|SpatialVLM]], [[2406.02537|TopViewRS]]

**Multi-View & Compositional** — Benchmarks requiring reasoning across multiple viewpoints or chaining spatial inferences.
- [[2603.18892|MultihopSpatial]], [[2603.16506|VIEW2SPACE]]

> [!star] Key Papers
> - [[2603.18892|MultihopSpatial]] — Tests multi-hop compositional spatial reasoning; exposes failures in models that pass simpler spatial tests
> - [[2401.12168|SpatialVLM]] — Evaluates 3D spatial reasoning in VLMs with real-world spatial queries

> [!tip] Spatial Reasoning Gap
> Most VLMs pass simple spatial tests (VSR) but fail multi-hop reasoning (MultihopSpatial). This gap reveals that current models memorize spatial patterns rather than truly reasoning about space.

---

## 10. Video Understanding & Temporal Benchmarks

Benchmarks for video-level reasoning that require understanding temporal dynamics, audio-visual integration, and spatio-temporal relationships.

- [[2603.14145|MMOU]], [[2503.23765|STI-Bench]], [[2507.18342|EgoExoBench]]

> [!star] Key Papers
> - [[2603.14145|MMOU]] — Joint audio-visual reasoning benchmark with 15K questions; tests true multimodal video understanding
> - [[2503.23765|STI-Bench]] — Evaluates spatio-temporal world understanding; goes beyond frame-level perception

> [!tip] Beyond Frame-Level
> Both benchmarks test capabilities that frame-level VLMs cannot solve. Models need temporal reasoning (STI-Bench) and cross-modal integration (MMOU) to succeed.

---

## 11. Reasoning & Cognitive Benchmarks

Benchmarks that evaluate logical reasoning, cognitive planning, and visual logic in language and multimodal models.

- [[2309.15129|CogEval]], [[2504.15279|VisuLogic]], [[2505.24760|REASONING GYM]], [[2512.06104|CompressARC]], [[2512.14693|URM]]

> [!star] Key Papers
> - [[2309.15129|CogEval]] — Tests cognitive maps and planning in LLMs; inspired by cognitive science experiments
> - [[2512.06104|CompressARC]] — Addresses the ARC-AGI benchmark via compression-based reasoning; 20% improvement over baselines
> - [[2505.24760|REASONING GYM]] — RL environments with verifiable rewards for training and evaluating reasoning

> [!tip] Reasoning vs. Pattern Matching
> CogEval and CompressARC test fundamentally different reasoning capabilities than standard NLP benchmarks. They reveal whether models can plan (CogEval) or abstract (CompressARC) rather than just pattern-match.

---

## 12. Data Quality, Selection & Annotation

Papers addressing how to build better training datasets through curation, selection, annotation automation, and analysis of data quality issues.

**Data Selection & Curation** — Methods for selecting the most valuable training data from large pools.
- [[2412.00420|TAROT]], [[2504.13161|Nemotron-CLIMB]]

> [!star] Key Papers
> - [[2412.00420|TAROT]] — Targeted data selection via Whitened Feature Distance and optimal transport; selects high-value subsets from massive pools
> - [[2504.13161|Nemotron-CLIMB]] — NVIDIA's automated framework for discovering and curating high-quality training data

**Annotation & Semi-Supervised Tools** — Reducing annotation cost through foundation-model-assisted labeling.
- [[2407.11464|Crowd-SAM]], [[2406.09294|DINOv2 (dataset application)]]

**Data Quality Analysis** — Understanding and diagnosing issues in training data.
- [[2409.14401|In-Class Data Imbalance]], [[2602.11217|Magic Correlations]]

> [!star] Key Papers
> - [[2409.14401|In-Class Data Imbalance]] — Reveals that datasets contain disproportionate sub-population representation within classes, not just across classes
> - [[2602.11217|Magic Correlations]] — Analyzes how accuracy and confidence transfer from pretraining to downstream tasks; reveals when more data helps and when it does not

> [!tip] Data Quality Over Quantity
> The In-Class Data Imbalance and Magic Correlations papers share a theme: naively adding more data does not always help. Targeted selection (TAROT, Nemotron-CLIMB) consistently outperforms random scaling.

---

## 13. Model Evaluation & Architecture Analysis

Benchmarks and analytical studies focused on evaluating model architectures, detection systems, and interpretability.

**Detection & Recognition** — Benchmarks and methods for evaluating object detection and interpretable visual recognition.
- [[2410.13842|D-FINE]], [[2410.20722|ProtoViT]], [[2505.01109|SSL-MIL Pathology Benchmark]]

> [!star] Key Papers
> - [[2410.13842|D-FINE]] — Redefines bounding box regression in DETR models; transforms coordinate prediction into fine-grained distribution refinement
> - [[2505.01109|SSL-MIL Pathology Benchmark]] — Reveals that simple instance-based MIL methods combined with strong SSL features outperform complex architectures

**LLM Inference & Representation Analysis** — Studies analyzing how model architectures and adaptations affect inference efficiency and learned representations.
- [[2603.02188|MLRA]], [[2602.15029|Language Symmetry Representations]]

> [!star] Key Papers
> - [[2603.02188|MLRA]] — Multi-Head Low-Rank Attention enhances LLM inference efficiency for long contexts
> - [[2602.15029|Language Symmetry Representations]] — Proves that translation symmetry in word co-occurrence statistics determines representational geometry

> [!tip] Simplicity Wins
> Both the SSL-MIL benchmark and D-FINE share a lesson: simpler methods with strong foundations often beat complex architectures. Evaluate against these baselines before adding complexity.

---

## Cross-References

- [[01_Foundation-Models]] — Transformer architecture surveys and training recipes
- [[02_Vision-Language-Models]] — VLM and open-vocabulary surveys in context
- [[04_Reinforcement-Learning]] — RL surveys and reasoning benchmarks
- [[07_Robotics-and-Embodied-AI]] — Robotics datasets and benchmarks applied
- [[11_Self-Evolving-AI]] — Self-evolving paradigm surveys

---

*This note indexes surveys and benchmarks across the vault. For topic-specific context and paper groupings, see the individual General/ overview files.*
