---
title: "Promising Research Directions: 3D/4D Spatial & Geometric Representation"
aliases:
  - "Spatial-4D"
  - "3D/4D Geometric Representation Directions"
tags:
  - research-directions
  - embodied-AI
  - 3D-understanding
  - spatial-reasoning
---

# Promising Research Directions: 3D/4D Spatial & Geometric Representation

> [!abstract] Overview
> Ten research directions across four clusters, drawn from the vault's 3D/4D-spatial corpus. The axis is **Mechanism**: the geometric *representation* that policies, reasoners, and world models stand on, independent of which robot uses it. The one idea behind all ten: **geometry is what the task keeps fixed; appearance is the noise on top.** Cluster A puts explicit 3D *inside the action head* — point-cloud policies, occupancy forward models, depth-token add-ons. Cluster B reasons over 3D geometry *before* acting — scene-graph CoT, 4D-consistent policies. Cluster C builds *world models and memory out of geometry instead of pixels*: externally-readable occupancy (C1) and 4D-video pointmaps (C2), a latent-4D imagination substrate (C3), and a persistent geometric memory for long-horizon coherence (C4) — each usable by any policy or model. Cluster D builds reconstruction assets you can *act in*, not just look at. Every direction names its first principle, the assumption it breaks, and a falsifiable bet pinned to a number from the vault.

## Methodology

**Scope.** Corpus = the vault's 3D/4D-spatial and geometric-representation papers in `_KnowledgeHub_/`, read in full. No date filter — 2024 (Video2Game) through 2026-Q2 (PointAction, OccSim, CausalSpatial). **What this doc owns.** Spatial-4D owns the *model-agnostic 3D/4D representation* — a geometric state any policy or model can stand on. Sibling [[WAM|WAM]] owns *WAM machinery only* (latent backbone, training, grounding); [[Sim2Real|Sim2Real]] owns the *reality gap*. So the latent-4D substrate ([[2604.26694|X-WAM]]) and persistent geometric memory ([[2603.17117|MosaicMem]], [[2603.24576|Chameleon (Episodic Memory)]]) live **here as C3 and C4** — treated as *representations*, not "world models," even though their source papers are world-model papers. **Out of scope:** the sim-to-real *transfer-gap* side of 3DGS reconstruction (that's [[Sim2Real|Sim2Real]]-A1/B1: [[2604.25459|GS-Playground]], [[2511.04665|Real-to-Sim GS]]); where a card borders it, one clause states the delta. The `_Projects_/01_FirstPublication/` subtree is not cross-linked.

- **Surveys** — anchored on three structural surveys: [[2604.26509|3D Generation for Embodied AI Survey]] (simulation-readiness), [[2506.20134|3D World Models Survey]] (2D → 3D transition), [[2504.05786|3D Spatial Reasoning in LLM Survey]] (the cognition-layer gap).
- **Deep-dives** — cross-read against [[../Embodied-AI/08_Latent-World-Models|08_Latent-World-Models]], [[../Embodied-AI/11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]], [[../Embodied-AI/06_VLA-Reasoning-and-CoT|06_VLA-Reasoning-and-CoT]], [[../Embodied-AI/02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]].
- **Filter** — every cited paper has a KH note; every number in a Thesis bet or Key-targets row traces to that note. No fabricated aliases or placeholder numbers.
- **Framing** — each direction names its first principle, the assumption it breaks (who believes what), and a falsifiable bet with a number. Directions are picked for where geometry departs from the RGB-token consensus, not for incremental tweaks to it.

## 3D/4D Spatial Survey Landscape

| Survey | Sub-theme | Key open problems |
|---|---|---|
| [[2506.20134\|3D World Models Survey]] | A — Geometry-native policies | Field is mid-transition "from 2D visual perception to comprehensive 3D spatial cognition"; explicit-3D action interfaces remain rare and embodiment-specific |
| [[2604.22748\|Agentic World Modeling Survey]] | A — Geometry-native policies | The L2 Simulator must "compose multi-step rollouts that respect domain laws" — but forward models that are geometric rather than pixel-based are underbuilt for manipulation |
| [[2504.05786\|3D Spatial Reasoning in LLM Survey]] | B — 3D-grounded cognition | MLLM spatial reasoning is "ungrounded": coordinate-metric reasoning lags object-naming; no consensus interface between language reasoning and metric 3D |
| [[2510.16732\|World Models for Embodied AI Survey]] | C — Geometry-native world models | Spatial-representation axis is evolving latent → token → explicit 3D; explicit-geometry world models are nascent and rarely externally renderable |
| [[2604.26509\|3D Generation for Embodied AI Survey]] | D — Reconstruction for embodied perception | "Simulation-readiness over visual fidelity" is the bottleneck; scarcity of physical annotations; trade-off between geometric quality and physical validity; deformable assets unsolved |

> [!tip] Convergence patterns
> The same gap shows up across the five surveys under different names:
> - **The RGB-token tax** — [[2506.20134|3D World Models Survey]], [[2510.16732|World Models for Embodied AI Survey]], and [[2604.22748|Agentic World Modeling Survey]] all find that policies and world models default to pixels, leaving *metric 3D motion, contact geometry, and spatial constraints implicit* — a supervision cost explicit geometry would erase. A1, A2, A3, C1, C2 attack this at different layers.
> - **The grounding gap is metric, not semantic** — [[2504.05786|3D Spatial Reasoning in LLM Survey]], [[2506.20134|3D World Models Survey]], and [[2604.22748|Agentic World Modeling Survey]] agree the failure isn't *naming* objects but *placing* them in 3D and *predicting how they move*. B1, B2 target this.
> - **Readiness beats fidelity** — [[2604.26509|3D Generation for Embodied AI Survey]], [[2510.16732|World Models for Embodied AI Survey]], and [[2506.20134|3D World Models Survey]] note the field optimizes *appearance* (PSNR/FID) when the real bottleneck is *interaction readiness* — geometry that carries physics, articulation, and a usable export format. C1, C2, D1 invert this.

## Formal Framing

The central object is an **explicit geometric state** $G_t$ — a representation of scene structure that is *metric* and *externally interpretable*, as opposed to an appearance latent $z_t$ that is only decodable to pixels. The cluster split is a statement about *where $G_t$ lives in the stack*.

| Object | Definition | Owning cluster |
|---|---|---|
| Point-cloud / pointmap policy | $a_t = \pi(G_t, l)$ with $G_t \in \mathbb{R}^{N\times 3}$ (XYZ, optionally + mask) the explicit action-conditioning state | A |
| Occupancy forward model | $\hat{O}_{t+1} = f(O_t, a_t)$ over a voxel-semantic grid $O \in \{0,1,\dots,K\}^{H\times W\times D}$ | A (forward model), C (rollout substrate) |
| Spatial-cognition layer | a scene-graph / coordinate state $S$ s.t. $a_t = \pi(\text{reason}(S))$ — reasoning is *over* metric geometry, upstream of the action head | B |
| Renderable geometry WM | $G_t$ = explicit 4D (pointmap sequence / occupancy) that an *external* renderer or tracker can consume to recover 6-DoF pose | C |
| Interaction-ready asset | a reconstructed scene carrying geometry **+** physics parameters **+** kinematic structure (URDF/MJCF-exportable), not just radiance | D |

> [[2604.26509|3D Generation for Embodied AI Survey]] defines the readiness criterion this doc adopts as the line between C/D and pure rendering:
> "simulation readiness as a primary evaluation criterion: geometric validity, physical parameterization, kinematic executability, and simulator format compatibility (URDF, MJCF)."

Cluster C spans the full **decodability axis** of $G_t$ as an internal organizing principle: C1 (occupancy) and C2 (4D-video pointmaps) keep $G_t$ *explicit and externally-readable* — a third-party tracker or renderer reads it; C3 ([[2604.26694|X-WAM]]) keeps $G_t$ as a *latent-4D* state decoded inside the model for imagination; C4 ([[2603.17117|MosaicMem]], [[2603.24576|Chameleon (Episodic Memory)]]) makes $G_t$ *persist* as geometric memory across long horizons. All four are the same explicit-geometry commitment at different points on the explicit-external ↔ latent-internal ↔ persistent line. The split from [[WAM|WAM]] is about *ownership*, not decodability: Spatial-4D owns these *representations* model-agnostically; WAM owns the WAM *machinery* (latent backbone, training, grounding). The split from [[Sim2Real|Sim2Real]] is about *purpose*: Sim2Real shrinks the transfer gap given an asset; Cluster D makes the asset interaction-ready in the first place.

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Geometry-Native Policies** | A1, A2, A3 | The action head reads/predicts RGB tokens, leaving metric 3D implicit and paying a data tax | A1's point-cloud state is the input A2's occupancy forward model rolls forward; A3's depth-token add-on is the *cheap* version of A1's full 3D branch — together they span the cost/benefit frontier |
| **B — 3D-Grounded Cognition** | B1, B2 | Reasoning isn't grounded in metric geometry: language CoT over RGB hallucinates spatial relations and dynamics | B1's scene-graph is the spatial half; B2's 4D-consistency is the temporal half; both supply the upstream geometry A's action heads consume |
| **C — Geometry-Native World Models & Memory** | C1, C2, C3, C4 | World models imagine in pixels; geometry is recovered after the fact, isn't externally usable, isn't natively 4D, and isn't kept over long horizons | Organizing axis: **explicit-external ↔ latent-internal ↔ persistent**. C1 (occupancy) and C2 (4D-video pointmaps) are external — a renderer/tracker reads them. C3 is latent — 4D imagination decoded inside the model. C4 is memory — pinning C1/C2/C3's geometry to a world-frame so it survives minute-scale horizons |
| **D — Reconstruction for Embodied Perception** | D1 | Reconstruction optimizes radiance, not interaction-readiness; assets aren't physics- or kinematics-ready | D1 supplies the geometry the others consume — readable geometry for C's world models, point-cloud assets for A's policies |

## Cluster A — Geometry-Native Policies

*The action head consumes or predicts explicit 3D — the policy's conditioning state is metric geometry, not RGB tokens.*

### A1 — Point-Cloud-Native Action Heads vs RGB-Token Policies

| | |
|---|---|
| **Cluster** | A — Geometry-Native Policies |
| **Thesis** | An action is a function of *where things are in metric 3D* — and a point cloud says that directly, while an RGB token leaves it implicit. The policy field skips explicit 3D because it assumes a 2D-pretrained backbone already encodes the geometry it needs. That assumption breaks under appearance shift, where geometry stays fixed but pixels move. The bet: a point-cloud-native head beats RGB-token policies on cross-embodiment zero-shot transfer ([[2606.03943\|PointAction]] 43.0% zero-shot xArm7, 47.7% RoboCasa365 ID; [[2508.09071\|GeoVLA]] 97.7% LIBERO). |
| **Anchor surveys** | [[2506.20134\|3D World Models Survey]], [[2510.16732\|World Models for Embodied AI Survey]], [[2604.22748\|Agentic World Modeling Survey]] |
| **Key targets** | Cross-embodiment zero-shot SR ≥43.0% ([[2606.03943\|PointAction]] xArm7); ID SR ≥47.7% RoboCasa365; LIBERO ≥97.7% ([[2508.09071\|GeoVLA]]); RLBench ≥82.3% ([[2605.21414\|PointACT]]) |

**Why it matters.** The dominant recipe ([[2501.15830|SpatialVLA]], OpenVLA-class) feeds the action head RGB tokens from a 2D backbone and hopes the geometry needed for contact-precise control falls out of the semantic features. [[2606.03943|PointAction]] names the cost: RGB representations "leave metric 3D motion, contact geometry, and fine-grained spatial constraints implicit," forcing the policy to learn grounding from "expensive, embodiment-specific, non-scalable paired observation-action data." [[2508.09071|GeoVLA]] adds the robustness angle: 2D reliance gives "poor depth perception" and breaks under object-height, scale, and viewpoint shift. The fix is to make the conditioning state geometric. [[2606.03943|PointAction]] splits into an embodiment-agnostic video-to-point model + a small point-to-action decoder, hitting 43.0% zero-shot on an xArm7 it never trained on. [[2508.09071|GeoVLA]] runs a 3D point branch beside a frozen VLM for 97.7% LIBERO with spatial-shift robustness. [[2605.21414|PointACT]] adds multi-scale point-action coupling for 82.3% RLBench. The non-consensus claim: a point-cloud head should win exactly where RGB heads are weakest — under appearance shift across embodiments and viewpoints.

