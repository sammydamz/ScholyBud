export type StudentStatus = 'active' | 'graduated' | 'withdrawn' | 'transferred' | 'suspended';
export type Gender = 'male' | 'female' | 'other';

export interface Student {
  id: string;
  admission_number: string;
  first_name: string;
  last_name: string;
  other_names: string | null;
  date_of_birth: string;
  gender: Gender;
  guardian_name: string;
  guardian_phone: string;
  guardian_email: string | null;
  guardian_relationship: string;
  address: string;
  class_id: string | null;
  status: StudentStatus;
  photo_url: string | null;
  enrollment_date: string;
  created_at: string;
  updated_at: string | null;
}

export interface CreateStudent {
  admission_number: string;
  first_name: string;
  last_name: string;
  other_names?: string;
  date_of_birth: string;
  gender: Gender;
  guardian_name: string;
  guardian_phone: string;
  guardian_email?: string;
  guardian_relationship?: string;
  address: string;
  class_id?: string;
  photo_url?: string;
}

export interface UpdateStudent {
  first_name?: string;
  last_name?: string;
  other_names?: string;
  guardian_name?: string;
  guardian_phone?: string;
  guardian_email?: string;
  address?: string;
  class_id?: string;
  photo_url?: string;
  status?: StudentStatus;
}

export interface Class {
  id: string;
  name: string;
  level: string;
  class_teacher_id: string | null;
  capacity: number | null;
  academic_year: string;
  is_active: boolean;
}
