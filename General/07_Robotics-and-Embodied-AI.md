---
title: "Robotics & Embodied AI — Topic Overview"
tags:
  - robotics
  - VLA
  - WAM
  - embodied-AI
  - world-model
  - self-evolving
  - manipulation
aliases:
  - "Robotics Overview"
---

# Robotics & Embodied AI

> [!abstract] Overview
> Embodied AI sits at the convergence of all other topics: foundation models provide the backbone, VLMs provide perception, RL provides learning, and world models provide physics understanding. This note maps the landscape from VLAs through WAMs to self-evolving systems — the full path toward autonomous robots.

## Evolution Graph

```mermaid
graph TD
    subgraph "Foundations"
        A0["RT-1<br/><i>2022</i>"]
        B["Diffusion Policy<br/><i>2023</i>"]
    end

    subgraph "VLAs"
        D["RT-2<br/><i>2023</i>"]
        E["OXE / RT-X<br/><i>2023</i>"]
        F["OpenVLA<br/><i>2024</i>"]
        G["π0<br/><i>2024</i>"]
        D1["GR-1<br/><i>2023</i>"]
        D2["GR-2<br/><i>2024</i>"]
    end

    subgraph "WAMs"
        H["DreamZero<br/><i>2026</i>"]
        H1["VLAW<br/><i>2026</i>"]
        H2["VLA-JEPA<br/><i>2026</i>"]
    end

    subgraph "Self-Evolving"
        K["EvoAgent<br/><i>2025</i>"]
        L["SPIRAL<br/><i>2026</i>"]
    end

    A0 --> D --> E --> F --> G
    B --> G
    D1 --> D2 --> H1
    G --> H
    G --> H1
    G --> H2
    G --> K
    H --> L
    K --> L

    style A0 fill:#e8f4fd,stroke:#4a90d9
    style G fill:#e8f4fd,stroke:#4a90d9
    style H fill:#f0e8fd,stroke:#9b59b6
    style K fill:#e8fde8,stroke:#27ae60
```

The field evolved through four phases: **foundations** (2022-2023) where RT-1 and Diffusion Policy proved Transformers and diffusion work for robot control; **VLAs** (2023-2024) where RT-2, OXE, OpenVLA, and pi0 scaled vision-language-action models from proof-of-concept to generalist policies; **WAMs** (2026) where DreamZero, VLAW, and VLA-JEPA added world modeling for physics-aware control; and **self-evolving** (2025-2026) where EvoAgent and SPIRAL enabled autonomous improvement loops.

| Year | Paper | Contribution |
|------|-------|-------------|
| 2022 | [[2212.06817\|RT-1]] | Transformer policy on 130K real demos; proved Transformers work for robot control at scale |
| 2023 | [[2303.04137\|Diffusion Policy]] | Pioneered action diffusion for robotics; proved denoising beats regression for multimodal action distributions |
| 2023 | [[2307.15818\|RT-2]] | Scaled to PaLI-X/PaLM-E backbones; first to show internet-scale VLM knowledge transfers to robot control |
| 2023 | [[2310.08864\|OXE]] | Open X-Embodiment: 1M+ trajectories from 22 embodiments; the ImageNet moment for robotics data |
| 2023 | [[2312.13139\|GR-1]] | GPT-style generative robot model unifying language, video prediction, and action in a single Transformer |
| 2024 | [[2406.09246\|OpenVLA]] | Open-source 7B VLA; democratized VLA research with competitive performance |
| 2024 | [[2410.24164\|pi0]] | Flow matching action expert + VLM for dexterous manipulation; current SOTA generalist robot control |
| 2024 | [[2410.06158\|GR-2]] | Scaled GR-1 to larger video generation backbone; improved long-horizon multi-task humanoid control |
| 2025 | [[2502.05907\|EvoAgent]] | Self-evolving agent with continual world model; +105% improvement via self-planning and self-reflection |
| 2026 | [[2602.15922\|DreamZero]] | 14B parameter WAM from NVIDIA; zero-shot robot policies via joint video+action prediction |
| 2026 | [[2604.15483\|π0.7]] | 5B steerable generalist VLA with subgoal-image + episode-metadata prompting; cross-embodiment transfer matching human experts |
| 2026 | [[2602.12063\|VLAW]] | Iterative co-improvement loop between VLA policy and world model; each bootstraps the other |
| 2026 | [[2602.10098\|VLA-JEPA]] | JEPA-style latent prediction for leakage-free future state modeling in robot control |
| 2026 | [[2603.08403\|SPIRAL]] | Closed-loop self-improving framework for controllable, long-horizon video generation and WAMs |

---

## 1. Robotic Policy Foundations & Manipulation

How robots learn to act from demonstrations. The field evolved from perception-based agents (PerAct) through diffusion-based action generation to spatial and language-conditioned policies. Manipulation is the proving ground — if a method works for dexterous object interaction, it can generalize to broader embodied tasks.

**Diffusion-Based Policies** — Treat robot actions as a noise-removal process, generating smooth multi-step trajectories that handle multimodal action distributions (e.g., reaching from the left vs. right) better than regression.
- [[2606.06049|L-SDPPO]], [[2606.03682|GN0]], [[2606.03551|Isaac Sim Survey]], [[2606.02432|NDPP-Grasp]], [[2605.26115|TriSplat]], [[2605.26006|MIND]], [[2605.25546|ISSf-CBF WBC]], [[2605.25537|Soft RTC]], [[2605.23733|Any2Any]], [[2605.14598|DSSP]], [[2605.10051|SSIP]], [[2605.09537|CAPS (Power Sampling)]], [[2605.08799|ElasticFlow]], [[2605.05756|MaMi-HOI]], [[2604.18933|Gated Memory Policy]], [[2604.15938|VADF]], [[2604.07084|FMP]], [[2604.06067|HiPolicy]], [[2604.04310|frax]], [[2604.03181|MV-VDP]], [[2604.00202|DreamControl-v2]], [[2603.26320|DFM-VLA]], [[2603.25406|MMaDA-VLA]], [[2603.16368|SCDP]], [[2603.13707|REFINE-DP]], [[2603.05687|CGP]], [[2602.07322|A2A]], [[2512.22688|ARFM]], [[2512.21430|EVE]], [[2512.16881|PolaRiS]], [[2511.04812|MDF]], [[2510.23763|OmniAction]], [[2510.13324|FARM]], [[2509.22652|DAWN]], [[2509.19696|Diffusion Impedance Learning]], [[2507.21053|FPO]], [[2503.15386|CCDP]], [[2503.14833|Curiosity-Diffuser]], [[2503.02881|RDP]], [[2502.10040|DTP]], [[2502.02316|DIME]], [[2407.05996|MDT]], [[2406.09905|Nymeria]], [[2403.03954|DP3]], [[2311.11893|CBP]], [[2305.06341|GGCS]], [[2303.04137|Diffusion Policy]], [[2302.01877|AdaptDiffuser]], [[2210.03094|VIMA]], [[2205.09991|Diffuser]], [[1804.02748|EPIC-KITCHENS]]

> [!star] Key Papers
> - [[2303.04137|Diffusion Policy]] — Pioneered action diffusion for robotics; proved denoising beats regression for multimodal distributions
> - [[2403.03954|DP3]] — Extended to 3D point clouds, enabling sim-to-real transfer without camera calibration

**Foundational Manipulation Architectures** — Transformer and perception-based agents that established how robots can learn multi-task manipulation from language instructions and visual observations.
- [[2606.06218|TAM (Torque Adaptation)]], [[2606.06041|iCEM+TL]], [[2606.05160|GRAIL]], [[2606.04233|Manipulation Benchmark Audit]], [[2606.03385|GTP-FA]], [[2606.03335|DGPO]], [[2606.03297|SplitAdapter]], [[2606.02551|AFUN]], [[2605.29564|VE2VF]], [[2605.28812|CoP Tactile]], [[2605.26638|HyperSim]], [[2605.21429|roto 2.0]], [[2605.21258|Structural Latent Points]], [[2605.19919|ZPRL]], [[2605.16257|DexJoCo]], [[2605.06593|ReActor]], [[2605.05925|DexSynRefine]], [[2605.03363|Hierarchical RL-QP Grasp]], [[2604.27711|ExoActor]], [[2604.24681|MoT-HRA]], [[2604.15215|HiST-AT]], [[2604.08418|DMBN-PTE]], [[2604.02408|F2F-AP]], [[2603.24576|Chameleon (Episodic Memory)]], [[2603.22264|UniDex]], [[2603.22003|VP-VLA]], [[2603.10052|OmniGuide]], [[2603.09513|VQ-Memory]], [[2603.07648|AtomicVLA]], [[2603.03243|HoMMI]], [[2603.01229|RMBench]], [[2602.15010|BPP]], [[2602.09013|VIDEOMANIP]], [[2602.00937|CLAMP]], [[2511.09484|SPIDER]], [[2510.20328|MemER]], [[2510.08568|NovaFlow]], [[2509.26633|OmniRetarget]], [[2508.11143|AC3]], [[2506.18448|GraspMAS]], [[2506.14968|FEAST]], [[2506.14754|Sparsh-X]], [[2505.18472|ManiFeel]], [[2505.14986|AnyBody]], [[2505.06776|FALCON (Loco-Manipulation)]], [[2504.03597|Real-is-Sim]], [[2503.13441|PH2D]], [[2502.10894|UAN]], [[2501.18564|SAM2Act]], [[2501.16389|Sim2Real Encoder Eval]], [[2412.11974|EMMA-X]], [[2412.04445|Moto]], [[2411.04999|DynaMem]], [[2410.24090|Sparsh]], [[2410.07864|RDT-1B]], [[2409.00215|Intent-Aware Co-Manipulation]], [[2408.10899|ARIO]], [[2407.07788|BiGym]], [[2406.17768|EXTRACT]], [[2405.12213|Octo]], [[2403.19622|RH20T-P]], [[2402.15487|RoboEXP]], [[2306.11565|HomeRobot]], [[2306.10007|RPT]], [[2210.06407|Language-Table]], [[2209.05451|PerAct]], [[2104.08212|MT-Opt]], [[1910.11215|RoboNet]], [[1910.10897|Meta-World]]

> [!star] Key Papers
> - [[2209.05451|PerAct]] — First to use Perceiver Transformer on voxelized observations for 6-DoF multi-task manipulation
> - [[2405.12213|Octo]] — Open-source generalist policy with strong zero-shot transfer across robot morphologies
> - [[2410.24090|Sparsh]] — First SSL family of vision-based tactile representations + TacBench benchmark; **+95.1%** average over end-to-end baselines, **20-53%** greater bead-maze distance on a real robot
> - [[2506.14754|Sparsh-X]] — Extends Sparsh to four tactile modalities (image, audio, IMU, pressure) on **~1M** contact interactions; **90%** plug-insertion success, **90%** reduction in in-hand-rotation vertical drift

