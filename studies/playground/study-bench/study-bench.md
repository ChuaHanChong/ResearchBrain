# Study Bench: shared design system for the three study sites

**Status:** v2.10, 2026-10-01. v2.10: TopicLinks — Summary · ▶ TL;DR · Open topic → on every Overview card, TL;DR section and Explorer topic, one ✓ Understood state; "Go deeper" retired. v2.9, 2026-09-30: v2.9: TL;DR page components (TldrSection, AnimatedGuide, StudyBench.anim/animAll), guide 95; TL;DR pages built on all three sites (2026-09-30; plan: Claude Doc "Study Bench · TL;DR page plan"). v2.8: v2.8: one Lab toolbar on all sites (Tours ▾ · On this bench); the Lab shows words at work, the Glossary page teaches them. v2.7, 2026-09-29: v2.7: every equation self-contained (In words + symbol key), faceted filters, glossary Back / Next walk, Story filmstrip, Compare without a method limit and a comprehensive race. v2.6, 2026-09-28: v2.6: ReturnNav (boxes go to their section; "← Return to …" restores page, tab and place), card links, symbol parts jump to their table row, Guide me never advances by itself. v2.5, 2026-09-27: v2.5: eight pages (Evolution and Compare split with different purposes; Decision guide moves to Compare), a page pager on every page, each site uses only its own book (Symbol concordance and CrossLink removed), fluid text width (no fixed measure). v2.4: v2.4 adds PageShell: one application shell for all three sites (same app bar, page container, page head, sub-tabs, section heads, toolbars, demo-launcher placement, Topic Explorer TOC layout, lab frame and footer), plus `StudyBench.themeToggle` and `StudyBench.demoHint`. v2.3.1: v2.3 fixes the seven pages every site has, adds key-term notes with autolink, demo mode (Watch / Guide me), the visual glossary, chapter summary cards and the PageGuide. v2.2 makes every interaction work with touch and keyboard, adds quiz, drawer and topic-pager patterns, and fixes small-screen layout. v2.1 added word limits and notation rules; v2 added the visual-learning components.
**Design system artifact:** https://claude.ai/artifact/NcEyD4mTnncMHUZNxp88jm (tokens, brand book, 56 components with live previews in light and dark, a TopicPage template, and guide sections for every part of a site).
**Drop-in files in this project:** `claude/study-bench.css` (tokens + components) and `claude/study-bench.js` (`window.StudyBench` helpers).

## Decisions
- **Fresh identity for all three sites.** None of the old looks is kept.
- **One accent for all three:** petrol, `--accent`. Only the book name, its monogram (RL, MA, MR) and the content tell the sites apart.
- **Light and dark are both first-class,** including the lab benches (RL Machine, MARL Lab, Robot Lab), which are no longer dark-only.
- **Type:** Schibsted Grotesk for display, Atkinson Hyperlegible Next for body, Atkinson Hyperlegible Mono for numbers and references. MathJax 3.2.2 tex-svg stays.
- **Shared color meanings across books:** `q-*` quantity roles (RL), `agent-*` / `equilibrium` / `pareto` (MARL), `frame-x/y/z` / `robot-body` / `vec-*` (robotics). All of them are aliases of `data-1..7`.
- **Chart palette:** `data-1`…`data-7` passed the palette validator in this order in both themes. They are for marks only (text stays ink), and charts are drawn on `surface`. `data-8` means Other or baseline.
- **Visual learning first:** every section has a diagram, chart, stepper or live playground; representations are linked (`StudyBench.link`); processes are step-throughs.

## How each site session applies it
1. Read the design system's README (`Artifact read` → `project/README.md`) and the component cards you use.
2. Delete the site's old `:root` token blocks, dark blocks and Google Fonts `<link>`s. Paste `claude/study-bench.css` whole into the page's first `<style>`, and paste `claude/study-bench.js` inline before the site's own scripts. Don't edit either per site. If the system needs a change, change it upstream.
3. Add `class="sb-root"` to `<body>`. Rename the site's variables using the map below, then replace the site's own component CSS with the `sb-` classes wherever one exists.
4. Canvas and SVG drawing: no hex literals. Take colors from `StudyBench.palette()` and redraw inside `StudyBench.onThemeChange(cb)`.
5. Run the acceptance checklist at the end, then republish the artifact and the local copy in `studies/playground/`.

