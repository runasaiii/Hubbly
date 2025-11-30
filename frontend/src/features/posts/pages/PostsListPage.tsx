import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { postsApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { formatDate } from '@/shared/lib/utils';
import { Plus, Clock, MessageSquare, Heart, Sparkles } from 'lucide-react';

export const PostsListPage = () => {
  const { data: posts, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: () => postsApi.list(),
  });

  const postsArray = Array.isArray(posts) ? posts : (posts as any)?.results || [];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="space-y-4 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Загрузка постов...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center py-16">
        <Card className="max-w-md border-red-200 bg-red-50">
          <CardContent className="py-8 text-center">
            <div className="mx-auto w-12 h-12 rounded-full bg-red-100 flex items-center justify-center mb-4">
              <MessageSquare className="h-6 w-6 text-red-600" />
            </div>
            <p className="text-red-600 font-medium">Ошибка загрузки постов</p>
            <p className="text-sm text-red-500 mt-2">Попробуйте обновить страницу</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-8">
      {/* Hero Header */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-500 via-blue-600 to-purple-600 p-8 text-white shadow-xl">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative flex items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="h-5 w-5 animate-pulse" />
              <span className="text-sm font-medium opacity-90">Лента публикаций</span>
            </div>
            <h1 className="text-4xl font-bold tracking-tight">Посты</h1>
            <p className="text-white/80">
              {postsArray.length > 0 
                ? `${postsArray.length} ${postsArray.length === 1 ? 'публикация' : 'публикаций'} от сообщества`
                : 'Будьте первым, кто создаст пост'
              }
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

      {/* Posts Grid */}
      <div className="space-y-6">
        {postsArray.length === 0 ? (
          <Card className="border-none shadow-lg">
            <CardContent className="py-16 text-center">
              <div className="mx-auto w-20 h-20 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center mb-6">
                <MessageSquare className="h-10 w-10 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Пока нет постов</h3>
              <p className="text-muted-foreground mb-6">
                Станьте первым, кто поделится своими мыслями с сообществом
              </p>
              <Button asChild size="lg" className="gap-2">
                <Link to="/posts/create">
                  <Plus className="h-4 w-4" />
                  Создать первый пост
                </Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          postsArray.map((post: any, index: number) => (
            <Card 
              key={post.id} 
              className="group border-none shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <CardHeader className="border-b bg-gradient-to-r from-muted/30 to-transparent">
                <div className="flex items-start justify-between">
                  <Link 
                    to={`/profile/${post.author}`}
                    className="flex items-center gap-4 hover:opacity-80 transition-opacity"
                  >
                    <div className="relative">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-lg font-bold text-white shadow-md">
                        {post.author_username?.[0]?.toUpperCase() || 'U'}
                      </div>
                      <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
                    </div>
                    <div>
                      <CardTitle className="text-lg hover:text-primary transition-colors cursor-pointer">
                        {post.author_username}
                      </CardTitle>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground mt-1">
                        <Clock className="h-3 w-3" />
                        <span>{formatDate(post.created_at)}</span>
                      </div>
                    </div>
                  </Link>
                </div>
              </CardHeader>
              
              <CardContent className="pt-6">
                {/* Content Preview */}
                <div className="mb-6">
                  <p className="text-base leading-relaxed whitespace-pre-wrap line-clamp-4">
                    {post.content}
                  </p>
                  {post.content.length > 200 && (
                    <Link 
                      to={`/posts/${post.id}`}
                      className="inline-flex items-center text-sm text-primary hover:underline mt-2 font-medium"
                    >
                      Читать полностью
                    </Link>
                  )}
                </div>

                {/* Tags */}
                {post.tags && post.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-6">
                    {post.tags.map((tag: any) => (
                      <span
                        key={tag.id}
                        className="px-3 py-1.5 text-xs bg-primary/10 text-primary rounded-full font-medium hover:bg-primary/20 transition-colors cursor-pointer"
                      >
                        #{tag.name}
                      </span>
                    ))}
                  </div>
                )}

                {/* Actions */}
                <div className="flex items-center justify-between pt-4 border-t">
                  <div className="flex items-center gap-6">
                    <button className="flex items-center gap-2 text-sm text-muted-foreground hover:text-red-500 transition-colors">
                      <Heart className="h-4 w-4" />
                      <span>Нравится</span>
                    </button>
                    <Link 
                      to={`/posts/${post.id}`}
                      className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors"
                    >
                      <MessageSquare className="h-4 w-4" />
                      <span>Комментарии</span>
                    </Link>
                  </div>
                  
                  <Button variant="ghost" size="sm" asChild className="gap-2">
                    <Link to={`/posts/${post.id}`}>
                      Подробнее
                    </Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Load More Placeholder */}
      {postsArray.length > 0 && postsArray.length >= 10 && (
        <div className="text-center pt-4">
          <Button variant="outline" size="lg" disabled className="gap-2">
            <Clock className="h-4 w-4" />
            Загрузить ещё
          </Button>
          <p className="text-xs text-muted-foreground mt-2">
            Скоро будет доступна пагинация
          </p>
        </div>
      )}
    </div>
  );
};