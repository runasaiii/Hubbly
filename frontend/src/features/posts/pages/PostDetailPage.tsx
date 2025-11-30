import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { postsApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Textarea } from '@/shared/components/ui/textarea';
import { formatDate } from '@/shared/lib/utils';
import { useAuth } from '@/features/auth/context/AuthContext';
import { useState } from 'react';
import { ArrowLeft, Trash2, Clock, MessageSquare, Heart, Send, User } from 'lucide-react';

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
    return (
      <div className="flex items-center justify-center py-16">
        <div className="space-y-4 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Загрузка поста...</p>
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="flex items-center justify-center py-16 max-w-2xl mx-auto">
        <Card className="border-none shadow-lg">
          <CardContent className="py-12 text-center">
            <div className="mx-auto w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
              <MessageSquare className="h-8 w-8 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Пост не найден</h3>
            <p className="text-muted-foreground mb-6">
              Возможно, он был удален или не существует
            </p>
            <Button onClick={() => navigate('/posts')} className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Вернуться к постам
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const isAuthor = user?.id === post.author;

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-8">
      {/* Back Button */}
      <Button 
        variant="ghost" 
        onClick={() => navigate('/posts')}
        className="gap-2 hover:gap-3 transition-all"
      >
        <ArrowLeft className="h-4 w-4" />
        Назад к постам
      </Button>

      {/* Main Post Card */}
      <Card className="border-none shadow-xl overflow-hidden">
        <CardHeader className="border-b bg-gradient-to-r from-muted/30 to-transparent pb-6">
          <div className="flex items-start justify-between gap-4">
            <Link 
              to={`/profile/${post.author}`}
              className="flex items-center gap-4 hover:opacity-80 transition-opacity group"
            >
              <div className="relative">
                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-xl font-bold text-white shadow-lg">
                  {post.author_username?.[0]?.toUpperCase() || 'U'}
                </div>
                <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <CardTitle className="text-xl group-hover:text-primary transition-colors">
                  {post.author_username}
                </CardTitle>
                <div className="flex items-center gap-2 text-sm text-muted-foreground mt-1">
                  <Clock className="h-3 w-3" />
                  <span>{formatDate(post.created_at)}</span>
                </div>
              </div>
            </Link>
            
            {isAuthor && (
              <Button variant="destructive" size="sm" className="gap-2">
                <Trash2 className="h-4 w-4" />
                Удалить
              </Button>
            )}
          </div>
        </CardHeader>
        
        <CardContent className="pt-6">
          {/* Content */}
          <div className="prose prose-slate max-w-none mb-6">
            <p className="text-base leading-relaxed whitespace-pre-wrap">
              {post.content}
            </p>
          </div>

          {/* Tags */}
          {post.tags && post.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-6 pb-6 border-b">
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

          {/* Actions Bar */}
          <div className="flex items-center gap-6">
            <button className="flex items-center gap-2 text-sm text-muted-foreground hover:text-red-500 transition-colors group">
              <div className="p-2 rounded-full group-hover:bg-red-50 transition-colors">
                <Heart className="h-5 w-5" />
              </div>
              <span className="font-medium">Нравится</span>
            </button>
            <button className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors group">
              <div className="p-2 rounded-full group-hover:bg-primary/10 transition-colors">
                <MessageSquare className="h-5 w-5" />
              </div>
              <span className="font-medium">{comments.length} комментариев</span>
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Comments Section */}
      <Card className="border-none shadow-xl">
        <CardHeader className="bg-gradient-to-r from-muted/30 to-transparent border-b">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                <MessageSquare className="h-5 w-5 text-primary" />
              </div>
              <div>
                <CardTitle className="text-xl">Комментарии</CardTitle>
                <p className="text-sm text-muted-foreground">
                  {comments.length} {comments.length === 1 ? 'комментарий' : 'комментариев'}
                </p>
              </div>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="pt-6">
          {/* Comment Form */}
          <form onSubmit={handleSubmitComment} className="mb-8">
            <div className="flex gap-3">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-sm font-bold text-white">
                  {user?.username?.[0]?.toUpperCase() || 'U'}
                </div>
              </div>
              <div className="flex-1 space-y-3">
                <Textarea
                  placeholder="Напишите комментарий..."
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  rows={3}
                  className="resize-none focus:ring-2 focus:ring-primary/20"
                />
                <div className="flex justify-end">
                  <Button 
                    type="submit" 
                    disabled={createCommentMutation.isPending || !comment.trim()}
                    className="gap-2"
                  >
                    {createCommentMutation.isPending ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        Отправка...
                      </>
                    ) : (
                      <>
                        <Send className="h-4 w-4" />
                        Отправить
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </div>
          </form>

          {/* Comments List */}
          <div className="space-y-6">
            {comments.length === 0 ? (
              <div className="text-center py-12">
                <div className="mx-auto w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
                  <MessageSquare className="h-8 w-8 text-muted-foreground" />
                </div>
                <p className="text-muted-foreground">
                  Пока нет комментариев. Будьте первым!
                </p>
              </div>
            ) : (
              comments.map((comment: any, index: number) => (
                <div 
                  key={comment.id} 
                  className="flex gap-3 p-4 rounded-lg hover:bg-muted/30 transition-colors border-l-2 border-primary/20"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <Link to={`/profile/${comment.author}`} className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-teal-500 flex items-center justify-center text-sm font-bold text-white hover:shadow-md transition-shadow">
                      {comment.author_username?.[0]?.toUpperCase() || 'U'}
                    </div>
                  </Link>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-2">
                      <Link 
                        to={`/profile/${comment.author}`}
                        className="font-semibold hover:text-primary transition-colors"
                      >
                        {comment.author_username}
                      </Link>
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Clock className="h-3 w-3" />
                        {formatDate(comment.created_at)}
                      </div>
                    </div>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">
                      {comment.content}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};