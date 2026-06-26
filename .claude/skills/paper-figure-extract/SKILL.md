---
name: paper-figure-extract
description: "Extract a paper's pipeline/architecture figure from its alphaxiv overview (or its arxiv HTML render as a fallback) and embed it (the source's own caption verbatim, after visually confirming it is the real diagram) under the KnowledgeHub note's Method section. Use this whenever someone wants a paper's architecture, pipeline, framework, or method figure pulled into its KH note, for example: 'get the architecture diagram for 2606.16542', 'extract the method figure', 'add the pipeline diagram to the note', or just sharing an arxiv ID and asking for its figure."
---

# Paper Figure Extract

Pull a paper's **pipeline / architecture figure** from its **alphaxiv overview page** (`https://www.alphaxiv.org/overview/{ID}`) and embed it under the KH note's `## Method`. The overview is the same source the KH notes are built from, so its figures come with **alphaxiv's own clean caption** and a short **alt-label** that usually flags which figure is the pipeline (e.g. alt `"ADAPT Framework Overview"`).

**Two rules, both mandatory:**
1. **Visually inspect** the candidate before embedding: the alt-label is a hint, not proof. Open the PNG and confirm it is a real pipeline/architecture diagram (boxes, arrows, model components, data flow), not a results plot, a hardware photo, a rollout montage, or a teaser.
2. **Use alphaxiv's caption verbatim** — do not rewrite or paraphrase it.

## Workflow

1. **Scrape the overview** (headless Chromium), which downloads the curated figures plus alphaxiv's captions:
   ```bash
   uv run python .claude/skills/paper-figure-extract/scripts/alphaxiv_figures.py {ID} --list
   ```
   Output is JSON `{id, figures:[{xnum, alt, caption, path}]}`: each curated overview figure with alphaxiv's alt-label, alphaxiv's caption, and a downloaded PNG `path`.

2. **Shortlist by alt-label.** The pipeline figure's alt usually contains *overview / framework / architecture / pipeline / method*. Note the candidate(s).

3. **Visually inspect (required).** Use the **Read tool on each candidate's `path`** to actually view the image, since the alt-label is a hint, not proof. Confirm it is the method diagram (it should match the `## Method` text in `_KnowledgeHub_/{ID}.md`). If several look diagram-like, prefer the overall-framework one.

4. **Embed the confirmed figure** (the script reuses alphaxiv's caption verbatim, so there is no caption to write):
   ```bash
   uv run python .claude/skills/paper-figure-extract/scripts/alphaxiv_figures.py {ID} --embed --xnum <N>
   ```

5. **If no candidate is a true pipeline diagram** (a benchmark/dataset/results-only paper, or the overview curated only result figures), revert so the note stays clean:
   ```bash
   uv run python .claude/skills/paper-figure-extract/scripts/alphaxiv_figures.py {ID} --revert
   ```

**Worked example (ADAPT, `2606.16542`).** `--list` returns four figures: x1 alt *"ADAPT Framework Overview"*, x2 *"Estimation Performance"*, x7 *"Light-footed Locomotion"*, x4 *"Disturbance Resistance"*. The alt-label flags **x1**; viewing `x1.png` confirms a real architecture diagram (an RL controller plus a whole-body disturbance-estimation loop), while the other three are results. So embed it: `--embed --xnum 1`.

## Behavior

- `--list [--refresh]`: loads the overview in headless Chromium, scrolls to lazy-load, downloads each curated `paper-assets` figure to `data/figures/_alphaxiv/{ID}/x{N}.png`, and caches `{ID}.json` (so `--embed` reuses the exact alphaxiv caption). Re-uses the cache unless `--refresh`.
- `--embed --xnum N`: copies the cached `x{N}.png` → `data/figures/{ID}-method.png` and inserts `![[{ID}-method.png]]` + the **verbatim alphaxiv caption** under `## Method` in `_KnowledgeHub_/{ID}.md` (replaces any prior embed; only collapses whitespace).
- `--revert`: removes the embed and the `{ID}-method.png`.

Runs through `uv` (needs `selenium` + a headless Chromium/chromedriver, same as `alphaxiv-summary-extract`).

## Second source: arxiv HTML (fallback when alphaxiv has no figure)

When the alphaxiv `--list` has no usable pipeline figure (it returned nothing, or only results plots / photos), try the paper's **arxiv HTML render** (`https://arxiv.org/html/{ID}`), which often has the architecture figure alphaxiv lacks. Same two rules (visually inspect, caption verbatim) and the same `--list` / `--embed --xnum N` / `--revert` flow, just a different script:

```bash
uv run python .claude/skills/paper-figure-extract/scripts/arxiv_figures.py {ID} --list           # fetch arxiv HTML, download figs, print JSON
uv run python .claude/skills/paper-figure-extract/scripts/arxiv_figures.py {ID} --embed --xnum N  # embed figure N with its arxiv figcaption (verbatim)
uv run python .claude/skills/paper-figure-extract/scripts/arxiv_figures.py {ID} --revert
```

`arxiv_figures.py` reads static HTML (requests + BeautifulSoup, no browser), so it is fast and Selenium-free. The figure number `N` is the paper's own, and **Figure 1 is usually the architecture**. It caches under `data/figures/_arxiv/{ID}/` and embeds to the same `data/figures/{ID}-method.png` (so the two sources are interchangeable). Limits: roughly 80% of papers have an arxiv HTML render; `--list` returns nothing when arxiv shows "No HTML for {ID}" (no render) or the page has no `<figure>` tags, and it silently skips broken images (some LaTeX/drawio figures render as a tiny stub on arxiv).

**TikZ-drawn figures (screenshot workaround).** Some papers draw the architecture in TikZ, so it renders as SVG, not a downloadable PNG, and `--list` then hands back the figure's *embedded* sub-images (e.g. rollout frames) rather than the diagram. Tell-tale: a figure whose caption reads like the pipeline but whose image is a photo or a frame. To capture it, screenshot the rendered `<figure>` element: load `https://arxiv.org/html/{ID}` in headless Chromium (reuse `_driver()` from `alphaxiv_figures.py`), find the architecture figure's `<figure>` (by its id, e.g. `figure[id="S1.F1"]`), hide its `<figcaption>` (`display:none`), and `.screenshot()` it to `data/figures/{ID}-method.png`. Then embed manually: `![[{ID}-method.png]]` + the figcaption text (verbatim) under `## Method`.

## Batch / many papers

Fan out a workflow, one agent per paper: each runs `--list` for its ID, **views the candidate PNGs**, picks the pipeline, and `--embed`s (or `--revert`s). Chunk it (~6 concurrent) to avoid API rate limits and browser contention.

## Notes

- The alphaxiv overview curates a **subset** of the paper's figures (the key ones), so the pipeline figure is almost always present and alt-labelled; results/photo-only papers legitimately have none → `--revert`.
- If the alphaxiv overview returns no usable figure, try the **arxiv HTML** second source above; only if that also has nothing does the diagram need a manual PDF screenshot (`data/papers/`) to `data/figures/{ID}-method.png`.
