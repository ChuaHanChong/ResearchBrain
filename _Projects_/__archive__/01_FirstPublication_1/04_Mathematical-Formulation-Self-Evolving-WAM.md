---
title: "Mathematical Formulation: Self-Evolving WAM (Fast-WAM + VLA-JEPA)"
tags:
  - self-evolving
  - WAM
  - Fast-WAM
  - VLA-JEPA
  - mathematics
  - methodology
aliases:
  - "Self-Evolving WAM Math"
  - "Fast-WAM Formulation"
  - "VLA-JEPA Formulation"
---

# Mathematical Formulation: Self-Evolving WAM

> [!abstract] Purpose
> Step-by-step mathematical proof that the combined methods in the self-evolving loop compose correctly. Each step shows: input → formula → output → how it feeds the next step. Formulas sourced from cited papers are marked; novel contributions are explicitly labeled as ==our design==.

> [!info] Notation Conventions
> - $a_{1:H} \in \mathbb{R}^{H \times d_a}$ — action chunk (H steps, $d_a$ dimensions per step)
> - $o$ — observation, $l$ — language instruction
> - $z$ — latent state (world model space), $e$ — VLA hidden state (feature space)
> - $f_\theta$ — Fast-WAM velocity field, $v_\theta$ — VLA-JEPA velocity field
> - $a_\delta$ — residual correction, $\bar{a} = a_{\text{base}} + a_\delta$ — combined action, $\xi \in (0,1]$ — residual bound
> - $E$ — encoder (Wan2.2 VAE for Fast-WAM, V-JEPA2 target encoder for VLA-JEPA)
> - $\epsilon \sim \mathcal{N}(0, I)$ — Gaussian noise, $t \in [0, 1]$ — flow matching timestep

---

## 1. Base: Flow Matching Action Generation

Both base models generate action chunks $a_{1:H}$ via ==conditional flow matching==, but use **opposite time conventions**.

### 1A. Fast-WAM ([[2603.16666|Fast-WAM]])

Fast-WAM learns a velocity field $f_\theta$ that transports noise $\epsilon$ to data $y$ (Eq. 5-6):

$$L_{FM}^{\text{FW}}(y) = \mathbb{E}_{y, \epsilon, t} \left[ \|f_\theta(y_t, t, o, l) - (\epsilon - y)\|_2^2 \right]$$

where $y_t = (1-t)y + t\epsilon$ ($t{=}0$: clean data, $t{=}1$: noise), $o$ is observation, $l$ is language instruction.

**Two branches trained jointly via MoT** (Eq. 9):

$$L_{\text{total}}^{\text{FW}} = L_{\text{act}} + \lambda \cdot L_{\text{vid}}$$

| Branch | What $y$ represents | Output |
|--------|-------------------|--------|
| **ActionDiT** | $y = a_{1:H}$ (action chunk) | $L_{\text{act}} = L_{FM}^{\text{FW}}(a_{1:H})$ |
| **Video DiT** | $y = z_{1:T}$ (future frame latents) | $L_{\text{vid}} = L_{FM}^{\text{FW}}(z_{1:T})$ |

**Inference** (deterministic ODE, Euler integration from noise to data):

$$\frac{da_\tau}{d\tau} = f_\theta(a_\tau, \tau, o, l), \quad a_0 \sim \mathcal{N}(0, I) \xrightarrow{\text{solve ODE}} a_1 = \text{action chunk}$$

### 1B. VLA-JEPA ([[2602.10098|VLA-JEPA]])

VLA-JEPA uses the ==reversed time convention== (Eq. 7-8): $t{=}0$ is noise, $t{=}1$ is data.

$$a_t = (1-t)\epsilon + t \cdot a_{0:H}, \quad t \sim \mathcal{U}(0,1), \quad \epsilon \sim \mathcal{N}(0,I)$$

$$L_{FM}^{\text{VJ}} = \mathbb{E}_{a_{0:H}, \epsilon, t} \left[ \|v_\theta(a_t, t \mid z_a) - (a_{0:H} - \epsilon)\|_2^2 \right]$$

where $z_a = p_\theta^{VLM}(\langle\text{action}\rangle \mid I_{t_0}, l, \langle\text{latent}\rangle)$ is the VLM-derived action-conditioning representation (Eq. 6), not raw observations. The action head is a DiT conditioned on $z_a$ via cross-attention.

**Joint training with world model** (Eq. 9):

$$L_{\text{total}}^{\text{VJ}} = L_{FM}^{\text{VJ}} + \beta \cdot L_{WM}$$

where $L_{WM}$ is the V-JEPA2 world model loss (see Step 2).

