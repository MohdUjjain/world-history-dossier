# PDF navigation — chapter index and bookmarks

The complete 33-chapter PDF is a true landscape 16:9 reference edition.

## Two ways to navigate

1. **Printed contents (pages 2–4):** Only the **33 chapter titles** are listed, with live page numbers. Select any chapter title to jump to its opening page. The index stays short and readable.
2. **PDF Bookmarks / Outline panel:** Contains **33 chapter entries**, expandable to **211 section entries**. In Chrome or Edge, open the PDF viewer's Contents/Document outline or Bookmarks panel (where supported). In Adobe Acrobat Reader, choose the Bookmarks navigation panel. Select a section to jump straight to its page.

The bookmarks are native PDF objects, not just HTML links. The PDF metadata requests `UseOutlines` as the initial page mode; individual readers may override that preference. The on-screen HTML reader still has its own independent collapsible chapter/section navigation.

## Generation and verification

Use the maintained source in `src/` rather than editing the PDF page count manually:

```bash
python src/build.py -o index.html
python src/tools/export_full_pdf.py --book index.html --out '20th-Century International History.pdf' --batch-size 16 --chromium /usr/bin/chromium
python src/tests/validate_pdf_navigation.py '20th-Century International History.pdf'
```

The GitHub Actions workflow `build-bookmarked-pdf.yml` runs the exporter using Playwright-managed Chromium when print-relevant source files change; it can also be run manually.

**Important:** Saving the browser's in-app export directly to a PDF may not preserve native bookmarks in all browsers. Use the repository's **pre-rendered bookmarked edition** for full outline navigation. The separate chapter-range print control is still useful for custom PDF excerpts.
