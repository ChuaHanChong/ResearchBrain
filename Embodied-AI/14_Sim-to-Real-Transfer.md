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
> Simulation is the only economically viable substrate for training data-hungry embodied policies — but simulators are wrong about *something*: lighting, friction, contact transients, actuator dynamics, or the long-tail of object appearance. The "reality gap" is the operational cost of those errors when the policy meets the real world. This note maps the four parallel research threads that have evolved to close it: building **better simulators** ([[2310.06114|UniSim]], [[2501.03575|Cosmos]], [[2402.15391|Genie]], [[2604.18564|MultiWorld]]) that hallucinate richer worlds; designing **more robust policies** ([[2510.14246|DR-RPO]], [[2204.12581|RAMBO-RL]], [[2210.13702|DeXtreme]], [[2603.15956|ExpertGen]]) that absorb sim noise; closing **real→sim→real loops** ([[2503.17973|PhysTwin]], [[2511.07416|PhysWorld]], [[2404.09833|Video2Game]]) that rebuild the deployment scene as a digital twin; and constructing **reality-gap diagnostics** ([[2405.05941|SimplerEnv]], [[2605.06311|VISER]], [[2604.24018|Sim2Real Betting]]) that let you measure how far you still are from real-world success.

## Evolution Graph

```mermaid
graph TD
    subgraph "Sim-Side: Learned & Procedural Simulators"
        A["GAIA-1<br/><i>2023</i>"]
        B["UniSim<br/><i>2023</i>"]
        C["Genie<br/><i>2024</i>"]
        D["Video2Game<br/><i>2024</i>"]
        E["Cosmos<br/><i>2025</i>"]
        F["MolmoB0T<br/><i>2026</i>"]
        G["AffordSim<br/><i>2026</i>"]
        H["MultiWorld<br/><i>2026</i>"]
        I["SimScale<br/><i>2026</i>"]
    end

    subgraph "Policy-Side: Robustness & Domain Randomization"
        J["RAMBO-RL<br/><i>2022</i>"]
        K["DeXtreme<br/><i>2022</i>"]
        L["Humanoid Sim2Real Dex<br/><i>2025</i>"]
        M["KungfuBot<br/><i>2025</i>"]
        N["DR-RPO<br/><i>2025</i>"]
        O["VIRAL<br/><i>2025</i>"]
        P["TCRL<br/><i>2026</i>"]
        Q["Force-Based Sim2Real<br/><i>2026</i>"]
        R["ExpertGen<br/><i>2026</i>"]
        S["ULTRA<br/><i>2026</i>"]
        T["QuietWalk<br/><i>2026</i>"]
        U["asRoBallet<br/><i>2026</i>"]
        V["ViserDex<br/><i>2026</i>"]
        W["HiPAN<br/><i>2026</i>"]
        X["Tune to Learn<br/><i>2026</i>"]
    end

    subgraph "Real2Sim2Real Loops & Digital Twins"
        Y["PhysTwin<br/><i>2025</i>"]
        Z["PhysWorld<br/><i>2025</i>"]
        AA["DOT-Sim<br/><i>2026</i>"]
        AB["Explicit WM Manip<br/><i>2026</i>"]
        AC["CoEnv<br/><i>2026</i>"]
        AD["Self-Adapting RL<br/><i>2026</i>"]
    end

    subgraph "Evaluation & Reality-Gap Measurement"
        AE["SimplerEnv<br/><i>2024</i>"]
        AF["RoboTwin 2.0<br/><i>2025</i>"]
        AG["Embodied Arena<br/><i>2025</i>"]
        AH["BridgeSim<br/><i>2026</i>"]
        AI["WorldMark<br/><i>2026</i>"]
        AJ["Sim2Real Betting<br/><i>2026</i>"]
        AK["VISER<br/><i>2026</i>"]
    end

    A --> E
    B --> C --> H
    B --> E
    D --> Y
    E --> I
    F --> R
    G --> R
    J --> N --> P
    K --> L --> O
    K --> V
    M --> S
    M --> T
    O --> S
    Y --> Z --> AB
    Y --> AA
    Z --> AC
    AE --> AF --> AK
    AE --> AH
    AG --> AK

    style B fill:#e8f4fd,stroke:#4a90d9
    style E fill:#e8f4fd,stroke:#4a90d9
    style I fill:#e8f4fd,stroke:#4a90d9
    style K fill:#fde8f4,stroke:#d94a90
    style O fill:#fde8f4,stroke:#d94a90
    style R fill:#fde8f4,stroke:#d94a90
    style Y fill:#e8fde8,stroke:#27ae60
    style Z fill:#e8fde8,stroke:#27ae60
    style AE fill:#fef3e8,stroke:#e67e22
    style AK fill:#fef3e8,stroke:#e67e22
```

