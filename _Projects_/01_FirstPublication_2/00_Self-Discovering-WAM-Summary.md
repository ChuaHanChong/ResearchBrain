---
title: "Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs — Summary"
tags:
  - WAM
  - diffusion
  - failure-detection
  - failure-attribution
  - self-discovery
  - summary
aliases:
  - "Two-Track Attribution Gate Summary"
  - "Diffusion-WAM Attribution TL;DR"
  - "FIPER-Generalized Attribution Gate Summary"
  - "2x2x2 Factorial Attribution Gate Summary"
---

# Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs — Summary

> [!abstract] The paper in one paragraph
> A per-episode **2-bit attribution gate** for diffusion-WAMs, built by **generalizing [[2510.09459|FIPER]]'s dual-signal CP architecture** from single-flag detection to component-level attribution. We evaluate the gate as a **2×2×2 factorial = 8 cells** spanning: two public diffusion-WAM backbones ([[2504.02792|UWM]], [[2601.16163|Cosmos Policy]]), two label-free imagination signals ([[2503.08558|FAIL-Detect]] `logpZO` — distributional OOD via CNF density on the WM's predicted $\hat{O}_{t+1}$, a novel extension — and [[2510.07206|EigenScore]] — leading eigenvalues of the denoiser's posterior covariance, estimated via Jacobian-free subspace iteration, post-hoc on any pretrained diffusion/flow-matching model), and two action signals (FIPER-ACE, Sentinel-STAC). All cells share success-only functional CP, Bonferroni-corrected 2×2 joint calibration, and **zero failure labels**. A pre-registered S3.1 pilot gates whether the two imag signals are sufficiently decorrelated to justify the 2×2×2 expansion; if not, the design collapses to 2×2 with EigenScore demoted to ablation.

## 1. Scope

**In scope**: two diffusion-WAM backbones — [[2504.02792|UWM]] (~90M DiT, modality-independent diffusion timesteps, Robomimic + LIBERO) + [[2601.16163|Cosmos Policy]] (~2B Cosmos-Predict2 DiT, latent-frame roles, LIBERO + RoboCasa + ALOHA). Two imag anchors — FAIL-Detect `logpZO` and EigenScore (posterior-covariance spectrum, Jacobian-free). Two act anchors — FIPER-ACE and Sentinel-STAC. FIPER as structural ancestor. Per-episode diagnostic label only.

**Out of scope**: AR-video-diffusion (DreamZero); latent-only WMs (Dreamer / JEPA); Fast-WAM-class backbones that remove test-time future imagination (incompatible with both imag anchors); closed-loop updates; self-improvement; any method requiring failure labels (SAFE, Guardian, WAV, etc.).

## 2. The 2×2×2 factorial experimental grid

Each of the 8 cells instantiates the **full 2×2 attribution gate** (imag × act → 4 outcome labels) on a specific (backbone, imag-signal, act-signal) combination.

| Cell | Backbone | Imag signal | Act signal |
|---|---|---|---|
| 1 | [[2504.02792\|UWM]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2510.09459\|FIPER]]-ACE |
| 2 | [[2504.02792\|UWM]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2410.04640\|Sentinel]]-STAC |
| 3 | [[2504.02792\|UWM]] | [[2510.07206\|EigenScore]] (posterior-covariance spectrum) | [[2510.09459\|FIPER]]-ACE |
| 4 | [[2504.02792\|UWM]] | [[2510.07206\|EigenScore]] (posterior-covariance spectrum) | [[2410.04640\|Sentinel]]-STAC |
| 5 | [[2601.16163\|Cosmos Policy]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2510.09459\|FIPER]]-ACE |
| 6 | [[2601.16163\|Cosmos Policy]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2410.04640\|Sentinel]]-STAC |
| 7 | [[2601.16163\|Cosmos Policy]] | [[2510.07206\|EigenScore]] (posterior-covariance spectrum) | [[2510.09459\|FIPER]]-ACE |
| 8 | [[2601.16163\|Cosmos Policy]] | [[2510.07206\|EigenScore]] (posterior-covariance spectrum) | [[2410.04640\|Sentinel]]-STAC |

