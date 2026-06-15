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
> Every policy, reasoner, and world model stands on *some* representation of the scene, and the field's default is RGB tokens — pixels a 2D backbone is hoped to turn into the geometry an action needs. The structural fact this doc bets on: **geometry is what the task keeps fixed; appearance is the noise on top.** A gripper, an object, and their contacts sit at metric 3D positions that do not move when the lighting, texture, or camera does — so a representation built around that geometry carries the action-relevant signal directly, and an RGB token leaves it implicit and pays to re-infer it every step.
> These **11 directions across 4 clusters** organize the bets by *where the explicit geometric state lives in the stack*: inside the action head (A), upstream of it as a 3D-grounded cognition layer (B), as the world-model and memory substrate (C), and as the reconstructed assets an agent acts in (D). The axis is **Mechanism** — the geometric representation itself, independent of which robot uses it.
> The non-consensus bet: the geometric channel, not the appearance channel, carries the action-relevant signal — and the gap to RGB *widens* exactly where geometry holds and pixels move (cross-embodiment, viewpoint shift, occlusion, long horizons). The field treats explicit 3D as overhead a big enough 2D model makes unnecessary; the directions here treat it as the thing the loss should be built around.

---

## Methodology

**Scope.** This doc reads the vault's 3D/4D-spatial and geometric-representation corpus in `_KnowledgeHub_/` — five structural surveys + benchmark suites (the Survey Landscape below) plus ~95 method papers — cross-checked against [[../General/05_Computer-Vision-and-3D|05_Computer-Vision-and-3D]] and [[../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] and the deep-dives [[../Embodied-AI/08_Latent-World-Models|08_Latent-World-Models]], [[../Embodied-AI/11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]], [[../Embodied-AI/06_VLA-Reasoning-and-CoT|06_VLA-Reasoning-and-CoT]], and [[../Embodied-AI/05_VLA|05_VLA]]. No date filter — 2024 (Video2Game) through 2026-Q2. It owns the *model-agnostic 3D/4D representation* — a geometric state any policy or model stands on. Sibling [[WAM|WAM]] owns *WAM machinery* (latent backbone, training, grounding), so the latent-4D substrate ([[2604.26694|X-WAM]]) and persistent geometric memory ([[2603.17117|MosaicMem]], [[2603.24576|Chameleon (Episodic Memory)]]) live here as C3/C4 treated as *representations*; sibling [[Sim2Real|Sim2Real]] owns the *transfer gap* of 3DGS reconstruction ([[2604.25459|GS-Playground]], [[2511.04665|Real-to-Sim GS]]), so Cluster D owns only *interaction-readiness*. Where a card borders a sibling, one clause states the delta.

---

## 3D/4D Spatial Survey Landscape

| Survey / Benchmark | The open problem it names (surveys) / what it measures (benchmarks) | Fuels |
|---|---|---|
| [[2506.20134\|3D World Models Survey]] | Field is mid-transition "from 2D visual perception to comprehensive 3D spatial cognition"; explicit-3D action and forward-model interfaces remain rare and embodiment-specific | A1, A2, A3, B1, C1, C3 |
| [[2510.16732\|World Models for Embodied AI Survey]] | Spatial-representation axis is evolving latent → token → explicit 3D; explicit-geometry world models are nascent and rarely externally renderable | A1, A2, B2, C1, C2, C3 |
| [[2604.22748\|Agentic World Modeling Survey]] | The L2 Simulator must "compose multi-step rollouts that respect domain laws" — but geometric (not pixel) forward models are underbuilt and break over long horizons | A1, A2, B1, C1, C4 |
| [[2504.05786\|3D Spatial Reasoning in LLM Survey]] | MLLM spatial reasoning is *ungrounded*: coordinate-metric reasoning lags object-naming; no consensus interface between language reasoning and metric 3D | A3, B1, B2 |
| [[2604.26509\|3D Generation for Embodied AI Survey]] | "Simulation-readiness over visual fidelity" is the bottleneck; scarce physical annotations; geometry-vs-physical-validity trade-off; deformable assets unsolved | D1, D2 |
| [[2306.03310\|LIBERO]] | The 4-suite manipulation success-rate bar (spatial / object / goal / long); the standard ID surface where RGB backbones already saturate (~97%) and the geometry advantage must instead show on shift | A1, A3, B2, C3 |
| [[2406.02523\|RoboCasa]] | Kitchen-scale generalization-stress manipulation (24 tasks + unseen); the geometry-bound long-horizon suite where pixel/latent world models drift | A1, A2, C1, C3, D1 |
| [[2601.13304\|CausalSpatial]] | MLLMs fail *causal* spatial reasoning (collision/occlusion/trajectory) and hallucinate when ungrounded; GPT-5 54.17% vs human 84.49%, low Not-Sure-Rate | B1, B2 |
| [[2605.29074\|Embodied3DBench]] | 13 SOTA VLMs, none robust on low-level metric 3D + interaction perception; score correlates with downstream LIBERO SR — the metric-3D gap is load-bearing for action | B1, B2 |
| [[2605.27367\|SpatialBench]] | Spatial-foundation-model benchmark (19 datasets, 31 models) exposing depth/pose gaps across density and egocentric views; the perception substrate upstream reasoning depends on | B1, A3 |
| [[2605.10921\|RoboMemArena]] | Robotic-memory benchmark (26 sim + 5 real); 68.9% of subtasks genuinely need history; reactive policies fail them | C4 |
| [[2605.21572\|PhysX-Omni]] | Physics-readiness benchmark + generator (PhysX-Bench/PhysXVerse): material / affordance / kinematic-structure scoring across rigid + deformable + articulated, which fidelity metrics ignore | D2 |

> [!tip] Convergence patterns
> - **The RGB-token tax — policies and world models default to pixels, leaving metric 3D motion, contact geometry, and spatial constraints implicit** (4-way): [[2506.20134|3D World Models Survey]] (field is only now moving "from 2D visual perception to comprehensive 3D spatial cognition"), [[2510.16732|World Models for Embodied AI Survey]] (the spatial axis is *still* evolving latent → token → explicit 3D, with explicit-geometry world models nascent), [[2604.22748|Agentic World Modeling Survey]] (the L2 Simulator must compose rollouts that "respect domain laws," yet geometric forward models are underbuilt), and [[2406.02523|RoboCasa]] (a geometry-bound generalization suite where the pixel/latent default visibly drifts) — four sources name the same supervision cost explicit geometry would erase, the mandate for Clusters A and C.
> - **The grounding gap is metric, not semantic — the failure is *placing* objects in 3D and predicting how they move, not *naming* them** (4-way): [[2504.05786|3D Spatial Reasoning in LLM Survey]] (coordinate-metric reasoning lags object-naming; no language↔metric-3D interface), [[2601.13304|CausalSpatial]] (GPT-5 sits **30 points** below humans on causal spatial tasks and is overconfident — a low Not-Sure-Rate), [[2605.29074|Embodied3DBench]] (13 VLMs, **none robust** on low-level metric 3D, and the score correlates with downstream LIBERO SR), and [[2605.27367|SpatialBench]] (19 datasets / 31 models expose persistent depth/pose gaps) — four benchmarks converge that the spatial deficit is a *missing metric representation*, the mandate for Cluster B.
> - **Readiness beats fidelity — the field optimizes appearance (PSNR/FID) when the embodied bottleneck is interaction-readiness: geometry that carries physics, articulation, and a usable export format** (3-way): [[2604.26509|3D Generation for Embodied AI Survey]] (names "simulation-readiness over visual fidelity," scarce physical annotations, and the deformable-asset gap as *the* bottleneck), [[2605.21572|PhysX-Omni]] (introduces a physics-readiness benchmark precisely because fidelity metrics do not score material / kinematics / affordance), and [[2406.02523|RoboCasa]] (a manipulation suite where a visually-faithful-but-physics-thin asset still fails the task) — three sources invert the fidelity objective, the mandate for Cluster D.

---

## Formal Framing

The central object is an **explicit geometric state** $G_t$ — a representation of scene structure that is *metric* and *externally interpretable*, as opposed to an appearance latent $z_t$ that is only decodable to pixels. Every direction is a statement about *where $G_t$ lives in the stack and who reads it*.

| Object | Definition | Owning cluster |
|---|---|---|
| Geometry-conditioned action head | $a_t = \pi(G_t, l)$ with $G_t$ an explicit metric state (point cloud $\in \mathbb{R}^{N\times 3}$, depth channel, or distilled 3D prior) the head conditions on instead of RGB tokens | A |
| Geometric forward model | $\hat G_{t+1} = f(G_t, a_t)$ over an explicit grid — occupancy $O \in \{0,1,\dots,K\}^{H\times W\times D}$ or rigid-body state — that the planner rolls forward | A (in-loop), C (substrate) |
| Spatial-cognition layer | a scene-graph / coordinate state $S$ over geometric entities s.t. $a_t = \pi(\text{reason}(S))$ — reasoning is *over* metric geometry, upstream of the action head | B |
| Renderable / 4D geometry WM | $G_t$ = explicit 4D (pointmap sequence, occupancy, or latent-4D) decoded for imagination (internal) or read by a third-party renderer/tracker to recover 6-DoF pose (external) | C |
| Interaction-ready asset | a reconstructed scene or object carrying geometry **+** physics parameters **+** kinematic structure (URDF/MJCF-exportable), not just radiance | D |

**The decodability axis.** $G_t$ differs by *who reads it*, and this is the doc's deepest organizing principle — sharper than 2D-vs-3D. At one end $G_t$ is **explicit and external**: occupancy a planner collision-checks (C1), pointmaps a tracker reads for 6-DoF (C2), assets a simulator loads (D1, D2). At the other end $G_t$ is **latent and internal**: a 4D state decoded inside the model for imagination (C3) or a scene-graph an end-to-end head consumes (B1, B2). Between them sits **persistent**: geometry pinned to a world-frame so it survives long horizons (C4). Externality buys debuggability, composability, and tool-reuse at the cost of a decoder/extractor step; internality is cheaper but opaque. The split from [[WAM|WAM]] is about *ownership* (Spatial-4D owns the representation model-agnostically; WAM owns the machinery), not decodability — C1/C2/C3 sit on the same axis inside *this* doc.

> [[2604.26509|3D Generation for Embodied AI Survey]] gives the canonical definition of the readiness criterion this doc adopts as the line between Cluster D and pure rendering:
> "simulation readiness as a primary evaluation criterion: geometric validity, physical parameterization, kinematic executability, and simulator format compatibility (URDF, MJCF)."

---

## Cluster Overview

| Cluster | Directions | Shared bottleneck | Cross-direction synergy |
|---|---|---|---|
| **A — Geometry-Native Policies** | A1, A2, A3 | The action head reads or predicts RGB tokens, leaving metric 3D implicit and paying an embodiment-specific data tax | **A1 is the lead** — its point-cloud state is the conditioning A2's occupancy forward model rolls forward and the upper bound A3's depth-token bridge approximates cheaply; the three span the *cost/benefit frontier* of explicit geometry (full point branch → in-loop occupancy → side-channel depth). [[2606.03943\|PointAction]] and [[2508.09071\|GeoVLA]] set the bar for A1; [[2510.14836\|QDepth-VLA]] for A3 |
| **B — 3D-Grounded Cognition** | B1, B2 | Reasoning isn't grounded in metric geometry: language CoT over RGB hallucinates spatial relations and dynamics | B1 grounds geometry in *space* (a scene-graph), B2 in *time* (4D consistency); together they are the spatial and temporal halves of one cognition layer, and both supply the upstream geometry Cluster A's action heads consume. [[2507.13362\|VLM Spatial Reasoning RL]] and [[2605.05126\|ConsisVLA-4D]] set the bar |
| **C — Geometry-Native World Models & Memory** | C1, C2, C3, C4 | World models imagine in pixels; geometry is recovered after the fact, isn't externally usable, isn't natively 4D, and isn't kept over long horizons | Organized by the **explicit-external ↔ latent-internal ↔ persistent** decodability axis: C1 (occupancy) and C2 (4D-video pointmaps) are *external* — a planner/tracker reads them; C3 ([[2604.26694\|X-WAM]]) is *latent* — 4D imagination decoded inside; C4 is *memory* — pinning C1/C2/C3's geometry to a world-frame so it survives minute-scale horizons. [[2603.28887\|OccSim]], [[2604.26694\|X-WAM]], [[2603.17117\|MosaicMem]] set the bars |
| **D — Reconstruction for Embodied Perception** | D1, D2 | Reconstruction optimizes radiance, not interaction-readiness; assets aren't physics- or kinematics-ready | D1 builds the *scene* you act in; D2 builds the *objects* that populate it (D2 → D1 composition); both supply the geometry the others consume — readable scenes for C's world models, point-cloud assets for A's policies. [[2404.09833\|Video2Game]] and [[2605.21572\|PhysX-Omni]] set the bars |


---

## Cluster A — Geometry-Native Policies

*The action head consumes or predicts explicit 3D — the policy's conditioning state is metric geometry, not RGB tokens. The three directions span the cost/benefit frontier of putting that geometry in the loop: a full point-cloud head where geometry is central, an occupancy forward model the planner rolls forward, and a cheap depth-token side-channel for the RGB policies nobody wants to re-train.*

### A1 — Point-Cloud-Native Action Heads vs RGB-Token Policies

| | |
|---|---|
| **Cluster** | A — Geometry-Native Policies |
| **Thesis** | An action is a function of *where things are in metric 3D* — and a point cloud says that directly, while an RGB token leaves it implicit. The policy field skips explicit 3D because it assumes a 2D-pretrained backbone already encodes the geometry the head needs. That assumption breaks under appearance shift, where geometry stays fixed but pixels move. The bet is in First-principles below. |
| **Anchor papers** | [[2506.20134\|3D World Models Survey]] (survey), [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2402.02500\|Point Cloud Matters]] (benchmark), [[2606.03943\|PointAction]] (method), [[2508.09071\|GeoVLA]] (method), [[2605.21414\|PointACT]] (method) |
| **Key targets** | Cross-embodiment zero-shot SR ≥43.0% ([[2606.03943\|PointAction]] xArm7); ID SR ≥47.7% RoboCasa365; LIBERO ≥97.7% ([[2508.09071\|GeoVLA]]); RLBench ≥82.3% ([[2605.21414\|PointACT]]); graded-shift sweep point > RGB by up to **76.92%** mean SR across **125** tasks ([[2402.02500\|Point Cloud Matters]]) |

**Why it matters.**
- **The gap**: the dominant recipe ([[2501.15830|SpatialVLA]], OpenVLA-class) feeds the head RGB tokens from a 2D backbone and hopes the geometry needed for contact-precise control falls out of the semantic features, so metric 3D motion and contact geometry stay implicit.
- **Today's answers**: the geometry-over-RGB principle is *already established* at small scale — [[2402.02500|Point Cloud Matters]] (NeurIPS'24) swept graded lighting/noise/background shift across 125 tasks and found point-cloud policies beat RGB by up to 76.92% mean SR *and* generalize better, and [[2306.06799|Point Cloud RL Study]] localized that advantage to agent-object relationship reasoning. At VLA scale: [[2606.03943|PointAction]] splits into an embodiment-agnostic video-to-point model + a small point-to-action decoder (43.0% zero-shot on an xArm7 it never trained on, 47.7% RoboCasa365 ID); [[2508.09071|GeoVLA]] runs a 3D point branch beside a frozen VLM (97.7% LIBERO) with height/scale/viewpoint robustness; [[2605.21414|PointACT]] couples points to actions at multiple scales (82.3% RLBench). All add geometry — none isolate the *minimal-sufficient-geometry knee* or the *representation-vs-decoder* driver of cross-embodiment transfer.
- **The opening**: [[2605.24642|GFM-VLA Study]] linear-probes the deficit directly — GR00T-N1.5's VLM output carries 0.73 m depth RMSE vs a geometric model's 0.41 m — so the RGB backbone provably does not encode the geometry the head needs, and supplying it explicitly is the lever.

**First-principles framing.**
- **First principle**: A manipulation action is set by the metric 3D layout (where gripper, object, and contacts are), not by 2D appearance. Geometry is fixed under lighting, texture, viewpoint, and camera placement; appearance is not. [[2606.02274|Dexterity-BEV]] is the cleanest demonstration: its BEV 3D frame holds 89.9% on shifted LIBERO exactly where 2D collapses to <10%.
- **Assumption being challenged**: the OpenVLA / [[2501.15830|SpatialVLA]] view that a big 2D backbone already encodes whatever geometry the head needs, so an explicit 3D branch is wasted overhead. [[2508.09071|GeoVLA]] and [[2606.03943|PointAction]] show it breaks under the shifts (height, scale, viewpoint, embodiment) where geometry holds but pixels move — and the latent counterpoint [[2602.10098|VLA-JEPA]] (97.2% LIBERO) shows even a strong *implicit*-geometry latent must be beaten on the geometry-bound split, not the saturated ID one. (The *graded-shift-helps* and *advantage-is-relational* claims are settled prior — [[2402.02500|Point Cloud Matters]], [[2306.06799|Point Cloud RL Study]] — so the contest moves to whether they hold *at 2D-pretrained-VLA scale* with *minimal* geometry.)
- **The bet**: the geometry-over-RGB advantage [[2402.02500|Point Cloud Matters]] proved with simple encoders survives at 2D-pretrained-VLA scale *and* most of it is recoverable from sparse geometry — specifically, (i) the recovery-vs-density curve has a knee far below [[2508.09071|GeoVLA]]'s full branch (≥80% of the full-branch SR gain at [[2403.03954|DP3]]-level sparsity), and (ii) it is the point *representation*, not [[2606.03943|PointAction]]'s factorized decoder, that carries the 43.0% xArm7 zero-shot transfer — swapping points→RGB-features (decoder fixed) collapses most of it, swapping the decoder (points fixed) does not.

**Related research papers.** One table; every paper is a row on the axis the direction turns on — *how geometry enters the action head* — from sensed points through predicted points, parallel branches, and learned/distilled latent priors, with `Key result` and the gap it leaves. The strongest rows are the load-bearing proof papers; the RGB row is the consensus this inverts.

| System | Geometry interface | Key result | What's missing |
|---|---|---|---|
| [[2606.03943\|PointAction]] | predicted dynamic pointmaps (embodiment-agnostic) | **47.7%** RoboCasa365 ID, **43.0%** zero-shot xArm7 (2–2.5× over baselines) | never isolates whether the point *representation* or the *factorized decoder* carries the zero-shot win |
| [[2606.02274\|Dexterity-BEV]] | BEV 3D frame + vertex maps aligning views and actions | **89.9%** shifted LIBERO where 2D fails (**<10%**) | the cleanest shift result, but on one BEV parameterization — no minimal-geometry sweep |
| [[2508.09071\|GeoVLA]] | parallel frozen-VLM + 3D point branch + 3D MoE expert | **97.7%** LIBERO, **77%** ManiSkill2, robust to height/scale/viewpoint | full branch is the expensive upper bound; doesn't say how much sparser geometry suffices |
| [[2605.21414\|PointACT]] | multi-scale point-action coupling | **96.0%** LIBERO, **82.3%** RLBench | coupling beats coarse injection but needs a full point cloud at inference |
| [[2506.06199\|3DFlowAction]] | 3D optical flow as an action interface (no action labels) | **70%** SR vs 2D-flow 25% / video-WM 20%; Franka↔XTrainer transfer | flow is a motion field, not a static state — limited on fine contact geometry |
| [[2403.03954\|DP3]] | sparse-point diffusion policy | compact point conditioning drives a precise policy | answers "is full 3D necessary" only at one sparse setting — no recovery-fraction curve |
| [[2402.02500\|Point Cloud Matters]] | sensed point cloud vs RGB/RGB-D, graded-shift sweep | point clouds beat RGB by up to **76.92%** mean SR across **125** tasks + best zero-shot to lighting/noise/background/view shift | runs H1's graded-shift sweep two years early, but on *simple* encoders/DP — never the 2D-pretrained-VLA backbone A1 inverts, nor a minimal-geometry knee |
| [[2306.06799\|Point Cloud RL Study]] | sensed point cloud in RL, vs RGB/RGB-D | 3D agents win on tasks needing agent-object 3D *relationship* reasoning, near-parity on planar | localizes the advantage to relational/contact reasoning (H2), but RL-scale, no VLA backbone, no representation-vs-decoder isolation |
| [[2601.16212\|Point Bridge]] | cross-domain point-cloud transfer interface | bridges sensed-point policies across domains | a transfer interface, not a minimal-geometry or representation-vs-decoder ablation |
| [[2505.18474\|Canonical Policy]] | SE(3)-equivariant canonicalized point policy | equivariance buys viewpoint/pose robustness for free | proves *structure* (equivariance) helps, but doesn't separate it from raw point density on the recovery curve |
| [[2509.01819\|ManiFlow]] | flow-matching policy where appearance *still* helps | strong SR with appearance retained alongside geometry | the counterpoint — geometry isn't strictly dominant; bounds the bet's "appearance is noise" claim where texture carries task signal |
| [[2604.12908\|VGA]] | manipulation as vision-to-geometry $f(v)\to G$ over a 3D-WM backbone | **98.1%** LIBERO, **+6%** OOD camera viewpoint | the first-principle as an architecture, but geometry is the *output*, not a sensed input |
| [[2604.15281\|R3D]] | LayerNorm-only 3D encoder + 3D augmentation (fixes the "scaling paradox") | RoboTwin 2.0 **83.8%** Easy / **64.8%** Hard, xArm6 real **60.7%** | makes 3D policies *scale*, but the win is the recipe, not an isolated geometry term |
| [[2605.11832\|AML-VLA]] | multi-view latent action manifold with G³T depth priors | **98.6%** LIBERO, **85.7%** LIBERO-Plus zero-shot perturbation | a learned 3D *prior*, not sensed geometry — leaves the sensed-vs-learned question open |
| [[2606.04436\|3DThinkVLA]] | latent 3D priors distilled via 3D-thinking co-training, no inference sensor | **98.7%** LIBERO, **81.0%** LIBERO-Plus zero-shot | geometry-as-latent-prior — strong OOD, but no explicit point state the head reads |
| [[2605.29416\|3DVLA]] | plug-and-play multi-view 3D fusion + object-centric 3D instances | **86.0%** LIBERO-Plus (SOTA), no 3D annotation | injected geometry, but on top of the RGB head — not a native point-cloud policy |
| [[2603.24393\|3D-MIX]] | VGGT 3D features into any VLA via semantic-gated fusion | **98.05%** LIBERO, **+12.51%** OOD | geometry bolted on without re-architecting — the cheap end of A1's own frontier (feeds A3) |
| [[2602.00937\|CLAMP]] | contrastive 3D multi-view action-conditioned pretraining | up to **+30%** SR, higher sample efficiency | 3D pretraining tuned for the policy, but the head still acts on RGB at inference |
| [[2604.14089\|UMI-3D]] | LiDAR 3D demonstration interface | drift-resistant pose on textureless/deformable scenes where vision SLAM fails | geometry-over-appearance at the *data* layer, not the action head |
| [[2604.06168\|Action Images]] | 7-DoF actions as projected multi-view 2D-Gaussian heatmaps (EE position/up/normal) | **60%** zero-shot RLBench reach / **45%** real close-drawer (vs **0–20%**), PSNR **23.48** vs TesserAct 20.83 | resolves 3D ambiguity by *projecting* geometry into views — not a sensed/predicted point state the head reads directly |
| [[2604.17880\|ST-π]] | structured spatio-temporal VLA (ST-VLM decomposition + dual-generator) | top SR across 4 LIBERO suites, gains widen on long-horizon | structured geometry, but no point-vs-RGB head ablation (feeds B-style structure) |
| [[2501.15830\|SpatialVLA]] | RGB-token spatial policy (consensus baseline) | the standard 2D head this direction inverts | leaves all metric 3D implicit — the row the bet is measured against |