## Token map: Study Bench · Reinforcement Learning (incl. Compare and RL Machine)
| old | new |
|---|---|
| `--bg` | `--paper` |
| `--surface`, `--surface-2`, `--surface-3` | `--surface`, `--surface-sunk`, `--surface-strong` |
| `--ink`, `--ink-2`, `--muted` | `--ink`, `--ink-2`, `--ink-3` |
| `--line`, `--grid`, `--axis` | `--line`, `--bench-grid`, `--line-strong` |
| `--accent`, `--accent-ink`, `--accent-soft`, `--focus` | `--accent`, `--accent-strong`, `--accent-soft`, `--focus` |
| `--good/-soft`, `--bad/-soft`, `--warn` | same names (+ `--warn-soft`) |
| `--s1` … `--s7` / `--s8` | `--data-1` … `--data-7` / `--data-8` (Other) |
| `--div-neg/mid/pos`, `--seq-0/1` | `--div-*`, `--seq-lo/hi` |
| `--wall` | `--ink-2` |
| `--shadow` on panels | none: use a `line` border. Drawers use `--shadow-pop` |
| `--f-display/body/mono`, `--r` | `--font-display/body/mono`, `--radius-md` |
| Explorer diff: new = orange, changed = blue | `\class{sb-new}{…}` / `\class{sb-chg}{…}` (`q-new`, `q-changed`) |
| Machine tokens: reward amber, estimate blue, ρ teal, trace violet, model orange, policy pink | `q-reward`, `q-value`, `q-ratio`, `q-trace`, `q-model`, `q-policy` |

Site-specific changes:
- Replace the filled dark view pill with `.sb-seg` in `.sb-appbar`.
- The `.rlm` scope must follow the theme: remove its forced dark palette.
- The machine's second top bar becomes a `.sb-bench-bar`.
- The Run button becomes `.sb-btn--primary`; Step, Episode, ×50 and Reset stay default buttons.
- Drop Bricolage, IBM Plex, JetBrains Mono, Instrument Sans and STIX Two.

## Token map: Study Bench · Multi-Agent RL (incl. Lab iframe)
| old | new |
|---|---|
| `--bg`, `--surface`, `--surface-2`, `--surface-3` | `--paper`, `--surface`, `--surface-sunk`, `--surface-strong` |
| `--ink`, `--ink-2`, `--ink-3`, `--rule` | `--ink`, `--ink-2`, `--ink-3`, `--line` |
| `--a1` (agent 1) / `--a1` used as UI accent | `--agent-1` / `--accent` |
| `--a2`, `--eq`, `--violet` | `--agent-2`, `--equilibrium`, `--pareto` |
| `--bad/-soft`, `--hl`, `--hl-ink` | same names |
| `--radius`, `--f-*` | `--radius-md`, `--font-*` |

Site-specific changes:
- The two-ring logo becomes the `MA` monogram.
- The Lab's `srcdoc` needs its own copy of study-bench.css and study-bench.js, and it must follow the parent's theme: post the parent's resolved theme into the iframe and set `data-theme` there.
- The Lab's per-action button colors (teal Train, purple Watch) become one `--primary` button (Train) and default buttons for the rest.
- Drop Bricolage and IBM Plex.

## Token map: Study Bench · Modern Robotics (incl. Robot Lab)
| old | new |
|---|---|
| `--bg`, `--surface`, `--surface2`, `--shade` | `--paper`, `--surface`, `--surface-sunk`, `--surface-strong` |
| `--ink`, `--muted`, `--line`, `--grid` | `--ink`, `--ink-2` (body-ish) or `--ink-3` (metadata), `--line`, `--bench-grid` |
| `--accent`, `--accent-soft`, `--on-accent` | UI: `--accent`, `--accent-soft`, `--on-accent`; robot links drawn in orange: `--robot-body` |
| `--vec`, `--vec-soft`, `--third` | `--vec-twist`, `--accent-soft`, `--data-3` |
| `--ax-x`, `--ax-y`, `--ax-z` | `--frame-x`, `--frame-y`, `--frame-z` |
| `--good/-soft`, `--bad/-soft` | same names |
| `--panel2`, `--amber` (Robot Lab scope) | `--surface-sunk`, `--accent` (UI) or `--robot-body` (scene) |
| `--gl-*` (9 glossary categories) | `--data-1` … `--data-8`; fold the ninth into `--data-8` |
| `--display/--disp`, `--body`, `--sans`, `--mono` | `--font-display`, `--font-body`, `--font-mono` |

