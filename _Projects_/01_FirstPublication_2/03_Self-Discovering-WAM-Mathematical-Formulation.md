---
title: "Mathematical Formulation: Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs"
tags:
  - WAM
  - diffusion
  - failure-detection
  - failure-attribution
  - self-discovery
  - mathematics
  - methodology
aliases:
  - "Self-Discovering WAM Math"
  - "Diffusion-WAM Attribution Math"
  - "2x2x2 Attribution Gate Math"
  - "FIPER-Generalized Gate Math"
---

# Mathematical Formulation: Self-Discovering Imagination vs. Action Failure in Diffusion-WAMs

> [!abstract] Purpose
> Formal derivation of the **2×2×2 factorial attribution gate** for diffusion-WAMs. Each section shows: inputs → formula → guarantee → how it feeds the next step. Formulas sourced from anchor papers are cited inline; novel constructions are explicitly labeled ==our design==. The document ends with a composition proof showing that the full 8-cell pipeline is well-defined, provides per-cell joint-FPR control at level $\alpha$ under exchangeability, and yields cross-cell inference via standard binomial testing.

> [!info] Notation Conventions (disambiguation table)
>
> **Trajectories and observations** (renamed from $\tau$ to $\omega$ to free $\tau$ for thresholds):
> - $o_t \in \mathcal{O}$ — real observation at time $t$; $l$ — language instruction; $\mathcal{O}$ an image/latent space with tokenization $\text{Tok}: \mathcal{O} \to \mathbb{R}^{N_o \times d}$.
> - $a_t \in \mathbb{R}^{d_a}$ — executed action at time $t$ ($d_a = 7$ LIBERO; $d_a = 3$ Push-T default).
> - $\mathbf{a}_{t:t+H} \in \mathbb{R}^{H \times d_a}$ — action chunk of horizon $H$ predicted at time $t$.
> - $\hat{O}_{t+1} \in \mathcal{O}$ — diffusion-WAM's **predicted** next frame.
> - $\omega = (o_1, a_1, \ldots, o_T, a_T)$ — episode **trajectory** of length $T$ (was $\tau$ in earlier drafts).
> - $\omega_\text{cal}, \omega_\text{test}, \omega_i$ — specific trajectories (calibration / test / indexed).
>
> **Signals and thresholds** (now unambiguous):
> - $s_{\text{imag}}(\cdot), s_{\text{act}}(\cdot)$ — per-timestep scalar signals on imag / act axis.
> - $R_{\text{imag}}(\omega), R_{\text{act}}(\omega) \in \mathbb{R}$ — episode-aggregated scores (max-so-far, §7).
> - $\tau_{\text{imag}}(t), \tau_{\text{act}}(t)$ — per-timestep **conformal thresholds** on each axis (§8). Always written with a time argument.
> - $b_{\text{imag}}, b_{\text{act}} \in \{0,1\}$ — binary axis decisions; gate output $\ell \in \{00, 01, 10, 11\}$.
>
> **Backbones, cells, and indices** (disambiguated):
> - $X \in \{A, B\}$ — backbone index ($A$ = UWM, $B$ = Cosmos Policy).
> - $c \in \{1, \ldots, 8\}$ — 2×2×2 cell index; $c_\text{inj} \in \{00, 01, 10, 11\}$ — injection class (subscript to distinguish from cell index).
> - $m \in \{\text{video}, \text{action}, \text{value}\}$ — output modality (used with $z_m^{(K)}$, $\mathcal{D}_m$, $N_m$).
> - $K$ — **diffusion/ODE solver steps** in (2.1); $K_\text{samp}$ — **action sample count** for STAC ($K_\text{samp} = 256$) and ACE ($K_\text{samp} = 100$). Different letters to avoid collision.
>
> **Parameters and noise**:
> - $\theta$ — shared DiT weights; $w_L$ — last-layer weights (DIFF-UQ Laplace subject); $\psi$ — CNF weights (logpZO).
> - $\alpha \in (0,1)$ — target joint false-positive rate per cell (headline $\alpha = 0.10$).
> - $\sigma_\mathrm{inj}$ — injected-failure noise scale (per backbone, per modality).
> - $M \geq 1$ — DIFF-UQ MC sample count; $M \geq 2$ required for CLIP semantic-entropy channel.
>
> **Convention**: $\tau$ **only ever appears as a threshold** (with subscript and time argument: $\tau_X(t)$). $\omega$ is always a trajectory. $X$ is always a backbone index. $K$ without qualification is always solver steps.

---

## 1. Notation — Diffusion-WAM Interface, Signals, Thresholds

### 1.1 Backbone-level interface (shared across UWM and Cosmos Policy)

Both backbones expose a single map

$$\mathcal{F}_\theta\colon (o_{1:t}, l) \;\mapsto\; \bigl(\hat{O}_{t+1},\; \mathbf{a}_{t:t+H},\; \phi_t\bigr)$$

