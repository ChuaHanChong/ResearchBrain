---
title: Architecture guide layout (template for every guide)
tags: [hybrid-system, visualization, guide-template]
---

# Architecture guide layout

Goal: one layout for every architecture guide, so each guide is a decision tool: see the design, check how it got implemented, and record what is still undecided.
This is a new design: the existing pages (`hybrid-system-architecture.html`, `hybrid-system-architecture-v2.html`) stay as they are.

## Page structure

```
+--------------------------------------------------------------------------+
| Eyebrow · Title · "checked on <date>, <commit>" · [Design|Built|Decide]  |
| Legend (one line; changes with the mode)                     [⤢ full]    |
+---------------------------------------------+----------------------------+
|                                             | BOX NAME  [L✓][R≠]  ◇      |
|                                             | Design   one line           |
|          DIAGRAM  (65% width)               | Built    L: …  R: …         |
|                                             |          ▸ pseudocode  f:l  |
|   ✓ ≠ ✕ marks on boxes and arrows           | Gap      n open · [prompt]  |
|   ◆ / ◇ decision pins                       | Decision ◇ question (open)  |
|                                             | Arrows   in … · out …       |
+---------------------------------------------+----------------------------+
| Decision register (full table) ·  [Copy as markdown]                     |
+--------------------------------------------------------------------------+
```

- Picture 65%, panel 35%. The ⤢ button gives the picture the full width and hides the panel.
- Below 1000px wide: the panel drops under the picture; the picture scrolls sideways, never shrinks text below the minimum.

## Modes (header switch)

| Mode | Picture shows | Legend shows |
|---|---|---|
| Design | the design only, no marks | role colours, call colours, icons |
| Built | + `[L✓][R≠]` marks on boxes and key arrows; not-built boxes get a dashed outline | ✓ built as designed · ≠ built differently · ✕ not built · L LIBERO · R RoboDojo |
| Decide | + ◆ decided / ◇ open pins; boxes without a decision fade | ◆ decided · ◇ open |

The panel always shows all sections; the mode only changes the picture.

## Encoding rules

- Fill colour = who owns the box (advisor, VLA, tools and data). Never used for status.
- Outline = built status only (solid = built, dashed = not built). The old "bold border = changed from v3" is dropped; that fact moves to the panel.
- Status marks: two small pills per box, `L` and `R`, each ✓ / ≠ / ✕, at the top-right corner.
- Arrows: the three advisor calls and the main flows carry one mark at the arrow's midpoint (for example ① ✕ = plan call not built).
- Decision pins sit at the top-left corner of the box they belong to.
- Every meaning is carried twice (colour plus a symbol), so it survives greyscale.

## Panel order (on click)

1. **Header:** name, `[L][R]` marks, decision pin.
2. **Design:** one line, what we designed.
3. **Built:** per robot, one line each, then collapsible pseudocode with `file:line` cites.
4. **Gap:** count of open gaps, each with its type (Build / Fix / Verify / Decide) and a copy-prompt button.
5. **Decision:** the card, if this box has one.
6. **Arrows:** in and out, as chips that jump.

## Decision register (full card)

| Column | Content |
|---|---|
| Pin | ◆ decided / ◇ open |
| Decision | the question, 10 words max |
| Box | where it sits on the picture (click jumps) |
| Options | the choices considered |
| Chosen + why | empty while open |
| Evidence | paper section, code cite, or run |
| Status · Date · Owner | |

Export: Copy as markdown (whole table, or only open rows).

## Sizing rules (the picture must be readable)

The picture is drawn on a 1000-unit-wide grid and shown at about 780px (65% of a laptop page), so it renders at about 0.78 scale. All sizes below are in grid units and are chosen so text renders at 11px or more at 65%, and 14px or more at full width.

| Element | Minimum |
|---|---|
| Box title | 17 units |
| Box sub-line | 14 units |
| Arrow label | 14 units |
| Chip (block inside a block) | 26 units tall, text 13.5 units, 8 units padding each side |
| Badge (number, icon) | 24 units diameter |
| Status pill `L✓` | 22 units tall |
| Box | 200 units wide; height grows to fit its chips, never the other way |
| Gap between rows of chips | 8 units |

- Nesting depth is at most two: a container holds boxes, and a box holds chips. Never chips inside chips.
- A box holds at most two rows of chips. More content goes to the panel, not into smaller chips.
- If a label does not fit at the minimum size, shorten the label or move it to the panel; never shrink it.

## Phases

1. **Wireframe:** a static HTML mockup of the layout with the Hybrid System v2 picture redrawn on the 1000-unit grid at the sizes above. No data yet, three modes switch the picture.
2. **Data shape:** one file per guide holding boxes, arrows, status per robot, evidence, gaps and decisions.
3. **Hybrid System v2 guide:** fill the data (status from the code, the 24 gaps re-mapped, the decisions made so far) as a new page.
4. **Template and index:** shared build script and checks (edge check, cite check, no external requests), plus an index page listing every guide with its freshness date.

## Unresolved questions

- File name for the new page (proposal: `hybrid-system-guide.html`).
- Owner column: your initials only, or names per decision?
- Should arrows other than the three calls and the main flows get marks, or stay unmarked?
