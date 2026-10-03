---
title: "Agents & Tool Use — Topic Overview"
tags:
  - agent
  - tool-use
  - multi-agent
  - agentic-ai
aliases:
  - "Agents Overview"
---

# Agents & Tool Use

> [!abstract] Overview
> AI agents that reason, plan, and use tools to accomplish multi-step tasks. This topic covers the full arc from ReAct-style reasoning-acting loops (2022) through RL-trained tool-using agents (2025) to self-evolving multi-agent systems (2026). The field has matured along several axes: single-turn to multi-turn, fixed tools to tool creation, single-agent to multi-agent orchestration, and handcrafted prompting to reinforcement-learned agentic behavior.

## Evolution Graph

```text
1. Reasoning-Acting Loop   (think, act, observe)
· interleave thought and action
                    +LLM as own
                    world model       +tree search
╔══════════════╗    ┌────────────┐    ┌─────────────┐
║ ReAct (2022) ║───►│ RAP (2023) │───►│ LATS (2023) │
╚═══════┬══════╝    └────────────┘    └─────────────┘
        │    +field map
        │    ┌────────────────────────────────────┐
        └───►│ Agentic-RL-Landscape-Survey (2025) │
             └────────────────────────────────────┘

2. Code Agents   (make code the action space)
· programs as actions
                                         +Python module         +evolutionary program
                  +program-of-thought    orchestration          search
┌────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌────────────────────┐
│ PAL (2022) │───►│ PoT (2022)      │───►│ ViperGPT (2023) │───►│ AlphaEvolve (2025) │
└──────┬─────┘    └─────────────────┘    └─────────────────┘    └────────────────────┘
       │    text → visual
       │    programs
       │    ┌────────────────┐
       └───►│ VISPROG (2022) │
            └────────────────┘

3. Tool-Use RL   (learn when to call, not just how)
· reward the tool call
                     +reward shaping      +scaled
                     for tools            tool-integrated RL    +dual distillation
┌───────────────┐    ┌───────────────┐    ┌────────────────┐    ┌───────────────────┐
│ ReTool (2025) │───►│ ToolRL (2025) │───►│ ToRL (2025)    │───►│ Agentic-R1 (2025) │
└───────┬───────┘    └───────────────┘    └────────────────┘    └───────────────────┘
        │    +reasoning and
        │    tools jointly
        │    ┌───────────────┐
        ├───►│ ARTIST (2025) │
        │    └───────────────┘
        │    text tools → visual
        │    tools
        │    ┌─────────────────────┐
        └───►│ OpenThinkIMG (2025) │
             └─────────────────────┘

4. Multi-Turn RL   (credit across a whole episode)
· train the trajectory
                    +verifiable
                    meta-reasoning reward    +decoupled RL training        +agentic RL at scale
┌──────────────┐    ┌───────────────────┐    ┌────────────────────────┐    ┌─────────────────────┐
│ RAGEN (2025) │───►│ RLVMR (2025)      │───►│ Agent-Lightning (2025) │───►│ rStar2-Agent (2025) │
└──────────────┘    └───────────────────┘    └────────────────────────┘    └─────────────────────┘

5. Web and GUI Agents   (act in someone else's interface)
· operate the screen
                                             +web world
                      +multimodal memory     model
┌────────────────┐    ┌─────────────────┐    ┌────────────┐
│ CoAct-1 (2025) │───►│ M3-Agent (2025) │───►│ WWM (2025) │
└────────┬───────┘    └─────────────────┘    └────────────┘
         │    +task-grounded shopping
         │    ┌──────────────────────────────┐
         └───►│ See-Think-Act-Shopper (2025) │
              └──────────────────────────────┘

6. Multi-Agent Orchestration   (who assigns the work)
· coordination protocol
                                                    +multi-agent RL
                       +orchestration protocol      fine-tuning
┌─────────────────┐    ┌───────────────────────┐    ┌──────────────┐
│ AgentGym (2024) │───►│ AgentOrchestra (2025) │───►│ MARFT (2025) │─┐
└─────────────────┘    └───────────────────────┘    └──────────────┘ │
                                                                     │    text → latent
                                                                     │    communication
                                                                     │    ┌──────────────────┐
                                                                     ├───►│ LatentMAS (2025) │
                                                                     │    └──────────────────┘
                                                                     │    +society-scale coordination
                                                                     │    ┌─────────────────────────────┐
                                                                     └───►│ Societies-of-Thought (2026) │
                                                                          └─────────────────────────────┘

7. Memory and Skills   (experience becomes reusable state)
· persist what worked
╔════════════════╗    ┌─────────────┐    ┌──────────────┐    ┌───────────────────────┐
║ Voyager (2023) ║    │ MEM1 (2025) │    │ MemRL (2026) │    │ Memento-Skills (2026) │
╚════════════════╝    └─────────────┘    └──────────────┘    └───────────────────────┘

8. Multimodal and Embodied Agents   (act in the world, not a shell)
· perception in the loop
                         +hierarchical                                 +geometry-grounded
                         controller          +agentic visual RFT       agent
┌───────────────────┐    ┌──────────────┐    ┌────────────────────┐    ┌────────────────┐
│ LLaVA-Plus (2023) │───►│ HYDRA (2024) │───►│ Visual-ARFT (2025) │───►│ RieMind (2026) │
└─────────┬─────────┘    └──────────────┘    └────────────────────┘    └────────────────┘
          │    +scientific discovery
          │    loop
          │    ┌────────────────────┐
          └───►│ InternAgent (2025) │
               └────────────────────┘

Legend: ╔═╗ double border = landmark/foundational paper. Boxes without arrows share a mechanism family but no KH-attested lineage.
```

