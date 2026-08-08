---
title: "TL;DR: Promising Research Directions: VLA × WAM × Embodied AI"
aliases:
  - "Embodied-AI TL;DR"
  - "Embodied-AI skim"
tags:
  - tldr
  - research-directions
  - VLA
  - WAM
  - embodied-AI
  - self-evolving
---

# TL;DR: Promising Research Directions: VLA × WAM × Embodied AI

> [!info] What this is
> A quick read of [[Embodied-AI|Promising Research Directions: VLA × WAM × Embodied AI]]. Each direction gives four things: the bet, the reasoning, the sharpest open questions, the risks. Plain-language version: [[__ELI5-EN__/Embodied-AI-ELI5|ELI5]].

> [!abstract] Overview
> Every robot body runs on the *same* core parts: a training goal, a way to test it, a memory loop, a way to move and pass skill across bodies. But people build these per body and per pipeline stage, throwing away the shared structure the data already holds. This umbrella doc covers **11 directions across 4 clusters**. The shared non-consensus bet: don't strip out load-bearing structure; that beats collecting more data. Predict the joint $p(o',a)$ in one loop, measure imagination and action on one causal axis, keep the control-relevant future in latent, keep the body-invariant intent. Cluster D pushes the same discipline upstream, to pretraining: run the head-to-head the field has skipped on which human-to-robot bridging mechanism actually wins and under what regime (D1), and attribute an unablated co-training recipe's gain to its real cause instead of assuming it (D2).

## Cluster map
| Cluster | Directions | Shared bottleneck |
|---|---|---|
| A: Architecture & Training | A1–A3 | Training goals don't match the causal structure of physical reasoning: they cascade, supervise only outcomes, or trust empirical losses off-distribution |
| B: Evaluation, Robustness & Deployment | B1–B4 | The lab-to-real gap: no joint metric, no recovery loop, a 3–5 Hz ceiling, forgetting after every fine-tune |
| C: Mobility & Embodiment Generalization | C1–C2 | Policies assume a fixed base and body. Drift breaks one; 0% extrapolation across body shapes breaks the other |
| D: Egocentric & Human-Video Pretraining | D1–D2 | No controlled comparison exists across human-to-robot bridging mechanisms, or across egocentric+video-WAM co-training's candidate causes: every paper validates its own choice against a no-transfer or unablated baseline, never a sibling mechanism or a data-matched control |

## A: Architecture & Training: How the Model Learns
*Match training goals to the causal structure of physical reasoning: don't cascade WM and policy (A1), don't supervise reasoning on outcomes alone (A2), don't trust empirical losses off-distribution where physics is checkable (A3).*

> [!tip] Cluster-A gate: synergy is a gate, not a given
> The claim that A1's latent-consistency reward, A2's causal-importance step weight, and A3's physics-predicate loss co-train cooperatively on one shared latent is *asserted, not tested*: A3's predicates live in world coordinates while A1/A2's signals live on latent tokens, so A3's loss may not even back-propagate into the same latent. Run the three-loss interference probe (H7) first. If the losses cooperate, Cluster A is one synergistic mechanism; if they gradient-conflict or one dominates, it is three sibling papers on a common diagnosis ("dense local signal on a latent substrate beats sparse outcome"), and each direction is defended on its own falsifier, not as a stacked system.

### A1: Single-Loop Co-Evolving Policy + World Model in Latent Space
> [!abstract] The bet
> One backward pass over a *shared latent* backbone beats *phased/iterative* co-evolution (World-VLA-Loop-style) on *both* in-distribution SR (≥97.2% LIBERO) and OOD SR (≥79.5% LIBERO-Plus), at no extra latency (latent ~10 ms vs pixel ~150 ms), and survives the CoLA-World collapse without warm-up. But MoLA (92.7%, cascaded imagine-then-act) and World-Pilot (84.7%, frozen-WM-prior latent) already clear that 79.5% OOD point, so the real win is the OOD-SR-*at-matched-latency* Pareto against those baselines, not a single OOD number, reported with an MDE (binomial SE ≈ ±2–4 pp at ~500 episodes) so a sub-MDE gap reads as a tie.

**Why**: Each future observation pairs with the action that caused it, so $p(o',a\mid o,l)$ is one joint distribution warranting one joint loss; the standard recipe cascades or alternates the two. Co-evolution wins offline (MMaDA-VLA 98.0% LIBERO; ACT-JEPA +53.7% over AR policies) but only in pixel space, phased, CoLA-World shows one-stage training collapses the codebook.

**First-principles**: *Principle:* WM and policy are two halves of one distribution. *Challenged:* CoLA-World's no-warm-up collapse. *Wager:* one cooperative gradient, EMA targets plus LeJEPA regularization.

**Sharpest questions**: 1) Does a single latent joint gradient beat phased pixel co-evolution and alternation on *both* SR axes at equal latency? 2) Does a latent-consistency reward ($\hat z_{t+1}$ vs encoder $z_{t+1}$) give the dense per-step signal outcome reward lacks? 3) Does the in-loop WM widen the OOD margin over a frozen-WM (WMPO) loop?