**First-principles framing.**
- **First principle**: A manipulation action is set by the metric 3D layout (where gripper, object, and contacts are), not by 2D appearance. Geometry is fixed under lighting, texture, viewpoint, and camera placement; appearance is not.
- **Assumption being challenged**: The OpenVLA / [[2501.15830|SpatialVLA]] view that a big 2D backbone already encodes whatever geometry the head needs, so an explicit 3D branch is wasted overhead. [[2508.09071|GeoVLA]] and [[2606.03943|PointAction]] show it breaks under the shifts (height, scale, viewpoint, embodiment) where geometry holds but pixels move.
- **The bet**: A point-cloud head transfers zero-shot across embodiments at ≥43.0% SR ([[2606.03943|PointAction]] xArm7) where RGB policies collapse, and the geometry-vs-RGB gap *widens* with shift magnitude — measurable as ID→OOD SR retention beating the RGB baseline on the same shift.

**Evidence.**
- [[2606.03943|PointAction]] — Dynamic 3D pointmaps as an embodiment-agnostic interface; 47.7% RoboCasa365 ID, 43.0% zero-shot xArm7 (2–2.5x over baselines); the canonical point-native cross-embodiment result.
- [[2508.09071|GeoVLA]] — Frozen VLM + Point Embedding Network + 3D MoE action expert; 97.7% LIBERO, 77% ManiSkill2, robust to height/scale/viewpoint shift.
- [[2605.21414|PointACT]] — Multi-scale point-action coupling; 96.0% LIBERO, 82.3% RLBench; fine-grained coupling beats coarse 3D-feature injection.
- [[2403.03954|DP3]] — 3D Diffusion Policy; compact point conditioning — evidence that sparse 3D points are enough to drive a precise policy.
- [[2403.09631|3D-VLA]] — Early 3D-grounded policy; the architectural template the anchors refine.

**Concrete research questions.**
1. **Q1 — Geometry-invariance ablation.** Hold the backbone fixed; compare a point-cloud head against an RGB-token head under a controlled appearance-shift sweep (texture, lighting, camera pose). Does the SR gap grow monotonically with shift magnitude, as the first principle predicts?
2. **Q2 — Where does the point state pay off?** Decompose SR by task phase (transit vs contact). Is the point-native advantage concentrated in contact-rich sub-segments where geometry determines the action, near-zero in free-space transit?
3. **Q3 — Minimal sufficient geometry.** [[2403.03954|DP3]] uses sparse points; [[2508.09071|GeoVLA]] uses a full point branch. What is the minimal point density / completeness that recovers most of the SR gain — i.e., the cheapest explicit geometry that still beats RGB?
4. **Q4 — Embodiment-agnostic pretraining transfer.** [[2606.03943|PointAction]] pretrains the video-to-point model embodiment-free. Quantify how much of the zero-shot xArm7 SR is attributable to the *point representation* vs the *factorized decoder* via a representation-swap control.

**Related research papers.**
- [[2606.03943|PointAction]] — Pointmap-as-action-interface; attacks the RGB supervision bottleneck directly.
- [[2508.09071|GeoVLA]] — Parallel 2D+3D paths keep VLM priors while adding geometry; the 2D-brittleness fix.
- [[2605.21414|PointACT]] — Multi-scale point-action coupling; fixes weak geometry-action binding.
- [[2403.03954|DP3]] — Sparse-point diffusion policy; the "is full 3D necessary" cost question.
- [[2403.09631|3D-VLA]] — 3D-grounded generative policy; the missing-3D-layer template.
- [[2501.15830|SpatialVLA]] — RGB-token spatial policy; the consensus baseline this inverts.
- [[2505.05800|3D-CAVLA]] — 3D context-aware policy; scene-level 3D conditioning.
- [[2602.10098|VLA-JEPA]] — Latent-JEPA policy, 97.2% LIBERO; the strong *latent* counterpoint A1 must beat on geometry-bound tasks.

**Benchmarks & metrics.**
- [[2306.03310|LIBERO]] — 4-suite manipulation benchmark; [[2508.09071|GeoVLA]] 97.7%, [[2605.21414|PointACT]] 96.0%; the standard ID manipulation bar.
- [[2406.02523|RoboCasa]] — Kitchen-scale manipulation; [[2606.03943|PointAction]] 47.7% ID on RoboCasa365 + 17.0% on 5 unseen tasks; the generalization-stress suite.
- [[2107.14483|ManiSkill]] / [[2410.00425|ManiSkill3]] — Contact-rich manipulation; [[2508.09071|GeoVLA]] 77% ManiSkill2; the cross-suite geometry check.

> [!warning] Risks
> - **Point clouds need depth sensing or reconstruction** that may be noisy or unavailable at deploy. → Mitigation: lean on the predicted-pointmap path ([[2606.03943|PointAction]]) so geometry is *generated*, not sensed, removing the hard depth-sensor dependency.
> - **The advantage may vanish on in-distribution benchmarks** where RGB backbones already saturate (LIBERO ~97%). → Mitigation: design the evaluation around appearance-shift / cross-embodiment splits where the first principle predicts the gap appears; treat ID parity as expected, not as failure.
> - **Full 3D branches add latency and parameters.** → Mitigation: Q3's minimal-sufficient-geometry sweep + A3's depth-token bridge as the lightweight fallback if full point branches don't pay their compute.

### A2 — Occupancy-Forecasting as the Policy's Forward Model

| | |
|---|---|
| **Cluster** | A — Geometry-Native Policies |
| **Thesis** | Planning needs to know *what space will be filled*, not *what the scene will look like* — a voxel grid answers that directly, while pixels make you re-infer geometry every step. The field defaults to pixel forward models because that's what video foundation models predict; occupancy world models matured in driving and were never ported to tabletop. The bet: an occupancy forward model ported to manipulation inherits the long-horizon stability [[2603.28887\|OccSim]] showed in driving (3,000+ stable frames, +22.1% relative mIoU over asset-based CARLA, 67% zero-shot) where pixel models drift within tens of frames. |
| **Anchor surveys** | [[2604.22748\|Agentic World Modeling Survey]], [[2510.16732\|World Models for Embodied AI Survey]], [[2506.20134\|3D World Models Survey]] |
| **Key targets** | Stable rollout ≥3,000 frames / ≥4 km ([[2603.28887\|OccSim]]); +22.1% relative mIoU vs asset-based sim; 67% zero-shot; manipulation port: beat a pixel-world-model baseline on geometry-bound RoboCasa tasks |

**Why it matters.** Model-based control needs a forward model, and the default is a pixel-space video predictor the policy must re-parse into geometry every step — so drift piles up fast (pixel/occupancy WMs in driving were "limited to fewer than 50 frames," per [[2603.28887|OccSim]]). [[2603.28887|OccSim]] forecasts *occupancy* — an explicit voxel-semantic grid — with a Warp-DiT block that bounds geometric error via 3D rigid transforms, sustaining 3,000+ stable frames over 4+ km (80x the prior ceiling), and the data it makes lifts downstream forecasting +22.1% relative mIoU over an asset-based CARLA baseline (67% zero-shot). The catch: that's a driving result. The contribution here is to *port the occupancy loop into the manipulation forward model* — swap the pixel inner loop for an occupancy loop, so the policy plans against "what space the object and gripper will fill" instead of "what the next frame looks like." Medawar-zone framing: not "build a perfect world model," but "transplant a representation that already solved long-horizon stability in one domain into the adjacent domain where the planning question is identical." A2 and C1 both build on [[2603.28887|OccSim]] at different points in the stack: **A2 puts occupancy *inside the policy's forward-model loop*** (baseline pixel-WM, payoff downstream SR); **C1 is occupancy as a *standalone WM substrate*** (baseline latent [[2604.26694|X-WAM]], payoff horizon-to-divergence) — complementary, not a duplicate.

**First-principles framing.**
- **First principle**: A planner needs to know which regions of space will be occupied (collision-freedom, contact, reachability) — a voxel grid answers that directly. Pixels are a lossy, view-dependent re-encoding of the same geometry; occupancy is the planning-native state.
- **Assumption being challenged**: That a manipulation forward model should predict pixels (the [[2510.10125|CTRL-WORLD]]/video-WM convention) because that's what video foundation models predict. [[2603.28887|OccSim]]'s 80x horizon gain shows the pixel substrate is itself the *source* of the drift the field treats as inherent.
- **The bet**: An occupancy forward model in the manipulation loop holds geometric stability an order of magnitude longer than a pixel-WM baseline on the same tasks, and the downstream SR gain tracks [[2603.28887|OccSim]]'s +22.1% relative mIoU lift — the stability transfer is real, not driving-specific.

**Evidence.**
- [[2603.28887|OccSim]] — Occupancy WM with Warp-DiT; 3,000+ stable frames, 4+ km, +22.1% rel mIoU, 67% zero-shot; the proof that geometry-grid forecasting breaks the horizon ceiling.
- [[2604.22748|Agentic World Modeling Survey]] — The L2 Simulator must "compose multi-step rollouts that respect domain laws" — the stability occupancy supplies.
- [[2510.16732|World Models for Embodied AI Survey]] — latent→token→explicit-3D trajectory; occupancy is the explicit end of the forward-model spectrum.
- [[2510.10125|CTRL-WORLD]] — Controllable *video* WM (38.7→83.4% on unseen objects); the pixel forward model this replaces with occupancy.
- [[2506.20134|3D World Models Survey]] — the 2D→3D transition that makes occupancy a natural manipulation substrate.

**Concrete research questions.**
1. **Q1 — Occupancy vs pixel inner loop.** Swap a manipulation world model's pixel-prediction loop for an occupancy-prediction loop with the backbone fixed. Measure rollout-horizon-to-divergence and downstream SR. Does the 80× driving horizon gain partially transfer to tabletop scale?
2. **Q2 — Voxel resolution vs planning fidelity.** What occupancy resolution is needed for contact-precise manipulation (sub-cm) vs driving (meter-scale)? Is the Warp-DiT error-bounding mechanism resolution-portable?
3. **Q3 — Dynamic-agent analog.** [[2603.28887|OccSim]] decouples static-scene rollout from dynamic-agent generation. In manipulation the "dynamic agent" is the manipulated object + gripper — does the same decoupling stabilize object-motion forecasting?
4. **Q4 — Occupancy as the A1 input.** A1's point-cloud head and A2's occupancy forward model share the explicit-geometry commitment. Can A2's predicted future-occupancy condition A1's action head directly — closing a fully-geometric perceive-imagine-act loop?

**Related research papers.**
- [[2603.28887|OccSim]] — Occupancy WM for long-horizon driving sim; the representation this ports to manipulation.
- [[2510.10125|CTRL-WORLD]] — Controllable video WM; the pixel baseline to beat on horizon stability.
- [[2604.22748|Agentic World Modeling Survey]] — Multi-step domain-law rollout requirement; motivates the geometric forward model.
- [[2510.16732|World Models for Embodied AI Survey]] — where occupancy sits in the substrate spectrum.
- [[2506.20134|3D World Models Survey]] — why pixel forward models are a legacy choice.
- [[2604.16484|DexWorldModel]] — O(1)-memory dexterous WM; the efficiency budget the occupancy loop must respect.
- [[2504.20995|TesserAct]] — 4D RGB-D-N WM; the depth-augmented midpoint between pixel and full occupancy.
- [[2604.26694|X-WAM]] — Unified 4D WAM (latent); the *latent-4D* neighbor (sibling C3) — A2's delta is explicit occupancy the planner reads directly vs X-WAM's internal latent.

**Benchmarks & metrics.**
- [[2603.28887|OccSim]]'s own protocol — stable-generation-length (frames / km) + downstream-mIoU lift; +22.1% rel mIoU, 67% zero-shot; the long-horizon-stability metric this direction inherits.
- [[2406.02523|RoboCasa]] — The proposed manipulation target suite for the occupancy-loop port; geometry-bound long-horizon kitchen tasks where pixel WMs drift.
- [[2410.00425|ManiSkill3]] — Contact-rich manipulation with GPU sim; the contact-precision stress test for sub-cm occupancy resolution.

> [!warning] Risks
> - **Cross-domain transfer may not hold** — driving occupancy is meter-scale and mostly-static; manipulation needs sub-cm dynamic occupancy. → Mitigation: Q2's resolution sweep + Q3's dynamic-agent analog are the explicit go/no-go before claiming transfer; report the scale at which the Warp-DiT error bound breaks.
> - **Occupancy ground truth is scarce in manipulation datasets.** → Mitigation: derive occupancy from depth + known gripper geometry (as driving derives it from LiDAR), or pretrain the forecaster in sim where occupancy is free.
> - **Voxel grids are memory-heavy at sub-cm resolution.** → Mitigation: sparse/hierarchical occupancy (octree) + bound the claim to the working-volume around the end-effector rather than the full scene.

### A3 — Depth-Token Bridges: 3D-Awareness into Pretrained 2D Policies Without Re-Training

