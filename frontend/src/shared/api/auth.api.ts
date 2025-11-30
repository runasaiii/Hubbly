import { apiClient } from '@/shared/lib/api';
import type { AuthResponse, LoginRequest, RegisterRequest, User } from '@/shared/types';

export const authApi = {
  register: (data: RegisterRequest) =>
    apiClient.post<AuthResponse>('/users/v1/user/register', data),

  login: (data: LoginRequest) =>
    apiClient.post<AuthResponse>('/users/v1/user/login', data),

  verifyToken: (token: string): Promise<{ detail?: string }> =>
    apiClient.post('/token/verify/', { token }),

  refreshToken: (refresh: string): Promise<{ access: string }> =>
    apiClient.post('/token/refresh/', { refresh }),

  getCurrentUser: (): Promise<User> =>
    apiClient.get<User>('/users/v1/user/personal_data'),
};

