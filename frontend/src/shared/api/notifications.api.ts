import { apiClient } from '@/shared/lib/api';
import type { Notification, PaginatedResponse } from '@/shared/types';

export const notificationsApi = {
  list: (): Promise<Notification[] | PaginatedResponse<Notification>> =>
    apiClient.get('/notification/'),

  markAsRead: (id: string): Promise<Notification> =>
    apiClient.patch(`/notification/${id}/read/`).catch(() => ({ id, user: '', created_at: '', updated_at: '', deleted_at: null })),
};

