# Transcript: FlashSAC (arxiv 2604.04539) — UTD ratio, batch size, entropy target

## 1. Tool calls

### Call 1

Tool name: `mcp__alphaxiv__answer_pdf_queries`

Parameters (exact JSON):
```json
{
  "paper": "2604.04539",
  "queries": [
    "What update-to-data (UTD) ratio does FlashSAC use?",
    "What batch size does FlashSAC use for training?",
    "What is the target entropy used in FlashSAC?"
  ]
}
```

Result: succeeded, no error. Returned raw filtered PDF pages (XML, `<paper id="2604.04539v2">...`) covering pages 1, 2, 4, 5, 6, 8, 11, 12, 24, 25, 39, 41 of the paper. Relevant excerpts:

- Page 5 (§4.1 Fast Training, body text): "FlashSAC employs a 2.5M-parameter, 6-layer network for both the actor and critic, paired with a batch size of 2048 that nearly saturates GPU utilization. The updates-to-data ratio is set to 2/1024, meaning only 2 gradient updates are performed per 1024 new transitions."
- Page 6 (§4.3 Exploration, "Unified Entropy Target"): "We instead parameterize the target entropy via a fixed action standard deviation σ_tgt... We set σ_tgt = 0.15 in all experiments."
- Page 12 (§6.4 Exploration Ablation): "the default value (σ_tgt=0.15) performs well without task-specific adjustment", with the optimal range found to be 0.15–0.2 across tasks (Figure 10a ablation over {0.05, 0.1, 0.15, 0.2, 0.25}).
- Page 24 (Appendix C, Table 9 — Hyperparameters, GPU-based Simulators, the "Common" configuration used for IsaacLab/MuJoCo Playground/ManiSkill/Genesis benchmarks):
  - Batch size: 2048
  - Update-to-data (UTD) ratio: 2/2048
  - Entropy target σ_tgt: 0.15
- Page 24 (Table 10 — CPU-based simulators, values that differ from Table 9): Batch size 512, UTD ratio 1.
- Page 25 (Table 11 — Vision-based RL, values that differ from Table 9): Batch size 256, UTD ratio 0.5.

No error was returned by this call.

## 2. Errors

None. The single tool call completed successfully; no other alphaxiv MCP tool calls were made.

## 3. Final answer to the user

For the main GPU-based-simulator setup (IsaacLab, MuJoCo Playground, ManiSkill, Genesis — the paper's primary/default configuration):

- **Batch size: 2048**
- **Update-to-data (UTD) ratio: 2/1024** per the body text (§4.1: "2 gradient updates are performed per 1024 new transitions"), but the paper's own Appendix C hyperparameter table (Table 9) lists it as **2/2048** instead. These two statements are inconsistent within the paper itself — I'm flagging both rather than picking one.
- **Entropy target: σ_tgt = 0.15** (fixed action standard deviation used to parameterize the target entropy via H̄ = ½|A|log(2πe·σ_tgt²); ablation in §6.4 shows the optimum lies in 0.15–0.2 and the paper is not very sensitive to this value).

Note the paper also reports different batch size / UTD settings for other benchmark regimes (not the "main" one):
- CPU-based simulators (MuJoCo, DMC, MyoSuite, HumanoidBench): batch size 512, UTD ratio 1.
- Vision-based RL: batch size 256, UTD ratio 0.5.

The entropy target (σ_tgt = 0.15) is stated as constant across all these configurations.
