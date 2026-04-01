---
title: "Mathematical Formulation: Self-Evolving Fast-WAM"
tags:
  - self-evolving
  - WAM
  - Fast-WAM
  - mathematics
  - methodology
aliases:
  - "Self-Evolving WAM Math"
  - "Fast-WAM Formulation"
---

# Mathematical Formulation: Self-Evolving Fast-WAM

> [!abstract] Purpose
> Step-by-step mathematical proof that the combined methods in the self-evolving loop compose correctly. Each step shows: input → formula → output → how it feeds the next step. All formulas are extracted from the cited papers.

---

## 1. Base: Fast-WAM Flow Matching ([[2603.16666|Fast-WAM]])

Fast-WAM generates action chunks $a_{1:H}$ via ==conditional flow matching==. The flow matching objective learns a velocity field $f_\theta$ that transports noise $\epsilon$ to data $y$:

$$L_{FM}(y) = \mathbb{E}_{y, \epsilon, t} \left[ \|f_\theta(y_t, t, o, l) - (\epsilon - y)\|_2^2 \right]$$

where $y_t = (1-t)y + t\epsilon$ is the interpolated sample, $o$ is observation, $l$ is language instruction.

**Two branches trained jointly via MoT:**

$$L_{\text{total}} = L_{\text{act}} + \lambda \cdot L_{\text{vid}}$$

| Branch | What $y$ represents | Output |
|--------|-------------------|--------|
| **ActionDiT** | $y = a_{1:H}$ (action chunk) | $L_{\text{act}} = L_{FM}(a_{1:H})$ |
| **Video DiT** | $y = z_{1:T}$ (future frame latents) | $L_{\text{vid}} = L_{FM}(z_{1:T})$ |

**At inference** (deterministic ODE):

$$\frac{da_\tau}{d\tau} = f_\theta(a_\tau, \tau, o, l), \quad a_0 \sim \mathcal{N}(0, I) \xrightarrow{\text{solve ODE}} a_1 = \text{action chunk}$$

> **Output of Step 1**: A trained ActionDiT that produces action chunks $a_{1:H}$ and a Video DiT that predicts future latent states $\hat{z}_{t+1}$.

---

## 2. DETECT: Video DiT Prediction Error (inspired by [[2602.20057|AdaWorldPolicy]])

Video DiT predicts the next observation in ==latent space== (Wan2.2 VAE encoder $E$):

$$\hat{z}_{t+1} = \text{VideoDiT}(z_t, a_t)$$

Compare with actual next observation encoded by the same VAE:

$$z_{t+1} = E(o_{t+1})$$

**Prediction error (environment-level discovery signal):**

$$L_{\text{pred}}(t) = \|z_{t+1} - \hat{z}_{t+1}\|_2^2$$

**Episode-level surprise score:**

$$S_{\text{env}}(\tau) = \frac{1}{T} \sum_{t=1}^{T} L_{\text{pred}}(t)$$

**Flagging threshold** (rolling statistics):

$$\text{Flag episode if } S_{\text{env}}(\tau) > \mu_S + 2\sigma_S$$

where $\mu_S, \sigma_S$ are rolling mean and standard deviation across recent episodes.

> **Output of Step 2**: A set of ==high-surprise episodes== $\mathcal{D}_{\text{hard}} = \{\tau : S_{\text{env}}(\tau) > \text{threshold}\}$ — environments the world model doesn't understand. These feed into Step 3 (EXPLORE) as the scenarios to probe further.

---

## 3a. EXPLORE (Action Uncertainty): πRL Flow-SDE ([[2510.25889|πRL]], [[2505.05470|Flow-GRPO]])

Convert ActionDiT's deterministic ODE to a ==Stochastic Differential Equation== for diverse action sampling.

**Original ODE** (deterministic — one noise seed → one action):

$$da_\tau = f_\theta(a_\tau, \tau, o, l) \, d\tau$$

**Flow-SDE** (stochastic — same seed → diverse actions):

