import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { communitiesApi } from '@/shared/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Button } from '@/shared/components/ui/button';

export const CommunitiesListPage = () => {
  const { data: communities, isLoading } = useQuery({
    queryKey: ['communities'],
    queryFn: () => communitiesApi.list(),
  });

  const communitiesArray = Array.isArray(communities) ? communities : (communities as any)?.results || [];

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Communities</h1>
        <p className="text-muted-foreground">Find interesting communities</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {communitiesArray.map((community: any) => (
          <Card key={community.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <CardTitle>{community.name}</CardTitle>
              <CardDescription>
                {community.visibility === 'public' && ' Публичное'}
                {community.visibility === 'private' && ' Приватное'}
                {community.visibility === 'secret' && 'Секретное'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                {community.description || 'Нет описания'}
              </p>
              <Button variant="outline" className="w-full" asChild>
                <Link to={`/communities/${community.id}`}>Подробнее</Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

