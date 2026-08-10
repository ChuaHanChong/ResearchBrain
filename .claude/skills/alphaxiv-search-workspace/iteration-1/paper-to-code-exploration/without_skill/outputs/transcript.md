# Transcript: LoRA training loop / forward-pass code lookup

## 1. Tool calls

### Call 1

Tool: `mcp__alphaxiv__get_paper_content`

Parameters:
```json
{
  "url": "https://arxiv.org/abs/2106.09685"
}
```

Error: none. Returned a structured AI-generated report on the LoRA paper (title, authors, methodology, results). Did not include a direct GitHub URL in the returned text; the official repo URL (`https://github.com/microsoft/LoRA`) was supplied from my own knowledge of the paper, not extracted from this tool's output.

### Call 2

Tool: `mcp__alphaxiv__read_files_from_github_repository`

Parameters:
```json
{
  "githubUrl": "https://github.com/microsoft/LoRA",
  "path": "/"
}
```

Error: none. Returned top-level repo listing and contents of `.gitignore`, `LICENSE.md`, `README.md`, `SECURITY.md`, `setup.py`, plus directory stubs for `examples/` and `loralib/`.

### Call 3

Tool: `mcp__alphaxiv__read_files_from_github_repository`

Parameters:
```json
{
  "githubUrl": "https://github.com/microsoft/LoRA",
  "path": "loralib/layers.py"
}
```

Error: none. Returned the full contents of `loralib/layers.py` (the `LoRALayer`, `Embedding`, `Linear`, `MergedLinear`, `ConvLoRA`/`Conv1d`/`Conv2d`/`Conv3d` classes).

### Call 4

Tool: `mcp__alphaxiv__read_files_from_github_repository`

Parameters:
```json
{
  "githubUrl": "https://github.com/microsoft/LoRA",
  "path": "examples/NLG/src"
}
```

Error (verbatim):
```
Error: result (92,268 characters across 2,547 lines) exceeds maximum allowed tokens. Output has been saved to /Users/chuahanchong/.claude/projects/-Users-chuahanchong-Documents-Projects-ResearchBrain/515b697b-2fc1-45a4-8d35-82e9e49e7555/tool-results/mcp-alphaxiv-read_files_from_github_repository-1786332389403.txt.
Format: Plain text
Use offset and limit parameters to read specific portions of the file, search within it for specific content, and jq to make structured queries.
REQUIREMENTS FOR SUMMARIZATION/ANALYSIS/REVIEW:
- You MUST read the content from the file at /Users/chuahanchong/.claude/projects/-Users-chuahanchong-Documents-Projects-ResearchBrain/515b697b-2fc1-45a4-8d35-82e9e49e7555/tool-results/mcp-alphaxiv-read_files_from_github_repository-1786332389403.txt in sequential chunks until 100% of the content has been read.
- If you receive truncation warnings when reading the file, reduce the chunk size until you have read 100% of the content without truncation.
- Before producing ANY summary or analysis, you MUST explicitly describe what portion of the content you have read. ***If you did not read the entire content, you MUST explicitly state this.***
- If after a few attempts you cannot read the file (file not found, lines too long for Read's offset/limit, no shell access), STOP retrying. Summarize what you were able to read, explicitly state which portion you could not read and why, and proceed.
```
(The `read_files_from_github_repository` tool has no offset/limit parameter, so I did not attempt the suggested chunking on this call; instead I targeted the specific file I actually needed with call 5.)

### Call 5

Tool: `mcp__alphaxiv__read_files_from_github_repository`

Parameters:
```json
{
  "githubUrl": "https://github.com/microsoft/LoRA",
  "path": "examples/NLG/src/gpt2_ft.py"
}
```

Error: none. Returned the full contents of `examples/NLG/src/gpt2_ft.py`, the GPT-2 fine-tuning script containing the actual training loop (`train_validate`).

## 2. Final answer

Repo: [microsoft/LoRA](https://github.com/microsoft/LoRA), official code for "LoRA: Low-Rank Adaptation of Large Language Models" (arXiv:2106.09685).

**How the low-rank update is applied in the forward pass** — `loralib/layers.py`, `Linear.forward`:

```python
def forward(self, x: torch.Tensor):
    def T(w):
        return w.transpose(0, 1) if self.fan_in_fan_out else w
    if self.r > 0 and not self.merged:
        result = F.linear(x, T(self.weight), bias=self.bias)
        result += (self.lora_dropout(x) @ self.lora_A.transpose(0, 1) @ self.lora_B.transpose(0, 1)) * self.scaling
        return result
    else:
        return F.linear(x, T(self.weight), bias=self.bias)
```

This is `h = W0*x + (B*A*x) * (alpha/r)`: the frozen pretrained weight `W0` (`self.weight`, `requires_grad = False`) is applied via the normal `F.linear`, and the low-rank path runs `x` through `lora_A` (`r x in_features`, Kaiming-init) then `lora_B` (`out_features x r`, zero-init) and adds the result scaled by `self.scaling = lora_alpha / r`. Zero-initializing `B` makes `delta_W = B @ A = 0` at the start of training, so training begins from the exact pretrained behavior. `Embedding.forward` and `ConvLoRA.forward` in the same file apply the identical idea to embedding and convolution layers respectively. At eval time (`model.eval()` -> `train(False)`), `B @ A * scaling` is merged directly into `self.weight` so inference has zero extra latency; `model.train()` un-merges it.

**The training loop** — `examples/NLG/src/gpt2_ft.py`, function `train_validate` (called from `__main__`):
- Before training starts: `lora.mark_only_lora_as_trainable(lm_net)` freezes everything except LoRA params when `args.lora_dim > 0`.
- Per batch: forward pass `_lm_logits, _lm_loss = model(_input, lm_labels=_target, lm_mask=_msk, label_smooth=...)`, loss backward + optimizer step via `optimizer_step(...)`, with gradient accumulation (`args.grad_acc`) and optional grad clipping.
- Periodic logging (`log_interval`), checkpointing only the LoRA weights (`torch.save({'model_state_dict': lora.lora_state_dict(model)}, model_path)` at `save_interval`), and periodic validation (`evaluate(...)` at `eval_interval`).
- Outer loop in `__main__` iterates epochs via `itertools.count`, calling `train_validate` each epoch until `max_step`/`max_epoch` is hit.

Both files are unmodified content pulled directly from the tool calls above — nothing here was written from memory of the repo.
