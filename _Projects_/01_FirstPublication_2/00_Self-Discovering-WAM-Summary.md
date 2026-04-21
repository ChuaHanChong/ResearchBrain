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
> A per-episode **2-bit attribution gate** for diffusion-WAMs, built by **generalizing [[2510.09459|FIPER]]'s dual-signal CP architecture** from single-flag detection to component-level attribution. We evaluate the gate as a **2×2×2 factorial = 8 cells** spanning: two public diffusion-WAM backbones ([[2504.02792|UWM]], [[2601.16163|Cosmos Policy]]), two label-free imagination signals ([[2503.08558|FAIL-Detect]] `logpZO` — distributional OOD on the WM's predicted $\hat{O}_{t+1}$, a novel extension — and [[2502.20946|DIFF-UQ]] — Bayesian last-layer Laplace + CLIP semantic likelihood, post-hoc on any pretrained diffusion model), and two action signals (FIPER-ACE, Sentinel-STAC). All cells share success-only functional CP, Bonferroni-corrected 2×2 joint calibration, and **zero failure labels**. A pre-registered S3.1 pilot gates whether the two imag signals are sufficiently decorrelated to justify the 2×2×2 expansion; if not, the design collapses to 2×2 with DIFF-UQ demoted to ablation.

## 1. Scope

**In scope**: two diffusion-WAM backbones — [[2504.02792|UWM]] (~90M DiT, modality-independent diffusion timesteps, Robomimic + LIBERO) + [[2601.16163|Cosmos Policy]] (~2B Cosmos-Predict2 DiT, latent-frame roles, LIBERO + RoboCasa + ALOHA). Two imag anchors — FAIL-Detect `logpZO` and DIFF-UQ (Laplace + CLIP). Two act anchors — FIPER-ACE and Sentinel-STAC. FIPER as structural ancestor. Per-episode diagnostic label only.

**Out of scope**: AR-video-diffusion (DreamZero); latent-only WMs (Dreamer / JEPA); Fast-WAM-class backbones that remove test-time future imagination (incompatible with both imag anchors); closed-loop updates; self-improvement; any method requiring failure labels (SAFE, Guardian, WAV, etc.).

## 2. The 2×2×2 factorial experimental grid

Each of the 8 cells instantiates the **full 2×2 attribution gate** (imag × act → 4 outcome labels) on a specific (backbone, imag-signal, act-signal) combination.

| Cell | Backbone | Imag signal | Act signal |
|---|---|---|---|
| 1 | [[2504.02792\|UWM]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2510.09459\|FIPER]]-ACE |
| 2 | [[2504.02792\|UWM]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2410.04640\|Sentinel]]-STAC |
| 3 | [[2504.02792\|UWM]] | [[2502.20946\|DIFF-UQ]] (Laplace + CLIP) | [[2510.09459\|FIPER]]-ACE |
| 4 | [[2504.02792\|UWM]] | [[2502.20946\|DIFF-UQ]] (Laplace + CLIP) | [[2410.04640\|Sentinel]]-STAC |
| 5 | [[2601.16163\|Cosmos Policy]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2510.09459\|FIPER]]-ACE |
| 6 | [[2601.16163\|Cosmos Policy]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2410.04640\|Sentinel]]-STAC |
| 7 | [[2601.16163\|Cosmos Policy]] | [[2502.20946\|DIFF-UQ]] (Laplace + CLIP) | [[2510.09459\|FIPER]]-ACE |
| 8 | [[2601.16163\|Cosmos Policy]] | [[2502.20946\|DIFF-UQ]] (Laplace + CLIP) | [[2410.04640\|Sentinel]]-STAC |

**Shared benchmark for cross-cell comparison**: LIBERO (only overlap between the two backbones). **Backbone-native secondaries**: Robomimic (UWM-only) + RoboCasa (Cosmos Policy-only).

