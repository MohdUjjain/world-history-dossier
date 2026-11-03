# World History Dossier — modular publishing source

**Final planned edition: Chapters 00–32 (33 chapters, 3 November 2026).**

This project turns the user's concise chapter-by-chapter international-history notes into
one polished flowing HTML reader and a true 16:9 paginated, searchable PDF. The active chapters were created from the user's newer pasted notes, not from the archived
long versions. See `MIGRATION_STATUS.md` and `NEW_NOTES_WORKFLOW.md`.

## Directory map

```
src/
  shell.html                  title page, header, export drawer, HTML containers
  styles.css                  screen + print design system → CSS_DOC.md
  engine.js                   pagination, TOC, navigation, export → JS_DOC.md
  chapters/
    ch00.html                 Introduction: Twentieth-Century International History - The Changing Face of Empire
    ch01.html                 Imperialism
    ch02.html                 Nationalism (combined from two user texts)
    ch03.html                 Internationalism
    ch04.html                 A Shrinking World
    ch05.html                 A Changing Diplomatic World
    ch06.html                 The Triple Alliance
    ch07.html                 The Ententes, 1894–1914
    ch08.html                 The July Crisis
    ch09.html                 Wartime Promises and Postwar Europe
    ch10.html                 Wartime Promises and the Postwar Empires
    ch11.html                 Envisioning a New World Order
    ch12.html                 The Versailles System
    ch13.html                 The Legacy of the First World War
    ch14.html                 Why International Finance Mattered: 1919–1939
    ch15.html                 The Far Eastern Crisis and the Balance of Power, 1920–1941
    ch16.html                 The Challenge to Empire in the Middle East and Asia
    ch17.html                 Mussolini's War in Ethiopia
    ch18.html                 The Challenge in Europe, 1935–1941
    ch19.html                 Appeasement
    ch20.html                 Stalin and the West
    ch21.html                 The United States and the End of Isolation
    ch22.html                 The Grand Alliance, 1941–1945
    ch23.html                 A Bipolar World
    ch24.html                 A Third World?
    ch25.html                 Making the New Europe: European Integration since 1950
    ch26.html                 The Making of Modern Southeast Asia in the Age of Decolonization and the Cold War
    ch27.html                 The Middle East, 1945–1991: The Making of a Mare's Nest
    ch28.html                 The Sino-Soviet Alliance
    ch29.html                 The Collapse of the Soviet Union and the End of the Cold War
    ch30.html                 War and Peace in the Global Community, 1989–2001
    ch31.html                 Globalization
    ch32.html                 Terrorism: September 11, 2001 and its Consequences
  archive/legacy-chapters/
    ch00.html, ch01.html      superseded long versions, inactive
  chapter_catalog.json        definitive official chapter titles, 00–32
  CHAPTER_TITLES.md           readable 00–32 chapter directory and status
  build.py                    assemble ../book.html from split source
  CSS_DOC.md                  live CSS reference (update with CSS changes)
  JS_DOC.md                   live JS reference (update with JS changes)
  NEW_NOTES_WORKFLOW.md       editorial and per-chapter authoring contract
  MIGRATION_STATUS.md         current build state + verification
  tests/
    validate_structure.py    structural checks for active chapters
    smoke_active.py          active-chapter browser/print regression
    smoke_legacy.py          optional archived-fixture engine stress test
    smoke_ch08_ch09.py        chapter 08–09 source-coverage and browser checks
    smoke_ch10_ch11.py        chapter 10–11 source-coverage and browser checks
    smoke_ch12_ch13.py        chapter 12–13 source and print integration checks
    smoke_ch16_ch17.py        chapter 16–17 source and print integration checks
    smoke_ch18_ch19.py        chapter 18–19 source and print integration checks
    smoke_ch20_ch21.py        chapter 20–21 source and print integration checks
    smoke_ch22_ch23.py        append-safe chapter 22–23 source/export checks
    smoke_ch24_ch25.py        append-safe chapter 24–25 source/export checks
    smoke_ch28_ch29.py        append-safe chapters 28–29 test
    smoke_ch30_ch32.py        append-safe final-three source/export test
    smoke_sidebar_alignment.py  screen/print sidebar alignment and variety
```

