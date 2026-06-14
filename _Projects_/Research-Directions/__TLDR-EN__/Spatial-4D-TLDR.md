---
title: "TL;DR: 3D/4D Spatial & Geometric Representation"
aliases:
  - "Spatial-4D TL;DR"
  - "Spatial-4D skim"
tags:
  - tldr
  - embodied-AI
  - 3D-understanding
  - spatial-reasoning
---

# TL;DR: 3D/4D Spatial & Geometric Representation

> [!info] What this is
> A skimmable TL;DR of [[Spatial-4D|3D/4D Spatial & Geometric Representation]]. Per direction: **the bet**, the reasoning, the sharpest open questions, the risks. Full detail (related-work tables, all hypotheses, benchmarks) stays in the source. Plain-language version: [[Spatial-4D-ELI5|ELI5]].

> [!abstract] Overview
> Geometry is what a task keeps fixed; appearance is the noise on top. A gripper, an object, and their contacts sit at metric 3D positions that don't move when lighting, texture, or camera does — so a representation built around geometry carries the action-relevant signal directly, while an RGB token leaves it implicit and pays to re-infer it every step. The non-consensus bet: the geometric channel, not the appearance channel, carries the action-relevant signal, and the gap to RGB *widens* exactly where geometry holds and pixels move (cross-embodiment, viewpoint shift, occlusion, long horizons). The field treats explicit 3D as overhead a big enough 2D model makes unnecessary; these 11 directions treat it as the thing the loss should be built around.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A — Geometry-Native Policies | A1–A3 | The action head reads or predicts RGB tokens, leaving metric 3D implicit and paying an embodiment-specific data tax |
| B — 3D-Grounded Cognition | B1–B2 | Reasoning isn't grounded in metric geometry: language CoT over RGB hallucinates spatial relations and dynamics |
| C — Geometry-Native World Models & Memory | C1–C4 | World models imagine in pixels; geometry is recovered after the fact, isn't externally usable, isn't natively 4D, and isn't kept over long horizons |
| D — Reconstruction for Embodied Perception | D1–D2 | Reconstruction optimizes radiance, not interaction-readiness; assets aren't physics- or kinematics-ready |

## A — Geometry-Native Policies
*The action head consumes or predicts explicit 3D — its conditioning state is metric geometry, not RGB tokens. The three directions span the cost/benefit frontier: a full point-cloud head, an occupancy forward model the planner rolls, and a cheap depth-token side-channel.*

### A1 — Point-Cloud-Native Action Heads vs RGB-Token Policies
> [!abstract] The bet
> The geometry-over-RGB advantage Point Cloud Matters proved with simple encoders survives at 2D-pretrained-VLA scale *and* most of it is recoverable from sparse geometry: (i) the recovery-vs-density curve has a knee far below GeoVLA's full branch (≥80% of the full-branch SR gain at DP3-level sparsity), and (ii) it is the point *representation*, not PointAction's factorized decoder, that carries the 43.0% xArm7 zero-shot transfer — swapping points→RGB-features (decoder fixed) collapses most of it, swapping the decoder (points fixed) does not.

**Why** — Today's policies (SpatialVLA, OpenVLA-class) feed the head RGB tokens and hope contact-precise geometry falls out of semantic features, leaving metric 3D implicit. The first principle: an action is set by metric 3D layout (gripper/object/contact positions), which stays fixed under lighting/texture/viewpoint while appearance does not. This challenges the OpenVLA/SpatialVLA assumption that a big 2D backbone already encodes whatever geometry the head needs — GFM-VLA Study linear-probes GR00T-N1.5's VLM output at 0.73 m depth RMSE vs a geometric model's 0.41 m, so the RGB backbone provably does not.

**First-principles** — *Principle:* a manipulation action is a function of where things are in metric 3D, and a point cloud says that directly. *Challenged:* OpenVLA/SpatialVLA's view that a 2D backbone makes an explicit 3D branch wasted overhead — Dexterity-BEV holds 89.9% on shifted LIBERO where 2D collapses to <10%. *Wager:* the geometry advantage is real at VLA scale and cheap geometry (DP3-sparsity) recovers most of it, so the win is the representation, not the architecture.

