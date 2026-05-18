---
name: paper-figure-extract
description: "Download a figure from an arxiv paper via ar5iv, save to data/figures/, and embed a wikilink under the KnowledgeHub note's Method section. Use when the user says 'crop the method diagram', 'extract figure N', 'get the architecture diagram', or shares an arxiv ID and wants a figure pulled out. Also trigger after `alphaxiv-summary-extract` to add method figures to newly-ingested KH notes."
---

# Paper Figure Extract

Download a paper's figure from **ar5iv** (arxiv's HTML5 render) and embed it into the KH note's `## Method` section. ar5iv pre-extracts every figure as a separate captioned PNG — no PDF, no cropping, no rendering.

The script does no automatic picking. You (the agent) read the figure captions and decide which one to download.

## Workflow

```bash
python3 .claude/skills/paper-figure-extract/scripts/extract_figure.py {ID} --list
```

Read the captions in the JSON output and:
1. **Pick the figure**. For the *method/architecture diagram* (the default case), look for captions describing the paper's framework, architecture, pipeline, or overall approach. If the user named a specific figure number, use that.
2. **Write a caption** for the embed, grounded in *that paper's* raw caption. The output should:
   - Drop the `Figure N:` prefix (the wikilink already signals it's a figure).
   - Be descriptive but tight — roughly one sentence, ~100–200 characters.
   - Capture what the diagram actually shows, named entities and all.
   - Be in the paper's own language where the original wording is already concise; paraphrase only when compressing.

```bash
python3 .claude/skills/paper-figure-extract/scripts/extract_figure.py {ID} --fig <N> \
  --caption "<your caption, derived from this paper's raw caption>"
```

The two steps are deliberate — you (the agent) are better at writing a descriptive-but-tight caption than any regex truncation. If you omit `--caption`, the script falls back to the raw ar5iv caption verbatim (usually too long).

## Behavior

`--list` prints every figure on `https://ar5iv.org/abs/{ID}` as JSON, each with `fig` number, `image_url`, and full `caption` text.

`--fig N [--caption "..."]`:
1. Downloads `https://ar5iv.org/html/{ID}/assets/x{N}.png` → `data/figures/{ID}-method.png`.
2. Inserts `![[{ID}-method.png]]` + caption under `## Method` in `_KnowledgeHub_/{ID}.md`. Uses `--caption` verbatim if provided, otherwise the raw ar5iv caption. Idempotent — skips if the wikilink already exists. Silently skips if the note is missing or has no `## Method` heading.

Default paths are `data/figures/` and `_KnowledgeHub_/`; override with `--out` and `--kh` if needed. The filename suffix is always `method`.

## Post-ingestion hook

After `Skill(skill="alphaxiv-summary-extract")` finishes a batch, for each new paper:
1. Run `--list` to get the figure captions.
2. Read the captions and pick the method figure.
3. Run `--fig N` to download + embed.

## Caveat

ar5iv may renumber figures relative to the published PDF — papers with cover-page teaser figures rendered as standalone `<img>` (outside any `<figure>` element) get skipped in ar5iv's numbering. Treat the caption text as the source of truth, not the figure number.

## Failure modes

| Script output | Cause | Fix |
|---|---|---|
| `ERROR: ar5iv has no entry for {ID} (...)` | No LaTeX source on arxiv, or paper too recent for ar5iv to have indexed | Manual screenshot from PDF in Preview → `data/figures/{ID}-method.png` |
| `ERROR: ar5iv page exists but has no <figure> elements` | Rare — paper has only inline `<img>` outside any `<figure>` block | Manual screenshot |
| `ERROR: Figure N not in ar5iv list. Available: [...]` | `--fig N` doesn't match a figure on ar5iv (numbering can differ from the PDF) | Re-check numbering with `--list` and pick from the available list |
