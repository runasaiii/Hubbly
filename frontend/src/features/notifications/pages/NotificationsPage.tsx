import { useQuery } from '@tanstack/react-query';
import { notificationsApi } from '@/shared/api';
import { Card, CardContent } from '@/shared/components/ui/card';
import { formatDate } from '@/shared/lib/utils';

export const NotificationsPage = () => {
  const { data: notifications, isLoading } = useQuery({
    queryKey: ['notifications'],
    queryFn: () => notificationsApi.list(),
  });

  const notificationsArray = Array.isArray(notifications) ? notifications : (notifications as any)?.results || [];

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Уведомления</h1>
        <p className="text-muted-foreground">Ваши уведомления</p>
      </div>

      <div className="space-y-2">
        {notificationsArray.length === 0 ? (
          <Card>
            <CardContent className="py-8 text-center text-muted-foreground">
              Нет уведомлений
            </CardContent>
          </Card>
        ) : (
          notificationsArray.map((notification: any) => (
            <Card key={notification.id}>
              <CardContent className="py-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Уведомление #{notification.id}</p>
                    <p className="text-sm text-muted-foreground">
                      {formatDate(notification.created_at)}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