**Sharpest questions** — 1) Does the graded appearance-shift advantage (point > RGB) hold with a 2D-pretrained-VLA backbone, with the margin growing monotonically with shift and ≈0 at zero shift? 2) Where is the minimal-sufficient-geometry knee — does sparse-point conditioning recover ≥80% of the full-branch gain? 3) In a 2×2 representation-vs-decoder swap on PointAction's embodiment-free pretraining, does the point representation (not the decoder) carry the zero-shot transfer? Plus: does a native point head beat the strongest latent-geometry policy (VLA-JEPA, 3DThinkVLA) on OOD LIBERO-Plus but only tie on ID?

> [!warning] Risks
> - Point clouds need depth sensing/reconstruction that may be noisy or unavailable → lean on the predicted-pointmap path (PointAction) so geometry is generated, not sensed.
> - Advantage may vanish on saturated ID benchmarks (LIBERO ~97%) → evaluate on appearance-shift / cross-embodiment splits; treat ID parity as expected.
> - Full 3D branches add latency/parameters → the minimal-geometry sweep + A3's depth bridge are the lightweight fallback.

### A2 — Occupancy-Forecasting as the Policy's Forward Model
> [!abstract] The bet
> A *dense explicit* voxel-occupancy forward model holds geometric stability an order of magnitude longer than a pixel-WM baseline at RoboCasa scale (rollout-horizon-to-divergence ≥10× the pixel baseline), its Warp-DiT error bound survives down to sub-cm resolution, and its forecast occupancy can condition A1's point head to close a fully-geometric perceive-imagine-act loop that beats present-frame-only conditioning on long-horizon SR — none of which any single occupancy-manipulation paper has run.

**Why** — Model-based control needs a forward model, and the default pixel-space video predictor must be re-parsed into geometry every step, so drift piles up fast (pixel/occupancy WMs in driving were limited to <50 frames). The first principle: a planner needs to know which regions of space will be occupied (collision-freedom, contact, reachability) — a voxel grid answers directly; pixels are a lossy, view-dependent re-encoding. This challenges the CTRL-WORLD/video-WM convention that a manipulation forward model should predict pixels because that's what video foundation models predict — OccSim's 80× horizon gain (3,000+ frames over 4+ km) shows the pixel substrate is itself the source of drift.

**First-principles** — *Principle:* the planning-native state is occupancy, not pixels. *Challenged:* the pixel-forward-model convention — OccSim's 80× horizon and RigidFormer's explicit-state stability show geometry forecasts further than pixels. *Wager:* a dense explicit voxel substrate (beyond ACID's implicit field and 3D-Occ-MPC's single object) holds horizon ≥10× the pixel baseline at RoboCasa scale.

**Sharpest questions** — 1) Does swapping a manipulation WM's pixel loop for a dense-voxel occupancy loop (backbone fixed) raise rollout-horizon-to-divergence ≥10× at RoboCasa scale? 2) Is OccSim's Warp-DiT rigid-transform error bound resolution-portable down to the sub-cm voxels manipulation needs? 3) Does feeding forecast future-occupancy into A1's point head beat present-frame conditioning on long-horizon SR? Plus: does explicit occupancy beat the latent-4D substrate (X-WAM) on horizon while losing on per-frame Chamfer (i.e. complementary, not competing)?

> [!warning] Risks
> - Driving→manipulation scale gap (meter-scale, mostly-static vs sub-cm dynamic) → the resolution sweep + dynamic-agent analog are the explicit go/no-go; report where the Warp-DiT bound breaks.
> - Occupancy ground truth is scarce in manipulation data → derive it from depth + known gripper geometry, or pretrain in sim where occupancy is free.
> - Voxel grids are memory-heavy at sub-cm → sparse/hierarchical octree occupancy bounded to the working volume around the end-effector.

### A3 — Depth-Token Bridges: 3D-Awareness into Pretrained 2D Policies Without Re-Training
> [!abstract] The bet
> The deliverable is the *measurement* nobody has produced, not the existence claim PointVLA settled: (i) on one common backbone the recovery-fraction-vs-added-params curve for a depth-token bridge has a clear knee recovering ≥80% of GeoVLA's full-3D-branch SR gain well below full-branch cost (no found paper plots this), and (ii) the frozen-backbone side-channel perturbs a held-out VQA semantic-alignment probe *measurably less* than full-branch fusion that backprops into the backbone — the alignment-preservation cost everyone assumed but PointVLA never numbered.

