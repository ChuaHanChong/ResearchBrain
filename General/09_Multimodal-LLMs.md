---
title: "Multimodal LLMs — Topic Overview"
tags:
  - multimodal
  - MLLM
  - instruction-tuning
  - vision-language
aliases:
  - MLLM Overview
---

# Multimodal LLMs

> [!abstract] Overview
> Multimodal LLMs extend language models with visual, audio, and other modalities. This topic covers architectures that process and generate across modalities — distinct from [[02_Vision-Language-Models|VLMs]] (which focus on vision-language alignment) and [[01_Foundation-Models]] (which cover the base architectures). The field has evolved from early encoder-decoder designs (BLIP, Flamingo) through instruction-tuned MLLMs (InstructBLIP, LLaVA) to unified native multimodal models (InternVL3, BAGEL) and efficient sub-3B deployments (SmolVLM, TinyVLM).

## Evolution Graph

```mermaid
graph TD
    subgraph "Foundational Alignment"
        A["CLIP (2021)"]
        B["BLIP (2022)"]
        C["CoCa (2022)"]
    end

    subgraph "Early MLLMs"
        D["InstructBLIP (2023)"]
        E["KOSMOS-2 (2023)"]
        F["Shikra (2023)"]
    end

    subgraph "Instruction-Tuned MLLMs"
        G["LLaVA-MORE (2025)"]
        H["Molmo (2024)"]
        I["PaliGemma (2024)"]
    end

    subgraph "Unified & Native Multimodal"
        J["InternVL3 (2025)"]
        K["BAGEL (2025)"]
        L["SAIL (2025)"]
    end

    subgraph "Efficient MLLMs"
        M["SmolVLM (2025)"]
        N["NVILA (2024)"]
        O["TinyVLM (2026)"]
    end

    A --> B --> D
    A --> C
    A --> E
    C --> D
    D --> G
    E --> F
    D --> H
    B --> I
    G --> J
    H --> J
    J --> K
    L --> K
    N --> M
    M --> O

    style A fill:#f0e8fd,stroke:#9b59b6
    style D fill:#e8f4fd,stroke:#4a90d9
    style J fill:#e8fde8,stroke:#27ae60
    style M fill:#fde8e8,stroke:#e74c3c
```

| Node | Paper |
|------|-------|
| CLIP | [[2103.00020\|CLIP]] |
| BLIP | [[2201.12086\|BLIP]] |
| CoCa | [[2205.01917\|CoCa]] |
| InstructBLIP | [[2305.06500\|InstructBLIP]] |
| KOSMOS-2 | [[2306.14824\|KOSMOS-2]] |
| Shikra | [[2306.15195\|Shikra]] |
| LLaVA-MORE | [[2503.15621\|LLaVA-MORE]] |
| Molmo | [[2409.17146\|Molmo]] |
| PaliGemma | [[2407.07726\|PaliGemma]] |
| InternVL3 | [[2504.10479\|InternVL3]] |
| BAGEL | [[2505.14683\|BAGEL]] |
| SAIL | [[2504.10462\|SAIL]] |
| SmolVLM | [[2504.05299\|SmolVLM]] |
| NVILA | [[2412.04468\|NVILA]] |
| TinyVLM | [[2603.00136\|TinyVLM]] |

---

## 1. Foundational Vision-Language Alignment

The core pretraining paradigms that established how to connect visual encoders with language models — from contrastive alignment to encoder-decoder fusion and multi-modal embedding spaces.

**Contrastive & Dual-Encoder Alignment** — Learning shared image-text embedding spaces through contrastive objectives on large-scale paired data.
- [[2103.00020|CLIP]], [[2212.07143|OpenCLIP]], [[2111.07991|LiT]], [[2406.17639|AlignCLIP]], [[2502.14786|SigLIP 2]], [[2505.04601|OpenVision]], [[2509.01644|OpenVision 2]], [[2507.22062|Meta CLIP 2]], [[2505.18983|AmorLIP]], [[2505.21549|DCLIP]], [[2411.04997|LLM2CLIP]], [[2505.03703|Modality Gap Reduction]], [[2506.03096|FuseLIP]]

> [!star] Key Papers
> - [[2103.00020|CLIP]] — Contrastive pre-training on 400M image-text pairs; launched the VLM era and enabled zero-shot transfer via text prompts
> - [[2502.14786|SigLIP 2]] — Multilingual vision-language encoders integrating decoder-based pretraining with sigmoid loss; advances over original SigLIP
> - [[2507.22062|Meta CLIP 2]] — Transparent, open-sourced methodology for training CLIP on native worldwide web data at scale

