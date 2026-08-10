---
title: Curvature-Conditioned Exploration for Distributional Critics
tags:
  - project
  - active
  - reinforcement-learning
  - flashsac
  - exploration
aliases:
  - Curvature-Conditioned Exploration
  - Beating FlashSAC
---

# Curvature-Conditioned Exploration for Distributional Critics

> [!abstract] Thesis
> Off-policy actor-critic's exploration shape has the irreducible truth that the critic already computes the local geometry that tells you where to explore — its action-space curvature — which breaks the field's assumption (FlashSAC included) that per-dimension exploration variance can be left to a free-form learned head shaped only by the policy loss, and I bet that conditioning exploration covariance on the critic's own action-Hessian beats FlashSAC on both wall-clock (matched Appendix A protocol) and final return on the tasks where that curvature is sharpest (dexterous manipulation), while costing nothing extra on the tasks where it's flat (locomotion) — a prediction directly falsifiable against FlashSAC's own published capacity-scaling asymmetry (+32.9% Allegro, +0.1% G1-flat).

**Anchor:** [[2604.04539|FlashSAC]] (Fast and Stable Off-Policy RL for High-Dimensional Robot Control). **Required foil:** [[2603.12612|FastDSAC (DEM)]] — nearest published rival mechanism, not a reason to change the anchor.

---

## Background — what FlashSAC's own data already says

Verified directly against FlashSAC's released repo (`github.com/holiday-robot/FlashSAC`) and its own result CSVs, not against claims in the paper text.

- **Capacity benefit is task-asymmetric.** 4× critic width, same run family (terminal step 50,000,896, seeds 0/1000/2000/3000/4000): Allegro (16-DoF) **+32.9%**, Shadow (20-DoF) **+15.8%**, G1-rough (37-DoF) +5.2%, G1-flat (37-DoF) **+0.1%**. Action dimension is *anti-correlated* with capacity need — dexterous hands, not the highest-DoF task, benefit most.
- **The ordered-additive ablation is non-monotone.** Normalized aggregate score: MLP 0.3011 → +Residual 0.4711 → +BatchNorm 0.4141 (−0.057) → +RMSNorm 0.6654 → +DistCritic 1.0008 → +WeightNorm 1.0000 (−0.0008). WeightNorm is measurably **inert on srank/dormant-neuron/feature-magnitude**: srank 951.4→951.8, dormant-neuron rate 0→0, feature magnitude 0.539→0.499. *Caveat added after verifying [[2509.25174|XQC]] directly:* WN's actually-claimed mechanism (Van Laarhoven 2017, cited by XQC) is keeping the **effective learning rate constant**, not these three diagnostics — this finding is real but doesn't refute WN's own stated purpose, only that it's inert on the diagnostics checked. BatchNorm, despite the score dip, is mechanistically load-bearing: dormant neurons 0.417→0, srank 214→848 on G1-flat.
- **The condition-number monotonicity claim in the paper text is false in their own logs.** Monotone decrease on 1 of 4 tasks; minimum reached *at* full FlashSAC on only 2 of 4; WeightNorm raises the condition number 4–14× on G1-flat.
- **Exploration is per-dimension and state-dependent, but curvature-blind.** `NormalTanhPolicy` (`layer.py`) computes `log_std` per action dimension from a learned linear head, bounded to `[log_std_min=-10, log_std_max=2]` via a tanh squash — shaped only by backprop through the Q-maximization actor loss. The **total** entropy budget is separately controlled by a single scalar temperature `α`, auto-tuned (`update_temperature`, standard Haarnoja-style dual) toward `temp_target_entropy`. Confirmed exactly in `agent.py:355`: `temp_target_entropy = 0.5 * action_dim * log(2·π·e·temp_target_sigma²)`, with `temp_target_sigma=0.15` (`flashSAC.yaml:45`) — the differential entropy of an *isotropic* Gaussian with std 0.15 in every dimension. So the target is isotropic-equivalent, but nothing forces the actual per-dimension `log_std` allocation to be isotropic or curvature-shaped — only their aggregate entropy needs to hit that target. The *magnitude* of exploration is well-calibrated (temperature-tuned toward an isotropic-equivalent budget); its *directional allocation* across action dimensions has no connection to the critic's local geometry at all.
- **Reward/target normalization ratchets.** `reward_normalization.py`: `new_G_r_max = torch.maximum(G_r_max, torch.max(torch.abs(new_G_r)))` — monotone, non-forgetting, checkpointed. Feeds a **fixed**-support (`[-5, 5]`) 101-bin categorical critic.
- **No wall-clock instrumentation is released.** CSVs log only `env_step`; `train.py`/`logger.py` have no time tracking. The paper's "Compute Time (min)" x-axis (real, and FlashSAC does win there — Fig. 8, sim-to-real: reduces training time "by nearly an order of magnitude") is computed offline via Appendix A's protocol: algorithm update-time is profiled on **2** reference environments (MuJoCo Humanoid-v4, DMC Walker-run) and **reused as a constant** across all ~20+ task configs (obs/act dims ranging Shadow 157/20 to G1-rough 310/37). Not independently reproducible from the repo; the reused constant is a known source of per-task distortion.
- **Run-to-run drift and statistical floor.** Two released same-config run families differ 1.89% (G1-flat) to 7.33% (Shadow) — upper bound, since they terminate at different steps. Converged-arm coefficients of variation: 2.8/2.0/1.1/3.3%. At a 2% TOST equivalence margin: n=25 seeds needed on Allegro, n=35 on G1-rough, n=4646 if an arm destabilizes.
- **Params.** Actor ~0.29M, critic ~1.11M each (pair ~2.23M) — paper's "2.5M-parameter 6-layer network for both actor and critic" is loose.

