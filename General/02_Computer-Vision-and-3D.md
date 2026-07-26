---
title: "Computer Vision & 3D Understanding — Topic Overview"
tags:
  - computer-vision
  - 3D
  - spatial-reasoning
  - object-detection
  - segmentation
  - self-supervised
  - vision-transformer
  - domain-adaptation
  - few-shot
aliases:
  - "CV and 3D Overview"
---

# Computer Vision & 3D Understanding

> [!abstract] Overview
> From feature pyramids to open-vocabulary detection to 3D scene understanding, this note covers the perception stack that underpins embodied AI. The key trends: (1) moving from closed-set recognition to open-world, grounded, and 3D-aware perception, (2) self-supervised pre-training replacing supervised ImageNet features, (3) Vision Transformers replacing CNNs across every sub-task, and (4) efficient architectures enabling real-time deployment.

## Evolution Graph

```text
Self-Supervised Foundations

┌──────────────┐     ┌──────────────┐
│ DINO (2021)  │     │ MAE (2021)   │
└──────┬───────┘     └──────┬───────┘
       ├───────────► GLIP (2021)      [Object Detection, below]
       ├───────────► DINOv (2023)     [Segmentation, below]
       │                    │
       └─────────┬──────────┘
                 ▼
          ╔═════════════════╗
          ║ *DINOv2 (2023)  ║
          ╚════════╤════════╝
                   ├───────────► RieMind (2026)    [3D Understanding, below]
                   └───────────► VEGA-3D (2026)    [3D Understanding, below]

Vision Architectures

╔══════════════╗
║ *ViT (2020)  ║
╚══════╤═══════╝
       ├───────────► DINO (2021)   [Self-Supervised Foundations, above]
       ├───────────► MAE (2021)    [Self-Supervised Foundations, above]
       │
       ▼
┌────────────────┐
│ Swin V2 (2021) │
└────┬───────┬───┘
     │       │
     ▼       ▼
┌──────────┐ ┌──────────┐
│ FocalNet │ │ MaxViT   │
│ (2022)   │ │ (2022)   │
└──────────┘ └──────────┘

Object Detection

┌──────────────┐    ┌──────────────┐
│ FPN (2016)   │    │ GLIP (2021)  │
└──────┬───────┘    └──────┬───────┘
       └─────────┬─────────┘
                 ▼
          ╔═══════════════════╗
          ║ *Grounding DINO   ║
          ║ (2023)            ║
          ╚═════════╤═════════╝
                    ├───────────► LISA (2023)
                    └───────────► RAM (2023)

Segmentation

┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ LISA (2023)  │   │ RAM (2023)   │   │ DINOv (2023) │
└──────┬───────┘   └──────────────┘   └──────────────┘
       │
       └───────────► VIEW2SPACE (2026)   [3D Understanding, below]

3D Understanding

╔═════════════════╗    ┌──────────────────┐   ┌───────────────────┐
║ *RieMind (2026) ║    │ VEGA-3D (2026)   │   │ VIEW2SPACE (2026) │
╚═════════════════╝    └──────────────────┘   └───────────────────┘

Legend: ╔═╗ double border + "*" prefix = landmark/foundational paper.
```

The field evolved through four phases: **backbone design** (2016-2022) where ViT, Swin V2, FocalNet, and FPN established the architectural vocabulary; **self-supervised feature learning** (2021-2023) where DINO, MAE, and DINOv2 eliminated label dependence; **open-vocabulary perception** (2021-2023) where GLIP, Grounding DINO, LISA, and RAM made detection and segmentation language-driven; and **3D spatial reasoning** (2023-2026) where RieMind, VEGA-3D, and VIEW2SPACE pushed models from 2D recognition into metric 3D understanding.

| Year | Paper | Contribution |
|------|-------|-------------|
| 2016 | [[1612.03144\|FPN]] | Top-down feature pyramid with lateral connections; foundational multi-scale architecture for object detection |
| 2020 | [[2010.11929\|ViT]] | Proved pure Transformers on image patches match CNNs; foundational backbone for all downstream architectures |
| 2021 | [[2104.14294\|DINO]] | Self-distillation without labels; ViT attention maps emerge as object segmenters |
| 2021 | [[2111.06377\|MAE]] | Masked 75% of image patches and reconstructed pixels; scalable self-supervised pretraining at 3-4x lower cost |
| 2021 | [[2111.09883\|Swin-Transformer-V2]] | Scaled window attention to 3B parameters with stable training; solved the low-to-high resolution transfer gap |
| 2021 | [[2112.03857\|GLIP]] | Unified detection and phrase grounding; learned object-level language-aware representations for open-vocabulary transfer |
| 2022 | [[2203.11926\|FocalNet]] | Attention-free focal modulation for efficient long-range interactions; SOTA on detection and segmentation with lower cost |
| 2022 | [[2204.01697\|MaxViT]] | Multi-axis attention combining blocked local and dilated global interactions with linear complexity |
| 2023 | [[2304.07193\|DINOv2]] | Scaled self-supervised learning to 142M images; universal visual features rivaling CLIP without text supervision |
| 2023 | [[2303.05499\|Grounding-DINO]] | Deep language-vision fusion in DINO detector; 52.5 AP zero-shot on COCO for open-set detection |
| 2023 | [[2308.00692\|LISA]] | Reasoning segmentation via LLM; generates pixel masks from implicit natural language queries |
| 2023 | [[2306.03514\|RAM]] | Open-vocabulary image tagging foundation model trained on annotation-free web data; 86.0 mAP on OpenImages |
| 2023 | [[2311.13601\|DINOv]] | Visual in-context prompting for unified segmentation; open-set generalization via purely visual cues |
| 2026 | [[2603.15386\|RieMind]] | Geometry-grounded agent decoupling perception from reasoning via 3D Scene Graph tools; +16% on VSI-Bench |
| 2026 | [[2603.19235\|VEGA-3D]] | Integrates video diffusion priors for dense geometric cues; improves MLLM spatial reasoning without 3D supervision |
| 2026 | [[2603.16506\|VIEW2SPACE]] | Benchmark for multi-view reasoning from sparse observations; grounded CoT with visual evidence training |

---

## 1. Vision Transformer Architectures

The backbone revolution: Vision Transformers replaced CNNs as the default architecture for nearly all perception tasks. The design space spans pure transformers (ViT), hierarchical multi-scale architectures (Swin, MPViT), CNN-transformer hybrids (CMT, ViT-CoMer), and efficiency-focused designs for high-resolution or resource-constrained deployment.

**Foundational Architectures** — The original ViT and its hierarchical extensions that introduced multi-scale feature processing to transformers.
- [[2606.04436|3DThinkVLA]], [[2606.02274|Dexterity-BEV]], [[2605.30561|VLM3]], [[2605.29416|3DVLA]], [[2605.24642|GFM-VLA-Study]], [[2605.21414|PointACT]], [[2605.06758|R3L]], [[2603.25744|MuRF]], [[2312.17686|BMViT]], [[2309.02031|Efficient-ViT-Survey]], [[2305.09880|ViT-CNN-Transformer-Survey]], [[2204.01697|MaxViT]], [[2112.11010|MPViT]], [[2112.01526|MViTv2]], [[2111.09883|Swin-Transformer-V2]], [[2111.06091|Visual-Transformers-Survey]], [[2105.13677|ResT]], [[2103.14030|Swin Transformer]], [[2102.12122|PVT]], [[2101.01169|Transformers-in-Vision-Survey]], [[2010.11929|ViT]]

> [!star] Key Papers
> - [[2010.11929|ViT]] — Proved a pure Transformer can match CNNs on image classification; launched the ViT era
> - [[2111.09883|Swin-Transformer-V2]] — Scaled to 3B parameters with shifted-window attention; established the hierarchical ViT blueprint
> - [[2101.01169|Transformers-in-Vision-Survey]] — First comprehensive survey of ViTs; established the taxonomy that later surveys build on
> - [[2309.02031|Efficient-ViT-Survey]] — Focused review of efficiency techniques for ViTs; essential for deployment-oriented work

**CNN-Transformer Hybrids** — Combine convolutional inductive biases (locality, translation equivariance) with transformer global attention for better speed-accuracy tradeoffs.
- [[2604.13596|VGGT-Segmentor]], [[2602.20160|tttLRM]], [[2602.17807|VidEoMT]], [[2602.10094|4RC]], [[2512.08924|D4RT]], [[2512.04012|RobustVGGT]], [[2501.18564|SAM2Act]], [[2403.11999|HIRI-ViT]], [[2403.07392|ViT-CoMer]], [[2203.01577|HOI4D]], [[2107.06263|CMT]]

> [!star] Key Papers
> - [[2403.07392|ViT-CoMer]] — Convolutional multi-scale feature interaction inside ViT; strong on detection and segmentation without extra FPN

**Attention Innovations** — Novel attention mechanisms that improve efficiency, multi-scale coverage, or token allocation within vision transformers.
- [[2604.02327|SteerViT]], [[2508.02124|DMA]], [[2507.00505|LLaVA-SP]], [[2505.22195|S2AFormer]], [[2308.12216|SG-Former]], [[2304.06250|RSIR-Transformer]], [[2203.11926|FocalNet]], [[2107.00641|Focal-Transformer]], [[1711.07971|Non-local Neural Networks]]

