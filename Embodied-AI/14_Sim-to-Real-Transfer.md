---
title: "Sim-to-Real Transfer — Deep Dive"
tags:
  - sim-to-real
  - simulation
  - world-model
  - robotics
  - embodied-AI
  - domain-adaptation
aliases:
  - "Sim-to-Real Transfer"
  - "Sim2Real"
  - "Reality Gap"
  - "Sim-to-Real Survey"
---

# Sim-to-Real Transfer — Deep Dive

> [!abstract] Overview
> Simulation is the only economically viable substrate for training data-hungry embodied policies — but simulators are wrong about *something*: lighting, friction, contact transients, actuator dynamics, or the long-tail of object appearance. The "reality gap" is the operational cost of those errors when the policy meets the real world. This note maps the four parallel research threads that have evolved to close it: building **better simulators** ([[2310.06114|UniSim]], [[2501.03575|Cosmos]], [[2402.15391|Genie]], [[2604.18564|MultiWorld]]) that hallucinate richer worlds; designing **more robust policies** ([[2510.14246|DR-RPO]], [[2204.12581|RAMBO-RL]], [[2210.13702|DeXtreme]], [[2603.15956|ExpertGen]]) that absorb sim noise; closing **real→sim→real loops** ([[2503.17973|PhysTwin]], [[2511.07416|PhysWorld]], [[2404.09833|Video2Game]]) that rebuild the deployment scene as a digital twin; and constructing **reality-gap diagnostics** ([[2405.05941|SimplerEnv]], [[2605.06311|VISER]], [[2604.24018|Sim2Real-Betting]]) that let you measure how far you still are from real-world success.

## Evolution Graph

