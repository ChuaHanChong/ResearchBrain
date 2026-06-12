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
---

# Promising Research Directions: World Action Models

> [!abstract] Overview
> A World Action Model imagines a future *and* commits to an action in one model, so its central tension is that the imagined state has to be represented *somewhere* — and every substrate choice trades fidelity against the latency and OOD-robustness a policy actually needs. These **seven directions across two clusters** organize the field's open bets around that tension: the *substrate and encoding* of the imagined state (Cluster A — what the latent is, how dense it is, what modalities it spans), and the *training-time grounding* that keeps imagination honest enough to act on (Cluster B — contact discreteness, self-evolution, calibration, and data synthesis).
> The non-consensus thesis the doc collectively bets: a WAM's imagination is not one fixed thing to be optimized — train density is independent of deploy density (A1), the encoder objective outweighs the latent-vs-pixel question (A3), contact physics needs *discrete* structure no smooth latent reaches (B1), and the imagination's most durable product is a *training corpus*, not an in-episode rollout (B4). The substrate is task-conditional, and the imagination is a verifiable surface, not just a planning convenience.

---

## Methodology

**Scope.** This doc reads ~35 pure-WAM and adjacent surveys plus ~70 WAM-method and benchmark papers from `_KnowledgeHub_/` (the Survey Landscape below names the surveys/benchmarks; the cards cite the methods), cross-checked against [[../../../General/08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] and the deep-dives [[../../../Embodied-AI/07_WAM|07_WAM]], [[../../../Embodied-AI/08_Latent-World-Models|08_Latent-World-Models]], [[../../../Embodied-AI/13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]], [[../../../Embodied-AI/11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]], and [[../../../Embodied-AI/14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]]. It owns the WAM-internal *substrate* and its *training-time grounding*: the latent / architecture / encoding choices for the imagined state (Cluster A) and the losses and data strategies that keep imagination aligned with physics (Cluster B). Five model-spanning directions the umbrella covers (joint WAM–policy co-evolution, physics-consistency verification, joint causal-consistency evaluation, real-time deployment, cross-embodiment transfer) and the model-agnostic 3D/4D geometric substrate are cross-referenced, not re-clustered — see Cross-References.

---

## World-Action Model Survey Landscape

| Survey / Benchmark | The open problem it names (surveys) / what it measures (benchmarks) | Fuels |
|---|---|---|
| [[2605.12090\|WAM Survey]] | WM-vs-action evaluation gap; data-ecosystem mixing; tactile/force/acoustic extension; long-horizon drift; closed-loop latency | A1, A2, B4 |
| [[2605.00080\|WM Robot Learning Survey]] | Evaluation beyond visual fidelity; latent-WM dominance; causal conditioning; failure-recovery datasets | A1, A3, B2 |
| [[2510.16732\|World Models for Embodied AI Survey]] | Physically-consistent metrics beyond FID/FVD; SSM/hybrid AR-global; spatial-representation axis (latent vector → token → grid → rendering) | A1, A3 |
| [[2511.02097\|WM Manipulation Survey]] | Structured task-relevant representations over raw capacity; hierarchical architectures for long-horizon | A1, A2, A3, B1 |
| [[2411.14499\|World Models Survey]] | Physical-rule adherence; standardized benchmarks; interactive 3D action-conditioned WMs | B1, B3 |
| [[2604.16592\|Cognition WM Survey]] | Motivation + meta-cognition under-developed; tactile as the contact-grounding modality | A2 |
| [[2604.04707\|OpenWorldLib]] | Definition fragmentation; 3D geometric consistency under camera motion; modular pipeline composition | A1 |
| [[2602.01630\|Unified World Model Framework]] | Fragmentation; integrated-module architecture; holistic-understanding gap | A1 |
| [[2604.22748\|Agentic World Modeling Survey]] | L1 Predictor / L2 Simulator / L3 Evolver hierarchy; autonomous self-revision; decision-centric metrics (ASR + COD) | B2, B3 |
| [[2604.02029\|Latent Space Survey]] | Evaluability / controllability / interpretability of the latent; theory gap; modality-native integration | A3 |
| [[2503.21765\|Physics Cognition Survey]] | Sub-human physics; limited physical coverage; physics foundation + neuro-symbolic | B1 |
| [[2510.04978\|Physical AI Survey]] | Causal understanding missing; compositional/causal structure; hybrid Neural Physics | B1 |
| [[2501.10928\|Generative Physical AI Survey]] | Functional vs visual realism; physical-plausibility metrics; material fidelity | B1 |
| [[2601.15533\|Actionable Simulators]] | Dynamical hallucinations; structured 4D interfaces; closed-loop decision-oriented eval | B1, B4 |
| [[2601.07823\|Video Generation in Robotics Survey]] | Hallucinations + physics violations; uncertainty; robotics-centric benchmarks | B3, B4 |
| [[2604.04974\|Video-to-Control Survey]] | Integration layer as the critical gap; latent-action identifiability; pre-execution verification; tactile/force integration | A2, B1, B3 |
| [[2604.15395\|Foundation Models in Robotics Survey]] | Five-phase FM evolution; dataset/challenge mapping; design-learning-deployment integration | B4 |
| [[2310.06253\|Objective Mismatch MBRL Survey]] | Decision-aware MBRL; predictive-loss vs return alignment; cross-family fragmentation | B3 |
| [[2602.04411\|Self-evolving Embodied AI]] | "Human-crafted settings" limit; multi-timescale closed-loop co-evolution; WM/memory/embodiment integration | B2, B3 |
| [[2508.07407\|Self-Evolving AI Agents Survey]] | Continuous self-improvement without forgetting; evolution-evaluation gap; safety under self-modification | B2 |
| [[2604.23775\|VLA Safety Survey]] | Threat taxonomy; adversarial/jailbreak robustness; safe-deployment mechanisms | B2 |
| [[2604.19092\|RoboWM-Bench]] | Visual plausibility ≠ executability — measured directly | B1, B3 |
| [[2510.13626\|LIBERO-Plus]] | 10,030 OOD perturbations; pure-latent OOD retention | A1, A3, B4 |
| [[2407.08028\|AutoMate]] | Insertion / assembly SR over 8 industrial tasks; 90.5% contact-naive baseline | B1 |
| [[2605.03941\|iWorld-Bench]] | Standardized interactive evaluation across WAM types | A1, B3 |

> [!tip] Convergence patterns
> - **Latent prediction is the dominant substrate, but the field cannot yet say what the latent must encode** (4-way): [[2510.16732|World Models for Embodied AI Survey]] (traces the spatial-representation axis from latent vector → token → grid → rendering but leaves *which* encoding is right open), [[2605.00080|WM Robot Learning Survey]] (names latent-WM dominance yet flags causal conditioning as unresolved), [[2511.02097|WM Manipulation Survey]] (ranks *structured task-relevant* representation above raw capacity), [[2604.02029|Latent Space Survey]] (names evaluability and controllability of the latent as the open theory gap) — four surveys converge that the substrate is latent but its *content* is undecided, the empirical mandate for A1 (density) and A3 (encoding).
> - **Imagination violates physics, and visual fidelity does not predict executability** (5-way): [[2503.21765|Physics Cognition Survey]], [[2510.04978|Physical AI Survey]], [[2501.10928|Generative Physical AI Survey]], and [[2601.15533|Actionable Simulators]] all diagnose dynamical hallucinations and converge on verifiable / neuro-symbolic physics, and [[2604.19092|RoboWM-Bench]] makes it empirical — visual plausibility ≠ executability, measured — the mandate for B1's discrete contact structure and B3's train-time calibration.
> - **The WAM's most underexploited output is training data, not a rollout** (3-way): [[2605.12090|WAM Survey]] (names "data-ecosystem mixing" as open), [[2604.15395|Foundation Models in Robotics Survey]] (names dataset/challenge mapping as the integration gap), [[2601.15533|Actionable Simulators]] (names structured, decision-oriented simulation that *produces* usable data) — three surveys point at the same underexploited product, the mandate for B4's data engine.
> - **Self-evolution and runtime verification are unbuilt as an integrated loop** (4-way): [[2604.22748|Agentic World Modeling Survey]] (its L3 Evolver is "emerging not mature"), [[2602.04411|Self-evolving Embodied AI]] (multi-timescale closed-loop co-evolution unbuilt), [[2508.07407|Self-Evolving AI Agents Survey]] (self-improvement without forgetting unresolved), [[2604.23775|VLA Safety Survey]] (imagination as an adversarial/jailbreak surface that must be verified) — four surveys name the pieces, none names the integrated detect→imagine→recover→verify loop, the mandate for B2.

---

## Formal Framing

**The world-action joint objective.** A WAM is defined — per [[2605.12090|WAM Survey]] — as an embodied foundation model that predicts a *joint* distribution over the next observation and the action, not the action alone:

> "WAMs are defined as embodied foundation models that integrate predictive state modeling with action generation, moving beyond merely predicting actions to predicting a joint distribution over future states and actions." — [[2605.12090|WAM Survey]]

$$\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o,l,o',a) \sim \mathcal{D}} \big[ -\log p(o', a \mid o, l) \big]$$

The family splits by what each model predicts:

