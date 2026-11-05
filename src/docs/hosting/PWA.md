# Installable World History Dossier — Offline and publication guide

The GitHub Pages reader is a Progressive Web App (PWA), not a native operating-system executable. Its complete HTML book is self-contained and can reopen without internet after a successful initial online visit. The separate 245-page bookmarked PDF is not automatically saved to Cache Storage.

## Install

- Chrome / Edge desktop: Open https://mohdujjain.github.io/world-history-dossier/ and use the browser's Install app action.
- Chrome Android: Browser menu → Install app or Add to Home screen.
- iPhone/iPad: Share → Add to Home Screen, subject to browser and OS support.
- Other browsers: Installation support varies; a manifest cannot force an install prompt.

## Offline readiness and edition updates

The Contents drawer has an **Offline edition** section. Once all eight essential assets are saved, it displays an offline-ready status. The **Keep on this device** button invokes the user-initiated navigator.storage.persist() request where supported. Persistence reduces eviction risk, but the user or operating system can still clear site data.

The app checks for updates on an online launch, when it returns to the foreground, or when connectivity resumes, at most once per minute. A new worker is allowed to activate **only after every required resource is cached**. A controllerchange event announces **Updated edition saved**, with Reload now and Later buttons; the currently open page is never forcibly refreshed.

An interrupted download leaves the previous complete edition intact. The initial migration from the first, unnotified PWA version may require an ordinary reload before the new notification interface is available; subsequent releases are announced.

The main book is self-contained: all 33 chapters and their interactive tools are offline. Browser-generated PDF printing is browser-dependent. The pre-rendered PDF remains a separate online download unless the user saves it manually. Unknown URLs have a cached branded 404 fallback when offline.

## Source and generated files

| Location | Responsibility |
| --- | --- |
| src/shell.html | Screen markup for offline status and update notice, with the offline-script injection marker |
| src/styles.css | Screen-only status/notice CSS; CSS_DOC.md must be updated in the same change |
| src/offline-reader.js | Registration, offline-ready status, persistent storage request, update checks and banner |
| src/service-worker.template.js | Atomic precache, cache cleanup, optional Google Fonts cache |
| src/build.py | Compiles HTML and emits the content-hashed service-worker.js |
| service-worker.js | Generated artifact; do not hand-edit |
| manifest.webmanifest, icons/ | PWA identity and app icons |
| 404.html, sitemap.xml, robots.txt | Friendly errors and website discoverability |
| .github/workflows/verify-pages.yml | Push/PR checks and weekly/manual live-site checks |
| src/tests/verify_publication.py | Site metadata, source, images, navigation and assets |
| src/tests/test_offline_cache.mjs | Simulated offline reopening, atomic update and font-cache test |
| src/tests/verify_live_site.py | Weekly/manual check of the deployed public URLs |

The manifest uses the GitHub Pages project ID /world-history-dossier/ with relative start_url and scope of ./ . Do not switch these to the account root.

## Content-hashed offline cache

The publishing builder calculates Git blob SHA-1 values for the assembled index.html and each small public file, then computes SHA-256 over the ordered path/hash listing. The first twelve hexadecimal characters replace __REVISION__ in the service worker template, giving a cache name like whd-edition-012345abcdef.

Any edit to the book, screen CSS, engine, metadata, icons, 404 page, sitemap, robots file or worker template therefore changes the edition identity automatically. The large PDF is not part of that hash: changing the PDF does not force readers to redownload the entire book.

A failed/incomplete install does not call skipWaiting, leaving the old cache active. Successful activation deletes only older whd-edition-* caches and the original whd-reader-v1 cache, retaining other 11AM applications and the optional Google Fonts cache.

Main-page navigation serves the saved complete HTML without network access. Opening the app online checks for newer service workers; after the next edition has installed, a banner invites a reload to switch the visible tab to it.

## Optional offline Google Fonts caching

The dossier's typography currently uses Georgia, Trebuchet MS, Times New Roman and system fallbacks: **it has no Google Fonts dependency**. The worker nonetheless supports saving legitimate Google Fonts responses only if a future edition requests them:

- https://fonts.googleapis.com/css2... (style sheets)
- https://fonts.gstatic.com/s/... (font files)

Only responses actually obtained from these approved domains are cached, in whd-google-fonts-v1. No Google font binaries are distributed with the source repository. Font warming is optional and never prevents opening the book. Browser caching and provider terms still apply.

## Rebuild and verification

From the repository root, run:

    python src/build.py -o index.html
    python src/build.py -o index.html --check
    python src/tests/validate_structure.py
    python src/tests/verify_publication.py
    node src/tests/test_offline_cache.mjs

The strict --check command fails if either the compiled index.html or generated service-worker.js is stale. The verify-pages GitHub Actions workflow runs those checks on each push and PR, and additionally checks the live GitHub Pages URLs weekly and on manual dispatch.

Manual device check: open the website online, wait for the Contents drawer to say All 33 chapters saved offline, switch to airplane mode, close and reopen the installed reader. The entire dossier should still be readable. After a future release, the active tab should show a new-edition notification once the update has fully downloaded.

Because this is a project site under a github.io subpath, its robots.txt is a helpful published reference but is not the origin-root /robots.txt that crawlers ordinarily consult. The XML sitemap can still be submitted directly to a search console.

## Boundaries

Browser PWA storage is not permanent device storage; clearing site data removes the saved reader. The separate full PDF is not precached. The update UI is hidden from printed pages and does not modify chapter modules or the 16:9 print engine.
