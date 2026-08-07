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
> A skimmable TL;DR of [[Spatial-4D|3D/4D Spatial & Geometric Representation]]. For each direction: **the bet**, the reasoning, the sharpest open questions, and the risks. Full detail stays in the source. Plain-language version: [[__ELI5-EN__/Spatial-4D-ELI5|ELI5]].

> [!abstract] Overview
> Geometry is what a task keeps fixed; appearance is the noise on top. A gripper, an object, and their contacts sit at metric 3D positions that don't move when lighting, texture, or camera changes. The non-consensus bet: the geometric channel carries the action signal, not appearance, and the gap to RGB *widens* exactly where geometry holds but pixels move (cross-embodiment, viewpoint shift, occlusion, long horizons). The field treats explicit 3D as overhead. These 11 directions build the loss around 3D.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A: Geometry-Native Policies | A1–A3 | The action head reads/predicts RGB tokens, leaving metric 3D implicit and paying an embodiment-specific data tax |
| B: 3D-Grounded Cognition | B1–B2 | Reasoning isn't grounded in metric geometry: language CoT over RGB hallucinates spatial relations and dynamics |
| C: Geometry-Native World Models & Memory | C1–C4 | World models imagine in pixels; geometry is recovered after the fact, not externally usable, not natively 4D, not kept over long horizons |
| D: Reconstruction for Embodied Perception | D1–D2 | Reconstruction optimizes radiance, not interaction-readiness; assets aren't physics- or kinematics-ready |

## A: Geometry-Native Policies
*Conditioning state is metric geometry, not RGB tokens. The three span the cost/benefit frontier: a full point-cloud head, an occupancy forward model, and a cheap depth-token side-channel.*

### A1: Point-Cloud-Native Action Heads vs RGB-Token Policies
> [!abstract] The bet
> A1: Point Cloud Matters proved a geometry-over-RGB advantage with simple encoders. The bet: it survives at 2D-pretrained-VLA scale, *and* most is recoverable from sparse geometry. The **primary gate for the whole A cluster** is the explicit-point-head vs distilled-latent head-to-head, on a cross-embodiment, geometry-bound split (not saturated ID): only if explicit metric structure beats the latent there does A1's native head stay load-bearing and A2/A3 become its cost-reduction frontier; if the latent matches, the cluster's gravity moves to A3. Two sub-bets: (i) the recovery-vs-density curve knees far below GeoVLA's full branch, ≥80% of the full-branch SR gain at DP3-level sparsity. (ii) The point *representation*, not PointAction's factorized decoder, carries the 43.0% xArm7 zero-shot transfer: swapping points for RGB-features (decoder fixed) collapses most of it; swapping the decoder (points fixed) doesn't.

**Why**: Today's policies (SpatialVLA, OpenVLA-class) feed the head RGB tokens, leaving metric 3D implicit. GFM-VLA Study linear-probes GR00T-N1.5's VLM output at 0.73 m depth RMSE vs a geometric model's 0.41 m.

**First-principles**
- *Principle:* an action is a function of metric 3D layout; a point cloud says it directly.
- *Challenged:* OpenVLA/SpatialVLA's "3D branch is wasted overhead." Dexterity-BEV holds 89.9% on shifted LIBERO where 2D collapses to <10%.
- *Wager:* the advantage holds at VLA scale, DP3-sparse geometry recovers most of it, and the win is the representation, not the architecture.

**Sharpest questions**
1. Does the point > RGB advantage hold at 2D-pretrained-VLA scale?
2. Does the margin grow with the shift and sit ≈0 at zero shift?
3. Where is the cheapest-geometry knee, does sparse-point conditioning recover ≥80% of the full-branch gain?
4. In a 2×2 swap on PointAction, does the representation carry the zero-shot transfer, not the decoder?
5. **(The primary gate)** Does a native point head beat the best *sensor-free* latent (VLA-JEPA, 3DThinkVLA, Evo) on a cross-embodiment, geometry-bound OOD split but only tie in-distribution? The margin's sign decides whether A1 stays the headline or the gravity shifts to A3.
6. Once you *charge for the depth source* (the sensor, or the second network that invents the points and errs worst on the contact-rich tail), does the explicit head keep its margin over a sensor-free latent, or does the sensing tax invert the externalized-geometry recommendation?