| | |
|---|---|
| **Cluster** | A — Geometry-Native Policies |
| **Thesis** | A 2D policy's geometry deficit is a *missing channel*, not a *wrong backbone* — so a cheap depth-token side-input can supply it without disturbing the pretrained semantic alignment. The field assumes 3D-awareness needs a full parallel 3D branch and re-training, forcing a false choice between RGB-only (cheap, geometry-blind) and full-3D (capable, expensive). The bet: a single-view depth-token bridge recovers most of a full-3D branch's spatial gain at a fraction of the cost ([[2510.14836\|QDepth-VLA]] +8.8% LIBERO-Spatial, +29.7% long-horizon over open_pi_0, single-view; vs [[2508.09071\|GeoVLA]]'s full 3D branch 97.7%). |
| **Anchor surveys** | [[2504.05786\|3D Spatial Reasoning in LLM Survey]], [[2506.20134\|3D World Models Survey]], [[2510.16732\|World Models for Embodied AI Survey]] |
| **Key targets** | +8.8% LIBERO-Spatial, +29.7% long-horizon over open_pi_0, +10–20% real-robot ([[2510.14836\|QDepth-VLA]], single-view); recover ≥80% of [[2508.09071\|GeoVLA]]'s full-3D-branch gain (97.7% LIBERO) at side-channel cost |

**Why it matters.** A1 and A2 buy geometry by changing the architecture — a parallel point branch or an occupancy loop. That's right when geometry is central, but it strands the huge installed base of RGB-pretrained policies that already work and that nobody wants to re-train. [[2510.14836|QDepth-VLA]] asks the cheaper question: can you give a frozen 2D policy just enough 3D-awareness through a *side channel*? Its answer — depth as discrete VQ-VAE tokens (less noisy than pixel-wise regression), fed to a depth-expert that reads the VLM's vision features without touching semantic alignment, integrated via hybrid attention — gives +8.8% LIBERO-Spatial, +29.7% long-horizon over `open_pi_0`, and +10–20% on a real robot, *from single-view input only*. The contrast with [[2508.09071|GeoVLA]]'s full 3D branch (97.7% LIBERO) is exactly the cost/benefit question this direction measures: how much of the full-branch capability survives in the bolt-on version? The Hinton-taste read: biology layers depth on as an early, cheap channel, not a separate stream re-learned from scratch — the bolt-on bridge is the biologically-natural form, and the deployable one.

**First-principles framing.**
- **First principle**: A 2D policy's spatial weakness is a *missing channel* (depth), not a corrupted representation. Adding the channel as discrete tokens through a decoupled expert supplies the metric cues — you don't need to rebuild the backbone to add a channel.
- **Assumption being challenged**: The [[2508.09071|GeoVLA]] / [[2606.03943|PointAction]] position that real 3D-awareness needs a full parallel 3D branch and joint re-training. [[2510.14836|QDepth-VLA]] shows a *frozen-backbone* depth-token task captures much of the gain while keeping the semantic alignment full-branch fusion risks disturbing — so the cheap/expensive split is false.
- **The bet**: A single-view depth-token bridge recovers ≥80% of a full-3D branch's spatial-task SR gain (same RGB-only baseline) at a fraction of the added parameters and zero re-training — and does it from *single-view* input where full-3D methods need multi-view or sensed point clouds.

**Evidence.**
- [[2510.14836|QDepth-VLA]] — Quantized depth tokens + decoupled depth expert + hybrid attention; +8.8% LIBERO-Spatial, +29.7% long-horizon, +10–20% real, single-view; the canonical cheap-bridge result.
- [[2508.09071|GeoVLA]] — Full 3D point branch; 97.7% LIBERO; the *expensive* upper bound this measures against.
- [[2504.20995|TesserAct]] — 4D RGB-D-N WM; depth as a predicted channel sharpens grounding without abandoning the pixel backbone.
- [[2502.13143|SoFar]] — Orientation grounding from 2D; a lightweight side-signal sharpens manipulation without a full 3D stack.
- [[2501.15830|SpatialVLA]] — RGB-token spatial policy; the frozen-backbone host the depth bridge bolts onto.

**Concrete research questions.**
1. **Q1 — Recovery-fraction curve.** Sweep depth-token capacity (codebook size, expert depth) and plot the fraction of [[2508.09071|GeoVLA]]'s full-3D-branch SR gain recovered vs added parameters. Where is the knee?
2. **Q2 — Quantized vs continuous depth.** [[2510.14836|QDepth-VLA]] argues discrete tokens beat pixel-wise regression on noise-robustness. Isolate the contribution of *quantization* vs the contribution of the *decoupled expert* via a 2×2 ablation.
3. **Q3 — Single-view vs multi-view depth bridge.** Does the single-view depth-token gain saturate, or does adding a second view's depth tokens close the remaining gap to full-3D methods that consume sensed point clouds?
4. **Q4 — Alignment preservation.** Quantify how much the depth-expert side-channel perturbs the frozen VLM's semantic-alignment (e.g., on a held-out VQA probe) vs full-branch fusion that backprops into the backbone.

**Related research papers.**
- [[2510.14836|QDepth-VLA]] — Quantized-depth bridge; attacks the cost of full-3D branches directly.
- [[2508.09071|GeoVLA]] — Full 3D branch; the capability upper bound and the alignment-disruption risk the bridge avoids.
- [[2504.20995|TesserAct]] — RGB-D-N 4D prediction; depth-as-predicted-channel side signal.
- [[2502.13143|SoFar]] — Orientation grounding; lightweight spatial augmentation.
- [[2501.15830|SpatialVLA]] — RGB-token spatial policy; the bolt-on host backbone.
- [[2605.21414|PointACT]] — Multi-scale point-action coupling; the full-3D contrast on action-coupling.
- [[2606.03943|PointAction]] — Predicted-pointmap interface; the generated-geometry alternative to sensed depth.
- [[2602.10098|VLA-JEPA]] — Latent-JEPA policy, 97.2% LIBERO; the implicit-geometry-in-latent alternative the bridge competes with on cost.

**Benchmarks & metrics.**
- [[2306.03310|LIBERO]] (Spatial suite) — [[2510.14836|QDepth-VLA]] +8.8% over open_pi_0 on Spatial; the depth-sensitive split where the bridge should pay off most.
- [[2306.03310|LIBERO]] (Long-horizon / 10) — [[2510.14836|QDepth-VLA]] +29.7% over open_pi_0; long-horizon tasks stress geometric memory the bridge supplies.
- Real-robot pick-and-place — [[2510.14836|QDepth-VLA]] +10–20% over open_pi_0 under challenging conditions; the deployability check that the cheap bridge transfers to hardware.

> [!warning] Risks
> - **The bridge may plateau below the full-3D ceiling** on the hardest geometry-bound tasks. → Mitigation: Q1's recovery-fraction curve sets an honest expectation — frame the contribution as *cost-efficiency frontier*, not SR-SOTA; concede the ceiling where it appears.
> - **Depth-token quality depends on the depth estimator.** → Mitigation: [[2510.14836|QDepth-VLA]]'s quantization buffers estimator noise; report sensitivity to estimator quality so the claim is bounded to realistic depth.
> - **Side-channel may still subtly perturb semantic alignment.** → Mitigation: Q4's VQA-probe quantifies the perturbation; gate the "non-disruptive" claim on it rather than assuming the frozen backbone is untouched.

## Cluster B — Spatial Reasoning as a 3D-Grounded Cognition Layer

*Reasoning happens over explicit metric geometry, upstream of the action head — the policy acts on the output of a 3D-grounded cognition step, not on raw RGB.*

### B1 — Explicit 3D Scene-Graph CoT for Metric Spatial Reasoning

| | |
|---|---|
| **Cluster** | B — 3D-Grounded Cognition |
| **Thesis** | Metric spatial relations are a *graph over geometric entities*; free-form language CoT only describes that graph lossily and hallucinates when ungrounded. The MLLM field trusts language CoT over RGB and assumes scale alone closes the spatial gap. The bet: structured scene-graph CoT plus RL grounding closes a measurable slice of the human-model gap ([[2507.13362\|VLM Spatial Reasoning RL]] +5–15%, 77.69% CVBench; [[2501.10074\|SpatialCoT]] 82.57% manip / 61.83% nav), with the residual largest on causal tasks ([[2601.13304\|CausalSpatial]] GPT-5 54.17% vs human 84.49%). |
| **Anchor surveys** | [[2504.05786\|3D Spatial Reasoning in LLM Survey]], [[2506.20134\|3D World Models Survey]], [[2604.22748\|Agentic World Modeling Survey]] |
| **Key targets** | CVBench ≥77.69% ([[2507.13362\|VLM Spatial Reasoning RL]]); manip SR ≥82.57% / nav SR ≥61.83% ([[2501.10074\|SpatialCoT]]); close part of the [[2601.13304\|CausalSpatial]] 54.17%→84.49% human gap |

**Why it matters.** [[2504.05786|3D Spatial Reasoning in LLM Survey]] and [[2601.13304|CausalSpatial]] reach the same diagnosis: MLLMs don't reason about metric space, they *describe* it in language and hallucinate when ungrounded. [[2601.13304|CausalSpatial]] measures the cost — on causal tasks (collision, occlusion, trajectory anticipation) GPT-5 scores 54.17% vs human 84.49%, and models are overconfident (low Not-Sure-Rate, no accuracy gain). The fix is structure. [[2507.13362|VLM Spatial Reasoning RL]] shows *Scene Graph CoT* — decompose the scene into a relational graph before answering — gives 5–15% (77.69% CVBench), and GRPO RL generalizes OOD where SFT degrades (+19.5% Depth-OOD). [[2501.10074|SpatialCoT]] pushes it into action: bidirectional coordinate alignment + CoT grounding yields precise coordinate actions (82.57% manip, 61.83% nav). The non-consensus claim against scale-is-all-you-need: the spatial gap is a *missing intermediate representation*, not a data deficit — make the scene-graph explicit and the reasoning becomes grounded. This is the cognition layer A's action heads consume.

**First-principles framing.**
- **First principle**: Spatial relations form a graph over geometric entities (objects with metric positions, pairwise relations, contacts). Reasoning correctly *is* operating on that graph; language is a lossy serialization that drops the metric structure the task needs.
- **Assumption being challenged**: The scaling view that a big-enough multimodal model reasons about space implicitly, so explicit structure is unneeded scaffolding. [[2507.13362|VLM Spatial Reasoning RL]] shows naive CoT can *hurt* and only *structured* scene-graph CoT helps; [[2601.13304|CausalSpatial]] shows even GPT-5 sits 30 points below humans — scale hasn't closed it.
- **The bet**: A scene-graph CoT layer with RL grounding closes a measurable fraction of the [[2601.13304|CausalSpatial]] gap (54.17%→84.49%) on the *causal* tasks where ungrounded language fails hardest, and the gain is largest where the scene-graph is most metric — not on object-naming, where RGB already suffices.

**Evidence.**
- [[2507.13362|VLM Spatial Reasoning RL]] — Scene-Graph CoT + GRPO; +5–15%, 77.69% CVBench, +19.5% Depth-OOD where SFT degrades; the canonical structured-beats-naive-CoT result.
- [[2501.10074|SpatialCoT]] — Bidirectional coordinate alignment + CoT grounding; 82.57% manip / 61.83% nav; ties scene-graph reasoning to coordinate actions (the B→A handoff).
- [[2601.13304|CausalSpatial]] — Causal-spatial benchmark + COW world model; GPT-5 54.17% vs human 84.49%; quantifies the gap, shows visual simulation suppresses hallucination.
- [[2504.20024|SpatialReasoner]] — Dedicated spatial-reasoning model; beats general MLLM prompting.
- [[2505.23747|Spatial-MLLM]] — 3D-structure-aware MLLM; injecting geometry into the reasoner improves spatial QA.

**Concrete research questions.**
1. **Q1 — Metric vs topological scene-graph.** Does the scene-graph need metric edge labels (distances, angles) or do topological relations (left-of, on-top-of) suffice? Decompose CVBench gains by relation type.
2. **Q2 — RL vs SFT for OOD grounding.** [[2507.13362|VLM Spatial Reasoning RL]] shows GRPO generalizes where SFT overfits. Replicate on causal tasks: does RL grounding transfer the scene-graph habit OOD better than SFT on [[2601.13304|CausalSpatial]]?
3. **Q3 — Where does the human gap live?** Decompose [[2601.13304|CausalSpatial]]'s 30-point gap by task (collision/occlusion/trajectory). Which causal task does scene-graph CoT close most, and is the residual a *reasoning* failure or a *perception* (depth/occlusion) failure?
4. **Q4 — Scene-graph CoT → action handoff.** [[2501.10074|SpatialCoT]] emits coordinates. Quantify how much of A1's point-cloud-head SR can be matched by feeding B1's scene-graph-reasoned coordinates into a simpler RGB action head — i.e., does upstream grounding substitute for downstream geometry?

**Related research papers.**
- [[2507.13362|VLM Spatial Reasoning RL]] — Scene-Graph CoT + GRPO; fixes naive-CoT hallucination with structure.
- [[2501.10074|SpatialCoT]] — Coordinate-aligned CoT; the language-to-coordinate handoff.
- [[2601.13304|CausalSpatial]] — Causal-spatial diagnostic + COW; the unmeasured causal-reasoning gap.
- [[2504.20024|SpatialReasoner]] — Dedicated spatial-reasoning model; general-MLLM spatial weakness.
- [[2505.23747|Spatial-MLLM]] — 3D-structure-aware MLLM; missing geometric structure in the reasoner.
- [[2505.20279|VLM-3R]] — 3D-reconstructive reasoning; grounding reasoning in reconstructed 3D.
- [[2506.04220|Struct2D]] — Structured 2D→spatial reasoning; cheap structure without full 3D.
- [[2504.05786|3D Spatial Reasoning in LLM Survey]] — Survey of the cognition-layer gap; frames the direction.

**Benchmarks & metrics.**
- [[2601.13304|CausalSpatial]] — Causal-spatial QA with Not-Sure-Rate; GPT-5 54.17% vs human 84.49%; the causal-reasoning gap this direction targets and the hallucination diagnostic.
- CVBench (via [[2507.13362|VLM Spatial Reasoning RL]]) — 77.69% with Scene-Graph CoT; +19.5% Depth-OOD; the structured-CoT and OOD-robustness bar.
- [[2501.10074|SpatialCoT]] simulated suite — 82.57% manip / 61.83% nav SR; the reasoning-to-action transfer metric.

> [!warning] Risks
> - **Scene-graph construction can itself hallucinate** — a wrong graph poisons downstream reasoning. → Mitigation: ground the graph in B2's 4D-consistency / depth ([[2601.13304|CausalSpatial]]'s COW visual-simulation evidence), and report graph-construction accuracy separately from answer accuracy.
> - **Gains may be benchmark-specific** (CVBench-tuned prompts don't transfer). → Mitigation: Q2's RL-OOD protocol tests cross-benchmark transfer explicitly; treat GRPO as the generalization mechanism, not prompt-tuning.
> - **The human gap may be perception-bound, not reasoning-bound** — scene-graph CoT can't fix bad depth. → Mitigation: Q3 separates perception from reasoning failure; if perception-bound, route to A3's depth bridge as the upstream fix.

### B2 — 4D-Consistent Policies: Spatio-Temporal Geometry as a Reasoning Constraint

| | |
|---|---|
| **Cluster** | B — 3D-Grounded Cognition |
| **Thesis** | For an action to be planned over a horizon, an object's geometry and identity must stay coherent across time and viewpoint — 4D consistency. The field forces a choice: stay 2D (cheap, inconsistent) or generate explicit future frames (expensive). The bet: *implicit* 4D-consistency attention matches explicit-3D accuracy at far lower cost ([[2605.05126\|ConsisVLA-4D]] 98.1% LIBERO, 70.0% real bimanual vs OpenVLA 28.5%, 2.31× faster) and depth-aware reasoning traces generalize OOD ([[2508.07917\|MolmoAct]] 86.6%, 72.1% OOD). |
| **Anchor surveys** | [[2506.20134\|3D World Models Survey]], [[2504.05786\|3D Spatial Reasoning in LLM Survey]], [[2510.16732\|World Models for Embodied AI Survey]] |
| **Key targets** | LIBERO ≥98.1% ([[2605.05126\|ConsisVLA-4D]]); real bimanual ≥70.0% (vs OpenVLA 28.5%); 2.31× inference speedup / 1.36× training-cost cut; OOD SR ≥72.1% ([[2508.07917\|MolmoAct]]) |

**Why it matters.** A policy that plans over a horizon must keep an object's geometry and identity coherent across time and viewpoint — else the action it commits at step 1 is invalidated by a hallucinated scene at step 5. The field's two answers both fall short: stay 2D (cheap, but projection-biased and 4D-inconsistent, per [[2605.05126|ConsisVLA-4D]]) or generate explicit future frames (consistent, but compute-heavy). [[2605.05126|ConsisVLA-4D]] takes a third path — *implicit* spatio-temporal consistency attention (CV-Aligner, CO-Fuser, CS-Thinker) that learns local object dynamics + global depth and enforces 4D coherence *without* generating frames at inference — for 98.1% LIBERO, 70.0% real long-horizon bimanual (vs OpenVLA 28.5%), at 2.31× faster inference and 1.36× cheaper training. [[2508.07917|MolmoAct]] makes the temporal-geometry reasoning *explicit and steerable* — depth-aware perception tokens + visual reasoning traces — and the payoff is OOD robustness (72.1% SimplerEnv variant-aggregation, 86.6% LIBERO). The non-consensus claim: 4D consistency is a *constraint to enforce on reasoning*, not a *frame sequence to generate* — and enforcing it implicitly is both cheaper and more robust. This is the temporal twin of B1's spatial scene-graph: B1 grounds geometry in space, B2 in time.

**First-principles framing.**
- **First principle**: For an action to be planned over a horizon, the imagined geometry must be *temporally and cross-view consistent* — the same object on a coherent 4D trajectory. Consistency is a constraint the representation must satisfy; it is not the same as rendering every intermediate frame.
- **Assumption being challenged**: The either/or that you accept projection-biased 2D (OpenVLA-class default) or pay for explicit future-frame generation ([[2604.26694|X-WAM]]-class) to get 4D consistency. [[2605.05126|ConsisVLA-4D]] gets explicit-3D accuracy *and* a 2.31× speedup with *implicit* consistency attention — so the tradeoff is breakable.
- **The bet**: Implicit 4D-consistency attention matches or beats explicit-frame policies on long-horizon real-world SR (≥70.0% bimanual vs OpenVLA 28.5%) at strictly lower inference cost (≥2.31× speedup), and the consistency constraint — not the raw 3D — drives the OOD robustness ([[2508.07917|MolmoAct]] 72.1% OOD): ablating consistency collapses OOD SR more than ablating any single perceptual feature.

**Evidence.**
- [[2605.05126|ConsisVLA-4D]] — Implicit consistency attention (CV-Aligner/CO-Fuser/CS-Thinker); 98.1% LIBERO, 70.0% real bimanual, 2.31× faster; the canonical "implicit 4D beats explicit-3D on cost" result.
- [[2508.07917|MolmoAct]] — Depth-aware perception tokens + visual reasoning traces; 86.6% LIBERO, 72.1% OOD, steerable; *explicit temporal-geometry reasoning* drives OOD robustness.
- [[2507.01099|Geometry-aware 4D Robot Video]] — 4D RGB+pointmap generation with cross-view consistency; the explicit-generation counterpart B2 enforces implicitly.
- [[2504.20995|TesserAct]] — 4D-aware (RGB-D-N) world model; evidence that adding the temporal-depth channel sharpens action prediction.
- [[2602.10098|VLA-JEPA]] — Latent-JEPA policy 97.2% LIBERO; the implicit-latent counterpart that enforces consistency in latent space without explicit geometry.

**Concrete research questions.**
1. **Q1 — Consistency-ablation OOD test.** Ablate the spatio-temporal consistency attention from [[2605.05126|ConsisVLA-4D]] while holding perception fixed. Does OOD SR collapse more than ID SR — confirming consistency (not raw 3D) drives robustness?
2. **Q2 — Implicit vs explicit 4D cost/accuracy frontier.** Plot [[2605.05126|ConsisVLA-4D]] (implicit) against [[2507.01099|Geometry-aware 4D Robot Video]] / [[2604.26694|X-WAM]] (explicit) on the SR-vs-latency plane. Is implicit Pareto-dominant, or only on a sub-class of tasks?
3. **Q3 — Reasoning-trace steerability transfer.** [[2508.07917|MolmoAct]]'s visual traces give 75% steering SR (+33% over language). Does pairing implicit consistency (B2) with explicit steerable traces ([[2508.07917|MolmoAct]]) compound, or are they redundant grounding signals?
4. **Q4 — Horizon-length scaling.** At what horizon does the implicit-consistency advantage over 2D appear and over explicit-generation disappear? Sweep task length and measure the crossover.

**Related research papers.**
- [[2605.05126|ConsisVLA-4D]] — Implicit 4D-consistency attention; the 2D-vs-explicit-3D cost dichotomy.
- [[2508.07917|MolmoAct]] — Depth-aware reasoning traces; OOD brittleness and language-steering ambiguity.
- [[2507.01099|Geometry-aware 4D Robot Video]] — Explicit 4D RGB+pointmap generation; the explicit counterpart (C2 boundary).
- [[2504.20995|TesserAct]] — 4D RGB-D-N WM; the temporal-depth channel.
- [[2602.10098|VLA-JEPA]] — Latent-JEPA consistency; implicit consistency in latent space.
- [[2505.05800|3D-CAVLA]] — 3D context-aware policy; scene-level 3D conditioning over time.
- [[2604.16484|DexWorldModel]] — O(1)-memory WM; the efficiency budget the consistency mechanism must fit.
- [[2510.16732|World Models for Embodied AI Survey]] — frames the implicit-vs-explicit 4D question.

**Benchmarks & metrics.**
- [[2306.03310|LIBERO]] — [[2605.05126|ConsisVLA-4D]] 98.1% (outperforming SpatialVLA +20%, CoT-VLA +14.2%), [[2508.07917|MolmoAct]] 86.6%; the ID consistency bar.
- Real-world long-horizon bimanual — [[2605.05126|ConsisVLA-4D]] 70.0% vs OpenVLA 28.5% / OpenVLA-OFT 51.8%; the sim-to-real horizon-consistency stress test.
- SimplerEnv variant-aggregation (OOD) — [[2508.07917|MolmoAct]] 72.1% (+7.8% over RT-2-X); the OOD-robustness metric the consistency constraint targets.

> [!warning] Risks
> - **Implicit consistency may not be inspectable** — you can't see what 4D structure the attention learned, hurting debuggability. → Mitigation: pair with [[2508.07917|MolmoAct]]'s explicit visual reasoning traces (Q3) so the temporal reasoning is steerable and auditable.
> - **Single-source cost claim** — the 2.31× speedup rests on [[2605.05126|ConsisVLA-4D]] alone. → Mitigation: Q2's full cost/accuracy frontier across implicit and explicit methods is the go/no-go before generalizing the efficiency claim.
> - **Implicit 4D may silently fail on the longest horizons** where drift accumulates invisibly. → Mitigation: Q4's horizon-scaling crossover bounds the regime; beyond it, route to **C4**'s explicit persistent geometric memory rather than stretching implicit consistency.

## Cluster C — Geometry-Native World Models & Memory

*The world model's representation is geometry, not appearance — a model-agnostic substrate any policy or model can use.*

### C1 — Occupancy World Models as the Manipulation Rollout Substrate

| | |
|---|---|
| **Cluster** | C — Geometry-Native World Models |
| **Thesis** | A world model's long-horizon stability is bounded by how fast *geometric* error piles up — and an explicit occupancy grid with rigid-transform constraints bounds that error where a latent substrate doesn't. The manipulation-WM field skips occupancy because it was built only in driving, and assumes the rollout substrate should be the same RGB-D latent the policy sees. The bet: a voxel-semantic occupancy WM holds geometric coherence over horizons where latent WMs drift ([[2603.28887\|OccSim]] 3,000+ stable frames, +22.1% rel mIoU, 80× horizon over latent baselines) — the failure mode is *horizon length*, not Chamfer-per-frame. |
| **Anchor surveys** | [[2510.16732\|World Models for Embodied AI Survey]], [[2604.22748\|Agentic World Modeling Survey]], [[2506.20134\|3D World Models Survey]] |
| **Key targets** | Stable rollout ≥3,000 frames / ≥4 km ([[2603.28887\|OccSim]]); +22.1% rel mIoU vs asset-based sim; 80× horizon over prior <50-frame WMs; manipulation port: minute-scale geometric coherence vs latent-world-model drift |

**Why it matters.** [[2510.16732|World Models for Embodied AI Survey]] traces the WM spatial axis from latent → token → explicit 3D, and sibling **C3** ([[2604.26694|X-WAM]]) already pushes the *latent-4D* frontier — geometry injected into a Diffusion Transformer, decoded internally, 15 Hz, Chamfer 0.0049. C1 takes the *other* corner of the same cluster: a WM whose rollout substrate is a voxel-semantic *occupancy grid* an external renderer or planner reads directly. The delta matters because the two substrates fail differently. C3's latent-4D fails on per-frame fidelity (Chamfer) — and is excellent there. An occupancy WM's failure mode is *horizon length* — and [[2603.28887|OccSim]] proves that explicit occupancy + Warp-DiT rigid-transform constraints bound the error to sustain 3,000+ frames over 4+ km (80× the prior <50-frame ceiling), with data that lifts downstream forecasting +22.1% rel mIoU. The contribution: bring this long-horizon-stable, externally-readable occupancy into manipulation, where it complements C3's latent imagination (explicit-external vs latent-internal) — explicit voxel geometry for the long-horizon planner-readable rollout, latent for the per-step high-fidelity imagine. Distinct from **A2**: A2 puts the same occupancy *inside a policy's forward-model loop* (vs a pixel-WM baseline); C1 is the *standalone WM substrate* (vs latent C3) — complementary positions, not a duplicate.

**First-principles framing.**
- **First principle**: A WM's long-horizon stability is bounded by how fast *geometric* error grows across rollout steps. An occupancy grid with rigid-transform constraints ([[2603.28887|OccSim]]'s Warp-DiT) moves geometry through a bounded operator; a latent substrate has no such per-step bound and drifts.
- **Assumption being challenged**: That the manipulation rollout substrate should be the same RGB-D latent the policy sees (the [[2510.10125|CTRL-WORLD]] / C3-latent [[2604.26694|X-WAM]] convention), because reusing the perception representation is convenient. [[2603.28887|OccSim]]'s 80× horizon gain shows a purpose-built occupancy substrate wins precisely on the long-horizon stability that matters for planning.
- **The bet**: A voxel-semantic occupancy WM holds geometric coherence over minute-scale manipulation horizons where a latent-4D baseline (sibling C3, [[2604.26694|X-WAM]]) drifts, and the gap is in *horizon-to-divergence* (not per-frame Chamfer, where latent-4D is strong) — making the two complementary, not competitive.

