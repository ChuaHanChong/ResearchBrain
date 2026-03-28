---
title: "VLA Design Principles — RoboVLMs Study"
tags:
  - VLA
  - robotics
  - foundation-model
  - manipulation
aliases:
  - VLA Design
  - RoboVLMs
---

# VLA Design Principles — RoboVLMs Study

> [!abstract] One-Line Summary
> Based on 600+ experiments, the optimal VLA recipe is: ==KosMos/[[2407.07726|PaliGemma]] backbone== + ==Policy Head fusion== + ==Continuous actions== + ==MoE== + ==Post-training on in-domain data==.

This note synthesizes findings from the [[2412.14058|RoboVLMs]] study on building high-performing Vision-Language-Action models for generalist robots.

---

## Why VLAs?

VLAs inherit robust multi-modal representations from pre-trained VLMs, giving them strong semantic generalization that model-free and model-based approaches lack. See [[01_VLA-WAM-101#Four Learning Strategies]] for the full comparison.

**RoboVLMs SOTA results:**
- CALVIN: average **4.25/5** consecutive tasks (zero-shot), outperforming [[2312.13139|GR-1]] by **+1.19** tasks
- SimplerEnv: highest average success rates on both WidowX + Bridge and Google Robot
- Real-world: outperformed [[2405.12213|Octo]] and [[2406.09246|OpenVLA]] across 20 tasks with unseen variables

---

## Backbone Selection

| Category | Models | Finding |
| --- | --- | --- |
| ==Encoder-Decoder== | Flamingo family | Outperformed by decoder-only architectures |
| ==Decoder-Only== | LLaVA, Qwen-VL, MoonDream, [[2407.07726\|PaliGemma]], KosMos | KosMos and PaliGemma are distinctly superior |

> [!tip] Why These Two Win
> Extensive ==vision-language pre-training== on large-scale datasets creates stronger alignment between visual and linguistic features — critical for following complex spatial instructions.

---

## Architecture Decisions

Three design axes determine VLA performance:

### Action Space

- ==Continuous== (recommended) — high-precision floating-point values; avoids compounding discretization errors over long horizons
- ==Discrete== — action tokens predicted auto-regressively; performance degrades as task horizons increase

### History Modeling

| Approach | How It Works | Trade-off |
| --- | --- | --- |
| ==One-Step== | Current observation only | Fast, but no temporal context |
| ==Interleaved== | History woven into VLM sequence | Effective but high memory/FLOPs |
| ==Policy Head== | VLM provides per-step features; separate head fuses history | Best balance — preserves VLM reasoning while integrating past observations |

### Training & Execution

- **Loss functions** — ==Flow Matching== (diffusion) and ==MSE+BCE== achieve similar results; diffusion adds complexity with limited benefit for short-horizon tasks
- **Chunking** — executing a full predicted action sequence outperforms single-action execution; maintains temporal coherence and enables >30Hz deployment
- **==Mixture-of-Experts (MoE)==** — dedicated action experts improve zero-shot generalization but don't boost seen-scenario performance

---

## Data Strategy

> [!warning] In-domain data is non-negotiable
> Even task-agnostic data from the *same robot* is more effective than massive cross-embodiment datasets for target tasks.

| Strategy | Impact |
| --- | --- |
| **In-domain only** | Best for task-specific performance |
| **Cross-embodiment (OXE)** | Improves few-shot learning (**+17.2%** on CALVIN few-shot) |
| **==Post-training==** (OXE → in-domain fine-tune) | Best overall — highest gains for high-frequency skills |

---

## Real-World Findings

Tested on a 7-DoF Kinova Gen3 with dual cameras (head + wrist) across four "unseen" conditions: distractors, backgrounds, target objects, and novel skill descriptions (GPT-4 synonyms).

> [!success] Emergent Self-Correction
> The KosMos-based policy head model autonomously adjusted its trajectory after a failed grasp attempt (e.g., re-locating an oven handle) — a behavior ==not present in the training data==.

---

## Quick-Reference Matrix

| Question | Answer |
| --- | --- |
| Why VLAs? | Strong robustness in real scenarios via VLM pre-training |
| Which backbone? | KosMos, [[2407.07726\|PaliGemma]] (extensive multi-modal pre-training) |
| How to formulate? | ==Continuous actions== + ==Policy Head== for history fusion |
| How to train? | Diffusion ≈ MSE; ==MoE== for zero-shot generalization |
| Data strategy? | ==Post-training==: cross-embodiment pre-train → in-domain fine-tune |

---

*See [[01_VLA-WAM-101]] for VLA vs WAM basics, and [[04_WAM]] for the WAM survey.*
