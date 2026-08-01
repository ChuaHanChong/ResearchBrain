---
title: "Multimodal LLMs — Topic Overview"
tags:
  - multimodal
  - MLLM
  - instruction-tuning
  - vision-language
aliases:
  - "MLLM Overview"
---

# Multimodal LLMs

> [!abstract] Overview
> Multimodal LLMs extend language models with visual, audio, and other modalities. This topic covers architectures that process and generate across modalities — distinct from [[05_Vision-Language-Models]] (which focus on vision-language alignment) and [[01_Foundation-Models]] (which cover the base architectures). The field has evolved from early encoder-decoder designs (BLIP, Flamingo) through instruction-tuned MLLMs (InstructBLIP, LLaVA) to unified native multimodal models (InternVL3, BAGEL) and efficient sub-3B deployments (SmolVLM, TinyVLM).

## Evolution Graph

```text
Foundational Vision-Language Alignment

╔════════════════╗
║ *CLIP (2021)   ║──┬──► BLIP (2022)
╚════════════════╝  ├──► CoCa (2022)
                    └──► InstructBLIP (2023)  [Early MLLMs]

┌────────────────┐
│ BLIP (2022)    │──┬──► InstructBLIP (2023)   [Early MLLMs]
└────────────────┘  └──► PaliGemma (2024)      [Instruction-Tuned MLLMs]

┌────────────────┐
│ CoCa (2022)    │─────► InstructBLIP (2023)   [Early MLLMs]
└────────────────┘


Early MLLMs

╔═════════════════════════╗
║ *InstructBLIP (2023)    ║──┬──► LLaVA-MORE (2025)  [Instruction-Tuned MLLMs]
╚═════════════════════════╝  └──► Molmo (2024)       [Instruction-Tuned MLLMs]

┌─────────────────┐
│ KOSMOS-2 (2023) │─────► Shikra (2023)   (leaf)
└─────────────────┘


Instruction-Tuned MLLMs

┌────────────────────┐
│ LLaVA-MORE (2025)  │─────► InternVL3 (2025)  [Unified & Native Multimodal]
└────────────────────┘

┌────────────────┐
│ Molmo (2024)   │─────► InternVL3 (2025)      [Unified & Native Multimodal]
└────────────────┘

┌────────────────────┐
│ PaliGemma (2024)   │   (leaf, no outgoing edges)
└────────────────────┘


Unified & Native Multimodal

╔════════════════════╗
║ *InternVL3 (2025)  ║─────► BAGEL (2025)
╚════════════════════╝

┌────────────────┐
│ SAIL (2025)    │─────► BAGEL (2025)
└────────────────┘

┌────────────────┐
│ BAGEL (2025)   │   (leaf; receives from InternVL3 + SAIL above)
└────────────────┘


Efficient MLLMs                              (disconnected sub-graph, no edges to/from groups above)

┌────────────────┐     ╔═══════════════════╗     ┌─────────────────┐
│ NVILA (2024)   │────►║ *SmolVLM (2025)   ║────►│ TinyVLM (2026)  │
└────────────────┘     ╚═══════════════════╝     └─────────────────┘

Legend: ╔═╗ double border + "*" prefix = landmark/foundational paper.
```

The field evolved through four phases: **foundational alignment** (2021-2022) where CLIP, BLIP, and CoCa established vision-language pretraining paradigms; **early MLLMs** (2023) where InstructBLIP, KOSMOS-2, and Shikra connected visual encoders to LLMs with instruction tuning and grounding; **instruction-tuned MLLMs** (2024-2025) where LLaVA-MORE, Molmo, and PaliGemma refined the recipe for general-purpose multimodal understanding; and **unified native multimodal + efficient deployment** (2024-2026) where InternVL3 and BAGEL achieved native multi-task generation while SmolVLM and TinyVLM pushed sub-3B parameter efficiency.

| Year | Paper | Contribution |
|------|-------|-------------|
| 2021 | [[2103.00020\|CLIP]] | Contrastive pretraining on 400M image-text pairs; enabled zero-shot visual recognition via natural language |
| 2022 | [[2201.12086\|BLIP]] | Unified vision-language understanding and generation with bootstrapped caption filtering for noisy web data |
| 2022 | [[2205.01917\|CoCa]] | Combined contrastive and generative objectives in a single model with decoupled text decoder |
| 2023 | [[2305.06500\|InstructBLIP]] | Applied instruction tuning to VLMs with instruction-aware visual features; SOTA zero-shot on unseen tasks |
| 2023 | [[2306.14824\|KOSMOS-2]] | Grounded MLLM that perceives and generates bounding boxes as location tokens in natural language |
| 2023 | [[2306.15195\|Shikra]] | Enabled referential dialogue by processing and generating spatial coordinates directly in text output |
| 2024 | [[2407.07726\|PaliGemma]] | Open-source 3B VLM matching larger models across 40 tasks; democratized VLM research |
| 2024 | [[2409.17146\|Molmo]] | Family of open-source MLLMs with state-of-the-art pointing capabilities and transparent training pipeline |
| 2024 | [[2412.04468\|NVILA]] | NVIDIA's efficient MLLM achieving strong performance via visual token compression and structured pruning |
| 2025 | [[2503.15621\|LLaVA-MORE]] | Extended LLaVA with RL-based preference optimization; improved reasoning without sacrificing perception |
| 2025 | [[2504.10479\|InternVL3]] | Native multimodal pre-training with tool-augmented generation; unified understanding and reasoning at scale |
| 2025 | [[2505.14683\|BAGEL]] | Unified multimodal model for interleaved image-text understanding and generation with 7B parameters |
| 2025 | [[2504.10462\|SAIL]] | Search-Augmented Instruction Learning for grounded multimodal reasoning with web knowledge retrieval |
| 2025 | [[2504.05299\|SmolVLM]] | Sub-3B parameter efficient MLLM achieving competitive performance through aggressive architectural optimization |
| 2026 | [[2603.00136\|TinyVLM]] | Ultra-compact MLLM pushing efficiency further with knowledge distillation from larger multimodal models |

---

## 1. Foundational Vision-Language Alignment

The core pretraining paradigms that established how to connect visual encoders with language models — from contrastive alignment to encoder-decoder fusion and multi-modal embedding spaces.

**Contrastive & Dual-Encoder Alignment** — Learning shared image-text embedding spaces through contrastive objectives on large-scale paired data.
- [[2509.01644|OpenVision-2]], [[2507.22062|Meta-CLIP-2]], [[2506.03096|FuseLIP]], [[2505.21549|DCLIP]], [[2505.18983|AmorLIP]], [[2505.04601|OpenVision]], [[2505.03703|Modality-Gap-Reduction]], [[2502.14786|SigLIP-2]], [[2411.04997|LLM2CLIP]], [[2406.17639|AlignCLIP]], [[2212.07143|OpenCLIP]], [[2111.07991|LiT]], [[2103.00020|CLIP]], [[1907.04307|Multilingual USE]]

> [!star] Key Papers
> - [[2103.00020|CLIP]] — Contrastive pre-training on 400M image-text pairs; launched the VLM era and enabled zero-shot transfer via text prompts
> - [[2502.14786|SigLIP-2]] — Multilingual vision-language encoders integrating decoder-based pretraining with sigmoid loss; advances over original SigLIP
> - [[2507.22062|Meta-CLIP-2]] — Transparent, open-sourced methodology for training CLIP on native worldwide web data at scale

**RL, Policy-Optimization & Distillation for Reasoning** — Reinforcement-learning and knowledge-distillation methods for LLM/VLM reasoning; tagged into this alignment bucket during ingest but topically distinct — see [[08_Reinforcement-Learning]].
- [[2605.31159|TRB]], [[2605.29198|GCPO]], [[2605.22817|VPO]], [[2605.22217|Survive-or-Collapse]], [[2605.21699|X-Token]], [[2605.21467|DelTA]], [[2605.16787|RLVR-Unlearnability]], [[2605.12227|dGRPO]], [[2605.10663|Evolving-RL]], [[2605.07396|ROPD]], [[2604.17535|OPSDL]], [[2603.07079|EOPD]], [[2602.20574|GATES]]

**Agentic, Embodied & Self-Play Systems** — Agentic, self-play, and embodied-memory papers misfiled into this alignment bucket during ingest — closer to [[11_Robotics-and-Embodied-AI]] and [[10_Agents-and-Tool-Use]].
- [[2606.03374|eMEM]], [[2606.03047|ModuLoop]], [[2605.30557|SpatialUncertain]], [[2605.28814|BES]], [[2605.27276|SIA]], [[2605.26494|MiniMax-M2]], [[2605.25832|AUTO-ROBOTIST]], [[2605.20025|AutoResearchClaw]], [[2602.16313|MemoryArena]], [[2506.14968|FEAST]], [[2409.18313|Embodied-RAG]], [[2209.07753|Code-as-Policies]]

**Encoder-Decoder & Generative Alignment** — Architectures that unify contrastive and generative objectives for both understanding and generation.
- [[2602.02381|AdaSSL]], [[2507.00833|HumanoidGen]], [[2506.16895|STRUCTURE-Alignment]], [[2505.11815|UniMoCo]], [[2305.05665|ImageBind]], [[2206.07643|FIBER]], [[2205.01917|CoCa]], [[2201.12086|BLIP]]

> [!star] Key Papers
> - [[2201.12086|BLIP]] — Unified understanding and generation with bootstrapped captioning; self-cleans noisy web data
> - [[2205.01917|CoCa]] — Combined contrastive and generative objectives in a single model with decoupled text decoder
> - [[2305.05665|ImageBind]] — Extended alignment to six modalities (image, text, audio, depth, thermal, IMU) via a single embedding space

**CLIP Variants & Compositional Enhancement** — Improving CLIP's compositional understanding, fine-grained alignment, and domain-specific capabilities.
- [[2512.11141|ItemizedCLIP]], [[2508.03102|CCA]], [[2505.20229|CLIP-Attribution-SAE]], [[2505.02278|GCLIP]], [[2504.16801|DeGLA]], [[2406.14830|CLIP-Decoder]]

