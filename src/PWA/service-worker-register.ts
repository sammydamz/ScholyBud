/**
 * Service Worker Registration Module
 * Handles service worker registration, update detection, and lifecycle management
 */

const SW_VERSION = '1.0.0';
const SW_URL = '/service-worker.js';

type UpdateCallback = (registration: ServiceWorkerRegistration) => void;
type ErrorCallback = (error: Error) => void;

let updateCallback: UpdateCallback | null = null;
let errorCallback: ErrorCallback | null = null;

/**
 * Register the service worker
 * @param onUpdate - Callback when a new service worker is available
 * @param onError - Callback when registration fails
 */
export function registerServiceWorker(
  onUpdate?: UpdateCallback,
  onError?: ErrorCallback
): void {
  if (typeof window === 'undefined' || !('serviceWorker' in navigator)) {
    console.warn('[Service Worker] Service workers are not supported in this environment');
    return;
  }

  updateCallback = onUpdate || null;
  errorCallback = onError || null;

  // Wait for the page to finish loading
  if (document.readyState === 'complete') {
    registerSW();
  } else {
    window.addEventListener('load', registerSW);
  }
}

/**
 * Internal function to register the service worker
 */
function registerSW(): void {
  navigator.serviceWorker
    .register(SW_URL, {
      updateViaCache: 'imports',
      type: 'classic',
    })
    .then((registration) => {
      console.log('[Service Worker] Registered successfully:', SW_VERSION);

      // Check for updates immediately
      if (registration.waiting) {
        handleUpdateAvailable(registration);
      }

      // Listen for updates
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;

        if (newWorker) {
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New service worker is available
              handleUpdateAvailable(registration);
            }
          });
        }
      });

      // Listen for controller change (new service worker activated)
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        console.log('[Service Worker] Controller changed, reloading page');
        window.location.reload();
      });

      return registration;
    })
    .catch((error: Error) => {
      console.error('[Service Worker] Registration failed:', error);
      if (errorCallback) {
        errorCallback(error);
      }
    });
}

/**
 * Handle when a new service worker update is available
 */
function handleUpdateAvailable(registration: ServiceWorkerRegistration): void {
  console.log('[Service Worker] New version available');

  if (updateCallback) {
    updateCallback(registration);
  } else {
    // Default behavior: show a simple confirm dialog
    const shouldUpdate = confirm(
      'A new version of ScholyBud is available. Would you like to update now?'
    );

    if (shouldUpdate) {
      // Tell the new service worker to skip waiting
      registration.waiting?.postMessage({ type: 'SKIP_WAITING' });
    }
  }
}

/**
 * Unregister the service worker
 */
export async function unregisterServiceWorker(): Promise<void> {
  if (typeof window === 'undefined' || !('serviceWorker' in navigator)) {
    return;
  }

  try {
    const registration = await navigator.serviceWorker.getRegistration();

    if (registration) {
      await registration.unregister();
      console.log('[Service Worker] Unregistered successfully');

      // Clear all caches
      const cacheNames = await caches.keys();
      await Promise.all(cacheNames.map((cacheName) => caches.delete(cacheName)));
      console.log('[Service Worker] All caches cleared');

      // Reload the page to ensure all service worker effects are removed
      window.location.reload();
    }
  } catch (error) {
    console.error('[Service Worker] Unregistration failed:', error);
    throw error;
  }
}

export default {
  registerServiceWorker,
  unregisterServiceWorker,
};