> [!warning] Risks
> - Optimization instability across discrete action head, continuous latent, adversarial finder → separate loss weights, EMA targets; frozen WM first.
> - Representational collapse on latent consistency (CoLA-World) → LeJEPA's anti-collapse regularization.
> - The ≥79.5% OOD target is already beaten by two cited baselines (MoLA 92.7%, World-Pilot 84.7%), and in-dist LIBERO is saturated (~98%) so it has near-zero discriminative power → re-target to the OOD-SR-at-latency Pareto, not a headline OOD point, and power the comparison with an MDE so a sub-MDE gap isn't read as a loss.

### A2: Causally-Important Step Rewards for Latent Policy Reasoning
> [!abstract] The bet
> The durable, primary contribution is the **LIBERO-Subgoals benchmark** (130 tasks, 3–7 κ>0.7-validated verifiable subgoals each, scored per subgoal), on which latent CoT plus a learned step reward gets ≥+5 pp SR on LIBERO-Long at matched latency and ≥+10 pp on compositional benchmarks over outcome-only RL, closing the faithfulness gap SEAL documented (its **+15 pp** to 53% novel-behavior composition is the bar). The *secondary* wager, and the thinner one, is that the learned causal-importance weight itself beats uniform latent-trajectory credit (RLTT's scheme) specifically on a robot policy: on LLM math, uniform credit already sits close to the causal-importance ceiling, so the embodied margin has to be larger to matter.

**Why**: An outcome reward scores a causally-correct trace the same as a lucky one: RL-trained traces become "factually correct via causally disconnected paths" (CIR/SR Reasoning), and RoboSemanticBench finds **89.93%** of grasp-success/task-failure cases reasoned correctly yet acted wrong. Challenged: that you must choose between latency-free latent CoT and step-level supervision, RLTT shows latent-process beats latent-outcome (+16.6% AIME24) but only for LLM math with *uniform* credit.

**First-principles**: *Principle:* reward must act on intermediate states, not the final one. *Challenged:* RLTT's uniform trajectory-level credit; explicit-CoT's per-token latency. *Wager:* a *learned causal-importance* step reward over latent steps.

**Sharpest questions**: 1) Does the LIBERO-Subgoals gain over outcome-only RL hold at answer-only latency (the primary claim), and does the causal-importance weight also beat RLTT's uniform credit (the secondary, thinner-margin claim)? 2) Are the latent tokens functionally *used* (Latent Utilization Index > 0.3 under step rewards, ~0 for outcome-only)? 3) Does it keep the gain at a fraction of explicit-CoT latency (~0 ms vs ECoT/EMMA-X ~1.2 s)?

> [!warning] Risks
> - Predicate scaling: hand-authored subgoals are brittle → validate auto-generated predicates against a κ > 0.7 gold set first.
> - Reward hacking (predicates satisfied trivially) → EVOL-RL novelty diversity plus the LUI probe.

### A3: Verifiable Physics-Consistent Training for Open-World Policy Generation
> [!abstract] The bet
> Verifiable physics-*law* predicates at the *action* level must out-extrapolate the strongest collision-geometry baseline, Neuro-Symbolic VLA Safety's in-generation trajectory-CBF (SafeLIBERO CAR **82.81%** / TSR **81.62%**), *and* PIPER's generic analytic-dynamics residual, on **OOD** Safe-SR: a CBF that satisfies collision geometry can still violate momentum, friction, and contact, exactly what the predicate set adds. They also beat FAN Prior's tolerance-geometry regularizer on OOD Safe-SR, and reach ≥0.70 sim-to-real SR retention (physics-naive: 0.50–0.60). Physical-Feasibility VLA's **43.50%** geometric-loss point is the mechanism-feasibility floor now, not the bar.

**Why**: Physical laws are checkable binary predicates, *independent of the training set*; policies instead trust empirical losses on seen samples only. ACWM-Phys measures the cliff: action-conditioned video WMs are crisp in-distribution (SSIM **0.988**) but degrade sharply OOD (ΔM-MSE up to **+40** robot-arm, **+30** cloth). Challenged: that a physics-respecting video generator gives a physics-respecting *policy* for free, and that *tolerance-geometry* (FAN Prior) equals physics *laws*.

**First-principles**: *Principle:* physics laws hold for held-out and OOD data alike. *Challenged:* FAN Prior's tolerance-geometry, Law-of-Task-Achieving-Body-Motion's symbolic-verifier bet. *Wager:* physics *laws* as a *differentiable* action-level loss.