> [!star] Key Papers
> - [[2505.02278|GCLIP]] — Training-free method enhancing CLIP's compositional understanding through grounding
> - [[2504.16801|DeGLA]] — Decoupled Global-Local Alignment for compositional VLM understanding

> [!success] Three-Layer Alignment Stack
> ==Layer 1: Contrastive pretraining== (CLIP/SigLIP 2) for broad zero-shot transfer → ==Layer 2: Generative alignment== (BLIP/CoCa) for understanding + generation → ==Layer 3: Compositional refinement== (grounding-based and decoupled alignment methods) for fine-grained reasoning. Modern MLLMs inherit all three layers.

> [!tip] The Alignment Stack
> The field converged on a three-layer alignment stack: (1) contrastive pretraining for broad zero-shot transfer (CLIP, SigLIP 2), (2) generative alignment for understanding + generation (BLIP, CoCa), and (3) compositional refinement for fine-grained reasoning (GCLIP, DeGLA). Each layer builds on the previous, and modern MLLMs inherit all three.

---

## 2. Early Multimodal LLMs

The first generation of models that connected visual encoders to large language models, establishing the MLLM paradigm through Q-Former bridges, instruction tuning, and grounded dialogue.

**Pioneering MLLM Architectures** — The initial designs for feeding visual information into frozen or fine-tuned LLMs.
- [[2605.22297|Layerwise-LR]], [[2605.08083|AutoTTS]], [[2605.03677|Uni-OPD]], [[2605.02600|CoRAL]], [[2504.15965|AI-Memory-Survey]], [[2311.05437|LLaVA-Plus]], [[2309.05519|NExT-GPT]], [[2306.15195|Shikra]], [[2306.14824|KOSMOS-2]], [[2305.14676|GRILL]], [[2305.11175|VisionLLM]], [[2305.06500|InstructBLIP]], [[2303.04671|Visual-ChatGPT]], [[2302.14045|KOSMOS-1]], [[2211.09699|PromptCap]], [[2204.00598|Socratic-Models]]

> [!star] Key Papers
> - [[2305.06500|InstructBLIP]] — Instruction-tuned BLIP-2 with Q-Former; established systematic instruction tuning for vision-language models
> - [[2306.14824|KOSMOS-2]] — Grounded MLLM generating bounding boxes alongside text; first model unifying vision-language understanding with spatial grounding
> - [[2306.15195|Shikra]] — Processes spatial coordinates as natural language tokens for referential dialogue without extra modules

**Region-Level & Grounded Understanding** — Early approaches to fine-grained visual understanding at the region or object level within MLLMs.
- [[2310.11441|SoM]], [[2308.00692|LISA]], [[2307.03601|GPT4RoI]], [[2203.17273|FindIt]], [[2104.12763|MDETR]]

> [!star] Key Papers
> - [[2308.00692|LISA]] — Introduced reasoning segmentation, enabling MLLMs to generate precise segmentation masks from complex language queries
> - [[2310.11441|SoM]] — Set-of-Mark visual prompting: overlays alphanumeric markers on images to unlock GPT-4V's fine-grained grounding

> [!tip] The Q-Former Legacy
> InstructBLIP's Q-Former bridge became the dominant early connector between frozen vision encoders and LLMs. While later work moved toward simpler linear projections (LLaVA) and native multimodal training (InternVL3), the principle of a learnable cross-modal bottleneck persists in modern designs.

---

## 3. Instruction-Tuned & Production MLLMs

The maturation of MLLMs through systematic instruction tuning, scaling to production quality, and comparative studies of different LLM backbones and training recipes.

**Foundational LLM Backbones** — Landmark text-only LLM papers that established the architecture and scaling lineage MLLMs build on.
- [[2303.12712|Sparks of AGI]], [[2303.08774|GPT-4]], [[2302.13971|LLaMA]], [[2204.02311|PaLM (Pathways Language Model)]], [[2005.14165|GPT-3]], [[1706.03762|Transformer]]

**Flagship Instruction-Tuned MLLMs** — Full-scale MLLMs trained with instruction-following data across diverse vision-language tasks.
- [[2603.25040|Intern-S1-Pro]], [[2511.00108|Pelican-VL-1.0]], [[2508.11737|Ovis2.5]], [[2508.01558|EvoVLMA]], [[2507.22448|Falcon-H1]], [[2507.12507|Nemotron]], [[2507.06261|Gemini-2.5]], [[2507.02029|RoboBrain-2.0]], [[2507.01006|GLM-4.5V]], [[2506.03569|MiMo-VL]], [[2505.18842|v1]], [[2505.07062|Seed1.5-VL]], [[2505.00949|Llama-Nemotron]], [[2504.13180|PerceptionLM]], [[2504.07491|Kimi-VL]], [[2503.15621|LLaVA-MORE]], [[2502.13130|Magma]], [[2410.08202|Mono-InternVL]], [[2409.17146|Molmo]], [[2408.03326|LLaVA-OneVision]], [[2407.07726|PaliGemma]], [[2311.07575|SPHINX (Multi-modal Weight Mixing)]]

> [!star] Key Papers
> - [[2407.07726|PaliGemma]] — Sub-3B parameter VLM achieving SOTA across 40+ tasks; demonstrated small models can match larger counterparts
> - [[2409.17146|Molmo]] — Family of open-weight VLMs with PixMo dataset; competitive with proprietary models while fully open
> - [[2503.15621|LLaVA-MORE]] — Systematic comparative study of MLLM design choices across LLM backbones and training strategies

**Instruction Data & Training Pipelines** — Methods for creating high-quality multimodal instruction data and optimizing training procedures.
- [[2603.27164|daVinci-LLM]], [[2603.26164|DataFlex]], [[2506.08429|SCALE]], [[2505.19030|RECAST]], [[2505.17316|Patch-Aligned-Training]], [[2505.08971|PRIOR]], [[2504.21850|COMPACT]], [[2504.15619|AdaViP]], [[2412.07012|ProVision]], [[2410.02742|GLIMO]], [[2403.13187|EvoLLM-JP]], [[2306.08543|MiniLLM]], [[2302.00674|FLAD]], [[2105.09938|APPS]]

> [!star] Key Papers
> - [[2412.07012|ProVision]] — Programmatic system for generating diverse vision-language instruction data at scale
> - [[2504.21850|COMPACT]] — Generates compositionally complex visual instruction tuning data for improved MLLM reasoning
> - [[2506.08429|SCALE]] — Automated pipeline curating high-quality multimodal instruction datasets with LLM-based filtering

**Parameter-Efficient Fine-Tuning & Adaptation** — Adapters, LoRA variants, and representation-efficient methods for adapting MLLMs to new domains without full retraining.
- [[2603.12248|EBFT]], [[2603.01097|LoRA-Knowledge-Memory]], [[2602.04118|TinyLoRA]], [[2507.11851|Gated-LoRA]], [[2506.05191|MokA]], [[2505.10088|MMRL++]], [[2505.00315|MoSA]], [[2503.08497|MMRL]], [[2501.13787|PEFT-for-Foundation-Models]], [[2412.01282|Align-KD]], [[2403.14608|PEFT-Comprehensive-Survey]], [[2312.12148|PEFT-Critical-Review]], [[2110.04366|MAM Adapter]], [[2106.09685|LoRA]], [[2104.08691|Prompt Tuning]], [[1902.00751|Adapters]]

**Model Merging** — Combining multiple fine-tuned models into one without full retraining.
- [[2604.07725|Squeeze-Evolve]], [[2601.07645|PlaM]], [[2502.17159|RobustMerge]], [[2408.07666|Model-Merging-in-LLMs/MLLMs]], [[2311.03099|DARE]], [[2306.01708|TIES-Merging]]

> [!star] Key Papers
> - [[2502.17159|RobustMerge]] — Training-free, data-free, storage-free model merging specifically designed for VLMs
> - [[2601.07645|PlaM]] — Training-free model merging preserving complementary knowledge from multiple fine-tuned models

> [!tip] Instruction Tuning is the Key
> The gap between a raw VLM and a usable MLLM is instruction tuning. PaliGemma showed that a well-tuned 3B model beats poorly tuned 13B+ models. The bottleneck has shifted from model size to data quality — SCALE, ProVision, and COMPACT address this directly.

---

## 4. Unified & Native Multimodal Models

A new generation of models trained end-to-end on interleaved multimodal data rather than bolting visual modules onto text-only LLMs, achieving seamless cross-modal understanding and generation.

**Diffusion & Flow-Based Unified Generation** — Native multimodal models whose generation path uses (discrete or continuous) diffusion or flow-matching instead of pure autoregression.
- [[2604.24763|Tuna-2]], [[2603.19227|MoTok]], [[2603.15975|UMO]], [[2507.23278|UniLiP]], [[2506.23044|Ovis-U1]], [[2506.17202|UniFork]], [[2506.15564|Show-o2]], [[2505.19223|LLaDA-1.5]], [[2505.16933|LLaDA-V]], [[2504.20996|X-Fusion]], [[2503.13436|UniFluid]], [[2502.09992|LLaDA]], [[2412.15188|LMFusion]], [[2412.08635|LatentLM]], [[2408.12528|Show-o]], [[2408.11039|Transfusion]]

**Autoregressive & Encoder-Integrated Unified Architectures** — Native multimodal models unifying vision and language via joint autoregressive token modeling or encoder-free/encoder-fused designs.
- [[2605.09131|MCP-Cosmos]], [[2601.03193|UniCorn]], [[2505.14683|BAGEL]], [[2504.17432|UniME]], [[2504.10479|InternVL3]], [[2504.10462|SAIL]], [[2503.20680|VoRA]], [[2501.17811|Janus-Pro]], [[2410.13848|Janus]], [[2410.01345|GemBench]], [[2409.04429|VILA-U]], [[2407.06135|ANOLE]], [[2405.09818|Chameleon]], [[2404.14396|SEED-X]], [[2312.13286|Emu2]]