**Why** — A1 and A2 buy geometry by changing the architecture, which strands the huge installed base of RGB-pretrained policies nobody wants to re-train. The first principle: a 2D policy's spatial weakness is a *missing channel* (depth), not a corrupted representation, so adding the channel as discrete tokens through a decoupled expert supplies metric cues without rebuilding the backbone. The "real 3D needs a full parallel branch + joint re-training" assumption is *already refuted* (PointVLA froze the backbone, Spatial Forcing/VEGA distill geometry at zero inference overhead) — so the open assumption A3 attacks is that "a depth bridge helps" is sufficient: nobody has drawn the cost-efficiency frontier or measured the alignment cost the side-channel was assumed to avoid.

**First-principles** — *Principle:* a missing channel is added, not relearned — depth as a cheap early channel through a decoupled expert. *Challenged:* the cheap/expensive false binary, already settled false by PointVLA / Depth Helps / Spatial Forcing — but the *measurement* of the frontier and alignment cost remains unrun. *Wager:* a knee recovering ≥80% of full-branch gain exists well below full cost, and the side-channel barely perturbs semantic alignment.

**Sharpest questions** — 1) Sweeping depth-token capacity on one common backbone, where is the recovery-fraction knee (≥80% of GeoVLA's full-branch gain at a small fraction of added params)? 2) Does a frozen-backbone depth expert perturb a held-out VQA alignment probe measurably less than full-branch fusion that backprops into the backbone? 3) Does train-time-only distillation (Spatial Forcing depth, SwiftVLA spatiotemporal) match the inference depth channel on geometry-bound tasks at zero inference cost? Plus: does quantization (not just the decoupled expert) drive the noise-robustness gain, and does a second view's depth tokens close the residual to full-3D?

> [!warning] Risks
> - The bridge may plateau below the full-3D ceiling on the hardest tasks → the recovery-fraction curve sets honest expectations; frame as a cost-efficiency frontier, not SR-SOTA.
> - Depth-token quality depends on the depth estimator → QDepth-VLA's quantization buffers estimator noise; report sensitivity so the claim is bounded to realistic depth.
> - The side-channel may still subtly perturb semantic alignment → the VQA probe quantifies it; gate the "non-disruptive" claim on the number, not assumption.

## B — Spatial Reasoning as a 3D-Grounded Cognition Layer
*Reasoning happens over explicit metric geometry, upstream of the action head. B1 grounds *where* objects are (a scene-graph); B2 keeps that geometry coherent *over time* (4D consistency) — the spatial and temporal halves of one cognition layer.*

### B1 — Explicit 3D Scene-Graph CoT for Metric Spatial Reasoning
> [!abstract] The bet
> The gain is carried by *metric* content, not graph topology, and bottlenecked by *construction*, not reasoning: (i) a scene-graph with metric edge labels (distances, angles) beats a purely topological graph on CVBench, with the gap concentrated in metric-relation question types and ≈0 on object-naming; and (ii) when scene-graph CoT errs on the CausalSpatial 54.17%→84.49% causal slice, most errors trace to a *wrong graph* (hallucinated/missing entity), so graph-construction accuracy predicts answer accuracy.

**Why** — MLLMs don't reason about metric space; they *describe* it in language and hallucinate when ungrounded — on causal tasks (collision/occlusion/trajectory) GPT-5 scores 54.17% vs human 84.49% and is overconfident. The first principle: spatial relations form a graph over geometric entities (objects with metric positions, pairwise relations, contacts), and language is a lossy serialization that drops that structure. This challenges the scaling view that a big-enough multimodal model reasons about space implicitly — VLM Spatial Reasoning RL shows naive CoT can *hurt* and only structured scene-graph CoT helps; the open assumption B1 attacks is that adding *any* graph is what matters (vs which property, and where it fails).

**First-principles** — *Principle:* reasoning correctly *is* operating on a metric graph of geometric entities. *Challenged:* both the scaling view (refuted by VLM Spatial Reasoning RL / CausalSpatial's 30-point gap) and the now-consensus "any structure helps" — the untested question is metric-vs-topological edges and construction-vs-reasoning failure. *Wager:* metric edge content carries the gain and graph construction is the bottleneck.

**Sharpest questions** — 1) Do metric edge labels beat a purely topological graph on CVBench, with the gap concentrated in metric-relation question types? 2) When scene-graph CoT errs on the causal slice, do most errors trace to a wrong graph (so construction accuracy predicts answer accuracy)? 3) Does the residual human gap split — scene-graph CoT closes the *trajectory* (reasoning) slice but little of the *occlusion* (perception/depth) slice? Plus: does RL grounding transfer the scene-graph habit to causal-OOD better than SFT, and does upstream scene-graph grounding partially (not fully) substitute for A1's downstream geometry?

