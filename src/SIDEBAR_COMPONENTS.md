# Educational Sidebar Standard — V2 (Chapters 00–25)

This file is an authoring reference for Chapters 06–32. It supplements `CSS_DOC.md` and `JS_DOC.md`. The goal is a **second teaching layer**, not a glossary that duplicates the main narrative.

## Two independent dimensions

Every note is a direct child of `.src-side` and declares:

- **Purpose** — `data-kind="def|concept|tip|mistake|memory|hy"` and the matching inner `.box` colour class (`.def`, `.concept`, `.tip`, `.mistake`, `.memory`, `.hy`). Quotations use `data-kind="quote"` and `.quote`.
- **Presentation** — `data-display="text|timeline|comparison|profiles|flow|steps|triptych|stat|contrast"`. This chooses the shape of the visual while **purpose still determines colour**.
- **Section anchor** — `data-for-section="s1"`, `s2`, ... or `revision`. The related heading in `.src-main` must have `data-section-key="s1"` and so on. A section may span multiple PDF pages; side aids are placed on an appropriate page of that section.
- **Pagination** — `data-keep="together"` for atomic cards; long lists/tables may use the existing split-list/table infrastructure.

Example:

```html
<div class="block" data-kind="tip" data-display="contrast"
     data-for-section="s2" data-keep="together">
  <div class="box tip learning-card">
    <div class="box-label">Exam insight</div>
    <div class="learning-title">Two outcomes to distinguish</div>
    <div class="learning-content"><p>A compact, source-derived contrast.</p></div>
  </div>
</div>
```

## Suggested editorial mix per concise chapter

Normally **6–9 main-body aids**, with optionally 1–2 revision aids. Choose only useful categories; no quotas, forced mnemonics or invented controversies. A useful chapter might contain 1–2 definitions, 1 key diagram, 1 misconception (only if the source supports it), 1 exam insight, 1 memory aid and 1 high-yield observation. Avoid a monotonous run of green `.concept` cards.

### Supported miniature visual layouts

| CSS class | Use |
| --- | --- |
| `.mini-compare` | Two contrasting interpretations or institutional models |
| `.mini-stack` | Three or more compact rows, such as forms of rule |
| `.mini-profiles` | Four thinkers, with very short accurate positions |
| `.mini-timeline` | Dates / sequence / milestones |
| `.mini-chain` | Short left-to-right transition |
| `.mini-flow` | A causal chain top to bottom |
| `.mini-triptych` | Three remembered pillars or categories |
| `.mini-steps` | Four phases in a 2×2 frame |
| `.mini-stat` | One source-supported number with context |

All are DOM text and CSS, not raster graphics. Keep a whole card within the sidebar page-height budget (560px; ideally far less). Historical source wording must be checked; a card may clarify or reorganize what is in the notes, but must not introduce new unsupported facts.

## Screen and PDF layout relationship

- **Screen HTML:** `appendPairedSections()` creates a `.chapter-grid.section-pair` for each narrative section, placing its corresponding side aids directly beside that section. The HTML remains one uninterrupted scrollable reading view.
- **PDF:** `packChapter()` first paginates the main text. Then `attachSectionSideNotes()` attaches each card to a content page where the matching section appears. It can split older sidebar glossary lists/tables and create a continuation page when truly required.
- **Revision:** Keep the first revision side card marked `data-revision-start="true"`, paired with a main revision heading using the same flag and `data-section-key="revision"`.
- **Existing safeguard:** The engine MUST continue measuring clones, never moving nodes out of `#chapterData`.

## Chapter-specific design applied in this baseline

