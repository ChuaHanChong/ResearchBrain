---
title: Uncertainty-Gated System-2 Escalation for VLA Policies
aliases:
  - Gated System-2
  - Design Plan
tags:
  - vla
  - failure-detection
  - system2
  - adaptive-compute
  - design-plan
---

# Uncertainty-Gated System-2 Escalation for VLA Policies

> [!abstract] In one paragraph
> A System-1 / System-2 hybrid already exists and works: pi0.5 proposes an action chunk, a frontier model reviews it, and either a pi0.5 prefix or a model-authored end-effector correction executes. The reviewer is called at **every** decision point and **blocks the robot** while it thinks. This plan inserts a cheap gate so the reviewer is called only when the policy's own signal says it is needed. Nothing else in the architecture changes.

> [!note] Provenance
> Every number below was read from the PDF in `papers/`, not from a summary. Claims that did not survive that check are marked **[corrected]** with the true value. Harness facts marked **[repo]** were read from the reference implementation in `repo/GPTasPolicy_reference`, not from the write-up. Verified 2026-09-19.

## 1. Thesis

**A blocking call to a slow model costs wall-clock in proportion to how often it is made, not how good it is.** The field assumes System-2 review must be synchronous and per-decision. The bet: **success rate within 15 points of the 48% ungated reference on RoboDojo, the frontier model invoked on at most 50% of decision points, cumulative stall time at least halved.**

- **First principle.** Review cost = `calls x latency`. The existing system fixes `calls = 1` per decision. Latency is not ours to control. So the saving must come from the call count.
- **Assumption challenged.** The reference system uses the frontier model as its own gate: it reviews every candidate to decide whether that candidate needed reviewing. Circular, and about two thirds of those calls end in an unmodified pi0.5 prefix.
- **Falsified if** detector recall on corrected decisions is too low to preserve success rate at any escalation budget below 100%.

> [!important] The target is 33%, not 14.4%
> The reference report's 14.4% is in **control steps**. A correction runs 1-5 steps, an accepted prefix runs 1-15, so the two branches are not comparable in that unit. In **decision points**, which is what a gate acts on, their published per-case results give 3,776 decisions, 6,174 corrected steps and 36,576 accepted steps. That constrains corrections to **32.7-35.4% of decision points**.
>
> So an oracle gate still calls the model on a third of decisions. Any target below that floor is unreachable. The prize survives because the cost removed is **stall**, not calls: ~75.5 blocking calls per episode against 40 s of physical motion.

## 2. What already exists

### 2.1 The reference system

Su, Zheng, Yan, Yi, Zhang, Wang, *GPT 6 Astra as an Embodied Policy*, 2026. Website anonymised; the repository names the authors. Tsinghua plus Galbot / PKU. Code cloned to `repo/GPTasPolicy_reference`.

