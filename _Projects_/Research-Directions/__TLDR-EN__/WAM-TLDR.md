---
title: "TL;DR: Promising Research Directions: World Action Models"
aliases:
  - "WAM TL;DR"
  - "WAM skim"
tags:
  - tldr
  - research-directions
  - WAM
  - embodied-AI
  - world-model
---

# TL;DR: Promising Research Directions: World Action Models

> [!info] What this is
> A skimmable TL;DR of [[WAM|Promising Research Directions: World Action Models]]. Each direction gives four things: **the bet**, the reasoning, the sharpest open questions, the risks. Full detail stays in the source. Plain-language version: [[__ELI5-EN__/WAM-ELI5|ELI5]].

> [!abstract] Overview
> A World Action Model imagines a future and picks an action in one model. Its tension: the imagined state must be stored somewhere, and every storage choice trades detail against speed and OOD robustness, a policy needs both. The non-consensus thesis: a WAM's imagination is not one fixed thing to optimize. Train density is separate from deploy density (A1). The encoder objective matters more than latent-vs-pixel (A3). Contact physics needs *discrete* structure no smooth latent reaches (B1). The imagination's most lasting output is a *training corpus*, not an in-episode rollout (B4). And some ambiguities aren't solved by imagining or checking harder, only a real action taken to gather new evidence closes them (C1). The storage choice depends on the task, and imagination is a surface you can check, not just a planning shortcut, and now, sometimes, a thing you probe.

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A: Substrate & Encoding | A1–A3 | The imagined state must be stored somewhere, and every storage choice trades detail against deploy latency and OOD retention |
| B: Training-Time Grounding | B1–B4 | Imagination drifts from physical reality unless a training-time signal forces the match |
| C: Action-Space Completeness | C1 | The WAM's action space has no category for actions taken purely for their information value, so no amount of storage refinement or training-time checking can close an ambiguity only a real action collapses |

## A: WAM Substrate & Encoding
*The imagined state lives somewhere: a latent vector, a token grid, a 3D scene, or a wrench trajectory. The three directions hit the same representation question: how dense at train vs deploy (A1), which modality it spans (A2), what its latent encodes once dense-vs-sparse is fixed (A3).*

### A1: Hybrid Latent+Pixel WAM Architectures
> [!abstract] The bet
> Use a renderable-3DGS dense head you drop at deploy. It beats a *matched-capacity 2D-video* dense head (the UVA form) on LIBERO-Plus OOD retention by ≥5 pp *at matched in-distribution SR*, both held to ≥97.2% (the VLA-JEPA pure-latent reference). The latent-only deploy path stays under 2× pure-latent latency, far below the 4.8× pixel-WAM cost. The non-consensus quantity: the 3D-structure × OOD margin, isolated against UVA's 2D-video head.

**Why**: Pixel/video is robust but slow; pure latent is fast but opaque. The drop-the-dense-head mechanism is settled (UVA: +40% real OOD, head dropped at inference; UWM confirms). A1's live assumption: the dropped head's *form* is interchangeable.

**First-principles**: *Principle:* train density and deploy density are separate. *Challenged:* UVA/UWM's dense head is 2D-video, and now a third pole cuts the other way, ImageWAM argues the dense signal need not be a video at all (single-edited-image, 83.1% LIBERO-Plus at −75% latency), so nobody has run the multi-form sweep yet. *Wager:* 3D structure (GaussianDream: 98.4% LIBERO, 34.4→50% real; GeoSem-WAM: +6.6 pp real) carries OOD geometry a flat video head cannot.

**Sharpest questions**: 1) Four-arm A/B at matched capacity (no dense head / 2D-video / 3DGS / single-edited-image, plus a sparse metric-3D-track arm), latent-only at deploy: does the 3DGS head lift LIBERO-Plus OOD ≥5 pp at matched 97.2% in-dist SR against the 2D-video head specifically, or does ImageWAM's single-edited-image form (83.1% LIBERO-Plus, no video at all) already win the OOD margin without density? 2) Sweep deploy full-pixel → latent-only: does real SR stay ≥50% down to <2× pure-latent latency, and does Faster-WAM's 66.5 ms + 75.0% LIBERO-Plus already sit at that frontier? 3) Do distillation (Flash-WAM, 23× speedup) and co-training land at *different* SR-latency points?