- **00:** Geopolitics definition, imperial-strength mnemonic, misconception about overseas-only imperialism, race/class contrast, Cold War exam insight, transition to economic empire, four-era revision.
- **01:** Three imperial rule forms, Boer War misconception, maritime dates, WWI/WWII comparison, dyarchy definition, Partition statistic, decolonization timeline.
- **02:** Four scholar tiles, imagined-community definition, Nature–Language–History anchor, language/state statistic, sacred/national ritual comparison, industrial identity chain, socialism misconception.
- **03:** Pre-1914 institutions timeline, Hague arbitration definition, League achievements-vs-failures tip, League organs, UN veto paradox, Cold War veto count, ICRC/MSF contrast, four-phase revision.
- **04:** Time-and-space causal flow, telegraph finance, 1925/1983 telephone-call comparison, television figure, transport chronology, Ford misconception, technology recap and neutral-use lessons in revision.
- **05:** Telegraph centralization flow, Wilson triptych, merit-based reform timeline, diplomat/consul comparison, four-country profile, erosion-of-monopoly misconception, EU specialist process and three-stage diplomatic evolution recap.

## Mandatory validation

```bash
python3 src/build.py
python3 src/tests/validate_structure.py
python3 src/tests/smoke_active.py
python3 src/tests/smoke_legacy.py
python3 src/tests/smoke_sidebar_alignment.py
```

The last test verifies all sidebar aids are paired with the correct screen section and printed beside a page containing the corresponding narrative section. Run `python3 src/tests/smoke_ch04_ch05.py` for additional source-specific checks of the two new chapters. It also verifies the `.src-main` text is unchanged relative to the previous Ch00–03 source when the baseline ZIP is available.

- **06:** <em>Revanchisme</em> and <em>casus foederis</em> definitions, 1879–1887 alliance timeline, restraint-versus-aggression misconception, Weltpolitik/Italian claims, geographic friction comparison, opposing war plans and Italy’s defection chronology.
- **07:** <em>Revanche</em> definition, France–Russia complementarity, splendid-isolation correction, Risk Fleet causal flow, 1902–1907 diplomatic sequence, Grey’s balancing strategy, Morocco/Bosnia/Agadir crisis chronology, Britain’s 1914 alternatives and closing source quotation.

- **20:** Capitalist-encirclement definition, 1918–27 events, 1930 planning contrast, industrialization causal chain, Comintern-versus-imports misconception, Soviet collective-security chronology, contrasting historiographical schools, Munich military/geographic constraints, 1939 pact flow, contested Icebreaker comparison and Barbarossa memory figure.
- **21:** Three-threat triptych, 1938–40 neutrality chronology, cash-and-carry definition, destroyers/base-leases statistic, opposing interpretations of the secret executive bargain, Lend-Lease causal flow, four-step undeclared Atlantic war, Japan’s oil-reserve figure, failed 1941 negotiation flow, revision chronology and Roosevelt’s quoted electoral assurance.

- **22:** Three Allied objectives, founding commitments, Second Front political/military distinction, TORCH-to-OVERLORD causal flow, Teheran decisions, the Four Policemen paradox, contested postwar self-determination, Balkan percentages mnemonic, Polish/Yalta diplomacy, EAC and a revision contrast of Anglo-American and Soviet-Western ties.
- **23:** Bipolarity definition with bloc-asymmetry misconception, internal bloc differences, 1944–49 emergence chronology, Marshall Plan exam framing, Korea→Cuba flow, nuclear-deterrence concept, 1963–75 détente timeline, human rights vs arms-control distinction, Reagan/Gorbachev change, collapse chain and retained Cold War phase table on revision.

- **24:** UN representation stat, Third Estate definition, political-versus-economic meaning of “Third World”, Bandung psychological impact, Nasser/Nehru/Tito leadership contrasts, NAM chronology, UNCTAD→G77→NIEO causal chain, aid benchmark, economic leverage and decline causes.
- **25:** OEEC/ECSC institutional distinction, Schuman security–industry chain, the Six, EDC misconception, Rome treaty essentials, Commission–Council comparison, idealist/realist/Milward historiography, 1966/1975 governance chronology and 1973–2004 enlargement.
