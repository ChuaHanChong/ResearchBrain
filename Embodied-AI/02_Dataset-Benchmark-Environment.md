---
title: "Datasets, Benchmarks & Environments — Deep Dive"
tags:
  - benchmark
  - robotics
  - embodied-AI
  - manipulation
  - VLA
aliases:
  - "Robotics Benchmarks"
  - "Embodied AI Datasets"
---

# Datasets, Benchmarks & Environments

> [!abstract] Overview
> The data and evaluation infrastructure that enables all embodied AI research. Embodied progress depends on three interlocked axes — the **data** the policy trains on, the **environment** it learns in, and the **benchmark** it is judged by. This note maps the full landscape: cross-embodiment scale datasets, multi-modal specialist data (tactile, bimanual, egocentric), simulation environments (rigid, soft-body, differentiable, household-scale), the diagnostic stack ([[2306.03310|LIBERO]] family, [[2601.11421|GM-100]], [[2507.10548|EmbRACE]]), language-conditioned long-horizon evals, sim-to-real transfer benchmarks, spatial reasoning probes, and the new generation of *interaction-centric* world model benchmarks. The field evolved from single-robot setups ([[1909.12271|RLBench]]) through million-trajectory cross-embodiment corpora ([[2310.08864|OXE]]) to household-scale simulation ([[2406.02523|RoboCasa]]), soft-body Gaussian-splat digital twins ([[2511.04665|Real-to-Sim GS]]) and diagnostic robustness evaluation ([[2510.13626|LIBERO-Plus]], [[2601.11421|GM-100]], [[2507.10548|EmbRACE-3K]]).

> [!example] How Datasets Are Used — Fuel for Every Training Stage
> Million-trajectory cross-embodiment corpora ([[2310.08864|OXE]], [[2403.12945|DROID]], [[2503.06669|AgiBot World]]) **pretrain VLA backbones** to learn task-invariant representations across robot morphologies; lab-curated single-embodiment data ([[2509.00576|G0]]) **post-trains specialists** when the deployment robot is fixed. Egocentric human video ([[2602.16710|EgoScale]], [[2605.06747|HumanNet]], [[2110.07058|Ego4D]]) supplies **finger-level supervision** that RGB-only robot data omits, while tactile and bimanual datasets ([[2604.20444|VTouch++]], [[2512.24653|RoboMIND 2.0]]) cover **modalities** (force, contact, dual-arm timing) that scale alone cannot. Hand-held collection paradigms ([[2402.10329|UMI]], [[2505.21864|DexUMI]], [[2605.03452|BifrostUMI]]) **replace teleoperation entirely**, unlocking dynamic and dexterous tasks that teleop physically cannot collect.

