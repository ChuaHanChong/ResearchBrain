---
title: "Diffusion & Generation — Topic Overview"
tags:
  - diffusion
  - image-generation
  - flow-matching
  - generative
  - discrete-diffusion
  - unified-multimodal
aliases:
  - "Diffusion Overview"
---

# Diffusion & Generation

> [!abstract] Overview
> Diffusion models and related generative architectures have expanded far beyond image synthesis. This topic tracks the full generative landscape: from foundational diffusion theory through discrete diffusion language models, unified multimodal architectures that combine understanding and generation, RL-based alignment of generative models, and applications in image editing, 3D, and robotics. The core question has shifted from "can diffusion generate images?" to "can diffusion replace autoregression as the foundation for general intelligence?"

## Evolution Graph

```text
1. Image Generation Backbone   (what the denoiser runs on)
· latent space to transformer
                                      U-Net →           +scale, refiner    +unified continuous
                                      transformer       stage              tokens
╔════════════════════════════════╗    ┌────────────┐    ┌─────────────┐    ┌─────────────────┐
║ Latent Diffusion Models (2021) ║───►│ DiT (2022) │───►│ SDXL (2023) │───►│ UniFluid (2025) │
╚════════════════┬═══════════════╝    └────────────┘    └─────────────┘    └─────────────────┘
                 │    images → video
                 │    ┌──────────────────┐
                 └───►│ CogVideoX (2024) │
                      └──────────────────┘

2. Discrete Diffusion LLMs   (replace autoregression outright)
· masked-token generation
                    +variance-reduced       +cached parallel
                    preference opt          decoding
╔══════════════╗    ┌──────────────────┐    ┌──────────────────┐
║ LLaDA (2025) ║───►│ LLaDA-1.5 (2025) │───►│ Fast-dLLM (2025) │
╚═══════┬══════╝    └──────────────────┘    └──────────────────┘
        │    +RL
        │    post-training
        │    ┌───────────┐
        ├───►│ d1 (2025) │
        │    └───────────┘
        │    +weighted policy
        │    optimization
        │    ┌──────────────┐
        └───►│ wd1 (2025)   │
             └──────────────┘

3. Unified Multimodal   (one model, both directions)
· fuse the objectives
                        +diffusion loss beside    +single              +diffusion across
                        next-token                transformer          all modalities
┌──────────────────┐    ┌────────────────────┐    ┌───────────────┐    ┌───────────────┐
│ Chameleon (2024) │───►│ Transfusion (2024) │───►│ Show-o (2024) │───►│ MMaDA (2025)  │
└─────────┬────────┘    └────────────────────┘    └───────────────┘    └───────────────┘
          │    +next-token for
          │    everything
          │    ┌─────────────┐
          ├───►│ Emu3 (2024) │
          │    └─────────────┘
          │    +1D compact
          │    tokenizer
          │    ┌──────────────┐
          └───►│ TiTok (2025) │
               └──────────────┘

4. RL Alignment   (align the sampler itself)
· reward through the denoiser
                   +direct reward      diffusion → flow                                 +self-improving,
                   backprop            matching                +tree branching, 4.7x    no external data
┌─────────────┐    ┌──────────────┐    ┌──────────────────┐    ┌───────────────────┐    ┌──────────────┐
│ DDPO (2023) │───►│ DRaFT (2023) │───►│ Flow-GRPO (2025) │───►│ BranchGRPO (2025) │───►│ UniRL (2025) │
└──────┬──────┘    └──────────────┘    └──────────────────┘    └───────────────────┘    └──────────────┘
       │    training →
       │    inference-time steering
       │    ┌─────────────────────┐
       └───►│ FK-Steering (2025)  │
            └─────────────────────┘

5. Chain-of-Thought Generation   (reason before you draw)
· reasoning in the loop
                                   +bi-level             +MLLM reasoning
                                   semantic/token CoT    in editing         images → video reasoning
┌─────────────────────────────┐    ┌────────────────┐    ┌─────────────┐    ┌───────────────────────────┐
│ CoT-Image-Generation (2025) │───►│ T2I-R1 (2025)  │───►│ GoT (2025)  │───►│ Thinking-in-Frames (2026) │
└─────────────────────────────┘    └────────────────┘    └─────────────┘    └───────────────────────────┘

6. Diffusion for Control   (trajectories, not images)
· denoise the action
                                                      +flow-matching    +efficient VLA
                       +visuomotor control            action expert     flow
╔═════════════════╗    ┌─────────────────────────┐    ┌────────────┐    ┌───────────────┐
║ Diffuser (2022) ║───►│ Diffusion-Policy (2023) │───►│ pi0 (2024) │───►│ FLOWER (2025) │
╚════════┬════════╝    └─────────────────────────┘    └────────────┘    └───────────────┘
         │    actions → video
         │    as policy
         │    ┌──────────────┐
         ├───►│ UniPi (2023) │
         │    └──────────────┘
         │    +compact VLA
         │    ┌────────────────┐
         └───►│ SmolVLA (2025) │
              └────────────────┘

7. Physical Plausibility   (does the generated video obey physics)
· benchmark, then reward
                      +text-to-video physics    +harder physical         benchmark → reward
                      eval                      commonsense              model
┌────────────────┐    ┌────────────────────┐    ┌───────────────────┐    ┌─────────────────┐
│ Physion (2021) │───►│ PhyGenBench (2024) │───►│ VideoPhy-2 (2025) │───►│ WMReward (2026) │
└────────────────┘    └────────────────────┘    └───────────────────┘    └─────────────────┘

8. Physics-Grounded 3D   (put mechanics in the representation)
· recover material properties
                       NeRF → Gaussian            +material               +expert constitutive
                       continuum                  distillation            models
┌─────────────────┐    ┌─────────────────────┐    ┌──────────────────┐    ┌───────────────────┐
│ PAC-NeRF (2023) │───►│ PhysGaussian (2023) │───►│ Physics3D (2024) │───►│ OmniPhysGS (2025) │
└─────────────────┘    └──────────┬──────────┘    └──────────────────┘    └───────────────────┘
                                  │    +video-diffusion priors
                                  │    ┌─────────────────────┐
                                  ├───►│ DreamPhysics (2024) │
                                  │    └─────────────────────┘
                                  │    +real-to-sim twins
                                  │    ┌─────────────────┐
                                  └───►│ PhysTwin (2025) │
                                       └─────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```