**Bimanual & Teleoperation** — Hardware platforms and methods for dual-arm manipulation and human-guided data collection, which are critical for scaling real-world demonstrations.
- [[2604.05831|BiCoord]], [[2601.02078|Genie Sim 3.0]], [[2512.04884|Hoi!]], [[2511.21264|MPPI-Bimanual]], [[2510.27607|DUST]], [[2510.08807|Humanoid Everyday]], [[2507.12898|Vidar]], [[2507.07969|Q-chunking]], [[2507.00990|RIGVid]], [[2507.00833|HumanoidGen]], [[2506.16012|DualTHOR]], [[2506.10966|GenManip]], [[2505.21864|DexUMI]], [[2505.12748|TeleOpBench]], [[2505.03233|SynGrasp-1B]], [[2504.18904|RoboVerse]], [[2504.13059|RoboTwin]], [[2503.05652|BEHAVIOR Robot Suite]], [[2502.05086|REASSEMBLE]], [[2412.07215|RoboData]], [[2410.24185|DexMimicGen]], [[2408.14368|GR-MG]], [[2408.06506|TacSL]], [[2403.19417|OAKINK2]], [[2403.07788|DexCap]], [[2402.10329|UMI]], [[2401.08399|TACO]], [[2310.17596|MimicGen]], [[2309.13037|GELLO]], [[2308.12952|BridgeData V2]], [[2304.13705|ALOHA]], [[2302.04659|ManiSkill2]], [[2206.08522|VLMbench]], [[2204.13662|ARCTIC]], [[2203.01577|HOI4D]], [[2104.11181|H2O]], [[1911.04052|RoboTurk]], [[1810.07121|MIME]], [[1806.10293|QT-Opt]]

> [!star] Key Papers
> - [[2304.13705|ALOHA]] — Low-cost open-source bimanual system; proved co-training on diverse data dramatically improves performance

**Spatial Reasoning for Manipulation** — Leverage 3D point clouds, depth maps, or learned spatial features to improve generalization across camera viewpoints and object arrangements.
- [[2605.21133|Spatial Brain Cerebellum]], [[2605.05163|PhysForge]], [[2604.21914|VistaBot]], [[2604.15281|R3D]], [[2604.14089|UMI-3D]], [[2604.08534|ActiveGlasses]], [[2604.06778|RichMap]], [[2604.02696|VBGS-SLAM]], [[2603.27967|XVR]], [[2603.13825|Explicit-WM Manipulation]], [[2603.00905|pySpatial]], [[2602.20901|SpatiaLQA]], [[2602.19063|Direction-aware 3D LMM]], [[2602.18374|ZS-IP]], [[2601.05172|CoV]], [[2512.13660|RoboTracer]], [[2511.19684|IndEgo]], [[2511.05491|VST]], [[2510.12276|Spatial Forcing]], [[2509.18644|State-Free Visuomotor Policy]], [[2503.11089|EmbodiedVSR]], [[2501.10074|SpatialCoT]], [[2406.01584|SpatialRGPT]], [[2402.08191|THE COLOSSEUM]], [[2401.12168|SpatialVLM]], [[2309.15278|Out of Sight Still in Mind]], [[2210.13066|DaXBench]], [[2104.11213|ManipulaTHOR]], [[2011.07215|SoftGym]]

> [!star] Key Papers
> - [[2501.10074|SpatialCoT]] — Chain-of-thought reasoning in 3D space; bridges VLM reasoning with spatial manipulation

**Language-Conditioned & Multi-Stage** — Plan and execute complex, multi-step tasks from natural language instructions by composing LLM planning with robot execution.
- [[2606.06139|MotionDisco]], [[2606.03047|ModuLoop]], [[2605.25832|AUTO-ROBOTIST]], [[2605.02600|CoRAL]], [[2604.26569|LLM-Flax]], [[2604.02812|Neuro-Symbolic Robot Policies]], [[2604.02021|Discrete-Continuous Planning Bridge]], [[2603.30022|Hybrid LLM-RL Manipulation]], [[2603.04560|MEMO]], [[2603.02511|Unveiler]], [[2602.21198|Reflective Test-Time Planning]], [[2507.17520|InstructVLA]], [[2501.04693|FuSe]], [[2412.18194|VLABench]], [[2410.01345|GemBench]], [[2409.01652|ReKep]], [[2405.19783|IVM]], [[2403.13358|QUARD-Auto]], [[2307.05973|VoxPoser]], [[2204.00598|Socratic Models]], [[2201.07207|LLM Zero-Shot Planners]]

> [!star] Key Papers
> - [[2307.05973|VoxPoser]] — LLMs generate 3D value maps that guide robot actions; no robot training data needed
> - [[2409.01652|ReKep]] — Automatic keypoint discovery from VLMs for constraint-based manipulation planning

**World Model Studies** — Empirical studies of predictive models in manipulation contexts.
- [[2606.05699|DexFuture]], [[2606.03834|SFMDS]], [[2606.02027|World-Task Factorization]], [[2605.25495|RepSAM]], [[2605.20752|GaussianDream]], [[2604.19683|MWM]], [[2604.19092|RoboWM-Bench]], [[2603.29090|HCLSM]], [[2603.28955|WAM]], [[2603.18336|ManiDreams]], [[2603.12553|Structured WM Planner]], [[2512.24497|JEPA-WM]], [[2512.23541|Act2Goal]], [[2512.13644|DexWM]], [[2512.03422|3D Scene Rep Survey]], [[2512.01119|World Model Surprise Robustness]], [[2511.14004|STAR (Memory-Action)]], [[2511.01718|UD-VLA]], [[2510.10125|CTRL-WORLD]], [[2507.10087|Foundation Robotics Review]], [[2506.06199|3DFlowAction]], [[2503.09867|OH-A-DINO]], [[2501.10100|RWM]], [[2411.04983|DINO-WM]]

> [!star] Key Papers
> - [[2411.04983|DINO-WM]] — World models built on pre-trained DINO features enable zero-shot planning; foundational for latent WM in manipulation
> - [[2512.24497|JEPA-WM]] — LeCun lab study identifying what drives success in JEPA-based physical planning; key design insights

> [!tip] The Diffusion Policy Shift
> Regression → diffusion → flow matching. If you're building a manipulation policy today, start with Diffusion Policy or DP3 and add 3D/spatial features for viewpoint invariance.

---

## 2. Vision-Language-Action Models (VLAs)

VLAs are the current mainstream approach to robot control: take a pre-trained vision-language model, fine-tune it to output robot actions directly. The field has exploded from RT-1/RT-2 (2022-2023) to 80+ models spanning efficient deployment, spatial awareness, reasoning, world-model augmentation, and self-evolution.

> [!success] Ideal VLA Recipe (from RoboVLMs)
> ==KosMos/[[2407.07726|PaliGemma]] backbone== + ==Policy Head fusion== + ==Continuous actions== + ==MoE== + ==Post-training on in-domain data==

**Foundation & Generalist** — The pioneering VLA architectures that established the paradigm: fine-tune a VLM to output robot actions as tokens or flow-matching trajectories.
- [[2606.04708|VISTA]], [[2605.30280|Qwen-VLA]], [[2605.29710|PhAIL]], [[2605.27284|FineVLA]], [[2605.24642|GFM-VLA Study]], [[2605.21061|Driving VLA IK]], [[2605.19986|MetaFine]], [[2605.19282|Pion]], [[2605.15298|PhysBrain]], [[2605.13403|RotVLA]], [[2605.10925|PriorVLA]], [[2605.03269|RLDX-1]], [[2605.00078|Being-H0.7]], [[2604.20100|JoyAI-RA]], [[2604.15483|π0.7]], [[2603.28545|ManipArena]], [[2602.18532|VLANeXt]], [[2602.16710|EgoScale]], [[2602.10556|LAP]], [[2601.21199|Thinker]], [[2601.14352|RoboBrain 2.5]], [[2601.04061|CLAP]], [[2512.22414|π0.5 + ego]], [[2511.18112|EchoVLA]], [[2511.11478|LIBERO-Mem]], [[2511.04357|GraSP-VLA]], [[2511.00108|Pelican-VL 1.0]], [[2510.21571|VITRA]], [[2510.13778|InternVLA-M1]], [[2510.11027|Vlaser]], [[2510.08022|FastUMI-100K]], [[2509.01106|Robix]], [[2508.21112|EO-1]], [[2508.20072|Discrete Diffusion VLA]], [[2507.23682|villa-X]], [[2507.15597|Being-H0]], [[2507.05331|LBM TRI]], [[2507.02029|RoboBrain 2.0]], [[2505.06111|UniVLA]], [[2505.03500|TLI]], [[2503.20020|Gemini Robotics]], [[2503.19757|Dita]], [[2503.15558|Cosmos-Reason1]], [[2503.10631|HybridVLA]], [[2502.13130|Magma]], [[2410.24164|π0]], [[2410.15959|DiT Policy]], [[2410.06158|GR-2]], [[2407.15208|Im2Flow2Act]], [[2406.09246|OpenVLA]], [[2405.12213|Octo]], [[2312.13139|GR-1]], [[2311.01378|RoboFlamingo]], [[2310.08864|OXE]], [[2307.15818|RT-2]], [[2212.06817|RT-1]], [[2210.05714|VLMaps]]

> [!star] Key Papers
> - [[2604.15483|π0.7]] — 5B-param steerable generalist VLA from Physical Intelligence with episode-metadata + subgoal-image prompting; cross-embodiment transfer matching human experts
> - [[2602.16710|EgoScale]] — NVIDIA's **20,854-hour** human-video VLA pretraining; established a log-linear scaling law for human data and enables cross-embodiment transfer
> - [[2507.15597|Being-H0]] — Physical Instruction Tuning on 150M human-hand motion pairs; first VLA to explicitly tokenize human dexterous actions for robot transfer
> - [[2212.06817|RT-1]] — Google's first VLA: 130K demonstrations, 700 tasks, Transformer-based; proved the paradigm works
> - [[2307.15818|RT-2]] — Scaled to PaLI-X/PaLM-E backbones; first to show internet-scale VLM knowledge transfers to robot control
> - [[2406.09246|OpenVLA]] — Open-source 7B VLA; democratized VLA research
> - [[2410.24164|π0]] — Flow matching for continuous actions; current SOTA for generalist robot control

**Efficient & Open-Source** — Smaller, faster, or quantized VLAs optimized for real-world deployment where inference speed and cost matter.
- [[2606.05737|One-Step VLA]], [[2605.29562|VLA-Pro]], [[2605.28634|PrimitiveVLA]], [[2605.25477|EXPO-FT]], [[2605.13778|Realtime-VLA FLASH]], [[2605.09948|LoopVLA]], [[2605.02739|Latent Bridge]], [[2604.20834|PokeVLA]], [[2604.11757|StarVLA-alpha]], [[2604.05672|A1]], [[2604.05656|SnapFlow]], [[2604.05323|VLA-InfoEntropy]], [[2604.04161|AAC]], [[2604.02965|SV-VLA]], [[2603.28740|FocusVLA]], [[2603.28565|StreamingVLA]], [[2602.18224|SimVLA]], [[2602.13710|HBVLA]], [[2601.22153|DynamicVLA]], [[2512.04952|FASTer]], [[2511.14148|AsyncVLA]], [[2511.05936|10 VLA Challenges]], [[2510.06710|RLinf-VLA]], [[2509.04996|FLOWER]], [[2506.19816|CronusVLA]], [[2506.01844|SmolVLA]], [[2505.23705|Knowledge Insulation VLA]], [[2504.19854|NORA]], [[2503.02310|PD-VLA]], [[2502.19645|OpenVLA-OFT]], [[2501.09747|FAST]], [[2409.12514|TinyVLA]]

