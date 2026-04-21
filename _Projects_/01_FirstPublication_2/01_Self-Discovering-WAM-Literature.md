---
title: "Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs — Literature Scan"
tags:
  - WAM
  - diffusion
  - failure-detection
  - failure-attribution
  - self-discovery
  - imagination-error
  - action-error
  - literature
aliases:
  - "Diffusion-WAM Attribution Lit"
  - "Self-Discovering Diffusion-WAM Lit Scan"
  - "FIPER-Generalized Attribution Gate Lit Scan"
  - "2x2 Factorial Attribution Gate Lit Scan"
---

# Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs — Literature Scan

> [!abstract] Scope
> Literature scan for a first-publication **FIPER-generalized 2×2 attribution gate** for diffusion-WAMs, evaluated as a **2×2 factorial = 4 cells**: two diffusion-WAM backbones × two act signals, with a single WM-prediction-native imag signal. The paper delivers a per-episode 2-bit diagnostic (==imagination failure== × ==action failure==); what to do with the diagnosis is out of scope. Backbones: [[2504.02792|UWM]] (~90M, DDPM-VP) + [[2601.16163|Cosmos Policy]] (~2B, rectified flow). Imag anchor: [[2503.08558|FAIL-Detect]] `logpZO` extended to $\hat{O}_{t+1}$. Act anchors: [[2510.09459|FIPER]]-ACE + [[2410.04640|Sentinel]]-STAC. [[2510.09459|FIPER]] = structural ancestor.

> [!tip] Anchor elevation — FIPER-generalized 2×2 factorial
> Method restructured around **FIPER as structural ancestor** with one WM-prediction-native imag signal and two candidate act signals evaluated on two diffusion-WAM backbones. [[2510.09459|FIPER]] (Römer et al., NeurIPS 2025; public repo `github.com/utiasDSL/fiper`, MIT, 2025-11-03) contributes the **dual-signal success-only CP architecture**. On the imag axis, one label-free anchor: [[2503.08558|FAIL-Detect]] (Xu/Itkina/Nishimura at TRI; public repo `github.com/CXU-TRI/FAIL-Detect`, CC BY-NC, 2025-06-18) — `logpZO` is a CNF density score on the noise latent, natively computed on real observations $O_t$; applying it to WM-predicted $\hat{O}_{t+1}$ is a **novel extension, not a drop-in port** (verified: `train.py` feeds `observation = x_batch` with real $O_t$; no predicted-frame path). On the action axis, two candidate anchors with public code: FIPER's own **ACE** (action-chunk entropy, parameter-free, same repo) and [[2410.04640|Sentinel]]'s **STAC** (Agia et al., CoRL 2024; public repo `github.com/agiachris/sentinel`, MIT, 2025-02-05) — MMD on 256 action samples per Sentinel's Push-T config. **2×2 factorial = 4 cells** (UWM × ACE; UWM × STAC; Cosmos × ACE; Cosmos × STAC). Backbone anchors: [[2504.02792|UWM]] (WEIRDLabUW, ICRA 2025; public repo, GDrive checkpoints, Robomimic + LIBERO — DDPM ε-prediction with DDIM sampling) and [[2601.16163|Cosmos Policy]] (NVIDIA, 2026; public repo `github.com/NVlabs/cosmos-policy`, Apache-2.0 code + NSCLv1 weights, HF checkpoints, LIBERO + RoboCasa + ALOHA — rectified-flow). AdaWorldPolicy (2602.20057) dropped as backbone — no public code. Fast-WAM (2603.16666) dropped — its "no test-time imagination" thesis is incompatible with `logpZO(\hat{O}_{t+1})`. Alternatives dismissed after verification: [[2506.09937|SAFE]] (labeled success+failure — demoted to B-SAFE baseline); [[2603.06987|Foundational WM]] (no confirmed public code — optional Plan-B ablation); [[2604.01985|WAV]] (sparse-IDM needs expert actions — B-WAV baseline); [[2602.16182|WM Failure Classifier]] (requires labeled known-failure data — B-WMFC baseline). Second imag anchor explored across 4 candidate rounds ([[2502.20946|DIFF-UQ]] — CLIP dependency; [[2510.07206|EigenScore]] — no robotics validation; [[2504.07793|RDM]] — density-family, H5-redundant; [[2508.05461|rFM]] — density-family) — **all lack VLA/WAM validation**, so the second imag anchor is deferred to publication #2.