> [!warning] Risks
> - Scene-graph construction can itself hallucinate, poisoning downstream reasoning → ground the graph in B2's 4D-consistency/depth and report construction accuracy separately.
> - Gains may be benchmark-specific (CVBench-tuned prompts) → the RL-OOD protocol tests cross-benchmark transfer; treat GRPO as the generalization mechanism, not prompt-tuning.
> - The human gap may be perception-bound, not reasoning-bound → separate perception from reasoning failure; if perception-bound, route to A3's depth bridge.

### B2 — 4D-Consistent Policies: Spatio-Temporal Geometry as a Reasoning Constraint
> [!abstract] The bet
> It is the consistency *constraint*, not raw 3D or viewpoint-geometry alone, that drives the OOD gain — and it must be shown over *full* space+time 4D, not the viewpoint-only slice GeoAware fenced. Ablating ConsisVLA-4D's consistency attention with *perception held fixed* collapses OOD SR (toward MolmoAct's 72.1% baseline) more than ablating any single perceptual feature, and more than it dents ID SR — the consistency-vs-perception isolation no paper has run.

**Why** — A policy that plans over a horizon must keep an object's geometry and identity coherent across time and viewpoint, else the action committed at step 1 is invalidated by a hallucinated scene at step 5. The field's two answers — projection-biased 2D (cheap, inconsistent) or explicit future-frame generation (expensive) — both fall short. The first principle: imagined geometry must be temporally and cross-view consistent, and consistency is a *constraint*, not the same as rendering every frame. This challenges the either/or — ConsisVLA-4D gets explicit-3D accuracy *and* a 2.31× speedup with *implicit* consistency attention, breaking the tradeoff.

**First-principles** — *Principle:* an action planned over a horizon needs a temporally + cross-view consistent 4D trajectory. *Challenged:* the projection-biased-2D-vs-expensive-frame-gen binary (broken by ConsisVLA-4D); and the now-consensus "implicit consistency helps OOD" — the untested question is *which* of consistency-vs-perception drives it, over full 4D. *Wager:* the consistency constraint (not raw 3D) is the OOD driver.

**Sharpest questions** — 1) Over full space+time 4D, does ablating consistency (perception fixed) collapse OOD more than ablating any perceptual feature, and more than it dents ID? 2) On the SR-vs-latency plane, is implicit 4D Pareto-dominant over explicit (Geometry-aware 4D Robot Video, STARRY) except where externally-readable geometry is required? 3) Is there a horizon crossover window where implicit consistency is optimal (beating 2D above one threshold, losing to explicit generation above a longer one)? Plus: does a scene-flow prior (LaMP) recover most of the consistency gain at lower cost, and do implicit consistency + explicit traces (MolmoAct) compound?

> [!warning] Risks
> - Implicit consistency may not be inspectable, hurting debuggability → pair with MolmoAct's steerable visual reasoning traces so temporal reasoning is auditable.
> - The 2.31× speedup rests on ConsisVLA-4D alone → the full implicit-vs-explicit cost/accuracy frontier is the go/no-go before generalizing.
> - Implicit 4D may silently fail on the longest horizons where drift accumulates invisibly → the horizon-crossover bounds the regime; beyond it, route to C4's explicit persistent memory.

## C — Geometry-Native World Models & Memory
*The world model's representation is geometry, not appearance. Ordered along the decodability axis: occupancy a planner reads (C1) and pointmaps a tracker reads (C2) are explicit-external; a latent-4D state decoded for imagination (C3) is internal; a world-frame memory (C4) makes whichever persist.*

### C1 — Occupancy World Models as the Manipulation Rollout Substrate
> [!abstract] The bet
> A voxel-semantic occupancy WM beats a latent-4D baseline (sibling C3, X-WAM) by ≥1 order of magnitude on *horizon-to-divergence* at tabletop scale — the head-to-head 3D-Occ-MPC and DSR-Net never ran — while *losing* on per-frame Chamfer (latent-4D's 0.0049), making the two complementary not competitive, and its Warp-DiT rigid-transform error bound survives to sub-cm.

**Why** — The manipulation default is a latent/pixel substrate whose geometric error compounds — the rollout drifts within tens of frames over long horizons. The first principle: a WM's long-horizon stability is set by how fast geometric error grows per step, and an occupancy grid with rigid-transform constraints (OccSim's Warp-DiT) keeps that error in check while a latent substrate has no such limit. This challenges the convention that the rollout substrate should be the same RGB-D latent the policy sees (CTRL-WORLD / X-WAM); the old "occupancy is driving-only" framing is empirically false (DSR-Net did it in 2020, Occupancy World Model ports to indoor), so the real open assumption is that the substrate choice doesn't bound horizon — OccSim's 80× gain says it does.