> [!star] Key Papers
> - [[2203.11926|FocalNet]] — Attention-free focal modulation; achieves strong results without self-attention, proving attention is not the only path

**Efficient & Scalable ViTs** — Architectures optimized for throughput, memory, deployment on resource-constrained hardware, and flexible handling of arbitrary resolutions or aspect ratios at inference time.
- [[2603.22570|CanViT]], [[2510.18091|APT]], [[2505.20802|Leaner-Transformers]], [[2403.18361|ViTAR]], [[2403.13298|RoPE-Mixed]], [[2307.09120|LW-PLG-ViT]], [[2307.06304|NaViT]], [[2306.06189|FasterViT]], [[2212.08013|FlexiViT]], [[2205.14756|EfficientViT]], [[2205.03436|EdgeViTs]], [[2107.02239|ViX]], [[2103.15358|ViL]]

> [!star] Key Papers
> - [[2306.06189|FasterViT]] — NVIDIA's hybrid design with hierarchical attention; Pareto-optimal across speed and accuracy
> - [[2510.18091|APT]] — Adaptive Patch Transformers that dynamically reduce spatial tokens; accelerates ViTs without retraining
> - [[2307.06304|NaViT]] — Processes images at native resolution and aspect ratio; eliminates distortion from forced resizing

**Dense Prediction Adaptation** — Adapters and modifications that turn plain ViTs into strong backbones for detection, segmentation, and depth estimation without pre-training changes.
- [[2603.15031|AttnRes]], [[2502.01962|META]], [[2412.18090|MPI-Tuning]], [[2205.08534|ViT-Adapter]], [[2203.16527|ViTDet]], [[2203.13116|EgoPAT3D]]

> [!star] Key Papers
> - [[2203.16527|ViTDet]] — Proved plain non-hierarchical ViTs can rival specialized architectures on detection when paired with simple FPN

**Positional Encoding & Internal Representations** — Studies on how ViTs encode position, semantics, and hierarchy internally.
- [[2607.14228|SeeSE3]], [[2602.10551|C2RoPE]], [[2601.15275|RayRoPE]], [[2601.05328|BFD]], [[2510.08638|Minkowski-Representation-Hypothesis]], [[2310.18969|ViT-Class-Embedding-Analysis]]

> [!star] Key Papers
> - [[2510.08638|Minkowski-Representation-Hypothesis]] — Showed DINOv2 internally represents visual concepts in a Minkowski-like geometric structure

> [!tip] Choosing a ViT Backbone
> For general-purpose tasks, start with DINOv2 features. For detection, use ViTDet or ViT-CoMer. For efficiency-constrained deployment, FasterViT and EfficientViT offer the best speed-accuracy tradeoffs.

---

## 2. Self-Supervised Visual Representation Learning

Learning powerful visual features without labels. Self-supervised pre-training now produces features that surpass ImageNet-supervised representations across nearly all downstream tasks, and forms the backbone for open-vocabulary detection, segmentation, and 3D understanding.

**Self-Distillation & Foundation Unification (DINO family)** — Learn representations by training a student network to match an exponential moving-average teacher, producing features with emergent segmentation properties; includes distilling or merging multiple such foundation encoders into one.
- [[2607.05247|LingBot-Vision]], [[2605.30350|DynaFLIP]], [[2605.22814|Remember-to-be-Curious]], [[2605.22629|H-Flow]], [[2605.21258|Structural-Latent-Points]], [[2604.26488|LILA]], [[2511.17309|MuM]], [[2412.07679|RADIOv2.5]], [[2312.06709|AM-RADIO]], [[2304.07193|DINOv2]], [[2106.09785|EsViT]], [[2104.14294|DINO]], [[2104.03602|SiT]]

> [!star] Key Papers
> - [[2104.14294|DINO]] — Self-distillation with no labels; attention maps spontaneously segment objects
> - [[2304.07193|DINOv2]] — Curated data + distillation at scale; the current best general-purpose visual encoder
> - [[2312.06709|AM-RADIO]] — Unifies CLIP, DINOv2, and SAM into one student model; best of all worlds in a single forward pass

**Masked & Predictive Pre-training (MIM + JEPA)** — Reconstruct masked patches (pixels or tokens) or predict abstract representations of masked regions, forcing the model to learn high-level semantics over low-level texture.
- [[2607.02404|Object-centric LeJEPA]], [[2607.00784|LeVLJEPA]], [[2606.32026|AdaJEPA]], [[2602.23058|GeoWorld]], [[2512.16922|NEPA]], [[2304.03977|EMP-SSL]], [[2301.08243|I-JEPA]], [[2111.09886|SimMIM]], [[2111.06377|MAE]], [[2106.08254|BEiT]]

> [!star] Key Papers
> - [[2111.06377|MAE]] — Elegantly simple: mask 75% of patches, reconstruct pixels; scales effortlessly
> - [[2106.08254|BEiT]] — Predicts discrete visual tokens instead of pixels; bridged BERT-style pre-training to vision
> - [[2301.08243|I-JEPA]] — Joint-Embedding Predictive Architecture; learns semantic features by predicting representations, not pixel reconstructions

**Generative & Autoregressive Pre-training** — Pre-training via autoregressive prediction of visual tokens, multi-crop contrastive learning at scale, or repurposing large-scale generative diffusion backbones as the visual pre-training objective.
- [[2607.09024|GenCeption]], [[2607.06553|ReChannel]], [[2510.08568|NovaFlow]], [[2401.08541|AIM]], [[2312.02116|GIVT]], [[2303.11331|EVA-02]], [[2302.05442|ViT-22B]]

> [!star] Key Papers
> - [[2607.09024|GenCeption]] — DeepMind's single-step repurposing of a text-to-video diffusion model into a generalist perception backbone; beats V-JEPA and VideoMAE V2 pre-training on depth
> - [[2607.06553|ReChannel]] — Drops the target-side VAE decoder for a token-local linear readout; SOTA on six dense tasks at up to 2.48x faster inference
> - [[2401.08541|AIM]] — Apple's autoregressive image model; proved autoregressive pre-training scales for vision just as for language
> - [[2302.05442|ViT-22B]] — 22B parameter ViT; established feasibility of scaling vision models to LLM-scale

**Domain-Specific Adaptation** — Adapting self-supervised models to specialized visual domains with limited labels.
- [[2606.31236|TactX]], [[2511.20844|Pre-train-to-Gain]], [[2510.20994|VESSA]], [[2505.22196|Aug-Aware-SSL-Theory]], [[2505.13584|SSL-Segmentation-Survey]], [[2406.09294|JEA-Scaling-Study]], [[2404.17202|Low-Data-SSL-Evaluation]]

> [!star] Key Papers
> - [[2510.20994|VESSA]] — Self-supervised adaptation to new visual domains without any labels; practical for medical/industrial deployment

**Additional methods** — Contrastive and momentum-based self-supervised methods, plus training-recipe studies (initialization, learning-rate schedules), not covered by the sub-topics above.
- [[2602.00937|CLAMP]], [[2507.17634|WSM]], [[2505.19985|Structured-ViT-Initialization]], [[2006.07733|BYOL]], [[1911.05722|MoCo]]

> [!star] Key Papers
> - [[2505.19985|Structured-ViT-Initialization]] — Embeds convolutional inductive biases into ViT attention at init; bridges the CNN-ViT gap on small datasets
> - [[2507.17634|WSM]] — Decay-free learning rate schedule via checkpoint merging; simplifies LLM pre-training with +1.3 avg benchmark improvement

> [!tip] The SSL Hierarchy
> DINO/DINOv2 for general-purpose features. MAE for tasks needing spatial detail (depth, segmentation). I-JEPA for semantic-level understanding. AM-RADIO if you need all properties in one model.

---

## 3. Object Detection

From closed-set detectors to open-vocabulary, language-grounded detection. The trajectory: multi-scale feature extraction (FPN) established the paradigm, transformer detectors eliminated hand-crafted components, and grounded pre-training opened detection to arbitrary categories described in natural language.

**CLIP-Based Region-Text Pretraining for Open-Vocabulary Detection** — Foundational open-vocabulary detectors built by adapting or distilling CLIP-style region-text alignment, or fusing grounded language-vision pretraining directly into the detector (2021-2024).
- [[2401.09865|SPARC]], [[2401.02361|MM-Grounding-DINO]], [[2306.09683|OWLv2]], [[2305.07011|RO-ViT]], [[2304.04514|DetCLIPv2]], [[2303.13076|CORA]], [[2303.05892|OADP]], [[2303.05499|Grounding-DINO]], [[2302.13996|BARON]], [[2209.15639|F-VLM]], [[2209.09407|DetCLIP]], [[2206.07643|FIBER]], [[2206.05836|GLIPv2]], [[2205.06230|OWL-ViT]], [[2203.17273|FindIt]], [[2203.16513|PromptDet]], [[2201.02605|Detic]], [[2112.09106|RegionCLIP]], [[2112.03857|GLIP]], [[2104.13921|ViLD]], [[2104.12763|MDETR]], [[2011.10678|OVR-CNN]]

