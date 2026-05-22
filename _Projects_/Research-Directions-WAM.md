---
title: "Promising Research Directions: World Action Models"
aliases:
  - "WAM Promising Directions"
  - "WAM Research Directions"
tags:
  - research-directions
  - WAM
  - embodied-AI
  - world-model
status: draft
created: 2026-05-17
modified: 2026-05-18
---

# Promising Research Directions: World Action Models

> [!info] Scope
> Eight WAM research directions across three clusters — *Theory & Architecture*, *Training & Grounding*, *Evaluation & Deployment* — anchored on 30 WAM surveys, five Embodied-AI deep-dives, and verbatim alphaxiv quotes from 10 surveys.

---

## Methodology

- **Survey enumeration**: 8 pure-WAM + 22 adjacent surveys from `_KnowledgeHub_/`; cross-checked against [[General/08_Benchmarks-and-Surveys|General/08]] §4–§7.
- **alphaxiv verification**: verbatim quotes from `https://www.alphaxiv.org/overview/{ID}.md` for 10 anchor surveys.
- **Deep-dive mining**: full reads of [[04_WAM]], [[05_Latent-World-Models]], [[06_Self-Evolving-VLA-WAM]], [[07_Physics-Aware-Embodied-AI]], [[11_Sim-to-Real-Transfer]]; 3+-way open-problem convergence seeded A2, A3, B2.

---

## WAM Survey Landscape

| Survey | Sub-theme | Topic |
|---|---|---|
| [[2605.12090\|WAM Survey]] | A: Core WAM | Formal $p(o', a \| o, l)$; Cascaded vs Joint taxonomy; 6 open challenges |
| [[2605.00080\|WM Robot Survey 2026]] | A: Core WAM | Decoupled → unified VLA/MoE/MoT; latent WM as dominant |
| [[2510.16732\|World Models for Embodied AI Survey]] | A: Core WAM | Three-axis taxonomy (Functionality × Temporal × Spatial) |
| [[2511.02097\|WM Manipulation Survey]] | A: Core WAM | 13 essential capabilities; Implicit / Latent Dynamics / Video Generation |
| [[2411.14499\|World Models Survey 2024]] | A: Core WAM | Implicit representation vs future-state prediction |
| [[2604.16592\|Cognition WM Survey]] | A: Core WAM | Video / Embodied / Epistemic WMs |
| [[2604.04707\|OpenWorldLib]] | A: Core WAM | Unified video + 3D + VLA + multimodal reasoning |
| [[2602.01630\|WM Research Critical Assessment]] | A: Core WAM | 5-module unified framework; fragmentation diagnosis |
| [[2604.22748\|Agentic World Modeling Survey]] | A: Core WAM | L1/L2/L3 capability hierarchy; ASR + COD metrics |
| [[2506.20134\|3D World Models Survey]] | A: Core WAM | 2D-to-3D paradigm shift |
| [[2503.04641\|Multimodal Generative Models Survey]] | A: Core WAM | 2D → Video → 3D → 4D progression |
| [[2509.20021\|Embodied AI LLM-WM Survey]] | A: Core WAM | Joint MLLM + WM roadmap |
| [[2503.21765\|Physics Cognition Survey]] | B: Physics-as-WAM | Basic / Passive / Active cognitive tiers |
| [[2510.04978\|Physical AI Survey]] | B: Physics-as-WAM | "Statistical correlations only; causal understanding missing" |
| [[2501.10928\|Generative Physical AI Survey]] | B: Physics-as-WAM | 6-paradigm taxonomy; functional vs visual realism gap |
| [[2601.15533\|Actionable Simulators]] | B: Physics-as-WAM | "Dynamical hallucinations"; closed-loop eval |
| [[2601.07823\|Video Generation in Robotics Survey]] | B: Physics-as-WAM | Hallucinations + physics violations as top-2 of 10 challenges |
| [[2604.04974\|Video-to-Control Survey]] | B: Video-as-WAM | Implicit / abstract / explicit interfaces; robotics integration gap |
| [[2603.28489\|Video Gen as WM Survey]] | C: Eval & Deploy | Efficiency-focused 3D taxonomy; efficiency as prerequisite |
| [[2604.15911\|Efficient Video Diffusion Survey]] | C: Eval & Deploy | KV-cache bottleneck; step distillation / sparse attention / quantization |
| [[2602.04411\|Self-evolving Embodied AI]] | C: Eval & Deploy | 5 co-evolving modules |
| [[2604.02029\|Latent Space Survey]] | C: Eval & Deploy | Evaluability / controllability / interpretability gaps |
| [[2504.21853\|Interactive Generative Video Survey]] | C: Eval & Deploy | Real-time vs quality trade-off |
| [[2507.00917\|Embodied Intelligence Survey]] | C: Eval & Deploy | IR-L0 to IR-L4; simulators × WMs |
| [[2605.03941\|iWorld-Bench]] | C: Eval & Deploy | First standardized interactive WM evaluation |
| [[2505.07634\|Neural Brain Framework]] | C: Eval & Deploy | Sensing / PCA / memory / neuromorphic HW |
| [[2505.05108\|Multi-agent Embodied AI Survey]] | C: Eval & Deploy | Self-evolution in open environments as top gap |
| [[2508.07407\|Self-Evolving AI Agents Survey]] | C: Eval & Deploy | Foundation models → lifelong agents |
| [[2507.21046\|Self-Evolving Agents Survey]] | C: Eval & Deploy | What/When/How/Where to Evolve |
| [[2310.06253\|Objective-Mismatch Survey]] | C: Eval & Deploy | MBRL objective mismatch; decision-aware MBRL fix |
| [[2512.24385\|Spatial Intelligence Pre-training Roadmap]] | C: Eval & Deploy | Generative WM × spatial reasoning |

**Cross-survey patterns** (N = number of independently converging surveys): joint causal-consistency (5), physical grounding (5), efficiency as deployment prerequisite (3), definition fragmentation (meta-pattern — the field is pre-paradigmatic).

---

## WAM Formal Framing

**Probabilistic** — [[2605.12090|WAM Survey]]:

> "WAMs are defined as embodied foundation models that integrate predictive state modeling with action generation, moving beyond merely predicting actions to predicting a joint distribution over future states and actions." — [[2605.12090|WAM Survey]]

$$\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o,l,o',a) \sim \mathcal{D}} \big[ -\log p(o', a \mid o, l) \big]$$

