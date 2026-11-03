# Editorial handover: Chapter 04 and Chapter 05

**Date:** 2026-11-02  
**Source:** concise chapter notes pasted directly by the user in the current conversation.  
**No external factual research or incorporation of archived long chapters.**

## Chapter 04 — A Shrinking World

- Official heading: **A Shrinking World**. User's expressive subtitle: *The 20th Century’s Acceleration of Globalism*. The user credits historical analysis to Jeffrey A. Engel; the notes remain the source of the claims, not a verified reproduction of a textbook chapter.
- Main structure: acceleration as the defining development; wired/voice/radio/television communications; automobile and aviation; milestone table; concluding claim of technology's moral neutrality.
- Restored the raw comma-delimited 1925/1983 telephone comparison and the five-technology milestone list as real HTML tables, preserving user-supplied values.
- Ten section-aware sidebar cards: false claim that globalism was invented in the twentieth century, compression of time/distance, telegraph-to-finance causal flow, long-distance telephone-price comparison, caution concerning the Zimmerman Telegram, television-ownership statistic, aviation/automobility chronology, clarification of Ford's contribution, four-part memory frame, and three closing lessons. Visual forms include flows, comparisons, a statistic, a timeline and a compact stack.
- The five-technology recap belongs to the **revision zone**, which begins on a new PDF page. The three final takeaways were placed as a compact high-yield revision sidebar to avoid creating an otherwise almost empty second revision page. These distinctions remain readable and searchable.
- Wording and details that appeared ambiguous in the supplied notes are not silently revised: for example, “Zworkin / Baird” in the television milestone table; the source-supplied mention of the Zimmerman Telegram. Historical verification may be conducted separately if requested.

## Chapter 05 — A Changing Diplomatic World

- Official heading: **A Changing Diplomatic World**. User's expressive subtitle: *The Evolution and Transformation of Modern Diplomacy*.
- Main structure: the three catalysts (technology, ideological/warfare transformation, more international actors); the professionalization/expansion/centralization of services; four distinct national reform paths; modern challenges to diplomats' information monopoly and bureaucratic distinctiveness; three-stage revision recap.
- The comma-delimited staffing comparison is reconstructed as a semantic table. Different benchmark years are explicitly retained; the German figure's later label is left as **“Today” in supplied notes; no year stated**, rather than inventing one.
- Ten section-aware sidebar cards: telegraph/capital control flow, Wilson's three pillars, expansion of actors, four-stage professionalization timeline, diplomatic-versus-consular comparison, centralization causal flow, four national-profile tiles, misconception about more relations necessarily strengthening ambassadors, EU specialist negotiation flow and a four-part revision memory aid.
- Clausewitz quotation and the source account of total warfare are preserved as source-derived claims, not independently adjudicated historical conclusions.

## Layout and testing

- No changes to `styles.css`, `engine.js`, or `shell.html`; therefore their living documents `CSS_DOC.md` and `JS_DOC.md` remain current and unchanged.
- Each sidebar card has `data-kind`, `data-display`, and `data-for-section` and is aligned with a real main-text section. Long tables use `data-keep="split-table"`.
- Official catalogue titles are used in the chapter heroes, the HTML contents drawer and the printed table of contents; expressive notes headings appear only as subtitles.
- The existing authoring method remains `python3 src/build.py` followed by validation, browser, archival and sidebar-alignment regressions. New factual-source consistency tests live in `tests/smoke_ch04_ch05.py`.
- Active chapters now run **00–05 (six chapters)**. Chapters 06–32 still await text.
