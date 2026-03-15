import { apiClient } from '../../api/client';
import { offlineStorage, PendingRequest } from './storage.service';

/**
 * Offline Sync Service
 * Manages queuing and synchronization of API requests when offline
 */
export class OfflineSyncService {
  private isOnline: boolean = navigator.onLine;
  private syncInProgress: boolean = false;
  private syncInterval: number | null = null;

  // Store event listener references for cleanup
  private handleOnline = () => {
    this.isOnline = true;
    console.log('[OfflineSync] Connection restored. Syncing pending requests...');
    this.syncPendingRequests().catch((error) => {
      console.error('[OfflineSync] Auto-sync failed:', error);
    });
  };

  private handleOffline = () => {
    this.isOnline = false;
    console.log('[OfflineSync] Connection lost. Requests will be queued.');
  };

  constructor() {
    this.setupEventListeners();
  }

  /**
   * Setup event listeners for online/offline status changes
   */
  setupEventListeners(): void {
    if (typeof window !== 'undefined') {
      window.addEventListener('online', this.handleOnline);
      window.addEventListener('offline', this.handleOffline);
    }
  }

  /**
   * Cleanup event listeners and intervals
   * Call this when the service is no longer needed to prevent memory leaks
   */
  destroy(): void {
    if (typeof window !== 'undefined') {
      window.removeEventListener('online', this.handleOnline);
      window.removeEventListener('offline', this.handleOffline);
    }
    this.stopAutoSync();
    console.log('[OfflineSync] Service destroyed and event listeners removed');
  }

  /**
   * Queue a request for offline sync
   * @param endpoint - API endpoint path
   * @param method - HTTP method
   * @param body - Request body (optional)
   * @returns Promise resolving to the queued request ID
   */
  async queueRequest(
    endpoint: string,
    method: 'GET' | 'POST' | 'PATCH' | 'DELETE',
    body?: unknown
  ): Promise<number> {
    const token = localStorage.getItem('access_token');

    const pendingRequest: PendingRequest = {
      endpoint,
      method,
      body,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` })
      },
      timestamp: Date.now(),
      retries: 0
    };

    const requestId = await offlineStorage.queueRequest(pendingRequest);
    console.log(`[OfflineSync] Request queued: ${method} ${endpoint} (ID: ${requestId})`);

    // Auto-sync if online
    if (this.isOnline) {
      this.syncPendingRequests().catch((error) => {
        console.error('[OfflineSync] Auto-sync after queue failed:', error);
      });
    }

    return requestId;
  }

  /**
   * Sync all pending requests
   * Processes queued requests in FIFO order
   */
  async syncPendingRequests(): Promise<void> {
    if (this.syncInProgress) {
      console.log('[OfflineSync] Sync already in progress. Skipping...');
      return;
    }

    if (!this.isOnline) {
      console.log('[OfflineSync] Currently offline. Cannot sync.');
      return;
    }

    this.syncInProgress = true;
    console.log('[OfflineSync] Starting sync of pending requests...');

    try {
      const pendingRequests = await offlineStorage.getPendingRequests();

      if (pendingRequests.length === 0) {
        console.log('[OfflineSync] No pending requests to sync.');
        return;
      }

      console.log(`[OfflineSync] Found ${pendingRequests.length} pending requests`);

      for (const request of pendingRequests) {
        if (!this.isOnline) {
          console.log('[OfflineSync] Connection lost during sync. Aborting...');
          break;
        }

        await this.processRequest(request);
      }

      console.log('[OfflineSync] Sync completed');
    } catch (error) {
      console.error('[OfflineSync] Sync failed:', error);
      throw error;
    } finally {
      this.syncInProgress = false;
    }
  }

  /**
   * Process a single pending request
   * @param request - The pending request to process
   */
  private async processRequest(request: PendingRequest): Promise<void> {
    const maxRetries = 3;
    const requestId = request.id!;

    try {
      console.log(`[OfflineSync] Processing request: ${request.method} ${request.endpoint}`);

      const response = await apiClient.request({
        method: request.method,
        url: request.endpoint,
        data: request.body,
        headers: request.headers
      });

      // Validate response status code before removing from queue
      if (response.status >= 200 && response.status < 300) {
        // Success - remove from queue
        await offlineStorage.removePendingRequest(requestId);
        console.log(`[OfflineSync] Request succeeded and removed from queue (ID: ${requestId})`);
      } else {
        // Non-success status code - treat as failure
        throw new Error(`Request returned status ${response.status}`);
      }
    } catch (error) {
      // Failure - increment retry count or remove if max retries exceeded
      if (request.retries >= maxRetries) {
        await offlineStorage.removePendingRequest(requestId);
        console.error(
          `[OfflineSync] Request failed after ${maxRetries} retries. Removed from queue (ID: ${requestId})`,
          error
        );
      } else {
        await offlineStorage.incrementRetry(requestId);
        console.warn(
          `[OfflineSync] Request failed. Retry ${request.retries + 1}/${maxRetries} (ID: ${requestId})`,
          error
        );
      }
    }
  }

  /**
   * Start automatic periodic sync
   * @param intervalMs - Sync interval in milliseconds (default: 60000 = 1 minute)
   */
  startAutoSync(intervalMs: number = 60000): void {
    if (this.syncInterval !== null) {
      console.log('[OfflineSync] Auto-sync already running');
      return;
    }

    console.log(`[OfflineSync] Starting auto-sync every ${intervalMs}ms`);

    this.syncInterval = window.setInterval(() => {
      if (this.isOnline && !this.syncInProgress) {
        this.syncPendingRequests().catch((error) => {
          console.error('[OfflineSync] Auto-sync failed:', error);
        });
      }
    }, intervalMs);
  }

  /**
   * Stop automatic periodic sync
   */
  stopAutoSync(): void {
    if (this.syncInterval !== null) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
      console.log('[OfflineSync] Auto-sync stopped');
    }
  }

  /**
   * Manually trigger a sync
   * Useful for forcing sync outside the automatic schedule
   */
  async forceSync(): Promise<void> {
    console.log('[OfflineSync] Force sync triggered');
    await this.syncPendingRequests();
  }

  /**
   * Get the count of pending requests
   * @returns Number of requests awaiting sync
   */
  async getPendingCount(): Promise<number> {
    const pendingRequests = await offlineStorage.getPendingRequests();
    return pendingRequests.length;
  }

  /**
   * Check if currently online
   * @returns True if online, false if offline
   */
  isCurrentlyOnline(): boolean {
    return this.isOnline;
  }
}

// Export singleton instance
export const offlineSyncService = new OfflineSyncService();