The eight lanes divide on **how the agent decides what to do next**. **Reasoning-acting loop** interleaves thought and action, ReAct establishing the pattern, RAP making the model its own world model, LATS adding tree search, and Agentic-RL-Landscape-Survey branching off to map the lane. **Code agents** make code the action space, PAL to PoT to ViperGPT to AlphaEvolve, with VISPROG branching from text programs to visual ones. **Tool-use RL** learns when to call rather than only how, ReTool to ToolRL to ToRL to Agentic-R1, with ARTIST and OpenThinkIMG branching to joint reasoning-and-tools and to visual tools. **Multi-turn RL** assigns credit across a whole episode, RAGEN to RLVMR to Agent-Lightning to rStar2-Agent. **Web and GUI agents** act inside someone else's interface, CoAct-1 to M3-Agent to WWM, with See-Think-Act-Shopper branching to a task-grounded shopping setting. **Multi-agent orchestration** decides who assigns the work, AgentGym to AgentOrchestra to MARFT, with LatentMAS and Societies-of-Thought branching to latent communication and society-scale coordination. **Memory and skills** turn experience into reusable state: Voyager's executable skill library, MEM1's RL-trained constant memory, MemRL's RL-trained retrieval policy over episodic memory, and Memento-Skills' read-write skill library with a behaviour-aligned router; they are drawn without arrows because none of their notes names another as its parent. Loops that rewrite the harness or the improver itself are traced in [[09_Self-Evolving-AI#10. Harness Optimization & Recursive Self-Improvement|09 §10]]. **Multimodal and embodied agents** act in the world rather than a shell, LLaVA-Plus to HYDRA to Visual-ARFT to RieMind, with InternAgent branching to the scientific-discovery loop.

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2022 | [[2210.03629\|ReAct]] | Reasoning-Acting · Thought and Action | Synergized reasoning and acting in a think-act-observe loop; launched the LLM agent paradigm |
| 2022 | [[2211.10435\|PAL]] | Code Agents · Programs as Actions | Program-aided Language Models offloading computation to a Python interpreter; separated reasoning from calculation |
| 2022 | [[2211.11559\|VISPROG]] | Code Agents · Programs as Actions | Neuro-symbolic visual programming: executable step-by-step programs from natural language queries |
| 2022 | [[2211.12588\|PoT]] | Code Agents · Programs as Actions | Program of Thoughts prompting: LLMs delegate numerical reasoning to code execution |
| 2023 | [[2303.08128\|ViperGPT]] | Code Agents · Programs as Actions | LLM generates Python programs orchestrating vision modules; composable zero-shot visual reasoning |
| 2023 | [[2305.14992\|RAP]] | Reasoning-Acting · Thought and Action | Treated the LLM as its own world model for lookahead planning within reasoning-acting loops |
| 2023 | [[2305.16291\|Voyager]] | Memory and Skills · Persist What Worked | Automatic curriculum plus an executable skill library that grows with experience |
| 2023 | [[2310.04406\|LATS]] | Reasoning-Acting · Thought and Action | Language Agent Tree Search unifying reasoning, acting, and planning through MCTS over action spaces |
| 2023 | [[2311.05437\|LLaVA-Plus]] | Embodied Agents · Perception in the Loop | Training VLMs to learn when and how to use external visual tools for any task |
| 2024 | [[2403.12884\|HYDRA]] | Embodied Agents · Perception in the Loop | Multi-stage dynamic compositional visual reasoning integrating an RL agent as cognitive controller |
| 2024 | [[2406.04151\|AgentGym]] | Multi-Agent · Coordination Protocol | Multi-environment agent evolution via behavioral cloning + self-evolution for generalist agents |
| 2025 | [[2503.23383\|ToRL]] | Tool-Use RL · Reward the Tool Call | Scaling tool-integrated RL; trains LLMs to autonomously learn when and how to use tools |
| 2025 | [[2504.11536\|ReTool]] | Tool-Use RL · Reward the Tool Call | ByteDance's RL framework enabling LLMs to dynamically decide when to invoke tools during reasoning |
| 2025 | [[2504.13958\|ToolRL]] | Tool-Use RL · Reward the Tool Call | Novel reward shaping for tool-use RL; meticulously designed rewards guide optimal tool invocation |
| 2025 | [[2504.16129\|MARFT]] | Multi-Agent · Coordination Protocol | Multi-Agent Reinforcement Fine-Tuning: RL-based optimization of LLM multi-agent systems |
| 2025 | [[2504.20073\|RAGEN]] | Multi-Turn RL · Train the Trajectory | Multi-turn RL training for LLM agents; established the paradigm for sustained agent-environment interaction |
| 2025 | [[2505.01441\|ARTIST]] | Tool-Use RL · Reward the Tool Call | Microsoft Research unifies agentic reasoning, dynamic tool integration, and RL training in a single framework |
| 2025 | [[2505.08617\|OpenThinkIMG]] | Tool-Use RL · Reward the Tool Call | Open-source framework for interleaved visual tool use during reasoning |
| 2025 | [[2505.14246\|Visual-ARFT]] | Embodied Agents · Perception in the Loop | Reinforcement fine-tuning framework for visual agents from Shanghai AI Lab |
| 2025 | [[2505.16938\|InternAgent]] | Embodied Agents · Perception in the Loop | Unified closed-loop multi-agent system for fully autonomous scientific research |
| 2025 | [[2506.15841\|MEM1]] | Memory and Skills · Persist What Worked | RL-trained agent keeps near-constant memory over long multi-turn tasks; up to 72.9% lower peak tokens |
| 2025 | [[2506.12508\|AgentOrchestra]] | Multi-Agent · Coordination Protocol | TEA protocol for unified multi-agent management and task orchestration |
| 2025 | [[2506.13131\|AlphaEvolve]] | Code Agents · Programs as Actions | Google DeepMind combining LLMs with evolutionary search to autonomously discover algorithms |
| 2025 | [[2507.05707\|Agentic-R1]] | Tool-Use RL · Reward the Tool Call | DualDistill framework training language models as tool-using agents via distillation and RL |
| 2025 | [[2507.22844\|RLVMR]] | Multi-Turn RL · Train the Trajectory | Verifiable meta-reasoning rewards improve long-horizon agent performance by rewarding sound reasoning process, not just outcomes |
| 2025 | [[2508.03680\|Agent-Lightning]] | Multi-Turn RL · Train the Trajectory | Microsoft Research decouples RL training from inference, enabling scalable agent training |
| 2025 | [[2508.03923\|CoAct-1]] | Web and GUI · Operate the Screen | Multi-agent framework integrating both GUI interactions and direct programmatic API access |
| 2025 | [[2508.09736\|M3-Agent]] | Web and GUI · Operate the Screen | ByteDance's multimodal agent processing continuous video and GUI streams for real-time task completion |
| 2025 | [[2508.20722\|rStar2-Agent]] | Multi-Turn RL · Train the Trajectory | Microsoft's agentic reasoning model enabling LLMs to "think slow" with structured deliberation over action spaces |
| 2025 | [[2509.02547\|Agentic-RL-Landscape-Survey]] | Reasoning-Acting · Thought and Action | Formal definition of agentic RL for LLMs using Partially Observable Markov Decision Processes |
| 2025 | [[2510.19245\|See-Think-Act-Shopper]] | Web and GUI · Operate the Screen | VLM-driven framework simulating online shopping tasks end-to-end |
| 2025 | [[2511.20639\|LatentMAS]] | Multi-Agent · Coordination Protocol | Agents collaborate through latent-space communication rather than verbose natural language exchanges |
| 2025 | [[2512.23676\|WWM]] | Web and GUI · Operate the Screen | Princeton's Web World Models: a new architectural paradigm where agents build predictive models of web environments for planning |
| 2026 | [[2601.03192\|MemRL]] | Memory and Skills · Persist What Worked | Frozen backbone plus episodic memory whose retrieval policy is trained with RL; +3.8% relative cumulative success |
| 2026 | [[2601.10825\|Societies-of-Thought]] | Multi-Agent · Coordination Protocol | Reveals how advanced LLMs implicitly implement multi-agent "society of mind" reasoning internally |
| 2026 | [[2603.15386\|RieMind]] | Embodied Agents · Perception in the Loop | Geometry-grounded agentic framework decoupling spatial reasoning into interpretable geometric operations |
| 2026 | [[2603.18743\|Memento-Skills]] | Memory and Skills · Persist What Worked | Skill library as external memory for continual learning; agents store and retrieve reusable skills |

---

## 1. ReAct-Style & Agentic Reasoning

The foundational paradigm for LLM agents: interleaving reasoning traces with environment actions in think-act-observe loops. These methods established that LLMs could autonomously plan and execute multi-step tasks, not just answer questions.

