# World History Dossier — Reader navigation and reading position

The single-file HTML reader has a screen-only navigation layer:
`src/reader-ui.js`, inlined into `index.html` from `src/build.py`.
It does **not** alter the chapter source modules or 16:9 PDF pagination.

## Contents drawer

- The right-edge floating Contents button opens a full-height, non-reflowing
  drawer; the mobile layout fills the viewport behind a backdrop.
- Chapter titles are **links to chapters**, separate from their chevrons.
  Chevron buttons expand/collapse nested section and study-shortcut links.
- Search matches chapter numbers, titles, section/revision headings, and study
  shortcuts. Results highlight matched phrases, distinguish matching chapter
  and section counts, and offer a clear control and zero-results message.
  Filtering temporarily expands matching branches without altering manually
  chosen expansion. A focused search clears on the first Escape and the
  drawer closes on a second Escape.
- Expand all and Collapse all deliberately set the chapter states.
- The current chapter and section are highlighted as reading progresses;
  `aria-current="location"` marks the active link. Scrolling never expands
  a branch automatically.
- The drawer is a single-owner modal dialog: Escape/backdrop closes it,
  focus returns to the opener, Tab/Shift+Tab remain inside, and hidden
  branches are unfocusable. Expand/collapse is disabled while filtering.
  On mobile, tap targets are approximately 44px; the drawer scrolls
  independently over the book.

## Study shortcuts

Each chapter offers links only to content actually present:

- **Revision:** the chapter's revision heading when revision is included.
- **Definitions:** the first authored definition card.
- **Memory aids:** the first authored memory card.
- **Questions:** an authored revision prompt/question block when present.

The module assigns screen-only anchors to those items. Original source notes
are not rewritten. Revision shortcuts disappear when summaries are excluded.

## Reading progress and optional resume

The existing narrow bar tracks whole-book physical scroll progress.
A separate circular percentage ring indicates progress through the current
chapter, adopting its identity accent color. Both are reading position,
**not** proof of studying, mastery, or completion.

A device-local bookmark in `localStorage` under
`whd-reading-place-v1` saves chapter number, stable section ID, approximate
section/chapter fraction, and timestamp. On a subsequent visit **to the cover**
it may offer Continue reading, Start at beginning, Forget saved place or
dismissal. It does not auto-jump; a direct URL fragment or browser-restored
scroll position takes precedence. This data stays in the local browser and
is not sent to GitHub or anywhere else. Private-mode restrictions and clearing
site data can remove it. Printing suppresses writes.

## Print controls

Print / Export PDF is collapsed by default to prioritize the index on small
screens. The same revision toggle remains available. Range input accepts
integer chapter numbers and inclusive ordered ranges (`6-5,1,6` is valid),
preserving explicitly repeated chapters. Unknown, malformed or empty entries
display a clear error and disable printing until fully corrected. The
print engine and its chapter-only PDF contents/bookmarks remain unchanged.

## Architecture and tests

`src/engine.js` owns the chapter render and paginated PDF export.
`src/engine.js` dispatches `whd:screen-will-render` and
`whd:screen-rendered` events around each screen rebuild. `reader-ui.js`
creates and owns the only Contents tree and drawer, with no legacy engine
modal handlers or TOC MutationObserver. It snapshots a viewport-relative
main-content block before a revision visibility change and restores that
place afterward. Export closes via the single `whd:drawer-close` event.
The screen reader has a `main` landmark and skip link; mobile retains
current-chapter context in the header. The PDF engine and whole-book
progress rail are preserved.

Update **`src/JS_DOC.md`** in the same commit as engine modifications and
**`src/CSS_DOC.md`** with any `src/styles.css` change. Source is assembled
through `src/build.py`, which updates the PWA's hashed worker automatically.

From the repository root:

```bash
python src/build.py -o index.html
python src/build.py -o index.html --check
python src/tests/validate_structure.py
python src/tests/smoke_reader_ui.py
python src/tests/smoke_reader_interactions.py
python src/tests/smoke_phase_a.py
```

The new browser smoke test runs against a local HTTP server and checks search,
keyboard focus, Escape, mobile viewport, progress, shortcuts, ordered printing,
validation, and optional resume. Re-run the older print smoke tests when
pagination or chapter content changes.

The Phase B browser suite covers search highlighting and empty results, focus/keyboard modal behavior, revision-toggle viewport continuity, export scroll restoration, 390px/320px mobile context, and tap-target geometry.
