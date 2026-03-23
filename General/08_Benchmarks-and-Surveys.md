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
> A cross-cutting index of the most important benchmarks, datasets, and survey papers across all topics in the vault. Organized by domain rather than chronology.

---

## Surveys by Domain

### Foundation Models & Transformers
| Paper | Year | Scope |
| --- | --- | --- |
| [[2009.06732\|Efficient Transformers Survey]] | 2020 | Linear attention, sparse attention, efficient architectures |
| [[2101.01169\|Transformers in Vision Survey]] | 2021 | ViTs for classification, detection, segmentation |
| [[2302.01107\|Efficient Transformer Training]] | 2023 | Training efficiency: mixed precision, distillation, pruning |
| [[2312.12148\|PEFT Survey]] | 2023 | LoRA, adapters, prompt tuning methods |
| [[2408.07666\|Model Merging Survey]] | 2024 | Combining multiple fine-tuned models |

### Vision-Language Models
| Paper | Year | Scope |
| --- | --- | --- |
| [[2306.13549\|MLLM Survey]] | 2023 | Comprehensive survey of multimodal LLMs |
| [[2306.15880\|Open Vocabulary Learning]] | 2023 | Open-vocabulary detection, segmentation, recognition |
| [[2402.00253\|LVLM Hallucination Survey]] | 2024 | Types, causes, and mitigation of VLM hallucination |
| [[2405.10739\|Efficient MLLM Survey]] | 2024 | Making multimodal LLMs practical |
| [[2504.03151\|Multimodal Reasoning Survey]] | 2025 | Reasoning in multimodal models |

### Reinforcement Learning
| Paper | Year | Scope |
| --- | --- | --- |
| [[2412.05265\|RL Overview]] | 2024 | Sutton's modern RL overview |
| [[2302.05209\|Causal RL Survey]] | 2023 | Causal inference meets RL |
| [[2110.01411\|DRL vs ES Survey]] | 2021 | Deep RL vs evolutionary strategies |
| [[2506.21872\|Continual RL Survey]] | 2025 | Lifelong/continual learning in RL |
| [[2501.09686\|Large Reasoning Models Survey]] | 2025 | RL-based reasoning in LLMs |

### Robotics & Embodied AI
| Paper | Year | Scope |
| --- | --- | --- |
| [[2103.04918\|Embodied AI Survey 2021]] | 2021 | Simulators, tasks, pyramid hierarchy |
| [[2407.06886\|ARIO]] | 2024 | Comprehensive embodied AI + ARIO dataset standard |
| [[2509.20021\|Embodied AI LLM-WM Survey]] | 2025 | Joint MLLM-WM architecture roadmap |
| [[2405.14093\|VLA Survey]] | 2024 | VLA models for embodied AI |
| [[2411.14499\|World Models Survey 2024]] | 2024 | Understanding vs predicting: world model landscape |
| [[2502.02133\|MPC-RL Survey]] | 2025 | MPC + RL integration for control |

### Self-Evolving AI
| Paper | Year | Scope |
| --- | --- | --- |
| [[2404.14387\|LLM Self-Evolution Survey]] | 2024 | Self-evolving LLMs: taxonomy and methods |
| [[2510.02665\|MLLM Self-Improvement Survey]] | 2025 | Self-improvement in multimodal LLMs |
| [[2507.21046\|Self-Evolving Agents Survey]] | 2025 | Self-evolving agents toward ASI |

---

## Key Benchmarks & Datasets

### Robotics
| Resource | Paper | What It Evaluates |
| --- | --- | --- |
| **LIBERO** | [[2306.03310]] | Lifelong robot learning (5 suites, 130 tasks) |
| **CALVIN** | [[2112.03227]] | Long-horizon language-conditioned manipulation |
| **RLBench** | [[1909.12271]] | 100 robot learning tasks with demonstrations |
| **OXE** | [[2310.08864]] | Cross-embodiment dataset (22 robot types) |
| **RH20T** | [[2307.00595]] | Diverse one-shot robot skills |
| **SIMPLER** | [[2405.05941]] | Real-world policy evaluation in simulation |
| **AgiBot World** | [[2503.06669]] | Large-scale manipulation platform |
| **RoboMIND** | [[2412.13877]] | Multi-embodiment normative benchmark |

### Spatial & 3D Reasoning
| Resource | Paper | What It Evaluates |
| --- | --- | --- |
| **VSR** | [[2205.00363]] | Visual spatial reasoning (true/false) |
| **SpatialVLM** | [[2401.12168]] | 3D spatial reasoning in VLMs |
| **MultihopSpatial** | [[2603.18892]] | Multi-hop compositional spatial reasoning |
| **VIEW2SPACE** | [[2603.16506]] | Sparse multi-view spatial reasoning |
| **TopViewRS** | [[2406.02537]] | Top-view spatial reasoning |

### Video Understanding
| Resource | Paper | What It Evaluates |
| --- | --- | --- |
| **MMOU** | [[2603.14145]] | Joint audio-visual reasoning (15K questions) |
| **STI-Bench** | [[2503.23765]] | Spatio-temporal world understanding |

### Reasoning
| Resource | Paper | What It Evaluates |
| --- | --- | --- |
| **CogEval** | [[2309.15129]] | Cognitive maps and planning in LLMs |
| **VisuLogic** | [[2504.15279]] | Visual logic reasoning in MLLMs |
| **REASONING GYM** | [[2505.24760]] | RL environments with verifiable rewards |

---

## Cross-References

- [[01_Foundation-Models]] — Transformer architecture surveys
- [[02_Vision-Language-Models]] — VLM and open-vocabulary surveys
- [[04_Reinforcement-Learning]] — RL surveys and benchmarks
- [[07_Robotics-and-Embodied-AI]] — Robotics datasets and benchmarks