## Build and validate

```bash
python3 src/tests/validate_structure.py
python3 src/build.py
python3 src/build.py --check
python3 src/tests/smoke_active.py
```

`book.html` is self-contained and can be opened in a Chromium-based browser.
For print or PDF, open the right-hand **Contents** drawer. The **Export** section
is above the table of contents. Enter ordered ranges such as `1,0,1` or leave
blank for all chapters. The **Include chapter summaries** checkbox controls
whether the contrasting chapter-revision sections are included. Save from the
browser's print dialog to PDF, with backgrounds enabled.

The 1280×720 layout uses 13.333×7.5-inch PDF geometry. No external JavaScript
pagination, export, or UI libraries are used. The engine creates pages in the
browser and uses Chromium's native print-to-PDF pathway.

## Complete edition, reproducibility and final PDF

All 33 planned chapters are now present. Rebuild with `python3 src/build.py`
and verify byte-identical output using `python3 src/build.py --check`.
Run the structural checks, the append-safe chapter fixtures, and
`python3 src/tests/smoke_sidebar_alignment.py` after any chapter-content edit.

For a reliable PDF export of the full 33-chapter book (requiring Playwright,
Chromium, BeautifulSoup and PyMuPDF), run:

```bash
python3 src/tools/export_full_pdf.py --chromium /usr/bin/chromium --batch-size 16
```

The exporter uses the unchanged `engine.js` pagination DOM, merges the batches,
and rebuilds working contents-to-page links. PDF links do not constitute a
native bookmarks outline. This release has a chapter-aware editorial and
historical verification report at `CH30_CH32_EDITORIAL_NOTES.md`.

## Editing or extending the complete book

1. Accept the **new, shorter chapter notes** as the content source; do not
   merge the old archival text or expand the concise notes into a long essay.
2. Create `chapters/chNN.html` with `.chapter-source`, `.src-hero`, `.src-main`,
   and `.src-side`. Author concepts in the sidebar, and mark the first block
   of each revision zone `data-revision-start="true"`.
3. Rebuild and run the tests above. Inspect representative screen and PDF pages
   visually, particularly tables, sidebars, and page boundaries.
4. **Only when shared styling or engine code changes:** update its matching
   `CSS_DOC.md` / `JS_DOC.md` in that same turn.
5. Keep the source ZIP as the latest portable recovery checkpoint for the next
   session, since the working sandbox may not persist.

## Current limitations

A clickable PDF contents page is generated, but no true native PDF outline tree.
Sidebars are section-aware in both screen and print, though some concise-note pages
have intentionally unused side-column space. Alignment is to the corresponding
section/page rather than to an exact paragraph baseline.

## Official chapter labels vs. notes titles

`chapter_catalog.json` records all 33 official textbook titles provided by the
user. Chapter H1 headings, the PDF chapter index and the collapsible HTML
contents always show those titles with two-digit chapter numbers. The shorter
notes' descriptive title belongs only in a secondary subtitle. Chapters 28–32
remain catalogue entries (not active/linked pages) until their notes are added.
The structural validator checks this convention.

## Educational sidebar V2 (Ch00–03 redesign)

The original six educational colour categories are retained, but the active chapters now use a variety of miniature, selectable-text visual components (comparisons, timelines, scholar profiles, memory triptychs, causal flows, statistics and exam/misconception contrasts). Each source side block declares a `data-for-section` key matched to its main `data-section-key` heading. The HTML reader pairs notes with their actual section; the 16:9 print engine places them on a page containing that section. See **`SIDEBAR_COMPONENTS.md`** for the full authoring contract, and run `tests/smoke_sidebar_alignment.py` after every engine or sidebar-content edit.

The substantial narrative in `.src-main` in all four active chapters was retained verbatim through this pass; only the sidebar and section metadata were redesigned. `CSS_DOC.md` and `JS_DOC.md` document every shared-code change.


## Chapter 04–05 checkpoint (2026-11-02)