**Evidence.**
- [[2603.28887|OccSim]] — Voxel-semantic occupancy WM; 3,000+ stable frames, 4+ km, +22.1% rel mIoU, 80× horizon, 67% zero-shot; the long-horizon-stable occupancy substrate.
- [[2604.26694|X-WAM]] — Unified 4D WM, latent depth-injection, Chamfer 0.0049 vs 0.0680, 15 Hz; sibling **C3**'s anchor — the latent-4D neighbor C1 is delta'd against (strong per-frame fidelity, internal decode).
- [[2510.16732|World Models for Embodied AI Survey]] — latent→token→explicit-3D trajectory; occupancy at the explicit end.
- [[2506.20134|3D World Models Survey]] — the 2D→3D transition motivating explicit-geometry WMs.
- [[2604.22748|Agentic World Modeling Survey]] — the L2-Simulator domain-law rollout requirement occupancy stability satisfies.

**Concrete research questions.**
1. **Q1 — Horizon-to-divergence: occupancy vs latent.** On matched manipulation tasks, measure frames-to-geometric-divergence for an occupancy WM vs sibling C3's [[2604.26694|X-WAM]]-class latent. Does the 80× driving gap partially survive at tabletop scale?
2. **Q2 — Externally-renderable advantage.** Quantify the value of the occupancy grid being *third-party readable* — can an off-the-shelf planner consume it for collision-checking without a learned decoder, and does that beat decoding a latent?
3. **Q3 — Complementary substrate switching.** Run occupancy for long-horizon planner-readable rollout, switch to C3's [[2604.26694|X-WAM]] latent for per-step high-fidelity imagine. Does the hybrid beat either substrate alone on (horizon × fidelity)?
4. **Q4 — Sub-cm Warp-DiT.** Does [[2603.28887|OccSim]]'s rigid-transform error-bounding survive at manipulation resolution, or does the bound loosen below the meter-scale it was validated at?

