# World History Dossier

**A complete 33-chapter digital companion to 20th-century international history**, presented in the Imperial Archive reading style.

**[Read the online book](https://mohdujjain.github.io/world-history-dossier/)** · **[Download the complete 245-page PDF](20th-Century%20International%20History.pdf)**

## The book

The dossier covers Chapters **00–32**, from imperialism and the First World War through decolonization, the Cold War, globalization, and the consequences of September 11. Its reader includes a navigable chapter and section index, historical comparisons, timelines, thematic learning aids, and dedicated end-of-chapter revision sections.

The single-file `index.html` works in a browser without an application server. Its export panel supports chapter ranges such as `5-6,1,3,20-24`, preserves the specified order, and lets you include or exclude revision sections when printing to a **16:9 landscape PDF**.

## Install as an app

In supported browsers, install the dossier on your device for a dedicated app-like window and an icon on the home screen or desktop. On Chrome or Edge, use **Install app** (usually in the address bar or browser menu). On iPhone or iPad, use **Share → Add to Home Screen**. After opening the online reader once, its chapters are available offline; the separately hosted PDF is not pre-cached. See the [PWA installation guide](src/docs/hosting/PWA.md) for details.

## PDF navigation

The bookmarked PDF has a concise, three-page contents listing all 33 chapters. Each chapter title is clickable, and the PDF reader's **Bookmarks / Outline** panel offers an expandable chapter-and-section hierarchy for jumping directly to any topic. See the [PDF navigation guide](src/docs/reference/PDF_NAVIGATION.md).

## Repository guide

| Location | Purpose |
| --- | --- |
| [`index.html`](index.html) | Published standalone HTML reader |
| [`20th-Century International History.pdf`](20th-Century%20International%20History.pdf) | Complete pre-rendered PDF |
| [`src/chapters/`](src/chapters/) | All 33 editable chapter modules |
| [`src/styles.css`](src/styles.css) and [`src/engine.js`](src/engine.js) | Shared styling and interactive/print engine |
| [`src/build.py`](src/build.py) | Assembles the reader from modular source |
| [`src/README.md`](src/README.md) | Developer quick start |
| [`src/docs/README.md`](src/docs/README.md) | Organized documentation index |

## Rebuilding

From the repository root, with Python installed:

```bash
python src/build.py -o index.html
python src/build.py -o index.html --check
python src/tests/validate_structure.py
```

Whenever shared CSS or JavaScript changes, update its living documentation in the same commit: [`src/CSS_DOC.md`](src/CSS_DOC.md) or [`src/JS_DOC.md`](src/JS_DOC.md). The separate full-book PDF should be regenerated if the book content changes.

This site is hosted on GitHub Pages from the `main` branch at the repository root.

## Editorial note

These are study notes prepared from supplied textbook summaries; they have **not been independently fact-checked**. See the chapter-specific editorial reports in [`src/docs/editorial/`](src/docs/editorial/) for source caveats, and review attribution/copyright permissions before redistribution.
