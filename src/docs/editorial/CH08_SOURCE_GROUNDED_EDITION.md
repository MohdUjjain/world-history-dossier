# Chapter 08 editorial report — Samuel R. Williamson Jr., “The July Crisis”

## Source hierarchy and purpose

1. **Authoritative source:** uploaded `20th Century History-08.pdf`, Samuel R. Williamson Jr., “The July Crisis,” main chapter printed pp. **105–116**, PDF pp. **1–12** (notes and bibliography extend onto PDF p. 13). Arguments, chronological qualifications, contested evidence and responsibility judgments follow this source.
2. **Language comparator:** uploaded `11- 20TH CENTURY HISTORY.pdf`, Chapter 8, PDF pp. **18–20**. The guide is useful for a readable overview, but its simple chain-reaction framing is insufficient for Williamson's account of political decisions, five distinct stages, and competing interpretations.
3. **Repository baseline:** `src/chapters/ch08.html` from Chapter 07 draft PR #23. Retain six anchors `s1`–`s5`, `revision`, five main topics, one end-of-chapter study section and distinct learning sidebars.
4. **Dependency:** Chapter 08 is stacked on the unmerged Chapter 07 draft PR #23 (after Chapters 04–06 drafts). It must not be merged independently.

## Central argument

Williamson's central explanation is that the Great War was **advertent**: not merely the mechanical outcome of alliance networks or military timetables. These structural conditions made crisis dangerous, but identifiable statesmen and military leaders accepted the possibility of war. Vienna and Berlin bear the **paramount responsibility** for provoking the confrontation, while actions in Serbia, St Petersburg, Paris and London further narrowed opportunities for restraint. Responsibility is **not evenly distributed** simply because many governments made consequential decisions.

The chapter opens with **28 July**, Emperor Franz Joseph's declaration of war; it then reconstructs the crisis's prior causes, assassination and **five successive phases** before assessing how historians have assigned blame.

## Source-grounded reconstruction

| Section | Historical claims and qualifications preserved |
| --- | --- |
| **I. Europe's worsening position, 1911–13** | Agadir and its political/military consequences; France's Joffre, Poincaré and service law; Italy's invasion of Libya; German addition of 136,000 troops; the Balkan League's successes; Albania preventing a Serbian Adriatic outlet; the repeated Habsburg war–peace confrontations culminating in the October 1913 ultimatum; strained South Slav, Romanian and Italian relationships; German Russian/Entente intelligence concerns; Irish, French and Russian domestic disturbances. |
| **II. Sarajevo** | Civilian Pašić versus military-intelligence chief Apis; Black Hand assistance to Princip, Grabež and Čabrinović; Protić's warning and Pašić's attempt to intervene; uncertainty about Artamonov and **no hard evidence** of an official Serbian warning to Vienna; the failed bomb and mistaken car route on 28 June. The simplified guide's claim that Princip was directly a Black Hand member is not silently substituted for Williamson's more specific evidence about Black Hand support and smuggling. |
| **III. Three initial stages** | Phase 1: Vienna's independently reached punishment decision, Hoyos mission, Wilhelm/Bethmann 5–6 July blank cheque and Conrad's harvest leave problem; Phase 2: efforts to lull Europe, Flotow and San Giuliano information leaks; Phase 3: 19 July finalization, Tisza's territorial condition, timing of the **23 July, 6 p.m.** ultimatum after Poincaré's departure, and demands framed for rejection. |
| **IV. Final two stages** | Serbian response and sovereignty, Russian military recall orders from **24 July** before the Habsburg declaration of war, partial vs. general mobilization, Paléologue's failure to urge restraint, Vienna's 28 July war decision, German Moltke/Bethmann ambiguity, Belgrade shooting, Nicholas II's withdrawal of 29 July orders, first **general** mobilization by Russia at 4 p.m. on **30 July**, Germany's consequent ultimatums, Conrad's damaging Plan B then Plan R redeployment, Schlieffen–Moltke through Belgium, France's ten-kilometre frontier order, Britain's cabinet split/Conservative pressure/Belgium, British declaration at 11 p.m. on 4 August and Italian neutrality. |
| **V. Historiography** | Versailles verdict and document publications; revisionist critiques and Lloyd George's unintended-war picture; structural explanations; Fischer's German preventive-war argument; Williamson's own conscious-choice interpretation and **unequal** weighting of responsibility. |
| **Revision** | Five-stage retrieval table, seven-power evidence comparison, 22 printable definitions and a source-analysis problem asking students to distinguish structural pressures from decisions. |

