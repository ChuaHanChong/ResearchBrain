---
title: "Contact-Rich & Tactile Control — Deep Dive"
tags:
  - tactile
  - force-aware
  - VLA
  - robotics
  - embodied-AI
  - manipulation
aliases:
  - "Contact-Rich & Tactile Control"
  - "Contact-Rich Control"
  - "Force-Aware and Tactile Policies"
  - "Tactile Manipulation Deep Dive"
---

# Contact-Rich & Tactile Control — Deep Dive

> [!abstract] Overview
> Physical interaction at the fingertip — governed by forces, contact, and compliance the camera cannot see — is the axis this note unifies. A force-aware policy fails the moment it treats force as an afterthought rather than a first-class signal, and the field's central finding is that contact dynamics deserve their *own* encoder, attention path, and gated expert, never naive concatenation with visual tokens. The note spans three threads of that axis. **Foundations & sensing** (Part A): the design-space of where force enters a policy and how it's pretrained, plus tactile sensor hardware (capacitive skins, FPC pads, binocular vision-tactile fingertips) and the touch-SSL foundation models that amortize labeling cost. **Force-conditioned policy architectures** (Part B): force-conditioned VLAs (force-aware action heads, force-aware MoE, force-grounded tactile alignment, human-intervention refinement) and force-as-generation-conditioning ([[2505.19386|Force-Prompting]]). **Evaluation** (Part C): contact-rich manipulation benchmarks, vision-to-tactile prediction, contact-grounded policies, tactile world models, and dexterous in-hand manipulation. The recurring architectural insight — **force/contact must be a first-class modality with its own parameters** — lifts to the body scale too: for whole-body and locomotion control (unified controllers, balance under load, humanoid skill data), see the sibling deep-dive [[12_Whole-Body-and-Locomotion-Control]]. For the RL-*methods* underpinning the control side, see [[03_Imitation-Learning-and-RL#6. RL for Locomotion, Navigation & Whole-Body Control]]; this note covers the contact-dynamics *substrate*.

## Evolution Graph

The *fingertip* thread of the contact-dynamics axis: bolt-on force sensors and per-task contact policies gave way to force-aware MoE VLAs that treat force/torque as a first-class modality, then to hybrid force-position control, contact grounding, and affordable open-source sensing hardware — all converging on force/contact as a dedicated signal rather than a concatenated input.

```text
1. Tactile Hardware   (getting a signal at all)
· sensor platforms
╔═══════════════╗
║ TacTip (2021) ║─┐
╚═══════════════╝ │
                  │    +6-axis force        +flexible array
                  │    ┌───────────────┐    ┌─────────────────┐
                  ├───►│ CoinFT (2025) │───►│ FlexiTac (2026) │
                  │    └───────────────┘    └─────────────────┘
                  │    +low-cost hand          +full-hand skin
                  │    ╔══════════════════╗    ┌────────────────┐
                  └───►║ LEAP Hand (2023) ║───►│ DexSkin (2025) │
                       ╚══════════════════╝    └────────────────┘

2. Tactile Representation   (learning from touch)
· touch encoders
                        +cross-sensor
┌──────────────────┐    ┌───────────┐
│ Touch100k (2024) │───►│ T3 (2024) │─┐
└──────────────────┘    └───────────┘ │
                                      │    +self-supervised     +multimodal touch
                                      │    ╔═══════════════╗    ╔═════════════════╗
                                      ├───►║ Sparsh (2024) ║───►║ Sparsh-X (2025) ║
                                      │    ╚═══════════════╝    ╚═════════════════╝
                                      │    +unified encoder
                                      │    ┌─────────────────┐
                                      └───►│ AnyTouch (2025) │
                                           └─────────────────┘

3. Force-Conditioned Policies   (act on what you feel)
· force in the policy
╔═════════════════╗
║ ForceVLA (2025) ║─┐
╚═════════════════╝ │
                    │    +force-aware
                    │    recovery
                    │    ┌─────────────┐
                    ├───►│ FARM (2025) │
                    │    └─────────────┘
                    │    +scaled force VLA       +haptic feedback
                    │    ┌──────────────────┐    ┌──────────────────┐
                    └───►│ ForceVLA2 (2026) │───►│ HapticVLA (2026) │
                         └──────────────────┘    └──────────────────┘

· tactile VLA
                    +tactile
                    language          +vision-tactile    +tactile priors           +torque-aware
┌──────────────┐    ┌────────────┐    ┌─────────────┐    ╔════════════════════╗    ┌───────────────┐
│ FACTR (2025) │───►│ TLA (2025) │───►│ VTLA (2025) │───►║ Tactile-VLA (2025) ║───►│ TA-VLA (2025) │
└──────────────┘    └────────────┘    └─────────────┘    ╚════════════════════╝    └───────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

Three lanes, hardware through to policy. Tactile hardware is two independent lines — force-sensing tips ([[2105.14455|TacTip]], [[2503.19225|CoinFT]]) and whole-hand platforms ([[2309.06440|LEAP Hand]], [[2509.18830|DexSkin]]) — that never merged. Representation forks at [[2406.13640|T3]] into self-supervised encoders ([[2410.24090|Sparsh]]) and a unified tokenizer ([[2502.12191|AnyTouch]]). Force-conditioned policies split a recovery offshoot from [[2505.22159|ForceVLA]]'s own successor line, while the tactile-VLA thread is a straight ladder adding one modality at a time.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2021 | [[2105.14455\|TacTip]] | Tactile Hardware | A decade-spanning review of the Soft Biomimetic Optical Tactile (SoftBOT) sensor family |
| 2023 | [[2309.06440\|LEAP Hand]] | Tactile Hardware | A **$2,000** direct-driven anthropomorphic hand with a novel Universal Abduction-Adduction Mechanism preserving |
| 2024 | [[2406.03813\|Touch100k]] | Tactile Representation | A touch-language-vision dataset (100,147 entries) with multi-granularity NL |
| 2024 | [[2406.13640\|T3]] | Tactile Representation | A Transferable Tactile Transformer (T3) with sensor-specific ViT encoders, a shared trunk, and task decoders |
| 2024 | [[2410.24090\|Sparsh]] | Tactile Representation | SSL touch foundation model: frozen/finetuned encoder reusable across tasks via MAE / DINO / JEPA over **460k** unlabeled |
| 2025 | [[2502.12191\|AnyTouch]] | Tactile Representation | A unified static-dynamic tactile representation over the multi-sensor TacQuad dataset |
| 2025 | [[2502.17432\|FACTR]] | Tactile VLA | A Force-Attending Curriculum Training method that decays visual corruption (blur, downsampling) over training to *force* |
| 2025 | [[2503.08548\|TLA]] | Tactile VLA | A Tactile-Language-Action model that integrates sequential tactile-image streams with NL via Qwen2-VL + LoRA on **24,000** |
| 2025 | [[2503.19225\|CoinFT]] | Tactile Hardware | A coin-sized capacitive 6-axis force/torque sensor (20 mm, 2 g, ~$11) joining two rigid PCBs by silicone-pillar arrays |
| 2025 | [[2505.09577\|VTLA]] | Tactile VLA | A Vision-Tactile-Language-Action model for insertion built on Qwen2-VL with Vision-Guided Temporally Enhanced (VGTE) tokens |
| 2025 | [[2505.22159\|ForceVLA]] | Force-Conditioned Policy | 6-axis F/T at wrist: aggregated force/torque vector, **$200–2k** off-the-shelf |
| 2025 | [[2506.14754\|Sparsh-X]] | Tactile Representation | SSL touch foundation model: extends Sparsh to multisensory fusion (image+audio+IMU+pressure) over **~1M** unlabeled contacts |
| 2025 | [[2507.09160\|Tactile-VLA]] | Tactile VLA | At low-level controller: hybrid position-force / admittance control regulates the policy's output |
| 2025 | [[2509.07962\|TA-VLA]] | Tactile VLA | A systematic when/where/how ablation of motor-current torque integration in pretrained VLAs |
| 2025 | [[2509.18830\|DexSkin]] | Tactile Hardware | High-coverage tactile skin: dense contact pressure map across end-effector |
| 2025 | [[2510.13324\|FARM]] | Force-Conditioned Policy | At low-level controller: a dual-mode controller switches free-space position control and closed-loop force control at contact |
| 2026 | [[2603.15169\|ForceVLA2]] | Force-Conditioned Policy | 6-axis F/T at wrist: aggregated force/torque vector, **$200–2k** off-the-shelf |
| 2026 | [[2603.15257\|HapticVLA]] | Force-Conditioned Policy | As predicted/distilled signal: tactile token predicted from vision/state, no sensor needed at inference |
| 2026 | [[2604.28156\|FlexiTac]] | Tactile Hardware | High-coverage tactile skin: dense contact pressure map across end-effector |

> [!tip] Three Phases, One Architectural Convergence
> Across all three phases, the field converged on the same architectural pattern: **force gets its own encoder, its own attention path, and its own gated expert** — never naive concatenation with visual tokens. From [[2507.09160|Tactile-VLA]]'s force-aware action expert to [[2505.22159|ForceVLA]]'s FVLMoE to [[2603.15169|ForceVLA2]]'s Cross-Scale MoE, the consistent finding is that contact dynamics require dedicated parameters that activate phase-aware (free-space vs in-contact). See [[04_VLA#7. Multi-Sensor & Force-Aware VLAs]] for how this fits the broader VLA design space.

---

## Part A — Foundations & Sensing

*The design space (where force enters, what sensors deliver what) and the tactile sensors themselves as a sensing modality.*

### 1. Design-Space Principles

> [!info] Survey Anchor
> [[2504.03515|Dexterous-IL-Survey]] (2025) is the standing reference for the broader landscape this note carves out: it systematically reviews Behavioral Cloning, IRL, GAIL, Hierarchical IL, and Continual IL applied to dexterous manipulation; surveys end-effector hardware (simple grippers → multi-fingered anthropomorphic hands) and emphasises tactile sensing as a critical modality; details teleoperation systems and learning-from-video data acquisition; and catalogues the persistent open problems (data sparsity, generalization gaps, sim-to-real, real-time control, safety). When the present note discusses where force/tactile enters a *contact-rich VLA*, the survey covers the parallel question of how IL methods *more broadly* incorporate the same sensing modality.

Every force-aware/tactile policy commits to three orthogonal choices — *what sensor*, *where the force signal enters the model*, and *how the model is pretrained*. The interesting work in the cluster lives at the intersection of these axes; the axes themselves are *almost* independent (e.g. you can pair any sensor with any entry point), but specific combinations win specific contact regimes. The sub-sections below treat each axis as a separate decision dimension.

#### 1.1 Sensor Modality — What Force Signal You Can Even Measure

==The upstream choice that bounds everything downstream.== Sensors range from coarse aggregated F/T at the wrist (cheap, ubiquitous) to dense per-taxel skin (rich, hardware-bound). The richer the sensor, the higher the data-scale floor before a policy generalizes.

- **[[2505.06451|Adaptive-Wiping]]** — ==6-axis F/T at wrist==: aggregated force/torque vector, **$200–2k** off-the-shelf, coarse spatial info; enough for its closed-loop admittance policy to hit **100%** contact and **96%** reference force across 40 wiping scenarios.
- **[[2505.22159|ForceVLA]]** — ==6-axis F/T at wrist==: aggregated force/torque vector, **$200–2k** off-the-shelf; the coarse signal still routes through FVLMoE to **60.5%** avg SR, **+23.2%** over π0+force.
- **[[2603.15169|ForceVLA2]]** — ==6-axis F/T at wrist==: aggregated force/torque vector, **$200–2k** off-the-shelf; paired with Cross-Scale MoE + force prompts it reaches **66%** avg SR, **+48pp** over π0.
- **[[2509.18830|DexSkin]]** — ==high-coverage tactile skin==: dense contact pressure map across end-effector, **$10–30 DIY** to **thousands** for high-fidelity capacitive variants; DexSkin's **294°**-coverage grid + pneumatic calibration lifts cross-instance transfer **5/20 → 14/20** SR.
- **[[2604.28156|FlexiTac]]** — ==high-coverage tactile skin==: dense contact pressure map across end-effector; FlexiTac undercuts the range at **~$30/unit** FPC piezoresistive, running **8×16 to 32×32** layouts at **100 Hz**.
- **[[2604.20689|FingerEye]]** — ==vision-tactile fingertip==: continuous pre-contact vision + post-contact deformation in one sensor, mid-range cost (~$100s); closes the contact-discontinuity gap for **+30%** SR over wrist-camera-only.
- **[[2603.05687|CGP]]** — ==predicted tactile, no sensor==: diffusion-generated tactile trajectory translated to controller targets, compute-only; beats visuomotor and visuotactile diffusion baselines across **5** contact-rich tasks, but the no-sensor bet adds long-horizon drift risk.
- **[[2607.03529|Current-as-Touch]]** — ==motor current + joint state, no dedicated sensor==: intrinsic proprioceptive channel already present in any motor-driven hand; an ACT-style ==compliance reference position== predicts a PD target whose tracking error induces grasp force, lifting card-picking SR **55.8% → 76.9%**.

#### 1.2 Where Force Enters the Model — The Integration Axis

==The architectural choice that determines whether force is a first-class modality or a bolted-on side-channel.== The same F/T stream can be injected at the controller, the action head, the MoE gating, or the VLM prompt — and the field has converged on *late fusion above the visual backbone* as the canonical recipe.

- **[[2505.06451|Adaptive-Wiping]]** — ==at low-level controller==: hybrid position-force / admittance control regulates the policy's output; simplest and most data-efficient when reference force is known, reaching **96%** reference-force tracking and **100%** contact across 40 scenarios.
- **[[2507.09160|Tactile-VLA]]** — ==at low-level controller==: hybrid position-force / admittance control regulates the policy's output, here adjusting grip force **3.5N → 6.7N** via CoT recovery for **90%** Charger SR.
- **[[2510.13324|FARM]]** — ==at low-level controller==: a dual-mode controller switches free-space position control and closed-loop force control at contact, predicting pose+grip+force for **100%** success on dynamic screw-tightening (W1 **0.7538N**).
- **[[2507.09160|Tactile-VLA]]** — ==at action head==: dedicated F/T encoder feeds a force-aware action expert while preserving pretrained VLM representations; **90%** Charger, **80%** zero-shot wiping.
- **[[2505.22159|ForceVLA]]** — ==at action head==: dedicated F/T encoder feeds a force-aware action expert; **+23.2%** over the π0+force concat baseline.
- **[[2602.23648|FAVLA]]** — ==at action head==: dedicated F/T encoder feeds a fast-slow force-injected action expert whose variance head raises execution frequency at contact; **80.8%** avg SR (**+38pp** over vision-only).
- **[[2505.22159|ForceVLA]]** — ==at MoE gating==: FVLMoE routes between phase-specialized experts (free-space vs in-contact); full gating reaches **80%** vs **60%** naive concat.
- **[[2603.15169|ForceVLA2]]** — ==at MoE gating==: Cross-Scale MoE routes between phase-specialized experts (free-space vs in-contact); the MoE alone contributes **+26%** toward the **66%** avg SR ceiling.
- **[[2603.12665|TacVLA]]** — ==at contact-aware token gating==: tactile tokens activated *only* on contact onset, preventing free-space noise injection; **83.75%** avg SR, **>60%** under severe visual occlusion.
- **[[2601.20321|TaF-VLA]]** — ==at force-grounded latent==: tactile sequence aligned to force latent via VQ-VAE codebook, plug-and-play across sensors; **64.8%** avg SR, **60.3%** zero-shot on unseen sensors.
- **[[2603.15169|ForceVLA2]]** — ==at VLM (as prompt)==: force readings tokenized as linguistic prompts feeding the VLM for long-horizon force-aware planning; combined with Cross-Scale MoE this is the only design integrating force at all three entry points, at **66%** avg SR.
- **[[2603.15257|HapticVLA]]** — ==as predicted/distilled signal==: tactile token predicted from vision/state, no sensor needed at inference; **86.7%** mean SR on fragile-object pick-and-place, **+45pp** on egg manipulation over SmolVLA.
- **[[2505.19386|Force-Prompting]]** — ==at video backbone==: force conditioning of video generator at the pre-action stage, trained on **15–23k** synthetic force-labeled videos; force-aware *world modeling* rather than control.

#### 1.3 Pretraining Strategy — Where Generalization Comes From

==The data-axis choice that determines whether a contact policy survives task variation.== Options run from per-task from-scratch (sample-efficient, brittle) to SSL touch foundation models pretrained on **460k–1M** unlabeled contacts (data-hungry, transferable).

- **[[2505.06451|Adaptive-Wiping]]** — ==from-scratch on contact demos==: sample-efficient per task, brittle across tasks; still reaches **100%** contact and **96%** reference force in-domain.
- **[[2505.06451|Adaptive-Wiping]]** — ==unsupervised VAE tactile-encoder pretrain==: VAE/contrastive on exploratory contact, reusable within a task family; feeds the closed-loop F/T policy that beats open-loop IL (**4%**) and admittance-only (**42%**) baselines.
- **[[2603.05687|CGP]]** — ==unsupervised KL-VAE tactile-encoder pretrain==: KL-regularized VAE compresses tactile into the latent a contact-consistency mapping later reads; the resulting policy beats visuomotor/visuotactile diffusion baselines on **5** contact-rich tasks.
- **[[2410.24090|Sparsh]]** — ==SSL touch foundation model==: frozen/finetuned encoder reusable across tasks via [[2111.06377|MAE]] / [[2104.14294|DINO]] / JEPA over **460k** unlabeled tactile images; beats end-to-end training by **~95.1%** avg on TacBench.
- **[[2506.14754|Sparsh-X]]** — ==SSL touch foundation model==: extends Sparsh to multisensory fusion (image+audio+IMU+pressure) over **~1M** unlabeled contacts; **+500%** plug-insertion SR over vision-only.
- **[[2507.09160|Tactile-VLA]]** — ==VLA fine-tune with force expert==: hybrid position-force controller + CoT force recovery; **90%** Charger SR.
- **[[2505.22159|ForceVLA]]** — ==VLA fine-tune with force expert==: force-aware MoE (FVLMoE) routes F/T into dedicated experts; **60.5%** avg SR.
- **[[2603.15169|ForceVLA2]]** — ==VLA fine-tune with force expert==: Cross-Scale MoE + VLM-level force prompts; **66%** avg SR (**+31pp** over ForceVLA).
- **[[2602.23648|FAVLA]]** — ==VLA fine-tune with force expert==: fast-slow force-injected action expert; **80.8%** avg SR.
- **[[2603.12665|TacVLA]]** — ==VLA fine-tune with force expert==: contact-aware token gating, MLP tactile encoder; **83.75%** avg SR.
- **[[2601.20321|TaF-VLA]]** — ==force-grounded latent alignment==: VQ-VAE binds tactile streams to a force codebook, plug-and-play across sensors and student backbones; **10M**+ tactile-force pairs, **+6.7–33.3%** on ACT/Diffusion Policy baselines.
- **[[2603.15257|HapticVLA]]** — ==sensor-free distillation==: teacher uses tactile sensors during training, student distills to inference without them; **86.7%** mean SR on fragile-object tasks with zero inference-time tactile hardware.
- **[[2505.19386|Force-Prompting]]** — ==force-conditioned video pretraining==: latent physical understanding trained on **15–23k** synthetic force-labeled videos; transfers to control via an as-yet-unbuilt downstream action head.

**Design-Space — Decision Matrix**

| Need | Recommendation |
|---|---|
| Known reference force, single contact-rich task (wiping, polishing, insertion) | Closed-loop admittance at controller — [[2505.06451\|Adaptive-Wiping]] |
| Multi-stage task with free-space → contact transitions | Force-aware MoE — [[2505.22159\|ForceVLA]], [[2603.15169\|ForceVLA2]] |
| Dense per-taxel contact info (in-hand reorient, fragile grasp) | Hardware first — [[2509.18830\|DexSkin]], [[2604.28156\|FlexiTac]] before policy architecture |
| Continuous pre→post-contact perception (alignment, insertion approach) | Vision-tactile fingertip — [[2604.20689\|FingerEye]] |
| Reusable tactile encoder across tasks | SSL touch foundation — [[2410.24090\|Sparsh]] / [[2506.14754\|Sparsh-X]] |
| Inference-time deployment without tactile sensor | Sensor-free distillation — [[2603.15257\|HapticVLA]] |
| Cross-sensor portability for tactile signal | Force-grounded latent — [[2601.20321\|TaF-VLA]] |
| Bootstrap physical priors from video pretraining | Force-conditioned video generator — [[2505.19386\|Force-Prompting]] |

^dm-1

> [!star] Key Design-Space Papers
> - [[2603.15169|ForceVLA2]] — The only architecture to integrate force at *all three* axis-2 entry points simultaneously (controller + MoE + VLM prompt); demonstrates the cluster's architectural ceiling at **66%** avg SR, **+48pp** over [[2410.24164|π0]]
> - [[2505.22159|ForceVLA]] — The canonical late-fusion design — the field's most-copied template for treating F/T as a first-class modality through a dedicated expert and phase-aware gating
> - [[2410.24090|Sparsh]] — The cluster's pretraining-axis founder; **460k** unlabeled tactile images + ==TacBench== established that the touch analog of [[2304.07193|DINOv2]] beats end-to-end training by **~95.1%** average

^key-papers-1

> [!tip] Picking by Constraint
> If your task has a known reference force (wiping, polishing, insertion with known tolerance), use **closed-loop admittance over the action head** ([[2505.06451|Adaptive-Wiping]]) — simplest and most data-efficient. If the task is multi-stage with free-space → contact transitions, use a **force-aware MoE** ([[2505.22159|ForceVLA]], [[2603.15169|ForceVLA2]]) so the gating switches experts at contact onset. If the task requires dense per-taxel contact info (in-hand reorientation, fragile grasping), the bottleneck is **sensor hardware** ([[2509.18830|DexSkin]], [[2604.28156|FlexiTac]]) before the policy architecture matters. See [[04_VLA#7. Multi-Sensor & Force-Aware VLAs]] for how the multi-modal entry-point taxonomy fits the broader VLA design space, and [[15_Sim-to-Real-Transfer#3. Policy-Side: Robustness & Domain Randomization]] for sensor-side calibration needed before any of these axes generalize. At body scale the same constraint question is asked of distributed skin rather than fingertips — see [[12_Whole-Body-and-Locomotion-Control#1.8 Whole-Body Distributed Tactile Sensing]].

^insight-1

---

### 2. Tactile Sensors as a Sensing Modality

Hardware is the upstream bottleneck. Until 2025, dense tactile sensing meant expensive GelSight-style optical sensors (slow, bulky, single-fingertip) or hand-rolled piezoresistive arrays (brittle, inconsistent). Three sensor papers attack this bottleneck on different fronts — high-coverage skin, affordable open-source FPC, and continuous vision-tactile.

#### 2.1 Tactile Sensor Hardware — The Physical Sensing Devices

==The physical sensing devices themselves.== Hardware spans event-driven neuromorphic skins, high-coverage capacitive/piezoresistive pads, continuous vision-tactile fingertips, and coin-sized capacitive force/torque pucks, the raw signal source every SSL encoder and cross-sensor transfer method below is trained on.

- **[[2608.05725|Near-Sensor-VT]]** — An FPGA ==near-sensor computing architecture== runs a fully-pipelined ==spectral Poisson solver== for dense 3D visuotactile reconstruction on-chip, plus a ==contact-triggered protective reflex loop== bypassing the host; **0.211 ms** deterministic 128×128 latency, **>10,000 fps** throughput, **6.0×** reflex-latency cut to **28.3 ms**, **324 mW** ASIC power.
- **[[2607.28416|FasTac]]** — A curved ==RGB-NIR multispectral vision-based tactile sensor== reading 3D shape from a single RGB-IR CMOS, paired with ==HyperForce==, an FEM-inspired ==dynamic convolution network== modelling position-dependent stiffness, deployed on an ==FPGA edge platform==; **0.0415 mm** depth MAE (**−32.8%**), **2.37–2.74%** force NMAE, **1.09 ms**/frame at **100 Hz**.
- **[[2607.18660|MVP-Tac]]** — A ==miniaturized dual-modal vision + photoelastic tactile sensor== for surgical palpation, via a ==reflective circular polariscope== + ==dual-mode semi-transparent elastomer== for unblocked vision/tactile switching; **0.0511 N** MAE force (R²=0.9874), **97.37%**/**92.11%** exposed/subdermal tumor-hardness classification, **100%** in-situ colonoscopy accuracy.
- **[[2607.05241|GelNeuro]]** — A ==sensing-computing integrated neuromorphic tactile system== routes a GelSight-style front end's events directly into a Speck2f SoC's ==spiking CNN==, with ==hardware-aware synaptic weight clamping== for INT8 deployment; **96.3%** 15-class texture recognition in **80ms** at **19.6mW** (**3800x** less power than CPU), **85.2%** OOD-depth generalization.
- **[[2512.20591|LightTact]]** — A ==deformation-independent visual-tactile fingertip sensor== using a ==non-parallel optical layout== + ==composite transparent medium== blocking stray light so only true-contact scattering reaches the camera, segmented by ==frame-differencing==; detects liquid/gel/thin-film contact (**IoU>0.888**) up to **2010 Lux**, **80%** SR on VLM-guided contact inference.
- **[[2509.18830|DexSkin]]** — A ==Conformable capacitive skin== on a parallel-plate grid delivering **294° coverage** across 60 taxels at **1.7 kPa** sensitivity, **6.52%** hysteresis, **2.09%** drift/500 cycles, <$10/pair; ==Pneumatic calibration== lifts cross-instance transfer **5/20 → 14/20** SR; **19/20** perturbed pen reorient (baselines **0/20**), **90%** berry pressure cut via residual RL.
- **[[2604.28156|FlexiTac]]** — An ==open-source plug-in tactile platform== pairing thin ==FPC piezoresistive sensor pads== with an Arduino Nano + multiplexer readout at **100 Hz**, layouts **8×16 to 32×32**; ==direct electrode integration== lifts manufacturing throughput, and visuo-tactile fusion + sim-to-real fine-tune enable nut-and-bolt assembly; **~$30/unit**.
- **[[2604.20689|FingerEye]]** — A ==Continuous vision-tactile fingertip== (28×25.4×26 mm, mid-range ~$100s) with ==binocular RGB cameras==, compliant soft ring, AprilTag cover; PnP-tracked AprilTag pose proxies 6D wrench: force **[4.30, 4.22, 9.93] mN**, torque **[0.32, 0.13, 8.55] mN-m**; vision sees alignment *before* contact, tactile deformation *after*; **+30%** SR over wrist-camera-only.
- **[[2503.19225|CoinFT]]** — A ==coin-sized capacitive 6-axis force/torque sensor== (20 mm, 2 g, ~$11) joining two rigid PCBs by silicone-pillar arrays with ==dual-mode electrode switching== for normal+shear sensing; **0.16 N** force / **1.08 mNm** moment RMSE, **97 Hz** bandwidth, survives a 180 N impact — a robust cheap F/T sensor for fingers and drones.
- **[[2410.14005|WhiskerNet]]** — ==FBG whisker sensor==: pre-curved nitinol wire + dual Fiber-Bragg-Grating base-torque sensing, paired with a ==MuJoCo digital-twin== sim2real pipeline and ==GPR== real-to-sim calibration; underwater contact tracking at **<2mm** RMSE across 20 YCB objects, no robot proprioception needed.
- **[[2105.14455|TacTip]]** — A decade-spanning review of the ==Soft Biomimetic Optical Tactile (SoftBOT)== sensor family, tracing marker-tracking classifiers to ==deep-learning== pose-servo control; **93%** object classification (26 objects), **95%** grasp-success prediction, **0.7 mm** localization — the optical-tactile lineage this section's sensors descend from.

#### 2.2 Touch Foundation Models — SSL Representations on Tactile Streams

A parallel thread to better sensors: learn ==general-purpose tactile representations== via SSL on large unlabeled tactile data, then reuse the frozen encoder downstream. The touch analog of [[2304.07193|DINOv2]] — and the same lesson holds: pretrained frozen encoder beats end-to-end task-specific training by a wide margin once labels are scarce.

- **[[2607.13522|Kepler-Encoder]]** — A ==multimodal SSL embedding model== fusing vision + proprioception + F/T via ==latent-query cross-attention== + ==masked cross-modal latent prediction== (LeJEPA/SIGReg); vision-only latent recovers force **R²=0.282** (vs **0.142** control), one encoder matches per-robot specialists across **7** RH20T embodiments, **0.90** AUROC invalid-state monitor.
- **[[2607.07574|Context-Aware Force Estimation]]** — A ==LSTM contact-dynamics encoder== + ==FiLM-modulated parameter-isolated context vectors== enabling few-shot continual adaptation to new surfaces/tools with a frozen backbone; **18–63%** RMSE reduction across 9 unseen regimes, zero forgetting on the source domain (**R²=0.991**).
- **[[2607.00302|Splash]]** — Mask-isolated ==dormant-parameter-subspace== tactile alignment for sMLLMs: a ==visual-relative importance metric== isolates redundant LLM weights for touch fine-tuning while freezing boundary layers; **4.91** avg VTL score (vs UniTouch **3.74**), MMMUval **50.0->55.3**, **zero** added inference latency.
- **[[2606.30109|TacEvo]]** — LLM-driven ==Quality-Diversity architecture search== (CVT MAP-Elites) evolving VBTS perception networks via code-level mutation/crossover; discovers force-prediction architectures statistically tying an expert CNN baseline and grating-classification architectures beating it (**100%** median accuracy, all **p_adj<0.05**).
- **[[2606.19161|HT-Bench]]** — A ==dexterous full-hand tactile benchmark== pairing ~**10M** RGB + **7.8M** synchronized full-hand tactile frames with an egocentric-vision ==HandTouch== VQ encoder trained in three stages (spatial topology → vision-tactile alignment → temporal dynamics); **99.27%** Hit@1 retrieval, **0.010** RMSE / **0.911** cIoU tactile inpainting.
- **[[2606.14344|LESS]]** — A ==Local Encoder for Spatial Sensing== representing tactile scenes as spatially-local receptive fields for hand-held, real-time 3D tactile imaging of soft internal structures (fiducial-tracked, no robot needed); **85.2%** 2D reconstruction F1, **71.1%** F1 on unseen multi-inclusion phantoms (vs **44.6%** global baseline).
- **[[2507.09985|Octopi-1.5]]** — A ==Visual-Tactile-Language Model== on a ==Qwen2-VL 7B== backbone with an improved CLIP-based tactile encoder (regression + contrastive losses) and a ==Retrieval-Augmented Generation== module for on-the-fly new-object learning; **95.12%** unseen-object tactile guessing accuracy with RAG teaching, **100%/93.18%** hardness-sorting on seen balls/fruits.
- **[[2410.24090|Sparsh]]** — A ==self-supervised touch encoder== that pretrains ViTs on **~460k** unlabeled tactile images across vision-based sensors under ==[[2111.06377|MAE]]==, ==[[2104.14294|DINO]]/[[2304.07193|DINOv2]]==, and ==JEPA==, introducing ==TacBench== (6 tasks); beats end-to-end by **~95.1%** avg, latent-SSL beats pixel reconstruction, **+20–53%** bead-maze traversal.
- **[[2506.14754|Sparsh-X]]** — A multisensory touch encoder jointly encoding **4 tactile modalities** (image + audio + IMU + pressure) from Digit 360 via ==attention bottlenecks==; **~1M** unlabeled contacts, teacher-student SSL; **+17%** physical-property estimation, **+500%** plug-insertion (to **90%**) vs vision-only, **+63%** vs tactile-image-only, **90%** in-hand rotation drift cut.
- **[[2505.18361|Tactile-CRNN]]** — A ==task-optimized convolutional recurrent network== (from an ==Encoder-Attender-Decoder== sweep) that aligns with rodent ==somatosensory cortex==, *saturating* explainable neural variance and beating feedforward / state-space encoders; ==contrastive SSL== (SimCLR) matches top supervised models — evidence that *recurrence* is the right touch bias.
- **[[2505.11420|Sparsh-skin]]** — Meta's ==SSL framework== for magnetic-skin tactile sensors on dexterous hands, using ==block-masked tokenization== + ==self-distillation== student-teacher networks for full-hand touch perception; **+41%** over prior work, **+56%** over end-to-end, higher plug-insertion SR than vision-only/end-to-end visuo-tactile.
- **[[2406.03813|Touch100k]]** — A ==touch-language-vision dataset== (100,147 entries) with multi-granularity NL, paired with ==TLV-Link== curriculum pretraining transferring a vision encoder to a touch encoder via ==contrastive alignment==; **67.2%** material / **93.1%** hard-soft linear-probe, **94.5%** grasp prediction (+12.2pp), **+14pp** zero-shot rough-smooth.
- **[[2405.08576|Hearing-Touch]]** — A ==contact-audio pretraining== method reframing tactile as an audio signal from cheap ==piezo contact microphones==, pretraining an audio encoder on AudioSet via ==Audio-Visual Instance Discrimination== then fusing with R3M visual features for BC; **+23%** SR and **+76%** reward over the best baseline, ~20% (vs 60%) train-test drop on flipping.

#### 2.3 Cross-Sensor Tactile Representation Transfer

The sensor-fragmentation problem: every tactile sensor (GelSight, DIGIT, uSkin, PapillArray) speaks a different signal format, so a policy or encoder trained on one rarely transfers to another. This thread learns a *sensor-invariant* tactile representation — via shared latents, marker-image canonicalization, contrastive cross-sensor pairing, or generative signal translation — so touch knowledge amortizes across the hardware zoo rather than re-collecting per sensor.

- **[[2606.31451|UniTac]]** — A ==unified multimodal model== for cross-sensor tactile understanding *and* generation, combining ==Dual-Level Mixture Comprehension (DLMC)== with a ==Sensor-Aware DiT Projector== + ==Sensor-Prior Sampling==; **66.51** PHYSICLEAR-Test score, **0.836** SSIM tactile-image generation, cross-sensor grasp classification **50.00%->99.37%** (Digit-to-GelSight).
- **[[2606.31236|TactX]]** — Aligns vision-based, magnetic, and resistive tactile sensors (fundamentally different transduction principles, not just same-family) into a shared 16-D latent via ==contrastive + cross-reconstruction== training; transitive alignment cosine **0.928** on unpaired sensors, lifts zero-shot cross-sensor policy transfer **27.5%->45.9%**.
- **[[2606.29948|HTT]]** — A ==Heterogeneous Tactile Transformer== aligning optical (GelSight/9DTact) and array-based (Xela/TAC-02) sensors via ==MAE masked reconstruction + cross-modal alignment== on the new **1.6M**-frame ==HPT== dataset; **+12.0** macro-F1 slip detection, lifts real toy-screw SR **50%->95%**, zero-shot to unseen sensors.
- **[[2606.18959|TactSpace]]** — A ==physics-enriched shared latent space== projecting real tactile, rigid-body sim, and finite-element data through ViT encoders aligned by ==InfoNCE contrastive== + cross-modal reconstruction loss, fed by a GPU Isaac Lab tactile plugin; zero-shot sim-to-real on in- and out-of-distribution contact tasks, InfoNCE beating MSE-aligned and unaligned baselines.
- **[[2606.13102|FTP-1]]** — A ==generalist foundation tactile policy== integrating language, RGB, proprioception, and diverse tactile sensors into one action space via a ==Morphology-Aware Tactile Token Space== with sensor-specific encoders and a 300M-param ==tactile expert== pretrained on a **3,000-hr** corpus; **+17.2%** SR on seen sensors, **+31.6%** on unseen sensor setups.
- **[[2602.21625|Tacmap]]** — A ==deform map== (geometry-consistent penetration depth) closing the tactile sim-to-real gap, generated by a GPU ==ray-casting== pipeline projecting along surface normals so it stays ==geometry-agnostic== across flat and curved sensors; **0.66/0.96 mm** contact-position error, **88.21/85.67%** deform IoU, zero-shot sim-trained in-hand rotation on real hardware.
- **[[2602.09617|AnyTouch-2]]** — A ==general optical tactile representation== over a 5-tier ==Tactile Dynamic Pyramid==, unifying object-level + dynamic perception via ==frame-difference reconstruction + action matching + force prediction==, on ==ToucHD== (**2.4M** contacts, 5 sensors); **~1.2×** force prediction, **+15-20%** SR on Chip-Moving / USB-Insertion.
- **[[2510.09817|Cross-Sensor-Touch-Generation]]** — A ==cross-sensor tactile signal translation== pair: ==Touch2Touch (T2T)== conditional diffusion maps signals between sensors with paired data, and ==Touch-to-Depth-to-Touch (T2D2)== routes through a sensor-agnostic depth intermediate to drop the paired-data need; **21/30** zero-shot peg insertion, **15/20** DIGIT marble-rolling.
- **[[2506.19699|UniTac-NV]]** — A ==cross-sensor tactile autoencoder== with per-sensor encoders feeding a ==single shared decoder==, trained on ==sample-matched== paired contacts with self- and cross-reconstruction losses into a **16-D** latent; SSIM **>0.95** seen-object reconstruction, **0.353–0.397 mm** self-latent geometry error rising to **~0.6 mm** cross-sensor.
- **[[2502.19638|SITR]]** — A ==sensor-invariant tactile representation== transformer combining tactile images with sensor-specific calibration images, pretrained on **1M** physics-rendered examples (100 sensor configs) under normal-map reconstruction + geometry-contrastive losses; **81.94%** inter-sensor classification (**+33pp** over ViT), **0.80 mm** pose RMSE (~50% lower).
- **[[2502.12191|AnyTouch]]** — A ==unified static-dynamic tactile representation== over the multi-sensor ==TacQuad== dataset, combining masked-modeling pixel detail with multi-modal alignment + cross-sensor matching, and a ==universal sensor token== for unseen-sensor generalization; SOTA on material/hardness/grasp prediction and lowest fine-grained pouring error.
- **[[2410.11834|CTTP]]** — A ==contrastive touch-to-touch pretraining== framework using ==InfoNCE== to pull together tactile signals from different sensors viewing the same interaction, on a ResNet-50 encoder over paired GelSlim/Soft-Bubble data; near-random baselines beaten on cross-sensor classification, **±5°** pose error (vs ±18–38°), **18/30** real peg insertions.
- **[[2406.13640|T3]]** — A ==Transferable Tactile Transformer== (T3) with sensor-specific ViT encoders, a shared trunk, and task decoders, pretrained MAE-then-distilled on ==FoTa== (**3M+** images, 13 sensors, 11 tasks); **+24%** median classification over scratch, near-optimal pose from **2,000** points, **+25%** sub-mm insertion SR over tactile baselines.
- **[[2503.01058|GenForce]]** — A ==cross-sensor force generation== method canonicalizing raw tactile into ==marker images==, performing ==Marker-to-Marker diffusion== translation across sensors, then training a spatiotemporal force predictor with material-hardness compensation; **~100×** lower FID, **<0.92 N** normal / **<0.3 N** shear MAE across heterogeneous sensors, damage-free grasping.

#### 2.4 Tactile Data-Capture Hardware — Gloves & Teleop Rigs

The sensor papers above deliver the *signal*; this thread delivers the *capture rig* — wearable gloves and teleoperation interfaces whose contribution is hardware that records human (or teleoperated) tactile interaction at scale, closing the demonstration-data bottleneck upstream of any policy architecture. The recurring move is to put rich shear+normal sensing on the human hand (or a teleop fingertip) and stream it, with the haptic loop, into a downstream imitation policy.

- **[[2607.29231|TacPrint]]** — A **$50** wearable fingertip sensor: 24 taxel-aligned silicone protrusions + ==real-to-sim-to-real== depth-map learning (LSTM encoder, ==TacFlex== sim labels) reconstructs a dense 35x26 contact map; tactile-compensated human-to-robot replay lifts grasp success **0% → 91.67%**.
- **[[2607.09190|TactiDex]]** — A ==whole-hand tactile-kinematic-object benchmark== (162-taxel glove + OptiTrack mocap, ==tactile-constrained post-optimization==) synchronizing pressure with hand/object 6D pose across **757** sequences, **49** objects; its **TactiSkill** residual-RL tri-component reward lifts tactile-aware success **39.35% → 64.64%**.
- **[[2606.31836|RoboTacDex]]** — A ==Unitree G1 humanoid== visual-tactile-action dataset captured via VR teleop + ==hardware-software co-synchronization== of multi-view RGB-D and Brainco Revo2 tactile hands; **6,000** trajectories (**25 hr**) across **19** tasks, **23** skills, **22** objects; tactile sensing shifts (not just reduces) UnscrewBottle failure modes.
- **[[2606.26093|ForceBand]]** — A **$300** wrist-worn ==sEMG+IMU== capture rig with anatomically-guided electrode placement, training ==EMG2Force== to predict per-finger force without fingertip instrumentation; halves error vs vision-based force inference, feeds a ==flow-matching== force-augmented policy to **87%** pick-squeeze-place SR.
- **[[2606.23431|DexTeleop-0]]** — A ==force-aware bimanual dexterous teleoperation== framework pairing VR ego-centric perception, ==Project-and-Escape== retargeting, and a ==QP shared-autonomy layer== computing residual actions from localized force tracking + multi-contact force-torque balance; **97%** sim Ball-Assembly, **57.14%** real Gear-Mesh, safer force (**11.15 N**).
- **[[2602.09888|TriPilot-FF]]** — An ==open-source whole-body teleoperation rig with force feedback== where a 3-DoF ==force-feedback foot pedal== drives the mobile base and ==arm-side force reflection== conveys contact, collecting ==torque-augmented demos== feeding joint-torque into an ACT policy; **100%** BlindCarry SR (vs 55%), torque co-training lifts BasketPack **12% → 60%**.
- **[[2512.08920|OSMO]]** — An ==open-source tactile glove== using magnetic sensors to capture 3-axis normal *and* shear forces from human hands, with ==MuMetal shielding + dual-magnetometer differential sensing== cutting crosstalk (RMS noise **−57%**) and a ==Glove2Robot diffusion== pipeline; **71.69%** wiping SR vs **55.75%** vision-only, eliminating contact-failure modes.
- **[[2509.14688|exUMI]] (TPP)** — An extensible UMI-style teaching rig (AR MoCap + magnetic rotary encoder replacing SLAM/ArUco, ~100% data usability) paired with ==Tactile Predictive Pretraining==, a ==diffusion==-based action-conditioned future-tactile prediction objective; **15-55%** SR gains over vision-only, **1M+**-frame contact-rich dataset.
- **[[2507.15062|Touch-in-the-Wild]]** — A portable ==flexible piezoresistive== visuo-tactile gripper for in-the-wild data collection, with a ==masked autoencoding== + ==cross-attention== framework fusing vision+touch to reconstruct tactile from partial inputs; **2.6M** synchronized pairs across **43** tasks, Test Tube Collection **0.25→0.85** SR.
- **[[2506.01944|FTF]]** — ==AnySkin-based tactile glove== + MediaPipe keypoint triangulation captures human demos; a transformer predicts future ==embodiment-agnostic== tracks + target force, reproduced by an outer-loop ==PD controller==; **77%** SR across 5 force-sensitive tasks, zero robot training data, **67%** under adversarial disturbance.
- **[[2506.01941|FreeTacMan]]** — A wearable ==in-situ gripper== mounting visuo-tactile sensors directly on fingertips (zero mechanical attenuation) + ==NOKOV motion capture== for sub-mm pose, pretrained via ==temporal-aware multi-positive contrastive== tactile encoding; **71%** avg SR (vs **21%** vision-only), **5.05x** CPUT over ALOHA, **>3M** visuo-tactile pairs.
- **[[2505.21495|CLAMP-Haptic]]** — An open-source **<$200** reacher-grabber captures active/passive thermal, force, vibration, and proprioception + vision; crowdsourced **12.3M**-sample, **5,357**-object dataset drives visuo-haptic material recognition to **0.87** accuracy (vs **0.65** vision-only).
- **[[2504.06156|ViTaMIn]]** — A ==robot-free visuo-tactile interface== pairing a GoPro with compliant omnidirectional ==AllTact== fingers, pretrained via ==masked visual-tactile contrastive learning== aligning touch+masked vision to future vision; **100%** Orange Placement (vs **40%** vision-only Test Tube), full performance at **25%** demo data.
- **[[2504.02318|X-Capture]]** — An ==open-source portable multi-sensory capture device== pairing RGBD + tactile + microphone with explicit input-output measurements, releasing a **3,000-point** dataset across 500 objects; fine-tuning foundation models on the aligned data improves cross-sensory retrieval, with audio embeddings substituting for text prompts in localization.
- **[[2503.01301|Force-Feedback Teleop Sim2Real]]** — A scaled leader-follower rig streams ==spring-model== contact-force estimates to the operator in MuJoCo, feeding a force-conditioned ==ACT== policy fine-tuned on 8 real demos; touch/grasp/place counts (of 20) rose **0/0/0 → 17/13/12** as rendering fidelity (not physics) closed the sim2real gap.
- **[[2502.07730|DOGlove]]** — A **$600** open-source haptic teleoperation glove with ==21-DoF anthropomorphic motion capture== + ==5-DoF cable-driven force feedback== via linear resonant actuators; **±7.2°** raw / **±1°** calibrated motion accuracy, integrating directly with imitation-learning pipelines at a fraction of the $5,000+ commercial-glove cost.
- **[[2407.03162|Bunny-VisionPro]]** — A ==real-time bimanual teleoperation system== on ==Apple Vision Pro== with online hand retargeting + arm collision/singularity handling and low-cost ==FSR fingertip → ERM haptic feedback== for contact perception; **+11%** SR and **−45%** completion time over prior rigs, IL policies reaching **80-95%** seen / **50-75%** unseen-object SR.
- **[[2404.16823|HATO]]** — A low-cost ==bimanual visuotactile teleoperation== system (==HATO==) repurposing ==Psyonic prosthetic hands== (60 touch sensors/hand) with Meta Quest 2 control, training ==DDPM== diffusion policies; **10/10** slippery handover & block-stacking, **9/10** pouring, removing touch fails the transfer stage (steak serving **0/10**).
- **[[2007.09545|ContactPose]]** — A thermal-camera ==non-invasive contact-capture== dataset of **2306** human grasps (25 objects, 50 participants, **2.9M** RGB-D frames) pairing hand-object contact maps with 3D hand + object pose, avoiding instrumented gloves; PointNet++ on mesh features beats heuristic conic-distance-field contact prediction (**.772** vs **.648** AuC).

#### 2.5 Dexterous Hand Platforms — The End-Effector Hardware

Upstream of any tactile sensor or force-conditioned policy sits the *hand itself*: a high-DoF anthropomorphic end-effector whose actuation scheme (remote cable-drive, hybrid SMA-motor, in-palm linkage, learned tendon control) sets the achievable fingertip force, distal mass, and grasp repertoire. These platform papers are the mechanical substrate the contact-dynamics axis runs on — the hands that *deliver* the forces the rest of this note measures and regulates.

- **[[2607.15448|VTAP Gripper]]** — A 13-DOF three-finger gripper: Fin-Ray fingers with ==FlexiTac== 32x12 tactile arrays + a ==Visuo-Tactile Active Palm== (one camera switching vision/touch via LED-controlled mirror coating); **93.3%** tactile-reactive grasp success, singulates objects down to **3mm**.
- **[[2606.30900|CTAM Soft Tail]]** — A tendon-actuated ==Continuous Tendon-Actuated Manipulator (CTAM)== soft gripper on a quadruped tail with ==common-mode tendon actuation== decoupling stiffness from bending; effective stiffness **3.9->16.7 N/m**, **65%** higher wipe-grasp SR than a rigid gripper.
- **[[2512.24657|Antagonistic-Bowden-Cable-Actuation-Lightweight]]** — A ==remotely-actuated lightweight anthropomorphic hand== (ABCDL) using 15 ==antagonistic Bowden-cable pairs== and ==Rolling Contact Joints== so one motor drives flexion+extension; **236 g** distal mass, **20 DoF**/15 motors, **21.9 N** fingertip force, lifts a 25 kg dumbbell (100× its mass).
- **[[2507.14538|21-DOF-Humanoid-Dexterous-Hand]]** — A ==1:1 biomimetic 21-DOF dexterous hand== (CYJ Hand-0) with ==hybrid SMA-motor actuation== (15 DC-motor flexion + 17 SMA extension modules) and fishing-line tendons on a 3D-printed AlSi10Mg skeleton; **380 g**, passes all 10 Kapandji tests, **32** human gestures, **1.2 kgf** single-finger / 8 kgf hand load.
- **[[2507.03227|Dexterous-Teleoperation-20-DoF-ByteDexter]]** — A compact ==20-DoF linkage-driven anthropomorphic hand== (ByteDexter) with a 3-actuator 4-DoF thumb and a microsecond ==kinematic solver==, paired with ==optimization-based motion retargeting== of human-robot keyvectors; closer pinch fingertips and fewer collisions than DexPilot, organizing 9 cluttered items in under 5 min.
- **[[2506.07490|RAPID-Hand]]** — A ==20-DoF anthropomorphic hand platform== with a spur-bevel gear module (7N fingertip force) and whole-hand perception fusing wrist RGBD + **96-taxel** piezoresistive fingertips + proprioception under hard **≤7 ms** sync, with an ==Apple Vision Pro== teleop interface; **50/50** in-hand rolling/translation, **2.3×** MCP load tolerance over a commercial hand.
- **[[2504.13165|RUKA]]** — A ==3D-printed tendon-driven humanoid hand== with ==learning-based control== (LSTM+MLP trained on MANUS-glove motion capture) replacing joint encoders, built from open-source off-the-shelf parts; **10/10** Kapandji score, **2.74 N** pinch, **6.03 kg** payload, 40 Hz direct / 25 Hz learned control, cube-flipping demonstrated.
- **[[2309.06440|LEAP Hand]]** — A **$2,000** ==direct-driven anthropomorphic hand== with a novel ==Universal Abduction-Adduction Mechanism== preserving 4-DoF-per-finger across the full flexion range; **19.5 N** pull-out force, 1-hour **2 kg** endurance — the open-source hand platform underlying this note's LEAP-hand tactile-RL results.

**Tactile Sensors — Decision Matrix**

| Need | Recommendation |
|---|---|
| High-coverage skin for in-hand reorientation / fragile grasping | [[2509.18830\|DexSkin]] — capacitive grid, **294° coverage**, pneumatic calibration required for cross-instance transfer |
| Open-source, budget-friendly piezoresistive pad with sim-to-real path | [[2604.28156\|FlexiTac]] — **$30/unit** FPC + Kelvin-Voigt calibration; lowest barrier for community adoption |
| Continuous pre→post-contact sensing for alignment-then-contact tasks | [[2604.20689\|FingerEye]] — binocular vision-tactile fingertip; **+30%** SR over wrist-cam-only |
| Frozen tactile encoder for label-scarce downstream tasks (unimodal) | [[2410.24090\|Sparsh]] — SSL on **460k** tactile images; latent-SSL beats pixel reconstruction; ships with TacBench |
| Multisensory tactile fusion (image + audio + IMU + pressure) | [[2506.14754\|Sparsh-X]] — attention-bottleneck fusion at **~1M** contacts; **+500%** plug-insertion vs vision-only |
| Coarse aggregated F/T only (wrist-mounted) — sensor secondary | Pair with [[2505.22159\|ForceVLA]]-style policy compensation; sensor sets the eventual ceiling |
| Policy/encoder must generalize across different tactile sensor hardware | [[2502.12191\|AnyTouch]] — universal sensor token for unseen-sensor generalization; SOTA material/hardness/grasp prediction |
| Bootstrap large-scale tactile demonstration data from human hands (not teleop robot time) | [[2512.08920\|OSMO]] — open-source magnetic tactile glove + Glove2Robot diffusion; **71.69%** wiping SR vs **55.75%** vision-only |
| Need an open, budget anthropomorphic end-effector for tactile/force research | [[2309.06440\|LEAP Hand]] — **$2,000** direct-driven hand; **19.5 N** pull-out force; underlies this note's tactile-RL results |

^dm-2

> [!star] Key Papers
> - [[2509.18830|DexSkin]] — High-coverage conformable capacitive skin; the **pneumatic calibration → policy transfer** insight (5/20 → 14/20 cross-instance) is the deployment breakthrough beyond single-instance demos
> - [[2604.28156|FlexiTac]] — $30 open-source FPC piezoresistive skin with a documented Kelvin-Voigt sim-to-real path; the hardware bottleneck-breaker for the community
> - [[2604.20689|FingerEye]] — Binocular vision-tactile fingertip with continuous pre→post-contact sensing; closes the contact-discontinuity gap (**+30%** SR)
> - [[2410.24090|Sparsh]] — Foundational SSL touch encoder across [[2111.06377|MAE]]/[[2104.14294|DINO]]/JEPA on **460k** tactile images; introduces ==TacBench==; established latent-space SSL beats pixel reconstruction for touch
> - [[2506.14754|Sparsh-X]] — Multisensory touch foundation model (image + audio + IMU + pressure) at **~1M** contacts; **+500%** plug insertion over vision-only — the multimodal extension of [[2410.24090|Sparsh]]

^key-papers-2

> [!tip] Sensor Bottleneck vs Policy Bottleneck — and Why You Should Pretrain the Encoder
> The binding bottleneck dictates the fix: tasks failing at *contact onset* (alignment, insertion approach) need **continuous vision-tactile** ([[2604.20689|FingerEye]]); tasks failing during *sustained contact* (perturbed reorientation, fragile grasping) need **high-coverage skin** ([[2509.18830|DexSkin]]); tasks limited by *coarse aggregated F/T* can be compensated in policy ([[2505.22159|ForceVLA]]) but the sensor sets the ceiling. Whatever the sensor, the *encoder* should be pretrained: the [[2410.24090|Sparsh]]/[[2506.14754|Sparsh-X]] result is the touch analog of the [[2304.07193|DINOv2]] lesson — a frozen SSL tactile encoder amortizes labeling cost across the whole downstream task family, and JEPA-style objectives generalize from RGB to tactile and from unimodal to multisensory. Most VLAs in §3 still train tactile encoders from scratch per task — an obvious upgrade path. Cross-reference [[07_Latent-World-Models#3. Broader Latent Prediction Landscape]] for the latent-prediction lineage this reuses and [[02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks]] for the evaluation side.

^insight-2

---

## Part B — Force-Conditioned Policy Architectures

*How force gets injected into VLAs (Tactile-VLA, ForceVLA, TaF-VLA) and how it conditions generation models.*

### 3. Force-Conditioned VLA Architectures

The core of the cluster. Force-aware VLAs cluster along *where* force enters the network — the action head, an MoE gating module, a latent-aligned adapter, a refinement layer that handles the human/recovery loop, or upstream as video-generation conditioning. The sub-sections below treat each entry-point as a distinct architectural axis, with the bullet-per-paper detail showing how multiple groups have explored the same axis with different design choices.

#### 3.1 Force-Aware Action Heads

The most direct integration: force enters at the action expert (or its controller), giving the policy a hybrid position-force output space. These papers preserve the pretrained VLM backbone and add force capacity through dedicated parameters at the action stage.

- **[[2608.01824|ReTouch]]** — A ==Tactile-Patch Encoder== preserves finger-wise contact topology, feeding a ==Foresight/Hindsight Action Expert== pair whose future tactile latents are ==online-refined== every control step rather than fixed at chunk start; **83.6%** macro-avg SR (**+18.4pp** over the best baseline), **73.1%** under perturbations, intra-chunk refinement alone worth **+23.6pp**.
- **[[2608.01402|FACT]]** — Diagnoses why VLAs fail contact-rich tasks: a ==Logit-Normal noise schedule== redistributes flow-matching gradient toward the low-noise regime for sub-mm corrections, paired with ==Time-Aware Force Injection== (contact-state sensitivity + force history + gradient gate); **66.0%** avg SR, **+25pp** over ForceVLA, noise schedule alone **+45pp** on force-critical tasks.
- **[[2607.24485|τ]]** — A ==touch-augmented VLA== adding a ==tactile encoding and adaptation module== to a pretrained backbone, trained by a ==JEPA-style SSL branch== predicting future visual feature changes conditioned on actions at no inference cost; **71.25%** avg SR (**+40pp** over the best VLA baseline), **−20pp** without it; ships the ==TacAura== dataset.
- **[[2607.23782|N0-VTLA]]** — A ==vision-tactile-language-action== foundation model extending a VLA backbone with a ==latent tactile pathway== whose ==latent tactile tokens== predict net tactile change over future action chunks, then improved by ==ALTER== ==advantage-conditioned offline RL==; **47.2%** real NeoReal vs **29.4%** π0.5, **83.1%** UniVTAC (**+16pp**), **95%** towel-folding.
- **[[2607.14609|LTP]]** — ==Representation-aligned tactile grounding==: frozen ==linear probes== find which VLA layer best predicts future tactile state (an intermediate action-expert layer, not VLM/final-action), grounded via a training-only **Latent Tactile Predictor** ==auxiliary loss== (removed at inference); **74%**/**73%** avg SR (SmolVLA/π0), latent beats raw tactile (**80%** vs **55%**).
- **[[2607.14578|ACT Torque Proxies]]** — Ablates ACT's reliance on ==implicit leader-follower teleop force cues== via observation-centric **ACT-o** (predicts follower not leader), restored via explicit ==screw-axis motor-current torque proxies== on proprioception; ACT-o collapses (**15%** vs **60%** Base ACT), ACT-o+τ recovers **95%**, **70-80%** stiffness discrimination (vs **0%**).
- **[[2607.14236|LIFT]]** — ==Reactive action expert== grafted onto **π0.5** via ==causal force-injected cross-attention== over 6D force memory, with ==output-equivalent init== + ==zero-initialized== cross-attention preserving the VLA prior; two-stage offline-vision + online-DAgger training; **0.825** towel-folding, **0.6** book-insertion (vs **0.4**), reactive memory beats single-frame force.
- **[[2607.01067|TTP]]** — Human-centric ==tactile pre-training== extending a VLA with a ==dual-expert (action+tactile) architecture== and ==Tactile-Action Manifold-Preserving Gating==, pretrained on **160 hr** egocentric human tactile-action data (H-Tac); **96.7%** fine-grained progress vs BeingH-0.5 **57.3%**/π0.5 **43.2%**, **79.2%** contact-rich & fragile.
- **[[2606.29089|TAP-VLA]]** — ==Tactile Annotation Prompting== renders GelSight ==shear fields== as colored-line visual overlays on a VLA's own RGB inputs (no architecture change), preserving pi0.5's pretraining distribution; **78%** avg SR across 4 tasks vs **<50%** for vision-only/encoder-fusion baselines, **80-83%** on mass/center-of-mass reasoning baselines fail at chance.
- **[[2606.26423|CoStream]]** — A ==hierarchical behavior-composition== framework combining semantic (task-frame), predictive (video-WM motion), and ==reactive tactile/force residual== behaviors via a multi-rate SE(3) composer + compliant controller; **14-15/15** sub-mm assembly insertions vs **0/15** for π0.5/VoxPoser; dropping the reactive behavior collapses SR **15/15 → 3/15**.
- **[[2606.12406|FACTR-2]]** — A ==sensorless external force-sensing== method for commodity arms where ==NEXT== learns free-space inverse dynamics to estimate external joint torques as a residual, and ==FIRST== behavior cloning up-samples pre-contact/contact phases; **0.547 Nm** L1 torque error (**87.6%** below FILIC), highest avg task progress across **5** long-horizon contact-rich tasks.
- **[[2606.11743|TacCoRL]]** — A ==sim-to-real tactile-into-VLA== method augmenting a pretrained VLA with a ==dual-path tactile fusion== + ==contact-aware gate==, warm-started by sim-real co-training then refined via ==RL post-training== on simulated near-failure states; sim SR **40.5% → 78.5%**, real-world **50.0% → 72.5%** across **4** bimanual contact-rich tasks.
- **[[2605.07308|AT-VLA]]** — An ==Adaptive Tactile Injection== VLA adding tactile feedback while *preserving pretrained knowledge* (**+17%**), plus a ==Tactile Reaction Dual-Stream== for real-time contact response (**+11%**); beats SOTA VLA + tactile baselines on contact-rich tasks (Unzip Bag, Stamp, Wipe Vase) yet stays robust — reliable even when tactile input is *absent* at inference.
- **[[2605.27886|Tabero]]** — A ==vision-tactile-language gentleness== framework with a tactile-sim data pipeline, process-aware force metrics, and a ==Tabero-VTLA== with a ==decoupled force-position interface== on a hybrid controller; **0.86** firm / **0.52** gentle SR, **3.7 N** gentle grip, adverb-conditioned (firmly vs gently) force modulation.
- **[[2604.13015|Touch-Dreaming]]** — A ==Humanoid Transformer with Touch Dreaming (HTD)== policy paired with an ==RL teacher-student lower-body controller==, whose ==touch dreaming== objective predicts future hand forces and tactile latents for contact-aware representations; **+30.0pp** avg SR over ACT across **5** real contact-rich tasks, **+30%** relative gain from latent tactile supervision.
- **[[2604.01414|Adaptive-Vision-Torque-Fusion]]** — An ==adaptive vision-torque diffusion policy== whose ==Contact Gating== injects joint-torque features only on detected contact (a learnable token in free space), fused via a ==CFG-style== dual-U-Net blend with a learned torque-guidance scale; **82.0%** avg SR (**+14%**), torque gating alone lifting **30% → 68%**.
- **[[2603.08342|PhaForce]]** — A ==slow-fast visual-force policy== coordinating chunk-level diffusion planning with high-rate residual correction under a ==Contact-Aware Phase Predictor==, where ==Orthogonal Residual Injection== preserves vision semantics and a fast corrector applies phase-routed force adjustments; **86%** avg SR (**+40pp** over diffusion), **85%** OOD raised-board wiping.
- **[[2602.13689|Symmetry-Aware-VT-Fusion]]** — A ==Cross-Modal Transformer== fusing global vision with local tactile via hierarchical self-attention + cross-attention, regularized by a physics-informed ==bilateral force-symmetry== loss and processing tactile as ==residual forces== off a pre-insertion reference; **96.59%** insertion SR (vs 93.23% vision-only, 92.97% naive fusion), at **153 fps**.
- **[[2602.10013|Force-Regulated-Manipulation]]** — A ==tactile-force-controlled gripper== ($150, 0.45–45 N) with direct force-teleoperation data plus ==RETAF==, decoupling a low-frequency base policy from a high-frequency (**80 Hz+**) force-adaptation policy; **68%** avg stable-grasp (vs 38% diffusion), **60%** task SR, lifting a VLA base's tomato-pick grasp **30% → 90%**.
- **[[2602.02142|FD-VLA]]** — A ==Force-Distilled VLA== predicting a latent force token from vision + proprioception (L2-supervised by raw force, **no inference-time sensor**) and fusing it through ==directional attention masking== that preserves VLM priors; **61.1%** mean SR over 3 contact-rich tasks vs **23.3%** SmolVLA and **38.9%** with raw force, the FDM lifting **38.9% → 61.1%**.
- **[[2512.01358|Modality-Augmented Fine-Tuning]]** — ==Modality-augmented fine-tuning== of **GR00T N1.5-3B** fusing ==contact force== (dedicated encoder vs proprioceptive fusion) + ==depth== for cross-embodiment (GR1→G1) manipulation; zero-shot GR00T **0%** on G1, force early-fusion reaches **94%** SR (vs **48%** standard fine-tune); force-entry-point is embodiment-specific.
- **[[2509.18865|Bi-VLA]]** — A ==bilateral-control VLA== sourcing rich force feedback ==without dedicated sensors== via a four-channel leader-follower setup with disturbance/reaction-force observers, fusing SigLIP language + EfficientNet vision by ==FiLM== into a ==CVAE-Transformer== for action; **90%** language-disambiguable SR (vs 50% vision-only), **75%** robust in an unlearned 3-ball scene.
- **[[2509.12741|FMVP]]** — A ==Force-Modulated Visual Policy== for dressing dynamic (non-cooperative) arm motions: SAC point-cloud pretraining in sim, then ==FiLM== layers directly condition PointNet++ visual features on real force feedback for ==IQL== fine-tuning; **0.79** upper-arm dressed ratio (human study), beats force-filtering (FCVP) and vision-only.
- **[[2509.07962|TA-VLA]]** — A systematic ==when/where/how== ablation of motor-current torque integration in pretrained VLAs; decoder-side aggregated-history token wins; π0+obs+obj lifts Charger-Plugging **0/20 → 17/20**, Button-Pushing **5/20 → 18/20**, generalizes to RDT + ROKAE SR cross-embodiment.
- **[[2502.17432|FACTR]]** — A ==Force-Attending Curriculum Training== method that decays visual corruption (blur, downsampling) over training to *force* the encoder-decoder transformer to attend to external joint-torque first, paired with a mediated-force-feedback bilateral teleop rig; **87.5%** SR on unseen objects (**+43%** over vision+force), **90%** perturbation recovery.
- **[[2505.13982|AdapTac]]** — An ==adaptive visuo-tactile fusion== diffusion policy (==AdapTac==) whose ==Force-Guided Attention Fusion (FGAF)== cross-attends force embeddings against vision + tactile to reweight modalities, plus a self-supervised ==Future Force Prediction== diffusion head; **93%** avg SR (Flip **50% → 90%**), **75%** unseen-object generalization.
- **[[2505.09577|VTLA]]** — A ==Vision-Tactile-Language-Action== model for insertion built on ==Qwen2-VL== with ==Vision-Guided Temporally Enhanced (VGTE) tokens== for temporal tactile and ==Direct Preference Optimization== bridging language modeling to continuous control; **>90%** SR on unseen peg shapes in sim, beating IL + multimodal baselines, transferring to a real UR3 from sim-only.
- **[[2507.09160|Tactile-VLA]]** — A ==Multi-modal transformer== fusing vision + language + ==tactile== on a ==pre-trained VLM backbone==, with a ==force-aware action expert== outputting position *and* force under a ==hybrid position-force controller==; CoT recovery adjusts force **3.5N → 6.7N**: **90%** Charger, **90%** OOD fragile paper-box, **80%** zero-shot wiping.
- **[[2602.23648|FAVLA]]** — A ==Fast-slow VLA==: slow VLM + high-frequency ==Force-Injected Action Expert== with force adapters across transformer layers, where a VLM-predicted ==force variance head== raises execution frequency during contact; **80.8%** avg SR (**+38pp** over vision-only, **+13.8pp** over the strongest force-aware baseline); peak contact force to **7.7N** on Gear Assembly.
- **[[2510.13324|FARM]]** — A ==Diffusion policy== with explicit force action predicting robot pose, grip width, *and* target grip force, conditioned on tactile force distributions; a dual-mode controller switches position-control in free space and closed-loop force-control during contact; **100%** success on dynamic screw-tightening and superior human-demonstration force matching; W1 **0.7538N**.
- **[[2503.08548|TLA]]** — A ==Tactile-Language-Action model== that integrates ==sequential tactile-image streams== with NL via ==Qwen2-VL== + ==LoRA== on **24,000** peg-in-hole tactile-action pairs; **>85%** SR on unseen clearances (**0.3–1.2mm**) and peg geometries, **+50%** over the next baseline; cleanest tactile-grounded-language proof for high-precision assembly.
- **[[2503.03998|DP-CA-Prying]]** — A vision-force ==diffusion policy (DP-CA)== conditioning action prediction on a joint vision-force embedding via a ==cross-attention== architecture where projected force features query image features, with force-data augmentation for robustness; **96%** prying SR (vs 39% vision-only), zero-shot transfer to unseen battery types/configs.
- **[[2603.15257|HapticVLA]]** — A ==Sensor-free deployment== method via ==Safety-Aware Reward-Weighted Flow Matching==: a tactile-equipped teacher distills into a student predicting a compact tactile token from vision+state at inference — **no tactile sensor needed**; **86.7%** mean SR on fragile-object pick-and-place, **+45pp** on egg manipulation over [[2506.01844|SmolVLA]].
- **[[2603.12665|TacVLA]]** — A ==Contact-aware token gating== VLA where tactile tokens activate *only* on contact onset, preventing free-space noise injection, and a lightweight MLP tactile encoder keeps the architecture compact; **83.75%** avg SR on disassembly, **>60%** SR under severe visual occlusion (vs ~30% for vision-only).

#### 3.2 Force-Aware Mixture-of-Experts

Force-aware MoE goes beyond a single force-aware action head: a learned gating module routes between phase-specialized experts (free-space vs in-contact), so the network *switches* parameters as the task transitions. This is the field's core architectural recipe for multi-stage contact-rich tasks.

- **[[2603.15169|ForceVLA2]]** — The current SOTA force-aware VLA pushing force up to the VLM via ==force-based prompts== and down to a ==Cross-Scale MoE== fusing VLM guidance with real-time F/T for ==hybrid force-position regulation==; **66%** avg SR over 5 tasks (**+48pp** over [[2410.24164|π0]], **+31pp** over [[2505.22159|ForceVLA]]); MoE alone **+26%**.
- **[[2505.22159|ForceVLA]]** — A canonical late-fusion VLA whose ==Force-aware MoE (FVLMoE)== routes 6-axis F/T into separate experts, gating learning force-vs-visual reliance; **60.5%** avg SR (vs **37.3%** [[2410.24164|π0]]+force), **90%** under occlusion, **20%** socket insertion; full FVLMoE **80%** vs **60%** concat. Ships **ForceVLA-Data** (**244** trajectories).

#### 3.3 Force-Grounded Tactile Alignment

A distinct architectural slot: rather than aligning tactile signals to *visual* embeddings (treating touch as visual texture), these papers ground tactile observations directly in *physical interaction forces* via a learned latent space. The result is a plug-and-play adapter that ports across tactile sensors and downstream policies.

- **[[2602.13579|TactAlign]]** — A ==human-to-robot tactile alignment== method self-supervising modality-specific human/robot touch encoders, mining noisy ==pseudo-pairs== from unpaired demos via pose + binary-contact filtering, then aligning via ==rectified flow==; **72–76%** SR on pivoting/insertion/lid-closing, **100%** zero-shot light-bulb screwing, **93–99%** lower cross-sensor force error.
- **[[2602.01153|UniForce]]** — A ==unified latent force model== whose ==CVAE== learns inverse dynamics (tactile→latent force) + forward reconstruction, supervised label-free by ==quasi-static force equilibrium== during bilateral grasps over a ==unified marker-image== canonicalization + causal transformer; **r = −0.74** latent–normal-force, SOTA zero-shot cross-sensor, VLA wiping **20% → 80%**.
- **[[2601.20321|TaF-VLA]]** — A force-grounded tactile adapter: TaF-Device collects a **>10M**-pair tactile-force corpus, a ==TaF-Adapter== aligns tactile to force via ==VQ-VAE== + ==temporal encoding==, frozen and plugging into any VLA; **64.8%** avg SR (vs **37.1%** vision-only, **42.8%** tactile-vision-aligned), **60.3%** zero-shot on unseen sensors, **+6.7–33.3%** on ACT/Diffusion Policy.
- **[[2605.14571|MTNet]]** — A ==dual-stream visuo-tactile alignment network== that projects vision and touch into a ==unified latent== under cross-modal constraints, predicting contact location and force from RGB; CKA **~0.74** between modalities; ==AMTNet== extends to *human* hands *without human tactile ground truth* — structural supervision, not pressure regression.
- **[[2502.02772|Force-Language Dual Autoencoder]]** — Grounds natural-language descriptions ("gentleness") directly in force via a ==dual autoencoder== shared latent space over human force-language demonstration pairs, trained with ==reconstruction + contrastive + translation== losses; **20–30%** better force-language translation than baselines, generalizes to unseen modifiers and directions.

#### 3.4 Force-Aware Human-Intervention & Refinement Layers

A complementary architectural layer: rather than redesigning the action head, these papers wrap a VLA backbone with a refinement loop — human-in-the-loop intervention, recurrent belief state, reconstructive supervision, or phased curriculum — whose mechanism plugs cleanly into force-aware settings even when the original paper targets vision.

- **[[2607.03723|OmniTacTune]]** — A ==policy-agnostic real-world RL== pipeline learns lightweight ==tactile residual corrections== atop frozen visual base policies via ==warm-start critic bootstrapping== + a multi-sensory reward; lifts **5-40%** -> **85-100%** SR in **40-80 min**, generalizes across 5 base policies (Flow/ACT/DP/π0.5).
- **[[2606.09337|TORL-VLA]]** — A ==tactile-guided online-RL== refinement layer feeding ==tactile-derived wrench== into a ==MoE== wrench-aware VLA that emits action + future-wrench references, refined live by an RL module with an ==intervention-censored critic== removing credit-assignment bias; full-task SR **12/30 → 28/30**, beating TA-VLA and ForceVLA on a real latch-box.
- **[[2605.15157|HandITL]]** — An ==interventional correction== layer for a bimanual 56-DoF hand-arm VLA via VR controllers + data gloves, where ==relative hand retargeting== tracks configuration *changes* from the intervention onset and ==velocity-based shared arm control== smooths wrist residuals; **99.8%** gesture-jump cut on Bread Clip; on-policy intervention fine-tuning beats teleop.
- **[[2603.04038|Force-Aware]]** — ==TER-DAgger== triggers human intervention only on force-prediction-error OOD detection (**98.8%** precision at **100%** recall), then an optimization-based ==trajectory-editing== step smoothly fuses the correction into the base ACT trajectory for consistent residual supervision; **77.2%** avg insertion SR, **>37pp** over the best baseline.
- **[[2601.20239|TouchGuide]]** — ==Inference-time steering== of pretrained visuomotor policies via a contrastively-trained ==Contact Physical Model (CPM)== that adapts classifier guidance to diffusion/flow-matching actions, paired with the low-cost ==TacUMI== handheld tactile teleop rig; Diffusion Policy **16.3% → 36.2%** SR, beating RDP (**30.3%**) and Policy Consensus (**24.7%**).
- **[[2507.17294|VLA-Touch]]** — A ==training-free dual-level tactile wrapper== augmenting any frozen VLA: a ==Tactile-Language Model== (Octopi) feeds tactile property descriptions to a GPT-4o ==Task Planner==, while an interpolant-diffusion ==Tactile-Augmented Controller== refines actions from force signals; **90%** force / **75%** hardness inference, base-VLA SR up **+140%** (Wipe).
- **[[2506.16685|Compliant-Residual-DAgger]]** — ==CR-DAgger== pairs an admittance-controlled intervention interface (on-policy delta corrections, not take-over) with a lightweight force-aware residual policy predicting pose+wrench corrections atop a frozen base policy; **+60%** book-flipping and **+50%** belt-assembly SR, force modality alone worth **45-53pp** over position-only residuals.
- **[[2502.14420|ChatVLA]]** — A ==Phased Alignment Training== VLA (control first, then understanding) over ==Qwen2-VL-2B== with an MLP ==MoE== splitting a ==Control-Expert== from an ==Understanding-Expert==; recovers VQA (**71.2%** TextVQA, **9.2×** over ECoT) without sacrificing control across **25** tasks at **3.5×** fewer params; the MoE split parents [[2505.22159|ForceVLA]]'s FVLMoE.

#### 3.5 Force as Video-Generation Conditioning

A category-of-one frontier: rather than feeding force *into* a policy, force is used to *condition video generation*, then video predictions bootstrap downstream policies. This is force-aware *world modeling* rather than force-aware control — the entry-point lives upstream of the action stack entirely. Single-paper sub-section here because no other published work has attempted force-as-generation-conditioning; explicitly a frontier slot.

- **[[2505.19386|Force-Prompting]]** — A force-conditioned video generator adapting ==CogVideoX== via [[2302.05543|ControlNet]] to accept ==physics-based force prompts== (wind + pokes), trained on **15–23k** synthetic Blender + [[2404.13026|PhysDreamer]] videos; emergent ==intuitive mass understanding==, beats text-only/trajectory baselines. *Open*: force-pretrain → action head unbuilt.

**Force-Conditioned Architectures — Decision Matrix**

| Need | Recommendation |
|---|---|
| Hybrid position-force action expert, simplest integration | [[2507.09160\|Tactile-VLA]] — force in augmented action space + hybrid controller |
| Adaptive execution frequency under contact | [[2602.23648\|FAVLA]] — fast-slow VLA with force-variance-triggered cadence |
| Force-aware diffusion with explicit force output | [[2510.13324\|FARM]] — predicts pose+grip+force; **100%** dynamic screw-tightening |
| Inference-time deployment *without* tactile sensor | [[2603.15257\|HapticVLA]] — flow-matching distillation; **86.7%** fragile-object SR |
| Gate tactile tokens *only* on contact onset | [[2603.12665\|TacVLA]] — contact-aware token gating; **83.75%** disassembly SR |
| Multi-stage task with free-space → contact transitions | [[2603.15169\|ForceVLA2]] (SOTA, **66%** SR) or [[2505.22159\|ForceVLA]] (canonical, **60.5%** SR) |
| Cross-sensor portability via force-grounded latent | [[2601.20321\|TaF-VLA]] — VQ-VAE on **10M** tactile-force pairs; **60.3%** zero-shot |
| Cross-domain (robot ↔ human) visuo-tactile alignment | [[2605.14571\|MTNet]] + AMTNet — CKA **~0.74**; vision-only human-touch response |
| Human-in-the-loop intervention + on-policy refinement | [[2605.15157\|HandITL]] — relative retargeting, **99.8%** gesture-jump reduction |
| Recurrent belief over force history | [[2511.18960\|AVA-VLA]] — POMDP recurrent state (force-specific variant pending) |
| Phased curriculum to avoid VLM forgetting under force fine-tuning | [[2502.14420\|ChatVLA]] — control-first, then understanding |
| Force-as-pretraining-signal for downstream policy | [[2505.19386\|Force-Prompting]] — only force-conditioned video generator extant |

^dm-3

> [!star] Key Papers
> - [[2603.15169|ForceVLA2]] — Cross-Scale MoE + force prompts; current SOTA for force-aware VLA at **66%** avg SR, **+48pp** over [[2410.24164|π0]]
> - [[2505.22159|ForceVLA]] — Force-aware MoE; the foundational late-fusion-with-phase-aware-gating architecture; **+23.2%** over force-concat baselines
> - [[2507.09160|Tactile-VLA]] — Force in augmented action space + Chain-of-Thought failure recovery; **90%** Charger, **80%** zero-shot blackboard wiping via autonomous force adjustment
> - [[2601.20321|TaF-VLA]] — Force-grounded tactile alignment via VQ-VAE on **10M** tactile-force pairs; the cleanest demonstration that *grounding tactile in physical force* (not visual texture) is what unlocks VLA contact-rich performance; plug-and-play with **6.7-33.3%** gain on ACT/Diffusion Policy baselines
> - [[2502.14420|ChatVLA]] — Phased Alignment Training + control/understanding MoE; the architectural parent of force-aware MoE designs

^key-papers-3

> [!tip] Generation vs Control — The Unbuilt Pipeline
> [[2505.19386|Force-Prompting]] answers *"what would happen if I applied this force?"*; [[2507.09160|Tactile-VLA]] and [[2505.22159|ForceVLA]] answer *"what force should I apply right now?"*. The two halves compose: pretrain on force-conditioned generation to absorb mass/dynamics priors, then attach a force-aware action head for control. No published work has executed this end-to-end yet. See [[08_Physics-Aware-Embodied-AI#3. Explicit Physics Losses for Video Generation]] for the broader physics-conditioned video-generation track and [[06_WAM#5. VLM-Integrated WAMs]] for the WAM augmentation patterns that would host the action head. The generative-policy backbones these force heads bolt onto are surveyed in [[10_Manipulation-Skill-Learning#1. Generative Policy Architectures]].

^insight-3

---

## Part C — Evaluation

*Contact-rich manipulation benchmarks — the downstream targets the force-conditioned policies of Part B race against.*

### 4. Contact-Rich Manipulation Benchmarks and Visuotactile Policies

The downstream targets of all this work. Contact-rich tasks — wiping, polishing, insertion, in-hand reorientation, fragile grasping, multi-finger jar opening — define the benchmarks the field is racing against. The papers below cluster along three contribution axes: ==vision-to-tactile prediction== from egocentric data (closes the tactile-supervision bottleneck), ==contact-grounded policies== built around generative tactile forecasts, and ==long-horizon memory== that turns single-contact policies into sustained-contact ones.

#### 4.1 Vision-to-Tactile Prediction — Closing the Supervision Bottleneck

==The pretraining-axis breakthrough for the benchmark frontier.== Contact-rich tasks have been data-starved because instrumented teleoperation rigs are expensive; predicting tactile from RGB unlocks egocentric-scale supervision.

- **[[2608.06192|HOPE (Hand-Object Pressure Estimation)]]** — Unifies glove/planar pressure and distance-based contact into a common ==MANO per-vertex space==, predicted by ==VertexFormer== (spatial-temporal attention + ==contact-gated force prediction==) from monocular human-hand video; **F1 0.874** / **1.808 kPa** MAE on OpenTouch, ARCTIC F1 **0.069 → 0.498** with HOI supervision.
- **[[2607.20683|FELT]]** — An ==attention-based cross-modal generative network== synthesizing per-finger pressure images from frozen ==DINOv2== features via a ==tactile query decoder== + ==gated cross-panel exchange==; beats MAE/NN baselines (LPIPS **0.191**, Energy Ratio **1.123**), matches real-tactile SR, and hits **90%** vs **70%** on Triangle Peg Insertion at **~20ms** latency.
- **[[2607.01684|TacImag]]** — A frozen ==conditional DDPM== generates ==imagined tactile observations== (TacRGB/TacFF) from vision+proprioception at deployment, eliminating physical tactile hardware; sim **57.5%** (vs **58.2%** real TacFF, **53.6%** vision-only), **+44.4pp** real-world contact-sensitive tasks.
- **[[2606.29173|TacGen]]** — A ==V+T contrastive alignment== framework (symmetric InfoNCE over frozen ==DINOv2==) paired with a ==latent-space residual-MLP V→T generator== synthesizing tactile features rather than pixels; mass-regression **ΔR²=+0.570**, TACTO manipulation SR **0.246→0.979**, generated latents matching real-tactile utility.
- **[[2605.13083|TouchAnything]] (EgoTouch)** — A ==vision-to-tactile prediction== framework from egocentric video alone; **20 hr** multi-view ego + bimanual 3D hand pose + dense pressure maps from RGB; ==view dropout== cuts the ego-only penalty **−27.20% → −5.78%** Volumetric IoU (**+6.1%** over ego-only) — first bridge from egocentric VLA pretraining to *dense* tactile supervision.
- **[[2603.15847|FEEL]]** — A ==force-enhanced egocentric dataset== pairing Project Aria video with a ==custom piezoresistive glove== (**~3M** force-synced frames, **27 hr**, 45% contact) and deriving per-frame contact labels from filtered force, with ==force-prediction SSL== pretraining; **95.6%** binary-contact accuracy, **+4.85/+6.26pp** EPIC-Kitchens verb/noun under frozen eval.
- **[[2512.04884|Hoi!]]** — A large-scale ==force-grounded multimodal dataset== of articulated-object interaction (synced vision, pose, force, tactile) exposing how badly in-the-wild estimation degrades: Sparsh tactile-force RMSE jumps to **3.86–4.11 N** (from millinewtons), ForceSight visual-force to **2.23 N** (from **0.404 N**) — the reality-check for force prediction.
- **[[2510.14117|ViTacGen]]** — A ==vision-to-touch generation== method for pushing where ==VT-Gen== synthesizes tactile contact-depth images from visual sequences and ==VT-Con== fuses them with vision + proprioception under attention + ==MoCo contrastive== RL, sim-only with domain randomization; **80-86%** sim, **86%** real mug-pushing (vs 10% vision-only), **75.2%** unseen-object zero-shot.

#### 4.2 Contact-Grounded Policies — Generative Tactile Forecasts as Policy Anchors

==The architectural answer to "how do you ground a contact-rich policy without an OXE-scale corpus".== Three complementary strategies: pretrained encoder + closed-loop F/T (sample-efficient), diffusion over coupled state+tactile (long-horizon), and MoE-with-curriculum (generalist coverage).

- **[[2608.03103|DPA-FTG]]** — A hierarchical ==slow-fast== IL pairing a 5Hz diffusion Task Selection Policy over a ==VQ-VAE== latent-primitive vocabulary with a 60Hz ==GRU== Motion Generation Policy (decoder-initialized, force-feedback fine-tuned) generating force-modulated motion; **100%** chiseling task success at **27.7N** peak force vs [[2503.02881|RDP]]'s **33.3%**/**44.7N**.
- **[[2607.04234|SoftVTBench]]** — An Isaac Sim ==FEM soft-body== benchmark for deformable-object manipulation pairing simulated GelSight Mini tactile with a dual ==Goal Success / Safety Success== protocol; visuo-tactile lifts Safety Success **21.4%->35.6%** (Object-Soft), P95 deformation **44.70%->38.81%**, exposing a persistent Goal-Safety Gap.
- **[[2606.29941|ViTacMotor]]** — A unified visuo-tactile policy pairing ==Tactile Motion Correlation (TMC)== (dot-product of transient x cumulative gel-motion, resolving contact-state ambiguity) with a ==Mixture-of-Transformers== fusion; **86.7%** whiteboard erasing, **73.3%** tube collection, beating TactileACT/ACT/DP baselines.
- **[[2603.08560|CONTACT-Disassembly]]** — A ==tactile-representation study for disassembly== over 5 sim + 5 real tasks comparing ==TacRGB== images vs a compact ==TacFF tactile force-field== from a GelSight R1.5 under a ==Diffusion Policy==; Vision+TacFF wins (real vertical-clip **15% → 55%**, **55%** under dim light vs 0%), while naive TacRGB+TacFF fusion *degrades*.
- **[[2602.13833|SCFields]]** — ==Semantic-Contact Fields==: a 3D representation fusing category-level visual semantics with dense extrinsic contact-probability + force-vector estimates, conditioning a ==3D diffusion policy== via a two-stage sim-to-real pipeline; **79.6%** SR on unseen scraping tools (**84.7%** cleaning efficiency), ablating force estimates drops efficiency to **27.6%**.
- **[[2602.01939|EFM-10]]** — A ==bimanual active-perception benchmark== formalizing Exploratory-and-Focused Manipulation over 10 tasks with a ==BAP strategy== using a non-operating arm for eye-in-hand vision and the operating arm's **6D F/T** for tactile compliance, plus **1850-demo BAPData**; force sensing lifts delicate tasks (Light-Plug **20% → 36.7%**) and cuts max vertical force **~29%**.
- **[[2510.14930|VT-Refine]]** — A ==real-to-sim-to-real bimanual assembly== policy pretraining a diffusion policy on limited real demos then ==RL-finetuning== in parallel sim, with a custom ==FlexiTac== sensor + GPU viscoelastic tactile sim and a ==unified point-cloud== fusing vision, tactile, proprioception; RL lifts real visuo-tactile SR **~40%** over vision-only, up to **0.98** sim SR.
- **[[2508.20561|SimShear]]** — A true sim-to-real tactile pipeline: ==shPix2pix== (shear-vector-conditioned U-Net GAN) generates shear-enabled synthetic tactile images so ==ShearNet== (GDNN pose/shear estimator) trains sim-only and deploys zero-shot; **MAPE 0.091** (vs pix2pix's 0.22), **1-2mm** tactile-tracking/co-lifting contact error.
- **[[2506.15953|ViTacFormer]]** — A ==cross-modal visuo-tactile CVAE== on the ==ACT== architecture fusing high-res vision + tactile via ==cross-attention== with an ==autoregressive tactile prediction head== forecasting future contact, stabilized by ==two-phase curriculum==; **~50%** higher SR on short-horizon dexterous tasks, **80%** on an 11-stage hamburger task (**0.88** HNS).
- **[[2506.13762|VITAL]]** — A ==generalizable visuotactile policy== pairing few-shot visuotactile ==behavior cloning== with online ==residual RL==, a ==Segment-Anything-2 semantic augmentation== pipeline, and a ==Molmo VLM== coarse-localizer over a fine local policy; **+40%** avg over the strongest baseline, **28/30** novel-position plug-in, tactile adds **+40%**.
- **[[2505.06451|Adaptive-Wiping]]** — A ==VAE-pretrained-on-exploratory-F/T + few-shot IL + closed-loop F/T== policy for deformable-sponge wiping under unseen heights/stiffnesses; **100%** contact, **96%** reference force across 40 scenarios; vs **4%** open-loop IL and **42%** admittance baselines — the cleanest data-efficient contact-rich benchmark, bounded to tightly-scoped tasks.
- **[[2503.02881|Reactive-Diffusion-Policy]]** — A ==slow-fast hierarchical IL== policy where a ==Latent Diffusion Policy== plans + an ==Asymmetric Tokenizer== reacts on high-freq tactile/force; **+35%** over Diffusion-Policy baselines, **0.90–0.95** peeling SR, **0.8 vs 0.15** under perturbations; paired ==TactAR AR-teleop== improves stable-contact-force ratio **0.58 → 0.87**.
- **[[2411.06408|Visuotactile-Insertion]]** — A ==teacher-student visuotactile== policy for compliant underactuated hands lacking proprioception, distilling a privileged PPO teacher into a Transformer student fusing segmented point clouds with AllSight tactile images; **95%** zero-shot real insertion (vs **80%** visual-only) across 11 object-socket pairs including 6 novel objects.
- **[[2408.17061|Robotic-Object-Insertion]]** — A ==sim-to-real privileged teacher-student== policy for soft-wrist peg insertion: an RL teacher with full state trains in a custom MuJoCo soft-wrist model, distilled to a TCN student on wrist pose + 6-axis F/T only; **100%** zero-shot circular-peg insertion, **70%** zero-shot generalization to an unseen square peg.
- **[[2603.05687|CGP]]** — A ==Conditional diffusion over coupled state + tactile trajectories== policy: a ==KL-regularized VAE== compresses tactile, then a learned ==contact-consistency mapping== (needs *both* state + tactile) translates predictions into ==compliance-controller== targets; beats visuomotor + visuotactile diffusion on **5** tasks (jar opening, in-hand box flipping) in real time.
- **[[2502.14420|ChatVLA]]** — A ==MoE + Phased Alignment Training== *generalist* contact-rich baseline with strong results across **25** real-world tasks, showing that even general-purpose VLAs can absorb a substantial fraction of contact-rich tasks with the right training curriculum.
- **[[2603.19201|OmniVTA]]** — A ==hierarchical slow-fast visuo-tactile framework== stacking a ==TactileVAE==, a ==Visuo-Tactile World Model==, an ==Adaptive Fusion Policy==, and a **60 Hz** ==Reflexive Latent Tactile Controller (RLTC)==; trained on **OmniViTac** (**21,000+** trajectories, **86** tasks); SOTA on 6 real tasks; RLTC lifts SR to **60%** Wipe / **63%** Peel under perturbation.
- **[[2409.16451|ARCH]]** — A ==hierarchical hybrid== assembly framework: ==motion planning== primitives for free space + ==reinforcement learning== (F/T-conditioned) for contact-rich insertion, orchestrated by a ==Diffusion Transformer== high-level policy from just **10** demonstrations; **55%** SR (vs **20-25%** hierarchical baselines), zero-shot **8**-object generalization (**80%** SR).
- **[[2307.06423|Bi-Touch]]** — An affordable ==bimanual tactile manipulation== platform (two MG400 arms + ==TacTip== sensors) extending Tactile Gym 2.0 for bimanual tasks, trained via PPO with ==GAN tactile image translation== + a ==Goal-Update Mechanism== for sim-to-real; robust Bi-Pushing/Bi-Reorienting/Bi-Gathering on unseen objects, recovers from perturbations via touch.
- **[[2207.10763|Tactile Gym 2.0]]** — Extends the Tactile-Gym sim-to-real ==GAN image-translation== framework across three low-cost optical sensors (TacTip, DIGIT, DigiTac) on a **$2.7k** Dobot arm, showing one zero-shot RL recipe generalizes across sensor types; SSIM **0.982-0.996** real-to-sim, **9-16mm** pushing / **0.6-1.8mm** edge-surface-following error, foundation Bi-Touch later extends.
- **[[2106.08796|Tactile-Real-to-Sim-GAN]]** — A ==tactile sim-to-real policy transfer== method training ==PPO== on simulated ==contact-geometry depth images==, then bridging with a ==pix2pix real-to-sim GAN== translating real images into the sim format for ==zero-shot transfer==; **4/5** tasks transfer (edge/surface following, rolling, pushing), **0.9955** SSIM, **1.09–1.58 mm** edge error.
- **[[2011.11270|COCOI]]** — A ==deep Q-learning== non-planar-pushing policy with ==Contact-aware Online Context Inference== that samples history only when contact force exceeds a threshold, inferring latent contact dynamics, bridged to real via a ==RetinaGAN== sim-to-real GAN; **90%** real push-in-bin SR, **+50%** relative over baseline, robust to OOD mass/friction and unseen objects.

#### 4.3 Long-Horizon Memory — Sustained-Contact Reasoning

==The temporal-axis missing piece for force-aware tasks.== Current force is meaningless without history ("am I still pressing, or did I just transition into free space?"). Memory architectures from broader VLA work plug in directly.

- **[[2603.01700|TacMamba]]** — A ==Mamba-based tactile history compressor== bridges **100Hz** reflexes with ~1Hz VLA reasoning as an O(1)-latency soft prompt, avoiding LSTM forgetting; **100%** sequential button-pressing SR vs π0.5's collapse to **0%** and MemoryVLA's **58%** ceiling.
- **[[2508.19236|MemoryVLA]]** — A ==Perceptual-Cognitive Memory Bank (PCMB)== dual-memory VLA: low-level perceptual details (recent F/T, contact events) + high-level cognitive semantics (task progress); **+26pp** over [[2503.22020|CogACT]] on real-world long-horizon temporal tasks (**83%**) at only **+3.6%** latency, **+0.8 GB** GPU; not force-specialized, but maps cleanly onto force history.

#### 4.4 Tactile World Models — Forecasting Future Contact State

==The world-modeling answer to reactive contact policies.== Rather than acting on current tactile readings, these models *predict* future tactile/contact state in a compact latent — turning a reactive policy into an anticipatory one. Force precedes tactile change, so a force-conditioned forecast gives the policy a head-start on the contact transition.

- **[[2608.19574|HiTac-WAM]]** — ==Hierarchical Tactile Forecast== (contact → deformation → slip, ==stop-gradient==-conditioned) ranks action candidates and triggers ==KDE-calibrated== online replanning; real-robot SR **31.1% → 72.2%** across chip grasping, erasing, USB insertion.
- **[[2608.00547|OVTF]]** — Disentangles WAM prediction accuracy from the ==future-to-action interface== via an oracle future provider; ==Asymmetric Phase-Local Future Memory (AFM)== routes phase-aligned visual context into tactile memory slots (cross-tactile access blocked); **32.0%** avg SR vs **23.7%** for modality-isolated routing (**+8.3pp**) and **14.9%** for the UniVTAC-ACT* baseline.
- **[[2607.24267|FeelWorld]]** — A ==hierarchical tactile state model== predicting contact state, 3D tactile latent, and slip probability, fused by ==contact-gated asymmetric attention== that admits touch only on predicted contact, feeding a ==contact-aware CEM planner==; **98.6%** contact / **83.4%** slip F1, **81.7%** zero-shot SR vs **49.2%** visual-only.
- **[[2607.23783|N0-TWAM]]** — A ==tactile-native world-action model== on a ==video-diffusion transformer== jointly flow-matching video, tactile, and action through a ==Mixture-of-Transformers==, coupling tactile ==foresight== with ==reactive== conditioning; **84.5%** UniVTAC (**+17pp**), **46.3%** real vs **30.0%** π0.5, **45%** vs **25%** under visual perturbation.
- **[[2607.22530|ViTacWorld]]** — An ==action-conditioned visuo-tactile world model== whose ==view-aware Diffusion Transformer== uses ==stream identity embeddings== + ==cross-view attention== to generate synchronized multi-view visual and tactile futures; rollout augmentation lifts real tactile-policy SR **42.5% → 67.5% → 80.0%**, doubling as an evaluator within **10pp** of real SR.
- **[[2607.07287|TouchWorld]]** — A hierarchical predictive-and-reactive tactile foundation model separating a **1Hz** Subtask Planner, a ==Tactile World Model== predicting contact subgoals, and a **30Hz** ==Tactile Residual Transformer== atop a frozen VLA; **65.0%** clean / **53.7%** perturbed SR (**+15.7/+18.5pp** over FTP-1), **86.3%** temporal contact accuracy.
- **[[2607.02503|VT-WAM]]** — A visual-tactile World Action Model jointly flow-matching visual, tactile-deformation, and action prediction via ==Asymmetric MoT Attention== (first-frame visual anchor + full tactile sequence) and ==Contact-Gated AVTAG== hinge-loss; **71.67%** avg SR (**+26.67pp** over Fast-WAM), wipe-vase ablation **40%->70%->85%**.
- **[[2606.31723|UniTacVLA]]** — Unifies tactile understanding and prediction in a VTLA policy via ==Tactile Chain-of-Thought (T-CoT)== reasoning + ==coarse-to-fine future tactile prediction== + an ==action-tactile mixed controller==; USB task ablation **30%->36%->52%->62%**, **20-30pp** gains under perturbation over TacVLA baselines.
- **[[2606.30988|MuSe]]** — A ==Multi-Sensory World Model== adapting a pretrained video-action policy (UVA) to new force-torque sensing via ==multi-stage fusion== + ==multisensory future prediction==, with ==experience replay== preventing catastrophic forgetting; **11.5/15** vase wiping, **13/15** peg insertion, plus backward-transfer gains on original vision-only tasks.
- **[[2606.26663|Tactile-WAM]]** — A ==touch-aware World Action Model== jointly predicting future visual latents, tactile contact states, and action chunks, where ==Tactile Asymmetric Attention (TAAM)== with a VIDEOCLEAN mask protects the visual pathway and a touch-aware bias anchors denoising to contact transitions; **44.7%** sim (**+38.9pp** over RGB-only DreamZero), **51%** real (**+33pp**).
- **[[2606.13877|ContactWorld]]** — A ==JEPA latent world model== + 12-task benchmark studying which visuo-tactile representation (spatiality, continuity, contact-sensitivity) best supports ==receding-horizon MPC== planning; point-cloud + ==tactile force-field== reaches **36.1%** avg planning SR (vs **20.7%** wrist-image), tactile gains growing with goal offset (16.0% → **20.5%** at 48 steps).
- **[[2606.11184|TacForeSight]]** — A ==force-guided tactile world model== (TacForceWM) forecasting short-horizon tactile latents from high-frequency wrist ==force/torque== as a leading indicator (~**200 ms** lead), feeding a ==flow-matching== policy via cross-attention + tactile-guided gating; **79.0%** avg completion, **86.7%** under perturbation, MSE **0.017** at **20 Hz**.
- **[[2606.08737|Dream-Tac]]** — A ==unified tactile world action model== on a ==video Diffusion Transformer== jointly predicting future vision, tactile, and action, with ==Contact-Aware Self-Attention (CASA)== amplifying sparse tactile during contact plus FlashBias + step-caching for speed; **83.3%** avg SR over **6** tasks (**+31.6%** over Cosmos-Policy), **2.9×** train / **1.8×** inference.
- **[[2606.08555|FAWAM]]** — A ==Force-Envisioned Action Model== jointly predicting future actions and end-effector wrenches on a video-WAM backbone, refined online by a ==Force-Guided Residual Corrector== reacting to predicted-vs-sensed wrench discrepancy; **85%** avg SR (**+36.25pp** over vision-only, **+21.25pp** over force-aware baselines) across 4 tasks.
- **[[2603.23481|VTAM]]** — A ==visuo-tactile world action model== projecting multi-view vision + tactile into a shared VAE latent under a ==multi-view diffusion== video transformer, with ==deformation-aware regularization== (a 3D virtual-force proxy from tactile optical flow) preventing modality collapse; **90/85/95%** SR on chip-pick / cucumber-peel / wipe, 0% without virtual-force reg.
- **[[2602.06001|VT-WM]]** — A multi-task ==Visuo-Tactile World Model== fusing pretrained ==Cosmos== vision + ==Sparsh-X== tactile encoders through a 12-layer autoregressive transformer predicting future visuo-tactile states; **~33%/29%** lower Fréchet distance (moving/static), **+35%** zero-shot planning SR, **77%** after 20-demo finetune.
- **[[2601.12796|Contact-Aware-Neural-Dynamics]]** — A ==two-stage neural dynamics model== first predicting future contacts with a ==contact predictor==, then object-pose trajectories with a ==diffusion pose predictor== conditioned on them, grounded in binary tactile signals + ==implicit sim-to-real alignment==; MSE **0.0082**, ADD-S **88.23%**, **73.7%/64.7%** single/multi-object SR.
- **[[2509.26642|MLA]]** — A ==multisensory language-action model== repurposing ==LLaMA-2 7B== to directly tokenize 2D images, 3D point clouds, and tactile via encoder-free shallow-layer ==token-level contrastive alignment==, with multisensory ==future-state forecasting== (image + point-cloud + tactile) in post-training; **+12%** over π₀ / **+24%** over SpatialVLA real-world, **81%** RLBench avg.
- **[[1903.04128|Deep-Tactile-MPC]]** — A ==deep predictive tactile model== training a ==recurrent ConvNet== on exploratory interactions to forecast ==future GelSight observations==, then planning touch-only actions via ==MPC + Cross-Entropy Method== to a goal tactile image; **86.6%** die-rolling SR, **2.10 mm** ball-repositioning L2 — the foundational tactile world model for contact control.

#### 4.5 Visuotactile Policies — Arm & In-Hand

The general visuotactile-policy bucket: end-to-end policies fusing touch with vision and proprioception, spanning arm- and gripper-level bimanual manipulation through multi-finger in-hand reorientation, fragile grasping, and dexterous insertion. Tactile ranges from primary (vision-free blind grasping, often distilled from a privileged-state sim teacher) to complementary (visuotactile policies where touch covers occlusion and regulates grip and rotation).

- **[[2607.13479|Sparse-Touch Mesh Reconstruction]]** — A ==topology-agnostic grid-query cross-attention== estimator reconstructs full deformable-object meshes (rope/cloth/soft-body) from sparse noisy touch, no vision; cuts error **~66-80%** vs GPIS/IDW baselines; a ==deep-ensemble== uncertainty drives a learned next-touch acquisition policy.
- **[[2607.04940|Dexterous Force-Based Grasping Sim-to-Real]]** — A sim-to-real ==asymmetric actor-critic PPO== pipeline pairs a fast ==Mooney-Rivlin tactile sim== with data-driven ==current-to-torque calibration== + randomized actuator modeling; zero-shot force-adaptive grasping to **93.92 N**, **25.1** consecutive in-hand rotation successes on real XHand.
- **[[2606.27344|VibeAct]]** — Maps real ==vibro-acoustic== piezoelectric-microphone signals to a compact physically-grounded ==contact-onset/slip== representation via a ==digital-clone== auto-labeling pipeline, letting sim-only RL policies exploit vibrotactile feedback; **+51pp** Cube Rotation, **+24pp** Peg-in-Hole, sim-to-real on a LEAP hand.
- **[[2606.24450|NoContactNoWorries]]** — A ==vision-proprioception contact estimator== for in-hand dexterous manipulation: a causal Transformer fuses ego RGB-D with current + commanded proprioception via ==pose-conditioned cross-attention== for binary fingertip contacts — no tactile sensor; **0.9** sim / **0.71-0.84** real F1, predicted-contact policies match oracle at **8 ms**.
- **[[2606.22332|Tactile-Genesis-Exploring]]** — A GPU-parallel ==tactile simulation platform== (7 sensor abstractions incl. a novel temperature grid) scaling to **20k+** envs, ablating placement/type/resolution via teacher-student RL+DAgger; palm+phalange coverage beats fingertip-only, per-taxel force/torque a robust default, sim-to-real on XHand1 in-palm rotation.
- **[[2606.17055|T-Rex-Tactile]]** — A ==tactile-reactive dexterous manipulation== framework pairing a 100-hr tactile-synced bimanual dataset with a ==Mixture-of-Transformer-Experts== splitting low-frequency visuomotor planning from high-frequency tactile refinement via ==asynchronous cascaded flow matching==; **65%** avg SR over 12 tasks (+30pp over EgoScale), **−23%** without tactile.
- **[[2606.11767|Blind-Dexterous-Grasping]]** — A ==tactile-only Real2Sim2Real== grasping policy with no vision or pose, where a ==Real2Sim== binary-contact calibration aligns onset/offset timing and a ==privileged-supervised layout-aware tactile encoder== feeds an expert-to-==Diffusion Policy==; **27%** real SR over **20** objects on LEAP Hand; pretraining lifts sim seen **36.2% → 60.4%**.
- **[[2605.28812|CoP-Tactile]]** — A physics-grounded ==Center-of-Pressure== contact representation (3D force + 3D location) with a ==differentiable taxel↔CoP mapping== and dynamics-based calibration; **0.78** peg-in-hole across 6 shapes, robust OOD, with emergent in-hand reorientation.
- **[[2605.21429|roto-2.0]]** — A ==GPU-parallelized tactile-RL benchmark== (Isaac Lab) standardizing "blind" dexterous manipulation across four hand morphologies on Bounce and Baoding tasks with a customized ==PPO== (observation-stacking, 8,092 envs); tactile-only blind agents hit **80** bounces and a SOTA **13** Baoding rotations in 10 s, setting a new tactile-intelligence ceiling.
- **[[2605.05241|DexSim2Real]]** — **FM-DR**: a ==VLM realism critic== scores rendered-vs-real frames, ==CMA-ES==-optimizing domain-randomization distributions; feeds **TVCAP**, a bidirectional cross-attention visuo-tactile PPO policy; **78.2%** avg real SR across 6 dexterous tasks, **8.3%** sim-to-real gap, zero real demos.
- **[[2604.01224|SoftAct]]** — A ==two-stage force-aware retargeting== algorithm transferring VR-captured human demos (kinematics + contact patches + forces) to non-anthropomorphic ==soft robot== hands via a ==learned pneumatic controller==; **55–75%** lower translational error, **85%** vs **35%** pouring SR, **95%** vs **30%** bulb-screwing SR over kinematic baselines.
- **[[2603.28475|Tac2Real]]** — A ==PNCG-IPC== GPU visuotactile simulator (multi-node ==Ray== cluster, marker-displacement fields) paired with **TacAlign**, four-stage sim-real calibration (controller-gain, ==CMA-ES== material fitting, task-based tuning, domain randomization); online-RL policy inserts an **8mm** peg zero-shot at **91.7%** real SR.
- **[[2603.00446|HydroShear]]** — A ==hydroelastic shear simulator== for vision-based tactile sensors decomposing marker displacement into dilation/shear via ==recursive force tracking== + ==SDF==-tracked object motion, calibrated by ==system identification== of 4 physical parameters; beats TacSL/FOTS on shear-simulation accuracy, **93%** avg zero-shot sim-to-real SR across 4 contact-rich tasks.
- **[[2603.04531|PTLD]]** — A ==Privileged tactile latent distillation== method for sim-to-real: an ==Asymmetric Actor-Critic== trains a ==privileged-sensor policy== (external-camera pose) in *one* sim stage, then a ==tactile encoder== matches real tactile + proprioception via ==DAgger==; **+182%** in-hand rotation, **+57%** reorient goals, ~**50%** lower 6D pose error (**0.43 → 0.21** rad).
- **[[2602.07326|Blind-Grasping]]** — A ==vision-free multifingered grasping== teacher-student method where an ==RL teacher== with a ==force-incentive reward== learns blind grasping from privileged state, distilled to an IL ==Transformer== student on only 9-DoF joints + **3 uniaxial fingertip forces**; **98.3%** real grasp SR over 18 objects (97.5% OOD) vs 37.2% partial-obs RL.
- **[[2602.05513|DECO]]** — A ==Decoupled Multimodal Diffusion Transformer== for bimanual dexterous manipulation with separate vision / proprioception / tactile pathways and a two-stage ==plugin tactile adapter== (cross-attention + LoRA); **82.50%** avg SR (**+21pp** over DP), **73.13%** on contact-rich Waste-Disposal/Assembly (**+53.75pp**) at ~10× fewer params; releases **DECO-50** (50 hr).
- **[[2602.05468|TaSA]]** — A two-phase ==tactile sensory attenuation== framework where a ==Self-Touch FCN== predicts self-generated tactile from joint positions, then a frozen-FCN-conditioned ==LSTM== attenuates predictable self-touch from raw tactile; r **0.96–0.98** self-touch prediction, **95% vs 70%** paper-clip / **92% vs 68%** coin insertion over a raw-tactile baseline.
- **[[2509.23075|In-Hand-Articulated-Tools]]** — A ==privileged-oracle-to-student== in-hand articulation policy trained with curriculum force-torque perturbations, then ==Cross-Attention Tactile Force Adaptation (CATFA)== fuses whole-hand tactile + motor torque with action intent online; **100%** SR across **5** articulated tools, **0.0 mm** clamp gap, lower pose deviation.
- **[[2509.22421|Bimanual-Tactile-Reactive-MPC]]** — A ==collaborative multi-agent MPC== for bi-manual tactile-reactive grasping where each arm's ==GelSight Mini== image is compressed into a ==differentiable MPC layer== with ==learnable cross-arm coupling==; up to **10/10** stable grasps across objects vs single-agent/PD baselines, only **45%** runtime overhead.
- **[[2509.15934|UniTac2Pose]]** — A unified ==energy-based diffusion model== for visuotactile in-hand pose estimation/tracking/uncertainty, trained sim-only via a ==render-compare== architecture comparing real tactile to CAD-rendered hypotheses; **2.1mm** ADD/ADD-S (vs **13-16mm** baselines), category-level generalization to unseen objects, **10Hz** tracking.
- **[[2509.07445|Text2Touch]]** — An ==LLM-designed-reward== tactile in-hand manipulation method (Eureka-adapted) generating + refining reward functions from task/environment context, with teacher-student sim-to-real to a real Allegro Hand + ==TacTip== sensors; LLM rewards are ~10× simpler yet **+38%** rotations/episode and 25% longer episodes over a human-engineered baseline.
- **[[2508.14441|FBI]]** — A ==dynamic visuotactile shortcut policy== for in-hand manipulation modeling the tactile↔object-motion causal link via a dynamics-aware latent, whose ==Flow2Tactile== module predicts dense contact from visual flow (a sensor-free ==Vision-Only== mode) under a one-step ==flow-matching shortcut==; **66.5%** sim / **35.0%** real SR (**+16-18pp**) at **17-34 ms** inference.
- **[[2506.12239|ViTaSCOPE]]** — A ==visuo-tactile implicit representation== fusing visual point clouds with high-resolution tactile shear fields via an SDF ==Object Module== + shear-field ==Tactile Module== + extrinsic-contact ==Contact Module==, trained entirely in sim; **4.049 mm** / **0.907°** real-world in-hand pose error (vs ICP's **43.0 mm** / **78.6°**), zero-shot sim-to-real.
- **[[2506.02353|SAVOR]]** — ==Visuo-haptic skill-affordance learning== for bite acquisition: a VLM sets commonsense food-property priors, refined online by ==SAVOR-Net== (RGB-D + F/T + pose LSTM), while calibrated ==tool affordances== gate a VLM skill-planner; **87.3%** SR3 (vs **73.4%** FLAIR), **51.5%** attempt efficiency, generalizes to **10** unseen foods.
- **[[2505.01974|KineDex]]** — A ==tactile kinesthetic-teaching== framework collecting force-enriched demos via ring-shaped finger straps + a modified ==PD== controller, training an ==inpainting-based visuomotor policy== that removes human-hand occlusions to prevent domain shift; **74.4%** avg SR across nine contact-rich tasks at **>2×** faster data collection than teleoperation.
- **[[2504.05287|RobustDexGrasp]]** — A ==zero-shot dynamic dexterous grasping== framework distilling a visual-tactile privileged teacher to a single-view-depth student via mixed IL+RL curriculum, with an ==LSTM tactile-contact reconstructor== from noisy proprioception substituting for direct touch; **94.6%** real SR on 512 novel objects, **84.0%** under 2.5 N external forces.
- **[[2503.19893|Visuo-Tactile]]** — A ==visuo-tactile object-pose tracker== fusing vision with **binary low-resolution** in-hand tactile via ==factor-graph optimization== under hand-configuration geometric constraints that reject impossible poses, on a 15-DoF hand with 16 tactile pads; real-time **13.3 Hz**, markedly better than vision-only accuracy under heavy occlusion.
- **[[2503.07926|Gentle-Grasping]]** — An ==end-to-end action-conditional== gentle-grasping framework fusing vision, ==DIGIT touch==, and sound on an Allegro Hand, with ==self-supervised gentleness labels== from sound thresholds, optimizing regrasps under a learned gentleness constraint; **79%** stable-and-gentle SR (**+17pp** vs vision-only, **+44pp** vs chance), **88.24%** prediction accuracy.
- **[[2503.01078|KineSoft]]** — ==Kinesthetic teaching== for underactuated soft hands: a ==FoldingNet==-based shape-estimation model reads strain sensors into per-vertex mesh deformation, driving a shape-conditioned diffusion policy; **1.92mm** shape error (**-41.3%**), **85%** bottle-unscrewing vs **0%** for a strain-tracking baseline.
- **[[2502.17434|V-HOP]]** — A ==unified haptic representation== converting taxel- and vision-based tactile signals + gripper kinesthetics into a coherent point cloud, fused with FoundationPose visual features via a ==transformer== for adaptive visuo-haptic 6D pose tracking; **32%** lower ADD-S than NeuralFeels at **~10x** speed (**32 FPS**), **80%** bimanual-handover SR (vs **40%** vision-only).
- **[[2410.24091|3D-ViTac]]** — A ==unified 3D visuo-tactile== bimanual policy concatenating 3D visual point clouds with dense 3D tactile point clouds (16×16 ~$20/pad resistive skin) into a ==PointNet++ diffusion policy==; **85%** Egg-Steaming / **90%** Hex-Key vs 50-65% vision-only, dense+continuous tactile beating sparse/binary, tactile covering visual occlusion.
- **[[2407.18834|Shape-Conditioned-Tactile-Agent]]** — A single ==shape-conditioned RL== in-hand reorientation agent on tactile-only (torque + position) feedback, encoding shape via pose-transformed ==Basis Point Sets== and co-training a recurrent state estimator via ==Estimator-Coupled RL==; OOD novel-object reorient matching object-specific SOTA, zero-shot sim-to-real, **−30%** SR without shape.
- **[[2405.07391|AnyRotate]]** — A ==gravity-invariant in-hand rotation== policy via ==teacher-student distillation== (privileged PPO teacher → real-observation student) with ==dense sim-to-real tactile features== (contact pose + force magnitude); zero-shot multi-axis 6D reorientation under continuous arm motion, with emergent reactive grasp re-stabilization absent in binary-touch policies.
- **[[2402.04820|Contact-Rich Hand Retargeting]]** — A kinematic retargeting framework transferring contact-rich human demos to diverse target hands via ==atlas-based logarithmic-map shape matching== of contact areas + multi-stage ==IK==/==cubic B-spline== fitting; **30** retargets over **5** hands × **6** objects beat DexPilot/keypoint-IK on contact fidelity, no dynamics sim needed.
- **[[2309.09979|RotateIt]]** — A ==vision+touch in-hand rotation== method training a sim oracle on ground-truth object properties then a ==visuotactile transformer== inferring them from depth + discretized contact locations; continuous multi-axis rotation on a real AllegroHand, OOD gap cut **41% → 15%** with vision+touch (shape encoding 22%→8%).
- **[[2309.07350|Curriculum-Sensing-Sim2Real]]** — ==Curriculum-based Sensing Reduction (CSR)== gradually strips tactile features from an actor's observation, while a ==Deep Random Generator (DRG)== replaces removed signals with re-initialized random noise (vs zeroing) to fully decouple dependencies; **58%** real Allegro-hand block-rotation SR at 10Hz, beating one-step Asymmetric-Actor-Critic.
- **[[2303.03486|SBRL]]** — A ==sampling-based-exploration RL== method seeding ==Asymmetric Actor-Critic PPO== with ==G-RRT reset distributions== from full-dynamics sim so a tactile-and-proprioception-only actor learns finger-gaiting reorientation of concave objects; real-robot multi-revolution L-shape reorient (median **1.5 rev**), tactile essential on hard objects.
- **[[2504.16649|PP-Tac]]** — A ==tactile paper-picking== method integrating a fabricable monochrome vision-based ==R-Tac== fingertip sensor into an Allegro hand with a ==diffusion policy== executing sliding/pinching to buckle paper, plus slip-based force control + randomization; **0.35 mm** depth MAE, **87.5%** grasp SR across paper-likes on flat/sloped/uneven terrain.
- **[[2504.15595|Cross-Modal-Visuo-Tactile-Grasping]]** — A ==SAC== deformable-object grasping method with a ==Cross-modal Spatio-Channel Attention== module fusing segmentation masks + tactile pressure images, under a reward encouraging stable contact-area grip and penalizing breakage; highest SR across basic/random/unseen settings, all multimodal variants beating a failing visual-only baseline.
- **[[2210.04887|In-Hand-RMA]]** — A ==Rapid Motor Adaptation== in-hand z-axis rotation policy trained in sim on cylinders only, with an adaptation module predicting a low-dimensional ==extrinsics== vector online from ==proprioception alone== (no vision/touch); direct sim-to-real on an Allegro Hand rotating **30+** unseen objects, **23.96** avg rotations on heavy objects, beating DR and sys-ID.
- **[[2112.06442|Deep-Predictive-Vision-Tactile]]** — A ==deep predictive learning== model fusing vision (CNN), tactile, and joint angles to predict future states/actions with a ==point-based attention== robust to occlusion + ==Softmax Transformation== for fine joint prediction; **93.3%** bag-unzip SR (vs 16.7% vision-only), **86.7%** under heavy occlusion (0% vision-only), lower fingertip loads.

#### 4.6 Contact-Safe Force Control

The safety-critical face of contact: regulating interaction force so fragile objects survive and unexpected collisions don't damage the robot or scene. These methods wrap a force/contact controller with explicit safety machinery — control-barrier functions, momentum-observer collision detection, or hybrid contact-mode models — rather than trusting an end-to-end policy to stay gentle.

- **[[2606.14188|Robust-Deformable-MPC]]** — A ==certified deformable manipulation== framework pairing a GPU-parallel differentiable rope/cloth simulator (contact smoothing for non-vanishing gradients) with a ==SLS robust output-feedback MPC== whose dynamics + perception bounds are ==Conformal-Prediction==-calibrated; **100%** safety, **0.758 s/step** 300-DoF cloth folding, hardware-validated.
- **[[2606.10818|IMPACT-Internal-Model]]** — An ==internal-model predictive control== framework for forceful manipulation that learns online to estimate slow external wrenches (payload weight) from ==joint-torque residuals==, fed as feedforward into an impedance loop while a diffusion policy plans kinematics; near-**100%** sim SR over 0-10 kg, **21/25** real on 5 kg trained only on 2.5 kg.
- **[[2605.20392|VBT-MPC]]** — A ==vision-based tactile MPC== for contour following that regulates contour features from a marker-less VBTS directly (no pose estimation, no cascaded force controller), fed by a ==Unet++ line-fitting (NNaLF) + EKF== pipeline at 50 Hz; **<0.51 mm** orthogonal-distance RMSE, **~1.0 s** faster settling, tracking contours where baselines lose contact.
- **[[2604.06133|Force-Feedback-MPC]]** — A ==force-feedback MPC for deburring== augmenting state with contact forces and regulating normal + tangential force via a 3D contact model, guided by a ==Diffusion Transformer motion prior== seeding collision-aware references into the local optimizer; **100%** multi-hole deburring SR with obstacle avoidance, normal-force RMSE as low as **4.40 N**.
- **[[2509.18447|PrioriTouch]]** — Personalizes whole-arm pHRI contact: ==LinUCB-Rank== contextual bandit learns to rank pose-tracking vs per-body-part force-regulation objectives, executed via ==Hierarchical Operational Space Control== null-space projection, refined in a ==simulation-in-the-loop== digital twin; preferred by **7/8** users over a heuristic baseline.
- **[[2504.08238|CATCH-FORM-3D]]** — A dual-loop ==PDE-driven observer== (Kelvin-Voigt/Maxwell reduction + spatial diffusion) fuses vision-tactile to estimate viscoelastic material params online, driving an ==admittance== outer loop + ==reaction-diffusion== inner loop; **0.68-0.85mm²** deformation error, force error **<5%** across five material hardnesses, no per-object retuning.
- **[[2412.10349|SafeDiff]]** — A ==diffusion-based state-planning== policy whose ==Tactile-Guided Calibration Module== cross-attends real-time force feedback to implicitly recalibrate vision-guided door-opening trajectories; **80-81%** SuR seen/unseen doors, **SaR-80@10N 78.73%** (vs **43.12%** baseline), **100%** few-shot sim-to-real SuR with 20% real data.
- **[[2411.07833|DOBCBF-Grasping]]** — A ==tactile + CBF-safety== grasping framework with a fingertip contact-force controller and ==disturbance-observer-based CBF== filters enforcing force-bound + force-closure constraints under a ==Kelvin-Voigt== contact model from electromagnetic tactile; safe grasping of fragile glassware where standard CBF fails, **83.5%** less conservatism than robust CBFs.
- **[[2211.02443|Robotic-Assembly-Control]]** — A ==Model-Hybrid Compliance Control== reconfiguration pairing ==Equivalent Theory of Compliance Law (ETCL)== parameter transfer with ==Weighted Dimensional Policy Distillation (WDPD)== transfer RL across peg-in-hole geometries; WDPD yields the lowest average force/moment among RL-enhanced controllers.
- **[[2207.13438|Contact-Safe-RL]]** — A ==hierarchical contact-safe== framework pairing a 60 Hz image-based RL policy with a 1 kHz ==contact-aware controller==, using a ==momentum observer== to estimate arm contact torques and switching free-space/contact modes via ==variable impedance== + null-space projection; wiping forces **<5N**, **~3×** lower collision force, **<1 cm** error under pushes.
- **[[2203.02468|Predicate-State-Estimation]]** — A ==Bayesian symbolic state estimator== for contact-rich tasks that classifies atomic binary ==predicates== from multimodal vision + force as ==virtual sensors== fused via GMM under conditional independence; **0.92** offline accuracy, **0.80** unseen-task accuracy (vs 0.38 direct), and **0.72** online insertion SR over a hand-tuned baseline.
- **[[1909.04915|Hybrid-GP-Contact-Model]]** — A ==hybrid-automaton contact dynamics model== identifying discrete modes + reset maps via ==Dirichlet-Process GMM== with ==Gaussian-Process== mode dynamics, propagating uncertainty by Unscented Transform + Monte-Carlo over guard functions; lowest NLL/RMSE on a 7-DOF YuMi contact task, capturing velocity jumps during slip from only **15** trials.

#### 4.7 Model-Based & Sampling-Based Trajectory Optimization for Contact-Rich Manipulation

==The classical-planning answer to the same benchmarks==, sidestepping learned policies entirely: differentiable-physics MPC, augmented-Lagrangian CITO solvers, and generative-prior-bootstrapped sampling controllers race the same PushT / in-hand-reorientation / insertion tasks that the rest of this note's learned policies target, several validated on real hardware (Panda, IiwaBimanual, AllegroHand, Spot).

- **[[2608.11731|ContactIPM]]** — A ==structure-exploiting primal-dual interior-point solver== for contact-implicit trajectory optimization: ==barrier-coupled elastic relaxation== of complementarity pairs + stage-local slack elimination via backward ==Riccati recursion==; **2.17-8.87x** faster than CRISP, **150/150** IMPACT cases, **50/50** closed-loop Push Box at **2.08ms** median solve.
- **[[2608.09166|CaPTURe]]** — ==Particle-based conformal prediction== over a robot's next configuration: samples particles from an approximate dynamics model, scores by k-NN distance, calibrates per-==Mondrian== group via a ==LOCART== regression tree over state/action/contact-stratum; holds **90%** coverage in every contact mode, lifts an ==MPPI== planner's peg-insertion SR **48% → 78%**.
- **[[2607.25053|ECE]]** — Inverts the collision-free premise: ==Environmental Constraint Exploitation== treats deliberate contact as a dimensionality reducer, sequencing =='manipulation funnels'== along contact manifolds in ==CERRT/ConCERRT== and partitioning ==belief space== by touch; **7-D** policies at **σ_m = 0.1** noise, insertion deviation **7cm→2cm**, **100%** granular-pile grasps.
- **[[2607.09218|TACTIC]]** — A ==contact-aware sampling-based MPC== (MPPI) fusing RGB-D + tactile via a ==hybrid predictive model== (ViT dynamics + kinematics) and ==contact-Jacobian-biased sampling==; **87.2%** SR / **39.0** force violations in sim (vs 64.1%/108.3 latent-only), real Side Rollover **12/20** vs **3/20** Diffusion Policy; open Kinova tactile-exoskeleton hardware.
- **[[2606.20712|Parallel-Sampling-MPC]]** — A JAX/MuJoCo-MJX ==Hydrax== SMPC framework deploying ==Model Tensor Planning== (global tensor-path + local Gaussian samples) on real hardware; escapes multimodal traps where MPPI/CEM/PS fail, lowest pose error on real-robot Push-T, finds contact-initiation domain-randomization params more informative than global physics params.
- **[[2605.09127|IMPACT-Active-Set]]** — An ==augmented-Lagrangian== CITO solver treating complementarity as hard constraints inside a ==Block Coordinate Descent== inner solve (closed-form active-set selection per contact pair); **100%** SR + **13.8x** geo-mean speedup over CRISP/SR/PM baselines, **100%** real-Panda pushing (10/10), **91.8%** Allegro-hand CI-MPC with lower control variance.
- **[[2605.07215|PISTO]]** — Reframes ==STOMP== as implicit forward-KL variational inference, then adds a ==proximal trust-region== penalty yielding derivative-free closed-form mean updates via importance-weighted Monte Carlo; **88.57%** motion-planning SR (vs **67.59%** STOMP), up to **2.8x** reward on contact-rich MuJoCo (PushT, HumanoidRun) at **1.4-3.2x** speedup.
- **[[2604.27175|KernelSOS]]** — ==Global-MPPI== combines ==graduated non-convexity== (Log-Sum-Exp smoothing) with ==KernelSOS== global surrogate exploration and auto-calibrated ==MPPI== local refinement to escape the local minima that trap vanilla MPPI/CEM on PushT and LEAP-hand in-hand reorientation; lower final cost/variance, matching DIAL-MPC's best cost in half the iterations.
- **[[2510.19974|Push-Anything]]** — ==C3+== enhances Contact-Implicit MPC with a ==slack-variable complementarity reformulation== decoupling the projection step into closed-form per-contact sub-problems (**4-5 orders of magnitude** faster than C3); paired with a real-time perception pipeline (FoundationPose+XMem), **98%** SR over **928** hardware trials, 33 objects, up to 4-object decluttering.
- **[[2510.14643|Generative-Sampling-MPC]]** — ==GPC-CEM== bootstraps online sampling-based MPC by mixing an offline ==conditional flow-matching== proposal (trained directly on noisy SPC rollouts) with the live CEM distribution; **99.8%** sim Push-T SR, **96%** zero-shot Push-K generalization, **60%** real-Spot chair-pushing SR vs **10%** for plain CEM.
- **[[2509.20917|Long-Range-Contact]]** — Attacks vanishing contact gradients at the source: a ==globally supported log-barrier potential== stays twice-differentiable and non-vanishing even for separated bodies, evaluated near-linearly via a ==Bounding Sphere Hierarchy==; finds multi-stage Billiards/Push/Sort motions from trivial inits where IPC, SDRS, GB stall, **O(T²)→~O(T)** (**0.6→3.18 s**).
- **[[2505.12214|CA-OED]]** — ==Contact-Aware Optimal Experimental Design==: derives a ==Contact-Aware Fisher Information Matrix== from a ==Contact-Aware MAP== problem embedding object parameters in contact dynamics, synthesizing trajectories that maximize it closed-loop; emergent human-like exploration (hefting for mass, rubbing for friction, pinching for stiffness), robust to sensor noise.
- **[[2505.04978|RT-Motion-Contact]]** — A ==robust model-based in-hand manipulation== framework pairing a ==contact-implicit MPC== planner over smoothed contact dynamics with a ==tactile-feedback tracking controller== compensating modeling errors at execution; real-time on 5 real tasks (rotation, door opening), holding precision under disturbances, beating baselines on force tracking.
- **[[2505.02291|Contact-Trust-Region]]** — The ==Contact Trust Region (CTR)== augments differentiable-physics Taylor expansions with primal/dual contact-feasibility constraints (friction cone, non-penetration) feeding an iterative MPC; robust hardware reorientation on IiwaBimanual/AllegroHand, offline roadmaps built in **<10 min** for long-horizon dexterous goals.
- **[[2505.00647|GeoDEx]]** — A ==unified geometric framework== representing force equilibrium/constraints via planes, cones, ellipsoids, projecting noisy tactile readings onto a ==Force-Equilibrium plane== solved by ==quadratic programming== + tracked by an ==admittance controller==; **14x** faster force planning than SOCP, higher grasp SR than raw sensor readings.

**Contact-Rich Benchmarks — Decision Matrix**

| Need | Recommendation |
|---|---|
| Pretraining tactile supervision *without* instrumented teleoperation | [[2605.13083\|TouchAnything]] — vision-to-tactile prediction from egocentric RGB |
| Single contact-rich task with known reference force | [[2505.06451\|Adaptive-Wiping]] — closed-loop F/T + VAE; **96%** reference force |
| Long-horizon multi-contact task (jar opening, in-hand flip) | [[2603.05687\|CGP]] — diffusion over coupled state + tactile |
| Generalist VLA covering many contact-rich tasks at once | [[2502.14420\|ChatVLA]] — MoE + Phased Alignment across **25** tasks |
| Sustained contact requiring force-history reasoning | [[2508.19236\|MemoryVLA]] — PCMB dual-memory (force-history specialization pending) |
| Bench against OXE-scale corpus for contact-rich tasks | **(no such benchmark exists yet)** — see [[02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks]] |

^dm-4

> [!star] Key Papers
> - [[2605.13083|TouchAnything]] — Multi-view egocentric + dense bimanual tactile dataset (**20 hr**) and vision-to-tactile prediction framework; **+6.1%** Volumetric IoU over ego-only; view dropout closes ego-only inference gap to **−5.78%**; first bridge between egocentric video pretraining and dense tactile supervision
> - [[2603.05687|CGP]] — Generative contact grounding via diffusion over coupled state+tactile trajectories; outperforms visuomotor/visuotactile diffusion baselines on **5** complex contact-rich tasks (jar opening, in-hand box flipping)
> - [[2505.06451|Adaptive-Wiping]] — Few-shot IL + F/T feedback + VAE object representation; **100% contact**, **96% reference force** under unseen heights/sponges; the cleanest contact-rich benchmark to date

^key-papers-4

> [!tip] Benchmark Frontier
> Most contact-rich benchmarks today (ForceVLA-Data, ForceVLA2-Dataset, [[2505.06451|Adaptive-Wiping]] scenarios) involve hundreds to ~1k trajectories on 5–25 task variants. None approach the scale of [[2310.08864|OXE]] (**1M+** trajectories). Until an "[[2310.08864|OXE]] for contact-rich tasks" exists, force-aware policy performance is bounded by *data scale*, not *architecture* — which is why [[2605.13083|TouchAnything]]'s vision-to-tactile prediction path matters disproportionately: it bypasses the instrumented-teleoperation cost ceiling. See [[02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks]] for the broader benchmark landscape and [[14_Egocentric-Pretraining-and-Human-Video#3. Scaling Laws for Egocentric Pretraining]] for the scaling-law evidence underwriting this argument. For §4.3's [[2508.19236|MemoryVLA]] and its dual-memory bank in the broader cross-domain memory context, see [[09_Robot-Memory#1.3 Episodic & Compression Memory for Manipulation]].

^insight-4

---
## Part D — Open Problems

*Where the contact-sensing / force-conditioned half of the axis still fails.*

### 5. Open Problems & Failure Modes

Despite the architectural convergence in §3, the force-aware cluster has unresolved bottlenecks. The seven problems split cleanly into three categories: *data & calibration* (the corpora and sensor-calibration infrastructure that doesn't yet exist), *architecture & tokenization* (how to feed continuous F/T into VLM-scale backbones), and *deployment & failure recovery* (millisecond-fast contact transitions that current reasoning latencies can't match).

#### 5.1 Data & Calibration

The data scarcity is the dominant root cause: no force-aware OXE, no cross-sensor calibration protocol, and no vision-tactile-language pretraining corpus at web scale.

- **==Cross-sensor transfer remains brittle==** — A policy on one [[2509.18830|DexSkin]] needs ==pneumatic calibration== to reach another; cross-modality transfer ([[2509.18830|DexSkin]] → [[2604.28156|FlexiTac]]) is untested. [[2410.24090|Sparsh]]/[[2506.14754|Sparsh-X]] add SSL portability; [[2601.20321|TaF-VLA]] reports **60.3%** zero-shot cross-sensor transfer via ==force alignment==.
- **==No "[[2310.08864|OXE]] for force-aware tasks"==** — [[2505.22159|ForceVLA]]'s ForceVLA-Data (**244 trajectories**) and [[2603.15169|ForceVLA2]]'s **1,000-trajectory** dataset are the largest publicly available force-instrumented datasets — orders of magnitude smaller than cross-embodiment visual datasets. The bottleneck is the cost of force-instrumented teleoperation rigs.
- **==Vision-tactile temporal alignment==** — Vision and tactile streams run at different rates (vision **30Hz**; tactile **100Hz-1kHz**), so naive concatenation injects phase errors at contact onset. Continuous sensors like [[2604.20689|FingerEye]] sidestep this by ==unifying modalities at the sensor level==, but discrete vision+tactile pairs still need careful temporal calibration.

#### 5.2 Architecture & Tokenization

How should continuous force / tactile signal enter a VLM-scale backbone? The literature has bifurcated into prompts-vs-signals, with neither winning, and contact prediction itself drifts over long horizons.

- **==Force prompts vs force signals as VLM input==** — [[2603.15169|ForceVLA2]] uses force *prompts* (linguistic descriptions of force at the VLM); [[2507.09160|Tactile-VLA]] feeds raw tactile signals into the VLM through ==tokenization==. Neither approach is clearly superior across all tasks. The right tokenization scheme for continuous F/T at VLM scale is unresolved.
- **==Contact prediction stability==** — [[2603.05687|CGP]] grounds policies on predicted tactile trajectories, but diffusion-predicted tactile signals can drift over long horizons. ==Closed-loop re-grounding== (predict, execute, re-predict) is the natural fix but adds latency and hasn't been systematically studied.

#### 5.3 Deployment & Failure Recovery

Contact-rich deployment exposes a sharper latency-quality trade than vision-only VLAs face. Failure-recovery coverage is also narrow because failure datasets are small.

- **==Failure recovery from tactile signals==** — [[2507.09160|Tactile-VLA]]'s ==CoT-from-tactile== covers only **~3-5 failure modes**. Open-set recovery needs either larger failure datasets or reasoning models that synthesize strategies without failure-mode supervision — see [[16_Self-Evolving-VLA-WAM#4. Failure Detection, Diagnosis & Recovery]] for the broader self-correction landscape.
- **==Force-aware reasoning latency==** — [[2507.09160|Tactile-VLA]]'s CoT recovery adds **1-3s** per recovery — fine for blackboard wiping, too slow for fast pick-and-place. The latency-quality trade-off in [[05_VLA-Reasoning-and-CoT#6. Reasoning Quality vs Inference Latency]] is *sharper* under contact because contact transitions are millisecond-fast.

**Force-Aware Failure Modes — Decision Matrix**

| Problem | Remediation Path |
|---|---|
| Need to transfer policy across tactile sensor instances | [[2509.18830\|DexSkin]] (pneumatic calibration) — instance-level only |
| Need cross-sensor-type transfer | [[2410.24090\|Sparsh]] / [[2506.14754\|Sparsh-X]] (SSL portability) + [[2601.20321\|TaF-VLA]] (force-grounded alignment, **60.3%** zero-shot) |
| Need larger force-instrumented dataset | [[2603.15169\|ForceVLA2]] (1K trajectories) — best public option; community-scale OXE-for-force still missing |
| How to feed continuous F/T into VLM | [[2603.15169\|ForceVLA2]] (prompts) vs. [[2507.09160\|Tactile-VLA]] (raw tokenization) — task-dependent; no winner |
| Predicted tactile trajectory drifts over horizon | [[2603.05687\|CGP]] (diffusion grounding) + closed-loop re-grounding (latency cost) |
| Vision-tactile sampling-rate mismatch | [[2604.20689\|FingerEye]] (unified sensor) or careful temporal calibration for discrete pairs |
| Need open-set failure recovery | [[2507.09160\|Tactile-VLA]] (CoT-from-tactile, narrow); [[16_Self-Evolving-VLA-WAM#4. Failure Detection, Diagnosis & Recovery]] for broader self-correction |
| Need fast reasoning under millisecond contact | Latency budget constraint — no current solution; use [[2602.23648\|FAVLA]] (fast-slow) as architectural workaround |

^dm-5

> [!star] Key Papers — Force-Aware Failure Frontier
> - [[2601.20321|TaF-VLA]] — **60.3%** zero-shot transfer across unseen tactile sensors via force-grounded alignment; the strongest current evidence that cross-sensor transfer is *possible* — but the residual gap remains large
> - [[2603.15169|ForceVLA2]] — Largest public force-instrumented dataset (**1K trajectories**) + the canonical "force prompts at the VLM" architecture; exposes both the data-scale gap and the prompts-vs-signals open question
> - [[2507.09160|Tactile-VLA]] — Raw tactile signal tokenization + CoT-from-tactile failure recovery; the load-bearing evidence for both the tokenization camp and the reasoning-latency-too-slow-for-contact problem

^key-papers-5

> [!tip] Force-Aware Bottlenecks Are Data-Scale + Integration-Scale
> Six of the seven problems above (cross-sensor transfer, no-OXE-for-force, prompts-vs-signals, failure recovery scarcity, contact prediction drift, vision-tactile alignment) trace to two roots: **(1) data scale** — the largest force-instrumented dataset ([[2603.15169|ForceVLA2]], ~1K trajectories) is **1000×** smaller than [[2310.08864|OXE]]; **(2) integration scale** — VLA backbones learned vision-language alignment at web scale, but have no equivalent pretraining corpus for vision-tactile-language. The seventh problem (reasoning latency) is sharper than in [[05_VLA-Reasoning-and-CoT#6. Reasoning Quality vs Inference Latency]] because contact transitions are millisecond-fast. Cross-reference [[02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks]] (Tactile & Contact-Rich Benchmarks — the evaluation-side echo of the data-scale gap) and [[05_VLA-Reasoning-and-CoT#7. Open Problems]] (the cross-modal reasoning gap — where reasoning over force/tactile is the underexplored frontier that meets §5.3 here from the other direction).

^insight-5

---

## Quick-Reference Matrix

| Need | Use |
|------|-----|
| Cheap high-coverage tactile skin (DIY) | [[2604.28156\|FlexiTac]] ($30, FPC piezoresistive, 100Hz, 8×16-32×32) |
| High-quality conformable skin + sim-to-real | [[2509.18830\|DexSkin]] (capacitive, 294° coverage, pneumatic calibration) |
| Continuous pre→post-contact sensing | [[2604.20689\|FingerEye]] (binocular vision-tactile fingertip) |
| Pretrained tactile encoder (foundation model) | [[2410.24090\|Sparsh]] ([[2111.06377\|MAE]]/[[2104.14294\|DINO]]/JEPA over **460k** images + TacBench) or [[2506.14754\|Sparsh-X]] (multisensory: image+audio+IMU+pressure) |
| Force-conditioned VLA, simplest formulation | [[2507.09160\|Tactile-VLA]] (force-augmented action space + hybrid controller) |
| Force-aware MoE, late-fusion best-practice | [[2505.22159\|ForceVLA]] (FVLMoE; 60.5% avg SR) |
| SOTA force-aware VLA (force prompts + Cross-Scale MoE) | [[2603.15169\|ForceVLA2]] (66% avg SR; +48pp over [[2410.24164\|π0]]) |
| Fast-slow VLA with adaptive force-trigger frequency | [[2602.23648\|FAVLA]] (80.8% avg SR; reduces peak contact forces) |
| Contact-aware tactile gating in VLA | [[2603.12665\|TacVLA]] (83.75% disassembly; robust to occlusion) |
| Tactile-aware VLA *without* inference-time tactile sensor | [[2603.15257\|HapticVLA]] (distilled tactile token; 86.7% on fragile-object tasks) |
| Force-grounded tactile alignment (plug-and-play VLA adapter) | [[2601.20321\|TaF-VLA]] (VQ-VAE on 10M tactile-force pairs; cross-sensor zero-shot) |
| Force-aware diffusion policy with explicit force action | [[2510.13324\|FARM]] (predicts pose+grip+force; 100% dynamic screw-tightening) |
| Visuotactile policy via diffusion-grounded contact prediction | [[2603.05687\|CGP]] (diffusion over coupled state+tactile trajectories) |
| Contact-rich task with known reference force | [[2505.06451\|Adaptive-Wiping]] (few-shot IL + closed-loop F/T) |
| Force-conditioned video generation (for pretraining) | [[2505.19386\|Force-Prompting]] (ControlNet-style force conditioning of CogVideoX) |
| Long-horizon memory for force history | [[2508.19236\|MemoryVLA]] (PCMB dual-memory; +26pp on long-horizon) |
| Failure recovery from tactile signals | [[2507.09160\|Tactile-VLA]] (CoT-from-tactile, 3.5N→6.7N adaptive adjustment) |
| Phased curriculum to avoid VLM forgetting | [[2502.14420\|ChatVLA]] (control-first, then understanding) |

---

## Cross-References

- [[12_Whole-Body-and-Locomotion-Control]] — The whole-body / locomotion half of the same contact-dynamics axis; the body-scale echo of force-as-first-class-modality (unified controllers, balance under load, humanoid skill data), and the home of [[2511.07820|SONIC]]/[[2504.11054|Meta-Motivo]]-style motion-tracking foundation models
- [[04_VLA]] — §7 Multi-Sensor & Force-Aware is the parent section the Parts A–C force-conditioned cluster expands; [[04_VLA#7. Multi-Sensor & Force-Aware VLAs]] holds the broader VLA design-space context
- [[03_Imitation-Learning-and-RL]] — The RL-*methods* side of contact-rich control; [[03_Imitation-Learning-and-RL#6. RL for Locomotion, Navigation & Whole-Body Control]] holds the policy-optimization machinery (residual RL, force-aware fine-tuning) that the force-conditioned policies instantiate as contact-dynamics substrate
- [[16_Self-Evolving-VLA-WAM]] — Self-correcting VLAs and failure-recovery mechanisms ([[2601.02295|CycleVLA]], [[2512.24426|CF-VLA]], [[2511.14148|AsyncVLA]]) that complement [[2507.09160|Tactile-VLA]]'s CoT-from-tactile; see [[16_Self-Evolving-VLA-WAM#4. Failure Detection, Diagnosis & Recovery]]
- [[08_Physics-Aware-Embodied-AI]] — Physics priors and physics-conditioned video generation ([[2509.20358|PhysCtrl]], [[2505.19386|Force-Prompting]]); the natural pretraining backbone for force-aware VLAs
- [[02_Dataset-Benchmark-Environment]] — Contact-rich benchmarks; see [[02_Dataset-Benchmark-Environment#6. Tactile & Contact-Rich Benchmarks]] for the evaluation-side echo of the §5 data-scale gap
- [[14_Egocentric-Pretraining-and-Human-Video]] — Egocentric/human-video pretraining underwriting vision-to-tactile prediction ([[2605.13083|TouchAnything]]); see [[14_Egocentric-Pretraining-and-Human-Video#3. Scaling Laws for Egocentric Pretraining]]
- [[15_Sim-to-Real-Transfer]] — Sim-to-Real Transfer deep-dive; tactile sim-to-real plus the domain randomization force-aware policies depend on; see [[15_Sim-to-Real-Transfer#3. Policy-Side: Robustness & Domain Randomization]]
- [[01_Embodied-AI-101]] — Primer on embodied AI and the four learning strategies; contact sensing sits at the intersection of imitation learning and physical interaction
- [[06_WAM]] — World-model augmentation patterns; [[2505.19386|Force-Prompting]] fits the video-WAM track with explicit force conditioning ([[06_WAM#2. VideoGen WAMs]])
- [[07_Latent-World-Models]] — Latent representation for multi-sensor inputs including tactile streams
- [[05_VLA-Reasoning-and-CoT]] — Reasoning architectures; tactile-driven CoT is the underexplored cross-modal slot ([[05_VLA-Reasoning-and-CoT#6. Reasoning Quality vs Inference Latency]])

---

*See [[12_Whole-Body-and-Locomotion-Control]] for the whole-body half of the axis, [[04_VLA#7. Multi-Sensor & Force-Aware VLAs]] for the VLA-design-space context this deep-dive expands, or [[16_Self-Evolving-VLA-WAM#4. Failure Detection, Diagnosis & Recovery]] for failure-recovery patterns that complement [[2507.09160|Tactile-VLA]]'s CoT.*
