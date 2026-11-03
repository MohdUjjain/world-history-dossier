# Installable World History Dossier (PWA)

The published GitHub Pages reader is a **Progressive Web App** (PWA), not a native Android/iOS/Windows executable. Installation gives it an app icon and, in supporting browsers, its own standalone window while preserving the existing chapter navigation and PDF-export controls.

## Install on your device

- **Chrome / Edge on desktop:** Open https://mohdujjain.github.io/world-history-dossier/ and use the install icon in the browser address bar, or the browser's menu item to install the site as an app. Chrome/Edge may wait until the page meets engagement and installability criteria before showing an automatic prompt.
- **Chrome on Android:** Open the site and choose **Install app** or **Add to Home screen** from the browser's menu.
- **iPhone / iPad:** Open the site, tap the Share menu and select **Add to Home Screen**. Installation prompts differ across browser and iOS versions.
- **Firefox:** Native PWA-install behavior varies by platform; on desktop, a full browser-managed install prompt may not be available.

The browser controls whether and when an install affordance is shown. A manifest cannot force an automatic installation.

## Files and GitHub Pages scope

- `/manifest.webmanifest`: app name, start URL, scope, theme and icons.
- `/icons/icon-192.png` and `/icons/icon-512.png`: navy/parchment/gold app icons sized for installability.
- `/service-worker.js`: root-scoped offline reader cache, versioned as `whd-reader-v1`.
- `/src/shell.html`: canonical HTML source for the manifest link, Apple touch metadata, and service-worker registration; rebuilding `index.html` preserves the integration.
- `/index.html`: published standalone reader, assembled with `python src/build.py -o index.html`.

The manifest uses `id: /world-history-dossier/`, and relative `start_url: ./` and `scope: ./` to remain within the GitHub Pages **project path**. Do not change these to `/`: that would refer to the account's top-level site, not this repository.

## Offline behavior and updates

After a successful online visit, the service worker pre-caches the entire self-contained reader, manifest and app icons. When offline, navigating to the installed site serves the cached reader, so its 33 chapters and local interactions remain accessible. Export/print behavior still depends on the installed browser's printing capabilities.

The pre-rendered PDF (`20th-Century International History.pdf`) is **not** automatically cached; users can download it separately when online. Other external links still require connectivity.

The worker uses **network-first for HTML navigation**, so online visits fetch the latest reader; its cached fallback supports offline use. When changing the list of pre-cached files or offline behavior, update the cache version in `service-worker.js` and retest. Changes to `src/styles.css` or `src/engine.js` must still update the adjacent `CSS_DOC.md` or `JS_DOC.md` in the same commit.

## Deployment verification

1. After pushing to `main`, verify `/manifest.webmanifest`, `/service-worker.js`, and both PNG icons return HTTP 200 on the site.
2. In Chrome/Edge DevTools → **Application**, confirm manifest details, 192/512 icons, and an active service worker scoped to `/world-history-dossier/`.
3. Reload once online; then turn off network access in DevTools and reload. The reader should still display all 33 chapters.
4. Use the browser's **Install app** menu or address-bar control, where supported. On iOS, test **Add to Home Screen**.
5. Verify the original site, Open Graph preview and chapter-order PDF-export controls still work.

Chrome may require user engagement before displaying its install suggestion. Do not confuse a browser shortcut with full PWA installation on platforms whose browser support differs.
