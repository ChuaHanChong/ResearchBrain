---
title: "Research Roadmap: Self-Evolving Fast-WAM"
tags:
  - self-evolving
  - WAM
  - robotics
  - Fast-WAM
  - roadmap
aliases:
  - "Self-Evolving WAM Roadmap"
  - "Fast-WAM Research Steps"
---

# Research Roadmap: Self-Evolving Fast-WAM

> [!abstract] What This Document Is
> A step-by-step research and implementation roadmap for making [[2603.16666|Fast-WAM]] self-evolving. Each phase lists: what to do, what data/benchmarks are needed, which papers' methods matter, and how to know when you're done. For the full reasoning, see [[02_How-to-Build-a-Light-Fast-Self-Evolving-WAM|the methodology document]].

> [!info] One-Line Pitch
> **Fast-WAM gets 97.6% on standard LIBERO — but what happens when the world changes?** We add self-evolution to extend a strong WAM's competence to unseen scenarios (perturbed physics, novel compositions, detail-oriented tasks) where all static models fail.

---

## Base Model

> [!info] Why Fast-WAM?
> ==Strongest open-source WAM== (97.6% [[2306.03310|LIBERO]], 91.8% [[2506.18088|RoboTwin]]). Published code ([GitHub](https://github.com/yuantianyuan01/FastWAM)) + checkpoints ([HuggingFace](https://huggingface.co/yuanty/fastwam)). MoT architecture: ActionDiT (~640M) + Video DiT (~5B, [Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)). ==Flow-matching action head==. World model: Video DiT predicts future frames in pixel/video space. Video DiT kept during self-evolving loop (810ms, A100) for prediction error + dreams; stripped for deployment (190ms, 20-30 Hz). Trade-off: prediction error requires A100 (5B Video DiT); OOD performance untested. See [[02_How-to-Build-a-Light-Fast-Self-Evolving-WAM#Base Models|methodology]].

> [!info] Why VLA-JEPA?
> ==Strongest open-source JEPA-based WAM== (97.2% [[2306.03310|LIBERO]], ==79.5% LIBERO-Plus OOD==, 65.2% [[2405.05941|SimplerEnv]]). Published code ([GitHub](https://github.com/ginwind/VLA-JEPA)) + checkpoints ([HuggingFace](https://huggingface.co/ginwind/VLA-JEPA)), Apache 2.0. Architecture: V-JEPA2 (ViT-L) world model + Qwen3-VL-2B VLM backbone. ==Flow-matching action head== (same as Fast-WAM — all exploration methods transfer). World model: V-JEPA2 has latent prediction capability (`vj_predictor` module) but is ==dormant at inference by default== — needs explicit activation for prediction error in the self-evolving loop (no 5B branch, no A100). LIBERO-Plus eval built into repo. Trade-off: slightly lower in-distribution (97.2% vs 97.6%); latent-level dreams only (no pixel video). See [[02_How-to-Build-a-Light-Fast-Self-Evolving-WAM#Base Models|methodology]].

We evaluate on ==two WAMs== to prove framework-agnostic applicability. Both use ==flow matching for actions== — all exploration methods (πRL, SOE, PLD, RoboMD) work identically on both.

**Key differences only** (everything else is the same):

| | Fast-WAM ([[2603.16666\|paper]]) | VLA-JEPA ([[2602.10098\|paper]]) |
|---|---|---|
| **World model** | Video DiT (~5B) — ==pixel/video== prediction | V-JEPA2 (ViT-L) — ==latent== prediction |
| **VLM backbone** | T5 text encoder | Qwen3-VL-2B |
| **LIBERO / OOD** | ==97.6%== / untested | 97.2% / ==79.5% LIBERO-Plus OOD== |
| **Prediction error** | ==Expensive== (5B Video DiT, A100) | ==Free== (V-JEPA2 is integrated) |
| **LoRA target** | ActionDiT attention layers (~640M) | VLA action head + Qwen3-VL-2B |
| **Dream space** | Pixel-level future frames | Latent-level future states |

### Fast-WAM: What to Modify

- **Code**: [GitHub](https://github.com/yuantianyuan01/FastWAM) | **Checkpoints**: [HuggingFace](https://huggingface.co/yuanty/fastwam)
- **LoRA target**: ActionDiT attention layers (==non-mixed-attention only== — inspect `mot.py` for mixed attention layer locations)
- **Video DiT**: Keep at inference (full MoT, 810ms on A100) for prediction error + dreams. ==Freeze== — never fine-tuned.
- **SOE adaptation**: Swap DDPM decoder for ActionDiT's FM decoder in SOE's `dp_ext.py`
- **πRL Flow-SDE**: Modify ODE solver in ActionDiT's scheduler to inject stochastic noise
- **Compute**: A100 for sim rollouts (full MoT); 2-4 GPUs for LoRA fine-tuning

### VLA-JEPA: What to Modify

- **Code**: [GitHub](https://github.com/ginwind/VLA-JEPA) | **Checkpoints**: [HuggingFace](https://huggingface.co/ginwind/VLA-JEPA)
- **LoRA target**: Qwen3-VL-2B action head layers (architecture details in `starVLA/` codebase)
- **V-JEPA2**: Has latent prediction capability (`vj_encoder` + `vj_predictor` modules exist) but is ==dormant at inference by default== — `predict_action()` bypasses V-JEPA2 entirely. For the self-evolving loop, ==explicitly call `vj_predictor()` during DETECT step== to compute prediction error. The modules are there — just need activation.
- **SOE adaptation**: Same approach — swap DDPM decoder for VLA-JEPA's FM action head
- **πRL Flow-SDE**: Same approach — modify FM action head's ODE solver for stochastic noise
- **Compute**: ==Lighter than Fast-WAM== — no 5B Video DiT branch. Standard GPU sufficient for sim rollouts.

---

## Phase 0: Reproduce Baseline

> [!tip] Goal
> Confirm Fast-WAM's published results using released checkpoints. Validation only — no training.

### Steps

1. Download Fast-WAM checkpoints from [HuggingFace](https://huggingface.co/yuanty/fastwam)
2. Set up [[2306.03310|LIBERO]] evaluation environment ([GitHub](https://github.com/Lifelong-Robot-Learning/LIBERO)) with [MuJoCo](https://mujoco.org) ([GitHub](https://github.com/google-deepmind/mujoco))
3. Run Fast-WAM on standard LIBERO (4 suites: libero_10, libero_goal, libero_object, libero_spatial)
4. Run Fast-WAM on standard [[2506.18088|RoboTwin]] ([GitHub](https://github.com/TianxingChen/RoboTwin))
5. Confirm results match published numbers

### Success Criteria

- [ ] Fast-WAM: LIBERO ~97.6%, RoboTwin ~91.8% (matching [[2603.16666|Fast-WAM]] paper)
- [ ] VLA-JEPA: LIBERO ~97.2%, LIBERO-Plus ~79.5%, SimplerEnv ~65.2% (matching [[2602.10098|VLA-JEPA]] paper)

---

## Phase 1: Establish Failure Cases

> [!tip] Goal
> Demonstrate WHERE Fast-WAM fails on out-of-distribution scenarios. ==This is the first publishable contribution== — nobody has tested Fast-WAM on these benchmarks.

### Steps

1. Run Fast-WAM on [[2510.03827|LIBERO-PRO]] (4 perturbation dims: object attributes, positions, language, environment)
2. Run Fast-WAM on [[2602.06556|LIBERO-X]] (5 hierarchical difficulty levels, 600 tasks)
3. Run Fast-WAM on [[2603.22078|LIBERO-Plus]] (7 visual perturbation dimensions, 21 sub-dims)
4. Run Fast-WAM on [[2603.28301|LIBERO-Para]] (paraphrased instruction robustness)
5. Run Fast-WAM on [[2601.11421|GM-100]] (100 detail-oriented tasks)
6. Run Fast-WAM on [[2112.03227|CALVIN]] (5-step instruction chains) ([GitHub](https://github.com/mees/calvin))
7. Record all results — these are the ==baselines that self-evolution must improve==

### Datasets & Benchmarks

| Resource | Role | Source | Expected Fast-WAM Performance |
|----------|------|--------|------|
| [[2510.03827\|LIBERO-PRO]] | Spatial/object perturbation eval | LIBERO-PRO benchmark | VLAs: >90% → ==near 0%==. Fast-WAM: untested |
| [[2602.06556\|LIBERO-X]] | Hierarchical robustness eval (5 levels) | LIBERO-X benchmark (600 tasks) | VLAs: ==39.4%== at easiest level. Fast-WAM: untested |
| [[2603.22078\|LIBERO-Plus]] | Visual perturbation eval | From WAM vs VLA Robustness paper | π0.5: 85.7% → 58.6% on perturbed RoboTwin |
| [[2603.28301\|LIBERO-Para]] | Language paraphrase eval | LIBERO-Para benchmark | VLAs drop ==22.8-51.9pp==. Fast-WAM: untested |
| [[2601.11421\|GM-100]] | Detail-oriented task eval | GM-100 benchmark | Best VLA ([[2410.24164\|π0.5]]): 24.9% |
| [[2112.03227\|CALVIN]] | Long-horizon multi-step | [GitHub](https://github.com/mees/calvin) | Best: 4.33 by [[2412.14803\|VPP]] |

### Key Papers (Why This Phase Matters)

These papers prove that ALL static models (VLAs and WAMs) fail under distribution shift — establishing the problem that self-evolution must solve.

| Paper | What It Shows |
|-------|---------------|
| [[2510.03827\|LIBERO-PRO]] | VLAs collapse from >90% to near 0% under minor perturbations — models memorize, don't generalize |
| [[2602.06556\|LIBERO-X]] | Only 39.4% at easiest level; near-zero for 3+ step tasks — structural limitation |
| [[2603.28301\|LIBERO-Para]] | 22.8-51.9pp drops from paraphrased instructions — language overfitting |
| [[2603.22078\|WAM vs VLA Robustness]] | π0.5: 85.7% → 58.6% under perturbation; WAMs more robust but 4.8x slower |
| [[2601.11421\|GM-100]] | Detail-oriented manipulation remains unsolved (best: 24.9%) |
| [[2505.03500\|TLI]] | Static models spatially overfit: 9% on novel compositions |
| [[2602.15922\|DreamZero]] | Even 14B WAMs get only 39.5% on unseen tasks |

### Success Criteria

- [ ] Fast-WAM tested on all 5 OOD benchmarks (all untested — first results)
- [ ] VLA-JEPA tested on remaining OOD benchmarks (LIBERO-Plus already 79.5% — test LIBERO-PRO, LIBERO-X, LIBERO-Para, GM-100)
- [ ] Results documented — drops from baseline quantified for BOTH models
- [ ] The performance gaps are clear enough to motivate self-evolution

---

## Phase 2: The Self-Evolving Loop

> [!tip] Goal
> Both Fast-WAM and VLA-JEPA ==discover their own weaknesses at three levels== — environment (which conditions are hard), action (which behaviors fail), and language (which instructions confuse it) — using active probing + passive signals. No human-designed perturbation types. The loop is ==identical for both models== except the DETECT and DREAM steps (see comparison table below).

### Three Levels of Self-Discovery

| Level | What It Discovers | Passive or Active? | Method |
|-------|------------------|-------------------|--------|
| **Environment** | Which ==sim conditions== the model can't handle | ==Active==: RL adversary searches for failure-inducing conditions | [[2412.02818|RoboMD]] (RL adversary, policy-agnostic) |
| **Environment** | Which conditions the world model ==doesn't understand== | Passive: prediction error flags surprise | Fast-WAM: Video DiT prediction error; VLA-JEPA: ==V-JEPA2 latent prediction error (free)== (inspired by [[2602.20057\|AdaWorldPolicy]]) |
| **Action** | Which ==action variations== cause failure | ==Active==: perturb conditioning via VIB (compact latent) → find behavioral boundaries | [[2509.19292\|SOE]] adapted for FM — swap DDPM decoder for ActionDiT, keep VIB MLPs |
| **Action** | Where the model is ==uncertain== | Passive: stochastic sampling measures spread | [[2510.25889\|πRL]] Flow-SDE |
| **Behavioral** | Where the model ==actually fails== | ==Active==: deploy and observe | [[2511.00091\|PLD]] probing |

> [!tip] Key Insight: World Model Enables True Self-Discovery
> Both models can ==imagine what SHOULD happen== and compare with what ACTUALLY happens. Fast-WAM uses Video DiT (pixel-level, A100); VLA-JEPA uses V-JEPA2 (==latent-level, free==). High prediction error = "I don't understand this physics." We don't design perturbation types — we randomize broadly (like [[2603.16861|MolmoBot]]'s 232K environments), and ==the world model's own surprise discovers which conditions matter.==

### The Method: DIVERSIFY → DETECT → EXPLORE → PROBE → LEARN → DISTILL → MEASURE

```
1. DIVERSIFY: Deploy WAM in broadly randomized sim environments
   Fast-WAM: full MoT (ActionDiT + Video DiT) on A100
   VLA-JEPA: full model (standard GPU — no 5B branch)
   + Language augmentation: LLM generates 3-5 paraphrases per task
    ↓
2. IMAGINE + DETECT: World model predicts future states →
   compare with actual sim states →
   Fast-WAM: Video DiT prediction error (pixel-level, A100)
   VLA-JEPA: V-JEPA2 prediction error (latent-level, free)
   high error = "I don't understand this physics"
    ↓
3. EXPLORE (three active probing levels):
   a. BEHAVIORAL: PLD deploys model → observes actual failures
   b. ENVIRONMENTAL: RoboMD RL adversary searches for
      failure-inducing sim conditions (policy-agnostic)
   c. LATENT: SOE (adapted for FM — swap decoder, keep VIB MLPs)
      perturbs conditioning → finds action-level weaknesses
   + πRL Flow-SDE provides passive uncertainty signal
    ↓
4. LEARN: PLD trains recovery specialists
   (πRL provides flow-matching-compatible RL mechanism)
    ↓
5. DISTILL: Recovery data → LoRA fine-tune action model
   Fast-WAM: LoRA on ActionDiT (non-mixed-attention layers only)
   VLA-JEPA: LoRA on Qwen3-VL-2B action head
   + Replay buffer (2% old data) prevents forgetting
    ↓
6. DREAM: World model generates additional future-state rollouts
   Fast-WAM: Video DiT → pixel-level dreams
   VLA-JEPA: V-JEPA2 → latent-level dreams
    ↓
7. MEASURE: Benchmark evaluation (LIBERO-PRO, LIBERO-X, etc.)
   → Repeat from step 1
```

### How the Core Methods Integrate

| Step | Level | Method | Paper | What It Does |
|------|-------|--------|-------|-------------|
| DIVERSIFY | Environment | Broad procedural randomization + language augmentation | [[2603.16861\|MolmoBot]], [[2506.12851\|KungfuBot]] | Diverse sim conditions + paraphrased instructions. Model encounters unknown physics and language naturally |
| IMAGINE + DETECT | ==Environment== | ==Video DiT prediction error (latent space)== | Inspired by [[2602.20057\|AdaWorldPolicy]] | Video DiT predicts future → compare in latent space → high error = "I don't understand this." ==Our novel use of Fast-WAM's world model for self-discovery.== |
| EXPLORE (behavioral) | ==Failure states== | Probe-Learn-Distill | [[2511.00091\|PLD]] | Deploys model → observes WHERE it fails → active behavioral probing. |
| EXPLORE (environmental) | ==Environment== | RL adversary | [[2412.02818|RoboMD]] | RL adversary actively searches for failure-inducing sim conditions. ==Policy-agnostic== — works with any model. |
| EXPLORE (latent) | ==Action== | ==SOE adapted for flow matching== | [[2509.19292\|SOE]] | SOE's VIB is architecture-agnostic (just MLPs). Swap DDPM decoder for ActionDiT's FM decoder. Exploration = noise injection into conditioning — works regardless of decoder type. Straightforward adaptation, not major re-engineering. |
| Uncertainty signal | Action | Flow-SDE stochastic sampling | [[2510.25889\|πRL]], [[2505.05470\|Flow-GRPO]] | ODE → SDE conversion → passive uncertainty measurement. High variance = "model is unsure." |
| LEARN | Both | RL fine-tuning | [[2510.25889\|πRL]] + [[2511.00091\|PLD]] | πRL provides flow-matching-compatible RL. PLD trains recovery specialists. |
| DREAM | Environment | Video DiT imagination | [[2603.16666\|Fast-WAM]] Video DiT | Future-state rollouts from imagination — extra training data. |
| Data collection | Both | Self-play rollouts | [[2603.09030\|PlayWorld]] | Autonomous diverse rollouts including failures. |

### How the Loop Maps to Each Model

The self-evolving loop is ==identical for both models== except the DETECT step:

| Step | Fast-WAM | VLA-JEPA | Same? |
|------|----------|----------|-------|
| DIVERSIFY | Broad MuJoCo randomization + LLM paraphrases | Same | ==Yes== |
| DETECT | Video DiT prediction error (5B, A100, pixel-level) | ==V-JEPA2 prediction error (ViT-L, cheap, latent-level)== | Different mechanism, same purpose |
| EXPLORE (env) | RoboMD adversary (policy-agnostic) | Same | ==Yes== |
| EXPLORE (action) | SOE adapted for FM (flow matching action head) | SOE adapted for FM (==same flow matching action head==) | ==Yes== |
| EXPLORE (uncertainty) | πRL Flow-SDE (flow matching ODE → SDE) | πRL Flow-SDE (==same flow matching ODE → SDE==) | ==Yes== |
| PROBE + LEARN | PLD + πRL RL training | Same | ==Yes== |
| DISTILL | LoRA on ActionDiT (640M) | LoRA on Qwen3-VL-2B action head | Different target, same technique |
| DREAM | Video DiT generates pixel futures | V-JEPA2 generates ==latent== futures | Different representation, same purpose |
| MEASURE | OOD benchmarks | Same | ==Yes== |

> [!tip] Why This Is Truly Self-Evolving
> - **Environment discovery**: Broad randomization + Video DiT prediction error → model discovers which conditions are hard (not human-designed)
> - **Action discovery**: πRL's Flow-SDE → stochastic action sampling reveals uncertainty; PLD probing confirms failures (not human-designed)
> - **Language discovery**: Instruction augmentation + success rate comparison across paraphrases → reveals language fragility
> - **Benchmarks** ([[2510.03827|LIBERO-PRO]], [[2602.06556|LIBERO-X]], etc.) ==measure== whether self-discovered improvements transfer — they don't ==design== the curriculum

### Concrete Steps to Implement

**Step 1: Set Up LoRA on the Action Model**

Apply LoRA (rank=32) to the action model's attention layers. For ==Fast-WAM==: apply only on layers that do NOT participate in mixed attention with Video DiT — these shared layers were calibrated during joint training, and changing only ActionDiT's side would break alignment. Video DiT remains frozen throughout. For ==VLA-JEPA==: apply LoRA to the Qwen3-VL-2B action head layers — no mixed attention concern since V-JEPA2 and the action head are more loosely coupled. Estimated trainable parameters: ~7.9M for Fast-WAM, similar scale for VLA-JEPA ([[2603.11653|VLA RL CL]]).

**Step 2: Add Flow-SDE Stochastic Action Sampling**

Following [[2510.25889|πRL]]'s Flow-SDE mechanism: both Fast-WAM's ActionDiT and VLA-JEPA's action head normally generate actions via a ==deterministic ODE== (one noise seed → one action). Flow-SDE converts this to a ==Stochastic Differential Equation== by injecting small noise at each denoising step, following [[2505.05470|Flow-GRPO]]'s ODE-to-SDE conversion. This preserves the original model's probability distribution while enabling stochastic exploration. ==Note==: πRL's codebase implements Flow-SDE ==within the RL training loop==, not as a standalone sampling module. Extracting the SDE conversion logic for standalone uncertainty measurement requires engineering work — the ODE-to-SDE math ([[2505.05470|Flow-GRPO]]) is well-defined, but the implementation needs to be adapted from πRL's RL-integrated code. At each observation, run the action model multiple times (e.g., 5) from different noise seeds → compute variance across samples. High variance = the model is uncertain → potential weakness.

**Step 3: Adapt SOE for Flow Matching**

[[2509.19292|SOE]] learns a ==compact 4-dimensional latent representation== of task-relevant information using a Variational Information Bottleneck (VIB). The VIB consists of a small encoder (MLP that compresses observation features to 4 dimensions) and a small decoder (MLP that decompresses back). These are ==architecture-agnostic== — they work with any policy. The exploration mechanism adds noise to the compressed representation, which produces diverse but valid action variations when decoded. To adapt for either model: keep the VIB MLPs and noise injection unchanged, but replace the original DDPM-based action decoder with the model's flow matching decoder. ==Note==: SOE's codebase calls DDPM-specific methods (`compute_weighted_loss`, `predict_action`, `compute_loss`) on the action decoder — not just the decoder class itself. Adapting for FM requires replacing ==both the decoder AND these method calls== with flow matching equivalents (velocity prediction loss, FM sampling). The VIB and exploration sit between the observation encoder and the action decoder and are unaffected — only the decoder interface changes.

**Step 4: Set Up Broad Procedural Randomization**

Randomize ALL simulation parameters broadly before each episode using [[2009.12293|robosuite]]'s [MuJoCo](https://mujoco.org) API: object mass (0.5x to 3.0x of default, [[2506.12851|KungfuBot]]-style), surface friction (0.2 to 2.0), joint damping (0.5x to 2.0x), object spawn positions (±0.2 units from default), camera angles, lighting, and backgrounds ([[2506.18088|RoboTwin 2.0]]'s 5-dimension approach). Additionally, an LLM generates 3-5 paraphrased versions of each task instruction for language diversity. This is ==NOT targeted per benchmark== — broad diversity lets the prediction error and active probing discover which conditions actually matter.

**Step 5: Set Up RoboMD RL Adversary**

Following [[2412.02818|RoboMD]]: train a separate RL agent (the "adversary") whose goal is to find ==environment configurations that make the target WAM fail== (run separately for Fast-WAM and VLA-JEPA). The adversary operates in a learned semantic embedding space (built from vision-language features), not raw simulation parameters. It treats Fast-WAM as a ==black box== — only observing inputs and outputs, no access to model internals. The adversary's reward is Fast-WAM's failure rate: the more Fast-WAM fails, the higher the adversary's reward. This produces a ranked list of the hardest environment configurations, which are then used as training scenarios in the self-evolving loop.

**Step 6: Run the Self-Evolving Loop (5-10 rounds)**

Each round consists of seven sub-steps:

> **a. DIVERSIFY**: Deploy WAM in broadly randomized sim environments with paraphrased instructions. Fast-WAM: full MoT on A100 (~810ms/step). VLA-JEPA: standard GPU (no 5B branch). Collect rollouts including both successes and failures.
>
> **b. DETECT**: During each rollout, the world model predicts the next observation. Fast-WAM: Video DiT predicts in pixel/VAE latent space (A100). VLA-JEPA: V-JEPA2 predicts in ==JEPA latent space (free)==. Compare predicted vs actual. High prediction error = the model was surprised. Flag episodes where error exceeds a rolling threshold.
>
> **c. EXPLORE**: Three parallel probing mechanisms run during or between rollouts:
> - ==Environmental probing==: RoboMD adversary generates the hardest environment configurations for the next round
> - ==Action probing==: SOE (adapted for FM) perturbs the VIB latent representation → generates diverse action variations → identifies which variations cause failure (maps behavioral boundaries)
> - ==Uncertainty measurement==: πRL Flow-SDE generates multiple stochastic action samples per observation → high variance flags action-level uncertainty
>
> **d. PROBE + LEARN**: [[2511.00091|PLD]] identifies the specific states where the model failed during rollouts. [[2510.25889|πRL]] trains lightweight residual RL specialists on those failure states — each specialist learns a small correction (additive residual) that recovers from the failure.
>
> **e. DISTILL**: Collect the successful recovery trajectories from the specialists. LoRA fine-tune the action model (Fast-WAM: ActionDiT non-mixed layers; VLA-JEPA: Qwen3-VL-2B action head) on recovery data plus a 2% replay buffer ([[2603.03818|VLA CL]]). If LoRA capacity saturates, merge weights into base and restart with fresh adapters.
>
> **f. DREAM**: World model generates additional future-state rollouts from diverse initial conditions. Fast-WAM: Video DiT → pixel-level dreams. VLA-JEPA: V-JEPA2 → latent-level dreams. Filter for quality: keep only those where action predictions are consistent (low flow matching sample variance).
>
> **g. MEASURE**: Evaluate on held-out OOD benchmarks ([[2510.03827|LIBERO-PRO]], [[2602.06556|LIBERO-X]], [[2603.28301|LIBERO-Para]], [[2601.11421|GM-100]]). Record per-benchmark improvement. If regression on standard [[2306.03310|LIBERO]] exceeds 2%, increase the replay buffer ratio. Plot improvement curves per benchmark per round.

**Step 7: Final Deployment**

After the final round: Fast-WAM strips Video DiT — ActionDiT deploys alone at 190ms (~20-30 Hz). VLA-JEPA deploys as-is (V-JEPA2 is lightweight, or can be stripped for speed). Self-evolved improvements are ==baked into LoRA-updated weights== for both. Run final benchmark suite and compare against Phase 1 baselines for ==both models==.

### Training Data

All training data is ==self-generated==. No human-designed perturbations needed.

| Source | What It Is | How Generated |
|--------|-----------|---------------|
| **Flow-SDE diverse rollouts** | Action variations from stochastic ODE sampling | [[2510.25889\|πRL]] Flow-SDE generates diverse action chunks per observation |
| **SOE exploration rollouts** | Action variations from VIB conditioning perturbation | [[2509.19292\|SOE]] adapted for FM perturbs VIB latent → diverse behaviors |
| **High-error scenarios** | Environments where world model is surprised | Fast-WAM: Video DiT prediction error; VLA-JEPA: V-JEPA2 latent prediction error |
| **PLD recovery data** | Recovery trajectories from failure states | [[2511.00091\|PLD]] + [[2510.25889\|πRL]] RL specialists generate these |
| **Autonomous rollouts** | Diverse self-play including failures | [[2603.09030\|PlayWorld]]-style deployment in sim |
| **Dream rollouts** | Future-state imagination | Fast-WAM: Video DiT (pixel); VLA-JEPA: V-JEPA2 (latent) |
| **Replay buffer** | 2% of original [[2306.03310\|LIBERO]] demonstrations | Prevents forgetting ([[2603.03818\|VLA CL]]) |

### Optional: Benchmark-Targeted Perturbations (Acceleration)

For faster improvement on specific benchmarks, you CAN additionally generate perturbations that match what each benchmark tests. This is ==optional acceleration==, not the primary mechanism.

| Perturbation Type | How to Generate | Targets |
|-------------------|----------------|---------|
| Object position/attribute | Modify spawn positions in [MuJoCo](https://mujoco.org) | [[2510.03827\|LIBERO-PRO]] |
| Spatial layout | Rearrange scene topology | [[2602.06556\|LIBERO-X]] |
| Language paraphrase | LLM generates equivalent instructions | [[2603.28301\|LIBERO-Para]] |
| Visual (camera, lighting, background) | Rendering parameter randomization | [[2603.22078\|LIBERO-Plus]] |
| Physics params | [[2506.12851\|KungfuBot]]-style MuJoCo randomization | General robustness |

> [!info] How perturbations are applied
> - **Object position, spatial layout, visual**: These are ==scene/rendering changes== — modify object spawn positions, rearrange layouts, change camera/lighting. Applied via robosuite's environment config or MuJoCo XML before episode start.
> - **Language paraphrase**: LLM generates semantically equivalent instructions — no sim modification needed.
> - **Physics params**: These modify ==physical properties of objects== (mass, friction, damping) via [[2009.12293|robosuite]]'s [MuJoCo](https://mujoco.org) API. Broad randomization ([[2506.12851|KungfuBot]]-style) + [[2412.02818|RoboMD]] adversary actively searches for failure-inducing physics regimes.


### Why NOT VLAW?

> [[2602.12063|VLAW]]'s "co-evolution" requires ==separate== world model and policy. Fast-WAM trains them ==jointly== via MoT. We use "self-evolving loop" instead: the model discovers its own weaknesses via Video DiT prediction error (inspired by [[2602.20057|AdaWorldPolicy]]) + Flow-SDE stochastic exploration ([[2510.25889|πRL]]) + failure probing ([[2511.00091|PLD]]).

### Key Papers — Supporting Evidence

| Paper | What It Validates |
|-------|-------------------|
| [[2505.05470\|Flow-GRPO]] | ODE-to-SDE conversion enables stochastic exploration in flow matching models |
| [[2505.22094\|ReinFlow]] | First online RL for flow matching robot control. Learnable noise injection for exploration |
| [[2603.11653\|VLA RL CL]] | LoRA + GRPO achieves <2% forgetting on [[2410.24164\|π0]] |
| [[2603.03818\|VLA CL]] | 2% replay buffer suffices for near-zero backward transfer |
| [[2603.04029\|Self-Adapting RL]] | World model prediction residuals detect OOD without human-specified change types |
| [[2510.09459\|FIPER]] | Runtime failure prediction via RND + action entropy, works with diffusion/flow matching |

### Known Risks and Mitigations

| Risk | Severity | Mitigation | Reference |
|------|----------|-----------|-----------|
| **Mixed attention drift**: LoRA changes ActionDiT but Video DiT is frozen — mixed attention alignment breaks | HIGH | LoRA on ==non-mixed-attention layers only==. Monitor cosine similarity of mixed attention outputs before/after LoRA | Verified from Fast-WAM's `mot.py` architecture |
| **LoRA rank-32 saturation**: Accumulated corrections across rounds may exceed rank-32 capacity | MEDIUM | Monitor LoRA singular values. If saturated, ==merge LoRA into base weights and restart fresh adapters== | [[2603.11653\|VLA RL CL]] supports merge-and-restart |
| **Dream validity after LoRA**: Video DiT generates dreams based on pre-LoRA ActionDiT dynamics | MEDIUM | LoRA changes <1.2% of params per round — drift is small. Add ==dream validity check==: compare dreams vs sim for same initial conditions | Architectural analysis |
| **Compute throughput**: Full MoT at 1.2Hz = ~170 episodes/day | MEDIUM | ==Two-speed strategy==: fast screening (ActionDiT only, ~5Hz) for broad exploration; full MoT only for prediction error computation on flagged scenarios | Compute estimate from architecture |
| **Language blind spot**: Prediction error catches physics/visual weaknesses but NOT language paraphrasing | HIGH | ==Mandatory language augmentation== in DIVERSIFY step. Detect language weakness via action divergence across paraphrases, not prediction error | [[2603.28301\|LIBERO-Para]] |
| **PLD uses SFT, not LoRA**: PLD's distillation step was validated with full SFT | MEDIUM | Use LoRA for efficiency (less forgetting). Benchmark LoRA vs SFT distillation in early rounds. If gap >20%, increase LoRA rank or use SFT for action head only | [[2511.00091\|PLD]] |
| **πRL Flow-SDE not standalone**: Codebase implements Flow-SDE within RL training loop, not as separate sampling module | MEDIUM | Extract ODE-to-SDE conversion logic based on [[2505.05470\|Flow-GRPO]] math. The theory is well-defined; implementation needs adaptation from πRL's RL-integrated code | [[2510.25889\|πRL]] |
| **SOE DDPM method coupling**: SOE calls DDPM-specific methods (compute_loss, predict_action), not just decoder class | MEDIUM | Replace both decoder AND method calls with FM equivalents (velocity prediction loss, FM sampling). VIB MLPs themselves are unaffected | [[2509.19292\|SOE]] |
| **VLA-JEPA V-JEPA2 dormant at inference**: `predict_action()` bypasses V-JEPA2 entirely — prediction modules exist but need explicit activation | LOW | Add `vj_predictor()` call during DETECT step in self-evolving loop. The modules (`vj_encoder`, `vj_predictor`) are in the model — just not called at inference by default | [[2602.10098\|VLA-JEPA]] |

### Success Criteria

- [ ] Positive improvement on OOD benchmarks for $\geq 3$ consecutive rounds (==both models==)
- [ ] $>10\%$ total gain on at least one OOD benchmark for ==each model==
- [ ] No significant regression on standard [[2306.03310\|LIBERO]] (<2% drop) for either model
- [ ] Improvement curve plotted per benchmark per round per model
- [ ] ==Cross-model comparison==: does the same methodology produce similar improvement patterns on Fast-WAM vs VLA-JEPA? (proves framework-agnostic claim)

---

## Summary: The Full Pipeline

```
Phase 0 → Reproduce Fast-WAM baseline (hours, A100)
    ↓
Phase 1 → Test on OOD benchmarks, establish failure gaps (days)
    ↓
Phase 2 → Self-Evolving Loop (iterative, on A100):
    ┌────────────────────────────────────────────────────┐
    │  DIVERSIFY: deploy in randomized sim environments  │
    │      ↓                                             │
    │  IMAGINE: Video DiT predicts future states         │
    │  DETECT: compare prediction vs reality →           │
    │          high error = "I don't understand this"    │
    │      ↓                                             │
    │  EXPLORE (3 levels):                               │
    │    env: RoboMD RL adversary (policy-agnostic)      │
    │    action: SOE VIB perturbation (adapted for FM)   │
    │    uncertainty: πRL Flow-SDE (passive signal)      │
    │      ↓                                             │
    │  PROBE: PLD confirms failures                      │
    │  LEARN: πRL trains recovery specialists            │
    │      ↓                                             │
    │  DISTILL: recovery data → LoRA fine-tune ActionDiT │
    │  DREAM: Video DiT generates extra training data    │
    │      ↓                                             │
    │  MEASURE: benchmark evaluation                     │
    │      ↓                                             │
    │  Repeat — world model discovers new weaknesses     │
    └────────────────────────────────────────────────────┘
    ↓
Final benchmarks: LIBERO-PRO, LIBERO-X, LIBERO-Para, GM-100
```

---

## FAQ

> [!question] What are the core methods?
> **Fast-WAM (full MoT) + 6 methods = Self-Evolving Fast-WAM:**
> - [[2510.25889|πRL]]: ==Flow-SDE stochastic sampling + RL training== for flow matching. Passive uncertainty signal + RL mechanism for PLD specialists.
> - [[2509.19292|SOE]] adapted for FM: ==Active action-level probing==. VIB = MLPs + conditioning noise injection. Swap DDPM decoder for ActionDiT.
> - Video DiT prediction error (inspired by [[2602.20057|AdaWorldPolicy]]): ==Environment-level passive discovery==. Our novel use of Fast-WAM's world model.
> - [[2412.02818|RoboMD]]: ==Environment-level active probing==. RL adversary, policy-agnostic.
> - [[2511.00091|PLD]]: ==Behavioral probing + failure recovery== (probe → learn → distill).
> - [[2603.09030|PlayWorld]]: ==Autonomous data collection==.

> [!question] What is the training data?
> ==Self-generated sim rollouts.== The model acts in [MuJoCo](https://mujoco.org)/[[2306.03310|LIBERO]] with perturbations, and its own trajectories (successes + failures + adapted rollouts) become the training data. A 2% replay buffer of original LIBERO demonstrations prevents forgetting. Optional: [[2603.16861|MolmoBot]]-Data (1.8M trajectories) for diversity. No new human demonstrations needed — that's what makes it "self-evolving."

> [!question] Benchmarks are NOT training data, right?
> Correct. Benchmarks ([[2510.03827|LIBERO-PRO]], [[2602.06556|LIBERO-X]], [[2603.28301|LIBERO-Para]], [[2601.11421|GM-100]]) are ==held-out evaluation only==. Never trained on. Used before the self-evolving loop (Phase 1: measure the gap) and after (measure improvement). The training data is self-generated sim rollouts from perturbed scenarios that ==match the same perturbation types== as the benchmarks.

> [!question] How does the model find its own weaknesses?
> ==Active + passive signals at three levels, no human-designed perturbations:==
> 1. **Environment (active)**: [[2412.02818|RoboMD]] RL adversary ==actively searches== for failure-inducing sim conditions (policy-agnostic).
> 2. **Environment (passive)**: Video DiT prediction error flags ==surprise== ("I don't understand this physics").
> 3. **Action (active)**: [[2509.19292|SOE]] adapted for FM — VIB is just MLPs, exploration is conditioning noise injection. Swap DDPM decoder for ActionDiT. Finds ==behavioral boundaries==.
> 4. **Action (passive)**: [[2510.25889|πRL]] Flow-SDE measures ==action uncertainty== (high sample variance).
> 5. **Language**: LLM paraphrases instructions → compares action sequences → ==language fragility==.
> 6. **Behavioral**: [[2511.00091|PLD]] ==deploys and observes== actual failures → trains recovery.
>
> Benchmarks ==measure== whether improvements transfer — they don't design the curriculum.

> [!question] Can Fast-WAM imagine future states?
> ==Yes, when Video DiT is kept at inference.== Fast-WAM has two modes: stripped (190ms, no imagination) and full MoT (810ms, with imagination). We use the full MoT mode — slower but the Video DiT enables prediction error, dream generation, and world model supervision. The 810ms (~1.2 Hz) is fine for sim data collection on A100.

> [!question] What does "self-evolving" mean? (Not "co-evolution")
> "Co-evolution" was [[2602.12063|VLAW]]'s term for alternating between training a separate world model and policy. Fast-WAM trains them jointly via MoT — there's nothing to alternate. We use **"self-evolving loop"** instead: the model generates its own training data through targeted failure discovery, adapts on-the-fly, and distills improvements back into itself. The model evolves itself, not two models co-evolving.

> [!question] Is this post-training research?
> Yes. Fast-WAM is already pre-trained (by its authors, on 8-64 GPUs). We use their released checkpoint and apply ==post-training== methods (LoRA fine-tuning, online adaptation, targeted data generation) to extend its capabilities to OOD scenarios. This is the same framing as [[2511.00091|PLD]] ("Self-Improving VLAs"), [[2602.20057|AdaWorldPolicy]] ("Online Adaptive Learning"), and [[2603.11653|VLA RL CL]] ("Continual RL for VLAs") — all post-training on pre-trained models.

---

*Companion to [[02_How-to-Build-a-Light-Fast-Self-Evolving-WAM|the methodology document]]. See also: [[00_How-to-Build-Self-Evolving-WAM|original blueprint]] | [[01_Critique-Self-Evolving-WAM|domain transfer critique]] | [[01_Critique-Methodology-Self-Evolving-WAM|methodology critique]]*
