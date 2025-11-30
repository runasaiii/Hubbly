import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { communitiesApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Input } from '@/shared/components/ui/input';
import { Textarea } from '@/shared/components/ui/textarea';
import { Label } from '@/shared/components/ui/label';
import { ArrowLeft, X, Sparkles, Users, Globe, Lock, Eye, AlertCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

const communitySchema = z.object({
  name: z.string().min(1, 'Название обязательно').min(3, 'Минимум 3 символа').max(100, 'Максимум 100 символов'),
  description: z.string().max(500, 'Максимум 500 символов').optional(),
  visibility: z.enum(['public', 'private', 'secret']).default('public'),
});

type CommunityFormData = z.infer<typeof communitySchema>;

export const CreateCommunityPage = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [charCount, setCharCount] = useState(0);

  const { register, handleSubmit, formState: { errors }, watch, setValue } = useForm<CommunityFormData>({
    resolver: zodResolver(communitySchema),
    defaultValues: {
      name: '',
      description: '',
      visibility: 'public',
    },
  });

  const nameValue = watch('name', '');
  const descriptionValue = watch('description', '');
  const visibilityValue = watch('visibility', 'public');

  useEffect(() => {
    setCharCount(descriptionValue?.length || 0);
  }, [descriptionValue]);

  const createMutation = useMutation({
    mutationFn: communitiesApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['communities'] });
      navigate(`/communities/${data.id}`);
    },
  });

  const onSubmit = (data: CommunityFormData) => {
    createMutation.mutate(data);
  };

  const handleCancel = () => {
    if ((nameValue && nameValue.length > 0) || (descriptionValue && descriptionValue.length > 0)) {
      if (window.confirm('У вас есть несохраненные изменения. Вы уверены, что хотите уйти?')) {
        navigate('/communities');
      }
    } else {
      navigate('/communities');
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
        Назад к сообществам
      </Button>

      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-green-500 via-emerald-600 to-teal-600 p-8 text-white shadow-xl">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="h-5 w-5 animate-pulse" />
            <span className="text-sm font-medium opacity-90">Создание сообщества</span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">Создать сообщество</h1>
          <p className="text-white/80">
            Создайте новое сообщество и объедините людей вокруг общих интересов
          </p>
        </div>
      </div>

      {/* Form Card */}
      <Card className="border-none shadow-xl">
        <CardHeader className="border-b bg-gradient-to-r from-muted/30 to-transparent">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-green-500/10 flex items-center justify-center">
              <Users className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Новое сообщество</CardTitle>
              <CardDescription>Заполните информацию о сообществе</CardDescription>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Name Field */}
            <div className="space-y-3">
              <Label htmlFor="name" className="text-base font-semibold">
                Название сообщества *
              </Label>
              <Input
                id="name"
                {...register('name')}
                placeholder="Например: Программисты Python"
                maxLength={100}
                className={`focus:ring-2 transition-all ${
                  errors.name 
                    ? 'border-red-500 focus:ring-red-500/20' 
                    : 'focus:ring-green-500/20'
                }`}
              />
              {errors.name && (
                <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                  <AlertCircle className="h-4 w-4 text-red-600 flex-shrink-0" />
                  <p className="text-sm text-red-600">{errors.name.message}</p>
                </div>
              )}
              <p className="text-xs text-muted-foreground">
                Минимум 3 символа, максимум 100 символов
              </p>
            </div>

            {/* Description Field */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Label htmlFor="description" className="text-base font-semibold">
                  Описание (необязательно)
                </Label>
                <span className={`text-xs font-medium ${
                  charCount > 500 
                    ? 'text-red-500' 
                    : 'text-muted-foreground'
                }`}>
                  {charCount} / 500 символов
                </span>
              </div>
              <Textarea
                id="description"
                {...register('description')}
                onChange={(e) => setCharCount(e.target.value.length)}
                placeholder="Расскажите о вашем сообществе, его целях и интересах..."
                rows={6}
                maxLength={500}
                className={`resize-none focus:ring-2 transition-all ${
                  errors.description 
                    ? 'border-red-500 focus:ring-red-500/20' 
                    : 'focus:ring-green-500/20'
                }`}
              />
              {errors.description && (
                <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                  <AlertCircle className="h-4 w-4 text-red-600 flex-shrink-0" />
                  <p className="text-sm text-red-600">{errors.description.message}</p>
                </div>
              )}
            </div>

            {/* Visibility Field */}
            <div className="space-y-3">
              <Label className="text-base font-semibold">
                Видимость сообщества *
              </Label>
              <div className="grid gap-3 md:grid-cols-3">
                <button
                  type="button"
                  onClick={() => setValue('visibility', 'public')}
                  className={`p-4 rounded-lg border-2 transition-all text-left ${
                    visibilityValue === 'public'
                      ? 'border-green-500 bg-green-50'
                      : 'border-input hover:border-green-300'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Globe className={`h-5 w-5 ${visibilityValue === 'public' ? 'text-green-600' : 'text-muted-foreground'}`} />
                    <span className={`font-semibold ${visibilityValue === 'public' ? 'text-green-600' : ''}`}>
                      Публичное
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Видно всем, любой может вступить
                  </p>
                </button>

                <button
                  type="button"
                  onClick={() => setValue('visibility', 'private')}
                  className={`p-4 rounded-lg border-2 transition-all text-left ${
                    visibilityValue === 'private'
                      ? 'border-orange-500 bg-orange-50'
                      : 'border-input hover:border-orange-300'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Lock className={`h-5 w-5 ${visibilityValue === 'private' ? 'text-orange-600' : 'text-muted-foreground'}`} />
                    <span className={`font-semibold ${visibilityValue === 'private' ? 'text-orange-600' : ''}`}>
                      Приватное
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Видно всем, требуется одобрение для вступления
                  </p>
                </button>

                <button
                  type="button"
                  onClick={() => setValue('visibility', 'secret')}
                  className={`p-4 rounded-lg border-2 transition-all text-left ${
                    visibilityValue === 'secret'
                      ? 'border-red-500 bg-red-50'
                      : 'border-input hover:border-red-300'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Eye className={`h-5 w-5 ${visibilityValue === 'secret' ? 'text-red-600' : 'text-muted-foreground'}`} />
                    <span className={`font-semibold ${visibilityValue === 'secret' ? 'text-red-600' : ''}`}>
                      Секретное
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Скрыто от всех, только по приглашению
                  </p>
                </button>
              </div>
              <input type="hidden" {...register('visibility')} />
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t">
              <Button 
                type="submit" 
                disabled={createMutation.isPending || !nameValue || nameValue.length < 3}
                className="flex-1 gap-2 h-11 shadow-md"
                size="lg"
              >
                {createMutation.isPending ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Создание...
                  </>
                ) : (
                  <>
                    <Users className="h-4 w-4" />
                    Создать сообщество
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
                  <p className="text-sm font-medium text-red-800">Ошибка при создании сообщества</p>
                  <p className="text-xs text-red-600 mt-1">
                    Попробуйте еще раз или обратитесь в поддержку
                  </p>
                </div>
              </div>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

