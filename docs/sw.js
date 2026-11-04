/* Service worker — network-first with cache fallback.
   The dashboard data refreshes monthly, so we always try the network
   first and only fall back to cache when offline. Bump CACHE_VERSION
   when sw.js itself changes to force a clean cache. */
var CACHE_VERSION = "biblio-dashboard-v1";
var CORE_ASSETS = [
  ".",
  "index.html",
  "styles.css",
  "app.js",
  "manifest.webmanifest",
  "vendor/chart.umd.min.js",
  "assets/icon-192.png",
  "assets/icon-512.png"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_VERSION).then(function (cache) {
      // Add each asset independently so one 404 doesn't fail the install.
      return Promise.all(
        CORE_ASSETS.map(function (asset) {
          return cache.add(asset).catch(function () { /* optional asset */ });
        })
      );
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.map(function (key) {
          return key !== CACHE_VERSION ? caches.delete(key) : Promise.resolve();
        })
      );
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (request.method !== "GET") return;
  var url = new URL(request.url);
  if (url.origin !== self.location.origin) return; // let external APIs go direct

  event.respondWith(
    fetch(request).then(function (response) {
      if (response && response.status === 200) {
        var copy = response.clone();
        caches.open(CACHE_VERSION).then(function (cache) { cache.put(request, copy); });
      }
      return response;
    }).catch(function () {
      return caches.match(request).then(function (cached) {
        if (cached) return cached;
        if (request.mode === "navigate") return caches.match("index.html");
        return new Response("Offline", { status: 503, headers: { "Content-Type": "text/plain" } });
      });
    })
  );
});