**Related research papers.**
- [[2603.28887|OccSim]] — Long-horizon occupancy WM; the rollout substrate.
- [[2604.26694|X-WAM]] — Latent-4D WM; sibling **C3** and the per-frame-fidelity contrast.
- [[2510.10125|CTRL-WORLD]] — Controllable video WM; the latent/pixel substrate occupancy replaces for long horizons.
- [[2604.16484|DexWorldModel]] — O(1)-memory dexterous WM; the efficiency contrast.
- [[2604.22748|Agentic World Modeling Survey]] — multi-step domain-law rollout requirement.
- [[2510.16732|World Models for Embodied AI Survey]] — explicit-3D substrate framing.
- [[2506.20134|3D World Models Survey]] — 2D→3D transition.
- [[2504.20995|TesserAct]] — RGB-D-N 4D WM; the depth-augmented midpoint between latent and full occupancy.

**Benchmarks & metrics.**
- [[2603.28887|OccSim]] protocol — stable-generation-length (frames/km) + downstream mIoU lift; 3,000+ frames, +22.1% rel mIoU; the horizon-stability metric (the right axis, not Chamfer-per-frame).
- [[2406.02523|RoboCasa]] — Geometry-bound long-horizon manipulation; the target suite for the occupancy-substrate port, where sibling C3's [[2604.26694|X-WAM]] (latent) sets 79.2% on 24 tasks.
- Chamfer / mIoU over horizon — the explicit metric distinguishing C1's failure mode (horizon length) from C3's [[2604.26694|X-WAM]] (per-frame Chamfer 0.0049).

> [!warning] Risks
> - **Driving→manipulation scale gap** — occupancy validated at meter-scale, manipulation needs sub-cm. → Mitigation: Q4's sub-cm Warp-DiT test is the go/no-go; report the resolution at which the error bound breaks rather than assuming transfer.
> - **Overlap with sibling C3** if the explicit/latent delta blurs in practice. → Mitigation: keep the contribution pinned to *externally-renderable long-horizon occupancy* (Q2) and *complementarity* (Q3) — C1 is not a better X-WAM, it is the substrate X-WAM isn't.
> - **Occupancy supervision scarcity in manipulation data.** → Mitigation: derive occupancy in sim (free) and from depth + gripper geometry on real data; bound real-world claims to where occupancy GT is recoverable.

### C2 — 4D-Geometric-Consistent Video Prediction for 6-DoF Pose Extraction

| | |
|---|---|
| **Cluster** | C — Geometry-Native World Models |
| **Thesis** | A 6-DoF pose is a geometric quantity — cross-view-consistent pointmaps expose it directly to any tracker, while RGB-only frames leave it ambiguous. The field predicts RGB-only frames and re-estimates 3D after the fact, assuming a pixel video model plus a downstream pose estimator suffices. The bet: jointly predicting RGB + cross-view-consistent pointmaps yields directly-readable 6-DoF trajectories that drive far higher manipulation SR ([[2507.01099\|Geometry-aware 4D Robot Video]] 0.64 avg task SR across three sim tasks vs Dreamitate 0.12 and Diffusion Policy 0.12). |
| **Anchor surveys** | [[2506.20134\|3D World Models Survey]], [[2510.16732\|World Models for Embodied AI Survey]], [[2604.22748\|Agentic World Modeling Survey]] |
| **Key targets** | Avg task SR ≥0.64 across three sim tasks ([[2507.01099\|Geometry-aware 4D Robot Video]]) vs Dreamitate 0.12 / Diffusion Policy 0.12 (≈5× baseline); cross-view geometric consistency (higher mIoU) + lower FVD/AbsRel; generalize to novel viewpoints without retraining |

**Why it matters.** Video-prediction-for-action methods (Dreamitate-class) predict future RGB frames and then bolt on a pose estimator — and the recovery is the weak link: RGB-only frames leave 6-DoF pose ambiguous, so the policies are brittle (Dreamitate and Diffusion Policy both at 0.12 avg task SR in [[2507.01099|Geometry-aware 4D Robot Video]]'s evaluation). [[2507.01099|Geometry-aware 4D Robot Video]] makes the geometry a *predicted output*: it extends Stable Video Diffusion to predict future multi-view RGB *and* aligned 3D pointmaps — a pointmap VAE + cross-view pointmap diffusion loss (each view's pointmaps in the reference frame) + multi-view cross-attention — *without* explicit camera poses at inference. The payoff: off-the-shelf trackers read accurate 6-DoF trajectories straight off the predicted pointmaps, for 0.64 avg task SR across three sim tasks (≈5× the 0.12 of RGB-only baselines) and novel-viewpoint generalization without retraining. The delta vs [[2605.05126|ConsisVLA-4D]] (B2): B2 enforces 4D consistency *implicitly* for an end-to-end head; C2 predicts *explicit externally-readable* pointmaps so a *separate* tracker extracts pose — the geometry leaves the model. That externality is exactly C's commitment.

**First-principles framing.**
- **First principle**: A 6-DoF pose is geometric. Cross-view-*consistent* pointmaps expose it to any tracker (pose = rigid transform read off corresponding 3D points); RGB-only frames encode it implicitly and view-dependently, so a downstream estimator must re-solve an ill-posed problem each frame.
- **Assumption being challenged**: The Dreamitate-class convention that a pixel video model + a downstream pose estimator suffices. [[2507.01099|Geometry-aware 4D Robot Video]]'s ≈5× SR gap (0.64 vs 0.12) shows the post-hoc estimator is the bottleneck — predicting geometry *consistently* inside the model, not estimating it after, is what makes the trajectory extractable.
- **The bet**: Jointly predicting RGB + cross-view-consistent pointmaps yields directly-readable 6-DoF trajectories at ≥0.64 avg task SR vs ~0.12 for RGB-plus-estimator baselines (≈5×), and the gain tracks *cross-view consistency* (mIoU) — ablating the cross-view pointmap loss collapses trajectory accuracy more than degrading RGB quality does.

**Evidence.**
- [[2507.01099|Geometry-aware 4D Robot Video]] — SVD extended to predict RGB + cross-view-consistent pointmaps (pointmap VAE + cross-view diffusion loss + multi-view cross-attention); 0.64 avg task SR vs 0.12 baselines, novel-viewpoint generalization; the canonical explicit-pointmap-for-pose result.
- [[2605.05126|ConsisVLA-4D]] — Implicit 4D-consistency policy; the B2 contrast — internal consistency for an end-to-end head vs C2's externally-read pointmaps.
- [[2606.03943|PointAction]] — Video-to-point model (RGB + dynamic pointmaps); the action-head sibling whose predicted points C2's readout parallels for pose.
- [[2504.20995|TesserAct]] — 4D RGB-D-N WM; predicting explicit geometric channels alongside RGB sharpens action extraction.
- [[2604.26694|X-WAM]] — Latent-4D WM with end-effector-derived camera poses; the latent-substrate contrast (sibling C3).

**Concrete research questions.**
1. **Q1 — Cross-view-consistency ablation.** Remove the cross-view pointmap diffusion loss while holding RGB quality fixed. Does trajectory-extraction accuracy (and downstream SR) collapse more than RGB FVD degrades — confirming consistency, not appearance, drives the action gain?
2. **Q2 — Predicted-pointmap vs sensed-depth pose readout.** Compare 6-DoF extraction from [[2507.01099|Geometry-aware 4D Robot Video]]'s predicted pointmaps against extraction from sensed depth on the same tasks. How much accuracy is lost by predicting vs sensing geometry?
3. **Q3 — Novel-viewpoint generalization bound.** The model generalizes to novel viewpoints without retraining. Quantify the viewpoint-extrapolation range before pose-extraction accuracy degrades — the operational envelope of the externally-readable claim.
4. **Q4 — Explicit-pointmap (C2) vs implicit-consistency (B2) on the same task.** Hold the task fixed; compare C2's tracker-readout pipeline against [[2605.05126|ConsisVLA-4D]]'s end-to-end implicit head. Where does externalizing geometry (debuggable, tracker-readable) beat internalizing it (cheaper)?

**Related research papers.**
- [[2507.01099|Geometry-aware 4D Robot Video]] — RGB+pointmap 4D prediction for pose; the RGB-only pose-ambiguity fix.
- [[2605.05126|ConsisVLA-4D]] — Implicit 4D consistency; the internalized-geometry contrast (B2 boundary).
- [[2606.03943|PointAction]] — RGB+dynamic-pointmap prediction; the same predict-geometry-not-pixels move for the action head.
- [[2504.20995|TesserAct]] — 4D RGB-D-N WM; explicit-geometric-channel prediction.
- [[2604.26694|X-WAM]] — Latent-4D WM; the latent-substrate alternative (sibling C3).
- [[2505.20279|VLM-3R]] — 3D-reconstructive reasoning; reading geometry out of reconstructed 3D.
- [[2507.13347|Pi3]] — Pointmap/3D-reconstruction model; the pointmap machinery C2 relies on.
- [[2510.16732|World Models for Embodied AI Survey]] — frames explicit-geometry WMs and the pose-extraction use case.

**Benchmarks & metrics.**
- [[2507.01099|Geometry-aware 4D Robot Video]] task SR — 0.64 avg across three sim tasks vs Dreamitate 0.12 / Diffusion Policy 0.12; the ≈5× action-extraction gap, the headline metric.
- Cross-view 3D consistency (mIoU) + depth (AbsRel, δ₁) + RGB temporal coherence (FVD) — [[2507.01099|Geometry-aware 4D Robot Video]] reports lower FVD/AbsRel + higher mIoU/δ₁; the geometric-consistency metrics that should predict the SR gain (Q1).
- Novel-viewpoint generalization — [[2507.01099|Geometry-aware 4D Robot Video]] maintains quality + consistency on unseen views without retraining; the externally-readable robustness check.

