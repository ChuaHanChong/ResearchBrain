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
> Step-by-step mathematical proof that the combined methods in the self-evolving loop compose correctly. Each step shows: input → formula → output → how it feeds the next step. Formulas sourced from cited papers are marked; novel contributions (our design) are explicitly labeled.

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

where $L_{WM}$ is the V-JEPA2 world model loss (see Step 2B).

**Inference** (Euler integration from noise to data, same direction as Fast-WAM despite reversed $t$):

$$a_0 \sim \mathcal{N}(0, I), \quad a_{k+1} = a_k + \frac{1}{N} v_\theta(a_k, t_k \mid z_a) \quad \text{for } t_k = k/N$$

> [!info] Time Convention Note
> Fast-WAM: $y_t = (1{-}t)\cdot\text{data} + t\cdot\text{noise}$, target velocity $= \epsilon - y$ (noise minus data).
> VLA-JEPA: $a_t = (1{-}t)\cdot\text{noise} + t\cdot\text{data}$, target velocity $= a - \epsilon$ (data minus noise).
> These are mathematically equivalent (mirrored time direction). Both produce valid action chunks $a_{1:H}$ from the same distribution.

> **Output of Step 1**: A trained action model that produces action chunks $a_{1:H}$, plus a world model — Video DiT (Fast-WAM) or V-JEPA2 predictor (VLA-JEPA) — that predicts future latent states.

---

## 2. DETECT: World Model Prediction Error

Use the world model's prediction error as an environment-level discovery signal for episodes the model doesn't understand.

### 2A. Fast-WAM: Video DiT Prediction Error (inspired by [[2602.20057|AdaWorldPolicy]])

Video DiT predicts the next observation in ==latent space== via iterative denoising (Wan2.2 VAE encoder $E$):

$$\hat{z}_{t+1} = \text{Denoise}(\text{VideoDiT}, z_t, a_t)$$

Compare with actual next observation encoded by the same VAE (AdaWorldPolicy Eq. 5):

$$z_{t+1} = E(o_{t+1})$$

$$L_{\text{pred}}^{\text{FW}}(t) = \|z_{t+1} - \hat{z}_{t+1}\|_2^2$$

### 2B. VLA-JEPA: V-JEPA2 Prediction Error ([[2602.10098|VLA-JEPA]])

V-JEPA2's latent predictor (==dormant at inference by default== — must be explicitly activated) predicts the next observation in ==V-JEPA2 feature space== via a single forward pass (no denoising needed):

$$\hat{z}_{t+1}^{\text{JEPA}} = \text{VJ2\_Predictor}(z_t^{\text{target}}, z_{a_t})$$

where $z^{\text{target}}$ is V-JEPA2's frozen target encoder output (stop-gradient) and $z_{a_t}$ are VLM-derived action tokens (not raw actions). World model loss uses ==L1 norm== (Eq. 5, confirmed by code `F.l1_loss`):

$$L_{\text{pred}}^{\text{VJ}}(t) = \|z_{t+1}^{\text{target}} - \hat{z}_{t+1}^{\text{JEPA}}\|_1$$

> [!info] Latent Space Difference
> Fast-WAM operates in Wan2.2 VAE latent space (pixel-level, expensive). VLA-JEPA operates in V-JEPA2 feature space (semantic-level, cheap). The $L_{\text{pred}}$ values are not directly comparable between the two, but serve the same role: flagging surprising episodes.

### Episode-Level Aggregation (==our design==)

**Episode-level surprise score** (not from AdaWorldPolicy — our formulation for episode-level flagging):

$$S_{\text{env}}(\tau) = \frac{1}{T} \sum_{t=1}^{T} L_{\text{pred}}(t)$$

**Flagging threshold** (rolling statistics, ==our design==):

$$\text{Flag episode if } S_{\text{env}}(\tau) > \mu_S + 2\sigma_S$$

where $\mu_S, \sigma_S$ are rolling mean and standard deviation across recent episodes. AdaWorldPolicy uses per-step prediction error for online LoRA updates; our episode-level aggregation is a novel adaptation.

> **Output of Step 2**: A set of ==high-surprise episodes== $\mathcal{D}_{\text{hard}} = \{\tau : S_{\text{env}}(\tau) > \text{threshold}\}$ — environments the world model doesn't understand. These feed into Step 3 (EXPLORE) as the scenarios to probe further.

---

