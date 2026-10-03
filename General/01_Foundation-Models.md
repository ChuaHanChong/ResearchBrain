---
title: "Foundation Models & Transformers — Topic Overview"
tags:
  - transformer
  - LLM
  - foundation-model
  - pre-training
  - self-supervised
aliases:
  - "Foundation Models Overview"
---

# Foundation Models & Transformers

> [!abstract] Overview
> From ViT to billion-parameter VLMs, foundation models define the backbone of modern AI. This note traces the evolution from vision transformers through self-supervised learning to the large multi-modal models that power VLAs, reasoning systems, and autonomous agents. It also covers the training recipes, attention innovations, and adaptation strategies that make these models practical.

## Evolution Graph

```text
1. Backbone Architecture   (what encodes the image)
· pure-transformer vision
                  +shifted windows, high-res        +22B dense scaling
╔════════════╗    ┌────────────────────────────┐    ┌────────────────┐
║ ViT (2020) ║───►│ Swin-Transformer-V2 (2021) │───►│ ViT-22B (2023) │
╚══════┬═════╝    └────────────────────────────┘    └────────────────┘
       │    +dense prediction on
       │    plain ViT
       │    ┌────────────────────┐
       └───►│ ViT-Adapter (2022) │
            └────────────────────┘

2. Attention Redesign   (replace the quadratic core)
· sparsify the attention
                   +differentiable    sparse tokens →
                   dynamic mask       sparse depth
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ MoSA (2025) │───►│ DMA (2025)  │───►│ MoDA (2026) │
└──────┬──────┘    └─────────────┘    └─────────────┘
       │    +attention-sink
       │    removal
       │    ┌─────────────────┐
       └───►│ Softpick (2025) │
            └─────────────────┘

· give it memory instead
                     +recursion for     +nested
                     parameter reuse    learning levels
┌───────────────┐    ┌─────────────┐    ┌─────────────┐
│ Titans (2025) │───►│ MoR (2025)  │───►│ Hope (2025) │
└───────┬───────┘    └─────────────┘    └─────────────┘
        │    +hybrid
        │    Transformer-Mamba
        │    ┌──────────────────┐
        └───►│ Falcon-H1 (2025) │
             └──────────────────┘

3. Label-Free Pretraining   (drop the labels, keep the signal)
· self-distillation
                   +142M curated        +coding-rate
                   images               regularization
┌─────────────┐    ┌───────────────┐    ┌────────────────┐
│ DINO (2021) │───►│ DINOv2 (2023) │───►│ SimDINO (2025) │
└──────┬──────┘    └───────────────┘    └────────────────┘
       │    +test-time training
       │    ┌───────────────────┐
       └───►│ Vision-TTT (2026) │
            └───────────────────┘

· reconstruction to latent prediction
                   discrete tokens →    pixel target →
                   raw pixels           latent target
┌─────────────┐    ┌───────────────┐    ┌───────────────┐
│ BEiT (2021) │───►│ MAE (2021)    │───►│ I-JEPA (2023) │─┐
└─────────────┘    └───────────────┘    └───────────────┘ │
                                                          │    +provable isotropic
                                                          │    objective
                                                          │    ┌─────────────────┐
                                                          ├───►│ LeJEPA (2025)   │
                                                          │    └─────────────────┘
                                                          │    +variational bottleneck
                                                          │    ┌────────────────────────────┐
                                                          ├───►│ VJEPA-Probabilistic (2026) │
                                                          │    └────────────────────────────┘
                                                          │    +object-centric causal
                                                          │    ┌────────────────────┐
                                                          └───►│ Causal-JEPA (2026) │
                                                               └────────────────────┘

4. Vision-Language Alignment   (pair the image with text)
· contrastive to generative
                   +bootstrapped      +both objectives    +unified
                   captions           at once             understand/generate
╔═════════════╗    ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
║ CLIP (2021) ║───►│ BLIP (2022) │───►│ CoCa (2022)  │───►│ BLIP3-o (2025)  │
╚══════┬══════╝    └─────────────┘    └──────────────┘    └─────────────────┘
       │    2 modalities → 6
       │    ┌──────────────────┐
       ├───►│ ImageBind (2023) │
       │    └──────────────────┘
       │    +fine-grained
       │    sparse alignment
       │    ┌──────────────┐
       └───►│ SPARC (2024) │
            └──────────────┘

5. Multimodal LLMs   (put the image inside the language model)
· interleaved to grounded
                       +arbitrary             +bounding-box
                       interleaving           tokens                 +open 3B, 40 tasks
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ Flamingo (2022) │───►│ KOSMOS-1 (2023) │───►│ KOSMOS-2 (2023) │───►│ PaliGemma (2024) │
└─────────────────┘    └────────┬────────┘    └─────────────────┘    └──────────────────┘
                                │    +simple projector
                                │    recipe
                                │    ┌──────────────────┐
                                ├───►│ LLaVA-1.5 (2023) │
                                │    └──────────────────┘
                                │    +any-to-any
                                │    modalities
                                │    ┌─────────────────┐
                                └───►│ NExT-GPT (2023) │
                                     └─────────────────┘

6. RL for Reasoning   (post-training, not pretraining)
· who verifies the answer
                          math/code →        +pretraining-scale
                          diverse domains    data
╔════════════════════╗    ┌─────────────┐    ┌────────────────────┐
║ DeepSeek-R1 (2025) ║───►│ RLVR (2025) │───►│ Webscale-RL (2025) │─┐
╚════════════════════╝    └─────────────┘    └────────────────────┘ │
                                                                    │    +zero-data,
                                                                    │    tool-integrated
                                                                    │    ┌───────────────┐
                                                                    ├───►│ Agent0 (2025) │
                                                                    │    └───────────────┘
                                                                    │    +zero-annotation
                                                                    │    multimodal
                                                                    │    ┌───────────────┐
                                                                    └───►│ V-Zero (2026) │
                                                                         └───────────────┘

7. Efficient Adaptation   (reuse a model you already have)
· adapt without retraining
                   prompts →         +multi-token
                   generated LoRA    prediction
┌─────────────┐    ┌────────────┐    ┌───────────────────┐
│ CoOp (2021) │───►│ T2L (2025) │───►│ Gated-LoRA (2025) │
└──────┬──────┘    └────────────┘    └───────────────────┘
       │    +multi-teacher
       │    distillation
       │    ┌─────────────────┐
       ├───►│ AM-RADIO (2023) │
       │    └─────────────────┘
       │    +checkpoint
       │    merging
       │    ┌────────────┐
       └───►│ PMA (2025) │
            └────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

The seven lanes divide on **which layer of the stack is being built**. **Backbone architecture** settles what encodes the image, ViT to Swin-Transformer-V2 to ViT-22B as resolution and parameter count climb, with ViT-Adapter branching to make a plain ViT handle dense prediction. **Attention redesign** attacks the quadratic core two ways that do not meet: MoSA, DMA, and MoDA sparsify what attends, with Softpick removing the attention sink, while Titans, MoR, and Hope give the model memory and recursion instead, and Falcon-H1 branches to a hybrid Transformer-Mamba stack. **Label-free pretraining** drops the labels, and again splits: DINO's self-distillation scales through DINOv2 to SimDINO, with Vision-TTT branching to train at test time, while BEiT's discrete tokens give way to MAE's raw pixels and then I-JEPA's latent targets, after which LeJEPA, VJEPA-Probabilistic, and Causal-JEPA each reformulate that same objective independently. **Vision-language alignment** pairs image with text, CLIP to BLIP to CoCa to BLIP3-o as the objective turns generative, with ImageBind and SPARC branching to more modalities and finer-grained alignment. **Multimodal LLMs** put the image inside the language model, Flamingo to KOSMOS-1 to KOSMOS-2 to PaliGemma, with LLaVA-1.5 and NExT-GPT branching off KOSMOS-1 toward a simpler projector and any-to-any modalities. **RL for reasoning** moves the work to post-training and turns on who verifies the answer, DeepSeek-R1 to RLVR to Webscale-RL, then Agent0 and V-Zero removing the annotation entirely. **Efficient adaptation** reuses a model you already have, CoOp to T2L to Gated-LoRA, with AM-RADIO and PMA branching to distillation and checkpoint merging.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2020 | [[2010.11929\|ViT]] | Backbone · Pure-Transformer Vision | Proved a pure Transformer on image patches matches CNNs at scale, eliminating convolutional inductive biases |
| 2021 | [[2103.00020\|CLIP]] | Alignment · Contrastive to Generative | Contrastive image-text pretraining on 400M web pairs; enabled zero-shot visual recognition via natural language |
| 2021 | [[2104.14294\|DINO]] | Label-Free · Self-Distillation | Self-distillation without labels produces ViT features with emergent object segmentation in attention maps |
| 2021 | [[2106.08254\|BEiT]] | Label-Free · Reconstruction to Latent | BERT-style pre-training for vision: predict discrete visual tokens from masked patches |
| 2021 | [[2109.01134\|CoOp]] | Adaptation · Adapt without Retraining | Learnable prompts for adapting CLIP without fine-tuning; launched the prompt learning field |
| 2021 | [[2111.06377\|MAE]] | Label-Free · Reconstruction to Latent | Masked 75% of patches and reconstructed pixels; made self-supervised ViT pretraining 3-4x cheaper |
| 2021 | [[2111.09883\|Swin-Transformer-V2]] | Backbone · Pure-Transformer Vision | Scaled vision Transformers to 3B parameters with stable training via residual post-norm and cosine attention |
| 2022 | [[2201.12086\|BLIP]] | Alignment · Contrastive to Generative | Unified vision-language understanding and generation with bootstrapped caption filtering for noisy web data |
| 2022 | [[2204.14198\|Flamingo]] | MLLM · Interleaved to Grounded | DeepMind's few-shot VLM interleaving vision and language; established in-context learning for multimodal models |
| 2022 | [[2205.01917\|CoCa]] | Alignment · Contrastive to Generative | Combined contrastive and generative objectives in a single contrastive captioner |
| 2022 | [[2205.08534\|ViT-Adapter]] | Backbone · Pure-Transformer Vision | Foundational adapter method enabling plain ViTs to handle dense prediction tasks without architectural changes |
| 2023 | [[2301.08243\|I-JEPA]] | Label-Free · Reconstruction to Latent | Predicted abstract representations instead of pixels; 10x cheaper pretraining with stronger semantic features |
| 2023 | [[2302.05442\|ViT-22B]] | Backbone · Pure-Transformer Vision | Demonstrated vision models can scale to 22B parameters, achieving 89.5% ImageNet with emergent LLM-like properties |
| 2023 | [[2302.14045\|KOSMOS-1]] | MLLM · Interleaved to Grounded | First MLLM with arbitrarily interleaved image-text inputs; 84.7 CIDEr on COCO, 22% on custom Raven IQ — established the foundational MLLM paradigm |
| 2023 | [[2304.07193\|DINOv2]] | Label-Free · Self-Distillation | Scaled self-supervised learning to 142M curated images; produced universal visual features competitive with CLIP without text |
| 2023 | [[2305.05665\|ImageBind]] | Alignment · Contrastive to Generative | Aligned six modalities into one embedding space using images as anchor; enabled emergent cross-modal zero-shot transfer |
| 2023 | [[2306.14824\|KOSMOS-2]] | MLLM · Interleaved to Grounded | Grounded MLLMs to spatial regions via bounding box tokens in text; 78.7% R@1 on Flickr30k phrase grounding |
| 2023 | [[2309.05519\|NExT-GPT]] | MLLM · Interleaved to Grounded | Any-to-any multimodal LLM handling text, image, audio, and video |
| 2023 | [[2310.03744\|LLaVA-1.5]] | MLLM · Interleaved to Grounded | Enhanced large multimodal model achieving SOTA with simple architectural improvements |
| 2023 | [[2312.06709\|AM-RADIO]] | Adaptation · Adapt without Retraining | Agglomerative multi-teacher distillation unifying CLIP, DINOv2, and SAM into one vision foundation model |
| 2024 | [[2401.09865\|SPARC]] | Alignment · Contrastive to Generative | Sparse fine-grained contrastive alignment from Google DeepMind; learns region-text correspondences without dense annotations |
| 2024 | [[2407.07726\|PaliGemma]] | MLLM · Interleaved to Grounded | Open-source 3B VLM matching larger models across 40 tasks; democratized VLM research through efficient transfer |
| 2025 | [[2501.00663\|Titans]] | Attention · Memory Instead | Learns to memorize at test time via a dedicated neural memory module; bridges short and long-range context |
| 2025 | [[2501.12948\|DeepSeek-R1]] | RL Post-Training · Who Verifies | RL-only training (no SFT) elicits emergent chain-of-thought reasoning; established the RL-for-reasoning paradigm the field now builds on |
| 2025 | [[2502.10385\|SimDINO]] | Label-Free · Self-Distillation | Dramatically simplified DINO via coding rate regularization; shows what DINO really needs |
| 2025 | [[2503.23829\|RLVR]] | RL Post-Training · Who Verifies | Extends RL with verifiable rewards beyond math/code to diverse domains |
| 2025 | [[2504.20966\|Softpick]] | Attention · Sparsify | Rectified non-sum-to-one normalization; eliminates attention sinks and massive activations |
| 2025 | [[2505.00315\|MoSA]] | Attention · Sparsify | Mixture of Sparse Attention with expert-choice routing; content-based learned sparsity |
| 2025 | [[2505.09568\|BLIP3-o]] | Alignment · Contrastive to Generative | Unified image understanding and generation in a single hybrid autoregressive-diffusion architecture |
| 2025 | [[2505.12082\|PMA]] | Adaptation · Adapt without Retraining | Pre-trained Model Average for effective merging of LLM checkpoints |
| 2025 | [[2506.06105\|T2L]] | Adaptation · Adapt without Retraining | Text-to-LoRA: hypernetwork that dynamically generates task-specific LoRA adapters from text descriptions |
| 2025 | [[2507.10524\|MoR]] | Attention · Memory Instead | Mixture-of-Recursions unifies parameter efficiency with adaptive per-token computation depth |
| 2025 | [[2507.11851\|Gated-LoRA]] | Adaptation · Adapt without Retraining | Enables pretrained autoregressive LLMs to perform multi-token prediction via gated LoRA modules |
| 2025 | [[2507.22448\|Falcon-H1]] | Attention · Memory Instead | Hybrid-head models integrating parallel Transformer and Mamba blocks; redefines the efficiency-performance frontier |
| 2025 | [[2508.02124\|DMA]] | Attention · Sparsify | Fully differentiable dynamic mask sparse attention; hardware-optimized for practical deployment |
| 2025 | [[2510.06499\|Webscale-RL]] | RL Post-Training · Who Verifies | Automated pipeline scaling verifiable RL training data to pretraining levels |
| 2025 | [[2511.08544\|LeJEPA]] | Label-Free · Reconstruction to Latent | Provable and scalable self-supervised learning framework based on Euclidean latent geometry |
| 2025 | [[2511.16043\|Agent0]] | RL Post-Training · Who Verifies | Self-evolving agents from zero data via tool-integrated reasoning; paradigm for autonomous agent improvement |
| 2025 | [[2512.24695\|Hope]] | Attention · Memory Instead | Nested Learning reinterprets deep learning as nested multi-level optimization |
| 2026 | [[2601.10094\|V-Zero]] | RL Post-Training · Who Verifies | Self-improving multimodal reasoning with zero annotation; proves annotation-free self-improvement is viable |
| 2026 | [[2601.14354\|VJEPA-Probabilistic]] | Label-Free · Reconstruction to Latent | Variational/Bayesian JEPA with predictive-information-bottleneck guarantees; filters high-variance nuisance distractors, keeps **R²>0.84** under SNR=-2.2 dB |
| 2026 | [[2602.11389\|Causal-JEPA]] | Label-Free · Reconstruction to Latent | Object-centric world model integrating JEPAs with causal reasoning via latent interventions |
| 2026 | [[2603.00518\|Vision-TTT]] | Label-Free · Self-Distillation | Adapts Test-Time Training for efficient visual representation learning; bridges pre-training and inference |
| 2026 | [[2603.15619\|MoDA]] | Attention · Sparsify | Mixture-of-Depths Attention dynamically allocates compute across tokens and layers |

---

## 1. Vision Transformers

The architectural revolution that brought attention mechanisms to computer vision, replacing CNN inductive biases with scalable self-attention over image patches.

**Foundational Architectures** — The core ViT lineage from patch tokenization through windowed attention to extreme parameter scale.
- [[2604.02327|SteerViT]] (ECCV'26), [[2603.29634|MacTok]] (CVPR'26), [[2511.13720|JiT-Denoise-Transformer]], [[2401.08541|AIM]] (ICML'24), [[2310.00632|WIN-WIN]] (ICLR'24), [[2307.06304|NaViT]] (NeurIPS'23), [[2303.11331|EVA-02]], [[2302.05442|ViT-22B]] (ICML'23 Oral), [[2212.08013|FlexiViT]] (CVPR'23), [[2205.14949|HiViT]], [[2205.10337|UViM]] (NeurIPS'22), [[2111.09883|Swin-Transformer-V2]], [[2106.04560|ViT-G/14]], [[2103.14030|Swin Transformer]] (ICCV'21), [[2012.12877|DeiT]] (ICML'21 Spotlight), [[2010.11929|ViT]] (ICLR'21 Oral)

> [!star] Key Papers
> - [[2010.11929|ViT]] (ICLR'21 Oral) — Split images into 16x16 patches, applied standard Transformer encoder; proved Transformers match CNNs with enough data
> - [[2111.09883|Swin-Transformer-V2]] — Shifted window attention for efficient high-resolution processing; scaled to 3B parameters
> - [[2302.05442|ViT-22B]] (ICML'23 Oral) — Largest dense ViT at 22B parameters; demonstrated continued scaling benefits for vision

**Hierarchical & Multi-Scale ViT Backbones** — Hierarchical, multi-scale attention designs that recover CNN-like locality and resolution flexibility for dense prediction.
- [[2505.22195|S2AFormer]], [[2403.18361|ViTAR]], [[2310.00632|WIN-WIN]] (ICLR'24), [[2306.06189|FasterViT]] (ICLR'24), [[2305.00104|MMViT]], [[2304.06250|RSIR-Transformer]], [[2205.14949|HiViT]], [[2205.14756|EfficientViT]] (ICCV'23), [[2204.01697|MaxViT]], [[2203.16527|ViTDet]] (ECCV'22), [[2203.11926|FocalNet]] (NeurIPS'22 Spotlight), [[2112.11010|MPViT]], [[2112.01526|MViTv2]] (CVPR'22), [[2111.01236|HRViT]] (CVPR'22), [[2110.09408|HRFormer]] (NeurIPS'21), [[2107.06263|CMT]] (CVPR'22), [[2107.00641|Focal-Transformer]], [[2105.13677|ResT]] (NeurIPS'21), [[2104.11227|MViT]] (ICCV'21), [[2102.12122|PVT]]

**Domain- & Task-Specific Vision Adaptations** — ViT variants adapted to specific vision tasks: stereo matching, hand-object pose, panoramic segmentation, and image/video segmentation.
- [[2607.13674|WAVE-Stereo]], [[2606.30598|HOPformer]] (ECCV'26), [[2602.17807|VidEoMT]] (CVPR'26), [[2503.19108|EoMT]] (CVPR'25), [[2312.05251|HaMeR]] (CVPR'24), [[2207.11860|Trans4PASS+]]

**Geometric & 3D/4D Reconstruction Transformers** — Feed-forward transformers for single- and multi-view 3D/4D scene geometry, depth, and dynamic reconstruction.
- [[2609.15018|G-ray]], [[2607.05801|TRIG]], [[2604.13596|VGGT-Segmentor]], [[2602.20160|tttLRM]] (CVPR'26), [[2602.10101|Robo3R]] (RSS'26), [[2602.10094|4RC]], [[2512.23667|MVID]], [[2512.08924|D4RT]], [[2512.04012|RobustVGGT]], [[2401.10891|Depth Anything]], [[2312.14132|DUSt3R]] (CVPR'24)

**Robotics-Oriented ViT Adaptations** — ViT-based encoders specialized for robot locomotion and manipulation policies rather than general vision tasks.
- [[2510.08568|NovaFlow]], [[2509.23745|LocoFormer]] (CoRL'25), [[2506.09588|Attention-Map-Encoding]], [[2501.18564|SAM2Act]] (ICML'25), [[2501.05420|RoboPanoptes]] (RSS'25), [[2212.07740|TERT]] (ICRA'23), [[2107.03996|LocoTransformer]] (ICLR'22 Spotlight)

**Key Surveys** — Comprehensive overviews of the vision transformer landscape.
- [[2604.00965|Transformers-for-Applied-Mathematicians]], [[2309.02031|Efficient-ViT-Survey]], [[2305.09880|ViT-CNN-Transformer-Survey]], [[2111.06091|Visual-Transformers-Survey]], [[2101.01169|Transformers-in-Vision-Survey]], [[2012.12556|Visual-Transformer-Survey]]

> [!star] Key Papers
> - [[2101.01169|Transformers-in-Vision-Survey]] — Early comprehensive survey that mapped the ViT landscape and catalyzed adoption of Transformers in computer vision
> - [[2309.02031|Efficient-ViT-Survey]] — Systematic taxonomy of efficiency methods for vision Transformers; essential reference for practical deployment
> - [[2012.12556|Visual-Transformer-Survey]] — One of the earliest broad surveys of Transformer architectures across vision tasks, predating the 2021 wave
> - [[2111.06091|Visual-Transformers-Survey]] — Consolidated taxonomy of ViT variants and training recipes as the field matured past first-generation designs

**Efficiency, Tokenization & Edge Deployment** — Reducing ViT compute and memory cost via patch/token-level optimization, sparsity, and lightweight designs for edge inference.
- [[2609.33325|VisionHOPE]], [[2603.25744|MuRF]], [[2603.22815|PinPoint]] (CVPR'26), [[2603.22387|EUPE]], [[2602.08683|OneVision-Encoder]], [[2512.01738|MSPT]], [[2510.23479|MergeMix]] (ICLR'26), [[2510.21501|GranViT]], [[2510.18091|APT]] (ICLR'26), [[2507.07995|KARL-Eff]] (NeurIPS'25), [[2507.01643|SAILViT]], [[2506.11136|JAFAR]] (NeurIPS'25), [[2505.23769|TextRegion]], [[2504.03118|NuWa-Eff]] (CVPR'26), [[2307.09120|LW-PLG-ViT]], [[2205.03436|EdgeViTs]], [[2107.02239|ViX]], [[2104.05704|CCT]]

**Domain Adaptation, Transfer & Interpretability** — Adapting pretrained ViTs to new domains via adapters and prompts, and analyzing what the adapted representations capture.
- [[2608.02124|HAFI-VLM]], [[2603.22570|CanViT]], [[2603.02959|SS-Text-U]], [[2601.08499|EfficientFSL]], [[2505.21501|PH-Reg]] (NeurIPS'25 Spotlight), [[2505.19985|Structured-ViT-Initialization]] (NeurIPS'25), [[2505.18364|ImLPR]] (CoRL'25), [[2505.17316|Patch-Aligned-Training]] (NeurIPS'25), [[2502.01962|META]] (ICLR'25), [[2501.09333|Prompt-CAM]] (CVPR'25), [[2412.04073|TransAdapter]], [[2303.13434|PMTrans]] (CVPR'23), [[2205.08534|ViT-Adapter]] (ICLR'23 Spotlight), [[2108.05988|TVT]]

> [!star] Key Papers
> - [[2205.08534|ViT-Adapter]] (ICLR'23 Spotlight) — Foundational adapter method enabling plain ViTs to handle dense prediction tasks without architectural changes
> - [[2412.04073|TransAdapter]] — Feature-centric unsupervised domain adaptation for ViTs; bridges the gap between pre-trained ViTs and target domains

> [!tip] Scaling vs Efficiency
> ViTs scale well (ViT-22B proves this), but raw scaling is not always practical. Hierarchical designs like Swin and HiViT recover multi-scale features efficiently, while domain-specific adaptations (HIPT for pathology, WIN-WIN for high-res) show that architecture matters as much as scale.

---

## 2. Attention Mechanisms & Architectural Innovations

New attention patterns, normalization strategies, and structural modifications that improve Transformer efficiency, stability, and expressiveness.

**Sparse & Efficient Attention** — Reducing the quadratic cost of self-attention through sparsity, routing, and learned masking.
- [[2603.15619|MoDA]], [[2603.08055|Speed3R]] (CVPR'26), [[2508.02124|DMA]], [[2507.16577|Sparse-State-Expansion]], [[2505.17083|Scale-invariant-Attention]] (NeurIPS'25), [[2505.06708|Gated-Attention]] (NeurIPS'25 Oral), [[2505.01996|Token-Graying]] (ICCV'25), [[2505.00315|MoSA]], [[2412.09871|BLT]], [[2312.06635|GLA]] (ICML'24), [[2009.06732|Efficient-Transformers-Survey]]

> [!star] Key Papers
> - [[2505.00315|MoSA]] — Mixture of Sparse Attention with expert-choice routing; content-based learned sparsity
> - [[2508.02124|DMA]] — Fully differentiable dynamic mask sparse attention; hardware-optimized for practical deployment
> - [[2603.15619|MoDA]] — Mixture-of-Depths Attention dynamically allocates compute across tokens and layers

**Activation & Normalization Replacements** — Drop-in replacements for LayerNorm and Softmax that improve training stability or remove normalization entirely.
- [[2603.15031|AttnRes]], [[2512.24880|mHC]], [[2512.10938|Derf]] (CVPR'26), [[2504.20966|Softpick]], [[2503.10622|DyT]] (CVPR'25), [[2502.15798|MaxSup]] (NeurIPS'25 Oral)

> [!star] Key Papers
> - [[2503.10622|DyT]] (CVPR'25) — Dynamic Tanh as a drop-in replacement for normalization layers; simpler and equally effective
> - [[2504.20966|Softpick]] — Rectified non-sum-to-one normalization; eliminates attention sinks and massive activations

**Residual Connections & Depth** — Rethinking how information flows through deep networks via improved residual strategies and adaptive depth.
- [[2607.13491|DeepLoop]], [[2603.15031|AttnRes]], [[2512.24880|mHC]], [[2512.24695|Hope]] (NeurIPS'25), [[2507.10524|MoR]] (NeurIPS'25), [[2506.09714|Auto-Compressing-Networks]] (NeurIPS'25 Oral), [[1512.03385|ResNet]] (CVPR'16)

> [!star] Key Papers
> - [[2507.10524|MoR]] (NeurIPS'25) — Mixture-of-Recursions unifies parameter efficiency with adaptive per-token computation depth
> - [[2512.24695|Hope]] (NeurIPS'25) — Nested Learning reinterprets deep learning as nested multi-level optimization

**Hybrid Architectures** — Combining Transformers with state-space models, recurrence, or looped computation for improved efficiency.
- [[2609.40305|Looped-DiT]], [[2609.38426|LoopVL]], [[2608.27763|Falcon (Fast Weight Attention)]], [[2608.05416|SpectraLDS]], [[2607.16051|Loopie]], [[2605.11689|MoE-Configuration-Study]], [[2604.21254|Hyperloop-Transformers]], [[2603.11691|STAIRS-Former]], [[2601.15275|RayRoPE]], [[2512.20856|Nemotron-3]], [[2508.09834|Efficient-LLM-Architectures-Survey]], [[2507.22448|Falcon-H1]], [[2507.12898|Vidar]], [[2507.06607|Gated-Memory-Unit]], [[2507.03285|Memory-Mosaics-v2]] (NeurIPS'25 Oral), [[2505.16416|Circle-RoPE]] (ICML'26), [[2505.05522|CTM]] (NeurIPS'25 Spotlight), [[2503.24067|TransMamba]], [[2501.00663|Titans]] (NeurIPS'25), [[2412.06464|Gated DeltaNet]], [[2405.21060|Mamba-2]] (ICML'24), [[2311.12424|Looped-Transformers]] (ICLR'24)

> [!star] Key Papers
> - [[2507.22448|Falcon-H1]] — Hybrid-head models integrating parallel Transformer and Mamba blocks; redefines the efficiency-performance frontier
> - [[2501.00663|Titans]] (NeurIPS'25) — Learns to memorize at test time via a dedicated neural memory module; bridges short and long-range context

**Theoretical Foundations of Transformers** — Formal analyses of what Transformers compute, how in-context learning works, and connections to established frameworks.
- [[2604.27077|νGPT]], [[2604.00965|Transformers-for-Applied-Mathematicians]], [[2603.17063|Transformers-as-Bayesian-Networks]], [[2601.15380|GOAT]], [[2510.19315|Transformers-Succinct]] (ICLR'26 Oral), [[2509.25040|Mean-Field-Transformers]] (NeurIPS'25 Oral), [[2509.00421|Prompt-Tuning-Memory-Limits]], [[2507.16003|ICL-Implicit-Dynamics]], [[2505.17863|Sparse-Attention-Emergence]] (NeurIPS'25 Oral), [[2504.13173|Miras]] (ICLR'26), [[2502.14010|ICL-Attention-Heads]] (ICML'25), [[2502.09324|Depth-Bounds-Braid]] (NeurIPS'25 Oral), [[2410.10101|Linear-Attention-Learnability]] (NeurIPS'25 Oral), [[2410.06205|p-RoPE]] (ICLR'25), [[2104.09864|RoPE]], [[1706.03762|Transformer]]

> [!star] Key Papers
> - [[2603.17063|Transformers-as-Bayesian-Networks]] — Proves sigmoid Transformers fundamentally operate as Bayesian networks
> - [[2507.16003|ICL-Implicit-Dynamics]] — Shows in-context learning in LLMs can be modeled as implicitly solving dynamical systems

> [!tip] The Post-Softmax Era
> 2025 saw a wave of work replacing or augmenting standard softmax attention (Softpick, DyT, Derf) and standard normalization (DyT removes it entirely). These are not incremental — they change how information flows through Transformers and may become default in next-generation architectures.

---

## 3. Self-Supervised Visual Learning

Learning visual representations without labels — the foundation for data-efficient downstream tasks.

**Foundational Contrastive & Self-Distillation Methods** — The core lineage of contrastive and self-distillation objectives that established label-free representation learning.
- [[2304.12824|CEP]] (ICML'23), [[2304.07193|DINOv2]] (ICLR'25), [[2304.03977|EMP-SSL]], [[2206.08954|BagSSL]], [[2203.10833|Hyp-ViT]] (CVPR'22), [[2202.03555|data2vec]] (ICML'22 Oral), [[2110.03374|HCL]] (NeurIPS'21), [[2106.09785|EsViT]] (ICLR'22), [[2105.04906|VICReg]] (ICLR'22), [[2105.04553|MoBY]], [[2104.14294|DINO]], [[2104.03602|SiT]], [[2104.02057|MoCo-v3]], [[2103.03230|Barlow Twins]] (ICML'21 Spotlight), [[2102.06810|SSL-Dynamics]] (ICML'21 Oral), [[2011.10566|SimSiam]] (CVPR'21), [[2006.07733|BYOL]] (NeurIPS'20 Oral), [[2002.05709|SimCLR]] (ICML'20), [[1911.05722|MoCo]] (CVPR'20), [[1906.00910|AMDIM]] (NeurIPS'19), [[1712.07629|SuperPoint]] (CVPR'18 Workshop)

> [!star] Key Papers
> - [[2104.14294|DINO]] — Self-distillation with no labels; emergent object segmentation in attention maps
> - [[2304.07193|DINOv2]] (ICLR'25) — Curated data + distillation produces universal visual features without fine-tuning

**DINO-Family & Latent Geometry Extensions** — Recent methods that extend, simplify, or theoretically analyze the DINO/DINOv2 self-distillation lineage.
- [[2603.28480|INSID3]] (CVPR'26), [[2510.08638|Minkowski-Representation-Hypothesis]] (ICLR'26), [[2507.14137|Franca]], [[2505.15970|DINOv2-Hierarchy-SAE]] (CVPR'25 Workshop), [[2503.20839|TAR]], [[2503.09867|OH-A-DINO]], [[2502.10385|SimDINO]] (ICML'25)

> [!star] Key Papers
> - [[2502.10385|SimDINO]] (ICML'25) — Dramatically simplified DINO via coding rate regularization; shows what DINO really needs

**Robotics-Applied Contrastive Perception** — Contrastive and self-supervised representation learning applied to robot manipulation, locomotion, and localization.
- [[2609.20107|AnyViewDex]], [[2607.05247|LingBot-Vision]], [[2606.04718|CoRe-MoE]], [[2604.09445|AsymLoc]], [[2603.12217|Verifier-Point-Tracking]] (CVPR'26), [[2602.00937|CLAMP]] (RSS'26), [[2506.10359|Multi-Suction Pick Success]] (RSS'25), [[2502.19374|VFM-LiDAR Registration]] (RSS'25)

**General Self-Supervised Learning Theory** — Theoretical and empirical studies of what makes contrastive/self-distillation objectives work and how they scale.
- [[2608.06174|SO-OPF]], [[2605.03517|LDM-SSL]] (ICML'26 Spotlight), [[2603.26799|GJE]], [[2603.15553|Bootleg]], [[2601.21584|Observation-Quotient]], [[2506.10159|VCL]], [[2410.10817|Human-Aligned Vision Representations]] (NeurIPS'24), [[2406.09294|JEA-Scaling-Study]] (NeurIPS'24)

**Masked Image Modeling** — Self-supervised methods that mask patches of an image and train the model to reconstruct or predict the missing content, learning rich visual representations without labels.
- [[2609.38278|Masked Swingers]], [[2603.22953|ClusterSTM]] (CVPR'26), [[2505.11129|PhiNet-v2]], [[2402.10093|MIM-Refiner]] (ICLR'25), [[2303.16727|VideoMAE V2]] (CVPR'23), [[2205.14949|HiViT]], [[2111.09886|SimMIM]] (CVPR'22), [[2111.06377|MAE]] (CVPR'22), [[2106.08254|BEiT]] (ICLR'22 Oral)

> [!star] Key Papers
> - [[2111.06377|MAE]] (CVPR'22) — Masked 75% of patches; proved simple reconstruction objective learns powerful features
> - [[2106.08254|BEiT]] (ICLR'22 Oral) — BERT-style pre-training for vision: predict discrete visual tokens from masked patches

**Video & Intuitive-Physics JEPA** — JEPA variants that learn video representations by latent prediction and probe intuitive physical understanding.
- [[2603.14482|V-JEPA-2.1]], [[2506.09985|V-JEPA-2]], [[2502.11831|V-JEPA (Intuitive Physics)]], [[2404.08471|V-JEPA]] (ICLR'25), [[2403.00504|IWM]], [[1803.07616|IntPhys]]

**Core JEPA Theory & Objectives** — Foundational and theoretical studies of the JEPA objective itself: variants, regularizers, and what makes latent prediction work.
- [[2609.23881|MotionJEPA]], [[2609.20800|JEPA-Anything]], [[2608.27395|LeVJEPA]], [[2607.02404|Object-centric LeJEPA]], [[2606.15956|TDV]], [[2606.02572|VISReg]], [[2605.03413|NEO-Theorizer]], [[2603.20111|Var-JEPA]], [[2601.14354|VJEPA-Probabilistic]], [[2512.19605|KerJEPA]], [[2511.08544|LeJEPA]], [[2509.25449|TS-JEPA]] (NeurIPS'24 Workshop), [[2509.12249|P-JEPA]], [[2507.15216|N-JEPA]], [[2505.03176|seq-JEPA]] (NeurIPS'25), [[2410.19560|C-JEPA]] (NeurIPS'24 Spotlight), [[2410.03755|D-JEPA]] (ICLR'25), [[2407.03475|JEPA-Noisy-Features]] (NeurIPS'24), [[2312.04000|LiDAR-Metric]] (ICLR'24 Spotlight), [[2307.12698|MC-JEPA]], [[2301.08243|I-JEPA]] (CVPR'23), [[2211.10831|JEPA-Slow-Features]] (NeurIPS'22 Workshop), [[1504.08023|Visual Representation Anticipation]] (CVPR'16)

> [!star] Key Papers
> - [[2301.08243|I-JEPA]] (CVPR'23) — Predicts in latent space instead of pixel space; avoids reconstruction artifacts
> - [[2511.08544|LeJEPA]] — Provable and scalable self-supervised learning framework based on Euclidean latent geometry
> - [[2602.11389|Causal-JEPA]] (ICML'26) — Object-centric world model integrating JEPAs with causal reasoning via latent interventions
> - [[2601.14354|VJEPA-Probabilistic]] — Variational/Bayesian JEPA with predictive-information-bottleneck guarantees; filters high-variance nuisance distractors, keeps **R²>0.84** under SNR=-2.2 dB

**Domain-Specific JEPA Applications** — JEPA adapted to non-standard modalities and domains: remote sensing, 3D/point clouds, graphs, satellite imagery, recommendation, and trajectory data.
- [[2608.22642|Mol-JEPA]], [[2511.18424|CrossJEPA]], [[2504.10512|JEPA4Rec]], [[2504.03169|REJEPA]] (CVPR'25 Workshop), [[2412.14123|AnySat]] (CVPR'25), [[2409.15803|3D-JEPA]], [[2406.12913|T-JEPA-Trajectory]], [[2404.16432|Point-JEPA]], [[2311.15153|SAR-JEPA]], [[2309.16014|Graph-JEPA]]

**Cross-Modal & Generative JEPA Variants** — JEPA formulations for vision-language alignment, text-conditioned generation, and multimodal pretraining.
- [[2607.00784|LeVLJEPA]], [[2605.02134|PV-VAE]], [[2512.10942|VL-JEPA]] (ICLR'26), [[2510.00974|JEPA-T]], [[2509.14252|LLM-JEPA]] (ICLR'26), [[2503.06380|TI-JEPA]]

> [!tip] The JEPA Lineage
> I-JEPA started a family: [[2511.08544|LeJEPA]] (provable foundations) and [[2512.19605|KerJEPA]] (kernel methods) extend the theory, while [[2602.11389|Causal-JEPA]] (ICML'26) adds causal reasoning. For the full robotics-oriented lineage (V-JEPA 2 → VL-JEPA → VLA-JEPA), see the JEPA notes in the vault.

**Tactile & Multi-Sensory Representation Learning** — Self-supervised and contrastive methods for learning transferable tactile representations across heterogeneous sensors and modalities.
- [[2609.39017|OccluDex]], [[2609.29822|PROPRA]], [[2609.24385|Tactile-JEPA]], [[2607.20683|FELT]], [[2607.13522|Kepler-Encoder]], [[2607.01067|TTP]], [[2606.31694|RCT]], [[2606.31236|TactX]] (CoRL'26), [[2606.29948|HTT]], [[2606.29173|TacGen]], [[2606.14344|LESS]] (RSS'26), [[2605.29564|VE2VF]], [[2603.15847|FEEL]] (ECCV'26 Oral), [[2601.20239|TouchGuide]] (RSS'26), [[2509.14688|exUMI]] (CoRL'25), [[2506.14754|Sparsh-X]] (CoRL'25), [[2505.11420|Sparsh-skin]] (CoRL'25), [[2410.24090|Sparsh]] (CoRL'24)

> [!star] Key Papers
> - [[2606.31236|TactX]] (CoRL'26) — Learns shared representations across heterogeneous tactile sensor families; transfers without hardware-specific retraining
> - [[2606.29948|HTT]] — Heterogeneous Tactile Transformer: general self-supervised framework spanning diverse sensor transduction types

**Continual & Semi-Supervised Learning Theory** — Adapting self-supervised models for streaming data, long-tailed distributions, class-incremental learning, and test-time shifts.
- [[2601.19897|SDFT]], [[2512.15934|IC-SSL]] (ICLR'26), [[2512.09441|MoP-CIL]], [[2511.20844|Pre-train-to-Gain]], [[2511.13787|TC2]], [[2507.10434|CLA]], [[2506.00467|SST]], [[2505.05062|ULFine]], [[2411.13852|ESRM]] (NeurIPS'24), [[2404.17202|Low-Data-SSL-Evaluation]], [[2305.13622|SER]]

> [!star] Key Papers
> - [[2507.10434|CLA]] — Continual Latent Alignment for online continual self-supervised learning; avoids catastrophic forgetting
> - [[2512.15934|IC-SSL]] (ICLR'26) — In-Context Semi-Supervised Learning: Transformer framework leveraging in-context learning for semi-supervised tasks

**Representation Capacity, Scaling & General SSL Methods** — Studies of representation capacity, scaling behavior, and general self-supervised methods that fall outside the continual/semi-supervised and robotics-specific buckets.
- [[2609.29350|FBDM]], [[2607.09657|VP]], [[2607.09024|GenCeption]] (ECCV'26), [[2607.06856|Gen4U]], [[2606.03940|SEAOTTER]], [[2606.02767|HAKF]], [[2605.29548|Capacity-Interference-Retention]], [[2605.27734|Latent-Sample-Complexity]], [[2605.22629|H-Flow]], [[2605.09963|Spatial-Prediction-SP]], [[2604.18267|MARCO]] (CVPR'26 Oral), [[2603.06693|SER]] (ICLR'26), [[2512.01342|InternVideo-Next]] (CVPR'26), [[2511.17309|MuM]], [[2509.15965|RLinf]], [[2410.21676|Critical-Batch-Size-Scaling]] (ICLR'25), [[2409.14401|In-Class-Data-Imbalance]], [[2101.12195|CADDY]] (CVPR'21)

**Robotics Imitation, Play & Offline Representation Learning** — Self-supervised and imitation-learning methods for robot manipulation and navigation from demonstrations, play, and offline interaction data.
- [[2607.08341|AnyDexRT]], [[2605.24934|HumanEgo]], [[2605.20811|Demo-JEPA]], [[2509.21986|Ego-VLA-Pretrain]], [[2508.19391|LaVA-Man]] (CoRL'25), [[2507.23523|H-RDT]], [[2506.05064|DemoSpeedup]] (CoRL'25), [[2505.17006|CoMo]] (CVPR'26), [[2504.18904|RoboVerse]], [[2412.04445|Moto]] (ICCV'25 Oral), [[2410.24221|EgoMimic]], [[2406.17768|EXTRACT]] (CoRL'24), [[2312.10812|LAPO]] (ICLR'24 Spotlight), [[2311.16098|Dobb-E]], [[2306.00958|LIV]] (ICML'23), [[2111.09793|Robotic-Interestingness]], [[2111.07447|Self-Replay]] (CoRL'21), [[2101.05181|MemAug-Image-Goal-Nav]], [[1909.06933|DD Policy]], [[1903.11239|TossingBot]], [[1903.01973|Play-LMP]] (CoRL'19), [[1806.09655|CLASP-Action-Space]] (ICLR'19), [[1805.07914|ILPO]] (ICML'19)

**Robot World Models, Latent Actions & RL Representation** — World models, latent-action representations, and RL-theoretic representation learning for robot control.
- [[2609.22175|Contrastive World Models]], [[2606.04130|CLAW-Latent-Action-WM]], [[2606.03985|Humanoid-GPT]] (CVPR'26), [[2606.03476|Human2Humanoid]], [[2605.30350|DynaFLIP]], [[2605.26379|LeJEPA-World-Model]], [[2605.25313|UWM-JEPA]], [[2605.22671|BehaviorVLA]] (ICML'26 Oral), [[2605.21258|Structural-Latent-Points]], [[2605.15725|DiLA]], [[2604.16391|DeFI]] (ICLR'26), [[2512.00961|GenReward]] (CVPR'26), [[2511.04131|BFM-Zero]] (ICLR'26), [[2505.00500|INR-DOM]] (RSS'25), [[2410.08208|SPA (3D Spatial-Awareness Representation)]] (ICLR'25), [[2407.20230|SAPG]] (ICML'24 Oral), [[2311.12244|muLV-Rep]] (ICML'24), [[2310.01404|H-InDex]] (NeurIPS'23), [[2212.05749|LfS (+aug) Baseline]] (ICML'23), [[2210.07241|Self-Supervised 3D RL]], [[2103.07945|Forward-Backward Representation]] (NeurIPS'21), [[2103.06326|S4RL]]

**Dataset Distillation & Representation Theory** — Compressing training data and understanding the theoretical properties of learned representations.
- [[2604.18811|Dataset-Distillation-Soft-Labels]] (CVPR'26 Oral), [[2604.03191|Compression-Gap]], [[2603.12228|Neural-Thickets]], [[2602.15029|Language-Symmetry-Representations]] (ICML'26), [[2602.01905|STELLAR]], [[2601.03220|Epiplexity]], [[2512.19693|Prism-Hypothesis]], [[2512.09322|GPSSL]], [[2512.00536|Dataset-Distillation-RL]] (ICLR'26), [[2511.16674|LGM]] (NeurIPS'25), [[2510.20994|VESSA]] (NeurIPS'25), [[2506.16895|STRUCTURE-Alignment]] (NeurIPS'25), [[2506.09278|UFM]] (NeurIPS'25), [[2505.12477|Joint-Embedding-vs-Reconstruction-SSL]] (NeurIPS'25 Spotlight), [[2504.10428|PIU-Learning]] (STOC), [[2402.11337|Reconstruction vs Perception]]

> [!star] Key Papers
> - [[2511.16674|LGM]] (NeurIPS'25) — Linear Gradient Matching for dataset distillation in self-supervised models; highly efficient compression
> - [[2601.03220|Epiplexity]] — New information measure beyond entropy for computationally bounded intelligence

**Test-Time Training & Adaptation** — Methods that adapt visual models at inference time to handle distribution shifts.
- [[2606.03127|TTT-VLA]], [[2603.00518|Vision-TTT]], [[2512.01643|ViT-cubed]] (CVPR'26 Oral), [[2506.23529|SSTTA]], [[2410.02735|OOD-Chameleon]] (ICML'25), [[2307.00972|MoVie]] (NeurIPS'23), [[2006.10726|Tent]] (ICLR'21 Spotlight)

> [!star] Key Papers
> - [[2603.00518|Vision-TTT]] — Adapts Test-Time Training for efficient visual representation learning; bridges pre-training and inference

**Anomaly & Domain-Specific Detection** — Self-supervised approaches for anomaly detection and unsupervised domain adaptation.
- [[2601.12964|Cross-Scale-Pretraining]], [[2601.05552|UniADet]], [[2502.10694|UDA-Simulation-Study]], [[2411.15869|SC-CLIP]], [[2407.21311|EUDA]], [[2403.14410|GLC++]], [[2402.14976|Foundation-Latent-UDA]], [[2312.07871|MLNet]], [[2308.15855|IIDM]], [[2211.03876|CoNMix]], [[2210.17067|UniOT]] (NeurIPS'22 Spotlight), [[2204.07683|SSRT]], [[2111.12941|WinTR]], [[2010.07734|STARTUP]] (ICLR'21 Oral), [[2002.07953|DANCE]] (NeurIPS'20)

> [!star] Key Papers
> - [[2601.05552|UniADet]] — Universal vision anomaly detection without language priors; purely visual foundation model approach
> - [[2411.15869|SC-CLIP]] — Training-free self-calibrated CLIP for open-vocabulary segmentation; resolves anomalous attention biases

**SSL Surveys** — Comprehensive reviews of self-supervised visual learning methods and evaluation.
- [[2605.28442|COTRATE]], [[2505.13584|SSL-Segmentation-Survey]], [[2504.07213|E-SSL-Survey]], [[2408.17059|SSL-for-ViT-Survey]], [[2306.02572|LV-EBM-Intro]], [[2305.13689|SSL-Survey]]

> [!star] Key Papers
> - [[2305.13689|SSL-Survey]] — Comprehensive taxonomy of image-based generative and discriminative self-supervised methods; essential landscape overview
> - [[2408.17059|SSL-for-ViT-Survey]] — Focused survey on self-supervised mechanisms specifically designed for vision Transformers

> [!tip] From Reconstruction to Prediction
> The field moved from pixel reconstruction (MAE, BEiT) to latent prediction (I-JEPA, LeJEPA). Latent prediction avoids wasting capacity on irrelevant pixel details and produces more semantically meaningful features. Meanwhile, continual learning (CLA, IC-SSL) ensures these methods work in non-stationary real-world settings.

---

## 4. Vision-Language Alignment

Connecting visual and textual representations in a shared embedding space, enabling zero-shot transfer and multimodal reasoning.

**Foundational Contrastive Alignment** — The core CLIP-style lineage of joint image-text embeddings learned via contrastive objectives on large-scale paired data.
- [[2502.14786|SigLIP-2]], [[2309.17425|DFN]] (ICLR'24), [[2309.16671|MetaCLIP]] (ICLR'24 Spotlight), [[2303.15343|SigLIP]], [[2212.07143|OpenCLIP]] (CVPR'23), [[2208.12262|MaskCLIP]] (CVPR'23), [[2205.01917|CoCa]], [[2112.04482|FLAVA]] (CVPR'22), [[2111.10050|BASIC]], [[2111.07991|LiT]] (CVPR'22), [[2111.02114|LAION-400M]], [[2103.00020|CLIP]] (ICML'21 Oral), [[2010.00747|ConVIRT]], [[1612.09161|Visual N-Grams]] (ICCV'17)

> [!star] Key Papers
> - [[2103.00020|CLIP]] (ICML'21 Oral) — Contrastive pre-training on 400M image-text pairs; enabled zero-shot transfer to any visual task via text prompts
> - [[2205.01917|CoCa]] — Combined contrastive and generative objectives in a single contrastive captioner
> - [[2507.18009|GRR-CoCa]] — Integrates modern LLM architectural features into the CoCa framework for improved multimodal performance

**Recent Contrastive Alignment Extensions** — Efficiency, distillation, and representation-quality improvements built on the CLIP-style contrastive alignment recipe.
- [[2608.17402|MoE-ViE]] (ECCV'26), [[2512.11141|ItemizedCLIP]], [[2509.01644|OpenVision-2]], [[2507.22062|Meta-CLIP-2]] (NeurIPS'25 Spotlight), [[2507.18009|GRR-CoCa]], [[2506.06970|MAPLE]] (NeurIPS'25), [[2506.03096|FuseLIP]], [[2505.21549|DCLIP]], [[2505.18983|AmorLIP]] (NeurIPS'25), [[2505.14204|Perceptual-Initialization]], [[2505.11192|FALCON]] (CVPR'26), [[2505.04601|OpenVision]] (ICCV'25), [[2505.04410|DeCLIP]] (CVPR'25), [[2505.03703|Modality-Gap-Reduction]], [[2504.13181|Perception-Encoder]] (NeurIPS'25 Oral), [[2503.15485|TULIP]], [[2503.06626|DiffCLIP]], [[2406.17639|AlignCLIP]] (ICLR'25), [[2406.06973|RWKV-CLIP]]

**Multi-Modal Embedding Spaces** — Extending alignment beyond image-text to encompass audio, depth, thermal, and other modalities.
- [[2511.00405|UME-R1]] (ICLR'26), [[2510.06673|Heptapod]], [[2506.23639|Being-VL]] (ICCV'25 Highlight), [[2505.15045|DIFFEMBED]], [[2505.05422|TokLIP]], [[2504.02318|X-Capture]] (ICCV'25), [[2502.02772|Force-Language Dual Autoencoder]] (RSS'25), [[2411.14402|AIMV2]] (CVPR'25), [[2411.04997|LLM2CLIP]], [[2305.05665|ImageBind]] (CVPR'23), [[2206.07643|FIBER]] (NeurIPS'22)

> [!star] Key Papers
> - [[2305.05665|ImageBind]] (CVPR'23) — Extended alignment to 6 modalities (image, text, audio, depth, thermal, IMU) via a single embedding space
> - [[2506.23639|Being-VL]] (ICCV'25 Highlight) — Unified multimodal understanding via byte-pair encoding applied to visual tokens

**Bootstrapped & Generative Alignment** — Methods that generate or bootstrap training data for vision-language alignment.
- [[2601.09859|TuneCLIP]] (ICLR'26), [[2506.22434|MiCo]] (NeurIPS'25), [[2505.21465|ID-Align]], [[2505.16149|REVEAL]], [[2504.20364|SSL-Representation-Human-Alignment]], [[2503.01776|CSR]] (ICML'25 Oral), [[2411.15869|SC-CLIP]], [[2403.19651|MagicLens]] (ICML'24 Oral), [[2301.11915|Part-Aware-SSL]], [[2201.12086|BLIP]] (ICML'22 Spotlight), [[2006.06666|VirTex]]

> [!star] Key Papers
> - [[2201.12086|BLIP]] (ICML'22 Spotlight) — Pioneered bootstrapped caption filtering for noisy web data; unified VL understanding and generation in one framework
> - [[2503.01776|CSR]] (ICML'25 Oral) — Sparse coding-based adaptive representations that go beyond Matryoshka for flexible embedding dimensionality

**Foundational Region-Level & Fine-Grained Alignment** — The core lineage of methods learning region-text correspondences for open-vocabulary detection and dense grounding.
- [[2401.09865|SPARC]] (ICML'24), [[2303.02489|CapDet]] (CVPR'23), [[2302.13996|BARON]] (CVPR'23), [[2211.13854|ComCLIP]], [[2206.05836|GLIPv2]] (NeurIPS'22), [[2203.12555|GriTS]], [[2112.09106|RegionCLIP]] (CVPR'22), [[2112.01071|MaskCLIP (Dense CLIP Labels)]] (ECCV'22), [[2111.07783|FILIP]] (ICLR'22), [[2104.12763|MDETR]]

> [!star] Key Papers
> - [[2401.09865|SPARC]] (ICML'24) — Sparse fine-grained contrastive alignment from Google DeepMind; learns region-text correspondences without dense annotations
> - [[2504.17432|UniME]] — Universal multimodal embeddings; SOTA on MMEB benchmark for fine-grained retrieval

**Recent Contrastive & Fine-Grained Representation Extensions** — Recent methods and theoretical studies extending contrastive vision-language alignment toward fine-grained, compositional, and general representation-learning settings.
- [[2606.04433|Stateful-Visual-Encoders]], [[2605.18740|Vision-OPD]], [[2512.17012|4D-RGPT]] (CVPR'26 Highlight), [[2507.09961|TDCRL]], [[2507.09615|FAIR]], [[2506.23156|Multi-Label-Contrastive-SSL]], [[2506.15757|WPCL]] (IROS'25), [[2506.12698|KDUP]], [[2506.07413|VarCon]] (NeurIPS'25), [[2506.04411|DCL-Neural-Collapse-Theory]] (NeurIPS'25), [[2505.22196|Aug-Aware-SSL-Theory]] (ICML'25), [[2505.21533|SOP]] (ICML'25), [[2505.02278|GCLIP]] (CVPR'25 Workshop), [[2504.19627|VCM]], [[2504.17432|UniME]], [[2502.02202|MLCL]]

> [!tip] Beyond Image-Text Pairs
> CLIP showed that contrastive learning on web-scale data creates powerful zero-shot models. The next frontier (ImageBind, Being-VL, Heptapod) extends this to arbitrary modalities. The key insight: a single well-aligned embedding space transfers better than modality-specific encoders.

---

## 5. Multimodal Large Language Models

LLMs augmented with visual perception — the backbone for modern VLMs and VLAs. These models bridge language understanding with visual grounding, generation, and action.

**Unified Understanding & Generation VLMs** — Single models that jointly handle multimodal understanding and image/action generation rather than understanding alone.
- [[2609.38597|PixelUMM]], [[2609.11929|SenseNova-U1.5]], [[2609.08282|GGF]], [[2608.05000|PhysMMPT]], [[2606.27376|Ask-Solve-Generate]], [[2603.25406|MMaDA-VLA]], [[2505.14683|BAGEL]], [[2505.09568|BLIP3-o]]

**Instruction-Tuned VLMs** — General-purpose multimodal models trained to follow instructions across vision-language tasks.
- [[2504.10479|InternVL3]], [[2504.00595|Open-Qwen2VL]], [[2407.07726|PaliGemma]], [[2405.13800|Dense Connector]] (NeurIPS'24), [[2404.16821|InternVL 1.5]], [[2403.05525|DeepSeek-VL]], [[2311.07575|SPHINX (Multi-modal Weight Mixing)]], [[2310.03744|LLaVA-1.5]] (CVPR'24 Highlight), [[2305.18565|PaLI-X]], [[2305.06500|InstructBLIP]] (NeurIPS'23), [[2303.08774|GPT-4]], [[2302.14045|KOSMOS-1]] (NeurIPS'23), [[2301.12597|BLIP-2]] (ICML'23), [[2210.03347|Pix2Struct]] (ICML'23 Oral), [[2209.06794|PaLI]] (ICLR'23 Oral), [[2204.14198|Flamingo]] (NeurIPS'22), [[2102.02779|VL-T5]] (ICML'21 Spotlight)

> [!star] Key Papers
> - [[2302.14045|KOSMOS-1]] (NeurIPS'23) — First MLLM with arbitrarily interleaved image-text inputs; established the foundational MLLM paradigm this whole group builds on
> - [[2407.07726|PaliGemma]] — Sub-3B VLM achieving SOTA on 40 tasks; SigLIP + Gemma connected by linear projection
> - [[2310.03744|LLaVA-1.5]] (CVPR'24 Highlight) — Enhanced large multimodal model achieving SOTA with simple architectural improvements
> - [[2505.09568|BLIP3-o]] — Fully open unified multimodal model family excelling in both understanding and generation
> - [[2303.08774|GPT-4]] — Multimodal Transformer with human-level performance across professional benchmarks; established RLHF-aligned foundation models as the standard
> - [[2204.14198|Flamingo]] (NeurIPS'22) — DeepMind's few-shot VLM interleaving vision and language; established in-context learning for multimodal models

**Grounded & Spatial MLLMs** — Models that can localize objects, reference bounding boxes, and reason about spatial relationships.
- [[2607.15054|ViPS]], [[2602.21186|Spa3R]], [[2602.11635|MathSpatial]], [[2601.13633|EGM]], [[2512.06963|VideoVLA]] (NeurIPS'25), [[2511.19418|COVT]] (ECCV'26 Oral), [[2510.27606|Spatial-SSRL]], [[2410.11829|MMFuser]], [[2306.14824|KOSMOS-2]] (ICLR'24)

> [!star] Key Papers
> - [[2306.14824|KOSMOS-2]] (ICLR'24) — Grounded multimodal LLM: generates text with bounding box references
> - [[2601.13633|EGM]] — Enables smaller VLMs to scale test-time inference for visual grounding

**Any-to-Any & Agent-Oriented MLLMs** — Models designed for arbitrary modality conversion or as foundations for autonomous agents.
- [[2511.20085|VICoT-Agent]], [[2509.09666|Unified-MM-Auto-Encoders]], [[2502.13130|Magma]] (CVPR'25), [[2309.05519|NExT-GPT]] (ICML'24 Oral), [[2303.11381|MM-REACT]]

> [!star] Key Papers
> - [[2309.05519|NExT-GPT]] (ICML'24 Oral) — Any-to-any multimodal LLM handling text, image, audio, and video
> - [[2502.13130|Magma]] (CVPR'25) — Foundation model specifically designed for multimodal AI agents

**Visual Reasoning & Thinking** — Methods for enhancing MLLMs with explicit reasoning, chain-of-thought over images, and self-rewarding loops.
- [[2601.13705|LVLM-Visual-Puzzle-Survey]], [[2511.10055|HCM-GRPO]] (PR), [[2511.09018|Owl]], [[2510.06783|TTRV]], [[2509.25190|Visual-Jigsaw]] (ICLR'26), [[2508.19652|Vision-SR1]], [[2506.23918|Thinking-with-Images-Survey]], [[2505.17022|GoT-R1]] (ICLR'26), [[2504.17207|APC]] (ICCV'25), [[2501.04693|FuSe]]

> [!star] Key Papers
> - [[2505.17022|GoT-R1]] (ICLR'26) — Applies RL to unleash reasoning capability of MLLMs for visual generation
> - [[2508.19652|Vision-SR1]] — Self-rewarding RL framework for VLMs via reasoning decomposition
> - [[2510.06783|TTRV]] — First test-time RL framework for decoder-based VLMs

**MLLM Evaluation & Benchmarks** — Reward models, judging frameworks, and benchmarks for evaluating multimodal model quality.
- [[2512.16899|MMRB2]], [[2510.17793|Foundational-Evaluators]] (ICLR'26), [[2508.19229|StepWiser]], [[2401.06209|MMVP]] (CVPR'24 Oral)

> [!star] Key Papers
> - [[2512.16899|MMRB2]] — First comprehensive benchmark for evaluating reward models on multimodal interleaved content
> - [[2508.19229|StepWiser]] — Generative judges that meta-reason about intermediate reasoning steps

**Key Surveys** — Comprehensive surveys mapping the rapidly evolving MLLM landscape.
- [[2405.19334|LLM-Multimodal-Generation-Survey]], [[2405.10739|Efficient-MLLM-Survey]], [[2306.13549|MLLM-Survey]], [[2303.18223|LLM Survey]]

> [!star] Key Papers
> - [[2306.13549|MLLM-Survey]] — Foundational survey that defined the taxonomy and evaluation framework for multimodal large language models
> - [[2405.10739|Efficient-MLLM-Survey]] — Comprehensive guide to making MLLMs practical through efficiency techniques across model, data, and inference

**Additional methods** — Papers referenced in this section that don't fit the categories above.
- [[2605.30370|IBNN]]

> [!success] The Modern VLM Stack
> ==Frozen vision encoder== (SigLIP or DINOv2) + ==lightweight connector== (linear projection) + ==LLM backbone== (Gemma, Llama) + ==instruction tuning== on diverse V-L tasks. Sub-3B models now achieve SOTA on 40+ tasks; open-source MLLMs match proprietary ones across understanding and generation.

> [!tip] The VLM Stack
> Modern VLMs follow a consistent pattern: frozen vision encoder (often SigLIP or DINOv2) + lightweight connector (linear projection or Q-Former) + LLM backbone. PaliGemma proved this can work at sub-3B scale, while BLIP3-o and LLaVA-1.5 showed that open models can compete with proprietary ones. The frontier is now visual reasoning (GoT-R1, Vision-SR1) and test-time RL (TTRV).

---

## 6. LLM Training & Optimization

Core training recipes, optimizers, scaling laws, and architectural insights for training large language models efficiently.

**Optimizers** — Second-order and novel optimizers that improve over AdamW for large-scale training.
- [[2606.25971|MD-Decoupling]], [[2605.31159|TRB]], [[2506.07254|SPlus]] (NeurIPS'25), [[2506.05454|Zeroth-Order-Flat-Minima]] (NeurIPS'25), [[2506.01393|GP-UCB-Regret]] (NeurIPS'25 Oral), [[2505.23725|MuLoCo]], [[2505.16932|Polar-Express]] (ICLR'26 Oral), [[2505.02222|Muon]], [[2502.16982|Muon]]

> [!star] Key Papers
> - [[2502.16982|Muon]] — Breakthrough: second-order optimizer demonstrating superior training efficiency over AdamW for LLMs
> - [[2505.23725|MuLoCo]] — Muon as inner optimizer for DiLoCo distributed training; significant speedup over AdamW

**Scaling Laws, Compute-Optimality & Foundational Releases** — Theoretical scaling laws and the landmark large-scale pretrained language models whose training runs put those laws into practice.
- [[2609.19107|Prelude-Core-Coda]], [[2609.15818|Atria Dawn]], [[2607.22043|Native Multimodal Scaling Laws]], [[2607.16097|Pretraining-RL Scaling Law]], [[2607.15314|Cura 1T]], [[2605.26494|MiniMax-M2]], [[2603.21191|BST-Scaling-Rule]], [[2603.15958|Hyperparameter-Scaling-Laws]], [[2510.06954|Condensation-Rank-Collapse]] (NeurIPS'25 Oral), [[2509.02754|LLM Modules for AD]] (CoRL'25), [[2507.20534|Kimi-K2]], [[2507.06261|Gemini-2.5]], [[2506.12932|Complexity-Scaling-Laws]] (NeurIPS'25), [[2505.10559|Neural-Thermodynamic-Laws]], [[2505.10465|Superposition-Scaling]] (NeurIPS'25 Oral), [[2504.07951|NMM-Scaling-Laws]] (ICCV'25 Oral), [[2503.12811|MPL]] (ICLR'25), [[2502.21269|Generalization-Overfitting-Decoupling]] (NeurIPS'25 Oral), [[2410.21276|GPT-4o]], [[2405.18392|Compute-Optimal-Scaling-Laws]] (NeurIPS'24 Spotlight), [[2303.12712|Sparks of AGI]], [[2302.13971|LLaMA]], [[2204.02311|PaLM (Pathways Language Model)]], [[2006.12467|Depth-to-Width Interplay]] (NeurIPS'20), [[2005.14165|GPT-3]] (NeurIPS'20 Oral), [[2001.08361|Neural Scaling Laws]]

> [!star] Key Papers
> - [[2503.12811|MPL]] (ICLR'25) — Multi-Power Law accurately predicts training loss across learning rate schedules
> - [[2302.13971|LLaMA]] — Open, efficient foundation LMs trained on public data only; matched GPT-3 at 10x fewer parameters and catalyzed the open-weight LLM ecosystem
> - [[2204.02311|PaLM (Pathways Language Model)]] — 540B-parameter model trained with Pathways; demonstrated emergent few-shot reasoning and chain-of-thought capabilities at scale

**Training Systems, Pipelines & MoE Infrastructure** — Practical systems work on pipeline scheduling, learning-rate/hyperparameter tuning, and mixture-of-experts routing for large-scale training.
- [[2607.21653|Molt]], [[2607.05155|EdgeBench]], [[2605.22297|Layerwise-LR]], [[2605.02087|MSM]], [[2604.27085|RoundPipe]], [[2604.05091|MegaTrain]], [[2603.27164|daVinci-LLM]], [[2603.26164|DataFlex]], [[2602.10556|LAP]] (RSS'26), [[2512.16913|DAP]], [[2508.18672|MoE-Sparsity-Reasoning]] (ICLR'26 Oral), [[2507.12507|Nemotron]], [[2506.16029|EvoLM]] (NeurIPS'25 Oral), [[2505.22323|MoE-Expert-Specialization]] (NeurIPS'25 Oral), [[2504.13161|Nemotron-CLIMB]] (NeurIPS'25 Spotlight), [[2405.16158|BRO]] (NeurIPS'24 Spotlight), [[2310.18969|ViT-Class-Embedding-Analysis]] (NeurIPS'23), [[2309.14322|Transformer-Training-Instabilities]] (ICLR'24 Oral), [[2302.01107|Efficient-Transformer-Training-Survey]], [[2109.08203|Seed-3407]], [[2107.02027|packedBERT]], [[1701.06538|Sparsely-Gated MoE]] (ICLR'17)

**Batch Size, Distributed Training & Large-Scale RL Systems** — Studies of batch size effects and the distributed/parallel training systems that enable large-scale learning, including early large-scale RL infrastructure.
- [[2507.07101|Small-Batch-LLM-Training]] (NeurIPS'25), [[2504.17838|CaRL]] (CoRL'25), [[2104.08212|MT-Opt]], [[1812.06162|Large-Batch-Training]], [[1811.03600|Data Parallelism Study]], [[1807.11205|Jizhi]], [[1803.00933|Ape-X]] (ICLR'18), [[1706.02677|ImageNet in 1 Hour]], [[1507.04296|Gorila]]

> [!star] Key Papers
> - [[2507.07101|Small-Batch-LLM-Training]] (NeurIPS'25) — Small batch sizes (even batch=1) can stably train LLMs; challenges the large-batch orthodoxy

**Inference Acceleration & Model Compression** — Techniques for faster or cheaper inference through early exit, speculative decoding, layer skipping, quantization, and low-rank compression.
- [[2609.28399|MA]], [[2608.09703|Matryoshka LM Suites]], [[2605.31124|QVGGT]] (CVPR'26), [[2602.05179|Parallel-DP-GPU]] (ICLR'26), [[2511.15190|GSIM]], [[2510.01143|Bridge-Parallel-Scaling]] (ICLR'26), [[2507.10069|ElasticMM]] (NeurIPS'25 Oral), [[2507.00754|LUViT]], [[2505.23416|KVzip]] (NeurIPS'25 Oral), [[2505.11820|CoLM]] (NeurIPS'25), [[2505.08022|RobustDLRT]] (NeurIPS'25 Oral), [[2404.16710|LayerSkip]], [[1703.09844|MSDNet]]

> [!star] Key Papers
> - [[2404.16710|LayerSkip]] — Enables accurate early exit and self-speculative decoding for faster LLM inference
> - [[2505.11820|CoLM]] (NeurIPS'25) — Chain-of-Model enables incremental scaling and elastic adaptation

**Sparse Autoencoders for Interpretability** — Using sparse autoencoders to decompose model activations into interpretable features and concepts.
- [[2604.28119|SAE-Concept-Manifolds]], [[2603.02908|SAE-Crystal-Ball]] (ICLR'26), [[2602.06218|SAE-A]] (ICLR'26), [[2506.15679|Dense-SAE-Latents]] (NeurIPS'25), [[2502.03714|USAE]] (ICML'25), [[2409.14507|Feature-Absorption-SAE]] (NeurIPS'25 Oral), [[2309.08600|Sparse Autoencoders]] (ICLR'24)

> [!star] Key Papers
> - [[2506.15679|Dense-SAE-Latents]] (NeurIPS'25) — Redefines dense latents in Sparse Autoencoders from artifacts to functional features

**Prototype-Based Interpretable Models** — Vision models that classify by comparing inputs to learned, human-inspectable prototypes.
- [[2410.20722|ProtoViT]] (NeurIPS'24), [[2208.10431|ProtoPFormer]], [[1806.10574|ProtoPNet]]

**Attribution & Adversarial Robustness Methods** — Classic feature-attribution and adversarial-perturbation methods for explaining and stress-testing model predictions.
- [[1706.06083|PGD Adversarial Training]] (ICLR'18), [[1706.05394|Memorization in Deep Networks]] (ICML'17), [[1704.02685|DeepLIFT]] (ICML'17), [[1703.01365|Integrated Gradients]] (ICML'17), [[1412.6572|FGSM]] (ICLR'15), [[0912.1128|Local Explanation Vectors]]

**Representation Analysis & Probing** — Analyzing what internal representations encode and how they change across layers, tasks, and training regimes.
- [[2607.14228|SeeSE3]], [[2605.12733|Generalist-to-Specialist-Rep]] (ICML'26), [[2603.12228|Neural-Thickets]], [[2602.03783|KernelSM]] (ICLR'26), [[2602.00462|LatentLens]] (ICML'26), [[2510.25943|InputDSA]] (ICLR'26), [[2509.20234|Texture-Bias-Revisited]] (NeurIPS'25 Oral), [[2502.02013|Layer-by-Layer-Representations]] (ICML'25 Oral), [[2205.10268|B-cos-Networks]] (CVPR'22)

> [!star] Key Papers
> - [[2502.02013|Layer-by-Layer-Representations]] (ICML'25 Oral) — Intermediate layers often provide superior downstream representations compared to final layers

**Additional methods** — Papers referenced in this section that don't fit the categories above.
- [[2608.05806|HiLP]], [[2605.15871|AIRA-Compose]], [[2507.18074|ASI-ARCH]], [[2507.02092|EBT]] (ICLR'26 Oral), [[2505.09343|DeepSeek-V3]], [[2404.05090|Model Collapse Statistical Analysis]], [[1907.04307|Multilingual USE]], [[1905.11946|EfficientNet]] (ICML'19)

> [!star] Key Papers
> - [[2507.18074|ASI-ARCH]] — Autonomous system that discovers novel transformer architectures via automated search
> - [[2505.09343|DeepSeek-V3]] — Hardware-software co-design strategy achieving SOTA LLM performance

> [!tip] The Muon Moment
> 2025 may be remembered as the year AdamW lost its monopoly. Muon (and its distributed variant MuLoCo) demonstrated that second-order optimization is practical at LLM scale. Combined with scaling law insights (MPL, small-batch training), the training recipe for LLMs is being fundamentally rewritten.

---

## 7. Efficient Adaptation & Model Composition

Making foundation models practical: parameter-efficient fine-tuning, model merging, prompt tuning, and efficient transfer.

**Prompt Learning** — Adapting foundation models through learned prompts rather than full fine-tuning.
- [[2309.16797|PromptBreeder]] (ICML'24), [[2203.12119|VPT (Visual Prompt Tuning)]], [[2203.05557|CoCoOp]] (CVPR'22), [[2109.01134|CoOp]], [[2104.08691|Prompt Tuning]]

> [!star] Key Papers
> - [[2109.01134|CoOp]] — Learnable prompts for adapting CLIP without fine-tuning; launched the prompt learning field
> - [[2309.16797|PromptBreeder]] (ICML'24) — Self-referential self-improvement via prompt evolution; automates prompt engineering

**LoRA & Parameter-Efficient Fine-Tuning** — Methods that adapt large models by training only a small fraction of parameters.
- [[2607.05938|Prior-First, Condition-Second]], [[2604.19254|ShadowPEFT]], [[2507.11851|Gated-LoRA]], [[2506.20629|PLoP]] (ICLR'26), [[2506.06105|T2L]] (ICML'25), [[2504.13292|GrokTransfer]] (ICLR'25), [[2502.16025|FeatSharp]] (ICML'25), [[2410.19878|PEFT-Methodologies-Survey]], [[2406.10973|ExPLoRA]] (ICML'25), [[2405.09673|LoRA-Learns-Less]] (ICLR'25), [[2312.12148|PEFT-Critical-Review]], [[2310.20587|LaMo]] (ICLR'24), [[1902.00751|Adapters]]

> [!star] Key Papers
> - [[2506.06105|T2L]] (ICML'25) — Text-to-LoRA: hypernetwork that dynamically generates task-specific LoRA adapters from text descriptions
> - [[2507.11851|Gated-LoRA]] — Enables pretrained autoregressive LLMs to perform multi-token prediction via gated LoRA modules

**Model Merging & Weight Averaging** — Combining multiple fine-tuned models into a single improved model without retraining.
- [[2609.33125|PolicyWeave]], [[2605.14386|Darwin]] (NeurIPS'26), [[2604.27155|GeoMerge]], [[2602.05943|Orthogonal-Model-Merging]], [[2512.13043|GTR-Turbo]] (CVPR'26), [[2512.05117|Universal Weight Subspace Hypothesis]], [[2510.21223|FDA]], [[2505.12082|PMA]] (NeurIPS'25), [[2408.07666|Model-Merging-in-LLMs/MLLMs]], [[2407.13771|Training-Free-Model-Merging-MTDA]] (ECCV'24), [[2403.13257|MergeKit]], [[1803.05407|SWA]]

> [!star] Key Papers
> - [[1803.05407|SWA]] — Stochastic Weight Averaging: simple technique that finds wider optima and better generalization
> - [[2505.12082|PMA]] (NeurIPS'25) — Pre-trained Model Average for effective merging of LLM checkpoints

**On-Policy Distillation Algorithms for LLMs** — Self-distillation and teacher-guided objectives that train student LLMs on their own on-policy rollouts during post-training.
- [[2609.36484|RIDE-OPD]], [[2609.30652|DCE]], [[2609.08798|OPRD]], [[2609.05295|RISE-PolicyDistillation]], [[2609.02998|TGOPD]], [[2608.24696|OPDVR]], [[2608.01735|DAPD]], [[2607.15161|OPD^2]], [[2607.05394|Direct-OPD]], [[2607.05339|TREK]], [[2607.04751|TOP-D]], [[2606.30626|DOPD]], [[2605.07465|SEIF]], [[2605.07396|ROPD]], [[2605.03677|Uni-OPD]], [[2604.14084|TIP]], [[2604.13010|Lightning-OPD]], [[2603.07079|EOPD]] (ICML'26), [[2601.20802|SDPO]], [[2601.18734|OPSD]]

**On-Policy Distillation for Multimodal, Agentic & Long-Horizon Settings** — On-policy distillation adapted to vision-language and video models, multi-turn agents, and long-context training.
- [[2609.32416|RE-0]], [[2608.14144|S2VOPD]], [[2608.01263|FP-OPD]], [[2607.28590|VAD]], [[2607.24731|PDM]], [[2607.14777|SEED]], [[2607.08766|OPSD-V]], [[2607.05804|TurnOPD]], [[2607.04763|ReOPD]], [[2605.12913|DAgger-for-Agents]], [[2604.28123|PRISM]], [[2604.17535|OPSDL]], [[2510.23497|VOLD]]

**On-Policy Distillation Studies & Surveys** — Empirical and theoretical analyses of why and when on-policy distillation works, plus field surveys.
- [[2609.32722|Same-Family-OPD]], [[2609.04172|One-Shot OPD]], [[2608.31046|OPSA]], [[2607.05184|Fork Suppression]], [[2606.24143|AsyncOPD]], [[2606.07082|On-Policy-Distillation-Geometry]], [[2604.13016|OPD-Distillation-Study]], [[2604.00626|On-Policy-Distillation-Survey]]

**Teacher-Student Distillation for Robot Control** — RMA-style distillation that transfers a privileged, simulation-trained teacher policy into a deployable sensor-limited student controller.
- [[2609.20756|OPTED]], [[2607.07357|HUMAIN]] (IROS'26), [[2607.02332|HEFT]], [[2607.02037|Cross-Platform ASV RL]], [[2606.30474|GOMP]], [[2603.08763|SPREAD]], [[2601.05407|HINT]], [[2310.04582|PULSE]] (ICLR'24 Spotlight), [[2309.14341|Extreme Parkour]], [[2309.05665|Robot Parkour]] (CoRL'23), [[2211.07638|Egocentric Legged Locomotion]] (CoRL'22)

**Vision, Multimodal & Domain-Adaptive Distillation** — General-purpose vision, multimodal, and domain-adaptive teacher-student and multi-teacher distillation methods.
- [[2607.21556|VCSD]], [[2607.10762|TOLiD]], [[2607.10082|Event-Image Dual-Stage Distillation]], [[2607.06957|Flow-ERD]], [[2606.08432|Trajectory-Refined-Distillation]], [[2602.05449|DisCa]], [[2512.22238|Mask-Teacher-Distill]], [[2508.04816|CoMAD]], [[2505.11221|LVLM2P]], [[2505.07675|DHO]], [[2503.11339|CSD]] (ICLR'26), [[2502.02538|FQL]] (ICML'25), [[2412.14446|VLM-AD]] (CoRL'25), [[2312.06709|AM-RADIO]] (CVPR'24)

**Reasoning, Agent & Language Distillation** — Distilling reasoning, chain-of-thought, and agentic capability from larger models into smaller or more efficient ones.
- [[2609.33378|RHD]], [[2609.24974|Harness-Zero]], [[2609.20791|StageGuard]], [[2608.25622|RefineCut]], [[2608.15763|HAT]], [[2605.21699|X-Token]], [[2604.01193|SSD-Code-Generation]], [[2603.24422|OneSearch-V2]], [[2603.16856|OEL]], [[2508.13167|CoA]], [[2507.05707|Agentic-R1]], [[2506.17486|PRISM-SLM]] (CoRL'25), [[2506.14728|AgentDistill]], [[2505.13975|DRP]], [[2504.15257|FlowReasoner]], [[2502.21074|CODI]], [[2311.01460|Implicit CoT]], [[2306.08543|MiniLLM]] (ICLR'24)

> [!star] Key Papers
> - [[2306.08543|MiniLLM]] (ICLR'24) — Foundational KD method for LLMs using reverse KL divergence; set the standard for language model compression
> - [[2312.06709|AM-RADIO]] (CVPR'24) — Agglomerative multi-teacher distillation unifying CLIP, DINOv2, and SAM into one vision foundation model
> - [[2506.14728|AgentDistill]] — Training-free agent distillation via generalizable MCP boxes; bridges large and small agent models

**Continual Pretraining & Domain Adaptation** — Extending foundation models to new domains or tasks through continued training.
- [[2609.06986|Long-Horizon Memorization]], [[2607.05665|Morphological Similarity Transfer Learning]], [[2606.02280|LDG]], [[2603.17655|CC-CDFSL]] (CVPR'26), [[2602.02381|AdaSSL]] (ICLR'26), [[2601.21725|Procedural-Pretraining]] (ICML'26), [[2511.13945|Procedural-Warm-Up]], [[2509.06806|MachineLearningLM]], [[2507.06187|Delta-Learning-Hypothesis]], [[2507.00994|MLM-vs-CLM-Pretraining]] (ICLR'26), [[2505.01812|New-News]], [[2504.07745|SF2T]] (CVPR'25), [[2504.06608|Cross-Domain-FSL-with-DKM]], [[2410.02355|AlphaEdit]], [[1703.05175|Prototypical Networks]] (NeurIPS'17), [[1411.1792|Transferable Features]] (NeurIPS'14)

> [!star] Key Papers
> - [[2509.06806|MachineLearningLM]] — Continued pretraining framework that enhances LLMs with robust many-shot in-context learning for ML tasks
> - [[2507.06187|Delta-Learning-Hypothesis]] — Preference tuning on pairs of individually weak outputs can yield strong gains

**Gradient-Free & Evolutionary Optimization** — Optimizing models without gradient computation using evolution strategies.
- [[2602.03120|QES]], [[2511.16652|EGGROLL]], [[2510.10603|EA4LLM]], [[2402.12479|Pruned-Networks-in-Deep-RL]] (ICML'24), [[1703.03864|OpenAI ES]]

> [!star] Key Papers
> - [[2510.10603|EA4LLM]] — Demonstrates evolutionary algorithms can effectively optimize LLMs without gradients; opens a new fine-tuning paradigm
> - [[2602.03120|QES]] — Quantized evolution strategies achieving high-precision fine-tuning at low-precision cost; practical gradient-free optimization

**Symmetry & Loss Landscape Theory** — Theoretical understanding of parameter space structure and its implications for training and merging.
- [[2509.11348|MoE-Mode-Connectivity]] (NeurIPS'25 Oral), [[2506.22712|Generalized-Linear-Mode-Connectivity]] (NeurIPS'25 Oral), [[2506.17093|Polynomial-NN-Identifiability]] (NeurIPS'25 Oral), [[2506.13018|NN-Parameter-Space-Symmetry-Survey]], [[2506.06259|Franz-Parisi-Criterion]] (NeurIPS'25 Oral), [[2505.14185|Safety-Subspaces]] (ICLR'26), [[2505.13631|ACE-Equivariance]] (NeurIPS'25 Oral)

> [!star] Key Papers
> - [[2506.13018|NN-Parameter-Space-Symmetry-Survey]] — First comprehensive survey of symmetries in neural network parameter spaces; foundational for understanding model merging and loss landscape geometry

**Additional methods** — Papers referenced in this section that don't fit the categories above.
- [[2402.15109|MU-Mis]] (ICLR'26)

> [!star] Key Papers
> - [[2402.15109|MU-Mis]] (ICLR'26) — Remaining-data-free unlearning via sample contribution suppression; enables privacy compliance without retaining original data

> [!tip] The Adaptation Toolkit
> The modern practitioner's stack: LoRA for efficient fine-tuning, SWA/PMA for merging multiple checkpoints, PromptBreeder for automated prompt optimization, and T2L for on-the-fly adapter generation. The key insight from 2025: you rarely need to fine-tune the full model — the right adapter strategy often matches or exceeds full fine-tuning.

---

## 8. RL for LLM Reasoning

Reinforcement learning applied to improve language model reasoning, self-improvement, and verifiable reward systems.

**RL-as-Pretraining, Self-Play & Data Scaling** — Using RL rollouts as a pretraining objective and scaling self-play or verifiable-reward data to pretraining-scale volumes.
- [[2609.30063|Zero-Data Self-Play]], [[2609.22068|CodeMidas]], [[2607.12395|Ring-Zero]], [[2604.20209|SGS]], [[2512.16649|JustRL]] (ICLR'26), [[2512.03442|PretrainZero]], [[2511.17473|MR-RLVR]], [[2510.06499|Webscale-RL]] (ICLR'26), [[2510.01265|RLP]] (ICLR'26), [[2508.05004|R-Zero]] (ICLR'26), [[2506.08007|RPT]], [[2506.00103|Writing-Zero]], [[2505.03335|Absolute-Zero]] (NeurIPS'25 Spotlight)

> [!star] Key Papers
> - [[2503.23829|RLVR]] — Extends RL with verifiable rewards beyond math/code to diverse domains
> - [[2510.06499|Webscale-RL]] (ICLR'26) — Automated pipeline scaling verifiable RL training data to pretraining levels
> - [[2512.16649|JustRL]] (ICLR'26) — Simplified RL recipe effectively scales a 1.5B model for mathematical reasoning

**Policy Optimization, Reward Modeling & Verification** — Policy-optimization algorithm variants, reward-model scaling, and self-verification methods for RL with verifiable rewards.
- [[2609.13058|ESRL]], [[2605.12227|dGRPO]], [[2604.20733|NPO]], [[2604.17654|Poly-EPO]], [[2604.02288|SRPO]], [[2509.26074|LENS-Reward]] (NeurIPS'25), [[2508.18588|RhymeRL]], [[2508.14460|DuPO]], [[2506.08388|RLTs]] (NeurIPS'25), [[2503.23829|RLVR]], [[2402.03300|DeepSeekMath]], [[2210.10760|RM Overoptimization]] (ICML'23)

**Reasoning Models** — LLMs explicitly trained for multi-step reasoning with RL.
- [[2603.02556|VC-STaR]] (ICLR'26 Oral), [[2512.12623|DMLR]], [[2510.00219|Thoughtbubbles]], [[2508.03613|Goedel-Prover-V2]] (ICLR'26), [[2507.18071|GSPO]], [[2506.10910|Magistral]], [[2505.16993|SeNaTra]] (NeurIPS'25), [[2505.11484|SoftCoT++]], [[2505.10320|J1]] (ICLR'26), [[2503.16219|Open-RS]], [[2503.14858|CRL]] (NeurIPS'25 Oral), [[2502.03275|Token-Assorted]], [[2501.12948|DeepSeek-R1]], [[2408.03314|Test-Time Compute Scaling]], [[2403.09629|Quiet-STaR]], [[2401.08967|ReFT]], [[2203.14465|STaR]] (NeurIPS'22)

> [!star] Key Papers
> - [[2501.12948|DeepSeek-R1]] — RL-only training (no SFT) elicits emergent chain-of-thought reasoning; established the RL-for-reasoning paradigm the field now builds on
> - [[2506.10910|Magistral]] — Mistral's first reasoning model using custom RLHF for chain-of-thought
> - [[2505.10320|J1]] (ICLR'26) — RL-trained LLM-as-a-Judge that incentivizes genuine thinking during evaluation

**LLM-as-a-Judge & Evaluation** — Using LLMs to evaluate other LLMs, with RL to improve judging quality.
- [[2508.19229|StepWiser]], [[2505.10320|J1]] (ICLR'26), [[2411.15594|LLM-as-a-Judge]]

> [!star] Key Papers
> - [[2411.15594|LLM-as-a-Judge]] — Comprehensive survey providing formal definitions and unified taxonomy for LLM-based evaluation

**Agentic RL & Search** — RL applied to LLM-based agents for tool use, search, and multi-step task completion.
- [[2603.28963|AutoWorld]], [[2603.26499|AIRA2]], [[2603.12011|RFT-LLM-Agent-Generalization]], [[2603.11327|MR-Search]], [[2602.05842|RWML]], [[2408.10899|ARIO]]

> [!star] Key Papers
> - [[2603.11327|MR-Search]] — Meta-RL framework enabling LLM search agents to improve via in-context learning
> - [[2603.12011|RFT-LLM-Agent-Generalization]] — Systematic investigation of whether reinforcement fine-tuning improves LLM agent generalization

**Unsupervised & Self-Supervised LLM Alignment** — Aligning language models without explicit human feedback through self-supervised objectives.
- [[2605.11609|AntiSD]], [[2602.20574|GATES]], [[2508.03682|SQLM]], [[2507.06187|Delta-Learning-Hypothesis]], [[2506.10139|ICM]]

> [!star] Key Papers
> - [[2508.03682|SQLM]] — Self-Questioning Language Models that generate their own training signal; eliminates dependence on human preference data
> - [[2506.10139|ICM]] — Unsupervised elicitation of language model capabilities without labeled examples; reveals latent model knowledge

**Self-Evolving & Self-Improving Agents** — LLM systems that autonomously improve their capabilities through self-play, self-generated data, or evolutionary strategies.
- [[2606.20657|A-Evolve-Training]], [[2604.03128|Self-Distilled-RLVR]], [[2603.29640|ASI-Evolve]], [[2601.10094|V-Zero]], [[2601.07055|Dr.-Zero]], [[2601.05877|iReasoner]], [[2512.20605|Internal-RL]], [[2512.06835|DoGe]], [[2512.02472|R-FEW]], [[2511.16672|EvoLMM]], [[2511.16043|Agent0]], [[2511.15661|VisPlay]], [[2511.13054|ViSS-R1]], [[2511.10395|AgentEvolver]], [[2510.16416|SSL4RL]], [[2510.16333|PIVOT]] (ICLR'26), [[2412.02674|GV-Gap]]

> [!star] Key Papers
> - [[2511.16043|Agent0]] — Self-evolving agents from zero data via tool-integrated reasoning; paradigm for autonomous agent improvement
> - [[2511.16672|EvoLMM]] — Self-evolving multimodal models with continuous rewards; bridges RL and self-improvement for vision-language agents
> - [[2601.10094|V-Zero]] — Self-improving multimodal reasoning with zero annotation; proves annotation-free self-improvement is viable

> [!tip] The RL-for-Reasoning Stack
> Post-DeepSeek-R1, the recipe is clear: start with SFT for format, then RL with verifiable rewards for reasoning. Webscale-RL showed you can automate reward data collection at pretraining scale. JustRL proved even a 1.5B model benefits. The frontier is extending verifiable rewards beyond math/code (Writing-Zero, RLVR).

---

## 9. Embodied Foundation Models

Foundation models applied to robotics — VLAs, action pretraining, world models, and sim-to-real transfer.

**Foundational & Generalist Manipulation VLA Models** — The flagship large-scale, general-purpose VLA systems trained on diverse real-robot manipulation data.
- [[2609.38164|Rho]], [[2609.14973|PhysBrain 1.5]], [[2607.15330|Xiaomi-Robotics-1]], [[2603.25406|MMaDA-VLA]], [[2602.12062|HoloBrain-0]], [[2602.11236|ABot-M0]], [[2601.18692|LingBot-VLA]], [[2512.15840|LV-P]], [[2512.00975|MM-ACT]], [[2510.10274|X-VLA]] (ICLR'26), [[2509.22652|DAWN]] (CVPR'26), [[2509.00576|G0]], [[2508.07917|MolmoAct]], [[2504.16054|π0.5]], [[2501.18867|UP-VLA]] (ICML'25), [[2501.15830|SpatialVLA]], [[2501.03575|Cosmos]], [[2412.14058|RoboVLMs]], [[2410.24164|π0]] (RSS'25), [[2409.20537|HPT]] (NeurIPS'24 Spotlight), [[2306.14896|RVT]] (CoRL'23), [[2205.06175|Gato]] (ICLR'24), [[2204.06252|HULC]]

> [!star] Key Papers
> - [[2504.16054|π0.5]] — VLA model enabling mobile robots to perform complex household tasks in entirely new homes
> - [[2512.00975|MM-ACT]] — Unified VLA model integrating text, image, and robot actions into a single multimodal framework
> - [[2508.07917|MolmoAct]] — Action Reasoning Models integrating depth-aware perception with visual reasoning for spatial tasks

**VLA Training Methodology: RL, Distillation & Test-Time Adaptation** — Algorithmic training recipes for VLA models: RL fine-tuning, on-policy distillation, continual learning, and test-time adaptation.
- [[2609.34250|WAM On-Policy Distillation]], [[2609.24682|World-Model-to-VLA Distillation]], [[2609.18242|ForceDelta-VLA]], [[2607.12892|UR-VC]], [[2606.29892|T2VLA]], [[2604.19730|FASTER]], [[2603.26666|VLA-OPD]], [[2603.11653|VLA-RL-Continual-Learning]] (ICRA'26 Workshop), [[2602.01067|LBM Co-training Study]] (RSS'26)

**VLA Representation, Reasoning & Alignment** — Representation-anchoring, latent-alignment, JEPA-based, and chain-of-thought reasoning methods for VLA models.
- [[2609.25558|GC-VLA]], [[2609.04193|GIFT-Manip]], [[2608.30643|Temporal Forcing]], [[2608.30378|PAVE]], [[2608.03563|UVT]] (IROS'26), [[2607.25912|SAM3D-VLA]], [[2607.24485|τ]], [[2607.23969|LeapBot-WA]], [[2607.13597|Semantic Anchoring]], [[2607.13429|Anchor-Align]], [[2607.01586|VLAFlow]], [[2606.31167|MIRTH]], [[2606.30552|ZR-0]], [[2602.19710|Pose-VLA]], [[2602.11832|JEPA-VLA]], [[2602.10098|VLA-JEPA]], [[2602.08167|R&B-EnCoRe]] (RSS'26), [[2506.22242|4D-VLA]] (NeurIPS'25), [[2505.03500|TLI]]

**Efficient, Fast & Lightweight VLA Control** — Efficiency-focused VLA methods: fast action tokenization, lightweight distillation, and real-time control policies.
- [[2609.29382|Exit Transformers]], [[2607.27205|TurboVLA]], [[2607.26657|Enfold]], [[2607.06564|Lift3D-VLA]], [[2607.04171|XS-VLA]], [[2604.02408|F2F-AP]], [[2603.16195|S-VAM]], [[2509.04996|FLOWER]] (CoRL'25), [[2505.08971|PRIOR]], [[2501.09747|FAST]] (RSS'25)

**Navigation & Cross-Platform VLA Scaling** — Foundation models and scaling pipelines for vision-and-language navigation and cross-platform VLA deployment.
- [[2609.29934|Spatial-Nav]], [[2609.03906|TopoMacro VLN-CE]], [[2607.23743|Traversability-Aware Global Planner]], [[2607.20679|CAT-Nav]] (IROS'26), [[2602.18803|LoTIS]] (RSS'26), [[2509.11480|VLA-Cross-Platform-Scaling]], [[2503.03921|CREStE]] (RSS'25), [[2307.15644|ScaleVLN]], [[2306.14846|ViNT]] (CoRL'23), [[2105.06453|E.T. (Episodic Transformer)]]

**Foundational Latent-Action & Video-Action Learning** — Core methods for learning action representations and goal-conditioned control from video and interaction data without explicit action labels.
- [[2609.23478|Latent-Action Consistency Audit]], [[2606.11525|IWR]], [[2509.19958|MotoVLA]] (CoRL'25), [[2410.11758|LAPA]] (ICLR'25), [[2410.06158|GR-2]], [[2409.16283|Gen2Act]] (CoRL'25), [[2402.15391|Genie]] (ICML'24 Oral), [[2310.08576|AVDC]] (ICLR'24 Spotlight), [[2306.10007|RPT]] (CoRL'23), [[2305.02195|CALM]], [[2203.12601|R3M]] (CoRL'22), [[2112.01511|VINN]]

> [!star] Key Papers
> - [[2410.11758|LAPA]] (ICLR'25) — Latent Action Pretraining from videos; learns action representations without action labels
> - [[2310.08576|AVDC]] (ICLR'24 Spotlight) — Learns manipulation tasks from actionless video via dense visual correspondences

**Robot Datasets & Benchmarks for Action Learning** — Large-scale robot manipulation, egocentric human-activity, and hand-object datasets and benchmarks used to pretrain and evaluate action representations.
- [[2607.25895|HiFi-UMI]], [[2510.08807|Humanoid-Everyday]], [[2504.13059|RoboTwin]] (CVPR'25), [[2503.06669|AgiBot-World]], [[2412.18194|VLABench]] (ICCV'25), [[2411.08380|EgoVid-5M]], [[2403.19417|OAKINK2]] (CVPR'24), [[2310.08864|OXE]], [[2309.17024|HoloAssist]], [[2308.12952|BridgeData-V2]] (CoRL'23), [[2307.00595|RH20T]] (ICRA'24), [[2306.03310|LIBERO]] (NeurIPS'23), [[2203.14712|Assembly101]], [[2203.01577|HOI4D]] (CVPR'22), [[2109.13396|Bridge]]

**Recent Action-Representation & World-Guided Pretraining Methods** — Newer methods for pretraining action representations, including world-model-guided, outcome-regularity, and task-agnostic approaches.
- [[2609.40341|Ego4WAM]], [[2609.10706|HuRo]], [[2607.18236|Patch Policy]], [[2607.15163|Humanoid Transformer]], [[2607.11427|EDAR]], [[2607.04714|GeoMoLa]], [[2607.02466|TAP]] (ICML'26), [[2606.30749|G2D-Pretrain]], [[2606.29834|STEAM]], [[2606.29517|CORE (Outcome Regularities)]], [[2606.28320|WARP-RM]], [[2606.12366|APT-VLA]], [[2604.19734|UniT]], [[2602.22010|WoG]], [[2602.12215|LDA-1B]] (RSS'26), [[2601.02427|NitroGen]], [[2512.13030|Motus]], [[2512.07203|MMRPT]], [[2511.21428|LAPS]] (CVPR'26), [[2511.16407|LAOF]] (CVPR'26), [[2511.07820|SONIC]], [[2508.17230|FVP]] (ICCV'25), [[2502.14795|Humanoid-VLA]]

**Foundational World Models & Model-Based RL** — The classic lineage of learned world models and model-based RL methods for planning.
- [[2609.30264|AD-WM]], [[2607.26712|ActSWM]], [[2606.05555|MR.Q]], [[2410.00564|JOWA]] (ICLR'25), [[2310.16828|TD-MPC2]] (ICLR'24 Spotlight), [[2005.05960|Plan2Explore]] (ICML'20), [[1809.01999|World Models]], [[1507.00814|Predictive Exploration Bonus]]

**Autonomous Driving World Models** — World models specifically for autonomous-driving perception, occupancy prediction, and planning.
- [[2607.15898|Orbis 2]], [[2607.04541|CRISP]], [[2510.12796|DriveVLA-W0]] (ICLR'26), [[2407.21126|LOPR]] (RSS'25), [[2311.16038|OccWorld]] (ECCV'24)

**Latent-Action & JEPA-Based World Models for Robotics** — World models built on latent-action and JEPA-style representations for robot planning and control.
- [[2610.00722|JEPA-TTT]], [[2609.37250|V-JEPA Policy]], [[2609.34375|LRC-JEPA]], [[2609.29171|RWM-LatentPlan]], [[2609.24749|Decision-Aligned JEPA]], [[2609.03565|Physically Grounded JEPA]], [[2607.26924|TC-LeWM]], [[2607.26056|INTACT]], [[2607.25337|Temporal-Distance-JEPA]], [[2607.09185|CD-LAM]], [[2607.04978|Qantara]], [[2606.32026|AdaJEPA]], [[2605.00078|Being-H0.7]], [[2603.19312|LeWM]], [[2602.23058|GeoWorld]] (CVPR'26), [[2602.11389|Causal-JEPA]] (ICML'26), [[2602.06949|DreamDojo]], [[2602.06130|SWIRL]], [[2601.05230|Latent-Action-World-Models]], [[2512.24497|JEPA-WM]], [[2512.23541|Act2Goal]] (RSS'26), [[2510.00739|TD-JEPA]] (ICLR'26 Oral), [[2507.19468|DINO-world]], [[2504.16591|JEPA-for-RL]], [[2502.14819|PLDM]] (NeurIPS'25), [[2411.04983|DINO-WM]] (ICML'25)

**Recent World-Model Architectures & Physics Simulation** — Recent world-model architectures, physics-aware simulators, and self-improving dynamics models.
- [[2610.02120|SkeleWAM]], [[2610.02054|UniWAM]], [[2609.39870|Magic-W0]], [[2609.39685|RoboCoach]], [[2609.38163|ReWAM]], [[2609.38059|WorldLine]], [[2609.34968|RoboFL]], [[2609.33218|Scope-WM]], [[2609.29092|DAWN-Parkour]], [[2609.27455|LeWAM]], [[2609.23888|HapticWAM]], [[2609.15570|DIDO]], [[2607.28415|QQWorld]], [[2607.28391|TacWAM]], [[2607.27924|ODEWorld]], [[2607.27017|POKEWORLD]], [[2607.25918|DC-WAM]]

**Recent World-Model Architectures & Physics Simulation · part 2** - Continuation of the list above.
- [[2607.21576|SDM]], [[2607.19191|ABot-World-0]], [[2607.02195|BRIDGE-WA]], [[2606.30534|Orca]], [[2606.29501|A2World]] (ECCV'26), [[2606.27364|PhysiFormer]], [[2605.03821|RoboAlign-R1]], [[2604.10333|ZWM]], [[2604.03208|HWM]], [[2604.01985|WAV]], [[2603.29090|HCLSM]], [[2603.12231|Temporal-Straightening]] (ICML'26), [[2512.09929|OWM]], [[2511.09057|PAN]], [[2506.17774|PhysiX]]

> [!star] Key Papers
> - [[2511.09057|PAN]] — World model using Generative Latent Prediction for general, interactable, long-horizon simulation
> - [[2603.12231|Temporal-Straightening]] (ICML'26) — Geometric regularization for straighter latent trajectories; improves latent planning

**Simulation Environments & Reset/Training Platforms** — Simulators, reset systems, and robotics software platforms for training and evaluating robotic manipulation and interaction.
- [[2604.17513|FLASH]], [[2604.04310|frax]] (ICRA'26 Workshop), [[2603.15789|OmniReset]] (ICLR'26), [[2603.03279|ULTRA]], [[2603.03026|URGT]], [[2506.10966|GenManip]] (CVPR'25), [[2003.08515|SAPIEN]] (CVPR'20)

> [!star] Key Papers
> - [[2003.08515|SAPIEN]] (CVPR'20) — Simulated environment with 2,346 articulated objects; foundational platform for robot manipulation research

**Robot State Estimation & Geometric Perception** — Learned-geometry and state-estimation methods for robot localization, odometry, and large-scale reconstruction.
- [[2605.10456|POLI]] (RSS'26), [[2509.10405|LED-State Pose Estimation]] (CoRL'25), [[2506.02587|BEVCALIB]] (CoRL'25), [[2504.09495|Hierarchical IMU Debiasing]] (RSS'25), [[2502.04640|XM]] (RSS'25), [[2311.04320|DRIFT (Dead Reckoning)]]

**Additional methods** — Papers referenced in this section that don't fit the categories above.
- [[2609.27095|Embodiment Diversity Scaling]], [[2607.24959|IFT Contact Differentiation]], [[2607.24538|NEO]], [[2607.23108|Curse of Precision]] (ICRA'26), [[2512.10950|E-RayZer]] (CVPR'26), [[2511.21395|Monet]], [[2511.20639|LatentMAS]] (ICML'26 Spotlight), [[2209.08959|TACO-RL]] (CoRL'22), [[1803.09956|VPG]] (IROS'18)

> [!tip] The VLA Pipeline
> Modern VLAs follow a pattern: large-scale pretraining on internet video (LAPA) or diverse robot data (pi0.5), then RL fine-tuning for specific tasks (VLA RL Continual Learning). World models (PAN, Causal-JEPA) are emerging as the "imagination engine" that enables sample-efficient policy learning without costly real-world interaction.

---

## 10. Emerging Methods

Unconventional approaches that do not fit neatly into the above categories but represent important research directions.

**Neuromorphic, Bio-Inspired & Neural Decoding** — Learning algorithms inspired by biological neural mechanisms, and self-supervised methods for long-term neural decoding in brain-machine interfaces.
- [[2607.24031|UnSPC]], [[2607.24023|SSCDL]], [[2607.20743|Bio-Inspired Self-Supervised Trajectory Planner]], [[2607.18737|SOM-ESN Motion Primitive Model]], [[2506.05259|RHEL]] (NeurIPS'25 Oral), [[2505.24161|Proxy-Target-SNN]] (NeurIPS'25), [[2505.18361|Tactile-CRNN]] (NeurIPS'25 Oral), [[2307.04054|Deep-STDP]]

> [!star] Key Papers
> - [[2307.04054|Deep-STDP]] — Spike-timing-dependent plasticity for deep unsupervised learning; explores biologically plausible alternatives to backpropagation

**LLM-Assisted Research Tools** — Using LLMs to automate aspects of the research process itself.
- [[2604.09258|Nexus]], [[2508.17971|LLM-NAR]], [[2504.17192|PaperCoder]] (ICLR'26), [[2203.03485|Self-directed-Exploratory-Planning]]

> [!star] Key Papers
> - [[2504.17192|PaperCoder]] (ICLR'26) — Multi-agent LLM framework that generates functional code from scientific papers
> - [[2508.17971|LLM-NAR]] — Integrates LLMs with Graph Neural Networks for multi-agent path finding

**Diffusion & Autoregressive Generation: Architectures, Tokenization & Control** — Core and efficient generative-model architectures for image and video synthesis, tokenization and representation-alignment techniques, and style-, subject- and layout-controlled generation.
- [[2608.01306|SPAE]], [[2607.21585|EFM]], [[2605.16147|Register Guidance]], [[2604.09168|ELT]] (ECCV'26), [[2603.28713|DreamLite]], [[2603.22187|VFLM]] (CVPR'26), [[2512.05665|ILVR]], [[2511.20645|PixelDiT]] (CVPR'26), [[2511.20549|Flash-DMD]], [[2508.18966|USO]], [[2411.10231|TaylorIR]], [[2410.06940|REPA]] (ICLR'25 Oral), [[2408.06072|CogVideoX]] (ICLR'25), [[2406.07550|TiTok (32 Tokens Reconstruction)]] (NeurIPS'24), [[2312.02116|GIVT]] (ECCV'24), [[2307.01952|SDXL]] (ICLR'24 Spotlight), [[2212.09748|DiT]], [[2209.14916|MDM]] (ICLR'23 Oral), [[2102.12092|DALL-E]] (ICML'21 Spotlight), [[1711.00937|VQ-VAE]] (NeurIPS'17)

> [!star] Key Papers
> - [[2212.09748|DiT]] — Diffusion Transformer replacing U-Net backbone; established the transformer-based diffusion architecture underlying modern generative video/image models
> - [[2508.18966|USO]] — Unified style and subject-driven generation via disentangled reward learning; achieves controllable personalization

**Video & 3D Scene Generation** — Generating and reconstructing video and 3D scenes with generative models.
- [[2607.15038|Wan-Streamer v0.3]], [[2607.05373|PixWorld]], [[2510.08575|ReSplat]] (ECCV'26 Spotlight), [[2503.20314|Wan]], [[2308.06571|ModelScopeT2V]]

**DETR-Family Transformer Detectors** — End-to-end transformer-based object detectors descending from DETR.
- [[2406.03459|LW-DETR]], [[2304.08069|RT-DETR]] (CVPR'24), [[2010.04159|Deformable DETR]] (ICLR'21 Oral), [[2005.12872|DETR]] (ECCV'20), [[1811.11168|DCNv2]] (CVPR'19)

**Open-Vocabulary & Zero-Shot Detection** — Detecting arbitrary object categories from text prompts or image-level supervision alone.
- [[2412.18273|SBV]], [[2303.05892|OADP]] (CVPR'23), [[2203.16513|PromptDet]] (ECCV'22), [[2201.02605|Detic]], [[2104.03344|OVANet]] (ICCV'21), [[2011.10678|OVR-CNN]]

**Data-Efficient, Weak & Semi-Supervised Detection** — Object detection and segmentation methods that reduce annotation cost via weak, semi-supervised, few-shot, or distillation-based supervision.
- [[2507.03302|SemiOVS]], [[2311.16241|SemiVL]] (ECCV'24), [[2308.09534|CFINet]] (ICCV'23), [[2112.05749|LVC]], [[2102.12252|LD]] (CVPR'22), [[2007.07986|Progressive-Knowledge-Transfer-WSOD]] (ECCV'20), [[2002.07421|EHSOD]], [[2002.04741|POTD]]

**Self-Supervised Segmentation & Category Discovery** — Self-supervised and promptable segmentation, and discovering novel object categories without full supervision.
- [[2602.23759|Selfment]], [[2408.00714|SAM 2]] (ICLR'25 Oral), [[2407.11464|Crowd-SAM]] (ECCV'24), [[2304.02643|SAM]] (ICCV'23), [[2211.11727|SimGCD]] (ICCV'23), [[2201.02609|GCD]], [[2109.10852|Pix2Seq]] (ICLR'22)

> [!star] Key Papers
> - [[2201.02605|Detic]] — Detects 20,000+ classes using only image-level supervision; pioneered scaling open-vocabulary detection with weak labels
> - [[2201.02609|GCD]] — Generalized Category Discovery framework; foundational method for discovering novel categories without full supervision
> - [[2602.23759|Selfment]] — Accurate segmentation learned purely from self-supervision; eliminates annotation dependency for dense prediction
> - [[2304.02643|SAM]] (ICCV'23) — Promptable segmentation foundation model trained on 1B masks; established zero-shot segmentation as a general capability

**Additional methods** — Papers referenced in this section that don't fit the categories above.
- [[2607.21309|ST-Block]], [[2607.21281|HGeo-TopoMap]], [[2607.18433|Learnable Novelty]], [[2505.21460|Calibration-Swap-Regret]] (NeurIPS'25 Oral), [[2505.09651|Location-Intelligence-Survey]], [[2505.03233|SynGrasp-1B]] (CoRL'25), [[2502.16736|AdaConG]] (ICLR'26), [[2502.07408|DNL]], [[2502.06309|Analog-In-Memory-Training]] (NeurIPS'25 Oral), [[2403.01299|Photonic-PUF-ML-Resilience]], [[2102.06746|Conformal-Functional-Bands]], [[2004.02684|Attribute-Mix]]

> [!star] Key Papers
> - [[2607.21309|ST-Block]] — Factorized spatio-temporal convolutions enable omnidirectional human detection and 2D relative pose estimation from planar LiDAR
> - [[2607.21281|HGeo-TopoMap]] — Hierarchical geometric priors boost topological mapping by combining explicit BEV road structure with implicit centerline geometry
> - [[2607.18433|Learnable Novelty]] — Proposes 'learnable novelty' as a unifying principle for intelligence via a differentiable novelty estimator
> - [[2102.06746|Conformal-Functional-Bands]] — Split conformal prediction with an L∞ nonconformity measure and data-driven modulation, yielding finite-sample exact prediction bands for functional data without distributional assumptions
> - [[2505.09651|Location-Intelligence-Survey]] — Comprehensive survey bridging deep learning and LLMs for geospatial representation; maps the emerging location intelligence landscape
> - [[2502.07408|DNL]] — Data-free, optimization-free sign-bit flips catastrophically disrupt DNNs; ResNet-50 accuracy drops 99.8% with just 2 flips across 43/48 ImageNet models
> - [[2403.01299|Photonic-PUF-ML-Resilience]] — Evaluates ML attack resilience of photonic physically unclonable functions; bridges foundation model techniques and hardware security

> [!tip] Watch List
> PaperCoder and LLM-NAR represent a meta-trend: AI systems that accelerate AI research itself. Deep-STDP explores whether biological learning rules can complement backpropagation. These are early signals of potentially transformative directions.


---

## Cross-References

- [[08_Reinforcement-Learning]] — RL fine-tunes these foundation models for reasoning
- [[05_Vision-Language-Models]] — VLMs built on these foundations
- [[11_Robotics-and-Embodied-AI]] — Foundation models as backbones for VLAs
- [[06_Multimodal-LLMs]] — Detailed coverage of multimodal architectures
- [[07_Reasoning-and-Planning]] — Reasoning methods that build on foundation models

---

*Next: [[02_Computer-Vision-and-3D]] for how these foundations power detection, segmentation, and 3D perception.*
