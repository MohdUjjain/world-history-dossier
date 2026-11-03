# Chapters 22–23 — editorial integration and source cautions

Release checkpoint: 3 November 2026. The two new modules use the **user-supplied concise chapter briefs** only; the official textbook H1 titles are obtained from `chapter_catalog.json`. This is a study-note transformation, **not** an independently verified historical edition.

## Chapter 22 — The Grand Alliance, 1941–1945

- Source subtitle: *Personal Diplomacy and the Architecture of Victory (1941–1945)*.
- Five narrative sections plus an explicitly separate revision section. The final source heading “Summary of Findings” is integrated into the revision spread; its substantive material—Casablanca, the European Advisory Commission, and contrasting Anglo-American/Soviet-Western relationships—is preserved in prose and a concise two-column sidebar comparison. This avoids a sparse print continuation page.
- Main-body tables: **3×4** matrix of Big Three interests and **3×2** table of the Churchill–Stalin Balkan percentages (six substantive data rows). The Grand Alliance relationship contrast is also rendered as a miniature revision comparison card.
- Fourteen section-linked educational sidebar blocks include definitions, triptych, founding commitments timeline, Second Front military/political comparison, TORCH→OVERLORD sequence, Teheran milestones, Four Policemen, Polish sovereignty misconception, percentage memorandum, Yalta causal chain, EAC definition, revision steps; Churchill’s Charter quotation remains in the opening narrative.
- Source-level checks before examination use: dates and interpretation of the planned May 1944 OVERLORD operation; whether Churchill’s quoted Stalin axiom is verbatim or a retrospective attribution; percentages as informal understanding rather than a binding treaty; the EAC occupation-zone time span and Churchill’s “not a law, but a star” attribution. Maintain the distinction between wartime military coordination and postwar political consent.

## Chapter 23 — A Bipolar World

- Source subtitle: *The Architecture of Global Tension (1944–1991)*.
- Six narrative sections plus a dedicated revision section. The full five-row Cold War phase chronology is placed on the revision page to avoid a mostly empty overflow page; Roosevelt–Gorbachev quotation remains a small revision-sidebar quote, keeping the overview legible.
- Main-body tables: four-row bloc contrast, three-row Soviet collapse factors and five-row Cold War phase chronology (**12 substantive rows**).
- Fifteen section-linked aids cover bloc definitions and internal divisions, the 1944–49 emergence, Marshall Plan interpretation, Korea→Cuba escalation, strategic deterrence, détente agreements, Helsinki, the 1979–85 war scare, 1991 collapse chain, NATO/Warsaw survival contrast and revision milestones.
- Source-level checks before examination use: the approximate 50,000 nuclear weapons figure has no specified peak date; precise characterization of Soviet/US military-economic parity, the timing and attribution of Khrushchev’s claims, the meaning of Helsinki Basket III, the causal weight attributed to Reagan’s SDI, and the Reagan–Gorbachev quotation. The discussion of why the Cold War ended is explicitly presented as an interpretation rather than a universally accepted single-factor explanation.

## Source and engineering boundaries

- Chapters 00–21 and `styles.css`, `engine.js`, `shell.html`, `build.py`, `CSS_DOC.md`, `JS_DOC.md` are unchanged from the previously delivered Chapters 00–21 source ZIP.
- No CSS or pagination engine change was needed. Revision blocks retain `data-revision-start="true"` in both the main and sidebar streams; `data-for-section` links all sidebars to the correct section or revision zone.
- Validate with `python src/build.py --check`, `python src/tests/validate_structure.py`, `python src/tests/smoke_ch22_ch23.py`, `python src/tests/smoke_sidebar_alignment.py`, and (where it completes) the comprehensive export control test. The old all-in-one export smoke may intermittently hang with a large book; separately verify the PDF and custom selection rather than claiming a passing rerun.