> [!star] Key Papers
> - [[2303.05499|Grounding-DINO]] — Married DINO features with grounded pre-training; the go-to open-set detector
> - [[2112.03857|GLIP]] — Grounded language-image pre-training; unified detection and phrase grounding

**LLM-Era, Benchmark & Emerging Open-Vocabulary Detection** — Later-generation open-vocabulary detectors driven by LLMs, autoregressive decoding, and application-specific adaptation, alongside the benchmarks and surveys charting the field's transition from closed-set to open-world (2023-2026).
- [[2604.02759|OMNI-PoseX]], [[2604.01179|Florence-2-ROS-2-Wrapper]], [[2603.14609|GroundSet]], [[2602.23759|Selfment]], [[2510.12798|Rex-Omni]], [[2506.23785|VisTex-OVLM]], [[2503.07465|YOLOE]], [[2501.18954|LLMDet]], [[2412.16334|dino.txt]], [[2410.13842|D-FINE]], [[2410.08021|OneRef]], [[2408.10787|UniProj-Det]], [[2404.13013|Groma]], [[2404.09216|DetCLIPv3]], [[2404.07664|PROWL]], [[2403.10191|GenerateU]], [[2312.10439|SIC-CADS]], [[2307.12813|DOD]], [[2307.09220|OVD/OVS-Survey]], [[2306.15880|Open-Vocabulary-Learning-Survey]], [[2304.11463|OmniLabel]], [[2303.02489|CapDet]]

> [!star] Key Papers
> - [[2306.15880|Open-Vocabulary-Learning-Survey]] — Comprehensive survey of open-vocabulary methods across detection, segmentation, and recognition
> - [[2307.09220|OVD/OVS-Survey]] — Focused review of open-vocabulary detection and segmentation; maps the rapid transition from closed-set to open-world

**Metric-Learning & Meta-Learning Few-Shot Detectors** — Classic few-shot/low-shot detection architectures based on metric learning, meta-learning, and Siamese matching (2018-2021).
- [[2203.07669|PE2E]], [[2108.09017|DeFRCN]], [[2003.06957|TFA]], [[2003.06800|OS2D]], [[2002.04741|POTD]], [[1911.12529|CoAE]], [[1909.13032|Meta-R-CNN]], [[1908.01998|Attention-RPN]], [[1812.01866|Feature-Reweighting Detector]], [[1811.11507|Siamese-Mask-R-CNN]], [[1806.04728|RepMet]], [[1803.01529|LSTD]]

> [!star] Key Papers
> - [[2003.06800|OS2D]] — One-stage one-shot detection integrating correlation matching with spatial alignment in a single network

**Attention-Based & Cross-Domain Few-Shot Detection** — Cross-attention transformers, co-excitation, and prototype-based few-shot detection for embodied and open-world settings (2021-2026).
- [[2506.06199|3DFlowAction]], [[2411.19167|HOT3D]], [[2408.05674|PS-TTL]], [[2303.14240|BSPG]], [[2207.01887|MKT]], [[2203.09093|SaFT]], [[2112.05749|LVC]], [[2112.02814|Low-Shot-Detection-Survey]], [[2105.01294|Feature Hallucinator]], [[2104.14984|CAT]]

> [!star] Key Papers
> - [[2104.14984|CAT]] — Cross-Attention Transformer for one-shot detection; models bidirectional query-target relationships

**Small Object & Crowded Scene Detection** — Specialized methods for detecting tiny or heavily overlapping objects where standard detectors fail.
- [[2605.27365|LocateAnything]], [[2604.27106|RecGen]], [[2603.17684|AFSS]], [[2507.12006|FDAM]], [[2504.13469|HMPE]], [[2504.09819|Density-Guided-Object-Detection]], [[2407.11464|Crowd-SAM]], [[2309.11069|Dynamic-Tiling]], [[2308.10677|Visual-Crowd-Analysis-Survey]], [[2308.09534|CFINet]], [[2207.14096|SODA]], [[2202.06934|SAHI]], [[2003.09163|MIP]], [[1904.03629|Adaptive-NMS]], [[1805.00123|CrowdHuman]]

> [!star] Key Papers
> - [[2504.13469|HMPE]] — HeatMap Embedding for small object detection; dynamically allocates attention to tiny targets

**Reward & RL-Tuned Detection** — Methods applying reinforcement learning or reward-based optimization to improve detection and visual grounding.
- [[2605.15951|Group-Revision]], [[2602.20630|TraqPoint]], [[2504.07615|VLM-R1]], [[2503.01785|Visual-RFT]], [[2302.08242|Reward-Tuning-CV]]

> [!star] Key Papers
> - [[2503.01785|Visual-RFT]] — Adapts RL fine-tuning to vision tasks with verifiable rewards; +24.3% on fine-grained classification, +21.9 mAP on few-shot detection
> - [[2302.08242|Reward-Tuning-CV]] — Google's framework for directly optimizing non-differentiable vision metrics via RL; +15.1% mAP on detection

**LLM-Assisted Detection & Automation** — Leveraging LLMs for detection chain-of-thought, auto-labeling, and specialized visual understanding tasks.
- [[2605.20284|JUDO]], [[2603.27179|ReAL]], [[2510.21311|FineRS]], [[2506.07850|SAM2Auto]], [[2506.02359|Auto-Labeling]], [[2503.23508|Real-LOD]], [[2412.18273|SBV]], [[2411.19331|Talk2DINO]], [[2405.17104|LLM-Optic]], [[2405.08593|NRAA]], [[2403.12488|DetToolChain]], [[2401.17981|MLLM-Detection-Infusion]], [[2401.07629|FPD]], [[2305.18565|PaLI-X]], [[2305.11175|VisionLLM]], [[2203.14712|Assembly101]]

> [!star] Key Papers
> - [[2403.12488|DetToolChain]] — Detection-specific chain-of-thought with a visual toolkit; enables zero-shot detection via prompting alone
> - [[2510.21311|FineRS]] — Coarse-to-fine pipeline with RL for ultra-small object reasoning and segmentation in 4K images

**Additional methods** — Detection-adjacent methods not covered by the sub-topics above, including classic multi-scale feature-pyramid detectors and weakly-supervised detection.
- [[2607.08402|Pedestrian Privacy Pipeline]], [[2607.08391|MURAL]], [[2607.06600|MiLSD]], [[2607.00191|HydraCollab]], [[2406.03459|LW-DETR]], [[2304.08069|RT-DETR]], [[2109.10852|Pix2Seq]], [[2104.11181|H2O]], [[2103.14259|OTA]], [[2102.12252|LD]], [[2010.04159|Deformable DETR]], [[2007.07986|Progressive-Knowledge-Transfer-WSOD]], [[2005.12872|DETR]], [[2002.07421|EHSOD]], [[1811.11168|DCNv2]], [[1803.01534|PANet]], [[1612.03144|FPN]], [[1607.03476|End-to-End mAP Training]], [[1512.02325|SSD]], [[1511.02853|WSDDN]], [[1511.02283|Google Refexp]]

> [!star] Key Papers
> - [[1612.03144|FPN]] — Feature Pyramid Networks: the multi-scale backbone that underlies nearly all modern detectors
> - [[2002.07421|EHSOD]] — End-to-end hybrid-supervised detection combining full and weak annotations

> [!tip] Detection in Practice
> For open-vocabulary needs, Grounding DINO is the standard. For few-shot scenarios, combine a strong DINO/DINOv2 backbone with metric-learning heads. For small objects, add Dynamic Tiling or HMPE on top of any base detector.

---

## 4. Segmentation & Recognition

From class-specific masks to open-world, language-guided segmentation. Modern segmentation leverages VLM reasoning to handle arbitrary queries ("the object the person is pointing at") rather than fixed category lists.

**Language-Guided Segmentation** — Segment objects described by natural language queries, combining VLM reasoning with pixel-level prediction; rooted in the class-agnostic, promptable (point/box/mask) foundation backbone extended by SAM 2, SAM-3D, and SAM-CLIP.
- [[2607.06560|SenseNova-Vision]], [[2605.00891|X2SAM]], [[2603.04002|DPAD]], [[2602.23339|Retrieve-and-Segment]], [[2602.17134|B3-Seg]], [[2601.10477|SocioSeg]], [[2601.05244|GREx]], [[2511.16624|SAM-3D]], [[2508.10104|DINOv3]], [[2506.22880|DeSa2VA]], [[2506.22624|Seg-R1]], [[2506.04277|RSVP]], [[2505.22596|SAM-R1]], [[2505.12081|VisionReasoner]], [[2503.06520|Seg-Zero]], [[2310.11441|SoM]], [[2308.00692|LISA]], [[2306.04356|FGVP]], [[2304.02643|SAM]], [[2203.16265|SeqTR]]