**Why two imag signals are structurally independent** (precondition for the 2×2×2 design):

| Axis | FAIL-Detect `logpZO` | DIFF-UQ |
|---|---|---|
| Signal type | Density on noise latent of a trained CNF | Epistemic uncertainty on diffusion model's last-layer weights + CLIP semantic distance |
| Space | Noise-space $\log p(Z_{\hat{O}})$ | Last-layer weight posterior + CLIP feature space |
| What it detects | "Is $\hat{O}_{t+1}$ off the success manifold?" | "Is the model itself uncertain about generating $\hat{O}_{t+1}$?" |
| Randomness | Single forward pass | Monte-Carlo over sampled last-layer weights |

These are orthogonal signal families — distributional OOD vs. Bayesian epistemic + semantic. H5 tests this decorrelation empirically at S3.1.

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
| Imag signal | Policy-observation RND-OE | **Two WM-prediction-native signals**: `logpZO` + DIFF-UQ |
| Act signal | ACE alone | ACE + STAC (both tested) |
| Combination rule | AND-gate (collapses disagreement) | **2×2 cross-tabulation** (preserves disagreement as attribution) |
| Joint FPR control | Marginal CP per axis | **Bonferroni α/2** joint correction |
| Backbone | Generative policies only | **Two diffusion WAMs** as a 2×2×2 factorial grid |

## 4. Hypotheses

| ID | Claim | Target |
|---|---|---|
| **H1** | Top-1 attribution accuracy on injected-failure suite, **winning cell** | ≥ **80%** (chance = 25%); pre-registered floor 70% |
| **H2** | Signal decorrelation $\rho(R_{\text{imag}}, R_{\text{act}})$ per cell, on 500 success rollouts | < 0.7 in at least one cell per (backbone, imag-signal) combination |
| **H3** | Detection AUROC (4-cell collapsed to fail/succeed) on winning cell | Match FIPER's published TWA (0.65) / overall acc (0.78) within 3 pp |
| **H4** | Cross-cell generality | Top-1 ≥ 70% in **≥ 6 of 8 cells** — supports "gate is not backbone-specific and not imag-signal-specific" |
| **H5** | Imag-axis internal decorrelation $\rho_{\text{Spearman}}(R_{\text{logpZO}}, R_{\text{DIFF-UQ}})$ (Spearman primary; Pearson as secondary) | < 0.6 on **100 success rollouts per backbone** (both UWM and Cosmos Policy) — **precondition for the 2×2×2 design** (validated at S3.1 dual-backbone pilot) |

## 5. Effectiveness / efficiency envelope

**The headline** — FIPER-generalized 2×2 gate delivers **≥ 80% Top-1 attribution (3.2× chance)** with **≤ 20% compute overhead** on top of published anchor heads, in at least one (backbone, imag-signal, act-signal) configuration, using **zero failure labels**.

| Dimension | Target | Source |
|---|---|---|
| Attribution Top-1, winning cell | ≥ 80% | Novel; floor 70% |
| Per-cell recall on `10` AND `01` | ≥ 75% each | Cross-side non-leakage (load-bearing ablation) |
| Detection AUROC parity with FIPER | Within 3 pp | FIPER headline |
| UWM overhead per step (logpZO, ACE) | ≈ 1–2% | CNF forward + parameter-free ACE |
| UWM overhead per step (logpZO, STAC-256) | ≈ 5–10% | Small WM amortizes 256 samples |
| UWM overhead per step (DIFF-UQ M=1/T=25, ACE) | ≈ 3–6% | Paper-validated cheap config + CLIP-B forward |
| UWM overhead per step (DIFF-UQ M=1/T=25, STAC-256) | ≈ 8–15% | |
| Cosmos Policy overhead per step (logpZO, ACE) | ≈ 1–2% | CNF on 2B DiT |
| Cosmos Policy overhead per step (logpZO, STAC-256) | ≈ 10–20% | 2B sampling dominates |
| Cosmos Policy overhead per step (DIFF-UQ M=1/T=25, ACE) | ≈ 5–10% | 2B Laplace + CLIP |
| Cosmos Policy overhead per step (DIFF-UQ M=1/T=25, STAC-256) | ≈ 15–30% | Most expensive cell |
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
| Detection | DIFF-UQ alone on $\hat{O}_{t+1}$ | No |
| Detection | Sentinel STAC alone | No |
| Detection | [[2602.16182\|WM Failure Classifier]] (success / known-failure / OOD + CP) | **Yes** |
| Detection | **B-SAFE** ([[2506.09937\|SAFE]] MLP/LSTM probe + CP) | **Yes** |
| Attribution | [[2604.01985\|WAV]] forward-inverse (latent-WM, sparse-IDM) | **Yes** |
| **Ours (M)** | 2×2 gate (per cell of the 2×2×2 factorial) | **No** |