**Sharpest questions**: 1) Do five binary predicates (momentum, no inter-object penetration, free-flight gravity, Newton's-3rd-law contact wrenches, Coulomb friction) as a differentiable loss lift Safe-SR past 55%, beat FAN Prior's tolerance-geometry on OOD, *and* out-extrapolate PIPER's generic dynamics-residual loss on the same OOD Safe-SR axis? 2) Is $\rho(\sum_i P_i,\ \text{task SR})$ clearly positive, is the imagination→action chain real? 3) Does it hold sim-to-real SR retention ≥0.70 where physics-naive policies lose it?

> [!warning] Risks
> - Verifiable physics scales poorly to cluttered scenes (PIRF) → start with ACWM-Phys's clean low-dimensional tasks.
> - Physics-consistent imagination ≠ physics-consistent action → H5's Pearson $\rho$ between $\sum P_i$ and SR is the go/no-go.
> - Reward hacking (frozen output) → static-output detection (σ drop > 2×) plus EVOL-RL novelty diversity.
> - "Physics-as-a-differentiable-loss" is already done generically: PIPER enforces a Lagrangian-consistency residual inside the actor's objective (+20–45% sample-efficiency) → pin the wedge to the *verifiable per-law predicate set*, not the loss mechanism, and test it head-to-head against PIPER's generic residual on OOD Safe-SR.
> - A stronger geometric-safety baseline now clears the SafeLIBERO obstacle bar: Neuro-Symbolic VLA Safety's trajectory-CBF hits 81.62% TSR / 82.81% CAR, far above the 43.50% anchor the old bet was stated against → re-state the target as out-extrapolating the CBF baseline with physics-*law* predicates on OOD Safe-SR, not merely clearing 55%.

## B: Evaluation, Robustness & Deployment: From Trained to Deployed
*Everything between a trained policy and deployment: measure whether imagination and action are causally bound (B1), recover with memory when it fails (B2), run in real time on edge (B3), don't forget under continual fine-tuning (B4).*

### B1: Joint Policy/World-Model Evaluation: Causal Consistency Between Imagination and Action
> [!abstract] The bet
> ASR plus COD over *action* counterfactuals *jointly* predict real-fleet SR at Pearson **ρ > 0.7**: far above the ρ < 0.4 ceiling of separate-axes evaluation, and above scene-counterfactual rubrics, which report no SR correlation. But a bare high ρ isn't the win: closed-loop correlations already run **0.79–0.99** across several WAM evaluators (one hits 0.989) and are overwritable by whoever has the GPUs. The actual deliverable is the causal-consistency metric *plus its validity wrapper*: an action-vs-scene negative control, an optimism-bias filter (MiraBench's paired action-counterfactual probes are the substrate), and cross-lab variance reduction.

**Why**: Current protocols score WM quality (FVD/PSNR) and action quality (SR) *separately*, so a joint model climbs each while the two stay causally disconnected; Objective-Mismatch MBRL shows predictive WM loss doesn't track downstream return. Challenged: the *action*-counterfactual link (vary $a'_t$, not a scene prompt) predicts real-fleet SR where fidelity and scene-counterfactual rubrics don't (WorldMark: fidelity and consistency unrelated; What-If World: looks-real overstates causal ability 52.2 pp).

**First-principles**: *Principle:* WM and policy are linked only when imagined-future actions match executed ones. *Challenged:* scene-counterfactual rubrics (What-If World never scores policy SR). *Wager:* varying the *action*, not the scene, bound to real-fleet SR.