where $\phi_t \in \mathbb{R}^{d_L}$ denotes the **last-layer input activations** of the shared DiT at step $t$ (the quantity consumed by DIFF-UQ's Laplace posterior). The two backbones differ only in how they route $\hat{O}_{t+1}$ and $\mathbf{a}_{t:t+H}$ out of the shared DiT:

| Backbone | Decoupling mechanism | What shares $\theta$ | What differs |
|---|---|---|---|
| **[[2504.02792\|UWM]]** (~90M) | Modality-independent diffusion timesteps | DiT weights + visual tokenizer | Timestep schedule for video vs. action outputs |
| **[[2601.16163\|Cosmos Policy]]** (~2B) | Distinct latent-frame roles | Cosmos-Predict2 DiT + tokenizer | Role assignment of latent frames: action / future-image / value |

Let $\pi(O \mid o_{1:t}, l; \theta)$ denote the diffusion-WAM's conditional distribution over next frames, and let $p(\mathbf{a} \mid o_{1:t}, l; \theta)$ denote the conditional over action chunks. Both are score- or velocity-parameterized in the usual diffusion / flow-matching sense.

### 1.2 Per-timestep signals (per cell)

Each cell of the 2×2×2 grid pairs one imag signal with one act signal:

| Axis | Options | Input | Output |
|---|---|---|---|
| **Imag** | `logpZO` **or** DIFF-UQ | $\hat{O}_{t+1}$ (+ $\phi_t$ for DIFF-UQ) | $s_\text{imag}(t) \in \mathbb{R}_{\geq 0}$ |
| **Act** | ACE **or** STAC | $\mathbf{a}_{t:t+H}$ (or $K$ samples thereof) | $s_\text{act}(t) \in \mathbb{R}_{\geq 0}$ |

### 1.3 Calibration and injection

- $\mathcal{D}_\text{cal}$ — calibration set of $N = 500$ **success-only** rollouts per cell (per §5.2 / S2 of Roadmap).
- $\mathcal{D}_\text{inj}(c)$ — injected-failure set: $500 \times 4 \times 2 = 4000$ synthetic rollouts, class $c \in \{00, 01, 10, 11\}$ (§5.3.2 of Roadmap).
- $\sigma_\mathrm{inj}(c; \theta)$ — per-backbone, per-class Gaussian noise scale on the output-token corruption protocol.

---

## 2. Diffusion-WAM Forward Pass

> Goal: a notation covering both UWM's timestep-decoupled forward and Cosmos Policy's role-token-decoupled forward, so that every downstream equation applies to both backbones.

### 2.1 Shared latent-flow forward

Let $\mathcal{V}$ denote the latent / token space of the shared DiT and let $v_\theta: \mathcal{V} \times [0,1] \times \mathcal{C} \to \mathcal{V}$ be the DiT's velocity field, where $\mathcal{C}$ is the conditioning space (observation + language tokens). Flow matching ([[2504.02792|UWM]] §3; [[2601.16163|Cosmos Policy]] §3, following Cosmos-Predict2) defines, for each output channel $m \in \{\text{video}, \text{action}, \text{value}\}$:

$$z_m^{(k+1)} = z_m^{(k)} + \tfrac{1}{K}\,v_\theta\!\bigl(z_m^{(k)},\;t_k^{(m)},\;c(o_{1:t}, l)\bigr),\qquad z_m^{(0)} \sim \mathcal{N}(0, I),\ k=0,\ldots,K-1. \tag{2.1}$$

The **distinguishing content** is $t_k^{(m)}$ (UWM: modality-independent schedules) or the channel identity baked into $z_m^{(0)}$ through latent-frame role assignment (Cosmos Policy). Let $\mathcal{D}_m$ denote the decoder that maps the final latent $z_m^{(K)}$ to output space:

$$\hat{O}_{t+1} = \mathcal{D}_\text{video}\bigl(z_\text{video}^{(K)}\bigr),\qquad \mathbf{a}_{t:t+H} = \mathcal{D}_\text{action}\bigl(z_\text{action}^{(K)}\bigr). \tag{2.2}$$

### 2.2 Last-layer activations (required by DIFF-UQ)

Let $g_\theta = h_\theta \circ f_{\theta \setminus w_L}$ be a decomposition of the DiT's final block, where $f_{\theta \setminus w_L}$ produces the last-layer input $\phi_t \in \mathbb{R}^{d_L}$ and $h_\theta$ is the affine last-layer map with weights $w_L$:

$$z_m^{(K)} = h_{w_L}(\phi_t) = W_L \phi_t + b_L. \tag{2.3}$$

DIFF-UQ treats only $w_L = (W_L, b_L)$ as random; all upstream weights are frozen. This is the **Bayesian last-layer** decomposition of [[2502.20946|DIFF-UQ]] §3.1.

### 2.3 Action-chunk sampling

For act signals that require a sample set (STAC), we draw $K$ independent action chunks by re-running (2.1) on the action channel with fresh initial noise:

$$\mathbf{a}^{(i)}_{t:t+H} \sim p(\cdot \mid o_{1:t}, l; \theta),\qquad i=1,\ldots,K. \tag{2.4}$$

ACE uses $K \geq K_\text{ACE}$ samples (FIPER default: $K = 100$ per step); STAC-256 uses $K = 256$; STAC-single ([[2506.09937|SAFE]]) uses $K = 1$ with a cheaper two-sample MMD surrogate.

> **Output of §2**: per-timestep tuple $\bigl(\hat{O}_{t+1},\; \mathbf{a}_{t:t+H},\; \phi_t,\; \{\mathbf{a}^{(i)}_{t:t+H}\}_{i=1}^K\bigr)$ — the interface that every downstream signal consumes.

---

## 3. Imag Signal #1 — FAIL-Detect `logpZO` on $\hat{O}_{t+1}$

### 3.1 Anchor formulation (on real $O_t$, [[2503.08558|FAIL-Detect]] §3.4)

[[2503.08558|FAIL-Detect]] trains a conditional flow matching (CFM) / CNF network $N_\psi: \mathcal{O} \times [0,1] \to \mathcal{O}$ on the density of success-rollout observations. With data-to-noise path $x_s = (1-s)x_0 + s x_1,\; x_1 \sim \mathcal{N}(0, I)$, the training loss is

$$\mathcal{L}_\text{CNF}(\psi) \;=\; \mathbb{E}_{x_0 \sim p_\text{success},\, x_1 \sim \mathcal{N}(0,I),\, s \sim \mathcal{U}(0,1)} \Bigl[\bigl\|N_\psi(x_s, s) - (x_1 - x_0)\bigr\|_2^2\Bigr]. \tag{3.1}$$

At inference, FAIL-Detect's public score (verified from `FAIL-Detect/UQ_test/eval_load_baseline.py:134-148`) is the squared $L_2$ norm of the estimated noise endpoint at $s=0$:

$$\ell_\text{CNF}(x) \;=\; \bigl\|\,x + N_\psi(x,\,s{=}0)\,\bigr\|_2^2. \tag{3.2}$$

**Interpretation**. The CNF is trained so that the straight-line velocity is $v = x_1 - x_0$ (noise minus clean). At $s=0$, feeding the clean-data input $x = x_0$ gives $N_\psi(x_0, 0) \approx x_1 - x_0$, so $x + N_\psi(x, 0) \approx x_1$ — the implied noise endpoint. The score $\ell_\text{CNF}$ is therefore a proxy for the squared norm of the noise latent at $s=0$, which is a monotonic surrogate for $-\log p_\psi(Z_x)$ **only when the input $x$ is on the clean-data manifold**. Inputs off the manifold break the $v \approx x_1 - x_0$ assumption; empirically FAIL-Detect verifies this proxy discriminates OOD observations despite the approximation. FAIL-Detect evaluates this on $x = O_t$ (real observation).

### 3.2 Our extension to $\hat{O}_{t+1}$ (==our design==)

==We apply (3.1)–(3.2) to the WM-predicted next frame $\hat{O}_{t+1}$ instead of the real observation $O_t$.== Per-cell (cells 1, 2, 5, 6 of the 2×2×2), we train a **per-backbone CNF** $N_{\psi_A}, N_{\psi_B}$ on success-rollout $\hat{O}_{t+1}$ distributions:

$$\mathcal{L}_\text{CNF}^{\text{(ours)}}(\psi_X) \;=\; \mathbb{E}_{\hat{O}\sim p_\text{success}^{(X)}(\hat{O}_{t+1})}\bigl[\ldots\bigr],\qquad X \in \{A, B\}. \tag{3.3}$$

**Per-timestep signal**:

$$\boxed{\; s_\text{imag}^\text{logpZO}(t; X) \;=\; \bigl\|\,\hat{O}_{t+1} + N_{\psi_X}(\hat{O}_{t+1},\,0)\,\bigr\|_2^2 \;} \tag{3.4}$$

**Why this is an extension, not a drop-in port.** FAIL-Detect's `train.py` (verified lines 19–80) feeds `observation = x_batch` with $x_\text{batch} = O_t$ (real). No predicted-frame path exists in the public code. Applying $N_\psi$ to $\hat{O}_{t+1}$ requires: (a) re-training the CNF on the predicted-frame success distribution, not the real-frame one, because the two marginals differ (WM predictions are denoiser outputs, not raw sensors); (b) per-backbone calibration, because the $\hat{O}_{t+1}$ marginal differs between UWM and Cosmos Policy.

Ablation S9 measures `logpZO(O_t)` vs. `logpZO(\hat{O}_{t+1})` per backbone to isolate this extension's effect.

---

## 4. Imag Signal #2 — DIFF-UQ (Laplace + CLIP)

### 4.1 Last-layer Laplace posterior ([[2502.20946|DIFF-UQ]] §3.1)

With the decomposition (2.3), the last-layer weights are given a Gaussian prior $w_L \sim \mathcal{N}(0, \tau_0^{-1} I)$ (using $\tau_0$ for the prior precision to avoid collision with conformal thresholds $\tau_X(t)$), and the Laplace approximation around the MAP $\hat{w}_L$ yields a Gaussian posterior with a **diagonal empirical-Fisher** precision (verified `DIFF-UQ/diffusion_laplace.py:119-132`; code uses `einsum("bp,bp->p")` — per-parameter squared-gradient sum, not full outer-product):

$$q(w_L \mid \mathcal{D}_\text{cal}) \;=\; \mathcal{N}(\hat{w}_L,\,\Sigma_L),\qquad [\Sigma_L^{-1}]_{jj} \;=\; \tau_0 \;+\; \sum_{x \in \mathcal{D}_\text{cal}} (G_{x,j})^2, \qquad [\Sigma_L^{-1}]_{jk} = 0\ \text{for}\ j \neq k, \tag{4.1}$$

where $G_x = \nabla_{w_L} \ell(f(x; \theta)) \in \mathbb{R}^{|w_L|}$ is the per-sample gradient of the flow-matching loss w.r.t. $w_L$, and $G_{x,j}$ denotes its $j$-th component. The diagonal structure reduces memory from $|w_L|^2$ to $|w_L|$ — essential for the 2B Cosmos Policy last layer.

### 4.2 MC sampling of predicted frames ([[2502.20946|DIFF-UQ]] §3.2)

Draw $M$ weight samples $w_L^{(m)} \sim q(w_L \mid \mathcal{D}_\text{cal})$ and, for each, run the diffusion reverse process (2.1) with perturbed last layer:

$$\hat{O}_{t+1}^{(m)} \;=\; \mathcal{D}_\text{video}\!\bigl(z_\text{video}^{(K)}(w_L^{(m)})\bigr),\qquad m=1,\ldots,M. \tag{4.2}$$

[[2502.20946|DIFF-UQ]] validates **$M \geq 1$** for the Laplace-only channel; **$M \geq 2$** is required for the CLIP semantic-entropy channel (verified from `DIFF-UQ/semantic_likelihood.py:46-58`, which stacks $M$ CLIP feature vectors and requires cross-sample variance).

### 4.3 CLIP semantic likelihood ([[2502.20946|DIFF-UQ]] §3.3)

Let $\Phi_\text{CLIP}: \mathcal{O} \to \mathbb{R}^{d_\text{CLIP}}$ be the frozen CLIP ViT-B/32 image encoder. Define $\mu_m = \Phi_\text{CLIP}(\hat{O}_{t+1}^{(m)}) \in \mathbb{R}^{d_\text{CLIP}}$. The diagonal per-dim variance across the $M$ samples is

$$\mathrm{Var}_j\!\bigl[\mu_{\cdot,j}\bigr] \;=\; \tfrac{1}{M}\!\sum_{m=1}^{M} \mu_{m,j}^2 \;-\; \bar{\mu}_j^2,\qquad j = 1, \ldots, d_\text{CLIP}. \tag{4.3}$$

The multivariate Gaussian entropy under the diagonal-plus-$\sigma^2 I$ approximation ([[2502.20946|DIFF-UQ]] Eq. 6; verified from `semantic_likelihood.py:17-36`) is

$$\mathcal{H}_\text{CLIP}(\hat{O}_{t+1}) \;=\; \tfrac{1}{2}\sum_{j=1}^{d_\text{CLIP}} \log\!\bigl(\mathrm{Var}_j + \sigma^2\bigr) \;+\; \tfrac{d_\text{CLIP}}{2}\bigl(\log(2\pi) + 1\bigr). \tag{4.4}$$

### 4.4 Combined per-timestep signal (==our design==)

==The additive combination with a learned $\lambda_\text{CLIP}$ below is our construction.== [[2502.20946|DIFF-UQ]] §3.3 reports Laplace predictive variance and CLIP semantic entropy as **two separate scalar channels** (each with its own calibration). Our 2×2 attribution gate requires a **single scalar per axis per timestep**, so we combine them additively:

$$\boxed{\; s_\text{imag}^\text{DIFF-UQ}(t; X) \;=\; \underbrace{\tfrac{1}{M}\sum_{m=1}^{M}\bigl\|\hat{O}_{t+1}^{(m)} - \bar{\hat{O}}_{t+1}\bigr\|_2^2}_{\text{Laplace predictive variance}} \;+\; \lambda_\text{CLIP}\,\mathcal{H}_\text{CLIP}(\hat{O}_{t+1})\;} \tag{4.5}$$

with $\lambda_\text{CLIP} \geq 0$ fit on held-out success rollouts per backbone so the two channels contribute comparable dynamic range. Channel ablations (S9): **Laplace-only** ($\lambda_\text{CLIP}=0$, allows $M = 1$) vs. **CLIP-only** (drop first term) vs. **combined** (above). The ablation is necessary because the additive combination is our contribution, not a sourced formula.

**Our contributions (flagged)**:

- ==Post-hoc fitting of (4.1) on UWM's / Cosmos Policy's DiT last layer== — neither paper performs this surgery; the anchor paper validates DIFF-UQ on ADM/UViT image models. Laplace-fit Hessian-conditioning is per-backbone (S2 sub-step: estimate #success-rollout-frames for a well-conditioned diagonal Laplace fit; 90M last layer ≈ $10^4$ frames; 2B last layer ≈ $10^5$ frames).
- ==Channel weight $\lambda_\text{CLIP}$ tuned per backbone on robot scenes== — CLIP was trained on web images; R9 ablation measures whether the CLIP channel transfers.

---

## 5. Act Signal #1 — FIPER-ACE

### 5.1 Anchor formulation (3-D actions, [[2510.09459|FIPER]] `fiper/evaluation/method_eval_classes/entropy_eval.py:56-104`)

For each step of the action chunk, FIPER places action endpoints onto a 3-D grid with per-dim cell size $\mathbf{c} = (c_x, c_y, c_z)$ and computes the **Shannon entropy of the resulting count vector** (base 2):

$$\mathcal{H}_\text{ACE}^{(3D)}\bigl(\{\mathbf{a}^{(i)}_t\}\bigr) \;=\; -\sum_{k=1}^{K_\text{cells}} \hat{p}_k \log_2 \hat{p}_k,\qquad \hat{p}_k = \frac{n_k}{\sum_{k'} n_{k'}},\quad n_k \text{ count in cell } k. \tag{5.1}$$

The cell size is set to a fixed fraction of per-dim range: $c_j = f \cdot (\max_i a^{(i)}_{t,j} - \min_i a^{(i)}_{t,j})$ with $f = 0.01$ (default). Per-chunk ACE averages over chunk steps:

$$s_\text{act}^\text{ACE, 3D}(t) \;=\; \frac{1}{H}\sum_{h=0}^{H-1} \mathcal{H}_\text{ACE}^{(3D)}\!\bigl(\{\mathbf{a}^{(i)}_{t+h}\}_i\bigr). \tag{5.2}$$

### 5.2 Dimensionality problem

LIBERO's action space is 7-D (6-DoF end-effector + 1-D gripper). A 7-D joint histogram at the same 1%-range resolution has $100^7 = 10^{14}$ cells and is **intractable**. Per-dim marginal binning discards joint structure; a bare 7-D joint histogram under-samples. R5 flags this as a high-severity risk requiring a rethink.

### 5.3 Our generalization (==our design==)

==We replace the 3-D joint histogram with one of two dimensionality-agnostic estimators, pre-registered before S5==:

**Variant A — per-dim marginal entropy sum**:

$$\boxed{\; s_\text{act}^{\text{ACE-marginal}}(t) \;=\; \frac{1}{H d_a}\sum_{h=0}^{H-1}\sum_{j=1}^{d_a} \mathcal{H}_\text{ACE}^{(1D)}\!\bigl(\{a^{(i)}_{t+h,j}\}_i\bigr) \;} \tag{5.3}$$

**Variant B — PCA-projected joint entropy**: project actions onto the top-$d'$ principal components ($d' = 3$ by default, fit on the calibration set), then apply (5.1) in $d'$-D:

$$\boxed{\; s_\text{act}^{\text{ACE-PCA}}(t) \;=\; \mathcal{H}_\text{ACE}^{(d')}\!\bigl(\{\mathrm{PCA}_{d'}(\mathbf{a}^{(i)}_{t+h})\}_{i,h}\bigr). \;} \tag{5.4}$$

