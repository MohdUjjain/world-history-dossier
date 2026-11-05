/* World History Dossier service worker: offline/atomic version tests (Node >=20).
   No external packages, browser sessions, or network connections. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const code = readFileSync(new URL('../../service-worker.js', import.meta.url), 'utf8');
const scope = 'https://mohdujjain.github.io/world-history-dossier/';
const urlOf = (x) => new URL(typeof x === 'string' ? x : x.url, scope).href;

function simulate(breakInstall = false) {
  const handlers = new Map();
  const stores = new Map();
  let online = true;
  let fetches = 0;
  let skipCount = 0;
  let claimCount = 0;
  const serverFetch = async (request) => {
    fetches++;
    const url = urlOf(request);
    if (!online) throw Error('offline');
    if (breakInstall && url.endsWith('/404.html')) throw Error('interrupted download');
    return new Response(url.endsWith('/index.html') ? 'FULL 33-CHAPTER READER' : 'asset: ' + url);
  };
  class MockCache {
    constructor() { this.data = new Map(); }
    async addAll(paths) {
      for (const path of paths) await this.put(path, await serverFetch(path));
    }
    async put(request, response) {
      this.data.set(urlOf(request), response.clone());
    }
    async match(request) {
      const r = this.data.get(urlOf(request));
      return r && r.clone();
    }
  }
  const caches = {
    async open(name) {
      if (!stores.has(name)) stores.set(name, new MockCache());
      return stores.get(name);
    },
    async keys() { return [...stores.keys()]; },
    async delete(name) { return stores.delete(name); },
  };
  const self = {
    registration: {scope},
    addEventListener(type, fn) {handlers.set(type, fn);},
    async skipWaiting() {skipCount++;},
    clients: {async claim() {claimCount++;}},
  };
  vm.runInNewContext(code, {
    self, caches, fetch: serverFetch, URL, Response, Promise, Set,
  }, {filename: 'service-worker.js'});
  async function dispatch(type, attrs = {}) {
    let waiting = [];
    let responding;
    const event = {
      ...attrs,
      waitUntil(value) {waiting.push(Promise.resolve(value));},
      respondWith(value) {responding = Promise.resolve(value);},
    };
    handlers.get(type)(event);
    await Promise.all(waiting);
    if (responding) return responding;
  }
  return {stores, caches, dispatch, setOnline(v) {online=v;},
    stats() {return {skipCount,claimCount,fetches};}};
}

const ok = simulate();
await ok.caches.open('11am-hikam-reader-untouched');
await ok.caches.open('whd-google-fonts-v1');
await ok.caches.open('whd-edition-prior');
await ok.caches.open('whd-reader-v1');
await ok.dispatch('install');
const current = [...ok.stores.keys()].find(n => /^whd-edition-[0-9a-f]{12}$/.test(n));
assert.ok(current, 'Cache name must use the content hash');
assert.equal(ok.stats().skipCount, 1, 'New edition activated only after complete download');
assert.equal(ok.stores.get(current).data.size, 8, 'All essential assets are saved');
await ok.dispatch('activate');
assert.equal(ok.stores.has('whd-edition-prior'), false, 'Old edition cleared');
assert.equal(ok.stores.has('whd-reader-v1'), false, 'Legacy cache cleared');
assert.ok(ok.stores.has('11am-hikam-reader-untouched'), 'Sibling app left untouched');
assert.ok(ok.stores.has('whd-google-fonts-v1'), 'Font cache survives editions');
assert.equal(ok.stats().claimCount, 1);

ok.setOnline(false);
const priorCalls = ok.stats().fetches;
const saved = await ok.dispatch('fetch', {
  request: {method:'GET',mode:'navigate',url:scope},
});
assert.equal(await saved.text(), 'FULL 33-CHAPTER READER');
assert.equal(ok.stats().fetches, priorCalls, 'Offline reader must not fetch');
const missing = await ok.dispatch('fetch', {
  request: {method:'GET',mode:'navigate',url:scope+'missing'},
});
assert.ok((await missing.text()).includes('404.html'), 'Offline fallback uses saved 404');
const pdfResponse = await ok.dispatch('fetch', {
  request:{method:'GET',mode:'cors',url:scope+'20th-Century%20International%20History.pdf'},
});
assert.equal(pdfResponse, undefined, 'Large PDF must not be intercepted or precached');

ok.setOnline(true);
await ok.dispatch('message', {data: {type: 'PREPARE_FONTS', urls:[
  'https://fonts.googleapis.com/css2?family=Amiri',
  'https://fonts.gstatic.com/s/amiri/v1/font.woff2',
  'https://example.org/bad.woff2',
]}});
ok.setOnline(false);
const cachedFont = await ok.dispatch('fetch', {
  request:{method:'GET',mode:'cors',url:'https://fonts.gstatic.com/s/amiri/v1/font.woff2'},
});
assert.ok((await cachedFont.text()).includes('fonts.gstatic.com'));
const fontCache = ok.stores.get('whd-google-fonts-v1');
assert.equal(fontCache.data.size, 2, 'Only approved Google Fonts URLs are cached');

const fail = simulate(true);
await fail.caches.open('whd-edition-prior');
await assert.rejects(fail.dispatch('install'), /interrupted download/);
assert.equal(fail.stats().skipCount, 0, 'Incomplete install must not activate');
assert.ok(fail.stores.has('whd-edition-prior'), 'Prior edition survives failed update');
console.log('PASS: atomic hashed install, offline book and 404, sibling isolation, PDF exclusion, optional fonts, failed update recovery');
