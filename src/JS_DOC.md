# JS_DOC.md — Engine Architecture Reference

Source of truth: `engine.js`. This doc exists so future changes don't
reintroduce bugs that were already found and fixed once. **Update this doc
in the same turn you change engine.js.** Section 4 ("Gotchas") is the most
important part of this file — read it before touching the measuring or
pagination code.

---

## 1. Big picture

The chapter render and pagination system live in the `engine.js` IIFE; the screen reader state and offline behavior live in independent, inlined `reader-ui.js` and `offline-reader.js` modules. There are two outputs from one chapter source:

```
#chapterData (hidden, pristine, never mutated)
        │
        ├──> renderScreenView()  ──> #screenView   (flowing, always visible)
        │
        └──> buildChapters() ──> ALL_CHAPTERS ──> buildPrintView() ──> #printView
                                                    (fixed 1280×720 pages,
                                                     built on demand, only
                                                     visible under print)
```

`renderScreenView()` runs once on load. `buildPrintView()` runs lazily, the
first time the person exports or prints (button click, or the `beforeprint`
safety net for native Ctrl+P). Both can be called **any number of times, in
any order, forever** — see §4.1, this was not true in an earlier version and
caused real bugs.

---

## 2. Content authoring convention

Each chapter file (`chapters/chNN.html`) is one:
```html
<div class="chapter-source" data-chapter="N" data-title="..." data-author="..." data-subtitle="...">
  <div class="src-hero"> ...hk/ht/hs/hb/hthesis/hyears... </div>
  <div class="src-main"> ...blocks... </div>
  <div class="src-side"> ...blocks... </div>
</div>
```

Every block is `<div class="block" data-keep="..." data-kind="...">`.

**`data-keep`** controls pagination behavior (print only — screen never
paginates):
- `together` (default) — atomic, never split. If it doesn't fit remaining
  page space, deferred whole to the next page.
- `split-table` — table can break across pages, header row + caption
  re-cloned onto continuation pages with "(continued)" appended.
- `split-list` — `<ul>`/`<ol>` can break across pages, "(continued)"
  appended to the box-label on the continuation slice.

**`data-kind`** is presentational/organizational, e.g. `section-head`,
`p`, `h3para`, `h3only`, `concept`, `quote`, `table`, `timeline`, `figures`,
`flow`, `connector`, `def`, `tip`, `mistake`, `memory`, `hy`, `list`.

**UPDATED placement rule:** `concept`/`def`/`tip`/`mistake`/`memory`/`hy` go in `.src-side` (the educational sidebar); prose, section heads, quotes, tables, timelines, figures and connectors go in `.src-main`. A long examination-question list may use a green box visually but must be `data-kind="list"` and remain in the main column. This overrides the old main-column concept rule by explicit user request in November 2026.

`normalizedStreams(chEl)` defensively **clones** both source columns and moves any mistakenly authored `data-kind="concept"` block from the cloned main column to the cloned sidebar, in both screen and print paths. It preserves body/revision separation and never moves a real node from `#chapterData`. Main-column concepts are placed before the sidebar's revision marker; revision concepts after it. A hidden revision divider is created if needed. Because placement into the sidebar is an authoring decision, new chapter files should still put concept blocks directly in `.src-side` at their intended order. The normalizer is a safety net, not a substitute for intentional placement.

**`data-title`** on a `section-head` block is used for the running header
(print) and the nav-panel TOC entry (screen+print) — always set it.

**`data-revision-start="true"`** marks exactly two blocks per chapter: the
"Chapter Summary" `section-head` in `.src-main`, and the "Key Definitions —
Collected" block in `.src-side`. This is how `packChapter()` and
`renderScreenView()` both know where the ordinary chapter content ends and
end-of-chapter revision material begins — see §3.3.

---

## 3. Pagination engine (print only)

### 3.1 Measuring (`extractBlocks`, `heightOf`)
Every block's rendered height is measured once, in an off-screen "rig" div
sized to the real column width, **before** any pagination decisions are made.
Results are cached on the block object (`height`, or for splittable blocks:
`theadH`/`capH`/`rowHsOriginal`/`wrapOverhead` for tables, `nonListH`/
`itemHsOriginal` for lists).

### 3.2 Packing (`fillPages`, `packChapter`)
`fillPages(mainQueue, sideQueue, pages, ch, isRevision, startTitle)` is the
core greedy bin-packer: walks the main queue filling one page at a time
against `PAGE_BUDGET`, handling atomic/split-table/split-list blocks; then
does the same for the side queue independently (main and side don't have to
break at the same point — sidebar just drains at its own rate through the
same run of pages).

`packChapter(ch, pages)`:
1. Pushes the chapter's hero as its own page (always forces a fresh page —
   free side-effect of being a separate `pages.push()` before the loop starts).
2. Splits `ch.main`/`ch.side` into body vs. revision arrays at the
   `data-revision-start` marker.
3. Calls `fillPages()` for body, THEN calls it AGAIN for revision. Two
   separate calls — not one continued loop — is what guarantees revision
   content always starts on a fresh page: the second call's first page is
   always empty when it starts.

### 3.3 Table/list splitting
`sliceTableBlock` / `sliceListBlock` build a new DOM fragment per page by
**moving** (not cloning) rows/items out of the *working copy* arrays
(`blk.rows`/`blk.items`) into the slice. This is safe specifically because
the working copies are throwaway clones — see §4.1.

