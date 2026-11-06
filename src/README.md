# World History Dossier — Source guide

The **complete edition comprises Chapters 00–32 (33 chapters)**. This directory is the maintained source for the single-file HTML reader and the landscape-print engine.

## Source layout

| Path | Description |
| --- | --- |
| `shell.html` | HTML shell and metadata for the published reader |
| `styles.css` | Imperial Archive screen and print design |
| `engine.js` | Chapter navigation, section pairing, pagination and export |
| `build.py` | Builds `index.html` and generates a content-hashed offline service worker |
| `reader-ui.js` | Accessible navigation-only Index tree, revision shortcuts, active section tracking, chapter progress and local resume |
| `reader-search.js` | Local full-book text search of passages, tables, side aids and revisions; inlined into the offline reader |
| `offline-reader.js` | Offline-ready status, persistent storage request and new-edition notifications; inlined into `index.html` |
| `service-worker.template.js` | Atomic precache, scoped cache cleanup and optional Google Fonts response caching |
| `chapter_catalog.json` | Official titles for all 33 chapters |
| `chapters/ch00.html` … `chapters/ch32.html` | Active authoring modules |
| `tests/` | Structural and browser/print regression checks |
| `tools/export_full_pdf.py` | Reproducible batched 16:9 PDF export |
| `archive/` | Superseded legacy chapter fixtures (not active) |
| [`docs/`](docs/README.md) | Editorial reports, authoring references, project history and hosting guide |

Two living engineering references intentionally remain at stable paths alongside the files they document:

- [`CSS_DOC.md`](CSS_DOC.md) — maintain with every change to `styles.css`
- [`JS_DOC.md`](JS_DOC.md) — maintain with every change to `engine.js`

Do not move these two references without also changing the established re-entry/maintenance workflow.

## Build and validate

Run from the **repository root**:

```bash
python src/build.py -o index.html
python src/build.py -o index.html --check
python src/tests/validate_structure.py
python src/tests/verify_publication.py
node src/tests/test_offline_cache.mjs
python src/tests/smoke_reader_ui.py
```

Writing the published `index.html` also regenerates `service-worker.js` with a version derived from the book and small public assets. The `--check` command returns a nonzero exit status when either generated file is stale. The original `python src/build.py` without `-o` still produces `book.html` for development.

The standalone reader has no external runtime dependencies. Full-book PDF export additionally requires local Chromium, Python Playwright, BeautifulSoup and PyMuPDF:

```bash
python src/tools/export_full_pdf.py --chromium /usr/bin/chromium --batch-size 16
```

The PDF exporter produces true 16:9 paginated pages, a short chapter-only printed contents, clickable chapter destinations, and a native two-level chapter/section bookmark outline. See [the PDF navigation guide](docs/reference/PDF_NAVIGATION.md).

## Working conventions

1. Author a chapter in `src/chapters/chNN.html`, using the established `.chapter-source`, `.src-hero`, `.src-main` and `.src-side` structure.
2. Follow the [notes workflow](docs/authoring/NEW_NOTES_WORKFLOW.md) and [sidebar component guide](docs/authoring/SIDEBAR_COMPONENTS.md).
3. Rebuild `index.html`, run the structural checks and relevant smoke tests, and visually inspect representative screen/print pages.
4. Keep CSS and JavaScript reference documentation synchronized with corresponding production edits, in the **same change**.
5. Use the [documentation index](docs/README.md) for chapter-specific editorial cautions and the [checkpoint archive](docs/history/PROJECT_CHECKPOINTS.md) for the project's development history.

The published book and full PDF are in the repository root. For hosting and link details, see [the GitHub Pages guide](docs/hosting/DEPLOYMENT.md).