> [!warning] Risks
> - **Single-anchor direction** — the headline rests on [[2507.01099|Geometry-aware 4D Robot Video]]'s three-task evaluation. → Mitigation: Q1's consistency-ablation and Q2's predicted-vs-sensed comparison are the internal validity checks; broaden the task set before generalizing the ≈5× claim.
> - **Predicted pointmaps may be noisier than sensed depth**, degrading pose readout. → Mitigation: Q2 quantifies the predict-vs-sense gap directly; if large, gate C2 to settings where sensing is unavailable (novel viewpoints, no depth sensor).
> - **Three-task SR is a narrow base** for a substrate claim. → Mitigation: frame the contribution as *the mechanism* (explicit cross-view pointmaps → tracker-readable pose) validated on three tasks, with broader evaluation as the explicit next step — do not overclaim breadth.

### C3 — Natively-4D Geometry as a World-Representation Substrate

| | |
|---|---|
| **Cluster** | C — Geometry-Native World Models & Memory |
| **Thesis** | For contact and spatial tasks the action is set by geometry a model can only infer indirectly from pixels — so a representation that is *natively 4D* (RGB + depth + 3D geometry over time) carries it directly, where 2D pixels lifted after the fact don't. The field treats live 4D as too expensive to deploy. The bet: a 4D-native substrate beats latent/pixel baselines on geometry-bound tasks — 79.2% [[2406.02523\|RoboCasa]] (+12.1 pp over [[2601.16163\|Cosmos Policy]]), Chamfer 0.0049 vs 0.0680, and a 4.5× action-latency speedup to 15 Hz — a representation any policy or model can stand on. |
| **Anchor surveys** | [[2506.20134\|3D World Models Survey]], [[2510.16732\|World Models for Embodied AI Survey]], [[2604.26509\|3D Generation for Embodied AI Survey]] |
| **Key targets** | [[2406.02523\|RoboCasa]] 79.2% avg over 24 tasks (+12.1 pp vs [[2601.16163\|Cosmos Policy]]); Chamfer 0.0049 vs 0.0680 two-stage; +2.34 dB PSNR; 4.5× action-latency speedup (4665→1033 ms) at 5 denoising steps → 15 Hz real-time |

**Why it matters.** [[2510.16732|World Models for Embodied AI Survey]] traces the spatial axis from latent vector → token sequence → explicit 3D rendering, and [[2506.20134|3D World Models Survey]] frames the field's move "from 2D visual perception to comprehensive 3D spatial cognition." Yet almost every deployed model still imagines in 2D pixels and recovers geometry only implicitly — which [[2604.26694|X-WAM]] says "leads to physically implausible predictions and hinders geometrically faithful reconstruction." The usual defense is that 4D is a luxury: high-fidelity video needs many denoising steps, actions need few, and reconstructing 3D online is assumed too slow to deploy. [[2604.26694|X-WAM]] breaks that trade-off — a lightweight interleaved depth branch injects 3D into a pretrained Diffusion Transformer, and Asynchronous Noise Sampling decouples the video and action denoising schedules so actions decode in 5 steps while video stays high-fidelity. The contribution is the *representation*: geometry as the native substrate of imagination, at real-time rates — exactly what a policy needs when the action depends on where things are in 3D, not how they look in 2D. X-WAM is a world model, but the 4D-native substrate is model-agnostic: the same latent-4D state could ground a policy's action head or planner, not only a world model's imagination. Intra-cluster delta: C1 (occupancy) and C2 (4D-video pointmaps) keep this geometry *explicit and external*; C3 keeps it *latent and internal*.

**First-principles framing.**
- **First principle**: For contact-rich and spatially-bound tasks, the action is a function of *geometry* — relative pose, depth, surface normals, free space. A pixel substrate that doesn't encode geometry forces the consumer to re-infer it from appearance every step, discarding structure the substrate could carry directly. The geometry is in the task, not the rendering choice.
- **Assumption being challenged**: That a pixel substrate is sufficient once its frames look right, and that explicit 4D is too expensive to deploy (so geometry, if needed, is recovered by a separate two-stage pipeline). [[2604.26694|X-WAM]] shows the two-stage path is both worse geometrically (Chamfer 0.0680 vs 0.0049) and slower than a unified 4D model with asynchronous denoising.
- **The bet**: A 4D-native substrate beats latent/pixel baselines on geometry-bound manipulation — 79.2% over 24 [[2406.02523|RoboCasa]] tasks, +12.1 pp over [[2601.16163|Cosmos Policy]] — with higher-fidelity geometry (Chamfer 0.0049 vs 0.0680, +2.34 dB PSNR) at *no* deployment penalty: a 4.5× action-latency speedup (4665→1033 ms) at 5 steps, 15 Hz on a physical robot.

**Evidence.**
- [[2604.26694|X-WAM]] — Unified 4D WM: interleaved depth branch + unilateral attention inject 3D into a pretrained DiT; Asynchronous Noise Sampling aligns train/inference noise across modalities; 79.2% [[2406.02523|RoboCasa]], Chamfer 0.0049 vs 0.0680, 15 Hz — the canonical 4D-native-substrate result.
- [[2510.16732|World Models for Embodied AI Survey]] — spatial axis latent → token → explicit 3D rendering (NeRF, 3DGS); 4D is the named end-state.
- [[2506.20134|3D World Models Survey]] — the 2D→3D-cognition transition; 3D scene generation + spatial reasoning are the open capabilities.
- [[2605.20752|GaussianDream]] — Feed-forward 3DGS WM supervising a renderable future at train time (98.4% [[2306.03310|LIBERO]], 34.4→50% real); the rendering-end neighbor that drops 3D heads at deploy rather than running 4D live.
- [[2603.17240|GigaWorld-Policy]] — Future visual dynamics as dense training supervision, *no* video generation at inference (9× speedup); the drop-the-geometry-at-deploy contrast for C3's "keep 4D at deployment" claim.

**Concrete research questions.**
1. **Q1 — Native-4D vs lift-after ablation.** Hold the backbone fixed; compare [[2604.26694|X-WAM]]'s interleaved depth branch against a pixel substrate + post-hoc depth estimator on geometry-bound [[2406.02523|RoboCasa]] tasks. Isolate how much *native* 4D buys over *recovered* 4D.
2. **Q2 — Asynchronous denoising for the action-quality / video-fidelity trade.** Generalize Asynchronous Noise Sampling: can the action schedule shrink to 1–4 steps (step-distillation, per the efficiency direction in the umbrella [[Embodied-AI|Embodied-AI]]) without degrading the 4D geometry the consumer reads?
3. **Q3 — 4D substrate for contact (C3 × B1-style discrete contact).** Does an explicit 3D geometry channel make discrete contact-mode prediction easier than a continuous latent — geometry exposes penetration / proximity directly?
4. **Q4 — Camera-pose-from-end-effector consistency.** [[2604.26694|X-WAM]] derives camera poses from end-effector poses; test whether this self-consistency constraint improves OOD geometry vs free camera conditioning.
5. **Q5 — 4D imagination as a model-agnostic planning oracle.** Roll the 4D substrate forward under candidate actions; does planning in explicit geometry beat planning in latent on spatially-bound tasks (insertion, stacking, pouring), and does the same substrate transfer from a world-model consumer to a policy action head?