**Inference** (Euler integration from noise to data, same direction as Fast-WAM despite reversed $t$):

$$a_0 \sim \mathcal{N}(0, I), \quad a_{k+1} = a_k + \frac{1}{N} v_\theta(a_k, t_k \mid z_a) \quad \text{for } t_k = k/N$$

> [!info] Time Convention Note
> Fast-WAM: $y_t = (1{-}t)\cdot\text{data} + t\cdot\text{noise}$, target velocity $= \epsilon - y$ (noise minus data).
> VLA-JEPA: $a_t = (1{-}t)\cdot\text{noise} + t\cdot\text{data}$, target velocity $= a - \epsilon$ (data minus noise).
> These are mathematically equivalent (mirrored time direction). Both produce valid action chunks $a_{1:H}$ from the same distribution.

> **Output of Step 1**: A trained action model that produces action chunks $a_{1:H}$, plus a world model — Video DiT (Fast-WAM) or V-JEPA2 predictor (VLA-JEPA) — that predicts future latent states.

---

## 2. DETECT: Multi-Signal Failure Detection

Use ==three complementary detection signals==, each targeting a different failure mode. Their combination is strictly more powerful than any single signal.

### 2.1 VLA Feature Probing ([[2506.09937|SAFE]])

The VLA's own internal features contain ==task-generic information about success and failure== — failed rollouts cluster in a distinct failure region in the latent space regardless of task ([[2506.09937|SAFE]], NeurIPS 2025). This provides a lightweight, architecture-agnostic detection signal.

**Feature probing**: At each timestep, extract the VLA's last-layer hidden state $e_t \in \mathbb{R}^D$ (before action decoding). A small MLP $g: \mathbb{R}^D \to \mathbb{R}$ maps this to a scalar failure score:

$$s_t = \sigma(g(e_t)), \quad S_t^{\text{SAFE}} = \frac{1}{t} \sum_{\tau=1}^{t} s_\tau$$

where $\sigma$ is the sigmoid function. The running mean $S_t^{\text{SAFE}}$ accumulates evidence of failure over the trajectory — it increases monotonically as more failure indicators appear.

**Training loss** (requires only trajectory-level success/failure labels, no per-step annotation):

$$L_{\text{SAFE}} = \sum_i \left[ y_i \sum_t \text{ReLU}(S_t) + (1 - y_i) \sum_t w_t \cdot (-S_t) \right]$$

where $y_i = 1$ for success (push scores toward zero), $y_i = 0$ for failure (push scores up), and $w_t$ is a time-weighting that emphasizes later steps where failures become clearer.

**Conformal prediction threshold** (principled statistical guarantee, replacing ad-hoc heuristics):

Calibrate on $N_{\text{cal}} \approx 50$ successful rollouts. Compute a prediction trajectory $\mu_t = \text{mean}(S_t^{\text{cal}})$ and an adaptive modulation envelope $h_t$ from the calibration set (normalized deviation of calibration trajectories from $\mu_t$). For significance level $\alpha \in (0, 1)$:

$$\text{upper}_t = \mu_t + q_\alpha \cdot h_t$$

where $q_\alpha$ is the $(1{-}\alpha)$-quantile of $\max_t |S_t^{\text{cal}} - \mu_t| / h_t$ over calibration trajectories ([[2506.09937|SAFE]], functional conformal prediction from Xu et al. 2102.06746). This guarantees that for any new successful rollout, $S_t < \text{upper}_t$ for all $t$ with probability $\geq 1 - \alpha$.

$$\text{Flag failure at time } t \text{ if } S_t^{\text{SAFE}} > \text{upper}_t$$

This signal detects ==VLA confidence failures== — "the model's internal representation looks like a failure trajectory." It adds <1ms overhead and generalizes zero-shot to unseen tasks.

### 2.2 World Model Prediction Error (inspired by [[2602.20057|AdaWorldPolicy]])

Complementary to VLA feature probing: while Section 2.1 detects failures from the VLA's internal confidence, prediction error detects ==world model understanding failures== — "the physics here surprises me."

**Fast-WAM**: Video DiT predicts the next observation in Wan2.2 VAE latent space via iterative denoising:

$$\hat{z}_{t+1} = \text{Denoise}(\text{VideoDiT}, z_t, a_t), \quad z_{t+1} = E(o_{t+1})$$

$$L_{\text{pred}}^{\text{FW}}(t) = \|z_{t+1} - \hat{z}_{t+1}\|_2^2$$

**VLA-JEPA**: V-JEPA2's latent predictor (dormant at inference by default — must be explicitly activated) predicts in V-JEPA2 feature space via a single forward pass:

$$\hat{z}_{t+1}^{\text{JEPA}} = \text{VJ2\_Predictor}(z_t^{\text{target}}, z_{a_t})$$

$$L_{\text{pred}}^{\text{VJ}}(t) = \|z_{t+1}^{\text{target}} - \hat{z}_{t+1}^{\text{JEPA}}\|_1$$

where $z^{\text{target}}$ is V-JEPA2's frozen target encoder output (stop-gradient) and $z_{a_t}$ are VLM-derived action tokens. Fast-WAM uses L2 norm (pixel-level VAE space); VLA-JEPA uses L1 norm (semantic feature space, confirmed by [[2602.10098|VLA-JEPA]] Eq. 5).

**Episode-level aggregation** (==our design==):

$$S_{\text{env}}(\tau) = \frac{1}{T} \sum_{t=1}^{T} L_{\text{pred}}(t), \quad \text{flag if } S_{\text{env}}(\tau) > \mu_S + 2\sigma_S$$

where $\mu_S, \sigma_S$ are rolling mean and standard deviation across recent episodes.

### 2.3 Action-Chunk Entropy ([[2510.09459|FIPER]], optional)

Action-chunk entropy (ACE) measures the ==sharpness of the FM action distribution== — high entropy means the model is unsure which action to take, providing a third orthogonal signal.

### 2.4 Multi-Signal Fusion (==our design==)

Three signals detect different failure modes. Flag an episode as hard if ==at least 2 of 3 signals== fire simultaneously (reduces false positives from any single noisy signal):

$$\mathcal{D}_{\text{hard}} = \left\{\tau : \geq 2 \text{ of } \begin{cases} S_t^{\text{SAFE}} > \text{upper}_t & \text{(VLA confidence failure)} \\ S_{\text{env}}(\tau) > \mu_S + 2\sigma_S & \text{(world model surprise)} \\ \text{ACE}(\tau) > \theta_{\text{ACE}} & \text{(action uncertainty)} \end{cases}\right\}$$

> **Output of Step 2**: A set of ==hard episodes== $\mathcal{D}_{\text{hard}}$ — episodes where the model is failing, the world model is surprised, or the action head is uncertain. These feed into Step 3 (EXPLORE).

---

## 3. EXPLORE: Multi-Level Weakness Discovery

### 3a. Action Uncertainty via Flow-SDE ([[2510.25889|πRL]], [[2505.05470|Flow-GRPO]])

Convert the action model's deterministic ODE to a ==Stochastic Differential Equation== for diverse action sampling. Applies to both Fast-WAM (ActionDiT) and VLA-JEPA (FM action head).

**Original ODE** (deterministic — one noise seed → one action):

$$da_\tau = f_\theta(a_\tau, \tau, o, l) \, d\tau$$

**Flow-SDE** (stochastic — same seed → diverse actions):

$$da_\tau = \underbrace{\left[f_\theta(a_\tau, \tau, o, l) + \frac{\sigma_\tau^2}{2\tau}\left(a_\tau + (1-\tau)f_\theta\right)\right]}_{\text{corrected drift}} d\tau + \underbrace{\sigma_\tau \, dw_\tau}_{\text{stochastic noise}}$$

where $\sigma_\tau = \alpha\sqrt{\frac{\tau}{1-\tau}}$ controls the noise level, and $dw_\tau$ is a Wiener process. This SDE has the ==same marginal distribution== as the original ODE ([[2505.05470|Flow-GRPO]]) — it doesn't change what the model can generate, only enables stochastic sampling.

**Action uncertainty** (==our proposed metric==): Run $N$ samples from the SDE for the same observation:

$$\text{Var}_{\text{action}}(o) = \frac{1}{N} \sum_{i=1}^{N} \|a_{1:H}^{(i)} - \bar{a}_{1:H}\|_2^2$$

> **Output of Step 3a**: Per-observation ==action uncertainty== $\text{Var}_{\text{action}}(o)$. High variance = the model is unsure what to do.

### 3b. Behavioral Probing via SOE VIB ([[2509.19292|SOE]])

SOE learns a ==compact latent representation== $z$ of task-relevant information via a Variational Information Bottleneck (VIB).

**VIB Encoder** (compress observation to compact latent):

$$z \sim p_\theta(z|o) = \mathcal{N}(\mu_\theta(o), \sigma_\theta^2(o))$$

**VIB Loss** (trade off reconstruction vs compression):