> [!warning] Risks
> - Depth may be noisy or unavailable. Fix: predicted-pointmap path (PointAction).
> - The unpriced geometry-source / sensing tax may decide the bet, a sensed head needs a depth sensor and a predicted-pointmap head needs a second network whose error is worst on the contact-rich tail where geometry matters most. Fix: gate the explicit-head recommendation on the *cost-charged* explicit-vs-latent margin under realistic estimated-depth noise, not the clean-depth number.
> - Advantage may vanish on saturated ID benchmarks (LIBERO ~97%). Fix: evaluate on appearance-shift and cross-embodiment splits; expect ID parity.
> - Full 3D branches add latency. Fix: the minimal-geometry sweep and A3's depth bridge.

### A2: Occupancy-Forecasting as the Policy's Forward Model
> [!abstract] The bet
> A2: A *dense explicit* voxel-occupancy forward model stays accurate ≥10× longer than a pixel-WM baseline before drifting (horizon-to-divergence) at RoboCasa scale. Its Warp-DiT error bound (a rigid-transform accuracy guarantee) survives to sub-cm. Its forecast occupancy can condition A1's point head, a fully-geometric perceive-imagine-act loop beating present-frame conditioning on long-horizon SR. No occupancy-manipulation paper has run any of this.

**Why**: The default pixel forward model is re-parsed into geometry every step, so drift piles up fast (driving pixel/occupancy WMs capped at <50 frames). A planner needs which regions will be occupied, answered directly by a voxel grid. OccSim's 80× horizon gain (3,000+ frames over 4+ km) shows the pixel substrate is the drift source.

**First-principles**
- *Principle:* the planning-native state is occupancy, not pixels.
- *Challenged:* the pixel-forward-model convention; OccSim's 80× and RigidFormer's explicit-state stability show geometry forecasts further.
- *Wager:* a dense explicit voxel substrate (beyond ACID's implicit field, 3D-Occ-MPC's single object) holds horizon ≥10× the pixel baseline at RoboCasa scale.

**Sharpest questions**
1. Swap a world model's pixel loop for dense-voxel occupancy (backbone fixed), does horizon-to-divergence rise ≥10× at RoboCasa scale?
2. Does OccSim's Warp-DiT bound hold at the sub-cm voxels manipulation needs?
3. Does forecasting future-occupancy into A1's point head beat present-frame conditioning on long-horizon success?
4. Does explicit occupancy beat latent-4D (X-WAM) on horizon while losing per-frame Chamfer? (then complementary)
5. Is a dense-voxel loop *deployable-latency-competitive* with the sparser explicit substrates? "Latency favours a sparser substrate" is a *hypothesis, not a settled fact*: the sparse incumbents already run deployable (PointWorld ~0.12 s per 10-step ≈ 0.012 s/step, *not* 0.1 s/step), so dense voxels must be shown to fall within a usable multiple on the same hardware, plot horizon-to-divergence against latency as a *frontier*.

> [!warning] Risks
> - Driving (meter-scale/static) vs manipulation (sub-cm/dynamic). Fix: the resolution sweep and dynamic-agent analog; report where Warp-DiT breaks.
> - The "deployable axis" *may* favour a sparser explicit substrate, sparse-point incumbents (PointWorld ~0.12 s/10-step, ParticleFormer) already run in real-time MPC, so dense voxels can win horizon yet lose latency. Fix: make deployability a *measured frontier* (horizon-to-divergence vs matched-hardware latency), not an asserted advantage; report the latency multiple before claiming the dense-voxel substrate is deployable.
> - Occupancy ground truth is scarce. Fix: derive from depth plus gripper geometry, or pretrain in sim.
> - Voxel grids are memory-heavy at sub-cm. Fix: sparse hierarchical octree bounded to the end-effector.

