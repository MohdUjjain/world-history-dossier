# CSS_DOC.md — Styling System Reference

Source of truth: `styles.css`. This doc describes what's in it so changes can
be made confidently without re-reading the whole file. **Update this doc in
the same turn you change styles.css** — a stale doc is worse than no doc.

---

## 1. Design tokens (`:root`)

**Palette — "Imperial Archive" theme:**
| Token | Hex | Use |
|---|---|---|
| `--ink` | #1B2A44 | primary text, navy surfaces (headers/footers/hero) |
| `--ink-soft` | #3A4A66 | secondary text |
| `--parchment` | #ECE4CE | page background (screen) |
| `--parchment-lt` | #F6F1E4 | card/section tint background |
| `--parchment-dk` | #DCD0AC | borders/dividers on parchment |
| `--paper` | #FBF8F1 | print page background |
| `--gold` / `--gold-lt` | #A9793B / #F1E3C3 | default accent (chapter 0's identity color; fallback everywhere else) |
| `--oxblood` / `--oxblood-lt` | #7E2A31 / #F3DEDD | quote fallback accent; one of the palette pairs |
| `--slate` | #5B6478 | muted labels |
| `--forest` / `--forest-lt` | #3E5C46 / #E3EBE1 | 🟩 Concept box (semantic — do not repurpose) |
| `--ink-lt` | #E4E9F0 | 🟦 Definition box (semantic — do not repurpose) |

**Type:** `--font-display` (Georgia serif, headings/thesis), `--font-body`
(Georgia, prose), `--font-mono` (Courier, page numbers/years/mono labels),
`--font-label` (Trebuchet/system sans, UI chrome/kickers/labels).

**Elevation scale** (added for the "SaaS polish" pass — see chat history):
- Radius: `--r-sm` 8px (buttons/pills/inputs) · `--r-md` 12px (boxes/cards/tables) · `--r-lg` 18px (banners/panels/revision zone)
- Shadow: `--sh-sm`/`--sh-md`/`--sh-lg` — soft layered shadows, not single hard drop-shadows. Applied to `.box`, `.figure-card`, `.table-wrap`, `.banner`, `.revision-flow`, `#navPanel`, `#navTab`, buttons.

**Chapter identity colors** — `paletteFor()` preserves the eight historical identity/contrast pairs, and `applyChapterPalette()` supplies the inline **source** roles `--chapter-primary` (unaltered accent), `--chapter-primary-ink` (accessible parchment text), `--chapter-on-dark` (accessible colored text on navy), `--chapter-contrast` (unaltered revision identity), `--chapter-contrast-ink`, and `--chapter-contrast-surface`. The CSS-owned `--chapter-color` and `--chapter-ink` active roles inherit from the source roles on normal pages, but switch to their contrast counterparts in revision pages. The on-light and on-dark roles target at least 4.5:1 with a cushion, rather than assuming the original hue always works for small text. Body palette remains unchanged. See §5.
`--gold-ink: #7B5320` is the shared accessible archival-gold *text* role; retain `--gold` for decorative accents. `--reader-anchor-clearance` (76px desktop / 68px narrow) offsets the sticky header for screen chapter/section/study-aid anchors without altering print geometry.

---

## 2. Two parallel layout systems

The document renders into **two independent DOM trees**, only one of which
is ever visible at a time:

- `#screenView` — flowing, continuous, comfortable reading. Always in normal
  document flow, no fixed heights. This is what a person actually reads.
- `#printView` — fixed 1280×720px page boxes (`.page`), built on demand only
  when printing. `display:none` on screen; `display:block` under
  `@media print`. Never shown to a person scrolling the page.

**They share one component library** (`.box`, `table.compare`, `.quote`,
`.figure-card`, `.timeline`, `.flow`, `.connector` — §4) but have **separate
font-size scales**: print stays compact (fits a fixed 604px column budget),
screen is deliberately larger/airier (`.main-flow p`, `.main-flow .box`, etc.
override sizes upward — see §3.2). If you resize print text, check
`SAFETY_BUFFER` in engine.js still covers the new sub-pixel drift (see
JS_DOC.md §4).