Site-specific changes:
- The page gets a `.sb-appbar` with views (e.g. Chapters, Robot Lab, Formula sheet). The brand and progress move out of the sidebar, and "0 of 12 understood" sits at the top of the `.sb-toc`.
- Replace the px font sizes (11–15.5px, about 12 distinct values) with the type scale.
- Robot Lab loses Barlow Condensed and uppercase titles and follows the theme.
- Drop Archivo, Source Serif 4, Barlow Condensed, IBM Plex and JetBrains Mono.

## Acceptance checklist (every site)
- [ ] Exactly three font families load (Schibsted Grotesk, Atkinson Hyperlegible Next, Atkinson Hyperlegible Mono), plus MathJax.
- [ ] Apart from the study-bench.css block, the CSS has no hex, rgb or named color. Canvas code reads `StudyBench.palette()`.
- [ ] Light, dark (OS setting) and both explicit `data-theme` values all render correctly, benches included, and canvases redraw when the theme changes.
- [ ] Font sizes come only from the type scale; radii only 3, 6, 10 or round; no shadows on panels.
- [ ] One `.sb-appbar` with a `.sb-seg` view switcher and a monogram. Benches use `.sb-bench` and `.sb-bench-bar`.
- [ ] Book references use `.sb-ref`; anything not from the book has a `.sb-prov`; book deviations use `.sb-callout--differs`.
- [ ] Equation diffs use only `sb-new` / `sb-chg`; bench update tokens use `q-*`.
- [ ] Focus rings are visible everywhere; quiz feedback shows ✓ / ✗ and words; no `NaN`, `undefined` or fake 0.
- [ ] No horizontal page scroll at 400px or at 1280px.

## v2: sections every site must have
The guide sections in the design system give each blueprint. Components in brackets.

| Section | Study Bench · Reinforcement Learning | Study Bench · Multi-Agent RL | Modern Robotics |
|---|---|---|---|
| Topic page order (TopicPage) | restructure to the template | restructure; add outcomes, takeaways | restructure; add takeaways |
| Course map + progress (CourseMap, progress) | add | add | move to the new component |
| Notation page + symbol anatomy (NotationSheet) | convert the drawer | convert the drawer | **add** (has none) |
| Glossary: drawer, map, inline cards (Drawer, GlossaryMap, TermHover) | add the map and inline cards | add the map and inline cards | convert the map; add inline cards |
| Lab (Bench, MethodRack, UpdateEngine, Trajectory, GuidedTour) | convert RL Machine | convert the Lab (iframe follows the theme) | convert Robot Lab |
| Evolution (LineageMap, EquationLineage, StoryMode, MasterTable, SideBySide, race) | convert the Compare page | expand to all five views | **add** for IK, planners and controllers |
| Worked examples and algorithm boxes (WorkedExample, Algorithm) | convert the pseudocode boxes | add | add |
| Workflow diagrams (FlowDiagram) | add the agent–environment loop and GPI | add the learning process (§5.1) | convert "Walk through the loop" |
| Flashcards | add | convert | convert (Robot Lab) |
| Formula sheet | add | add | convert Appendix A |
| Decision guide | add | convert | add (IK / planning) |
| Search, differences-from-book page | add | add | add |
| Symbol concordance column, cross links | fill the RL column | fill the MARL column | fill the MR column |
| States and accessibility | apply | apply | apply |

Additions to the acceptance checklist:
- [ ] Every topic follows the TopicPage order, and every section has a visual.
- [ ] Symbols use shared `data-sym` ids and linked highlighting works in the equation, the diagram, the pseudocode and the notation.
- [ ] Charts use `StudyBench.lineChart` / `grid` (or match their spec): legend, direct labels for up to four series, tooltip, data table.
- [ ] The course map's edges match each topic's Builds on list; progress drives the TOC checks, the map and the meter.
- [ ] The differences-from-book page lists every `.sb-prov` and `.sb-callout--differs` on the site.

