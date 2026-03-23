---
title: Self-Evolving World Action Models — 101
tags:
  - self-evolving
  - world-model
  - WAM
  - robotics
  - continual-learning
aliases:
  - Self-Evolving 101
  - Self-Evolving WAM
---

# Self-Evolving World Action Models — 101

> [!abstract] One-Line Summary
> Start with a trained [[01_VLA-WAM-101|world action model]] and add self-evolution — not the other way around.

## The Key Question

> [!question] What's the best starting point?
> **Option 1:** Train a self-evolving agent, then add "dreaming" (future state prediction).
> **Option 2:** Take a trained [[03_WAM|world action model]], then add self-evolution.

==Option 2 wins.== A world model already has a robust latent space for generating synthetic future states. Adding memory and continual learning to a system that can already "imagine" is far easier than teaching a reactive agent to dream from scratch.

**Why?** A model-free agent's neural pathways map states → actions only. Bolting on a world model means rebuilding the architecture. A world model already generates its own training data — the challenge shifts to ==data quality within the model's own imagination== (preventing hallucinated dynamics, artifact exploitation, and catastrophic forgetting).

---

## Self-Evolving Agent vs Self-Evolving WAM

> [!tip] The Distinction
> A self-evolving WAM is a *subset* of self-evolving agents. ==Not all self-evolving agents can predict the future.==

| | Self-Evolving Agent | Self-Evolving WAM |
|---|---|---|
| **Type** | Model-free (broader category) | Model-based (specific subset) |
| **Learns** | State → Action mapping via trial and error | Transition dynamics: $S_t, A_t \rightarrow S_{t+1}, R_{t+1}$ |
| **Can "dream"?** | No — reacts to outcomes after the fact | Yes — simulates thousands of futures in latent space |
| **Self-evolution focus** | Improving the policy directly | Minimizing world model prediction error + policy improvement |

> [!example] The Button Test
> A model-free agent learns "pressing button → reward" but has no concept of the gears behind the button. If the button jams, it's surprised *after* pressing. A WAM *imagines* the jam scenario and plans accordingly.

---

## What Is a Self-Evolving WAM?

A ==self-evolving world action model== simultaneously learns to predict environmental dynamics (world model) and optimize decision-making (action model) through continuous, self-supervised interaction. The world model refines its simulation of "how the world works" while the action model uses that simulation to plan and evolve.

### Core Mechanisms

- **World Models as Internal Simulators** — Forecast future states in latent space, enabling planning without real-world risk
- **Co-Evolutionary Loops** — The world model and action policy bootstrap each other: the world model generates synthetic rollouts for the policy; the policy's real experience grounds the world model (see [[2602.12063|VLAW]], [[2510.16079|EVOLVER]])
- **Self-Training and Self-Critique** — Techniques like [[2203.14465|STaR]] and [[2403.09629|Quiet-STaR]] let agents iteratively refine action plans through self-reflection rather than external labels
- **Curiosity-Driven Exploration** — Agents actively explore where their world model is most uncertain, ensuring the model evolves to cover a broader range of states

---

*See [[01_VLA-WAM-101]] for VLA vs WAM basics, and [[03_WAM]] for a survey of WAM papers by category.*
