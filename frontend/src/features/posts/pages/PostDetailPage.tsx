import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { postsApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Textarea } from '@/shared/components/ui/textarea';
import { formatDate } from '@/shared/lib/utils';
import { useAuth } from '@/features/auth/context/AuthContext';
import { useState } from 'react';

export const PostDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [comment, setComment] = useState('');
  const queryClient = useQueryClient();

  const { data: post, isLoading } = useQuery({
    queryKey: ['post', id],
    queryFn: () => postsApi.get(id!),
    enabled: !!id,
  });

  const { data: comments = [] } = useQuery({
    queryKey: ['post-comments', id],
    queryFn: () => postsApi.getComments(id!),
    enabled: !!id,
  });

  const createCommentMutation = useMutation({
    mutationFn: postsApi.createComment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['post-comments', id] });
      setComment('');
    },
  });

  const handleSubmitComment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!comment.trim() || !id) return;
    createCommentMutation.mutate({ post: id, content: comment });
  };

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  if (!post) {
    return <div className="text-center py-8">Пост не найден</div>;
  }

  const isAuthor = user?.id === post.author;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <Button variant="ghost" onClick={() => navigate('/posts')}>
        ← Назад к постам
      </Button>

      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle>{post.author_username}</CardTitle>
              <p className="text-sm text-muted-foreground">
                {formatDate(post.created_at)}
              </p>
            </div>
            {isAuthor && (
              <Button variant="destructive" size="sm">
                Удалить
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          <p className="whitespace-pre-wrap mb-4">{post.content}</p>
          {post.tags && post.tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {post.tags.map((tag: any) => (
                <span key={tag.id} className="px-2 py-1 text-xs bg-secondary rounded-md">
                  #{tag.name}
                </span>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Комментарии ({comments.length})</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={handleSubmitComment} className="space-y-2">
            <Textarea
              placeholder="Написать комментарий..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              rows={3}
            />
            <Button type="submit" disabled={createCommentMutation.isPending}>
              Отправить
            </Button>
          </form>

          <div className="space-y-4 mt-6">
            {comments.map((comment: any) => (
              <div key={comment.id} className="border-l-2 pl-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium">{comment.author_username}</span>
                  <span className="text-sm text-muted-foreground">
                    {formatDate(comment.created_at)}
                  </span>
                </div>
                <p className="text-sm">{comment.content}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

