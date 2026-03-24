---
title: "Methodology — Spatial Intelligence in MLLMs"
tags:
  - spatial-reasoning
  - research-proposal
  - RL
  - chain-of-thought
  - architecture
aliases:
  - Spatial Intelligence Methodology
---

## Methodology

> [!abstract] Four Pillars
> This research adopts a comprehensive methodology integrating ==training-free strategies==, ==post-training enhancements==, ==agentic frameworks==, and ==architectural innovations== to address the four progressive stages of spatial reasoning.

---

### 1. Training-Free Strategies

Training-free strategies offer an efficient pathway to enhance spatial intelligence by operating directly at inference time, circumventing costly retraining. They refine the model's reasoning process, guide attention, and structure information access to unlock latent capabilities already present but not effectively utilized.

#### Structured Inference

Strategies for structured inference guide reasoning without altering model parameters. Decomposing complex spatial problems through structured prompting or simulating mental imagery can convert challenging allocentric questions into more manageable egocentric ones [[2506.03642|Spatial Understanding from Videos]], [[2504.17207|Perspective-Aware Reasoning]]. Other inference-time techniques enhance visual perception by adaptively adjusting attention mechanisms, dynamically searching for crucial image regions, or automatically cropping inputs based on internal states [[2503.01773|Why Is Spatial Reasoning Hard]], [[2504.14920|DyFo]], [[2502.17422|MLLMs Know Where to Look]]. Reasoning can also be improved by explicitly grounding textual rationales with interleaved visual patches or by refining latent thought trajectories using contrastive feedback search during inference [[2506.07235|Interleaved-Modal CoT]], [[2506.08552|Efficient PR]].

#### Explicit World Modeling (Cognitive Maps)

Another set of training-free approaches builds and utilizes explicit world models. This involves constructing dynamic or heterogeneous cognitive maps online — structured graphs of environmental entities, objects, and their relationships — to guide complex planning and navigation [[2506.17629|CLiViS]], [[2412.10439|CogNav]]. Evaluations show that standard models frequently fail on tasks requiring deep understanding of latent relational structures [[2309.15129|CogEval]]. These limitations can be addressed by extracting explicit, interpretable cognitive maps from internal representations [[2401.05946|TDB]] or by prompting the model to generate spatial layouts through a map imagination mechanism [[2412.10439|SpaceR]].

---

### 2. Post-Training Enhancements

> [!note] Key Concerns
> While pre-training provides a strong foundation, post-training enhancements are essential for refining reasoning and alignment [[2502.21321|LLM Post-Training]], [[2501.09686|LRM Survey]], [[2505.02665|Slow Thinking Survey]], [[2507.09662|Towards CA]], [[2504.12328|RLVR Survey]], [[2506.23918|Thinking with Images Survey]], [[2505.04921|LMRM Survey]], [[2504.03151|Multimodal Reasoning Survey]], [[2508.17298|Compositional VR Survey]], [[2506.21872|RL in Vision Survey]]. This stage must address ==efficient reasoning== to prevent resource-intensive "overthinking" [[2503.16419|Stop Overthinking]], [[2503.21614|Efficient Reasoning Survey]], [[2503.23077|Efficient Inference]], [[2407.14414|System-1.x]], [[2504.10903|Efficient RM]] and ==continual learning== to avoid catastrophic forgetting [[2506.21872|Continual RL Survey]], [[2508.04227|VLM CL Survey]].

#### 2.1 Building Reasoning Skills through Reward Optimization

##### Multistage Training (SFT then RL)

Multistage training progressively builds capabilities through distinct learning phases. An initial SFT phase teaches foundational behavior, followed by RL for optimization. Models are first taught to generate structured outputs like cognitive maps, visually grounded reasoning steps, or latent visual tokens, then refined using RL to improve task accuracy [[2506.21458|MindCube]], [[2505.23678|Grounded RL]], [[2506.17218|Machine Mental Imagery]]. This pipeline is also effective for instilling complex skills such as code generation for image processing or unifying general and spatial reasoning [[2508.11630|Thyme]], [[2507.08306|M2-Reasoning]], [[2505.23747|Spatial-MLLM]]. The process can be applied iteratively to co-evolve model and training data, or adapted with specialized rewards for semantic consistency and temporal awareness [[2507.16518|C2-Evo]], [[2505.12434|VideoRFT]], [[2503.21776|Video-R1]].