**Hypotheses & tests.** The FP bet — the small-scale geometry-over-RGB advantage survives at VLA scale *and* from sparse geometry — decomposed. H1/H2 are *confirmed prior* ([[2402.02500|Point Cloud Matters]], [[2306.06799|Point Cloud RL Study]]) re-run at VLA scale to anchor the regime; the front-line contribution is H3 (minimal-geometry knee) + H4 (representation-vs-decoder) + H5 (beat the latent on OOD).
1. **H1 — The graded-shift advantage replicates at 2D-pretrained-VLA scale (confirmed prior, extended).**
   - *Prediction*: [[2402.02500|Point Cloud Matters]]'s graded lighting/noise/background sweep — which already showed point > RGB on simple encoders — holds with a *2D-pretrained-VLA backbone*: holding the backbone fixed, the point-head-minus-RGB SR margin grows monotonically with shift magnitude, ≈0 at zero shift.
   - *Test*: re-run [[2402.02500|Point Cloud Matters]]'s sim shift sweep with a [[2508.09071|GeoVLA]]-style VLA point head vs an RGB head; check the small-scale monotone pattern survives the backbone swap, then confirm it physically on [[2509.18953|Eva-VLA]]'s real-world graded-shift suite (illumination + 3D object transforms + adversarial patches, per-variation failure rates — SOTA VLAs surge from **4.0–23.5%** to over **80%** under optimized shift).
   - *Row*: Point Cloud Matters / GeoVLA / SpatialVLA.
   - *Falsifier*: a flat/non-monotone margin at VLA scale → the small-scale result is encoder-specific, not a backbone-invariant geometry principle.
2. **H2 — The advantage concentrates in relational/contact sub-segments at VLA scale (confirmed prior, extended).**
   - *Prediction*: [[2306.06799|Point Cloud RL Study]]'s localization of the win to agent-object *relationship* reasoning reproduces at VLA scale — decomposing SR by phase, the point-head margin concentrates in contact-rich segments and is near-zero in free-space transit.
   - *Test*: phase-label trajectories on [[2606.03943|PointAction]]'s RoboCasa365 tasks; report margin per phase.
   - *Row*: Point Cloud RL Study / PointAction.
   - *Falsifier*: a uniform margin across phases → the point state helps globally, not via relational contact geometry.
3. **H3 — Minimal sufficient geometry sits well below a full point branch.**
   - *Prediction*: most of the SR gain is recovered by sparse points ([[2403.03954|DP3]]-density), and the recovery-vs-density curve has a knee far below [[2508.09071|GeoVLA]]'s full branch.
   - *Test*: sweep point density/completeness on a fixed head; plot recovered fraction of the full-branch gain.
   - *Row*: DP3 / GeoVLA.
   - *Falsifier*: gain scales with density up to the full branch → cheap geometry doesn't suffice; A3's depth bridge is the only economical path.
4. **H4 — The point *representation*, not the factorized decoder, carries the zero-shot win.**
   - *Prediction*: swapping [[2606.03943|PointAction]]'s point representation for an RGB-feature representation (decoder architecture held fixed) collapses most of the 43.0% xArm7 transfer; swapping the decoder while keeping points does not.
   - *Test*: 2×2 representation-vs-decoder swap on the embodiment-free pretraining, scored on [[2505.14986|AnyBody]]'s controlled morphology-distance protocol (18 Isaac-Sim morphologies, explicit interpolation/extrapolation/composition splits) so the transfer is read off a suite that *isolates* morphological generalization from appearance/geometry confounds — though its reach/push tasks narrow rather than close the contact-precise side.
   - *Row*: PointAction.
   - *Falsifier*: the decoder swap costs as much as the representation swap → factorization, not geometry, is the driver.
5. **H5 — A native point head beats the strongest latent-geometry policy on the geometry-bound split, not on ID.**
   - *Prediction*: against [[2602.10098|VLA-JEPA]] (97.2% LIBERO) and [[2606.04436|3DThinkVLA]] (81.0% LIBERO-Plus), the point head ties on ID LIBERO but exceeds on LIBERO-Plus perturbation, where explicit metric structure beats distilled latent priors.
   - *Test*: head-to-head on LIBERO (ID) and LIBERO-Plus (OOD) at matched data.
   - *Row*: VLA-JEPA / 3DThinkVLA.
   - *Falsifier*: latent priors match the point head on OOD → explicit points add nothing the latent can't distill.

> [!warning] Risks
> - **Point clouds need depth sensing or reconstruction** that may be noisy or unavailable at deploy. → Lean on the predicted-pointmap path ([[2606.03943|PointAction]]) so geometry is *generated*, not sensed, removing the hard depth-sensor dependency.
> - **The advantage may vanish on in-distribution benchmarks** where RGB backbones already saturate (LIBERO ~97%). → Design evaluation around the appearance-shift / cross-embodiment splits where H1/H5 predict the gap appears; treat ID parity as expected, not failure.
> - **Full 3D branches add latency and parameters.** → H3's minimal-sufficient-geometry sweep + A3's depth-token bridge as the lightweight fallback if full point branches don't pay their compute.

### A2 — Occupancy-Forecasting as the Policy's Forward Model

| | |
|---|---|
| **Cluster** | A — Geometry-Native Policies |
| **Thesis** | Planning needs to know *what space will be filled*, not *what the scene will look like* — a voxel grid answers that directly, while pixels make you re-infer geometry every step. The field defaults to pixel forward models because that's what video foundation models predict; occupancy world models matured in driving and were never ported to tabletop. The bet is in First-principles below. |
| **Anchor papers** | [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2506.20134\|3D World Models Survey]] (survey), [[2603.28887\|OccSim]] (method), [[2510.10125\|CTRL-WORLD]] (method) |
| **Key targets** | Stable rollout ≥3,000 frames / ≥4 km ([[2603.28887\|OccSim]]); +22.1% relative mIoU vs asset-based sim; 67% zero-shot; manipulation port: beat a pixel-world-model baseline on geometry-bound [[2406.02523\|RoboCasa]] tasks, scored via [[2604.19092\|RoboWM-Bench]]'s WM→executable-action→step+final SR (more discriminative than perceptual-plausibility metrics) |