---

## 3. Screen (flowing) layout

### 3.1 Structural shell
- `.site-header` — sticky, slim: book title + scroll-spy chapter label. NOT
  a control panel (no jump/print here — those live in the nav panel, §3.3).
- `.progress-track` / `.progress-fill` — 3px reading-progress bar under the
  header, driven by scroll position (engine.js `updateProgress()`).
- `.title-page` / `.tp-*` — the one-time cover page at the very top of
  `#screenView`. Non-sticky, scrolls away normally. Mirrored in print as
  `.page.type-title` / `.pt-*` (nearly identical rules, kept separate
  because print is a fixed 1280×720 canvas and screen is `min-height:88vh`).

### 3.2 Per-chapter flow
- `.chapter-flow` — one per chapter; the renderer assigns source palette roles inline (`--chapter-primary` and related tokens), while CSS owns active `--chapter-color` / `--chapter-ink` so revision can override them.
- `.banner` / `.banner .kicker/.thesis/.yrs` — the chapter-opening hero. Auto-height (NOT the fixed-720px print hero). Kicker, thesis border, year-chips all use `var(--chapter-color)`.
- `.chapter-grid` — CSS grid with `minmax(0,1fr) var(--reader-aside-width)` and `gap:var(--reader-column-gap)`; both are screen-only layout tokens. `.section-pair.no-side` spans the full reading width and hides an empty study-aid rail. At widths below 980px the two columns stack.
- `.main-flow` — narrative body prose, headings, tables, timelines, figures, quotes and connectors (NOT concept callouts). Text measure capped at `var(--reader-prose-width)` (42rem) without restricting tables and figures. Paragraph and block spacing uses the central reader rhythm tokens; fixed print body typography is unchanged.
- `.side-flow` — the base rule is sticky, but the active section-aware `.section-pair .side-flow` overrides it to `position:static`; educational notes are paired with their own sections. It holds concept/definition/tip/mistake/memory/high-yield blocks. `data-kind="concept"` authored in the main source is routed into the sidebar by `normalizedStreams()`; see JS_DOC.md §2. Long question banks with `data-kind="list"` remain in the main reading column.
- `.revision-flow` — the end-of-chapter zone. Reassigns `--chapter-color: var(--chapter-contrast)` **and** `--chapter-ink: var(--chapter-contrast-ink)` so both structural accents and readable small-text roles use the revision identity. Tinted background via `color-mix(in srgb, var(--chapter-contrast) 9%, var(--parchment-lt))`. The `.revision-badge` uses `--chapter-contrast-surface` with white text; the printed revision header uses the same surface token.

### 3.3 Sidebar navigation panel (NOT the `.side-flow` content sidebar — this is the site-wide nav/export drawer)
- `#navTab` — small vertical edge tab, fixed right-center. Click opens the panel. This is the *only* screen-visible trigger for navigation/export; deliberately absent from the persistent header.
- `#navOverlay` / `#navPanel` — overlay dims the page; panel slides in from the right (`transform:translateX(100%)` → `0` via `.open`). Rounded left corners (`--r-lg`), layered shadow.
- `.nav-tools` (FIRST) contains search and expansion controls; the collapsed `.nav-export-details` (SECOND) stays **above the chapter TOC**, retaining `#includeRevisionChk`, strict `#rangeInput`, `#rangeHint`, and `#printBtn`. The offline status follows export, then the TOC tree. The new explainer clarifies that revision inclusion also controls screen visibility.
- `.nav-toc-wrap` / `.nav-toc` (SECOND) — enlarged, legible collapsible chapter tree (chapter labels 1rem; section links .94rem, with deeper click/tap targets), `.nav-chapter.expanded` toggles `.nav-sections` visibility. Each chapter row has a small `.dot` colored via inline style from `paletteFor()` (JS), matching that chapter's identity color — same palette as everywhere else, just a low-key nod rather than the full treatment the print TOC gets (§3.4).
- `.nav-section-label` — small caps label ("EXPORT" / "CONTENTS") headlining each zone.

