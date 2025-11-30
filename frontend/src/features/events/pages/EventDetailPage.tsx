import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { eventsApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { formatDate } from '@/shared/lib/utils';
import { 
  ArrowLeft, 
  Calendar, 
  Clock, 
  MapPin, 
  Users, 
  User, 
  Share2, 
  BookmarkPlus,
  CheckCircle2,
  XCircle,
  AlertCircle
} from 'lucide-react';

export const EventDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: event, isLoading } = useQuery({
    queryKey: ['event', id],
    queryFn: () => eventsApi.get(id!),
    enabled: !!id,
  });

  // Функция для определения цвета и иконки статуса
  const getStatusInfo = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'upcoming':
      case 'scheduled':
        return {
          color: 'bg-blue-100 text-blue-700 border-blue-200',
          icon: <Clock className="h-4 w-4" />,
          text: 'Предстоящее'
        };
      case 'ongoing':
      case 'active':
        return {
          color: 'bg-green-100 text-green-700 border-green-200',
          icon: <CheckCircle2 className="h-4 w-4" />,
          text: 'В процессе'
        };
      case 'completed':
      case 'finished':
        return {
          color: 'bg-gray-100 text-gray-700 border-gray-200',
          icon: <CheckCircle2 className="h-4 w-4" />,
          text: 'Завершено'
        };
      case 'cancelled':
        return {
          color: 'bg-red-100 text-red-700 border-red-200',
          icon: <XCircle className="h-4 w-4" />,
          text: 'Отменено'
        };
      default:
        return {
          color: 'bg-purple-100 text-purple-700 border-purple-200',
          icon: <AlertCircle className="h-4 w-4" />,
          text: status
        };
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="space-y-4 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Загрузка события...</p>
        </div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="flex items-center justify-center py-16 max-w-2xl mx-auto">
        <Card className="border-none shadow-lg">
          <CardContent className="py-12 text-center">
            <div className="mx-auto w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
              <Calendar className="h-8 w-8 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Событие не найдено</h3>
            <p className="text-muted-foreground mb-6">
              Возможно, оно было удалено или не существует
            </p>
            <Button onClick={() => navigate('/events')} className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Вернуться к событиям
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const statusInfo = getStatusInfo(event.status);
  const eventDate = new Date(event.start_at);
  const isUpcoming = eventDate >= new Date();

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-8">
      {/* Back Button */}
      <Button 
        variant="ghost" 
        onClick={() => navigate('/events')}
        className="gap-2 hover:gap-3 transition-all"
      >
        <ArrowLeft className="h-4 w-4" />
        Назад к событиям
      </Button>

      {/* Hero Card */}
      <Card className="border-none shadow-xl overflow-hidden">
        <div className="h-3 bg-gradient-to-r from-orange-500 via-pink-600 to-purple-600"></div>
        
        <CardHeader className="bg-gradient-to-r from-muted/30 to-transparent pb-6">
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-3">
                <span className={`px-3 py-1.5 text-sm rounded-full border font-medium flex items-center gap-1.5 ${statusInfo.color}`}>
                  {statusInfo.icon}
                  {statusInfo.text}
                </span>
                {isUpcoming && (
                  <span className="px-3 py-1.5 text-sm rounded-full bg-orange-100 text-orange-700 border border-orange-200 font-medium">
                    Скоро
                  </span>
                )}
              </div>
              <CardTitle className="text-3xl md:text-4xl mb-3">
                {event.title}
              </CardTitle>
              <p className="text-muted-foreground leading-relaxed">
                {event.description || 'Описание события отсутствует'}
              </p>
            </div>
            
            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="gap-2">
                <Share2 className="h-4 w-4" />
                Поделиться
              </Button>
              <Button variant="outline" size="sm" className="gap-2">
                <BookmarkPlus className="h-4 w-4" />
                Сохранить
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-6">
          <div className="grid gap-6 md:grid-cols-2">
            {/* Date & Time */}
            <Card className="border-none shadow-md bg-gradient-to-br from-blue-50 to-blue-100/50">
              <CardContent className="pt-6">
                <div className="flex items-start gap-4">
                  <div className="h-12 w-12 rounded-full bg-blue-500 flex items-center justify-center text-white flex-shrink-0">
                    <Calendar className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg mb-3">Дата и время</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2">
                        <Clock className="h-4 w-4 text-muted-foreground" />
                        <div>
                          <p className="font-medium">Начало</p>
                          <p className="text-muted-foreground">{formatDate(event.start_at)}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Clock className="h-4 w-4 text-muted-foreground" />
                        <div>
                          <p className="font-medium">Окончание</p>
                          <p className="text-muted-foreground">{formatDate(event.end_at)}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Details */}
            <Card className="border-none shadow-md bg-gradient-to-br from-purple-50 to-purple-100/50">
              <CardContent className="pt-6">
                <div className="flex items-start gap-4">
                  <div className="h-12 w-12 rounded-full bg-purple-500 flex items-center justify-center text-white flex-shrink-0">
                    <Users className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg mb-3">Детали</h3>
                    <div className="space-y-2 text-sm">
                      {event.capacity && (
                        <div className="flex items-center gap-2">
                          <Users className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <p className="font-medium">Вместимость</p>
                            <p className="text-muted-foreground">До {event.capacity} участников</p>
                          </div>
                        </div>
                      )}
                      {event.location && (
                        <div className="flex items-center gap-2">
                          <MapPin className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <p className="font-medium">Локация</p>
                            <p className="text-muted-foreground">{event.location}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      {/* Organizer Card */}
      <Card className="border-none shadow-lg">
        <CardHeader className="bg-gradient-to-r from-muted/30 to-transparent border-b">
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5 text-primary" />
            Организатор
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <Link 
            to={`/profile/${event.organizer}`}
            className="flex items-center gap-4 p-4 rounded-lg hover:bg-muted/50 transition-colors group"
          >
            <div className="h-14 w-14 rounded-full bg-gradient-to-br from-orange-500 to-purple-500 flex items-center justify-center text-xl font-bold text-white shadow-md">
              {event.organizer_username?.[0]?.toUpperCase() || 'O'}
            </div>
            <div className="flex-1">
              <p className="font-semibold text-lg group-hover:text-primary transition-colors">
                {event.organizer_username}
              </p>
              <p className="text-sm text-muted-foreground">Организатор мероприятия</p>
            </div>
            <ArrowLeft className="h-5 w-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all rotate-180" />
          </Link>
        </CardContent>
      </Card>

      {/* Action Button */}
      {isUpcoming && event.status?.toLowerCase() !== 'cancelled' && (
        <Card className="border-none shadow-lg bg-gradient-to-br from-primary/5 to-primary/10">
          <CardContent className="py-8 text-center">
            <h3 className="text-xl font-semibold mb-2">Хотите принять участие?</h3>
            <p className="text-muted-foreground mb-6">
              Зарегистрируйтесь на событие прямо сейчас
            </p>
            <Button size="lg" className="gap-2 shadow-md">
              <CheckCircle2 className="h-5 w-5" />
              Участвовать в событии
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};