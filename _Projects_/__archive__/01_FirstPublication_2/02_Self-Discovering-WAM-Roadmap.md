---
title: "Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs — Research Roadmap"
tags:
  - WAM
  - diffusion
  - failure-detection
  - failure-attribution
  - self-discovery
  - roadmap
aliases:
  - "Two-Track Attribution Gate Roadmap"
  - "Diffusion-WAM Self-Discovery Roadmap"
  - "FIPER-Generalized Attribution Gate Roadmap"
  - "2x2 Factorial Attribution Gate Roadmap"
---

# Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs — Research Roadmap

> [!abstract] What This Document Is
> A step-ordered plan for a **per-episode 2-bit attribution gate** for diffusion-WAMs, evaluated as a **2×2 factorial = 4 cells**: two diffusion-WAM backbones × two act signals, with one WM-prediction-native imag signal. The method generalizes [[2510.09459|FIPER]]'s dual-signal CP detector to component-level attribution. **Imag anchor**: [[2503.08558|FAIL-Detect]] `logpZO` (distributional OOD via CNF density, novel extension to $\hat{O}_{t+1}$). **Act anchors**: FIPER-ACE + [[2410.04640|Sentinel]]-STAC. **Backbones**: [[2504.02792|UWM]] (~90M, DDPM-VP) + [[2601.16163|Cosmos-Policy]] (~2B, rectified-flow). Success-only functional CP, Bonferroni-corrected joint FPR, zero failure labels. Second imag signal, AR sub-variant, multi-component stacks, and closed-loop updates are deferred to publication #2.

> [!info] One-Line Pitch
> FIPER, but (a) WM-prediction-native `logpZO` on $\hat{O}_{t+1}$ (novel extension of FAIL-Detect), (b) two act signals (ACE + STAC), (c) AND-gate → Bonferroni-corrected 2×2 cross-tabulation, (d) validated across **two diffusion-WAM backbones** as a 2×2 factorial.

---

## 0. Instantiation — 2×2 factorial interface

> [!tip] The diagnostic grid in one table
> Four cells. All share success-only functional CP with Bonferroni α/2. Cells differ on (backbone, act signal). S4 selects winning cell on H2 decorrelation.

| Cell | Backbone | Imag signal | Act signal | Public code |
|---|---|---|---|---|
| **1** | [[2504.02792\|UWM]] (~90M) | [[2503.08558\|FAIL-Detect]] `logpZO` | FIPER-ACE | UWM + FIPER + FAIL-Detect |
| **2** | [[2504.02792\|UWM]] (~90M) | [[2503.08558\|FAIL-Detect]] `logpZO` | Sentinel-STAC | UWM + Sentinel + FAIL-Detect |
| **5** | [[2601.16163\|Cosmos-Policy]] (~2B) | [[2503.08558\|FAIL-Detect]] `logpZO` | FIPER-ACE | Cosmos + FIPER + FAIL-Detect |
| **6** | [[2601.16163\|Cosmos-Policy]] (~2B) | [[2503.08558\|FAIL-Detect]] `logpZO` | Sentinel-STAC | Cosmos + Sentinel + FAIL-Detect |

(Cell numbers 1/2/5/6 preserved from prior design drafts so intermediate artifacts and git history map cleanly; cells 3/4/7/8 were second-imag-signal cells and are dropped in this revision.)

Shared across all cells:

| Axis | Instantiation |
|---|---|
| $r_{\text{imag}}(\tau)$ | `logpZO` applied to backbone's predicted next-frame $\hat{O}_{t+1}$ |
| Calibration | Success-only functional CP + Bonferroni α/2 per axis for joint FPR |
| Gate output | 4-cell attribution label via 2×2 cross-tabulation |

### Why two backbones — and why these two

[[2503.08558|FAIL-Detect]]'s `logpZO` requires a predicted next-frame $\hat{O}_{t+1}$ at inference, so any backbone that removes test-time imagination (e.g., [[2603.16666|Fast-WAM]]) is structurally ruled out. AdaWorldPolicy (2602.20057) would have been the ideal backbone — distinct WM and action weight modules — but has no public code. Among public diffusion-WAMs with preserved future imagination:

- **[[2504.02792|UWM]]** (~90M): one shared DiT with **modality-independent diffusion timesteps** for video and action. DDPM ε-prediction, VP schedule.
- **[[2601.16163|Cosmos-Policy]]** (~2B): one shared Cosmos-Predict2 DiT with **distinct latent-frame roles** for action / future-image / value tokens. Rectified flow.