> [!warning] Risks
> - Two-branch training doubles compute. → Fix: distill a pre-trained 3DGS WM into the latent encoder (GaussianDream/Flash-WAM pattern).
> - Latent-pixel branches drift apart. → Fix: anchor both to a shared target (DexWorldModel's DINOv3 targets).
> - In-distribution is saturated (pure latent 97.2% LIBERO, GaussianDream 98.4%). → Fix: bind the bet to OOD (LIBERO-Plus) + deploy latency, not in-dist SR.

### A2: Tactile/Force-Integrated WAM Imagination
> [!abstract] The bet
> Use a WAM head that forecasts a *future 6-DoF wrench* (force+torque) as a rolled-forward output the policy acts on inside imagination, with *no* force sensor at deploy. Three papers already forecast a future 6-DoF wrench (FAWAM ~85%, MuSe, TORL-VLA), but all three keep the sensor at deploy and hand the forecast to a fixed control law or an outer refiner rather than letting the policy reason over it directly. A2's surviving wedge is two-part: sensorless forecasting (still clears FD-VLA's present-time token 61.1% by ≥5 pp, and recovers DexViTac's vision-only tactile drop 83.3%→43.3% toward ~63%) and a policy that reasons directly over the imagined rollout rather than a fixed controller-target coupling. MuSe's own ablation already shows the controller-target coupling alone beats mere conditioning (vase-wiping 11.5/15→8/15) — the open question is whether full rollout-reasoning beats even that coupling.

**Why**: WAMs imagine visual/proprioceptive futures but rarely tactile/force ones, yet force dominates contact-rich manipulation. Force-prediction is now crowded even at the future-6-DoF-wrench level (FAWAM, MuSe, TORL-VLA) — but all three keep the sensor at deploy and consume the forecast through a fixed controller or an outer refiner. A2's live assumption is twofold: the forecast must be sensorless at deploy, and the policy — not a fixed control law — must reason over the rollout directly.

**First-principles**: *Principle:* in contact, force is cause and motion effect; rolling forward only the effect can't pin contact dynamics. *Challenged:* FAWAM, MuSe, and TORL-VLA already forecast a future 6-DoF wrench, so that claim is taken too — the live gap is sensorless + policy-reasoning, not the wrench forecast itself. *Wager:* the tactile latent is load-bearing (DexViTac ablation 83.3→43.3%) and predictable from vision+proprioception, so a sensorless wrench-rollout head has a tractable target.

**Sharpest questions**: 1) A/B sensorless future-wrench-rollout (via either an architecture lever or a train-time-only supervision lever) vs the *sensored* ceiling (FAWAM/MuSe ~85%) vs the present-time token vs vision-only: how close does sensorless come to the sensored ceiling? 2) Does the policy reasoning directly over the imagined rollout beat MuSe's fixed-controller-target coupling and TORL-VLA's outer-refiner-context coupling, at matched wrench-prediction accuracy — or does MuSe's simpler coupling already capture most of the gain? 3) Does the sensorless gap-closing hold uniformly across high-force and light-touch regimes, or is it concentrated in high-force tasks? HapticVLA's sensor-free student already beats its own sensored teacher (86.7% vs 75–81.7%) on fragile jar/waffles/egg tasks, arguing against the naive "sensorless degrades in light-touch" intuition — the test is run to decide, not to confirm.

> [!warning] Risks
> - Noise floor, but the closest evidence disagrees: HapticVLA's sensor-free student beats its sensored teacher on fragile tasks. → Fix: run the light-touch-vs-high-force split as an open question, not an assumed degradation.
> - Cross-sensor brittleness, 60.3% zero-shot (TaF-VLA) is not deploy-ready. → Fix: use DexViTac's kinematics grounding to stabilize the latent.
> - Force-prediction is crowded, including future-6-DoF-wrench papers (FAWAM, MuSe, TORL-VLA). → Fix: claim only sensorless + policy-reasons-over-rollout, and test each half separately — sensor status is orthogonal to coupling type.

