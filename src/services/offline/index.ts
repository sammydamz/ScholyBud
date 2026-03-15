// Export database instance
export { db, offlineStorage } from './storage.service';

// Export service classes
export { OfflineStorageService } from './storage.service';
export { OfflineSyncService, offlineSyncService } from './sync.service';

// Export types
export type {
  PendingRequest,
  OfflineStudent,
  OfflineAttendance
} from './storage.service';
