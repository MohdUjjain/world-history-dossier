# World History Dossier — Complete Edition

A single-file interactive reading edition of **33 chapters (00–32)** of 20th-century international history study notes, using the Imperial Archive theme and Educational Sidebar V2 learning aids.

## Read the book

**[Open the online reader](https://mohdujjain.github.io/world-history-dossier/)** (after GitHub Pages is enabled).

The `index.html` file is self-contained: the screen reader, chapter navigation, revision controls, and print/export engine run entirely in your browser.

## Printing and chapter selection

Use the reader's sidebar to choose chapters (including ranges such as `5-6,1,3,20-24`), include or exclude revision sections, and export the selected content for printing as a **16:9 landscape PDF**.

A separate pre-rendered 259-page PDF exists in the project release package, but it has **not yet been added to this GitHub repository**. Upload `World_History_Dossier.pdf` to the repository root if you also want a direct PDF download on this site.

## Enable GitHub Pages

Go to **Settings → Pages → Build and deployment**. Choose **Deploy from a branch**, select **main** and **/(root)**, and save. The site will be available at:

https://mohdujjain.github.io/world-history-dossier/

## Maintainable source

The full editing/rebuild archive includes `src/chapters/ch00.html` through `ch32.html`, `styles.css`, `engine.js`, `shell.html`, `build.py`, and living `CSS_DOC.md` and `JS_DOC.md`. It is available in the separate project source ZIP; it is **not yet uploaded to this repository**.

After adding those source files, run `python src/build.py -o index.html` when updating the book. Whenever you change CSS or the print engine, update their corresponding living documentation in the same commit.

## Editorial notice

These are study notes based on supplied textbook summaries, not independently fact-checked. Check copyright and attribution permissions before redistributing.
