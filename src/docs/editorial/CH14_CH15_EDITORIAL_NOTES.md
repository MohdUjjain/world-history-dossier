# Chapters 14–15 editorial and engineering handover

## Input and source policy

Chapters were composed solely from the user's concise pasted notes in the 2026-11-03 conversation. No original textbooks or external research were used. The official titles come from `chapter_catalog.json`; the notes' more descriptive formulations appear only as subtitles. The narrative is reorganized without introducing outside historical events, and the study sidebars are derived from the supplied material. No claims have been independently verified.

## Chapter 14 — Why International Finance Mattered: 1919–1939

- Four substantive sections + contrasting chapter conclusion, 12 main table rows, 11 section-anchored Sidebar V2 aids.
- Central logic: British gold and financial appeasement → conflicting American internationalist/isolationist policies → French defensive credit politics → breakdown of payments, trade and diplomatic solidarity.
- Comparison table: Wall Street and Washington (four rows). Timeline table: 1928–1932 crisis stages (five rows). Revision: three-fold conceptual comparison of liberal internationalism, gold and Allied solidarity.
- Sidebar formats include gold-standard flow, gold-exchange definition, comparison of national priorities, loan-dependency memory steps, reserve dispute statistic, depression timeline; source-check caveats remain documented here and in the main chronology.
- **Editorial flags (do not silently correct):** (a) user notes say Smoot–Hawley was 'signed' in March 1930; date needs checking; (b) notes describe Bank of France as 'bankrupt' following sterling devaluation; precision/severity needs verification; (c) strong interpretive claims about the London Conference and the reparations commission's American veto should be checked against the scholar's source.

## Chapter 15 — The Far Eastern Crisis and the Balance of Power, 1920–1941

- Six substantive sections + contrasting chapter conclusion; one Washington-system comparison with three rows; 15 section-anchored Sidebar V2 aids.
- Sequence: Washington treaty order → erosion by Chinese nationalism, Soviet action and Kwantung Army autonomy → Mukden/Manchukuo and League rupture → naval and Chinese wars → European strategic opportunity → embargo and southern war gamble.
- Sidebar formats include treaty restriction caution, 5:5:3 stat, Chinese/Kwantung/Soviet flow, Manchuria timeline, strategic North/South comparison, sanctions decision trap, Stimson term, 1941/1931 chronological memory aids.
- **Editorial flags (do not silently correct):** (a) Four-Power Treaty assigned base fortification restrictions (requires treaty attribution check); (b) user notes give the Nazi–Soviet Pact as 'August 1933', potentially a date typo (the chapter avoids reproducing this year as a fact); (c) anti-Comintern chronology is compressed in the source and should be checked; (d) placement of ABDA in 1940–41 requires confirmation of formal creation versus preliminary cooperation; (e) the exact scope of metal/oil embargo timings needs source verification.

## Technical checkpoint

- Source modules added: `chapters/ch14.html`, `chapters/ch15.html`.
- Main and revision `data-section-key` metadata matches the `.src-side` `data-for-section` keys; each revision zone begins with `data-revision-start=true` in both streams.
- Source-specific regression: `tests/smoke_ch14_ch15.py`.
- Existing `tests/smoke_ch12_ch13.py` revised to count revision pages dynamically, not assume exactly fourteen forever. No production CSS/JS/shell changes; `CSS_DOC.md` and `JS_DOC.md` remain authoritative without edits.
- New checkpoint to retain for next session: `World_History_Dossier_Ch00-15_Source.zip` (contains all active chapter sources and the build/test/docs system).

## Final layout refinement

The first Chapter 14 PDF produced a sidebar-only page at the boundary before the mandatory revision page. The disputed-date caution was retained in the editorial handover and the 1930 timeline row rather than occupying a standalone sidebar card; the repeated explanation of the customs-union and sterling-crisis chronology was consolidated into the main semantic table. This removes the orphaned page while preserving the source claims. Final Chapter 14 has 11 sidebar aids, and the final dossier has 120 pages.