---

*This note serves as a quick-reference index. For topic-specific context, see the individual General/ overview files.*

---

## Complete Paper Listing

### Benchmarks (9)

| Paper | Year | Summary |
| --- | --- | --- |
| [[2409.14401\|In-Class Data Imbalance]] | 2024 | Pukowski and Lu introduce the concept of "in-class data imbalance," revealing that datasets contain disproportionate ... |
| [[2410.13842\|D-FINE]] | 2024 | D-FINE redefines bounding box regression in DETR models by transforming fixed coordinate predictions into a fine-grai... |
| [[2410.20722\|ProtoViT]] | 2024 | ProtoViT, developed by researchers from Dartmouth College, Duke University, and the University of Maine, integrates V... |
| [[2505.01109\|SSL-MIL Pathology Benchmark]] | 2025 | A comprehensive benchmark study reveals that simple instance-based Multiple Instance Learning (MIL) methods combined ... |
| [[2505.13840\|EfficientLLM]] | 2025 | A comprehensive empirical evaluation framework assesses efficiency techniques for Large Language Models across archit... |
| [[2512.06104\|CompressARC]] | 2025 | CompressARC, developed by researchers at Carnegie Mellon University, addresses the ARC-AGI benchmark by achieving 20%... |
| [[2512.14693\|URM]] | 2025 | The Universal Reasoning Model (URM), developed by Ubiquant, systematically analyzes Universal Transformers to identif... |
| [[2602.11217\|Magic Correlations]] | 2026 | Researchers at Google DeepMind and EPFL systematically analyzed how accuracy and confidence transfer from pretraining... |
| [[2603.01097\|LoRA Knowledge Memory]] | 2026 | Researchers from KAIST, Samsung SDS, and NYU systematically audited Low-Rank Adaptation (LoRA) as a parametric knowle... |

### Datasets (4)

| Paper | Year | Summary |
| --- | --- | --- |
| [[2406.09294\|DINOv2]] | 2024 | Researchers at FAIR at Meta demonstrated that joint-embedding self-supervised learning models like DINOv2 can achieve... |
| [[2407.11464\|Crowd-SAM]] | 2024 | Crowd-SAM introduces a framework that adapts the Segment Anything Model (SAM) and DINOv2 to serve as a smart annotato... |
| [[2412.00420\|TAROT]] | 2024 | TAROT introduces a targeted data selection framework that leverages Whitened Feature Distance (WFD) and Optimal Trans... |
| [[2504.13161\|Nemotron-CLIMB]] | 2025 | Nemotron-CLIMB, developed by NVIDIA and Georgia Institute of Technology, introduces an automated framework for discov... |

### Evaluation (2)

| Paper | Year | Summary |
| --- | --- | --- |
| [[2602.15029\|Language Symmetry Representations]] | 2026 | A theoretical framework demonstrates that translation symmetry in pairwise word co-occurrence statistics determines t... |
| [[2603.02188\|MLRA]] | 2026 | Multi-Head Low-Rank Attention (MLRA) enhances large language model inference efficiency and scalability for long cont... |

### Surveys (14)

| Paper | Year | Summary |
| --- | --- | --- |
| [[2009.06732\|Efficient Transformers Survey]] | 2020 | A survey from Google Research systematically categorizes the diverse landscape of efficient Transformer models, prese... |
| [[2302.01107\|Efficient Transformer Training Survey]] | 2023 | Researchers systematically categorize techniques for efficient Transformer training, offering the first comprehensive... |
| [[2312.12148\|PEFT Survey]] | 2023 | This paper provides a comprehensive review and assessment of Parameter-Efficient Fine-Tuning (PEFT) methods for pretr... |
| [[2408.13296\|LLM Fine-Tuning Guide]] | 2024 | This report from CeADAR: Ireland’s Centre for AI, located at University College Dublin, offers an exhaustive review o... |
| [[2501.09223\|LLM Foundations]] | 2025 | Tong Xiao and Jingbo Zhu from Northeastern University and NiuTrans Research offer a foundational guide to Large Langu... |
| [[2501.13787\|PEFT Survey]] | 2025 | Tsinghua University researchers present the first comprehensive analysis of Parameter-Efficient Fine-Tuning (PEFT) me... |
| [[2504.07213\|E-SSL Survey]] | 2025 | This survey paper systematically reviews the growing body of literature combining Evolutionary Machine Learning (EML)... |
| [[2504.14117\|PEFT A2Z]] | 2025 | This survey provides a structured overview of Parameter-Efficient Fine-Tuning (PEFT) techniques, examining their mech... |
| [[2505.03113\|Lightweight ViT Survey]] | 2025 | This survey systematically reviews online lightweighting techniques for Vision Transformers, categorizing methods lik... |
| [[2506.20134\|3D World Models Survey]] | 2025 | This survey provides a structured and forward-looking review of general world models, emphasizing their transition fr... |
| [[2507.13334\|Context Engineering Survey]] | 2025 | Mei et al. formalize "Context Engineering" as a systematic discipline for optimizing information supplied to Large La... |
| [[2508.09834\|Efficient LLM Architectures Survey]] | 2025 | This survey provides a systematic, unified taxonomy of efficient architectural designs and optimization strategies fo... |
| [[2510.26493\|Context Engineering 2.0]] | 2025 | Researchers from Shanghai Jiao Tong University and Shanghai Artificial Intelligence Laboratory redefine context engin... |
| [[2512.13564\|AI Agent Memory Survey]] | 2025 | This survey provides a comprehensive analysis of memory systems in AI agents, introducing a novel "Forms–Functions–Dy... |
