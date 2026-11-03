# Chapters 26–27 — Editorial and Print Integration Notes

Checkpoint: 2026-11-03 · Official textbook titles · Educational Sidebar V2

## Sources, emphasis, and boundaries

The user supplied two self-contained concise historical briefs, not the underlying textbook chapters. These chapter modules condense and reorganize **only those supplied briefs**; they are not independently fact-checked, bibliographically verified, or supplemented from outside materials. No named authors were supplied for Chapters 26–27, so the source `data-author` and hero byline remain blank. The official titles come from `chapter_catalog.json`; the expressive brief titles are retained as study-notes subtitles.

### Chapter 26 — The Making of Modern Southeast Asia in the Age of Decolonization and the Cold War

- **Seven main sections**, a separate revision section; **9 semantic table rows**, **17 section-linked educational cards** across six visual-purpose types.
- Narrative arc: regional imperial map in 1939 → Japanese victories and nationalism → British/Dutch paths to independence → Indochina/PRC/US involvement → SEATO and domino theory → Colombo/Bandung/ASEAN → Vietnam wars, China–Vietnam confrontation and regional economic adaptation.
- Explicitly preserves the distinction between indigenous communist nationalism and proxy-war superpower involvement. Side cards include Ho versus Sukarno, 1945–49 decolonization, Vietnam conflict flow, three-way region-building and the SEATO/ASEAN distinction.
- The source's initial territory table also lists **India, Sri Lanka, Hong Kong and Japan** alongside Southeast Asian colonies and powers. This is an expansive geopolitical overview, not a geographically rigorous list of only Southeast Asian states. The final document labels it as the source's regional comparison rather than pretending all listed places are in Southeast Asia.
- The source calls the post-1975 Sino-Vietnamese confrontation a **“Third Vietnam War”**, an interpretive label not presented here as universal terminology. Vietnam's later *doi moi* reforms are mentioned without an unsupported start year. War chronology and claims should be checked against the cited textbook for examination use.

### Chapter 27 — The Middle East, 1945–1991: The Making of a Mare's Nest

- **Six main sections**, a separate revision section; **8 semantic table rows**, **17 section-linked educational cards**.
- Narrative arc: British postwar decline/Suez → Eisenhower Doctrine and interventions → Nixon Doctrine and Gulf partners → Carter Doctrine, Iran–Iraq War and secret arms dealings → Kuwait → conceptual critique of the “superpower straightjacket.”
- The chapter explicitly **separates Iran and Saudi Arabia as Gulf security partners from Israel's wider military role**, rather than treating all three as a single undifferentiated “twin pillar.”
- The supplied text attributes a **very large Aden population fall (220,000 → 80,000 within 18 months)** and specific violence/displacement details to the 1967 British withdrawal. These figures are **not independently verified** and should not be treated as settled without checking the textbook; the chapter mentions the claim with an explicit source verification caution rather than repeating unverified numbers as fact.
- The source dates restoration of US–Iraq diplomatic relations to **1986**. The chapter instead describes the broader mid-1980s shift without endorsing that specific date; verify the original date and the chronology of arms and naval escort policies before relying on it.
- The source's claims about US attitudes to Shiite and Kurdish uprisings in 1991 and about imperial-policy motives are interpretations; they are retained in source-grounded terms, not asserted as independently confirmed facts.

## Structural/layout rules and QA

1. Use `data-title` and H1 **exactly** as in `chapter_catalog.json` and put expressive subtitle in `data-subtitle`/`.hs`.
2. Only `.src-side > .block` elements carry the 17 learning aids, with matching `data-for-section` keys in `.src-main`.
3. Use the existing six purposes (`def`, `concept`, `tip`, `mistake`, `memory`, `hy`) and appropriate independently chosen displays (`text`, `comparison`, `triptych`, `timeline`, `stat`, `flow`). No new CSS or JS was necessary.
4. Place **exactly one** `data-revision-start="true"` in the first revision main block and the **first** revision side block of each chapter. Chapter 27’s final exam-thesis card was moved into the revision sidebar to eliminate an almost-empty print page.
5. Test `python src/build.py --check`, `python src/tests/validate_structure.py`, `python src/tests/smoke_ch26_ch27.py`, `python src/tests/smoke_sidebar_alignment.py`, and the archived-engine smoke test. The isolated fixture confirms custom range `27,26,27`, revision toggling, true 16:9 geometry and mobile width 390px.
6. For full 28-chapter PDF generation, the custom JS engine generated the full **215-page** print DOM. The print DOM was saved as a static HTML snapshot, rendered in **11 batches** of up to 20 pages, then merged into a searchable PDF. **202 internal PDF links** were reconstructed using the real DOM link coordinates, preserving navigation. This avoids the full-document Chromium PDF printing slowdown without changing the production HTML engine.
7. Existing Chapters 00–25, `styles.css`, `engine.js`, `shell.html`, `build.py`, `CSS_DOC.md` and `JS_DOC.md` remain identical to the previous checkpoint; no shared-code changes mean the two engineering references require no revision.

**Next official chapter:** 28 — The Sino-Soviet Alliance.

For future PDF rebuilding, a parameterized version of the batched renderer is
provided as `src/tools/export_full_pdf.py`; it uses the same audited DOM and
clickable-link reconstruction method. The two Kuwait review cards in Chapter 27
are anchored to the *following synthesis section* (rather than the immediately
preceding Kuwait section) so their retrospective argument and placement agree
in both HTML and PDF; this eliminated the two old section-mismatch findings.