**Encoder-Decoder & Generative Alignment** — Architectures that unify contrastive and generative objectives for both understanding and generation.
- [[2201.12086|BLIP]], [[2205.01917|CoCa]], [[2206.07643|FIBER]], [[2305.05665|ImageBind]], [[2505.11815|UniMoCo]], [[2602.02381|AdaSSL]], [[2506.16895|STRUCTURE Alignment]]

> [!star] Key Papers
> - [[2201.12086|BLIP]] — Unified understanding and generation with bootstrapped captioning; self-cleans noisy web data
> - [[2205.01917|CoCa]] — Combined contrastive and generative objectives in a single model with decoupled text decoder
> - [[2305.05665|ImageBind]] — Extended alignment to six modalities (image, text, audio, depth, thermal, IMU) via a single embedding space

**CLIP Variants & Compositional Enhancement** — Improving CLIP's compositional understanding, fine-grained alignment, and domain-specific capabilities.
- [[2505.02278|GCLIP]], [[2504.16801|DeGLA]], [[2508.03102|CCA]], [[2512.11141|ItemizedCLIP]], [[2505.20229|CLIP Attribution SAE]], [[2406.14830|CLIP-Decoder]], [[2511.13876|QwenCLIP]]

> [!star] Key Papers
> - [[2505.02278|GCLIP]] — Training-free method enhancing CLIP's compositional understanding through grounding
> - [[2504.16801|DeGLA]] — Decoupled Global-Local Alignment for compositional VLM understanding
> - [[2511.13876|QwenCLIP]] — Medical vision-language pretraining framework adapting CLIP to clinical domains

> [!tip] The Alignment Stack
> The field converged on a three-layer alignment stack: (1) contrastive pretraining for broad zero-shot transfer (CLIP, SigLIP 2), (2) generative alignment for understanding + generation (BLIP, CoCa), and (3) compositional refinement for fine-grained reasoning (GCLIP, DeGLA). Each layer builds on the previous, and modern MLLMs inherit all three.

---

## 2. Early Multimodal LLMs

The first generation of models that connected visual encoders to large language models, establishing the MLLM paradigm through Q-Former bridges, instruction tuning, and grounded dialogue.

**Pioneering MLLM Architectures** — The initial designs for feeding visual information into frozen or fine-tuned LLMs.
- [[2305.06500|InstructBLIP]], [[2306.14824|KOSMOS-2]], [[2306.15195|Shikra]], [[2204.00598|Socratic Models]], [[2309.05519|NExT-GPT]], [[2305.14676|GRILL]], [[2211.09699|PromptCap]]

> [!star] Key Papers
> - [[2305.06500|InstructBLIP]] — Instruction-tuned BLIP-2 with Q-Former; established systematic instruction tuning for vision-language models
> - [[2306.14824|KOSMOS-2]] — Grounded MLLM generating bounding boxes alongside text; first model unifying vision-language understanding with spatial grounding
> - [[2306.15195|Shikra]] — Processes spatial coordinates as natural language tokens for referential dialogue without extra modules

**Region-Level & Grounded Understanding** — Early approaches to fine-grained visual understanding at the region or object level within MLLMs.
- [[2307.03601|GPT4RoI]], [[2308.00692|LISA]], [[2310.11441|SoM]], [[2203.17273|FindIt]], [[2104.12763|MDETR]]

> [!star] Key Papers
> - [[2308.00692|LISA]] — Introduced reasoning segmentation, enabling MLLMs to generate precise segmentation masks from complex language queries
> - [[2310.11441|SoM]] — Set-of-Mark visual prompting: overlays alphanumeric markers on images to unlock GPT-4V's fine-grained grounding

> [!tip] The Q-Former Legacy
> InstructBLIP's Q-Former bridge became the dominant early connector between frozen vision encoders and LLMs. While later work moved toward simpler linear projections (LLaVA) and native multimodal training (InternVL3), the principle of a learnable cross-modal bottleneck persists in modern designs.

---

## 3. Instruction-Tuned & Production MLLMs

The maturation of MLLMs through systematic instruction tuning, scaling to production quality, and comparative studies of different LLM backbones and training recipes.

**Flagship Instruction-Tuned Models** — Full-scale MLLMs trained with instruction-following data across diverse vision-language tasks.
- [[2407.07726|PaliGemma]], [[2409.17146|Molmo]], [[2503.15621|LLaVA-MORE]], [[2502.13130|Magma]], [[2505.07062|Seed1.5-VL]], [[2410.08202|Mono-InternVL]]