**Shared benchmark for cross-cell comparison**: LIBERO (only overlap between the two backbones). **Backbone-native secondaries**: Robomimic (UWM-only) + RoboCasa (Cosmos Policy-only).

**Why two imag signals are structurally independent** (precondition for the 2×2×2 design):

| Axis | FAIL-Detect `logpZO` | EigenScore |
|---|---|---|
| Signal type | Density on noise latent of a trained CNF | Leading eigenvalues of the denoiser's posterior covariance $\Sigma(x_t) = \sigma_t^2\,\partial_x D_\theta(x_t, \sigma_t)$ |
| Space | Noise-space $\log p(Z_{\hat{O}})$ (value / likelihood) | Local curvature / posterior-covariance spectrum (geometry) |
| What it detects | "Is $\hat{O}_{t+1}$ off the success manifold?" | "Is the denoiser's local curvature at $\hat{O}_{t+1}$ inflated (high covariance → OOD)?" |
| Randomness | Single forward pass | Jacobian-free subspace iteration: $k_\text{ev}$ eigvecs × $n_\text{iter}$ central-difference power steps × $n_\text{ts}$ timesteps, all forward evals only |

These are orthogonal signal families — **density (value-based)** vs. **spectral curvature (Hessian-like, geometry-based)**. H5 tests this decorrelation empirically at S3.1.

Gate output in every cell is the 4-cell attribution label:

| | low $R_{\text{act}}$ | high $R_{\text{act}}$ |
|---|---|---|
| **low $R_{\text{imag}}$** | Success | Action failure |
| **high $R_{\text{imag}}$** | Imagination failure | Joint failure |

## 3. Delta vs. FIPER

> [!tip] Our method = FIPER with five concrete upgrades
> FIPER is the structural ancestor; we generalize its dual-signal CP detector for diffusion-WAM attribution and validate the generalization across two backbones × two imag signals × two act signals.

| | [[2510.09459\|FIPER]] | This work |
|---|---|---|
| Output | Single binary flag (RND-OE ∧ ACE) | **2-bit structured attribution label** |
| Imag signal | Policy-observation RND-OE | **Two WM-prediction-native signals**: `logpZO` (density) + EigenScore (posterior-covariance spectrum) |
| Act signal | ACE alone | ACE + STAC (both tested) |
| Combination rule | AND-gate (collapses disagreement) | **2×2 cross-tabulation** (preserves disagreement as attribution) |
| Joint FPR control | Marginal CP per axis | **Bonferroni α/2** joint correction |
| Backbone | Generative policies only | **Two diffusion WAMs** as a 2×2×2 factorial grid |

## 4. Hypotheses

| ID | Claim | Target |
|---|---|---|
| **H1** | Top-1 attribution accuracy on injected-failure suite, **winning cell** (4-class `{00, 01, 10, 11}`; chance = 25%) | Target **≥ 75%**; pre-registered floor **≥ 70%** |
| **H2** | Signal decorrelation $\rho(R_{\text{imag}}, R_{\text{act}})$ per cell, on 500 success rollouts | < 0.7 in at least one cell per (backbone, imag-signal) combination |
| **H3** | Detection AUROC (4-cell collapsed to fail/succeed) on winning cell | Match FIPER's published TWA (0.65) / overall acc (0.78) within 3 pp |
| **H4** | Cross-cell generality (descriptive at n=2 backbones; see Prop. 12.2 of math doc) | **Primary test**: both backbones hit ≥ 3 of 4 cells at Top-1 ≥ 70% (cluster-robust). **Descriptive secondary**: Top-1 ≥ 70% in ≥ 6 of 8 cells overall (anti-conservative under naive Bin(8, π) because within-backbone cells share calibration data, $n_\text{eff} \in [2, 8]$) |
| **H5** | Imag-axis internal decorrelation $\rho_{\text{Spearman}}(R_{\text{logpZO}}, R_{\text{EigenScore}})$ (Spearman primary; Pearson as secondary) | < 0.6 on **100 success rollouts per backbone** (both UWM and Cosmos Policy) — **precondition for the 2×2×2 design** (validated at S3.1 dual-backbone pilot) |

