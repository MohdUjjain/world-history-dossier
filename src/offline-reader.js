/* World History Dossier — offline status, storage and edition updates.
 * Kept independent from the chapter/print engine; inlined by src/build.py.
 */
(() => {
  'use strict';
  const status = document.getElementById('offlineStatus');
  const keep = document.getElementById('offlineKeep');
  const editionId = document.getElementById('offlineEditionId');
  const checkButton = document.getElementById('offlineCheckUpdate');
  const checkResult = document.getElementById('offlineCheckResult');
  const notice = document.getElementById('editionUpdateNotice');
  const reload = document.getElementById('editionReloadBtn');
  const dismiss = document.getElementById('editionDismissBtn');
  const PREFIX = 'whd-edition-';
  // The offline-ready label reflects the executable book, not optional
  // social previews, icons, sitemap or the best-effort 404 fallback.
  const ESSENTIALS = ['./index.html', './manifest.webmanifest'];
  let registration = null;
  let hadController = Boolean(navigator.serviceWorker && navigator.serviceWorker.controller);
  let updateShown = false;
  let lastUpdateCheck = 0;
  let preparingFonts = false;
  let checkingManually = false;

  const say = (message) => { if (status) status.textContent = message; };
  const reportCheck = (message) => { if (checkResult) checkResult.textContent = message; };
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
    if (checkButton) checkButton.hidden = true;
    if (editionId) editionId.textContent = 'Unavailable';
    return;
  }

  async function checkOffline() {
    if (!registration) return;
    try {
      const names = (await caches.keys()).filter((name) => name.startsWith(PREFIX));
      let ready = false, savedEdition = '';
      const scope = registration.scope;
      for (const name of names) {
        const cache = await caches.open(name);
        const results = await Promise.all(
          ESSENTIALS.map((path) => cache.match(new URL(path, scope).href))
        );
        if (results.every(Boolean)) {
          ready = true;
          savedEdition = name.slice(PREFIX.length);
          break;
        }
      }
      if (editionId) editionId.textContent = savedEdition || 'Not saved yet';
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

  async function checkForUpdates(manual = false) {
    if (manual && checkingManually) return;
    if (!registration) {
      if (manual) reportCheck('Offline reader setup is not ready yet.');
      return;
    }
    if (!navigator.onLine) {
      if (manual) reportCheck('You are offline. Connect to check for updates.');
      return;
    }
    // Background checks are throttled; deliberate checks always reach the worker.
    const now = Date.now();
    if (!manual && now - lastUpdateCheck < 60000) return;
    lastUpdateCheck = now;
    let updateFound = false;
    const onUpdateFound = () => {
      updateFound = true;
      if (manual) reportCheck('New edition found; preparing it for offline reading…');
    };
    if (manual) {
      checkingManually = true;
      if (checkButton) checkButton.disabled = true;
      reportCheck('Checking for a newer edition…');
    }
    registration.addEventListener('updatefound', onUpdateFound);
    try {
      await registration.update();
      if (manual) {
        await checkOffline();
        if (updateShown) reportCheck('Updated edition ready. Reload to read it.');
        else if (updateFound || registration.installing)
          reportCheck('An update is being prepared. You will be prompted when it is ready.');
        else reportCheck('No newer edition detected.');
      }
    } catch (_) {
      if (manual) reportCheck('Unable to check for updates. Try again when connected.');
    } finally {
      registration.removeEventListener('updatefound', onUpdateFound);
      if (manual) {
        checkingManually = false;
        if (checkButton) checkButton.disabled = false;
      }
    }
  }

  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (hadController) {
      showUpdate();
      reportCheck('Updated edition ready. Reload to read it.');
    }
    hadController = true;
    checkOffline();
    prepareFonts();
  });

  async function register() {
    try {
      registration = await navigator.serviceWorker.register('./service-worker.js', {
        scope: './', updateViaCache: 'none'
      });
      if (checkButton) checkButton.disabled = false;
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
  if (checkButton) checkButton.addEventListener('click', () => checkForUpdates(true));
  window.addEventListener('online', () => { checkForUpdates(); prepareFonts(); });
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) { checkOffline(); checkForUpdates(); }
  });
})();