## Writing, notation and terminology (v2.1)
The full rules are in the design system's "Writing, notation and terminology" section. In short:
- **Word limits:** hero lede 40 words, topic lede 25, Why this exists 60, outcomes 15 each, captions 35, step text 30, callouts 40, takeaways 25 each, quiz explanation 40, glossary definition 35, prose per topic 900 (200 per section, 80 per paragraph).
- **Notation:** each site uses its own book's notation exactly (RL Sₜ, Rₜ₊₁; MARL sᵗ, rᵗ with agent subscripts; MR θ, 𝒱, T_sb). One form per block: numbered equations are time-indexed, while pseudocode, tables and lab tokens use the pseudocode form (S, R, S′). Keep true values and estimates distinct (v_π vs V). Every symbol is in the Notation sheet with one `data-sym` id.
- **Terminology:** use the book's term (RL "step-size parameter", "discount rate"; MARL "learning rate", "discount factor"). Define each term at first use with a hover card, spell out abbreviations once per topic, avoid jargon the book doesn't use, and keep interface labels in plain words.
- **Spelling:** American, as in all three books.

Additions to the acceptance checklist:
- [ ] All text is within the word limits: `StudyBench.audit()` in the browser console returns an empty list.
- [ ] No equation block mixes the time-indexed and pseudocode forms; every symbol is on the Notation sheet.
- [ ] Every term matches the book's wording; the site's column of the symbol concordance is filled in and checked.
- [ ] Every illustrative (not computed) chart or number is labeled "Illustrative".

## UI/UX rules (v2.2)
- **Touch first:** nothing depends on hover. Tap pins linked highlights and opens term cards, tap selects map nodes, and dragging moves the chart crosshair. On touch screens, controls are 44px tall.
- **Keyboard:** add a skip link. Segmented controls are one Tab stop with arrow keys. Maps use arrow keys, Enter and Escape. Drawers trap focus (`StudyBench.drawer`), and the quiz moves focus to its explanation (`StudyBench.quiz`).
- **Wayfinding:** a Continue button at the top of the TOC, `#` anchors on every section heading, and Previous / Next topic cards at the end of each topic (`TopicPager`). Anchored headings never hide under the sticky app bar.
- **Small screens:** wide diagrams (520px) and tables (560px) keep their minimum width and scroll sideways inside `.sb-scroll-x`; the page itself never scrolls sideways.
- **Feedback:** tables show "Nothing matches" with Clear filters, chart legends hide or show series without recoloring, and steppers end with Replay.

Additions to the acceptance checklist:
- [ ] Every hover interaction also works by tap and by keyboard focus.
- [ ] Tested at 400px on a touch device: no sideways page scroll, all controls at least 44px.
- [ ] Every topic ends with Quiz, Mark as understood and the Previous / Next pager.


## Site structure and guidance (v2.3)
Every site has the same seven pages, labels, ids and order (guide "Site structure: the seven pages"):
Overview `#overview` · Topic Explorer `#explorer` · Evolution & Compare `#evolution` · Interactive Lab `#lab` · Reference `#reference` · Glossary `#glossary` · Notation `#notation`.
Old ids redirect (`#compare`→evolution, `#machine`/`#robot-lab`→lab, `#chapters`→explorer, `#formulas`/`#decide`→reference, `#terms`→glossary).
- Sub-tabs: Evolution & Compare = Lineage · Equation changes · Story · Side by side · Master table. Reference = Formula sheet · Decision guide · Review cards · Differences from the book · Symbol concordance. Glossary = Visual · Map · A–Z.
- Every page opens with an h1, a one-line lede and a PageGuide (`ol.sb-howto`, three steps with working buttons).
- Every interactive section has a `▶ Watch demo` / `Guide me` launcher (`StudyBench.demo`, 4–8 steps, drives the real controls). The first demo on a page shows a dismissible "New here?" hint.
- One TERMS dictionary per site feeds the visual glossary, A–Z, map, Search and `StudyBench.autolink` (pinned notes with a real extra note, "Show me ▶", "Glossary ↗"). `window.SB_SITE = {terms, coverage}`.
- Content on each page comes only from that site's own book.
- The page and sub-tab switchers use the segmented look without the `.sb-seg` class, so labels like "Differences from the book" pass the word-limit audit.
- QA harness: `qa.js` (7-page nav, aliases, visibility, hscroll at 1280/400 in both themes, coverage, audit, axe, every demo run to its last step).