**Sharpest questions**: 1) Does an action-counterfactual metric (sample $a'_t$, require $\|\hat s_{t+1}-\hat s'_{t+1}\|$ monotone in $\|a_t-a'_t\|$) beat FID *and* scene-counterfactual rubrics at predicting real SR? 2) Do ASR plus COD *together* clear ρ > 0.7 where separate L1/L2/L3 sub-scores stay below 0.4? 3) Does it expose shortcut-solvable benchmarks (a 0.09B DINOv2+MLP probe hits 99.0% LIBERO-Spatial)?

> [!warning] Risks
> - Metric noise from feature-space similarity → pair with A3's predicates; cross-validate against VISER's sim-real r = 0.92.
> - Counterfactual probes may need 100+ rollouts per task → use vla-eval's 47× speedup plus X4Val variance reduction.
> - Selection bias flattering current WAMs → include adversarial (JailWAM, VLA Patch Attack at 90.7% attack SR, BadWAM's imagination-preserving drift attack dropping closed-loop SR >50% while the imagined future stays plausible) and physics-violating baselines.
> - Optimism in the scoring model: if an LLM/VLM reward model scores the WAM's imagined success, it can systematically over-reward suboptimal behavior → calibrate any reward-model judge with dense per-timestep failure labels before trusting its success scores, and prefer the action-counterfactual metric over an LLM-judged-success surrogate.

### B2: Long-Horizon Memory + Failure Recovery Loops for Real-World Deployment
> [!abstract] The bet
> The safe core comes first: **cause-attributed recovery beats uniform rollback** (the GTP-FA **11.2→76.8%** real-Franka attribution gain), and it stands on its own. The higher-variance extension is the cross-episode-memory face: a trained-VLA loop carrying failure memory across episodes lifts SR on RoboMemArena's repeated-failure subtasks by ≥+5 pp over HELM's episode-local loop (baseline: HELM's +23.1 pp LIBERO-Long). State-machine integration cuts oscillation incidents ≥50%.

**Why**: HELM wires episodic memory, memory-conditioned detection, and recovery into one frozen-VLA loop (+23.1 pp LIBERO-Long), but it is *episode-local* (most-recent checkpoint only) and *cause-blind* (uniform rollback). The lowest-risk win is just fixing the cause-blindness, diagnosis-then-recovery, which GTP-FA already shows on real hardware. RoboMemArena shows 68.9% of subtasks need historical info, which motivates the riskier cross-episode extension. Challenged: HELM bets episode-local memory plus uniform rollback suffices; UniManip and SOMA bet a within-episode LLM orchestrator does (SOMA even supplies cause-*typed* attribution, but in-context, not a cross-episode trained-policy memory, so the trained-VLA cross-episode wedge survives).

**First-principles**: *Principle:* cause-blind recovery oscillates (the safe core); episode-local memory can't recognize recurrence (the extension). *Challenged:* HELM's uniform-rollback loop; UniManip's / SOMA's within-episode LLM orchestration. *Wager:* diagnosis-conditioned recovery first, then a *trained* VLA carrying cross-episode failure memory.

**Sharpest questions**: 1) Does GTP-FA-style grasp-vs-planning attribution beat uniform rollback at matched detection (the safe core)? 2) Does cross-episode memory recognize recurrence (≥+5 pp on repeated-failure subtasks, higher strategy-switch rate on the second encounter) where HELM re-fails identically? 3) Does state-machine integration cut oscillation incidents ≥50% without SR loss?

> [!warning] Risks
> - Composed-budget latency gate: cross-episode retrieval, the diagnosis model, and the recovery state machine each cost time, and only their *sum* against B3's 3–5 Hz ceiling decides deployability, a per-component "fast enough" can still blow the composed budget → budget the three components together per step, invoke recovery only when the verifier fires, compress memory to per-failure-signature keys (HELM's CLIP-indexed store).
> - Calibration-under-drift of the recurrence key: the cross-episode "have I failed this way before?" match is only as good as its failure-signature key, which can drift under pose / lighting / background change, silently mis-firing (false matches trigger the wrong cached fix; missed matches lose the recurrence) → instrument the signature-matcher's calibration under a perturbed-episode replay, and gate the cross-episode-memory SR claim on the matcher staying calibrated, not just on clean-replay recurrence.
> - Undiagnosed-loop oscillation → diagnosis-gated state-machine transitions (the ≥50% reduction the bet measures).
> - Memory as attack surface (poisoning amplified across episodes) → gate cross-episode writes behind a recovery-success check; treat the buffer as untrusted.

### B3: Real-Time-Deployable Policies via Architectural-Algorithmic-Data Co-design
> [!abstract] The bet
> On an *un-saturated contact-rich OOD* bench, the primary deliverable is a **drift-calibrated embodied-efficiency frontier**: SR *and* embodied smoothness (jerk-L2 / path-length / SPARC), re-scored under LIBERO-Plus-style perturbation, at ≥95% base-policy SR on edge (Jetson Orin / Apple M). This matters because a lever can hold SR in-distribution while ringing the contact-rich loop: compression (weight-prune / quant) holds SR within −2.7% yet adds +19.5% jerk, a degradation an SR-and-Hz-only frontier can't detect. The *secondary*, likely-non-transferable wager is that a matched-FLOPs Pareto sweep across architecture × decoding × precision × data finds a *composed* point that beats the best single lever (VOTE's edge throughput at ≥95% SR) on the plain SR-vs-frequency frontier, plus a stated law for *when* composing wins. The 95% bar is a design-chosen target, not a paper-reported figure.

**Why**: A contact-rich policy is a feedback loop with a Nyquist *stability* floor: contacts ringing at tens of Hz can't be stabilized by a 3–5 Hz loop. Challenged: the *cross-lever composition law*, composing the four levers beats the best single lever, with a predictable rule for when. VOTE at 38.6× and Fast-Slow WB VLA at 32.3 Hz clear the floor with one or two levers; single-lever winners (VOTE, VLA-Adapter at 219.2 Hz) bet one lever suffices everywhere.

