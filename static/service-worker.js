self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('static-cache-v1').then(cache => {
            return cache.addAll([
                './styles.css',
                './app.js',
                './manifest.json',
                './images/icon.png',
                './images/apple-touch-icon.png'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