**Why it matters.**
- **The gap**: model-based control needs a forward model, and the default is a pixel-space video predictor the policy must re-parse into geometry every step — so drift piles up fast (pixel/occupancy WMs in driving were "limited to fewer than 50 frames," per [[2603.28887|OccSim]]).
- **Today's answers**: occupancy-as-manipulation-forward-model is *not* new — [[2203.06856|ACID]] (RSS'22) already rolled an implicit occupancy+flow forward model in a goal-conditioned manipulation loop (+30% SR over the strongest baseline, sim→real on plush toys), and [[2505.16249|3D-Occ-MPC]] (RA-L'25) ran explicit occupancy → learned dynamics → predictive control on elasto-plastic objects (occupancy-state EMD **28.6e-3** vs patch/crop baselines). What persists in pixels: [[2510.10125|CTRL-WORLD]] makes the pixel forward model controllable (38.7→83.4% on unseen objects); [[2506.23135|RoboScape]] augments it with temporal depth + keypoint dynamics (91% Robomimic on 200 synthetic trajectories). None of the occupancy prior runs the dense-voxel-vs-pixel-WM *horizon-to-divergence* head-to-head at RoboCasa scale.
- **The opening**: [[2603.28887|OccSim]] forecasts *occupancy* — an explicit voxel-semantic grid — with a Warp-DiT block that bounds geometric error via 3D rigid transforms, sustaining 3,000+ stable frames over 4+ km (**80×** the prior <50-frame ceiling) and lifting downstream forecasting **+22.1%** relative mIoU (67% zero-shot). The horizon ceiling the field treats as inherent is a *property of the pixel substrate*, removable.

**First-principles framing.**
- **First principle**: a planner needs to know which regions of space will be occupied (collision-freedom, contact, reachability) — a voxel grid answers that directly. Pixels are a lossy, view-dependent re-encoding of the same geometry; occupancy is the planning-native state.
- **Assumption being challenged**: that a manipulation forward model should predict pixels (the [[2510.10125|CTRL-WORLD]] / video-WM convention) because that's what video foundation models predict. [[2603.28887|OccSim]]'s 80× horizon gain shows the pixel substrate is itself the *source* of the drift, and rigid-body forecasters like [[2605.09196|RigidFormer]] (8× faster than FIGNet, stable to 217 objects) confirm explicit geometric state forecasts further than pixels. (That occupancy-is-the-planning-native-state is *settled* — [[2203.06856|ACID]], [[2505.16249|3D-Occ-MPC]] — so the contest is the *dense-explicit-voxel substrate at RoboCasa scale*, not the implicit-field/single-object regime they covered.)
- **The bet**: a *dense explicit* voxel-occupancy forward model — beyond [[2203.06856|ACID]]'s implicit field and [[2505.16249|3D-Occ-MPC]]'s single-object grid — holds geometric stability an order of magnitude longer than a pixel-WM baseline at RoboCasa scale (rollout-horizon-to-divergence ≥10× the pixel baseline), its Warp-DiT error bound survives down to sub-cm resolution, and its *forecast* occupancy can condition A1's point head to close a fully-geometric perceive-imagine-act loop that beats present-frame-only conditioning on long-horizon SR — none of which any single occupancy-manipulation paper has run.

**Related research papers.** One table on the axis the direction turns on — *the forward-model substrate the planner rolls forward* (occupancy-voxel / pixel-video / rigid-body / depth-augmented / latent-4D) — with `Key result` and what each leaves missing for a manipulation planner.

| System | Forward-model substrate | Key result | What's missing |
|---|---|---|---|
| [[2603.28887\|OccSim]] | voxel-semantic occupancy + Warp-DiT rigid-transform bound | **3,000+** stable frames, **4+ km**, **+22.1%** rel mIoU, **67%** zero-shot | a driving result — never ported to sub-cm tabletop occupancy |
| [[2203.06856\|ACID]] | implicit occupancy + flow forward model (goal-conditioned) | **55.6%** SR (**+30%** over best baseline) on unseen deformable manipulation, sim→real | establishes occupancy-as-forward-model for manipulation (2022), but *implicit* field, plush-deformable-specific, no horizon-to-divergence vs pixel WM |
| [[2505.16249\|3D-Occ-MPC]] | explicit occupancy → learned dynamics → MPC | occupancy state EMD **28.6e-3** / DCD **34.5e-4** (beats patch/crop), elasto-plastic sim+real | runs the in-loop explicit-occupancy control A2 proposes, but single-object/elasto-plastic, no RoboCasa-scale ≥10× horizon claim, no A1-head conditioning |
| [[2505.05512\|Occupancy World Model]] | autoregressive indoor occupancy forecasting | **+22.34** IoU / **+12.21** mIoU next-state, **+19.48**/**+11.61** autoregressive | ports occupancy WM driving→indoor (the scale move A2 needs), but a scene forecaster, not a manipulation control loop |
| [[2506.23126\|ParticleFormer]] | particle/point forward dynamics + MPC | superior MSE/CD dynamics, robust to hyperparams, lower MPC final-state error | particle (not dense-voxel-occupancy) substrate — the point-set alternative to A2's grid; no occupancy horizon-to-divergence |
| [[2506.23135\|RoboScape]] | physics-informed RGB + temporal depth + keypoint dynamics | **91%** Robomimic (200 synthetic trajectories), **0.953** Pearson real-SR | depth-augmented but still pixel-anchored — geometry not the native state |
| [[2605.09196\|RigidFormer]] | transformer rigid-body dynamics forecaster | **0.161 m / 15.33°** MOVi-B error, **23.9** FPS (8× FIGNet), stable to 217 objects | object-level rigid bodies, not a dense occupancy field the planner queries |
| [[2604.22152\|dWorldEval]] | pixel-video drift-over-horizon evaluator (benchmark) | LPIPS **0.243** at 20-step round-trip horizon (beats drifting baselines), policy-ranking Pearson **~0.9–0.92** | standardizes the drift-over-horizon measurement A2 borrows from driving, but pixel substrate — cannot score *geometric* divergence; the metric vehicle for H1's frames-to-divergence axis |
| [[2504.20995\|TesserAct]] | 4D RGB-D-N world model | depth+normal channels sharpen action prediction | the depth-augmented midpoint — geometry is a channel, not the substrate |
| [[2604.16484\|DexWorldModel]] | O(1)-memory latent dexterous WM | constant-memory rollout over 2,000 steps | latent, not explicit — the efficiency budget the occupancy loop must respect |
| [[2604.26694\|X-WAM]] | latent-4D unified WAM (sibling C3) | Chamfer **0.0049** vs 0.0680, 15 Hz | internal latent the planner can't read directly — A2's delta is *external* occupancy |
| [[2510.16732\|World Models for Embodied AI Survey]] | latent → token → explicit-3D taxonomy | locates occupancy at the explicit end of the spectrum | a map, not a manipulation forward model |
| [[2406.02523\|RoboCasa]] | the proposed target suite | geometry-bound long-horizon kitchen tasks where pixel WMs drift | no occupancy-loop baseline exists on it yet — the gap A2 fills |
| [[2410.00425\|ManiSkill3]] | GPU contact-rich manipulation | the sub-cm contact-precision stress test | tests policies, not forward-model horizon stability |

**Hypotheses & tests.** The FP bet — a *dense explicit* voxel substrate beats pixels on horizon at RoboCasa scale, holds sub-cm, and conditions A1's head — decomposed. (That occupancy-is-the-forward-model-state is settled by [[2203.06856|ACID]] / [[2505.16249|3D-Occ-MPC]]; the front-line is the dense-voxel/scale/conditioning conjunction nobody has run.)
1. **H1 — A dense voxel-occupancy inner loop beats the pixel inner loop on horizon-to-divergence at RoboCasa scale.**
   - *Prediction*: swapping a manipulation WM's pixel-prediction loop for a *dense-voxel* occupancy loop (backbone fixed) raises rollout-horizon-to-geometric-divergence ≥10× — beyond what [[2203.06856|ACID]]'s implicit field or [[2505.16249|3D-Occ-MPC]]'s single-object grid demonstrated — and the 80× driving gain partially survives the scale change.
   - *Test*: matched-backbone dense-occupancy-vs-pixel forward models on [[2406.02523|RoboCasa]], hosting both WM contestants on [[2604.19092|RoboWM-Bench]]'s shared WM→action→step+final SR scorecard (its discriminative-power finding — execution accuracy varies even at high perceptual scores — is exactly the fixed-horizon-SR-hides-stability claim) and comparing the two inner loops in genuine closed loop via [[2510.18135|World-in-World]] (counterfactual rollout → revision policy → task SR, manipulation in its suite); measure frames-to-divergence + downstream SR.
   - *Row*: OccSim / CTRL-WORLD / 3D-Occ-MPC.
   - *Falsifier*: occupancy ≤ pixel horizon at RoboCasa scale → the driving gain is scale-specific and ACID/3D-Occ-MPC's single-object result doesn't densify.
2. **H2 — The Warp-DiT error bound is resolution-portable to sub-cm.**
   - *Prediction*: the rigid-transform error bound holds at sub-cm voxel resolution needed for contact-precise manipulation, not just meter-scale driving; the bound degrades gracefully, not catastrophically, as resolution tightens.
   - *Test*: sweep voxel resolution on a contact task; report the resolution at which the bound breaks.
   - *Row*: OccSim.
   - *Falsifier*: the bound collapses below meter-scale → occupancy doesn't transfer to manipulation precision.
3. **H3 — Decoupling the dynamic agent stabilizes object-motion forecasting.**
   - *Prediction*: applying [[2603.28887|OccSim]]'s static-scene / dynamic-agent decoupling to manipulation (object+gripper = dynamic agent) lowers object-motion forecast error vs a monolithic occupancy predictor.
   - *Test*: ablate the decoupling on a pick-place occupancy forecaster.
   - *Row*: OccSim / RigidFormer.
   - *Falsifier*: the monolithic predictor matches the decoupled one → the static/dynamic split is driving-specific.
4. **H4 — Predicted future-occupancy can condition A1's action head directly.**
   - *Prediction*: feeding A2's forecast occupancy into A1's point-cloud head closes a fully-geometric perceive-imagine-act loop that beats the same head on present-frame geometry alone on long-horizon tasks.
   - *Test*: condition the A1 head on forecast vs present occupancy; report long-horizon SR on [[2510.18135|World-in-World]]'s closed-loop embodied-utility protocol (WM counterfactual rollout → plan selection → task success), the standardized inner-loop substrate the perceive-imagine-act comparison otherwise lacks.
   - *Row*: OccSim / DexWorldModel.
   - *Falsifier*: forecast conditioning ≤ present-frame → imagination adds nothing for the action head.
5. **H5 — Explicit occupancy beats the latent-4D substrate on horizon, not per-frame fidelity.**
   - *Prediction*: against sibling C3's [[2604.26694|X-WAM]] latent, the occupancy loop wins on frames-to-divergence while losing on per-frame Chamfer — confirming the two are complementary substrates, not competitors.
   - *Test*: matched-task occupancy vs X-WAM latent; report (horizon, Chamfer) jointly.
   - *Row*: X-WAM / OccSim.
   - *Falsifier*: occupancy also wins per-frame Chamfer → the substrates are redundant, not complementary.

> [!warning] Risks
> - **Cross-domain transfer may not hold** — driving occupancy is meter-scale and mostly-static; manipulation needs sub-cm dynamic occupancy. → H2's resolution sweep + H3's dynamic-agent analog are the explicit go/no-go; report the scale at which the Warp-DiT bound breaks.
> - **Occupancy ground truth is scarce in manipulation datasets.** → Derive occupancy from depth + known gripper geometry (as driving derives it from LiDAR), or pretrain the forecaster in sim where occupancy is free.
> - **Voxel grids are memory-heavy at sub-cm resolution.** → Sparse/hierarchical occupancy (octree) + bound the claim to the working-volume around the end-effector rather than the full scene.

### A3 — Depth-Token Bridges: 3D-Awareness into Pretrained 2D Policies Without Re-Training

| | |
|---|---|
| **Cluster** | A — Geometry-Native Policies |
| **Thesis** | A 2D policy's geometry deficit is a *missing channel*, not a *wrong backbone* — so a cheap depth-token side-input can supply it without disturbing the pretrained semantic alignment. The field assumes 3D-awareness needs a full parallel 3D branch and re-training, forcing a false choice between RGB-only (cheap, geometry-blind) and full-3D (capable, expensive). The bet is in First-principles below. |
| **Anchor papers** | [[2504.05786\|3D Spatial Reasoning in LLM Survey]] (survey), [[2506.20134\|3D World Models Survey]] (survey), [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2306.03310\|LIBERO]] (benchmark), [[2510.14836\|QDepth-VLA]] (method), [[2508.09071\|GeoVLA]] (method) |
| **Key targets** | +8.8% LIBERO-Spatial, +29.7% long-horizon over open_pi_0, +10–20% real-robot ([[2510.14836\|QDepth-VLA]], single-view) on [[2306.03310\|LIBERO]]'s 4-suite SR (SPATIAL/OBJECT/GOAL/100); recover ≥80% of [[2508.09071\|GeoVLA]]'s full-3D-branch gain (97.7% LIBERO) at side-channel cost; alignment-preservation tracked via [[2505.05456\|SITE]]'s spatial-VQA→LIBERO-Spatial-SR correlation (**0.902** Pearson) |

**Why it matters.**
- **The gap**: A1 and A2 buy geometry by changing the architecture — a parallel point branch or an occupancy loop — but that strands the huge installed base of RGB-pretrained policies that already work and that nobody wants to re-train.
- **Today's answers**: the frozen-backbone 3D bolt-on is *already established* — [[2503.07511|PointVLA]] freezes the action expert and injects 3D via a lightweight modular block with no retraining (skip-block analysis to minimize disruption), explicitly motivated by not stranding the 2D-pretrained installed base; [[2510.13375|DepthVLA]] runs the twin depth-expert stream (94.9% LIBERO, 74.8% SimplerEnv); [[2408.05107|Depth Helps]] (DI², IROS'24) already quantization-denoises depth on LIBERO (63.15% RGB-only, only **0.8%** below its RGB-D variant). At VLA scale: [[2510.14836|QDepth-VLA]] feeds depth as discrete VQ-VAE tokens to a depth-expert reading the VLM's vision features (+8.8% LIBERO-Spatial, +29.7% long-horizon over `open_pi_0`, single-view); [[2605.14950|Evo-Depth]] injects implicit depth via FiLM (95.4% LIBERO, 0.9B at 12.3 Hz); [[2606.03240|GeoAlign]] trains a depth encoder dropped at execution (99.0% LIBERO). None measure the *recovery-fraction frontier* against a full-3D branch on a common backbone, nor the *alignment-preservation* number.
- **The opening**: [[2510.12276|Spatial Forcing]] aligns VLA features to a 3D foundation model with *no 3D at inference*, hitting 98.5% LIBERO at 3.8× faster training / 5.9× more data-efficiency — proof the geometry can be a frozen-backbone side-task, not a parallel stream.

**First-principles framing.**
- **First principle**: a 2D policy's spatial weakness is a *missing channel* (depth), not a corrupted representation. Adding the channel as discrete tokens through a decoupled expert supplies the metric cues — you don't rebuild the backbone to add a channel. The biology read: depth is layered on as an early, cheap channel, not a separate stream re-learned from scratch.
- **Assumption being challenged**: that real 3D-awareness needs a full parallel 3D branch and joint re-training is *already refuted* — [[2503.07511|PointVLA]] froze the backbone and bolted on 3D with no retraining, [[2408.05107|Depth Helps]] showed quantized depth costs only 0.8% to drop at inference, [[2510.12276|Spatial Forcing]] / [[2605.10485|VEGA]] distill geometry at *zero* inference overhead. So the cheap/expensive split is *settled false*. The open assumption A3 now attacks: that "a depth bridge helps" is a sufficient claim — it isn't, because nobody has drawn the cost-efficiency frontier or measured the alignment cost the side-channel was *assumed* to avoid.
- **The bet**: the deliverable is the *measurement* nobody has produced, not the existence claim PointVLA settled — specifically, (i) on one common backbone the recovery-fraction-vs-added-params curve for a depth-token bridge has a clear *knee* recovering ≥80% of [[2508.09071|GeoVLA]]'s full-3D-branch SR gain well below full-branch cost (no found paper plots this), and (ii) the frozen-backbone side-channel perturbs a held-out VQA semantic-alignment probe *measurably less* than full-branch fusion that backprops into the backbone — the alignment-preservation cost everyone assumed but [[2503.07511|PointVLA]] never numbered.

**Related research papers.** One table on the axis the direction turns on — *where and how the geometry is injected into a pretrained 2D policy* (single-view depth token / FiLM implicit depth / train-time-only alignment / full-3D branch upper bound / SSL-backbone pretext) — with `Key result` and what each leaves missing.

| System | Injection point | Key result | What's missing |
|---|---|---|---|
| [[2510.14836\|QDepth-VLA]] | quantized depth tokens → decoupled depth expert (single-view) | **+8.8%** LIBERO-Spatial, **+29.7%** long-horizon, **+10–20%** real | never measured head-to-head vs a full-3D branch on one backbone — no recovery-fraction curve |
| [[2503.07511\|PointVLA]] | freeze action expert + lightweight modular 3D injection block, no retraining (skip-block) | beats 2D IL across tasks, long-horizon from **20** demos/task, cross-embodiment | states A3's mechanism + installed-base assumption verbatim, but *sensed* point clouds (not single-view depth tokens) and never plots the recovery-fraction-vs-full-branch knee or the alignment-drift number |
| [[2510.13375\|DepthVLA]] | parallel depth-expert stream beside the VLA | **94.9%** LIBERO, **74.8%** SimplerEnv WidowX (vs π0 58.8%), 79% real progress | the twin depth-expert, but a heavier parallel stream — no recovery-fraction-vs-cost frontier on a common backbone |
| [[2408.05107\|Depth Helps]] | depth-aware codebook (quantized depth), drop to RGB-only at inference | **63.15%** LIBERO RGB-only (only **0.8%** below RGB-D), 66.67% real | pre-answers H2 (quantization denoises depth) on LIBERO, but only one codebook setting — no capacity sweep, no full-branch ceiling |
| [[2605.14950\|Evo-Depth]] | implicit depth from multi-view RGB via FiLM (no sensor) | **95.4%** LIBERO, **90%** real, **0.9B** params at **12.3 Hz** | multi-view, and quantization-vs-FiLM contribution not isolated |
| [[2606.03240\|GeoAlign]] | depth encoder trained on RGB-D, dropped at execution | **99.0%** LIBERO, **78.8%** geometry-critical real (**+13.8 pp**) | geometry without sensing, but the alignment-preservation cost is unmeasured |
| [[2512.00903\|SwiftVLA]] | frozen-4D-VGGT spatiotemporal features distilled via mask-and-reconstruct, 4D branch dropped at inference | **94.7%** LIBERO, **0.53** RoboTwin 2.0 (vs SmolVLA 0.29), **18×** faster / **12×** less memory on Jetson Orin | train-time-only 4D, *spatiotemporal* not depth — recovery-fraction vs a full-3D branch unmeasured |
| [[2510.17439\|FALCON (Spatial VLA)]] | global 3D priors from RGB (optional depth/pose) into a Spatial-Enhanced Action Head, VLM alignment preserved | **70.0%** real cluttered (**+25.6%** over SpatialVLA), height-sensitive SR **60→80%** | injects into the head not the backbone (A3's alignment thesis), but on top of a full ESM, not a light side-channel |
| [[2510.12276\|Spatial Forcing]] | feature-alignment to a 3D foundation model, no 3D at inference | **98.5%** LIBERO, **3.8×** faster training, **5.9×** data-efficient | train-time alignment, not a deployable depth channel — different lever |
| [[2605.10485\|VEGA]] | cosine-distill a 3D-aware DINOv2-FiT3D teacher, no inference overhead | RoboTwin 2.0 **67.5%/30.7%** | distillation, not an explicit side-channel the policy can attend to |
| [[2605.30350\|DynaFLIP]] | tri-modal-dynamics-guided encoder, no inference 3D | highest-SR frozen backbone on MetaWorld/RLBench; best LIBERO mean w/ DP | geometry baked into the encoder — not a modular bolt-on bridge |
| [[2508.09071\|GeoVLA]] | full parallel 3D point branch (the upper bound) | **97.7%** LIBERO | the *expensive* ceiling A3 measures against; risks disturbing semantic alignment |
| [[2606.03943\|PointAction]] | predicted-pointmap interface | 43.0% zero-shot xArm7 | generated geometry, full-head — the architecture-change A3 avoids |
| [[2504.20995\|TesserAct]] | depth-as-predicted-channel (RGB-D-N) | depth channel sharpens grounding | predicts depth, doesn't inject sensed/quantized depth into a frozen head |
| [[2502.13143\|SoFar]] | orientation grounding from 2D | a lightweight side-signal sharpens manipulation | orientation only — not a metric depth channel |
| [[2605.09963\|Spatial Prediction SP]] | spatial pretext tasks on MAE/MoCo/DINO | **+8.0%** ImageNet-1K, jigsaw 69.87%→90.24%, lower texture bias | adds the spatial channel at the SSL-backbone layer, not the policy head |
| [[2605.24642\|GFM-VLA Study]] | Early/Late Fusion + Spatial Forcing comparison | maps how to bolt geometric-foundation-model features on | a survey of integration strategies, not a single recovery-fraction result |
| [[2602.10098\|VLA-JEPA]] | implicit geometry in a JEPA latent | **97.2%** LIBERO | the latent alternative the bridge competes with on cost, not an explicit channel |
| [[2501.15830\|SpatialVLA]] | RGB-token spatial policy (the bolt-on host) | the frozen backbone the depth bridge attaches to | leaves all depth implicit — the baseline the bridge improves |

**Hypotheses & tests.** The FP bet — the cost-efficiency frontier and alignment-cost nobody has measured, not "a depth bridge works" ([[2503.07511|PointVLA]] settled that) — decomposed. H1 (recovery-fraction knee) + H4 (alignment-preservation number) are the front-line; H2 is largely pre-answered by [[2408.05107|Depth Helps]] and re-run only to extend it to a capacity sweep.
1. **H1 — The recovery-fraction curve has a knee well below full-branch cost.**
   - *Prediction*: sweeping depth-token capacity (codebook size, expert depth) on one common backbone, the recovered fraction of [[2508.09071|GeoVLA]]'s full-3D-branch SR gain reaches ≥80% at a small fraction of the added parameters, with a clear knee — the frontier neither [[2503.07511|PointVLA]] nor [[2510.13375|DepthVLA]] plotted.
   - *Test*: capacity sweep on a common backbone; plot recovered-fraction vs added params on [[2306.03310|LIBERO]]-Spatial / long-horizon SR (the named suite the sweep is read off, against GeoVLA's full-3D ceiling).
   - *Row*: QDepth-VLA / GeoVLA / PointVLA.
   - *Falsifier*: recovery scales linearly to full-branch cost → no cheap operating point exists.
2. **H2 — Quantization, not just the decoupled expert, drives the noise-robustness gain (extend pre-answered).**
   - *Prediction*: [[2408.05107|Depth Helps]] already shows quantized depth costs only 0.8% to drop; extending to a 2×2 (quantized vs continuous depth) × (decoupled vs fused expert) ablation, quantization contributes a *separable* robustness gain beyond the expert across a capacity range.
   - *Test*: the 2×2 on [[2510.14836|QDepth-VLA]]'s setup under depth-estimator noise, sweeping codebook size.
   - *Row*: QDepth-VLA / Depth Helps / Evo-Depth.
   - *Falsifier*: continuous-depth matches quantized at equal expert across the sweep → quantization is incidental beyond Depth Helps' single setting.
3. **H3 — A second view's depth tokens close the residual gap to full-3D.**
   - *Prediction*: single-view depth-token gain saturates below the full-3D ceiling; adding a second view's depth tokens closes most of the residual to methods that consume sensed point clouds.
   - *Test*: single-vs-two-view depth tokens vs a sensed-point-cloud full-3D method.
   - *Row*: QDepth-VLA / GeoVLA.
   - *Falsifier*: a second view doesn't help → the bridge ceiling is intrinsic, not view-limited.
4. **H4 — The side-channel perturbs semantic alignment far less than full-branch fusion.**
   - *Prediction*: [[2505.05456|SITE]]'s spatial-VQA probe shows the frozen-backbone depth expert perturbs semantic alignment measurably less than full-branch fusion that backprops into the backbone — and because SITE's CAA tracks LIBERO-Spatial manipulation SR at **0.902** Pearson, the probe drift it measures demonstrably predicts the downstream SR the side-channel must not damage.
   - *Test*: [[2505.05456|SITE]] spatial-VQA-probe drift, depth-expert vs full-branch fusion, same data.
   - *Row*: QDepth-VLA / GeoVLA.
   - *Falsifier*: the side-channel perturbs alignment as much as fusion → the "non-disruptive" claim fails.
5. **H5 — Train-time-only distillation matches the inference depth channel on geometry-bound tasks.**
   - *Prediction*: [[2510.12276|Spatial Forcing]]-style train-time alignment recovers a comparable fraction of the full-3D gain to QDepth-VLA's inference channel on geometry-critical tasks, at *zero* inference cost — so the cheapest deployable form needs no depth at test; [[2512.00903|SwiftVLA]]'s mask-and-reconstruct distillation (94.7% LIBERO with the 4D branch dropped) extends this to *spatiotemporal* (not just depth) features, predicting the dropped channel can be richer than depth without an inference cost.
   - *Test*: train-time-distill ([[2510.12276|Spatial Forcing]] depth, [[2512.00903|SwiftVLA]] spatiotemporal) vs inference-depth-token on geometry-critical real tasks at matched backbone.
   - *Row*: Spatial Forcing / SwiftVLA / QDepth-VLA.
   - *Falsifier*: train-time alignment underperforms the inference channel materially → depth must be present at inference.

> [!warning] Risks
> - **The bridge may plateau below the full-3D ceiling** on the hardest geometry-bound tasks. → H1's recovery-fraction curve sets an honest expectation — frame the contribution as a *cost-efficiency frontier*, not SR-SOTA; concede the ceiling where it appears.
> - **Depth-token quality depends on the depth estimator.** → [[2510.14836|QDepth-VLA]]'s quantization buffers estimator noise (H2); report sensitivity to estimator quality so the claim is bounded to realistic depth.
> - **Side-channel may still subtly perturb semantic alignment.** → H4's VQA-probe quantifies the perturbation; gate the "non-disruptive" claim on it rather than assuming the frozen backbone is untouched.

---

## Cluster B — Spatial Reasoning as a 3D-Grounded Cognition Layer

*Reasoning happens over explicit metric geometry, upstream of the action head — the policy acts on the output of a 3D-grounded cognition step, not on raw RGB. The two directions are the spatial and temporal halves of the same layer: a scene-graph that grounds *where* objects are (B1) and a 4D-consistency constraint that keeps that geometry coherent *over time* (B2), each feeding the metric structure the action heads downstream consume.*

### B1 — Explicit 3D Scene-Graph CoT for Metric Spatial Reasoning

| | |
|---|---|
| **Cluster** | B — 3D-Grounded Cognition |
| **Thesis** | Metric spatial relations are a *graph over geometric entities*; free-form language CoT only describes that graph lossily and hallucinates when ungrounded. The MLLM field trusts language CoT over RGB and assumes scale alone closes the spatial gap. The bet is in First-principles below. |
| **Anchor papers** | [[2504.05786\|3D Spatial Reasoning in LLM Survey]] (survey), [[2506.20134\|3D World Models Survey]] (survey), [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2507.13362\|VLM Spatial Reasoning RL]] (method), [[2501.10074\|SpatialCoT]] (method), [[2601.13304\|CausalSpatial]] (benchmark) |
| **Key targets** | CVBench ≥77.69% ([[2507.13362\|VLM Spatial Reasoning RL]]); per-relation-type metric-spatial-QA on [[2412.07825\|3DSRBench]] (12 question types / 4 categories, FlipEval+CircularEval bias controls, 6D-viewpoint OOD split, human **95.7%** vs LMM **52.0–60.3%**); manip SR ≥82.57% / nav SR ≥61.83% ([[2501.10074\|SpatialCoT]]); close part of the [[2601.13304\|CausalSpatial]] 54.17%→84.49% human gap |

**Why it matters.**
- **The gap**: [[2504.05786|3D Spatial Reasoning in LLM Survey]] and [[2601.13304|CausalSpatial]] reach the same diagnosis — MLLMs don't reason about metric space, they *describe* it in language and hallucinate when ungrounded; on causal tasks (collision, occlusion, trajectory) GPT-5 scores 54.17% vs human 84.49% and is overconfident (low Not-Sure-Rate).
- **Today's answers**: the structure-first + RL + anti-shortcut-OOD recipe is *already demonstrated* — [[2601.01984|Thinking with Blueprints]] builds an explicit structured spatial representation, reasons over it, and adds RL rewards + anti-shortcut augmentation (92.7% SAT-val, **79.7%** SAT-test OOD, +16.4% over base), and [[2512.16909|MomaGraph]] predicts a scene-graph via RL with edge-level reward (71.6% MomaGraph-Bench, 70% real long-horizon SR). [[2507.13362|VLM Spatial Reasoning RL]] decomposes the scene into a relational graph before answering (77.69% CVBench, +19.5% Depth-OOD where SFT degrades); [[2501.10074|SpatialCoT]] pushes it into action via coordinate alignment (82.57% manip). None isolate whether the gain is the *metric* edges vs topological ordering, nor instrument graph-construction accuracy as the bottleneck.
- **The opening**: [[2604.24300|ReVSI]]'s dummy-video stress test shows fine-tuned models catastrophically hallucinate *absent* objects, and [[2605.30161|Why Far Looks Up]] traces a "vertical-distance entanglement" shortcut (36.9 pp gap) — proof the deficit is a *missing metric representation* a scene-graph supplies, not a data shortage.

**First-principles framing.**
- **First principle**: spatial relations form a graph over geometric entities (objects with metric positions, pairwise relations, contacts). Reasoning correctly *is* operating on that graph; language is a lossy serialization that drops the metric structure the task needs. [[2503.11089|EmbodiedVSR]]'s dynamic scene-graph + physics-constrained CoT (+18.4% Arm Feasibility, 80% real reassembly) shows the graph, made explicit, is what carries the gain.
- **Assumption being challenged**: the scaling view that a big-enough multimodal model reasons about space implicitly is *already refuted* — [[2507.13362|VLM Spatial Reasoning RL]] shows naive CoT can *hurt* and only *structured* scene-graph CoT helps; [[2601.13304|CausalSpatial]] shows even GPT-5 sits 30 points below humans. And the *structure+RL+OOD-generalizes* claim is now consensus too ([[2601.01984|Thinking with Blueprints]], [[2512.16909|MomaGraph]]). The open assumption B1 attacks: that adding *any* graph is what matters — when the untested question is *which property of the graph* (metric edges vs topological ordering) carries the gain, and *where* the graph fails (construction vs reasoning).
- **The bet**: the gain is carried by *metric* content, not graph topology, and bottlenecked by *construction*, not reasoning — neither isolated by [[2601.01984|Thinking with Blueprints]] or [[2512.16909|MomaGraph]]. Specifically, (i) a scene-graph with metric edge labels (distances, angles) beats a purely topological graph on CVBench, with the gap concentrated in metric-relation question types and ≈0 on object-naming; and (ii) when scene-graph CoT errs on the [[2601.13304|CausalSpatial]] 54.17%→84.49% causal slice, most errors trace to a *wrong graph* (hallucinated/missing entity), so graph-construction accuracy predicts answer accuracy.

**Related research papers.** One table on the axis the direction turns on — *how the spatial representation upstream of the answer is structured* (metric scene-graph / topological relations / depth-rationale / simulate-then-reason / symbolic state / 3D-proxy tokens / reconstructed-3D / diagnostic) — with `Key result` and what each leaves missing. The diagnostic rows prove the gap is metric; the method rows attack it with structure.

| System | Spatial representation | Key result | What's missing |
|---|---|---|---|
| [[2507.13362\|VLM Spatial Reasoning RL]] | explicit metric scene-graph + GRPO | **77.69%** CVBench (+5–15%), **+19.5%** Depth-OOD where SFT degrades | doesn't separate metric-edge from topological-edge contribution |
| [[2601.01984\|Thinking with Blueprints]] | explicit structured spatial representation + RL reward + anti-shortcut aug | **92.7%** SAT-val, **79.7%** SAT-test OOD (+16.4% over base), 60.7% BLINK, 7B | records positions/sizes + RL-OOD (settles B1's H2), but never decomposes metric-vs-topological gain, nor instruments construction accuracy |
| [[2512.16909\|MomaGraph]] | scene-graph prediction via RL with edge-level reward | **71.6%** MomaGraph-Bench, **+4.8%** BLINK, **70%** real long-horizon SR | RL over a learned graph with edge reward, but no metric-edge isolation (H1) and no causal-task split (H3) |
| [[2603.22279\|3D-Layout-R1]] | RL-tuned 3D layout reasoning (IoU/collision reward) | **+15%** Mean IoU, **1.000** Collision-Free on Sorting, 7B/8B ≥ commercial | layout-as-RL-target, but layout-only — not a relational metric scene-graph with contact edges |
| [[2501.10074\|SpatialCoT]] | coordinate-aligned CoT (language→coords) | **82.57%** manip / **61.83%** nav SR | the B→A handoff, but never benchmarked vs a geometric action head |
| [[2503.11089\|EmbodiedVSR]] | dynamic scene-graph + physics-constrained CoT | **+18.4%** Arm Feasibility over GPT-4o, **80%** real reassembly | scene-graph for robots, but graph-construction accuracy not reported separately |
| [[2601.11442\|Map2Thought]] | metric cognitive map (symbolic grid + continuous metric scale) + deterministic geometric Cog-CoT | **61.0%** VSI-Bench (top open-source), **59.9%** at half the data | a *map* not a relational graph — verifiable on metric queries, but no pairwise contact/relation edges |
| [[2505.20279\|VLM-3R]] | reasoning over reconstructed 3D | grounds reasoning in reconstructed geometry | reconstruction cost; not a lightweight graph |
| [[2506.04220\|Struct2D]] | structured 2D → spatial reasoning | cheap structure without full 3D | 2D structure — leaves the metric-vs-topological question open |
| [[2605.08064\|Proxy3D]] | compact semantically-clustered 3D proxy tokens | **700 vs 8000** tokens, efficient metric-3D interface | a token interface, not a reasoned relational graph |
| [[2605.06758\|R3L]] | relative-relation invariant decomposition + consistent imagination | **0.0%** collision/out-of-bound, **1.8×** faster convergence | metric scene-graph *construction*, but layout-only, not full CoT |
| [[2606.06076\|MGSD]] | symbolic-state self-distillation for visual planning | **11.2%→30.5%** on FrozenLake/Maze/MiniBehaviour | symbolic state for planning — not metric 3D relations |
| [[2507.12508\|MindJourney]] | simulate-then-reason via controllable video WM | SAT-Real o1 **74.6%→84.7%** | imagination at test time; gain depends on the WM, not a graph |
| [[2604.26934\|World2VLM]] | distilled WM imagination into the VLM (GRPO) | **+15.44–15.98 pp** across 4 spatial benchmarks | internalizes simulate-then-reason — but no explicit relational graph |
| [[2606.03988\|Imaginative Perception Tokens]] | flow-matching tokens simulate unobserved views | **67.3%** Multiview Counting, beats textual CoT; gains persist w/o inference gen | view simulation, not metric relational structure |
| [[2605.18162\|SAGE]] | self-evolving geometric-logic duality + GRPO | **+15.0** MindCube at **<37%** of the data | targets "pseudo-understanding" via RL, but not a metric graph per se |
| [[2604.14144\|SpatialEvo]] | deterministic geometric environment for RL labels | **54.7** avg (7B), **−5.1 pt** without DGE GT | structure-as-supervision, but the graph isn't the reasoning substrate |
| [[2505.12448\|SSR]] | raw depth → structured rationales → compact latents | **+13.6%** spatial accuracy, CoT cost **23.16s→0.32s** | depth-grounded rationale (B1×A3 tie) — not a relational scene-graph |
| [[2506.03135\|OmniSpatial]] | comprehensive spatial-reasoning benchmark + built-in PointGraph scene-graph baseline | **>56%** top VLM vs human **92.6%** (30-pt gap); Complex-Spatial-Logic **30–40%**; PointGraph + SpatialCoT boost, SFT **+7.82** avg | a standardized suite where B1's metric-vs-structure comparison runs against a *built-in* scene-graph baseline, but reports answer accuracy, not graph-construction accuracy (H5) |
| [[2605.29074\|Embodied3DBench]] | metric-3D perception suite (3D bbox / object point / grasp point) + View-Augmented-CoT | 13 VLMs, none robust on low-level metric 3D; score correlates with downstream LIBERO SR | the load-bearing metric-3D substrate for the reasoning-vs-perception split (H3), but a diagnostic, not a deployable graph layer |
| [[2601.13304\|CausalSpatial]] | causal-spatial diagnostic + COW visual simulation | GPT-5 **54.17%** vs human **84.49%**; visual sim suppresses hallucination | measures the gap; the COW is a probe, not a deployable graph layer |
| [[2604.24300\|ReVSI]] | dummy-video hallucination stress test | fine-tuned models hallucinate absent objects catastrophically | a diagnostic — exposes shortcut-vs-metric, prescribes no fix |
| [[2605.30161\|Why Far Looks Up]] | vertical-distance-entanglement probe | **36.9 pp** shortcut gap (consistent vs counter) | proves reasoning is shortcut, not metric — no remedy |
| [[2605.30557\|SpatialUncertain]] | unanswerable-question calibration probe | overconfident: **~30%** occlusion, **<10%** perspective ambiguity | the calibration half of the gap; no grounding mechanism |

**Hypotheses & tests.** The FP bet — explicit metric scene-graph CoT + RL grounding closes the causal slice of the human gap — decomposed.
1. **H1 — Metric edges, not topological relations, carry the gain.**
   - *Prediction*: a scene-graph with metric edge labels (distances, angles) beats a purely topological graph (left-of, on-top-of) on CVBench, with the gap concentrated in metric-relation question types.
   - *Test*: ablate metric-vs-topological edges on [[2507.13362|VLM Spatial Reasoning RL]]; decompose gains by relation type over [[2412.07825|3DSRBench]]'s 12-question-type / 4-category split (its FlipEval directly tests the left/right topological shortcut to dissociate from metric content, and its 6D-viewpoint OOD split doubles as the H2 OOD substrate CVBench lacks).
   - *Row*: VLM Spatial Reasoning RL.
   - *Falsifier*: topological edges match metric edges → the win is structure, not metric content.
2. **H2 — RL grounding transfers the scene-graph habit OOD better than SFT (settled prior, re-confirm on causal-OOD).**
   - *Prediction*: GRPO-grounded scene-graph CoT generalizes to [[2601.13304|CausalSpatial]]'s causal tasks where SFT-trained CoT degrades, replicating the +19.5% Depth-OOD pattern — already demonstrated in general OOD by [[2601.01984|Thinking with Blueprints]] (79.7% SAT-test) and [[2512.16909|MomaGraph]]; B1 only re-confirms it on the *causal* slice those papers didn't isolate.
   - *Test*: RL vs SFT on the same scene-graph backbone, evaluated on held-out causal tasks.
   - *Row*: VLM Spatial Reasoning RL / Thinking with Blueprints / CausalSpatial.
   - *Falsifier*: SFT matches RL on causal-OOD → grounding is prompt-tuning, not a transferable habit.
3. **H3 — The residual human gap is reasoning-bound on trajectory, perception-bound on occlusion.**
   - *Prediction*: decomposing the 30-point gap by task, scene-graph CoT closes most of the *trajectory* slice (reasoning) but little of the *occlusion* slice (perception/depth).
   - *Test*: per-task (collision/occlusion/trajectory) gain measurement on CausalSpatial, extended by [[2506.03135|OmniSpatial]]'s per-dimension split (Complex-Spatial-Logic 30–40% = reasoning-bound vs Perspective-Taking/perception = perception-bound) for a standardized reasoning-vs-perception decomposition beyond CausalSpatial's slice.
   - *Row*: CausalSpatial / Embodied3DBench / OmniSpatial.
   - *Falsifier*: uniform closure across tasks → the gap isn't split reasoning-vs-perception.
4. **H4 — Upstream scene-graph grounding partially substitutes for downstream geometry.**
   - *Prediction*: feeding [[2501.10074|SpatialCoT]]'s reasoned coordinates into a simpler RGB action head recovers a measurable fraction of A1's point-cloud-head SR on geometry-bound tasks — but not all of it, leaving a residual only sensed geometry closes.
   - *Test*: scene-graph-coords + RGB head vs A1 point head on matched tasks.
   - *Row*: SpatialCoT.
   - *Falsifier*: upstream grounding fully matches the point head → downstream geometry is redundant (collapses A1 into B1); or recovers ≈0 → reasoning doesn't substitute at all.
5. **H5 — Graph-construction accuracy, not answer accuracy, is the failure bottleneck.**
   - *Prediction*: when scene-graph CoT errs, most errors trace to a wrong graph (hallucinated/missing entity), not wrong reasoning over a correct graph — so reporting graph-construction accuracy separately predicts answer accuracy.
   - *Test*: instrument graph-construction vs reasoning errors on [[2503.11089|EmbodiedVSR]] / [[2604.24300|ReVSI]] stress sets.
   - *Row*: EmbodiedVSR / ReVSI.
   - *Falsifier*: errors are evenly split construction-vs-reasoning → graph quality isn't the dominant lever.

> [!warning] Risks
> - **Scene-graph construction can itself hallucinate** — a wrong graph poisons downstream reasoning. → Ground the graph in B2's 4D-consistency / depth ([[2601.13304|CausalSpatial]]'s COW visual-simulation evidence), and report graph-construction accuracy separately from answer accuracy (H5).
> - **Gains may be benchmark-specific** (CVBench-tuned prompts don't transfer). → H2's RL-OOD protocol tests cross-benchmark transfer explicitly; treat GRPO as the generalization mechanism, not prompt-tuning.
> - **The human gap may be perception-bound, not reasoning-bound** — scene-graph CoT can't fix bad depth. → H3 separates perception from reasoning failure; if perception-bound, route to A3's depth bridge as the upstream fix.

### B2 — 4D-Consistent Policies: Spatio-Temporal Geometry as a Reasoning Constraint

| | |
|---|---|
| **Cluster** | B — 3D-Grounded Cognition |
| **Thesis** | For an action to be planned over a horizon, an object's geometry and identity must stay coherent across time and viewpoint — 4D consistency. The field forces a choice: stay 2D (cheap, inconsistent) or generate explicit future frames (expensive). The bet is in First-principles below. |
| **Anchor papers** | [[2506.20134\|3D World Models Survey]] (survey), [[2504.05786\|3D Spatial Reasoning in LLM Survey]] (survey), [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2603.22078\|WAM vs VLA Robustness]] (benchmark), [[2605.05126\|ConsisVLA-4D]] (method), [[2508.07917\|MolmoAct]] (method) |
| **Key targets** | LIBERO ≥98.1% ([[2605.05126\|ConsisVLA-4D]]); factor-decomposed OOD on [[2510.13626\|LIBERO-Plus]] (7 axes, isolated camera-viewpoint where SR drops 95%→<30%); real bimanual ≥70.0% (vs OpenVLA 28.5%) on [[2506.18088\|RoboTwin 2.0]] (5-dim DR, +24.4% real few-shot); 2.31× inference speedup / 1.36× training-cost cut; OOD SR ≥72.1% ([[2508.07917\|MolmoAct]]) |

**Why it matters.**
- **The gap**: a policy that plans over a horizon must keep an object's geometry and identity coherent across time and viewpoint — else the action it commits at step 1 is invalidated by a hallucinated scene at step 5; the field's two answers (projection-biased 2D, or expensive explicit future-frame generation) both fall short.
- **Today's answers**: each flank of the bet is already fenced. Viewpoint-OOD: [[2509.14117|GeoAware]] states B2's hypothesis verbatim — "generalization across views is tied to the geometric acuity of the visual encoder" — with an implicit/no-reconstruction route (**+35 pp** zero-shot unseen-viewpoint SR on LIBERO, 96.8% ID), but *spatial-only*, no temporal 4D. Temporal-consistency-as-in-policy-constraint: [[2605.21862|EvoScene-VLA]] (recurrent scene-prior + depth/3D anchors, 89.1% RoboTwin) and [[2602.20200|OptimusVLA]] (98.6% LIBERO, 2.9× speedup) already enforce it. [[2605.05126|ConsisVLA-4D]] enforces 4D coherence with *implicit* consistency attention (98.1% LIBERO, 70.0% real bimanual vs OpenVLA 28.5%, 2.31× faster); [[2508.07917|MolmoAct]] makes it *explicit and steerable* (72.1% OOD). None runs the consistency-vs-perception ablation (perception held fixed) over *full* space+time 4D.
- **The opening**: [[2603.25399|LaMP]] shows a dense 3D-scene-flow latent motion prior lifts LIBERO-Plus +9.7 pp over OpenVLA-OFT (79.3%) — a temporal-geometry constraint, not explicit frames, driving exactly the OOD robustness this direction predicts.

**First-principles framing.**
- **First principle**: for an action to be planned over a horizon, the imagined geometry must be *temporally and cross-view consistent* — the same object on a coherent 4D trajectory. Consistency is a constraint the representation must satisfy; it is not the same as rendering every intermediate frame. [[2604.08532|SelfEvo]] shows consistency can even be a *self-supervision* target (−19.7% depth AbsRel, +20.1% AUC@30 on new domains, no labels).
- **Assumption being challenged**: the either/or that you accept projection-biased 2D (OpenVLA-class) or pay for explicit future-frame generation ([[2604.26694|X-WAM]]-class) to get 4D consistency. [[2605.05126|ConsisVLA-4D]] gets explicit-3D accuracy *and* a 2.31× speedup with *implicit* consistency attention — so the tradeoff is breakable. (That implicit consistency *helps OOD* is now consensus — [[2509.14117|GeoAware]] for viewpoint, [[2605.21862|EvoScene-VLA]] / [[2602.20200|OptimusVLA]] for time — so the contest is *which* of consistency-vs-perception drives it, and whether it holds over *full* space+time 4D, not viewpoint alone.)
- **The bet**: it is the consistency *constraint*, not raw 3D or viewpoint-geometry alone, that drives the OOD gain — and it must be shown over *full* space+time 4D, not the viewpoint-only slice [[2509.14117|GeoAware]] fenced. Specifically, ablating [[2605.05126|ConsisVLA-4D]]'s consistency attention with *perception held fixed* collapses OOD SR (toward MolmoAct's 72.1% baseline) more than ablating any single perceptual feature, and more than it dents ID SR — the consistency-vs-perception isolation no paper has run ([[2511.17199|VLA-4D]] varied coordinate-chaos, [[2509.14117|GeoAware]] varied VGGT-layer selection; neither isolated consistency-as-driver).

**Related research papers.** One table on the axis the direction turns on — *the 4D-consistency mechanism* (implicit attention / explicit frame generation / latent-JEPA / scene-flow prior / multi-view diffusion / kinematic tuning / self-distillation) — with `Key result` and what each leaves missing. The contrast that defines the direction is implicit (cheap, in-model) vs explicit (generated, external — the C2 boundary).

| System | Consistency mechanism | Key result | What's missing |
|---|---|---|---|
| [[2605.05126\|ConsisVLA-4D]] | implicit spatio-temporal consistency attention (no frame gen) | **98.1%** LIBERO, **70.0%** real bimanual vs OpenVLA 28.5%, **2.31×** faster | single-source cost claim; consistency-vs-3D not ablated on OOD |
| [[2508.07917\|MolmoAct]] | explicit depth-aware tokens + steerable visual reasoning traces | **86.6%** LIBERO, **72.1%** OOD (+7.8% over RT-2-X), 75% steering | explicit traces aid OOD, but heavier than implicit attention |
| [[2506.22242\|4D-VLA]] | 3D coord embeddings + multi-frame history | **+12.1%** LIBERO over OpenVLA, **+25.4%** LIBERO-LONG, real **85.63%** vs 27.70% | spatiotemporal pretraining, but consistency not enforced as a constraint |
| [[2509.14117\|GeoAware]] | geometric-acuity encoder for viewpoint generalization (no reconstruction) | **+35 pp** zero-shot unseen-viewpoint SR on LIBERO, **96.8%** ID, real-robot | states B2's hypothesis verbatim but *spatial-only* (viewpoint), no temporal 4D; ablation is VGGT-layer selection, not consistency-vs-perception |
| [[2605.21862\|EvoScene-VLA]] | recurrent scene-prior + local depth + global 3D-foundation anchor | **89.1%** RoboTwin Clean / 88.5% Rand, **42.0%** real (+4.7%) | enforces temporal-consistency-as-in-policy-constraint, but never isolates consistency vs the depth/3D perceptual anchors on OOD |
| [[2602.20200\|OptimusVLA]] | temporal-consistency constraint + fast inference | **98.6%** LIBERO, **38%** RoboTwin-2.0-Hard, **2.9×** real speedup | the temporal half of the constraint, but no consistency-vs-perception ablation and no SR-vs-latency frontier vs explicit methods |
| [[2511.17199\|VLA-4D]] | full space+time 4D embeddings (coordinate-chaos ablation) | **97.4%** LIBERO, smooth global + stable local trajectories, zero-shot | runs the *closest* full-4D ablation (3D-vs-no-3D coordinate chaos), but tests 3D presence, not the consistency-vs-perception isolation B2's H1 needs |
| [[2603.25399\|LaMP]] | dense 3D-scene-flow latent motion prior | **98.3%** LIBERO, **79.3%** LIBERO-Plus (+9.7 pp over OpenVLA-OFT) | a temporal-geometry prior — strong OOD, but not a full 4D head |
| [[2604.26848\|STARRY]] | action-centric WM jointly denoising ST latents + actions | RoboTwin 2.0 **93.82%**, real bimanual **70.8%** (+31.7 pp over π0.5) | explicit ST-coherence — the heavier sibling of implicit attention |
| [[2604.03181\|MV-VDP]] | multi-view video diffusion policy w/ 3D + temporal priors | Meta-World **89.1%** at 5 demos, ~89% at one denoising step (5 Hz) | explicit multi-view generation — the cost B2 avoids |
| [[2602.09878\|MVISTA-4D]] | view-consistent 4D WM (spherical embed + deformable cross-view attn) | **72.6%** RLBench, lower depth/Chamfer | explicit 4D-consistency, externally read (C2 boundary), not in-policy |
| [[2507.01099\|Geometry-aware 4D Robot Video]] | explicit RGB+pointmap 4D generation, cross-view consistent | the externally-read pose pipeline (C2's anchor) | generates geometry for a tracker — the explicit counterpart B2 internalizes |
| [[2504.20995\|TesserAct]] | RGB-D-N temporal-depth channel | depth+normal sharpen action prediction | a channel, not an enforced consistency constraint |
| [[2503.19355\|ST-VLM]] | kinematic instruction tuning for ST reasoning | STKit-Bench **59.8%** vs GPT-4V 28.5% | the reasoning side of temporal geometry, not a policy constraint |
| [[2602.10098\|VLA-JEPA]] | implicit consistency in a JEPA latent | **97.2%** LIBERO | latent consistency without explicit geometry — the latent counterpoint |
| [[2604.08532\|SelfEvo]] | consistency-as-self-supervision (self-distillation, no labels) | **−19.7%** depth AbsRel, **+20.1%** AUC@30 on new domains | proves consistency is learnable label-free — not yet a deployed policy |
| [[2604.16484\|DexWorldModel]] | O(1)-memory latent WM | constant-memory rollout | the efficiency budget the consistency mechanism must fit |
| [[2505.05800\|3D-CAVLA]] | 3D context-aware scene-level conditioning over time | scene-level 3D conditioning | conditions on 3D, doesn't enforce cross-time consistency |
| [[2603.22078\|WAM vs VLA Robustness]] | implicit-VLA-vs-explicit-WAM SR×latency frontier (benchmark) | shared 21-sub-dim / 7-category perturbation taxonomy over LIBERO-Plus + RoboTwin-2.0-Plus; WAMs **≥4.8×** slower than π0.5's 63 ms/chunk; π0.5 **85.7%** LIBERO-Plus | the only suite plotting OOD-SR *and* implicit-vs-explicit cost jointly, but compares architecture *families* — doesn't hold perception fixed to isolate consistency-as-driver (H1) |
| [[2506.18088\|RoboTwin 2.0]] | standardized bimanual domain-randomized suite (benchmark) | 5-dim DR; **+24.4%** real few-shot / **+21.0%** zero-shot unseen-background; auto expert-code **71.3%** | the named substrate behind B2's real-bimanual ≥70% target (and the suite EvoScene-VLA/OptimusVLA's RoboTwin numbers come from), but a DR suite, not a consistency mechanism itself |

**Hypotheses & tests.** The FP bet — implicit 4D-consistency matches explicit-3D at far lower cost, and consistency (not raw 3D) drives OOD — decomposed.
1. **H1 — Over full space+time 4D, ablating consistency collapses OOD more than ablating perception.**
   - *Prediction*: removing [[2605.05126|ConsisVLA-4D]]'s consistency attention (perception held fixed) collapses OOD SR more than removing any single perceptual feature, and more than it dents ID SR — the consistency-vs-perception isolation that [[2509.14117|GeoAware]] (VGGT-layer ablation, viewpoint-only) and [[2511.17199|VLA-4D]] (coordinate-chaos, 3D-presence) did *not* run, and over *time* not just viewpoint.
   - *Test*: consistency-ablation vs perceptual-feature-ablation on [[2510.13626|LIBERO-Plus]]'s decomposed factor axes (the isolated camera-viewpoint slice vs background/lighting/layout) and [[2603.22078|WAM vs VLA Robustness]]'s per-category SR breakdown over LIBERO-Plus + RoboTwin-2.0-Plus; report ID-vs-OOD delta for each.
   - *Row*: ConsisVLA-4D / GeoAware / VLA-4D.
   - *Falsifier*: a perceptual-feature ablation hurts OOD as much → raw 3D / viewpoint-geometry, not consistency, drives robustness.
2. **H2 — Implicit 4D is Pareto-dominant on the SR-vs-latency plane, except on a task sub-class.**
   - *Prediction*: plotting implicit ([[2605.05126|ConsisVLA-4D]]) vs explicit ([[2507.01099|Geometry-aware 4D Robot Video]], [[2604.26848|STARRY]]) on SR-vs-latency, implicit dominates except where externally-readable geometry is required (debuggability, tracker handoff).
   - *Test*: build the frontier across implicit and explicit methods on matched tasks — [[2603.22078|WAM vs VLA Robustness]] already plots exactly this SR×latency frontier (implicit-VLA vs explicit-generation-WAM, WAMs ≥4.8× slower than π0.5's 63 ms/chunk) on a shared perturbation suite, the substrate this test otherwise lacks.
   - *Row*: ConsisVLA-4D / Geometry-aware 4D Robot Video.
   - *Falsifier*: explicit dominates broadly → the cost advantage is illusory.
3. **H3 — Implicit consistency + explicit traces compound, not redundant.**
   - *Prediction*: pairing implicit consistency (B2) with [[2508.07917|MolmoAct]]'s steerable visual traces raises OOD SR beyond either alone — the two ground different things (constraint vs auditability).
   - *Test*: implicit-only vs traces-only vs both on OOD SimplerEnv.
   - *Row*: ConsisVLA-4D / MolmoAct.
   - *Falsifier*: both ≈ max(either) → the signals are redundant.
4. **H4 — The implicit advantage has a horizon crossover.**
   - *Prediction*: implicit consistency beats 2D above a horizon threshold and loses to explicit-generation above a longer one — there is a measurable crossover window where implicit is optimal.
   - *Test*: sweep task horizon; locate the two crossovers.
   - *Row*: ConsisVLA-4D / STARRY.
   - *Falsifier*: no crossover (implicit always or never wins) → horizon isn't the operating variable; beyond the upper crossover, route to C4.
5. **H5 — A scene-flow prior recovers most of the consistency gain at lower cost.**
   - *Prediction*: [[2603.25399|LaMP]]'s dense 3D-scene-flow prior recovers a large fraction of ConsisVLA-4D's OOD gain (toward 79.3% [[2510.13626|LIBERO-Plus]]) at lower architectural cost than full consistency attention — flow is the cheap form of the constraint.
   - *Test*: scene-flow prior vs full consistency attention on [[2510.13626|LIBERO-Plus]] at matched backbone.
   - *Row*: LaMP / ConsisVLA-4D.
   - *Falsifier*: the flow prior underperforms materially → the full attention mechanism is load-bearing, not just the temporal-geometry signal.

> [!warning] Risks
> - **Implicit consistency may not be inspectable** — you can't see what 4D structure the attention learned, hurting debuggability. → Pair with [[2508.07917|MolmoAct]]'s explicit visual reasoning traces (H3) so the temporal reasoning is steerable and auditable.
> - **Single-source cost claim** — the 2.31× speedup rests on [[2605.05126|ConsisVLA-4D]] alone. → H2's full cost/accuracy frontier across implicit and explicit methods is the go/no-go before generalizing the efficiency claim.
> - **Implicit 4D may silently fail on the longest horizons** where drift accumulates invisibly. → H4's horizon-scaling crossover bounds the regime; beyond it, route to **C4**'s explicit persistent geometric memory rather than stretching implicit consistency.

---

## Cluster C — Geometry-Native World Models & Memory

*The world model's representation is geometry, not appearance — a model-agnostic substrate any policy or model can use. The four directions are ordered along the decodability axis: occupancy a planner reads (C1) and pointmaps a tracker reads (C2) keep geometry explicit and external; a latent-4D state decoded for imagination (C3) keeps it internal; and a world-frame memory (C4) makes whichever of the three persist over long horizons.*

### C1 — Occupancy World Models as the Manipulation Rollout Substrate

| | |
|---|---|
| **Cluster** | C — Geometry-Native World Models |
| **Thesis** | A world model's long-horizon stability is bounded by how fast *geometric* error piles up — and an explicit occupancy grid with rigid-transform constraints bounds that error where a latent substrate doesn't. The manipulation-WM field assumes the rollout substrate should be the same RGB-D latent the policy sees, and nobody has run the occupancy-vs-latent horizon comparison at tabletop scale. The bet is in First-principles below. |
| **Anchor papers** | [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2506.20134\|3D World Models Survey]] (survey), [[2604.19092\|RoboWM-Bench]] (benchmark), [[2603.28887\|OccSim]] (method), [[2604.26694\|X-WAM]] (method) |
| **Key targets** | Stable rollout ≥3,000 frames / ≥4 km ([[2603.28887\|OccSim]]); +22.1% rel mIoU vs asset-based sim; 80× horizon over prior <50-frame WMs; manipulation port: minute-scale geometric coherence vs latent-world-model drift, scored on [[2604.19092\|RoboWM-Bench]]'s step+final manipulation SR (rigid/articulated/deformable/long-horizon/bimanual, more discriminative than perceptual-plausibility metrics) |

**Why it matters.**
- **The gap**: [[2510.16732|World Models for Embodied AI Survey]] traces the WM spatial axis from latent → token → explicit 3D, but the manipulation default is a latent/pixel substrate whose geometric error compounds — the rollout drifts within tens of frames over long horizons.
- **Today's answers**: occupancy-as-the-manipulation-rollout-substrate is *not* novel and *not* driving-only — [[2505.16249|3D-Occ-MPC]] runs dense voxel occupancy → learned dynamics → MPC sim+real, and [[2011.01968|DSR-Net]] built occupancy + MPC manipulation back in 2020 (planar-pushing voxel IoU **0.72** vs SE3-Net 0.31), with [[2505.05512|Occupancy World Model]] porting occupancy WMs to indoor scenes. Sibling **C3** ([[2604.26694|X-WAM]]) pushes the *latent-4D* corner (15 Hz, Chamfer 0.0049, per-frame-excellent); [[2510.10125|CTRL-WORLD]] makes the pixel substrate controllable. None runs the explicit-occupancy-vs-latent-4D *horizon-to-divergence* head-to-head at tabletop scale.
- **The opening**: [[2603.28887|OccSim]] proves explicit occupancy + Warp-DiT rigid-transform constraints bound per-step geometric error to sustain 3,000+ frames over 4+ km (**80×** the prior <50-frame ceiling), with data lifting downstream forecasting **+22.1%** rel mIoU — the long-horizon stability the field treats as unattainable.

**First-principles framing.**
- **First principle**: a WM's long-horizon stability is set by how fast *geometric* error grows from one rollout step to the next. An occupancy grid with rigid-transform constraints ([[2603.28887|OccSim]]'s Warp-DiT) keeps that per-step error in check; a latent substrate has no such limit, so the error compounds and the rollout drifts.
- **Assumption being challenged**: that the rollout substrate should be the same RGB-D latent the policy sees (the [[2510.10125|CTRL-WORLD]] / C3-latent [[2604.26694|X-WAM]] convention). The card's old "field skips occupancy because it was built only in driving" framing is *empirically false* — [[2011.01968|DSR-Net]] (2020) and [[2505.05512|Occupancy World Model]] already did occupancy in manipulation/indoor robots, and [[2505.16249|3D-Occ-MPC]] instantiates the occupancy-rollout principle. The real open assumption: that *because* occupancy and latent both "work," the choice doesn't bound horizon — when [[2603.28887|OccSim]]'s 80× horizon gain says the substrate *is* the drift source.
- **The bet**: a voxel-semantic occupancy WM beats a latent-4D baseline (sibling C3, [[2604.26694|X-WAM]]) by ≥1 order of magnitude on *horizon-to-divergence* at tabletop scale — the head-to-head [[2505.16249|3D-Occ-MPC]] and [[2011.01968|DSR-Net]] never ran — while *losing* on per-frame Chamfer (latent-4D's 0.0049), making the two complementary not competitive, and its Warp-DiT rigid-transform error bound survives to sub-cm.

**Related research papers.** One table on the axis the direction turns on — *the rollout substrate's decodability* (explicit-occupancy / latent-4D / pixel-video / depth-augmented / O(1)-latent) — with `Key result` and what each leaves missing for a long-horizon planner.

| System | Rollout substrate | Key result | What's missing |
|---|---|---|---|
| [[2603.28887\|OccSim]] | explicit voxel-semantic occupancy + Warp-DiT | **3,000+** stable frames, **4+ km**, **+22.1%** rel mIoU, **80×** horizon, **67%** zero-shot | a driving result — never ported to sub-cm manipulation occupancy |
| [[2505.16249\|3D-Occ-MPC]] | explicit occupancy → learned dynamics → MPC (the rollout substrate) | occupancy EMD **28.6e-3** / DCD **34.5e-4** beats patch/crop, elasto-plastic sim+real | instantiates C1's principle (occupancy-as-rollout-substrate) but object-centric, no full-scene occupancy-vs-latent horizon comparison |
| [[2011.01968\|DSR-Net]] | 3D scene-flow voxel state + MPC (occupancy in manipulation, 2020) | planar-push voxel IoU **0.72** vs SE3-Net 0.31, surface MSE **5.54 cm**, IoU **0.772** under occlusion | falsifies "occupancy is driving-only," but no rigid-transform horizon bound and no latent comparator |
| [[2505.05512\|Occupancy World Model]] | autoregressive indoor-scene occupancy forecasting | **+22.34** IoU / **+12.21** mIoU next-state, **+19.48** autoregressive IoU | proves occupancy WMs port driving→indoor (C1's scale move), but a scene forecaster, not a planner-readable manipulation rollout |
| [[2506.23126\|ParticleFormer]] | particle/point forward dynamics + MPC | superior MSE/CD, robust to hyperparams, lower MPC final-state error | the point-set rollout alternative — externally inspectable but not a dense occupancy grid a planner collision-checks |
| [[2604.26694\|X-WAM]] | latent-4D, decoded internally (sibling C3) | Chamfer **0.0049** vs 0.0680, **15 Hz**, 79.2% RoboCasa | internal latent the planner can't read; fails on *horizon*, excels per-frame |
| [[2510.10125\|CTRL-WORLD]] | controllable pixel video | **38.7→83.4%** on unseen objects | pixel substrate re-parses geometry; drifts long-horizon, not planner-readable |
| [[2504.20995\|TesserAct]] | RGB-D-N (depth-augmented) | depth+normal channels sharpen prediction | midpoint between latent and occupancy — geometry is a channel, not the state |
| [[2604.16484\|DexWorldModel]] | O(1)-memory latent | constant-memory rollout over 2,000 steps | latent, not explicit — the efficiency budget occupancy must respect |
| [[2604.22152\|dWorldEval]] | pixel-video horizon-drift evaluator (benchmark) | round-trip LPIPS **0.243** at 20-step horizon, policy-ranking Pearson **~0.9–0.92** | the manipulation drift-over-horizon metric vehicle for C1's central horizon claim, but pixel substrate — cannot itself score *occupancy-geometric* divergence |
| [[2406.02523\|RoboCasa]] | the proposed target suite | geometry-bound long-horizon manipulation (X-WAM 79.2% on 24 tasks) | no occupancy-substrate baseline on it yet — the gap C1 fills |
| [[2510.16732\|World Models for Embodied AI Survey]] | latent → token → explicit-3D taxonomy | locates occupancy at the explicit end | a map, not a manipulation WM |
| [[2604.22748\|Agentic World Modeling Survey]] | L2-Simulator domain-law rollout requirement | names the stability occupancy supplies | requirement, not mechanism |
| [[2506.20134\|3D World Models Survey]] | 2D→3D-cognition transition | motivates explicit-geometry WMs | survey framing only |

**Hypotheses & tests.** The FP bet — explicit occupancy beats latent on horizon-to-divergence, complementary on per-frame fidelity — decomposed.
1. **H1 — Occupancy beats latent on horizon-to-divergence at tabletop scale (the head-to-head nobody ran).**
   - *Prediction*: on matched manipulation tasks, frames-to-geometric-divergence for an occupancy WM exceeds sibling C3's [[2604.26694|X-WAM]]-class latent by ≥one order of magnitude — the explicit-vs-latent horizon comparison [[2505.16249|3D-Occ-MPC]] and [[2011.01968|DSR-Net]] never ran — partially surviving the driving→tabletop scale change.
   - *Test*: matched-task occupancy vs X-WAM latent on [[2604.19092|RoboWM-Bench]]'s long-horizon manipulation tasks (step+final SR, the shared substrate the occupancy-vs-latent head-to-head otherwise lacks), measuring frames-to-divergence via [[2604.22152|dWorldEval]]'s 20-step round-trip-consistency LPIPS (the manipulation analog of OccSim's driving stable-frame-count).
   - *Row*: OccSim / X-WAM / 3D-Occ-MPC.
   - *Falsifier*: occupancy ≤ latent horizon → the driving gain is scale-specific.
2. **H2 — Externally-readable occupancy beats a decoded latent for collision-checking.**
   - *Prediction*: an off-the-shelf planner consumes the occupancy grid for collision-checking without a learned decoder, and this beats decoding C3's latent into a usable state on planning latency and accuracy.
   - *Test*: planner-on-occupancy vs planner-on-decoded-latent on collision-check tasks, hosted on [[2510.18135|World-in-World]]'s closed-loop WM-in-control-loop protocol (counterfactual rollout → unified planning → downstream SR, with Robotic Manipulation in its suite) — the planner-on-WM-state substrate H2 otherwise lacks.
   - *Row*: OccSim / X-WAM.
   - *Falsifier*: decoding the latent matches direct occupancy → externality buys nothing.
3. **H3 — A hybrid substrate beats either alone on (horizon × fidelity).**
   - *Prediction*: running occupancy for long-horizon planner-readable rollout and switching to C3's [[2604.26694|X-WAM]] latent for per-step high-fidelity imagine beats either substrate alone on the joint metric.
   - *Test*: hybrid vs occupancy-only vs latent-only on (horizon × Chamfer).
   - *Row*: OccSim / X-WAM.
   - *Falsifier*: one substrate dominates both axes → the complementarity claim fails.
4. **H4 — The Warp-DiT error bound survives at sub-cm.**
   - *Prediction*: [[2603.28887|OccSim]]'s rigid-transform error-bounding holds at manipulation resolution, degrading gracefully rather than collapsing below meter-scale.
   - *Test*: sweep occupancy resolution; report the resolution at which the bound loosens.
   - *Row*: OccSim.
   - *Falsifier*: the bound collapses below meter-scale → occupancy doesn't transfer to manipulation precision.
5. **H5 — Occupancy-grid drift, not Chamfer, predicts downstream planning failure.**
   - *Prediction*: downstream long-horizon planning SR correlates with horizon-to-divergence (mIoU-over-horizon), not per-frame Chamfer — confirming the right failure axis is horizon length.
   - *Test*: regress planning SR on both metrics across rollouts — [[2510.18135|World-in-World]] supplies the downstream closed-loop SR (e.g. Image-Goal Nav 38.19→45.14%, manipulation) to regress against, and [[2604.22152|dWorldEval]] the complementary policy-ranking correlation (Pearson ~0.9 of WM-proxy vs real SR) tying drift to outcome.
   - *Row*: OccSim / X-WAM.
   - *Falsifier*: per-frame Chamfer predicts SR as well → C1 and C3 measure the same thing.

> [!warning] Risks
> - **Driving→manipulation scale gap** — occupancy validated at meter-scale, manipulation needs sub-cm. → H4's sub-cm Warp-DiT test is the go/no-go; report the resolution at which the error bound breaks rather than assuming transfer.
> - **Overlap with sibling C3** if the explicit/latent delta blurs in practice. → Keep the contribution pinned to *externally-renderable long-horizon occupancy* (H2) and *complementarity* (H3) — C1 is not a better X-WAM, it is the substrate X-WAM isn't.
> - **Occupancy supervision scarcity in manipulation data.** → Derive occupancy in sim (free) and from depth + gripper geometry on real data; bound real-world claims to where occupancy GT is recoverable.

### C2 — 4D-Geometric-Consistent Video Prediction for 6-DoF Pose Extraction

| | |
|---|---|
| **Cluster** | C — Geometry-Native World Models |
| **Thesis** | A 6-DoF pose is a geometric quantity — cross-view-consistent pointmaps expose it directly to any tracker, while RGB-only frames leave it ambiguous. The field predicts RGB-only frames and re-estimates 3D after the fact, assuming a pixel video model plus a downstream pose estimator suffices. The bet is in First-principles below. |
| **Anchor papers** | [[2506.20134\|3D World Models Survey]] (survey), [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2604.19092\|RoboWM-Bench]] (benchmark), [[2507.01099\|Geometry-aware 4D Robot Video]] (method), [[2507.13347\|Pi3]] (method) |
| **Key targets** | Avg task SR ≥0.64 across three sim tasks ([[2507.01099\|Geometry-aware 4D Robot Video]]) vs Dreamitate 0.12 / Diffusion Policy 0.12 (≈5× baseline), scaled out on [[2604.19092\|RoboWM-Bench]]'s predicted-video→executable-action step+final SR (more discriminative than perceptual plausibility); cross-view geometric consistency (higher mIoU) + lower FVD/AbsRel; generalize to novel viewpoints without retraining |

**Why it matters.**
- **The gap**: video-prediction-for-action methods (Dreamitate-class) predict future RGB frames and then bolt on a pose estimator — but RGB-only frames leave 6-DoF pose ambiguous, so the policies are brittle (Dreamitate and Diffusion Policy both at 0.12 avg task SR in [[2507.01099|Geometry-aware 4D Robot Video]]'s evaluation).
- **Today's answers**: [[2507.01099|Geometry-aware 4D Robot Video]] makes geometry a *predicted output* — SVD predicting future multi-view RGB *and* aligned 3D pointmaps (pointmap VAE + cross-view pointmap diffusion loss), no explicit camera poses at inference — so off-the-shelf trackers read 6-DoF straight off (0.64 avg task SR, ≈5× the 0.12 baselines). The nearest neighbor [[2509.00361|Gen Visual Foresight Pose]] (GVF-TAPE) predicts in-model RGB-D and extracts 6-DoF in a closed loop (83.0% LIBERO, +11.56% over action-labeled IL) — but from a *single* view with a *learned* pose estimator, not cross-view-consistent points read by an off-the-shelf geometric tracker. [[2602.09878|MVISTA-4D]] reaches cross-view-consistent geometry but routes it to an end-to-end head, not a tracker. The cross-view-consistency-for-tracker mechanism + the H1 consistency-vs-fidelity ablation remain untaken.
- **The opening**: [[2604.27106|RecGen]]'s reconstruction-by-generation recovers explicit shape + 6-DoF pose at 92.7% ADD-SB@0.1 and +38.2 pp under occlusion vs SAM3D — proof the predicted-geometry → tracker-readable-pose pipeline holds where post-hoc estimation collapses.

**First-principles framing.**
- **First principle**: a 6-DoF pose is geometric. If the pointmaps agree across views, any tracker reads the pose straight off them — the pose is just the rigid transform between matching 3D points. RGB-only frames hide the pose: it is left implicit and changes with the viewpoint, so a downstream estimator re-solves it from scratch every frame with too little to go on. The pointmap machinery [[2507.13347|Pi3]] makes the consistent 3D the readout depends on.
- **Assumption being challenged**: the Dreamitate-class convention that a pixel video model + a downstream pose estimator suffices — held by [[2508.20840|Primitive Embodied WM]] (PEWM), which extracts 6-DoF from generated video *without explicit geometric supervision* (Gen6D, RGB-only). And the *softer* convention that geometry-from-a-single-view is enough: [[2509.00361|Gen Visual Foresight Pose]] predicts RGB-D but reads pose with a *learned* estimator, not off cross-view-consistent points. [[2507.01099|Geometry-aware 4D Robot Video]]'s ≈5× SR gap shows the post-hoc/single-view estimator is the bottleneck.
- **The bet**: the discriminator that survives the whole field is *cross-view pointmap consistency read by an off-the-shelf geometric tracker* — not single-view RGB-D ([[2509.00361|Gen Visual Foresight Pose]]) and not a learned estimator or RGB-only Gen6D ([[2508.20840|Primitive Embodied WM]]). Specifically, jointly predicting RGB + cross-view-consistent pointmaps yields tracker-readable 6-DoF trajectories at ≥0.64 avg task SR vs ~0.12 for RGB-plus-estimator baselines (≈5×), and the gain tracks *cross-view consistency* (mIoU): ablating the cross-view pointmap loss collapses trajectory accuracy more than degrading RGB quality (FVD) does — the H1 isolation no neighbor has run.

**Related research papers.** One table on the axis the direction turns on — *the source of the geometry a tracker reads pose from* (predicted cross-view pointmaps / sensed depth / reconstruction-by-generation / latent-4D / implicit-in-policy) — with `Key result` and what each leaves missing. The contrast that defines the direction is externalized geometry (C2) vs internalized consistency (B2's [[2605.05126|ConsisVLA-4D]]).

| System | Pose-readout source | Key result | What's missing |
|---|---|---|---|
| [[2507.01099\|Geometry-aware 4D Robot Video]] | predicted cross-view-consistent pointmaps (SVD) | **0.64** avg task SR vs 0.12 baselines (≈5×), novel-viewpoint | three-task base; consistency-vs-RGB not ablated against the SR gain |
| [[2509.00361\|Gen Visual Foresight Pose]] | predicted *single-view* RGB-D → *learned* 6-DoF pose estimator (closed loop) | **83.0%** LIBERO (+11.56% over action-labeled IL, +26.9% over video-pred), 56→86% real w/ human-video transfer | the nearest neighbor, but single-view (no cross-view pointmap consistency) + learned estimator, not an off-the-shelf tracker reading consistent points |
| [[2508.20840\|Primitive Embodied WM]] | generated video → 6-DoF *without* geometric supervision (Gen6D, RGB-only) | **93%** RLBench close-box, 16/20 real vs OpenVLA 0/20, 75× faster, 12 FPS | the Dreamitate-class convention C2 inverts — RGB-only pose makes it the baseline, not a solution |
| [[2601.05237\|ObjectForesight]] | predicted 3D object trajectories from egocentric video (DiT) | ADE **0.016 m** / ARE **2.30°** on EPIC-Kitchens, 2M-traj dataset | forecasts geometric trajectories, but offline from human video, not a tracker-readable in-policy rollout |
| [[2601.18323\|TC-IDM]] | post-hoc inverse-dynamics over generated video (motion prior) | **61.11%** real avg, novel-viewpoint + deformable + dual-arm/dexterous transfer | extracts action from generated video, but post-hoc IDM, not pose read off cross-view-consistent points |
| [[2511.12882\|MTV-World]] | multi-view video WM with object-mask prior (no explicit pointmaps) | J **54.9/45.0** dual-arm (vs Ctrl-World 35.3), zero-shot novel-view | multi-view consistency for *interaction* but RGB/mask, not tracker-readable 3D pointmaps |
| [[2502.10028\|3D Foresight Manipulation]] | predicted future depth/3D foresight (in-policy) | LIBERO **95.3%**, depth-critical real 70% vs 35% 2D, +6 ms latency | predicts 3D for *action*, not 6-DoF pose extraction by a tracker; single-view depth, no cross-view consistency |
| [[2602.09878\|MVISTA-4D]] | cross-view-consistent RGB-D 4D prediction | lower Chamfer/depth than baselines, 72.6% RLBench | routes consistency to an end-to-end head — not an external tracker |
| [[2606.03943\|PointAction]] | predicted dynamic pointmaps (action interface) | 43.0% zero-shot xArm7 | predicts points for *action*, not pose extraction by a tracker |
| [[2605.05126\|ConsisVLA-4D]] | implicit consistency, internal (B2 boundary) | 98.1% LIBERO, 2.31× faster | geometry never leaves the model — the internalized contrast |
| [[2504.20995\|TesserAct]] | explicit geometric channels alongside RGB | depth+normal sharpen action extraction | a channel, not tracker-readable cross-view pointmaps |
| [[2604.26694\|X-WAM]] | latent-4D, end-effector-derived camera poses | Chamfer 0.0049, 15 Hz | latent substrate — pose is internal, not externally read (sibling C3) |
| [[2505.20279\|VLM-3R]] | reading geometry out of reconstructed 3D | grounds reasoning in reconstructed 3D | reconstruction for reasoning, not 6-DoF trajectory readout |
| [[2507.13347\|Pi3]] | pointmap/3D-reconstruction model | the consistent-pointmap machinery | a reconstruction backbone, not a predictive rollout |
| [[2604.19092\|RoboWM-Bench]] | predicted-video→executable-action SR (benchmark) | step+final SR across rigid/articulated/deformable/long-horizon, real-to-sim-validated; separates executable from merely-plausible where perceptual metrics saturate | the discriminative SR substrate the ≈5× headline scales onto (its perceptual-vs-executability split *is* H1's "consistency not RGB fidelity drives action"), but doesn't itself isolate 6-DoF readout from predicted vs sensed geometry |
| [[2510.16732\|World Models for Embodied AI Survey]] | explicit-geometry WM + pose-extraction framing | frames the use case | survey only |

**Hypotheses & tests.** The FP bet — cross-view-consistent predicted pointmaps make pose tracker-readable, and consistency (not RGB fidelity) drives the action gain — decomposed.
1. **H1 — Cross-view consistency, not RGB fidelity or single-view depth, drives the action gain.**
   - *Prediction*: removing the cross-view pointmap diffusion loss (RGB quality held fixed) collapses trajectory-extraction accuracy and downstream SR more than degrading RGB FVD does — *and* a single-view-depth + learned-estimator variant ([[2509.00361|Gen Visual Foresight Pose]]-style) underperforms the cross-view-consistent tracker readout on the same tasks, isolating consistency-for-tracker as the lever neither neighbor tested.
   - *Test*: ablate the cross-view loss vs degrade RGB vs swap to single-view-depth + learned estimator; report SR delta for each on [[2604.19092|RoboWM-Bench]]'s predicted-video→action SR (its perceptual-vs-executability discrimination is exactly H1's axis — execution accuracy varies even at high perceptual scores) and against [[2602.08971|WorldArena]]'s measured *perception–functionality gap* (high FVD/visual quality ≠ downstream SR) at the world-model level.
   - *Row*: Geometry-aware 4D Robot Video / Gen Visual Foresight Pose.
   - *Falsifier*: degrading RGB or single-view depth hurts SR as much → appearance / single-view geometry, not cross-view consistency, carries the gain.
2. **H2 — Predicted pointmaps cost little vs sensed depth on pose readout.**
   - *Prediction*: 6-DoF extraction from predicted pointmaps loses only a small margin to extraction from sensed depth on the same tasks — small enough to justify predicting where sensing is unavailable.
   - *Test*: predicted-pointmap vs sensed-depth pose readout, matched tasks.
   - *Row*: Geometry-aware 4D Robot Video / RecGen.
   - *Falsifier*: predicted pointmaps lose a large margin → C2 only applies where depth sensing is impossible.
3. **H3 — Novel-viewpoint generalization has a measurable extrapolation envelope.**
   - *Prediction*: pose-extraction accuracy holds out to a bounded viewpoint-extrapolation range before degrading — the operational envelope of the externally-readable claim.
   - *Test*: sweep test viewpoint distance from training; locate the degradation point.
   - *Row*: Geometry-aware 4D Robot Video.
   - *Falsifier*: accuracy degrades immediately off-training-views → "no retraining" is overclaimed.
4. **H4 — Externalized geometry beats internalized on debuggability-critical tasks.**
   - *Prediction*: on the same task, C2's tracker-readout pipeline beats [[2605.05126|ConsisVLA-4D]]'s end-to-end implicit head where the geometry must be inspected/reused (multi-tracker, failure diagnosis), and loses where only cost matters.
   - *Test*: C2 vs ConsisVLA-4D on matched tasks; split by debuggability requirement.
   - *Row*: Geometry-aware 4D Robot Video / ConsisVLA-4D.
   - *Falsifier*: the implicit head matches externalization everywhere → externality buys nothing.
5. **H5 — Occlusion is where predicted-geometry pose readout wins most.**
   - *Prediction*: the predicted-pointmap → pose pipeline's advantage over post-hoc estimation is largest under occlusion, mirroring [[2604.27106|RecGen]]'s +38.2 pp occlusion gain.
   - *Test*: stratify pose-readout accuracy by occlusion level.
   - *Row*: RecGen / Geometry-aware 4D Robot Video.
   - *Falsifier*: the advantage is flat across occlusion → predicting geometry doesn't specifically help the hard case.

> [!warning] Risks
> - **Single-anchor direction** — the headline rests on [[2507.01099|Geometry-aware 4D Robot Video]]'s three-task evaluation. → H1's consistency-ablation and H2's predicted-vs-sensed comparison are the internal validity checks; broaden the task set before generalizing the ≈5× claim.
> - **Predicted pointmaps may be noisier than sensed depth**, degrading pose readout. → H2 quantifies the predict-vs-sense gap directly; if large, gate C2 to settings where sensing is unavailable (novel viewpoints, no depth sensor).
> - **Three-task SR is a narrow base** for a substrate claim. → Frame the contribution as *the mechanism* (explicit cross-view pointmaps → tracker-readable pose) validated on three tasks, with broader evaluation as the explicit next step — do not overclaim breadth.

### C3 — Natively-4D Geometry as a World-Representation Substrate

| | |
|---|---|
| **Cluster** | C — Geometry-Native World Models & Memory |
| **Thesis** | For contact and spatial tasks the action is set by geometry a model can only infer indirectly from pixels — so a representation that is *natively 4D* (RGB + depth + 3D geometry over time) carries it directly, where 2D pixels lifted after the fact don't. The field treats live 4D as too expensive to deploy. The bet is in First-principles below. |
| **Anchor papers** | [[2506.20134\|3D World Models Survey]] (survey), [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2604.26509\|3D Generation for Embodied AI Survey]] (survey), [[2406.02523\|RoboCasa]] (benchmark), [[2602.08971\|WorldArena]] (benchmark), [[2604.26694\|X-WAM]] (method), [[2503.18945\|Aether]] (method), [[2506.01103\|DeepVerse]] (method) |
| **Key targets** | [[2406.02523\|RoboCasa]] 79.2% avg over 24 tasks (+12.1 pp vs [[2601.16163\|Cosmos Policy]]); native-vs-lift geometric fidelity on [[2603.03485\|Phys4D]]'s three-tier protocol (per-frame AbsRel → short-term consistency → world-level 4D Chamfer + Worldline-L2 over horizon — lowest 4D-CD **0.4626**); Chamfer 0.0049 vs 0.0680 two-stage; +2.34 dB PSNR; 4.5× action-latency speedup (4665→1033 ms) at 5 denoising steps → 15 Hz real-time |

**Why it matters.**
- **The gap**: [[2510.16732|World Models for Embodied AI Survey]] traces the spatial axis latent → token → explicit 3D and [[2506.20134|3D World Models Survey]] frames the move "from 2D visual perception to comprehensive 3D spatial cognition," yet almost every deployed model still imagines in 2D pixels and recovers geometry only implicitly — which [[2604.26694|X-WAM]] says "leads to physically implausible predictions and hinders geometrically faithful reconstruction."
- **Today's answers**: explicit-geometry-kept-online is *no longer unattempted* — [[2601.03782|PointWorld]] (Fei-Fei lab) keeps an explicit-3D point-flow WM online at real-time (0.12 s, 10-step), rolls it under candidate actions in MPC, and the *same* shared 3D state-action representation transfers across embodiments (zero-shot Franka), substantially taking C3's broad thesis and most of its H5 transfer claim at 1B-param scale. The other defense — 4D is a train-time luxury: [[2603.17240|GigaWorld-Policy]] (9× speedup, no video at inference), [[2606.03188|GeoSem-WAM]] (98.55% LIBERO, aux dropped at test), [[2602.10098|VLA-JEPA]] (97.2% LIBERO, pure latent). None runs the async-denoising no-deployment-penalty latency-vs-pixel comparison or the Chamfer-vs-two-stage native-vs-lift ablation.
- **The opening**: [[2604.26694|X-WAM]] breaks the trade-off — a lightweight interleaved depth branch injects 3D into a pretrained DiT, and Asynchronous Noise Sampling decouples video and action denoising so actions decode in **5 steps** (4665→1033 ms, **4.5×**, **15 Hz**) while geometry stays faithful (**Chamfer 0.0049** vs 0.0680, **79.2%** RoboCasa, +12.1 pp over [[2601.16163|Cosmos Policy]]) — 4D at real-time rates, no deployment penalty.

**First-principles framing.**
- **First principle**: for contact-rich and spatially-bound tasks, the action is a function of *geometry* — relative pose, depth, surface normals, free space. A pixel substrate that doesn't encode geometry forces the consumer to re-infer it from appearance every step, discarding structure the substrate could carry directly. The geometry is in the task, not the rendering choice; [[2506.01103|DeepVerse]]'s explicit depth + camera-pose memory cures the scale ambiguity a pixel substrate suffers.
- **Assumption being challenged**: that explicit 4D is too expensive to deploy, so geometry is recovered by a separate two-stage pipeline. [[2604.26694|X-WAM]] shows the two-stage path is both worse geometrically (Chamfer 0.0680 vs 0.0049) *and* slower than a unified 4D model with asynchronous denoising. But "explicit geometry online beats latent + transfers across embodiments" is now *demonstrated* by [[2601.03782|PointWorld]] — so C3's distinctiveness narrows to what PointWorld omits: the *async-denoising no-penalty* latency comparison and the *native-vs-lift Chamfer* ablation, on a native-4D-RGB-D-video (not point-flow) substrate.
- **The bet**: the two pillars no paper — including [[2601.03782|PointWorld]] — has run decide whether native online 4D earns its keep over a train-time auxiliary: (i) holding the backbone fixed, [[2604.26694|X-WAM]]'s interleaved depth branch beats a pixel substrate + post-hoc depth estimator on geometry-bound [[2406.02523|RoboCasa]] tasks (Chamfer 0.0049 native vs the two-stage 0.0680), isolating native-over-recovered; and (ii) generalizing Asynchronous Noise Sampling, the action schedule step-distills to 1–4 steps (extending X-WAM's 5-step 15 Hz, 4665→1033 ms) without degrading the read-out geometry — the latency-fidelity frontier PointWorld's point-flow MPC never charted.

**Related research papers.** One table on the axis the direction turns on — *where the 4D geometry lives and when it is available* (native-latent online / train-time auxiliary, dropped at deploy / AR-explicit / rendering-end / semantic-latent / real-time-from-video) — with `Key result` and what each leaves missing.

| System | Where 4D geometry lives | Key result | What's missing |
|---|---|---|---|
| [[2604.26694\|X-WAM]] | native interleaved latent-4D, online (async denoising) | **79.2%** RoboCasa, Chamfer **0.0049** vs 0.0680, **15 Hz** | the single result the direction rests on — no native-vs-recovered ablation |
| [[2601.03782\|PointWorld]] | explicit-3D point-flow WM, online real-time, rolled in MPC, model-agnostic transfer | **0.12 s** 10-step at **1B** params, zero-shot Franka push/fold/microwave, transfers across embodiments | takes C3's broad thesis + H5 transfer at scale, but point-flow (not native-4D-RGB-D-video), no async-denoising latency-vs-pixel, no Chamfer-vs-two-stage native-vs-lift ablation |
| [[2510.09036\|iMoWM]] | interactive multi-modal (RGB+depth) WM, online | best FVD/PSNR/AbsRel vs iVideoGPT/GWM, faster MBRL convergence, real IL augmentation | online multi-modal substrate, but depth-as-channel not native-4D, no native-vs-recovered Chamfer head-to-head |
| [[2506.14135\|GAF]] | Gaussian Action Field — 4D dynamic-scene WM | **60.4%** RLBench (+15.7% over DP), **+11.5 dB** PSNR future-state, real 10/10 push | explicit 4D for action, but rendering-Gaussian substrate, not the async-denoising no-penalty latency claim |
| [[2506.23126\|ParticleFormer]] | particle/point 4D forward dynamics + MPC | superior MSE/CD dynamics, lower MPC final-state error | particle substrate online, but no async step-distillation latency-vs-pixel and no WM→policy-head transfer test |
| [[2507.06710\|Spatial]] | spatio-temporal-aware 4D diffusion policy (DP4) | Adroit **84.7%** (+16.4% over DP3), DexArt **82.5%**, real **54.6%** | adds the temporal axis to a 3D policy, but a policy not a transferable WM substrate — H5 transfer untested |
| [[2505.10075\|FlowDreamer]] | scene-flow-conditioned RGB-D WM + MPC | **+7%** semantic / **+11%** pixel vs RGB-D WM, **+6%** MPC SR | flow-augmented RGB-D, the lift-after-channel midpoint — no native-4D async-denoising real-time claim |
| [[2503.18945\|Aether]] | unified geometry-aware (4D recon + action-cond + planning) | zero-shot KITTI AbsRel **0.056** | reconstruction objective lifts planning, but not a real-time policy substrate |
| [[2506.01103\|DeepVerse]] | AR-4D-native (explicit depth + pose + geometry memory) | cures scale ambiguity + long-horizon drift | autoregressive — latency vs X-WAM's async-denoising not compared |
| [[2603.12639\|RoboStereo]] | dual-tower RGB-video + 3D-pointmap DiT, bidirectional cross-attn, 4DGS head, frame-level action conditioning | **30→65%** real-arm SR, **>97%** rel sim uplift, 1st/2nd on **16** WorldArena physics/3D metrics | online action-conditioned 4D substrate, but tied to its policy-optimization framework — substrate-only transfer to a third-party head untested |
| [[2605.20752\|GaussianDream]] | feed-forward 3DGS, train-time, dropped at deploy | **98.4%** LIBERO, 34.4→50% real | renderable geometry dropped at inference — opposite of online 4D |
| [[2603.17240\|GigaWorld-Policy]] | future-dynamics supervision, no video at inference | **9×** speedup | geometry as train-time signal only — not an online substrate |
| [[2606.03188\|GeoSem-WAM]] | geometry+semantic on latents, aux dropped at test | **98.55%** LIBERO | the geometry-as-train-time-signal contrast to keeping 4D online |
| [[2604.16484\|DexWorldModel]] | causal latent on DINOv3 semantic targets | **94%** RoboTwin | semantic-latent, not geometric — the non-geometric alternative |
| [[2602.10098\|VLA-JEPA]] | pure latent JEPA, no geometric decoder | **97.2%** LIBERO | no geometry channel at all — the latent-only baseline to beat |
| [[2603.16666\|Fast-WAM]] | train video, test latent (drops WM at deploy) | drop-at-deploy efficiency | opposite of keeping 4D online — the deploy-light contrast |
| [[2603.03485\|Phys4D]] | three-tier 4D-geometric-fidelity evaluator (benchmark) | per-frame AbsRel **0.2711** → world-level 4D-CD **0.4626** + Worldline-L2 over horizon; +11.4 pp Physics-IQ | finally measures Chamfer + horizon *jointly* (the native-vs-lift fidelity axis), but doesn't itself run native-vs-recovered at matched latency |
| [[2602.08971\|WorldArena]] | WM-functional-utility evaluator: data-engine / policy-evaluator / action-planner (benchmark) | EWMScore↔human **r=0.825** perceptual but only **r=0.360** action-planning — the *perception–functionality gap* | tests whether a WM substrate transfers to control (H5), but scores functional utility, not geometric fidelity, and doesn't isolate native-vs-recovered |
| [[2604.07209\|INSPATIO-WORLD]] | real-time 4D from a single video (ST-AR + JDMD) | **24 FPS**, RotErr **2.8762** | real-time-4D neighbor, but reconstruction-from-video, not action-conditioned |
| [[2605.01799\|Embody4D]] | generalist 4D synthesizing novel views from mono video | data engine lifts robot SR **74% vs 32%** OOD | manufactures geometry as data, not an online action substrate |
| [[2605.15153\|Pelican-Unified]] | shared latent z + pixel-side generator | **93.5%** RoboTwin | multi-modal but not natively 4D-geometric |
| [[2411.04983\|DINO-WM]] | frozen DINOv2 + lightweight dynamics | appearance latent | no geometry channel |

**Hypotheses & tests.** The FP bet — native-4D beats lift-after on geometry-bound tasks at no deployment penalty, and the substrate is model-agnostic — decomposed.
1. **H1 — Native 4D beats lift-after-pixel on geometry-bound tasks.**
   - *Prediction*: holding the backbone fixed, [[2604.26694|X-WAM]]'s interleaved depth branch beats a pixel substrate + post-hoc depth estimator on geometry-bound [[2406.02523|RoboCasa]] tasks, isolating native-over-recovered 4D.
   - *Test*: native-4D vs pixel+post-hoc-depth at matched backbone on [[2406.02523|RoboCasa]] SR, with native-vs-recovered geometric fidelity scored on [[2603.03485|Phys4D]]'s per-frame-3D (AbsRel) + 4D-Chamfer protocol (the standardized native-vs-recovered measurement H1 otherwise reads off X-WAM's single self-reported Chamfer).
   - *Row*: X-WAM / GaussianDream.
   - *Falsifier*: recovered 4D matches native → online geometry is an unnecessary cost; train-time signal suffices.
2. **H2 — The async action schedule shrinks to 1–4 steps without degrading the read-out geometry.**
   - *Prediction*: generalizing Asynchronous Noise Sampling, the action denoising schedule shrinks to 1–4 steps (step-distillation) without degrading the 4D geometry a consumer reads.
   - *Test*: sweep action denoising steps; report geometry fidelity vs steps on [[2603.03485|Phys4D]]'s short-term-consistency + world-level-4D-Chamfer + Worldline-L2 tiers (the over-horizon geometric-degradation axis the step-distillation sweep needs, not just per-frame Chamfer).
   - *Row*: X-WAM.
   - *Falsifier*: fewer steps degrade geometry → the speedup trades away the substrate's value.
3. **H3 — Explicit 3D makes discrete contact-mode prediction easier than a latent.**
   - *Prediction*: an explicit 3D geometry channel lowers discrete contact-mode (penetration/proximity) prediction error vs a continuous latent, because geometry exposes contact directly.
   - *Test*: contact-mode classification, explicit-3D channel vs latent, matched data.
   - *Row*: X-WAM / VLA-JEPA.
   - *Falsifier*: latent matches explicit on contact → geometry isn't needed for the contact signal.
4. **H4 — End-effector-derived camera poses improve OOD geometry.**
   - *Prediction*: [[2604.26694|X-WAM]]'s end-effector→camera-pose self-consistency constraint improves OOD geometric fidelity vs free camera conditioning.
   - *Test*: ablate the end-effector-pose constraint; report OOD Chamfer.
   - *Row*: X-WAM / DeepVerse.
   - *Falsifier*: free camera matches → the self-consistency constraint is inert.
5. **H5 — A *native-4D-RGB-D-video* substrate transfers WM→policy as well as PointWorld's point-flow (settled-in-part, extend to RGB-D).**
   - *Prediction*: [[2601.03782|PointWorld]] already shows model-agnostic cross-embodiment transfer for a point-flow substrate; the open extension is whether a native-4D-RGB-D-video substrate ([[2604.26694|X-WAM]]'s) transfers WM→policy-head *with its appearance channel intact* — planning in explicit geometry beats latent on spatial tasks (insertion, stacking, pouring), and the same substrate plugged into a policy head matches its WM-consumer gain.
   - *Test*: 4D-plan vs latent-plan on spatial tasks via [[2602.08971|WorldArena]]'s action-planner + policy-evaluator tracks (does the WM substrate transfer to control); then swap the RGB-D substrate into an action head and score closed-loop physical executability on [[2604.19092|RoboWM-Bench]]'s step+final SR, comparing to the WM-consumer result and to PointWorld's point-flow transfer.
   - *Row*: X-WAM / PointWorld.
   - *Falsifier*: latent planning matches, or the RGB-D substrate transfers no better than point-flow → the appearance-carrying native-4D form adds nothing PointWorld didn't.

> [!warning] Risks
> - **4D supervision needs depth/3D ground truth** not present in most robot datasets. → Mitigate via [[2604.26694|X-WAM]]'s end-effector-derived camera poses + off-the-shelf depth estimators; bound the claim to tasks where geometry is recoverable.
> - **4D is only worth it on geometry-bound tasks** — on appearance-bound tasks latent already wins. → Score on contact / spatial tasks ([[2406.02523|RoboCasa]] insertion, stacking), not headline [[2306.03310|LIBERO]] SR; report the task-type split explicitly.
> - **Real-time 4D is now shown by two results** ([[2604.26694|X-WAM]] native-RGB-D, [[2601.03782|PointWorld]] point-flow) — so the open question is no longer "is it possible" but "does native-vs-recovered + async step-distillation pay." → Treat H1's native-vs-recovered Chamfer ablation and H2's latency-fidelity frontier as the go/no-go, conceding PointWorld owns the broad transfer claim.

### C4 — Persistent Geometric Memory as a Substrate-Agnostic Persistence Layer

| | |
|---|---|
| **Cluster** | C — Geometry-Native World Models & Memory |
| **Thesis** | That explicit geometric memory holds long-horizon coherence where attention-only models drift is now *settled* — [[2505.05495|3D Persistent Embodied WM]] showed it for an action-conditioned consumer. The unsolved question is whether one world-frame memory can serve as a *reusable persistence layer* over C1's occupancy, C2's pointmaps, and C3's latent-4D — and whether geometric + episodic memory *compound* on action-conditioned memory-required tasks. The field builds memory once, per substrate, and never benchmarks the two memory types together. The bet is in First-principles below. |
| **Anchor papers** | [[2604.22748\|Agentic World Modeling Survey]] (survey), [[2504.21853\|Interactive Generative Video Survey]] (survey), [[2602.04411\|Self-evolving Embodied AI]] (survey), [[2505.05495\|3D Persistent Embodied WM]] (method), [[2603.17117\|MosaicMem]] (method), [[2603.24576\|Chameleon (Episodic Memory)]] (method), [[2605.10921\|RoboMemArena]] (benchmark) |
| **Key targets** | Substrate-agnostic persistence: each of C1/C2/C3 + the C4 layer beats the bare substrate on minute-scale coherence, scored on [[2602.08025\|MIND-Bench]]'s closed-loop revisit memory-consistency + action-control metric (>**4%** context-memory gain on the long-context-memory metric, substrate-level not per-method); episodic+geometric compound > max(either) on [[2605.10921\|RoboMemArena]] (68.9% of subtasks need history); anchored to [[2505.05495\|3D Persistent Embodied WM]] SRC 81.7% / FVD 91.9 (vs no-memory 63.4 / 194), [[2603.17117\|MosaicMem]] RotErr 0.51° vs 1.42°/4.65° at 16 FPS, [[2603.24576\|Chameleon (Episodic Memory)]] 100% episodic-recall / 73.5% spatial-tracking |

**Why it matters.**
- **The gap**: the headline "explicit geometric memory beats attention-only on action-conditioned long-horizon coherence" is *already taken* — [[2505.05495|3D Persistent Embodied WM]] (PEWM) builds a volumetric world-frame memory, conditions an *action*-conditioned RGB-D WM on it, and beats the no-memory baseline (Scene-Revisit-Consistency **81.7%** vs **63.4%**, FVD **91.9** vs **194**) with downstream MPC/policy gains. So the open gap is not "does it help" but two things nobody has done: a memory layer that serves *any* substrate (C1/C2/C3), and a benchmark of geometric + episodic memory *together*.
- **Today's answers**: each memory type is built in isolation. Geometric: [[2603.17117|MosaicMem]] lifts 2D patches to 3D, RotErr **0.51°** vs 1.42°/4.65° at 16 FPS, but camera-controlled video not action-conditioned manipulation. Episodic: [[2603.24576|Chameleon (Episodic Memory)]] disambiguates indexable events (100% episodic-recall) but no persistent geometry. [[2506.05284|Long-Term Spatial Memory WM]] already combines geometric + episodic in *one* WM (PSNR **19.10** vs 11.71 baselines on view-recall) — but for camera-video, not benchmarked on action-conditioned memory-required tasks.
- **The opening**: [[2605.10921|RoboMemArena]] proves the demand is real and *action-conditioned* — **68.9%** of its subtasks genuinely need history and reactive policies fail them — giving the substrate-agnostic + compound bet a benchmark target that PEWM's revisit-coherence metric does not cover.

**First-principles framing.**
- **First principle**: a world-frame geometric memory is *substrate-orthogonal* — object permanence (where things are when they leave view and return) is a property of the metric frame, not of the representation that fills it, so the *same* persistence mechanism should pin C1's occupancy, C2's pointmaps, or C3's latent-4D. [[2505.05495|3D Persistent Embodied WM]] proves the mechanism on an RGB-D substrate; the principle says it is not tied to that substrate. And geometric and episodic memory are *complementary* primitives — one fixes *where*, the other fixes *which event* — so they should compound.
- **Assumption being challenged**: that memory is built once per substrate and that geometric vs episodic memory are alternatives, not complements. [[2505.05495|3D Persistent Embodied WM]] and [[2603.17117|MosaicMem]] each build a *bespoke* geometric memory for their own model; [[2603.24576|Chameleon (Episodic Memory)]] builds episodic memory alone; [[2506.05284|Long-Term Spatial Memory WM]] combines both but only for camera-video, never benchmarked on the action-conditioned memory tasks [[2605.10921|RoboMemArena]] defines.
- **The bet**: (i) a single world-frame memory layer, dropped over each of C1/C2/C3, raises minute-scale coherence above the bare substrate by a margin tracking [[2505.05495|3D Persistent Embodied WM]]'s SRC 81.7% vs 63.4% no-memory gap — i.e. the layer is substrate-agnostic, not substrate-bespoke; and (ii) geometric ([[2603.17117|MosaicMem]]) + episodic ([[2603.24576|Chameleon (Episodic Memory)]]) memory *compound* on [[2605.10921|RoboMemArena]] (combined > max(either) on the 68.9% history-required subtasks), because they address different failure modes — neither demonstrated by any single paper.

**Related research papers.** One table on the axis the direction turns on — *the memory representation* (geometric-3D-patch / episodic-events / world-frame-semantic / evolving-3D / tiered-consolidation / O(1)-TTT / controllable-no-memory) — with `Key result` and what each leaves missing for action-conditioned long-horizon coherence.

| System | Memory representation | Key result | What's missing |
|---|---|---|---|
| [[2505.05495\|3D Persistent Embodied WM]] | volumetric world-frame 3D-feature memory, *action*-conditioned RGB-D WM | SRC **81.7%** vs no-memory **63.4%**, FVD **91.9** vs **194**, 112-frame, MPC/policy gains | takes the bet's headline (action-conditioned geometric memory beats attention-only), but a *bespoke* memory for its own WM, indoor-nav, no substrate-agnostic layer or episodic compound |
| [[2603.17117\|MosaicMem]] | lifted-3D patches + Warped RoPE/Latent (hybrid) | RotErr **0.51°** vs 1.42°/4.65°, **16 FPS**, minute-level | camera-controlled video, not action-conditioned manipulation — the geometric half of the compound |
| [[2603.24576\|Chameleon (Episodic Memory)]] | disambiguated indexable episodic events + latent imagination | **100%** episodic-recall / **73.5%** spatial-tracking / **72.2%** sequential DSR | events, not persistent geometry — the episodic half of the compound |
| [[2506.05284\|Long-Term Spatial Memory WM]] | combined geometric + episodic memory in one WM | view-recall PSNR **19.10** vs 11.71 baselines, SSIM 0.647 vs 0.44 | pre-empts the compound (H2) but camera-video only — never run on action-conditioned RoboMemArena tasks |
| [[2509.20297\|mindmap]] | world-frame metric-semantic 3D reconstruction memory in an action policy | **76%** avg SR (+56% over 3D Diffuser Actor) on out-of-view spatial-memory tasks, 97% Mug-in-Drawer | closes the action-policy flank for *one* bespoke memory, but a single manipulation policy — not a substrate-agnostic layer, no episodic compound |
| [[2603.03482\|PERSIST]] | persistent 3D world-frame memory, generative WM | lower FVD/FID over **600-step** episodes, mid-generation 3D editing, off-screen dynamics | persistent-3D coherence, but camera/generation-side — not pinned to an action-conditioned policy or used as a cross-substrate layer |
| [[2605.22283\|SOMA]] | world-frame spatial-semantic (2D detections lifted to 3D) | cuts target-localization time **40–59%** | semantic memory, geometric-coherence drift not reported |
| [[2604.11302\|3D-ALP]] | persistent 3D memory + world-model MCTS | **0.650** SR on memory-required steps vs 0.006 reactive; memory = **82%** of gain | the action-conditioned object-permanence result; planner-coupled |
| [[2510.01183\|EvoWorld]] | explicit evolving 3D memory in a generative WM | FVD **106.81** vs GenEx 199.76, **93.3%** long-horizon target-reaching | camera-video memory, not pinned to an action-conditioned policy |
| [[2606.03374\|eMEM]] | tiered spatio-temporal memory + R-tree 3D index | flat recall to **1-year** simulated delay | consolidation architecture, not geometric-coherence-under-action |
| [[2605.22814\|Remember to be Curious]] | persistent 3DGS WM + long-term episodic memory | higher scene completeness HM3D/Gibson, RGB-only at test | exploration, not manipulation — episodic+geometry combined (H2 in one system) |
| [[2603.23497\|WildWorld]] | 108M-frame state-action long-horizon substrate | Action Following + State Alignment | a dataset/substrate, not a memory mechanism |
| [[2604.16484\|DexWorldModel]] | dual-state O(1) TTT memory | constant memory over 2,000 steps | efficiency, not geometric permanence — the contrast |
| [[2510.10125\|CTRL-WORLD]] | controllable video, no persistent memory | **38.7→83.4%** unseen objects | controllability without memory — the no-memory baseline |
| [[2503.14489\|SEVA]] | implicit-attention camera memory | RotErr 1.42° (the explicit baseline MosaicMem beats) | drifts vs hybrid geometric memory |
| [[2506.03141\|CaM]] | static explicit-3D cache | RotErr 4.65° | breaks on dynamic scenes |

**Hypotheses & tests.** The reframed bet — one world-frame memory is a substrate-agnostic persistence *layer*, and geometric + episodic memory *compound* on action-conditioned tasks — decomposed. (The headline "geometric memory beats attention-only for an action-conditioned consumer" is *settled* by [[2505.05495|3D Persistent Embodied WM]]; the front-line is the layer-reuse + compound nobody has run.)
1. **H1 — One world-frame memory layer transfers across C1/C2/C3 substrates.**
   - *Prediction*: dropping a single world-frame memory mechanism over C1's occupancy, C2's pointmaps, and C3's latent-4D raises each substrate's minute-scale coherence above the bare substrate by a margin tracking [[2505.05495|3D Persistent Embodied WM]]'s SRC 81.7% vs 63.4% gap — i.e. the layer is substrate-agnostic, not the bespoke per-model memory PEWM/MosaicMem built.
   - *Test*: each of C1/C2/C3 with vs without the shared C4 layer, scored on [[2602.08025|MIND-Bench]]'s closed-loop revisit memory-consistency + action-control metric (temporal stability + scene-revisit coherence, decoupled from any one method's bespoke metric) so the coherence lift is read off a substrate-level, model-agnostic suite rather than PEWM/MosaicMem self-numbers — though MIND-Bench is camera/scene-navigation, so it backs the coherence-metric + model-agnostic claim, not all three manipulation substrates by itself.
   - *Row*: 3D Persistent Embodied WM / MosaicMem.
   - *Falsifier*: the lift varies wildly per substrate or one substrate gets none → memory is substrate-bespoke, not a reusable layer.
2. **H2 — Episodic events + geometric memory compound on action-conditioned tasks.**
   - *Prediction*: combining [[2603.24576|Chameleon (Episodic Memory)]]'s indexable events with [[2603.17117|MosaicMem]]'s geometry-consistent patches beats either alone on [[2605.10921|RoboMemArena]] — extending [[2506.05284|Long-Term Spatial Memory WM]]'s camera-video compound to action-conditioned memory-required tasks, where disambiguated *events* + persistent *geometry* address different failure modes.
   - *Test*: events-only vs geometry-only vs both on RoboMemArena.
   - *Row*: Chameleon / MosaicMem / Long-Term Spatial Memory WM.
   - *Falsifier*: both ≈ max(either) → the two memory types are redundant, not complementary.
3. **H3 — The compound advantage concentrates on perceptual-aliasing + out-of-view subtasks.**
   - *Prediction*: decomposing [[2605.10921|RoboMemArena]] by subtask type, the episodic+geometric compound's margin over geometric-only is largest on perceptual-aliasing/occlusion subtasks (where events disambiguate) and ≈0 on pure-revisit subtasks (where geometry alone suffices).
   - *Test*: per-subtask margin of compound vs geometric-only on RoboMemArena's occlusion/counting/revisit splits.
   - *Row*: Chameleon / RoboMemArena.
   - *Falsifier*: a uniform margin across subtask types → episodic memory helps globally, not via aliasing-specific disambiguation.
4. **H4 — World-frame memory holds coherence better than robot-frame memory.**
   - *Prediction*: a geometric memory pinned to a persistent *world*-frame ([[2505.05495|3D Persistent Embodied WM]]'s action→camera-pose retrieval, [[2603.17117|MosaicMem]]'s lifted-3D patches) holds long-horizon coherence better than a robot-frame memory — decoupling memory from the body's pose reduces drift.
   - *Test*: world-frame vs robot-frame memory on long-horizon traversal; report drift.
   - *Row*: 3D Persistent Embodied WM / SOMA.
   - *Falsifier*: robot-frame matches world-frame → the frame choice doesn't drive drift.
5. **H5 — The substrate-agnostic layer costs less than substrate-bespoke memory at equal coherence.**
   - *Prediction*: a single shared C4 layer reaching PEWM-level coherence over all three substrates has a lower total parameter/memory footprint than three bespoke per-substrate memories ([[2505.05495|3D Persistent Embodied WM]] + occupancy-memory + pointmap-memory built separately), against [[2604.16484|DexWorldModel]]'s O(1) TTT budget.
   - *Test*: shared-layer vs three-bespoke-memories on (coherence × footprint) across C1/C2/C3 tasks.
   - *Row*: 3D Persistent Embodied WM / DexWorldModel.
   - *Falsifier*: the shared layer costs as much as three bespoke memories at equal coherence → reuse buys no efficiency, only engineering convenience.

> [!warning] Risks
> - **Explicit geometric memory needs reliable 3D lifting** — off-the-shelf estimators can fail on texture-poor scenes ([[2603.17117|MosaicMem]]). → Hybridize with implicit attention ([[2603.17117|MosaicMem]]'s own design) so the model degrades gracefully when lifting is noisy.
> - **Episodic memory retrieval can interfere** on visually-aliased-but-irrelevant events ([[2603.24576|Chameleon (Episodic Memory)]]). → Use disambiguated indexable encoding + goal-directed retrieval, not similarity-only retrieval; validate on [[2605.10921|RoboMemArena]]'s occlusion/counting splits.
> - **Memory adds footprint** against the real-time deployment budget. → H5's patch-level vs [[2604.16484|DexWorldModel]] O(1) TTT Pareto is the go/no-go; persistent memory only earns its place if coherence gain beats the memory cost.

---

## Cluster D — Reconstruction for Embodied Perception

*Reconstruction built for interaction-readiness — geometry that carries physics and kinematic structure, not just radiance. The two directions split by the unit of reconstruction: a whole scene an agent acts in (D1) and the reusable single object that populates it (D2), the same readiness-over-fidelity inversion applied at two scales.*

### D1 — Interaction-Ready Scene Reconstruction: Whole Environments You Can Act In

| | |
|---|---|
| **Cluster** | D — Reconstruction for Embodied Perception |
| **Thesis** | An embodied agent acts on *scene-level interaction-readiness* — geometric validity, physical parameterization, kinematic executability of a whole reconstructed environment — not on appearance. The reconstruction field optimizes visual fidelity (PSNR/FID) and assumes a higher-fidelity NeRF/3DGS scene is a better embodied asset. The bet is in First-principles below. |
| **Anchor papers** | [[2604.26509\|3D Generation for Embodied AI Survey]] (survey), [[2506.20134\|3D World Models Survey]] (survey), [[2510.16732\|World Models for Embodied AI Survey]] (survey), [[2505.17966\|Single-View Mesh for Robotics]] (benchmark), [[2404.09833\|Video2Game]] (method), [[2605.26115\|TriSplat]] (method), [[2506.06440\|Vid2Sim]] (method) |
| **Key targets** | Single-video → interactive environment at ≥100 FPS browser-compatible ([[2404.09833\|Video2Game]]); per-criterion readiness pass/fail on [[2505.17966\|Single-View Mesh for Robotics]]'s 5 robotics desiderata (Chamfer<**2 mm**, no-collision, stability<5° tilt, occlusion-robustness, <2 s — 12 recon models on YCB-Video + Aria, ~**50%** grasp transfer); simulation-readiness criteria met (geometric validity + physical parameterization + kinematic executability + URDF/MJCF compat) per [[2604.26509\|3D Generation for Embodied AI Survey]] |

**Why it matters.**
- **The gap**: the reconstruction community optimizes radiance (PSNR/SSIM/FID), and [[2604.26509|3D Generation for Embodied AI Survey]] names the mismatch as *the* embodied bottleneck — "a crucial distinction between conventional 3D generation (focused on visual appearance) and embodied-oriented 3D generation, which demands interaction readiness, physical grounding, and simulator compatibility," blocked by "scarcity of physical annotations."
- **Today's answers**: the sim-ready-twin-from-single-video build is *crowded* — [[2510.05560|HoloScene]] (NeurIPS'25) bakes physics into reconstruction (Isaac-Sim-in-the-loop), reports an Object-Readiness/Stable-Ratio metric (**81.7%** stable, **100%** object-reconstruction on Replica) *alongside* PSNR/SSIM, and surfaces the readiness-vs-fidelity trade-off as an ablation co-product; [[2404.09833|Video2Game]] fuses NeRF + baked mesh + physics at 100+ FPS; [[2605.26115|TriSplat]] outputs sim-loadable meshes (33–249× faster); [[2506.06440|Vid2Sim]] reconstructs appearance + geometry + physics. None runs the *controlled* readiness-vs-fidelity per-criterion comparison (same scene, PSNR-optimized vs the four readiness criteria), and all but HoloScene's future-work are rigid-body only.
- **The opening**: [[2406.10788|Embodied Gaussians]] couples a 3DGS render to PBD particles in a predict-correct loop at 30 Hz with lower tracking error — proof a physics-coupled reconstruction an agent acts in is buildable, not a downstream conversion of a fidelity asset.

**First-principles framing.**
- **First principle**: an embodied agent interacts with geometry, physics, and kinematics — not radiance. A reconstruction's embodied value is its *interaction-readiness* (can the agent collide, grasp, articulate in it), a property orthogonal to and not implied by visual fidelity. [[2003.08515|SAPIEN]] sets the kinematic-executability (URDF) bar a reconstructed scene must hit to be acted in.
- **Assumption being challenged**: the NeRF/3DGS default that higher-fidelity is a better asset is *already documented false* — [[2510.05560|HoloScene]]'s Table-3 ablation reports "a trade-off between scene-level reconstruction and instance-level physical stability," and [[2505.17966|Single-View Mesh for Robotics]] (RA-L'25) shows CV-benchmark-winning single-view reconstructions miss the 2 mm robotics bar (median Chamfer ~5 mm–1 cm, ~50% grasp transfer) with colliding/unstable objects. So the orthogonality *exists*; the open assumption D1 attacks is that a *single joint objective* surfacing it as a side-effect (HoloScene) suffices — when no one has run the *controlled* per-criterion measurement, nor recovered *articulation* readiness from single video (HoloScene's named future work).
- **The bet**: the deliverables are the *controlled measurement* and the *articulation* readiness HoloScene's joint objective leaves out — specifically, (i) building the same scene under (a) a PSNR objective vs (b) the survey's four readiness criteria, the fidelity-optimal asset fails ≥1 criterion measurably more often, reported per-criterion pass/fail (the controlled isolation HoloScene only surfaces as an ablation co-product); and (ii) single-video reconstruction recovers rigid decomposition reliably but fails articulated structure (joints/DoF) for URDF/MJCF export without multi-view or interaction data — the rigid-body ceiling HoloScene names but does not cross.

**Related research papers.** One table on the axis the direction turns on — *what the reconstruction outputs for embodied use* (physics-baked-scene / sim-format-mesh / scene-physics-for-sim / physics-coupled-render / dynamics-carrying-3DGS / articulation-reference / transfer-gap-neighbor) — with `Key result` and what each leaves missing. The transfer-gap rows are the [[Sim2Real|Sim2Real]] neighbors D1 borders but does not own.

| System | Reconstruction output | Key result | What's missing |
|---|---|---|---|
| [[2404.09833\|Video2Game]] | single-video → NeRF + baked mesh + rigid-body physics | **100+ FPS** browser-compatible interactive environment | rigid entities only — articulated structure from single video unproven |
| [[2510.05560\|HoloScene]] | single-video → sim-ready interactive twin, Isaac-Sim-in-the-loop | **81.7%** stable-ratio, **100%** object-reconstruction (Replica); Table-3 fidelity-vs-stability trade-off | reports the orthogonality as an ablation co-product, not D1's controlled per-criterion measurement; rigid-body only (articulation named as future work) |
| [[2505.17966\|Single-View Mesh for Robotics]] | per-criterion readiness scorecard over 12 single-view recon models (benchmark) | 5 robotics desiderata (Chamfer<2 mm / no-collision / stability<5° / occlusion / <2 s); most miss **2 mm** bar (~5 mm–1 cm Chamfer), ~**50%** grasp transfer, colliding/unstable poses | the standardized per-criterion readiness protocol H1 needs (object-level on YCB-Video + Aria), but a one-sided probe — no readiness-*optimizing* pipeline, no scene-level dual-objective isolation |
| [[2603.14010\|URDF-Anything+]] | image→articulated URDF generation | Part IoU **0.879**, Joint-Axis-Err **0.129 rad**, zero-shot real laptop 100% / drawer 90% | recovers articulation→URDF (D1's H2 gap), but from a curated image, not in-the-wild single video of a whole scene |
| [[2506.08334\|iTACO]] | casual-capture → articulated object reconstruction | Joint-Axis-Err **0.32 rad** (vs 0.82–1.16), type-error **15.9%** (vs 40–89%) | articulation from casual capture, but per-object — not whole-scene articulated decomposition for an act-in environment |
| [[2509.17647\|VideoArtGS]] | monocular video → articulated digital twin (3DGS) | revolute-axis error **0.32°** (vs 13.83°), position error **0.42 cm** | the single-video articulation path D1's H2 needs, but object-level twins, not a readiness-scored scene |
| [[2605.26115\|TriSplat]] | feed-forward triangle meshes loadable in Isaac Sim/Unity | **33–249×** faster than Gaussian baselines, no post-hoc meshing | simulator-format geometry, but no physical parameterization baked in |
| [[2506.06440\|Vid2Sim]] | appearance + geometry + physics for mesh-free scene sim | reconstruction optimized for the simulator, not the renderer | scene physics, but readiness-vs-fidelity not quantified |
| [[2406.10788\|Embodied Gaussians]] | 3DGS render + PBD particles in a predict-correct loop | **30 Hz** on 3 cameras, lower tracking error | physics-coupled, but a tracking WM more than a reusable asset |
| [[2411.12789\|Sim-GS]] | open-vocab 3DGS + MLLM zero-shot per-object material (density / Young's / Poisson) for MPM sim | physics-based 4D scene dynamics in **~2 min** on one GPU (vs 0.1–1.5 hr) | infers scene material *zero-shot* but doesn't score readiness-vs-fidelity; material is predicted, not validated against contact |
| [[2403.08321\|ManiGaussian]] | 3DGS world model carrying dynamics for manipulation | dynamics-carrying scene reconstructions | dynamics for action, but not a full readiness scorecard |
| [[2003.08515\|SAPIEN]] | articulated-object simulator (URDF reference) | the kinematic-executability bar | hand-authored assets, not reconstructed-for-readiness |
| [[2604.25459\|GS-Playground]] | high-throughput 3DGS sim (Sim2Real-A1 neighbor) | **90%** real SR | minimizes the transfer gap *given* an asset — not readiness itself |
| [[2511.04665\|Real-to-Sim GS]] | 3DGS + soft-body digital twins (Sim2Real-B1 neighbor) | **r=0.915** sim-real correlation | reconstruction-for-transfer, not interaction-readiness as the target |
| [[2604.26509\|3D Generation for Embodied AI Survey]] | the four readiness criteria | "simulation-readiness over visual fidelity" | the organizing frame — names criteria, prescribes no pipeline |
| [[2510.16732\|World Models for Embodied AI Survey]] | reconstruction → geometry for world models | the D→C handoff | survey framing only |

**Hypotheses & tests.** The FP bet — readiness, not fidelity, is the embodied target, and it is reachable from single video — decomposed.
1. **H1 — Fidelity-optimal scenes fail readiness criteria measurably more often (controlled, beyond HoloScene's co-product).**
   - *Prediction*: building the same scene optimizing (a) PSNR vs (b) [[2604.26509|3D Generation for Embodied AI Survey]]'s four readiness criteria, the fidelity-optimal asset fails ≥1 readiness criterion substantially more often — the *controlled* per-criterion isolation [[2510.05560|HoloScene]] surfaces only as a Table-3 trade-off ablation and [[2505.17966|Single-View Mesh for Robotics]] shows only as a one-sided probe.
   - *Test*: dual-objective reconstruction on a matched scene set; report per-criterion pass/fail rates against [[2505.17966|Single-View Mesh for Robotics]]'s 5-desiderata protocol (Chamfer<2 mm / no-collision / stability<5° / occlusion / <2 s + grasp-transfer SR), the standardized per-criterion readiness scorecard the card otherwise treats as nonexistent.
   - *Row*: HoloScene / Single-View Mesh for Robotics / 3D Generation for Embodied AI Survey.
   - *Falsifier*: fidelity-optimal assets also pass readiness → fidelity and readiness aren't orthogonal.
2. **H2 — Single-video recovers rigid structure but not articulation (the ceiling HoloScene names).**
   - *Prediction*: [[2404.09833|Video2Game]]/[[2510.05560|HoloScene]]-style single-video reconstruction recovers rigid-entity decomposition reliably but fails articulated structure (joints, DoF) for URDF/MJCF export without multi-view or interaction data — closable by porting the [[2603.14010|URDF-Anything+]] / [[2506.08334|iTACO]] / [[2509.17647|VideoArtGS]] articulation path into the scene pipeline.
   - *Test*: single-video vs multi-view kinematic recovery on articulated scenes; report URDF-exportability + joint-axis/type error on [[2604.05621|FunRec]]'s RealFun4D (the only scene-level articulated-readiness suite — 127 photorealistic sequences in 12 OmniGibson scenes + a real counterpart, URDF/USD-exportable, part-mIoU / joint-axis / pose metrics), with [[2603.19231|MonoArt]] establishing the single-image articulation ceiling on PartNet-Mobility (Chamfer **0.77**, type-accuracy **88.26%**).
   - *Row*: VideoArtGS / URDF-Anything+ / SAPIEN.
   - *Falsifier*: single-video recovers articulation directly → the multi-view requirement is unnecessary.
3. **H3 — A readiness threshold for physical parameters exists below sim-accurate fidelity.**
   - *Prediction*: a policy trained in the reconstructed asset acts correctly once physical parameters (mass, friction, restitution) cross a *sufficiency* threshold well below sim-accurate fidelity — readiness is a threshold, not a fidelity race.
   - *Test*: degrade physical-parameter fidelity; locate the SR-preserving threshold.
   - *Row*: Vid2Sim / Embodied Gaussians.
   - *Falsifier*: SR scales smoothly with parameter fidelity (no threshold) → readiness reduces to the transfer-gap question Sim2Real owns.
4. **H4 — A readiness-asset feeds A1 and C1 end-to-end.**
   - *Prediction*: a D1 interaction-ready asset directly feeds A1's point-cloud head (act-on geometry) and C1's occupancy WM (rollout-over geometry), and the end-to-end D→A and D→C chains match hand-built-asset baselines.
   - *Test*: drive A1/C1 from a D1 asset vs a hand-built asset; compare downstream SR.
   - *Row*: Video2Game / TriSplat.
   - *Falsifier*: the reconstructed asset underperforms hand-built downstream → readiness isn't yet sufficient for the consumer.
5. **H5 — Simulator-format output beats post-hoc meshing for readiness.**
   - *Prediction*: [[2605.26115|TriSplat]]'s feed-forward simulator-format mesh passes the kinematic-executability + format-compat criteria more reliably (and far faster) than meshing a fidelity-optimized 3DGS scene post-hoc.
   - *Test*: feed-forward sim-mesh vs post-hoc-meshed 3DGS on the format-compat + executability criteria.
   - *Row*: TriSplat / Video2Game.
   - *Falsifier*: post-hoc meshing matches feed-forward on readiness → simulator-format output is a speed win only, not a readiness one.

> [!warning] Risks
> - **Interaction-readiness lacks a standard benchmark** — readiness is a checklist, not a leaderboard number. → Adopt [[2604.26509|3D Generation for Embodied AI Survey]]'s four criteria as the explicit scorecard (H1) and report per-criterion pass/fail, not a single fidelity number.
> - **Single-video may not recover articulation/physics** for complex scenes. → H2 bounds what single-video reconstruction can recover; fall back to multi-view or interaction data where articulation needs it, and state the boundary.
> - **Boundary blur with [[Sim2Real|Sim2Real]]-A1/B1.** → Keep D1 pinned to *readiness as the optimization target* (H1, H3) and explicitly route the *transfer-gap evaluation* to [[2604.25459|GS-Playground]] / [[2511.04665|Real-to-Sim GS]].

### D2 — Object-Level Physical-Asset Generation: One Object That Carries Its Own Physics

| | |
|---|---|
| **Cluster** | D — Reconstruction for Embodied Perception |
| **Thesis** | The reusable unit of an interactive environment is the *object*, not the scene — and an object is only embodied-useful if it carries its own material, mass, and kinematic structure, not just a watertight mesh. The 3D-generation field treats geometry and physics as separable stages: generate appearance first, annotate physics later (or never), and assumes deformable/articulated assets can be hand-authored. The bet is in First-principles below. |
| **Anchor papers** | [[2604.26509\|3D Generation for Embodied AI Survey]] (survey), [[2506.20134\|3D World Models Survey]] (survey), [[2605.21572\|PhysX-Omni]] (method), [[2605.05163\|PhysForge]] (method), [[2605.30347\|NeuROK]] (method), [[2503.17973\|PhysTwin]] (method), [[2311.12198\|PhysGaussian]] (method) |
| **Key targets** | Per-object kinematic score ≥0.92 ([[2605.21572\|PhysX-Omni]] PhysXVerse); Chamfer-L1 ≤0.028 / IoU ≥0.764 ([[2605.30347\|NeuROK]]); deformable-twin Hand Chamfer ≤7.17 mm ([[2605.09538\|PhysHanDI]]); cover rigid + deformable + articulated in one generator; PhysX-Bench readiness across material / affordance / kinematics |

**Why it matters.**
- **The gap**: D1 builds a whole scene you can act in, but the scene's *reusable parts* are objects — and a fidelity-first object is a hollow prop, a watertight surface with no mass, friction, or joints. [[2604.26509|3D Generation for Embodied AI Survey]] names the sharpest version at the object level: the "trade-off between geometric quality and physical validity" and "scarcity of physical annotations," with *deformable assets* called out as unsolved.
- **Today's answers**: the unified generator + scorecard the bet proposed to *build* is *already built* — the card's own anchor [[2605.21572|PhysX-Omni]] is titled for unified rigid+deformable+articulated generation and ships PhysX-Bench (six readiness attributes), and [[2504.12684|SOPHY]] already ran D2's *own* H1 ablation (joint vs geometry-first: material-class +>20%, sim-Chamfer **5×** lower) and H2 prediction (it *skips* rigid because rigid nearly suffices). The rigid+articulated half is owned in one pass by [[2511.13648|PhysX-Anything]] (abs-scale error **43.44→0.30**, MuJoCo-importable) and [[2511.21887|UniArt]] (>**85%** retention on unseen categories vs <60% baselines). [[2605.05163|PhysForge]] / [[2605.30347|NeuROK]] add kinematics/energy-conservation; [[2503.17973|PhysTwin]] / [[2605.09538|PhysHanDI]] deformable twins. None runs a *matched-object joint-vs-staged* head-to-head decomposed per-class on one scorecard.
- **The opening**: [[2406.04338|Physics3D]] recovers material parameterization from video diffusion with *no annotation*, and [[2412.17804|GausSim]] runs a per-object elastic rollout (L2 1.85 vs 11.32) with mass/momentum conservation — proof physics-consistent generation is buildable without a physics-annotation step.

**First-principles framing.**
- **First principle**: an object's embodied value is a *joint* (geometry, material, kinematics) — the physics is not a separable post-hoc label but a property the geometry must be generated *consistent with* (a mesh and its mass/friction/joints co-determine how it behaves under contact). Splitting them discards the consistency a single-pass generator could enforce; [[2311.12198|PhysGaussian]] shows continuum mechanics baked into the Gaussians themselves is the consistent form.
- **Assumption being challenged**: the geometry-first convention (NeRF/3DGS-then-annotate) is *already refuted* — [[2605.21572|PhysX-Omni]], [[2504.12684|SOPHY]], and [[2511.21887|UniArt]] each generate physics-with-geometry in one pass and generalize to unseen categories. So "build the unified generator" is settled. The open assumption D2 attacks: that demonstrating a unified generator *exists* proves joint > staged — when no paper has run the *matched-object controlled comparison*, nor tested whether energy/momentum-consistency (not fidelity) is what predicts *out-of-category* readiness.
- **The bet**: the controlled falsifier nobody has run unified — not the generator [[2605.21572|PhysX-Omni]] already built — decides it: (i) generating the *same* matched object set (a) geometry-first-then-annotate vs (b) jointly via a PhysX-Omni-style unified head, the staged pipeline fails the kinematic/material readiness criterion substantially more often, decomposed per-class with the advantage concentrated on deformable + articulated (≈0 on rigid props), as [[2504.12684|SOPHY]]'s skip-rigid choice already hints; and (ii) a physical-consistency metric (energy/momentum, [[2605.30347|NeuROK]]-style, Chamfer-L1 ≤0.028) predicts out-of-category readiness better than fidelity (PSNR/Chamfer) — the generalization signal no scorecard isolates.

**Related research papers.** One table on the axis the direction turns on — *how per-object physics is recovered* (unified-joint-generation / generative-kinematics / deformable-twin-from-video / hand-object-twin / baked-into-Gaussians / elastic-simulator / from-video-diffusion) — with `Key result` and what each leaves missing. The contrast is joint generation (physics-with-geometry) vs staged annotation.

| System | Per-object physics recovery | Key result | What's missing |
|---|---|---|---|
| [[2605.21572\|PhysX-Omni]] | unified generator: rigid + deformable + articulated, physics baked | kinematic **0.9185** PhysXVerse, abs-scale **2.79** vs >298, deployed in policy learning | the card's own anchor already ships the unified generator + PhysX-Bench scorecard — but never the matched joint-vs-staged controlled comparison; deformable readiness undertested |
| [[2504.12684\|SOPHY]] | joint shape + material generation (deformable-focused) | material-class accuracy **+>20%**, deformation Sim-CD **5×** lower vs geometry-first baseline | runs D2's own H1 (joint vs geometry-first) + H2 (skips rigid as nearly-sufficient) on deformable — but deformable-only, no cross-class scorecard or energy-predicts-OOD test |
| [[2511.13648\|PhysX-Anything]] | single-image → physics-grounded asset, MuJoCo-importable | abs-scale error **43.44→0.30**, VLM geometry/kinematics **0.94**, contact-rich policy learning | rigid+articulated one pass with URDF, but doesn't isolate joint-vs-staged or run the per-class deformable comparison |
| [[2507.12465\|PhysX-3D]] | physics-grounded 3D generation (PhysXNet, 6M assets) | PSNR **24.53**, abs-scale error **7.24** vs 13.21, material **13.01** vs 8.63, affordance **11.30** vs 7.23 | the data+generator scale, but reports aggregate fidelity+physics, not a controlled joint-vs-staged per-class readiness split |
| [[2511.21887\|UniArt]] | unified articulated-object generation + URDF | PSNR **28.52** rest / 23.77 articulated, **>85%** retention on unseen categories (vs <60%) | owns the articulated half with strong OOD, but articulated-only — not the cross-class joint-vs-staged falsifier |
| [[2605.05163\|PhysForge]] | two-stage VLM physical-planning + diffusion realizing geometry **and** continuous kinematic params (KVI) | Joint-Axis-Err-5 **0.101** (SOTA), assets simulation-ready in robotic sims | strong on articulated kinematics, but physics-property breadth (material/deformable) less validated than PhysX-Omni |
| [[2605.30347\|NeuROK]] | generative 4D neural object kinematics, energy-conserving | Chamfer-L1 **0.028**, IoU **0.764**, **83.33%/81.43%** user-pref on unseen categories | kinematics-consistent, but material parameters not the focus |
| [[2503.17973\|PhysTwin]] | physics-informed deformable twin from video | real-time sim + robotic motion planning | per-object deformable, single-instance — not a category generator |
| [[2605.09538\|PhysHanDI]] | hand–deformable-object physics twin from sparse RGB-D | Hand Chamfer **7.57→7.17 mm**, ~2×/>7× lower spring RRD than PhysTwin | contact-rich deformable case, but hand-object-specific |
| [[2311.12198\|PhysGaussian]] | continuum mechanics baked into Gaussians (elastic/plastic/fracture) | physical parameterization in the 3DGS object itself | per-object physics, but not a generator across categories |
| [[2412.11258\|GaussianProperty]] | training-free SAM part-seg + LMM material reasoning, voted onto 3D Gaussians | **55.83%** mIoU material seg (vs Nerf2Physics 25.59%), **100%** real adaptive-grasp success | tags material onto a *given* mesh — recovery, not generation; no kinematic structure |
| [[2412.17804\|GausSim]] | continuum elastic Gaussian simulator | L2 **1.85** vs 11.32, **95%** fewer computations, 0.13 s/frame | elastic rollout, not asset generation |
| [[2406.04338\|Physics3D]] | material parameterization from video diffusion (no annotation) | PSNR **14.72**, material recovered annotation-free | the recover-physics-from-appearance variant — fidelity-limited |
| [[2505.16971\|UniPhy]] | unified neural constitutive model — inverse material inference from observed 3D motion | elastic reconstruction error **5.2e-6** vs **2.4e-4** (NCLaw), material-type-agnostic | infers material *post-hoc* from motion — needs an observed trajectory, not a one-pass generator |
| [[2604.26509\|3D Generation for Embodied AI Survey]] | the geometry-vs-physics trade-off + deformable gap | names the bottleneck | the organizing frame — prescribes no generator |
| [[2003.08515\|SAPIEN]] | articulated-object simulator (URDF reference) | the kinematic-executability bar a generated object must hit | hand-authored, not generated |

**Hypotheses & tests.** The FP bet — joint physics-geometry generation hits per-object readiness across categories where staged annotation fails, largest on deformable/articulated — decomposed.
1. **H1 — Joint generation passes the kinematic/material criterion the staged pipeline fails (extend SOPHY's deformable result cross-class).**
   - *Prediction*: generating the same matched object set (a) geometry-first then annotate vs (b) jointly via a [[2605.21572|PhysX-Omni]]-style unified head, the staged pipeline fails the kinematic/material readiness criterion substantially more often — [[2504.12684|SOPHY]] already showed this on *deformable* (material +>20%, Sim-CD 5×); the open test is whether it holds across rigid + deformable + articulated *on one scorecard*.
   - *Test*: dual-pipeline generation; per-criterion readiness ([[2604.26509|3D Generation for Embodied AI Survey]]'s four) on a matched object set spanning all three classes.
   - *Row*: PhysX-Omni / SOPHY.
   - *Falsifier*: staged annotation passes as often as joint outside deformable → the consistency the joint pass enforces isn't load-bearing beyond SOPHY's class.
2. **H2 — The joint-generation advantage concentrates on deformable + articulated objects (SOPHY's skip-rigid choice, made explicit).**
   - *Prediction*: decomposing readiness by class, the joint-generation advantage is near-zero on rigid props (a mesh nearly suffices — why [[2504.12684|SOPHY]] *skipped* rigid) and concentrated on deformable + articulated, as the first principle predicts.
   - *Test*: per-class (rigid/deformable/articulated) readiness comparison, joint vs staged.
   - *Row*: SOPHY / PhysX-Anything / PhysHanDI.
   - *Falsifier*: the advantage is uniform across classes → physics-with-geometry helps everywhere, not specifically the hard cases.
3. **H3 — Energy-conservation predicts out-of-category readiness better than fidelity.**
   - *Prediction*: enforcing a physical-consistency constraint (energy, momentum, [[2412.17804|GausSim]]'s mass conservation) at generation time predicts out-of-category readiness better than fidelity (PSNR/Chamfer) alone — mirroring [[2605.30347|NeuROK]]'s energy-conserving generalization.
   - *Test*: regress out-of-category readiness on a consistency metric vs a fidelity metric — using [[2503.21745|3DGen-Bench]]'s standardized human-preference fidelity yardstick (3DGen-Score, **0.725/0.767** human-alignment for text/image-to-3D) as the *fidelity arm* the consistency-vs-fidelity comparison structurally requires (cited only as the fidelity comparator — never as a physical-readiness backer, which would invert the bet's contrast).
   - *Row*: NeuROK / GausSim.
   - *Falsifier*: fidelity predicts out-of-category readiness as well → physical consistency isn't the generalization signal.
4. **H4 — A generated object transfers to a sim-trained policy via material *or* kinematics.**
   - *Prediction*: a D2 physics-jointly-generated object dropped into a D1 scene lets a sim-trained policy act correctly, and the binding constraint is identifiable as either per-object material fidelity (mass/friction) or kinematic structure — not both equally.
   - *Test*: ablate material-fidelity vs kinematic-structure on the generated object; report which gates transfer.
   - *Row*: PhysX-Omni / NeuROK.
   - *Falsifier*: neither ablation degrades transfer → the object's physics isn't the transfer constraint.
5. **H5 — Deformable readiness is the widest gap and the largest single-pass win.**
   - *Prediction*: on the survey-named deformable gap, a joint generator ([[2605.09538|PhysHanDI]]-class deformable twin) closes more of the readiness gap than any staged pipeline can, and deformable is where the staged pipeline fails hardest.
   - *Test*: deformable-class readiness, joint generator vs staged, vs the survey-named baseline.
   - *Row*: PhysHanDI / PhysTwin.
   - *Falsifier*: staged pipelines close the deformable gap comparably → deformable isn't the distinguishing case.

> [!warning] Risks
> - **Per-object readiness has no shared leaderboard across categories** — PhysX-Bench is rigid/articulated-leaning, PhysTwin/PhysHanDI are deformable-specific. → Adopt [[2604.26509|3D Generation for Embodied AI Survey]]'s four criteria as the common scorecard (H1) and report per-class (rigid/deformable/articulated) pass/fail, not one aggregate.
> - **Physical parameters from a single video / sparse RGB-D may be under-determined** (mass/friction unobservable from kinematics alone). → H3's physical-consistency constraints (energy/momentum) regularize the under-determined parameters; bound the claim to where the constraint identifies them.
> - **Boundary blur with D1** if "object" and "scene" leak. → Pin D2 to the *single-object* generation unit (H2, H4) and D1 to *whole-scene* environments; a D2 object *populating* a D1 scene is the intended composition (H4), not an overlap.

---

## Cross-Cutting Themes

> [!tip] Geometry Is What the Task Keeps Fixed; Appearance Is Noise
> A1, A3, B2, C1, and C2 all make the same move: build the representation around the geometry the *task* keeps fixed (where things are, how they persist in 3D), not the appearance the *rendering* adds. The bets are independent but converge on one falsifiable claim — A1 predicts the geometry-vs-RGB gap *widens* under appearance shift; B2 predicts the 4D-*consistency* constraint (not raw 3D) drives OOD robustness; C2 predicts cross-view *consistency* (not RGB fidelity) drives the ≈5× action gain. Three directions, one claim: the geometric channel, not the appearance channel, carries the action-relevant signal. This is the Hinton tenet that the brain plans in world coordinates, not image coordinates, turned into a measurable bet — and the diagnostics ([[2605.30161|Why Far Looks Up]]'s shortcut gap, [[2604.24300|ReVSI]]'s hallucination) show the field's RGB default is exactly the failure mode.

> [!tip] The RGB-Token Tax Is Paid at Every Layer of the Stack
> The representation-supervision bottleneck [[2606.03943|PointAction]] names isn't local to the policy — it shows up at every layer, which is why A1/A3, B1/B2, C1/C2, and D1/D2 *stack* instead of compete. A1/A3 pay the tax at the *action head*; B1/B2 at the *cognition layer* (ungrounded language over RGB); C1/C2/C3 at the *world-model substrate* (latent/pixel rollouts that re-parse geometry); D1/D2 at the *asset* (fidelity-optimized scenes and objects that aren't interaction-ready). Each cluster removes the tax at its layer, and the gains *compound down the stack*: a D2 object populates a D1 scene, which feeds A1's geometric head and C1's occupancy WM; a B1 scene-graph feeds A1's action head; B2's consistency is the temporal half of B1's spatial grounding. The whole is one geometric pipeline, not five isolated tricks.

> [!tip] Cheap Geometry vs Full Geometry — A Frontier, Not a Binary
> A3, B2, and C1 each sit at the *cheap* end of a cost/capability frontier whose expensive end a sibling owns. A3's single-view depth-token bridge is the cheap version of A1's full point branch (≥80% of the gain at side-channel cost); B2's implicit 4D-consistency is the cheap version of C2's explicit pointmap generation (same accuracy, 2.31× faster, no frame generation); C1's externally-readable occupancy is the long-horizon-cheap complement to C3's per-frame-expensive latent-4D. The non-consensus reading: the field frames these as either/or (RGB vs 3D, implicit vs explicit, latent vs occupancy), but each pair is a *frontier* whose operating point is task-conditional — cheap geometry for transit/appearance-bound segments, full geometry for contact/spatial-bound ones. The research question isn't "which substrate wins" but "where is the crossover" — measured in A1-H1, A3-H1, B2-H4, C1-H1.

> [!tip] Explicit-External ↔ Latent-Internal Is the Doc's Deepest Axis (and the Real C-vs-B Line)
> The deepest split in the doc isn't 2D-vs-3D but *who reads the geometry*, and it cuts across clusters. B1 and B2 keep it *internal* — a scene-graph or consistency-attention the action head consumes end-to-end (cheaper, less inspectable). C1, C2, and D1 make it *external* — occupancy a third-party planner reads (C1), pointmaps a tracker reads for 6-DoF (C2), assets a simulator loads (D1). Externality buys debuggability, composability, and tool-reuse (C1-H2, C2-H4) at the cost of a decoder/extractor step. This is also Cluster C's *internal* organizing principle: C3 ([[2604.26694|X-WAM]]) keeps its 4D latent *internal* (decoded for imagination), C1/C2 keep geometry *external*, and C4 makes whichever persist — the split lives *inside* one cluster, not across the [[WAM|WAM]] boundary. The same axis cleanly separates B2 (implicit, internal) from C2 (explicit, external) on the overlapping 4D-consistency idea.

---

## Benchmark Gaps

| Gap | Direction | Existing closest |
|---|---|---|
| No benchmark isolates *cross-embodiment appearance-shift* SR to test the geometry-vs-RGB claim — current suites mix appearance and geometry shift | A1 | [[2606.03943\|PointAction]] xArm7 zero-shot (43.0%) conflates embodiment + appearance + geometry in one number; the gap is now *narrowed via two single-axis benchmarks* — [[2505.14986\|AnyBody]] isolates the embodiment axis (18 morphologies, interpolation/extrapolation/composition splits, reach/push only) and [[2509.18953\|Eva-VLA]] the real-world appearance axis (graded illumination + 3D-transform + patches, per-variation failure rates), but no single suite does both on contact-rich tasks |
| No manipulation benchmark measures *rollout-horizon-to-geometric-divergence* for forward models — SR is reported at fixed horizon, hiding stability | A2 | [[2604.19092\|RoboWM-Bench]] scores WM→executable-action→step+final SR (discriminative beyond fixed-horizon, but SR not geometric divergence), [[2604.22152\|dWorldEval]] measures pixel drift over a 20-step rollout (LPIPS, round-trip consistency), and [[2510.18135\|World-in-World]] standardizes closed-loop WM utility — but none scores *geometric* divergence at sub-cm voxel resolution (the only occupancy-forecasting suites — UniOcc driving, restructured OccWorld-ScanNet inside [[2505.05512\|Occupancy World Model]] — have no tabletop analog), the residual A2 fills |
| No benchmark reports the *recovery-fraction* of a cheap depth-bridge vs a full-3D branch on a common backbone — gains are vs weak RGB baselines, not the full-3D ceiling | A3 | [[2306.03310\|LIBERO]]-Spatial/long-horizon is the named SR substrate, but no protocol plots recovery-fraction vs [[2508.09071\|GeoVLA]]'s full-3D ceiling (97.7%) on one backbone ([[2510.14836\|QDepth-VLA]] +8.8% / +29.7% over open_pi_0 — never head-to-head); the alignment-preservation half (H4) has only [[2505.05456\|SITE]]'s spatial-VQA→SR correlation (0.902), which links alignment to SR but not the recovery-fraction frontier — both protocols remain genuine gaps |
| No benchmark splits the human-model spatial gap into *reasoning* vs *perception* failure, nor isolates *genuine metric 3D* from *shortcut* answering | B1 | [[2601.13304\|CausalSpatial]] (GPT-5 54.17% vs human 84.49%) measures the gap; [[2605.29074\|Embodied3DBench]], [[2605.30161\|Why Far Looks Up]] (36.9 pp), [[2605.30557\|SpatialUncertain]] diagnose the shortcut; for the metric-vs-shortcut isolation, [[2412.07825\|3DSRBench]] (12 relation types, FlipEval/CircularEval controls, 6D-viewpoint OOD) and [[2506.03135\|OmniSpatial]] (50 subcategories + built-in PointGraph scene-graph baseline) are the closest standardized substrates — but neither reports graph-construction accuracy separately from answer accuracy, and none isolate reasoning from depth-perception on one probe (H5 stays open) |
| No benchmark plots the *implicit-vs-explicit 4D* cost/accuracy frontier at matched accuracy | B2 | [[2603.22078\|WAM vs VLA Robustness]] already plots the implicit-VLA-vs-explicit-generation-WAM SR×latency frontier (WAMs ≥4.8× slower than π0.5's 63 ms/chunk) over a shared LIBERO-Plus + RoboTwin-2.0-Plus suite, and [[2510.13626\|LIBERO-Plus]] supplies the factor-decomposed OOD axis — so the residual gap narrows to: no benchmark plots the frontier with *perception held fixed* (the consistency-as-driver isolation H1 needs), only architecture-family comparisons |
| No manipulation benchmark stress-tests *long-horizon geometric coherence* of occupancy vs latent at sub-cm resolution | C1 | [[2604.19092\|RoboWM-Bench]] supplies the manipulation rollout substrate (step+final SR, discriminative beyond perceptual metrics) and [[2604.22152\|dWorldEval]] the horizon-DRIFT metric (round-trip LPIPS@20-step), but both score pixel/video drift — no benchmark measures sub-cm *occupancy*-geometric horizon-to-divergence at tabletop scale (all 3D occupancy-forecasting suites are driving — Cam4DOcc/UniOcc/Occ3D-nuScenes — or static indoor — Occ-ScanNet/RoboOcc, no temporal horizon); the sub-cm occupancy variant (H4 + occupancy half of H1) is a true field gap |
| No benchmark isolates *6-DoF-extraction accuracy from predicted vs sensed geometry* across viewpoints | C2 | [[2604.19092\|RoboWM-Bench]] (executability-vs-perceptual discrimination, step+final SR) and [[2602.08971\|WorldArena]] (perception–functionality gap) provide the discriminative predicted-video→action SR axis the headline needs, but neither isolates 6-DoF-extraction-accuracy from predicted vs sensed geometry across viewpoints — that predicted-vs-sensed pose-readout isolation (H2/H3) remains a genuine field gap (FoundationPose-as-tracker is the method, no standardized suite scores it) |
| No benchmark scores *native-4D-at-deployment vs lift-after-pixel* on geometry-bound tasks (Chamfer + SR + latency jointly), nor whether the latent-4D substrate transfers WM↔policy | C3 | [[2603.03485\|Phys4D]] scores geometry-over-horizon (per-frame AbsRel → 4D-Chamfer → Worldline-L2) and [[2602.08971\|WorldArena]] scores WM functional utility (action-planner / policy-evaluator), with [[2406.02523\|RoboCasa]] the in-dist SR substrate — but none isolates the *single-system matched-backbone* native-4D-at-deploy vs lift-after-pixel head-to-head scoring Chamfer-over-horizon + SR + latency on one plane (H3/H4 stay method-internal) |
| No benchmark scores *persistent geometric + episodic memory* on memory-dependent manipulation over minute-scale horizons, model-agnostic across substrates | C4 | [[2602.08025\|MIND-Bench]] is the model-agnostic memory-CONSISTENCY benchmark (closed-loop revisit-coherence + action control at the WM substrate level, narrowing the "model-agnostic" half) and [[2605.10921\|RoboMemArena]] the action-conditioned-manipulation demand-side anchor; but MIND is scene-navigation (not manipulation at sub-cm), so no suite instantiates the *same* memory layer over C1-occupancy / C2-pointmaps / C3-latent-4D substrates, and no world-frame-vs-robot-frame drift suite exists for H4 |
| No benchmark scores *scene* reconstruction on *interaction-readiness* (the four criteria) rather than fidelity — readiness is a checklist with no leaderboard | D1 | [[2505.17966\|Single-View Mesh for Robotics]] is the closest readiness-CRITERIA protocol (5 desiderata, 12 recon models, YCB-Video + Aria, per-criterion pass/fail + ~50% grasp transfer) but object-level with no readiness-OPTIMIZING pipeline, and [[2604.05621\|FunRec]]'s RealFun4D the closest scene-level articulation-readiness suite (127 seqs / 12 OmniGibson, URDF/USD-exportable); the residual gap is a standardized scene-level four-criteria leaderboard running the controlled PSNR-vs-readiness dual-objective comparison ([[2604.25459\|GS-Playground]]/[[2511.04665\|Real-to-Sim GS]] grade transfer, not readiness) |
| No benchmark scores *per-object* physical-asset generation uniformly across *rigid + deformable + articulated* classes — readiness metrics are class-siloed | D2 | The only cross-class readiness scorecard is PhysX-Bench, shipped by the [[2605.21572\|PhysX-Omni]] method itself (kinematic 0.92, rigid/articulated-leaning); [[2503.17973\|PhysTwin]]/[[2605.09538\|PhysHanDI]] are deformable-specific. The closest *standardized* 3D-gen benchmark is fidelity-only ([[2503.21745\|3DGen-Bench]] human-preference/3DGen-Score) — which scores appearance fidelity, the very axis D2's bet argues against, so the standardized leaderboards measure the wrong axis for embodied readiness |

---

## Cross-References

> [!note] Focus-Direction tie-in
> The coupling term $M_{\text{base,arm}}$ in [[Focus-Direction|Focus-Direction]] is irreducibly geometric. **A1 (point-cloud-native action heads) plugs into [[Focus-Direction|Focus-Direction]] under WB-A1's representation layer, and is the policy-side twin of WAM-A2's wrench imagination** — an explicit-geometry representation enabler under the anchor, not a 5th corner. A1 supplies the metric-3D state on which the explicit coupling head operates; the direction's four corners (WB-A1 anchor / WAM-A2 predict / Sim2Real-B2 ground / EAI-B1 verify) are unchanged.

**Sibling research-direction docs:**
- [[WAM|WAM]] — the WAM-machinery sibling. WAM owns the machinery (latent/architecture substrate, training, grounding); C3 ([[2604.26694|X-WAM]] natively-4D imagination) and C4 ([[2603.17117|MosaicMem]], [[2603.24576|Chameleon (Episodic Memory)]] geometric memory) are the *representations* any policy reuses. Cluster C's explicit-vs-latent split sits *inside* this doc, not across the WAM boundary.
- [[Sim2Real|Sim2Real]] — A1/B1 ([[2604.25459|GS-Playground]] 90% real SR, [[2511.04665|Real-to-Sim GS]] r=0.915) own the *transfer-gap* face of 3DGS reconstruction; this doc's D1 owns the *interaction-readiness* face. Cross-reference, never re-own.
- [[Embodied-AI|Embodied-AI]] — the umbrella; cross-cutting joint-evaluation and cross-embodiment directions live there.
- [[Whole-Body|Whole-Body]] — WB-A1's coupled-dynamics action model consumes A1's geometric representation (see Focus-Direction tie-in).
- [[Focus-Direction|Focus-Direction]] — the four-corner focused direction A1 plugs into under WB-A1's representation layer.

**Deep-dives:**
- [[../Embodied-AI/08_Latent-World-Models|08_Latent-World-Models]] — the latent-vs-explicit substrate debate Cluster C extends to the explicit-geometry side.
- [[../Embodied-AI/11_Physics-Aware-Embodied-AI|11_Physics-Aware-Embodied-AI]] — physical parameterization (D1, D2) and physics-grounded geometry.
- [[../Embodied-AI/06_VLA-Reasoning-and-CoT|06_VLA-Reasoning-and-CoT]] — the spatial-CoT cognition layer (Cluster B).
- [[../Embodied-AI/05_VLA|05_VLA]] — the RGB-token policy baselines Cluster A inverts.
- [[../Embodied-AI/02_Dataset-Benchmark-Environment|02_Dataset-Benchmark-Environment]] — the benchmark suites and simulation environments cited throughout.

**General topics:**
- [[../General/05_Computer-Vision-and-3D|05_Computer-Vision-and-3D]] — 3D-understanding foundations.
- [[../General/07_Robotics-and-Embodied-AI|07_Robotics-and-Embodied-AI]] — the policy / world-model / manipulation papers.
- [[../General/03_Reasoning-and-Planning|03_Reasoning-and-Planning]] — spatial reasoning and CoT (Cluster B).
- [[../General/08_Benchmarks-and-Surveys|08_Benchmarks-and-Surveys]] — the five anchor surveys.
