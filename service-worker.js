/* World History Dossier — atomic, content-hashed offline reader.
 * Google Fonts: optional cache of fetched responses, no bundled font files.
 * The pre-rendered PDF is deliberately not precached.
 */
const CACHE_PREFIX = 'whd-edition-';
const CACHE_NAME = CACHE_PREFIX + '4e71995d6d08';
const FONT_CACHE = 'whd-google-fonts-v1';
// The flowing HTML book is a required atomic unit; auxiliary web metadata
// and imagery must never block a complete edition from being installed.
const CORE_ASSETS = ['./index.html', './manifest.webmanifest'];
const OPTIONAL_ASSETS = [
  './icons/icon-192.png', './icons/icon-512.png', './og-image.jpg',
  './404.html', './sitemap.xml', './robots.txt'
];
const SCOPE = new URL(self.registration.scope);

function isGoogleFont(url) {
  return url.protocol === 'https:' &&
    ((url.hostname === 'fonts.googleapis.com' && url.pathname.startsWith('/css2')) ||
     (url.hostname === 'fonts.gstatic.com' && url.pathname.startsWith('/s/')));
}

self.addEventListener('install', (event) => {
  // An incomplete core never replaces a working older edition.
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await cache.addAll(CORE_ASSETS);
    await Promise.allSettled(OPTIONAL_ASSETS.map(path => cache.addAll([path])));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter((name) =>
      (name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME) ||
      name === 'whd-reader-v1' // one-time cleanup of the original PWA cache
    ).map((name) => caches.delete(name)));
    // Keep the Google Fonts cache and all other applications' caches intact.
    await self.clients.claim();
  })());
});

self.addEventListener('message', (event) => {
  if (!event.data || event.data.type !== 'PREPARE_FONTS') return;
  event.waitUntil((async () => {
    const raw = Array.isArray(event.data.urls) ? event.data.urls.slice(0, 40) : [];
    const permitted = [...new Set(raw.filter((s) => typeof s === 'string' && s.length < 2048))]
      .map((s) => { try { return new URL(s); } catch (_) { return null; } })
      .filter((url) => url && isGoogleFont(url));
    const cache = await caches.open(FONT_CACHE);
    await Promise.allSettled(permitted.map(async (url) => {
      if (await cache.match(url.href)) return;
      const response = await fetch(url.href, {
        mode: url.hostname === 'fonts.gstatic.com' ? 'cors' : 'no-cors',
        credentials: 'omit'
      });
      if (!response.ok && response.type !== 'opaque') return;
      await cache.put(url.href, response);
    }));
  })());
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  if (isGoogleFont(url)) {
    event.respondWith((async () => {
      const cache = await caches.open(FONT_CACHE);
      const saved = await cache.match(request);
      if (saved) return saved;
      try {
        const fresh = await fetch(request);
        if (fresh.ok || fresh.type === 'opaque') {
          event.waitUntil(cache.put(request, fresh.clone()));
        }
        return fresh;
      } catch (_) { return Response.error(); }
    })());
    return;
  }

  if (url.origin !== SCOPE.origin || !url.pathname.startsWith(SCOPE.pathname)) return;
  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      if (url.pathname === SCOPE.pathname || url.pathname === SCOPE.pathname + 'index.html') {
        // Cache-first keeps an entire edition coherent until the user reloads
        // after a successful update; avoids mixing old and new chapter markup.
        const saved = await cache.match('./index.html');
        if (saved) return saved;
      }
      try { return await fetch(request); }
      catch (_) {
        return (await cache.match('./404.html')) || Response.error();
      }
    })());
    return;
  }
  if (url.pathname.toLowerCase().endsWith('.pdf')) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const saved = await cache.match(request);
    return saved || fetch(request);
  })());
});