More complex frameworks introduce additional stages or reorder the conventional pipeline. Some approaches employ a progressive curriculum advancing from text-centric to multimodal reasoning [[2506.04207|Advancing Multimodal Reasoning]], [[2507.22607|VL-Cogito]]. Others insert intermediate steps such as reflective rejection sampling [[2506.09965|VILASR]], [[2505.12363|Visuospatial Cognition]]. The standard pipeline can be inverted — using RL first to broadly activate latent reasoning before SFT enhances specific skills [[2506.13056|Metis-RISE]], [[2501.10074|SpatialCoT]].

Beyond direct policy training, multistage methods also develop specialized components: advanced reward models can be created via distillation followed by RL refinement [[2505.02387|RM-R1]], and a single base model can be fine-tuned into a system that dynamically balances fast and slow reasoning [[2407.14414|System-1.x]].

##### Advanced GRPO

Group Relative Policy Optimization (GRPO) refines model reasoning by sampling and rewarding superior response strategies, but standard GRPO is often suboptimal for spatial reasoning due to instability, reward hacking, and inefficient exploration.

==Core algorithmic enhancements== include replacing the objective with a geometric mean to stabilize training [[2507.20673|Geometric-Mean PO]], analyzing instability sources to prevent artificial response length growth [[2503.20783|Dr. GRPO]], adaptively balancing rewards across task difficulty [[2505.19000|Thinking with Videos]], [[2310.04406|TreePO]], [[2505.19255|Depth-Breadth Synergy]], and improving both on-policy and off-policy dynamics with robust open-source frameworks [[2505.22257|Off-Policy GRPO]], [[2503.14476|DAPO]], [[2504.05118|VAPO]].

==Reward engineering== involves designing task-specific rewards based on cognitive map accuracy or step consistency [[2412.10439|SpaceR]], [[2506.16141|GRPO-CARE]], [[2504.00883|vsGRPO]], and training models to generate their own rewards via decomposition or reflection [[2508.19652|Self-Rewarding VLM]], [[2505.24726|Reflect Retry Reward]], [[2505.14674|Reward RM]].

==Data management== strategies include dynamically filtering for concise yet correct responses [[2503.20783|GFPO]], using verifiers to construct high-quality preference pairs [[2505.19000|VerIPO]], [[2507.13362|Enhancing SR]], and applying GRPO to unsupervised post-training without human-labeled data [[2505.22453|Unsupervised PF]]. GRPO has been used to refine structured outputs such as interwoven drawing operations or tool-use code [[2506.09965|VILASR]], [[2508.11630|Thyme]], and to reinforce reasoning for complex spatial transformations [[2505.15804|STAR-R1]], [[2507.08306|M2-Reasoning]], [[2505.21493|Reinforcing GR]]. These methods rely on robust data pipelines and dynamic hyper-parameter adjustments [[2503.21776|Video-R1]], [[2506.13056|Metis-RISE]], [[2507.16518|C2-Evo]].

#### 2.2 Explicit Visual Reasoning ("Thinking with Images")

Explicit visual reasoning enables models to generate and manipulate visual information as intermediate reasoning steps. Surveys have systematically categorized these Multimodal Chain-of-Thought methodologies [[2506.23918|Thinking with Images Survey]], [[2505.04921|LMRM Survey]], [[2503.12605|Multimodal CoT Survey]].

A primary strategy trains models to generate new visual representations. This includes producing interwoven visual drawings as part of the thought process [[2506.09965|VILASR]] or generating intrinsic "perception tokens" representing depth maps or bounding boxes internally [[2502.17425|Perception Tokens]]. These methods often use curriculum learning progressing from simple token generation to complex multi-step reasoning, optimized with RL [[2507.13362|Enhancing SR]], [[2501.19201|Efficient RW]].

Another line of research generates structured rationales grounded in visual information. Models can produce scene graphs before answering [[2507.20529|Enhancing SR Visual+Text]], align textual plans with coordinate-based actions [[2501.10074|SpatialCoT]], or interleave visual patches directly within generated text [[2506.17218|Machine Mental Imagery]], [[2506.07235|Interleaved-Modal CoT]].

