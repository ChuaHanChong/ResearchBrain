---
name: visualize
description: Turn anything into one self-contained HTML file the user opens in a browser, built from a catalogue of proven forms (side-by-side comparisons, annotated diffs, module maps, flowcharts and inline SVG figures, slide decks, interactive explainers, status and incident reports, and throwaway editors that export the user's edits back as pasteable text). Use whenever someone asks to visualize something, says "show me", "make this visual", "make an HTML page", "make an artifact", "build a dashboard", "lay these out side by side", "turn this into a deck", "prototype this", "make me an editor for this", or when the answer you are about to write would be a wall of markdown they would skim rather than read. Also use when a task needs its blindspots surfaced before building, such as fanning out design directions, interviewing the user about an ambiguous request, or quizzing them before a merge. For a five-lens citation-verified research briefing, defer to storm-research. For pulling an existing figure out of a paper, defer to paper-figure-extract. For rebuilding concept-graph data, defer to kh-graph-sync.
argument-hint: "[what to visualize]"
---

# Visualize

Build one `.html` file that opens in a browser with no server, no build step, and no network.
The bet behind this skill is that a reader who can point, click, compare, and export learns more in thirty seconds than they would from a page of prose, so the work goes into choosing the right shape and filling it with real material.

## What this does

Takes whatever the user has (a codebase, a diff, a dataset, a decision, a process, a concept, an ambiguous request) and produces a single visual artifact of the form best suited to what the reader has to do with it.
Works on external subjects and on this vault's own contents alike.
The medium never changes: one self-contained HTML file.

## Step 1: Pick the form

**Read `references/forms.md` before choosing.** It catalogues the forms, says when each one wins, and names a real file in `examples/` to read for each.
Do not skip to building from memory, since the default shape a model reaches for is a title followed by sections of prose, which is the one shape this skill exists to avoid.

Choose on what the reader must *do*, not on the subject matter.
Someone deciding between options needs a comparison; someone inheriting a change needs an annotated diff; someone who has to hand you back structured input needs an editor.
When two forms fit, build the one whose reader does more.

**Read the matching example in `examples/` before writing any markup.** Those twenty files are the reference implementation of the house style, and copying the structure of the closest one is faster and better than inventing a layout.
The unknowns family in Part 2 has its own eleven files in `examples/unknowns/`, named in the catalogue entry for each form.

**Say no when the artifact is not the answer.** If a two-line reply, a table in chat, or a code edit fully serves the request, do that instead and say why.
An unwanted HTML file is worse than no file.

## Step 2: Gather real material

The artifact is only worth building if it is filled with the truth.

1. Read the actual source.
   Real diff text, real function names, real numbers, real file paths.
   Paraphrase in the annotations, never in the artifact's primary content.
   Quote the smallest span that carries the point, typically a few lines with their line numbers, and reference the rest by path.
2. When a number is unknown, show it as unknown.
   An empty state, a labelled gap, or an explicit "not measured" is honest; an invented figure that looks plausible is the single worst failure this skill can produce, because the visual polish makes it convincing.
3. When the material is thin, shrink the artifact rather than padding it.
   Three real rows beat twelve where nine are filler.
4. Label anything illustrative as illustrative, in the artifact itself.

## Step 3: Build it

1. Start from `base.html` in this skill folder.
   It carries the palette, the system font stacks, the reset, and the responsive container, plus commented idiom blocks for clipboard export, deck navigation, and SVG arrowheads.
   Paste in the idioms the form needs and delete the rest along with the header comment.
   Treat it as a floor rather than a kit: the machinery specific to a form (side panels, click-to-reveal detail, multi-color edges, drag handling) lives in the examples, so lift that from the file you read in Step 1.
2. **Self-contained or it does not ship.** No CDN scripts, no webfonts, no remote images, no `fetch`.
   Inline every style and script, and embed images as `data:` URIs.
   The file has to render correctly opened from disk with the network off, which is the condition it will actually be read under.
3. **Density is the point.** Use tables for tabular data, inline SVG for structure, color and position to encode meaning, and progressive disclosure (collapsible sections, tabs, hover detail) so depth is available without crowding the first screen.
   If a section is three paragraphs of prose, ask what shape that information really wants.
4. **Encode meaning twice.** Anything carried by color also carries a label or a shape, so severity survives a grayscale print and a colorblind reader.
5. **Artifacts that capture decisions must export.** When the reader's clicks create state you want back (a ranking, a set of toggles, answers, edits), end with a button that turns it into pasteable text: markdown, JSON, a diff, a config block.
   Export the delta when the delta is what they will act on.
   Use the clipboard idiom from `base.html`, whose textarea fallback matters because `navigator.clipboard` is often unavailable on `file://` URLs.
   Interaction that only reveals what is already on the page (filters, tabs, click-to-expand detail) creates no state and needs no export button, so do not bolt one on.
   Most of the unknowns family sits on the exporting side of that line even when it looks like a read-only report, since collecting the reader's judgement is usually the point there, so check the entry in Part 2 of `forms.md` rather than judging by appearance.
6. Give it a real `<title>`, since that is what the browser tab and any shared link will show.

## Step 4: Check it before handing it over

Run these against the file you just wrote, and fix what they catch.
Then run them again after your last fix, because the edit made after the final check is the one nobody has verified.

1. **No external requests.** Both of these should return nothing: `grep -nE '<(script|link|img|iframe|source|use|object|embed)[^>]*(src|href)=.?https?:' <file>` and `grep -nE '@import|url\(https?:' <file>`.
   They catch fetched resources only.
   An `<a href>` pointing at a real PR, ticket, or paper is fine and often useful, so do not strip those.
2. **No placeholders left.** Search for `REPLACE ME`, `TODO`, `Lorem`, `{{`, and the instructional comments from `base.html`.
3. **Read the rendered result, not just the source.** Open it, or at minimum re-read the body as a reader would, and ask whether the first screen answers the question that prompted it.
4. **Trace every SVG edge against every node.** Markup that parses cleanly still draws wrong, and this is the most common way a hand-authored diagram ships a lie.
   Test each `<path>` endpoint against the bounding box of *every* node, not just the two it is meant to join, because the failure that survives review is an endpoint that stops inside some third box on the way.
   Checking only the intended pair passes an edge that never arrives.
   Write the check as a script over the coordinates rather than reading them, since eyeballing a list of numbers is how this defect gets waved through.
5. **Every interactive control does something.** A slider that moves nothing or a button wired to no handler reads as broken and discredits the rest.
6. **Narrow viewport.** The single `@media` breakpoint in `base.html` should keep it usable at phone width.
   Widen or add breakpoints if the form demands it.

## Output

Write to `docs/visuals/{slug}.html` when the project root has a `docs/` folder, where the project root is the repository root inside a git repository and the working directory otherwise.
Failing that, write `visuals/{slug}.html` at the working directory.
Derive `{slug}` from the subject and the form, such as `auth-refactor-module-map.html` or `sampler-options-comparison.html`.

Tell the user the path, name the form you chose and why in one line, and flag anything you left as an honest gap.
Do not paste the HTML into chat.

## Notes and guardrails

- **The form catalogue is the skill.** `references/forms.md` plus the twenty files in `examples/` are why this beats asking for an HTML file directly.
  Consult them every run, including runs where the form seems obvious.
- **Real material only.** Never invent data to fill a chart, a timeline, or a table.
  Visual confidence is exactly what makes fabricated content dangerous here.
- **Light only, deliberately.** Not one of the 31 examples implements a dark mode, so its absence is the house style rather than an oversight; add `prefers-color-scheme` handling only when someone asks for it.
- **One file.** No sidecar CSS, JS, or image files.
  Portability is the property that makes these artifacts get shared and read.
- **Throwaway is fine.** Many of these are built for one conversation and then discarded.
  That is not a reason to fabricate, but it is a reason not to over-engineer, and a reason to prefer a small sharp artifact over a large general one.
- **Stay inside the palette.** The core of the `:root` block in `base.html` (the ivory surface, the slate ink, clay, oat, olive, and the four grays) is identical across all 31 examples, which is why they look like one hand made them; `--rust` and `--sky` are the rarer accents, so reach for them only when a third and fourth signal colour genuinely earn their place.
- **Attribution.** `examples/` is the Anthropic `html-effectiveness` gallery, MIT licensed.
  `examples/unknowns/` is the companion set, Apache 2.0 licensed.
  Both are vendored with their own `LICENSE` file, so keep the two trees separate.
  All product names, figures, and scenarios in those files are fictional.
  Never lift their sample data into a real artifact.