> [!star] Key Papers
> - [[2308.00692|LISA]] — Reasoning segmentation: handles complex referring expressions that require multi-step inference
> - [[2503.06520|Seg-Zero]] — Reasoning-chain guided segmentation via cognitive RL; combines chain-of-thought with pixel predictions
> - [[2304.02643|SAM]] — Segment Anything: promptable, zero-shot segmentation foundation model trained on 1B+ masks; the backbone underlying SAM 2, SAM-CLIP, and the entire promptable-segmentation ecosystem

**Open-Vocabulary Recognition & Tagging** — Recognize or tag arbitrary categories in images without being restricted to a fixed label set.
- [[2607.00978|UTTO]], [[2603.28480|INSID3]], [[2603.03197|SpeciaRL]], [[2511.18305|DiVE-k]], [[2505.04410|DeCLIP]], [[2311.13601|DINOv]], [[2310.15308|SAM-CLIP]], [[2310.05916|TEXTSPAN]], [[2306.03514|RAM]], [[2203.12555|GriTS]], [[2112.01071|MaskCLIP (Dense CLIP Labels)]]

> [!star] Key Papers
> - [[2306.03514|RAM]] — Recognize Anything Model: strong multi-label image tagging at scale
> - [[2311.13601|DINOv]] — Extends in-context prompting to generic segmentation using pure visual exemplars

**High-Resolution & Efficient Segmentation** — Architectures designed for segmentation at high spatial resolution without excessive compute, maintaining fine boundary detail.
- [[2605.25495|RepSAM]], [[2505.16993|SeNaTra]], [[2504.18158|E-InMeMo]], [[2503.19108|EoMT]], [[2111.01236|HRViT]], [[2110.09408|HRFormer]], [[1908.07919|HRNet]]

> [!star] Key Papers
> - [[2505.16993|SeNaTra]] — NVIDIA's content-aware spatial grouping inside ViTs; groups semantically related tokens for efficient segmentation

**Feature Enhancement for Dense Prediction** — Methods that sharpen or enhance foundation model features to produce precise segmentation boundaries.
- [[2602.01905|STELLAR]], [[2601.16093|SAMTok]], [[2601.12964|Cross-Scale-Pretraining]], [[2512.10554|GETok]], [[2506.13925|HVL]], [[2506.11136|JAFAR]], [[2412.03069|TokenFlow]]

> [!star] Key Papers
> - [[2506.11136|JAFAR]] — Enhances frozen encoder features to produce sharp, high-resolution segmentation without fine-tuning

**Video & Temporal Segmentation** — Segmentation methods that extend to video sequences, combining spatial precision with temporal consistency.
- [[2603.12382|SPARROW]], [[2512.11782|MatAnyone-2]], [[2511.22950|RobotSeg]], [[2511.20886|V2-SAM]], [[2511.16077|VideoSeg-R1]], [[2511.15622|SA-FARI]], [[2506.07850|SAM2Auto]], [[2506.05302|PAM]], [[2502.04144|HD-EPIC]], [[2408.00714|SAM 2]]

> [!star] Key Papers
> - [[2511.16077|VideoSeg-R1]] — First RL-based framework for video object segmentation; explicit reasoning chains for temporal tracking
> - [[2603.12382|SPARROW]] — Dual-prompt grounding with tracked features; +8.9 J&F on MeViS for temporally consistent segmentation
> - [[2408.00714|SAM 2]] — Extends SAM to video with a streaming memory mechanism; the standard backbone underlying SAM2Act, SAM2Auto, and RobotSeg

**Limited-Label & Few-Shot Segmentation** — Segment novel categories or handle limited labeled data via one-shot similarity guidance, prototype matching, or semi-supervised pseudo-labeling with language anchors.
- [[2507.03302|SemiOVS]], [[2402.06912|ES-Linear-Policy]], [[2311.16241|SemiVL]], [[1810.09091|SG-One]]

> [!star] Key Papers
> - [[2507.03302|SemiOVS]] — Uses open-vocabulary models for pseudo-labels on out-of-distribution data; +12.6% mIoU in low-label settings
> - [[1810.09091|SG-One]] — Similarity guidance network for one-shot segmentation; halved parameters while exceeding prior methods by 5+ mIoU

**Additional methods** — Segmentation-adjacent methods not covered by the sub-topics above.
- [[2406.08231|Video Game Glitch Detection]], [[2205.10337|UViM]], [[1801.00868|Panoptic Segmentation]], [[1604.01685|Cityscapes]]

> [!tip] Segmentation Stack
> Use Grounding DINO for detection + SAM for masks in most applications. For complex language queries, LISA adds reasoning. For domain-specific needs, JAFAR sharpens frozen features without retraining.

---

## 5. 3D Scene Understanding

The frontier of perception: giving AI models true 3D spatial awareness. This capability is critical for embodied AI, where robots must reason about object positions, spatial relationships, and scene geometry from limited viewpoints.

**3D Scene Graphs, Occupancy & Spatial Memory** — Persistent, structured 3D scene representations (topological maps, scene graphs, occupancy/voxel memory) supporting long-horizon embodied navigation and exploration.
- [[2607.21281|HGeo-TopoMap]], [[2607.13245|JITOMA]], [[2607.10879|BRO Scene Graph Prediction]], [[2607.08537|Whareformer]], [[2607.07885|TTC Obstacle Avoidance]], [[2607.05543|GEM-Occ]], [[2606.30598|HOPformer]], [[2606.29786|OP3DSG]], [[2606.02551|AFUN]], [[2606.00637|GLAD]], [[2604.11302|3D-ALP]], [[2512.14692|O-Voxel]], [[2411.17735|3D-Mem]], [[2402.15487|RoboEXP]]

**VLM-Grounded 3D Reasoning, Body Pose & Benchmarks** — Agentic/VLM-based spatial reasoning over 3D scenes, human/object 3D pose estimation, and dedicated benchmarks or datasets for 3D scene understanding.
- [[2605.29563|ViewSuite]], [[2603.15386|RieMind]], [[2602.20363|3D-Aesthetic-Field]], [[2602.15989|SAM-3D-Body]], [[2602.12087|MetricMM]], [[2602.06037|GeoThinker]], [[2601.22231|PE-Spatial-Reasoning-Analysis]], [[2512.16811|GeoPredict]], [[2510.16714|SceneCOT]], [[2509.21420|QuadGPT]], [[2507.07781|SURPRISE3D]], [[2505.20279|VLM-3R]], [[2505.12448|SSR]], [[2410.08208|SPA]], [[1709.06158|Matterport3D]]

**Multi-View, Cross-Frame & Omnidirectional Spatial Benchmarks** — Evaluate viewpoint- and perspective-taking spatial reasoning across multiple views, frames, or 360-degree observations.
- [[2603.16506|VIEW2SPACE]], [[2601.14339|CityCube]], [[2512.23365|SpatialMosaic]], [[2510.11549|ODI-Bench]], [[2505.24257|DISJOINT-3DQA]], [[2505.21500|MVSM]], [[2505.17015|Multi-SpatialMLLM]], [[2505.11907|OSR-Bench]]

**Compositional, Causal & Dynamic (4D) Spatial Reasoning Benchmarks** — Evaluate multi-hop, causal, deformation, and temporal (4D) spatial reasoning in vision-language models.
- [[2603.18892|MultihopSpatial]], [[2603.00515|MLLM-4D]], [[2601.13304|CausalSpatial]], [[2601.00092|Spatial4D-Bench]], [[2510.18873|DSI-Bench]], [[2507.02978|Inf-Bench]], [[2506.07966|SpaCE-10]], [[2506.04633|STARE]]

**General Spatial-Intelligence Benchmarks & Datasets** — Broad-coverage benchmarks, datasets, and evaluation suites for spatial intelligence in vision-language models.
- [[2605.27367|SpatialBench-SFM]], [[2602.11236|ABot-M0]], [[2601.11729|SpaRRTa]], [[2512.19683|OpenBench]], [[2507.20174|LRR-Bench]], [[2507.07610|SpatialViz-Bench]], [[2506.18385|InternSpatial]], [[2506.14512|SIRI-Bench]], [[2506.03135|OmniSpatial]], [[2505.17012|SpatialScore]], [[2503.22976|SPAR-7M]], [[2412.10908|Do-VLMs-Understand-3D-Shapes]], [[2412.07825|3DSRBench]], [[2410.06468|SPACE]], [[2408.16662|Space3D-Bench]], [[2404.12390|BLINK]]

**Spatial-Reasoning Training & RL Methods** — Train or fine-tune models to improve spatial reasoning directly, via RL, SFT, or architectural fusion, rather than only evaluating it.
- [[2507.05258|REA]], [[2506.23120|R2S]], [[2505.12363|ViCA2]], [[2505.12312|ViCA-7B]], [[2505.00788|SpatialLLM]], [[2504.01805|SpaceR]], [[2503.13111|MM-Spatial]]

**Additional methods** — 3D-adjacent benchmarks and methods not covered by the sub-topics above.
- [[2607.12398|Dual-Cam 3D Ultrasound]], [[2607.10873|X-GuideAR]], [[2503.21745|3DGen-Bench]], [[2212.08051|Objaverse]], [[2204.11918|GSO]], [[2103.16397|3D-AffordanceNet]], [[2005.00343|EPIC-KITCHENS (Collection & Baselines)]]