---

## First-principles framing

- **First principle.** For any differentiable critic, the local curvature of Q with respect to the action *is* the information that determines how sensitive return is to perturbing each action dimension — a low-curvature direction can absorb noise for free, a high-curvature direction cannot. This is a property of the objective, not a hyperparameter.
- **Assumption being challenged.** FlashSAC (and every off-policy actor-critic in its lineage — CrossQ, SimBa, XQC, BRO, FastDSAC) treats exploration shape as something the policy network should *learn from scratch* via the policy-gradient signal alone, or via a separate learned heuristic (FastDSAC's Dimension-wise Entropy Modulation is a learned softmax, not derived from the objective). The field's implicit belief: exploration structure and value structure are separate learning problems. Ciosek & Whiteson's 2018 result (below) already proved this false for the Gaussian/scalar-critic case; nobody has carried it into the modern high-throughput, distributional-critic lineage.
- **The bet.** A single mechanism — condition exploration covariance directly on the critic's own action-Hessian, keep FlashSAC's existing temperature-controlled total entropy budget unchanged — produces gains that track FlashSAC's own measured capacity asymmetry: largest on Allegro/Shadow (dexterous, sharp curvature), near-zero on G1-flat (locomotion, shallow curvature). Specific numbers in [[#Falsifiable bets]].

---

## Related work — foils and the one dead ingredient

| Paper | What it actually does | Role here |
|---|---|---|
| [[1706.05374|Ciosek & Whiteson, Expected Policy Gradients]] (JMLR v21 2018) | Verified directly (Lemma 2, Algorithm 3): $\Sigma \propto \sigma_0^2 e^{cH}$, $H$ = Hessian of $Q$ w.r.t. action at the policy mean. Paper's own cost argument, verified verbatim: "this Hessian... is the same size as the policy's covariance matrix, which any policy gradient must store anyway, and should not be confused with the Hessian with respect to the parameters of the neural network... which can easily have thousands of entries" — i.e. the "free" claim is about *matrix size* ($d\times d$, $d$=action dim), not about the cost of *computing* it at FlashSAC's throughput, which EPG never tested (4 single-env MuJoCo domains: HalfCheetah-v1, InvertedPendulum-v1, Reacher2d-v1, Walker2d-v1). | **Theoretical source of the mechanism.** Never combined with a distributional/categorical critic or a massively-parallel/high-UTD setting — confirmed by exhaustive adversarial search (below). Gate B exists precisely because "free" (size) ≠ "free" (wall-clock at scale). |
| [[2603.12612|FastDSAC (DEM)]] | Direct SAC-family, massively-parallel, high-UTD humanoid competitor to FlashSAC. Primary critic: continuous (DSAC-T-style) distributional, not fixed-support categorical — but Section 4.3/Fig. 5 also runs a **`FastSAC (C51+DEM)` ablation**, i.e. DEM has already been paired with a categorical critic (it underperforms the continuous-critic version but exists). DEM itself redistributes the exploration budget per-dimension via a **temperature-scaled softmax gate** on learned logits (Eq. 4), zero-sum, "emergent and driven solely by reward maximization" — not derived from critic curvature. Appendix J (their own internal ablation) shows `C51+DEM`'s performance is highly sensitive to categorical support-range choice on Basketball. Separately, Section F ("Comparison with Contemporary Works") directly re-runs FlashSAC on the 61-DoF `h1hand-basketball`/`h1hand-balance_hard` tasks (outside FlashSAC's own published suite) and reports it "scoring below 200 even after 10⁶ environment steps" — confirms the number, but it's FastDSAC's re-evaluation, not a FlashSAC-reported figure (Phase 3 caveat below still applies). Also states explicitly: DEM's config is **held fixed across all tasks within a benchmark domain**, "in contrast to FastTD3, whose distributional critic may require task-specific tuning of the C51 support range" — a real, stated within-domain transfer property, not silence. | **Required H1 foil, not an anchor replacement** (task locked FlashSAC as anchor/baseline). Since `C51+DEM` already exists, the open gap is narrower than "structured exploration + categorical critic" — it's specifically **curvature-*derived* exploration** (an objective property) **vs. a *learned softmax heuristic*** on the same categorical-critic substrate. Falsifiable edge, now more precise given DEM's stated within-domain fixed-config property: curvature should transfer *across* benchmark domains (HumanoidBench ↔ IsaacLab ↔ MuJoCo Playground) with one configuration, a stronger claim than DEM's own (only within-domain fixed). |
| [[2606.31691\|FastDSAC (truncated-Gaussian policy)]] | A **different** paper with the same name (later, different mechanism — truncated Gaussian policy to exclude OOD actions under high UTD). Not to be conflated with the DEM paper above. | Secondary reference only; not a required comparison target. |
| [[2601.20071|Distributional Sobolev RL (DSDPG)]] (Debes & Tuytelaars, 2026) | Already in the vault, missed by the WebSearch sweep. Models the *joint distribution* of return **and its action-gradient** ($\partial Z/\partial a$, first derivative, distributional) via a generative critic + differentiable world model, for a *deterministic* DPG-style policy — no Gaussian exploration covariance at all, so nothing to shape. Authors flag high computational cost from multi-sample input-gradients as an open limitation. | **Adjacent, not competing.** Confirms "gradient/derivative-aware distributional value learning" is a live thread, but at the first-derivative, gradient-signal-robustness level, not second-derivative exploration-shaping — different problem, independent evidence for Gate B's cost concern (their limitation is structurally the same risk). |
| [[2509.25174|XQC]] (Palenicek et al., ICLR 2026) | Also a 101-atom, `[-5,5]`-support categorical critic (essentially FlashSAC's recipe) — and does analyze "the critic's Hessian." **That Hessian is of the critic *loss* w.r.t. network *parameters*** (loss-landscape conditioning), not of $Q$ w.r.t. *action*. Different object entirely. | Flagged explicitly to prevent a shallow read from mis-citing this as prior art. |
| BRO / BRC (arXiv 2405.16158) | [[2405.16158\|Scaling Off-Policy RL with Batch and Weight Normalization]] lineage; "optimistic exploration" via dual-actor KL-regularized UCB from quantile-ensemble *disagreement* (epistemic variance), not curvature. Cites EPG only as background. | Confirms curvature-of-mean and variance-of-ensemble are two distinct, non-overlapping mechanisms in the current literature. |
| [[2607.01880|DySEL]] (Chang, Osa, Harada, RLJ 2026) and Adaptive HL-Gaussian (Chen et al. 2025) | Learn the categorical critic's `[v_min, v_max]` support directly via constrained optimization, rather than rescaling a fixed support. Explicitly: *"PopArt is effective for scalar regression, it does not naturally extend to the preservation of distributional shape in categorical critics."* | Live, already-published, better-motivated alternatives to the killed ingredient below. |
| [[2301.04104\|DreamerV3]] symlog+twohot | Fixed universal transform, no running statistic, so no ratchet question arises by construction — a different strategy (transform the target space) than adaptively rescaling a fixed-support critic. Never grafted onto a SAC-family massively-parallel algorithm. | Noted as a genuinely open adjacent direction, **out of scope for this project** — don't chase it here. |
| [[2105.05347|Schaul, Ostrovski, Kemaev, Borsa]] (DeepMind, 2021) | Direct counter-evidence: on Atari `asterix`, PopArt-style **non-ratcheting** fast scale adaptation caused *repeated performance collapses* under a reward spike; their conservative, effectively non-forgetting statistic stayed stable. | Falsifies the premise of the killed ingredient. |

### Killed: non-ratcheting reward/target normalization

Original plan: replace FlashSAC's monotone `G_r_max` ratchet with an online Kalman-filter-style estimator (candidate: [[2604.23056|K-Score]]). Adversarially verified and dropped, for the record (per the vault's standing rule to log dead candidates, not just live ones):