Variant A is the default (parameter-free, interpretable, paper-honest); Variant B is the ablation cross-check. Variant A strictly generalizes (5.2) when $d_a = 3$ and the per-dim ranges dominate joint structure; Variant B strictly generalizes when $d_a > 3$ and principal variation is low-rank.

**Design note**: a KDE-based differential-entropy estimator (Kozachenko–Leonenko) was considered but rejected because it introduces a bandwidth hyperparameter that would need its own calibration pass, and differential entropy is not scale-invariant — both undesirable for a pre-registered protocol.

---

## 6. Act Signal #2 — Sentinel-STAC

### 6.1 MMD with RBF kernel ([[2410.04640|Sentinel]] `sentinel/bc/ood_detection/error_utils.py:62-93`)

Given two action sample sets $\mathbf{X} = \{\mathbf{x}^{(i)}\}_{i=1}^{K_\text{samp}},\; \mathbf{Y} = \{\mathbf{y}^{(j)}\}_{j=1}^{K_\text{samp}}$, the **biased V-statistic MMD$^2$ with RBF kernel** $k(x, y) = \exp(-\gamma\|x-y\|^2)$ used by Sentinel's code (verified `error_utils.py:90-93`, which computes `xx.mean() + yy.mean() - 2*xy.mean()` — **biased** form, includes diagonal $i{=}i'$ and $j{=}j'$ terms) is

