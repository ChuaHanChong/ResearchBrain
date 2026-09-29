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
1. Alignment Objective   (how image meets text)
· objective design
                   +bootstrapped      +both objectives    softmax → sigmoid
                   captions           at once             loss
╔═════════════╗    ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
║ CLIP (2021) ║───►│ BLIP (2022) │───►│ CoCa (2022)  │───►│ SigLIP-2 (2025) │
╚══════┬══════╝    └─────────────┘    └──────────────┘    └─────────────────┘
       │    2 modalities → 6
       │    ┌──────────────────┐
       ├───►│ ImageBind (2023) │
       │    └──────────────────┘
       │    +worldwide data
       │    curation
       │    ┌────────────────────┐
       └───►│ Meta-CLIP-2 (2025) │
            └────────────────────┘

2. Early Grounded MLLMs   (say where, not just what)
· coordinates as output
                       +referential         boxes → pixel
                       dialogue             masks
┌─────────────────┐    ┌───────────────┐    ┌─────────────┐
│ KOSMOS-2 (2023) │───►│ Shikra (2023) │───►│ LISA (2023) │
└────────┬────────┘    └───────────────┘    └─────────────┘
         │    +instruction-aware
         │    features
         │    ┌─────────────────────┐
         ├───►│ InstructBLIP (2023) │
         │    └─────────────────────┘
         │    +set-of-mark
         │    prompting
         │    ┌────────────┐
         └───►│ SoM (2023) │
              └────────────┘

3. Instruction-Tuned Production   (make it usable)
· supervision to preference
                        +open data,         +preference              +production-scale
                        pointing            optimization             recipe
┌──────────────────┐    ┌──────────────┐    ┌───────────────────┐    ┌───────────────┐
│ PaliGemma (2024) │───►│ Molmo (2024) │───►│ LLaVA-MORE (2025) │───►│ PlaM (2026)   │
└──────────────────┘    └──────────────┘    └───────────────────┘    └───────────────┘

4. Native Multimodal   (one model, not an encoder bolted on)
· unified pretraining
                                            encoder →          +unified corpus
                        +MoT interleaved    vision-as-LoRA     scaling
┌──────────────────┐    ┌──────────────┐    ┌─────────────┐    ┌────────────────┐
│ InternVL3 (2025) │───►│ BAGEL (2025) │───►│ VoRA (2025) │───►│ UniCorn (2026) │
└──────────────────┘    └──────────────┘    └─────────────┘    └────────────────┘

5. Visual Encoding   (what the LLM actually receives)
· feature quality
                    +high-res hierarchical     +contrastive-free encoder        +feature upsampling
┌──────────────┐    ┌─────────────────────┐    ┌───────────────────────────┐    ┌──────────────────┐
│ AIMV2 (2024) │───►│ LLaVA-UHD-v2 (2024) │───►│ Perception-Encoder (2025) │───►│ FeatSharp (2025) │
└───────┬──────┘    └─────────────────────┘    └───────────────────────────┘    └──────────────────┘
        │    +cross-modal position
        │    ┌────────────────────┐
        ├───►│ Circle-RoPE (2025) │
        │    └────────────────────┘
        │    +ray-based 3D
        │    position
        │    ┌────────────────┐
        └───►│ RayRoPE (2026) │
             └────────────────┘

6. Efficiency   (shrink it without losing it)
· parameter budget
                                          +knowledge
                    +sub-3B               distillation
┌──────────────┐    ┌────────────────┐    ┌────────────────┐
│ NVILA (2024) │───►│ SmolVLM (2025) │───►│ TinyVLM (2026) │
└───────┬──────┘    └────────────────┘    └────────────────┘
        │    smaller model →
        │    fewer tokens
        │    ┌──────────────┐
        ├───►│ VScan (2025) │
        │    └──────────────┘
        │    +conditional-diversity
        │    pruning
        │    ┌────────────────────┐
        └───►│ CDPruner (2025)    │
             └────────────────────┘

7. Hallucination Mitigation   (stop it inventing what it sees)
· name it, then patch it
                                        +contrastive                               +cross-modal
                                        decoding           +post-hoc alignment     consistency
┌──────────────────────────────────┐    ┌─────────────┐    ┌──────────────────┐    ┌──────────────┐
│ LVLM-Hallucination-Survey (2024) │───►│ CODE (2024) │───►│ PostAlign (2025) │───►│ CRoPS (2026) │
└──────────────────────────────────┘    └──────┬──────┘    └──────────────────┘    └──────────────┘
                                               │    +adaptive visual
                                               │    preference
                                               │    ┌───────────────┐
                                               └───►│ AdaViP (2025) │
                                                    └───────────────┘

8. Trustworthiness and Continual Use   (what happens after deployment)
· keep it reliable over time
                                                                                           +uncertainty
                                      +trust estimation      +safety benchmark             quantification
┌────────────────────────────────┐    ┌─────────────────┐    ┌────────────────────────┐    ┌─────────────┐
│ MLLM-Continual-Learning (2024) │───►│ TrustVLM (2025) │───►│ MIR-SafetyBench (2026) │───►│ VAUQ (2026) │
└────────────────────────────────┘    └─────────────────┘    └────────────────────────┘    └─────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