---

## Why One Imag Signal, Not Two

We deliberately ship with **only `logpZO`** on the imag axis. Explored candidates for a second imag anchor across four search rounds (DIFF-UQ, EigenScore, RDM, rFM/WT-Flow, Diff-DAgger) and dismissed each:

| Candidate | Why rejected |
|---|---|
| [[2502.20946\|DIFF-UQ]] | CLIP pretraining-distribution mismatch on robot scenes |
| [[2510.07206\|EigenScore]] | Native validation is image-OOD (CIFAR-10/100, SVHN) — no robotics / VLA / WAM evidence that posterior-covariance spectrum discriminates predicted-frame failure |
| [[2504.07793\|RDM]] | Density-family signal — structurally redundant with `logpZO` |
| [[2508.05461\|rFM / WT-Flow]] | Density-family signal — structurally redundant with `logpZO`; industrial anomaly domain, no robotics validation |
| [[2410.14868\|Diff-DAgger]] | Own-loss signal is computed on **actions**, not on predicted observations — wrong axis |

**Conclusion**. Every structurally-distinct-from-logpZO candidate with public code has been validated only on image-OOD benchmarks, not on VLA / WAM predicted frames. The field-level gap is real, not a defect of candidate selection. Ship with **one validated imag signal** + the 2×2 dual-backbone generality claim; defer the second imag anchor to publication #2 after robot-scene spectral-OOD evidence exists.

---

## Why Diffusion + Why These Two Backbones

Backbone choice is pragmatic and constrained: both imag anchors require a WAM that produces a predicted next-frame at inference, so backbones that remove test-time imagination (Fast-WAM) are structurally ruled out. Among public diffusion-WAMs with future imagination + released checkpoints, **[[2504.02792|UWM]]** and **[[2601.16163|Cosmos Policy]]** span the interesting design axis:

| Backbone | Parameters | WM/action coupling | Benchmarks | Decorrelation basis for H2 |
|---|---|---|---|---|
| **[[2504.02792\|UWM]]** | ~90M DiT | Shared backbone; **modality-independent diffusion timesteps** for video vs. action | Robomimic Square/Transport/Can + LIBERO-100 | Timestep-level modality decoupling |
| **[[2601.16163\|Cosmos Policy]]** | ~2B DiT (Cosmos-Predict2) | Shared backbone; **distinct latent-frame roles** for action / future-image / value | LIBERO + RoboCasa + ALOHA | Latent-role-token decoupling |

Neither has AdaWorldPolicy-style distinct-weight-module separation. H2 decorrelation is weakened on both but through *different* architectural mechanisms — which is why the 2×2×2 factorial is the right evaluation design: it tests whether the signal-level decorrelation is robust across both backbone coupling mechanisms.

Latent-WM families (Dreamer / JEPA) remain excluded by anchor availability.

---

## Diffusion-WAM Landscape

| Sub-variant | Exemplar(s) | Our scope |
|---|---|---|
| **Continuous-diffusion video + preserved test-time imagination** | [[2504.02792\|UWM]] (DDPM-VP), [[2601.16163\|Cosmos Policy]] (rectified-flow) | **In scope — the 2 backbones of the 2×2 grid** |
| **Distinct-weight WM + action modules** | [[2602.20057\|AdaWorldPolicy]] | Referenced for architectural ideal, **no public code** → not usable |
| **Removed test-time imagination** | [[2603.16666\|Fast-WAM]] | Incompatible with `logpZO(\hat{O}_{t+1})` — excluded |
| **AR-video-diffusion** | [[2602.15922\|DreamZero]] | Deferred to publication #2 |

---

## Problem Setup

A diffusion-WAM executes an episode by rolling out in imagination (denoising future frames + predicting actions) and acting in reality. When the episode fails, the failure has two possible blame targets:

| | Imagination failure (cell `10`) | Action failure (cell `01`) |
|---|---|---|
| **What's wrong** | Predicted frame $\hat{O}_{t+1}$ off the success-rollout manifold | WM prediction on-manifold, action head picks poorly |
| **Signal in our gate** | `logpZO(\hat{O}_{t+1})` (FAIL-Detect) — one signal, both cells 1/5 and 2/6 | ACE (FIPER) or STAC (Sentinel) — one per cell |