Current short-notes edition: **00–05**. Add only `chapters/chNN.html` when incorporating future user-supplied concise chapters; the engine and shared CSS remain unchanged for this checkpoint. See `CH04_CH05_EDITORIAL_NOTES.md` for content decisions, source caveats, and the extra smoke test. Chapter titles are in `chapter_catalog.json`.

## Chapters 06–07 checkpoint (2026-11-02)

**Current active range: 00–07**. Chapters 06/07 use the existing Sidebar V2 component system; the shared CSS, JavaScript and shell and their two living documentation files remain unmodified. The Ch04/05 source-specific test has been generalized for future chapters. Run `python3 src/tests/smoke_ch06_ch07.py` to verify the 06/07 chapter source and print/HTML integration. See `CH06_CH07_EDITORIAL_NOTES.md`.

## Chapters 10–11 checkpoint (2026-11-02)

**Current active range: 00–11.** Chapters 10/11 use the established Sidebar V2 component grammar. Eleven and ten section-linked learning aids respectively complement the new source-driven chapter narratives. The active and archival browser checks remain passing; `tests/smoke_ch10_ch11.py` adds append-safe source checks. The prior 08/09 source test was made append-safe. No changes were made to production `styles.css`, `engine.js` or `shell.html`, so their existing living docs remain current. See `CH10_CH11_EDITORIAL_NOTES.md`.

## Chapters 12–13 checkpoint (2026-11-02)

**Current active range: 00–13.** Chapter 12 studies the punitive and institutional dimensions of Versailles; Chapter 13 follows the League of Nations' political limitations and financial/humanitarian legacy. Both use concise source-derived sections, semantic tables, source-anchored Sidebar V2 learning cards, and separate revision pages. Their source-specific validator is `tests/smoke_ch12_ch13.py`. The HTML/PDF engine, CSS and living docs are unmodified. See `CH12_CH13_EDITORIAL_NOTES.md` for authoring choices and source data caveats.

## Chapters 14–15 checkpoint (2026-11-03)

The active book now includes **00–15**. Chapter 14 studies the international financial crisis and Chapter 15 the Far Eastern crisis, using the existing Sidebar V2 design. The supplied notes' source-level dates/treaty ambiguities are documented in `CH14_CH15_EDITORIAL_NOTES.md`. A new append-safe source-specific test is `tests/smoke_ch14_ch15.py`; `tests/smoke_ch12_ch13.py` was made append-safe. Shared CSS, JavaScript and shell were not modified; their living docs remain in sync.

## Chapters 18–19 checkpoint (2026-11-03)

**Current active range: 00–19.** Chapter 18 examines the 1935–41 challenge to the Versailles settlement; Chapter 19 uses the author's supplied interpretation of British appeasement as a reciprocal settlement strategy. Both use official textbook H1 titles and concise notes titles as subtitles. Combined, they add 24 semantic table rows and 28 section-aware educational aids; both conclude on separate revision pages. Run `tests/smoke_ch18_ch19.py`. Shared production CSS/JS/shell and their living documentation remain byte-for-byte unchanged. See `CH18_CH19_EDITORIAL_NOTES.md` for source-level cautions and layout decisions.

## Chapters 20–21 checkpoint (2026-11-03)

**Current active range: 00–21.** Chapters 20 and 21 cover Stalin’s dual-track relationship with capitalist powers and Roosevelt’s incremental abandonment of American isolation. The two new sources preserve the supplied notes’ interpretations, tables and quotations; both have varied section-linked Sidebar V2 aids and separate revision zones. Full release: 163-page 16:9 PDF; 219 table rows; 250 sidebar aids; 22 revision sections. See `CH20_CH21_EDITORIAL_NOTES.md` for unresolved source-level verification flags and the paragraph/section keep-together authoring decision. Run `tests/smoke_ch20_ch21.py` plus the active/archival tests. Existing production engine/CSS/shell and their living documentation remain unchanged.


## Chapters 22–23 checkpoint (2026-11-03)

