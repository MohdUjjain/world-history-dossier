# Phase D — Comprehensive release verification

**Status:** Automated release candidate checks, run against the pull request
*before* merging to `main`. The public GitHub Pages site currently uses
branch-based publishing; this repository's PR workflow cannot by itself block
a direct push to `main`. **Require the check names below in GitHub branch
rules** to enforce the gate before deploying, and avoid merging while they
are pending or failing.

## What is checked

| Area | Automated gate | Evidence / acceptance rule |
| --- | --- | --- |
| Source integrity | `python src/build.py -o index.html --check`, structural + publication validators | 33 authored chapters, deterministic single HTML and content-hashed worker |
| Responsive interaction | `smoke_release_browser.py` and Phases A–C Playwright suites | 1440×900, 1024×768, 768×1024, 390×844, 320×720; no horizontal page overflow; accurate current chapter, modal focus |
| Accessibility | `smoke_release_accessibility.py` with pinned axe-core 4.10.3 | Scans cover, Chapter 00, desktop and phone Contents drawer; **zero serious or critical WCAG 2.0/2.1 A/AA findings**, saved JSON; keyboard/ARIA behavior is also exercised by the other browser suites |
| Visual regression | `smoke_release_browser.py --baseline` | Compares 17 deterministic viewport screenshots against the **PR base commit's** published HTML, not against a regenerated copy of the candidate. Differences greater than 3.5% changed pixels fail unless an intentional visual change is documented and explicitly approved. Uploads baseline, candidate, diff images |
| Range and summaries | `smoke_release_ranges.py`, Phases A–C tests | Strict rejection of malformed/unknown chapter ranges, reverse and repeated ranges, selected order and revision toggling, no stale print tree |
| Offline edition | Node `test_offline_cache.mjs` **and** real Chromium `smoke_release_offline.py` | Cache-first offline reopen with all 33 chapters, PDF excluded from PWA precache, atomic worker replacement, update banner without forced reload |
| Full 16:9 PDF | `validate_pdf_navigation.py` and `inspect_pdf_release.py` on **freshly regenerated candidate PDF** | All-page 16:9 geometry, no nearly blank pages or off-page text, 33 chapter bookmarks, 200+ section bookmarks; sampled cover/TOC/hero/body rendered images and diffs against the committed PDF |
| Documentation | `verify_docs_sync.py` | Living CSS/JS references include active roles; local release-document links resolve; source CSS, engine/reader/offline JS and CI changes must have corresponding docs changes in the same PR |

The existing chapter titles, note content, eight-pair color identities, revision
contrast roles and PDF pagination dimensions are not modified by Phase D.
Tests aim to catch regressions, not introduce new content.

The CI installs pinned axe-core 4.10.3 using a restored npm download cache and a bounded 150-second install, in a separate step from Chromium. This isolates upstream registry failures from website defects and prevents a hung package download from consuming the entire verification window.

## CI gate and screenshots

`.github/workflows/verify-pages.yml` supplies:

- **`verify`** — structural, PWA, live browser, axe accessibility,
  responsive screenshots, ordered export and documentation checks. Ordered
  range/screenshot tests run before the real-PWA update test, so a failed
  update check cannot prevent collection of other regression evidence.
  Pixel comparisons run against the PR-base HTML **on pull requests only**;
  production pushes still capture responsive screenshots but do not
  compare them with an arbitrarily different previous commit.
- **`release-pdf`** — on PR/manual dispatch, regenerates the full PDF with
  the actual browser print engine, checks its outline/page geometry and
  compares rasterized representative pages with the repository's current PDF.

The verification concurrency group is named `dossier-qa` (distinct from the earlier superseded experimental group), preserving per-PR cancellation while allowing the current gate to proceed without waiting on obsolete dependency-install jobs.

The workflow also uses per-PR `concurrency` with `cancel-in-progress` to stop superseded screenshot/PDF reviews when new commits land; only evidence from the latest commit should be considered release evidence.

The evidence directory is intentionally dot-prefixed (`.release-evidence/`); both artifact-upload steps explicitly opt into `include-hidden-files: true`. Without that option the browser PNGs/JSON are silently skipped even when the pixel comparisons succeed.

The job artifacts include `phase-d-browser-evidence` (candidate/baseline/
diff PNG files, accessibility JSON) and `phase-d-pdf-evidence` (sample PNGs,
contact sheet, diff masks and JSON).

**Required status checks for branch rules:**
`Verify World History Dossier website / verify` and
`Verify World History Dossier website / release-pdf`. GitHub displays the
exact job names under each PR. The installation of branch protection/rulesets
must be confirmed separately in repository settings; this documentation alone
does not protect the branch.

## Standard release sequence

1. Author on a feature branch; update `src/CSS_DOC.md` when `src/styles.css`
   changes and `src/JS_DOC.md` when `engine.js`, `reader-ui.js` or
   `offline-reader.js` changes.
2. Open a PR. Allow both checks to finish. Examine the uploaded screenshot
   contact sheets, accessibility report and PDF page samples.
3. If visual change is intentional, document it in the PR and manually
   inspect baseline, candidate and diff artifacts; do **not** simply increase
   the pixel-difference thresholds. Release scripts support an explicit
   `--allow-visual-change` switch only for separately approved runs; CI
   does not enable that switch by default.
