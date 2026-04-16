---
title: "Research Topics — Index"
tags:
  - index
aliases:
  - General Index
  - Topic Map
---

## Research Topics — Index

> [!abstract]
> Complete overview of all 2,190 papers in [[_KnowledgeHub_]], organized into 12 topic areas. Each topic file has curated narrative sections with evolution graphs, grouped sub-topics, key paper highlights, and practical insights.

### Topic Map

```mermaid
graph LR
    A["1. Foundation Models"] --> B["2. VLMs"]
    A --> C["4. RL"]
    B --> D["3. Reasoning"]
    A --> E["5. CV & 3D"]
    E --> F["6. Video"]
    B --> G["7. Robotics"]
    C --> G
    D --> G
    F --> G
    B --> H["9. Multimodal LLMs"]
    D --> I["10. Agents"]
    C --> J["11. Self-Evolving"]
    A --> K["12. Diffusion"]
    K --> F
    J --> G

    style A fill:#e8f4fd,stroke:#4a90d9
    style G fill:#e8fde8,stroke:#27ae60
    style J fill:#f0e8fd,stroke:#9b59b6
```

### Files

| # | Topic | Key Threads | Papers |
| --- | --- | --- | --- |
| [[01_Foundation-Models]] | ViT, SSL, CLIP, PEFT, theory | ViT → DINO → DINOv2 → I-JEPA | 473 |
| [[02_Vision-Language-Models]] | Grounding, alignment, hallucination, spatial | CLIP → GLIP → Grounding DINO → LISA | 597 |
| [[03_Reasoning-and-Planning]] | CoT, agentic reasoning, visual reasoning, TTS | CoT → STaR → ReAct → R1-style RL | 950 |
| [[04_Reinforcement-Learning]] | Model-based RL, RLHF, GRPO, agentic RL | Dreamer → DreamerV3; STaR → GRPO → Absolute Zero | 730 |
| [[05_Computer-Vision-and-3D]] | Detection, segmentation, 3D, spatial reasoning | FPN → Grounding DINO; DINO → RieMind | 386 |
| [[06_Video-and-Temporal]] | Video SSL, generation as world models, motion | V-JEPA → V-JEPA 2.1; UniPi → UniSim → WAMs | 114 |
| [[07_Robotics-and-Embodied-AI]] | VLAs, WAMs, self-evolving, driving, datasets | RT-1 → RT-2 → OpenVLA → π0 → DreamZero → SPIRAL | 511 |
| [[08_Benchmarks-and-Surveys]] | Cross-cutting surveys and evaluation resources | LIBERO, CALVIN, OXE, MMOU, MultihopSpatial | 539 |
| [[09_Multimodal-LLMs]] | MLLMs, instruction tuning, omni-modal | InstructBLIP → KOSMOS-2 → PaliGemma → Magma | 799 |
| [[10_Agents-and-Tool-Use]] | LLM agents, tool use, multi-agent, code gen | ReAct → LATS → AgentGym → KARL → Memento-Skills | 219 |
| [[11_Self-Evolving-AI]] | Self-training, bootstrapping, curriculum, meta | STaR → Self-Rewarding → Absolute Zero → SPIRAL | 137 |
| [[12_Diffusion-and-Generation]] | Diffusion, flow matching, image/text generation | Diffuser → Diffusion Policy → Transfusion → Flow-GRPO | 214 |

**Total: 2,190 papers** — papers may appear in multiple topic files where relevant.

### Deep-Dive Folders

- `VLA-WAM/` — VLA vs WAM comparison, design principles, WAM survey, JEPA evolution
- `_Projects_/01_FirstPublication/` — Self-evolving WAM blueprint and RL vs CL analysis
