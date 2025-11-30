import { apiClient } from '@/shared/lib/api';
import type { Post, Comment, CreatePostRequest, PaginatedResponse } from '@/shared/types';

export const postsApi = {
  list: (params?: { community?: string; search?: string }): Promise<Post[] | PaginatedResponse<Post>> =>
    apiClient.get('/posts/api/', { params }),

  get: (id: string): Promise<Post> =>
    apiClient.get(`/posts/api/${id}/`),

  create: (data: CreatePostRequest): Promise<Post> =>
    apiClient.post('/posts/api/', data),

  update: (id: string, data: Partial<CreatePostRequest>): Promise<Post> =>
    apiClient.put(`/posts/api/${id}/`, data),

  delete: (id: string): Promise<void> =>
    apiClient.delete(`/posts/api/${id}/`),

  getUserPosts: (userId: string): Promise<Post[]> =>
    apiClient.get(`/posts/v1/user/${userId}`),

  getComments: async (postId: string): Promise<Comment[]> => {
  try {
    return await apiClient.get<Comment[]>(`/posts/${postId}/comments/`);
  } catch {
    return [];
  }
},


  createComment: async (postId: string, data: { content: string }, token: string): Promise<Comment> => {
  return apiClient.post(
    `/posts/${postId}/comments/`,
    data,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }
  );
},

  like: async (postId: string, token: string): Promise<Post> => {
    return apiClient.post(
      `/posts/${postId}/like/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
  },

  unlike: async (postId: string, token: string): Promise<Post> => {
    return apiClient.delete(
      `/posts/${postId}/like/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
  },

};
