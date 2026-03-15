import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { BrowserRouter } from 'react-router';
import { registerServiceWorker } from './PWA/service-worker-register';

// Register service worker for offline support
registerServiceWorker(
  // Callback when a new service worker is available
  (registration) => {
    console.log('[App] New service worker available:', registration);
    // You can show a custom UI here instead of the default prompt
  },
  // Callback when registration fails
  (error) => {
    console.error('[App] Service worker registration failed:', error);
  }
);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
