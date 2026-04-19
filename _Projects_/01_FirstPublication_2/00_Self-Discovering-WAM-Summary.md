---
title: "Self-Discovering Diffusion-WAM — Summary"
tags:
  - WAM
  - diffusion
  - failure-detection
  - failure-attribution
  - summary
aliases:
  - "Self-Discovering WAM Summary"
  - "Diffusion-WAM Attribution TL;DR"
---

# Self-Discovering Diffusion-WAM — Summary

> [!abstract] The paper in one paragraph
> A per-episode **diagnostic gate** for diffusion-based World Action Models that decomposes a failed rollout into **imagination failure** (the WM's next-frame prediction was wrong) vs. **action failure** (the prediction was correct but the action head chose poorly). **Self-discovery-only**: no failure-labeled data, no learned probe — just intrinsic signals from the frozen backbone plus simulator-provided observation ground truth. Instantiated across **AR-video-diffusion** ([[2602.15922|DreamZero]]) and **FM-video-diffusion** (Fast-WAM / Cosmos-Predict2 via [[2602.20057|AdaWorldPolicy]]). What to *do* with a diagnosis — retraining, residual RL, data synthesis — is explicit future work.

## 1. Scope

**In scope**: diffusion-video WAMs; discovery-only (label production, not updates); simulation-engine setting with observation ground truth.

**Out of scope**: self-improvement loops; latent-only WMs (Dreamer / JEPA — excluded by design, see full roadmap §Why Diffusion); real-robot-only methods; any method requiring labeled failure data.

## 2. The attribution gate

Two intrinsic signals, z-scored on a success-only calibration set, one-sided Functional Conformal threshold per axis. Gate output is a 4-cell label.

| | low action residual | high action residual |
|---|---|---|
| **low imag. residual** | Success | Action failure |
| **high imag. residual** | Imagination failure | Joint failure |

Signals per sub-variant:

| Sub-variant | $r_{\text{imag}}$ | $r_{\text{act}}$ | Gate frequency |
|---|---|---|---|
| **AR** ([[2602.15922\|DreamZero]]) | Pixel-MSE / LPIPS + [[2502.20946\|generative uncertainty]] (Laplace + CLIP) | Next-token entropy + [[2604.04161\|AAC]] differential entropy | Per-episode |
| **FM** (Fast-WAM / Cosmos) | Pixel-MSE / LPIPS + [[2502.20946\|generative uncertainty]] + CFG-disagreement | [[2510.25889\|Flow-SDE]] sample variance + [[2604.04161\|AAC]] | Per-step |

Optional stacks (both sub-variants): [[2603.19312|LeWM]] physics-plausibility on sim-reported poses; [[2604.01985|WAV]] sparse-IDM reachability.

## 3. Self-discovery claim vs. [[2506.09937|SAFE]]

> [!tip] Strictly stronger self-discovery than the closest prior art
> SAFE trains a small probe on *labeled failure rollouts*; we never need failure labels.

| | [[2506.09937\|SAFE]] | This work |
|---|---|---|
| Probe trained on failure labels | **Yes** (MLP/LSTM) | **No** |
| Calibration data | Success-only | Success-only (identical) |
| Failure data needed at deployment | Yes (for new-task probe) | **Never** |
| Output | Scalar failure score | Two-axis label (WM-fail, action-fail) |

## 4. Hypotheses

| ID | Claim | Target |
|---|---|---|
| **H1** | Top-1 attribution accuracy on synthetic injected-failure suite | ≥ **80%** per sub-variant (chance = 25%) |
| **H2** | Signal decorrelation $\rho(R_{\text{imag}}, R_{\text{act}})$ | < **0.7** on real rollouts |
| **H3** | AR vs. FM cross-sub-variant accuracy gap | ≤ **10 pp** |

## 5. Effectiveness / efficiency envelope

**The four-part headline** — < 10% compute overhead per episode, detection parity with supervised [[2506.09937|SAFE]], first-in-class component-level attribution at 3.2× chance, zero failure labels required.

| Dimension | Target |
|---|---|
| Detection AUROC (4-cell collapsed to fail/succeed) | Match [[2506.09937\|SAFE]] ≈ 0.85–0.90 on LIBERO unseen |
| Attribution Top-1 cell accuracy | ≥ 80% per sub-variant (chance = 25%) |
| Per-cell recall (no cross-side leakage) | ≥ 75% on cell `10` AND cell `01` |
| T-det (detection earliness) | Within 1–3 s per SAFE's protocol |
| Per-episode overhead over baseline rollout | ≈ 5–10% (FM per-step) / ≈ 1–5% (AR per-episode) |

Full analysis — including baseline-by-baseline compute comparison and three honest limitations — in [[02_Self-Discovering-WAM-Roadmap]] §4.7.

## 6. Experiments

**Benchmarks**: [[2306.03310|LIBERO]]-Plus (stresses imagination axis via visual OOD) + [[2506.18088|RoboTwin 2.0]] (stresses action axis via contact-rich manipulation). 3 seeds, 3-of-10 held-out tasks per SAFE's protocol.

**Headline baselines** (full roster in full roadmap §5.2):

| | Baseline | Needs failure labels? |
|---|---|---|
| Detection | [[2510.09459\|FIPER]] (AND-gate) | No |
| Detection | [[2506.09937\|SAFE]] probe + CP | **Yes** |
| Attribution | [[2604.01985\|WAV]] forward-inverse | Needs expert IDM data |
| Attribution | [[2512.01946\|Guardian / FailCoT]] | **Yes** (30K+ examples) |
| Attribution | [[2602.01515\|RAPT]] LLM root-cause | **Yes** |
| **Ours (M)** | 4-cell Attribution Gate | **No** |

**Metrics** (follows [[2506.09937|SAFE]] verbatim): max-so-far ROC-AUC, TPR, TNR, Balanced Accuracy, T-det, plus attribution-specific Top-1 cell accuracy, per-cell confusion matrix, macro-F1.

## 7. Execution steps

| # | Step | ★ |
|---|---|---|
| S1 | Reproduce in-distribution baselines on both sub-variants | |
| S2 | FM sub-variant signal extraction | |
| S3 | AR sub-variant signal extraction | |
| S4 | Conformal calibration + pre-registered correlation test | ★ kill gate |
| S5 | Synthetic injected-failure suite (500 traj × 4 cells × 2 sub-variants) | |
| S6 | Full baseline roster implementation (Tier 1–3) | |
| S7 | Full benchmark run per SAFE protocol | ★ kill gate |
| S8 | Signal-decorrelation + cross-sub-variant consistency analyses | |
| S9 | Ablations (per-signal, $\alpha$ sweep, rank-based cells) | |
| S10 | Write-up | |

## 8. Kill gates

- **S4**: if $\rho(R_{\text{imag}}, R_{\text{act}}) > 0.8$ on [[2602.20057|AdaWorldPolicy]] public logs → pivot to orthogonal decomposition or negative-result taxonomy paper.
- **S7**: if Top-1 attribution accuracy < 70% in both sub-variants → pivot to detection-only workshop paper.

## 9. Top 3 risks

- **R1** — signal correlation dissolves attribution (mitigated by S4 pre-reg + orthogonal decomposition plan B).
- **R2** — DreamZero compute cost for 14 B inference-only rollouts (mitigated by per-episode signal caching, reduced per-cell budget, controlled AR-downgrade).
- **R3** — cross-side leakage via shared backbone tokenizer (mitigated by freezing tokenizer; diagnosed by confusion-matrix off-diagonals).

## 10. Where to find more

- **Full roadmap** → [[02_Self-Discovering-WAM-Roadmap]] — §4.4 Why-this-works proof, §4.5 Stacking-validity argument, §4.6 Evidence chain, §5.2 full tiered baseline roster, §5.5 head-to-head competitor-by-competitor comparison, §5.3 complete metrics spec, §8 full five-risk register.
- **Literature scan** → [[01_Self-Discovering-WAM-Literature]] — §Why Diffusion motivation, §Diffusion-WAM Landscape, three-bucket literature survey, §The Gap and attribution-competitor tables.

---

*Companion summary to [[01_Self-Discovering-WAM-Literature]] and [[02_Self-Discovering-WAM-Roadmap]].*
