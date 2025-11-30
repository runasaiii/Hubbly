import { useQuery } from '@tanstack/react-query';
import { notificationsApi } from '@/shared/api';
import { Card, CardContent } from '@/shared/components/ui/card';
import { Button } from '@/shared/components/ui/button';
import { formatDate } from '@/shared/lib/utils';
import { Bell, BellOff, Check, Sparkles, MessageSquare, Heart, UserPlus, Calendar, Trash2 } from 'lucide-react';

export const NotificationsPage = () => {
  const { data: notifications, isLoading } = useQuery({
    queryKey: ['notifications'],
    queryFn: () => notificationsApi.list(),
  });

  const notificationsArray = Array.isArray(notifications) ? notifications : (notifications as any)?.results || [];
  const unreadCount = notificationsArray.filter((n: any) => !n.is_read).length;

  // Функция для определения иконки по типу уведомления
  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'comment':
        return <MessageSquare className="h-5 w-5" />;
      case 'like':
        return <Heart className="h-5 w-5" />;
      case 'follow':
        return <UserPlus className="h-5 w-5" />;
      case 'event':
        return <Calendar className="h-5 w-5" />;
      default:
        return <Bell className="h-5 w-5" />;
    }
  };

  // Функция для определения цвета по типу уведомления
  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'comment':
        return 'from-blue-500 to-blue-600';
      case 'like':
        return 'from-red-500 to-pink-600';
      case 'follow':
        return 'from-green-500 to-emerald-600';
      case 'event':
        return 'from-purple-500 to-purple-600';
      default:
        return 'from-gray-500 to-gray-600';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="space-y-4 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Загрузка уведомлений...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary via-primary/90 to-primary/80 p-8 text-primary-foreground shadow-lg">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative flex items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="h-5 w-5 animate-pulse" />
              <span className="text-sm font-medium opacity-90">Центр уведомлений</span>
            </div>
            <h1 className="text-4xl font-bold tracking-tight">Уведомления</h1>
            <p className="text-white/80">
              {notificationsArray.length > 0 
                ? `У вас ${notificationsArray.length} ${notificationsArray.length === 1 ? 'уведомление' : 'уведомлений'}`
                : 'Нет новых уведомлений'
              }
              {unreadCount > 0 && (
                <span className="ml-2 px-2 py-0.5 bg-white/20 rounded-full text-sm">
                  {unreadCount} непрочитанных
                </span>
              )}
            </p>
          </div>
          {notificationsArray.length > 0 && (
            <Button variant="secondary" size="lg" className="gap-2 shadow-lg">
              <Check className="h-5 w-5" />
              Прочитать все
            </Button>
          )}
        </div>
      </div>

      {/* Stats Cards */}
      {notificationsArray.length > 0 && (
        <div className="grid gap-4 md:grid-cols-3">
          <Card className="border-none shadow-md">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-blue-500/10 flex items-center justify-center">
                  <Bell className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{notificationsArray.length}</p>
                  <p className="text-xs text-muted-foreground">Всего уведомлений</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-none shadow-md">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-green-500/10 flex items-center justify-center">
                  <Check className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{notificationsArray.length - unreadCount}</p>
                  <p className="text-xs text-muted-foreground">Прочитано</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-none shadow-md">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-orange-500/10 flex items-center justify-center">
                  <BellOff className="h-5 w-5 text-orange-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{unreadCount}</p>
                  <p className="text-xs text-muted-foreground">Непрочитано</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Notifications List */}
      <div className="space-y-3">
        {notificationsArray.length === 0 ? (
          <Card className="border-none shadow-lg">
            <CardContent className="py-16 text-center">
              <div className="mx-auto w-20 h-20 rounded-full bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center mb-6">
                <BellOff className="h-10 w-10 text-indigo-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Нет уведомлений</h3>
              <p className="text-muted-foreground mb-6">
                У вас пока нет новых уведомлений. Мы сообщим вам о важных событиях!
              </p>
              <div className="flex justify-center gap-2 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <MessageSquare className="h-4 w-4" />
                  <span>Комментарии</span>
                </div>
                <span>•</span>
                <div className="flex items-center gap-1">
                  <Heart className="h-4 w-4" />
                  <span>Лайки</span>
                </div>
                <span>•</span>
                <div className="flex items-center gap-1">
                  <UserPlus className="h-4 w-4" />
                  <span>Подписки</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ) : (
          notificationsArray.map((notification: any, index: number) => {
            const notificationType = notification.type || 'default';
            const isUnread = !notification.is_read;
            
            return (
              <Card 
                key={notification.id}
                className={`group border-none shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden ${
                  isUnread ? 'bg-primary/5' : ''
                }`}
                style={{ animationDelay: `${index * 50}ms` }}
              >
                <CardContent className="p-0">
                  <div className="flex items-start gap-4 p-4">
                    {/* Icon */}
                    <div className={`flex-shrink-0 h-12 w-12 rounded-full bg-gradient-to-br ${getNotificationColor(notificationType)} flex items-center justify-center text-white shadow-md`}>
                      {getNotificationIcon(notificationType)}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <div className="flex items-center gap-2">
                          <p className="font-semibold text-base">
                            Уведомление #{notification.id}
                          </p>
                          {isUnread && (
                            <span className="px-2 py-0.5 bg-primary text-primary-foreground text-xs rounded-full font-medium">
                              Новое
                            </span>
                          )}
                        </div>
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-3">
                        {notification.message || 'У вас новое уведомление'}
                      </p>
                      
                      <div className="flex items-center gap-4 text-xs text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Bell className="h-3 w-3" />
                          <span>{formatDate(notification.created_at)}</span>
                        </div>
                        {notification.type && (
                          <>
                            <span>•</span>
                            <span className="capitalize">{notification.type}</span>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex-shrink-0 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      {isUnread && (
                        <Button variant="ghost" size="sm" className="gap-1">
                          <Check className="h-4 w-4" />
                        </Button>
                      )}
                      <Button variant="ghost" size="sm" className="gap-1 text-red-600 hover:text-red-700">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })
        )}
      </div>

      {/* Load More */}
      {notificationsArray.length >= 10 && (
        <div className="text-center pt-4">
          <Button variant="outline" size="lg" className="gap-2">
            <Bell className="h-4 w-4" />
            Загрузить старые уведомления
          </Button>
        </div>
      )}
    </div>
  );
};