**First-principles** — *Principle:* long-horizon stability is governed by per-step geometric error growth, which rigid-transform-constrained occupancy bounds and a latent doesn't. *Challenged:* the RGB-D-latent-rollout convention — and the assumption that both substrates "working" means the choice is horizon-neutral. *Wager:* occupancy beats latent ≥10× on horizon while losing per-frame, so they are complementary.

**Sharpest questions** — 1) On matched manipulation tasks, does frames-to-geometric-divergence for an occupancy WM exceed X-WAM-class latent by ≥one order of magnitude? 2) Does an off-the-shelf planner collision-check the occupancy grid directly, beating decoding C3's latent on latency and accuracy? 3) Does occupancy-grid drift (mIoU-over-horizon), not per-frame Chamfer, predict downstream planning failure? Plus: does a hybrid (occupancy for long-horizon planning, latent for per-step fidelity) beat either on (horizon × fidelity), and does the Warp-DiT bound survive sub-cm?

> [!warning] Risks
> - Driving→manipulation scale gap (meter-scale vs sub-cm) → the sub-cm Warp-DiT test is the go/no-go; report where the bound breaks rather than assuming transfer.
> - Overlap with sibling C3 if the explicit/latent delta blurs → pin C1 to externally-renderable long-horizon occupancy + complementarity; C1 is the substrate X-WAM isn't, not a better X-WAM.
> - Occupancy supervision scarcity in manipulation data → derive in sim (free) and from depth + gripper geometry; bound real claims to recoverable GT.

### C2 — 4D-Geometric-Consistent Video Prediction for 6-DoF Pose Extraction
> [!abstract] The bet
> The discriminator that survives the whole field is *cross-view pointmap consistency read by an off-the-shelf geometric tracker* — not single-view RGB-D and not a learned estimator or RGB-only Gen6D. Jointly predicting RGB + cross-view-consistent pointmaps yields tracker-readable 6-DoF trajectories at ≥0.64 avg task SR vs ~0.12 for RGB-plus-estimator baselines (≈5×), and the gain tracks *cross-view consistency* (mIoU): ablating the cross-view pointmap loss collapses trajectory accuracy more than degrading RGB quality (FVD) does.

**Why** — Video-prediction-for-action methods (Dreamitate-class) predict future RGB frames then bolt on a pose estimator, but RGB-only frames leave 6-DoF pose ambiguous, so the policies are brittle (Dreamitate and Diffusion Policy both at 0.12 avg task SR). The first principle: a 6-DoF pose is geometric — if pointmaps agree across views, any tracker reads the pose straight off as the rigid transform between matching 3D points; RGB-only frames hide it. This challenges the Dreamitate-class convention that a pixel video model + downstream estimator suffices (PEWM, RGB-only Gen6D), and the softer convention that single-view geometry is enough (GVF-TAPE's learned estimator) — the ≈5× SR gap shows the post-hoc/single-view estimator is the bottleneck.

**First-principles** — *Principle:* a 6-DoF pose is the rigid transform between matching cross-view 3D points; consistent pointmaps make it tracker-readable. *Challenged:* the pixel-video-plus-estimator convention (PEWM) and the single-view-RGB-D convention (GVF-TAPE). *Wager:* cross-view pointmap consistency read by an off-the-shelf tracker is the discriminator, gain tracking consistency not RGB fidelity.

**Sharpest questions** — 1) Does removing the cross-view pointmap loss (RGB fixed) collapse trajectory accuracy and SR more than degrading RGB FVD — and does a single-view-depth + learned-estimator variant underperform the cross-view tracker readout? 2) How small is the cost of predicted pointmaps vs sensed depth on pose readout (justifying prediction where sensing is unavailable)? 3) Where is the novel-viewpoint extrapolation envelope before pose accuracy degrades? Plus: does externalized geometry beat internalized (ConsisVLA-4D) on debuggability-critical tasks, and is occlusion where predicted-geometry pose readout wins most (mirroring RecGen's +38.2 pp)?

> [!warning] Risks
> - Single-anchor direction — the headline rests on Geometry-aware 4D Robot Video's three-task evaluation → the consistency-ablation + predicted-vs-sensed comparison are the internal validity checks; broaden the task set before generalizing ≈5×.
> - Predicted pointmaps may be noisier than sensed depth → quantify the predict-vs-sense gap; if large, gate C2 to settings where sensing is unavailable.
> - Three-task SR is a narrow base → frame the contribution as *the mechanism* (cross-view pointmaps → tracker-readable pose) validated on three tasks, with broader evaluation as the explicit next step.

### C3 — Natively-4D Geometry as a World-Representation Substrate
> [!abstract] The bet
> The two pillars no paper — including PointWorld — has run decide whether native online 4D earns its keep over a train-time auxiliary: (i) holding the backbone fixed, X-WAM's interleaved depth branch beats a pixel substrate + post-hoc depth estimator on geometry-bound RoboCasa tasks (Chamfer 0.0049 native vs the two-stage 0.0680), isolating native-over-recovered; and (ii) generalizing Asynchronous Noise Sampling, the action schedule step-distills to 1–4 steps (extending X-WAM's 5-step 15 Hz, 4665→1033 ms) without degrading the read-out geometry — the latency-fidelity frontier PointWorld's point-flow MPC never charted.

