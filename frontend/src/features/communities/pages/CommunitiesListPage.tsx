import { useState, useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { communitiesApi } from '@/shared/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Button } from '@/shared/components/ui/button';
import { Input } from '@/shared/components/ui/input';
import { 
  Users, 
  Sparkles, 
  Plus, 
  Globe, 
  Lock, 
  Eye, 
  ArrowRight,
  Search,
  TrendingUp,
  Crown,
  Filter,
  X
} from 'lucide-react';

export const CommunitiesListPage = () => {
  const [searchInput, setSearchInput] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [visibilityFilter, setVisibilityFilter] = useState<string>('');
  const [showSearch, setShowSearch] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setSearchQuery(searchInput.trim());
    }, 500); // 500ms delay

    return () => clearTimeout(timer);
  }, [searchInput]);

  const { data: communities, isLoading } = useQuery({
    queryKey: ['communities', searchQuery, visibilityFilter],
    queryFn: () => communitiesApi.list({
      ...(searchQuery && { search: searchQuery }),
      ...(visibilityFilter && { visibility: visibilityFilter }),
    }),
    enabled: true, // Always enabled, but queryKey changes trigger refetch
  });

  const communitiesArray = Array.isArray(communities) ? communities : (communities as any)?.results || [];

  // Группируем сообщества по видимости
  const publicCommunities = communitiesArray.filter((c: any) => c.visibility === 'public');
  const privateCommunities = communitiesArray.filter((c: any) => c.visibility === 'private');

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
          <p className="text-muted-foreground">Загрузка сообществ...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary via-primary/90 to-primary/80 p-8 text-primary-foreground shadow-lg">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative flex items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="h-5 w-5 animate-pulse" />
              <span className="text-sm font-medium opacity-90">Найди своё сообщество</span>
            </div>
            <h1 className="text-4xl font-bold tracking-tight">Сообщества</h1>
            <p className="text-white/80">
              {communitiesArray.length > 0 
                ? `${communitiesArray.length} ${communitiesArray.length === 1 ? 'сообщество' : 'сообществ'} для вас`
                : 'Создайте первое сообщество'
              }
            </p>
          </div>
          <div className="flex gap-2">
            <Button 
              variant="secondary" 
              size="sm" 
              className="gap-2"
              onClick={() => {
                setShowSearch(!showSearch);
                setShowFilters(false);
              }}
            >
              <Search className="h-4 w-4" />
              Поиск
            </Button>
            <Button 
              variant="secondary" 
              size="sm" 
              className="gap-2"
              onClick={() => {
                setShowFilters(!showFilters);
                setShowSearch(false);
              }}
            >
              <Filter className="h-4 w-4" />
              Фильтры
            </Button>
            <Button size="sm" variant="secondary" className="gap-2 shadow-lg" asChild>
              <Link to="/communities/create">
                <Plus className="h-5 w-5" />
                Создать
              </Link>
            </Button>
          </div>
        </div>
      </div>

      {/* Search Bar */}
      {showSearch && (
        <Card className="border-none shadow-md">
          <CardContent className="pt-6">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Поиск по названию или описанию..."
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  className="pl-10 pr-10"
                />
                {searchInput && (
                  <button
                    onClick={() => {
                      setSearchInput('');
                      setSearchQuery('');
                    }}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    <X className="h-4 w-4" />
                  </button>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Filters */}
      {showFilters && (
        <Card className="border-none shadow-md">
          <CardContent className="pt-6">
            <div className="flex gap-4 items-end">
              <div className="flex-1">
                <label className="text-sm font-medium mb-2 block">Видимость</label>
                <select
                  value={visibilityFilter}
                  onChange={(e) => setVisibilityFilter(e.target.value)}
                  className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                >
                  <option value="">Все</option>
                  <option value="public">Публичные</option>
                  <option value="private">Приватные</option>
                  <option value="secret">Секретные</option>
                </select>
              </div>
              {visibilityFilter && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setVisibilityFilter('')}
                >
                  <X className="h-4 w-4 mr-1" />
                  Сбросить
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="border-none shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-green-500/10 flex items-center justify-center">
                <Globe className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{publicCommunities.length}</p>
                <p className="text-xs text-muted-foreground">Публичных</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-none shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-orange-500/10 flex items-center justify-center">
                <Lock className="h-5 w-5 text-orange-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{privateCommunities.length}</p>
                <p className="text-xs text-muted-foreground">Приватных</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-none shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-purple-500/10 flex items-center justify-center">
                <Users className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{communitiesArray.length}</p>
                <p className="text-xs text-muted-foreground">Всего</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Empty State */}
      {communitiesArray.length === 0 ? (
        <Card className="border-none shadow-lg">
          <CardContent className="py-16 text-center">
            <div className="mx-auto w-20 h-20 rounded-full bg-gradient-to-br from-green-500/20 to-teal-500/20 flex items-center justify-center mb-6">
              <Users className="h-10 w-10 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Нет сообществ</h3>
            <p className="text-muted-foreground mb-6">
              Создайте первое сообщество и начните объединять людей!
            </p>
            <Button className="gap-2" asChild>
              <Link to="/communities/create">
                <Plus className="h-4 w-4" />
                Создать сообщество
              </Link>
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Featured Section */}
          {publicCommunities.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  <TrendingUp className="h-6 w-6 text-primary" />
                  Популярные сообщества
                </h2>
                <Button variant="ghost" size="sm" className="gap-1">
                  Все
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
              
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {publicCommunities.slice(0, 6).map((community: any, index: number) => {
                  const visibilityInfo = getVisibilityInfo(community.visibility);
                  const memberCount = community.members_count || 0;
                  
                  return (
                    <Card 
                      key={community.id}
                      className="group border-none shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden"
                      style={{ animationDelay: `${index * 50}ms` }}
                    >
                      {/* Header with gradient */}
                      <div className="h-24 bg-gradient-to-br from-green-500/20 via-emerald-500/20 to-teal-500/20 relative">
                        <div className="absolute -bottom-8 left-6">
                          <div className="h-16 w-16 rounded-full bg-gradient-to-br from-green-500 to-teal-500 flex items-center justify-center text-white shadow-lg border-4 border-white">
                            <Users className="h-8 w-8" />
                          </div>
                        </div>
                      </div>

                      <CardHeader className="pt-10">
                        <div className="flex items-start justify-between gap-2 mb-2">
                          <CardTitle className="text-lg group-hover:text-primary transition-colors line-clamp-1">
                            {community.name}
                          </CardTitle>
                          <span className={`px-2 py-1 text-xs rounded-full border font-medium flex items-center gap-1 flex-shrink-0 ${visibilityInfo.color}`}>
                            {visibilityInfo.icon}
                          </span>
                        </div>
                        <CardDescription className="line-clamp-2 min-h-[2.5rem]">
                          {community.description || 'Нет описания'}
                        </CardDescription>
                      </CardHeader>
                      
                      <CardContent className="space-y-3">
                        <div className="flex items-center gap-4 text-xs text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Users className="h-3 w-3" />
                            <span>{memberCount} участников</span>
                          </div>
                          {community.owner_username && (
                            <div className="flex items-center gap-1">
                              <Crown className="h-3 w-3 text-yellow-600" />
                              <span className="truncate">{community.owner_username}</span>
                            </div>
                          )}
                        </div>
                        
                        <Button 
                          variant="outline" 
                          className="w-full gap-2 group-hover:bg-primary group-hover:text-primary-foreground transition-colors" 
                          asChild
                        >
                          <Link to={`/communities/${community.id}`}>
                            Подробнее
                            <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                          </Link>
                        </Button>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </div>
          )}

          {/* Private Communities */}
          {privateCommunities.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  <Lock className="h-6 w-6 text-orange-600" />
                  Приватные сообщества
                </h2>
              </div>
              
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {privateCommunities.map((community: any) => {
                  const visibilityInfo = getVisibilityInfo(community.visibility);
                  
                  return (
                    <Card 
                      key={community.id}
                      className="border-none shadow-sm hover:shadow-md transition-shadow"
                    >
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2 mb-2">
                          <div className="h-10 w-10 rounded-full bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center text-white">
                            <Lock className="h-5 w-5" />
                          </div>
                          <span className={`px-2 py-1 text-xs rounded-full border font-medium flex items-center gap-1 ${visibilityInfo.color}`}>
                            {visibilityInfo.icon}
                          </span>
                        </div>
                        <CardTitle className="text-base line-clamp-1">{community.name}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <Button variant="ghost" size="sm" asChild className="w-full gap-1">
                          <Link to={`/communities/${community.id}`}>
                            Подробнее
                            <ArrowRight className="h-3 w-3" />
                          </Link>
                        </Button>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </div>
          )}

          {/* All Communities Section */}
          {communitiesArray.length > 6 && (
            <div className="text-center pt-4">
              <Button variant="outline" size="lg" className="gap-2">
                <Filter className="h-4 w-4" />
                Показать все сообщества
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
};