| | |
|---|---|
| Fast policy | pi0.5, RoboDojo task-finetuned, independent OpenPI/JAX service |
| Candidate | 50 x 14 joint-space chunk, plus its bimanual forward-kinematics trajectory |
| Reviewer | gpt-6-astra at xhigh, persistent Codex thread with file, image, compute and note tools |
| Reviewer decision | **[repo]** three modes, not two: `student` (execute a 1-15 step prefix), `edit` (a 1-5 step delta on the student's own target), `eef` (a 1-5 step absolute pose target). Remaining suffix discarded. |
| Execution | damped least-squares IK recomputed after every control ACK. **[repo]** two clamp layers: target within 0.05 m / 0.35 rad of the current measured pose, and per increment 2 cm / 0.1 rad with each joint under 0.05 rad. No planner, no teleport. |
| Protocol | `robodojo_start`, `pi05_infer`, `robodojo_execute`. **[repo]** the harness calls them "the three blocking rollout tools". |
| Checkpoint | **[repo]** `pi05_base_aloha_full_sim_arx-x5_seed_0`, normalizer `arx_x5_sim` |
| What `pi05_infer` returns | **[repo]** all 50 target steps plus both-arm forward-kinematics poses. **No policy internals.** |
| Control rate | **[repo]** 25 Hz (0.04 s) native control observations; the reviewer observes at chunk boundaries, not physics substeps |
| Rollback | **[repo]** none. "There is no rollback... Do not rewind." |
| RoboDojo | hybrid **48%** / Score 62.60; direct 26% / 37.81; pi0.5 15.67% / 24.43 |
| RoboLab | direct 49/50; hybrid 46/50; pi0.5 18/50 |
| Decisions | 3,776 over 50 episodes, ~75.5 per episode, mean 11.32 control steps each |
| Corrections | 6,174 of 42,750 steps (14.4%); **32.7-35.4% of decisions** |
| Tokens | 624.8M hybrid against 1.13B direct, 50 episodes |

**Two admissions this plan builds on.** Their Section 7: the comparison varies action priors, action-generation interfaces and segment lengths at once, so its own contributions are entangled. Their conclusion: latency remains unresolved for real-time deployment, and Table 3 excludes model-response time from reported duration. **Stall has never been measured in this architecture.**

> [!important] The reference system already has a gate, and it explicitly bars uncertainty **[repo]**
> `gate_assessment.py` holds a `GATE_INSTRUCTION` requiring the reviewer to produce a structured outcome-and-intent assessment at every chunk boundary, and it states the takeover rule outright:
>
> *"An edit/eef takeover requires execution_status=failed or intent_status=misaligned. Uncertainty alone or an aesthetically imperfect pose is not a takeover reason."*
>
> **This is not a competing design, it is a different layer, and the distinction sharpens the contribution.** Their rule gates *whether to override* - and it can only run after the reviewer has already been called and paid for. The gate proposed here runs one level earlier and decides *whether to call at all*. The two compose: uncertainty gates the invocation, their assessment still gates the takeover. Say this explicitly in any write-up, because a reader who knows the harness will otherwise read the proposal as contradicting a rule its own authors wrote down.

**No latency instrumentation exists in the harness [repo].** A search for timing across `hybrid_rollout/` returns only video duration in the report renderer. Nothing records model response time or robot idle time. Section 6 step 2 is therefore new instrumentation, not a re-analysis.

**Benchmark facts.** RoboDojo (2607.04434): 42 simulation and 18 real-world tasks, bimanual ARX X5 with arm bases 0.6 m apart, five capability dimensions (generalization, memory, precision, long-horizon, open-vocabulary), public leaderboard with hidden verification layouts. **[corrected]** 25 Hz is the *demonstration recording* rate; the paper states no control frequency. The Score metric has **no published formula** - it is described in prose, and real-world Score is the mean of three double-blind human evaluators. RoboLab (2604.09860): 120 tasks on three competency axes at three difficulty levels, 7-DoF Franka Panda with a Robotiq 2F-85 gripper in a DROID-style setup, Isaac Lab.

### 2.2 Detectors

| | **accel** 2607.27933 | **ActProbe** 2606.08508 |
|---|---|---|
| Reads | denoising velocities of the chunk being generated | two most recent chunks, **plus normalised timestep and a frozen task embedding** |
| Signal | accumulated velocity change / mean velocity magnitude over the prefix | squared error on chunk overlap, plus chunk norm |
| Model | none, a derivation | ~24K parameters **total** (LSTM ~4.7K; the `Linear(1024,16)` language bottleneck is ~16.4K) |
| Supervision | **no failure labels**, but fits on 50 successes | trajectory outcomes, broadcast to every step |
| Threshold | CUSUM height on 50 held-out successes | split-conformal cutoff on the running maximum, default alpha 0.15 |
| Cost | free at inference | ~3 ms (**hardware not stated in the paper**) |
| Access | **white-box**, the flow head's internals | **black-box**, only the returned array |
| Headline | 0.66 true-positive rate at 0.1 false alarms, against SAFE 0.68, STAC 0.60, FIPER 0.55; spread 0.01-0.03 against SAFE's 0.05-0.09 | 75.8% early ROC-AUC against SAFE-MLP's 71.2, +9.0 unseen, +12.7% hypervolume |
| Limits | flow-matching heads only, **no real robot at all**, silent when the policy is confidently wrong | needs failed rollouts; real-robot detection was **replayed offline**, not run online |

> [!warning] Three corrections that change the design
>
> **1. accel is not unsupervised. [corrected]** It uses no *failure* labels, but fits its reference mean, standard deviation and CUSUM height on **M=50 held-out successful rollouts**, plus a run-pooled action standardisation. The paper never reconciles this with its own "requires no extra training or labelled data". The honest framing is *success-only calibration*, which is still cheaper than ActProbe but is not free of data.
>
> **2. The half-path lead-time argument does not survive. [corrected]** The numbers are exact - Spearman 0.541 to 0.792 at prefix 5 of 10 on pi0.5+LIBERO, because terminal Euler steps carry discretisation noise near the schedule singularity. But: the paper **never proposes the truncated read as early warning**, only as an accuracy ablation; the best prefix is an **oracle post-hoc maximum**, not a rule; the optimal prefix ranges from 3/10 to 4/4 across the twelve cells, with **zero truncation gain** in two of them; and the **deployed** detector uses `accel_-2`, essentially the full path. Worse, truncating the denoise saves a fraction of one chunk's *inference* (~278 ms total by an independent measurement), which is noise beside a multi-second reasoning call. **Any lead time in this design comes from firing at chunk generation and letting the prefix execute during the call, not from reading the denoise early.**
>
> **3. ActProbe's overlap signal has an unverified precondition.** Its core feature compares the policy's own predictions for the same physical timestep made at two different decision steps. The paper assumes **the policy itself executes between chunks** and says nothing about an external corrector, a safety filter, or shared autonomy. It also never states the chunk horizon or stride for any of its five settings. Meanwhile the accel paper reports STAC collapsing to 0.06 on pi0.5+RoboCasa precisely because "the policy executes its entire predicted chunk before re-planning" - zero overlap. In the reference harness only 1-15 of 50 steps execute, leaving 35-49 steps of overlap, which is favourable. **Confirm the stride before building on this feature.**

**accel's derivation, with its stated status.** For a maximally certain flow-matching field the Jacobian is an affine isotropic contraction, so every denoising trajectory is a straight line at constant velocity with zero acceleration - **exact** (Theorem 1). A second-order Tweedie identity ties the field's excess over that template to the posterior covariance - **exact pointwise**, at interior schedule times. The posterior-covariance lower bound is **in expectation**, an inequality. The link to the computed statistic is **local**: the authors' own note reads *"theoretical faithfulness of accel is local and holds in expectation, under an exact CFM field and a small-spread family with fixed covariance shape."* The path also bends when the posterior *mean* moves, not only when covariance grows.

**accel's own words on its blind spot.** *"This error originates from high-level reasoning or instruction understanding in the VLM backbone, rather than from uncertainty in the FM head, and is therefore not reflected in FM geometry."*

**ActProbe's guard against memorisation.** The instruction enters only at the recurrent initial state, 1024 dimensions to a 16-wide bottleneck then two 32-wide projections, stated to push the probe toward task-conditional thresholds rather than per-task patterns. **[corrected]** Its overlap-beats-resampling ablation is architecture-matched at **70.5 against 68.2**, not the 72.1 against 68.4 often quoted - that pair compares the full model against an unlearned baseline. Real robot: Unitree G1-D dual-arm humanoid, **6/12 on one task and 5/12 on another**.

**Default is ActProbe alone**, on deployment grounds. pi0.5 runs as a separate service behind `pi05_infer`; ActProbe reads the array it already returns, so the service is untouched. accel requires opening it.

> [!note] Combining them is a Phase 0 ablation, not a design decision
> No paper shows the pair beats either alone, and the comparison is free once both scores exist. Two meanings, only the first is a detector question:
> - **Score fusion** - both read at the boundary, scores combined. Settled offline in Phase 0.
> - **Temporal cascade** - accel fires mid-denoise, ActProbe confirms. Correction 2 above removes most of its motivation.

### 2.3 Prior art

| Paper | Holds | Lacks |
|---|---|---|
| **AEGIS** 2606.06660 | the closest structural match. Two-layer MLP on frozen layer-15 action-expert activations of SmolVLA-450M, split conformal at alpha 0.10, early-harm gate at `t >= max(0.20T, 2)`, budget cap `Kmax = ceil(0.05T)`, escalation to pi0.5-4.14B at the next chunk boundary (H=10), hysteretic de-escalation. Early-window AUROC 0.764 [0.70, 0.84]. Recovered-task rate **0.101** against budget-matched-blind **0.046** and random-trigger **0.051**, Holm-adjusted p = 8.5e-6 and 1.0e-4. Duty cycle 38%, ~44% of always-strong compute. Ceiling 0.319; absolute marginal success 0.156 | escalates to a **bigger VLA**, not a general model. LIBERO-Spatial only. **Reports no wall-clock anywhere** - its compute axis is explicitly a parameter-count schematic, and it twice promises a measured overhead it never prints. |
| **CorrectVLA** 2608.29967 | training-free. A human watches one failed rollout, Claude Sonnet 4.5 structures the correction into (dimension, sign, magnitude, window), and it becomes an additive per-timestep per-dimension bias on frozen pi0.5. 93.0 to 96.3% in-distribution; 10% to 95% on a real xArm7 | a **human** triggers it, offline, once per task. No latency reported. |
| **AESOP** 2407.08735 | a fast embedding anomaly detector triggers a slow generative model that **selects** among precomputed contingencies. Its consensus constraint forces all recovery options to share a control prefix, so the drone descends and slows during the first K steps, explicitly budgeting time for the call. ~10 Hz on a real quadrotor with a Jetson AGX Orin. **And it prints the latency table this field otherwise lacks** | quadrotor and model-predictive control, not a VLA. The slow model never generates a trajectory. |
| **RARRL** 2603.16673 | a reinforcement-learned orchestrator choosing ACT or THINK(role, budget). **Measured end-to-end API latency: GPT-4o-mini 0.82 s mean, 1.34 s p95, 380 tokens per call, no synthetic delay injected** | acts over an abstract five-action space, never a continuous action. Its gate uses failure-frequency proxies and the paper states it provides no explicit uncertainty estimate. **Client hardware and network are not reported.** |
| **Jetson-PI** 2607.12659 | the gating direction proven: a learned confidence head on a 40M future-correction module decides whether to skip the vision-language backbone entirely | **[corrected]** the 8.66x headline is the **full stack** (scheduling, CUDA-graph reuse, GPU-resident buffering, flow unrolling). **The confidence gate alone buys 0.70 to 1.48 Hz, 2.11x.** It skips a perception backbone, not a reasoner; there is no override branch; the skip fraction is never reported. |
| **BCP** 2608.03483 | an ordered-Bernoulli head on a frozen VLA choosing among five execution horizons {30,35,40,45,50}, at **2.03 ms** on an A100, reusing representations already produced so no extra VLA pass. RoboTwin 2.0 + LingBot-VLA: +11.08% on 13 low-success tasks, 89.88 to 93.94% over 50 | **[corrected]** it is **not an external-signal baseline**. It reads visual-language tokens, denoised actions and action-velocity features - VLA-internal features, but with no sampling and no posterior. A third category, and still the fairest competitor to an intrinsic gate. |
| **VLA-ULAP** 2609.18663 | the best published cost curve, three panels of absolute success against VLA-call reduction with retention bands | **[corrected]** the range endpoints are **different operating points**: 76.7% removed at 95.8% retention (VLA-JEPA), 48.8% removed at 97.5% (Cosmos-Policy), 50.7% at 95.0% (GR00T). Risk-aware gain is **0.08-2.00 pp** across pairs, not 0.45-2.00. Schedule is fixed; the risk proxy is input-novelty, not policy uncertainty. |
| **VLA-Corrector (stage-aware)** 2609.06508 | concrete gate hysteresis on pi0.5: risk threshold 0.40, four-window confirmation, ten-step cooldown, evaluated every two steps, verifier at 0.457 ms median **on CPU**. Discards the pending chunk, appends a stage directive, restores the original instruction | no large model in the loop - the directive is a template routed by a stage head, with a generic fallback below 0.9625 confidence. **[corrected]** its 70.9 to 82.6 headline is the **combined-perturbation** column; clean LIBERO is 93.7 to 94.2. |
| **VLA-Corrector (ZJU)** 2607.01804 | a 40M latent monitor on residual visual dynamics; cosine mismatch above a median-absolute-deviation threshold for p consecutive steps truncates the chunk and re-infers under online gradient guidance. A **decoupled** monitor beats a coupled internal head on success rate, 64.35 against 49.55 | no second model. **[corrected]** 1.62-1.68x is aggregate wall-clock across all episodes; **per firing it is 2.12x**, 278.01 ms to 588.52 ms. |
| **RoboMonkey** 2506.17811 | samples and verifies 16 candidates in ~650 ms, ~1.5 Hz on an H100, 28 GB | candidates are Gaussian perturbations of a few base samples, not 16 independent policy calls. |
| **ReconVLA** 2604.16677 | conformalised quantile regression on action-token latents selects the lowest-uncertainty of K samples; Mahalanobis state distance above the 99th percentile flags a state anomaly | the fallback is genuinely **unspecified** - the paper offers only "halting execution or invoking a fallback strategy" and its algorithm terminates at `return Unsafe`. No recovery policy, no experiment. |
| **FPC-VLA** 2509.04018 | a VLM supervisor emits a correction that is applied at **action** level, `a' = a + [dx, dy, dz, 0, 0, dr_z, 0]`, after dual-stream fusion over the VLA's own action history. Triggered only on gripper state change, at most ~3 calls per episode, 1.766 s on keyframes | language is only an intermediate representation; nothing is re-prompted to the VLA. |
| ~~FORTRESS 2505.10547~~ | **[corrected - do not cite for this]** its conformal prediction calibrates an **avoid cost inside the planner**, not a trigger; the trigger is an *assumed external* runtime monitor. Fallback goals and cost functions are **precomputed offline and cached**; only the trajectory is synthesised at runtime, taking 1.28 s on a Jetson Nano. It is not evidence that waypoint fallback works under a conformal gate. |

> [!warning] The most important negative result, restated correctly
> CorrectVLA ran an autonomous version of this idea as a baseline: a model watches the failure video and generates the correction itself, no human. It recovered **0 of 139** in-distribution failures and **0 of 328** out-of-distribution failures.
>
> **[corrected] Three things commonly got wrong about this result.** The model was **GPT-5 mini**, not a frontier model, and the paper gives no prompt details at all. The real-robot "0/20" is **not a paper figure** - Table II reports that baseline as not-run in every row; only prose says it "recovers nothing", and the failure pool was 18, since the base policy succeeded twice. And the diagnosis is *only* about magnitude - *"autonomous correction from visual feedback alone proves insufficient for reliable magnitude estimation"*. The paper never claims the model correctly identifies the axis.
>
> **What still stands.** A weak model, given only video and asked for a free-floating magnitude, recovers nothing. The reference system evades this by handing a strong model the forward-kinematics trajectory and an **absolute pose** interface with clamped deltas. Its 48% is the existence proof that pose-level output works under those conditions. **Preserve that interface in every arm.**
>
> **What does not stand: 2409.03966 is not a pose-output precedent. [corrected]** That paper's VLM emits **discrete directional tokens** from `{up, down, left, right, forward, backward}` scaled by a fixed constant, not a 3D pose delta. Its 0.005 m is **residual distance to the correct alignment position** after 20 steps on a simulated Lego task, not correction accuracy.
>
> CorrectVLA also bounds the prize: Execution Misalignment is ~23%/22% of failures (OpenVLA-OFT / pi0.5) and is the only category the paper calls correctable at inference time. Task Misunderstanding plus Perception Failure is over 70%.

### 2.4 The latency number the field is missing

No paper reports the response time of a frontier reasoning model inside a robot loop. Three measurements bracket it:

| Model | Latency | Source |
|---|---|---|
| Mistral (local, Jetson AGX Orin) | 0.32 s | AESOP Table III |
| GPT-4o-mini, end-to-end API, 380 tokens | 0.82 s mean, 1.34 s p95 | RARRL |
| GPT-3-Turbo with chain of thought, cloud-queried from a Jetson | 3.10 s (sd 0.85) | AESOP Table III |
| **GPT-4 with chain of thought, cloud-queried from a Jetson** | **18.88 s (sd 3.92)** | AESOP Table III |

**At 25 Hz, 18.88 s is 472 control steps.** A pi0.5 chunk is 50 steps, 2 s, and only 1-15 of them execute, so the lead time available from firing at chunk generation is **0.04 to 0.6 s**. `gpt-6-astra` at xhigh reasoning is not faster than GPT-4 with chain of thought.

**Consequence.** Latency cannot be hidden by timing. Freezing is not a design choice, it is forced. This reshapes Axis A below, and it makes the stall measurement the whole contribution rather than one metric among several. AESOP is the only paper that copes, and it copes by making every recovery option share a control prefix so the vehicle can slow down for a budgeted K seconds - on a quadrotor, with K = 1.5 s.

## 3. System design

### 3.1 The loop

The gate is the only inserted component. Everything after it is the reference system unchanged - deliberately, since their Section 7 already confesses three entangled factors.

```
  pi0.5 emits a 50x14 candidate
        |
        v
  ActProbe                                    [2606.08508; ~3 ms, ~24K params]
  reads: chunk-overlap squared error, chunk norm, timestep, task embedding
        |
  above split-conformal cutoff?
        |
        +-- no --> execute a 1-15 step pi0.5 prefix, loop
        |
       yes
        |
        +--> API call issued at chunk generation; the prefix executes during
        |    it, buying 0.04-0.6 s against a latency of seconds. Then freeze.
        |                                     [see Section 2.4]
        v
  slow model called
  gets: 3 RGB views, 14-D proprioception, end-effector poses, instruction,
        execution history, candidate forward-kinematics trajectory
  returns: bimanual pose target + gripper, 1-5 steps      [reference report]
        |
        v
  damped least-squares IK, 5 cm / 0.35 rad clamp          [reference report]
        |
        v
  hysteretic hand-back to pi0.5                           [AEGIS 2606.06660]
  confirm window + cooldown, original conditioning restored
                                              [VLA-Corrector 2609.06508]
```

accel is not in the deployed loop. It is a Phase 0 ablation arm, and Section 2.2 correction 2 removed its lead-time justification.

### 3.2 Where each part comes from

| Loop element | Source |
|---|---|
| Propose, review, accept-prefix-or-correct, re-decide at the boundary | reference report |
| Pose interface, clamp, damped least-squares IK, and the evidence it works | reference report (48%) |
| Why not a free-floating magnitude | CorrectVLA 2608.29967 |
| Gate on a policy-derived score, escalate at a boundary, hysteretic hand-back, duty cycle as headline, early-harm gate, per-episode budget cap | AEGIS 2606.06660 |
| Random-trigger and budget-matched-blind controls, and the intervention paradox that makes them mandatory (arXiv 2602.03338) | AEGIS 2606.06660 |
| Confirm window, cooldown, restore original conditioning | VLA-Corrector 2609.06508 |
| Hedge motion during the call, and the only latency table in the field | AESOP 2407.08735 |
| End-to-end API latency for a small model in-loop | RARRL 2603.16673 |
| Precedent for gating the big model down | Jetson-PI 2607.12659 |
| Cost curve to plot against | VLA-ULAP 2609.18663 |
| Competing gate design | BCP 2608.03483 |
| Cheaper override than regeneration | VLA-Corrector ZJU 2607.01804 |
| Axis B option 2, rank or veto | RoboMonkey 2506.17811, ReconVLA 2604.16677 |
| Axis B option 3, action-level correction from a language intermediate | FPC-VLA 2509.04018 |
| Detectors | 2607.27933, 2606.08508 |

### 3.3 Novelty, stated honestly

Every piece is published. AEGIS has the gate, the controls and the hand-back but escalates to a bigger VLA and reports no wall-clock. CorrectVLA has the action-level override but a human triggers it, offline. RARRL has a real API in-loop but acts at plan level. Jetson-PI proves the gating direction on a perception backbone, and its headline is mostly kernel engineering. AESOP has the latency problem solved but on a quadrotor selecting among precomputed options. The reference report has the full override and no gate.

Nobody holds them together. **The contribution is the gate plus the stall measurement, not a new architecture.** The architecture is the reference report's.

## 4. Axes under study

**Axis A, coupling.** Section 2.4 changes the ranking here. If the reviewer takes seconds and one chunk buys at most 0.6 s, anticipatory timing is arithmetically irrelevant.

| Cell | Status after verification |
|---|---|
| **A1, freeze on a reactive trigger** | **the default.** The reference system minus suppressed calls. |
| A2, freeze on an anticipatory trigger | **downgraded.** Firing at chunk generation rather than at prefix end buys 0.04-0.6 s off a multi-second stall, so ~3%. The half-path denoise read buys ~140 ms more and is unsupported as an early-warning mechanism. Keep as a free implementation detail of A1, not a separate arm. |
| A3, hedge on an anticipatory trigger | **the only way to keep moving**, and unproven on a manipulator. AESOP budgets 1.5 s on a quadrotor by descending and slowing; there is no analogue for a bimanual arm mid-task holding an object, and no paper attempts one. High risk, high reward. |
| A4, keep moving on a reactive trigger | **negative control only.** Isolates staleness cost: same trigger, same model, wait removed. **[repo]** note the harness offers no rollback, so a correction landing on a state that moved cannot be undone - this arm can only degrade, which is what makes it a clean control. |

**Axis B, request type.**

1. **`eef`, an absolute pose target.** The reference interface, unchanged. Most capable, slowest, most tokens.
2. **`edit`, a delta on the student's own target. [repo]** Already implemented in the harness and largely overlooked: per arm a `delta_position`, a `delta_rotation_vector` and a gripper `keep/open/closed`, applied to the chunk pi0.5 already produced. A zero-or-keep edit leaves that arm's target untouched. Strictly less to generate than a full pose, and it keeps the policy's own trajectory as the prior - which is exactly the property CorrectVLA's failure says matters. **This should be the cheap arm, not a language rewrite.**
3. **Rank or veto** resampled candidates. Output is an integer, so latency falls sharply. Ceiling is hard: selection cannot fix a mode present in every sample.
4. **Re-instruct.** FPC-VLA shows an action-level delta derived from a language intermediate working at ~1.766 s per keyframe call with at most three calls per episode. Cheapest; discards the 3D contact reasoning the reference report credits to its reviewer.

The axes interact: a cheap request type is the only thing that could make A3 tractable.

## 5. Phase 0, offline feasibility

**Purpose.** Does a policy-derived detector fire where the reviewer actually corrected? No API cost, no robot. If recall is near zero at a usable false-alarm rate, every cell in Section 4 is dead.

> [!warning] Why it might fail
> The reference report attributes corrections to **grounding** errors: wrong object, wrong position, wrong direction. Those are **confident** errors. accel's own limitations section says the error then lives in the vision-language backbone and *"is therefore not reflected in FM geometry"*. These two facts are in direct tension and have never been tested against each other.

**Data.** `ZihuiGao/dpsk-robot-policy` on HuggingFace, non-commercial research licence. 28 complete RoboDojo hybrid episodes, 1,841 decision points, 22,842 control steps, 1,964 corrected (8.6%), bimanual ARX X5. Each decision carries the 50x14 candidate, three camera frames, proprioception, and a three-way label: accepted prefix, pose replacement, chunk edit.

**Steps.**

1. Join by request identifier, **not** file position. There are 1,869 observations, 1,842 proposals and 1,841 executions, so positional joins misalign.
2. Collapse the label to binary, corrected against accepted. Report the three-way split separately: an `edit` is a delta on the policy's own target, so it is weaker evidence than an `eef` replacement. **[repo]** the harness's own decision log already carries `codex_override` (true for `edit` and `eef`) and `prefix_only` (a `student` decision taking fewer than 50 steps), which is the label definition to match.
3. **Measure the stride first.** ActProbe's overlap feature needs `s < H`, and its paper never states either value. Recover the executed prefix length per decision from the dataset and confirm the overlap actually exists before scoring anything. Then flag every pair whose preceding segment was a model correction rather than a policy prefix - the feature's validity there is unsupported - and report with and without them.
4. Score with **ActProbe** on the saved chunks, no policy inference needed. Train leave-one-episode-out over the 28; report held-out only. Reproduce its inputs faithfully: the two scalars, the normalised timestep, and the frozen task embedding through the 16-wide bottleneck.
5. Score with **accel**. The denoise path is not stored, so this needs a pi0.5 forward pass on the saved frames. Flow matching is stochastic, so recover the policy seed from the shipped pipeline snapshot, or verify distributional agreement and score across several samples. Calibrate its CUSUM height on successful episodes only - but note only 4 of 28 succeeded, well short of the paper's M=50, so calibration will be the weakest link.
6. Report recall on the corrected set at 0.1 false alarms, plus the full curve, per detector.
7. Break recall down by correction type, and by whether the episode succeeded.
8. **Detector ablation, free:** ActProbe alone, accel alone, both fused, at matched escalation budget. Add BCP as a fourth arm if its head trains on this data - note it reads VLA-internal features, so it needs the same forward pass accel does.
9. Convert each threshold to an escalation budget and compare against the 33% oracle floor.

**What this actually measures.** The label is the reviewer's *decision*, not ground-truth failure, and that reviewer's judgement is itself unvalidated. That is the right target anyway: the gate's job is to predict **where review would have changed something**, not to predict failure.

**Gate to Phase 1.** Recall on corrected decisions materially above the escalation budget at the same threshold. A detector firing on 30% of decisions and catching 30% of corrections has learned nothing.

> [!warning] State these limitations in writing
> The reviewer here is deepseek-flash at maximum effort, not gpt-6-astra at xhigh, and the source label is inherited from the original pipeline. Correction rate 8.6% of steps against the reference's 14.4%. Success 4 of 28. The run stopped when API credit ran out, so the 22 missing cases are those in flight, not a random sample. Different hardware, and the authors observed identical seeds scoring 1.00 and 0.10 across runs. Separately: neither detector paper evaluated a bimanual 14-DoF platform, and accel was never run on a real robot at all. **Phase 0 establishes whether the signal exists, not its magnitude under the reference reviewer.**

**If the dataset proves unusable.** The reference authors publish frozen evaluation cases and episode-level counts, but no per-decision data. Regenerating it needs Isaac Sim, RoboDojo assets, the published pi0.5 checkpoint and authorised frontier access. That is a Phase 1 cost.

## 6. Phase 1, coupling screen

**Purpose.** Pick one coupling from Axis A, on effects large enough to resolve at small n.

**Design.** A1 and A4 always; A3 only if a hedge policy can be defined for a bimanual arm. Request type held at the cheapest Axis B option. Detector and threshold fixed at the Phase 0 operating point.

1. Choose tasks spanning the reference report's difficulty stratification, not its easiest.
2. **Measure the latency nobody has measured.** Per-call response time for the reviewer at its deployed reasoning effort, and cumulative robot-idle wall-clock per episode. Report the distribution, not just the mean - AESOP's GPT-4 figure carries a standard deviation of 3.92 s on a mean of 18.88 s.
3. Run against a common seed set, aligned per instance on task, scene, layout, reset and policy seed, matching the reference protocol.
4. Record per arm: success, native Score, calls per episode, tokens, cumulative stall, end-to-end wall-clock including model time.
5. **Select on stall and call count, not success rate.** Those are large multiplicative effects with low variance. Success rate is a proportion near 0.5 and needs an order of magnitude more trials.

## 7. Phase 2, confirmation

**Purpose.** Establish the success-rate claim against the reference anchor.

1. Run the surviving coupling crossed with the Axis B request types, full ten-task set.
2. Set trials per arm from the margin you want. At a rate near 0.48, one-sided alpha 0.025, 80% power, trials per arm run as **3.9 / margin²**:

| Margin | Trials per arm | |
|---|---|---|
| 10 points | ~390 | a genuine equivalence claim, expensive |
| **15 points** | **~175** | **defensible, the recommended target** |
| 20 points | ~100 | weak, but still bounds the loss above the 26% direct arm |
| the reference's 50 | ~30 points | not a claim, a sanity check |

Two arms minimum, plus two controls, so multiply. **This table is the scale decision.**

3. **Run both controls**, following AEGIS: a random trigger at the detector's own rate, and a budget-matched blind arm spending the same calls on a fixed schedule. AEGIS's own margins show why - its method beat random-trigger by only 5.0 points of recovered-task rate, which would have been invisible without the control.
4. Report against the reference anchors on the same subset: hybrid 48%, direct 26%, pi0.5 15.67%.

## 8. Metrics

| Tier | Metric |
|---|---|
| **Primary** | cumulative stall per episode; calls per episode. Never measured in this architecture, and Section 2.4 says stall dominates. |
| **Non-inferiority** | success rate and native Score against the 48% and 62.60 anchors, as an interval. Note the Score has no published formula. |
| **Secondary** | tokens per episode; end-to-end wall-clock including model time; realised operating point against the offline calibration |
| **Diagnostic** | **correction precision** - the fraction of triggered calls where the model actually changed the action. 32.7-35.4% in the reference system by construction. Raising it towards 100% is the whole point. |
| **Plot** | absolute success against fraction of calls removed, on VLA-ULAP's axes, with its retention bands. **Its y-axis is absolute success, not retention**, so an overlay is only valid within a single base-policy panel. |

## 9. Risks

> [!warning] Detector blindness
> The class the reviewer corrects may be the class the detector cannot see. accel says so about itself. Phase 0 exists to test this before any spend.

> [!warning] The overlap precondition may not hold
> ActProbe's feature assumes the policy executes between chunks. Under an external corrector it is undefined, and its paper never states the stride it needs. Phase 0 step 3 measures this first.

> [!warning] Conformal validity does not survive the loop
> Both detectors calibrate on an uncorrected policy. Once corrections alter the trajectory distribution, the guarantee is void. Treat the gate as a heuristic; claiming a preserved bound is a separate, harder contribution.

> [!warning] The intervention paradox
> A high-AUROC detector can still cost success, because interventions that rescue failing trajectories also derail succeeding ones - 26 points at AUROC 0.94 in the LLM result AEGIS imports. This is why the two controls are mandatory.

> [!warning] Gating removes a capability, not only cost
> The reference reviewer notices the simulator has not terminated and re-checks its own work. Nothing is *uncertain* when a policy confidently repeats a failed action, so an uncertainty gate cannot fire there. A steps-without-progress trigger is the likely remedy, and a second trigger to defend.

> [!warning] The claim inverts by benchmark
> On RoboLab the order reverses: reviewer alone 49/50, hybrid 46/50, policy 18/50. Gating the reviewer down hurts where System-1 is weak. The claim holds only where the fast policy is task-competent. Restrict to that regime and say so, or run both and report the boundary as a finding.

## 10. Unresolved questions

1. **What is gpt-6-astra/xhigh's actual response latency?** Unpublished. Section 2.4 brackets it above GPT-4 chain-of-thought's 18.88 s, which would make freezing unavoidable and A3 the only alternative. **Measure it first; it is one API call.**
2. **What budget, in tokens and wall-clock?** Section 7 step 2 converts it into claim strength: ~175 trials per arm buys a 15-point bound, ~390 buys 10.
3. **Is frontier access available at that reasoning effort**, or must a weaker model stand in? A mini-class model at ~0.82 s is hideable inside one chunk, but CorrectVLA's zero came from a mini-class model.
4. **Can a hedge policy be defined for a bimanual arm?** AESOP's consensus-prefix trick has no published manipulator analogue. If not, A3 dies and freezing is the only design.
5. **Which benchmark carries the headline** - RoboDojo where the hybrid wins, RoboLab where it loses, or both with the boundary as the result?
6. **Single trigger, or dual** with a stall detector to recover the capability in Section 9?
7. **Does a feature-based gate beat a posterior-based one?** BCP reads VLA-internal features with no sampling at 2.03 ms. If it matches, the uncertainty framing loses its point and this becomes a cheaper-features paper.
8. **What context does the model wake up with** after skipped decisions? Full history preserves continuity but lets tokens creep back towards the ungated arm. Current observation only is cheap but discards the execution history the reference system relies on.
