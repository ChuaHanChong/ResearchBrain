---
title: "Glossary: Self-Evolving WAM"
tags:
  - self-evolving
  - WAM
  - glossary
aliases:
  - "Self-Evolving WAM Glossary"
---

## Where do static WAMs fail?

Three categories of OOD failure modes that static WAMs struggle with:

**Perturbed physics** (changed mass, friction, damping, lighting) - robot encounters physical properties it wasn't trained on. [[2510.03827|LIBERO-PRO]]: VLAs collapse from >90% to near 0%.

- A cup is 3x heavier than training → gripper can't lift it
- Table surface is oiled → objects slide when pushed
- Robot joint damping doubled → arm overshoots target positions
- Lighting changed → visual encoder misidentifies objects

**Novel compositions** (multi-step sequencing, unseen object pairings, new spatial layouts) -combinations of skills seen individually but never together. [[2602.06556|LIBERO-X]]: only 39.4% at easiest level; [[2505.03500|TLI]]: 9% on novel spatial compositions.

- "Pick up the red cube AND place it in the blue bowl" — seen pick-up and place separately, never this combo
- "Stack 3 blocks then push the tower into the bin" — 3-step chain never demonstrated
- Objects in new spatial arrangements (cube behind the bowl instead of beside it)

**Detail-oriented tasks** (sub-mm insertion, deformable manipulation, precise pouring) - fine-grained precision that typical demonstrations don't emphasize. [[2601.11421|GM-100]]: best VLA achieves only 24.9%.

- Insert a peg into a hole with 0.2mm clearance
- Fold a cloth along a specific crease line
- Pour liquid to a precise fill level without spilling
- Thread a cable through a small loop

Each maps to a loop mechanism: perturbed physics → DETECT (prediction error), novel compositions → RoboMD adversary, detail-oriented → SOE VIB probing (low α* = fragile).

## Active probing vs passive signals — what's the difference?

**Passive signals** — metrics you get for free from running the model normally. No special action needed, just observe:

- Prediction error — world model predicts the future anyway; check how wrong it was
- Action variance — run SDE sampler multiple times; high spread = model is unsure

**Active probing** — deliberately stress-test the model to force failures:

- SOE VIB — perturb the latent representation with increasing α until the model breaks (finding α*)
- RoboMD — train an RL adversary whose job is to discover environment configs that make the model fail
- PLD probing — deploy the model in hard scenarios specifically to observe where it fails

Passive tells you "the model is struggling here." Active tells you "the model breaks HERE, at THIS boundary, under THESE conditions." Active is more expensive but more informative.

## What is Variational Information Bottleneck (VIB)?

A compression technique that forces a network to learn only the most task-relevant information.

In [[2509.19292|SOE]] (Step 3b): an MLP encoder compresses the full observation into a tiny latent z (~8-16 effective dimensions), then tries to reconstruct the correct action from only z. A KL penalty forces z to stay close to a standard Gaussian — if information isn't essential for action prediction, it gets discarded.

Why it matters: by compressing to a compact z, SOE discovers what information the model actually relies on. Perturbing z with increasing noise (α > 1) finds where behavior breaks — the behavioral boundary α*. Small α* = fragile (narrow information channel, easily disrupted). See [[04_Mathematical-Formulation-Self-Evolving-WAM#3b Behavioral Probing via SOE VIB 2509 19292 SOE|04_ Section 3b]] for the math.

## How does the loop decide which episodes are "hard"?

After each episode, compute mean prediction error: S_env = (1/T) Σ L_pred(t). Keep a rolling window of recent scores (last 100 episodes), compute μ and σ, then flag if S_env > μ + 2σ — meaning the prediction error is 2+ standard deviations above the recent average.

"Rolling" means the threshold adapts over time — as the model improves, baseline error drops, so what counts as "surprising" adjusts automatically. An episode that was normal in round 1 might be flagged in round 5 if the model has improved on everything else.

Note: in the updated loop, this is one of three detection signals. The full DETECT uses [[X0_Glossary#Active probing vs passive signals — what's the difference?|multi-signal fusion]] (≥2 of 3 must fire), so the rolling threshold alone doesn't flag an episode — it needs at least one other signal (SAFE or action variance) to agree.

## Why not adopt existing self-evolving VLA methods directly?

Papers like [[2602.06508|World-VLA-Loop]], [[2511.16166|EvoVLA]], [[2511.15605|SRPO]], [[2506.21669|SEEA-R1]], and [[2509.15155|Self-Improving EFM]] each tackle self-improvement for VLAs, but none can be directly applied to Fast-WAM or VLA-JEPA for two reasons:

1. **Action representation mismatch** — 3 of 5 (SRPO, SEEA-R1, Self-Improving EFM) use discrete token actions with PPO/GRPO/REINFORCE on token log-probabilities. Our WAMs use continuous action chunks via flow matching — the RL algorithms don't transfer. Even SRPO, which tested on π0 in real-world, only transferred the *reward* via offline RL — not the full online optimization loop.

2. **Stage coverage gaps** — No single method covers detection + exploration + recovery. World-VLA-Loop has dreams but no OOD detection. EvoVLA has intrinsic reward but no world model. SRPO has dense reward but no active exploration. None addresses all three OOD failure modes (perturbed physics, novel compositions, detail-oriented tasks).

## Why flow matching over discrete action tokens?

Flow matching generates actions by solving an ODE from noise to continuous action chunks (e.g., 8 steps × 7-DoF = 56 continuous values). Discrete token VLAs (OpenVLA, RT-2) bin each dimension into ~256 tokens.

- **Precision** — no quantization error. Sub-mm tasks (GM-100: 0.2mm peg-in-hole) need arbitrary-precision outputs, not 0.008-wide bins
- **Multi-modal actions** — different noise seeds → different valid strategies. This is what πRL Flow-SDE exploits for uncertainty estimation
- **Chunk coherence** — the entire chunk is generated jointly by one ODE solve, not as independent tokens
- **Richer RL gradients** — continuous velocity field gives directional gradient signal, not just "right/wrong token"
