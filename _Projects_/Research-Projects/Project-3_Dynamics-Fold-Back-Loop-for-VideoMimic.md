---
title: Dynamics Fold-Back Loop for VideoMimic Real2Sim2Real
tags:
  - project
  - active
  - robotics
  - humanoid
  - sim-to-real
  - imitation-learning
  - reinforcement-learning
aliases:
  - Dynamics Fold-Back Loop
  - Iterated ASAP for VideoMimic
---

# Dynamics Fold-Back Loop for VideoMimic Real2Sim2Real

> [!abstract] Thesis
> VideoMimic's sim2real gap has the irreducible truth that it is dominated by *dynamics* mismatch (contact, friction, actuator response) rather than reconstruction fidelity for the deployment failure mode this project targets — its real2sim reconstruction is a static, one-time scan with no round-over-round degradation signal, whatever its absolute quality (a separate question, [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2]]'s axis) — which breaks the field's implicit assumption (Arcadia, CASHER, and this vault's own [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2]]) that closing a real2sim2real loop means re-grounding the *reconstruction or retargeting*, and I bet that wrapping [[2502.01143|ASAP]]'s single-round dynamics-correction mechanism inside [[2606.27353|Continual Variational Neural Dynamics]]'s proven iterative loop structure produces monotone real-SR improvement across ≥3 rounds on VideoMimic's G1 tracking task — a claim never tested on any legged or humanoid platform; the one mechanism proven to do this monotonically (41→9cm) has only ever run on a quadrotor.

**Anchor:** [[2505.03729|VideoMimic]] — the real2sim2real pipeline being closed; its own Sec 5.2 real deployment uses only ad hoc sim2real mitigations (relaxed termination tolerance, physics-perturbation training), no fold-back of any kind. **Mechanism sources:** [[2502.01143|ASAP]] — the single-round dynamics-correction primitive, verified code-compatible with VideoMimic's exact G1 action space; [[2606.27353|Continual Variational Neural Dynamics]] — the only iterative loop structure in the literature with a proven monotone multi-round trajectory, on a different embodiment.

---

## Background — what's actually verified, not assumed

Verified this session directly against alphaXiv full text and, for ASAP, the cloned repo (`data/.repositories/ASAP`) — not abstracts, not prose claims taken on faith.

