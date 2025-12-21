import { apiClient } from '@/shared/lib/api';
import type { Event, EventApplication, CreateEventRequest, ApplyToEventRequest, PaginatedResponse } from '@/shared/types';

export const eventsApi = {
  list: (params?: { community?: string; status?: string; search?: string; requires_approval?: boolean }): Promise<Event[] | PaginatedResponse<Event>> =>
    apiClient.get('/events/api/', { params }),

  get: (id: string): Promise<Event> =>
    apiClient.get(`/events/api/${id}/`),

  create: (data: CreateEventRequest): Promise<Event> =>
    apiClient.post('/events/api/', data),

  update: (id: string, data: Partial<CreateEventRequest>): Promise<Event> =>
    apiClient.put(`/events/api/${id}/`, data),

  delete: (id: string): Promise<void> =>
    apiClient.delete(`/events/api/${id}/`),

  apply: (eventId: string, data?: ApplyToEventRequest): Promise<EventApplication> =>
    apiClient.post(`/events/api/${eventId}/apply/`, data),

  getApplications: (eventId: string): Promise<EventApplication[]> =>
    apiClient.get(`/events/api/${eventId}/applications/`).catch(() => []),

  reviewApplication: (eventId: string, applicationId: string, status: 'approved' | 'declined'): Promise<EventApplication> =>
    apiClient.patch(`/events/api/${eventId}/applications/${applicationId}/`, { status }),
};

