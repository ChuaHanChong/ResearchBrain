# Topic-File Formatting Reference

Read this when creating or restructuring a General/ topic overview file. Covers paper ordering, callout types, wikilink format, sub-topic groups, ASCII evolution graphs, and anti-patterns.

### Paper Ordering

Within each sub-topic bullet list, sort wikilinks by **arxiv ID descending** (newest first). This surfaces the latest research immediately. The arxiv ID encodes the submission date (YYMM.NNNNN), so descending order = reverse chronological.

### Callout Types & Their Purpose

Each callout type serves a specific role in the topic overview. Using them consistently helps readers quickly find what they need.

| Callout | Syntax | Purpose | Frequency | Content Rules |
|---------|--------|---------|-----------|---------------|
| **Overview** | `> [!abstract] Overview` | Sets the scene for the entire topic — what it covers, why it matters, and how it connects to the rest of the vault | 1 per file (at top) | 2-3 sentences. Explain scope, evolution arc, and key threads. |
| **Key Papers** | `> [!star] Key Papers` | Highlights the 2-3 most impactful papers in a sub-topic — the ones a newcomer should read first | After each sub-topic group | Each entry: `- [[ID\|Name]] — 1-sentence justification`. Focus on impact (paradigm shift, SOTA, foundational) not content summary. |
| **Practical Insight** | `> [!tip] {Title}` | Synthesizes the section's papers into actionable guidance — the "so what?" for a practitioner | 1 per major `##` section (at end) | 2-3 sentences. Bridge from research to practice. Include concrete recommendations, trade-offs, or decision frameworks. |
| **Ideal Recipe** | `> [!success] {Title}` | Documents a proven, validated approach or recipe that emerged from multiple papers | Rare (0-1 per file) | Use `==highlights==` for key components. Only for well-established patterns with empirical backing. |

**When to update callouts:**
- `[!star]`: Update when a new paper is more impactful than an existing starred paper. Signs: it sets a new SOTA, introduces a paradigm shift, or is from a top group and addresses a key limitation of previously starred work.
- `[!tip]`: Update when new papers collectively shift the practical takeaway. If the old tip says "use X" but 3 recent papers show "Y is better", update it.
- `[!success]`: Update when the proven recipe changes (new component, better backbone, validated alternative).

### Wikilink Format

```
[[2602.15922|DreamZero]]
```
- Use the paper's alias from KH frontmatter as display text
- Arxiv ID without version suffix

### Sub-topic Groups

Each sub-topic group follows this pattern:
```
**{Descriptive Name}** — {1-2 sentence explanation of what these papers share}
- [[ID|Paper1]], [[ID|Paper2]], [[ID|Paper3]]
```

Rules:
- Name should be descriptive and specific (not "Other" or "Miscellaneous")
- Description explains the shared theme or approach
- Papers comma-separated on a single bullet line, sorted by ID descending
- When a sub-topic exceeds ~15 papers, split into two more specific sub-topics

### Evolution Graph Diagrams

Plain-text Unicode box diagrams in a fenced `text` block — not mermaid (all 12 `General/` files were converted off it).

````
```text
2. Label-Free Representation   (drop the labels, keep the signal)
· self-distillation
                   +142M curated
                   images               one teacher → many
┌─────────────┐    ┌───────────────┐    ┌─────────────────┐
│ DINO (2021) │───►│ DINOv2 (2023) │───►│ AM-RADIO (2023) │
└──────┬──────┘    └───────────────┘    └─────────────────┘
       │    +test-time domain
       │    adaptation
       │    ┌───────────────┐
       └───►│ VESSA (2025)  │
            └───────────────┘

· reconstruction to latent prediction
                   discrete tokens →    pixel target →       +autoregressive
                   raw pixels           latent target        scaling
┌─────────────┐    ┌───────────────┐    ┌───────────────┐    ┌─────────────┐
│ BEiT (2021) │───►│ MAE (2021)    │───►│ I-JEPA (2023) │───►│ AIM (2024)  │
└─────────────┘    └───────────────┘    └───────────────┘    └─────────────┘

Legend: ╔═╗ double border = landmark/foundational paper.
```
````

Lifted verbatim from `02_Computer-Vision-and-3D.md`, and it exercises every rule below: one mechanism lane holding two threads, a delta on every arrow, one-row and two-row deltas bottom-aligned side by side, `→` kept at the end of row one, and a fork drawn because VESSA adapts at test time rather than continuing the scaling line.

**Lanes and nodes**