## 3a. EXPLORE (Action Uncertainty): πRL Flow-SDE ([[2510.25889|πRL]], [[2505.05470|Flow-GRPO]])

Convert the action model's deterministic ODE to a ==Stochastic Differential Equation== for diverse action sampling. Applies to both Fast-WAM (ActionDiT) and VLA-JEPA (FM action head).

**Original ODE** (deterministic — one noise seed → one action):

$$da_\tau = f_\theta(a_\tau, \tau, o, l) \, d\tau$$

**Flow-SDE** (stochastic — same seed → diverse actions):

$$da_\tau = \underbrace{\left[f_\theta(a_\tau, \tau, o, l) + \frac{\sigma_\tau^2}{2\tau}\left(a_\tau + (1-\tau)f_\theta\right)\right]}_{\text{corrected drift}} d\tau + \underbrace{\sigma_\tau \, dw_\tau}_{\text{stochastic noise}}$$

where $\sigma_\tau = \alpha\sqrt{\frac{\tau}{1-\tau}}$ controls the noise level, and $dw_\tau$ is a Wiener process.

**Key property** ([[2505.05470|Flow-GRPO]]): This SDE has the ==same marginal distribution== as the original ODE — it doesn't change what the model can generate, only enables stochastic sampling.

**Action uncertainty signal** (==our proposed metric==): Run $N$ samples from the SDE for the same observation:

$$a_{1:H}^{(1)}, a_{1:H}^{(2)}, \ldots, a_{1:H}^{(N)} \sim \text{Flow-SDE}(o, l)$$

$$\text{Var}_{\text{action}}(o) = \frac{1}{N} \sum_{i=1}^{N} \|a_{1:H}^{(i)} - \bar{a}_{1:H}\|_2^2$$

> **Output of Step 3a**: Per-observation ==action uncertainty== $\text{Var}_{\text{action}}(o)$. High variance = the model is unsure what to do → potential action-level weakness.

---

## 3b. EXPLORE (Action Active Probing): SOE VIB ([[2509.19292|SOE]])

SOE learns a ==compact latent representation== $z$ of task-relevant information via a Variational Information Bottleneck (VIB).

**VIB Encoder** (compress observation to compact latent, configurable $d \in [16, 64]$; effective dims $\sim 8\text{-}16$ via SNR):

$$z \sim p_\theta(z|o) = \mathcal{N}(\mu_\theta(o), \sigma_\theta^2(o))$$

**VIB Loss** (trade off reconstruction vs compression):

$$L_{\text{VIB}} = \underbrace{-\mathbb{E}_{z \sim p_\theta(z|o)} \left[\log q_\phi(a|z)\right]}_{\text{action reconstruction}} + \underbrace{\beta \cdot \text{KL}\left[p_\theta(z|o) \| \mathcal{N}(0, I)\right]}_{\text{information bottleneck}}$$

**Exploration** (perturb the compressed representation):

$$\tilde{z} = \mu_\theta(o) + \alpha \cdot \sigma_\theta(o) \cdot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

where $\alpha > 1$ amplifies the perturbation beyond the learned variance.

**Adapted VIB reconstruction loss for flow matching** (replacing DDPM noise prediction):

$$L_{\text{VIB-FM}} = \underbrace{\mathbb{E}_{z \sim p_\theta(z|o)} \left[\|f_\theta(a_t, t, \tilde{z}, o, l) - (\epsilon - a)\|_2^2\right]}_{\text{FM velocity prediction conditioned on perturbed } \tilde{z}} + \underbrace{\beta \cdot \text{KL}\left[p_\theta(z|o) \| \mathcal{N}(0, I)\right]}_{\text{information bottleneck (unchanged)}}$$

**Decode to action via the base model's flow matching head**:

$$\tilde{a}_{1:H} = \text{FM\_Head}(\tilde{z}, o, l) \quad \text{(conditioned on perturbed } \tilde{z} \text{)}$$

**Behavioral boundary mapping** (==our proposed definition==; SOE ablates $\alpha$ but does not define $\alpha^*$): For each observation, sweep $\alpha$ from 1.0 to 3.0 and record where task success drops:

$$\alpha^* = \min \{\alpha : \text{success}(\tilde{a}_{1:H}(\alpha)) < 0.5\}$$

Small $\alpha^*$ = fragile behavior (breaks easily). Large $\alpha^*$ = robust behavior.

> **Output of Step 3b**: Per-observation ==behavioral fragility== $\alpha^*(o)$. Low $\alpha^*$ = the model's behavior is fragile here → ==active weakness found==.

