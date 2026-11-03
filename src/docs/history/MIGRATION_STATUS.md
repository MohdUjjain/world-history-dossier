# World History Dossier — Active Edition Status

Date: 2026-11-02

## Live contents

The book currently contains fourteen replacement chapters (00–13). Original historical checkpoints below are retained for continuity; the most recent checkpoint is appended at the end.

Initial four replacement chapters:

- **00 — Introduction: Twentieth-Century International History - The Changing Face of Empire** (Gordon Martel)
- **01 — Imperialism** (John MacKenzie)
- **02 — Nationalism** (R. J. B. Bosworth): **two newly supplied Nationalism texts merged** into one coherent chapter. Complementary distinctions, citations, examples, theorists, Jewish case study, national rituals, and modern religious-national fusions retained; repeated explanation consolidated. Neither original long archived chapter nor outside research was used.
- **03 — Internationalism**: based exclusively on the newly pasted text. Malformed pasted tables restored as semantic HTML tables; no chapter author inferred.

Official chapter titles remain the only H1 and chapter-level index labels. The notes' expressive titles are subtitles. All chapters contain a distinct revision zone controlled by the existing export checkbox; the revision begins on a new PDF page. Educational concept cards are stored in sidebar source streams.

## Technical verification

- Modular source files: `src/chapters/ch00.html`–`ch03.html` + unchanged `styles.css`, `engine.js` and `shell.html`.
- Build and build-check pass, structural validator: 4 chapters, 0 errors, 0 warnings.
- Browser tests: 4 chapter headings, 33 sidebar concept cards, zero main-column concepts, 47 original and printed table rows, 4 revision zones, no observed print column overflow.
- Full 16:9 export: **35 PDF pages**, **29 PDF links**, searchable text. The PDF contains no native outline/bookmark panel (existing engine limitation).
- Revision inclusion checkbox works; custom reordering with repeated chapters works; 390px mobile viewport has no horizontal document overflow.
- An orphaned final quotation in Chapter 03 was relocated to its revision sidebar, removing an otherwise nearly blank last PDF page.
- `tests/smoke_active.py` is now chapter-count-agnostic and will continue to work as chapters are appended.

## Authoring and maintenance

- Preserve the supplied concise notes as the content authority. Chapter 02's two sources were **deduplicated, not concatenated**.
- Archived legacy long chapters remain inactive in `archive/legacy-chapters/`.
- `chapter_catalog.json` is the definitive official 00–32 title list.
- **No CSS or JS production code changed** for Chapters 02–03; existing layout conventions and their docs remain valid. The README, title catalogue, migration status and active browser regression were updated.

## Next

Chapter 04 — A Shrinking World. Add `chapters/ch04.html`, rebuild, run structural and browser tests, and visually inspect PDF page breaks.

## 2026-11-02 sidebar learning-layer overhaul

Four current chapters (00–03) retain their exact main narrative text. All 39 sidebar aids have been newly authored from the existing chapter material, classified by purpose and rendered with ten visual forms, instead of the previous 33 predominantly green concept summaries. Print and screen sidebar placement is section-aware. Source remains four active chapters, with official 00–32 title catalogue unchanged. All structure, current-book, archived-legacy, and dedicated sidebar-alignment regressions pass. See `SIDEBAR_COMPONENTS.md` and `SIDEBAR_QA.json` in the exported ZIP root.


## 2026-11-02 Chapters 04–05 added using Sidebar V2

- **04 — A Shrinking World:** newly supplied concise notes processed into source-faithful narratives, two semantic tables and ten section-aware, varied educational aids. Concluding technology milestone table and closing lessons share one revision page.
- **05 — A Changing Diplomatic World:** new supplied concise notes converted to structured historical analysis, a foreign-services staffing comparison and ten varied aids. Ambiguous later German staffing date left explicitly unverified.
- Six active chapters: 00–05. No older chapter content or shared production CSS/JS changed.
- Full current HTML/PDF regression and archived-engine regression completed; new-specific content checks captured in `tests/smoke_ch04_ch05.py`.
- The two living references `CSS_DOC.md` and `JS_DOC.md` remain current because neither underlying production file was changed this turn.

## 2026-11-02 Chapters 06–07 checkpoint

