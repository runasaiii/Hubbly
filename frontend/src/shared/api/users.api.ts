import { apiClient } from '@/shared/lib/api';
import type { User, Profile, PaginatedResponse } from '@/shared/types';

export const usersApi = {
  list: (): Promise<User[] | PaginatedResponse<User>> =>
    apiClient.get('/users/api/'),

  get: (id: string | number): Promise<User> =>
    apiClient.get(`/users/api/${id}/`),

  getProfile: (userId: string): Promise<Profile> =>
    apiClient.get(`/users/${userId}/profile/`),

  updateProfile: (userId: string, data: Partial<Profile>): Promise<Profile> =>
    apiClient.patch(`/users/${userId}/profile/`, data),
};

