import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { eventsApi, communitiesApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Input } from '@/shared/components/ui/input';
import { Textarea } from '@/shared/components/ui/textarea';
import { Label } from '@/shared/components/ui/label';
import { ArrowLeft, Sparkles, Calendar, Clock, Users, AlertCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

const eventSchema = z.object({
  title: z.string().min(1, 'Название обязательно').min(3, 'Минимум 3 символа').max(200, 'Максимум 200 символов'),
  description: z.string().min(1, 'Описание обязательно').max(2000, 'Максимум 2000 символов'),
  start_at: z.string().min(1, 'Дата начала обязательна'),
  end_at: z.string().min(1, 'Дата окончания обязательна'),
  community: z.string().min(1, 'Сообщество обязательно'),
  capacity: z.string().optional(),
  requires_approval: z.boolean().default(false),
  status: z.enum(['draft', 'published']).default('draft'),
}).refine((data) => {
  if (data.start_at && data.end_at) {
    return new Date(data.end_at) > new Date(data.start_at);
  }
  return true;
}, {
  message: 'Дата окончания должна быть позже даты начала',
  path: ['end_at'],
});

type EventFormData = z.infer<typeof eventSchema>;

export const CreateEventPage = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [charCount, setCharCount] = useState(0);

  const { register, handleSubmit, formState: { errors }, watch, setValue } = useForm<EventFormData>({
    resolver: zodResolver(eventSchema),
    defaultValues: {
      title: '',
      description: '',
      start_at: '',
      end_at: '',
      community: '',
      capacity: '',
      requires_approval: false,
      status: 'draft',
    },
  });

  const descriptionValue = watch('description', '');
  const startAtValue = watch('start_at', '');
  const endAtValue = watch('end_at', '');

  // Загрузка сообществ
  const { data: communitiesData, isLoading: communitiesLoading } = useQuery({
    queryKey: ['communities'],
    queryFn: () => communitiesApi.list(),
  });

  const communitiesArray = Array.isArray(communitiesData) 
    ? communitiesData 
    : (communitiesData as any)?.results || [];

  useEffect(() => {
    setCharCount(descriptionValue?.length || 0);
  }, [descriptionValue]);

  // Устанавливаем минимальную дату для end_at
  useEffect(() => {
    if (startAtValue) {
      const startDate = new Date(startAtValue);
      const minEndDate = new Date(startDate.getTime() + 60 * 60 * 1000); // +1 час
      const minEndDateString = minEndDate.toISOString().slice(0, 16);
      const endDateInput = document.getElementById('end_at') as HTMLInputElement;
      if (endDateInput && (!endAtValue || new Date(endAtValue) < minEndDate)) {
        endDateInput.min = minEndDateString;
      }
    }
  }, [startAtValue, endAtValue]);

  const createMutation = useMutation({
    mutationFn: eventsApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['events'] });
      navigate(`/events/${data.id}`);
    },
  });

  const onSubmit = (data: EventFormData) => {
    const submitData: any = {
      title: data.title,
      description: data.description,
      start_at: new Date(data.start_at).toISOString(),
      end_at: new Date(data.end_at).toISOString(),
      community: data.community,
      requires_approval: data.requires_approval,
      status: data.status,
    };
    
    if (data.capacity && data.capacity.trim() !== '') {
      submitData.capacity = parseInt(data.capacity, 10);
    }
    
    createMutation.mutate(submitData);
  };

  const handleCancel = () => {
    const hasChanges = watch('title') || watch('description') || watch('start_at');
    if (hasChanges) {
      if (window.confirm('У вас есть несохраненные изменения. Вы уверены, что хотите уйти?')) {
        navigate('/events');
      }
    } else {
      navigate('/events');
    }
  };

  // Получаем текущую дату и время для минимального значения
  const now = new Date();
  const minDateTime = now.toISOString().slice(0, 16);

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-8">
      {/* Back Button */}
      <Button 
        variant="ghost" 
        onClick={handleCancel}
        className="gap-2 hover:gap-3 transition-all"
      >
        <ArrowLeft className="h-4 w-4" />
        Назад к событиям
      </Button>

      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-orange-500 via-purple-600 to-pink-600 p-8 text-white shadow-xl">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="h-5 w-5 animate-pulse" />
            <span className="text-sm font-medium opacity-90">Создание события</span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">Создать событие</h1>
          <p className="text-white/80">
            Организуйте мероприятие и пригласите участников
          </p>
        </div>
      </div>

      {/* Form Card */}
      <Card className="border-none shadow-xl">
        <CardHeader className="border-b bg-gradient-to-r from-muted/30 to-transparent">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-orange-500/10 flex items-center justify-center">
              <Calendar className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Информация о событии</CardTitle>
              <CardDescription>
                Заполните все необходимые поля для создания события
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Title */}
            <div className="space-y-2">
              <Label htmlFor="title">
                Название события <span className="text-red-500">*</span>
              </Label>
              <Input
                id="title"
                {...register('title')}
                placeholder="Введите название события"
                className={errors.title ? 'border-red-500' : ''}
              />
              {errors.title && (
                <div className="flex items-center gap-1 text-sm text-red-500">
                  <AlertCircle className="h-4 w-4" />
                  {errors.title.message}
                </div>
              )}
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label htmlFor="description">
                Описание <span className="text-red-500">*</span>
              </Label>
              <Textarea
                id="description"
                {...register('description')}
                placeholder="Опишите ваше событие..."
                rows={6}
                className={`resize-none ${errors.description ? 'border-red-500' : ''}`}
              />
              <div className="flex items-center justify-between">
                {errors.description && (
                  <div className="flex items-center gap-1 text-sm text-red-500">
                    <AlertCircle className="h-4 w-4" />
                    {errors.description.message}
                  </div>
                )}
                <span className={`text-xs ml-auto ${charCount > 2000 ? 'text-red-500' : 'text-muted-foreground'}`}>
                  {charCount} / 2000
                </span>
              </div>
            </div>

            {/* Community */}
            <div className="space-y-2">
              <Label htmlFor="community">
                Сообщество <span className="text-red-500">*</span>
              </Label>
              {communitiesLoading ? (
                <div className="text-sm text-muted-foreground">Загрузка сообществ...</div>
              ) : (
                <select
                  id="community"
                  {...register('community')}
                  className={`w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${
                    errors.community ? 'border-red-500' : ''
                  }`}
                >
                  <option value="">Выберите сообщество</option>
                  {communitiesArray.map((community: any) => (
                    <option key={community.id} value={community.id}>
                      {community.name}
                    </option>
                  ))}
                </select>
              )}
              {errors.community && (
                <div className="flex items-center gap-1 text-sm text-red-500">
                  <AlertCircle className="h-4 w-4" />
                  {errors.community.message}
                </div>
              )}
            </div>

            {/* Date and Time */}
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="start_at">
                  Дата и время начала <span className="text-red-500">*</span>
                </Label>
                <div className="relative">
                  <Input
                    id="start_at"
                    type="datetime-local"
                    {...register('start_at')}
                    min={minDateTime}
                    className={errors.start_at ? 'border-red-500' : ''}
                  />
                  <Clock className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
                </div>
                {errors.start_at && (
                  <div className="flex items-center gap-1 text-sm text-red-500">
                    <AlertCircle className="h-4 w-4" />
                    {errors.start_at.message}
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="end_at">
                  Дата и время окончания <span className="text-red-500">*</span>
                </Label>
                <div className="relative">
                  <Input
                    id="end_at"
                    type="datetime-local"
                    {...register('end_at')}
                    min={startAtValue || minDateTime}
                    className={errors.end_at ? 'border-red-500' : ''}
                  />
                  <Clock className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
                </div>
                {errors.end_at && (
                  <div className="flex items-center gap-1 text-sm text-red-500">
                    <AlertCircle className="h-4 w-4" />
                    {errors.end_at.message}
                  </div>
                )}
              </div>
            </div>

            {/* Capacity */}
            <div className="space-y-2">
              <Label htmlFor="capacity">
                Вместимость (необязательно)
              </Label>
              <div className="relative">
                <Input
                  id="capacity"
                  type="number"
                  min="1"
                  {...register('capacity')}
                  placeholder="Максимальное количество участников"
                />
                <Users className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
              </div>
            </div>

            {/* Status */}
            <div className="space-y-2">
              <Label htmlFor="status">Статус</Label>
              <select
                id="status"
                {...register('status')}
                className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              >
                <option value="draft">Черновик</option>
                <option value="published">Опубликовано</option>
              </select>
            </div>

            {/* Requires Approval */}
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="requires_approval"
                {...register('requires_approval')}
                className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
              />
              <Label htmlFor="requires_approval" className="text-sm font-normal cursor-pointer">
                Требуется одобрение организатора для участия
              </Label>
            </div>

            {/* Submit Buttons */}
            <div className="flex items-center justify-end gap-3 pt-4 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={handleCancel}
                disabled={createMutation.isPending}
              >
                Отмена
              </Button>
              <Button
                type="submit"
                disabled={createMutation.isPending}
                className="gap-2"
              >
                {createMutation.isPending ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Создание...
                  </>
                ) : (
                  <>
                    <Calendar className="h-4 w-4" />
                    Создать событие
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