### A3: Depth-Token Bridges: 3D-Awareness into Pretrained 2D Policies Without Re-Training
> [!abstract] The bet
> A3: The deliverable is the *measurement* nobody has produced (PointVLA settled existence). (i) On one backbone, plot recovered gain vs added parameters for a depth-token bridge: the curve knees, recovering ≥80% of GeoVLA's full-3D-branch SR gain below full-branch cost. No found paper plots this. (ii) The frozen-backbone side-channel disturbs a held-out VQA semantic-alignment probe *less* than full-branch fusion that backprops into the backbone, the alignment cost everyone assumed but PointVLA never numbered.

**Why**: A1 and A2 strand the installed base of RGB-pretrained policies. A 2D policy's spatial weakness is a *missing channel* (depth), not a corrupted representation, add it as tokens via a decoupled expert. The "real 3D needs a full parallel branch plus re-training" assumption is *already refuted*: PointVLA froze the backbone; Spatial Forcing/VEGA distill geometry at zero inference overhead.

**First-principles**
- *Principle:* a missing channel is added, not relearned, depth enters as a cheap early channel.
- *Challenged:* the cheap-vs-expensive false binary (settled by PointVLA / Depth Helps / Spatial Forcing); the frontier and alignment cost remain unrun.
- *Wager:* a knee recovering ≥80% of full-branch gain exists below full cost, and the side-channel barely disturbs alignment.

**Sharpest questions**
1. Sweep depth-token capacity on one backbone, where is the knee recovering ≥80% of GeoVLA's full-branch gain at a fraction of params?
2. Does a frozen-backbone depth expert disturb a VQA alignment probe less than full-branch backprop fusion?
3. Does train-time-only distillation (Spatial Forcing, SwiftVLA) match the inference depth channel at zero inference cost?
4. Does the quantization (not just the decoupled expert) drive the noise-robustness gain?
5. Do a second view's depth tokens close the gap to full-3D?

> [!warning] Risks
> - May plateau below the full-3D ceiling on hardest tasks. Fix: the recovery-fraction curve sets expectations; frame as a cost-efficiency frontier.
> - Depth-token quality depends on the estimator. Fix: QDepth-VLA's quantization buffers noise; report sensitivity.
> - Side-channel may still disturb alignment. Fix: the VQA probe gates the "non-disruptive" claim.

## B: Spatial Reasoning as a 3D-Grounded Cognition Layer
*Reasoning over explicit metric geometry, upstream of the action head. B1 grounds *where* objects are (a scene-graph); B2 keeps it coherent *over time* (4D consistency), the spatial and temporal halves of one layer.*

### B1: Explicit 3D Scene-Graph CoT for Metric Spatial Reasoning
> [!abstract] The bet
> B1: The gain comes from *metric* content, not graph topology, and is bottlenecked by *construction*, not reasoning. (i) A scene-graph with metric edge labels (distances, angles) beats a topological graph on CVBench; the gap concentrates in metric-relation types and sits ≈0 on object-naming. (ii) When scene-graph CoT errs on the CausalSpatial causal slice (GPT-5 54.17% vs human 84.49%), most errors trace to a *wrong graph* (hallucinated or missing entity), construction accuracy predicts answer accuracy.

**Why**: MLLMs *describe* metric space and hallucinate when ungrounded; on causal tasks GPT-5 scores 54.17% vs human 84.49%, overconfident. Spatial relations form a graph over geometric entities; language is a lossy serialization. VLM Spatial Reasoning RL shows naive CoT can *hurt*, only structured scene-graph CoT helps, but "any graph helps" says nothing about which property carries the gain.