> [!star] Key Papers
> - [[2407.07726|PaliGemma]] — Sub-3B parameter VLM achieving SOTA across 40+ tasks; demonstrated small models can match larger counterparts
> - [[2409.17146|Molmo]] — Family of open-weight VLMs with PixMo dataset; competitive with proprietary models while fully open
> - [[2503.15621|LLaVA-MORE]] — Systematic comparative study of MLLM design choices across LLM backbones and training strategies

**Instruction Data & Training Pipelines** — Methods for creating high-quality multimodal instruction data and optimizing training procedures.
- [[2412.07012|ProVision]], [[2504.21850|COMPACT]], [[2506.08429|SCALE]], [[2505.08971|PRIOR]], [[2505.17316|Patch-Aligned Training]], [[2504.15619|AdaViP]]

> [!star] Key Papers
> - [[2412.07012|ProVision]] — Programmatic system for generating diverse vision-language instruction data at scale
> - [[2504.21850|COMPACT]] — Generates compositionally complex visual instruction tuning data for improved MLLM reasoning
> - [[2506.08429|SCALE]] — Automated pipeline curating high-quality multimodal instruction datasets with LLM-based filtering

**Model Merging & Adaptation** — Combining multiple fine-tuned models or adapting MLLMs to new domains without full retraining.
- [[2408.07666|Model Merging Survey]], [[2502.17159|RobustMerge]], [[2601.07645|PlaM]], [[2412.01282|Align-KD]], [[2505.10088|MMRL++]], [[2503.08497|MMRL]]

> [!star] Key Papers
> - [[2502.17159|RobustMerge]] — Training-free, data-free, storage-free model merging specifically designed for VLMs
> - [[2601.07645|PlaM]] — Training-free model merging preserving complementary knowledge from multiple fine-tuned models

> [!tip] Instruction Tuning is the Key
> The gap between a raw VLM and a usable MLLM is instruction tuning. PaliGemma showed that a well-tuned 3B model beats poorly tuned 13B+ models. The bottleneck has shifted from model size to data quality — SCALE, ProVision, and COMPACT address this directly.

---

## 4. Unified & Native Multimodal Models

A new generation of models trained end-to-end on interleaved multimodal data rather than bolting visual modules onto text-only LLMs, achieving seamless cross-modal understanding and generation.

**Native Multimodal Architectures** — Models pre-trained jointly on vision and language from scratch, eliminating the modular vision encoder + LLM pipeline.
- [[2504.10479|InternVL3]], [[2505.14683|BAGEL]], [[2504.10462|SAIL]], [[2503.20680|VoRA]], [[2506.17202|UniFork]], [[2601.03193|UniCorn]], [[2504.17432|UniME]]

> [!star] Key Papers
> - [[2504.10479|InternVL3]] — Native multimodal pre-training paradigm jointly acquiring visual and linguistic capabilities; new MLLM SOTA
> - [[2505.14683|BAGEL]] — Open-source unified multimodal foundation model; trained on trillions of interleaved tokens for both understanding and generation
> - [[2503.20680|VoRA]] — Encoder-free MLLM treating visual features as LoRA parameters; eliminates the separate vision encoder entirely

**Multimodal Scaling Laws & Pre-Training** — Understanding how to scale native multimodal models and what training recipes work best.
- [[2504.07951|NMM Scaling Laws]], [[2412.18619|Multimodal NTP Survey]], [[2503.19903|PS3]], [[2509.26625|LLM Visual Priors]]

> [!star] Key Papers
> - [[2504.07951|NMM Scaling Laws]] — First comprehensive study of scaling laws for native multimodal models; shows joint training outperforms modular approaches
> - [[2509.26625|LLM Visual Priors]] — Demonstrates that LLM weights carry useful visual priors before any visual training

**Unified Understanding & Generation** — Models bridging the comprehension-generation gap to handle both tasks in a single framework.
- [[2601.03193|UniCorn]], [[2603.03241|UniG2U-Bench]], [[2602.22766|CapImagine]], [[2506.22880|DeSa2VA]]

> [!star] Key Papers
> - [[2601.03193|UniCorn]] — Autonomously bridges comprehension and generation capabilities within a single model
> - [[2506.22880|DeSa2VA]] — Decouples textual and visual generation in MLLMs for improved quality in both