$$\mathrm{MMD}^2_\text{biased}(\mathbf{X}, \mathbf{Y}) \;=\; \tfrac{1}{K_\text{samp}^2}\!\sum_{i,i'} k(\mathbf{x}^{(i)}, \mathbf{x}^{(i')}) \;+\; \tfrac{1}{K_\text{samp}^2}\!\sum_{j,j'} k(\mathbf{y}^{(j)}, \mathbf{y}^{(j')}) \;-\; \tfrac{2}{K_\text{samp}^2}\!\sum_{i,j} k(\mathbf{x}^{(i)}, \mathbf{y}^{(j)}). \tag{6.1}$$

**Note on estimator choice**: the **unbiased** U-statistic form uses $\tfrac{1}{K_\text{samp}(K_\text{samp}-1)}\sum_{i\neq i'}$ (Gretton et al. 2012, Eq. 3) and excludes diagonal terms. Sentinel's code uses the biased form; we follow Sentinel's convention for code-compatibility and because the bias ($O(K_\text{samp}^{-1})$) is negligible at $K_\text{samp}=256$.

Sentinel's default kernel bandwidth is the median pairwise distance heuristic: $\gamma = 1/(2 \cdot \mathrm{median}\{\|x - y\|^2\})$ (verified `error_utils.py:77-81`). Sentinel's paper headline uses $K_\text{samp} = 256$; the public `compute_mmd_rbf` operates on **all action dimensions** when called as `mmd_rbf_all` and on **position only** ($x,y,z$) when called as the default `mmd_rbf_pos`.

### 6.2 Our default — STAC-all over flattened chunk

==We pre-register `mmd_rbf_all` on the **full flattened action chunk** $\mathbf{a}^{(i)}_{t:t+H} \in \mathbb{R}^{H d_a}$== (not position-only), because the 2×2×2 design evaluates decorrelation on 7-DoF action spaces and position-only is the same ablation issue as FIPER-ACE's 3-D hardcoding (R5 mirror).

Per-timestep STAC-256 signal:

$$\boxed{\; s_\text{act}^\text{STAC-256}(t) \;=\; \mathrm{MMD}^2\!\bigl(\{\mathbf{a}^{(i)}_{t:t+H}\}_{i=1}^{256},\;\{\mathbf{a}^{(i)}_{t-1:t-1+H}\}_{i=1}^{256}\bigr). \;} \tag{6.2}$$

### 6.3 STAC-single ([[2506.09937|SAFE]] §5 fallback)

[[2506.09937|SAFE]] introduces a single-sample variant for compute-tight settings: compute MMD$^2$ between the **current single action chunk** $\mathbf{X} = \{\mathbf{a}_{t:t+H}\}$ (cardinality 1) and a calibration pool $\mathbf{Y} = \mathcal{P} = \{\mathbf{a}^{(j)}_\text{cal}\}_{j=1}^{K_\mathcal{P}}$ of success-rollout chunks. Because $|\mathbf{X}| = 1$, the X–X self-term in (6.1) reduces to a single $k(\mathbf{x}, \mathbf{x}) = 1$ (constant under RBF), giving

$$\boxed{\; s_\text{act}^\text{STAC-single}(t) \;=\; 1 \;+\; \tfrac{1}{K_\mathcal{P}^2}\!\sum_{j,j'} k(\mathbf{y}^{(j)}, \mathbf{y}^{(j')}) \;-\; \tfrac{2}{K_\mathcal{P}}\!\sum_{j} k(\mathbf{a}_{t:t+H},\, \mathbf{y}^{(j)}). \;} \tag{6.3}$$

The constant $+1$ is retained in the biased form for consistency with (6.1); it shifts the signal by a constant and does not affect CP calibration (which standardizes via per-timestep means in §8). This reduces per-step cost from $K_\text{samp} = 256$ diffusion samples of the action branch to 1, trading variance for ~2 orders of magnitude compute savings. Deployed by default on Cell 8 (Cosmos × DIFF-UQ × STAC) if compute-bound.

---

## 7. Episode Aggregation — Max-So-Far Convention

Per [[2510.09459|FIPER]] and [[2506.09937|SAFE]] conventions, we aggregate per-timestep signals into episode-level scores with the **max-so-far** operator (using $\omega$ for trajectory per §1):

$$\boxed{\; R_\text{imag}(\omega) \;=\; \max_{1 \leq t \leq T} s_\text{imag}(t),\qquad R_\text{act}(\omega) \;=\; \max_{1 \leq t \leq T} s_\text{act}(t). \;} \tag{7.1}$$

> [!info] Why max-so-far (not mean)
> (a) Failure detection needs *peak* anomaly, not average — a single severely off-manifold frame should trip the gate.
> (b) Max-so-far is monotonic in $t$: $R_\text{imag}(\omega, t) = \max_{s \leq t} s_\text{imag}(s)$ is non-decreasing, enabling early-warning T-det metrics.
> (c) Heavy-tailed — this motivates Spearman (rank) rather than Pearson (linear) correlation in all decorrelation analyses (§3.5.3, §8.5).

### 7.1 Formal statement

**Proposition 7.1 (Measurability).** If $s_\text{imag}, s_\text{act}: \{1,\ldots,T\} \to \mathbb{R}$ are measurable random functions of the trajectory $\omega$, then $R_\text{imag}(\omega), R_\text{act}(\omega)$ are measurable real-valued random variables as finite maxima of measurable functions.

**Proposition 7.2 (Exchangeability preservation).** If $\{\omega_i\}_{i=1}^N$ are exchangeable success rollouts and $s_\text{imag}, s_\text{act}$ are deterministic functions of $\omega$ (modulo independent sampling noise for STAC), then $\{R_\text{imag}(\omega_i)\}_{i=1}^N, \{R_\text{act}(\omega_i)\}_{i=1}^N$ remain exchangeable. This is the hypothesis Conformal Prediction requires.