> [!star] Key Papers
> - [[2504.10479|InternVL3]] — Native multimodal pre-training paradigm jointly acquiring visual and linguistic capabilities; new MLLM SOTA
> - [[2505.14683|BAGEL]] — Open-source unified multimodal foundation model; trained on trillions of interleaved tokens for both understanding and generation
> - [[2503.20680|VoRA]] — Encoder-free MLLM treating visual features as LoRA parameters; eliminates the separate vision encoder entirely

**Multimodal Scaling Laws & Pre-Training** — Understanding how to scale native multimodal models and what training recipes work best.
- [[2603.21191|BST-Scaling-Rule]], [[2603.15958|Hyperparameter-Scaling-Laws]], [[2509.26625|LLM-Visual-Priors]], [[2507.15857|Diffusion-vs-AR]], [[2507.00994|MLM-vs-CLM-Pretraining]], [[2506.03295|CFT]], [[2505.07291|INTELLECT-2]], [[2504.07951|NMM-Scaling-Laws]], [[2503.19903|PS3]], [[2502.03275|Token-Assorted]], [[2412.18619|Multimodal-NTP-Survey]], [[2006.12467|Depth-to-Width Interplay]], [[2001.08361|Neural Scaling Laws]]

> [!star] Key Papers
> - [[2504.07951|NMM-Scaling-Laws]] — First comprehensive study of scaling laws for native multimodal models; shows joint training outperforms modular approaches
> - [[2509.26625|LLM-Visual-Priors]] — Demonstrates that LLM weights carry useful visual priors before any visual training

**Unified Understanding & Generation** — Models bridging the comprehension-generation gap to handle both tasks in a single framework.
- [[2606.05979|WLA]], [[2603.03241|UniG2U-Bench]], [[2602.22766|CapImagine]], [[2602.12279|UniT]], [[2602.12205|DeepGen-1.0]], [[2601.03193|UniCorn]], [[2506.22880|DeSa2VA]], [[2506.13759|Discrete-Diffusion-LLM-Survey]], [[2503.10631|HybridVLA]], [[2403.10191|GenerateU]], [[2305.17216|GILL]]

> [!star] Key Papers
> - [[2601.03193|UniCorn]] — Autonomously bridges comprehension and generation capabilities within a single model
> - [[2506.22880|DeSa2VA]] — Decouples textual and visual generation in MLLMs for improved quality in both

> [!tip] The Native Multimodal Shift
> The field is moving from "LLM + vision encoder" to jointly pre-trained multimodal models. InternVL3 and NMM Scaling Laws demonstrate that native multimodal training outperforms modular assembly. VoRA pushes this further by eliminating the encoder entirely. This trend mirrors how text-only LLMs evolved from pipeline systems to end-to-end models.

---

## 5. Visual Encoding & Feature Integration

How visual information is encoded, projected, and integrated into the language model — from vision encoder design to cross-modal connectors and feature fusion strategies.

**Vision Encoder Design** — Building and improving the visual backbone that feeds MLLMs.
- [[2602.01905|STELLAR]], [[2512.15885|JARVIS]], [[2512.10942|VL-JEPA]], [[2510.21501|GranViT]], [[2507.01643|SAILViT]], [[2507.00754|LUViT]], [[2505.24541|Mixpert]], [[2505.22664|VLM-Surrogate-Grafting]], [[2505.20802|Leaner-Transformers]], [[2505.19985|Structured-ViT-Initialization]], [[2505.15970|DINOv2-Hierarchy-SAE]], [[2504.13181|Perception-Encoder]], [[2411.14402|AIMV2]], [[2311.13601|DINOv]], [[2112.11010|MPViT]], [[2111.12941|WinTR]], [[2107.02239|ViX]], [[2107.00641|Focal-Transformer]], [[2106.08254|BEiT]]

> [!star] Key Papers
> - [[2411.14402|AIMV2]] — Apple's autoregressive + contrastive pre-training for vision encoders; strong zero-shot transfer
> - [[2504.13181|Perception-Encoder]] — Family of vision models achieving SOTA across diverse tasks; designed as universal perception backbone
> - [[2512.10942|VL-JEPA]] — Joint Embedding Predictive Architecture for vision-language; shows latent prediction outperforms reconstruction

**Cross-Modal Connectors & Feature Fusion** — Mechanisms for projecting visual features into the LLM's embedding space.
- [[2603.15619|MoDA]], [[2603.15031|AttnRes]], [[2602.20980|CrystaL]], [[2512.06281|LaVer]], [[2509.07979|VIRAL]], [[2508.12466|Inverse-LLaVA]], [[2506.17629|CLiViS]], [[2506.17608|HIRE]], [[2506.16691|LaVi]], [[2506.10966|GenManip]], [[2506.04220|Struct2D]], [[2506.01850|MoDA]], [[2504.21447|Shallow-ViT-Features]], [[2503.06063|Multi-Layer-Visual-Fusion]], [[2410.13733|Arcana]], [[2410.11829|MMFuser]], [[2403.13043|S2]]

> [!star] Key Papers
> - [[2503.06063|Multi-Layer-Visual-Fusion]] — Systematic analysis showing multi-layer visual features outperform single-layer for MLLMs
> - [[2504.21447|Shallow-ViT-Features]] — Demonstrates shallow ViT layers carry critical information that deep layers discard
> - [[2506.01850|MoDA]] — Modulation Adapter dynamically refining pre-aligned visual features for the LLM

**Position Encoding for Vision** — Adapting positional encodings for visual tokens in multimodal contexts.
- [[2601.15275|RayRoPE]], [[2505.21465|ID-Align]], [[2505.20444|HoPE]], [[2505.16416|Circle-RoPE]], [[2410.06205|p-RoPE]], [[2104.09864|RoPE]]

> [!star] Key Papers
> - [[2505.16416|Circle-RoPE]] — Decoupled rotary position encoding for visual and textual tokens; resolves position conflicts in MLLMs
> - [[2601.15275|RayRoPE]] — Projective ray positional encoding for multi-view transformers using 3D geometric priors

**High-Resolution & Multi-Scale Processing** — Handling high-resolution images without losing fine-grained details.
- [[2511.19820|CropVLM]], [[2506.12776|NativeRes-LLaVA]], [[2506.01663|Zoom-Refine]], [[2502.16025|FeatSharp]], [[2412.13871|LLaVA-UHD-v2]], [[2412.13303|FastVLM]], [[2207.13050|Efficient-High-Resolution-Survey]]

> [!star] Key Papers
> - [[2412.13871|LLaVA-UHD-v2]] — Hierarchical Window Transformer for native high-resolution MLLM input processing
> - [[2502.16025|FeatSharp]] — Generates sharper high-resolution features from low-resolution vision encoders without retraining

> [!tip] The Feature Integration Bottleneck
> How visual features reach the LLM matters as much as the encoder quality. Multi-Layer Visual Fusion and Shallow ViT Features show that using only the final encoder layer loses critical information. Meanwhile, position encoding (Circle-RoPE, HoPE) is emerging as an underappreciated factor in MLLM visual understanding.

---

## 6. Efficient & Compact MLLMs

Reducing MLLM inference cost through token compression, model compression, and compact architectures designed for resource-constrained deployment.

**Visual Token Reduction** — Dynamically pruning or merging visual tokens to reduce the computational burden of processing images.
- [[2603.22815|PinPoint]], [[2506.10967|CDPruner]], [[2506.07138|STF]], [[2506.01097|Explainability-Guided-Token-Compression]], [[2505.22654|VScan]], [[2505.16411|SPIN]], [[2504.17040|DyMU]], [[2504.00557|Trimmed-Llama]], [[2503.16660|Adaptive-Token-Reduction]]

> [!star] Key Papers
> - [[2504.17040|DyMU]] — Training-free framework dynamically reducing visual tokens based on image complexity
> - [[2506.10967|CDPruner]] — Training-free token pruning leveraging content-dependency analysis
> - [[2505.22654|VScan]] — Two-stage framework achieving up to 90% visual token reduction with minimal quality loss

**Compact Model Architectures** — Building small but capable MLLMs under 3B parameters for edge deployment.
- [[2604.27488|Skills-Coach]], [[2604.10929|Ro-SLM]], [[2603.06569|Penguin-VL]], [[2603.00136|TinyVLM]], [[2504.05299|SmolVLM]], [[2504.00595|Open-Qwen2VL]], [[2412.04468|NVILA]], [[2411.09691|TinyGroundingGPT]], [[2408.01800|MiniCPM-V]], [[2401.15947|MoE-LLaVA]]

> [!star] Key Papers
> - [[2504.05299|SmolVLM]] — Family of compact multimodal models (256M-2B) processing images and video; competitive with much larger models
> - [[2603.00136|TinyVLM]] — Zero-shot object detection on microcontrollers; sub-1MB models for edge deployment
> - [[2412.04468|NVILA]] — NVIDIA's efficient MLLM family achieving competitive quality at reduced compute

**Efficient Inference & Acceleration** — Methods for speeding up MLLM inference at deployment time.
- [[2602.11812|EGTP]], [[2512.13607|Nemotron-Cascade]], [[2508.09834|Efficient-LLM-Architectures-Survey]], [[2508.03682|SQLM]], [[2507.06607|Gated-Memory-Unit]], [[2505.22618|Fast-dLLM]], [[2505.10526|MASSV]], [[2412.06464|Gated DeltaNet]], [[2410.19878|PEFT-Methodologies-Survey]], [[2405.21060|Mamba-2]], [[2404.16710|LayerSkip]], [[2312.06635|GLA]], [[2107.02027|packedBERT]], [[2009.06732|Efficient-Transformers-Survey]]

> [!star] Key Papers
> - [[2505.10526|MASSV]] — Speculative decoding framework accelerating VLM inference through multi-head parallel generation

