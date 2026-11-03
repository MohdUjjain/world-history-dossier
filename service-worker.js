/* World History Dossier — small, scoped offline reader.
   Do not precache the full PDF: it is a separate, optional download. */
const CACHE_VERSION = 'whd-reader-v1';
const APP_SHELL = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) => Promise.all(
      names.filter((name) => name.startsWith('whd-reader-') && name !== CACHE_VERSION)
        .map((name) => caches.delete(name))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin || !url.pathname.startsWith(new URL(self.registration.scope).pathname)) return;

  // Always request fresh HTML when online, but allow offline reading after a visit.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).then((response) => {
        if (response.ok) {
          const cacheCopy = response.clone();
          event.waitUntil(caches.open(CACHE_VERSION).then((cache) => cache.put('./index.html', cacheCopy)));
        }
        return response;
      }).catch(async () => (await caches.match('./index.html')) || Response.error())
    );
    return;
  }

  // Leave the large PDF outside the automatic offline cache.
  if (url.pathname.toLowerCase().endsWith('.pdf')) return;
  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request).then((response) => {
      if (response.ok) {
        const copy = response.clone();
        event.waitUntil(caches.open(CACHE_VERSION).then((cache) => cache.put(request, copy)));
      }
      return response;
    }))
  );
});
