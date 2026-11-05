# World History Dossier — Reader navigation and reading position

The single-file HTML reader has a screen-only navigation layer:
`src/reader-ui.js`, inlined into `index.html` from `src/build.py`.
It does **not** alter the chapter source modules or 16:9 PDF pagination.

## Contents drawer

- The right-edge floating Contents button opens a full-height, non-reflowing
  drawer; the mobile layout fills the viewport behind a backdrop.
- Chapter titles are **links to chapters**, separate from their chevrons.
  Chevron buttons expand/collapse nested section and study-shortcut links.
- Search matches chapter numbers, chapter titles, section headings, revision
  headings and shortcut labels. It opens matching branches only temporarily;
  clearing search returns to the reader's manual expansion choices.
- Expand all and Collapse all deliberately set the chapter states.
- The current chapter and section are highlighted as reading progresses;
  `aria-current="location"` marks the active link. Scrolling never expands
  a branch automatically.
- The drawer is a modal dialog: Escape/backdrop closes it, focus returns to
  the opener, Tab/Shift+Tab remain inside, and hidden branches are unfocusable.

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
`src/reader-ui.js` rebuilds the core's screen-only navigation whenever the
rendered chapter tree changes (including revision toggles); it also owns
focus management, active reading and resume. The old core chapter spy is
disabled to avoid competing updates. The existing progress rail is preserved.

Update **`src/JS_DOC.md`** in the same commit as engine modifications and
**`src/CSS_DOC.md`** with any `src/styles.css` change. Source is assembled
through `src/build.py`, which updates the PWA's hashed worker automatically.

From the repository root:

```bash
python src/build.py -o index.html
python src/build.py -o index.html --check
python src/tests/validate_structure.py
python src/tests/smoke_reader_ui.py
```

The new browser smoke test runs against a local HTTP server and checks search,
keyboard focus, Escape, mobile viewport, progress, shortcuts, ordered printing,
validation, and optional resume. Re-run the older print smoke tests when
pagination or chapter content changes.
