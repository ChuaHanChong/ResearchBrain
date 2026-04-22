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
  - "2x2 Factorial Attribution Gate Summary"
---

# Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs — Summary

> [!abstract] The paper in one paragraph
> A per-episode **2-bit attribution gate** for diffusion-WAMs, built by **generalizing [[2510.09459|FIPER]]'s dual-signal CP architecture** from single-flag detection to component-level attribution. We evaluate the gate as a **2×2 factorial = 4 cells** spanning: two public diffusion-WAM backbones ([[2504.02792|UWM]] DDPM-VP, [[2601.16163|Cosmos Policy]] rectified-flow), one label-free imagination signal ([[2503.08558|FAIL-Detect]] `logpZO` — distributional OOD via CNF density on the WM's predicted $\hat{O}_{t+1}$, a novel extension), and two action signals (FIPER-ACE, Sentinel-STAC). All cells share success-only functional CP, Bonferroni-corrected 2×2 joint calibration, and **zero failure labels**. Cross-cell generality is claimed on LIBERO across both backbones.

## 1. Scope

**In scope**: two diffusion-WAM backbones — [[2504.02792|UWM]] (~90M DiT, DDPM ε-prediction VP schedule, modality-independent diffusion timesteps, Robomimic + LIBERO) + [[2601.16163|Cosmos Policy]] (~2B Cosmos-Predict2 DiT, rectified-flow, latent-frame roles, LIBERO + RoboCasa + ALOHA). One imag anchor — FAIL-Detect `logpZO` extended to $\hat{O}_{t+1}$. Two act anchors — FIPER-ACE and Sentinel-STAC. FIPER as structural ancestor. Per-episode diagnostic label only.

**Out of scope**: AR-video-diffusion (DreamZero); latent-only WMs (Dreamer / JEPA); Fast-WAM-class backbones that remove test-time future imagination (incompatible with `logpZO`); closed-loop updates; self-improvement; any method requiring failure labels (SAFE, Guardian, WAV, etc.); second imag signal (explored — all candidates structurally distinct from `logpZO` lack robotics/VLA validation; deferred to publication #2).

## 2. The 2×2 factorial experimental grid

Each of the 4 cells instantiates the **2×2 attribution gate** (imag × act → 4 outcome labels) on a specific (backbone, act-signal) combination.

| Cell | Backbone | Imag signal | Act signal |
|---|---|---|---|
| 1 | [[2504.02792\|UWM]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2510.09459\|FIPER]]-ACE |
| 2 | [[2504.02792\|UWM]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2410.04640\|Sentinel]]-STAC |
| 5 | [[2601.16163\|Cosmos Policy]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2510.09459\|FIPER]]-ACE |
| 6 | [[2601.16163\|Cosmos Policy]] | [[2503.08558\|FAIL-Detect]] `logpZO` | [[2410.04640\|Sentinel]]-STAC |

(Cell numbers 1/2/5/6 preserved from prior design drafts so intermediate artifacts map cleanly; cells 3/4/7/8 were second-imag-signal cells and are dropped.)

**Shared benchmark for cross-cell comparison**: LIBERO (only overlap between the two backbones). **Backbone-native secondaries**: Robomimic (UWM-only) + RoboCasa (Cosmos Policy-only).

Gate output in every cell is the 4-cell attribution label:

| | low $R_{\text{act}}$ | high $R_{\text{act}}$ |
|---|---|---|
| **low $R_{\text{imag}}$** | Success | Action failure |
| **high $R_{\text{imag}}$** | Imagination failure | Joint failure |

## 3. Delta vs. FIPER

> [!tip] Our method = FIPER with four concrete upgrades
> FIPER is the structural ancestor; we generalize its dual-signal CP detector for diffusion-WAM attribution and validate the generalization across two backbones × two act signals.

| | [[2510.09459\|FIPER]] | This work |
|---|---|---|
| Output | Single binary flag (RND-OE ∧ ACE) | **2-bit structured attribution label** |
| Imag signal | Policy-observation RND-OE | **WM-prediction-native `logpZO`** on $\hat{O}_{t+1}$ (novel extension of [[2503.08558\|FAIL-Detect]]) |
| Act signal | ACE alone | ACE + STAC (both tested) |
| Combination rule | AND-gate (collapses disagreement) | **2×2 cross-tabulation** (preserves disagreement as attribution) |
| Joint FPR control | Marginal CP per axis | **Bonferroni α/2** joint correction |
| Backbone | Generative policies only | **Two diffusion WAMs** as a 2×2 factorial grid |

