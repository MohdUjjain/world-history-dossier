# Chapters 30–32 — Closing editorial record (3 November 2026)

## Scope and source fidelity

The final three active chapters were authored exclusively from the three concise study briefs provided by the user. They **do not** import earlier legacy notes, unrequested research, or an outside narrative. Names, official chapter headings, conceptual comparisons, argumentative structure, principal dates and supplied data are preserved or clearly attributed. Expressions such as *End of History*, *Jihad vs. McWorld*, *Golden Straitjacket*, *Electronic Herd*, *propaganda by deed* and *preventive war* are explained rather than used as unsupported slogans.

### Chapter 30 — War and Peace in the Global Community, 1989–2001
- Subtitle: *Wilsonianism, Globalization and the Fragile Global Community*.
- Six main sections plus a distinct contrasting revision: Wilsonian triad; Bush's New World Order; international economic integration; Clinton and intervention; Balkan wars/NATO; limits by 2001.
- **12 main table rows; 15 Sidebar V2 learning aids**. Retains all three supplied US economic indicators for 1990 and 2000, all three selected intervention comparisons, and the final triad verdict.
- Academic caveats: the supplied account describes the Somalia losses as “18 US Marines”; their service identity should be checked. Its “100,000 in 100 days” figure for Rwanda is not a reliable total for the genocide. The claim that Kosovo was NATO's “first-ever combat operation” and the precise attribution of a Clinton quotation should also be independently verified. The narrative avoids repeating questionable precision where not essential to the source’s argument.

### Chapter 31 — Globalization
- Subtitle: *The Synergistic Integration of the Modern World*.
- Six substantive sections plus revision: four engines; nineteenth-century globalization; interwar disruption and continuity; late-century acceleration; ideological contest; fragility.
- **15 main table rows; 15 Sidebar V2 learning aids**. Includes GATT, IMF and IBRD roles, the Keynes recollection, port handling and transnational estimates, Stiglitz's criticism of IMF programmes, and a future projection clearly labelled as a projection.
- Academic caveats: source numbers for shipping costs, container port productivity, number/employment of transnationals and annual FDI growth need source verification. The proposal that Asian states may lead after 2050 is forecast, not an established event. Distinguish *The Lexus and the Olive Tree* from later “flat world” vocabulary if attributing specific metaphors to exact works.

### Chapter 32 — Terrorism: September 11, 2001 and its Consequences
- Subtitle: *The Architecture of Asymmetry — September 11 and Global Security*.
- Six main sections plus revision: definition and comparison; historical patterns; al-Qaeda; September 11 and collective defense; preemption/prevention and Iraq; detention, networks and international legitimacy.
- **12 main table rows; 15 Sidebar V2 learning aids**. Distinguishes terrorism from guerrilla war and organized crime; distinguishes preemptive force from preventive war, and Afghanistan's 2001 rationale from Iraq's 2003 justification. Treats al-Qaeda's religious-political claims as its **own extremist programme**, not a description of Muslim people.
- **Especially important source checks:** the briefing's “over 3,000” September 11 fatalities figure needs correction against an authoritative victim count before factual publication; the approximate $500,000 operational cost should be independently checked. UN Security Council Resolution 1368 recognized the inherent right of self-defense, but that does not resolve the legality of subsequent uses of force. Attribution of Madrid and London attacks to the named Abu Hafs al-Masri Brigade is disputed and should not be stated as fact without robust independent evidence. The briefing's terms *unlawful combatant*, *preemption* and *prevention* all require careful legal distinctions. No current-events updating is implied by the older source’s “to the present” phrase.

## Production decisions

- The 33 official chapter titles in `chapter_catalog.json` control H1, chapter metadata, sidebar index and PDF navigation. Expressive note headings are secondary subtitles.
- Every main section is keyed (`data-section-key`), and every learning aid references it (`data-for-section`). Revision markers are set once in the narrative and once at the first revision-sidebar card. Later revision cards remain in the same semantic zone without reopening revision pages.
- Large, redundant visual learning aids were consolidated to prevent section-spill and nearly empty continuation pages. The core ideas remain in chapter narratives or tables.
- `styles.css`, `engine.js`, `shell.html`, `build.py`, `CSS_DOC.md` and `JS_DOC.md` were intentionally **not edited**. The design system and engine documentation are still canonical.
- An append-safe `tests/smoke_ch30_ch32.py` verifies source coverage, repeated custom-order exports, revisions, 16:9 print geometry and 390px mobile layout. The full sidebar alignment suite additionally checks the assembled 33-chapter book.
- The final PDF is exported from the **same assembled book's pagination DOM** in bounded batches with `tools/export_full_pdf.py`, preserving clickable contents links. PDF **does not contain native bookmark outlines**.