> [!tip] The Native Multimodal Shift
> The field is moving from "LLM + vision encoder" to jointly pre-trained multimodal models. InternVL3 and NMM Scaling Laws demonstrate that native multimodal training outperforms modular assembly. VoRA pushes this further by eliminating the encoder entirely. This trend mirrors how text-only LLMs evolved from pipeline systems to end-to-end models.

---

## 5. Visual Encoding & Feature Integration

How visual information is encoded, projected, and integrated into the language model — from vision encoder design to cross-modal connectors and feature fusion strategies.

**Vision Encoder Design** — Building and improving the visual backbone that feeds MLLMs.
- [[2411.14402|AIMV2]], [[2504.13181|Perception Encoder]], [[2507.01643|SAILViT]], [[2505.22664|VLM Surrogate Grafting]], [[2505.24541|Mixpert]], [[2510.21501|GranViT]], [[2512.10942|VL-JEPA]], [[2512.15885|JARVIS]], [[2602.01905|STELLAR]]

> [!star] Key Papers
> - [[2411.14402|AIMV2]] — Apple's autoregressive + contrastive pre-training for vision encoders; strong zero-shot transfer
> - [[2504.13181|Perception Encoder]] — Family of vision models achieving SOTA across diverse tasks; designed as universal perception backbone
> - [[2512.10942|VL-JEPA]] — Joint Embedding Predictive Architecture for vision-language; shows latent prediction outperforms reconstruction

**Cross-Modal Connectors & Feature Fusion** — Mechanisms for projecting visual features into the LLM's embedding space.
- [[2503.06063|Multi-Layer Visual Fusion]], [[2504.21447|Shallow ViT Features]], [[2506.01850|MoDA]], [[2506.16691|LaVi]], [[2506.17608|HIRE]], [[2410.13733|Arcana]], [[2509.07979|VIRAL]], [[2512.06281|LaVer]], [[2602.20980|CrystaL]]

> [!star] Key Papers
> - [[2503.06063|Multi-Layer Visual Fusion]] — Systematic analysis showing multi-layer visual features outperform single-layer for MLLMs
> - [[2504.21447|Shallow ViT Features]] — Demonstrates shallow ViT layers carry critical information that deep layers discard
> - [[2506.01850|MoDA]] — Modulation Adapter dynamically refining pre-aligned visual features for the LLM

**Position Encoding for Vision** — Adapting positional encodings for visual tokens in multimodal contexts.
- [[2505.16416|Circle-RoPE]], [[2505.20444|HoPE]], [[2505.21465|ID-Align]], [[2601.15275|RayRoPE]]

> [!star] Key Papers
> - [[2505.16416|Circle-RoPE]] — Decoupled rotary position encoding for visual and textual tokens; resolves position conflicts in MLLMs
> - [[2601.15275|RayRoPE]] — Projective ray positional encoding for multi-view transformers using 3D geometric priors

**High-Resolution & Multi-Scale Processing** — Handling high-resolution images without losing fine-grained details.
- [[2412.13871|LLaVA-UHD v2]], [[2502.16025|FeatSharp]], [[2506.12776|NativeRes-LLaVA]], [[2506.01663|Zoom-Refine]]

> [!star] Key Papers
> - [[2412.13871|LLaVA-UHD v2]] — Hierarchical Window Transformer for native high-resolution MLLM input processing
> - [[2502.16025|FeatSharp]] — Generates sharper high-resolution features from low-resolution vision encoders without retraining

> [!tip] The Feature Integration Bottleneck
> How visual features reach the LLM matters as much as the encoder quality. Multi-Layer Visual Fusion and Shallow ViT Features show that using only the final encoder layer loses critical information. Meanwhile, position encoding (Circle-RoPE, HoPE) is emerging as an underappreciated factor in MLLM visual understanding.

---

## 6. Efficient & Compact MLLMs

Reducing MLLM inference cost through token compression, model compression, and compact architectures designed for resource-constrained deployment.

**Visual Token Reduction** — Dynamically pruning or merging visual tokens to reduce the computational burden of processing images.
- [[2503.16660|Adaptive Token Reduction]], [[2504.17040|DyMU]], [[2504.00557|Trimmed Llama]], [[2505.22654|VScan]], [[2506.10967|CDPruner]], [[2506.07138|STF]], [[2506.01097|Explainability-Guided Token Compression]], [[2505.16411|SPIN]]

> [!star] Key Papers
> - [[2504.17040|DyMU]] — Training-free framework dynamically reducing visual tokens based on image complexity
> - [[2506.10967|CDPruner]] — Training-free token pruning leveraging content-dependency analysis
> - [[2505.22654|VScan]] — Two-stage framework achieving up to 90% visual token reduction with minimal quality loss