**Metrics**: max-so-far ROC-AUC, TPR, TNR, Balanced Accuracy, T-det (detection) + Top-1 cell accuracy, per-cell 4×4 confusion matrix, macro-F1 (attribution).

## 7. Execution steps

| # | Step | ★ |
|---|---|---|
| S1 | Reproduce anchor numbers within 3 pp (FIPER ACE on Push-T; FAIL-Detect `logpZO(O_t)` on Robomimic; DIFF-UQ on ADM/UViT; STAC on Push-T) + reproduce backbone numbers (UWM + Cosmos Policy on LIBERO) | ★ reproduction gate |
| S1.1 | **LIBERO eval-protocol alignment** — reconcile task split, held-out set, and preprocessing between UWM (robomimic harness) and Cosmos Policy (`experiments/robot/libero/`) into one shared eval spec | ★ (needed before H4 is apples-to-apples) |
| S2 | Port `logpZO` to both backbones' predicted $\hat{O}_{t+1}$ (two CNFs) + port DIFF-UQ Laplace to both backbones' last layer + fit CLIP likelihood on success rollouts + verify Laplace Hessian sample-size adequacy per backbone | |
| S3 | Wire both act signals (ACE + STAC) to both backbones' action outputs — 8 cells staged (generalize FIPER-ACE + Sentinel-STAC to 7-DoF per R5) | |
| **S3.1 ★** | **Imag-axis decorrelation pilot — dual-backbone** — 100 success rollouts on **both** UWM and Cosmos Policy; measure Spearman $\rho_S$ per backbone. Decision: ρ_S<0.6 on both → commit 2×2×2; ρ_S>0.85 on either → demote DIFF-UQ, stay 2×2; middle → proceed with caveat | ★ **H5 kill/demote gate** |
| S4 | **8-cell act-imag decorrelation pilot — select winning cell** — 500 success rollouts per committed cell | ★ kill gate |
| S5 | Synthetic injected-failure suite (500 traj × 4 attribution classes × 2 backbones = 4000) | |
| S6 | Baseline roster on both backbones | |
| S7 | Full benchmark run — LIBERO (all committed cells) + Robomimic (UWM cells) + RoboCasa (Cosmos cells) | ★ kill gate |
| S8 | Decorrelation + joint-FPR + cross-side-leakage analyses, per cell + across cells | |
| S9 | Ablations (Bonferroni vs. copula, proprio-gated act-signal, α sweep, `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})`, DIFF-UQ Laplace-only vs. CLIP-only vs. combined, backbone ablation) | |
| S10 | Write-up — headline = winning cell; generality finding = H4 across committed cells | |

## 8. Kill gates