> [!tip] The Efficiency Imperative
> Token reduction is the most impactful lever for MLLM efficiency — VScan and CDPruner achieve 70-90% token reduction with minimal quality loss. For deployment, SmolVLM and TinyVLM show that architecture-level compactness combined with token reduction enables MLLMs on edge devices. The key insight: most visual tokens are redundant for any given query.

---

## 7. Hallucination Mitigation

Addressing the fundamental challenge of MLLMs generating text that contradicts visual evidence — through decoding strategies, contrastive methods, preference optimization, and evaluation frameworks.

**Decoding-Based Methods** — Modifying the generation process to suppress hallucinated content without retraining.
- [[2607.21556|VCSD]], [[2602.16702|SAP]], [[2602.11737|OA-VCD]], [[2512.23453|CoFi-Dec]], [[2509.23236|Self-Reflection-VLM]], [[2509.03113|GACD]], [[2508.11616|MRGD]], [[2507.00898|ONLY]], [[2506.23601|SemDiD]], [[2506.09522|ReVisiT]], [[2506.08391|SECOND]], [[2406.01920|CODE]], [[2210.15097|Contrastive Decoding]]

> [!star] Key Papers
> - [[2406.01920|CODE]] — Training-free decoding method reducing hallucination through contrastive output distributions
> - [[2509.03113|GACD]] — Gradient-based influence-aware constrained decoding; first to use gradient information for hallucination mitigation
> - [[2512.23453|CoFi-Dec]] — Coarse-to-fine decoding leveraging geometric consistency for grounded generation

**Visual Attention & Token Intervention** — Steering the model's visual attention to reduce over-reliance on language priors.
- [[2605.02735|Silenced-Visual-Latents]], [[2605.00814|PVM]], [[2604.15809|AIF]], [[2603.14117|SIEVE]], [[2603.00207|VisRef]], [[2602.24041|AIR]], [[2602.21497|ECRD]], [[2602.08241|SAYO]], [[2602.02004|ClueTracer]], [[2509.12132|Reflection-V]], [[2508.02419|TVAI]], [[2507.22003|ViHallu]], [[2506.12609|VisFlow]], [[2505.17812|VaLSe]], [[2505.05177|MARK]], [[2411.12591|VIC]]

> [!star] Key Papers
> - [[2506.12609|VisFlow]] — Dual-level attention intervention redirecting model focus toward relevant visual tokens
> - [[2508.02419|TVAI]] — Identifies modality bias as a root cause of hallucination; proposes targeted visual attention injection

**Visual Prompting Against Hallucination** — Using visual cues and prompts to anchor model outputs in visual evidence.
- [[2601.00659|CRoPS]], [[2510.16596|SHIELD]], [[2506.16112|AutoV]], [[2506.07227|MED]], [[2504.21559|BBVPE]], [[2503.12799|GCoT]]

> [!star] Key Papers
> - [[2504.21559|BBVPE]] — Black-box visual prompt engineering mitigating hallucination without model access
> - [[2601.00659|CRoPS]] — Dynamic cropping strategy forcing models to attend to relevant image regions

**Preference Optimization & Training-Based** — Aligning MLLM outputs with visual ground truth through preference learning and targeted fine-tuning.
- [[2604.20366|MPD]], [[2604.20328|HyLaR]], [[2602.22859|DPE]], [[2511.15661|VisPlay]], [[2507.16814|SOPHIA]], [[2506.17901|PostAlign]], [[2506.13888|VL-GenRM]], [[2506.10128|ViCrit]], [[2504.15619|AdaViP]]

> [!star] Key Papers
> - [[2504.15619|AdaViP]] — Adaptive visual preference optimization reducing hallucination through contrastive visual grounding
> - [[2506.17901|PostAlign]] — Post-training alignment framework improving visual fidelity without catastrophic forgetting

**Hallucination Analysis & Benchmarks** — Understanding when, why, and how MLLMs hallucinate, including knowledge-grounding as an orthogonal mitigation strategy.
- [[2605.03808|Agentic-imodels]], [[2605.02087|MSM]], [[2604.28182|Exploration-Hacking]], [[2604.15574|FT-Hallucinations]], [[2602.09276|Reasoning-ID]], [[2601.21969|Token-Guard]], [[2601.13304|CausalSpatial]], [[2509.25373|VLM-Perception-Cognition-Survey]], [[2508.01781|LLM-Hallucination-Taxonomy]], [[2507.10442|VLM-Three-Space-Analysis]], [[2505.23224|MMBoundary]], [[2505.12886|LRM-Hallucination]], [[2502.17422|MLLM-Small-Visual-Details]], [[2402.00253|LVLM-Hallucination-Survey]], [[2401.06209|MMVP]], [[2310.00754|LURE]], [[2305.10355|POPE]], [[2005.11401|RAG]], [[1809.02156|CHAIR]]

> [!star] Key Papers
> - [[2402.00253|LVLM-Hallucination-Survey]] — Comprehensive taxonomy of hallucination types in large vision-language models
> - [[2502.17422|MLLM-Small-Visual-Details]] — Reveals fundamental limitations in MLLM perception of small visual details

> [!tip] Defense in Depth
> No single method solves hallucination. The most effective approach combines decoding-time intervention (CODE, GACD) with attention steering (VisFlow, TVAI) and preference alignment (AdaViP). LURE and the LVLM Survey provide the diagnostic framework for understanding which hallucination types affect your specific use case.

---

## 8. Visual Grounding & Spatial Understanding

Enabling MLLMs to localize, reference, and reason about specific objects and regions in images — from bounding box prediction to dense spatial reasoning.

**Grounded MLLMs** — Models that jointly generate text and spatial coordinates for objects.
- [[2511.06908|Mono3DVG-EnSD]], [[2411.09691|TinyGroundingGPT]], [[2410.08021|OneRef]], [[2405.19783|IVM]], [[2405.17104|LLM-Optic]], [[2404.13013|Groma]], [[2401.17981|MLLM-Detection-Infusion]]

> [!star] Key Papers
> - [[2404.13013|Groma]] — Localized visual tokenizer for robust MLLM visual grounding at the region level
> - [[2405.19783|IVM]] — Instruction-guided visual masking that automatically highlights task-relevant image regions

**Visual Prompting for MLLMs** — Methods for communicating spatial information to MLLMs through visual annotations and markers.
- [[2510.09201|MPO]], [[2506.16112|AutoV]], [[2409.15310|Visual-Prompting-MLLM-Survey]], [[2407.01400|GalLoP]], [[2304.06712|Visual-Prompt-Engineering]]

> [!star] Key Papers
> - [[2409.15310|Visual-Prompting-MLLM-Survey]] — Comprehensive survey of visual prompting techniques for MLLMs; taxonomizes the field
> - [[2510.09201|MPO]] — Multimodal Prompt Optimizer jointly optimizing textual and visual prompts

**Dense Perception & Tracking** — Fine-grained visual understanding including tracking, referring, and pixel-level grounding.
- [[2603.03857|DeepScan]], [[2512.22799|VPTracker]], [[2510.23603|PixelRefer]], [[2505.23769|TextRegion]], [[2505.20612|RF100-VL]], [[2309.08912|MP-FGVC]]

> [!star] Key Papers
> - [[2510.23603|PixelRefer]] — Unified framework for fine-grained spatiotemporal object understanding in images and videos
> - [[2512.22799|VPTracker]] — Location-aware visual prompting enabling MLLMs for multi-object tracking

**Spatial Reasoning Benchmarks & Analysis** — Evaluating and diagnosing how well MLLMs handle spatial relationships and scene structure.
- [[2604.18484|XEmbodied]], [[2602.21619|VSR-Information-Injection-Analysis]], [[2602.15950|VLM-Spatial-Reasoning-OCR]], [[2602.15918|EarthSpatialBench]], [[2602.03916|SpatiaLab]], [[2601.22231|PE-Spatial-Reasoning-Analysis]], [[2504.15037|MLLM-Spatial-Reasoning-Position-Paper]], [[2502.11859|VLM-Spatial-Abilities-Benchmark]], [[2406.14852|SpatialEval]], [[2406.02537|TopViewRS]]

**Spatial Grounding & Scene Understanding Methods** — Models and mechanisms for localizing and reasoning about scene structure beyond object detection, including physical-property inference (gravity, mass, materials, dynamics) as a distinct capability from geometric/spatial reasoning.
- [[2602.03361|Z3D]], [[2601.19834|Visual-Generation-Reasoning]], [[2601.05600|SceneAlign]], [[2601.04777|GeM-VG]], [[2511.21688|G2VLM]], [[2507.00505|LLaVA-SP]], [[2506.21710|FOCUS]], [[2506.10778|SlotPi]], [[2506.08708|PhyBlock]], [[2504.13469|HMPE]], [[2501.09038|Physics-IQ]], [[2411.16044|ZoomEye]], [[2410.08500|STMR]], [[2410.06468|SPACE]], [[2312.14135|V*]], [[2307.12981|3D-LLM]]

> [!star] Key Papers
> - [[2601.05600|SceneAlign]] — Aligns MLLMs with scene-level spatial structure for holistic visual understanding
> - [[2602.15950|VLM-Spatial-Reasoning-OCR]] — Reveals consistent spatial reasoning degradation in VLMs on OCR-related tasks
> - [[2501.09038|Physics-IQ]] — Probes whether video foundation models implicitly encode dynamic physical properties (mass, friction); a diagnostic complement to PhyGenBench-style generation tests
> - [[2506.08708|PhyBlock]] — Block-stacking benchmark exposing whether MLLMs reason about gravitational stability from images alone

> [!tip] Grounding as First-Class Capability
> Grounding is no longer an afterthought — KOSMOS-2 and Shikra (Section 2) showed it can be native. The trend is toward models that ground by default (Groma, PixelRefer) rather than requiring external detection modules. For robotics applications, this shift is critical — see [[11_Robotics-and-Embodied-AI]].

---

## 9. Video & Temporal MLLMs