$$da_\tau = \underbrace{\left[f_\theta(a_\tau, \tau, o, l) + \frac{\sigma_\tau^2}{2\tau}\left(a_\tau + (1-\tau)f_\theta\right)\right]}_{\text{corrected drift}} d\tau + \underbrace{\sigma_\tau \, dw_\tau}_{\text{stochastic noise}}$$

where $\sigma_\tau = \alpha\sqrt{\frac{\tau}{1-\tau}}$ controls the noise level, and $dw_\tau$ is a Wiener process.

**Key property** ([[2505.05470|Flow-GRPO]]): This SDE has the ==same marginal distribution== as the original ODE — it doesn't change what the model can generate, only enables stochastic sampling.

**Action uncertainty signal**: Run $N$ samples from the SDE for the same observation:

$$a_{1:H}^{(1)}, a_{1:H}^{(2)}, \ldots, a_{1:H}^{(N)} \sim \text{Flow-SDE}(o, l)$$

$$\text{Var}_{\text{action}}(o) = \frac{1}{N} \sum_{i=1}^{N} \|a_{1:H}^{(i)} - \bar{a}_{1:H}\|_2^2$$

> **Output of Step 3a**: Per-observation ==action uncertainty== $\text{Var}_{\text{action}}(o)$. High variance = the model is unsure what to do → potential action-level weakness.

---

## 3b. EXPLORE (Action Active Probing): SOE VIB ([[2509.19292|SOE]])

SOE learns a ==compact latent representation== $z$ of task-relevant information via a Variational Information Bottleneck (VIB).

**VIB Encoder** (compress observation to 4-dim latent):

$$z \sim p_\theta(z|o) = \mathcal{N}(\mu_\theta(o), \sigma_\theta^2(o))$$

**VIB Loss** (trade off reconstruction vs compression):

$$L_{\text{VIB}} = \underbrace{-\mathbb{E}_{z \sim p_\theta(z|o)} \left[\log q_\phi(a|z)\right]}_{\text{action reconstruction}} + \underbrace{\beta \cdot \text{KL}\left[p_\theta(z|o) \| \mathcal{N}(0, I)\right]}_{\text{information bottleneck}}$$

**Exploration** (perturb the compressed representation):

$$\tilde{z} = \mu_\theta(o) + \alpha \cdot \sigma_\theta(o) \cdot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

where $\alpha > 1$ amplifies the perturbation beyond the learned variance.

**Decode to action via ActionDiT's flow matching** (adapted for FM — swap decoder):

$$\tilde{a}_{1:H} = \text{ActionDiT}(\tilde{z}, o, l) \quad \text{(conditioned on perturbed } \tilde{z} \text{)}$$

**Behavioral boundary mapping**: For each observation, sweep $\alpha$ from 1.0 to 3.0 and record where task success drops:

$$\alpha^* = \min \{\alpha : \text{success}(\tilde{a}_{1:H}(\alpha)) < 0.5\}$$

Small $\alpha^*$ = fragile behavior (breaks easily). Large $\alpha^*$ = robust behavior.

> **Output of Step 3b**: Per-observation ==behavioral fragility== $\alpha^*(o)$. Low $\alpha^*$ = the model's behavior is fragile here → ==active weakness found==.

---

## 3c. EXPLORE (Environment Active Probing): RoboMD ([[2412.02818|RoboMD]])

RoboMD trains an RL adversary $\pi_{\text{adv}}$ that searches for failure-inducing environment configurations.

**Adversary's MDP**: State = semantic embedding of environment, Action = environment parameter changes, Reward = Fast-WAM's failure rate.

$$\pi_{\text{adv}}^* = \arg\max_{\pi_{\text{adv}}} \mathbb{E}_{\pi_{\text{adv}}} \left[\sum_t r_t\right], \quad r_t = \mathbb{1}[\text{Fast-WAM fails at step } t]$$

**Semantic embedding space** (ViT + CLIP):

$$e = f_{\text{ViT+CLIP}}(o, l)$$

