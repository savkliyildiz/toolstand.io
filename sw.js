// ToolStand Service Worker — minimal, no precache, no cross-origin interception
const CACHE_VERSION = 'ts-v20';

// Install: skip waiting so new SW activates immediately
self.addEventListener('install', () => {
  self.skipWaiting();
});

// Activate: claim all clients
self.addEventListener('activate', e => {
  e.waitUntil(self.clients.claim());
});

// Fetch: pass through all requests, don't cache cross-origin
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Don't intercept cross-origin requests
  if (url.origin !== self.location.origin) return;
  // Don't intercept analytics API
  if (url.pathname.startsWith('/api/')) return;
  // Network-first: try network, fall back to cache
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