$$L_{\text{VIB}} = \underbrace{-\mathbb{E}_{z \sim p_\theta(z|o)} \left[\log q_\phi(a|z)\right]}_{\text{action reconstruction}} + \underbrace{\beta \cdot \text{KL}\left[p_\theta(z|o) \| \mathcal{N}(0, I)\right]}_{\text{information bottleneck}}$$

**Exploration** (perturb the compressed representation beyond the learned variance):

$$\tilde{z} = \mu_\theta(o) + \alpha \cdot \sigma_\theta(o) \cdot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I), \quad \alpha > 1$$

**VIB-FM adaptation** (replacing DDPM noise prediction with flow matching velocity):

$$L_{\text{VIB-FM}} = \mathbb{E}_{z \sim p_\theta(z|o)} \left[\|f_\theta(a_t, t, \tilde{z}, o, l) - v_{\text{target}}\|_2^2\right] + \beta \cdot \text{KL}\left[p_\theta(z|o) \| \mathcal{N}(0, I)\right]$$

where $v_{\text{target}} = \epsilon - a$ for Fast-WAM, $v_{\text{target}} = a - \epsilon$ for VLA-JEPA.

**Behavioral boundary** (==our proposed definition==; SOE ablates $\alpha$ but does not define $\alpha^*$):

$$\alpha^* = \min \{\alpha : \text{success}(\tilde{a}_{1:H}(\alpha)) < 0.5\}$$

Small $\alpha^*$ = fragile behavior. Large $\alpha^*$ = robust behavior.

> **Output of Step 3b**: Per-observation ==behavioral fragility== $\alpha^*(o)$.

### 3c. Environment Adversary via RoboMD ([[2412.02818|RoboMD]])

RoboMD trains an RL adversary $\pi_{\text{adv}}$ (optimized via PPO) that searches for failure-inducing environment configurations. It is ==policy-agnostic==: it treats the target policy as a black box.

**Adversary's MDP**: State $s \in \mathcal{E} \subset \mathbb{R}^{512}$ (semantic embedding from ViT+CLIP dual backbone), Action = variation in embedding space.

$$\pi_{\text{adv}}^* = \arg\max_{\pi_{\text{adv}}} \mathbb{E}_{\pi_{\text{adv}}} \left[\sum_t R(s_t, a_t)\right]$$

**Reward function** (RoboMD Eq. 2):

$$R(s, a) = \begin{cases} \frac{K_{\text{fail}}}{\text{penalty}+1} - k \cdot \mathcal{N}(a) & \text{if target policy fails} \\ -\frac{K_{\text{success}}}{\text{horizon}} \cdot \left(\frac{1000}{\text{penalty}} + 1\right) & \text{if target policy succeeds} \end{cases}$$

where $\text{penalty} = \min_{e \in \mathcal{E}_{\text{known}}} \|a - e\|$ encourages exploration away from known embeddings, and $\mathcal{N}(a)$ is a frequency penalty discouraging repetitive actions.

> **Output of Step 3c**: A ranked set of ==failure-inducing environment configurations== $\mathcal{E}_{\text{hard}} = \{e_1, e_2, \ldots\}$.

---

## 4. PROBE + LEARN: Layered Residual Recovery

Deploy the base model in the hard scenarios ($\mathcal{D}_{\text{hard}}$ from Step 2, $\mathcal{E}_{\text{hard}}$ from Step 3c). Train a ==residual specialist== to recover from failures using three layers of increasing sophistication.

### 4.1 Residual Off-Policy RL ([[2509.19301|ResFiT]])

The core idea: freeze the base policy and train a lightweight residual correction $a_\delta$ on top of it.

**Residual actor**: The actor takes observation features and the base policy's action as input, and outputs a bounded residual correction:

$$\mu_\delta = \xi \cdot \tanh\!\left(\text{MLP}([e_{\text{obs}}, a_{\text{base}}])\right)$$

$$a_\delta \sim \text{TruncatedNormal}(\mu_\delta, \sigma_{\text{explore}}), \quad \bar{a} = a_{\text{base}} + a_\delta$$

where $e_{\text{obs}}$ is the observation feature from the base model's encoder, $a_{\text{base}}$ is the frozen base model's action, and $\xi \in (0, 1]$ bounds the residual magnitude. The Tanh ensures $\mu_\delta \in [-\xi, +\xi]$, and $\sigma_{\text{explore}}$ is the exploration noise (annealed during training).

**Distributional critic** (HLGauss): Instead of predicting a scalar Q-value, predict a categorical distribution over returns — more expressive and stable for long-horizon tasks:

$$Q_\phi(s, \bar{a}) = \sum_{k=1}^{K} p_k \cdot c_k, \quad p = \text{softmax}\!\left(\text{MLP}([e_{\text{obs}}, \bar{a}])\right)$$

