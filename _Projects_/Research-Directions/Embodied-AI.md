---
title: "Promising Research Directions: VLA × WAM × Embodied AI"
aliases:
  - "VLA-WAM Promising Directions"
  - "Embodied-AI Research Directions"
tags:
  - research-directions
  - VLA
  - WAM
  - embodied-AI
  - self-evolving
---

# Promising Research Directions: VLA × WAM × Embodied AI

> [!abstract] Overview
> Every embodiment — a tabletop arm, a quadruped, a humanoid — runs on the *same* underlying mechanisms: a training objective, an evaluation protocol, a memory loop, a way to move through the world and transfer across bodies. The structural tension is that these mechanisms are usually built *per embodiment and per pipeline stage* — world model and policy trained separately, fidelity and control evaluated separately, navigation and manipulation engineered separately — discarding the joint structure the data actually carries.
> This is the **cross-cutting umbrella** the six sibling docs specialize: its **9 directions across 3 clusters** are embodiment-agnostic mechanisms — *Architecture & Training* (A), *Evaluation, Robustness & Deployment* (B), and *Mobility & Embodiment Generalization* (C) — that hold for any robot body, which [[Manipulation|Manipulation]], [[Locomotion|Locomotion]], [[Whole-Body|Whole-Body]], [[WAM|WAM]], [[Spatial-4D|Spatial-4D]], and [[Sim2Real|Sim2Real]] then instantiate per capability.
> The non-consensus bet the doc collectively makes: **refusing to factor away load-bearing structure beats collecting more of it** — predict the joint $p(o',a)$ in one loop rather than cascade two models, measure imagination-and-action on one causal axis rather than two, keep the control-relevant future in latent rather than render pixels, and keep the morphology-invariant intent rather than tokenize per body.

---

## Methodology

**Scope.** Corpus: ~56 VLA / WAM / embodied / physics / safety surveys and ~120 method + benchmark papers from `_KnowledgeHub_/`, cross-checked against [[08_Benchmarks-and-Surveys#4. Robotics & Embodied AI Surveys|08_Benchmarks-and-Surveys §4]] / [[08_Benchmarks-and-Surveys#5. Self-Evolving AI Surveys|§5]] / [[08_Benchmarks-and-Surveys#7. Specialized Domain Surveys|§7]] and the `Embodied-AI/` deep-dives ([[05_VLA|05_VLA]], [[07_WAM|07_WAM]], [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]], [[06_VLA-Reasoning-and-CoT|06_VLA-Reasoning-and-CoT]], [[13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]], [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]]). This doc owns the **embodiment-agnostic mechanisms** — training objective, evaluation, deployment, mobility, cross-body transfer — that hold for any body; a direction is admitted only if it is a *mechanism* rather than a physical capability. Single-embodiment capabilities are cross-referenced, not re-clustered: arms + hands to [[Manipulation|Manipulation]], legs + wheels to [[Locomotion|Locomotion]], the loco-manipulation coupling to [[Whole-Body|Whole-Body]]; the WAM-internal architecture to [[WAM|WAM]], 4D scene structure to [[Spatial-4D|Spatial-4D]], transfer machinery to [[Sim2Real|Sim2Real]]. Kept directions have 3–10 papers attacking them with no agreed solution; saturated (more-compute-only) and premature (hypothetical-AGI) framings were dropped; intersections were favored (VLA×WAM, VLA×RL, WAM×egocentric, physics×RL, safety×deployment).

---

## VLA × WAM × Embodied AI Survey Landscape

| Survey / Benchmark | The open problem it names (surveys) / what it measures (benchmarks) | Fuels |
|---|---|---|
| [[2605.12090\|WAM Survey]] | Causal-consistency joint metrics; separate WM-vs-action eval gap; long-horizon drift; closed-loop latency — Joint over Cascaded named as the frontier | A1, B1, B3 |
| [[2605.00080\|WM Robot Learning Survey]] | Eval beyond visual fidelity; closed-loop vs open-loop; latent WM dominance; causal conditioning; cross-embodiment | A1, B1, C1 |
| [[2604.04974\|Video-to-Control Survey]] | Integration layer is the critical gap; interface trade-offs; latent-action identifiability; pre-execution verification; physical feasibility as a missing layer | A1, A3 |
| [[2604.22748\|Agentic World Modeling Survey]] | Counterfactual reasoning; constraint adherence; autonomous self-revision (L3 Evolver); decision-centric metrics (ASR + COD) | A1, B1, B2 |
| [[2510.16732\|World Models for Embodied AI Survey]] | Physically-consistent metrics beyond FID/FVD; long-horizon temporal consistency; SSM/hybrid AR-global; WM × LLM-CoT synergy | A1, B1 |
| [[2601.15533\|Actionable Simulators]] | Dynamical hallucinations; structured 4D interfaces; self-evolution; closed-loop decision-oriented eval | A3, B1 |
| [[2411.14499\|World Models Survey]] | Physical-rule adherence; standardized benchmarks; sim2real; interactive 3D action-conditioned WMs | A3, B1 |
| [[2604.15395\|Foundation Models in Robotics Survey]] | Tactile/failure-data scarcity; embodiment-agnostic action spaces; latency; long-horizon memory; physics-informed WMs; formal verification | A1, B2, C2 |
| [[2509.19012\|Pure VLA Survey]] | Data scarcity; architectural heterogeneity; real-time inference; eval fragmentation; world modeling + causal reasoning | A2, B3 |
| [[2510.07077\|VLA Robotics Real-World Review]] | Embodiment transfer; data scarcity; computational cost; eval + safety; gradient insulation / PEFT / inference optimization | B3, C2 |
| [[2506.20966\|VLA Post-Training Survey]] | Generalization-vs-precision; knowledge insulation during RL | A1, A2 |
| [[2505.04769\|VLA Concepts Survey]] | Real-time inference (AR 3–5 Hz ceiling); safety (~82% collision); generalization gap (~40%) | B3 |
| [[2503.21765\|Physics Cognition Survey]] | Sub-human physics (multi-object/fluid); limited physical coverage; sim2real; physics foundation + neuro-symbolic | A3 |
| [[2510.04978\|Physical AI Survey]] | Causal understanding missing; compositional/causal structure; hybrid Neural Physics | A2, A3 |
| [[2509.25373\|VLM Perception-Cognition Survey]] | Shallow perception-cognition integration; pixel-to-world-model translation; hallucination from disjoint coupling | A2 |
| [[2601.07823\|Video Generation in Robotics Survey]] | Hallucinations + physics violations as top-2; uncertainty; long videos; robotics-centric benchmarks | A3, B1 |
| [[2604.16592\|Cognition WM Survey]] | Motivation + meta-cognition drastically under-developed; epistemic WMs over structured knowledge | B2 |
| [[2602.04411\|Self-evolving Embodied AI]] | "Human-crafted settings" limit; multi-timescale closed-loop co-evolution; integration of WM/memory/embodiment | B2, B4 |
| [[2508.07407\|Self-Evolving AI Agents Survey]] | Continuous self-improvement w/o forgetting; evolution-evaluation gap; safety under self-modification | B4 |
| [[2404.14387\|LLM Self-Evolution Survey]] | Lifelong-learning forgetting; self-generated experience quality; alignment under self-evolution | B4 |
| [[2310.06253\|Objective Mismatch MBRL Survey]] | Decision-aware MBRL; predictive-loss vs return misalignment; cross-family fragmentation | B1 |
| [[2510.24795\|Efficient VLA Survey]] | Latency / control freq incompatible with edge; pre-training cost; embodiment-agnostic; self-sustaining data | B3 |
| [[2603.28489\|Video Gen as WM Survey]] | Efficiency as prerequisite; distillation / sparse attention / quantization; integrated efficiency | B3 |
| [[2511.05936\|10 VLA Challenges]] | OOD brittleness; data quality; resource efficiency; safety assurances; cross-robot generalization as named bottlenecks | A1, B1, B3, B4 |
| [[2605.02900\|Safety in Embodied AI Survey]] | Five-layer attack taxonomy (perception→cognition→planning→action); cascade propagation; memory poisoning; self-evolving misalignment | B1, B2 |
| [[2604.23775\|VLA Safety Survey]] | Multi-layered defense; fragmented evaluation methodology | B1, B2 |
| [[2311.00530\|LLM Embodied Navigation Survey]] | Long-horizon planning grounding; context-window limits; multimodal grounding | C1 |
| [[2504.21853\|Interactive Generative Video Survey]] | Real-time vs quality; persistent memory; dynamics fidelity; cross-domain transferability | C1 |
| [[2504.03515\|Dexterous IL Survey]] | Tactile integration; cross-embodiment transfer; demo scaling | C2 |
| [[2604.04707\|OpenWorldLib]] | Definition fragmentation; 3D geometric consistency under camera motion; modular pipeline composition | C2 |
| [[2306.03310\|LIBERO]] | In-distribution manipulation SR ceiling (97.2%) across 130 task suites; the action-quality anchor every direction reports against | A1, A2, B1, B3, B4 |
| [[2510.13626\|LIBERO-Plus]] | 10,030 OOD perturbations; the robustness axis joint training / step rewards / continual methods must improve | A1, A2, B2, B3, B4 |
| [[2605.08567\|ACWM-Phys]] | Action-conditioned video-WM physics generalization: InD SSIM 0.988 → OOD ΔM-MSE up to +40; the physics cliff A3 fixes | A3 |
| [[2605.21800\|stable-worldmodel]] | Reproducible WM harness; planning SR decays under mild perturbation even at 92–94% in-dist SR | A1, B1 |
| [[2605.06311\|VISER]] | Sim-real Pearson r = 0.92 with 1,000+ PBR objects; existence proof the joint-axis correlation is recoverable | B1 |
| [[2605.20774\|VLA-REPLICA]] | Reproducible real-world VLA eval; cross-lab reproducibility validated (ID 0.49 vs 0.48) | B1, B3 |
| [[2506.18123\|RoboArena]] | Real-fleet evaluation across 8 platforms / ~120 tasks; the deployment anchor | B1, B2, B3 |
| [[2505.14986\|AnyBody]] | 18-robot cross-embodiment transfer: interpolation transfers, extrapolation collapses to 0% | C2 |
| [[2004.02857\|R2R-CE]] | Continuous-environment VLN SR / SPL on Val-Unseen; the navigation efficiency-vs-accuracy battleground | C1 |

> [!tip] Convergence patterns
> - **The joint WM-action evaluation gap** (5-way): [[2605.12090|WAM Survey]], [[2605.00080|WM Robot Learning Survey]], [[2510.16732|World Models for Embodied AI Survey]], [[2601.15533|Actionable Simulators]], and [[2601.07823|Video Generation in Robotics Survey]] all diagnose that current protocols score WM quality (FVD/PSNR) and action quality (SR) *separately* under different vocabulary (causal consistency / closed-loop / physically-consistent metrics) — a joint model can pass each while imagination and action are disconnected. The benchmarks make it measurable: [[2605.06311|VISER]] reports sim-real Pearson **r = 0.92** when fidelity is controlled and [[2605.21800|stable-worldmodel]] shows planning SR collapses under mild perturbation even at 92–94% in-dist SR — the empirical mandate for A1's joint loop and B1's joint metric.
> - **Physical grounding / dynamical hallucinations** (5-way): [[2503.21765|Physics Cognition Survey]], [[2510.04978|Physical AI Survey]], [[2601.15533|Actionable Simulators]], [[2411.14499|World Models Survey]], and [[2601.07823|Video Generation in Robotics Survey]] converge on hybrid neural-symbolic + verifiable physics as the missing layer, and [[2605.08567|ACWM-Phys]] *quantifies* the cliff (InD SSIM **0.988** → OOD ΔM-MSE up to **+40** on robot-arm, **+30** on cloth) — the mandate for A3's action-level physics predicates.
> - **Data scarcity as the dominant scaling wall** (5-way): [[2604.15395|Foundation Models in Robotics Survey]], [[2509.19012|Pure VLA Survey]], [[2510.07077|VLA Robotics Real-World Review]], [[2504.03515|Dexterous IL Survey]], and [[2511.05936|10 VLA Challenges]] all name internet-scale human video + massively-parallel sim + self-exploration as the levers against a tactile / failure / demonstration data shortage — the substrate constraint B3 and B4 design around.
> - **Efficiency as a deployment prerequisite, not an afterthought** (4-way): [[2510.24795|Efficient VLA Survey]], [[2603.28489|Video Gen as WM Survey]], [[2505.04769|VLA Concepts Survey]] (the **3–5 Hz** AR ceiling vs the 20–50 Hz needed), and [[2511.05936|10 VLA Challenges]] (resource efficiency named one of ten bottlenecks) reframe inference cost from "engineering to sort out later" to a first-class control constraint — the mandate for B3.
> - **Self-evolution / autonomous adaptation as the missing function** (5-way): [[2602.04411|Self-evolving Embodied AI]], [[2604.16592|Cognition WM Survey]], [[2604.22748|Agentic World Modeling Survey]], [[2508.07407|Self-Evolving AI Agents Survey]], and [[2404.14387|LLM Self-Evolution Survey]] all name meta-cognition / autonomous self-revision (the L3 Evolver) as the un-built capability, *and* continual improvement without forgetting as its hard precondition — the mandate for B2's recovery loop and B4's forgetting-free fine-tune.
> - **Safety as a deployment-blocking, non-separable axis** (3-way): [[2605.02900|Safety in Embodied AI Survey]] (five-layer attack taxonomy + cascade propagation + memory poisoning), [[2604.23775|VLA Safety Survey]], and [[2511.05936|10 VLA Challenges]] (safety assurances named explicitly) converge on the finding that adversarial/jailbreak robustness and self-evolving misalignment cannot be separated from the evaluation and memory loops they corrupt — the constraint that cuts across B1 and B2.

---

## Formal Framing

**Three families of conditional distributions.** Every direction in this doc operates on one of three joint distributions over an observation $o$ (image/video), an action $a$, and a language instruction $l$, where a prime marks a predicted output ($o'$ a future observation):

| Family | Joint distribution | Predicts |
|---|---|---|
| **VLA** (Vision-Language-Action) | $p(a \mid o, l)$ | Action conditioned on observation + language; no dynamics |
| **WM** (World Model) | $p(o' \mid o, a)$ | Next observation conditioned on action; no action policy |
| **WAM** (World Action Model) | $p(o', a \mid o, l)$ | Both — the unifying frontier |

A WAM's training objective is the joint negative log-likelihood

$$\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o,l,o',a) \sim \mathcal{D}} \big[ -\log p(o', a \mid o, l) \big],$$

and the central observation is that the data $\mathcal{D}$ pairs each $o'$ with the $a$ that caused it, so $p(o',a \mid o,l)$ is *one* distribution — factoring it into a separate $p(o' \mid o,a)$ and $p(a \mid o,l)$ discards the conditional link the loss could exploit. WAMs split into **Cascaded** (predict state, derive action via inverse dynamics) and **Joint** (unified end-to-end); most "joint" methods are in fact Cascaded, so Joint is the architectural frontier A1 targets. Per the canonical definition:

> "WAMs are defined as embodied foundation models that integrate predictive state modeling with action generation, moving beyond merely predicting actions to predicting a joint distribution over future states and actions." — [[2605.12090|WAM Survey]]

**The causal-consistency object (B1).** A world model and a policy are *causally bound* only when the action taken in an imagined future matches the action taken in the executed one. Formally, sampling a counterfactual action $a'_t$ and rolling the WM to $\hat o'_{t+1}$, the binding holds iff $\|\hat o'_{t+1} - \hat o_{t+1}\|$ scales monotonically with $\|a'_t - a_t\|$ — a property visual-fidelity metrics (FID/FVD) cannot see, because a frame can look correct while being action-inconsistent. The **Action Success Rate (ASR)** and **Counterfactual Outcome Deviation (COD)** are the decision-centric metrics this object licenses.

**The capability hierarchy (B1, B2).** A WAM's competence factors into three levels — *L1 Predictor* (one-step local transitions), *L2 Simulator* (multi-step action-conditioned rollouts that respect domain laws), *L3 Evolver* (autonomous self-revision when predictions fail). L3 is "emerging not mature" for physical-world policies — the target B2's recovery loop builds and the constraint B1's metric must certify.

**The verifiable-physics object (A3).** A physical law (momentum, gravity, friction, contact) is a binary predicate $P_i(\cdot)$ checkable on an action sequence and *independent of the training set* — it holds for held-out and OOD data alike. A loss $\sum_i \lambda_i \big(1 - P_i(a_{1:T})\big)$ that penalizes violation therefore keeps working off-distribution, unlike an empirical loss that only trusts its samples. The bet of A3 is that $\rho\big(\sum_i P_i,\ \text{task SR}\big)$ is non-trivial — that satisfying physics at the action level predicts downstream success.

**The forgetting-as-interference object (B4).** In an over-parameterized policy, a new skill leans on a small set of weight directions $S_{\text{new}}$ and an old skill occupies $S_{\text{old}}$; the two are *mostly disjoint*, so forgetting occurs only on the overlap $S_{\text{new}} \cap S_{\text{old}}$. Retention is therefore a problem of *protecting the overlapping directions* (an importance-weighted penalty, $\mathcal{L} + \sum_j F_j (\theta_j - \theta_j^*)^2$), not of re-showing the old data — making replay the exception, not the default.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Architecture & Training** | A1, A2, A3 | Training objectives don't match the causal structure of physical reasoning — they cascade, supervise on outcomes only, or trust empirical losses off-distribution | A1's latent co-evolving substrate exposes the intermediate tokens A2 needs for step rewards; A3's physics-verifiable rewards stabilize A1's joint loop; A2's causal-importance predicates and A3's physical predicates are the same "dense local check beats sparse outcome" move at the reasoning vs dynamics level |
| **B — Evaluation, Robustness & Deployment** | B1, B2, B3, B4 | The lab-to-real gap — no joint metric, no recovery loop, a 3–5 Hz ceiling, forgetting under every fine-tune | B1's joint causal metric certifies whether A1/A3 gains transfer; B2's memory+recovery loop rides on B3's efficiency budget; B4's forgetting-free fine-tune is the precondition for B2's continual recovery updates not to erase prior skills; safety ([[2605.02900\|Safety in Embodied AI Survey]]) cuts across all four |
| **C — Mobility & Embodiment Generalization** | C1, C2 | Policies assume a fixed base and a fixed body; moving through the world (drift) and across morphologies (0% extrapolation) breaks both | C1's in-policy latent dreaming is the navigation analog of A1's latent loop and B3's latent-for-speed thesis; C2's morphology-invariant intermediate carries the structure-preserving lens A1/A3 exploit across *bodies* rather than across time; both hand their per-capability instantiations to the sibling docs |

---

## Cluster A — Architecture & Training: How the Model Learns

*Training objectives and architectural choices that align with the causal structure of physical reasoning — refusing to cascade the world model and policy (A1), refusing to supervise reasoning on outcomes alone (A2), and refusing to trust empirical losses off-distribution where physics is checkable (A3).*

### A1 — Single-Loop Co-Evolving Policy + World Model in Latent Space

| | |
|---|---|
| **Cluster** | A — Architecture & Training |
| **Thesis** | Train the policy and world model in one loop, not cascaded or alternating. One stream of data pairs each future observation with the action that caused it, so $p(o',a\mid o,l)$ is a single joint distribution and a single joint loss is the natural objective — separate losses throw away the conditional link. The field assumes WM↔policy alternation is needed for training stability. The bet is in First-principles below. |
| **Anchor papers** | [[2605.12090\|WAM Survey]] (survey), [[2605.00080\|WM Robot Learning Survey]] (survey), [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2306.03310\|LIBERO]] (benchmark), [[2510.13626\|LIBERO-Plus]] (benchmark), [[2511.08544\|LeJEPA]] (method) |
| **Key targets** | [[2306.03310\|LIBERO]] ≥97.2% in-dist; [[2510.13626\|LIBERO-Plus]] ≥79.5% OOD; latent ~10 ms inference vs pixel ~150 ms |

**Why it matters.**
- **The gap**: the world model and the policy learn two halves of the *same* distribution $p(o',a\mid o,l)$, yet the standard recipe trains them in stages — cascade a state predictor into an inverse-dynamics policy, or alternate WM and policy updates — discarding the conditional link the joint loss could exploit.
- **Today's answers**: every "joint" method falls short of a single cooperative loop — [[2602.12063|VLAW]] alternates so the WM trains on stale policy data; [[2603.16666|Fast-WAM]] drops the WM at deployment; [[2605.15153|Pelican-Unified]] unifies the architecture (**93.5%** [[2504.13059|RoboTwin]]) but trains multi-stage; [[2511.09515|WMPO]] and [[2511.15605|SRPO]] freeze the WM during inner-loop RL. None shows a single GRPO loop on the joint $(\text{action}, \text{imagination})$ log-prob with cooperative gradient flow.
- **The opening**: [[2603.25406|MMaDA-VLA]] jointly denoises the goal observation *and* the action chunk in one shared discrete-token space under a single masked-denoising objective — no auxiliary WM, no alternation — and already clears the in-dist bar at **98.0%** [[2306.03310|LIBERO]] (**4.78** CALVIN ABC→D), evidence that one joint loss is not only natural but competitive.

**First-principles framing.**
- **First principle**: One stream of data already pairs each future observation with the action that caused it, given the current view and the instruction — the world model and the policy are learning two halves of the *same* distribution. Train them with separate losses and you throw away that link. So one joint loss is the natural choice; training them in stages is the exception that needs a reason.
- **Assumption being challenged**: That you must alternate world-model and policy updates to keep training stable. Modern latent backbones — with a slow-moving target copy and a geometry term that stops the latent from collapsing ([[2511.08544|LeJEPA]]) — may make a single joint update stable enough that alternation is just a leftover from the pixel-space era. [[2511.09515|WMPO]] and [[2511.15605|SRPO]] bet the opposite by freezing the WM in their inner loops.
- **The bet**: One backward pass over a shared latent backbone beats alternating training on *both* in-distribution SR (≥97.2% [[2306.03310|LIBERO]]) and OOD SR (≥79.5% [[2510.13626|LIBERO-Plus]]), at no extra latency (latent ~10 ms vs pixel ~150 ms).

**Related research papers.**

Eighteen systems that put the WM↔policy relationship together in different ways — alternating, frozen-WM, frozen-policy, cascaded imagine-then-act, multi-stage joint, or single-objective joint — none of them a *single cooperative gradient* over a shared latent backbone. The axis is *how the WM and policy are coupled during training*:

| System | WM↔policy coupling | Space | Key result | What's missing |
|---|---|---|---|---|
| [[2602.12063\|VLAW]] | alternating WM + policy updates | latent | WM trains on stale policy data | the alternation A1 replaces — never a single joint gradient |
| [[2603.19370\|VAMPO]] | GRPO over video-denoising-as-MDP | pixel | single-loop but pixel-space, expensive | the imagination is rendered, so the loop cannot run at latent latency |
| [[2511.09515\|WMPO]] | on-policy GRPO in imagination, WM frozen | pixel | policy improves inside a fixed WM | the WM never updates — half the joint distribution is held fixed |
| [[2511.15605\|SRPO]] | frozen [[2506.09985\|V-JEPA 2]] + trajectory clustering | latent | WM never updates | latent and cheap, but the WM is a fixed feature extractor, not co-evolved |
| [[2606.02486\|AHEAD]] | frozen *policy*, train a 4.9M-param latent WM around it | latent | >**95%** sim conveyor SR | the inverse freeze — one side is still always held fixed, never co-evolution |
| [[2605.15153\|Pelican-Unified]] | shared latent $z$, multi-stage training | latent | **93.5%** [[2504.13059\|RoboTwin]] | unifies the architecture but trains in stages, not one loop |
| [[2504.02792\|UWM]] | unified action-conditioned + video diffusion | pixel | one model for action + video | high latency from pixel diffusion; not a single latent gradient |
| [[2602.10098\|VLA-JEPA]] | pure latent JEPA WM + separate action head | latent | **97.2%** [[2306.03310\|LIBERO]] at ~10 ms | the heads are separate — the joint loss is never closed |
| [[2606.01027\|τ0-WM]] | shared video-diffusion backbone for video-action + simulator | pixel | **+17%** unseen-task SR | pixel-space backbone, not a single latent gradient |
| [[2606.01955\|WALL-WM]] | layer-coupled video-action denoiser, multi-stage | pixel | Task Progress **53.75**; learns semantic action events | joint but multi-stage and pixel-space — not one cooperative loop |
| [[2602.10717\|SDA]] | distilled-Cosmos WM imagines keyframes, in-context action model | pixel | **98.1%** [[2306.03310\|LIBERO]] | imagine-then-act (cascaded), not a joint objective |
| [[2511.07732\|ViPRA]] | jointly predicts future visual states + latent actions, then flow-matches | latent | control at **22 Hz** | A1's joint objective, but learned offline, not in a closed RL loop |
| [[2605.13775\|RoboEvolve]] | co-evolves a planner + a video simulator | pixel | beats a 25K-demo SFT baseline from 300 seed images | co-evolution but *alternating* — the schedule A1 replaces |
| [[2606.04130\|CLAW (Latent Action WM)]] | joint latent-action + diffusion-WM, reciprocal supervision | latent | adversarial regularization blocks collapse | the anti-collapse substrate A1 needs, but not yet a GRPO loop |
| [[2606.05979\|WLA]] | joint action + world + language experts, world prediction implicit | latent | **56.5%** RMBench, ~40 ms | joint-loss and latent-cheap, but one-pass, not co-evolving |
| [[2603.10448\|DiT4DiT]] | video DiT conditions an action DiT via denoising features | pixel | **98.6%** [[2306.03310\|LIBERO]], **10×** sample efficiency | pixel-space, not a single latent gradient |
| [[2604.11135\|AIM]] | jointly predicts action-value maps + future RGB, two-stage | pixel | **+15.3 pp** RoboTwin Hard over π0.5 | joint but two-stage, and the imagination is rendered |
| [[2603.10422\|World2Act]] | latent-action post-training aligns actions to WM dynamics latents | latent | **66.3%** RoboCasa with fewer demos | latent-joint, but post-hoc alignment, not a co-evolving loop |
| [[2603.25406\|MMaDA-VLA]] | single masked-denoising over goal observation + action, no aux WM | latent (discrete) | **98.0%** [[2306.03310\|LIBERO]], **4.78** CALVIN | the single-objective joint variant — but supervised offline, not GRPO-co-evolved |
| [[2603.08403\|SPIRAL]] | critic filters hallucinated dynamics before they corrupt the policy | latent | the dream-quality gate for the co-evolution loop | a gate, not the loop itself — pairs with A1 rather than realizing it |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a single cooperative gradient beats alternating on a shared latent backbone), with the experiment and the Related-table row it lands on.
1. **H1 — A single joint GRPO gradient beats alternating on the same backbone.**
   - *Prediction*: $\mathcal{L} = \mathbb{E}[A \cdot \log \pi(a, \hat z_{t+1} \mid s_t)]$ updating both heads in one backward pass over a pretrained latent WAM ([[2504.02792|UWM]] / [[2602.10098|VLA-JEPA]]) beats [[2602.12063|VLAW]]-style alternation on *both* ≥97.2% in-dist and ≥79.5% OOD [[2510.13626|LIBERO-Plus]].
   - *Test*: hold the backbone and data fixed; swap only the update schedule (joint single-pass vs alternating); report both SR axes.
   - *Row*: VLAW (alternating).
   - *Falsifier*: alternation matches or beats the joint pass on either axis → staged training is not just a legacy.
2. **H2 — A latent-consistency reward supplies the dense signal task reward lacks.**
   - *Prediction*: adding a latent-consistency term ($\hat z_{t+1}$ vs the encoder's $z_{t+1}$) to the task + action-quality reward improves OOD SR more than task reward alone, because the latent gives a per-step signal sparse outcome reward cannot.
   - *Test*: ablate the latent-consistency term on the joint loop; report OOD-SR delta and per-step credit-assignment density.
   - *Row*: VLA-JEPA (separate heads) / MMaDA-VLA (single-objective).
   - *Falsifier*: task-reward-only matches the consistency-augmented loop → the latent reward is redundant.
3. **H3 — Stop-gradient from action to the WM encoder preserves pretrained physics priors.**
   - *Prediction*: extending knowledge-insulation's stop-gradient from action→VLM to action→WM-encoder keeps the joint loop's OOD SR above an un-insulated variant, which drifts as the action loss corrupts the pretrained dynamics latent.
   - *Test*: train joint loops with and without action→encoder stop-gradient; track OOD SR and encoder-feature drift over training.
   - *Row*: SRPO (frozen V-JEPA 2) — the fully-frozen extreme the insulated loop relaxes.
   - *Falsifier*: the un-insulated loop matches the insulated one → the action gradient does not corrupt the WM encoder.
4. **H4 — Latent rollout makes the joint loop run at no latency cost vs pixel co-training.**
   - *Prediction*: a latent backbone ([[2602.10098|VLA-JEPA]] ~10 ms) closes the joint loop at inference latency indistinguishable from a policy-only baseline, while a pixel-space joint loop ([[2603.19370|VAMPO]] / [[2606.01027|τ0-WM]]) pays ~150 ms.
   - *Test*: profile per-step inference latency of latent vs pixel joint loops at matched accuracy.
   - *Row*: VAMPO (pixel) / τ0-WM (pixel) vs VLA-JEPA (latent).
   - *Falsifier*: the latent loop's latency is not below the pixel loop's at matched accuracy → latent buys no deployment advantage.
5. **H5 — A shared latent makes the joint loop co-evolve where a frozen-WM loop plateaus.**
   - *Prediction*: letting the WM update inside the loop (vs [[2511.09515|WMPO]]'s frozen-WM inner loop) widens the OOD margin over training, because the imagination target tracks the improving policy instead of a fixed model.
   - *Test*: compare frozen-WM vs co-evolving-WM inner loops on the same backbone; plot OOD SR vs training steps.
   - *Row*: WMPO (WM frozen) / AHEAD (policy frozen).
   - *Falsifier*: the frozen-WM loop matches the co-evolving one at convergence → freezing one side costs nothing.
6. **H6 — Real-robot transfer survives deploying only the policy (WM stays sim-only).**
   - *Prediction*: a LoRA-on-frozen-WM-base policy transfers to a real robot with the WM and any failure-finder kept sim-only, since only the policy is deployed — retaining the joint loop's training gain without paying its imagination cost at runtime.
   - *Test*: deploy the policy head alone on a real platform; compare real SR to a policy trained without the joint loop.
   - *Row*: SDA (imagine-then-act) — the cascaded baseline that needs the imagination at runtime.
   - *Falsifier*: real SR matches the non-joint baseline → the joint loop's gain does not survive deploying the policy alone.

> [!warning] Risks
> - **Optimization instability** — a discrete action head, a continuous latent, and an adversarial finder have conflicting gradients. → Balance with separate loss weights + EMA targets; run H1 on a frozen WM first to isolate the action-head gradient.
> - **Chasing problem** — simultaneous updates let the WM model an obsolete policy. → EMA target networks decouple the imagination target from the live policy (the mechanism H5 measures).
> - **Reward hacking on latent consistency** — gameable by collapsing the latent. → [[2511.08544|LeJEPA]]'s Euclidean anti-collapse regularization defends; [[2604.27998|Latent-GRPO]]'s failure-mode patches apply (tied to H2's falsifier).

### A2 — Causally-Important Step Rewards for Latent Policy Reasoning

| | |
|---|---|
| **Cluster** | A — Architecture & Training |
| **Thesis** | Put step rewards on *latent* reasoning tokens. An outcome reward binds the agent to the result, not the path, so it cannot tell a causally-correct reasoning path from a lucky one that lands the same outcome — to shape reasoning the reward must act on intermediate states. The field assumes you must choose between latency-free latent CoT and step-level supervision. The bet is in First-principles below. |
| **Anchor papers** | [[2509.19012\|Pure VLA Survey]] (survey), [[2510.04978\|Physical AI Survey]] (survey), [[2509.25373\|VLM Perception-Cognition Survey]] (survey), [[2604.18486\|OneVL]] (method), [[2604.22074\|CIR/SR Reasoning]] (method), [[2510.16281\|SEAL]] (benchmark) |
| **Key targets** | ≥+5 pp SR on LIBERO-Long at matched latency; ≥+10 pp on compositional (vs [[2510.16281\|SEAL]]'s **+15 pp** novel-behavior-composition gain to 53%) |

**Why it matters.**
- **The gap**: an outcome reward scores two reasoning paths identically if they reach the same result, so RL-trained traces become "factually correct via causally disconnected paths" ([[2604.22074|CIR/SR Reasoning]]) — and explicit chain-of-thought pays a per-token latency cost a closed-loop policy cannot afford.
- **Today's answers**: the two halves exist but uncombined — [[2604.18486|OneVL]] shows latent reasoning beats explicit CoT at answer-only latency (**88.84** PDM-score, **+2.64 pts** over an 8B baseline); [[2604.22074|CIR/SR Reasoning]] shows step rewards fix causal disconnection but is demonstrated on *written* reasoning; [[2510.16281|SEAL]] documents the CoT-faithfulness gap as a runtime problem. No paper pairs latent (unwritten) CoT with step-reward training for policy reasoning.
- **The opening**: [[2606.02277|RoboSemanticBench]] makes the failure mode measurable — **89.93%** of grasp-success/task-failure cases reasoned correctly yet acted wrong, the "causally-disconnected path" in benchmark form, giving the step-reward gain a faithfulness target to move.

**First-principles framing.**
- **First principle**: Outcome rewards bind the agent to the *result*, not the *reasoning path*. Two paths that reach the same outcome score the same, even if only one is causally correct. To shape reasoning, the reward must act on intermediate states, not just the terminal one.
- **Assumption being challenged**: That you need an explicit, written-out chain-of-thought to supervise reasoning. [[2604.22074|CIR/SR Reasoning]]'s step rewards work on *latent* (unwritten) reasoning tokens too, so [[2604.18486|OneVL]]'s latent CoT can take the same step-by-step supervision without the extra tokens — and the latency — that spelling the reasoning out would cost at inference. [[2407.08693|ECoT]] and [[2604.17800|ReFineVLA]] bet the opposite, distilling *explicit* text reasoning.
- **The bet**: Latent CoT + step rewards gets ≥+5 pp SR on LIBERO-Long at matched latency and ≥+10 pp on compositional benchmarks, closing the faithfulness gap [[2510.16281|SEAL]] documented (its **+15 pp** to 53% novel-behavior composition is the bar).

**Related research papers.**

Twenty systems that supervise reasoning differently — explicit-text CoT, visual/sketch intermediates, latent reasoning, test-time search, or step-vs-outcome reward — none pairing *latent* CoT with *step-reward* training. The axis is *where the reasoning lives and what signal shapes it*:

| System | Reasoning form | Reward / supervision | Key result | What's missing |
|---|---|---|---|---|
| [[2604.18486\|OneVL]] | latent (dual-decoder) | answer-only (no step) | **88.84** PDM-score, **+2.64 pts**; answer-only latency | the latent substrate A2 bolts step rewards onto — but no step signal yet |
| [[2604.22074\|CIR/SR Reasoning]] | explicit step trace | step reward (causal importance) | outcome rewards insufficient — "causally disconnected paths" | demonstrated on *written* reasoning, not latent tokens |
| [[2604.27998\|Latent-GRPO]] | latent | RL with 3 failure-mode patches | stabilizes latent RL | stabilization, not a causal-importance step reward |
| [[2510.16281\|SEAL]] | explicit (verified) | runtime CoT-faithfulness verifier | **+15 pp** compositional to 53% | a runtime verifier, not a training signal — A2 trains what SEAL checks |
| [[2606.02277\|RoboSemanticBench]] | diagnostic | — (measurement) | **89.93%** reasoned-right-acted-wrong | the faithfulness benchmark A2's gain must move, not a method |
| [[2606.03784\|ERVLA]] | explicit AR CoT (+ dropout) | 226M-sample corpus, CoT-dropout | explicit AR CoT *doesn't* scale | empirical backing for A2's latent direction — explicit is the wrong axis |
| [[2606.04436\|3DThinkVLA]] | latent reasoning-anchor token | distilled 3D *thinking* (no text) | **98.7%** LIBERO | the anchor mechanism A2 builds on — but distillation, not step reward |
| [[2512.22939\|ColaVLA]] | meta-action embeddings (latent) | relocated text CoT | **>5×** faster than text CoT (727 ms vs >3700 ms) | latent-reasoning substrate at driving scale, no step-reward training |
| [[2606.03127\|TTT-VLA]] | latent prompt (test-time) | self-supervised state-grounding | SimplerEnv **51.1% → 67.4%** | latent reasoning shaped by a non-outcome signal — but test-time only |
| [[2509.22643\|VLA-Reasoner]] | explicit (MCTS over WM) | value network scores intermediate states | **+19 pp** real SR | A2's dense-intermediate-feedback via search, not a learned step reward |
| [[2506.21669\|SEEA-R1]] | agent reasoning | MCTS → dense step Q-values | sparse→dense reward at agent level | the "sparse → dense" mechanism, but not on latent policy tokens |
| [[2509.25681\|dVLA]] | multimodal CoT (co-masked) | one diffusion objective | **+6.6 pp** from CoT at ~2× speed | reasoning in one objective, but visual+text, not latent step rewards |
| [[2605.13632\|GTA-VLA]] | async spatial CoT | "slow reason, fast act" | **98.6%** [[2306.03310\|LIBERO]] | the reasoning/latency decoupling A2 targets, no step-level reward |
| [[2601.01618\|Action-Sketcher]] | visual-sketch intermediate | token-gated reason↔act | **96.0%** LIBERO-Long | visual-intermediate variant, not latent tokens with step rewards |
| [[2604.17800\|ReFineVLA]] | explicit language rationale | teacher-distilled selective FT | **+9.6%** SimplerEnv | the explicit-CoT-distillation baseline A2's latent approach must beat |
| [[2407.08693\|ECoT]] | explicit grounded CoT | full plan→box→gripper trace | **+28 pp** SR, one correction **+48 pp** | the explicit-step baseline A2's latent variant must beat at lower latency |
| [[2412.11974\|EMMA-X]] | grounded look-ahead CoT | per-step grounding (gripper + 3D plan) | **+24.17%** SR; ablating it drops **43–55%** | per-step grounding as the dense signal — but explicit, costing latency |
| [[2603.28730\|SOLE-R1]] | spatiotemporal CoT | per-timestep RLVR as *sole* signal | from-random-init on-robot RL ≥**50%** on 24 unseen | dense + hack-resistant step reward, but explicit, not latent |
| [[2604.28192\|LaST-R1]] | adaptive latent reasoning | RL | adaptive physical latent reasoning | the substrate step rewards bolt onto — no causal-importance predicate |
| [[2605.02735\|Silenced Visual Latents]] | latent (diagnostic) | — (probe) | latents can be "semantically rich but functionally ignored" | the diagnostic warning — latent reasoning can be present yet unused |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (latent CoT + step rewards beats outcome-only and explicit-CoT at matched latency), with the experiment and the Related-table row it lands on.
1. **H1 — Step rewards on latent tokens beat outcome-only RL at matched latency.**
   - *Prediction*: exposing [[2604.18486|OneVL]]'s K=8 latent tokens and training $\mathcal{L} = \lambda_a \mathcal{L}_{\text{action}} + \lambda_s \sum_i r_{\text{step},i}(z_i)$ with per-token subgoal predicates gets ≥+5 pp SR on LIBERO-Long over vanilla OneVL and over outcome-only RL, at answer-only latency.
   - *Test*: build LIBERO-Subgoals (130 tasks → 3–7 verifiable subgoals each, auto-generated via [[2503.15558|Cosmos-Reason1]] LLM-as-judge, validated on a 100-subgoal gold set at κ > 0.7); train with step rewards vs outcome-only; report SR + latency.
   - *Row*: OneVL (latent, answer-only) / CIR/SR Reasoning (step reward, explicit).
   - *Falsifier*: outcome-only RL matches the step-reward variant → the path signal adds nothing on latent tokens.
2. **H2 — The latent tokens are functionally used, not just present.**
   - *Prediction*: a Latent Utilization Index (normalized action $L_2$ distance between $a(\mathbf z)$ and $a(\mathbf z + \epsilon)$) exceeds 0.3 under step-reward training but stays near zero for outcome-only — i.e., step rewards force the latents to drive the action, fixing [[2605.02735|Silenced Visual Latents]]' "rich but ignored" failure.
   - *Test*: probe LUI before/after step-reward training; correlate LUI with SR gain.
   - *Row*: Silenced Visual Latents (latent diagnostic).
   - *Falsifier*: LUI stays low while SR rises → the gain isn't coming from the latent reasoning.
3. **H3 — Compositional generalization moves where explicit-CoT distillation plateaus.**
   - *Prediction*: training on simple instructions and testing compositions ("open drawer + place red mug") gets ≥+10 pp on [[2603.28301|LIBERO-Para]] / [[2510.13626|LIBERO-Plus]] with ≤−3 pp in-dist, beating [[2604.17800|ReFineVLA]]'s explicit-rationale distillation at matched backbone.
   - *Test*: head-to-head latent-step-reward vs explicit-CoT-distillation on paraphrase/compositional splits.
   - *Row*: ReFineVLA (explicit distillation) / SEAL (verified compositional).
   - *Falsifier*: explicit distillation matches or beats the latent-step variant on compositional → spelling reasoning out is required.
4. **H4 — Latent CoT keeps the reasoning gain at a fraction of explicit-CoT latency.**
   - *Prediction*: across {ID, OOD, Compositional}, latent CoT + step rewards (~0 ms reasoning) retains the accuracy of explicit grounded CoT ([[2407.08693|ECoT]] / [[2412.11974|EMMA-X]], ~1.2 s) while costing the latency of [[2604.18486|OneVL]] / [[2512.22939|ColaVLA]] (≤ a few ms), not the explicit trace.
   - *Test*: ablate explicit CoT vs [[2604.22709|Abstract-CoT]] (~50 ms) vs OneVL (~0 ms) vs OneVL+step-rewards (~0 ms); report SR and latency per regime.
   - *Row*: ECoT (explicit) / EMMA-X (explicit grounded) vs OneVL (latent) / ColaVLA (latent meta-action).
   - *Falsifier*: the latent variant's accuracy drops below the explicit one at matched task → the latency saving costs the reasoning gain.
5. **H5 — A learned causal-importance step reward beats search-derived dense feedback at runtime cost.**
   - *Prediction*: a trained step reward matches [[2509.22643|VLA-Reasoner]]'s MCTS-over-WM intermediate scoring (**+19 pp** real) on accuracy while avoiding its test-time search cost, because the dense signal is amortized into the weights.
   - *Test*: compare learned-step-reward vs test-time-MCTS at matched accuracy; report inference cost.
   - *Row*: VLA-Reasoner (MCTS search) / SEEA-R1 (MCTS dense Q).
   - *Falsifier*: the learned step reward cannot match search accuracy → dense feedback needs runtime search, not training.

> [!warning] Risks
> - **Predicate scaling** — hand-authoring subgoals is brittle; LLM-as-judge fallback re-introduces the verification cost step rewards avoid. → Validate auto-generated predicates against a κ > 0.7 gold set (H1) before scaling.
> - **Reward hacking** — models can satisfy predicates trivially. → [[2509.15194|EVOL-RL]] novelty diversity + the LUI probe (H2) catch trivial satisfaction.
> - **Compositional generalization may be unsolved at this scale** — [[2510.16281|SEAL]] documented this exact failure mode. → Bound the compositional claim (H3) to [[2603.28301|LIBERO-Para]]-style paraphrase novelty rather than unbounded composition.

### A3 — Verifiable Physics-Consistent Training for Open-World Policy Generation

| | |
|---|---|
| **Cluster** | A — Architecture & Training |
| **Thesis** | Enforce verifiable physics predicates at the *action* level, not just the generated-video level. Physical laws (momentum, gravity, friction, contact) are checkable and hold the same for held-out and OOD data, so a loss enforcing them extrapolates without distribution shift. The field assumes a physics-aware video generator hands you a physics-aware *policy* for free. The bet is in First-principles below. |
| **Anchor papers** | [[2604.04974\|Video-to-Control Survey]] (survey), [[2503.21765\|Physics Cognition Survey]] (survey), [[2510.04978\|Physical AI Survey]] (survey), [[2604.17896\|Physical-Feasibility VLA]] (method), [[2605.08567\|ACWM-Phys]] (benchmark), [[2603.23376\|ABot-PhysWorld]] (method) |
| **Key targets** | obstacle-perturbation Safe-SR **43.50% → >55%** ([[2604.17896\|Physical-Feasibility VLA]]'s geometric-only action-level ceiling); sim-to-real SR retention **≥0.70**; DPO pass-target **≥90%** on held-out via [[2603.23376\|ABot-PhysWorld]] physics-rejected negatives; non-trivial $\rho(\sum P_i,\ \text{task SR})$ |

**Why it matters.**
- **The gap**: physical laws are universal and checkable, yet policies are trained with empirical losses that only trust the samples they saw — so the generation-side progress on physics-aware video does not obviously reach the *chosen action*, and the imagination→policy chain is untested end-to-end.
- **Today's answers**: physics-aware video generators ([[2509.21309|NewtonGen]], [[2510.13809|PhysMaster]], [[2512.00425|NewtonRewards]], [[2603.13770|PhysAlign]]) progress on the *generation* side; on the action side, the closest is [[2604.17896|Physical-Feasibility VLA]] — a differentiable *geometric* loss on actions that lifts obstacle-perturbation Safe-SR ($\Pr(d_{\min} > \alpha \wedge d_{\text{tgt}} < \beta)$) from 22% → **43.50%**, but it is geometric-only, with no verifiable physics predicates and no [[2510.13626|LIBERO-Plus]] eval.
- **The opening**: [[2605.08567|ACWM-Phys]] *quantifies* the cliff the whole chain leaks through — action-conditioned video WMs are crisp in-distribution (SSIM **0.988**) but degrade sharply OOD (ΔM-MSE up to **+40** on robot-arm, **+30** on cloth) — so even the first step already leaks, making action-level physics a measurable axis to fix rather than assume.

**First-principles framing.**
- **First principle**: Physical laws (momentum, gravity, friction, contact) are universal and checkable, and they don't depend on the training set — they hold for held-out and OOD data alike. A loss that enforces them keeps working off-distribution, unlike ordinary losses that only trust the samples they saw.
- **Assumption being challenged**: That a video generator which respects physics hands you a *policy* that respects physics for free. That hand-off — from physics in the generated video to physics in the chosen action — is assumed but never measured end-to-end; [[2605.08567|ACWM-Phys]] shows even the first step already leaks OOD, so the rest can't be assumed intact. The generation-side physics work ([[2509.21309|NewtonGen]], [[2510.13809|PhysMaster]]) bets the chain transfers; nobody has measured it to the action.
- **The bet**: Physics predicates at the *action* level lift obstacle-perturbation Safe-SR from **43.50% → >55%** ([[2604.17896|Physical-Feasibility VLA]]'s geometric-only Safe-SR is the baseline) and reach ≥0.70 sim-to-real SR retention (physics-naive: 0.50–0.60), making physics-consistent action a measurable axis, not a generation-side correlate.

**Related research papers.**

Eleven systems that put physics somewhere in the pipeline — in the generated video, in a preference signal, in a learned physical WM, in the gradient estimator, or in the action — none with a *verifiable predicate set enforced on the action sequence*. The axis is *where physics is enforced and whether it reaches the action*:

| System | Physics enforced | Reaches the action? | Key result | What's missing |
|---|---|---|---|---|
| [[2605.08567\|ACWM-Phys]] | scored on action-conditioned WM rollouts | measures, doesn't enforce | InD SSIM **0.988**, OOD ΔM-MSE up to **+40** | the eval substrate that quantifies the cliff — not a training fix |
| [[2604.17896\|Physical-Feasibility VLA]] | differentiable *geometric* loss on actions | yes — geometric only | **22 → 43.50%** Safe-SR | geometric, not physics; no verifiable predicates, no LIBERO-Plus |
| [[2603.23376\|ABot-PhysWorld]] | Diffusion-DPO with physics-rejected negatives | yes — via preference | the bridge from generation to action | preference signal, not a per-step verifiable predicate over the trajectory |
| [[2509.21309\|NewtonGen]] | physics-aware video generation | no — generation only | physics-consistent video | the action chain is untested — generation respects physics, the policy may not |
| [[2512.00425\|NewtonRewards]] | reward-shaped physics video | no — generation only | physics rewards on generation | documents reward hacking on the *generation* side — the action-side analog is likely |
| [[2510.13809\|PhysMaster]] / [[2603.13770\|PhysAlign]] | physics-aligned video | no — generation only | improved physical realism | no WAM-state path — physics never enters the chosen action |
| [[2509.20570\|PIRF]] | PDE residual rewards | no — generation only | physics via residuals | generation-side; verifiable physics scales poorly to cluttered scenes |
| [[2511.07416\|PhysWorld]] | learned physical WM (positions/velocities) | indirectly via WM | **82%** real SR | a physical WM, but positions/velocities only — no momentum/contact predicates |
| [[2605.06593\|ReActor]] | bilevel RL + physics sim | motion-retargeting only | **+15.22 pp** | physics in retargeting, not in a manipulation-action predicate set |
| [[2605.15298\|PhysBrain]] | physics-aware policy from egocentric | yes — implicit | closest physics-grounded policy | no *verifiable* predicate set — physics is learned, not checked |
| [[2604.18161\|DDCG]] | contact/friction-aware gradient estimator | yes — training-time | unified `c=0.3` 0th/1st-order switching | the differentiable-physics gradient substrate A3 trains *through*, not the predicate set |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (verifiable action-level physics predicates extrapolate where geometric/generation-side losses don't), with the experiment and the Related-table row it lands on.
1. **H1 — Verifiable physics predicates over actions lift the Safe-SR ceiling past geometric-only.**
   - *Prediction*: five binary predicates — P1 momentum ($|\Delta p_{\text{total}}| < 0.05\,p_{\max}$ off-contact), P2 no inter-object penetration (signed-distance > 0), P3 free-flight $\Delta z \sim -\tfrac12 g t^2 \pm 10\%$, P4 Newton's-3rd-law on contact wrenches, P5 Coulomb friction ($|F_t| \le \mu|F_n|$) — added as a differentiable training loss lift obstacle-perturbation Safe-SR from **43.50%** to **>55%**, beating [[2604.17896|Physical-Feasibility VLA]]'s geometric-only loss.
   - *Test*: instrument 50 [[2306.03310|LIBERO]] + 30 [[2502.16707|ReflectVLM]] long-horizon tasks (~4,000 labeled trajectories); compare predicate-loss vs geometric-loss on a [[2604.17896|Physical-Feasibility VLA]]-style obstacle gauntlet; track plain SR on [[2510.13626|LIBERO-Plus]] separately.
   - *Row*: Physical-Feasibility VLA (geometric, reaches action).
   - *Falsifier*: predicate loss ≤ 43.50% Safe-SR → verifiable physics on actions adds nothing over geometric.
2. **H2 — The interface where physics enters (implicit/abstract/explicit) changes Safe-SR at matched FLOPs.**
   - *Prediction*: per the [[2604.04974|Video-to-Control Survey]] taxonomy, an explicit physics-predicate interface beats implicit and abstract interfaces on the obstacle + physics gauntlet at matched FLOPs, with latent within ±2 pp at lower latency.
   - *Test*: same backbone, three interfaces, matched FLOPs; report Safe-SR on the gauntlet + [[2605.08567|ACWM-Phys]] OOD splits.
   - *Row*: ACWM-Phys (measures the OOD cliff the interface must close).
   - *Falsifier*: implicit matches explicit → the interface is not the lever and physics can stay latent.
3. **H3 — Physics-rejected preference negatives generalize to held-out via DPO.**
   - *Prediction*: ~10k preference pairs of physically-rejected vs accepted actions, trained with Diffusion-DPO, satisfy $\beta(\log p_\theta(a_+) - \log p_\theta(a_-)) > 0$ on ≥90% of 1k held-out (baseline ~74%), via [[2603.23376|ABot-PhysWorld]] negatives.
   - *Test*: train DPO on [[2603.23376|ABot-PhysWorld]]'s physics-rejected negatives; measure held-out preference accuracy.
   - *Row*: ABot-PhysWorld (preference bridge).
   - *Falsifier*: held-out pass-rate ≤ baseline → preference physics does not generalize off the training pairs.
4. **H4 — Physics-consistent action retains sim-to-real SR where physics-naive policies lose it.**
   - *Prediction*: a policy trained with action-level physics predicates holds SR retention ≥0.70 across sim → twin → real on [[2511.04665|Real-to-Sim GS]] soft-body twins (12 cloth/rope/dough), vs 0.50–0.60 for a physics-naive policy.
   - *Test*: eval sim → twin → real retention with and without the predicate loss.
   - *Row*: Real-to-Sim GS (sim-real twin substrate, off-table).
   - *Falsifier*: physics-naive retention matches → physics consistency does not survive the real gap.
5. **H5 — Predicate satisfaction correlates with downstream SR (the chain is real, not hacked).**
   - *Prediction*: a regression of $\sum_i P_i$ against task SR shows a non-trivial positive $\rho$, and static-output reward-hacking is detectable (σ drop > 2×) under periodic [[2412.02818|RoboMD]] adversarial probing — i.e., satisfying physics actually predicts success rather than gaming the predicates.
   - *Test*: fit $\rho(\sum P_i, \text{SR})$; run static-output and [[2412.02818|RoboMD]] hacking diagnostics; apply [[2509.15194|EVOL-RL]] novelty diversity as the defense.
   - *Row*: ACWM-Phys (OOD physics measurement) — the cliff the correlation must hold across.
   - *Falsifier*: $\rho$ near zero → physics-consistent imagination ≠ physics-consistent action, and the direction collapses (the go/no-go).

> [!warning] Risks
> - **Verifiable physics scales poorly** ([[2509.20570|PIRF]]) — predicates for cluttered scenes are hard. → Start with [[2605.08567|ACWM-Phys]]'s low-dimensional clean-structure tasks where predicates are tractable, then expand.
> - **Physics-consistent imagination ≠ physics-consistent action** — this is the gap to test; if it's small, the direction collapses. → H5's Pearson $\rho$ between $\sum P_i$ and SR is the go/no-go before scaling.
> - **Reward hacking** — [[2512.00425|NewtonRewards]] documented it on the generation side; the action-side analog (model freezes) is likely. → Static-output detection (σ drop > 2×) + [[2509.15194|EVOL-RL]] novelty diversity defend (tied to H5).

---

## Cluster B — Evaluation, Robustness & Deployment: From Trained to Deployed

*Everything that stands between a trained policy and reliable deployment: measuring whether imagination and action are causally bound (B1), recovering when it fails with memory (B2), running it in real time on edge hardware (B3), and not forgetting what it knew under continual fine-tuning (B4).*

### B1 — Joint Policy/World-Model Evaluation: Causal Consistency Between Imagination and Action

| | |
|---|---|
| **Cluster** | B — Evaluation, Robustness & Deployment |
| **Thesis** | Measure the world model and policy on one joint causal-consistency axis, not two separate ones (WM quality via FVD/PSNR, action quality via SR). A WM and a policy are causally bound only when the action taken in an imagined future matches the executed one — a property visual fidelity cannot see. The field assumes the visual fidelity of WM-generated futures predicts policy success. The bet is in First-principles below. |
| **Anchor papers** | [[2605.12090\|WAM Survey]] (survey), [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2310.06253\|Objective Mismatch MBRL Survey]] (survey), [[2606.05773\|PiL-World]] (method), [[2606.04463\|OSCAR]] (method), [[2605.06311\|VISER]] (benchmark) |
| **Key targets** | ASR + COD → real SR Pearson **ρ > 0.7** (separate axes: ρ < 0.4); the joint metric replaces FID-style WM eval |

**Why it matters.**
- **The gap**: current protocols score WM quality (FVD/PSNR) and action quality (SR) *separately*, so a joint model can score high on each while imagination and actions are causally disconnected — and [[2310.06253|Objective Mismatch MBRL Survey]] gives the MBRL substrate showing predictive WM loss doesn't correlate with downstream return.
- **Today's answers**: the correlation *is* recoverable once you measure it right — [[2605.06311|VISER]] hits sim-real Pearson **r = 0.92** with controlled fidelity; [[2606.05773|PiL-World]] closes the imagined-vs-real SR gap **63.2% → 12.0%** (Pearson **0.94**); [[2606.04463|OSCAR]] tracks real-fleet rankings at **r = +0.852** (MAE **1.73 pp**). But [[2603.22078|WAM vs VLA Robustness]] shows world-action models win on visual perturbation while running **4.8×** slower — a cost worth paying only if imagination helps action quality, which separate metrics can't certify.
- **The opening**: [[2604.21686|WorldMark]] shows looking-real (FID/FVD) and being-physically-consistent are *unrelated*, and [[2605.28527|VLA Value Probing]] reads a value-like signal straight from a *frozen* policy's features (R² ≈ 0.55, value-guided selection **+17.67 pp**) — so the success signal the joint metric certifies may already live in the policy, not in a separate WM.

**First-principles framing.**
- **First principle**: A world model and a policy are truly linked only when the actions taken in *imagined* futures match the actions taken in *executed* ones. If you never measure that link directly, the "world-model quality" score and the "policy SR" score can both climb while the combined skill goes nowhere — each metric gets gamed on its own.
- **Assumption being challenged**: That how real the generated futures *look* (FID, FVD) tells you whether the policy will succeed. [[2604.21686|WorldMark]] shows it's *wrong* — looking good and being physically consistent are unrelated — and [[2605.21800|stable-worldmodel]] shows planning SR collapses under perturbation even when in-distribution visual SR is 92–94%; yet FID-style metrics persist.
- **The bet**: ASR + COD *jointly* predict real-fleet SR at Pearson **ρ > 0.7**, far above the ρ < 0.4 ceiling of separate-axes evaluation (ρ < 0.4 is the contrast baseline the experiment must establish, not a paper-reported number) — making the pair the practical replacement for current WM eval.

**Related research papers.**

Sixteen evaluation systems that measure something — WM fidelity, controllability, closed-loop correlation, real-fleet ranking, or statistical validity — none scoring *WM↔action causal binding* directly. The axis is *what the eval measures and whether it certifies the imagination↔action link*:

| System | What it measures | Joint causal axis? | Key result | What's missing |
|---|---|---|---|---|
| [[2603.22212\|Omni-WorldBench]] | interaction-centric WM via counterfactual probes | WM-only | first counterfactual WM eval | scores the WM alone — never the action it should drive |
| [[2603.23497\|WildWorld]] | Action Following + State Alignment | WM-only (large-scale) | 108M Monster Hunter frames | game-domain WM metrics, no policy-success binding |
| [[2510.10125\|CTRL-WORLD]] | controllability for manipulation | WM-only | controllability score | controllability ≠ causal binding to executed actions |
| [[2603.22078\|WAM vs VLA Robustness]] | robustness grid (WAM vs VLA) | separate axes | **4.8×** latency cost | measures both axes separately — the cost-vs-benefit it can't resolve |
| [[2605.21800\|stable-worldmodel]] | reproducible OOD WM harness | WM planning-only | [[2603.19312\|LeWM]] 94% / [[2411.04983\|DINO-WM]] 92% [[2109.00137\|Push-T]], decays under occlusion | the perturbation substrate — planning SR, not action-causality |
| [[2605.06311\|VISER]] | sim-real visual-fidelity correlation | fidelity, not causality | **r = 0.92**, 1,000+ PBR objects | existence proof the correlation is recoverable — but visual, not causal |
| [[2606.05773\|PiL-World]] | closed-loop imagined-vs-real SR | closed-loop correlation | Pearson **0.94**, gap 63.2→12.0% | correlates closed-loop, but evaluates rather than certifies causal binding |
| [[2606.04463\|OSCAR]] | virtual vs real-fleet policy ranking | correlation via conditioning | **r = +0.852**, MAE **1.73 pp** | ranks via skeleton conditioning, not an action-causality metric |
| [[2605.25874\|WBench]] | multi-turn interactive video-WM | WM-only | 289 cases, 22 sub-metrics; nav drops 33 pts Turn-1→4+ | the substrate B1 adds an action-causality axis to |
| [[2604.21686\|WorldMark]] | looks-real vs physically-consistent | decoupling diagnostic | fidelity and consistency *unrelated* | proves FID is the wrong predictor — but offers no replacement metric |
| [[2605.28527\|VLA Value Probing]] | value signal from a frozen policy | policy-internal | R² ≈ 0.55, **+17.67 pp** value-guided | the signal may live in the policy, not a separate WM — needs a metric |
| [[2605.26379\|LeJEPA World Model]] | when a latent encodes the true world | theory | oracle planning R² > 0.999 iff isotropic-Gaussian | the theory of *when* B1's latent is trustworthy, not a benchmark |
| [[2606.05159\|X4Val]] | variance-reduced policy eval | statistical layer | **38.4%** variance cut from non-paired data | the statistical-validity layer a joint metric needs, not the metric |
| [[2605.29710\|PhAIL]] | time-to-success CDF + KS test | statistical rigor | **80%** detection at N=25-30 vs binary at N=30 | adds statistical rigor, but still binary success, not causal binding |
| [[2606.04233\|Manipulation Benchmark Audit]] | significance of SR claims | meta-eval | 0.09B [[2304.07193\|DINOv2]]+MLP hits **99.0%** LIBERO-Spatial; only **19.8%** of claims significant | shows current SR certifies the wrong thing — the motivation, not a fix |
| [[2510.04354\|SureSim]] | prediction-powered real/sim inference | statistical layer | **−20–25%** real-hardware effort | the statistical layer for the joint metric, not the causality axis |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a joint causal-consistency metric predicts real SR where separate axes don't), with the experiment and the Related-table row it lands on.
1. **H1 — A counterfactual-probe causal metric beats FID-style WM eval at predicting real SR.**
   - *Prediction*: a metric that samples $a'_t$, generates $\hat s'_{t+1}$, and requires $\|\hat s_{t+1} - \hat s'_{t+1}\|$ to scale monotonically with $\|a_t - a'_t\|$ (on [[2304.07193|DINOv2]] features) predicts real-fleet SR better than FID/FVD on the same models.
   - *Test*: compute the causal metric + FID on a fixed WAM set; regress each against real SR ([[2603.13966|vla-eval]] reference harness).
   - *Row*: WorldMark (fidelity-vs-consistency decoupling) / VISER (visual correlation).
   - *Falsifier*: FID predicts real SR as well as the causal metric → fidelity already certifies action quality.
2. **H2 — ASR + COD jointly clear ρ > 0.7 where separate sub-scores stay below 0.4.**
   - *Prediction*: ASR (action success in imagination) + COD (counterfactual outcome deviation) *together* predict real SR at Spearman ρ > 0.7, while L1/L2/L3 sub-scores ([[2604.22748|Agentic World Modeling Survey]]) used separately stay below ρ < 0.4.
   - *Test*: layer the suite on [[2306.03310|LIBERO]] + [[2510.13626|LIBERO-Plus]] + [[2603.28301|LIBERO-Para]] (~40k pairs per WAM); cross-check against [[2506.18123|RoboArena]] + [[2605.20774|VLA-REPLICA]] real SR.
   - *Row*: PiL-World (closed-loop r 0.94) / OSCAR (r +0.852).
   - *Falsifier*: the joint metric stays below ρ 0.7, or separate sub-scores already reach it → the joint axis adds nothing.
3. **H3 — The speed-quality Pareto justifies the 4.8× WAM cost only when imagination helps L3.**
   - *Prediction*: re-running [[2603.22078|WAM vs VLA Robustness]]'s config grid with the joint metric shows the **4.8×** latency cost buys a measurable L3-Evolver gain, isolating *when* imagination is worth paying for.
   - *Test*: re-score the ~12-config grid on the joint metric; plot L3 gain vs latency.
   - *Row*: WAM vs VLA Robustness (separate axes, 4.8× cost).
   - *Falsifier*: the joint metric shows no L3 gain from the extra cost → imagination doesn't help action quality and the cost is unjustified.
4. **H4 — The joint metric exposes shortcut-solvable benchmarks current SR rewards.**
   - *Prediction*: on benchmarks where a 0.09B [[2304.07193|DINOv2]]+MLP probe already hits **99.0%** ([[2606.04233|Manipulation Benchmark Audit]]), the joint causal metric separates genuinely WM-bound policies from shortcut solvers that the SR number cannot distinguish.
   - *Test*: apply the joint metric to the shortcut-probe vs real WAMs on LIBERO-Spatial; report metric separation.
   - *Row*: Manipulation Benchmark Audit (shortcut-solvable) / MetaFine (binary inflates capability).
   - *Falsifier*: the joint metric scores the shortcut probe as high as a real WAM → it certifies the same wrong thing as SR.
5. **H5 — The joint metric's predictive validity survives variance reduction across labs.**
   - *Prediction*: under [[2606.05159|X4Val]] / [[2510.04354|SureSim]] variance reduction, the joint-metric → real-SR correlation holds at ρ > 0.7 cross-lab on [[2605.20774|VLA-REPLICA]]'s reproducible protocol, so the signal is real, not a single-lab artifact.
   - *Test*: estimate the correlation with variance-reduced surrogates across the [[2605.20774|VLA-REPLICA]] / [[2506.18123|RoboArena]] real-fleet split.
   - *Row*: X4Val (variance reduction) / SureSim (prediction-powered).
   - *Falsifier*: the correlation collapses under variance reduction or across labs → it was a sampling artifact.

> [!warning] Risks
> - **Metric noise** — feature-space similarity embeds blind spots. → Pair with explicit physical predicates from A3; cross-validate against [[2605.06311|VISER]]'s measured sim-real correlation.
> - **Sample size** — counterfactual probes may need 100+ rollouts per task instance. → Use [[2603.13966|vla-eval]]'s **47×** speedup to amortize the rollout cost; add [[2606.05159|X4Val]]'s variance reduction (H5).
> - **Selection bias** — the benchmark may flatter current WAMs. → Include adversarial ([[2604.05498|JailWAM]], [[2606.03556|VLA Patch Attack]] at **90.7%** attack SR, [[2605.02900|Safety in Embodied AI Survey]] attack layers) + physics-violating ([[2603.23376|ABot-PhysWorld]] rejects) baselines.

### B2 — Long-Horizon Memory + Failure Recovery Loops for Real-World Deployment

| | |
|---|---|
| **Cluster** | B — Evaluation, Robustness & Deployment |
| **Thesis** | Build one integrated detect-diagnose-recover loop with memory, not four separate modules. An agent that can't remember can't notice repeated failure; one that notices it must change behavior or it isn't learning — so memory, detection, and recovery are three faces of one capability. The field assumes these four parts compose trivially. The bet is in First-principles below. |
| **Anchor papers** | [[2604.16592\|Cognition WM Survey]] (survey), [[2602.04411\|Self-evolving Embodied AI]] (survey), [[2604.23775\|VLA Safety Survey]] (survey), [[2605.10921\|RoboMemArena]] (benchmark), [[2605.10993\|ECHO-VLA]] (method), [[2508.19236\|MemoryVLA]] (method) |
| **Key targets** | ≥+15 pp SR on [[2306.03310\|LIBERO]]-Long memory-dependent tasks (baseline: [[2605.10993\|ECHO-VLA]] **+12.8 pp**); end-to-end on [[2605.10921\|RoboMemArena]] (**68.9%** memory-dependent subtasks); oscillation incidents **−50%**; [[2510.02298\|ARMADA]] **23.3%** intervention reduction |

**Why it matters.**
- **The gap**: a fielded policy is fine-tuned and corrected again and again, but recovery needs memory (to notice repeated failure), detection (to know it failed), and diagnosis (to know *why*) — and [[2604.16592|Cognition WM Survey]] names *meta-cognition*, the embodied form of this loop, one of two drastically under-researched cognitive functions.
- **Today's answers**: the field has each face but no integration — [[2605.10921|RoboMemArena]] shows **68.9%** of subtasks need historical info; [[2605.10993|ECHO-VLA]] is the closest memory system (**+12.8 pp** LIBERO-Long) but has no detection integration; [[2510.02298|ARMADA]] hits **95%** detection accuracy and **23.3%** intervention reduction but no memory; [[2606.03385|GTP-FA]] adds grasp-vs-planning *diagnosis* (real Franka **11.2% → 76.8%**) but as a standalone step. Five memory papers, eight detection papers, six correction papers — none integrated.
- **The opening**: [[2603.09030|PlayWorld]]'s self-play proposer/executor captures failure modes absent from human data (Pearson **0.8766** predicted-vs-real SR, **+65%** real SR), showing the failure-data engine the recovery loop needs already exists — the missing piece is wiring it into a single detect-diagnose-recover loop.

**First-principles framing.**
- **First principle**: An agent that can't remember has no basis for recognizing repeated failure; one that recognizes it must change behavior or it isn't learning. Memory + detection + recovery are three faces of one capability, not three independent modules.
- **Assumption being challenged**: That memory, failure detection, correction, and recovery are independent problems. The field has 5+ memory papers, 8+ detection papers, 6+ correction papers — but no system integrates them. That they compose trivially has never been tested; oscillation, dropout, and latency stacking suggest they don't. [[2602.04411|Self-evolving Embodied AI]]'s 5-module framework names the integration as the open problem.
- **The bet**: An integrated detect-diagnose-recover loop with memory lifts long-horizon SR on [[2306.03310|LIBERO]]-Long memory-dependent tasks by ≥+15 pp over [[2605.10993|ECHO-VLA]]'s +12.8 pp on memory alone (both on LIBERO-Long), end-to-end on [[2605.10921|RoboMemArena]] where **68.9%** of subtasks need history, and cuts oscillation incidents ≥50% via state-machine integration.

**Related research papers.**

Twenty systems that build one face of the loop — memory, detection, diagnosis, recovery, or continual-update — none integrating all four into a single stack. The axis is *which face of the detect-diagnose-recover-with-memory loop it implements and whether it integrates the others*:

| System | Loop face | Integrated? | Key result | What's missing |
|---|---|---|---|---|
| [[2605.10921\|RoboMemArena]] | memory benchmark | — (measures) | **68.9%** subtasks need history | the benchmark the integrated loop is evaluated on, not a method |
| [[2605.10993\|ECHO-VLA]] | hierarchical memory | memory-only | **+12.8 pp** LIBERO-Long | no detection or recovery integration — the closest, but one face |
| [[2508.19236\|MemoryVLA]] | activation-level memory | memory-only | **+26 pp** temporal, **+3.6%** latency | memory alone — doesn't notice or recover from failure |
| [[2606.03374\|eMEM]] | tiered spatio-temporal memory | memory-only | **80.8%** eMEM-Bench, no forgetting to 1-year delay | the long-horizon memory substrate, no detect/recover loop |
| [[2603.12942\|ReMem-VLA]] | 15-min memory bank | memory-only | **94.5%** memory-dependent sim | memory recall, no failure loop |
| [[2510.02298\|ARMADA]] | FLOAT detector | detect-only | **95%** accuracy, **23.3%** intervention reduction | detection without memory or an integrated recovery generator |
| [[2605.30834\|Hide-and-Seek]] | trajectory-only failure localization | detect-only | bACC **0.852**, **2,000×** faster than VLM judge | the cheap detection front-end, no diagnosis or recovery |
| [[2503.08558\|FAIL-Detect]] | failure detection w/o failure data | detect-only | **78%** | detection only, label-free, but not wired to recovery |
| [[2606.03385\|GTP-FA]] | grasp-vs-planning diagnosis | diagnose (closed) | real Franka **11.2% → 76.8%** | the diagnose step detection-only work skips — but a standalone loop |
| [[2410.00371\|AHA]] | failure-reasoning VLM | diagnose | beats GPT-4o (**0.446** AHA-Test), **+22.34%** RL reward | the diagnosis model between detect and recover, not the full loop |
| [[2601.02295\|CycleVLA]] | proactive backtracking correction | recover-only | proactive correction | backtracks but doesn't consult memory for repeated failure |
| [[2602.21633\|SC-VLA]] | imagination + residual-RL correction | detect+recover | **86%** ManiSkill3, **71%** real | imagination-driven correction, no long-horizon memory |
| [[2602.20057\|AdaWorldPolicy]] | WM-error test-time LoRA | recover (online) | recovers SR under OOD at **4 Hz** | the label-free online recover step, no detection/memory front-end |
| [[2505.12224\|RoboFAC]] | recovery from failure traces | recover-only | recovery from traces | recovery without the memory that flags *repeated* failure |
| [[2606.02307\|FATE-VLA]] | adaptive failure discovery | test harness | **+29.7 pp** failure discovery over random | the harness that validates the loop fires, not a loop component |
| [[2511.16166\|EvoVLA]] | self-evolving + gated memory | memory+evolve | stage-hallucination **38.5% → 14.8%**, **69.2%** sim | memory-plus-evolution, but no integrated detect-diagnose-recover |
| [[2506.21669\|SEEA-R1]] | recovery → training example | continual-update | **+34.72 pp** real (replay-free) | the "recovery → training example" engine, not the detection front-end |
| [[2606.05395\|VASO]] | verification-gated correction | recover (verified) | **89% → 97%** feasibility, ~**95%** safety | LTL-gated correction, but no memory of repeated failure |
| [[2510.01642\|FailSafe]] | auto failure-action pipeline | detect+recover | **0.9094** detect / **0.6522** action-cos, **+22.6%** | the detect+auto-labeled-recovery front-end, no memory integration |
| [[2603.09030\|PlayWorld]] | self-play failure-data engine | data engine | Pearson **0.8766**, **+65%** real SR | the failure-data engine feeding the loop, not the loop itself |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (an integrated loop with memory beats summed single-face modules), with the experiment and the Related-table row it lands on.
1. **H1 — Memory-grounded detection catches history-dependent failures memory-blind detectors miss.**
   - *Prediction*: using [[2605.10993|ECHO-VLA]] / [[2508.19236|MemoryVLA]] hierarchical memory as the detection context catches "tried this 3× already" failures that a memory-blind detector ([[2510.02298|ARMADA]]) cannot, raising detection recall on repeated-failure episodes.
   - *Test*: compare memory-grounded vs memory-blind detection on RoboMemArena's repeated-failure subtasks; report recall.
   - *Row*: ECHO-VLA (memory) vs ARMADA (detect-only).
   - *Falsifier*: memory adds no detection recall → the two faces are independent after all.
2. **H2 — The integrated loop beats summed single-face modules on long-horizon SR.**
   - *Prediction*: a stack of memory + parallel detectors + corrective head + recovery generator lifts [[2306.03310|LIBERO]]-Long memory-dependent SR ≥+15 pp over [[2605.10993|ECHO-VLA]]'s memory-only +12.8 pp — i.e., integration beats the best single face.
   - *Test*: build the full loop; evaluate end-to-end on [[2605.10921|RoboMemArena]] (**68.9%** history-dependent); compare to each face alone.
   - *Row*: ECHO-VLA (memory) / SC-VLA (detect+recover).
   - *Falsifier*: the integrated loop ≤ memory-only +12.8 pp → the faces don't compose into a gain.
3. **H3 — State-machine integration cuts the oscillation trivial composition produces.**
   - *Prediction*: detectors firing on each other's corrections produce oscillation in a naive stack; explicit state-machine mode transitions cut oscillation incidents ≥50% with no SR loss.
   - *Test*: run naive-compose vs state-machine integration; count oscillation incidents and SR.
   - *Row*: CycleVLA (proactive correction) / FailSafe (detect+recover).
   - *Falsifier*: naive composition shows no oscillation → the integration overhead buys nothing.
4. **H4 — Diagnosis between detection and recovery raises recovery success over detect-then-recover.**
   - *Prediction*: inserting [[2606.03385|GTP-FA]]-style grasp-vs-planning diagnosis between detection and recovery raises recovery SR over a detect-then-recover loop that skips attribution, because the recovery action is chosen for the *cause*.
   - *Test*: ablate the diagnosis step; compare recovery SR with vs without attribution on the same failures.
   - *Row*: GTP-FA (diagnose) / AHA (diagnose VLM).
   - *Falsifier*: skipping diagnosis matches → cause attribution doesn't improve recovery.
5. **H5 — Each verified recovery becomes a training example without eroding base skills.**
   - *Prediction*: feeding [[2510.02298|ARMADA]]-pooled successful recoveries back as training examples ([[2506.21669|SEEA-R1]] pattern) improves the policy continually, *if* memory writes are gated behind a recovery-success check and protected against poisoning ([[2605.02900|Safety in Embodied AI Survey]]).
   - *Test*: run 100 recovery-update cycles; measure new-task gain and old-task retention (bridges B4).
   - *Row*: SEEA-R1 (recovery→training) / VASO (verification-gated).
   - *Falsifier*: recovery updates erase base skills or fail to improve → the continual loop is unstable without B4.

> [!warning] Risks
> - **Latency stacking** — each component adds 10–100 ms; the full loop may not be real-time. → Parallelize detectors ([[2410.04640|Sentinel]] pattern) and invoke recovery only on firing; co-design with B3's efficiency budget.
> - **Component oscillation** — detectors may fire on each other's corrections. → State-machine integration with explicit mode transitions is the mitigation the bet measures (H3's ≥50% oscillation reduction).
> - **Memory as attack surface** — [[2605.02900|Safety in Embodied AI Survey]] flags memory poisoning. → Gate memory writes behind a recovery-success check (H5); treat the failure-exclusion buffer as untrusted input.

### B3 — Real-Time-Deployable Policies via Architectural-Algorithmic-Data Co-design

| | |
|---|---|
| **Cluster** | B — Evaluation, Robustness & Deployment |
| **Thesis** | Treat efficiency as a primary research target, not "engineering to sort out after publication." Inference cost has three independent levers — what / how often / how precisely you predict — and a contact-rich control loop has a *stability* floor (Nyquist), not just a speed preference, so the levers' Pareto frontier needs co-design. The field assumes single-lever tuning or faster silicon will suffice. The bet is in First-principles below. |
| **Anchor papers** | [[2510.24795\|Efficient VLA Survey]] (survey), [[2510.07077\|VLA Robotics Real-World Review]] (survey), [[2603.28489\|Video Gen as WM Survey]] (survey), [[2505.04769\|VLA Concepts Survey]] (survey), [[2605.14598\|DSSP]] (method) |
| **Key targets** | ≥30 Hz on edge ([Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) / Apple M, vs the AR 3–5 Hz ceiling); ≥95% of base-policy [[2306.03310\|LIBERO]] SR retained; matched-FLOPs Pareto sweep |

**Why it matters.**
- **The gap**: a contact-rich policy runs as a feedback loop on discrete time steps, so it has a Nyquist *stability* floor — a manipulator whose contacts ring at tens of Hz cannot be stabilized by a 3–5 Hz loop, no matter how well tuned — yet efficiency is treated as post-publication engineering.
- **Today's answers**: [[2505.04769|VLA Concepts Survey]] quantifies the wall (AR decoding caps speed at **3–5 Hz** vs the 20–50 Hz needed); [[2510.24795|Efficient VLA Survey]] and [[2603.28489|Video Gen as WM Survey]] reframe efficiency from "optimization" to "prerequisite"; but the levers are pulled singly — [[2602.20309|QuantVLA]] quantizes (**70%** memory cut at **97.6%** LIBERO), [[2503.02310|PD-VLA]] parallel-decodes (**2.52×** to 4.56 Hz), [[2509.09372|VLA-Adapter]] re-architects (**219.2 Hz** at **97.3%**) — rarely co-optimized.
- **The opening**: [[2606.05254|Flash-WAM]]'s modality-aware distillation drops a WAM's per-chunk latency **8.1 s → 348 ms** (**23×**) into the real-time budget, and [[2605.29438|ElegantVLA]]'s "when to think" RL scheduler lifts control freq 16.64 → 35.03 Hz at **3.77×** FLOPs — both showing the latency-quality curve moves with *method*, not silicon.

**First-principles framing.**
- **First principle**: A contact-rich policy runs as a feedback loop on discrete time steps, so it has a *stability* floor, not just a speed preference. Stiff contacts shake the robot at high frequencies. The Nyquist sampling rule says a loop has to run at least ~2× faster than the fastest motion it controls; run it slower and it *cannot* be stabilized, no matter how well tuned. That floor doesn't care about the data or the hardware.
- **Assumption being challenged**: That efficiency is "engineering, not research," something faster chips will fix on their own. In contact-rich manipulation, the gap between 3–5 Hz and 30 Hz isn't a tuning knob — it's the line between sitting below the stability floor and above it. [[2510.07077|VLA Robotics Real-World Review]] names latency a top-3 deployment concern and [[2511.05936|10 VLA Challenges]] names resource efficiency one of ten bottlenecks; no other direction here treats efficiency as a primary thesis.
- **The bet**: Co-designed (architecture + training + data + quantization) policies hit ≥30 Hz on edge ([Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) / Apple M) while keeping ≥95% of base-policy SR — showing the latency-quality curve can be moved by method, not just hardware. (The 95% bar is a design-chosen target, not a paper-reported figure.)

**Related research papers.**

Sixteen efficiency methods that pull *one* lever — backbone, decoding, quantization, data, or distillation — none co-optimizing all four against a stability-floor target. The axis is *which lever it pulls and whether it clears the 30 Hz floor while holding SR*:

| System | Efficiency lever | Clears 30 Hz? | Key result | What's missing |
|---|---|---|---|---|
| [[2510.24795\|Efficient VLA Survey]] | three-pillar taxonomy (model/training/data) | — (survey) | the co-design map | survey only — names the levers, doesn't co-optimize them |
| [[2505.04769\|VLA Concepts Survey]] | quantitative anchor | — (survey) | AR **3–5 Hz** vs 20–50 Hz needed | the wall, not a method |
| [[2605.14598\|DSSP]] | linear-time state-space backbone | yes (smaller footprint) | **62.30%** [[2506.18088\|RoboTwin 2.0]] | the in-vault linear-backbone exemplar — single lever |
| [[2509.09372\|VLA-Adapter]] | bridge-attention 0.5B architecture | **219.2 Hz** | **97.3%** [[2306.03310\|LIBERO]], no robotic pre-training | architecture lever alone — clears the floor but isn't co-designed |
| [[2605.08799\|ElasticFlow]] | one-step average-velocity decoding | **71 Hz** (14 ms) | **98.5%** [[2306.03310\|LIBERO]], 5× over diffusion policy | the decoding lever alone — real-time is a method choice |
| [[2606.05737\|One-Step VLA]] | high-noise-biased one-step flow matching | yes (one-step) | **95.6%** LIBERO-Long, no distillation needed | decoding lever, no quantization/data co-design |
| [[2503.02310\|PD-VLA]] | training-free parallel decoding | **4.56 Hz** (**2.52×**) | **94.7%** [[2306.03310\|LIBERO]] | the decoding lever with no retraining — but below the floor alone |
| [[2602.20309\|QuantVLA]] | training-free W4A8 quantization | (composes) | **70%** memory cut, **97.6%** [[2306.03310\|LIBERO]] | the quantization lever the co-design composes — single axis |
| [[2511.04555\|Evo-1]] | 0.77B small backbone + edge deploy | **16.4 Hz** on 2.3 GB | **94.8%** [[2306.03310\|LIBERO]] | small-backbone + edge point, below the 30 Hz floor alone |
| [[2605.13778\|Realtime-VLA FLASH]] | dual-path speculative inference | **3.04×** latency cut (58→19 ms) | **93.8%** [[2306.03310\|LIBERO]] | the latency lever via draft-verify — one axis |
| [[2605.29438\|ElegantVLA]] | RL "when to think" compute scheduler | 16.64 → **35.03 Hz** | **3.77×** FLOPs sim / 2.18× real | per-phase compute, not a fixed rule — but only the compute axis |
| [[2606.05254\|Flash-WAM]] | modality-aware distillation | **348 ms**/chunk (**23×**) | into the ~500 ms budget | WAM-side proof real-time is a method choice — distillation lever |
| [[2603.16195\|S-VAM]] | self-distilled single-pass foresight | **25 Hz** | **+15.8%** latency over teacher | resolves foresight-vs-real-time, but one lever |
| [[2605.28634\|PrimitiveVLA]] | reusable motion primitives | (data lever) | full-data SR at **50%** data, **6×** zero-shot | the data-efficiency lever, not composed with the others |
| [[2602.16710\|EgoScale]] | log-linear ego data scaling | (data lever) | **+54%** dexterous | the data lever — pretraining, not inference speed |
| [[2505.23705\|Knowledge Insulation VLA]] | stop-gradient PEFT | (training lever) | knowledge-insulated fine-tuning | the training lever for efficient RL on small backbones |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (co-design clears the stability floor where single levers and silicon don't), with the experiment and the Related-table row it lands on.
1. **H1 — Co-design reaches 30 Hz on edge where any single lever falls short.**
   - *Prediction*: a Pareto sweep of backbone (Transformer / linear-attn / Mamba) × decoding (AR / parallel / diffusion) × precision (FP16 / INT8 / INT4) reaches ≥30 Hz on [Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) at ≥95% base SR, where the best single lever ([[2503.02310|PD-VLA]] at 4.56 Hz, [[2602.20309|QuantVLA]] memory-only) cannot.
   - *Test*: sweep the three axes on [[2306.03310|LIBERO]] + 1 real task; locate the co-designed point vs single-lever points.
   - *Row*: PD-VLA (decoding) / QuantVLA (quantization) — single levers below the floor.
   - *Falsifier*: a single lever already reaches 30 Hz at ≥95% SR → co-design is unnecessary.
2. **H2 — Linear-time backbones hold SR at the floor only with knowledge-insulated RL.**
   - *Prediction*: a Mamba VLA + [[2505.23705|Knowledge Insulation VLA]] stop-gradient retains ≥95% SR on [[2510.13626|LIBERO-Plus]] at >30 Hz, while an un-insulated Mamba VLA loses SR — the backbone speed only matters if SR holds.
   - *Test*: train insulated vs un-insulated Mamba VLA; report SR-retention at matched frequency.
   - *Row*: DSSP (linear backbone) / VLA-Adapter (architecture lever).
   - *Falsifier*: the un-insulated Mamba holds SR → insulation isn't needed and the linear backbone is free.
3. **H3 — Data-efficient ego co-training matches a 10×-data baseline on a fraction of robot data.**
   - *Prediction*: [[2602.16710|EgoScale]] + a mixed-data recipe matches a 10×-robot-data baseline's SR using far less robot data, so the data lever moves the curve as much as the model lever.
   - *Test*: measure robot data needed to match the 10×-data baseline with vs without ego co-training.
   - *Row*: EgoScale (data lever) / PrimitiveVLA (data efficiency).
   - *Falsifier*: ego co-training needs the full robot data anyway → the data lever doesn't move the frontier.
4. **H4 — A real-time joint policy+latent-WM (A1) runs above the floor.**
   - *Prediction*: A1's joint loop with a Mamba latent WM ([[2511.15605|SRPO]] [[2506.09985|V-JEPA 2]] substrate, ~10 ms) runs >30 Hz, confirming the latent-for-speed thesis composes with the joint-loop thesis.
   - *Test*: profile the latent joint loop on edge; report frequency and SR.
   - *Row*: Flash-WAM (distilled WAM real-time) / S-VAM (single-pass foresight).
   - *Falsifier*: the joint latent loop runs below 30 Hz → A1 and B3 don't compose at the floor.
5. **H5 — The edge-deployment chain loses ≤5% SR per stage.**
   - *Prediction*: train → quantize ([[2602.20309|QuantVLA]]) → distill ([[2606.05254|Flash-WAM]]) → deploy on [Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) / Apple M holds ≥95% base SR end-to-end, validated cross-lab via [[2605.20774|VLA-REPLICA]] (ID 0.49 vs 0.48).
   - *Test*: measure SR retention per stage; validate cross-lab reproducibility.
   - *Row*: QuantVLA (quantization) / Realtime-VLA FLASH (speculative latency).
   - *Falsifier*: cumulative SR loss exceeds 5% → the chain doesn't preserve the policy and the floor is unreachable at deployable quality.

> [!warning] Risks
> - **Linear-attn / Mamba may underperform Transformers on long-context policies** — the speed gain only matters if SR holds. → Gate every Pareto point on an SR-retention threshold (H2); report points that fail it.
> - **Edge-hardware diversity** — [Jetson](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) vs Apple M vs custom NPUs need per-platform tuning. → Validate cross-platform via [[2605.20774|VLA-REPLICA]]'s reproducibility protocol (H5), not a single device.
> - **Saturation risk** — if "Mamba + LoRA + co-training" becomes the dominant recipe, the contribution shrinks to engineering. → Frame the deliverable as the Pareto curve + system-level insights, not a single point estimate.

### B4 — Continual Policy Learning Without Catastrophic Forgetting

| | |
|---|---|
| **Cluster** | B — Evaluation, Robustness & Deployment |
| **Thesis** | Protect selective weight subspaces during continual policy fine-tuning instead of defaulting to data-replay. In an over-parameterized policy, the directions a new skill needs and those an old skill occupies are *mostly disjoint*, so forgetting is a subspace-overlap problem, not a storage one. The field assumes replaying old trajectories is the price of retention. The bet is in First-principles below. |
| **Anchor papers** | [[2508.07407\|Self-Evolving AI Agents Survey]] (survey), [[2404.14387\|LLM Self-Evolution Survey]] (survey), [[2602.04411\|Self-evolving Embodied AI]] (survey), [[2510.20685\|C-Nav]] (benchmark), [[2605.15735\|UAM]] (method), [[1612.00796\|EWC]] (method) |
| **Key targets** | ≥+9.7 pp old-task SR over Data Replay ([[2510.20685\|C-Nav]] **42.61% vs 32.9%** [[2109.08238\|HM3D]]); replay-free manipulation transfer ([[2605.29562\|VLA-Pro]] real **5.8% → 65.0%**, unseen **+207%** [[2504.13059\|RoboTwin]]); embodiment tax **<5%** ([[2605.15735\|UAM]]); ≤−3 pp new-task SR vs full fine-tune |

**Why it matters.**
- **The gap**: a fielded policy is fine-tuned again and again (new objects, new corrections from B2's loop), and every fine-tune erodes prior skill — yet forgetting shows up elsewhere in this doc only as a *risk* (B2 names it the hazard its recovery-update loop must avoid), never as a first-class objective.
- **Today's answers**: the field's reflex is data-replay, which carries cost — [[2510.20685|C-Nav]] shows replay's storage + privacy burden (whole trajectories) *and still loses* to a dual-path design (**42.61% vs 32.9%** old-task SR on [[2109.08238|HM3D]], replay-free, half the data); [[2605.15735|UAM]] quantifies the "embodiment tax" (unfreezing a VLM degrades >5% multimodal competence, freezing cripples action learning); [[2605.26820|VLA Continual Forgetting]] shows naive sequential fine-tuning collapses earlier-task score **99.2 → 17.8**.
- **The opening**: [[2603.24350|Emergent Self]] shows that in continual quadruped RL a behavior-invariant subnetwork forms and *persists* (**+16.9 pp**, p<0.001) while task-specific parts reorganize — direct evidence for a stable shared subspace — and [[2605.29548|Capacity Interference Retention]] supplies the why: forgetting is inter-task *interference*, which scale and selective protection both reduce.

**First-principles framing.**
- **First principle**: A large policy has far more weights than any one skill needs. The handful of weight directions a new skill leans on barely overlap with the ones an old skill already uses — so forgetting happens only where they *do* overlap, in a small set of shared directions, not because the model ran out of room. The fix is therefore to *protect those shared directions*, not to re-show the old data.
- **Assumption being challenged**: That data-replay is the safe, near-free default. [[2510.20685|C-Nav]] shows replay carries real storage + privacy cost and *still loses* to a dual-path design; [[2605.15735|UAM]] shows a dual-stream beats freeze-or-unfreeze with no replay. "Replay is the price of retention" is borrowed from supervised continual learning and never re-checked for action policies.
- **The bet**: A replay-free selective-subspace / dual-path method beats data-replay by ≥+9.7 pp old-task SR (matching [[2510.20685|C-Nav]]'s [[2109.08238|HM3D]] 42.61% vs 32.9% gain) at strictly lower storage, holding the embodiment tax <5% ([[2605.15735|UAM]]) and new-task SR within −3 pp of full fine-tune — making forgetting a controllable axis, not an accepted loss.

**Related research papers.**

Seventeen systems that handle continual learning — by subspace protection, dual-path architecture, adapters, replay-content scheduling, or weight merging — most borrowed from classification and few validated on action policies. The axis is *how it protects old skills and whether it is replay-free and policy-validated*:

| System | Protection mechanism | Replay-free? | Key result | What's missing |
|---|---|---|---|---|
| [[2605.15735\|UAM]] | dual-stream (Semantic + Dorsal Expert) | yes | **>95%** VLM retention, **<5%** embodiment tax | architectural, no continual-*task-sequence* eval |
| [[2510.20685\|C-Nav]] | Dual-Path Anti-Forgetting + LOF keyframes | yes (half data) | **+9.7 pp** old-task SR (**42.61 vs 32.9**) [[2109.08238\|HM3D]] | nav-only — the head-to-head B4 extends to manipulation |
| [[2605.26820\|VLA Continual Forgetting]] | configured replay + fixed action-norm | partial replay | naive crashes **99.2 → 17.8**; configured holds within **10 pp** | the replay baseline to beat — still needs stored data |
| [[2606.03598\|PHASER]] | phase-aware semantic experience replay | no (replay-content) | **+31%** Average SR over standard ER | replay *content* matters — but still replay, not subspace protection |
| [[2605.29562\|VLA-Pro]] | per-task procedural-memory LoRA adapters | yes | unseen **+207%** RoboTwin, real **5.8% → 65.0%** | weight-space transfer, the replay-free alternative — per-task, not unified subspace |
| [[1612.00796\|EWC]] | Fisher-weighted parameter protection | yes | canonical subspace-importance prior | classification/Atari — predates action policies |
| [[2605.29548\|Capacity Interference Retention]] | (theory) larger models forget less | — | capacity *cuts inter-task interference* | the theory behind "forgetting is interference," not a policy method |
| [[2603.24350\|Emergent Self]] | behavior-invariant subnetwork emerges | yes (emergent) | **+16.9 pp**, persists while task-parts reorganize | evidence for the stable shared subspace, not an explicit protection scheme |
| [[2605.08879\|ConSFT]] | conservative importance weight + stop-gradient | yes | **34%** [[2306.03310\|LIBERO]] retention vs vanilla-SFT collapse | the replay-free SFT-side mechanism, no subspace-overlap analysis |
| [[2603.07648\|AtomicVLA]] | skill-guided MoE adds experts without retraining | yes | **96.6%** avg [[2306.03310\|LIBERO]], **1.3%** forgetting | modular protection vs subspace penalties — adds parameters per skill |
| [[2602.03445\|CRL-VLA]] | dual-critic (frozen goal-value + trainable MC) | yes | **+0.17** positive backward transfer | the plasticity-retention frontier as architecture, not subspace overlap |
| [[2503.18684\|OMLA]] | online meta-learned LoRA from task-agnostic prior | yes | **0.86** FWT (vs LoRA 0.71), **0** backward transfer | replay-free fast adaptation, no explicit overlap protection |
| [[2602.10503\|Long-Lived Robots]] | interaction-free RFT (GRPO + process reward) | yes | NBT **1.5 vs SFT 6.8**, **+19.6%** FWT at 20% data | the RFT continual baseline to beat — no subspace mechanism |
| [[2509.22195\|Actions as Language]] | recast actions as language to preserve base | yes (interface) | retains **>85%** VQA, no forgetting | stability via the interface, not weight-subspace protection |
| [[2211.15944\|Continual-Dreamer]] | replay + Plan2Explore in a world model | no (replay) | mitigates forgetting on [[2109.13202\|MiniHack]] | the WM-side analog — game benchmarks, replay-based |
| [[2408.07666\|Model Merging in LLMs/MLLMs]] | weight-space merging as consolidation | yes | replay-free consolidation operator | not validated on action policies — candidate for fusing adapters |
| [[2405.09673\|LoRA-Learns-Less]] | PEFT under-fits but forgets less | yes | quantifies plasticity-retention trade-off | documents the trade-off B4 must navigate, not a protection method |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (replay-free subspace protection beats replay on action policies), with the experiment and the Related-table row it lands on.
1. **H1 — Consecutive fine-tunes overlap in <0.3 of their gradient subspace.**
   - *Prediction*: for a sequence of [[2510.13626|LIBERO-Plus]] / object-nav tasks, principal-angle / Fisher-overlap between consecutive fine-tunes stays below 0.3 for most task pairs — the precondition for selective protection.
   - *Test*: measure gradient-subspace overlap across the task sequence; build an overlap matrix predicting which pairs forget.
   - *Row*: EWC (subspace-importance prior) / Emergent Self (stable subnetwork).
   - *Falsifier*: overlap > 0.5 dominates → subspaces aren't disjoint and selective protection can't work.
2. **H2 — Replay-free dual-path protection beats replay at lower storage.**
   - *Prediction*: [[2605.15735|UAM]]'s Semantic/Dorsal split + [[2510.20685|C-Nav]]'s representation-drift losses, protecting only the high-overlap (H1) directions via [[1612.00796|EWC]] Fisher penalties, beats data-replay by ≥+9.7 pp old-task SR at strictly lower storage.
   - *Test*: compare full fine-tune / replay / LoRA / dual-path-subspace on the same task stream; report old-task SR and storage.
   - *Row*: C-Nav (dual-path, +9.7 pp) / VLA Continual Forgetting (replay baseline).
   - *Falsifier*: replay matches or beats the subspace method at equal storage → replay is the right default.
3. **H3 — The embodiment tax stays <5% across a continual sequence.**
   - *Prediction*: after each fine-tune, re-running the frozen VLM's multimodal suite ([[2311.16502|MMMU]] / [[2306.13394|MME]] / [[2307.06281|MMBench]]) shows the tax stays <5% across ≥5 sequential tasks, matching [[2605.15735|UAM]]'s single-step result over a sequence.
   - *Test*: track multimodal-competence drop across 5 sequential fine-tunes.
   - *Row*: UAM (dual-stream, <5% tax).
   - *Falsifier*: the tax exceeds 5% over the sequence → dual-path doesn't hold competence under repeated fine-tuning.
4. **H4 — Subspace protection stops B2's recovery updates from erasing base skills.**
   - *Prediction*: feeding B2's recovery-success examples as a task stream, the subspace method keeps old-task SR within −3 pp over 100 recovery updates, where unprotected continual updates erode it.
   - *Test*: measure old-task SR before/after 100 recovery updates with vs without subspace protection (bridges B2).
   - *Row*: Long-Lived Robots (RFT continual) / CRL-VLA (dual-critic).
   - *Falsifier*: protected updates still erase base skills → the loop B2+B4 forms is unstable.
5. **H5 — A replay-free point dominates replay on the storage-vs-retention Pareto.**
   - *Prediction*: sweeping keyframe budget ([[2510.20685|C-Nav]] LOF) × protection strength yields a replay-free point that dominates replay on *both* storage and retention, not merely matching it.
   - *Test*: plot retention vs storage for replay-free vs replay configurations; locate the dominating point.
   - *Row*: PHASER (replay-content) / VLA-Pro (replay-free adapters).
   - *Falsifier*: no replay-free point dominates → replay stays Pareto-competitive and the claim narrows to "matches replay."

> [!warning] Risks
> - **Subspaces may not be disjoint for *similar* tasks** — two manipulation skills sharing contact dynamics could overlap heavily, collapsing the geometric premise. → H1's overlap matrix is the go/no-go: if overlap >0.5 dominates, fall back to memory ([[2605.10993|ECHO-VLA]]) rather than subspace protection.
> - **Plasticity collapse** — protecting too many directions freezes new-task learning (the [[2405.09673|LoRA-Learns-Less]] failure mode). → Bound protection strength by the ≤−3 pp new-task-SR target; report the retention/plasticity frontier, not a single point.
> - **Replay quietly wins at scale** — if storage is cheap and privacy a non-issue, replay may stay competitive. → Frame the deliverable as the storage-vs-retention Pareto (H5); the claim is *dominance on both axes*, not merely matching replay.

---

## Cluster C — Mobility & Embodiment Generalization: Moving and Transferring

*Two directions fail the same way: by factoring away load-bearing structure — the world's layout (C1) and the body's morphology (C2) — that the policy needed to keep. Keep the right invariant and the fixed-base and fixed-body assumptions stop breaking. The per-capability instantiations defer to the sibling docs; here the mechanism is the contribution.*

### C1 — Latent In-Policy Dreaming for Vision-and-Language Navigation

| | |
|---|---|
| **Cluster** | C — Mobility & Embodiment Generalization |
| **Thesis** | Put a latent dream-ahead head *inside* the navigation policy instead of bolting on an external world model. A navigation decision needs only the *control-relevant* slice of the future — "will this action open a path to the goal?" — which a latent token carries far more cheaply than a rendered frame. The field assumes anticipatory VLN needs an external pixel-space world model. The bet is in First-principles below. |
| **Anchor papers** | [[2311.00530\|LLM Embodied Navigation Survey]] (survey), [[2605.00080\|WM Robot Learning Survey]] (survey), [[2504.21853\|Interactive Generative Video Survey]] (survey), [[2603.29165\|LatentPilot]] (method), [[2506.23468\|NavMorph]] (method) |
| **Key targets** | ≥62.0% SR / 58.0% SPL [[2004.02857\|R2R-CE]] Val-Unseen at ≤130 ms / 22.8 GB ([[2603.29165\|LatentPilot]]); **+4.1% SR** online adaptation at **2.1×** speed ([[2506.23468\|NavMorph]]) |

**Why it matters.**
- **The gap**: VLN agents decide myopically from current observations alone; the obvious fix — an external world model rendering candidate futures — adds compounding prediction error, memory, and latency to a per-step closed loop, paying to render pixels when only a low-dimensional control-relevant slice is needed.
- **Today's answers**: this is the same latent-beats-external bet A1 makes for manipulation, with navigation's own evidence — [[2603.29165|LatentPilot]] internalizes anticipatory reasoning as a single "Pilot Token" and reaches **62.0% SR** on [[2004.02857|R2R-CE]] Val-Unseen at **130 ms / 22.8 GB**, beating external world models on *both* accuracy and efficiency; [[2506.23468|NavMorph]] adds a compact RSSM that self-evolves online (**2.1×** faster than gradient adaptation, **+4.1% SR** on unseen [[2010.07954|RxR-CE]]).
- **The opening**: no work fuses in-policy latent dreaming ([[2603.29165|LatentPilot]]) with online self-evolution ([[2506.23468|NavMorph]]) and measures the joint efficiency-accuracy frontier against reasoning-heavy VLN ([[2605.22816|AwareVLN]] hits **73.5% SR** with an explicit reasoning data engine) — the unclaimed point that would prove foresight is a representation choice.

**First-principles framing.**
- **First principle**: A navigation decision needs only the *control-relevant* slice of the future — "will this action open a path to the goal?" — not a photorealistic render of the next viewpoint. That slice is low-dimensional and lives naturally in a latent token; rendering pixels to recover it wastes compute on a per-step closed loop.
- **Assumption being challenged**: That anticipatory VLN needs an external pixel-space world model. The explicit-lookahead work ([[2309.17080|GAIA-1]]-style simulators, candidate-future rendering, [[2403.09631|3D-VLA]]) treats foresight and generation as one problem; [[2603.29165|LatentPilot]]'s Pilot Token and [[2506.23468|NavMorph]]'s RSSM already carry the control-relevant future in latent space for far less — yet external-WM VLN is still the default.
- **The bet**: An in-policy latent dream head, optionally self-evolving online, matches or beats external-WM VLN SOTA — ≥62.0% SR / 58.0% SPL on [[2004.02857|R2R-CE]] Val-Unseen at ≤130 ms / 22.8 GB ([[2603.29165|LatentPilot]]) and ≥+4.1% online-adaptation SR at 2.1× the speed of gradient adaptation ([[2506.23468|NavMorph]]) — proving foresight is a representation choice, not an external module.

**Related research papers.**

Sixteen navigation systems that handle foresight differently — in-policy latent, joint action+latent, external pixel-WM, rendered-data, reasoning-token, or sandbox-experience — none fusing in-policy dreaming with online self-evolution. The axis is *where foresight lives and how it is represented*:

| System | Foresight form | Online self-evolution? | Key result | What's missing |
|---|---|---|---|---|
| [[2603.29165\|LatentPilot]] | in-policy Pilot Token (latent) | no | **62.0% SR / 58.0% SPL** [[2004.02857\|R2R-CE]] at **130 ms / 22.8 GB** | SOTA accuracy + efficiency, but no online self-evolution |
| [[2606.04907\|WAM-Nav]] | joint long-horizon action + 1-step latent foresight (DiT) | no | **+15.7% SR** Image-Goal, real **85%** Unitree G1 | multi-task but single-step foresight, no online evolution |
| [[2506.23468\|NavMorph]] | self-evolving RSSM + Contextual Evolution Memory | yes | **+4.1% SR / +2.73% SPL** [[2010.07954\|RxR-CE]], **2.1×** faster | online adaptation, but not fused with in-policy dreaming |
| [[2603.02772\|ASER]] | agentic self-evolutionary replanning | yes (runtime) | **+10% SR**, **20-40%** fewer tokens | runtime self-evolution C1 pairs with dreaming, not a dream head |
| [[2605.22816\|AwareVLN]] | explicit reasoning trace | no | **73.5% SR / 65.4% SPL** [[2004.02857\|R2R-CE]] | reasoning-heavy — the latency baseline latent dreaming must beat |
| [[2606.03682\|GN0]] | rendered-data (3DGS) gen+eval+policy | no | **67.7% SR / 63.4% SPL** R2R, zero real-world training | solves transfer with rendered data, orthogonal to in-policy foresight |
| [[2512.01550\|NavForesee]] | dual-horizon predictive in one backbone | no | **66.2% SR / +10.9% OSR** [[2004.02857\|R2R-CE]] | in-backbone foresight, but *pixel-level* prediction |
| [[2511.17097\|Progress-Think]] | semantic-progress reasoning (monotonic loss) | no | **60.1% SR** [[2004.02857\|R2R-CE]], no progress labels | anticipation without privileged supervision, not latent dreaming |
| [[2605.10118\|SAGE]] | physics-grounded sandbox experience + GRPO | no | **64.8% SR** GOAT-Bench (4B beats GPT-4o), real | navigation from imagined-sandbox, not in-policy dreaming |
| [[2507.22028\|S2E (Navigation)]] | offline video pre-training + RL | no | **+21% SR** over BC, zero-shot to wheeled + quadruped | the video-prior + RL alternative to dreaming |
| [[2603.25981\|PiJEPA]] | policy-guided MPPI over JEPA latent WM | no | **1.65 m** RMSE | policy-plus-latent-WM fusion, but planner-side, not in-policy |
| [[2603.07799\|MWM]] | mobile WM via consistency distillation | no | **4×** rollout speedup, real goal-image SR **0.30** vs NoMaD **0.08** | the external nav-WM C1 sidesteps |
| [[2604.24391\|FreqCache]] | frequency-guided token caching | no | **637 → 401 ms** (**1.59×**), **76.0%** Oracle SR | the inference-acceleration lever on C1's frontier, not foresight |
| [[2411.04983\|DINO-WM]] | latent WM planning in [[2304.07193\|DINOv2]] features | no | latent rollouts plan without pixel decoding | the manipulation-side proof, not deployed for VLN |
| [[2402.19161\|MemoNav]] | goal-aware working memory | no | image-goal navigation memory | the memory-as-foresight precursor NavMorph's CEM generalizes |
| [[2309.17080\|GAIA-1]] | external generative pixel-WM | no | driving world model | the external-pixel-WM paradigm C1 bets against |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (in-policy latent dreaming matches external-WM VLN at a fraction of the cost), with the experiment and the Related-table row it lands on.
1. **H1 — Fusing in-policy dreaming with online self-evolution beats either alone within the latency budget.**
   - *Prediction*: bolting [[2506.23468|NavMorph]]'s Contextual Evolution Memory onto [[2603.29165|LatentPilot]]'s Pilot Token improves the dreamed latent at test time without the gradient-adaptation cost — staying ≤130 ms while gaining NavMorph's +4.1% online-adaptation SR.
   - *Test*: add a test-time CEM update to the Pilot Token; report SR and latency vs LatentPilot and NavMorph alone.
   - *Row*: LatentPilot (in-policy latent) / NavMorph (online RSSM).
   - *Falsifier*: the fused system exceeds 130 ms or gains no online SR → the two don't compose within budget.
2. **H2 — Latent foresight pays off only up to a shallow dream horizon.**
   - *Prediction*: varying the imagined horizon (1-step vs k-step Pilot-Token rollout), SR/SPL saturates at a shallow horizon on [[2004.02857|R2R-CE]] / [[2010.07954|RxR-CE]] while latency keeps rising — deeper dreaming stops paying off.
   - *Test*: sweep dream horizon; plot SR/SPL vs latency; locate the saturation point.
   - *Row*: NavForesee (dual-horizon pixel) — the pixel-prediction contrast.
   - *Falsifier*: SR keeps rising with horizon → deeper latent dreaming is worth the cost and the cheap-foresight claim weakens.
3. **H3 — Privileged future-obs supervision transfers from sim to real without collapse.**
   - *Prediction*: [[2603.29165|LatentPilot]]'s PilotLoop (future observations as privileged supervision in sim) transfers to real deployment ([[2507.13019|VLN-PE]] Fall/Stuck rate) without sim-only collapse, retaining the foresight gain on a physical embodiment.
   - *Test*: deploy on [[2507.13019|VLN-PE]]; compare Fall/Stuck rate with vs without the privileged-supervision head.
   - *Row*: LatentPilot (in-policy latent) — its **10.65%** Fall / **0.97%** Stuck the reference.
   - *Falsifier*: the privileged signal collapses on real deployment → fall back to [[2506.23468|NavMorph]]'s unsupervised CEM.
4. **H4 — Latent foresight is cost-competitive with explicit reasoning where reasoning isn't load-bearing.**
   - *Prediction*: head-to-head at matched backbone, the latent Pilot Token ([[2603.29165|LatentPilot]]) matches the explicit reasoning trace ([[2605.22816|AwareVLN]]) on closed-loop nav SR at far lower latency on the regimes where reasoning isn't the bottleneck, losing only where explicit reasoning is essential.
   - *Test*: compare latent vs reasoning-token foresight at matched backbone across task difficulty; report the accuracy-latency trade per regime.
   - *Row*: AwareVLN (explicit reasoning) vs LatentPilot (latent).
   - *Falsifier*: explicit reasoning wins broadly at acceptable latency → latent foresight is not the efficient default.
5. **H5 — The latent dream head transfers cross-embodiment, or needs C2-style invariance.**
   - *Prediction*: the latent dream head transfers zero-shot to a new mobile base (matching [[2509.23203|CE-Nav]]'s cross-robot mSR **0.745–0.860**), or it needs a C2-style morphology-invariant interface — the test that ties C1 to C2.
   - *Test*: deploy the dream head on a held-out base zero-shot; if it fails, add a morphology-invariant action interface and re-test.
   - *Row*: CE-Nav (cross-embodiment local nav) / S2E (zero-shot to wheeled + quadruped).
   - *Falsifier*: the head transfers zero-shot with no invariance scaffolding → C1 is embodiment-agnostic on its own.

> [!warning] Risks
> - **Latent dreaming may not help on long-horizon [[2010.07954|RxR-CE]]** — Pilot Token foresight could plateau where explicit reasoning ([[2605.22816|AwareVLN]]) still wins. → H4's head-to-head bounds the claim to the regimes where latent foresight is cost-competitive; report where it loses.
> - **Online self-evolution can drift** — CEM updates at test time risk catastrophic adaptation to a misleading episode. → Gate CEM writes behind a confidence check; borrow B4's forgetting-aware protection for the test-time update.
> - **Sim-only privileged supervision** — PilotLoop's future-obs supervision exists only in sim; real deployment loses it. → H3 validates [[2507.13019|VLN-PE]] transfer before claiming real-world foresight; fall back to [[2506.23468|NavMorph]]'s unsupervised CEM if it collapses.

### C2 — Morphology-Invariant Action Representations for Cross-Embodiment Zero-Shot Transfer

| | |
|---|---|
| **Cluster** | C — Mobility & Embodiment Generalization |
| **Thesis** | The open question is *which invariant intermediate* — language, latent goal, pointmap, or phase — carries control across robot *families*, not how to retarget within one. Some abstraction of "pick up the cup" is morphology-invariant by construction; native-per-body tokenization is the accidental one that couples policy to a single body plan. The field assumes cross-family transfer needs per-robot fine-tuning. The bet is in First-principles below. The per-capability *instantiations* defer to the siblings: cross-morphology *hands* to [[Manipulation\|Manipulation]], cross-embodiment *whole-body* to [[Whole-Body\|Whole-Body]]. |
| **Anchor papers** | [[2510.07077\|VLA Robotics Real-World Review]] (survey), [[2504.03515\|Dexterous IL Survey]] (survey), [[2604.04707\|OpenWorldLib]] (survey), [[2505.14986\|AnyBody]] (benchmark), [[2602.10556\|LAP]] (method), [[2605.20811\|Demo-JEPA]] (method) |
| **Key targets** | >30% extrapolation SR on [[2505.14986\|AnyBody]] novel-morphology split (current **0%**); >50% zero-shot cross-embodiment ([[2602.10556\|LAP]], **2×** prior policies); **0.36** one-shot ([[2605.20811\|Demo-JEPA]], vs **0.04** [[2412.14803\|VPP]]) |

**Why it matters.**
- **The gap**: "pick up the cup" denotes the same task intent for a 7-DoF arm, a parallel gripper, or a humanoid hand, but a policy that tokenizes in *joint space* couples its representation to a single body plan — and [[2505.14986|AnyBody]] is the brutal diagnostic: multi-embodiment policies match single-embodiment baselines on *seen* robots and *interpolation* but collapse to **0%** SR on *extrapolation* across very different link structures.
- **Today's answers**: the candidates differ only in *which intermediate they make invariant* — [[2602.10556|LAP]] parses continuous actions into *natural language*, aligning with the VLM's pretraining, and hits **>50%** zero-shot (**2×** prior policies, 2.5× fewer demos); [[2605.20811|Demo-JEPA]] abstracts demonstrations into *target-compatible latent goals* (**0.36** one-shot vs [[2412.14803|VPP]]'s **0.04**); [[2606.03943|PointAction]] uses 3D pointmaps; [[2606.01851|PHASOR]] uses motion phase. All replace native-per-body tokenization — but none has faced AnyBody's extrapolation wall.
- **The opening**: [[2605.25044|X-DiffVLA]] generalizes across grippers and dexterous hands *after* training via a single morphological-tree diffusion head (no per-embodiment head, **+15.3 pp** over π0.5 on RoboCasa), showing per-robot fine-tuning is already escapable — what's missing is testing such an invariant against the unbeaten 0% benchmark.

**First-principles framing.**
- **First principle**: "Pick up the cup" denotes the same *task intent* for a 7-DoF arm, a parallel gripper, or a humanoid hand. The intent is morphology-invariant; the joint-space trajectory is morphology-specific. A representation grounded in intent (language, latent goal, or task-space) is invariant *by construction*; native-joint tokenization is the accidental one that couples policy to body.
- **Assumption being challenged**: That cross-embodiment transfer needs per-robot fine-tuning — the norm ([[2212.06817|RT-1]] / [[2409.20537|HPT]] / [[2510.10274|X-VLA]] all retrain or adapt per body). [[2602.10556|LAP]]'s language-actions and [[2605.20811|Demo-JEPA]]'s latent goals already get *zero-shot* transfer from an invariant intermediate — yet [[2505.14986|AnyBody]] shows the best multi-embodiment policies still hit 0% on true extrapolation, because they tokenize in joint space.
- **The bet**: A morphology-invariant action representation reaches >30% zero-shot SR on [[2505.14986|AnyBody]]'s extrapolation split (current best: **0%**), consistent with [[2602.10556|LAP]]'s **>50%** zero-shot and [[2605.20811|Demo-JEPA]]'s **0.36** one-shot — turning extrapolation to novel link structures from an impossibility into a measurable transfer rate.

**Related research papers.**

Seventeen cross-embodiment systems that make a *different* intermediate invariant — language, latent goal, pointmap, phase, soft-prompt, or native joint — none yet beating the AnyBody extrapolation wall. The axis is *which invariant intermediate carries control across families and whether it faces true extrapolation*:

| System | Invariant intermediate | Faces AnyBody wall? | Key result | What's missing |
|---|---|---|---|---|
| [[2505.14986\|AnyBody]] | 18-robot benchmark | — (sets the wall) | interpolation transfers, extrapolation **0%** | the unbeaten 0% benchmark C2 must break, not a method |
| [[2602.10556\|LAP]] | natural-language actions | no | **>50%** zero-shot (**2×** prior), 2.5× fewer demos | intent-grounded space, but untested on AnyBody extrapolation |
| [[2605.20811\|Demo-JEPA]] | target-compatible latent goal | no | **0.36** sim / **0.25** real one-shot (vs [[2412.14803\|VPP]] **0.04**) | demonstration-as-latent-goal, not yet against novel link structures |
| [[2606.03943\|PointAction]] | 3D pointmaps + per-robot decoder | no | real **43.0%** xArm7, **2-2.5×** over baselines | a *third* invariant beside language and latent goal — untested on the wall |
| [[2606.01851\|PHASOR]] | motion phase (FFT + InfoNCE) | no | **90.3%** human→robot retrieval, beats raw-kinematics | invariance via phase, retrieval-validated, not extrapolation SR |
| [[2603.10158\|XL-VLA]] | shared embodiment-invariant VAE action space | partial (4 hands) | **0.72** mean SR over 4 hands (**+40%** over π0) | a fourth invariant, but within-hand-family, not full link-structure extrapolation |
| [[2603.00732\|UniHM]] | morphology-agnostic VQ-VAE tokenizer | partial (hands) | lower MPJPE, higher real grab SR across hands | the shared-tokenizer route, hand-scope, not the AnyBody wall |
| [[2605.25044\|X-DiffVLA]] | morphological-tree diffusion (no per-embodiment head) | no | **+15.3 pp** over π0.5 on RoboCasa | escapes per-robot fine-tuning, untested on extrapolation |
| [[2512.00975\|MM-ACT]] | text+image+action discrete tokens | no | **52.38%** RoboTwin2.0 unseen, up to **40 Hz** | a discrete-token cross-embodiment space, not the link-structure wall |
| [[2606.02745\|SeeTraceAct]] | visibility-aware visual latent plan | no | **+12.5 pp** real one-shot | the demo-as-latent-intermediate route, untested on AnyBody |
| [[2605.30280\|Qwen-VLA]] | embodiment-aware prompts | no | **97.9%** [[2306.03310\|LIBERO]], **76.9%** ALOHA OOD, R2R **57.5%** | the cross-embodiment generalist baseline — but adapts via prompt |
| [[2602.12062\|HoloBrain-0]] | embodiment-prior-aware policy | no | **74.0%** zero-shot [[2510.13626\|LIBERO-Plus]], **+5.65–8.02 pp** over π0.5 | the generalist baseline C2 measures against |
| [[2409.20537\|HPT]] | shared trunk + per-embodiment stems | no (the baseline) | **10–30%** transfer gain | stems tokenize *per robot* — the joint-space baseline C2 challenges |
| [[2510.10274\|X-VLA]] | soft-prompt per platform | no | SOTA 5/6, **93%** [[2306.03310\|LIBERO]] at 1% params | strong, but still *adapts* per platform — not zero-shot extrapolation |
| [[2505.06111\|UniVLA]] | latent-action backbone | no | **95.2%** [[2306.03310\|LIBERO]], **47.1%** [[2004.02857\|R2R-CE]] | cross-task + cross-embodiment latent, not tested on the wall |
| [[2507.23682\|villa-X]] | latent-action cross-embodiment | no | the lineage Demo-JEPA extends | latent-action transfer, not faced with novel link structures |
| [[2212.06817\|RT-1]] | native action tokens | no (the baseline) | foundational cross-embodiment transformer | tokenizes natively — the joint-space precedent C2 inverts |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (an intent-grounded invariant breaks AnyBody's extrapolation wall), with the experiment and the Related-table row it lands on.
1. **H1 — An intent-grounded invariant beats 0% on AnyBody extrapolation.**
   - *Prediction*: running [[2602.10556|LAP]] (language-action), [[2605.20811|Demo-JEPA]] (latent goal), and task-space tokenization head-to-head on [[2505.14986|AnyBody]]'s extrapolation/composition splits, at least one intent-grounded invariant exceeds **30%** SR where joint-space policies score 0%.
   - *Test*: invariant-representation bake-off on the AnyBody extrapolation/composition splits; report SR per invariant.
   - *Row*: AnyBody (the wall) / LAP (language) / Demo-JEPA (latent goal).
   - *Falsifier*: every invariant stays at ~0% on extrapolation → the wall is not a tokenization problem.
2. **H2 — Joint-space failure is memorization, not control learning.**
   - *Prediction*: probing [[2409.20537|HPT]]-style per-embodiment stems shows low representation overlap across morphologies (they memorize body-specific control), explaining the 0% extrapolation.
   - *Test*: measure representation overlap across morphologies for joint-space stems vs an invariant intermediate.
   - *Row*: HPT (per-embodiment stems) / RT-1 (native tokens).
   - *Falsifier*: joint-space stems show high cross-morphology overlap → the 0% isn't memorization and invariance won't fix it.
3. **H3 — Language-intent and latent-goal invariants compose better than either alone.**
   - *Prediction*: combining [[2602.10556|LAP]]'s language intermediate (*what*) with [[2605.20811|Demo-JEPA]]'s latent goal (*how-on-this-body*) beats either alone on AnyBody composition.
   - *Test*: train language-only, latent-goal-only, and composed; evaluate on the composition split.
   - *Row*: LAP (language) / Demo-JEPA (latent goal).
   - *Falsifier*: the composition doesn't beat the better single invariant → the two intermediates are redundant.
4. **H4 — The invariance tax on precision is bounded on seen robots.**
   - *Prediction*: measuring EE error of an invariant-space vs native-joint policy on *seen* robots, the invariant loses bounded precision (a quantifiable tax), so the extrapolation gain isn't free but is worth it.
   - *Test*: report EE precision of invariant vs native-joint on seen robots; bound the tax before claiming extrapolation gains.
   - *Row*: PointAction (pointmap + decoder) / X-DiffVLA (tree diffusion).
   - *Falsifier*: the invariance tax is unbounded (precision collapses on seen robots) → the invariant is unusable for precise control.
5. **H5 — Handoff: the invariant survives the jump from fixed arms to a coupled body, or it doesn't.**
   - *Prediction*: an invariant *task intent* assumes the body is a passive executor, but whole-body loco-manipulation couples that intent to balance and contact — the invariant either survives the jump to a humanoid or coupling breaks it (the instantiation belongs to [[Whole-Body|Whole-Body]]; C2 certifies the cross-family representation it hands off).
   - *Test*: evaluate the AnyBody-validated invariant on a coupled whole-body platform; measure SR retention vs the fixed-arm result.
   - *Row*: Qwen-VLA (manipulation+navigation generalist) / HoloBrain-0 (embodiment-prior generalist).
   - *Falsifier*: the invariant transfers to the coupled body with no loss → intent-invariance is sufficient even under coupling, and the handoff to Whole-Body is unnecessary.

> [!warning] Risks
> - **Invariance may cost precision** — a language/latent action space could blur fine-grained control native joints capture. → H4 bounds the invariance tax on seen robots before claiming extrapolation gains; report the precision floor.
> - **[[2505.14986|AnyBody]]'s 0% may be partly task-hardness, not pure morphology** — extrapolation tasks could be intrinsically harder. → Control with interpolation SR on the *same* tasks; attribute the gap to morphology only if interpolation succeeds.
> - **Language-actions discretize continuous control** — [[2602.10556|LAP]]'s parsing may lose high-frequency detail. → Pair the language intermediate with a knowledge-insulated continuous action expert ([[2602.10556|LAP]]'s own design) rather than acting in language directly.

---

## Cross-Cutting Themes

> [!tip] Latent-Space Prediction Is the Default Substrate
> A1, A2, B3, and C1 share one substrate decision: supervise on video/pixel at training, predict in latent at deployment. A1's joint loop is tractable only because latent rollout is ~10 ms vs pixel ~150 ms; A2's latent CoT keeps step-reward supervision latency-free; B3 makes this the *primary* thesis (latent + Mamba for >30 Hz); C1 carries it into navigation, where [[2603.29165|LatentPilot]]'s in-policy Pilot Token beats external pixel-WMs at **130 ms / 22.8 GB**. [[2603.16666|Fast-WAM]] and [[2511.08544|LeJEPA]] are the shared anchors — the latent must be both cheap and non-collapsing.

> [!tip] Step-Level Verifiable Rewards Beat Outcome-Only Signals
> A2, A3, and B2 all reject the sufficiency of terminal reward. A2 applies [[2604.22074|CIR/SR Reasoning]]'s "outcome rewards don't guarantee causal reasoning" to latent tokens; A3 turns physical laws into per-step verifiable predicates over action sequences; B2 turns each successful recovery into a verified training example. The shared move — swap a single sparse outcome signal for a dense stream of locally-checkable predicates — is the most actionable result the three share.

> [!tip] Detection-Diagnosis-Recovery as a Unified Stack
> B2 builds the loop explicitly; A1, A2, and B1 each supply one face. A1's failure-finder adversary surfaces the perturbations that should trigger detection; A2's CoT-faithfulness probe is a diagnosis instrument; B1's joint causal metric certifies recovery actually closed the loop. [[2602.04411|Self-evolving Embodied AI]]'s 5-module framework is the formalization all four point at.

> [!tip] Efficiency and Safety Are Deployment-Blocking, Not Optional
> B3 makes efficiency a first-class axis; A1, B1, and B2 all assume real-time, so B3's Pareto curve is the enabling condition for the rest. Safety cuts the same way: [[2605.02900|Safety in Embodied AI Survey]]'s five-layer attack taxonomy means B1's joint metric must include adversarial baselines and B2's memory loop must defend against poisoning. [[2505.04769|VLA Concepts Survey]]'s 3–5 Hz ceiling and the Safety survey's cascade-propagation finding are the two anchors that turn "nice to have" into "blocks deployment."

> [!tip] Latent-Beats-External Generalizes From the Bench to the World
> The doc's central architectural bet — predict the control-relevant future in latent space, not pixels — was scoped to fixed-base manipulation in A1 and B3. C1 carries it into *navigation*: [[2603.29165|LatentPilot]]'s in-policy Pilot Token beats external pixel-space world models on [[2004.02857|R2R-CE]] at **130 ms / 22.8 GB** — the same latent-is-cheaper argument A1 makes for the joint loop and B3 makes its primary thesis. [[2506.23468|NavMorph]]'s feature-level RSSM is the navigation analog of [[2411.04983|DINO-WM]]'s manipulation latent planner. The lesson: foresight is a representation choice across mobility *and* manipulation — external-world-model framing is a pixel-space legacy in both.

> [!tip] Structure-Preserving Beats Structure-Discarding
> Don't discard the structure the data carries — the principle A1 and A3 exploit, and the one C2 extends to *bodies*. C2 keeps the *morphology-invariant* task intent that native-joint tokenization throws away ([[2602.10556|LAP]] **>50%** zero-shot, [[2605.20811|Demo-JEPA]] **0.36** one-shot vs [[2505.14986|AnyBody]]'s 0% wall). The same move runs through A1's "the joint $p(o',a)$ is the natural loss" and A3's "physical laws are invariant by construction" — refusing to factor away load-bearing structure, whether that is coupled dynamics, physical law, or morphology-invariant intent. The coupled-whole-body face of this lens is the sibling [[Whole-Body|Whole-Body]] doc's central claim.

> [!tip] Forgetting Is the Tax on Every Loop That Updates Weights
> B4 promotes catastrophic forgetting from a B2 risk-footnote to a direction, and it underwrites every other update loop here. B2's continual recovery updates ([[2510.02298|ARMADA]] pooled-intervention pattern) erase base skills unless B4's subspace protection holds; C1's online CEM self-evolution ([[2506.23468|NavMorph]]) can drift catastrophically at test time; C2's per-embodiment fine-tuning is forgetting across *bodies*, not tasks. [[2605.15735|UAM]]'s **<5%** embodiment tax and [[2510.20685|C-Nav]]'s **+9.7 pp** replay-free retention show the tax is controllable — but only if forgetting is a first-class objective.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Joint-vs-alternating co-training ablation on a fixed latent backbone | A1 | [[2605.21800\|stable-worldmodel]] (OOD harness, but not the joint-vs-alternating grid) + [[2603.25406\|MMaDA-VLA]] (single-objective joint, but offline) |
| Causal faithfulness of latent reasoning under compositional novelty | A2 | [[2606.02277\|RoboSemanticBench]] (reasoning-into-action gap) + [[2510.16281\|SEAL]] (runtime verifier, not a benchmark) |
| Physics-consistency of policy *action* sequences against a verifiable simulator | A3 | [[2605.08567\|ACWM-Phys]] (WM rollouts) + [[2604.17896\|Physical-Feasibility VLA]] (geometric only) |
| Joint WM-action causal-consistency metric on manipulation | B1 | [[2603.22212\|Omni-WorldBench]] (WM-only) + [[2603.22078\|WAM vs VLA Robustness]] (separate axes) + [[2605.06311\|VISER]] (sim-real r, no action causality) |
| Integrated detect-diagnose-recover loops on long-horizon real tasks | B2 | [[2605.10921\|RoboMemArena]] (memory) + [[2506.18123\|RoboArena]] (no recovery stack) |
| Policy SR × control freq × edge-compute Pareto | B3 | [[2306.03310\|LIBERO]] (SR only) + [[2603.13966\|vla-eval]] (training speedup) + [[2605.20774\|VLA-REPLICA]] (real SR, no compute axis) |
| Replay-free continual policy fine-tuning with bounded embodiment tax | B4 | [[2510.20685\|C-Nav]] (continual object-nav, **+9.7 pp** replay-free) + [[2605.15735\|UAM]] (**<5%** tax, no task sequence) + [[1612.00796\|EWC]] (classification/Atari, pre-action-policy) |
| Joint in-policy latent-dreaming + online self-evolution for VLN | C1 | [[2603.29165\|LatentPilot]] (in-policy dreaming, no online evolution) + [[2506.23468\|NavMorph]] (online CEM, not fused with dreaming) |
| Zero-shot extrapolation to novel link structures (morphology-invariant) | C2 | [[2505.14986\|AnyBody]] (**0%** extrapolation wall) + [[2602.10556\|LAP]] (**>50%** zero-shot, untested on [[2505.14986\|AnyBody]]) + [[2605.20811\|Demo-JEPA]] (**0.36** one-shot) |

---

## Cross-References

- [[05_VLA|05_VLA]] — VLA design space (A1, A2, B3, C2)
- [[07_WAM|07_WAM]] — WAM taxonomy: VideoGen / latent / Dreamer / VLM-integrated / efficient / self-evolving (A1, B1)
- [[08_Latent-World-Models|08_Latent-World-Models]] — JEPA evolution + alternative latents (A1, B1, C1)
- [[13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]] — Failure detection, diagnosis, recovery (B2, B4)
- [[11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] — Physics-aware design space (A3)
- [[06_VLA-Reasoning-and-CoT|06_VLA-Reasoning-and-CoT]] — Reasoning insertion slots (A2)
- [[12_Egocentric-Pretraining-and-Human-Video|12_Egocentric-Pretraining-and-Human-Video]] — Egocentric scaling + transfer (B3, C2)
- [[14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]] — Zero-shot sim-to-real + cross-embodiment transfer (A3, C2)
- [[02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]] — Data + sim + benchmark stacks ([[2505.14986|AnyBody]], VLN-CE, LIBERO suites)
- [[07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — Navigation, humanoid, and cross-embodiment paper index (Cluster C)
- [[08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — Canonical survey index
- [[WAM|WAM]] — Sibling research-direction doc: the WAM-internal architecture (representation substrate, contact-mode latent, calibrated imagination) this umbrella's A1 / B1 hand off to.
- [[Manipulation|Manipulation]] — Sibling research-direction doc (arms + hands): grasping, contact-rich assembly, bimanual, dexterous/in-hand; develops the tactile-substrate and manipulation instantiations of C2.
- [[Locomotion|Locomotion]] — Sibling research-direction doc (legs + wheels): bipedal + quadruped locomotion; consumes this doc's C1 (VLN) and C2 (morphology-invariance) mechanisms.
- [[Whole-Body|Whole-Body]] — Sibling research-direction doc (the coupling): whole-body loco-manipulation, mobile manipulation, force-adaptive control; instantiates A1's joint policy and C2's morphology-invariance on the coupled body.
- [[Spatial-4D|Spatial-4D]] — Sibling research-direction doc: 4D scene structure and spatial reasoning the world-model substrate (A1, B1) builds on.
- [[Sim2Real|Sim2Real]] — Sibling research-direction doc: sim-to-real / real-to-sim transfer machinery under A3's physics-consistency and B3/B4's deployment directions.
