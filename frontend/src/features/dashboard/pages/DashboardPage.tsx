import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { FileText, Calendar, Users, TrendingUp, Plus, ArrowRight, Sparkles, Clock, MessagesSquare } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '@/shared/components/ui/button';
import { useQuery } from '@tanstack/react-query';
import { postsApi, eventsApi, communitiesApi } from '@/shared/api';
import { formatDate } from '@/shared/lib/utils';

export const DashboardPage = () => {
  // Загрузка данных из API
  const { data: postsData } = useQuery({
    queryKey: ['posts'],
    queryFn: () => postsApi.list(),
  });

  const { data: eventsData } = useQuery({
    queryKey: ['events'],
    queryFn: () => eventsApi.list(),
  });

  const { data: communitiesData } = useQuery({
    queryKey: ['communities'],
    queryFn: () => communitiesApi.list(),
  });

  // Преобразование данных в массивы
  const posts = Array.isArray(postsData) ? postsData : (postsData as any)?.results || [];
  const events = Array.isArray(eventsData) ? eventsData : (eventsData as any)?.results || [];
  const communities = Array.isArray(communitiesData) ? communitiesData : (communitiesData as any)?.results || [];

  // Последние 4 поста
  const recentPosts = posts.slice(0, 4);

  // Предстоящие события (сортируем по дате)
  const upcomingEvents = events
    .filter((event: any) => new Date(event.start_at) >= new Date())
    .sort((a: any, b: any) => new Date(a.start_at).getTime() - new Date(b.start_at).getTime())
    .slice(0, 3);

  // Статистика активности (посты за последние 24 часа)
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const todayActivity = posts.filter((post: any) => 
    new Date(post.created_at) >= today
  ).length;

  return (
    <div className="space-y-8 pb-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary via-primary/90 to-primary/80 p-8 text-primary-foreground shadow-lg">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="h-5 w-5 animate-pulse" />
              <span className="text-sm font-medium opacity-90">Добро пожаловать в Hubbly</span>
            </div>
            <h1 className="text-4xl font-bold tracking-tight">Ваша главная страница</h1>
            <p className="text-primary-foreground/80 max-w-2xl">
              Социальная платформа для создания и развития сообществ
            </p>
          </div>
          <Button size="lg" variant="secondary" asChild className="shadow-lg">
            <Link to="/posts/create" className="gap-2">
              <Plus className="h-5 w-5" />
              Создать пост
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="relative overflow-hidden border-none shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
          <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full -mr-16 -mt-16"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Посты</CardTitle>
            <div className="h-10 w-10 rounded-full bg-blue-500/10 flex items-center justify-center">
              <FileText className="h-5 w-5 text-blue-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600">{posts.length}</div>
            <p className="text-xs text-muted-foreground mt-1">Всего публикаций</p>
          </CardContent>
        </Card>

        <Card className="relative overflow-hidden border-none shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
          <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 rounded-full -mr-16 -mt-16"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">События</CardTitle>
            <div className="h-10 w-10 rounded-full bg-purple-500/10 flex items-center justify-center">
              <Calendar className="h-5 w-5 text-purple-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-purple-600">{upcomingEvents.length}</div>
            <p className="text-xs text-muted-foreground mt-1">Предстоящих</p>
          </CardContent>
        </Card>

        <Card className="relative overflow-hidden border-none shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
          <div className="absolute top-0 right-0 w-32 h-32 bg-green-500/10 rounded-full -mr-16 -mt-16"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Сообщества</CardTitle>
            <div className="h-10 w-10 rounded-full bg-green-500/10 flex items-center justify-center">
              <Users className="h-5 w-5 text-green-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600">{communities.length}</div>
            <p className="text-xs text-muted-foreground mt-1">Активных групп</p>
          </CardContent>
        </Card>

        <Card className="relative overflow-hidden border-none shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
          <div className="absolute top-0 right-0 w-32 h-32 bg-orange-500/10 rounded-full -mr-16 -mt-16"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Активность</CardTitle>
            <div className="h-10 w-10 rounded-full bg-orange-500/10 flex items-center justify-center">
              <TrendingUp className="h-5 w-5 text-orange-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-orange-600">{todayActivity}</div>
            <p className="text-xs text-muted-foreground mt-1">Постов сегодня</p>
          </CardContent>
        </Card>
      </div>

      {/* Content Grid */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Recent Posts */}
        <Card className="lg:col-span-2 border-none shadow-lg">
          <CardHeader className="border-b bg-muted/30">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-xl">Последние посты</CardTitle>
                <CardDescription>Свежий контент от сообщества</CardDescription>
              </div>
              <Button asChild variant="ghost" size="sm" className="gap-1">
                <Link to="/posts">
                  Все посты
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent className="pt-6">
            {recentPosts.length === 0 ? (
              <div className="text-center py-12">
                <div className="mx-auto w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
                  <MessagesSquare className="h-8 w-8 text-muted-foreground" />
                </div>
                <p className="text-muted-foreground mb-4">Пока нет постов</p>
                <Button asChild size="sm">
                  <Link to="/posts/create">Создать первый пост</Link>
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {recentPosts.map((post: any) => (
                  <Link
                    key={post.id}
                    to={`/posts/${post.id}`}
                    className="group block p-4 rounded-xl border border-border hover:border-primary/50 hover:bg-accent/50 transition-all duration-200"
                  >
                    <div className="space-y-3">
                      <div className="flex items-start gap-3">
                        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center text-sm font-bold">
                          {post.author_username?.[0]?.toUpperCase() || 'U'}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">
                            {post.author_username}
                          </p>
                          <p className="text-xs text-muted-foreground flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {formatDate(post.created_at)}
                          </p>
                        </div>
                      </div>
                      
                      <p className="text-sm font-medium line-clamp-2 group-hover:text-primary transition-colors">
                        {post.content.split('\n')[0].slice(0, 120)}
                        {post.content.length > 120 ? '...' : ''}
                      </p>
                      
                      {post.tags && post.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1.5">
                          {post.tags.slice(0, 3).map((tag: any) => (
                            <span
                              key={tag.id}
                              className="px-2 py-1 text-xs bg-primary/10 text-primary rounded-md font-medium"
                            >
                              #{tag.name}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <Card className="border-none shadow-lg overflow-hidden">
            <div className="bg-gradient-to-br from-primary/10 to-primary/5 p-4 border-b">
              <CardTitle className="text-lg">Быстрые действия</CardTitle>
              <CardDescription>Создайте новый контент</CardDescription>
            </div>
            <CardContent className="pt-4 space-y-2">
              <Button asChild className="w-full justify-start gap-2 h-11 shadow-sm">
                <Link to="/posts/create">
                  <Plus className="h-4 w-4" />
                  Создать пост
                </Link>
              </Button>
              <Button asChild variant="outline" className="w-full justify-start gap-2 h-11 hover:bg-accent">
                <Link to="/events">
                  <Calendar className="h-4 w-4" />
                  Смотреть события
                </Link>
              </Button>
              <Button asChild variant="outline" className="w-full justify-start gap-2 h-11 hover:bg-accent">
                <Link to="/communities">
                  <Users className="h-4 w-4" />
                  Найти сообщество
                </Link>
              </Button>
            </CardContent>
          </Card>

          {/* Upcoming Events */}
          <Card className="border-none shadow-lg">
            <div className="bg-gradient-to-br from-purple-500/10 to-purple-500/5 p-4 border-b">
              <CardTitle className="text-lg">Предстоящие события</CardTitle>
              <CardDescription>Не пропустите интересное</CardDescription>
            </div>
            <CardContent className="pt-4">
              {upcomingEvents.length === 0 ? (
                <div className="text-center py-8">
                  <div className="mx-auto w-12 h-12 rounded-full bg-muted flex items-center justify-center mb-3">
                    <Calendar className="h-6 w-6 text-muted-foreground" />
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Нет предстоящих событий
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {upcomingEvents.map((event: any) => (
                    <Link
                      key={event.id}
                      to={`/events/${event.id}`}
                      className="group block p-3 rounded-lg border hover:border-purple-500/50 hover:bg-purple-500/5 transition-all duration-200"
                    >
                      <h4 className="font-semibold text-sm mb-2 line-clamp-1 group-hover:text-purple-600 transition-colors">
                        {event.title}
                      </h4>
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          <span>{formatDate(event.start_at)}</span>
                        </div>
                        {event.capacity && (
                          <div className="flex items-center gap-1 bg-muted px-2 py-0.5 rounded">
                            <Users className="h-3 w-3" />
                            <span>{event.capacity}</span>
                          </div>
                        )}
                      </div>
                    </Link>
                  ))}
                  <Button asChild variant="ghost" size="sm" className="w-full gap-1 mt-2">
                    <Link to="/events">
                      Все события
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};