---

## 8. Success-Only Functional Conformal Prediction + Bonferroni

### 8.1 Per-axis per-timestep CP (from [[2510.09459|FIPER]] §3.4; [[2503.08558|FAIL-Detect]] §3.3)

For each axis $X \in \{\text{imag}, \text{act}\}$, calibrate on $N$ success rollouts. Let $S_t^{X,(i)} = s_X(t)$ on rollout $i$. Define the per-timestep success mean

$$\mu_t^X \;=\; \tfrac{1}{N}\sum_{i=1}^{N} S_t^{X,(i)}. \tag{8.1}$$

Because failure detection flags anomalies only when $s_X(t)$ is **high** (not deviation in either direction), we use a **signed one-sided** deviation profile throughout — both in the nonconformity score and the threshold:

$$D^{(i)} \;=\; \max_{t} \frac{S_t^{X,(i)} - \mu_t^X}{h_t^X},\qquad h_t^X = \mathrm{MAD}\bigl(\{S_t^{X,(i)}\}_{i}\bigr) + \epsilon, \tag{8.2}$$

where MAD is median absolute deviation (robust to heavy tails; computed as $\mathrm{median}_i\,|S_t^{X,(i)} - \mathrm{median}_i\,S_t^{X,(i)}|$) and $\epsilon > 0$ prevents division by zero. The functional CP quantile at level $\alpha$ is

$$q_\alpha^X \;=\; \text{Quantile}_{1-\alpha}\!\bigl(\{D^{(i)}\}_{i=1}^N\bigr). \tag{8.3}$$

> **Signed vs. absolute deviation**: using signed deviation in (8.2) — $S - \mu$, not $|S - \mu|$ — aligns the calibration with the one-sided threshold in (8.4). Had we used $|S - \mu|$ and the $(1-\alpha)$-quantile for a one-sided threshold, each marginal would have been calibrated at $\alpha/2$ effective miscoverage (only the upper tail of an absolute-deviation quantile matters), making Bonferroni doubly conservative. Signed deviation gives the correct $\alpha/2$ marginal miscoverage per axis needed for the union-bound proof below.

### 8.2 Per-timestep threshold (one-sided, anomaly direction)

$$\tau_X(t) \;=\; \mu_t^X \;+\; q_\alpha^X \cdot h_t^X. \tag{8.4}$$

### 8.3 Bonferroni correction for joint FPR (==our design==)

Apply per-axis CP at level $\alpha/2$. By standard split-CP coverage (exchangeability of calibration + test, signed nonconformity scores, one-sided threshold) each marginal satisfies:

$$\mathbb{P}\!\bigl(R_\text{imag}(\omega_\text{test}) > \tau_\text{imag}(t_\text{test}) \;\big|\;\text{success}\bigr) \leq \alpha/2, \tag{8.5a}$$

$$\mathbb{P}\!\bigl(R_\text{act}(\omega_\text{test}) > \tau_\text{act}(t_\text{test}) \;\big|\;\text{success}\bigr) \leq \alpha/2, \tag{8.5b}$$

each under exchangeability of the calibration set and the test point.

### 8.4 Joint FPR guarantee (proof)

**Proposition 8.1 (Joint FPR control via Bonferroni).** Let $E_\text{imag} = \{R_\text{imag} > \tau_\text{imag}\}$ and $E_\text{act} = \{R_\text{act} > \tau_\text{act}\}$ denote the per-axis Type-I errors on a held-out success rollout. If (8.5a)–(8.5b) hold at level $\alpha/2$ each, then

$$\mathbb{P}(E_\text{imag} \cup E_\text{act} \mid \text{success}) \;\leq\; \mathbb{P}(E_\text{imag}) + \mathbb{P}(E_\text{act}) \;\leq\; \tfrac{\alpha}{2} + \tfrac{\alpha}{2} \;=\; \alpha. \tag{8.6}$$

**Proof**. Union bound on the probability of the union of two events; validity of each marginal CP guarantee follows from the exchangeability assumption of standard split CP (Vovk, Gammerman & Shafer, 2005; applied to functional CP in [[2510.09459|FIPER]] Appendix A).

$\qed$

**Corollary**. $\mathbb{P}(\text{any false alarm}) \leq \alpha$, so the 2×2 cell-label assignment **Success = cell `00`** has miscoverage $\leq \alpha$. This is the joint-coverage claim our gate makes.

### 8.5 Why Bonferroni (not copula) for the headline

Bonferroni is conservative: it assumes worst-case positive dependence between $E_\text{imag}$ and $E_\text{act}$. If the two axes are approximately independent (H2 target: $\rho < 0.7$), Bonferroni over-protects, and a copula-quantile joint CP would be tighter. **Headline uses Bonferroni**; S9 ablation measures the empirical gap to an empirical-copula lower bound.

---

## 9. The 2×2 Attribution Gate (Per Cell)

### 9.1 Binary axis decisions

Given per-cell thresholds $\tau_\text{imag}(t), \tau_\text{act}(t)$, the per-episode binary decisions are

$$b_\text{imag}(\omega) = \mathbb{1}\!\bigl[R_\text{imag}(\omega) > \tau_\text{imag}(t^*)\bigr],\qquad b_\text{act}(\omega) = \mathbb{1}\!\bigl[R_\text{act}(\omega) > \tau_\text{act}(t^*)\bigr], \tag{9.1}$$

where $t^* = \arg\max_t s_X(t)$ is the first-exceedance time (or any fixed horizon end; the choice affects T-det but not Top-1 accuracy).

### 9.2 Label function

The 4-cell attribution label $\ell: \{0,1\}^2 \to \{00, 01, 10, 11\}$ is given by the 2×2 cross-tabulation:

| $b_\text{imag}$ | $b_\text{act}$ | Label $\ell$ | Semantics |
|:---:|:---:|:---:|---|
| 0 | 0 | `00` **Success** | Both axes within success band |
| 0 | 1 | `01` **Action failure** | WM on-manifold, action head anomalous |
| 1 | 0 | `10` **Imagination failure** | WM off-manifold, action head within band |
| 1 | 1 | `11` **Joint failure** | Both axes anomalous |

$$\boxed{\; \ell(\omega) \;=\; \bigl(b_\text{imag}(\omega),\; b_\text{act}(\omega)\bigr)_2 \quad\in\{00, 01, 10, 11\}. \;} \tag{9.2}$$

Every cell of the 2×2×2 factorial instantiates **the same** $\ell$ under its own signal implementations and thresholds.

---

## 10. Correctness Claims (A, B, C, D) — Formal Propositions + Falsifiers

Each claim is restated as a formal proposition, paired with a pre-registered hypothesis-test statistic and threshold constituting its falsifier.

### 10.1 Claim A — Both imag signals discriminate imag failure

> **Proposition A.** For each backbone $X \in \{A, B\}$, the imag signal $s_\text{imag} \in \{\text{logpZO}, \text{DIFF-UQ}\}$ separates success from `10`-class rollouts, i.e.
> $$\mathrm{AUROC}\bigl(s_\text{imag}\;;\;\text{success vs. } c{=}10\bigr) \;\geq\; 0.70. \tag{10.A.1}$$

**Falsifier (S9 ablation)**: per backbone, fit ROC on 500 success + 500 `10`-class rollouts. **Statistic**: empirical AUROC $\hat{A}$. **Pre-registered threshold**: reject Proposition A if $\hat{A} + 1.96 \cdot \mathrm{SE}(\hat{A}) < 0.70$ (one-sided 95% CI upper bound below target). For `logpZO`: additionally compare $\hat{A}_{O_t}$ vs. $\hat{A}_{\hat{O}_{t+1}}$ to isolate the ==our extension== (§3.2) effect.

