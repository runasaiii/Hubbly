import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from '@/features/auth/context/AuthContext';
import { usersApi, postsApi } from '@/shared/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/shared/components/ui/card';
import { Button } from '@/shared/components/ui/button';
import { Input } from '@/shared/components/ui/input';
import { Textarea } from '@/shared/components/ui/textarea';
import { Label } from '@/shared/components/ui/label';
import { formatDate } from '@/shared/lib/utils';
import type { Post, Profile } from '@/shared/types';
import { Edit2, Camera, MapPin, Calendar, Mail, Phone, Globe } from 'lucide-react';

export const ProfilePage = () => {
  const { userId } = useParams<{ userId?: string }>();
  const { user: currentUser, isLoading: authLoading, refreshUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    display_name: '',
    bio: '',
    location: '',
    interests: [] as string[],
    gender: 'other' as 'male' | 'female' | 'other',
    avatar: null as File | null,
  });
  const [interestsInput, setInterestsInput] = useState('');

  // Load profile data
  const { data: profileData, isLoading: profileLoading, error: profileError, refetch: refetchProfile } = useQuery({
    queryKey: ['profile', userId || 'me'],
    queryFn: async () => {
      if (!userId) {
        // Own profile
        if (!currentUser) {
          throw new Error('User not authenticated. Please log in.');
        }
        // Try to use profile from currentUser if available (from personal_data endpoint)
        if (currentUser.profile) {
          console.log('Using profile from currentUser');
          // Ensure interests is properly formatted - normalize to array of strings
          const profile = { ...currentUser.profile };
          if (profile.interests) {
            if (Array.isArray(profile.interests)) {
              profile.interests = profile.interests.map(i => typeof i === 'string' ? i : String(i));
            } else if (typeof profile.interests === 'object') {
              // Convert object to array
              profile.interests = Object.values(profile.interests).map(v => String(v));
            } else {
              profile.interests = [String(profile.interests)];
            }
          } else {
            profile.interests = [];
          }
          return { profile, user: currentUser };
        }
        // Otherwise fetch profile separately
        console.log('Fetching profile separately');
        try {
          const profile = await usersApi.getProfile();
          // Normalize interests from API response
          if (profile.interests) {
            if (Array.isArray(profile.interests)) {
              profile.interests = profile.interests.map(i => typeof i === 'string' ? i : String(i));
            } else if (typeof profile.interests === 'object') {
              profile.interests = Object.values(profile.interests).map(v => String(v));
            } else {
              profile.interests = [String(profile.interests)];
            }
          } else {
            profile.interests = [];
          }
          return { profile, user: currentUser };
        } catch (error) {
          console.error('Error fetching profile:', error);
          throw error;
        }
      } else {
        // Other user's profile
        console.log('Loading other user profile:', userId);
        try {
          const result = await usersApi.getUserProfile(userId);
          // Normalize interests from API response
          if (result.profile.interests) {
            if (Array.isArray(result.profile.interests)) {
              result.profile.interests = result.profile.interests.map(i => typeof i === 'string' ? i : String(i));
            } else if (typeof result.profile.interests === 'object') {
              result.profile.interests = Object.values(result.profile.interests).map(v => String(v));
            } else {
              result.profile.interests = [String(result.profile.interests)];
            }
          } else {
            result.profile.interests = [];
          }
          return result;
        } catch (error) {
          console.error('Error loading user profile:', error);
          throw error;
        }
      }
    },
    enabled: !userId ? (!authLoading && !!currentUser) : !authLoading, // Wait for auth to finish loading
    retry: 1,
    staleTime: 30000, // Cache for 30 seconds
  });

  const profile = profileData?.profile;
  const user = profileData?.user || currentUser;
  const isOwnProfile = !userId || (currentUser && userId === currentUser.id);

  // Load user posts - use user from profileData if available
  const targetUserId = userId || user?.id || currentUser?.id;
  const { data: userPosts = [], isLoading: postsLoading } = useQuery({
    queryKey: ['user-posts', targetUserId],
    queryFn: () => {
      if (!targetUserId) {
        throw new Error('User ID is required');
      }
      return postsApi.getUserPosts(targetUserId);
    },
    enabled: !!targetUserId && !!user, // Wait for user to be loaded
    retry: 1,
  });

  // Debug logging
  useEffect(() => {
    console.log('ProfilePage state:', {
      userId,
      authLoading,
      currentUser: currentUser ? { id: currentUser.id, email: currentUser.email } : null,
      profileLoading,
      profileData,
      profileError,
    });
  }, [userId, authLoading, currentUser, profileLoading, profileData, profileError]);

  useEffect(() => {
    if (profile) {
      // Ensure interests is an array of strings
      let interestsArray: string[] = [];
      if (Array.isArray(profile.interests)) {
        interestsArray = profile.interests.map(i => typeof i === 'string' ? i : String(i));
      } else if (profile.interests && typeof profile.interests === 'object') {
        // If it's an object, try to extract values
        interestsArray = Object.values(profile.interests).map(v => String(v));
      } else if (profile.interests) {
        interestsArray = [String(profile.interests)];
      }
      
      setFormData({
        display_name: profile.display_name || '',
        bio: profile.bio || '',
        location: profile.location || '',
        interests: interestsArray,
        gender: profile.gender || 'other',
        avatar: null,
      });
      setInterestsInput(interestsArray.join(', '));
      if (profile.avatar) {
        setAvatarPreview(profile.avatar);
      }
    }
  }, [profile]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFormData(prev => ({ ...prev, avatar: file }));
      const reader = new FileReader();
      reader.onloadend = () => {
        setAvatarPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleInterestsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInterestsInput(value);
    const interests = value.split(',').map(i => i.trim()).filter(i => i.length > 0);
    setFormData(prev => ({ ...prev, interests }));
  };

  const handleSave = async () => {
  if (!currentUser || !isOwnProfile) return;

  try {
    setIsSaving(true);

    // --- 1. Обновляем остальные поля профиля ---
    const payload: Partial<Profile> = {
      display_name: formData.display_name,
      bio: formData.bio,
      location: formData.location,
      gender: formData.gender,
      interests: formData.interests, // массив строк
    };

    await usersApi.updateProfile(payload);

    // --- 2. Если есть аватар, отправляем отдельно ---
    if (formData.avatar) {
      await usersApi.uploadAvatar(formData.avatar);
    }

    // --- 3. Обновляем локальный стейт и данные ---
    setIsEditing(false);
    await refetchProfile();
    await refreshUser();

    console.log('Профиль успешно обновлен');
  } catch (error: any) {
    console.error('Не удалось обновить профиль:', error);
    alert('Не удалось обновить профиль');
  } finally {
    setIsSaving(false);
  }
};




  const handleCancel = () => {
    if (profile) {
      // Ensure interests is an array of strings
      let interestsArray: string[] = [];
      if (Array.isArray(profile.interests)) {
        interestsArray = profile.interests.map(i => typeof i === 'string' ? i : String(i));
      } else if (profile.interests && typeof profile.interests === 'object') {
        interestsArray = Object.values(profile.interests).map(v => String(v));
      } else if (profile.interests) {
        interestsArray = [String(profile.interests)];
      }
      
      setFormData({
        display_name: profile.display_name || '',
        bio: profile.bio || '',
        location: profile.location || '',
        interests: interestsArray,
        gender: profile.gender || 'other',
        avatar: null,
      });
      setInterestsInput(interestsArray.join(', '));
      setAvatarPreview(profile.avatar || null);
    }
    setIsEditing(false);
  };

  if (authLoading || profileLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>{authLoading ? 'Загрузка пользователя...' : 'Загрузка профиля...'}</p>
        </div>
      </div>
    );
  }

  if (profileError) {
    console.error('Profile error:', profileError);
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center max-w-md">
          <p className="text-red-600 mb-4 text-lg font-semibold">Ошибка загрузки профиля</p>
          <p className="text-sm text-muted-foreground mb-4">
            {profileError instanceof Error ? profileError.message : 'Неизвестная ошибка'}
          </p>
          {userId && (
            <p className="text-xs text-muted-foreground mb-4">
              Пытались загрузить профиль пользователя с ID: {userId}
            </p>
          )}
          <Button onClick={() => refetchProfile()}>Попробовать снова</Button>
        </div>
      </div>
    );
  }

  if (!user || !profile) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-lg mb-2">Пользователь не найден</p>
          <p className="text-sm text-muted-foreground mb-4">
            {userId ? `Пользователь с ID ${userId} не существует` : 'Профиль не найден'}
          </p>
          {!userId && (
            <Button onClick={() => refetchProfile()}>Обновить</Button>
          )}
        </div>
      </div>
    );
  }

  const displayName = profile.display_name || user.username || user.email;

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      {/* Cover Photo Section */}
      <div className="relative h-64 bg-gradient-to-r from-primary/20 via-primary/10 to-secondary/20">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        {isOwnProfile && !isEditing && (
          <div className="absolute top-4 right-4">
            <Button onClick={() => setIsEditing(true)} variant="secondary" size="sm">
              <Edit2 className="w-4 h-4 mr-2" />
              Редактировать профиль
            </Button>
          </div>
        )}
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 -mt-20 relative z-10">
        {/* Profile Header */}
        <Card className="border-0 shadow-xl">
          <CardContent className="pt-6">
            <div className="flex flex-col sm:flex-row gap-6">
              {/* Avatar */}
              <div className="relative flex-shrink-0">
                <div className="relative">
                  {avatarPreview ? (
                    <img
                      src={avatarPreview}
                      alt="Avatar"
                      className="w-32 h-32 rounded-full object-cover border-4 border-background shadow-lg"
                    />
                  ) : (
                    <div className="w-32 h-32 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-4xl font-bold text-white shadow-lg border-4 border-background">
                      {displayName[0]?.toUpperCase() || user.email[0].toUpperCase()}
                    </div>
                  )}
                  {isEditing && (
                    <label className="absolute bottom-0 right-0 bg-primary text-primary-foreground rounded-full p-2 cursor-pointer hover:bg-primary/90 transition-colors shadow-lg">
                      <Camera className="w-4 h-4" />
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleAvatarChange}
                        className="hidden"
                      />
                    </label>
                  )}
                </div>
              </div>

              {/* Profile Info */}
              <div className="flex-1 space-y-4">
                <div>
                  <h1 className="text-3xl font-bold">{displayName}</h1>
                  {user.username && (
                    <p className="text-muted-foreground">@{user.username}</p>
                  )}
                  {profile.is_verified && (
                    <span className="inline-flex items-center gap-1 mt-2 px-2 py-1 bg-primary/10 text-primary rounded-full text-xs font-medium">
                      ✓ Верифицирован
                    </span>
                  )}
                </div>

                {profile.bio && !isEditing && (
                  <p className="text-lg text-muted-foreground">{profile.bio}</p>
                )}

                {/* Stats */}
                <div className="flex flex-wrap gap-6 pt-2">
                  <div>
                    <div className="text-2xl font-bold">{userPosts.length}</div>
                    <div className="text-sm text-muted-foreground">Постов</div>
                  </div>
                  {profile.location && (
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <MapPin className="w-4 h-4" />
                      <span>{profile.location}</span>
                    </div>
                  )}
                  {user.date_joined && (
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Calendar className="w-4 h-4" />
                      <span>Присоединился {new Date(user.date_joined).toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          {/* Left Column - Profile Details */}
          <div className="lg:col-span-1 space-y-6">
            {/* About Section */}
            <Card>
              <CardHeader>
                <CardTitle>О пользователе</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {isEditing ? (
                  <>
                    <div>
                      <Label htmlFor="display_name">Отображаемое имя</Label>
                      <Input
                        id="display_name"
                        name="display_name"
                        value={formData.display_name}
                        onChange={handleInputChange}
                        placeholder="Ваше отображаемое имя"
                        className="mt-2"
                      />
                    </div>
                    <div>
                      <Label htmlFor="bio">О себе</Label>
                      <Textarea
                        id="bio"
                        name="bio"
                        value={formData.bio}
                        onChange={handleInputChange}
                        placeholder="Расскажите о себе..."
                        rows={4}
                        className="mt-2"
                      />
                    </div>
                    <div>
                      <Label htmlFor="location">Местоположение</Label>
                      <Input
                        id="location"
                        name="location"
                        value={formData.location}
                        onChange={handleInputChange}
                        placeholder="Город, Страна"
                        className="mt-2"
                      />
                    </div>
                    <div>
                      <Label htmlFor="gender">Пол</Label>
                      <select
                        id="gender"
                        name="gender"
                        value={formData.gender}
                        onChange={handleInputChange}
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm mt-2"
                      >
                        <option value="male">Мужской</option>
                        <option value="female">Женский</option>
                        <option value="other">Другой</option>
                      </select>
                    </div>
                    <div>
                      <Label htmlFor="interests">Интересы (через запятую)</Label>
                      <Input
                        id="interests"
                        value={interestsInput}
                        onChange={handleInterestsChange}
                        placeholder="Программирование, Музыка, Спорт..."
                        className="mt-2"
                      />
                    </div>
                    <div className="flex gap-2 pt-2">
                      <Button onClick={handleSave} disabled={isSaving} className="flex-1">
                        {isSaving ? 'Сохранение...' : 'Сохранить'}
                      </Button>
                      <Button onClick={handleCancel} variant="outline" className="flex-1">
                        Отмена
                      </Button>
                    </div>
                  </>
                ) : (
                  <>
                    {profile.bio && (
                      <div>
                        <p className="text-sm text-muted-foreground mb-1">О себе</p>
                        <p>{profile.bio}</p>
                      </div>
                    )}
                    {profile.location && (
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-muted-foreground" />
                        <span>{profile.location}</span>
                      </div>
                    )}
                    {user.email && (
                      <div className="flex items-center gap-2">
                        <Mail className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm">{user.email}</span>
                      </div>
                    )}
                    {user.phone_number && (
                      <div className="flex items-center gap-2">
                        <Phone className="w-4 h-4 text-muted-foreground" />
                        <span>{user.phone_number}</span>
                      </div>
                    )}
                    {user.city && user.country && (
                      <div className="flex items-center gap-2">
                        <Globe className="w-4 h-4 text-muted-foreground" />
                        <span>{user.city}, {user.country}</span>
                      </div>
                    )}
                    {(() => {
                      // Handle interests - can be array, object, or string
                      let interestsArray: string[] = [];
                      if (Array.isArray(profile.interests)) {
                        interestsArray = profile.interests.map(i => typeof i === 'string' ? i : String(i));
                      } else if (profile.interests && typeof profile.interests === 'object') {
                        // If it's an object, try to extract values or convert to string
                        interestsArray = Object.values(profile.interests).map(v => String(v));
                      } else if (profile.interests) {
                        interestsArray = [String(profile.interests)];
                      }
                      
                      return interestsArray.length > 0 && (
                        <div>
                          <p className="text-sm text-muted-foreground mb-2">Интересы</p>
                          <div className="flex flex-wrap gap-2">
                            {interestsArray.map((interest, index) => (
                              <span
                                key={index}
                                className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
                              >
                                {String(interest)}
                              </span>
                            ))}
                          </div>
                        </div>
                      );
                    })()}
                  </>
                )}
              </CardContent>
            </Card>

            {/* Personal Info */}
            <Card>
              <CardHeader>
                <CardTitle>Личная информация</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                {user.full_name && (
                  <div>
                    <span className="text-muted-foreground">Полное имя:</span>
                    <p className="font-medium">{user.full_name}</p>
                  </div>
                )}
                {user.first_name && (
                  <div>
                    <span className="text-muted-foreground">Имя:</span>
                    <p className="font-medium">{user.first_name}</p>
                  </div>
                )}
                {user.last_name && (
                  <div>
                    <span className="text-muted-foreground">Фамилия:</span>
                    <p className="font-medium">{user.last_name}</p>
                  </div>
                )}
                {user.birthdate && (
                  <div>
                    <span className="text-muted-foreground">Дата рождения:</span>
                    <p className="font-medium">{new Date(user.birthdate).toLocaleDateString('ru-RU')}</p>
                  </div>
                )}
                {user.date_joined && (
                  <div>
                    <span className="text-muted-foreground">Дата регистрации:</span>
                    <p className="font-medium">{new Date(user.date_joined).toLocaleDateString('ru-RU')}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Posts */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Посты</CardTitle>
                <CardDescription>Все посты пользователя</CardDescription>
              </CardHeader>
              <CardContent>
                {postsLoading ? (
                  <div className="text-center py-8">Загрузка постов...</div>
                ) : userPosts.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    {isOwnProfile ? 'У вас пока нет постов. Создайте первый!' : 'У пользователя пока нет постов.'}
                  </div>
                ) : (
                  <div className="space-y-4">
                    {userPosts.map((post: Post) => (
                      <Card key={post.id} className="hover:shadow-md transition-shadow">
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-sm font-bold">
                                {post.author_username?.[0]?.toUpperCase() || 'U'}
                              </div>
                              <div>
                                <CardTitle className="text-base">{post.author_username}</CardTitle>
                                <p className="text-xs text-muted-foreground">
                                  {formatDate(post.created_at)}
                                </p>
                              </div>
                            </div>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <p className="mb-4 whitespace-pre-wrap">{post.content}</p>
                          {post.tags && post.tags.length > 0 && (
                            <div className="flex flex-wrap gap-2 mb-4">
                              {post.tags.map((tag) => (
                                <span
                                  key={tag.id}
                                  className="px-2 py-1 text-xs bg-secondary rounded-md"
                                >
                                  #{tag.name}
                                </span>
                              ))}
                            </div>
                          )}
                          <Button variant="outline" size="sm" >
                            <Link to={`/posts/${post.id}`}>Читать далее</Link>
                          </Button>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};