---

## 3c. EXPLORE (Environment Active Probing): RoboMD ([[2412.02818|RoboMD]])

RoboMD trains an RL adversary $\pi_{\text{adv}}$ (optimized via PPO) that searches for failure-inducing environment configurations.

**Adversary's MDP** $\langle S, A, P, R, \gamma \rangle$: State $s \in \mathcal{E} \subset \mathbb{R}^{512}$ (semantic embedding), Action = variation in embedding space, Reward = shaped failure signal.

$$\pi_{\text{adv}}^* = \arg\max_{\pi_{\text{adv}}} \mathbb{E}_{\pi_{\text{adv}}} \left[\sum_t R(s_t, a_t)\right]$$

**Reward function** (RoboMD Eq. 2; simplified from the shaped reward which includes distance penalty and repetition penalty $\mathcal{N}(a)$):

$$R(s, a) = \begin{cases} \frac{K_{\text{fail}}}{\text{penalty}+1} - k \cdot \mathcal{N}(a) & \text{if target policy fails} \\ -\frac{K_{\text{success}}}{\text{horizon} \times (\text{penalty}+1)} & \text{if target policy succeeds} \end{cases}$$

where $\text{penalty} = \min_{e \in \mathcal{E}_{\text{known}}} \|a - e\|$ encourages exploration away from known embeddings, and $\mathcal{N}(a)$ is a frequency penalty discouraging repetitive actions.

**Semantic embedding space** (ViT + CLIP dual backbone, Eq. 1):

$$e = f_{\text{ViT+CLIP}}(x^{\text{vision}}, x^{\text{lang}})$$

where $x^{\text{lang}}$ is the environmental variation description (not the task instruction). The adversary operates in this $\mathbb{R}^{512}$ embedding space, enabling generalization to unseen variations. RoboMD is ==policy-agnostic==: it treats the target policy (Fast-WAM or VLA-JEPA) as a black box.

> **Output of Step 3c**: A ranked set of ==failure-inducing environment configurations== $\mathcal{E}_{\text{hard}} = \{e_1, e_2, \ldots\}$ ordered by failure severity.

---

## 4. PROBE + LEARN: PLD Residual Recovery ([[2511.00091|PLD]])

**PLD Probing**: Deploy the base model (Fast-WAM or VLA-JEPA) in the discovered hard scenarios ($\mathcal{D}_{\text{hard}}$ from Step 2, $\mathcal{E}_{\text{hard}}$ from Step 3c). Record failure states.

**Residual Actor** (lightweight correction on top of frozen base, PLD §3.1):

$$\bar{a}_t = \underbrace{a_t^{\text{base}}}_{\text{frozen base model}} + \underbrace{a_t^{\delta}}_{\text{residual specialist}}$$

where $a_t^{\delta} \in [-\xi, \xi]$ is a bounded residual correction ($\xi \in [0,1]$, tuned by scheduler).

**Training the specialist** via off-policy actor-critic RL ([[2511.00091|PLD]] Eq. 2, initialized with Cal-QL):

$$Q^{\bar{\pi}}(s_t, \bar{a}_t) \leftarrow r(s,a) + \gamma \mathbb{E}_{s_{t+1} \sim p(\cdot|s_t, \bar{a}_t)} \left[Q^{\bar{\pi}}_{\text{target}}(s_{t+1}, \bar{a}_{t+1})\right], \quad \bar{a} = a_b + a_\delta$$

The specialist's reward = task success in the hard scenarios. PLD was validated on π0 (==flow matching==) and OpenVLA (autoregressive), confirming compatibility with both base models.

**Hybrid data collection** (base probes, specialist recovers):

$$\tau_{\text{PLD}} = \underbrace{\{(o_1, a_1^{\text{base}}), \ldots, (o_k, a_k^{\text{base}})\}}_{\text{base policy explores (may fail)}} \cup \underbrace{\{(o_{k+1}, \bar{a}_{k+1}), \ldots, (o_T, \bar{a}_T)\}}_{\text{specialist recovers from failure}}$$

> **Output of Step 4**: A dataset of ==recovery trajectories== $\mathcal{D}_{\text{recovery}} = \{\tau_{\text{PLD}}\}$ — successful trajectories that include recovery from failure states. These are the self-generated training data.

---

## 5. DISTILL: LoRA Fine-Tune

Fine-tune the action model on recovery data using LoRA adapters:

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