| Family | Joint distribution | Predicts |
|---|---|---|
| **VLA** | $p(a \mid o, l)$ | Action only; no dynamics |
| **WM** | $p(o' \mid o, a)$ | Dynamics only; no action |
| **WAM** | $p(o', a \mid o, l)$ | Both; the unifying frontier |

WAMs split into **Cascaded** (predict state, derive action via inverse dynamics) vs **Joint** (unified end-to-end). Most "joint" methods are actually Cascaded — Joint is the architectural frontier.

**Architectural** — [[2510.16732|World Models for Embodied AI Survey]]:

> "The world models are categorized along three axes: Functionality (Decision-Coupled vs General-Purpose), Temporal Modeling (Sequential Simulation vs Global Difference Prediction), and Spatial Representation (Global Latent Vector, Token Feature Sequence, Spatial Latent Grid, Decomposed Rendering Representation)." — [[2510.16732|World Models for Embodied AI Survey]]

Spatial axis trajectory: latent vectors → token sequences → explicit 3D rendering (NeRF, 3DGS).

**Capability hierarchy** — [[2604.22748|Agentic World Modeling Survey]]:

> "We introduce three capability levels: L1 Predictor, which learns one-step local transition operators; L2 Simulator, which composes them into multi-step, action-conditioned rollouts that respect domain laws; and L3 Evolver, which autonomously revises its own model when predictions fail against new evidence." — [[2604.22748|Agentic World Modeling Survey]]

Physical-law L3 Evolver is "emerging not mature" — the target for B3. ASR + COD anchor C1.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Synergy |
|---|---|---|---|
| **A — Theory & Architecture** | A1, A2, A3 | Right latent for joint imagination + action | A2's hybrid latents are A1's substrate; A3 extends both into tactile |
| **B — Training & Grounding** | B1, B2, B3 | Imagination diverges from physical reality | B1's physics + B2's contact awareness stabilize B3's self-evolution |
| **C — Evaluation & Deployment** | C1, C2 | Joint causal metric + cheap to compute | C1 verifies that C2's efficient WAMs preserve quality under speed |

---

## Cluster A — WAM Theory & Architecture

#### **A1: Single-Loop Co-Evolving WAM + Policy**

**Thesis.** Move beyond alternating WAM↔Policy co-improvement to a **unified single-step gradient** where action and imagination losses jointly update both networks in the same optimizer step, in latent space for real-time feasibility.

> "The design space has progressively expanded toward single-backbone, unified VLA, and latent world-modeling approaches with tighter integration between prediction and action generation." — [[2605.00080|WM Robot Learning Survey]]

**State of evidence**

- [[2510.16732|World Models for Embodied AI Survey]] and [[2511.02097|WM Manipulation Survey]] independently converge on structured latent + joint architectures as the trajectory.
- Current "joint" implementations fall short: [[2602.12063|VLAW]] alternates; [[2603.16666|Fast-WAM]] drops the WM at deployment; [[2605.15153|Pelican-Unified]] unifies architecturally but trains multi-stage; [[2511.09515|WMPO]] and [[2511.15605|SRPO]] freeze the WM during inner RL.

**Concrete research questions**

- Q1 — **Unified GRPO in latent space.** $\mathcal{L} = \mathbb{E}[A \cdot \log \pi(a, \hat{z}_{t+1} \mid s_t)]$ on a pretrained latent WAM ([[2504.02792|UWM]] or [[2602.10098|VLA-JEPA]]); single backward pass updates both heads.
- Q2 — **Reward decomposition.** Task + latent-consistency ($\hat{z}_{t+1}$ vs encoder's $z_{t+1}$) + action-quality; latent provides the dense signal sparse task reward cannot.
- Q3 — **Knowledge insulation.** Extend [[2505.23705|Knowledge Insulation VLA]]'s stop-gradient pattern to the WAM encoder; preserves pretrained physics priors during RL.

**Related research papers**

| Paper | Contribution | Gap addressed |
| --- | --- | --- |
| [[2602.12063\|VLAW]] | Iterative WAM+VLA co-improvement | Cascaded; WM trains on stale policy data |
| [[2603.19370\|VAMPO]] | GRPO over video-denoising-as-MDP | Pixel-space; not real-time |
| [[2511.09515\|WMPO]] | On-policy GRPO in imagination | WM frozen during inner loop |
| [[2511.15605\|SRPO]] | Frozen V-JEPA-2 + trajectory clustering | WM never updates |
| [[2605.15153\|Pelican-Unified]] | Shared latent z; 93.5% RoboTwin | Multi-stage training |
| [[2605.10942\|HarmoWAM]] | Dual experts + adaptive gating; 89% in-domain | Gating learned post-hoc |
| [[2602.10098\|VLA-JEPA]] | JEPA WM + flow-matching head; 97.2% LIBERO | Action head and WM trained separately |
| [[2605.00078\|Being-H0.7]] | Future-informed dual-branch; 3–4 ms/step | Privileged future supervision is offline |
| [[2504.02792\|UWM]] | Unified action-conditioned + video diffusion | Latency cost still high |
| [[2605.06732\|On Training in Imagination]] | Theoretical bounds + budget allocation for MBRL imagination | Theory only; not yet wired into latent joint loop |

**Benchmarks & metrics**

| Benchmark | What it measures | Why it matters |
| --- | --- | --- |
| [[2306.03310\|LIBERO]] | In-distribution SR; best **97.2%** | Joint loop must not hurt in-dist |
| [[2510.13626\|LIBERO-Plus]] | 10,030-perturbation OOD; best **79.5%** | Joint loop should improve OOD over alternating |
| [[2603.22212\|Omni-WorldBench]] | WM causal consistency | Verifies WM half respects action conditioning |
| [[2506.18123\|RoboArena]] | Real-fleet cross-platform | Real-world translation |

**Risks**

- **Chasing problem**: simultaneous updates → WM models obsolete policy. Mitigate via EMA targets.
- **Reward hacking on latent consistency**: gameable by collapsing the latent. [[2511.08544|LeJEPA]]'s Euclidean regularization defends.
- **No published joint-vs-alternating ablation on fixed backbone** — first-paper opportunity.

#### **A2: Hybrid Latent+Pixel WAM Architectures**

**Thesis.** Resolve the latent-vs-pixel trade-off (latent fast/opaque vs pixel slow/robust) via **hybrid architectures**: train-time pixel co-prediction + test-time latent rollout; semantic latents + decoder for inspection; dual experts with process-adaptive gating.

> "World models in robotic manipulation can be categorized into three primary paradigms: Implicit World Modeling, Latent Dynamics Modeling, and Video Generation, detailing their respective strengths and limitations." — [[2511.02097|WM Manipulation Survey]]

**State of evidence**

- [[2510.16732|World Models for Embodied AI Survey]]: "An evolutionary trend from compact global latent vector representations (e.g., RSSMs) towards token feature sequences (e.g., Transformers with LLMs) and explicit 3D rendering representations (e.g., NeRF, 3D Gaussian Splatting) is observed." Hybrids occupy multiple axis points — currently unexplored.
- [[2605.06388|Semantic-LDM-WM]]: semantic-aligned latents beat reconstruction VAEs by **+9.8 pp** closed-loop and **+13.6 pp** OOD; encoding quality matters more than the latent-vs-pixel dichotomy. [[2604.02029|Latent Space Survey]] names evaluability / interpretability as the pure-latent gap — pixel branches resolve these without test-time cost.
- [[04_WAM]] §6 diagnoses VideoGen 4.8× slower but most robust; latent fast but opaque. [[05_Latent-World-Models]] §6 names interpretability + latent-pixel alignment as 2 of 4 open problems.

**Concrete research questions**

- Q1 — **Hybrid training, single-branch deployment.** Extend [[2603.16666|Fast-WAM]]: joint pixel + latent objectives at train, latent-only at deploy (~10 ms vs ~150 ms). Measure OOD retention from pixel co-training.
- Q2 — **Shared latent z across modalities.** Can [[2605.15153|Pelican-Unified]]'s shared z anchor a hybrid where imagination decodes to pixel (interpretable) and action decodes to latent (fast)?
- Q3 — **Process-adaptive gating beyond [[2605.10942|HarmoWAM]].** Gate latent-only (transit) vs pixel-aided (interaction) based on contact prediction.
- Q4 — **Semantic vs reconstruction latents under hybrid training.** Does [[2605.06388|Semantic-LDM-WM]]'s single-branch result persist when a pixel branch supervises training?

**Related research papers**

| Paper | Contribution | Gap addressed |
| --- | --- | --- |
| [[2603.16666\|Fast-WAM]] | Train video, test latent | Drops WM at test; no test-time imagination |
| [[2605.06388\|Semantic-LDM-WM]] | Semantic vs reconstruction; +9.8 pp closed-loop | Single-branch only |
| [[2605.10942\|HarmoWAM]] | Dual experts + adaptive gating; 89% in-domain | Both experts in latent |
| [[2602.10098\|VLA-JEPA]] | Pure latent: 97.2% LIBERO | No pixel decoder for interpretation |
| [[2605.15153\|Pelican-Unified]] | Shared latent z; 93.5% RoboTwin | Pixel-side generator; deployment latency open |
| [[2504.02792\|UWM]] | Unified action-conditioned + video | Single-stream |
| [[2511.08544\|LeJEPA]] | Provable Euclidean latent geometry | Pure latent — regularization anchor |
| [[2411.04983\|DINO-WM]] | Frozen DINOv2 + lightweight dynamics | No pixel verification |
| [[2605.00078\|Being-H0.7]] | Dual-branch deployable+privileged; 3–4 ms/step | Both branches latent |
| [[2605.15618\|Latent Video Prediction WMs]] | Systematic latent-vs-pixel SSL eval under perturbations | Pretrain-only; no policy joint |

**Benchmarks & metrics**

| Benchmark | What it measures | Why it matters |
| --- | --- | --- |
| [[2510.13626\|LIBERO-Plus]] | 10,030 OOD perturbations | Match pure-latent in-dist; gain OOD over latent-only |
| Inference latency (Hz) | A100 forward latency | Latent ~10 ms vs pixel ~150 ms |
| Interpretability probes | Visual inspection of pixel-decoded futures | Verify pixel branch preserves dream quality |
| [[2603.22078\|WAM vs VLA Robustness]] | 4.8× latency cost | Hybrid must show <2× cost vs pure latent at pixel-WAM OOD |

**Risks**

- **Two-branch training cost** dominates compute. Mitigate by distilling a pre-trained pixel WM into the latent encoder.
- **Latent-pixel divergence** without shared parameters — need explicit alignment loss.
- **Saturated regime**: pure latent already at 97% LIBERO; contribution must show on OOD + interpretability.

#### **A3: Tactile/Force-Integrated WAM Imagination**

**Thesis.** Current WAMs imagine visual + proprioceptive futures but rarely **tactile/force futures**, despite force being the dominant signal in contact-rich manipulation. Build force-conditioned WAMs that imagine wrench trajectories alongside visual ones.

> "Multimodal Physical State Representation: The need to move beyond RGB to include tactile, force, and acoustic feedback for contact-rich manipulation." — [[2605.12090|WAM Survey]] (one of six core open challenges)

**State of evidence**

- [[2605.12090|WAM Survey]] explicitly names the modality gap. [[2511.02097|WM Manipulation Survey]]'s 13 capabilities put Multimodal Perception first and Physics Awareness third. [[2604.27621|Robot Learning from Human Videos Survey]] and [[2604.16592|Cognition WM Survey]] independently name tactile as the contact-grounding modality.
- All existing tactile work treats force as *policy input*, never *WAM imagined output*: [[2603.15169|ForceVLA2]], [[2601.20321|TaF-VLA]] (60.3% cross-sensor), [[2506.14754|Sparsh-X]] (encoder only), [[2603.15257|HapticVLA]] (distillation sidesteps the problem).

**Concrete research questions**

- Q1 — **Wrench-trajectory prediction head.** Add 6-DoF wrench head to a JEPA WAM; train on [[2506.14754|Sparsh-X]]'s 1M contacts.
- Q2 — **Tactile latent as cross-sensor bridge.** Use [[2601.20321|TaF-VLA]]'s VQ-VAE force latent as WAM imagination target; decode per-sensor on demand.
- Q3 — **Imagined-vs-measured force as auxiliary loss.** Train-time supervised; deploy-time used as proprioceptive forecast.
- Q4 — **Contact-event as discrete latent transition.** Make/break as categorical; continuous force only in contact regime.
- Q5 — **Force-conditioned video prediction inverse.** Run [[2505.19386|Force Prompting]] backward: predict force from frames, condition next-step on predicted force.

**Related research papers**

| Paper | Contribution | Gap addressed |
| --- | --- | --- |
| [[2605.12090\|WAM Survey]] | Names the modality gap | Survey only; no method proposed |
| [[2506.14754\|Sparsh-X]] | Multisensory touch foundation (1M contacts) | Encoder only; no prediction head |
| [[2601.20321\|TaF-VLA]] | VQ-VAE force latent; 60.3% cross-sensor | Latent is policy-consumed, not WM-predicted |
| [[2603.15257\|HapticVLA]] | Teacher-student tactile distillation; 86.7% SR | Sensor-free deployment; force not modeled in WM |
| [[2603.15169\|ForceVLA2]] | Cross-scale MoE + force prompts; 66% avg SR | Force is policy input, not predicted output |
| [[2605.13083\|TouchAnything]] | Multi-view egocentric + dense tactile | Dataset only; no WAM consumer |
| [[2505.19386\|Force Prompting]] | Force-conditioned video generation | Generation side |
| [[2509.18830\|DexSkin]] | Capacitive tactile sensor (294° coverage) | Sensor hardware |
| [[2509.07962\|TA-VLA]] | Torque-aware VLA design study | Policy-side only |

**Benchmarks & metrics**

| Benchmark | What it measures | Why it matters |
| --- | --- | --- |
| [[2510.25725\|HumanoidVTA]] | 2,124-sensor humanoid tactile | Substrate for imagined-vs-measured force |
| ForceVLA-Data (244 traj) | Contact-rich 5-task | Test WAM imagination on existing force-aware benchmark |
| AutoMate assembly | 8 industrial tasks; [[2603.15956\|ExpertGen]] **90.5%** | Contact-rich tasks where imagined force matters |

**Risks**

- **Noise floor**: subtle slip / microvibration not in vision — imagined force may plateau below measured.
- **Cross-sensor brittleness**: 60.3% zero-shot is not deployment-ready.
- **No published WAM with tactile prediction head** — genuinely unattacked.

---

## Cluster B — WAM Training & Grounding

#### **B1: Verifiable Physics-Consistent WAM Training**

**Thesis.** Bridge [[2604.04974|Video-to-Control Survey]]'s "robotics integration layer" gap by training WAMs with verifiable physics predicates (momentum, contact, friction) on *imagined* state trajectories — not only on *generated* pixels.

> "Modern video generation models often produce visually impressive content that lacks physical plausibility, such as objects defying gravity or passing through each other. Even state-of-the-art video generation models still fall short of human-level physics understanding, particularly in complex scenarios involving multiple interacting objects or fluid dynamics." — [[2503.21765|Physics Cognition Survey]]

**State of evidence**

- [[2604.04974|Video-to-Control Survey]] names physical feasibility as one of three missing layers between video and dependable control. [[2510.04978|Physical AI Survey]] generalizes: "statistical correlations only, no causal understanding." [[2601.15533|Actionable Simulators]] coins *dynamical hallucinations*; [[2601.07823|Video Generation in Robotics Survey]] ranks them top-2 of 10 challenges.
- Physics-aware video generators ([[2509.21309|NewtonGen]], [[2510.13809|PhysMaster]], [[2512.00425|NewtonRewards]], [[2603.13770|PhysAlign]]) haven't been tested on the WAM imagination → policy chain. Closest bridges: [[2604.17896|Physical-Feasibility VLA]] (geometric loss on actions; 22 → 43.50% SSR); [[2603.23376|ABot-PhysWorld]] (Diffusion-DPO on generation).

**Concrete research questions**

- Q1 — **Physics predicate set over WAM-imagined state**: P1 momentum $|\Delta p_{\text{total}}| < 0.05 \cdot p_{\max}$ over 1s; P2 no inter-object penetration; P3 anti-gravity check $\Delta z \sim -\frac{1}{2}gt^2 \pm 10\%$; P4 Newton's 3rd law on contact wrenches; P5 Coulomb $|F_t| \leq \mu |F_n|$.
- Q2 — **WAM-level vs action-level physics rewards.** Three-way ablation per implicit / abstract / explicit interface taxonomy; matched FLOPs; SSR on LIBERO-Plus + 20-task physics gauntlet.
- Q3 — **WAM-DPO with physics-rejected negatives.** Extend [[2603.23376|ABot-PhysWorld]]'s DPO to WAM imagination; $\beta(\log p_\theta(o'_+) - \log p_\theta(o'_-)) > 0$ ≥90% on 1,000 held-out pairs.
- Q4 — **Sim-to-real validation chain.** Train with predicates in [[2511.04665|Real-to-Sim GS]] twins → eval sim → twin → real; target SR retention $\geq 0.70$ (physics-naive: 0.50–0.60).
- Q5 — **Reward-hacking diagnostics**: imagined-state variance (collapse), Pearson $\rho$ between $\sum P_i$ and SR (gaming), [[2412.02818|RoboMD]] adversarial probing.

**Related research papers**

| Paper | Contribution | Gap addressed |
| --- | --- | --- |
| [[2604.04974\|Video-to-Control Survey]] | Names robotics integration gap | Survey only; no method proposed |
| [[2604.17896\|Physical-Feasibility VLA]] | Geometric loss on actions; 22→43.50% SSR | Geometric only; on actions |
| [[2603.23376\|ABot-PhysWorld]] | Diffusion-DPO with physics-rejected negatives | Generation side |
| [[2509.21309\|NewtonGen]] | Neural Newtonian T2V | Video only |
| [[2512.00425\|NewtonRewards]] | Newton's laws as verifiable RL reward | Generation side |
| [[2509.20570\|PIRF]] | PDE residual rewards | Generation; no WAM-state path |
| [[2510.13809\|PhysMaster]] | RL fine-tune of video diffusion w/ physics rep | Generation side |
| [[2603.13770\|PhysAlign]] | Feature + 3D-rep alignment | Generation side |
| [[2511.07416\|PhysWorld]] | Policy vs learned physical WM; 82% real SR | Positions/velocities only |
| [[2503.15558\|Cosmos-Reason1]] | Physical commonsense + embodied reasoning | Reasoning, not predicates |
| [[2605.06593\|ReActor]] | Bilevel RL + physics sim; +15.22 pp | Motion retargeting only |
| [[2605.15458\|Video-RLVR]] | RL with verifiable rewards on video diffusion | Generation side; no WAM-imagined-state path |

**Benchmarks & metrics**

| Benchmark | What it measures | Why it matters |
| --- | --- | --- |
| [[2410.05363\|PhyGenBench]] | Physical commonsense; best T2V **0.51/3.0** PCA | Threshold for WAM-imagined-state physics |
| [[2503.06800\|VideoPhy-2]] | Action-centric physical reasoning; best **32.6%** joint | Closest physics-on-action benchmark |
| [[2501.09038\|Physics-IQ]] | Whether models *understand* physics | Visual-quality vs physics-correctness gap |
| [[2504.02918\|Morpheus]] | Real-physical-experiment benchmark | Real-physics ground truth |
| LIBERO-Plus + 20-task physics gauntlet | Action-level SSR | Target: 43.50% → >55% |

**Risks**

- **Verifiable physics scales poorly**: writing predicates for cluttered scenes is hard ([[2509.20570|PIRF]]); learned verifiers generalize poorly.
- **Physics-consistent imagination ≠ physics-consistent action** — the gap to measure; if small, direction collapses.
- **No benchmark scores physics-consistency of WAM-imagined sequences** — first-paper deliverable.

#### **B2: Contact-Aware WAM for Fine Manipulation**

**Thesis.** Latent WAMs excel at trajectories but fail at insertion/assembly because contact physics is **locally non-smooth** (make/break, slip, normal-force singularities). Build contact-aware WAMs that model contact events as discrete latent transitions — addressing the 3-way recurring open problem across [[05_Latent-World-Models]] §6, [[07_Physics-Aware-Embodied-AI]] §8, and [[11_Sim-to-Real-Transfer]] §7.

> "Learned sims blur on contact: UniSim and Cosmos produce stunning visuals but physical contact regions (collisions, friction transients) look implausible to robots." — [[11_Sim-to-Real-Transfer]] §7 (vault deep-dive, anchored by [[2310.06114|UniSim]] and [[2501.03575|Cosmos]] alphaxiv overviews)

**State of evidence**

- 3-way deep-dive convergence: latent WAMs excel at trajectories but fail sub-millimeter contact; verifiable physics scales poorly to cluttered scenes; learned sims blur on contact.
- Closest substrates: [[2503.17973|PhysTwin]] (deformable digital twin; no discrete events); [[2511.07416|PhysWorld]] (continuous physical WM; 82% real SR); [[2604.27367|DOT-Sim]] (differentiable optical tactile; contact ground truth but no WAM consumer).
- Pattern: [[2602.23253|SPARR]] **95–100%** AutoMate; [[2603.15956|ExpertGen]] **90.5%** AutoMate. All policy-side improvements; contact events as first-class WAM latent has not been explored.

**Concrete research questions**

- Q1 — **Discrete contact-mode latent** $c_t \in \{\text{no-contact, making, in-contact, breaking, slipping}\}$; predict $c_t$; condition continuous latent dynamics on $c_t$.
- Q2 — **Contact-mode-conditional physics losses**: Coulomb only in `in-contact`; ballistic only in `no-contact`.
- Q3 — **Contact-event time prediction** as auxiliary regression head $\hat{t}_{\text{contact}}$ with simulator supervision.
- Q4 — **Distillation from [[2604.27367|DOT-Sim]]** as teacher; distill contact dynamics into WAM latent.
- Q5 — **Sim-to-real on AutoMate / NIST**: train on [[2511.04665|Real-to-Sim GS]] twins; eval on real AutoMate.

**Related research papers**

| Paper | Contribution | Gap addressed |
| --- | --- | --- |
| [[2503.17973\|PhysTwin]] | Physics-informed deformable twin from video | No discrete contact mode |
| [[2511.07416\|PhysWorld]] | Policy vs learned physical WM; **82%** real SR | Continuous; no event discretization |
| [[2604.27367\|DOT-Sim]] | Differentiable MPM + tactile; **96.6%** tumor detection zero-shot | No WAM consumer |
| [[2603.15956\|ExpertGen]] | Generative prior + DSRL + distillation; **90.5%** AutoMate | Policy-side |
| [[2602.23253\|SPARR]] | Sim + vision-conditioned real residual; **95–100%** AutoMate | Policy-side; no WAM |
| [[2603.16861\|MolmoBot]] | 232K-env procedural MuJoCo; **79.2%** real Franka FR3 | Domain randomization only |
| [[2511.04665\|Real-to-Sim GS]] | 3DGS + soft-body PhysTwin; **r > 0.9** sim-real | Evaluation substrate |
| [[2604.24916\|asRoBallet]] | Friction-aware MuJoCo + RL | Prior for contact-mode losses |
| [[2604.23702\|QuietWalk]] | PINN GRF predictor + curriculum | Analog of contact-force prediction |

**Benchmarks & metrics**

| Benchmark | What it measures | Why it matters |
| --- | --- | --- |
| AutoMate (8 tasks) | Insertion / assembly SR | **90.5%** is the WAM-naive baseline |
| NIST industrial assembly | Cross-task assembly | **+74.5%** SPARR transfer on unseen NIST |
| [[2511.04665\|Real-to-Sim GS]] deformable | Plush packing, rope routing, T-block pushing | Soft-body contact — where latent WAMs fail hardest |
| Contact-mode classification accuracy | $c_t$ vs simulator | Internal diagnostic before downstream gains |

**Risks**

- **Discrete latent optimization**: Gumbel-softmax / REINFORCE variance; start soft, harden over training.
- **Contact-mode supervision requires simulator**: real labels not available.
- **No published WAM with discrete contact-event latent** — genuinely unattacked.

#### **B3: WAM-Driven Self-Evolution & Recovery**

**Thesis.** Use WAM imagination as **safe practice substrate** for closed-loop self-improvement: failure-finder → WAM dreams failures → GRPO over joint (action, imagination) log-prob → recovery via FPC-VLA-style corrective head. Target [[2604.22748|Agentic World Modeling Survey]]'s L3 Evolver — "emerging not mature" for physical-world WAMs.

> "L3 Evolver, which autonomously revises its own model when predictions fail against new evidence." — [[2604.22748|Agentic World Modeling Survey]]

**State of evidence**

- [[2604.22748|Agentic World Modeling Survey]] defines L1/L2/L3 and names physical L3 as the gap. [[2602.04411|Self-evolving Embodied AI]]'s 5-module framework (memory / task / environment / embodiment / model) is canonical; [[2508.07407|Self-Evolving AI Agents Survey]], [[2507.21046|Self-Evolving Agents Survey]], [[2505.05108|Multi-agent Embodied AI Survey]] all name open-environment self-evolution as the top unresolved capability.
- 2026 components: [[2506.24119|SPIRAL]] (CriticAgent filters dreams), [[2502.05907|EvoAgent]] (+105% Minecraft), [[2511.16166|EvoVLA]] (first end-to-end self-evolving VLA), [[2510.16079|EVOLVER]] (trajectory → principles), [[2604.18131|Native Evolution]] (reward-free self-evolution). The gap: **none integrates detection + diagnosis + recovery + memory + WAM-driven imagination end-to-end** under the L3 Evolver framing.

**Concrete research questions**

- Q1 — **WAM-driven failure-finder.** Recast [[2412.02818|RoboMD]] as adversary; failure-finder proposes initial states; WAM rolls forward; policy judged on imagined outcomes.
- Q2 — **GRPO over joint (action, imagination) log-prob.** A1 provides inner optimizer; B3 wraps outer self-evolution. Reward = task SR in imagination + COD + [[2509.15194|EVOL-RL]] novelty.
- Q3 — **Recovery via WAM-imagined alternatives.** On [[2510.09459|FIPER]] / [[2506.09937|SAFE]] detection, WAM dreams N candidates; pick highest imagined SR.
- Q4 — **Misevolution prevention**: [[2506.07468|SELF-REDTEAM]] in imagination; [[2509.15194|EVOL-RL]] for entropy collapse.
- Q5 — **Continual update from recoveries**: [[2401.16650|WMAR]]-style FIFO + reservoir; **+0.071** vs 0.665 baseline forgetting.

**Related research papers**

| Paper | Contribution | Gap addressed |
| --- | --- | --- |
| [[2604.22748\|Agentic World Modeling Survey]] | L1/L2/L3; physical L3 emerging | Survey only; no L3 method proposed |
| [[2502.05907\|EvoAgent]] | Continual WM; **+105%** Minecraft | Minecraft domain only; no physical manipulation |
| [[2506.24119\|SPIRAL]] | CriticAgent filters dreams | Critic filter only; no full self-evolving loop |
| [[2511.16166\|EvoVLA]] | First end-to-end self-evolving VLA | VLA only; no WAM imagination driving evolution |
| [[2510.16079\|EVOLVER]] | Trajectory → strategic principles | Behavior-level only; no WAM imagination |
| [[2603.19370\|VAMPO]] | GRPO over video denoising | Pixel-space template; not the joint latent loop |
| [[2412.02818\|RoboMD]] | RL adversary for failure discovery | Probes real robot; not driven by WAM imagination |
| [[2510.09459\|FIPER]] | Predictive failure via OOD + uncertainty | Detection only; no recovery |
| [[2506.09937\|SAFE]] | Internal-feature + conformal prediction | Detection only; no recovery |
| [[2509.04018\|FPC-VLA]] | Failure prediction + corrective action | No WAM-imagined alternatives at recovery |
| [[2510.02298\|ARMADA]] | FLOAT detector + multi-robot; **95%** accuracy | Real-fleet only; not WAM-driven |
| [[2509.26354\|Misevolution]] | Identifies risk class | Diagnosis only; no in-loop mitigation |
| [[2506.07468\|SELF-REDTEAM]] | Adversarial self-play | Pre-deployment safety check; not integrated in loop |
| [[2509.15194\|EVOL-RL]] | Novelty prevents entropy collapse | Standalone regularizer; not in WAM-driven loop |
| [[2605.14733\|Video-Zero]] | Self-evolution video understanding via self-play | Understanding only; no action grounding |
| [[2605.14539\|Correction-Oriented PO]] | RL from failure traces with verifiable rewards | Language traces; needs VLA/WAM extension |

**Benchmarks & metrics**

| Benchmark | What it measures | Why it matters |
| --- | --- | --- |
| [[2605.10921\|RoboMemArena]] | Memory-dependent SR; **68.9%** subtasks need history | Recovery must consult memory |
| Continual improvement curves | Per-cycle SR | Per [[2507.21046\|Self-Evolving Agents Survey]] rubric |
| Catastrophic forgetting probes | SR retention across sequential tasks | [[2401.16650\|WMAR]] **+0.071** vs 0.665 baseline |
| WAM-imagined-vs-real SR Pearson $\rho$ | Predictive validity | Validates loop is grounded |

**Risks**

- **Misevolution drift**: self-reward biases amplify; red-team after each cycle.
- **Reward hacking on imagined SR**: model games WAM not real; periodic real-robot validation + novelty bonuses.
- **WAM drifts from real dynamics**: outer-loop WAM updates ([[2603.04029|Self-Adapting RL]]).

---

## Cluster C — WAM Evaluation & Deployment

#### **C1: Joint Causal-Consistency WAM/Policy Evaluation**

**Thesis.** Build the first standardized benchmark that jointly measures whether a WAM's *imagined future* is causally bound to the *action it then takes* — closing the 5-survey-converged evaluation gap. Anchor on [[2604.22748|Agentic World Modeling Survey]]'s ASR + COD framework.

> "Most approaches focus on injecting world knowledge into isolated, task-specific systems—such as visual prediction, 3D estimation, symbol grounding, image editing, or autonomous driving. While these integrations often yield performance gains on specific benchmarks, the paper argues that they fundamentally lack the systematic coherence required for a holistic understanding of the world." — [[2602.01630|WM Research Critical Assessment]]

**State of evidence**

- 5-way convergence: [[2605.12090|WAM Survey]] names *"absence of joint metrics that causally link predicted futures to executed actions"*; [[2605.00080|WM Robot Learning Survey]] demands eval *"beyond visual fidelity for action faithfulness, physical consistency, controllability"*; [[2510.16732|World Models for Embodied AI Survey]] cites physically-consistent metrics as fundamental; [[2601.15533|Actionable Simulators]] demands *"closed-loop, decision-oriented evaluation"*; [[2601.07823|Video Generation in Robotics Survey]] ranks robotics-centric eval as top challenge.
- [[2604.22748|Agentic World Modeling Survey]] proposes the framework: ASR + COD as decision-centric anchor metrics. [[2310.06253|Objective-Mismatch Survey]] generalizes: predictive WM loss fails to correlate with downstream return.
- Existing partials: [[2603.22212|Omni-WorldBench]] (WM-only), [[2506.00613|WorldGym]] (game-style), [[2510.10125|CTRL-WORLD]] (controllability), [[2603.23497|WildWorld]] (game domain), [[2510.16281|SEAL]] (verifier not benchmark), [[2604.21686|WorldMark]] ($\rho > 0.9$ with human; visual quality ⊥ consistency).

**Concrete research questions**

- Q1 — **Causal-consistency metric**: [[2304.07193|DINOv2]] (ViT-L/14) cosine between $\hat{s}_{t+1}$ and $s_{t+1}$, plus counterfactual probe — sample $a'_t$, generate $\hat{s}'_{t+1}$, require $\|\hat{s}_{t+1} - \hat{s}'_{t+1}\|$ to scale monotonically with $\|a_t - a'_t\|$. Reference on [[2603.13966|vla-eval]].
- Q2 — **50–100 task diagnostic suite.** [[2306.03310|LIBERO]] + [[2510.13626|LIBERO-Plus]] + [[2603.28301|LIBERO-Para]]; record (predicted_state, achieved_state, action) at every step. Scale: ~40k pairs per WAM.
- Q3 — **L1/L2/L3 sub-scores.** L1: 1-step MSE in DINOv2 (>90% [[2510.10125|CTRL-WORLD]] controllability). L2: 8-step cumulative drift (<2× linear). L3: COD as AUROC of swapped-action detection (0.5 = chance, 1.0 = perfect).
- Q4 — **Speed-quality Pareto.** Re-run [[2603.22078|WAM vs VLA Robustness]]'s ~12-config grid. Does the 4.8× latency cost translate to ≥X pp on L3?
- Q5 — **Deployment-readiness axis.** Cross-reference [[2506.18123|RoboArena]] (8 platforms, ~120 tasks). Does joint metric predict real SR at $\rho > 0.7$? Current separate sub-scores: $\rho < 0.4$.

**Related research papers**

| Paper | Contribution | Gap addressed |
| --- | --- | --- |
| [[2603.22212\|Omni-WorldBench]] | First interaction-centric WM eval w/ counterfactual probes | WM-only |
| [[2506.00613\|WorldGym]] | Policy inside WM; downstream transfer | Game-style only |
| [[2510.10125\|CTRL-WORLD]] | Controllability eval for manipulation | Controllability, not joint causal |
| [[2603.23497\|WildWorld]] | Action Following + State Alignment on 108M frames | Game domain |
| [[2510.16281\|SEAL]] | Runtime CoT-faithfulness verifier; +15 pp | Verifier, not benchmark |
| [[2604.21686\|WorldMark]] | Unified I2V; $\rho > 0.9$ w/ human; visual ⊥ consistency | Interactive WMs only |
| [[2603.13966\|vla-eval]] | Unified eval harness; 47× LIBERO speedup | Eval infrastructure only; no joint causal metric |
| [[2603.22078\|WAM vs VLA Robustness]] | Grid; 4.8× latency cost | WM quality + action SR measured on separate axes |
| [[2506.18123\|RoboArena]] | Real-fleet across 8 platforms | Real-world anchor |
| [[2605.03941\|iWorld-Bench]] | Interactive WM benchmark | Needs WAM extension |
| [[2601.04137\|WowWoVal]] | Comprehensive embodied WM eval Turing test | Coarse task success; no causal-binding probe |
| [[2602.08971\|WorldArena]] | Unified perception + functional utility for embodied WMs | Perception-leaning; needs WAM-policy joint extension |

**Benchmarks & metrics**

| Benchmark | What it measures | Why it matters |
| --- | --- | --- |
| [[2306.03310\|LIBERO]] + LIBERO-Plus + LIBERO-Para | Action SR baseline | ~40k pairs |
| [[2603.22212\|Omni-WorldBench]] | WM causal consistency in isolation | WM-only baseline to extend |
| ASR + COD | Action Success Rate + Counterfactual Outcome Deviation | C1 metric pair; AUROC ≥ 0.7 |
| [[2506.18123\|RoboArena]] | Real-fleet SR | Validation at $\rho > 0.7$ |

**Risks**

- **Metric noise**: feature-space similarity embeds training blind spots; pair with explicit physical predicates.
- **Selection bias**: benchmark may flatter current WAMs; include adversarial / physics-violating baselines.
- **Visual quality ⊥ world consistency** ([[2604.21686|WorldMark]]): score axes independently.

#### **C2: Real-Time-Deployable WAMs**

**Thesis.** VideoGen WAMs are 4.8× slower than VLAs (~7 Hz), making them deployment-infeasible. Achieve ≥30 Hz via amortized planning ([[2605.08732|GC-IDM]] 100–130× faster), Fast-WAM, efficient architectures (Mamba/linear-attn), latent rollout, step distillation.

> "Efficiency is a prerequisite, not an optimization, for video-based world models. The high-dimensional nature of video data and complex dynamics impose substantial computational and memory bottlenecks." — [[2603.28489|Video Gen as WM Survey]]

**State of evidence**

- [[2603.28489|Video Gen as WM Survey]] reframes efficiency as prerequisite — AR hits KV-cache explosion; diffusion hits iterative-denoising latency. [[2604.15911|Efficient Video Diffusion Survey]] inventories levers: 1–4 step distillation, sparse attention, QAT/PTQ. [[2510.24795|Efficient VLA Survey]] adds three-pillar framing.
- Quantitative anchors: [[2505.04769|VLA Concepts Survey]] caps AR at 3–5 Hz (vs 20–50 Hz needed); [[2603.22078|WAM vs VLA Robustness]] documents 4.8× slowdown.
- Single-lever results from deep-dives: [[2603.16666|Fast-WAM]], [[2603.17240|GigaWorld-Policy]], [[2512.19133|WorldRFT]], [[2605.08732|GC-IDM]] (**100–130×** faster planning, **15–36×** lower jerk). All single-lever; no co-design.

**Concrete research questions**

- Q1 — **Pareto sweep**: backbone × decoding × precision on LIBERO + 1 real task; is 30 Hz on edge reachable without unacceptable SR loss?
- Q2 — **Amortized latent planning extension.** Extend [[2605.08732|GC-IDM]]'s 1.5M-param MLP to amortize MPC search in frozen latent WMs.
- Q3 — **Step distillation for WAM inference.** Apply 1–4 step distillation to WAM diffusion head; measure SR vs 50-step base.
- Q4 — **Sparse + linear attention substitution.** Replace WAM backbone attention; goal: linear-in-token without SR collapse.
- Q5 — **Quantization-aware training for joint loops.** Does INT8 / INT4 break latent-consistency reward in A1 / B3?
- Q6 — **Edge deployment chain**: train → quantize → distill → deploy on Jetson Orin / Apple M; SR retention at each stage.

**Related research papers**

| Paper | Contribution | Gap addressed |
| --- | --- | --- |
| [[2603.28489\|Video Gen as WM Survey]] | 3D efficiency taxonomy | Survey only; no co-design implementation |
| [[2604.15911\|Efficient Video Diffusion Survey]] | 4-category technique taxonomy | Survey only; techniques not co-designed |
| [[2510.24795\|Efficient VLA Survey]] | Three-pillar taxonomy (model / training / data) | Survey only; no end-to-end co-design |
| [[2603.16666\|Fast-WAM]] | Train video, test latent | Single lever (architecture); no training/data co-design |
| [[2603.17240\|GigaWorld-Policy]] | Action-centered architecture | Single lever (architecture); no training/data co-design |
| [[2605.08732\|GC-IDM]] | Amortized latent IDM; **100–130×** vs CEM | IDM-only; not generalized to full WAM imagination |
| [[2502.16707\|RoboMamba]] | Mamba-based efficient VLA | VLA backbone; not yet adapted to WAM |
| [[2511.15605\|SRPO]] | Frozen V-JEPA-2; ~10 ms inference | Inference-only fast WM; no training-time co-design |
| [[2605.00078\|Being-H0.7]] | Dual-branch latent; 3–4 ms/step | Architecture-only latency win; no data/training co-design |
| [[2605.15178\|SANA-WM]] | Hybrid Linear DiT; **22 videos/hour** H100, **39×** distilled | Architecture lever only; proves linear-attention is viable |
| [[2603.16861\|MolmoBot]] | 232K-env procedural MuJoCo; **79.2%** real Franka | Data-side lever only; no architecture/training co-design |
| [[2602.16710\|EgoScale]] | Log-linear scaling on internet video; **+54%** dexterous | Data-side lever only; no architecture/training co-design |

**Benchmarks & metrics**

| Benchmark | What it measures | Why it matters |
| --- | --- | --- |
| Inference latency (Hz) | A100 / Jetson Orin / Apple M | Headline: ≥30 Hz on edge |
| [[2306.03310\|LIBERO]] + [[2603.13966\|vla-eval]] | SR at matched latency | SR not degraded |
| [[2510.13626\|LIBERO-Plus]] | OOD SR | Efficiency must not break OOD |
| [[2506.18123\|RoboArena]] | Real-fleet SR | Deployment validation |
| Pareto SR × Hz × edge-compute | Joint metric | No current benchmark — first-paper opportunity |

**Risks**

- **Linear-attention / Mamba may underperform Transformers on long-context WAM** — gain only matters if SR holds.
- **Quantization-aware training for joint loops uncharted** — may break latent-consistency reward.
- **Saturation risk**: if "Mamba + LoRA + step-distill + latent" becomes dominant recipe, contribution shrinks to engineering.

---

## Cross-Cutting Themes

1. **Latent-space prediction as dominant substrate** — A1, A2, A3, B3, C2. Consensus: "video at training, latent at deployment" + JEPA / DiT-on-latent backbones.
2. **Verifiable predicates over imagined state** — B1, B2, C1. Turns the "statistical correlations ≠ causal understanding" diagnosis into action; makes the WAM an L3 Evolver.
3. **Joint optimization over (action, imagination)** — A1, B3, C1. Cascaded-to-joint is the central architectural shift; $\mathcal{L}_{\text{WAM}} = -\log p(o', a \mid o, l)$ is the target.
4. **Closed-loop detection-diagnosis-recovery via WAM imagination** — B3 explicitly; C1 implicitly; A1 (failure-finder in inner loop). End-to-end integration is unattacked.
5. **Efficiency as deployment prerequisite** — C2 explicitly; A1, A2, B3 all require real-time budgets. 3–5 Hz AR ceiling and 4.8× WAM latency cost are the quantitative anchors.

---

## Benchmark Gaps (Consolidated)

| Gap | Direction | Existing closest |
|---|---|---|
| Joint-vs-alternating co-training ablation on fixed WAM backbone | A1 | None |
| Hybrid latent+pixel vs pure-latent vs pure-pixel WAM at matched FLOPs | A2 | [[2605.06388\|Semantic-LDM-WM]] (semantic vs reconstruction) |
| WAM with tactile/force prediction head | A3 | [[2506.14754\|Sparsh-X]] (encoder) + [[2601.20321\|TaF-VLA]] (policy-side) |
| Physics-consistency of WAM-imagined state sequences | B1 | [[2410.05363\|PhyGenBench]] (video only) + [[2604.17896\|Physical-Feasibility VLA]] (geometric on actions) |
| Discrete contact-mode latent; assembly SR with contact-aware imagination | B2 | [[2511.07416\|PhysWorld]] (continuous) + [[2604.27367\|DOT-Sim]] (sim only) |
| Integrated detection-recovery loop with WAM-driven imagination | B3 | [[2605.10921\|RoboMemArena]] (memory only) + 06_Self-Evolving §4 (isolated) |
| Joint WAM-policy causal-consistency on unified manipulation suite | C1 | [[2603.22212\|Omni-WorldBench]] (WM-only) + [[2506.00613\|WorldGym]] (game) |
| WAM SR × control frequency × edge-compute Pareto | C2 | [[2306.03310\|LIBERO]] (SR only) + [[2603.13966\|vla-eval]] (training speedup) |

---

## References

- [[04_WAM]] — WAM taxonomy (VideoGen / latent / Dreamer / VLM-integrated / efficient / self-evolving)
- [[05_Latent-World-Models]] — JEPA + alternative latent models; latent reasoning
- [[06_Self-Evolving-VLA-WAM]] — Failure detection, diagnosis, recovery; self-evolution mechanisms
- [[07_Physics-Aware-Embodied-AI]] — Physics-aware design space; physics commonsense benchmarks
- [[11_Sim-to-Real-Transfer]] — Sim-to-real strategies; learned simulators; reality-gap diagnostics
- [[General/08_Benchmarks-and-Surveys|General/08]] — Canonical survey index
