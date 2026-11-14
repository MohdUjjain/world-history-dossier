# NEW_NOTES_WORKFLOW.md — replacement notes contract

## Editorial reset

The user explicitly rejected the previous long notes as too lengthy. This
relaunch deliberately archives, rather than builds, the older chapter texts.
The next submitted, shorter chapter notes become the chapter's primary text.
**Do not resurrect or merge older notes without asking.**

## Current programme: original-source-grounded teaching revision (November 2026)

**This takes precedence over the earlier concise-brief rule above whenever an original academic textbook chapter is available.** The earlier reset explains how the 33-chapter baseline was assembled; it is not the source-of-truth rule for the deeper chapter-by-chapter refinement now being undertaken.

### Source hierarchy

1. **Original academic chapter** — authoritative for the historian’s thesis, argument order, evidence, dates, terminology, interpretation and qualifications.
2. **`11- 20TH CENTURY HISTORY.pdf` simplified course guide** — reference for accessible phrasing and common student comprehension difficulties; never an authority for an unsupported claim or a correction to the academic chapter.
3. **Existing `src/chapters/chNN.html`** — the text and semantic architecture to improve while keeping stable section anchors, six sidebar categories, reading interaction, revision toggles and print fidelity.

If the academic chapter is unavailable, do not label the work a three-source verification or silently substitute general historical knowledge. Keep the existing chapter intact until a source-grounded pass can be made. Clearly identify any provisional audit based only on the current notes and simplified guide.

### Seven editorial commitments

1. **Original-source authority** — reconstruct what the specific author argues and how evidence supports it.
2. **Terminological fidelity** — keep academic terms such as *imperial power*, *collective security* or *informal empire*, even when explaining the surrounding sentence in simpler language.
3. **Accessible prose** — shorter, explicit causal sentences; define unfamiliar terms at first meaningful mention with the existing dotted-underline popup mechanism rather than repeated parentheses.
4. **Causal completeness** — explain *what, why, how and with what consequence*, not just a list of events.
5. **Conceptual closure** — return to the problem introduced in a paragraph, section or chapter when its resolution is educationally important. Close the causal circle rather than repeating the opening mechanically.
6. **Intelligent compression** — remove duplicated exposition, not distinct evidence, qualifications, examples or reasoning. No hard five-page or word-count cutoff: learning quality determines length.
7. **Source-grounded verification** — check chronology, actors, substantive claims, interpretive limitations, omitted links and source disagreements before approving.

### Five-stage editorial process

1. Reconstruct the original author’s complete intellectual progression and the evidence behind it.
2. Compare original PDF, simplified guide and existing chapter module; flag gaps, overstatements and misconceptions.
3. Rewrite for understandable, terminologically faithful teaching and explicit conceptual closure.
4. Audit **semantic** repetition across hero, main notes, popup terms, sidebar aids, tables and revision material.
5. Verify again against the original and record what was removed, changed, corrected, retained deliberately and tested in `src/docs/editorial/CHNN_SOURCE_GROUNDED_EDITION.md`.

### One conceptual owner per layer

- **Hero/opening:** orientation and one clear central argument; do not repeat the full hero roadmap in the first main paragraph.
- **Main notes:** a self-contained explanation of historical causes, mechanisms, evidence, comparisons, limitations and consequences.
- **First-use popups:** short, faithful academic definitions that do not disrupt sentence flow.
- **Sidebar:** a distinct operation—comparison, application, classification, memory cue, misconception diagnosis or examination technique. Remove any fact-only card that merely restates nearby prose.
- **Revision:** independent recall and a print-safe terminology reference. Repetition is purposeful when the learning task changes, but whole explanations should not be copied.

Structural validation rejects identical popup/definition-sidecard terms; a **human semantic audit** remains required because reworded duplication is not detectable by name matching. Count and describe removals and rewritten cards in the chapter’s editorial record.

**Print policy:** Keep the existing opt-in revision glossary as the source of definitions when printing with revision content. Printing with revision material disabled follows the established current behavior; do not reintroduce parenthetical definitions in the main notes or alter the compositor without a separate requirement.

## Processing each pasted chapter

1. Read the full pasted chapter notes. Retain their academic content, names,
   dates, distinctions, emphasis, examples and wording where possible. Do not
   invent missing claims or add background facts from outside the user's text.