1. K-Score is validated only on toy on-policy policy-gradient tasks (CartPole, LunarLander), for raw-reward normalization — not TD-target/critic-support normalization, not off-policy, not distributional. Large transferability gap.
2. Two stronger, already-published, live alternatives exist for the actual problem (DySEL, Adaptive HL-Gaussian — learned support bounds; and DreamerV3-style symlog+twohot — sidesteps the problem by transform rather than estimation).
3. Direct published evidence (Schaul et al. 2021) contradicts the working premise that "ratchet = bug" — fast, non-ratcheting adaptation has a documented failure mode (spike-induced collapse) in a closely analogous return-scaling-for-value-learning setting.

No rescue attempted. One mechanism is enough for a coherent recipe; a second ingredient bolted on to fill a pattern would violate the one-mechanism-story requirement this plan is held to.

---

## Proposed method: Curvature-Conditioned Exploration

**What stays unchanged:** FlashSAC's scalar temperature `α`, auto-tuned against `target_entropy` (from `σ_tgt=0.15`) — this already controls the *total* exploration budget well. Leave it alone.

**What changes:** the *directional allocation* of that budget across action dimensions, currently a free-form learned `log_std` head shaped only by the Q-maximization loss.

1. Let $\bar{Q}(s,a) = \mathbb{E}_{Z(s,a)}[\cdot] = \text{softmax}(\text{logits}(s,a)) \cdot \text{atoms}$ — the categorical critic's mean, a smooth composition, so $\nabla_a^2 \bar{Q}(s, \mu(s))$ is well-defined by plain autodiff regardless of the critic being distributional.
2. Compute $H(s) = \nabla_a^2 \bar{Q}(s, \mu(s))$ at the policy mean, via Hessian-vector products (Pearlmutter's trick — forward-over-reverse), reusing the $\nabla_a Q$ graph FlashSAC's actor loss already computes. No full Hessian materialization.
3. **Contingent on Phase 0 Gate A (below):**
   - If $H(s)$ is negative-definite and reasonably conditioned → use EPG's closed form directly: exploration covariance direction $\propto \exp(\text{scaled } H)$, eigenvectors of $H$ set the directional allocation, magnitude re-normalized to preserve FlashSAC's existing `target_entropy` (so the intervention is a *reshaping*, not a change of budget).
   - If $H(s)$ is indefinite (plausible near contact switches, the expected failure mode in contact-rich dexterous/locomotion tasks) → fall back to a PSD surrogate: Gauss-Newton approximation on the categorical logits, or eigenvalue clipping before exponentiating. This is not a minor implementation detail — it changes the functional form the plan commits to, which is exactly why Gate A must run before Phase 1, not be assumed.
4. Replace the free-form `log_std` head's *direction* with the (possibly clipped) Hessian eigenbasis; keep the scalar `α`-controlled magnitude.

---

## Phase 0 — go/no-go gates (mandatory, before any full training run)

FlashSAC ships no pretrained checkpoints (confirmed: repo has no `.ckpt`/`.pt` release, only a checkpointing mechanism for runs you train yourself). Both gates require a short training run first.

**Gate A — Hessian-definiteness diagnostic.**
Train FlashSAC as-released to an early checkpoint and a late checkpoint on one hand task (Allegro or Shadow) and one locomotion task (G1-flat). At each checkpoint, sample a batch of states, compute the eigenspectrum of $\nabla_a^2 \bar{Q}(s,a)$ at the policy mean. Decision rule:
- Predominantly negative-definite on **both** probed tasks, condition number bounded → EPG's closed form is well-posed, proceed as specified.
- Indefinite on **both** → commit to the PSD-surrogate branch instead; this is the expected outcome in contact-rich regimes and must not be treated as a fallback of last resort — design for it.
- **Task-dependent split** (e.g. negative-definite on G1-flat, indefinite on Allegro) — the likely-real outcome, and it is not a coin flip: if the two branches ran on different tasks, every cross-task comparison in this plan (bets 1/2/4) would be confounded by which functional form ran where. Pre-committed resolution: run the **PSD surrogate everywhere**, holding the mechanism fixed across the full comparison; report the closed form only as a same-task ablation on the subset where it's well-posed, never as part of the main cross-task result.
- This same run also settles whether softmax/categorical saturation degenerates the Hessian late in training (a live, unverified concern surfaced during literature review) — check condition number early-vs-late, not just definiteness.

**Gate B — wall-clock break-even microbenchmark.**
Under FlashSAC's own Appendix A protocol (profile on the same 2 reference environments, reuse the constant), measure the per-update wall-clock overhead of the Hessian-vector product against the unmodified baseline, at FlashSAC's actual scale (1024 parallel envs, batch 2048, UTD 2/1024). State the break-even explicitly before Phase 1: if the HVP adds $X\%$ per-update overhead, the method must recover it via $\geq X\%$ fewer gradient updates to reach matched return, or the wall-clock half of the goal fails **by design**, independent of any final-return win. No prior work has measured HVP cost at this scale (confirmed by adversarial search) — this is a first measurement, not a look-up.

Both gates are pass/fail on the *plan's* mechanism statement, not on the project — a fail on Gate A changes the functional form (still proceeds, with the surrogate); a fail on Gate B is the honest signal that this mechanism cannot deliver the speed half of the bet and the project should be re-scoped to a results-only claim before further investment.

---

## Phase 1 — implement and unit-verify

- Implement both branches (EPG closed form, PSD surrogate) behind Gate A's decision.
- Unit-check ("mechanism off," not "curvature off"): identity $H$ is positive-definite, so `exp(scaled H)` produces *uniform inflation*, not a match to FlashSAC's baseline — that's a different test with a different expected value, not a no-op. The actual regression test: zero the curvature-scaling coefficient entirely and confirm bit-comparable returns against unmodified FlashSAC on one task, one seed. This is the test that catches implementation bugs before they're mistaken for a negative result.

## Phase 2 — full-suite training (sim)

- Train and evaluate on FlashSAC's own full task suite (60+ tasks, 10 simulators) as released — sim only, matching decision to trust their harness with no reproduction gate.
- Seed counts per task from the CoV table above (n=25 Allegro, n=35 G1-rough minimum for a 2% TOST margin); do not report an effect size below the run-family drift floor (1.89–7.33%) as real.
- Report both speed metrics separately per the locked decision: wall-clock (Gate B protocol) and sample-efficiency (return vs. env-steps/gradient-updates).

## Phase 3 — FastDSAC head-to-head

- On tasks where FlashSAC's and [[2603.12612|FastDSAC]]'s suites overlap, compare structured-exploration mechanisms directly: curvature-conditioned vs. DEM.
- **Caveat to enforce, not skip:** FlashSAC's own HumanoidBench evaluation is 14 locomotion tasks *without hand control* (verified: Table 7, paper text — "We evaluate 14 humanoid locomotion tasks without hand control from HumanoidBench"). Any FastDSAC claim about FlashSAC's performance on hand-control tasks (e.g. `h1hand-basketball`) is FastDSAC's own out-of-original-suite re-evaluation of FlashSAC's released code, not a FlashSAC-reported number — cite it as such if used, don't launder it as FlashSAC's own result.
- Test the transfer claim: does one fixed curvature-conditioned configuration generalize across tasks without per-task retuning, where DEM's learned gate is trained per run? Report as a genuine open question resolved by this experiment, not asserted going in.

## Phase 4 — sim-to-real

- Mandatory per project scope. Match FlashSAC's own sim-to-real protocol (Unitree G1) so the wall-clock comparison ("hours → minutes") stays apples-to-apples.
- Primary risk to watch: the reward-normalization ratchet stays unchanged in this plan (ingredient killed) — if sim-to-real transfer degrades, first check whether it's attributable to the untouched normalization stack before attributing it to the exploration mechanism.

---

## Falsifiable bets

**Bet 2 is the load-bearing stop-condition.** Bet 1 is directional context only — FlashSAC's own capacity-scaling sweep covers just 4 task families (32.9, 15.8, 5.2, 0.1%), two of them (G1-rough, G1-flat) statistically indistinguishable given their CoV (1.1%, 3.3%) against a 5.1-point spread. A Spearman correlation over n=4 points has no real power and must not be the thing the project lives or dies on. If a proper quantitative correlation test is wanted later, it requires first extending FlashSAC's own width sweep to more than 4 task families (a real Phase 2 sub-task, not assumed here) — out of scope for the core bet.

1. **Capacity-curvature direction (directional, not a stop-condition).** Curvature-conditioned exploration's per-task gain should be qualitatively *larger* on Allegro/Shadow than on G1-flat/G1-rough, consistent with FlashSAC's own published capacity asymmetry. Reported as supporting evidence for the mechanism story, not as a statistical test.
2. **Dexterous-task win (load-bearing).** ≥10% final-return improvement over FlashSAC on Allegro and Shadow, at the seed counts above (properly powered against the CoV floor), without regressing G1-flat/G1-rough by more than the run-family drift floor (7.33%). **If this fails, the thesis is wrong and the project stops here** — this replaces bet 1 as the stop-condition.
3. **Speed, matched-protocol.** Meets or beats FlashSAC's wall-clock (Appendix A protocol) AND sample-efficiency on the dexterous task subset; Gate B's break-even is the hard precondition for this bet to even be attempted.
4. **FastDSAC transfer edge.** One fixed curvature-conditioned configuration matches or beats DEM's per-task-tuned performance on ≥2 of the 3 overlapping task families, without per-task retuning. Evaluated only on tasks where Gate A's PSD-surrogate-everywhere rule (or the closed form, if well-posed everywhere) held the mechanism fixed across the comparison.

---

> [!warning] Risks
> - **Primary scientific risk:** EPG's local quadratic Taylor approximation of $Q$ was validated only on smooth, low-DoF classic control. Contact-rich dexterous manipulation and humanoid locomotion (contact switching, hybrid dynamics) may be far less locally-quadratic around the mean action — this is the dominant threat to the whole proposal, independent of scalar-vs-categorical critic, and is exactly what Gate A is designed to catch early.
> - **Wall-clock risk:** HVP cost at 1000+-env massively-parallel scale has zero precedent in the literature (confirmed by adversarial search) — Gate B is a first measurement, not a validated assumption.
> - **Statistical risk:** run-family drift (1.89–7.33%) and per-task CoV set a real noise floor; underpowered seed counts would make a claimed win indistinguishable from drift.
> - **Attribution risk in Phase 4:** the reward-normalization ratchet is left untouched by this plan; any sim-to-real degradation needs to be checked against that known-unfixed component before being attributed to the new exploration mechanism.
> - **FastDSAC comparison risk:** don't compare against tasks outside FlashSAC's own original suite as if they were FlashSAC's reported numbers (see Phase 3 caveat).

---

## Unresolved questions

- PSD-surrogate exact form (Gauss-Newton on logits vs. eigenvalue clipping) — decided by Gate A's result, not fixed in advance.
- Whether categorical cross-entropy's own saturation degenerates $H$ late in training — flagged, untested, Gate A settles it empirically.
- Exact real-robot G1 access/logistics for Phase 4 — out of scope per the "hardware not a plan constraint" decision; assumes FlashSAC's own setup.
- Whether DEM in FastDSAC actually requires per-task retuning, or generalizes some other way not stated in its own paper — Phase 3 resolves this rather than assuming it.

---

## Cross-References

- [[2604.04539|FlashSAC]] — anchor and baseline
- [[2603.12612|FastDSAC (DEM)]] — required foil
- [[1706.05374|Expected Policy Gradients (EPG)]] — theoretical source of the curvature-exploration mechanism
- [[2607.01880|DySEL]] — learned-support alternative to the killed reward-normalization ingredient
- [[2105.05347|Return-based Scaling]] — counter-evidence that falsified the killed ingredient's premise
- [[2604.23056|K-Score]] — killed ingredient candidate, logged for the record
- [[2606.31691|FastDSAC (truncated Gaussian)]] — distinct paper, secondary reference
- [[2301.04104|DreamerV3]] — symlog+twohot, adjacent open direction, out of scope here
- [[2405.16158|BRO / Scaling Off-Policy RL with Batch and Weight Normalization]] — variance-based exploration contrast
- [[2509.25174|XQC]] — parameter-Hessian conflation trap, WeightNorm's actual claimed mechanism
- [[2601.20071|Distributional Sobolev RL (DSDPG)]] — adjacent first-derivative work, independent evidence for Gate B's cost concern