**First-principles**: *Principle:* Nyquist says a loop must run ~2× faster than the fastest motion it controls. *Challenged:* the single-lever-suffices bet (VOTE, VLA-Adapter). *Wager:* a composed four-lever point Pareto-dominates the best single lever.

**Sharpest questions**: 1) Does the sweep find a composed point that *dominates* (not just matches) VOTE on the SR-vs-Hz frontier, with a rule for when composing wins? 2) Do linear-time backbones (Mamba) hold ≥95% SR at >30 Hz only with knowledge-insulated RL? 3) Does the edge chain (train → quantize → distill → deploy) lose ≤5% SR per stage, cross-lab via VLA-REPLICA?

> [!warning] Risks
> - Linear-attn / Mamba may underperform Transformers on long-context policies → gate every Pareto point on an SR-retention threshold.
> - Edge-hardware diversity (Jetson vs Apple M vs NPUs) → validate cross-platform via VLA-REPLICA, not a single device.
> - Saturation if "Mamba + LoRA + co-training" becomes the dominant recipe → frame the deliverable as the Pareto curve plus law.
> - Calibration-under-drift of every Pareto point: quantization / pruning / token-skipping degrade *non-uniformly* under OOD drift, so a clean-bench frontier mis-states deployed quality → re-score every reported point under LIBERO-Plus-style perturbation (SR *and* jerk-L2 / path-length); a point only counts if it holds SR-and-smoothness under drift.
> - Composed-budget gate when B3 pairs with B2's memory loop or C1's dream head: the control-rate gate is the *sum* of all per-step components, not the policy's inference alone → profile the composed loop as one budget against the 3–5 Hz ceiling.

### B4: Continual Policy Learning Without Catastrophic Forgetting
> [!abstract] The bet
> The durable deliverable is the **policy-overlap-matrix diagnostic**, and it must hold on *two* streams, not one: an **orthogonal** stream (a diverse LIBERO sequence where overlap stays below ~0.3 and principal-angle $\cos^2\theta_{\min}$ predicts forgetting at r > 0.5) *and* a **correlated** stream, repeated re-fine-tunes of one skill family (the realistic deployment case where B2's recovery updates keep hitting the same skill), where overlap is high and the law's prediction must still hold. Protecting that single shared subspace then matches per-task-expansion retention (CLARE's near-zero NBT) at a *flat* parameter budget, holds the embodiment tax <5% (UAM), and keeps new-task SR within −3 pp of full fine-tune. So forgetting is geometry, not storage.

**Why**: A fielded policy is fine-tuned again and again (new objects, B2's corrections), and every one erodes prior skill. Challenged: a *single protected shared subspace* beats *per-task adapter expansion* on policies, i.e. the Geometric Forgetting Law (r=0.994 on Split-CIFAR100/GLUE, never on policies) transfers. CLARE/CORAL go replay-free but bet expansion is necessary; Shared LoRA Subspaces bets a unified subspace suffices, proven only for LLMs.

**First-principles**: *Principle:* a large policy has far more weights than any one skill needs, so forgetting happens only on the small overlap of shared directions. *Challenged:* CLARE/CORAL's per-task expansion and replay-as-default. *Wager:* the law transfers, so one protected subspace matches expansion at flat budget.

**Sharpest questions**: 1) Does the Geometric Forgetting Law hold on policies on *both* streams, the orthogonal one (overlap below 0.3, r > 0.5) *and* the correlated one (high overlap from repeated re-fine-tunes of one skill family, where the law must still predict forgetting)? 2) Does one protected shared subspace match CLARE's retention *without* growing parameters per task, beyond what SPREAD's flat-budget whole-subspace alignment already achieves on policies (LIBERO NBT 9.0% vs M2Distill 20.0%), i.e. does choosing *which* directions to protect by overlap add anything over aligning the whole dominant subspace? 3) Does subspace protection stop B2's recovery updates from erasing base skills (old-task SR within −3 pp over 100 updates)?

> [!warning] Risks
> - Subspaces may not be disjoint for *similar* tasks (shared contact dynamics) → H1's overlap matrix is the go/no-go; if overlap >0.5 dominates, fall back to memory (ECHO-VLA).
> - Plasticity collapse (too many protected directions freeze new-task learning) → bound protection by the ≤−3 pp new-task-SR target.
> - Replay quietly wins at scale (cheap storage, no privacy) → frame the deliverable as the storage-vs-retention Pareto; claim *dominance on both axes*.

## C: Mobility & Embodiment Generalization: Moving and Transferring
*Two directions fail the same way: they strip out load-bearing structure, the world's layout (C1) and the body's morphology (C2). Keep the right invariant and the fixed-base and fixed-body assumptions stop breaking.*

