# GitHub Pages — Publishing and maintenance

**Repository:** https://github.com/MohdUjjain/world-history-dossier  
**Live reader:** https://mohdujjain.github.io/world-history-dossier/  
**Branch and folder:** `main` → `/(root)` (already configured)

## Published files

- `index.html` — complete interactive 33-chapter reader.
- `20th-Century International History.pdf` — pre-rendered full-book PDF.
- `og-image.jpg` — social preview image.
- `.nojekyll` — serves files without Jekyll processing.
- `src/` — maintainable chapter/source modules and documentation.

The book PDF is intentionally named **`20th-Century International History.pdf`**. Use this link, preserving URL encoding:  
https://mohdujjain.github.io/world-history-dossier/20th-Century%20International%20History.pdf

## Installable reader

The site is also an installable **Progressive Web App**. Its root manifest (`manifest.webmanifest`), root service worker (`service-worker.js`), and app icons (`icons/`) are published alongside `index.html`. The installation integration is maintained in `src/shell.html`. See [the PWA guide](PWA.md) for browser instructions, scope, offline caching and updates.

## Bookmarked PDF

The pre-rendered 245-page PDF has a three-page, chapter-only printed contents and a native outline with 33 expandable chapters and 211 section bookmarks. See the [PDF navigation guide](../reference/PDF_NAVIGATION.md).

Print-source changes trigger the `.github/workflows/build-bookmarked-pdf.yml` workflow, which validates the HTML, regenerates the PDF and commits it under the existing filename. A direct browser **Print → Save as PDF** export may lack native PDF bookmarks; use the pre-rendered file for the best navigation.

## Making a change

From your locally cloned repository:

```bash
git pull --ff-only origin main
# Edit the needed files under src/
python src/build.py -o index.html
python src/build.py -o index.html --check
python src/tests/validate_structure.py
git add -A
git commit -m "Update World History Dossier"
git push origin main
```

The PDF should be regenerated separately if book content or print styling changes. GitHub Pages deploys automatically after pushes to `main`; the existing Pages settings do not need adjustment.

## Share-card metadata

The canonical page title, description, Open Graph image reference and Twitter card tags live in **`src/shell.html`**, not solely in the assembled HTML. The image resides at the repository root and should remain directly accessible at:  
https://mohdujjain.github.io/world-history-dossier/og-image.jpg

If a social app still shows an older cached thumbnail, allow its cache to refresh or test the URL with a temporary query parameter.

## Documentation rules

Keep `src/CSS_DOC.md` synchronized with `src/styles.css`, and `src/JS_DOC.md` synchronized with `src/engine.js`, in the same commit as a corresponding edit. For other documentation, start at [the documentation index](../README.md).
