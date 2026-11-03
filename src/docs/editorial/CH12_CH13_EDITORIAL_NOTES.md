# Editorial checkpoint — Chapters 12 and 13

Date: 2026-11-02. Based on the user's latest shorter chapter briefs exclusively. No independent fact-checking or outside historical research was performed. The official textbook titles appear in chapter headings/index, while descriptive notes titles are subtitles. All substantive concepts, figures, chronology, arguments and concluding assessments in the supplied briefs have been represented, in concise structured prose, tables or side aids.

## Chapter 12 — The Versailles System

Seven main sections: punishment/rehabilitation/idealism; reparations and financial stabilization; Articles 231, 227 and 228; disarmament/IMCC; plebiscites/minorities; Locarno/fulfilment; Hitler's violation of treaty limits. A separate revision page collects the final institutional assessment and treaty-violation table, avoiding an otherwise nearly empty spillover page. Three main/revision tables contain 5+4+4 = **13 body rows**. Eleven side aids cover seven main sections and the revision; they vary by type (def, concept, tip, memory, high-yield, misconception) and display (contrast, timeline, comparison, flow, statistic, text).

**Source caveat (not silently changed):** the supplied material dates the Luftwaffe announcement to 8 March 1936 and the conscription announcement to 16 March 1936. These look inconsistent with standard historical chronology; the source's dates are reproduced in a labelled table, with a visible source-verification reminder in the section sidebar. The source's bank name varies; the notes use *Bank for International Settlements*. Its characterization of Article 231 is described as the familiar war-guilt label together with its reparation liability function. Treaty interpretation and causal claims are presented as interpretations supplied by the user, not independently verified facts.

## Chapter 13 — The Legacy of the First World War

The supplied briefing focuses on the **League of Nations** rather than an all-purpose survey of the war's legacy. Its heading is the official catalogue name; its descriptive subtitle identifies that focus. Four main sections cover the peace treaties/Covenant, Anglo-French control and American absence, financial and humanitarian institutions, and arbitration case studies. The separate revision draws out the sovereignty–collective-security problem and League institutional legacy. Two tables contain 4+5 = **9 rows**. Twelve side aids use six purpose categories and several visual presentation forms.

**Source caveat (not silently changed):** the input describes the Åland Islands dispute as resolved in Sweden's favour and Vilna as a port. These details require consultation of the original academic chapter before memorization and are explicitly flagged in a source-check side card. The notes retain the League case-study argument without adopting those doubtful geographical descriptions as fact. The connections drawn between Sèvres and the mandate scheme reflect the user-provided briefing. The source's figures for League financial loans and minority protections have been preserved without external validation.

## Quality and preservation

- Existing `ch00.html`–`ch11.html`, `shell.html`, `styles.css`, `engine.js`, `CSS_DOC.md` and `JS_DOC.md` remain byte-identical to the Ch00–11 checkpoint. No shared production code or style changes were needed.
- The new chapter authoring uses semantic `.src-main` blocks and `.src-side` Sidebar V2 learning cards with `data-for-section` anchors matching `s1`..`sN`, plus first revision markers in both columns.
- `src/tests/smoke_ch12_ch13.py` checks source sentinels, exact table-row counts, sidebar cards, the official headings, complete chapter order and print preservation. Existing structure, active, sidebar, old-pair and legacy regression suites passed.
- Full-book PDF is **106 pages** of 16:9 landscape with selectable text and 96 clickable internal links. No native PDF outline (known engine/export limitation). Print content has zero detected column overflow.