where $c_k$ are $K$ equally-spaced bin centers in $[V_{\min}, V_{\max}]$, and $p_k$ is the predicted probability for each bin. The critic loss is cross-entropy between the predicted distribution and a Gaussian-smoothed target centered on the TD target.

**Key design choice** (confirmed by [[2602.01789|RFS]] ablation): The critic must be conditioned on the ==final combined action $\bar{a} = a_{\text{base}} + a_\delta$==, not on separate components. Conditioning on separate $a_{\text{base}}$ and $a_\delta$ leads to training instability.

### 4.2 PLD Enhancements ([[2511.00091|PLD]])

Three improvements layered on top of the residual RL baseline:

**4.2a. SAC entropy bonus** (replace TD3 deterministic actor with stochastic SAC):

$$J_\pi = \mathbb{E}_{s \sim \mathcal{D}} \left[Q(s, \bar{a}) - \alpha \log \pi(a_\delta \mid s, a_{\text{base}})\right]$$

The entropy term $-\alpha \log \pi$ encourages diverse recovery strategies — the specialist explores different ways to recover from the same failure state. The temperature $\alpha$ is auto-tuned via dual gradient descent on target entropy $\mathcal{H}_{\text{target}} = -d_a$.

**4.2b. Cal-QL conservative warmup** (stable offline → online transition):

$$L_{\text{CalQL}} = L_{\text{TD}} + \alpha_{\text{cql}} \left(\log \sum_{a'} \exp Q(s, a') - \log N - \mathbb{E}_{a \sim \mathcal{D}_{\text{offline}}}[Q(s, a)]\right)$$

Pre-train the critic on offline successful base policy rollouts before online RL. The conservative penalty prevents Q-value overestimation for out-of-distribution actions, ensuring that the critic's value estimates are reliable when the specialist begins online exploration. PLD was validated on π0 (flow matching) and OpenVLA (autoregressive), confirming compatibility with both base models.

**4.2c. Hybrid data collection** (base probes, specialist recovers):

$$\tau_{\text{PLD}} = \underbrace{\{(o_1, a_1^{\text{base}}), \ldots, (o_k, a_k^{\text{base}})\}}_{\text{base policy explores (may fail)}} \cup \underbrace{\{(o_{k+1}, \bar{a}_{k+1}), \ldots, (o_T, \bar{a}_T)\}}_{\text{specialist recovers from failure}}$$

where $k \sim \text{Uniform}(0, T)$ is the random handoff point. This produces diverse training data that includes both base-policy-explored states AND specialist-recovered states.

### 4.3 Chunk-Aware Q + Dual Modulation ([[2507.07969|Q-chunking]], [[2602.01789|RFS]])

**4.3a. Chunk-Aware Q-Function** ([[2507.07969|Q-chunking]])

Both base models produce H-step action chunks. A per-step Q-function evaluates each action independently, ignoring temporal coherence within the chunk. Q-chunking defines a Q-function over the ==entire chunk jointly==:

**Chunk-aware critic** (architecture-agnostic — same for both models):