**First-principles**
- *Principle:* reasoning correctly *is* operating on a metric graph of geometric entities.
- *Challenged:* the scaling view (refuted by VLM Spatial Reasoning RL, CausalSpatial's 30-point gap) and the consensus "any structure helps"; metric-vs-topological and construction-vs-reasoning untested.
- *Wager:* metric edge content carries the gain, and construction is the bottleneck.

**Sharpest questions**
1. Do metric edge labels (distances, angles) beat a topological graph on CVBench, gap concentrated in metric-relation types?
2. When scene-graph CoT errs on the causal slice, do most errors trace to a wrong graph?
3. Does the human gap split, closing *trajectory* (reasoning) but little of *occlusion* (perception)?
4. Does RL grounding transfer the scene-graph habit to OOD causal cases better than SFT?
5. Does upstream scene-graph grounding partly substitute for A1's downstream geometry?

> [!warning] Risks
> - Construction can hallucinate and poison reasoning. Fix: ground in B2's 4D-consistency and depth; report construction accuracy separately.
> - Gains may be benchmark-specific (CVBench-tuned). Fix: the RL-on-OOD protocol tests cross-benchmark transfer.
> - Human gap may be perception-bound. Fix: separate the two; if perception-bound, route to A3's depth bridge.

### B2: 4D-Consistent Policies: Spatio-Temporal Geometry as a Reasoning Constraint
> [!abstract] The bet
> B2: The consistency *constraint* drives the OOD gain, not raw 3D or viewpoint-geometry alone, and must hold over *full* space+time 4D, not the viewpoint-only slice GeoAware fenced. Ablate ConsisVLA-4D's consistency attention with *perception fixed*: OOD SR collapses (toward MolmoAct's 72.1% baseline) more than ablating any single perceptual feature, and more than it dents ID SR. No paper has run this isolation.

**Why**: A policy planning over a horizon must keep object geometry and identity coherent across time and view, else the step-1 action is invalidated by a hallucinated step-5 scene. The two existing answers fall short: projection-biased 2D (cheap, inconsistent) and explicit future-frame generation (expensive). ConsisVLA-4D gets explicit-3D accuracy *and* a 2.31× speedup with *implicit* consistency attention.

**First-principles**
- *Principle:* an action over a horizon needs a 4D trajectory consistent across time and views.
- *Challenged:* the 2D-vs-frame-generation binary (broken by ConsisVLA-4D) and the consensus "implicit consistency helps OOD"; *which* of consistency or perception drives it, over full 4D, untested.
- *Wager:* the consistency constraint (not raw 3D) is the OOD driver.

**Sharpest questions**
1. Over full 4D, does turning off consistency (perception fixed) collapse OOD success more than ablating any perceptual feature, and more than it dents ID?
2. On the success-vs-latency plane, does implicit 4D beat explicit (Geometry-aware 4D Robot Video, STARRY) on both axes, except where readable geometry is required?
3. Is there a horizon window where implicit consistency is best (beats 2D above one length, loses to explicit above a longer one)?
4. Does a scene-flow prior (LaMP) recover most of the consistency gain cheaper?
5. Do implicit consistency and explicit traces (MolmoAct) add up?

> [!warning] Risks
> - Implicit consistency may not be inspectable. Fix: pair with MolmoAct's steerable reasoning traces.
> - The 2.31× speedup rests on ConsisVLA-4D alone. Fix: chart the full implicit-vs-explicit cost/accuracy frontier first.
> - May silently fail on longest horizons. Fix: the horizon-crossover bounds the safe regime; beyond it, route to C4's persistent memory.

## C: Geometry-Native World Models & Memory
*The representation is geometry, not appearance, ordered by who reads it: occupancy a planner reads (C1) and pointmaps a tracker reads (C2) are external; latent-4D (C3) is internal; world-frame memory (C4) makes whichever persist.*