The adversary operates in this embedding space, enabling generalization to unseen environmental variations.

> **Output of Step 3c**: A ranked set of ==failure-inducing environment configurations== $\mathcal{E}_{\text{hard}} = \{e_1, e_2, \ldots\}$ ordered by failure severity.

---

## 4. PROBE + LEARN: PLD Residual Recovery ([[2511.00091|PLD]] + [[2510.25889|πRL]])

**PLD Probing**: Deploy ActionDiT in the discovered hard scenarios ($\mathcal{D}_{\text{hard}}$ from Step 2, $\mathcal{E}_{\text{hard}}$ from Step 3c). Record failure states.

**Residual Actor** (lightweight correction on top of frozen base):

$$\bar{a}_t = \underbrace{a_t^{\text{base}}}_{\text{ActionDiT (frozen)}} + \underbrace{a_t^{\delta}}_{\text{residual specialist}}$$

where $a_t^{\delta} \in [-\xi, \xi]$ is a bounded residual correction.

**Training the specialist** via off-policy RL ([[2510.25889|πRL]] provides the flow-matching-compatible RL mechanism):

$$L_Q = \mathbb{E}_{(s,a,r,s') \sim \mathcal{B}} \left[\left(Q(s,a) - \left(r + \gamma \min_i Q_{\text{target},i}(s', \pi(s'))\right)\right)^2\right]$$

The specialist's reward = task success in the hard scenarios.

**Hybrid data collection** (base probes, specialist recovers):

$$\tau_{\text{PLD}} = \underbrace{\{(o_1, a_1^{\text{base}}), \ldots, (o_k, a_k^{\text{base}})\}}_{\text{base policy explores (may fail)}} \cup \underbrace{\{(o_{k+1}, \bar{a}_{k+1}), \ldots, (o_T, \bar{a}_T)\}}_{\text{specialist recovers from failure}}$$

> **Output of Step 4**: A dataset of ==recovery trajectories== $\mathcal{D}_{\text{recovery}} = \{\tau_{\text{PLD}}\}$ — successful trajectories that include recovery from failure states. These are the self-generated training data.

---

## 5. DISTILL: LoRA Fine-Tune ActionDiT

Fine-tune ActionDiT on recovery data using LoRA adapters:

**LoRA parameterization** (low-rank update to attention weights):

$$W' = W_0 + \Delta W = W_0 + AB$$

where $W_0 \in \mathbb{R}^{d \times d}$ is the frozen pre-trained weight, $A \in \mathbb{R}^{d \times r}$, $B \in \mathbb{R}^{r \times d}$, $r = 32 \ll d = 1024$.

**Training loss** (flow matching on recovery data + replay):

$$L_{\text{distill}} = \underbrace{\mathbb{E}_{(o,a^*) \sim \mathcal{D}_{\text{recovery}}} \left[\|f_\theta(a_t, t, o, l) - (\epsilon - a^*)\|_2^2\right]}_{\text{learn from recovery data}} + \underbrace{\mathbb{E}_{(o,a^*) \sim \mathcal{D}_{\text{replay}}} \left[\|f_\theta(a_t, t, o, l) - (\epsilon - a^*)\|_2^2\right]}_{\text{2\% replay prevents forgetting}}$$

**LoRA update rule:**

$$A, B \leftarrow A, B - \eta \nabla_{A,B} L_{\text{distill}}$$

Only $A, B$ are updated — $W_0$ remains frozen. This constrains updates to a rank-32 subspace, preventing catastrophic changes ([[2603.11653|VLA RL CL]]: <2% forgetting).

> **Output of Step 5**: ==Updated ActionDiT== with LoRA adapters that encode the recovery behaviors from self-discovered failure states.

---

## 6. DREAM: Video DiT Imagination

Video DiT (frozen) generates additional training data:

$$\hat{z}_{1:T} = \text{VideoDiT}(z_0, a_{1:H}^{\text{proposed}})$$

**Dream quality filter** (only keep consistent dreams):

$$\text{Keep dream if } \text{Var}_{\text{action}}(\hat{z}_{1:T}) < \theta_{\text{dream}}$$

where $\text{Var}_{\text{action}}$ is computed by running the LoRA-updated ActionDiT on the dreamed observation and checking action consistency (low variance = ActionDiT agrees with the dream).

> **Output of Step 6**: Additional ==dream trajectories== $\mathcal{D}_{\text{dream}}$ added to recovery data for the next round.

---

## 7. MEASURE: Benchmark Evaluation

After each round, evaluate on held-out OOD benchmarks:

$$\text{Score}_k^{(n)} = \text{SuccessRate}(\text{ActionDiT}^{(n)}, \mathcal{B}_k)$$

where $k \in \{\text{LIBERO-PRO}, \text{LIBERO-X}, \text{LIBERO-Para}, \text{GM-100}\}$ and $n$ is the round number.

**Convergence criterion:**

$$\Delta_k^{(n)} = \text{Score}_k^{(n)} - \text{Score}_k^{(n-1)} > 0 \quad \text{for } \geq 3 \text{ consecutive } n$$

**Regression check:**

$$\text{Score}_{\text{LIBERO}}^{(n)} > 0.98 \times \text{Score}_{\text{LIBERO}}^{(0)}$$

If standard LIBERO drops more than 2%, increase replay ratio.

---

## Composition Proof: Why the Methods Chain Correctly

The key question: do the outputs of each step correctly feed the inputs of the next?

| Step | Output | Feeds Into | Mathematical Compatibility |
|------|--------|-----------|---------------------------|
| **1. Fast-WAM** | Action chunks $a_{1:H}$ via FM ODE + future latents $\hat{z}_{t+1}$ via Video DiT | Step 2 (prediction error), Step 3a (ODE to SDE) | ODE produces $a_{1:H}$; Video DiT produces $\hat{z}_{t+1}$. Both in same latent space (Wan2.2 VAE). |
| **2. DETECT** | Hard episodes $\mathcal{D}_{\text{hard}}$ where $L_{\text{pred}} > \text{threshold}$ | Step 3c (RoboMD probes these), Step 4 (PLD probes these) | $\mathcal{D}_{\text{hard}}$ is a set of episodes — any method can use them as evaluation scenarios. |
| **3a. Flow-SDE** | Per-observation uncertainty $\text{Var}_{\text{action}}(o)$ | Step 4 (flags which observations need recovery), Step 6 (dream quality filter) | $\text{Var}_{\text{action}}$ is computed from same FM model — just multiple ODE → SDE samples. Compatible because SDE has ==same marginal== as ODE ([[2505.05470\|Flow-GRPO]]). |
| **3b. SOE VIB** | Behavioral fragility $\alpha^*(o)$ | Step 4 (identifies fragile behaviors for PLD to recover) | VIB sits ==between== observation encoder and ActionDiT decoder. Decoder is swapped from DDPM to FM, but VIB MLPs are decoder-agnostic. Perturbation is in ==conditioning space==, not action space. |
| **3c. RoboMD** | Hard environment configs $\mathcal{E}_{\text{hard}}$ | Step 4 (PLD probes in these environments) | RoboMD is ==policy-agnostic== black-box — only needs input/output. No mathematical coupling to FM internals. |
| **4. PLD** | Recovery trajectories $\mathcal{D}_{\text{recovery}}$ with $\bar{a} = a^{\text{base}} + a^{\delta}$ | Step 5 (LoRA training data) | Residual $a^{\delta}$ is ==additive in action space==. The combined action $\bar{a}$ is a valid action chunk — same dimensionality as $a_{1:H}$. PLD tested on pi0 (flow matching) — confirmed compatible ([[2511.00091\|PLD]]). |
| **5. DISTILL** | LoRA-updated ActionDiT: $W' = W_0 + AB$ | Step 1 (next round uses updated model) | LoRA update is ==additive to weights==, preserving the FM velocity field structure. The updated model still generates actions via the same ODE/SDE. LoRA on non-mixed-attention layers preserves Video DiT alignment. |
| **6. DREAM** | Filtered dream trajectories $\mathcal{D}_{\text{dream}}$ | Step 5 (additional training data) | Dreams are generated by frozen Video DiT in ==same latent space== (Wan2.2 VAE). Quality filter uses ActionDiT's own consistency — compatible because both operate in same action space. |

### Why the Composition Works

1. **Shared representation space**: All methods operate in Wan2.2 VAE latent space for observations and the same action chunk space $a_{1:H} \in \mathbb{R}^{H \times d_a}$. There is no representation mismatch.

2. **Flow-SDE preserves marginal**: Converting ODE → SDE ([[2505.05470|Flow-GRPO]]) preserves $p(a|o,l)$ — the stochastic exploration generates actions from the ==same distribution== as the deterministic model. This means uncertainty estimates from SDE are valid assessments of the original model's confidence.

3. **SOE VIB is decoder-agnostic**: SOE's encoder $p_\theta(z|o)$ and decoder $q_\phi(a|z)$ are MLPs that sit ==between== the observation encoder and the action decoder. Swapping the action decoder from DDPM to FM only changes the reconstruction loss from noise prediction to velocity prediction — the VIB's KL term and latent structure are unaffected.

4. **PLD residual is additive in action space**: $\bar{a} = a^{\text{base}} + a^{\delta}$ operates in ==action space==, not model internals. The residual correction doesn't depend on how $a^{\text{base}}$ was generated (ODE, SDE, or any other method). This is confirmed by PLD's testing on pi0 (flow matching).

5. **LoRA preserves FM structure**: The update $W' = W_0 + AB$ is a ==rank-r perturbation== of the weight matrix. The flow matching velocity field $f_{\theta'}(a_\tau, \tau, o, l)$ with perturbed weights still satisfies the FM ODE/SDE structure — it's just a slightly different velocity field. The model remains a valid flow matching model after LoRA.

6. **Prediction error and dreams use same VAE**: Video DiT prediction error $L_{\text{pred}} = \|z_{t+1} - \hat{z}_{t+1}\|_2^2$ and dream generation both use the Wan2.2 VAE encoder $E$. There is no encoder mismatch — the comparison is in the ==same latent space==.

---

## The Full Self-Evolving Loop as One Equation

Combining all steps into one optimization objective per round $n$:

$$\theta^{(n+1)} = \theta^{(n)} + \Delta\theta$$

where $\Delta\theta = AB$ (LoRA update) is trained on:

$$L^{(n)} = \underbrace{\mathbb{E}_{\mathcal{D}_{\text{recovery}}^{(n)}} \left[L_{FM}\right]}_{\text{PLD recovery data}} + \underbrace{\mathbb{E}_{\mathcal{D}_{\text{dream}}^{(n)}} \left[L_{FM}\right]}_{\text{Video DiT dreams}} + \underbrace{\mathbb{E}_{\mathcal{D}_{\text{replay}}} \left[L_{FM}\right]}_{\text{2\% replay buffer}}$$

And the data $\mathcal{D}_{\text{recovery}}^{(n)}$ is self-generated via:

$$\mathcal{D}_{\text{recovery}}^{(n)} = \text{PLD}\left(\pi_{\theta^{(n)}}, \; \underbrace{\mathcal{D}_{\text{hard}}^{(n)}}_{\text{from Video DiT prediction error}} \cup \underbrace{\mathcal{E}_{\text{hard}}^{(n)}}_{\text{from RoboMD adversary}}\right)$$

This is a ==fixed-point iteration==: the model generates its own training signal, improves, then generates a new training signal from the improved model. Convergence is measured externally via OOD benchmarks.

---

*Mathematical companion to [[02_How-to-Build-a-Light-Fast-Self-Evolving-WAM|methodology]] and [[03_Research-Roadmap-Self-Evolving-WAM|roadmap]].*