**Why** — Almost every deployed model still imagines in 2D pixels and recovers geometry only implicitly, which X-WAM says "leads to physically implausible predictions and hinders geometrically faithful reconstruction." The first principle: for contact-rich and spatially-bound tasks the action is a function of geometry (relative pose, depth, normals, free space), so a pixel substrate forces re-inferring it every step. This challenges the assumption that explicit 4D is too expensive to deploy — X-WAM shows the two-stage path is both worse geometrically (0.0680 vs 0.0049) *and* slower than a unified 4D model with async denoising. But "explicit geometry online beats latent + transfers across embodiments" is now demonstrated by PointWorld, so C3's distinctiveness narrows to the async-no-penalty latency comparison and the native-vs-lift Chamfer ablation on a native-4D-RGB-D-video (not point-flow) substrate.

**First-principles** — *Principle:* the action's geometry is in the task, not the rendering choice, so a native-4D substrate carries it directly. *Challenged:* the "4D is too expensive to deploy, recover it two-stage" assumption (broken by X-WAM); and PointWorld already owns the broad online-explicit + transfer claim. *Wager:* native-4D beats lift-after-pixel at no deployment penalty, with the action schedule distillable to 1–4 steps.

**Sharpest questions** — 1) Holding the backbone fixed, does X-WAM's interleaved depth branch beat a pixel substrate + post-hoc depth estimator on geometry-bound RoboCasa (native-over-recovered)? 2) Does the async action schedule shrink to 1–4 steps without degrading the read-out geometry (Chamfer vs steps)? 3) Does a native-4D-RGB-D-video substrate transfer WM→policy-head with its appearance channel intact, at least matching PointWorld's point-flow transfer? Plus: does an explicit 3D channel lower contact-mode prediction error vs a latent, and do end-effector-derived camera poses improve OOD geometry?

> [!warning] Risks
> - 4D supervision needs depth/3D ground truth absent in most robot datasets → use X-WAM's end-effector-derived camera poses + off-the-shelf depth estimators; bound the claim to recoverable geometry.
> - 4D is only worth it on geometry-bound tasks (latent already wins on appearance-bound) → score on contact/spatial tasks (RoboCasa insertion, stacking), not headline LIBERO SR.
> - Real-time 4D is now shown twice (X-WAM, PointWorld), so the open question is native-vs-recovered + async step-distillation paying off → the native-vs-recovered Chamfer ablation + latency-fidelity frontier are the go/no-go; concede PointWorld owns the broad transfer claim.

### C4 — Persistent Geometric Memory as a Substrate-Agnostic Persistence Layer
> [!abstract] The bet
> (i) A single world-frame memory layer, dropped over each of C1/C2/C3, raises minute-scale coherence above the bare substrate by a margin tracking 3D Persistent Embodied WM's SRC 81.7% vs 63.4% no-memory gap — i.e. the layer is substrate-agnostic, not substrate-bespoke; and (ii) geometric (MosaicMem) + episodic (Chameleon) memory *compound* on RoboMemArena (combined > max(either) on the 68.9% history-required subtasks), because they address different failure modes — neither demonstrated by any single paper.