### 10.2 Claim B — Cross-side non-leakage (weakest claim)

> **Proposition B.** For each cell $c$ of the 2×2×2, the imag signal responds to imag corruption but not to pure act corruption, and vice versa:
> $$\mathrm{Recall}_{10} \geq 0.60,\quad \mathrm{Recall}_{01} \geq 0.60,\quad \text{per cell}. \tag{10.B.1}$$

**Falsifier (§5.3.2 confusion matrix)**: per-cell 4×4 confusion matrix on $500 \times 4$ injected-failure rollouts. **Statistic**: per-cell recall on rows `10` and `01`. **Pre-registered threshold**: reject Proposition B for cell $c$ if either recall is below 0.60. H4 requires Proposition B to hold in **$\geq 6$ of 8 cells** (descriptive; see Prop. 12.2 for cluster-robust primary test).

**Relation to H1 (Top-1 target)**. $\mathrm{Recall}_{c}$ is the row-recall on the 4×4 confusion matrix: $\mathrm{Recall}_c = \mathbb{P}(\hat\ell = c \mid \text{true class} = c)$. Under uniform injected-class priors (500 rollouts per class × 4 classes = 2000 injected rollouts, §5.3.2 of Roadmap), the overall Top-1 is the mean of the diagonal:
$$\mathrm{Top\text{-}1} = \tfrac{1}{4}\bigl(\mathrm{Recall}_{00} + \mathrm{Recall}_{01} + \mathrm{Recall}_{10} + \mathrm{Recall}_{11}\bigr). \tag{10.B.2}$$
$\mathrm{Recall}_{00} \geq 1 - \alpha = 0.90$ follows from the joint FPR control of Prop. 8.1. The remaining three recalls are empirical — Claim B pre-registers the $\mathrm{Recall}_{10},\mathrm{Recall}_{01} \geq 0.60$ falsifier; $\mathrm{Recall}_{11}$ is reported alongside but not pre-registered (both axes fire by design under joint corruption, so the floor is expected to be high but is not a falsifier). The H1 target of 75% is a pre-registered aspiration given these inputs; the 70% floor is the kill-gate.

### 10.3 Claim C — Joint calibration under exchangeability

> **Proposition C.** Under exchangeability of calibration and test sets, per-cell Bonferroni-corrected functional CP controls joint FPR at level $\alpha$:
> $$\mathbb{P}\bigl(\ell(\omega_\text{test}) \neq 00 \;\big|\;\text{success}\bigr) \leq \alpha. \tag{10.C.1}$$

**Proof**: Proposition 8.1 above.

**Falsifier**: empirical per-cell FPR on held-out success set. **Statistic**: $\widehat{\mathrm{FPR}}_c = \frac{1}{N_\text{held}} \sum_i \mathbb{1}[\ell(\omega_i) \neq 00]$. **Pre-registered threshold**: reject Proposition C for cell $c$ if $\widehat{\mathrm{FPR}}_c > \alpha + 0.03$; switch that cell to copula-quantile variant.

### 10.4 Claim D — Imag-axis internal decorrelation (new for 2×2×2)

> **Proposition D.** The two imag signals are empirically decorrelated on success rollouts:
> $$\rho_S\bigl(R_\text{logpZO},\; R_\text{DIFF-UQ}\bigr) < 0.6 \quad\text{on both backbones}. \tag{10.D.1}$$

**Falsifier (S3.1 pilot)**: 100 success rollouts per backbone. **Statistic**: Spearman $\hat{\rho}_S$ with Fisher-z 95% CI. **Pre-registered thresholds** (per §0 of Roadmap):

- $\hat{\rho}_S < 0.6$ (upper CI) on both backbones → commit to 2×2×2.
- $\hat{\rho}_S > 0.85$ (lower CI) on either backbone → reject Proposition D; demote DIFF-UQ to ablation; collapse to 2×2 (Cells 1/2/5/6).
- Intermediate → proceed with caveat.

Fisher-z SE with $n=100$ is $\mathrm{SE}(z) = 1/\sqrt{n-3} \approx 0.1015$. Back-transformed to the $\rho$ scale at $\rho = 0.85$: $z = \mathrm{arctanh}(0.85) \approx 1.256$; 95% CI on $z$ is $[1.057, 1.455]$; 95% CI on $\rho_S$ is $\tanh([1.057, 1.455]) \approx [0.785, 0.897]$. Half-width ≈ 0.056 — enough resolution to distinguish 0.70 from 0.85 at ~80% power per backbone.

---

## 11. Injected-Failure Protocol — Output-Token Level

### 11.1 Why output-token injection (not weight-module)

Neither UWM nor Cosmos Policy has distinct WM and action weight modules. "Weight-module injection" (AdaWorldPolicy-style) is **structurally undefined** on a single shared DiT. We inject at the modality-output boundary — i.e., on the final DiT output tokens before the modality-specific decoder $\mathcal{D}_m$.

**Important caveat**. Injecting $\delta_v$ on video-output tokens and $\delta_a$ on action-output tokens does **not mathematically guarantee** that $s_\text{imag}$ responds only to $\delta_v$ and $s_\text{act}$ responds only to $\delta_a$. Both modalities share upstream weights $\theta$ and shared visual tokenizers; perturbing output tokens does not perturb the shared upstream pathway. Cross-side separability (Claim B, §10.2) is therefore an **empirical property to be measured**, not a property that output-token injection enforces by construction. The 2×2×2 factorial is specifically designed to quantify this separability via per-cell confusion matrices.

### 11.2 Formal noise model per class

Let $z_m^{(K)} \in \mathbb{R}^{N_m \times d}$ be the final DiT output tokens for modality $m$ (video vs. action). Per class $c \in \{00, 01, 10, 11\}$, we define a **corruption operator** $\mathcal{C}_c$:

$$\mathcal{C}_c\bigl(z_\text{video}^{(K)}, z_\text{action}^{(K)}\bigr) \;=\; \bigl(z_\text{video}^{(K)} + \delta_v,\;\; z_\text{action}^{(K)} + \delta_a\bigr), \tag{11.1}$$

where $\delta_v, \delta_a$ are class-dependent additive Gaussian noise:

| Class $c$ | $\delta_v$ (video-tokens) | $\delta_a$ (action-tokens) | GT label |
|---|---|---|:---:|
| `00` Clean | $0$ | $0$ | $00$ |
| `10` Imag | $\epsilon_v,\; \epsilon_v \sim \mathcal{N}(0, \sigma^2_\mathrm{inj,v} I)$ | $0$ | $10$ |
| `01` Act | $0$ | $\epsilon_a,\; \epsilon_a \sim \mathcal{N}(0, \sigma^2_\mathrm{inj,a} I)$ | $01$ |
| `11` Joint | $\epsilon_v$ | $\epsilon_a$ | $11$ |

### 11.3 Injection during rollout

Corruption is applied **mid-episode** at a uniformly sampled timestep $t_\text{inj} \sim \mathcal{U}(\lfloor 0.25 T \rfloor, \lfloor 0.75 T \rfloor)$ and persists until end-of-episode. Injection is applied independently at each affected $t \geq t_\text{inj}$ to avoid stationarity confounds.

### 11.4 $\sigma_\mathrm{inj}$ calibration (pre-registered before S5)

For each backbone $X$ and each affected modality $m$, measure the per-scalar activation standard deviation $\sigma_\phi^{X,m}$ on success rollouts (average per-element std across all token positions and feature channels):

