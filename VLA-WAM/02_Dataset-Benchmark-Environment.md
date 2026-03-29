---
title: "Datasets, Benchmarks & Environments — Deep Dive"
tags:
  - benchmark
  - robotics
  - embodied-AI
  - manipulation
  - VLA
aliases:
  - Robotics Benchmarks
  - Embodied AI Datasets
---

# Datasets, Benchmarks & Environments

> [!abstract] Overview
> The data and evaluation infrastructure that enables all embodied AI research. Datasets provide training signal, benchmarks measure progress, and simulators enable safe experimentation. The field evolved from small single-robot setups (RLBench, 2019) through million-trajectory cross-embodiment corpora (OXE, 2023) to household-scale simulation and diagnostic robustness evaluation (LIBERO-Plus, 2025). This note maps the full landscape: training datasets, simulation platforms, diagnostic benchmarks, spatial reasoning evaluations, and world model benchmarks.

---

## 1. Cross-Embodiment Scale Datasets

The biggest unlock in robot learning: training across many robot types simultaneously. Scale and diversity matter more than curation.

- [[2503.06669|AgiBot World]], [[2403.12945|DROID]], [[2310.08864|OXE]], [[2307.00595|RH20T]]

> [!star] Key Papers
> - [[2310.08864|OXE]] — 1M+ real-robot trajectories from 22 embodiments; the ImageNet moment for robotics
> - [[2403.12945|DROID]] — In-the-wild data across 16 institutions; 20% success rate improvement; proved diverse data beats curated data
> - [[2503.06669|AgiBot World]] — 1M trajectories + GO-1 generalist policy; 32% improvement over baselines; largest single-lab effort

> [!tip] Data Scale vs Quality
> OXE proved cross-embodiment transfer works. DROID proved diversity beats curation. AgiBot World proved a single lab can match collaborative scale. The pattern: more robots, more scenes, more tasks → better generalization.

---

## 2. Multi-Modal & Specialist Datasets

Rich sensing (tactile, force, dual-arm) or specific manipulation challenges. For when scale alone isn't enough.

**Bimanual Manipulation** — Coordinated two-arm control requires specialized data.
- [[2512.24653|RoboMIND 2.0]], [[2511.17441|RoboCOIN]], [[2412.13877|RoboMIND]]

**Single-Embodiment High-Quality** — Depth over breadth: consistent data from one robot in diverse environments.
- [[2509.00576|G0]]

