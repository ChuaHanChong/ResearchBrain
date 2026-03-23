---
title: Datasets, Benchmarks & Environments for Embodied AI
tags:
  - dataset
  - benchmark
  - embodied-AI
  - robotics
---

%%
PROMPT:
Based on @_KnowledgeHub_, briefly explain the key ideas of the papers related to datasets and benchmarks/environments for embodied AI. For each dataset or benchmark, you may group the papers if they share similar goals.

You may only refer to the papers in the list below and should not refer to any other papers.

Datasets (9 papers)
- https://arxiv.org/abs/2601.11421  # GM100
- https://arxiv.org/abs/2512.24653  # RoboMIND 2.0
- https://arxiv.org/abs/2511.17441  # RoboCOIN
- https://arxiv.org/abs/2509.00576  # Galaxea
- https://arxiv.org/abs/2503.06669  # AgiBot World
- https://arxiv.org/abs/2412.13877  # RoboMIND
- https://arxiv.org/abs/2403.12945  # DROID
- https://arxiv.org/abs/2310.08864  # Open X-Embodiment
- https://arxiv.org/abs/2307.00595  # RH20T

Benchmark / Environment (9 papers)
- https://arxiv.org/abs/2510.13626  # LIBERO-Plus
- https://arxiv.org/abs/2506.18088  # RoboTwin 2.0
- https://arxiv.org/abs/2406.02523  # RoboCasa
- https://arxiv.org/abs/2405.05941  # SimplerEnv
- https://arxiv.org/abs/2306.03310  # LIBERO
- https://arxiv.org/abs/2305.12821  # FurnitureBench
- https://arxiv.org/abs/2112.03227  # CALVIN
- https://arxiv.org/abs/2003.08515  # SAPIEN
- https://arxiv.org/abs/1909.12271  # RLBench
%%

# Datasets, Benchmarks & Environments

> [!abstract] Overview
> Two parallel efforts underpin progress in embodied AI: **datasets** that provide diverse real-world demonstrations for training, and **benchmarks/environments** that provide standardized evaluation grounds. The field has evolved from small, single-robot setups to million-trajectory cross-embodiment corpora and from single-task sim environments to household-scale simulators with language conditioning.

---

## Datasets

### Group 1 — Cross-Embodiment Scale Datasets

The biggest unlock in robot learning is training across many robot types simultaneously. These datasets pursue that goal at scale.

**⭐ [[2310.08864|Open X-Embodiment]]** (2310) is the landmark effort: 1M+ real-robot trajectories from 22 embodiments, contributed by institutions worldwide. Training RT-X models on OXE demonstrated positive transfer and emergent skills across robot platforms — the ImageNet moment for robotics.

**⭐ [[2403.12945|DROID]]** (2403) pushes diversity further by collecting "in-the-wild" data across 16 institutions, covering an unprecedented range of scenes, tasks, and objects. Policies co-trained on DROID show an average **20% improvement** in success rate and better robustness to distribution shift compared to smaller datasets.

**[[2503.06669|AgiBot World]]** (2503) ⭐ scales to **1 million real-world trajectories** spanning diverse tasks and environments, and pairs the dataset with GO-1, a generalist policy using latent action representations. It delivers a 32% average improvement over baselines, positioning it as the largest single-lab effort to date.

### Group 2 — Multi-Modal & Multi-Embodiment Specialist Datasets

These datasets prioritize richer sensing or specific manipulation challenges.

**[[2412.13877|RoboMIND]]** (2412) provides a unified multi-embodiment dataset collected under consistent standards across four robot types including a humanoid — enabling fair cross-embodiment comparison. **[[2512.24653|RoboMIND 2.0]]** (2512) extends this to 310K bimanual and mobile manipulation trajectories with tactile sensing and a high-fidelity digital twin, accompanied by the MIND-2 dual-system policy framework.

**[[2511.17441|RoboCOIN]]** (2511) focuses on **bimanual manipulation** specifically: 180K+ demonstrations across diverse platforms with hierarchical annotations and a data quality framework (CoRobot), leading to improved VLA performance on complex two-arm tasks.

**[[2509.00576|Galaxea]]** (2509) takes a different angle — a 500-hour dataset collected in diverse real-world environments with a *single consistent embodiment*, demonstrating that single-embodiment, in-domain data quality can outperform heterogeneous scale.

**[[2307.00595|RH20T]]** (2307) provides 110K+ multi-modal sequences across 147 tasks collected at SJTU, enabling improved few-shot learning and task generalization.

### Group 3 — Evaluation-Oriented Dataset