### 3.4 TOC (`collectTocEntries`, `buildTocRowNodes`, `packRows`)
Two-pass: (1) paginate all content first with *relative* page numbers,
(2) build TOC rows referencing those relative numbers, paginate the TOC
itself to find out how many pages IT needs (`T`), (3) go back and add `T`
(plus 1 for the title page) to every page number, including the ones
already printed into TOC row text. TOC is only generated at all when more
than one chapter is in the current export (a single chapter doesn't need one).

**Chapter-only print index (November 2026).** `collectTocEntries()` still
collects chapter AND section metadata, but `buildTocRowNodes()` intentionally
renders only one row per chapter for the printed contents. A complete edition
therefore has 33 clickable chapter rows, instead of a 17-page section-by-section
index. Do not re-add `ch.sections` to the paper TOC to provide navigation:
the flowing screen's own `renderNavToc()` remains section-aware, and the
full-book PDF exporter now writes native, two-level PDF bookmarks using
print DOM chapter heroes and `data-kind="section-head"` headings. This source
change affects only the index-generation step; body/revision pagination,
chapter colors, section-linked sidebars, duplicate-range exports, PDF page
numbering, and the original screen navigation remain unchanged. The number
of printed pages will decrease because `T` is smaller, and all links are
recomputed from `1+T+rel`.

**PDF bookmarks (exporter, not engine.js).** `src/tools/export_full_pdf.py`
collects each chapter hero and each section heading from the original
`#printView > .page-slot` DOM before it is printed in batches. After merging,
`fitz.Document.set_toc()` creates a chapter-first level-1 / section-level-2
outline. On-page PDF index links and bookmark destinations are separate
navigation systems; both must be verified. Chromium's direct browser
print-to-PDF may not preserve those outline objects, so the pre-rendered
PDF from the batch exporter is the reference bookmarked edition.

---

## 4. Gotchas (read before touching measuring/packing code)

### 4.1 THE big one: measure clones, never the original
Early versions had `heightOf()` and the table/list measuring code do
`rig.appendChild(el); ...; rig.removeChild(el);` directly on the real
content node. This **detaches `el` from `#chapterData` permanently** — a
node can only have one parent, so moving it into the measuring rig and back
out leaves it attached to *nothing*. Since `buildChapters()` only runs
once (cached as `ALL_CHAPTERS`), this meant: the first time anyone printed
anything, `#chapterData` was silently drained. Toggling "include chapter
summaries" afterward called `renderScreenView()` again, which tried to
clone from an now-empty source — the whole screen view vanished and never
came back.

**Fix, and the rule going forward:** every measurement clones first
(`el.cloneNode(true)`), measures the clone, discards it. The real node
(`node: el` on the block object) never moves. At render time
(`renderPage`), every insertion also clones (`n.cloneNode(true)`) before
`appendChild`. Net effect: `#chapterData` is permanently pristine, no matter
how many times you call either render path, in any order, including calling
`buildPrintView()` twice with the same chapter listed twice in one export
(see §4.4).

**If you ever see content "disappearing after the second print/toggle,"
this is the bug class to suspect first.**

### 4.2 Margins aren't captured by `getBoundingClientRect()`
The row/item/caption height-measuring code reads individual sub-elements
directly (`tr.getBoundingClientRect()`, `caption.getBoundingClientRect()`,
`li.getBoundingClientRect()`) rather than going through a flow-root parent.
An element's own **margin** is never included in its own rect. Two real bugs
came from this:
- Table `caption{margin-bottom:5px}` → the 5px silently vanished from the
  fit calculation → tables slightly overflowed. Fixed by using `padding-bottom`
  instead, and additionally by dynamically measuring `wrapOverhead` (the
  gap between the wrapper's total height and cap+thead+rows summed) so ANY
  future spacing change is self-correcting instead of needing a new
  hand-fix each time.
- `.one-pager li` / `.qbank li` used `margin-bottom` → same issue for list
  splitting. Fixed by switching to `padding-bottom`.

**Rule: any element measured individually (not via its flow-root parent)
must use padding, not margin, for its own spacing.** `.block{ display:
flow-root }` protects the generic atomic-block path, but table
rows/captions and list items are measured directly and are NOT protected
by that.

### 4.3 `border-collapse:collapse` breaks row-height math
With `collapse`, adjacent cell borders merge and the shared pixel isn't
cleanly attributable to either row when measured individually — summed row
heights came out a few px short of the table's true rendered height.
Switched to `border-collapse:separate; border-spacing:0`. Don't change this
back without re-deriving the row-fit math.

### 4.4 Shared node references break on deliberate repeats
`ch.heroNode` is built once per chapter and stored on the chapter object.
If the same chapter number is exported twice in one custom range (e.g.
`"1,0,1"`), `packChapter` pushes `{type:'hero', heroNode: ch.heroNode}`
**twice**, both pointing at the same DOM node — the second `appendChild`
silently steals it from the first page, leaving the first occurrence's hero
empty. Fixed by cloning in `renderPage` (`p.heroNode.cloneNode(true)`).
**Any time a chapter can legitimately repeat in the output, check that
every reference to that chapter's shared objects gets cloned at
insertion, not just moved.**

Similarly, `resetWorkingCopies()` must be called **per occurrence**, right
before that occurrence's `packChapter()` call — not once for the whole
batch — or the second occurrence of a repeated chapter sees its
split-table/list rows already drained by the first. See `buildPrintView()`.

### 4.5 Caption padding is load-bearing (CSS, but affects this file's math)
`table.compare caption` needs real padding — see CSS_DOC.md §4 for why
(rounded-corner clipping, not a measurement bug). Worth knowing here too:
because `capH` is measured via `getBoundingClientRect()` (padding included
correctly), and `wrapOverhead` is derived dynamically as "whatever's left
over" (§3.1), a change to the caption's padding requires no code change on
this side — the pagination math adjusts itself. Confirmed by the regression
after fixing it: zero overflow, no `SAFETY_BUFFER` change needed.

### 4.6 `SAFETY_BUFFER`
`PAGE_BUDGET = CONTENT_H - SAFETY_BUFFER`. This exists purely to absorb
residual sub-pixel rendering drift between the measuring rig and the live
page — it is NOT a substitute for fixing a real measurement bug (see 4.2,
4.3 which were real bugs and got real fixes, not just a bigger buffer).
Current value is 44, tuned after increasing the TOC typography and rerouting concepts to the sidebar (a 12px main-column overflow was revealed in regression and eliminated with this conservative 44px buffer). **If you
increase print font sizes again, bump this and re-run the full overflow
regression** (see below) rather than assuming it still holds.

---

## 5. Rendering

- `renderPage(p, absNum)` — builds one `.page` div for print: title / toc /
  hero / content variants. Sets `--chapter-color`/`--chapter-contrast`
  inline via `paletteFor()`. Adds `.is-revision` class when `p.isRevision`.
- `normalizedStreams()` — produces safe, cloned column streams, routing any `data-kind="concept"` from main into sidebar. Used by BOTH outputs before measurement/placement.
- `renderScreenView()` — clears and rebuilds `#screenView` from scratch
  every time it's called (on load, and every time the "include summaries"
  checkbox changes). Splits each chapter's blocks into body vs. revision the
  same way `packChapter` does, but with NO pagination — just two `.chapter-grid`
  blocks in normal flow (revision one wrapped in `.revision-flow`).
- `buildFlowingHero()` (screen) vs `buildHeroNode()` (print) — deliberately
  separate functions, not shared, because the layouts are different enough
  (auto-height flex vs. fixed 720px two-column) that sharing would need more
  conditionals than just having two small functions.

---

## 6. Chapter identity palette

```js
var CHAPTER_PALETTE = [ {id, contrast}, ... 8 pairs ... ];
function paletteFor(chapterNum){ return CHAPTER_PALETTE[chapterNum % 8]; }
```
Cycles automatically — adding chapter 8 wraps back to pair 0, etc. No
per-chapter configuration needed. If you want a SPECIFIC chapter to always
get a specific pair regardless of position, that would need a small lookup
override here — not implemented, hasn't been needed yet.

---

## 7. Export / range parsing

`parseChapterRangeInput(str, allChapters)` — parses free text like
`"5-6,1,3,20-24"` into an **ordered** array of chapter numbers, preserving
exact sequence (including reverse ranges like `"6-5"`) and allowing
deliberate repeats. Empty string = full book in natural order. Unknown
chapter numbers are reported but don't block the rest of the export.

`buildPrintView(chapterNumList)` takes this ordered array directly (not a
from/to pair) — chapters are looked up and packed in exactly the order
given, `resetWorkingCopies` is called per-occurrence (§4.4).

`lastRange` remembers the last list used, so the `beforeprint` listener
(native Ctrl+P) rebuilds the same selection rather than silently defaulting
to something else.

---

## 8. Before shipping a change, re-run this regression

Automated browser smoke checks now exist in `src/tests/smoke_active.py`
(for the current concise-note chapters) and `src/tests/smoke_legacy.py`
(for archived, longer stress fixtures). Run the current smoke test after
rebuilding, in addition to PDF visual review. At minimum, after touching
anything in §3 or §4, re-verify by hand:
1. Load the page, no console errors.
2. Export the full book → zero pages with `lastElementChild.bottom > column.bottom` in `.col-main`/`.col-side`/`.col-full`.
3. Toggle "include chapter summaries" off then on → screen view still has content (§4.1).
4. Export a custom range with a repeated chapter (e.g. `"1,0,1"`) → correct number of distinct heroes, no missing split-table/list content (§4.4).
5. A table/list big enough to split still shows correct row/item counts summing to the original total, with "(continued)" on the second slice.

---

## 9. November 2026 notes-replacement milestone

- **Active chapter directory starts empty.** Old `ch00.html` and `ch01.html` are in `archive/legacy-chapters/`, which `build.py` intentionally ignores. `build.py` supports an empty `chapters/` directory. The assembled book displays an empty-state card and the PDF export button is disabled. No source material was deleted.
- **User-provided short notes take priority** over the previous long NotebookLM-derived notes. Do not silently expand, shorten, fact-check, or rewrite the pasted notes. See `NEW_NOTES_WORKFLOW.md`.
- **No-change assumption:** print page geometry remains exactly 1280×720 with the existing title, running headers/footers, chapter identity accents, revision contrast and custom multi-range ordering.
- **Smoke test:** an isolated temporary build incorporating the archived chapters produced 40 pages, 3 TOC pages, 7 sidebar concept blocks and 0 main-column concept blocks, 0 detected overflows, correct revision toggle behaviour, and correct `1,0,1` repeated-chapter export ordering. At 390px mobile width both the empty source and the archived preview have no document-wide horizontal overflow.
- **Future caution:** with longer or different incoming notes, a concept callout might itself exceed the sidebar page budget. Validate per chapter and split or redesign such a block rather than relying on a blanket safety buffer.


## 10. Replacement chapters 00 and 01 — 2026-11-02 verification

No changes to `engine.js` were needed to integrate the two newly pasted, concise
chapters. All concepts are authored as explicit `.src-side` blocks, so
`normalizedStreams()` does not have to move any on the current edition.
The user-supplied narrative remains in `.src-main`, with 4 semantic tables
(`data-keep="split-table"`), two distinct marked revision zones, and 16
short concept cards. Chapter 00's notable quotation sits in the revision
sidebar and is marked with `data-revision-start="true"` so it hides along
with the summary and starts in the same fresh revision page in PDF.

After modest CSS-only TOC spacing adjustments, `src/tests/smoke_active.py`
verifies the current 18-page pagination, 1-page larger-type TOC, 17 table
rows preserved through splitting, 16 concept blocks in sidebar (0 in main),
no print-column overflow, summary toggling, `1,0,1` repeated-chapter order,
and 390px viewport sizing. This test is deliberately content-specific;
update its expectations when Chapter 02 is added. The archived stress test
is a separate regression and does not affect production content.

Note: the independent main and sidebar print queues leave some sidebars empty
after their notes are exhausted; this is a known layout-quality limitation,
not a data-loss symptom. Do not insert source-unrelated filler to hide it.


### 2026-11-02 — historical checkpoint: independent cover metadata (superseded by Phase C)

The print title page generated by `renderPage({type:'title'})` now says
“An Independent Study Companion,” matching `shell.html`, rather than
implying membership in an official Cambridge-branded series. Its one-line
book description matches the shorter-notes editorial reset and screen
cover. Neither edit changes pagination or element geometry.

## Canonical textbook titles and numbering (November 2026)

- `chapter_catalog.json` is the permanent **00–32 textbook title catalogue**,
  not an indication that unpopulated chapters have content.
- Each active `chNN.html` must use the catalogue's exact official title as
  the chapter root's `data-title` and `.src-hero .ht`. The separate `data-subtitle`
  and `.hs` may describe the user's shorter notes and must never substitute
  for the official book title in navigation or TOC entries.
- `buildChapters`, `renderScreenView`/`buildFlowingHero`, `collectTocEntries`,
  `buildTocRowNodes`, `renderPage`, and reader-ui chapter-row construction
  all read the official `data-title`. Never substitute the notes subtitle.
- Two-digit display numbering (`00`, `01`, etc.) is used on both print content
  running headers and sidebar/scroll-spy chapter labels, matching the TOC badge.
- Only actual active chapter sources get clickable index entries; upcoming
  catalogue chapters are not silently represented as populated content.
- The static `tests/validate_structure.py` validates title/hero consistency
  against the complete catalogue; `tests/smoke_active.py` tests labels in
  HTML and in the generated TOC.


## 12. Chapter 02–03 content-only integration (2026-11-02)

- No changes to `engine.js`. New `ch02.html` and `ch03.html` comply with its
  `.src-main` / `.src-side` stream contract and revision-start markers.
- The previous `tests/smoke_active.py` had hard-coded two-chapter expectations.
  It has been generalized to derive the active chapter list and source counts
  dynamically, and verifies repeated custom-order exports and print overflow.
- The existing independent sidebar-column packing can leave intentional empty
  space; preserving the main-column educational narrative remains the priority.
- Four-chapter print output was verified at 35 pages with no column overflow.

---

## Section-aware educational sidebar V2 — 2026-11-02

### The original problem

Previous `fillPages(mainQ, sideQ, ...)` packed both streams by height independently. Even correctly authored cards could drift to a different historical section's page. The flowing HTML also rendered a single chapter-length sticky sidebar stack at the start, disengaged from individual topics. Both caused monotonous glossary-like reading and unreliable relevance.

### Current structural contract

- Main `data-kind="section-head"` blocks declare `data-section-key="s1"` etc. The revision heading declares `data-section-key="revision"` and `data-revision-start="true"`.
- Each side block declares matching `data-for-section="s1"` etc; the **first revision side block** also carries `data-revision-start="true"`.
- `data-kind` retains educational semantics; `data-display` controls presentation purely through CSS. New side cards use the actual `.def`, `.hy` etc CSS categories. See `SIDEBAR_COMPONENTS.md`.
- `normalizedStreams()` still clones content and moves stray main-column `concept` blocks defensively into the cloned side stream. It now also assigns `data-content-section` on the cloned main blocks; these attributes are **not written to original nodes** in `#chapterData`.

### Screen implementation

`appendPairedSections(host, mainNodes, sideNodes)` groups cloned main and side nodes by section key, creating one `.chapter-grid.section-pair` per section. `renderScreenView()` calls it separately for body and revision. The title page and continuous HTML flow remain unchanged. Each DOM section-head stays in the rendered tree for nav anchors and scroll spy.

### PDF implementation

`packChapter()` first runs `fillPages(mainQ, [], ...)` to paginate the main column. It then calls `attachSectionSideNotes()` to place cards on pages **containing matching section blocks**. This is page-level association, not exact baseline alignment within a single page. When several sections share a page, the sidebar cards may appear at the top of that page; do not claim pixel-level same-row alignment in PDF.

For side notes that overflow the target page, the algorithm tries later pages of that section, then later pages, without backtracking in card order. If necessary it inserts a safe side-only continuation page after the section. Long legacy sidebar lists/tables use `fitSidebarFragment()` and the existing `sliceListBlock()` / `sliceTableBlock()` functions. This is essential to avoid regressing the large, archived Chapter 00–01 glossary fixtures.

### Do not regress

1. Never measure a live original node; `heightOf()` and the split-measurement branches must operate on clones.
2. Reinitialize working table/list rows for every export. Repeated chapter IDs (`1,0,1`) need independent hero/table/list clones.
3. Keep `PAGE_BUDGET` safety buffering. Atomic sidebar cards should not exceed it.
4. The revision sidebar partition is **not** optional: the first revision card must have `data-revision-start`. Revision starts a fresh PDF page.
5. In multi-range export, each repeated occurrence is packed from fresh working copies. Anchored cards must appear once per exported occurrence.
6. Preserve both the old legacy smoke test and new section-alignment test. Both must pass after any engine change.

### New test

`python3 src/tests/smoke_sidebar_alignment.py` verifies meaningful component diversity, all screen aids in the correct section grid, all PDF aids on a page containing their section, zero print overflow, plus no changes to the substantive narrative text relative to the earlier four-chapter baseline. Run it together with `smoke_active.py`, `smoke_legacy.py`, and `validate_structure.py`.

### Full-book PDF publication workflow (November 2026)

	src/tools/export_full_pdf.py

now has strict checks that the printed index contains precisely one link per
chapter, **all link hit-boxes are on the 1280×720 page**, and all PDF links
remain present after merge. It builds an outline with native PyMuPDF
	toc = [[1, chapter_title, absolute_page],
           [2, section_title, absolute_page], ...]

then calls `set_toc(toc, collapse=1)` (chapter nodes open, section nodes
initially collapsed) and `set_pagemode('UseOutlines')` to request that
supporting PDF viewers display the Bookmarks pane. PDF page numbers are
recalculated from the reduced paper index automatically.

The repo CI workflow `.github/workflows/build-bookmarked-pdf.yml` performs
full 16:9 regeneration, structural PDF navigation tests and commits the
result under the existing public filename. The CLI exporter can run locally
with `--chromium /usr/bin/chromium`, or in CI with `--chromium auto` and the
Playwright-managed Chromium. Keep that filename synchronized with the PDF
link in the root README.


## Interactive reading navigation and strict print selection (November 2026)

**Source boundaries:** `src/engine.js` retains the chapter rendering and print
pagination engine, while the new **`src/reader-ui.js`** owns screen-only
navigation behavior. `src/build.py` inlines the latter at
`/*__READER_UI__*/` **after** the core engine and **before** the offline
reader script. Keep that order. The single-file published `index.html`
contains all scripts; the PWA cache hash updates automatically when rebuilt.

### Contents lifecycle

The core `renderScreenView()` now owns **only** `#screenView`, never
`#navToc` or modal listeners. It dispatches `whd:screen-will-render` before
the content subtree is replaced and `whd:screen-rendered` once all chapters
have been attached. The reader module listens to both and constructs its own
chapter links, sections, shortcuts and separate chevrons directly. There is
no `MutationObserver` and no legacy TOC renderer.

Each chapter has independent manually expanded/collapsed state (a Set of
chapter numbers). Expand all and Collapse all intentionally update that Set,
and `syncExpandedState()` applies it to the tree. The Index panel has no
search control or temporary filtering; header full-book search lives in
`src/reader-search.js`.

Chapter titles navigate; chevrons only expand/collapse. Revision shortcuts
point to the real revision heading; definitions and memory aids link to
actual `data-kind="def"`/`data-kind="memory"` blocks; a Questions shortcut
is offered only if a recognizable revision prompt/question block exists.
Nothing is synthesized or added to the chapter content.

### Scroll tracking and resume

The old `setupChapterSpy()` function was removed from engine.js. The
single `src/reader-ui.js` scroll tracker now owns the chapter header,
active chapter and active section highlights, `aria-current="location"`,
and the circular current-chapter progress indicator. The existing
whole-book progress bar retains its separate lightweight `updateProgress()`
handler. Scroll updates **never force any collapsed navigation branch open**.

A device-local `localStorage` record, `whd-reading-place-v1`, saves:
chapter number, stable section anchor `whd-sec-<chapter>-<key>`,
relative chapter position, relative section position, and timestamp.
These anchors are assigned only in the screen DOM; **chapter source HTML is
unchanged**. Writes are throttled, guarded against storage exceptions,
and suppressed during print. On an ordinary later visit to the cover, an
optional prompt offers Continue reading, Start at beginning, Forget saved
place and dismissal. Direct URL fragments and browser-restored scroll
positions override the prompt. No automatic resume jump, account, remote
storage, sync, telemetry, or analytics is introduced.

### Accessible modal drawer

The panel is a `role="dialog"`/`aria-modal="true"` region with `inert`
and `aria-hidden` while closed. Opening transfers focus to the close
button; Escape/backdrop close and restore focus to the opener. Tab/Shift+Tab
are trapped among visible controls. Following a content link moves
focus to the heading instead. Chapter toggle buttons have accessible
labels, `aria-controls`, and `aria-expanded`. The mobile drawer covers
the viewport without shifting the book, and screen-only controls are hidden
from print.

### Strict chapter-range export (engine.js)

`parseChapterRangeInput()` now accepts **only** whole chapter numbers
or explicit integer ranges, separated by commas, e.g. `5-6,1,3,20-24`.
It preserves entered order, reverse ranges and duplicates. Blank interior
tokens, non-numeric suffixes, unknown chapters and out-of-bounds ranges
are errors; **no partial selection prints**. `describeRange()` displays
those errors, sets `aria-invalid` and disables `#printBtn` until corrected.
The print/export controls live inside the collapsible `#navExportPanel`
without changing their original IDs or paginated output behavior.

### Regression coverage

Run `python src/tests/smoke_reader_ui.py` with Playwright Chromium to
exercise search and expansion, keyboard access/focus restoration, active
reading, revision/study links, strict export order and errors, saved resume,
re-render after revision toggles, and 390px mobile geometry. Also run the
existing chapter/print smoke tests after any core engine change.

**Drawer-close regression (resolved in Phase B):** The legacy `openNav()`/
`closeNav()` handlers are removed from `engine.js`. Export dispatches
`whd:drawer-close` with `detail.restoreFocus=true`; the single
`reader-ui.js` `closeDrawer()` updates the dialog, backdrop, scroll lock,
`inert`, aria attributes and opener focus. A section link uses
`closeDrawer(false)`, then focuses the destination. The browser smoke tests
must check both export and reader navigation closure paths.

**Deferred bookmark save (November 2026):** A user may scroll once
immediately after jumping to a chapter, while the brief navigation guard
is still in effect. `reader-ui.js` now schedules a deferred position
capture after that guard expires, instead of requiring another scroll
event; that would silently lose the user's last-read place. The timer is
screen-only and print updates remain suppressed.

---

## Phase A: accessible chapter roles and print-build idempotency (November 2026)

### Chapter palette role derivation
The fixed `CHAPTER_PALETTE` arrays of eight `id` / `contrast` pairs remain unchanged. `ACCESSIBLE_PALETTE` derives, for each pair, `ink` (small colored type on the darkest parchment `#ECE4CE`), `onDark` (small type over navy `#1B2A44`), `contrastInk` (revision text on parchment), and `contrastSurface` (background for white-text revision badges and print headers). `readableHue()` mixes the base hue minimally with black or white to reach at least 4.55:1; color operations use standard sRGB relative luminance. `applyChapterPalette(el,num)` sets six **source** properties on each chapter/page: `--chapter-primary`, `--chapter-primary-ink`, `--chapter-on-dark`, `--chapter-contrast`, `--chapter-contrast-ink`, `--chapter-contrast-surface`. The active `--chapter-color` / `--chapter-ink` are computed by CSS on `.chapter-flow,.page`, not assigned inline. This is essential: `.page.is-revision` must be able to override both active roles; inline active styles would win and make the revision accents wrong. Printed TOC chapter rows explicitly set `--chapter-ink` because they are outside any chapter page.

Do not overwrite `--chapter-color` with the darkened value: decorative marks should retain the user's original chapter palette. Screen revision elements override `--chapter-color` **and** `--chapter-ink` with their contrast equivalents. The print revision page makes the same override; its header uses `--chapter-contrast-surface`.

### Print cache, native Ctrl+P, and double-build guard
`buildPrintView(chapterNumList)` uses `lastPrintSignature = ordered chapter numbers + revision flag`. A second call with an identical signature and an existing page tree returns without repacking. This prevents the Export button's explicit build from being redundantly repeated in the native `beforeprint` callback. Any change in ordered ranges or `INCLUDE_REVISION` invalidates the signature and repaginates.

The `beforeprint` handler **must remain** as a native Ctrl+P fallback, and `lastRange` still denotes the most recently exported ordered selection. Do not use a one-time boolean that would suppress required later rebuilds. To prove idempotency, `smoke_phase_a.py` compares print DOM node identity across duplicate `beforeprint` calls and checks that the page tree is replaced after changing the revision selection.

### Screen anchor positioning
This lives in `styles.css`, not the measured print engine: `scroll-margin-top` is applied to chapter/section/study-aid anchor targets via a responsive `--reader-anchor-clearance` token. Browser smoke tests assert that a linked section is not covered by the sticky header after navigation.

### Associated tests
`src/tests/smoke_phase_a.py` runs from the root via a local HTTP server with Playwright Chromium. It checks the full eight-color role system, revision-page computed styles, print hero identity, anchor clearance, duplicate-build avoidance and revision-triggered rebuild. Keep it in the `verify-pages.yml` workflow beside `smoke_reader_ui.py`. Do not modify chapter sources or the fixed page-packing dimensions for these cosmetic correctness changes.


---

## Phase B — single reader ownership and position-preserving rebuilds (November 2026)

### Explicit lifecycle and one modal owner

`engine.js` dispatches `whd:screen-will-render` and
`whd:screen-rendered` around every `renderScreenView()` call, including
the empty-book branch. It no longer constructs a legacy Contents tree,
opens or closes the modal, or owns a competing chapter spy. The print Export
button dispatches `whd:drawer-close` before `window.print()`; the same
`reader-ui.js` handler manages backdrop, classes, focus and body scroll lock
for all close paths. The engine retains page export, palette assignment and
the lightweight whole-book progress rail.

### Preserve viewport location when revision pages appear or disappear

On first load, `captureView()` returns null because no previous chapter tree
exists; this preserves the browser's native history scroll restoration.
Before a subsequent screen-tree rebuild, `captureView()` records the active
chapter and a main-content block ordinal (including the chapter hero), the
relative fraction inside that block at a viewport anchor, and a scroll fallback.
After rendering, `buildChapterRows()` recreates the navigation and
`restoreView()` maps the same ordinal block into the new chapter tree.
When a revision block was removed, the last surviving body block is a sensible
fallback. The bookmark write guard prevents synthetic repositioning from
immediately overriding a saved reading choice. Absolute `scrollY` is not a
valid identity for this test because removing dozens of earlier revision zones
necessarily changes global document height. Test the same section's
*viewport-relative* position and the drawer's focus/scroll state instead.

### Index tree, keyboard and mobile

The Index panel is navigation-only: chapter links, individual section toggles,
learning shortcuts and Expand all / Collapse all buttons. `addLink()` creates
plain-text anchors, `updateExpanded()` reads `manualExpanded`, and
`syncExpandedState()` synchronizes visibility plus ARIA attributes after
TOC rebuild or manual changes. There is **no Index search/filter**. Escape
closes the modal directly; a single document keydown handler traps Tab. The
mobile chapter label stays visible and the UI uses approximately 44px touch
targets, independent panel scroll regions and dynamic viewport units.
`main#screenView` remains a landmark and keyboard skip-link target.

### Regression suite

Run:
`python src/tests/smoke_reader_ui.py`
`python src/tests/smoke_reader_interactions.py`
`python src/tests/smoke_phase_a.py`

The Phase B suite now checks navigation-only Index controls, keyboard
close/focus, export scroll unlock, viewport-relative reading preservation
on revision toggles, mobile touch target sizes and overflow. The header search
has separate whole-book interaction tests. It does not modify
any chapter content or the fixed 1280×720 PDF page measurements.

---

## Phase C — sidebar rail, mobile tables and print-cover copy (November 2026)

### One source of publication copy

The screen cover is authored in `src/shell.html` as `#titlePage` with `.tp-mark`, `.tp-series`, `.tp-title`, `.tp-subtitle`, `.tp-rule`, `.tp-desc` and `.tp-imprint`. `renderPage({type:'title'})` now clones these **seven existing nodes** and gives each clone the equivalent `.pt-*` class. That prevents cover-copy drift between the screen reader and PDF while preserving print-specific typography and dimensions. If a cover field is removed, print rendering throws an intentional error rather than printing an incomplete cover. Print footer labels on chapter heroes, contents and ordinary chapter pages now all read `World History Dossier`; page numbers and chapter running headers are unchanged. The screen-only `.tp-pdf-access` action is intentionally **not** cloned into the PDF.

### Pairing with no empty aid rail

`appendPairedSections()` still pairs every authored main section with side cards whose `data-for-section` matches the section key. It marks a `.section-pair.no-side` when the section has no side cards. CSS then makes that row single-column, allowing comparisons and text to use the full reading width. Sections that have authored side content retain their two-column pairing on desktop and stacked layout on mobile. No chapter source or PDF `attachSectionSideNotes()` logic is altered.

### Responsive table affordances: display only

`updateScreenTableAffordances()` executes after the flowing tree has been appended and on resize. It checks actual horizontal overflow using `scrollWidth > clientWidth + 2`. Only overflowing screen table wrappers acquire `role=region`, a descriptive ARIA label, `tabindex=0`, an `aria-describedby` hint ID, and a short screen-only `Swipe sideways to view all columns` prompt. When the table fits, all extra attributes/hints are removed; keyboard users are not forced through dozens of non-scrollable tables. CSS enforces a legible minimum width for three-/four-column tables on narrow devices and scrolls only within the screen wrapper. This function never touches the pristine `#chapterData` source or measured `#printView` table copies. Maintain unique hint IDs across the full document.

### PDF publishing affordance

The screen cover and the Export drawer both open `./20th-Century%20International%20History.pdf` (relative to the hosted reader), as does the new `<noscript>` fallback. The prebuilt PDF contains native bookmarks; browser exports of custom ranges may not. The large PDF is intentionally **not** included in the service worker's offline precache and has its own `rel=alternate` metadata in the document head. Update `src/docs/reference/PDF_NAVIGATION.md` if the name or semantics change.

### Testing

`python src/tests/smoke_phase_c.py` checks cover parity, PDF link destinations, full-width empty-aid sections, source-grounded sidebar pairing, true table overflow affordances and 16:9 print footer/geometry. Re-run all existing Phase A and B Playwright suites plus `python src/build.py -o index.html --check`. Full bookmarked PDF generation/outline validation remains the independent `build-bookmarked-pdf.yml` workflow.


## Phase D — documentation and source integrity verification (November 2026)

`src/tests/verify_docs_sync.py` checks active CSS/JavaScript role names in `CSS_DOC.md`/`JS_DOC.md`, source links and the release test inventory. When provided a Git base ref, it checks changed files: CSS edits require a same-PR CSS reference update; changes to `engine.js`, `reader-ui.js` or `offline-reader.js` require a JS reference update. Editing the release CI workflow requires updating `src/docs/release/RELEASE_VERIFICATION.md` in the same PR. This phase changes **verification and documentation only**, not reader logic or PDF pagination.

The release browser suite captures responsive screenshots, uses axe-core for scoped WCAG audit, tests real PWA offline updates and verifies strict ordered/repeated chapter selection. A separate pull-request `release-pdf` CI job builds a *fresh* 16:9 PDF and checks every page's geometry and text bounds as well as representative raster differences and PDF chapter/section bookmarks. The [Phase D runbook](docs/release/RELEASE_VERIFICATION.md) lists both automated and manual review. Pages currently deploys directly from `main`; protect that branch with required `verify` and `release-pdf` checks to make review a hard pre-deployment gate.

## Batch 1 — modal and edition-notice resilience (November 2026)

`reader-ui.js` owns a snapshot of the inert state of every direct body child
except `#navPanel` and `#navOverlay`. On modal open it makes background
reading, cover, progress/navigation chrome, and independent notices inert;
on close it restores each element's previous state **before** returning focus.
Do not replace this with focus trapping alone; it would permit assistive
technology to reach controls behind the open drawer. Normal close, backdrop,
Escape, navigation, and the print/export `whd:drawer-close` event must converge
on the same cleanup.

`offline-reader.js` sends `whd:edition-notice` with `detail.visible`
whenever the update notice is presented or dismissed. The reader defers the
optional Continue Reading prompt while an edition notice is visible and may
restore it after dismissal only if a valid saved checkpoint remains and the
reader has not navigated, moved, or dismissed the suggestion. The persistent
reading checkpoint is never cleared by this notice coordination.

`src/service-worker.template.js` separates `CORE_ASSETS` from
`OPTIONAL_ASSETS`: failed supplemental icon, social-preview, sitemap, robots
or 404 downloads cannot abort installation of a complete HTML reader.
Installation still rejects a missing required resource, and the offline-ready
indicator in `src/offline-reader.js` checks only core resources. Keep both
copies of this contract aligned when new functional assets are introduced.

## Batch 3: Manual edition checks and readable saved identifiers

`src/offline-reader.js` identifies a **complete saved** cache by the established `whd-edition-` prefix and required reader assets, showing its 12-character suffix in `#offlineEditionId`. The `#offlineCheckUpdate` button invokes a manual service-worker `registration.update()` even inside the ordinary one-minute background-check throttle, announcing offline, error, no-new-version and update-in-progress states in `#offlineCheckResult`. `controllerchange` retains the existing user-controlled reload prompt and updates the saved-edition label; it does not automatically reload or touch the bookmark. The former contents-only search in `src/reader-ui.js` has been removed; header full-book search is implemented in `src/reader-search.js`.

## 2026-11-06 — Reader Index / Tools tab model

`src/reader-ui.js` now owns the modal drawer's accessible two-view tab
model. `switchNavView('index'|'tools',focus)` updates each tab's
`aria-selected`, roving `tabIndex`, and panel `hidden`/`inert`.
Left/Right arrows and Home/End switch and focus tabs; mouse/touch click
activates a view. Opening Contents defaults to Index. The floating opener,
background inert isolation, Escape/backdrop dismissal and focus return remain.

`focusables()` explicitly excludes inactive tab buttons and inert descendants
from the modal trap. Index owns `#navToc` and tree expansion (no search).
Tools owns `#includeRevisionChk`, `#navExportPanel`, `#rangeInput`,
`#printBtn`, the prebuilt PDF link and offline status/actions. The revision
switch **still affects BOTH screen and custom-print composition**; the
existing range grammar, repeat/order semantics and
`whd:drawer-close` are unchanged. A new Tools-only Continue Reading action
uses the existing `resumeReading()` checkpoint and hides when unavailable;
`saveCurrent`, `forgetSaved`, and `initializeResume` synchronize it.
No new localStorage key or scroll tracker is introduced.

`src/shell.html` exposes `#navIndexTab`, `#navToolsTab`,
`#navIndexPanel`, `#navToolsPanel`, `#navToolsResumeSection` and
`#navToolsResume`. This screen-only component does not touch
`#chapterData`, `#printView` or the independent 16:9 pagination engine.


## November 2026 — full-book search in the reading header

The independent `src/reader-search.js` is inlined by `src/build.py` at
`/*__READER_SEARCH__*/` in `src/shell.html`. The existing `src/reader-ui.js`
still owns the navigation-only Index tab, the modal Contents drawer,
the reading bookmark and active-section highlighting.
Neither the pagination engine nor authored source chapters are modified.

`WHDReaderSearch.buildIndex(document)` creates a lazy, local text corpus
from **all 33 immutable `#chapterData > .chapter-source` nodes**, including
chapter hero information, paragraphs, headings, table cells/captions,
inline emphasis, learning sidebars, diagram labels and revision sections.
Do not index `#printView`'s page clones. Each normalized passage stores
its source order, chapter title/number, section, revision status and a
generated content-fingerprint link. Search applies case and accent folding,
requires every term within a passage, ranks exact phrases and headings,
and displays highlighted contextual excerpts in batches of 30. Its pure
helper methods can be tested without a browser.

The screen compositor destroys/rebuilds `#screenView` on
`#includeRevisionChk` changes. `whd:screen-will-render` ensures the
search corpus exists and stamps inert `data-whd-search-key` attributes
on original source text units *before* the normal engine clones them.
The search keeps those keys through `whd:screen-rendered` and resolves
them against the current live `.chapter-flow` only when navigating.
This is deliberate: do not cache stale rendered element references or
move original nodes out of `#chapterData`. No MutationObserver,
localStorage key, or second reading position tracker is introduced.

The header's `#readerSearchInput` displays a viewport-bounded popover
(`#readerSearchResults`) with native button results and
`#readerSearchHits`, a count (`#readerSearchStatus`), Show more,
clear and close controls. Slash focuses the field outside edit controls;
Up/Down/Enter navigate; Escape dismisses; click-away closes. A chosen
passage receives a shareable `#whd-hit-...` URL fragment, focus and
scroll into view, and transient CSS Custom Highlight API decoration where
supported. Query generations invalidate stale debounced render callbacks.
Text nodes and `mark` are used for safe highlighted excerpts, never
query-derived `innerHTML`.

When a revision hit is absent from the current screen because the
Tools **Include chapter summaries** option is unchecked, the search uses
that same existing control's change handler to re-enable summaries,
with a temporary `#readerSearchFeedback` announcement. It does
not set a separate persistent preference or touch print architecture.

Rebuild `index.html` and the service worker together. Test browser
search, deep links, mobile widths, revision-hidden jump, results paging
and the existing Index filter separately. Any edits to this JS file
must update `src/JS_DOC.md` in the same change.


## 2026-11-06 — Remove sidebar contents filter

`src/reader-ui.js` no longer resolves `#tocSearch`, `#tocClearSearch`, `#tocSearchStatus`, or `#tocNoResults`. `applySearch()`, `highlightLink()`, and its local `normalize()` were deleted; no content search or text highlights run inside the Contents drawer. The chapter tree is unchanged: `syncExpandedState()` renders `manualExpanded` decisions through `updateExpanded()`, and Expand all / Collapse all remain always available. Escape simply dismisses the drawer and restores opener focus. The independent header `src/reader-search.js` still performs complete-book text matching and deep links; neither chapter source nor PDF pagination changes. Browser tests should confirm old Index search controls are absent and header search still works.


## Full-book search and revision visibility (November 2026)

\`src/reader-search.js\` indexes meaningful authored text from \`#chapterData\`,
then filters its results against the current \`includeRevisionChk\` (Contents
→ Tools) setting. The source index remains complete, but **hidden revision
sections are not returned as search hits**. Toggling revision visibility
refreshes any open result list after the screen engine has rebuilt its
chapter clones. Selecting a stale hidden hit cannot override the user's
choice or automatically tick \`includeRevisionChk\`.

A previously shared \`#whd-hit-...\` URL referencing revision content may
fall back to its existing chapter when revisions are hidden; it does not
silently change the Tools setting. The screen-reader revision toggle and
the print compositor's chapter-range/revision signature remain otherwise
unchanged. Browser checks in \`src/tests/smoke_reader_ui.py\` and pure search
checks in \`src/tests/test_full_text_search.mjs\` cover these boundaries.


## 11. Full-text search visibility and exact passage navigation (2026-11-06)

`src/reader-search.js` indexes both the main notes stream and the chapter-side learning cards. The revision boundary is **sticky per stream**: after encountering `data-revision-start="true"`, `data-section-key="revision"`, or `data-for-section="revision"`, subsequent blocks in that stream are revision content even if later blocks omit the marker. The active **Include chapter summaries** setting is applied inside `find(index, query, {includeRevision:false})` before relevance ranking and paging, not by hiding rendered result buttons afterward. This keeps the scope consistent with the chapter reader and prevents hidden end-of-matter material from reappearing through search.

Search result clicks target the exact generated passage key using an instant scroll, rather than leaving a previous smooth-scroll animation in flight; stale hidden revision results must not switch the reader's visibility preference. Rebuild the published `index.html` and content-hashed `service-worker.js` using `python src/build.py -o index.html`, then run `src/tests/test_full_text_search.mjs` and the browser interaction suite. Preserve `#chapterData` as the immutable authored source.