A third approach centers on iterative refinement: models autonomously re-process visual information by generating special tokens that trigger re-encoding with specialized vision modules [[2502.17425|VPT]], [[2505.22525|TwGI]]. Other methods use an "imagine-and-refine" loop [[2501.07542|Imagine and Refine]], [[2504.18397|Unsupervised Visual CoT]] or are simplified into end-to-end frameworks with visual programs [[2505.11409|Visual Planning]], [[2505.22525|Mind's Eye]], [[2508.12109|Simple o3]].

#### 2.3 Implicit Visual Reasoning ("Thinking in Latent Space")

Implicit visual reasoning moves chain-of-thought into the model's continuous hidden states, allowing more complex and efficient multi-step reasoning by bypassing the natural language bottleneck. Surveys establish unified taxonomies for these methods and highlight the bandwidth advantage of latent representations [[2507.06203|Latent Reasoning Survey]], [[2505.16782|Reasoning Beyond Language]].

==Internalizing and compressing thought processes:== Models can reason in continuous latent space from the outset [[2412.06769|Training LLMs in Latent]] or use "stepwise internalization" to gradually remove the need for explicit output [[2405.14838|Stepwise Internalization]]. Other methods compress complex thoughts into dense representations via self-distillation [[2412.13171|Compressed CoT]], [[2502.21074|CODIC]], [[2410.17385|LaRS]]. This paradigm extends through looped transformers enabling iterative refinement within hidden states [[2502.17416|Reasoning with Loops]].

==Multimodal latent reasoning:== Frameworks reason with latent visual tokens, demonstrating that multimodal models are inherently capable of latent reasoning [[2506.17218|Machine Mental Imagery]], [[2412.08635|LatentLM]]. These develop into hybrid systems mixing latent and explicit text tokens [[2502.03275|Token AM]], [[2504.17207|Perspective-Aware Reasoning]], enhanced by RL or multimodal thought compression [[2505.18454|Hybrid Latent Reasoning]], [[2508.12587|MCOUT]].

==Optimizing latent reasoning trajectories:== This can be done at inference time without parameter updates, using contrastive feedback search [[2506.08552|Efficient PR]] or policy gradient approaches [[2505.13308|Seek in the Dark]]. Models can also learn from synthesized latent thoughts via Expectation-Maximization [[2503.18866|Reasoning to Learn]] or compress verbose CoT into single "thinking tokens" [[2501.19201|Efficient RW]]. Looped transformer architectures scale reasoning through deeper iterative processing [[2502.05171|Scaling UT]], [[2311.12424|Looped Transformers]].

#### 2.4 Inference-Time Optimization

Dynamic problem-solving at inference time enhances reasoning by applying adaptive strategies during generation, allowing the model to refine its thought process, correct errors, and explore different solution paths per problem.

==Iterative refinement:== This includes policy gradient optimization of latent representations [[2505.13308|Seek in the Dark]], self-correction via reward model feedback [[2505.14674|Reward RM]], dynamic attention focusing [[2504.14920|DyFo]], automated structured thinking and answer verification [[2412.18319|Boosting MR]], verifier-based output selection [[2508.14313|AIRL-S]], and fine-grained optimization with targeted rewards [[2506.21656|Fine-Grained PO]].

==Search-based strategies:== Monte Carlo Tree Search (MCTS) treats reasoning as a planning problem, balancing exploration and exploitation [[2407.14414|System-1.x]], [[2310.04406|LATS]]. By integrating MCTS, models decompose complex problems into manageable steps and build reasoning trees [[2501.09686|AtomThink]], [[2412.18319|Mulberry]]. This search-based approach is particularly effective for grounded reasoning aligned with environmental states [[2505.23678|Grounded RL]].

---

### 3. Agentic Frameworks

Agentic frameworks enhance spatial reasoning by decomposing complex problems into sub-tasks delegated to specialized modules or external tools. A central reasoner orchestrates components such as code interpreters and vision tools for fine-grained analysis.

==Interleaved reasoning and tool execution:== Systems are trained to use visual editing tools as part of multimodal chain-of-thought or to autonomously generate and execute code for image processing and quantitative reasoning [[2505.19255|VTool-R1]], [[2508.11630|Thyme]]. This iterative interaction can be learned through scalable data synthesis pipelines [[2508.12109|Simple o3]].

==Multi-agent and verifier-enhanced systems:== Frameworks can be designed as multi-agent systems with specialized tools for object detection or depth estimation, or employ dedicated verifier modules to determine when iterative reasoning should terminate [[2505.17012|SpatialScore]], [[2506.07235|Multi-Step VR]]. Such systems are often optimized with RL algorithms designed for multi-task difficulty imbalance [[2505.19000|Thinking with Videos]].

==Modular skill decomposition:== Specialized expert modules can be trained with parameter-efficient methods, each responsible for a specific reasoning skill [[2506.03525|Video-Skill-CoT]]. Complex cognitive processes like perspective-taking can be simulated through structured pipelines that abstract a scene, transform the viewpoint, and prompt for an answer [[2504.17207|Perspective-Aware Reasoning]].

---

### 4. Architectural Innovations

> [!warning] The Encoder Bottleneck
> Standard vision encoders, optimized for high-level semantic recognition, tend to flatten visual inputs and discard ==fine-grained geometric and structural details== essential for spatial reasoning.

#### Enhanced Visual Capture

Integrating dual or hierarchical vision encoders captures both high-level semantics and low-level structural details [[2505.23747|Spatial-MLLM]], [[2505.12363|Visuospatial Cognition]]. Other approaches redesign the vision-language interface by introducing novel projectors that create dedicated visual spatial tokens [[2507.00505|LLaVA-SP]] or add a discrete bottleneck to learn interpretable cognitive maps [[2401.05946|TDB]].

#### Efficient Internal Representations

Architectures can handle hybrid token types by compressing verbose reasoning into single "thinking tokens" [[2501.19201|Efficient RW]], mixing latent and text tokens for balanced efficiency and interpretability [[2502.03275|Token AM]], or using distinct heads for continuous and discrete data [[2412.08635|LatentLM]].

#### Iterative Processing

Recurrent depth and looped transformer architectures scale reasoning at test time by repeatedly applying the same weights, emulating iterative algorithms and enabling complex computational patterns without increasing parameter count [[2502.05171|Scaling UT]], [[2311.12424|Looped Transformers]], [[2502.17416|Reasoning with Loops]].

---

### 5. Uniqueness

This research is unique in its holistic integration of all four pillars to advance spatial intelligence:

> [!tip] Training-Free Strategies
> Combines structured inference [[2506.03642|Spatial Understanding from Videos]], [[2504.17207|Perspective-Aware Reasoning]], attention refinement [[2503.01773|Why Is Spatial Reasoning Hard]], [[2504.14920|DyFo]], and cognitive maps [[2506.17629|CLiViS]], [[2412.10439|CogNav]] into a versatile, model-agnostic framework.

> [!tip] Post-Training Enhancements
> Synergizes multistage SFT-then-RL pipelines [[2506.21458|MindCube]], [[2505.23678|Grounded RL]], [[2505.23747|Spatial-MLLM]] with advanced GRPO [[2507.20673|Geometric-Mean PO]], [[2503.20783|Dr. GRPO]], [[2310.04406|TreePO]], [[2505.19255|Depth-Breadth Synergy]]. Uniquely combines explicit visual reasoning [[2506.09965|VILASR]], [[2502.17425|Perception Tokens]], [[2506.23918|Thinking with Images Survey]] with implicit latent reasoning [[2507.06203|Latent Reasoning Survey]], [[2412.06769|Training LLMs in Latent]], [[2506.17218|Machine Mental Imagery]]. Dynamic inference-time optimization via search and self-correction [[2505.13308|Seek in the Dark]], [[2505.14674|Reward RM]], [[2407.14414|System-1.x]] ensures adaptive problem-solving.

> [!tip] Agentic Frameworks
> A modular approach leveraging specialized tools and multi-agent collaboration [[2505.19255|VTool-R1]], [[2508.11630|Thyme]], [[2508.12109|Simple o3]], guided by verifier-enhanced frameworks [[2505.17012|SpatialScore]], [[2506.07235|Multi-Step VR]].

> [!tip] Architectural Innovations
> Dual-pathway vision encoders for geometric detail [[2505.23747|Spatial-MLLM]], [[2505.12363|Visuospatial Cognition]], specialized vision-language interfaces with spatial tokens [[2507.00505|LLaVA-SP]], [[2401.05946|TDB]], and recurrent structures for deeper iterative reasoning [[2502.05171|Scaling UT]].

---

*See also: [[01_Background-and-Rationales]] | [[02_Research-Stages]] | [[04_Challenges]]*
