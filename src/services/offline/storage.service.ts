import Dexie, { Table } from 'dexie';

// Interface for pending API requests
export interface PendingRequest {
  id?: number;
  endpoint: string;
  method: 'GET' | 'POST' | 'PATCH' | 'DELETE';
  body?: unknown;
  headers?: Record<string, string>;
  timestamp: number;
  retries: number;
}

// Interface for offline student data
export interface OfflineStudent {
  id: string;
  admission_number: string;
  first_name: string;
  last_name: string;
  class_id: string | null;
  status: string;
  photo_url: string | null;
  synced: boolean;
  updated_at: number;
}

// Interface for offline attendance data
export interface OfflineAttendance {
  id: string;
  student_id: string;
  date: string; // ISO date string
  status: 'present' | 'absent' | 'late' | 'excused';
  synced: boolean;
  timestamp: number;
}

// Dexie database class
class ScholyBudDB extends Dexie {
  pendingRequests!: Table<PendingRequest, number>;
  offlineStudents!: Table<OfflineStudent, string>;
  offlineAttendance!: Table<OfflineAttendance, string>;

  constructor() {
    super('ScholyBudDB');

    // Define schema with indexes
    this.version(1).stores({
      pendingRequests: '++id, endpoint, timestamp',
      offlineStudents: 'id, admission_number, synced',
      offlineAttendance: 'id, student_id, date, synced'
    });
  }
}

// Initialize database instance
export const db = new ScholyBudDB();

// Offline Storage Service
export class OfflineStorageService {
  private db: ScholyBudDB;

  constructor(database: ScholyBudDB) {
    this.db = database;
  }

  // ==================== Pending Request Methods ====================

  /**
   * Queue a request for later sync
   */
  async queueRequest(request: PendingRequest): Promise<number> {
    try {
      return await this.db.pendingRequests.add({
        ...request,
        timestamp: request.timestamp || Date.now(),
        retries: request.retries || 0
      });
    } catch (error) {
      console.error('Failed to queue request:', error);
      throw error;
    }
  }

  /**
   * Get all pending requests
   */
  async getPendingRequests(): Promise<PendingRequest[]> {
    return await this.db.pendingRequests.toArray();
  }

  /**
   * Remove a pending request by ID
   */
  async removePendingRequest(id: number): Promise<void> {
    return await this.db.pendingRequests.delete(id);
  }

  /**
   * Increment retry count for a request
   */
  async incrementRetry(id: number): Promise<void> {
    return await this.db.pendingRequests.update(id, (request) => {
      return { retries: (request.retries || 0) + 1 };
    });
  }

  // ==================== Offline Student Methods ====================

  /**
   * Save or update a student offline
   */
  async saveOfflineStudent(student: OfflineStudent): Promise<string> {
    try {
      await this.db.offlineStudents.put(student);
      return student.id;
    } catch (error) {
      console.error('Failed to save offline student:', error);
      throw error;
    }
  }

  /**
   * Get all offline students
   */
  async getOfflineStudents(): Promise<OfflineStudent[]> {
    return await this.db.offlineStudents.toArray();
  }

  /**
   * Mark a student as synced
   */
  async markStudentSynced(studentId: string): Promise<number> {
    return await this.db.offlineStudents.update(studentId, { synced: true });
  }

  // ==================== Offline Attendance Methods ====================

  /**
   * Save attendance record offline
   */
  async saveOfflineAttendance(attendance: OfflineAttendance): Promise<string> {
    try {
      await this.db.offlineAttendance.put(attendance);
      return attendance.id;
    } catch (error) {
      console.error('Failed to save offline attendance:', error);
      throw error;
    }
  }

  /**
   * Get all offline attendance records
   */
  async getOfflineAttendance(): Promise<OfflineAttendance[]> {
    return await this.db.offlineAttendance.toArray();
  }

  /**
   * Mark attendance record as synced
   */
  async markAttendanceSynced(attendanceId: string): Promise<number> {
    return await this.db.offlineAttendance.update(attendanceId, { synced: true });
  }

  // ==================== Utility Methods ====================

  /**
   * Clear all synced data to free up space
   */
  async clearSyncedData(): Promise<void> {
    try {
      await this.db.transaction('rw', [this.db.offlineStudents, this.db.offlineAttendance], async () => {
        await this.db.offlineStudents.where('synced').equals(true).delete();
        await this.db.offlineAttendance.where('synced').equals(true).delete();
      });
    } catch (error) {
      console.error('Failed to clear synced data:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const offlineStorage = new OfflineStorageService(db);