## 4. Hypotheses

| ID | Claim | Target |
|---|---|---|
| **H1** | Top-1 attribution accuracy on injected-failure suite, **winning cell** (4-class `{00, 01, 10, 11}`; chance = 25%) | Target **≥ 75%**; pre-registered floor **≥ 70%** |
| **H2** | Signal decorrelation $\rho(R_{\text{imag}}, R_{\text{act}})$ per cell, on 500 success rollouts | < 0.7 in at least one cell per (backbone, act-signal) combination |
| **H3** | Detection AUROC (4-cell collapsed to fail/succeed) on winning cell | Match FIPER's published TWA (0.65) / overall acc (0.78) within 3 pp |
| **H4** | Cross-cell generality (descriptive at n=2 backbones; see Prop. 11.2 of math doc) | **Primary test**: both backbones independently hit $\geq$ 1 of 2 cells at Top-1 ≥ 70% (cluster-robust). **Descriptive secondary**: Top-1 ≥ 70% in ≥ 3 of 4 cells overall |

## 5. Effectiveness / efficiency envelope

**The headline** — FIPER-generalized 2×2 gate delivers **≥ 75% Top-1 attribution (3.0× chance)** with **≤ 20% compute overhead** on top of published anchor heads, in at least one (backbone, act-signal) configuration, using **zero failure labels**.

| Dimension | Target | Source |
|---|---|---|
| Attribution Top-1, winning cell | ≥ 75% (target); ≥ 70% (floor) | Novel; derived from Claim B row-recall floor under uniform priors (§9 of math doc) |
| Per-cell recall on `10` AND `01` | ≥ 0.60 each (Claim B floor); ≥ 0.75 stretch | Cross-side non-leakage (load-bearing ablation) |
| Detection AUROC parity with FIPER | Within 3 pp | FIPER headline |
| UWM overhead per step (logpZO, ACE) | ≈ 1–2% | CNF forward + parameter-free ACE |
| UWM overhead per step (logpZO, STAC-256) | ≈ 5–10% | Small WM amortizes 256 samples |
| Cosmos Policy overhead per step (logpZO, ACE) | ≈ 1–2% | CNF on 2B DiT |
| Cosmos Policy overhead per step (logpZO, STAC-256) | ≈ 10–20% | 2B sampling dominates; most expensive cell |
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
| Detection | FAIL-Detect full ensemble (logpZO + logpO + RND, CDF-combined) on $\hat{O}_{t+1}$ | No |
| Detection | Sentinel STAC alone | No |
| Detection | [[2602.16182\|WM Failure Classifier]] (success / known-failure / OOD + CP) | **Yes** |
| Detection | **B-SAFE** ([[2506.09937\|SAFE]] MLP/LSTM probe + CP) | **Yes** |
| Attribution | [[2604.01985\|WAV]] forward-inverse (latent-WM, sparse-IDM) | **Yes** |
| **Ours (M)** | 2×2 gate (per cell of the 2×2 factorial) | **No** |

**Metrics**: max-so-far ROC-AUC, TPR, TNR, Balanced Accuracy, T-det (detection) + Top-1 cell accuracy, per-cell 4×4 confusion matrix, macro-F1 (attribution).

## 7. Execution steps