Neither has AdaWorldPolicy-style distinct-weight-module separation. Both are coupled through shared backbone weights + shared visual tokenizers. The 2×2 factorial spans two backbone coupling mechanisms × two act signals, testing generality of the imag-vs-act separation across both architectures.

### Why one imag signal, not two

The imag axis uses `logpZO` alone. A second structurally-distinct imag signal was explored across four candidate rounds ([[2502.20946|DIFF-UQ]], [[2510.07206|EigenScore]], [[2504.07793|RDM]], [[2508.05461|rFM/WT-Flow]]); every candidate with public code has been **validated only on image-OOD benchmarks** (CIFAR / ImageNet / MVTec / VisA), not on VLA / WAM predicted frames. Committing 2B-DiT compute to an unvalidated posterior-covariance signal on robot scenes is too risky for a first publication. The second imag anchor is **explicitly deferred to publication #2** once robot-validated spectral or epistemic signals exist. This choice:
- Removes H5 (imag-axis decorrelation precondition) from the hypothesis list
- Removes S3.1 (imag-axis decorrelation pilot) from the execution plan
- Removes R9/R10 (EDM-to-FM reformulation risks; imag-axis redundancy) from the risk register
- Keeps the headline 2×2 attribution gate + 4-cell backbone-generality claim intact

### Why continuous-diffusion only, not AR

`logpZO` requires a Gaussian-noising observation decoder — UWM's DDPM $\varepsilon$-predictor and Cosmos Policy's rectified-flow velocity field both qualify, though they use different schedules and parameterizations (see math doc §2). [[2602.15922|DreamZero]]'s AR categorical token stream would require a softmax-density adaptation — deferred to publication #2.

### Self-discovery — strictly zero failure labels