> [!star] Key Papers
> - [[2501.09747|FAST]] — Compression-based action tokenization; makes VLAs 5x faster by compactly encoding continuous actions
> - [[2506.01844|SmolVLA]] — 450M params achieving competitive performance; proves VLAs don't need to be massive

**Spatial & 3D-Aware** — Inject depth, 3D coordinate embeddings, or volumetric features into VLAs for better spatial generalization.
- [[2606.03240|GeoAlign]], [[2606.02274|Dexterity-BEV]], [[2605.29416|3DVLA]], [[2605.29074|Embodied3DBench]], [[2605.22812|GesVLA]], [[2605.22283|SOMA]], [[2605.18746|ESI-Bench]], [[2605.14950|Evo-Depth]], [[2605.11832|AML-VLA]], [[2605.10485|VEGA]], [[2605.05126|ConsisVLA-4D]], [[2604.02759|OMNI-PoseX]], [[2603.25399|LaMP]], [[2603.24393|3D-MIX]], [[2511.01571|PixelVLA]], [[2510.00695|HAMLET]], [[2508.09071|GeoVLA]], [[2506.22242|4D-VLA]], [[2505.05800|3D-CAVLA]], [[2501.15830|SpatialVLA]], [[2403.09631|3D-VLA]]

> [!star] Key Papers
> - [[2501.15830|SpatialVLA]] — Novel spatial representations that let VLAs understand object arrangements without explicit 3D supervision

**Reasoning & Chain-of-Thought** — VLAs that think before they act: predict subgoals, search over plans, or use MCTS for test-time reasoning.
- [[2606.05979|WLA]], [[2606.03784|ERVLA]], [[2605.29438|ElegantVLA]], [[2605.22816|AwareVLN]], [[2605.22183|AVP]], [[2605.14712|IntentVLA]], [[2605.13632|GTA-VLA]], [[2605.13119|VLAs-as-Tools]], [[2605.12369|GuidedVLA]], [[2605.06234|RobotEQ]], [[2605.02881|MolmoAct2]], [[2605.01772|Anticipation-VLA]], [[2604.22615|GazeVLA]], [[2604.21924|LoHo-Manip]], [[2604.18486|OneVL]], [[2604.17880|ST-π]], [[2604.17800|ReFineVLA]], [[2604.14125|HiVLA]], [[2603.09292|See Plan Rewind]], [[2603.05147|Act, Think or Abstain]], [[2602.07845|RD-VLA]], [[2602.03973|VLS]], [[2602.01166|LaRA-VLA]], [[2601.11404|ACoT-VLA]], [[2601.09708|Fast-ThinkAct]], [[2601.07060|PALM]], [[2601.01618|Action-Sketcher]], [[2601.00969|V-VLAPS]], [[2512.24125|GenieReasoner]], [[2510.16281|SEAL]], [[2510.01623|VLA-R1]], [[2509.25852|REVER]], [[2509.25681|dVLA]], [[2509.22643|VLA-Reasoner]], [[2508.12211|VLAPS]], [[2507.16815|ThinkAct]], [[2503.22020|CoT-VLA]], [[2411.19650|CogACT]], [[2407.08693|ECoT]], [[2405.17418|SC-VLA]]

> [!star] Key Papers
> - [[2604.18486|OneVL]] — First latent CoT to beat explicit autoregressive CoT on driving benchmarks (88.84 PDM-score on NAVSIM) while keeping answer-only inference latency
> - [[2503.22020|CoT-VLA]] — Predicts visual subgoals as chain-of-thought before acting; bridges language reasoning with physical planning
> - [[2509.22643|VLA-Reasoner]] — Online MCTS for test-time reasoning; trades compute for better decisions

**Video-Prediction-Augmented VLAs** — VLAs augmented with video/future-frame prediction.
- [[2606.04968|ForesightFlow]], [[2606.03598|PHASER]], [[2606.03556|VLA Patch Attack]], [[2606.03392|OpenEAI-Platform]], [[2606.02735|S2-VLA]], [[2606.02313|VLA Aerial Nav GRPO]], [[2606.02277|RoboSemanticBench]], [[2606.01955|WALL-WM]], [[2605.12167|MoLA]], [[2605.06192|EA-WM]], [[2605.03821|RoboAlign-R1]], [[2604.26694|X-WAM]], [[2604.25859|PFD]], [[2604.12908|VGA]], [[2604.07209|INSPATIO-WORLD]], [[2604.06168|Action Images]], [[2604.04913|DeltaWorld]], [[2604.01765|DriveDreamer-Policy]], [[2603.19370|VAMPO]], [[2603.16860|DreamPlan]], [[2603.16195|S-VAM]], [[2603.10448|DiT4DiT]], [[2603.03195|CoWVLA]], [[2603.00110|MCSWIM]], [[2602.22010|WoG]], [[2602.11832|JEPA-VLA]], [[2602.10717|SDA]], [[2602.06508|World-VLA-Loop]], [[2601.16163|Cosmos Policy]], [[2512.23864|DreamTacVLA]], [[2511.07732|ViPRA]], [[2509.06951|F1]], [[2507.04447|DreamVLA]], [[2506.00613|WorldGym]], [[2501.18867|UP-VLA]], [[2407.05530|This&That]]

**Latent & JEPA-Augmented VLAs** — VLAs with latent/JEPA-style world modeling.
- [[2606.04436|3DThinkVLA]], [[2606.03127|TTT-VLA]], [[2606.02486|AHEAD]], [[2605.06388|Semantic-LDM-WM]], [[2604.28192|LaST-R1]], [[2604.02097|LatentUM]], [[2603.29844|DIAL]], [[2603.10422|World2Act]], [[2602.10098|VLA-JEPA]], [[2512.13030|Motus]], [[2509.02055|Align-Then-Steer]], [[2502.01828|FOREWARN]]

**Dynamics & Planning-Augmented VLAs** — VLAs coupling dynamics models and planning.
- [[2606.02745|SeeTraceAct]], [[2605.30226|BORA]], [[2605.28527|VLA Value Probing]], [[2605.25044|X-DiffVLA]], [[2605.22446|Pre-VLA]], [[2605.21862|EvoScene-VLA]], [[2605.21854|CrossVLA]], [[2605.21414|PointACT]], [[2605.20774|VLA-REPLICA]], [[2605.15153|Pelican-Unified]], [[2605.10942|HarmoWAM]], [[2605.06481|OA-WAM]], [[2605.06247|CKT-WAM]], [[2605.06222|FFDC-WAM]], [[2605.01799|Embody4D]], [[2604.27792|MotuBrain]], [[2604.26848|STARRY]], [[2604.21741|Hi-WM]], [[2604.17876|OFlow]], [[2604.14732|WVA]], [[2604.09860|RoboLab]], [[2604.05014|StarVLA]], [[2603.19201|OmniVTA]], [[2603.09030|PlayWorld]], [[2602.21633|SC-VLA]], [[2602.20057|AdaWorldPolicy]], [[2602.13977|WoVR]], [[2602.12099|GigaBrain-0.5M*]], [[2602.12063|VLAW]], [[2602.11291|H-WM]], [[2602.11075|RISE]], [[2601.21998|LingBot-VA]], [[2512.09928|HiF-VLA]], [[2512.05955|SIMPACT]], [[2511.19221|Percept-WAM]], [[2511.17502|RynnVLA-002]], [[2511.14659|NORA-1.5]], [[2511.09515|WMPO]], [[2510.11689|Phys2Real]], [[2508.18269|FlowVLA]], [[2506.21539|WorldVLA]], [[2505.15659|FLARE]], [[2410.22689|SIRIUS-FLEET]], [[2304.04321|ARNOLD]], [[2209.07753|Code as Policies]], [[2104.03311|PlasticineLab]]

> [!star] Key Papers
> - [[2602.12063|VLAW]] — Iterative co-improvement loop between VLA policy and world model; each bootstraps the other
> - [[2602.10098|VLA-JEPA]] — JEPA-style latent prediction for leakage-free future state modeling in robot control
> - [[2601.16163|Cosmos Policy]] — Fine-tunes NVIDIA's Cosmos video diffusion model; 98.5% on LIBERO

**RL-Enhanced** — VLAs improved via reinforcement learning post-training, pushing performance beyond what imitation alone achieves.
- [[2606.05468|FlowPRO]], [[2605.13959|WarmPrior]], [[2605.13276|D-VLA]], [[2605.13105|PAIR-VLA]], [[2605.09410|RePO-VLA]], [[2605.05172|Q2RL]], [[2605.03065|OGPO]], [[2605.00416|LWD]], [[2604.27472|PRTS]], [[2604.23073|RLT]], [[2604.19730|FASTER]], [[2604.18107|PDF]], [[2604.17706|OmniVLA-RL]], [[2604.10165|MoRI]], [[2604.08168|ViVa]], [[2604.05614|GPLA]], [[2603.27670|ProgressVLA]], [[2603.26666|VLA-OPD]], [[2603.15600|Active Critic RL]], [[2602.12281|Scaling Verification VLA]], [[2602.01789|RFS]], [[2601.06748|TT-VLA]], [[2511.15605|SRPO]], [[2511.14759|RECAP]], [[2511.01331|RobustVLA]], [[2510.26406|Hi-ORS]], [[2510.25889|piRL]], [[2510.00406|VLA-RFT]], [[2509.19301|ResFiT]], [[2509.15937|VLAC]], [[2509.09674|SimpleVLA-RL]], [[2509.04063|ARFM]], [[2506.08440|TGRPO]], [[2505.22094|ReinFlow]], [[2505.18719|VLA-RL]], [[2505.17016|RIPT-VLA]], [[2505.16517|ManipLVM-R1]], [[2505.03238|RobotxR1]], [[2503.03480|SafeVLA]], [[2502.05450|ConRFT]], [[2501.16664|iRe-VLA]], [[2412.09858|RLDG]], [[2411.19309|GRAPE]], [[2410.24221|EgoMimic]], [[2409.16578|FLaRe]], [[2307.08927|Cable-Routing]], [[1910.11956|Franka Kitchen]]

> [!star] Key Papers
> - [[2604.17706|OmniVLA-RL]] — Introduces Flow-GSPO (SDE reformulation of flow matching); 97.6% on LIBERO with faster, more stable RL than PPO/GRPO
> - [[2505.18719|VLA-RL]] — First systematic RL framework for VLAs; showed RL post-training consistently improves over SFT
> - [[2505.17016|RIPT-VLA]] — Adds a "third stage" of RL training that bridges the gap between simulation and real-world

**Self-Evolving & Continual** — VLAs that can adapt, merge, or evolve autonomously from ongoing experience without catastrophic forgetting.
- [[2606.05395|VASO]], [[2605.26820|VLA Continual Forgetting]], [[2605.22671|BehaviorVLA]], [[2605.13775|RoboEvolve]], [[2605.10993|ECHO-VLA]], [[2605.10903|CapVector]], [[2605.10819|ALAM]], [[2605.08879|ConSFT]], [[2605.01191|Sentinel-VLA]], [[2602.10503|Long-Lived Robots]], [[2602.03445|CRL-VLA]], [[2602.01811|VLA-SCT]], [[2601.09512|CLARE]], [[2601.02295|CycleVLA]], [[2512.14666|EVOLVE-VLA]], [[2511.18810|MergeVLA]], [[2511.16166|EvoVLA]], [[2511.02239|LACY]], [[2511.00091|PLD]], [[2510.12710|Reflective Self-Adaptation]], [[2509.24948|RehearseVLA]], [[2509.21986|Ego VLA Pretrain]], [[2506.07127|APO]], [[2506.06658|SILVR]]