### C1: Latent In-Policy Dreaming for Vision-and-Language Navigation
> [!abstract] The bet
> A fused in-policy latent dream head plus online self-evolution matches or beats external-WM and single-mechanism VLN: ≥62.0% SR / 58.0% SPL on R2R-CE Val-Unseen at ≤130 ms / 22.8 GB (LatentPilot). It adds ≥+4.1% online-adaptation SR (NavMorph), and beats Dream-to-Recall's memory-fusion-without-evolution at the same budget. A non-dreaming hierarchical generalist (ABot-N1) has since reached 70.9% SR on the same split, above LatentPilot's own number, so the bet is now the *cost* Pareto, SR at a given latency and memory budget, not the SR ceiling alone.

**Why**: A navigation decision needs only the *control-relevant* slice of the future; an external pixel-WM adds compounding prediction error, memory, and latency. In-policy latent foresight already beats external pixel-WMs (LatentPilot, MonoDream, Cross-from-Left-to-Right-Brain). Challenged: *fusing* it with online self-evolution beats either alone, and beats imagination+memory without self-evolution (Dream-to-Recall). NavMorph bets self-evolution alone; Memoir bets imagination+memory alone.

**First-principles**: *Principle:* the control-relevant future slice is low-dimensional and lives in a latent token; rendering pixels wastes compute. *Challenged:* NavMorph (self-evolution alone), Dream-to-Recall (imagination+memory alone). *Wager:* fusing dreaming plus self-evolution within the latency budget.

**Sharpest questions**: 1) Does bolting NavMorph's Contextual Evolution Memory onto LatentPilot's Pilot Token stay ≤130 ms while gaining +4.1% online SR *and* beating Memoir on unseen splits? 2) Does latent foresight saturate at a shallow dream horizon while latency keeps rising? 3) Does LatentPilot's privileged future-obs supervision transfer sim→real (VLN-PE Fall/Stuck)?

> [!warning] Risks
> - Latent dreaming may plateau on long-horizon RxR-CE where explicit reasoning (AwareVLN) wins → H4's head-to-head bounds the claim.
> - A non-dreaming generalist (ABot-N1, 70.9% SR via scale + hierarchical slow-fast decomposition + multi-task RL) now beats the dreaming anchor's own headline SR number → re-run H1/H4 with it as an added no-dreaming baseline at matched parameters, and report its latency/GB footprint before conceding the frontier.
> - Online self-evolution can drift (CEM adapting to a misleading episode) → gate CEM writes behind a confidence check; borrow B4's protection.
> - Sim-only privileged supervision (PilotLoop's future-obs exists only in sim) → validate VLN-PE transfer first; fall back to NavMorph's unsupervised CEM.

### C2: Morphology-Invariant Action Representations for Cross-Embodiment Zero-Shot Transfer
> [!abstract] The bet
> In a head-to-head bake-off, at least one intent-grounded invariant reaches >30% zero-shot SR on AnyBody's arm-extrapolation split (current best: **0%**). This fits LAP's **>50%** zero-shot and GET's **20%** zero-shot to unseen graph structure. It turns extrapolation into a measurable transfer rate, and names which invariant carries it.

**Why**: "Pick up the cup" is the same intent for a 7-DoF arm, a gripper, or a humanoid hand, but a *joint-space* tokenizer ties it to one body plan. AnyBody is the brutal diagnostic: multi-embodiment policies match single-embodiment baselines on seen robots and interpolation, but collapse to **0%** SR on extrapolation across very different link structures. But that 0% is one paper's baseline number, and AnyBody's reported 0% may be an *architecture artifact* (an under-tuned multi-embodiment head), not a property of joint-space tokenization, so before it can anchor a "law" you must reproduce it under a *properly-tuned* baseline, in order: a **sim-RL-tuned joint-space control first**, then the **interpolation control second**. Candidates differ only in *which intermediate they make invariant* (language, latent goal, pointmap, phase, kinematic graph). Cross-family transfer without per-robot fine-tuning is done (MetaMorph 2022, GET 2024); the open question is *which* invariant survives the arm-extrapolation split, measured against the *tuned* baseline, not the reported 0%.

**First-principles**: *Principle:* task intent is morphology-invariant while the joint-space trajectory is morphology-specific. *Challenged:* native-joint tokenization (HPT stems, RT-1), and each candidate (LAP, Demo-JEPA, GET) betting its own untested intermediate. *Wager:* a bake-off names which intent-grounded invariant breaks the 0% wall.

**Sharpest questions**: 1) In a bake-off of LAP (language), Demo-JEPA (latent goal), GET-style kinematic-graph, and task-space tokenization on AnyBody, does at least one exceed 30% where joint-space scores 0%, and which ranks highest? 2) Is joint-space failure memorization, not control learning (low cross-morphology overlap in HPT-style stems)? 3) Is the invariance tax on precision bounded on *seen* robots?

