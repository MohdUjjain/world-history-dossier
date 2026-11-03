# Chapters 20–21 — Editorial and publishing handover

**Edition:** World History Dossier, concise-study-notes + Educational Sidebar V2, 3 November 2026. The source is the two user-supplied chapter briefings from this conversation. No external historical research or independent fact-checking was performed. Official textbook titles govern each H1, navigation heading and print contents; descriptive source headings are subtitles.

## Chapter 20 — Stalin and the West

- **Six main sections plus revision**, **8 semantic table rows** (three Gosplan strategic scenarios and five phases of Soviet diplomatic change), **12 section-anchored sidebar aids** across all six established educational purposes.
- Keeps the dual-track argument: fear of capitalist encirclement and ideological revolutionary expectations coexisted with reliance on Western trade, engineers and technology. Includes the 1918–21 interventions, Brest-Litovsk, NEP, Arcos crisis, Five-Year Plans, Metro-Vickers affair, Rapallo/Italy contacts, Popular Front and League entry, 1935 agreements, Munich, 1939 pact, Finnish/Baltic actions and June 1941.
- **Historiographical distinction retained:** Viktor Suvorov's “Icebreaker” thesis is a disputed claim, countered by David Glantz and the source's view that Soviet planning for eventual offensive war did not establish readiness for an imminent July 1941 invasion. This must not be flattened into an assertion of consensus that Stalin was about to attack Germany.
- Miniature aids: 1918–27 timeline, capitalism/trade misconception, strategy contrast, industrialization causal flow, collective-security chronology, contrasting schools of interpretation, 1938 intervention obstacles, pact chain, Barbarossa date, revision four-stage recap.
- **Layout decision:** the Munich heading and first explanatory paragraph are a single atomic `section-head` block to prevent a stranded section heading at the bottom of one PDF page. Screen retains the section association; the main prose is unchanged.

**Textbook/source checks advised:** precise causal relationship between 1927 Arcos/war scare and abandonment of NEP, nature and extent of Rapallo-era military arrangements, attribution and documentary basis for the three Soviet planning scenarios, and evidence in the 1941 pre-emptive-war controversy. They remain attributed to the user's notes rather than silently corrected.

## Chapter 21 — The United States and the End of Isolation

- **Six main sections plus revision**, **10 semantic table rows** (Roosevelt's three threats, three views of Lend-Lease, four revision instruments), **14 section-anchored sidebar aids** including one author-attributed quotation in the revision sidebar.
- Retains the military/economic/ideological rationale, changing Neutrality Acts, cash-and-carry, fall of France, Burke–Wadsworth draft, 50 destroyers and 99-year base leases, the Churchill financial plea, Roosevelt's Lend-Lease authority, America First criticism, Greenland and Iceland, Greer and shoot-on-sight policy, Japan sanctions, Plan A / Plan B, Hull's ten-point proposal, Tripartite Pact and Pearl Harbor.
- Differentiates policy instruments and the immediate-versus-longer-term account of Lend-Lease; preserves the debate over Roosevelt's executive powers and alleged lack of candor. Source's 1940 electoral “your boys” quotation sits alongside the main revision material rather than causing an extra page.
- Miniature aids: three-fear triptych, 1938–40 chronology, cash-and-carry definition, 50/99 quantitative card, historiography contrast, loan-to-aid flow, four-step Atlantic escalation, Japanese oil reserve statistic, Pacific negotiation sequence and consolidated revision timeline.

**Textbook/source checks advised:** the 1941 “1% of Britain's munitions” attribution to David Reynolds and its precise denominator, the Western Hemisphere patrol's unspecified “26th meridian” and the exact blockade geography, comparative strategic claims about destroyers, the eighteen-month Japanese oil reserve estimate, and the Roosevelt 1940 quotation's wording/context. No undocumented adjustment was made.

## QA and maintainability

- **22 active chapters (00–21)**; assembled HTML generated solely from `src/`; **163 16:9 PDF pages (960×540 pt)**, **219 total semantic table rows**, **250 section-linked sidebar entries** (including quotations), **22 revision sections**.
- All previous chapters `00–19` and six shared source/reference files (`styles.css`, `engine.js`, `shell.html`, `build.py`, `CSS_DOC.md`, `JS_DOC.md`) remain byte-identical to the preceding checkpoint. Since CSS/JS did not change, their living references require no changes.
- `tests/smoke_ch20_ch21.py` validates content markers, semantic types, source structure and reader/PDF integration. `tests/smoke_active.py` now uses a three-chapter selection (`last,first,last`) for export-order duplication: this avoids a redundant full-book rebuild on every ever-larger release. `tests/smoke_ch18_ch19.py` now checks the revision count dynamically. `tests/smoke_legacy.py` stubs the native print dialog during its custom-order test to prevent interactive blocking.
- Full active, section-alignment, archived-engine, recent-chapter and source-specific browser regressions pass. Chromium print and 390px screen geometry were inspected; source table rows are complete and no `.col-main/.col-side/.col-full` overflow or JavaScript error was found. Ch20 and Ch21's revision sections each fit on one printed page. The PDF index contains clickable internal hyperlinks but there is no native PDF outline tree.

**Next:** Chapter 22 — The Grand Alliance, 1941–1945.