**Embodied VLA: Navigation, Manipulation & Driving** — VLM-driven 3D spatial grounding applied directly to robot navigation, manipulation, or autonomous-driving action policies.
- [[2607.18016|POT-VLA]], [[2607.17977|RynnBrain 1.1]], [[2607.14586|SoftNav]], [[2607.06564|Lift3D-VLA]], [[2606.31329|3D HAMSTER]], [[2606.30632|GROW²]], [[2606.03682|GN0]], [[2603.27287|Uni-World-VLA]], [[2512.24331|LVLDrive]], [[2510.17439|FALCON-Spatial-VLA]], [[2508.07804|Pose-RFT]], [[2506.07961|BridgeVLA]], [[2505.18947|OpenHOI]], [[2505.11383|Dynam3D]]

**3D-Grounded VLM Reasoning & Prompting Techniques** — Prompting, chain-of-thought, and architectural techniques that inject 3D spatial grounding into VLM reasoning without a downstream action policy.
- [[2607.15054|ViPS]], [[2603.27967|XVR]], [[2603.25411|HiSpatial]], [[2603.23404|TRACE]], [[2603.00905|pySpatial]], [[2602.19063|Direction-aware-3D-LMM]], [[2601.16538|OnlineSI]], [[2601.11442|Map2Thought]], [[2601.05172|CoV]], [[2510.13800|GS-Reasoner]], [[2507.12508|MindJourney]], [[2506.04220|Struct2D]], [[2506.03642|SpatialMind]], [[2505.23747|Spatial-MLLM]]

**Foundational 3D-LLM Integration, Representations & Surveys** — Foundational integrations of LLMs with 3D representations, efficient 3D-VLM representations, and surveys/benchmarks charting the field.
- [[2607.21595|VLM-IE3D]], [[2607.04057|PreSIST]], [[2605.08064|Proxy3D]], [[2512.17012|4D-RGPT]], [[2512.12822|LEMON]], [[2511.01618|Actial]], [[2510.08673|Puffin]], [[2510.08531|SpatialLadder]], [[2504.20024|SpatialReasoner]], [[2504.05786|3D-Spatial-Reasoning-in-LLM-Survey]], [[2503.18470|MetaSpatial]], [[2407.07895|LLaVA-NeXT-Interleave]], [[2307.12981|3D-LLM]], [[2008.01655|Adaptive-Memory-VO]]

> [!star] Key Papers
> - [[2603.15386|RieMind]] — 3D Scene Graph + agentic framework; decouples perception from reasoning, achieving 89.5% on VSI-Bench
> - [[2603.16506|VIEW2SPACE]] — Benchmark for sparse multi-view spatial reasoning; +77% accuracy with grounded chain-of-thought

**Gaussian-Splatting SLAM & Robotic Mapping** — Real-time visual/inertial SLAM and mapping built on 3D Gaussian Splatting representations.
- [[2607.07452|GeoGS-SLAM]], [[2607.06222|APVI-SLAM]], [[2607.02005|OCD SLAM]], [[2607.01860|DL-SLAM]], [[2606.30809|GaussLite]], [[2606.29237|MoPe]], [[2606.28720|CubifyGS]], [[2604.12942|RMGS-SLAM]], [[2604.12837|GGD-SLAM]], [[2604.11992|ReefMapGS]], [[2604.02696|VBGS-SLAM]], [[2601.13132|GaussExplorer]], [[2510.08575|ReSplat]], [[2308.04079|3D Gaussian Splatting]]

**Feed-Forward Geometry, Depth & Multi-View Reconstruction** — Feed-forward pointmap/depth regression and multi-view 3D reconstruction without per-scene optimization (the DUSt3R lineage).
- [[2607.13674|WAVE-Stereo]], [[2607.13524|COLMAR]], [[2607.01962|NeoMap]], [[2605.31124|QVGGT]], [[2605.26115|TriSplat]], [[2604.14141|LingBot-Map]], [[2603.27455|NAS3R]], [[2603.26599|VGGRPO]], [[2603.19231|MonoArt]], [[2603.08055|Speed3R]], [[2603.03026|URGT]], [[2602.21186|Spa3R]], [[2512.16913|DAP]], [[2512.14696|CRISP]], [[2512.10950|E-RayZer]], [[2511.21688|G2VLM]], [[2511.10647|Depth-Anything-3]], [[2511.06908|Mono3DVG-EnSD]], [[2507.13347|Pi3]], [[2312.14132|DUSt3R]]

**Generative & World-Model Scene Rendering** — Generative and world-model approaches that synthesize or render 3D/4D scenes rather than passively reconstructing them.
- [[2607.06856|Gen4U]], [[2607.05373|PixWorld]], [[2607.01803|PixGS]], [[2604.19747|AnyRecon]], [[2604.08532|SelfEvo]], [[2604.07105|Genie-Sim-PanoRecon]], [[2604.02329|Generative-World-Renderer]], [[2604.01479|UniRecGen]], [[2603.30045|OmniRoam]], [[2603.24581|Latent-WAM]], [[2603.22275|GLD]], [[2603.19235|VEGA-3D]], [[2603.18524|3DreamBooth]], [[2602.21992|PanoEnv]], [[2512.13683|I-Scene]], [[2511.01294|Kinematify]], [[2510.01183|EvoWorld]]

**Occupancy, Flow, Dynamic Motion & Specialized Reconstruction** — Occupancy prediction, scene flow, dynamic motion capture, and reconstruction of challenging materials or objects.
- [[2607.07139|Disturbance-Aware Underwater Motion Planning]], [[2607.05801|TRIG]], [[2607.04144|Semantic-Guided Object Removal]], [[2606.23293|Flow6D]], [[2606.02058|TIDES]], [[2605.14950|Evo-Depth]], [[2605.10204|3DReflecNet]], [[2605.09538|PhysHanDI]], [[2604.26262|Semantic-Foam]], [[2604.10836|HO-Flow]], [[2603.29089|WorldFlow3D]], [[2602.03361|Z3D]], [[2512.15160|EagleVision]], [[2506.13040|MAMMA]], [[2505.23663|AMBER-Mesh]], [[2505.18190|PhySense]], [[2504.14604|RoboOcc]], [[2412.04380|EmbodiedOcc]], [[2406.04316|Omni6DPose]]

> [!star] Key Papers
> - [[2604.14141|LingBot-Map]] — Feed-forward streaming 3D foundation model with Geometric Context Transformer; 20 FPS for sequences up to 10K frames with nearly constant memory
> - [[2603.19235|VEGA-3D]] — Video diffusion as a latent world simulator producing dense geometric cues
> - [[2603.19231|MonoArt]] — End-to-end monocular articulated object reconstruction; handles non-rigid objects
> - [[2312.14132|DUSt3R]] — Feed-forward pairwise pointmap regression with no camera calibration; the foundational architecture behind Pi3, Depth-Anything-3, and Speed3R
> - [[2308.04079|3D Gaussian Splatting]] — Real-time explicit radiance field via differentiable 3D Gaussians; became the standard scene representation underlying GaussianProperty, PhysGaussian, and dozens of downstream reconstruction/physics methods

**Human Body & Motion Reconstruction** — Recover 3D human pose, shape, hands, and motion from images, video, or other sensors (e.g. LiDAR), often world-grounded or diffusion-based for robustness to occlusion and noisy input.
- [[2607.21309|ST-Block]], [[2401.08570|RoHM]], [[2312.07531|WHAM]], [[2312.05251|HaMeR]], [[2308.12969|ROAM]], [[2012.00924|CPF]], [[2008.11200|GRAB]], [[1904.05767|ObMan]], [[1904.03278|AMASS]]

> [!star] Key Papers
> - [[2312.07531|WHAM]] — Reconstructs world-grounded human motion from video with accurate global trajectory, not just root-relative pose
> - [[2312.05251|HaMeR]] — Transformer-based 3D hand reconstruction; the standard hand-pose backbone for egocentric and manipulation research

**Feature Matching & Correspondence** — Match local features across views for 3D reconstruction, visual localization, and structure-from-motion pipelines.
- [[2607.10082|Event-Image Dual-Stage Distillation]], [[2607.01757|DL-VINS-Factory]], [[2606.16569|PROSE]], [[2604.04055|DINO-VO]], [[2602.05755|FMPose3D]], [[2506.09278|UFM]], [[2306.13643|LightGlue]], [[2108.08771|SGMNet]], [[2104.00680|LoFTR]], [[2006.13566|DISK]], [[1911.11763|SuperGlue]], [[1712.07629|SuperPoint]]

> [!star] Key Papers
> - [[2306.13643|LightGlue]] — Adaptive deep feature matching that prunes easy pairs early; fast and accurate for real-time SLAM

