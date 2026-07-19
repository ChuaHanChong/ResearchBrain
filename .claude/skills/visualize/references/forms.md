# Form catalogue

Two families of artifact.
Part 1 is the gallery in `examples/`: forms that present work you have already done.
Part 2 is the unknowns set: forms whose job is to surface what nobody has thought of yet.
Every filename in Part 1 is a real file in `examples/`, so read one before building the same shape.

## Choosing

Ask what the reader has to *do* with the artifact.
That answer picks the form faster than the subject matter does.

| The reader has to... | Reach for |
|---|---|
| Pick between options | Side-by-side comparison, Part 1.1 |
| Understand a change someone made | Annotated diff or module map, Part 1.2 |
| React to a look or a feel | Design sheet or live prototype, Part 1.3, 1.4 |
| Follow a structure or a process | SVG figure or flowchart, Part 1.5 |
| Sit through it in a meeting | Deck, Part 1.6 |
| Learn something new | Explainer, Part 1.7 |
| Skim a recurring update | Report, Part 1.8 |
| Give you back structured input | Custom editor, Part 1.9 |
| Discover what is missing | Anything in Part 2 |

When two forms fit, build the one whose reader does more.
A comparison beats a summary, an editor beats a comparison.

The one pairing that tiebreaker does not settle is diagram versus explainer, since both are legitimately "explain how this works".
Ask whether the reader needs the whole shape at a glance or depth on demand.
A two-minute walkthrough, a handoff, or anything the reader has to re-explain to someone else wants the diagram.
A first encounter with an unfamiliar idea wants the explainer.

---

# Part 1: the gallery

## 1.1 Exploration and planning

For when the shape of the work is not settled.
Fan out across directions and lay them next to each other so the reader can point at one, instead of holding three sequential walls of text in their head.

- **Option comparison**: several approaches to the same problem, trade-offs called out inline, in parallel columns rather than sequential sections. `01-exploration-code-approaches.html`
- **Visual directions**: layouts and palettes rendered live so the reader reacts to them rather than imagining them. `02-exploration-visual-designs.html`
- **Implementation plan**: milestones on a timeline, a data-flow diagram, inline mockups, the risky code, a risk table. `16-implementation-plan.html`

Ingredients: equal visual weight per option so the layout does not pre-select a winner, an explicit trade-off row per option, and a recommendation stated as a recommendation.

## 1.2 Code review and understanding

Diffs and call graphs are spatial.
Markdown flattens them.

- **Annotated pull request**: the real diff with margin notes, severity tags, jump links. `03-code-review-pr.html`
- **PR write-up**: the author's side, giving motivation, before and after, a file-by-file tour carrying the *why*, and where to focus review. `17-pr-writeup.html`
- **Module map**: an unfamiliar package as boxes and arrows with the hot path highlighted and a key-files panel alongside. `04-code-understanding.html`

Ingredients: real code text rather than paraphrase, with severity encoded as color plus a label so it survives a grayscale print and a colorblind reader.

## 1.3 Design

HTML is the medium a design system ships in, so it is the natural format for discussing one.
Tokens become swatches, components become contact sheets.

- **Living design system**: colors, type scale, spacing tokens pulled from the repo and rendered as swatches the reader can copy from. `05-design-system.html`
- **Component variants**: several structural treatments of one component on a single sheet, with shared controls that restyle every cell at once. `06-component-variants.html`

Ingredients: render the real component rather than screenshotting it, and put a copyable token value next to every swatch.

## 1.4 Prototyping

Motion and interaction cannot be described, only felt.
Five seconds with the real easing curve beats a paragraph about it.

- **Animation sandbox**: the transition in isolation with named easing presets that swap a CSS custom property, so the reader can feel each option instead of reading its curve. `07-prototype-animation.html`
- **Interaction sandbox**: a single interaction built for real, such as drag-to-reorder, at enough fidelity to judge whether it feels right. `08-prototype-interaction.html`

Ingredients: expose the parameters as controls, choosing named presets when the useful values are few and a slider when the range is continuous, and show the resulting value as text so the tuned setting can be copied back out.

## 1.5 Illustrations and diagrams

Inline SVG gives you a real pen.
Vector art the reader can tweak by hand or paste into a final document.

- **Figure sheet**: the diagrams for a piece of writing, drawn inline so each can be copied out separately. `10-svg-illustrations.html`
- **Annotated flowchart**: a process as a real flowchart, clickable steps revealing what runs, timings, failure paths. `13-flowchart-diagram.html`

Ingredients: an explicit `viewBox` grid, one arrowhead `<marker>` per edge color, edges as `<path>` with stated coordinates, and every node labelled in text rather than in the path data so the diagram stays searchable and editable.
Both files reserve a dashed stroke for the path off the happy route, a failure branch or a retry arc, which reads correctly even before anyone consults the legend.
Lay the nodes out on a coordinate grid you decide once and derive every edge endpoint from it, rather than typing a node's position in one place and its incoming edge's endpoint in another, since the same number written twice is how an edge quietly ends up stopping in the wrong box.

## 1.6 Decks

A handful of `<section>` tags and twenty lines of JS is a slide deck.
No Keynote, no export step.

- **Arrow-key deck**: one file, left and right to navigate. `09-slide-deck.html`

Ingredients: one idea per slide, a live slide counter, and keyboard navigation that also accepts space, all provided by the deck idiom in `base.html`.

## 1.7 Research and learning

An explainer with collapsible sections, tabbed samples, and a glossary in the margin reads very differently from the same words dumped linearly.