### A3: Latent-Encoding Quality for WAM Imagination
> [!abstract] The bet
> The deliverable is the matched-capacity, matched-deploy-latency three-arm encoder sweep (continuous / discrete-FSQ / VQ) scored on closed-loop SR, not a predicted single winner. The live expectation is a *regime-contingent contingency map*, not a universal victor: discrete-FSQ favours contact / return tasks (DC-MPC), continuous favours fine manipulation (CLAM), and the null (all three tie at matched dim) is *pre-registered*. The recon-vs-semantic margin (Semantic-LDM-WM's +9.8 pp closed-loop / +13.6 pp OOD) reproduces *with a reconstruction/VAE arm* on JEPA-VLA's own non-LDM backbone (which left out the recon arm) as the publishable floor, EgoWAM already shows the same recon-vs-semantic gap on a *different* HPT/human-video backbone, so this is reproduction, not a cold test. A clean contingency map is publishable even with no global winner.

**Why**: A1 fixes *how dense*; A3 fixes *what the latent encodes*. A latent trained to reconstruct appearance spends capacity on detail the controller throws away (Semantic-LDM-WM swaps only the encoder objective, closed-loop SR swings +9.8 pp). The semantic-vs-static side is settled (JEPA-VLA: video-predictive wins, +6.7% LIBERO-plus), though JEPA-VLA never ran a reconstruction arm on its own backbone, and EgoWAM now partially pre-empts that swap on a *different* (HPT, human-video) backbone, finding semantic beats reconstruction by up to 4× OOD. A3's contested assumption is the bottleneck *type*: DiLA bets continuous > VQ/VAE, CompACT bets discrete-FSQ; nobody has run a recon/VQ/continuous three-arm at matched dim on closed-loop SR.

**First-principles**: *Principle:* the encoder objective sets the control ceiling, not architecture. *Challenged:* DiLA (continuous, scored on generation) contradicts CompACT (discrete-FSQ, on planning latency); neither scores manipulation closed-loop SR. *Wager:* "what to preserve" is causal for control, so a matched-dim three-arm sweep separates the regimes, with the winning encoding contingent on task family rather than a single global victor.

**Sharpest questions**: 1) Three-arm at matched dim (continuous DiLA vs discrete-FSQ CompACT vs LGQ/VQ), same policy, closed-loop SR + stability: does the winning arm flip by task family (discrete-FSQ on contact / return, continuous on fine manipulation), or do all three tie (the pre-registered null)? 2) Add a reconstruction/VAE arm to JEPA-VLA's backbone (recon-VAE vs DINOv2 vs V-JEPA 2): does Semantic-LDM-WM's ≥9.8 pp closed-loop / ≥13.6 pp OOD margin reproduce, matching EgoWAM's up-to-4× OOD gap on its own (HPT) backbone? 3) Are control-winning encodings exactly the ones that pass LeJEPA's isotropic-Gaussian identifiability test?

> [!warning] Risks
> - Encoding gain is dataset-specific (+9.8/+13.6 pp may not transfer off Bridge-V2). → Fix: reproduce on a second backbone + dataset.
> - Semantic latents destabilize diffusion training. → Fix: reuse Semantic-LDM-WM's wide-head DiT + S-VAE compression recipe; report stability.
> - Encoding quality ≠ controllability. → Fix: pair the IDM-recoverability diagnostic with closed-loop SR and LeJEPA's identifiability test, not action-recovery alone.

## B: WAM Training-Time Grounding
*A WAM that imagines freely imagines physically impossible futures, and a policy trained on those inherits the impossibility. The four directions install a training-time signal that keeps imagination honest: discrete contact structure (B1), a self-evolution loop that checks its dreams (B2), forward-inverse calibration (B3), a physics-validation filter on synthesized data (B4).*

### B1: Contact-Aware (Discrete-Mode) WAM for Fine Manipulation
> [!abstract] The bet
> Use an *explicit, tactile-supervised* contact mode $c_t \in \{\text{no-contact, making, in-contact, breaking, slipping}\}$, its taxonomy distilled from DOT-Sim contact ground truth, not discovered by a reward-driven gate. It hits >90.5% AutoMate (the contact-naive ceiling) and sub-millimeter assembly with two properties: (a) smooth WAMs cannot reach it at any scale; (b) PRISM-WM's *implicit* MoE-gated mode latent cannot match it without the taxonomy.

**Why**: Latent WAMs handle free-space but fail at insertion/assembly: contact physics is locally non-smooth, and friction-cone boundaries and slip-stick are abrupt discrete state changes a smooth latent approximates only by splitting into pieces. "Discrete beats smooth" is consensus, but PRISM-WM proves it only for *locomotion* with an *implicit* gate, and DHAL learns 3-mode automata as locomotion. B1 bets that at sub-mm precision the modes must be *explicit, tactile-supervised*.