- **VideoMimic's real2sim isn't a fold-back target, even though its absolute fidelity is a known weak point.** Its reconstruction (MegaSam/MonST3R depth + NKSR meshification, verified this session on our own reproduction run) is a one-time video scan of static geometry — it doesn't degrade with deployment and there's no natural real-world signal that would improve it *round-over-round*. Whether it's good *enough* in absolute terms (MeshMimic's own data says often not, on terrain-contact tasks) is [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2]]'s axis — a one-time reconstruction-quality graft (MeshMimic's loss-terms) plus retargeting (DDR), not a per-round correction. Explicitly out of scope here to avoid duplicating that project.
- **ASAP has no loop, confirmed in code, not just prose.** `README.md` ships exactly two commands: train the delta-action model once on a pre-recorded motion file with an `action` field (`+exp=train_delta_a_open_loop`), then fine-tune the policy once against it (`+exp=train_delta_a_closed_loop`, `algo.config.num_learning_iterations=1000`). No orchestration script chains these; no round counter anywhere in the released code. The paper states outright: "we deploy the fine-tuned policy **without** delta action model in the real world" — the correction is discarded after one use, not kept in the loop.
- **ASAP is action-space-compatible with VideoMimic, verified at the code level, not by domain analogy.** Both control the same Unitree G1 with `a_t ∈ R^23` (target joint positions, PD position control — confirmed against VideoMimic's own `DOF_MODE_POS` / `num_dof=23` from this session's live Isaac Gym query). Both are instances of the same "video → SMPL retarget → DeepMimic-style RL tracking" pipeline shape (ASAP: TRAM → retarget → phase-conditioned tracking; VideoMimic: SAM2/VIMO/ViTPose/BSTRO → MegaHunter → retarget → joint/link/feet-contact tracking reward). ASAP's delta-action model consumes `(state, action, real-trajectory)` tuples — it does not care whether the reference came from TRAM or MegaHunter.
- **ASAP's data requirement is real but unverifiable from released code.** The paper states >400 real clips would be needed to train the *full* 23-DOF delta-action model, but only 100 were safely collected for their agile motions (two G1s broke), forcing a fallback to a 4-DOF ankle-only model. This fallback is a real, live code path (`humanoidverse/envs/delta_a/delta_a_closed_loop.py:155-158`, `self.config.anklePR` zeroes every non-ankle-pitch-roll action dimension) — not just a paper claim. The >400 number itself cannot be independently checked: the real G1 motion dataset isn't published, only the training infrastructure is. Whether VideoMimic's gentler motions (walking, LAFAN dance vs. backflips/kicks) need fewer real clips at full 23-DOF is unknown and must be checked empirically, not assumed.
- **[[2606.28476|FADA]] is the cheap fallback if full-DOF proves too data-hungry.** Same G1, same action-space family, but only ~2 minutes of real rollouts (≈6000 control steps at 50Hz) per adaptation round via LoRA-finetuning an inverse-dynamics module — no simulator refit, no reward, no privileged labels. Also single-shot (confirmed this session). FADA's own code is not released (`FADA-humanoid` GitHub repo, checked directly, is only the Vite/React project-page landing site — "Code: coming_soon" in the paper is accurate).
- **[[2606.27353|Continual Variational Neural Dynamics]] is the only genuinely iterative, proven mechanism found in an exhaustive search this session** (general robotics → humanoid-specific → broadened to bipedal/quadruped/lifelong-learning framings, multiple rounds, cross-checked against ENPIRE, Learning-While-Deploying, Extreme-RGMT, Self-adapting-Agents, and the SimOpt lineage). It alternates real rollouts and differentiable-sim policy improvement via a condition-aware latent residual dynamics model, and reports actual round-by-round trajectories: 41cm→9cm (wind recovery), 52cm→24cm→12cm (cut-propeller, a genuinely novel hardware fault). But real-hardware validation is quadrotor-only; the manipulation extension is simulation-only; nothing legged.
- **The older SimOpt-lineage loop already demonstrated the failure mode this project must guard against.** [[2206.14661|ADR Benchmark]] (Tiboni et al., 2022) empirically shows SimOpt's iterative correction *degrading* mid-loop under noisy conditions on a harder task — an intermediate ill-behaving policy produces a misleading real rollout, which corrupts the next round's correction. This is real, observed drift in a mechanically similar (though not identical) loop, not a hypothesized risk.
- **Iteration only works if each round is cheap — confirmed across embodiments, not just asserted.** [[2607.29172|CLIFT]] (2 rounds, 93→100%/70→98%/53→96%, no simulator, real-only), [[2606.19980|ENPIRE]] (agentic hill-climb, +3.8/+10.8/+0.4/+0.9/+1.3pp over wall-clock hours), and [[2605.00416|Learning While Deploying]] (fleet-scale, 0.95 vs 0.68 SFT baseline) all show real, sustained multi-round gains — all manipulation, all real-only (no simulator), and all deliberately keep each round's data/compute cost low. This is the argument for FADA-first, ASAP-full-DOF-second in the phase ordering below.
- **[[2605.21458|Fisher-SEP]]'s formal bound is the theoretical reason this project can fail even if every mechanism above works individually.** Any *passive* fold-back loop's error splits into a local component (states the deployed policy visits — closed by more rounds) and a reachability component (states it doesn't — provably bounded away from zero at any horizon under passive learning alone). For locomotion specifically, a successful walking policy rarely visits fall/recovery states — exactly the states most informative for dynamics correction. Passively-collected VideoMimic rollout data may systematically under-sample the highest-value correction target, independent of how good the correction mechanism itself is.

---

## First-principles framing

- **First principle.** A fold-back loop only closes the gap on states its own rollouts actually visit (Fisher-SEP's local/reachability bound, proven, not hypothesized). For a tracking policy that mostly succeeds, "actually visits" undersamples exactly the contact-transition and recovery states where sim-real dynamics mismatch is largest and most consequential — the same states that make ASAP's full-DOF correction data-hungry (agile motions with more failure/recovery events needed more data to correct, per ASAP's own experience).
- **Assumption being challenged.** The field splits into two camps, neither of which studies the loop itself run to convergence: the twin-reconstruction camp (Arcadia, CASHER, this vault's Project-2) treats re-grounding the *scene/motion content* as the lever; the single-shot-correction camp (ASAP, HALO, FADA) treats one dynamics-alignment pass as sufficient and stops. Both implicitly assume their one intervention is enough — nobody has run either mechanism to multiple rounds on a humanoid and reported whether it converges or drifts.
- **The bet.** Wrapping ASAP's (or FADA's, if data-scarcity forces the cheaper option — see Phase 0) dynamics-correction mechanism inside a loop structure modeled on the Zurich paper's proven pattern (condition-aware residual model, updated each round from accumulated real/proxy-domain rollouts, differentiable- or standard-sim retraining, redeploy) produces a monotone tracking-error trajectory across ≥3 rounds on VideoMimic's G1 policy — where an *ungated* version of the same loop (no check on whether each round's correction actually helps) drifts, replicating the SimOpt-under-noise failure mode Tiboni et al. already documented in the mechanically adjacent DR-parameter lineage. Specific numbers in [[#Falsifiable bets]].

---

## Related work — roles, not just citations

| Paper | What it actually does | Role here |
|---|---|---|
| [[2505.03729\|VideoMimic]] | Video → real2sim reconstruction (MegaSam/NKSR) + kinematic retargeting (PyRoKi) + 4-stage RL. No fold-back anywhere; Sec 5.2 real deployment is a leaf node. | **Anchor.** The pipeline this project adds a loop to. Real2sim/retargeting stage kept unchanged — that's Project-2's axis, not this one. |
| [[2502.01143\|ASAP]] | Delta-action residual dynamics correction, single-round, real G1, verified code-compatible action space. | **Primary mechanism source.** The per-round correction step, wrapped in an outer loop this project adds. |
| [[2606.28476\|FADA]] | Cheaper single-round IDM finetune, ~2 min real data, same G1. Code not released. | **Fallback mechanism** if ASAP's full-DOF data requirement proves prohibitive (Phase 0 gate). |
| [[2606.27353\|Continual Variational Neural Dynamics]] | Genuinely iterative, condition-aware residual dynamics loop, proven monotone (41→9cm), quadrotor real hardware. | **Loop-structure source.** The iteration/accumulation/online-inference pattern this project borrows and re-embodies for legged locomotion. |
| [[2605.21458\|Fisher-SEP]] | Formal local/reachability decomposition of fold-back error; proves passive loops can't close the reachability gap. | **Theoretical grounding** for why an *ungated*, purely passive version of this loop is expected to plateau or drift — motivates the gate in Phase 3. |
| [[2206.14661\|Online vs. Offline ADR Benchmark]] | Empirically shows SimOpt-style iterative dynamics correction degrading under noise on a hard task. | **Documented failure precedent** in a mechanically adjacent (parameter-only, not residual-action) loop — the risk this project must not silently repeat. |
| [[2607.29172\|CLIFT]], [[2606.19980\|ENPIRE]], [[2605.00416\|Learning While Deploying]] | Real-only (no simulator) closed loops, all proven multi-round, all manipulation. | **Cross-embodiment evidence that cheap-per-round is what makes iteration actually work** — informs the FADA-first phase ordering, not a mechanism source itself. |
| [[2512.00076\|Arcadia]], [[2412.01770\|CASHER]] | Real2sim2real closed loops that re-ground *assets/scenes*, single-pass each. | **Different axis (reconstruction, not dynamics)** — the [[Sim2Real]] B2 cluster's existing gap; this project instantiates the B2/H6 twin-free-vs-twin-dependent question for the dynamics-correction side specifically, not the asset side. |
| [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting\|Project-2]] | Anchored on VideoMimic itself; grafts MeshMimic's reconstruction loss-terms (one-time) plus DDR's terrain-extended dynamic *retargeting* onto it, fold-back re-solves the reference motion on failure segments. | **Sibling project, different loop.** Project-2 corrects *what the robot is asked to do and how well the scene is reconstructed* (reference + geometry); this project corrects *how well the simulator predicts what happens when it tries* (the dynamics). Not competing — could in principle compose, not attempted here to keep one mechanism per project. |

---

## Killed: full real2sim re-grounding loop (Arcadia/CASHER-style)

Considered and rejected during scoping.

1. **Option:** close the loop by re-scanning the deployment scene and re-deriving the motion reference from new real-world video each round (Arcadia/CASHER's mechanism, or Project-2's DDR-based retargeting fold-back).
2. **Why rejected here:** the scene geometry doesn't change round-to-round in a fixed deployment environment — there's no natural signal from a robot's *dynamics* failure that should trigger a *re-scan*, regardless of the reconstruction's absolute quality. Project-2 already owns the reconstruction/retargeting axis (its own one-time fidelity graft + DDR retargeting, not a fold-back target either) for tasks matching MeshMimic's hardest multi-contact difficulty. Re-deriving it here would duplicate that project's mechanism under a different name.
3. **What stays instead:** the loop closes on *dynamics* (delta-action / IDM correction), not *content* (scene/motion). If a future round of evidence shows VideoMimic's real2sim is also degrading over deployments (e.g., outdoor scenes with lighting/weather drift), that's a case for composing with Project-2, not a reason to rebuild its mechanism here.

---

## Proposed method: iterated dynamics correction on VideoMimic's G1 pipeline

**What stays unchanged:** VideoMimic's real2sim reconstruction and retargeting (Stages producing `retarget_poses_g1.h5`), and its 4-stage RL training recipe (MCPT → terrain-conditioned → distillation → RL finetune) as the base-policy source for round 0.

**What's added:** a fold-back loop wrapping a per-round dynamics-correction step, run after Stage 4 (or the latest available VideoMimic checkpoint), structured on Zurich's proven pattern rather than ASAP's stop-after-one-round default.

1. Deploy the current policy (round 0: VideoMimic's own Stage-4 checkpoint) in the target evaluation domain — sim2sim proxy domain first (IsaacGym-trained → MuJoCo or Genesis, following ASAP's own validated cross-simulator methodology), real G1 only if/when hardware access materializes (Phase 4, explicitly conditional, matching Project-2's own honest framing).
2. Log `(state, action)` rollout trajectories from this deployment, in the schema ASAP's motion library already expects (`root_trans_offset`, `pose_aa`, `fps`, plus the recorded `action` field) — this is the concrete engineering bridge from VideoMimic's `retarget_poses_g1.h5` format to ASAP's delta-action training input.
3. Train (or update, if a residual model already exists from a prior round) a dynamics-correction model on the accumulated rollout data — start with FADA's cheap IDM-finetune (≈2 min real/proxy data, LoRA) per Phase 0's data-efficiency gate; escalate to ASAP's full delta-action model only once that gate passes.
4. Fine-tune the policy against the corrected dynamics model (ASAP's existing recipe, `train_delta_a_closed_loop`).
5. Redeploy, log new rollouts, and repeat for up to 3 rounds — gating each round on whether the correction actually reduced tracking error on a held-out evaluation segment (the fidelity gate this vault's [[Sim2Real|B2 cluster's H5]] hypothesis already specifies as a precondition for trusting any monotone-improvement claim). Gate C below runs this gated-vs-ungated comparison directly.

---

## Phase 0 — go/no-go gates (mandatory, before any full pipeline build)

**Gate A — data-efficiency check, before committing to full-DOF.** On VideoMimic's own Stage-1 (MCPT, gentler AMASS/LAFAN motions) checkpoint, measure how many proxy-domain rollout episodes are needed for a full 23-DOF delta-action model (ASAP's mechanism) to converge to a stable correction, versus FADA's 4-DOF-or-cheaper IDM approach at its stated ~2-minute budget. Decision rule: if full-DOF converges within a budget comparable to what a real deployment schedule could plausibly supply (order-of-magnitude check against ASAP's own 100-clip agile-motion experience, adjusted for VideoMimic's gentler motion distribution), proceed with ASAP's full mechanism in the loop; otherwise, use FADA's cheaper correction as the per-round primitive throughout.

**Gate B — does one round already saturate the gain?** Before building the multi-round loop, run ASAP's mechanism exactly as released (single pass) on the VideoMimic checkpoint and measure the tracking-error reduction. If round 1 alone closes the sim-proxy-domain gap to within noise of the ceiling (no meaningful residual error left to correct), the loop's premise is moot for this specific policy/task combination — report that as a finding (single-shot suffices) rather than forcing a multi-round result.

**Gate C — gated vs. ungated drift check.** Run 3 rounds both with and without the fidelity gate (step 5). This is the load-bearing test: it directly replicates Tiboni et al.'s SimOpt-drift observation in this project's own mechanism, and is the empirical answer to whether Fisher-SEP's theoretical local/reachability concern actually manifests here.

---

## Phase 1 — implement and unit-verify

- Build the format bridge from VideoMimic's `retarget_poses_g1.h5` output to ASAP's motion-library `.pkl` schema (`root_trans_offset`/`pose_aa`/`fps`/`action`). Regression-test: with zero rollout data (empty correction), confirm the wrapped pipeline reproduces VideoMimic's own baseline tracking performance bit-comparably, isolating "did the bridge break anything" from "does the correction help."
- Implement the rollout logger (state+action trajectories in ASAP's expected format) as a wrapper around VideoMimic's existing playback/deployment scripts (`play_terrain_policy.sh`-style), not a rewrite of them.

## Phase 2 — single-round correction (no loop yet)

- Run Gate B's single-pass ASAP correction on VideoMimic's Stage-4 checkpoint, sim2sim (IsaacGym → Genesis or MuJoCo). Compare tracking error (MPJPE, matching ASAP's own reporting metric) before/after, isolating the correction-mechanism contribution from the loop contribution — the same separation Project-2 makes between its single-shot retargeting swap (Phase 2) and its closed loop (Phase 3).

## Phase 3 — fold-back loop, gated vs. ungated

- Run Gate C's 3-round comparison. Report the tracking-error trajectory per round for both conditions, on both VideoMimic's Stage-1 (MCPT-only, gentler) and Stage-2/3/4 (terrain-conditioned, more contact-rich) checkpoints separately — the contact-richness axis is the direct test of whether Zurich's continuous-disturbance result (wind) survives locomotion's discontinuous one (contact transitions, falls).

## Phase 4 — sim-to-real (conditional, not assumed)

- No G1 hardware access is assumed at scoping time (same honest framing as [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2]]'s Phase 4). If access materializes, repeat Phase 3 on real hardware. Until then, every result is reported as sim2sim (IsaacGym→Genesis/MuJoCo), with that caveat explicit — never silently upgraded to read as a real-hardware claim.

---

## Falsifiable bets

**Bet 2 is the load-bearing stop-condition.** Bet 1 is directional context only.

1. **Correction mechanism works at all, single-round (directional).** ASAP's (or FADA's) correction reduces sim-proxy-domain tracking error (MPJPE) on VideoMimic's Stage-4 checkpoint versus the uncorrected baseline. Expected given ASAP's own published results on a structurally identical task; supporting evidence, not the stop-condition.
2. **Gated loop is monotone across 3 rounds where ungated drifts (load-bearing).** On at least one of VideoMimic's terrain-conditioned checkpoints (Stage 2/3/4), the gated 3-round loop shows a monotonically non-increasing tracking-error trajectory, while the ungated variant shows a round where error increases relative to the previous round — Gate C's test (above), the same pattern Tiboni et al. observed. **If the gated loop also drifts, or if ungated never drifts either, the thesis's central claim (gating matters, the loop needs to be built carefully, not just wrapped) is wrong and the project reports that as the finding.**
3. **Contact-richness is the actual boundary condition (the novel part).** The Stage-1 (MCPT, gentle) checkpoint's gated loop converges faster / to a lower error floor than the Stage-2/3/4 (terrain-conditioned, contact-rich) checkpoint's, under matched round budget — direct evidence for the first-principles claim that discontinuous dynamics (falls, contact transitions) are harder for a passive fold-back loop to correct than continuous ones (Zurich's wind), consistent with Fisher-SEP's reachability-gap argument.
4. **No regression on VideoMimic's already-working motions.** Simple walking clips (VideoMimic's strongest category per its own reported results) should not regress in tracking error as a side effect of the wrapped correction loop.

---

> [!warning] Risks
> - **Primary risk: the data-efficiency wall.** ASAP's own agile-motion experience needed >400 real clips for full-DOF and broke two robots collecting 100. VideoMimic's gentler motions may or may not need less — Gate A is the first real measurement of this, not an assumption either way.
> - **Format-bridge risk.** VideoMimic's `retarget_poses_g1.h5` and ASAP's motion-library `.pkl` schema encode the same underlying SMPL→G1 retarget but were never designed to interoperate — the bridge (Phase 1) could silently drop information (e.g. contact/terrain context VideoMimic's reward depends on that ASAP's tracking-only reward doesn't use) in ways that only surface downstream.
> - **The gate itself could be the wrong one.** This project's fidelity gate (does the round's correction reduce held-out tracking error) is a direct instantiation of this vault's own unresolved [[Sim2Real|B2 cluster's H5]] hypothesis (does Δfidelity actually predict ΔSR) — if that hypothesis is false in general, it's false here too, and the gate provides no real protection against drift.
> - **Quadrotor-to-legged transfer of the loop *structure* itself is unproven**, independent of the dynamics-correction mechanism swapped into it — Zurich's condition-aware latent model assumes smoothly-varying hidden conditions (wind direction/magnitude); a fall is not a smoothly-varying condition, and the latent-conditioning machinery itself may need rethinking, not just the correction primitive inside it.
> - **Hardware risk.** Phase 4 is explicitly conditional, same caveat as Project-2 — sim2sim results must never be silently reported as real-hardware ones.

---

## Unresolved questions

- Whether to start the loop from VideoMimic's Stage-4 (fully finetuned, most real-deployment-ready) or an earlier stage (Stage-1 MCPT, simpler dynamics, better isolates the correction mechanism from confounds) — Phase 3 runs both, not fixed in advance.
- Whether ASAP's delta-action architecture needs modification to handle the *accumulation* across rounds (Zurich's latent-conditioning approach) versus ASAP's own from-scratch-per-round default — untested; first attempt uses ASAP's architecture unmodified inside an outer loop, revisited only if Gate C's drift comparison motivates it.
- Whether this project should eventually compose with [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2]] (dynamics correction + retargeting correction, jointly) — explicitly out of scope for now, kept as one mechanism per project per the same discipline Project-2 itself applies to CRISP/GRAIL.
- Real G1 hardware access/logistics for Phase 4 — unresolved, same as Project-2.