The field evolved through four parallel research threads. **Sim-side** (2023→2026) replaces hand-crafted simulators with *learned* world simulators that absorb internet-scale video — [[2310.06114|UniSim]] → [[2501.03575|Cosmos]] → [[2511.23369|SimScale]] push photorealistic, action-conditioned generation. **Policy-side** (2022→2026) trains the *policy* to be sim-noise-invariant — [[2210.13702|DeXtreme]]'s automatic domain randomization, [[2506.12851|KungfuBot]]'s physics-feasible motion retargeting, and [[2510.14246|DR-RPO]]'s distributionally robust policy optimization treat the reality gap as adversarial. **Real2sim2real** (2024→2026) reconstructs the *deployment* scene as a high-fidelity digital twin ([[2503.17973|PhysTwin]], [[2404.09833|Video2Game]], [[2511.07416|PhysWorld]]), then trains the policy against the twin before transfer. **Evaluation** (2024→2026) builds diagnostic benchmarks ([[2405.05941|SimplerEnv]], [[2605.06311|VISER]]) that *measure* the sim-to-real correlation — making the reality gap quantifiable rather than mythical.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2022 | [[2204.12581\|RAMBO-RL]] | Policy-side | Adversarial dynamics model for robust offline RL; reality gap as zero-sum game |
| 2022 | [[2210.13702\|DeXtreme]] | Policy-side | Vectorized Automatic Domain Randomization on Allegro Hand; 27.8 mean reorientations |
| 2023 | [[2309.17080\|GAIA-1]] | Sim-side | Generative world model for autonomous driving; 40s+ photoreal rollouts |
| 2023 | [[2310.06114\|UniSim]] | Sim-side | Learned interactive real-world simulator from heterogeneous video |
| 2024 | [[2402.15391\|Genie]] | Sim-side | Latent-action interactive environments from unlabeled internet video |
| 2024 | [[2404.09833\|Video2Game]] | Real2sim2real | Single-video → browser-compatible interactive 3D environment with physics |
| 2024 | [[2405.05941\|SimplerEnv]] | Evaluation | r>0.85 sim-to-real correlation via system-id + green screening |
| 2025 | [[2501.03575\|Cosmos]] | Sim-side | NVIDIA World Foundation Model platform; 100M curated clips; physical-AI digital twins |
| 2025 | [[2502.20396\|Humanoid Sim2Real Dex]] | Policy-side | Autotuned modeling + hybrid object reps; 80% box-lift on GR-1 humanoid |
| 2025 | [[2503.17973\|PhysTwin]] | Real2sim2real | Physics-informed deformable digital twin from video; real-time interactive sim |
| 2025 | [[2504.03597\|Real-is-Sim]] | Real2sim2real | Embodied-Gaussians digital twin as policy's *sole* interface; real robot mirrors sim |
| 2025 | [[2506.12851\|KungfuBot]] | Policy-side | Physics-based motion processing; zero-shot transfer of martial arts on G1 |
| 2025 | [[2506.18088\|RoboTwin 2.0]] | Evaluation | Domain-randomized data generator; +24.4% real-world few-shot |
| 2025 | [[2509.15273\|Embodied Arena]] | Evaluation | 22+ benchmarks unified; capability taxonomy |
| 2025 | [[2510.14246\|DR-RPO]] | Policy-side | Distributionally robust regularized policy optimization with linear FA |
| 2025 | [[2511.04665\|Real-to-Sim GS]] | Evaluation | 3DGS + soft-body [[2503.17973\|PhysTwin]] for deformable-policy evaluation; **r > 0.9** sim-real correlation |
| 2025 | [[2511.07416\|PhysWorld]] | Real2sim2real | Robot learning from physical world model; 82% real success across 10 tasks |
| 2025 | [[2511.15200\|VIRAL]] | Policy-side | Visual sim-to-real at scale for humanoid loco-manipulation; 54/59 on Unitree G1 |
| 2026 | [[2511.23369\|SimScale]] | Sim-side | 3DGS sim data engine + sim-real co-training; +20% weak-baseline gains |
| 2026 | [[2602.23253\|SPARR]] | Policy-side | Sim-trained base + vision-conditioned real residual; 95-100% AutoMate assembly without human supervision |
| 2026 | [[2601.02778\|Force-Based Sim2Real]] | Policy-side | Tactile distance-field sim + actuator calibration for force-aware grasping |
| 2026 | [[2602.13040\|TCRL]] | Policy-side | Temporal-coupled adversarial training for constrained RL; up to 19,077% cost reduction |
| 2026 | [[2603.04029\|Self-Adapting RL]] | Real2sim2real | [[2301.04104\|DreamerV3]] world-model feedback for online sim-to-real adaptation |
| 2026 | [[2603.15956\|ExpertGen]] | Policy-side | Generative prior + DSRL + visuomotor distillation; 90.5% AutoMate assembly |
| 2026 | [[2603.16861\|MolmoBot]] | Sim-side | 232K-environment procedural [MuJoCo](https://mujoco.org); 79.2% real [Franka FR3](https://franka.de) — no real-world data |
| 2026 | [[2604.10856\|BridgeSim]] | Evaluation | Decomposes OL-CL gap; observational shift + objective mismatch; +19.1 DS via TTA |
| 2026 | [[2604.11138\|ViserDex]] | Policy-side | 3DGS pre-rasterization augmentation + monocular RGB; 37.6 reorientations |
| 2026 | [[2604.11674\|AffordSim]] | Sim-side | Affordance-aware data generator + 3DGS backgrounds for sim-to-real |
| 2026 | [[2604.18564\|MultiWorld]] | Sim-side | Multi-agent multi-view video world models; agent-identity + global state encoder |
| 2026 | [[2604.21686\|WorldMark]] | Evaluation | Unified benchmark suite for interactive video WMs; ρ>0.9 with human |
| 2026 | [[2604.24018\|Sim2Real Betting]] | Evaluation | Sequential-betting estimator; 70-100% win rate vs Monte Carlo |
| 2026 | [[2604.24916\|asRoBallet]] | Policy-side | Friction-aware [MuJoCo](https://mujoco.org) + RL; zero-shot ballbot whole-body locomotion |
| 2026 | [[2604.27367\|DOT-Sim]] | Real2sim2real | Differentiable MPM + residual rendering; 90.5% indenter, 96.6% tumor detection |
| 2026 | [[2604.23702\|QuietWalk]] | Policy-side | PINN GRF predictor + curriculum; 7.17 dBA noise reduction across footwear |
| 2026 | [[2605.06311\|VISER]] | Evaluation | Ray-traced PBR + MLLM asset pipeline; r=0.92 Pearson sim-real correlation |

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
| **Hand-crafted physics** | [PhysX](https://developer.nvidia.com/physx-sdk) / [MuJoCo](https://mujoco.org) / [[2511.04831\|Isaac Lab]] with explicit constitutive laws | [[2210.13702\|DeXtreme]], [[2603.16861\|MolmoBot]] |
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
| Physical accuracy on contact | Hand-crafted physics ([MuJoCo](https://mujoco.org) / [[2511.04831\|Isaac Lab]]) + DR ([[2210.13702\|DeXtreme]]) |
| Fast deployment-specific transfer | Digital twin: [[2503.17973\|PhysTwin]] / [[2511.07416\|PhysWorld]] / [[2504.03597\|Real-is-Sim]] |
| Cheap visual diversity + physical contact | Hybrid 3DGS + physics: [[2604.11138\|ViserDex]] / [[2511.23369\|SimScale]] / [[2604.11674\|AffordSim]] |
| Publishable rigor on sim claims | Pair with correlation benchmark: [[2405.05941\|SimplerEnv]] (r > 0.85) or [[2605.06311\|VISER]] (r = 0.92) |
| Long-deployment continual shift | Adaptation-at-deployment: [[2603.04029\|Self-Adapting RL]] with [[2301.04104\|DreamerV3]] feedback |
| Combine many imperfect sims | Statistical estimator: [[2604.24018\|Sim2Real Betting]] (Kelly portfolio) |

> [!star] Key Papers — Design-Space Exemplars
> - [[2310.06114|UniSim]] — Pure Axis-1 learned-sim exemplar; **3-4×** zero-shot policy gain via ==conditional video generation== with a **5.6B**-parameter diffusion model
> - [[2210.13702|DeXtreme]] — Pure Axis-2 in-simulator-adaptation exemplar; ==Vectorized Automatic Domain Randomization== doubles transfer (**27.8** vs **14.8** reorientations on Allegro Hand)
> - [[2405.05941|SimplerEnv]] — Pure Axis-3 evaluation exemplar; first reliable correlation benchmark (**r > 0.85**) with ==MMRV== rank metric
> - [[2511.07416|PhysWorld]] — All-three-axes integrated; digital twin (Axis 1) + residual RL (Axis 2) + 10-task real-world ground truth (Axis 3), **82%** average success
> - [[2604.24018|Sim2Real Betting]] — Reframes Axis 3 as variance reduction; **70-100%** win rate vs Monte Carlo using a ==Kelly portfolio== of biased simulators

> [!tip] Pick by Constraint
> If you need to **scale to internet video data**, pick learned sim ([[2310.06114|UniSim]]/[[2501.03575|Cosmos]]). If you need **physical accuracy on contact**, pick hand-crafted physics ([MuJoCo](https://mujoco.org) + DR). If you need **fast deployment-specific transfer**, pick a digital twin ([[2503.17973|PhysTwin]]/[[2511.07416|PhysWorld]]). If you need **publishable rigor**, pair any of these with a correlation benchmark ([[2405.05941|SimplerEnv]]/[[2605.06311|VISER]]). The three axes are *not* independent in practice — better sim quality (Axis 1) reduces the burden on policy-side robustness (Axis 2), and tighter correlation benchmarks (Axis 3) force investment in both. See [[07_WAM#2. VideoGen WAMs]] for the WAM-as-simulator perspective on Axis 1, and [[11_Physics-Aware-Embodied-AI#4. External Simulator Coupling]] for the digital-twin coupling that bridges Axes 1 and 2.

---

## Part B — Closing the Gap

*Three complementary attack surfaces: sim-side (better simulators), policy-side (robustness), and real2sim2real (digital twins).*

### 2. Sim-Side: Learned & Procedural Simulators

The first sim-to-real strategy is to make the simulator richer than reality — through learned video generation, procedural environment scale, or photorealistic rendering. The trade-off: learned simulators handle visual diversity well but blur on physical contact; hand-crafted simulators handle contact well but require enormous procedural-asset effort to cover the visual long tail.

#### 2.1 Generative Video World Simulators

Learn the simulator from internet-scale video; the model itself becomes the simulator. A complementary hand-crafted-but-LLM-driven track ([[2601.02078|Genie Sim 3.0]]) converges on the same goal — cheap, scalable, photorealistic, evaluable — from the opposite direction.

- **[[2606.02058|TIDES]]** — A simulator doing ==Time-derivative event simulation== from a dynamic ==4D Gaussian splatting== scene: ==visibility-consistent time-derivatives of log-luminance== via forward-mode autodiff + ==risk-guided adaptive time-stepping==; best fidelity (lowest **IG-NLL** + **Chamfer**); **models trained on TIDES events transfer best to real data**.
- **[[2604.18564|MultiWorld]]** — A multi-agent multi-view video world model that builds on an ==action-conditioned diffusion== + ==Flow Matching== backbone, combining ==Agent Identity Embedding== (RoPE), ==Adaptive Action Weighting==, and a ==Global State Encoder== over pretrained ==VGGT==; reaches **FVD 179** vs baselines' 207–245 and **RPE 0.67** vs 0.72–0.75.
- **[[2511.23369|SimScale]]** — A ==3D Gaussian Splatting== reconstruction sim that bridges the sim-real visual gap for autonomous driving; its ==pseudo-expert pipeline== couples reactive ==Intelligent Driver Model== agents with ==LQR== ego + trajectory perturbation; weak baselines (LTF, DiffusionDrive) see **>20%** relative gains under sim-real co-training; **EPDMS 48.0** on navhard.
- **[[2501.03575|Cosmos]]** — An open-source ==World Foundation Model Platform== from NVIDIA that curates **20M hr** raw video → **100M** clips and pre-trains diffusion + autoregressive ==WFMs== fine-tuned for navigation/manipulation/driving; Tokenizer suite +**4 dB** PSNR, **2-12×** faster inference; repositions WFMs as a foundation-model category analogous to LLMs.
- **[[2402.15391|Genie]]** — A learned simulator of ==Latent-action interactive environments== from unlabeled internet video via ==Video Tokenizer + Latent Action Model (LAM) + Dynamics Model==; its ==ST-transformer== separates spatial/temporal attention for linear-in-frames scaling. Learns discrete latent action codes unsupervised; the foundational unsupervised-action-discovery simulator.
- **[[2310.06114|UniSim]]** — A simulator doing ==Conditional video generation== via ==5.6B-parameter video diffusion==; orchestrates heterogeneous data (robotics, human activity, panoramas, internet video) into a ==unified action space== (lang + control → ==T5 embeddings== + normalized values); zero-shot sim-to-real on physical robots, **3-4×** better goal reduction for VLMs vs baselines.
- **[[2309.17080|GAIA-1]]** — A two-stage ==autoregressive world model + video diffusion decoder== that frames world modeling as ==next-token prediction== over a common token space (video + text + actions); generates **40s+** photorealistic action-conditioned rollouts, demonstrating LLM-style scaling for driving WMs — early proof learned simulators could model long-horizon driving dynamics.
- **[[2601.02078|Genie Sim 3.0]]** — A hand-crafted-but-LLM-driven humanoid simulation platform whose ==Genie Sim Generator== composes scenes from natural-language instructions, with ==LLM-VLM auto-evaluation== and ==3D Gaussian Splatting== reconstruction; **R²=0.94** sim-real correlation, and **1,500 episodes** of synthetic data beat real-data baselines zero-shot.

#### 2.2 Procedural Environment Generation

Hand-crafted physics + massive procedural scale; no learned visual model.

- **[[2603.16861|MolmoBot]]** — An ==MolmoBot-Engine== procedural data generator in ==[MuJoCo](https://mujoco.org)==; **232K** indoor environments, **48K** objects, **1.8M** expert trajectories; ==domain randomization== enables zero-shot sim-to-real *without real fine-tuning*; **79.2%** real [Franka FR3](https://franka.de) pick-and-place — beats real-data π0.5-DROID (**39.2%**).
- **[[2604.11674|AffordSim]]** — An affordance-aware data generator integrating ==VoxAfford== open-vocabulary 3D affordance prediction with ==two-stage grasp selection== and ==3DGS background-replacement== DR; collection reaches **79%/64%** (medium/hard) vs AnyGrasp's **15%/3%**, yet zero-shot Franka FR3 sim-to-real averages just **24%** — canonical evidence that affordance is the DR ceiling.
- **[[2505.10755|Infinigen-Articulated]]** — A procedural articulated-asset toolkit using ==Blender Geometry/Shader Nodes== with custom revolute/prismatic joint node-groups, auto-converting to ==simulation-ready URDF/USD/MJCF==; RL policies trained only on it improve success **2.86×** over PartNet-Mobility and lift real door-opening to **18/30** (vs **3/30**) zero-shot.
- **[[2504.09997|GenTe]]** — A ==dual-level terrain simulation framework== for legged locomotion modeling both geometry (height maps, obstacles) and physical interactions (water wading, deformable sand) with realistic forces, using ==VLMs + function-calling== to generate contextual terrains; policies hold high success on diverse unseen VLM-generated terrains.

#### 2.3 Synthetic Demonstration Generation

Generate diverse, action-consistent training demonstrations — via video diffusion or sim-replay — to amortize real-world collection and close the visual sim-to-real gap.

- **[[2604.03552|CRAFT]]** — A ==video diffusion==-based bimanual data generator that replays real demos into varied sim trajectories, extracts ==Canny-edge control videos==, and conditions a diffusion transformer across ==seven augmentation axes== (pose, lighting, color, background, viewpoint, multi-view, cross-embodiment); **89.3%** sim cross-embodiment and **17-19/20** real generalization.
- **[[2603.25725|SoftMimicGen]]** — A deformable-object data-generation system using ==non-rigid registration== to adapt 1-3 human demos into thousands of demonstrations via a continuous ==deformation field== in Isaac Lab; **70-100%** generation success, **25-97%** higher policy SR than source-only, and zero-shot sim-to-real (**63.3%**, **93.3%** with co-training).
- **[[2512.11797|AnchorDream]]** — A ==video diffusion== robot-data synthesizer using a ==decoupled trajectory-environment== paradigm: render ==robot-only motion videos== as conditioning, then a pretrained diffusion model fills photorealistic objects/scenes coherent with the anchored motion; **+36%** sim (RoboCasa) and real SR doubled **28% → 60%** across six PiPER tasks.
- **[[2508.03944|Constraint-Preserving DataGen]]** — A constraint-preserving data generator (CP-Gen) that formulates skills as ==object-centric keypoint-trajectory constraints== from one demo, then samples novel poses and non-uniform geometries and re-optimizes joint configs; **70%** sim and **83%** zero-shot sim-to-real on novel-geometry tasks (vs MimicGen **40%**).

**Sim-Side — Decision Matrix**

| Need | Recommendation |
|---|---|
| Scale to internet-video diversity, blur-tolerant on contact | [[2501.03575\|Cosmos]] or [[2310.06114\|UniSim]] — learned video-WFMs; **100M** clips / **3-4×** zero-shot gain |
| Multi-agent multi-view interactive simulator | [[2604.18564\|MultiWorld]] — action-conditioned diffusion + Flow Matching; **FVD 179**, **RPE 0.67** |
| Sim-real visual gap closure for autonomous driving | [[2511.23369\|SimScale]] — 3DGS reconstruction + sim-real co-training; **EPDMS 48.0** on navhard |
| Latent-action interactive environments from unlabeled web video | [[2402.15391\|Genie]] — unsupervised action discovery; foundational learned-sim |
| Long-horizon photorealistic driving rollouts | [[2309.17080\|GAIA-1]] — generative WM; 40s+ action-conditioned rollouts |
| LLM-driven scene composition + auto-evaluation for humanoid | [[2601.02078\|Genie Sim 3.0]] — **R²=0.94** sim-to-real correlation, **10K+ hr** synthetic |
| Procedural physics scale, no learned visual model, real-data-free | [[2603.16861\|MolmoBot]] — **232K** environments + [MuJoCo](https://mujoco.org); **79.2%** real Franka beats π0.5-DROID |
| Affordance-aware procedural sim for grasp/pour/hang | [[2604.11674\|AffordSim]] — VoxAfford + 3DGS DR; **+10pp** average, exposes the semantic-DR ceiling |
| Hybrid 3DGS-augmented physics (visual + contact accuracy) | [[2511.23369\|SimScale]] / [[2604.11674\|AffordSim]] / [[2604.11138\|ViserDex]] — the emerging sweet spot |

> [!star] Key Papers
> - [[2310.06114|UniSim]] — Learned interactive real-world simulator; **3-4x** better zero-shot policy transfer than baselines; foundational learned-sim paper
> - [[2501.03575|Cosmos]] — NVIDIA WFM platform: **100M** curated clips, **+4 dB** PSNR tokenizer, **10 FPS** real-time autoregressive generation; defines the WFM category
> - [[2603.16861|MolmoBot]] — **79.2%** real [Franka FR3](https://franka.de) success trained *exclusively* on procedural [MuJoCo](https://mujoco.org) data; proves sim-only can outperform real-data baselines (π0.5-DROID **39.2%**)
> - [[2511.23369|SimScale]] — 3DGS sim-real co-training for autonomous driving; weak baselines see **>20%** relative gains; new **EPDMS 48.0** on navhard

> [!tip] Sim-Side Trade-Off
> Learned video simulators ([[2310.06114|UniSim]], [[2501.03575|Cosmos]]) scale to internet video and capture visual diversity but blur on contact dynamics. Procedural physics simulators ([[2603.16861|MolmoBot]]) handle contact accurately but require massive procedural-asset effort to cover the visual long tail. Hybrid 3DGS-augmented physics ([[2511.23369|SimScale]], [[2604.11674|AffordSim]], [[2604.11138|ViserDex]]) is the emerging sweet spot.

---

### 3. Policy-Side: Robustness & Domain Randomization

Instead of making the simulator perfect, make the *policy* invariant to sim imperfections. This is the dominant industrial-scale recipe — domain randomization remains the de-facto sim-to-real method in 2026.

#### 3.1 Domain Randomization Foundations

The canonical industrial recipe: train in sim with extensive randomization, then either distill to vision or layer a real-world residual on top.

- **[[2605.09789|DRIS]]** — A ==structured, VRAM-efficient randomization== recipe for zero-shot dexterous *reactive catching*, robust to observation noise, execution error, and OOD physical parameters at far lower VRAM than brute-force randomization; **68%** real flat-plate catching vs hand-crafted **5%** / sim-trained **13%**, with emergent generalization to human-thrown objects.
- **[[2605.21688|Microfiber Shape Control]]** — A closed-loop sim-to-real RL method for deformable *microfiber* shaping that trains in a ==frictionless MuJoCo sim== (geometry-focused) and deploys zero-shot with ==real-time visual feedback==; **270 µm** mean / **390 µm** max error on 50 µm silk, generalizing across fiber diameters and to higher-bending-energy targets unseen in training.
- **[[2506.10133|Offline Domain Randomization]]** — A statistical-guarantees framework for ==Offline DR== that formalizes it as ==Maximum-Likelihood Estimation== of a simulator-parameter distribution from offline data, proves **weak and strong consistency** (learned randomization concentrates on true params), and adds ==α-informativeness==, extending to ergodic data + *identified-set* convergence.
- **[[2210.13702|DeXtreme]]** — A ==[[1707.06347|PPO]]== policy trained in ==[Isaac Gym](https://developer.nvidia.com/isaac-gym)== on the Allegro Hand, where the foundational ==Vectorized Automatic Domain Randomization== (VADR) adjusts sim params by policy capability; **27.8** mean real reorientations vs **14.8** hand-tuned DR — auto-DR nearly doubles transfer.
- **[[2603.15956|ExpertGen]]** — A three-phase scalable sim-to-real recipe that learns from *imperfect* behavior priors: (1) a generative ==diffusion policy== prior; (2) ==Diffusion Steering RL (DSRL)== optimizes only the diffusion's initial noise; (3) ==DAgger== visuomotor distillation; **90.5%** avg on 8 AutoMate tasks, **80%** real [Franka](https://franka.de) Lift Banana from RGB.
- **[[2502.20396|Humanoid Sim2Real Dex]]** — A vision-based dexterous-manipulation recipe for the Fourier GR-1 humanoid where ==autotuned robot modeling== bridges the dynamics gap, plus ==contact stickers==, ==stage-based rewards==, and ==divide-and-conquer distillation==; **80%** box-lift, **62.3%** grasp-and-reach, **52.5%** bimanual handover, **60-80%** unseen-object generalization.
- **[[2506.13751|LeVERB]]** — A whole-body humanoid VLA with zero-shot sim-to-real on Unitree G1, whose learned latent ==verb vector== bridges a high-level ==residual CVAE== VLA and a low-level ==DAgger==-distilled reactive controller; **58.5%** mean success across 10 task categories (**7.8×** over naive hierarchical VLA's **7.5%**); align a *latent intermediate*, not *actions*.
- **[[2602.23253|SPARR]]** — An industrial-assembly recipe whose sim base trains via ==PPO + dense imitation rewards==, then adds a **real-world residual** — the base policy autonomously generates demos and a ==vision-conditioned residual== via ==RLPD== corrects them; **95-100%** on 10 AutoMate (**+38.4%**, matching [[2410.21845|HIL-SERL]] with no human supervision); **+74.5%** unseen NIST.
- **[[2606.18953|Object-Centric Residual RL]]** — A residual RL framework adding a sim-trained corrective policy to a frozen real-world base VLA over a ==domain-invariant observation space== (object poses + proprioception + base action) with ==pose noise injection + dropout==; zero-shot real SR **42% → 76%**, and a VLA self-improvement loop lifts the base **42% → 59%**.
- **[[2505.11858|Tight Insertion Sim2Real]]** — A hybrid framework pairing a ==potential-field controller== with a ==residual RL== policy for sub-millimeter insertion, with a ==curriculum== escalating observation noise and correction magnitude; **>90%** real-world zero-shot success across object configs, beating IndustReal without real fine-tuning.

#### 3.2 Robust RL Foundations

Treat the sim-real gap as adversarial; train against the worst-case dynamics.

- **[[2204.12581|RAMBO-RL]]** — An offline RL method framed as a ==two-player zero-sum game== — agent maximizes value, adversarial environment model minimizes it; ==ensemble of neural networks== for dynamics, updated adversarially via ==Model Gradient==; **highest total** D4RL [MuJoCo](https://mujoco.org) score; adversarial training of the *dynamics model itself* adds conservatism.
- **[[2510.14246|DR-RPO]]** — The first provably efficient *online* policy-optimization algorithm for robust MDPs with ==linear function approximation==; policy-regularized d-rectangular ==DRMDPs== / ==RRMDPs== with ==KL-divergence==, ==softmax policy updates==, ==UCB== bonuses; **Õ(d²H²/√K)** average suboptimality — matches value-based methods while supporting *stochastic* policies.
- **[[2602.13040|TCRL]]** — A *constrained*-RL defense against ==temporal-coupled adversarial perturbations==; a ==worst-case-perceived cost constraint== estimates safety costs without explicit adversarial-policy modeling, plus ==dual-constraint defense== (autocorrelation + entropy stability); **559-19,077%** safety-cost reduction, **8.36-34.76%** reward improvement under worst-case attacks.
- **[[2509.18648|SPiDR]]** — A zero-shot *safe* sim-to-real method that extends ==domain randomization== with a ==pessimistic cost penalty== from a ==dynamics-model ensemble== approximating the ==L1-Wasserstein== sim-real gap, solved as a ==CMDP==; transfers safely to a real race car + Unitree Go1 where vanilla DR violates constraints — DR with a formal safety margin.

#### 3.3 Physics-Informed Policy Robustness

Bake physics priors *into* the policy via curriculum, reward shaping, or motion processing.

- **[[2605.10063|EFGCL]]** — An external-force-guided curriculum for high-risk dynamic-motion learning (backflips, jumps) on legged robots, applying ==spotting-inspired external forces== with an ==adaptive curriculum== that decays assistance by success rate; acquires backflip/lateral-flip that PPO baselines *cannot learn at all*; **~2×** faster jumping, zero-shot transfer to real KLEIYN quadruped.
- **[[2604.24916|asRoBallet]]** — A reconfigurable humanoid ballbot built by ==subtractive reconfiguration== of a quadruped, whose critical ingredient is ==friction-aware [MuJoCo](https://mujoco.org)== modeling ==tribological phenomena== + actuator friction; with DR it achieves **zero-shot sim-to-real**, **100%** sim velocity-tracking, **0.05 m/s** real MAE, and recovers from **0.3 m** pushes.
- **[[2604.23702|QuietWalk]]** — A physics-informed RL method for low-noise humanoid locomotion in which an ==inverse-dynamics-constrained PINN== estimates per-foot vertical GRFs from proprioception alone, and the frozen GRF predictor is folded *into the RL reward*; **7.17 dBA** mean-noise reduction across 4 surfaces and **4** footwear types — sim-to-real of the *reward signal*.
- **[[2506.12851|KungfuBot]]** — A physics-based recipe for *highly-dynamic* humanoid skills (martial arts, dancing); a ==physics-based motion processing pipeline== filters untrackable mocap and ==adaptive motion tracking== adjusts the reward factor; with ==asymmetric actor-critic== + ==reference state initialization== + DR, per-body error **53.25 mm** vs **>233 mm** for OmniH2O/ExBody2.
- **[[2508.21065|Learning on the Fly]]** — An online real-time adaptation framework using ==differentiable simulation== in which a ==hybrid dynamics model== couples a low-fidelity analytical model with a learned residual net and ==BPTT== gives first-order policy updates; cuts hovering error **81%** vs L1-MPC / **55%** vs DATT; real quadrotors adapt to mass + wind in **3 steps** (**4.5 s**).
- **[[2602.14174|Direction Matters]]** — A contact-rich sim-to-real method training a sim policy to predict the ==normal force direction== as a *dynamics-invariant* signal, then deploying a ==force-aware admittance controller== with a hand-tuned magnitude; **91%** across four real tasks (vs best baseline **67%**), cutting both insufficient- and excessive-force failures.
- **[[2510.25405|Stress-Guided RL]]** — A ==SAC==-based framework for gentle deformable/fragile manipulation that adds an ==internal-object-stress penalty== (top-10% + mean particle stress) to the reward, with human demos, ==rigid-to-soft curriculum==, and DR; zero-shot sim-to-real handles real tofu undamaged, **100%** foam pick-up at **10%** vs naive RL's **41.9%** water loss.

#### 3.4 Vision-Aware Sim-to-Real

Close the *visual* gap explicitly via neural rendering, teacher-student distillation, or controller-aware system-id.

- **[[2511.15200|VIRAL]]** — A visual sim-to-real framework at scale for humanoid loco-manipulation built on ==two-phase teacher-student== learning — a privileged RL teacher distilled into a vision student via DAgger + BC with **64-GPU** ==tiled rendering==; **54/59** cycles on real Unitree G1, matching expert teleop; ablating ==Reference State Initialization== drops success **95% → <10%**.
- **[[2604.11138|ViserDex]]** — A monocular-RGB dexterous-reorientation method that puts ==3D Gaussian Splatting== *in the simulation loop*, where ==pre-rasterization augmentation== applies DR to 3DGS attributes for diverse lighting + materials; **37.6** reorientations on real Allegro Hand, **~25** adversarial; single GPU, **1.6×** faster than tiled rendering.
- **[[2604.02523|Tune to Learn]]** — An MIT study of how *controller gains* shape sim-to-real, using ==Torque-to-Position Retargeting== to isolate gain effects; ==stiff/overdamped gains== yield *lowest* sysid errors but *worst* transfer, while for BC ==compliant overdamped gains== win despite higher training loss; RL reaches **99%+** under *any* regime — low sysid error does *not* track transfer.
- **[[2601.02778|Force-Based Sim2Real]]** — A sim-to-real RL framework for zero-shot force-aware manipulation on a real 5-finger hand via ==asymmetric actor-critic PPO== in ==IsaacLab==; a ==distance-field tactile sim== maps touch to force features, plus ==current-to-torque calibration== + a randomized actuator; in-hand rotation reaches **25.1** *with* tactile vs **1.1** *without*.
- **[[2512.04731|S2GS]]** — A ==Semantic 2D Gaussian Splatting== representation extracting ==object-centric, domain-invariant spatial features== via feature-level splatting + ==semantic retrieval== (CLIP/SAM) to filter background, fed to a ==Diffusion Policy==; **86.7%** Pick/Push and **80.0%** Stack zero-shot sim-to-real on unseen objects, **+2.46 dB** PSNR over 3DGS.
- **[[2505.00991|DexCtrl]]** — An adaptive-controller-learning framework that jointly predicts actions (==self-attention==) and ==controller parameters== (==cross-attention==) from trajectory history, with oracle-to-student sim distillation; params adapt to object properties (stiffer for heavier), beating fixed-tuning on real LEAP-hand in-hand rotation without retraining.
- **[[2502.14457|Watch Less, Feel More]]** — A sim-to-real RL method for articulated objects that uses vision only for the initial grasp then switches to ==proprioception + interaction history==, with ==online policy distillation== inferring hidden object properties and ==learnable variable impedance==; **80%/84%** zero-shot on unseen doors/drawers, impedance lifting OpenDoor **40% → 80%**.

#### 3.5 Humanoid & Legged Sim-to-Real

Whole-body and legged robots cross the gap via teacher-student distillation, staged RL curricula, and physics-driven retargeting — the depth-conditioned student observes the same modality it deploys with.

- **[[2604.26504|HiPAN]]** — A two-level ==hierarchical RL== (goal-seeking + posture-adaptive locomotion) for quadruped navigation in unstructured 3D scenes via teacher-student + DR; ==Path-Guided Curriculum Learning== + intrinsic reward beat long-horizon myopia, posture commands enable confined-space traversal; **94.7%** SR / **83.6** SPL on Complex-2, on Unitree Go1 from depth only.
- **[[2603.03279|ULTRA]]** — A ==Physics-driven neural retargeting== method translating MoCap into contact-aware humanoid demos; a single ==multimodal controller== with ==transformer encoder== + ==availability masking== handles dense and sparse goals; ==teacher-student distillation== + RL lifts OOD-goal success up to **200%**; **73%** dense-tracking, **50-90%** sparse-following on Unitree G1.
- **[[2508.10538|MLM]]** — A multi-task RL framework giving a quadruped-plus-arm one whole-body loco-manipulation policy via an ==asymmetric actor-critic== + ==Trajectory-Velocity Prediction== net (NAE foresight + memory-encoder velocity) and ==adaptive curriculum sampling==; with extensive DR it zero-shot transfers to a real quadruped at up to **85%** across teleop and autonomous tasks.
- **[[2502.12152|HUMANUP]]** — A ==Two-stage RL curriculum== for humanoid fall recovery: Stage I Discovery Policy on simplified sim, Stage II Deployable Policy on full ==URDF== with **20,000** postures + diverse-terrain DR; Unitree G1 recovers from supine at **78.3%** / rolls over at **98.3%** across **6 terrains** in **~6s** (vs **11s**); *separating discovery from refinement* is critical.
- **[[2502.10894|UAN]]** — An ==Unsupervised Actuator Net== bridging the *actuation* gap for athletic loco-manipulation: it predicts corrective torques to close the sim-real gap *without* torque sensors, paired with a two-stage WBC pre-train→fine-tune pipeline; the real Unitree B2+arm throws objects **~20 m**, lifts **8 kg**, drags a **113 N** cart — sim-to-real of the actuator model.
- **[[2502.01143|ASAP]]** — A sim-real physics alignment for *agile* humanoid whole-body skills: pre-train motion-tracking on retargeted human video, learn a ==delta-action model== on real data that residually corrects nominal sim actions, then fine-tune inside the *aligned* simulator; on Unitree G1 reduces tracking error up to **52.7%** — closes unmodeled dynamics beyond SysID/DR.
- **[[2212.07740|TERT]]** — A ==Terrain Transformer==: a GPT-like transformer student predicting teacher actions directly from proprioceptive history (no latent-vector estimation), trained two-stage (offline distillation → online correction) over heavy DR in Isaac Gym; on a real Unitree A1 it hits **100%** on sand pits and **60%** on stairs where the TCN-based RMA baseline scores **0%**.
- **[[2403.16967|VBC]]** — A ==hierarchical== visual whole-body-control framework for legged loco-manipulation: a low-level RL policy tracks EE + body-velocity goals in a height-invariant frame while a ==privileged teacher== is ==DAgger==-distilled into a segmented-depth visuomotor student; zero real-world data, robust sim-to-real on a real Unitree B1+Z1 grasping at 0.0/0.3/0.5 m heights.
- **[[2107.04034|RMA]]** — The canonical ==Rapid Motor Adaptation== recipe: a base RL policy conditioned on a privileged ==extrinsics vector==, plus an adaptation module regressing that vector online from proprioceptive history alone (100 Hz base / 10 Hz adapter); a Unitree A1 crosses sand, mud, and slippery floors with **12 kg** payload, zero real-world fine-tuning.
- **[[2510.07094|Universal Quadruped Sampling]]** — A universal locomotion controller (==asymmetric actor-critic== + morphology estimator) studying how to sample ==morphology and joint PD gains==, with a novel ==adaptive particle-filter curriculum==; enables zero-shot deployment on real ANYmal (**0.09-0.11 m/s** RMSE) without unsafe PD gains where baselines fail.
- **[[2507.04039|ROLT]]** — A ==Robust Locomotion Transformer== whose architecture targets OOD dynamic + perceptual gaps via ==Body Tokenization== (action token enabling cross-limb knowledge transfer for fault tolerance) and ==Consistent Dropout==; zero-shot real Unitree Go1 across weakened limbs, box-dragging, and roller-skates, beating RMA.
- **[[2505.14266|Sampling-Based SysID]]** — A sampling-based ==system identification== framework (SPI-Active) for legged sim2real that minimizes real-vs-sim trajectory discrepancy, then adds ==Fisher-Information-guided active exploration== to collect informative trajectories — *no* differentiable physics or torque sensors; **42-63%** policy improvement on real Go1 quadruped and H1 humanoid.

#### 3.6 Domain Adaptation & Continual Transfer

Align the source/target distributions or keep adapting after deployment — without joint data access or catastrophic forgetting.

- **[[2606.06218|TAM]]** — A policy-agnostic ==torque-interface residual module== corrects nominal torque commands via ==multi-robot sim pretraining== then per-robot fine-tune, with an async ==History Encoder== conditioning a 1 kHz ==Torque Adaptor==; real Franka pushing **47.6%→76.2%**, BC flipping **50.0%→72.0%**, **>60%** EE-RMSE cut, zero-shot to Google Robot (**1.05°** vs **4.69°**).
- **[[2605.23733|Any2Any]]** — A cross-*embodiment* transfer framework for pre-trained humanoid whole-body-tracking policies: ==kinematic alignment== (coupling matrices remap obs+action spaces) then ==LoRA== dynamic adaptation reuses motor priors across LimX Oli/Luna + Unitree G1/H1 at only **~1%** of from-scratch compute and data, with comparable-or-better tracking.
- **[[2602.18025|Cross-Embodiment Offline RL]]** — An offline-RL method exploiting *heterogeneous, suboptimal* multi-robot data: morphology-agnostic ==URMA== + ==IQL==, plus ==Embodiment Grouping== (==Fused Gromov-Wasserstein== clustering + group-wise actor updates) to kill inter-robot gradient conflicts; **+33.99%** over standard cross-embodiment IQL on 70%-suboptimal data (r=**0.815**).
- **[[2509.18631|Sim-Real OT Co-Training]]** — A generalist co-training framework over abundant sim + sparse real demos where ==Unbalanced Optimal Transport== aligns the *joint* observation-action distribution across domains, with ==Dynamic-Time-Warping== sampling; **0.73** image / **0.77** point-cloud real SR, generalizing to novel textures (BoxInBin **0.7**, Stack **0.4**) unseen in the demos.
- **[[2506.08460|MOBODY]]** — A model-based *off-dynamics* offline-RL method for mismatched dynamics that learns ==target dynamics== (shared state encoder + separate source/target action encoders), rolls out the policy for fake transitions, and optimizes with ==target-Q-weighted behavior cloning==; **+44%** over the best baseline across 32 MuJoCo gravity/friction-shift tasks.
- **[[2503.10949|SCDA]]** — A safe *continual* domain-adaptation framework for post-transfer drift where DR pretraining + ==PCRPO== safe RL + ==Elastic Weight Consolidation== let a deployed policy keep adapting to real drift without catastrophic forgetting; on real grasping it lifts SR **20% → 60%** while holding **zero** safety violations — where reward-only adaptation turns unsafe.
- **[[2407.13771|Training-Free Model Merging MTDA]]** — A training-free merge building one generalist from many single-target ==STDA== adapters with *no* joint data access, via ==linear mode connectivity== (parameter averaging + ==Gaussian BatchNorm-statistic merging==). Matches combined-data training on multi-target driving segmentation and *outperforms* prior consistency-training MTDA.
- **[[2602.20220|Sim-to-Online RL]]** — An empirical study (100+ runs, 3 platforms) of sim-trained policies fine-tuned ==online via off-policy SAC== on real robots, isolating what stabilizes it: ==retaining sim + past real data==, ==warm-start buffers==, and ==asymmetric actor-critic updates== (delayed actor, smaller LR) prevent the downward spiral across manipulation, locomotion, navigation.
- **[[2602.12628|RL-Co]]** — A ==RL-based sim-real co-training== framework for VLAs: ==SFT== on real + sim demos initializes the policy, then ==RL in simulation== refined by ==ongoing real-data SFT== prevents domain drift; real SR rises to **64.0%** (OpenVLA) and **66.2%** (π0.5), with stronger OOD robustness and data efficiency.
- **[[2601.16212|Point Bridge]]** — A cross-domain framework distilling observations into ==domain-agnostic 3D point representations== (==VLM== scene filtering + ==Foundation Stereo== depth) trained on synthetic data with a ==multi-task transformer policy==; **39-44%** zero-shot sim-to-real gain, **97%** held-out-object SR, and **+30%** from 45 real co-train demos.

**Policy-Side — Decision Matrix**

| Need | Recommendation |
|---|---|
| Industrial-default dexterous reorientation (DR baseline) | [[2210.13702\|DeXtreme]] — VADR doubles real-world transfer (**27.8** vs **14.8**) |
| Train from imperfect demo priors at industrial assembly scale | [[2603.15956\|ExpertGen]] — diffusion prior + DSRL + DAgger; **90.5%** avg AutoMate |
| Real-world residual learning without human supervision | [[2602.23253\|SPARR]] — Pattern A+C hybrid; **95-100%** AutoMate, **+74.5%** unseen NIST |
| Full-stack dexterous humanoid recipe (Fourier GR-1) | [[2502.20396\|Humanoid Sim2Real Dex]] — autotuned modeling + contact stickers; **80%** box-lift |
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
| Question whether stiff/compliant gains improve transfer | [[2604.02523\|Tune to Learn]] — compliant overdamped gains beat stiff for BC; sysid ≠ transfer |
| Zero-shot force-aware dexterous in-hand rotation | [[2601.02778\|Force-Based Sim2Real]] — distance-field tactile + current-to-torque cal; **25.1** rotations w/ tactile |
| Quadruped navigation in unstructured 3D from depth-only | [[2604.26504\|HiPAN]] — hierarchical RL + path-guided curriculum; **94.7%** Complex-2 |
| MoCap-to-humanoid retargeting with sparse/dense goal support | [[2603.03279\|ULTRA]] — multimodal controller + availability masking; **73%** dense-tracking G1 |

> [!star] Key Papers
> - [[2210.13702|DeXtreme]] — Foundational VADR result: automatic DR doubles real-world transfer (**27.8** vs **14.8** reorientations); the canonical industrial sim-to-real recipe
> - [[2511.15200|VIRAL]] — Visual sim-to-real at scale for humanoid loco-manipulation; **54/59** real Unitree G1 success matching expert human teleop; RSI is critical
> - [[2506.12851|KungfuBot]] — Physics-feasible motion processing + adaptive tracking; **53.25 mm** error vs **>233 mm** baselines; first to zero-shot transfer highly-dynamic skills
> - [[2604.24916|asRoBallet]] — Friction-aware [MuJoCo](https://mujoco.org) + RL closes sim2real gap for underactuated dynamics; **zero-shot** ballbot whole-body control with **0.05 m/s** real-world MAE

> [!tip] Domain Randomization is the Default — But Has Limits
> Every paper in this section uses DR, but [[2604.11674|AffordSim]] showed DR alone only lifts real-world success from **17%** to **27%** on affordance-demanding tasks — fine-grained semantic transfer still fails. DR works for *dynamics* gaps ([[2210.13702|DeXtreme]], [[2506.12851|KungfuBot]]) but is *brittle* for *semantic* gaps (manipulating novel categories). Combine DR with neural rendering ([[2604.11138|ViserDex]]) or learned simulators ([[2310.06114|UniSim]]) when the visual gap dominates.

> [!success] The Modern Policy-Side Recipe
> ==Auto domain randomization== + ==teacher-student distillation== + ==reference state initialization== + ==system identification== + ==privileged-info asymmetric actor-critic== — proven across [[2210.13702|DeXtreme]], [[2511.15200|VIRAL]], [[2506.12851|KungfuBot]], and [[2603.15956|ExpertGen]]. Pick a subset based on which gap (dynamics, visual, kinematic) dominates your deployment.

---

### 4. Real2Sim2Real Loops & Digital Twins

Reverse the direction: reconstruct the *deployment* scene as a high-fidelity interactive simulator, train the policy *against the twin*, then execute on the real robot. Eliminates the visual long tail because the simulator is *grounded* in the deployment environment from the start.

#### 4.1 Video → Interactable Sim

Reconstruct the *deployment* scene as a simulatable twin from one or a few real videos.

- **[[2606.12604|EgoEngine]]** — A pipeline turning egocentric human videos into high-fidelity dexterous robot demos via an object-centric ==digital twin==, a visual branch that inpaints humans out and renders a robot in, and ==adaptive multi-solver (Replay/MPC/RL)== retargeting of hand motions; **83%** TACO, **90%** Aria, and zero-shot real beats teleoperation (**60%** vs **25%** on Hammer).
- **[[2606.08828|Video2Sim2Real]]** — A full-stack pipeline acquiring dexterous skills from a single human video via an autonomous ==digital twin== + ==object-centric keyframe refinement==, then a ==decoupled sim-to-real== split — IL for keyframe-pose geometry + residual RL for local finger physics; **91.4%** sim / **95.7%** real avg across 7 tasks vs pure IL/RL's 3-**45.7%**.
- **[[2512.14696|CRISP]]** — A real-to-sim pipeline turning monocular human-scene-interaction video into sim-ready assets via ==normal-based planar-primitive fitting== + ==contact-guided scene completion== (InteractVLM infers occluded surfaces) + an RL motion-tracking validity check; **93.1%** real-to-sim success (vs VideoMimic **44.8%**) at **23K** FPS (**43%** faster RL throughput).
- **[[2511.07416|PhysWorld]]** — A digital-twin pipeline chaining ==Task-conditioned video generation== → ==geometry-aligned 4D reconstruction== → physical twin → ==object-centric residual RL== inside the twin; **82%** avg success across **10** real-world tasks, **+15 pp** over RIGVid; cuts grasping failures **18% → 3%**; the explicit physical world model is what makes generated video actionable.
- **[[2504.03597|Real-is-Sim]]** — A digital twin made the policy's *sole interface*, mirrored by the real robot: an ==Embodied Gaussians== twin syncs via **60 Hz** RGB while the policy (==Conditional Flow Matching==) reads/writes *only* the sim; 30+30 demos lift state-based PushT **57% → 80%**, virtual cameras reach **82%** — unlike [[2503.17973|PhysTwin]]/[[2511.07416|PhysWorld]].
- **[[2503.17973|PhysTwin]]** — A reconstruction of ==physics-informed interactive digital twins== of *deformable* objects from videos; multi-stage optimization jointly recovers geometry, physical properties, and appearance via ==spring-mass models== + ==generative shape priors== + ==Gaussian splats==; real-time sim drives motion planning — lifts videos into simulatable physics.
- **[[2404.09833|Video2Game]]** — A real2sim pipeline turning a single video into a real-time browser-compatible interactive 3D environment with physics; enhanced ==Instant-NGP== distilled to ==game-engine-compatible mesh + neural texture map==, decomposed into entities with ==rigid-body physics==; **>100 FPS** browser rendering; monocular 2D priors regularize NeRF from sparse video.

- **[[2403.03949|RialTo]]** — A ==Real-to-sim-to-real pipeline== building task-specific digital twins of articulated scenes; ==inverse distillation== transfers real imitation policies into sim, then ==PPO+IL== + ==teacher-student distillation== refine them; **91%** object-pose, **77%** distractors, **75%** disturbances (**2.5×** vs imitation); target twins give **90%** vs generic **10%**.
- **[[2606.17520|GASE]]** — A ==3D Gaussian Splatting== automated reconstruction system using panoramic multi-view streams and a ==2D-domain object-scene decomposition== for accurate masks + background inpainting; decouples static collision-mesh background from manipulable foreground objects, reaching **>10%** higher mIoU and a **<10%** sim-to-real manipulation gap.
- **[[2606.15338|SimWeaver]]** — A deformable-manipulation sim-to-real system pairing a robust simulator (==active-collision-region scheme==) with a ==topology-aware trajectory synthesizer== and a real protocol of ==cloth-state randomization== + ==sensor-aware photometric augmentation==; **91.30%** avg zero-shot RGB sim-to-real from 200 sim demos at **$0.03**/trajectory.
- **[[2603.14010|URDF-Anything+]]** — An end-to-end ==autoregressive diffusion== framework generating simulation-ready URDF (==part geometry== + ==kinematic structure==) from a single RGB image via a shared ==Diffusion Transformer== latent; Part IoU **0.879** and zero-shot **100%/90%** laptop/drawer sim-to-real in a ==Real-Follow-Sim== paradigm.
- **[[2601.03200|3DGS Digital Twin]]** — A ==3DGS==-based digital-twin pipeline (==InstantSplat==) with ==multi-view semantic fusion== + three-stage ==geometric cleaning== (filtering, connectivity pruning, watertight Alpha-Shape meshing) into planning-ready collision geometry; **229 s** reconstruction (**5×** faster than NeRF), **90%** real zero-shot pick-and-place, zero collisions.
- **[[2602.02402|SoMA-Sim]]** — A real-to-sim *neural* simulator for soft-body manipulation representing objects as ==hierarchical 3D Gaussian Splats== whose dynamics are driven by environmental + robot-induced ==forces== via neural interaction modules, with ==multi-resolution training== for long-horizon stability; **+20%** resim accuracy and PSNR **33.51** vs PhysTwin's **28.77**.
- **[[2511.20348|Material-GS]]** — A camera-only ==3D Gaussian Splatting== digital-twin pipeline with ==monocular material extraction== (RMSNet + FastSAM) projected to mesh surfaces as ==PBR textures== for physics-based sensor simulation; matches LiDAR-camera-fusion reflectivity accuracy (MAE **10.05** vs **10.14**) from cameras alone.
- **[[2510.20813|GSWorld]]** — A closed-loop photorealistic suite integrating ==3D Gaussian Splatting== with physics engines via a portable ==Gaussian Scene Description File (GSDF)== and a marker-based real-to-sim reconstruction pipeline; **68%/52%** zero-shot sim2real, and ==automated DAgger== in sim lifts Place-Box **68% → 76%**.
- **[[2510.10637|High]]** — A real2sim2real data generator (RoboSimGS) with hybrid scene representation (==3DGS== backgrounds + explicit interactive meshes) where ==MLLMs (GPT-4o)== auto-infer articulation and physical material properties from renders; zero-shot transfer across eight real tasks and **>10,000** demos/day on one GPU.
- **[[2502.08645|Re3Sim]]** — A real-to-sim-to-real pipeline reconstructing scenes with ==hybrid rendering== (ray-traced foreground meshes + ==3DGS== background) and marker/ICP alignment for large-scale data generation; **>58%** avg real zero-shot SR with a strong **0.924** sim-real Pearson correlation, reconstructing scenes in under a minute.
- **[[2502.08643|IKER]]** — A real-to-sim-to-real framework (IKER) where ==VLMs generate iterative keypoint reward== functions, a ==scene transfer== (BundleSDF mesh + FoundationPose) builds faithful sim, and ==PPO + DR== trains transferable policies; enables multi-step tasks, disturbance recovery, on-the-fly replanning (**0.7** Shoe-Place vs **0.3**).

#### 4.2 Differentiable Real2Sim Calibration

Replace manual system-id with gradient descent on simulator parameters.

- **[[2604.27367|DOT-Sim]]** — A differentiable optical-tactile simulator calibrated to real soft sensors where a ==Material Point Method== models gel deformation, ==differentiable physics== calibrates material params, and a neural ==residual image== adds optical fidelity; **PSNR 30.48** (**+17.34%**) and zero-shot **90.5%** indenter, **96.6%** tumor detection, **0.896 mm** trajectory error.
- **[[2508.12252|Robot Trains Robot]]** — A *latent* dynamics-calibration method replacing explicit param calibration: a compliant arm teacher supplies ==F/T reward signals== + autonomous resets, then a three-stage pipeline refines a ==FiLM-conditioned dynamics latent== to fit real dynamics; humanoid doubles walking speed in **20 min**, learns swing-up in **15 min**.
- **[[2603.01151|D-REX]]** — A ==differentiable real-to-sim-to-real engine== that reconstructs ==Gaussian Splats== and identifies ==object mass== via differentiable physics (minimizing real-vs-sim pushing-trajectory discrepancy), then trains mass-conditioned force-aware grasping from human videos; mass error **4.8-12.0%**, **86%** real grasping (vs DexGraspNet 2.0 **76%**), beating DR on OOD mass.
- **[[2512.19390|TwinAligner]]** — A Real2Sim2Real system with a ==Mesh-GS digital twin== (3DGS rendering + SDF/mesh collision) and ==visual-dynamic alignment== fitting viewpoint + rigid physics (friction, mass, CoM, controller) via ==gradient-free optimization== robust to rendering error; PSNR **38.03**, ADD **1.39 cm**, strong zero-shot transfer plus trustworthy cross-environment evaluation.
- **[[2506.15680|Particle-Grid Neural Dynamics]]** — A hybrid ==Lagrangian-Eulerian particle-grid== framework learning deformable-object dynamics directly from real RGB-D video (SAM + CoTracker tracks), bypassing sim-to-real material-ID; outperforms MPM and GNN baselines on rollout accuracy, robust to single-view partial observation, and improves MPC manipulation of cloth and rope.
- **[[2506.04120|Splatting Physical Scenes]]** — An end-to-end ==differentiable== real-to-sim pipeline introducing ==SplatMesh== (triangle meshes + surface-constrained 3D Gaussians) that jointly optimizes geometry, camera extrinsics, and robot joint angles via differentiable rendering + ==MuJoCo MJX== physics from imperfect data; CD cut **18.92 → 7.35 mm** on real ALOHA 2.
- **[[2504.16693|PIN-WM]]** — A Real2Sim2Real method (PIN-WM) learning a ==physics-informed world model== of 3D rigid-body dynamics + appearance end-to-end from few-shot video via ==differentiable physics (LCP)== + ==2D Gaussian Splatting==, then trains policies on ==physics-aware digital cousins==; **97%/83%** sim and **75%/65%** real push/flip from a single sysid trajectory.
- **[[2503.10118|RSR Loop]]** — An iterative ==Real-Sim-Real loop== that tunes ==differentiable simulation parameters== (MuJoCo MJX ==L_physical== loss) and the policy together, with an ==Adaptive InfoGap Loss== mitigating data-collection bias; KL divergence between real and sim block-pushing trajectories drops from **16.3/36.3** to **<1** by the 4th iteration.

#### 4.3 World-Model-Driven Online Adaptation

Treat the sim-real gap as an OOD shift the world model detects, then fine-tune online.

- **[[2603.04029|Self-Adapting RL]]** — An online continual-RL framework with world-model feedback; built on ==[[2301.04104|DreamerV3]]==, ==Observation== + ==Reward Prediction Residuals== trigger online world-model + policy fine-tuning; Walker adapts to actuator damage in **10,000 steps** (**2 min**); F1Tenth adapts to *both* sim-real gap *and* friction drop in **10,000 real steps** (**8 min**).
- **[[2603.13825|Explicit-WM Manipulation]]** — A zero-shot open-world manipulation framework via on-demand digital twins; ==open-set segmentation== (Grounded-SAM) + ==grasp pose prediction== (AnyGrasp) → ==digital twin== (Hunyuan 3D 2.0) + ==two-stage pose alignment== ([[2304.07193|DINOv2]] + RANSAC/ICP) → physics sampling; **6/9** at **≥75%**; alignment lifts mug-handling **27% → 91%**.

#### 4.4 Compositional Sim-Real Environments

Use sim as a safety filter, not a training source.

- **[[2604.05484|CoEnv]]** — A multi-agent-collaboration framework via ==compositional environment== unifying scene reconstruction with a physics simulator; ==VLM-based hierarchical planner== decomposes tasks; ==collision-aware sim-to-real transfer== verifies swept collision volumes before execution; **49%** across **5** real multi-agent benchmarks; sim is the *safety filter*, not training source.

**Real2Sim2Real — Decision Matrix**

| Need | Recommendation |
|---|---|
| Generate physical digital twin from a single task-conditioned video | [[2511.07416\|PhysWorld]] — video → 4D recon → physical twin → residual RL; **82%** real across 10 tasks |
| Make the sim the policy's **sole** interface, real robot mirrors sim | [[2504.03597\|Real-is-Sim]] — Embodied Gaussians + 60Hz visual sync; eliminates sim-real gap from policy POV |
| Deformable-object twin from video (cloth, rope, soft objects) | [[2503.17973\|PhysTwin]] — spring-mass + Gaussian splats; real-time interactive sim |
| Browser-deployable interactive 3D environment from one video | [[2404.09833\|Video2Game]] — Instant-NGP + neural texture + rigid-body physics; **>100 FPS** browser |
| Calibrate optical tactile sim to real sensor via gradients | [[2604.27367\|DOT-Sim]] — differentiable MPM + residual rendering; **96.6%** zero-shot tumor detection |
| Online continual RL adapting to sim-real gap as OOD shift | [[2603.04029\|Self-Adapting RL]] — [[2301.04104\|DreamerV3]] residual triggers; **2 min** Walker, **8 min** F1Tenth |
| Zero-shot open-world manipulation via on-demand twins | [[2603.13825\|Explicit-WM Manipulation]] — Grounded-SAM + Hunyuan + [[2304.07193\|DINOv2]] two-stage alignment; **27→91%** mug-handling |
| Multi-agent collaboration with sim as safety filter | [[2604.05484\|CoEnv]] — compositional env + collision-aware verification; **49%** across 5 multi-agent benchmarks |

> [!star] Key Papers
> - [[2503.17973|PhysTwin]] — Physics-informed deformable digital twins from videos; real-time interactive sim + motion planning integration
> - [[2511.07416|PhysWorld]] — **82%** real-world success across 10 tasks via task-conditioned video → physical digital twin → object-centric residual RL; explicit physics is what makes generated video actionable
> - [[2504.03597|Real-is-Sim]] — Embodied-Gaussians digital twin as the policy's **sole interface**; the real robot mirrors the sim instead of vice-versa, eliminating the sim-real gap from the policy's perspective; +23pp PushT with 30+30 demos
> - [[2404.09833|Video2Game]] — Single video → **100+ FPS** browser-compatible interactive environment with rigid-body physics; foundational real2sim pipeline
> - [[2604.27367|DOT-Sim]] — Differentiable MPM + residual rendering for optical tactile sensors; **96.6%** tumor detection zero-shot

> [!tip] When Real2Sim2Real Wins
> Digital twins win when your *deployment scene matters most* — a specific robot, a specific workspace, a specific deformable target. They lose when you need *broad generalization across scenes*, where learned simulators ([[2310.06114|UniSim]], [[2501.03575|Cosmos]]) or large-scale procedural generation ([[2603.16861|MolmoBot]]) scale better. The decision: how variable is your deployment environment?

---

## Part C — Evaluation, Integration & Open Problems

*Measuring the gap, combining the three strategies, and what is still unsolved.*

### 5. Evaluation & Reality-Gap Measurement

You cannot optimize what you cannot measure. The reality-gap evaluation stack went from absent (pre-2024) to the determining factor for whether a sim-to-real claim is publishable (2026).

#### 5.1 Sim-Real Correlation Benchmarks

Quantify how well sim predicts real — the prerequisite for any publishable sim-to-real claim.

- **[[2606.10366|Sim-Real VLA Eval]]** — A correlation recipe quantifying when sim predicts real VLA performance, sweeping 3 benchmarks × 5 policies under matched ==vision/language/layout/behavior perturbations== on DROID; REALM wins (**ρ=0.700**, **MMRV=0.030**), and ==simulator-based post-training== lifts ranking **ρ 0.700→0.875** at a 10-demo data optimum.
- **[[2605.06311|VISER]]** — A correlation benchmark pushing realism with ==ray tracing== and ==physically-based rendering (PBR)== materials, while an ==MLLM-driven asset pipeline== generates **>1,000** 3D assets *without* baked-lighting artifacts; **r = 0.92** avg Pearson sim-real correlation; ==specular highlights== and ==contact shadows== are the *load-bearing cues* current VLAs depend on.
- **[[2512.16881|PolaRiS]]** — A scalable real-to-sim correlation benchmark for *generalist* policies whose automated ==2D Gaussian Splatting== pipeline rebuilds interactive scenes from short monocular scans + ==TRELLIS== objects + a policy-agnostic co-train; **r = 0.9** avg Pearson sim-real (up to **0.98** vs RoboArena), beating Libero-Score and Ctrl-World, at **<20 min** human effort per scene.
- **[[2511.04665|Real-to-Sim GS]]** — A *deformable-object* sim-real correlation framework (where [[2405.05941|SimplerEnv]] / [[2605.06311|VISER]] lose fidelity) coupling ==3D Gaussian Splatting== + soft-body twins ([[2503.17973|PhysTwin]]); optimizes params with ==color alignment== + **NVIDIA Warp** physics; **r > 0.9** across plush packing, rope routing, T-block — vs **IsaacLab r=0.649**.
- **[[2405.05941|SimplerEnv]]** — The first benchmark for *reliable* sim-real correlation across Google Robot + BridgeData V2; it closes the control gap via ==system identification==, the visual gap via ==green screening== + ==texture baking==; Pearson **r > 0.85** Google Robot, **r = 0.890** BridgeData V2; introduces ==Mean Maximum Rank Violation (MMRV)== — whether sim correctly *ranks* policies.

#### 5.2 Diagnostic Benchmarks for Specific Sim-to-Real Failures

Decompose the gap into specific failure modes that single-metric benchmarks miss.

- **[[2604.10856|BridgeSim]]** — A cross-simulator closed-loop evaluation suite that decomposes the OL-CL gap into ==Observational Domain Shift== + ==Objective Mismatch==; a training-free ==Test-Time Adaptation== combines a ==flow-matching calibrator==, ==truncated Q-value estimator==, and ==adaptive replan==; **+19.1** Driving Score with [[2305.14992|RAP]]; *scaling OL does not improve CL*.
- **[[2510.23571|RobotArena Infinity]]** — A scalable benchmarking system via ==real-to-sim translation==: single-view robot video → re-executable sim with reconstructed objects + calibrated dynamics, scored by a ==dual VLM-guided + human-preference== protocol (Bradley-Terry over **8,500+** judgments) and perturbed along background/color/pose; six open VLAs drop sharply under OOD shift.
- **[[2506.18088|RoboTwin 2.0]]** — An automated expert-data generator via ==MLLMs== + ==closed-loop simulation-in-the-loop feedback==, applying ==domain randomization== across **5** dimensions (clutter, textures, lighting, heights, paraphrases) + ==embodiment-aware grasp adaptation==; **+24.4%** real-world few-shot, **+21.0%** zero-shot unseen-background generalization.
- **[[2509.15273|Embodied Arena]]** — A unified platform integrating **22+** benchmarks and **30+** models; ==Embodied Capability Taxonomy== with **7** core capabilities and **25** fine-grained dimensions; ==LLM-driven automated data generation== prevents overfitting; specialized models beat closed-source generalists; *object and spatial perception are the dominant bottlenecks*, not reasoning.
- **[[2501.16389|Sim2Real Encoder Eval]]** — An *offline* framework diagnosing which pretrained vision encoder will transfer, via two metrics: ==Domain Invariance Score== (sim↔real embedding alignment) + ==Action Score== (task-relevant features); encoders pretrained on manipulation data (MCR) top both, beating generic backbones — pick the encoder before training the policy, not after.
- **[[2606.18594|Action-Space Bench]]** — A systematic benchmark of four ==action-space representations== (pose/joint × increment/velocity) for vision-based ==PPO== manipulation, evaluating zero-shot sim-to-real on a real Franka; ==joint velocity== gives **100%** real picking with low jerk where Cartesian pose-velocity fails entirely — sim SR does not predict real transfer.
- **[[2603.22876|Grounding Sim-to-Real]]** — A factorized empirical study (10,000+ real trials, OpenVLA-OFT on RoboTwin 2.0) isolating which sim-to-real factors matter for dexterous VLA generalization; ==spatial domain randomization== (camera pose, table height) dominates appearance, ==frame-wise== beats episode-wise DR, and RL + comprehensive DR lifts real SR **5.6% → 42.8%**.
- **[[2602.00678|RoboGauge]]** — A predictive assessment suite measuring ==sim-to-real transferability== via ==sim-to-sim metrics== in MuJoCo across terrains/difficulties/DR, paired with a ==MoE== proprioception-only locomotion policy; RoboGauge tracks real ground truth (error **0.0873**) better than IsaacGym metrics, enabling **4.01 m/s** robust real Go2 locomotion.
- **[[2508.11117|Robot Policy Eval (Sim2Real)]]** — A benchmarking framework for generalist-policy sim-to-real transferability using ==high-fidelity IsaacLab== sim, a four-level ==task-complexity taxonomy==, ==five perturbations== (lighting, texture, camera pose, placement), and graded metrics including explicit sim-to-real matching; finds policies highly vulnerable to minor perturbations.
- **[[2505.17966|Single-View Mesh for Robotics]]** — An empirical study defining ==five robotics desiderata== (<2 mm Chamfer, no collisions, <5° stability, occlusion robustness, <2 s) and testing 12 single-view mesh-reconstruction models on YCB-Video + Aria; most exceed **5 mm** error with colliding, unstable meshes and **~50%** grasp transfer — digital twins are not yet robotics-ready.

#### 5.3 Sim-Real Estimation as a Statistical Problem

Reframe sim-to-real as variance reduction across a portfolio of biased simulators.

- **[[2604.24018|Sim2Real Betting]]** — A ==Sequential betting framework== where simulators inform strategic wagers via a ==bet-weighted estimator==; ==Cover's universal portfolio== with ==Kelly-style bet sizes== combines diverse simulators and ==double betting== tolerates bias; **70-100%** win rates (lower error than Monte Carlo); sim-to-real is *variance reduction*, not *fidelity*.
- **[[2512.05024|Simulator Fidelity Quantile Curves]]** — A ==model-free== framework profiling the sim-to-real gap as a *distribution*, constructing a ==calibrated quantile curve== of per-scenario ==pseudo-discrepancy== over rigorous confidence sets with high-probability upper-bound guarantees; treats the gap as a random variable rather than a scalar, validated on LLM simulators.
- **[[2506.20553|Sim2Val]]** — A variance-reduced real-metric estimator applying classical ==control variates== over paired real+surrogate and abundant surrogate-only samples, with a learned ==Metric Correlator Function== boosting weak correlation; **up to 82.9%** variance reduction and **51-58%** fewer real samples for the same confidence across driving + quadruped.
- **[[2503.05696|MFPG]]** — A ==Multi-Fidelity Policy Gradients== framework treating cheap sim as a low-fidelity ==control variate== for scarce high-fidelity data, with a ==policy reparameterization trick== correlating cross-fidelity trajectories for an unbiased variance-reduced gradient; beats high-fidelity-only in **8/8** dynamics-gap scenarios, robust to anti-correlated low-fidelity rewards.

#### 5.4 Interactive World-Model Evaluation

Make heterogeneous interactive simulators comparable on the same axis.

- **[[2604.21686|WorldMark]]** — A unified benchmark for *interactive* I2V world models whose ==unified action-mapping layer== maps WASD-style vocabulary to each model's native control; **500** cases, **8** metrics in **3** dimensions; Spearman **ρ > 0.9** with human judgments; visual quality and world consistency are *uncorrelated* ([[2402.15391|Genie]] 3 leads consistency, YUME 1.5 quality).

**Evaluation — Decision Matrix**

| Need | Recommendation |
|---|---|
| Reliable rigid-object sim-real correlation + policy *ranking* | [[2405.05941\|SimplerEnv]] — Pearson **r > 0.85**, **MMRV** for rank-violation diagnostics |
| Pinpoint *which visual cues* drive sim-real correlation | [[2605.06311\|VISER]] — ray-traced PBR; **r = 0.92**; identifies specular highlights / contact shadows |
| Deformable-object (cloth, rope, soft) sim-real correlation | [[2511.04665\|Real-to-Sim GS]] — 3DGS + [[2503.17973\|PhysTwin]]; **r > 0.9** across plush / rope / T-block |
| Decompose OL-CL gap into observation shift vs Q-mismatch | [[2604.10856\|BridgeSim]] — flow-matching TTA + truncated Q + adaptive replan; **+19.1 DS** |
| Automated expert-data generation with DR across 5 dims | [[2506.18088\|RoboTwin 2.0]] — MLLM + closed-loop sim-in-the-loop; **+24.4%** few-shot real |
| Unified embodied-AI capability evaluation across 22+ benchmarks | [[2509.15273\|Embodied Arena]] — 7 capabilities × 25 dimensions; LLM-driven anti-overfitting data gen |
| Combine predictions from multiple imperfect simulators | [[2604.24018\|Sim2Real Betting]] — Cover's universal portfolio + Kelly bets; **70-100%** win rate vs MC |
| Evaluate *interactive* I2V world models against each other | [[2604.21686\|WorldMark]] — unified action mapping + 500 cases; **ρ > 0.9** with human judgments |

> [!star] Key Papers
> - [[2405.05941|SimplerEnv]] — First reliable sim-real correlation benchmark (**r > 0.85**, **r = 0.890**); introduces MMRV ranking metric; foundational evaluation paper
> - [[2605.06311|VISER]] — **r = 0.92** sim-real correlation via ray-traced PBR + MLLM asset pipeline; identifies specular highlights and contact shadows as load-bearing visual cues
> - [[2511.04665|Real-to-Sim GS]] — **r > 0.9** sim-real correlation on *deformable* tasks (plush, rope, T-block) via 3DGS + [[2503.17973|PhysTwin]]; the soft-body counterpart to [[2405.05941|SimplerEnv]]/[[2605.06311|VISER]]'s rigid-object work; identifies color alignment + physics optimization as jointly required
> - [[2604.10856|BridgeSim]] — Decomposes OL-CL gap into observational shift + objective mismatch; **+19.1 DS** via training-free TTA; sim-to-real is paradigm gap, not data gap
> - [[2604.24018|Sim2Real Betting]] — Sequential-betting estimator achieving **70-100%** win rate vs Monte Carlo; reframes sim-to-real as variance reduction

> [!tip] The Evaluation Stack
> ==[[2405.05941|SimplerEnv]]== (does sim correlate with real?) → ==[[2605.06311|VISER]]== (which visual cues drive correlation?) → ==[[2604.10856|BridgeSim]]== (where does OL-CL diverge?) → ==[[2604.24018|Sim2Real Betting]]== (how to combine multiple imperfect sims?). Use the stack — single-metric evaluation now reads as inadequate.

---

### 6. Integration Patterns

The §2–§5 components are not standalone recipes — they compose into four canonical deployable pipelines. Each pattern picks a primary point on the §1 design-space axes, then layers complementary elements to plug the gaps. The pattern you pick is determined by your *deployment regime* (one robot vs. fleet, narrow task vs. open world) far more than by your favorite paper.

#### 6.1 Pattern A — Massive DR + Procedural Sim

Combine procedural environment generation ([[2603.16861|MolmoBot]]) with extensive domain randomization ([[2210.13702|DeXtreme]] VADR) + teacher-student distillation ([[2511.15200|VIRAL]]). The industrial-scale recipe for general-purpose VLA training. Expensive in compute, broad in generalization.

- **[[2603.16861|MolmoBot]]** (Allen AI) — A procedural [MuJoCo](https://mujoco.org) data engine at scale: ==232K environments==, ==48K objects==, ==1.8M trajectories==; **79.2%** real [Franka FR3](https://franka.de) zero-shot vs π0.5-DROID's **39.2%** *with* real data.
- **[[2210.13702|DeXtreme]]** — The foundational ==Vectorized Automatic Domain Randomization== recipe on the Allegro Hand; **27.8** real reorientations vs **14.8** hand-tuned — auto-DR roughly doubles transfer.
- **[[2511.15200|VIRAL]]** (Unitree) — A visual sim-to-real framework at scale; ==tiled-renderer DAgger== student up to **64 GPUs**; **54/59** real G1 loco-manipulation cycles, matching expert teleop.

See [[05_VLA#1. Design-Space Principles]] for the upstream data strategy.

#### 6.2 Pattern B — Learned-Sim Foundation + Policy Fine-Tune

Pre-train against a learned world simulator ([[2310.06114|UniSim]] / [[2501.03575|Cosmos]]), then policy-side fine-tune on deployment-specific dynamics. Tradeoff: cheap visual diversity, but learned simulators ==blur on contact== — pair with hand-crafted physics for contact-heavy tasks.

- **[[2501.03575|Cosmos]]** — A ==World Foundation Model Platform==: **100M** curated clips, **+4 dB** PSNR tokenizer, ==10 FPS== autoregressive generation; defines the WFM category.
- **[[2310.06114|UniSim]]** — A simulator doing ==Conditional video generation== via ==5.6B-parameter diffusion==; **3-4×** zero-shot policy gain vs baselines on vision-language tasks.
- **[[2511.23369|SimScale]]** (driving) — A ==3DGS reconstruction== + sim-real co-training sim for autonomous driving; **>20%** relative gain for weak baselines, **EPDMS 48.0** on navhard.

See [[07_WAM#2. VideoGen WAMs]] for the upstream WAM architectures used as simulators.

#### 6.3 Pattern C — Digital-Twin-in-the-Loop

Reconstruct deployment scene as a digital twin ([[2503.17973|PhysTwin]] / [[2511.07416|PhysWorld]]), train RL inside the twin, transfer. Deployment-specific but cheap *per deployment*. Best for narrow, high-precision applications (specific assembly task, specific deformable target).

- **[[2511.07416|PhysWorld]]** — A digital-twin pipeline: task-conditioned video → ==4D reconstruction== → physical twin → ==object-centric residual RL==; **82%** real success across 10 tasks; **+15pp** over RIGVid.
- **[[2503.17973|PhysTwin]]** — A twin built from ==Spring-mass models== + ==Gaussian splats== for *deformable* objects from video; real-time interactive sim drives motion planning.
- **[[2504.03597|Real-is-Sim]]** — An ==Embodied Gaussians== twin as the policy's ==sole interface==; real robot mirrors sim via **60Hz** visual sync; **+23pp** PushT with 30+30 demos.

See [[11_Physics-Aware-Embodied-AI#4. External Simulator Coupling]] for the external-simulator coupling perspective.

#### 6.4 Pattern D — Online Adaptation with World-Model Feedback

Treat the sim-real gap as an OOD shift the world model detects and corrects for ([[2603.04029|Self-Adapting RL]]). Cheapest at deployment time but requires a continually-trained world model. Good fit for long-deployment robots that face slow distribution shift (e.g., wear over months).

- **[[2603.04029|Self-Adapting RL]]** — An ==[[2301.04104|DreamerV3]]==-based online continual RL; ==Observation== + ==Reward Prediction Residuals== trigger fine-tuning; Walker recovers from actuator damage in **2 min**; F1Tenth adapts to combined sim-real + friction shift in **8 min**.

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
| Multi-month deployed robot with slow drift | **Pattern D** (Online WM) | [[2603.04029\|Self-Adapting RL]] treats deployment drift as just-another-OOD event |
| Industrial assembly with imperfect demos | **Pattern A + C hybrid** | [[2603.15956\|ExpertGen]]/[[2602.23253\|SPARR]] layer real residual on sim-trained base (**95-100%** AutoMate) |
| Force-aware dexterous tasks | **Pattern A + tactile sim** | [[2601.02778\|Force-Based Sim2Real]] / [[2604.27367\|DOT-Sim]] add ==distance-field tactile== + ==MPM== to the recipe |

> [!star] Key Papers — Integration Pattern Exemplars
> - [[2603.16861|MolmoBot]] — Pattern A exemplar: **79.2%** real [Franka FR3](https://franka.de) from 232K procedural environments, no real data
> - [[2501.03575|Cosmos]] — Pattern B exemplar: WFM platform with 100M curated clips for learned-sim foundation
> - [[2511.07416|PhysWorld]] — Pattern C exemplar: **82%** real success across 10 tasks via task-conditioned video → physical twin → residual RL
> - [[2603.04029|Self-Adapting RL]] — Pattern D exemplar: [[2301.04104|DreamerV3]] prediction residuals trigger online world-model + policy fine-tuning
> - [[2602.23253|SPARR]] — Pattern A+C hybrid exemplar: sim-trained base + ==vision-conditioned real residual==; **95-100%** AutoMate assembly without human supervision

> [!tip] Patterns Compose — Pure Recipes Are Rare
> The 2026 frontier is *hybrid* patterns, not pure ones. [[2602.23253|SPARR]] layers a real-world residual (Pattern C-ish) on top of a procedurally-trained sim base (Pattern A). [[2603.15956|ExpertGen]] combines generative priors (Pattern B-ish) with DR (Pattern A) and visuomotor distillation. The discipline that wins is *picking the right primary pattern* for your deployment regime, then layering the secondary elements based on which sim-real gap (dynamics, visual, semantic) is dominant. For a learned-WAM-as-simulator deep dive, see [[07_WAM#2. VideoGen WAMs]]; for physics-grounded digital-twin coupling, see [[11_Physics-Aware-Embodied-AI#4. External Simulator Coupling]]; for force-aware tactile integration, see [[09_Contact-Rich-and-Whole-Body-Control#3. Force-Conditioned VLA Architectures]].

---

### 7. Open Problems

Sim-to-real has reached the point where the *median* lab-task transfers with reasonable success — but the failure modes have moved upstream. The seven open problems below cluster into three categories: *evaluation & generalization* (correlation benchmarks collapse under perturbation; benchmarks are fragmented), *simulator fidelity* (DR ceilings, learned-sim contact failures), and *methodological / orthogonal frontiers* (reward-signal transfer, statistical sim-stacking, controller-gain interaction). Each cluster needs a different research bet.

#### 7.1 Evaluation & Generalization

The benchmarks that currently certify sim-to-real are unstable: high correlation holds in-distribution but collapses under perturbation, and the benchmark stack itself is fragmented across correlation, generalization, and world-model evaluations.

- **==Sim-real correlation collapses on OOD perturbations==** — [[2405.05941|SimplerEnv]] and [[2605.06311|VISER]] achieve high correlation on *in-distribution* tasks but neither has shown the correlation survives intentional visual or dynamics perturbations. The next frontier is *robust* sim-real correlation under deliberate domain shift.
- **==Sim-to-real evaluation is fragmented==** — [[2509.15273|Embodied Arena]] unifies **22+** benchmarks but the *correlation* benchmarks ([[2405.05941|SimplerEnv]], [[2605.06311|VISER]]), *generalization* benchmarks ([[2506.18088|RoboTwin 2.0]]), and *world-model* benchmarks ([[2604.21686|WorldMark]]) remain separate stacks. A unified meta-benchmark would expose where methods are weakest.

#### 7.2 Simulator Fidelity

The simulator side of the loop is fundamentally limited by either DR's semantic ceiling or learned-sim contact-physics failures — neither yet generalizes.

- **==DR has limits==** — [[2604.11674|AffordSim]] reveals that domain randomization lifts simple-grasping zero-shot success only to **27%** on affordance-demanding tasks (pouring, hanging) — fine-grained semantic transfer is still unsolved. Combining DR with learned-sim foundations or digital twins is plausible but unproven at scale.
- **==Learned sims blur on contact==** — [[2310.06114|UniSim]] and [[2501.03575|Cosmos]] produce stunning visuals but physical contact regions (collisions, friction transients) look implausible to robots. Hybrid pipelines ([[2604.11138|ViserDex]]: ==3DGS rendering + MuJoCo physics==) are emerging but compute-expensive.

#### 7.3 Methodological & Orthogonal Frontiers

These three problems sit orthogonal to the mainstream "transfer actions across the sim-real gap" framing — they suggest reframings of the problem itself.

- **==Reward-signal sim-to-real==** — Most sim-to-real research transfers *actions*. [[2604.23702|QuietWalk]] shows you can also transfer *reward signals* (a ==PINN-estimated GRF== as RL reward generalizes across footwear). The reward-side sim-to-real problem is underexplored.
- **==Statistical sim-to-real==** — [[2604.24018|Sim2Real Betting]] proposes treating sim-real as ==variance reduction with biased predictors== — but the practical impact of running banks of cheap biased sims vs. one expensive accurate sim is open.
- **==Online controller-gain interaction==** — [[2604.02523|Tune to Learn]] shows controller gains are an unrecognized hyperparameter for sim-to-real, with ==stiff gains *worsening*== transfer despite lower sysid errors. Whether this generalizes beyond proportional-derivative position control is unknown.

**Sim-to-Real Failure Modes — Decision Matrix**

| Problem | Remediation Path |
|---|---|
| Sim-real correlation breaks under OOD perturbation | Stack [[2405.05941\|SimplerEnv]] + [[2605.06311\|VISER]] + perturbation harness — no single robust benchmark yet |
| Need unified meta-benchmark across correlation / generalization / WM | [[2509.15273\|Embodied Arena]] (22+ benchmarks unified) — partial; correlation stack still separate |
| DR ceiling on affordance-demanding tasks | [[2604.11674\|AffordSim]] (exposes ceiling) + DR-on-top-of-learned-sim — research gap |
| Learned simulator blurs on contact | [[2604.11138\|ViserDex]] (3DGS render + [MuJoCo](https://mujoco.org) physics hybrid) — compute-expensive |
| Need reward signals to cross the gap, not just actions | [[2604.23702\|QuietWalk]] (PINN GRF as RL reward) — underexplored |
| Want to combine multiple cheap biased simulators | [[2604.24018\|Sim2Real Betting]] (Kelly portfolio of sims) — early framing |
| Controller gains worsen sim-to-real despite low sysid | [[2604.02523\|Tune to Learn]] (compliant overdamped > stiff) — narrow to PD position control |

> [!star] Key Papers — Sim-to-Real Frontier
> - [[2604.11674|AffordSim]] — Exposes DR's ceiling: lifts simple grasping to **27%** but fine-grained affordance tasks (pouring/hanging) stay at **10-20%**; the canonical evidence that DR is insufficient for semantic transfer
> - [[2604.02523|Tune to Learn]] — Counterintuitive finding: stiff gains minimize sysid error but *worsen* sim-to-real; controller gains are an unrecognized hyperparameter — load-bearing evidence that the sysid metric is the wrong target
> - [[2604.24018|Sim2Real Betting]] — Reframes sim-to-real as a statistical variance-reduction problem; opens the frontier of combining multiple biased simulators rather than chasing a single accurate one

> [!tip] The Common Root Is Mis-Specified Targets
> Six of the seven problems above (correlation collapse, fragmented eval, DR ceiling, learned-sim contact blur, controller-gain interaction, and the implicit assumption that *actions* are what should transfer) trace to the same root: **sim-to-real research has been targeting the wrong proxies**. Sysid error ≠ transfer quality ([[2604.02523|Tune to Learn]]); DR coverage ≠ semantic generalization ([[2604.11674|AffordSim]]); visual realism ≠ contact fidelity (UniSim/Cosmos); in-distribution correlation ≠ OOD correlation (SimplerEnv/VISER under perturbation). The methodological reframings ([[2604.23702|QuietWalk]] reward-side, [[2604.24018|Sim2Real Betting]] statistical) suggest the next decade's progress will come from changing what we measure, not pushing harder on current metrics. Cross-reference [[07_WAM#9. Open Problems & Failure Modes]] (WAMs deployed as simulators inherit the same correlation-under-perturbation failures) and [[11_Physics-Aware-Embodied-AI#8. Open Problems]] (the benchmark-vs-deployment gap is the same problem from the physics-fidelity angle — verifiability gap upstream of the sim-real gap).

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
| Need humanoid sim-to-real? | [[2511.15200\|VIRAL]] (loco-manipulation), [[2506.12851\|KungfuBot]] (highly-dynamic), or [[2502.20396\|Humanoid Sim2Real Dex]] (dexterous) |
| Need force-aware sim-to-real? | [[2601.02778\|Force-Based Sim2Real]] or [[2604.27367\|DOT-Sim]] — see [[09_Contact-Rich-and-Whole-Body-Control#2. Tactile Sensors as a Sensing Modality]] for tactile depth |
| Need a digital twin? | [[2503.17973\|PhysTwin]] (deformable) or [[2511.07416\|PhysWorld]] (robot policy) — see [[11_Physics-Aware-Embodied-AI#4. External Simulator Coupling]] |
| Need policy that runs *only* in the twin (real robot mirrors sim)? | [[2504.03597\|Real-is-Sim]] (Embodied-Gaussians + 60Hz visual sync; +23pp PushT) |
| Need real2sim from video? | [[2404.09833\|Video2Game]] (rigid-body, browser-compatible) |
| Need vision-residual on top of sim-trained base for industrial assembly? | [[2602.23253\|SPARR]] (95-100% AutoMate without human supervision) |
| Need controller-gain awareness? | [[2604.02523\|Tune to Learn]] — compliant overdamped gains beat stiff for BC; stiff gains *worsen* sim-to-real |
| Need to evaluate sim-real correlation? | [[2405.05941\|SimplerEnv]] (r > 0.85) + [[2605.06311\|VISER]] (r = 0.92) — or [[2511.04665\|Real-to-Sim GS]] (r > 0.9) for **deformable-object** tasks |
| Need to diagnose OL-CL gap? | [[2604.10856\|BridgeSim]] (observational shift + objective mismatch) |
| Need to combine multiple sims? | [[2604.24018\|Sim2Real Betting]] (Kelly portfolio of sims) |
| Need a unified evaluation platform? | [[2509.15273\|Embodied Arena]] (22+ benchmarks) or [[2604.21686\|WorldMark]] (interactive WMs) |
| Need physics-informed reward shaping? | [[2604.23702\|QuietWalk]] (PINN GRF predictor as reward) |
| Need friction modeling for sim-to-real? | [[2604.24916\|asRoBallet]] (multi-channel tribology in [MuJoCo](https://mujoco.org)) |

---

## Cross-References

- [[01_Embodied-AI-101]] — Embodied AI primer; sim-to-real is the bridge between training and deployment
- [[02_Dataset-Benchmark-Environment]] — Datasets and benchmarks; §12 Sim-to-Real Transfer Evaluation + §4 Physics Engines + §7 Soft-Body Benchmarks expand here
- [[05_VLA]] — VLA deep-dive; sim-to-real is the bottleneck for the in-domain post-training recipe (§1)
- [[07_WAM]] — WAM deep-dive; learned world simulators ([[2310.06114|UniSim]], [[2501.03575|Cosmos]]) are WAMs deployed as simulators
- [[13_Self-Evolving-VLA-WAM]] — Self-evolving; world-model feedback for online sim-to-real adaptation
- [[11_Physics-Aware-Embodied-AI]] — Physics priors; §4 External Simulator Coupling overlaps real2sim2real
- [[09_Contact-Rich-and-Whole-Body-Control]] — Force-aware policies; tactile sim-to-real ([[2604.27367|DOT-Sim]], Force-Based)

---

*See [[07_WAM]] for world-model architectures used as simulators, [[11_Physics-Aware-Embodied-AI]] for physics-coupled sim-real loops, or [[02_Dataset-Benchmark-Environment]] for the broader benchmark ecosystem.*
