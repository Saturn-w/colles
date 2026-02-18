const CACHE_NAME = 'colles-psi-v1';
const urlsToCache = [
  './',
  './index.html',
  './manifest.json'
];

// Installation du service worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache ouvert');
        return cache.addAll(urlsToCache);
      })
  );
  self.skipWaiting();
});

// Activation et nettoyage des anciens caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Suppression du cache ancien:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Stratégie : Cache-First pour les PDFs, Network-First pour le reste
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // Pour les PDFs : Cache-First (rapide)
  if (url.pathname.endsWith('.pdf')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          // Si le PDF est en cache, le retourner
          if (response) {
            return response;
          }
          
          // Sinon, le télécharger et le mettre en cache
          return fetch(event.request).then(response => {
            // Vérifier que la réponse est valide
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Cloner la réponse
            const responseToCache = response.clone();
            
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
            
            return response;
          });
        })
    );
  } 
  // Pour le reste : Network-First (toujours à jour)
  else {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Cloner et mettre en cache
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
          return response;
        })
        .catch(() => {
          // Si le réseau échoue, essayer le cache
          return caches.match(event.request);
        })
    );
  }
});