- **06 — The Triple Alliance:** new concise user-supplied notes. Four main sections plus distinct revision section; three semantic main-text tables (10 total rows); ten sidebar aids across six educational purposes. Specific emphases: Bismarck's defensive system, Russia and Italy, New Course, lack of military coordination, and Italian neutrality/defection.
- **07 — The Ententes, 1894–1914:** new concise user-supplied notes. Six main sections and revision; three semantic main-text tables (11 rows); eleven sidebar aids including the final source quotation in the revision sidebar. Connections between colonial agreements and contingent 1914 wartime alliance are preserved.
- **Eight active chapters 00–07**, 64-page 16:9 print PDF; 78 main-text table rows; 80 section-aware sidebar aids and 8 revision zones. No print overflow or sidebar misplacement detected in browser regression.
- All six existing chapters (00–05) and shared engine/CSS/shell and their living docs remain **byte-identical** to the previous source ZIP. `smoke_ch04_ch05.py` now tests its two titles without assuming they are the latest chapter files. New source-sentinel and layout test: `tests/smoke_ch06_ch07.py`.
- Historical statements and quotations were taken only from supplied notes; no outside historical verification has been performed.
- **Next:** 08 — The July Crisis.

## 2026-11-02 Chapters 08–09 checkpoint

- **08 — The July Crisis:** Five main sections and one revision section; two main tables (15 rows) and ten varied Sidebar V2 aids. Accidental extra content page removed by integrating the interpretive closing point into the revision conclusion.
- **09 — Wartime Promises and Postwar Europe:** Six main sections and one revision; three main tables (11 rows) and eleven varied aids. Source quotation occupies the revision sidebar.
- **Ten active chapters 00–09** and **78-page 16:9 print PDF**. Full book: **104 table rows**, **101 sidebar aids**, **10 revision sections**. Successful structural validation, active browser/regression, section alignment, source-sentinel tests, archived-engine regression and custom-order/revision-toggle validation.
- Previous eight chapters and shared shell/CSS/JS and living docs remain byte-identical to the preceding source checkpoint. `smoke_ch06_ch07.py` was made append-safe; new `smoke_ch08_ch09.py` checks both new chapters. No new historical research or external correction was performed.
- **Next:** 10 — Wartime Promises and the Postwar Empires.

## 2026-11-02 Chapters 10–11 checkpoint

- **10 — Wartime Promises and the Postwar Empires:** Four main sections and one contrasting revision section, two regional/military themes and the mandate scheme; three semantic tables containing 10 rows. Eleven varied sidebar aids include the conflicting-promise chronology, Africa figures, askari/vilayet terminology, Japanese Pacific comparison and a mandate-class quick reference.
- **11 — Envisioning a New World Order:** Four main sections and a separate revision section, three comparison tables containing 12 rows. Ten sidebar aids cover Wilsonian liberalism, Lenin's causal theory, two meanings of self-determination, institutional differences, and why both projects stalled.
- **Twelve active chapters 00–11**. Full-book export: **92 true-16:9 PDF pages**, **126 table rows**, **122 section-aware sidebar learning aids**, **12 chapter revision sections**. The full-browser regression reports zero print column or hero overflows and zero JS errors. The print source has selectable/searchable text and clickable index links.
- Existing chapter files 00–09, shell, production CSS/JS, CSS_DOC.md and JS_DOC.md remain unchanged from the Ch00–09 source checkpoint. Only an older append-unsafe test was repaired (08/09 hero check), and a new Ch10/11 test was added.
- Historical claims, numerical estimates, and interpretations are drawn from the user-provided concise notes; no independent fact-check or external augmentation has been performed.
- **Next:** Chapter 12 — The Versailles System.

## 2026-11-02 Chapters 12–13 checkpoint

- **12 — The Versailles System:** Seven substantive sections and a separate revision section. Three semantic tables with 13 total rows cover reparations, military restrictions and the chronology of treaty violations; the latter was moved onto the dedicated revision page to avoid a nearly empty standalone continuation page. Eleven section-aware learning aids include policy contrasts, an economic sequence, legal articles, armament limits, Locarno and a source-date caution.
- **13 — The Legacy of the First World War:** The supplied League-of-Nations text is retained with its descriptive notes title as subtitle, but the official textbook title governs the hero and index. Four substantive sections and revision, two semantic tables with nine rows, and twelve varied section-linked learning aids. Subjects include the Covenant, Anglo-French power, mandates, reconstruction loans, refugees, minorities and selected arbitration cases.
- **Fourteen active chapters 00–13**. PDF: **106 true-16:9 pages**, with **148 total table rows**, **145 total section-aligned sidebar aids** and 14 revision sections. Full-browser, previous-chapter, sidebar alignment, archived-engine and 12/13 source-specific tests pass; no print column overflow or JavaScript errors detected.
- Existing chapter files 00–11 and production CSS/JS/shell, including CSS_DOC.md and JS_DOC.md, remain unchanged. Source text was editorially condensed and organized from the user's supplied brief without outside historical research. Possible source-level inaccuracies (e.g. selected 1935/36 dates and Åland/Vilna claims) are flagged as unverified rather than silently rewritten.
- **Next:** 14 — Why International Finance Mattered: 1919–1939.