Extending multimodal understanding to video inputs, requiring models to handle temporal dynamics, long-form content, and cross-frame reasoning.

**Video & Temporal MLLM Methods** — Architectures and benchmarks for temporal reasoning, long-context video memory, and cross-frame understanding.
- [[2603.17541|Temporal-Trap-Analysis]], [[2602.20159|VBVR]], [[2602.05986|RISE-Video]], [[2602.01984|Delimiter-Token-Scaling]], [[2601.09430|Video-MSR]], [[2507.01544|MARVIS]], [[2506.06279|CoMemo]], [[2406.07476|VideoLLaMA 2]]

> [!star] Key Papers
> - [[2602.05986|RISE-Video]] — Comprehensive benchmark for evaluating MLLMs on temporal video reasoning
> - [[2602.20159|VBVR]] — Community-curated dataset with over one million video reasoning examples
> - [[2506.06279|CoMemo]] — Dual-path architecture addressing the long-context memory problem in video MLLMs

> [!tip] The Video Frontier
> Video MLLMs remain significantly behind image MLLMs in capability. The core challenge is temporal context — CoMemo and Delimiter Token Scaling address this through specialized memory and multi-frame architectures. RISE-Video and VBVR provide the benchmarks needed to drive progress.

---

## 10. Reasoning & Trustworthiness

Methods for improving MLLM reasoning capabilities and estimating the reliability of model outputs.

**RL-Trained Visual Reasoning** — Reinforcement-learning methods that train MLLMs to reason over visual input.
- [[2605.15198|ATLAS]], [[2602.08346|ThinkWithImages-PRMBENCH]], [[2510.20817|MARA]], [[2510.20607|Compositional-Energy-Minimization]], [[2509.23285|Tool-Light]], [[2506.08011|ViGaL]], [[2506.07218|Perception-R1]], [[2505.24025|DINO-R1]], [[2505.22453|MM-UPT]], [[2505.22334|Multimodal-RL-Cold-Start]], [[2505.20289|VisTA]], [[2505.19590|INTUITOR]], [[2505.19255|VTool-R1]], [[2504.18397|UV-CoT]]

**Visual Reasoning Benchmarks, Probes & Interpretability** — Diagnosing and evaluating what MLLMs actually do when they reason over images.
- [[2603.02556|VC-STaR]], [[2512.08228|MM-CoT]], [[2508.02095|VLM4D]], [[2506.09047|Back-Patching-VLM]], [[2506.08008|VLMs-Overlook-Visual-Representations]], [[2506.04277|RSVP]], [[2505.23764|MMSI-Bench]], [[2505.21538|PAM-CVR]], [[2505.05626|PERCEPTLLM]], [[2501.13620|VLM-Perception-Reasoning-Probe]], [[2410.10855|CoreCognition]]

**Chain-of-Thought & Tool-Augmented Visual Reasoning Methods** — Prompting and tool-use techniques that structure step-by-step visual reasoning without RL training.
- [[2605.11856|UniVLR]], [[2511.15703|VLSR]], [[2510.09312|CRV]], [[2506.11515|Manager]], [[2505.23766|Argus]], [[2505.20753|Griffon-R]], [[2505.20164|VAT]], [[2504.14200|KeCO]], [[2503.16434|Interactive-Sketchpad]], [[2502.07503|RINS]], [[2412.13171|CCoT]], [[2411.10440|LLaVA-CoT]], [[2406.09403|VisualSketchPad]], [[2404.03622|VoT]], [[2302.00923|Multimodal-CoT]]

> [!star] Key Papers
> - [[2502.07503|RINS]] — Recursive Inference Scaling from Google DeepMind; enhances MLLM performance through iterative self-refinement
> - [[2603.02556|VC-STaR]] — Visual Contrastive Self-Taught Reasoner improving VLM reasoning through contrastive self-training

**Safety, Deception & Alignment Auditing** — Detecting and auditing unsafe, deceptive, or misaligned model behavior.
- [[2603.30036|CoT-Monitorability]], [[2602.08145|Reliable-Foundation-Models-Survey]], [[2601.14127|MIR-SafetyBench]], [[2512.15926|DSO]], [[2510.06738|AWM]], [[2510.06096|Alignment-Auditor]], [[2510.01088|Safety-Instincts]], [[2509.22989|Strategic-Persuasion]], [[2509.03518|LLM-Lying]], [[2506.19823|Persona-Misalignment]], [[2506.19807|KnowRL]], [[2502.05206|Safety-at-Scale-Survey]]

**Trustworthiness Calibration & Robustness Benchmarks** — Measuring confidence calibration and robustness of MLLM predictions.
- [[2603.13292|Pragma-VL]], [[2603.03944|SCP-Bench]], [[2602.21054|VAUQ]], [[2602.01816|VIA-Bench]], [[2506.22982|CroPA]], [[2505.23745|TrustVLM]], [[2504.18053|DREAM]], [[2410.21276|GPT-4o]], [[2406.18925|VisArgs]]

> [!star] Key Papers
> - [[2505.23745|TrustVLM]] — Framework estimating prediction trustworthiness by combining internal and external confidence signals
> - [[2602.21054|VAUQ]] — Training-free self-evaluation framework quantifying visual vs. textual reliance in MLLM predictions
> - [[2601.14127|MIR-SafetyBench]] — First benchmark for evaluating safety risks from multi-image reasoning in MLLMs

**Continual & Incremental Learning** — Enabling MLLMs to acquire new knowledge without forgetting prior capabilities.
- [[2602.21628|RuCL]], [[2512.24695|Hope]], [[2512.09441|MoP-CIL]], [[2510.10487|Triangular-Consistency]], [[2508.04227|VLM-Continual-Learning-Survey]], [[2410.19925|MLLM-Continual-Learning]]

**RL-Trained Multimodal Reasoning** — Reinforcement-learning/RFT methods that train LLM reasoning extended to vision/video/spatial inputs.
- [[2604.03128|Self-Distilled-RLVR]], [[2602.04884|RAL]], [[2601.18631|AdaReasoner]], [[2512.12633|DiG]], [[2512.04563|COOPER]], [[2509.24251|LVR]], [[2505.21457|ACTIVE-O3]], [[2505.19702|Point-RFT]], [[2505.19094|SATORI]], [[2504.13055|NoisyRollout]], [[2503.20752|Reason-RFT]], [[2503.16188|Think-or-Not-Think]]

**Multimodal Reasoning: Data, Representation & Efficiency** — Non-RL methods improving multimodal reasoning through data curation, representation design, or inference efficiency.
- [[2606.07500|SETA]], [[2602.02951|NUWA]], [[2512.12822|LEMON]], [[2511.22715|ReAG]], [[2511.19972|Activation-Replay-MM]], [[2511.17487|EXTRACT+THINK]], [[2510.14605|Wiki-PRF]], [[2510.08673|Puffin]], [[2508.15568|ADAPT]], [[2507.10302|DisCo]], [[2506.22819|TCA]], [[2506.05302|PAM]], [[2506.04559|RAPID]], [[2506.04209|LIFT]], [[2506.02138|PA-LRP]], [[2505.16151|FRANK]], [[2505.07956|LLM-LEx]], [[2502.20120|Modality-Boosting]]

**Surveys** — Literature surveys of LLM reasoning and RL.
- [[2603.25681|LLM-Self-Improvement-Survey]], [[2509.08827|RL-for-LRM-Survey]], [[2509.04501|RL-for-Model-Training-Survey]], [[2509.02350|Implicit-Reasoning-Survey]], [[2507.13334|Context-Engineering-Survey]], [[2507.09662|Concise-Adaptive-Thinking-Survey]], [[2507.06203|Latent-Reasoning-Survey]], [[2506.13018|NN-Parameter-Space-Symmetry-Survey]], [[2505.02665|Slow-Thinking-LLM-Survey]], [[2505.00551|DeepSeek-R1-Replication-Survey]], [[2503.16419|Stop-Overthinking-Survey]], [[2503.09567|Long-CoT-Survey]], [[2502.21321|LLM-Post-Training-Survey]], [[2501.09686|Large-Reasoning-Models-Survey]], [[2404.14387|LLM-Self-Evolution-Survey]]

**Interpretability & Empirical Analysis** — Mechanistic and empirical studies of LLM/VLM reasoning and RL training dynamics.
- [[2605.10889|OPD-Diagnostic]], [[2510.26493|Context-Engineering-2.0]], [[2510.08985|Document-Ranking-CoT-Study]], [[2510.00034|MOWI]], [[2509.24156|Reasoning-vs-Retrieval]], [[2509.21128|RL-Squeezes-SFT-Expands]], [[2509.18376|GnnXemplar]], [[2509.03646|HICRA]], [[2509.00421|Prompt-Tuning-Memory-Limits]], [[2508.16546|SFT-vs-RL-Spectral-Analysis]], [[2507.16003|ICL-Implicit-Dynamics]], [[2507.02199|Huginn-Latent-CoT]], [[2506.09501|LLM-Inference-Nondeterminism]], [[2506.04374|SLDS-LLM-Reasoning]], [[2506.02126|Knowledge-vs-Reasoning-LLM-Eval]], [[2505.10559|Neural-Thermodynamic-Laws]], [[2504.20966|Softpick]], [[2502.14010|ICL-Attention-Heads]], [[2501.11223|RLM-Blueprint]], [[2412.05265|RL-Overview]], [[2311.12022|GPQA]], [[2201.02373|Mirror-Learning]]

**Long & Efficient CoT** — Long-chain and token-efficient reasoning.
- [[2606.18967|EfficientRollout]], [[2604.08706|RL-Experience-Replay-for-LLMs]], [[2603.28204|ERPO]], [[2510.02752|Self-Aware-RL-for-LLMs]], [[2510.01135|PCL]], [[2509.25849|Knapsack-GRPO]], [[2509.01321|DEPO]], [[2508.17445|TreePO]], [[2508.09726|GFPO]], [[2507.10524|MoR]], [[2506.08552|Latent-Reasoning-Refinement]], [[2506.05316|DOTS]], [[2506.01939|High-Entropy-Token-RLVR]], [[2505.24034|LlamaRL]], [[2505.02222|Muon]], [[2504.01296|ThinkPrune]], [[2503.10460|Light-R1]], [[2503.04697|L1]], [[2502.21074|CODI]]