**Compact Model Architectures** — Building small but capable MLLMs under 3B parameters for edge deployment.
- [[2504.05299|SmolVLM]], [[2504.00595|Open-Qwen2VL]], [[2603.06569|Penguin-VL]], [[2603.00136|TinyVLM]], [[2411.09691|TinyGroundingGPT]], [[2412.04468|NVILA]]

> [!star] Key Papers
> - [[2504.05299|SmolVLM]] — Family of compact multimodal models (256M-2B) processing images and video; competitive with much larger models
> - [[2603.00136|TinyVLM]] — Zero-shot object detection on microcontrollers; sub-1MB models for edge deployment
> - [[2412.04468|NVILA]] — NVIDIA's efficient MLLM family achieving competitive quality at reduced compute

**Efficient Inference & Acceleration** — Methods for speeding up MLLM inference at deployment time.
- [[2505.10526|MASSV]], [[2410.19878|PEFT Methodologies Survey]]

> [!star] Key Papers
> - [[2505.10526|MASSV]] — Speculative decoding framework accelerating VLM inference through multi-head parallel generation

> [!tip] The Efficiency Imperative
> Token reduction is the most impactful lever for MLLM efficiency — VScan and CDPruner achieve 70-90% token reduction with minimal quality loss. For deployment, SmolVLM and TinyVLM show that architecture-level compactness combined with token reduction enables MLLMs on edge devices. The key insight: most visual tokens are redundant for any given query.

---

## 7. Hallucination Mitigation

Addressing the fundamental challenge of MLLMs generating text that contradicts visual evidence — through decoding strategies, contrastive methods, preference optimization, and evaluation frameworks.

**Decoding-Based Methods** — Modifying the generation process to suppress hallucinated content without retraining.
- [[2406.01920|CODE]], [[2508.11616|MRGD]], [[2506.08391|SECOND]], [[2509.03113|GACD]], [[2506.09522|ReVisiT]], [[2512.23453|CoFi-Dec]], [[2602.11737|OA-VCD]], [[2602.16702|SAP]], [[2507.00898|ONLY]]

> [!star] Key Papers
> - [[2406.01920|CODE]] — Training-free decoding method reducing hallucination through contrastive output distributions
> - [[2509.03113|GACD]] — Gradient-based influence-aware constrained decoding; first to use gradient information for hallucination mitigation
> - [[2512.23453|CoFi-Dec]] — Coarse-to-fine decoding leveraging geometric consistency for grounded generation

**Visual Attention & Token Intervention** — Steering the model's visual attention to reduce over-reliance on language priors.
- [[2506.12609|VisFlow]], [[2603.00207|VisRef]], [[2505.17812|VaLSe]], [[2508.02419|TVAI]], [[2602.21497|ECRD]], [[2602.24041|AIR]]

> [!star] Key Papers
> - [[2506.12609|VisFlow]] — Dual-level attention intervention redirecting model focus toward relevant visual tokens
> - [[2508.02419|TVAI]] — Identifies modality bias as a root cause of hallucination; proposes targeted visual attention injection

**Visual Prompting Against Hallucination** — Using visual cues and prompts to anchor model outputs in visual evidence.
- [[2504.21559|BBVPE]], [[2506.16112|AutoV]], [[2601.00659|CRoPS]], [[2510.16596|SHIELD]], [[2506.07227|MED]]

> [!star] Key Papers
> - [[2504.21559|BBVPE]] — Black-box visual prompt engineering mitigating hallucination without model access
> - [[2601.00659|CRoPS]] — Dynamic cropping strategy forcing models to attend to relevant image regions

**Preference Optimization & Training-Based** — Aligning MLLM outputs with visual ground truth through preference learning and targeted fine-tuning.
- [[2504.15619|AdaViP]], [[2602.22859|DPE]], [[2506.17901|PostAlign]]

> [!star] Key Papers
> - [[2504.15619|AdaViP]] — Adaptive visual preference optimization reducing hallucination through contrastive visual grounding
> - [[2506.17901|PostAlign]] — Post-training alignment framework improving visual fidelity without catastrophic forgetting

**Hallucination Analysis & Benchmarks** — Understanding when, why, and how MLLMs hallucinate.
- [[2310.00754|LURE]], [[2402.00253|LVLM Hallucination Survey]], [[2502.17422|MLLM Small Visual Details]]