### C1: Occupancy World Models as the Manipulation Rollout Substrate
> [!abstract] The bet
> C1: A voxel-semantic occupancy WM beats a latent-4D baseline (sibling C3, X-WAM) by ≥10× on *horizon-to-divergence* at tabletop scale, a head-to-head (3D-Occ-MPC, DSR-Net) never run. But it *loses* on per-frame Chamfer (latent-4D's 0.0049), so the two are complementary. And its Warp-DiT rigid-transform error bound survives to sub-cm.

**Why**: The default latent/pixel substrate compounds geometric error; the rollout drifts within tens of frames. An occupancy grid with rigid-transform constraints (OccSim's Warp-DiT) bounds error growth, a latent doesn't. The "occupancy is driving-only" framing is false (DSR-Net did it in 2020; Occupancy World Model ports indoor), so the real assumption is that substrate doesn't bound horizon, OccSim's 80× gain says it does.

**First-principles**
- *Principle:* long-horizon stability tracks per-step geometric-error growth; rigid-transform-constrained occupancy bounds it, a latent doesn't.
- *Challenged:* the RGB-D-latent-rollout convention and the assumption that substrate choice doesn't affect horizon.
- *Wager:* occupancy beats latent ≥10× on horizon while losing per-frame, so they are complementary.

**Sharpest questions**
1. On matched tasks, does an occupancy WM stay geometrically stable ≥10× longer than an X-WAM-class latent?
2. Can an off-the-shelf planner collision-check the grid directly, beating C3's decoded latent on latency and accuracy?
3. Does occupancy-grid drift (mIoU over horizon), not per-frame Chamfer, predict planning failure?
4. Does a hybrid (occupancy for long-horizon, latent for per-step detail) beat either alone on horizon × fidelity?
5. Does the Warp-DiT bound survive to sub-cm?

> [!warning] Risks
> - Driving (meter-scale) vs manipulation (sub-cm). Fix: the sub-cm Warp-DiT test is the go/no-go; report where the bound breaks.
> - May overlap sibling C3. Fix: pin C1 to externally-renderable long-horizon occupancy and complementarity, not a better X-WAM.
> - Occupancy supervision is scarce. Fix: derive in sim and from depth plus gripper geometry; bound to recoverable ground truth.

### C2: 4D-Geometric-Consistent Video Prediction for 6-DoF Pose Extraction
> [!abstract] The bet
> C2: The surviving discriminator is *cross-view pointmap consistency read by an off-the-shelf tracker*, not single-view RGB-D, not a learned estimator or RGB-only Gen6D. Jointly predicting RGB plus cross-view-consistent pointmaps yields tracker-readable 6-DoF trajectories at ≥0.64 avg task SR vs ~0.12 for RGB-plus-estimator baselines (≈5×). The gain tracks *cross-view consistency* (mIoU): ablating the pointmap loss collapses trajectory accuracy more than degrading RGB quality (FVD).

**Why**: Video-prediction methods (Dreamitate-class) predict future RGB then bolt on a pose estimator, but RGB-only frames leave 6-DoF pose ambiguous, so policies are brittle (Dreamitate, Diffusion Policy both at 0.12 avg task success). A 6-DoF pose is geometric: if pointmaps agree across views, any tracker reads the rigid transform between matching 3D points. The ≈5× gap shows the after-the-fact single-view estimator is the bottleneck.

**First-principles**
- *Principle:* a 6-DoF pose is the rigid transform between matching cross-view 3D points; consistent pointmaps make it tracker-readable.
- *Challenged:* the pixel-video-plus-estimator convention (PEWM) and the single-view-RGB-D convention (GVF-TAPE).
- *Wager:* cross-view pointmap consistency read by a tracker is the discriminator, and the gain tracks consistency, not RGB fidelity.

**Sharpest questions**
1. Does removing the cross-view pointmap loss (RGB fixed) collapse trajectory accuracy and success more than degrading RGB quality (FVD)?
2. Does a single-view-depth + learned-estimator variant do worse than reading pose off the cross-view tracker?
3. How small is the pose-readout cost of predicted vs sensed pointmaps?
4. How far can the viewpoint move before pose accuracy degrades?
5. Does externalized geometry beat internalized (ConsisVLA-4D) where debuggability matters?
6. Is occlusion where predicted-geometry pose readout wins most (mirroring RecGen's +38.2 pp)?

> [!warning] Risks
> - Single anchor: headline from Geometry-aware 4D Robot Video's three-task eval. Fix: the consistency-ablation and predicted-vs-sensed comparison are the validity checks; broaden the task set.
> - Predicted pointmaps may be noisier than sensed depth. Fix: measure the gap; gate to where sensing is unavailable.
> - Three-task base is narrow. Fix: frame the contribution as *the mechanism*, validated on three tasks, broader eval next.

### C3: Natively-4D Geometry as a World-Representation Substrate
> [!abstract] The bet
> C3: The broad "native 4D beats recovered 4D" claim is now near-consensus, not open: X-WAM already ran the native-vs-recovered Chamfer ablation (0.0049 native vs 0.0401/0.0680 two-stage) and PointWorld already took the "explicit-4D-online beats latent, and transfers across embodiments" claim. What neither paper charted, and what C3 actually bets on: (i) generalizing Asynchronous Noise Sampling (a few-step denoising trick), does the action schedule step-distill to 1–4 steps, extending X-WAM's 5-step 15 Hz run (4665 ms to 1033 ms), without degrading read-out geometry, the latency-fidelity frontier PointWorld's point-flow MPC never charted; and (ii) does a native-4D RGB-D-video substrate, with its appearance channel intact, transfer world-model-to-policy at least as well as PointWorld's geometry-only point-flow, or is appearance the noise the doc's thesis says it is.

**Why**: Most deployed models imagine in 2D pixels, recovering geometry only implicitly, which X-WAM says yields physically implausible predictions. For contact-rich tasks the action is a function of geometry, and a pixel substrate re-infers it every step. X-WAM shows the two-stage path is both worse geometrically *and* slower than a unified 4D model with few-step (async) denoising. PointWorld owns the online-explicit + transfer claim, so C3 narrows to the two pillars.

**First-principles**
- *Principle:* the action's geometry lives in the task, not the rendering choice, so a native-4D substrate carries it directly.
- *Challenged:* the "4D too expensive, recover it two-stage" assumption is now settled false by X-WAM's own ablation, not just challenged; PointWorld separately already owns the broad online-explicit-beats-latent-and-transfers claim. Neither is what's left open.
- *Wager:* the action schedule step-distills to 1–4 steps without degrading read-out geometry, and the RGB-D appearance channel transfers world-model-to-policy at least as well as PointWorld's geometry-only point-flow, the two things neither X-WAM nor PointWorld charted.

**Sharpest questions**
1. Does X-WAM's self-reported native-vs-recovered Chamfer gap (0.0049 vs 0.0401) replicate on a third-party standardized fidelity protocol (Phys4D), not just X-WAM's own ablation?
2. Can the few-step (async) action schedule shrink to 1–4 steps without degrading read-out geometry? Plot Chamfer vs steps.
3. Does a native-4D RGB-D-video substrate carry from world model to policy head with appearance intact, matching PointWorld's point-flow transfer?
4. Does an explicit 3D channel lower contact-mode prediction error vs a latent?
5. Do camera poses derived from the end-effector improve OOD geometry?

> [!warning] Risks
> - 4D supervision needs depth/3D ground truth most datasets lack. Fix: X-WAM's end-effector camera poses plus off-the-shelf depth estimators; bound to recoverable geometry.
> - 4D only pays on geometry-bound tasks. Fix: score on contact/spatial tasks (RoboCasa insertion, stacking), not headline LIBERO.
> - Real-time 4D is now shown by two results (X-WAM native-RGB-D, PointWorld point-flow), and X-WAM already ran the native-vs-recovered Chamfer ablation, so the open question is no longer whether native beats recovered. Fix: treat the 1–4-step latency-fidelity frontier and the RGB-D world-model-to-policy transfer test as the go/no-go; concede X-WAM owns native-vs-recovered and PointWorld owns the broad transfer claim.

### C4: Persistent Geometric Memory as a Substrate-Agnostic Persistence Layer
> [!abstract] The bet
> C4: (i) A single world-frame memory layer, dropped over each of C1/C2/C3, raises minute-scale coherence above the bare substrate by a margin tracking 3D Persistent Embodied WM's SRC 81.7% vs 63.4% no-memory gap, so the layer works on any substrate, not just one it was built for. (ii) Geometric (MosaicMem) and episodic (Chameleon) memory *add up* on RoboMemArena (the two beat either alone on the 68.9% history-required subtasks) because they fix different failure modes. No single paper has demonstrated either.

**Why**: Explicit geometric memory beating attention-only on long-horizon coherence is *already taken* (3D Persistent Embodied WM, FVD 91.9 vs 194). The open gap: a memory layer serving *any* substrate, and a benchmark of geometric + episodic memory *together*. Object permanence is a property of the metric frame, so the *same* world-frame mechanism should pin C1's occupancy, C2's pointmaps, or C3's latent-4D. And geometric fixes *where*, episodic *which event*, so they add up.

**First-principles**
- *Principle:* object permanence lives in the metric world-frame, so one persistence mechanism serves any substrate; geometric and episodic memory are complementary.
- *Challenged:* the "memory built once per substrate, geometric vs episodic are alternatives" convention.
- *Wager:* one shared layer transfers across substrates, and the two memory types add up.

**Sharpest questions**
1. Drop one world-frame memory layer over C1/C2/C3, does each substrate's minute-scale coherence rise by a margin tracking the 81.7% vs 63.4% gap?
2. Do episodic events and geometric memory add up on RoboMemArena, beating either alone on history-required subtasks?
3. Does the combined advantage concentrate on look-alike-or-out-of-view subtasks and sit ≈0 on pure-revisit?
4. Does world-frame memory hold coherence better than robot-frame?
5. Does the one shared layer cost less than three custom memories at equal coherence?

> [!warning] Risks
> - Geometric memory needs reliable 3D lifting; estimators fail on texture-poor scenes. Fix: mix in implicit attention (MosaicMem) for graceful degradation.
> - Episodic retrieval can fire on look-alike but irrelevant events. Fix: disambiguated encoding plus goal-directed retrieval; validate on RoboMemArena occlusion and counting splits.
> - Memory adds footprint. Fix: the patch-level-vs-O(1)-TTT trade-off is the go/no-go; memory earns its place only if coherence gain beats cost.

## D: Reconstruction for Embodied Perception
*Reconstruction built for interaction-readiness: geometry carrying physics and kinematic structure, not radiance. Split by unit, D1 is a whole scene an agent acts in; D2 is the reusable single object that populates it.*

### D1: Interaction-Ready Scene Reconstruction: Whole Environments You Can Act In
> [!abstract] The bet
> D1: The deliverables are the *controlled measurement* and *articulation* readiness HoloScene's joint objective leaves out. (i) Build the same scene under a PSNR objective vs the survey's four readiness criteria. The fidelity-optimal asset fails ≥1 criterion more often; report pass/fail per criterion. (HoloScene only surfaces this as an ablation by-product.) (ii) Single-video reconstruction recovers rigid parts but fails jointed (articulated) structure for URDF/MJCF export without multi-view or interaction data, the rigid-body ceiling HoloScene names but doesn't cross.

**Why**: The reconstruction community optimizes radiance (PSNR/SSIM/FID); the survey names this the embodied bottleneck. An embodied agent interacts with geometry, physics, and kinematics, not radiance, so its value is interaction-readiness, separate from fidelity. The NeRF/3DGS "higher fidelity = better asset" default is *already documented false* (HoloScene's Table-3 trade-off; Single-View Mesh for Robotics missing the 2 mm bar).

**First-principles**
- *Principle:* embodied value is interaction-readiness (collide, grasp, articulate), separate from visual fidelity and not implied by it.
- *Challenged:* the higher-fidelity-is-better default (refuted by HoloScene + Single-View Mesh for Robotics); per-criterion measurement and single-video articulation remain unrun.
- *Wager:* fidelity-optimal scenes fail readiness measurably more, and single video misses articulation.

**Sharpest questions**
1. Build the same scene for PSNR vs the four readiness criteria, does the fidelity-optimal asset fail ≥1 criterion more often?
2. Does single-video reconstruction recover rigid parts but fail jointed structure for URDF/MJCF export without multi-view or interaction data?
3. Is there a physical-parameter readiness *threshold* (mass/friction/restitution) below sim-accurate fidelity where a policy still acts correctly?
4. Does a D1 readiness-asset feed A1's point head and C1's occupancy WM as well as a hand-built asset?
5. Does emitting simulator-format output directly beat meshing it afterward on readiness?

> [!warning] Risks
> - No standard readiness benchmark; it's a checklist. Fix: adopt the survey's four criteria; report pass/fail per criterion.
> - Single-video may not recover articulation or physics. Fix: bound what it recovers; fall back to multi-view or interaction data.
> - Boundary with Sim2Real-A1/B1 can blur. Fix: pin D1 to readiness as the target; route transfer-gap eval to GS-Playground and Real-to-Sim GS.

### D2: Object-Level Physical-Asset Generation: One Object That Carries Its Own Physics
> [!abstract] The bet
> D2: The controlled falsifier nobody has run decides it, not PhysX-Omni's existing generator. (i) Generate the *same* matched object set both ways, geometry-first-then-annotate, and jointly via a PhysX-Omni-style unified head. The staged pipeline fails the kinematic/material readiness criterion more often, concentrated on deformable + articulated objects and ≈0 on rigid props (SOPHY's skip-rigid choice hints at this). (ii) A physical-consistency metric (energy/momentum conservation check, NeuROK-style, Chamfer-L1 ≤0.028) predicts out-of-category readiness better than fidelity (PSNR/Chamfer), the generalization signal no scorecard isolates.

**Why**: D1 builds a whole scene; its reusable parts are objects. A fidelity-first object is a hollow prop, a watertight surface with no mass, friction, or joints (the survey names this bottleneck, deformable assets unsolved). An object's embodied value is a *joint* of geometry, material, and kinematics. The geometry-first convention is *already refuted* (PhysX-Omni, SOPHY, UniArt each generate physics-with-geometry in one pass), but a generator *existing* doesn't prove joint > staged.

**First-principles**
- *Principle:* an object's behavior under contact is set jointly by geometry, material, and kinematics, so they must be generated together.
- *Challenged:* the geometry-first-then-annotate convention (refuted by PhysX-Omni / SOPHY / UniArt); the matched-object joint-vs-staged falsifier and consistency-predicts-OOD test remain unrun.
- *Wager:* joint generation passes readiness where staged fails, largest on deformable and articulated objects; consistency (not fidelity) predicts out-of-category readiness.

**Sharpest questions**
1. On a matched object set, does staged geometry-first-then-annotate fail the kinematic/material readiness criterion more often than joint? Score rigid, deformable, articulated.
2. Is the joint advantage near-zero on rigid props, concentrated on deformable + articulated (makes SOPHY's skip-rigid explicit)?
3. Does an energy/momentum-consistency constraint at generation time predict out-of-category readiness better than fidelity (PSNR/Chamfer)?
4. Dropped into a D1 scene, is the binding transfer constraint a generated object's material or its kinematic structure?
5. Is deformable the widest gap and the largest single-pass win?

> [!warning] Risks
> - No shared cross-category leaderboard (PhysX-Bench leans rigid/articulated; PhysTwin, PhysHanDI are deformable-specific). Fix: adopt the survey's four criteria; report pass/fail per class.
> - Physical parameters from single video or sparse RGB-D may be under-determined. Fix: energy/momentum consistency constraints regularize them; bound to where they're pinned.
> - Boundary with D1 can blur. Fix: pin D2 to the single-object unit, D1 to whole-scene. A D2 object in a D1 scene is the intended composition.