> [!warning] Risks
> - Invariance may cost precision (language/latent action space blurs fine-grained control) → H4 bounds the invariance tax on seen robots first; report the precision floor.
> - AnyBody's 0% may be partly task-hardness or an architecture artifact, not pure morphology → run two ordered controls: a sim-RL-tuned joint-space baseline at matched budget *first* (if it rises above 0%, the wall was under-tuning), then interpolation SR on the *same* tasks; attribute the gap to morphology only if the tuned baseline still scores ~0% and interpolation succeeds. Report the *tuned* baseline as the real wall, not AnyBody's reported 0%.
> - Language-actions discretize continuous control (LAP loses high-frequency detail) → pair the language intermediate with a knowledge-insulated continuous action expert.
> - The win may be data, not representation: physics-accurate cross-embodiment data augmentation alone (OXE-AugE) already lifts unseen-config SR (OpenVLA +24%, π0 +45%) with no new invariant → add a data-scaled joint-space control to the bake-off; the invariant only wins if it beats data-scaling on the *extrapolation* split, not just on seen/interpolation configs.

## D: Egocentric & Human-Video Pretraining: Learning Before the Robot Body Exists
*The same refusal, pushed upstream of the robot body entirely: don't factor away the kinematic structure a human hand carries across the human-to-robot hop (D1), and don't cascade the pretraining objective into two separate stages when a coupled loop might carry a synergy neither stage alone can (D2).*

### D1: Regime-Contingent Bridging Mechanisms for Human-to-Robot Skill Transfer
> [!abstract] The bet
> Sweeping six human-to-robot bridging mechanisms (explicit projection, learned-gap co-training, mid-training alignment, embodiment-agnostic intermediate representation, visual embodiment-gap editing, generative video transfer) at matched egocentric-hours on a shared two-tier harness (parallel-jaw + dexterous hand), no single mechanism's SR margin over the second-best exceeds a pre-registered **10 pp** in every cell (precision × OOD-scene × platform-tier). More specifically: explicit projection (Being-H0-style) wins the dexterous-tier precision-critical cell while learned-gap co-training (π0.5-+-ego-style) wins the parallel-jaw OOD-scene cell, a regime split, not a universal winner. Zero-robot-data instances (VidBot, ZeroMimic, Phantom) pay a bounded precision tax versus co-trained Being-H0 at matched mechanism.

**Why**: A human hand's 22+ DoF has to become a robot gripper's 1–7 DoF somewhere in the pipeline, and the field has converged on six distinct places to put that conversion, yet every method paper reports a win only against a no-transfer or unaligned baseline, never against a sibling mechanism trained on the same data. Each family shows a real number in isolation: Being-H0's explicit MANO tokenization matches 50–100%-data baselines with only **25%** as much teleop data; π0.5-+-ego's learned-gap co-training lifts egg-sorting **57%→78%**; EgoScale's mid-training alignment adds **+54%** SR on a 22-DoF hand; Phantom's visual embodiment-gap editing hits **92%** Pick/Place with zero robot data. None has ever run against another on the same task or platform. EgoWAM already proves the controlled-sweep move works within one family (DINO wins OOD, 3D-flow wins in-domain); D1 ports that exact methodology across the six families.

**First-principles**: *Principle:* the kinematic gap between a human hand and a robot end-effector is conserved information, it relocates, it does not disappear; where in the pipeline it relocates trades off precision, data-efficiency, and OOD-robustness differently. *Challenged:* EgoScale's own claim that human motion supplies a "robust, embodiment-agnostic motor prior" (in tension with its own ablation, where a wrist-only projection performed poorly) and π0.5-+-ego's claim that transfer is an emergent property of data scale, neither tests the mechanism-choice question directly against a sibling mechanism on the same tasks. *Wager:* a shared harness with two platform tiers and a precision-vs-OOD task split surfaces a regime-contingent winner, not a universal one.

**Sharpest questions**: 1) Does no mechanism's SR margin over the second-best exceed 10 pp in every cell, or does one mechanism win every cell and refute regime-contingency outright? 2) Does explicit projection win the dexterous-tier precision cell while learned-gap co-training wins the parallel-jaw OOD cell, or does one mechanism win both? 3) Do zero-robot-data instances (VidBot, ZeroMimic, Phantom) pay only a bounded precision tax against co-trained Being-H0 at matched mechanism, or does the tax collapse toward total precision loss?

