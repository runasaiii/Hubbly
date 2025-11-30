import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { postsApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Textarea } from '@/shared/components/ui/textarea';
import { Label } from '@/shared/components/ui/label';
import { ArrowLeft, Send, X, Sparkles, FileText, AlertCircle } from 'lucide-react';
import { useState } from 'react';

const postSchema = z.object({
  content: z.string().min(1, 'Контент обязателен').min(10, 'Минимум 10 символов'),
  community: z.string().optional(),
});

type PostFormData = z.infer<typeof postSchema>;

export const CreatePostPage = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [charCount, setCharCount] = useState(0);
  
  const { register, handleSubmit, formState: { errors }, watch } = useForm<PostFormData>({
    resolver: zodResolver(postSchema),
  });

  const contentValue = watch('content', '');
  
  // Update character count
  useState(() => {
    setCharCount(contentValue?.length || 0);
  });

  const createMutation = useMutation({
    mutationFn: postsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      navigate('/posts');
    },
  });

  const onSubmit = (data: PostFormData) => {
    createMutation.mutate(data);
  };

  const handleCancel = () => {
    if (contentValue && contentValue.length > 0) {
      if (window.confirm('У вас есть несохраненные изменения. Вы уверены, что хотите уйти?')) {
        navigate('/posts');
      }
    } else {
      navigate('/posts');
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-8">
      {/* Back Button */}
      <Button 
        variant="ghost" 
        onClick={handleCancel}
        className="gap-2 hover:gap-3 transition-all"
      >
        <ArrowLeft className="h-4 w-4" />
        Назад к постам
      </Button>

      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-500 via-purple-600 to-blue-600 p-8 text-white shadow-xl">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="h-5 w-5 animate-pulse" />
            <span className="text-sm font-medium opacity-90">Создание публикации</span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">Создать пост</h1>
          <p className="text-white/80">
            Поделитесь своими мыслями и идеями с сообществом
          </p>
        </div>
      </div>

      {/* Form Card */}
      <Card className="border-none shadow-xl">
        <CardHeader className="border-b bg-gradient-to-r from-muted/30 to-transparent">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-purple-500/10 flex items-center justify-center">
              <FileText className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Новый пост</CardTitle>
              <CardDescription>Напишите что-нибудь интересное</CardDescription>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Content Field */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Label htmlFor="content" className="text-base font-semibold">
                  Содержание
                </Label>
                <span className={`text-xs font-medium ${
                  charCount < 10 
                    ? 'text-red-500' 
                    : charCount > 500 
                    ? 'text-orange-500' 
                    : 'text-muted-foreground'
                }`}>
                  {charCount} / 1000 символов
                </span>
              </div>
              
              <Textarea
                id="content"
                {...register('content')}
                onChange={(e) => setCharCount(e.target.value.length)}
                placeholder="Что у вас на уме? Поделитесь своими мыслями, идеями или новостями..."
                rows={12}
                maxLength={1000}
                className={`resize-none focus:ring-2 transition-all ${
                  errors.content 
                    ? 'border-red-500 focus:ring-red-500/20' 
                    : 'focus:ring-purple-500/20'
                }`}
              />
              
              {errors.content && (
                <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                  <AlertCircle className="h-4 w-4 text-red-600 flex-shrink-0" />
                  <p className="text-sm text-red-600">{errors.content.message}</p>
                </div>
              )}

              {/* Tips */}
              {!errors.content && charCount === 0 && (
                <div className="p-4 rounded-lg bg-blue-50 border border-blue-200">
                  <p className="text-sm text-blue-800 font-medium mb-2">💡 Советы:</p>
                  <ul className="text-xs text-blue-700 space-y-1 list-disc list-inside">
                    <li>Минимум 10 символов для публикации</li>
                    <li>Будьте вежливы и уважительны к другим</li>
                    <li>Добавьте теги для лучшей видимости (скоро)</li>
                  </ul>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t">
              <Button 
                type="submit" 
                disabled={createMutation.isPending || charCount < 10}
                className="flex-1 gap-2 h-11 shadow-md"
                size="lg"
              >
                {createMutation.isPending ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Публикация...
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    Опубликовать
                  </>
                )}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={handleCancel}
                disabled={createMutation.isPending}
                className="flex-1 gap-2 h-11"
                size="lg"
              >
                <X className="h-4 w-4" />
                Отмена
              </Button>
            </div>

            {/* Error Message */}
            {createMutation.isError && (
              <div className="flex items-center gap-2 p-4 rounded-lg bg-red-50 border border-red-200">
                <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium text-red-800">Ошибка при создании поста</p>
                  <p className="text-xs text-red-600 mt-1">
                    Попробуйте еще раз или обратитесь в поддержку
                  </p>
                </div>
              </div>
            )}
          </form>
        </CardContent>
      </Card>

      {/* Preview Card */}
      {charCount > 0 && (
        <Card className="border-none shadow-lg bg-gradient-to-br from-muted/30 to-muted/10">
          <CardHeader>
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                👁️
              </div>
              <CardTitle className="text-lg">Предварительный просмотр</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="p-4 rounded-lg bg-background border">
              <p className="text-sm leading-relaxed whitespace-pre-wrap">
                {contentValue || 'Ваш текст появится здесь...'}
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};