---

### 3.4 Print table of contents (`.toc-row` etc.)
Only generated when a print export spans more than one chapter (engine.js,
`buildPrintView`). Print TOC typography remains legible: `.toc-title` 1.2rem, `.toc-row.chapter` 1.30rem, `.toc-row.section` 1.08rem and page numbers approximately 1rem. The printed TOC now displays chapter rows only; the hierarchical native PDF bookmark outline provides section navigation. This can increase TOC page count; `packRows()` remeasures every row and recomputes page offsets. Real baseline dot-leaders, not a per-row bottom border:
each row is `[num badge?] [official chapter title, wrapping as necessary] [.leader, flex:1,
dotted bottom border] [.pg, page number]` — the leader is what visually
connects title to number, sized by flexbox to fill whatever gap is left.
Chapter rows get `--chapter-color` inline (from `paletteFor()` in
engine.js) driving the circular number badge, the divider rule, and
the colored page number. The old `.toc-row.chapter:first-of-type`
exception was removed: every individually measured row matched that selector,
but only the first printed row on each page did. Keeping all rows styled
identically makes measurements reflect their actual printed height.

**Critical measured-row rule:** `.toc-row.chapter` uses **padding, not a
positive margin** (`margin-top:0; padding-top:9px; padding-bottom:6px`).
`packRows()` measures each row with `heightOf()`, which does not include an
element's own margins. With 33 large chapter rows, old `margin-top:14px`
caused hidden vertical overflow and missing clickable rows in exported PDF
pages. Keep row spacing inside the measured box. The 1.30rem chapter font
retains legibility and allows the complete chapter-only TOC to fit on three
properly paginated pages.

## 4. Shared component library (used by BOTH screen and print)