| Family | Distribution | Predicts |
|---|---|---|
| **VLA** | $p(a \mid o, l)$ | Action only; no dynamics |
| **WM** | $p(o' \mid o, a)$ | Dynamics only; no action |
| **WAM** | $p(o', a \mid o, l)$ | Both; the unifying frontier |

WAMs further split into **Cascaded** (predict the state, then derive the action by inverse dynamics) vs **Joint** (one end-to-end model). The joint-vs-cascaded *optimization* question lives in the umbrella; this doc keeps the WAM-internal fact that whatever the optimizer, the imagined state $o'$ has to be *represented* — and that representation choice is what Cluster A attacks.

**The spatial-representation axis.** [[2510.16732|World Models for Embodied AI Survey]] gives the canonical axis the substrate choice moves along:

> "The world models are categorized along three axes: Functionality (Decision-Coupled vs General-Purpose), Temporal Modeling (Sequential Simulation vs Global Difference Prediction), and Spatial Representation (Global Latent Vector, Token Feature Sequence, Spatial Latent Grid, Decomposed Rendering Representation)." — [[2510.16732|World Models for Embodied AI Survey]]

Reading this axis as a *design space* rather than an evolution is A1's move: a model can be trained at the rendering end (dense 3D supervision) yet deployed at the latent-vector end (cheap rollout). Two quantities make this measurable — **train density** $\rho_{\text{train}}$ (the supervision signal's richness) and **deploy density** $\rho_{\text{deploy}}$ (the rollout representation's cost) — and the doc's first claim is that they are independent.

**The capability hierarchy.** [[2604.22748|Agentic World Modeling Survey]] gives the canonical levels Cluster B's grounding directions target:

> "We introduce three capability levels: L1 Predictor, which learns one-step local transition operators; L2 Simulator, which composes them into multi-step, action-conditioned rollouts that respect domain laws; and L3 Evolver, which autonomously revises its own model when predictions fail against new evidence." — [[2604.22748|Agentic World Modeling Survey]]

The physical-law L3 Evolver is the target for B2's self-evolution loop; the survey's decision-centric metrics — **ASR** (Action Success Rate) and **COD** (Counterfactual Outcome Deviation) — anchor the joint causal-consistency evaluation that lives in the umbrella. The recurring quantity across B2/B3 is the **imagined-vs-real success-rate correlation** $\rho$ (Pearson): a WAM whose imagined outcomes track real ones ($\rho$ high) can train a policy on dreams; a WAM whose imagination diverges cannot.

**The identifiability criterion.** [[2605.26379|LeJEPA World Model]] supplies the formal test for *when* a learned latent is a world model:

> "[[2511.08544|LeJEPA]] achieves linear identifiability — recovering true latent variables up to an orthogonal transformation — if and only if the underlying latent variables follow an isotropic Gaussian distribution." — [[2605.26379|LeJEPA World Model]]

This gives A1's substrate and A3's encoding a membership test: a latent is identifiable iff isotropic-Gaussian, at which point latent-space planning matches an oracle controller ($R^2 > 0.999$ to 1024 dims). A3's sharpest question is whether the encodings that *win control* are exactly the ones that *pass this test*.

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Substrate & Encoding** | A1, A2, A3 | The imagined state must be represented somewhere, and every substrate trades fidelity against deploy latency and OOD retention | **A1 is the substrate lead** — it fixes *how dense* the imagined state is at train vs deploy ([[2605.20752\|GaussianDream]] train-dense/deploy-light); **A3 fixes *what* that latent encodes** (semantic / continuous over reconstruction / VQ — orthogonal to A1's density axis), and **A2 adds the modality A1's backbone does not yet imagine** (the wrench channel). [[2605.26379\|LeJEPA World Model]]'s identifiability criterion governs A1's latent half and is A3's encoding-geometry target; A2's imagined wrench is a train-time forecast the same calibration machinery (B3) must keep honest. [[2605.20752\|GaussianDream]], [[2604.16484\|DexWorldModel]], [[2605.06388\|Semantic-LDM-WM]] set the bar |
| **B — Training-Time Grounding** | B1, B2, B3, B4 | Imagination drifts from physical reality unless a training-time signal forces the match | **B3 is the trust lead** — its forward-inverse calibration raises the imagined-vs-real $\rho$ that **B2's** self-evolution loop uses as a stop condition, so investing in B3 shrinks B2's runtime recovery work; **B1's** discrete contact-mode latent is the structure B2's failures and B3's calibration both need in contact-rich regimes; **B4** turns the same grounded imagination into a *training corpus*, and B3's physics calibration is exactly what makes B4's synthesized demos executable rather than plausible-looking. [[2604.01985\|WAV]]'s asymmetry signal and [[2605.22446\|Pre-VLA]]'s runtime verifier are the trust valves all four share |

---

## Cluster A — WAM Substrate & Encoding

*The imagined state has to live somewhere — a latent vector, a token grid, a rendered 3D scene, or a wrench trajectory. The three directions attack the same representation question from different axes: how dense the substrate is at train vs deploy (A1), which modality it spans (A2), and what its latent is trained to encode once dense-vs-sparse is fixed (A3).*

### A1 — Hybrid Latent+Pixel WAM Architectures

| | |
|---|---|
| **Cluster** | A — Substrate & Encoding |
| **Thesis** | Train a WAM on dense pixel/3DGS supervision but let it roll out on a cheap latent at deployment, rather than picking latent-vs-pixel once and locking both. The reason it must work: train density and deploy density are independent — nothing forces a model to predict at the same density it learned from, the way a human rehearses in full detail but acts on a compressed prediction. The field assumes latent-vs-pixel is a one-time binary that locks both phases and that hybrids are too complex to be worth it. The bet is in First-principles below — one backbone with dense train-time heads dropped at deploy. |
| **Anchor papers** | [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2511.02097\|WM Manipulation Survey]] (survey), [[2604.19092\|RoboWM-Bench]] (benchmark), [[2605.20752\|GaussianDream]] (method), [[2604.16484\|DexWorldModel]] (method) |
| **Key targets** | Match [[2605.20752\|GaussianDream]]'s 98.4% [[2306.03310\|LIBERO]] / 34.4→50% real at lower deploy cost than a pixel WAM (its own 531 ms/chunk reference); keep pure-latent OOD retention on [[2510.13626\|LIBERO-Plus]] from dense co-training; latent ~10 ms vs pixel ~150 ms forward latency |

**Why it matters.**
- **The gap**: a WAM must imagine a future to plan, but a pixel/video substrate is robust-yet-slow ([[../../../Embodied-AI/07_WAM#6. Efficient & Action-Centered WAMs|07_WAM §6]] finds VideoGen 4.8× slower but most robust) while a pure latent is fast-yet-opaque, and single-paradigm WAMs are stuck on that trade-off.
- **Today's answers**: [[2605.20752|GaussianDream]] supervises a renderable 3D-Gaussian future at train time then *drops the auxiliary heads at inference* (98.4% [[2306.03310|LIBERO]], 34.4→50% real, 531 ms/chunk); [[2604.16484|DexWorldModel]] uses semantic [[2508.10104|DINOv3]] latents as prediction targets to separate interaction from visual noise (94% [[2504.13059|RoboTwin]], zero-shot sim-to-real). Both work — but each is a *single point* on the train-density/deploy-density plane, not a controlled sweep of it.
- **The opening**: [[2606.05254|Flash-WAM]]'s modality-aware distillation cuts a two-stage WAM 8.1 s → 348 ms (23×) while keeping 81.41% of the 91.25% teacher's [[2504.13059|RoboTwin]] SR — direct proof that deploy density can be cut hard without dropping the WM, so the hybrid recipe has measured headroom.

**First-principles framing.**
- **First principle**: Train density and deploy density are independent quantities. A model can learn from pixel/3DGS-dense signal yet act on latent-dense signal, because the supervision that shapes the weights and the representation that carries the rollout are decoupled — the dense branch is a *teacher* the deploy path need not retain. [[2605.20752|GaussianDream]] demonstrates the decoupling directly: its renderable-3D heads exist only at train time and are discarded at inference with no SR loss.
- **Assumption being challenged**: That latent-vs-pixel is a one-time binary locking both train and deploy, held by every single-paradigm WAM. [[2605.20752|GaussianDream]] and [[2604.16484|DexWorldModel]] bet the opposite — a hybrid is one backbone with dense train-time heads dropped at deploy — and [[2606.03188|GeoSem-WAM]] reproduces it on a second signal (geometry + semantic supervision on latent tokens, branches dropped at test; 98.55% [[2306.03310|LIBERO]], +6.6 pp real).
- **The bet**: A hybrid backbone reaches [[2605.20752|GaussianDream]]-class real SR (≥50%) *and* matches or beats pure-latent OOD retention on [[2510.13626|LIBERO-Plus]] (≥79.5%, the [[2602.10098|VLA-JEPA]] pure-latent reference), at <2× the deploy latency of a pure-latent WAM and far below the 4.8× pixel-WAM cost ([[2603.22078|WAM vs VLA Robustness]]) — one measurable inequality, not a three-way tie. Interpretability (the dense branch stays inspectable) is a qualitative aside, not part of the falsifiable claim.

**Related research papers.**

Twenty systems that put the imagined state at a different point on the *train-density × deploy-density* plane — the axis the direction turns on. The discriminator is whether dense supervision is *retained* or *dropped* at deploy, and what the deploy representation is:

| System | Train substrate | Deploy substrate | Key result | What's missing |
|---|---|---|---|---|
| [[2605.20752\|GaussianDream]] | renderable 3D Gaussians (dense) | latent, heads dropped | 98.4% [[2306.03310\|LIBERO]], 34.4→50% real, 531 ms/chunk | a single point on the plane, not a controlled density sweep — the train-dense/deploy-light exemplar |
| [[2604.16484\|DexWorldModel]] | [[2508.10104\|DINOv3]] semantic-latent targets | causal latent, O(1) TTT | 94% [[2504.13059\|RoboTwin]], zero-shot sim-to-real | semantic-latent *target*, but no dense pixel/3DGS branch — the semantic end of the axis |
| [[2606.03188\|GeoSem-WAM]] | geometry + semantic on latent tokens | latent, branches dropped | 98.55% [[2306.03310\|LIBERO]], +6.6 pp real | confirms train-dense/deploy-light on a *second* signal, but still one operating point |
| [[2606.05254\|Flash-WAM]] | two-stage WAM (dense) | distilled, 348 ms | 23× speedup 8.1 s→348 ms, 81.41% of 91.25% teacher | deploy-light *without* dropping the WM — distillation, not a co-trained latent branch |
| [[2606.05979\|WLA]] | text intentions + latent actions (AR) | AR latent, no image gen | 56.5% RMBench SOTA, ~40 ms | unifies world+language+action but no dense visual supervision to drop |
| [[2603.16666\|Fast-WAM]] | video (dense) | latent, WM dropped at test | trains on video, tests latent | drops the WM entirely at test — no test-time imagination at all |
| [[2605.10942\|HarmoWAM]] | dual experts + adaptive gating | both experts latent | 89% in-domain | both branches latent — never tests pixel-vs-latent at the *same* operating point |
| [[2602.10098\|VLA-JEPA]] | JEPA latent (semantic-predictive) | pure latent | 97.2% [[2306.03310\|LIBERO]], 79.5% [[2510.13626\|LIBERO-Plus]] | no pixel decoder for inspection — the pure-latent OOD reference A1 must match |
| [[2605.15153\|Pelican-Unified]] | shared latent z, pixel-side generator | shared z | 93.5% [[2504.13059\|RoboTwin]] | deploy latency of the generator branch left open — the shared-z hybrid candidate |
| [[2411.04983\|DINO-WM]] | frozen [[2304.07193\|DINOv2]] + light dynamics | frozen-feature latent | zero-shot planning | no pixel verification path — the frozen-semantic baseline |
| [[2605.00078\|Being-H0.7]] | dual-branch deployable+privileged | both branches latent | 3–4 ms/step | both branches latent, privileged dropped — speed exemplar, no pixel branch |
| [[2606.01955\|WALL-WM]] | layer-coupled video-action denoiser | event-granular latent | Task Progress 32.6→71.6 | the representation-*granularity* axis (events vs chunks), orthogonal to density |
| [[2606.02800\|Cosmos 3]] | omnimodal MoT (lang/img/video/audio/action) | generative, video+policy | 39.7% RoboLab, #1 RoboArena | the unified-generative-substrate end — heavy deploy, no light path |
| [[2605.28816\|Gamma-World]] | latent video-diffusion + Sparse Hub Attention | KV-cached streaming latent | FVD 184.1 vs 333.8 | the efficient real-time substrate, but pure-video — no latent-action deploy path |
| [[2605.21862\|EvoScene-VLA]] | latent scene interface co-denoised w/ action | scene predictor dropped | 88.5% [[2504.13059\|RoboTwin]] (+2.4), 42.0% real (+4.7) | train-dense/deploy-light on a *scene* latent — closest co-trained hybrid |
| [[2602.11832\|JEPA-VLA]] | V-JEPA 2 video-predictive embedding | cheap policy | +7.4% [[2306.03310\|LIBERO]], better real robustness | shows dense predictive supervision transfers, but no explicit pixel/3DGS branch |
| [[2603.14482\|V-JEPA 2.1]] | dense predictive loss on masked+unmasked tokens | latent | RMSE 0.307 NYUv2 depth, +20% grasp, 10× nav | the dense train-time supervision A1 reuses — a backbone, not a full WAM |
| [[2412.14803\|VPP]] | frozen SVD video predictor (single forward pass) | DiffPolicy head, no video gen | CALVIN ABC→D length 4.33 (+41.5% over GR-1) | train-dense-video/deploy-light, but the video predictor is *frozen*, not co-trained |
| [[2412.15109\|Seer]] | conditional visual foresight + action (unidir. attn) | action reads predicted-future tokens | +13% LIBERO-LONG, +43% real | future-state prediction at train, action at deploy — no 3DGS density |
| [[2603.29409\|CLaD]] | grounded proprio + semantic future latents | diffusion policy, 25 Hz | 94.7% LIBERO-LONG at 0.66B | latent-foresight train signal, fast deploy — no pixel branch to compare against |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a hybrid backbone keeps GaussianDream-class real SR + pure-latent OOD at <2× latent latency), with the experiment and the Related-table row it lands on.
1. **H1 — Dense train heads can be dropped at deploy with no SR loss but with OOD gain.**
   - *Prediction*: co-training [[2602.10098|VLA-JEPA]]'s latent backbone with a [[2605.20752|GaussianDream]]-style renderable-3D auxiliary head, then dropping the head at inference, holds 97.2% [[2306.03310|LIBERO]] *and* lifts [[2510.13626|LIBERO-Plus]] OOD above the 79.5% pure-latent baseline.
   - *Test*: A/B the same backbone with vs without the dense auxiliary head at train; deploy latent-only; report in-dist SR + OOD retention + forward latency.
   - *Row*: GaussianDream (train-dense/deploy-light) vs VLA-JEPA (pure latent).
   - *Falsifier*: OOD retention does not exceed pure-latent at matched in-dist SR → dense co-training adds nothing the latent didn't already have.
2. **H2 — The deploy-density frontier is below 2× pure-latent latency.**
   - *Prediction*: sweeping deploy representation from full-pixel rollout → latent-only, real SR stays ≥50% down to a latent path costing <2× the pure-latent forward latency, far under the 4.8× pixel-WAM cost.
   - *Test*: profile SR-vs-latency along the density sweep on a fixed A100; mark where SR drops below 50%.
   - *Row*: Flash-WAM (distilled, 348 ms) / WAM vs VLA Robustness (4.8× cost anchor).
   - *Falsifier*: holding ≥50% SR requires ≥2× pure-latent latency → the hybrid buys no latency advantage.
3. **H3 — A shared latent z lets one backbone decode to pixel (inspect) and latent (act).**
   - *Prediction*: [[2605.15153|Pelican-Unified]]'s shared z anchors a hybrid where imagination decodes to pixel/3DGS for inspection and action decodes to latent for speed, with no SR cost vs decoding both from the latent.
   - *Test*: train one z, two decoders; compare SR + latency vs latent-only and vs the EvoScene-VLA co-denoised scene latent.
   - *Row*: Pelican-Unified (shared z) / EvoScene-VLA (co-denoised scene).
   - *Falsifier*: the dual-decoder z underperforms latent-only on SR → the shared substrate cannot serve both jobs.
4. **H4 — Process-adaptive gating beats a fixed deploy substrate.**
   - *Prediction*: gating latent-only (free-space transit) vs pixel/3DGS-aided (predicted-contact) by a contact predictor beats [[2605.10942|HarmoWAM]]'s fixed dual-expert gating on contact-rich tasks, with the gain concentrated where contact is imminent.
   - *Test*: stratify tasks by contact-onset proximity; compare contact-gated substrate switching vs HarmoWAM's adaptive gating.
   - *Row*: HarmoWAM (dual-expert gating).
   - *Falsifier*: a fixed substrate matches the gated one on contact-rich tasks → switching adds nothing.
5. **H5 — Semantic-latent supervision survives a dense pixel branch.**
   - *Prediction*: [[2604.16484|DexWorldModel]]'s [[2508.10104|DINOv3]]-target advantage (94% [[2504.13059|RoboTwin]]) persists when a dense pixel/3DGS branch co-supervises training — i.e., the dense branch does not wash out the semantic-latent gain.
   - *Test*: add a renderable-pixel head to the DexWorldModel target; measure whether the semantic-latent SR holds.
   - *Row*: DexWorldModel (semantic target) / GeoSem-WAM (geometry+semantic).
   - *Falsifier*: the pixel branch erases the semantic-latent advantage → density and encoding interfere, contradicting A3's orthogonality claim.
6. **H6 — Distillation and co-training reach different points on the frontier.**
   - *Prediction*: [[2606.05254|Flash-WAM]]'s post-hoc distillation and a co-trained dense-head/latent hybrid land at *different* SR-latency operating points — distillation cheaper to train but lower OOD retention than co-training.
   - *Test*: build both from the same teacher; compare OOD retention at matched deploy latency.
   - *Row*: Flash-WAM (distilled) vs GaussianDream (co-trained).
   - *Falsifier*: distillation matches co-training on OOD at equal latency → co-training's extra train cost is unjustified.

> [!warning] Risks
> - **Two-branch training cost dominates compute** — dense + latent objectives double the train budget. → Distill a pre-trained pixel/3DGS WM into the latent encoder ([[2605.20752|GaussianDream]]'s discard-at-inference pattern, [[2606.05254|Flash-WAM]]'s 23× distillation); H6 reports whether distillation recovers co-training's OOD at lower train cost.
> - **Latent-pixel divergence without shared parameters** — the two branches can drift apart and the dropped head then misleads. → Anchor both to a shared target ([[2604.16484|DexWorldModel]]'s [[2508.10104|DINOv3]] targets); H5 tests whether the semantic anchor survives the dense branch.
> - **Saturated in-distribution regime** — pure latent is already 97.2% [[2306.03310|LIBERO]] and [[2605.20752|GaussianDream]] 98.4%, so headline LIBERO SR cannot distinguish methods. → Bind the bet to OOD ([[2510.13626|LIBERO-Plus]]) + deploy latency, not in-dist SR; H1/H2 are scored there.

### A2 — Tactile/Force-Integrated WAM Imagination

| | |
|---|---|
| **Cluster** | A — Substrate & Encoding |
| **Thesis** | Add a wrench (force + torque) channel to a WAM's imagination, so it predicts force futures and not only visual futures. The reason it must work: in contact, force is the generative *cause* and what you see is the *effect* — the object moves because of force — so a model that predicts only the effect is structurally incomplete. The field treats force as a policy *input* to consume, never as a WM *output* to forecast. The bet is in First-principles below — an imagined wrench can stand in for a missing force sensor at deploy. |
| **Anchor papers** | [[2605.12090\|WAM Survey]] (survey), [[2511.02097\|WM Manipulation Survey]] (survey), [[2604.16592\|Cognition WM Survey]] (survey), [[2603.17851\|DexViTac]] (method), [[2601.20321\|TaF-VLA]] (method) |
| **Key targets** | Recover ≥50% of [[2603.17851\|DexViTac]]'s measured-tactile→no-tactile drop (83.3%→43.3% pipetting ablation) using *imagined* rather than measured tactile, approaching the with-real-tactile ceiling of 85.8%; cross-sensor transfer >60.3% ([[2601.20321\|TaF-VLA]] baseline) |

**Why it matters.**
- **The gap**: current WAMs imagine visual and proprioceptive futures but rarely tactile/force futures, even though force is the dominant signal in contact-rich manipulation — [[2605.12090|WAM Survey]] names the modality gap and [[2511.02097|WM Manipulation Survey]]'s 13 capabilities rank Multimodal Perception first, Physics Awareness third.
- **Today's answers**: every tactile system consumes force as policy *input* — [[2603.15169|ForceVLA2]] (66% avg SR, force as prompt), [[2601.20321|TaF-VLA]] (60.3% cross-sensor via a VQ-VAE force latent the *policy* reads), [[2603.15257|HapticVLA]] (distills tactile away for sensor-free deploy) — none imagines force as a WM output.
- **The opening**: [[2603.17851|DexViTac]] proves tactile is *modelable*: kinematics-grounded tactile pretraining resolves the semantic ambiguity of raw touch (85.8% contact-rich SR), and the pretraining ablation (pipetting 83.3%→43.3%) shows the tactile representation is load-bearing — so a WAM head that *imagines* that representation has a tractable target.

**First-principles framing.**
- **First principle**: In contact, force is the cause and the observed motion is the effect — the object accelerates *because* of an applied wrench. A WM that predicts only the effect can never fully pin down the contact dynamics, because the causal variable is unobserved in its rollout. The data precondition is now met: [[2603.17851|DexViTac]]'s ablation (83.3→43.3% without tactile pretraining) shows the tactile latent carries causal information vision alone does not.
- **Assumption being challenged**: That force can be fed in (as policy input) without being predicted (as WM output) — the bet of every force-aware VLA. That treats force as something you *measure*, so the policy must infer the dynamics itself; [[2603.17851|DexViTac]] shows tactile *can* be modeled but stops at sensing it, and [[2601.20321|TaF-VLA]] builds a force latent but routes it to the policy, not the imagination.
- **The bet**: A WAM that imagines wrench at train time recovers ≥50% of the measured-tactile→no-tactile contact-task drop ([[2603.17851|DexViTac]]'s 83.3%→43.3% pipetting ablation, i.e. lifting the no-tactile floor back toward ~63%) *even with no force sensors at deployment*, where the imagined wrench stands in for a force reading, approaching the with-real-tactile 85.8% ceiling. Falsifiable: if imagined wrench does not beat a vision-only WAM on contact-task SR, force adds nothing as an imagined channel.

**Related research papers.**

Ten systems that differ on *where force lives in the loop* — the axis the direction turns on (dataset / encoder / policy input / generated video / never imagined). The discriminator is whether force is *consumed* or *predicted*:

| System | Force role | Imagines force? | Key result | What's missing |
|---|---|---|---|---|
| [[2603.17851\|DexViTac]] | kinematics-grounded tactile pretraining | no (perceives) | 85.8% contact-rich SR; pretraining ablation 83.3→43.3% pipetting | perception, not imagination — the modelability proof A2 builds on |
| [[2601.20321\|TaF-VLA]] | VQ-VAE force latent, policy-consumed | no (policy reads it) | 60.3% cross-sensor | the latent is policy-consumed, not WM-predicted — the cross-sensor bridge A2 redirects to imagination |
| [[2603.15257\|HapticVLA]] | teacher-student tactile distillation | no (distilled away) | 86.7% SR, sensor-free deploy | force is distilled out of the deploy model, never modeled in a WM |
| [[2603.15169\|ForceVLA2]] | cross-scale MoE + force prompts | no (input) | 66% avg SR | force is a policy input prompt, not a predicted output |
| [[2506.14754\|Sparsh-X]] | multisensory touch foundation (1M contacts) | no (encoder only) | touch foundation encoder | no prediction head — the encoder a WAM imagination target could reuse |
| [[2509.07962\|TA-VLA]] | torque-aware VLA design study | no (input) | torque-conditioned policy | policy-side torque awareness, no WM forecast |
| [[2505.19386\|Force Prompting]] | force-conditioned video generation | partial (force→video) | force-conditioned generation | generates video *from* force; A2 runs it backward (predict force) |
| [[2604.20444\|VTouch++]] | bimanual vision+tactile+proprioception data | n/a (dataset) | 120K episodes, 36M synced frames | data substrate with no WAM consumer — the synchronized corpus A2 trains on |
| [[2604.07335\|TAMEn]] | closed-loop tactile + AR recovery data | no (collection) | 75% SR | collection engine, no WM prediction |
| [[2605.13083\|TouchAnything]] | multi-view egocentric + dense tactile | n/a (dataset) | dense-tactile corpus | dataset only, no imagination consumer |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (imagined wrench recovers ≥50% of the no-tactile drop at deploy), with the experiment and the Related-table row it lands on.
1. **H1 — A wrench-prediction head recovers ≥50% of the no-tactile drop.**
   - *Prediction*: adding a 6-DoF wrench head to a JEPA WAM, trained on [[2604.20444|VTouch++]]'s 36M synchronized frames and [[2506.14754|Sparsh-X]]'s 1M contacts, lifts the no-tactile pipetting floor from 43.3% back above ~63% (≥50% of the 83.3→43.3 drop) with *no* force sensor at deploy.
   - *Test*: train the wrench head; deploy vision-only; compare contact-task SR vs a vision-only WAM and vs DexViTac's with-tactile 85.8% ceiling.
   - *Row*: DexViTac (perceives).
   - *Falsifier*: imagined-wrench SR ties the vision-only WAM → force adds nothing as an imagined channel.
2. **H2 — A tactile latent transfers across sensors as an imagination target.**
   - *Prediction*: using [[2601.20321|TaF-VLA]]'s VQ-VAE force latent (or [[2603.17851|DexViTac]]'s kinematics-grounded latent) as the WAM's *imagination target* and decoding per-sensor on demand beats TaF-VLA's 60.3% policy-side cross-sensor transfer.
   - *Test*: train the WAM to imagine the shared force latent; decode to a held-out sensor; report cross-sensor SR.
   - *Row*: TaF-VLA (policy reads it).
   - *Falsifier*: imagination-target transfer ≤ 60.3% → the latent is no better predicted than consumed.
3. **H3 — Imagined-vs-measured wrench is a useful auxiliary loss.**
   - *Prediction*: supervising imagined wrench against measured wrench at train time (where sensors exist) improves contact-task SR more than an equal-capacity proprioception-only auxiliary loss.
   - *Test*: A/B wrench-auxiliary vs proprioception-auxiliary at matched parameters on [[2604.20444|VTouch++]].
   - *Row*: VTouch++ (dataset).
   - *Falsifier*: the wrench auxiliary ties proprioception-only → the force signal is redundant with proprioception.
4. **H4 — Contact make/break is better modeled as a discrete latent transition.**
   - *Prediction*: representing make/break as a categorical event (continuous wrench only inside the in-contact regime) beats a purely continuous wrench head on slip-stick tasks — sharing the substrate with B1's discrete contact modes.
   - *Test*: ablate discrete-event-gated wrench vs continuous wrench on contact-onset-heavy tasks.
   - *Row*: DexViTac (perceives) / cross-ref B1.
   - *Falsifier*: continuous wrench matches the discrete-gated one → contact events need no special structure here.
5. **H5 — Force-conditioned video prediction run backward yields a usable force forecast.**
   - *Prediction*: inverting [[2505.19386|Force Prompting]] (predict force *from* frames, then condition the next step on the predicted force) gives a force forecast accurate enough to improve next-step manipulation over an unconditioned baseline.
   - *Test*: train the inverse predictor; condition rollout on predicted force; compare next-step SR vs unconditioned.
   - *Row*: Force Prompting (force→video).
   - *Falsifier*: predicted-force conditioning ties unconditioned → the inverse forecast is too noisy to act on.

> [!warning] Risks
> - **Noise floor** — subtle slip and microvibration are not in vision, so imagined force may plateau below measured. → Bound the claim to regimes where force is vision-correlated; report the floor explicitly, and pair with H4's discrete contact events where vision is uninformative.
> - **Cross-sensor brittleness** — 60.3% zero-shot ([[2601.20321|TaF-VLA]]) is not deployment-ready. → Use [[2603.17851|DexViTac]]'s kinematics grounding to stabilize the cross-sensor latent; H2 measures whether imagination-as-target beats policy-as-consumer.
> - **No published WAM has a tactile prediction head** — the bet is genuinely unattacked, so a wrong abstraction has no prior art to correct it. → Treat the prediction-head ablation (imagined vs no-tactile, H1) as the first-paper deliverable and the load-bearing result.

### A3 — Latent-Encoding Quality for WAM Imagination

| | |
|---|---|
| **Cluster** | A — Substrate & Encoding |
| **Thesis** | Once a WAM goes latent, choose the encoder by its *training objective* — semantic / continuous-disentangled over reconstruction / VQ — because that objective, not the latent-vs-pixel split, sets the ceiling on downstream control. The reason it must work: a policy consumes dynamics, not pixels, so a latent trained to reconstruct appearance spends capacity on detail the controller discards. The field spends its effort on latent-vs-pixel and treats the encoder, once latent, as an interchangeable detail. The bet is in First-principles below — at matched architecture and deploy cost, the encoder objective swings closed-loop SR more than most architecture changes. |
| **Anchor papers** | [[2604.02029\|Latent Space Survey]] (survey), [[2511.02097\|WM Manipulation Survey]] (survey), [[2605.06388\|Semantic-LDM-WM]] (method), [[2605.15725\|DiLA]] (method), [[2604.16484\|DexWorldModel]] (method) |
| **Key targets** | Match [[2605.06388\|Semantic-LDM-WM]]'s +9.8 pp closed-loop / +13.6 pp OOD margin of semantic over reconstruction, reproduced on a second backbone; continuous bottleneck beats VQ/VAE on generation quality + training stability ([[2605.15725\|DiLA]]); hold the gain on [[2510.13626\|LIBERO-Plus]] OOD at fixed deploy latency |

**Why it matters.**
- **The gap**: A1 decides *how dense* the imagined state is at train vs deploy; A3 decides *what the latent encodes* once you commit to one — and the second is the under-examined axis, because [[2604.02029|Latent Space Survey]] names evaluability and controllability of the latent as open and [[2511.02097|WM Manipulation Survey]] ranks structured task-relevant representation above raw capacity.
- **Today's answers**: [[2605.06388|Semantic-LDM-WM]] holds the action-conditioned LDM fixed and swaps only the latent's objective (reconstruction-aligned SD3-VAE / VA-VAE vs semantic-aligned V-JEPA 2.1 / Web-DINO / SigLIP 2), finding semantic latents lift closed-loop SR +9.8 pp and OOD +13.6 pp with a stronger IDM Pearson r — *even when reconstruction latents win on pixel fidelity*; [[2604.16484|DexWorldModel]] uses [[2508.10104|DINOv3]] semantic targets to separate interaction from visual noise (94% [[2504.13059|RoboTwin]], zero-shot sim-to-real).
- **The opening**: [[2605.15725|DiLA]] sharpens it from the *type* side: a *continuous* information bottleneck beats discrete VQ and variational VAE on both generation quality and training stability — so not just semantic-vs-reconstruction but the bottleneck *type* is load-bearing, a clean controlled lever.

**First-principles framing.**
- **First principle**: A policy consumes dynamics, not pixels. A latent trained to reconstruct appearance spends capacity on detail the controller discards; a latent trained to predict future semantics keeps exactly the action-relevant structure. What the encoder is *told to preserve* fixes a ceiling on downstream control that no amount of downstream architecture can lift. [[2605.06388|Semantic-LDM-WM]]'s controlled swap demonstrates it: the LDM is held fixed and only the encoder objective changes, yet closed-loop SR swings +9.8 pp.
- **Assumption being challenged**: That once you pick latent over pixel, the encoder is interchangeable — grab any pretrained VAE / VQ tokenizer and move on. [[2605.06388|Semantic-LDM-WM]] shows the encoder objective swings closed-loop SR more than most architecture changes do; [[2605.15725|DiLA]] shows the *type* of bottleneck (continuous vs VQ vs VAE) is itself load-bearing, not a free choice — both bet against encoder-as-detail.
- **The bet**: At matched architecture and matched deploy latency, swapping a reconstruction / VQ latent for a semantic / continuous-disentangled latent yields ≥9.8 pp closed-loop SR and ≥13.6 pp OOD ([[2605.06388|Semantic-LDM-WM]]'s measured margins), and the continuous bottleneck beats VQ/VAE on generation quality + stability ([[2605.15725|DiLA]]) — reproduced on a *second* WAM backbone to show the lever is the encoding, not the paper. Falsifiable: if the margin collapses on a second backbone, the swing was the LDM, not the encoder.

**Related research papers.**

Eight systems that differ on *what the latent is trained to preserve* — the axis the direction turns on (reconstruction / semantic / continuous / disentangled / uncertainty-aware / identifiable). The discriminator is the encoder's training objective:

| System | Encoder objective | Preserves | Key result | What's missing |
|---|---|---|---|---|
| [[2605.06388\|Semantic-LDM-WM]] | semantic vs reconstruction (controlled swap) | action-relevant semantics | +9.8 pp closed-loop, +13.6 pp OOD, stronger IDM r | single backbone only — the reproduction A3 demands |
| [[2605.15725\|DiLA]] | continuous bottleneck vs VQ/VAE | smooth disentangled dynamics | SSIM/LPIPS gains on SSv2/RT-1; better stability | scored on generation quality, not closed-loop SR — the bottleneck-type lever |
| [[2604.16484\|DexWorldModel]] | [[2508.10104\|DINOv3]] causal-semantic targets | interaction vs visual noise | 94% [[2504.13059\|RoboTwin]], zero-shot sim-to-real | the causal-semantic encoding choice, not ablated against reconstruction |
| [[2602.10102\|VideoWorld 2]] | dLDM decouples dynamics from appearance | task-relevant dynamics only | 72.3% step-7 folding | disentangled-encoding evidence — untested under action conditioning |
| [[2601.14354\|VJEPA-Probabilistic]] | variational predictive bottleneck + Bayesian PoE | signal under nuisance | R²>0.84 under noisy-TV where VAE/pixel-AR hit ~0.50 | uncertainty-aware encoding that discards nuisance — not benchmarked on closed-loop SR |
| [[2602.10098\|VLA-JEPA]] | JEPA semantic-predictive (no reconstruction) | predicted future semantics | 97.2% [[2306.03310\|LIBERO]], 79.5% [[2510.13626\|LIBERO-Plus]] | a winning encoding with no reconstruction objective — the second backbone for the swap |
| [[2606.04130\|CLAW (Latent Action WM)]] | continuous latent-action + adversarial reg | leakage-free action latent | 7/10 visual-planning tasks | regularized continuous-action encoding — not compared to VQ at matched dim |
| [[2511.08544\|LeJEPA]] | isotropic-Gaussian via SIGReg | identifiable latent geometry | provably optimal embedding | the encoding-geometry criterion an encoding-quality study is judged against |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (the encoder objective, not density, sets the control ceiling), with the experiment and the Related-table row it lands on.
1. **H1 — The encoding swing reproduces on a non-LDM backbone.**
   - *Prediction*: re-running [[2605.06388|Semantic-LDM-WM]]'s reconstruction-vs-semantic swap on a non-LDM WAM ([[2602.10098|VLA-JEPA]] or [[2604.16484|DexWorldModel]]) reproduces ≥9.8 pp closed-loop / ≥13.6 pp OOD, isolating the encoding as the lever rather than the LDM.
   - *Test*: swap only the encoder objective on the second backbone; report closed-loop SR + OOD at matched architecture.
   - *Row*: Semantic-LDM-WM (controlled swap) → VLA-JEPA (second backbone).
   - *Falsifier*: the margin collapses below ~5 pp on the second backbone → the swing was the LDM, not the encoder.
2. **H2 — Continuous beats VQ beats VAE at matched dimension on closed-loop SR.**
   - *Prediction*: holding latent dimension fixed and ablating [[2605.15725|DiLA]]'s continuous bottleneck vs a VQ tokenizer vs a VAE orders them continuous > VQ > VAE on *closed-loop SR and training stability*, not just SSIM/LPIPS.
   - *Test*: three encoders at matched dim, same downstream policy; report SR + stability, not generation metrics alone.
   - *Row*: DiLA (continuous vs VQ/VAE).
   - *Falsifier*: VQ matches continuous on closed-loop SR → the bottleneck type is a free choice for control.
3. **H3 — Disentangled dynamics survive action conditioning and help control.**
   - *Prediction*: [[2602.10102|VideoWorld 2]]'s dynamics/appearance split survives action conditioning, and keeping *only* the dynamics latent for the policy beats the entangled latent at fixed deploy cost.
   - *Test*: condition the dLDM on actions; compare dynamics-only vs entangled latent on closed-loop SR.
   - *Row*: VideoWorld 2 (disentangled).
   - *Falsifier*: dynamics-only ties entangled → disentanglement buys no control advantage under conditioning.
4. **H4 — Control-winning encodings pass the identifiability test.**
   - *Prediction*: the latents that win control (semantic / continuous) are exactly the ones that pass [[2605.26379|LeJEPA World Model]]'s isotropic-Gaussian identifiability test — encoding quality is a proxy for the membership criterion.
   - *Test*: measure SIGReg/identifiability on each encoder; correlate with closed-loop SR rank.
   - *Row*: LeJEPA (identifiability) / VLA-JEPA (winning encoding).
   - *Falsifier*: a control-winning encoding fails identifiability (or vice versa) → the two criteria are independent.
5. **H5 — The semantic-latent advantage survives A1's dense pixel branch.**
   - *Prediction*: the semantic-latent advantage persists when a dense pixel/3DGS branch supervises training (A1's hybrid) — i.e., dense pixel supervision does not wash out the encoding gap (the orthogonality claim).
   - *Test*: add a renderable-pixel head; re-measure semantic-vs-reconstruction closed-loop SR.
   - *Row*: Semantic-LDM-WM (controlled swap) / cross-ref A1.
   - *Falsifier*: the pixel branch erases the semantic-latent gap → density and encoding interfere, and A1/A3 are not orthogonal.
6. **H6 — Uncertainty-aware encoding wins specifically under distractors.**
   - *Prediction*: [[2601.14354|VJEPA-Probabilistic]]'s variational bottleneck beats deterministic semantic encoders *specifically* on distractor-heavy OOD (where it holds R²>0.84 vs ~0.50), and ties them on clean tasks — so the win is the discard-nuisance mechanism, not capacity.
   - *Test*: compare variational vs deterministic semantic on clean vs noisy-TV-style OOD.
   - *Row*: VJEPA-Probabilistic (uncertainty-aware).
   - *Falsifier*: the variational encoder wins equally on clean tasks → the gain is capacity, not nuisance-discarding.

> [!warning] Risks
> - **Encoding gain is dataset-specific** — the +9.8 / +13.6 pp swing may not transfer off [[2605.06388|Semantic-LDM-WM]]'s Bridge-V2 setup. → H1 reproduces on a second backbone + dataset before claiming the lever is general; report per-dataset deltas.
> - **Semantic latents destabilize diffusion training** — high-dimensional SSL/VL latents historically break diffusion. → Reuse [[2605.06388|Semantic-LDM-WM]]'s wide-head DiT + S-VAE compression recipe rather than feeding raw high-dim latents; H2 reports stability as a first-class metric.
> - **Encoding quality ≠ controllability** — a latent that recovers actions well may still be hard to plan in. → Pair the IDM-recoverability diagnostic with closed-loop SR and [[2605.26379|LeJEPA World Model]]'s identifiability test (H4), never action-recovery alone.

---

## Cluster B — WAM Training-Time Grounding

*A WAM that imagines freely will imagine physically impossible futures, and a policy trained on those futures inherits the impossibility. The four directions install a training-time signal that keeps imagination honest: discrete contact structure (B1), a self-evolution loop that verifies its own dreams (B2), forward-inverse calibration before runtime (B3), and a physics-validation filter on synthesized data (B4).*

### B1 — Contact-Aware (Discrete-Mode) WAM for Fine Manipulation

| | |
|---|---|
| **Cluster** | B — Training-Time Grounding |
| **Thesis** | Give a WAM a *discrete* contact-mode latent (no-contact, making, in-contact, breaking, slipping) with switch dynamics per mode, instead of trying to reach contact physics by scaling a smooth latent. The reason it must work: contact physics jumps sharply — friction-cone boundaries, normal-force singularities, slip-stick are abrupt state changes — and a smooth function approximating a hard step gets exponentially more expensive right at the boundary. The field tries to close the contact gap by adding latent capacity. The bet is in First-principles below — a discrete contact mode reaches assembly precision no smooth WAM reaches at any scale. |
| **Anchor papers** | [[2604.04974\|Video-to-Control Survey]] (survey), [[2510.04978\|Physical AI Survey]] (survey), [[2407.08028\|AutoMate]] (benchmark), [[2604.16484\|DexWorldModel]] (method), [[2604.27367\|DOT-Sim]] (method) |
| **Key targets** | Beat [[2407.08028\|AutoMate]]'s 90.5% contact-naive ceiling ([[2603.15956\|ExpertGen]]) with contact-aware imagination; sub-millimeter assembly; beat [[2602.23253\|SPARR]]'s +74.5% relative SR on unseen [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) transfer; contact-mode classification accuracy vs simulator as the internal diagnostic |

**Why it matters.**
- **The gap**: latent WAMs handle free-space trajectories but fail at insertion/assembly, because contact physics is locally non-smooth (make/break, slip, normal-force singularities) — three deep-dives converge that latent WAMs miss sub-millimeter contact ([[../../../Embodied-AI/08_Latent-World-Models#6. Open Problems|08_Latent-World-Models §6]]), verifiable physics scales poorly to clutter ([[../../../Embodied-AI/11_Physics-Aware-Embodied-AI#8. Open Problems|11_Physics-Aware-Embodied-AI §8]]), and learned sims blur on contact ([[../../../Embodied-AI/14_Sim-to-Real-Transfer#7. Open Problems|14_Sim-to-Real-Transfer §7]]).
- **Today's answers**: the contact gains are all *policy-side* — [[2602.23253|SPARR]] 95–100% [[2407.08028|AutoMate]] (sim + vision-conditioned real residual), [[2603.15956|ExpertGen]] 90.5% (generative prior + distillation) — while the closest substrate, [[2604.16484|DexWorldModel]]'s causal latent ([[2508.10104|DINOv3]] targets, 94% [[2504.13059|RoboTwin]]), keeps contact transitions *continuous*.
- **The opening**: [[2606.05645|Discrete-WAM]] proves a *discrete* shared latent works for joint world + policy (90.4 EPDMS NAVSIM-v2 via discrete diffusion) — in the AV domain where tokens are scene/maneuver units, so the substrate is trainable and stable; whether discrete tokens transfer to make/break/slip *contact* modes is exactly B1's open question, and [[2604.27367|DOT-Sim]]'s differentiable MPM tactile sim now manufactures the make/break/slip labels a smooth WAM cannot (96.55% tumor detection zero-shot, 0.896 mm trajectory error).

**First-principles framing.**
- **First principle**: Contact physics jumps sharply — friction-cone boundaries, normal-force singularities, and slip-stick are abrupt, discrete state changes in the physics itself, not the model. A smooth latent can only represent a hard step by internally splitting into discrete pieces, and approximating it gets exponentially more expensive right at the boundary. [[2604.27367|DOT-Sim]]'s differentiable contact sim demonstrates that make/break/slip are *categorically* distinct regimes with distinct governing equations.
- **Assumption being challenged**: That adding latent capacity (more dimensions, layers, parameters) closes the contact gap — the implicit bet of every scale-up. Capacity never touches the *structural* jump; even [[2604.16484|DexWorldModel]]'s causal latent keeps contact smooth and so caps out before sub-millimeter assembly. [[2606.05645|Discrete-WAM]] bets the opposite — a discrete token substrate is trainable — but in a domain where the discreteness is scene-level, not contact-level.
- **The bet**: A discrete contact mode $c_t \in \{\text{no-contact, making, in-contact, breaking, slipping}\}$ with switch dynamics per mode hits >90.5% [[2407.08028|AutoMate]] (the best a contact-naive WAM reaches) and sub-millimeter assembly that purely smooth WAMs cannot reach at any scale. Falsifiable: if a scaled smooth latent matches the discrete-mode WAM on sub-millimeter insertion, the structural-jump argument is wrong.

**Related research papers.**

Eleven systems that differ on *how contact is represented in the model* — the axis the direction turns on (continuous latent / digital twin / discrete tokens / differentiable sim / policy-side / friction-aware). The discriminator is whether contact is a smooth function or a discrete regime:

| System | Contact representation | Discrete contact? | Key result | What's missing |
|---|---|---|---|---|
| [[2604.16484\|DexWorldModel]] | causal latent ([[2508.10104\|DINOv3]] targets) | no (continuous) | 94% [[2504.13059\|RoboTwin]], zero-shot sim-to-real | the closest WAM substrate, but contact stays smooth |
| [[2606.05645\|Discrete-WAM]] | shared discrete token space (discrete diffusion) | yes — but scene-level | 90.4 EPDMS NAVSIM-v2 (AV) | proves discrete tokens train, but tokens are scene/maneuver, not contact modes |
| [[2604.27367\|DOT-Sim]] | differentiable MPM optical-tactile sim | yes (ground truth) | 96.55% tumor detection zero-shot, 0.896 mm | contact ground truth but no WAM consumer — the distillation teacher (H4) |
| [[2503.17973\|PhysTwin]] | physics-informed deformable twin | no (continuous) | deformable twin from video | no discrete contact event |
| [[2511.07416\|PhysWorld]] | continuous physical WM | no (continuous) | 82% real SR | continuous, no event discretization |
| [[2512.13644\|DexWM]] | diffusion-transformer WM on frozen DINOv2 + hand keypoints | no (continuous) | 83% zero-shot real Franka+Allegro, 0 real data | contact-rich dexterous WM, but continuous contact |
| [[2503.16806\|DyWA]] | FiLM dynamics-adaptation over point cloud | no (continuous, adapted) | +31.5% SR, 68% zero-shot real across frictions | adapts contact dynamics but stays continuous |
| [[2603.15956\|ExpertGen]] | generative prior + [[2506.15799\|DSRL]] + distillation | no (policy-side) | 90.5% [[2407.08028\|AutoMate]] | policy-side improvement, contact not a WM latent |
| [[2602.23253\|SPARR]] | sim + vision-conditioned real residual | no (policy-side) | 95–100% [[2407.08028\|AutoMate]] | policy-side, no WAM — the contact-naive ceiling B1 must beat structurally |
| [[2604.24916\|asRoBallet]] | friction-aware [MuJoCo](https://github.com/google-deepmind/mujoco) + RL | partial (friction-aware) | friction-aware control | a prior for contact-mode losses, not a discrete-mode WAM |
| [[2511.04665\|Real-to-Sim GS]] | 3DGS + soft-body [[2503.17973\|PhysTwin]] | no (continuous twin) | r=0.915 (push-T) / 0.901 (rope) sim-real | the evaluation substrate, not a contact-mode model |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (discrete contact modes reach precision smooth latents cannot), with the experiment and the Related-table row it lands on.
1. **H1 — A discrete contact-mode latent beats a matched smooth latent on sub-millimeter insertion.**
   - *Prediction*: adding $c_t \in \{\text{no-contact, making, in-contact, breaking, slipping}\}$ atop a [[2604.16484|DexWorldModel]]-style causal latent, with continuous dynamics conditioned on $c_t$, beats the same backbone without the discrete mode on [[2407.08028|AutoMate]] sub-millimeter insertion (>90.5%).
   - *Test*: A/B discrete-mode vs continuous-only at matched capacity on AutoMate's 8 tasks.
   - *Row*: DexWorldModel (continuous) vs the discrete-mode variant.
   - *Falsifier*: continuous-only matches the discrete-mode WAM on insertion → capacity, not discreteness, was the constraint.
2. **H2 — A scaled smooth latent does not close the gap.**
   - *Prediction*: scaling [[2511.07416|PhysWorld]]'s continuous physical WM (dimensions/layers/params) raises insertion SR sub-linearly and plateaus *below* the discrete-mode WAM — the structural jump is capacity-insensitive.
   - *Test*: sweep smooth-latent capacity; plot insertion SR vs parameters against the discrete-mode point.
   - *Row*: PhysWorld (continuous).
   - *Falsifier*: smooth SR keeps rising to match the discrete-mode WAM with enough scale → the jump is learnable smoothly.
3. **H3 — Contact-mode-conditional physics losses beat a single global physics loss.**
   - *Prediction*: applying Coulomb friction only in `in-contact` and ballistic dynamics only in `no-contact` (mode-gated losses) beats a single regime-agnostic physics loss on contact-onset-heavy tasks.
   - *Test*: ablate mode-gated vs global physics loss; stratify by contact-onset frequency.
   - *Row*: asRoBallet (friction-aware) as the loss prior.
   - *Falsifier*: the global loss matches mode-gated → conditioning the physics on the mode adds nothing.
4. **H4 — Distilling DOT-Sim contact ground truth supplies the supervision smooth WAMs lack.**
   - *Prediction*: distilling [[2604.27367|DOT-Sim]]'s differentiable make/break/slip labels into the discrete-mode latent gives contact-mode classification accuracy high enough that downstream insertion SR tracks it — a smooth WAM cannot manufacture these labels for itself.
   - *Test*: train the mode classifier on DOT-Sim labels; correlate mode accuracy with insertion SR; compare to a self-supervised contact proxy.
   - *Row*: DOT-Sim (ground truth).
   - *Falsifier*: insertion SR is flat in mode-classification accuracy → the discrete modes are not the operative variable.
5. **H5 — Discrete contact modes transfer sim-to-real on AutoMate / NIST.**
   - *Prediction*: training the discrete-mode WAM on [[2511.04665|Real-to-Sim GS]] twins and evaluating on real [[2407.08028|AutoMate]] / [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/benchmarks-and-datasets-tackle-real-world-robotic) holds the contact-mode advantage zero-shot, beating [[2602.23253|SPARR]]'s +74.5% relative on unseen transfer.
   - *Test*: train in sim twins; eval real; report SR retention and unseen-task relative gain.
   - *Row*: SPARR (policy-side) / Real-to-Sim GS (eval substrate).
   - *Falsifier*: the discrete-mode advantage vanishes on real → the modes overfit the simulator.
6. **H6 — Contact-event time prediction is a useful auxiliary head.**
   - *Prediction*: an auxiliary regression head predicting contact-onset time $\hat t_{\text{contact}}$ (supervised by the simulator) improves pre-contact deceleration and raises insertion SR over the discrete-mode WAM without it.
   - *Test*: add the $\hat t_{\text{contact}}$ head; compare insertion SR + impact force at contact.
   - *Row*: DOT-Sim (ground truth) for the timing supervision.
   - *Falsifier*: the timing head leaves SR and impact force unchanged → onset timing is already implicit in the modes.

> [!warning] Risks
> - **Discrete-latent optimization is high-variance** — Gumbel-softmax / REINFORCE gradients are noisy. → Start soft and harden over training (annealed temperature); report mode-classification accuracy as the convergence diagnostic before downstream SR.
> - **Contact-mode supervision requires a simulator** — real make/break/slip labels are unavailable. → Distill from [[2604.27367|DOT-Sim]] / [[2511.04665|Real-to-Sim GS]] twins where contact ground truth exists (H4); H5 then tests sim-to-real retention.
> - **No published WAM has a discrete contact-event latent** — genuinely unattacked, so a wrong mode taxonomy has no prior art to correct. → Make H1's contact-mode classification accuracy the first internal milestone, before any downstream-SR claim.

### B2 — WAM-Driven Self-Evolution & Recovery

| | |
|---|---|
| **Cluster** | B — Training-Time Grounding |
| **Thesis** | Close a failure-finder → WAM-imagines-failure → GRPO → recover loop where the WAM *generates* the failures the recovery policy trains on, instead of assuming self-evolution needs costly real-world exploration. The reason it must work: an agent only learns to recover from failures it can produce for itself, so reachable competence is bounded by what the WM can *imagine*, not by how much real interaction it logs — and a verifier can screen out bad dreams. The field assumes real experience beats imagined and so self-evolution must run on a real robot. The bet is in First-principles below — imagined rehearsal drives real improvement when the imagined-vs-real correlation is high enough. |
| **Anchor papers** | [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2602.04411\|Self-evolving Embodied AI]] (survey), [[2508.07407\|Self-Evolving AI Agents Survey]] (survey), [[2603.08403\|SPIRAL]] (method), [[2605.22446\|Pre-VLA]] (method) |
| **Key targets** | Imagined-vs-real SR Pearson $\rho$ > 0.7 + continual per-cycle SR improvement; [[2605.22446\|Pre-VLA]]-style verifier ≥0.83 F1 on bad-rollout filtering (+6.83 pp [[2306.03310\|LIBERO]]); catastrophic forgetting held to [[2401.16650\|WMAR]]-class +0.071 vs 0.665 baseline |

**Why it matters.**
- **The gap**: [[2604.22748|Agentic World Modeling Survey]] defines L1 Predictor / L2 Simulator / L3 Evolver and calls physical L3 Evolver the gap ("emerging not mature") — an agent that revises itself when predictions fail — yet no system integrates detection + diagnosis + recovery + memory + WAM-driven imagination + rollout verification end-to-end.
- **Today's answers**: the pieces exist separately — [[2412.02818|RoboMD]] (RL adversary probes a *real* robot), [[2510.09459|FIPER]] / [[2506.09937|SAFE]] (detection only, no recovery), [[2401.16650|WMAR]] (continual update, +0.071 vs 0.665 forgetting), and now [[2605.22446|Pre-VLA]] (filters unsafe actions and *truncates unreliable WM imaginations*, +6.83 pp [[2306.03310|LIBERO]]) — but each is one stage, not the loop.
- **The opening**: [[2603.08403|SPIRAL]] already closes a think-act-reflect cycle — a PlanAgent decomposes goals, an Action-Conditioned WM imagines, a CriticAgent verifies and feeds GRPO that *internalizes* the reflection (58.72% EgoPlan-Bench, +3.94 pp over GPT-5.1) — proving the imagine→verify→GRPO spine works; it self-improves *generation* fidelity rather than driving detect→recover, which is exactly the seam B2 fills.

**First-principles framing.**
- **First principle**: How well an agent prepares is bounded by what it can imagine. A recovery policy trains on the failures it sees, so an agent only learns to recover from failures it can *generate* for itself — making a self-improvement loop capped by how widely the WM can imagine failure, not by how much real interaction it logs. [[2603.13528|Counterfactual Failure Synthesis]]'s Dream2Fix demonstrates the supply side: perturbing actions in a generative WM yields 120K counterfactual-failure + recovery pairs that lift real recovery to 46%.
- **Assumption being challenged**: That self-evolution needs real exploration because real experience beats imagined — held by every real-robot RL loop. Real failure-finding is costly and irreversible (robot time, safety); a good-enough WAM can drive real improvement from imagined failures with only *occasional* real checking, provided a verifier ([[2605.22446|Pre-VLA]]) screens out bad dreams. [[2509.19080|World4RL]] bets this way: PPO inside imagined rollouts of a frozen diffusion WM reaches 93.3% real Franka (+25 pp over BC).
- **The bet**: A closed loop — failure-finder → WAM imagines failure → GRPO over (action, imagination) → recovery — gives steady per-cycle SR gains, with imagined and real success correlating above 0.7 (Pearson $\rho$), *without* forgetting ([[2401.16650|WMAR]]-style FIFO + reservoir, +0.071 vs 0.665), and a [[2605.22446|Pre-VLA]]-class verifier screening bad rollouts at ≥0.83 F1. Falsifiable: if imagined SR rises while real SR stalls ($\rho$ collapses), the loop is gaming the WM, not improving the policy.

**Related research papers.**

Eleven systems that differ on *which stage of the detect→imagine→recover→retain loop* they build — the axis the direction turns on (detect / imagine-failure / RL-on-imagination / recover / verify / retain). The discriminator is whether the WAM *drives the loop* or sits at one stage:

| System | Loop stage | WAM drives loop? | Key result | What's missing |
|---|---|---|---|---|
| [[2603.08403\|SPIRAL]] | imagine→verify→GRPO (generation) | partial (improves WM) | 58.72% EgoPlan-Bench, +3.94 pp over GPT-5.1 | self-improves *generation* fidelity, not detect→recover — the closest spine |
| [[2603.13528\|Counterfactual Failure Synthesis]] | imagine-failure (offline) | yes (offline) | 120K pairs, 46% real recovery | imagine-then-recover, but offline, not a closed online loop |
| [[2509.19080\|World4RL]] | RL-on-imagination | yes (frozen WM) | 93.3% real Franka (+25 pp over BC) | PPO in imagined rollouts, but no failure-finder or recovery stage |
| [[2603.17808\|EVA]] | RL-on-imagination (executability) | yes (aligns WM) | kinematic plausibility +20.9% (→91.4%), 64.0% real | RL aligns the WM to executability, not a detect→recover loop |
| [[2602.21633\|SC-VLA]] | imagine→recover (residual RL) | yes (sparse imagination) | 86% ManiSkill3, 71% real ARX5 | imagination-driven recovery from self-predicted error, but no continual retention |
| [[2606.03385\|GTP-FA]] | detect→diagnose→recover | no (policy-side) | +54.0 pp terminal SR ManiSkill3, real π0.5 11.2→76.8% | the loop B2 wraps, but failures are real, not WAM-imagined |
| [[2509.04018\|FPC-VLA]] | recover (VLM supervisor) | no (policy-side) | 86.0% real SR, disturbance 31.3→16% | the recovery half, no WAM-driven failure generation |
| [[2605.22446\|Pre-VLA]] | verify (runtime) | no (verifier) | +6.83 pp [[2306.03310\|LIBERO]], truncates unreliable imaginations | verification only — the trust valve the loop needs |
| [[2412.02818\|RoboMD]] | detect (RL adversary) | no (real robot) | RL adversary for failure discovery | probes a real robot, not WAM-driven |
| [[2401.16650\|WMAR]] | retain (continual) | n/a (memory) | +0.071 vs 0.665 forgetting | the retention lever for per-cycle updates, no imagination loop |
| [[2606.03598\|PHASER]] | retain (phase-aware replay) | n/a (memory) | +31% ASR over standard replay, 85.8% LIBERO-Long | interference-aware retention, no failure-generation loop |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a WAM-driven loop drives real improvement at high imagined-vs-real $\rho$), with the experiment and the Related-table row it lands on.
1. **H1 — A WAM-driven failure-finder generates failures that transfer to real recovery.**
   - *Prediction*: recasting [[2412.02818|RoboMD]] as a WAM adversary (failure-finder proposes initial states, WAM rolls forward, policy judged on imagined outcomes) yields recovery skills that transfer to real failures at least as well as [[2603.13528|Counterfactual Failure Synthesis]]'s offline 46% real recovery.
   - *Test*: train recovery on WAM-imagined failures; evaluate real-robot recovery SR against the offline-synthesis baseline.
   - *Row*: RoboMD (detect) / Counterfactual Failure Synthesis (imagine-failure).
   - *Falsifier*: WAM-imagined failures give lower real recovery than offline synthesis → online imagination adds no coverage.
2. **H2 — Per-cycle SR rises only while imagined-vs-real $\rho$ stays > 0.7.**
   - *Prediction*: across self-evolution cycles, real SR improves monotonically while $\rho$ > 0.7 and stalls once $\rho$ drops — so $\rho$ is the operative stop condition, validated against [[2606.05773|PiL-World]]'s r=0.94 closed-loop reference.
   - *Test*: run the loop; track real SR and $\rho$ per cycle; correlate SR-gain with $\rho$.
   - *Row*: SPIRAL (imagine→verify→GRPO) with PiL-World as the $\rho$ anchor.
   - *Falsifier*: real SR keeps rising after $\rho$ < 0.7 → the WM need not be grounded for the loop to work.
3. **H3 — A runtime verifier on imagined rollouts beats an unverified loop.**
   - *Prediction*: gating recovery candidates through a [[2605.22446|Pre-VLA]]-class verifier (≥0.83 F1) before execution beats the same loop without verification, with the gap largest on tasks where the WM hallucinates most.
   - *Test*: A/B verified vs unverified recovery selection; stratify by WM hallucination rate.
   - *Row*: Pre-VLA (verify).
   - *Falsifier*: verification leaves SR unchanged → the WM's dreams are reliable enough to skip the filter.
4. **H4 — GRPO over joint (action, imagination) beats RL on action alone.**
   - *Prediction*: optimizing GRPO over the joint (action, imagination) log-prob — reward = imagined task SR + COD + novelty — beats action-only PPO-in-imagination ([[2509.19080|World4RL]]) on per-cycle gain, because the joint objective shapes the WM and policy together.
   - *Test*: A/B joint-GRPO vs action-only RL inside the same imagined rollouts.
   - *Row*: World4RL (RL-on-imagination).
   - *Falsifier*: action-only RL matches joint-GRPO → shaping the imagination jointly buys nothing.
5. **H5 — Phase-aware replay holds forgetting near WMAR levels across cycles.**
   - *Prediction*: updating from recoveries with [[2606.03598|PHASER]]'s phase-aware interference-aware replay holds catastrophic forgetting to [[2401.16650|WMAR]]-class (+0.071 vs 0.665) across sequential tasks, beating naive fine-tuning.
   - *Test*: sequential-task forgetting probe with PHASER vs WMAR FIFO vs naive update.
   - *Row*: PHASER (retain) / WMAR (retain).
   - *Falsifier*: forgetting exceeds 0.2 with PHASER → per-cycle updates cannot retain without a real-data anchor.
6. **H6 — In-loop red-teaming prevents misevolution drift.**
   - *Prediction*: running a [[2604.05498|JailWAM]]-style red-team probe each cycle (with [[2509.15194|EVOL-RL]] novelty against entropy collapse) keeps real SR monotonic where an unprobed loop drifts into reward-hacked imagined SR.
   - *Test*: A/B red-teamed vs unprobed loops over many cycles; track real-vs-imagined SR divergence.
   - *Row*: SPIRAL (imagine→verify→GRPO) extended with the red-team probe.
   - *Falsifier*: the unprobed loop stays grounded → in-loop red-teaming is unnecessary.

> [!warning] Risks
> - **Misevolution drift** — self-reward biases amplify across cycles ([[2509.26354|Misevolution]] names the risk class). → Red-team after each cycle ([[2604.05498|JailWAM]] / [[2506.07468|SELF-REDTEAM]] probes, H6); keep a novelty bonus against entropy collapse.
> - **Reward hacking on imagined SR** — the model games the WM, not reality. → Periodic real-robot validation + [[2605.22446|Pre-VLA]]'s rollout truncation; the $\rho$ > 0.7 gate (H2) is the stop condition that catches it.
> - **WAM drifts from real dynamics** — imagination diverges over cycles, so old recoveries become invalid. → Outer-loop WAM updates ([[2603.04029|Self-Adapting RL]]) and the $\rho$ stop condition; validate against the joint causal-binding metric in the umbrella, not imagined SR alone.

### B3 — Self-Verifying / Calibrated-Imagination WAM

| | |
|---|---|
| **Cluster** | B — Training-Time Grounding |
| **Thesis** | Make a WAM's imagination trustworthy at *training* time using the forward-inverse asymmetry — judge whether an imagined subgoal is plausible (cheap, from action-free video) and whether it is reachable (cheap, from a small inverse model) — instead of verifying a finished dream at runtime. The reason it must work: generating a transition and checking one are not equally hard — action-free video is abundant and action-relevant features are low-dimensional, so verifying is structurally cheaper than generating, at any scale. The field filters the dream after it is generated. The bet is in First-principles below — calibrate the dream while training so there is less to truncate. |
| **Anchor papers** | [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2310.06253\|Objective Mismatch MBRL Survey]] (survey), [[2601.07823\|Video Generation in Robotics Survey]] (survey), [[2604.01985\|WAV]] (method), [[2504.16680\|RWM-U]] (method) |
| **Key targets** | ≥2× WM sample-efficiency + 22% downstream reward with no extra action labels ([[2604.01985\|WAV]]); epistemic-uncertainty gating 0.91 normalized reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/) ([[2504.16680\|RWM-U]]); imagined-vs-real $\rho$ maximized as the calibration objective (shared with B2) |

**Why it matters.**
- **The gap**: [[2604.22748|Agentic World Modeling Survey]]'s L3 Evolver "revises its own model when predictions fail" — but the usual tool for knowing *when* a prediction failed is uncertainty estimation, which [[2604.01985|WAV]] shows "often fails in under-explored data regions where new information is most needed," exactly where calibration matters, and [[2310.06253|Objective Mismatch MBRL Survey]] generalizes it: low predictive WM loss does not imply high downstream return.
- **Today's answers**: the field verifies at *runtime* — [[2605.22446|Pre-VLA]] truncates unreliable imaginations (+6.83 pp [[2306.03310|LIBERO]]), [[2510.09459|FIPER]] / [[2506.09937|SAFE]] detect failure post-hoc — patching a dream after it is generated rather than shaping it during training.
- **The opening**: two results reframe the problem as a train-time lever — [[2604.01985|WAV]] exploits the forward/inverse asymmetry to turn verification into a self-improving training cycle (2× sample-efficiency, +22% reward, no extra labels), and [[2504.16680|RWM-U]] shows an ensemble's epistemic uncertainty, used to *penalize* imagined rollouts, makes offline MBRL work on real quadrupeds and humanoids (0.91 reward).

**First-principles framing.**
- **First principle**: Making a prediction and checking one are not equally hard. Video without action labels is plentiful, so judging whether an imagined future *looks* plausible is cheap; and the action-relevant part of a state is low-dimensional, so judging whether a future is *reachable* by some action needs little labeled data. A checker that exploits this gap is fundamentally cheaper than the generator it checks. [[2604.01985|WAV]] proves the asymmetry is exploitable: a sparse inverse model is more OOD-robust than a dense one and prioritizes where plausible and predicted futures disagree.
- **Assumption being challenged**: That the reliability gap closes by estimating uncertainty *better* — held by the runtime-verification line. [[2604.01985|WAV]] shows plain uncertainty estimates fail right where they are needed; [[2504.16680|RWM-U]] shows uncertainty helps only when it *steers* the training objective, not when it merely reports a confidence number. B3 shapes the dream while training, not after.
- **The bet**: Using the make-vs-check gap as a training signal — judge plausibility (action-free generator) and reachability (small inverse model) — yields ≥2× WM sample-efficiency and +22% downstream reward with *no extra action labels* ([[2604.01985|WAV]]), and uncertainty-based gating reaches 0.91 reward on real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/) ([[2504.16680|RWM-U]]). Falsifiable: if a runtime-only verifier matches train-time calibration on sample-efficiency and downstream reward, calibrating during training buys nothing.

**Related research papers.**

Twelve systems that differ on *when and how the imagination is made trustworthy* — the axis the direction turns on (train-time asymmetry / train-time uncertainty / runtime filter / detection-only / $\rho$-calibration / IDM-reward). The discriminator is train-time-shaping vs runtime-filtering:

| System | Trust mechanism | When | Key result | What's missing |
|---|---|---|---|---|
| [[2604.01985\|WAV]] | forward-inverse asymmetry self-improving cycle | train-time | 2× sample-eff, +22% reward, no extra labels | the calibration-as-training exemplar — not yet tied to a $\rho$-objective |
| [[2504.16680\|RWM-U]] | ensemble epistemic uncertainty penalty ([[2005.13239\|MOPO]]) | train-time | 0.91 reward real [ANYmal D](https://www.anybotics.com/robotics/anymal/) / [Unitree G1](https://www.unitree.com/g1/) | locomotion only; uncertainty must gate, not just report |
| [[2605.04709\|ELVIS]] | UCB-gated λ-return truncates uncertain futures | train + plan | SOTA vs TD-MPC2 / DreamerV3 on 14 DMC, sim-to-real 2.2±0.4 mm | the latent sibling of RWM-U's gating, no inverse-asymmetry signal |
| [[2602.20057\|AdaWorldPolicy]] | WM prediction error as self-supervised LoRA signal | train-time | 0.96 LIBERO-10, OOD recovery at 4 Hz | uncertainty steers training, not just reports — no forward/inverse split |
| [[2509.23958\|RLIR]] | GRPO on inverse-dynamics frame-level reward | post-train | +5–10% action-classification across AR + diffusion WMs | IDM reward beats human-preference + pixel rewards — a reward, not a sample-efficiency cycle |
| [[2606.02486\|AHEAD]] | uncertainty-gated adaptive horizon-halting | runtime (calibrated) | 93.7% vs 48% under acceleration | calibration *in action* at speed, but no train-time asymmetry signal |
| [[2605.22446\|Pre-VLA]] | preemptive runtime verifier | runtime | +6.83 pp [[2306.03310\|LIBERO]] | runtime filter, not train-time calibration — B3's complement |
| [[2510.09459\|FIPER]] | predictive failure via OOD + uncertainty | runtime | failure prediction | detection only, no training signal |
| [[2606.05773\|PiL-World]] | chunk-wise policy-in-the-loop closed-loop WM | eval | imagined-vs-real r 0.94, gap 63.2→12.0% | the $\rho$-calibration target B3 maximizes — evaluates rather than trains on it |
| [[2606.04463\|OSCAR]] | skeleton-conditioned (URDF/MANO) action-following | train (conditioning) | Pearson r +0.852 with RoboArena, MAE 1.73 pp | conditioning keeps $\rho$ high, not the inverse-asymmetry mechanism |
| [[2511.11520\|Video WM Policy Eval]] | action-conditional WM scores policies (VLM judge) | eval | r 0.833–0.879 sim / 0.687 real | measures $\rho$, does not train to maximize it |
| [[2605.06732\|Training in Imagination]] | decomposes return-gap into dynamics + reward error | analysis | reward error decays fast (0.96) vs dynamics (0.11) | tells calibration where to spend the data budget — an analysis, not a method |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (train-time calibration via the make-vs-check gap beats runtime filtering), with the experiment and the Related-table row it lands on.
1. **H1 — A forward-inverse verifier on a latent WAM beats an uncertainty-only baseline.**
   - *Prediction*: wrapping [[2604.01985|WAV]]'s subgoal-generator + sparse-inverse decomposition around a JEPA WAM ([[2602.10098|VLA-JEPA]] / [[2605.25313|UWM-JEPA]]) gives ≥2× WM sample-efficiency over an uncertainty-only calibration baseline at equal labels.
   - *Test*: A/B forward-inverse vs uncertainty-only on the same WAM; report sample-efficiency + downstream reward.
   - *Row*: WAV (train-time asymmetry).
   - *Falsifier*: uncertainty-only matches the asymmetry signal → the make-vs-check gap is not the lever.
2. **H2 — Epistemic-uncertainty gating as a dense reward stabilizes A1's latent rollout.**
   - *Prediction*: adapting [[2504.16680|RWM-U]]'s [[2005.13239|MOPO]] penalty to a latent-consistency reward on A1's hybrid backbone stabilizes the latent-rollout objective (lower divergence over horizon) vs an ungated rollout.
   - *Test*: add the uncertainty penalty to A1's latent rollout; measure rollout divergence vs horizon.
   - *Row*: RWM-U (train-time uncertainty) / ELVIS (UCB-gated).
   - *Falsifier*: the penalty leaves rollout divergence unchanged → uncertainty gating does not stabilize the latent.
3. **H3 — Training to maximize imagined-vs-real $\rho$ beats gating on it.**
   - *Prediction*: treating the B2 $\rho$ > 0.7 gate as B3's *objective* (train the WM to maximize imagined-vs-real SR correlation directly, against [[2606.05773|PiL-World]]'s r=0.94 reference) yields higher final $\rho$ than using $\rho$ only as a stop condition.
   - *Test*: A/B $\rho$-as-objective vs $\rho$-as-stop-condition; report final $\rho$ and downstream SR.
   - *Row*: PiL-World ($\rho$-calibration) / Video WM Policy Eval (measures $\rho$).
   - *Falsifier*: optimizing $\rho$ directly does not raise final $\rho$ over gating → $\rho$ is not directly trainable.
4. **H4 — Verifier disagreement is a useful active-data signal.**
   - *Prediction*: using [[2604.01985|WAV]]'s plausibility/reachability discrepancy to choose which real-robot interactions to collect next (closing the loop with B2's failure-finder) reaches target SR with fewer real interactions than uniform collection.
   - *Test*: discrepancy-driven vs uniform real-data collection; report real-interaction budget to fixed SR.
   - *Row*: WAV (train-time asymmetry).
   - *Falsifier*: discrepancy-driven collection ties uniform → the disagreement signal carries no information about what to collect.
5. **H5 — The IDM reward beats human-preference and pixel rewards for WM calibration.**
   - *Prediction*: [[2509.23958|RLIR]]'s inverse-dynamics frame-level reward calibrates a WM (higher action-recoverability) more than a human-preference or pixel reward at matched budget, across AR and diffusion WMs.
   - *Test*: post-train the same WM with IDM vs preference vs pixel reward; report action-classification accuracy.
   - *Row*: RLIR (IDM-reward).
   - *Falsifier*: pixel or preference reward matches IDM → the inverse signal is not the calibration lever.
6. **H6 — Sparse-inverse OOD robustness holds in contact-rich regimes.**
   - *Prediction*: [[2604.01985|WAV]]'s sparse-inverse OOD robustness holds on contact-rich tasks when paired with B1's discrete contact modes — i.e., the low-dimensional action features remain recoverable across make/break transitions.
   - *Test*: evaluate sparse-vs-dense inverse on contact-onset-heavy tasks with B1's contact-mode gating.
   - *Row*: WAV (train-time asymmetry) / cross-ref B1.
   - *Falsifier*: the sparse inverse drops contact transients → calibration must go dense in contact, bounding the claim.

> [!warning] Risks
> - **Sparse inverse model misses subtle dynamics** — low-dimensional action features may drop contact transients. → Bound the claim to where action-relevant features are recoverable; pair with B1's discrete contact modes for contact-rich regimes (H6).
> - **Uncertainty gating too conservative** — penalizing all high-uncertainty states kills exploration ([[2504.16680|RWM-U]]'s penalty coefficient is a critical hyperparameter). → Tune the penalty on a held-out real-robot calibration set, not in simulation alone; H2 reports the exploration cost.
> - **Calibration ≠ correctness** — a WM can be well-calibrated about being wrong. → Validate against B2's imagined-vs-real $\rho$ (H3) AND the joint causal-binding metric in the umbrella, not calibration alone.

### B4 — WAM-as-Data-Engine

| | |
|---|---|
| **Cluster** | B — Training-Time Grounding |
| **Thesis** | Treat a generative WAM's highest-value output as a *training corpus* a separate policy consumes, not as an in-episode rollout or safety check. The reason it must work: how good a policy can get is set by how much variety its data covers and how physically correct it is — not by where the data came from — and a WAM can manufacture variety (objects, scenes, views, bodies) real collection cannot afford. The field treats WAM output as something you plan or verify within one episode. The bet is in First-principles below — the durable product is data, and a physics-validation filter is what makes it executable. |
| **Anchor papers** | [[2605.12090\|WAM Survey]] (survey), [[2601.15533\|Actionable Simulators]] (survey), [[2604.15395\|Foundation Models in Robotics Survey]] (survey), [[2606.02577\|RoboDream]] (method), [[2606.04708\|VISTA]] (method) |
| **Key targets** | Downstream SR over real-only by ≥25 pp ([[2606.02577\|RoboDream]] Gen-Mix 62.5% vs real-only 36.3%); collection cost ≥2× lower ([[2606.02577\|RoboDream]] 2.2×); validated-vs-unfiltered downstream SR gap ([[2606.04708\|VISTA]] 0.65 vs 0.00); zero-shot lift from imagined-corpus pretraining ([[2606.01027\|τ0-WM]] 0.55 vs 0.14) |

**Why it matters.**
- **The gap**: B1–B3 consume the WAM's imagination *inside* an episode — contact to roll out (B1), failures to recover from (B2), dreams to calibrate (B3) — but real robot data is the binding constraint on policy competence and teleoperation does not scale, while [[2605.12090|WAM Survey]] names "data-ecosystem mixing" and [[2604.15395|Foundation Models in Robotics Survey]] names dataset/challenge mapping as the underexploited output.
- **Today's answers**: three 2026 results show the WAM-as-data-engine already beats real collection — [[2606.02577|RoboDream]] decouples robot motion from scene/object context and synthesizes demos compositionally (Gen-Mix 62.5% vs 36.3% real-only, 2.2× faster); [[2606.01027|τ0-WM]] pretrains on ~27,300 hours of heterogeneous imagined-plus-real data and triples zero-shot SR (0.55 vs 0.14).
- **The opening**: [[2606.04708|VISTA]] supplies the missing discipline — physics-validate every synthesized trajectory because raw human-collected (UMI) data is often kinematically infeasible — its validated subset trains to 0.65 OSR while the unfiltered-low subset trains to 0.00, the cleanest proof the filter is load-bearing.

**First-principles framing.**
- **First principle**: How good a policy can get is set by how much variety its training data covers and how physically correct that data is — not by its provenance. A generative WAM can manufacture variety (new objects, scenes, camera views, robot bodies) real collection cannot afford, making it a variety-widening machine for whatever consumes its data. [[2606.02577|RoboDream]]'s compositional decoupling demonstrates it: altering priors yields novel objects/scenes/tasks/viewpoints with no retraining.
- **Assumption being challenged**: That a WAM's outputs are rollouts or dreams — short-lived, used up within one episode — held by B1–B3 and the runtime-tool framing. [[2606.02577|RoboDream]], [[2505.12705|DreamGen]], and [[2606.01027|τ0-WM]] flip it: the lasting product is a *dataset*, and the WAM is a data engine feeding a separate policy.
- **The bet**: A physics-validated WAM data engine beats real-data-only collection by ≥25 pp SR ([[2606.02577|RoboDream]] 62.5% vs 36.3% = +26.2 pp) at ≥2× lower cost (2.2×) — *and* the physics filter does real work, not decoration ([[2606.04708|VISTA]]: validated 0.65 vs unfiltered 0.00). Unlike B2 (imagines *failures* to improve a policy that already exists), B4 imagines *demonstrations* to bootstrap a policy that does not yet exist. Falsifiable: if synthesized-plus-real ties real-only at matched policy and budget, or if the validation filter does not change downstream SR, the engine adds nothing.

**Related research papers.**

Sixteen systems that differ on *what kind of data engine the WAM is and whether it validates physics* — the axis the direction turns on (compositional video / unified video-action / physics-validated / digital-twin / procedural / reward-generator / flow-extraction). The discriminator is generative-engine-with-validation vs not:

| System | Engine type | Physics-validated? | Key result | What's missing |
|---|---|---|---|---|
| [[2606.02577\|RoboDream]] | compositional video-diffusion (motion ⊥ scene) | no | Gen-Mix 62.5% vs 36.3% real-only, 2.2× faster | the data-engine exemplar — no physics-validation filter |
| [[2606.01027\|τ0-WM]] | unified video-action WM (~27,300 hrs) | partial (rectifies) | zero-shot 0.55 vs 0.14; test-time rectify 0.43→0.60 | engine + rectifier in one backbone — validation is implicit |
| [[2606.04708\|VISTA]] | physics-validated UMI-data adaptation | yes (explicit) | validated 0.65 vs 0.00 low-score | the validation discipline B4 makes mandatory — not itself a generative engine |
| [[2505.12705\|DreamGen]] | video WMs as synthetic data generators | no | 22 novel behaviors, 10 unseen environments | the video-WM-as-data-engine precedent, no validation filter |
| [[2511.19861\|GigaWorld-0]] | production-scale 2B-MoE video + 3DGS + physics | yes (executable traj) | VLA trained *only* on its data works real; 82.07 PBench | the large-scale existence proof — heavy infrastructure |
| [[2412.14957\|DREMA]] | compositional WM (3DGS + physics) | yes (twin physics) | low-data imitation + novel-config generalization | digital-twin generator, not a video-diffusion engine |
| [[2603.16861\|MolmoBot]] | procedurally generated sim data | no (procedural) | 79.2% real Franka FR3 | procedural generation, not a learned WM engine |
| [[2603.08546\|Interactive World Simulator]] | consistency-model AE + action-conditioned latent | yes (fidelity check) | policies on its data 87.9% vs 90.3% real, 0.85–0.99 corr | data-engine-with-fidelity-check precedent, not compositional |
| [[2606.05979\|WLA]] | action-free cross-embodiment video learning | n/a (source) | nearly triples unseen-task SR | the cross-embodiment data source for Q3, not a full engine |
| [[2511.04665\|Real-to-Sim GS]] | 3DGS + soft-body twins | yes (sim-real corr) | r=0.915 / 0.901 sim-real | supplies the validation substrate, does not synthesize demos |
| [[2512.00961\|GenReward]] | frozen video diffusion → multi-granular RL reward | n/a (reward) | beats DreamerV3 (Bin-Picking 398→822) | the imagination-as-reward variant, not a demonstration corpus |
| [[2512.24766\|Dream2Flow]] | image-to-video → 3D object flow → action inference | partial (flow) | up to 8/10 real tasks rigid/articulated/deformable | the flow-extraction data-engine variant |
| [[2602.12099\|GigaBrain-0.5M*]] | RAMP + human-in-the-loop + continual joint VLA/WM | yes (HITL) | 100% Juice-Prep, +30 pp over RECAP | self-improving closed-loop engine — needs human-in-the-loop |
| [[2506.22007\|RoboEnvision]] | hierarchical KeyframeDiff + FillingDiff (long-horizon) | no | 67.4% on 45 LHMM tasks vs UniPi 23.5% | the long-horizon synthetic-data source, no validation |
| [[2510.26583\|Emu3.5]] | 34.1B native next-state predictor (~63M videos) | no | 67.1% win vs Gemini-2.5-Flash on manipulation | the internet-scale generative substrate, no physics filter |
| [[2602.23253\|SPARR]] | sim + vision-conditioned real residual | partial (residual) | 95–100% [[2407.08028\|AutoMate]] | a data-augmentation point, not a generative engine |

**Hypotheses & tests.** Each item is a falsifiable sub-hypothesis of the FP bet (a physics-validated WAM data engine beats real-only and the filter is load-bearing), with the experiment and the Related-table row it lands on.
1. **H1 — The physics-validation filter is load-bearing, reproduced on a second generator.**
   - *Prediction*: putting [[2606.04708|VISTA]]'s continuity / self-collision / execution-fidelity scoring downstream of [[2606.02577|RoboDream]]'s compositional generator reproduces VISTA's validated-vs-unfiltered gap (0.65 vs 0.00) — i.e., the filter does real work on a *different* engine.
   - *Test*: ablate validated-vs-unfiltered downstream SR on RoboDream-generated data.
   - *Row*: VISTA (physics-validated) on RoboDream (compositional).
   - *Falsifier*: validated ≈ unfiltered downstream SR → the filter is decoration for this generator.
2. **H2 — Gen-Mix beats both extremes, and the optimal ratio is task-family-specific.**
   - *Prediction*: sweeping the synthesized:real ratio, downstream SR peaks at an interior Gen-Mix point ([[2606.02577|RoboDream]] 62.5% beats Real-50 36.3% and Orig-100 0%), and the peak ratio differs across task families.
   - *Test*: sweep the ratio per task family; report the SR-maximizing mix.
   - *Row*: RoboDream (compositional).
   - *Falsifier*: SR is monotone in real-fraction (more real always better) → the engine only augments, never substitutes.
3. **H3 — The engine synthesizes usable demos for an embodiment with zero real demos of the task.**
   - *Prediction*: using [[2606.05979|WLA]]'s action-free cross-embodiment video as a source, the engine synthesizes demos that train a target embodiment with *zero* real demos of the target task above a no-synthesis baseline.
   - *Test*: hold out all real demos of a target task on a target embodiment; train on synthesized demos only.
   - *Row*: WLA (cross-embodiment source).
   - *Falsifier*: zero-real-demo synthesis does not beat the no-synthesis baseline → cross-embodiment transfer needs real target data.
4. **H4 — Co-training the engine on its own rectification signal improves synthesized-data quality.**
   - *Prediction*: [[2606.01027|τ0-WM]] uses one backbone for generation and test-time rectification; co-training the engine on its rectification signal (closing B3's calibration into B4's generation) raises downstream SR over a generation-only engine.
   - *Test*: A/B engine-with-rectification-co-training vs generation-only; report downstream SR.
   - *Row*: τ0-WM (unified engine+rectifier).
   - *Falsifier*: co-training ties generation-only → the rectification signal does not improve the corpus.
5. **H5 — Prop-free teleoperation scales without downstream SR loss.**
   - *Prediction*: extending [[2606.02577|RoboDream]]'s kinematic-only (prop-free) collection — imaginary objects, visual synthesis later — covers a measurable fraction of a manipulation curriculum with no downstream SR loss vs full teleoperation.
   - *Test*: collect prop-free vs full-prop for a curriculum; compare downstream SR and collection cost.
   - *Row*: RoboDream (compositional).
   - *Falsifier*: prop-free collection loses SR vs full-prop → the prop signal is load-bearing and cannot be deferred.
6. **H6 — Synthesized data widens OOD coverage beyond real-only.**
   - *Prediction*: a policy trained on the validated synthesized corpus generalizes wider on [[2510.13626|LIBERO-Plus]] OOD than a real-only policy at matched in-distribution SR — the variety claim, not just the SR claim.
   - *Test*: match in-dist SR between synthesized-trained and real-trained policies; compare LIBERO-Plus OOD.
   - *Row*: GigaWorld-0 (large-scale) / Interactive World Simulator (fidelity-checked).
   - *Falsifier*: OOD coverage ties real-only at matched in-dist SR → the engine's diversity is shallow.

> [!warning] Risks
> - **Synthesized data looks plausible but is not executable** — physically infeasible demos teach the wrong dynamics. → Make [[2606.04708|VISTA]]'s physics-validation filter mandatory, not optional (H1); report validated-vs-unfiltered downstream SR as the first ablation.
> - **Distribution narrows to the engine's biases** — the WM only synthesizes what it has seen, so apparent diversity may be shallow. → Sweep the imagined:real mixing ratio (H2, [[2606.02577|RoboDream]] Gen-Mix beats both extremes) and keep a real-data anchor; never train on synthesized data alone.
> - **Compounding error** — a policy trained on a WM's data inherits the WM's failure modes silently. → Validate downstream on a real-robot held-out set and on [[2510.13626|LIBERO-Plus]] OOD (H6), not only on in-distribution synthesized evals.

---

## Cross-Cutting Themes

> [!tip] Latent Prediction Is the Dominant Substrate — and Now Has a Formal Membership Test
> A1, A2, A3, and B2 all assume "dense signal at training, latent at deployment" with JEPA / DiT-on-latent backbones, but the field has lacked a test for *when* a learned latent is actually a world model. [[2605.26379|LeJEPA World Model]] supplies it (identifiable iff isotropic-Gaussian, then latent planning matches an oracle), and [[2605.25313|UWM-JEPA]] extends the substrate to belief space. So A1's hybrid latents, A2's tactile-imagination latent, A3's encoding-quality choice, and B2's self-evolution rollouts answer to one membership test instead of convention — and A3 makes the sharpest use of it, asking whether the semantic / continuous latents that win control are exactly the ones that pass the isotropic-Gaussian test (its H4).

> [!tip] Verifiable Predicates over Imagined State Turn Diagnosis into Action
> B1, B2, and B3 each make the recurring "statistical correlation ≠ causal understanding" diagnosis enforceable on the *imagination itself*, not just the pixels: B1 makes contact a discrete verifiable transition ($c_t \in$ {no-contact, making, in-contact, breaking, slipping}), B2 makes recovery contingent on a verified imagined rollout, and B3 makes the forward-inverse asymmetry a train-time calibration signal. [[2604.01985|WAV]]'s asymmetry and [[2605.22446|Pre-VLA]]'s rollout truncation are the shared mechanism — and A2's imagined wrench is one more channel the same predicate machinery must score before the policy trusts it.

> [!tip] Calibrated Imagination Is the Training-Time Twin of Runtime Verification
> B3, B2, and A2 form a trust stack at three different times. B3 calibrates imagination at *training* time (forward-inverse asymmetry, [[2604.01985|WAV]] 2× sample-eff; epistemic gating, [[2504.16680|RWM-U]] 0.91 real-robot reward); B2 verifies and recovers at *runtime* ([[2605.22446|Pre-VLA]] truncates unreliable dreams); A2's imagined-vs-measured wrench loss is a train-time forecast the same machinery can score. The coupling is quantitative: B3's calibration raises the imagined-vs-real $\rho$ that B2 uses as its stop condition, so investing in B3 shrinks B2's recovery work, and A2's force imagination is one more channel calibration must keep honest.

> [!tip] Train Density and Deploy Density Are Two Independent Knobs the Field Treats as One
> A1, A3, and B4 all separate a quantity the field bundles. A1 separates *train density* from *deploy density* — dense pixel/3DGS supervision yet a cheap latent rollout, [[2605.20752|GaussianDream]]'s heads dropped at inference. A3 separates the *encoder objective* from the latent-vs-pixel question — semantic / continuous over reconstruction, [[2605.06388|Semantic-LDM-WM]]'s +9.8 pp swing at fixed architecture. B4 separates the *output's durability* from its in-episode use — the same imagination that rolls out once becomes a reusable training corpus, [[2606.02577|RoboDream]]'s Gen-Mix 62.5% vs 36.3%. The common error each corrects is treating one WAM design decision as a single binary when it is two orthogonal axes.

> [!tip] Efficiency Is a Deployment Prerequisite That Couples to Every Direction Here
> No direction owns efficiency, yet A1 and B2 both need real-time budgets to be feasible at all — the 3–5 Hz AR ceiling and 4.8× WAM latency cost are the anchors ([[2604.16484|DexWorldModel]]'s O(1) memory + async inference shows the levers are co-designable; full real-time co-design lives in the umbrella). A1's train-dense/deploy-light hybrid is itself an efficiency move, and B2's evolution cycle is infeasible if each imagined rollout is too slow to iterate, so a method that ignores the latency budget cannot be deployed whatever its SR. [[2606.05254|Flash-WAM]]'s 23× distillation and [[2605.28816|Gamma-World]]'s linear-scaling streaming are the levers A1 and B4 both draw on.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| Hybrid latent+pixel/3DGS vs pure-latent vs pure-pixel WAM at matched FLOPs (OOD × latency, at matched real SR) | A1 | [[2605.20752\|GaussianDream]] (train-dense/deploy-light, single point on the plane) + [[2603.22078\|WAM vs VLA Robustness]] (4.8× latency cost, no hybrid) |
| WAM with a tactile/force *prediction* head (imagined wrench, not consumed force) | A2 | [[2506.14754\|Sparsh-X]] (touch encoder, no prediction head) + [[2604.20444\|VTouch++]] (synchronized dataset, no WAM consumer) |
| Encoding-quality ablation at matched architecture: semantic / continuous vs reconstruction / VQ, scored by closed-loop SR + OOD | A3 | [[2605.06388\|Semantic-LDM-WM]] (reconstruction-vs-semantic, single backbone) + [[2605.15725\|DiLA]] (continuous-vs-VQ/VAE, scored on SSIM/LPIPS not closed-loop SR) |
| Discrete contact-mode latent; sub-millimeter assembly SR with contact-aware imagination | B1 | [[2604.16484\|DexWorldModel]] (causal latent but continuous contact) + [[2604.27367\|DOT-Sim]] (contact ground truth, no WAM consumer) |
| Integrated detection→diagnosis→recovery loop with WAM-driven imagination + rollout verification | B2 | [[2605.22446\|Pre-VLA]] (verifier only, no full loop) + [[2603.08403\|SPIRAL]] (imagine→verify→GRPO for generation, not detect→recover) |
| Forward-inverse calibration as a *training* signal (not a runtime filter) tied to imagined-vs-real $\rho$ | B3 | [[2604.01985\|WAV]] (asymmetry cycle, not $\rho$-objective) + [[2504.16680\|RWM-U]] (uncertainty gating, locomotion only) |
| Physics-validated WAM data engine with the validation filter ablated against downstream SR | B4 | [[2606.02577\|RoboDream]] (compositional synthesis, no physics-validation filter) + [[2606.04708\|VISTA]] (physics-validated UMI adaptation, not a generative engine) |

---

## Cross-References

- [[../../../Embodied-AI/07_WAM|07_WAM]] — WAM taxonomy (VideoGen / latent / Dreamer / VLM-integrated / efficient / self-evolving)
- [[../../../Embodied-AI/08_Latent-World-Models|08_Latent-World-Models]] — JEPA + alternative latent models; latent reasoning
- [[../../../Embodied-AI/13_Self-Evolving-VLA-WAM|13_Self-Evolving-VLA-WAM]] — Failure detection, diagnosis, recovery; self-evolution mechanisms
- [[../../../Embodied-AI/11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] — Physics-aware design space; physics commonsense benchmarks
- [[../../../Embodied-AI/14_Sim-to-Real-Transfer|14_Sim-to-Real-Transfer]] — Sim-to-real strategies; learned simulators; reality-gap diagnostics
- [[../../../General/08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — Canonical survey index
- [[Embodied-AI|Embodied-AI]] — Umbrella directions. Joint WAM–policy co-evolution, physics-consistency verification, joint causal-consistency evaluation, real-time deployment, and cross-embodiment transfer live there — omitted here to avoid duplication.
- [[Spatial-4D|Spatial-4D]] — Sibling doc on the model-agnostic 3D/4D representation: natively-4D imagination and persistent geometric memory, framed as representations any policy reuses.
- [[Sim2Real|Sim2Real]] — Sibling doc on sim-to-real / real-to-sim transfer; borders this doc's physics-grounding (Cluster B) and world-model-as-simulator themes.