The active concise-notes reader now contains **Chapters 00–23**. New chapter modules: `chapters/ch22.html` (Grand Alliance) and `chapters/ch23.html` (bipolar Cold War). They retain the existing section-linked Sidebar V2 grammar and official catalogue titles; neither the shared stylesheet nor engine was changed. Editorial verification points and print-page reflow decisions are recorded in `CH22_CH23_EDITORIAL_NOTES.md`; new append-safe QA: `tests/smoke_ch22_ch23.py`. Rebuild using `python src/build.py` and verify with `--check`. The next intended chapter is **24 — A Third World?**

## Chapters 24–25 checkpoint (2026-11-03)

**Current active range: 00–25 (26 chapters).** Chapter 24 traces the Third World from Sauvy and Bandung through NAM, UNCTAD, the G77 and NIEO to post-Cold War fragmentation. Chapter 25 treats European integration as a flexible collective exercise of national sovereignty, from the Schuman Plan to enlargement and the euro. The standard six semantic card categories and section-aware placement are retained. See `CH24_CH25_EDITORIAL_NOTES.md` and `tests/smoke_ch24_ch25.py`. The **197-page** PDF was generated from the audited print DOM in render batches to avoid a browser painting stall; it retains clickable contents destinations. Shared CSS, JavaScript, shell/build, and their living engineering docs are untouched. **Next:** 26 — The Making of Modern Southeast Asia in the Age of Decolonization and the Cold War.

## Chapters 26–27 checkpoint (2026-11-03)

**Current active range: 00–27 (28 chapters).** Chapter 26 covers the making of modern Southeast Asia from wartime occupation through decolonization, Vietnam and ASEAN. Chapter 27 analyzes British retreat, American intervention, regional state agency and the Gulf crises to 1991. The official chapter titles and V2 purpose/presentation system are unchanged. **215-page true-16:9 PDF**, **289 table rows**, **344 sidebar items**, **28 revision sections**, **202 live PDF TOC links**. See `CH26_CH27_EDITORIAL_NOTES.md` for source caveats and the 11-batch PDF rendering procedure; test with `tests/smoke_ch26_ch27.py`. Shared CSS/JS/shell/build and both living documentation files are unmodified. **Next: Chapter 28 — The Sino-Soviet Alliance.**

### Reproducible batched PDF export

Once `python src/build.py` creates `book.html`, the source includes
`python src/tools/export_full_pdf.py --chromium /usr/bin/chromium` for
reproducible export of larger editions. It invokes the unchanged engine, then
prints the audited `#printView` DOM in small batches, merges into `book.pdf`,
reconstructs internal contents links, and writes `PDF_MERGE_QA.json`.
The script requires Python packages `playwright`, `beautifulsoup4` and
`pymupdf`, plus local Chromium. This is an *offline authoring utility*, not
an external runtime dependency of the self-contained `book.html`.

## Chapters 28–29 checkpoint (2026-11-03)

**Current active range: 00–29 (30 chapters).** Chapter 28 traces the fragile Sino-Soviet alliance and its breakdown by 1969; Chapter 29 analyzes Gorbachev's reform programme, the retreat from Eastern Europe and the dissolution of the USSR. Both use official catalogue titles, condensed authoring grounded only in the supplied notes, diverse section-aware Sidebar V2 aids and distinct revision zones. Full-book verified PDF: **234 true 16:9 pages**, **309 table rows**, **378 learning aids**, **30 revision sections**, **220 internal PDF links**. New QA: `tests/smoke_ch28_ch29.py` (append-safe) and `CH28_CH29_EDITORIAL_NOTES.md` (historical caveats and layout decisions). The original source modules 00–27 and shared CSS/JS/shell/build and living references are unchanged. For large-book PDF export use `python src/tools/export_full_pdf.py --batch-size 16`; this produces clickable internal links but not native PDF outline bookmarks. **Next:** Chapter 30 — War and Peace in the Global Community, 1989–2001.


## Social sharing metadata

The canonical title, description, Open Graph image URL, and Twitter Card tags live in `shell.html`, the same source as the published HTML head. Rebuild with `python src/build.py -o index.html` to retain them. The referenced `og-image.jpg` belongs in the repository root at `https://mohdujjain.github.io/world-history-dossier/og-image.jpg`. Do not put page-specific metadata only in the assembled `index.html`: a rebuild would remove it.