The eight lanes divide on **which property of the MLLM is being pushed**. **Alignment objective** settles how image meets text, CLIP contrastive, BLIP bootstrapping captions, CoCa carrying both losses, SigLIP-2 swapping softmax for sigmoid, with ImageBind and Meta-CLIP-2 branching to more modalities and worldwide curation. **Early grounded MLLMs** make the model say where, KOSMOS-2 to Shikra to LISA as output moves from boxes to masks, with InstructBLIP and SoM branching to instruction-aware features and set-of-mark prompting. **Instruction-tuned production** makes it usable, PaliGemma to Molmo to LLaVA-MORE to PlaM as the signal moves from supervision to preference. **Native multimodal** stops bolting an encoder on, InternVL3 to BAGEL to VoRA to UniCorn. **Visual encoding** attacks what the language model actually receives, AIMV2 to LLaVA-UHD-v2 to Perception-Encoder to FeatSharp, with Circle-RoPE and RayRoPE branching on how position is encoded across modalities. **Efficiency** shrinks it, NVILA to SmolVLM to TinyVLM, while VScan and CDPruner branch to cutting tokens rather than parameters. **Hallucination mitigation** starts from the survey that named the failure, CODE decoding against it, PostAlign patching after the fact, CRoPS enforcing cross-modal consistency, with AdaViP branching to adaptive visual preference. **Trustworthiness and continual use** covers what happens after deployment, MLLM-Continual-Learning to TrustVLM to MIR-SafetyBench to VAUQ.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2021 | [[2103.00020\|CLIP]] | Alignment · Objective Design | Contrastive pretraining on 400M image-text pairs; enabled zero-shot visual recognition via natural language |
| 2022 | [[2201.12086\|BLIP]] | Alignment · Objective Design | Unified vision-language understanding and generation with bootstrapped caption filtering for noisy web data |
| 2022 | [[2205.01917\|CoCa]] | Alignment · Objective Design | Combined contrastive and generative objectives in a single model with decoupled text decoder |
| 2023 | [[2305.05665\|ImageBind]] | Alignment · Objective Design | Extended alignment to six modalities (image, text, audio, depth, thermal, IMU) via a single embedding space |
| 2023 | [[2305.06500\|InstructBLIP]] | Grounding · Coordinates as Output | Applied instruction tuning to VLMs with instruction-aware visual features; SOTA zero-shot on unseen tasks |
| 2023 | [[2306.14824\|KOSMOS-2]] | Grounding · Coordinates as Output | Grounded MLLM that perceives and generates bounding boxes as location tokens in natural language |
| 2023 | [[2306.15195\|Shikra]] | Grounding · Coordinates as Output | Enabled referential dialogue by processing and generating spatial coordinates directly in text output |
| 2023 | [[2308.00692\|LISA]] | Grounding · Coordinates as Output | Introduced reasoning segmentation, enabling MLLMs to generate precise segmentation masks from complex language queries |
| 2023 | [[2310.11441\|SoM]] | Grounding · Coordinates as Output | Set-of-Mark visual prompting: overlays alphanumeric markers on images to unlock GPT-4V's fine-grained grounding |
| 2024 | [[2402.00253\|LVLM-Hallucination-Survey]] | Hallucination · Name it then Patch it | Comprehensive taxonomy of hallucination types in large vision-language models |
| 2024 | [[2406.01920\|CODE]] | Hallucination · Name it then Patch it | Training-free decoding method reducing hallucination through contrastive output distributions |
| 2024 | [[2407.07726\|PaliGemma]] | Instruction · Supervision to Preference | Open-source 3B VLM matching larger models across 40 tasks; democratized VLM research |
| 2024 | [[2409.17146\|Molmo]] | Instruction · Supervision to Preference | Family of open-source MLLMs with state-of-the-art pointing capabilities and transparent training pipeline |
| 2024 | [[2410.19925\|MLLM-Continual-Learning]] | Trust · Reliable over Time | Systematic quantification of linguistic forgetting in continually trained MLLMs |
| 2024 | [[2411.14402\|AIMV2]] | Visual Encoding · Feature Quality | Apple's autoregressive + contrastive pre-training for vision encoders; strong zero-shot transfer |
| 2024 | [[2412.04468\|NVILA]] | Efficiency · Parameter Budget | NVIDIA's efficient MLLM achieving strong performance via visual token compression and structured pruning |
| 2024 | [[2412.13871\|LLaVA-UHD-v2]] | Visual Encoding · Feature Quality | Hierarchical Window Transformer for native high-resolution MLLM input processing |
| 2025 | [[2502.14786\|SigLIP-2]] | Alignment · Objective Design | Multilingual vision-language encoders integrating decoder-based pretraining with sigmoid loss; advances over original SigLIP |
| 2025 | [[2502.16025\|FeatSharp]] | Visual Encoding · Feature Quality | Generates sharper high-resolution features from low-resolution vision encoders without retraining |
| 2025 | [[2503.15621\|LLaVA-MORE]] | Instruction · Supervision to Preference | Extended LLaVA with RL-based preference optimization; improved reasoning without sacrificing perception |
| 2025 | [[2503.20680\|VoRA]] | Native · Unified Pretraining | Encoder-free MLLM treating visual features as LoRA parameters; eliminates the separate vision encoder entirely |
| 2025 | [[2504.05299\|SmolVLM]] | Efficiency · Parameter Budget | Sub-3B parameter efficient MLLM achieving competitive performance through aggressive architectural optimization |
| 2025 | [[2504.10479\|InternVL3]] | Native · Unified Pretraining | Native multimodal pre-training with tool-augmented generation; unified understanding and reasoning at scale |
| 2025 | [[2504.13181\|Perception-Encoder]] | Visual Encoding · Feature Quality | Family of vision models achieving SOTA across diverse tasks; designed as universal perception backbone |
| 2025 | [[2504.15619\|AdaViP]] | Hallucination · Name it then Patch it | Adaptive visual preference optimization reducing hallucination through contrastive visual grounding |
| 2025 | [[2505.14683\|BAGEL]] | Native · Unified Pretraining | Unified multimodal model for interleaved image-text understanding and generation with 7B parameters |
| 2025 | [[2505.16416\|Circle-RoPE]] | Visual Encoding · Feature Quality | Decoupled rotary position encoding for visual and textual tokens; resolves position conflicts in MLLMs |
| 2025 | [[2505.22654\|VScan]] | Efficiency · Parameter Budget | Two-stage framework achieving up to 90% visual token reduction with minimal quality loss |
| 2025 | [[2505.23745\|TrustVLM]] | Trust · Reliable over Time | Framework estimating prediction trustworthiness by combining internal and external confidence signals |
| 2025 | [[2506.10967\|CDPruner]] | Efficiency · Parameter Budget | Training-free token pruning leveraging content-dependency analysis |
| 2025 | [[2506.17901\|PostAlign]] | Hallucination · Name it then Patch it | Post-training alignment framework improving visual fidelity without catastrophic forgetting |
| 2025 | [[2507.22062\|Meta-CLIP-2]] | Alignment · Objective Design | Transparent, open-sourced methodology for training CLIP on native worldwide web data at scale |
| 2026 | [[2601.00659\|CRoPS]] | Hallucination · Name it then Patch it | Dynamic cropping strategy forcing models to attend to relevant image regions |
| 2026 | [[2601.03193\|UniCorn]] | Native · Unified Pretraining | Autonomously bridges comprehension and generation capabilities within a single model |
| 2026 | [[2601.07645\|PlaM]] | Instruction · Supervision to Preference | Training-free model merging preserving complementary knowledge from multiple fine-tuned models |
| 2026 | [[2601.14127\|MIR-SafetyBench]] | Trust · Reliable over Time | First benchmark for evaluating safety risks from multi-image reasoning in MLLMs |
| 2026 | [[2601.15275\|RayRoPE]] | Visual Encoding · Feature Quality | Projective ray positional encoding for multi-view transformers using 3D geometric priors |
| 2026 | [[2602.21054\|VAUQ]] | Trust · Reliable over Time | Training-free self-evaluation framework quantifying visual vs. textual reliance in MLLM predictions |
| 2026 | [[2603.00136\|TinyVLM]] | Efficiency · Parameter Budget | Ultra-compact MLLM pushing efficiency further with knowledge distillation from larger multimodal models |

---

## 1. Foundational Vision-Language Alignment

The core pretraining paradigms that established how to connect visual encoders with language models — from contrastive alignment to encoder-decoder fusion and multi-modal embedding spaces.

**Contrastive & Dual-Encoder Alignment** — Learning shared image-text embedding spaces through contrastive objectives on large-scale paired data.
- [[2509.01644|OpenVision-2]], [[2507.22062|Meta-CLIP-2]] (NeurIPS'25 Spotlight), [[2506.16895|STRUCTURE-Alignment]] (NeurIPS'25), [[2506.03096|FuseLIP]], [[2505.21549|DCLIP]], [[2505.18983|AmorLIP]] (NeurIPS'25), [[2505.11815|UniMoCo]], [[2505.04601|OpenVision]] (ICCV'25), [[2505.03703|Modality-Gap-Reduction]], [[2502.14786|SigLIP-2]], [[2411.04997|LLM2CLIP]], [[2406.17639|AlignCLIP]] (ICLR'25), [[2212.07143|OpenCLIP]] (CVPR'23), [[2111.07991|LiT]] (CVPR'22), [[2103.00020|CLIP]] (ICML'21 Oral), [[1907.04307|Multilingual USE]]

