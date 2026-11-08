# World History Dossier — Source-Fidelity Editorial Audit

**Date:** 8 November 2026  
**Review branch:** `audit/history-source-fidelity-20261108`  
**Primary source:** The owner-provided numbered Drive folder: https://drive.google.com/drive/folders/1C-izmqgS5K_ZLs5Souds6wU0jbe6k0KJ  
**Published corpus:** 33 chapters, 00–32  
**Scope of verifiable source comparisons:** Drive Briefings 04–32 (29 Google Docs). Matching briefings 00–03 were **not present in the supplied folder**; those chapters received only limited production-language repairs, not a verified substantive source audit.

## Governing editorial contract

The provided study briefings are the authority for this transformation. The dossier may reorganize and clarify their arguments but must not silently insert editorial skepticism, present-day qualifications, outside historical corrections, claims of independent fact checking, moral instructions or author's-argument downgrades. Preserve historical comparisons, disputes and qualifications *made by the sources themselves*, including arguments expressed strongly or in terms now contested. A genuine historical correction may be documented outside the reader but may not be slipped into the primary explanatory prose.

The six-category note system, chapter accents, print engine and reader UX are outside the scope of this correction.

## Procedure

1. Inspected all 33 chapter source modules, chapter overview text, timelines, data comparisons, revision sections and learning aid cards.
2. Mapped 29 corresponding Drive briefings for Chapters 04–32; searched these documents for historical positions and whether the dossier's warnings and source-verification language were actually present in the briefing.
3. Searched for `supplied`, `source check`, `the supplied notes`, `the briefing`, `the source`, claims of external verification, interpretive warnings and unnatural assistant commentary.
4. Reviewed each source-context match instead of globally removing cautionary words. Retained ordinary historical verbs such as “Stalin supplied weapons” and legitimate historiographical disagreements.
5. Applied exact, auditable text changes in modular `src/chapters/chNN.html` and rebuilt publication `index.html`. Recorded the original/replacement text and reasons in ten numbered JSON manifests under `src/audits/`.
6. Conducted second-pass grammar and duplication checks. Replaced broken sentences introduced by initial attribution cleanup instead of leaving a superficially sanitized reader.
7. Added source-fidelity regression checks for known insertions, preservation of substantive anchors, the generated index and the content-hashed offline edition.

## Change inventory

**245 exact documented corrections across 30 of 33 chapters.** Chapters 00, 04 and 07 did not need changes in the targeted searches; this does **not** certify them sentence-by-sentence.

| Chapter | Corresponding source status | Corrections |
| --- | --- | ---: |
| 00 | No matching Drive briefing | 0 |
| 01 | No matching Drive briefing | 3 |
| 02 | No matching Drive briefing | 4 |
| 03 | No matching Drive briefing | 1 |
| 04 | Briefing 04 | 0 |
| 05 | Briefing 05 | 4 |
| 06 | Briefing 06 | 3 |
| 07 | Briefing 07 | 0 |
| 08 | Briefing 08 | 1 |
| 09 | Briefing 09 | 4 |
| 10 | Briefing 10 | 5 |
| 11 | Briefing 11 | 3 |
| 12 | Briefing 12 | 8 |
| 13 | Briefing 13 | 13 |
| 14 | Briefing 14 | 11 |
| 15 | Briefing 15 | 12 |
| 16 | Briefing 16 | 12 |
| 17 | Briefing 17 | 7 |
| 18 | Briefing 18 | 9 |
| 19 | Briefing 19 | 4 |
| 20 | Briefing 20 | 7 |
| 21 | Briefing 21 | 9 |
| 22 | Briefing 22 | 1 |
| 23 | Briefing 23 | 13 |
| 24 | Briefing 24 | 9 |
| 25 | Briefing 25 | 8 |
| 26 | Briefing 26 | 19 |
| 27 | Briefing 27 | 23 |
| 28 | Briefing 28 | 6 |
| 29 | Briefing 29 | 15 |
| 30 | Briefing 30 | 3 |
| 31 | Briefing 31 | 15 |
| 32 | Briefing 32 | 13 |

## Representative findings and action

- **12 · Versailles System:** Replaced a red “DATE CHECK” card that directed students to verify 1936 dates against an outside text. The briefing's chronology was preserved rather than silently corrected.
- **13 · Legacy of the First World War:** Replaced the “SOURCE CHECK” warning about Åland and Vilna with content on the League’s arbitration. Retained the briefing's historical framing.
- **15 · Far Eastern Crisis:** Removed the instruction to check treaty attribution against outside treaty texts. The briefing's own Nazi–Soviet Pact date was retained, with the discrepancy treated as a separate source-authenticity concern, not repaired invisibly in the notes.
- **17 · Ethiopia:** Removed an unrequested verification warning about chemical weapons; retained the historical discussion of Italy’s conduct and the League crisis.
- **21 · End of US Isolation:** Removed an external-verification instruction about Atlantic patrol geography; preserved the briefing's patrol account.
- **23 · Bipolar World:** Removed an added “not independently verified” qualifier after the approximate nuclear-arms figure; retained the source's scale and Cold War interpretation.
- **27 · Middle East:** Rewrote production-context attribution, repaired the discussion of the Iran–Iraq War and Shiite/Kurdish uprisings, preserving criticism and political interpretations *present in the source*.
- **29 · USSR collapse:** Removed extraneous textbook-verification instructions on dates and budget estimates; preserved the argument about Gorbachev's reforms and dissolution.
- **30 · War and Peace:** Removed the separate “EVIDENCE CHECK” card about Somalia and Rwanda; retained the source's contrast in humanitarian intervention.
- **31 · Globalization:** Preserved the author's forward-looking analysis as a projection without an unsolicited warning telling the reader not to accept it as established history.
- **32 · September 11:** Removed publication fact-check directives and a repeated explanatory sentence. Retained distinctions between terrorism, guerrilla war, international law and post-9/11 policy.
- **Across the book:** Converted “the supplied notes,” “in the supplied account,” and other input-generation commentary into historical exposition or attributed analysis. Six factual past-tense uses of “supplied” remain.

## Important retention decisions

A historical source can genuinely distinguish myth from evidence, describe competing scholarly positions, discuss propaganda or make a tentative projection. Such source-authored distinctions belong in the dossier. The remedy was **not** a blanket deletion of terms such as “mistake,” “caution,” “history,” “claim,” “supply,” or “source.” Examples preserved include the historiography of appeasement, Soviet military intentions in 1941, the nationalist politics of communist anticolonial movements and disputes over League effectiveness.

## Build/QA and publication safety

- Canonical source remains **the modular chapter files**, not a one-off patch to `index.html`.
- `src/build.py -o index.html --check` must reproduce the reader exactly. A content-hashed service worker must be refreshed from the corrected publication to prevent offline clients from holding an old edition.
- `src/tests/test_source_fidelity.py` checks all 33 modules, the ten correction logs, substantive retained markers, forbidden source-verification insertions and publication/offline hash parity.
- The draft PR preserves `main`; no site deployment occurs until review/merge.
- The repository's separately committed **full-book bookmarked PDF must be regenerated from the corrected HTML before publishing a new complete PDF**. This branch's source/reader changes do not constitute an updated PDF release.

## Limits

This was a substantive, source-document-based editorial-interference review of the dossier, not a complete word-for-word equivalence proof for every paragraph. Because the explicitly provided folder lacks source briefings for Chapters 00–03, those four chapters cannot be claimed as independently source-verified. The 29 source documents are themselves study briefings, not necessarily the original textbook; no outside historical fact-check was introduced. Findings and exact substitutions are traceable in the manifests.
