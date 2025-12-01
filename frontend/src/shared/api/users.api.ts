import { apiClient } from '@/shared/lib/api';
import type { User, Profile, PaginatedResponse } from '@/shared/types';

export const usersApi = {
  list: async (): Promise<User[] | PaginatedResponse<User>> => {
    return await apiClient.get<User[] | PaginatedResponse<User>>('/api/');
  },

  get: async (id: string | number): Promise<User> => {
    return await apiClient.get<User>(`/api/${id}/`);
  },

  getProfile: async (): Promise<Profile> => {
    return await apiClient.get<Profile>('/users/v1/user/profile');
  },

  getUserProfile: async (userId: string): Promise<{ user: User; profile: Profile }> => {
    return await apiClient.get<{ user: User; profile: Profile }>(`/users/v1/user/${userId}/profile`);
  },

  uploadAvatar: async (file: File): Promise<Profile> => {
    const formData = new FormData();
    formData.append('avatar', file);
    return await apiClient.post<Profile>('/users/v1/user/profile/avatar', formData);
  },

  updateProfile: async (data: Partial<Profile> | FormData): Promise<Profile> => {
    if (data instanceof FormData) {
      const avatar = data.get('avatar');
      if (avatar instanceof File) {
        const profile = await usersApi.uploadAvatar(avatar);
        const otherData: Partial<Profile> = {};
        if (data.get('display_name')) otherData.display_name = data.get('display_name') as string;
        if (data.get('bio')) otherData.bio = data.get('bio') as string;
        if (data.get('location')) otherData.location = data.get('location') as string;
        if (data.get('gender')) otherData.gender = data.get('gender') as 'male' | 'female' | 'other';
        if (data.get('interests')) {
          try {
            otherData.interests = JSON.parse(data.get('interests') as string);
          } catch {
            otherData.interests = [];
          }
        }
        if (Object.keys(otherData).length > 0) {
          return usersApi.updateProfile(otherData);
        }
        return profile;
      }
    }
    return await apiClient.patch<Profile>('/users/v1/user/profile', data);
  },
};