Six-category color-coded box system — **semantic, do not vary by chapter or
theme.** Same category = same color everywhere, always (this was an explicit
early requirement — "the same type of information should always receive the
same style"):

| Class | Emoji | Color | Meaning |
|---|---|---|---|
| `.def` | 🟦 | `--ink-lt` | Definition |
| `.concept` | 🟩 | `--forest-lt` | Concept (lives in the SIDEBAR; `data-kind="concept"` routes it) |
| `.tip` | 🟨 | `--gold-lt` | Exam tip |
| `.mistake` | 🟥 | `--oxblood-lt` | Common mistake |
| `.memory` | 🟪 | `#EDE3F0` | Memory aid |
| `.hy` | ⭐ | dashed gold | High-yield takeaway |

Base `.box` rule: `border-radius:var(--r-md)`, `box-shadow:var(--sh-sm)`,
padding `16px 19px` (print) / bumped further in `.main-flow`/`.side-flow`
screen overrides. Six variants only set `background`/`border-color`/
`.box-label` color — never radius/shadow/padding (keep those unified).

Other shared pieces:
- `table.compare` + `.table-wrap` — table is a rounded card (the **print/global** wrapper keeps `overflow:hidden`; only `#screenView .table-wrap` can scroll sideways when required). `border-top:4px solid var(--chapter-color)` accent. `border-collapse:separate; border-spacing:0` — **do not change to `collapse`**, it breaks the row-height measurement math in engine.js (see JS_DOC.md §4, "the border-collapse bug"). `table.compare caption` carries `padding:13px 16px 8px` — **this is load-bearing, not decorative.** `.table-wrap` itself has zero padding (so the dark header row can span edge-to-edge, clipped to the rounded corners), which means the caption is the only thing sitting right at the rounded top-left/top-right corners. Without its own padding, caption text gets visibly clipped by the border-radius curve (real bug, reported with screenshots — the fix is the padding, not a smaller radius or removing overflow:hidden).
- `.quote` — now a soft card (`background:var(--parchment-lt)`, rounded right side), not a bare left-border line.
- `.timeline` / `.tl-item` — vertical rail, internal margins fine (never individually paginated/measured — see JS_DOC.md).
- `.flow` — pill-chip process chain.
- `.connector` — small caps divider line, `var(--chapter-color)`.
- `.defgrid-list` — the "Key Definitions — Collected" glossary. **Is a `<ul>`, not a `<dl>`** — changed deliberately so it could reuse the split-list pagination engine once it grew too tall for one page at larger font sizes. If you add a new collected-glossary block, use this same `<ul><li><strong>Term</strong> — def</li></ul>` shape, not `<dl>`.
- `.one-pager` / `.qbank` / `.further-list` — plain `<ul>`/`<ol>` inside a `.box`, spacing via `padding-bottom` on `<li>` (NOT `margin-bottom` — margins aren't captured by the height-measuring code; see JS_DOC.md §4).

---

## 5. Chapter identity color mechanism

Purely a CSS custom-property relay:
1. JS sets `--chapter-color` / `--chapter-contrast` inline on the chapter's
   container (`.chapter-flow` on screen, each `.page` in print).
2. Every rule that wants to be "on-brand" for that chapter reads
   `var(--chapter-color, var(--gold))` — never the raw palette hex.
3. `.revision-flow` (screen) / `.page.is-revision` (print) reassign
   `--chapter-color: var(--chapter-contrast)` at that scope, so the SAME
   downstream rules automatically flip to the contrast hue. No rule exists
   twice for "normal" vs "revision" — this is the whole point of using a
   custom property instead of a second class per element.

If you add a new chapter-branded element, just reference
`var(--chapter-color, var(--gold))` (or `--chapter-contrast` directly if it
should ALWAYS be the contrast hue regardless of scope) — don't hardcode a
color and don't add a manual `.is-revision .my-thing{}` override.

Palette itself (8 hand-picked `{id, contrast}` pairs, cycled by chapter
index) lives in **engine.js**, not here — see JS_DOC.md §2.

---

## 6. Print mechanics

- `@page{ size:13.333in 7.5in; margin:0; }` — true 16:9 (1280×720px at 96dpi). Do not change without also changing `PAGE_W`/`PAGE_H` in engine.js — they must match exactly or the JS pagination math and the physical PDF page will disagree.
- `.page` — absolute-positioned 1280×720 box, `overflow:hidden` (safety net, should never actually clip if engine.js's budget math is right).
- `.page-header-bar` / `.page-footer-bar` — full-bleed navy strips, 46px/30px, deliberately edge-to-edge ("bleeding colors" was an explicit request).
- `@media print` block hides `.site-header`, `#screenView`, `.title-page`, `#navTab`/`#navOverlay`/`#navPanel`, and forces `#printView{display:block}`. `.page{break-after:page}` forces one physical page per `.page` div.

---

## 7. Responsive breakpoints

- `980px` — `.chapter-grid` collapses to `minmax(0,1fr)` (important: avoids 390px-wide mobile horizontal overflow from intrinsic content widths), `.side-flow` loses `position:sticky`; responsive tables can scroll inside their wrappers.
- `640px` — tighter padding, `.tp-title` shrinks, `#navPanel` goes full-width, `.site-header .current` **remains visible** with ellipsis, figures switch to a single column, and headings may wrap.

Print has no responsive breakpoints — it's always exactly 1280×720.

---

## 8. November 2026 relaunch adjustments

- **Preserved theme, changed information layout:** narrative concepts are now sidebar notes, not main-column interruptions. The `.concept` colour itself is unchanged; placement is governed by semantic `data-kind`, not by CSS alone.
- **Index legibility:** on-screen drawer chapter links are 16px / section links ~15px; print index chapter headings ~20.8px at the current base font. The printed index deliberately omits individual section entries; see the native PDF bookmarks for those.
- **Navigation stacking:** `#navOverlay` z-index 108 and `#navPanel` 109 deliberately exceed the sticky `.site-header` z-index 100; previously the header intercepted the close button at the top of the drawer. Keep this ordering.
- **Empty-book screen:** `.empty-state` renders when `chapters/` contains no files; it does not appear in print. Export is disabled with no chapters. This state is intentional while replacement notes are being supplied.
- **Mobile:** forcing the 1-column grid to `minmax(0,1fr)` and scrollable wide tables prevents horizontal overflow without altering the fixed 16:9 PDF.
- **No notes content policy in CSS:** refer to `NEW_NOTES_WORKFLOW.md` for the user-authoritative shorter-notes process.


### 2026-11-02 — compact enlarged print contents without shrinking text

This historical checkpoint explains why the first print TOC had enlarged
chapter and section typography. The **current complete-edition design**
(November 2026) supersedes these old values: printed contents contain **chapters
only**, chapter rows use **1.30rem** with **zero margin** and 9px top/6px
bottom padding; section links remain available in the native PDF outline.
Every row's spacing must be captured in its bounding-box measurement, otherwise
`packRows()` can hide rows at page boundaries. The full 33-chapter edition
has **three print TOC pages**, all chapter rows visible and linked.

### Official chapter-title wrapping (November 2026)

Long textbook headings such as Chapter 00 must not be truncated in the PDF index.
`.toc-row.chapter a` now shares the multi-line wrapping treatment with section
links: `white-space:normal; text-overflow:clip; min-width:0`. Page heights are
remeasured by `packRows()` so index pagination adjusts to the actual lines.
The main chapter heading may wrap naturally on both screen and print heroes.

---

## Sidebar learning components V2 — 2026-11-02

Updated `styles.css` to make the second column a **semantic teaching aid** rather than a glossary. This is a full CSS feature, not just decorative polish. The fixed six semantic colours remain unchanged: `.def` (blue), `.concept` (green), `.tip` (gold), `.mistake` (red), `.memory` (purple), `.hy` (high-yield gold). The newer authoring class names `.definition` and `.highyield` are **invalid**; the new Ch00–03 cards have been normalized to the existing `.def` and `.hy` classes.

Styles added: `.learning-card`, `.learning-title`, `.learning-content`, plus source-derived visual layouts `.mini-compare`, `.mini-stack`, `.mini-profiles`, `.mini-triptych`, `.mini-timeline`, `.mini-chain`, `.mini-flow`, `.mini-steps`, and `.mini-stat`. Every visual is HTML text plus CSS, preserving PDF text selection and browser zoom clarity. `data-display` describes the presentation; `data-kind` and the inner `.box` class determine colour.

Screen `.section-pair` is a separate grid row for each narrative section and its anchored aids, retaining the continuous scroll while ensuring that aid cards appear beside the topic they teach. The sidebar within each row is no longer a chapter-spanning independent sticky stack (`.section-pair .side-flow{position:static}`). At widths under 980px the established one-column mobile layout applies.

Print `.col-side .learning-card` has compact padding, legible type and small internal diagrams that fit 330px. **Critical:** all new mini-diagram vertical spacing uses padding, not margins on individually measured elements; do not add element margins to table caption/rows or split-list items. Preserve the current `border-collapse: separate` math and table caption padding. Cards are measured as the outer `.block` BFC by the JS engine.

Companion authoring contract: `docs/authoring/SIDEBAR_COMPONENTS.md`; regression test: `tests/smoke_sidebar_alignment.py`.

### PDF navigation integrity (November 2026)

A user-visible bug in the first chapter-only export was that 6 of the 33
chapter links were clipped: `heightOf()` excludes element **margins**, so
`packRows()` packed more rows than the paper height actually permitted. The
current `.toc-row.chapter` has no vertical margin, **no positional CSS
exception (`:first-of-type`)**, and retains all its spacing inside padding,
matching measured and actual geometry. QA must check **33
printed chapter entries, 33 clickable page links and zero clipped rows** in
the final PDF, as well as a properly nested 33-chapter/section PDF bookmark
outline. Do not undo the no-margin rule.


## Offline edition controls (November 2026)

The following screen-only CSS lives in `src/styles.css` and is inlined
into the standalone reader by `src/build.py`:

- `.nav-offline`, `.nav-offline button` and associated typography show
  the cached edition state and offer a user-initiated request for persistent
  browser storage. They appear in the Contents drawer after Export.
- `.edition-update-notice`, `.edition-update-message` and
  `.edition-update-actions` create an accessible, dismissible notice when a
  fully cached new edition takes control. Reloading switches the open tab to
  that edition. The banner uses the existing Imperial Archive navy/gold tokens,
  is fixed on screen, and is excluded via `@media print`.
- `.edition-update-notice[hidden]` explicitly overrides the author-level
  display declaration to avoid accidental banner visibility before an update.

Keep the UI outside `#printView` and hidden in printed exports; it must not
affect the 16:9 pagination or individually measured TOC/table/list blocks.
Behavior belongs in `src/offline-reader.js`, not the print engine. The worker
template, revision hashing, optional Google Fonts caching and offline tests
are documented in `src/docs/hosting/PWA.md`.


## Accessible navigation, progress and resume styling (November 2026)

The new **screen-only** styles in `src/styles.css` cover:

- `#navPanel[aria-hidden]`, `.nav-tools`, `#tocSearch`,
  `.nav-tree-controls` and `.nav-export-details`: an inert modal drawer,
  searchable chapter index, expand/collapse controls and a collapsed-by-default
  Print / Export PDF details panel.
- `.nav-chapter-link` and `.nav-chapter-toggle`: **separate** chapter
  navigation and chevron actions with keyboard focus outlines.
  `.nav-chapter.current-chapter`, `.nav-sections a.current-section`
  and `.nav-shortcuts` highlight reading location and link to real
  learning/revision blocks; `[hidden]` selectors ensure filtered/collapsed
  entries never receive focus.
- `.chapter-progress-ring`: circular current-chapter percentage in the
  sticky header, with chapter identity color supplied by the renderer.
  The existing 3px whole-book progress track remains unchanged.
- `.resume-reader-prompt`: a dismissible, responsive, keyboard-accessible
  device-local Continue reading prompt on the cover.
- Mobile `#navPanel`: full viewport width with backdrop and body scroll
  lock while open; the book's underlying dimensions remain unchanged.

**Print safety:** All new UI lives outside `#printView` and is hidden by
the existing drawer/header print rules or explicit `@media print` rules.
No `.page`, `.page-slot`, `.toc-row`, `.block`, chapter color, or
measured margin/padding rules were changed. The screen navigation module
owns behavior and is described in `src/JS_DOC.md`. Recheck the 245-page
bookmarked PDF and paired-sidebar layout before changing print CSS.

---

## Phase A correctness / contrast contract (November 2026)

- **Revision CSS is parse-sensitive.** The explanatory comment immediately before `.page.is-revision` must be valid CSS; a previous stray text fragment made the entire revision-page rule invalid while later header rules still applied. The browser regression checks computed revision backgrounds and header contrast, rather than merely searching for selector strings.
- **Chapter roles must not be collapsed.** Use raw `--chapter-color` for borders and illustrations; `--chapter-ink` for captions, section numbers and other small text on parchment; `--chapter-on-dark` for chapter-branded labels on navy. Revision blocks inherit contrast equivalents and a high-contrast surface for white labels. Do not globally recolor semantic learning cards.
- **Print hero parity.** Chapter-specific thesis borders, timeline dots and structural labels in the fixed 16:9 print hero must derive from the same palette as the flowing banner. The timeline's neutral connecting line can remain neutral.
- **Sticky-header navigation.** `.chapter-flow,.chapter-flow [id]` have `scroll-margin-top:var(--reader-anchor-clearance)`; this affects section/aid targets and direct links on the screen reader, never fixed-size PDF layout.
- **Safe UI gold.** `--gold-ink` is the shared darkened gold used for small UI labels; the export button uses dark brass with white text rather than illegible navy on medium brass.
- **Regression gate.** `src/tests/smoke_phase_a.py` checks actual computed colors, navigation clearance, and print cache idempotency across the eight-pair palette.

**Revision inheritance regression:** Never set `--chapter-color` or `--chapter-ink` as inline styles on a `.page`. Inline styles override `.page.is-revision` rules, silently keeping main-body accents even when the revision header changes color. `--chapter-primary` / `--chapter-primary-ink` are inline inputs; `.chapter-flow,.page` declare the CSS-owned active roles. Printed TOC chapter entries set their own active ink from `paletteFor()`.


---

## Phase B — reader interaction and accessibility polish (November 2026)

The screen-only reader is the sole modal drawer and TOC owner; print geometry is unchanged.

- **Drawer positioning and touch:** The Contents edge tab, modal close button, chapter chevrons, chapter/section links, tree controls, and study shortcut chips have roughly 44px minimum hit areas. The modal's own `.nav-body` scrolls with overscroll containment and bottom safe-area padding; `#navPanel` uses `100dvh` where supported. The backdrop blocks background touches. The `body.drawer-open` scroll lock is set or removed only by the reader UI.
- **Search treatment:** `.nav-search-field` positions the clear control, `.nav-search-match` highlights matched text, `.nav-no-results` explains zero results, and tree-wide expansion controls visibly disable while searching. Filters never mutate manual branch expansion.
- **Accessible movement:** `.skip-to-content` is revealed by keyboard focus and targets `main#screenView`. Focus outlines cover Contents/close/search/print and tree controls; reduced-motion media rules suppress drawer and control transitions. The new no-JavaScript note is hidden during print.
- **Mobile chapter context:** The compact `#currentChapterLabel` now remains visible on screens 640px or narrower, using a shortened available measure rather than disappearing altogether.
- **Reader-only scope:** These rules apply to screen navigation and controls. Do not alter `.page`, `.page-slot`, `.col-main`, `.col-side`, or the fixed 16:9 print measurement rules to tune mobile layout.
- **Tests:** Run `src/tests/smoke_reader_interactions.py` alongside `smoke_reader_ui.py` and `smoke_phase_a.py`. Check touch target sizes, horizontal overflow, mobile header context, modal focus, search outcomes and reading-place preservation.

---

## Phase C — reading space, adaptive tables and publishing access (November 2026)

- **Consolidated screen layout tokens:** `--reader-width`, `--reader-inline-pad`, `--reader-aside-width`, `--reader-column-gap`, `--reader-section-gap`, `--reader-first-section-gap`, `--reader-chapter-gap`, `--reader-prose-width`, and `--reader-rule` live in `:root`. They govern the flowing reader exclusively. The archival color tokens, fixed 1280×720 print canvas, measured `.block` padding, split-table and split-list mechanics are deliberately untouched.
- **Empty-aid sections:** `.section-pair.no-side` uses one grid column, hides its empty aside, and avoids permanently reserving 320px for no educational content. `appendPairedSections()` sets this class based on the authored section's side-node count. Never use a content-dependent `:empty` rule as the only source of truth.
- **True first-section rhythm:** `.chapter-flow>.banner+.section-pair` and `.revision-flow>.revision-badge+.section-pair` apply the larger first-section gap. The former `.section-pair:first-of-type` selector could fail because a preceding `div.banner` shares the same element type. Subsequent sections use the smaller standard gap; stacked mobile aids receive a light rule and internal padding for clarity.
- **Mobile table affordances:** `#screenView .table-wrap` gets horizontal scrolling with touch containment and a visible keyboard focus ring. At 640px and below, authored 3-column and 4-column comparisons receive `min-width:540px` or `680px` respectively; the screen-only engine adds a hint and an ARIA-labeled, keyboard-focusable region **only when the table actually overflows**. No table source or print wrapper styles are modified. Keep table captions' explicit padding: it prevents clipping by rounded corners in PDFs.
  The generated on-screen hint uses the exact `.table-scroll-hint` class; it is absent from print measurement nodes and hidden in physical PDF output.
- **Publication actions:** `.tp-pdf-access` on the screen cover and `.nav-pdf-access` in the Export drawer link to the same relative bookmarked-PDF file. The call-to-action's copy distinguishes a full, prebuilt, native-bookmarked file from browser-generated custom excerpts; the PDF is not part of offline precaching.
- **Cover parity:** the printed cover clones the existing screen cover fields rather than duplicating title/description/imprint strings. The `.pt-*` styles continue sizing those clones for 16:9 print. Print footers consistently say *World History Dossier*.
- **Visual evidence:** the dossier retains existing authored timelines, comparisons and instructional mini-graphics. Consult `src/docs/authoring/HISTORICAL_VISUALIZATIONS.md` before adding any external or generated historical maps/images; no unverified illustrations were inserted in Phase C.
- **Regression:** `python src/tests/smoke_phase_c.py` compares cover/print text, PDF links, empty-rail geometry, table focus and overflow at narrow widths, and PDF footer copy.


## Phase D — visual regression and accessibility release gates (November 2026)

No CSS geometry, colors or text styles are changed in this phase. The new `src/tests/smoke_release_browser.py` captures 1440px, 1024px, 768px, 390px and 320px viewport screenshots (cover, chapter 12, open drawer and wide mobile table) and diffs them against the trusted PR base's compiled `index.html`. The `smoke_release_accessibility.py` script injects pinned axe-core for cover, chapter and modal WCAG A/AA checks, failing on serious/critical results. The PDF inspection script `src/tests/inspect_pdf_release.py` renders representative 16:9 pages and compares their pixels with the committed edition; raw print-col/page dimensions and all-page text bounds are also checked. Output PNGs/JSON are retained as CI artifacts for human visual signoff. See `src/docs/release/RELEASE_VERIFICATION.md` for acceptance criteria and branch-protection limitations.

## Batch 3: Offline edition and contents scope

`src/styles.css` styles `.nav-edition-meta`, `#offlineCheckResult`, and `.nav-search-scope` within the existing navy/parchment Contents drawer. The extra manual update action inherits `.nav-offline button` keyboard-focus and touch target rules; these additions remain screen-only and do not change chapter, PDF, or print geometry.

## 2026-11-06 — Accessible Index / Tools drawer

The original floating **Contents** edge trigger and modal drawer remain screen-only.
The drawer now has two fixed, large **Index** and **Tools** ARIA tabs. Its
`.nav-body` is a non-scrolling flex shell: individual `.nav-view` tabpanels
scroll independently and use `min-height:0` to avoid clipping narrow mobile
viewports. `[hidden]` + `inert` remove the inactive tabpanel from
paint and keyboard focus. Index retains the chapter-colour dots, search,
Expand/Collapse controls, hierarchical links and study shortcuts.

New selectors: `.nav-tablist`, `.nav-view-tab`, `.nav-view`,
`.nav-index-view`, `.nav-tools-view`, `.nav-resume-tool`,
`.nav-reading-options`, `#navToolsResume`. The selected tab is parchment
on navy with a gold inset underline; Imperial Archive colour, 44px targets,
gold focus outlines, safe-area insets and reduced-motion handling remain.
These overrides are inside `@media screen`: **do not move them into the
fixed 16:9 print styles**.