## 5. Effectiveness / efficiency envelope

**The headline** — FIPER-generalized 2×2 gate delivers **≥ 75% Top-1 attribution (3.0× chance)** with **≤ 20% compute overhead** on top of published anchor heads, in at least one (backbone, imag-signal, act-signal) configuration, using **zero failure labels**.

| Dimension | Target | Source |
|---|---|---|
| Attribution Top-1, winning cell | ≥ 75% (target); ≥ 70% (floor) | Novel; derived from Claim B row-recall floor under uniform priors (§10 of math doc) |
| Per-cell recall on `10` AND `01` | ≥ 0.60 each (Claim B floor); ≥ 0.75 stretch | Cross-side non-leakage (load-bearing ablation) |
| Detection AUROC parity with FIPER | Within 3 pp | FIPER headline |
| UWM overhead per step (logpZO, ACE) | ≈ 1–2% | CNF forward + parameter-free ACE |
| UWM overhead per step (logpZO, STAC-256) | ≈ 5–10% | Small WM amortizes 256 samples |
| UWM overhead per step (EigenScore $k_\text{ev}$=5, $n_\text{iter}$=3, $n_\text{ts}$=5, ACE) | ≈ 3–6% | ~150 extra central-difference NFEs, forward-only |
| UWM overhead per step (EigenScore, STAC-256) | ≈ 8–15% | |
| Cosmos Policy overhead per step (logpZO, ACE) | ≈ 1–2% | CNF on 2B DiT |
| Cosmos Policy overhead per step (logpZO, STAC-256) | ≈ 10–20% | 2B sampling dominates |
| Cosmos Policy overhead per step (EigenScore, ACE) | ≈ 6–12% | 2B denoiser central-difference |
| Cosmos Policy overhead per step (EigenScore, STAC-256) | ≈ 16–32% | Most expensive cell |
| STAC-single fallback (any cell) | ≈ 1–2% overhead saved | [[2506.09937\|SAFE]]'s single-sample protocol |

## 6. Experiments

**Benchmarks** (dictated by backbone overlap):

| Benchmark | UWM supports? | Cosmos Policy supports? | Role |
|---|---|---|---|
| **LIBERO** | ✓ (via robomimic harness + LIBERO-90 pretrain + downstream task finetuning per UWM README §LIBERO Experiments) | ✓ (LIBERO-10/90) | **Shared headline** — enables cross-cell comparison across all 8 cells |
| **Robomimic** (Square, Transport, Can) | ✓ | ✗ | UWM-only secondary (cells 1–4) |
| **RoboCasa** | ✗ | ✓ | Cosmos Policy-only secondary (cells 5–8) |

3 seeds per (cell, benchmark). Push-T and RoboTwin 2.0 dropped — neither backbone evaluates on them natively.

**Headline baselines**:

| | Baseline | Needs labels? |
|---|---|---|
| Detection | FIPER AND-gate (RND-OE ∧ ACE) | No |
| Detection | FAIL-Detect `logpZO` alone on $O_t$ (native use) | No |
| Detection | EigenScore alone on $\hat{O}_{t+1}$ | No |
| Detection | Sentinel STAC alone | No |
| Detection | [[2602.16182\|WM Failure Classifier]] (success / known-failure / OOD + CP) | **Yes** |
| Detection | **B-SAFE** ([[2506.09937\|SAFE]] MLP/LSTM probe + CP) | **Yes** |
| Attribution | [[2604.01985\|WAV]] forward-inverse (latent-WM, sparse-IDM) | **Yes** |
| **Ours (M)** | 2×2 gate (per cell of the 2×2×2 factorial) | **No** |

**Metrics**: max-so-far ROC-AUC, TPR, TNR, Balanced Accuracy, T-det (detection) + Top-1 cell accuracy, per-cell 4×4 confusion matrix, macro-F1 (attribution).