**Egocentric & Motion Capture** — Human-perspective video and motion data for cross-embodiment skill transfer.
- [SEED (Bones Studio)](https://huggingface.co/datasets/bones-studio/seed) — High-quality motion capture and manipulation dataset for dexterous skill learning
- [EgoVerse (Georgia Tech)](https://github.com/gatech-rl2/egoverse) — Egocentric video dataset capturing first-person human activities for robot skill transfer

**Teleoperation Hardware** — The data collection systems themselves.
- [[2309.13037|GELLO]], [[2304.13705|ALOHA]]

> [!star] Key Papers
> - [[2512.24653|RoboMIND 2.0]] — 310K bimanual + mobile manipulation trajectories with tactile sensing and digital twin
> - [[2304.13705|ALOHA]] — Low-cost bimanual teleoperation; enabled fine-grained data collection for dexterous tasks

> [!tip] When Scale Doesn't Help
> [[2509.00576|G0]] showed single-embodiment in-domain data quality can outperform heterogeneous cross-embodiment scale. If your deployment robot is fixed, invest in diverse *scenes* not diverse *robots*.

---

## 3. Diagnostic & Evaluation Datasets

Not for training — for exposing failure modes and measuring real capability.

- [[2601.11421|GM-100]], [[2507.10548|EmbRACE-3K]], [[2507.05258|REA]], [[2508.13142|EASI]]

> [!star] Key Papers
> - [[2601.11421|GM-100]] — 100 detail-oriented tasks; current VLAs achieve very low success rates, exposing real capability gaps
> - [[2508.13142|EASI]] — Holistic evaluation framework for spatial intelligence in embodied agents

---

## 4. Simulation Environments

The physical simulation substrate on which benchmarks are built. Choice of environment determines what you can test.

**Foundation Simulators** — General-purpose physics platforms for robot learning.
- [[2003.08515|SAPIEN]], [[1909.12271|RLBench]], [Genesis](https://genesis-world.readthedocs.io/en/latest/), [Newton (NVIDIA)](https://developer.nvidia.com/newton-physics)

**Household-Scale** — Realistic home environments with diverse objects and tasks.
- [[2406.02523|RoboCasa]]

**Teleoperation-Friendly** — Environments designed for collecting human demonstrations.
- [[2310.06114|UniSim]]

> [!star] Key Papers
> - [[2003.08515|SAPIEN]] — 2,346 articulated objects with physics-accurate simulation; foundational platform for manipulation research
> - [[1909.12271|RLBench]] — 100 tasks with infinite expert demos via motion planning; standardized few-shot and imitation learning evaluation
> - [[2406.02523|RoboCasa]] — Scaling synthetic data significantly improves generalist policy performance; data-generation platform + benchmark

### Physics Engines

| Engine | Strengths | Typical Use |
|--------|-----------|-------------|
| **PhysX** | GPU-accelerated rigid body + deformable simulation, NVIDIA ecosystem | SAPIEN, Isaac Gym/Lab, large-scale parallel RL |
| **MuJoCo** | Fast, accurate contact/tendon dynamics, low overhead | Standard RL benchmarks, OpenAI Gym, DeepMind Control |
| **PyBullet** | Open-source, easy Python API, good for prototyping | RLBench, early robot learning pipelines |

> [!tip] Sim Engine Choice
> PhysX dominates GPU-parallel training (throughput). MuJoCo is gold standard for contact-rich manipulation accuracy. PyBullet enabled rapid prototyping but is increasingly replaced. For production: PhysX if GPU-parallel, MuJoCo if contact accuracy matters.

---

## 5. Language-Conditioned Long-Horizon Benchmarks

Testing the harder problem: following language instructions over extended task horizons with compositional generalization.

- [[2510.13626|LIBERO-Plus]], [[2506.18088|RoboTwin 2.0]], [[2306.03310|LIBERO]], [[2305.12821|FurnitureBench]], [[2112.03227|CALVIN]], [[2505.15660|AGNOSTOS]]

> [!star] Key Papers
> - [[2306.03310|LIBERO]] — Lifelong robot learning benchmark; tests continual learning and long-horizon capability
> - [[2112.03227|CALVIN]] — Standard for long-horizon, language-conditioned policy evaluation; most-cited compositionality benchmark
> - [[2510.13626|LIBERO-Plus]] — Diagnostic layer: VLAs are brittle despite high LIBERO scores; 7 perturbation dimensions expose real-world gaps

> [!tip] Don't Trust Standard Benchmarks Alone
> LIBERO-Plus revealed that models scoring >90% on LIBERO fail badly under visual perturbations. Always pair standard benchmarks (LIBERO, CALVIN) with diagnostic ones (LIBERO-Plus, GM-100) to measure true robustness.

---

## 6. Sim-to-Real Transfer Evaluation

Bridging the reality gap: does simulation performance predict real-world success?

- [[2405.05941|SimplerEnv]], [[2602.20687|NativeEmbodied]], [[2602.21992|PanoEnv]]

> [!star] Key Papers
> - [[2405.05941|SimplerEnv]] — Strong correlation between sim and real performance; enables cheap, reproducible policy evaluation without hardware

---

## 7. Spatial Reasoning & 3D Benchmarks

Evaluating whether robots (and their VLM backbones) actually understand 3D space, object relationships, and spatial reasoning.

- [[2602.20901|SpatiaLQA]], [[2601.09430|Video-MSR]], [[2601.15224|PROGRESSLM]], [[2505.05456|SITE]], [[2503.23765|STI-Bench]], [[2507.18342|EgoExoBench]], [[2603.18892|MultihopSpatial]], [[2603.19231|MonoArt]], [[2511.04670|Cambrian-S]], [[2410.06468|SPACE]]

> [!star] Key Papers
> - [[2505.05456|SITE]] — Comprehensive spatial intelligence evaluation across multiple reasoning types
> - [[2410.06468|SPACE]] — Systematic evaluation of spatial cognition in VLMs; reveals gap between VLM and human spatial reasoning
> - [[2601.09430|Video-MSR]] — Multi-step spatial reasoning benchmark for video understanding

> [!tip] The Spatial Gap
> Current VLMs and VLAs consistently underperform on spatial reasoning benchmarks compared to object recognition tasks. SPACE and SITE show this is a fundamental representation issue, not just a data issue. Papers like SpatialVLA and 4D-VLA attempt to close this gap architecturally.

---

## 8. World Model Benchmarks

Evaluating whether learned world models generate physically plausible, action-consistent, long-horizon predictions.

- [[2603.23497|WildWorld]], [[2603.22212|Omni-WorldBench]], [[2603.22078|WAM vs VLA Robustness]], [[2603.09030|PlayWorld]], [[2602.05986|RISE-Video]]

> [!star] Key Papers
> - [[2603.22212|Omni-WorldBench]] — First interaction-centric evaluation for world models; tests causal consistency and action following
> - [[2603.22078|WAM vs VLA Robustness]] — Systematic comparison: WAMs are more robust to visual perturbations but 4.8x slower
> - [[2603.23497|WildWorld]] — 108M frames from Monster Hunter: Wilds with explicit state annotations; Action Following and State Alignment metrics

> [!tip] Beyond Visual Quality
> Early world model evals focused on video quality (FID, FVD). 2026 benchmarks (Omni-WorldBench, WildWorld) shifted to *interaction fidelity*: does the model follow actions? Are state transitions consistent? This is what matters for robot control.

---

## 9. VLA Architecture & Design Studies

Systematic studies that benchmark VLA design decisions rather than individual models.

- [[2412.14058|RoboVLMs]], [[2601.18692|LingBot-VLA]], [[2503.14734|GR00T N1]], [[2512.14666|EVOLVE-VLA]]

> [!star] Key Papers
> - [[2412.14058|RoboVLMs]] — 600+ experiments systematically testing backbone, action space, history fusion, and data strategy choices

> [!tip] The RoboVLMs Recipe
> The most rigorous VLA design study: KosMos/PaliGemma backbone + Policy Head fusion + Continuous actions + MoE + Post-training. See [[03_VLA#1. Design-Space Principles]] for the full breakdown.

---

## 10. Benchmark Hierarchy

Use this progression to evaluate robot policies at increasing levels of rigor:

| Level | Benchmark | What It Tests | When to Use |
|-------|-----------|--------------|-------------|
| 1. Basic | LIBERO, CALVIN | In-distribution task success | Early development |
| 2. Scale | SimplerEnv | Sim-to-real correlation | Before real-world deployment |
| 3. Robustness | LIBERO-Plus, GM-100 | Perturbation robustness | Before claiming generalization |
| 4. Spatial | SITE, SPACE, SpatiaLQA | 3D reasoning capability | For spatial tasks |
| 5. World Model | Omni-WorldBench, WildWorld | Dynamics prediction fidelity | For WAM-based policies |

> [!success] The Evaluation Stack
> ==LIBERO== (can the policy do the task?) → ==SimplerEnv== (does sim predict real?) → ==LIBERO-Plus== (is it robust?) → ==GM-100== (does it handle detail?) → ==Omni-WorldBench== (does the world model work?)

---

## Cross-References

- [[03_VLA]] — VLA deep-dive (Section 2 uses RoboVLMs findings)
- [[04_WAM]] — WAM deep-dive (Section 8 covers failure modes found by benchmarks)
- [[01_VLA-WAM-101]] — VLA vs WAM basics

---

*See [[03_VLA]] for VLA design principles informed by these benchmarks, or [[04_WAM]] for world model evaluation.*