**Related research papers.**
- [[2604.26694|X-WAM]] — Unified 4D WM with asynchronous denoising; 79.2% [[2406.02523|RoboCasa]], 15 Hz; the natively-4D substrate, the anchor.
- [[2605.20752|GaussianDream]] — Feed-forward 3DGS WM; dense 3D train, light deploy; 98.4% [[2306.03310|LIBERO]]; renderable geometry dropped at inference.
- [[2603.17240|GigaWorld-Policy]] — Future-dynamics supervision, no video at inference; 9× speedup; the drop-the-geometry contrast.
- [[2604.16484|DexWorldModel]] — Causal latent WM on [DINOv3](https://arxiv.org/abs/2508.10104) semantic targets; 94% [[2504.13059|RoboTwin]]; semantic-latent, not geometric — the alternative to explicit 4D.
- [[2605.15153|Pelican-Unified]] — Shared latent z + pixel-side generator; 93.5% [[2504.13059|RoboTwin]]; multi-modal but not natively 4D-geometric.
- [[2411.04983|DINO-WM]] — Frozen [[2304.07193|DINOv2]] + lightweight dynamics; appearance latent, no geometry channel.
- [[2602.10098|VLA-JEPA]] — Pure latent JEPA WM; 97.2% [[2306.03310|LIBERO]]; no geometric decoder.
- [[2603.16666|Fast-WAM]] — Train video, test latent; drops the WM at deploy — opposite of keeping 4D online.

**Benchmarks & metrics.**
- [[2406.02523|RoboCasa]] (24 tasks) — [[2604.26694|X-WAM]] 79.2% avg, +12.1 pp over [[2601.16163|Cosmos Policy]]; the geometry-bound manipulation suite.
- Chamfer Distance / PSNR — [[2604.26694|X-WAM]] Chamfer 0.0049 vs 0.0680 two-stage, +2.34 dB PSNR; geometric-fidelity ground truth, not visual FID.
- [[2306.03310|LIBERO]] — Action SR; [[2605.20752|GaussianDream]] 98.4% reference for the rendering-end neighbor.
- Inference latency (Hz) — [[2604.26694|X-WAM]] 4.5× speedup → 15 Hz at 5 steps; whether 4D survives the real-time budget.

> [!warning] Risks
> - **4D supervision needs depth/3D ground truth** not present in most robot datasets. → Mitigate via [[2604.26694|X-WAM]]'s end-effector-derived camera poses + off-the-shelf depth estimators; bound the claim to tasks where geometry is recoverable.
> - **4D is only worth it on geometry-bound tasks** — on appearance-bound tasks latent already wins. → Score on contact / spatial tasks ([[2406.02523|RoboCasa]] insertion, stacking), not headline [[2306.03310|LIBERO]] SR; report the task-type split explicitly.
> - **Real-time 4D rests on one result** ([[2604.26694|X-WAM]]). → Treat Q1's native-vs-recovered ablation as the go/no-go before claiming 4D belongs at deployment rather than as a train-time auxiliary.

### C4 — Persistent Geometric Memory for Long-Horizon Coherence

| | |
|---|---|
| **Cluster** | C — Geometry-Native World Models & Memory |
| **Thesis** | Long-horizon coherence needs geometric object permanence — remembering where things are when they leave view and return — and that drifts away in attention-only models. The field assumes a long-enough context window or a Markovian latent suffices. The bet: an explicit geometric memory holds minute-scale coherence where Markovian/long-context substrates drift — [[2603.17117\|MosaicMem]] RotErr 0.51° vs 1.42°/4.65° at 16 FPS, [[2603.24576\|Chameleon (Episodic Memory)]] 100%/73.5% long-horizon DSR, with [[2605.10921\|RoboMemArena]] showing 68.9% of subtasks genuinely need history — a memory any policy, model, or reasoner can pin its geometry to. |
| **Anchor surveys** | [[2604.22748\|Agentic World Modeling Survey]], [[2504.21853\|Interactive Generative Video Survey]], [[2602.04411\|Self-evolving Embodied AI]] |
| **Key targets** | [[2603.17117\|MosaicMem]] RotErr 0.51° vs [SEVA](https://arxiv.org/abs/2503.14489) 1.42° / [CaM](https://arxiv.org/abs/2506.03141) 4.65°, 16 FPS autoregressive, minute-level coherence; [[2603.24576\|Chameleon (Episodic Memory)]] 100.0% episodic-recall / 73.5% spatial-tracking / 72.2% sequential DSR; [[2605.10921\|RoboMemArena]] 68.9% of subtasks need history |

**Why it matters.** [[2504.21853|Interactive Generative Video Survey]] names persistent memory and dynamics fidelity as the two open problems blocking explorable world simulators, and [[2604.22748|Agentic World Modeling Survey]]'s L2 Simulator must "compose multi-step rollouts that respect domain laws" — which fails over long horizons when the model forgets where things were. The usual fix — longer context, or a Markovian latent to carry state — drifts: [[2603.17117|MosaicMem]] documents that implicit attention memory "suffers from inaccurate egomotion (drift), redundancy, and difficulty manipulating latent scene representations," while static explicit-3D caches "struggle with dynamic scenes." A hybrid now exists. [[2603.17117|MosaicMem]] lifts 2D patches into 3D and conditions on them geometry-consistently (Warped RoPE / Warped Latent), reaching RotErr 0.51° vs [SEVA](https://arxiv.org/abs/2503.14489)'s 1.42° and [CaM](https://arxiv.org/abs/2506.03141)'s 4.65°, minute-level coherence at 16 FPS. [[2603.24576|Chameleon (Episodic Memory)]] takes the manipulation side — perceptual aliasing makes long-horizon tasks non-Markovian, so it builds disambiguated, indexable episodic events with a latent imagination objective (100% episodic-recall DSR). And [[2605.10921|RoboMemArena]] proves the need is real: 68.9% of its subtasks genuinely require history, and reactive policies fail them. The contribution is the *memory representation* — geometric object-permanence pinned to a world-frame — usable by C3's 4D substrate, a policy's action head, or a world model's imagination loop alike. The source papers are video/WM papers, but the mechanism is model-agnostic.

**First-principles framing.**
- **First principle**: Long-horizon coherence requires *object permanence* — remembering where things are when they leave view and return. This is a geometric memory problem, not a sequence-length one: an attention-only model with unbounded context still drifts because nothing pins imagined geometry to a persistent frame.
- **Assumption being challenged**: That a long-enough context window or a Markovian latent suffices. [[2603.17117|MosaicMem]] shows implicit attention drifts and static 3D caches break on dynamics; [[2605.10921|RoboMemArena]] shows 68.9% of subtasks are non-Markovian; [[2603.24576|Chameleon (Episodic Memory)]] shows perceptual aliasing makes the observation-level decision genuinely history-dependent.
- **The bet**: A memory-augmented representation holds minute-scale geometric coherence where Markovian/long-context substrates drift — [[2603.17117|MosaicMem]]'s RotErr 0.51° vs 1.42° (explicit) / 4.65° (implicit) at 16 FPS, and [[2603.24576|Chameleon (Episodic Memory)]]'s 100.0% episodic-recall / 73.5% spatial-tracking / 72.2% sequential DSR — on the [[2605.10921|RoboMemArena]] subtasks (68.9%) that demonstrably need history.

**Evidence.**
- [[2603.17117|MosaicMem]] — Hybrid spatial memory: lift 2D patches to 3D, condition a DiT via Warped RoPE / Warped Latent + PRoPE camera interface; RotErr 0.51° vs 1.42°/4.65°, 16 FPS autoregressive ("Mosaic Forcing"), minute-level coherence — the geometric-memory anchor.
- [[2603.24576|Chameleon (Episodic Memory)]] — Bio-inspired episodic memory (spatiotemporal anchors, multi-timescale states, HoloHead imagination objective); 100% episodic-recall / 73.5% spatial-tracking / 72.2% sequential DSR; memory makes manipulation non-Markovian-aware.
- [[2605.10921|RoboMemArena]] — 26 sim + 5 real memory tasks; PrediMem (keyframe bank + sliding window + predictive-coding head) 38.5% TSR / 55.2% CSR; 68.9% of subtasks need history — the demand-side proof.
- [[2504.21853|Interactive Generative Video Survey]] — names persistent memory + dynamics fidelity as the open problems for explorable simulators.
- [[2604.22748|Agentic World Modeling Survey]] — L2 long-horizon composition is where memory becomes load-bearing.

**Concrete research questions.**
1. **Q1 — Geometric memory for action-conditioned consumers.** Port [[2603.17117|MosaicMem]]'s lifted-3D-patch memory from camera-controlled video to *action*-conditioned manipulation; does RotErr-style geometric coherence translate to higher long-horizon SR?
2. **Q2 — Episodic memory × geometric memory (C4 internal).** Combine [[2603.24576|Chameleon (Episodic Memory)]]'s indexable events with [[2603.17117|MosaicMem]]'s geometry-consistent patches — do disambiguated *events* + persistent *geometry* compound on [[2605.10921|RoboMemArena]]?
3. **Q3 — Predictive-coding memory as a calibration signal.** [[2605.10921|RoboMemArena]]'s predictive-coding head makes hidden states sensitive to state transitions; does this double as a forward-inverse calibration target (the train-time-trust lever)?
4. **Q4 — Memory pinned to world-frame vs robot-frame.** Does a geometric memory pinned to a persistent *world*-frame ([[2603.17117|MosaicMem]]'s lifted-3D patches) hold long-horizon coherence better than a robot-frame memory — i.e., does decoupling memory from the body's pose reduce drift? (Cross-embodiment transfer of this world-frame memory is developed in the umbrella [[Embodied-AI|Embodied-AI]].)
5. **Q5 — Memory as the persistence layer for C1/C2/C3.** Does pinning C1's occupancy, C2's pointmaps, or C3's latent-4D to C4's world-frame memory keep their geometry coherent over minute-scale horizons — the cluster-spanning persistence test?

**Related research papers.**
- [[2603.17117|MosaicMem]] — Hybrid explicit-3D + implicit-attention spatial memory; RotErr 0.51°, 16 FPS; the geometric-memory anchor.
- [[2603.24576|Chameleon (Episodic Memory)]] — Episodic memory for long-horizon manipulation; 100% episodic-recall DSR; indexable events + latent imagination.
- [[2605.10921|RoboMemArena]] — Memory benchmark + PrediMem; 68.9% subtasks need history; the demand-side proof and benchmark substrate.
- [[2604.16484|DexWorldModel]] — Dual-State TTT memory, O(1) over 2,000 steps; memory as efficiency, not geometric permanence — the contrast.
- [[2603.23497|WildWorld]] — 108M-frame state-action dataset; Action Following + State Alignment; long-horizon state-consistency substrate.
- [[2510.10125|CTRL-WORLD]] — Controllable video WM; 38.7→83.4% on unseen objects; controllability, no persistent memory.
- [[2504.21853|Interactive Generative Video Survey]] — names persistent memory as an open problem; no mechanism.
- [[2604.22748|Agentic World Modeling Survey]] — L1/L2/L3; L2 long-horizon composition needs memory.

**Benchmarks & metrics.**
- [[2605.10921|RoboMemArena]] — 26 sim + 5 real memory tasks; 68.9% need history; PrediMem 38.5% TSR / 55.2% CSR / 52% real; the memory-dependence benchmark.
- RotErr (camera-motion accuracy) — [[2603.17117|MosaicMem]] 0.51° vs [SEVA](https://arxiv.org/abs/2503.14489) 1.42° / [CaM](https://arxiv.org/abs/2506.03141) 4.65°; geometric-drift metric for long-horizon coherence.
- Decision Success Rate (DSR) — [[2603.24576|Chameleon (Episodic Memory)]] 100% episodic-recall / 73.5% spatial-tracking / 72.2% sequential; episodic-memory ground truth.
- Generation rate + coherence horizon — [[2603.17117|MosaicMem]] 16 FPS autoregressive, minute-level coherent; the speed-at-which-memory-holds metric.

> [!warning] Risks
> - **Explicit geometric memory needs reliable 3D lifting** — off-the-shelf estimators can fail on texture-poor scenes ([[2603.17117|MosaicMem]]). → Hybridize with implicit attention ([[2603.17117|MosaicMem]]'s own design) so the model degrades gracefully when lifting is noisy.
> - **Episodic memory retrieval can interfere** on visually-aliased-but-irrelevant events ([[2603.24576|Chameleon (Episodic Memory)]]). → Use disambiguated indexable encoding + goal-directed retrieval, not similarity-only retrieval; validate on [[2605.10921|RoboMemArena]]'s occlusion/counting splits.
> - **Memory adds footprint** against the real-time deployment budget. → Q5's patch-level vs [[2604.16484|DexWorldModel]] O(1) TTT Pareto is the go/no-go; persistent memory only earns its place if coherence gain beats the memory cost.

## Cluster D — 3DGS/4D Reconstruction for Embodied Perception & Sim

*Reconstruction built for interaction-readiness — geometry that carries physics and kinematic structure, not just radiance.*

### D1 — Interaction-Ready 3DGS Assets: Geometry Built for Physics, Not Rendering

| | |
|---|---|
| **Cluster** | D — Reconstruction for Embodied Perception |
| **Thesis** | An embodied agent acts on *interaction-readiness* — geometric validity, physical parameterization, kinematic executability — not on appearance. The reconstruction field optimizes visual fidelity (PSNR/FID) and assumes a higher-fidelity NeRF/3DGS is a better embodied asset. The bet: a pipeline that bakes physics + kinematics from a single video produces directly-usable interactive environments ([[2404.09833\|Video2Game]] single-video → interactive NeRF+mesh+physics at 100+ FPS), against the survey-named bottleneck that "simulation-readiness over visual fidelity" is the real blocker ([[2604.26509\|3D Generation for Embodied AI Survey]]). |
| **Anchor surveys** | [[2604.26509\|3D Generation for Embodied AI Survey]], [[2506.20134\|3D World Models Survey]], [[2510.16732\|World Models for Embodied AI Survey]] |
| **Key targets** | Single-video → interactive environment at ≥100 FPS browser-compatible ([[2404.09833\|Video2Game]]); simulation-readiness criteria met (geometric validity + physical parameterization + kinematic executability + URDF/MJCF compat) per [[2604.26509\|3D Generation for Embodied AI Survey]] |

**Why it matters.** The reconstruction community optimizes radiance — PSNR, SSIM, FID — and [[2604.26509|3D Generation for Embodied AI Survey]] names the mismatch as *the* embodied bottleneck: there is "a crucial distinction between conventional 3D generation (focused on visual appearance) and embodied-oriented 3D generation, which demands interaction readiness, physical grounding, and simulator compatibility," blocked by "scarcity of physical annotations" and the "trade-off between geometric quality and physical validity." [[2404.09833|Video2Game]] proves you can build for interaction directly: from a *single video* it produces a real-time, browser-compatible environment fusing a large NeRF with a baked game-engine mesh *and a physics module* — scene decomposed into entities with rigid-body attributes for collision and manipulation, at 100+ FPS. The contribution: treat *interaction-readiness* ([[2604.26509|3D Generation for Embodied AI Survey]]'s four criteria — geometric validity, physical parameterization, kinematic executability, URDF/MJCF compat) as the *optimization target*, not a downstream conversion of a fidelity-optimized asset. The delta from [[Sim2Real|Sim2Real]]-A1/B1 is sharp: [[2604.25459|GS-Playground]] (90% real SR) and [[2511.04665|Real-to-Sim GS]] (r=0.915) minimize the transfer gap *given* an asset; D1 makes the asset interaction-ready *in the first place*. The Hinton-taste inversion: the field rewards fidelity because fidelity is measurable, but the embodied-relevant quantity is whether the agent can *act* in the asset.

**First-principles framing.**
- **First principle**: An embodied agent interacts with geometry, physics, and kinematics — not radiance. A reconstruction's embodied value is its *interaction-readiness* (can the agent collide, grasp, articulate in it), a property orthogonal to and not implied by visual fidelity.
- **Assumption being challenged**: The NeRF/3DGS default that a higher-fidelity reconstruction (better PSNR/FID) is a better asset, full stop. [[2604.26509|3D Generation for Embodied AI Survey]] documents the shift to "interaction readiness and simulation deployability *over* visual fidelity" — fidelity-optimized assets are routinely *not* simulation-ready, so the target is wrong.
- **The bet**: A pipeline that optimizes interaction-readiness directly — baking physics + kinematic decomposition from a single video ([[2404.09833|Video2Game]]'s 100+ FPS environment) — produces assets an agent can act in *without* post-hoc physics annotation, meeting [[2604.26509|3D Generation for Embodied AI Survey]]'s four criteria where fidelity-first pipelines fail at least one (usually physical parameterization or kinematic executability).

**Evidence.**
- [[2404.09833|Video2Game]] — Single-video → interactive NeRF + baked mesh + rigid-body physics, scene decomposed into actionable entities, 100+ FPS browser-compatible; the canonical build-for-interaction result.
- [[2604.26509|3D Generation for Embodied AI Survey]] — Establishes "simulation-readiness over visual fidelity" + the four readiness criteria; the direction's organizing frame.
- [[2403.08321|ManiGaussian]] — 3DGS world model for manipulation; 3DGS reconstructions can carry dynamics for action, not just rendering.
- [[2311.12198|PhysGaussian]] — Physics-integrated Gaussian Splatting (continuum mechanics on Gaussians); physical parameterization baked into the 3DGS itself.
- [[2003.08515|SAPIEN]] — Articulated-object sim; the kinematic-executability (URDF-style) reference D1's reconstructions must hit.

**Concrete research questions.**
1. **Q1 — Readiness-vs-fidelity decoupling.** Build the same scene optimizing (a) PSNR and (b) [[2604.26509|3D Generation for Embodied AI Survey]]'s four readiness criteria. Measure how often a fidelity-optimal asset fails a readiness criterion — quantifying the orthogonality the first principle claims.
2. **Q2 — Single-video kinematic recovery.** [[2404.09833|Video2Game]] decomposes into rigid entities. Can articulated structure (joints, DoF) be recovered from a single video to produce URDF/MJCF-exportable assets, or does articulation need multi-view / interaction data?
3. **Q3 — Physical-parameter sufficiency for policy transfer.** What fidelity of physical parameterization (mass, friction, restitution) is *sufficient* for a policy trained in the reconstructed asset to act correctly — the readiness threshold, distinct from the transfer-gap question Sim2Real owns?
4. **Q4 — Readiness asset → A/C consumer.** Does a D1 interaction-ready asset directly feed A1's point-cloud head (act-on geometry) and C1's occupancy WM (rollout-over geometry)? Test the D→A and D→C supply chain end-to-end.

**Related research papers.**
- [[2404.09833|Video2Game]] — Single-video → interactive physics-ready environment; the build-for-interaction target.
- [[2604.26509|3D Generation for Embodied AI Survey]] — Simulation-readiness taxonomy; the fidelity-vs-readiness mismatch.
- [[2403.08321|ManiGaussian]] — 3DGS world model for manipulation; dynamics-carrying reconstructions.
- [[2311.12198|PhysGaussian]] — Physics-integrated Gaussians; baked physical parameterization.
- [[2003.08515|SAPIEN]] — Articulated-object sim; kinematic executability (URDF).
- [[2604.25459|GS-Playground]] — High-throughput 3DGS sim, 90% real SR; the Sim2Real-A1 transfer-gap neighbor (D1 = readiness, not transfer).
- [[2511.04665|Real-to-Sim GS]] — 3DGS + soft-body digital twins, r=0.915; the Sim2Real-B1 reconstruction-for-transfer neighbor.
- [[2510.16732|World Models for Embodied AI Survey]] — reconstruction's role in supplying geometry to world models (the D→C handoff).

**Benchmarks & metrics.**
- [[2404.09833|Video2Game]] — Novel-view synthesis (PSNR/SSIM) + interactive frame rate (100+ FPS) + physics plausibility; the joint fidelity-and-interactivity metric showing both can be met.
- [[2604.26509|3D Generation for Embodied AI Survey]] readiness criteria — geometric validity / physical parameterization / kinematic executability / simulator-format compat; the readiness scorecard (the right axis, not PSNR alone).
- [[2604.25459|GS-Playground]] / [[2511.04665|Real-to-Sim GS]] — 90% real SR / r=0.915 sim-real correlation; the transfer-gap benchmarks D1's readiness-asset feeds into but does not itself optimize (the Sim2Real delta made measurable).

> [!warning] Risks
> - **Interaction-readiness lacks a standard benchmark** — readiness is a checklist, not a leaderboard number. → Mitigation: adopt [[2604.26509|3D Generation for Embodied AI Survey]]'s four criteria as the explicit scorecard (Q1) and report per-criterion pass/fail, not a single fidelity number.
> - **Single-video may not recover articulation/physics** for complex scenes. → Mitigation: Q2 bounds what single-video reconstruction can recover; fall back to multi-view or interaction data where articulation needs it, and state the boundary.
> - **Boundary blur with [[Sim2Real|Sim2Real]]-A1/B1.** → Mitigation: keep D1 pinned to *readiness as the optimization target* (Q1, Q3) and explicitly route the *transfer-gap evaluation* to [[2604.25459|GS-Playground]] / [[2511.04665|Real-to-Sim GS]].

## Cross-Cutting Themes

> [!tip] Geometry Is What the Task Keeps Fixed; Appearance Is Noise
> The one idea fires across all four clusters. A1's point-cloud head, A3's depth-token bridge, B2's 4D-consistency attention, C1's occupancy substrate, and C2's cross-view pointmaps all make the same move: build the representation around the geometry the *task* keeps fixed (where things are, how they persist in 3D), not the appearance the *rendering* adds (pixels). A1 predicts geometry-vs-RGB gaps *widen* under appearance shift; B2 predicts the 4D-*consistency* constraint (not raw 3D) drives OOD robustness; C2 predicts cross-view *consistency* (not RGB fidelity) drives the ≈5× action gain — three independent directions, one falsifiable claim: the geometric channel, not the appearance channel, carries the action-relevant signal. This is the Hinton tenet that the brain plans in world coordinates, not image coordinates, turned into a measurable bet.

> [!tip] The RGB-Token Tax Is Paid at Every Layer of the Stack
> The "representation-supervision bottleneck" [[2606.03943|PointAction]] names isn't local to the policy — it shows up at every layer, which is why the directions stack instead of compete. A1/A3 pay it at the *action head*; B1/B2 at the *cognition layer* (ungrounded language over RGB); C1/C2 at the *world-model substrate* (latent/pixel rollouts that re-parse geometry); D1 at the *asset* (fidelity-optimized reconstructions that aren't interaction-ready). Each cluster removes the tax at its layer, and the gains *compound* down the stack: a D1 asset feeds A1's geometric head and C1's occupancy WM; a B1 scene-graph feeds A1's action head; B2's consistency is the temporal half of B1's spatial grounding. The whole is one geometric pipeline, not five isolated tricks.

> [!tip] Cheap Geometry vs Full Geometry — A Frontier, Not a Binary
> A3, B2, and C1 each sit at the *cheap* end of a cost/capability frontier whose expensive end a sibling owns. A3's single-view depth-token bridge is the cheap version of A1's full point branch (≥80% of the gain at side-channel cost). B2's implicit 4D-consistency is the cheap version of C2's explicit pointmap generation (same accuracy, 2.31× faster, no frame generation). C1's externally-readable occupancy is the long-horizon-cheap complement to sibling **C3**'s per-frame-expensive latent-4D. The non-consensus reading: the field frames these as either/or (RGB vs 3D, implicit vs explicit, latent vs occupancy), but each pair is a *frontier* whose operating point is task-conditional — cheap geometry for transit/appearance-bound segments, full geometry for contact/spatial-bound ones. The research question isn't "which substrate wins" but "where is the crossover" — measured in A1-Q2, B2-Q4, A3-Q1, C1-Q3.

> [!tip] Explicit-External ↔ Latent-Internal Is Cluster C's Organizing Axis (and the Real C-vs-B Line)
> The deepest split in the doc isn't 2D-vs-3D but *who reads the geometry*. B1, B2 keep it *internal* — a scene-graph or consistency-attention the action head consumes end-to-end (cheaper, less inspectable). C1, C2, D1 make it *external* — occupancy a third-party planner reads (C1), pointmaps a tracker reads for 6-DoF (C2), assets a simulator loads (D1). Externality buys debuggability, composability, and tool-reuse (Q2 in C1/C2, Q4 in C2) at the cost of a decoder/extractor step. This is Cluster C's *internal* organizing principle: C3 ([[2604.26694|X-WAM]]) keeps its 4D latent *internal* (decoded for imagination), C1/C2 keep geometry *external* — the split lives inside one cluster, not across the [[WAM|WAM]] boundary. The same axis cleanly separates B2 (implicit, internal) from C2 (explicit, external) on the overlapping 4D-consistency idea, and C1/C2 from C3 on the world-model substrate.

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| No benchmark isolates *cross-embodiment appearance-shift* SR to test the geometry-vs-RGB claim — current suites mix appearance and geometry shift | A1 | [[2606.03943\|PointAction]] xArm7 zero-shot (43.0%) is the closest split, but conflates embodiment + appearance + geometry shift in one number |
| No manipulation benchmark measures *rollout-horizon-to-geometric-divergence* for forward models — SR is reported at fixed horizon, hiding stability | A2 | [[2603.28887\|OccSim]]'s stable-frame-count (3,000+) is the metric, but only in driving; no manipulation analog |
| No benchmark reports the *recovery-fraction* of a cheap depth-bridge vs a full-3D branch on a common backbone — gains are vs weak RGB baselines, not the full-3D ceiling | A3 | [[2510.14836\|QDepth-VLA]] +8.8% / +29.7% over open_pi_0 vs [[2508.09071\|GeoVLA]] 97.7% — never head-to-head on one backbone |
| No benchmark splits the human-model spatial gap into *reasoning* vs *perception* failure | B1 | [[2601.13304\|CausalSpatial]] (GPT-5 54.17% vs human 84.49%) measures the gap but doesn't isolate reasoning from depth-perception failure |
| No benchmark plots the *implicit-vs-explicit 4D* cost/accuracy frontier at matched accuracy | B2 | [[2605.05126\|ConsisVLA-4D]] (98.1% LIBERO, 2.31× speedup) reports both but only for the implicit method; no explicit-4D point on the same plane |
| No manipulation benchmark stress-tests *long-horizon geometric coherence* of occupancy vs latent at sub-cm resolution | C1 | [[2603.28887\|OccSim]] horizon stability (driving, meter-scale) + [[2604.26694\|X-WAM]] Chamfer 0.0049 (per-frame) — neither measures sub-cm horizon-to-divergence |
| No benchmark isolates *6-DoF-extraction accuracy from predicted vs sensed geometry* across viewpoints | C2 | [[2507.01099\|Geometry-aware 4D Robot Video]] (0.64 vs 0.12 SR, 3 tasks) shows the gap but on a narrow set, no predicted-vs-sensed isolation |
| Native-4D-at-deployment vs lift-after-pixel on geometry-bound tasks (Chamfer + SR + latency jointly), and whether the latent-4D substrate transfers across consumers (WM ↔ policy) | C3 | [[2604.26694\|X-WAM]] (native 4D, single system, no native-vs-recovered ablation) + [[2605.20752\|GaussianDream]] (4D at train, dropped at deploy) |
| Persistent geometric + episodic memory on memory-dependent manipulation over minute-scale horizons, model-agnostic across substrates | C4 | [[2605.10921\|RoboMemArena]] (demand-side, reactive baselines) + [[2603.17117\|MosaicMem]] (geometric memory on camera-video, not action-conditioned) |
| No benchmark scores reconstruction on *interaction-readiness* (the four criteria) rather than fidelity — readiness is a checklist with no leaderboard | D1 | [[2604.26509\|3D Generation for Embodied AI Survey]] names the four criteria; [[2404.09833\|Video2Game]] meets them, but no standardized readiness benchmark exists ([[2604.25459\|GS-Playground]]/[[2511.04665\|Real-to-Sim GS]] grade transfer, not readiness) |

## Cross-References

> [!note] Focus-Program tie-in
> The coupling term $M_{\text{base,arm}}$ in [[Focus-Program|Focus-Program]] is irreducibly geometric. **A1 (point-cloud-native action heads) plugs into [[Focus-Program|Focus-Program]] under WB-A1's representation layer, and is the policy-side twin of WAM-A2's wrench imagination** — an explicit-geometry representation enabler under the anchor, NOT a 5th program corner. A1 supplies the metric-3D state on which the explicit coupling head operates; the program's four corners (WB-A1 anchor / WAM-A2 predict / Sim2Real-B2 ground / EAI-C1 verify) are unchanged.

**Sibling research-direction docs:**
- [[WAM|WAM]] — the WAM-machinery sibling. The model-agnostic *representations* WAM once hosted — natively-4D imagination ([[2604.26694|X-WAM]]) and persistent geometric memory ([[2603.17117|MosaicMem]], [[2603.24576|Chameleon (Episodic Memory)]]) — now live here as **C3** and **C4**. WAM keeps the WAM-internal concerns: the latent/architecture substrate (its Cluster A) and training/grounding (its Cluster B). Cluster C's explicit-vs-latent split is an *intra-cluster* axis, not a cross-doc boundary.
- [[Sim2Real|Sim2Real]] — A1/B1 ([[2604.25459|GS-Playground]] 90% real SR, [[2511.04665|Real-to-Sim GS]] r=0.915) own the *transfer-gap* face of 3DGS reconstruction; this doc's D1 owns the *interaction-readiness* face. Cross-reference, never re-own.
- [[Embodied-AI|Embodied-AI]] — the umbrella; cross-cutting joint-evaluation and cross-embodiment directions live there.
- [[Whole-Body|Whole-Body]] — WB-A1's coupled-dynamics action model consumes A1's geometric representation (see Focus-Program tie-in).
- [[Focus-Program|Focus-Program]] — the four-corner focused program A1 plugs into under WB-A1's representation layer.

**Deep-dives:**
- [[../Embodied-AI/08_Latent-World-Models|08_Latent-World-Models]] — the latent-vs-explicit substrate debate Cluster C extends to the explicit-geometry side.
- [[../Embodied-AI/11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] — physical parameterization (D1) and physics-grounded geometry.
- [[../Embodied-AI/06_VLA-Reasoning-and-CoT|06_VLA-Reasoning-and-CoT]] — the spatial-CoT cognition layer (Cluster B).
- [[../Embodied-AI/05_VLA|05_VLA]] — the RGB-token policy baselines Cluster A inverts.
- [[../Embodied-AI/02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]] — the benchmark suites and simulation environments cited throughout.

**General topics:**
- [[../General/05_Computer-Vision-and-3D|05_Computer-Vision-and-3D]] — 3D-understanding foundations.
- [[../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — the policy / world-model / manipulation papers.
- [[../General/03_Reasoning-and-Planning|03_Reasoning-and-Planning]] — spatial reasoning and CoT (Cluster B).
- [[../General/08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — the five anchor surveys.
