/// <reference lib="webworker" />

declare const self: ServiceWorkerGlobalScope;

const CACHE_NAME = 'scholybud-v1';
const OFFLINE_URL = '/offline.html';

// Assets to cache immediately on service worker installation
const PRECACHE_ASSETS = [
  '/',
  '/offline.html',
  '/manifest.webmanifest',
];

// API routes that should be cached
const API_ROUTES = ['/api/v1/'];

/**
 * Install event - precache static assets
 */
self.addEventListener('install', (event: ExtendableEvent) => {
  console.log('[Service Worker] Installing...');

  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      console.log('[Service Worker] Precaching assets');
      await cache.addAll(PRECACHE_ASSETS);

      // Force the waiting service worker to become the active service worker
      await self.skipWaiting();
    })()
  );
});

/**
 * Activate event - clean up old caches
 */
self.addEventListener('activate', (event: ExtendableEvent) => {
  console.log('[Service Worker] Activating...');

  event.waitUntil(
    (async () => {
      // Clean up old caches
      const cacheNames = await caches.keys();
      const cachesToDelete = cacheNames.filter(
        (cacheName) => cacheName !== CACHE_NAME
      );

      await Promise.all(
        cachesToDelete.map((cacheName) => caches.delete(cacheName))
      );

      // Take control of all pages immediately
      await self.clients.claim();
    })()
  );
});

/**
 * Fetch event - handle network requests with appropriate caching strategies
 */
self.addEventListener('fetch', (event: FetchEvent) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle API requests with Network-First strategy
  if (API_ROUTES.some((route) => url.pathname.startsWith(route))) {
    event.respondWith(handleApiRequest(request));
    return;
  }

  // Handle navigation requests with Network-First fallback to offline
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(request));
    return;
  }

  // Handle static assets (images, CSS, JS) with Cache-First strategy
  if (request.destination === 'image' ||
      request.destination === 'style' ||
      request.destination === 'script') {
    event.respondWith(handleStaticAssetRequest(request));
    return;
  }

  // Default: Network-First for everything else
  event.respondWith(
    (async () => {
      try {
        const response = await fetch(request);
        return response;
      } catch (error) {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
          return cachedResponse;
        }
        throw error;
      }
    })()
  );
});

/**
 * Handle API requests with Network-First strategy
 * Caches successful GET responses for offline use
 */
async function handleApiRequest(request: Request): Promise<Response> {
  const cache = await caches.open(CACHE_NAME);

  // For non-GET requests, always go to network
  if (request.method !== 'GET') {
    try {
      const networkResponse = await fetch(request);
      return networkResponse;
    } catch (error) {
      // Return 503 when offline
      return new Response(
        JSON.stringify({
          error: 'Service Unavailable',
          message: 'You are currently offline. Please check your connection.',
          offline: true,
        }),
        {
          status: 503,
          statusText: 'Service Unavailable',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
    }
  }

  try {
    // Try network first
    const networkResponse = await fetch(request);

    // Cache successful responses
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    // Network failed, try cache
    const cachedResponse = await cache.match(request);

    if (cachedResponse) {
      console.log('[Service Worker] Serving cached API response');
      return cachedResponse;
    }

    // No cached data available, return 503
    console.log('[Service Worker] Offline and no cached data');
    return new Response(
      JSON.stringify({
        error: 'Service Unavailable',
        message: 'You are currently offline and no cached data is available.',
        offline: true,
      }),
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  }
}

/**
 * Handle navigation requests with Network-First strategy
 * Falls back to offline page when offline
 */
async function handleNavigationRequest(request: Request): Promise<Response> {
  try {
    // Try network first
    const networkResponse = await fetch(request);
    return networkResponse;
  } catch (error) {
    // Network failed, try cache
    const cachedResponse = await caches.match(request);

    if (cachedResponse) {
      console.log('[Service Worker] Serving cached navigation');
      return cachedResponse;
    }

    // No cached page, return offline page
    console.log('[Service Worker] Offline, serving offline page');
    const offlineResponse = await caches.match(OFFLINE_URL);

    if (offlineResponse) {
      return offlineResponse;
    }

    // Fallback response if offline page is not cached
    return new Response(
      '<h1>You are offline</h1><p>Please check your internet connection and try again.</p>',
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: {
          'Content-Type': 'text/html',
        },
      }
    );
  }
}

/**
 * Handle static asset requests with Cache-First strategy
 */
async function handleStaticAssetRequest(request: Request): Promise<Response> {
  const cache = await caches.open(CACHE_NAME);

  // Try cache first
  const cachedResponse = await cache.match(request);

  if (cachedResponse) {
    console.log('[Service Worker] Serving cached static asset:', request.url);
    return cachedResponse;
  }

  // Cache miss, fetch from network
  try {
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.error('[Service Worker] Static asset fetch failed:', error);
    throw error;
  }
}

/**
 * Message event - handle messages from clients
 */
self.addEventListener('message', (event: ExtendableMessageEvent) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

export null;
