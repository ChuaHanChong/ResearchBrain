# Transcript: FlashSAC (2604.04539) hyperparameter lookup

## 1. Tool calls

### Call 1

Tool: `mcp__alphaxiv__answer_pdf_queries`

Parameters (exact JSON passed):

```json
{
  "paper": "2604.04539",
  "queries": [
    "What update-to-data (UTD) ratio does FlashSAC use?",
    "What batch size does FlashSAC use?",
    "What entropy target does FlashSAC use?"
  ]
}
```

Per the alphaxiv-search skill (`## 3. mcp__alphaxiv__answer_pdf_queries`), all three questions about this one paper were batched into a single call rather than issuing three separate calls.

Error: none. Call succeeded and returned XML-formatted page content (`<paper id="2604.04539v2">...</paper>`) covering pages 1, 2, 4, 5, 6, 8, 10, 11, 12, 24, 25, 41.

## 2. Errors

No errors were returned by any tool call.

## 3. Final answer

**Paper:** FlashSAC: Fast and Stable Off-Policy Reinforcement Learning for High-Dimensional Robot Control (arXiv 2604.04539)

**Update-to-data (UTD) ratio:** For the main (GPU-based, massively parallel) setting, the paper states two different values in two places, which appear to be inconsistent with each other:
- Main text (Section 4.1): "The updates-to-data ratio is set to 2/1024, meaning only 2 gradient updates are performed per 1024 new transitions."
- Table 9 (Appendix C, Hyperparameters for GPU-based Simulators): "Update-to-data (UTD) ratio: 2/2048"

I'm reporting both rather than picking one, since this is a discrepancy in the source paper itself, not something I can resolve without the authors' clarification. Other UTD settings given: CPU-based simulators use UTD = 1; vision-based tasks use UTD = 0.5.

**Batch size:** 2048 for the main GPU-based experiments (consistent in both the main text and Table 9). Table 10/11 give different batch sizes for other settings: 512 for CPU-based simulators, 256 for vision-based RL.

**Entropy target:** The target entropy is parameterized via a fixed target action standard deviation σ_tgt, set to **σ_tgt = 0.15** in all experiments (Section 4.3 and confirmed in Table 9's hyperparameter list). An ablation (Figure 10a) shows performance is fairly insensitive to this value across {0.05, 0.1, 0.15, 0.2, 0.25}, with the optimum lying roughly in the 0.15-0.2 range, but 0.15 is the value actually used.