> [!warning] Risks
> - Re-implementing six mechanisms faithfully is a large engineering surface, and a weak arm fakes regime-contingency → reproduce each mechanism against its own paper's reported number first (Being-H0's 99.8–100% valid generation, π0.5-+-ego's 78% egg-sorting, Phantom's 92% Pick/Place) as an arm-validity gate.
> - Collapsing to a single parallel-jaw platform silently strips the finger-level mechanism the precision-cell claim predicts wins → run two platform tiers (parallel-jaw and dexterous hand) and scope the precision-cell claim to the dexterous tier explicitly.
> - Three of six arms (learned gap, mid-training, generative video transfer) are thin on independent instances → report per-cell margins only for arms with ≥2 verified instances.

### D2: Objective-Coupling vs. Data-Volume Attribution in Egocentric + Video-WAM Co-Training
> [!abstract] The bet
> At matched total compute (mirroring HumanScale's controlled 5,000-hr protocol), joint egocentric-VLA + video-WAM co-training at $N$ hours beats a single-objective egocentric-VLA baseline trained on $2N$ hours (the actually compute-matched data-volume control) by **≥5 pp** downstream SR on held-out tasks, meaning the gain is objective-coupling, not data volume alone. Within that coupling, the advantage is **≥2×** larger on a genuinely novel-dynamics held-out split than on an in-distribution held-out split, consistent with a shared-dynamics-prior mechanism rather than pure representation-alignment.

**Why**: π0.7 pretrains on egocentric human video and a video-WAM subgoal-image objective as parallel signals on overlapping corpora, and reports the recipe works, but never isolates why: is the gain the extra training signal, or just the extra data tokens riding along with it? JoyAI-RA sharpens the question from the other side: it pretrains on the same class of egocentric video with no WAM objective anywhere in its architecture, and still reaches a strong recipe (**90.48%/89.28%** RoboTwin 2.0 Easy/Hard), a no-WAM control case that argues against the premise, not for it. Fast-WAM comes closest to an ablation: removing video co-training drops RoboTwin **91.8%→83.8%**, but it removes the objective and its tokens together, so the drop could be either cause. HumanScale runs the controlled-compute protocol D2 needs, but for a different question (egocentric vs. robot video as a pretraining source, not objective-coupling vs. data-volume as a mechanism). Being-H0.7 shows the synergy, if it exists, doesn't need pixel-space video at all: a latent dual-branch target matches or beats pixel-WAM baselines at **99.2%** LIBERO and **3–4 ms/step**.

**First-principles**: *Principle:* a video-WAM's pixel-future-prediction objective and an egocentric-VLA's hand-action-prediction objective are two loss functions computed over overlapping footage of the same underlying process, coupling them in one joint optimization, rather than cascading pretraining into a video-prediction stage and a separate action-prediction stage, should let each objective's gradient inform the other's representation, a synergy a data-volume-matched single objective can't reach by adding capacity alone. *Challenged:* π0.7's own framing treats the recipe's non-degradation as sufficient evidence the WAM objective is pulling its weight, but never tests whether the same token budget, spent doubling a single objective's data with no WAM component at all, would get equally far; JoyAI-RA is the closest existing missing-control in the wild, and it undercuts rather than confirms the "coupling is what's carrying it" reading. *Wager:* a 3-arm compute-matched comparison (single-$N$, single-$2N$, joint-$N$) isolates coupling from volume.

**Sharpest questions**: 1) Does joint-$N$ beat single-$2N$ (the actually compute-matched control, not just single-$N$) by ≥5 pp downstream SR, or does single-$2N$ tie or beat it, meaning the reported co-training gain was compute, not coupling? 2) Does a volume-matched control (replacing Fast-WAM's removed video objective with more robot-action-only training on the same tokens) recover a meaningful fraction of the 91.8%→83.8% gap? 3) Does swapping the pixel-space WAM target for a Being-H0.7-style latent dual-branch target recover ≥80% of the full pixel-WAM co-training's gain?

> [!warning] Risks
> - A volume-matched control for Fast-WAM's ablation isn't a perfectly clean control: even matching token count, the extra robot-only steps use tokens differently than the removed objective did → report the recovered-gap fraction with confidence intervals, treat partial recovery as evidence both mechanisms contribute rather than forcing a binary verdict.
> - Latent (Being-H0.7) and pixel (DreamZero) WAM targets aren't apples-to-apples architectures, a Mixture-of-Transformers dual-branch vs. a full video-diffusion backbone, risking a confound between "latent vs. pixel" and "architecture family" → implement both targets on the same backbone, swapping only the prediction head/target, the way EgoWAM already does for its own 3-way target sweep.
> - The dynamics-shift split needs a genuinely novel contact mode, not just a novel object texture, or the "shift" is cosmetic → borrow LIBERO-Plus's OOD-perturbation taxonomy (physical, not just visual, perturbations) to construct the split.