> [!star] Key Papers
> - [[2512.14666|EVOLVE-VLA]] — Continuous adaptation from environmental feedback; addresses the deploy-and-forget problem

**Humanoid & Platform-Specific** — VLAs designed for humanoid robots, loco-manipulation, or domain-specific applications.
- [[2606.05880|TAGA]], [[2605.27724|HumanoidMimicGen]], [[2605.14417|DAJI]], [[2605.03452|BifrostUMI]], [[2604.24916|asRoBallet]], [[2604.23702|QuietWalk]], [[2604.19734|UniT]], [[2604.17807|Re2MoGen]], [[2604.17335|G1 WBC-Gen+Track]], [[2604.07993|HEX]], [[2604.07457|CMP]], [[2604.07430|HY-Embodied-0.5]], [[2604.02707|Humanoid Surgical Instrument Exchange]], [[2604.01158|SMASH]], [[2603.25038|AirVLA]], [[2603.20147|AGILE]], [[2603.15789|OmniReset]], [[2603.12263|Psi0]], [[2603.03279|ULTRA]], [[2602.10106|EgoHumanoid]], [[2602.06341|HiWET]], [[2512.11047|WholeBodyVLA]], [[2512.01061|Sim-to-Real Door]], [[2511.20351|HVS]], [[2511.16518|MiMo-Embodied]], [[2511.15200|VIRAL]], [[2508.16943|LHM-Humanoid]], [[2508.10538|MLM]], [[2508.08328|DQ-Net]], [[2507.06905|ULC]], [[2506.13751|LeVERB]], [[2506.13751|LeVERB]], [[2506.12851|KungfuBot]], [[2504.11054|Meta Motivo]], [[2504.09532|Humanoid-COA]], [[2504.06662|RAMBO]], [[2503.14734|GR00T N1]], [[2503.09527|CombatVLA]], [[2502.20396|Humanoid Sim2Real Dex]], [[2502.14795|Humanoid-VLA]], [[2502.12152|HUMANUP]], [[2411.06782|QuadWBG]], [[2408.00342|MuJoCo MPC HumanoidBench]], [[2403.17367|RoboDuet]], [[2403.16967|VBC]]

> [!star] Key Papers
> - [[2503.14734|GR00T N1]] — NVIDIA's open foundation model for humanoid whole-body control
> - [[2603.12263|Psi0]] — Decoupled locomotion + manipulation for humanoids; practical loco-manipulation

**Multi-Sensor & Force-Aware** — VLAs that go beyond vision by integrating tactile, force, or proprioceptive feedback for contact-rich tasks.
- [[2605.15157|HandITL]], [[2605.14571|MTNet]], [[2604.28156|FlexiTac]], [[2604.27367|DOT-Sim]], [[2604.20689|FingerEye]], [[2603.15257|HapticVLA]], [[2603.15169|ForceVLA2]], [[2603.12665|TacVLA]], [[2602.23648|FAVLA]], [[2602.19764|Multi-Sensory Sparse Experts]], [[2601.20321|TaF-VLA]], [[2511.18960|AVA-VLA]], [[2509.18830|DexSkin]], [[2509.07962|TA-VLA]], [[2508.10333|ReconVLA]], [[2507.09160|Tactile-VLA]], [[2505.22159|ForceVLA]], [[2505.20829|Unified Force-Position Control]], [[2505.06451|Adaptive Wiping]], [[2503.08548|TLA]], [[2502.14420|ChatVLA]]

> [!star] Key Papers
> - [[2507.09160|Tactile-VLA]] — First to integrate 6-axis force feedback into VLAs; critical for assembly and insertion tasks
> - [[2603.15257|HapticVLA]] — Tactile distillation removes the need for sensors at inference; **86.7%** mean SR on contact-rich pick-and-place
> - [[2602.23648|FAVLA]] — Force-injected fast-slow architecture with adaptive frequency control; **80.8%** SR (+38.0 pp over vision-only)

**Architecture Studies** — Systematic explorations of VLA design choices, scaling laws, and novel architectures.
- [[2605.15735|UAM]], [[2605.11564|RIO]], [[2605.06175|VLA-GSE]], [[2605.04678|Pixels-to-Tokens VLA]], [[2605.03941|iWorld-Bench]], [[2605.02757|VideoTransfer-VLA]], [[2604.24182|M2-VLA]], [[2604.23121|DeLock]], [[2604.20012|EmbodiedMidtrain]], [[2604.19728|VLA Foundry]], [[2604.17896|Physical-Feasibility VLA]], [[2604.17887|StableIDM]], [[2604.03191|Compression Gap]], [[2604.02523|Tune to Learn]], [[2604.01570|FAN Prior]], [[2603.28301|LIBERO-Para]], [[2603.24584|TAG]], [[2603.22078|WAM vs VLA Robustness]], [[2603.16861|MolmoBot]], [[2603.12942|ReMem-VLA]], [[2603.12772|PVI]], [[2603.03596|MEM]], [[2602.20687|NativeEmbodied]], [[2602.17659|CAG]], [[2602.11236|ABot-M0]], [[2601.18692|LingBot-VLA]], [[2601.02456|InternVLA-A1]], [[2512.02834|TACO]], [[2511.18085|Stellar VLA]], [[2511.05275|TwinVLA]], [[2510.22201|ACG]], [[2510.19430|GigaBrain-0]], [[2510.17950|RoboChallenge]], [[2510.13054|VLA-0]], [[2510.10274|X-VLA]], [[2510.09459|FIPER]], [[2510.07077|VLA Robotics Real-World Review]], [[2510.05681|MG-Select]], [[2510.04354|SureSim]], [[2509.14889|CollabVLA]], [[2509.11417|VLA Pretrain Preserve]], [[2509.09372|VLA-Adapter]], [[2509.04018|FPC-VLA]], [[2508.19236|MemoryVLA]], [[2507.17049|VLA Uncertainty Eval]], [[2507.10672|VLA Manipulation Survey]], [[2506.19850|UniVLA]], [[2506.17561|VLA-OS]], [[2506.09937|SAFE]], [[2506.00123|VeBrain]], [[2412.14058|RoboVLMs]], [[2412.10345|TraceVLA]], [[2409.03299|RT-1-X SCARA Transfer]]

> [!star] Key Papers
> - [[2412.14058|RoboVLMs]] — 600+ experiments systematically testing VLA design choices; the definitive recipe paper

> [!tip] The VLA Stack
> Pick a VLM backbone (PaliGemma) → add action head (flow matching) → fine-tune on in-domain data → post-train with RL. This is the proven recipe from RoboVLMs.


**Failure Detection & Recovery** — VLAs and VLMs trained to detect, diagnose, and recover from robotic manipulation failures.
- [[2605.16056|Health-VLA]], [[2604.21192|VLA Open-World Audit]], [[2604.20472|TDQC]], [[2604.18791|HELM]], [[2604.16677|ReconVLA]], [[2604.13788|Failure ID Filtering]], [[2603.18091|ADV]], [[2603.13528|Counterfactual Failure Synthesis]], [[2603.11106|RC-NF]], [[2603.06987|Foundational WM]], [[2602.16182|WM Failure Classifier]], [[2602.12405|Self-Refining VLM Failure]], [[2602.11124|PhyCritic]], [[2602.01515|RAPT]], [[2601.07821|FARL]], [[2512.03913|VINE]], [[2512.02787|ViFailback]], [[2512.01946|FailCoT]], [[2510.02298|ARMADA]], [[2510.01642|FailSafe]], [[2509.16072|I-FailSense]], [[2509.04018|FPC-VLA]], [[2507.17383|VLA Confidence Calibration]], [[2507.00435|RoboEval]], [[2505.12224|RoboFAC]], [[2505.08548|FSD]], [[2505.05811|M-SVDD]], [[2504.11170|Sparse MAF-AAE]], [[2503.15202|VLM-BT Failure Handling]], [[2503.08558|FAIL-Detect]], [[2412.04455|Code-as-Monitor]], [[2410.14868|Diff-DAgger]], [[2410.04640|Sentinel]], [[2410.00371|AHA]], [[2409.19190|RAIL]], [[2409.03966|VLM Failure Recovery]], [[2407.08735|AESOP]], [[2406.15917|BGR]], [[2406.11548|AIC MLLM]], [[2404.00756|Recover]], [[2310.17552|Sirius-Runtime]], [[2306.15724|REFLECT]], [[2303.07280|SuccessVQA]]

> [!star] Key Papers
> - [[2510.01642|FailSafe]] — Automatic pipeline generating failure-action data; boosts VLA success by up to 22.6%
> - [[2505.12224|RoboFAC]] — Lightweight failure critic outperforming GPT-4o; improves real-world success by 29.1%
> - [[2410.00371|AHA]] — NVIDIA's failure reasoning VLM; generalizes from sim to real with procedurally generated failure data


**Adversarial Robustness & Red-Teaming** — Auditing VLAs by generating adversarial linguistic, visual, and physical perturbations that surface unsafe or fragile behaviors before deployment. Spans linguistic fragility (DAERT, Q-DIG, ERT), visual/3D patches (EDPA, Tex3D, UADA-UPA-TMA), gradient-coordinate jailbreaks (GCG-VLA), backdoor attacks (AttackVLA), and physically grounded scene attacks (RedVLA).
- [[2606.02307|FATE-VLA]], [[2605.30834|Hide-and-Seek]], [[2604.22591|RedVLA]], [[2604.05595|DAERT]], [[2604.01618|Tex3D]], [[2603.12510|Q-DIG]], [[2511.12149|AttackVLA]], [[2510.13237|EDPA]], [[2506.03350|GCG-VLA]], [[2411.18676|ERT]], [[2411.13587|VLA Adversarial Vulnerabilities]]

> [!star] Key Papers
> - [[2604.05595|DAERT]] — RL-based diversity-aware red-teaming reduces π0 success from 93.33% to 5.85% with strong cross-VLA transferability
> - [[2604.22591|RedVLA]] — Two-stage physical red-teaming via risk-scenario synthesis + trajectory-driven amplification; 64.9-95.5% ASR across six VLAs
> - [[2506.03350|GCG-VLA]] — Greedy Coordinate Gradient adapts LLM jailbreaking to VLA control authority; 90%+ targeted-action success on OpenVLA, sim-to-real transfer
> - [[2511.12149|AttackVLA]] — First unified benchmark for adversarial + backdoor attacks on VLAs; BackdoorVLA achieves 50% targeted success on physical Franka arm

> [!success] VLA Red-Team Recipe
> ==Diversity-aware adversary== (DAERT, Q-DIG) generates linguistic perturbations → ==physical/3D attack surfaces== (Tex3D, RedVLA, EDPA) probe visual robustness → ==gradient-based suffix attacks== (GCG-VLA) test action-space reachability → ==adversarial fine-tuning== (Q-DIG, EDPA-defense) closes the loop. Failure-mining and adversarial robustness are now the same problem viewed from opposite sides.