**Why** — That explicit geometric memory beats attention-only on action-conditioned long-horizon coherence is *already taken* (3D Persistent Embodied WM: SRC 81.7% vs 63.4%, FVD 91.9 vs 194). So the open gap is two things nobody has done: a memory layer that serves *any* substrate, and a benchmark of geometric + episodic memory *together*. The first principle: a world-frame geometric memory is substrate-orthogonal — object permanence is a property of the metric frame, not the representation that fills it — so the *same* mechanism should pin C1's occupancy, C2's pointmaps, or C3's latent-4D; and geometric vs episodic memory fix *where* vs *which event*, so they should compound. This challenges the convention that memory is built once per substrate and that the two memory types are alternatives, not complements.

**First-principles** — *Principle:* object permanence lives in the metric world-frame, so one persistence mechanism should serve any substrate; geometric + episodic memory are complementary primitives. *Challenged:* the "memory built once per substrate, geometric vs episodic are alternatives" convention (each prior paper builds bespoke memory for its own model). *Wager:* one shared layer transfers across substrates, and the two memory types compound.

**Sharpest questions** — 1) Does dropping one world-frame memory mechanism over C1/C2/C3 raise each substrate's minute-scale coherence by a margin tracking the 81.7% vs 63.4% gap (substrate-agnostic, not bespoke)? 2) Do episodic events + geometric memory compound on RoboMemArena (beating either alone on history-required subtasks)? 3) Does the compound advantage concentrate on perceptual-aliasing/out-of-view subtasks and ≈0 on pure-revisit? Plus: does world-frame memory hold coherence better than robot-frame, and does the shared layer cost less than three bespoke memories at equal coherence?

> [!warning] Risks
> - Explicit geometric memory needs reliable 3D lifting (off-the-shelf estimators fail on texture-poor scenes) → hybridize with implicit attention (MosaicMem's design) so it degrades gracefully when lifting is noisy.
> - Episodic retrieval can interfere on visually-aliased-but-irrelevant events → use disambiguated indexable encoding + goal-directed retrieval, not similarity-only; validate on RoboMemArena's occlusion/counting splits.
> - Memory adds footprint against the real-time budget → the patch-level-vs-O(1)-TTT Pareto is the go/no-go; memory earns its place only if coherence gain beats cost.

## D — Reconstruction for Embodied Perception
*Reconstruction built for interaction-readiness — geometry that carries physics and kinematic structure, not just radiance. Split by unit: a whole scene an agent acts in (D1) and the reusable single object that populates it (D2).*

### D1 — Interaction-Ready Scene Reconstruction: Whole Environments You Can Act In
> [!abstract] The bet
> The deliverables are the *controlled measurement* and the *articulation* readiness HoloScene's joint objective leaves out: (i) building the same scene under (a) a PSNR objective vs (b) the survey's four readiness criteria, the fidelity-optimal asset fails ≥1 criterion measurably more often, reported per-criterion pass/fail (the controlled isolation HoloScene only surfaces as an ablation co-product); and (ii) single-video reconstruction recovers rigid decomposition reliably but fails articulated structure (joints/DoF) for URDF/MJCF export without multi-view or interaction data — the rigid-body ceiling HoloScene names but does not cross.

**Why** — The reconstruction community optimizes radiance (PSNR/SSIM/FID), and the survey names the mismatch as *the* embodied bottleneck: conventional 3D generation focuses on visual appearance, but embodied-oriented generation demands interaction readiness, physical grounding, and simulator compatibility, blocked by scarce physical annotations. The first principle: an embodied agent interacts with geometry, physics, and kinematics — not radiance — so a reconstruction's embodied value is interaction-readiness, a property orthogonal to visual fidelity. The NeRF/3DGS "higher fidelity = better asset" default is *already documented false* (HoloScene's Table-3 trade-off, Single-View Mesh for Robotics missing the 2 mm bar), so the open assumption D1 attacks is that a single joint objective surfacing it as a side-effect suffices — no one has run the controlled per-criterion measurement, nor recovered articulation from single video.

**First-principles** — *Principle:* embodied value is interaction-readiness (collide/grasp/articulate), orthogonal to and not implied by visual fidelity. *Challenged:* the higher-fidelity-is-better default (refuted by HoloScene + Single-View Mesh for Robotics) — but the *controlled* per-criterion measurement and single-video articulation remain unrun. *Wager:* fidelity-optimal scenes fail readiness measurably more, and single video misses articulation.