| Paper | Failure labels? | Role |
|---|---|---|
| [[2503.08558\|FAIL-Detect]] | No (success-only CP on noise-latent density) | Imag anchor (all 4 cells) |
| [[2510.09459\|FIPER]] | No (success-only CP; ACE + RND-OE) | Structural ancestor + ACE act anchor (Cells 1, 5) |
| [[2410.04640\|Sentinel]] | No (STAC calibrated on success rollouts) | STAC act anchor (Cells 2, 6) |
| [[2504.02792\|UWM]] | No (pretrained WM; we don't retrain) | Backbone A |
| [[2601.16163\|Cosmos-Policy]] | No (pretrained NVIDIA checkpoints) | Backbone B |
| [[2506.09937\|SAFE]] | **Yes** | Baseline only (B-SAFE) |
| [[2604.01985\|WAV]] | **Yes** | Baseline only (B-WAV) |
| [[2602.16182\|WM-Failure-Classifier]] | **Yes** | Baseline only (B-WMFC) |

---

## 1. Research Question

> [!question] Central question
> Can [[2510.09459|FIPER]]'s dual-signal success-only CP architecture be generalized to a per-episode 2-bit attribution gate on diffusion-WAMs by (a) replacing its policy-observation OOD signal with a WM-prediction-native imag signal (`logpZO` on $\hat{O}_{t+1}$, novel extension of FAIL-Detect), (b) pairing it with two action signals (ACE + STAC), (c) replacing the AND-gate with a Bonferroni-corrected 2×2 cross-tabulation, and (d) demonstrating generality **across two diffusion-WAM backbones as a 2×2 factorial** — with no failure labels?

---

## 2. Testable Hypotheses

> [!tip] H1 — Attribution accuracy, winning cell
> On 500 × 4-cell synthetic injected failures (uniform class priors), the winning cell of the 2×2 factorial achieves $\geq 75\%$ Top-1 cell accuracy. Pre-registered floor: 70%. §9.2 of the math doc relates this to Claim B's row-recall floor under joint-FPR Recall$_{00} \geq 1-\alpha$.

> [!tip] H2 — Act × imag decorrelation, per cell (decides winning cell at S4)
> On 500 success rollouts per cell: $\rho(R_{\text{imag}}, R_{\text{act}}) < 0.7$ in at least one cell per backbone. Cell with lowest ρ globally wins. If all 4 cells have $\rho > 0.7$ → pivot.

> [!tip] H3 — Detection AUROC parity with FIPER
> Winning cell's collapsed-to-binary detection AUROC matches FIPER's published numbers (TWA **0.65** / overall acc **0.78**) within 3 pp on LIBERO.

> [!tip] H4 — Cross-cell generality (2×2-native, descriptive at n=2 backbones)
> **Primary test**: both backbones independently hit ≥ 1 of 2 cells at Top-1 ≥ 70% (cluster-robust per Prop. 11.2 of the math doc).
> **Secondary (descriptive)**: Top-1 ≥ 70% in ≥ 3 of 4 cells overall. Reported but anti-conservative under naive Bin(4, π) because within-backbone cells share calibration data ($n_\text{eff} \in [2, 4]$).

---

## 3. System Architecture

> [!info] Two backbones × one imag signal × two act signals = 2×2 factorial
> All four cells share the CP calibration. Cells differ on (backbone, act signal). Cross-cell comparison on LIBERO (the only shared benchmark).

```mermaid
graph TD
    OBS["o_t, l"]

    subgraph "Backbone A: UWM (~90M, DDPM-VP)"
        OBS --> UWM["UWM DiT<br/>(ε-prediction, DDIM sampler)"]
        UWM --> OHAT_A["o_hat_t+1 (A)"]
        UWM --> ACHUNK_A["action chunk (A)"]
    end

    subgraph "Backbone B: Cosmos Policy (~2B, rectified flow)"
        OBS --> COS["Cosmos-Predict2 DiT<br/>(velocity, RF Euler sampler)"]
        COS --> OHAT_B["o_hat_t+1 (B)"]
        COS --> ACHUNK_B["action chunk (B)"]
    end

    subgraph "Imag signal — FAIL-Detect logpZO (one signal, both backbones)"
        OHAT_A --> LPZ_A["CNF density on UWM preds"]
        OHAT_B --> LPZ_B["CNF density on Cosmos preds"]
    end

    subgraph "Act signal #1 — FIPER ACE"
        ACHUNK_A --> ACE_A["ACE (UWM)"]
        ACHUNK_B --> ACE_B["ACE (Cosmos)"]
    end

    subgraph "Act signal #2 — Sentinel STAC"
        ACHUNK_A --> STAC_A["STAC (UWM)"]
        ACHUNK_B --> STAC_B["STAC (Cosmos)"]
    end

    LPZ_A --> C1{Cell 1}
    ACE_A --> C1
    LPZ_A --> C2{Cell 2}
    STAC_A --> C2
    LPZ_B --> C5{Cell 5}
    ACE_B --> C5
    LPZ_B --> C6{Cell 6}
    STAC_B --> C6

    classDef novel fill:#f0e8fd,stroke:#9b59b6
    classDef signal fill:#e8f4fd,stroke:#4a90d9
    classDef slot fill:#fdf5e8,stroke:#d9a64a
    class C1,C2,C5,C6,LPZ_A,LPZ_B novel
    class ACE_A,ACE_B,STAC_A,STAC_B signal
    class UWM,COS slot
```

---

## 4. The FIPER-Generalized Attribution Gate

### 4.1 Episode-aggregated signals (per cell)

$$R_{\text{imag}}(\tau) = \max_{t \leq T}\,s_{\text{imag}}(\hat{O}_{t+1}),\qquad R_{\text{act}}(\tau) = \max_{t \leq T}\,s_{\text{act}}(t)$$

where $s_{\text{imag}}$ is `logpZO` applied to $\hat{O}_{t+1}$ (all 4 cells) and $s_{\text{act}}$ is ACE (cells 1/5) or STAC (cells 2/6).

### 4.2 Functional CP — Bonferroni-corrected for joint coverage

Per cell. Both imag and act signals use success-only functional Conformal Prediction with Bonferroni correction at level $\alpha / 2$.

**Step 1** — Per-axis per-timestep mean $\mu_t^{\text{axis}}$ on success calibration set (N = 500 per cell).

**Step 2** — Bonferroni-corrected conformal quantile → bandwidth $h_t^{\text{axis}}$.

**Step 3** — One-sided thresholds:

$$\tau_{\text{imag}}(t) = \mu_t^{\text{imag}} + h_t^{\text{imag}}/2,\qquad \tau_{\text{act}}(t) = \mu_t^{\text{act}} + h_t^{\text{act}}/2$$

**Joint guarantee** per cell: $P(R_{\text{imag}} < \tau_{\text{imag}} \wedge R_{\text{act}} < \tau_{\text{act}}) \geq 1 - \alpha$ by union bound. Each cell is calibrated independently.

Sweep $\alpha \in \{0.05, 0.10, 0.20\}$; copula-quantile variant as ablation.

### 4.3 The 4-cell attribution label (per cell of the 2×2×2 grid)

$b_{\text{imag}} = \mathbb{1}[R_{\text{imag}}(\tau) > \tau_{\text{imag}}],\quad b_{\text{act}} = \mathbb{1}[R_{\text{act}}(\tau) > \tau_{\text{act}}]$

| $b_{\text{imag}}$ | $b_{\text{act}}$ | Label |
|---|---|---|
| 0 | 0 | **Success** |
| 0 | 1 | **Action failure** |
| 1 | 0 | **Imagination failure** |
| 1 | 1 | **Joint failure** |

### 4.4 Why this works — claims and falsifiers

#### Claim A — WM-prediction-native density discriminates imag failure

> The imag signal `logpZO` assigns higher failure scores to predicted frames that are off the success-frame manifold.

**Argument**. `logpZO` is a density estimator on the success-frame manifold; FAIL-Detect validates it on real observations $O_t$ from Robomimic, with functional-CP calibration. Our extension to $\hat{O}_{t+1}$ retrains the CNF per-backbone on predicted success frames (not raw demonstrations).

**Preconditions**. `logpZO` CNFs are trained on predicted success frames per backbone (two CNFs total).

**Falsifier (S9 ablation)**: Per backbone, compare discrimination AUROC of `logpZO(O_t)` (FAIL-Detect native) vs. `logpZO(\hat{O}_{t+1})` (our extension). If predicted-frame AUROC drops below 0.70 while real-frame AUROC is ≥ 0.80, Claim A has failed for that backbone.

#### Claim B — Cross-side non-leakage (weakest claim)

> Within each cell, $r_{\text{imag}}$ responds to WM-prediction errors but NOT action-head corruption; $r_{\text{act}}$ responds to action-head uncertainty but NOT WM-prediction errors.

**Argument**. Per-backbone mechanism: UWM uses modality-independent timesteps; Cosmos Policy uses distinct latent-frame roles. Neither is distinct-weight-module decoupling — so shared-tokenizer leakage is real and must be bounded empirically.

**Confounders**: (a) shared visual tokenizers feed both imag and act paths in each backbone; (b) the 2B Cosmos Policy has richer feature mixing than UWM's ~90M.

**Falsifier (§5.3.2 confusion matrix)**: per-cell recall on injected-failure suite. If cell-`10` or cell-`01` recall drops below 60% in a given cell, Claim B has failed for that cell. H4 requires Claim B to hold in ≥ 3 of 4 cells.

#### Claim C — Joint calibration under exchangeability

> Bonferroni-corrected functional CP controls joint FPR at $\alpha$ under exchangeability, per cell.

**Argument**: union bound over two marginal CP guarantees. Exchangeability holds per cell because the backbone and both signal paths are frozen.

**Falsifier**: empirical joint FPR on held-out success set, per cell. If FPR $> \alpha + 0.03$ in a cell, switch to copula-based joint quantile for that cell.

---

### 4.5 Efficiency envelope (per cell)

| Component | UWM (~90M) | Cosmos Policy (~2B) |
|---|---|---|
| `logpZO` CNF forward | ≈ 1–2% | < 1% |
| ACE — dim-wise entropy | < 0.1% | < 0.1% |
| STAC-256 | ≈ 5–10% | ≈ 10–20% |
| STAC-single (fallback) | < 0.5% | < 0.2% |
| **Cell 1 (UWM × logpZO × ACE)** | **≈ 1–2%** | — |
| **Cell 2 (UWM × logpZO × STAC-256)** | **≈ 6–12%** | — |
| **Cell 5 (Cosmos × logpZO × ACE)** | — | **≈ 1–2%** |
| **Cell 6 (Cosmos × logpZO × STAC-256)** | — | **≈ 11–21%** |

STAC-single fallback available per [[2506.09937|SAFE]]'s protocol — especially for Cell 6 if 2B-STAC-256 becomes compute-bound.

### 4.6 Honest limitations

1. **`logpZO(\hat{O}_{t+1})` is unvalidated by FAIL-Detect's paper.** Repo inspection confirms `train.py` feeds `observation = x_batch` = real $O_t$; no predicted-frame path. S9 ablation is load-bearing, per backbone.
2. **No second imag signal.** Four candidate rounds found no robot-scene-validated structurally-distinct alternative; deferred to publication #2.
3. **Cross-side non-leakage has no prior empirical support** on diffusion-WAMs, and both backbones use *shared-weight* decoupling (timestep or latent-role) rather than distinct-weight-module separation.
4. **Benchmark overlap across backbones is limited to LIBERO.** Push-T and RoboTwin 2.0 dropped from headline.

---

## 5. Experiments

### 5.1 Benchmarks

| Benchmark | UWM | Cosmos Policy | Role |
|---|---|---|---|
| **LIBERO** | ✓ via robomimic harness (UWM's `eval_robomimic.py` with `dataset=libero_*.yaml`; LIBERO-90 pretrained ckpt + downstream task finetuning per README §LIBERO Experiments) | ✓ (LIBERO-10/90 via dedicated scripts in `experiments/robot/libero/`) | **Shared headline** — cross-cell H4 test across all committed cells |
| **Robomimic** (Square, Transport, Can) | ✓ | ✗ | UWM-only backbone-native secondary (Cells 1–4) |
| **RoboCasa** | ✗ | ✓ | Cosmos Policy-only backbone-native secondary (Cells 5–8) |

3 seeds per (cell, benchmark).

### 5.2 Baselines — classified by label requirement

#### Tier 1 — label-free (fair comparison)

| ID | Baseline | Side |
|---|---|---|
| **B-FIPER** | [[2510.09459\|FIPER]] AND-gate (RND-OE ∧ ACE) | Both |
| **B-LPZ-OBS** | [[2503.08558\|FAIL-Detect]] `logpZO(O_t)` (native) | Imag |
| **B-LPZ-PRED** | [[2503.08558\|FAIL-Detect]] `logpZO(\hat{O}_{t+1})` per backbone | Imag |
| **B-FAIL-FULL** | [[2503.08558\|FAIL-Detect]] full ensemble (logpZO + logpO + RND, CDF-combined) on $\hat{O}_{t+1}$ | Imag |
| **B-ACE** | FIPER-ACE alone | Act |
| **B-STAC** | Sentinel-STAC alone | Act |
| **B-FWM** | [[2603.06987\|Foundational-WM]] predicted-std (optional, reimplementation) | Imag |
| **B-NF** | [[2603.11106\|RC-NF]] nominal-only normalizing flow | Both |

#### Tier 2 — supervised baselines

| ID | Baseline | Extra supervision |
|---|---|---|
| **B-SAFE** | [[2506.09937\|SAFE]] MLP/LSTM probe + CP | Labeled success + failure rollouts |
| **B-WAV** | [[2604.01985\|WAV]] forward-inverse | Expert action data |

#### Our method

| ID | Method | Which cell |
|---|---|---|
| **M-1, M-2, M-5, M-6** | 2×2 gate, per cell of the factorial | Cells 1, 2, 5, 6 |
| **M★** | Winning cell at S4 | Headline |

### 5.3 Metrics

#### 5.3.1 Detection metrics (from SAFE)

Max-so-far score, ROC-AUC, TPR/TNR, Balanced Accuracy, T-det. Collapse 4-cell → `{00, 01/10/11}` for comparison. Reported per cell.

#### 5.3.2 Attribution metrics — injection at output-token level (not weight-module level)

Synthetic injected-failure suite: 500 × 4 attribution classes × 2 backbones = 4000 trajectories.

**Why output-token injection, not weight-module injection**: neither UWM nor Cosmos Policy has distinct WM and action weight modules (both use a single shared DiT with modality-specific outputs — UWM via modality-independent diffusion timesteps, Cosmos Policy via distinct latent-frame roles). "Gaussian noise on WM DiT weights vs. action DiT weights" — the protocol used for AdaWorldPolicy-style backbones — is **structurally undefined here**. We inject at the modality-output boundary instead.

| Class | Injection site | GT |
|---|---|---|
| Clean | None | `00` |
| Imag corruption | Gaussian noise on DiT's **video-output tokens** (UWM: video-modality outputs; Cosmos Policy: future-image role tokens) mid-episode | `10` |
| Act corruption | Gaussian noise on DiT's **action-output tokens** (UWM: action-modality outputs; Cosmos Policy: action role tokens) mid-episode | `01` |
| Joint | Both simultaneously | `11` |

Noise scale calibrated per backbone: sweep σ ∈ {0.1, 0.5, 1.0} × per-token activation std on the injection-site tokens. Pre-register chosen σ before S5 based on the lowest σ that produces a measurable deviation in rollout success rate on a held-out task.

**Caveat (R6 reinforced)**: output-token injection is still synthetic and may not mirror real-world failure modes (e.g., visual OOD, contact physics failures, task misinterpretation). The §5.3.5 natural-failure VLM-rated validity check is the backstop.

Metrics: Top-1 cell accuracy, per-cell precision/recall (4×4 confusion matrix), macro-F1, attribution-AUROC. Reported per cell of the 2×2×2.

#### 5.3.3 Decorrelation analysis (H2, S4)

- **H2 (S4)**: Spearman $\rho_S(R_{\text{imag}}, R_{\text{act}})$ per cell on 500 success rollouts (Pearson secondary); selects winning cell.

Spearman is the primary statistic because max-so-far episode-aggregates are heavy-tailed (Pearson's Gaussian assumption is violated). Report: full 4×4 Spearman correlation heatmap across all signals + cells, with Pearson overlay in supplementary.

#### 5.3.4 Joint-FPR analysis (Claim C)

Empirical joint FPR per cell on held-out success vs. Bonferroni-predicted $\alpha$. Copula-quantile variant as ablation.

#### 5.3.5 Cross-cell generality (H4)

Top-1 attribution across all 4 cells on LIBERO. Report: (a) "best cell" headline; (b) primary statistic — both backbones hit ≥ 1 of 2 cells at Top-1 ≥ 70% (cluster-robust per Prop. 11.2); (c) descriptive secondary — "≥ 3 of 4" raw count; (d) ρ heatmap across cells.

#### 5.3.6 Data splits

Per anchor / backbone convention. LIBERO holdout per each backbone's published split. Robomimic per FAIL-Detect. RoboCasa per Cosmos Policy. 3 seeds.

### 5.4 Pre-registered analyses

> [!warning] Pre-register before S4
> Run H2 (S4) on public anchor data (FIPER Push-T, Sentinel Push-T if feasible) before backbone compute commitment.

---

## 6. Execution Steps

Compute budget: 1× 8×H100 node. UWM cells first; commit Cosmos Policy compute only after UWM cells pass S4.

| # | Step | Deliverable | Risk |
|---|---|---|---|
| **S1** | Reproduce anchor + backbone numbers within 3 pp | FIPER ACE + AND on Push-T; FAIL-Detect `logpZO(O_t)` + full-ensemble on Robomimic; Sentinel STAC on Push-T; UWM on LIBERO-100; Cosmos Policy on LIBERO | Medium (env alignment × 4 anchors × 2 backbones) |
| **S1.1 ★** | **LIBERO eval-protocol alignment between backbones** — reconcile task split, held-out set, image preprocessing, and reporting metrics across UWM's robomimic-harness LIBERO pipeline and Cosmos Policy's `experiments/robot/libero/` pipeline. Deliverable: one shared LIBERO eval spec (`libero_shared.yaml`) that both backbones' inference scripts consume | Shared LIBERO eval harness; without this, cross-cell H4 is a cross-setup claim, not a cross-backbone claim | Medium |
| **S2** | Train `logpZO` CNFs on both backbones' $\hat{O}_{t+1}$; verify per-backbone CNF convergence on success-rollout predicted-frame distribution | 2 CNFs (per-backbone trained + calibrated) | **Medium-High** (novel extension of FAIL-Detect; predicted-frame distribution differs from native real-$O_t$ regime) |
| **S3** | Wire ACE + STAC to both backbones' action outputs — all 4 cells staged | Per-timestep $R_{\text{act}}$ logged per cell | Medium (generalize FIPER's ACE for 7-DoF actions per R5) |
| **S4 ★** | **Act × imag decorrelation pilot — select winning cell** | $\rho_c$ per cell on 500 success rollouts. Commit to winner. **UWM cells run first; Cosmos Policy cells only if at least one UWM cell passes.** | **HIGH — H2 kill criterion** |
| **S5** | Synthetic injected-failure suite on both backbones | 4000 trajectories (500 × 4 classes × 2 backbones) | Medium |
| **S6** | Baseline roster on both backbones where applicable | B-FIPER, B-LPZ-OBS, B-LPZ-PRED (×2), B-FAIL-FULL (×2), B-ACE, B-STAC, B-NF, B-SAFE, B-WAV | Medium |
| **S7 ★** | **Full benchmark run** | All 4 cells on LIBERO; UWM cells on Robomimic; Cosmos cells on RoboCasa | **HIGH — kill criterion** |
| **S8** | Decorrelation + joint-FPR + cross-side-leakage analyses, per cell | ρ heatmap across all signals × cells; per-cell Claim C empirical FPR; per-cell Claim B confusion-matrix off-diagonals | Low |
| **S9** | Ablations | `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})` (×2 backbones); CNF architecture sensitivity; Bonferroni vs. copula; proprio-gated act signal; α sweep; backbone ablation | Low |
| **S10** | Write-up | Paper — headline = winning cell; generality = H4 across 4 cells | Low |

---

## 7. Kill Criteria

> [!warning] S1 — Anchor + backbone reproduction gate
> **KILL if** any anchor or backbone fails to reproduce within 3 pp of its published number.

> [!warning] S4 — Act × imag decorrelation gate (cell selection, H2)
> **KILL if** all 4 cells have $\rho > 0.7$ AND the same holds on public anchor data.
>
> **PIVOT** to Plan B: reimplement [[2603.06987|Foundational-WM]] (~3-4 weeks) as single-axis detection paper.
>
> **PARTIAL PIVOT**: if only 1 cell has $\rho < 0.7$, proceed with that single cell as headline; withdraw H4.

> [!warning] S7 — Attribution accuracy gate
> **KILL if** winning cell's Top-1 attribution < 70%. **PIVOT** to detection-only workshop paper.

---

## 8. Risk Register

> [!warning] R1 — `logpZO(\hat{O}_{t+1})` is an unvalidated extension of FAIL-Detect
> **Severity**: HIGH. **Evidence**: `FAIL-Detect/UQ_baselines/logpZO/train.py` feeds `observation = x_batch` = real $O_t$; paper Q&A confirms no predicted-frame application.
>
> **Mitigation**: S9 ablation `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})` per backbone. Framing: novel contribution, not drop-in port.

> [!warning] R2 — Cross-side non-leakage has zero anchor-paper support, and both backbones lack distinct-weight-module decoupling
> **Severity**: HIGH.
>
> **Mitigation**: confusion-matrix off-diagonals per cell; proprio-gated ACE/STAC ablation; 2×2 factorial surfaces whether leakage is backbone-specific or act-signal-specific.

> [!warning] R3 — No prior ρ number for H2 on either backbone
> **Severity**: MEDIUM.
>
> **Mitigation**: run S4 on public data (FIPER Push-T, Sentinel Push-T, FAIL-Detect Robomimic) before committing backbone compute.

> [!warning] R4 — STAC-256 cost on 2B Cosmos Policy
> **Severity**: MEDIUM (Cell 6). Cell 6 (Cosmos × STAC-256) is the most expensive.
>
> **Mitigation**: STAC-single fallback on Cell 6 per [[2506.09937|SAFE]]. If compute forces a cut, drop Cell 6 first.

> [!warning] R5 — ACE standalone not cleanly tabulated + ACE is dimensionality-bound (not just "3-D hardcoded")
> **Severity**: **HIGH** (Cells 1, 3, 5, 7). `fiper/evaluation/method_eval_classes/entropy_eval.py:62-96` uses dim-wise histogram binning (`cell_indices_x/y/z`, `num_cells_x/y/z`). Scaling to 7-DoF action spaces is not a config flip — a 7-D joint histogram at the same resolution has ~10⁷ cells and is intractable; per-dim marginal binning discards joint structure. Generalization requires a **rethink** — e.g., KDE, random projection to low-dim subspaces, marginalization with a defensible aggregation rule. Same concern applies to Sentinel's default `mmd_rbf_pos` (position-only MMD) on the STAC side.
>
> **Mitigation**: in S3, implement a dimensionality-agnostic ACE variant (recommend: per-dim marginal entropy summed with PCA-projection cross-check as ablation). If ACE cells underperform in S5, fall back to STAC cells (using `mmd_rbf_all`, not `mmd_rbf_pos`) as the headline. Pre-register the chosen ACE generalization before S5.

> [!warning] R6 — Injected-failure protocol doesn't reflect real failures + protocol had to be restructured after backbone swap
> **Severity**: MEDIUM-HIGH. Original protocol was weight-module Gaussian noise (AdaWorldPolicy-style, distinct WM/action modules). Neither UWM nor Cosmos Policy has separate modules — both share a single DiT with modality-specific outputs. Protocol was redesigned to **output-token injection** (§5.3.2): noise on video-output tokens (imag corruption) vs. action-output tokens (act corruption). This is a compromise — output-level noise is cleaner than weight noise in these backbones but is still synthetic.
>
> **Mitigation**: (a) σ sweep {0.1, 0.5, 1.0} × activation std pre-registered before S5; (b) real LIBERO-Plus OOD rollouts + natural failures as held-out validity check; (c) RAPT-style VLM-rated attribution on 100 natural failures as secondary (label-free, task-progress-based).

> [!warning] R7 — Benchmark overlap between backbones limited to LIBERO
> **Severity**: MEDIUM (scope).
>
> **Mitigation**: backbone-native secondaries (Robomimic, RoboCasa) provide per-backbone depth; H4 claimed within LIBERO.

> [!warning] R8 — Compute budget
> **Severity**: **LOW** for inference. Cosmos Policy's README reports **6.8 GB** peak VRAM for LIBERO inference; 8×H100 (80 GB each) is massively overprovisioned. Base Cosmos inference is ~0.5 s/step; STAC-256 multiplies action sampling only (cheap: ~2.6 GB peak for 256 × 10 MB action-chunk activations) and does not multiply future-state generation. Cell 6 (2B × STAC-256) is the most expensive and still comfortably feasible. (Risk remains relevant if CNF training for both backbones + injected-failure suite generation saturates wallclock, but that's a scheduling risk, not a compute risk.)
>
> **Mitigation**: (a) UWM cells first for faster iteration; (b) STAC-single fallback available if needed; (c) Cell 6 drop-rule retained as defensive depth.

> [!warning] R9 — Second imag anchor deferred; no structural redundancy for `logpZO`
> **Severity**: MEDIUM. The 2×2 design rests on a single imag signal. If `logpZO(\hat{O}_{t+1})` fails to discriminate imagination failure on either backbone (R1 materializes), the whole imag axis collapses and the paper degrades to act-only detection.
>
> **Mitigation**: (a) S9 ablation `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})` per backbone — if predicted-frame AUROC drops badly, retrain CNF with predicted-frame augmentation; (b) B-FAIL-FULL ensemble baseline as backup imag signal if `logpZO` alone fails; (c) Foundational-WM reimplementation is the plan-B pivot per S4 partial-pivot.

> [!warning] R11 — Both signals sit near CP thresholds on real (subtle) failures — gate collapses to detection
> **Severity**: HIGH. Real manipulation failures (near-miss grasps, partial occlusions, subtle physics errors) may produce signal values in the 80–95 percentile of the success distribution — high enough to be concerning but below the α=0.10 CP threshold. The 2×2 gate then labels most real episodes as `00` (success-looking) with only rare `01` / `10` fires, degrading the attribution USP.
>
> **Mitigation**: §5.3.4 must report the **full joint distribution** of $(R_\text{imag}, R_\text{act})$ on natural-failure rollouts (not only gate labels); add a soft-scoring variant (rank percentiles) alongside the hard-threshold gate; include heatmap of $(R_\text{imag}, R_\text{act})$ percentiles on the injected vs. natural-failure suites.

> [!warning] R12 — Real failures are ≥ 80% mixed (class `11`) — 4-cell label effectively 2-class
> **Severity**: MED-HIGH. If natural LIBERO-Plus failures concentrate in the `11` cell (both signals elevated), the 2×2 attribution degenerates into detection with one extra bit, losing the differential-diagnosis USP. WorldArena-style co-fire correlations (r ≈ 0.36 reported in prior work) support this risk.
>
> **Mitigation**: S1 cheap probe on LIBERO-Plus to estimate class balance on natural failures; pre-register threshold "kill gate if `11` > 80% of natural failures." If `11` dominates, reframe the paper as "calibrated joint-failure detection with 4-way explanatory breakdown" rather than "attribution."


---

## 9. Out of Scope / Future Work

This paper produces a 2-bit label under FIPER-generalized stacking, on two backbones × one imag signal × two act signals. Follow-ups:

1. **Second imag signal** — once a robot-scene-validated spectral / epistemic / own-loss signal exists on VLA / WAM predicted frames, extend to 2×2×2. Candidate pool: [[2502.20946|DIFF-UQ]], [[2510.07206|EigenScore]], [[2504.07793|RDM]], [[2508.05461|rFM]] (all currently image-OOD validated only).
2. **AR sub-variant (DreamZero)** — adapt `logpZO` to AR-token categorical flow.
3. **Multi-component signal stacks** — restore pixel-MSE + additional semantic/perceptual channels on imag; Flow-SDE + AAC on act.
4. **Closed-loop update routing** — cell `10` → WM LoRA; cell `01` → action-head residual RL.
5. **Attribution-gated safety** — refuse-to-act on real-time imag-fail.
6. **Foundational-WM reimplementation** — Plan B if S4 kills all cells.
7. **Distinct-weight-module backbone** — re-run 2×2 on AdaWorldPolicy if code opens or on a successor with separate WM / action weight modules.

---

## Cross-References

- [[01_Self-Discovering-WAM-Literature]] — §Anchor Elevation paragraph motivating this roadmap; why one imag signal not two; Bucket A.
- [[00_Self-Discovering-WAM-Summary]] — one-page companion pitch.

---

*Companion to [[01_Self-Discovering-WAM-Literature]].*
