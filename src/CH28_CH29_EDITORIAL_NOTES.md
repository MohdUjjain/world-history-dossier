# Chapters 28–29 — Editorial and Integration Notes

Checkpoint: 2026-11-03 · Imperial Archive / Educational Sidebar V2

## Scope and source fidelity

The two chapter modules are based solely on the user's newly pasted concise briefings. They reorganize and moderately condense the supplied explanations without independently validating historical claims or consulting external histories. The *official textbook titles* from `chapter_catalog.json` are used for all chapter headings and chapter-level contents entries; the expressive brief titles remain subtitles. No chapter author bylines are guessed. Each chapter is source-authored separately and closes on a contrasting revision section.

### Chapter 28 — The Sino-Soviet Alliance

- Seven substantive sections + one revision section; **9 semantic table rows**, **16 visually varied, section-aware cards**.
- Argument sequence: Soviet interests in the 1945 Guomindang arrangement → Stalin's Tito anxiety and the February 1950 treaty → Korea's unequal wartime burdens → Khrushchev's technical aid and 1956 ideological disruption → 1958 joint-fleet sovereignty dispute → 1959 nuclear assistance withdrawal and open polemics → 1969 border confrontations and strategic Chinese rapprochement with the United States.
- Sidebars are not a mini-glossary: they include a treaty negotiation flow, Korean cooperation/responsibility comparison, Khrushchev/Mao ideological contrast, naval sovereignty misconception, three-way cause model, 1969 timeline and revision synthesis.
- **Verification cautions:** The 1950 secret arrangements described as Soviet preferential/exclusive rights in Xinjiang and Manchuria; characterization of Stalin's Korean calculation; the 1959 prototype nuclear promise; the exact 1969 Soviet nuclear threats; and the exact wording/attribution of Mao's 1958 statements and 1963 poem should be checked against the original textbook before examination use. The notes are presented as supplied, not endorsed as independently verified archival findings.

### Chapter 29 — The Collapse of the Soviet Union and the End of the Cold War

- Seven substantive sections + one revision section; **11 semantic table rows**, **18 section-linked cards**.
- Source interpretation: Gorbachev's plans and limitations; 1985 anti-alcohol drive, regional patronage networks and Chernobyl; partial enterprise reform and Yeltsin's political opposition; summits and Soviet non-intervention in Eastern Europe; nationality conflicts and Russian sovereignty; 1991 coup and Belavezha dissolution; multicausal review.
- **Verification cautions:** The source's estimated 40% share of national wealth devoted to defense is definition-sensitive and unverified. The enterprise-law date is presented in the user's briefing as 1986, which may refer to a different legislative or preparatory event; confirm against a reliable chronology before exam use. The supplied anecdote about Yeltsin's 1987 personal crisis/possible self-injury is not asserted as a settled event or necessary to the chapter's argument. The Malta summit characterization, the June 1990 sovereignty resolution and the precise chronology of the December 1991 dissolution should be checked with the original textbook. Accounts of Gorbachev's expertise and intentions are framed as the supplied historian's interpretation. Although the union's central demise was comparatively nonviolent, the chapter explicitly mentions violence in the republics and Vilnius.
- A source-based early-shocks timeline originally straddled the transition from section II to section III in the print engine. It has been replaced by a **1986–89 reform-to-opposition timeline anchored to section III**, which is the most relevant conceptual discussion. The earlier 1985–86 events remain fully explained in the section-II narrative and its two other educational cards. This eliminates the single page-level mismatch without an engine change.

## Implementation / release contract

1. Keep the existing `styles.css`, `engine.js`, `shell.html`, `build.py`, `CSS_DOC.md`, `JS_DOC.md` and Chapters 00–27 byte-for-byte unchanged.
2. Each new chapter has the official `data-title`/hero H1, descriptive `data-subtitle`, `src-hero`, `src-main` and `src-side`, and one `data-revision-start="true"` in each of main and sidebar source streams.
3. The sidebar's *purpose* (`def`, `concept`, `tip`, `mistake`, `memory`, `hy`) is distinct from its *display* (`text`, `comparison`, `triptych`, `flow`, `timeline`, `stat`); each is anchored by `data-for-section` to a matching main `data-section-key`.
4. Run `python src/build.py --check`, `python src/tests/validate_structure.py`, `python src/tests/smoke_ch28_ch29.py` and `python src/tests/smoke_sidebar_alignment.py`. The focused smoke also checks repeated custom export `29,28,29`, revision toggle and 390px mobile width. The archival smoke is maintained.
5. The batched `src/tools/export_full_pdf.py` renders the unchanged full-book print DOM in manageable Chromium batches and restores internal TOC destinations in PyMuPDF. This is a **searchable 16:9 PDF with clickable contents links**, not a native PDF outline/bookmark tree.

**Next official chapter:** 30 — War and Peace in the Global Community, 1989–2001.

**Final visual QA:** The section-V heading in Chapter 28 initially began at the very bottom of a print page without its initial explanation. The source authoring now keeps that heading and the first “Who Plays the First Violin?” explanation in **one indivisible source block**; it starts cleanly on the following page, and full-book pagination remains at 234 pages. This changes neither the CSS/JS engine nor the historical argument. All layout and source-specific smoke tests were rerun after the fix.