$$\sigma_\phi^{X,m} \;=\; \sqrt{\tfrac{1}{|\mathcal{D}_\text{cal}| \cdot N_m \cdot d}\sum_{\omega \in \mathcal{D}_\text{cal}} \bigl\|z_m^{(K)}(\omega) - \bar{z}_m^{(K)}\bigr\|_F^2}, \tag{11.2}$$

where $\|\cdot\|_F$ is Frobenius norm over the $N_m \times d$ token tensor. The division by $N_m \cdot d$ under the sqrt yields per-scalar std (not per-token).

Sweep $\sigma_\mathrm{inj} \in \{0.1, 0.5, 1.0\} \cdot \sigma_\phi^{X,m}$; pre-register the **smallest** $\sigma_\mathrm{inj}$ that produces a measurable drop in rollout success rate (say, ≥ 10 pp on a held-out LIBERO task). This keeps the injected-failure suite task-hard rather than signal-hard — failures must be plausible within the backbone's own dynamics.

---

## 12. 2×2×2 Factorial Composition

### 12.1 Cell structure

Each cell $c \in \{1, \ldots, 8\}$ is defined by a triple $(X, S_\text{imag}, S_\text{act})$ where $X \in \{A, B\}$, $S_\text{imag} \in \{\text{logpZO}, \text{DIFF-UQ}\}$, $S_\text{act} \in \{\text{ACE}, \text{STAC}\}$. Every cell instantiates:

1. The same backbone interface (§2).
2. Its own per-timestep signals $s_\text{imag}(t), s_\text{act}(t)$ (§3–6).
3. The same max-so-far aggregation (§7).
4. Its own per-cell CP calibration at level $\alpha/2$ per axis (§8).
5. The same 2×2 attribution gate $\ell$ (§9).

### 12.2 Per-cell FPR control (shared CP + Bonferroni)

**Proposition 12.1 (Per-cell FPR).** For each cell $c$, under exchangeability of its calibration set $\mathcal{D}_\text{cal}^{(c)}$ and test point:

$$\mathbb{P}\!\bigl(\ell_c(\omega_\text{test}) \neq 00 \;\big|\;\text{success}\bigr) \;\leq\; \alpha. \tag{12.1}$$

**Proof**. Apply Proposition 8.1 to each cell independently; the calibration set, signal implementations, and thresholds are cell-specific but the framework is identical. $\qed$

### 12.3 Dependence of cell-level inferences — honest framing

**Proposition 12.2 (Cross-cell dependence structure).** The per-cell FPR guarantees in (12.1) each hold **conditional on exchangeability within that cell's calibration set**. However, the 8 cells are **not statistically independent** in general:

- Cells 1–4 share backbone A (UWM); cells 5–8 share backbone B (Cosmos Policy). Within a backbone, calibration rollouts $\{\omega_i^{(A)}\}$ and action samples $\{\mathbf{a}^{(i),(A)}\}$ are **reused across the 4 cells** that use that backbone.
- Cells 1 and 3 share backbone A and act signal ACE — they differ only in imag signal (logpZO vs. DIFF-UQ). Their $R_\text{imag}$ values are computed on the *same* $\hat{O}_{t+1}$ frames.

**Effective independent units**: not 8. Under strongest dependence (full agreement within backbone), n_eff ≈ 2 (one per backbone). Under H2/D holding (signals decorrelated), n_eff is between 2 and 8.

**Corollary — H4 binomial test with cluster-robust framing**. The naive binomial test $\mathbb{P}(\mathrm{Bin}(8, \pi_\text{pass}) \geq 6)$ assumes 8 independent trials and is **anti-conservative** when cells within a backbone share data. Two pre-registered options:

1. **Conservative backbone-level test** (primary): $\mathbb{P}(\text{H4}_\text{backbone-level})$ = probability both backbones have $\geq 3$ of 4 cells passing. Under $\pi_\text{pass} = 0.80$ per cell and within-backbone cell outcomes treated as exchangeable (but not independent), a conservative bound via Markov inequality gives $\approx 0.60$.

2. **Cluster-robust binomial** (ablation): treat each backbone as a block; estimate effective $n_\text{eff}$ via bootstrap resampling of backbones; compute binomial $p$-value with $n_\text{eff}$ trials.

$$\mathbb{P}\bigl(\text{H4 passes (backbone-level)}\bigr) \;=\; \mathbb{P}\bigl(\text{at least 3 of 4 cells pass per backbone, both backbones}\bigr). \tag{12.2}$$

The naive Bin(8, $\pi$)-based statistic is reported only as a descriptive upper bound on the effective pass rate, not as the test statistic for H4.

### 12.4 S3.1 gate as formal hypothesis test

> **S3.1 Gate (H5)**: Decide whether to run 8 cells or 4.

**Test statistic**: Spearman's $\hat{\rho}_S$ on $n = 100$ success rollouts per backbone. Fisher-z transform:

$$z \;=\; \tfrac{1}{2}\log\!\frac{1 + \hat{\rho}_S}{1 - \hat{\rho}_S},\qquad \mathrm{SE}(z) \;=\; \tfrac{1}{\sqrt{n-3}}. \tag{12.3}$$

**95% CI on $\rho_S$**: back-transform $z \pm 1.96 \cdot \mathrm{SE}(z)$.

**Pre-registered decision rule (3-way, per-backbone, must hold on both)**:

| $\hat{\rho}_S$ 95% CI | Decision |
|---|---|
| Upper bound $< 0.60$ on both | Commit to 2×2×2 (8 cells) |
| Lower bound $> 0.85$ on either | Collapse to 2×2 (Cells 1/2/5/6); demote DIFF-UQ to S9 ablation |
| Else | Proceed with caveat; flag in write-up; H4 claimed only on backbone with upper bound $< 0.60$ |

The test is paired per backbone because DIFF-UQ's Laplace is scale-dependent (90M vs. 2B).

### 12.5 Winning-cell selection (S4)

> **S4 Gate (H2)**: Per committed cell, measure $\hat{\rho}_c = \rho_S(R_\text{imag}, R_\text{act})$ on 500 success rollouts.

$$c^\star \;=\; \arg\min_{c \in \mathcal{C}_\text{committed}} \hat{\rho}_c, \tag{12.4}$$

with the constraint $\hat{\rho}_{c^\star} < 0.7$. If all committed cells violate $\hat{\rho}_c < 0.7$, S4 kill triggers (Plan B pivot per §7 of Roadmap).

---

## 13. Composition Proof — End-to-End Well-Definedness

> **Theorem 13.1 (Whole-pipeline well-definedness and FPR control).** Under the exchangeability of success rollouts within each cell's calibration set, the 2×2×2 attribution gate defined by §2–§11 satisfies:
>
> 1. **Well-definedness**: every map in §2–§9 is measurable and has finite, deterministic outputs for any well-formed episode $\omega$.
> 2. **Per-cell FPR control**: for each cell $c$, $\mathbb{P}(\ell_c(\omega_\text{test}) \neq 00 \mid \text{success}) \leq \alpha$.
> 3. **Cross-cell inference (descriptive)**: H4 is evaluated under the cluster-robust framing of Prop. 12.2. The primary test is the backbone-level criterion (≥ 3 of 4 cells passing within *each* backbone); the naive Bin(8, $\pi_\text{pass}$) "≥ 6 of 8 cells" statistic is reported descriptively only, with the explicit caveat that within-backbone cells share calibration data so the effective number of independent trials is $n_\text{eff} \in [2, 8]$. At $n_\text{eff}=2$ backbones, H4 is a descriptive generality statement, not an inferential claim with nominal Type-I control.
> 4. **Decorrelation kill gate**: S3.1 Spearman CI on $n=100$ per backbone has Fisher-z SE $\approx 0.10$. At true $\rho_S=0.85$, CI on $\rho_S$ is $\approx [0.785, 0.897]$; power to distinguish 0.70 from 0.85 is ~80% per backbone under the pre-registered 3-way decision rule (§12.4).

