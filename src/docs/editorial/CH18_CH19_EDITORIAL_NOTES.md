# Chapters 18–19 — Editorial and production handover

**Edition:** World History Dossier concise study notes / Educational Sidebar V2, 3 November 2026. Source: the two user-provided chapter briefings in this conversation. They were pasted in reverse numerical order (19 before 18); the modules, hero titles, contents and PDF are in official order: 18 then 19. Both descriptive notes titles are secondary subtitles. No external material was added and no independent history fact-check was performed.

## Chapter 18 — The Challenge in Europe, 1935–1941

- Five substantive sections and one separate chapter revision; **15 table rows** across an actor comparison, an event chronology and a final comparison; **13 section-aware aids**.
- Keeps the distinction between moderate treaty grievances and Hitler's wider racial and territorial ambitions. Covers the German resource/military cycle, Fascist Italy, the Soviet shift in 1939, French demographics and Rhineland policy, Britain's imperial distractions, and events through June 1941.
- Formats: two-column actor comparison, three-grievance mnemonic, economic causal flow, alliance timeline, demographic fact, misconception, response comparison and escalation chronology.
- The source's closing point contrasting bold challengers and indecisive defenders was combined with the revision conclusion, rather than stranded on a single near-empty page; its substantive point remains present.
- **Check against the original textbook:** the source's simplified assessment of a 1930s Soviet 'status quo' stance, the economic necessity interpretation of German expansion, the attribution of a dominant 'intentionalist' interpretation to historical consensus, and the quantitative French 'hollow years' statement. These are interpretive or compressed claims, not independently verified facts.

## Chapter 19 — Appeasement

- Six substantive sections and one separate revision; **nine semantic table rows**, **15 section-aware aids**.
- The argument follows a reciprocal and policy-coherent reading of British appeasement: Sargent and Ashton-Gwatkin's 1931 paper, John Simon and disarmament, Chamberlain's 'fourth arm' and RAF priorities, the colonial lever, policy toward Italy, Henderson's March 1938 approach, Munich and the March–September 1939 pivot.
- Formats: settlement causal flow, concept distinctions, four diplomatic levers, three-theatre comparative card, Munich contrast, 1939 chronology, and exam-oriented questions about credibility and Eden.
- **Check against the original textbook:** the quotation ascribed to the 1931 memorandum, the precise date/consequences of Henderson's 'first and last' attempt, the account of Eden's resignation, and the interpretive claim that 1939 was the decisive end of appeasement as a strategy. Preserve the supplied author's perspective while treating it as a historiographical interpretation.

## Production

- Core engine, CSS, shell and living docs not changed. Existing chapter 00–17 modules preserved byte-for-byte. New `tests/smoke_ch18_ch19.py` checks exact official titles, source coverage, section keys, sidebar aid counts, revision markers and browser/print integration.
- Rebuild using `python3 src/build.py`, verify using `python3 src/build.py --check`, then run `smoke_active.py`, `smoke_sidebar_alignment.py`, `smoke_ch18_ch19.py` and `smoke_legacy.py`. The page balance was visually reviewed, especially the Chapter 18 revision and Chapter 19 Munich continuation. PDF rendered with Chromium `prefer_css_page_size=True`.
