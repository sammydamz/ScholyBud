export type AttendanceStatus = 'present' | 'absent' | 'late' | 'excused';

export interface AttendanceRecord {
  id: string;
  student_id: string;
  date: string;
  status: AttendanceStatus;
  remarks: string | null;
  recorded_by: string;
  created_at: string;
}

export interface CreateAttendance {
  student_id: string;
  date: string;
  status: AttendanceStatus;
  remarks?: string;
}

export interface AttendanceSummary {
  total: number;
  present: number;
  absent: number;
  late: number;
  excused: number;
  percentage: number;
}