The eight lanes divide on **what diffusion is being applied to**. **Image generation backbone** settles what the denoiser runs on, Latent Diffusion Models moving it into latent space, DiT swapping the U-Net for a transformer, SDXL scaling it, UniFluid unifying the token space, with CogVideoX branching from images to video. **Discrete diffusion LLMs** replace autoregression outright, LLaDA to LLaDA-1.5 to Fast-dLLM, while d1 and wd1 branch to post-train it with RL. **Unified multimodal** fuses both directions in one model, Chameleon to Transfusion to Show-o to MMaDA, with Emu3 and TiTok branching on pure next-token prediction and compact tokenization. **RL alignment** puts reward through the denoiser, DDPO to DRaFT to Flow-GRPO to BranchGRPO to UniRL, with FK-Steering branching to skip training and steer at inference. **Chain-of-thought generation** makes the model reason before it draws, CoT-Image-Generation to T2I-R1 to GoT to Thinking-in-Frames. **Diffusion for control** denoises actions rather than pixels, Diffuser to Diffusion-Policy to pi0 to FLOWER, with UniPi and SmolVLA branching toward video-as-policy and compact VLAs. **Physical plausibility** asks whether the output obeys physics at all, Physion to PhyGenBench to VideoPhy-2, until WMReward turns the benchmark into a reward model. **Physics-grounded 3D** puts mechanics inside the representation, PAC-NeRF to PhysGaussian to Physics3D to OmniPhysGS, with DreamPhysics and PhysTwin branching to video-diffusion priors and real-to-sim twins.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2021 | [[2106.08261\|Physion]] | Physical Plausibility · Benchmark then Reward | Foundational dataset that pioneered "physics prediction from video" as a benchmark setting; the original benchmark that defined the model-vs-human physical-prediction gap |
| 2021 | [[2112.10752\|Latent Diffusion Models]] | Backbone · Latent Space to Transformer | Runs diffusion in a compressed autoencoder latent space instead of pixel space; the architecture behind Stable Diffusion and the efficiency backbone of nearly all modern T2I systems |
| 2022 | [[2205.09991\|Diffuser]] | Control · Denoise the Action | First to use denoising diffusion for RL planning; treated trajectories as data to denoise |
| 2022 | [[2212.09748\|DiT]] | Backbone · Latent Space to Transformer | Replaced the U-Net backbone with a Transformer for diffusion; the architecture underlying nearly every modern T2I/T2V model |
| 2023 | [[2302.00111\|UniPi]] | Control · Denoise the Action | Universal policy as text-conditioned video generation; crosses the boundary between video models and robot control |
| 2023 | [[2303.04137\|Diffusion-Policy]] | Control · Denoise the Action | Extended diffusion to visuomotor control; became the standard for robot action generation |
| 2023 | [[2303.05512\|PAC-NeRF]] | Physics-3D · Material Properties | Physics-Augmented Continuum NeRF; jointly recovers geometry and material parameters (Young's modulus, density, plasticity) from video, foundational for material-property estimation from pixels |
| 2023 | [[2305.13301\|DDPO]] | RL Alignment · Reward through the Denoiser | Reformulated multi-step denoising as an MDP and applied policy gradients; the first principled RL approach to diffusion alignment, outperforming reward-weighted regression across compressibility, aesthetics, and prompt alignment |
| 2023 | [[2307.01952\|SDXL]] | Backbone · Latent Space to Transformer | Scaled latent diffusion to a two-stage base+refiner pipeline; became the standard open-weight T2I model |
| 2023 | [[2309.17400\|DRaFT]] | RL Alignment · Reward through the Denoiser | Direct backpropagation of differentiable rewards through the entire sampling chain via LoRA + gradient checkpointing; >200× more sample-efficient than DDPO and the foundation for modern reward-gradient methods |
| 2023 | [[2311.12198\|PhysGaussian]] | Physics-3D · Material Properties | Couples 3D Gaussian Splatting with continuum mechanics MPM solver; first to make 3DGS scenes physically interactive without rebuilding meshes |
| 2024 | [[2405.09818\|Chameleon]] | Unified · Fuse the Objectives | Meta's early-fusion token-based model; proved full modality unification is architecturally viable at scale |
| 2024 | [[2406.01476\|DreamPhysics]] | Physics-3D · Material Properties | Physics-based 3D dynamics learned from video diffusion priors via score distillation; among the first to make image/video diffusion supervise material parameter inference |
| 2024 | [[2406.04338\|Physics3D]] | Physics-3D · Material Properties | Distills physical properties (Young's modulus, viscosity, plasticity) into 3D Gaussians via video diffusion priors; the canonical Score-Distillation-from-video-prior recipe for material inference |
| 2024 | [[2408.06072\|CogVideoX]] | Backbone · Latent Space to Transformer | Expert-transformer T2V diffusion model that established a strong open baseline for text-to-video generation |
| 2024 | [[2408.11039\|Transfusion]] | Unified · Fuse the Objectives | Pioneered mixing next-token prediction with diffusion loss in one model; outperformed quantization approaches |
| 2024 | [[2408.12528\|Show-o]] | Unified · Fuse the Objectives | Single transformer unifying understanding and generation; proved unified architectures are viable |
| 2024 | [[2409.18869\|Emu3]] | Unified · Fuse the Objectives | Showed next-token prediction alone can handle text, image, and video generation without diffusion |
| 2024 | [[2410.05363\|PhyGenBench]] | Physical Plausibility · Benchmark then Reward | 160-prompt benchmark across Mechanics/Optics/Thermal/Materials with PhyGenEval auto-scoring (Spearman ρ=0.81 with humans); top T2V model scored only 0.51/3.0, exposing the physics gap |
| 2024 | [[2410.24164\|pi0]] | Control · Denoise the Action | Vision-language-action flow model for general robot control; established flow matching as the standard for VLA action generation |
| 2025 | [[2501.06848\|FK-Steering]] | RL Alignment · Reward through the Denoiser | Feynman-Kac Interacting Particle Systems for steering diffusion at inference; enables a 0.8B Stable Diffusion to beat a 2.6B fine-tuned SDXL-DPO and works for both continuous and discrete state spaces |
| 2025 | [[2501.13926\|CoT-Image-Generation]] | CoT Generation · Reasoning in the Loop | First comprehensive study of CoT for AR image generation; +24% over Show-o baseline |
| 2025 | [[2501.18982\|OmniPhysGS]] | Physics-3D · Material Properties | Constitutive Gaussians with learnable per-particle constitutive networks; ensemble of 12 expert models + custom PyTorch MPM reduces memory **75%** vs Warp solvers |
| 2025 | [[2502.09992\|LLaDA]] | Discrete Diffusion · Masked-Token Generation | First 8B diffusion LLM competitive with AR models; proved diffusion works for large-scale language modeling |
| 2025 | [[2503.06800\|VideoPhy-2]] | Physical Plausibility · Benchmark then Reward | Action-centric physical commonsense benchmark; best models hit only 32.6% joint performance (22% on hard subset), with VideoPhy-2-AutoEval offering 47–49% relative gains as automated judge |
| 2025 | [[2503.10639\|GoT]] | CoT Generation · Reasoning in the Loop | Integrates MLLM reasoning into visual generation and editing via a unified framework |
| 2025 | [[2503.13436\|UniFluid]] | Backbone · Latent Space to Transformer | Google DeepMind's unified AR framework using continuous and discrete tokens for seamless visual generation and understanding |
| 2025 | [[2503.17973\|PhysTwin]] | Physics-3D · Material Properties | Single-image-to-physical-twin pipeline; estimates material parameters and rigging that re-simulate under arbitrary forces |
| 2025 | [[2504.12216\|d1]] | Discrete Diffusion · Masked-Token Generation | First RL post-training framework for dLLMs; introduced diffu-GRPO with +26.2% on Countdown |
| 2025 | [[2505.00703\|T2I-R1]] | CoT Generation · Reasoning in the Loop | Bi-level CoT (semantic + token) with RL; excels on complex, reasoning-intensive prompts |
| 2025 | [[2505.05470\|Flow-GRPO]] | RL Alignment · Reward through the Denoiser | First framework adapting GRPO to flow matching; enables online RL for continuous generative models |
| 2025 | [[2505.15809\|MMaDA]] | Unified · Fuse the Objectives | Unified diffusion model handling text reasoning, image generation, and multimodal understanding simultaneously |
| 2025 | [[2505.19223\|LLaDA-1.5]] | Discrete Diffusion · Masked-Token Generation | Variance-Reduced Preference Optimization for aligning masked diffusion models with human preferences |
| 2025 | [[2505.22618\|Fast-dLLM]] | Discrete Diffusion · Masked-Token Generation | Training-free 27.6x throughput improvement via KV cache and confidence-aware parallel decoding |
| 2025 | [[2505.23380\|UniRL]] | RL Alignment · Reward through the Denoiser | Unified self-improving post-training for both diffusion and flow models |
| 2025 | [[2506.01844\|SmolVLA]] | Control · Denoise the Action | Affordable and efficient VLA via flow matching; democratized robot learning with minimal compute requirements |
| 2025 | [[2506.08257\|TiTok]] | Unified · Fuse the Objectives | Highly compressed 1D tokenizer that generates images via test-time optimization without a generative model |
| 2025 | [[2507.08838\|wd1]] | Discrete Diffusion · Masked-Token Generation | Weighted policy optimization achieving up to 100% improvement on reasoning benchmarks while eliminating SFT |
| 2025 | [[2509.04996\|FLOWER]] | Control · Denoise the Action | Generalist flow-based VLA policy enabling broad robot skill transfer across embodiments |
| 2025 | [[2509.06040\|BranchGRPO]] | RL Alignment · Reward through the Denoiser | Tree-structured branching yielding 4.7x training speedup and 16% better alignment over vanilla GRPO |
| 2026 | [[2601.10553\|WMReward]] | Physical Plausibility · Benchmark then Reward | Differentiable physics reward derived from V-JEPA2 prediction surprise; first place at ICCV 2025 PhysicsIQ Challenge with 62.64%, +11.4% human-preference win rate via Best-of-N + gradient guidance |
| 2026 | [[2601.21037\|Thinking-in-Frames]] | CoT Generation · Reasoning in the Loop | Video generators as visual reasoners; discovers "Visual Test-Time Scaling" where more frames improve OOD performance |

---

## 1. Image Generation & Editing Architectures

Dedicated architectures for high-quality image synthesis, editing, and multimodal generation that bridge pre-trained language models with visual output. These systems focus on the engineering challenge of getting LLMs to produce, modify, and control visual content.

**Foundational & Classic Diffusion Architectures** — Canonical latent and transformer diffusion backbones for image and video synthesis, alongside the early wave of customization and control methods that first made pretrained T2I/T2V diffusion models steerable without full retraining, plus the training-data infrastructure that scaled large-scale T2I pretraining.
- [[2608.05976|Diff-VF]], [[2607.08770|LongE2V]], [[2605.18233|MIGA]] (ICML'26), [[2412.07730|STIV]] (ICCV'25), [[2408.06072|CogVideoX]] (ICLR'25), [[2406.17758|MotionBooth]] (NeurIPS'24 Spotlight), [[2406.16863|FreeTraj]], [[2312.00777|VideoBooth]] (CVPR'24), [[2311.17982|VBench]] (CVPR'24 Highlight), [[2310.20700|SEINE]] (ICLR'24), [[2308.06571|ModelScopeT2V]], [[2307.04725|AnimateDiff]] (ICLR'24 Spotlight), [[2307.01952|SDXL]] (ICLR'24 Spotlight), [[2306.01872|Video Adapter]], [[2304.01186|Follow-Your-Pose]], [[2212.11565|Tune-A-Video]] (ICCV'23), [[2212.09748|DiT]], [[2210.02303|Imagen Video]], [[2112.10752|Latent Diffusion Models]], [[2111.02114|LAION-400M]]

> [!star] Key Papers
> - [[2112.10752|Latent Diffusion Models]] — Runs diffusion in a compressed autoencoder latent space instead of pixel space; the architecture behind Stable Diffusion and the efficiency backbone of nearly all modern T2I systems
> - [[2212.09748|DiT]] — Replaced the U-Net backbone with a Transformer for diffusion; the architecture underlying nearly every modern T2I/T2V model
> - [[2307.01952|SDXL]] (ICLR'24 Spotlight) — Scaled latent diffusion to a two-stage base+refiner pipeline; became the standard open-weight T2I model
> - [[2408.06072|CogVideoX]] (ICLR'25) — Expert-transformer T2V diffusion model that established a strong open baseline for text-to-video generation

**LLM-Integrated Image Generation** — Connect pre-trained LLMs to image decoders, enabling models to generate images as part of natural language interaction, orchestrate agentic media-generation pipelines, or self-improve generation quality via generated feedback.
- [[2609.08282|GGF]], [[2607.04438|ResearchStudio-Reel]], [[2606.27376|Ask-Solve-Generate]], [[2603.29620|Unify-Agent]], [[2603.28713|DreamLite]], [[2510.27492|ThinkMorph]] (ICLR'26), [[2507.16663|MLLM-Self-Improvement]] (ICLR'26), [[2504.20996|X-Fusion]] (ICCV'25), [[2504.06256|MetaQueries]], [[2411.08127|TIPO]] (ICLR'26), [[2310.02239|MiniGPT-5]], [[2305.17216|GILL]] (NeurIPS'23)

> [!star] Key Papers
> - [[2305.17216|GILL]] (NeurIPS'23) — First to enable LLMs to generate novel images via learned mapping to frozen Stable Diffusion
> - [[2504.06256|MetaQueries]] — Bridges frozen MLLMs with diffusion generators via learned meta-query tokens
> - [[2507.16663|MLLM-Self-Improvement]] (ICLR'26) — Systematic framework for MLLMs to improve generation via self-generated feedback

**End-to-End Multimodal Generators** — Models that natively produce interleaved text and images, trained end-to-end for seamless multimodal output.
- [[2607.15038|Wan-Streamer v0.3]], [[2607.04443|Wan-Streamer v0.2]], [[2605.04128|JoyAI-Image]], [[2602.21435|AD-Loop]] (ICLR'26), [[2602.12205|DeepGen-1.0]], [[2602.05449|DisCa]], [[2510.26583|Emu3.5]], [[2510.08673|Puffin]] (ICLR'26), [[2503.20314|Wan]], [[2503.13436|UniFluid]], [[2501.08316|APT]] (ICML'25), [[2412.14164|MetaMorph]] (ICCV'25), [[2409.04429|VILA-U]] (ICLR'25), [[2407.06135|ANOLE]], [[2404.14396|SEED-X]], [[2312.13286|Emu2]] (CVPR'24), [[2309.05519|NExT-GPT]] (ICML'24 Oral)

**Text-to-Motion Generation** — Diffusion and contrastive methods for synthesizing and retrieving 3D human motions from natural language, including LLM-planned + physics-aware refinement pipelines.
- [[2607.08741|ARDY]], [[2607.05938|Prior-First, Condition-Second]], [[2606.26981|ICMPG]], [[2606.18243|MOCHI]], [[2605.30969|OmniME]], [[2604.24833|MotionBricks]], [[2604.17807|Re2MoGen]], [[2604.10836|HO-Flow]], [[2603.19305|PhyGile]], [[2603.19227|MoTok]], [[2603.15546|Kimodo]], [[2510.14427|Compositional-Phase-Diffusion]] (NeurIPS'25 Oral), [[2509.03883|HMVG Survey]], [[2507.05419|Motion Generation Survey 2025]], [[2506.03191|AR-LLM Motion Generation Survey]], [[2505.09379|Text-driven Motion Generation Survey]], [[2410.10790|Sitcom-Crafter]] (ICLR'25), [[2408.17135|TIMotion]] (CVPR'25), [[2405.18700|MCLD]], [[2405.18483|Open-Domain Multi-Person Motion Synthesis]] (ECCV'24), [[2405.18438|GHOST]], [[2405.15763|FreeMotion]] (ECCV'24), [[2405.07784|Scene-Aware Text-to-Motion]] (CVPR'24), [[2404.09988|in2IN]] (CVPR'22 Workshop), [[2404.04890|S2Fusion]] (CVPR'24), [[2401.08570|RoHM]] (CVPR'24 Oral), [[2306.00416|A-MDM]], [[2305.00976|TMR]], [[2209.14916|MDM]] (ICLR'23 Oral)

> [!star] Key Papers
> - [[2604.17807|Re2MoGen]] — MCTS-enhanced LLM keyframe planning + diffusion completion + PPO physics refinement; SOTA open-vocabulary T2M with 2.46 mm float error
> - [[2401.08570|RoHM]] (CVPR'24 Oral) — Denoising-diffusion robust human motion reconstruction that jointly fills occlusion gaps and denoises noisy pose estimates

**Human Interaction & Multi-Person Motion Generation** — Generative and survey work specifically on human-human, human-object, and human-scene interaction, from social group motion to dyadic dance and interaction-aware video synthesis, plus spoken-dialogue models that emit co-speech full-body motion.
- [[2609.04250|Motion-Omni]], [[2512.19692|Interact2Ar]], [[2512.09646|VHOI]], [[2506.18680|DuetGen]], [[2503.22906|SocialGen]], [[2503.16289|SceneMI]], [[2503.13120|3D Human Interaction Generation Survey]], [[2503.12763|Human Interaction Motion Generation Survey]]

> [!star] Key Papers
> - [[2512.19692|Interact2Ar]] — First end-to-end text-conditioned autoregressive diffusion model for full-body human-human interaction, generating hand motion jointly with body via a cooperative multi-head denoiser
> - [[2503.12763|Human Interaction Motion Generation Survey]] — First comprehensive review unifying human-human, human-object, human-scene, and human-mix interaction under one taxonomy across 110+ methods and 68 datasets

**Physics-Based & RL Character Control** — RL-driven physically-simulated character control via distilled universal motion priors, adversarial latent skill embeddings, or language-directed control; the pre-diffusion generation of generative character-animation methods that A-MDM and RoHM later extended with denoising diffusion.
- [[2609.17682|DSD]], [[2606.03536|Bionic-Whole-Body-Control]], [[2605.26006|MIND]], [[2310.04582|PULSE]] (ICLR'24 Spotlight), [[2308.12969|ROAM]], [[2305.02195|CALM]], [[2302.00883|Physical Character-Scene Interactions]], [[2301.13868|PADL]]

> [!star] Key Papers
> - [[2310.04582|PULSE]] (ICLR'24 Spotlight) — Distills a universal humanoid motion prior for physics-based control, reusable across downstream RL tasks
> - [[2305.02195|CALM]] — Conditional adversarial latent model producing directable, diverse virtual-character behaviors without task-specific reward shaping

> [!star] Key Papers
> - [[2309.05519|NExT-GPT]] (ICML'24 Oral) — End-to-end any-to-any multimodal LLM covering text, image, video, and audio
> - [[2503.13436|UniFluid]] — Google DeepMind's unified AR framework using continuous and discrete tokens for seamless visual generation and understanding

**VLM-Guided Image Editing & Refinement** — VLM-in-the-loop methods that use a vision-language model to plan, critique, or verify instruction-guided image edits and refinements.
- [[2607.05465|CanvasAgent]], [[2604.25636|RvR]], [[2604.06870|RefineAnything]], [[2604.04746|Think-in-Strokes]], [[2604.00849|DisCo-Image]] (CVPR'26), [[2604.00530|AceTone]] (CVPR'26), [[2603.29602|IMAGAgent]], [[2509.12883|Lego-Edit]], [[2506.20911|FaSTA*]], [[2506.04158|IEAP]], [[2505.18600|CoZ]] (NeurIPS'25 Spotlight), [[2503.10613|CoSTA*]], [[2403.19103|PRISM-T2I]]

**Diffusion-Based Image/Video Editing, Control & Benchmarks** — Diffusion-native editing, spatial-control, and privacy/domain-transfer methods for image and video content, plus benchmarks for spatial and compositional generation.
- [[2609.01252|MeRoPE]], [[2608.21776|SpatialDiff]] (CVPR'26), [[2608.16812|ConceptEdit]], [[2607.10873|X-GuideAR]], [[2606.00351|UniVerse]], [[2605.07429|MagicBokeh]] (CVPR'26 Oral), [[2605.02757|VideoTransfer-VLA]] (ICML'26), [[2604.04911|SpatialEdit]], [[2604.02296|VOID]], [[2602.19083|ChordEdit]] (CVPR'26), [[2601.20354|SpatialGenEval]] (ICLR'26), [[2601.02356|Talk2Move]], [[2512.09924|ReViSE]], [[2512.01236|PSR-Image-Gen]] (CVPR'26), [[2509.21953|MultiCrafter]], [[2505.20498|ControlTac]], [[2503.19012|DiffV2IR]], [[2410.13911|GraspDiffusion]], [[2410.04891|LoRA-Continual-Diffusion]] (ICLR'25), [[2206.01714|Composed Diffusion]] (ECCV'22)

> [!star] Key Papers
> - [[2601.02356|Talk2Move]] — RL-based text-instructed geometric transformations with spatially grounded rewards
> - [[2403.19103|PRISM-T2I]] — Automated black-box prompt engineering for T2I models; produces human-interpretable transferable prompts

**Multimodal Hallucination Evaluation** — Surveys, taxonomies, and mitigation of hallucination in generative and understanding directions, spanning both text-to-image and image-to-text models.
- [[2507.22003|ViHallu]], [[2507.19024|Multimodal Hallucination Survey]]

> [!tip] Choosing an Architecture
> For research prototyping, connect a frozen LLM to a diffusion decoder (GILL, MetaQueries). For production unified models, train end-to-end (Emu3.5, UniFluid). For controllable editing, use reward-guided methods (Talk2Move, EditReward).

---

## 2. Discrete Diffusion Language Models

Diffusion is no longer just for images. Masked diffusion models (MDMs) generate text by iteratively unmasking tokens, offering a non-autoregressive alternative to GPT-style LLMs. The LLaDA family proved 8B-parameter diffusion models rival autoregressive models on language benchmarks, sparking a wave of follow-up work on reasoning, alignment, and efficiency.

**Core dLLM Architectures** — Masked diffusion models trained from scratch on text, demonstrating that the denoising paradigm scales to language without autoregressive factorization, including training-free and KV-cache-based decoding acceleration.
- [[2505.22618|Fast-dLLM]] (ICLR'26), [[2505.19223|LLaDA-1.5]], [[2505.16933|LLaDA-V]], [[2502.09992|LLaDA]] (NeurIPS'25 Oral)

> [!star] Key Papers
> - [[2502.09992|LLaDA]] (NeurIPS'25 Oral) — First 8B diffusion LLM competitive with AR models; proved diffusion works for large-scale language modeling and solves the reversal curse
> - [[2505.19223|LLaDA-1.5]] — Variance-Reduced Preference Optimization for aligning masked diffusion models with human preferences
> - [[2505.22618|Fast-dLLM]] (ICLR'26) — Training-free 27.6x throughput improvement via KV cache and confidence-aware parallel decoding

**Reasoning in dLLMs** — Applying RL post-training and chain-of-thought to boost diffusion LLM reasoning on math, code, and planning tasks.
- [[2606.18195|d-OPSD]], [[2509.23653|RemeDi]] (ICLR'26), [[2507.08838|wd1]] (ICLR'26), [[2505.13138|NESYDMS]] (NeurIPS'25), [[2504.12216|d1]] (NeurIPS'25 Spotlight)

> [!star] Key Papers
> - [[2504.12216|d1]] (NeurIPS'25 Spotlight) — First RL post-training framework for dLLMs; introduced diffu-GRPO with +26.2% on Countdown
> - [[2507.08838|wd1]] (ICLR'26) — Weighted policy optimization achieving up to 100% improvement on reasoning benchmarks while eliminating SFT

**Diffusion vs. Autoregression Analysis** — Empirical studies comparing when and why diffusion beats autoregressive generation.
- [[2605.08078|NTM]], [[2507.15857|Diffusion-vs-AR]] (NeurIPS'25), [[2505.15045|DIFFEMBED]], [[2210.15097|Contrastive Decoding]]

> [!star] Key Papers
> - [[2507.15857|Diffusion-vs-AR]] (NeurIPS'25) — Diffusion has 16x better data reuse half-life; dominates AR in data-constrained settings
> - [[2505.15045|DIFFEMBED]] — Diffusion LLMs outperform AR on text embeddings by 20% on long-document retrieval, thanks to bidirectional attention

> [!tip] When to Use Diffusion Over Autoregression
> Diffusion LLMs excel where bidirectional context matters (embeddings, retrieval) and where data is limited. For open-ended generation with abundant data, AR still leads — but the gap is closing fast with LLaDA 1.5 and d1.

---

## 3. Unified Multimodal Models

The hottest design question in generative AI: can one model both understand and generate across text and images? Unified models replace the pipeline of separate encoders, LLMs, and diffusion decoders with a single architecture that handles all modalities natively. The field splits into two camps: token-based (discretize everything) and hybrid (mix AR for text + diffusion for images).

**Hybrid AR + Diffusion** — Use autoregressive generation for text tokens and diffusion for continuous image patches within a single Transformer, avoiding information loss from discretization.
- [[2603.03276|Beyond-LLMs]], [[2503.10631|HybridVLA]] (ICLR'26), [[2501.00289|D-DiT]] (CVPR'25), [[2412.15188|LMFusion]] (NeurIPS'25), [[2412.08635|LatentLM]], [[2408.11039|Transfusion]] (ICLR'25 Oral)

> [!star] Key Papers
> - [[2408.11039|Transfusion]] (ICLR'25 Oral) — Pioneered mixing next-token prediction with diffusion loss in one model; outperformed quantization-based approaches in scaling efficiency
> - [[2412.08635|LatentLM]] — Unified framework for discrete and continuous data via next-token diffusion in latent space

**Token-Based Unified Models** — Discretize images into tokens and treat all modalities uniformly with a single autoregressive or diffusion objective, enabling interleaved multimodal generation; includes surveys taxonomizing the unified-model landscape.
- [[2609.11929|SenseNova-U1.5]], [[2607.06560|SenseNova-Vision]], [[2605.31604|Representation-Forcing]], [[2605.28820|NEO-ov]], [[2605.18678|Lance]], [[2507.23278|UniLiP]] (ICLR'26), [[2506.23044|Ovis-U1]], [[2506.17202|UniFork]], [[2506.15564|Show-o2]] (NeurIPS'25), [[2506.13759|Discrete-Diffusion-LLM-Survey]], [[2506.03147|UniWorld-V1]], [[2505.20147|FUDOKI]] (NeurIPS'25 Spotlight), [[2505.05472|Mogao]], [[2505.02567|Unified-Multimodal-Survey]], [[2504.21356|Nexus-Gen]], [[2501.17811|Janus-Pro]], [[2410.13848|Janus]] (CVPR'25), [[2409.18869|Emu3]], [[2408.12528|Show-o]] (ICLR'25), [[2405.09818|Chameleon]], [[2107.14483|ManiSkill]], [[2104.03311|PlasticineLab]] (ICLR'21 Spotlight), [[2102.12092|DALL-E]] (ICML'21 Spotlight)

> [!star] Key Papers
> - [[2405.09818|Chameleon]] — Meta's early-fusion token-based model; proved full unification is architecturally viable at scale
> - [[2408.12528|Show-o]] (ICLR'25) — Single transformer unifying understanding and generation; later scaled to Show-o2 with native multimodal capabilities
> - [[2409.18869|Emu3]] — Showed next-token prediction alone can handle text, image, and video generation without diffusion
> - [[2506.13759|Discrete-Diffusion-LLM-Survey]] — Systematic overview of dLLMs and dMLLMs; covers up to 10x faster inference vs. AR models
> - [[2501.17811|Janus-Pro]] — DeepSeek's decoupled-visual-encoding unified model; scaled data and model size to match or beat task-specific baselines

**Multimodal Diffusion Architectures** — Extend diffusion beyond images to jointly handle text reasoning, image generation, and multimodal understanding in a single diffusion-native model.
- [[2606.31451|UniTac]] (ECCV'26), [[2605.02641|Mamoda2.5]], [[2604.02097|LatentUM]], [[2511.09611|MMaDA-Parallel]] (ICLR'26), [[2506.23115|MoCa]], [[2506.05340|DiT-Grafting]] (NeurIPS'25 Oral), [[2505.15809|MMaDA]] (NeurIPS'25), [[2505.13031|MindOmni]] (NeurIPS'25)

> [!star] Key Papers
> - [[2505.15809|MMaDA]] (NeurIPS'25) — Unified diffusion model handling text reasoning, image generation, and multimodal understanding simultaneously

**Visual Tokenization** — Learning discrete or compressed visual representations that bridge the gap between continuous images and discrete language model architectures.
- [[2609.07815|Vision-of-Thought]], [[2605.02134|PV-VAE]], [[2603.29634|MacTok]] (CVPR'26), [[2506.08257|TiTok]] (ICML'25), [[2505.07538|Selftok]], [[2505.05422|TokLIP]], [[2412.03069|TokenFlow]] (CVPR'25), [[2406.11838|MAR]] (NeurIPS'24 Spotlight), [[2406.07550|TiTok (32 Tokens Reconstruction)]] (NeurIPS'24), [[2312.02116|GIVT]] (ECCV'24), [[1711.00937|VQ-VAE]] (NeurIPS'17)

> [!star] Key Papers
> - [[2505.07538|Selftok]] — Derives discrete visual tokens from the reverse diffusion process; enables purely discrete VLMs with RL-based visual reasoning
> - [[2506.08257|TiTok]] (ICML'25) — Highly compressed 1D tokenizer that generates images via test-time optimization without a generative model

> [!tip] Token vs. Hybrid
> Token-based models (Chameleon, Show-o) are simpler but lose continuous detail. Hybrid models (Transfusion, LatentLM) preserve image fidelity but add architectural complexity. For production use, token-based is easier to scale; for quality-critical generation, hybrid wins.

---

## 4. Representation Learning & Theory

Foundational work on how diffusion models learn representations, the theoretical underpinnings that unify different formulations, and methods for leveraging diffusion dynamics for pre-training and downstream tasks beyond generation.

**Foundational Generative Model Theory** — Seminal papers establishing the mathematical foundations of denoising diffusion, score-based generative modeling, flow matching, and GAN training stability that underlie the modern generative-modeling landscape.
- [[2210.02747|Flow Matching]] (ICLR'23 Spotlight), [[2010.02502|DDIM]] (ICLR'21), [[2006.11239|DDPM]] (NeurIPS'20), [[1907.05600|NCSN]] (NeurIPS'19), [[1802.05957|SN-GAN]] (ICLR'18)

**Diffusion as Pre-Training** — Use the diffusion denoising objective as a self-supervised pre-training method for representation learning, improving downstream classification, understanding, and robustness tasks.
- [[2609.29350|FBDM]], [[2607.24249|SILICA]], [[2607.09024|GenCeption]] (ECCV'26), [[2607.06856|Gen4U]], [[2607.06553|ReChannel]], [[2604.08121|Uni-ViGU]], [[2602.07588|PVB]] (ICLR'26), [[2512.19693|Prism-Hypothesis]], [[2508.17230|FVP]] (ICCV'25), [[2507.01467|REG]] (NeurIPS'25 Oral), [[2505.06890|RCLDT]], [[2505.02831|SRA]] (ICLR'26), [[2503.06132|USP]] (ICCV'25), [[2410.06940|REPA]] (ICLR'25 Oral), [[2402.11337|Reconstruction vs Perception]], [[2308.06038|DiffTPT]] (ICCV'23), [[2306.09344|DreamSim]] (NeurIPS'23 Spotlight)

> [!star] Key Papers
> - [[2503.06132|USP]] (ICCV'25) — Unified pretraining in VAE latent space that 11.7x accelerates DiT convergence and improves both generation and understanding
> - [[2505.02831|SRA]] (ICLR'26) — Diffusion transformers provide their own representation guidance; eliminates external encoders
> - [[2410.06940|REPA]] (ICLR'25 Oral) — Aligning DiT hidden states with pretrained visual encoders accelerates convergence and improves generation quality
> - [[2402.11337|Reconstruction vs Perception]] — Counterpoint showing pixel-reconstruction objectives alone yield uninformative features for perception, motivating explicit representation-alignment losses like REPA

**Latent Space Design** — Principled methods for learning optimal latent representations that diffusion models operate in, controlling information content and generation quality.
- [[2608.05811|EG-FM]], [[2608.01306|SPAE]], [[2607.21585|EFM]], [[2607.01642|MrFlow]], [[2605.16147|Register Guidance]], [[2604.16044|DCW]] (CVPR'26), [[2602.18993|SeaCache]] (CVPR'26), [[2602.17270|UL]], [[2512.13592|Diffusion-Preview]] (CVPR'26), [[2511.13720|JiT-Denoise-Transformer]], [[2505.13447|MeanFlow]] (NeurIPS'25 Oral), [[2410.12557|Shortcut Models]] (ICLR'25 Oral)

> [!star] Key Papers
> - [[2602.17270|UL]] — Google DeepMind's Unified Latents framework; principled regularization achieves SOTA on ImageNet-512 and Kinetics-600
> - [[2604.16044|DCW]] (CVPR'26) — Characterizes SNR-t bias in DPMs and applies training-free wavelet-domain differential correction; 42.6% FID reduction on CIFAR-10 with 20 steps

**Theoretical Foundations & Surveys** — Monographs, comprehensive surveys, and statistical theory (including recursive training and model collapse) that unify variational, score-based, and flow-based perspectives on diffusion.
- [[2609.18111|GPAI]], [[2604.15911|Efficient-Video-Diffusion-Survey]], [[2511.03032|DADO]] (ICLR'26), [[2510.21890|Diffusion-Models-Principles]], [[2509.26364|Data-to-Energy-Dynamics]] (ICLR'26), [[2506.03719|Flow-Matching-Closed-Form]] (NeurIPS'25 Oral), [[2502.18049|Weighting-Based Stabilization]]

> [!star] Key Papers
> - [[2510.21890|Diffusion-Models-Principles]] — Definitive monograph from Sony AI, OpenAI, and Stanford unifying all diffusion formulations into a continuous-time framework
> - [[2506.19360|Synthetic-Image-Privacy-SoK]] — Empirical evaluation showing diffusion models offer superior utility-privacy tradeoffs for synthetic data

**Privacy, Safety & Red-Teaming of Generators** — Membership inference, red-teaming, adversarial transferability, and privacy evaluation of generative models and the synthetic data they produce.
- [[2607.08402|Pedestrian Privacy Pipeline]], [[2605.27020|SD-MIA]] (CVPR'26 Oral), [[2506.21046|dSVA]] (ICCV'25), [[2506.19360|Synthetic-Image-Privacy-SoK]], [[2506.10047|GenBreak]]

**Generative Sequence Modeling for Perception Tasks** — Cast detection, grounding, segmentation, and dense prediction as sequence generation, emitting boxes, masks, and labels as tokens from a single generative model.
- [[2404.09216|DetCLIPv3]] (CVPR'24), [[2403.10191|GenerateU]] (CVPR'24), [[2401.14159|Grounded SAM]], [[2205.10337|UViM]] (NeurIPS'22), [[2109.10852|Pix2Seq]] (ICLR'22), [[2102.02779|VL-T5]] (ICML'21 Spotlight)

> [!star] Key Papers
> - [[2506.03147|UniWorld-V1]] — Integrates VL understanding, image generation, perception, and grounding in one model

**Generative-Model Signals for OOD & Anomaly Detection** — Use the internals of diffusion or flow-matching models (posterior covariance, reversed-flow vector fields) as distribution-shift signals for unsupervised OOD and anomaly detection.
- [[2608.15748|Dual-Head Flow Matching]], [[2607.27933|accel-FM-Uncertainty]], [[2605.23070|Flow Mismatching]], [[2601.21662|REPVLM]], [[2510.07206|EigenScore]] (ICLR'26), [[2510.01456|SCOPED]] (ICLR'26), [[2508.05461|WT-Flow]], [[2504.07793|RDM]], [[2502.20946|Generative-Uncertainty-Diffusion]], [[1606.01868|Pseudo-Counts]] (NeurIPS'16)

> [!star] Key Papers
> - [[2510.07206|EigenScore]] (ICLR'26) — Jacobian-free posterior-covariance spectrum as an OOD signal; +5% AUROC over best baseline, especially strong in near-OOD
> - [[2605.23070|Flow Mismatching]] — Velocity-discrepancy scoring beats WT-Flow on the same backbone, 91.9 vs 70.2 pixel AUPRO on MVTec-AD; the new best FM-native anomaly detector

**Energy/Flow Iterative Reasoning Substrates** — Use energy minimization, probability-flow integration, or looped recurrence as the iterative computation for reasoning and generation (Sudoku, mazes, ARC-AGI, compositional problems), scaling test-time compute with more iterations.
- [[2609.11801|Looped Flows]], [[2606.29150|FRM]], [[2605.19376|GRAM]], [[2604.09168|ELT]] (ECCV'26), [[2510.20607|Compositional-Energy-Minimization]] (NeurIPS'25 Spotlight), [[2507.02092|EBT]] (ICLR'26 Oral)

> [!tip] Diffusion Representations
> Diffusion pre-training is underexplored but powerful. USP shows a single masked-latent pretraining phase improves both generation and understanding. If you need representations and generation from the same model, start here. For diagnostic use (OOD, anomaly), EigenScore and Flow Mismatching show that the generative model's *internals* — its posterior covariance or velocity mismatch — are informative distribution-shift signals.


---

## 5. RL Alignment for Generative Models

Reinforcement learning is transforming how diffusion and flow-matching models are trained. Instead of relying solely on maximum likelihood, these methods use reward signals (human preference, text-image alignment, task success) to directly optimize generation quality. The paradigm parallels RLHF for LLMs but requires novel algorithms for the continuous, multi-step denoising process.

**Foundational Diffusion Fine-Tuning Methods (RL & Alternatives)** — Seminal methods that established the paradigm of RL/gradient-based fine-tuning of generative models against arbitrary reward functions, predating the GRPO/flow-matching wave.
- [[2407.08737|VADER]], [[2309.17400|DRaFT]] (ICLR'24), [[2305.13301|DDPO]] (ICLR'24), [[1805.11973|MolGAN]] (ICML'18 Workshop)

> [!star] Key Papers
> - [[2305.13301|DDPO]] (ICLR'24) — Reformulated multi-step denoising as an MDP and applied policy gradients; the first principled RL approach to diffusion alignment, outperforming reward-weighted regression across compressibility, aesthetics, and prompt alignment
> - [[2309.17400|DRaFT]] (ICLR'24) — Direct backpropagation of differentiable rewards through the entire sampling chain via LoRA + gradient checkpointing; >200× more sample-efficient than DDPO and the foundation for modern reward-gradient methods

**On-Policy Distillation for Few-Step Diffusion** — Distill multi-step diffusion or flow teachers into few-step students by training on the student's own on-policy rollouts scored or guided by the teacher, instead of fixed offline trajectories.
- [[2608.26872|Self-OPD]], [[2608.03316|Any-OPD]], [[2607.24731|PDM]], [[2607.08766|OPSD-V]], [[2605.15055|DiffusionOPD]], [[2605.13724|AnyFlow]], [[2605.05204|D-OPSD]]

**Flow Matching + RL for Non-VLA Robot Policies** — Apply policy optimization to non-VLA flow-matching and diffusion robot-control policies (manipulation, navigation, offline RL), treating the denoising trajectory as a sequential decision process; RL for flow VLAs lives in section 7.
- [[2608.30378|PAVE]], [[2607.26460|RLMM-Flow]], [[2607.14643|NavCMPO]] (IROS'26), [[2607.10892|ESM]], [[2607.10369|VINE]], [[2607.06262|OTQL]], [[2606.29934|RoamFlow]], [[2606.17551|RQL]], [[2606.03834|SFMDS]], [[2605.30056|CGPO]] (ICML'26), [[2605.27079|TRQAM]], [[2605.12236|TMRL]] (RSS'26), [[2605.03065|OGPO]], [[2603.11470|NFPO]], [[2603.05296|LPS-Flow]] (RSS'26), [[2510.08568|NovaFlow]], [[2507.21053|FPO]] (ICLR'26), [[2502.02538|FQL]] (ICML'25), [[2411.18179|PAD]] (NeurIPS'24), [[2407.15208|Im2Flow2Act]] (CoRL'24)

**Flow Matching + RL for Image/Video Generation** — Apply GRPO-style policy optimization to flow-matching and continuous diffusion models for text-to-image/video alignment, treating the denoising trajectory as a sequential decision process.
- [[2606.11025|Flow-DPPO]], [[2605.26535|RecFM]], [[2605.15458|VideoRLVR]], [[2605.10759|RAM]], [[2605.06507|MARBLE-RL]], [[2605.01663|FAN]] (ICML'26), [[2604.24764|World-R1]] (ICML'26), [[2604.23380|V-GRPO]], [[2604.15311|LeapAlign]] (CVPR'26), [[2604.01421|EgoFlow]] (CVPR'26), [[2603.27866|Wan-R1]], [[2603.26599|VGGRPO]] (ECCV'26), [[2603.23500|UniGRPO]], [[2603.04333|floq]], [[2602.05755|FMPose3D]], [[2511.19965|HiCoGen]], [[2509.06040|BranchGRPO]] (ICLR'26), [[2505.05470|Flow-GRPO]] (NeurIPS'25)

> [!star] Key Papers
> - [[2505.05470|Flow-GRPO]] (NeurIPS'25) — First framework adapting GRPO to flow matching; enables online RL for continuous generative models
> - [[2509.06040|BranchGRPO]] (ICLR'26) — Tree-structured branching yields 4.7x training speedup and 16% better alignment over vanilla GRPO

**Inference-Time Alignment & Steering** — Training-free methods that align pre-trained diffusion models with arbitrary rewards at sampling time using particle systems, SMC, beam search, or interacting particle resampling — preserving diversity and avoiding fine-tuning costs.
- [[2607.14280|DiMaS]], [[2607.10781|Training-Free Norm Injection]], [[2607.07076|PriGo]], [[2606.31132|ELASTIC]], [[2601.20239|TouchGuide]] (RSS'26), [[2511.14178|VLA-Pilot]], [[2509.00271|HAVE]] (CoRL'25), [[2508.03645|DiWA]] (CoRL'25), [[2505.23614|Diffusion-Search-Scaling]] (ICLR'26), [[2503.18942|Video-T1]] (ICCV'25), [[2503.02039|DSearch]], [[2501.06848|FK-Steering]] (ICML'25), [[2501.05803|DAS]] (ICLR'25 Spotlight), [[2408.08252|SVDD]] (NeurIPS'25), [[2304.12824|CEP]] (ICML'23)

> [!star] Key Papers
> - [[2503.02039|DSearch]] — Gradient-free dynamic beam search with Monte Carlo look-ahead for inference-time alignment; achieves 35% faster reward-per-second scaling and superior naturalness over SVDD across image, DNA, and molecule domains
> - [[2501.06848|FK-Steering]] (ICML'25) — Feynman-Kac Interacting Particle Systems for steering diffusion at inference; enables a 0.8B Stable Diffusion to beat a 2.6B fine-tuned SDXL-DPO and works for both continuous and discrete state spaces
> - [[2408.08252|SVDD]] (NeurIPS'25) — Foundational derivative-free inference-time guidance via soft-value MDP formulation; the reference baseline that DSearch and later beam-search methods build on

**Self-Improving World Models & Embodied Policies** — Self-improvement loops for world/simulation models and embodied robot policies via generated rollouts, multi-agent interaction, or self-distillation, without fresh human annotation.
- [[2609.03681|WISE]], [[2608.30237|Motus2]], [[2605.30347|NeuROK]] (CVPR'26), [[2603.19370|VAMPO]]

**Self-Improving Image/Video Generation** — Self-improvement of image/video generation quality via reward feedback, cycle-consistency, or model merging, without fresh human annotation.
- [[2604.28190|FD-loss]], [[2603.17051|Astrolabe]], [[2512.08269|EgoX]], [[2508.16204|M2N2]], [[2506.02095|CycleReward]] (ICCV'25), [[2505.23380|UniRL]]

> [!star] Key Papers
> - [[2505.23380|UniRL]] — Unified self-improving post-training for both diffusion and flow models
> - [[2506.02095|CycleReward]] (ICCV'25) — Self-supervised reward via cycle consistency; eliminates need for human preference data
> - [[2603.17051|Astrolabe]] — Forward-process RL with rolling-KV streaming rollouts for distilled autoregressive video models; aligns long-video generation (30–60s) without sacrificing inference speed, and prevents reward hacking via uncertainty-aware selective KL

**Reward Models for Image Generation** — Learning reward functions that capture human preferences for image quality, text-image alignment, or edit fidelity to guide RL training.
- [[2604.27505|Edit-R1]], [[2604.11626|RationalRewards]], [[2601.04153|Diffusion-DRF]], [[2509.26346|EditReward]] (ICLR'26)

> [!star] Key Papers
> - [[2509.26346|EditReward]] (ICLR'26) — Human-aligned reward model for instruction-guided image editing; enables curation of high-quality training data
> - [[2507.22003|ViHallu]] — Vision-centric framework reducing hallucinations in LVLMs by up to 5.9% via generated visual variations

> [!success] RL Post-Training for Generative Models
> ==Likelihood pre-training== (diffusion or flow) → ==RL post-training== with reward model. Flow-matching models benefit from GRPO-adapted policy optimization; tree-structured branching yields 4–5x training speedup; cycle-consistency provides self-supervised rewards without human annotation.

> [!tip] RL for Generation
> The recipe: train a base generative model (diffusion or flow) with likelihood, then post-train with RL using a reward model. Flow-GRPO for flow matching, BranchGRPO for efficiency at scale. CycleReward eliminates the human annotation bottleneck.

---

## 6. Chain-of-Thought and Reasoning in Generation

A new paradigm: generative models that "think before they draw." Instead of generating images in a single pass, these models decompose generation into reasoning steps — planning layouts, predicting semantic structure, or generating intermediate visual states. The insight is that CoT, which transformed language reasoning, can similarly improve visual generation quality and controllability.

**CoT for Image Generation** — Autoregressive image generators that plan generation via chain-of-thought at the semantic or token level before producing final output.
- [[2602.12279|UniT]] (CVPR'26), [[2512.23568|ThinkGen]] (CVPR'26), [[2511.16671|TWIG]], [[2506.03596|ControlThinker]], [[2505.00703|T2I-R1]] (NeurIPS'25), [[2503.10639|GoT]], [[2501.13926|CoT-Image-Generation]]

> [!star] Key Papers
> - [[2501.13926|CoT-Image-Generation]] — First comprehensive study of CoT for AR image generation; +24% over Show-o baseline, surpasses Stable Diffusion 3
> - [[2505.00703|T2I-R1]] (NeurIPS'25) — Bi-level CoT (semantic + token) with RL; excels on complex, reasoning-intensive prompts
> - [[2503.10639|GoT]] — Integrates MLLM reasoning into visual generation and editing via a unified framework

**Visual Reasoning with Generated Images** — Use generated images as intermediate reasoning artifacts, enabling models to "think" in visual space rather than text.
- [[2607.21072|ProVisE]], [[2607.15278|HDR]], [[2607.14187|RxBrain]], [[2607.12800|UniVR]], [[2606.03988|Imaginative-Perception-Tokens]], [[2603.16870|Video-Reasoning-Chain-of-Steps]], [[2602.10675|TwiFF]], [[2601.21037|Thinking-in-Frames]], [[2601.02771|AbductiveMLLM]], [[2509.20328|Chain-of-Frames]], [[2505.22525|TwGI]], [[2505.19094|SATORI]], [[2312.08762|DPMM-CoT]]

> [!star] Key Papers
> - [[2505.22525|TwGI]] — Models generate images as intermediate reasoning steps; proves visual thinking complements textual CoT
> - [[2601.21037|Thinking-in-Frames]] — Video generators as visual reasoners; discovers "Visual Test-Time Scaling" where more frames improve OOD performance

> [!tip] Visual Chain-of-Thought
> The pattern is clear: generation quality improves when models plan first. For T2I, use semantic CoT (T2I-R1). For spatial reasoning, generate intermediate frames (TwGI). This parallels the thinking-before-acting paradigm in VLAs.

---

## 7. Diffusion for Robotics and Planning

Diffusion models applied to physical action generation rather than image synthesis. These methods treat robot trajectories, action sequences, or video predictions as data to denoise, enabling smooth multi-step planning that handles multimodal action distributions better than regression.

**Navigation & Mobile Diffusion Planning** — Diffusion and flow-matching models for visual and safety-critical navigation, treating navigation actions or safety margins as data to denoise.
- [[2607.28560|X-NavDP]], [[2607.26817|CF²Loc]], [[2607.20785|Robostral Navigate]], [[2607.18200|Adaptive Safety Critic for Visual Navigation]], [[2607.12965|MAMMOTH]] (IROS'26), [[2607.10288|PIER-Flow]], [[2607.08359|FSD-VLN]], [[2606.31654|DynFly]], [[2606.03512|SPADE]], [[2605.25685|HumanFlow]] (RSS'26), [[2604.00416|EgoNav]], [[2603.16368|SCDP]], [[2602.00923|SanD-Planner]] (RSS'26), [[2508.03027|CogniPlan]] (CoRL'25), [[2505.07261|CHD]] (CoRL'25), [[2410.16687|DARE (Diffusion Robot Exploration)]], [[2307.15644|ScaleVLN]], [[2306.14846|ViNT]] (CoRL'23)

**Foundational Diffusion & Flow Planning (Classic Methods)** — The paradigm-establishing methods that first treated robot trajectories and action sequences as data to denoise or generate via video/flow models.
- [[2409.16283|Gen2Act]] (CoRL'25), [[2407.05530|This&That]], [[2407.01903|TADPoLe]] (NeurIPS'24), [[2407.01573|MBD]] (NeurIPS'24), [[2403.12861|D-Cubed]] (CoRL'25), [[2303.04137|Diffusion-Policy]] (RSS'23), [[2302.01877|AdaptDiffuser]] (ICML'23 Oral), [[2302.00111|UniPi]] (NeurIPS'23 Spotlight), [[2210.15629|LCD]] (ICLR'24), [[2208.06193|Diffusion-QL]] (ICLR'23), [[2205.09991|Diffuser]] (ICML'22 Oral), [[2106.01345|Decision Transformer]] (NeurIPS'21), [[1903.01973|Play-LMP]] (CoRL'19), [[1707.02920|RoboInstruct-2]] (ICRA'18)

> [!star] Key Papers
> - [[2205.09991|Diffuser]] (ICML'22 Oral) — First to use denoising diffusion for RL planning; treat trajectories as data to denoise
> - [[2303.04137|Diffusion-Policy]] (RSS'23) — Extended Diffuser to visuomotor control; became the standard for robot action generation
> - [[2302.00111|UniPi]] (NeurIPS'23 Spotlight) — Universal policy as text-conditioned video generation; crosses the boundary between video models and robot control

**Generalist & Scaled Diffusion/Flow Manipulation Policies** — Large pretrained, multi-task diffusion/flow manipulation backbones that scale the foundational paradigm to generalist robot control.
- [[2503.14734|GR00T-N1]], [[2411.19650|CogACT]], [[2410.24091|3D-ViTac]] (CoRL'24), [[2410.15959|DiT-Policy]], [[2410.07864|RDT-1B]] (ICLR'25), [[2408.14368|GR-MG]], [[2407.05996|MDT]] (RSS'24), [[2405.12213|Octo]] (RSS'24), [[2403.03954|DP3]] (RSS'24), [[2403.03181|VQ-BeT]] (ICML'24 Spotlight)

**Reinforcement-Learning & Constraint-Aware Diffusion Planning** — Diffusion planners trained or corrected with RL, curiosity, or safety-critical objectives, including model-based planners that enforce hard safety and dynamic-feasibility constraints during denoising via CBF/CLF projections, augmented Lagrangian optimization, and MPC integration, plus video-diffusion reward models and diffusion locomotion priors refined by residual RL.
- [[2607.14455|MD-COAS]], [[2607.12423|MDOC]] (RSS'26), [[2607.10842|D-SafeMPC]], [[2607.01111|FAR]], [[2606.31562|Stabilization Learning]], [[2606.30362|ReactiveBFM]], [[2606.19656|DF-ExpEnse]] (ICML'26), [[2606.06049|L-SDPPO]], [[2604.19730|FASTER]], [[2604.10953|DRL-3DBP]], [[2604.00202|DreamControl-v2]], [[2603.27670|ProgressVLA]], [[2603.13707|REFINE-DP]], [[2509.08775|JM2D]] (CoRL'25), [[2509.08160|DG-MAP]] (CoRL'25), [[2508.21375|Super-Nominal Payload Diffusion]] (CoRL'25), [[2508.21001|DiTree]] (CoRL'25), [[2508.18268|SafeBimanual]] (CoRL'25), [[2508.12166|B-COD]] (CoRL'25), [[2506.11470|Multi-Loco]] (CoRL'25), [[2505.13131|CoDiG]] (CoRL'25), [[2505.12934|DiffusiveGRAIN]] (CoRL'25), [[2504.08661|SafeFlow-CBF]], [[2503.14833|Curiosity-Diffuser]], [[2503.00653|DC-MPC]] (ICLR'25), [[2502.02316|DIME-RL]] (ICML'25), [[2412.10349|SafeDiff]] (CoRL'25), [[2312.14134|Diffusion Reward]] (ECCV'24)

**Imitation-Learning-Based Manipulation Diffusion Policies · Part 1 (2607)** — Diffusion and flow-matching manipulation policies trained via imitation learning from demonstrations, the largest and most common family of robot diffusion policies; split by month for length, newest batch first.
- [[2609.28281|BrickCraft-Duo]], [[2607.28596|FA-RDP]], [[2607.27890|SIDO]], [[2607.24296|PAC-DP]], [[2607.23108|Curse of Precision]] (ICRA'26), [[2607.21049|GuidedAttention]], [[2607.20912|URF]], [[2607.20033|HOST]], [[2607.14424|ConFlow]] (RSS'26 Workshop), [[2607.14021|IDB]], [[2607.13455|Auto-E2H]], [[2607.11884|MoF Policy]], [[2607.11027|SegDiff]], [[2607.10625|DASL]], [[2607.10206|SL-FM]], [[2607.07101|GeoProp]], [[2607.05780|FORGE]], [[2607.01684|TacImag]]

**Imitation-Learning-Based Manipulation Diffusion Policies · Part 2 (2606 and earlier)** — Continuation of the same family; older half of the list.
- [[2606.31493|ChronoFlow-Policy]], [[2606.30457|Behavior Prompting Policy]], [[2606.30318|Chronos]], [[2606.29201|MoRE]], [[2606.29028|Keypose Exploration]] (IROS'26), [[2606.28939|ReGuide]], [[2606.28813|Human2Any]], [[2606.01865|SDP]] (RSS'26), [[2605.14598|DSSP]], [[2605.10051|SSIP]] (RSS'26), [[2604.01224|SoftAct]] (RSS'26), [[2603.03243|HoMMI]] (RSS'26), [[2511.04671|X-Diffusion]] (ICRA'26), [[2509.22652|DAWN]] (CVPR'26), [[2509.19712|TopoCut]] (CoRL'25), [[2509.19292|SOE]], [[2509.10952|ImMimic]] (CoRL'25), [[2508.21501|Neuro-Symbolic IL]] (CoRL'25), [[2508.10511|KDPE]] (CoRL'25), [[2506.14769|CDP]] (CoRL'25), [[2505.09561|PTP]] (CoRL'25), [[2504.04612|Tool-as-Interface]] (CoRL'25), [[2503.15386|CCDP]], [[2503.03081|AirExo-2]] (CoRL'25), [[2502.10040|DTP]], [[2501.14400|SKIL]] (RSS'25), [[2501.05420|RoboPanoptes]] (RSS'25), [[2410.12124|OAF]] (CoRL'25)

**VLA-Based Manipulation Diffusion Policies** — Vision-language-action models that wrap diffusion action heads with language/vision grounding for instruction-following manipulation.
- [[2609.22895|H-VLA]], [[2607.26807|KinRT]], [[2607.07608|LaMem-VLA]], [[2605.25044|X-DiffVLA]] (RSS'26), [[2604.03191|Compression-Gap]], [[2603.25406|MMaDA-VLA]], [[2603.12263|Psi0]], [[2603.10052|OmniGuide]], [[2602.11236|ABot-M0]], [[2601.07060|PALM]] (CVPR'26), [[2601.02456|InternVLA-A1]], [[2512.21430|EVE]], [[2508.20072|Discrete-Diffusion-VLA]] (ICML'26), [[2508.10333|ReconVLA]], [[2506.16652|CodeDiffuser]] (RSS'25), [[2503.19757|Dita]] (ICCV'25)

**General Diffusion/Flow Manipulation Architectures · Part 1 (2607 and later)** — Architectural and representational variations on diffusion/flow manipulation policies (memory, latent structure, efficiency, sim-to-real) that don't fall cleanly into the IL, RL, or VLA families above; split by month for length, newest batch first.
- [[2609.30127|RMFP]], [[2609.27513|BAAT]], [[2609.25322|JAMB]], [[2609.24068|VWT-Attn]], [[2609.16586|ProxiDex]], [[2609.03715|MINERVA]], [[2608.30880|Zeva]], [[2608.29516|TR-FDF]], [[2607.27138|DLAM]], [[2607.26770|Vision-TL-Action]], [[2607.24538|NEO]], [[2607.21341|BiCompoDiff]] (IROS'26), [[2607.14725|BridgeFlow]] (IROS'26), [[2607.11031|GraspGraphNet]], [[2607.04739|Spatial Attention]], [[2607.04714|GeoMoLa]], [[2607.04554|HUGS]], [[2607.01166|Structured 4D Latent]]

**General Diffusion/Flow Manipulation Architectures · Part 2 (2606 and earlier)** — Continuation of the same family; older half of the list.
- [[2605.25537|Soft-RTC]], [[2605.23477|SMoDP]] (RSS'26), [[2605.13428|SID]] (RSS'26), [[2604.18933|Gated-Memory-Policy]], [[2604.13645|CFG-ADDA]], [[2604.03181|MV-VDP]], [[2603.27012|UMI-Underwater]] (RSS'26), [[2603.15975|UMO]], [[2601.08246|FSAG]], [[2512.22688|ARFM]], [[2511.04812|MDF]], [[2510.09459|FIPER]] (NeurIPS'25), [[2509.19696|Diffusion-Impedance-Learning]], [[2508.08269|emg2tendon]] (RSS'25), [[2506.22007|RoboEnvision]] (IROS'25), [[2506.06196|Mid-Level MoE]] (RSS'25), [[2505.16892|FlashBack]] (CoRL'25), [[2505.09144|LatentToM]] (CoRL'25), [[2504.18792|STDArm]] (RSS'25), [[2504.00342|Constraint-Aligned-Diffusion]], [[2502.16707|ReflectVLM]] (CoRL'25)

**Diffusion-Based Object Pose Estimation & Generation** — Diffusion and energy-based generative models that estimate real-world object poses (visual, tactile) or generate/predict novel object placement, stacking, and dexterous grasp poses (including physics-simulation-refined grasp datasets), providing precise spatial grounding for downstream robotic manipulation rather than generating full action trajectories directly.
- [[2602.15201|DexEvolve]] (RSS'26), [[2509.15934|UniTac2Pose]] (CoRL'25), [[2509.07978|OnePoseViaGen]] (CoRL'25), [[2508.15972|UnPose]] (CoRL'25), [[2508.02093|StackItUp]] (CoRL'25), [[2504.18829|Dexonomy]] (RSS'25), [[2502.04531|AnyPlace]] (CoRL'25), [[2407.15161|FFHFlow]] (CoRL'25)

**Diffusion/Flow Planning for Autonomous Driving** — Generative trajectory and behavior-latent methods for traffic simulation and intersection coordination, applying diffusion or flow matching to multi-agent driving scenarios rather than single-robot manipulation.
- [[2609.02252|DiffuSearch]], [[2608.07468|SimWAM]], [[2607.15898|Orbis 2]], [[2607.14507|DRIFT]], [[2607.06957|Flow-ERD]], [[2607.02496|CNeVA]], [[2606.30940|Compressed Latent Motion Planning]], [[2606.30694|DSIP]], [[2606.03296|SC-Diff-Planning]], [[2604.26065|FlowS]], [[2604.11734|Multi-ORFT]], [[2407.21126|LOPR]] (RSS'25), [[2311.16038|OccWorld]] (ECCV'24)

**Efficient & Accelerated Flow VLA Policies** — Vision-language-action models using flow matching for continuous action generation, specifically optimized for inference speed via caching, token reuse, or efficient architectures.
- [[2609.29382|Exit Transformers]], [[2609.22854|SmoLSTM]], [[2609.20776|GeoAAC]], [[2608.29749|DriftingVLA]], [[2608.29208|AdaVLA]], [[2607.26055|πR²]], [[2607.14695|Reflex]] (ICML'26), [[2607.12287|Temporal Token Reuse]], [[2607.10504|SUREFlow]], [[2607.08575|FabriVLA]], [[2607.06370|ActionCache]], [[2607.04609|SEAM]], [[2606.29936|OpenSPM]], [[2606.21372|NAC]], [[2606.05737|One-Step-VLA]], [[2605.21854|CrossVLA]], [[2604.05672|A1]], [[2604.05656|SnapFlow]], [[2603.28565|StreamingVLA]], [[2603.24800|Calibri]], [[2602.18397|VLA-Perf]], [[2602.12978|Legato]] (RSS'26), [[2602.01166|LaRA-VLA]] (ICML'26)

**RL & Preference-Optimized Flow VLA Policies** — Flow-matching VLA policies trained or refined with reinforcement learning or preference optimization on top of the base flow-matching action head.
- [[2609.28838|Uncertainty-Gated Exploration Noise]], [[2609.06114|DLS]], [[2607.27782|RedFlow]], [[2607.02092|Guided Action Flow]], [[2606.31846|Z-1]], [[2606.05468|FlowPRO]], [[2606.04968|ForesightFlow]], [[2605.13959|WarmPrior]], [[2604.10962|ScoRe-Flow]], [[2602.02481|FPO++]], [[2602.01789|RFS]] (ICLR'26), [[2601.20218|DenseGRPO]] (ICLR'26), [[2511.14759|RECAP]], [[2511.01718|UD-VLA]], [[2510.25889|piRL]], [[2510.02654|Smart-GRPO]], [[2509.04063|ARFM]], [[2505.22094|ReinFlow]] (NeurIPS'25), [[2504.18471|AFM]]

**Flagship & Scaled Flow VLA Models** — Widely-adopted, generalist flow-matching VLA backbones that established or scaled flow matching as the standard for VLA action generation.
- [[2609.03591|XR-2]], [[2608.30289|CometVLA]], [[2601.18692|LingBot-VLA]], [[2512.24125|GenieReasoner]], [[2510.22201|ACG]] (ICRA'26), [[2510.10274|X-VLA]] (ICLR'26), [[2509.19958|MotoVLA]] (CoRL'25), [[2509.04996|FLOWER]] (CoRL'25), [[2508.21112|EO-1]], [[2507.23682|villa-X]] (ICLR'26), [[2506.01844|SmolVLA]], [[2410.24164|π0]] (RSS'25), [[2403.09631|3D-VLA]] (ICML'24)

> [!star] Key Papers
> - [[2410.24164|pi0]] (RSS'25) — Vision-language-action flow model for general robot control; established flow matching as the standard for VLA action generation
> - [[2506.01844|SmolVLA]] — Affordable and efficient VLA via flow matching; democratized robot learning with minimal compute requirements
> - [[2509.04996|FLOWER]] (CoRL'25) — Generalist flow-based VLA policy enabling broad robot skill transfer across embodiments

**Specialized & Task-Variant Flow VLA Policies** — Flow-matching VLA policies specialized for a particular embodiment, sensing modality, safety property, or task variant (dexterous grasping, tactile/soft-robot control, humanoid, pose estimation, world-model augmentation).
- [[2609.25558|GC-VLA]], [[2609.16641|SAVLA]], [[2607.20207|SeededGrasp]], [[2607.15275|RoboTTT]], [[2607.11018|Soft-Trunk Flow Matching]], [[2607.08283|TFP]] (RSS'26 Workshop), [[2607.06655|Pelican-VLA 0.5]], [[2607.04988|InternVLA-A1.5]], [[2607.04927|DSWAM]], [[2607.04816|CAC-VLA]], [[2607.04171|XS-VLA]], [[2607.02503|VT-WAM]], [[2607.02417|LIME]], [[2607.01804|VLA-Corrector]], [[2607.01586|VLAFlow]], [[2607.01378|Neuro-Symbolic VLA Safety]], [[2606.12366|APT-VLA]], [[2605.14417|DAJI]], [[2605.13403|RotVLA]], [[2604.07084|FMP]], [[2604.04646|FDS]] (ECCV'26), [[2604.02759|OMNI-PoseX]], [[2603.29844|DIAL]], [[2603.26320|DFM-VLA]], [[2603.01549|Pri4R]], [[2512.21970|StereoVLA]] (RSS'26), [[2511.14148|AsyncVLA]], [[2511.07732|ViPRA]] (ICLR'26)

**Manipulation-Focused Robot World Models · Part 1 (2607 and later)** — Video-diffusion world models adapted specifically to manipulation tasks, using generated future video as a physics simulator for grasping and tabletop manipulation; split by month for length, newest batch first.
- [[2609.30247|Rolling-WAM]], [[2609.28339|NowWAM]], [[2609.24868|DualWAM]], [[2609.15570|DIDO]], [[2609.02531|SA-WAM]], [[2609.00161|IMPACT-WM]], [[2608.29242|AnyWorld]], [[2607.27511|FoMo-FD]], [[2607.26579|ContactFlow]], [[2607.24159|DeVA]], [[2607.23909|WorldDiT]], [[2607.15065|DriftWorld]], [[2607.13017|FlowWAM]], [[2607.08639|LingBot-VA 2.0]], [[2607.06018|RoboTALES]] (ECCV'26), [[2607.04652|KAM-WM]]

**Manipulation-Focused Robot World Models · Part 2 (2606 and earlier)** — Continuation of the same family; older half of the list.
- [[2606.32028|DVG-WM]], [[2606.29501|A2World]] (ECCV'26), [[2606.05645|Discrete-WAM]], [[2606.01027|τ0-WM]], [[2605.06388|Semantic-LDM-WM]], [[2605.06192|EA-WM]], [[2602.20057|AdaWorldPolicy]], [[2601.21998|LingBot-VA]] (RSS'26), [[2601.16163|Cosmos-Policy]] (ICLR'26), [[2512.15692|mimic-video]] (RSS'26), [[2510.10125|CTRL-WORLD]] (ICLR'26), [[2508.00795|Video-Policy]], [[2507.12898|Vidar]], [[2506.06199|3DFlowAction]], [[2504.02792|UWM]] (RSS'25), [[2503.00200|UVA]] (RSS'25), [[2502.00622|GPC]], [[2412.14803|VPP]] (ICML'25 Spotlight), [[2406.13301|ARDuP]] (IROS'24)

**Visuo-Tactile World Models** — Action-conditioned world models that jointly predict future vision and touch alongside robot actions, treating tactile sensing as a first-class modality for contact-rich manipulation.
- [[2609.20761|Agile-WAM]], [[2608.19574|HiTac-WAM]], [[2607.28391|TacWAM]], [[2607.24267|FeelWorld]], [[2607.23783|N0-TWAM]], [[2607.22530|ViTacWorld]]

**Code-Based World Models for Planning** — World models that synthesize executable code (rather than pixels or latent video) as the dynamics representation, letting a planner select and optimize over qualitatively correct, explicitly-structured transition functions.
- [[2608.27549|Code-as-World]], [[2607.25236|VisualPatchWorld]]

**General-Purpose & Interactive Robot World-Model Simulators** — Robot-oriented video world models used as general-purpose interactive simulators or imagination engines, not tied to a specific manipulation policy.
- [[2609.25627|MachEmbodied-U0]], [[2607.19191|ABot-World-0]], [[2607.14997|AeroAct]], [[2607.11643|Xiaomi-Robotics-U0]], [[2607.04978|Qantara]], [[2606.29908|SWAM]] (ECCV'26), [[2606.28804|ViPSim]], [[2606.16533|Kairos-WM]], [[2605.22123|FLORA]], [[2604.18564|MultiWorld]], [[2510.19430|GigaBrain-0]], [[2507.13340|LPS-WM]], [[2504.15369|Inverse-Probabilistic-Adaptation]] (ICLR'25), [[2502.01784|VILP]], [[2501.03575|Cosmos]], [[2310.06114|UniSim]] (ICLR'24 Oral)

**Policy-Integrated & Persistent Robot World Models** — Robot world models designed to feed directly into a control policy or to maintain persistent, long-horizon scene memory across rollouts.
- [[2609.18430|StrucPhysVideo]], [[2607.23969|LeapBot-WA]], [[2606.27677|DiM-WAM]], [[2604.09330|VAG]], [[2603.25685|Persistent-Robot-World-Models]], [[2603.23376|ABot-PhysWorld]], [[2603.17240|GigaWorld-Policy]], [[2603.12639|RoboStereo]], [[2603.10448|DiT4DiT]], [[2603.07799|MWM]], [[2602.15922|DreamZero]], [[2602.10098|VLA-JEPA]], [[2602.06949|DreamDojo]], [[2601.20540|LingBot-World]], [[2512.13644|DexWM]], [[2512.10675|Veo-Robotics]]

**Game & Interactive World Models** — Video-diffusion world models trained on game or agent-interaction data, generating controllable, playable environments rather than robot-task video.
- [[2609.10540|PWM]], [[2608.07408|WorldTrace]], [[2607.07675|LingBot-Video]], [[2607.07534|LingBot-World-Infinity]], [[2607.06559|RynnWorld-4D]], [[2607.06291|AlayaWorld]], [[2607.06216|MoWorld]], [[2606.31734|MemLearner]] (ECCV'26), [[2605.28816|Gamma-World]], [[2605.22718|WorldKV]], [[2604.08995|Matrix-Game-3.0]], [[2512.14614|WorldPlay]], [[2510.00855|DyVA]], [[2507.17744|Yume]], [[2506.18701|Matrix-Game]], [[2506.09995|PlayerOne]] (NeurIPS'25 Oral), [[2501.08325|GameFactory]] (ICCV'25 Highlight), [[2412.03568|The-Matrix]] (NeurIPS'25), [[2411.00769|GameGen-X]] (ICLR'25), [[2402.15391|Genie]] (ICML'24 Oral), [[2203.01914|Playable-Environments]], [[2101.12195|CADDY]] (CVPR'21)

**General-Purpose & Driving Video World Models** — Video-diffusion world models for general-purpose or autonomous-driving simulation, outside the robot-manipulation and game-interaction lines above.
- [[2607.04546|Mask2Real-WM]], [[2606.03159|OmniDreams]], [[2606.02800|Cosmos-3]], [[2605.23993|Nano-World-Models]], [[2605.15178|SANA-WM]], [[2605.08567|ACWM-Phys]], [[2604.14732|WVA]], [[2603.30045|OmniRoam]], [[2603.28963|AutoWorld]], [[2603.28887|OccSim]], [[2603.25716|HyDRA]], [[2603.17117|MosaicMem]], [[2512.11061|VDAWorld]], [[2508.02512|QuaDreamer]] (CoRL'25), [[2504.12369|WorldMem]] (NeurIPS'25), [[2502.20694|WorldModelBench]] (NeurIPS'25), [[2411.08380|EgoVid-5M]], [[2409.18964|PhysGen]] (ECCV'24), [[2403.06845|DriveDreamer-2]], [[1809.01999|World Models]], [[1507.08750|Action-Conditional-Video-Prediction]] (NeurIPS'15)

> [!star] Key Papers
> - [[2512.13644|DexWM]] — Leverages human video data for dexterous manipulation; 83% zero-shot success without real-world training
> - [[2504.15369|Inverse-Probabilistic-Adaptation]] (ICLR'25) — Adapts internet video models to robot tasks; 3x improvement over unadapted models

**Scene & World Spatial Reconstruction** — Diffusion models that reconstruct or generate 3D-consistent scenes and leverage implicit 3D priors for embodied spatial understanding.
- [[2608.24212|NeoWorld-Pro]], [[2608.07012|Executable Scene Programs]], [[2607.10879|BRO Scene Graph Prediction]] (IROS'26), [[2607.04144|Semantic-Guided Object Removal]], [[2607.01962|NeoMap]] (ECCV'26), [[2606.01869|WorldCoder-Bench]], [[2605.11367|3D-Belief]], [[2605.05163|PhysForge]] (ICML'26), [[2605.01799|Embody4D]], [[2605.00781|Map2World]], [[2604.27106|RecGen]], [[2604.26341|SpatialFusion]], [[2604.15805|WorldComposer]], [[2604.14268|HY-World-2.0]], [[2604.13036|Lyra-2.0]], [[2604.02329|Generative-World-Renderer]], [[2603.29089|WorldFlow3D]], [[2603.19235|VEGA-3D]] (ECCV'26), [[2512.13683|I-Scene]], [[2505.04831|Steerable Scene Generation]] (CoRL'25)

> [!star] Key Papers
> - [[2603.19235|VEGA-3D]] (ECCV'26) — Extracts implicit 3D geometric cues from video diffusion for spatial understanding in MLLMs

**3D Object & Asset Generation** — Diffusion and Gaussian-splatting/NeRF methods that generate or reconstruct individual 3D objects and assets, plus benchmarks for 3D generation quality.
- [[2609.05416|WorldSculpt]], [[2607.16805|Scene-SAM3D]], [[2607.05373|PixWorld]], [[2607.01803|PixGS]] (ECCV'26), [[2605.21572|PhysX-Omni]], [[2603.22275|GLD]], [[2603.18524|3DreamBooth]], [[2602.15989|SAM-3D-Body]], [[2602.15727|LoRWeB]] (ECCV'26), [[2601.16148|ActionMesh]] (CVPR'26), [[2511.16624|SAM-3D]] (CVPR'26 Oral), [[2510.08575|ReSplat]] (ECCV'26 Spotlight), [[2503.21745|3DGen-Bench]], [[2503.14489|SEVA]] (ICCV'25), [[2501.12202|Hunyuan3D]], [[2412.01506|TRELLIS]] (CVPR'25), [[2406.04316|Omni6DPose]] (ECCV'24), [[2404.07191|InstantMesh]], [[2209.14988|DreamFusion]] (ICLR'23 Oral)

**Whole-Body Humanoid World-Action Models** — World-action models extended from tabletop/arm manipulation to full bipedal humanoid loco-manipulation, coordinating body locomotion with hand and arm manipulation through shared video-action-motion diffusion/flow backbones.
- [[2609.22829|WB-UMI]], [[2609.18197|Motion-Prior WholeBodyWAM]], [[2609.16644|WBC-Grounded WholeBodyWAM]]

**Structured & Feature-Space World-Action Models** — World-action models that predict compact structured targets — point tracks, semantic features, keypoints, or contact vertices — instead of dense pixel video, trading full visual fidelity for compute efficiency or out-of-distribution generalization.
- [[2609.28811|DeltaWAM]], [[2609.27455|LeWAM]], [[2609.25961|PatchWAM]], [[2609.20709|MoWAM]], [[2609.19600|WorldContact]], [[2609.19142|PointZero]], [[2609.18462|CSWAM]], [[2609.17524|ModAR]]

**Additional methods** — Diffusion applications to robotics outside the families above, such as generating robot morphologies jointly with their control policies.
- [[2607.25798|Transformer Transformer]]

> [!tip] Diffusion Beyond Images
> The same denoising framework that generates images also generates robot actions (Diffusion Policy), plans trajectories (Diffuser), and simulates physics (DexWM). If your problem involves generating structured sequences with multimodal distributions, diffusion is likely the right tool.

---

## 8. Physics-Aware Training for Generative Models

A focused thread on injecting physical laws into generative pipelines. Standard diffusion and flow models learn from pixels alone, so they reliably violate gravity, conservation, and rigid-body constraints — limiting their use as world simulators for robotics, scientific computing, and embodied AI. Methods in this section span four mechanisms: (1) **physics-grounded training data** with synthetic simulators, (2) **physics-conditioned architectures** that consume material/force inputs, (3) **physics losses** (PDE residuals, kinematic residuals, mass conservation) backpropagated during fine-tuning, and (4) **inference-time physics rewards** from latent world models or rule-based proxies.

**3D & Material Physics-Conditioned Generation** — Generative models that consume explicit physical inputs (material properties, forces, rigid-body parameters) grounded in an explicit 3D or point-trajectory representation.
- [[2607.13586|UniPhysGen]], [[2605.20290|TelePhysics]], [[2605.09216|TDCR Flow Matching]] (RSS'26), [[2605.08279|LaWM]], [[2603.13770|PhysAlign]], [[2603.09668|DiffWind]] (ICLR'26), [[2510.22975|VoMP]] (ICLR'26), [[2509.21541|ControlHair]] (ECCV'26), [[2509.20358|PhysCtrl]] (NeurIPS'25), [[2509.07920|ScoreHOI]] (ICCV'25), [[2507.04192|JAX-MPM]], [[2503.21442|RainyGS]] (CVPR'25)

**Video/Image Physics-Conditioned Generation** — Generative models that consume physical inputs or reconstruct physical scenes directly in pixel/video space, without an explicit 3D intermediate representation.
- [[2607.20683|FELT]], [[2606.29173|TacGen]], [[2605.30341|GPIC]], [[2604.28169|PhyCo]] (CVPR'26), [[2603.26285|PhysVid]] (CVPR'26), [[2602.18690|Motor-Gated Neural Fields]], [[2602.16086|LGQ]], [[2511.20280|VLM-Refine-Physics-Video]] (ICCV'25), [[2509.21309|NewtonGen]] (ICLR'26), [[2503.23368|VLIPP]] (ICCV'25), [[2502.02492|VideoJAM]] (ICML'25 Oral), [[2409.18964|PhysGen]] (ECCV'24), [[2211.14680|PIDM-Flow-Reconstruction]], [[1801.03924|LPIPS]]

> [!star] Key Papers
> - [[2509.20358|PhysCtrl]] (NeurIPS'25) — Diffusion-based generative physics network conditioned on material properties and external forces; produces 3D point trajectories with spatio-temporal attention regularized by physics, velocity, and boundary losses
> - [[2603.13770|PhysAlign]] — LoRA adapter for DiT-based I2V models; dual latent-space alignment with V-JEPA2 kinematic priors and 3D-geometry depth heads, trained on only 3,000 Blender-simulated clips
> - [[2509.21309|NewtonGen]] (ICLR'26) — Physics-informed neural ODE module (Neural Newtonian Dynamics) embedded inside T2V; explicit Newtonian motion control over 12 motion types with **0.98** Physical Invariance Score

**Physics-Loss & Reward Fine-Tuning** — Post-training and inference-time methods that align pre-trained generators with physics-derived loss functions or verifiable rewards (PDE residuals, Newtonian kinematic constraints, mass conservation, world-model surprise), whether by fine-tuning or by steering at sampling time.
- [[2606.05328|Invisible-Hand-of-Physics]], [[2603.13925|SmoothVLA]], [[2602.03627|Phys-Instruct]], [[2601.11087|PhysRVG]], [[2601.10553|WMReward]], [[2512.24551|PhyGDPO]] (ECCV'26), [[2512.00425|NewtonRewards]], [[2510.13809|PhysMaster]], [[2509.20570|PIRF]] (NeurIPS'25 Workshop), [[2506.04171|PCFM]] (NeurIPS'25), [[2506.02244|PGML]], [[2504.15932|Phys-AR]], [[2503.09595|PISA]] (ICML'25), [[2412.02617|AIF-Dynamic-T2V]], [[2403.14404|PIDM]] (ICLR'25)

> [!star] Key Papers
> - [[2512.00425|NewtonRewards]] — Verifiable rule-based rewards from optical-flow proxies and visual-feature mass conservation; +9.75% physical fidelity on NewtonBench-60K with explicit anti-reward-hacking design
> - [[2509.20570|PIRF]] (NeurIPS'25 Workshop) — Backpropagates trajectory-level PDE-residual rewards through the entire denoising process; layer-wise truncation prevents reward hacking and beats SOTA on 4/5 PDE benchmarks
> - [[2503.09595|PISA]] (ICML'25) — Physics Supervised Fine-Tuning + Object Reward Optimization on small simulated datasets; first systematic post-training recipe for object freefall
> - [[2601.10553|WMReward]] — Differentiable physics reward derived from V-JEPA2 prediction surprise; first place at ICCV 2025 PhysicsIQ Challenge with 62.64%, +11.4% human-preference win rate via Best-of-N + gradient guidance

**Physics-Aware Robotic World Models** — Generative video models repurposed as physically-interactable digital twins for robot policy learning, bridging visual plausibility and physical feasibility.
- [[2609.26292|RoboTwin-Phys]], [[2607.19190|Agentic Real2Sim]], [[2607.18154|World Translation]], [[2607.01938|PhysMani]] (ECCV'26), [[2607.00673|PVWM]], [[2606.28128|PhysisForcing]], [[2606.03476|Human2Humanoid]], [[2606.02432|NDPP-Grasp]], [[2605.20758|g-car]] (ICML'26), [[2604.11386|ComSim]], [[2604.08544|SIM1]], [[2603.23376|ABot-PhysWorld]], [[2512.06963|VideoVLA]] (NeurIPS'25), [[2511.07416|PhysWorld]], [[2504.13059|RoboTwin]] (CVPR'25), [[2406.16862|Dreamitate]] (CoRL'24), [[2310.06114|UniSim]] (ICLR'24 Oral), [[2307.08927|Cable-Routing]], [[2104.11213|ManipulaTHOR]], [[2011.07215|SoftGym]] (CoRL'20), [[1812.01717|FVD]]

> [!star] Key Papers
> - [[2511.07416|PhysWorld]] — Reconstructs a physically interactable digital twin from generated task-conditioned videos; object-centric residual RL achieves 82% real-world success and reduces grasping failures from 18% to 3%

**Physics-Constrained Scene Reconstruction for Simulation-Ready Twins (Non-Generative)** — Retrofits existing object pose and shape estimators with non-penetration, stability, and contact constraints so multi-object scene reconstructions survive rollout in a physics simulator, producing simulation-ready digital twins rather than generating new pixels or 3D content.
- [[2604.19923|UniCon3R]], [[2602.20150|SPARCS]] (RSS'26), [[2602.08058|Picasso]] (RSS'26), [[2510.15342|SHARE]]

**Physics Cognition Limits & Surveys** — Diagnostic studies and surveys analyzing whether scaling alone yields physical understanding, and taxonomies of physics cognition tiers in video generators.
- [[2607.27017|POKEWORLD]], [[2607.05966|iKCE]], [[2602.06033|VLM-Intuitive-Physics]] (ICML'26), [[2510.06251|Physics-Frontier-Diagnostic]], [[2503.21765|Physics-Cognition-Survey]], [[2503.21668|Object-Understanding-Cog-Eval]], [[2503.04641|Multimodal-Generative-Models-Survey]], [[2502.11831|V-JEPA (Intuitive Physics)]], [[2502.07007|Grounding-Creativity-in-Physics]], [[2411.02385|PhyWorld]] (ICML'25)

> [!star] Key Papers
> - [[2411.02385|PhyWorld]] (ICML'25) — Definitive scaling study showing video models generalize "case-based" rather than learning abstract physics; OOD errors stay an order of magnitude above ID even at DiT-XL/6M-video scale, and the visual-attribute hierarchy (color > size > velocity > shape) explains object-consistency failures
> - [[2503.21765|Physics-Cognition-Survey]] — Three-tier Piaget-inspired taxonomy (Basic Schema Perception → Passive Cognition → Active Cognition) for video generators; surveys mechanics/optics/thermal/materials coverage and identifies neuro-symbolic + differentiable physics as future frontiers

**Physical Reasoning & Prediction Benchmarks** — Classic video QA and physical-prediction benchmarks that test causal/intuitive physics understanding from real video, predating the generative-video-fidelity question.
- [[2411.13609|VAMP]], [[2406.18522|ChronoMagic-Bench]] (NeurIPS'24 Spotlight), [[2311.10111|VideoCon]] (CVPR'24), [[2305.13786|Perception Test]] (NeurIPS'23), [[2106.08261|Physion]], [[2012.04293|CRAFT]], [[1910.01442|CLEVRER]] (ICLR'20), [[1803.07616|IntPhys]]

**Generative Video Physics-Fidelity Benchmarks** — Evaluation suites that systematically measure whether generated videos obey gravity, optics, thermodynamics, and material properties.
- [[2609.18323|MiniMax-H3 Physical Reasoning]], [[2608.09873|Sci-VBench]], [[2606.28757|CrashTwin]], [[2606.24256|TailOR]], [[2606.04811|Dream.exe]], [[2605.29360|MiraBench]], [[2603.15847|FEEL]] (ECCV'26 Oral), [[2512.12756|FysicsWorld]], [[2510.11512|LikePhys]] (ICLR'26), [[2510.08398|VideoVerse]], [[2510.02311|IDPP]], [[2507.15824|PhysVidBench]], [[2506.00022|PHYSICS-Dataset]] (NeurIPS'25), [[2505.15929|PhyX]], [[2504.02918|Morpheus]] (ICML'26), [[2503.06800|VideoPhy-2]] (ICLR'26), [[2503.05333|PhysicsGen]] (CVPR'25), [[2410.05363|PhyGenBench]] (ICML'25)

> [!star] Key Papers
> - [[2504.02918|Morpheus]] (ICML'26) — 130 real-world Newtonian mechanics videos with hierarchical Discard/Dynamical/Invariance scoring; even SOTA generators (WAN-2.1, COSMOS-predict2) score only 0.52–0.55 vs. real-world's 0.98+
> - [[2503.06800|VideoPhy-2]] (ICLR'26) — Action-centric physical commonsense benchmark; best models hit only 32.6% joint performance (22% on hard subset), with VideoPhy-2-AutoEval offering 47–49% relative gains as automated judge
> - [[2410.05363|PhyGenBench]] (ICML'25) — 160-prompt benchmark across Mechanics/Optics/Thermal/Materials with PhyGenEval auto-scoring (Spearman ρ=0.81 with humans); top T2V model scored only 0.51/3.0, exposing the physics gap
> - [[2106.08261|Physion]] — Foundational dataset that pioneered "physics prediction from video" as a benchmark setting; the original benchmark that defined the model-vs-human physical-prediction gap

**Force, Kinematic & Sketch-Guided Video Generation** — Physics-conditioned T2V/I2V/V2V methods that consume forces, sketches, kinematic priors, or masks as an explicit controllable generation signal.
- [[2601.22135|PI-Light]] (ICLR'26), [[2601.18577|Self-Refining-Video-Sampling]] (ICML'26), [[2601.00504|MotionPhysics]], [[2512.10927|FoundationMotion]], [[2511.17450|Sketch-Guided-Plan-Verification]], [[2510.02284|KineMask]], [[2509.24702|Implausibility-Reasoning-Video-Gen]], [[2505.21653|DiffPhy]], [[2505.19386|Force-Prompting]] (NeurIPS'25), [[2505.18151|WonderPlay]] (ICCV'25 Highlight), [[2502.19868|C-Drag]], [[2501.16550|PhysAnimator]] (CVPR'25), [[2411.19381|Sketch-Animation-Diffusion]], [[2305.13840|Control-A-Video]]

> [!star] Key Papers
> - [[2505.19386|Force-Prompting]] (NeurIPS'25) — Force vectors as a controllable generation prompt; first to enable physics-driven I2V where users specify push/drag forces
> - [[2510.02284|KineMask]] — Object-mask-conditioned kinematics for diffusion video; teaches the model object-interaction physics by guiding the masking pattern
> - [[2505.18151|WonderPlay]] (ICCV'25 Highlight) — Action-conditioned dynamic 3D scene generation via differentiable physics + video diffusion; supports user-specified force interventions for one-shot replanning

**Score-Distilled Physics-from-Video Priors** — Recover physical/material properties or dynamics by distilling from pre-trained video diffusion priors via score-distillation sampling.
- [[2505.16971|UniPhy]] (CVPR'25), [[2505.16456|MAGIC]] (ECCV'26), [[2505.13437|FinePhys]] (CVPR'25), [[2503.20822|Synthetic-Video-Physical-Fidelity]] (ICCV'25), [[2411.17189|PhysMotion]], [[2411.14423|PhysFlow]], [[2409.07179|Phy124]], [[2406.04338|Physics3D]], [[2406.04155|Lagrangian-Particle-Optimization]] (CVPR'24), [[2406.01476|DreamPhysics]], [[2405.13557|MotionCraft]] (NeurIPS'24), [[2401.16663|VR-GS]]

**Physics-Grounded Gaussians and NeRFs** — Couples explicit 3D Gaussian / NeRF representations with physical simulators (MPM, FEM, PBD) so that each Gaussian carries material properties and obeys conservation laws under deformation. The dominant pattern for 4D dynamics: scene reconstruction first, then simulator-driven evolution.
- [[2607.12265|DiffRadar]], [[2606.21753|RAF]] (CVPR'26), [[2606.03479|PersistGS]], [[2605.25909|R5DGS]], [[2605.11266|PG-3DGS]], [[2603.21356|FluidGaussian]] (CVPR'26), [[2602.18886|PhysConvex]], [[2503.21442|RainyGS]] (CVPR'25), [[2503.04720|FluidNexus]] (CVPR'25 Oral), [[2501.18982|OmniPhysGS]] (ICLR'25), [[2412.17804|GausSim]] (ICCV'25), [[2412.11258|GaussianProperty]] (ICCV'25), [[2411.14423|PhysFlow]], [[2410.08257|NeuMA]], [[2409.07179|Phy124]], [[2406.04338|Physics3D]], [[2404.01223|Feature-Splatting]], [[2401.15318|Gaussian-Splashing]] (CVPR'25), [[2312.00583|DeformGS]], [[2311.13099|PIE-NeRF]] (CVPR'24), [[2311.12198|PhysGaussian]] (CVPR'24 Highlight), [[2308.09713|Dynamic-3D-Gaussians]], [[2304.14369|NCLaw]] (ICML'23), [[2303.05512|PAC-NeRF]] (ICLR'23 Spotlight)

> [!star] Key Papers
> - [[2311.12198|PhysGaussian]] (CVPR'24 Highlight) — Couples 3D Gaussian Splatting with continuum mechanics MPM solver; first to make 3DGS scenes physically interactive without rebuilding meshes
> - [[2303.05512|PAC-NeRF]] (ICLR'23 Spotlight) — Physics-Augmented Continuum NeRF; jointly recovers geometry and material parameters (Young's modulus, density, plasticity) from video, foundational for material-property estimation from pixels
> - [[2412.11258|GaussianProperty]] (ICCV'25) — Distills Vision Foundation Model priors into 3D Gaussians to predict per-Gaussian material properties; bridges VLMs and physical simulation
> - [[2501.18982|OmniPhysGS]] (ICLR'25) — Constitutive Gaussians with learnable per-particle constitutive networks; ensemble of 12 expert models + custom PyTorch MPM reduces memory **75%** vs Warp solvers
> - [[2406.04338|Physics3D]] — Distills physical properties (Young's modulus, viscosity, plasticity) into 3D Gaussians via video diffusion priors; the canonical Score-Distillation-from-video-prior recipe for material inference

**Articulated and 4D Physics** — Methods specialized for articulated objects (joints, kinematic chains) and 4D dynamics where geometry, motion, and physics co-evolve over time.
- [[2606.31388|OVOW]] (ECCV'26), [[2606.27364|PhysiFormer]], [[2603.03485|Phys4D]], [[2504.01204|Articulated-Kinematics-Distillation]] (CVPR'25), [[2411.16800|Phys4DGen]], [[2410.07155|Trans4D]], [[2405.16849|Sync4D]], [[2405.15056|ElastoGen]], [[2403.17920|TC4D]] (ECCV'24)

> [!star] Key Papers
> - [[2504.01204|Articulated-Kinematics-Distillation]] (CVPR'25) — Distills articulated kinematics from video diffusion priors into rigged-skeleton 3D models; bridges generative video and physically-driven character animation
> - [[2410.07155|Trans4D]] — Realistic geometry-aware transitions for compositional text-to-4D synthesis; handles topological changes (e.g., breaking, melting) that prior methods could not
> - [[2405.15056|ElastoGen]] — 4D generative elastodynamics via convolution-like local quadratic approximation + Neural Material Module; **0.98** correlation with FEM ground truth across hyperelastic materials

**Material and Elastic Physics** — Recover and edit material properties (elasticity, plasticity, fluid, granular) from video or single images, then re-simulate under new forces.
- [[2608.06164|BendTwin]], [[2607.20653|PhysCoRe]], [[2607.13451|PGRD]], [[2603.23973|SLAT-Phys]], [[2504.18719|Vysics]] (RSS'25), [[2503.17973|PhysTwin]] (ICCV'25), [[2411.11343|TVML]], [[2410.08257|NeuMA]], [[2406.04338|Physics3D]], [[2406.01476|DreamPhysics]], [[2404.13026|PhysDreamer]] (ECCV'24), [[2304.14369|NCLaw]] (ICML'23)

> [!star] Key Papers
> - [[2503.17973|PhysTwin]] (ICCV'25) — Single-image-to-physical-twin pipeline; estimates material parameters and rigging that re-simulate under arbitrary forces
> - [[2406.04338|Physics3D]] — Distills physical properties (elasticity, viscoelasticity, plasticity) into 3D Gaussians via SDS from video diffusion; canonical material-from-pixels recipe
> - [[2406.01476|DreamPhysics]] — Physics-based 3D dynamics learned from video diffusion priors via score distillation; among the first to make image/video diffusion supervise material parameter inference

**Simulator-in-the-Loop Generation** — Use a physics renderer/engine (Blender, MPM, MuJoCo) inside the generation loop, either to provide ground-truth scaffolding or to fix violations after diffusion sampling.
- [[2607.27380|VideoCoCo]], [[2607.21522|GS-Agent]], [[2607.01766|SimWorlds]], [[2606.08688|PhysAgent]], [[2603.18639|PhysVideo]], [[2603.06408|Physical-Simulator-In-the-Loop-Video]] (CVPR'26), [[2603.05449|RealWonder]], [[2508.13911|PhysGM]] (CVPR'26), [[2506.08006|Dreamland]], [[2506.06440|Vid2Sim]] (CVPR'25), [[2503.20746|PhysGen3D]] (CVPR'25), [[2411.12789|Sim-GS]] (ICCV'25), [[2411.02394|AutoVFX]], [[2408.10453|Kubrick]] (CVPR'25 Workshop), [[2404.09833|Video2Game]] (CVPR'24), [[2311.12631|GPT4Motion]] (CVPR'22 Workshop)

> [!star] Key Papers
> - [[2411.02394|AutoVFX]] — End-to-end automatic VFX pipeline using LLMs to script Blender simulations driven by visual context; bridges generative AI and traditional rendering
> - [[2311.12631|GPT4Motion]] (CVPR'22 Workshop) — GPT-4 plans Blender scenes that drive ControlNet-guided text-to-video; one of the earliest LLM+simulator+diffusion stacks for physically-grounded video

**LLM-Driven Physics Reasoning** — LLMs acting as reasoning engines to derive physical equations, force fields, or simulation parameters that drive downstream generators.
- [[2608.09296|CADEngBench]], [[2608.08053|Structured Physical CoT]], [[2605.18396|NEWTON]], [[2603.09094|CoECT]] (CVPR'26), [[2601.05848|Goal-Force]] (CVPR'26), [[2512.05564|ProPhy]], [[2512.04221|MoReGen]], [[2507.06830|Physics-Grounded-Motion-Forecasting]], [[2505.05469|LegoGPT]] (ICCV'25 Oral), [[2503.20654|AccidentSim]], [[2502.19868|C-Drag]], [[2411.08027|LLMPhy]], [[2309.17444|LVD]] (ICLR'24)

> [!star] Key Papers
> - [[2505.05469|LegoGPT]] (ICCV'25 Oral) — LLM-driven physically-stable LEGO assembly generation; the LLM proposes brick layouts that are then verified for structural physics
> - [[2603.09094|CoECT]] (CVPR'26) — Chain of Event-Centric Causal Thought; LLM decomposes physical phenomena into causally ordered event units grounded in formulas; **+8.19%** over PhysHPO on PhyGenBench
> - [[2507.06830|Physics-Grounded-Motion-Forecasting]] — Retrieval-based Symbolic Regression discovers physical equations from video trajectories; predicts physically aligned futures used as I2V guidance — neuro-symbolic precursor to physics-grounded T2V
> - [[2502.19868|C-Drag]] — Training-free chain-of-thought motion controller using VLM reasoning over object physics; bridges multimodal LLM perception and trajectory-based video generation

> [!tip] Physics-Aware Training Recipe
> The community has converged on a layered approach: (1) start with a strong pre-trained video diffusion / flow model, (2) fine-tune on a small (~3K-60K) synthetic physics dataset from a controllable simulator (Blender, MPM), (3) add a physics-derived loss or reward — kinematic residuals (NewtonRewards), PDE residuals (PIRF), or world-model surprise (WMReward) — with layer-wise truncation to prevent reward hacking, and (4) evaluate on PhyGenBench/VideoPhy/PhysicsIQ/VideoVerse rather than visual fidelity alone. Always include a *conservation* term (mass, feature consistency) — without it, models collapse to trivial reward-hacked solutions where objects vanish or freeze. The **neuro-symbolic frontier** (NewtonGen, Phys-Motion-Forecast, CoECT) is now competitive: physics-informed neural ODEs and equation-discovery modules embedded *inside* T2V pipelines achieve explicit Newtonian control where reward-only fine-tuning struggled.

> [!success] Validated Physics-Aware Pipeline
> ==Pre-trained generator (DiT/flow)== → ==LoRA-adapted alignment== with V-JEPA2 kinematic teacher + 3D depth head (PhysAlign) OR ==full fine-tuning== with PDE/kinematic residual reward (PIRF, NewtonRewards) → ==inference-time== Best-of-N with WMReward for an extra +6-11% physics gain at zero retraining cost. Anchor evaluation on PhyGenBench, VideoPhy, and PhysicsIQ — visual quality metrics alone do not detect physics violations.

---

## Cross-References

- [[04_Video-and-Temporal]] — Video generation as world models
- [[11_Robotics-and-Embodied-AI]] — Diffusion Policy and flow matching for robot control
- [[08_Reinforcement-Learning]] — RL + diffusion intersection
- [[09_Self-Evolving-AI]] — Self-evolving generative systems

---

*Next: [[04_Video-and-Temporal]] for how generative and perception models combine to model dynamics over time.*