Prior detection systems ([[2510.09459|FIPER]], [[2506.09937|SAFE]], [[2503.08558|FAIL-Detect]], [[2602.16182|WM Failure Classifier]]) fire a single "failure likely" flag and do not decompose the failure. This paper's contribution is the decomposition + joint calibration + 2×2×2 generality validation.

---

## Bucket A — Imagination-Failure Detection (Trimmed to Two Anchors + Direct Competitors)

Signals on the WM side.

- [[2503.08558|FAIL-Detect]] — **Imag anchor (all 4 cells).** `logpZO` flow-based density + functional Conformal Prediction; label-free, calibrated on success rollouts only. Public code. Native use is on real $O_t$; our novel extension is to $\hat{O}_{t+1}$. Additional FAIL-Detect signals (`logpO`, RND, combined CDF-ensemble) serve as baselines (B-FAIL-DETECT-FULL).
- [[2502.20946|DIFF-UQ]], [[2510.07206|EigenScore]], [[2504.07793|RDM]], [[2508.05461|rFM]] — **Dropped second-imag-anchor candidates.** All four are image-OOD validated only; none have been shown to discriminate failure on robot-scene predicted frames. Deferred to publication #2 once a robot-validated spectral or epistemic signal exists.
- [[2603.06987|Foundational WM]] — **Plan-B imag anchor.** Predicted-std + prediction error on Cosmos-Tokenizer latents. No confirmed public code — reimplementation candidate if S4 kills all 4 cells with `logpZO`.
- [[2602.16182|WM Failure Classifier]] — **Supervised baseline.** Success / known-failure / OOD via latent prediction error + CP; **requires labeled known-failure data**. Closest prior system in detection structure.
- [[2603.11106|RC-NF]] — **Tier-1 baseline.** Robot-Conditioned Normalizing Flow; fully unsupervised. Density-based like `logpZO`; reported as a comparator in baselines.

---

## Bucket B — Action-Failure Detection (Trimmed to Anchors + Direct Competitors)

Signals on the action-head side.

- [[2510.09459|FIPER]] — **Structural ancestor + act anchor #1 (cells 1, 3, 5, 7).** RND-OE + ACE under AND-gate. Headline numbers are AND-gate combined (TWA 0.65, overall 0.78); ACE-alone not cleanly tabulated → R5 risk. Public code (MIT). Repo inspection confirms ACE is currently coded for 3-D position actions (x/y/z) — must be generalized for 7-DoF.
- [[2410.04640|Sentinel]] — **Act anchor #2 (cells 2, 4, 6, 8).** STAC = MMD on 256 action samples. Published: STAC > 90% balanced acc on Push-T, 96% on Close Box. Public code (MIT). **Gotcha**: default config in `sentinel/bc/ood_detection/error_utils.py:62` is `mmd_rbf_pos` (position-only, 3-D); full-action `mmd_rbf_all` exists but isn't in the paper's headline numbers — parallels R5 on FIPER-ACE. For 7-DoF AdaWorldPolicy-style action chunks we use `mmd_rbf_all`.
- [[2506.09937|SAFE]] — **Supervised baseline + source of STAC-single reduction.** Labeled success+failure rollouts. Also names **STAC-single** — single-sample fallback we'll implement atop Sentinel's code for Cell 6 (2B × STAC-256 is the most expensive cell).
- [[2510.25889|Flow-SDE]] — **Future-work component.** Cited only.

---

## Bucket C — Attribution & Verification Competitors (Trimmed)

- [[2604.01985|WAV]] — **Closest prior decomposition + supervised attribution baseline.** Forward-inverse asymmetry: subgoal generator + sparse IDM. **Requires expert action data.** Latent WM, not diffusion-video. We differ on: (a) diffusion-native pixel ground-truth vs. latent; (b) per-episode diagnostic vs. self-improvement; (c) label-free vs. expert-action.
- [[2603.04029|Self-Adapting RL]] — **Conceptual precedent for decomposition.** OPR + RPR, OR-gated within Dreamer-RSSM. Not diffusion; threshold-based, not CP. Retained as prior decomposition reference.
- [[2602.08971|WorldArena]] — **Empirical support.** 2×2 benchmark of 14 WMs reports r ≈ 0.36 between perceptual quality and action-planning utility — evidence the decomposition is non-trivial.
- [[2603.07799|MWM]] — **Empirical support.** Visually-faithful diffusion rollouts can be action-inconsistent.