**First-principles**: *Principle:* contact regimes are categorically distinct with distinct governing equations (DOT-Sim). *Challenged:* PRISM-WM/DHAL use implicit gates on locomotion; DexWorldModel's continuous latent caps out; Discrete-WAM's discreteness is scene-level. *Wager:* DOT-Sim's MPM sim can *manufacture* the make/break/slip labels a smooth WAM cannot self-generate, so the explicit 5-mode taxonomy is the residue an implicit gate leaves untouched.

**Sharpest questions**: 1) Three-arm A/B at matched capacity (continuous-only / implicit-gated discrete / explicit-tactile-supervised discrete) on AutoMate's 8 tasks: does explicit supervision beat both above 90.5%? 2) Does scaling a smooth physical WM (PhysWorld) plateau *below* the discrete-mode WAM, or rise to match it? 3) Distill DOT-Sim contact labels into the discrete latent: does insertion SR *track* contact-mode classification accuracy?

> [!warning] Risks
> - Discrete-latent optimization is high-variance (Gumbel-softmax/REINFORCE). → Fix: start soft, harden over training (annealed temperature); report mode-classification accuracy.
> - Contact-mode supervision needs a simulator. → Fix: distill from DOT-Sim / Real-to-Sim GS twins; test sim-to-real retention separately.
> - A discrete-mode WM has a locomotion prior (PRISM-WM). → Fix: make the explicit-vs-implicit head-to-head and classification accuracy the first milestones; keep the wedge at sub-mm + tactile-supervision.

### B2: WAM-Driven Self-Evolution & Recovery
> [!abstract] The bet
> Against RISE/WoVR as imagined-RL baselines, add three missing pieces: an *active* failure-finder (vs RISE's passive low-advantage discovery); an imagined-vs-real ρ > 0.7 (Pearson) *stop gate* anchored to Persistent Robot World Models' 0.822; a Pre-VLA-class *separate* verifier at ≥0.83 F1. This yields higher per-cycle real-SR gain at equal rollout budget, *without* forgetting (WMAR-style, +0.071 vs 0.665). If the three tie a plain RISE-style passive loop at matched budget, they are unnecessary.

**Why**: The L3 Evolver (an agent that revises itself when predictions fail) is "emerging not mature". EWAM now integrates the full detect→route→correct/rollback→retain loop end-to-end, so full-loop integration alone is no longer the open question. What EWAM still leaves on the table: an active (not passive/online-encountered) failure-finder, and an imagined-vs-real ρ-specific stop-gate (EWAM gates on an experience filter, not ρ). A recovery policy only learns from failures it can *generate*, so the loop is capped by how widely the WM imagines failure. The *imagined-RL-improves-SR* half is 2026 consensus (RISE, WoVR +29.3 pp, VLAW +39.2 pp, World-VLA-Loop), and StressDream now covers the active-failure-finder piece too (VLM-steered stress events lift real SR 39%→71%). B2's live assumption: what's left, after EWAM and StressDream, is the ρ-gate and the separate verifier, and an *ungated, unverified* loop still suffices without them.

**First-principles**: *Principle:* reachable recovery competence is bounded by what the WM is actively driven to imagine. *Challenged:* RISE/WoVR/VLAW drive real improvement but find failures *passively* and run an *ungated, unverified* loop. *Wager:* the three additions are buildable from SPIRAL's imagine→verify→GRPO spine and the ρ=0.822 anchor.

**Sharpest questions**: 1) Recast RoboMD as a WAM adversary (active finder), or lean on StressDream's VLM-steered stress-event generation (39%→71% real): does either beat RISE's passive low-advantage discovery on real recovery SR + failure-mode coverage at equal budget? 2) Does real SR rise monotonically only while ρ > 0.7 and stall once ρ drops, is ρ the operative stop condition? 3) Gate recovery candidates through a ≥0.83-F1 separate verifier: does it beat an unverified loop, gap largest where the WM hallucinates most?

> [!warning] Risks
> - Misevolution drift, self-reward biases amplify across cycles. → Fix: red-team each cycle (JailWAM/SELF-REDTEAM); keep a novelty bonus against entropy collapse.
> - Reward hacking on imagined SR. → Fix: periodic real-robot validation + Pre-VLA rollout truncation; the ρ > 0.7 gate catches it.
> - WAM drifts from real dynamics. → Fix: outer-loop WAM updates + the ρ stop condition; validate against the joint causal-binding metric, not imagined SR.

