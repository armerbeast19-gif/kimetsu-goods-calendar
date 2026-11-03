// 鬼滅グッズカレンダー：オフラインでも前回の内容を表示するための最小限のService Worker
const CACHE = "kmt-v1";
self.addEventListener("install", e => { self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const mine = url.origin === location.origin || url.hostname === "raw.githubusercontent.com";
  if (!mine) return; // 広告やフォントには関与しない
  e.respondWith(
    fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(url.hostname === "raw.githubusercontent.com" ? url.origin + url.pathname : req, copy)); }
      return res;
    }).catch(() => caches.match(url.hostname === "raw.githubusercontent.com" ? url.origin + url.pathname : req).then(r => r || caches.match("./")))
  );
});