> [!star] Key Papers
> - [[2103.00020|CLIP]] (ICML'21 Oral) — Contrastive pre-training on 400M image-text pairs; launched the VLM era and enabled zero-shot transfer via text prompts
> - [[2502.14786|SigLIP-2]] — Multilingual vision-language encoders integrating decoder-based pretraining with sigmoid loss; advances over original SigLIP
> - [[2507.22062|Meta-CLIP-2]] (NeurIPS'25 Spotlight) — Transparent, open-sourced methodology for training CLIP on native worldwide web data at scale

**Encoder-Decoder & Generative Alignment** — Architectures that unify contrastive and generative objectives for both understanding and generation.
- [[2305.05665|ImageBind]] (CVPR'23), [[2206.07643|FIBER]] (NeurIPS'22), [[2205.01917|CoCa]], [[2201.12086|BLIP]] (ICML'22 Spotlight)

> [!star] Key Papers
> - [[2201.12086|BLIP]] (ICML'22 Spotlight) — Unified understanding and generation with bootstrapped captioning; self-cleans noisy web data
> - [[2205.01917|CoCa]] — Combined contrastive and generative objectives in a single model with decoupled text decoder
> - [[2305.05665|ImageBind]] (CVPR'23) — Extended alignment to six modalities (image, text, audio, depth, thermal, IMU) via a single embedding space

**CLIP Variants & Compositional Enhancement** — Improving CLIP's compositional understanding, fine-grained alignment, and domain-specific capabilities.
- [[2512.11141|ItemizedCLIP]], [[2508.03102|CCA]] (ICCV'25), [[2505.20229|CLIP-Attribution-SAE]], [[2505.02278|GCLIP]] (CVPR'25 Workshop), [[2504.16801|DeGLA]], [[2406.14830|CLIP-Decoder]]

> [!star] Key Papers
> - [[2505.02278|GCLIP]] (CVPR'25 Workshop) — Training-free method enhancing CLIP's compositional understanding through grounding
> - [[2504.16801|DeGLA]] — Decoupled Global-Local Alignment for compositional VLM understanding

> [!success] Three-Layer Alignment Stack
> ==Layer 1: Contrastive pretraining== (CLIP/SigLIP 2) for broad zero-shot transfer → ==Layer 2: Generative alignment== (BLIP/CoCa) for understanding + generation → ==Layer 3: Compositional refinement== (grounding-based and decoupled alignment methods) for fine-grained reasoning. Modern MLLMs inherit all three layers.

> [!tip] The Alignment Stack
> The field converged on a three-layer alignment stack: (1) contrastive pretraining for broad zero-shot transfer (CLIP, SigLIP 2), (2) generative alignment for understanding + generation (BLIP, CoCa), and (3) compositional refinement for fine-grained reasoning (GCLIP, DeGLA). Each layer builds on the previous, and modern MLLMs inherit all three.

---

## 2. Early Multimodal LLMs

The first generation of models that connected visual encoders to large language models, establishing the MLLM paradigm through Q-Former bridges, instruction tuning, and grounded dialogue.

**Pioneering MLLM Architectures** — The initial designs for feeding visual information into frozen or fine-tuned LLMs.
- [[2311.05437|LLaVA-Plus]] (ECCV'24), [[2309.05519|NExT-GPT]] (ICML'24 Oral), [[2306.15195|Shikra]], [[2306.14824|KOSMOS-2]] (ICLR'24), [[2305.14676|GRILL]], [[2305.11175|VisionLLM]] (NeurIPS'23), [[2305.06500|InstructBLIP]] (NeurIPS'23), [[2303.04671|Visual-ChatGPT]], [[2302.14045|KOSMOS-1]] (NeurIPS'23), [[2211.09699|PromptCap]] (ICCV'23), [[2204.00598|Socratic-Models]] (ICLR'23 Oral)

> [!star] Key Papers
> - [[2305.06500|InstructBLIP]] (NeurIPS'23) — Instruction-tuned BLIP-2 with Q-Former; established systematic instruction tuning for vision-language models
> - [[2306.14824|KOSMOS-2]] (ICLR'24) — Grounded MLLM generating bounding boxes alongside text; first model unifying vision-language understanding with spatial grounding
> - [[2306.15195|Shikra]] — Processes spatial coordinates as natural language tokens for referential dialogue without extra modules

**Region-Level & Grounded Understanding** — Early approaches to fine-grained visual understanding at the region or object level within MLLMs.
- [[2310.11441|SoM]], [[2308.00692|LISA]] (CVPR'24 Oral), [[2307.03601|GPT4RoI]] (ECCV'24 Workshop), [[2203.17273|FindIt]] (ECCV'22), [[2104.12763|MDETR]]

> [!star] Key Papers
> - [[2308.00692|LISA]] (CVPR'24 Oral) — Introduced reasoning segmentation, enabling MLLMs to generate precise segmentation masks from complex language queries
> - [[2310.11441|SoM]] — Set-of-Mark visual prompting: overlays alphanumeric markers on images to unlock GPT-4V's fine-grained grounding

> [!tip] The Q-Former Legacy
> InstructBLIP's Q-Former bridge became the dominant early connector between frozen vision encoders and LLMs. While later work moved toward simpler linear projections (LLaVA) and native multimodal training (InternVL3), the principle of a learnable cross-modal bottleneck persists in modern designs.

---

## 3. Instruction-Tuned & Production MLLMs

The maturation of MLLMs through systematic instruction tuning, scaling to production quality, and comparative studies of different LLM backbones and training recipes.

**Foundational LLM Backbones** — Landmark text-only LLM papers that established the architecture and scaling lineage MLLMs build on.
- [[2303.12712|Sparks of AGI]], [[2303.08774|GPT-4]], [[2302.13971|LLaMA]], [[2204.02311|PaLM (Pathways Language Model)]], [[2005.14165|GPT-3]] (NeurIPS'20 Oral), [[1706.03762|Transformer]]

**Flagship Instruction-Tuned MLLMs** — Full-scale MLLMs trained with instruction-following data across diverse vision-language tasks.
- [[2603.25040|Intern-S1-Pro]], [[2511.00108|Pelican-VL-1.0]], [[2508.11737|Ovis2.5]], [[2508.01558|EvoVLMA]], [[2507.22448|Falcon-H1]], [[2507.12507|Nemotron]], [[2507.06261|Gemini-2.5]], [[2507.02029|RoboBrain-2.0]], [[2507.01006|GLM-4.5V]], [[2506.03569|MiMo-VL]], [[2505.18842|v1]], [[2505.07062|Seed1.5-VL]], [[2505.00949|Llama-Nemotron]], [[2504.13180|PerceptionLM]] (NeurIPS'25 Spotlight), [[2504.07491|Kimi-VL]], [[2503.15621|LLaVA-MORE]], [[2502.13130|Magma]] (CVPR'25), [[2410.21276|GPT-4o]], [[2410.08202|Mono-InternVL]] (CVPR'25), [[2409.17146|Molmo]] (CVPR'25 Oral), [[2408.03326|LLaVA-OneVision]], [[2407.07726|PaliGemma]], [[2311.07575|SPHINX (Multi-modal Weight Mixing)]]

> [!star] Key Papers
> - [[2407.07726|PaliGemma]] — Sub-3B parameter VLM achieving SOTA across 40+ tasks; demonstrated small models can match larger counterparts
> - [[2409.17146|Molmo]] (CVPR'25 Oral) — Family of open-weight VLMs with PixMo dataset; competitive with proprietary models while fully open
> - [[2503.15621|LLaVA-MORE]] — Systematic comparative study of MLLM design choices across LLM backbones and training strategies

**Instruction Data & Training Pipelines** — Methods for creating high-quality multimodal instruction data and optimizing training procedures.
- [[2603.26164|DataFlex]], [[2602.10388|FAC Synthesis]], [[2506.08429|SCALE]], [[2505.19030|RECAST]] (ICLR'26), [[2505.17316|Patch-Aligned-Training]] (NeurIPS'25), [[2505.08971|PRIOR]], [[2504.21850|COMPACT]], [[2412.07012|ProVision]], [[2410.02742|GLIMO]], [[2302.00674|FLAD]] (NeurIPS'23)

> [!star] Key Papers
> - [[2412.07012|ProVision]] — Programmatic system for generating diverse vision-language instruction data at scale
> - [[2504.21850|COMPACT]] — Generates compositionally complex visual instruction tuning data for improved MLLM reasoning
> - [[2506.08429|SCALE]] — Automated pipeline curating high-quality multimodal instruction datasets with LLM-based filtering

**Parameter-Efficient Fine-Tuning & Adaptation** — Adapters, LoRA variants, and representation-efficient methods for adapting MLLMs to new domains without full retraining.
- [[2603.12248|EBFT]], [[2603.01097|LoRA-Knowledge-Memory]] (ICML'26), [[2602.04118|TinyLoRA]], [[2507.11851|Gated-LoRA]], [[2506.05191|MokA]] (NeurIPS'25 Oral), [[2505.10088|MMRL++]], [[2505.00315|MoSA]], [[2503.08497|MMRL]] (CVPR'25), [[2501.13787|PEFT-for-Foundation-Models]], [[2412.01282|Align-KD]] (CVPR'25), [[2410.19878|PEFT-Methodologies-Survey]], [[2403.14608|PEFT-Comprehensive-Survey]], [[2312.12148|PEFT-Critical-Review]], [[2310.20587|LaMo]] (ICLR'24), [[2110.04366|MAM Adapter]] (ICLR'22 Spotlight), [[2106.09685|LoRA]] (ICLR'22), [[2104.08691|Prompt Tuning]], [[1902.00751|Adapters]] (ICML'19)

**Model Merging** — Combining multiple fine-tuned models into one without full retraining.
- [[2604.07725|Squeeze-Evolve]], [[2601.07645|PlaM]], [[2502.17159|RobustMerge]] (NeurIPS'25 Spotlight), [[2408.07666|Model-Merging-in-LLMs/MLLMs]], [[2403.13187|EvoLLM-JP]], [[2311.03099|DARE]] (ICML'24), [[2306.01708|TIES-Merging]] (NeurIPS'23)

> [!star] Key Papers
> - [[2502.17159|RobustMerge]] (NeurIPS'25 Spotlight) — Training-free, data-free, storage-free model merging specifically designed for VLMs
> - [[2601.07645|PlaM]] — Training-free model merging preserving complementary knowledge from multiple fine-tuned models

> [!tip] Instruction Tuning is the Key
> The gap between a raw VLM and a usable MLLM is instruction tuning. PaliGemma showed that a well-tuned 3B model beats poorly tuned 13B+ models. The bottleneck has shifted from model size to data quality — SCALE, ProVision, and COMPACT address this directly.

---

## 4. Unified & Native Multimodal Models

A new generation of models trained end-to-end on interleaved multimodal data rather than bolting visual modules onto text-only LLMs, achieving seamless cross-modal understanding and generation.

**Diffusion & Flow-Based Unified Generation** — Native multimodal models whose generation path uses (discrete or continuous) diffusion or flow-matching instead of pure autoregression.
- [[2609.08282|GGF]], [[2604.24763|Tuna-2]], [[2603.19227|MoTok]], [[2603.15975|UMO]], [[2507.23278|UniLiP]] (ICLR'26), [[2506.23044|Ovis-U1]], [[2506.17202|UniFork]], [[2506.15564|Show-o2]] (NeurIPS'25), [[2505.19223|LLaDA-1.5]], [[2505.16933|LLaDA-V]], [[2504.20996|X-Fusion]] (ICCV'25), [[2503.13436|UniFluid]], [[2502.09992|LLaDA]] (NeurIPS'25 Oral), [[2412.15188|LMFusion]] (NeurIPS'25), [[2412.08635|LatentLM]], [[2408.12528|Show-o]] (ICLR'25), [[2408.11039|Transfusion]] (ICLR'25 Oral)

**Autoregressive & Encoder-Integrated Unified Architectures** — Native multimodal models unifying vision and language via joint autoregressive token modeling or encoder-free/encoder-fused designs.
- [[2505.14683|BAGEL]], [[2504.17432|UniME]], [[2504.10479|InternVL3]], [[2504.10462|SAIL]] (ICCV'25 Highlight), [[2503.20680|VoRA]], [[2501.17811|Janus-Pro]], [[2410.13848|Janus]] (CVPR'25), [[2410.01345|GemBench]], [[2409.04429|VILA-U]] (ICLR'25), [[2407.06135|ANOLE]], [[2405.09818|Chameleon]], [[2404.14396|SEED-X]], [[2312.13286|Emu2]] (CVPR'24)

> [!star] Key Papers
> - [[2504.10479|InternVL3]] — Native multimodal pre-training paradigm jointly acquiring visual and linguistic capabilities; new MLLM SOTA
> - [[2505.14683|BAGEL]] — Open-source unified multimodal foundation model; trained on trillions of interleaved tokens for both understanding and generation
> - [[2503.20680|VoRA]] — Encoder-free MLLM treating visual features as LoRA parameters; eliminates the separate vision encoder entirely

**Multimodal Scaling Laws & Pre-Training** — Understanding how to scale native multimodal models and what training recipes work best.
- [[2608.11859|Small-Scale Scaling Laws]], [[2608.05000|PhysMMPT]], [[2607.09657|VP]], [[2509.26625|LLM-Visual-Priors]] (ICLR'26 Oral), [[2507.15857|Diffusion-vs-AR]] (NeurIPS'25), [[2507.00994|MLM-vs-CLM-Pretraining]] (ICLR'26), [[2506.03295|CFT]], [[2504.07951|NMM-Scaling-Laws]] (ICCV'25 Oral), [[2503.19903|PS3]] (CVPR'25), [[2412.18619|Multimodal-NTP-Survey]]

> [!star] Key Papers
> - [[2504.07951|NMM-Scaling-Laws]] (ICCV'25 Oral) — First comprehensive study of scaling laws for native multimodal models; shows joint training outperforms modular approaches
> - [[2509.26625|LLM-Visual-Priors]] (ICLR'26 Oral) — Demonstrates that LLM weights carry useful visual priors before any visual training

**Unified Model Benchmarks, Agents & Decoupled Generation** — Benchmarks, agents, and decoupled or self-improving designs that bridge comprehension and generation in one framework.
- [[2603.29620|Unify-Agent]], [[2603.03241|UniG2U-Bench]], [[2602.22766|CapImagine]] (ICML'26), [[2602.12279|UniT]] (CVPR'26), [[2602.12205|DeepGen-1.0]], [[2601.03193|UniCorn]], [[2506.22880|DeSa2VA]], [[2506.13759|Discrete-Diffusion-LLM-Survey]], [[2506.03147|UniWorld-V1]], [[2412.14164|MetaMorph]] (ICCV'25), [[2403.10191|GenerateU]] (CVPR'24), [[2305.17216|GILL]] (NeurIPS'23)

> [!star] Key Papers
> - [[2601.03193|UniCorn]] — Autonomously bridges comprehension and generation capabilities within a single model
> - [[2506.22880|DeSa2VA]] — Decouples textual and visual generation in MLLMs for improved quality in both

> [!tip] The Native Multimodal Shift
> The field is moving from "LLM + vision encoder" to jointly pre-trained multimodal models. InternVL3 and NMM Scaling Laws demonstrate that native multimodal training outperforms modular assembly. VoRA pushes this further by eliminating the encoder entirely. This trend mirrors how text-only LLMs evolved from pipeline systems to end-to-end models.

---

## 5. Visual Encoding & Feature Integration

How visual information is encoded, projected, and integrated into the language model — from vision encoder design to cross-modal connectors and feature fusion strategies.

**Vision Encoder Design** — Building and improving the visual backbone that feeds MLLMs.
- [[2602.01905|STELLAR]], [[2512.15885|JARVIS]], [[2512.10942|VL-JEPA]] (ICLR'26), [[2510.21501|GranViT]], [[2507.01643|SAILViT]], [[2507.00754|LUViT]], [[2505.24541|Mixpert]], [[2505.22664|VLM-Surrogate-Grafting]] (ICCV'25), [[2505.20802|Leaner-Transformers]], [[2505.19985|Structured-ViT-Initialization]] (NeurIPS'25), [[2505.15970|DINOv2-Hierarchy-SAE]] (CVPR'25 Workshop), [[2504.13181|Perception-Encoder]] (NeurIPS'25 Oral), [[2411.14402|AIMV2]] (CVPR'25), [[2406.03303|Learned-Visual-Prompts-for-ViT]] (CVPR'24 Workshop), [[2311.13601|DINOv]] (CVPR'24), [[2112.11010|MPViT]], [[2111.12941|WinTR]], [[2107.02239|ViX]], [[2107.00641|Focal-Transformer]], [[2106.08254|BEiT]] (ICLR'22 Oral)

> [!star] Key Papers
> - [[2411.14402|AIMV2]] (CVPR'25) — Apple's autoregressive + contrastive pre-training for vision encoders; strong zero-shot transfer
> - [[2504.13181|Perception-Encoder]] (NeurIPS'25 Oral) — Family of vision models achieving SOTA across diverse tasks; designed as universal perception backbone
> - [[2512.10942|VL-JEPA]] (ICLR'26) — Joint Embedding Predictive Architecture for vision-language; shows latent prediction outperforms reconstruction

**Cross-Modal Connectors & Feature Fusion** — Mechanisms for projecting visual features into the LLM's embedding space.
- [[2602.20980|CrystaL]], [[2512.06281|LaVer]], [[2509.07979|VIRAL]], [[2508.12466|Inverse-LLaVA]], [[2506.17629|CLiViS]], [[2506.17608|HIRE]] (CVPR'25 Workshop), [[2506.16691|LaVi]], [[2506.04220|Struct2D]] (NeurIPS'25), [[2506.01850|MoDA]] (ICML'26), [[2504.21447|Shallow-ViT-Features]], [[2503.06063|Multi-Layer-Visual-Fusion]] (CVPR'25), [[2410.13733|Arcana]], [[2410.11829|MMFuser]], [[2403.13043|S2]] (ECCV'24)

> [!star] Key Papers
> - [[2503.06063|Multi-Layer-Visual-Fusion]] (CVPR'25) — Systematic analysis showing multi-layer visual features outperform single-layer for MLLMs
> - [[2504.21447|Shallow-ViT-Features]] — Demonstrates shallow ViT layers carry critical information that deep layers discard
> - [[2506.01850|MoDA]] (ICML'26) — Modulation Adapter dynamically refining pre-aligned visual features for the LLM

**Position Encoding for Vision** — Adapting positional encodings for visual tokens in multimodal contexts.
- [[2601.15380|GOAT]], [[2601.15275|RayRoPE]], [[2505.21465|ID-Align]], [[2505.20444|HoPE]] (NeurIPS'25), [[2505.16416|Circle-RoPE]] (ICML'26), [[2410.06205|p-RoPE]] (ICLR'25), [[2104.09864|RoPE]]

> [!star] Key Papers
> - [[2505.16416|Circle-RoPE]] (ICML'26) — Decoupled rotary position encoding for visual and textual tokens; resolves position conflicts in MLLMs
> - [[2601.15275|RayRoPE]] — Projective ray positional encoding for multi-view transformers using 3D geometric priors

**High-Resolution & Multi-Scale Processing** — Handling high-resolution images without losing fine-grained details.
- [[2511.19820|CropVLM]] (CVPR'26 Workshop), [[2506.12776|NativeRes-LLaVA]], [[2506.01663|Zoom-Refine]], [[2502.16025|FeatSharp]] (ICML'25), [[2412.13871|LLaVA-UHD-v2]], [[2412.13303|FastVLM]] (CVPR'25), [[2207.13050|Efficient-High-Resolution-Survey]]

> [!star] Key Papers
> - [[2412.13871|LLaVA-UHD-v2]] — Hierarchical Window Transformer for native high-resolution MLLM input processing
> - [[2502.16025|FeatSharp]] (ICML'25) — Generates sharper high-resolution features from low-resolution vision encoders without retraining

> [!tip] The Feature Integration Bottleneck
> How visual features reach the LLM matters as much as the encoder quality. Multi-Layer Visual Fusion and Shallow ViT Features show that using only the final encoder layer loses critical information. Meanwhile, position encoding (Circle-RoPE, HoPE) is emerging as an underappreciated factor in MLLM visual understanding.

---

## 6. Efficient & Compact MLLMs

Reducing MLLM inference cost through token compression, model compression, and compact architectures designed for resource-constrained deployment.

**Visual Token Reduction** — Dynamically pruning or merging visual tokens to reduce the computational burden of processing images.
- [[2603.22815|PinPoint]] (CVPR'26), [[2506.10967|CDPruner]] (NeurIPS'25), [[2506.07138|STF]], [[2506.01097|Explainability-Guided-Token-Compression]] (ICLR'26), [[2505.22654|VScan]], [[2505.16411|SPIN-HeadSuppression]], [[2504.17040|DyMU]], [[2504.00557|Trimmed-Llama]] (CVPR'25 Workshop), [[2503.16660|Adaptive-Token-Reduction]]

> [!star] Key Papers
> - [[2504.17040|DyMU]] — Training-free framework dynamically reducing visual tokens based on image complexity
> - [[2506.10967|CDPruner]] (NeurIPS'25) — Training-free token pruning leveraging content-dependency analysis
> - [[2505.22654|VScan]] — Two-stage framework achieving up to 90% visual token reduction with minimal quality loss

**Compact Model Architectures** — Building small but capable MLLMs under 3B parameters for edge deployment.
- [[2603.06569|Penguin-VL]], [[2603.00136|TinyVLM]], [[2504.05299|SmolVLM]], [[2504.00595|Open-Qwen2VL]], [[2412.04468|NVILA]] (CVPR'25), [[2411.09691|TinyGroundingGPT]], [[2408.01800|MiniCPM-V]], [[2401.15947|MoE-LLaVA]]

> [!star] Key Papers
> - [[2504.05299|SmolVLM]] — Family of compact multimodal models (256M-2B) processing images and video; competitive with much larger models
> - [[2603.00136|TinyVLM]] — Zero-shot object detection on microcontrollers; sub-1MB models for edge deployment
> - [[2412.04468|NVILA]] (CVPR'25) — NVIDIA's efficient MLLM family achieving competitive quality at reduced compute

**Efficient Inference & Acceleration** — Methods for speeding up MLLM inference at deployment time.
- [[2602.11812|EGTP]] (ICLR'26), [[2512.13607|Nemotron-Cascade]], [[2508.03682|SQLM]], [[2505.22618|Fast-dLLM]] (ICLR'26), [[2505.10526|MASSV]], [[2404.16710|LayerSkip]]

> [!star] Key Papers
> - [[2505.10526|MASSV]] — Speculative decoding framework accelerating VLM inference through multi-head parallel generation

> [!tip] The Efficiency Imperative
> Token reduction is the most impactful lever for MLLM efficiency — VScan and CDPruner achieve 70-90% token reduction with minimal quality loss. For deployment, SmolVLM and TinyVLM show that architecture-level compactness combined with token reduction enables MLLMs on edge devices. The key insight: most visual tokens are redundant for any given query.

---

## 7. Hallucination Mitigation

Addressing the fundamental challenge of MLLMs generating text that contradicts visual evidence — through decoding strategies, contrastive methods, preference optimization, and evaluation frameworks.

**Decoding-Based Methods** — Modifying the generation process to suppress hallucinated content without retraining.
- [[2607.21556|VCSD]], [[2606.09859|MGAP]], [[2602.16702|SAP]], [[2602.11737|OA-VCD]], [[2512.23453|CoFi-Dec]], [[2509.23236|Self-Reflection-VLM]], [[2509.03113|GACD]] (CVPR'26), [[2508.11616|MRGD]] (ICCV'25), [[2507.00898|ONLY]] (ICCV'25), [[2506.23601|SemDiD]] (NeurIPS'25), [[2506.09522|ReVisiT]], [[2506.08391|SECOND]] (ICML'25), [[2504.12137|Efficient Contrastive Decoding]], [[2406.01920|CODE]] (NeurIPS'24), [[2210.15097|Contrastive Decoding]]

> [!star] Key Papers
> - [[2406.01920|CODE]] (NeurIPS'24) — Training-free decoding method reducing hallucination through contrastive output distributions
> - [[2509.03113|GACD]] (CVPR'26) — Gradient-based influence-aware constrained decoding; first to use gradient information for hallucination mitigation
> - [[2512.23453|CoFi-Dec]] — Coarse-to-fine decoding leveraging geometric consistency for grounded generation

**Visual Attention & Token Intervention** — Steering the model's visual attention to reduce over-reliance on language priors.
- [[2608.02124|HAFI-VLM]], [[2605.02735|Silenced-Visual-Latents]], [[2605.00814|PVM]], [[2604.15809|AIF]] (CVPR'26), [[2603.14117|SIEVE-VLM]], [[2603.00207|VisRef]] (CVPR'26), [[2602.24041|AIR]] (ICLR'26), [[2602.21497|ECRD]] (CVPR'26), [[2602.08241|SAYO]], [[2602.02004|ClueTracer]], [[2509.12132|Reflection-V]], [[2508.02419|TVAI]], [[2507.22003|ViHallu]], [[2506.12609|VisFlow]], [[2505.17812|VaLSe]], [[2505.05177|MARK]], [[2411.12591|VIC]]

> [!star] Key Papers
> - [[2506.12609|VisFlow]] — Dual-level attention intervention redirecting model focus toward relevant visual tokens
> - [[2508.02419|TVAI]] — Identifies modality bias as a root cause of hallucination; proposes targeted visual attention injection

**Visual Prompting Against Hallucination** — Using visual cues and prompts to anchor model outputs in visual evidence.
- [[2601.00659|CRoPS]], [[2510.16596|SHIELD]] (ICLR'26), [[2506.16112|AutoV]] (ECCV'26), [[2506.07227|MED]] (NeurIPS'25), [[2504.21559|BBVPE]], [[2503.12799|GCoT]]

> [!star] Key Papers
> - [[2504.21559|BBVPE]] — Black-box visual prompt engineering mitigating hallucination without model access
> - [[2601.00659|CRoPS]] — Dynamic cropping strategy forcing models to attend to relevant image regions

**Preference Optimization & Training-Based** — Aligning MLLM outputs with visual ground truth through preference learning and targeted fine-tuning.
- [[2608.25580|V-Rubrics]], [[2608.19598|PEA-DPO]], [[2604.20366|MPD]], [[2604.20328|HyLaR]] (ECCV'26), [[2602.22859|DPE]], [[2511.15661|VisPlay]], [[2507.16814|SOPHIA]] (NeurIPS'25), [[2506.17901|PostAlign]] (ICLR'26), [[2506.13888|VL-GenRM]], [[2506.10128|ViCrit]] (NeurIPS'25), [[2504.15619|AdaViP]]

> [!star] Key Papers
> - [[2504.15619|AdaViP]] — Adaptive visual preference optimization reducing hallucination through contrastive visual grounding
> - [[2506.17901|PostAlign]] (ICLR'26) — Post-training alignment framework improving visual fidelity without catastrophic forgetting

**Hallucination Analysis & Benchmarks** — Understanding when, why, and how MLLMs hallucinate, including knowledge-grounding ([[2005.11401|RAG]] (NeurIPS'20)) as an orthogonal mitigation strategy.
- [[2609.11244|OmniHallu]], [[2608.29193|HalluPrism]], [[2605.02087|MSM]], [[2604.15574|FT-Hallucinations]], [[2602.09276|Reasoning-ID]], [[2601.21969|Token-Guard]] (ICLR'26), [[2512.07687|HalluShift++]], [[2509.25373|VLM-Perception-Cognition-Survey]], [[2508.01781|LLM-Hallucination-Taxonomy]], [[2507.19024|Multimodal Hallucination Survey]], [[2507.10442|VLM-Three-Space-Analysis]], [[2506.19513|PRE-HAL]], [[2505.23224|MMBoundary]], [[2505.12886|LRM-Hallucination]], [[2502.17422|MLLM-Small-Visual-Details]] (ICLR'25), [[2402.00253|LVLM-Hallucination-Survey]], [[2401.06209|MMVP]] (CVPR'24 Oral), [[2310.00754|LURE]] (ICLR'24), [[2305.10355|POPE]], [[1809.02156|CHAIR]]

> [!star] Key Papers
> - [[2402.00253|LVLM-Hallucination-Survey]] — Comprehensive taxonomy of hallucination types in large vision-language models
> - [[2502.17422|MLLM-Small-Visual-Details]] (ICLR'25) — Reveals fundamental limitations in MLLM perception of small visual details

> [!tip] Defense in Depth
> No single method solves hallucination. The most effective approach combines decoding-time intervention (CODE, GACD) with attention steering (VisFlow, TVAI) and preference alignment (AdaViP). LURE and the LVLM Survey provide the diagnostic framework for understanding which hallucination types affect your specific use case.

---

## 8. Visual Grounding & Spatial Understanding

Enabling MLLMs to localize, reference, and reason about specific objects and regions in images — from bounding box prediction to dense spatial reasoning.

**Grounded MLLMs** — Models that jointly generate text and spatial coordinates for objects.
- [[2607.05978|MTLA]], [[2511.06908|Mono3DVG-EnSD]], [[2411.09691|TinyGroundingGPT]], [[2410.08021|OneRef]] (NeurIPS'24), [[2405.19783|IVM]] (NeurIPS'24), [[2405.17104|LLM-Optic]], [[2404.13013|Groma]] (ECCV'24), [[2401.17981|MLLM-Detection-Infusion]]

> [!star] Key Papers
> - [[2404.13013|Groma]] (ECCV'24) — Localized visual tokenizer for robust MLLM visual grounding at the region level
> - [[2405.19783|IVM]] (NeurIPS'24) — Instruction-guided visual masking that automatically highlights task-relevant image regions

**Visual Prompting for MLLMs** — Methods for communicating spatial information to MLLMs through visual annotations and markers.
- [[2510.09201|MPO]] (ICLR'26), [[2506.16112|AutoV]] (ECCV'26), [[2409.15310|Visual-Prompting-MLLM-Survey]], [[2407.01400|GalLoP]] (ECCV'24), [[2304.06712|Visual-Prompt-Engineering]]

> [!star] Key Papers
> - [[2409.15310|Visual-Prompting-MLLM-Survey]] — Comprehensive survey of visual prompting techniques for MLLMs; taxonomizes the field
> - [[2510.09201|MPO]] (ICLR'26) — Multimodal Prompt Optimizer jointly optimizing textual and visual prompts

**Dense Perception & Tracking** — Fine-grained visual understanding including tracking, referring, and pixel-level grounding.
- [[2608.24574|PhysMLLMs]], [[2603.03857|DeepScan]], [[2512.22799|VPTracker]], [[2510.23603|PixelRefer]], [[2505.23769|TextRegion]]

> [!star] Key Papers
> - [[2510.23603|PixelRefer]] — Unified framework for fine-grained spatiotemporal object understanding in images and videos
> - [[2512.22799|VPTracker]] — Location-aware visual prompting enabling MLLMs for multi-object tracking

**Spatial Reasoning Benchmarks & Analysis** — Evaluating and diagnosing how well MLLMs handle spatial relationships and scene structure.
- [[2604.18484|XEmbodied]], [[2602.21619|VSR-Information-Injection-Analysis]], [[2602.15950|VLM-Spatial-Reasoning-OCR]], [[2602.15918|EarthSpatialBench]], [[2602.03916|SpatiaLab]] (ICLR'26), [[2601.22231|PE-Spatial-Reasoning-Analysis]], [[2601.13304|CausalSpatial]], [[2504.15037|MLLM-Spatial-Reasoning-Position-Paper]], [[2502.11859|VLM-Spatial-Abilities-Benchmark]], [[2406.14852|SpatialEval]] (NeurIPS'24), [[2406.02537|TopViewRS]]

**Spatial Grounding & Scene Understanding Methods** — Models and mechanisms for localizing and reasoning about scene structure beyond object detection, including physical-property inference (gravity, mass, materials, dynamics) as a distinct capability from geometric/spatial reasoning.
- [[2602.03361|Z3D]], [[2601.19834|Visual-Generation-Reasoning]], [[2601.05600|SceneAlign]], [[2601.04777|GeM-VG]], [[2511.21688|G2VLM]], [[2509.06233|O3Afford]] (CoRL'25), [[2507.00505|LLaVA-SP]] (ICCV'25), [[2506.21710|FOCUS]] (NeurIPS'25), [[2506.10778|SlotPi]], [[2506.08708|PhyBlock]] (NeurIPS'25), [[2504.13469|HMPE]], [[2501.09038|Physics-IQ]], [[2411.16044|ZoomEye]], [[2410.08500|STMR]], [[2410.06468|SPACE]] (ICLR'25), [[2312.14135|V*]] (CVPR'24), [[2307.12981|3D-LLM]] (NeurIPS'23 Spotlight)

> [!star] Key Papers
> - [[2601.05600|SceneAlign]] — Aligns MLLMs with scene-level spatial structure for holistic visual understanding
> - [[2602.15950|VLM-Spatial-Reasoning-OCR]] — Reveals consistent spatial reasoning degradation in VLMs on OCR-related tasks
> - [[2501.09038|Physics-IQ]] — Probes whether video foundation models implicitly encode dynamic physical properties (mass, friction); a diagnostic complement to PhyGenBench-style generation tests
> - [[2506.08708|PhyBlock]] (NeurIPS'25) — Block-stacking benchmark exposing whether MLLMs reason about gravitational stability from images alone

> [!tip] Grounding as First-Class Capability
> Grounding is no longer an afterthought — KOSMOS-2 and Shikra (Section 2) showed it can be native. The trend is toward models that ground by default (Groma, PixelRefer) rather than requiring external detection modules. For robotics applications, this shift is critical — see [[11_Robotics-and-Embodied-AI]].

---

## 9. Video & Temporal MLLMs

Extending multimodal understanding to video inputs, requiring models to handle temporal dynamics, long-form content, and cross-frame reasoning.

**Video & Temporal MLLM Methods** — Architectures and benchmarks for temporal reasoning, long-context video memory, and cross-frame understanding.
- [[2609.30221|WanPE]], [[2603.17541|Temporal-Trap-Analysis]], [[2602.20159|VBVR]], [[2602.05986|RISE-Video]], [[2602.01984|Delimiter-Token-Scaling]] (ICLR'26), [[2601.09430|Video-MSR]], [[2507.01544|MARVIS]], [[2506.06279|CoMemo]] (ICML'25), [[2406.07476|VideoLLaMA 2]]

> [!star] Key Papers
> - [[2602.05986|RISE-Video]] — Comprehensive benchmark for evaluating MLLMs on temporal video reasoning
> - [[2602.20159|VBVR]] — Community-curated dataset with over one million video reasoning examples
> - [[2506.06279|CoMemo]] (ICML'25) — Dual-path architecture addressing the long-context memory problem in video MLLMs

> [!tip] The Video Frontier
> Video MLLMs remain significantly behind image MLLMs in capability. The core challenge is temporal context — CoMemo and Delimiter Token Scaling address this through specialized memory and multi-frame architectures. RISE-Video and VBVR provide the benchmarks needed to drive progress.

---

## 10. Reasoning & Trustworthiness

Methods for improving MLLM reasoning capabilities and estimating the reliability of model outputs.

**RL-Trained Visual Reasoning** — Reinforcement-learning methods that train MLLMs to reason over visual input.
- [[2605.15198|ATLAS]], [[2604.03128|Self-Distilled-RLVR]], [[2603.26348|VRE]], [[2602.08346|ThinkWithImages-PRMBENCH]], [[2602.04884|RAL]], [[2601.18631|AdaReasoner]] (ICLR'26), [[2512.12633|DiG]], [[2512.04563|COOPER]], [[2510.20817|MARA]], [[2510.20607|Compositional-Energy-Minimization]] (NeurIPS'25 Spotlight), [[2509.24251|LVR]] (ICLR'26), [[2509.23285|Tool-Light]] (ICLR'26), [[2506.08011|ViGaL]] (ICLR'26), [[2506.07218|Perception-R1]] (ICLR'26), [[2505.24025|DINO-R1]], [[2505.22453|MM-UPT]] (NeurIPS'25), [[2505.22334|Multimodal-RL-Cold-Start]], [[2505.21457|ACTIVE-O3]] (ICML'26), [[2505.20289|VisTA]], [[2505.19702|Point-RFT]] (NeurIPS'25), [[2505.19590|INTUITOR]] (ICLR'26), [[2505.19255|VTool-R1]] (ICLR'26), [[2505.19094|SATORI]], [[2504.18397|UV-CoT]] (ICCV'25), [[2504.13055|NoisyRollout]] (NeurIPS'25), [[2503.20752|Reason-RFT]] (NeurIPS'25), [[2503.16188|Think-or-Not-Think]]

**Visual Reasoning Benchmarks, Probes & Interpretability** — Diagnosing and evaluating what MLLMs actually do when they reason over images.
- [[2603.02556|VC-STaR]] (ICLR'26 Oral), [[2603.00461|ReMoT]] (CVPR'26 Highlight), [[2512.08228|MM-CoT]], [[2508.02095|VLM4D]] (ICCV'25), [[2506.09047|Back-Patching-VLM]] (NeurIPS'25), [[2506.08008|VLMs-Overlook-Visual-Representations]], [[2506.04277|RSVP]], [[2505.23764|MMSI-Bench]] (ICLR'26), [[2505.21538|PAM-CVR]] (NeurIPS'25 Spotlight), [[2505.05626|PERCEPTLLM]], [[2501.13620|VLM-Perception-Reasoning-Probe]], [[2410.10855|CoreCognition]] (ICML'25)

**Chain-of-Thought & Tool-Augmented Visual Reasoning Methods** — Prompting and tool-use techniques that structure step-by-step visual reasoning without RL training.
- [[2605.11856|UniVLR]], [[2511.15703|VLSR]], [[2510.09312|CRV]] (ICLR'26 Oral), [[2506.11515|Manager]], [[2505.23766|Argus]] (CVPR'25), [[2505.20753|Griffon-R]], [[2505.20164|VAT]], [[2504.14200|KeCO]], [[2503.16434|Interactive-Sketchpad]], [[2502.07503|RINS]] (NeurIPS'25), [[2412.13171|CCoT]], [[2412.03548|AURORA]] (CVPR'25), [[2411.10440|LLaVA-CoT]] (ICCV'25), [[2410.16400|VipAct]], [[2406.09403|VisualSketchPad]] (NeurIPS'24), [[2404.03622|VoT]] (NeurIPS'24), [[2303.08128|ViperGPT]] (ICCV'23), [[2302.00923|Multimodal-CoT]], [[2211.11559|VISPROG]] (CVPR'23)

> [!star] Key Papers
> - [[2502.07503|RINS]] (NeurIPS'25) — Recursive Inference Scaling from Google DeepMind; enhances MLLM performance through iterative self-refinement
> - [[2603.02556|VC-STaR]] (ICLR'26 Oral) — Visual Contrastive Self-Taught Reasoner improving VLM reasoning through contrastive self-training
> - [[2302.00923|Multimodal-CoT]] — First to extend chain-of-thought prompting into the multimodal setting, separating rationale generation from answer inference

**Safety, Deception & Alignment Auditing** — Detecting and auditing unsafe, deceptive, or misaligned model behavior.
- [[2604.28182|Exploration-Hacking]], [[2603.30036|CoT-Monitorability]], [[2602.08145|Reliable-Foundation-Models-Survey]], [[2601.14127|MIR-SafetyBench]], [[2512.15926|DSO]], [[2510.06738|AWM]] (ICLR'26), [[2510.06096|Alignment-Auditor]] (ICLR'26), [[2510.01088|Safety-Instincts]] (ICLR'26), [[2509.22989|Strategic-Persuasion]] (ICLR'26), [[2509.03518|LLM-Lying]], [[2506.19823|Persona-Misalignment]] (ICLR'26), [[2506.19807|KnowRL]], [[2502.05206|Safety-at-Scale-Survey]], [[2405.02411|Socially Aware NLP]] (CL)

**Trustworthiness Calibration & Robustness Benchmarks** — Measuring confidence calibration and robustness of MLLM predictions.
- [[2609.22206|MLLM Uncertainty Benchmark]], [[2608.17084|MLLM Uncertainty Survey]], [[2606.14728|FUSE-VLM-UQ]], [[2604.09529|VL-Calibration]], [[2603.13292|Pragma-VL]] (ICLR'26), [[2603.03944|SCP-Bench]], [[2602.21054|VAUQ]], [[2602.14934|GAPA]], [[2602.01816|VIA-Bench]], [[2506.22982|CroPA]], [[2505.23745|TrustVLM]], [[2504.18053|DREAM]], [[2411.11919|VL-Uncertainty]], [[2406.18925|VisArgs]]

> [!star] Key Papers
> - [[2505.23745|TrustVLM]] — Framework estimating prediction trustworthiness by combining internal and external confidence signals
> - [[2602.21054|VAUQ]] — Training-free self-evaluation framework quantifying visual vs. textual reliance in MLLM predictions
> - [[2601.14127|MIR-SafetyBench]] — First benchmark for evaluating safety risks from multi-image reasoning in MLLMs

**Continual & Incremental Learning** — Enabling MLLMs to acquire new knowledge without forgetting prior capabilities.
- [[2609.06986|Long-Horizon Memorization]], [[2603.12056|XSkill-agent-CL]] (ICML'26), [[2602.21628|RuCL]], [[2512.24695|Hope]] (NeurIPS'25), [[2512.09441|MoP-CIL]], [[2510.10487|Triangular-Consistency]] (NeurIPS'25), [[2508.04227|VLM-Continual-Learning-Survey]], [[2410.19925|MLLM-Continual-Learning]] (NeurIPS'24)

> [!star] Key Papers
> - [[2410.19925|MLLM-Continual-Learning]] (NeurIPS'24) — Systematic quantification of linguistic forgetting in continually trained MLLMs
> - [[2508.04227|VLM-Continual-Learning-Survey]] — Comprehensive taxonomy of continual learning challenges specific to VLMs

**Multimodal Reasoning: Data, Representation & Efficiency** — Non-RL methods improving multimodal reasoning through data curation, representation design, or inference efficiency.
- [[2606.07500|SETA]], [[2602.02951|NUWA]] (ICLR'26), [[2512.12822|LEMON]], [[2511.22715|ReAG]] (CVPR'26), [[2511.19972|Activation-Replay-MM]] (CVPR'26), [[2511.17487|EXTRACT+THINK]] (CVPR'26), [[2510.14605|Wiki-PRF]] (NeurIPS'25), [[2510.08673|Puffin]] (ICLR'26), [[2508.15568|ADAPT]] (NeurIPS'25), [[2507.10302|DisCo]] (ICCV'25), [[2506.22819|TCA]], [[2506.05302|PAM]] (NeurIPS'25), [[2506.04559|RAPID]] (ICLR'26), [[2506.04209|LIFT]], [[2506.02138|PA-LRP]] (NeurIPS'25), [[2505.16151|FRANK]], [[2505.07956|LLM-LEx]], [[2502.20120|Modality-Boosting]] (NeurIPS'25 Oral)

> [!tip] Reasoning You Can Trust
> MLLM reasoning gains now come mostly from RL on verifiable visual tasks, but a reasoning trace is only useful if its confidence is trustworthy. TrustVLM scores predictions training-free from image-to-text and image-to-image similarity, VAUQ quantifies how much a prediction relies on visual evidence, and MIR-SafetyBench is the first benchmark for safety risks that arise from multi-image reasoning, so calibration and safety checks belong next to the RL that improves accuracy. Agent, self-improvement and harness work formerly listed here now lives in [[10_Agents-and-Tool-Use]] and [[09_Self-Evolving-AI]].

---

## 11. Interpretability & Mechanistic Analysis

Understanding what MLLMs learn internally — which visual features matter, how cross-modal representations are structured, and why models produce specific outputs.

**Mechanistic Analysis & Circuit-Level Tools** — General mechanistic-interpretability primitives (circuits, sparse features, task representations) applied to transformers.
- [[2608.12036|Mechanist]], [[2605.14738|TAPIOCA]], [[2605.03808|Agentic-imodels]], [[2604.11791|Looped-Reasoning-Mechanistic-Analysis]], [[2603.17063|Transformers-as-Bayesian-Networks]], [[2507.02199|Huginn-Latent-CoT]], [[2506.15679|Dense-SAE-Latents]] (NeurIPS'25), [[2504.20966|Softpick]], [[2502.14010|ICL-Attention-Heads]] (ICML'25), [[2501.09333|Prompt-CAM]] (CVPR'25), [[2310.15916|Task Vectors]], [[2310.15213|Function Vectors]] (ICLR'24), [[2309.08600|Sparse Autoencoders]] (ICLR'24), [[2209.11895|Induction Heads]]

**Visual Representation & Cross-Modal Probing** — Tools and analyses specific to probing what MLLMs encode visually and cross-modally.
- [[2607.03973|MANCE]], [[2603.07335|VisualScratchpad]] (ICLR'26 Workshop), [[2602.15029|Language-Symmetry-Representations]] (ICML'26), [[2602.11217|Magic-Correlations]], [[2602.11144|GENIUS]], [[2602.02140|GAPEVAL]], [[2602.00462|LatentLens]] (ICML'26), [[2510.02292|VLM-Lens]], [[2506.11976|VLM-Visual-Language-Alignment]], [[2506.07326|Reward-Model-Interpretability]], [[2504.19627|VCM]], [[2502.02013|Layer-by-Layer-Representations]] (ICML'25 Oral)

> [!star] Key Papers
> - [[2602.00462|LatentLens]] (ICML'26) — Training-free method interpreting visual token representations layer-by-layer inside MLLMs
> - [[2603.07335|VisualScratchpad]] (ICLR'26 Workshop) — Interactive framework using Sparse Autoencoders to analyze and causally test visual features
> - [[2510.02292|VLM-Lens]] — Unified toolkit for systematically extracting and analyzing internal VLM representations

> [!tip] Interpretability Enables Improvement
> LatentLens and VLM-Lens reveal what MLLMs actually attend to, which directly informs hallucination mitigation (Section 7) and feature integration (Section 5). Understanding internal representations is not academic curiosity — it is the diagnostic tool for improving model quality.

---

## 12. Adaptation, Recognition & Retrieval

Applying MLLMs and VLMs to downstream tasks including fine-grained recognition, image-text retrieval, domain adaptation, and specialized applications.

**Fine-Grained Recognition** — Leveraging MLLM capabilities for detailed visual categorization and recognition tasks.
- [[2602.00795|DVLA-RL]] (ICLR'26), [[2507.23070|E-FineR]], [[2507.10203|ARL]] (ICCV'25), [[2507.10202|ECP]] (CVPR'25 Workshop), [[2505.16149|REVEAL]], [[2505.11192|FALCON]] (CVPR'26), [[2505.02056|VLM-Pseudo-label-Calibration]] (ICML'25), [[2505.01064|NeaR]], [[2311.04157|INTR]] (ICLR'24), [[2309.08912|MP-FGVC]]

> [!star] Key Papers
> - [[2505.01064|NeaR]] — Vocabulary-free fine-grained visual recognition combining MLLM-generated descriptions with retrieval
> - [[2507.23070|E-FineR]] — Fully automated, training-free fine-grained recognition without predefined vocabularies

**Retrieval & Composition** — Methods for image-text retrieval and composed image retrieval using VLMs.
- [[2604.12148|ViLL-E]], [[2603.02959|SS-Text-U]], [[2508.04987|UniMoS++]], [[2506.23115|MoCa]], [[2505.20046|REARANK]], [[2505.19707|MVFT-JI]], [[2503.23508|Real-LOD]] (ICLR'25), [[2501.05452|ReFocus]] (ICML'25)

> [!star] Key Papers
> - [[2505.19707|MVFT-JI]] — Zero-shot composed image retrieval through direct VLM fine-tuning
> - [[2506.23115|MoCa]] — Transforms causal VLMs into bidirectional encoders for robust retrieval

**Creative & Domain-Specific Applications** — MLLMs applied to creative, simulation, and unconventional domain tasks.
- [[2607.15314|Cura 1T]], [[2607.08374|JAM]], [[2606.31209|RosettaSim]] (ECCV'26), [[2606.31131|Crash-to-Scenario LLM Pipeline]], [[2604.13074|PersonaVLM]] (CVPR'26), [[2511.11007|VisMem]], [[2505.21497|PosterAgent]] (NeurIPS'25), [[2505.11820|CoLM]] (NeurIPS'25), [[2505.01812|New-News]], [[2411.17673|SketchAgent]] (CVPR'25), [[2312.04684|LaRS]], [[2301.05226|IPVR]], [[2210.02506|GameBugDescriptions]]

**Evaluation, Testing & Deployment Applications** — Evaluating and stress-testing MLLM applications for real-world deployment.
- [[2601.12585|MLLM-Visualization-Literacy]], [[2601.00561|AEGIS]], [[2511.20814|SPHINX]], [[2509.24207|Humanline]] (ICLR'26), [[2508.13142|EASI]], [[2507.01955|GPT-4o-Vision-Evaluation]] (ICLR'26), [[2506.22395|Test-Time-VLM-Consistency]], [[2412.18072|MMFactory]], [[2403.19103|PRISM-T2I]], [[2310.10625|VLP]] (ICLR'24), [[2305.00104|MMViT]]

> [!star] Key Papers
> - [[2505.21497|PosterAgent]] (NeurIPS'25) — Automated academic poster generation from papers; demonstrates creative MLLM applications
> - [[2601.12585|MLLM-Visualization-Literacy]] — First taxonomy of visualization literacy barriers in MLLMs
> - [[2604.13074|PersonaVLM]] (CVPR'26) — Long-term personalized MLLM with dynamic memory architecture; 79% win rate vs. GPT-4o on open-ended personalized generation

> [!tip] MLLMs as General Visual Assistants
> The fine-grained recognition results (NeaR, E-FineR) show that MLLMs can replace specialized classifiers when paired with the right prompting strategy. For retrieval, MoCa's trick of converting causal models to bidirectional encoders unlocks capabilities that the original training never intended.

---

## 13. Open-Vocabulary Detection with MLLMs

Extending MLLM capabilities to open-vocabulary object detection — detecting objects described by arbitrary text at inference time.

**Open-Vocabulary Detection with MLLMs** — Steering or pretraining MLLMs/VLMs to detect objects described by arbitrary text.
- [[2505.23004|QLIP]] (ICLR'26), [[2505.20612|RF100-VL]] (NeurIPS'25), [[2502.17425|VPT]], [[2501.18954|LLMDet]] (CVPR'25), [[2410.13842|D-FINE]], [[2404.09216|DetCLIPv3]] (CVPR'24), [[2304.04514|DetCLIPv2]] (CVPR'23), [[2209.15639|F-VLM]] (ICLR'23), [[2209.09407|DetCLIP]] (NeurIPS'22)

> [!star] Key Papers
> - [[2304.04514|DetCLIPv2]] (CVPR'23) — End-to-end pre-training for open-vocabulary detection learning directly from large-scale image-text data
> - [[2209.15639|F-VLM]] (ICLR'23) — Open-vocabulary detection using frozen VLMs with minimal training overhead
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
