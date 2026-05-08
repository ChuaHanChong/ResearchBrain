---
title: "Datasets, Benchmarks & Environments — Deep Dive"
tags:
  - benchmark
  - robotics
  - embodied-AI
  - manipulation
  - VLA
aliases:
  - "Robotics Benchmarks"
  - "Embodied AI Datasets"
---

# Datasets, Benchmarks & Environments

> [!abstract] Overview
> The data and evaluation infrastructure that enables all embodied AI research. Datasets provide training signal, benchmarks measure progress, and simulators enable safe experimentation. The field evolved from small single-robot setups (RLBench, 2019) through million-trajectory cross-embodiment corpora (OXE, 2023) to household-scale simulation and diagnostic robustness evaluation (LIBERO-Plus, 2025). This note maps the full landscape: training datasets, simulation platforms, diagnostic benchmarks, spatial reasoning evaluations, and world model benchmarks.

---

## 1. Cross-Embodiment Scale Datasets

The biggest unlock in robot learning: training across many robot types simultaneously. Scale and diversity matter more than curation.

Cross-embodiment transfer works because diverse robot morphologies force the model to learn *task-invariant* representations — grasping a cup looks different on a Franka vs a UR5, but the semantic understanding of 'grasp the cup' is shared. OXE proved that training on 22 robot types simultaneously produces better policies than training on any single type, even for that specific robot. The mechanism: visual and language encoders learn to project morphology-specific observations into a shared task space. DROID extended this by showing that *environmental* diversity (16 institutions, different kitchens, labs, offices) matters as much as robot diversity.

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

Standard VLA datasets capture RGB images + actions — sufficient for simple pick-and-place but inadequate for contact-rich tasks (insertion, polishing, assembly) where force feedback determines success or failure. Bimanual datasets (RoboMIND 2.0) must capture coordinated dual-arm trajectories with synchronization — the timing between left and right arm matters as much as the positions. Egocentric datasets capture human-perspective video that maps more naturally to robot head-mounted cameras, reducing the viewpoint gap in cross-embodiment transfer.

**Bimanual Manipulation** — Coordinated two-arm control requires specialized data.
- [[2603.05687|CGP]], [[2512.24653|RoboMIND 2.0]], [[2511.17441|RoboCOIN]], [[2412.13877|RoboMIND]]

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

Diagnostic benchmarks differ from training benchmarks in a crucial way: they are designed to *expose specific failure modes*, not measure overall performance. GM-100's 100 detail-oriented tasks (precise insertion, fine alignment, tool manipulation) systematically test manipulation capabilities that standard benchmarks miss — current VLAs achieve very low success rates, revealing that 'grasping things' and 'precise manipulation' are fundamentally different capabilities. EmbRACE-3K evaluates embodied reasoning across 3,000 scenarios, testing whether models understand spatial relationships, physical causality, and task decomposition — not just whether they can pick up objects.

- [[2601.11421|GM-100]], [[2507.10548|EmbRACE-3K]], [[2507.05258|REA]], [[2508.13142|EASI]]

> [!star] Key Papers
> - [[2601.11421|GM-100]] — 100 detail-oriented tasks; current VLAs achieve very low success rates, exposing real capability gaps
> - [[2508.13142|EASI]] — Holistic evaluation framework for spatial intelligence in embodied agents

**Diagnostic Datasets by Failure Mode** — Each diagnostic benchmark probes a different VLA failure axis:

| Benchmark | Failure Axis | Primary Mode |
|-----------|-------------|--------------|
| [[2306.03310\|LIBERO]] | Standard manipulation | In-distribution skill |
| [[2510.13626\|LIBERO-Plus]] | Visual perturbations | 7-axis visual robustness |
| [[2603.28301\|LIBERO-Para]] | Instruction paraphrase | Language surface-form overfit |
| [[2601.11421\|GM-100]] | Fine manipulation | Detail-oriented precision |
| [[2507.10548\|EmbRACE-3K]] | Embodied reasoning | Spatial + causal reasoning |

> [!tip] Use the Diagnostic Stack
> Each benchmark stresses one failure axis. A model can score >90% on LIBERO yet collapse on LIBERO-Plus (visual), LIBERO-Para (language), or GM-100 (precision). Always evaluate across the full diagnostic stack before claiming generalization.

---

## 4. Simulation Environments

The physical simulation substrate on which benchmarks are built. Choice of environment determines what you can test.

