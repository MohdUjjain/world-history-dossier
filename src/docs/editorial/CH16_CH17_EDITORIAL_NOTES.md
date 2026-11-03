# Chapters 16–17 — Editorial and production handover

**Edition:** concise World History Dossier / Sidebar V2, November 2026. These two chapter modules derive exclusively from the author's/user's supplied concise briefings in this conversation, not from external research. The official titles are drawn from `chapter_catalog.json`; descriptive briefing titles remain secondary subtitles. The existing historical claims have **not been independently verified**. Minor editorial joining of adjacent material is intended to remove repetition and improve pagination, not expand the narrative.

## Ch16 — The Challenge to Empire in the Middle East and Asia

- Five substantive sections plus one contrasting revision section, **five semantic table rows**, **thirteen section-linked learning aids**.
- Organizing argument: the mandate system, elitist nationalist histories versus subaltern resistance, Gandhian non-cooperation and its limits, Turkey/Egypt/Iraq/Syria, and Vietnam/Indochina. The distinction between protests driven by material grievances and elite retrospective national narratives remains central.
- Sidebar diversity: definitions and premise checks on mandates and self-determination; subaltern-vs-elite comparison; Satyagraha/Swaraj/Hartal memory steps; Amritsar figure; Egypt–Turkey contrast; Middle Eastern chronology; Indochina sequence; exam-oriented question about retrospective leadership claims.
- The original two subsections on VNQDD/ICP and Nghe An/Ha Tinh were joined into one main-text block to avoid a near-empty last content page; all three events/organizations, spontaneity of rural uprisings, suppression, and their approximate dates remain.
- **Verification flags:** The absolute wording that Turkey was the only country to attain genuine independence should be judged within the scope of the scholar's comparison rather than applied to every Asian or Middle Eastern country. Amritsar's death toll, the claim about the 1935 Government of India Act's reserved powers, the Syrian death estimate, and the specific causal interpretation of the peasant movements should be checked against the textbook before examination use.

## Ch17 — Mussolini's War in Ethiopia

- Four substantive sections plus one contrasting revision, **nine semantic table rows**, **twelve section-linked sidebar aids**.
- Organizing argument: Ethiopia's sovereign military and diplomatic foundations; Mussolini's Fascist national project; Stresa, partial sanctions, Suez and Hoare–Laval; chemical violence, bombing and European realignment.
- Sidebar diversity: Adowa strength comparison; Ethiopia 1896/1935 security contrast; Rases definition; Fascist prestige causal flow; wedding rings high-yield observation; League sanctions misconception; 1935 chronology; competing League/strategic priorities; civilian-war exam framing; revision dates.
- **Verification flags:** The source describes both “nerve gas and mustard gas.” Mustard gas is retained in the main text; the “nerve gas” attribution is explicitly flagged as requiring verification and must not be taught as established. The source's treatment of the Peace Ballot's 11 million, the exact diplomatic consequences of Stresa and Hoare–Laval, and simple linear accounts of Mussolini's shift to Hitler are highly compressed and require comparison with the original scholarly source. Direct quotations should be checked against their source for exact wording. The number of troops at Adowa is as supplied and not independently established.

## Production and validation

- Added `chapters/ch16.html`, `chapters/ch17.html`, and `tests/smoke_ch16_ch17.py`.
- Metadata: one `data-section-key` per main section, one first revision marker per stream, and all educational aids assigned via `data-for-section`. Confirm the entire book with `smoke_active.py` and `smoke_sidebar_alignment.py`.
- No modifications to `styles.css`, `engine.js` or `shell.html`: their living `CSS_DOC.md` and `JS_DOC.md` need no revision and remain canonical.
- Source checkpoint contains all 18 active modules, the 00–32 catalogue, archive, build script, test suite and living documentation. PDF is true 16:9, source-selectable and in-page clickable. Native PDF outline/bookmarks remain unsupported, as in prior checkpoints.