**[[2601.11421|GM-100]]** (2601) is less a training dataset and more a **diagnostic tool**: 100 carefully designed, detail-oriented tasks that expose failure modes of current VLA models. Existing models achieve very low success rates on GM-100, making it a useful stress test for measuring real capability gaps rather than benchmark saturation.

---

## Benchmarks & Environments

### Group 1 — Simulation Environments (Infrastructure)

These provide the physical simulation substrate on which many downstream benchmarks are built.

**⭐ [[2003.08515|SAPIEN]]** (2003) is the foundational part-based interactive environment — physically accurate simulation with a large articulated object collection and photorealistic rendering. It is the simulation backbone for many subsequent benchmarks.

**⭐ [[1909.12271|RLBench]]** (1909) from Dyson Robotics Lab provides 100 visually-guided manipulation tasks with infinite expert demonstrations via motion planning. It standardized the research interface for few-shot and imitation learning in robotic manipulation and remains a widely-used baseline environment.

### Group 2 — Language-Conditioned Long-Horizon Benchmarks

These benchmarks evaluate the harder problem of following language instructions over extended task horizons.

**⭐ [[2112.03227|CALVIN]]** (2112) is the standard for long-horizon, language-conditioned policy evaluation in simulation. Tasks require chaining multiple sub-goals using continuous control, with multimodal sensing and diverse natural language instructions. It is the most cited benchmark for measuring compositional generalization.

**⭐ [[2306.03310|LIBERO]]** (2306) extends the paradigm to *lifelong learning* — procedurally generated tasks designed to evaluate knowledge transfer of both declarative (what) and procedural (how) skills across task sequences. Its findings highlight that policy architecture matters more than algorithm for knowledge retention.

**[[2305.12821|FurnitureBench]]** (2305) tests real-world long-horizon manipulation through furniture assembly with 3D-printable standardized props and a teleoperated dataset. Notably, current state-of-the-art algorithms fail to complete any full assembly task — making it a hard-open challenge.

### Group 3 — Household-Scale Simulation

**⭐ [[2406.02523|RoboCasa]]** (2406) targets everyday household tasks at scale: diverse kitchen environments, a large object repository, and 100 benchmark tasks. Crucially, it shows that scaling synthetic training data significantly improves generalist policy performance, making it a data-generation platform as much as a benchmark.

**⭐ [[2506.18088|RoboTwin 2.0]]** (2506) focuses on **bimanual manipulation** with strong domain randomization. Its synthetic data pipeline produces a **24.4% improvement** in real-world few-shot success rates, demonstrating that high-quality sim-to-real transfer is achievable with sufficient randomization.

### Group 4 — Robustness & Sim-to-Real Evaluation

**[[2510.13626|LIBERO-Plus]]** (2510) is a diagnostic layer on top of LIBERO that systematically tests VLA robustness across **seven perturbation dimensions**. Its key finding: VLA models are brittle despite high scores on standard benchmarks — strong performance on LIBERO does not guarantee real-world robustness.

**⭐ [[2405.05941|SimplerEnv]]** (2405) addresses the sim-to-real evaluation gap directly: a framework for evaluating real-world robot policies *in simulation* by carefully matching control and visual properties. It shows strong correlation with real-world performance, enabling cheap and reproducible policy evaluation without hardware.

---

## Physics Engines

Physics engines are the invisible substrate beneath every simulation benchmark. The choice of engine affects contact accuracy, sim-to-real transfer quality, and computational cost.

| Engine | Strengths | Typical Use |
| --- | --- | --- |
| **⭐ [PhysX](https://developer.nvidia.com/physx-sdk)** | GPU-accelerated rigid body and deformable simulation, tight NVIDIA ecosystem integration | SAPIEN, Isaac Gym/Lab, large-scale parallel RL training |
| **⭐ [MuJoCo](https://mujoco.org)** | Fast, accurate contact and tendon dynamics, low overhead, excellent for continuous control | Standard RL benchmarks, OpenAI Gym, Deepmind Control Suite |
| **⭐ [PyBullet](https://pybullet.org/wordpress/)** | Open-source, easy Python interface, good for prototyping and academic use | RLBench, early robot learning pipelines |

> [!note] Why It Matters
> Sim-to-real transfer quality is heavily dependent on physics engine fidelity. **PhysX** dominates GPU-parallel training pipelines due to massive throughput. **MuJoCo** is the gold standard for contact-rich manipulation accuracy and is used in most rigorous RL benchmarks. **PyBullet** enabled rapid prototyping in the community but is increasingly replaced by MuJoCo or PhysX for production-quality research.