**Test-Time Scaling & Search** — Test-time compute, search, and sampling.
- [[2603.24422|OneSearch-V2]], [[2601.22628|TTCS]], [[2601.18067|EvolVE]], [[2511.17473|MR-RLVR]], [[2510.14901|Power-Sampling]], [[2510.08964|DisTANCE]], [[2508.14313|AIRL-S]], [[2506.09026|e3]], [[2506.08388|RLTs]], [[2505.24872|ProxyThinker]], [[2503.07572|MRT]], [[2503.04412|AB-MCTS]], [[2502.05171|Huginn]], [[2501.19393|s1]], [[2501.05366|Search-o1]], [[2501.01478|MCTS-Process-Supervision]], [[2501.00663|Titans]], [[2408.03314|Test-Time Compute Scaling]], [[2305.10601|Tree of Thoughts]]

**Flagship Reasoning Models & Provers** — Named reasoning/theorem-proving models and their training recipes.
- [[2512.10938|Derf]], [[2512.03442|PretrainZero]], [[2510.25741|Ouro]], [[2504.21801|DeepSeek-Prover-V2]], [[2504.21318|Phi-4-reasoning]], [[2504.21233|Phi-4-Mini-Reasoning]], [[2504.11354|Kimina-Prover]], [[2502.07640|Goedel-Prover]], [[2502.06772|ReasonFlux]], [[2502.05234|TURN]], [[2502.03387|LIMO]], [[2501.12948|DeepSeek-R1]], [[2501.12599|Kimi k1.5]], [[2412.09413|STILL-2]], [[2411.14405|Marco-o1]]

**GRPO & Policy-Optimization Variants for CoT** — Group-relative and policy-optimization algorithm variants applied to chain-of-thought training.
- [[2603.19835|FIPO]], [[2510.15242|DWRL]], [[2510.10603|EA4LLM]], [[2510.08191|Training-Free-GRPO]], [[2510.02245|ExGRPO]], [[2506.15050|T-PPO]], [[2506.08007|RPT]], [[2503.20783|Dr.-GRPO]], [[2503.18866|BoLT]], [[2503.14476|DAPO]], [[2503.03746|Process-based-Self-Rewarding]]

**CoT Training Efficiency & Systems** — Systems- and efficiency-focused work for training and running CoT models at scale.
- [[2512.01374|MiniRL]], [[2511.16652|EGGROLL]], [[2510.26788|FP16-RL-Training]], [[2510.23925|LaCoT]], [[2510.23596|BR-RM]], [[2510.05069|SwiReasoning]], [[2508.15260|DeepConf]], [[2508.02124|DMA]], [[2507.18074|ASI-ARCH]], [[2507.07101|Small-Batch-LLM-Training]], [[2507.00417|ASTRO]]

**CoT Prompting, Latent Reasoning & Data Curation** — Prompting strategies, latent/implicit reasoning representations, and training-data curation for chain-of-thought.
- [[2601.21725|Procedural-Pretraining]], [[2506.23061|DyME]], [[2506.07751|AbstRaL]], [[2506.06105|T2L]], [[2505.24726|Reflect-Retry-Reward]], [[2505.23725|MuLoCo]], [[2505.12514|COCONUT]], [[2505.00147|AdaptMI]], [[2412.06769|Coconut]], [[2412.00420|TAROT]], [[2405.14838|Stepwise-Internalization]], [[2403.09629|Quiet-STaR]], [[2311.12424|Looped-Transformers]], [[2311.01460|Implicit CoT]], [[2305.04091|Plan-and-Solve]], [[2211.01910|APE]], [[2210.03493|Auto-CoT]], [[2205.10625|Least-to-Most]], [[2201.11903|Chain-of-Thought Prompting]], [[2109.00110|miniF2F]]

**On-Policy Distillation (OPD) Family** — On-policy knowledge-distillation variants for LLM reasoning.
- [[2607.15161|OPD^2]], [[2607.05804|TurnOPD]], [[2607.05394|Direct-OPD]], [[2607.05339|TREK]], [[2607.05184|Fork Suppression]], [[2607.04763|ReOPD]], [[2607.04751|TOP-D]], [[2606.30626|DOPD]], [[2605.12483|Teacher-First-OPD]], [[2605.11609|AntiSD]], [[2605.07465|SEIF]], [[2604.13016|OPD-Distillation-Study]], [[2604.13010|Lightning-OPD]]

**Self-Training & Continual Improvement (STaR Lineage)** — Self-generated-data bootstrapping and continual reasoning improvement without a fixed teacher.
- [[2604.02288|SRPO]], [[2604.01193|SSD-Code-Generation]], [[2602.23413|EvoX]], [[2511.01191|Self-Harmony]], [[2510.21223|FDA]], [[2510.02263|RLAD]], [[2509.26626|RSA]], [[2509.15194|EVOL-RL]], [[2509.14234|CaT]], [[2508.16204|M2N2]], [[2507.17634|WSM]], [[2506.15710|RAST]], [[2506.10943|SEAL]], [[2506.08989|SwS]], [[2502.08922|SCIR]], [[2412.01951|Sharpening-Mechanism]], [[2312.06585|ReST-EM]], [[2203.14465|STaR]]

**GRPO & Group-Relative Methods** — GRPO and group-relative policy optimization variants.
- [[2602.05547|MT-GRPO]], [[2507.21848|EDGE-GRPO]], [[2506.08440|TGRPO]], [[2505.22257|Off-Policy-GRPO]], [[2402.03300|DeepSeekMath]]

**Reward Model & Verifier Design** — Constructing and training reward models and verifiers for RL and alignment.
- [[2607.05391|LLM-as-a-Verifier]], [[2605.12474|Rubric-RL-Diagnostic]], [[2605.10899|RubricEM]], [[2510.08696|LENS]], [[2510.07242|HERO]], [[2509.26074|LENS]], [[2509.22638|FCP]], [[2508.14460|DuPO]], [[2507.17746|RaR]], [[2507.16806|RLCR]], [[2506.23235|EndoRM]], [[2506.03637|RewardAnything]], [[2505.21493|VeriFree]], [[2505.19000|VerIPO]], [[2407.13399|χPO]], [[2405.16436|RPO]], [[2405.14734|SimPO]], [[2401.10020|Self-Rewarding-LM]], [[2305.20050|Process Supervision]], [[2204.05862|HH-RLHF]], [[2203.02155|InstructGPT]]

**RLVR Training Dynamics & Reward Benchmarks** — Empirical study of reward signals and RLVR training behavior, plus benchmark suites.
- [[2604.11297|MEDS]], [[2603.18886|RLLM]], [[2511.07317|RLVE]], [[2511.01758|RLAC]], [[2510.03222|Lp-Reg]], [[2509.11452|Multi-Objective-RL-Alignment]], [[2508.05629|DFT]], [[2507.08068|QRPO]], [[2506.18254|RLPR]], [[2506.10947|Spurious-Rewards-RLVR]], [[2505.24760|REASONING-GYM]], [[2505.23585|OPO]], [[2503.13551|HRM]], [[2412.09544|POWER-DL]], [[2306.05685|MT-Bench]], [[2110.14168|GSM8K]]

**Exploration, Stability & Training Dynamics** — Entropy, exploration, collapse, and RL training dynamics.
- [[2607.10169|RIPO]], [[2509.02534|Darling]], [[2508.13755|DARS-Breadth]], [[2505.22617|Entropy-Collapse-in-RL]], [[2505.20561|BARL]], [[2505.15660|AGNOSTOS]], [[2503.23631|Intrinsic-Motivation-Human-Agent-Study]]

**Search & Tool-Integrated RL** — RL and prompting methods that interleave search or external tool calls into the reasoning trajectory.
- [[2510.03259|MASA]], [[2509.09284|Tree-OPO]], [[2509.06870|AggLM]], [[2507.19849|ARPO]], [[2507.16815|ThinkAct]], [[2505.04588|ZeroSearch]], [[2503.23383|ToRL]], [[2503.19470|ReSearch]], [[2503.09516|Search-R1]], [[2503.05592|R1-Searcher]], [[2401.08190|MARIO]], [[2310.04406|LATS]], [[2305.14992|RAP]], [[2303.08128|ViperGPT]], [[2211.12588|PoT]], [[2211.11559|VISPROG]], [[2211.10435|PAL]], [[2210.03629|ReAct]]

**GRPO-Lineage & Group-Relative Variants** — Group-relative policy-optimization algorithm variants descending from GRPO.
- [[2607.16850|GECPO]], [[2601.19280|GDRO]], [[2509.02333|DCPO]], [[2508.02298|CAPO]], [[2507.20673|GMPO]], [[2506.13923|Guide-GRPO]], [[2505.20686|A*-PO]], [[2505.20258|ARM]], [[2505.18454|HRPO]], [[2505.17508|RPG]], [[2504.19599|GVPO]], [[2503.19612|AGRO]], [[2503.12811|MPL]]

**PPO-Lineage & Other Policy-Gradient Variants** — Non-group-relative policy-gradient algorithm variants for LLM/VLM RL.
- [[2607.19331|ISO]], [[2607.18722|Staleness-Adaptive Trust Region]], [[2607.07508|SAO]], [[2605.28421|DenoiseRL]], [[2605.06139|LPO]], [[2604.08865|SPPO]], [[2603.10160|ReMix]], [[2602.10675|TwiFF]], [[2602.05842|RWML]], [[2602.04879|DPPO]], [[2602.03806|COBALT]], [[2602.02710|MaxRL]], [[2602.01058|PEAR]], [[2510.18927|BAPO]], [[2510.09001|DARO]], [[2510.01265|RLP]], [[2508.08221|Lite-PPO]], [[2507.18391|IBRO]], [[2507.01679|Prefix-RFT]], [[2506.21495|Offline-Online-RL-for-LLMs]], [[2505.24864|ProRL]]

