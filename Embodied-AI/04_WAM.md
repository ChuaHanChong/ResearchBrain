---
title: "World Action Models — Deep Dive"
tags:
  - world-model
  - robotics
  - VLA
  - diffusion
  - JEPA
aliases:
  - "WAM Deep Dive"
  - "WAM Survey"
---

# World Action Models — Deep Dive

> [!abstract] Overview
> World Action Models (WAMs) learn to predict future states of the environment, giving robots the ability to "imagine" consequences before acting. Unlike VLAs that map observations directly to actions, WAMs explicitly model dynamics — enabling planning, robustness to perturbation, and sample-efficient learning. This note maps the full WAM landscape across five paradigms: VideoGen, latent prediction (JEPA family), model-based RL ([[1912.01603|Dreamer]] lineage), VLM-integrated, and efficient/action-centered designs.

## Evolution Graph

```mermaid
graph TD
    subgraph "Model-Based RL (2019-2026)"
        A["Dreamer<br/><i>2019</i>"]
        B["DreamerV3<br/><i>2023</i>"]
        C["Dreamer 4<br/><i>2026</i>"]
    end

    subgraph "Video Generation (2023-2026)"
        D["UniPi<br/><i>2023</i>"]
        E["UniSim<br/><i>2023</i>"]
        F["Cosmos Policy<br/><i>2025</i>"]
        G["DreamZero<br/><i>2026</i>"]
    end

    subgraph "Latent Prediction (2023-2026)"
        H["I-JEPA<br/><i>2023</i>"]
        I["V-JEPA 2<br/><i>2025</i>"]
        J["VLA-JEPA<br/><i>2026</i>"]
    end

    subgraph "VLM-Integrated (2025-2026)"
        K["VLAW<br/><i>2026</i>"]
        L["Fast-WAM<br/><i>2026</i>"]
    end

    subgraph "Physics-Aware (2025-2026)"
        N["NewtonGen<br/><i>2025</i>"]
        O["PhysCtrl<br/><i>2025</i>"]
        P["PhysWorld<br/><i>2025</i>"]
    end

    A --> B --> C
    D --> F --> G
    E --> F
    H --> I --> J
    J --> K
    G --> L
    F --> N
    N --> O
    O --> P

    style A fill:#e8f4fd,stroke:#4a90d9
    style B fill:#e8f4fd,stroke:#4a90d9
    style G fill:#f0e8fd,stroke:#9b59b6
    style J fill:#f0e8fd,stroke:#9b59b6
    style K fill:#e8fde8,stroke:#27ae60
    style L fill:#e8fde8,stroke:#27ae60
    style N fill:#fde8f4,stroke:#d94a90
    style O fill:#fde8f4,stroke:#d94a90
    style P fill:#fde8f4,stroke:#d94a90
```

The field evolved through four threads: **model-based RL** (2019-2026) where [[1912.01603|Dreamer]] established latent imagination for planning; **video generation** (2023-2026) where diffusion models learned physics from internet video; **latent prediction** (2023-2026) where JEPA showed you can predict in representation space without reconstructing pixels; and **VLM integration** (2025-2026) where world models merged with VLAs for robust, efficient policies.

| Year | Paper | Contribution |
|------|-------|-------------|
| 2019 | [[1912.01603\|Dreamer]] | Latent imagination via RSSM; learned behaviors from pixels without reward |
| 2023 | [[2301.04104\|DreamerV3]] | Mastered diverse domains with fixed hyperparameters; universal model-based RL |
| 2023 | [[2302.00111\|UniPi]] | Actions as text-conditioned video; proved video generation = planning |
| 2023 | [[2310.06114\|UniSim]] | Universal simulator via video diffusion; interactive world generation |
| 2023 | [[2301.08243\|I-JEPA]] | Predict in latent space, not pixel space; avoids reconstruction artifacts |
| 2025 | [[2506.09985\|V-JEPA 2]] | Self-supervised video model enabling understanding, prediction, and planning |
| 2025 | [[2601.16163\|Cosmos Policy]] | Fine-tuned video diffusion model as visuomotor policy |
| 2026 | [[2602.15922\|DreamZero]] | 14B WAM: joint video + action prediction enables zero-shot policies |
| 2026 | [[2602.10098\|VLA-JEPA]] | JEPA world model + flow-matching action head; 97.2% [[2306.03310\|LIBERO]] |
| 2026 | [[2602.12063\|VLAW]] | Iterative co-improvement: VLA and world model reinforce each other |
| 2026 | [[2509.24527\|Dreamer 4]] | Scalable world model training agents inside video game environments |
| 2026 | [[2603.16666\|Fast-WAM]] | WAM benefits without test-time imagination via video co-training |
| 2026 | [[2605.15153\|Pelican-Unified]] | Single-model unification of understanding + reasoning + imagination + action via shared latent z + UFG |
| 2026 | [[2605.12090\|WAM Survey]] | First formal WAM definition; Cascaded vs Joint architectural taxonomy; four-data-ecosystem analysis |
| 2026 | [[2605.10942\|HarmoWAM]] | Dual predictive+reactive experts + process-adaptive gating resolve generalization-precision trade-off |
| 2025 | [[2509.21309\|NewtonGen]] | Physics-consistent T2V via neural Newtonian dynamics |
| 2025 | [[2509.20358\|PhysCtrl]] | Generative physics for controllable video generation |
| 2025 | [[2511.07416\|PhysWorld]] | Robot learning from a physical world model |
| 2026 | [[2603.13770\|PhysAlign]] | Feature + 3D-representation alignment for physics-coherent video |
| 2026 | [[2603.26285\|PhysVid]] | Physics-aware local conditioning for generative video |

---

## Part A — Design Space

*The dimensions every WAM choice sits on: where to predict, when to predict, how to condition.*

### 1. The Design Space

> [!star] WAM Definition & Cascaded vs Joint Taxonomy
> [[2605.12090|WAM Survey]] is the first paper to formally define WAMs and disambiguate them from VLAs (no dynamics model) and pure World Models (no action generation). It splits the architectural landscape along a single axis — ==Cascaded== (sequential: predict next state, then derive action) vs ==Joint== (unified state-action prediction) — and surveys four data-ecosystem axes (robot, human, simulation, internet-scale video) plus emerging evaluation protocols. The Cascaded/Joint distinction is the field-defining taxonomy that subsequent sections of this note implicitly use.

Three axes define where a WAM sits in the design landscape:

| Axis | Options | Trade-off |
|------|---------|-----------|
| **Where to predict** | Pixel space ([[2602.15922\|DreamZero]]), Latent space (JEPA, [[2504.02792\|UWM]]), Action space ([[2205.09991\|Diffuser]]) | Pixel = rich but slow; Latent = fast but abstract; Action = efficient but no visual feedback |
| **When to predict** | Training-time only ([[2603.16666\|Fast-WAM]]), Test-time imagination ([[2602.15922\|DreamZero]]) | Training-time = fast inference; Test-time = more robust but 4.8x slower |
| **What to predict** | Full video (Cosmos), Optical flow ([[2508.18269\|FlowVLA]]), Compressed latent ([[2602.22010\|WoG]]), Future embeddings (JEPA) | Full video = interpretable but expensive; Latent = efficient but opaque |

**Where to predict** determines computational cost and expressiveness. Pixel-space prediction ([[2602.15922|DreamZero]]'s 14B DiT) generates full video frames — maximally expressive but requires iterative denoising (~150ms per frame). Latent-space prediction ([[2602.10098|VLA-JEPA]]'s V-JEPA2 predictor) operates on compressed embeddings — a single forward pass (~10ms) but loses fine visual detail. Action-space prediction ([[2205.09991|Diffuser]]) skips visual prediction entirely — fastest but provides no visual feedback for planning or debugging.

**When to predict** is the 2026 insight from [[2603.16666|Fast-WAM]]: you need video generation at training time (to learn spatiotemporal priors from internet video) but NOT at test time (where it adds 4.8x latency). The world model's value is in the representations it creates during training, not in the predictions it makes during deployment.

**What to predict** trades off between interpretability and efficiency. Full video (Cosmos) is human-readable but expensive. Optical flow ([[2508.18269|FlowVLA]]) captures motion efficiently. Future embeddings (JEPA) are opaque but compact. The choice depends on whether a human needs to inspect the predictions (development/debugging) or only the policy needs them (deployment).

**Design Space — Decision Matrix**

| If you need... | Reach for... |
|---|---|
| Maximum physics priors + interpretable rollouts | Pixel-space VideoGen (§2) — [[2602.15922\|DreamZero]] (slow but robust) |
| Real-time latent prediction (~10ms/step) | Latent prediction (§3) — JEPA / [[2504.02792\|UWM]] |
| WAM robustness *without* test-time latency | Training-time-only video co-training — [[2603.16666\|Fast-WAM]] |
| Efficient motion signal, no full frames | Compact prediction — optical flow ([[2508.18269\|FlowVLA]]), latent ([[2602.22010\|WoG]]) |
| Pure planning with no visual feedback | Action-space prediction — [[2205.09991\|Diffuser]] |
| Formal cascaded-vs-joint placement | [[2605.12090\|WAM Survey]] taxonomy |

> [!tip] The Core Trade-off
> VideoGen WAMs are the most robust (spatiotemporal priors from internet video) but the slowest. Latent prediction WAMs are fast and sample-efficient. [[2603.16666|Fast-WAM]] shows you can bridge this gap: train with video generation objectives but deploy without test-time imagination.

---

## Part B — WAM Paradigms

*Five architectural families: VideoGen, latent prediction, Dreamer/RSSM, VLM-integrated, efficient/action-centered.*

### 2. VideoGen WAMs

Video diffusion models repurposed as world simulators. The richest source of physics priors — trained on internet-scale video data.

#### 2.1 Planning as Video Generation

The foundational insight: generating a video of the future IS a plan. Condition the diffusion model on the current observation and a language instruction, then denoise to produce a future video; an inverse dynamics model extracts the motor commands. This axis defines *what the WAM outputs* — a goal video, not actions directly.

- **[[2310.06114|UniSim]]** — ==5.6B-parameter video diffusion== + ==dataset orchestration== unifying robotic + human + panorama + internet data + ==T5-embedded unified action space==; zero-shot sim-to-real **3–4× better** goal reduction; captioning fine-tune CIDEr **15.2 → 46.23** — first interactive world generator covering both human + robot agents.
- **[[2302.00111|UniPi]]** — ==Unified Predictive Decision Process== formulation casting policy as text-conditioned video generation + ==task-specific inverse dynamics model==; **60.1%** vs **12.5%** baselines on novel "Place" tasks, **51.6%** vs **14.8%** unseen CLIPort "Place Bowl"; internet-video pretrain lifts real robots **72.6% → 77.1%** — defined the *"video is the plan"* formulation.
- **[[2310.10625|VLP]]** — ==Parallel hill-climbing tree search== with VLM as policy+heuristic + ==text-to-video dynamic simulator== + ==goal-conditioned receding-horizon execution==; **98%** Group-Color synthesis (vs **2–64%** baselines), **92%** robot execution (vs **0–4%** baselines), validated on 7-DoF + 14-DoF bimanual.

#### 2.2 Video Pretraining for Robot Policies