## 7. Execution steps

| # | Step | ★ |
|---|---|---|
| S1 | Reproduce anchor numbers within 3 pp (FIPER ACE on Push-T; FAIL-Detect `logpZO(O_t)` on Robomimic; EigenScore on CIFAR-10/100 + SVHN; STAC on Push-T) + reproduce backbone numbers (UWM + Cosmos Policy on LIBERO) | ★ reproduction gate |
| S1.1 | **LIBERO eval-protocol alignment** — reconcile task split, held-out set, and preprocessing between UWM (robomimic harness) and Cosmos Policy (`experiments/robot/libero/`) into one shared eval spec | ★ (needed before H4 is apples-to-apples) |
| S2 | Port `logpZO` to both backbones' predicted $\hat{O}_{t+1}$ (two CNFs) + port EigenScore central-difference subspace iteration with per-backbone Tweedie reconstructions (UWM DDPM-VP; Cosmos Policy rectified-flow); calibrate ($k_\text{ev}$, $n_\text{iter}$, $n_\text{ts}$) on success rollouts per backbone | |
| S3 | Wire both act signals (ACE + STAC) to both backbones' action outputs — 8 cells staged (generalize FIPER-ACE + Sentinel-STAC to 7-DoF per R5) | |
| **S3.1 ★** | **Imag-axis decorrelation pilot — dual-backbone** — 100 success rollouts on **both** UWM and Cosmos Policy; measure Spearman $\rho_S$ per backbone. Decision: ρ_S<0.6 on both → commit 2×2×2; ρ_S>0.85 on either → demote EigenScore, stay 2×2; middle → proceed with caveat | ★ **H5 kill/demote gate** |
| S4 | **8-cell act-imag decorrelation pilot — select winning cell** — 500 success rollouts per committed cell | ★ kill gate |
| S5 | Synthetic injected-failure suite (500 traj × 4 attribution classes × 2 backbones = 4000) | |
| S6 | Baseline roster on both backbones | |
| S7 | Full benchmark run — LIBERO (all committed cells) + Robomimic (UWM cells) + RoboCasa (Cosmos cells) | ★ kill gate |
| S8 | Decorrelation + joint-FPR + cross-side-leakage analyses, per cell + across cells | |
| S9 | Ablations (Bonferroni vs. copula, proprio-gated act-signal, α sweep, `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})`, EigenScore ($k_\text{ev}$, $n_\text{iter}$, $n_\text{ts}$) sensitivity, single leading eigenvalue vs. top-$k$ trace, backbone ablation) | |
| S10 | Write-up — headline = winning cell; generality finding = H4 across committed cells | |

## 8. Kill gates

- **S1** — anchor or backbone reproduction fails by > 3 pp → debug before proceeding.
- **S3.1** — Spearman $\rho_S(R_{\text{logpZO}}, R_{\text{EigenScore}}) > 0.85$ on **either** UWM or Cosmos Policy (100 rollouts per backbone) → demote EigenScore to S9 ablation; plan collapses to 2×2 (4 cells). Commit to 2×2×2 requires $\rho_S < 0.6$ on **both** backbones.
- **S4** — all committed cells have $\rho(R_{\text{imag}}, R_{\text{act}}) > 0.7$ → pivot to Plan B (single-axis detection paper, Foundational-WM reimplementation).
- **S7** — winning cell's Top-1 attribution < 70% → pivot to detection-only workshop paper.

## 9. Top risks