- **Lanes are mechanisms, never eras.** Numbered Title-Case header naming the axis the lane divides on, optionally with a parenthetical framing. A year or year-range in the header chops every thread at the boundary, so no lane holds a full lineage. No brackets, ALL-CAPS, `==wrapping==`, or letter-codes.
- **Every lane carries at least one `· thread` label**, lowercase, on its own line. Without it, parallel rows read as one chain someone forgot to connect. Several threads per lane when the mechanisms genuinely diverge, each with its own label and blank line.
- Node text is `Name (Year)`, plain, and must match the table's alias **exactly**: a fenced `text` block renders no wikilinks, so the table is the only route to the note.
- Unicode box-drawing only (`┌─┐│└┘├┬┴╔═╗║╚╝`), never ASCII. Double border marks the one landmark per thread, sparingly. One legend line, inside the fence, no colors or mermaid backstory. A cross-lane arrow may use a bracket hint: `───────► Target (Year)   [Lane Name, below]`.

**Edges**

- **Deltas are required.** An arrow says *came after*; the delta says *what changed*. Put it above the box the arrow **enters**, since it describes what the successor adds. Two grammars only: `+X` adds X, `X → Y` moves an axis. Source it from the paper's own summary, never invent it, and never strip existing deltas during a restyle.
- **Branch on content, not on a template.** Competing replacements for one component branch from a shared parent; independent transplants of one recipe fan out in parallel; a genuine succession stays a chain. Never draw A → B on chronology alone. Two files should not share a topology profile unless their histories really rhyme.
- A survey or reference that descends from nothing belongs in the table with **no** diagram node. Never draw a bare box with no arrow just to give it a home.
- Add a node only when it's genuinely phase-defining. A diagram trailing the body slightly is curation lag, not a defect.

**Width** (budget: 110 characters)

- **Wrap a long delta over two rows rather than widening its box.** Width is otherwise `max(label + 4, delta)`, so one long delta stretches its box and pushes the whole row right for no gain. Two rows is the cap, since a third out-talls the box it labels. Rows bottom-align, so a one-row delta still sits on the box top beside a two-row neighbour.
- Never let `→` start the second row: it belongs to the axis it moves *from*, and a leading bare arrow reads as a new delta (`self-distillation →` / `masked pixels`, never `self-distillation` / `→ masked pixels`).
- Still too wide? Branch an **earlier** node, never the last one: a branch off the final node starts its stem past the entire row and comes out wider than the chain it replaced. Never abbreviate a label to make it fit.

### Evolution Reference Table

After the evolution graph diagram, add a **trend paragraph**, then a **4-column reference table**:

```
The N lanes divide on **what the axis is**. **Lane name** does X, paper to paper to paper.
**Lane name** does Y, and forks where the field forked. ...

| Year | Paper | Track | Contribution |
|------|-------|-------|--------------|
| 2022 | [[2212.06817\|RT-1]] | Action · Tokens to Continuous Flow | Transformer policy on 130K real demos; proved Transformers work for robot control |
| 2024 | [[2410.24164\|π0]] | Action · Tokens to Continuous Flow | Flow matching action expert + VLM for dexterous manipulation |
```

- **Year**: extracted from the diagram node label `Name (Year)`
- **Paper**: wikilink with escaped pipe (`\|`) inside table cells. Escape the pipe **only** inside tables, never in prose.
- **Track**: `Lane · Thread`, matching the diagram's lane header and `· thread` label. This is what lets a reader carry a row back to its place on the map.
- **Contribution**: one complete sentence on what the paper introduced or proved, never cut mid-clause to hit a length target. Source it from the row already in the table, else the paper's `[!star]` justification, else its KnowledgeHub summary — the vault's own prose in every case, never written fresh.
- Rows sorted chronologically (oldest first — this is the one place ascending order is used, because the table tells a story of progression)
- **Every diagram node must have a row.** Extra rows are allowed for papers deliberately kept off the map (see the survey rule above); a node with no row is a broken link layer.

**The trend paragraph must describe the diagram that is actually there.** Name the axis the lanes divide on, walk each lane in order, and say where a fork happens and why. Cite only papers that appear on the map: a paragraph naming papers the diagram dropped is the most common drift after a restyle.

### What NOT to Do

- No "Other" or "Miscellaneous" catch-all groups — every paper belongs somewhere specific
- No truncated summaries with "..." — just wikilinks grouped by method
- No flat paper dumps — every paper goes in a named sub-topic with a description
- No content duplication — summaries live in KnowledgeHub, General/ just groups and contextualizes
- No `[!star]` without explanation — always include em-dash + 1-sentence justification
- No papers sorted randomly — always sort by arxiv ID descending within each sub-topic
- General/ files should be standalone — do not cross-reference deep-dive folders
- No wikilinks inside evolution-graph diagram nodes — use plain text in nodes, put wikilinks in the reference table below
- No mermaid — evolution graphs are plain-text Unicode box diagrams (see Evolution Graph Diagrams above), not `mermaid` code blocks