**Foundation Simulators** — General-purpose physics platforms for robot learning.
- [[2604.08258|EvoGymCM]], [[2003.08515|SAPIEN]], [[1909.12271|RLBench]], [Genesis](https://genesis-world.readthedocs.io/en/latest/), [Newton (NVIDIA)](https://developer.nvidia.com/newton-physics)

**Household-Scale** — Realistic home environments with diverse objects and tasks.
- [[2406.02523|RoboCasa]]

**Teleoperation-Friendly** — Environments designed for collecting human demonstrations.
- [[2310.06114|UniSim]]

Simulator choice has profound implications for what you can test. SAPIEN provides 2,346 articulated objects with accurate joint mechanics — essential for tasks involving doors, drawers, and tools. RLBench offers 100 standardized tasks with infinite expert demonstrations via motion planning — making it the default for few-shot evaluation. RoboCasa generates photorealistic kitchen environments at scale — proving that synthetic data from realistic simulators can substitute for expensive real demonstrations. The emerging platform Genesis (GPU-accelerated, open-source) and NVIDIA Newton aim to combine PhysX's parallelism with MuJoCo's contact accuracy.

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

**The LIBERO Family — Testing Different Failure Modes**:

| Benchmark | What It Tests | Key Finding |
|-----------|--------------|-------------|
| [[2306.03310\|LIBERO]] | Standard manipulation (4 suites) | VLAs and WAMs both achieve ~97% — ceiling reached |
| [[2603.22078\|LIBERO-Plus]] | Visual perturbations (camera, lighting, background) | WAMs outperform VLAs by large margins; VLA-JEPA: 79.5% |
| [[2510.03827\|LIBERO-PRO]] | Minor perturbations on LIBERO tasks | VLAs collapse from >90% to near 0% under small changes |
| [[2602.06556\|LIBERO-X]] | Cross-task generalization | Only 39.4% at easiest level — massive unsolved gap |
| [[2603.28301\|LIBERO-Para]] | Paraphrased instructions | 22-52pp drops — models overfit to exact instruction phrasing |

> [!star] Key Papers
> - [[2306.03310|LIBERO]] — Lifelong robot learning benchmark; tests continual learning and long-horizon capability
> - [[2112.03227|CALVIN]] — Standard for long-horizon, language-conditioned policy evaluation; most-cited compositionality benchmark
> - [[2510.13626|LIBERO-Plus]] — Diagnostic layer: VLAs are brittle despite high LIBERO scores; 7 perturbation dimensions expose real-world gaps

> [!tip] Don't Trust Standard Benchmarks Alone
> LIBERO-Plus revealed that models scoring >90% on LIBERO fail badly under visual perturbations. Always pair standard benchmarks (LIBERO, CALVIN) with diagnostic ones (LIBERO-Plus, GM-100) to measure true robustness.

---

## 6. Sim-to-Real Transfer Evaluation

Bridging the reality gap: does simulation performance predict real-world success?

- [[2604.10856|BridgeSim]], [[2405.05941|SimplerEnv]], [[2602.20687|NativeEmbodied]], [[2602.21992|PanoEnv]]

The sim-to-real gap has two components: the *visual* gap (rendered vs real images) and the *dynamics* gap (simulated vs real physics). SimplerEnv addresses the visual gap by using high-fidelity rendering of real robot scenes — achieving strong correlation between sim and real performance. BridgeSim measures the dynamics gap specifically for autonomous driving, where tire friction, wind, and road surface vary unpredictably. The key finding: visual fidelity matters more than dynamics accuracy for manipulation (objects are rigid, contacts are brief), but dynamics accuracy matters more for locomotion and driving (continuous contact, long-horizon effects).

> [!star] Key Papers
> - [[2405.05941|SimplerEnv]] — Strong correlation between sim and real performance; enables cheap, reproducible policy evaluation without hardware

---

## 7. Spatial Reasoning & 3D Benchmarks

Evaluating whether robots (and their VLM backbones) actually understand 3D space, object relationships, and spatial reasoning.

- [[2602.20901|SpatiaLQA]], [[2601.09430|Video-MSR]], [[2601.15224|PROGRESSLM]], [[2505.05456|SITE]], [[2503.23765|STI-Bench]], [[2507.18342|EgoExoBench]], [[2603.18892|MultihopSpatial]], [[2603.19231|MonoArt]], [[2511.04670|Cambrian-S]], [[2410.06468|SPACE]]

Spatial reasoning evaluation tests whether models understand *where things are relative to each other* — not just what they are. SPACE probes five spatial capabilities: distance estimation, size comparison, containment (is X inside Y?), spatial relations (X is left of Y), and counting. Most frontier VLMs fail at basic spatial tasks that humans find trivial, exposing a fundamental gap between language understanding and physical understanding. MultihopSpatial extends this to multi-step spatial reasoning: 'the cup is on the table, the table is in the kitchen, where is the cup?' — requiring compositional spatial inference.

> [!star] Key Papers
> - [[2505.05456|SITE]] — Comprehensive spatial intelligence evaluation across multiple reasoning types
> - [[2410.06468|SPACE]] — Systematic evaluation of spatial cognition in VLMs; reveals gap between VLM and human spatial reasoning
> - [[2601.09430|Video-MSR]] — Multi-step spatial reasoning benchmark for video understanding

> [!tip] The Spatial Gap
> Current VLMs and VLAs consistently underperform on spatial reasoning benchmarks compared to object recognition tasks. SPACE and SITE show this is a fundamental representation issue, not just a data issue. Papers like SpatialVLA and 4D-VLA attempt to close this gap architecturally.

---

## 8. World Model Benchmarks

Evaluating whether learned world models generate physically plausible, action-consistent, long-horizon predictions.

- [[2604.11689|LARY]], [[2603.23497|WildWorld]], [[2603.22212|Omni-WorldBench]], [[2603.22078|WAM vs VLA Robustness]], [[2603.09030|PlayWorld]], [[2602.05986|RISE-Video]]

World model evaluation has shifted from passive video quality metrics (FVD, SSIM) to *interactive* benchmarks that test whether the model can predict consequences of actions. WR-Arena evaluates action-following fidelity: given an action, does the predicted next frame show the correct outcome? Causal consistency testing checks counterfactuals: if the action changes, does the predicted future change accordingly? OpenWorldLib provides a unified codebase for comparing world models across interactive video generation, 3D generation, and VLA tasks — standardizing evaluation that was previously fragmented across papers.

> [!star] Key Papers
> - [[2604.11689|LARY]] — Latent action representation yielding benchmark for generalizable vision-to-action alignment
> - [[2603.22212|Omni-WorldBench]] — First interaction-centric evaluation for world models; tests causal consistency and action following
> - [[2603.22078|WAM vs VLA Robustness]] — Systematic comparison: WAMs are more robust to visual perturbations but 4.8x slower
> - [[2603.23497|WildWorld]] — 108M frames from Monster Hunter: Wilds with explicit state annotations; Action Following and State Alignment metrics
> - [[2602.05986|RISE-Video]] — Probes whether video generators decode implicit world rules; rule-induction evaluation

> [!tip] Beyond Visual Quality
> Early world model evals focused on video quality (FID, FVD). 2026 benchmarks (Omni-WorldBench, WildWorld) shifted to *interaction fidelity*: does the model follow actions? Are state transitions consistent? This is what matters for robot control.

---

## 9. VLA Architecture & Design Studies

Systematic studies that benchmark VLA design decisions rather than individual models.

- [[2412.14058|RoboVLMs]], [[2601.18692|LingBot-VLA]], [[2503.14734|GR00T N1]], [[2512.14666|EVOLVE-VLA]]

RoboVLMs conducted the most systematic VLA design study to date: 600+ experiments varying backbone, fusion method, action space, training recipe, and data strategy. The key finding is that design choices *interact*: the best backbone depends on the fusion method, which depends on the action space. For example, PaliGemma excels with policy-head fusion but underperforms with cross-attention fusion. This interaction effect means you can't optimize each choice independently — the design space must be explored jointly.

> [!star] Key Papers
> - [[2412.14058|RoboVLMs]] — 600+ experiments systematically testing backbone, action space, history fusion, and data strategy choices — the largest published VLA design-space ablation to date
> - [[2503.14734|GR00T N1]] — Open foundation model + accompanying design study for generalist humanoid policies
> - [[2512.14666|EVOLVE-VLA]] — Evolutionary VLA improvement: progressive adaptation over many task iterations

> [!tip] The RoboVLMs Recipe
> The most rigorous VLA design study to date: 600+ experiments converging on KosMos/PaliGemma backbone + Policy Head fusion + Continuous actions + MoE + Post-training. See [[03_VLA#1. Design-Space Principles]] for the full breakdown.

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
- [[05_Latent-World-Models]] — Latent world models (JEPA benchmarks, latent vs pixel comparison)
- [[06_Self-Evolving-VLA-WAM]] — Self-evolving systems (evaluation of self-improvement methods)
- [[07_Physics-Aware-Embodied-AI]] — Physics commonsense benchmarks (PhyGenBench, VideoPhy-2, Physics-IQ, Morpheus)
- [[09_Egocentric-Pretraining-and-Human-Video]] — Egocentric datasets (Ego4D, EgoDex, Something-Something)
- [[01_Embodied-AI-101]] — VLA vs WAM basics

---

*See [[03_VLA]] for VLA design principles informed by these benchmarks, or [[04_WAM]] for world model evaluation.*