Only $A, B$ are updated — $W_0$ remains frozen. This constrains updates to a rank-$r$ subspace, preventing catastrophic changes ([[2603.11653|VLA RL CL]]: <2% forgetting on π0).

> **Output of Step 5**: ==Updated action model== with LoRA adapters that encode the recovery behaviors from self-discovered failure states.

---

## 6. DREAM: World Model Imagination (==our design==)

The frozen world model generates additional training data via iterative imagination.

### 6A. Fast-WAM: Video DiT Dreams

Video DiT (frozen) generates future latent frames via ==iterative denoising== (multiple forward passes, not a single function call):

$$\hat{z}_{1:T} = \text{Denoise}(\text{VideoDiT}, z_0, a_{1:H}^{\text{proposed}})$$

### 6B. VLA-JEPA: V-JEPA2 Latent Dreams

V-JEPA2 predictor (frozen) generates future states in ==V-JEPA2 feature space== via a single forward pass (cheaper than Video DiT):

$$\hat{z}_{1:T}^{\text{JEPA}} = \text{VJ2\_Predictor}(z_0^{\text{target}}, z_{a}^{\text{proposed}})$$

Note: V-JEPA2 dreams are latent features, not decodable to pixel observations. They can be used directly to condition the action head via $z_a$ tokens.

### Dream Quality Filter (==our design==)

$$\text{Keep dream if } \text{Var}_{\text{action}}(\hat{z}_{1:T}) < \theta_{\text{dream}}$$

where $\text{Var}_{\text{action}}$ is computed by running the LoRA-updated action model on the dreamed observation and checking action consistency via Flow-SDE (Step 3a). Low variance = the action model agrees with the dream.

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

If standard LIBERO drops more than 2%, increase replay ratio.

---

## Composition Proof: Why the Methods Chain Correctly

The key question: do the outputs of each step correctly feed the inputs of the next? We verify for **both** base models.

| Step | Output | Feeds Into | Fast-WAM Compatibility | VLA-JEPA Compatibility |
|------|--------|-----------|------------------------|------------------------|
| **1. Base** | Action chunks $a_{1:H}$ via FM + future latents via world model | Steps 2, 3a | ODE in Wan2.2 VAE latent space | ODE in V-JEPA2 feature space |
| **2. DETECT** | Hard episodes $\mathcal{D}_{\text{hard}}$ | Steps 3c, 4 | Episode set — any method can use | Same |
| **3a. Flow-SDE** | $\text{Var}_{\text{action}}(o)$ | Steps 4, 6 | SDE has ==same marginal== as ODE ([[2505.05470\|Flow-GRPO]]) | Same — both use FM action heads |
| **3b. SOE VIB** | $\alpha^*(o)$ | Step 4 | VIB is decoder-agnostic (DDPM→FM swap only changes reconstruction loss) | Same — perturbation is in conditioning space, not action space |
| **3c. RoboMD** | $\mathcal{E}_{\text{hard}}$ | Step 4 | ==Policy-agnostic== black-box | Same — treats any policy as black box |
| **4. PLD** | $\mathcal{D}_{\text{recovery}}$ with $\bar{a} = a^{\text{base}} + a^{\delta}$ | Step 5 | Residual ==additive in action space==; PLD tested on π0 (FM) | Same — PLD tested on π0 + OpenVLA |
| **5. DISTILL** | LoRA-updated model: $W' = W_0 + AB$ | Step 1 (next round) | LoRA on ActionDiT non-mixed layers; Video DiT frozen | LoRA on FM action head DiT; V-JEPA2 predictor frozen |
| **6. DREAM** | $\mathcal{D}_{\text{dream}}$ | Step 5 | Frozen Video DiT in Wan2.2 VAE latent space | Frozen V-JEPA2 in feature space (latent-only, no pixel decode) |

### Why the Composition Works

1. **Shared action space**: Both models produce action chunks $a_{1:H} \in \mathbb{R}^{H \times d_a}$ via flow matching. Steps 3a-4 operate in this shared action space regardless of architecture. The observation representation differs (Wan2.2 VAE vs V-JEPA2 features), but all EXPLORE/PROBE mechanisms interface through ==action space==, not observation internals.

2. **Flow-SDE preserves marginal**: Converting ODE → SDE ([[2505.05470|Flow-GRPO]]) preserves $p(a|o,l)$ — the stochastic exploration generates actions from the ==same distribution== as the deterministic model. This holds for any flow matching model (architecture-agnostic).