> [!success] Failure-Mining ↔ Failure-Avoidance ↔ WAM-as-Eval Bridge
> Three threads converge on the same loop:
> - **RL failure-search**: [[2412.02818|RoboMD]], [[2604.05595|DAERT]], [[2509.03771|Co-Evolving MARL]], [[1903.10654|FAILMAKER-ADVRL]] — RL learns adversaries that mine failures.
> - **Non-RL VLA red-team**: [[2604.22591|RedVLA]], [[2604.05595|DAERT]], [[2604.01618|Tex3D]], [[2603.12510|Q-DIG]], [[2511.12149|AttackVLA]], [[2510.13237|EDPA]], [[2506.03350|GCG-VLA]], [[2411.18676|ERT]], [[2411.13587|VLA Adversarial Vulnerabilities]], [[2509.18953|Eva-VLA]] — gradient/QD/scene attacks mine VLA failures without RL.
> - **Failure-avoidance**: [[2601.07821|FARL]] — failure-aware policy regularization closes the loop.
> - **WAM-as-eval**: [[2506.00613|WorldGym]], [[2510.21232|Confusing World Models]] — world models become the evaluator, not just the simulator.
> The cross-recipe: mine failures (RL or QD) → train avoidance (FARL) → re-evaluate inside a WAM (WorldGym) → repeat.

> [!note] Open Research Wedge
> Two cells are conspicuously empty in the literature:
> - **(RL scene-adversary) × (VLA target)** — DAERT uses RL on linguistic adversaries against VLAs; FAILMAKER-ADVRL/Co-Evolving MARL use RL on scene/agent adversaries against rule-based or RL agents. No paper yet trains a *physics-grounded RL adversary that perturbs the scene* to attack a VLA. RedVLA does scene attacks but with gradient-free optimization, not RL.
> - **(RL failure-search) × (WAM target)** — Confusing World Models perturbs world-model dynamics statically; WorldGym evaluates inside a WAM. No paper closes the loop with an RL adversary that searches for WAM-confusing trajectories at training time. This is the natural intersection of [[04_Reinforcement-Learning|adversarial RL]] and [[2506.00613|WorldGym]]-style WAM-as-environment.


---

## 3. World Action Models (WAMs)

WAMs go beyond VLAs by jointly predicting future states and actions — they learn the physics of the world, not just how to imitate demonstrations. The key architectural question is *where* to predict: in pixel space (video generation), latent space (JEPA-style), or action space only (efficient WAMs).

**Dreamer Lineage** — The original model-based RL approach: learn world dynamics in compressed latent space via recurrent state-space models, then plan entirely in "imagination."
- [[2605.09196|RigidFormer]], [[2605.04709|ELVIS]], [[2605.04568|Dream-MPC]], [[2509.24527|Dreamer 4]], [[2503.21047|CBET-DreamerV3]], [[2502.05907|EvoAgent]], [[2405.18418|Puppeteer]], [[2401.16650|WMAR]], [[2301.04104|DreamerV3]], [[2211.15944|Continual-Dreamer]], [[2206.14176|DayDreamer]], [[2206.02072|VSRL]], [[2007.07853|γ-Progress]], [[2005.05960|Plan2Explore]], [[1912.01603|Dreamer]], [[1911.10601|Scaling Active Inference]], [[1803.10122|World Models]]

> [!star] Key Papers
> - [[2206.14176|DayDreamer]] — First to deploy Dreamer on real robots; proved sample-efficient learning from imagination works physically

**Action-Conditioned Video World Models** — Video WMs conditioned on actions/policies.
- [[2606.05773|PiL-World]], [[2606.05645|Discrete-WAM]], [[2606.05015|Quadrotor World Model Study]], [[2606.04907|WAM-Nav]], [[2606.04463|OSCAR]], [[2606.04130|CLAW (Latent Action WM)]], [[2606.03943|PointAction]], [[2606.03188|GeoSem-WAM]], [[2606.03159|OmniDreams]], [[2606.02800|Cosmos 3]], [[2606.02577|RoboDream]], [[2606.01027|τ0-WM]], [[2605.25874|WBench]], [[2605.23993|Nano World Models]], [[2605.15725|DiLA]], [[2605.08567|ACWM-Phys]], [[2604.08995|Matrix-Game 3.0]], [[2603.23376|ABot-PhysWorld]], [[2603.17117|MosaicMem]], [[2603.12639|RoboStereo]], [[2603.08546|Interactive World Simulator]], [[2603.07799|MWM]], [[2602.15922|DreamZero]], [[2601.15533|Actionable Simulators]], [[2512.15692|mimic-video]], [[2508.03645|DiWA]], [[2412.14803|VPP]], [[2408.14472|DWL]], [[2312.10812|LAPO]], [[2310.06114|UniSim]], [[2203.01914|Playable Environments]], [[2101.12195|CADDY]]

**Physics & Dynamics Video World Models** — Physics-grounded and dynamics-aware video WMs.
- [[2606.02280|LDG]], [[2604.14268|HY-World 2.0]], [[2603.25716|HyDRA]], [[2603.15759|SimDist]], [[2602.07050|Interpreting Physics Video WM]], [[2512.06628|MIND-V]], [[2511.07416|PhysWorld]], [[2510.21447|PhysWorld-Deformable]], [[2411.02385|PhyWorld]]

**Video Generation Backbones for WMs** — Video-generation backbones used as world models.
- [[2605.30347|NeuROK]], [[2605.28816|Gamma-World]], [[2605.26535|RecFM]], [[2605.26379|LeJEPA World Model]], [[2605.25313|UWM-JEPA]], [[2605.21800|stable-worldmodel]], [[2605.19957|WEM]], [[2605.15178|SANA-WM]], [[2605.11367|3D-Belief]], [[2605.09131|MCP-Cosmos]], [[2605.01694|Latent State Design WM]], [[2604.18564|MultiWorld]], [[2604.13036|Lyra 2.0]], [[2604.11351|WM-DAgger]], [[2604.04502|Veo-Act]], [[2603.25685|Persistent Robot World Models]], [[2602.17259|FRAPPE]], [[2602.10102|VideoWorld 2]], [[2601.20540|LingBot-World]], [[2512.24766|Dream2Flow]], [[2512.00961|GenReward]], [[2511.19861|GigaWorld-0]], [[2510.26583|Emu3.5]], [[2510.01183|EvoWorld]], [[2508.00795|Video Policy]], [[2505.13934|RLVR-World]], [[2505.12705|DreamGen]], [[2504.15369|Inverse Probabilistic Adaptation]], [[2502.00622|GPC]], [[2412.14957|DREMA]], [[2408.02272|COM Kitchens]], [[2406.13301|ARDuP]], [[2403.04253|R2I]], [[2310.10625|VLP]], [[2302.00111|UniPi]], [[2103.10369|RH-UCRL]], [[1806.09655|CLASP (Action Space)]]

> [!star] Key Papers
> - [[2602.15922|DreamZero]] — 14B parameter WAM from NVIDIA; zero-shot robot policies via joint video+action prediction; 39.5% on unseen tasks
> - [[2310.06114|UniSim]] — Universal simulator from video diffusion; learns interaction dynamics from heterogeneous data
> - [[2412.14803|VPP]] — Extracts visual representations from video diffusion in a single forward pass (no iterative denoising at test time)

**Efficient / Action-Centered** — WAMs optimized for speed: focus compute on action prediction rather than full video generation. Key insight: you need video modeling at *training time* for learning physics, but not at *test time* for acting.
- [[2606.05254|Flash-WAM]], [[2605.08732|GC-IDM]], [[2604.01985|WAV]], [[2603.17240|GigaWorld-Policy]], [[2603.16666|Fast-WAM]], [[2512.19133|WorldRFT]], [[2506.22007|RoboEnvision]], [[2504.16680|RWM-U]], [[2503.16806|DyWA]], [[2412.15109|Seer]], [[2411.08380|EgoVid-5M]], [[2410.00564|JOWA]], [[2203.13116|EgoPAT3D]], [[1906.03327|HowTo100M]]

> [!star] Key Papers
> - [[2603.16666|Fast-WAM]] — Proved training-time video modeling is what matters, not test-time imagination; 97.6% on LIBERO
> - [[2603.17240|GigaWorld-Policy]] — 9x speedup over DreamZero via action-centered design with training-only video supervision

**Latent Prediction** — Predict future states in a learned latent space (JEPA-style) rather than reconstructing pixels. Faster, more robust to visual noise, and better suited for real-time control.
- [[2605.00078|Being-H0.7]], [[2604.26182|LWM]], [[2604.03208|HWM]], [[2603.25981|PiJEPA]], [[2603.22281|ThinkJEPA]], [[2603.19312|LeWM]], [[2603.14482|V-JEPA 2.1]], [[2603.05815|HiLAM]], [[2602.06130|SWIRL]], [[2602.02381|AdaSSL]], [[2601.14354|VJEPA-Probabilistic]], [[2601.05230|Latent Action World Models]], [[2512.09929|OWM]], [[2511.08544|LeJEPA]], [[2510.26433|CoLA-World]], [[2510.15047|SPA]], [[2507.19468|DINO-world]], [[2507.13340|LPS]], [[2506.23468|NavMorph]], [[2506.09985|V-JEPA 2]], [[2505.13696|ESWM]], [[2505.11528|LaDi-WM]], [[2505.03176|seq-JEPA]], [[2504.16591|JEPA for RL]], [[2504.02792|UWM]], [[2503.18938|AdaWorld]], [[2503.00200|UVA]], [[2502.14819|PLDM]], [[2403.08321|ManiGaussian]], [[2301.08243|I-JEPA]]

> [!star] Key Papers
> - [[2504.02792|UWM]] — Unified World Models: a single architecture handling action-conditioned, action-free, and video prediction tasks
> - [[2506.23468|NavMorph]] — Self-evolving world model for navigation; Contextual Evolution Memory updates latent representations online

**VLM-Integrated** — Combine the semantic reasoning of VLMs with the physics simulation of world models for high-level planning + low-level control.
- [[2604.02190|UniDriveVLA]], [[2603.28963|AutoWorld]], [[2603.28116|AutoDrive-P3]], [[2603.27287|Uni-World VLA]], [[2603.14497|WorldVLM]], [[2603.08572|MetaWorld-X]], [[2602.15549|VLM-DEWM]], [[2602.08236|AVIC]], [[2602.05842|RWML]], [[2602.01960|GVP-WM]], [[2602.00475|GRASP]], [[2601.14514|JIT]], [[2512.15885|JARVIS]], [[2512.07733|SpatialDreamer]], [[2511.02824|Kosmos AI Scientist]], [[2510.00855|DyVA]], [[2509.19080|World4RL]], [[2509.02722|VLWM]], [[2507.23773|SimuRA]], [[2507.12508|MindJourney]], [[2505.05626|PERCEPTLLM]], [[2503.00761|TRACE]], [[2403.06845|DriveDreamer-2]], [[2309.17024|HoloAssist]]

> [!star] Key Papers
> - [[2602.08236|AVIC]] — Adaptive: decides when and how much to imagine based on task difficulty; 17x fewer world-model calls

**Self-Evolving WAMs** — WAMs designed to continuously improve through experience-driven loops, curiosity, and reflective planning.
- [[2604.07392|ERA]], [[2603.15381|Autonomous Learning Framework]], [[2602.04411|Self-evolving Embodied AI]], [[2509.15155|Self-Improving EFM]], [[2507.09177|Online Agent (OA)]], [[2504.21024|WebEvolver]]