## PageShell rules (v2.4)
- Every page: `main.sb-page[data-page]` → `header.sb-page-head` (eyebrow, 32px `h1.sb-page-title`, lede, 3-step `ol.sb-howto`) → optional `nav.sb-subtabs` → `section.sb-sec` (sec-head: eyebrow?, 22px `h2.sb-sec-title`, lede?, demo launcher?) → `.sb-toolbar` for all controls → body. Overview uses `header.sb-hero` instead of a page head.
- Topic Explorer: `.sb-page--toc` with a sticky TOC (head: meter, Continue, next; foot: Peek notation drawer); one topic visible at a time; topic sections use fixed eyebrow → title pairs (Orientation → Before you start, Key concepts → Terms to know, Methods → Methods in this topic, Takeaways → What to remember, Check yourself → Quiz and flashcards).
- Interactive Lab: bench first (`.sb-bleed`), then `details.sb-demo-list` with a demo card per method.
- Demo launchers only in section heads, demo cards or the bench; hint via `StudyBench.demoHint`. App bar end = Search ⌘K + theme (`StudyBench.themeToggle`, key `sb-theme`). One `footer.sb-footer`.
- Checks (session-local, /home/claude/unify/shell): `check.js` (rules), `compare.py` (geometry vs skeleton), `skeleton.html` (canonical markup).

## v2.5 (2026-09-27)
- **Eight pages:** Overview · Topic Explorer · Evolution · Compare · Interactive Lab · Reference · Glossary · Notation.
  - Evolution (learn the story): Lineage · Story · Equation changes, then a "What changed?" quiz.
  - Compare (choose): Side by side · Master table · Race · Decision guide, then a "Tell them apart" quiz.
  - Links between them: "Compare with parent →" (Evolution) and "See its lineage →" / "Add to side by side" (Compare). Pattern taken from studies/playground/harness-engineering-guide.html (layout only).
  - Reference: Formula sheet · Review cards · Differences from the book.
- **Identical toolbars** on Evolution and Compare (see guide 50 and SPLIT-SPEC §E): Lineage [family] · Compare with parent → · Selected; Story Play ▶ · ← · → · slider · Step n of N; Side by side Add a method · chips · Clear · n of 3; Master table Filter methods · Clear · count + filter row.
- **Page pager** (`nav.sb-pager.sb-page-pager`) at the end of every page.
- **Own book only:** no links to other sites, no cross-book cards, no symbol concordance; other authors named only where the site's own book cites them. The shell checker fails on cross-book links/blocks and lists other-book mentions.
- **Fluid text:** `--prose-w` is 100%; ledes, prose, captions, cards and text containers have no max-width. Only form controls, meters, popovers and SVG diagrams keep one.