- **R1 — `logpZO(\hat{O}_{t+1})` is an unvalidated extension of FAIL-Detect.** FAIL-Detect's `train.py` takes `observation = x_batch` = real $O_t$; no predicted-frame path. *Mitigation*: S9 ablation comparing `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})` on both backbones; honest "novel contribution" framing throughout the paper.
- **R2 — Cross-side non-leakage has zero anchor-paper support on diffusion-WAMs.** Both UWM and Cosmos Policy use shared-weight decoupling (timestep / latent-role), not AdaWorldPolicy's distinct-weight-module separation. *Mitigation*: Per-cell recall on injected-failure suite; proprio-gated ACE/STAC ablation; the 2×2×2 factorial reveals whether leakage is backbone-/imag-signal-/act-signal-specific.
- **R3 — No prior ρ(imag, act) number exists.** H2 requires first-light measurement per cell. *Mitigation*: S4 pilot on public anchor data before committing backbone compute.
- **R7 — Benchmark overlap between backbones is limited to LIBERO.** *Mitigation*: backbone-native secondaries (Robomimic, RoboCasa) provide per-backbone depth; H4 claimed within LIBERO.
- **R8 — Compute ≈ 2× vs. 2×2 plan, ≈ 4× vs. original single-backbone plan.** *Mitigation*: S3.1 pilot may collapse to 4 cells; UWM cells first; small-($k_\text{ev}$, $n_\text{iter}$, $n_\text{ts}$) EigenScore config on Cosmos; STAC-single fallback; drop Cell 8 (2B × EigenScore × STAC-256) first if forced to cut.
- **R9 — EigenScore's posterior-covariance identity is EDM-native; each backbone needs its own Tweedie reformulation.** UWM is DDPM ε-prediction (VP schedule); Cosmos Policy is rectified flow. Neither is EDM. Per-backbone Tweedie reconstructions and spectral operators are derived in math doc §2.2/§4.2 — UWM's is close to a standard DDPM x0-Tweedie (minor $1/\alpha_t^2$ prefactor), Cosmos Policy's requires a velocity ↔ score bridge with correct signal-scaling. *Mitigation*: S2 numerically validates per-backbone identities; S9 ablation single-$\lambda_1$ vs. top-$k$ trace; restrict timestep sampling to mid-range to avoid schedule singularities; use each backbone's own scheduler API for $(\alpha, \sigma)$ lookup.
- **R10 — Imag-axis redundancy collapses 2×2×2 to 2×2.** If logpZO and EigenScore agree too strongly, the second imag anchor is redundant. *Mitigation*: S3.1 pilot gate is the explicit mitigation; pre-registered Spearman threshold ρ > 0.85 on 100 rollouts per backbone triggers the demote-to-ablation path. (Expected to be lower risk than with DIFF-UQ because EigenScore's spectral signal is a fundamentally different signal family from `logpZO`'s density.)
- **R11 — Both signals sit near CP thresholds on real (subtle) failures; gate collapses to detection (HIGH).** Real manipulation failures (near-misses, subtle physics errors) may produce signals in the 80–95 percentile of success — enough to worry a human but below the α=0.10 CP cutoff. *Mitigation*: §5.3.4 must report the full joint distribution $(R_\text{imag}, R_\text{act})$ on natural failures, not just gate labels; supplement with a soft-scoring variant.
- **R12 — Real failures are ≥ 80% mixed (class `11`); 4-cell label effectively 2-class (MED-HIGH).** If natural failures concentrate in `11` (both signals fire), the attribution USP degrades to detection-with-extra-bit. *Mitigation*: cheap LIBERO-Plus probe at S1 to estimate class-balance on natural failures; kill gate if `11` > 80%.

## 10. Where to find more

- **Full roadmap** → [[02_Self-Discovering-WAM-Roadmap]] — §3 dual-backbone + dual-imag architecture, §4 2×2×2 factorial, §4.2 Bonferroni derivation, §5.2 full baseline roster, §5.3.2 output-token-level injection protocol, §6 execution steps (S1.1 LIBERO alignment, S3.1 dual-backbone pilot), §7 kill criteria, §8 twelve-risk register.
- **Literature scan** → [[01_Self-Discovering-WAM-Literature]] — anchor-elevation paragraph, EigenScore's role as second imag anchor, backbone selection rationale, full three-bucket survey.

---

*Companion summary to [[01_Self-Discovering-WAM-Literature]] and [[02_Self-Discovering-WAM-Roadmap]].*