## 2026-11-03 Chapters 14–15 checkpoint

- Chapter 14 examines British gold policy, the Wall Street–Washington rift, defensive French financial action and the 1929–33 international collapse; Chapter 15 follows the Washington Treaty System, Manchuria, conflict in China and the Pacific descent to 1941.
- **Sixteen active chapters 00–15**, 120 true-16:9 PDF pages, **163 preserved table rows**, **171 section-aware learning aids**, **16 revision sections**. Full active-browser and sidebar alignment regressions report no print overflow or JavaScript errors, and correct mobile geometry.
- Two new independent HTML sources plus `tests/smoke_ch14_ch15.py`, `CH14_CH15_EDITORIAL_NOTES.md`. Existing source modules 00–13, production CSS/JS/shell and their living docs unchanged. `smoke_ch12_ch13.py` now uses a dynamic revision-page count to stay append-safe.
- Source caveats are documented and signalled within the notes rather than silently resolved. See the new editorial notes for key dates and treaty attributions requiring textbook checking.
- **Next:** 16 — The Challenge to Empire in the Middle East and Asia.

## 2026-11-03 Chapters 16–17 checkpoint

- **16 — The Challenge to Empire in the Middle East and Asia:** five main sections and separate revision; five semantic table rows and thirteen varied sidebar aids; subaltern critiques of elite nationalist histories, Gandhi, Egypt, Turkey, Iraq/Syria and Indochina. One close-related Indochina explanation block consolidated to prevent an orphaned print page.
- **17 — Mussolini's War in Ethiopia:** four sections and revision; nine semantic table rows and twelve sidebar aids; Ethiopian independence, Fascist mobilization, League sanctions and diplomacy, violence against civilians and the move toward alignment with Hitler.
- **18 active chapters (00–17)**; final book PDF **134 pages, true 16:9**, **177 preserved table rows**, **196 sidebar aids** (including non-learning-card quotes), and 18 separate revision zones.
- Source components 00–15 and the production CSS, JS, shell, build system, CSS_DOC.md and JS_DOC.md are unchanged. New chapter-specific regression: `tests/smoke_ch16_ch17.py`. Editorial ambiguities and technical decisions: `CH16_CH17_EDITORIAL_NOTES.md`.
- **Next:** 18 — The Challenge in Europe, 1935–1941.

## 2026-11-03 Chapters 18–19 checkpoint

- Chapter **18 — The Challenge in Europe, 1935–1941:** five sections plus a revision section, 15 table rows, 13 varied, anchored learning aids; differences between limited treaty revision and unlimited ideological expansion, the Italian/Soviet dimensions, French/British vulnerabilities and 1935–41 escalation. One isolated closing paragraph was moved into the revision conclusion to avoid a near-empty page, with its argument retained.
- Chapter **19 — Appeasement:** six sections plus revision, nine table rows and 15 educational aids; the 1931 proposal for a general settlement, Simon's cautious engagement, the economic “fourth arm”, bargaining through colonial claims, Chamberlain's three-theatre problem, Munich and the break of 1939.
- **20 active chapters (00–19)**; rebuilt **148-page** 16:9 PDF; **201 table rows**, **224 section-linked side aids**, **20 distinct chapter revision zones**. Active browser regression, section-aware/sidebar checks, older archived test and dedicated source test pass; no print column overflow or JavaScript errors.
- Existing chapter modules 00–17 and `styles.css`, `engine.js`, `shell.html`, `build.py`, `CSS_DOC.md`, `JS_DOC.md` remain byte-identical to the preceding source package. `tests/smoke_ch18_ch19.py` is append-safe. Source caveats recorded separately; no external historical fact-check performed.
- **Next:** Chapter 20 — Stalin and the West.