| # | Step | ★ |
|---|---|---|
| S1 | Reproduce anchor numbers within 3 pp (FIPER ACE on Push-T; FAIL-Detect `logpZO(O_t)` on Robomimic; STAC on Push-T) + reproduce backbone numbers (UWM + Cosmos Policy on LIBERO) | ★ reproduction gate |
| S1.1 | **LIBERO eval-protocol alignment** — reconcile task split, held-out set, and preprocessing between UWM (robomimic harness) and Cosmos Policy (`experiments/robot/libero/`) into one shared eval spec | ★ (needed before H4 is apples-to-apples) |
| S2 | Port `logpZO` to both backbones' predicted $\hat{O}_{t+1}$ (two CNFs); verify CNF convergence on each backbone's $\hat{O}_{t+1}$ distribution | |
| S3 | Wire both act signals (ACE + STAC) to both backbones' action outputs — 4 cells staged (generalize FIPER-ACE + Sentinel-STAC to 7-DoF per R5) | |
| S4 | **4-cell act-imag decorrelation pilot — select winning cell** — 500 success rollouts per cell | ★ kill gate |
| S5 | Synthetic injected-failure suite (500 traj × 4 attribution classes × 2 backbones = 4000) | |
| S6 | Baseline roster on both backbones | |
| S7 | Full benchmark run — LIBERO (all 4 cells) + Robomimic (UWM cells) + RoboCasa (Cosmos cells) | ★ kill gate |
| S8 | Decorrelation + joint-FPR + cross-side-leakage analyses, per cell + across cells | |
| S9 | Ablations (Bonferroni vs. copula, proprio-gated act-signal, α sweep, `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})`, CNF architecture sensitivity, backbone ablation) | |
| S10 | Write-up — headline = winning cell; generality finding = H4 across all 4 cells | |

## 8. Kill gates

- **S1** — anchor or backbone reproduction fails by > 3 pp → debug before proceeding.
- **S4** — all 4 cells have $\rho(R_{\text{imag}}, R_{\text{act}}) > 0.7$ → pivot to Plan B (single-axis detection paper, Foundational-WM reimplementation).
- **S7** — winning cell's Top-1 attribution < 70% → pivot to detection-only workshop paper.

## 9. Top risks

- **R1 — `logpZO(\hat{O}_{t+1})` is an unvalidated extension of FAIL-Detect.** FAIL-Detect's `train.py` takes `observation = x_batch` = real $O_t$; no predicted-frame path. *Mitigation*: S9 ablation comparing `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})` on both backbones; honest "novel contribution" framing throughout the paper.
- **R2 — Cross-side non-leakage has zero anchor-paper support on diffusion-WAMs.** Both UWM and Cosmos Policy use shared-weight decoupling (timestep / latent-role), not AdaWorldPolicy's distinct-weight-module separation. *Mitigation*: Per-cell recall on injected-failure suite; proprio-gated ACE/STAC ablation; the 2×2 factorial reveals whether leakage is backbone-/act-signal-specific.
- **R3 — No prior ρ(imag, act) number exists.** H2 requires first-light measurement per cell. *Mitigation*: S4 pilot on public anchor data before committing backbone compute.
- **R7 — Benchmark overlap between backbones is limited to LIBERO.** *Mitigation*: backbone-native secondaries (Robomimic, RoboCasa) provide per-backbone depth; H4 claimed within LIBERO.
- **R8 — Compute budget.** *Mitigation*: UWM cells first; STAC-single fallback available; drop Cell 6 (2B × STAC-256) first if forced to cut.
- **R11 — Signals sit near CP thresholds on real (subtle) failures; gate collapses to detection (HIGH).** Real manipulation failures (near-misses, subtle physics errors) may produce signals in the 80–95 percentile of success — enough to worry a human but below the α=0.10 CP cutoff. *Mitigation*: §5.3.4 must report the full joint distribution $(R_\text{imag}, R_\text{act})$ on natural failures, not just gate labels; supplement with a soft-scoring variant.
- **R12 — Real failures are ≥ 80% mixed (class `11`); 4-cell label effectively 2-class (MED-HIGH).** If natural failures concentrate in `11` (both signals fire), the attribution USP degrades to detection-with-extra-bit. *Mitigation*: cheap LIBERO-Plus probe at S1 to estimate class-balance on natural failures; kill gate if `11` > 80%.

## 10. Where to find more

- **Full roadmap** → [[02_Self-Discovering-WAM-Roadmap]] — §3 dual-backbone architecture, §4 2×2 factorial, §4.2 Bonferroni derivation, §5.2 full baseline roster, §5.3.2 output-token-level injection protocol, §6 execution steps (S1.1 LIBERO alignment), §7 kill criteria, §8 risk register.
- **Literature scan** → [[01_Self-Discovering-WAM-Literature]] — anchor-elevation paragraph, backbone selection rationale, full three-bucket survey, why we do NOT stack a second imag anchor (domain-validation gap).

---

*Companion summary to [[01_Self-Discovering-WAM-Literature]] and [[02_Self-Discovering-WAM-Roadmap]].*