> [!star] Key Papers
> - [[2602.04411|Self-evolving Embodied AI]] — Defines the paradigm: agents that autonomously acquire, refine, and transfer skills across environments

**Physics-Aware World Simulators** — Generative world simulators with explicit physics-fidelity goals: action-conditioned video generation aligned with physical laws via RL, reward signals, or world-model surprise. The bridge between video-generation research and embodied control: papers here close the loop with action conditioning, often directly evaluating on robotics benchmarks.
- [[2604.22152|dWorldEval]], [[2604.16484|DexWorldModel]], [[2603.03505|PhyPrompt]], [[2602.12215|LDA-1B]], [[2602.09878|MVISTA-4D]], [[2602.02454|World-Gymnast]], [[2601.04153|Diffusion-DRF]], [[2601.03665|PhysVideoGenerator]], [[2512.16023|CoVAR]], [[2512.15840|LV-P]], [[2512.10675|Veo Robotics]], [[2512.06963|VideoVLA]], [[2512.03556|RoboScape-R]], [[2511.20280|VLM-Refine Physics Video]], [[2511.03997|PhysCorr]], [[2511.00062|Physical AI World Sim]], [[2510.21840|V-JEPA-2 Physics Reward]], [[2509.24702|Implausibility Reasoning Video Gen]], [[2509.21309|NewtonGen]], [[2508.10858|PhysHPO]], [[2506.23135|RoboScape]], [[2506.18655|RDPO]], [[2506.01103|DeepVerse]], [[2505.23656|VideoREPA]], [[2505.21996|VRAG-WM]], [[2505.09723|EnerVerse-AC]], [[2504.20995|TesserAct]], [[2504.15397|MirrorVerse]], [[2504.13129|Science-T2I]], [[2503.18945|Aether]], [[2503.08153|WISA]], [[2502.02088|IPO]], [[2502.01784|VILP]], [[2501.13918|VideoAlign]], [[2501.09038|Physics-IQ]], [[2412.20404|Open-Sora]], [[2412.08410|DrivePhysica]], [[2412.02617|AIF-Dynamic-T2V]], [[2412.00596|PhyT2V]], [[2411.18179|PAD]], [[2410.18072|WorldSimBench]], [[2410.13571|DriveDreamer4D]], [[2410.10076|VideoAgent]], [[2410.05582|Gen-Drive]], [[2410.00425|ManiSkill3]], [[2409.19499|FastUMI]], [[2409.16283|Gen2Act]], [[2408.07009|Imagen 3]], [[2406.16862|Dreamitate]], [[2404.05014|MagicTime]], [[2403.09227|BEHAVIOR-1K]], [[2401.09985|WorldDreamer]], [[2309.17080|GAIA-1]], [[2109.13396|Bridge]], [[2107.14483|ManiSkill]]

> [!star] Key Papers
> - [[2501.09038|Physics-IQ]] — Diagnostic study showing visual realism does not imply physical understanding; the canonical "do generative video models learn physics?" probe
> - [[2309.17080|GAIA-1]] — Wayve's 9B autoregressive driving world model; foundational result that internet-scale video pretraining yields a useful driving world simulator
> - [[2501.03575|Cosmos]] — NVIDIA's open foundation video world model platform for Physical AI; covered separately above as a video-policy backbone
> - [[2603.24506|PhyGenesis]] — Physically consistent multi-view driving video world model under challenging trajectories; co-trained on nuScenes + CARLA with a 6-DoF Physical Condition Generator that rectifies physics-violating trajectories before generation
> - [[2509.21309|NewtonGen]] — Embeds physics-informed neural ODEs (linear ODEs + residual MLP) into T2V; explicit Newtonian motion with **0.98** Physical Invariance Score on 12 motion types from only 100 physics-clean clips

**Surveys** — Comprehensive reviews of world model architectures, taxonomies, and design principles.
- [[2605.12090|WAM Survey]], [[2605.03413|NEO Theorizer]], [[2605.00080|WM Robot Learning Survey]], [[2604.22748|Agentic World Modeling Survey]], [[2604.16592|Cognition WM Survey]], [[2604.04707|OpenWorldLib]], [[2603.28489|Video Gen as WM Survey]], [[2603.25887|WR-Arena]], [[2602.01630|Unified World Model Framework]], [[2511.08585|Visual World Roadmap]], [[2511.02097|WM Manipulation Survey]], [[2510.16732|World Models for Embodied AI Survey]], [[2509.20021|Embodied AI LLM-WM Survey]], [[2506.22355|Embodied AI World Modeling]], [[2506.01622|General Agents World Models]], [[2504.04170|Digital Gene]], [[2411.14499|World Models Survey]], [[2407.06886|ARIO]], [[2310.06253|Objective Mismatch MBRL Survey]]

- [[2604.23775|VLA Safety Survey]] — First comprehensive review of VLA safety threats, defenses, and evaluation; unifies fragmented adversarial-robustness research
- [[2510.24795|Efficient VLA Survey]] — First dedicated survey on efficient VLAs
- [[2509.19012|Pure VLA Survey]] — Taxonomy of VLA action-generation paradigms
- [[2508.13073|Large VLM-based VLA Survey]] — First taxonomy-oriented VLA review
> [!star] Key Papers
> - [[2411.14499|World Models Survey]] — Most comprehensive world model survey; distinguishes "understanding" vs "predicting" paradigms
> - [[2602.01630|Unified World Model Framework]] — Argues world model research must go beyond task-specific injection; proposes a unified framework

> [!tip] Video vs Latent
> DreamZero proves video generation works at scale, but Fast-WAM shows you only need video at *training time*. For deployment, latent prediction (UWM, VLA-JEPA) is faster and more practical.

---

## 4. Self-Evolving Embodied AI

The frontier of embodied AI: robots that improve themselves through experience without human intervention. These systems combine world models (for imagination), continual learning (for memory), curiosity (for exploration drive), and evolutionary algorithms (for policy improvement). See [[11_Self-Evolving-AI]].

- [[2502.05907|EvoAgent]] (2025) — ==self-evolving agent== with continual world model for long-horizon tasks; **+105%** improvement
- [[2506.21669|SEEA-R1]] (2025) — ==tree-structured RL== for self-evolving embodied agents; **+24%** via MCTS + generative reward
- [[2503.01584|SENSEI]] (2025) — ==semantic exploration== with epistemic uncertainty + Go-Explore for versatile world models
- [[2510.16079|EVOLVER]] (2025) — LLM agents self-evolving through experience-driven lifecycle
- [[2603.08403|SPIRAL]] (2026) — ==closed-loop framework== for self-improving action world models via reflective planning
- [[2510.12693|ERA]] (2025) — VLMs transformed into embodied agents via embodied prior learning + online RL

- [[2508.04700|SEAgent]] (2025) — ==self-evolving curriculum== with World State Model for computer use agents
- [[2310.08367|MCU]] (2023) — Evaluation framework for open-ended game agents with AutoEval VLM judging

> [!star] Key Papers
> - [[2502.05907|EvoAgent]] — Built on DreamerV3 with continual world model; demonstrated self-planning + self-control + self-reflection loop
> - [[2603.08403|SPIRAL]] — Closed-loop self-improvement for WAMs via reflective planning; the system critiques its own failures and adapts

> [!tip] The Self-Evolving WAM Path
> The ideal trajectory: train a WAM → add continual learning → add curiosity-driven exploration → self-evolving robot.

---

## 5. Navigation & Autonomous Driving

Both navigation and driving reduce to the same core problem: perceive the environment, predict its future state, and plan a trajectory. Navigation operates at room/building scale with discrete goals; driving operates at city scale with continuous safety constraints.

**Indoor Object-Goal Navigation** — Find and navigate to target objects in unseen environments using visual reasoning, cognitive maps, or LLM-based planning.
- [[2605.25685|HumanFlow]], [[2605.22814|Remember to be Curious]], [[2605.21935|MIF]], [[2605.14174|VIA]], [[2605.12689|3D RL-DWA]], [[2605.10118|SAGE]], [[2605.06595|CRONA]], [[2605.03846|SigLoMa]], [[2604.26504|HiPAN]], [[2604.09445|AsymLoc]], [[2604.02829|STRNet]], [[2603.29165|LatentPilot]], [[2603.07799|MWM]], [[2603.02772|ASER]], [[2601.13132|GaussExplorer]], [[2510.20685|C-Nav]], [[2508.05634|Conformal Crowd Navigation]], [[2506.17629|CLiViS]], [[2506.05997|SRU]], [[2412.10439|CogNav]], [[2402.19161|MemoNav]], [[2401.05946|TDB]], [[2301.13261|Blind Nav Agents]], [[2101.05181|MemAug Image-Goal Nav]], [[2012.03912|MultiON]]

> [!star] Key Papers
> - [[2412.10439|CogNav]] — Models human-like cognitive processes for navigation; outperforms reactive policies on complex layouts

**Vision-Language Navigation** — Follow natural language instructions through visual environments, requiring grounding of spatial language to visual observations.
- [[2604.24391|FreqCache]], [[2604.07957|WorldMAP]], [[2603.25981|PiJEPA]], [[2507.13152|SE-VLN]], [[2506.15757|WPCL]], [[2405.07060|Memory-Maze]]

> [!star] Key Papers
> - [[2506.15757|WPCL]] — Weakly-supervised VLM-guided contrastive learning for VLN; reduces annotation cost while improving grounding

**Autonomous Driving (World Model Perspective)** — Driving as a world model problem: predict the scene's future, then plan safe trajectories.
- [[2606.05159|X4Val]], [[2606.03296|SC-Diff Planning]], [[2605.05328|Query2Uncertainty]], [[2605.04470|CRAFT Driving]], [[2604.26065|FlowS]], [[2604.25329|ProDrive]], [[2604.18486|OneVL]], [[2604.17651|I-WM]], [[2604.12942|RMGS-SLAM]], [[2604.11734|Multi-ORFT]], [[2604.10856|BridgeSim]], [[2604.03023|Behavior-Constrained RL]], [[2604.01765|DriveDreamer-Policy]], [[2603.28887|OccSim]], [[2603.24581|Latent-WAM]], [[2603.24506|PhyGenesis]], [[2603.15771|CorrectionPlanner]], [[2603.14851|AutoMoT]], [[2603.14497|WorldVLM]], [[2602.18739|PhysAtt]], [[2512.24426|CF-VLA]], [[2512.24331|LVLDrive]], [[2511.23369|SimScale]], [[2509.01944|AutoDrive-R2]], [[2505.17685|FSDrive]], [[2503.20654|AccidentSim]], [[2409.18964|PhysGen]], [[2403.06845|DriveDreamer-2]], [[2008.01655|Adaptive Memory VO]]

**Safety-Critical Scenario Generation (Driving)** — Adversarial RL, generative, and counterfactual methods for synthesizing rare safety-critical traffic scenarios that stress-test AV stacks. Bridges driving WMs (above) with adversarial RL ([[04_Reinforcement-Learning|§4]]).
- [[2605.00880|AFM]], [[2603.21104|CounterScene]], [[2603.04071|SaFeR]], [[2510.10937|Neutral Adversarial Policy]], [[2508.02027|Dual-DM]], [[2206.09682|SafeBench]], [[1903.10654|FAILMAKER-ADVRL]]