### B3: Self-Verifying / Calibrated-Imagination WAM
> [!abstract] The bet
> On a *latent robot WAM*, train-time forward-inverse calibration beats a matched runtime-only verifier on two fronts: ≥2× WM sample-efficiency and +22% downstream reward at equal labels (WAV's margins as target), a head-to-head no paper has run. *And* training the WM to maximize imagined-vs-real ρ as an objective yields higher final ρ than gating on it (vs PiL-World's r=0.94 / Persistent Robot World Models' 0.822). If the verifier matches train-time calibration, or ρ is no higher trained-for, the wedge is empty.

**Why**: The L3 Evolver needs to know *when* a prediction failed, but uncertainty estimation "often fails in under-explored data regions." The verify-cheaper-than-generate asymmetry is collectively owned: WAV (2× sample-eff, +22% reward, no extra labels), SWIRL (+26.4% on action-free sequences), DeFI (81.3% real Franka), LAPO+ (IDM is a lower-complexity class). B3's unclaimed assumption: *when* you calibrate (train vs runtime) is a free choice, and ρ is only a gating diagnostic, never a *trainable objective*.

**First-principles**: *Principle:* verifying is cheaper than generating; the action-relevant signal is low-dimensional. *Challenged:* the runtime line (Pre-VLA, FIPER) treats calibration-time as irrelevant and ρ as gate-only. *Wager:* shaping the dream during training beats patching it after, and imagined-vs-real ρ is directly maximizable as an objective.

**Sharpest questions**: 1) Apply the forward-inverse signal as *train-time* calibration vs a Pre-VLA-style *runtime* filter on one JEPA WAM: does train-time win by ≥2× sample-efficiency and +22% reward? 2) Treat B2's ρ > 0.7 gate as B3's *objective*, train the WM to maximize imagined-vs-real SR correlation: higher final ρ than ρ-as-stop only? 3) Does WAV's plausibility/reachability *disagreement* signal pick which real interactions to collect next, reaching target SR with fewer than uniform collection?

> [!warning] Risks
> - Sparse inverse model misses subtle dynamics. → Fix: bound the claim to where action-relevant features are recoverable; pair with B1's discrete contact modes.
> - Uncertainty gating too conservative. → Fix: tune the penalty on a held-out real-robot calibration set, not sim alone; report the exploration cost.
> - Calibration ≠ correctness, a WM can be well-calibrated about being wrong. → Fix: validate against B2's imagined-vs-real ρ AND the joint causal-binding metric.

### B4: WAM-as-Data-Engine
> [!abstract] The bet
> VISTA's kinematic-physics-feasibility filter — whose load-bearingness on human-teleoperated UMI data is shown by a score-controlled comparison (0.65 high-score vs 0.00 low-score, stapler placement, RealMan) — reproduces a ≥15 pp downstream-SR gap when applied, via an IDM that converts RoboDream's generated video into scoreable trajectories, to RoboDream's compositional-engine rollouts it was never validated against. A success-replay filter (CRAFT) does not transfer as cleanly. This is a *new*, untested extension of VISTA's result — VISTA's own number never touched a generative engine. The engine-beats-collection claim (≥25 pp SR, RoboDream +26.2 pp; ≥2× cheaper, 2.2×) is the *settled* backdrop, not the bet. The transfer claim must also survive three named confounds: which IDM bridges pixels to a trajectory, which embodiment the filter is scored for, and which sub-component of the filter is doing the work. If the gap vanishes on RoboDream's rollouts, or any of those confounds turns out to be driving the number instead of the filter, the filter's load-bearingness is not what it appears and the claim is wrong.

**Why**: The field knows a WAM data engine helps, and single-generator filter-ablations now isolate which *property* of the data is load-bearing (WM-DAgger's filter-ablation drops SR 96.7→46.7%; SAGE-Scene's physics-critic-alone cuts collisions 7.8→1.9%) — but nobody has tested whether a filter's load-bearingness, shown on non-generated data, transfers when applied to an actual generative engine's rollouts. A video can look right and be kinematically impossible.

