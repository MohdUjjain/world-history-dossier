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