3. **SOE VIB is decoder-agnostic**: SOE's encoder $p_\theta(z|o)$ and decoder $q_\phi(a|z)$ are MLPs that sit ==between== the observation encoder and the action decoder. Swapping the action decoder from DDPM to FM only changes the reconstruction loss from noise prediction to velocity prediction — the VIB's KL term and latent structure are unaffected. Works with both base models.

4. **PLD residual is additive in action space**: $\bar{a} = a^{\text{base}} + a^{\delta}$ operates in ==action space==, not model internals. The residual correction doesn't depend on how $a^{\text{base}}$ was generated. PLD was tested on π0 (flow matching) and OpenVLA (autoregressive) — confirmed architecture-agnostic ([[2511.00091|PLD]]).

5. **LoRA preserves FM structure**: The update $W' = W_0 + AB$ is a ==rank-r perturbation== of the weight matrix. The flow matching velocity field with perturbed weights still satisfies the FM ODE/SDE structure. For Fast-WAM, LoRA targets ActionDiT non-mixed-attention layers (preserving Video DiT alignment). For VLA-JEPA, LoRA targets the FM action head DiT (V-JEPA2 predictor remains frozen). Both preserve FM validity.

6. **Prediction error and dreams use consistent latent spaces**: Fast-WAM: both $L_{\text{pred}}$ and dreams use Wan2.2 VAE latent space — same encoder $E$, no mismatch. VLA-JEPA: both $L_{\text{pred}}$ and dreams use V-JEPA2 feature space — same target encoder $F(\cdot)$, no mismatch. The two architectures use ==different== latent spaces from each other, but each is ==internally consistent==.

---

## The Full Self-Evolving Loop as One Equation

Combining all steps into one optimization objective per round $n$:

$$\theta^{(n+1)} = \theta^{(n)} + \Delta\theta$$

where $\Delta\theta = AB$ (LoRA update) is trained on:

$$L^{(n)} = \underbrace{\mathbb{E}_{\mathcal{D}_{\text{recovery}}^{(n)}} \left[L_{FM}\right]}_{\text{PLD recovery data}} + \underbrace{\mathbb{E}_{\mathcal{D}_{\text{SOE}}^{(n)}} \left[L_{FM}\right]}_{\text{SOE exploration successes}} + \underbrace{\mathbb{E}_{\mathcal{D}_{\text{dream}}^{(n)}} \left[L_{FM}\right]}_{\text{world model dreams}} + \underbrace{\mathbb{E}_{\mathcal{D}_{\text{replay}}} \left[L_{FM}\right]}_{\text{2\% replay buffer}}$$

where $L_{FM} = L_{FM}^{\text{FW}}$ (Fast-WAM convention: target $\epsilon - y$) or $L_{FM} = L_{FM}^{\text{VJ}}$ (VLA-JEPA convention: target $a - \epsilon$), matching the base model being trained.

The self-generated data comes from three discovery mechanisms:

$$\mathcal{D}_{\text{recovery}}^{(n)} = \text{PLD}\left(\pi_{\theta^{(n)}}, \; \underbrace{\mathcal{D}_{\text{hard}}^{(n)}}_{\text{from prediction error}} \cup \underbrace{\mathcal{E}_{\text{hard}}^{(n)}}_{\text{from RoboMD adversary}}\right)$$

$$\mathcal{D}_{\text{SOE}}^{(n)} = \left\{\tilde{a}_{1:H} : \text{SOE}(\alpha, o) \text{ succeeds} \wedge \alpha > \alpha^*_{\text{prev}}\right\}$$

$$\mathcal{D}_{\text{hard}}^{(n)} = \left\{\tau : S_{\text{env}}(\tau) > \mu_S + 2\sigma_S\right\} \cup \left\{\tau : \text{Var}_{\text{action}}(o) > \theta_{\text{var}}\right\}$$

The last term includes episodes flagged by ==both== Video DiT/V-JEPA2 prediction error (environment-level) and πRL Flow-SDE variance (action-level).

This is a ==fixed-point iteration==: the model generates its own training signal, improves, then generates a new training signal from the improved model. Convergence is measured externally via OOD benchmarks.

---

*Mathematical companion to [[02_How-to-Build-a-Light-Fast-Self-Evolving-WAM|methodology]] and [[03_Research-Roadmap-Self-Evolving-WAM|roadmap]].*