**Proof sketch by component chain**:

| § | Component | Input | Output | Property invoked |
|---|---|---|---|---|
| 2 | DiT forward | $(o_{1:t}, l)$ | $(\hat{O}_{t+1}, \mathbf{a}_{t:t+H}, \phi_t)$ | Deterministic mod. diffusion noise; flow-matching well-defined [[2504.02792\|UWM]], [[2601.16163\|Cosmos Policy]] |
| 3 | logpZO | $\hat{O}_{t+1}$ | $s^\text{logpZO}(t)$ | (3.2) is a continuous function of CNF output; CNF is a trained Lipschitz ODE flow [[2503.08558\|FAIL-Detect]] |
| 4 | DIFF-UQ | $(\hat{O}_{t+1}^{(m)}, \phi_t)$ | $s^\text{DIFF-UQ}(t)$ | Diagonal Laplace posterior is a valid Gaussian approximation [[2502.20946\|DIFF-UQ]]; CLIP entropy is a continuous function of variance (M≥2 required) |
| 5 | ACE | $\{\mathbf{a}^{(i)}_{t+h}\}$ | $s^\text{ACE}(t)$ | Shannon entropy is well-defined on finite multinomials; our generalizations (5.3)–(5.4) are strict extensions for $d_a \neq 3$ |
| 6 | STAC | $\{\mathbf{a}^{(i)}_{t:t+H}\}$ | $s^\text{STAC}(t)$ | Biased MMD$^2$ V-statistic is well-defined for any $K_\text{samp} \geq 1$; RBF kernel is characteristic [[2410.04640\|Sentinel]] |
| 7 | Max-so-far | $s_X(1:T)$ | $R_X(\omega)$ | Prop. 7.1–7.2: measurability + exchangeability preserved |
| 8 | CP | $\{R_X^{(i)}\}$, $\alpha/2$ | $\tau_X(t)$ | Standard split-CP coverage under exchangeability with signed one-sided scores [[2510.09459\|FIPER]] Appx A |
| 9 | Gate | $(R_\text{imag}, R_\text{act}, \tau_\text{imag}, \tau_\text{act})$ | $\ell \in \{00,01,10,11\}$ | Deterministic cross-tab |
| 10 | Claims | Prop. A–D | Falsifiers | Hypothesis tests with pre-registered thresholds |
| 11 | Injection | $z_m^{(K)}$ | $z_m^{(K)} + \delta_m$ | Measurable translation; $\sigma_\mathrm{inj}$ pre-registered |
| 12 | Factorial | 8× pipelines | $\{\ell_c\}_{c=1}^8$ | Prop. 12.1–12.2: per-cell Bonferroni + cross-cell binomial |

**Each row shows**: inputs are well-defined → the operation is measurable / differentiable / deterministic → outputs feed the next row. Exchangeability for CP is inherited from frozen backbones + i.i.d. success-rollout sampling. Bonferroni over-protects under any positive dependence between axes, so (8.6) is conservative and cannot be violated by empirical signal correlations.

**Per-cell FPR (part 2)** follows from Prop. 12.1, which applies Prop. 8.1 (proved via union bound on (8.5a)–(8.5b)) to each cell's own calibration set.

**Part (3) — cross-cell framing**. Cells 1–4 share UWM calibration data; cells 5–8 share Cosmos Policy calibration data; cells 1/3 and 5/7 share $\hat{O}_{t+1}$ across the imag axis. Therefore the 8 cell-level pass/fail outcomes are **not independent Bernoulli trials**, and Proposition 12.2's cluster-robust framing replaces the naive binomial. The **primary H4 test** is the backbone-level statistic (both backbones independently hit ≥ 3 of 4 cells at Top-1 ≥ 70%); the "≥ 6 of 8 cells" statistic is reported descriptively with a note that $n_\text{eff} \in [2, 8]$. At $n_\text{eff} = 2$ backbones the generality claim is **descriptive, not inferential**.

**Part (4) — S3.1 Fisher-z CI at $n=100$**. SE on $z$ is $1/\sqrt{97} \approx 0.1015$; 95% CI half-width on $z$ is $1.96 \cdot 0.1015 \approx 0.199$. At true $\rho_S = 0.85$ the CI on $\rho_S$ is $\tanh(\mathrm{arctanh}(0.85) \pm 0.199) \approx [0.785, 0.897]$. The 3-way decision rule (§12.4) commits on lower $\rho_S$, collapses on high $\rho_S$, and carries an intermediate "proceed with caveat" branch for ambiguous outcomes.

$\qed$

---

## 14. Summary Table — Contributions vs. Sourced Components

| Section | Component | Source | Our delta |
|---|---|---|---|
| 2 | Diffusion-WAM forward | [[2504.02792\|UWM]] §3; [[2601.16163\|Cosmos Policy]] §3 | Unified notation covering both decoupling mechanisms |
| 3.1 | CNF training / inference | [[2503.08558\|FAIL-Detect]] §3.4 | — (verbatim) |
| 3.2 | ==logpZO on $\hat{O}_{t+1}$== | — | ==Novel: re-train CNF on predicted frames, per-backbone== |
| 4.1–4.4 | Laplace + CLIP combined | [[2502.20946\|DIFF-UQ]] §3.1–3.3 | Per-backbone Laplace fit on DiT last layer; $\lambda_\text{CLIP}$ robot-scene calibration |
| 5.1 | 3-D ACE | [[2510.09459\|FIPER]] `entropy_eval.py:56-104` | — |
| 5.3–5.4 | ==ACE generalization== | — | ==Novel: per-dim marginal + PCA fallback for 7-DoF== |
| 6.1 | MMD-RBF kernel | [[2410.04640\|Sentinel]] `error_utils.py` | — |
| 6.2 | ==STAC-all default== | — | ==Pre-registered `mmd_rbf_all` on full 7-D chunk== |
| 6.3 | STAC-single | [[2506.09937\|SAFE]] §5 | — |
| 7 | Max-so-far aggregation | [[2510.09459\|FIPER]], [[2506.09937\|SAFE]] | Formal statement (Prop. 7.1–7.2) |
| 8.1–8.2 | Functional CP | [[2510.09459\|FIPER]] §3.4 | — |
| 8.3–8.4 | ==Bonferroni joint correction== | — | ==Novel: $\alpha/2$ per axis + union-bound proof (8.6)== |
| 9 | 2×2 cross-tab | — | ==Replaces FIPER's AND-gate with structured attribution== |
| 10 | Claims A–D | — | Falsifiers pre-registered |
| 11 | ==Output-token injection== | — | ==Novel: compromise protocol for shared-DiT backbones== |
| 12 | 2×2×2 factorial | — | ==Novel: first factorial evaluation of dual-signal CP attribution== |
| 13 | Composition proof | — | ==Full end-to-end proof== |

---

## Cross-References

- [[00_Self-Discovering-WAM-Summary]] — one-page pitch
- [[01_Self-Discovering-WAM-Literature]] — anchor elevation, lit scan
- [[02_Self-Discovering-WAM-Roadmap]] — execution steps, kill gates, risk register
- [[04_Mathematical-Formulation-Self-Evolving-WAM|First publication: Self-Evolving-WAM math]] — structural template

---

*Mathematical companion to [[02_Self-Discovering-WAM-Roadmap|roadmap]].*