$$Q(s_t, a_{t:t+h-1}) \leftarrow \sum_{t'=t}^{t+h-1} \gamma^{t'-t} r_{t'} + \gamma^h Q(s_{t+h}, a_{t+h:t+2h-1})$$

Action chunks are flattened: $a_{t:t+h-1} \in \mathbb{R}^{H \times d_a} \to \mathbb{R}^{H \cdot d_a}$. The $\gamma^h$ discounting propagates reward information $h$ steps backward per update, matching the action chunk horizon. The critic is convention-agnostic — it operates on flattened action vectors regardless of how they were generated.

**Chunk-aware actor** (convention-specific — must match the base model's flow matching direction):

For **VLA-JEPA** ($t{=}0$ noise, $t{=}1$ data):

$$x_t = (1-t)\epsilon + t \cdot a_{1:H}, \quad v_{\text{target}} = a_{1:H} - \epsilon$$

$$L_{\text{actor}}^{\text{VJ}} = \mathbb{E}\left[\|v_\phi(x_t, t, s) - v_{\text{target}}\|_2^2\right] - \lambda_Q \cdot Q(s, a_{1:H})$$

For **Fast-WAM** ($t{=}0$ data, $t{=}1$ noise):

$$y_t = (1-t) \cdot a_{1:H} + t \cdot \epsilon, \quad v_{\text{target}} = \epsilon - a_{1:H}$$

$$L_{\text{actor}}^{\text{FW}} = \mathbb{E}\left[\|v_\phi(y_t, t, s) - v_{\text{target}}\|_2^2\right] - \lambda_Q \cdot Q(s, a_{1:H})$$

In both cases, the actor is trained with a flow matching loss (first term) regularized by the Q-function (second term, $\lambda_Q > 0$). The flow matching loss keeps the actor close to the base policy; the Q-function guides it toward higher-value actions.

**4.3b. RFS Dual Modulation** ([[2602.01789|RFS]])

Upgrade the residual-only actor to ==joint noise steering + residual==, enabling both global behavioral shifts and local corrections:

$$\pi_{\text{RFS}}(a_0, a_\delta \mid s), \quad a_{\text{base}} = \text{Denoise}(s, a_0, v_\theta), \quad \bar{a} = a_{\text{base}} + a_\delta$$

where $a_0$ is the ==learned initial noise== (steered, not sampled randomly), $v_\theta$ is the frozen flow-matching velocity field, and $a_\delta$ is the residual correction.

- **Input modulation** ($a_0$ steering): induces ==global behavioral shifts== — the specialist selects qualitatively different actions by choosing different starting points in noise space.
- **Output modulation** ($a_\delta$ residual): provides ==local fine-grained corrections== — precise adjustments for execution errors.

This combination enables the policy to expand beyond the demonstration data manifold: noise steering explores new behavioral modes while residual corrections ensure precision. Pure residual RL (Sections 4.1-4.2) can only make local corrections near the base action; RFS additionally enables global mode shifts.

**Actor loss**:

$$L_{\text{RFS}} = -Q(s, \bar{a}) + \lambda_{\text{BC}} \|a_\delta\|_2^2$$

The BC regularizer on $a_\delta$ (not on $a_0$) keeps residual corrections small while allowing unrestricted noise steering. The critic is conditioned on the final combined action $\bar{a}$.

> **Output of Step 4**: A dataset of ==recovery trajectories== $\mathcal{D}_{\text{recovery}} = \{\tau_{\text{PLD}}\}$ — successful trajectories that include recovery from failure states. These are the self-generated training data.

---

## 5. DISTILL: LoRA Fine-Tune

Fine-tune the action model on recovery data using LoRA adapters, preserving the base model's general competence.

**LoRA parameterization** (low-rank update to attention weights):

$$W' = W_0 + \Delta W = W_0 + AB$$

where $W_0 \in \mathbb{R}^{d \times d}$ is the frozen pre-trained weight, $A \in \mathbb{R}^{d \times r}$, $B \in \mathbb{R}^{r \times d}$, $r = 32 \ll d$.

| Base Model | LoRA Target | $d$ |
|-----------|------------|-----|
| **Fast-WAM** | ActionDiT attention layers (non-mixed only; Video DiT frozen) | 1024 |
| **VLA-JEPA** | FM action head DiT layers (V-JEPA2 predictor frozen) | Action head dim |

**Training loss** (flow matching on recovery data + replay, ==our design== combining data sources):

$$L_{\text{distill}} = \underbrace{\mathbb{E}_{(o,a^*) \sim \mathcal{D}_{\text{recovery}}} \left[L_{FM}\right]}_{\text{learn from recovery data}} + \underbrace{\mathbb{E}_{(o,a^*) \sim \mathcal{D}_{\text{replay}}} \left[L_{FM}\right]}_{\text{2\% replay prevents forgetting}}$$

where $L_{FM}$ uses the base model's own velocity convention: $\|f_\theta(\cdot) - (\epsilon - a^*)\|_2^2$ for Fast-WAM, $\|v_\theta(\cdot) - (a^* - \epsilon)\|_2^2$ for VLA-JEPA.

**LoRA update rule:**

$$A, B \leftarrow A, B - \eta \nabla_{A,B} L_{\text{distill}}$$

Only $A, B$ are updated — $W_0$ remains frozen. This constrains updates to a rank-$r$ subspace, preventing catastrophic changes (<2% forgetting on π0, [[2603.11653|VLA-RL-CL]]).

> **Output of Step 5**: ==Updated action model== with LoRA adapters that encode the recovery behaviors.

---

## 6. DREAM: World Model Imagination (==our design==)

The frozen world model generates additional training data via imagination, amplifying the recovery signal without requiring more environment interaction.

**Fast-WAM**: Video DiT (frozen) generates future latent frames via iterative denoising:

$$\hat{z}_{1:T} = \text{Denoise}(\text{VideoDiT}, z_0, a_{1:H}^{\text{proposed}})$$

**VLA-JEPA**: V-JEPA2 predictor (frozen) generates future states in feature space via a single forward pass (cheaper than Video DiT):

$$\hat{z}_{1:T}^{\text{JEPA}} = \text{VJ2\_Predictor}(z_0^{\text{target}}, z_{a}^{\text{proposed}})$$

Note: V-JEPA2 dreams are latent features, not decodable to pixel observations. They condition the action head directly via $z_a$ tokens.

**Dream quality filter** (==our design==):

$$\text{Keep dream if } \text{Var}_{\text{action}}(o_{\text{initial}}) < \theta_{\text{dream}}$$

where $\text{Var}_{\text{action}}$ is computed by running the LoRA-updated action model on the initial observation and checking action consistency via Flow-SDE (Step 3a). Low variance = the action model is confident about what to do in this scenario, so the dream is likely meaningful.

> **Output of Step 6**: Additional ==dream trajectories== $\mathcal{D}_{\text{dream}}$ added to recovery data for the next round.

---

## 7. MEASURE: Benchmark Evaluation

After each round, evaluate on held-out OOD benchmarks:

$$\text{Score}_k^{(n)} = \text{SuccessRate}(\pi_{\theta}^{(n)}, \mathcal{B}_k)$$

where $\pi_\theta$ is the base model (Fast-WAM or VLA-JEPA), $k \in \{\text{LIBERO-PRO}, \text{LIBERO-X}, \text{LIBERO-Para}, \text{GM-100}\}$, and $n$ is the round number.

**Convergence criterion:**

$$\Delta_k^{(n)} = \text{Score}_k^{(n)} - \text{Score}_k^{(n-1)} > 0 \quad \text{for } \geq 3 \text{ consecutive } n$$

**Regression check:**

$$\text{Score}_{\text{LIBERO}}^{(n)} > 0.98 \times \text{Score}_{\text{LIBERO}}^{(0)}$$

If standard LIBERO drops more than 2%, increase replay ratio in Step 5.

---

## Composition Proof: Why the Methods Chain Correctly

The key question: do the outputs of each step correctly feed the inputs of the next? We verify for **both** base models.

| Step | Output | Feeds Into | Compatible with Both Models? |
|------|--------|-----------|------------------------------|
| **1. Base** | Action chunks $a_{1:H}$ + future latents | Steps 2, 3 | Yes — both use FM to produce $a_{1:H} \in \mathbb{R}^{H \times d_a}$ |
| **2. DETECT** | Hard episodes $\mathcal{D}_{\text{hard}}$ | Steps 3, 4 | Yes — SAFE uses VLA hidden states (any VLA); prediction error uses each model's own world model |
| **3a. Flow-SDE** | Action variance $\text{Var}_{\text{action}}(o)$ | Steps 4, 6 | Yes — SDE preserves marginal for any FM model ([[2505.05470\|Flow-GRPO]]) |
| **3b. SOE VIB** | Behavioral fragility $\alpha^*(o)$ | Step 4 | Yes — VIB is decoder-agnostic (only reconstruction loss changes) |
| **3c. RoboMD** | Hard environments $\mathcal{E}_{\text{hard}}$ | Step 4 | Yes — policy-agnostic black box |
| **4. Residual Recovery** | Recovery data $\mathcal{D}_{\text{recovery}}$ | Step 5 | Yes — residual is additive in action space; PLD tested on π0 + OpenVLA |
| **5. DISTILL** | LoRA-updated model $W' = W_0 + AB$ | Step 1 (next round) | Yes — LoRA on ActionDiT (FW) or action head DiT (VJ); world models frozen |
| **6. DREAM** | Dream data $\mathcal{D}_{\text{dream}}$ | Step 5 | Yes — each model dreams in its own latent space (internally consistent) |

### Why Each Connection Works

1. **Shared action space**: Both models produce $a_{1:H} \in \mathbb{R}^{H \times d_a}$ via flow matching. All EXPLORE and PROBE mechanisms interface through this shared action space, not through architecture-specific internals.

2. **SAFE is architecture-agnostic**: The MLP detector operates on last-layer hidden states that exist in any VLA. It was tested directly on pi0, pi0-FAST, and OpenVLA — architecturally diverse models ([[2506.09937|SAFE]]).

3. **Multi-signal fusion is orthogonal**: SAFE detects VLA confidence failures. Prediction error detects world model surprise. ACE detects action uncertainty. These are independent signals — requiring ≥2 to fire filters transient noise.

4. **Flow-SDE preserves marginal**: The ODE → SDE conversion preserves $p(a|o,l)$ — stochastic exploration generates actions from the same distribution as the deterministic model. This holds for any FM model ([[2505.05470|Flow-GRPO]]).

5. **Residual RL is additive in action space**: $\bar{a} = a_{\text{base}} + a_\delta$ operates in action space, not model internals. The correction doesn't depend on how $a_{\text{base}}$ was generated. Validated on both FM (π0) and autoregressive (OpenVLA) models ([[2511.00091|PLD]]).

6. **Layered improvements compose additively**: ResFiT residual (4.1) → PLD SAC/Cal-QL (4.2) → Q-chunking/RFS (4.3) are additive upgrades. Each layer modifies a component without breaking the others: 4.2 replaces TD3 with SAC (same interface); 4.3a upgrades per-step Q to chunk Q (richer input); 4.3b adds noise steering (strictly more expressive — reduces to pure residual when $a_0$ is fixed).

7. **RFS preserves FM structure**: $\bar{a} = \text{Denoise}(s, a_0, v_\theta) + a_\delta$ — the frozen velocity field $v_\theta$ is unmodified. Steering $a_0$ only changes the starting point; the residual $a_\delta$ is additive. Both preserve the FM ODE/SDE structure ([[2602.01789|RFS]]).

8. **LoRA preserves FM structure**: $W' = W_0 + AB$ is a rank-$r$ perturbation. The velocity field with perturbed weights still satisfies the FM structure. For Fast-WAM, LoRA targets non-mixed-attention layers (preserving Video DiT alignment). For VLA-JEPA, LoRA targets the action head DiT (V-JEPA2 remains frozen).

9. **Consistent latent spaces**: Fast-WAM: prediction error and dreams both use Wan2.2 VAE space. VLA-JEPA: both use V-JEPA2 feature space. Different from each other, but internally consistent within each model.

---

## The Full Self-Evolving Loop as One Equation

Combining all steps into one optimization objective per round $n$:

$$\theta^{(n+1)} = \theta^{(n)} + \Delta\theta, \quad \Delta\theta = AB \text{ (LoRA update)}$$

The LoRA parameters are trained on:

$$L^{(n)} = \underbrace{\mathbb{E}_{\mathcal{D}_{\text{recovery}}^{(n)}} \left[L_{FM}\right]}_{\text{recovery data (Step 4)}} + \underbrace{\mathbb{E}_{\mathcal{D}_{\text{SOE}}^{(n)}} \left[L_{FM}\right]}_{\text{SOE successes (Step 3b)}} + \underbrace{\mathbb{E}_{\mathcal{D}_{\text{dream}}^{(n)}} \left[L_{FM}\right]}_{\text{world model dreams (Step 6)}} + \underbrace{\mathbb{E}_{\mathcal{D}_{\text{replay}}} \left[L_{FM}\right]}_{\text{2\% replay buffer}}$$

where $L_{FM} = L_{FM}^{\text{FW}}$ (target $\epsilon - y$) for Fast-WAM, or $L_{FM} = L_{FM}^{\text{VJ}}$ (target $a - \epsilon$) for VLA-JEPA.

The self-generated data comes from three discovery mechanisms:

**Recovery data** (from residual RL on hard scenarios):

$$\mathcal{D}_{\text{recovery}}^{(n)} = \text{PLD}\!\left(\pi_{\theta^{(n)}}, \; \mathcal{D}_{\text{hard}}^{(n)} \cup \mathcal{E}_{\text{hard}}^{(n)}\right)$$

**SOE exploration successes** (from active behavioral probing):

$$\mathcal{D}_{\text{SOE}}^{(n)} = \left\{\tilde{a}_{1:H} : \text{SOE}(\alpha, o) \text{ succeeds} \wedge \alpha > \alpha^*_{\text{prev}}\right\}$$

**Hard episode discovery** (from multi-signal fusion):

$$\mathcal{D}_{\text{hard}}^{(n)} = \left\{\tau : \geq 2 \text{ of } \left\{S_t^{\text{SAFE}} > \text{upper}_t, \; S_{\text{env}}(\tau) > \mu_S + 2\sigma_S, \; \text{Var}_{\text{action}}(o) > \theta_{\text{var}}\right\}\right\}$$

This is a ==fixed-point iteration==: the model generates its own training signal, improves, then generates a new signal from the improved model. Convergence is measured externally via OOD benchmarks (Step 7). The three detection signals (SAFE, prediction error, action variance) discover different failure modes; the three recovery mechanisms (residual RL, SOE probing, world model dreams) address them. The loop terminates when OOD performance converges or regresses.

---

*Mathematical companion to [[02_How-to-Build-a-Light-Fast-Self-Evolving-WAM|methodology]] and [[03_Research-Roadmap-Self-Evolving-WAM|roadmap]].*
