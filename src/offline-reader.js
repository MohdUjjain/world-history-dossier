/* World History Dossier — offline status, storage and edition updates.
 * Kept independent from the chapter/print engine; inlined by src/build.py.
 */
(() => {
  'use strict';
  const status = document.getElementById('offlineStatus');
  const keep = document.getElementById('offlineKeep');
  const notice = document.getElementById('editionUpdateNotice');
  const reload = document.getElementById('editionReloadBtn');
  const dismiss = document.getElementById('editionDismissBtn');
  const PREFIX = 'whd-edition-';
  const ESSENTIALS = [
    './index.html', './manifest.webmanifest', './icons/icon-192.png',
    './icons/icon-512.png', './og-image.jpg', './404.html',
    './sitemap.xml', './robots.txt'
  ];
  let registration = null;
  let hadController = Boolean(navigator.serviceWorker && navigator.serviceWorker.controller);
  let updateShown = false;
  let lastUpdateCheck = 0;
  let preparingFonts = false;

  const say = (message) => { if (status) status.textContent = message; };
  // Edition notifications take priority over the optional resume card.
  // This only changes screen notice visibility, never the stored bookmark.
  const notifyEdition = (visible) => {
    if (notice) notice.hidden = !visible;
    document.dispatchEvent(new CustomEvent('whd:edition-notice', {
      detail: {visible}
    }));
  };
  const showUpdate = () => {
    if (updateShown) return;
    updateShown = true;
    notifyEdition(true);
    say('A new edition is ready. Reload to read it.');
  };
  if (reload) reload.addEventListener('click', () => location.reload());
  if (dismiss) dismiss.addEventListener('click', () => notifyEdition(false));

  if (!('serviceWorker' in navigator) || !('caches' in window)) {
    say('This browser does not support saving the reader offline.');
    if (keep) keep.hidden = true;
    return;
  }

  async function checkOffline() {
    if (!registration) return;
    try {
      const names = (await caches.keys()).filter((name) => name.startsWith(PREFIX));
      let ready = false;
      const scope = registration.scope;
      for (const name of names) {
        const cache = await caches.open(name);
        const results = await Promise.all(
          ESSENTIALS.map((path) => cache.match(new URL(path, scope).href))
        );
        if (results.every(Boolean)) { ready = true; break; }
      }
      const persistent = Boolean(navigator.storage && navigator.storage.persisted &&
        await navigator.storage.persisted());
      if (keep) {
        keep.disabled = !ready || persistent;
        keep.textContent = persistent ? 'Stored with extra protection' : 'Keep on this device';
      }
      if (!updateShown) {
        say(ready ? (persistent ?
          'All 33 chapters saved offline. Persistent storage enabled.' :
          'All 33 chapters saved offline. Your browser may clear site data.') :
          'Preparing all 33 chapters for offline reading…');
      }
    } catch (_) {
      say('Offline storage status could not be checked on this device.');
    }
  }

  if (keep) keep.addEventListener('click', async () => {
    keep.disabled = true;
    try {
      const granted = Boolean(navigator.storage && navigator.storage.persist &&
        await navigator.storage.persist());
      await checkOffline();
      if (!granted) say('Reader saved offline; persistent storage was not granted. Avoid clearing site data.');
    } catch (_) {
      say('Reader remains cached, but persistent storage is not available here.');
    }
    if (keep.textContent !== 'Stored with extra protection') keep.disabled = false;
  });

  async function prepareFonts() {
    if (preparingFonts || !navigator.onLine || !navigator.serviceWorker.controller) return;
    preparingFonts = true;
    try {
      const urls = new Set();
      document.querySelectorAll('link[href^="https://fonts.googleapis.com/"]').forEach(
        (link) => urls.add(link.href)
      );
      if (performance && performance.getEntriesByType) {
        performance.getEntriesByType('resource').forEach((res) => {
          if (/^https:\/\/fonts\.(googleapis|gstatic)\.com\//.test(res.name)) urls.add(res.name);
        });
      }
      // The current book uses local/system fonts: normally there are no URLs.
      if (urls.size) navigator.serviceWorker.controller.postMessage({
        type: 'PREPARE_FONTS', urls: [...urls].slice(0, 40)
      });
    } catch (_) { /* Optional font caching never blocks the local reader. */ }
    preparingFonts = false;
  }

  async function checkForUpdates() {
    if (!registration || !navigator.onLine) return;
    const now = Date.now();
    if (now - lastUpdateCheck < 60000) return;
    lastUpdateCheck = now;
    try { await registration.update(); } catch (_) { /* Offline usage remains safe. */ }
  }

  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (hadController) showUpdate();
    hadController = true;
    checkOffline();
    prepareFonts();
  });

  async function register() {
    try {
      registration = await navigator.serviceWorker.register('./service-worker.js', {
        scope: './', updateViaCache: 'none'
      });
      await navigator.serviceWorker.ready;
      await checkOffline();
      checkForUpdates();
      prepareFonts();
      if (registration.installing) {
        registration.installing.addEventListener('statechange', checkOffline);
      }
    } catch (error) {
      say('Offline setup failed. Reopen the reader online to retry.');
      console.warn('Offline registration failed:', error);
    }
  }
  if (document.readyState === 'complete') register();
  else window.addEventListener('load', register, {once:true});
  window.addEventListener('online', () => { checkForUpdates(); prepareFonts(); });
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) { checkOffline(); checkForUpdates(); }
  });
})();