2. Organize the supplied material into a readable heading hierarchy and
   identify genuinely useful sidebar callouts (definitions, key concepts,
   exam tips, mistakes, memory aids, high-yield points) **without duplicating
   long stretches of the narrative**. A callout can quote a short supplied
   phrase or summarize a point clearly attributed to the supplied text.
3. Store each chapter as `chapters/chNN.html` with one chapter-source root.
   The `.src-main` container carries the uninterrupted explanation.
   The `.src-side` container carries concepts and other supporting callouts.
   This is the first choice; the JS `normalizedStreams()` fallback also
   catches any accidentally main-column `data-kind="concept"` blocks.
4. Keep the chapter's identity palette and revision contrast colour. If the
   pasted notes include a revision section, mark its first `section-head`
   with `data-revision-start="true"` in `.src-main`; set the matching first
   revision sidebar block marker when one exists. Use these markers to keep
   the revision toggle and new-print-page rule intact.
5. Don't automatically append all six long legacy revision sections just to
   follow the old template. Prefer concise useful revision content and only
   what the user provided or explicitly asks to generate.
6. Rebuild the single-file HTML with `python3 src/build.py`. Check the
   screen view, large-print TOC, sidebar concept placement, revision toggle,
   export order, and PDF overflow (print media). Correct issues before
   marking the chapter complete.
7. Update `CSS_DOC.md` in the same change as `styles.css`, and `JS_DOC.md` in
   the same change as `engine.js`. Merely adding a chapter should not require
   changing either shared file.

## Formatting contract

The current project uses: flowing HTML reading view, 1280×720 true 16:9 PDF,
chapter-specific main/contrast colours, six fixed semantic callout colours,
sidebar export controls, flexible chapter ordering and optional revision.
No external pagination, PDF or UI JavaScript libraries.

## Missing information

If a future pasted chapter supplies no author, publication title or other
metadata, ask only if essential, or keep that field neutral/absent. Never
invent bibliographic details or citations. Do not infer claims from the old
longer chapter while writing the new one.

## Official chapter headings (November 2026 update)

Read `chapter_catalog.json` BEFORE authoring any new chapter. The user
provided the complete textbook contents, 00–32. The catalogue fixes the
chapter numbering and its official chapter title, which must appear as the
primary H1 and as the chapter-level item in HTML navigation and PDF contents.
The user's more expressive **notes title** is distinct: place it as a
secondary hero subtitle (`data-subtitle` and `.hs`) only, if useful.
Do not replace the official title in `data-title` with the notes title.
The contents shows only chapters whose files have been supplied and authored;
future chapters in the catalogue are not clickable, imaginary pages.
For example, chapter 01 is officially **Imperialism**, while its notes subtitle
remains **The Imperial Century — Rise, Crisis, and the Global Transition to the
Nation-State**. Chapter 00 carries the full official Introduction heading.

## Contextual definitions: one concept, one explanatory owner

For each chapter written from the original source, preserve the author's
essential terms. On **first meaningful use only**, an unfamiliar technical
term can receive a dotted-underline glossary button with a short plain-language
definition on hover, click, touch tap or keyboard focus. Do not sprinkle the
same tooltip over repeated occurrences.

**Avoid redundant learning aids:** when the popup defines a term, do not add
a `data-kind="def"` sidebar card merely repeating the same definition.
Keep a sidebar card on that topic only when it performs a *different* task:
a causal explanation, instructive comparison, worked example, historical
qualification, memory sequence, or exam application. If it adds no new
learning value, remove it rather than replacing it with decorative wording.
A sidebar definition for another term with **no popup** is still appropriate.

The chapter's revision glossary is a deliberate exception: its compact
definitions enable independent examination review and ensure that printing
the dossier does not make meanings disappear. It must not substitute for the
main narrative's explanations of cause and effect. Before release, compare
all popup terms with sidebar definition titles, review any near-matches
semantically, and run `python src/tests/validate_structure.py`. The
structural check rejects the same named term in both a popup and a
sidebar definition card (ignoring an initial "the", "a" or "an").

### Semantic duplication review beyond exact matches

Automated validation catches identical glossary-term and sidebar-definition titles, not repeated *teaching functions*. Compare each sidebar to the main paragraph, opener, tables and revision material. Remove fact/number/conclusion recaps; repurpose cards into applications, instructive comparisons or mistake checks when supported by the primary text. Keep purposeful memory transformations, exam cautions and the print-revision glossary. Ask **whether each repeated concept performs a distinct intellectual operation**, not merely whether its wording differs. Never delete the main explanation just to preserve a callout.