Train a video-prediction backbone on internet-scale video, then fine-tune with action heads. The video objective gives spatiotemporal priors that pure action-imitation cannot match.

- **[[2606.04463|OSCAR]]** — ==Skeleton-conditioned omni-embodiment WAM== finetuning a **2B** Cosmos-Predict2.5 ==Diffusion Transformer== on ==2D kinematic skeleton rendering==; **FVD 7.08 / FID 15.07 / PSNR 24.24** beating seven larger baselines, and virtual policy eval correlates with real RoboArena rankings at **Pearson r +0.852** (mean SR error **1.73 pp**).
- **[[2606.01955|WALL-WM]]** — ==Layer-coupled video-action denoiser== shifting the atomic learning unit from action chunks to ==semantically coherent action events==; embodied video-gen Motion Quality **0.771** (vs **0.683**), Semantic Alignment **0.886** (vs **0.805**), real-robot Task Progress **75.86** / **71.60** / **53.75** beating DreamZero.
- **[[2606.03159|OmniDreams]]** — ==Autoregressive action-conditioned generative world model== on a causal ==transformer== for real-time closed-loop AV simulation, conditioned on past frames + text + abstract scenario maps; **68 FPS** single-camera / **105 FPS** four-camera on GB300, **FVD 24.8** with driving-semantic preservation (3D-vehicle LET-AP **0.400**, lane-line F1 **0.828**).
- **[[2605.15178|SANA-WM]]** — **2.6B** open-source ==Hybrid Linear Diffusion Transformer== generating ==one-minute 720p videos== with precise 6-DoF camera control on a single GPU. Frame-wise ==Gated DeltaNet== fused with ==softmax attention==; key-scaling $1/\sqrt{D \cdot S}$ prevents minute-scale state explosion. VBench Overall **80.62/81.89** matching 480p/8-GPU baselines; **22 videos/hour** on H100, **39x** distilled speedup on RTX 5090 — first open-source minute-scale 720p WAM.
- **[[2605.06192|EA-WM]]** — ==Kinematic-to-Visual Action Fields (KVAFs)== projecting 3D robot geometry to camera plane + ==Event-Aware Bidirectional Fusion (EAF)== in DiT + ==Event-Difference Latent Supervision==; **P3CScore 76.60** on WorldArena (+5.52 over CogVideoX); ablations confirm KVAFs (-5.63) + EAF (-1.80) load-bearing.
- **[[2604.06168|Action Images]]** — Encodes 7-DoF actions as ==multi-view 2D Gaussian heatmap action images== of EE-position/up/normal + unified video-action joint training with diverse masking; zero-shot **60%** RLBench reach-target + **45%** real-world close-drawer (vs **0–20%** baselines); PSNR **23.48** vs **20.83** TesserAct.
- **[[2602.15922|DreamZero]]** — **14B** joint video+action model; **39.5%** on unseen tasks, **42%** cross-embodiment improvement, **7Hz** real-time; defines the robustness ceiling for VideoGen WAMs.
- **[[2602.12099|GigaBrain-0.5M*]]** — ==RAMP== (Reinforcement learning via world-Model-conditioned Policy) + ==self-improving closed loop== with ==Human-in-the-Loop Rollout== + continual joint VLA/WM training; **100%** Juice-Preparation, +30pp over RECAP on Box-Packing/Espresso, intermediate GigaBrain-0.1 tops RoboChallenge at **51.67%**.
- **[[2601.16163|Cosmos Policy]]** — fine-tuned Cosmos video diffusion as visuomotor policy; **98.5%** on [[2306.03310|LIBERO]]; the cleanest demonstration that pretrained video diffusion transfers to robot control.
- **[[2601.21998|LingBot-VA]]** — ==Autoregressive diffusion== unifying video+action tokens in shared continuous latent + ==Mixture-of-Transformers== + ==closed-loop rollout with KV-caching== + ==asynchronous FDM-grounded inference==; **92.9%** RoboTwin 2.0 Easy / **91.6%** Hard, **98.5%** LIBERO avg.
- **[[2511.07732|ViPRA]]** — ==Three-stage pipeline==: latent action learning from actionless videos → multimodal pretraining with video-language model → continuous adaptation via ==flow matching decoder + action chunking==; **69.8%** SIMPLER discrete, **62.5%** continuous, **79%** LIBERO Long, **54.1%** real single-arm at up to **22 Hz**.
- **[[2508.00795|Video Policy]]** — ==Modular Video U-Net + Action U-Net== with action prediction conditioned on intermediate hidden embeddings + ==two-stage training== with gradient stopping; SOTA RoboCasa + Libero10 with only **50** demos/task; robust to unseen objects + backgrounds in real-world.
- **[[2505.15659|FLARE]]** — ==Future Latent Representation Alignment== predicts compact future state representations (not pixels) + ==action-aware observation embedding== + diffusion transformer + ==co-training with action-free human videos==; up to **+26%** over baselines, **95%** real-world with only **100** trajectories/task.
- **[[2412.14803|VPP]]** — Fine-tuned ==Stable Video Diffusion text-guided video predictor== used as ==frozen predictive visual encoder== (single forward pass) + ==Video Former== feature condensation + Diffusion Policy head; CALVIN ABC→D avg length **4.33** (**+41.5%** over GR-1), **0.682** MetaWorld-50, **0.73** Franka unseen / **0.68** dex hand.
- **[[2410.06158|GR-2]]** — ==GPT-style transformer== with ==video-language pretrain on 38M clips== + fine-tune with ==cVAE== for diverse action trajectories; **97.7%** multi-task tabletop, **75%** at **50 demos**, **79.0%** industrial bin-picking (vs **35.9%** GR-1), **98.6%** + length **4.64** on CALVIN.
- **[[2312.13139|GR-1]]** — ==Decoder-only GPT-style transformer== with ==CLIP+MAE encoders== + ==[ACT]/[OBS] tokens== pretrained on **800K** Ego4D clips; **94.9%** CALVIN multi-task (vs **88.9%** HULC), **85.4%** unseen-scene zero-shot (vs **53.3%**), **77.8%** with only **10%** data — pioneered the video-prediction backbone + action-decoder pattern.

#### 2.3 Video Models as Data Engines

Use generated video as synthetic training data offline, rather than running the world model at test time. Decouples WAM benefits from inference latency.

- **[[2606.02577|RoboDream]]** — ==Compositional video-diffusion data engine== that ==decouples robot motion from visual context== for zero-shot novel-object/scene/viewpoint synthesis; Gen-Mix policies reach **62.5%** avg vs Real-50 **36.3%** and raw-retrieved **0%**, and prop-free collection runs **2.2×** faster than real teleoperation.
- **[[2512.24766|Dream2Flow]]** — Off-the-shelf ==image-to-video gen== → ==3D object flow== (depth + segmentation + 2D point tracking + lifted to 3D) → ==optimization-based action inference== (particle dynamics / rigid-grasp / RL); up to **8/10** real-world success on Put-Bread-in-Bowl + Open-Oven across rigid/articulated/deformable/granular objects.
- **[[2512.13644|DexWM]]** — ==Conditional Diffusion Transformer== on frozen DINOv2 + ==3D hand-keypoint difference action repr== + ==Hand Consistency Loss==; pretrained on EgoDex → MPC planning; **83%** zero-shot real-world Franka+Allegro grasping with **0** real-world training data; Reach **72%** / Grasp **58%** vs Diffusion Policy **16% / 0%**.
- **[[2505.12705|DreamGen]]** — ==4-stage pipeline==: fine-tune image-to-video → roll out synthetic videos → IDM/LAPA pseudo-actions → train policies; scales data **333×**; GR1 humanoid **37% → 46.4%**, Franka **23% → 37%**; generalizes to **22** novel behaviors (**43.2%** vs **11.2%**) + **10** unseen environments (**28.5%** vs **0%**).
- **[[2504.15369|Inverse Probabilistic Adaptation]]** — ==Inverse Probabilistic Adaptation==: freeze pretrained T2V + subtract score of small "distractor" model trained on irrelevant content; up to **3×** task-success improvement; ==Subject Customization== with only static images is highly data-efficient.

#### 2.4 Physics-Aligned Video Generation

