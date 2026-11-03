# Chapters 24–25 — Editorial Integration and Source Cautions

## Scope and editorial policy

Both chapters were created solely from the user's concise pasted briefs. The **official textbook titles** (`A Third World?` and `Making the New Europe: European Integration since 1950`) govern the main H1 and contents; the more descriptive pasted headings remain subtitles. The supplied claims were **not independently fact-checked**. Tables were reconstructed as accessible HTML tables, and some prose was consolidated to avoid repetition without intentionally introducing additional historical assertions.

## Chapter 24 — A Third World?

- **Six substantive sections + revision**. Fifteen section-linked Sidebar V2 aids use six kinds and six presentation types, including the 1945–1980 UN-membership statistic, Sauvy's Third Estate analogy, Bandung, the leaders, NAM summits, NIEO policy targets and movement fragmentation.
- **17 preserved table rows**: three UN-demography observations, five leader profiles, five selected NAM summits and four NIEO policy objectives. No original datum was omitted merely to fit a page.
- The source spells the Egyptian leader **“Gammal Abdel Nasser”**; the notes normalize this to the more common **“Gamal Abdel Nasser”**. Verify against the textbook if literal reproduction is important.
- The values **51/100/150** UN members and **14/52/91** Afro-Asian members (with stated percentages) are included **as provided**. Membership classification varies by definition and these are not independently verified.
- The source describes a strict NAM rule excluding membership in defence pacts. The study notes frame this as an **initial political principle**, not a universal timeless legal eligibility rule. Early organization is described as minimalist and heterogeneous.
- Source claims about the **Monroe Doctrine's role in Latin America's absence at Bandung**, the ideological grouping at the 1979 Havana summit, the NIEO's **0.7% GNP** development-aid target, and the category **“Fourth World”** are presented as the source's framing rather than independent findings.

## Chapter 25 — Making the New Europe

- **Six substantive sections + revision**. Sixteen section-linked Sidebar V2 aids use six kinds and five-plus presentation types. Emphasis is on the *exercise of sovereignty collectively* rather than a teleological surrender of statehood.
- **18 preserved table rows**: three institutional contrasts, four Community institutions, three historiographical schools and eight historical milestones.
- The briefing treats OEEC and the Council of Europe as inadequate to **supranational integration**. The text distinguishes that narrow evaluation from any claim that they accomplished nothing in other fields.
- The supplied chronology simplifies several institutional transitions and uses **1947** for the Marshall Plan/OEEC sequence, **1992/2002** for Internal Market/Euro and **2004** for “Eastern enlargement.” Values and stages are retained as the source presents them, not externally corrected.
- “**Mailbox democracy**,” **Milward's rescue-of-the-nation-state** interpretation, the **Luxembourg Compromise**, Commission/Council differences and post-1973 enlargement appear in the explanatory narrative and learning aids.
- The first-edition PDF has one readable continuation page (p. 196) for the final eight-row milestones table and the widening/deepening explanation. Moving the entire table to the revision section made revision run over to a second page, so the cleaner original arrangement was retained. The one-page dedicated revision spread remains intact.

## Engineering and QA

- No changes were made to `styles.css`, `engine.js`, `shell.html` or `build.py`, so `CSS_DOC.md` and `JS_DOC.md` **remain synchronized and unchanged**.
- `smoke_ch24_ch25.py` validates source coverage, tables, sidebar variety/anchors, revision toggles, repeated custom-order export and 390px mobile width using an isolated production-shell fixture.
- `smoke_ch22_ch23.py` received a **test-only append-safe** index fix so it continues to work after Chapters 24–25 are added.
- Full source and print-DOM audits preserve all **272 table rows**, **310 side notes**, and **26 revision zones**, with no detected overflow or misplaced side notes.
- A full-size Chromium `Page.pdf()` call stalled while painting the entire 197-page book. The verified print DOM was therefore rendered into **17 consecutively numbered print-only batches**, merged to a single 16:9 PDF, and **185 internal PDF contents links were restored using actual DOM anchor rectangles and page IDs**. This method creates the downloadable PDF without altering the **browser's own chapter-range export behavior**. No claim is made for native PDF outline bookmarks.
- The original supplied historical claims are left for future checking against the textbook rather than silently amended.
