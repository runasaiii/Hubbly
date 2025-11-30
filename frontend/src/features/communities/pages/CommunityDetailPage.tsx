import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { communitiesApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { formatDate } from '@/shared/lib/utils';

export const CommunityDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: community, isLoading } = useQuery({
    queryKey: ['community', id],
    queryFn: () => communitiesApi.get(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  if (!community) {
    return <div className="text-center py-8">Сообщество не найдено</div>;
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <Button variant="ghost" onClick={() => navigate('/communities')}>
        ← Назад
      </Button>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{community.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="mb-4">{community.description || 'Нет описания'}</p>
          <div className="flex gap-4 text-sm text-muted-foreground">
            <span>Владелец: {community.owner_username}</span>
            <span>Создано: {formatDate(community.created_at)}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