## Naming (v2.5.1, 2026-09-28)
- Family pattern **Study Bench · <subject>**: Study Bench · Reinforcement Learning (https://claude.ai/artifact/RDRYggFQyhHZPy65u4Y727, `study-bench-rl.html`), Study Bench · Multi-Agent RL (https://claude.ai/artifact/CkF3Fjej3rY5c9awXXd48Y, `study-bench-marl.html`), Study Bench · Modern Robotics (https://claude.ai/artifact/VeUPgAENA1QCyJgYsScaKr, `study-bench-robotics.html`). The design system artifact is titled Study Bench Design System.
- App bar brand: monogram, then "STUDY BENCH" in small mono caps over the subject. Tab title: "<Page> · Study Bench · <subject>".
- Project notes: claude/study-bench-rl.md, claude/study-bench-rl-machine.md, claude/study-bench-marl.md, claude/study-bench-robotics.md.

## v2.6 (2026-09-28): navigation and guides
- **Every box goes to its section:** course-map boxes → `#explorer/<topic>`; chapter summary cards and concept cards → their link (concept cards get "In the glossary →" when they have none); lineage/story boxes select the method and bring its detail into view; flow nodes naming another chapter → that topic; glossary map boxes → `#glossary/<term>`; symbol-anatomy parts → their row in the symbol table. The landing element flashes (`StudyBench.flash`).
- **Return:** `StudyBench.returnNav()` shows "← Return to <page · tab · section>" (bottom left) after any jump to another page, tab or far-away section; it restores the page, sub-tab and position (anchored to the clicked element). Hidden during demos; ✕ clears it.
- **Guide me waits:** `StudyBench.demo` in guide mode marks a finished task and highlights Next →; it never advances by itself. Tasks may not be already done when their step opens (all three sites audited). Watch mode still plays through on its own.
- Shared wiring snippet appended to every site: /home/claude/unify/nav/wire.html (session-local).

## v2.7 (2026-09-29): self-contained equations, facets, walk-throughs
- **EquationKey:** every displayed equation (Overview summary cards, topic rules, worked examples, algorithm update lines, lineage detail, story steps, formula sheet) has `p.sb-eqwords` ("In words", 25 words; 20 on cards) and `ul.sb-eqkey` (one `li[data-sym]` per symbol, book's term, 6 words). TeX symbols wrapped `\\class{sym-<id>}{…}` with Notation ids; `StudyBench.link` lights equation ↔ key.
- **Faceted filters:** `StudyBench.facetCounts(items, groups)`: every chip shows its count; chips that would give no results disappear; All stays. On formula sheet, review cards, master table, notation kinds, glossary groups, differences.
- **Glossary walk:** visual glossary card has ← Back · n of N · Next → (no Play through, never auto-advances); Map and A–Z give the same when a term is open; A–Z has Walk through.
- **Evolution:** Lineage adds "How to read this map", legend and a richer detail (problem fixed, change from parent, update equation with key, § ref). Story is a picture filmstrip (large current card + clickable thumbnails), not the lineage DAG.
- **Compare:** Side by side takes any number of methods ("n selected", Add all, Clear, sticky row labels, sideways scroll). Race = every runnable method, ≥ 20 seeds, mean + 95% band, sortable results table (final, AUC, steps to threshold, rank), methods note with book setup.

## v2.8 (2026-09-30): Lab tours and "On this bench"
- **Two purposes, split:** Glossary page = learn the words (definitions, pictures, map, A–Z, walk). Lab = see them at work. The Lab has no second glossary (RL glossary drawer, MARL "Glossary · 93 terms" panel and MR definition cards removed).
- **Bench bar, identical on all three:** monogram · name · subtitle · prov … status · **Tours ▾** · **On this bench**.
- **On this bench** (`StudyBench.benchTerms`): only the terms visible now for the current method/world/scene, grouped by bench part, each with what to watch (≤15 words), a live value, Point to it (centres + outlines target) and Definition ↗ (#glossary/<id>). Fixed sheet under the app bar (360px; bottom sheet ≤640px); the bench gets `.has-benchterms` and makes room. Glossary Show in Lab ▶ opens it pointed at the term. MARL draws it in the parent page (lab is an iframe).
- **Tours ▾:** menu under the button, goal-based tours (Look at → Run it ▶ → Notice), Back · n of N · Next, never the site tour. Fixed RL bug: Lab Tours shared id `tourBtn` with the Overview site-tour button and started the site tour; all ids now unique (`labTour…`) and tested.
- **MR:** tours moved from the Explore/Tours/Flashcards switch to Tours ▾ (15 tours); lab flashcards merged into Reference → Review cards; term list shows name + § only.

## v2.9 (2026-09-30): TL;DR page (built)
- Ninth page `#tldr`, second in nav. One scrolling page partitioned into sections; each = AnimatedGuide (looping captioned SVG beats, plays in view, one Pause control, reduced motion = finished picture) + TldrSection text (title 8 words, TL;DR 30, 2–3 points, ≤1 equation with key, Remember, Go deeper →). Not interactive.
- Planned content: RL 16 sections (3 parts + unified-view recap, Fig. 8.11), MARL 15 (foundations / deep MARL + recap), MR 13 (describe / velocities-forces-dynamics / plan-control-contact-mobility + recap). Full table per section (TL;DR, beats, equation, ref) in the plan doc.
- Built: nine-page nav on all sites (Overview · TL;DR · …); `#tldr/<id>` deep links; Overview card + 9th tour stop; search entries; a 4-step TL;DR demo. Parts are `section.sb-sec.sb-tldr-part` (sec-head only) so the 48px rhythm holds; section titles are h3. Shared audit: /home/claude/unify/nav/tldraudit.js (session-local).

## v2.10 (2026-10-01): one topic, three depths
- TopicLinks (`div.sb-topiclinks`): fixed order Summary (`#overview/<topic>`, new deep link that centres + flashes the card) · ▶ TL;DR (`#tldr/<section>`) · Open topic → (`#explorer/<topic>`), leaving out the current place. Overview card: TL;DR · Open topic; TL;DR section: Summary · Open topic (recaps: See the evolution →); Explorer topic head: Summary · TL;DR.
- One ✓ Understood (`.sb-done`) on card, TL;DR section(s), section-list box and topic head. Sections covering two topics show "Open topic: <name> →" per topic; topics covered twice link to the first section.
- v2.9.1: TL;DR section-list boxes equal size (grid-auto-rows: 1fr).