> [!note] How Environments & Engines Are Used — The Substrate
> Engines underwrite **both** data generation and evaluation. GPU-parallel engines ([[2511.04831|Isaac Lab]], [[2003.08515|SAPIEN]], [[2603.12185|ComFree-Sim]]) spawn thousands of environments at once to make **RL data scaling** feasible; photorealistic kitchens ([[2406.02523|RoboCasa]], [[2602.10116|SAGE]]) **close the visual reality gap** during training; bimanual sim+benchmark pairs ([[2506.18088|RoboTwin 2.0]]) ship data generator, evaluation suite, and domain randomization together so the trio stops being separable. The newer **real-to-sim wave** ([[2511.04665|Real-to-Sim GS]], [[2506.06440|Vid2Sim]], [[2510.21447|PhysWorld-Deformable]]) rebuilds the deployment scene from real video into a photorealistic digital twin that the policy can be re-evaluated against — collapsing the sim-real distinction for a specific target. Engine choice is itself a research-design decision (see §4): contact-accurate [MuJoCo](https://mujoco.org) vs throughput-optimized [PhysX](https://developer.nvidia.com/physx-sdk) shapes which experiments are even runnable.

---

> [!question] How Benchmarks Are Used — Staged Diagnostic Gates
> Modern evaluation is a *pipeline*, not a single score. A policy is pushed through ascending rigor: standard in-distribution ([[2306.03310|LIBERO]], [[2112.03227|CALVIN]]) → perturbation robustness ([[2510.13626|LIBERO-Plus]], [[2510.03827|LIBERO-PRO]], [[2603.28301|LIBERO-Para]]) → fine manipulation ([[2601.11421|GM-100]]) → embodied reasoning ([[2507.10548|EmbRACE-3K]], [[2508.13142|EASI]]) → sim-to-real correlation ([[2405.05941|SimplerEnv]], [[2605.06311|VISER]]) → distributed real-robot leaderboards ([[2506.18123|RoboArena]], [[2510.17950|RoboChallenge]]). Each tier probes a **different failure axis**: a policy that scores >90% on [[2306.03310|LIBERO]] can collapse to near-0% on [[2510.03827|LIBERO-PRO]] under minor perturbations, so passing any one tier in isolation no longer counts as evidence of generalization. World-model benchmarks ([[2603.22212|Omni-WorldBench]], [[2506.00613|WorldGym]], [[2603.23497|WildWorld]]) extend evaluation from passive video quality into **interactive action-fidelity** and **policy-transfer** measurement.

## Evolution Graph

```mermaid
graph LR
  subgraph Datasets
    SS[Something-Something<br/>2017] --> E4[Ego4D<br/>2022] --> RH[RH20T<br/>2023] --> OXE[OXE<br/>2023]
    OXE --> DR[DROID<br/>2024] --> AGI[AgiBot World<br/>2025] --> RM2[RoboMIND 2.0<br/>2026]
  end
  subgraph Sim
    RL[RLBench<br/>2019] --> SP[SAPIEN<br/>2020] --> RC[RoboCasa<br/>2024] --> RT2[RoboTwin 2.0<br/>2025] --> GEN[Genesis / Newton<br/>2025]
  end
  subgraph Benchmarks
    L1[LIBERO<br/>2023] --> LPL[LIBERO-Plus<br/>2025]
    L1 --> LPA[LIBERO-Para<br/>2026]
    L1 --> LPR[LIBERO-PRO<br/>2025]
    L1 --> LX[LIBERO-X<br/>2026]
    L1 --> GM[GM-100<br/>2026] --> EMB[EmbRACE-3K<br/>2025]
  end
  RM2 -.feeds.-> RT2
  RT2 -.evaluates.-> LPL
```

The three axes co-evolved. Datasets grew from gesture clips through household ego-video to million-trajectory robot corpora. Simulators grew from 100-task rigid-body sandboxes through articulated-object physics to GPU-parallel + photorealistic + soft-body. Benchmarks grew from in-distribution success rates through diagnostic perturbation suites and finally to interaction-fidelity world-model evaluation. The same paper now often releases data + sim + benchmark *together* ([[2506.18088|RoboTwin 2.0]], [[2406.02523|RoboCasa]], [[2503.06669|AgiBot World]]) — the trio is no longer separable.

## Part A — Datasets

*The fuel for policy training. Cross-embodiment scale, multi-modal specialist data, and the collection-system papers behind them.*

### 1. Cross-Embodiment Scale Datasets

The biggest unlock in robot learning: training across many robot types simultaneously. Scale and diversity matter more than curation.

Cross-embodiment transfer works because diverse robot morphologies force the model to learn *task-invariant* representations — grasping a cup looks different on a [Franka](https://franka.de) vs a [UR5](https://www.universal-robots.com/products/ur5-robot/), but the semantic understanding of "grasp the cup" is shared. The mechanism: visual and language encoders learn to project morphology-specific observations into a shared task space. The field's empirical progression has been *scale + diversity*, in that order — more robots, more environments, more institutions, more trajectories — with each new corpus pushing the cross-robot generalization frontier.

#### 1.1 Million-Trajectory Foundation Corpora

The internet-scale tier of robot data. Each corpus pushed a different scaling axis (robot count, institution count, single-lab depth).

- **[[2310.08864|OXE]]** — A cross-embodiment corpus of **1M+** real-robot trajectories from **22** embodiments that is the ==ImageNet moment== for robotics; the first dataset to prove cross-embodiment transfer is feasible.
- **[[2403.12945|DROID]]** — An in-the-wild dataset across **16** institutions that proves ==environmental diversity beats curation== at fixed trajectory count; **+20%** SR improvement vs single-lab baselines.
- **[[2503.06669|AgiBot World]]** — A single-lab corpus of **1M+** trajectories + [[2503.06669|GO-1]] generalist policy that is the dominant ==single-lab== scaling proof; **+32%** vs baseline — collaborative consortia are not the only path to million-trajectory corpora.
- **[[2408.10899|ARIO]]** — A ==unified hierarchical data standard== + corpus of **~3M** episodes / **321,064** tasks fusing real teleop, **~703K** sim episodes, and **62** converted datasets; timestamp-aligned across **5** modalities (2D/3D vision, text, tactile, audio) and single-arm/bimanual/humanoid/mobile embodiments — the format-unification answer to OXE's fragmentation.

#### 1.2 Diverse-Skill Tier

Smaller in trajectory count but engineered for *skill diversity* — many task families per embodiment rather than many embodiments per task.

- **[[2604.07607|EgoVerse]]** — A continuously-growing ==egocentric human dataset== (academic + industry) on ==EgoDB cloud ingestion== spanning **1,362** hours / **80,000** episodes / **1,965** tasks / **240** scenes / **2,087** demonstrators; ==flow-matching== co-training lifts robot policies up to **+30%** ID+OOD, with a small domain-aligned anchor key to transfer.
- **[[2307.00595|RH20T]]** — A ==multi-modal== dataset of **110,000+** contact-rich sequences across **147** tasks and **42** skills via ==haptic-device + force-torque teleoperation==, each carrying RGB/depth/IR + tactile + force-torque + audio + proprioception with demo video; targets ==one-shot skill learning==, complementing [[2310.08864|OXE]] as the *novel skill* reference.
- **[[2308.12952|BridgeData V2]]** — A diverse-skill dataset of **60,096** trajectories across **13** skills / **24** environments / **100+** objects on a low-cost ~**$4,000** WidowX-250 arm; RT-1 reaches **49%** seen-task SR and GCBC **60%** on unseen objects/environments — the canonical accessible corpus that goal- and language-conditioned policies benchmark on.

**Cross-Embodiment Datasets — Decision Matrix**

| Need | Dataset |
|---|---|
| Internet-scale generalist VLA pretraining | [[2310.08864\|OXE]] (**1M+** trajectories / **22** embodiments) |
| Maximum *environment* diversity | [[2403.12945\|DROID]] (**16** institutions / in-the-wild) |
| Single-lab depth without consortium overhead | [[2503.06669\|AgiBot World]] (**1M+** trajectories + [[2503.06669\|GO-1]] policy) |
| Few-shot / one-shot skill transfer | [[2307.00595\|RH20T]] |
| Compose multiple corpora for cross-embodiment + diversity | [[2310.08864\|OXE]] + [[2403.12945\|DROID]] mix (see §16 Picking Your Stack) |

> [!star] Key Papers
> - [[2310.08864|OXE]] — **1M+** real-robot trajectories from **22** embodiments; the ImageNet moment for robotics
> - [[2403.12945|DROID]] — In-the-wild data across **16** institutions; **+20%** SR improvement; proved diverse data beats curated data
> - [[2503.06669|AgiBot World]] — **1M+** trajectories + [[2503.06669|GO-1]] generalist policy; **+32%** improvement over baselines; largest single-lab effort

> [!tip] Data Scale vs Quality
> [[2310.08864|OXE]] proved cross-embodiment transfer works. [[2403.12945|DROID]] proved diversity beats curation. [[2503.06669|AgiBot World]] proved a single lab can match collaborative scale. The pattern: more robots, more scenes, more tasks → better generalization. The corollary appears in §2 ([[2509.00576|G0]]): when your deployment robot is fixed, single-embodiment depth beats heterogeneous breadth — *whose* scaling law applies depends on whether the test-time embodiment is open or closed. Cross-reference [[12_Egocentric-Pretraining-and-Human-Video#3. Scaling Laws for Egocentric Pretraining]] for the egocentric-data scaling-law analogue and [[05_VLA#1. Design-Space Principles]] for backbone-choice implications.

---

### 2. Multi-Modal & Specialist Datasets

Rich sensing (tactile, force, dual-arm) or specific manipulation challenges. For when scale alone isn't enough.

Standard VLA datasets capture RGB images + actions — sufficient for simple pick-and-place but inadequate for contact-rich tasks (insertion, polishing, assembly) where force feedback determines success or failure. Bimanual datasets ([[2512.24653|RoboMIND 2.0]]) must capture coordinated dual-arm trajectories with synchronization — the timing between left and right arm matters as much as the positions. Egocentric datasets capture human-perspective video that maps more naturally to robot head-mounted cameras, reducing the viewpoint gap in cross-embodiment transfer.

#### 2.1 Bimanual Manipulation

Coordinated two-arm control requires specialized data with synchronized dual-arm timing, tactile feedback, and contact-rich task variety.

- **[[2604.20444|VTouch++]]** — A bimanual tactile dataset of **120,000+** episodes and **1,000+** hours across **380+** systematically categorized tasks, each with synchronized fingertip tactile + multi-view RGB-D + proprioception; the modern bimanual tactile landmark.
- **[[2604.07335|TAMEn]]** — A closed-loop bimanual collection system combining a ==modular gripper-adaptive wearable== + ==feasibility-aware acquisition== + ==AR teleop (tAmeR)== recovery + ==pyramid-structured data regime==; object tracking **100%** SR (vs **32–78%** marker-only), validation lifts replay to **100%** (from **12–39%**), full system **75%** avg SR on 4 contact-rich tasks.
- **[[2603.05687|CGP]]** — A contact-grounded policy that feeds ==coupled state+tactile diffusion trajectories== into a ==contact-consistency mapping== for a compliance controller; outperforms visuomotor + visuotactile diffusion baselines on **5** dexterous tasks (jar-opening, in-hand box flipping) at real-time inference latency.
- **[[2512.24653|RoboMIND 2.0]]** — A dual-arm dataset of **310K** trajectories from **6** heterogeneous platforms spanning **759** tasks, **129** skills, and **1,139** objects, with ==tactile feedback== and an ==Isaac Sim digital twin==; the paired ==MIND-2 hierarchical dual-system== (VLM planner + IQL-optimized VLA executor) reaches **1.0** SR on multi-robot collaborative tasks.
- **[[2511.17441|RoboCOIN]]** — A bimanual dataset of **180,000+** demos across **15** platforms and **421** tasks, with a ==hierarchical capability pyramid== (trajectory/segment/frame annotations) and ==CoRobot RTML quality control==; RTML filtering removes **35.3%** low-quality trajectories and raises [[2503.14734|GR00T N1]].5 SR by **+23%**.
- **[[2412.13877|RoboMIND]]** — A multi-platform dataset of **107,000** trajectories (**305.5 hours**) over **479** tasks across Franka + UR5e + AgileX + Tien Kung humanoid, including **5,000** failure demos and **10,000** frame-level language-annotated trajectories, plus an ==Isaac Sim digital twin== (Pearson **0.83–0.91** sim-real correlation); precursor to RoboMIND 2.0.
- **[[2502.05086|REASSEMBLE]]** — A force-grounded assembly dataset for contact-rich assembly/disassembly on the ==NIST Task Board #1== via ==haptic teleoperation== of a Franka FR3, synchronizing RGB + proprioception + audio + ==6-axis force-torque== + event-camera streams; **4,551** demos (**781 min**, incl. **516** failures), SOTA temporal action segmentation only **44.1%** F1@50.
- **[[2403.19417|OAKINK2]]** — A bimanual human-object manipulation dataset under a ==3-level affordance/primitive/complex task hierarchy==, spanning **627** sequences and **~4.01M** frames over **100** household objects with precise 3D hand/body/object pose, plus a ==Complex Task Completion== framework that decomposes tasks into primitives.
- **[[2401.08399|TACO]]** — A large-scale 4D ==bimanual tool-action-object== dataset (multi-view RGB + egocentric RGBD + ==optical MoCap==) serving as a tool-use generalization probe; **2.5K** sequences / **5.2M** frames / **131** tool-action-object triplets, with compositional-action recognition dropping **86.15%→44.00%** under compound generalization.

#### 2.2 Single-Embodiment High-Quality

Depth over breadth: consistent data from one robot in diverse environments. The case for *fixed-deployment-robot* specialists.

- **[[2509.00576|G0]]** — A **500-hour** Galaxea Open-World single-embodiment dataset (R1 Lite, **50** scenes) + ==dual-system VLA== (G0-VLM planner + G0-VLA executor) via ==3-stage curriculum== (cross-embodiment → single-embodiment → task-specific); Stage-2 pre-training improves language following + few-shot; fine-tuned G0-VLM beats baseline VLMs by **+50%** subtask-instruction accuracy.

#### 2.3 Egocentric & Motion Capture

Human-perspective video and motion data for cross-embodiment skill transfer. [[2602.16710|EgoScale]] demonstrates that egocentric *dexterous* human data scales differently than RGB-only embodiments — finger-level supervision is the bottleneck, not viewpoint. [[2605.06747|HumanNet]] pushes the scale axis to 1M hours, demonstrating that 1,000 hours of curated egocentric pretrain can match 100 hours of real-robot data. [[2605.05945|MobileEgo Anywhere]] pushes the *accessibility* axis — long-horizon (up to 108-minute) egocentric capture from commodity LiDAR-enabled smartphones, democratizing the hardware bar.

- **[[2605.06747|HumanNet]]** — A **1,000,000-hour** human-centric video corpus (==egocentric + exocentric==) via a ==three-stage collection→processing→annotation pipeline== with ==interaction-centric annotations==; **1,000 hr** of egocentric pretrain matches **100 hr** of real-robot CoBot pretrain and closes the gap to **LingBot** (**20,000 hr** robot data) — the largest to date.
- **[[2605.05945|MobileEgo Anywhere]]** — An open infrastructure providing **200-hour / 354-session** long-horizon (up to 108-min) egocentric data on commodity iPhone Pro + open-source Python pipeline; [ARKit](https://developer.apple.com/augmented-reality/arkit/) drift **<1 cm** for hour-long household activities; automated hierarchical action labels at **$1.29** for all sessions.
- **[[2602.16710|EgoScale]]** — A dataset of **20,854 hours** of ==egocentric human video== with ==two-stage learning== (human pretrain → embodiment-aligned mid-train); **+54%** task completion on a **22-DoF** robot hand, **log-linear scaling law** in action-prediction validation loss, **88%** one-shot shirt folding, **+30%** absolute cross-embodiment gain on a **7-DoF** tri-finger hand.
- **[[2605.09613|SABER]]** — A **100+ hours** grocery-activity corpus (ego+exo) feeding ==three action-representation streams== (==LAPA latent actions== + ==Dex-Retargeting== + body-pose retargets) as a ==domain-specific post-training layer== on **GR00T N1.6** via ==conditional flow-matching==; **2.19x** SR gain (**13.4% → 29.3%**) on [[2511.10276|RoboBenchMart]], `open_fridge` **12% → 82%**.
- **[[2502.04144|HD-EPIC]]** — A **41.3-hour** unscripted home-kitchen egocentric corpus on ==Project Aria== with ==multi-video SLAM 3D digital twins== + 'how'/'why' action clauses + nutrition tracking, serving as a hard egocentric-understanding probe: **59,454** actions, **263** annotations/min; on the **26,650-question** VQA, Gemini Pro reaches **37.6%** vs **90.3%** human.
- **[[2411.19167|HOT3D]]** — An **833-minute** multi-view, hardware-synchronized egocentric hand+object dataset (Aria + Quest 3) with ==marker-based 3D ground truth==; two-view input lifts hand-pose error **41%** relative and 6-DoF object recall **8–12pp** over single-view — the egocentric 3D hand/object-tracking reference.
- **[[2402.13349|Aria Everyday]]** — An open multimodal egocentric corpus of **7.3 hours** across **143** sequences (RGB + eye-tracking + 7-ch spatial audio + IMU), annotated with **1 kHz** ==globally-aligned 6-DoF trajectories== + ==3D eye gaze== + speech transcripts; Gaussian-splat reconstruction reaches **25.12** PSNR — the AR-glasses always-on context substrate.
- **[[2203.14712|Assembly101]]** — A **513-hour** procedural assembly/disassembly corpus (8 static + 4 egocentric cams, **101** toys) with **1M+** action segments + **18M** ==3D hand poses== + novel ==mistake/correction labels==; static beats egocentric by **16.2%**, mistake-detection recall only **46.6%** — the procedural-activity + error-detection benchmark.
- **[[2406.09905|Nymeria]]** — The largest in-the-wild human-motion dataset, with ==XSens MoCap + Project Aria + miniAria wristbands== sub-ms synchronized in a gravity-aligned metric world; **300 hours** / **264** participants / **50** locations with **260M** body poses, **201.2M** egocentric images, and **310K+** hierarchical language sentences — the motion+language egocentric scale anchor.
- **[[2203.01577|HOI4D]]** — A **4D egocentric** category-level human-object interaction dataset on head-mounted dual RGB-D and a hard articulated-HOI probe: **800** object instances across **16** categories (7 rigid / 9 articulated) in **610** indoor rooms; BundleTrack pose accuracy collapses **86.5%→19.3%** (bottle) and 4D segmentation hits only **44.6%** mIoU.
- **[[2104.11181|H2O]]** — The first markerless ==two-hands-manipulating-objects== egocentric dataset and the two-hand egocentric pose reference: **571,645** frames with 3D two-hand + 6D object pose + **36** interaction classes at ~**1 cm** annotation error; a ==Topology-Aware GCN== reaches **79.25%** interaction recognition (beating SlowFast/I3D).
- **[[2006.00626|EGTEA Gaze+]]** — The first-person video benchmark with synchronized ==binocular gaze== + pixel-level hand masks + fine-grained actions; a ==probabilistic gaze + action joint model== (Gumbel-Softmax attention) hits **55.03%** mean-class accuracy and generalizes to EPIC-Kitchens without gaze supervision — the canonical gaze-grounded egocentric dataset.
- [SEED (Bones Studio)](https://huggingface.co/datasets/bones-studio/seed) — High-quality motion capture and manipulation dataset for dexterous skill learning
- [EgoVerse (Georgia Tech)](https://github.com/gatech-rl2/egoverse) — Egocentric video dataset capturing first-person human activities for robot skill transfer

#### 2.4 Teleoperation Hardware & Hand-Held Data Collection

The data collection systems themselves. [[2402.10329|UMI]] introduced the "in-the-wild" hand-held paradigm that eliminates teleoperation entirely; subsequent work has extended it to dexterous hands and humanoid whole-body manipulation.

- **[[2402.10329|UMI]]** — A hand-held in-the-wild data-collection system using a wrist GoPro + ==IMU-aware monocular SLAM== for 6-DoF tracking; **20/20** cup-arrangement on [UR5](https://www.universal-robots.com/products/ur5-robot/) cross-embodied to **18/20** on [Franka](https://franka.de), **71.7%** unseen-env generalization, **87.5%** dynamic tossing, **>3×** faster than teleop.
- **[[2505.21864|DexUMI]]** — A dexterous extension of UMI using robot-specific wearable hand ==exoskeletons== (Inspire Hand, XHand) for natural haptic feedback + a ==visual adaptation pipeline== that ==inpaints the human hand== with the robot hand image; **86%** SR across 4 contact-rich tasks, **3.2×** data efficiency vs teleop.
- **[[2605.03452|BifrostUMI]]** — A gripper-cam paradigm generalized to humanoid whole-body manipulation via ==head-and-hand pose retargeting== that maps gripper-cam pose into a humanoid frame — humanoid demos collected without ever wearing a teleop harness.
- **[[2309.13037|GELLO]]** — A ==kinematically isomorphic== 3D-printed leader replica using ==backdrivable servo motors as encoders== + ==passive joint regularizers==; **92%** avg SR across 5 bi-manual tasks (vs **63%** for 3D mouse, **72%** for VR), validated on **3** robots (UR5/xArm7/Franka) at **<$300** BOM per device.
- **[[2304.13705|ALOHA]]** — An open-source bimanual platform (**<$20K**) + ==ACT (Action Chunking with Transformers)== — a ==Transformer CVAE== predicting multi-step action sequences with ==temporal ensembling==; the original benchmark for fine-grained tasks (zip-tie threading, cup separation, ping-pong juggling).
- **[[1911.04052|RoboTurk]]** — A scalable human-supervision platform extending crowdsourced ==remote teleoperation== to physical arms with a mutual-exclusion access system + input low-pass filtering + proximate servers; **111+ hours** / **2,144** demos across 3 tasks from **54** users in one week — the foundational data-collection platform.

> [!star] Key Papers
> - [[2604.20444|VTouch++]] — The bimanual-tactile landmark: 120,000+ episodes / 380+ skill-axis-categorized tasks with synchronized fingertip tactile; contrastive learning lifts cross-modal retrieval **7×**, diffusion policy reaches **0.022 MAE** on real hardware
> - [[2605.03452|BifrostUMI]] — Robot-free demonstration paradigm extended to humanoids; the dominant scaling alternative for whole-body data
> - [[2512.24653|RoboMIND 2.0]] — 310K bimanual + mobile manipulation trajectories with tactile sensing and digital twin
> - [[2602.16710|EgoScale]] — Scaling dexterous manipulation specifically via diverse egocentric *human* data — fingers, not arms, are the bottleneck
> - [[2402.10329|UMI]] — Hand-held in-the-wild data collection; **>3x faster** than teleop, cross-robot zero-shot generalization, dynamic tasks impossible via teleop; the dominant alternative to teleoperation

**Specialist Datasets — Decision Matrix**

| Need | Dataset |
|---|---|
| Bimanual tactile with skill-axis task design | [[2604.20444\|VTouch++]] (**120K+** episodes / **380+** tasks) |
| Large-scale bimanual + digital twin | [[2512.24653\|RoboMIND 2.0]] (**310K** trajectories / **6** platforms) |
| Closed-loop bimanual collection + recovery | [[2604.07335\|TAMEn]] (**75%** avg SR) |
| Single-embodiment fixed-deployment depth | [[2509.00576\|G0]] (**500-hour** / **50** scenes) |
| Dexterous egocentric *human* pretrain (finger-level) | [[2602.16710\|EgoScale]] (**20,854 hr**), [[2605.06747\|HumanNet]] (**1M hr**) |
| Robot-free collection without teleop | [[2402.10329\|UMI]], [[2505.21864\|DexUMI]], [[2605.03452\|BifrostUMI]] |
| Low-cost bimanual teleop baseline | [[2304.13705\|ALOHA]] (**<$20K**) |

> [!tip] When Scale Doesn't Help
> [[2509.00576|G0]] showed single-embodiment in-domain data quality can outperform heterogeneous cross-embodiment scale. If your deployment robot is fixed, invest in diverse *scenes* not diverse *robots*. The corollary from [[2602.16710|EgoScale]]: if your deployment robot has *fingers*, invest in diverse *human hand* data — VLA-scale RGB does not cover the finger-control space.

---

## Part B — Simulation Environments

*The robot-learning platforms — scenes + assets + sensor models + task APIs. Where the policy actually trains and evaluates.*

### 3. Simulation Environments

The physical simulation substrate on which benchmarks are built. Choice of environment determines what you can test.

#### 3.1 Foundation Simulators

General-purpose physics platforms for robot learning. Each picks a different point on the (visual fidelity × physics accuracy × throughput) trade-off.

- **[[2606.03551|Isaac Sim Survey]]** — A system overview of ==NVIDIA Isaac Sim== integrating ==GPU-accelerated PhysX== dynamics + ==RTX photorealistic rendering== over a ==USD-based asset system==, with ==IsaacLab== for GPU-parallel ==reinforcement learning== + ==Replicator== synthetic-data generation; the reference high-fidelity GPU simulator on the visual-fidelity end.
- **[[2003.08515|SAPIEN]]** — A simulator of **2,346** articulated PartNet-Mobility objects with ==part-level kinematic/dynamic attributes==, [PhysX 4.1](https://developer.nvidia.com/physx-sdk) at **~5000 Hz** + OpenGL+OptiX renderer at **~700 Hz**; heuristic baselines reach **95.3%** drawer-pull / **81.8%** door-open; the foundational platform for articulation-heavy research.
- **[[1909.12271|RLBench]]** — A benchmark of **100** visually-guided manipulation tasks on [CoppeliaSim](https://www.coppeliarobotics.com/) + PyRep with ==Task/Variation/Episode hierarchy== and ==waypoint motion-planned== infinite expert demos; the few-shot evaluation standard for the Franka Panda.
- **[[2009.12293|robosuite]]** — A [MuJoCo](https://mujoco.org) framework with separate ==Modeling/Simulation APIs==, **10** robot + **9** gripper models, ==variable-impedance control==, **9** single-arm/bimanual/mobile tasks; SAC solves **3/9** environments, OSC-POSE learns faster than joint-velocity — reproducibility substrate under [[2406.02523|RoboCasa]] / [[2506.18088|RoboTwin 2.0]].
- **[[2604.08258|EvoGymCM]]** — An EvoGym extension adding ==continuous material stiffness== S∈[0.5, 2] as a first-class optimizable parameter via ==bi-level optimization== over morphology + material + control; **+41%** in Reactive-Material co-design on BridgeWalker (**2.10 → 2.97**) and AreaMaximizer (**0.62 → 0.74**).
- [Genesis](https://genesis-world.readthedocs.io/) — GPU-native, open-source, multi-physics (rigid + soft + cloth + fluid) in one runtime; emerging community-driven research substrate.
- **[[2502.08844|MuJoCo Playground]]** — A ==JAX/MuJoCo-MJX-native== open-source RL framework standardizing reproducible robot learning on quadrupeds, humanoids, and dexterous manipulation; runs in-browser via WASM, supports ==tile-rendered visual policies== on a single GPU, and demonstrates direct sim-to-real transfer.
- **[[2504.18904|RoboVerse]]** — A unified platform built on ==METASIM infrastructure== abstracting simulators (==MuJoCo==, ==PhysX==, ==Isaac Sim==, ==SAPIEN==, ==CoppeliaSim==) into one interface + ==multi-source synthetic data pipeline== (rollouts + motion planning + teleop + AI task gen); standardizes IL/RL benchmarks with proven sim-to-real — closest to a simulator-stack abstraction.
- **[[2410.00425|ManiSkill3]]** — A ==GPU-parallelized== robotics simulator on SAPIEN + PhysX with parallel rendering; **30,000+ FPS** sim+render, **2-3×** less GPU memory than peers; **91.6%** zero-shot real-robot cube-pick, **0.928** real2sim correlation; reduces visual RL training from hours to minutes.
- **[[2506.10966|GenManip]]** — An Isaac-Sim tabletop platform with **10,000** annotated 3D objects + **100** articulated objects + ==LLM-driven Task-oriented Scene Graph== auto-generating instruction-following scenarios; on GenManip-Bench, modular systems reach **23.0%** SR (**9.07%** long-horizon) while GR-1 hits **95.0%** familiar but **0.0%** novel — a generalization stress-test.
- **[[2506.04941|ArtVIP]]** — An open-source library of **992** ==digital-twin articulated assets== with ==PBR materials==, pixel-level affordance labels, tuned joint stiffness/friction, and **5** ==modular interaction primitives== (latching, variable damping); beats BEHAVIOR-1K / PartNet-Mobility on CLIP-feature realism, **98%** RL trashcan-closing, **0.9886** sim-real Pearson.
- **[[2302.04659|ManiSkill2]]** — A throughput-oriented manipulation benchmark of **20** task families including real-time ==rigid-MPM soft-body== environments with two-way coupling + multi-controller support + cross-action-space demo conversion; ~**2000 FPS** visual-RL collection (RGBD) and **80–84 FPS** soft-body sim — the predecessor to [[2410.00425|ManiSkill3]].
- [Newton (NVIDIA)](https://developer.nvidia.com/newton-physics) — Successor to [Isaac Gym](https://developer.nvidia.com/isaac-gym) physics; [PhysX-5](https://github.com/NVIDIA-Omniverse/PhysX) with full soft-body and fluid in one runtime; aims to be the "universal" sim.

#### 3.2 Household-Scale

Realistic home environments with diverse objects and tasks. Bridges the visual reality gap during training.

- **[[2406.02523|RoboCasa]]** — A household simulator of **120** unique kitchen scenes across **10** floor plans / **12** styles + **2,500+** ==asset library== + **100-task** benchmark (25 atomic / 75 LLM-composed); ==MimicGen== machine-generated demos generalize better than human teleop and transfer to a real Franka Panda — pioneered data-gen-as-benchmark.
- **[[2602.10116|SAGE]]** — An ==agentic LLM-orchestrated== scene generator chaining a ==Scene Initializer + Asset Placer + Mover/Remover== with ==Visual Critic + Physics Critic (simulator-in-the-loop)==; **99.9%** stability / **1.9%** collision in Isaac Sim (vs **63.8%/22.0%** Holodeck, **67.7%/32.8%** SceneWeaver); policies trained on SAGE data reach **39.1%** OOD SR (vs **13.2%** baseline).

#### 3.3 Photorealistic 3D Environments

Visually realistic 3D worlds for navigation, HRI, and vision-based policies.

- **[[2604.25459|GS-Playground]]** — A high-throughput simulator pairing a parallel physics engine with a memory-efficient ==batch 3D Gaussian Splatting== renderer (==point-pruning==) + ==Rigid-Link Gaussian Kinematics==; **10,000 FPS** at 640×480, **32×** over MuJoCo for 50 humanoids; zero-shot sim-to-real manipulation at **90%** real SR — photorealism without the ray-tracing penalty.
- **[[2003.08515|SAPIEN]]** — A simulator of **2,346** articulated PartNet-Mobility objects with [PhysX 4.1](https://developer.nvidia.com/physx-sdk) at **~5000 Hz** + OpenGL+OptiX rendering at **~700 Hz** *(also listed under Foundation Simulators above)*.
- **[[2406.02523|RoboCasa]]** — A household simulator of **120** kitchens / **10** floor plans / **2,500+** ==assets== with [MuJoCo](https://mujoco.org)+RoboSuite backend; the modern household-photorealism reference *(also listed under Household-Scale above)*.
- **[[2601.02078|Genie Sim 3.0]]** — A humanoid-targeted high-fidelity simulator with LLM-driven scene generation + LLM-VLM automated evaluation + ==3D Gaussian Splatting== environment reconstruction; **10,000+ hours** synthetic data, **100,000+** evaluation scenarios; **R²=0.94** sim-to-real correlation; **1,500 episodes** of synthetic data beats real-data baselines on zero-shot manipulation.
- **[[2109.08238|HM3D]]** — A large-scale photorealistic ==Habitat-Matterport 3D== substrate of **1,000** real-world building-scale scans (**112.5k m²** navigable) via Matterport Pro2 + proprietary reconstruction + 800h human curation; **1.4–3.7×** larger coverage and **34–91%** fewer reconstruction defects than MP3D/Gibson — the substrate for embodied navigation.
- [Habitat 3.0](https://aihabitat.org) — Photorealistic 3D environments + humanoid avatars; the standard for navigation + HRI research.

#### 3.4 Agentic 3D Scene Generation

Scalable scene generation as a simulation substrate.

- **[[2604.07105|Genie Sim PanoRecon]]** — A ==feed-forward Gaussian-splatting pipeline== decomposing a single panorama into ==cubemap faces== + ==Panoramic Depth Fusion== (DA360 global + DepthPro local via Laplacian pyramid) + ==training-free depth injection==; reconstructs photorealistic 3D backgrounds in seconds, feeding manipulation-sim asset generation on Genie Sim.
- **[[2602.10116|SAGE]]** — An ==LLM agent + Visual + Physics critic loop== over Isaac Sim; **99.9%** stability / **1.9%** collision (vs **63.8%/22.0%** Holodeck), with physics critic alone driving collision rate **7.8% → 1.9%**.

#### 3.5 Generative & Real-to-Sim Simulators

Build sim worlds *from real video*, sidestepping authoring entirely. A new category that doesn't use a hand-crafted physics engine — these synthesize the dynamics or rendering from learned video priors:

- **[[2604.15805|WorldComposer]]** — A real-to-sim generator producing a photorealistic ==Digital Twin== (==3D Gaussian Splats== + collision mesh) plus diverse ==Digital Cousins== from a single panorama via ==prompt-driven semantic/geometric editing== + ==multi-room ICP stitching==; **r=0.91** sim-real, up to **85%** real SR augmenting 50 real with 1,000 sim — twin-plus-cousins beats single-twin.
- **[[2604.11386|ComSim]]** — A ==compositional "real-sim-real" pipeline== fusing classical-simulator action precision with a ==DiT neural simulator== converting sim video into "pseudo-real" data; Shake-Bottle SR climbs **17/30 → 28/30** (10 real + 200 pseudo-real) and OOD **0/30 → 12/30**, bridging the sim2real visual gap while preserving action consistency.
- **[[2604.10982|Psi-Map]]** — A ==2D Gaussian Surfel== panoptic real2sim mapper reinforced by ==SOGMM== geometric priors + query-guided segmentation; **74.12** PQ on ScanNet-V2, **98.07** F1 geometry, **45 FPS** rendering — high-integrity digital twins with object-level identities for control-loop-rate simulation.
- **[[2604.08544|SIM1]]** — A physics-aligned ==real-to-sim-to-real data engine== for deformables with submillimeter ==geometric alignment== + ==AVBD-inspired deformation-stable solver==; zero-shot **76%** SR where real-data baselines hit **0%**, **+50%** spatial / **+47%** lighting generalization, **27×** cost reduction / **6.8×** throughput vs real collection.
- **[[2602.16444|RoboGene]]** — A ==diversity-driven agentic task generator== with ==LFU sampling== + ==multi-faceted LLM self-reflection== + memory-augmented refinement; **0.99** physical feasibility, **719** objects (**1.7×** expansion) / **118** skills, VLA pretrain reaches **40%** unseen dual-arm SR — the data-coverage complement to scene-level generators.
- **[[2509.22970|RoLA]]** — A real-to-sim engine turning *any single in-the-wild image* into an interactive sim via ==generative physical-scene recovery== + ==z-buffer visual blending== of rendered sim over the real background; **76.2%** avg SR (vs **10.5%** retrieval / **11.4%** pixel-edit), deploys to real Franka + Unitree humanoid — internet images as a robot-data source.
- **[[2506.06440|Vid2Sim]]** — A two-stage pipeline (==feed-forward init of Young's modulus / Poisson's ratio / LBS weights== via VideoMAE → ==Gaussian-splat== refinement + ==Neural Jacobian== implicit-Euler dynamics); **PSNR 30.17** vs **22.06** PAC-NeRF, **~15 min** per-scene refinement vs **54–120 min** baselines.
- **[[2511.04665|Real-to-Sim GS]]** — A soft-body digital-twin pipeline combining ==3D Gaussian Splatting== rendering + ==PhysTwin== twins on ==NVIDIA Warp==, params optimized from interaction video + ==positional + color alignment==; Pearson **r > 0.9** sim-real across plush-toy / rope / T-block (vs **r = 0.649** Isaac Lab on T-block); ablations confirm color + physics opt are load-bearing.
- **[[2510.21447|PhysWorld-Deformable]]** — A three-stage MPM digital twin from short real videos via ==VLM-assisted constitutive-model selection== + global-to-local property optimization, then ==VMP-Gen== motion synthesis + ==P³-Pert== perturbation feeding a GNN fine-tuned on real video; **799 FPS** (**47×** the **17 FPS** PhysTwin), Chamfer **0.010**; enables MPPI planning on deformables.
- **[[2504.13059|RoboTwin]]** — A ==generative digital-twin== dual-arm framework synthesizing diverse 3D assets from limited real images via image-conditioned 3D generation + ==LLM task decomposition==; **300** simulated + **20** real samples match **300** real samples alone — the canonical generative-twin data-efficiency result robot policies report SR against.
- **[[2310.17596|MimicGen]]** — A data-generation engine using ==object-centric subtask parsing== of ~**200** human demos, transformed and replayed across new object poses to auto-synthesize **50,000+** demonstrations over **18** tasks (**250×** multiplication); agents trained on it match or beat human-only data — the engine [[2406.02523|RoboCasa]] builds on.
- **[[2501.03575|NVIDIA Cosmos]]** — A platform of ==5.6B-parameter video diffusion + autoregressive WFMs== trained on **20M hours / 100M clips**; Cosmos Tokenizer is **+4 dB** PSNR + **2x–12x** faster; autoregressive WFM runs at **10 FPS** real-time at 320×512 via Medusa speculative decoding; **<7 cm** trajectory error for autonomous-driving fine-tunes.

#### 3.6 Egocentric / Interaction Simulators

Generative simulators that produce egocentric video conditioned on action.

- **[[2604.01001|EgoSim]]** — A ==closed-loop geometry-action-aware observation simulator== with ==training-free incremental 3D-scene state updating==; **PSNR 25.056** + Depth-ERR **8.888** on EgoDex (best of class); cross-embodiment pretraining lifts AgiBot-World PSNR **15.180 → 18.670**.

#### 3.7 Teleoperation-Friendly

Environments designed for collecting human demonstrations with low-friction interaction loops.

- **[[2310.06114|UniSim]]** — A ==5.6B-parameter video diffusion== simulator with ==dataset orchestration== over heterogeneous robotic + human + panorama + internet data + ==T5-embedded unified action space==; zero-shot sim-to-real with **3–4× better** goal reduction; captioning fine-tune CIDEr **15.2 → 46.23**.

#### 3.8 Bimanual Sim + Benchmark

Sim platforms that ship with a paired benchmark and data generator.

- **[[2506.18088|RoboTwin 2.0]]** — A bimanual sim + benchmark using ==automated MLLM expert-code generation== with closed-loop simulation feedback + ==5-axis domain randomization== (clutter / texture / lighting / heights / instructions) + ==embodiment-aware grasp adaptation==; **71.3%** auto-code SR, **+24.4%** real-world few-shot SR, **+21.0%** zero-shot on unseen backgrounds.
- **[[2605.16257|DexJoCo]]** — A benchmark of **11 task-oriented dexterous manipulation tasks** in [MuJoCo](https://mujoco.org) (finger coordination, tool-use, bimanual, long-horizon) with Rokoko-Smartgloves + HTC-Vive teleop (GeoRT) for low-cost demos; exposes IL brittleness under full visual randomization (DP-T **50.4%→20.0%**) and a lack of true language generalization in VLAs.

Simulator choice has profound implications for what you can test — articulation fidelity, task variety, photorealism, and physics accuracy each gate different research questions. The 2025-2026 frontier moves along two axes: (1) **next-gen multi-physics engines** ([Genesis](https://genesis-world.readthedocs.io/), [NVIDIA Newton](https://developer.nvidia.com/newton-physics)) aim to combine [PhysX](https://developer.nvidia.com/physx-sdk)'s parallelism with [MuJoCo](https://mujoco.org)'s contact accuracy; (2) **LLM-driven scene generation** sidesteps the 3D-artistry bottleneck — producing simulation environments at the rate of LLM prompting rather than per-scene authoring effort.

> [!star] Key Papers
> - [[2003.08515|SAPIEN]] — 2,346 articulated objects with physics-accurate simulation; foundational platform for manipulation research
> - [[1909.12271|RLBench]] — 100 tasks with infinite expert demos via motion planning; standardized few-shot and imitation learning evaluation
> - [[2406.02523|RoboCasa]] — Scaling synthetic data significantly improves generalist policy performance; data-generation platform + benchmark
> - [[2506.18088|RoboTwin 2.0]] — Bimanual sim + benchmark with strong domain randomization; the modern bimanual reference
> - [[2602.10116|SAGE]] — Agentic 3D scene generation; bypasses the scene-authoring bottleneck via LLM-driven layout + asset retrieval

#### 3.9 Physics Engines — Quick Reference

*A summary card; §4 below treats each engine as a research-design choice with paper-anchored detail.*

| Engine | Strengths | Typical Use |
|--------|-----------|-------------|
| **[PhysX](https://developer.nvidia.com/physx-sdk)** | GPU-accelerated rigid body + deformable simulation, NVIDIA ecosystem | [[2003.08515\|SAPIEN]], [Isaac Gym](https://developer.nvidia.com/isaac-gym)/[[2511.04831\|Lab]], large-scale parallel RL |
| **[MuJoCo](https://mujoco.org)** | Fast, accurate contact/tendon dynamics, low overhead | Standard RL benchmarks, OpenAI Gym, DeepMind Control |
| **[PyBullet](https://pybullet.org)** | Open-source, easy Python API, good for prototyping | [[1909.12271\|RLBench]], early robot learning pipelines |
| **[MJX (MuJoCo-JAX)](https://mujoco.readthedocs.io/en/stable/mjx.html)** | Differentiable [MuJoCo](https://mujoco.org) on GPU/TPU | Differentiable physics RL, gradient-based MPC |
| **[Brax](https://github.com/google/brax)** | JAX-native GPU rigid-body sim | Massively-parallel RL ablation studies |
| **[Taichi](https://www.taichi-lang.org) / [DiffTaichi](https://github.com/taichi-dev/difftaichi)** | Differentiable Lagrangian / MPM | Soft body, fluid, deformable manipulation |
| **[PhysX-5](https://github.com/NVIDIA-Omniverse/PhysX) / [Newton (NVIDIA)](https://developer.nvidia.com/newton-physics)** | GPU contact-rich + soft + fluid + cloth in one engine | Next-gen general-purpose sim |
| **[Genesis](https://genesis-world.readthedocs.io/)** | GPU-native, open-source, multi-physics (rigid + soft + cloth) | Emerging research substrate |

> [!tip] Sim Engine Choice
> [PhysX](https://developer.nvidia.com/physx-sdk) dominates GPU-parallel training (throughput). [MuJoCo](https://mujoco.org) is gold standard for contact-rich manipulation accuracy. [PyBullet](https://pybullet.org) enabled rapid prototyping but is increasingly replaced. For production: [PhysX](https://developer.nvidia.com/physx-sdk) if GPU-parallel, [MuJoCo](https://mujoco.org) if contact accuracy matters.

**Simulator — Decision Matrix**

| Need | Simulator |
|---|---|
| General-purpose articulated objects | [[2003.08515\|SAPIEN]] (2,346 objects + [PhysX](https://developer.nvidia.com/physx-sdk)) |
| Standardized few-shot manipulation tasks | [[1909.12271\|RLBench]] (100 tasks + motion-planned demos) |
| Photorealistic kitchens / households | [[2406.02523\|RoboCasa]] ([MuJoCo](https://mujoco.org) backend) |
| Photorealistic 3D nav + humanoid avatars | [Habitat 3.0](https://aihabitat.org) |
| Agentic LLM-driven scene generation | [[2602.10116\|SAGE]] |
| Bimanual sim + benchmark (paired) | [[2506.18088\|RoboTwin 2.0]] ([MuJoCo](https://mujoco.org) via [ManiSkill](https://github.com/haosulab/ManiSkill), domain randomization) |
| Egocentric video conditioned on action | [[2604.01001\|EgoSim]] |
| Teleoperation-friendly demonstration collection | [[2310.06114\|UniSim]] |
| Soft-body digital twin from real video | [[2511.04665\|Real-to-Sim GS]] (Gaussian splat) |
| Generative real-to-sim simulators | [[2506.06440\|Vid2Sim]], [[2510.21447\|PhysWorld-Deformable]], [[2501.03575\|NVIDIA Cosmos]] |
| Driving / wheeled robots | [CARLA](https://carla.org), [NVIDIA Drive Sim](https://developer.nvidia.com/drive/simulation) |
| GPU-parallel scaled training | See **Part C** (the engine layer); pair an engine with a §3 simulator |

---

## Part C — Physics Engines

*The dynamics solvers underneath the simulators in Part B. A physics engine answers: "given state + forces, what is the next state?" Multiple simulators often sit on the same engine.*

### 4. Physics Engines as Research Substrate

Beyond benchmark-shipped simulators, a separate category of research-grade physics engines is shaping what kinds of learning experiments are even *possible* — differentiable physics, GPU-massive parallelism, photorealistic rendering with contact, and multi-physics (rigid + soft + cloth + fluid) in one runtime.

#### 4.1 Differentiable Physics Engines

Provide gradients through dynamics, enabling system-identification, gradient-based MPC, and end-to-end policy + physics co-optimization.

- **[MJX (MuJoCo-JAX)](https://mujoco.readthedocs.io/en/stable/mjx.html)** — JAX rewrite of [MuJoCo](https://mujoco.org); differentiable, GPU/TPU-parallel; replaces [MuJoCo](https://mujoco.org) for gradient-based RL workflows.
- **[DiffTaichi](https://github.com/taichi-dev/difftaichi)** — Differentiable Lagrangian/MPM simulator; primary substrate for soft-body and fluid manipulation research (cloth, dough, soft tissue).
- **[Brax](https://github.com/google/brax)** — JAX-native GPU rigid-body engine; the standard for massively-parallel RL ablations.
- **[Drake (TRI)](https://drake.mit.edu)** — Smooth contact + differentiable trajectory optimization for grasping and contact-rich manipulation.

#### 4.2 GPU-Native Massively-Parallel Engines

Trade contact accuracy for thousands-of-environment parallelism, enabling RL data scaling that was infeasible on CPU.

- **[[2511.04831|Isaac Lab]]** — A GPU-parallel engine succeeding [Isaac Gym](https://developer.nvidia.com/isaac-gym) on [PhysX-5](https://github.com/NVIDIA-Omniverse/PhysX) + RTX + [OpenUSD](https://openusd.org); **>900K FPS** state-based, up to **1.6M FPS** in distributed training; foundational for **[[2503.14734|GR00T N1]]/N1.5** training and Mimic synthetic-data pipeline.
- **[Isaac Gym](https://developer.nvidia.com/isaac-gym) / [Isaac Sim](https://developer.nvidia.com/isaac-sim)** (NVIDIA, legacy) — Original [PhysX](https://developer.nvidia.com/physx-sdk)-backed parallel sims; 4,096+ envs/GPU; superseded by [[2511.04831|Isaac Lab]] for most use cases.
- **[[2603.12185|ComFree-Sim]]** — A GPU-parallelized analytical contact engine (complementarity-free); **~3×** simulation speed and near-linear scaling with contact count vs [MJWarp](https://github.com/google-deepmind/mujoco_warp); real-time MPPI on physical hardware gains **2.4×** compute speedup and **+27pp** closed-loop SR for dexterous manipulation.
- **[Genesis](https://genesis-world.readthedocs.io/)** — Open-source GPU-native, multi-physics (rigid + soft + cloth + fluid) in one runtime; community-driven alternative to Isaac.
- **[Newton (NVIDIA)](https://developer.nvidia.com/newton-physics)** — Successor to [Isaac Gym](https://developer.nvidia.com/isaac-gym) physics; [PhysX-5](https://github.com/NVIDIA-Omniverse/PhysX) with full soft-body and fluid in one runtime; aims to be the "universal" sim.

**Engine — Decision Matrix**

| Need | Engine |
|---|---|
| Differentiable gradients (for system-ID or grad-MPC) | [MJX](https://mujoco.readthedocs.io/en/stable/mjx.html), [DiffTaichi](https://github.com/taichi-dev/difftaichi), [Drake](https://drake.mit.edu) |
| Massive GPU parallelism (RL data scaling) | [[2511.04831\|Isaac Lab]]/Sim, [Genesis](https://genesis-world.readthedocs.io/), [Brax](https://github.com/google/brax) |
| Soft-body / cloth / fluid | [DiffTaichi](https://github.com/taichi-dev/difftaichi), [Genesis](https://genesis-world.readthedocs.io/), [Newton](https://developer.nvidia.com/newton-physics) |
| Contact-rich manipulation accuracy | [MuJoCo](https://mujoco.org) / [MJX](https://mujoco.readthedocs.io/en/stable/mjx.html) |
| Real-time contact + lightweight | [MuJoCo](https://mujoco.org) (CPU), [PyBullet](https://pybullet.org) (prototyping) |
| Open-source GPU multi-physics | [Genesis](https://genesis-world.readthedocs.io/), [Newton](https://developer.nvidia.com/newton-physics) |
| GPU contact-solver speed-up | [[2603.12185\|ComFree-Sim]] (3× [MJWarp](https://github.com/google-deepmind/mujoco_warp) on dense contact) |

> [!star] Key Papers
> - [[2511.04831|Isaac Lab]] — NVIDIA's GPU-accelerated framework ([PhysX-5](https://github.com/NVIDIA-Omniverse/PhysX) + RTX + [OpenUSD](https://openusd.org)); **>900K FPS** to **1.6M FPS** distributed; trains [[2503.14734|GR00T N1]]/N1.5. The dominant 2025-2026 GPU-parallel substrate
> - [[2603.12185|ComFree-Sim]] — Complementarity-free analytical contact engine; **3×** faster than [MJWarp](https://github.com/google-deepmind/mujoco_warp) with near-linear scaling on dense contact; **+27pp** hardware MPPI SR gain — proves you can drop iterative solvers without losing fidelity
> - [[2506.06440|Vid2Sim]] — Replaces 3D-asset authoring with video-driven reconstruction; the cheapest path to a custom simulator
> - [[2511.04665|Real-to-Sim GS]] — Gaussian-splat soft-body twins for policy evaluation; closes the visual + physical gap for deformables in one stack
> - [[2003.08515|SAPIEN]] — Still the foundational articulated-object benchmark, but [Genesis](https://genesis-world.readthedocs.io/) and [Newton](https://developer.nvidia.com/newton-physics) are catching up on fidelity while leading on throughput

> [!tip] Engine Choice is a Policy Decision
> Choosing an engine constrains what experiments you can run. If you commit to [MuJoCo](https://mujoco.org), you can't easily train at 4,096-env parallelism. If you commit to Isaac, you give up the cleanest contact dynamics. Modern projects ([[2406.02523|RoboCasa]], [[2506.18088|RoboTwin 2.0]], [Genesis](https://genesis-world.readthedocs.io/)) increasingly use *multiple* engines — one for fast policy training, one for accurate evaluation. Cross-reference [[14_Sim-to-Real-Transfer#1. Design-Space Principles]] for how engine choice interacts with the sim-real gap.

---

## Part D — Benchmarks

*The evaluation axes — tactile, diagnostic, long-horizon, spatial, world-model. Each tier probes a different failure mode of the policy stack.*

### 5. Diagnostic & Evaluation Datasets

Not for training — for exposing failure modes and measuring real capability.

Diagnostic benchmarks differ from training benchmarks in a crucial way: they are designed to *expose specific failure modes*, not measure overall performance. [[2601.11421|GM-100]]'s 100 detail-oriented tasks (precise insertion, fine alignment, tool manipulation) systematically test manipulation capabilities that standard benchmarks miss — current VLAs achieve very low success rates, revealing that 'grasping things' and 'precise manipulation' are fundamentally different capabilities. [[2507.10548|EmbRACE-3K]] evaluates embodied reasoning across 3,000 scenarios, testing whether models understand spatial relationships, physical causality, and task decomposition — not just whether they can pick up objects.

#### 5.1 Precision & Reasoning Probes

Diagnostics that target the *low-level skill* and *high-level reasoning* axes — what VLAs get wrong even when language and grasping work.

- **[[2606.02307|FATE-VLA]]** — A ==failure-aware adaptive test generation== framework combining ==Adaptive Random Testing== with ==surrogate ML models== predicting failure likelihood to generate failure-prone yet diverse scenarios; raises discovered failure rate by up to **+29.7 pp** over random sampling on models like GR00T-N1.6.
- **[[2606.02277|RoboSemanticBench]]** — A controlled benchmark recasting semantic grounding as an ==answer-selection task==, with a ==Normalized Semantic Grounding (nSG)== metric; most VLAs score **2.0–12.7%** TSR with nSG ≤ 0 (π0.5 the lone outlier at **21.8%** TSR / **5.2%** nSG), and even ReasoningVLA leaves **89.93%** correct-reasoning/wrong-action cases.
- **[[2601.11421|GM-100]]** — A benchmark of **100** detail-oriented tasks (precise insertion, fine alignment, tool manipulation); current VLAs achieve very low SR, exposing real ==precision gaps== between "grasp the cup" and "insert the peg".
- **[[2507.10548|EmbRACE-3K]]** — A benchmark of **3,000** multi-stage language-guided tasks across **24** Unreal Engine environments via human demos in a ==closed-loop perception-action cycle== with ==step-wise "thinking" rationales==; GPT-4o/Gemini-2.5-Pro near-zero zero-shot, Qwen2.5-VL-sft-rl reaches **42.4%** Dynamic Spatial-Semantic — high [[2306.03310|LIBERO]] ≠ embodied intelligence.
- **[[2508.13142|EASI]]** — A holistic MLLM spatial-intelligence framework with ==unified 6-capability taxonomy== (Metric / Mental Reconstruction / Spatial Relations / Perspective-Taking / Deformation / Comprehensive) over 8 benchmarks under zero-shot CoT; GPT-5 lags human by **>30pp** on average and **>76pp** on hardest SI tasks.
- **[[2507.05258|REA]]** — A benchmark of **24,371 QA pairs** combining 3D point clouds + egocentric video (EPIC-KITCHENS/VISOR/EPIC-FIELDS) across 5 tasks (Relative Direction/Distance, Find My Item, Affordance, Action Planning); ==STLLM-Aligner== cross-modal alignment hits **46.50%** vs **23.85–31.46%** existing MLLMs.
- **[[2307.10224|RL-ViGen]]** — A visual-RL ==generalization benchmark== of **5** task categories × **5** OOD axes (appearance, lighting, camera, scene structure, cross-embodiment) over 8 algorithms; all collapse on novel scene structures, PIE-G (ImageNet priors) leads on appearance/lighting and SGQN on camera-view — exposes which OOD axis each algorithm fails.

#### 5.2 Capability-Disentangling & Memory Probes

Diagnostics that decompose a single "success rate" into ==capability axes== (planning vs perception vs memory) — answer the question *which* part of the policy stack is failing.

- **[[2605.10921|RoboMemArena]]** — The first comprehensive robotic-memory benchmark; **26 sim + 5 real** tasks where **68.9%** of subtasks require historical information; ==PrediMem== (predictive-coding VLA with hierarchical memory) hits **38.5%** TSR vs MemER's **27.3%** — the dedicated memory-failure-axis diagnostic.
- **[[2603.09513|VQ-Memory]]** — A ==RuleSafe== non-Markovian long-horizon articulated-unlocking benchmark (LLM-aided SAPIEN) + a model-agnostic ==VQ-VAE memory== over proprioceptive history with K-means codebook clustering; lifts avg SR across 20 tasks **25.0% → 56.3%** (**+31.3%**), DP3 **5.0% → 45.0%**, π0 **0.0% → 45.0%** on rule 020.
- **[[2603.04639|RoboMME]]** — A ==cognitively-motivated memory benchmark== over **16** long-horizon tasks split into ==temporal / spatial / object / procedural memory==; **1,600** demos / **770K** timesteps on ManiSkill, **14** memory-augmented π0.5 variants — perceptual memory wins at **44.51%** SR, oracle-symbolic **84.08%** vs **90.5%** human; decomposes which memory each lacks.
- **[[2603.01229|RMBench]]** — A memory-dependent dual-arm benchmark of **9** tasks graded by a ==Task Memory Complexity== metric + the ==Mem-0== modular memory policy (key/anchor/sliding memory); Mem-0 reaches **52.8%** on M(1) (**+38.4%**) and **28.5%** on M(n) (**+21.2%**), real-world **22.50%** vs ACT **0.0%** / Pi0.5 **5.83%**.
- **[[2602.22663|CEBench]]** — A ==cross-embodiment practicality benchmark== (single-arm / bimanual / mobile-bimanual, sim + real, ==domain randomization==) + ==LLaVA-VLA== (0.5B, pre-training-free, ==hybrid direction+value action space==); LLaVA-VLA **50.6%** on CALVIN 5/5 beating OpenVLA-7B, **30.7%** real DR bimanual, first end-to-end VLA at real mobile manipulation.
- **[[2502.09560|EmbodiedBench]]** — A benchmark of **1,128 tasks** across **4** environments (ALFRED, [Habitat](https://aihabitat.org), Nav, Manipulation) × **6** capabilities (commonsense, instructions, spatial, perception, planning, basic); GPT-4o scores **>60%** on high-level planning but only **28.9%** on low-level manipulation, and removing vision drops Nav **57.7% → 17.4%**.

#### 5.3 LIBERO-Family Robustness Suite

The same parent benchmark ([[2306.03310|LIBERO]]) re-released along distinct perturbation axes — each child exposes a *different* over-fit / brittleness mode that the standard suite hides.

- **[[2510.13626|LIBERO-Plus]]** — A **7-axis visual robustness** suite (camera, lighting, background, distractor, occlusion, texture, instruction variant); WAMs outperform VLAs by large margins (VLA-JEPA: **79.5%**).
- **[[2510.03827|LIBERO-PRO]]** — A minor-task-perturbation suite on which VLAs collapse from **>90% → near 0%** under *small* changes — the most damning data point in recent VLA evaluation literature.
- **[[2602.06556|LIBERO-X]]** — A benchmark of **600** tasks / **100** scenes with a ==5-level protocol== perturbing layout / object properties / instruction semantics; VLAs hit only **39.4%** at Level 1 and decline **31.2%** by Level 5 (near-zero on 3+ step tasks) — massive unsolved cross-task gap.
- **[[2603.28301|LIBERO-Para]]** — A meaning-preserving paraphrase suite on LIBERO-Goal scored by the ==PRIDE== difficulty-aware metric; across **7** VLA configs (0.6B–7.5B) SR drops **22.8–51.9pp**, PRIDE runs **8.4–22.0%** below raw SR, and **79.5–95.5%** of failures are planning-level — models overfit to exact instruction phrasing.

#### 5.4 VLA Robustness & Adversarial Benchmarks

Distinct from the LIBERO-family's *passive* perturbation children, this tier *actively* searches for failures — adversarial/backdoor attacks, metamorphic relations, optimized worst-case physical variations, and automated test-and-evaluation infrastructure. The shared finding: VLAs that pass standard suites harbor exploitable failure surfaces that only adversarial search reveals.

- **[[2603.22435|CaP-X]]** — An open ==Code-as-Policy benchmark== (==CaP-Gym== + ==CaP-Bench==) probing how agent performance scales with primitive abstraction; ==CaP-Agent0== (visual differencing + skill libraries) hits human-level on **4/7** tasks, out-robustifies VLAs on LIBERO-PRO; ==CaP-RL== verifiable rewards lift Cube-Lift **25% → 80%** — isolates reasoning from human priors.
- **[[2602.22579|VLA Metamorphic Testing]]** — A ==Metamorphic Testing== framework with two task-agnostic ==Metamorphic Relation Patterns== (Trajectory Consistency / Variation) across synonym, object-addition, lighting, negation, and relocation transforms; surfaces **3,527** failures the symbolic oracle misses — exposes execution-level Motion/Manipulation faults beyond task non-completion.
- **[[2602.01640|A2Eval]]** — A ==two-agent automated eval framework== (Data Agent diversity-aware sampling + sandboxed Eval Agent) for embodied VLMs; compresses **24,519 → 3,781** examples (**85%**) into **8** balanced capability dimensions at **77%** cost reduction / **3.4–4.6×** speedup, with **κ=0.78** / **ρ=0.85** human alignment — fixes the redundant-benchmark ecosystem.
- **[[2512.01989|PAI-Bench]]** — A ==three-track Physical-AI benchmark== (generation / conditional-generation / understanding) probing physics plausibility via ==MLLM-as-Judge== Domain Scores; VGMs match source video on Quality but lag badly on physical plausibility, and all MLLMs trail the **93.2%** human baseline — separates visual fidelity from physical understanding.
- **[[2511.12149|AttackVLA]]** — A ==unified adversarial + backdoor attack benchmark== across OpenVLA / SpatialVLA / π0-fast; ==BackdoorVLA== bi-modal trigger induces attacker-specified long-horizon actions at **75.35%** ASR_t in sim and **50.00%** on a physical Franka arm (untargeted UADA up to **100%** ASR_u) — the first targeted physical-robot backdoor threat model.
- **[[2509.18953|Eva-VLA]]** — A ==gradient-free black-box robustness search== (CMA-ES over ==3D rotations==, ==point-light illumination==, ==natural adversarial patches==) with a cosine-action-similarity objective; drives OpenVLA/UniVLA failure rates **4.0–23.5% → >80%**, adversarial examples retrain π0.5 to **85.8% → 56.8%** 3D-transform failure.

> [!star] Key Papers
> - [[2605.10921|RoboMemArena]] — First comprehensive robotic-memory benchmark: 26 sim + 5 real-world tasks with multimodal annotations (visual keyframes + language) where **68.9%** of subtasks genuinely require historical information; **PrediMem** (predictive-coding VLA with hierarchical memory) hits **38.5%** TSR vs MemER's **27.3%** — the dedicated memory-failure-axis diagnostic
> - [[2502.09560|EmbodiedBench]] — 1,128 tasks across 4 environments (ALFRED, [Habitat](https://aihabitat.org), Nav, Manipulation) × 6 capabilities (commonsense, instructions, spatial, perception, planning, basic). Exposes that **GPT-4o** scores **>60%** on high-level planning but only **28.9%** on low-level manipulation; removing vision drops Nav from **57.7% → 17.4%** — the de-facto capability-disentangling MLLM-agent benchmark
> - [[2601.11421|GM-100]] — 100 detail-oriented tasks; current VLAs achieve very low success rates, exposing real capability gaps
> - [[2507.10548|EmbRACE-3K]] — 3,000 scenarios testing embodied reasoning (spatial + causal + task-decomposition); reveals that high [[2306.03310|LIBERO]] scores do not imply embodied intelligence
> - [[2510.03827|LIBERO-PRO]] — Minor-perturbation collapse from **>90% → ~0%**; the field's "memorization vs generalization" reference point

**Diagnostic — Decision Matrix**

| Need | Diagnostic |
|---|---|
| Baseline in-distribution skill | [[2306.03310\|LIBERO]], [[2112.03227\|CALVIN]] |
| Visual robustness (camera, lighting, occlusion) | [[2510.13626\|LIBERO-Plus]] (**7-axis**) |
| Memorization vs generalization | [[2510.03827\|LIBERO-PRO]] (**>90% → ~0%** collapse under small changes) |
| Cross-task / cross-instruction transfer | [[2602.06556\|LIBERO-X]] + [[2603.28301\|LIBERO-Para]] |
| Detail-oriented precision (insertion, alignment) | [[2601.11421\|GM-100]] |
| Embodied reasoning (spatial + causal) | [[2507.10548\|EmbRACE-3K]], [[2508.13142\|EASI]] |
| Capability decomposition (planning vs perception) | [[2502.09560\|EmbodiedBench]] (**6-axis**) |
| Long-term memory failure | [[2605.10921\|RoboMemArena]] (**68.9%** subtasks memory-dependent) |
| Robust evaluation under perturbation | [[2507.05258\|REA]] |

> [!tip] Use the Diagnostic Stack
> Each benchmark stresses one failure axis. A model can score >90% on [[2306.03310|LIBERO]] yet collapse on [[2510.13626|LIBERO-Plus]] (visual), [[2603.28301|LIBERO-Para]] (language), [[2510.03827|LIBERO-PRO]] (minor perturbations), or [[2601.11421|GM-100]] (precision). Always evaluate across the full diagnostic stack before claiming generalization. The [[2510.03827|LIBERO-PRO]] collapse from >90% to near 0% under *small* changes is the most damning data point in recent VLA evaluation literature. Cross-reference [[05_VLA#1. Design-Space Principles]] for architectural responses to these failure modes, [[08_Latent-World-Models#5. Latent vs Pixel Comparison]] for the WAM-vs-VLA robustness gap, and [[14_Sim-to-Real-Transfer#3. Policy-Side: Robustness & Domain Randomization]] for policy-side robustness recipes.

---

### 6. Tactile & Contact-Rich Benchmarks

Force-feedback, touch, and contact-rich manipulation form their own evaluation axis — orthogonal to RGB-only VLA benchmarks. A model can score perfectly on [[2306.03310|LIBERO]] and still fail at peg insertion because no part of [[2306.03310|LIBERO]]'s evaluation requires force-aware behavior. The 2024-2026 wave of tactile work created the first standardized evaluation infrastructure for touch.

#### 6.1 Tactile Representation Benchmarks

The *representation* axis: do learned tactile features beat sensor-specific end-to-end pipelines on a fixed, multi-sensor task suite? Introduced in [[2410.24090|Sparsh]], [[2410.24090|TacBench]] is the de-facto standard.

- **[[2410.24090|Sparsh]]** / [[2410.24090|TacBench]] — A tactile-representation benchmark of **6** touch tasks (force estimation, slip detection, contact localization, fabric classification, dynamic pose tracking, bead maze) across ==DIGIT==, ==GelSight Mini==, ==OmniTact==, ==OptoTact== sensors; self-supervised reps beat sensor-specific end-to-end on **6/6** across the **95.8K-image** benchmark.
- **[[2506.14754|Sparsh-X]]** — A ==multisensory touch== extension of [[2410.24090|Sparsh]] (image + audio + IMU + pressure) from ==Digit 360== via ==attention bottlenecks==, self-supervised on ~**1M** unlabeled contact interactions; **>3× improvement** on hardest force-and-vibration tasks and **+500%** plug-insertion SR over vision-only (to **90%**) — defines the multisensory tactile axis.

#### 6.2 Tactile-Augmented Policy Benchmarks

The *policy* axis: full robot policies (not just representations) evaluated under contact-rich settings — does adding touch improve closed-loop SR on insertion / wiping / soft-object tasks?

- **[[2606.04825|HapTile]]** — A ==haptic-informed vision-tactile-language-action dataset== of **1,726** demonstrations across **38** contact-rich tasks with synchronized fingertip ==visuotactile== data, collected with ==real-time haptic feedback to the operator==; adding raw tactile (V+T) lifts SR — strikingly **0% → 90%** for π0 peg insertion — though marker-tracked features can hurt.
- **[[2604.07335|TAMEn]]** — A Tactile-Aware Manipulation Engine for closed-loop data collection; ==online feasibility validation== lifts demo-replay success to **100%** (from **12–39%**), and the full system with ==tactile pretraining== + AR-recovery + ==pyramid-structured data regime== reaches **75%** avg SR across 4 contact-rich bimanual tasks (see §2.1).
- **[[2603.17851|DexViTac]]** — A portable ==visuo-tactile-kinematic== human-demo system with a ==ROS2 synchronized-acquisition framework== at **248 demos/hr** (near human speed); ==two-stage== recipe — ==kinematics-grounded tactile pretraining== → ACT policy — reaches **85.8%** avg SR on 4 contact-rich dexterous tasks, Pipetting collapsing **83.3% → 43.3%** without pretraining.
- **[[2603.05687|CGP]]** — A contact-grounded policy using ==diffusion-predicted coupled state + tactile trajectories== + ==learned contact-consistency mapping== to a compliance controller; outperforms visuomotor + visuotactile baselines on **5** dexterous tasks (jar-opening, in-hand box flipping) at real-time inference latency.
- **[[2510.25725|HumanoidVTA]]** — The first humanoid visual-tactile-action dataset for *soft-object* manipulation; teleoperated Inspire Hands with **2,124 high-resolution tactile sensors**; t-SNE shows dense tactile signals separate task conditions where sparse signals collapse — establishes the dense-vs-sparse tactile evaluation axis for soft-object policies
- **[[2510.13324|FARM]]** — A ==Force-Aware Robotic Manipulation== diffusion policy predicting pose+grip+force from ==high-dim tactile force distributions== + ==dual-mode position/force controller==; **100%** dynamic screw-tightening, **95%** plant-insertion + grape-picking; W1 **0.7538 N** force matching to human demos.
- **[[2509.07962|TA-VLA]]** — A systematic ==when/where/how== ablation of motor-current torque integration in pretrained VLAs; decoder-side aggregated-history token wins; π0+obs+obj lifts Charger-Plugging **0/20 → 17/20**, Button-Pushing **5/20 → 18/20**, generalizes to RDT + ROKAE SR cross-embodiment.
- **[[2509.18830|DexSkin]]** — A ==conformable capacitive parallel-plate-grid skin== of **60** taxels @ **294°** fingertip coverage at **<$10/pair**; senses to **1.7 kPa** with **6.52%** hysteresis; **19/20** perturbed pen reorientation (vs **0/20** baseline); ==pneumatic calibration== recovers transfer from **5/20 → 14/20** on swapped sensors.
- **[[2503.02881|Reactive Diffusion Policy]]** — A ==slow-fast hierarchical IL== policy where a ==Latent Diffusion Policy== plans + an ==Asymmetric Tokenizer== reacts on high-freq tactile/force; **+35%** over Diffusion-Policy baselines, **0.90–0.95** peeling SR, **0.8 vs 0.15** under perturbations; paired ==TactAR AR-teleop== improves stable-contact-force ratio **0.58 → 0.87**.
- **[[2505.22566|Universal Visuo-Tactile]]** — A ==VTV-LLM== model with the **VTV150K** dataset (150,000 frames, 100 objects, 3 sensors: GelSight Mini / DIGIT / Tac3D) + ==optical-flow-guided masking==; **60.4%** avg high-level tactile reasoning (vs **28.0%** GPT-4o), **75.0%** individual-attribute accuracy.
- **[[2505.06451|Adaptive Wiping]]** — A ==two-step few-shot IL== method with a pre-trained ==VAE object encoder== + closed-loop force-torque feedback; **100%** contact + **96%** reference-force tracking across **40** unseen-height/sponge scenarios (vs **4%** open-loop IL, **42%** admittance), generalizes to wall-wiping at **104%** force.
- **[[2505.18472|ManiFeel]]** — The first comprehensive visuotactile sim benchmark in IsaacGym: **13** tasks (insertion, screwing, exploration) with simulated ==GelSight R1.5== (TacRGB + TacFF); benchmarks pre-trained encoders (UniT, T3, AnyTouch) + policies (DP, Flow Matching); **+26pp** TacFF on peg-insertion, **+14pp** on real gear-assembly — the "does touch help" probe.
- **[[2408.06506|TacSL]]** — A GPU-accelerated visuotactile sim in Isaac with ==implicit Kelvin-Voigt soft contact== + ==Asymmetric Actor-Critic Distillation==; **200×** tactile-image gen (**1631 FPS**), **428×** force-field gen (**1.5M FPS**); zero-shot sim-to-real **91.4%** peg-place / **82.7%** peg-insert; image-aug lifts real SR **27.2 → 87.7%** — de-facto tactile-sim foundation.
- **[[2109.04027|Taxim]]** — An ==example-based optical simulation== for GelSight sensors: a polynomial look-up table maps contact geometry to per-pixel intensity, with ==linear-elastic== marker-field motion (first to combine marker + optical sim); **lowest pixel-wise intensity error** vs prior work, runs **online on CPU** — the foundational tactile simulator for sim-to-real data generation.

> [!star] Key Papers
> - [[2410.24090|Sparsh]] — Introduces [[2410.24090|TacBench]] (6 tasks, 4 sensors); first standardized tactile representation benchmark; self-supervised reps beat end-to-end on **6/6** tasks
> - [[2506.14754|Sparsh-X]] — Extends [[2410.24090|Sparsh]] to multisensory touch (image + audio + vibration + force); **>3x improvement** on force-and-vibration tasks; defines the multisensory tactile evaluation axis
> - [[2603.17851|DexViTac]] — The *human-demo* data engine (248 demos/hr, kinematics-grounded tactile pretrain); its **83.3% → 43.3%** Pipetting SR collapse without grounded pretrain is the most damning ablation for naïve tactile fusion
> - [[2604.07335|TAMEn]] — The *closed-loop* data engine (online feasibility + AR recovery); pairs with [[2603.17851|DexViTac]] as the dual-pillar tactile collection pipeline (human bulk-pretrain → robot online-recovery refinement)
> - [[2509.07962|TA-VLA]] — Torque-aware VLA design study; the de-facto reference for which torque-integration recipe matters most under contact-rich evaluation

**Tactile Benchmarks — Decision Matrix**

| Need | Benchmark |
|---|---|
| Standardized tactile representation eval | [[2410.24090\|Sparsh]] / [[2410.24090\|TacBench]] (**6/6** tasks SOTA) |
| Multisensory touch (image + audio + vibration + force) | [[2506.14754\|Sparsh-X]] (**>3×** on force-and-vibration) |
| Closed-loop bimanual policy SR | [[2604.07335\|TAMEn]] (**75%** avg SR) |
| Dexterous human-demo pretrain + eval | [[2603.17851\|DexViTac]] (**248 demos/hr**, **85.8%** avg SR) |
| Insertion / assembly contact-grounded eval | [[2603.05687\|CGP]] |
| Soft-object humanoid manipulation | [[2510.25725\|HumanoidVTA]] (**2,124** tactile sensors) |
| Tactile-vs-vision contribution isolation | [[2510.13324\|FARM]] |
| Torque-aware VLA recipe ablation | [[2509.07962\|TA-VLA]] (none / wrist-FT / per-joint grid) |
| Full-arm skin coverage | [[2509.18830\|DexSkin]] |
| Slow-fast visuotactile control | [[2503.02881\|Reactive Diffusion Policy]] |
| Force-feedback wiping / surface task | [[2505.06451\|Adaptive Wiping]] |

> [!tip] Cross-Reference
> See [[09_Contact-Rich-and-Whole-Body-Control#3. Force-Conditioned VLA Architectures]] for the full deep-dive on how [[2410.24090|Sparsh]]/[[2506.14754|Sparsh-X]] representations feed into VLAs ([[2509.07962|TA-VLA]], [[2510.13324|FARM]], [[2603.05687|CGP]]). The benchmarks here measure *what* you're getting from touch; the policies in 10 measure *how to use it*. The tactile axis also overlaps with §2.1 bimanual data ([[2604.20444|VTouch++]], [[2604.07335|TAMEn]]) where collection and evaluation use the same hardware.

---

### 7. Soft-Body & Deformable Benchmarks

Soft body, cloth, and deformable manipulation form an evaluation axis that almost no rigid-body benchmark covers. The wave of 2025-2026 work — Gaussian-splat soft-body twins, video-derived deformable world models, physics-aware multi-body benchmarks — moved deformables from "open problem" to "evaluable category."

#### 7.1 Real-to-Sim Soft-Body Twins

Build a deformable scene's digital twin from real video / Gaussian-splat reconstruction; evaluate policies *in the twin* rather than against hand-authored deformable assets.

- **[[2511.04665|Real-to-Sim GS]]** — A real-to-sim policy-evaluation pipeline for soft-body interactions that builds a ==Gaussian-splat twin== of the deformable scene; the first standardized soft-body evaluation pipeline that doesn't require hand-authored deformable assets.
- **[[2510.21447|PhysWorld-Deformable]]** — A data-side pipeline turning real videos into world models of deformable objects via ==physics-aware demonstration synthesis==; the counterpart that converts real deformable interactions into training data.

#### 7.2 Multi-Body Physics Benchmarks

Rigid + soft + fluid + cloth in a unified evaluation suite — measures whether a policy / WAM handles *every* deformable category, not just one.

- **[[2506.02794|PhysGaia]]** — A physics-aware dynamic-novel-view-synthesis benchmark of **17** Houdini scenes spanning ==liquids + gases + viscoelastic + textiles==, with ground-truth ==3D particle trajectories== + per-material physics params (FLIP / Pyro / ==MPM== / Vellum); SOTA DyNVS (D-3DGS, 4DGS, STG) score **PSNR < 30** even multiview — unified deformable + rigid + fluid evaluation.
- **[[2401.15318|Gaussian Splashing]]** — A single 3DGS substrate unifying ==3DGS rendering kernels + Position-Based Dynamics + Position-Based Fluids== under one particle representation with ==anisotropy loss== + ==PBR materials== + ==surface tension== modeling; demonstrates robust two-way fluid-solid coupling (deformable solids in water, waves, flooding) for cloth + fluid + rigid.

#### 7.3 Deformable Scene Flow

Ground-truth scene flow for highly-deformable manipulation; the metric layer underneath soft-body benchmarks.

- **[[2312.00583|DeformGS]]** — A scene-flow method for highly deformable scenes in deformable-object manipulation that provides ==ground-truth scene flow== for evaluation.

**Soft-Body — Decision Matrix**

| Need | Benchmark |
|---|---|
| Build a soft-body digital twin from real video | [[2511.04665\|Real-to-Sim GS]] (Gaussian-splat) |
| Generate deformable training data from real interactions | [[2510.21447\|PhysWorld-Deformable]] |
| Unified deformable + rigid + fluid eval | [[2506.02794\|PhysGaia]] |
| Fluid + rigid combination in Gaussian-splat | [[2401.15318\|Gaussian Splashing]] |
| Ground-truth scene flow for deformable scenes | [[2312.00583\|DeformGS]] |

> [!star] Key Papers
> - [[2511.04665|Real-to-Sim GS]] — Build a soft-body digital twin from real video; the dominant soft-body evaluation recipe in 2026
> - [[2506.02794|PhysGaia]] — Multi-body deformable + rigid + fluid benchmark; closes the "everything that isn't a rigid box" evaluation gap
> - [[2510.21447|PhysWorld-Deformable]] — Synthesizes deformable demonstrations from videos; the data-side complement to [[2511.04665|Real-to-Sim GS]]

> [!tip] Cross-Reference
> See [[14_Sim-to-Real-Transfer#4. Real2Sim2Real Loops & Digital Twins]] for the broader real-to-sim story (rigid + soft). The papers in this section are the soft-body *evaluation* tier — they answer "did my policy work on the towel?", not "how do I cross the sim-to-real gap?". The two literatures meet at Gaussian-splat digital twins ([[2511.04665|Real-to-Sim GS]] is the bridge paper). Cross-reference [[11_Physics-Aware-Embodied-AI#1. Design-Space Principles]] for the physics-prior side and [[07_WAM#2.4 Physics-Aligned Video Generation]] for the physics-aligned video-generation track that complements deformable simulation.

---

### 8. Bimanual & Humanoid Evaluation

Humanoid whole-body manipulation and bimanual coordination form their own evaluation axis. Single-arm benchmarks ([[2306.03310|LIBERO]], [[2112.03227|CALVIN]]) cannot test the bilateral-coordination, whole-body-balance, or human-scale workspace constraints that humanoid platforms face.

#### 8.1 Humanoid Whole-Body Benchmarks

Whole-body locomotion + manipulation evaluation on bipedal humanoid platforms — tests bilateral coordination *under* whole-body balance constraints that arm-only benchmarks ignore.

- **[[2604.17335|G1 WBC-Gen+Track]]** — A whole-body humanoid locomotion system via ==diffusion motion generation + RL motion tracking==; Unitree G1 climbs **75cm** boxes, traverses stairs, vaults hurdles, with Tracker+Gen achieving **0.962 SR** on 80cm box vs **0.230** for Tracker-Only — the current reference for online terrain-aware whole-body locomotion.
- **[[2506.12851|KungfuBot]]** — A ==physics-based motion-processing pipeline== (raw video → physically feasible robot reference) + ==adaptive tracking factor== + ==asymmetric actor-critic + reference state init==; **53.25 mm** mean per-body position error on easy motions (vs **>233 mm** OmniH2O/ExBody2), zero-shot martial arts + dance on Unitree G1.
- **[[2604.07993|HEX]]** — A hierarchical VLA + ==RL whole-body controller== with ==Unified Proprioceptive Predictor + morphology MoE== + ==review-and-forecast== visual cache; **79.8%** avg SR on 7 real-robot tasks (vs **70.2%** GR00T N1.5, **57.1%** ACT), **61.8%** on unseen scenes (vs **44.3%** π0.5), pretrained on **12M+** humanoid frames.
- **[[2502.20396|Humanoid Sim2Real Dex]]** — A vision-based dex-manip ==sim-to-real RL recipe== combining ==autotuned robot modeling== + ==contact stickers== + ==stage-based rewards== + ==divide-and-conquer distillation==; on Fourier GR-1: **80%** box lift, **62.3%** grasp-and-reach, **52.5%** bimanual handover, **60–80%** zero-shot on unseen objects.
- **[[2512.01061|Sim-to-Real Door]]** — A DoorMan ==teacher-student-bootstrap== recipe in NVIDIA Isaac Lab with PPO teacher + ==staged-reset exploration== + DAgger student + ==GRPO== partial-observability fine-tune; **83%** SR on diverse real doors (matches **80%** human teleoperator), **23.8%** faster than human experts.
- **[[2605.03452|BifrostUMI]]** — A portable PICO-4 VR + UMI-inspired gripper for ==robot-free demos== feeding a hierarchical ==diffusion policy== + ==Spatial Keypoint Retargeting (SKR)== over **5** keypoints (pelvis + L/R TCPs + L/R feet); Unitree G1 executes cluttered tabletop pick-and-place + under-table waste-disposal with stepping + torso bending + knee flexion from sparse keypoints.
- **[[2510.25725|HumanoidVTA]]** — The first humanoid ==visual-tactile-action dataset== with **2,124-sensor** Inspire Hands (proprioception + egocentric vision + dense tactile) for *soft-object* manipulation across **4** tasks (towel, sponge under strong/weak pressure); ==ACT== baseline shows dense tactile separates conditions under t-SNE where sparse collapse — the dense-vs-sparse axis.
- **[[2503.05652|BRS]]** (BEHAVIOR Robot Suite) — An integrated whole-body household manipulation suite around the ==Galaxea R1== wheeled dual-arm + ==4-DoF torso==; ==JoyLo== Joy-Con teleop + ==WB-VIMA== autoregressive whole-body decoding; **88%** avg sub-task / **58%** entire-task across **5** household tasks at near-zero safety-violation; **13×**–**21×** over DP3/RGB-DP.
- **[[2502.12152|HUMANUP]]** — The first learned humanoid fall-recovery policy via ==two-stage RL curriculum== (Discovery Policy in simplified sim → Deployable Policy with full URDF + **20,000** initial postures); Unitree G1 recovers from supine at **78.3%** SR / rolls over at **98.3%** across **6 terrains** in **~6s** (vs **11s** manufacturer); canonical whole-body fall-recovery reference.

#### 8.2 Bimanual Benchmarks

Two-arm coordination evaluation — tests *timing*, *handover*, and *contact-rich dual-arm tasks* that single-arm benchmarks cannot probe.

- **[[2603.15469|RoCo Challenge]]** — An AAAI 2026 benchmark of robotic collaborative manipulation for industrial assembly (planetary gearbox); **60+ teams**, **170+ participants**, end-to-end VLA architectures (ARC-VLA) beat modular pipelines; uncovers the "Sim-to-Real Cliff" as a quantitative drop.
- **[[2604.20444|VTouch++]]** — A bimanual tactile dataset of **120,000+** episodes (**1,000+ hours**, **~36M** image frames) across **380+** tasks with ==fingertip tactile + multi-view RGB-D + proprioception==, reaching **MAE 0.022** + Expert Similarity **0.848** on real bimanual hardware — see §2 for full description.
- **[[2604.07335|TAMEn]]** — A closed-loop bimanual collection system reaching **75%** avg SR on 4 contact-rich tasks via a gripper-adaptive wearable + ==online feasibility validation== (**100%** replay vs **12–39%**) + AR-recovery refinement — see §2.1.
- **[[2604.05831|BiCoord]]** — A long-horizon tightly-coupled bimanual benchmark with ==spatial-temporal coordination metrics== (MRD/ARD/SMT/SMP/STI) + AI-coding-agent task construction; tasks show **4×** higher spatial-temporal integral than prior suites and all policies degrade in later stages.
- **[[2506.18088|RoboTwin 2.0]]** — A bimanual sim + benchmark using ==MLLM expert-code generation== + ==5-axis domain randomization==; **71.3%** auto-code SR, **+24.4%** real-world few-shot SR — the modern bimanual reference (replaces RoboTwin 1.0).
- **[[2512.24653|RoboMIND 2.0]]** — A dual-arm dataset of **310K** trajectories from **6** platforms across **759** tasks, with ==tactile feedback==, an ==Isaac Sim digital twin==, and the MIND-2 dual-system (IQL-optimized VLA).
- **[[2603.05687|CGP]]** — A contact-grounded policy using ==diffusion-predicted coupled state+tactile trajectories== + ==contact-consistency mapping== to a compliance controller; outperforms visuomotor + visuotactile baselines on **5** dexterous tasks.
- **[[2511.17441|RoboCOIN]]** — A bimanual dataset of **180,000+** demos from **15** platforms across **421** tasks with a ==hierarchical capability pyramid==; RTML filtering yields a **+23%** [[2503.14734|GR00T N1]].5 gain.
- **[[2304.13705|ALOHA]]** — An open-source bimanual platform (**<$20K**) + ==ACT (Action Chunking with Transformers)== — Transformer CVAE + temporal ensembling; the original benchmark for fine-grained tasks.
- **[[2401.02117|Mobile ALOHA]]** — A **16 DoF** mobile bimanual platform with ==whole-body teleoperation== (operator's waist tethered to base) + ==behavior cloning + co-training== over static-ALOHA data; **>90%** SR on **7** real tasks (cook shrimp / wipe wine / call elevator); co-training lifts wipe-wine **20→40%** at 25 demos, **50→95%** at 50 — the mobile-bimanual reference.
- **[[2407.07788|BiGym]]** — A ==demo-driven== **40-task** mobile bimanual benchmark with mixed scene/task complexity and ==human-teleop demonstrations==; targets the slot between static bimanual (ALOHA) and pure mobile (RoboTHOR) — closes the bimanual + mobility evaluation gap with **>200** demos per task across kitchen/living-room scenes.
- **[[2410.24185|DexMimicGen]]** — An automated bimanual data generator replaying few human demos in sim via ==SE(3)-equivariant subtask decomposition== with per-arm async + sync + ordering constraints; **76.0%** vs **0.7%** Drawer Cleanup, **80.7%** vs **3.3%** Piece Assembly; **90%** real GR-1 can-sorting from 40 sim demos vs **0%** with 4 source demos — the bimanual MimicGen extension.

**Bimanual & Humanoid — Decision Matrix**

| Need | Benchmark |
|---|---|
| Terrain-aware humanoid locomotion | [[2604.17335\|G1 WBC-Gen+Track]] (**0.962** SR on 80cm box) |
| Highly-dynamic humanoid skills (jump / kick / parkour) | [[2506.12851\|KungfuBot]] |
| Humanoid-centered cross-embodiment eval | [[2604.07993\|HEX]] |
| Humanoid sim-to-real dexterous transfer | [[2502.20396\|Humanoid Sim2Real Dex]], [[2512.01061\|Sim-to-Real Door]] |
| Humanoid soft-object tactile manipulation | [[2510.25725\|HumanoidVTA]] (**2,124** sensors) |
| Robot-free humanoid demos | [[2605.03452\|BifrostUMI]] |
| Bimanual collaborative-assembly competition | [[2603.15469\|RoCo Challenge]] |
| Bimanual sim + benchmark + data-gen (paired) | [[2506.18088\|RoboTwin 2.0]] |
| Large-scale bimanual + mobile trajectories | [[2512.24653\|RoboMIND 2.0]] (**310K** trajectories) |
| Dexterous bimanual visuotactile eval | [[2603.05687\|CGP]] |
| Low-cost bimanual baseline | [[2304.13705\|ALOHA]] |

> [!star] Key Papers
> - [[2604.17335|G1 WBC-Gen+Track]] — Online terrain-aware diffusion-motion-gen + RL-motion-track on Unitree G1; the dominant 2026 whole-body locomotion recipe (75cm box / vault / stairs)
> - [[2603.15469|RoCo Challenge]] — AAAI 2026 industrial-assembly challenge; first benchmark to formally quantify the "Sim-to-Real Cliff" for collaborative manipulation
> - [[2506.12851|KungfuBot]] — Dynamic-skill humanoid benchmark; the only published reference for kungfu-class moves on a humanoid
> - [[2604.07993|HEX]] — Cross-embodiment evaluation centered on humanoids; bridges humanoid + arm benchmarks
> - [[2506.18088|RoboTwin 2.0]] — The modern bimanual sim + benchmark + data-generator triple
> - [[2502.20396|Humanoid Sim2Real Dex]] — Sim-to-real RL on humanoid hands; reference baseline for visual + dynamics gap

> [!tip] Bimanual ≠ "Two LIBEROs"
> Two-arm benchmarks are not the union of two single-arm benchmarks. The novel failure modes are *coordination* (timing between arms), *bilateral handover*, and *whole-body balance* under coupled arm motion. [[2506.18088|RoboTwin 2.0]] and [[2512.24653|RoboMIND 2.0]] explicitly stress these modes; running [[2306.03310|LIBERO]] twice does not. Cross-reference [[09_Contact-Rich-and-Whole-Body-Control#4. Contact-Rich Manipulation Benchmarks and Visuotactile Policies]] for the tactile-policy side of bimanual contact-rich tasks, [[14_Sim-to-Real-Transfer#5. Evaluation & Reality-Gap Measurement]] for the "Sim-to-Real Cliff" diagnostic surfaced by [[2603.15469|RoCo Challenge]], and §2.1 above for the bimanual *data* side.

---

### 9. Spatial Reasoning & 3D Benchmarks

Evaluating whether robots (and their VLM backbones) actually understand 3D space, object relationships, and spatial reasoning.

Spatial reasoning evaluation tests whether models understand *where things are relative to each other* — not just what they are. The benchmark progression spans three difficulty tiers: **single-step relations** (distance, size, containment, left-of, counting), **compositional multi-step inference** ("cup on table, table in kitchen, where is cup?"), and **temporal-spatial reasoning** in video (tracking, occluded-state, trajectory prediction). Most frontier VLMs still fail tasks humans find trivial, exposing a persistent gap between language understanding and physical understanding.

#### 9.1 Single-Step Spatial Cognition

Probes the *atomic* spatial relations — distance, size, containment, left-of, counting — that compositional reasoning is built on. Failures here propagate up to the multi-step tier.

- **[[2410.06468|SPACE]]** — A ==cognitive-science-grounded== benchmark split into ==large-scale== (direction/distance, map sketching, route retracing) and ==small-scale== (==mental rotation==, ==perspective taking==, maze); frontier models score near chance (vs **80–100%** human) on large-scale and **<30%** SPL navigation — a fundamental VLM-vs-human gap.
- **[[2505.05456|SITE]]** — A ==cognitive-science-derived== VLM spatial benchmark with ==Ego-exo View Association + Shuffled Frames Reordering== + ==Chance-Adjusted Accuracy (CAA)==; GPT-4o **37.8%** CAA (vs **67.5%** human), only **28.20%** on Ego-exo (vs **100%** human); SITE-CAA Pearson **0.902** with LIBERO-Spatial manipulation SR.
- **[[2510.19400|MV-RoboBench]]** — A *multi-view* spatial-reasoning benchmark of **1,708** human-curated QA across **8** subtasks (3D Spatial Consistency, Cross-View Matching, Action Planning, Affordance); GPT-5 reaches **56.41%** vs **91.04%** human, dropping **−18.73%** under vertical flips; reasoning correlates with execution, yet synthetic novel views often *hurt*.
- **[[2602.20901|SpatiaLQA]]** — A benchmark of **9,605** image–text QA pairs / **241** indoor scenes with explicit ==precondition annotations== + ==Recursive Scene Graph Assisted Reasoning (RSGAR)==; GPT-5 best at **F1 76.0** content / **47.0** preconditions (vs **97.6 / 92.5** human) — reveals causal-reasoning deficiency.
- **[[2603.19231|MonoArt]]** — An end-to-end ==progressive structural reasoning== pipeline (geometry-aware → part-aware → motion-aware) with ==TRELLIS 3D Generator== + ==Dual-Query Motion Decoder==; **Chamfer 0.77** (vs 1.26) + **Type Accuracy 88.26%** (vs 77.12%) on PartNet-Mobility; **4.63/5** geometric, **4.37/5** kinematic on in-the-wild study at **20.5 s** per instance.
- **[[2602.21992|PanoEnv]]** — A ==geometry-grounded panoramic (ERP) spatial benchmark== (**14.8K** QA from TartanAir 3D ground truth) + ==PanoEnv-RL== (GRPO geometry-aware rewards + two-stage curriculum); lifts Qwen2.5-VL-7B open-ended accuracy **6.39% → 14.83%** (**+132%**), transfers zero-shot to real OSR-Bench beating the 72B baseline — 360° distortion as an unsolved spatial axis.
- **[[2412.07755|SAT]]** — A ==Spatial Aptitude Training== data engine using ==3D simulators== to procedurally generate static + **5-category dynamic** spatial QA (egocentric/object movement, allocentric, goal-aiming, action-consequence); SAT-tuning LLaVA-1.5-13B improves CVBench/BLINK **+23.9%** to **75.6%**, transfers to real images **+13.3%** — sim-generated dynamic supervision.

#### 9.2 Compositional Multi-Step Spatial Reasoning

Tests *chained* spatial inference (e.g., "cup on table, table in kitchen, where is cup?") — the next failure tier above atomic relations.

- **[[2603.18892|MultihopSpatial]]** — A benchmark of **4,500** manually annotated VQA samples with ==ground-truth bounding boxes== + ==Acc@50IoU== metric (answer + box IoU ≥ 0.5); best VLM hits **40.6%** Acc@50IoU, collapsing to **8.5%** on 3-hop ego-centric (GPT-5.2-Thinking); **59%** of correct answers lack proper grounding; RL post-training improves Libero by **+4.2pp**.
- **[[2507.18342|EgoExoBench]]** — The first ==cross-view ego/exo== benchmark with **7,300+** MCQs across ==semantic alignment / view transition / temporal reasoning== (11 subtasks); Gemini 2.5 Pro **51.7%** vs **90.1%** human; perfect-human Egocentric Wearer ID exposes major cross-view ID-inference gap; CoT prompting *degrades* performance.
- **[[2601.15224|PROGRESSLM]]** — A ==PROGRESS-BENCH== benchmark with answerability + viewpoint variants + ==two-stage episodic-retrieval + mental-simulation== reasoning; Qwen2.5-VL-3B + CoT-SFT + RL outperforms GPT-5 and Qwen2.5-VL-**72B** on NSE + PRC + unanswerable-case recognition.

#### 9.3 Spatial-Temporal Reasoning in Video

Extends spatial reasoning from static frames to *temporal sequences* — tracking, occlusion reasoning, trajectory prediction.

- **[[2511.04670|Cambrian-S]]** — A four-stage ==spatial supersensing hierarchy== + ==VSI-SUPER== (Visual Spatial Recall + Counting on arbitrarily-long video) + ==predictive sensing== with "surprise"-driven memory; Cambrian-S sets SOTA **67.5%** on VSI-Bench using **VSI-590K**; maintains stable VSR accuracy across arbitrary video lengths where Gemini-2.5-Flash collapses.
- **[[2601.09430|Video-MSR]]** — A benchmark of **4,993** dual-phase-verified video-QA pairs across 4 MSR tasks (Constrained Localization, Chain Retrieval, Route Planning, Counterfactual Physical Deduction); SOTA MLLMs only **20–44%** (Qwen3-VL-8B **43.92%**, GPT-4o **41.87%**); MSR-9K fine-tuning lifts Qwen2.5-VL-7B by **+7.82%** overall, **+48.62%** on Route Planning.
- **[[2503.23765|STI-Bench]]** — A benchmark of **300+** real-world videos / **2,000+** QA across ==8 tasks== (static: dimensional / spatial / 3D grounding; dynamic: displacement / speed / ego-orientation / trajectory / pose) with ground-truth 3D annotations; Gemini-2.5-Pro tops at **41.4%** avg (only **33.1%** Speed&Acceleration), exposing quantitative spatial-numerics weakness.

#### 9.4 Interactive Embodied Spatial Reasoning Benchmarks

Static VQA tells you what a VLM *recognizes*; **interactive embodied benchmarks** tell you what it can *do* in a 3D world. This tier evaluates MLLMs as agents that observe egocentric frames, choose actions, and receive environmental feedback — closing the loop between perception and action. The four entries below are the modern frontier, each targeting a different failure mode (interaction, 3D rotational geometry, EQA grounding, physics).

- **[[2501.11858|EmbodiedEval]]** — A benchmark of **328 tasks** on the ==LEGENT platform== covering navigation, object interaction, social interaction, attribute QA, and spatial QA; best MLLM (GPT-4o) hits only **25.00%** overall vs **97.26%** non-expert human and interaction tasks collapse to **10–12%**, exposing the long-horizon and ego-centric brittleness of frontier MLLMs.
- **[[2603.13033|ESPIRE]]** — A diagnostic benchmark in ==Isaac Sim== decomposing tasks into ==3D localization== (2D pixel coords) and ==6-DoF execution== (goal poses), probing spatial *aspects* × reference frames × objects; VLMs are stronger at localization than execution — they lack robust 3D rotational geometry, and reflection feedback *improves* localization but *degrades* execution.
- **[[2503.11117|EXPRESS-Bench]]** — An embodied-QA benchmark in ==Habitat + HM3D== with **777** trajectories / **2,044** QA pairs + novel ==Exploration-Answer Consistency (EAC)== metric; companion **Fine-EQA** combines ==frontier-based + goal-oriented exploration== (**40.55%** C, **16.22%** E_path; **+42%** path-length cut on HM-EQA) and punishes answers hallucinated without observing the scene.
- **[[2602.21015|CHAIN]]** — An interactive 3D physics benchmark with **109 levels** across ==interlocking mechanical puzzles== + ==3D stacking/packing== (Unity + Python engine) under ==closed-loop action-and-feedback== eval; best VLM (GPT-5.2) hits **22.9%** Pass@1 and puzzle tasks are near-zero even at "easy". Cross-listed in [[11_Physics-Aware-Embodied-AI#6. Physics Commonsense Benchmarks]].

**Spatial Reasoning — Decision Matrix**

| Need | Benchmark |
|---|---|
| Atomic spatial cognition (distance, size, containment, counting) | [[2410.06468\|SPACE]] |
| Comprehensive multi-axis spatial eval | [[2505.05456\|SITE]] |
| Spatial language QA | [[2602.20901\|SpatiaLQA]] |
| Monocular articulated-object reasoning | [[2603.19231\|MonoArt]] |
| Compositional multi-hop spatial inference | [[2603.18892\|MultihopSpatial]] |
| Viewpoint-invariant ego+exo reasoning | [[2507.18342\|EgoExoBench]] |
| Progress-aware spatial reasoning | [[2601.15224\|PROGRESSLM]] |
| Video-spatial / occlusion / tracking | [[2511.04670\|Cambrian-S]] |
| Multi-step video spatial reasoning | [[2601.09430\|Video-MSR]] |
| Joint spatial-temporal intelligence | [[2503.23765\|STI-Bench]] |
| Interactive embodied agent (Navigation + Interaction + QA) | [[2501.11858\|EmbodiedEval]] |
| 3D rotational geometry + 6-DoF execution probe | [[2603.13033\|ESPIRE]] |
| Exploration-grounded Embodied QA | [[2503.11117\|EXPRESS-Bench]] |
| Interactive 3D physics reasoning | [[2602.21015\|CHAIN]] |

> [!star] Key Papers
> - [[2505.05456|SITE]] — Comprehensive spatial intelligence evaluation across multiple reasoning types
> - [[2410.06468|SPACE]] — Systematic evaluation of spatial cognition in VLMs; reveals gap between VLM and human spatial reasoning
> - [[2601.09430|Video-MSR]] — Multi-step spatial reasoning benchmark for video understanding
> - [[2511.04670|Cambrian-S]] — Spatial supersensing in video; extends spatial benchmarks from static frames to temporal sequences

> [!tip] The Spatial Gap — and the Static-vs-Interactive Cliff
> Current VLMs and VLAs consistently underperform on spatial reasoning benchmarks compared to object recognition tasks. [[2410.06468|SPACE]] and [[2505.05456|SITE]] show this is a fundamental representation issue, not just a data issue. The gap *widens* under interaction: the headline finding across §9.4 is that VLMs scoring **>70%** on §9.1–9.3 static-image VQA *collapse* to **10–30%** as soon as they must act and receive feedback — the bottleneck is not perception but closed-loop action-observation alignment, which ==generative evaluation== ([[2603.13033|ESPIRE]]'s localization-vs-execution decomposition) exposes. The same model that correctly *answers* "the cup is left of the bowl" cannot reliably *pick the cup up from the left*. Papers like [[2501.15830|SpatialVLA]] and [[2506.22242|4D-VLA]] attempt to close the representation gap architecturally. Cross-reference [[06_VLA-Reasoning-and-CoT#1. The Four Reasoning Insertion Slots]] for the reasoning-side responses to these failures and [[05_VLA#3. Spatial & 3D-Aware VLAs]] for 3D-aware architectures.

---

### 10. Long-Horizon Task Benchmarks

Most VLA benchmarks evaluate a single short task. Long-horizon evaluation tests whether a policy can chain skills, plan subgoals, recover from intermediate failures, and maintain task identity over minutes-long episodes.

#### 10.1 Long-Horizon Manipulation Suites

Multi-step manipulation evaluation — chained skills with episode-level success rather than per-step success.

- **[[2506.06677|RoboCerebra]]** — A large-scale long-horizon benchmark whose tasks average **2,972.4 sim steps** (~**6×** prior datasets), with **1,000 human-annotated trajectories**, **100 task variants**, **10,000+ step-level segments**; Hierarchical Planning + Execution (HPE) reaches **13.21%** in "Mix" where [[2406.09246|OpenVLA]] gets 0%, and GPT-4o tops VLM planning at **68.33%**.
- **[[2305.12821|FurnitureBench]]** — A reproducible real-world furniture-assembly benchmark on Franka Panda + ==3D-printable furniture models== + Dockerized stack + **200+ hours** / **5,000+ demos** + ==FurnitureSim==; **75–93%** cross-lab reproducibility; both BC + IQL **fail** to complete any full assembly (inserting **0–20%** SR, screwing **0–10%**).
- **[[2112.03227|CALVIN]]** — A long-horizon benchmark of a **7-DOF arm** in 4 environments × **34 tasks** with **~24 hours** of teleop play + 1% language-annotated by 400+ crowd workers + ==multi-task long-horizon== + ==zero-shot generalization== protocols; MCIL baseline **53.9%** single task but only **0.08%** on 5-instruction chains, **~0%** zero-shot on chains of ≥2.
- **[[2604.21924|LoHo-Manip]]** — A hierarchical ==VLM task manager + VLA executor== with ==receding-horizon== plan + ==visual-trace conditioning==; **97.5%** avg LIBERO, RoboVQA BLEU **63.1**, EgoPlan-Bench2 **56.7%**, **0.39** vs **0.24** π0.5 on VLABench.
- **[[2605.01772|Anticipation-VLA]]** — An ==Anticipation Model== generating ==recursive multimodal (text+image) subgoals== adaptive in granularity + ==Optimal Value Function== for progress re-planning every K steps; **80.8%** avg LIBERO, **+107%** improvement on unseen real-world configurations vs π0.5.
- **[[2410.22689|SIRIUS-FLEET]]** — A multi-robot fleet-learning framework + ==visual-world-model runtime monitor== with ==adaptive anomaly thresholds==; autonomous SR **+13%** sim (RoboCasa) / **+45%** real (Mutex) over 3 deployment rounds; **>95%** combined-policy performance.

#### 10.2 Mobile + Long-Horizon (Combined)

Long-horizon mobile-then-manipulate composition — tests whether navigation skills and manipulation skills chain across episodes.

- **[[2512.24653|RoboMIND 2.0]]** — A dataset whose **310K** trajectories include mobile-manipulation episodes covering the long-horizon ==mobile-then-manipulate== composition.

#### 10.3 Language-Conditioned Long-Horizon

Testing the harder problem: following language instructions over extended task horizons with compositional generalization. The standard `[[2306.03310|LIBERO]]` is now ceiling-saturated at **~97%**; modern work pivots to *perturbation* and *paraphrase* axes.

- **[[2306.03310|LIBERO]]** — A lifelong robot-learning benchmark on ==Robosuite== — **130** tasks across **4** suites (Spatial / Object / Goal / 100) ==procedurally generated== from Ego4D activity templates + ==PDDL==, with **50** teleop demos/task; VLAs and WAMs now both hit ~**97%** — ceiling reached on standard manipulation.
- **[[2112.03227|CALVIN]]** — The most-cited compositionality benchmark, where the MCIL baseline reaches **53.9%** single-task but only **0.08%** on 5-instruction chains and **~0%** zero-shot on chains of ≥2.
- **[[2510.13626|LIBERO-Plus]]** — A visual perturbation diagnostic (==7-axis robustness==); WAMs outperform VLAs by large margins (VLA-JEPA: **79.5%**).
- **[[2505.15660|AGNOSTOS]]** — An RLBench-based zero-shot benchmark with **23** unseen tasks; existing VLAs cap at **17.5%** SR (8+ tasks at 0%); ==X-ICM== with ==dynamics-guided in-context selection== via diffusion hits **30.1%** (+12.6pp).
- **[[2305.12821|FurnitureBench]]** — A multi-step assembly benchmark with **200+ hours** / **5,000+ demos** + ==FurnitureSim==; BC/IQL both **fail** all full assembly tasks (inserting **0–20%** SR).
- **[[2506.18088|RoboTwin 2.0]]** — A bimanual sim + benchmark using ==MLLM expert-code generation== + ==5-axis domain randomization==; **+24.4%** real-world few-shot, **+21.0%** zero-shot — the modern bimanual reference.

#### 10.4 The LIBERO Family — Testing Different Failure Modes

The same parent benchmark re-released along distinct *language-conditioned long-horizon* axes — each child exposes a different over-fit / brittleness mode that the standard suite hides. (Absorbed from former §11; the precision/perturbation diagnostics in this table are also surfaced in §5.3 from the diagnostic-stack angle — same papers, different framing.)

| Benchmark | What It Tests | Key Finding |
|-----------|--------------|-------------|
| [[2306.03310\|LIBERO]] | Standard manipulation (4 suites) | VLAs and WAMs both achieve ~**97%** — ceiling reached |
| [[2510.13626\|LIBERO-Plus]] | Visual perturbations (camera, lighting, background) | WAMs outperform VLAs by large margins; VLA-JEPA: **79.5%** |
| [[2510.03827\|LIBERO-PRO]] | Minor perturbations on [[2306.03310\|LIBERO]] tasks | VLAs collapse from **>90% → near 0%** under small changes |
| [[2602.06556\|LIBERO-X]] | Cross-task generalization | Only **39.4%** at easiest level — massive unsolved gap |
| [[2603.28301\|LIBERO-Para]] | Paraphrased instructions | **22–52pp drops** — models overfit to exact instruction phrasing |

**Long-Horizon — Decision Matrix**

| Need | Benchmark |
|---|---|
| Multi-step assembly (the hardest published) | [[2305.12821\|FurnitureBench]] |
| ~6× longer than CALVIN/LIBERO trajectories | [[2506.06677\|RoboCerebra]] (**2,972.4** avg steps) |
| Trace-conditioned plan-fidelity eval | [[2604.21924\|LoHo-Manip]] |
| Subgoal-prediction eval (planning vs interpolation) | [[2605.01772\|Anticipation-VLA]] |
| Multi-robot fleet long-horizon | [[2410.22689\|SIRIUS-FLEET]] |
| Mobile + manipulation composition | [[2512.24653\|RoboMIND 2.0]] |
| Standard language-conditioned long-horizon | [[2112.03227\|CALVIN]], [[2306.03310\|LIBERO]] (saturated at ~97%) |
| Cross-task instruction transfer | [[2505.15660\|AGNOSTOS]], [[2602.06556\|LIBERO-X]] (**39.4%** easiest) |
| Visual perturbation robustness | [[2510.13626\|LIBERO-Plus]] (**79.5%** VLA-JEPA) |
| Memorization vs generalization (small-perturbation collapse) | [[2510.03827\|LIBERO-PRO]] (**>90% → ~0%**) |
| Language paraphrase overfit | [[2603.28301\|LIBERO-Para]] (**22–52pp** drops) |

> [!star] Key Papers
> - [[2306.03310|LIBERO]] — Lifelong robot learning benchmark; tests continual learning and long-horizon capability; **~97%** saturation point that anchors the family of perturbation children
> - [[2112.03227|CALVIN]] — Standard for long-horizon, language-conditioned policy evaluation; most-cited compositionality benchmark
> - [[2305.12821|FurnitureBench]] — Multi-step assembly remains the hardest published long-horizon manipulation benchmark
> - [[2604.21924|LoHo-Manip]] — Trace-conditioned long-horizon evaluation; pairs episode success with planning-trace fidelity
> - [[2605.01772|Anticipation-VLA]] — Subgoal-level evaluation; surfaces whether the model is planning vs interpolating
> - [[2510.13626|LIBERO-Plus]] — Diagnostic layer: VLAs are brittle despite high [[2306.03310|LIBERO]] scores; **7** perturbation dimensions expose real-world gaps

> [!tip] Long-Horizon Failure Modes
> Long-horizon policies fail through three distinct routes: **(a) skill drift** — the model executes the wrong skill at step N+1 even though step N succeeded; **(b) state confusion** — the model loses track of which subgoal is active; **(c) terminal collapse** — early successful steps consume the model's context budget and the final step is executed by a "forgetful" policy. Different benchmarks stress different routes — [[2604.21924|LoHo-Manip]] stresses (b), [[2605.01772|Anticipation-VLA]] stresses (c), [[2305.12821|FurnitureBench]] stresses (a). Pair them. The orthogonal failure axis is *language brittleness* — [[2510.13626|LIBERO-Plus]] and [[2510.03827|LIBERO-PRO]] show that models scoring >90% on standard [[2306.03310|LIBERO]] fail badly under perturbations, so always pair standard benchmarks with diagnostic ones. Cross-reference [[05_VLA#6. RL Post-Training for VLAs]] for the RL-post-training response to long-horizon failures, [[06_VLA-Reasoning-and-CoT#1. The Four Reasoning Insertion Slots]] for the planning-level reasoning recipes, and [[13_Self-Evolving-VLA-WAM#4. Failure Detection, Diagnosis & Recovery]] for failure-detection.

---

### 11. World Model Benchmarks

Evaluating whether learned world models generate physically plausible, action-consistent, long-horizon predictions.

- **[[2605.25874|WBench]]** — A ==multi-turn interactive video-WM benchmark== (**289** cases / **1,058** turns) scoring five roles (Renderer/Director/Controller/Memory/Engine) via **22** sub-metrics; native-control models beat text-driven by ~**10** points on navigation, perspective-switching collapses to **30.7**, and navigation drops **33** points by Turn 4+ — exposing spatial-frame drift.
- **[[2605.21800|stable-worldmodel]]** — An open-source ==reproducible WM platform== (PyTorch + Gymnasium + Lance data layer) with controllable Factors-of-Variation for OOD robustness studies; reproduces LeWM **94%** / DINO-WM **92%** Push-T in-distribution but planning decays sharply under mild visual perturbation, and prediction-error magnitude correlates *weakly* with planning success.
- **[[2605.08567|ACWM-Phys]]** — An ==action-conditioned video-WM physics benchmark== of **8** envs (rigid/deformable/particle/kinematic) with InD vs OoD physical-shift protocols + the ACWM-DiT baseline; strong in-distribution (Push Rope **M-MSE 2.61** / **SSIM 0.988**) but large OoD drops (Robot Arm **ΔM-MSE +40.35**, Cloth Move **+29.99**), with model scale improving OoD robustness most.
- **[[2604.22152|dWorldEval]]** — A ==discrete-diffusion WM for policy evaluation== treating actions as primary tokens + ==sparse keyframe memory== + a ==discrete progress token== for automatic success detection; Pearson **~0.9–0.92** with real success across LIBERO/RoboTwin/real and LPIPS **0.243** at a 20-step round-trip horizon, ranking diverse policies without hardware.
- **[[2603.25887|WR-Arena]]** — A ==World Reasoning Arena== scoring WMs on Action-Simulation Fidelity / Long-horizon Forecast / Simulative-Reasoning-&-Planning via ==LLM action-proposers + VLM judges==; MiniMax leads fidelity (**72.33%** agent / **51.67%** env), a PAN+VLM planner adds **+26.33%** open-ended / **+23.40%** structured, no model exceeds **65%** long-horizon consistency.
- **[[2603.22212|Omni-WorldBench]]** — The first ==interaction-centric== WM evaluation with ==Omni-WorldSuite== (1,068 prompts × 3 levels) + ==Omni-Metrics== agent-based protocol (long-horizon consistency / causal faithfulness / event chronology); Wan2.2 + Cosmos lead at **75.92%** / **75.42%** AgenticScore; WonderWorld trades **84.96%** long-horizon for **24.89%** non-target stability.
- **[[2506.00613|WorldGym]]** — An ==action-conditioned latent DiT== trained on robot data + ==VLM (GPT-4o) reward computation== eliminating hand-coded rewards; Pearson **r = 0.78** with real-world success on 17 Bridge tasks, mean SR differs by only **3.3%**; preserves relative rankings across RT-1-X / Octo / OpenVLA.
- **[[2603.23497|WildWorld]]** — A game-scale WM benchmark of **108M** frames from *Monster Hunter: Wilds* with **119** annotation columns / **29** monster species / **450+** actions + ==Action Following + State Alignment metrics==; AF metric **85%** human-judgment agreement; SkelCtrl reaches **92.81%** AF + **22.03%** SA.
- **[[2510.10125|CTRL-WORLD]]** — A ==Stable-Video-Diffusion== world model adapted with ==multi-view joint prediction== + ==pose-conditioned memory retrieval== + ==frame-level action conditioning==; in-imagination fine-tuning lifts π0.5 from **38.7% → 83.4%** (**+44.7pp**) on novel-object + novel-instruction tasks.
- **[[2510.19430|GigaBrain-0]]** — A ==Mixture-of-Transformers== VLA with RGBD + ==Action Diffusion Transformer== + ==Embodied CoT== supervision + ==GigaWorld synthetic data engine== (Real2Real/Sim2Real/View/Human transfers); **+30%** laundry-folding SR, **>80%** novel-viewpoint, **>90%** unseen-placement; GigaBrain-0-Small hits **80%** at **12.5%** parameters / **9×** lower latency.
- **[[2603.22078|WAM vs VLA Robustness]]** — A comparison of VLAs, WAMs, and hybrids over a ==21-sub-dimension / 7-category== perturbation taxonomy on ==LIBERO-Plus== + ==RoboTwin 2.0-Plus==; WAMs more visually robust (LingBot-VA **74.2%** bimanual, Cosmos-Policy **82.2%** LIBERO-Plus) but data-rich π0.5 matches (**85.7%**) at **4.8×** faster — diffusion is the latency cost.
- **[[2602.05986|RISE-Video]]** — A benchmark of **467 human-annotated samples** across 8 reasoning categories + ==4-dim eval== (Reasoning Alignment / Temporal Consistency / Physical Rationality / Visual Quality) + ==LMM (GPT-5) auto-judging==; best TI2V Hailuo 2.3 only **22.5%** across 11 models, exposing logical-reasoning collapse despite visual fidelity.
- **[[2604.11689|LARY]]** — A ==Latent Action Representation== quantitative benchmark with **1.2M+** videos + **595K** trajectories from an ==automated data engine==; V-JEPA 2 + DINOv3 (no action supervision) hit **76.62%** / **68.68%** semantic accuracy vs Embodied LAMs at **17.99–20.90%**, proving general visual backbones beat specialized embodied LAMs.
- **[[2603.09030|PlayWorld]]** — An ==autonomous robot self-play data collection== framework via VLM ==Task Proposer + VLA Task Executer== + ==curriculum learning== on Stable-Video-Diffusion; Pearson **0.8766** with real-world policy success, up to **+65%** real-world SR via in-model fine-tuning, broader contact-rich coverage than human demos.
- **[[2601.15282|RBench]]** — A robot-oriented video-generation benchmark scoring ==physical realism + task correctness== across 5 domains, paired with ==RoVid-X== — a **4M**-annotated-clip robotic video dataset; automated MLLM metrics hit **0.96** Spearman with human preference, and RoVid-X fine-tuning lifts open generators across all 5 domains / 4 embodiments.
- **[[2601.07823|Video Generation in Robotics Survey]]** — A review positioning ==diffusion / flow-matching video models== as embodied world models across **4** application areas (IL data-gen, RL dynamics/rewards, policy evaluation, visual planning) + **10** challenges (hallucination, physics violation, uncertainty, cost); maps the WM-as-evaluator + WM-as-environment literature.
- **[[2505.19017|WorldEval]]** — A ==WM-as-evaluator== framework generating policy-execution video via ==Policy2Vec latent-action injection== + ==LLM (Gemini-2.0) success detection==; **0.79** Pearson with real-world SR, beats real-to-sim on MMRV + correlation, and flags unsafe policies pre-deployment — video generation as a safer-than-hardware policy test bed.
- **[[2410.18072|WorldSimBench]]** — A 4-stage ==predictive-model hierarchy== (S0–S3, S3 = "World Simulator") + dual ==Explicit Perceptual== and ==Implicit Manipulative== (closed-loop task SR) evaluation; its ==HF-Embodied== dataset trains a Human Preference Evaluator beating GPT-4o alignment — current video models largely fail to capture physical rules for *actionable* generation.
- **[[2505.09694|EWMBench]]** — The first embodied-WM generation benchmark on ==AgiBot-World== scoring ==Visual Scene Consistency (DINOv2)== + ==Motion Correctness (YOLO-World HSD/NDTW/DYN)== + ==Semantic Alignment==; domain-adapted models beat general video generators, motion correctness the hardest axis — separates "good embodied WM" from "good video model".

World model evaluation has shifted from passive video quality metrics (FVD, SSIM) to *interactive* benchmarks that test whether the model can predict consequences of actions. Two axes drive the new generation: **action-following fidelity** (given an action, does the predicted next frame match the actual outcome?) and **causal consistency** (do counterfactual actions produce counterfactual futures?). The most ambitious framing — **WM-as-environment** — replaces "is the video pretty?" with "does a policy trained inside the WM transfer to real?".

**World Model Benchmarks — Decision Matrix**

| Need | Benchmark |
|---|---|
| Interaction-centric WM eval (causal + chronology) | [[2603.22212\|Omni-WorldBench]] (**75.92%** AgenticScore) |
| WM-as-environment (policy-transfer fidelity) | [[2506.00613\|WorldGym]] (**r=0.78** with real success), [[2603.09030\|PlayWorld]] (**0.8766**) |
| Action-following + state-alignment on game-scale data | [[2603.23497\|WildWorld]] (**108M** frames, AF/SA metrics) |
| In-imagination policy fine-tuning | [[2510.10125\|CTRL-WORLD]] (π0.5 **38.7% → 83.4%**) |
| WAM-vs-VLA robustness trade-off | [[2603.22078\|WAM vs VLA Robustness]] (**4.8×** slower, more robust) |
| Video-generator rule-induction / reasoning probe | [[2602.05986\|RISE-Video]] (best TI2V only **22.5%**) |
| Latent-action representation quality | [[2604.11689\|LARY]] (**1.2M+** videos; general backbones beat embodied LAMs) |
| Integrated WM-powered VLA stack | [[2510.19430\|GigaBrain-0]] (**+30%** laundry SR) |

> [!star] Key Papers
> - [[2603.22212|Omni-WorldBench]] — First interaction-centric evaluation for world models; tests causal consistency and action following
> - [[2603.22078|WAM vs VLA Robustness]] — Systematic comparison: WAMs are more robust to visual perturbations but 4.8x slower
> - [[2506.00613|WorldGym]] — World model AS environment; evaluates by training policies *inside* the world model and measuring downstream transfer
> - [[2510.10125|CTRL-WORLD]] — Controllable generative world model for robot manipulation; standardizes the controllability evaluation axis
> - [[2510.19430|GigaBrain-0]] — World-model-powered VLA; integrated-stack evaluation
> - [[2603.23497|WildWorld]] — 108M frames from Monster Hunter: Wilds with explicit state annotations; Action Following and State Alignment metrics
> - [[2602.05986|RISE-Video]] — Probes whether video generators decode implicit world rules; rule-induction evaluation

> [!tip] Beyond Visual Quality
> Early world model evals focused on video quality (FID, FVD). 2026 benchmarks ([[2603.22212|Omni-WorldBench]], [[2603.23497|WildWorld]], [[2506.00613|WorldGym]]) shifted to *interaction fidelity*: does the model follow actions? Are state transitions consistent? Can a policy trained inside the world model transfer to real? This is what matters for robot control.

---

## Part E — Synthesis & Decision Aids

*Cross-cutting design studies, survey papers, evaluation hierarchies, and recommended stacks. Use these to assemble the right combination from Parts A–C.*

### 12. Sim-to-Real Transfer Evaluation

Bridging the reality gap: does simulation performance predict real-world success?

> [!info] Full Deep-Dive
> This section gives the evaluation-focused subset of the sim-to-real story. **See [[14_Sim-to-Real-Transfer]] for the full deep-dive** covering learned simulators, policy-side robustness (DR, robust RL), real2sim2real digital twins, integration patterns, and open problems.

- **[[2606.05159|X4Val]]** — A variance-reduced policy-validation method from *non-paired* auxiliary data: a ==neural surrogate== feeds an unbiased ==control-variate estimator== with cross-fitting; **15–20%** variance reduction in new driving regions, **38.4%** for iterative development — removes the explicit-pairing requirement of classic control variates.
- **[[2405.05941|SimplerEnv]]** — The first reliable sim-real correlation benchmark (Pearson **r > 0.85**) via system identification + green-screening; introduces MMRV ranking metric.
- **[[2605.06311|VISER]]** — A ray-traced PBR + MLLM-driven asset-generation benchmark (1,000+ assets); pushes correlation to **r = 0.92** and pinpoints specular highlights + contact shadows as load-bearing visual cues.
- **[[2604.10856|BridgeSim]]** — A cross-simulator closed-loop eval platform decomposing the open-loop vs closed-loop gap into ==Observational Domain Shift== + ==Objective Mismatch==; a training-free ==Test-Time Adaptation== (==flow-matching observational calibrator== + truncated Q-value estimator + adaptive replan) adds **+19.1** Driving Score with RAP in IDM mode.
- **[[2604.24018|Sim2Real Betting]]** — A ==sequential-betting== variance-reduction method reframing sim-real estimation: a ==Cover universal-portfolio==-inspired approximation combines diverse simulators into ==Kelly-style bet sizes== via a ==double-betting mechanism== tolerating simulator bias; **70–100%** win rates over Monte Carlo, domain-randomized sim banks converging fastest.
- **[[2511.04665|Real-to-Sim GS]]** — A soft-body twin pipeline combining ==3D Gaussian Splatting== rendering + ==PhysTwin== twins + ==NVIDIA Warp== engine; Pearson **r > 0.9** sim-real across plush toy / rope / T-block, beating IsaacLab (**r=0.915** vs **r=0.649** for T-block pushing).
- **[[2506.06440|Vid2Sim]]** — A two-stage pipeline (==LGM + VideoMAE== feed-forward init → ==3D Gaussian Splatting== refinement + ==Neural Jacobian== implicit-Euler dynamics); **PSNR 30.17** vs PAC-NeRF **22.06**, **~15 min**/scene vs **54–120 min**, **PSNR 25.07** future-state vs **20.11**.

The sim-to-real evaluation problem has two components: the *visual* gap (rendered vs real images) and the *dynamics* gap (simulated vs real physics). The field has converged on three attack strategies: (1) **better correlation benchmarks** that quantify how predictive sim-success is of real-success (Pearson r); (2) **better statistical estimators** that reduce variance in real-rollout count needed for a confident sim-real comparison; (3) **real-to-sim closures** that rebuild the deployment scene from video as a re-evaluable digital twin. Each new entry pushes Pearson r toward 1.0 (current best: **r = 0.92**) by closing a specific failure mode — specular highlights, contact shadows, observation-distribution shift, or asset diversity.

**Sim-to-Real Evaluation — Decision Matrix**

| Need | Benchmark |
|---|---|
| Canonical sim-real correlation baseline | [[2405.05941\|SimplerEnv]] (**r > 0.85**, MMRV metric) |
| Highest-fidelity visual correlation | [[2605.06311\|VISER]] (**r = 0.92**, PBR + ray-tracing) |
| Decompose OL-vs-CL gap | [[2604.10856\|BridgeSim]] (observational shift + objective mismatch) |
| Variance-reduced sim-real estimation | [[2604.24018\|Sim2Real Betting]] (**70–100%** win vs Monte Carlo) |
| Soft-body / deformable real-to-sim twin | [[2511.04665\|Real-to-Sim GS]] (**r > 0.9**), [[2506.06440\|Vid2Sim]] (**PSNR 30.17**) |

> [!star] Key Papers
> - [[2605.06311|VISER]] — Ray-tracing + PBR materials + MLLM-driven asset generation; **0.92** sim-to-real Pearson correlation; pinpoints specular highlights and contact shadows as the load-bearing visual cues for VLA policies
> - [[2405.05941|SimplerEnv]] — First reliable sim-real correlation benchmark (**r > 0.85**); introduces MMRV ranking metric; enables cheap, reproducible policy evaluation without hardware
> - [[2604.10856|BridgeSim]] — Decomposes OL-CL gap into observational shift + objective mismatch; **+19.1 DS** via training-free TTA; sim-to-real is a paradigm gap, not a data gap
> - [[2511.04665|Real-to-Sim GS]] — Gaussian-splat soft-body twins close the loop for deformables

> [!tip] Correlation Is the Currency
> Sim-to-real *evaluation* converges on one number: how predictive is sim-success of real-success (Pearson r)? The frontier pushes r toward 1.0 by closing specific visual failure modes — [[2605.06311|VISER]] (r=0.92) isolates specular highlights and contact shadows as load-bearing, while [[2604.24018|Sim2Real Betting]] attacks the orthogonal problem of *how few* real rollouts you need for a confident comparison. The residual ~8% gap is where deployment surprises live (see §17 Open Problems). Cross-reference [[14_Sim-to-Real-Transfer#5. Evaluation & Reality-Gap Measurement]] for the full reality-gap measurement deep-dive.

---

### 13. Real-World Evaluation Infrastructure

Sim benchmarks predict sim performance. The 2025-2026 wave introduced *standardized* real-world evaluation — distributed fleets, real-robot leaderboards, and on-real-hardware diagnostic suites.

- **[[2506.18123|RoboArena]]** — A ==decentralized crowd-sourced double-blind pairwise A/B comparison== leaderboard + ==task-aware Bradley-Terry model==; **600+** episodes across **7** academic institutions on DROID; **0.98** Pearson with oracle ranking, **1.8%** Max Rank Violation, converges in **~100** pairwise comparisons; LLM/VLM qualitative pipeline reaches **95%** human-expert agreement.
- **[[2510.17950|RoboChallenge]]** — A ==remote-robot online paradigm== with async APIs + ==visual task reproduction== (overlay reference image on live camera) to standardize initial states; **Table30** benchmark (30 tasks, **up to 1000** demos/task) with ==progress score==; temporal-reasoning **3%** SR / **14%** progress, soft-body **8%/27%**, precise-3D **18%/38%** expose VLA failure axes.
- **[[2509.17057|RoboManipBaselines]]** — An ==OpenAI-Gym-compatible== unified IL framework spanning MuJoCo / Isaac Gym / PyBullet + real UR5e / xArm 7; Diffusion Policy hits **52.0%** sim avg, **47.9%** real avg across **8** tasks; data-augmentation case study lifts SR **36% → 82%**.
- **[[2511.16518|MiMo-Embodied]]** — A cross-embodied VLM unifying autonomous-driving + embodied-AI via ==4-stage training== (SFT → embodied SFT → CoT → RLHF); SOTA across **17** embodied + **12** driving benchmarks (**29** total), demonstrating positive cross-domain transfer.
- **[[2603.13966|vla-eval]]** — A unified VLA eval harness across [[2306.03310|LIBERO]]/[[2112.03227|CALVIN]]/[[2405.05941|SimplerEnv]] whose client-server architecture decouples inference from execution; **47x speedup on [[2306.03310|LIBERO]]** (14h → 18min / 2,000 episodes); reproduced 6 VLAs / 3 benchmarks, exposed pitfalls (wrong proprioception **55pp**, quaternion errors **14–39pp**).

**Real-World Evaluation — Decision Matrix**

| Need | Benchmark |
|---|---|
| Distributed real-robot leaderboard (crowd-sourced) | [[2506.18123\|RoboArena]] (**0.98** Pearson with oracle ranking) |
| Remote-robot online eval with standardized resets | [[2510.17950\|RoboChallenge]] (**Table30**, up to 1000 demos/task) |
| Sim + real unified IL harness | [[2509.17057\|RoboManipBaselines]] (MuJoCo/Isaac/PyBullet + real UR5e) |
| Eval-side audit / pitfall detection | [[2603.13966\|vla-eval]] (**47×** [[2306.03310\|LIBERO]] speedup; **14–55pp** pitfall drops) |
| Cross-domain (driving + embodied) VLM eval | [[2511.16518\|MiMo-Embodied]] (**29** benchmarks total) |

> [!star] Key Papers
> - [[2510.17950|RoboChallenge]] — Large-scale real-robot leaderboard; the closest thing to a "robotics ImageNet competition"
> - [[2506.18123|RoboArena]] — Distributed fleet evaluation; resolves the long-standing lab-by-lab evaluation incompatibility
> - [[2509.17057|RoboManipBaselines]] — Sim-real-unified harness; the same code evaluates both, which kills sim-real mismatch reporting bugs
> - [[2603.13966|vla-eval]] — Unified VLA eval harness; **47x [[2306.03310|LIBERO]] speedup**; exposes undocumented evaluation pitfalls that drop reported scores by **14–55 pp** — first eval-side audit framework for VLAs

> [!tip] Real-World Evaluation is a Coordination Problem
> Real robots break, fall over, and need humans to reset them. The bottleneck for real-world benchmarking has always been the *scheduling* and *coordination* of multi-lab evaluation, not the algorithms. [[2506.18123|RoboArena]] and [[2510.17950|RoboChallenge]] address this by treating evaluation as distributed infrastructure rather than per-paper effort.

---

### 14. Benchmark Surveys

The field has matured enough that several recent surveys structure the entire benchmark / dataset / sim landscape — useful when you're starting on a new sub-area.

- **[[2606.04233|Manipulation Benchmark Audit]]** — A ==validity audit== probing shortcut solvability, significance, creeping overfitting, and data-source dependence; a DINO+MLP probe hits **99–100%** on LIBERO without pretraining/language, only **19.8%** of LIBERO SOTA claims are significant, CALVIN ATC drops **1.03**, and a **22M** policy on 120 SimplerEnv demos reaches **94.8%**.
- **[[2103.04918|Embodied AI Survey]]** — A foundational embodied-AI survey evaluating **9** simulators across **7 technical features** + categorizing **3** core tasks (visual exploration, visual navigation, embodied QA); identifies Habitat-Sim / iGibson as graphics leaders and AI2-THOR as interaction leader.
- **[[2507.00917|Embodied Intelligence Survey]]** — A modern follow-up survey integrating the world-model wave; proposes a ==5-level IR-L0→IR-L4 grading== for intelligent robots + identifies ==3 core WM functional roles== (neural simulators / dynamic models / reward models).
- **[[2510.16732|World Models for Embodied AI Survey]]** — A canonical WM survey with ==3-axis taxonomy== (Functionality × Temporal Modeling × Spatial Representation) under a POMDP-ELBO formalism; tracks evolution from RSSM latent vectors → Transformer token sequences → 3DGS-based explicit rendering.
- **[[2503.21765|Physics Cognition Survey]]** — A canonical video-generation physics survey with a ==Piaget-inspired 3-tier taxonomy== (Basic Schema Perception / Passive / Active Cognition) + ==4-domain physical-phenomena map== (mechanics / optics / thermal / material); reviews PhyBench + VideoPhy failure modes.
- **[[2501.10928|Generative Physical AI Survey]]** — A survey mapping physics-aware visual generation, splitting ==Physics-Aware Generation== into explicit (PAG-E) vs implicit (PAG-I) and cataloguing **6** paradigms for coupling generative models to simulators; documents the shift to LLM-based physical-parameter inference and argues visual-fidelity metrics are insufficient.
- **[[2604.15395|Foundation Models in Robotics Survey]]** — A systematic review of **435** articles under a ==six-criteria taxonomy== (FM type / architecture / paradigm / stage / task / domain) tracing a ==five-phase evolution== (RT-1 → PaLM-E → GR00T N1); flags the dataset gap in tactile + failure/recovery data — the broadest FM-in-robotics map.
- **[[2509.20021|Embodied AI LLM-WM Survey]]** — A position survey proposing a joint ==MLLM + World-Model architecture==: MLLMs supply semantic decomposition, WMs supply physics-aware prediction + real-time adaptation; the conceptual roadmap for the LLM-to-WM transition in embodied AI.
- **[[2506.21872|Continual RL Survey]]** — A taxonomy of ==Continual RL== by what is stored/transferred (==policy / experience / dynamics / reward==), naming the stability-plasticity-scalability dilemma + standardizing CRL scenarios and metrics; the reference for catastrophic-forgetting-free embodied learning.
- **[[2506.20966|VLA Post-Training Survey]]** — A review of **129** VLA post-training studies via a ==human-motor-learning taxonomy== (Newell's constraints: perception / embodiment / task comprehension / integration); documents LIBERO **75% → 98%** over **16 months** and CALVIN **3.5 → 4.3** sequence length — maps the adaptation design space.
- **[[2505.05108|Multi-agent Embodied AI Survey]]** — The first systematic review of ==multi-agent embodied AI== across classic control / learning-based / generative-integration; articulates exponential complexity, partial observability, non-stationarity, credit assignment, and the nascent-benchmark gap for coordinated embodied agents.
- **[[2505.04769|VLA Concepts Survey]]** — A survey categorizing **80+** VLA models from foundational integration (2022–23) to specialization (2024–25) across **6** domains; quantifies the deployment bottlenecks — autoregressive decoding caps speed at **3–5 Hz**, **~82%** collision accuracy, up to **40%** unseen-task degradation.
- **[[2405.14093|VLA for Embodied AI Survey]]** — An early structuring survey with a ==hierarchical control taxonomy== (low-level policies vs high-level planners) + PVRs / dynamics / world-model components; aggregates datasets + simulators + benchmarks into a resource hub for language-conditioned robotics.
- **[[2401.03568|Agent AI Survey]]** — A survey defining ==Agent AI== as multimodal-perception + embodied-action systems via a ==Unified Agent Multimodal Transformer== with agent tokens; introduces ==CuisineWorld== (multi-agent gaming) + ==VideoAnalytica== benchmarks; the foundational generalist-agent framing.

**Benchmark Surveys — Decision Matrix**

| Need a structural map of... | Survey |
|---|---|
| World-model evaluation taxonomy | [[2510.16732\|World Models for Embodied AI Survey]] (3-axis: Functionality × Temporal × Spatial) |
| Simulator + world-model integration | [[2507.00917\|Embodied Intelligence Survey]] (IR-L0→IR-L4 grading) |
| Physics-aware video generation evaluation | [[2503.21765\|Physics Cognition Survey]] (Piaget 3-tier taxonomy) |
| Classic simulator / task landscape | [[2103.04918\|Embodied AI Survey]] (9 simulators × 7 features) |

> [!star] Key Papers
> - [[2510.16732|World Models for Embodied AI Survey]] — Single best entry-point for world-model evaluation taxonomy
> - [[2507.00917|Embodied Intelligence Survey]] — Modern integration of simulator + world-model literatures
> - [[2503.21765|Physics Cognition Survey]] — Frames physics-aware video generation as an evaluation problem, not just a generation problem

> [!tip] Use Surveys as Map, Not Encyclopedia
> The four surveys above structure the landscape but they're inevitably stale on the latest 6 months of work. Use them to learn the *axis* — what categories exist, what evaluation criteria are accepted — then use the per-section benchmarks above for the current frontier.

---

### 15. Benchmark Hierarchy

Use this progression to evaluate robot policies at increasing levels of rigor.

**Benchmark Hierarchy — Decision Matrix**

| Level | Benchmark | What It Tests | When to Use |
|-------|-----------|--------------|-------------|
| 1. Basic | [[2306.03310\|LIBERO]], [[2112.03227\|CALVIN]] | In-distribution task success | Early development |
| 2. Scale | [[2405.05941\|SimplerEnv]] | Sim-to-real correlation | Before real-world deployment |
| 3. Robustness | [[2510.13626\|LIBERO-Plus]], [[2510.03827\|LIBERO-PRO]], [[2601.11421\|GM-100]] | Perturbation robustness | Before claiming generalization |
| 4. Spatial | [[2505.05456\|SITE]], [[2410.06468\|SPACE]], [[2511.04670\|Cambrian-S]], [[2602.20901\|SpatiaLQA]] | 3D + temporal spatial reasoning | For spatial tasks |
| 5. World Model | [[2603.22212\|Omni-WorldBench]], [[2603.23497\|WildWorld]], [[2506.00613\|WorldGym]] | Dynamics prediction + policy-fidelity | For WAM-based policies |
| 6. Real-Robot | [[2506.18123\|RoboArena]], [[2510.17950\|RoboChallenge]] | Distributed real-world success | Before publication / deployment |

> [!success] The Evaluation Stack — Production-Ready 7-Item Set for WAMs
> Linked plan: [[00_Benchmark-Pipeline-WAM]] (`_Projects_/02_BenchmarkPipeline-WAM/`). Every item scores **action quality** — that's what a WAM ultimately delivers. Pick #2 is the special case: it scores actions selected via WM imagination, the WAM's coupling claim.
>
> 1. **Diagnostic gate** → ==[[2510.03827|LIBERO-PRO]]== (memorizing or generalizing?)
> 2. **Joint WM+action** → ==[[2506.00613|WorldGym]]== (Stanford, Pearson r=0.78 vs real Bridge) + ==[[2602.08971|WorldArena]]== (Tsinghua, live leaderboard on RoboTwin 2.0) + ==[[2601.04137|WoW-World-Eval]]== (PKU, IDM Turing Test for video→action executability)
> 3. **Bimanual** → ==[[2506.18088|RoboTwin 2.0]]== (two-arm coordination + data generator + live leaderboard)
> 4. **Humanoid** → ==[[2403.10506|HumanoidBench]]== (Unitree H1 + Shadow Hand, 27 tasks)
> 5. **Long-horizon** → ==[[2506.06677|RoboCerebra]]== (~6× longer than CALVIN/LIBERO)
> 6. **Sim-to-real** → ==[[2405.05941|SimplerEnv]]== (canonical sim-real correlation) + ==[[2605.06311|VISER]]== (PBR stretch goal)
> 7. **Independent bar + safety** → ==[[2506.18123|RoboArena]]== (decentralized real-robot leaderboard) + ==[[2510.17950|RoboChallenge]]== + a **collision_violation_rate** sub-metric
>
> **Tier-2 contenders** (ingested, not yet on the critical path): [[2512.22539|VLA-Arena]], [[2601.21282|WorldBench]], [[2604.19092|RoboWM-Bench]], [[2512.19562|REALM]], [[2510.17801|RoboBench]], [[2603.22212|Omni-WorldBench]] (video-faithfulness diagnostic — does not score action).
>
> **Broader waypoints** (still valid for non-WAM or wider scope): [[2306.03310|LIBERO]], [[2112.03227|CALVIN]], [[2510.13626|LIBERO-Plus]], [[2601.11421|GM-100]].

> [!star] Key Papers
> - [[2510.03827|LIBERO-PRO]] — The robustness gate (Level 3): its **>90% → ~0%** collapse under minor perturbation is the single most decisive promotion test in the hierarchy
> - [[2405.05941|SimplerEnv]] — The scale gate (Level 2): cheapest reproducible way to estimate real-world transfer before touching hardware
> - [[2506.00613|WorldGym]] — The world-model gate (Level 5): scores a WAM by the transfer of policies trained *inside* it, not by video quality
> - [[2506.18123|RoboArena]] — The real-robot gate (Level 6): distributed leaderboard that turns deployment-scale evaluation into shared infrastructure

> [!tip] Climb the Ladder, Don't Skip Rungs
> The hierarchy is a *promotion gate*, not a menu: a policy must clear each level before its score at the next level is trustworthy. The common failure is reporting a Level-1 [[2306.03310|LIBERO]] number (~97%, saturated) as if it implied Level-3 robustness — [[2510.03827|LIBERO-PRO]] exists precisely to break that inference. For WAM work, the load-bearing rung is Level 5: a beautiful video that fails policy-transfer ([[2506.00613|WorldGym]]) is a Level-5 failure no amount of Level-1 success redeems. Cross-reference [[07_WAM#9. Open Problems & Failure Modes]] for the WAM-evaluation gaps this ladder still cannot close.

---

### 16. Picking Your Stack

> [!success] A Recommended Starting Stack
> The three axes — **data**, **environment**, and **benchmark** — are not independent. Common, well-validated triples for new projects:
>
> **Cross-embodiment generalist (research)**
> - Data: [[2310.08864|OXE]] + [[2403.12945|DROID]] for pretrain; [[2503.06669|AgiBot World]] for post-train
> - Environment: [[2003.08515|SAPIEN]] + [[2406.02523|RoboCasa]] for sim
> - Benchmark: [[2306.03310|LIBERO]] + [[2510.13626|LIBERO-Plus]] + [[2405.05941|SimplerEnv]] + [[2510.17950|RoboChallenge]]
>
> **Bimanual specialist**
> - Data: [[2304.13705|ALOHA]] + [[2512.24653|RoboMIND 2.0]]
> - Environment: [[2506.18088|RoboTwin 2.0]]
> - Benchmark: [[2506.18088|RoboTwin 2.0]] evaluation suite + [[2603.05687|CGP]] for contact-rich
>
> **Humanoid whole-body**
> - Data: [[2605.03452|BifrostUMI]] + [[2602.16710|EgoScale]]
> - Environment: [[2511.04831|Isaac Lab]] / [Genesis](https://genesis-world.readthedocs.io/) for parallelism; [[2502.20396|Humanoid Sim2Real Dex]] sim
> - Benchmark: [[2506.12851|KungfuBot]] (dynamic) + [[2604.07993|HEX]] (cross-embodiment) + [[2512.01061|Sim-to-Real Door]] (transfer)
>
> **Force-aware / contact-rich**
> - Data: [[2506.14754|Sparsh-X]] tactile pretraining + [[2509.18830|DexSkin]] for arm-skin
> - Environment: [MuJoCo](https://mujoco.org) / [MJX](https://mujoco.readthedocs.io/en/stable/mjx.html) for contact accuracy; [[2511.04665|Real-to-Sim GS]] for soft-body
> - Benchmark: [[2410.24090|TacBench]] ([[2410.24090|Sparsh]]) + [[2510.13324|FARM]] + [[2603.05687|CGP]]
>
> **World-model-powered VLA**
> - Data: any cross-embodiment + [[2503.06669|AgiBot World]]
> - Environment: [[2510.10125|CTRL-WORLD]] / [[2510.19430|GigaBrain-0]] as integrated WM-sim
> - Benchmark: [[2603.22212|Omni-WorldBench]] + [[2506.00613|WorldGym]] + [[2603.22078|WAM vs VLA Robustness]]

**Picking Your Stack — Decision Matrix**

| If your project is... | Data | Environment | Benchmark |
|---|---|---|---|
| Cross-embodiment generalist | [[2310.08864\|OXE]] + [[2403.12945\|DROID]] → [[2503.06669\|AgiBot World]] | [[2003.08515\|SAPIEN]] + [[2406.02523\|RoboCasa]] | [[2306.03310\|LIBERO]] + [[2510.13626\|LIBERO-Plus]] + [[2405.05941\|SimplerEnv]] |
| Bimanual specialist | [[2304.13705\|ALOHA]] + [[2512.24653\|RoboMIND 2.0]] | [[2506.18088\|RoboTwin 2.0]] | [[2506.18088\|RoboTwin 2.0]] suite + [[2603.05687\|CGP]] |
| Humanoid whole-body | [[2605.03452\|BifrostUMI]] + [[2602.16710\|EgoScale]] | [[2511.04831\|Isaac Lab]] / [Genesis](https://genesis-world.readthedocs.io/) | [[2506.12851\|KungfuBot]] + [[2604.07993\|HEX]] + [[2512.01061\|Sim-to-Real Door]] |
| Force-aware / contact-rich | [[2506.14754\|Sparsh-X]] + [[2509.18830\|DexSkin]] | [MuJoCo](https://mujoco.org) + [[2511.04665\|Real-to-Sim GS]] | [[2410.24090\|TacBench]] + [[2510.13324\|FARM]] + [[2603.05687\|CGP]] |
| World-model-powered VLA | cross-embodiment + [[2503.06669\|AgiBot World]] | [[2510.10125\|CTRL-WORLD]] / [[2510.19430\|GigaBrain-0]] | [[2603.22212\|Omni-WorldBench]] + [[2506.00613\|WorldGym]] |

> [!star] Key Papers
> - [[2310.08864|OXE]] — The default pretraining substrate for any cross-embodiment generalist stack
> - [[2506.18088|RoboTwin 2.0]] — The one paper that ships data-gen + sim + benchmark together, anchoring the bimanual stack
> - [[2511.04831|Isaac Lab]] — The GPU-parallel substrate that makes the humanoid whole-body stack trainable at scale
> - [[2410.24090|Sparsh]] — The tactile-representation foundation underwriting any force-aware stack

> [!tip] The Three Axes Are Coupled, Not Independent
> The recurring mistake is treating data, environment, and benchmark as separable purchases — picking a great dataset, then a great sim, then a great benchmark in isolation. The validated stacks above are *triples* because the axes constrain each other: a bimanual dataset needs a bimanual sim and a bimanual benchmark, and [[2506.18088|RoboTwin 2.0]] ships all three precisely so they cannot drift apart. Start from your project archetype, take the whole triple, and only swap a component when you can name what it breaks downstream. Cross-reference [[14_Sim-to-Real-Transfer#6. Integration Patterns]] for how these stacks compose with the sim-to-real loop.

---

### 17. Open Problems & Failure Modes

The evaluation stack is mature enough to expose first-order failures, but six structural gaps remain — each is a frontier in its own right.

> [!warning] Where the Evaluation Stack Still Breaks
> - **Sim-real correlation ceiling** — [[2605.06311|VISER]] reaches r=0.92, but no benchmark closes the residual gap to r=1.0. The remaining ~8% is load-bearing: it's where deployment surprises live.
> - **Cross-lab evaluation drift** — [[2506.18123|RoboArena]] and [[2510.17950|RoboChallenge]] are the first distributed real-robot leaderboards, but the data they produce is itself a moving target (different robots, different episodes, different reset protocols across labs) — not a fixed benchmark.
> - **Soft-body / deformable evaluation** — Gaussian-splat twins ([[2511.04665|Real-to-Sim GS]], [[2510.21447|PhysWorld-Deformable]]) are <12 months old; no consensus exists yet on what a "fair" deformable benchmark looks like (which materials, what failure modes count).
> - **Tactile data scaling** — [[2410.24090|Sparsh]] reached 460k images, [[2506.14754|Sparsh-X]] extended to multisensory; but tactile is still <1% the data scale of vision. Foundation-model effects observed in vision haven't been definitively demonstrated for touch.
> - **Long-horizon language-conditioned eval** — [[2604.21924|LoHo-Manip]] and [[2605.01772|Anticipation-VLA]] surface skill-chaining and subgoal failures, but no standard exists for the >10-minute task horizons real deployment increasingly requires.
> - **Failure-aware evaluation** — every benchmark above scores task *success*; none score *failure detection* or *recovery*, despite [[2510.09459|FIPER]] showing these are independently trainable capabilities. The eval stack measures what the policy gets right, not what it knows it's getting wrong.

**Open Problems — Decision Matrix**

| Problem | Remediation Path |
|---|---|
| Sim-real correlation ceiling (r=0.92, not 1.0) | Push asset diversity + visual-cue isolation ([[2605.06311\|VISER]]); close residual via real-to-sim twins ([[2511.04665\|Real-to-Sim GS]]) |
| Cross-lab evaluation drift | Standardize reset protocols on distributed leaderboards ([[2506.18123\|RoboArena]], [[2510.17950\|RoboChallenge]]) |
| No consensus deformable benchmark | Converge material + failure-mode definitions atop Gaussian-splat twins ([[2511.04665\|Real-to-Sim GS]], [[2510.21447\|PhysWorld-Deformable]]) |
| Tactile data <1% of vision scale | Scale multisensory tactile corpora ([[2506.14754\|Sparsh-X]]) toward foundation-model regime |
| No >10-min long-horizon eval standard | Extend subgoal/skill-chaining diagnostics ([[2604.21924\|LoHo-Manip]], [[2605.01772\|Anticipation-VLA]]) to deployment horizons |
| No failure-detection / recovery scoring | Add failure-aware sub-metrics; treat detection as a trainable axis ([[2510.09459\|FIPER]]) |

> [!star] Key Papers — Benchmark-Stack Failure Frontier
> - [[2605.06311|VISER]] — Defines the sim-real correlation ceiling (r=0.92) and the load-bearing residual gap where deployment surprises live
> - [[2506.18123|RoboArena]] — The distributed-leaderboard frontier; exposes that cross-lab eval data is itself a moving target, not a fixed benchmark
> - [[2510.21447|PhysWorld-Deformable]] — Frontier of deformable evaluation; <12 months old, no consensus benchmark yet exists
> - [[2510.09459|FIPER]] — Shows failure detection / recovery are independently trainable — the capability the entire success-scoring eval stack omits

> [!tip] Reading Compass
> Open problems on the sim-real axis → [[14_Sim-to-Real-Transfer#7. Open Problems]]; world-model evaluation gaps → [[07_WAM#9. Open Problems & Failure Modes]]; failure-aware evaluation → [[13_Self-Evolving-VLA-WAM#4. Failure Detection, Diagnosis & Recovery]] + [[09_Contact-Rich-and-Whole-Body-Control#8. Open Problems & Failure Modes]]; tactile scaling → [[09_Contact-Rich-and-Whole-Body-Control#2. Tactile Sensors as a Sensing Modality]].

---

## Quick-Reference Matrix

| If you need to... | Objective | Use |
|---|---|---|
| Pretrain a cross-embodiment VLA | Cross-morphology generalization | [[2310.08864\|OXE]], [[2403.12945\|DROID]], [[2503.06669\|AgiBot World]] |
| Pretrain on dexterous human data | Finger-level supervision | [[2602.16710\|EgoScale]], [[2605.09613\|SABER]], [[2402.10329\|UMI]] |
| Collect data without teleop | Scale collection beyond teleop | [[2402.10329\|UMI]], [[2505.21864\|DexUMI]], [[2605.03452\|BifrostUMI]] |
| Benchmark VLAs in-distribution | Baseline task success | [[2306.03310\|LIBERO]], [[2112.03227\|CALVIN]], [[1909.12271\|RLBench]] |
| Stress-test VLA robustness | Expose perturbation failures | [[2510.13626\|LIBERO-Plus]], [[2510.03827\|LIBERO-PRO]], [[2603.28301\|LIBERO-Para]], [[2602.06556\|LIBERO-X]] |
| Test fine manipulation | Surface precision gaps | [[2601.11421\|GM-100]] |
| Test embodied reasoning | Probe spatial + causal cognition | [[2507.10548\|EmbRACE-3K]], [[2508.13142\|EASI]] |
| Eval on a real fleet of robots | Validate at deployment scale | [[2506.18123\|RoboArena]], [[2510.17950\|RoboChallenge]] |
| Run sim with photorealistic kitchens | Bridge visual reality gap | [[2406.02523\|RoboCasa]], [[2602.10116\|SAGE]] |
| Run sim with soft bodies / deformables | Cover deformable physics | [[2511.04665\|Real-to-Sim GS]], [[2510.21447\|PhysWorld-Deformable]] |
| Run sim with massive GPU parallelism | Scale RL data throughput | [Genesis](https://genesis-world.readthedocs.io/), [Newton (NVIDIA)](https://developer.nvidia.com/newton-physics), [[2003.08515\|SAPIEN]] |
| Eval a world model | Measure dynamics + action fidelity | [[2603.22212\|Omni-WorldBench]], [[2603.23497\|WildWorld]], [[2506.00613\|WorldGym]] |
| Predict real performance from sim | Quantify sim-real correlation | [[2405.05941\|SimplerEnv]], [[2605.06311\|VISER]], [[2604.24018\|Sim2Real Betting]] |
| Test spatial reasoning | Probe 3D + spatial cognition | [[2410.06468\|SPACE]], [[2505.05456\|SITE]], [[2603.18892\|MultihopSpatial]] |
| Test long-horizon planning | Skill-chaining + subgoal recovery | [[2305.12821\|FurnitureBench]], [[2604.21924\|LoHo-Manip]], [[2605.01772\|Anticipation-VLA]] |
| Compare humanoid whole-body control | Bilateral + whole-body coordination | [[2506.12851\|KungfuBot]], [[2604.07993\|HEX]], [[2502.20396\|Humanoid Sim2Real Dex]] |
| Read a survey of the whole space | Build a structural mental map | [[2510.16732\|World Models for Embodied AI Survey]], [[2507.00917\|Embodied Intelligence Survey]], [[2103.04918\|Embodied AI Survey 2021]] |

---

---

## Cross-References

- [[05_VLA]] — VLA deep-dive (Section 2 uses [[2412.14058|RoboVLMs]] findings)
- [[07_WAM]] — WAM deep-dive (Section 8 covers failure modes found by benchmarks)
- [[08_Latent-World-Models]] — Latent world models (JEPA benchmarks, latent vs pixel comparison)
- [[13_Self-Evolving-VLA-WAM]] — Self-evolving systems (evaluation of self-improvement methods)
- [[11_Physics-Aware-Embodied-AI]] — Physics commonsense benchmarks ([[2410.05363|PhyGenBench]], [[2503.06800|VideoPhy-2]], [[2501.09038|Physics-IQ]], [[2504.02918|Morpheus]]); soft-body physics-aware data generation overlaps with §7 here
- [[06_VLA-Reasoning-and-CoT]] — VLA reasoning architectures deep-dive; complements §9 Spatial Reasoning benchmarks
- [[12_Egocentric-Pretraining-and-Human-Video]] — Egocentric datasets ([[2110.07058|Ego4D]], [[2505.11709|EgoDex]], [[1706.04261|Something-Something]], [[2602.16710|EgoScale]])
- [[09_Contact-Rich-and-Whole-Body-Control]] — Tactile policies ([[2410.24090|Sparsh]], [[2506.14754|Sparsh-X]], [[2510.13324|FARM]], [[2603.05687|CGP]], [[2509.07962|TA-VLA]]); §6 here is the evaluation side, 10 is the policy side
- [[14_Sim-to-Real-Transfer]] — Full sim-to-real deep-dive: learned simulators, robust RL, digital twins, evaluation
- [[01_Embodied-AI-101]] — VLA vs WAM basics

---

*See [[05_VLA]] for VLA design principles informed by these benchmarks, [[07_WAM]] for world model evaluation, or [[09_Contact-Rich-and-Whole-Body-Control]] for the policy side of tactile.*
