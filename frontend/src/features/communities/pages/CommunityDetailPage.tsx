import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { communitiesApi } from '@/shared/api';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { formatDate } from '@/shared/lib/utils';
import { useAuth } from '@/features/auth/context/AuthContext';
import { 
  ArrowLeft, 
  Users, 
  Crown,
  Calendar,
  Lock,
  Globe,
  Eye,
  UserPlus,
  Share2,
  Settings,
  MessageSquare,
  FileText,
  TrendingUp,
  Check,
  Clock
} from 'lucide-react';

export const CommunityDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const queryClient = useQueryClient();

  const { data: community, isLoading } = useQuery({
    queryKey: ['community', id],
    queryFn: () => communitiesApi.get(id!),
    enabled: !!id,
  });

  const joinMutation = useMutation({
    mutationFn: () => communitiesApi.join(id!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['community', id] });
    },
  });

  // Функция для определения иконки и цвета видимости
  const getVisibilityInfo = (visibility: string) => {
    switch (visibility?.toLowerCase()) {
      case 'public':
        return {
          icon: <Globe className="h-4 w-4" />,
          color: 'bg-green-100 text-green-700 border-green-200',
          text: 'Публичное'
        };
      case 'private':
        return {
          icon: <Lock className="h-4 w-4" />,
          color: 'bg-orange-100 text-orange-700 border-orange-200',
          text: 'Приватное'
        };
      case 'secret':
        return {
          icon: <Eye className="h-4 w-4" />,
          color: 'bg-red-100 text-red-700 border-red-200',
          text: 'Секретное'
        };
      default:
        return {
          icon: <Users className="h-4 w-4" />,
          color: 'bg-blue-100 text-blue-700 border-blue-200',
          text: visibility
        };
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="space-y-4 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Загрузка сообщества...</p>
        </div>
      </div>
    );
  }

  if (!community) {
    return (
      <div className="flex items-center justify-center py-16 max-w-2xl mx-auto">
        <Card className="border-none shadow-lg">
          <CardContent className="py-12 text-center">
            <div className="mx-auto w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
              <Users className="h-8 w-8 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Сообщество не найдено</h3>
            <p className="text-muted-foreground mb-6">
              Возможно, оно было удалено или не существует
            </p>
            <Button onClick={() => navigate('/communities')} className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Вернуться к сообществам
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const visibilityInfo = getVisibilityInfo(community.visibility);
  const memberCount = community.members_count || 0;
  const postCount = community.posts_count || 0;
  
  // Определяем роль пользователя
  const isOwner = community.is_owner || false;
  const isMember = community.is_member || false;
  const membershipStatus = community.membership_status;
  const membershipRole = community.membership_role;

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-8">
      {/* Back Button */}
      <Button 
        variant="ghost" 
        onClick={() => navigate('/communities')}
        className="gap-2 hover:gap-3 transition-all"
      >
        <ArrowLeft className="h-4 w-4" />
        Назад к сообществам
      </Button>

      {/* Hero Card */}
      <Card className="border-none shadow-xl overflow-hidden">
        <div className="h-3 bg-gradient-to-r from-green-500 via-emerald-600 to-teal-600"></div>
        
        {/* Cover Image Placeholder */}
        <div className="h-48 bg-gradient-to-br from-green-500/20 via-emerald-500/20 to-teal-500/20 relative">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-24 w-24 rounded-full bg-gradient-to-br from-green-500 to-teal-500 flex items-center justify-center text-white shadow-2xl">
              <Users className="h-12 w-12" />
            </div>
          </div>
        </div>

        <CardHeader className="pt-16 bg-gradient-to-r from-muted/30 to-transparent">
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-3 flex-wrap">
                <span className={`px-3 py-1.5 text-sm rounded-full border font-medium flex items-center gap-1.5 ${visibilityInfo.color}`}>
                  {visibilityInfo.icon}
                  {visibilityInfo.text}
                </span>
                {memberCount > 0 && (
                  <span className="px-3 py-1.5 text-sm rounded-full bg-primary/10 text-primary border border-primary/20 font-medium flex items-center gap-1.5">
                    <Users className="h-4 w-4" />
                    {memberCount} {memberCount === 1 ? 'участник' : 'участников'}
                  </span>
                )}
              </div>
              <CardTitle className="text-3xl md:text-4xl mb-3">
                {community.name}
              </CardTitle>
              <p className="text-muted-foreground leading-relaxed">
                {community.description || 'Описание сообщества отсутствует'}
              </p>
            </div>
            
            <div className="flex gap-2">
              {isOwner ? (
                <>
                  <Button size="lg" variant="outline" className="gap-2 shadow-md" asChild>
                    <Link to={`/posts/create?community=${id}`}>
                      <FileText className="h-5 w-5" />
                      Создать пост
                    </Link>
                  </Button>
                </>
              ) : isMember ? (
                <>
                  {membershipStatus === 'pending' ? (
                    <Button size="lg" variant="outline" className="gap-2 shadow-md" disabled>
                      <Clock className="h-5 w-5" />
                      Заявка на рассмотрении
                    </Button>
                  ) : (
                    <Button size="lg" variant="default" className="gap-2 shadow-md" asChild>
                      <Link to={`/posts/create?community=${id}`}>
                        <FileText className="h-5 w-5" />
                        Создать пост
                      </Link>
                    </Button>
                  )}
                  <div className="px-3 py-2 rounded-lg bg-primary/10 text-primary border border-primary/20 flex items-center gap-2">
                    <Check className="h-4 w-4" />
                    <span className="text-sm font-medium">
                      {membershipRole === 'organizer' ? 'Организатор' : 
                       membershipRole === 'moderator' ? 'Модератор' : 
                       'Участник'}
                    </span>
                  </div>
                </>
              ) : (
                <>
                  <Button 
                    size="lg" 
                    className="gap-2 shadow-md"
                    onClick={() => joinMutation.mutate()}
                    disabled={joinMutation.isPending || !user}
                  >
                    {joinMutation.isPending ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        Вступление...
                      </>
                    ) : (
                      <>
                        <UserPlus className="h-5 w-5" />
                        Вступить
                      </>
                    )}
                  </Button>
                </>
              )}
              <Button variant="outline" size="lg" className="gap-2">
                <Share2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-6">
          {/* Stats */}
          <div className="grid gap-4 md:grid-cols-3 mb-6">
            <Card className="border-none shadow-sm bg-gradient-to-br from-blue-50 to-blue-100/50">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white">
                    <Users className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">{memberCount}</p>
                    <p className="text-xs text-muted-foreground">Участников</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-none shadow-sm bg-gradient-to-br from-purple-50 to-purple-100/50">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-purple-500 flex items-center justify-center text-white">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">{postCount}</p>
                    <p className="text-xs text-muted-foreground">Постов</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-none shadow-sm bg-gradient-to-br from-green-50 to-green-100/50">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center text-white">
                    <TrendingUp className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">+{Math.floor(memberCount * 0.15)}</p>
                    <p className="text-xs text-muted-foreground">За месяц</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      {/* Owner Card */}
      <Card className="border-none shadow-lg">
        <CardHeader className="bg-gradient-to-r from-muted/30 to-transparent border-b">
          <CardTitle className="flex items-center gap-2">
            <Crown className="h-5 w-5 text-yellow-600" />
            Владелец сообщества
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <Link 
            to={`/profile/${community.owner}`}
            className="flex items-center gap-4 p-4 rounded-lg hover:bg-muted/50 transition-colors group"
          >
            <div className="relative">
              <div className="h-14 w-14 rounded-full bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center text-xl font-bold text-white shadow-md">
                {community.owner_username?.[0]?.toUpperCase() || 'O'}
              </div>
              <div className="absolute -bottom-1 -right-1 h-6 w-6 bg-yellow-500 rounded-full flex items-center justify-center border-2 border-white">
                <Crown className="h-3 w-3 text-white" />
              </div>
            </div>
            <div className="flex-1">
              <p className="font-semibold text-lg group-hover:text-primary transition-colors">
                {community.owner_username}
              </p>
              <p className="text-sm text-muted-foreground">Основатель и администратор</p>
            </div>
            <ArrowLeft className="h-5 w-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all rotate-180" />
          </Link>
        </CardContent>
      </Card>

      {/* Additional Info */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Community Info */}
        <Card className="border-none shadow-lg">
          <CardHeader className="bg-gradient-to-r from-muted/30 to-transparent border-b">
            <CardTitle className="flex items-center gap-2 text-lg">
              <MessageSquare className="h-5 w-5 text-primary" />
              Информация
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4 text-sm">
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span>Создано</span>
                </div>
                <span className="font-medium">{formatDate(community.created_at)}</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
                <div className="flex items-center gap-2 text-muted-foreground">
                  {visibilityInfo.icon}
                  <span>Видимость</span>
                </div>
                <span className="font-medium">{visibilityInfo.text}</span>
              </div>
              {community.category && (
                <div className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <FileText className="h-4 w-4" />
                    <span>Категория</span>
                  </div>
                  <span className="font-medium">{community.category}</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="border-none shadow-lg">
          <CardHeader className="bg-gradient-to-r from-muted/30 to-transparent border-b">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Settings className="h-5 w-5 text-primary" />
              Действия
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <Button variant="outline" className="w-full justify-start gap-2" asChild>
                <Link to={`/posts?community=${id}`}>
                  <MessageSquare className="h-4 w-4" />
                  Посмотреть посты ({postCount})
                </Link>
              </Button>
              <Button 
                variant="outline" 
                className="w-full justify-start gap-2"
                onClick={async () => {
                  try {
                    const members = await communitiesApi.getMembers(id!);
                    alert(`Участников: ${members.length}\n\n${members.map((m: any) => `${m.user_username} (${m.role})`).join('\n')}`);
                  } catch (error) {
                    alert('Не удалось загрузить список участников');
                  }
                }}
              >
                <Users className="h-4 w-4" />
                Участники ({memberCount})
              </Button>
              <Button variant="outline" className="w-full justify-start gap-2" disabled>
                <Share2 className="h-4 w-4" />
                Пригласить друзей (скоро)
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};