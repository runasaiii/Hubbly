import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { eventsApi } from '@/shared/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Button } from '@/shared/components/ui/button';
import { formatDate } from '@/shared/lib/utils';
import { Calendar, Clock, MapPin, Users, Sparkles, Plus, ArrowRight, Filter } from 'lucide-react';

export const EventsListPage = () => {
  const { data: events, isLoading } = useQuery({
    queryKey: ['events'],
    queryFn: () => eventsApi.list(),
  });

  const eventsArray = Array.isArray(events) ? events : (events as any)?.results || [];
  
  // Разделяем события на предстоящие и прошедшие
  const now = new Date();
  const upcomingEvents = eventsArray.filter((event: any) => new Date(event.start_at) >= now);
  const pastEvents = eventsArray.filter((event: any) => new Date(event.start_at) < now);

  // Функция для определения цвета статуса
  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'upcoming':
      case 'scheduled':
        return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'ongoing':
      case 'active':
        return 'bg-green-100 text-green-700 border-green-200';
      case 'completed':
      case 'finished':
        return 'bg-gray-100 text-gray-700 border-gray-200';
      case 'cancelled':
        return 'bg-red-100 text-red-700 border-red-200';
      default:
        return 'bg-purple-100 text-purple-700 border-purple-200';
    }
  };

  // Функция для перевода статуса
  const translateStatus = (status: string) => {
    const translations: { [key: string]: string } = {
      'upcoming': 'Предстоящее',
      'scheduled': 'Запланировано',
      'ongoing': 'В процессе',
      'active': 'Активно',
      'completed': 'Завершено',
      'finished': 'Завершено',
      'cancelled': 'Отменено'
    };
    return translations[status?.toLowerCase()] || status;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="space-y-4 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Загрузка событий...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary via-primary/90 to-primary/80 p-8 text-primary-foreground shadow-lg">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative flex items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="h-5 w-5 animate-pulse" />
              <span className="text-sm font-medium opacity-90">Календарь мероприятий</span>
            </div>
            <h1 className="text-4xl font-bold tracking-tight">События</h1>
            <p className="text-white/80">
              {eventsArray.length > 0 
                ? `${upcomingEvents.length} предстоящих из ${eventsArray.length} всего`
                : 'Пока нет запланированных событий'
              }
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="secondary" size="sm" className="gap-2">
              <Filter className="h-4 w-4" />
              Фильтры
            </Button>
            <Button size="sm" variant="secondary" className="gap-2 shadow-lg">
              <Plus className="h-5 w-5" />
              Создать событие
            </Button>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="border-none shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-blue-500/10 flex items-center justify-center">
                <Calendar className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{upcomingEvents.length}</p>
                <p className="text-xs text-muted-foreground">Предстоящих событий</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-none shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-purple-500/10 flex items-center justify-center">
                <Users className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{eventsArray.length}</p>
                <p className="text-xs text-muted-foreground">Всего событий</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-none shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-gray-500/10 flex items-center justify-center">
                <Clock className="h-5 w-5 text-gray-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{pastEvents.length}</p>
                <p className="text-xs text-muted-foreground">Прошедших событий</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Empty State */}
      {eventsArray.length === 0 ? (
        <Card className="border-none shadow-lg">
          <CardContent className="py-16 text-center">
            <div className="mx-auto w-20 h-20 rounded-full bg-gradient-to-br from-orange-500/20 to-purple-500/20 flex items-center justify-center mb-6">
              <Calendar className="h-10 w-10 text-orange-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Нет событий</h3>
            <p className="text-muted-foreground mb-6">
              Пока нет запланированных событий. Создайте первое мероприятие!
            </p>
            <Button className="gap-2">
              <Plus className="h-4 w-4" />
              Создать событие
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Upcoming Events */}
          {upcomingEvents.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  <Calendar className="h-6 w-6 text-primary" />
                  Предстоящие события
                </h2>
                <span className="text-sm text-muted-foreground">
                  {upcomingEvents.length} {upcomingEvents.length === 1 ? 'событие' : 'событий'}
                </span>
              </div>
              
              <div className="grid gap-6 md:grid-cols-2">
                {upcomingEvents.map((event: any, index: number) => (
                  <Card 
                    key={event.id} 
                    className="group border-none shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden"
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <div className="h-2 bg-gradient-to-r from-orange-500 to-purple-600"></div>
                    <CardHeader className="bg-gradient-to-r from-muted/30 to-transparent">
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <CardTitle className="text-xl group-hover:text-primary transition-colors line-clamp-1">
                          {event.title}
                        </CardTitle>
                        <span className={`px-2 py-1 text-xs rounded-full border font-medium flex-shrink-0 ${getStatusColor(event.status)}`}>
                          {translateStatus(event.status)}
                        </span>
                      </div>
                      <CardDescription className="flex items-center gap-2">
                        <Clock className="h-3 w-3" />
                        {formatDate(event.start_at)}
                      </CardDescription>
                    </CardHeader>
                    
                    <CardContent className="space-y-4">
                      <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">
                        {event.description || 'Описание отсутствует'}
                      </p>
                      
                      <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
                        {event.location && (
                          <div className="flex items-center gap-1 px-2 py-1 bg-muted rounded-md">
                            <MapPin className="h-3 w-3" />
                            <span>{event.location}</span>
                          </div>
                        )}
                        {event.capacity && (
                          <div className="flex items-center gap-1 px-2 py-1 bg-muted rounded-md">
                            <Users className="h-3 w-3" />
                            <span>До {event.capacity} чел.</span>
                          </div>
                        )}
                      </div>
                      
                      <Button variant="outline" size="sm" asChild className="w-full gap-2 group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                        <Link to={`/events/${event.id}`}>
                          Подробнее
                          <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                        </Link>
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* Past Events */}
          {pastEvents.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold flex items-center gap-2 text-muted-foreground">
                  <Clock className="h-6 w-6" />
                  Прошедшие события
                </h2>
                <span className="text-sm text-muted-foreground">
                  {pastEvents.length} {pastEvents.length === 1 ? 'событие' : 'событий'}
                </span>
              </div>
              
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {pastEvents.slice(0, 6).map((event: any) => (
                  <Card 
                    key={event.id} 
                    className="border-none shadow-sm hover:shadow-md transition-shadow opacity-75 hover:opacity-100"
                  >
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base line-clamp-1">{event.title}</CardTitle>
                      <CardDescription className="flex items-center gap-1 text-xs">
                        <Clock className="h-3 w-3" />
                        {formatDate(event.start_at)}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <Button variant="ghost" size="sm" asChild className="w-full gap-1">
                        <Link to={`/events/${event.id}`}>
                          Подробнее
                          <ArrowRight className="h-3 w-3" />
                        </Link>
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};