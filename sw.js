/* Courier Symphony — Offline Service Worker (Cache-First) */
const CACHE_NAME = 'courier-symphony-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/demo.html',
  '/repo-reality-check.html',
  '/architecture.html',
  '/security.html',
  '/use-cases.html',
  '/developers.html',
  '/company.html',
  '/widerruf.html',
  '/impressum.html',
  '/datenschutz.html',
  '/privacy.html',
  '/404.html',
  '/styles.css',
  '/favicon.svg',
  '/apple-touch-icon.png',
  '/og-cover.png',
  '/robots.txt',
  '/sitemap.xml',
  '/manifest.json',
  '/receipt.schema.json',
  '/sample-receipt.json',
  '/sample-reality-report.json',
  '/sample-inventory-dirty.csv',
  '/sample-inventory-clean.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) {
        return cached;
      }
      return fetch(event.request).then((response) => {
        // Cache valid responses dynamically
        if (response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      }).catch(() => {
        // Fallback to offline 404 or root
        return caches.match('/404.html');
      });
    })
  );
});
