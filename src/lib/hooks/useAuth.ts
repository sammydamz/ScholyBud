import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api';
import { useAuthStore } from '../stores';

interface LoginCredentials {
  username: string;
  password: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
}

export function useAuth() {
  const { user, isAuthenticated, setAuth, logout } = useAuthStore();
  const queryClient = useQueryClient();

  const loginMutation = useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      const formData = new FormData();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);

      const response = await apiClient.post<AuthResponse>('/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Fetch user data after successful login
      const userResponse = await apiClient.get('/auth/me');
      const userData = userResponse.data;

      return {
        token: response.data.access_token,
        user: userData,
      };
    },
    onSuccess: (data) => {
      setAuth(data.user, data.token);
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
  });

  const logoutMutation = useMutation({
    mutationFn: async () => {
      await apiClient.post('/auth/logout');
    },
    onSettled: () => {
      logout();
      queryClient.clear();
    },
  });

  return {
    user,
    isAuthenticated,
    login: loginMutation.mutateAsync,
    logout: () => logoutMutation.mutate(),
    isLoading: loginMutation.isPending,
    error: loginMutation.error,
  };
}
