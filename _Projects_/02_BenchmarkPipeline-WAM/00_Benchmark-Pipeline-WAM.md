---
id: benchmark-pipeline-wam
title: WAM Benchmark Pipeline — Production-Ready Evaluation Plan
created: 2026-05-17
tags:
  - benchmark
  - WAM
  - world-action-model
  - bimanual
  - humanoid
  - sim-to-real
  - long-horizon
  - evaluation-protocol
aliases:
  - WAM Benchmark Suite
  - Benchmark Pipeline
---

# WAM Benchmark Pipeline — Production-Ready Evaluation Plan

> [!abstract] Purpose
> A focused, **7-item production-ready evaluation plan** for a **video-generative World-Action Model (WAM)**. Every benchmark scores **action quality** — that's what the WAM ultimately delivers. The world model is internal scaffolding; benchmarks for WAM are still fundamentally action benchmarks. Pick #2 is the special case: it scores actions *selected via WM imagination*, which is the WAM's coupling claim.
>
> **WAM paradigm assumed**: video-generative ([[2601.16163|Cosmos Policy]] / [[2504.02792|UWM]] style) — predicted future *frames* are the WM output. Paradigm only affects pick #2 (joint WM+action requires the WM to emit video to be rollouted as a simulator); the other 5 axes are paradigm-agnostic.
>
> **Cross-cutting hygiene** (applies to every entry below): report inference latency alongside SR — [[2603.22078|WAM vs VLA Robustness]] shows WAMs are ≥4.8× slower than VLAs; cite [[2603.16666|Fast-WAM]] if imagination is decoupled from deploy.

**Why these 7 axes.** A WAM is judged by its actions, but the path runs through *dynamics prediction* and *imagination-time planning*. The 7 axes cover the distinct failure modes on that path: (i) memorization vs generalization, (ii) WM↔action coupling, (iii) bimanual coordination, (iv) humanoid whole-body + dex, (v) long-horizon rollout, (vi) sim-to-real correlation, (vii) third-party credibility + safety.

---

## The 7-item set

### Pipeline mapping (development → deployment)

```
[DEV] ───────────── [CAPABILITY] ──────── [VALIDATE] ───── [DEPLOY]

#1 LIBERO-PRO       #3 RoboTwin 2.0       #6 SimplerEnv    #7 RoboArena
#2 WorldGym +       #4 HumanoidBench         + VISER          + RoboChallenge
   WorldArena +     #5 RoboCerebra                            + safety
   WoW-World-Eval

mid-training        specific-capability   sim-real         real-world
diagnostics         evaluation            correlation      leaderboard
```

Each gate has higher cost and higher credibility than the previous. Passing #1 is the entry ticket to #2 - #5; passing capability evals lets you trust the sim-real correlation in #6; #6 lets you predict #7 performance before paying for real-robot evals.

| # | Role | Benchmark | Institution | Venue | Core question it answers |
|---|------|-----------|-------------|-------|--------------------------|
| 1 | Diagnostic gate | [[2510.03827\|LIBERO-PRO]] | Huazhong UST + Lehigh | arXiv 2025 | Is the WAM memorizing or generalizing? |
| 2 | Joint WM+action | [[2506.00613\|WorldGym]] + [[2602.08971\|WorldArena]] + [[2601.04137\|WoW-World-Eval]] | Stanford (Liang + Yang); Tsinghua (Yong Li); PKU (Shanghang Zhang) | arXiv 2025; arXiv 2026 (leaderboard); arXiv 2026 | Does WM-mediated policy ranking transfer to real action quality, and can imagined videos be inverted to executable actions? |
| 3 | Bimanual | [[2506.18088\|RoboTwin 2.0]] | HKU + Shanghai AI Lab + CUHK | arXiv 2025 | Can the WAM coordinate two arms? |
| 4 | Humanoid | [[2403.10506\|HumanoidBench]] | UC Berkeley + Yonsei | **RSS 2024** | Can the WAM drive a humanoid (whole-body + dex)? |
| 5 | Long-horizon | [[2506.06677\|RoboCerebra]] | Beihang + NUS + SJTU | **NeurIPS 2025** | Can imagined rollouts survive multi-step compositional tasks? |
| 6 | Sim-to-real (primary + supplement) | [[2405.05941\|SimplerEnv]] + [[2605.06311\|VISER]] | UCSD/Stanford/Berkeley/GDM; Nanjing U | **CoRL 2024**; arXiv 2026 | Does the sim score predict the real score? |
| 7 | Independent real-world (primary + supplement + safety) | [[2506.18123\|RoboArena]] + [[2510.17950\|RoboChallenge]] + collision-violation rate | UC Berkeley/Stanford; Dexmal + Hugging Face | **CoRL 2025**; arXiv 2025 | Is the result credible to a third party, and is the WAM safe? |