**Sharpest questions** — 1) Building the same scene under PSNR vs the four readiness criteria, does the fidelity-optimal asset fail ≥1 criterion substantially more often (per-criterion pass/fail)? 2) Does single-video reconstruction recover rigid decomposition reliably but fail articulated structure for URDF/MJCF export without multi-view/interaction data? 3) Is there a physical-parameter readiness *threshold* (mass/friction/restitution) below sim-accurate fidelity where a trained policy still acts correctly? Plus: does a D1 readiness-asset feed A1's point head and C1's occupancy WM end-to-end as well as a hand-built asset, and does feed-forward simulator-format output beat post-hoc meshing on readiness?

> [!warning] Risks
> - Interaction-readiness lacks a standard benchmark (a checklist, not a leaderboard) → adopt the survey's four criteria as the explicit scorecard; report per-criterion pass/fail, not a single fidelity number.
> - Single-video may not recover articulation/physics for complex scenes → bound what single-video can recover; fall back to multi-view or interaction data where articulation needs it.
> - Boundary blur with Sim2Real-A1/B1 → pin D1 to readiness as the optimization target; route the transfer-gap evaluation to GS-Playground / Real-to-Sim GS.

### D2 — Object-Level Physical-Asset Generation: One Object That Carries Its Own Physics
> [!abstract] The bet
> The controlled falsifier nobody has run unified — not the generator PhysX-Omni already built — decides it: (i) generating the *same* matched object set (a) geometry-first-then-annotate vs (b) jointly via a PhysX-Omni-style unified head, the staged pipeline fails the kinematic/material readiness criterion substantially more often, decomposed per-class with the advantage concentrated on deformable + articulated (≈0 on rigid props), as SOPHY's skip-rigid choice already hints; and (ii) a physical-consistency metric (energy/momentum, NeuROK-style, Chamfer-L1 ≤0.028) predicts out-of-category readiness better than fidelity (PSNR/Chamfer) — the generalization signal no scorecard isolates.

**Why** — D1 builds a whole scene, but its reusable parts are objects, and a fidelity-first object is a hollow prop — a watertight surface with no mass, friction, or joints. The survey names the object-level bottleneck as the trade-off between geometric quality and physical validity plus scarce physical annotations, with deformable assets called out as unsolved. The first principle: an object's embodied value is a *joint* (geometry, material, kinematics) — physics is not a separable post-hoc label but a property the geometry must be generated consistent with. The geometry-first convention is *already refuted* (PhysX-Omni, SOPHY, UniArt each generate physics-with-geometry in one pass), so the open assumption D2 attacks is that demonstrating a unified generator *exists* proves joint > staged — no paper has run the matched-object controlled comparison or tested whether energy/momentum-consistency predicts out-of-category readiness.

**First-principles** — *Principle:* an object's behavior under contact is co-determined by geometry + material + kinematics, so they must be generated jointly. *Challenged:* the geometry-first-then-annotate convention (refuted by PhysX-Omni / SOPHY / UniArt) — but the matched-object joint-vs-staged falsifier and the consistency-predicts-OOD test remain unrun. *Wager:* joint generation passes readiness where staged fails, largest on deformable/articulated; consistency (not fidelity) predicts OOD readiness.

**Sharpest questions** — 1) On a matched object set, does staged geometry-first-then-annotate fail the kinematic/material readiness criterion substantially more often than joint generation, across rigid + deformable + articulated on one scorecard? 2) Is the joint-generation advantage near-zero on rigid props and concentrated on deformable + articulated (SOPHY's skip-rigid choice, made explicit)? 3) Does an energy/momentum-consistency constraint at generation time predict out-of-category readiness better than fidelity (PSNR/Chamfer)? Plus: when a generated object is dropped into a D1 scene, is the binding transfer constraint per-object material *or* kinematic structure, and is deformable the widest gap / largest single-pass win?

> [!warning] Risks
> - Per-object readiness has no shared cross-category leaderboard (PhysX-Bench is rigid/articulated-leaning; PhysTwin/PhysHanDI deformable-specific) → adopt the survey's four criteria as the common scorecard; report per-class pass/fail, not one aggregate.
> - Physical parameters from single video / sparse RGB-D may be under-determined (mass/friction unobservable from kinematics alone) → energy/momentum consistency constraints regularize them; bound the claim to where the constraint identifies them.
> - Boundary blur with D1 if "object" and "scene" leak → pin D2 to the single-object unit and D1 to whole-scene; a D2 object populating a D1 scene is the intended composition, not an overlap.
