// Offline support for the product-film page (/promo/).
// The page, poster, font and the 1080p video are cached on first visit; the 4K file is cached once it is played.
// Video requests are answered from the cache, including byte-range requests, so seeking and looping work offline.
const CACHE = 'infu-promo-v1';
const V1080 = 'export/INFU-RETRO_%ED%99%8D%EB%B3%B4%EC%98%81%EC%83%81_1080p60.mp4';
const CORE = ['./', 'index.html', 'poster.jpg', 'src/PretendardVariable.woff2', 'manifest.webmanifest', 'icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(CORE);
    try { await c.add(V1080); } catch (err) { /* network hiccup: cached later on first play */ }
    self.skipWaiting();
  })());
});
self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
    await self.clients.claim();
  })());
});
self.addEventListener('message', e => {           // page asks: { cache: url } → store a full copy, reply when done
  if (!e.data || !e.data.cache) return;
  e.waitUntil((async () => {
    const c = await caches.open(CACHE), url = new URL(e.data.cache, self.registration.scope).href;
    let ok = !!(await c.match(url));
    if (!ok) { try { await c.add(url); ok = true; } catch (err) { ok = false; } }
    for (const cl of await self.clients.matchAll()) cl.postMessage({ cached: e.data.cache, ok });
  })());
});

async function ranged(req, full) {              // serve a Range request from a cached full response
  const range = req.headers.get('range');
  if (!range) return full;
  const buf = await full.arrayBuffer(), size = buf.byteLength;
  const m = /bytes=(\d*)-(\d*)/.exec(range);
  let start = m && m[1] ? +m[1] : 0, end = m && m[2] ? +m[2] : size - 1;
  if (m && !m[1] && m[2]) { start = size - +m[2]; end = size - 1; }
  end = Math.min(end, size - 1);
  return new Response(buf.slice(start, end + 1), { status: 206, statusText: 'Partial Content', headers: {
    'Content-Type': full.headers.get('Content-Type') || 'video/mp4', 'Content-Range': `bytes ${start}-${end}/${size}`,
    'Content-Length': String(end - start + 1), 'Accept-Ranges': 'bytes' } });
}

self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (!url.pathname.startsWith(new URL(self.registration.scope).pathname)) return;
  if (url.pathname.endsWith('.mp4')) {
    e.respondWith((async () => {
      const c = await caches.open(CACHE), hit = await c.match(url.href);
      if (hit) return ranged(req, hit);
      return fetch(req);                         // not cached yet: stream from the network
    })());
    return;
  }
  e.respondWith((async () => {                   // pages & assets: network first (fresh), cache as fallback (offline)
    const c = await caches.open(CACHE);
    try { const r = await fetch(req); if (r.ok) c.put(req, r.clone()); return r; }
    catch (err) { return (await c.match(req, { ignoreSearch: true })) || (await c.match('index.html')) || Response.error(); }
  })());
});