## 2026-11-03 Chapters 20–21 checkpoint

- **20 — Stalin and the West:** Six main sections and a distinct revision; 8 table rows, 12 side aids. The account connects the Arcos crisis, NEP, industrialization and trade, Popular Front and collective security, Munich, the 1939 pact and the contested Icebreaker hypothesis to Barbarossa. The Munich heading and its first substantive paragraph share a single atomic block to prevent an isolated section heading in print.
- **21 — The United States and the End of Isolation:** Six main sections plus revision; 10 table rows and 14 side aids including a revision quotation. Cash-and-carry, conscription, destroyers-for-bases, Lend-Lease, Atlantic patrols, Pacific sanctions and failed US–Japanese negotiations are kept distinct in the source and learning aids.
- **22 active chapters (00–21)**; **163-page 16:9 PDF**; **219 full-book table rows**, **250 section-aware sidebar items**, **22 revision zones**. Structural validation, active browser export tests, section-aware alignment, the older 18–19 source test, 20–21 coverage and archived-engine regression pass. No detected print overflow or JavaScript errors, and the mobile reader remains within 390px.
- All prior chapter files `00–19` plus production CSS, JS, shell, build, CSS_DOC.md and JS_DOC.md are unchanged from the preceding source ZIP. Only three test scripts are repaired for scalability or to avoid native print dialogs; one new source-specific test is added. Historical claims have not been independently verified. Editorial cautions: `CH20_CH21_EDITORIAL_NOTES.md`.
- **Next:** Chapter 22 — The Grand Alliance, 1941–1945.


## Chapters 22–23 checkpoint (2026-11-03)

**Current active range: 00–23 (24 chapters)**. Chapter 22 covers the wartime coalition’s Germany-First strategy, Second Front dispute, Teheran, Poland, the percentages agreement and Yalta. Chapter 23 covers the two rival blocs, containment, nuclear brinkmanship, détente and the Soviet collapse. Both use source-grounded Sidebar V2 components, official textbook H1 labels and dedicated revision spreads. See `CH22_CH23_EDITORIAL_NOTES.md` and `tests/smoke_ch22_ch23.py` for editorial decisions and append-safe checks. Shared CSS/JS/shell/build and their living documentation remain unchanged. **Next:** Chapter 24 — A Third World?

## 2026-11-03 Chapters 24–25 checkpoint

- **24 — A Third World?:** Six substantive sections, one distinct revision, 17 source-grounded table rows, 15 varied section-linked side aids. Sauvy, Bandung, the five leaders, NAM, UNCTAD/G77, NIEO and post-Cold War decline are distinguished as political and economic phases.
- **25 — Making the New Europe: European Integration since 1950:** Six sections and revision, 18 table rows, 16 side aids. The notes emphasize national interests and jointly exercised sovereignty, early forums versus ECSC, Rome, competing interpretations, Commission/Council power and deepening/widening.
- **26 active chapters 00–25**. **197 true-16:9 PDF pages**, **272 preserved table rows**, **310 section-aware sidebar aids**, and **26 revision zones**. Full print DOM reports zero side-note misplacements, print overflows, hero overflows and JavaScript errors. The PDF is searchable and has **185 functioning internal destination links** (not native outline bookmarks).
- An isolated `smoke_ch24_ch25.py` fixture tests both chapter sources, live sidebar, repeated custom export order, revision toggle and mobile width. `smoke_ch22_ch23.py` is repaired to be append-safe (test only). All earlier chapter source modules and six shared production/engineering-reference files are byte-identical to the preceding source release.
- A single huge Chromium PDF print stalled, so a verified static print snapshot was rendered in sequential small batches and merged. Internal TOC links were reconstructed from the rendered DOM's actual coordinates and page identifiers. The user-facing full HTML book still has the unchanged native export machinery. See `CH24_CH25_EDITORIAL_NOTES.md`.
- **Next:** Chapter 26 — The Making of Modern Southeast Asia in the Age of Decolonization and the Cold War.

## 2026-11-03 Chapters 26–27 checkpoint

