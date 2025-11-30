import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { postsApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { formatDate } from '@/shared/lib/utils';
import { Plus } from 'lucide-react';

export const PostsListPage = () => {
  const { data: posts, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: () => postsApi.list(),
  });

  const postsArray = Array.isArray(posts) ? posts : (posts as any)?.results || [];

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  if (error) {
    return <div className="text-center py-8 text-red-600">Ошибка загрузки постов</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Посты</h1>
          <p className="text-muted-foreground">Все посты сообщества</p>
        </div>
        <Button asChild>
          <Link to="/posts/create">
            <Plus className="mr-2 h-4 w-4" />
            Создать пост
          </Link>
        </Button>
      </div>

      <div className="grid gap-4">
        {postsArray.length === 0 ? (
          <Card>
            <CardContent className="py-8 text-center text-muted-foreground">
              Пока нет постов. Создайте первый!
            </CardContent>
          </Card>
        ) : (
          postsArray.map((post: any) => (
            <Card key={post.id} className="hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-lg">{post.author_username}</CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {formatDate(post.created_at)}
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="mb-4 whitespace-pre-wrap">{post.content}</p>
                {post.tags && post.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.tags.map((tag: any) => (
                      <span
                        key={tag.id}
                        className="px-2 py-1 text-xs bg-secondary rounded-md"
                      >
                        #{tag.name}
                      </span>
                    ))}
                  </div>
                )}
                <Button variant="outline" size="sm" asChild>
                  <Link to={`/posts/${post.id}`}>Читать далее</Link>
                </Button>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