**First-principles**: *Principle:* executability is a filter property, not a generator property — VISTA's score-controlled 0.65-vs-0.00 comparison shows this on human-teleoperated data, but VISTA has no generative engine of its own, so whether that property survives contact with an actual generator is untested, not something VISTA's number already proves. *Challenged:* the data-engine line (RoboDream, AnchorDream, DreamGen) treats the engine as the contribution, not an ablated filter — and treats the bridging IDM, the target embodiment, and the filter's internal structure as nuisance to average away rather than testable confounds. *Wager:* a kinematic-physics predicate is intrinsic to the data, so it carries over from teleop data to a generator's rollouts where CRAFT's success-replay and GE-Sim 2.0's learned VLM-judge will not — and that transfer claim survives being probed on each confound in turn.

**Sharpest questions**: 1) Apply VISTA's kinematic filter to RoboDream's rollouts via an IDM bridging step, and CRAFT's success-replay filter to the same rollouts: does the kinematic filter reproduce a ≥15 pp gap analogous to VISTA's 0.65-vs-0.00 result, while success-replay shows a smaller one — isolating filter type as the transferable variable? 2) Does success-replay actually fail to transfer, or was that assumed rather than measured (CRAFT's 89.3% is cross-embodiment, not cross-generator)? 3) Does the same gap hold when VISTA's filter is applied instead to DREMA's 3DGS-physics-twin rollouts — a structurally different generator than RoboDream's video-diffusion, scored directly off DREMA's own physics-engine trajectory state with no IDM needed — showing the property transfers across generator architecture classes, not just within one? 4) Swap three structurally different IDMs (WAV's sparse inverse, MoLA's mixture-of-IDMs, StableIDM's truncation-robust refinement) into the same VISTA-on-RoboDream ablation: does the gap stay stable, or does it track each IDM's own accuracy — meaning the number was measuring IDM quality, not filter transfer? 5) VISTA's own data shows the same trajectories score low and fail on RealMan but score high and succeed (0.80 SR / 1.00 post-grasp SR) on R1Pro — does a RealMan-calibrated score applied embodiment-blind to a different generator's target embodiment still show the gap, or does it require re-scoring per embodiment first? 6) VISTA's filter is a product of three sub-scores (smoothness, self-collision, execution-fidelity) — does the collision/fidelity pair alone reproduce most of the gap (echoing SAGE-Scene's physics-critic-alone result), meaning the cheap embodiment-agnostic smoothness score was never the load-bearing piece?

> [!warning] Risks
> - Synthesized data looks plausible but isn't executable. → Fix: make a physics-validation filter mandatory; report the score-controlled (high-score vs low-score) downstream SR gap as the first ablation.
> - The IDM bridging step is unproven, not a controlled variable. → Fix: sweep three different IDMs and regress gap-vs-IDM-quality directly (question 4); if the gap tracks IDM accuracy, treat the transfer claim as untested, not confirmed.
> - The "success-replay does not transfer" foil is asserted, not shown, CRAFT's 89.3% is cross-*embodiment*, a different invariance than cross-*generator*. → Fix: measure success-replay's transfer directly; if it transfers equally, demote the headline to "ground-truth-anchored filters transfer."
> - The 15 pp differential may sit below detectable power at RoboCasa-100's per-seed sample size. → Fix: run the power calc (n needed to detect 15 pp at p<0.05) before the ablation; if infeasible, the differential can't be the headline regardless of truth.
> - A RealMan-calibrated score applied embodiment-blind could silently inflate or deflate the reported gap. → Fix: re-score per target embodiment (question 5) before reporting any cross-generator number; state which embodiment each number is calibrated for.
> - A single dominant sub-score could be mistaken for the whole filter's contribution. → Fix: report the per-component breakdown (question 6) alongside the aggregate gap, not just the aggregate.

## C: WAM Action-Space Completeness
*Every direction in A and B treats the imagined state as something to represent better or check harder, neither cluster asks whether the WAM's action space is complete. C1 asks what happens when the checking machinery itself flags an ambiguity no amount of training-time checking can resolve, and only a real action taken for its information value alone can close.*

### C1: Calibration-Triggered Epistemic Probing
> [!abstract] The bet
> Give a WAM a third action category: a brief, targeted probe taken purely to collapse an ambiguity the WAM's own calibration signal flags as unresolvable from imagination alone, then return to the task. When the checking signal (ρ, or forward-inverse divergence) exceeds threshold on a task-relevant hidden variable, insert one disambiguating action before resuming, beating a matched WAM that only checks/filters/retries by ≥15 pp real-task success on a high-ambiguity stratum (occluded content, ambiguous friction, sub-mm peg-hole offset), at ≤2 extra real timesteps, with no change on a low-ambiguity control where the probe never fires.

**Why**: every WAM in this doc's corpus trains on demonstrations, human teleop, scripted plans, RL rollouts scored on task return, where every recorded action serves the labeled goal. A teleoperator's disambiguating micro-move folds indistinguishably into the demonstration, so the field's tooling cannot represent a "probe for information" category at all. The closest existing WAM, ICWM, has an active probing phase, but its own ablation finds no probing strategy dominates, it resolves a fixed camera/gripper setup constant across the whole deployment, not a per-episode hidden fact, and it never fires again once the task starts. WAV, the doc's own calibration anchor, considered and explicitly rejected an info-seeking-exploration design as unreliable, building a purely statistical checker instead. Meanwhile a mature separate research culture (active inference, interactive perception, information-seeking RL) already proves the general mechanism, explore then switch to execution, works on real hardware (Poke and Strike: real KUKA arm, 8 of 9 and 8 of 10 successes; DISaM: beats every baseline on five sim and real tasks), and a value-of-information framework already proves the exact trigger logic, fire a probe only when a formal signal crosses a threshold, cuts probing actions by 85% versus generic-uncertainty triggering (VoNI). None of it is wired to a WAM's own imagined-rollout checking signal.

**First-principles**: *Principle:* some facts aren't in the picture no matter how well it's checked, only a real touch produces the missing evidence, and "act for information" is a well-posed goal distinct from "act for reward," a decades-old idea (expected free energy) the field never plugged into a modern WAM. *Challenged:* every WAM here assumes its action space is exhaustively task-progressing, checking machinery only ever computes on data already collected, never goes and gets new data. *Wager:* wiring the WAM's own checking signal to a single well-timed probe clears the ≥15 pp bar where checking alone plateaus, and closes without the probe on the easy cases where it never fires.

**Sharpest questions**: 1) Does a checking-triggered single probe beat a matched no-probe WAM by ≥15 pp on genuinely ambiguous cases, at ≤2 extra steps, with zero cost on easy cases? 2) Is "sensor always on vs predict from vision" a false choice, does a touch-on-demand third option match the always-sensored ceiling using the sensor a fraction of the time? 3) Is act-time checking a genuine third pole beyond train-time-vs-runtime, does it close a gap that neither leftover approach can close alone? 4) Does searching harder *inside* imagination (StressDream-style) substitute for a real probe, or does only the real probe move the needle? 5) Does the same fire-a-probe-then-resume trick work across different kinds of ambiguity, occlusion, friction, geometric offset, or is it a one-trick fix for one sense? 6) Trigger choice depends on the kind of not-knowing: does the WAM's own checking signal match a hand-built uncertainty proxy (DISaM's) on missing-information cases like occlusion, but miss more than half of what that proxy catches when the real system crosses a friction or dynamics regime it was never trained on, because a single model's own consistency check can stay flat exactly where the real system fails?

> [!warning] Risks
> - The result could go either way, checking alone might already close the gap on the chosen test cases. → Fix: pick the hard test cases before running the experiment, not after, so they aren't cherry-picked to guarantee a win.
> - Every standard benchmark scores extra probing steps as pure overhead, so the bet can look like a regression on the suites this doc otherwise trusts. → Fix: score at matched total budget (task steps plus probe steps), and report probing cost as its own number, separate from task success.
> - A probe that looks like it worked might not have resolved anything. → Fix: check whether the ambiguity signal actually dropped after the probe, not just whether the task later succeeded.
> - A badly-aimed probe can make things worse, touching the wrong thing, or a wiggle that ruins an already-good grip. → Fix: restrict probes to a safe, pre-approved set of touches rather than letting the policy invent one.
> - The checking signal can only see what the imagining model itself already sees, so it can't catch the one failure that matters most: being smoothly, confidently wrong. On a friction or dynamics regime the WAM was never trained on, the checking signal can stay flat exactly when it should fire, while the real system's behavior collapses. → Fix: don't treat occlusion, friction, and offset as interchangeable test cases; the checking signal is a plausible trigger for missing-information cases, but its reliability on confidently-wrong regime-shift cases isn't assumed, question 6 tests it directly.
