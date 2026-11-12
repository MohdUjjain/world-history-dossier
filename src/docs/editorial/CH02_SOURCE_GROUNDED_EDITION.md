# Chapter 02 — Nationalism: source-grounded teaching edition

**Status:** A separate editorial pilot based on the Chapter 01 clarity/glossary infrastructure. This is a content revision, not an alteration to the print compositor, site typography, color semantics or existing chapter navigation.

**Three-source hierarchy**

1. **Authority:** R. J. B. Bosworth, “Nationalism,” `20th Century History-02.pdf`, PDF pp. 1–12 (original chapter pages 26–37), followed by references on PDF p. 13.
2. **Language reference, not fact authority:** `11- 20TH CENTURY HISTORY.pdf`, “Chapter 2: Nationalism,” PDF pp. 3–4.
3. **Editable baseline:** pre-edit `src/chapters/ch02.html` on the Chapter 01 editorial branch in `MohdUjjain/world-history-dossier`.

## The author's argument reconstructed

| PDF source pages | Scholarly movement | How retained in the revised notes |
| --- | --- | --- |
| 1 | Shakespeare's MacMorris; national identification can inspire sacrifice, exclusion and violence; historical victimhood reinforces national boundary | Introduction: belonging and the “Other” are the opening problem, not a slogan about patriotism |
| 2 | Theorists disagree: Gellner, Hobsbawm, Anderson, Smith; origins, invention and emotional reality | §1: comparative theory table and a paragraph interpreting their differences |
| 2–3 | Geography or “native soil” as political justification; mutable environment and meanings; Nazi “blood and soil” appropriation | §2 Nature: real land versus its historically constructed claim to an eternal nation |
| 3 | Language is not a one-to-one nationality test; approximate 6,800 languages and 230 states are Bosworth's period estimates; languages are politically standardized and socially mixed | §2 Language: caution that counts are historical estimates and distinction between language and state |
| 3–5 | National culture and the “usable past”; Michelet, Bancroft, Palacký; professionalism of history and its national institutional setting; genealogy and invented continuity | §2 History: historians as nation-makers and potential critics |
| 5–6 | George L. Mosse's “nationalization of the masses”; French Revolution, popular will, secularization, flags, anthems and rituals acting as civic religion; modern advances accompanied contradiction | §3: what ritual actually **does** rather than just listing emblems |
| 6–7 | Are there premodern nations? Medieval labels were variable, many languages and loyalties coexisted; modern national obligation is not simply identical with premodern uses of the word | §4: 1138 chronicler, medieval multilingual “English nation,” 1220 Paris student “nations” |
| 7–8 | Revolutionary and Napoleonic acceleration; independence and unification; modern bureaucracy, railways and education | §4: political revolution **and** administrative infrastructure explain the rise of nation-states |
| 8–9 | Marx/Engels reject national priority; German socialists support war credits in 1914; Soviet ideology oscillates between universalism and patriotism | §5: theorized universal class loyalty versus actual wartime national loyalties |
| 9–10 | Jewish assimilation/socialism, antisemitic classification and racist pseudoscience, Holocaust, Herzl/Zionism and disputed territory | §6: racist claims explicitly identified as false; Zionism and competing claims to Palestine described as Bosworth's analysis |
| 10–12 | Decolonization, Cold War, Berlin Wall and “end of history”; US nationalism/immigration/religion, Israel, India and Arab/Muslim worlds; nation can sustain progress yet requires exclusionary myth | §7: comparative but not equivalent examples, early-2000s contextualization, and explicit conceptual closure |

## What changed relative to the existing Chapter 02

- Replaced abbreviated lists of theoretical positions with a **cause-and-interpretation** comparison; “imagined” is not misconstrued as unreal.
- Restored Bosworth's introductory discussion of nation-based exclusion, fear of the Other, ethnic cleansing, and grievance/victimhood.
- Kept the source's deliberately unsettling distinction between nature/language/history as *real material* and their nationalist uses as *naturalized proof*.
- Strengthened the continuity argument: history is both a tool of nation-building and a critic of nation-building.
- Made the Mosse **popular sovereignty → ritual/civic religion → durable national solidarity** chain explicit, with a closing sentence resolving it.
- Restored the section on **nation before the nation**, including distinct medieval “nations” that did not align with present political borders.
- Explained the institutional mechanism of railways, bureaucracy and mass education, rather than assuming they naturally create national unity.
- Connected socialist internationalism to the specific **1914 German social-democratic vote** and to **Soviet patriotic mobilization**, closing the anti-nation paradox.
- Carefully distinguished antisemitic propaganda from facts about Jews, and kept the Zionism and Palestinian-territory discussion without collapsing it into one-sided triumphalism.
- Treated the original author's 2000s examples and value judgments as **historically situated interpretations**, not as unqualified present-day descriptions.
- Expanded/clarified the main explanation where doing so removed inferential burdens on students; preserved the existing seven section anchors `s1`–`s7` plus `revision`.

