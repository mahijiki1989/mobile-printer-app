// Basic Service Worker to allow PWA installation
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('advprint-store').then((cache) => cache.addAll([
      '/mobile-printer-app/',
      '/mobile-printer-app/index.html',
      '/mobile-printer-app/styles.css',
      '/mobile-printer-app/app.js',
      '/mobile-printer-app/voice-memory.html',
      '/mobile-printer-app/voice-memory.js',
      '/mobile-printer-app/voice-memory.css'
    ]))
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => response || fetch(e.request))
  );
});