> [!star] Key Papers
> - [[2402.00253|LVLM Hallucination Survey]] — Comprehensive taxonomy of hallucination types in large vision-language models
> - [[2502.17422|MLLM Small Visual Details]] — Reveals fundamental limitations in MLLM perception of small visual details

> [!tip] Defense in Depth
> No single method solves hallucination. The most effective approach combines decoding-time intervention (CODE, GACD) with attention steering (VisFlow, TVAI) and preference alignment (AdaViP). LURE and the LVLM Survey provide the diagnostic framework for understanding which hallucination types affect your specific use case.

---

## 8. Visual Grounding & Spatial Understanding

Enabling MLLMs to localize, reference, and reason about specific objects and regions in images — from bounding box prediction to dense spatial reasoning.

**Grounded MLLMs** — Models that jointly generate text and spatial coordinates for objects.
- [[2404.13013|Groma]], [[2405.17104|LLM-Optic]], [[2405.19783|IVM]], [[2410.08021|OneRef]], [[2401.17981|MLLM Detection Infusion]], [[2411.09691|TinyGroundingGPT]], [[2511.06908|Mono3DVG-EnSD]]

> [!star] Key Papers
> - [[2404.13013|Groma]] — Localized visual tokenizer for robust MLLM visual grounding at the region level
> - [[2405.19783|IVM]] — Instruction-guided visual masking that automatically highlights task-relevant image regions

**Visual Prompting for MLLMs** — Methods for communicating spatial information to MLLMs through visual annotations and markers.
- [[2304.06712|Visual Prompt Engineering]], [[2409.15310|Visual Prompting MLLM Survey]], [[2407.01400|GalLoP]], [[2510.09201|MPO]], [[2506.16112|AutoV]]

> [!star] Key Papers
> - [[2409.15310|Visual Prompting MLLM Survey]] — Comprehensive survey of visual prompting techniques for MLLMs; taxonomizes the field
> - [[2510.09201|MPO]] — Multimodal Prompt Optimizer jointly optimizing textual and visual prompts

**Dense Perception & Tracking** — Fine-grained visual understanding including tracking, referring, and pixel-level grounding.
- [[2510.23603|PixelRefer]], [[2512.22799|VPTracker]], [[2603.03857|DeepScan]], [[2505.20612|RF100-VL]], [[2505.23769|TextRegion]], [[2309.08912|MP-FGVC]]

> [!star] Key Papers
> - [[2510.23603|PixelRefer]] — Unified framework for fine-grained spatiotemporal object understanding in images and videos
> - [[2512.22799|VPTracker]] — Location-aware visual prompting enabling MLLMs for multi-object tracking

**Spatial Reasoning & Scene Understanding** — Going beyond object detection to understand spatial relationships and scene structure.
- [[2601.05600|SceneAlign]], [[2602.15950|VLM Spatial Reasoning OCR]], [[2506.21710|FOCUS]]

> [!star] Key Papers
> - [[2601.05600|SceneAlign]] — Aligns MLLMs with scene-level spatial structure for holistic visual understanding
> - [[2602.15950|VLM Spatial Reasoning OCR]] — Reveals consistent spatial reasoning degradation in VLMs on OCR-related tasks

> [!tip] Grounding as First-Class Capability
> Grounding is no longer an afterthought — KOSMOS-2 and Shikra (Section 2) showed it can be native. The trend is toward models that ground by default (Groma, PixelRefer) rather than requiring external detection modules. For robotics applications, this shift is critical — see [[07_Robotics-and-Embodied-AI]].

---

## 9. Video & Temporal MLLMs

Extending multimodal understanding to video inputs, requiring models to handle temporal dynamics, long-form content, and cross-frame reasoning.

- [[2602.05986|RISE-Video]], [[2602.20159|VBVR]], [[2506.06279|CoMemo]], [[2507.01544|MARVIS]], [[2602.01984|Delimiter Token Scaling]]

> [!star] Key Papers
> - [[2602.05986|RISE-Video]] — Comprehensive benchmark for evaluating MLLMs on temporal video reasoning
> - [[2602.20159|VBVR]] — Community-curated dataset with over one million video reasoning examples
> - [[2506.06279|CoMemo]] — Dual-path architecture addressing the long-context memory problem in video MLLMs

> [!tip] The Video Frontier
> Video MLLMs remain significantly behind image MLLMs in capability. The core challenge is temporal context — CoMemo and Delimiter Token Scaling address this through specialized memory and multi-frame architectures. RISE-Video and VBVR provide the benchmarks needed to drive progress.

