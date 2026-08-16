---
title: "Research Topics — Index"
tags:
  - index
aliases:
  - "General Index"
  - "Topic Map"
---

## Research Topics — Index

> [!abstract]
> Complete overview of all 8,999 papers in [[_KnowledgeHub_]], organized into 12 topic areas. Each topic file has curated narrative sections with evolution graphs, grouped sub-topics, key paper highlights, and practical insights.

### Topic Map

```text
╔═════════════════════════╗
║  1. Foundation Models   ║──────► 2. CV & 3D
║                         ║──────► 3. Diffusion
║                         ║──────► 5. VLMs
║                         ║──────► 8. RL
╚═════════════════════════╝

┌──────────────┐
│  2. CV & 3D  │──────► 4. Video
└──────────────┘

┌──────────────────┐
│  3. Diffusion    │──────► 4. Video
└──────────────────┘

┌──────────────┐
│  4. Video    │──────► 11. Robotics
└──────────────┘

┌──────────────┐
│  5. VLMs     │──────► 6. Multimodal LLMs
│              │──────► 7. Reasoning
│              │┄┄┄┄┄┄► 11. Robotics   (skip-layer)
└──────────────┘

┌───────────────────────┐
│  6. Multimodal LLMs   │  (sink — no outgoing edges)
└───────────────────────┘

┌──────────────────┐
│  7. Reasoning    │──────► 10. Agents
│                  │──────► 11. Robotics
└──────────────────┘

┌──────────────┐
│  8. RL       │──────► 9. Self-Evolving
│              │┄┄┄┄┄┄► 11. Robotics   (skip-layer)
└──────────────┘

╔══════════════════════╗
║  9. Self-Evolving    ║──────► 11. Robotics
╚══════════════════════╝

┌──────────────┐
│  10. Agents  │  (sink — no outgoing edges)
└──────────────┘

╔══════════════════╗
║  11. Robotics    ║  (sink — no outgoing edges)
╚══════════════════╝

┌───────────────────────┐
│  12. Benchmarks       │  (cross-cutting capstone; evaluates topics 1-11, no dependency edges)
└───────────────────────┘

Legend:
  ╔═╗ double border = notable/highlighted node (Foundation Models, Robotics, Self-Evolving).
  ──────► = direct edge to the adjacent layer.  ┄┄┄┄┄┄► = edge that skips a layer (e.g. VLMs/RL straight to Robotics).
  File numbers now follow this dependency order: each topic is numbered after everything it depends on.
```

### Files

| # | Topic | Key Threads | Papers |
| --- | --- | --- | --- |
| [[01_Foundation-Models]] | ViT, SSL, CLIP, PEFT, theory | ViT → DINO → DINOv2 → I-JEPA | 1175 |
| [[02_Computer-Vision-and-3D]] | Detection, segmentation, 3D, spatial reasoning | FPN → Grounding DINO; DINO → RieMind | 1108 |
| [[03_Diffusion-and-Generation]] | Diffusion, flow matching, image/text, physics-aware | Diffuser → Diffusion Policy → Transfusion → Flow-GRPO → PhysGaussian → NewtonRewards → OmniPhysGS | 1051 |
| [[04_Video-and-Temporal]] | Video SSL, generation as world models, physics, motion | V-JEPA → V-JEPA 2.1; UniPi → UniSim → WAMs; Force Prompting → Cosmos → NewtonGen | 584 |
| [[05_Vision-Language-Models]] | Grounding, alignment, hallucination, spatial | CLIP → GLIP → Grounding DINO → LISA | 1162 |
| [[06_Multimodal-LLMs]] | MLLMs, instruction tuning, omni-modal | InstructBLIP → KOSMOS-2 → PaliGemma → Magma | 1157 |
| [[07_Reasoning-and-Planning]] | CoT, agentic reasoning, visual reasoning, TTS | CoT → STaR → ReAct → R1-style RL | 1403 |
| [[08_Reinforcement-Learning]] | Model-based RL, RLHF, GRPO, agentic RL | Dreamer → DreamerV3; STaR → GRPO → Absolute Zero | 2634 |
| [[09_Self-Evolving-AI]] | Self-training, bootstrapping, curriculum, meta | STaR → Self-Rewarding → Absolute Zero → SPIRAL | 386 |
| [[10_Agents-and-Tool-Use]] | LLM agents, tool use, multi-agent, code gen | ReAct → LATS → AgentGym → KARL → Memento-Skills | 501 |
| [[11_Robotics-and-Embodied-AI]] | VLAs, WAMs, self-evolving, driving, datasets | RT-1 → RT-2 → OpenVLA → π0 → DreamZero → SPIRAL | 5980 |
| [[12_Benchmarks-and-Surveys]] | Cross-cutting surveys and evaluation resources | LIBERO, CALVIN, OXE, Physion → VideoPhy → PhyGenBench → FysicsWorld | 1483 |

**Total: 8,999 papers** — papers may appear in multiple topic files where relevant.

See [[00_Table-of-Contents]] for a click-through section index of all 12 files.

### Deep-Dive Folders

- `Embodied-AI/` — VLA deep dive, WAM deep dive, latent world models (JEPA), self-evolving VLAs & WAMs
- `_Projects_/01_FirstPublication/` — Self-evolving WAM blueprint and RL vs CL analysis