---

## Cross-References
- [[2505.03729|VideoMimic]] — anchor, the pipeline this project adds a loop to
- [[2502.01143|ASAP]] — primary dynamics-correction mechanism, verified code-compatible
- [[2606.28476|FADA]] — cheaper fallback correction mechanism
- [[2606.27353|Continual Variational Neural Dynamics]] — proven iterative loop structure, different embodiment
- [[2605.21458|Fisher-SEP]] — theoretical grounding for the gate (local/reachability bound)
- [[2206.14661|ADR Benchmark]] — documented drift precedent in an adjacent loop
- [[2607.29172|CLIFT]], [[2606.19980|ENPIRE]], [[2605.00416|Learning While Deploying]] — cross-embodiment evidence for cheap-per-round iteration
- [[2512.00076|Arcadia]], [[2412.01770|CASHER]] — different-axis real2sim2real loops (reconstruction, not dynamics)
- [[Sim2Real]] B2/H5/H6 — the vault's existing open closed-loop hypotheses this project instantiates for the dynamics-correction axis specifically
- [[Project-2_Terrain-Extended-Direct-Dynamic-Retargeting|Project-2: Terrain-Extended DDR]] — sibling project, closes the retargeting/real2sim loop instead of the dynamics/sim2real loop
- [[VideoMimic-Reproduction-Steps|VideoMimic Reproduction Steps]] — the live reproduction this project's checkpoints and infrastructure come from