Explicitly enforce physical plausibility during video generation. See [[07_Physics-Aware-Embodied-AI#3. Explicit Physics Losses for Video Generation]] for the full physics-aware design space (implicit/explicit/external-simulator approaches).

- **[[2604.13036|Lyra 2.0]]** — ==Autoregressive retrieve–generate–update loop== with ==incremental 3D cache + geometry-aware retrieval== + ==self-augmentation== anti-drift training + ==DAv3 reconstruction fine-tune== for generative artifacts; outperforms baselines on SSIM/LPIPS/FID + distilled model achieves **13× speedup** (4 vs 35 denoising steps).
- **[[2604.07348|MoRight]]** — ==Dual-stream DiT== with canonical (object) + target (final) streams + ==active/passive motion decomposition== + ==motion dropout==; **53.5%** controllability + **54.6%** motion realism + **55.9%** photorealism human-preference; best FID/FVD on WISA + Cooking; supports forward+inverse causal reasoning from sparse inputs.
- **[[2604.07209|INSPATIO-WORLD]]** — ==Spatiotemporal Autoregressive (STAR)== with implicit spatiotemporal cache + ==position-index fixing + chunk-wise BP== + ==Joint Distribution Matching Distillation== + multi-condition causal init; **24 FPS** real-time on H-series, **42.68 FID / 100.55 FVD** long-term I2V with Rotation Error **2.8762** — only open-source real-time solution.
- **[[2603.26285|PhysVid]]** — ==Chunk-aware cross-attention== with Rotary Position Embeddings + VLM-generated physics-grounded local prompts + ==counterfactual classifier-free guidance==; **PC 0.32** on VideoPhy (+33% rel. over Wan-14B at **1.7B** vs **14B** params), **PC 0.64** on VideoPhy2 (vs **0.59** Wan-14B).
- **[[2603.23376|ABot-PhysWorld]]** — ==Diffusion-DPO== for physics alignment; suppresses implausible predictions (object penetration, anti-gravity). The DPO-on-physics-preference-pairs recipe. **0.8491** PBench average (SOTA Domain Score **0.9306**); SOTA zero-shot generalization on EZSbench (**0.8030**); action-conditioned PSNR **21.09** / nDTW **0.8522** for gripper-trajectory adherence.
- **[[2603.13770|PhysAlign]]** — ==LoRA adapter== on DiT I2V models + ==dual latent alignment== (Gram-based spatio-temporal alignment with V-JEPA2 teacher + 3D-convolution depth head) + Blender synthetic 3K-video dataset; **PIS a_x 0.632** vs **0.520** Wan2.2, VBench i2v subject **0.911** + motion smoothness **0.996**.
- **[[2602.05986|RISE-Video]]** — ==RISE-Video== with **467 human-annotated samples** across 8 reasoning categories + ==4-dim eval== (Reasoning Alignment / Temporal Consistency / Physical Rationality / Visual Quality); best TI2V Hailuo 2.3 only **22.5%** across 11 models — explicit potential-energy terms only marginally help on logical reasoning.
- **[[2511.07416|PhysWorld]]** — ==Task-conditioned video gen== → ==4D digital twin== reconstruction (geometry-aligned 4D + textured-mesh generative priors + physical-property estimation) + ==object-centric residual RL==; **82%** real-world avg across **10** tasks (+15pp over RIGVid), grasping failures **18% → 3%**.
- **[[2509.21309|NewtonGen]]** — physics-consistent T2V via ==neural Newtonian dynamics==; explicit physics constraints during generation. Physical Invariance Score **0.9830** (Uniform Motion) vs Sora's **0.6548** across **12** motion types; faithful trajectory/velocity controllability, and the ==residual-MLP NND== learns from as few as **100** physics-clean videos.
- **[[2509.20358|PhysCtrl]]** — Two-stage ==image → 3D point cloud → physics-grounded 3D point trajectories via diffusion-based generative physics network== with ==spatio-temporal attention + diffusion/velocity/physics/boundary losses==; trained on **550K** object animations; GPT-4o eval **4.5** semantic/physical commonsense + **4.3** video quality; vIoU **77.59%**, Chamfer **0.0028**.
- **[[2503.15558|Cosmos-Reason1]]** — ==Hybrid Mamba-MLP-Transformer== (56B) MLLMs with ==two-stage SFT → RL with verifiable rule-based rewards==; **60.2%** physical-commonsense + **63.7%** embodied-reasoning (56B); 7B variant **81.5%** intuitive physics after RL (+32.4pp over backbone).
- **[[2409.18964|PhysGen]]** — ==Perception (GPT-4V + Grounded-SAM)== → ==rigid-body physics simulation== → ==generative refinement via video diffusion==; training-free perception-simulation-rendering pipeline; outperforms data-driven I2V baselines on physical realism + photorealism in human studies.

**VideoGen — Decision Matrix**

| Need | Approach |
|---|---|
| Zero-shot novel-task generation (cross-embodiment) | [[2602.15922\|DreamZero]] (Planning as Video Generation; **39.5%** unseen tasks) |
| Internet-video pretraining + action decoder | [[2410.06158\|GR-2]] / [[2312.13139\|GR-1]] |
| Synthetic robot training data (offline) | [[2505.12705\|DreamGen]] / [[2512.13644\|DexWM]] / [[2512.24766\|Dream2Flow]] |
| Physics-aligned video (suppress hallucinations) | [[2603.23376\|ABot-PhysWorld]] / [[2509.21309\|NewtonGen]] |
| Minute-scale 720p video on single GPU | [[2605.15178\|SANA-WM]] (**22 videos/hour**, **39×** distilled speedup) |
| Pretrained-Cosmos fine-tune (clean LIBERO baseline) | [[2601.16163\|Cosmos Policy]] (**98.5%** LIBERO) |
| Foundational learned-sim baseline | [[2310.06114\|UniSim]] |

> [!star] Key Papers
> - [[2602.15922|DreamZero]] — **14B** joint video+action; **39.5%** unseen tasks, **42%** cross-embodiment, **7Hz** real-time; the robustness ceiling for VideoGen WAMs
> - [[2605.15178|SANA-WM]] — First viable open-source minute-scale 720p WAM; **22 videos/hour** on H100, **39×** distilled speedup
> - [[2601.16163|Cosmos Policy]] — Fine-tuned Cosmos video model hits **98.5%** [[2306.03310|LIBERO]]; the cleanest proof pretrained video diffusion transfers to control
> - [[2603.23376|ABot-PhysWorld]] — Diffusion-DPO for physics alignment; the reference recipe for suppressing object-penetration / anti-gravity hallucinations
> - [[2509.21309|NewtonGen]] — Physics-consistent T2V via neural Newtonian dynamics; explicit physics constraints during generation (Physical Invariance **0.9830** vs Sora's **0.6548**)

> [!tip] Video Generation = Physics Engine
> Video diffusion models trained on internet data implicitly learn physics. [[2602.15922|DreamZero]] proved joint video+action generation provides spatiotemporal priors that pure VLAs lack. But test-time video generation is expensive — consider [[2603.16666|Fast-WAM]]'s training-only approach. For an explicit physics-priors view, see [[07_Physics-Aware-Embodied-AI#3. Explicit Physics Losses for Video Generation]]; for the egocentric pretraining substrate these models reuse, see [[09_Egocentric-Pretraining-and-Human-Video#6. Egocentric Pretraining Meets WAMs]].

---

### 3. Latent Prediction WAMs

Predict in representation space rather than pixel space — faster, more abstract, and avoids wasting capacity on irrelevant visual details. See [[05_Latent-World-Models#2. JEPA Evolution: Visual-Only → Dense → Vision-Language → Vision-Language-Action]] for the detailed JEPA evolution.

#### 3.1 JEPA Family

Joint Embedding Predictive Architecture: predict future embeddings from current embeddings rather than reconstructing pixels. The compressed-prediction axis is what makes latent WAMs ~10ms/step vs ~150ms for VideoGen.

- **[[2603.22281|ThinkJEPA]]** — ==VLM "thinker" branch== with ==dual-temporal perception== (dense for JEPA + sparse for VLM) + ==hierarchical pyramid feature extraction== injected via ==FiLM==; **ADE 0.061 / FDE 0.056** on EgoDex (vs **6** trajectory baselines), maintains best stability at H=**32** recursive rollout.
- **[[2603.19312|LeWM]]** — ==Two-term objective== (MSE + ==Sketched-Isotropic-Gaussian Regularizer==) on ViT-Tiny + Transformer with AdaLN end-to-end (no stop-grad/EMA); **+18%** SR on Push-T over PLDM, **48× faster** planning (<1 s/cycle); emergent temporal-latent-path straightening.
- **[[2603.14482|V-JEPA 2.1]]** — ==Dense Predictive Loss== on masked + unmasked tokens + ==Deep Self-Supervision== + ==modality-specific tokenizers== on VisionMix-163M up to ViT-G; SOTA **7.71 mAP** Ego4D short-term anticipation (+35% rel.), **+20%** robotic arm grasp, **10×** faster nav planning, **RMSE 0.307** NYUv2 depth.
- **[[2602.11832|JEPA-VLA]]** — Integrates ==V-JEPA 2== into VLA via ==Early Fusion== (scratch) or ==Gated Fusion== (pretrained); **+7.4pp** LIBERO + **+6.7pp** LIBERO-Plus, **100%** real pick-place under layout/lighting shifts, **+15.2pp** LIBERO-Long over DINOv2/SigLIP; one-fifth data beats full-data baseline.
- **[[2602.11389|Causal-JEPA]]** — object-centric world model with causal reasoning via ==latent interventions==; supports counterfactual queries.
- **[[2602.10098|VLA-JEPA]]** — full VLA + JEPA pipeline: **97.2%** [[2306.03310|LIBERO]] in-distribution, **79.5%** [[2510.13626|LIBERO-Plus]] OOD, **65.2%** SimplerEnv real robot; defines the speed-quality Pareto frontier.
- **[[2512.10942|VL-JEPA]]** — ==4-component JEPA== (visual X-encoder + query-conditioned predictor + text Y-encoder + inference-only Y-decoder) + ==InfoNCE latent prediction loss==; **46.4%** avg on 8 video classification, **58.4%** R@1 on 8 text-video retrieval; **1.6B** SFT variant matches established VLMs; **~2.85×** fewer decoding ops via selective decoding.
- **[[2511.19221|Percept-WAM]]** — ==World-Awareness-Action== framework with World-PV (2D) + World-BEV (3D) tokens + ==grid-conditioned dense perception== + ==IoU-aware scoring== + parallel AR decoding + streaming inference; **51.7 mAP** COCO + **0.589 mAP** nuScenes BEV + **0.36 m** L2 nuScenes planning + **90.2 PMDS** NAVSIM at **+40%** inference speedup.
- **[[2510.00739|TD-JEPA]]** — ==Temporal-Difference JEPA== with asymmetric state φ + task ψ encoders + TD-based loss + ==zero-shot policies parameterized by task embeddings==; matches/outperforms SOTA across **65 tasks / 13 datasets** in ExoRL + OGBench, especially strong on pixel-based observations.
- **[[2506.09985|V-JEPA 2]]** — **1M+ hours** of video pretraining; **80%** pick-and-place with **62 hours** of unlabeled robot video; the canonical scale anchor for the JEPA family.
- **[[2605.15618|V-JEPA Robustness Study]]** — Matched-capacity ==ViT-Large== head-to-head of **V-JEPA 2.1 / V-JEPA 2 / VideoPrism / VideoMAEv2** across **5 robustness axes** (discriminability, corruption, fine-grained action, occlusion, temporal); latent-prediction JEPAs dominate pixel-reconstruction + contrastive baselines, and **frozen V-JEPA 2 outperforms task-adapted fine-tuned** VideoMAE/TimeSformer — the first capacity-matched empirical justification for latent-space prediction.

#### 3.2 Unified Latent Diffusion

Shared diffusion transformer for both video and action in a *common* latent space. Couples generation and control under one objective.

- **[[2606.04907|WAM-Nav]]** — ==Asymmetric latent world-action model== jointly modeling action trajectories + short-horizon ==latent visual foresight== in a shared ==Diffusion Transformer==; **+15.7%** SR over NavDP on Image-Goal (**50.2%** SR / **48.2%** SPL), **0.26 s** latency at **0.7 TFLOPs/decision**, and **85%** real-world SR zero-shot on a Unitree G1.
- **[[2605.06388|Semantic-LDM-WM]]** — first systematic head-to-head of reconstruction- vs semantic-aligned latents in action-conditioned LDMs; semantic latents ([[2603.14482|V-JEPA 2.1]], [[2502.14786|SigLIP 2]], Web-DINO) yield **+9.8 pp** VLA closed-loop success and **+13.6 pp** OOD robustness over reconstruction VAEs.
- **[[2512.13030|Motus]]** — ==Mixture-of-Transformer== unifying VLM + Video Gen + Action Expert via ==Tri-model Joint Attention== + ==optical-flow-derived latent actions== compressed by VAE; **88.66%** RoboTwin 2.0 Clean / **87.02%** Random (+45% over π0.5, +15% over X-VLA); +48.43pp on AC-One bimanual real-world.
- **[[2505.11528|LaDi-WM]]** — ==Latent diffusion WM== on concatenated DINOv2 (geometry) + Siglip (semantic) latents + ==interactive diffusion with cross-attention== + ==Imagination-Guided iterative action refinement==; **68.7%** LIBERO-LONG with 10 demos (+15.1pp over SOTA), **90.7%** full data; +20pp real-world over BC.
- **[[2504.02792|UWM]]** — ==Unified video + action diffusion== in single Diffusion Transformer with ==independent diffusion timesteps== enabling flexible inference modes (policy / forward dyn / inverse dyn / video pred); **+20pp** SR on real DROID, action-free video co-training lifts Stack-Bowls **0.86→0.92** in-dist, **0.76→0.84** OOD.
- **[[2503.18938|AdaWorld]]** — ==Latent Action Autoencoder== extracts context-invariant latent actions from unlabeled video + ==Stable-Video-Diffusion-initialized autoregressive WM== + ==β-VAE info bottleneck==; **FVD 767.0** on LIBERO (vs **1545.2** baseline), **70.5%** human SR vs **20%** baseline; efficient adaptation across Habitat/Minecraft/DMLab/nuScenes.

#### 3.3 Self-Supervised Latent Models

Learn world representations from unlabeled data using self-supervised objectives — no action labels, no language captions, just raw video / image streams.

- **[[2606.03188|GeoSem-WAM]]** — Augments WAM training with ==multi-modal predictive supervision== via a ==DPT-style dense prediction head== on video ==latent== tokens, discarded at test time; **98.55%** avg LIBERO + **92.52%** RoboTwin 2.0 beating Fast-WAM, real-world **88.9% → 95.4%** (+**6.6%**), geometry (+**0.61%**) + semantic (+**0.51%**) combining to +**1.02%**.
- **[[2604.10333|ZWM]]** — ==Sparse Temporally-Factored Prediction== ViT trained on uncurated egocentric child video + ==Approximate Causal Inference== + ==Compositional Prompting==; BabyZWM (**868 hours** child video) rivals supervised SOTA on optical flow (TAP-Vid-DAVIS), **>90%** relative depth, matches Mask2Former on SpelkeBench — representations align with human fMRI + macaque electrophysiology.
- **[[2604.03208|HWM]]** — ==Top-down hierarchical planning== in shared latent space: ==high-level latent macro-actions + low-level primitive actions== with ==receding-horizon MPC==; **70%** real-robot pick-place (vs **0%** single-level VJEPA2-AC), **61%** Push-T at d=75 (vs **17%** flat DINO-WM) using **~3×** less compute, **83%** on hard mazes (vs **44%** flat PLDM) at **4×** less planning compute.
- **[[2603.29090|HCLSM]]** — Five-layer ==ViT + dynamic Slot Attention + Spatial Broadcast Decoder== + ==hierarchical SSM + Event Transformer + Goal Compression== + ==causal adjacency GNN with Gumbel-softmax== + ==acyclicity constraint== + two-stage training; MSE **0.008** PushT next-state, **38.0×** speedup via custom Triton SSM kernel.
- **[[2511.08544|LeJEPA]]** — provable and scalable SSL framework based on ==Euclidean latent geometry==; theoretical guarantees on representation quality.
- **[[2509.14252|LLM-JEPA]]** — Combines autoregressive LM loss with ==JEPA loss on multi-view (text + code/paraphrase) data== + reuses internal transformer layers as encoder/predictor + ==loss dropout==; significant gains on NL-RX-SYNTH, GSM8K, Spider for Llama-3.2 + Gemma-2-2b-it; loss dropout cuts overhead **up to 50%**.
- **[[2507.19468|DINO-world]]** — Frozen ==DINOv2 ViT-B/14 encoder== + lightweight ==cross-attention predictor with RoPE== + smooth L1 next-frame loss; **47.0%** mIoU VSPW (vs **40.7%** COSMOS), **91.3%** IntPhys, fine-tuned plan SR **93.8%** Wall env (vs **87.1%** from-scratch).
- **[[2505.03176|seq-JEPA]]** — ==Transformer sequence aggregator over action-observation pairs== + ==action-conditioned predictor head==; resolves invariance-equivariance trade-off (R² **0.71** 3DIEBench rotation + **86.14%** classification vs **80.40%** equivariant baselines); **83.44%** STL-10 PLS, scales with longer sequences.
- **[[2504.16591|JEPA for RL]]** — ==Separate context + target ViT networks== + ==JEPA loss + actor-critic gradient propagation== + ==regularization== to prevent collapse + ==learnable classification tokens==; combined JEPA-RL achieves faster learning + better performance than either alone on Cart Pole.
- **[[2512.19605|KerJEPA]]** — Generalizes JEPA regularization via ==kernel discrepancies (MMD + Kernel Stein Discrepancy)== with ==closed-form analytical sliced expressions== eliminating Monte Carlo variance + ==non-Gaussian priors== (Laplace + IMQ kernel); **91.90%** ImageNette (vs **91.13%** LeJEPA) with IMQ kernel.
- **[[2411.04983|DINO-WM]]** — Frozen DINOv2 + ==ViT transition model== with ==latent consistency loss==; **+45pp** avg over prior on manipulation (**0.90** PushT vs **0.32** IRIS), **0.82** SR WallRandom + **0.63** Chamfer GranularRandom on novel configurations — the canonical frozen-encoder WAM baseline.

**Latent WAM — Decision Matrix**

| Need | Approach |
|---|---|
| Fast latent prediction for real-time MPC | JEPA family ([[2506.09985\|V-JEPA 2]] / [[2603.14482\|V-JEPA 2.1]]) |
| Full VLA + JEPA stack | [[2602.10098\|VLA-JEPA]] (**97.2%** LIBERO, **79.5%** LIBERO-Plus OOD) |
| Unified video+action diffusion in latent space | [[2504.02792\|UWM]] or [[2505.11528\|LaDi-WM]] (**+15.1%** on LIBERO-LONG) |
| Semantic latents beat reconstruction VAEs | [[2605.06388\|Semantic-LDM-WM]] (**+9.8 pp** closed-loop, **+13.6 pp** OOD) |
| Self-supervised from frozen vision encoder | [[2411.04983\|DINO-WM]] / [[2511.08544\|LeJEPA]] |
| Object-centric latent reasoning | [[2602.11389\|Causal-JEPA]] |
| Massive-video pretraining for manipulation | [[2506.09985\|V-JEPA 2]] (**1M+ hours** video; **80%** pick-and-place from 62 hr unlabeled robot data) |

> [!star] Key Papers
> - [[2602.10098|VLA-JEPA]] — Full VLA+JEPA pipeline: **97.2%** [[2306.03310|LIBERO]] in-distribution, **79.5%** [[2510.13626|LIBERO-Plus]] OOD; defines the latent speed-quality Pareto frontier
> - [[2506.09985|V-JEPA 2]] — **1M+ hours** video pretraining; **80%** pick-and-place from **62 hours** unlabeled robot video; the JEPA-family scale anchor
> - [[2605.06388|Semantic-LDM-WM]] — First controlled head-to-head proving semantic latents beat reconstruction VAEs (**+9.8 pp** closed-loop, **+13.6 pp** OOD) inside one LDM framework
> - [[2504.02792|UWM]] — Unified video+action diffusion in one Diffusion Transformer; the clean modern latent-diffusion WAM
> - [[2411.04983|DINO-WM]] — Frozen-DINOv2 transition model; the canonical self-supervised zero-shot-planning baseline

> [!tip] Latent > Pixel for Efficiency
> Latent prediction avoids the expensive pixel-level reconstruction of VideoGen WAMs. [[2506.09985|V-JEPA 2]] achieves competitive manipulation performance using self-supervised video pre-training alone. The JEPA family shows that predicting in embedding space produces more semantically meaningful features — you don't waste capacity modeling textures and shadows. [[2605.06388|Semantic-LDM-WM]] formalizes this: in a controlled study within a single LDM framework, semantic-aligned latents ([[2603.14482|V-JEPA 2.1]], [[2502.14786|SigLIP 2]]) beat reconstruction VAEs by **+9.8 pp** closed-loop and **+13.6 pp** OOD — visual fidelity is *not* the right objective for control. Cross-reference [[05_Latent-World-Models#2. JEPA Evolution: Visual-Only → Dense → Vision-Language → Vision-Language-Action]] for the JEPA lineage in full and [[08_VLA-Reasoning-and-CoT#3. Latent Reasoning — Token-Free CoT]] for the latent-reasoning frontier built on top.

---

### 4. [[1912.01603|Dreamer]] Lineage

Model-based RL from scratch: learn a latent dynamics model (RSSM) and plan via imagination in latent space. The oldest WAM paradigm, still evolving — and the only one that works without internet-scale video or a pretrained VLM.

#### 4.1 RSSM & Latent Imagination

The foundational architecture: a recurrent latent state-space model (RSSM) that supports planning by rolling forward in imagination. The agent "imagines" thousands of action sequences in latent space and selects the best via a learned value function — no physical actions required during planning.

- **[[1912.01603|Dreamer]]** — latent imagination via ==RSSM==; learned behaviors from pixels without reward. The architectural anchor every subsequent variant extends.
- **[[2301.04104|DreamerV3]]** — universal: fixed hyperparameters across **150+** diverse tasks; ==symlog normalization== and ==KL balancing== stabilize training across Atari, control, and locomotion without per-task tuning. The modern domain-agnostic substrate.
- **[[2509.24527|Dreamer 4]]** — three-phase scalable world model (==causal tokenizer== + ==efficient transformer== + ==shortcut forcing with x-prediction==, K=4 sampling steps); first agent to obtain Minecraft diamonds offline (**0.7%** SR), real-time **21 FPS** on a single H100, action conditioning from only **100 hr** of labeled data out of **2541 hr** total — pushes the lineage toward high-complexity dynamics.

#### 4.2 Exploration & Intrinsic Motivation

Variants that bolt explicit exploration signals onto the RSSM to push the agent into rarely-visited states. The axis: *how to construct an intrinsic reward when the extrinsic one is sparse*.

- **[[2005.05960|Plan2Explore]]** — self-supervised exploration via ==world-model disagreement==; ensemble of dynamics predictors, reward = predictor variance.
- **[[2007.07853|γ-Progress]]** — ==prediction-gain curiosity== comparing current model to an ==exponentially-decaying mixture== of past models (constant memory) + ==disentangled per-agent dynamics== with DQN controller; rewards *progress* rather than uncertainty, defeats the "white noise" problem and induces emergent animate-attention matching human gaze patterns.
- **[[2503.21047|CBET-DreamerV3]]** — ==Change-Based Exploration Transfer== adapted for [[2301.04104|DreamerV3]] via two world-model + policy instances; rewards latent-state transitions, modest gains in Crafter but *negative* in Minigrid — proving intrinsic motivation is context-dependent even with modern model-based RL. **Doubles VRAM** as a cost.

#### 4.3 Physical-Robot & Continual

Adaptations to embodied / continual deployment settings — where the agent runs on real hardware or must learn across a task stream without forgetting.

- **[[2606.05015|Quadrotor World Model Study]]** — Study of ==DreamerV3-based world models== for quadrotor navigation across four ==randomness levels (L1–L4)==, with actor policies fine-tuned ==inside latent imagination==; Sobol-sampled WM3 holds win rates **>72.0%** on OOD layouts and flies an unseen corridor (gaps as narrow as **0.67 m**) plus **12 m** open-loop traverses on imagination alone.
- **[[2206.14176|DayDreamer]]** — adapted [[1912.01603|Dreamer]] to physical robots; **1 hour** of physical learning for quadruped locomotion (vs days for model-free RL). The sim-to-real-without-sim baseline.
- **[[2211.15944|Continual-Dreamer]]** — extended ==DreamerV2== with ==persistent FIFO replay across tasks== + ==Plan2Explore intrinsic exploration== + ==Reservoir Sampling==; robustly mitigates catastrophic forgetting on Minihack and beats model-free baselines in average return on Minigrid — first systematic study of world models for task-agnostic Continual RL.
- **[[2604.02911|DreamTIP]]** — extends [[1912.01603|Dreamer]] with a ==Task-Invariant Properties predictor== in latent space, LLM-extracted TIPs (base angle, contact stability, terrain clearance) from privileged observations + ==mixed-replay real-world adaptation== with frozen recurrent model + ==cosine-similarity regularization==; **+28.1%** avg over SOTA across 8 sim transfer tasks, **100%** real-world Unitree Go2 on 52 cm Climb (vs WMP **10%**) from as few as **5** real trajectories.

#### 4.4 Evolution Timeline

Chronological view — the lineage spans 2019–2026, with each entry adding a distinct capability the bullets above describe in isolation.

| Year | Paper | Contribution |
|------|-------|-------------|
| 2019 | [[1912.01603\|Dreamer]] | Latent imagination via RSSM; learned behaviors from pixels |
| 2020 | [[2005.05960\|Plan2Explore]] | Self-supervised exploration via world model disagreement |
| 2020 | [[2007.07853\|γ-Progress]] | Curiosity signal for active world model learning |
| 2022 | [[2206.14176\|DayDreamer]] | Adapted [[1912.01603\|Dreamer]] to physical robots; hours-not-days learning |
| 2022 | [[2211.15944\|Continual-Dreamer]] | Explored continual RL with world models; measured forgetting |
| 2023 | [[2301.04104\|DreamerV3]] | Universal: fixed hyperparameters across 150+ diverse tasks |
| 2025 | [[2503.21047\|CBET-DreamerV3]] | Change-based intrinsic motivation for harder exploration |
| 2026 | [[2604.02911\|DreamTIP]] | Task-invariant [[1912.01603\|Dreamer]] properties for efficient quadruped policy transfer |
| 2026 | [[2509.24527\|Dreamer 4]] | Scalable world model in complex video game environments |

#### 4.5 Related Model-Based Planning

Planning algorithms that leverage learned world models — not strict [[1912.01603|Dreamer]]/RSSM derivatives, but the same imagination-as-planning bet expressed in a different architecture.

- **[[2604.08958|WOMBET]]** — ==uncertainty-aware world-model planning== with ==uncertainty penalty== generates offline trajectories from a source task + ==dual-criterion filtering== (high return + low uncertainty) + ==adaptive sampling== mixing offline/online data; achieves comparable or higher asymptotic returns than SAC/PPO/TD3 on MuJoCo using **<half** the interaction budget.
- **[[2602.00475|GRASP]]** — ==parallel gradient-based planning== via "virtual states" + ==Langevin-style noise injection== + ==grad-cut dynamics loss== to escape brittle gradients + periodic full-rollout synchronization; **43.4%** Push-T success at 50-step horizon vs CEM **30.2%** / vanilla GD **37.6%** / Latent Collocation **4.2%** — the canonical lifted-state planner for long-horizon visual control.
- **[[2410.00564|JOWA]]** — ==shared transformer backbone== for world dynamics + Q-value via ==distributional CQL== + ==parallelizable inference planning==; **78.9%** IQM human-normalized on 15 Atari games (+**71.4%** over baselines), steepest scaling curve **40M→150M** params, **64.7%** IQM on 5 novel games with only **5k** fine-tuning transitions — the action-centered scaling baseline.
- **[[2302.01877|AdaptDiffuser]]** — ==self-evolving diffusion planner== generates ==reward-guided synthetic trajectories==, filtered by an ==inverse-dynamics discriminator== for dynamics consistency + reward; **+20.8%** over [[2205.09991|Diffuser]] on Maze2D, **+27.9%** zero-shot on unseen KUKA pick-and-place — proves diffusion planners can refine themselves without new expert data.
- **[[2205.09991|Diffuser]]** — ==denoising diffusion== over entire ==state-action trajectories== with non-autoregressive ==U-Net== + ==classifier-guided sampling== for rewards + inpainting-style goal conditioning; **>100** Maze2D scores beating MPPI/CQL/IQL on long-horizon sparse-reward tasks, one trained model adapts to new objectives by swapping only the guidance — the canonical diffusion-planning baseline.

**Dreamer Variant — Decision Matrix**

| Need | Variant |
|---|---|
| Foundational RSSM + latent imagination | [[1912.01603\|Dreamer]] / [[2301.04104\|DreamerV3]] |
| Multi-task universal (fixed hyperparameters) | [[2301.04104\|DreamerV3]] (**150+** tasks, no per-task tuning) |
| Sim-to-real fast learning on physical robot | [[2206.14176\|DayDreamer]] (**1 hour** quadruped locomotion) |
| Exploration in sparse-reward domains | [[2005.05960\|Plan2Explore]] / [[2503.21047\|CBET-DreamerV3]] |
| Continual / task-invariant transfer | [[2211.15944\|Continual-Dreamer]] / [[2604.02911\|DreamTIP]] |
| Complex video-game-scale dynamics | [[2509.24527\|Dreamer 4]] |
| Trajectory-level diffusion planning | [[2205.09991\|Diffuser]] / [[2302.01877\|AdaptDiffuser]] |

> [!star] Key Papers
> - [[2301.04104|DreamerV3]] — Fixed hyperparameters across **150+** tasks; proved model-based RL generalizes without per-task tuning — the modern domain-agnostic substrate
> - [[2206.14176|DayDreamer]] — Adapted [[1912.01603|Dreamer]] to physical robots; **1 hour** of physical learning for quadruped locomotion (vs days for model-free RL)
> - [[2205.09991|Diffuser]] — Denoising diffusion for trajectory optimization; unified planning and acting under one objective

> [!tip] Why [[1912.01603|Dreamer]] Still Matters
> [[1912.01603|Dreamer]] models are lean (no VLM backbone needed), sample-efficient ([[2206.14176|DayDreamer]] learned quadruped locomotion in 1 hour), and domain-agnostic ([[2301.04104|DreamerV3]]'s fixed hyperparameters). When you don't have a pretrained VLM or internet video, the [[1912.01603|Dreamer]] approach remains the strongest option.

---

### 5. VLM-Integrated WAMs

VLMs provide semantic understanding; world models provide dynamics prediction. These papers combine both, with the integration strategy determining which capability dominates — reasoning, unified action, test-time imagination, or compact motion.

#### 5.1 Visual Chain-of-Thought

VLM predicts *visual* subgoals (future frames or scene states) before generating actions; the world model plans between subgoals. Reasoning happens at the image-token level rather than the action level.

- **[[2604.07957|WorldMAP]]** — ==teacher-student distillation==: world-model teacher builds ==3D semantic-spatial memory== from imagined futures + ==Fast Marching Method on BEV cost map== for geometric planning, then trains a lightweight ==VLM trajectory student== on quality-filtered pseudo-labels; **ADE 42.06** / **FDE 38.87** on Target-Bench, **−18.0% ADE** and **−42.1% FDE** vs Gemini-3-Pro — world models as supervision engines, not inference-time planners.
- **[[2603.14497|WorldVLM]]** — hybrid driving stack: ==VLM emits behavioral commands + justifications== that condition the ==LAW== trajectory-predicting world model via a ==motion vector==; **+24% BERTScore F1 (0.67)** on justifications vs zero-shot, **L2 1.03m @3s** comparable to LAW alone but qualitatively more cautious; ground-truth motion-vector conditioning drops L2 to **0.27m** and collisions to **0.10%** — clean separation of high-level reasoning from low-level dynamics.
- **[[2509.02722|VLWM]]** — ==natural-language world state representation== trained on a ==Tree of Captions== from natural videos + ==dual-system planning== (System-1 reactive + System-2 self-supervised critic); **+3.2 SR / +3.9 MeanAcc** on VPA, **Elo 1261** in PlannerArena human eval (**+27%** S2 over S1), **BLEU-4 55.6** on RoboVQA, critic hits **98.4%** goal-achievement accuracy — language as abstract world state for high-level planning.
- **[[2507.23773|SimuRA]]** — ==Policy + World Model + Critic== triplet orchestrated by LLMs, using ==natural language as discrete hierarchical latent space== with separate Actor for low-level execution; **32.2%** on FlightQA (**+124%** over autoregressive baseline), **+47.5%** fact-level accuracy on FanOutQA multi-hop, **23.0%** on WebArena (**+91.7%** over BrowsingAgent) — explicit world-model simulation beats autoregressive reasoning for complex goal-oriented agents.
- **[[2601.02456|InternVLA-A1]]** — ==Mixture-of-Transformers== fusing Understanding Expert + lightweight Generation Expert (==VAE tokenization + non-autoregressive parallel decoding==, ~**13 Hz** on RTX 4090) + Action Expert; trained on InternData-A1 sim + AgiBot-World + EgoDex human videos; **75.1%** real-world static (vs **60.6%** π0 / **70.7%** π0.5), **86.7%** dynamic (**+26.7%** over π0.5 on Express Sorting); removing generation expert drops performance **20%**.

#### 5.2 Unified Policy + World Model

Single framework that *jointly* trains policy and world model under a shared objective or shared latent — not a stitched pipeline.

- **[[2606.02800|Cosmos 3]]** — ==Omnimodal Mixture-of-Transformers== jointly processing + generating language/image/video/audio/action, with distinct Reasoner (autoregressive) and Generator (==diffusion==) pathways co-initialized from pretrained VLMs; strong across **48** Physical-AI benchmarks, SOTA open-source video generation, and Cosmos3-Nano-Policy-DROID hits **39.7%** on RoboLab while ranking **#1** on real-world RoboArena — one backbone for world-model gen + robot policy.
- **[[2605.15153|Pelican-Unified]]** — first single-model unification of understanding + reasoning + imagination + action via shared ==latent variable z== + ==Unified Future Generator==: a diffusion transformer conditions on z and jointly models future video + actions with one loss. **64.7** multimodal-VLM avg (**+28.2pp** Where2Place), **93.5%** RoboTwin 50-task dual-arm, **1st** on WorldArena imagination (EWM **66.03**, 3D Accuracy **98.13**); zero-shot generalization on real robots.
- **[[2605.10942|HarmoWAM]]** — resolves the generalization-precision trade-off via ==dual action experts==: a ==predictive expert== on current-step latents for precise interaction and a ==reactive expert== on *future predicted frames* for generalizable exploration, with a ==Process-Adaptive Gating Mechanism== switching by task stage (transit vs interaction). **89%** in-domain average across six real-world tasks with only **7.9%** OOD drop — smallest gap among unified WAMs.
- **[[2603.08572|MetaWorld-X]]** — hierarchical world model handling ==negative interference== in monolithic humanoid RL by decomposing control into ==Specialized Expert Policies (SEPs)== + a VLM-guided ==Intelligent Routing Mechanism (IRM)==; SEPs trained via ==energy-based imitation rewards== (H2O). 'Walk' converges in **0.5M steps** vs TD-MPC2's **1.8M**; **9/10** Walk/Run/Carry; **470.0** 'Door' return vs TD-MPC2's **285.0** — let the VLM compose experts, not learn a monolith.
- **[[2602.12063|VLAW]]** — ==iterative co-improvement== alternating between fine-tuning a pre-trained ==action-conditioned WM== on ==real-world rollouts (with failure cases)== then generating ==synthetic trajectories== filtered by a ==VL reward model==; world-model FVD drops **225.13→64.12**, VLA success **0.46→0.868** (**+39.2pp**) on contact-rich tasks; synthetic data alone contributes **+11.6pp** — the canonical mutual-improvement template.
- **[[2511.17502|RynnVLA-002]]** — ==autoregressive VLA+WM unification== initialized from ==Chameleon== LLM + ==attention masking for discrete actions== (each action conditions only on visual/textual inputs) + compact continuous ==Action Transformer head== with learnable queries for parallel chunk decoding; **97.4%** LIBERO without large-scale pretraining, **>80%** real-world "Place the block" in clutter; integrating WM training data lifts real-world SR by **+50%**.
- **[[2506.21539|WorldVLA]]** — ==autoregressive action + world-state forecasting== on a ==Chameleon-initialized VLM== with discrete tokenizers for image/text/action + novel ==action-attention masking== that prevents error propagation in chunk decoding; **81.8%** LIBERO grasp success at 512×512 (vs **76.5%** discrete OpenVLA); WM data lifts SR **62.8%→67.2%**, action masking lifts naive chunking **54.0%→76.6%**.
- **[[2506.19850|UniVLA]]** — ==discrete-token unification== of vision/language/action in a shared 8.5B-param ==autoregressive Transformer== with two-stage training (==action-free video WM pretraining== then policy fine-tune); SOTA on CALVIN, **95.5%** avg on LIBERO (LIBERO-Long **94.0%**); WM pretraining matches full-data CALVIN with only **10%** fine-tuning data.

#### 5.3 Imagination & Test-Time Reasoning

World model used for *test-time* simulation: the agent runs imagined rollouts during deployment to evaluate candidate plans. Expensive but maximally flexible — the imagination budget adapts to task difficulty.

- **[[2604.11751|GWM-MPC]]** — ==Grounded World Model== predicting in a ==frozen Qwen3-VL-Embedding latent space== + ==Rendering-based Action Tokenization (RAT)== rendering joint actions as images + ==KNN trajectory proposal==; **87%** on WISER semantic-generalization benchmark vs **22%** VLA average / **47%** best VLA, **83%** zero-shot cross-embodiment on xArm6 trained only on Panda — disentangling action from semantic understanding prevents knowledge forgetting.
- **[[2604.11302|3D-ALP]]** — ==persistent 3D camera-to-world anchor== updated via forward kinematics + ==MCTS over a 3D-consistent generative WM (InSpatio-WorldFM)== as oracle + ==hybrid VLM-semantic + kinematic-depth scorer==; **0.650** SR on memory-required steps vs **0.006** greedy reactive (**+0.645**), **0.822** on chained 2-position memory vs **0.000** baseline; persistent tree-search memory alone accounts for **82%** of the gain — gives reactive VLAs object permanence.
- **[[2604.07392|ERA]]** — ==Event-Centric Retrieval-Based Action==: dynamic envs abstracted to ==semantic events== in a compact latent space + ==memory-augmented retrieval (ANN)== over a physics-informed knowledge bank + ==Clustered Bayesian Selection== to avert "average-to-collision" multimodal failures + ==Lyapunov stability constraints==; **100%** SR with zero collisions across 5 adversarial UAV curricula, **sub-millisecond** decisions on Jetson Orin Nano.
- **[[2602.08236|AVIC]]** — ==Adaptive Visual Imagination Control== with a ==policy-model gatekeeper== deciding whether to skip/invoke the WM + ==trajectory-level verification== of full imagined paths; GPT-4.1 on SAT-Real **74.0%→79.3%** with ~**17×** fewer WM calls and ~**9×** fewer language tokens than always-on imagination; the budget-aware test-time baseline — small 1-2-view imagination beats exhaustive expansion.
- **[[2507.12508|MindJourney]]** — couples VLMs with ==controllable video-diffusion world models== via a ==Spatial Beam Search== that plans exploratory trajectories then accumulates multi-view evidence — training-free; **+7.7%** avg top-1 across diverse VLMs on SAT, OpenAI o1 on SAT-Real **74.6%→84.7%** — VLM imagination via a physically-consistent simulator is orthogonal to text-CoT scaling.
- **[[2602.01960|GVP-WM]]** — converts physically-inconsistent video plans into feasible actions via ==video-guided latent collocation== on an ==action-conditioned WM== using the ==Augmented Lagrangian Method== + a ==scale-invariant alignment loss==; **0.80** Push-T SR with domain-adapted videos where UniPi fails, holds **0.82** under MB-10 motion blur vs UniPi collapse **0.52→0.03** — robust grounding of video generators in dynamics-feasible action.
- **[[2601.14514|JIT]]** — ==Just-in-Time== cognitive model interleaving ==simulation + visual search + dynamic representation modification== on a ==representational sketchpad==; explains human memory (**r=0.95**) and attention (**r=0.88**) during grid-world planning + physical reasoning (**r=0.87** recall / **r=0.96** confidence), beats Value-Guided Construal in dissociation tests — algorithmic account of how minds avoid the pre-computation paradox by encoding objects *only when relevant*.

#### 5.4 Compact Motion Representations

Predict condensed motion signals (optical flow, motion tokens) instead of full video frames. Trades visual richness for inference speed.

- **[[2602.22010|WoG]]** — ==World Guidance==: compresses future observations into a compact ==condition space== via a ==Q-Former encoder== over frozen vision features + ==two-stage curriculum== (explicit conditions → self-guided inference); **69.4%** avg on Google Robot in sim (vs **60.5%** π0-FAST), real-world "Pick and Place" lifts **60%→85%** with UMI data — resolves the redundancy-precision trade-off by predicting only action-relevant features.

**VLM-Integrated WAM — Decision Matrix**

| Need | Approach |
|---|---|
| Single end-to-end unified model (shared latent z) | [[2605.15153\|Pelican-Unified]] (**64.7** VLM avg, **93.5%** RoboTwin, **1st** on WorldArena) |
| Generalization-precision dual experts | [[2605.10942\|HarmoWAM]] (**89%** in-domain, **−7.9%** OOD drop) |
| Hierarchical humanoid loco-manipulation | [[2603.08572\|MetaWorld-X]] (**0.5M** steps vs **1.8M** TD-MPC2) |
| Visual chain-of-thought subgoal planning | [[2604.07957\|WorldMAP]] / [[2509.02722\|VLWM]] |
| Iterative co-improvement (VLA ↔ WM) | [[2602.12063\|VLAW]] (**+39%** improvement loop) |
| Adaptive test-time imagination budget | [[2602.08236\|AVIC]] (decides when/how much to imagine) |
| Compact motion representation (no full video) | [[2602.22010\|WoG]] |
| Unified VLA + WM under one loss | [[2506.21539\|WorldVLA]] / [[2506.19850\|UniVLA]] |

> [!star] Key Papers
> - [[2605.15153|Pelican-Unified]] — First single-model unification of understanding + reasoning + imagination + action via shared latent z; **64.7** VLM avg, **93.5%** RoboTwin dual-arm, **1st** on WorldArena — structurally shared representations beat modular assembly
> - [[2605.10942|HarmoWAM]] — Resolves the generalization-precision trade-off via dual experts + process-adaptive gating; **89%** in-domain, smallest reported OOD drop (**−7.9%**)
> - [[2602.12063|VLAW]] — The canonical iterative co-improvement loop: VLA and WM reinforce each other; **+39.2pp** on contact-rich tasks
> - [[2602.08236|AVIC]] — Adaptive test-time imagination: decides *when and how much* to imagine, **17×** fewer WM calls than always-on
> - [[2506.19850|UniVLA]] — Discrete-token VLA+WM unification; WM pretraining matches full-data CALVIN with only **10%** fine-tuning data

> [!tip] The Co-Improvement Insight
> [[2602.12063|VLAW]] showed that VLA and world model don't just coexist — they actively improve each other through iterative training. The world model generates better synthetic data for the VLA, and the VLA's improving actions give the world model harder scenarios to learn from. Cross-reference [[03_VLA#5. World-Model-Augmented VLAs]] for the VLA-side framing of the same architectures and [[08_VLA-Reasoning-and-CoT#2. Visual Chain-of-Thought]] for how visual chain-of-thought composes with WAM-integrated VLAs.

---

### 6. Efficient & Action-Centered WAMs

Full video generation at test time is **4.8x slower** than pure VLAs. These models keep WAM benefits while eliminating the inference bottleneck via three architectural strategies — train with video then strip it at deployment, plan in compact latent / action spaces, or add uncertainty layers so the agent knows when to fall back to cautious behavior.

#### 6.1 Training-Time Video, Test-Time Speed

Train with video co-training to absorb spatiotemporal priors; deploy with a slim action head — *no test-time video generation*. The dominant efficient-WAM recipe of 2026.

- **[[2603.16666|Fast-WAM]]** — video co-training during training; ==ActionDiT== runs alone at deployment (~**190 ms/step**); no test-time imagination. WAM robustness without WAM latency — the canonical production recipe.
- **[[2603.17240|GigaWorld-Policy]]** — ==unified diffusion Transformer== jointly modeling action chunks + sparsely-sampled future visual observations under ==flow matching==; action-only decoding at inference for low latency + ==curriculum pretraining== from web-video → embodied → target-robot data; **360 ms/step** on A100 (~**9× speedup** vs Motus's 3231 ms), **0.83** avg real-world SR (**+7%** over Motus, **+14%** over VLM-based VLAs), comparable performance with **10%** training data.

#### 6.2 Latent Planning & Parameter-Efficient Transfer

Compact latent representations for fast planning, or LoRA-scale adaptation that swaps in a new WAM without retraining the backbone.

- **[[2605.06247|CKT-WAM]]** — parameter-efficient context transfer between WAMs; **86.1%** [[2510.13626|LIBERO-Plus]] with only **1.17%** trainable params; matches full fine-tune. The LoRA-scale baseline for WAM-to-WAM transfer.
- **[[2512.19133|WorldRFT]]** — ==Spatial-aware World Encoder== injects frozen ==VGGT== 3D priors + ==Hierarchical Planning Refinement== with local-aware deformable convolution + ==GRPO RL fine-tuning== with collision-aware sparse reward; **−21% L2** and **−83% collision rate** (**0.30%→0.05%**) over LAW on nuScenes, **PDMS 87.8** vision-only on NavSim closed-loop nearly matching LiDAR, **96.8% Drivable Area Compliance** — safety as active objective rather than passive imitation.
- **[[2503.16806|DyWA]]** — ==teacher-student distillation== with student jointly predicting actions + future object states from single-view point cloud + ==Dynamics Adaptation Module== inferring physical properties via ==FiLM conditioning==; **+31.5%** SR over SOTA, **82.2%** seen / **75.0%** unseen objects in sim, **68%** zero-shot real with no external pose tracking vs CORN **36%** — generalizable non-prehensile manipulation without multi-view rigs.
- **[[2410.00564|JOWA]]** — ==shared transformer backbone== for world dynamics + Q-value via ==distributional CQL== + ==parallelizable planning at inference==; **78.9%** IQM on 15 Atari (+**71.4%** over baselines), steepest scaling curve **40M→150M** params, **64.7%** IQM on 5 novel games with only **5k** fine-tune transitions — the action-centered scaling baseline.

#### 6.3 Uncertainty-Aware & Self-Verifying

Introspection layers so the agent knows when to *distrust* its own predictions — and falls back to cautious behavior or queries an oracle.

- **[[2504.16680|RWM-U]]** — Robotic World Model with ==epistemic uncertainty==; enables offline model-based RL on real robots by detecting OOD states.
- **[[2604.01985|WAV]]** — World-model Asymmetry Verification: compares ==forward model== (predict next state from action) with ==inverse model== (infer action from transition); disagreement = unreliable dynamics. Self-correcting WAM.
- **[[2604.11351|WM-DAgger]]** — world-model-based ==DAgger==; uses imagined rollouts as the expert query, eliminating online expert queries during data aggregation.
- **[[2511.11520|Video WM Policy Eval]]** — uses an ==action-conditional video diffusion model== to evaluate policies without real-robot rollouts: roll out inside the video WM, then an ==off-the-shelf VLM== judges success; rollout-augmented training (**PSNR 18.7 → 20.6**), **Pearson r = 0.833–0.879** policy-ranking correlation in RoboMimic sim and **r = 0.687** against real-world Bridge.

**Efficient WAM — Decision Matrix**

| Need | Recommendation |
|---|---|
| Production deployment with WAM robustness | [[2603.16666\|Fast-WAM]] |
| Parameter-efficient transfer (LoRA-scale) | [[2605.06247\|CKT-WAM]] (**1.17%** trainable params) |
| Action-centered training from scratch | [[2603.17240\|GigaWorld-Policy]] |
| Real-time latent planning (driving / control) | [[2512.19133\|WorldRFT]] |
| Offline model-based RL with uncertainty | [[2504.16680\|RWM-U]] |
| Self-correction via forward-inverse check | [[2604.01985\|WAV]] |
| Eliminate online expert queries | [[2604.11351\|WM-DAgger]] |

> [!star] Key Papers
> - [[2603.16666|Fast-WAM]] — proves the **training-time video, test-time speed** recipe; WAM robustness without WAM latency penalty
> - [[2605.06247|CKT-WAM]] — **86.1%** [[2510.13626|LIBERO-Plus]] with only **1.17%** trainable params; the parameter-efficient transfer baseline
> - [[2410.00564|JOWA]] — jointly-optimized world-action pretraining; the action-centered scaling baseline

> [!success] The Efficiency Recipe
> ==Train with video objectives== (to get spatiotemporal priors) → ==Deploy without video generation== (no test-time imagination). [[2603.16666|Fast-WAM]] proved this works: you get most of the robustness benefit without the latency penalty.

> [!tip] Training-Time vs Test-Time Video
> The critical insight from 2026: you need video generation at **training time** (to learn physics) but NOT at **test time** (where it causes latency). This decouples the benefit of VideoGen WAMs from their computational cost. Cross-reference [[03_VLA#2. Efficient & Lightweight VLAs]] for the efficient-VLA design space (parameter-light models that pair well with these efficient WAMs) and [[11_Sim-to-Real-Transfer#6. Integration Patterns]] for the learned-sim deployment recipe.

---

## Part C — Capabilities, Comparison & Open Problems

*Self-evolution, cross-paradigm comparison, and the open problems / failure modes that still bound WAM progress.*

### 7. Self-Evolving WAMs

WAMs that autonomously improve through experience, self-play, or co-evolution. See [[06_Self-Evolving-VLA-WAM#5. Self-Evolving WAMs]] for the full deep-dive on self-evolving mechanisms, VLA vs WAM comparison, failure modes, and research directions.

#### 7.1 Reflective Planning Loops

Generate, critique, regenerate. The agent improves through self-assessment of its own predictions — judging plan quality turns out to be easier than generating perfect plans first try.

- **[[2603.08403|SPIRAL]]** — closed-loop reflective planning: agent generates a long-horizon action-conditioned video plan; ==CriticAgent== evaluates temporal coherence + action completeness; failed plans regenerate with critic feedback. The canonical generate → critique → regenerate template — *judging* plan quality is easier than *generating* perfect plans, so VLM reasoning can score "physical sense" even when the generator can't produce perfect physics first pass.
- **[[2502.05907|EvoAgent]]** — three-part loop with continual world model: ==self-planning== proposes a plan via the WM, ==self-control== executes while monitoring prediction error, ==self-reflection== compares predicted vs actual outcomes and updates WM + policy. The continual WM provides both the prediction-error signal for control and the training signal for reflection. **+105%** on long-horizon tasks; the loop contributes **72%** of total gain (Minecraft).

#### 7.2 Self-Play & Autonomous Exploration

Agent generates its own training data via play or epistemic curiosity — no human demonstrations required. The "free data" recipe.

- **[[2603.09030|PlayWorld]]** — ==autonomous self-play data collection== with ==VLM Task Proposer + VLA Executer== + ==Stable-Video-Diffusion== finetuned via ==curriculum learning== on diverse contact-rich play; captures failure modes (missed grasps, slips) absent in human data, **Pearson 0.8766** between predicted and real-world success, **+65%** real-world SR via in-model fine-tune — scales WAM training without human demonstrations.
- **[[2503.01584|SENSEI]]** — semantic exploration with ==epistemic uncertainty== + Go-Explore; targeted exploration of high-uncertainty regions rather than uniform random play.
- **[[2506.23468|NavMorph]]** — ==RSSM-based WM== with ==Contextual Evolution Memory== for gradient-free online adaptation + feature-level (not pixel) future prediction; **+4.1% SR / +2.73% SPL** on RxR-CE unseen, **2.1× faster** test-time adaptation than gradient-based alternatives — navigation-specialized self-play in continuous 3D environments.

#### 7.3 RL-Driven & Co-Evolving

Continual RL on world-model dynamics; agent and environment co-evolve. The world model is itself a learning target, not just a frozen simulator.

- **[[2603.19370|VAMPO]]** — RL optimization of video action model dynamics via ==GRPO==; the canonical GRPO-on-WAM recipe.
- **[[2504.21024|WebEvolver]]** — co-trains a web agent policy + ==dedicated world-model LLM== generating synthetic multi-step trajectories + ==WMLA inference-time multi-step lookahead==; **+10%** over OpenWebVoyager baseline, **51.37%** SR on WebVoyager and **24.53%** on Mind2Web-Live (from **18.86%**) at WMLA depth 2 — overcoming self-improvement plateaus via WM-generated diversity.

**Self-Evolving WAM — Decision Matrix**

| Need | Mechanism |
|---|---|
| Plan-then-critique improvement loop | [[2603.08403\|SPIRAL]] |
| Continual 3-part loop (plan / control / reflect) | [[2502.05907\|EvoAgent]] (**+105%** on long-horizon) |
| Autonomous self-play data collection | [[2603.09030\|PlayWorld]] |
| Epistemic-driven exploration | [[2503.01584\|SENSEI]] |
| Visual-language-navigation self-evolution | [[2506.23468\|NavMorph]] |
| RL on video action-model dynamics | [[2603.19370\|VAMPO]] (GRPO-based) |
| Co-evolving agent + world model | [[2504.21024\|WebEvolver]] |

> [!star] Key Papers
> - [[2603.08403|SPIRAL]] — closed-loop reflective planning (generate → critique → regenerate) is the canonical self-improving WAM template; judging plan quality is easier than generating perfect plans
> - [[2502.05907|EvoAgent]] — three-part loop with continual world model; **+105%** on long-horizon tasks; loop contributes **72%** of total gain — proves continual world models are the key enabler for self-evolution
> - [[2603.09030|PlayWorld]] — autonomous self-play data collection scales WAM training without human demonstrations; the "free data" recipe

> [!tip] Why WAMs Enable Self-Evolution
> WAMs already have a learned dynamics model that generates synthetic experience — the agent can "rehearse" in imagination, discover failure modes, and improve without costly real-world interaction. See [[06_Self-Evolving-VLA-WAM#2. Self-Evolving Agent vs VLA vs WAM]] for the comprehensive comparison of self-evolving VLAs, WAMs, and embodied agents, and [[03_VLA#9. Self-Evolving & Continual VLAs]] for the VLA-side continual-learning landscape that pairs with these WAM mechanisms.

---

### 8. Cross-Paradigm Comparison

WAM paradigms encode different bets on the speed–robustness–sample-efficiency frontier. The five families don't compete on a single axis — they occupy orthogonal points in the design space, each dominating one constraint at the cost of others. This section frames the trade-offs so practitioners can pick the right paradigm for the deployment constraint that *actually binds*.

The 2026 frontier is hybridization: train with VideoGen objectives to absorb spatiotemporal priors, then deploy without test-time imagination (the [[2603.16666|Fast-WAM]] / [[2602.10098|VLA-JEPA]] recipe). The choice of paradigm has become a choice of *which axis to optimize at deployment*, not which is "best".

#### 8.1 Robustness-Optimized Paradigms

Maximize physics fidelity and zero-shot generalization at the cost of inference latency. The frontier when the bottleneck is *out-of-distribution* generalization, not throughput.

- **[[2602.15922|DreamZero]]** (VideoGen) — slowest (~**7Hz**) but highest robustness; **39.5%** on unseen tasks via cross-embodiment video priors. Defines the robustness ceiling.
- **[[2605.15153|Pelican-Unified]]** (VLM-Integrated) — moderate speed, high robustness via unified VLM + WAM; **64.7** VLM avg, **93.5%** RoboTwin; the unified-architecture entry on the robustness frontier.

#### 8.2 Speed-Optimized Paradigms

Maximize inference throughput for real-time control and production deployment. The frontier when the bottleneck is *latency per decision*, not absolute robustness.

- **[[2602.10098|VLA-JEPA]]** (Latent) — fast latent prediction (~**10ms/step**); **97.2%** [[2306.03310|LIBERO]] in-distribution; the speed-quality Pareto baseline.
- **[[2603.16666|Fast-WAM]]** (Efficient) — training-time video, test-time action-only; ~**190ms/step** at deployment; the canonical production-ready recipe.

#### 8.3 Sample-Efficient Paradigms

Maximize what's learnable from *limited* data without VLM priors. The frontier when neither internet-scale video nor a pretrained VLM is available.

- **[[2301.04104|DreamerV3]]** ([[1912.01603|Dreamer]] Lineage) — highest sample efficiency; **150+** tasks with *fixed hyperparameters*; works without internet-scale data. The substrate when the data axis collapses to zero.

**Paradigm — Decision Matrix**

| Paradigm | Speed | Robustness | Sample Efficiency | Transfer | Best For |
|----------|-------|-----------|-------------------|----------|----------|
| **VideoGen** ([[2602.15922\|DreamZero]]) | Slow (7Hz) | Highest | Moderate | Cross-embodiment via video | Novel environments, zero-shot |
| **Latent** ([[2602.10098\|VLA-JEPA]]) | Fast | High | High | Latent transfer | In-domain, real-time control |
| **[[1912.01603\|Dreamer]]** ([[2301.04104\|DreamerV3]]) | Fast | Moderate | Highest | Within-domain | Limited data, no VLM available |
| **VLM-Integrated** ([[2602.12063\|VLAW]]) | Moderate | High | Moderate | Semantic transfer | Complex tasks needing reasoning |
| **Efficient** ([[2603.16666\|Fast-WAM]]) | Fast | High | Moderate | VideoGen priors, fast deploy | Production deployment |

> [!star] Key Papers (one canonical per paradigm)
> - [[2602.15922|DreamZero]] — canonical **VideoGen** WAM; 14B joint video+action model; **39.5%** unseen tasks; defines the robustness ceiling
> - [[2602.10098|VLA-JEPA]] — canonical **Latent** WAM; **97.2%** LIBERO at ~**10ms/step**; defines the speed-quality Pareto frontier
> - [[2301.04104|DreamerV3]] — canonical **Dreamer** paradigm; **150+** tasks with fixed HP; the limited-data substrate
> - [[2605.15153|Pelican-Unified]] — canonical **VLM-Integrated** WAM; unified understanding + imagination + action; **93.5%** RoboTwin
> - [[2603.16666|Fast-WAM]] — canonical **Efficient** WAM; proves training-time video + test-time speed; the production recipe

> [!tip] No Single Winner — Match Paradigm to Constraint
> Each paradigm dominates one axis: **VideoGen** maximizes robustness at the cost of speed (~7Hz); **Latent** ([[2602.10098|VLA-JEPA]]) maximizes speed and sample efficiency; **[[1912.01603|Dreamer]]** lineage maximizes sample efficiency for limited-data regimes; **VLM-Integrated** maximizes semantic transfer for complex tasks; **Efficient** ([[2603.16666|Fast-WAM]]) wins for production deployment. The 2026 frontier hybridizes — train with VideoGen objectives, deploy without test-time imagination ([[2603.16666|Fast-WAM]], [[2602.10098|VLA-JEPA]]) — extracting robustness without paying the latency cost. Cross-reference [[05_Latent-World-Models#1. The JEPA Principle]] for the JEPA design space in depth, [[06_Self-Evolving-VLA-WAM#2. Self-Evolving Agent vs VLA vs WAM]] for the agent-VLA-WAM comparison axis, and [[11_Sim-to-Real-Transfer#6. Integration Patterns]] for deployment-pattern selection.

---

### 9. Open Problems & Failure Modes

WAMs convert visual or latent prediction into actionable policy — but their failure modes cluster into three distinct categories: *generative pathologies* (the model predicts physically impossible or trivially exploitable futures), *deployment-side weaknesses* (inference latency, adversarial robustness), and *uncertainty handling* (the model doesn't know when its own predictions are unreliable). Each category needs a different remediation path; conflating them leads to chasing the wrong fix.

#### 9.1 Generative & Prediction Pathologies

The cluster of failures rooted in the WAM's own prediction quality — hallucinated dynamics, exploited artifacts, and the coupled dynamics-reward bottleneck.

- **==Hallucinated dynamics==** — VideoGen WAMs can predict physically impossible futures (object teleportation, mass non-conservation). [[2603.23376|ABot-PhysWorld]] addresses this with ==Diffusion-DPO== over preference pairs scored by a physics critic.
- **==Artifact exploitation==** — Agents trained on WAM rollouts may exploit unrealistic visual artifacts in generated video (smooth gradients that don't exist in real cameras), leading to policies that fail at deployment. Physics-grounded training objectives mitigate but don't eliminate.
- **==Object-identity entanglement==** — Holistic WAMs fuse target identity with surrounding visual content; small scene changes flip target binding. [[2605.06481|OA-WAM]] — object-addressable attention with cached identity addresses; **+4.8pp** [[2510.13626|LIBERO-Plus]] geometric robustness over π0.5.
- **==Coupled dynamics-reward error==** — Existing return-gap theory treats learned dynamics + reward as one entity, hiding which is the bottleneck. [[2605.06732|Training in Imagination]] — decomposes the bound into separate dynamics and reward error terms; reward error decays much faster (exponent **0.96**) than dynamics error (**0.11**), so for fixed budgets the dominant residual is dynamics — invest there.

#### 9.2 Deployment-Side Weaknesses

Problems exposed once a WAM leaves the training loop — inference latency, adversarial vulnerability, and the perturbation-robustness asymmetry vs. VLAs.

- **==Inference latency==** — WAMs are **≥4.8x** slower than VLAs ([[2603.22078|WAM vs VLA Robustness]]); naive deployment misses real-time control loops. Use [[2603.16666|Fast-WAM]] for ==training-only video== (test-time speed) or latent-prediction variants (§3) to amortize cost.
- **==Adversarial jailbreaking==** — [[2604.05498|JailWAM]] shows WAMs are vulnerable to adversarial perturbations on action generation; small input shifts induce safety-violating rollouts. Need adversarial robustness training, currently underdeveloped relative to vision-only adversarial work.
- **==Visual perturbation robustness (positive)==** — Conversely, WAMs *outperform* VLAs on camera/light/background changes ([[2603.22078|WAM vs VLA Robustness]]); spatiotemporal priors from video pretraining act as a regularizer. This asymmetry — robust to vision shift, vulnerable to action-space adversarial — suggests the two failure modes have orthogonal roots.

#### 9.3 OOD Detection & Uncertainty Handling

When should a WAM distrust its own predictions? Three complementary signals are emerging — each cheap on its own, but none yet integrated into a unified abstention policy.

- **==Prediction error monitoring==** — [[2603.04029|Self-Adapting RL]] tracks the residual between predicted and observed next states; when the residual exceeds a threshold, the WAM flags the state as OOD and triggers targeted adaptation.
- **==Surprise filtering==** — [[2512.01119|WM Surprise Robustness]] distinguishes genuine OOD events (new physics) from sensor noise (camera glitch) by filtering prediction errors through a learned noise model.
- **==Forward-inverse asymmetry==** — [[2604.01985|WAV]] compares the forward model (predict next state from action) with the inverse model (infer action from state transition); disagreement reveals states where dynamics are poorly modeled.

**WAM Failure Modes — Decision Matrix**

| Problem | Remediation Path |
|---|---|
| Hallucinated / physically impossible rollouts | [[2603.23376\|ABot-PhysWorld]] (Diffusion-DPO with physics critic) |
| Artifact exploitation by trained policy | Physics-grounded training objectives — see [[07_Physics-Aware-Embodied-AI#3. Explicit Physics Losses for Video Generation]] |
| Object-identity confusion under scene shift | [[2605.06481\|OA-WAM]] (object-addressable attention) |
| Don't know whether dynamics or reward is the bottleneck | [[2605.06732\|Training in Imagination]] (decomposed return-gap bound) |
| WAM too slow for real-time loop | [[2603.16666\|Fast-WAM]] (training-only video) or latent WAMs (§3) |
| Action-space adversarial robustness | [[2604.05498\|JailWAM]] (exposes attack surface; no fix yet) |
| WAM should abstain on OOD state | [[2603.04029\|Self-Adapting RL]] + [[2512.01119\|WM Surprise Robustness]] + [[2604.01985\|WAV]] (combine signals) |

> [!star] Key Papers — WAM Failure Frontier
> - [[2605.06732|Training in Imagination]] — Decomposes return-gap into separate dynamics + reward error terms; the canonical evidence that dynamics-error (exponent **0.11**) dominates reward-error (**0.96**) at scale — invest the data budget in dynamics
> - [[2605.06481|OA-WAM]] — Object-addressable attention with cached identity; **+4.8pp** [[2510.13626|LIBERO-Plus]] geometric robustness — the first principled fix for holistic-WAM identity entanglement
> - [[2604.05498|JailWAM]] — Exposes adversarial attack surface on WAM action generation; the canonical "WAMs are not yet safe" evidence and the open-problem benchmark for robustness research

> [!tip] When to Use WAM vs VLA — and the Common Root of WAM Failures
> **Use WAM when** robustness to visual perturbations matters, physics-aware planning is needed, or real-world data is limited (world model enables imagination). **Use pure VLA when** inference speed is critical, tasks are simple enough for direct imitation, or in-domain data is abundant. The common root across §9.1–§9.3 failures is **calibration**: WAMs predict confidently in regimes where the prediction is unreliable. Three of seven problems above (hallucination, artifact exploitation, identity entanglement) are *training-time* miscalibration — the WAM doesn't know it's outside its training distribution. The remaining four (latency, adversarial, OOD detection, dynamics-reward decomposition) are *deployment-time* miscalibration — the WAM doesn't know when to abstain or hand off. Cross-reference [[05_Latent-World-Models#6. Open Problems]] (latent-space failure modes with the same calibration root) and [[07_Physics-Aware-Embodied-AI#8. Open Problems]] (physics-verifiability as the upstream constraint that *would* fix many of these if it generalized).

---

## Quick-Reference Matrix

| Question | Answer |
|----------|--------|
| Need physics? | VideoGen ([[2602.15922\|DreamZero]]) or physics-aligned ([[2603.23376\|ABot-PhysWorld]]) |
| Need speed? | Latent ([[2602.10098\|VLA-JEPA]]) or Efficient ([[2603.16666\|Fast-WAM]]) |
| Limited data? | [[1912.01603\|Dreamer]] lineage (sample-efficient from scratch) |
| Need reasoning? | VLM-Integrated ([[2602.12063\|VLAW]], [[2603.14497\|WorldVLM]], [[2602.08236\|AVIC]]) |
| Need both generalization AND precision? | [[2605.10942\|HarmoWAM]] — dual predictive+reactive experts with process-adaptive gating |
| Need self-improvement? | Self-Evolving ([[2502.05907\|EvoAgent]], [[2603.08403\|SPIRAL]]) |
| Need cross-embodiment? | VideoGen ([[2602.15922\|DreamZero]]) — video priors transfer |
| Need object-identity robustness? | [[2605.06481\|OA-WAM]] — object-addressable attention with cached identity addresses |
| Need parameter-efficient transfer? | [[2605.06247\|CKT-WAM]] — context-knowledge transfer at 1.17% trainable params |
| Production deployment? | Efficient ([[2603.16666\|Fast-WAM]]) — training-time video, test-time speed |
| Full JEPA lineage? | [[05_Latent-World-Models#2. JEPA Evolution: Visual-Only → Dense → Vision-Language → Vision-Language-Action]] for [[2506.09985\|V-JEPA 2]] → 2.1 → [[2512.10942\|VL-JEPA]] → [[2602.10098\|VLA-JEPA]] |

---

## Cross-References

- [[03_VLA]] — VLA deep-dive (Section 6 covers WAM-augmented VLAs)
- [[05_Latent-World-Models]] — Detailed JEPA evolution ([[2506.09985|V-JEPA 2]] → 2.1 → [[2512.10942|VL-JEPA]] → [[2602.10098|VLA-JEPA]] → [[2602.11832|JEPA-VLA]] → [[2510.00739|TD-JEPA]] → [[2511.19221|Percept-WAM]])
- [[06_Self-Evolving-VLA-WAM]] — Self-evolving VLAs & WAMs deep dive
- [[07_Physics-Aware-Embodied-AI]] — Physics-aware video generation, physics priors, and physics-coupled training
- [[08_VLA-Reasoning-and-CoT]] — Reasoning insertion patterns in WAM-augmented VLAs
- [[09_Egocentric-Pretraining-and-Human-Video]] — Egocentric video as a pretraining substrate for WAMs
- [[10_Force-Aware-and-Tactile-Policies]] — Force/tactile policies deep-dive; complements WAM action conditioning
- [[11_Sim-to-Real-Transfer]] — Sim-to-Real Transfer deep-dive; covers learned simulators as objects of study
- [[01_Embodied-AI-101]] — VLA vs WAM basics and four learning strategies
- [[02_Dataset-Benchmark-Environment]] — Datasets, benchmarks, and simulation platforms

---

*See [[03_VLA]] for the VLA alternative, [[07_Physics-Aware-Embodied-AI]] for physics-coupled training, or [[01_Embodied-AI-101]] to start from the basics.*