## Corrections to the simplified guide

- **Not a straight chain reaction:** five stages each with distinctive choices, including efforts at secrecy, delays and continuing attempts to mediate.
- **Apis is not Pašić:** Black Hand support for assassination is well described; attribution of direct cabinet sponsorship is not established by Williamson. The original source expressly qualifies what ministers knew and whether an official warning reached Vienna.
- **Russian military orders have two different milestones:** early troop-recall instructions on **24 July**, before Austria-Hungary declared war, versus nationwide **general mobilization on 30 July**. The guide collapses these distinctions.
- **Vienna chose confrontation before Berlin's pledge:** the blank cheque was fateful, but it was not the original cause of Vienna deciding to punish Serbia.
- **Harvest leave and military planning are contingent decisions:** Conrad's Plan B deployment created a damaging rerouting; German assumptions about a quick strike through Belgium constricted the government's choices.
- **Britain did not enter solely by generic alliance pressure:** Ireland dominated politics; British naval obligations, Belgian neutrality and a Conservative offer of support shaped the divided cabinet's eventual decision.
- **The verdict is deliberately weighted:** Williamson identifies Vienna and Berlin as paramount while assigning meaningful roles to Russian, French, Serbian and British actions. “All were equally to blame” misrepresents him.
- **Italy stayed neutral in August 1914** in spite of its Triple Alliance membership; it later fought on the opposite side in 1915. This underscores why automatic-alliance language must be avoided.

## Dedicated semantic-duplication audit — pre-publication

**Main reading text:** each historical event appears in its own chronological or thematic section. The opening establishes the problem, the five-phase narrative supplies evidence, and the historiographical section evaluates responsibility; there is no parallel sequence-by-sequence retelling in prose.

**Tables:** no table interrupts the main exposition simply to restate recently taught facts. The stage chart and country-decision chart are **only in the revision section**, as compact stand-alone retrieval aids; they do not compete with narrative paragraphs.

**Sidebars:** 12 cards each require an operation: counterfactual prediction, distinguishing domestic and international scales, assessing degrees of knowledge, separating trigger from causes, reasoning about the blank cheque, interpreting institutional delay, classifying military orders, understanding sovereignty, explaining deployment logistics, cabinet politics, evaluating unequal responsibility, and a short revision framework. They are not passive restatements of the same timeline.

**Definitions:** the 22 first-use `glossary-term` popups each correspond to exactly one printable glossary row. The print copy is necessary for export, not an inadvertent duplicate. Terms retain specific historical meanings and source qualifications.

**Structure:** 6 anchors, **12** learning cards, **34** table-body rows (5 chronology + 7 comparative + 22 glossary), **22** unique interactive definitions and 22 corresponding printable rows. Main teaching prose approximately **1,807** words excluding revision and glossary. No shared styles, engine, scripts or CSS/JS living references changed.

## Validation checklist

- Extend `src/tests/smoke_ch08_ch09.py` to assert dates, authorship and glossary/side structures while retaining Chapter 09's independent checks.
- Update global glossary count in `src/tests/smoke_reader_ui.py` from 119 to 141; verify Ch08 popup hover and printed rows.
- Regenerate `index.html` and revisioned `service-worker.js` with the current build algorithm; ensure the chapter is embedded exactly once.
- Run all automated CI: source coverage, navigation, accessibility, responsive, print, offline and edition-migration tests.

**Scope:** Chapter 08 prose, its glossary/revision and associated test, documentation, compiled reader and cache artefacts. No styling or pagination-engine edits.
