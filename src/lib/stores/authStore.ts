import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { STORAGE_KEYS } from '../constants';

/**
 * User interface representing the authenticated user structure
 */
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'super_admin' | 'school_admin' | 'teacher';
  school_id?: string;
  is_active: boolean;
}

/**
 * Authentication state interface
 */
export interface AuthState {
  /** Current authenticated user */
  user: User | null;
  /** JWT access token */
  token: string | null;
  /** Authentication status flag */
  isAuthenticated: boolean;

  /**
   * Sets authentication data
   * @param user - User object to set
   * @param token - JWT access token
   */
  setAuth: (user: User, token: string) => void;

  /**
   * Logs out the user and clears all authentication state
   */
  logout: () => void;

  /**
   * Updates user data with partial updates
   * @param updates - Partial user object with fields to update
   */
  updateUser: (updates: Partial<User>) => void;
}

/**
 * Authentication store using Zustand with persistence
 * Stores auth state in localStorage under 'scholybud-auth' key
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      setAuth: (user, token) => {
        localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, token);
        set({ user, token, isAuthenticated: true });
      },

      logout: () => {
        localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
        set({ user: null, token: null, isAuthenticated: false });
      },

      updateUser: (updates) => {
        set((state) => ({
          user: state.user ? { ...state.user, ...updates } : null,
        }));
      },
    }),
    {
      name: 'scholybud-auth',
    }
  )
);
