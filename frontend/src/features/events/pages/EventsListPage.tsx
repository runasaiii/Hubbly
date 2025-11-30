import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { eventsApi } from '@/shared/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Button } from '@/shared/components/ui/button';
import { formatDate } from '@/shared/lib/utils';

export const EventsListPage = () => {
  const { data: events, isLoading } = useQuery({
    queryKey: ['events'],
    queryFn: () => eventsApi.list(),
  });

  const eventsArray = Array.isArray(events) ? events : (events as any)?.results || [];

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">События</h1>
        <p className="text-muted-foreground">Предстоящие события</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {eventsArray.map((event: any) => (
          <Card key={event.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <CardTitle>{event.title}</CardTitle>
              <CardDescription>
                {formatDate(event.start_at)}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm mb-4 line-clamp-2">{event.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-xs text-muted-foreground">
                  Статус: {event.status}
                </span>
                <Button variant="outline" size="sm" asChild>
                  <Link to={`/events/${event.id}`}>Подробнее</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