---

## 10. Reasoning & Trustworthiness

Methods for improving MLLM reasoning capabilities and estimating the reliability of model outputs.

**Visual Reasoning** — Enhancing the chain-of-thought and compositional reasoning abilities of MLLMs.
- [[2502.07503|RINS]], [[2603.02556|VC-STaR]], [[2410.10855|CoreCognition]], [[2504.14200|KeCO]], [[2506.09047|Back-Patching VLM]], [[2506.08008|VLMs Overlook Visual Representations]], [[2506.11515|Manager]], [[2504.18397|UV-CoT]]

> [!star] Key Papers
> - [[2502.07503|RINS]] — Recursive Inference Scaling from Google DeepMind; enhances MLLM performance through iterative self-refinement
> - [[2603.02556|VC-STaR]] — Visual Contrastive Self-Taught Reasoner improving VLM reasoning through contrastive self-training

**Trustworthiness, Safety & Robustness** — Evaluating and improving the reliability of MLLM outputs.
- [[2505.23745|TrustVLM]], [[2602.21054|VAUQ]], [[2601.14127|MIR-SafetyBench]], [[2602.01816|VIA-Bench]], [[2506.22982|CroPA]], [[2406.18925|VisArgs]], [[2504.18053|DREAM]]

> [!star] Key Papers
> - [[2505.23745|TrustVLM]] — Framework estimating prediction trustworthiness by combining internal and external confidence signals
> - [[2602.21054|VAUQ]] — Training-free self-evaluation framework quantifying visual vs. textual reliance in MLLM predictions
> - [[2601.14127|MIR-SafetyBench]] — First benchmark for evaluating safety risks from multi-image reasoning in MLLMs

**Continual & Incremental Learning** — Enabling MLLMs to acquire new knowledge without forgetting prior capabilities.
- [[2410.19925|MLLM Continual Learning]], [[2508.04227|VLM Continual Learning Survey]], [[2512.09441|MoP-CIL]]

> [!star] Key Papers
> - [[2410.19925|MLLM Continual Learning]] — Systematic quantification of linguistic forgetting in continually trained MLLMs
> - [[2508.04227|VLM Continual Learning Survey]] — Comprehensive taxonomy of continual learning challenges specific to VLMs

> [!tip] Beyond Accuracy
> MLLM deployment requires more than benchmark scores. TrustVLM and VAUQ address confidence calibration, MIR-SafetyBench covers safety under multi-image inputs, and continual learning (MoP-CIL) ensures models do not degrade as they are updated. These are prerequisites for real-world deployment.

---

## 11. Interpretability & Mechanistic Analysis

Understanding what MLLMs learn internally — which visual features matter, how cross-modal representations are structured, and why models produce specific outputs.

- [[2602.00462|LatentLens]], [[2603.07335|VisualScratchpad]], [[2506.11976|VLM Visual-Language Alignment]], [[2510.02292|VLM-Lens]], [[2504.19627|VCM]], [[2602.11144|GENIUS]], [[2602.02140|GAPEVAL]]

> [!star] Key Papers
> - [[2602.00462|LatentLens]] — Training-free method interpreting visual token representations layer-by-layer inside MLLMs
> - [[2603.07335|VisualScratchpad]] — Interactive framework using Sparse Autoencoders to analyze and causally test visual features
> - [[2510.02292|VLM-Lens]] — Unified toolkit for systematically extracting and analyzing internal VLM representations

> [!tip] Interpretability Enables Improvement
> LatentLens and VLM-Lens reveal what MLLMs actually attend to, which directly informs hallucination mitigation (Section 7) and feature integration (Section 5). Understanding internal representations is not academic curiosity — it is the diagnostic tool for improving model quality.

---

## 12. Adaptation, Recognition & Retrieval

Applying MLLMs and VLMs to downstream tasks including fine-grained recognition, image-text retrieval, domain adaptation, and specialized applications.

**Fine-Grained Recognition** — Leveraging MLLM capabilities for detailed visual categorization and recognition tasks.
- [[2505.01064|NeaR]], [[2507.23070|E-FineR]], [[2507.10202|ECP]], [[2505.02056|VLM Pseudo-label Calibration]], [[2505.16149|REVEAL]], [[2505.11192|FALCON]], [[2507.10203|ARL]]

> [!star] Key Papers
> - [[2505.01064|NeaR]] — Vocabulary-free fine-grained visual recognition combining MLLM-generated descriptions with retrieval
> - [[2507.23070|E-FineR]] — Fully automated, training-free fine-grained recognition without predefined vocabularies