**Visual/Inertial Odometry & Single-Robot Localization** — Sensor fusion, odometry, and radar/UWB-based localization for a single robot or agent.
- [[2607.14009|AeroMap3D]], [[2607.11184|GeoGS-SLAM]], [[2607.08115|RadLoc]], [[2607.07374|PLED-VINS]], [[2607.06782|G-PROBE]], [[2607.05957|Delay-Aware Active Triangulation for Counter-UAS]], [[2607.05777|CO-Calib]], [[2607.05669|EVC-Mamba]], [[2607.05449|GAIA]], [[2607.00145|IterIEKF]], [[2606.29910|Sphere-VIO]], [[2308.13561|Project Aria]]

**Multi-Robot Cooperative Localization, Pose-Graph & Force Estimation** — Distributed/cooperative multi-robot localization, pose-graph optimization, and contact/force-based state estimation.
- [[2607.12811|PixelLoop]], [[2607.12265|DiffRadar]], [[2607.10372|Robotic Contextual Awareness Thesis]], [[2607.08735|DeepCORD]], [[2607.01201|Sensorless Bilateral Teleoperation]], [[2607.01106|Async-BCD]], [[2606.29868|MP-NF]], [[2606.29851|TACO (Pose Graph Optimization)]], [[2606.29673|DCL]], [[2606.29165|Continuum Robot Force Estimation]], [[2606.28712|J-LAW]], [[2203.02468|Predicate-State-Estimation]]

**3D Point-Cloud & Gaussian Diffusion Manipulation Policies** — Diffusion or transformer policies acting directly on 3D point-cloud or Gaussian-Splat scene representations for manipulation.
- [[2607.10706|Action Map Policy]], [[2604.15281|R3D]], [[2604.10953|DRL-3DBP]], [[2604.03181|MV-VDP]], [[2603.24393|3D-MIX]], [[2603.13825|Explicit-WM-Manipulation]], [[2601.16148|ActionMesh]], [[2409.01652|ReKep]], [[2403.08321|ManiGaussian]], [[2403.03954|DP3]], [[2306.14896|RVT]], [[2209.05451|PerAct]]

> [!star] Key Papers
> - [[2403.03954|DP3]] — 3D Diffusion Policy: generalizable visuomotor policy from point clouds; enables sim-to-real without camera calibration

**VLA, Flow-Matching & World-Model Manipulation Policies** — Vision-language-action, flow-matching, and world-model-conditioned policies that ground manipulation (or driving) in 3D/4D spatial representations.
- [[2607.12356|VistaVLA]], [[2607.11498|Robot-Centric Pointmaps]], [[2607.04714|GeoMoLa]], [[2606.31493|ChronoFlow-Policy]], [[2606.29936|OpenSPM]], [[2605.25685|HumanFlow]], [[2604.14089|UMI-3D]], [[2602.23721|StemVLA]], [[2512.19133|WorldRFT]], [[2510.12276|Spatial-Forcing]], [[2506.22242|4D-VLA]], [[2505.06451|Adaptive-Wiping]], [[2505.05800|3D-CAVLA]], [[2501.15830|SpatialVLA]], [[2403.09631|3D-VLA]]

**Manipulation Benchmarks, Datasets & Simulators** — Simulation environments, benchmark suites, and hand/object interaction datasets for evaluating 3D-grounded manipulation.
- [[2504.13059|RoboTwin]], [[2412.07755|SAT]], [[2412.07215|RoboData]], [[2410.01345|GemBench]], [[2403.19417|OAKINK2]], [[2402.08191|THE-COLOSSEUM]], [[2304.04321|ARNOLD]], [[2204.13662|ARCTIC]], [[2203.15709|OakInk]], [[2107.14483|ManiSkill]], [[2104.04631|DexYCB]]

**Affordance, Retrieval & Pose-Driven Manipulation** — 3D-grounded manipulation methods driven by retrieval, active pose estimation, descriptor fields, or trajectory transformation rather than diffusion action heads.
- [[2607.07897|StiffNET]], [[2607.07129|Object-Centric Neural Field LfD]], [[2509.16063|DSPv2]], [[2411.19408|SoGraB]], [[2410.24091|3D-ViTac]], [[2407.04689|RAM (Retrieval Affordance Transfer)]], [[2403.15203|DITTO (Trajectory Transformation)]], [[2310.03478|RGBManip]], [[2309.16118|D3Fields]], [[2201.12716|YODO]]

> [!star] Key Papers
> - [[2309.16118|D3Fields]] — Dynamic 3D descriptor fields enable zero-shot generalizable rearrangement without task-specific training
> - [[2407.04689|RAM (Retrieval Affordance Transfer)]] — Retrieves affordances from a memory of prior interactions for zero-shot manipulation generalization

**Embodied Simulation Environments, Platforms & World Memory** — Simulation platforms, environment generators, and persistent spatial/episodic memory for embodied agents.
- [[2607.07459|EmbodiedGen V2]], [[2607.06699|RoboSnap]], [[2606.30645|VLK]], [[2606.03943|PointAction]], [[2605.11367|3D-Belief]], [[2605.01799|Embody4D]], [[2605.00781|Map2World]], [[2604.04707|OpenWorldLib]], [[2604.01001|EgoSim]], [[2603.28887|OccSim]], [[2603.17117|MosaicMem]], [[2602.10116|SAGE]], [[2512.10949|RL-Text-to-3D-Study]], [[2506.04941|ArtVIP]], [[2411.04999|DynaMem]], [[2309.17024|HoloAssist]], [[2203.01914|Playable-Environments]]

**Generative World Models for Prediction, Planning & Driving** — World models that predict, plan, or render future states for robotic manipulation and autonomous driving.
- [[2607.13154|WANDA]], [[2607.06559|RynnWorld-4D]], [[2607.06216|MoWorld]], [[2607.05390|Deform360]], [[2607.01938|PhysMani]], [[2607.01166|Structured 4D Latent]], [[2607.00673|PVWM]], [[2607.00148|3DPWM]], [[2606.03188|GeoSem-WAM]], [[2605.30347|NeuROK]], [[2605.21572|PhysX-Omni]], [[2605.20752|GaussianDream]], [[2605.05163|PhysForge]], [[2604.15805|WorldComposer]], [[2604.14268|HY-World-2.0]], [[2504.20995|TesserAct]], [[2502.13144|RAD]]

**Latent World Models for Dynamics Prediction** — Learn a compact latent (occupancy, 4D, or metric) state to predict future dynamics for control or driving, distinct from the simulation-environment tooling above.
- [[2607.21576|SDM]], [[2607.05468|MECo-WAM]], [[2607.04541|CRISP]], [[2607.03941|WSA1]], [[2605.08279|LaWM]], [[2603.01549|Pri4R]], [[2311.16038|OccWorld]]

> [!star] Key Papers
> - [[2311.16038|OccWorld]] — First 3D occupancy world model for autonomous driving; predicts future scene evolution and ego trajectory jointly

**Physics-Solver Coupled 3DGS/NeRF (MPM/FEM/PBD)** — Couples 3D Gaussian Splatting or NeRF directly with continuum-mechanics solvers (MPM/FEM/PBD) so scenes obey real physical dynamics.
- [[2602.06035|InterPrior]], [[2508.13911|PhysGM]], [[2501.18982|OmniPhysGS]], [[2412.17804|GausSim]], [[2412.11258|GaussianProperty]], [[2411.16800|Phys4DGen]], [[2411.12789|Sim-GS]], [[2406.04338|Physics3D]], [[2405.15056|ElastoGen]], [[2401.16663|VR-GS]], [[2401.15318|Gaussian-Splashing]], [[2312.00583|DeformGS]], [[2311.13099|PIE-NeRF]], [[2311.12198|PhysGaussian]], [[2304.14369|NCLaw]], [[2303.05512|PAC-NeRF]]