4. Merge only after required checks pass and the screenshots/PDF pages have
   been reviewed. The existing GitHub Pages branch publisher then deploys.
5. Confirm the Pages deployment and the full bookmarked-PDF rebuild workflow
   succeeded. The PDF is intentionally a separate asset outside offline
   precaching; its later PDF-only commit can cause a second Pages deployment.
6. Use `verify_live_site.py` after deployment, and verify both online
   reader and PDF links resolve. The scheduled live-site check remains enabled.

## Local commands

From the repository root (with Chromium, Node, and Python 3.12 available):

```bash
python -m pip install playwright beautifulsoup4 lxml pymupdf pillow
python -m playwright install chromium
npm install --no-save --ignore-scripts --no-audit --no-fund axe-core@4.10.3

python src/build.py -o index.html --check
python src/tests/validate_structure.py
python src/tests/verify_publication.py
python src/tests/verify_docs_sync.py
node src/tests/test_offline_cache.mjs
python src/tests/smoke_reader_ui.py
python src/tests/smoke_phase_a.py
python src/tests/smoke_reader_interactions.py
python src/tests/smoke_phase_c.py
python src/tests/smoke_release_accessibility.py
python src/tests/smoke_release_browser.py
python src/tests/smoke_release_offline.py
python src/tests/smoke_release_ranges.py

python src/tools/export_full_pdf.py --book index.html \
  --out /tmp/dossier-candidate.pdf --batch-size 16 --chromium auto \
  --qa /tmp/dossier-qa.json
python src/tests/validate_pdf_navigation.py /tmp/dossier-candidate.pdf
python src/tests/inspect_pdf_release.py /tmp/dossier-candidate.pdf \
  --reference '20th-Century International History.pdf' \
  --out /tmp/dossier-pdf-evidence
```

For visual regression versus the PR base, first extract its `index.html`:

```bash
git fetch origin main
git show origin/main:index.html > /tmp/dossier-baseline.html
python src/tests/smoke_release_browser.py \
  --baseline /tmp/dossier-baseline.html --out /tmp/dossier-screens
python src/tests/verify_docs_sync.py --base origin/main
```

## Manual inspection that automation cannot replace

Confirm the phone/table scrolling feels natural with touch and that the
Contents modal is usable with a screen reader. Review representative 16:9
pages, especially the cover, full-width tables, section side notes and
revision transitions; note that automated bounding-box checks do not prove
all typography is subjectively legible. Verify archive dates, rights, captions
and underlying sources before adding any historical illustrations.

For a change to the 245-page source edition, compare the full candidate PDF
to the committed edition using both the visual evidence and the structural
QA report. A newly intentional page-count difference requires a documented
editorial review rather than bypassing the check silently.

## Batch 1 — correctness and resilience cross-repository regression

The release workflow runs `node src/tests/test_optional_precache.mjs`
after the established cache lifecycle suite. It deliberately fails one
optional social-preview fetch and asserts that the complete reader still
activates; it separately rejects a missing core `index.html` and confirms
that the previous edition is not replaced.

`python src/tests/smoke_batch1_dialog_notices.py` runs in desktop and
390px mobile Chromium, seeds an actual saved reading position, verifies
background inertness and focus restoration while the Contents modal is open,
then reproduces an edition notification through consecutive service-worker
`controllerchange` events. The update notice must take priority over the
resume card; dismissing the update returns the resume suggestion without
clearing the saved checkpoint. Both tests are regression gates, not visual
redesign work. A failed optional asset must not be misreported as an
incomplete offline book, and preserving the previous install remains
mandatory when core precaching fails.

## Batch 2 — continuity regression fixtures (November 2026)

`src/tests/fixtures/batch2_modified_edition.json` models a saved section
anchor absent in an updated edition but with its chapter identity intact.
`python src/tests/smoke_batch2_continuity.py` tests that Continue Reading
falls back within the surviving chapter, then verifies that hiding summaries
does not overwrite the saved chapter or strand the reading viewport.
These are browser-driven, real DOM checks on mobile and desktop. The workflow
now verifies stacked PRs targeting the Batch 1 review branch as well as PRs
targeting `main`; this avoids bypassing CI while the batches remain unmerged.

## Explicit approval of intentional screenshot changes

A product-design PR may intentionally alter the Contents drawer and exceed the 3.5% screenshot-diff gate. Inspect the uploaded **baseline**, **candidate**, and **diff** screenshots for every affected viewport first. Only after verifying that the visual change is intentional, label that PR **`reviewed-visual-change`**. The workflow then supplies `--allow-visual-change` for that labelled pull request only, and still captures the complete before/after/diff evidence and records `manualApproval: true`. All unlabelled PRs retain the original strict 3.5% gate. Remove the label if further unrelated changes invalidate the review.

For Batch 3, visual review of the 6 November 2026 evidence showed that the changes are restricted to the Contents drawer (search-scope explanation and saved-edition/update controls): cover, chapter and table screenshots are unchanged. The approved drawer deltas were 3.68% at 1024px, 5.21% at 768px, 9.94% at 390px and 11.40% at 320px. No PDF or chapter layout change is approved by this exception.
