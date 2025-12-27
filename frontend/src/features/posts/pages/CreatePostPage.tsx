import { useNavigate, useSearchParams } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { postsApi, communitiesApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Textarea } from '@/shared/components/ui/textarea';
import { Input } from '@/shared/components/ui/input';
import { Label } from '@/shared/components/ui/label';
import { useAuth } from '@/features/auth/context/AuthContext';
import { ArrowLeft, Send, X, Sparkles, FileText, AlertCircle, Users, Hash, Plus } from 'lucide-react';
import { useState, useEffect } from 'react';

const postSchema = z.object({
  content: z.string().min(1, 'Контент обязателен').min(10, 'Минимум 10 символов'),
  community: z.string().optional(),
  tags: z.array(z.string()).optional(),
});

type PostFormData = z.infer<typeof postSchema>;

export const CreatePostPage = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { user } = useAuth();
  const [searchParams] = useSearchParams();
  const communityFromUrl = searchParams.get('community');
  const [charCount, setCharCount] = useState(0);
  const [tagInput, setTagInput] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  
  const { register, handleSubmit, formState: { errors }, watch, control, setValue } = useForm<PostFormData>({
    resolver: zodResolver(postSchema),
    defaultValues: {
      content: '',
      community: communityFromUrl || '',
      tags: [],
    },
  });

  const contentValue = watch('content', '');
  const selectedCommunity = watch('community', '');
  
  const { data: communitiesData, isLoading: communitiesLoading } = useQuery({
    queryKey: ['communities'],
    queryFn: () => communitiesApi.list(),
  });

  useEffect(() => {
    if (communityFromUrl) {
      setValue('community', communityFromUrl);
    }
  }, [communityFromUrl, setValue]);

  const communitiesArray = Array.isArray(communitiesData) 
    ? communitiesData 
    : (communitiesData as any)?.results || [];


  const availableCommunities = communitiesArray.filter((c: any) => 
    c.is_owner === true
  );
  
  useEffect(() => {
    setCharCount(contentValue?.length || 0);
  }, [contentValue]);
  useEffect(() => {
    setValue('tags', tags);
  }, [tags, setValue]);

  const createMutation = useMutation({
    mutationFn: postsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      if (user?.id) {
        queryClient.invalidateQueries({ queryKey: ['user-posts', user.id] });
      }
      navigate('/posts');
    },
  });

  const handleAddTag = () => {
    const trimmedTag = tagInput.trim().toLowerCase();
    if (trimmedTag && !tags.includes(trimmedTag) && tags.length < 10) {
      setTags([...tags, trimmedTag]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleTagInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  const onSubmit = (data: PostFormData) => {
    const submitData: any = {
      content: data.content,
    };
    
    if (data.community && data.community.trim() !== '') {
      submitData.community = data.community;
    }
    
    if (tags.length > 0) {
      submitData.tags_list = tags;
    }
    
    createMutation.mutate(submitData);
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
            {/* Community Selection */}
            <div className="space-y-3">
              <Label htmlFor="community" className="text-base font-semibold flex items-center gap-2">
                <Users className="h-4 w-4" />
                Сообщество (необязательно)
              </Label>
              <Controller
                name="community"
                control={control}
                render={({ field }) => (
                  <select
                    {...field}
                    id="community"
                    disabled={communitiesLoading}
                    className="w-full px-4 py-2.5 rounded-lg border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <option value="">👤 От моего имени (личный пост)</option>
                    {communitiesLoading ? (
                      <option disabled>Загрузка сообществ...</option>
                    ) : availableCommunities.length === 0 ? (
                      <option disabled>У вас нет сообществ для публикации</option>
                    ) : (
                      availableCommunities.map((community: any) => (
                        <option key={community.id} value={community.id}>
                          🏘️ {community.name} {community.visibility === 'public' ? '(Публичное)' : community.visibility === 'private' ? '(Приватное)' : '(Секретное)'}
                        </option>
                      ))
                    )}
                  </select>
                )}
              />
              <div className="space-y-2">
                {selectedCommunity ? (
                  <div className="p-3 rounded-lg bg-blue-50 border border-blue-200">
                    <p className="text-sm text-blue-800">
                      📌 Пост будет опубликован от имени выбранного сообщества. Только владелец может создавать посты от имени сообщества.
                    </p>
                  </div>
                ) : (
                  <div className="p-3 rounded-lg bg-green-50 border border-green-200">
                    <p className="text-sm text-green-800">
                      ✅ Пост будет опубликован от вашего имени как личный пост.
                    </p>
                  </div>
                )}
                <p className="text-xs text-muted-foreground">
                  Выберите сообщество, чтобы опубликовать пост от его имени (только ваши сообщества, где вы владелец). 
                  Оставьте пустым для личного поста от вашего имени.
                </p>
              </div>
            </div>

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
                    <li>Добавьте теги для лучшей видимости вашего поста</li>
                    <li>Выберите сообщество, чтобы опубликовать от его имени</li>
                  </ul>
                </div>
              )}
            </div>

            {/* Tags Field */}
            <div className="space-y-3">
              <Label htmlFor="tags" className="text-base font-semibold flex items-center gap-2">
                <Hash className="h-4 w-4" />
                Теги (необязательно)
              </Label>
              <div className="space-y-2">
                <div className="flex gap-2">
                  <Input
                    id="tags"
                    type="text"
                    value={tagInput}
                    onChange={(e) => setTagInput(e.target.value)}
                    onKeyDown={handleTagInputKeyDown}
                    placeholder="Введите тег и нажмите Enter или кнопку Добавить"
                    className="flex-1"
                  />
                  <Button
                    type="button"
                    onClick={handleAddTag}
                    disabled={!tagInput.trim() || tags.length >= 10}
                    variant="outline"
                    className="gap-2"
                  >
                    <Plus className="h-4 w-4" />
                    Добавить
                  </Button>
                </div>
                
                {tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 p-3 rounded-lg bg-muted/30 border">
                    {tags.map((tag) => (
                      <span
                        key={tag}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm bg-primary/10 text-primary rounded-full font-medium"
                      >
                        #{tag}
                        <button
                          type="button"
                          onClick={() => handleRemoveTag(tag)}
                          className="hover:bg-primary/20 rounded-full p-0.5 transition-colors"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </span>
                    ))}
                  </div>
                )}
                
                <p className="text-xs text-muted-foreground">
                  Добавьте до 10 тегов для лучшей видимости вашего поста. Теги помогают другим пользователям найти ваш контент.
                </p>
              </div>
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
          <CardContent className="space-y-4">
            {/* Community Preview */}
            {selectedCommunity && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Users className="h-4 w-4" />
                <span>
                  От имени: <span className="font-medium text-foreground">
                    {availableCommunities.find((c: any) => c.id === selectedCommunity)?.name || 'Сообщество'}
                  </span>
                </span>
              </div>
            )}
            
            {/* Content Preview */}
            <div className="p-4 rounded-lg bg-background border">
              <p className="text-sm leading-relaxed whitespace-pre-wrap">
                {contentValue || 'Ваш текст появится здесь...'}
              </p>
            </div>

            {/* Tags Preview */}
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-3 py-1.5 text-xs bg-primary/10 text-primary rounded-full font-medium"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};