> [!star] Key Papers
> - [[2311.12198|PhysGaussian]] — Couples 3D Gaussian Splatting with continuum mechanics MPM solver; the foundational result that made 3DGS scenes physically interactive
> - [[2303.05512|PAC-NeRF]] — Physics-Augmented Continuum NeRF; jointly recovers geometry and material parameters (Young's modulus, density, plasticity) from video — the canonical material-from-pixels reference
> - [[2501.18982|OmniPhysGS]] — Constitutive Gaussians with ensemble of 12 expert constitutive networks (elastic/viscoelastic/plastic/fluid); custom PyTorch MPM solver cuts memory **75%** vs Warp-based baselines
> - [[2406.04338|Physics3D]] — Distills Young's modulus, viscosity, and plasticity into 3D Gaussians via SDS from video diffusion priors
> - [[2412.11258|GaussianProperty]] — Distills VLM priors into 3D Gaussians to predict per-Gaussian material properties; bridges VLMs and physical simulation

**4D Dynamic Scene & Diffusion-Prior Generation** — Generates 4D dynamic scenes or physical material properties by distilling video/image diffusion priors (SDS-style), without an explicit physics solver.
- [[2511.00503|Diff4Splat]], [[2506.19798|CoCo4D]], [[2505.18151|WonderPlay]], [[2412.11785|InterDyn]], [[2411.14423|PhysFlow]], [[2410.08257|NeuMA]], [[2410.07155|Trans4D]], [[2409.07179|Phy124]], [[2409.00558|Compositional-3D-Video]], [[2406.01476|DreamPhysics]], [[2405.16849|Sync4D]], [[2404.13026|PhysDreamer]], [[2404.09833|Video2Game]], [[2403.17920|TC4D]], [[2309.07906|Generative-Image-Dynamics]], [[2308.09713|Dynamic-3D-Gaussians]], [[2209.14988|DreamFusion]]

> [!star] Key Papers
> - [[2511.00503|Diff4Splat]] — Feed-forward 4D scene generation as deformable 3D Gaussian fields with explicit camera control; **60x** faster than per-scene optimization
> - [[2209.14988|DreamFusion]] — Introduced Score Distillation Sampling to optimize a NeRF against a frozen 2D text-to-image diffusion model; launched the entire text-to-3D generation subfield

**Specialized Physical Phenomena, Embodied Physics & Surveys** — Domain-specific physical phenomena (fluid, hair, rain, underwater), egocentric/robotic physics reasoning, and surveys of physics-informed vision.
- [[2606.27364|PhysiFormer]], [[2606.16202|EgoPhys]], [[2606.09806|TNO]], [[2603.23973|SLAT-Phys]], [[2603.03485|Phys4D]], [[2512.08269|EgoX]], [[2512.03422|3D-Scene-Rep-Survey]], [[2509.21541|ControlHair]], [[2507.01099|Geometry-aware-4D-Robot-Video]], [[2506.03150|IllumiCraft]], [[2503.21442|RainyGS]], [[2503.20746|PhysGen3D]], [[2503.04720|FluidNexus]], [[2503.04641|Multimodal-Generative-Models-Survey]], [[2502.03639|3DPointReg-I2V]], [[2501.10928|Generative-Physical-AI-Survey]], [[2404.01223|Feature-Splatting]], [[2305.18035|PICV-Survey]]

> [!star] Key Papers
> - [[2305.18035|PICV-Survey]] — Foundational taxonomy of physics-informed computer vision; covers observational/inductive/learning biases across 250+ papers

> [!star] Key Papers
> - [[2604.14268|HY-World-2.0]] — Tencent Hunyuan's open-source multi-modal 3D world framework unifying reconstruction + generation; high-fidelity 3DGS worlds in ~10 min
> - [[2604.15805|WorldComposer]] — Generates "Digital Cousins" from single panoramas; 0.91 Pearson correlation between sim and real-world policy success

**Spatial Intelligence Surveys** — Comprehensive reviews of 4D spatial intelligence, encompassing 3D understanding across time.
- [[2603.22057|SpatialBoost]], [[2512.24385|Spatial-Intelligence-Roadmap]], [[2507.21045|4D-Spatial-Intelligence-Survey]], [[2506.20134|3D-World-Models-Survey]], [[2504.15280|All-Angles-Bench]], [[2504.15037|MLLM-Spatial-Reasoning-Position-Paper]], [[2504.09848|LLM-Spatial-Intelligence-Survey]], [[2412.14171|VSI-Bench]]

> [!star] Key Papers
> - [[2507.21045|4D-Spatial-Intelligence-Survey]] — Five-level hierarchical taxonomy for 4D reconstruction; the most structured overview of spatial intelligence
> - [[2512.24385|Spatial-Intelligence-Roadmap]] — Maps the multi-modal pre-training trajectory from single-modality to unified foundation models for autonomous systems

> [!tip] 3D for Robotics
> 3D understanding is the missing link between VLMs and physical manipulation. RieMind and VEGA-3D show that explicit geometric grounding dramatically improves robot task performance. See [[11_Robotics-and-Embodied-AI]].

---

## 6. Domain Adaptation & Transfer Learning

Transferring visual models across domains, merging multiple fine-tuned models, and adapting to new distributions without full retraining. Critical for deploying perception in real-world environments that differ from training data.

**Robot & Humanoid Sim-to-Real Policy Transfer** — Sim-to-real transfer of robot/humanoid/quadruped control policies across embodiments, contact conditions, and tactile sensing.
- [[2606.06041|iCEM+TL]], [[2606.03297|SplitAdapter]], [[2606.02280|LDG]], [[2606.02027|World-Task-Factorization]], [[2606.01851|PHASOR]], [[2605.28812|CoP-Tactile]], [[2605.26638|HyperSim]], [[2605.23733|Any2Any]], [[2605.21688|Microfiber-Shape-Control]], [[2604.02911|DreamTIP]], [[2603.15759|SimDist]], [[2505.12672|TransferTraj]], [[2502.10894|UAN]], [[2502.01143|ASAP]], [[2501.16389|Sim2Real-Encoder-Eval]]

**Classic CNN & Segmentation Domain Adaptation** — Pre-transformer and segmentation-focused unsupervised domain adaptation for urban-scene and classification benchmarks.
- [[2207.11860|Trans4PASS+]], [[2204.13132|HRDA]], [[2204.00822|SAN-SAW]], [[2107.04034|RMA]], [[2103.15597|RobustNet]], [[2002.07953|DANCE]], [[1909.00889|DRPC]], [[1812.01754|M3SDA]], [[1811.10200|IDD]], [[1807.09441|IBN-Net]], [[1608.02192|Playing for Data]]

**Transformer & Foundation-Model Domain Adaptation** — ViT-, CLIP-, and DINOv2-based attention alignment techniques for unsupervised domain adaptation.
- [[2508.04987|UniMoS++]], [[2412.04073|TransAdapter]], [[2407.21311|EUDA]], [[2405.02797|VDPG]], [[2404.15817|VT-ADA]], [[2402.14976|Foundation-Latent-UDA]], [[2312.07871|MLNet]], [[2308.15855|IIDM]], [[2308.05659|AD-CLIP]], [[2303.13434|PMTrans]], [[2212.07740|TERT]], [[2204.07683|SSRT]], [[2111.12941|WinTR]], [[2110.03374|HCL]], [[2109.06165|CDTrans]], [[2108.05988|TVT]]

> [!star] Key Papers
> - [[2108.05988|TVT]] — Transferable Vision Transformer: pioneered attention-based domain alignment for ViTs
> - [[2407.21311|EUDA]] — Uses frozen DINOv2 features for efficient unsupervised domain adaptation; no fine-tuning needed

**Sim-to-Real Policy Transfer via RL** — Adapt reinforcement-learning policies trained in simulation to real-world or cross-platform dynamics via distribution reshaping, invariant feature representations, or distillation.
- [[2607.18154|World Translation]], [[2607.13319|OptCar]], [[2607.02037|Cross-Platform ASV RL]], [[2607.01410|BIFROST]], [[2606.31043|Warp RL]], [[2606.28476|FADA]], [[2603.22039|RAFL]], [[2507.23445|Physics-Guided-Gain-Regularization]], [[2503.20839|TAR]], [[2003.02471|BayRn]], [[1703.06907|Domain Randomization]], [[1702.02453|UP-OSI]]

**Source-Free & Low-Data Adaptation** — Adapt to a target domain when source data is unavailable due to privacy or storage constraints.
- [[2603.24322|HeuSCM]], [[2507.09961|TDCRL]], [[2507.00462|MS-TTA]], [[2506.00513|SSAM]], [[2406.10973|ExPLoRA]], [[2403.14410|GLC++]], [[2403.03421|LEAD]], [[2303.07110|GLC]], [[2303.01906|DPCL]], [[2211.03876|CoNMix]], [[2210.17067|UniOT]], [[2104.03344|OVANet]], [[2006.10726|Tent]]

> [!star] Key Papers
> - [[2406.10973|ExPLoRA]] — Parameter-efficient extended pre-training that adapts ViTs to new visual domains with minimal data

**Model Merging** — Combine multiple fine-tuned models into a single multitask model without retraining, by operating on parameter deltas.
- [[2607.00666|Domain Arithmetic]], [[2601.10497|MERGETUNE]], [[2510.21223|FDA]], [[2507.04380|Explainability-Task-Arithmetic]], [[2503.08998|Model-Merging-Approaches-Review]], [[2403.13257|MergeKit]], [[2403.01753|MuDSC]], [[2311.03099|DARE]], [[2306.01708|TIES-Merging]], [[2211.10277|TaskRes]]

> [!star] Key Papers
> - [[2306.01708|TIES-Merging]] — Three-step approach to resolve sign conflicts and redundancy when merging fine-tuned model parameters
> - [[2403.13257|MergeKit]] — Open-source toolkit that made model merging practical and accessible

**OOD Generalization & Robustness** — Predicting and improving model performance on out-of-distribution data.
- [[2607.18540|Recti-Q]], [[2605.05328|Query2Uncertainty]], [[2604.02260|Time-Varying-MBRL]], [[2603.21191|BST-Scaling-Rule]], [[2602.02140|GAPEVAL]], [[2511.13787|TC2]], [[2506.10133|Offline-Domain-Randomization]], [[2504.13292|GrokTransfer]], [[2502.16736|AdaConG]], [[2410.02735|OOD-Chameleon]], [[2404.04452|ViT-Domain-Robustness-Survey]], [[2305.18712|Transfer-Score]]

> [!star] Key Papers
> - [[2410.02735|OOD-Chameleon]] — Meta-learning framework that automatically selects the best OOD generalization strategy for a given distribution shift
> - [[2504.13292|GrokTransfer]] — Accelerates grokking via embedding transfer from weaker models; eliminates delayed generalization

**VLM-Based Adaptation** — Adapting vision-language models (CLIP and variants) to new domains via prompting, fine-tuning, or representation learning.
- [[2512.09441|MoP-CIL]], [[2509.02055|Align-Then-Steer]], [[2507.09615|FAIR]], [[2507.03657|ProtoMM]], [[2504.12104|Logits-DeConfusion]], [[2504.10428|PIU-Learning]], [[2504.06389|SemiDAViL]], [[2503.08497|MMRL]], [[2503.06626|DiffCLIP]], [[2411.04997|LLM2CLIP]], [[2407.15173|CLIP-Domain-Adaptation]], [[2407.07726|PaliGemma]], [[2407.01400|GalLoP]], [[2309.08912|MP-FGVC]], [[2308.06038|DiffTPT]], [[2210.03117|MaPLe (Multi-modal Prompt Learning)]], [[2209.07511|TPT]]

> [!star] Key Papers
> - [[2411.04997|LLM2CLIP]] — Integrates LLM text understanding into CLIP; +15.8 points on long-text retrieval over EVA02
> - [[2407.07726|PaliGemma]] — Google's sub-3B VLM achieving strong transfer across 40 tasks; proves small VLMs can rival large ones

**Additional methods** — Foundational transfer-learning studies, cross-spectral image translation, and surveys of domain adaptation/VLM generalization not covered by the sub-topics above.
- [[2607.05665|Morphological Similarity Transfer Learning]], [[2508.05547|VLM-Unsupervised-Adaptation-Survey]], [[2506.18504|VLM-Generalization-Survey]], [[2506.02843|REAP]], [[2503.19012|DiffV2IR]], [[1706.07522|DAH]], [[1411.1792|Transferable Features]]

> [!star] Key Papers
> - [[2506.18504|VLM-Generalization-Survey]] — Comprehensive survey of VLM generalization and adaptation methods; maps the taxonomy of domain shift strategies

> [!tip] Adaptation Strategy
> If source data is available, use TVT or TransAdapter. If source-free, use CoNMix. For combining specialists, TIES-Merging + MergeKit. For unknown domain shifts, OOD-Chameleon selects the right strategy automatically.

---

## 7. Few-Shot & Zero-Shot Learning

Learning from minimal examples or no examples at all. These methods enable visual systems to generalize to novel categories with 1-10 labeled samples per class, or transfer across visual domains with very limited target data.

**Cross-Domain Few-Shot Learning** — Few-shot learning where support and query sets come from different visual domains, requiring both category and domain transfer.
- [[2603.17655|CC-CDFSL]], [[2504.06608|Cross-Domain-FSL-with-DKM]], [[2502.14214|ACT]], [[2401.13987|ADAPTER]], [[2104.14385|ATA]], [[2010.07734|STARTUP]], [[2001.08735|LTL-FWT]]

> [!star] Key Papers
> - [[2401.13987|ADAPTER]] — Adaptive Transformer Networks for cross-domain few-shot; integrates domain alignment into the few-shot pipeline
> - [[2603.17655|CC-CDFSL]] — Self-supervised regularization framework achieving strong cross-domain few-shot transfer

**Additional methods** — Efficient few-shot tuning, auxiliary-data augmentation, generalized category discovery, and semantic augmentation methods not covered by the sub-topics above.
- [[2603.21138|Generative-ZSL-RL]], [[2601.08499|EfficientFSL]], [[2506.23822|LaZSL]], [[2506.04713|VEST]], [[2504.09828|FATE]], [[2408.05674|PS-TTL]], [[2302.00674|FLAD]], [[2301.02419|eTT]], [[2201.02609|GCD]], [[2004.02684|Attribute-Mix]]

> [!star] Key Papers
> - [[2601.08499|EfficientFSL]] — Provides a principled framework for few-shot learning efficiency across backbone sizes and shot counts
> - [[2302.00674|FLAD]] — Models auxiliary dataset selection as a Multi-Armed Bandit; automatically discovers which extra data helps
> - [[2201.02609|GCD]] — Formalized generalized category discovery; a more realistic setting than traditional zero-shot learning
> - [[2004.02684|Attribute-Mix]] — Semantic data augmentation via attribute-level feature mixing; +3.1% on CUB-200 without extra inference cost

> [!tip] Few-Shot Checklist
> Check domain gap first: same-domain few-shot is largely solved by DINOv2 + linear probe. Cross-domain few-shot (ADAPTER, CC-CDFSL) remains challenging. For discovering entirely new categories, use GCD.

---

## 8. Interpretability & Analysis

Understanding what vision models learn, explaining their decisions, and providing transparent reasoning. Essential for deploying vision systems in safety-critical applications.

**Interpretable Architectures** — Models designed from the ground up to produce human-understandable explanations of their predictions, plus sparse-autoencoder and retrieval-based post-hoc interpretability methods.
- [[2605.22658|SegCompass]], [[2604.10982|Psi-Map]], [[2505.15970|DINOv2-Hierarchy-SAE]], [[2502.16435|VISFACTOR]], [[2502.03714|USAE]], [[2501.09333|Prompt-CAM]], [[2411.10231|TaylorIR]], [[2311.04157|INTR]], [[2205.10268|B-cos-Networks]], [[2104.00032|CoDA-Nets]], [[1610.02391|Grad-CAM]], [[1512.04150|CAM (Class Activation Mapping)]]

> [!star] Key Papers
> - [[2205.10268|B-cos-Networks]] — Inherently interpretable deep networks via B-cos transform; explanations emerge from the architecture itself
> - [[2311.04157|INTR]] — Interpretable Transformer for fine-grained classification using prototype-based attention
> - [[2505.15970|DINOv2-Hierarchy-SAE]] — Discovers that DINOv2 implicitly learns hierarchical visual concepts (texture, parts, objects) in its layers
> - [[2411.10231|TaylorIR]] — 1x1 pixel-wise patch embeddings with TaylorShift attention; 60% memory reduction for transformer-based super-resolution

> [!tip] Interpretability in Practice
> B-cos Networks and INTR offer built-in explanations. For post-hoc analysis of frozen models, sparse autoencoders (USAE, DINOv2 Hierarchy SAE) reveal what features encode without modifying the model.

---

## 9. Efficient Training & Data

Practical methods for training vision models efficiently: dataset pruning, continual learning, knowledge distillation, and parameter-efficient fine-tuning. These techniques determine whether a method is publishable versus deployable.

**Model Compression, PEFT & Robustness** — Knowledge distillation, parameter-efficient fine-tuning, and adversarial robustness for deployable vision models.
- [[2607.10762|TOLiD]], [[2604.11138|ViserDex]], [[2604.10856|BridgeSim]], [[2509.18891|Point-Prompt-Defender]], [[2506.21046|dSVA]], [[2505.21501|PH-Reg]], [[2402.02242|V-PEFT-Bench]], [[2306.08543|MiniLLM]], [[2306.01872|Video Adapter]]

> [!star] Key Papers
> - [[2306.08543|MiniLLM]] — Reverse KL divergence + on-policy optimization for LLM distillation; produces higher-precision student models
> - [[2402.02242|V-PEFT-Bench]] — Comprehensive benchmark of visual PEFT methods; reveals which adapter designs actually matter
> - [[2506.21046|dSVA]] — Exploits self-supervised ViT features for adversarial attacks; outperforms prior methods by 13.7% on average transferability

**Data Curation & Training Efficiency** — Dataset pruning, weakly-supervised pre-training, continual learning, and high-resolution efficiency techniques.
- [[2604.11674|AffordSim]], [[2604.11386|ComSim]], [[2604.08626|WildDet3D]], [[2402.13349|Aria-Everyday-Activities]], [[2305.13622|SER]], [[2207.13050|Efficient-High-Resolution-Survey]], [[2205.09329|Dataset-Pruning]]

> [!star] Key Papers
> - [[2205.09329|Dataset-Pruning]] — Optimization-based pruning using influence functions; reduces training data while maintaining accuracy
> - [[2305.13622|SER]] — Strong Experience Replay with dual consistency loss; prevents catastrophic forgetting during sequential task learning
> - [[2207.13050|Efficient-High-Resolution-Survey]] — First comprehensive survey of efficient high-resolution deep learning; categorizes five families of approaches

> [!tip] Efficiency Stack
> Prune your dataset (Dataset Pruning) -> pre-train with SSL (DINOv2/MAE) -> fine-tune with PEFT (V-PEFT Bench recipes) -> distill for deployment (AM-RADIO/MiniLLM). Each stage compounds savings.


---

## Cross-References

- [[01_Foundation-Models]] — ViT and self-supervised backbones
- [[05_Vision-Language-Models]] — VLMs built on these visual features
- [[04_Video-and-Temporal]] — Extending spatial perception to temporal understanding
- [[11_Robotics-and-Embodied-AI]] — 3D perception for robotic manipulation

---

*Next: [[03_Diffusion-and-Generation]] for the generative counterpart to perception: synthesizing rather than recognizing.*