- **How a feature works**: TL;DR box, collapsible steps along the request path, tabbed config snippets, FAQ. `14-research-feature-explainer.html`
- **Concept explainer**: the idea taught with a live model the reader can manipulate, a comparison table, a hover-linked glossary. `15-research-concept-explainer.html`

Ingredients: a TL;DR that stands alone, progressive depth so the reader chooses how far to go, and an interactive model wherever the concept has a moving part.

## 1.8 Reports

Recurring documents benefit most from structure and color.
A small chart and a colored timeline turn something people skim into something they read.

- **Status update**: what shipped, what slipped, a small chart, formatted for a Monday morning skim. `11-status-report.html`
- **Incident timeline**: a minute-by-minute narrative timeline, the root cause shown as the actual config diff, and action items carrying owners and due dates. `12-incident-report.html`

Ingredients: the headline judgement at the top, time as a visual axis rather than a list of timestamps, and owners named on every follow-up.

## 1.9 Custom editing interfaces

Sometimes it is hard to describe what you want in a text box.
A throwaway editor for the exact thing at hand, always ending in an export button that turns the reader's work back into text they can paste to you.
They stay in the loop, and the loop gets tighter.

- **Triage board**: drag items across columns, copy the final ordering out. `18-editor-triage-board.html`
- **Toggle editor**: options grouped by area, dependency warnings when a prerequisite is off, copy just the changed keys. `19-editor-feature-flags.html`
- **Prompt tuner**: editable template with highlighted variable slots, sample inputs re-rendering live as the reader types. `20-editor-prompt-tuner.html`

The three files above cover reordering, config editing, and live-preview tuning, but the form stretches further than they show: curating a dataset by approving, rejecting, and tagging rows, annotating a document or transcript or diff and exporting just the annotations, and picking values that are painful to type, such as colours, easing curves, crop regions, cron schedules, and regexes.
Reach for it whenever the reader can point at the right answer faster than they can describe it.

Ingredients: an export button is mandatory rather than optional, exporting the delta when the delta is what the reader will act on, with dependencies validated in the UI and the breakage named.

---

# Part 2: the unknowns family

Different purpose.
These artifacts exist to expose the gap between the plan and the territory.
The map is not the territory, and the gap between them is your unknowns.
The eleven files live in `examples/unknowns/`, so read the matching one before building, exactly as in Part 1.

**The dominant ingredient: the artifact assembles your reply.** Eight of the eleven end by composing text the reader pastes straight back to you: copyable prompt fixes that assemble into one better implementation prompt, steal and skip chips that write the reply, resonate checkboxes that collect a selection, a decisions table that becomes a ready-to-paste implementation prompt, bullets to fold into the next attempt.
That makes the artifact one half of a round trip, and it is the easiest thing to leave out.
The discriminator is what the artifact is for: build the composed output whenever the job is to collect the reader's choices or judgements, and skip it when the job is to teach them a vocabulary, persuade them, or gate them.
The three that compose nothing are the vocabulary ladder, the buy-in doc, and the merge quiz, whose outputs are respectively a reader who can now write a precise prompt, a reviewer who signs off, and a pass or fail.

Two further conventions.
Each page in `examples/unknowns/` shows the exact prompt that produced it at the top, with the artifact below, so the reader can rerun it.
And the honest close matters more here than anywhere else in this catalogue: say plainly what you did not check, since an artifact about unknowns that hides its own gaps refutes itself.
Size it to the findings you actually have, because invented findings bury the real ones.

## 2.1 Before building

The cheapest place to find an unknown is before any code is written.
Ask for a blindspot pass when the territory is unfamiliar, brainstorm and prototype when the reader will only know it when they see it, interview them about the rest, and hand them references when words run out.

- **Blindspot pass**: for someone about to change a system they did not build, report the unknown unknowns as cards, each carrying a copyable prompt fix and all assembling into one better implementation prompt. `01-blindspot-pass.html`
- **Vocabulary ladder**: the cure for "make it nicer", teaching the domain's vocabulary with a live before and after preview so a request that is a feeling becomes a request that is a spec. `02-color-grading-explainer.html`
- **Design directions**: the same thing rendered four wildly different ways, not variations on one idea, with steal and skip chips per element that compose the reader's reply. `03-design-directions.html`
- **Mock before you wire**: a clickable throwaway mock with no backend, toggleable placements, multiple-choice questions, and a self-filling reply template. `04-toolbar-mock.html`
- **Intervention brainstorm**: the solution space grounded in the real codebase and plotted from ship-this-afternoon to quarter-long bet, with checkboxes that assemble the reply. `05-churn-brainstorm.html`
- **The interview**: when the request has more open questions than stated ones, ask them one at a time ordered by architectural blast radius, then hand back a decisions table and a ready-to-paste implementation prompt. `06-interview.html`
- **Reference port**: before porting between languages or frameworks, prove you understood the reference with a semantics map of matched excerpts, gotcha notes, and edge-case tables. `07-reference-port.html`
- **Tweakable plan**: the plan sorted by likelihood of tweaking instead of execution order, with flagged choices offering toggleable alternatives and the mechanical work collapsed at the bottom. `08-implementation-plan.html`

## 2.2 While building

- **Deviation log**: a running log of every place the code forced a departure from the plan, each with the conservative call made at the time, closing with a few bullets to fold into the next attempt. `09-implementation-notes.html`

## 2.3 After building

Shipping means other people inherit your unknowns.

- **Buy-in doc**: leads with a demo of the thing working, then pre-answers every reviewer objection with evidence, and names exactly who signs off on what. `10-pitch-doc.html`
- **Merge quiz**: a merge-readiness report over the real diff that ends in a short quiz the reader has to pass, where a wrong answer points back to the exact section they skimmed. `11-change-quiz.html`