> [!star] Key Papers
> - [[2603.21104|CounterScene]] — Counterfactual causal reasoning in generative WMs; resolves the realism-adversarial trade-off via causal-agent identification + minimal interventions
> - [[2206.09682|SafeBench]] — Unified Carla benchmarking platform with 8 NHTSA pre-crash scenarios + 4 generation algorithms + 10 multi-level metrics
> - [[1903.10654|FAILMAKER-ADVRL]] — Foundational MADDPG-based adversarial RL for natural failure-scenario generation; balances adversarial reward with personal reward for realism
> - [[2605.00880|AFM]] — Adversarial flow matching produces imperceptible 1-NFE perturbations causing 88% attack success on Transformer-backbone end-to-end driving stacks

> [!tip] Infrastructure vs Ego-Centric
> Most driving WMs are ego-centric (the car's view). I-WM flips the frame: fixed roadside sensors give "temporal depth" over a location, complementing ego-vehicle "spatial breadth". Expect infrastructure + V2X world models to be a growing thread alongside ego-centric DriveDreamer-style generators.

> [!star] Key Papers
> - [[2403.06845|DriveDreamer-2]] — LLM-enhanced driving video generation; creates diverse scenarios for world model training
> - [[2603.14497|WorldVLM]] — Hybrid VLM + world model architecture; combines semantic reasoning with physics prediction for driving

**Surveys & Roadmaps** — Reviews of embodied navigation and spatial intelligence.
- [[2512.24385|Spatial Intelligence Roadmap]], [[2311.00530|LLM Embodied Navigation Survey]]

> [!star] Key Papers
> - [[2512.24385|Spatial Intelligence Roadmap]] — Comprehensive roadmap for multi-modal spatial pre-training in autonomous systems; defines the field's trajectory
> - [[2311.00530|LLM Embodied Navigation Survey]] — First survey connecting LLM advances to embodied navigation; maps the integration landscape

> [!tip] Navigation → Driving
> Both reduce to "predict the future scene, then plan a trajectory." The difference is scale and safety constraints. World model approaches transfer between them.

---

## 6. Imitation Learning & RL for Robotics

The training paradigm question: pure imitation learning (behavior cloning) is simple but plateaus at the demonstration distribution ceiling. Adding RL post-training pushes policies beyond what demonstrations alone can teach — handling novel situations, recovering from errors, and optimizing long-horizon objectives.

**RL-Augmented Imitation** — Combine imitation learning with RL reward signals to overcome the limitations of pure behavior cloning.
- [[2606.06194|ActiveMimic]], [[2606.04825|HapTile]], [[2606.04269|Instant-Fold]], [[2606.03985|Humanoid-GPT]], [[2606.03536|Bionic Whole-Body Control]], [[2606.03512|SPADE]], [[2606.03268|EaDex]], [[2606.01951|Ego-Video Robot Nav]], [[2606.01851|PHASOR]], [[2605.27114|VR-DAgger]], [[2605.25829|OASIS]], [[2605.22272|Imagine2Real]], [[2605.20811|Demo-JEPA]], [[2605.14810|CaMeRL]], [[2605.10063|EFGCL]], [[2605.09789|DRIS]], [[2605.09772|GP-Safe-Exploration]], [[2605.05544|AQC]], [[2604.20841|DeVI]], [[2604.10953|DRL-3DBP]], [[2604.10677|LIDEA]], [[2604.08958|WOMBET]], [[2604.06943|Sustainable Transfer RL]], [[2604.04539|FlashSAC]], [[2604.03037|ARM]], [[2604.02260|Time-Varying MBRL]], [[2603.13925|SmoothVLA]], [[2603.04029|Self-Adapting RL]], [[2602.16863|SimToolReal]], [[2602.15827|PHP]], [[2512.05094|GenMimic]], [[2510.25992|SRL]], [[2510.22512|TRL]], [[2510.19307|RIL]], [[2509.19292|SOE]], [[2509.04259|RL's Razor]], [[2507.23523|H-RDT]], [[2505.13709|Policy-Driven WM Adaptation]], [[2505.03181|AFSFT]], [[2504.18471|AFM]], [[2503.24361|Sim-and-Real Co-Training]], [[2503.14858|CRL]], [[2408.05804|Single-Goal Contrastive RL]], [[2407.16677|ResiP]], [[2403.03949|RialTo]], [[2311.03351|Uni-O4]], [[2210.10765|PAINT]], [[2202.02005|BC-Z]], [[2010.15920|Recovery RL]], [[2010.11944|SPiRL]], [[1805.07914|ILPO]]

> [!star] Key Papers
> - [[2505.03181|AFSFT]] — Advantage-filtered SFT: uses RL advantage estimates to select which demonstrations to learn from

**Reward Learning** — Learn reward functions from visual feedback or human preferences to guide robot training without hand-crafted reward engineering.
- [[2606.04718|CoRe-MoE]], [[2606.03963|AgenticRL]], [[2606.03940|SEAOTTER]], [[2606.03476|Human2Humanoid]], [[2606.03441|PerchRL]], [[2605.30350|DynaFLIP]], [[2605.28442|COTRATE]], [[2605.27046|Thermal-Aware Residual]], [[2605.26478|SDPG]], [[2605.26452|Koopman-CBF SAC]], [[2605.24934|HumanEgo]], [[2605.22123|FLORA]], [[2605.21710|PGDG]], [[2605.21688|Microfiber Shape Control]], [[2605.20373|SUGAR]], [[2605.19924|RoHIL]], [[2605.12771|PASTA]], [[2605.11020|TRIRL]], [[2605.08774|ProcVLM]], [[2604.16391|DeFI]], [[2604.10962|ScoRe-Flow]], [[2603.28730|SOLE-R1]], [[2603.02115|Robometer]], [[2602.11393|Visual Motion Pref Modeling]], [[2602.02481|FPO++]], [[2601.16973|VisGym]], [[2512.20675|VLM Reward Objectives]], [[2512.01996|Humanoid Loco 15min]], [[2511.14565|Masked IRL]], [[2511.04131|BFM-Zero]], [[2509.23745|LocoFormer]], [[2507.12440|EgoVLA]], [[2505.22642|FastTD3]], [[2505.17006|CoMo]], [[2505.09561|PTP]], [[2502.10550|MIKASA]], [[2502.01143|ASAP]], [[2501.10395|t-DGR]], [[2212.07740|TERT]], [[2111.09793|Robotic Interestingness]], [[2108.03298|Robomimic]], [[2107.04034|RMA]], [[2107.03996|LocoTransformer]], [[2104.10218|Episodic Memory Manipulation]], [[2003.01239|Evolutionary Meta-Learning Legged]]

> [!star] Key Papers
> - [[2512.20675|VLM Reward Objectives]] — Simple triplet loss on VLMs produces effective reward signals for robot learning

**Continual & Experience-Driven** — Agents that improve from ongoing real-world interaction without catastrophic forgetting.
- [[2604.15814|Continual Hand-Eye Calibration]], [[2604.11306|Hierarchical Episodic Memory]], [[2604.10892|HECTOR]], [[2604.10096|ABot-Claw]], [[2604.07799|ECM]], [[2603.24350|Emergent Self]], [[2603.03818|VLA Continual Learning]], [[2510.08558|Early Experience]], [[2207.07560|SkiMo]]

> [!star] Key Papers
> - [[2603.03818|VLA Continual Learning]] — Showed pre-trained VLAs have surprising resistance to catastrophic forgetting during continual adaptation

> [!tip] When to Add RL
> Pure imitation plateaus at the demonstration distribution. Add RL post-training (RIPT-VLA, VLA-RL) to improve robustness beyond what demonstrations alone can teach.

---

## 7. Embodied AI — General

Cross-cutting research that doesn't fit neatly into manipulation, VLAs, or navigation — but addresses fundamental challenges like cross-embodiment transfer, scene understanding, and domain adaptation that all embodied AI systems face.

**Generalist Architectures** — Modular frameworks designed to work across different robot types, sensor configurations, and task domains.
- [[2605.26637|Embodied Tool Protocol]], [[2605.25813|EQA-Decision]], [[2605.11381|Kairos]], [[2605.02900|Safety in Embodied AI Survey]], [[2604.21568|Bayesian Triage Robot]], [[2604.19839|EUEA]], [[2604.15475|NeuroMesh]], [[2604.11373|Minimal Embodiment]], [[2604.10929|Ro-SLM]], [[2604.09330|VAG]], [[2604.01179|Florence-2 ROS 2 Wrapper]], [[2604.00061|R2X Multi-Robot MLLM Survey]], [[2603.22201|NMR]], [[2602.16444|RoboGene]], [[2511.07820|SONIC]], [[2510.21817|VITA-E]], [[2508.07033|P3]], [[2508.01415|RoboMemory]], [[2507.12846|Mind Palace]], [[2505.13948|Memory-Centric EQA]], [[2412.07755|SAT]], [[2410.02742|GLIMO]], [[2409.20537|HPT]], [[2409.18313|Embodied-RAG]], [[2402.15116|LMA Survey]]

> [!star] Key Papers
> - [[2409.20537|HPT]] — Heterogeneous Pre-trained Transformers: modular architecture that handles diverse robot embodiments through shared trunk + task-specific heads

**Hardware & Simulation Platforms** — Robotic hardware designs and simulation environments that enable large-scale data collection and policy evaluation.
- [[2605.12654|COSMIC]], [[2604.25459|GS-Playground]], [[2604.24018|Sim2Real Betting]], [[2604.17245|MM-Hand]], [[2604.15805|WorldComposer]], [[2604.11768|GC-PFO]], [[2604.11251|CLAW]], [[2604.08544|SIM1]], [[2604.08258|EvoGymCM]], [[2604.07105|Genie Sim PanoRecon]], [[2604.04664|ROSClaw]], [[2602.21992|PanoEnv]], [[2602.10116|SAGE]], [[2601.02778|Force-Based Sim2Real]], [[2511.04665|Real-to-Sim GS]], [[2509.22970|RoLA]], [[2508.12252|Robot Trains Robot]], [[2506.18088|RoboTwin 2.0]], [[2504.04259|ORCA Hand]], [[2503.22122|REMAC]]

> [!star] Key Papers
> - [[2504.04259|ORCA Hand]] — Open-source anthropomorphic hand; bridges the gap between simulation and real dexterous manipulation
> - [[2511.04665|Real-to-Sim GS]] — 3DGS rendering + physics-informed soft-body twins; **Pearson r > 0.9** sim-real correlation across deformable manipulation tasks
> - [[2508.12252|Robot Trains Robot]] — Robotic-arm teacher + 3-stage RL pipeline doubles humanoid walking speed in **20 min** and learns swing-up in **15 min** of real-world training

**Spatial & Scene Understanding** — Understanding 3D scenes, layouts, and spatial relationships as a prerequisite for embodied reasoning.
- [[2606.03374|eMEM]], [[2605.09538|PhysHanDI]], [[2605.02306|NANO Filter]], [[2604.27508|SASI]], [[2604.18484|XEmbodied]], [[2604.12837|GGD-SLAM]], [[2604.11992|ReefMapGS]], [[2604.11320|CLASP]], [[2604.11302|3D-ALP]], [[2604.10982|Psi-Map]], [[2604.08509|Visually-grounded Humanoid Agents]], [[2604.01001|EgoSim]], [[2603.19231|MonoArt]], [[2603.18892|MultihopSpatial]], [[2601.16538|OnlineSI]], [[2512.12822|LEMON]], [[2511.16160|Video2Layout]], [[2511.01294|Kinematify]], [[2507.05258|REA]], [[2505.12707|PLAICraft]], [[2504.12680|Embodied-R]], [[2411.17735|3D-Mem]], [[2410.06468|SPACE]]

> [!star] Key Papers
> - [[2604.18484|XEmbodied]] — VLM with 3D Adapter + Mamba-based Efficient Image-Embodied Adapter; SOTA on 18 embodied benchmarks including 55.28% Ego3DBench and 77.01% DriveLMM-o1

> [!star] Key Papers
> - [[2410.06468|SPACE]] — Benchmark probing whether spatial cognition emerges in frontier models; reveals fundamental gaps in spatial reasoning
> - [[2504.12680|Embodied-R]] — Activates embodied spatial reasoning in foundation models via RL; bridges perception and physical action

**Domain Adaptation** — Transfer policies across visual domains without retraining from scratch.
- [[2604.11386|ComSim]], [[2604.11138|ViserDex]], [[2604.02911|DreamTIP]], [[2602.23253|SPARR]], [[2509.18631|Sim-Real OT Co-Training]], [[2508.21065|Learning on the Fly]], [[2503.18684|OMLA]], [[2503.10949|SCDA]], [[2502.16707|ReflectVLM]], [[2412.02818|RoboMD]], [[2407.13771|Training-Free Model Merging MTDA]]

> [!star] Key Papers
> - [[2602.23253|SPARR]] — Sim-trained base + real-world vision-conditioned residual policy; **95-100%** SR on 10 AutoMate tasks without human supervision; **+38.4%** relative over AutoMate
> - [[2509.18631|Sim-Real OT Co-Training]] — Unbalanced Optimal Transport aligning *joint* observation-action distributions across sim and real; **0.73-0.77** real-world success across modalities
> - [[2508.21065|Learning on the Fly]] — Differentiable simulation + online residual dynamics learning; **81%** hover-error reduction vs L1-MPC, adapts in **4.5 s** wall-time on real quadrotors

> [!tip] Cross-Embodiment Transfer
> The key challenge: policies trained on one robot must work on others. HPT and OXE show that modular architectures + diverse training data are the path.

---

## 8. Datasets, Benchmarks & Simulators

The data and evaluation infrastructure that makes all the above research possible. Datasets provide training signal, benchmarks measure progress, and simulators enable safe, scalable experimentation.

**Large-Scale Cross-Robot Datasets** — Massive datasets spanning multiple robot types and environments.
- [[2503.06669|AgiBot World]], [[2403.12945|DROID]], [[2310.08864|OXE]], [[2307.00595|RH20T]]

> [!star] Key Papers
> - [[2310.08864|OXE]] — Open X-Embodiment: 1M+ trajectories from 22 embodiments; the ImageNet moment for robotics
> - [[2403.12945|DROID]] — In-the-wild data across 16 institutions; proved diverse data beats curated data

**Multi-Modal & Bimanual Datasets** — Datasets with rich sensor modalities (tactile, force) or bimanual manipulation focus.
- [[2605.13083|TouchAnything]], [[2605.09613|SABER]], [[2604.20444|VTouch++]], [[2604.07607|EgoVerse]], [[2604.07335|TAMEn]], [[2603.17851|DexViTac]], [[2512.24653|RoboMIND 2.0]], [[2511.17441|RoboCOIN]], [[2510.25725|HumanoidVTA]], [[2509.00576|G0]], [[2412.13877|RoboMIND]]

> [!star] Key Papers
> - [[2604.20444|VTouch++]] — 120K episodes / 1,000+ hr / 380+ bimanual tasks with fingertip tactile + multi-view RGB-D; contrastive learning lifts cross-modal retrieval by 7×
> - [[2412.13877|RoboMIND]] — Multi-embodiment benchmark with normative manipulation data; standardizes evaluation across robot types
> - [[2512.24653|RoboMIND 2.0]] — Extended to bimanual mobile manipulation; the most comprehensive multi-modal robotics dataset

**Egocentric Human-Video Datasets** — Large-scale first-person video corpora with pose/hand annotations used to pretrain VLAs and learn dexterous priors from humans.
- [[2605.06747|HumanNet]], [[2605.05945|MobileEgo Anywhere]], [[2505.11709|EgoDex]], [[2502.04144|HD-EPIC]], [[2411.19167|HOT3D]], [[2402.13349|Aria Everyday Activities]], [[2203.14712|Assembly101]], [[2110.07058|Ego4D]], [[2006.00626|EGTEA Gaze+]]

> [!star] Key Papers
> - [[2605.06747|HumanNet]] — 1M-hour human-centric video; egocentric + exocentric viewpoints; 1,000 hr pretrain matches/surpasses 100 hr real-robot pretrain
> - [[2110.07058|Ego4D]] — 3,670 hours of egocentric video from 931 wearers across 9 countries; foundational resource for first-person perception and Being-H0/EgoScale-style VLA pretraining
> - [[2505.11709|EgoDex]] — Apple's 829-hour Vision Pro dataset with SE(3) hand/body poses; establishes scaling laws for dexterous manipulation

**Benchmarks — Simulation** — Standardized simulation environments for reproducible evaluation.
- [[2605.06311|VISER]], [[2604.11674|AffordSim]], [[2603.15469|RoCo Challenge]], [[2603.12185|ComFree-Sim]], [[2602.22663|CEBench]], [[2511.04831|Isaac Lab]], [[2510.13626|LIBERO-Plus]], [[2506.06677|RoboCerebra]], [[2502.09560|EmbodiedBench]], [[2408.15511|AeroVerse]], [[2406.02523|RoboCasa]], [[2405.05941|SIMPLER]], [[2306.03310|LIBERO]], [[2112.03227|CALVIN]], [[1909.12271|RLBench]]

> [!star] Key Papers
> - [[2306.03310|LIBERO]] — Lifelong robot learning benchmark; tests continual learning and long-horizon capability
> - [[2405.05941|SIMPLER]] — Bridges sim and real; evaluates whether simulation performance predicts real-world success

**Benchmarks — Diagnostic** — Targeted benchmarks that expose specific failure modes.
- [[2605.10921|RoboMemArena]], [[2604.21686|WorldMark]], [[2604.11689|LARY]], [[2604.05498|JailWAM]], [[2603.23497|WildWorld]], [[2603.22435|CaP-X]], [[2603.22212|Omni-WorldBench]], [[2603.13966|vla-eval]], [[2603.04639|RoboMME]], [[2602.22579|VLA Metamorphic Testing]], [[2602.08971|WorldArena]], [[2602.06556|LIBERO-X]], [[2602.05986|RISE-Video]], [[2602.01640|A2Eval]], [[2601.15224|PROGRESSLM]], [[2601.11421|GM-100]], [[2601.09430|Video-MSR]], [[2512.01989|PAI-Bench]], [[2511.12149|AttackVLA]], [[2511.04670|Cambrian-S]], [[2510.17801|Robobench]], [[2510.03827|LIBERO-PRO]], [[2509.18953|Eva-VLA]], [[2509.17057|RoboManipBaselines]], [[2509.15273|Embodied Arena]], [[2508.13142|EASI]], [[2508.12211|VLAPS]], [[2507.18342|EgoExoBench]], [[2507.10548|EmbRACE-3K]], [[2506.18123|RoboArena]], [[2506.18088|RoboTwin 2.0]], [[2505.19017|WorldEval]], [[2505.15660|AGNOSTOS]], [[2505.09694|EWMBench]], [[2503.23765|STI-Bench]], [[2501.16411|PhysBench]], [[2305.12821|FurnitureBench]], [[2206.09682|SafeBench]], [[2009.12293|robosuite]]

> [!star] Key Papers
> - [[2506.18123|RoboArena]] — Distributed real-world VLA eval via crowd-sourced pairwise comparisons; 0.98 Pearson correlation with oracle, paradigm shift from sim-only benchmarking
> - [[2601.11421|GM-100]] — 100 detail-oriented tasks; current VLAs achieve very low success rates, exposing real capability gaps

**Surveys:**
- [[2605.05017|SPINE]] — Position paper: embodied AI requires a privacy-utility trade-off as life-cycle architectural constraint, not localized patches
- [[2604.15395|Foundation Models in Robotics Survey]] — 435 articles across 6-criteria taxonomy; maps 5 evolutionary phases of FMs in robotics
- [[2601.07823|Video Generation in Robotics Survey]] — Systematic review of generative video models as embodied world models for imitation learning, RL, policy evaluation, and visual planning; enumerates 10 challenges including physics violations and uncertainty quantification
- [[2506.20966|VLA Post-Training Survey]] — Reviews 129 VLA post-training studies; taxonomy mirrors human motor learning (Newell's constraints-led theory) across environmental perception, embodiment awareness, task comprehension; LIBERO success climbs from 75% to 98% over 16 months
- [[2507.00917|Embodied Intelligence Survey]] — 2018-2025 review on physical simulators and world models; proposes IR-L0 to IR-L4 robot intelligence grading
- [[2212.14020|System-Level OOD Robotics]] — Stanford framework for out-of-distribution data in robotics: distinguishes distributional shifts from functional uncertainty, organizes 6 research questions across real-time / episodic / data-lifecycle timescales
- [[2505.07634|Neural Brain Framework]] — neuroscience-inspired framework for embodied agents; defines 4 core components for human-like adaptability
- [[2505.05108|Multi-agent Embodied AI Survey]] — first systematic survey of multi-agent embodied AI
- [[2509.20021|Embodied AI LLM-WM Survey]] — joint MLLM-WM architecture roadmap
- [[2506.21872|Continual RL Survey]] — lifelong learning in RL for sequential tasks
- [[2505.04769|VLA Concepts Survey]] — updated VLA landscape review
- [[2504.15037|MLLM Spatial Reasoning Position Paper]] — spatial reasoning in MLLMs requires new recipes
- [[2504.09848|LLM Spatial Intelligence Survey]] — LLM-powered spatial intelligence across scales
- [[2502.02133|MPC-RL Survey]] — MPC + RL synthesis for robotic control
- [[2501.02765|VLLM Survey]] — visual LLMs for generalized/specialized applications
- [[2409.15310|Visual Prompting MLLM Survey]] — visual prompting methods for MLLMs
- [[2407.06886|ARIO]] — comprehensive survey with ARIO dataset standard
- [[2405.14093|VLA for Embodied AI Survey]] — survey of VLA models for embodied AI
- [[2401.03568|Agent AI Survey]] — surveys Agent AI at the intersection of LLMs/VLMs and multimodal interaction
- [[2301.11972|Social Cues HRI Survey]] — recognizing robot task failures via human social cues
- [[2103.04918|Embodied AI Survey]] — simulators and research tasks

> [!tip] The Dataset Hierarchy
> Start with simulation (RLBench, CALVIN) → scale with in-the-wild data (DROID, OXE) → diagnose with targeted benchmarks (GM-100, LIBERO-Plus).


---

## Cross-References

- [[11_Self-Evolving-AI]] — Broader self-evolving paradigm
- [[04_Reinforcement-Learning]] — RL as the training backbone
- [[06_Video-and-Temporal]] — Video generation as world modeling

---

*Next: [[08_Benchmarks-and-Surveys]] for a cross-cutting view of evaluation resources.*