- **26 — The Making of Modern Southeast Asia in the Age of Decolonization and the Cold War:** Seven sections, separate revision, nine table rows and seventeen varied section-linked aids. From Japanese occupation and diverse decolonizations to Vietnam, SEATO, ASEAN and regional interdependence. Preserves the author's emphasis on local nationalist agency rather than passive proxy status.
- **27 — The Middle East, 1945–1991: The Making of a Mare's Nest:** Six sections, separate revision, eight table rows and seventeen varied section-linked aids. Traces British retreat, Suez, American regional doctrines, Gulf conflicts and Kuwait; stresses local state agency within superpower competition. A concluding exam aid was moved into the revision sidebar to remove a single-card continuation page.
- **28 active chapters (00–27)**, **215 true 16:9 PDF pages**, **289 table body rows**, **344 section-aware side items** (including quotation items), **28 revision zones**, and **202 clickable internal PDF destination links**. No print column overflow or JavaScript errors in the full-book audit.
- Official headings match `chapter_catalog.json`; source files 00–25 and shared publishing engine, shell, build and `CSS_DOC.md`/`JS_DOC.md` are unchanged. New append-safe fixture `tests/smoke_ch26_ch27.py`; commentary and source-level verification cautions are in `CH26_CH27_EDITORIAL_NOTES.md`.
- PDF printed from the identical audited full-book DOM in 11 batches to avoid a Chromium full-job slowdown; the user-facing HTML retains its unchanged dynamic export machinery. No true native PDF outline bookmarks are claimed.
- **Next:** Chapter 28 — The Sino-Soviet Alliance.

## 2026-11-03 Chapters 28–29 checkpoint

- **28 — The Sino-Soviet Alliance:** Seven sections and separate revision; 9 main table rows; 16 learning aids. Follows the inherited 1945 settlement, 1950 alliance, Korean War, Khrushchev's early aid, 1956 ideological break, 1958–59 sovereignty/nuclear disputes and 1969 armed confrontation. Distinguishes the stated communist ideal from the Moscow-centered hierarchy Beijing resisted.
- **29 — The Collapse of the Soviet Union and the End of the Cold War:** Seven sections and separate revision; 11 main table rows; 18 learning aids. Traces Gorbachev, early economic and patronage reforms, Chernobyl, Yeltsin, foreign-policy realignment, Eastern Europe, nationalities and the 1991 coup/dissolution.
- **30 active chapters 00–29**; **234 true 16:9 PDF pages**, **309 table rows**, **378 section-aware sidebar aids**, **30 revision sections**, and **220 clickable internal PDF links**. Full print audit finds no side-note mismatch, overflow or JS error. Focused new-chapter custom/repeated ordering, toggles and mobile checks pass.
- Previous 28 source chapter files and all six shared production/engineering files unchanged. New `tests/smoke_ch28_ch29.py` and editorial caveats in `CH28_CH29_EDITORIAL_NOTES.md`. PDF exported using the existing `src/tools/export_full_pdf.py`, with no CSS/engine modification and no native PDF outline claims.
- **Next:** Chapter 30 — War and Peace in the Global Community, 1989–2001.

## Final planned chapters 30–32 completed (3 November 2026)

- **30 — War and Peace in the Global Community, 1989–2001:** Six main sections, separate revision, 12 main table rows, 15 section-linked learning aids. Wilsonian triad, 1990s globalization, Kuwait, Clinton, Rwanda/Somalia/Haiti, NATO, and the Balkan conflicts.
- **31 — Globalization:** Six main sections and revision, 15 main table rows, 15 learning aids. Four engines, first wave (1850–1914), interwar disruption, postwar institutions, late-century acceleration, debate and fragility.
- **32 — Terrorism: September 11, 2001 and its Consequences:** Six main sections and revision, 12 main table rows, 15 learning aids. Definitions, historical evolution, al-Qaeda, 9/11, self-defense, preemption versus prevention, Iraq and legal consequences.
- **Complete active catalogue: 00–32, 33 chapters.** All chapter heroes match `chapter_catalog.json`; archival chapter files remain inactive. `tests/smoke_ch30_ch32.py` validates the final three in isolation, repeated export ordering, revision inclusion, and mobile layout. The full assembled book also passes `tests/smoke_sidebar_alignment.py` with no misplaced learning aids or print overflows. For final page/link counts see `PDF_MERGE_QA.json` and `RELEASE_NOTES.md` in the release root.
- Source fidelity and historical verification cautions are recorded in `CH30_CH32_EDITORIAL_NOTES.md`. Earlier 30 chapter HTML files and the six shared publishing/engineering files remain unchanged. **The 00–32 source architecture is now complete.**
