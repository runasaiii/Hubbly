import { apiClient } from '@/shared/lib/api';
import type { Post, Comment, CreatePostRequest, CreateCommentRequest, PaginatedResponse } from '@/shared/types';

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

  getComments: (postId: string): Promise<Comment[]> =>
    apiClient.get(`/posts/api/${postId}/comments/`).catch(() => []),

  createComment: (data: CreateCommentRequest): Promise<Comment> =>
    apiClient.post('/posts/api/comments/', data),
};

