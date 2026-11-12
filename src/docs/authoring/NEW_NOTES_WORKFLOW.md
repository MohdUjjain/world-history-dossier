# NEW_NOTES_WORKFLOW.md — replacement notes contract

## Editorial reset

The user explicitly rejected the previous long notes as too lengthy. This
relaunch deliberately archives, rather than builds, the older chapter texts.
The next submitted, shorter chapter notes become the chapter's primary text.
**Do not resurrect or merge older notes without asking.**

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