**Reasoning-Acting Loops** — The core think-act-observe pattern that grounds LLM reasoning in real environment feedback, enabling self-correcting multi-step execution.
- [[2507.23773|SimuRA]], [[2410.08328|Talker-Reasoner]], [[2310.04406|LATS]] (ICML'24), [[2309.15129|CogEval]] (NeurIPS'23), [[2305.18323|ReWOO]], [[2305.14992|RAP]], [[2303.17651|Self-Refine]], [[2303.11366|Reflexion]], [[2210.03629|ReAct]] (ICLR'23 Oral)

> [!star] Key Papers
> - [[2210.03629|ReAct]] (ICLR'23 Oral) — Synergizing reasoning and acting: the foundational think-act-observe loop that launched all modern LLM agents
> - [[2310.04406|LATS]] (ICML'24) — Language Agent Tree Search: unifies reasoning, acting, and planning through MCTS over action spaces
> - [[2305.14992|RAP]] — Treats the LLM as its own world model, enabling lookahead planning within the reasoning-acting framework

**Agent Harness Design** — Studies and formalisms of the fixed software layer around a model (loop, tools, context management, verification, state), measured at depth 0 with no optimization loop; loops that rewrite the harness live in [[09_Self-Evolving-AI#10. Harness Optimization & Recursive Self-Improvement|09 §10]].
- [[2610.01415|PoS]], [[2610.00972|VeriHarness]], [[2609.31847|Omni-IO-Skills]], [[2609.20804|Coding Agent Harness Study]], [[2608.01964|LongHorizon-Harness]], [[2607.28802|Model-or-Harness]], [[2603.25723|Natural-Language-Agent-Harnesses]]

**Prompt, Pipeline & Harness Optimization** - Methods that search, learn, or co-train over prompts, LM-program pipelines, agent modules, and harness code; recursive self-improvement loops are traced in [[09_Self-Evolving-AI#10. Harness Optimization & Recursive Self-Improvement|09 §10]].
- [[2609.38143|MetaSkill]], [[2609.33439|Raven]], [[2609.00196|WHALE]], [[2608.15763|HAT]], [[2608.13560|AutoDesign]], [[2607.26598|Living-Harness]], [[2605.08083|AutoTTS]], [[2604.25850|Agentic-Harness-Engineering]], [[2603.28052|Meta-Harness]], [[2603.03329|AutoHarness]], [[2602.12275|OPCD]], [[2601.21557|MCE]], [[2507.19457|GEPA]] (ICLR'26 Oral), [[2505.00147|AdaptMI]], [[2502.04306|ScoreFlow]], [[2410.10762|AFlow]], [[2410.06153|AgentSquare]], [[2406.18532|Agent Symbolic Learning]], [[2406.11695|MIPRO]], [[2406.07496|TextGrad]], [[2403.19103|PRISM-T2I]], [[2310.03714|DSPy]], [[2309.08532|EvoPrompt]], [[2309.03409|OPRO]], [[2305.03495|ProTeGi]], [[2212.10560|Self-Instruct]]

**Foundational Agent Benchmarks & Capabilities** — Landmark early benchmarks and capability studies that established what LLMs could do as autonomous agents, motivating the reasoning-acting paradigms that followed.
- [[2607.05155|EdgeBench]], [[2605.15188|FutureSim]], [[2604.08523|ClawBench]], [[2602.11964|Gaia2]] (ICLR'26 Oral), [[2510.11977|HAL]], [[2509.22391|SeekBench]], [[2505.15146|lmgame-Bench]] (ICLR'26), [[2410.09024|AgentHarm]], [[2407.01502|AI Agents That Matter]], [[2310.12823|AgentLM]], [[2307.13854|WebArena]] (ICLR'24), [[2303.12712|Sparks of AGI]], [[2210.02506|GameBugDescriptions]]

> [!tip] ReAct Set the Pattern
> ReAct's think-act-observe loop remains the default skeleton for nearly all LLM agents. LATS and RAP refined the search strategy (tree search, world-model planning), but the core loop is unchanged. When designing a new agent, start with ReAct and add structure as needed.

---

## 2. Code Agents & Program-Aided Reasoning

Agents that generate and execute code as their primary action modality. Instead of reasoning in natural language alone, these systems write programs to offload computation, compose vision modules, or perform scientific discovery.

**Mathematical & Formal Reasoning via Code** — LLMs generate executable code or formal proofs to handle computation, separating logical reasoning from arithmetic and procedural execution.
- [[2510.15700|ProofOptimizer]] (ICLR'26), [[2510.01539|Executable-Counterfactuals]] (ICLR'26), [[2506.11487|DSP+]] (NeurIPS'25), [[2506.09820|CoRT]], [[2506.07047|Mathesis]] (ICLR'26), [[2401.08190|MARIO]], [[2211.12588|PoT]], [[2211.10435|PAL]] (ICML'23)

**Domain-Specific Code Generation & Translation** — Code agents specialized for SQL, front-end, robotics, binary, and symbolic-solver targets rather than general-purpose reasoning.
- [[2609.39018|URAI]], [[2609.35432|HexaAnything]], [[2609.32416|RE-0]], [[2607.24051|HELIOS]], [[2509.25411|KeyTrace]] (ICLR'26), [[2509.22114|SK2Decompile]] (ICLR'26), [[2505.24189|SLM-vs-LLM-Low-Code-Workflows]], [[2504.08600|SQL-R1]] (NeurIPS'25), [[2504.02327|LearNAT]] (ICLR'26), [[2503.01619|Flame]], [[2305.03129|PROLEX]]

**Code-Generation Training & Quality Optimization** — RL and feedback-driven methods that train code models for correctness, multi-language coverage, and interpreter-integrated reasoning quality.
- [[2609.34587|IR4RL]], [[2609.32577|Gagar]], [[2609.22068|CodeMidas]], [[2509.25810|RA3]] (ICLR'26), [[2508.04865|Agnostics]] (ICLR'26), [[2506.20639|DiffuCoder]] (ICLR'26), [[2505.22704|REAL-Code]] (NeurIPS'25), [[2505.21668|R1-Code-Interpreter]] (ICLR'26), [[2505.12723|OORL]] (NeurIPS'25)

**Secure & Verifiable Code Generation** — Benchmarks and inference-/training-time defenses that measure and improve the security of LLM-generated code without sacrificing functional correctness.
- [[2507.19060|PurpCode]] (NeurIPS'25), [[2410.11096|SeCodePLT]], [[2405.00218|CODEGUARD+]], [[2402.09497|SafeCoder]] (ICML'24)

> [!star] Key Papers
> - [[2211.10435|PAL]] (ICML'23) — Program-aided Language Models: offload computation to a Python interpreter, separating reasoning from calculation
> - [[2211.12588|PoT]] — Program of Thoughts prompting: LLMs delegate numerical reasoning to code execution

**Visual Programming & Compositional Code** — Composing vision-and-language modules into executable programs for visual reasoning, enabling training-free compositional problem-solving.
- [[2608.21031|PhysCaP]], [[2607.25236|VisualPatchWorld]], [[2606.03047|ModuLoop]], [[2604.01600|MM-ReCoder]] (CVPR'26), [[2603.25118|AnyDoc]] (CVPR'26), [[2603.03072|TikZilla]] (ICLR'26), [[2601.05344|Im2Sim]], [[2512.03746|CodeVision]], [[2511.19661|CodeV]], [[2508.13587|Chart-to-Code-RL]] (ICLR'26), [[2508.11630|Thyme]] (ICLR'26), [[2507.20766|RRVF]], [[2505.10557|MathCoder-VL]], [[2412.04455|Code-as-Monitor]] (CVPR'25), [[2303.08128|ViperGPT]] (ICCV'23), [[2211.11559|VISPROG]] (CVPR'23)

> [!star] Key Papers
> - [[2303.08128|ViperGPT]] (ICCV'23) — Compose vision modules via Python programs for visual reasoning without any training
> - [[2211.11559|VISPROG]] (CVPR'23) — Neuro-symbolic visual programming: executable step-by-step programs from natural language queries
> - [[2512.03746|CodeVision]] — Code-as-tool framework equipping MLLMs with dynamically generated visual processing code

**Coding Agents as Robot Control Policies** - LLM-generated robot programs and coding agents that write and execute code as the manipulation policy itself, often refining from physical or simulated rollout feedback instead of training a VLA.
- [[2610.02196|InterEvolve]], [[2609.30249|RAPID-Nonprehensile]], [[2609.30233|AgenticGenPlan]], [[2609.29394|RACaP]], [[2609.27308|EmbodiedSWE]], [[2609.26499|Local Coding Agent]], [[2609.20822|SafeHarness]], [[2609.12541|AGP]], [[2608.18227|Agentic Push-T]], [[2606.16458|RHO-CodingAgent]], [[2605.02600|CoRAL]] (RSS'26), [[2604.10929|Ro-SLM]], [[2603.22435|CaP-X]], [[2603.04466|AOR]], [[2601.20334|FAEA]], [[2601.19510|ALRM]], [[2510.21302|NeSyRo]], [[2508.02629|HyCodePolicy]], [[2501.04268|RoboPro]], [[2305.16744|Demo2Code]], [[2305.11176|Instruct2Act]], [[2209.11302|ProgPrompt]], [[2209.07753|Code-as-Policies]] (ICRA'23)

**Evolutionary Algorithm & Heuristic Discovery** — Agents that autonomously discover algorithms or evolve heuristics for optimization and combinatorial problems via evolutionary/genetic search.
- [[2607.07984|AgentNAS]], [[2605.15871|AIRA-Compose]], [[2603.24517|AVO]], [[2601.18067|EvolVE]], [[2511.23473|ThetaEvolve]], [[2510.11121|RFTHGS]] (ICLR'26), [[2510.10644|LLM-Meta-Optimizer-MoD]] (NeurIPS'25), [[2510.06056|DeepEvolve]], [[2509.19349|ShinkaEvolve]] (ICLR'26), [[2509.16865|LLM-CombOpt-Solvers]] (NeurIPS'25), [[2508.05433|MLES]] (ICLR'26), [[2506.13131|AlphaEvolve]], [[2505.17866|DesignX]] (NeurIPS'25), [[2505.16053|RLAF]] (ICLR'26), [[2505.12285|CALM-Heuristic-Design]] (ICLR'26), [[2206.08896|ELM]]

**RL-Trained Code Optimization & Test Generation** — RL-driven methods that improve existing code's performance, aesthetics, or test coverage post-hoc rather than discovering new algorithms.
- [[2604.01193|SSD-Code-Generation]], [[2510.23272|AesCoder]] (ICLR'26), [[2510.14635|ATGen]] (ICLR'26), [[2510.01832|SCRIBES]] (ICLR'26), [[2509.22824|Critique-Coder]] (ICLR'26), [[2509.21016|RL-Grokking-DELTA]] (ICLR'26), [[2508.21107|UTRL]] (ICLR'26), [[2507.14111|CUDA-L1]] (ICLR'26), [[2507.11948|Kevin]] (ICLR'26), [[2506.15701|Compiler-R1]] (NeurIPS'25), [[2506.11442|ReVeal-Agent]] (ICLR'26), [[2505.23387|Afterburner]] (NeurIPS'25)

**SWE Coding-Agent Infrastructure, Benchmarks & Surveys** — Harnesses, reward models, foundation models, and benchmarks for autonomous software-engineering agents.
- [[2609.20804|Coding Agent Harness Study]], [[2608.23552|Prime Agent]], [[2608.20169|Task-CoEvolve]], [[2604.25067|Frontier-Coding-Agents-AlphaZero]], [[2603.16790|InCoder-32B]], [[2601.11868|Terminal-Bench]], [[2512.21919|SWE-RM]] (ICLR'26), [[2511.18538|Code-Intelligence-Survey]], [[2506.22419|LLM-Speedrunning-Benchmark]] (NeurIPS'25), [[2502.10517|KernelBench]], [[2502.04692|STRIDE]], [[2407.16741|OpenHands]], [[2407.01489|Agentless]], [[2405.15793|SWE-agent]], [[2310.06770|SWE-bench]], [[2105.09938|APPS]]

> [!star] Key Papers
> - [[2506.13131|AlphaEvolve]] — Google DeepMind combines LLMs with evolutionary search to autonomously discover algorithms, finding new mathematical results
> - [[2511.18538|Code-Intelligence-Survey]] — Comprehensive synthesis of LLMs for automated software development across the full model lifecycle

**Code World Models** - Agents that write executable programs as world models (transition, reward, or game-rule code), then plan or learn against them instead of a neural simulator.
- [[2609.35047|EMPIRIC]], [[2608.27549|Code-as-World]], [[2608.25927|Code World Model]], [[2606.16070|Mind-Studio]], [[2605.30880|PatchWorld]], [[2602.01576|gWorld]], [[2510.04542|CWM-Games]], [[2505.10819|PoE-World]], [[2405.15383|GIF-MCTS]], [[2402.12275|WorldCoder]]

**3D Scene & Asset Synthesis via Code** - Agents that write Blender, procedural, or scene-program code to build, reconstruct, or edit 3D assets and interactive environments.
- [[2609.11499|RCWM]], [[2608.24212|NeoWorld-Pro]], [[2608.18840|RoomWright]], [[2606.02580|SEIG]], [[2606.01869|WorldCoder-Bench]], [[2605.19587|SceneCode]], [[2605.18451|Code-as-Room]], [[2605.14700|SR-Platform]], [[2601.11109|VIGA]], [[2508.08228|LL3M]], [[2403.01248|SceneCraft]], [[2310.12945|3D-GPT]]

> [!tip] Code Beats Language for Computation
> PAL and PoT proved that LLMs should not do arithmetic -- they should write code that does arithmetic. ViperGPT extended this to vision: compose perception modules via programs. The pattern generalizes: whenever reasoning involves precise computation or systematic search, delegate to code.

---

## 3. Tool-Augmented Reasoning & RL

Training LLMs to learn when and how to invoke external tools through reinforcement learning, rather than relying on handcrafted prompting. This section covers the transition from prompted tool use to learned tool-use policies.

**Search & Retrieval-Augmented Tool-Use RL** — RL frameworks that train LLMs specifically to invoke search/retrieval tools and integrate retrieved evidence into reasoning chains.
- [[2608.08944|Pair-ID]], [[2605.28828|Micro-Macro-Retrieval]] (ICLR'26), [[2603.22293|TIPS-RL]] (ICLR'26), [[2602.22225|SmartChunk]] (ICLR'26), [[2511.07328|Q-RAG]] (ICLR'26 Oral), [[2510.27566|Interact-RAG]] (ICLR'26), [[2510.07794|HiPRAG]] (ICLR'26), [[2509.01092|REFRAG]], [[2505.14069|ReasonRAG]] (NeurIPS'25), [[2505.09316|InForage]] (NeurIPS'25 Spotlight), [[2505.07233|DynamicRAG]] (NeurIPS'25), [[2505.04588|ZeroSearch]], [[2504.20595|ReasonIR]], [[2503.19470|ReSearch]] (NeurIPS'25), [[2503.09516|Search-R1]], [[2503.05592|R1-Searcher]], [[2501.05366|Search-o1]], [[2412.14835|AR-MCTS]]

**General Tool-Integrated Reasoning RL Frameworks** — Domain-agnostic RL frameworks that teach LLMs when and how to invoke arbitrary tools during reasoning.
- [[2603.13348|AutoTool]] (ICLR'26), [[2509.23285|Tool-Light]] (ICLR'26), [[2509.21826|ResT-RL]] (ICLR'26), [[2509.17325|CodeGym]] (ICLR'26), [[2509.02479|SimpleTIR]] (ICLR'26), [[2509.01055|VerlTool]], [[2505.07773|ZeroTIR]], [[2505.00024|Nemotron-Research-Tool-N1]] (ICLR'26), [[2504.13958|ToolRL]] (NeurIPS'25), [[2504.11536|ReTool]] (ICLR'26), [[2504.04736|SWiRL]], [[2503.23383|ToRL]]

**Embodied & Robotic Tool Use** — Tool-use RL and functional-tool-grounding methods applied to embodied and robotic agents.
- [[2609.35318|DexAgent]], [[2609.27340|MCP Robot Navigation]], [[2608.05738|VLA-Talker]], [[2607.05780|FORGE]], [[2605.26637|Embodied-Tool-Protocol]], [[2605.13119|VLAs-as-Tools]], [[2602.09430|AtomBridge]], [[2510.14902|VLA2]]

> [!star] Key Papers
> - [[2504.11536|ReTool]] (ICLR'26) — ByteDance's RL framework enabling LLMs to dynamically decide when to invoke tools during reasoning
> - [[2504.13958|ToolRL]] (NeurIPS'25) — Novel reward shaping for tool-use RL; meticulously designed rewards guide optimal tool invocation
> - [[2503.23383|ToRL]] — Scaling tool-integrated RL: trains LLMs to autonomously learn when and how to use tools

**Agentic Tool Integration Frameworks** — Unified frameworks that combine reasoning, tool invocation, and multi-step planning into coherent agent architectures.
- [[2512.20745|AgentMath]] (ICLR'26), [[2510.06217|TaTToo]] (ICLR'26), [[2510.05592|AgentFlow]] (ICLR'26 Oral), [[2507.05707|Agentic-R1]], [[2506.14728|AgentDistill]], [[2506.12115|Cognitive-Tools]] (NeurIPS'25), [[2505.05177|MARK]], [[2505.01441|ARTIST]], [[2504.21776|WebThinker]] (NeurIPS'25), [[2503.23278|MCP Security Survey]], [[2402.01030|CodeAct]] (ICML'24)

> [!star] Key Papers
> - [[2505.01441|ARTIST]] — Microsoft Research unifies agentic reasoning, dynamic tool integration, and RL training in a single framework
> - [[2507.05707|Agentic-R1]] — DualDistill framework training language models as tool-using agents via distillation and RL
> - [[2506.14728|AgentDistill]] — Training-free distillation of tool-use capabilities from large to small models
> - [[2506.15692|MLE-STAR]] (NeurIPS'25) — LLM agent automating machine learning engineering by leveraging web search and tool composition

**Video & Long-Horizon Visual Tool Use** — Tool-augmented RL methods for reasoning over long or streaming video via native tool calling and adaptive focus.
- [[2603.22918|EVA-Video-Agent]] (CVPR'26), [[2602.20913|LongVideo-R1]] (CVPR'26), [[2601.13942|GoG]], [[2512.22315|VideoZoomer]] (ICLR'26), [[2512.10359|STAR]] (NeurIPS'25), [[2511.20785|LongVT]] (CVPR'26), [[2511.20085|VICoT-Agent]], [[2511.13026|REVISOR]], [[2510.08480|Video-STAR]] (ICLR'26), [[2508.04416|VITAL]]

**Adaptive Visual Tool Selection & Compositional Reasoning** — Methods enabling vision-language models to select, compose, and invoke visual tools (detectors, segmenters, editors, CAD/3D solvers) on demand during reasoning.
- [[2608.29374|ReVISE-SelfCorrect]], [[2605.15198|ATLAS]], [[2605.09218|Flame3D]], [[2605.07177|HyperEyes]], [[2604.21409|S1-VL]], [[2603.23483|SpecEyes]] (ECCV'26), [[2603.17729|SARE]], [[2512.17312|CodeDance]] (CVPR'26), [[2512.16918|AdaTooler-V]], [[2511.19773|VISTA-Gym]], [[2510.27363|ToolScope]], [[2510.09733|EVisRAG]], [[2509.07969|Mini-o3]] (ICLR'26), [[2509.01656|ReV-PT]], [[2508.12109|Simple-o3]], [[2505.08617|OpenThinkIMG]], [[2504.21561|SPORT]] (NeurIPS'25), [[2503.19263|DWIM]] (ICCV'25), [[2412.18072|MMFactory]], [[2412.13810|CAD-Assistant]] (ICCV'25), [[2412.05479|LATTE]]

> [!star] Key Papers
> - [[2412.05479|LATTE]] — Trains open-source VLMs to integrate external tools for complex multimodal reasoning
> - [[2512.16918|AdaTooler-V]] — MLLM that adaptively decides when external vision tools are needed; RL-trained selective tool invocation
> - [[2505.08617|OpenThinkIMG]] — Open-source framework for interleaved visual tool use during reasoning
> - [[2509.01656|ReV-PT]] — RL-trained visual tool-use policy for compositional reasoning across detectors, segmenters, and editors

**Agentic Image & Video Editing** - Agents that plan and orchestrate editing or generation tools, or emit code, across multi-turn image and video creation tasks.
- [[2609.34309|MaLiang-Harness]], [[2607.27380|VideoCoCo]], [[2607.05465|CanvasAgent]], [[2606.23327|VideoAgent-Edit]], [[2603.29602|IMAGAgent]], [[2509.12883|Lego-Edit]], [[2509.10761|EditDuet]], [[2506.20911|FaSTA*]], [[2503.10613|CoSTA*]]

**Routing, Composition & Model Selection** — Meta-agents that dynamically select, compose, or route between multiple models and tools to match task requirements.
- [[2604.23626|GraphPlanner]] (ICLR'26), [[2601.03872|ATLAS]], [[2512.24330|SenseNova-MARS]], [[2506.09033|Router-R1]] (NeurIPS'25), [[2506.04632|Risk-Sensitive-Agents]] (ICLR'26)

> [!star] Key Papers
> - [[2506.09033|Router-R1]] (NeurIPS'25) — RL-trained router that learns to dispatch queries to the optimal model or tool combination
> - [[2512.24330|SenseNova-MARS]] — SenseTime's multimodal agentic reasoning and search system integrating diverse tools and models

> [!tip] From Prompted to Learned Tool Use
> Early agents used handcrafted prompts to invoke tools (ReAct, Toolformer). ReTool, ToolRL, and ToRL showed that RL can learn tool-use policies that surpass prompting. The key insight: tool invocation is a decision problem, and RL is better at decision problems than prompting.

---

## 4. Multi-Turn & RL-Trained Agents

Agents trained via reinforcement learning for multi-turn interactions with environments, moving beyond single-call tool use to sustained, stateful task execution across many steps.

**Multi-Turn Policy-Optimization Algorithms (GRPO Variants & Credit Assignment)** — GRPO-family and related algorithmic variants that tackle credit assignment and turn-level optimization in multi-turn agent RL.
- [[2609.13739|HarnessBandit]], [[2609.13443|NGU]], [[2609.02042|SPACE]], [[2608.17310|Agentic ESOpt]], [[2608.16072|SA-MRPO]], [[2608.05987|AgentOPSD]], [[2607.21653|Molt]], [[2607.07508|SAO]], [[2607.05804|TurnOPD]], [[2607.05339|TREK]], [[2607.04763|ReOPD]], [[2606.03963|AgenticRL]], [[2605.28774|AXPO]], [[2605.20246|GROW]], [[2605.10899|RubricEM]], [[2605.10663|Evolving-RL]], [[2602.22817|HGPO]] (ICLR'26), [[2512.16848|LAMER]] (ICLR'26), [[2510.20150|Rank-GRPO]] (ICLR'26), [[2510.14967|IGPO-Info-Gain]] (ICLR'26), [[2509.21240|Tree-GRPO]] (ICLR'26), [[2508.03680|Agent-Lightning]], [[2505.10978|GiGPO]] (NeurIPS'25)

**Reward Design, Exploration, Environments & Evaluation for Multi-Turn Agents** — Reward shaping, exploration strategies, training environments, and diagnostic evaluation for sustained multi-turn agent-environment interaction.
- [[2608.06197|EnvACE]], [[2607.05378|CompactionRL]], [[2604.06268|RAGEN-2]], [[2602.02196|TIDE]], [[2511.07327|IterResearch]] (ICLR'26), [[2510.10197|Environment-Tuning]] (ICLR'26), [[2509.19199|iStar]] (ICLR'26), [[2509.08755|AgentGym-RL]], [[2507.17842|Shop-R1]] (ICLR'26), [[2506.00539|ARIA]] (NeurIPS'25 Spotlight), [[2504.20997|LLM-PSRL]] (ICLR'26), [[2504.16078|LLM-Greedy-Agents]] (ICLR'26), [[2504.03206|CURIO]] (NeurIPS'25), [[2408.10899|ARIO]], [[2406.04151|AgentGym]], [[2007.07853|γ-Progress]]

> [!star] Key Papers
> - [[2504.20073|RAGEN]] — Multi-turn RL training for LLM agents; establishes the training paradigm for sustained agent-environment interaction
> - [[2510.01132|Multi-turn-Agentic-RL-Guide]] — Systematic practical guide from UCSD and NVIDIA for training multi-turn LLM agents
> - [[2508.03680|Agent-Lightning]] — Microsoft Research decouples RL training from inference, enabling scalable agent training
> - [[2505.10468|AI-Agents-vs-Agentic-AI]] — Cornell taxonomy distinguishing AI agents (autonomous entities) from agentic AI (design pattern); essential conceptual clarity
> - [[2509.02547|Agentic-RL-Landscape-Survey]] — Formal definition of agentic RL for LLMs using Partially Observable Markov Decision Processes
> - [[2406.04151|AgentGym]] — Landmark multi-environment benchmark; agents evolve via behavioral cloning + self-evolution across diverse environments

**Verifiable Reasoning & Meta-Reasoning** — Agents that verify their own reasoning steps, use meta-cognitive strategies, or integrate judges for reliable multi-step execution.
- [[2607.05391|LLM-as-a-Verifier]], [[2605.03782|GLANCE]] (ICML'26 Spotlight), [[2511.01833|TIR-Bench]], [[2510.23038|TIR-Judge]] (ICLR'26), [[2510.08191|Training-Free-GRPO]], [[2509.15172|MACA]], [[2508.10874|SSRL]], [[2507.22844|RLVMR]] (ICLR'26)

> [!star] Key Papers
> - [[2507.22844|RLVMR]] (ICLR'26) — Verifiable meta-reasoning rewards improve long-horizon agent performance by rewarding sound reasoning process, not just outcomes
> - [[2510.23038|TIR-Judge]] (ICLR'26) — LLM judge framework integrating tool-invoked reasoning for reliable multi-step evaluation

**Dynamic Planning & Adaptive Agents** — Agents that dynamically revise plans during execution, adapting to unexpected observations rather than following fixed scripts.
- [[2609.28416|AEWM]], [[2608.01964|LongHorizon-Harness]], [[2607.04162|ACE-Manipulation]], [[2605.22138|SR2AM]], [[2605.09131|MCP-Cosmos]], [[2602.21728|Explore-on-Graph]] (ICLR'26), [[2512.23167|SPIRAL]], [[2512.09706|CrossHA]] (CVPR'26 Highlight), [[2510.09577|Dyna-Mind]] (ICLR'26), [[2509.01920|DSP-Speculative]] (ICLR'26), [[2508.20722|rStar2-Agent]], [[2507.11988|Aime]], [[2507.08664|INoT]], [[2203.03485|Self-directed-Exploratory-Planning]]

> [!star] Key Papers
> - [[2507.11988|Aime]] — ByteDance multi-agent framework overcoming static planning limitations with dynamic plan revision
> - [[2508.20722|rStar2-Agent]] — Microsoft's agentic reasoning model enabling LLMs to "think slow" with structured deliberation over action spaces
> - [[2512.24601|RLMs]] — Recursive Language Models: inference-time paradigm for iterative computation within a single forward pass

> [!tip] Multi-Turn Is the Real Challenge
> Single-turn tool calls are largely solved. The frontier is multi-turn: agents that maintain state, recover from errors, and adapt strategy over 10-100 steps. RAGEN and the Multi-turn RL Guide show that standard RL techniques need significant modification for this setting -- reward sparsity, credit assignment, and state tracking are all harder.

---

## 5. Web Agents & GUI Interaction

Agents that operate in real digital environments -- browsing the web, interacting with GUIs, and completing tasks in applications. These bridge language understanding with pixel-level perception and action.

**Web Navigation & Browsing Agents** — Agents that navigate websites, fill forms, and complete multi-step web tasks by combining visual perception with action planning.
- [[2603.20278|OpenResearcher]], [[2603.05044|WebFactory]] (ICLR'26), [[2601.21872|WebArbiter]] (ICLR'26), [[2512.23676|WWM]], [[2510.19245|See-Think-Act-Shopper]], [[2510.18798|WebSeer]] (ICLR'26), [[2509.24107|Fathom-DeepResearch]] (ICLR'26), [[2509.22644|WebGen-Agent]] (ICLR'26), [[2509.13305|WebSailor-V2]] (ICLR'26), [[2508.07976|ASearcher]], [[2508.05748|WebWatcher]], [[2507.04103|LLM-Web-Agent-Diagnosis]] (NeurIPS'25), [[2505.24332|DeepDiver]], [[2505.22648|WebDancer]] (NeurIPS'25), [[2504.21024|WebEvolver]]

> [!star] Key Papers
> - [[2512.23676|WWM]] — Princeton's Web World Models: a new architectural paradigm where agents build predictive models of web environments for planning
> - [[2510.19245|See-Think-Act-Shopper]] — VLM-driven framework simulating online shopping tasks end-to-end

**GUI & Multi-Application Agents** — Agents that interact with graphical user interfaces across multiple applications, combining screen understanding with structured actions.
- [[2604.11201|CocoaBench]], [[2604.06126|Gym-Anything]], [[2603.24533|UI-Voyager]], [[2603.02951|CGL]], [[2511.22235|CES-Scheduler]] (CVPR'26), [[2511.07332|GroundCUA]] (ICLR'26), [[2510.20286|UI-Ins]] (ICLR'26), [[2510.09872|WARC-Bench]] (ICLR'26), [[2509.18119|MobileRL]] (ICLR'26), [[2508.14040|ComputerRL]] (ICLR'26), [[2508.09736|M3-Agent]] (ICLR'26), [[2508.04389|GuirlVG]] (ICLR'26), [[2508.03923|CoAct-1]], [[2507.05791|GTA1]] (ICLR'26), [[2505.15810|GUI-G1]] (NeurIPS'25), [[2505.12493|GUI-Shift]] (ICLR'26), [[2505.12370|SE-GUI]] (NeurIPS'25)

> [!star] Key Papers
> - [[2508.03923|CoAct-1]] — Multi-agent framework integrating both GUI interactions and direct programmatic API access
> - [[2508.09736|M3-Agent]] (ICLR'26) — ByteDance's multimodal agent processing continuous video and GUI streams for real-time task completion

> [!tip] Web Agents Need World Models
> WWM's key insight: web agents that build predictive models of what happens next (like a chess engine) outperform reactive agents that just observe and act. The web is a partially observable environment, and planning beats reacting.

---

## 6. Multi-Agent Systems & Orchestration

Systems where multiple LLM agents collaborate, specialize, or compete. Multi-agent architectures enable division of labor, debate-based reasoning, and scalable task decomposition that single agents cannot achieve.

**Physical & Robotic Multi-Agent Coordination** — Multi-agent architectures coordinating physical or scientific-domain systems: multi-robot teams, industrial governance, chip placement, and infrastructure control.
- [[2609.35651|D4ORM]], [[2609.32745|MORPH]], [[2609.08220|AID-SR]], [[2607.18536|MAGE-MacroPlacement]], [[2607.12050|EFLUX]], [[2607.07403|Megamind]], [[2606.31339|Verification-Gated Mission Governance]], [[2606.25404|HEART]], [[2602.14926|MAC-AMP]] (ICLR'26), [[2506.18448|GraspMAS]] (IROS'25), [[2505.19486|VLMLight]] (NeurIPS'25), [[2503.11739|CoLLMLight]] (ICLR'26), [[2409.10106|Industry 6.0]] (IROS'25)

**Multi-Agent Orchestration & Training** - Architectures and RL fine-tuning methods for coordinating and training teams of software agents.
- [[2604.01658|CORAL]], [[2601.19204|MATA]] (ICLR'26), [[2601.10825|Societies-of-Thought]], [[2601.09295|MACRO-LLM]], [[2512.04388|Conductor]] (ICLR'26), [[2510.11062|AT-GRPO]] (ICLR'26), [[2509.24323|MAS²]], [[2508.13167|CoA]], [[2507.01701|LbMAS]], [[2506.12508|AgentOrchestra]], [[2505.23885|OWL-Workforce]] (NeurIPS'25), [[2505.19591|Puppeteer-Agent]] (NeurIPS'25), [[2504.16129|MARFT]], [[2504.01990|Foundation-Agents-Survey]], [[2501.15228|MMOA-RAG]] (NeurIPS'25)

**Multi-Agent Failure Diagnosis & Attribution** - Tools that trace, attribute, and repair failures in multi-agent and agent-harness runs.
- [[2608.25920|SymTrace]], [[2608.11772|DARC]], [[2608.05906|MERIT]], [[2607.28802|Model-or-Harness]], [[2606.09071|REFLECT-Attribution]], [[2605.25338|CausalFlow]], [[2604.25135|FAMA]], [[2509.14295|Aegis-Agent]] (ICLR'26), [[2509.03312|AgenTracer]] (ICLR'26)

**Latent & Direct Agent Communication** - Agents that exchange latent states or caches instead of verbose natural-language messages.
- [[2604.24881|Latent-Agents]], [[2511.20639|LatentMAS]] (ICML'26 Spotlight), [[2510.03215|C2C]]

> [!star] Key Papers
> - [[2504.01990|Foundation-Agents-Survey]] — Brain-inspired comprehensive framework integrating diverse LLM agent research areas
> - [[2506.12508|AgentOrchestra]] — TEA protocol (Tool-Environment-Agent) for unified multi-agent management and task orchestration
> - [[2504.16129|MARFT]] — Multi-Agent Reinforcement Fine-Tuning: RL-based optimization of LLM multi-agent systems
> - [[2511.20639|LatentMAS]] (ICML'26 Spotlight) — Agents collaborate through latent-space communication rather than verbose natural language exchanges
> - [[2601.10825|Societies-of-Thought]] — Reveals how advanced LLMs implicitly implement multi-agent "society of mind" reasoning internally

**Multi-Agent Frameworks & Topology Search** - Role-playing and conversation frameworks and agent operating systems for building multi-agent applications, plus methods that automatically search agent graphs, prompts, and topologies.
- [[2504.15257|FlowReasoner]], [[2502.04180|MaAS]], [[2502.02533|MASS-MultiAgent]], [[2406.14228|EvoAgent-MAS]], [[2403.16971|AIOS]], [[2402.16823|GPTSwarm]], [[2308.08155|AutoGen]], [[2308.00352|MetaGPT]]

**Co-Evolution & Group Dynamics** — Multiple agents that evolve together, with competitive or cooperative dynamics driving collective improvement beyond what individual agents achieve.
- [[2609.22682|Self-Organizing Agent Teams]], [[2607.22529|Skill-SP]], [[2604.22446|Skills-to-Talent]], [[2604.20987|Co-Evolve-Agents]], [[2602.04837|GEA]], [[2601.09667|MATTRL]], [[2510.27072|Self-Play Reasoning Analysis]], [[2510.23595|MAE]], [[2510.18821|Search-Self-play]] (ICLR'26), [[2510.08529|CoMAS]] (ICLR'26), [[2506.24119|SPIRAL]] (ICLR'26), [[2410.17517|Maynard-Cross-Learning]]

> [!star] Key Papers
> - [[2602.04837|GEA]] — Group-Evolving Agents: agents co-evolve in groups, with emergent specialization and collective capability growth
> - [[2601.09667|MATTRL]] — Multi-Agent Test-Time Reinforcement Learning from MIT/NUS/Microsoft; agents coordinate adaptation at inference time

> [!tip] Multi-Agent as Scaling Strategy
> Multi-agent systems offer a different scaling axis than bigger models: instead of more parameters, use more specialized agents. AgentOrchestra and MARFT show this works in practice. The key challenge is coordination cost -- LatentMAS addresses this by replacing verbose text communication with compact latent messages.

---

## 7. Memory, Planning & Self-Evolution

Agents that accumulate experience over time, build persistent memory, and reuse skills across tasks. Self-evolving agents that retrain on their own experience are in [[09_Self-Evolving-AI#4. Self-Evolving Agents|09 §4]]; loops that rewrite the harness or the improver itself, and their benchmarks, are in [[09_Self-Evolving-AI#10. Harness Optimization & Recursive Self-Improvement|09 §10]].

**Agent Memory Architectures & Systems** — Persistent episodic, semantic, and working-memory systems that let agents recall and reuse information across long or lifelong interactions.
- 2026 · [[2609.19656|SELF-INDEX]], [[2608.24876|Recuris]], [[2608.23982|Conditional-Memory]], [[2608.06663|Horizon Gap]], [[2607.09759|ReflectWorld-MM]], [[2607.01988|Identity-Stable Consolidation]], [[2606.23283|RootMem]], [[2606.03374|eMEM]], [[2605.15128|MemEye]], [[2605.10870|DeMem]], [[2605.07313|Scale-Conditioned Agent Memory]], [[2604.07985|RAG-Benefit-Prediction]], [[2604.04503|MIA]], [[2604.01560|DeltaMem]], [[2604.01007|Omni-SimpleMem]], [[2603.29493|MemFactory]], [[2603.05218|KARL]], [[2602.16313|MemoryArena]], [[2602.06052|Agent Memory Survey]]
- 2023-2025 · [[2512.23343|Agent Memory Survey 2025]], [[2512.20092|Memory-T1]] (ICLR'26), [[2512.13564|AI-Agent-Memory-Survey]], [[2511.14004|STAR-Memory-Action]], [[2510.04618|ACE]] (ICLR'26), [[2509.23040|ReMemR1]] (ICLR'26), [[2508.06433|Memp]], [[2508.01415|RoboMemory]], [[2506.15841|MEM1]] (ICLR'26), [[2504.15965|AI-Memory-Survey]], [[2504.07952|Dynamic Cheatsheet]], [[2409.18313|Embodied-RAG]], [[2409.07429|AWM-Agent]], [[2310.08560|MemGPT]], [[2308.10144|ExpeL]]

**Skill Libraries, Discovery & Internalization** — Agents that maintain persistent, reusable skill repositories and discover or internalize new skills without retraining.
- [[2609.37810|RoboSkill]], [[2609.35690|APPL]], [[2609.30674|SkillRefine]], [[2609.11682|COBRA-Skills]], [[2609.05571|Code2Skill]], [[2608.24747|SkillForge]], [[2608.02636|Feedback-Conditioned Skill Evolution]], [[2607.08448|Harness-VLA]], [[2607.00272|ASPIRE]], [[2606.29538|Resource2Skill]], [[2606.08671|SkillHone]], [[2605.19576|Ratchet]], [[2605.06614|SkillOS]], [[2604.27488|Skills-Coach]], [[2604.04804|SkillX]], [[2604.02268|SKILL0]], [[2604.01687|EvoSkills]], [[2603.18743|Memento-Skills]], [[2603.12056|XSkill]] (ICML'26), [[2602.08234|SkillRL]], [[2505.20286|Alita]], [[2504.07079|SkillWeaver]], [[2305.16291|Voyager]]

> [!star] Key Papers
> - [[2305.16291|Voyager]] — Automatic curriculum plus an ever-growing library of executable skills; discovered 3.3x more unique items than prior agents
> - [[2603.18743|Memento-Skills]] — Skill library as external memory with a behaviour-aligned router; GAIA 52.3% -> 66.0%, HLE 17.9% -> 38.7%

**Memory-Integrated RL & Self-Evolving Memory** — RL and evolutionary-search methods where the memory or planning trace itself is the object being trained or evolved.
- [[2608.10504|MEGA]], [[2607.28272|MemHarness]], [[2603.24639|ERL]] (ICLR'26 Workshop), [[2602.23008|EMPO-squared]] (ICLR'26), [[2602.17930|MIRA-RL]] (ICLR'26), [[2601.03192|MemRL]], [[2512.18746|MemEvolve]], [[2510.12635|MemAct]], [[2509.25140|ReasoningBank]] (ICLR'26)

> [!star] Key Papers
> - [[2603.18743|Memento-Skills]] — Skill library as external memory for continual learning; agents store and retrieve reusable skills without weight updates
> - [[2603.05218|KARL]] — Knowledge agent via off-policy RL for grounded reasoning over enterprise knowledge bases

> [!tip] Memory Makes the Agent
> Without persistent memory, an agent is a stateless function call. Memento-Skills shows the gain comes from the library, not the model: on a frozen backbone, rewriting and routing skills lifts GAIA from 52.3% to 66.0% and HLE from 17.9% to 38.7%, and the training success rate keeps rising across three rounds (65.1% -> 91.6%). KARL gets its gains the other way, training search behaviour with RL: 37% shorter search trajectories and, on BrowseComp-Plus, 37% more unique documents retrieved.

---

## 8. Multimodal & Embodied Agents

Agents that process visual, spatial, and multi-sensory inputs alongside language, enabling interaction with physical and visual environments beyond text-only tasks.

**Physical Robot Agent Architectures & Manipulation** — Integrated architectures combining vision-language understanding with agent capabilities for real-world robot manipulation and interaction.
- [[2609.29091|Agentic Embodied Manipulation]], [[2609.09808|GTA-2]], [[2609.01281|EmbodiedSkills]], [[2608.29896|EMERGE-Policy]], [[2608.03924|ETA]], [[2607.23784|ARCHITECT]], [[2607.12894|Hy-Embodied-VLM-1.0]], [[2607.11119|VIA]], [[2607.10350|ABot-AgentOS]], [[2607.05377|Cortex]], [[2607.04426|ACE-Brain-0.5]], [[2606.30632|GROW²]], [[2606.16295|VisualClaw]], [[2605.21133|Spatial-Brain-Cerebellum]], [[2604.20348|BiCICLe]], [[2512.21220|RoboSafe]], [[2510.21817|VITA-E]], [[2505.20424|ApBot]]

**Robot Harnesses Around a Frozen Policy** - Scaffolds of code, skills, memory and verifiers that steer a fixed VLA or VLM at runtime, improved without weight updates.
- [[2610.02204|RPG-Robot]], [[2609.40306|DynaHarness]], [[2609.39304|Scale and Selection]], [[2609.38078|MotorMind]], [[2609.37583|RoboHarn-Evo]], [[2609.34276|NavHarness]], [[2609.33378|RHD]], [[2609.32862|RoboFoundry]], [[2609.29964|WAA]], [[2609.29389|K1]], [[2609.29204|AdaHVLA]], [[2609.19138|GPT-Policy]], [[2607.26148|Agentic Embodied Control]], [[2607.18060|RoboHarness]], [[2607.16636|PhyAgentOS]], [[2606.05395|VASO]]

**Embodied Simulation, World Engines & Foundational Benchmarks** — Simulated worlds, 3D scene engines, and benchmark environments underpinning embodied multimodal agent research.
- [[2610.00854|Embodied Agent Arena]], [[2608.15265|VibeWorlding]], [[2608.05248|WorldClaw]], [[2607.11377|PHILIA]], [[2607.07534|LingBot-World-Infinity]], [[2607.07459|EmbodiedGen V2]], [[2412.13178|SafeAgentBench]], [[2410.06237|BUMBLE]], [[2403.19622|RH20T-P]] (NeurIPS'24 Workshop), [[2304.04321|ARNOLD]], [[2210.03094|VIMA]] (ICML'23), [[1806.07011|VirtualHome]] (CVPR'18)

**General Multimodal Vision-Agent Architectures** — Vision-language agents for non-embodiment tasks: image/video understanding, generalized visual search, and domain-specialized reasoning.
- [[2602.17558|RetouchIQ]], [[2512.18745|InSight-o3]] (ICLR'26), [[2512.05111|ARM-Thinker]], [[2511.19524|VideoChat-M1]] (CVPR'26), [[2511.05271|DeepEyesV2]] (ICLR'26)

> [!star] Key Papers
> - [[2402.15116|LMA-Survey]] — Systematic review of Large Multimodal Agents deconstructing their core components and capabilities
> - [[2403.12884|HYDRA]] (ECCV'24) — Multi-stage dynamic compositional visual reasoning integrating an RL agent as cognitive controller
> - [[2311.05437|LLaVA-Plus]] (ECCV'24) — Training VLMs to learn when and how to use external visual tools for any task

**VLM Fine-Tuning & Reinforcement for Agency** — Methods for fine-tuning vision-language models via RL to act as agents in visual environments.
- [[2607.13818|Agentic Execution RL]], [[2607.13653|REAL]] (ECCV'26), [[2604.08545|Metis]], [[2512.00961|GenReward]] (CVPR'26)

> [!star] Key Papers
> - [[2405.10292|VLM-RL-Fine-Tuning]] (NeurIPS'24) — Directly fine-tuning VLMs with RL for agentic visual tasks; bridges perception and action
> - [[2505.14246|Visual-ARFT]] — Reinforcement fine-tuning framework for visual agents from Shanghai AI Lab

**Spatial Intelligence & Geometry Grounding** — Agents that reason about 3D space, geometric relationships, and physical structure for grounded problem-solving.
- [[2603.15386|RieMind]], [[2602.10116|SAGE]], [[2512.10534|InternGeometry]] (ICLR'26), [[2512.04069|SpaceTools]] (CVPR'26), [[2504.09848|LLM-Spatial-Intelligence-Survey]], [[2408.16662|Space3D-Bench]] (ECCV'24 Workshop)

> [!star] Key Papers
> - [[2504.09848|LLM-Spatial-Intelligence-Survey]] — Comprehensive survey examining how LLMs enable spatial intelligence across domains
> - [[2603.15386|RieMind]] — Geometry-grounded agentic framework decoupling spatial reasoning into interpretable geometric operations

> [!tip] Vision Is the Missing Sense
> Most LLM agents are "blind" -- they operate on text APIs. Multimodal agents like HYDRA and M3-Agent show that adding visual perception dramatically expands the task space (GUI interaction, scientific visualization, physical manipulation). The bottleneck has shifted from architecture to training data for visual agency.

---

## 9. Scientific & Research Agents

Agents that automate the research loop itself, from literature review and idea generation to experiment execution and paper writing, plus the benchmarks that grade them on end-to-end research and ML-engineering work.

**Scientific & Research Agents** — Agents designed for autonomous scientific research, from literature review to experiment design and execution.
- 2026 · [[2609.26457|AIDE²]], [[2607.27191|Shadow Evaluation]], [[2607.15079|BrainPilot]], [[2607.04508|Agentic Self-Driving Lab]] (ICML'26 Workshop), [[2607.04439|IdeaSpark]], [[2607.04438|ResearchStudio-Reel]], [[2606.21891|ARTS]], [[2605.03808|Agentic-imodels]], [[2604.28158|Intern-Atlas]], [[2604.05550|AutoSOTA]], [[2603.29557|FlowPIE]], [[2603.26499|AIRA2]], [[2603.23420|Bilevel Autoresearch]], [[2603.17216|ML-AutoResearch]], [[2603.07642|Helix-Scientific]] (ICLR'26), [[2602.24288|DARE-bench]] (ICLR'26), [[2601.23265|PaperBanana]], [[2601.19439|OSIRIS]] (ICLR'26), [[2601.15715|RebuttalAgent]] (ICLR'26), [[2601.10402|ML-Master-2.0]], [[2601.03315|LLMs Aren't Scientists Yet]]
- 2024-2025 · [[2511.16072|GPT-5 Science Acceleration]], [[2511.02824|Kosmos-AI-Scientist]], [[2510.11661|SR-Scientist]] (ICLR'26), [[2509.01684|ML-Engineering-RL-Agents]] (ICLR'26), [[2506.15692|MLE-STAR]] (NeurIPS'25), [[2506.02153|SLMs-for-Agentic-AI]], [[2505.21497|PosterAgent]], [[2505.16938|InternAgent]], [[2504.08066|AI Scientist-v2]], [[2504.01538|AI-Newton]], [[2503.18102|AgentRxiv]], [[2502.14297|Sakana AI Scientist Evaluation]], [[2502.13138|AIDE]], [[2501.03916|DOLPHIN]], [[2411.00816|CycleResearcher]], [[2408.06292|The AI Scientist]], [[2404.07738|ResearchAgent]]

> [!star] Key Papers
> - [[2505.16938|InternAgent]] — Unified closed-loop multi-agent system for fully autonomous scientific research
> - [[2511.02824|Kosmos-AI-Scientist]] — Multi-agent architecture with structured world knowledge for autonomous scientific discovery
> - [[2506.02153|SLMs-for-Agentic-AI]] — NVIDIA/Georgia Tech argument that Small Language Models are optimal for deployable agentic systems

**Research & ML-Engineering Agent Benchmarks** - Benchmarks that grade agents on reproducing papers, running experiments, and doing ML or R&D engineering end to end.
- [[2609.34210|RLE-Bench]], [[2505.24785|EXP-Bench]], [[2504.01848|PaperBench]], [[2411.15114|RE-Bench]], [[2410.07095|MLE-bench]], [[2410.05080|ScienceAgentBench]], [[2409.11363|CORE-Bench]]

---

## Cross-References

- [[07_Reasoning-and-Planning]] — Reasoning foundations for agents (CoT, search, planning)
- [[08_Reinforcement-Learning]] — RL training methods powering agent learning
- [[09_Self-Evolving-AI]] — Self-improving and continually learning agents
- [[11_Robotics-and-Embodied-AI]] — Embodied agents in physical environments
- [[06_Multimodal-LLMs]] — Multimodal foundations for visual agents
- [[12_Benchmarks-and-Surveys]] — Agent evaluation benchmarks

---

*Next: [[11_Robotics-and-Embodied-AI]] for how agentic reasoning and tool use extend into physical embodiment.*