```text
1. Learned Simulators   (generate the sim instead of building it)
· video-model simulators
                     +action-conditioned
┌───────────────┐    ╔═════════════════╗
│ GAIA-1 (2023) │───►║ UniSim (2023)   ║─┐
└───────────────┘    ╚═════════════════╝ │
                                         │    +latent actions
                                         │    ╔══════════════╗
                                         ├───►║ Genie (2024) ║
                                         │    ╚══════════════╝
                                         │    +world foundation    +scaling laws
                                         │    ╔═══════════════╗    ┌─────────────────┐
                                         └───►║ Cosmos (2025) ║───►│ SimScale (2025) │
                                              ╚═══════════════╝    └─────────────────┘

2. Domain Randomization   (train across worlds so one is real)
· randomization & residuals
                          +Bayesian search
┌────────────────────┐    ┌──────────────┐
│ Residual RL (2018) │───►│ BayRn (2020) │─┐
└────────────────────┘    └──────────────┘ │
                                           │    +dexterous scale       +LLM-designed DR
                                           │    ╔═════════════════╗    ┌─────────────────┐
                                           ├───►║ DeXtreme (2022) ║───►│ DrEureka (2024) │
                                           │    ╚═════════════════╝    └─────────────────┘
                                           │    +robust policy
                                           │    opt
                                           │    ┌───────────────┐
                                           └───►│ DR-RPO (2025) │
                                                └───────────────┘

3. Online Adaptation   (close the gap after deployment)
· adapt to the real robot
                       +rapid                               +visual           +hierarchical
                       adaptation        +transformer       backbone          adapt
┌─────────────────┐    ╔════════════╗    ┌─────────────┐    ┌────────────┐    ┌──────────────┐
│ Sim2Real (2019) │───►║ RMA (2021) ║───►│ TERT (2022) │───►│ VBC (2024) │───►│ HiPAN (2026) │
└─────────────────┘    ╚════════════╝    └─────────────┘    └────────────┘    └──────────────┘

4. Teacher-Student Distillation   (privileged sim to blind real)
· privileged distillation
                            +dexterous grasp
┌──────────────────────┐    ╔══════════════════╗
│ Visual-Policy (2023) │───►║ DextrAH-G (2024) ║─┐
└──────────────────────┘    ╚══════════════════╝ │
                                                 │    +visual RL
                                                 │    ╔══════════════╗
                                                 ├───►║ VIRAL (2025) ║
                                                 │    ╚══════════════╝
                                                 │    +viser transfer
                                                 │    ┌─────────────────┐
                                                 └───►│ ViserDex (2026) │
                                                      └─────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

Four lanes, four ways to cross the same gap. Learned simulators generate the sim instead of building it, [[2310.06114|UniSim]] forking into interactive worlds ([[2402.15391|Genie]]) and scaled foundations ([[2501.03575|Cosmos]]). Domain randomization trains across many worlds so that one of them is real. Online adaptation is a single ladder — [[2107.04034|RMA]] through [[2604.26504|HiPAN]] — each generation adapting faster with less privileged information. Teacher-student distillation moves privileged simulator policies into blind real ones.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2018 | [[1812.03201\|Residual RL]] | Domain Randomization | The foundational residual reinforcement learning recipe: a hand-engineered feedback controller handles base motion |
| 2019 | [[1906.04452\|Sim2Real]] | Online Adaptation | Combines State Representation Learning, policy distillation of sequential-task teacher policies into one student |
| 2020 | [[2003.02471\|BayRn]] | Domain Randomization | Bayesian Domain Randomization: a bilevel loop where Bayesian Optimization over a Gaussian Process of sparse real-world |
| 2021 | [[2107.04034\|RMA]] | Online Adaptation | The canonical Rapid Motor Adaptation recipe: a base RL policy conditioned on a privileged extrinsics vector |
| 2022 | [[2210.13702\|DeXtreme]] | Domain Randomization | A PPO policy trained in [Isaac Gym](https://developer.nvidia.com/isaac-gym) on the Allegro Hand |
| 2022 | [[2212.07740\|TERT]] | Online Adaptation | A Terrain Transformer: a GPT-like transformer student predicting teacher actions directly from proprioceptive history |
| 2023 | [[2303.07026\|Visual-Policy]] | Teacher-Student | Distills a multi-camera teacher into a single-camera student under aggressive viewpoint randomization + curriculum |
| 2023 | [[2309.17080\|GAIA-1]] | Learned Simulator | A two-stage autoregressive world model + video diffusion decoder that frames world modeling as next-token prediction over |
| 2023 | [[2310.06114\|UniSim]] | Learned Simulator | A Conditional video diffusion model (**5.6B** params) with dataset orchestration over robot logs + human activity |
| 2024 | [[2402.15391\|Genie]] | Learned Simulator | A learned simulator of Latent-action interactive environments from unlabeled internet video via Video Tokenizer + Latent |
| 2024 | [[2403.16967\|VBC]] | Online Adaptation | A hierarchical visual whole-body-control framework for legged loco-manipulation: a low-level RL policy tracks EE |
| 2024 | [[2406.01967\|DrEureka]] | Domain Randomization | An LLM-automated sim-to-real pipeline synthesizing safety-regularized reward functions in code and configuring domain |
| 2024 | [[2407.02274\|DextrAH-G]] | Teacher-Student | Integrates Geometric Fabrics (collision-safe inductive bias) with a privileged PPO teacher over 140 objects |
| 2025 | [[2501.03575\|Cosmos]] | Learned Simulator | An open-source World Foundation Model Platform from NVIDIA that curates **20M hr** raw video → **100M** clips and pre-trains |
| 2025 | [[2510.14246\|DR-RPO]] | Domain Randomization | The first provably efficient *online* policy-optimization algorithm for robust MDPs with linear function approximation |
| 2025 | [[2511.15200\|VIRAL]] | Teacher-Student | A visual sim-to-real framework at scale for humanoid loco-manipulation built on two-phase teacher-student learning |
| 2025 | [[2511.23369\|SimScale]] | Learned Simulator | A 3D Gaussian Splatting reconstruction sim that bridges the sim-real visual gap for autonomous driving |
| 2026 | [[2604.11138\|ViserDex]] | Teacher-Student | A monocular-RGB dexterous-reorientation method that puts 3D Gaussian Splatting *in the simulation loop* |
| 2026 | [[2604.26504\|HiPAN]] | Online Adaptation | A two-level hierarchical RL (goal-seeking + posture-adaptive locomotion) for quadruped navigation in unstructured 3D scenes |

---

## Part A — Foundations

*Design-space principles: three axes (sim quality / adaptation locus / evaluation grounding) that classify every sim-real strategy.*

### 1. Design-Space Principles

Three orthogonal axes determine every sim-to-real strategy. Choose your point on each axis — *what* you simulate, *where* the adaptation happens, and *how* you measure success — and the rest of the design is forced. Most papers in §2–§5 are interpretable as points in this 3-D space; the trade-offs are not soluble individually because each axis has a cost on the others.

> [!success] The Three Axes
> - **Sim quality**: hand-crafted MPM/[PhysX](https://developer.nvidia.com/physx-sdk) (precise, narrow) vs. learned video simulator (broad, blurry) vs. real2sim digital twin (precise + deployable)
> - **Adaptation locus**: in the simulator (domain randomization, system-id) vs. in the policy (robust RL, distillation) vs. at deployment (TTA, online adaptation)
> - **Evaluation grounding**: sim-only proxy metrics vs. sim-real correlation (Pearson r, MMRV) vs. real-only ground truth

#### 1.1 Axis 1 — Sim Quality

How accurate or rich is the simulator itself? Four families, ordered from narrowest-precise to broadest-blurry to deployment-specific.

| Approach | Mechanism | Example |
|----------|-----------|---------|
| **Hand-crafted physics** | [PhysX](https://developer.nvidia.com/physx-sdk) / [MuJoCo](https://mujoco.org) / [[2511.04831\|Isaac-Lab]] with explicit constitutive laws | [[2210.13702\|DeXtreme]], [[2603.16861\|MolmoBot]] |
| **Learned video simulator** | Diffusion-based video model conditioned on actions | [[2310.06114\|UniSim]], [[2501.03575\|Cosmos]], [[2402.15391\|Genie]] |
| **Hybrid (sim + neural rendering)** | Physics sim + 3DGS / NeRF-rendered visuals | [[2604.11138\|ViserDex]], [[2604.11674\|AffordSim]] |
| **Digital twin from video** | Reconstruct deployment scene as interactable sim | [[2503.17973\|PhysTwin]], [[2404.09833\|Video2Game]], [[2511.07416\|PhysWorld]] |

#### 1.2 Axis 2 — Adaptation Locus

*Where* in the pipeline does the system absorb the sim-real gap? Trade compute against deployment latency against generalization breadth.

| Where adaptation happens | Cost | Generalization |
|--------------------------|------|----------------|
| **In simulator** (domain randomization) | High training compute | Broad — covers the *imagined* range |
| **In policy** (robust RL, distillation) | High RL stability cost | Tight — robust to the *trained* perturbations |
| **At deployment** (TTA, world-model online adaptation) | Latency at deployment | Adaptive — handles new distribution shifts |

#### 1.3 Axis 3 — Evaluation Grounding

How do you *know* your sim-to-real strategy works before you ship? The metric you pick determines what you can claim.

| Metric | What it measures | Failure mode |
|--------|------------------|--------------|
| **Sim-only proxy** (success rate in sim) | Cheap, fast | Fails to predict real (see [[2604.10856\|BridgeSim]] OL-CL gap) |
| **Sim-real correlation** (Pearson r) | Sim's predictive value | Fragile to OOD perturbations |
| **MMRV / Kelly betting** (rank reliability) | Whether sim ranks policies correctly | Requires bank of diverse sims |
| **Real-only ground truth** | Authoritative | Expensive, slow, unsafe |

**Design-Space — Decision Matrix**

| Need | Recommendation |
|------|---------------|
| Scale to internet-video data | Learned sim: [[2310.06114\|UniSim]] / [[2501.03575\|Cosmos]] / [[2402.15391\|Genie]] |
| Physical accuracy on contact | Hand-crafted physics ([MuJoCo](https://mujoco.org) / [[2511.04831\|Isaac-Lab]]) + DR ([[2210.13702\|DeXtreme]]) |
| Fast deployment-specific transfer | Digital twin: [[2503.17973\|PhysTwin]] / [[2511.07416\|PhysWorld]] / [[2504.03597\|Real-is-Sim]] |
| Cheap visual diversity + physical contact | Hybrid 3DGS + physics: [[2604.11138\|ViserDex]] / [[2511.23369\|SimScale]] / [[2604.11674\|AffordSim]] |
| Publishable rigor on sim claims | Pair with correlation benchmark: [[2405.05941\|SimplerEnv]] (r > 0.85) or [[2605.06311\|VISER]] (r = 0.92) |
| Long-deployment continual shift | Adaptation-at-deployment: [[2603.04029\|Self-Adapting-RL]] with [[2301.04104\|DreamerV3]] feedback |
| Combine many imperfect sims | Statistical estimator: [[2604.24018\|Sim2Real-Betting]] (Kelly portfolio) |

^dm-1

> [!star] Key Papers — Design-Space Exemplars
> - [[2310.06114|UniSim]] — Pure Axis-1 learned-sim exemplar; **3-4×** zero-shot policy gain via ==conditional video generation== with a **5.6B**-parameter diffusion model
> - [[2210.13702|DeXtreme]] — Pure Axis-2 in-simulator-adaptation exemplar; ==Vectorized Automatic Domain Randomization== doubles transfer (**27.8** vs **14.8** reorientations on Allegro Hand)
> - [[2405.05941|SimplerEnv]] — Pure Axis-3 evaluation exemplar; first reliable correlation benchmark (**r > 0.85**) with ==MMRV== rank metric
> - [[2511.07416|PhysWorld]] — All-three-axes integrated; digital twin (Axis 1) + residual RL (Axis 2) + 10-task real-world ground truth (Axis 3), **82%** average success
> - [[2604.24018|Sim2Real-Betting]] — Reframes Axis 3 as variance reduction; **70-100%** win rate vs Monte Carlo using a ==Kelly portfolio== of biased simulators

^key-papers-1

> [!tip] Pick by Constraint
> If you need to **scale to internet video data**, pick learned sim ([[2310.06114|UniSim]]/[[2501.03575|Cosmos]]). If you need **physical accuracy on contact**, pick hand-crafted physics ([MuJoCo](https://mujoco.org) + DR). If you need **fast deployment-specific transfer**, pick a digital twin ([[2503.17973|PhysTwin]]/[[2511.07416|PhysWorld]]). If you need **publishable rigor**, pair any of these with a correlation benchmark ([[2405.05941|SimplerEnv]]/[[2605.06311|VISER]]). The three axes are *not* independent in practice — better sim quality (Axis 1) reduces the burden on policy-side robustness (Axis 2), and tighter correlation benchmarks (Axis 3) force investment in both. See [[06_WAM#2. VideoGen WAMs]] for the WAM-as-simulator perspective on Axis 1, and [[08_Physics-Aware-Embodied-AI#4. External Simulators in the Optimization Loop]] for the digital-twin coupling that bridges Axes 1 and 2.

^insight-1

---

## Part B — Closing the Gap

*Three complementary attack surfaces: sim-side (better simulators), policy-side (robustness), and real2sim2real (digital twins).*

### 2. Sim-Side: Learned & Procedural Simulators

The first sim-to-real strategy is to make the simulator richer than reality — through learned video generation, procedural environment scale, or photorealistic rendering. The trade-off: learned simulators handle visual diversity well but blur on physical contact; hand-crafted simulators handle contact well but require enormous procedural-asset effort to cover the visual long tail.

#### 2.1 Learned Sensory World Simulators

Learn the sensory simulator directly from data so the model itself becomes the simulator: internet-scale video world models, plus learned audio ([[2507.02864|MultiGen]]) and event-camera ([[2606.02058|TIDES]]) simulation for sensory streams hand-crafted renderers cannot produce. A complementary hand-crafted-but-LLM-driven track ([[2601.02078|Genie-Sim-3.0]]) converges on the same goal (cheap, scalable, photorealistic, evaluable) from the opposite direction.

- **[[2606.02058|TIDES]]** — A simulator doing ==Time-derivative event simulation== from a dynamic ==4D Gaussian splatting== scene: ==visibility-consistent time-derivatives of log-luminance== via forward-mode autodiff + ==risk-guided adaptive time-stepping==; best fidelity (lowest **IG-NLL** + **Chamfer**); **models trained on TIDES events transfer best to real data**.
- **[[2604.18564|MultiWorld]]** — A multi-agent multi-view video world model on an ==action-conditioned diffusion== + ==Flow Matching== backbone; its ==Multi-Agent Condition Module== (==Agent Identity Embedding== RoPE, ==Adaptive Action Weighting==, ==Global State Encoder== over ==VGGT==) handles variable agent/view counts from one checkpoint; **FVD 179** vs 207–245, **RPE 0.67** vs 0.72–0.75.
- **[[2602.18690|Motor-Gated Neural Fields]]** — A neurobiologically-inspired ==motor-gated neural field== (Amari-style local lateral dynamics, not video-diffusion) preserves spatial topology as a frozen differentiable simulator for offline policy training; **0%** trajectory teleportation vs VAE-LSTM's **15.4%**, **81.5%** transfer catch-rate vs **46.0%**.
- **[[2511.23369|SimScale]]** — A ==3D Gaussian Splatting== reconstruction sim that bridges the sim-real visual gap for autonomous driving; its ==pseudo-expert pipeline== couples reactive ==Intelligent Driver Model== agents with ==LQR== ego + trajectory perturbation; weak baselines (LTF, DiffusionDrive) see **>20%** relative gains under sim-real co-training; **EPDMS 48.0** on navhard.
- **[[2507.02864|MultiGen]]** — ==MULTIGEN== augments a physics simulator (RoboVerse visuals/kinematics) with a ==generative audio== diffusion model (finetuned MMAudio + SAMv2 segmentation conditioning) for hard-to-simulate sensory streams; zero-shot real pouring at **0.46 NMAE**, audio cuts NMAE **23.3%** (**29.4%** for opaque containers).
- **[[2501.03575|Cosmos]]** — An open-source ==World Foundation Model Platform== from NVIDIA that curates **20M hr** raw video → **100M** clips and pre-trains diffusion + autoregressive ==WFMs== fine-tuned for navigation/manipulation/driving; Tokenizer suite +**4 dB** PSNR, **2-12×** faster inference; repositions WFMs as a foundation-model category analogous to LLMs.
- **[[2402.15391|Genie]]** — A learned simulator of ==Latent-action interactive environments== from unlabeled internet video via ==Video Tokenizer + Latent Action Model (LAM) + Dynamics Model==; its ==ST-transformer== separates spatial/temporal attention for linear-in-frames scaling. Learns discrete latent action codes unsupervised; the foundational unsupervised-action-discovery simulator.
- **[[2310.06114|UniSim]]** — A simulator doing ==Conditional video generation== via ==5.6B-parameter video diffusion==; orchestrates heterogeneous data (robotics, human activity, panoramas, web video) into a ==unified action space== (lang + control → ==T5 embeddings==); zero-shot sim-to-real on real robots, **3-4×** better goal reduction for VLMs, captioning fine-tune CIDEr **15.2 → 46.23**.
- **[[2309.17080|GAIA-1]]** — A two-stage ==autoregressive world model + video diffusion decoder== that frames world modeling as ==next-token prediction== over a common token space (video + text + actions); generates **40s+** photorealistic action-conditioned rollouts, demonstrating LLM-style scaling for driving WMs — early proof learned simulators could model long-horizon driving dynamics.
- **[[2601.02078|Genie-Sim-3.0]]** — A hand-crafted-but-LLM-driven humanoid simulation platform whose ==Genie Sim Generator== composes scenes from natural-language instructions, with ==LLM-VLM auto-evaluation== and ==3D Gaussian Splatting== reconstruction; **R²=0.94** sim-real correlation, and **1,500 episodes** of synthetic data beat real-data baselines zero-shot.

#### 2.2 Procedural Environment Generation

Hand-crafted physics + massive procedural scale; no learned visual model.

- **[[2607.08098|EVIS]]** — A physics-grounded ==event camera== plugin for NVIDIA Isaac Sim using a ==log-intensity contrast model== + ==motion-vector frame interpolation== for kHz-scale event streams with six configurable ==sensor noise== models; **240 Hz** at **1.2x** real-time, generated events consumed directly by pretrained E-RAFT/E2VID with sub-pixel optical-flow accuracy.
- **[[2606.19641|Self-Play]]** — ==Gigapixel==, a **1000×**-faster-than-HUGSIM batched bounding-box driving simulator, trains pixel-based end-to-end policies via ==self-play DAgger== distillation from a vectorized teacher, then a frozen-planner ==perception-only sim-to-real adaptation==; **+12.5** HD-Score over BC.
- **[[2604.17513|FLASH]]** — A ==GPU-native simulation framework== approximating the ==Schur complement== for contact-rich deformable dynamics, paired with ==digital-twin calibration== (system ID + perception augmentation) and ==teacher-student distillation==; **100-300×** training speedup, **85.8%** real dual-arm towel folding zero-shot.
- **[[2603.16861|MolmoBot]]** — An ==MolmoBot-Engine== procedural data generator in ==[MuJoCo](https://mujoco.org)==; **232K** indoor environments, **48K** objects, **1.8M** expert trajectories; ==domain randomization== enables zero-shot sim-to-real *without real fine-tuning*; **79.2%** real [Franka FR3](https://franka.de) pick-and-place — beats real-data π0.5-DROID (**39.2%**).
- **[[2604.11674|AffordSim]]** — An affordance-aware data generator integrating ==VoxAfford== open-vocabulary 3D affordance prediction with ==two-stage grasp selection== and ==3DGS background-replacement== DR; collection reaches **79%/64%** (medium/hard) vs AnyGrasp's **15%/3%**, yet zero-shot Franka FR3 sim-to-real averages just **24%** — canonical evidence that affordance is the DR ceiling.
- **[[2602.09153|SceneSmith]]** — An agentic generator of ==simulation-ready== articulated indoor scenes from natural language via a ==Designer-Critic-Orchestrator VLM trio==, with text-to-3D + articulated-library retrieval and ==non-penetration projection + gravity settling==; **71.1** objects/room (3-6× denser), **1.2%** collision rate, **95.6%** static stability, **92.2%** realism win-rate.
- **[[2601.22550|Exo-Plore]]** — A ==human-aligned neuromechanical== simulator closing the exoskeleton sim-to-real gap via a ==DRL gait generator== (PoseNet + muscle net) with a ==metabolic + human-exoskeleton-interaction reward== calibrated to real cost-of-transport curves, plus a surrogate optimizer; recovers pathology-specific optimal assistance without human-in-the-loop trials.
- **[[2505.10755|Infinigen-Articulated]]** — A procedural articulated-asset toolkit using ==Blender Geometry/Shader Nodes== with custom revolute/prismatic joint node-groups, auto-converting to ==simulation-ready URDF/USD/MJCF==; RL policies trained only on it improve success **2.86×** over PartNet-Mobility and lift real door-opening to **18/30** (vs **3/30**) zero-shot.
- **[[2504.09997|GenTe]]** — A ==dual-level terrain simulation framework== for legged locomotion modeling both geometry (height maps, obstacles) and physical interactions (water wading, deformable sand) with realistic forces, using ==VLMs + function-calling== to generate contextual terrains; policies hold high success on diverse unseen VLM-generated terrains.

#### 2.3 Synthetic Demonstration Generation

Generate diverse, action-consistent training demonstrations — via video diffusion or sim-replay — to amortize real-world collection and close the visual sim-to-real gap.

- **[[2606.15338|SimWeaver]]** — A deformable-manipulation sim-to-real system pairing a robust simulator (==active-collision-region scheme==) with a ==topology-aware trajectory synthesizer== and a real protocol of ==cloth-state randomization== + ==sensor-aware photometric augmentation==; **91.30%** avg zero-shot RGB sim-to-real from 200 sim demos at **$0.03**/trajectory.
- **[[2606.08548|OASIS]]** — Simulation-data-driven humanoid loco-manipulation: ==VR-teleoperated== kinematic capture + offline rendering under extensive ==visual domain randomization==, feeding a ==hierarchical Flow-Matching visuomotor policy==; **1.84×** faster data collection than real teleop, **0.83** avg real SR with full visual DR, lighting the dominant factor.
- **[[2604.03552|CRAFT]]** — A ==video diffusion==-based bimanual data generator that replays real demos into varied sim trajectories, extracts ==Canny-edge control videos==, and conditions a diffusion transformer across ==seven augmentation axes== (pose, lighting, color, background, viewpoint, multi-view, cross-embodiment); **89.3%** sim cross-embodiment and **17-19/20** real generalization.
- **[[2603.25725|SoftMimicGen]]** — A deformable-object data-generation system using ==non-rigid registration== to adapt 1-3 human demos into thousands of demonstrations via a continuous ==deformation field== in Isaac Lab; **70-100%** generation success, **25-97%** higher policy SR than source-only, and zero-shot sim-to-real (**63.3%**, **93.3%** with co-training).
- **[[2512.11797|AnchorDream]]** — A ==video diffusion== robot-data synthesizer using a ==decoupled trajectory-environment== paradigm: render ==robot-only motion videos== as conditioning, then a pretrained diffusion model fills photorealistic objects/scenes coherent with the anchored motion; **+36%** sim (RoboCasa) and real SR doubled **28% → 60%** across six PiPER tasks.
- **[[2508.03944|Constraint-Preserving-DataGen]]** — A constraint-preserving data generator (CP-Gen) that formulates skills as ==object-centric keypoint-trajectory constraints== from one demo, then samples novel poses and non-uniform geometries and re-optimizes joint configs; **70%** sim and **83%** zero-shot sim-to-real on novel-geometry tasks (vs MimicGen **40%**).
- **[[2505.09109|FoldNet]]** — Synthesizes diverse garment meshes with automatic ==keypoint annotations== (generative textures + VLM filtering) and generates error-recovery demos via ==Keypoint-Gated DAgger==; ==Diffusion Policy== reaches **90%** sim / **75%** real folding (**+25pp** over no-recovery), **70%** on an unseen robot via π0 fine-tune.
- **[[2502.20382|Physics-Driven-Data-Gen]]** — A contact-rich data generator collecting ==VR human-hand demos== (Apple Vision Pro + Drake), applying ==kinematic motion retargeting== per embodiment, then ==demonstration-guided trajectory optimization== with ==domain randomization== for dynamically-feasible diverse data; lifts cube-flip real sim-to-real **26% → 70-74%** over human-demo-only.
- **[[2405.01472|IntervenGen]]** — Autonomously generates diverse corrective-intervention trajectories from just 10 human interventions via ==closed-loop policy execution== (genuine mistakes) + object-centric replay of recovery segments; **39x** success-rate gain, zero-shot sim-to-real Franka grasping at **90%**.
- **[[2306.01872|Video Adapter]]** — Guides a small domain-specific video-diffusion model with a frozen **5.6B**-parameter pretrained model's score function (==EBM product distribution==, low-temperature CFG) using just **1.25%** extra parameters; generates paired sim/real robotic videos with style augmentation for domain-randomization-style data.

**Sim-Side — Decision Matrix**

| Need | Recommendation |
|---|---|
| Scale to internet-video diversity, blur-tolerant on contact | [[2501.03575\|Cosmos]] or [[2310.06114\|UniSim]] — learned video-WFMs; **100M** clips / **3-4×** zero-shot gain |
| Multi-agent multi-view interactive simulator | [[2604.18564\|MultiWorld]] — action-conditioned diffusion + Flow Matching; **FVD 179**, **RPE 0.67** |
| Sim-real visual gap closure for autonomous driving | [[2511.23369\|SimScale]] — 3DGS reconstruction + sim-real co-training; **EPDMS 48.0** on navhard |
| Latent-action interactive environments from unlabeled web video | [[2402.15391\|Genie]] — unsupervised action discovery; foundational learned-sim |
| Long-horizon photorealistic driving rollouts | [[2309.17080\|GAIA-1]] — generative WM; 40s+ action-conditioned rollouts |
| LLM-driven scene composition + auto-evaluation for humanoid | [[2601.02078\|Genie-Sim-3.0]] — **R²=0.94** sim-to-real correlation, **10K+ hr** synthetic |
| Procedural physics scale, no learned visual model, real-data-free | [[2603.16861\|MolmoBot]] — **232K** environments + [MuJoCo](https://mujoco.org); **79.2%** real Franka beats π0.5-DROID |
| Affordance-aware procedural sim for grasp/pour/hang | [[2604.11674\|AffordSim]] — VoxAfford + 3DGS DR; **+10pp** average, exposes the semantic-DR ceiling |
| Hybrid 3DGS-augmented physics (visual + contact accuracy) | [[2511.23369\|SimScale]] / [[2604.11674\|AffordSim]] / [[2604.11138\|ViserDex]] — the emerging sweet spot |

^dm-2

> [!star] Key Papers
> - [[2310.06114|UniSim]] — Learned interactive real-world simulator; **3-4x** better zero-shot policy transfer than baselines; foundational learned-sim paper
> - [[2501.03575|Cosmos]] — NVIDIA WFM platform: **100M** curated clips, **+4 dB** PSNR tokenizer, **10 FPS** real-time autoregressive generation; defines the WFM category
> - [[2603.16861|MolmoBot]] — **79.2%** real [Franka FR3](https://franka.de) success trained *exclusively* on procedural [MuJoCo](https://mujoco.org) data; proves sim-only can outperform real-data baselines (π0.5-DROID **39.2%**)
> - [[2511.23369|SimScale]] — 3DGS sim-real co-training for autonomous driving; weak baselines see **>20%** relative gains; new **EPDMS 48.0** on navhard

^key-papers-2

> [!tip] Sim-Side Trade-Off
> Learned video simulators ([[2310.06114|UniSim]], [[2501.03575|Cosmos]]) scale to internet video and capture visual diversity but blur on contact dynamics. Procedural physics simulators ([[2603.16861|MolmoBot]]) handle contact accurately but require massive procedural-asset effort to cover the visual long tail. Hybrid 3DGS-augmented physics ([[2511.23369|SimScale]], [[2604.11674|AffordSim]], [[2604.11138|ViserDex]]) is the emerging sweet spot. Cross-reference [[02_Dataset-Benchmark-Environment#3. Simulation Environments]] for the simulator roster this trade-off ranges over and [[02_Dataset-Benchmark-Environment#4. Physics Engines as Research Substrate]] for the contact-solver layer underneath.

^insight-2

---

### 3. Policy-Side: Robustness & Domain Randomization

Instead of making the simulator perfect, make the *policy* invariant to sim imperfections. This is the dominant industrial-scale recipe — domain randomization remains the de-facto sim-to-real method in 2026.

#### 3.1 Domain Randomization Foundations

The canonical industrial recipe: train in sim with extensive randomization, then either distill to vision or layer a real-world residual on top.

- **[[2607.18135|Isaac Sim-to-Real Quadruped RL]]** — A straight ==PPO== policy trained in ==Isaac Sim== with comprehensive ==domain randomization== (friction, mass, terrain, pushes) plus an ==actuator-net== MLP for Unitree Go1's nonlinear dynamics; zero-shot transfer matches the stock controller on velocity tracking (**2.0 m/s**) and disturbance rejection across gravel, sand, and inclines.
- **[[2607.14997|AeroAct]]** — An action-centered ==World-Action Model== (video-diffusion Transformer) for language-conditioned quadrotor flight, predicting fifth-order-polynomial trajectory chunks while decoupling visual prediction from inference, trained on hybrid ==Isaac Lab + 3DGS== + handheld data; **100%** sim success / **0%** collisions, first reported real-world WAM-quadrotor flight.
- **[[2607.11874|REGRIND]]** — A minimalist real-to-sim-to-real dexterous recipe: ==interaction-aware motion retargeting== turns one human demo into a physically-plausible reference guiding a residual RL policy (asymmetric actor-critic + keypoint reward) with DR; zero-shot on **3/4** contact-rich tasks, **9/10** LEAP-Scissors, **10/10** LEAP-Screwdriver on real hardware.
- **[[2607.11481|TELEDEXTER]]** — A ==hand-object co-tracking== teleoperation controller mapping operator targets to contact execution via ==consecutive subgoal tracking==, with DR and a ==random action masking== regularizer for zero-shot transfer; **75.2%** avg SR across seven real dexterous tasks with a SharpaWave hand, autonomous Diffusion Policies reaching **40-73%** SR.
- **[[2607.10892|ESM]]** — ==Energy-Guided Score Matching== trains a single ==diffusion-policy== controller for multi-task block pushing via online RL from sparse rewards (no demos), using an ==objective-centric state representation== + ==reverse curriculum==; **100%** sim SR, **61%** on unseen block shape, all **36** real zero-shot tasks completed across varying friction/weight/goal poses.
- **[[2607.01281|WaveLander]]** — A ==hierarchical RL== framework decoupling a compact vertical-decision policy (descent/hold/retreat) from low-level flight stabilization for UAV landing on wave-disturbed platforms; touchdown success **8-33% → 30-76%** across tilt severities, zero-shot MuJoCo→Isaac Sim SITL transfer plus real-hardware deployment.
- **[[2607.00160|Phase-Decomposed RL]]** — Decomposes lunar cargo transport into ==lifting/transportation/placement== phase-specific ==PPO== policies with a discrete MDP phase controller + ==synchronization clamp==, trained with domain randomization; a monolithic policy fails to converge, while phased policies transfer zero-shot to lunar-analog hardware across **5.3-9.5 kg** payloads.
- **[[2606.31101|Sim-to-Real WAM]]** — First reported zero-shot sim-to-real transfer of a ==world-action model== (==Cosmos Policy==) trained purely on **3,200** ==AnyTask==-generated synthetic demos with extensive DR, no real data; **35%** avg real-Franka success, beating Diffusion-Policy baselines trained on 50 real demos (**25%**).
- **[[2606.31043|Warp RL]]** — Generalizes additive residual RL into an ==invertible, state-conditioned RQ-spline-flow warp== of a frozen base policy's action distribution, identity-initialized and compatible with PPO/SAC/Evolution-Strategies; beats residual RL on hard ManiSkill3 tasks (**70.6%** vs **57.4%**) and cuts real peg-insertion cycle time **30%**.
- **[[2606.27163|LeHome]]** — A prize-winning bimanual garment-folding recipe combining a ==π0.5==-based VLA with ==AWR + RECAP-style advantage conditioning== and human-in-the-loop DAgger over heavy simulation DR, plus environment-alignment + motion-intensity-matched real fine-tuning; **79.63%** sim SR (1st place), 2nd place real-world ICRA final.
- **[[2606.11525|IWR]]** — ==Interaction-Weighted Resampling== reshapes the Contrastive RL training distribution, up-weighting goals near predicted interaction events via a ==Gaussian-kernel weighting== on the ==InfoNCE== objective for mode-conditioned dynamics; **+19.8%** avg gain across sim benchmarks, real UR5e air-hockey transfer at **60%** SR, a **140%** gain over the next-best CRL method.
- **[[2605.09789|DRIS]]** — A ==structured, VRAM-efficient randomization== recipe for zero-shot dexterous *reactive catching*, robust to observation noise, execution error, and OOD physical parameters at far lower VRAM than brute-force randomization; **68%** real flat-plate catching vs hand-crafted **5%** / sim-trained **13%**, with emergent generalization to human-thrown objects.
- **[[2605.21688|Microfiber-Shape-Control]]** — A closed-loop sim-to-real RL method for deformable *microfiber* shaping that trains in a ==frictionless MuJoCo sim== (geometry-focused) and deploys zero-shot with ==real-time visual feedback==; **270 µm** mean / **390 µm** max error on 50 µm silk, generalizing across fiber diameters and to higher-bending-energy targets unseen in training.
- **[[2601.02778|Force-Based-Sim2Real]]** — A sim-to-real RL framework for zero-shot force-aware manipulation on a real 5-finger hand via ==asymmetric actor-critic PPO== in ==IsaacLab==; a ==distance-field tactile sim== maps touch to force features, plus ==current-to-torque calibration== + a randomized actuator; in-hand rotation reaches **25.1** *with* tactile vs **1.1** *without*.
- **[[2510.01708|PolySim]]** — A ==multi-simulator dynamics randomization== framework training one RL whole-body policy concurrently across heterogeneous physics engines via a ==Simulator Router== harmonizing APIs, so the mixed transition kernel is provably closer (Wasserstein) to reality; **+52.8%** zero-shot SR on an unseen MuJoCo domain, zero-shot real Unitree G1.
- **[[2506.10133|Offline-Domain-Randomization]]** — A statistical-guarantees framework for ==Offline DR== that formalizes it as ==Maximum-Likelihood Estimation== of a simulator-parameter distribution from offline data, proves **weak and strong consistency** (learned randomization concentrates on true params), and adds ==α-informativeness==, extending to ergodic data + *identified-set* convergence.
- **[[2210.13702|DeXtreme]]** — A ==[[1707.06347|PPO]]== policy trained in ==[Isaac Gym](https://developer.nvidia.com/isaac-gym)== on the Allegro Hand, where the foundational ==Vectorized Automatic Domain Randomization== (VADR) adjusts sim params by policy capability; **27.8** mean real reorientations vs **14.8** hand-tuned DR — auto-DR nearly doubles transfer.
- **[[2603.15956|ExpertGen]]** — A three-phase scalable sim-to-real recipe that learns from *imperfect* behavior priors: (1) a generative ==diffusion policy== prior; (2) ==Diffusion Steering RL (DSRL)== optimizes only the diffusion's initial noise; (3) ==DAgger== visuomotor distillation; **90.5%** avg on 8 AutoMate tasks, **80%** real [Franka](https://franka.de) Lift Banana from RGB.
- **[[2603.08111|DeReCo]]** — A three-stage MARL recipe decoupling ==object-dependent representation== from ==multi-agent coordination== via a ==privileged-info MAPPO teacher== + supervised ==adaptive encoder== distillation; **0.80** unseen-object SR in sim, real dual-HSR transport **9/10** zero-shot on unseen objects.
- **[[2603.04166|Hip-Exoskeleton-Control]]** — A neuromusculoskeletal-sim RL recipe (SAC) distilling a privileged teacher into a single-IMU ==TCN student== for a hip exoskeleton; sim-to-real torque agreement **r=0.82±0.19**, reducing muscle activation up to **3.4%**.
- **[[2502.20396|Humanoid-Sim2Real-Dex]]** — A vision-based dexterous-manipulation recipe for the Fourier GR-1 humanoid where ==autotuned robot modeling== bridges the dynamics gap, plus ==contact stickers==, ==stage-based rewards==, and ==divide-and-conquer distillation==; **80%** box-lift, **62.3%** grasp-and-reach, **52.5%** bimanual handover, **60-80%** unseen-object generalization.
- **[[2506.13751|LeVERB]]** — A whole-body humanoid VLA with zero-shot sim-to-real on Unitree G1, whose learned latent ==verb vector== bridges a high-level ==residual CVAE== VLA and a low-level ==DAgger==-distilled reactive controller; **58.5%** mean success across 10 task categories (**7.8×** over naive hierarchical VLA's **7.5%**); align a *latent intermediate*, not *actions*.
- **[[2602.23253|SPARR]]** — An industrial-assembly recipe whose sim base trains via ==PPO + dense imitation rewards==, then adds a **real-world residual** — the base policy autonomously generates demos and a ==vision-conditioned residual== via ==RLPD== corrects them; **95-100%** on 10 AutoMate (**+38.4%**, matching [[2410.21845|HIL-SERL]] with no human supervision); **+74.5%** unseen NIST.
- **[[2606.18953|Object-Centric-Residual-RL]]** — A residual RL framework adding a sim-trained corrective policy to a frozen real-world base VLA over a ==domain-invariant observation space== (object poses + proprioception + base action) with ==pose noise injection + dropout==; zero-shot real SR **42% → 76%**, and a VLA self-improvement loop lifts the base **42% → 59%**.
- **[[2505.11858|Tight-Insertion-Sim2Real]]** — A hybrid framework pairing a ==potential-field controller== with a ==residual RL== policy for sub-millimeter insertion, with a ==curriculum== escalating observation noise and correction magnitude; **>90%** real-world zero-shot success across object configs, beating IndustReal without real fine-tuning.
- **[[2407.18902|Lessons-from-to]]** — First continuous real-world pen-spinning: a privileged oracle PPO policy pre-trains a proprioceptive student on its rollouts, then fine-tunes on **~50** real oracle-replay trajectories; direct ==DAgger== distillation fails outright, beating pure open-loop replay by **10-30%** on unseen pens.
- **[[2406.01967|DrEureka]]** — An ==LLM-automated== sim-to-real pipeline synthesizing ==safety-regularized reward functions== in code and configuring ==domain randomization== from a ==Reward-Aware Physics Prior== of feasible param ranges; **~34%** higher quadruped forward velocity than human-designed policies and the first quadruped to walk on a yoga ball — LLMs as the DR-and-reward designer.
- **[[2307.12074|MRLM]]** — A multi-stage RL framework (**P2ManNet**) decomposing occluded grasping into four ==point-cloud state-goal fusion== stages with a ==spatially-reachable distance metric== reward, trained via SAC + ==Automatic Domain Randomization==; **100%/95%** sim far/close-grasp, **95%/67.5%** zero-shot real UR5e.
- **[[2305.17110|IndustReal]]** — The foundational contact-rich assembly recipe transferring ==GPU-accelerated [Isaac Gym](https://developer.nvidia.com/isaac-gym) RL== via ==Simulation-Aware Policy Update==, ==SDF dense rewards==, a ==sampling-based curriculum==, and a ==Policy-Level Action Integrator==; **80%** pegs / **97.5%** gears / **100%** unseen NEMA connectors, no real fine-tuning.
- **[[2207.14561|Cyclic-Policy-Distillation]]** — Partitions the randomized domain into sub-domains with a ==cyclic monotonic policy-mixing== scheme (beats DiDoR/P2PDRL baselines) before late-stage global distillation; **3-6×** more sample-efficient, **13/14** real ball-dispersal knockdowns vs SAC-DR's **6/14**.
- **[[2112.03149|DiDoR]]** — ==Distilled Domain Randomization==: trains N ==teacher policies== on fixed randomized-domain instances, then distills them into one ==student== via KL-divergence policy distillation; matches or beats Uniform-DR and ensemble baselines on Furuta-pendulum zero-shot transfer with **no** extra memory or inference-time cost.
- **[[2110.06192|Beyond-Pick-and-Place]]** — A three-stage recipe on the new **152-object** RGB-Stacking benchmark: state-based ==MPO== experts in sim, distilled to a vision policy via ==Interactive Imitation Learning== under heavy domain randomization, then refined with ==offline RL (CRR)==; zero-shot transfer hits **67.9%**, boosted to **81.6%** by the offline stage.
- **[[2003.02471|BayRn]]** — ==Bayesian Domain Randomization==: a ==bilevel== loop where ==Bayesian Optimization== over a ==Gaussian Process== of sparse real-world returns adapts the DR distribution, sidestepping the circular-dependency failure of explicit system-ID methods like SimOpt; higher median, lower variance than uniform DR on a real Furuta pendulum and Barrett WAM ball-in-cup task.
- **[[1910.04854|Imitation-of-Sequential]]** — Trains deep imitation-learning policies for sequential fabric smoothing from an algorithmic supervisor in a custom ==FEM simulator==, combining ==domain randomization== with ==DAgger==; RGBD policies zero-shot transfer to a real dVRK robot at **83.0%** coverage on the hardest fabric tier, beating RGB-only and depth-only variants.
- **[[1903.11774|DR Parameter Optimization]]** — Frames picking domain-randomization parameters φ as ==bilevel optimization==: ==Cross Entropy Method== optimizes φ in the outer loop while ==PPO== trains the inner policy; optimized φ lifts sim-to-sim transfer **102%** (Hopper) and **80%** (Walker) over hand-tuned defaults — DR distributions are themselves optimizable, not fixed by intuition.
- **[[1812.03201|Residual RL]]** — The foundational ==residual reinforcement learning== recipe: a hand-engineered feedback controller handles base motion while a ==TD3== residual policy learns contact-rich corrections; sim-pretrained residual solves real Sawyer block assembly in **under 1,000** real timesteps — ancestor of [[2602.23253|SPARR]]'s real-residual-on-sim-base pattern.
- **[[1710.06537|Dynamics Randomization]]** — Randomizes **95** simulated physical parameters (mass, friction, latency, observation noise) and trains an ==LSTM== policy via ==Recurrent DDPG + HER==; zero-shot real Fetch puck-pushing hits **0.89** success (vs sim's **0.91**), while a feedforward DR policy lags at **0.67** — memory beats memoryless robustness.
- **[[1703.06907|Domain Randomization]]** — The foundational ==domain randomization== recipe: randomizing textures, lighting, camera pose, and distractors in ==MuJoCo== trains a ==VGG-16== detector purely in sim to localize real-world object position; **1.5 cm** average error with zero real data — the historical root of every DR method in this file.

#### 3.2 Robust RL Foundations

Treat the sim-real gap as adversarial; train against the worst-case dynamics.

- **[[2607.20665|DGPPO]]** — Discrete Graph CBF-constrained PPO for ==safe multi-drone payload transport==, trained on a ==minimal 2D abstraction== + DR with a formal bridge from discrete-time DGCBF safety to continuous-time execution; **zero-shot** transfer to up to **six** physical drones across 10 scenarios, beyond the 3-5-drone training range.
- **[[2504.06585|Sim-to-Real-world-model]]** — A sim-to-real humanoid-locomotion framework injecting ==state-dependent MLP-generated perturbations into joint-torque space== with ==Denoising World Model Learning==, recasting domain randomization as a fixed functional perturbation; **54.9%** tracking error under unseen joint stiffness (vs 0.00 DR), zero-shot TOCABI under hardware mods.
- **[[2204.12581|RAMBO-RL]]** — An offline RL method framed as a ==two-player zero-sum game== — agent maximizes value, adversarial environment model minimizes it; ==ensemble of neural networks== for dynamics, updated adversarially via ==Model Gradient==; **highest total** D4RL [MuJoCo](https://mujoco.org) score; adversarial training of the *dynamics model itself* adds conservatism.
- **[[2510.14246|DR-RPO]]** — The first provably efficient *online* policy-optimization algorithm for robust MDPs with ==linear function approximation==; policy-regularized d-rectangular ==DRMDPs== / ==RRMDPs== with ==KL-divergence==, ==softmax policy updates==, ==UCB== bonuses; **Õ(d²H²/√K)** average suboptimality — matches value-based methods while supporting *stochastic* policies.
- **[[2602.13040|TCRL]]** — A *constrained*-RL defense against ==temporal-coupled adversarial perturbations==; a ==worst-case-perceived cost constraint== estimates safety costs without explicit adversarial-policy modeling, plus ==dual-constraint defense== (autocorrelation + entropy stability); **559-19,077%** safety-cost reduction, **8.36-34.76%** reward improvement under worst-case attacks.
- **[[2509.18648|SPiDR]]** — A zero-shot *safe* sim-to-real method that extends ==domain randomization== with a ==pessimistic cost penalty== from a ==dynamics-model ensemble== approximating the ==L1-Wasserstein== sim-real gap, solved as a ==CMDP==; transfers safely to a real race car + Unitree Go1 where vanilla DR violates constraints — DR with a formal safety margin.
- **[[2505.12462|Model-Free-Robust-Avg-Reward-RL]]** — A model-free ==Robust Halpern Iteration== for *average-reward* robust RL, using a ==quotient-space== formulation + ==K-order multi-level Monte-Carlo== bias-reduced oracle over ==KL / χ² / ℓp uncertainty sets==; first finite-sample **Õ(SAH²ε⁻²)** guarantee matching model-based bounds for steady-state robust transfer.

#### 3.3 Physics-Informed Policy Robustness

Bake physics priors *into* the policy via curriculum, reward shaping, or motion processing.

- **[[2607.12105|Physics-Priors In-Hand Rotation]]** — Bakes a ==grasp-quality prior== (grasp-Gramian reward) into RL and a ==contact-geometry prior== into ==anisotropic cylinder-aligned fingertips==, with two-stage ==RMA== + grasp cache + DR for proprioceptive zero-shot transfer; grasp-reward alone lifts SR **24% → 56%**, fingertip+reward reach **83%**, a **3.3×** gain under gravity variation.
- **[[2606.16513|Agile-Fall-Recovery]]** — An ==asymmetric actor-critic== with a recurrent GRU actor and a low-level ==INDI controller== recovers bidirectional-thrust quadrotors from ground-resting falls using only optical-flow + distance sensors, plus heavy Isaac-Lab DR; zero-shot real **10/10** indoor recoveries, robust to wind and payload.
- **[[2605.10063|EFGCL]]** — An external-force-guided curriculum for high-risk dynamic-motion learning (backflips, jumps) on legged robots, applying ==spotting-inspired external forces== with an ==adaptive curriculum== that decays assistance by success rate; acquires backflip/lateral-flip that PPO baselines *cannot learn at all*; **~2×** faster jumping, zero-shot transfer to real KLEIYN quadruped.
- **[[2604.24916|asRoBallet]]** — A reconfigurable humanoid ballbot built by ==subtractive reconfiguration== of a quadruped, whose critical ingredient is ==friction-aware [MuJoCo](https://mujoco.org)== modeling ==tribological phenomena== + actuator friction; with DR it achieves **zero-shot sim-to-real**, **100%** sim velocity-tracking, **0.05 m/s** real MAE, and recovers from **0.3 m** pushes.
- **[[2507.23445|GC-DR-RNN]]** — A physics-guided sim-to-real recipe for wide-gap mechanisms where a ==gain-regularization loss== ties the controller's ==input-output partial derivatives== to ==measured hardware gains==, plus ==parameter-conditioned DR== and a ==curriculum==-trained Elman RNN; on a **110:1**-gearbox balancer it kills the DR-RNN's **5 Hz** oscillation and matches real decay.
- **[[2506.12851|KungfuBot]]** — A recipe for *highly-dynamic* skills, zero-shot martial arts + dance on a real Unitree G1; a ==physics-based motion processing pipeline== filters untrackable mocap and ==adaptive motion tracking== adjusts the reward factor; with ==asymmetric actor-critic== + ==reference state initialization== + DR, per-body error **53.25 mm** vs **>233 mm** for OmniH2O/ExBody2.
- **[[2602.14174|Direction-Matters]]** — A contact-rich sim-to-real method training a sim policy to predict the ==normal force direction== as a *dynamics-invariant* signal, then deploying a ==force-aware admittance controller== with a hand-tuned magnitude; **91%** across four real tasks (vs best baseline **67%**), cutting both insufficient- and excessive-force failures.
- **[[2510.25405|Stress-Guided-RL]]** — A ==SAC==-based framework for gentle deformable/fragile manipulation that adds an ==internal-object-stress penalty== (top-10% + mean particle stress) to the reward, with human demos, ==rigid-to-soft curriculum==, and DR; zero-shot sim-to-real handles real tofu undamaged, **100%** foam pick-up at **10%** vs naive RL's **41.9%** water loss.
- **[[2503.01255|Impact-Static-Friction-Sim2Real]]** — A study identifying ==static friction== as an overlooked Sim2Real contributor for a Saturn Lite hexapod, with a ==static-friction-aware domain randomization== ("deception method" widening the range) over RMA teacher-student RL; **0.442 N·m** measured shank static friction (vs Go1's 0.0481), enabling real stable walking + stair climbing.
- **[[2311.13081|to-Fly-in]]** — An ==asymmetric actor-critic== quadrotor controller mapping states directly to motor RPM via a custom **1284M-steps/s** C++ simulator, with ==action-history== compensating motor delay + curriculum reward shaping; trains in **18s**/300K steps, zero-shot across **300+** real Crazyflie flights, beats PID/Geometric/INDI on agile trajectories.
- **[[2311.07499|Dynamic-Compliance-Tuning]]** — A contact-rich insertion recipe decoupling a ==Decision-Transformer Force Planner== (predicting motion + ==desired contact force==) from a ==Gain Tuner== that adjusts ==admittance stiffness== so the real robot tracks the planned force, both sim-only-trained; **70-100%** zero-shot on **0.02-0.05 mm** peg-hole, connectors, and deformable assembly.
- **[[2310.10509|Online Admittance Residual Learning]]** — Learns motion + initial ==admittance-control== gains offline via SAC + DR, then an ==online local-optimization== loop refines only the residual compliance parameters from real force feedback; **100%** peg-in-hole / **90%** pivoting on a real FANUC arm vs baselines' near-**0%** direct transfer.
- **[[2306.09852|AC-MPC]]** — An agile-flight recipe embedding a ==differentiable MPC solver== as the actor inside a ==PPO actor-critic==, with a ==Neural Cost Map== for the quadratic cost and ==MP Value Expansion== for the critic; zero-shot sim-to-real drone racing at **21 m/s**, **83.3%** vs **6.5%** under wind gusts, robust to **+27%** mass — bakes MPC structure into the policy.
- **[[2306.00286|MPC]]** — Extends ==Robust Tube MPC== imitation with ==parametric-sensitivity data augmentation== to nonlinear RTMPC (360° flips) alongside the linear tube case; **100%** success from **1** demonstration vs DAgger+DR's **100+**, zero-shot sim-to-real *and* lab-to-real, **180-280×** faster inference than the MPC expert.
- **[[2109.09910|Tube-MPC-Imitation]]** — Distills a ==Robust Tube MPC== expert via ==Sampling Augmentation==, drawing extra state-action pairs from the MPC's invariant tube to bake robustness into the imitation data itself; **100%** success from a *single* demonstration, zero-shot real-quadrotor wind rejection, and a **2-order-of-magnitude** latency cut versus the **55.3 ms** MPC expert.

#### 3.4 Vision-Aware Sim-to-Real

Close the *visual* gap explicitly via neural rendering, teacher-student distillation, or controller-aware system-id.

- **[[2607.14635|Action QFormer]]** — A ==query-based action-facing interface== mediating how action-loss gradients reshape a VLA's inherited representations via 16 ==instruction-conditioned learnable queries== that abstract control-relevant visual info; **0%** OOD instruction generation (vs up to 100%), **37.5-62.5%** zero-shot sim-to-real navigation SR vs **0-25%** baseline.
- **[[2607.11004|Real-to-Sim Affordance Planning]]** — Inverts the usual direction: an ==Image Conversion Module== restyles real ==RGBD== into sim-consistent images so a sim-trained affordance planner transfers, with ==object mask channels== and ==virtual camera motion== tracking occluded objects; **92%** GRASP accuracy, plans on **9/10** sim tasks, **5/5** trials on **6/10** real tasks.
- **[[2607.00148|3DPWM]]** — A ==Point Transformer V3==-based action-conditioned 3D world model trained on complete simulated point clouds, paired with a ==point cloud completion== module bridging real partial RGB-D observations at deployment; Chamfer L1 **0.080 → 0.009** on PickCube, MPPI closed-loop SR **35% → 85%**, zero-shot real-Franka picking without fine-tuning.
- **[[2512.01061|Sim-to-Real-Door]]** — A DoorMan ==teacher-student-bootstrap== recipe in NVIDIA Isaac Lab with PPO teacher + ==staged-reset exploration== + DAgger student + ==GRPO== partial-observability fine-tune; **83%** SR on diverse real doors (matches **80%** human teleoperator), **23.8%** faster than human experts.
- **[[2511.15200|VIRAL]]** — A visual sim-to-real framework at scale for humanoid loco-manipulation built on ==two-phase teacher-student== learning — a privileged RL teacher distilled into a vision student via DAgger + BC with **64-GPU** ==tiled rendering==; **54/59** cycles on real Unitree G1, matching expert teleop; ablating ==Reference State Initialization== drops success **95% → <10%**.
- **[[2604.11138|ViserDex]]** — A monocular-RGB dexterous-reorientation method that puts ==3D Gaussian Splatting== *in the simulation loop*, where ==pre-rasterization augmentation== applies DR to 3DGS attributes for diverse lighting + materials; **37.6** reorientations on real Allegro Hand, **~25** adversarial; single GPU, **1.6×** faster than tiled rendering.
- **[[2604.02523|Tune-to-Learn]]** — An MIT study of how *controller gains* shape sim-to-real, using ==Torque-to-Position Retargeting== to isolate gain effects; ==stiff/overdamped gains== yield *lowest* sysid errors but *worst* transfer, while for BC ==compliant overdamped gains== win despite higher training loss; RL reaches **99%+** under *any* regime — low sysid error does *not* track transfer.
- **[[2602.18071|EgoPush]]** — A constrained teacher-student recipe for egocentric mobile rearrangement: privileged PPO teacher masked to the student's ==virtual FOV== + ==Center-Gated Visibility==, distilled via a novel ==relational distillation loss==; **80%** zero-shot real TurtleBot3 SR (**70.70%** vs **0%** for an unconstrained-teacher ablation).
- **[[2602.15828|Dex4D]]** — A task-agnostic ==Anypose-to-Anypose== dexterous policy trained purely in sim (extensive DR + curriculum) with ==Paired Point Encoding== and a transformer ==action world model== student distilled via DAgger; **+22.5pp** real zero-shot SR over NovaFlow-CL on unseen tasks.
- **[[2512.09571|Robust-Drone-Racing]]** — A two-phase (soft-then-hard collision) RL racing policy with an ==adaptive noise-augmented curriculum== + asymmetric actor-critic + an ==L2C2== smoothness constraint; zero-shot real >**5 m/s** cluttered flight, **80%** SR under **2.1 m** gate-noise vs baselines' near-zero.
- **[[2512.04731|S2GS]]** — A ==Semantic 2D Gaussian Splatting== representation extracting ==object-centric, domain-invariant spatial features== via feature-level splatting + ==semantic retrieval== (CLIP/SAM) to filter background, fed to a ==Diffusion Policy==; **86.7%** Pick/Push and **80.0%** Stack zero-shot sim-to-real on unseen objects, **+2.46 dB** PSNR over 3DGS.
- **[[2510.14783|SkyDreamer]]** — A ==DreamerV3==-based (Informed Dreamer) model-based-RL drone-racing policy whose world model decodes to privileged state/params for interpretability, plus ==StochGAN== mask augmentation for visual sim-to-real; real champion-level **21 m/s**, **6g**, **100%** SR across 75 laps.
- **[[2505.00991|DexCtrl]]** — An adaptive-controller-learning framework that jointly predicts actions (==self-attention==) and ==controller parameters== (==cross-attention==) from trajectory history, with oracle-to-student sim distillation; params adapt to object properties (stiffer for heavier), beating fixed-tuning on real LEAP-hand in-hand rotation without retraining.
- **[[2504.04516|DexSinGrasp]]** — A unified RL policy integrating dexterous object ==singulation and grasping== via a continuous piece-wise singulation reward + ==clutter arrangement curriculum==, distilled to a point-cloud-based student; **98%** sim teacher, **61%** zero-shot real practical clutter — finger dexterity (DoF) is empirically essential.
- **[[2502.17894|FetchBot]]** — A zero-shot sim-to-real fetching policy for cluttered occluded scenes trained on ==UniVoxGen== (**1M** synthetic voxel scenes) via a dynamics-aware RL oracle, then distilled with a ==DepthAnything== sim-friendly depth rep + predicted ==3D semantic occupancy== to infer occlusions; **86.6%** suction / **93.3%** gripper real, lowest disturbance.
- **[[2502.14457|Watch-Less,-Feel-More]]** — A sim-to-real RL method for articulated objects that uses vision only for the initial grasp then switches to ==proprioception + interaction history==, with ==online policy distillation== inferring hidden object properties and ==learnable variable impedance==; **80%/84%** zero-shot on unseen doors/drawers, impedance lifting OpenDoor **40% → 80%**.
- **[[2411.01850|ManiBox]]** — Decouples visual perception from policy learning via ==YOLO-World bounding-box== intermediates: an Isaac-Lab teacher (PPO + DR) generates data, a masked-==RNN== student distills on boxes; **91.67%** sim, **70-100%** real zero-shot on Mobile ALOHA; data scales as spatial_volume^**0.35**.
- **[[2407.02274|DextrAH-G]]** — Integrates ==Geometric Fabrics== (collision-safe inductive bias) with a privileged PPO teacher over 140 objects, distilled via online ==DAgger== into a depth-based student; **99%** sim, **87%** real bin-packing over 256 attempts, **zero** hardware damage.
- **[[2406.12505|Demonstrating-Agile-Flight]]** — An ==asymmetric actor-critic== PPO policy mapping raw gate-segmentation pixels directly to collective-thrust + body-rate commands, no VIO/state estimation; zero-shot sim-to-real at **40 km/h**, **100%** success on a real Figure-8 drone-racing track.
- **[[2401.13362|TraKDis]]** — A ==Decision Transformer== knowledge-distillation framework transferring a state-privileged cloth-folding teacher to a vision-only student via weight-init + a pre-trained CNN state-estimator; **21.9%** over visual-RL baselines, **0.895** real UR5 cloth-folding, no fine-tuning.
- **[[2312.04670|Rapid-Motor-Adaptation]]** — Extends ==Rapid Motor Adaptation== to manipulator arms: a depth-CNN adapter infers pre-contact object properties plus learnable ==category/instance embeddings== for implicit geometry-awareness; **73.8%** YCB pick-place vs DR's **0.3%**, **90.5%** on unseen EGAD shapes.
- **[[2311.03622|TWIST-WM-Distill]]** — Trains a privileged state-based ==Dreamer world-model teacher== in sim, then distills its latent dynamics into a vision-based student over domain-randomized images via ==imagined-trajectory distillation==; beats Dreamer+DR and asymmetric SAC on the Distracting-Control-Suite and real Franka Block-Push/Lift.
- **[[2303.07026|Visual-Policy]]** — Distills a multi-camera teacher into a single-camera student under aggressive ==viewpoint randomization== + curriculum, minimizing teacher-student ==feature Euclidean distance==; student beats its own teacher under random views (**96.0%/81.7%** vs **68.7%/41.3%** cube/mug), **70-80%** zero-shot real Franka.
- **[[2201.12716|YODO]]** — A sim-trained ==NUNOCS== category-level 3D representation paired with model-free ==6DoF object tracking== (BundleTrack) for closed-loop category-level behavior cloning from one demo; **82.22%** battery assembly and **82.9%** gear insertion at 0.5mm tolerance, vs baselines' **<25%**.
- **[[2006.05768|Drone-Acrobatics]]** — Distills a privileged ==MPC== expert into a sensorimotor student via ==DAgger==, bridging the visual sim-to-real gap with ==input abstraction== (feature tracks instead of raw pixels, preprocessed IMU) rather than photorealism; zero-shot **3g** acrobatic maneuvers hit **100%** real success, while a raw-image policy fails entirely on unseen backgrounds.

#### 3.5 Humanoid & Legged Sim-to-Real

Whole-body and legged robots cross the gap via teacher-student distillation, staged RL curricula, and physics-driven retargeting — the depth-conditioned student observes the same modality it deploys with.

- **[[2607.15036|VOP-Nav]]** — An end-to-end RL quadruped-navigation policy whose ==Velocity Obstacle Perception Network== predicts a safe-velocity region from raw LiDAR, used as both policy input and a ==velocity-constraint reward==; zero-shot Go2 transfer hits **100%** SR indoors (15 trials), **12/15** outdoors, at **>3 m/s** under aggressive human interference.
- **[[2607.14643|NavCMPO]]** — A two-stage navigation policy pre-training a ==MeanFlow== trajectory generator (with ==Obstacle Proximity Prediction==) then RL fine-tuning, plus inference-time ==Critic-Guided Trajectory Refinement== for safety; cuts latency **85ms → 60ms**, **66.7%** zero-shot real-world SR on a Unitree Go2, beating NavDP's **56.7%**.
- **[[2607.11041|PAKE]]** — A hierarchical loco-manipulation controller where a ==Kinematic Normalizing Flow== learns the feasible-kinematics distribution so a high-level controller navigates its latent space for redundancy-aware EE references, executed by a low-level controller; real quadruped EE tracking hits **0.0449 m** / **0.1437 rad** error, **5.6×** the workspace of VBC.
- **[[2607.02205|Actuator Reality Shaping]]** — Shapes the physical actuator's closed-loop dynamics (==cascaded 2-DoF controller== + ==disturbance observer==) to match sim's idealized model, rather than adapting sim/policy to hardware; **96.3%** position / **99.1%** velocity deviation cut, zero-shot slope-climbing wheeled-legged + walking 22-DOF humanoid transfer.
- **[[2604.26504|HiPAN]]** — A two-level ==hierarchical RL== (goal-seeking + posture-adaptive locomotion) for quadruped navigation in unstructured 3D scenes via teacher-student + DR; ==Path-Guided Curriculum Learning== + intrinsic reward beat long-horizon myopia, posture commands enable confined-space traversal; **94.7%** SR / **83.6** SPL on Complex-2, on Unitree Go1 from depth only.
- **[[2508.10538|MLM]]** — A multi-task RL framework giving a quadruped-plus-arm one whole-body loco-manipulation policy via an ==asymmetric actor-critic== + ==Trajectory-Velocity Prediction== net (NAE foresight + memory-encoder velocity) and ==adaptive curriculum sampling==; with extensive DR it zero-shot transfers to a real quadruped at up to **85%** across teleop and autonomous tasks.
- **[[2502.12152|HUMANUP]]** — The *first learned* humanoid fall-recovery policy, a ==Two-stage RL curriculum==: Stage I discovery on simplified sim, Stage II deployable on full ==URDF== with **20,000** postures + diverse-terrain DR; Unitree G1 supine recovery **78.3%** / roll-over **98.3%** across **6 terrains** in **~6s** (vs **11s**); *separating discovery from refinement* is critical.
- **[[2503.20839|TAR]]** — A teacher-student quadruped recipe fixing rep misalignment via ==contrastive learning== — a ==triplet loss== with the teacher's next-state latent as anchor, a ==forward-dynamics== positive, task-informed negatives — and ==removes the teacher encoder post-sim==; **74% lower** OOD error than the teacher, zero-shot Go2 with **12 kg** + **150 N** pushes.
- **[[2212.07740|TERT]]** — A ==Terrain Transformer==: a GPT-like transformer student predicting teacher actions directly from proprioceptive history (no latent-vector estimation), trained two-stage (offline distillation → online correction) over heavy DR in Isaac Gym; on a real Unitree A1 it hits **100%** on sand pits and **60%** on stairs where the TCN-based RMA baseline scores **0%**.
- **[[2403.16967|VBC]]** — A ==hierarchical== visual whole-body-control framework for legged loco-manipulation: a low-level RL policy tracks EE + body-velocity goals in a height-invariant frame while a ==privileged teacher== is ==DAgger==-distilled into a segmented-depth visuomotor student; zero-shot real Unitree B1+Z1 grasping at 0.0/0.3/0.5 m heights vs non-hierarchical baseline's **0%**.
- **[[2107.04034|RMA]]** — The canonical ==Rapid Motor Adaptation== recipe: a base RL policy conditioned on a privileged ==extrinsics vector==, plus an adaptation module regressing that vector online from proprioceptive history alone (100 Hz base / 10 Hz adapter); a Unitree A1 crosses sand, mud, and slippery floors with **12 kg** payload, zero real-world fine-tuning.
- **[[2510.07094|Universal-Quadruped-Sampling]]** — A universal locomotion controller (==asymmetric actor-critic== + morphology estimator) studying how to sample ==morphology and joint PD gains==, with a novel ==adaptive particle-filter curriculum==; enables zero-shot deployment on real ANYmal (**0.09-0.11 m/s** RMSE) without unsafe PD gains where baselines fail.
- **[[2507.04039|ROLT]]** — A ==Robust Locomotion Transformer== whose architecture targets OOD dynamic + perceptual gaps via ==Body Tokenization== (action token enabling cross-limb knowledge transfer for fault tolerance) and ==Consistent Dropout==; zero-shot real Unitree Go1 across weakened limbs, box-dragging, and roller-skates, beating RMA.
- **[[2507.07825|LoadAdapt]]** — A teacher-student RL framework for quadruped locomotion under *unknown dynamic loads* on rough terrain, with ==load-characteristics modeling== (mass, velocity, friction), a ==Load Estimator== inferring load from proprioception, and a ==load-stabilization reward==; zero-shot sim-to-real on Unitree Go2 carrying **4-6 kg** shifting loads, near a direct-load oracle.
- **[[2407.04224|PA-LOCO]]** — A perturbation-adaptive quadruped recipe with a ==teacher-student multi-encoder== decoupling external-force / terrain / state privileged info, plus a ==residual policy network== and ==perturbation curriculum==; **90%** recovery from a **4.6 kg** lateral impact in **0.75 s** (vs **43%** / **1.98 s**) — decoupling force features enables targeted recovery.
- **[[2207.10821|Lower-Fidelity-Sim2Real]]** — A counter-intuitive finding for legged visual navigation: training a high-level policy in ==lower-fidelity kinematic sim== (teleport-to-pose, no low-level physics) over a manufacturer ==low-level controller== beats high-fidelity dynamic sim by enabling **10×** more training steps; **100%** real Spot point-goal (vs **40-67%**) — speed-over-fidelity.

#### 3.6 Domain Adaptation & Continual Transfer

Align the source/target distributions or keep adapting after deployment — without joint data access or catastrophic forgetting.

- **[[2607.05665|Morphological Similarity Transfer Learning]]** — A self-supervised ==autoencoder== aligns latent dynamics of morphologically similar soft underwater robots via ==Maximum Mean Discrepancy== domain alignment + next-state prediction; zero-shot (no target labels) velocity prediction cuts RMSE **~40%** over an unadapted source-only model on Micro-CAT.
- **[[2607.02037|Cross-Platform ASV RL]]** — A ==teacher-student== RL recipe where a ==GRU-based adapter== infers unknown vessel dynamics online from interaction history, trained on a lightweight 3-DoF Fossen model with wide domain randomization; zero-shot cross-platform transfer cuts real position error **58%** vs. non-adaptive generalist PPO, matching platform-specific MPC in ~30 min training.
- **[[2607.01410|BIFROST]]** — Learns a shared ==GRU history encoder== latent space via ==Generalized Bisimulation Metric== alignment (reward prediction + latent dynamics + ==Wasserstein-1== cross-domain loss), unifying perceptual and dynamics gaps for zero-shot POMDP policy transfer; **0.50** cross-simulator navigation SR vs. BDA's **0.34** under compounded visual+dynamics shift.
- **[[2607.00666|Domain Arithmetic]]** — ==DART== extracts a reusable ==domain vector== via weight-arithmetic subtraction of task-specific update-vectors from a single target demo, refined by ==subspace filtering + scaling==, then adds it to a base VLA's weights for one-shot adaptation; **+38.4pp** over zero-shot on real UR10e across viewpoint and cross-embodiment shifts.
- **[[2606.15469|Context-ODE]]** — A ==context-aware Neural ODE== dynamics model with a two-phase ==privileged-encoder + history-based adaptive module== (1D-CNN) feeding ==MPPI== control, plus online fine-tuning; **3×** wind-disturbance robustness beyond DATT's training range, outperforms RMA on real Fanuc CoM-shift pushing.
- **[[2606.06218|TAM-Torque-Adaptation]]** — A policy-agnostic ==torque-interface residual module== corrects torque commands via ==multi-robot sim pretraining== then per-robot fine-tune, with an async ==History Encoder== driving a 1 kHz ==Torque Adaptor==; real Franka pushing **47.6%→76.2%**, BC flipping **50.0%→72.0%**, **>60%** EE-RMSE cut, zero-shot to Google Robot (**1.05°** vs **4.69°**).
- **[[2605.23733|Any2Any]]** — A cross-*embodiment* transfer framework for pre-trained humanoid whole-body-tracking policies: ==kinematic alignment== (coupling matrices remap obs+action spaces) then ==LoRA== dynamic adaptation reuses motor priors across LimX Oli/Luna + Unitree G1/H1 at only **~1%** of from-scratch compute and data, with comparable-or-better tracking.
- **[[2604.13645|CFG-ADDA]]** — A mechanistic analysis of ==sim-and-real co-training== for ==diffusion policies== isolating two drivers — ==representation alignment== (~50% of loss variance) and ==importance reweighting== (~20%) — then **CFG-ADDA** (==adversarial alignment== + ==domain conditioning== + ==negative classifier-free guidance==); **~74% (21/30)** real success.
- **[[2602.18025|Cross-Embodiment-Offline-RL]]** — An offline-RL method exploiting *heterogeneous, suboptimal* multi-robot data: morphology-agnostic ==URMA== + ==IQL==, plus ==Embodiment Grouping== (==Fused Gromov-Wasserstein== clustering + group-wise actor updates) to kill inter-robot gradient conflicts; **+33.99%** over standard cross-embodiment IQL on 70%-suboptimal data (r=**0.815**).
- **[[2602.07227|Cerebellar]]** — An ==inference-time cerebellar-inspired residual controller== augmenting a *frozen* RL policy for fault recovery via ==phase-aligned references==, ==microzone partitioning==, ==dual eligibility traces==, and a ==reward-trend meta-controller==; recovers from unseen actuator/dynamics faults on MuJoCo locomotion + PandaReach, staying inactive when fault-free.
- **[[2512.00453|Conformal-Expert-Query]]** — ==CRSAIL== queries an expert only when a K-NN ==state-novelty score== exceeds a ==conformal-prediction== calibrated threshold, post-hoc in batch with no real-time takeover; matches expert reward using **3.4%** of DAgger's queries, a distribution-free sibling to [[2410.08852|Conformalized-Interactive-Imitation]]'s drift-focused conformal use.
- **[[2509.18631|Sim-Real-OT-Co-Training]]** — A generalist co-training framework over abundant sim + sparse real demos where ==Unbalanced Optimal Transport== aligns the *joint* observation-action distribution across domains, with ==Dynamic-Time-Warping== sampling; **0.73** image / **0.77** point-cloud real SR, generalizing to novel textures (BoxInBin **0.7**, Stack **0.4**) unseen in the demos.
- **[[2508.21065|Learning-on-the-Fly]]** — An online real-time adaptation framework using ==differentiable simulation== in which a ==hybrid dynamics model== couples a low-fidelity analytical model with a learned residual net and ==BPTT== gives first-order policy updates; cuts hovering error **81%** vs L1-MPC / **55%** vs DATT; real quadrotors adapt to mass + wind in **3 steps** (**4.5 s**).
- **[[2508.12252|Robot-Trains-Robot]]** — A *latent* dynamics-calibration method replacing explicit param calibration: a compliant arm teacher supplies ==F/T reward signals== + autonomous resets, then a three-stage pipeline refines a ==FiLM-conditioned dynamics latent== to fit real dynamics; humanoid doubles walking speed in **20 min**, learns swing-up in **15 min**.
- **[[2506.08460|MOBODY]]** — A model-based *off-dynamics* offline-RL method for mismatched dynamics that learns ==target dynamics== (shared state encoder + separate source/target action encoders), rolls out the policy for fake transitions, and optimizes with ==target-Q-weighted behavior cloning==; **+44%** over the best baseline across 32 MuJoCo gravity/friction-shift tasks.
- **[[2503.22634|Sim-and-Real-Cotraining-Study]]** — An empirical study of ==sim-and-real cotraining== for ==diffusion policies== on planar pushing from pixels, sweeping real-data sizes, sim scales, and mixing ratios on a KUKA iiwa; cotraining gives **2-7×** real gains (**10/20 → 19/20** at |D_R|=50), physical accuracy dominates contact tasks, and direct data-mixing beats pretrain-then-finetune.
- **[[2503.10949|SCDA]]** — A safe *continual* domain-adaptation framework for post-transfer drift where DR pretraining + ==PCRPO== safe RL + ==Elastic Weight Consolidation== let a deployed policy keep adapting to real drift without catastrophic forgetting; on real grasping it lifts SR **20% → 60%** while holding **zero** safety violations — where reward-only adaptation turns unsafe.
- **[[2407.13771|Training-Free-Model-Merging-MTDA]]** — A training-free merge building one generalist from many single-target ==STDA== adapters with *no* joint data access, via ==linear mode connectivity== (parameter averaging + ==Gaussian BatchNorm-statistic merging==). Matches combined-data training on multi-target driving segmentation and *outperforms* prior consistency-training MTDA.
- **[[2602.20220|Sim-to-Online-RL]]** — An empirical study (100+ runs, 3 platforms) of sim-trained policies fine-tuned ==online via off-policy SAC== on real robots, isolating what stabilizes it: ==retaining sim + past real data==, ==warm-start buffers==, and ==asymmetric actor-critic updates== (delayed actor, smaller LR) prevent the downward spiral across manipulation, locomotion, navigation.
- **[[2602.12628|RL-Co]]** — A ==RL-based sim-real co-training== framework for VLAs: ==SFT== on real + sim demos initializes the policy, then ==RL in simulation== refined by ==ongoing real-data SFT== prevents domain drift; real SR rises to **64.0%** (OpenVLA) and **66.2%** (π0.5), with stronger OOD robustness and data efficiency.
- **[[2601.16212|Point-Bridge]]** — A cross-domain framework distilling observations into ==domain-agnostic 3D point representations== (==VLM== scene filtering + ==Foundation Stereo== depth) trained on synthetic data with a ==multi-task transformer policy==; **39-44%** zero-shot sim-to-real gain, **97%** held-out-object SR, and **+30%** from 45 real co-train demos.
- **[[2412.04323|GRAM]]** — A deep-RL framework unifying *adaptive* ID and *robust* OOD generalization in one policy via an ==Epistemic Neural Network== that gauges deployment uncertainty and blends an adaptive latent with a fixed ==robust latent feature==, trained by standard + ==adversarial RL==; **0.92/0.79/0.58** ID/near/far-OOD return, **100%** on a real Go2 under **9 kg** on slippery ground.
- **[[2410.08852|Conformalized-Interactive-Imitation]]** — ==ConformalDAgger== extends online ==conformal prediction== (Intermittent Quantile Tracking) to intermittent labels, using calibrated uncertainty to trigger expert queries under expert shift; queries jump **20%→60%**, lower miscoverage than EnsembleDAgger, on a real 7-DoF sponging task.
- **[[2201.13248|SafeAPT]]** — A *safe* sim-to-real adaptation framework generating a ==diverse policy repertoire== via ==MAP-Elites== under varied sim dynamics, then online-learning ==GP reward + safety models== (sim as prior) and selecting policies by an ==Expected-Safe-Improvement== acquisition; **zero** safety violations on a real Kuka hockey task, finding high-reward policies in minutes.
- **[[2007.04309|Self-Supervised-Deploy-Adapt]]** — A reward-free deployment-time adaptation (PAD) sharing a feature extractor between the policy and a ==self-supervised head== (==inverse-dynamics== or rotation prediction), updating the visual encoder online with no extrinsic reward; generalizes in **31/36** environments and **+24%** on real reach/push under disco-light + patterned backgrounds.
- **[[1909.00889|DRPC]]** — Extends domain randomization to *domain generalization* for segmentation: ==image-to-image-translation stylization== plus ==Pyramid Consistency== (across-domain + within-image) losses train on GTA/SYNTHIA alone; **36.11%** mIoU on unseen Cityscapes rivals target-data-requiring domain-adaptation methods like CyCADA.
- **[[1906.04452|Sim2Real]]** — Combines ==State Representation Learning==, ==policy distillation== of sequential-task teacher policies into one student, and ==domain randomization== to mitigate catastrophic forgetting across continually-learned tasks; the distilled student matches individual teachers' near-max reward, inferring task identity from visual cues alone.
- **[[1702.02453|UP-OSI]]** — A ==Universal Policy== conditioned on dynamics parameters μ (==TRPO==), paired with an ==Online System Identification== net inferring μ from a short state-action history; matches a true-parameter oracle and *outperforms* it **100%** outside the training range on Cart-Pole — precursor to [[2107.04034|RMA]]'s privileged-extrinsics-plus-adapter recipe.
- **[[1608.02192|Playing for Data]]** — The foundational game-engine synthetic-data recipe: ==detouring== intercepts DirectX calls in Grand Theft Auto V, with a ==custom shader== pass for ==semi-automatic pixel-accurate labeling==; **24,966** images labeled in 49 hours (**514-771×** faster than manual), CamVid mIoU **+3.9pp** — ancestor of [[1909.00889|DRPC]]'s GTA/SYNTHIA generalization.

#### 3.7 Gradient-Based Controller Auto-Tuning

Close the gap by tuning the controller's own parameters on real data via analytical gradients — sidestepping both manual sysid and full policy retraining.

- **[[2507.10914|M-GAPS]]** — A ==non-episodic, model-based online policy optimization== algorithm computing ==surrogate-cost gradients== in O(1)/step over a ==geometric controller== with ==log-reparameterized gains==; on real hardware it reaches near-optimal in **8-12 s**, cuts Ackermann-car error **>5×** in **~10 s**, and adapts to wind + **60%** added mass — single-trajectory, not episodic.
- **[[2505.24068|DiffCoTune]]** — A gradient-based ==co-tuning== framework *simultaneously* adapting a ==differentiable simulator== and a ==differentiable controller==, with a robust ==Split-Alternate== strategy refining sim params from real rollouts then tuning the controller; **+60%** quadruped sim-to-sim tracking and a real **34 cm** biped jump where controller-only tuning falls.
- **[[2212.03194|DiffTune+]]** — A ==hyperparameter-free== extension of DiffTune turning its ==sensitivity-propagation== gradients into optimal update rules — a ==Gauss-Newton== step and a ==line-search== learning rate via ==first-order Taylor expansions== of the closed-loop loss; Line-Search beats hand-tuned gradient descent on Dubin's-car + quadrotor tuning, removing the manual LR knob.
- **[[2209.10021|DiffTune]]** — The foundational ==auto-differentiation controller tuner== framing tuning as ==parameter optimization== via ==sensitivity propagation== (gradients straight from real sensor data) with ==L1 adaptive control== for unbiased gradients; **3.5×** lower real quadrotor tracking RMSE within a **10-trial** budget — gradient-based tuning that runs on hardware, not just sim.

#### 3.8 Jump-Start & Attenuated Teacher Guidance

Blend a classical or foundation-model teacher transiently during early training, then attenuate it to zero, leaving a standalone RL policy that inherits the teacher's inductive bias without inheriting its runtime cost or performance ceiling.

- **[[2604.13733|Jump-Starting]]** — ==VLAJS== jump-starts PPO with sparse, temporally-discretized ==VLA teacher== deltas via a ==directional action-consistency loss==, reward-scheduled to zero; **+50%** sample efficiency, zero-shot real Franka **70-80%** SR, insensitive to teacher quality.
- **[[2603.12960|Attenuated-Residual-Racing]]** — ==α-RPO== linearly attenuates a Stanley-controller base policy into a standalone residual network via a PPO ==synchronization trick==; zero-shot real Roboracer **+12%** lap time, **3.5 ms** embedded inference, no base policy at deployment.
- **[[2510.24461|Surrogate-Gradients-for]]** — ==TD3BC+JSRL== jump-starts an SNN quadrotor controller with a privileged ANN guide phased out over rollouts, plus adaptive ==surrogate-gradient== slope scheduling; **+600pt** over vanilla TD3, zero-shot real Crazyflie flight at **9.7×10⁻⁵ mJ**/inference.

**Policy-Side — Decision Matrix**

| Need | Recommendation |
|---|---|
| Industrial-default dexterous reorientation (DR baseline) | [[2210.13702\|DeXtreme]] — VADR doubles real-world transfer (**27.8** vs **14.8**) |
| Train from imperfect demo priors at industrial assembly scale | [[2603.15956\|ExpertGen]] — diffusion prior + DSRL + DAgger; **90.5%** avg AutoMate |
| Real-world residual learning without human supervision | [[2602.23253\|SPARR]] — Pattern A+C hybrid; **95-100%** AutoMate, **+74.5%** unseen NIST |
| Full-stack dexterous humanoid recipe (Fourier GR-1) | [[2502.20396\|Humanoid-Sim2Real-Dex]] — autotuned modeling + contact stickers; **80%** box-lift |
| Whole-body humanoid VLA with latent-intermediate alignment | [[2506.13751\|LeVERB]] — CVAE verb-vector bridges 10Hz VLA ↔ 50Hz controller; **58.5%** mean SR |
| Adversarial robust offline RL against worst-case dynamics | [[2204.12581\|RAMBO-RL]] — two-player zero-sum dynamics ensemble; top D4RL [MuJoCo](https://mujoco.org) score |
| Provably efficient online robust RL with linear function approx | [[2510.14246\|DR-RPO]] — softmax policy + KL-regularized DRMDP; **Õ(d²H²/√K)** suboptimality |
| Defend constrained RL against temporally-coupled attacks | [[2602.13040\|TCRL]] — dual-constraint defense; **559-19,077%** safety-cost reduction |
| Learn previously-unlearnable dynamic skills (flips, jumps) | [[2605.10063\|EFGCL]] — spotting-inspired external forces + adaptive curriculum |
| Bridge underactuated dynamics with friction-aware physics | [[2604.24916\|asRoBallet]] — friction-aware [MuJoCo](https://mujoco.org) + DR; zero-shot ballbot, **0.05 m/s** MAE |
| Low-noise humanoid locomotion across diverse footwear | [[2604.23702\|QuietWalk]] — PINN GRF predictor in reward; **7.17 dBA** noise reduction |
| Highly-dynamic humanoid skills (martial arts, dance) | [[2506.12851\|KungfuBot]] — physics-feasible motion processing + adaptive tracking; **53.25 mm** error |
| Visual sim-to-real at scale for loco-manipulation | [[2511.15200\|VIRAL]] — two-phase teacher-student + 64-GPU tiled rendering; **54/59** real G1 |
| Visual sim-to-real on a single consumer GPU | [[2604.11138\|ViserDex]] — 3DGS in the sim loop + pre-rasterization aug; **37.6** reorientations |
| Question whether stiff/compliant gains improve transfer | [[2604.02523\|Tune-to-Learn]] — compliant overdamped gains beat stiff for BC; sysid ≠ transfer |
| Zero-shot force-aware dexterous in-hand rotation | [[2601.02778\|Force-Based-Sim2Real]] — distance-field tactile + current-to-torque cal; **25.1** rotations w/ tactile |
| Quadruped navigation in unstructured 3D from depth-only | [[2604.26504\|HiPAN]] — hierarchical RL + path-guided curriculum; **94.7%** Complex-2 |
| MoCap-to-humanoid retargeting with sparse/dense goal support | [[2603.03279\|ULTRA]] — multimodal controller + availability masking; **73%** dense-tracking G1 |

^dm-3

> [!star] Key Papers
> - [[2210.13702|DeXtreme]] — Foundational VADR result: automatic DR doubles real-world transfer (**27.8** vs **14.8** reorientations); the canonical industrial sim-to-real recipe
> - [[2511.15200|VIRAL]] — Visual sim-to-real at scale for humanoid loco-manipulation; **54/59** real Unitree G1 success matching expert human teleop; RSI is critical
> - [[2506.12851|KungfuBot]] — Physics-feasible motion processing + adaptive tracking; **53.25 mm** error vs **>233 mm** baselines; first to zero-shot transfer highly-dynamic skills
> - [[2604.24916|asRoBallet]] — Friction-aware [MuJoCo](https://mujoco.org) + RL closes sim2real gap for underactuated dynamics; **zero-shot** ballbot whole-body control with **0.05 m/s** real-world MAE

^key-papers-3

> [!tip] Domain Randomization is the Default — But Has Limits
> Every paper in this section uses DR, but [[2604.11674|AffordSim]] showed DR alone only lifts real-world success from **17%** to **27%** on affordance-demanding tasks — fine-grained semantic transfer still fails. DR works for *dynamics* gaps ([[2210.13702|DeXtreme]], [[2506.12851|KungfuBot]]) but is *brittle* for *semantic* gaps (manipulating novel categories). Combine DR with neural rendering ([[2604.11138|ViserDex]]) or learned simulators ([[2310.06114|UniSim]]) when the visual gap dominates. Cross-reference [[11_Whole-Body-and-Locomotion-Control#1. Whole-Body Control & Coordination]] for where DR-on-dynamics carries whole-body transfer outright. The RL-side view of the same robustness machinery — what the policy optimizer can and cannot absorb — is [[03_Imitation-Learning-and-RL#4. RL Algorithms, Efficiency & Policy Representations]].

^insight-3

> [!success] The Modern Policy-Side Recipe
> ==Auto domain randomization== + ==teacher-student distillation== + ==reference state initialization== + ==system identification== + ==privileged-info asymmetric actor-critic== — proven across [[2210.13702|DeXtreme]], [[2511.15200|VIRAL]], [[2506.12851|KungfuBot]], and [[2603.15956|ExpertGen]]. Pick a subset based on which gap (dynamics, visual, kinematic) dominates your deployment.

---

### 4. Real2Sim2Real Loops & Digital Twins

Reverse the direction: reconstruct the *deployment* scene as a high-fidelity interactive simulator, train the policy *against the twin*, then execute on the real robot. Eliminates the visual long tail because the simulator is *grounded* in the deployment environment from the start.

#### 4.1 Video/Scan → Exact-Twin Reconstruction

Reconstruct the *deployment* scene or object as a faithful, aligned twin from real video, scans, or multi-view capture: the simulator substrate is a replica of the specific scene the policy will face.

- **[[2607.06699|RoboSnap]]** — One-shot real-to-sim: VLM+SAM3+SAM3D physical layer + Gaussian-splat visual layer, refined via alternating ==SDF-physics optimization==; falling-object rate **0.381 → 0.103**, **100%** DROID trajectory replay (vs RoLA's **40%**), real π0 success **29.3% → 42.7%**, **r=0.887** sim-real correlation.
- **[[2606.16202|EgoPhys]]** — A framework constructing deformable-object physical digital twins from single ==egocentric RGB-only video== via a ==codebook-based physics prior== (material prototypes predicting dense spring-stiffness fields) for zero-shot stiffness on unseen objects; **0.015** Chamfer / **0.025** track error, **77.6%** config-error cut in sim-to-real xArm6 manipulation.
- **[[2606.08828|Video2Sim2Real]]** — A full-stack pipeline acquiring dexterous skills from a single human video via an autonomous ==digital twin== + ==object-centric keyframe refinement==, then a ==decoupled sim-to-real== split — IL for keyframe-pose geometry + residual RL for local finger physics; **91.4%** sim / **95.7%** real avg across 7 tasks vs pure IL/RL's 3-**45.7%**.
- **[[2605.26115|TriSplat]]** — A feed-forward ==oriented-triangle primitives== reconstructor from sparse unposed images, geometry-anchored and surface-sharpened; **24.69 dB** PSNR on RE10K, **33–249×** faster than Gaussian baselines, meshes load directly into Isaac Sim for sim-ready robot scenes.
- **[[2604.05621|FunRec]]** — A training-free pipeline reconstructing *functional* articulated digital twins from egocentric RGB-D interaction video via VLM ==fragment classification==, ==articulation-aware motion clustering==, and joint part-pose + ==kinematic-parameter== optimization in canonical frames; **~5°** axis error, **77.9** mIoU, **0.7 cm** Chamfer — simulation-ready twins.
- **[[2603.13825|Explicit-WM-Manipulation]]** — A zero-shot open-world manipulation framework via on-demand digital twins; ==open-set segmentation== (Grounded-SAM) + ==grasp pose prediction== (AnyGrasp) → ==digital twin== (Hunyuan 3D 2.0) + ==two-stage pose alignment== ([[2304.07193|DINOv2]] + RANSAC/ICP) → physics sampling; **6/9** at **≥75%**; alignment lifts mug-handling **27% → 91%**.
- **[[2512.14696|CRISP]]** — A real-to-sim pipeline turning monocular human-scene-interaction video into sim-ready assets via ==normal-based planar-primitive fitting== + ==contact-guided scene completion== (InteractVLM infers occluded surfaces) + an RL motion-tracking validity check; **93.1%** real-to-sim success (vs VideoMimic **44.8%**) at **23K** FPS (**43%** faster RL throughput).
- **[[2504.03597|Real-is-Sim]]** — A digital twin made the policy's *sole interface*, mirrored by the real robot: an ==Embodied Gaussians== twin syncs via **60 Hz** RGB while the policy (==Conditional Flow Matching==) reads/writes *only* the sim; 30+30 demos lift state-based PushT **57% → 80%**, virtual cameras reach **82%** — unlike [[2503.17973|PhysTwin]]/[[2511.07416|PhysWorld]].
- **[[2502.01536|VR-Robo]]** — A ==Real-to-Sim-to-Real== framework reconstructing scenes into ==3D Gaussian Splatting== + mesh hybrids in Isaac Sim (3DGS rendering, mesh collision) for training legged visual navigation/locomotion via PPO + domain randomization; **100%** sim cone-reaching, zero-shot real Go2/Galaxea R1 across 6 indoor scenes (93–100% SR).
- **[[2503.17973|PhysTwin]]** — A reconstruction of ==physics-informed interactive digital twins== of *deformable* objects from videos; multi-stage optimization jointly recovers geometry, physical properties, and appearance via ==spring-mass models== + ==generative shape priors== + ==Gaussian splats==; real-time sim drives motion planning — lifts videos into simulatable physics.
- **[[2407.03245|TieBot]]** — A Real-to-Sim-to-Real pipeline for bimanual tie-knotting: ==Hierarchical Feature Matching== (local LoFTR + global oriented keypoints + physics priors) estimates a deformable mesh from RGB-D demo video, then a teacher-student policy grasps/pulls toward mesh subgoals; **50%** real tie-knotting, **70%** unseen towel-folding.
- **[[2404.09833|Video2Game]]** — A real2sim pipeline turning a single video into a real-time browser-compatible interactive 3D environment with physics; enhanced ==Instant-NGP== distilled to ==game-engine-compatible mesh + neural texture map==, decomposed into entities with ==rigid-body physics==; **>100 FPS** browser rendering; monocular 2D priors regularize NeRF from sparse video.
- **[[2403.03949|RialTo]]** — A ==Real-to-sim-to-real pipeline== building task-specific digital twins of articulated scenes; ==inverse distillation== transfers real imitation policies into sim, then ==PPO+IL== + ==teacher-student distillation== refine them; **91%** object-pose, **77%** distractors, **75%** disturbances (**2.5×** vs imitation); target twins give **90%** vs generic **10%**.
- **[[2606.17520|GASE]]** — A ==3D Gaussian Splatting== automated reconstruction system using panoramic multi-view streams and a ==2D-domain object-scene decomposition== for accurate masks + background inpainting; decouples static collision-mesh background from manipulable foreground objects, reaching **>10%** higher mIoU and a **<10%** sim-to-real manipulation gap.
- **[[2601.03200|3DGS-Digital-Twin]]** — A ==3DGS==-based digital-twin pipeline (==InstantSplat==) with ==multi-view semantic fusion== + three-stage ==geometric cleaning== (filtering, connectivity pruning, watertight Alpha-Shape meshing) into planning-ready collision geometry; **229 s** reconstruction (**5×** faster than NeRF), **90%** real zero-shot pick-and-place, zero collisions.
- **[[2602.02402|SoMA-Sim]]** — A real-to-sim *neural* simulator for soft-body manipulation representing objects as ==hierarchical 3D Gaussian Splats== whose dynamics are driven by environmental + robot-induced ==forces== via neural interaction modules, with ==multi-resolution training== for long-horizon stability; **+20%** resim accuracy and PSNR **33.51** vs PhysTwin's **28.77**.
- **[[2511.20348|Material-GS]]** — A camera-only ==3D Gaussian Splatting== digital-twin pipeline with ==monocular material extraction== (RMSNet + FastSAM) projected to mesh surfaces as ==PBR textures== for physics-based sensor simulation; matches LiDAR-camera-fusion reflectivity accuracy (MAE **10.05** vs **10.14**) from cameras alone.
- **[[2510.20813|GSWorld]]** — A closed-loop photorealistic suite integrating ==3D Gaussian Splatting== with physics engines via a portable ==Gaussian Scene Description File (GSDF)== and a marker-based real-to-sim reconstruction pipeline; **68%/52%** zero-shot sim2real, and ==automated DAgger== in sim lifts Place-Box **68% → 76%**.
- **[[2502.08645|Re3Sim]]** — A real-to-sim-to-real pipeline reconstructing scenes with ==hybrid rendering== (ray-traced foreground meshes + ==3DGS== background) and marker/ICP alignment for large-scale data generation; **>58%** avg real zero-shot SR with a strong **0.924** sim-real Pearson correlation, reconstructing scenes in under a minute.
- **[[2502.08643|IKER]]** — A real-to-sim-to-real framework (IKER) where ==VLMs generate iterative keypoint reward== functions, a ==scene transfer== (BundleSDF mesh + FoundationPose) builds faithful sim, and ==PPO + DR== trains transferable policies; enables multi-step tasks, disturbance recovery, on-the-fly replanning (**0.7** Shoe-Place vs **0.3**).
- **[[2603.05108|GaussTwin]]** — A real-time digital twin unifying rigid + deformable objects via an extended ==Position-Based Dynamics== model (==discrete Cosserat rod== for DLOs) coupled to ==3D Gaussian Splatting== in a ==prediction-correction loop== with segmentation-mask correction forces; **>0.75** IoU rope tracking and **1.2 cm** / **0.01 rad** model-based push planning.
- **[[2510.15352|GaussGym]]** — An open-source real-to-sim framework fusing ==3D Gaussian Splatting== with ==vectorized IsaacGym physics== so locomotion policies learn from RGB pixels at **>100,000** steps/s, with an ==asymmetric actor-critic== over ==DINOv2== + proprioception and an auxiliary voxel head; zero-shot to a real Unitree A1, RGB avoids a penalty region depth-only policies miss.
- **[[2411.11839|RoboGSim]]** — A Real2Sim2Real simulator pairing ==3D Gaussian Splatting== with ==Isaac Sim== physics + MDH kinematics, a ==Digital Twins Builder== aligning real/3DGS/sim, and a Synthesizer + closed-loop Evaluator; **PSNR 31.3** novel-pose synthesis, **10×** faster data gen, and RoboGSim-trained policies hit **90%** in novel scenes vs real-data's **60%**.
- **[[2409.20291|RL-GSBridge]]** — A Real2Sim2Real method reconstructing scenes as ==3D Gaussian Splatting== with a novel ==soft mesh binding== (Gaussians float along mesh normals) and ==physics-driven GS editing== synced to a Pybullet sim for zero-shot RL grasping transfer; only **6.6%** average SR drop sim-to-real (vs an **80%** RL-sim baseline drop).
- **[[2409.10161|SplatSim]]** — A zero-shot Sim2Real RGB-manipulation method replacing mesh rendering with ==segmented 3D Gaussian Splats== transformed by physics-derived poses, training a ==Diffusion Policy== with image augmentation; **86.25%** average across four contact-rich tasks (vs **97.5%** Real2Real), cutting data effort from **20.5 h** to **0-3 h**.

#### 4.2 Generative Digital Cousins & Data Engines

Start from minimal real input, often a single image or video, and generate the rest: digital-cousin scene variations, AIGC 3D assets, and synthesized demonstrations that trade exact-replica fidelity for diversity and data scale.

- **[[2607.04880|PRISM]]** — From a single RGB-D image + language instruction, builds ==digital cousin== scenes (VLM + Grounded-SAM object retrieval) and synthesizes demonstrations via ==TAMP== with ==motion-aware grasp selection==, then applies ==trajectory-preserving visual randomization==; autonomously generates **400** demos/task in **2-7h**, real-world success up to **100%**.
- **[[2606.28276|SimFoundry]]** — A modular real-to-sim pipeline (VLM + 3D-generative Extraction→Generation→Augmentation) turning one RGB video into an interactive twin plus unlimited ==digital cousins== (object/scene/task variations); **r = 0.911** sim-real correlation, **+17-40%** sim-to-real SR from cousin augmentation.
- **[[2606.12604|EgoEngine]]** — A pipeline turning egocentric human videos into high-fidelity dexterous robot demos via an object-centric ==digital twin==, a visual branch that inpaints humans out and renders a robot in, and ==adaptive multi-solver (Replay/MPC/RL)== retargeting of hand motions; **83%** TACO, **90%** Aria, and zero-shot real beats teleoperation (**60%** vs **25%** on Hammer).
- **[[2511.07416|PhysWorld]]** — A digital-twin pipeline chaining ==Task-conditioned video generation== → ==geometry-aligned 4D reconstruction== → physical twin → ==object-centric residual RL== inside the twin; **82%** avg success across **10** real-world tasks, **+15 pp** over RIGVid; cuts grasping failures **18% → 3%**; the explicit physical world model is what makes generated video actionable.
- **[[2412.14957|DREMA]]** — A ==compositional world model== building physically-grounded digital twins via object-centric ==Gaussian Splatting== + open-vocab tracking + a ==PyBullet physics engine==, generating ==equivariant-transform== demonstrations verified before training; real-world SR nearly doubles **31.7% → 62.9%**, **+9.1%** single-task / **+13.1%** multi-task in low-data sim.
- **[[2603.14010|URDF-Anything+]]** — An end-to-end ==autoregressive diffusion== framework generating simulation-ready URDF (==part geometry== + ==kinematic structure==) from a single RGB image via a shared ==Diffusion Transformer== latent; Part IoU **0.879** and zero-shot **100%/90%** laptop/drawer sim-to-real in a ==Real-Follow-Sim== paradigm.
- **[[2510.10637|High]]** — A real2sim2real data generator (RoboSimGS) with hybrid scene representation (==3DGS== backgrounds + explicit interactive meshes) where ==MLLMs (GPT-4o)== auto-infer articulation and physical material properties from renders; zero-shot transfer across eight real tasks and **>10,000** demos/day on one GPU.
- **[[2410.07408|Digital-Cousins-ACDC]]** — A real2sim pipeline (ACDC) auto-generating ==digital cousins== — diverse sim scenes preserving geometric + semantic affordances of one real RGB image *without* an exact replica — via ==GPT-4 / GroundedSAM / DINOv2==; cousins give *guided* DR, **90%** real door-opening vs a digital twin's **25%** — relaxing exact-replica fidelity buys robustness.
- **[[2409.02920|RoboTwin]]** — A dual-arm benchmark + real-to-sim data generator pairing teleoperated with synthetic data, building ==AIGC 3D twins from a single 2D image== and using ==GPT-4V/GPT-4== to auto-generate expert pose sequences + trajectory scripts; on DP3, Empty-Cup-Place rises **10% → 96%** and Block-Handover **50% → 98%** at 50 demos (early RoboTwin 2.0).
- **[[2412.01770|CASHER]]** — A ==Real-to-Sim-to-Real== pipeline scaling robot data super-linearly with sub-linear human effort via ==crowdsourced 3D digital twins== and an ==amortized data-collection== loop where a self-improving generalist generates demos; **62%** zero-shot on 8 unseen real kitchens (**R²=0.92** sim-real), and unsupervised fine-tuning adds **+55%**.

#### 4.3 Differentiable Real2Sim Calibration

Replace manual system-id with gradient descent on simulator parameters.

- **[[2607.20653|PhysCoRe]]** — A hybrid deformable-dynamics model coupling a differentiable ==MLS-MPM== simulator with a ==Material from Motion== module (graph U-Net inferring per-particle elasticity/plasticity from RGB-D) and a ==Residual from Dynamics== velocity-correction; Chamfer Distance cut **43.7%** (elastic) / **30.5%** (elastoplastic) vs [[2503.17973|PhysTwin]], **11.4s** inference.
- **[[2606.24552|Sim-in-Loop-Cloth]]** — A closed-loop ==real-to-sim-to-real== cloth pipeline pairing the FLASH deformable simulator with an ==RGB-native state estimator== (DINOv2 + canonical tokens) and a prior-guided ==MPPI== controller refining an offline base policy via parallel sim rollouts; **9/10** single-arm / **8/10** dual-arm folding, **2.33 mm²** recon MSE at **7.4 ms**.
- **[[2604.27367|DOT-Sim]]** — A differentiable optical-tactile simulator calibrated to real soft sensors where a ==Material Point Method== models gel deformation, ==differentiable physics== calibrates material params, and a neural ==residual image== adds optical fidelity; **PSNR 30.48** (**+17.34%**) and zero-shot **90.5%** indenter, **96.6%** tumor detection, **0.896 mm** trajectory error.
- **[[2603.22039|RAFL]]** — A soft-robot sim-to-real method augmenting a ==differentiable simulator== with a learned ==element-level residual-acceleration field== — an ==MLP== over ==local deformation/velocity gradients== with ==rotational equivariance== — trained ==end-to-end through the sim==; cuts real error **6.571 → 3.536 mm** where sysid shows negative transfer.
- **[[2603.01151|D-REX]]** — A ==differentiable real-to-sim-to-real engine== that reconstructs ==Gaussian Splats== and identifies ==object mass== via differentiable physics (minimizing real-vs-sim pushing-trajectory discrepancy), then trains mass-conditioned force-aware grasping from human videos; mass error **4.8-12.0%**, **86%** real grasping (vs DexGraspNet 2.0 **76%**), beating DR on OOD mass.
- **[[2602.03623|Physics-Informed-DLO]]** — ==SPiD== fits a differentiable extended ==mass-spring model== (a novel analytical bending-damping term) to real rope trajectories via gradient-based system-ID + curriculum horizon, then trains a self-supervised controller with DR and ==self-supervised DAgger== OOD-correction; RMSE **0.0810→0.0591 m** real, **F1 0.898** markerless perception.
- **[[2506.04120|Splatting-Physical-Scenes]]** — An end-to-end ==differentiable== real-to-sim pipeline introducing ==SplatMesh== (triangle meshes + surface-constrained 3D Gaussians) that jointly optimizes geometry, camera extrinsics, and robot joint angles via differentiable rendering + ==MuJoCo MJX== physics from imperfect data; CD cut **18.92 → 7.35 mm** on real ALOHA 2.
- **[[2504.16693|PIN-WM]]** — A Real2Sim2Real method (PIN-WM) learning a ==physics-informed world model== of 3D rigid-body dynamics + appearance end-to-end from few-shot video via ==differentiable physics (LCP)== + ==2D Gaussian Splatting==, then trains policies on ==physics-aware digital cousins==; **97%/83%** sim and **75%/65%** real push/flip from a single sysid trajectory.
- **[[2503.10118|RSR-Loop]]** — An iterative ==Real-Sim-Real loop== that tunes ==differentiable simulation parameters== (MuJoCo MJX ==L_physical== loss) and the policy together, with an ==Adaptive InfoGap Loss== mitigating data-collection bias; KL divergence between real and sim block-pushing trajectories drops from **16.3/36.3** to **<1** by the 4th iteration.
- **[[2412.00259|One-Shot-Real-to-Sim]]** — A one-shot method identifying geometry, appearance, and physics of novel rigid objects from a single interaction via an ==end-to-end differentiable simulator + renderer== over a hybrid ==Shape-as-Points== + grid representation converted to an explicit mesh; **64%** lower Chamfer + positional error, and infers occluded geometry to be physically plausible.
- **[[2411.00554|DPSI]]** — A ==Differentiable Physics-based System Identification== framework inferring elastoplastic material params (Young's modulus, yield stress, friction) from noisy 3D point clouds by minimizing an ==Earth Mover's Distance== loss through ==MLS-MPM== ==von Mises plasticity== in ==DiffTaiChi==; converges in **100 updates** (~**10 min**) from one datapoint.
- **[[2204.03139|DiffCloud]]** — An end-to-end ==differentiable== real-to-sim pipeline inferring deformable-object physics (stiffness, mass) from real point-cloud sequences via ==differentiable mesh physics (DiffSim)== + ==differentiable point-cloud sampling== minimizing a ==unidirectional Chamfer== loss; **~10 min**/trajectory (an order of magnitude faster), robust to occlusion + partial views.
- **[[2104.02646|gradSim]]** — The foundational ==differentiable multiphysics simulation + rendering== framework unifying physics and a ==differentiable rasterizer== into one graph so gradients flow ==from pixels to physical parameters== via the discrete adjoint method; **9e-5** mass-estimation error from video with no 3D supervision, and trains visuomotor cloth control from pixel-wise loss alone.

#### 4.4 World-Model-Driven Online Adaptation

Treat the sim-real gap as an OOD shift the world model detects, then fine-tune online.

- **[[2603.04029|Self-Adapting-RL]]** — An online continual-RL framework with world-model feedback; built on ==[[2301.04104|DreamerV3]]==, ==Observation== + ==Reward Prediction Residuals== trigger online world-model + policy fine-tuning; Walker adapts to actuator damage in **10,000 steps** (**2 min**); F1Tenth adapts to *both* sim-real gap *and* friction drop in **10,000 real steps** (**8 min**).

#### 4.5 Compositional Sim-Real Environments

Use sim as a safety filter, not a training source.

- **[[2604.05484|CoEnv]]** — A multi-agent-collaboration framework via ==compositional environment== unifying scene reconstruction with a physics simulator; ==VLM-based hierarchical planner== decomposes tasks; ==collision-aware sim-to-real transfer== verifies swept collision volumes before execution; **49%** across **5** real multi-agent benchmarks; sim is the *safety filter*, not training source.

#### 4.6 Learned & Bayesian Real2Sim Calibration

Calibrate the simulator to real dynamics *without* differentiable physics — via learned dynamics models, Bayesian parameter inference, or iterative sim-param refinement.

- **[[2607.24079|Renormalization for Robotics]]** — Borrows renormalization from field theory: stop chasing physical accuracy, fit ==effective parameters== absorbing omitted physics and finite sim resolution via a ==four-step procedure==; simulated derivative gain and inertia must rise by **δt·K_P** and **δt·K_D**, and **5** hydrodynamic coefficients fit from **2** trajectories.
- **[[2607.23268|Sling2Sim2Real]]** — ==One-shot elastic system identification== from a single non-destructive ==visuo-haptic== probe (sling point cloud + end-effector force), fitting five elasticity parameters by ==Differential Evolution== global search then ==multi-start CMA-ES==; zero-shot landing error **7.17 cm** soft / **19.00 cm** stiff bands, calibration loss **−72.5%** vs best baseline.
- **[[2607.11734|NeuralActuator]]** — A ==Transformer==-based actuator model learning history-dependent mappings from telemetry to simulator-equivalent ==generalized-effort surrogates== and external forces, trained end-to-end in a differentiable simulator via pose-based supervision; **5.5×** better force estimation than classical current-to-torque baselines, **+10pp** real lift-and-hold success.
- **[[2606.30268|ConCent]]** — A real-to-sim-to-real framework optimizing simulated ==contact geometry== (evolutionary search) to match a single demo's local contact dynamics, extracting a ==contact event sequence== as an automatic RL reward, plus a ==Virtual Collision Penalty== for scalable parallel training; **80.0%** real tight-clearance insertion (vs **20%** without geometry optimization).
- **[[2605.22597|MoSA-Continuum]]** — A real-to-sim continuum-dynamics calibrator augmenting an ==isotropic constitutive prior== with learned ==bounded residual stress== + an ==implicit heterogeneity field==, supervised by ==motion-constrained== higher-order losses from dynamic ==3DGS==; lowest Chamfer **13.5**, **31.35** real PSNR, lifting elastic-object manipulation **42% → 68%**.
- **[[2604.11090|Simulator-Adaptation-Loco]]** — A motion-capture-free simulator adaptation for legged sim-to-real matching proprioceptive observation + action distributions via a ==1D-marginal Wasserstein== cost, optimizing static params, a ==state-dependent action-delta==, or a ==residual actuator model== with ==CMA-ES==; cuts Unitree Go2 drift up to **80%** from **<5 min** of hardware data.
- **[[2512.19390|TwinAligner]]** — A Real2Sim2Real system with a ==Mesh-GS digital twin== (3DGS rendering + SDF/mesh collision) and ==visual-dynamic alignment== fitting viewpoint + rigid physics (friction, mass, CoM, controller) via ==gradient-free optimization== robust to rendering error; PSNR **38.03**, ADD **1.39 cm**, strong zero-shot transfer plus trustworthy cross-environment evaluation.
- **[[2510.11689|Phys2Real]]** — A ==real-to-sim-to-real== method with 3D reconstruction + ==physics-conditioned== policy + uncertainty-aware transfer; **100%** weighted T-block push (vs Domain-Randomization 79.17%) — physics conditioning beats blind randomization.
- **[[2510.08556|DexNDM]]** — A reality-gap closer for dexterous in-hand rotation: sim ==oracle policies== distilled to a ==generalist==, a ==joint-wise neural dynamics model== (per-joint factorization) fit on autonomous ==Chaos-Box== real data, then a ==residual policy== correcting it; rotates high-aspect-ratio (up to **5.33**) and **2-3 cm** objects under diverse wrist poses, beating AnyRotate.
- **[[2509.06342|Towards-bridging-the-gap]]** — A systematic legged sim-to-real (PACE) aligning sim physics via a ==minimal physically-interpretable parameter set== (inertia, damping, friction, bias, delay) fit with ==CMA-ES== from ~**20 s** of encoder-only data, plus a ==PMSM energy reward==; **32%** lower ANYMAL D Cost-of-Transport and zero-shot transfer *without* domain randomization.
- **[[2506.15680|Particle-Grid-Neural-Dynamics]]** — A hybrid ==Lagrangian-Eulerian particle-grid== framework learning deformable-object dynamics directly from real RGB-D video (SAM + CoTracker tracks), bypassing sim-to-real material-ID; outperforms MPM/GNN baselines on rollout accuracy at **4.8 ms**/forward-pass, enabling real-time MPC manipulation of cloth and rope.
- **[[2505.14266|Sampling-Based-SysID]]** — A sampling-based ==system identification== framework (SPI-Active) for legged sim2real that minimizes real-vs-sim trajectory discrepancy, then adds ==Fisher-Information-guided active exploration== to collect informative trajectories — *no* differentiable physics or torque sensors; **42-63%** policy improvement on real Go1 quadruped and H1 humanoid.
- **[[2503.15481|Play-Piano-Real-World]]** — A dexterous piano-playing recipe (xArm7 + Allegro Hand) whose ==iterative Sim2Real2Sim workflow== refines sim params from real data and adds ==key fences== so simulated contact matches real, plus ==domain randomization==; the fences cut the Sim2Real gap **11.2% → 6.8%** and reach **0.881** real F1 across five songs (vs **0.946** in sim).
- **[[2502.18615|Real2Sim2Real-DLO]]** — An object-centric Real2Sim2Real framework for deformable-linear-object manipulation using ==BayesSim== (==RKHS-net== embeddings) to infer multimodal posteriors of DLO params (length, Young's modulus) from real trajectories, then guiding ==object-specific DR== for PPO; DTW analysis confirms behavioral adaptation to each DLO's softness.
- **[[2502.10894|UAN]]** — An ==Unsupervised Actuator Net== bridging the *actuation* gap for athletic loco-manipulation: it predicts corrective torques to close the sim-real gap *without* torque sensors, paired with a two-stage WBC pre-train→fine-tune pipeline; the real Unitree B2+arm throws objects **~20 m**, lifts **8 kg**, drags a **113 N** cart — sim-to-real of the actuator model.
- **[[2502.01143|ASAP]]** — A sim-real physics alignment for *agile* humanoid whole-body skills: pre-train motion-tracking on retargeted human video, learn a ==delta-action model== on real data that residually corrects nominal sim actions, then fine-tune inside the *aligned* simulator; on Unitree G1 reduces tracking error up to **52.7%** — closes unmodeled dynamics beyond SysID/DR.
- **[[2410.20357|Dynamics-as-Prompts]]** — An online system-id method (CAPTURE) reframing calibration as ==in-context learning==: a ==causal transformer== predicts ==simulation parameters== from ==multi-episode interaction histories==, trained on ==randomized-binary-search== data, with an env-conditioned RL policy; ~**20%** better real air-hockey trajectory error, converging in ~**4** iterations.
- **[[2409.17992|LoopSR]]** — A lifelong legged-policy adaptation loop pretraining in sim then using limited real trajectories to infer a ==latent representation== (transformer autoencoder + contrastive loss) that updates sim params into a ==digital twin== for continual retraining; on a real Unitree A1, Stair-Up rises to **100%** SR (vs **70%**) with faster, smoother gaits.
- **[[2404.12308|ASID]]** — A "sim-real-sim-real" pipeline training a ==Fisher-information== exploration policy in sim to collect one informative real episode, then refining sim params with ==black-box CEM== and training a zero-shot task policy in the calibrated sim; **6/9** rod-balancing and **7/10** shuffleboard on a real Franka from a single exploration episode where DR fails.

**Real2Sim2Real — Decision Matrix**

| Need | Recommendation |
|---|---|
| Generate physical digital twin from a single task-conditioned video | [[2511.07416\|PhysWorld]] — video → 4D recon → physical twin → residual RL; **82%** real across 10 tasks |
| Make the sim the policy's **sole** interface, real robot mirrors sim | [[2504.03597\|Real-is-Sim]] — Embodied Gaussians + 60Hz visual sync; eliminates sim-real gap from policy POV |
| Deformable-object twin from video (cloth, rope, soft objects) | [[2503.17973\|PhysTwin]] — spring-mass + Gaussian splats; real-time interactive sim |
| Browser-deployable interactive 3D environment from one video | [[2404.09833\|Video2Game]] — Instant-NGP + neural texture + rigid-body physics; **>100 FPS** browser |
| Calibrate optical tactile sim to real sensor via gradients | [[2604.27367\|DOT-Sim]] — differentiable MPM + residual rendering; **96.6%** zero-shot tumor detection |
| Online continual RL adapting to sim-real gap as OOD shift | [[2603.04029\|Self-Adapting-RL]] — [[2301.04104\|DreamerV3]] residual triggers; **2 min** Walker, **8 min** F1Tenth |
| Zero-shot open-world manipulation via on-demand twins | [[2603.13825\|Explicit-WM-Manipulation]] — Grounded-SAM + Hunyuan + [[2304.07193\|DINOv2]] two-stage alignment; **27→91%** mug-handling |
| Multi-agent collaboration with sim as safety filter | [[2604.05484\|CoEnv]] — compositional env + collision-aware verification; **49%** across 5 multi-agent benchmarks |

^dm-4

> [!star] Key Papers
> - [[2503.17973|PhysTwin]] — Physics-informed deformable digital twins from videos; real-time interactive sim + motion planning integration
> - [[2511.07416|PhysWorld]] — **82%** real-world success across 10 tasks via task-conditioned video → physical digital twin → object-centric residual RL; explicit physics is what makes generated video actionable
> - [[2504.03597|Real-is-Sim]] — Embodied-Gaussians digital twin as the policy's **sole interface**; the real robot mirrors the sim instead of vice-versa, eliminating the sim-real gap from the policy's perspective; +23pp PushT with 30+30 demos
> - [[2404.09833|Video2Game]] — Single video → **100+ FPS** browser-compatible interactive environment with rigid-body physics; foundational real2sim pipeline
> - [[2604.27367|DOT-Sim]] — Differentiable MPM + residual rendering for optical tactile sensors; **96.6%** tumor detection zero-shot

^key-papers-4

> [!tip] When Real2Sim2Real Wins
> Digital twins win when your *deployment scene matters most* — a specific robot, a specific workspace, a specific deformable target. They lose when you need *broad generalization across scenes*, where learned simulators ([[2310.06114|UniSim]], [[2501.03575|Cosmos]]) or large-scale procedural generation ([[2603.16861|MolmoBot]]) scale better. The decision: how variable is your deployment environment? Cross-reference [[09_Manipulation-Skill-Learning#7. Demonstration, Data-Generation & Cross-Embodiment Transfer]] for how twin-generated demonstrations feed manipulation policies downstream.

^insight-4

---

## Part C — Evaluation, Integration & Open Problems

*Measuring the gap, combining the three strategies, and what is still unsolved.*

### 5. Evaluation & Reality-Gap Measurement

You cannot optimize what you cannot measure. The reality-gap evaluation stack went from absent (pre-2024) to the determining factor for whether a sim-to-real claim is publishable (2026).

A third axis of this landscape — *interactive world-model evaluation*, making heterogeneous interactive simulators comparable on the same footing — remains a still-separate stack (§7.1), exemplified by [[2604.21686|WorldMark]], which unifies action mapping across interactive I2V world models at **ρ > 0.9** with human judgments (detailed at its canonical home in [[02_Dataset-Benchmark-Environment#11. World Model Benchmarks]]).

#### 5.1 Sim-Real Correlation Benchmarks

Quantify how well sim predicts real — the prerequisite for any publishable sim-to-real claim.

- **[[2606.10366|Sim-Real-VLA-Eval]]** — A correlation recipe quantifying when sim predicts real VLA performance, sweeping 3 benchmarks × 5 policies under matched ==vision/language/layout/behavior perturbations== on DROID; REALM wins (**ρ=0.700**, **MMRV=0.030**), and ==simulator-based post-training== lifts ranking **ρ 0.700→0.875** at a 10-demo data optimum.
- **[[2605.06311|VISER]]** — A correlation benchmark pushing realism with ==ray tracing== and ==physically-based rendering (PBR)== materials, while an ==MLLM-driven asset pipeline== generates **>1,000** 3D assets *without* baked-lighting artifacts; **r = 0.92** avg Pearson sim-real correlation; ==specular highlights== and ==contact shadows== are the *load-bearing cues* current VLAs depend on.
- **[[2512.16881|PolaRiS]]** — A scalable real-to-sim correlation benchmark for *generalist* policies whose automated ==2D Gaussian Splatting== pipeline rebuilds interactive scenes from short monocular scans + ==TRELLIS== objects + a policy-agnostic co-train; **r = 0.9** avg Pearson sim-real (up to **0.98** vs RoboArena), beating Libero-Score and Ctrl-World, at **<20 min** human effort per scene.
- **[[2512.10675|Veo-Robotics]]** — A ==generative digital twin== fine-tuning ==Veo2== for action-conditioning + multi-view consistency, synthesizing OOD/safety-critical variations to evaluate VLA policies; predicts policy ranking at **MMRV 0.03** / **Pearson 0.88** with real success, **0.91** on background-change OOD — a learned twin substituting for physical eval rollouts.
- **[[2511.04665|Real-to-Sim-GS]]** — A *deformable-object* sim-real correlation framework (where [[2405.05941|SimplerEnv]] / [[2605.06311|VISER]] lose fidelity) coupling ==3D Gaussian Splatting== + soft-body twins ([[2503.17973|PhysTwin]]); optimizes params with ==color alignment== + **NVIDIA Warp** physics; **r > 0.9** across plush, rope, T-block (**r=0.915**) vs **IsaacLab r=0.649**.
- **[[2405.05941|SimplerEnv]]** — The first benchmark for *reliable* sim-real correlation across Google Robot + BridgeData V2; it closes the control gap via ==system identification==, the visual gap via ==green screening== + ==texture baking==; Pearson **r > 0.85** Google Robot, **r = 0.890** BridgeData V2; introduces ==Mean Maximum Rank Violation (MMRV)== — whether sim correctly *ranks* policies.
- **[[2111.00765|VSDR]]** — A DR policy-selection score (Validate-on-Sim, Detect-on-Real) multiplying ==sim validation== over held-out DR environments with a real-world ==OOD score== from ==GMMs== fit to simulated feature activations, ranking which policy will transfer from as few as **64** real observations; **86-100%** Spearman ranking accuracy, beating OPC/SoftOPC.
- **[[1912.06321|Sim2Real-Predictivity]]** — The foundational predictivity study introducing the ==Sim2Real Correlation Coefficient (SRCC)== for visual navigation via a ==Habitat-PyRobot bridge==; default settings score a low SRCC **0.18** because agents ==slide== through obstacles, but disabling sliding + actuation noise lifts SRCC to **0.844** — fidelity is *predictivity*, not realism.

#### 5.2 Diagnostic Benchmarks for Specific Sim-to-Real Failures

Decompose the gap into specific failure modes that single-metric benchmarks miss.

- **[[2506.18088|RoboTwin-2.0]]** — An automated expert-data generator via ==MLLMs== + ==closed-loop simulation-in-the-loop feedback==, applying ==domain randomization== across **5** dimensions (clutter, textures, lighting, heights, paraphrases) + ==embodiment-aware grasp adaptation==; **+24.4%** real-world few-shot, **+21.0%** zero-shot unseen-background generalization.
- **[[2607.04434|RoboDojo]]** — A unified sim-and-real benchmark: 42 simulation tasks across five capability dimensions (Generalization/Memory/Precision/Long-Horizon/Open) + 18 real tasks on three embodiments via standardized ==RoboDojo-RealEval==; best policy scores just **8.80%** sim / **12.8%** real success, exposing action jitter and unsafe contacts invisible to simulation alone.
- **[[2606.31993|OopsieVerse]]** — ==DAMAGESIM==, a simulator-agnostic mechanical/thermal/fluid ==object-health== damage model, exposes a task-completion-vs-safety gap invisible to standard SR (GR00T: **92%** complete, **4%** safe) and transfers: damage-aware policies cut real Franka unsafe behaviors **60%** sim-to-real.
- **[[2606.18097|WireCraft]]** — A unified Isaac Lab ==DLO simulation benchmark== for industrial assembly integrating an ==articulated== (high-throughput) and ==FEM deformable== (high-fidelity) physics model with a shared sim-to-real protocol; privileged RL hits **>92%** insertion but vision policies show a large ==reach-insert gap== and sim-only zero-shot fails — diagnosing the DLO gap.
- **[[2604.10856|BridgeSim]]** — A cross-simulator closed-loop evaluation suite that decomposes the OL-CL gap into ==Observational Domain Shift== + ==Objective Mismatch==; a training-free ==Test-Time Adaptation== combines a ==flow-matching calibrator==, ==truncated Q-value estimator==, and ==adaptive replan==; **+19.1** Driving Score with [[2305.14992|RAP]]; *scaling OL does not improve CL*.
- **[[2510.23571|RobotArena-Infinity]]** — A scalable benchmarking system via ==real-to-sim translation==: single-view robot video → re-executable sim with reconstructed objects + calibrated dynamics, scored by a ==dual VLM-guided + human-preference== protocol (Bradley-Terry over **8,500+** judgments) and perturbed along background/color/pose; six open VLAs drop sharply under OOD shift.
- **[[2501.16389|Sim2Real-Encoder-Eval]]** — An *offline* framework diagnosing which pretrained vision encoder will transfer, via two metrics: ==Domain Invariance Score== (sim↔real embedding alignment) + ==Action Score== (task-relevant features); encoders pretrained on manipulation data (MCR) top both, beating generic backbones — pick the encoder before training the policy, not after.
- **[[2606.18594|Action-Space-Bench]]** — A systematic benchmark of four ==action-space representations== (pose/joint × increment/velocity) for vision-based ==PPO== manipulation, evaluating zero-shot sim-to-real on a real Franka; ==joint velocity== gives **100%** real picking with low jerk where Cartesian pose-velocity fails entirely — sim SR does not predict real transfer.
- **[[2603.22876|Grounding-Sim-to-Real]]** — A factorized empirical study (10,000+ real trials, OpenVLA-OFT on RoboTwin 2.0) isolating which sim-to-real factors matter for dexterous VLA generalization; ==spatial domain randomization== (camera pose, table height) dominates appearance, ==frame-wise== beats episode-wise DR, and RL + comprehensive DR lifts real SR **5.6% → 42.8%**.
- **[[2602.00678|RoboGauge]]** — A predictive assessment suite measuring ==sim-to-real transferability== via ==sim-to-sim metrics== in MuJoCo across terrains/difficulties/DR, paired with a ==MoE== proprioception-only locomotion policy; RoboGauge tracks real ground truth (error **0.0873**) better than IsaacGym metrics, enabling **4.01 m/s** robust real Go2 locomotion.
- **[[2508.11117|Robot-Policy-Eval-Sim2Real]]** — A benchmarking framework for generalist-policy sim-to-real transferability using ==high-fidelity IsaacLab== sim, a four-level ==task-complexity taxonomy==, ==five perturbations== (lighting, texture, camera pose, placement), and graded metrics including explicit sim-to-real matching; finds policies highly vulnerable to minor perturbations.
- **[[2505.17966|Single-View-Mesh-for-Robotics]]** — An empirical study defining ==five robotics desiderata== (<2 mm Chamfer, no collisions, <5° stability, occlusion robustness, <2 s) and testing 12 single-view mesh-reconstruction models on YCB-Video + Aria; most exceed **5 mm** error with colliding, unstable meshes and **~50%** grasp transfer — digital twins are not yet robotics-ready.
- **[[2503.11007|DARPA]]** — DARPA's ==TIAMAT== program bets on "abstract-to-real transfer" from diverse low-fidelity sims + ==semantic anchors== (logic, scene graphs) instead of high-fidelity chasing, run via an **APSU** quadruped sim-to-sim→sim-to-real challenge scored on adaptation time and semantic accuracy.
- **[[2312.03673|Action-Space-Sim-to-Real-Study]]** — A large-scale empirical study (**250+** PPO agents, **13** action-space variants) on a Franka of how action space shapes sim-to-real; ==joint-velocity== (and delta) gives lowest offline trajectory error + highest real accuracy + fewest constraint violations, while ==joint-torque== is unsafe for contact and multi-step deltas widen the gap.

#### 5.3 Sim-Real Estimation as a Statistical Problem

Reframe sim-to-real as variance reduction across a portfolio of biased simulators.

- **[[2604.24018|Sim2Real-Betting]]** — A ==Sequential betting framework== where sims inform wagers via a ==bet-weighted estimator==; ==Cover's universal portfolio== with ==Kelly-style bet sizes== combines diverse sims and ==double betting== tolerates bias; **70-100%** win rates vs Monte Carlo, domain-randomized sim banks converging fastest; sim-to-real is *variance reduction*, not *fidelity*.
- **[[2512.05024|Simulator-Fidelity-Quantile-Curves]]** — A ==model-free== framework profiling the sim-to-real gap as a *distribution*, constructing a ==calibrated quantile curve== of per-scenario ==pseudo-discrepancy== over rigorous confidence sets with high-probability upper-bound guarantees; treats the gap as a random variable rather than a scalar, validated on LLM simulators.
- **[[2506.20553|Sim2Val]]** — A variance-reduced real-metric estimator applying classical ==control variates== over paired real+surrogate and abundant surrogate-only samples, with a learned ==Metric Correlator Function== boosting weak correlation; **up to 82.9%** variance reduction and **51-58%** fewer real samples for the same confidence across driving + quadruped.
- **[[2503.05696|MFPG]]** — A ==Multi-Fidelity Policy Gradients== framework treating cheap sim as a low-fidelity ==control variate== for scarce high-fidelity data, with a ==policy reparameterization trick== correlating cross-fidelity trajectories for an unbiased variance-reduced gradient; beats high-fidelity-only in **8/8** dynamics-gap scenarios, robust to anti-correlated low-fidelity rewards.
- **[[2206.05165|MFMCRL]]** — A ==multifidelity Monte-Carlo RL== framework cutting high-fidelity (real) sample cost by using correlated low-fidelity (sim) returns as a ==control variate== over the value estimate, with an estimated optimal coefficient; provably cuts high-fidelity samples by **(1 − ρ²)** — an early case for stacking cheap biased sims against ground truth.

**Evaluation — Decision Matrix**

| Need | Recommendation |
|---|---|
| Reliable rigid-object sim-real correlation + policy *ranking* | [[2405.05941\|SimplerEnv]] — Pearson **r > 0.85**, **MMRV** for rank-violation diagnostics |
| Pinpoint *which visual cues* drive sim-real correlation | [[2605.06311\|VISER]] — ray-traced PBR; **r = 0.92**; identifies specular highlights / contact shadows |
| Deformable-object (cloth, rope, soft) sim-real correlation | [[2511.04665\|Real-to-Sim-GS]] — 3DGS + [[2503.17973\|PhysTwin]]; **r > 0.9** across plush / rope / T-block |
| Decompose OL-CL gap into observation shift vs Q-mismatch | [[2604.10856\|BridgeSim]] — flow-matching TTA + truncated Q + adaptive replan; **+19.1 DS** |
| Automated expert-data generation with DR across 5 dims | [[2506.18088\|RoboTwin-2.0]] — MLLM + closed-loop sim-in-the-loop; **+24.4%** few-shot real |
| Unified embodied-AI capability evaluation across 22+ benchmarks | [[2509.15273\|Embodied-Arena]] — 7 capabilities × 25 dimensions; LLM-driven anti-overfitting data gen |
| Combine predictions from multiple imperfect simulators | [[2604.24018\|Sim2Real-Betting]] — Cover's universal portfolio + Kelly bets; **70-100%** win rate vs MC |
| Evaluate *interactive* I2V world models against each other | [[2604.21686\|WorldMark]] — unified action mapping + 500 cases; **ρ > 0.9** with human judgments |

^dm-5

> [!star] Key Papers
> - [[2405.05941|SimplerEnv]] — First reliable sim-real correlation benchmark (**r > 0.85**, **r = 0.890**); introduces MMRV ranking metric; foundational evaluation paper
> - [[2605.06311|VISER]] — **r = 0.92** sim-real correlation via ray-traced PBR + MLLM asset pipeline; identifies specular highlights and contact shadows as load-bearing visual cues
> - [[2511.04665|Real-to-Sim-GS]] — **r > 0.9** sim-real correlation on *deformable* tasks (plush, rope, T-block) via 3DGS + [[2503.17973|PhysTwin]]; the soft-body counterpart to [[2405.05941|SimplerEnv]]/[[2605.06311|VISER]]'s rigid-object work; identifies color alignment + physics optimization as jointly required
> - [[2604.10856|BridgeSim]] — Decomposes OL-CL gap into observational shift + objective mismatch; **+19.1 DS** via training-free TTA; sim-to-real is paradigm gap, not data gap
> - [[2604.24018|Sim2Real-Betting]] — Sequential-betting estimator achieving **70-100%** win rate vs Monte Carlo; reframes sim-to-real as variance reduction

^key-papers-5

> [!tip] The Evaluation Stack
> ==[[2405.05941|SimplerEnv]]== (does sim correlate with real?) → ==[[2605.06311|VISER]]== (which visual cues drive correlation?) → ==[[2604.10856|BridgeSim]]== (where does OL-CL diverge?) → ==[[2604.24018|Sim2Real-Betting]]== (how to combine multiple imperfect sims?). Use the stack — single-metric evaluation now reads as inadequate. Cross-reference [[02_Dataset-Benchmark-Environment#12. Sim-to-Real Transfer Evaluation]] for the benchmark-side view of the same stack and [[02_Dataset-Benchmark-Environment#13. Real-World Evaluation Infrastructure]] for the real-robot harnesses it terminates in. For the policy-side evaluation methodology this stack feeds, see [[04_VLA#16. VLA Evaluation & Benchmarking Methodology]].

^insight-5

---

### 6. Integration Patterns

The §2–§5 components are not standalone recipes — they compose into four canonical deployable pipelines. Each pattern picks a primary point on the §1 design-space axes, then layers complementary elements to plug the gaps. The pattern you pick is determined by your *deployment regime* (one robot vs. fleet, narrow task vs. open world) far more than by your favorite paper.

#### 6.1 Pattern A — Massive DR + Procedural Sim

Combine procedural environment generation ([[2603.16861|MolmoBot]]) with extensive domain randomization ([[2210.13702|DeXtreme]] VADR) + teacher-student distillation ([[2511.15200|VIRAL]]). The industrial-scale recipe for general-purpose VLA training. Expensive in compute, broad in generalization.

- **[[2603.16861|MolmoBot]]** (Allen AI) — A procedural [MuJoCo](https://mujoco.org) data engine at scale: ==232K environments==, ==48K objects==, ==1.8M trajectories==; **79.2%** real [Franka FR3](https://franka.de) zero-shot vs π0.5-DROID's **39.2%** *with* real data.
- **[[2210.13702|DeXtreme]]** — The foundational ==Vectorized Automatic Domain Randomization== recipe on the Allegro Hand; **27.8** real reorientations vs **14.8** hand-tuned — auto-DR roughly doubles transfer.
- **[[2511.15200|VIRAL]]** (Unitree) — A visual sim-to-real framework at scale; ==tiled-renderer DAgger== student up to **64 GPUs**; **54/59** real G1 loco-manipulation cycles, matching expert teleop.

See [[04_VLA#1. Design-Space Principles]] for the upstream data strategy.

#### 6.2 Pattern B — Learned-Sim Foundation + Policy Fine-Tune

Pre-train against a learned world simulator ([[2310.06114|UniSim]] / [[2501.03575|Cosmos]]), then policy-side fine-tune on deployment-specific dynamics. Tradeoff: cheap visual diversity, but learned simulators ==blur on contact== — pair with hand-crafted physics for contact-heavy tasks.

- **[[2501.03575|Cosmos]]** — A ==World Foundation Model Platform==: **100M** curated clips, **+4 dB** PSNR tokenizer, ==10 FPS== autoregressive generation; defines the WFM category.
- **[[2310.06114|UniSim]]** — A simulator doing ==Conditional video generation== via ==5.6B-parameter diffusion==; **3-4×** zero-shot policy gain vs baselines on vision-language tasks.
- **[[2511.23369|SimScale]]** (driving) — A ==3DGS reconstruction== + sim-real co-training sim for autonomous driving; **>20%** relative gain for weak baselines, **EPDMS 48.0** on navhard.

See [[06_WAM#2. VideoGen WAMs]] for the upstream WAM architectures used as simulators.

#### 6.3 Pattern C — Digital-Twin-in-the-Loop

Reconstruct deployment scene as a digital twin ([[2503.17973|PhysTwin]] / [[2511.07416|PhysWorld]]), train RL inside the twin, transfer. Deployment-specific but cheap *per deployment*. Best for narrow, high-precision applications (specific assembly task, specific deformable target).

- **[[2511.07416|PhysWorld]]** — A digital-twin pipeline: task-conditioned video → ==4D reconstruction== → physical twin → ==object-centric residual RL==; **82%** real success across 10 tasks; **+15pp** over RIGVid.
- **[[2503.17973|PhysTwin]]** — A twin built from ==Spring-mass models== + ==Gaussian splats== for *deformable* objects from video; real-time interactive sim drives motion planning.
- **[[2504.03597|Real-is-Sim]]** — An ==Embodied Gaussians== twin as the policy's ==sole interface==; real robot mirrors sim via **60Hz** visual sync; **+23pp** PushT with 30+30 demos.

See [[08_Physics-Aware-Embodied-AI#4. External Simulators in the Optimization Loop]] for the external-simulator coupling perspective.

#### 6.4 Pattern D — Online Adaptation with World-Model Feedback

Treat the sim-real gap as an OOD shift the world model detects and corrects for ([[2603.04029|Self-Adapting-RL]]). Cheapest at deployment time but requires a continually-trained world model. Good fit for long-deployment robots that face slow distribution shift (e.g., wear over months).

- **[[2603.04029|Self-Adapting-RL]]** — An ==[[2301.04104|DreamerV3]]==-based online continual RL; ==Observation== + ==Reward Prediction Residuals== trigger fine-tuning; Walker recovers from actuator damage in **2 min**; F1Tenth adapts to combined sim-real + friction shift in **8 min**.

> [!success] Choose Your Pattern
> - **Generalist robot foundation?** Pattern A (Procedural + DR + Distillation)
> - **Need visual diversity + actions?** Pattern B (Learned sim + policy fine-tune)
> - **Narrow high-precision deployment?** Pattern C (Digital twin)
> - **Long-deployment continual adaptation?** Pattern D (Online world-model)

**Integration Patterns — Decision Matrix**

| Deployment regime | Pattern | Why |
|---|---|---|
| Open-world generalist robot fleet | **Pattern A** (Procedural + DR) | [[2603.16861\|MolmoBot]] proves real-data-free training can beat real-data baselines at scale |
| Pre-trained VLA, broad visual coverage | **Pattern B** (Learned sim) | [[2501.03575\|Cosmos]]/[[2310.06114\|UniSim]] absorb internet video at sub-sim asset cost |
| One robot, one workspace, deformable or precise contact | **Pattern C** (Digital twin) | [[2511.07416\|PhysWorld]]/[[2503.17973\|PhysTwin]] win when the deployment scene is the same as training |
| Multi-month deployed robot with slow drift | **Pattern D** (Online WM) | [[2603.04029\|Self-Adapting-RL]] treats deployment drift as just-another-OOD event |
| Industrial assembly with imperfect demos | **Pattern A + C hybrid** | [[2603.15956\|ExpertGen]]/[[2602.23253\|SPARR]] layer real residual on sim-trained base (**95-100%** AutoMate) |
| Force-aware dexterous tasks | **Pattern A + tactile sim** | [[2601.02778\|Force-Based-Sim2Real]] / [[2604.27367\|DOT-Sim]] add ==distance-field tactile== + ==MPM== to the recipe |

^dm-6

> [!star] Key Papers — Integration Pattern Exemplars
> - [[2603.16861|MolmoBot]] — Pattern A exemplar: **79.2%** real [Franka FR3](https://franka.de) from 232K procedural environments, no real data
> - [[2501.03575|Cosmos]] — Pattern B exemplar: WFM platform with 100M curated clips for learned-sim foundation
> - [[2511.07416|PhysWorld]] — Pattern C exemplar: **82%** real success across 10 tasks via task-conditioned video → physical twin → residual RL
> - [[2603.04029|Self-Adapting-RL]] — Pattern D exemplar: [[2301.04104|DreamerV3]] prediction residuals trigger online world-model + policy fine-tuning
> - [[2602.23253|SPARR]] — Pattern A+C hybrid exemplar: sim-trained base + ==vision-conditioned real residual==; **95-100%** AutoMate assembly without human supervision

^key-papers-6

> [!tip] Patterns Compose — Pure Recipes Are Rare
> The 2026 frontier is *hybrid* patterns, not pure ones. [[2602.23253|SPARR]] layers a real-world residual (Pattern C-ish) on top of a procedurally-trained sim base (Pattern A). [[2603.15956|ExpertGen]] combines generative priors (Pattern B-ish) with DR (Pattern A) and visuomotor distillation. The discipline that wins is *picking the right primary pattern* for your deployment regime, then layering the secondary elements based on which sim-real gap (dynamics, visual, semantic) is dominant. For a learned-WAM-as-simulator deep dive, see [[06_WAM#2. VideoGen WAMs]]; for physics-grounded digital-twin coupling, see [[08_Physics-Aware-Embodied-AI#4. External Simulators in the Optimization Loop]]; for force-aware tactile integration, see [[10_Contact-Rich-and-Tactile-Control#3. Force-Conditioned VLA Architectures]].

^insight-6

---

### 7. Open Problems

Sim-to-real has reached the point where the *median* lab-task transfers with reasonable success — but the failure modes have moved upstream. The seven open problems below cluster into three categories: *evaluation & generalization* (correlation benchmarks collapse under perturbation; benchmarks are fragmented), *simulator fidelity* (DR ceilings, learned-sim contact failures), and *methodological / orthogonal frontiers* (reward-signal transfer, statistical sim-stacking, controller-gain interaction). Each cluster needs a different research bet.

#### 7.1 Evaluation & Generalization

The benchmarks that currently certify sim-to-real are unstable: high correlation holds in-distribution but collapses under perturbation, and the benchmark stack itself is fragmented across correlation, generalization, and world-model evaluations.

- **==Sim-real correlation collapses on OOD perturbations==** — [[2405.05941|SimplerEnv]] and [[2605.06311|VISER]] achieve high correlation on *in-distribution* tasks but neither has shown the correlation survives intentional visual or dynamics perturbations. The next frontier is *robust* sim-real correlation under deliberate domain shift.
- **==Sim-to-real evaluation is fragmented==** — [[2509.15273|Embodied-Arena]] unifies **22+** benchmarks but the *correlation* benchmarks ([[2405.05941|SimplerEnv]], [[2605.06311|VISER]]), *generalization* benchmarks ([[2506.18088|RoboTwin-2.0]]), and *world-model* benchmarks ([[2604.21686|WorldMark]]) remain separate stacks. A unified meta-benchmark would expose where methods are weakest.

#### 7.2 Simulator Fidelity

The simulator side of the loop is fundamentally limited by either DR's semantic ceiling or learned-sim contact-physics failures — neither yet generalizes.

- **==DR has limits==** — [[2604.11674|AffordSim]] reveals that domain randomization lifts simple-grasping zero-shot success only to **27%** on affordance-demanding tasks (pouring, hanging) — fine-grained semantic transfer is still unsolved. Combining DR with learned-sim foundations or digital twins is plausible but unproven at scale.
- **==Learned sims blur on contact==** — [[2310.06114|UniSim]] and [[2501.03575|Cosmos]] produce stunning visuals but physical contact regions (collisions, friction transients) look implausible to robots. Hybrid pipelines ([[2604.11138|ViserDex]]: ==3DGS rendering + MuJoCo physics==) are emerging but compute-expensive.

#### 7.3 Methodological & Orthogonal Frontiers

These three problems sit orthogonal to the mainstream "transfer actions across the sim-real gap" framing — they suggest reframings of the problem itself.

- **==Reward-signal sim-to-real==** — Most sim-to-real research transfers *actions*. [[2604.23702|QuietWalk]] shows you can also transfer *reward signals* (a ==PINN-estimated GRF== as RL reward generalizes across footwear). The reward-side sim-to-real problem is underexplored.
- **==Statistical sim-to-real==** — [[2604.24018|Sim2Real-Betting]] proposes treating sim-real as ==variance reduction with biased predictors== — but the practical impact of running banks of cheap biased sims vs. one expensive accurate sim is open.
- **==Online controller-gain interaction==** — [[2604.02523|Tune-to-Learn]] shows controller gains are an unrecognized hyperparameter for sim-to-real, with ==stiff gains *worsening*== transfer despite lower sysid errors. Whether this generalizes beyond proportional-derivative position control is unknown.

**Sim-to-Real Failure Modes — Decision Matrix**

| Problem | Remediation Path |
|---|---|
| Sim-real correlation breaks under OOD perturbation | Stack [[2405.05941\|SimplerEnv]] + [[2605.06311\|VISER]] + perturbation harness — no single robust benchmark yet |
| Need unified meta-benchmark across correlation / generalization / WM | [[2509.15273\|Embodied-Arena]] (22+ benchmarks unified) — partial; correlation stack still separate |
| DR ceiling on affordance-demanding tasks | [[2604.11674\|AffordSim]] (exposes ceiling) + DR-on-top-of-learned-sim — research gap |
| Learned simulator blurs on contact | [[2604.11138\|ViserDex]] (3DGS render + [MuJoCo](https://mujoco.org) physics hybrid) — compute-expensive |
| Need reward signals to cross the gap, not just actions | [[2604.23702\|QuietWalk]] (PINN GRF as RL reward) — underexplored |
| Want to combine multiple cheap biased simulators | [[2604.24018\|Sim2Real-Betting]] (Kelly portfolio of sims) — early framing |
| Controller gains worsen sim-to-real despite low sysid | [[2604.02523\|Tune-to-Learn]] (compliant overdamped > stiff) — narrow to PD position control |

^dm-7

> [!star] Key Papers — Sim-to-Real Frontier
> - [[2604.11674|AffordSim]] — Exposes DR's ceiling: lifts simple grasping to **27%** but fine-grained affordance tasks (pouring/hanging) stay at **10-20%**; the canonical evidence that DR is insufficient for semantic transfer
> - [[2604.02523|Tune-to-Learn]] — Counterintuitive finding: stiff gains minimize sysid error but *worsen* sim-to-real; controller gains are an unrecognized hyperparameter — load-bearing evidence that the sysid metric is the wrong target
> - [[2604.24018|Sim2Real-Betting]] — Reframes sim-to-real as a statistical variance-reduction problem; opens the frontier of combining multiple biased simulators rather than chasing a single accurate one

^key-papers-7

> [!tip] The Common Root Is Mis-Specified Targets
> Six of the seven problems above (correlation collapse, fragmented eval, DR ceiling, learned-sim contact blur, controller-gain interaction, and the implicit assumption that *actions* are what should transfer) trace to the same root: **sim-to-real research has been targeting the wrong proxies**. Sysid error ≠ transfer quality ([[2604.02523|Tune-to-Learn]]); DR coverage ≠ semantic generalization ([[2604.11674|AffordSim]]); visual realism ≠ contact fidelity (UniSim/Cosmos); in-distribution correlation ≠ OOD correlation (SimplerEnv/VISER under perturbation). The methodological reframings ([[2604.23702|QuietWalk]] reward-side, [[2604.24018|Sim2Real-Betting]] statistical) suggest the next decade's progress will come from changing what we measure, not pushing harder on current metrics. Cross-reference [[06_WAM#9. Open Problems & Failure Modes]] (WAMs deployed as simulators inherit the same correlation-under-perturbation failures) and [[08_Physics-Aware-Embodied-AI#8. Open Problems]] (the benchmark-vs-deployment gap is the same problem from the physics-fidelity angle — verifiability gap upstream of the sim-real gap). The navigation domain hits the same mis-specified-target root from its own direction — see [[12_Navigation-and-Mobile-Manipulation#6. Open Problems & Failure Modes]].

^insight-7

---

## Quick-Reference Matrix

| Question | Answer |
|----------|--------|
| Need a learned video simulator? | [[2310.06114\|UniSim]] (foundational), [[2501.03575\|Cosmos]] (platform), or [[2402.15391\|Genie]] (latent actions) |
| Need procedural sim at scale? | [[2603.16861\|MolmoBot]] (232K environments, 79.2% real [Franka](https://franka.de)) |
| Need photoreal autonomous driving sim? | [[2511.23369\|SimScale]] (3DGS + sim-real co-training) or [[2309.17080\|GAIA-1]] |
| Need multi-agent sim? | [[2604.18564\|MultiWorld]] (action-identity + global state encoder) |
| Need domain randomization? | [[2210.13702\|DeXtreme]] (VADR) — auto-DR doubles transfer over hand-tuned |
| Need robust RL? | [[2510.14246\|DR-RPO]] (linear FA), [[2204.12581\|RAMBO-RL]] (adversarial offline), or [[2602.13040\|TCRL]] (temporal-coupled constrained) |
| Need humanoid sim-to-real? | [[2511.15200\|VIRAL]] (loco-manipulation), [[2506.12851\|KungfuBot]] (highly-dynamic), or [[2502.20396\|Humanoid-Sim2Real-Dex]] (dexterous) |
| Need force-aware sim-to-real? | [[2601.02778\|Force-Based-Sim2Real]] or [[2604.27367\|DOT-Sim]] — see [[10_Contact-Rich-and-Tactile-Control#2. Tactile Sensors as a Sensing Modality]] for tactile depth |
| Need a digital twin? | [[2503.17973\|PhysTwin]] (deformable) or [[2511.07416\|PhysWorld]] (robot policy) — see [[08_Physics-Aware-Embodied-AI#4. External Simulators in the Optimization Loop]] |
| Need policy that runs *only* in the twin (real robot mirrors sim)? | [[2504.03597\|Real-is-Sim]] (Embodied-Gaussians + 60Hz visual sync; +23pp PushT) |
| Need real2sim from video? | [[2404.09833\|Video2Game]] (rigid-body, browser-compatible) |
| Need vision-residual on top of sim-trained base for industrial assembly? | [[2602.23253\|SPARR]] (95-100% AutoMate without human supervision) |
| Need controller-gain awareness? | [[2604.02523\|Tune-to-Learn]] — compliant overdamped gains beat stiff for BC; stiff gains *worsen* sim-to-real |
| Need to evaluate sim-real correlation? | [[2405.05941\|SimplerEnv]] (r > 0.85) + [[2605.06311\|VISER]] (r = 0.92) — or [[2511.04665\|Real-to-Sim-GS]] (r > 0.9) for **deformable-object** tasks |
| Need to diagnose OL-CL gap? | [[2604.10856\|BridgeSim]] (observational shift + objective mismatch) |
| Need to combine multiple sims? | [[2604.24018\|Sim2Real-Betting]] (Kelly portfolio of sims) |
| Need a unified evaluation platform? | [[2509.15273\|Embodied-Arena]] (22+ benchmarks) or [[2604.21686\|WorldMark]] (interactive WMs) |
| Need physics-informed reward shaping? | [[2604.23702\|QuietWalk]] (PINN GRF predictor as reward) |
| Need friction modeling for sim-to-real? | [[2604.24916\|asRoBallet]] (multi-channel tribology in [MuJoCo](https://mujoco.org)) |

---

## Cross-References

- [[01_Embodied-AI-101]] — Embodied AI primer; sim-to-real is the bridge between training and deployment
- [[02_Dataset-Benchmark-Environment]] — Datasets and benchmarks; §12 Sim-to-Real Transfer Evaluation + §4 Physics Engines + §7 Soft-Body Benchmarks expand here
- [[04_VLA]] — VLA deep-dive; sim-to-real is the bottleneck for the in-domain post-training recipe (§1)
- [[06_WAM]] — WAM deep-dive; learned world simulators ([[2310.06114|UniSim]], [[2501.03575|Cosmos]]) are WAMs deployed as simulators
- [[15_Self-Evolving-VLA-WAM]] — Self-evolving; world-model feedback for online sim-to-real adaptation
- [[08_Physics-Aware-Embodied-AI]] — Physics priors; §4 External Simulators in the Optimization Loop overlaps real2sim2real
- [[10_Contact-Rich-and-Tactile-Control]] — Force-aware policies; tactile sim-to-real ([[2604.27367|DOT-Sim]], Force-Based)

---

*See [[06_WAM]] for world-model architectures used as simulators, [[08_Physics-Aware-Embodied-AI]] for physics-coupled sim-real loops, or [[02_Dataset-Benchmark-Environment]] for the broader benchmark ecosystem.*