**Retrieval & Composition** — Methods for image-text retrieval and composed image retrieval using VLMs.
- [[2505.19707|MVFT-JI]], [[2506.23115|MoCa]], [[2503.23508|Real-LOD]], [[2603.02959|SS-Text-U]], [[2508.04987|UniMoS++]]

> [!star] Key Papers
> - [[2505.19707|MVFT-JI]] — Zero-shot composed image retrieval through direct VLM fine-tuning
> - [[2506.23115|MoCa]] — Transforms causal VLMs into bidirectional encoders for robust retrieval

**Specialized Applications** — MLLMs applied to specific domains and unconventional tasks.
- [[2505.21497|PosterAgent]], [[2601.12585|MLLM Visualization Literacy]], [[2507.01955|GPT-4o Vision Evaluation]], [[2305.00104|MMViT]], [[2511.11007|VisMem]], [[2506.22395|Test-Time VLM Consistency]]

> [!star] Key Papers
> - [[2505.21497|PosterAgent]] — Automated academic poster generation from papers; demonstrates creative MLLM applications
> - [[2601.12585|MLLM Visualization Literacy]] — First taxonomy of visualization literacy barriers in MLLMs

> [!tip] MLLMs as General Visual Assistants
> The fine-grained recognition results (NeaR, E-FineR) show that MLLMs can replace specialized classifiers when paired with the right prompting strategy. For retrieval, MoCa's trick of converting causal models to bidirectional encoders unlocks capabilities that the original training never intended.

---

## 13. Open-Vocabulary Detection with MLLMs

Extending MLLM capabilities to open-vocabulary object detection — detecting objects described by arbitrary text at inference time.

- [[2209.09407|DetCLIP]], [[2304.04514|DetCLIPv2]], [[2209.15639|F-VLM]], [[2505.23004|QLIP]], [[2502.17425|VPT]]

> [!star] Key Papers
> - [[2304.04514|DetCLIPv2]] — End-to-end pre-training for open-vocabulary detection learning directly from large-scale image-text data
> - [[2209.15639|F-VLM]] — Open-vocabulary detection using frozen VLMs with minimal training overhead
> - [[2502.17425|VPT]] — Visual Perception Tokens enabling MLLMs to dynamically attend to detection-relevant regions

> [!tip] Detection Without Boundaries
> Open-vocabulary detection removes the fixed-class bottleneck. DetCLIPv2 and F-VLM show that CLIP-style alignment can drive detection, while VPT demonstrates that MLLMs can be steered toward detection tasks through learned perception tokens. See [[02_Vision-Language-Models]] for the broader open-vocabulary detection landscape.

---

## 14. Surveys & Meta-Analyses

Comprehensive overviews and large-scale analyses of the MLLM field.

- [[2306.13549|MLLM Survey]], [[2405.10739|Efficient MLLM Survey]], [[2501.02189|VLM Survey 2025]], [[2501.02765|VLLM Survey]], [[2510.09586|VLM Survey 26K]], [[2012.12556|Visual Transformer Survey]]

> [!star] Key Papers
> - [[2306.13549|MLLM Survey]] — First comprehensive synthesis of the MLLM field covering architectures, training, and evaluation
> - [[2405.10739|Efficient MLLM Survey]] — Categorizes efficiency techniques across the full MLLM pipeline
> - [[2510.09586|VLM Survey 26K]] — Quantitative meta-analysis of 26,104 papers from top-tier AI conferences; maps the VLM research landscape

> [!tip] Navigating the Literature
> With 26K+ VLM papers across three years of top conferences, surveys are essential navigation aids. Start with the MLLM Survey (2023) for foundations, then the VLM Survey 2025 for recent advances, and the Efficient MLLM Survey for deployment-oriented work.

---

## Cross-References

- [[01_Foundation-Models]] — Backbone architectures (ViT, DINO, CLIP)
- [[02_Vision-Language-Models]] — Vision-language alignment, prompt learning, open-vocabulary detection
- [[03_Reasoning-and-Planning]] — Reasoning capabilities built on MLLMs
- [[05_Computer-Vision-and-3D]] — 3D and spatial understanding
- [[07_Robotics-and-Embodied-AI]] — MLLMs as perception backbone for VLAs
- [[12_Diffusion-and-Generation]] — Generation models that complement MLLM understanding

---

*Next: [[10_Agents-and-Tool-Use]] for how MLLMs are deployed as autonomous agents.*