- **S1** — anchor or backbone reproduction fails by > 3 pp → debug before proceeding.
- **S3.1** — Spearman $\rho_S(R_{\text{logpZO}}, R_{\text{DIFF-UQ}}) > 0.85$ on **either** UWM or Cosmos Policy (100 rollouts per backbone) → demote DIFF-UQ to S9 ablation; plan collapses to 2×2 (4 cells). Commit to 2×2×2 requires $\rho_S < 0.6$ on **both** backbones.
- **S4** — all committed cells have $\rho(R_{\text{imag}}, R_{\text{act}}) > 0.7$ → pivot to Plan B (single-axis detection paper, Foundational-WM reimplementation).
- **S7** — winning cell's Top-1 attribution < 70% → pivot to detection-only workshop paper.

## 9. Top risks

- **R1 — `logpZO(\hat{O}_{t+1})` is an unvalidated extension of FAIL-Detect.** FAIL-Detect's `train.py` takes `observation = x_batch` = real $O_t$; no predicted-frame path. *Mitigation*: S9 ablation comparing `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})` on both backbones; honest "novel contribution" framing throughout the paper.
- **R2 — Cross-side non-leakage has zero anchor-paper support on diffusion-WAMs.** Both UWM and Cosmos Policy use shared-weight decoupling (timestep / latent-role), not AdaWorldPolicy's distinct-weight-module separation. *Mitigation*: Per-cell recall on injected-failure suite; proprio-gated ACE/STAC ablation; the 2×2×2 factorial reveals whether leakage is backbone-/imag-signal-/act-signal-specific.
- **R3 — No prior ρ(imag, act) number exists.** H2 requires first-light measurement per cell. *Mitigation*: S4 pilot on public anchor data before committing backbone compute.
- **R7 — Benchmark overlap between backbones is limited to LIBERO.** *Mitigation*: backbone-native secondaries (Robomimic, RoboCasa) provide per-backbone depth; H4 claimed within LIBERO.
- **R8 — Compute ≈ 2× vs. 2×2 plan, ≈ 4× vs. original single-backbone plan.** *Mitigation*: S3.1 pilot may collapse to 4 cells; UWM cells first; M=1/T=25 for DIFF-UQ on Cosmos; STAC-single fallback; drop Cell 8 (2B × DIFF-UQ × STAC-256) first if forced to cut.
- **R9 — DIFF-UQ's CLIP was trained on web images, not robot scenes.** *Mitigation*: S9 ablation = Laplace-only vs. CLIP-only vs. combined; if CLIP channel harms robot-scene performance, use Laplace-only on DIFF-UQ cells.
- **R10 — Imag-axis redundancy collapses 2×2×2 to 2×2.** If logpZO and DIFF-UQ agree too strongly, the second imag anchor is redundant. *Mitigation*: S3.1 pilot gate is the explicit mitigation; pre-registered Spearman threshold ρ > 0.85 on 100 rollouts triggers the demote-to-ablation path.
- **R11 — LICENSE ambiguity on DIFF-UQ and UWM repos.** Neither `metodj/DIFF-UQ` nor `WEIRDLabUW/unified-world-model` ships a LICENSE file. Research use is community norm but the legal default is "all rights reserved." *Mitigation*: fine for this publication (user has confirmed license is not a constraint for research); flag in supplementary if any code snippets are redistributed; open a GitHub issue with each author requesting explicit license before artifact release.

## 10. Where to find more

- **Full roadmap** → [[02_Self-Discovering-WAM-Roadmap]] — §3 dual-backbone + dual-imag architecture, §4 2×2×2 factorial, §4.2 Bonferroni derivation, §5.2 full baseline roster, §5.3.2 output-token-level injection protocol, §6 execution steps (S1.1 LIBERO alignment, S3.1 dual-backbone pilot), §7 kill criteria, §8 eleven-risk register.
- **Literature scan** → [[01_Self-Discovering-WAM-Literature]] — anchor-elevation paragraph, DIFF-UQ's role as second imag anchor, backbone selection rationale, full three-bucket survey.

---

*Companion summary to [[01_Self-Discovering-WAM-Literature]] and [[02_Self-Discovering-WAM-Roadmap]].*