## Academic terminology and interaction

Fourteen **first meaningful occurrences** get screen-reader definition popovers via the existing Chapter 01 `.glossary-term` controller, with **no parenthetical glosses** in the main notes:

**nationalism; ethnic cleansing; nation-state; invented tradition; imagined community; native soil; usable past; nationalization of the masses; popular sovereignty; civic religion; self-determination; socialist internationalism; Zionism; decolonization.**

The definitions are collected into the separate, **print-safe** revision table. A glossary popup is not duplicated by a definition-only sidebar. There are **12 section-linked sidebar cards** across all six semantic colors/types. The standalone **civil service** sidebar definition is deliberately **not** also a popup. The other callouts add memory sequences, interpretive distinctions and exam cautions rather than definition duplicates.

**Print behavior:** the popup itself is hidden in print; the revision glossary preserves the meaning of all 14 terms when revision material is included. If the user explicitly excludes revision material, the prose still uses the specialist terms but does not carry the glossary table (the same agreed limitation as the Chapter 01 pilot).

## Factual corrections, qualifications and the role of the simpler guide

- **Gellner's given name:** Bosworth's chapter prints “Ernst Gellner” (PDF p. 2), but the author of *Nations and Nationalism* is **Ernest Gellner**. The editorial version uses the bibliographically verified spelling. External confirmation (used only for this name): [Indiana University Library, *Nations and nationalism*](https://iucat.iu.edu/iub/4060999). Bosworth's representation of his position remains the authority for the argument.
- **Language estimates:** Bosworth quotes about 6,800 languages and 230 states; these are **figures cited in his period**, not verified counts for 2026.
- **Historical language standardization:** the original calls certain modern languages “invented”; the rewrite explains their deliberate promotion, revival or standardization in nation-building, avoiding the inaccurate impression that earlier speakers and varieties did not exist.
- **European socialism:** the simplified guide presents the broad tension correctly, but Bosworth's specific 1914 German parliamentary example and Stalin's Russian wartime-patriotic usage are essential and retained.
- **Jewish history:** no antisemitic conspiracy or racial description is presented as fact. These are explicitly treated as perpetrators' false assertions and Bosworth's analysis of exclusion.
- **Current relevance:** the guide's generic climate-change/international-cooperation discussion does not appear as an independent chapter argument in the primary source and was not inserted into the edited chapter. The opening of the author's post-1945 section is explained as a historical thesis, not a forecast made today.

## Structural and regression obligations

- One `.chapter-source` root, official Chapter 02 metadata and seven intact `s1`–`s7` section keys plus `revision`.
- Six semantic note kinds retained (`concept`, `def`, `memory`, `hy`, `mistake`, `tip`), all linked to real sections.
- Exactly 14 unique first-use `button.glossary-term[data-definition]` elements; the revision glossary has 14 matching rows.
- No duplicate definition-only sidebar title for a glossary term; the shared validator enforces this.
- The Chapter 01 source/module, CSS, reader UI, and all other chapters remain unchanged on the new review branch. All changes are Chapter 02 + supporting tests and documentation + derived `index.html` and versioned service worker.
- The Chapter 01 smoke test's total glossary count must increase from 14 to 28 because Chapter 02 now contributes 14 more; add a chapter-specific popup/print-reference assertion.
- Build/rebuild and browser regression should be run in repository GitHub Actions before accepting or merging. Review print packing and visual diffs independently; no font shrinking or compositor retuning merely to fit a page target.

**Editorial measure of success:** a student can explain *why* nationhood seems natural, *how* modern institutions taught it, *why* universalism struggled against it, and *what* Bosworth sees as its enduring contradiction. Reducing page count alone is not a success criterion.

## Responsive visual review (12 November 2026)

The GitHub Actions run `43164473757` passed source, build, structural, navigation, accessibility, touch, search and offline checks but flagged the 390px **Chapter 12** screenshot at **3.988% changed pixels**, marginally exceeding the unchanged 3.5% visual guardrail. The reference screenshot is of an **untouched chapter**, not Chapter 02. I downloaded and compared `phase-d-browser-evidence/screens/baseline/390-chapter.png` and `candidate/390-chapter.png` side by side. The header, chapter boundaries, thesis panel, title line breaks, year chips and Contents launcher coincide; changes are visible as text-edge rasterization rather than layout movement. The 320px, 768px, 1024px and 1440px chapter screenshots were under threshold, and there was no horizontal overflow at any tested width. Original CSS and compositor files were not edited.

The review is recorded in PR #18's discussion with the original GitHub Actions artifact reference, and the repository's existing `reviewed-visual-change` label was applied **after comparing the screenshots**. The label allows the existing CI rule to recognize a reviewed difference without changing the visual threshold or creating a design exception. The PR remains a **draft** awaiting editorial approval, irrespective of the eventual CI result.