---

## Complementarity matrix (7 axes ↔ 7 entries)

| Failure axis stressed | LIBERO-PRO | WorldGym + WorldArena + WoW | RoboTwin 2.0 | HumanoidBench | RoboCerebra | SimplerEnv + VISER | RoboArena + RoboChallenge |
|------------------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1. Memorization detection | ✓ | | | | | | |
| 2. Joint WM+action coupling | | ✓ | | | | | |
| 3. Bimanual coordination | | | ✓ | partial | | | |
| 4. Humanoid whole-body + dex | | | | ✓ | | | |
| 5. Long-horizon chains | | partial | | | ✓ | | |
| 6. Sim-to-real Pearson r | | | | partial | | ✓ | |
| 7. Independent real-world + safety | | | | | | | ✓ |

No two columns are redundant. Every failure axis has a primary owner.

---

## The 7 entries

Each entry follows the same template: **Institution / venue → Embodiment → Why for WAM → SOTA to beat → Reporting**. Multi-paper entries (#2, #6, #7) bundle papers under one axis; each paper uses the same 5-bullet template.

### 1. Diagnostic gate (memorization detection): [[2510.03827|LIBERO-PRO]]
- **Institution / venue**: Huazhong UST + Lehigh — arXiv 2025
- **Embodiment**: Single-arm Franka in [Robosuite](https://robosuite.ai/)
- **Why for WAM**: Minor perturbations on object attributes, initial positions, instructions, environment **collapse SOTA VLAs from >90% to ~0%**. Run this first — if your WAM also collapses, every downstream score is a memorization artifact.
- **SOTA to beat**: OpenVLA / π0 / π0.5 all hit **~0%** on the generalized setting. Any WAM holding even 20% is publication-worthy.
- **Reporting**: per-perturbation-axis SR + displacement-binned curve (sensitivity grows >0.2 units).

### 2. Joint WM+action coupling: [[2506.00613|WorldGym]] + [[2602.08971|WorldArena]] + [[2601.04137|WoW-World-Eval]]
The only axis that scores *coupling* between the WAM's two halves. Three benchmarks, three facets.

**2a. [[2506.00613|WorldGym]] — canonical WM-as-simulator correlation**
- **Institution / venue**: Stanford (Percy Liang + Sherry Yang) — arXiv 2025
- **Embodiment**: BridgeData V2 single-arm
- **Why for WAM**: Policy SR *inside* a learned video WM correlated with real-robot SR. **Pearson r=0.78** across 17 Bridge tasks, mean SR diff **3.3%**.
- **SOTA to beat**: r=0.78 vs real Bridge — the reference correlation every video-WAM paper cites.
- **Reporting**: Pearson r + per-task SR-difference distribution.

**2b. [[2602.08971|WorldArena]] — unified benchmark, 4 functional roles**
- **Institution / venue**: Tsinghua (Yong Li lab) — arXiv 2026
- **Embodiment**: RoboTwin 2.0 bimanual (same substrate as pick #3)
- **Why for WAM**: 14 representative embodied world models scored across **perception (6 dimensions) + 3 embodied tasks** (data engine, policy evaluator, action planner) under one harness. CtrlWorld policy-evaluator Pearson r=**0.986**.
- **SOTA to beat**: EWMScore correlates with human judgments at Pearson **r=0.825** (perceptual quality), but only weakly with action planning (**r=0.360**) — substantial headroom on the action-planning axis.
- **Reporting**: EWMScore + functional-utility breakdown (data-engine, policy-eval, action-planning).

**2c. [[2601.04137|WoW-World-Eval]] — IDM Turing Test**
- **Institution / venue**: PKU (Shanghang Zhang, Jian Tang) — arXiv 2026
- **Embodiment**: Video WMs scored across 5 dimensions (Perception / Planning / Prediction / Generalization / Execution)
- **Why for WAM**: **IDM Turing Test** feeds imagined video into an Inverse Dynamics Model, recovers actions, executes on real robot. Damning: Kling **9.88%** / Hailuo **2.47%** despite high video-quality; only real-robot-trained WoW-wan **40.74%**.
- **SOTA to beat**: IDM Turing Test **40.74%** (WoW-wan); 22-metric overall–human Pearson **r=0.93**.
- **Reporting**: 22-metric score + IDM execution SR + human-correlation Pearson.

> [!tip] Suite-wide joint-coupling reporting
> Beyond the three benchmark numbers, compute a paper-internal correlation table — regress your WAM's imagined-rollout SR against its closed-loop real-robot SR across your 7-axis tasks. Per the methodological successor [Scalable Policy Evaluation with Video WMs (2511.11520)](https://arxiv.org/abs/2511.11520) (NVIDIA + U Toronto, 2025; r=0.83–0.88 synthetic, 0.687 Bridge), this self-computed coupling metric is the cleanest publishable joint-coupling claim.

### 3. Bimanual coordination: [[2506.18088|RoboTwin 2.0]]
- **Institution / venue**: HKU + Shanghai AI Lab + CUHK (Ping Luo, Yao Mu) — arXiv 2025 (live leaderboard)
- **Embodiment**: Bimanual dual-arm (5 platforms); ManiSkill / [MuJoCo](https://mujoco.org) backend
- **Why for WAM**: Ships **data generator + benchmark + domain randomization** together. **+24.4% real-world few-shot SR**, **+21.0% zero-shot unseen-background**. Dual identity (generator + benchmark) suits the data-hungry inner loop of WAM training.
- **SOTA to beat**: MLLM expert code-gen **71.3%** with multimodal feedback; policy-side gains +24.4% / +21.0%.
- **Reporting**: per-task SR + coordinated-timing failure breakdown — DR alone does not fix this, your WAM's predicted-future fidelity should.

### 4. Humanoid whole-body + dexterous: [[2403.10506|HumanoidBench]]
- **Institution / venue**: UC Berkeley + Yonsei (Sferrazza, Huang, Lin, Lee, Abbeel) — **RSS 2024**
- **Embodiment**: Unitree H1 + dual Shadow Hand (101 DoF total, 61-D action space)
- **Why for WAM**: 27 standardized tasks (**12 locomotion + 15 whole-body manipulation**), shared rewards, open-source code, 4 reproducible baselines (==DreamerV3==, ==TD-MPC2==, ==SAC==, ==PPO==). Paradigm-agnostic: WAM ingests 151D state, imagines futures internally, outputs 61-D actions.
- **SOTA to beat**: All 4 baselines fail most manipulation; locomotion partial. Hierarchical RL with pretrained low-level skills the only progress. Vast headroom; you'd be the first video-generative WAM number.
- **Reporting**: locomotion subset SR + manipulation subset SR (separately) + 4 baseline numbers for context. *Reference baseline*: [[2502.20396|Humanoid Sim2Real Dex]] reports 80% box-lift, 52.5% bimanual handover on Fourier GR-1 — cite for vision-conditioned context.

### 5. Long-horizon chains: [[2506.06677|RoboCerebra]]
- **Institution / venue**: Beihang + NUS + Shanghai Jiao Tong — **NeurIPS 2025**
- **Embodiment**: Simulated household manipulation; 1,000 trajectories, 100 task variants
- **Why for WAM**: **2,972.4 sim steps per trajectory (~6× longer than CALVIN/LIBERO)**. HPE **13.21%** on Mix vs OpenVLA **0.00%** — pure System-1 fails; natural showcase for WAM imagined-multi-step planning.
- **SOTA to beat**: GPT-4o planner **16.04% SR / 68.33%** planning accuracy; HPE framework **13.21%**.
- **Reporting**: end-to-end SR + step-level segment accuracy — the WAM thesis is imagination chains the steps.

### 6. Sim-to-real correlation: [[2405.05941|SimplerEnv]] + [[2605.06311|VISER]]
SimplerEnv is the canonical primary; VISER is the PBR stretch goal.

**6a. [[2405.05941|SimplerEnv]] — canonical correlation gate**
- **Institution / venue**: UCSD + Stanford + Berkeley + Google DeepMind (Levine, Finn, Hao Su, Vuong) — **CoRL 2024**
- **Embodiment**: Google Robot + BridgeData V2 digital twins
- **Why for WAM**: **Pearson r > 0.85** (Google Robot tasks), **r = 0.890** (BridgeData V2). Introduces **MMRV (Mean Maximum Rank Violation)** — the policy-ranking metric.
- **SOTA to beat**: r ≥ 0.85, MMRV ≤ baseline.
- **Reporting**: Pearson r + MMRV + per-task breakdown.

**6b. [[2605.06311|VISER]] — PBR sim-real correlation (supplement)**
- **Institution / venue**: Nanjing U + collaborators — arXiv 2026
- **Embodiment**: Ray-traced PBR digital twins, MLLM-driven asset generation
- **Why for WAM**: **Pearson r=0.92** with per-cue diagnostics — specular highlights and contact shadows pinpointed as load-bearing visual cues for VLA generalization.
- **SOTA to beat**: r=0.92 (stretch goal beyond SimplerEnv).
- **Reporting**: r + per-cue ablation table. Report alongside SimplerEnv, not instead of.

### 7. Independent real-world + safety: [[2506.18123|RoboArena]] + [[2510.17950|RoboChallenge]]
RoboArena is the peer-reviewed primary; RoboChallenge supplements with platform diversity. Both report a `collision_violation_rate` sub-metric.

**7a. [[2506.18123|RoboArena]] — decentralized real-robot leaderboard**
- **Institution / venue**: UC Berkeley + Stanford (Levine, Finn, Liang, Pertsch) — **CoRL 2025**
- **Embodiment**: 7 academic labs, DROID Franka Panda
- **Why for WAM**: Decentralized pairwise comparison with **Pearson r=0.98 to oracle, MMRV 1.8%**, converges in ~100 pairs over **600+ real-robot episodes** across **7 academic institutions**. Third-party credibility.
- **SOTA to beat**: live leaderboard (submission-based).
- **Reporting**: public submission + frozen checkpoint hash + `collision_violation_rate` (hard collisions, off-track motion, operator hand-clamp). Caveat: slow gate (weeks) — submit early.

**7b. [[2510.17950|RoboChallenge]] — Table30 remote-robot leaderboard (supplement)**
- **Institution / venue**: Dexmal + Hugging Face — arXiv 2025
- **Embodiment**: 10 diverse remote real robots (multi-platform fleet)
- **Why for WAM**: **Table30** with 30 fixed tasks, 1,000 demos/task, async API. π0.5 leads; soft-body **8% SR / 27% progress** is open WAM headroom.
- **SOTA to beat**: π0.5 fine-tuned (varies by task).
- **Reporting**: per-task progress-score + collision rate.

---

## Cross-references

- [[02_Dataset-Benchmark-Environment]] — master benchmark deep-dive
- [[11_Sim-to-Real-Transfer]] — sim-real protocol deep-dive
- [[04_WAM]] — WAM paradigms being benchmarked
- [[Research-Directions-WAM]] — WAM research direction overview
- [[Research-Directions-Embodied-AI]] — broader VLA / WAM research direction overview
