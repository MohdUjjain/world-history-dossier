# World History Dossier — Complete Edition

An interactive Imperial Archive reading companion to **20th-century international history**: **33 chapters (00–32)**, timelines, comparisons, section-linked learning aids, and end-of-chapter revision sections.

**[Read the online book](https://mohdujjain.github.io/world-history-dossier/)** · **[Download the complete 259-page PDF](World_History_Dossier.pdf)** · **[View the social-preview image](og-image.jpg)**

## Online reader

The published website is a **single standalone HTML file** (`index.html`), with no framework or backend. Open the table of contents using the **Contents** tab. The export drawer supports custom chapter order (e.g., `5-6,1,3,20-24`), repeat selections, and an include/exclude revision toggle. Use the reader's print/export option for a custom 16:9 landscape PDF, or download the full pre-rendered PDF above.

## Social-sharing preview

The `<head>` in `index.html` contains the official page title, description, canonical URL, Open Graph tags, and Twitter/X card tags. The `og:image` field points to **https://mohdujjain.github.io/world-history-dossier/og-image.jpg** (1200 × 630 JPEG). The same metadata is maintained in **`src/shell.html`** so it survives rebuilding the website. For accurate previews, the image and HTML must both be deployed to the same public site. Messaging apps may cache a prior preview; try sharing `?v=2` once if the card remains stale.

## Editable source

The canonical source lives in `src/`: 33 chapter modules, `styles.css`, `engine.js`, `shell.html`, `build.py`, test scripts, historical-editorial notes, and the two living references (`CSS_DOC.md` / `JS_DOC.md`). Build and validate it from the repository root:

```bash
python src/build.py -o index.html
python src/build.py -o index.html --check
python src/tests/validate_structure.py
```

Whenever `src/styles.css` changes, update `src/CSS_DOC.md` in the same commit. Whenever `src/engine.js` changes, update `src/JS_DOC.md` in the same commit. After editing chapters, rebuild `index.html` and regenerate the separate PDF if necessary.

## Hosting

This public repository is published via **GitHub Pages** from **`main` → `/(root)`**. Changes to `index.html`, `og-image.jpg`, or the PDF are deployed after committing to `main`; the Pages settings do not need to be changed.

## Editorial note

These are study notes based on supplied textbook summaries and have **not been independently fact-checked**. Examine the editorial notes and confirm copyright/attribution permissions before redistributing source material.