**Self-Play, Self-Correction & Zero-Supervision RL** — RL methods that bootstrap from self-generated data or self-play without external supervision.
- [[2607.12395|Ring-Zero]], [[2604.09258|Nexus]], [[2512.02389|Synthetic-Error-Self-Correct]], [[2508.05004|R-Zero]], [[2508.02150|Self-Supervised-RL-IF]], [[2507.23751|CoT-Self-Instruct]], [[2506.10139|ICM]], [[2505.22954|DGM]], [[2505.21444|SRT]], [[2505.17746|Fast-Quiet-STaR]], [[2505.03335|Absolute-Zero]], [[2503.24290|Open-Reasoner-Zero]]

**RLVR Training Dynamics & Theory** — Empirical and theoretical study of what happens during RL-with-verifiable-reward training.
- [[2604.03993|Noisy-Supervision-Reasoning]], [[2603.23355|ReVal]], [[2603.22117|RLVR-Direction]], [[2603.02188|MLRA]], [[2602.00170|Blessing-of-Dimensionality-LLM]], [[2510.08189|R-Horizon]], [[2509.22637|Variational-Reasoning]], [[2509.04259|RL's-Razor]], [[2507.10532|RandomCalculation]], [[2507.06187|Delta-Learning-Hypothesis]], [[2507.00432|Math-Reasoning-Transferability]], [[2506.09477|KL-Divergence-Gradient-Pitfalls]], [[2505.02406|TCPA]], [[2504.20571|1-shot-RLVR]], [[2501.17161|SFT-Memorizes-RL-Generalizes]], [[2309.14322|Transformer-Training-Instabilities]], [[2309.05858|Mesa-Optimization-Transformers]]

**RL Training Efficiency & Systems** — Systems-level and optimizer-level work for scaling RL training.
- [[2607.01232|Single-Layer RL Training]], [[2510.25992|SRL]], [[2509.24372|Evolution-Strategies-at-Scale]], [[2509.07980|Parallel-R1]], [[2508.17784|PSFT]], [[2508.10874|SSRL]], [[2507.08838|wd1]], [[2503.10622|DyT]], [[2502.16982|Muon]]

**Reasoning-Domain RL Extensions & Applications** — RLVR applied to specific reasoning domains and downstream applications.
- [[2512.24601|RLMs]], [[2512.14693|URM]], [[2512.02472|R-FEW]], [[2509.20357|RLMT]], [[2509.14760|ALIGN3]], [[2509.14252|LLM-JEPA]], [[2509.06806|MachineLearningLM]], [[2508.12790|Rubicon]], [[2506.15211|ProtoReasoning]], [[2504.20595|ReasonIR]], [[2504.19254|uqlm]], [[2503.16219|Open-RS]], [[2411.14251|NLRL]], [[2309.15129|CogEval]]

**Agent Memory & Skill-Library Evolution** — Agents that accumulate and reuse skills or memories across episodes.
- [[2607.23784|ARCHITECT]], [[2607.22529|Skill-SP]], [[2606.08671|SkillHone]], [[2605.06614|SkillOS]], [[2603.18743|Memento-Skills]], [[2603.12056|XSkill]], [[2511.00758|ATM]], [[2509.25140|ReasoningBank]], [[2509.15172|MACA]], [[2509.07414|LSP]], [[2508.19005|ELL-Framework]], [[2406.04151|AgentGym]], [[2305.16291|Voyager]]

**Curriculum & Experience-Driven Agent Evolution** — Agents that evolve through structured curricula or accumulated environment experience.
- [[2607.23515|LEACL]], [[2607.21461|AREX]], [[2605.15188|FutureSim]], [[2605.09387|NEXUS]], [[2604.01658|CORAL]], [[2603.16856|OEL]], [[2601.06794|ECHO]], [[2510.24684|SPICE]], [[2510.23595|MAE]], [[2510.15047|SPA]], [[2510.08558|Early-Experience]], [[2510.04618|ACE]], [[2506.01716|SCA]], [[2504.21024|WebEvolver]], [[2409.00872|SAGE]]

**Self-Play & Adversarial Agent Evolution** — Agents that self-improve through self-play, self-generated curricula, or adversarial red-teaming.
- [[2606.29082|EFT]], [[2603.17621|Complementary-RL]], [[2602.00359|A-EVOLVE]], [[2510.16079|EVOLVER]], [[2509.24726|Socratic-Zero]], [[2509.19349|ShinkaEvolve]], [[2507.14172|SOAR]], [[2506.24119|SPIRAL]], [[2506.07468|SELF-REDTEAM]], [[2506.06499|SPARQ]]

**Self-Evolving Agent Surveys & Benchmarks** — Survey and benchmark work framing the self-evolving-agent landscape.
- [[2607.13104|Self-Improving Agents Survey]], [[2607.05155|EdgeBench]], [[2508.07407|Self-Evolving-AI-Agents-Survey]], [[2507.21046|Self-Evolving-Agents-Survey]]

**Agentic RL Training Methods** — RL and RL-adjacent training methods for tool-use and multi-turn agentic reasoning.
- [[2607.21653|Molt]], [[2604.03098|Self-Guide]], [[2603.30022|Hybrid-LLM-RL-Manipulation]], [[2603.24639|ERL]], [[2603.21383|PivotRL]], [[2602.06130|SWIRL]], [[2510.23038|TIR-Judge]], [[2510.01132|Multi-turn-Agentic-RL-Guide]], [[2509.02479|SimpleTIR]], [[2509.01055|VerlTool]], [[2508.20722|rStar2-Agent]], [[2508.07976|ASearcher]], [[2508.03680|Agent-Lightning]], [[2507.22844|RLVMR]], [[2507.19457|GEPA]], [[2507.05707|Agentic-R1]], [[2506.13131|AlphaEvolve]], [[2506.09033|Router-R1]], [[2506.06122|ROLL]], [[2505.04588|ZeroSearch]]

**Agent Memory, Skill & Multi-Agent Frameworks** — Architectures for agent memory, skill acquisition, and multi-agent coordination.
- [[2607.15079|BrainPilot]], [[2607.04439|IdeaSpark]], [[2606.29538|Resource2Skill]], [[2604.02268|SKILL0]], [[2604.01687|EvoSkills]], [[2603.29620|Unify-Agent]], [[2603.29557|FlowPIE]], [[2603.29493|MemFactory]], [[2603.25111|SEVerA]], [[2603.05218|KARL]], [[2601.19204|MATA]], [[2511.20639|LatentMAS]], [[2511.16043|Agent0]], [[2511.10395|AgentEvolver]], [[2508.13167|CoA]], [[2508.03923|CoAct-1]], [[2508.02085|SE-Agent]], [[2507.23773|SimuRA]], [[2507.01701|LbMAS]]

**Tool-Use Applications & Benchmarks** — Domain-specific agent/tool-use applications and evaluation suites, including secure code generation as a specialized benchmark track.
- [[2607.24051|HELIOS]], [[2607.17250|EvolvingWorld]], [[2603.20278|OpenResearcher]], [[2603.00142|ToM-Multi-Agent-Eval]], [[2511.02824|Kosmos-AI-Scientist]], [[2509.13351|PDDL-INSTRUCT]], [[2507.20534|Kimi-K2]], [[2506.02153|SLMs-for-Agentic-AI]], [[2503.19263|DWIM]], [[2412.18072|MMFactory]], [[2412.13810|CAD-Assistant]], [[2411.17673|SketchAgent]], [[2410.11096|SeCodePLT]], [[2410.08328|Talker-Reasoner]], [[2405.00218|CODEGUARD+]], [[2403.13257|MergeKit]], [[2402.09497|SafeCoder]], [[2310.12823|AgentLM]], [[2307.13854|WebArena]]

**Agentic Surveys & Landscape** — Survey work mapping the agentic-AI and agentic-RL research landscape.
- [[2512.13564|AI-Agent-Memory-Survey]], [[2511.18538|Code-Intelligence-Survey]], [[2509.02547|Agentic-RL-Landscape-Survey]], [[2508.17692|Agentic-Reasoning-Framework-Survey]], [[2507.23276|AI-Scientist-Survey]]

**VLA Models & World-Models** — Vision-language-action models and world-model architectures for embodied control.
- [[2607.23899|Embodied GPT-5.1]], [[2510.13054|VLA-0]], [[2506.21539|WorldVLA]], [[2503.22020|CoT-VLA]], [[2503.18769|AlphaSpace]], [[2406.09246|OpenVLA]], [[2403.06845|DriveDreamer-2]], [[2312.06571|Alter3]], [[2311.01378|RoboFlamingo]], [[2307.15818|RT-2]], [[2307.00329|DoReMi]], [[2210.15629|LCD]], [[2204.01691|SayCan]]

**Robot Planning, Navigation & HRI Systems** — Cross-domain planning, navigation, teleoperation, and human-robot interaction foundations.
- [[2607.24190|Kim Episodic Memory]], [[2607.24113|Kim]], [[2607.13072|HRO]], [[2607.12630|MTEFR]], [[2607.12050|EFLUX]], [[2607.10437|Inter-POMDP]], [[2607.07430|VR-LLM Humanoid Teleoperation]], [[2607.06990|Closed-Loop Multi-Robot Manipulation Framework]], [[2607.06724|EvoPlan]], [[2607.01044|CommNav]], [[2606.31260|SymPlan]], [[2606.29774|ACM]], [[2606.29460|LLM Intervention Explanations in HRI]], [[2604.20348|BiCICLe]], [[2604.02911|DreamTIP]], [[2511.14565|Masked-IRL]]

**Embodied AI & VLA Surveys** — Survey and position papers framing the embodied-AI/VLA research landscape.
- [[2509.20021|Embodied-AI-LLM-WM-Survey]], [[2505.04769|VLA-Concepts-Survey]], [[2409.10106|Industry 6.0]], [[2405.14093|VLA-for-Embodied-AI-Survey]]

**RL & Foundations for Agents** — RL and foundational methods underpinning agents.
- [[2604.00626|On-Policy-Distillation-Survey]], [[2603.00461|ReMoT]], [[2602.00795|DVLA-RL]], [[2509.25810|RA3]], [[2509.25454|DeepSearch]], [[2509.25133|SIREN]], [[2509.24981|ROVER]], [[2506.03147|UniWorld-V1]], [[2503.09527|CombatVLA]], [[2502.04692|STRIDE]], [[2412.14164|MetaMorph]], [[2412.03548|AURORA]], [[2410.16400|VipAct]], [[2410.02355|AlphaEdit]], [[2406.03303|Learned-Visual-Prompts-for-ViT]]

> [!star] Key Papers
> - [[2410.19925|MLLM-Continual-Learning]] — Systematic quantification of linguistic forgetting in continually trained MLLMs
> - [[2508.04227|VLM-Continual-Learning-Survey]] — Comprehensive taxonomy of continual learning challenges specific to VLMs

> [!tip] Beyond Accuracy
> MLLM deployment requires more than benchmark scores. TrustVLM and VAUQ address confidence calibration, MIR-SafetyBench covers safety under multi-image inputs, and continual learning (MoP-CIL) ensures models do not degrade as they are updated. These are prerequisites for real-world deployment.

---

## 11. Interpretability & Mechanistic Analysis

Understanding what MLLMs learn internally — which visual features matter, how cross-modal representations are structured, and why models produce specific outputs.

**Mechanistic Analysis & Circuit-Level Tools** — General mechanistic-interpretability primitives (circuits, sparse features, task representations) applied to transformers.
- [[2604.11791|Looped-Reasoning-Mechanistic-Analysis]], [[2603.17063|Transformers-as-Bayesian-Networks]], [[2506.15679|Dense-SAE-Latents]], [[2501.09333|Prompt-CAM]], [[2310.15916|Task Vectors]], [[2310.15213|Function Vectors]], [[2309.08600|Sparse Autoencoders]], [[2209.11895|Induction Heads]]

**Visual Representation & Cross-Modal Probing** — Tools and analyses specific to probing what MLLMs encode visually and cross-modally.
- [[2607.03973|MANCE]], [[2603.07335|VisualScratchpad]], [[2602.15029|Language-Symmetry-Representations]], [[2602.11217|Magic-Correlations]], [[2602.11144|GENIUS]], [[2602.02140|GAPEVAL]], [[2602.00462|LatentLens]], [[2510.02292|VLM-Lens]], [[2506.11976|VLM-Visual-Language-Alignment]], [[2506.07326|Reward-Model-Interpretability]], [[2504.19627|VCM]], [[2502.02013|Layer-by-Layer-Representations]]

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
- [[2507.23070|E-FineR]], [[2507.10203|ARL]], [[2507.10202|ECP]], [[2505.20046|REARANK]], [[2505.16149|REVEAL]], [[2505.11192|FALCON]], [[2505.02056|VLM-Pseudo-label-Calibration]], [[2505.01064|NeaR]], [[2311.04157|INTR]]

> [!star] Key Papers
> - [[2505.01064|NeaR]] — Vocabulary-free fine-grained visual recognition combining MLLM-generated descriptions with retrieval
> - [[2507.23070|E-FineR]] — Fully automated, training-free fine-grained recognition without predefined vocabularies

**Retrieval & Composition** — Methods for image-text retrieval and composed image retrieval using VLMs.
- [[2604.12148|ViLL-E]], [[2603.02959|SS-Text-U]], [[2509.01092|REFRAG]], [[2508.04987|UniMoS++]], [[2506.23115|MoCa]], [[2505.19707|MVFT-JI]], [[2503.23508|Real-LOD]], [[2501.05452|ReFocus]]

> [!star] Key Papers
> - [[2505.19707|MVFT-JI]] — Zero-shot composed image retrieval through direct VLM fine-tuning
> - [[2506.23115|MoCa]] — Transforms causal VLMs into bidirectional encoders for robust retrieval

**Creative & Domain-Specific Applications** — MLLMs applied to creative, simulation, and unconventional domain tasks.
- [[2607.15314|Cura 1T]], [[2607.08374|JAM]], [[2606.31209|RosettaSim]], [[2606.31131|Crash-to-Scenario LLM Pipeline]], [[2604.13074|PersonaVLM]], [[2512.24880|mHC]], [[2511.11007|VisMem]], [[2505.21497|PosterAgent]], [[2505.11820|CoLM]], [[2505.01812|New-News]], [[2312.04684|LaRS]], [[2301.05226|IPVR]], [[2210.02506|GameBugDescriptions]]

**Evaluation, Testing & Deployment Applications** — Evaluating and stress-testing MLLM applications for real-world deployment.
- [[2601.12585|MLLM-Visualization-Literacy]], [[2601.00561|AEGIS]], [[2511.20836|DSPy+HELM]], [[2511.20814|SPHINX]], [[2509.24207|Humanline]], [[2508.13142|EASI]], [[2507.01955|GPT-4o-Vision-Evaluation]], [[2506.22395|Test-Time-VLM-Consistency]], [[2505.24189|SLM-vs-LLM-Low-Code-Workflows]], [[2403.19103|PRISM]], [[2310.10625|VLP]], [[2305.00104|MMViT]]

> [!star] Key Papers
> - [[2505.21497|PosterAgent]] — Automated academic poster generation from papers; demonstrates creative MLLM applications
> - [[2601.12585|MLLM-Visualization-Literacy]] — First taxonomy of visualization literacy barriers in MLLMs
> - [[2604.13074|PersonaVLM]] — Long-term personalized MLLM with dynamic memory architecture; 79% win rate vs. GPT-4o on open-ended personalized generation

> [!tip] MLLMs as General Visual Assistants
> The fine-grained recognition results (NeaR, E-FineR) show that MLLMs can replace specialized classifiers when paired with the right prompting strategy. For retrieval, MoCa's trick of converting causal models to bidirectional encoders unlocks capabilities that the original training never intended.

---

## 13. Open-Vocabulary Detection with MLLMs

Extending MLLM capabilities to open-vocabulary object detection — detecting objects described by arbitrary text at inference time.

**Open-Vocabulary Detection with MLLMs** — Steering or pretraining MLLMs/VLMs to detect objects described by arbitrary text.
- [[2505.23004|QLIP]], [[2502.17425|VPT]], [[2501.18954|LLMDet]], [[2410.13842|D-FINE]], [[2404.09216|DetCLIPv3]], [[2304.04514|DetCLIPv2]], [[2209.15639|F-VLM]], [[2209.09407|DetCLIP]]

> [!star] Key Papers
> - [[2304.04514|DetCLIPv2]] — End-to-end pre-training for open-vocabulary detection learning directly from large-scale image-text data
> - [[2209.15639|F-VLM]] — Open-vocabulary detection using frozen VLMs with minimal training overhead
> - [[2502.17425|VPT]] — Visual Perception Tokens enabling MLLMs to dynamically attend to detection-relevant regions

> [!tip] Detection Without Boundaries
> Open-vocabulary detection removes the fixed-class bottleneck. DetCLIPv2 and F-VLM show that CLIP-style alignment can drive detection, while VPT demonstrates that MLLMs can be steered toward detection tasks through learned perception tokens. See [[05_Vision-Language-Models]] for the broader open-vocabulary detection landscape.

---

## 14. Surveys & Meta-Analyses

Comprehensive overviews and large-scale analyses of the MLLM field.

**MLLM Surveys & Meta-Analyses** — Field-wide reviews spanning MLLM architectures, efficiency, prompting, and predecessor visual-transformer surveys.
- [[2604.02029|Latent-Space-Survey]], [[2603.22862|LLM-Tool-Use-Survey]], [[2510.09586|VLM-Survey-26K]], [[2508.02120|Efficient-R1-style-Reasoning-Survey]], [[2501.09223|LLM-Foundations]], [[2501.02765|VLLM-Survey]], [[2501.02189|VLM-SOTA-Survey]], [[2405.10739|Efficient-MLLM-Survey]], [[2402.07927|Prompt-Engineering-Survey]], [[2306.13549|MLLM-Survey]], [[2303.18223|LLM Survey]], [[2111.06091|Visual-Transformers-Survey]], [[2012.12556|Visual-Transformer-Survey]]

> [!star] Key Papers
> - [[2306.13549|MLLM-Survey]] — First comprehensive synthesis of the MLLM field covering architectures, training, and evaluation
> - [[2405.10739|Efficient-MLLM-Survey]] — Categorizes efficiency techniques across the full MLLM pipeline
> - [[2510.09586|VLM-Survey-26K]] — Quantitative meta-analysis of 26,104 papers from top-tier AI conferences; maps the VLM research landscape

> [!tip] Navigating the Literature
> With 26K+ VLM papers across three years of top conferences, surveys are essential navigation aids. Start with the MLLM Survey (2023) for foundations, then the VLM Survey 2025 for recent advances, and the Efficient MLLM Survey for deployment-oriented work.


---

## Cross-References

- [[01_Foundation-Models]] — Backbone architectures (ViT, DINO, CLIP)
- [[05_Vision-Language-Models]] — Vision-language alignment, prompt learning, open-vocabulary detection
- [[07_Reasoning-and-Planning]] — Reasoning capabilities built on MLLMs
- [[02_Computer-Vision-and-3D]] — 3D and spatial understanding
- [[11_Robotics-and-Embodied-AI]] — MLLMs as perception backbone for VLAs
- [[03_Diffusion-and-Generation]] — Generation models that complement MLLM understanding

---

*Next: [[07_Reasoning-and-Planning]] for how these multimodal models learn to reason step-by-step.*