Supervised VLM-based attribution systems ([[2512.01946|Guardian / FailCoT]], [[2410.00371|AHA]], [[2510.01642|FailSafe]], [[2602.01515|RAPT]]) cited only — label-free constraint rules them out.

---

## The Gap

> [!question] What no prior paper does
> No prior work combines a **WM-prediction-native imag signal** (`logpZO` on $\hat{O}_{t+1}$) with **two success-only action-side signals** (ACE + STAC) into a **Bonferroni-corrected joint CP gate** that reports 2-bit attribution on **two diffusion-WAM backbones** as a 2×2 factorial, with zero failure labels.

| Paper | Output | Why it's not the same |
|---|---|---|
| [[2510.09459\|FIPER]] | Single flag (RND-OE ∧ ACE) | AND-gate collapses signals; no attribution; policy-observation RND-OE not WM-prediction-native; single backbone |
| [[2503.08558\|FAIL-Detect]] | Scalar OOD on real $O_t$ | Single axis; native use doesn't touch WM predictions |
| [[2410.04640\|Sentinel]] | STAC (action) + VLM (progress) | Action-axis only; VLM companion needs task labels |
| [[2604.01985\|WAV]] | Forward-inverse asymmetry | Supervised; latent WM; self-improvement loop |
| [[2602.16182\|WM Failure Classifier]] | 3-way success/known-failure/OOD | Supervised; single signal; no decomposition |
| [[2506.09937\|SAFE]] | Scalar failure score | Supervised; single signal; no component localization |
| [[2603.04029\|Self-Adapting RL]] | OPR + RPR, OR-gated | Dreamer-only; threshold-based not CP |
| [[2602.08971\|WorldArena]] | Per-model 2×2 decomposition | Benchmark-level, not per-episode |

**Contribution**: the 4-cell diagnostic matrix from the joint of $(R_{\text{imag}}, R_{\text{act}})$, computed on **two diffusion-WAMs with different parameterizations** (UWM DDPM-VP + Cosmos Policy rectified-flow) × **two act signals** as a 2×2 factorial, using `logpZO` extended to WM-predicted $\hat{O}_{t+1}$ as the single imag signal.

| | low $R_{\text{act}}$ | high $R_{\text{act}}$ |
|---|---|---|
| **low $R_{\text{imag}}$** | Success | Action failure |
| **high $R_{\text{imag}}$** | Imagination failure | Joint failure |

---

## Out-of-Scope / Future Work

Explicitly deferred to publication #2:

- **Second imag signal** — restore a structurally-distinct imag anchor ([[2502.20946|DIFF-UQ]], [[2510.07206|EigenScore]], [[2504.07793|RDM]], [[2508.05461|rFM]]) once a robot-scene-validated spectral / epistemic / own-loss signal exists on VLA / WAM predicted frames.
- **AR sub-variant** — [[2602.15922|DreamZero]] with categorical-softmax adaptation of `logpZO`.
- **Multi-component signal stacks** — restore pixel-MSE + [[2510.25889|Flow-SDE]] + [[2604.04161|AAC]] on top of this 2×2 foundation.
- **Closed-loop update routing** — cell `10` → WM LoRA; cell `01` → action-head residual RL. Relevant: [[2511.00091|PLD]], [[2507.21053|FPO]], [[2602.04879|DPPO]], [[2602.20057|AdaWorldPolicy]], [[2603.13528|Dream2Fix]].
- **Attribution-gated safety** — refuse-to-act on real-time imag-fail.
- **Distinct-weight-module backbones** — re-run the 2×2 gate on AdaWorldPolicy if code becomes public, or on any successor backbone with separate WM / action weight modules.

---

## Cross-References

- [[02_Self-Discovering-WAM-Roadmap]] — operational plan (architecture, hypotheses, execution steps, risk register).
- [[00_Self-Discovering-WAM-Summary]] — one-page pitch.

---

*Companion to [[00_Self-Discovering-WAM-Summary]] and [[02_Self-Discovering-WAM-Roadmap]].*
