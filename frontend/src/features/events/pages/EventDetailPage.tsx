import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { eventsApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { formatDate } from '@/shared/lib/utils';

export const EventDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: event, isLoading } = useQuery({
    queryKey: ['event', id],
    queryFn: () => eventsApi.get(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  if (!event) {
    return <div className="text-center py-8">Событие не найдено</div>;
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <Button variant="ghost" onClick={() => navigate('/events')}>
        ← Назад
      </Button>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{event.title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p>{event.description}</p>
          <div className="grid gap-2 text-sm">
            <div>
              <span className="font-medium">Начало:</span> {formatDate(event.start_at)}
            </div>
            <div>
              <span className="font-medium">Конец:</span> {formatDate(event.end_at)}
            </div>
            {event.capacity && (
              <div>
                <span className="font-medium">Вместимость:</span> {event.capacity}
              </div>
            )}
            <div>
              <span className="font-medium">Организатор:</span> {event.organizer_username}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

