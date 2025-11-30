import { useAuth } from '@/features/auth/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card';

export const ProfilePage = () => {
  const { user } = useAuth();

  if (!user) {
    return <div>Загрузка профиля...</div>;
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Профиль</h1>
        <p className="text-muted-foreground">Информация о вашем аккаунте</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Личная информация</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <span className="font-medium">Email:</span> {user.email}
          </div>
          {user.username && (
            <div>
              <span className="font-medium">Имя пользователя:</span> {user.username}
            </div>
          )}
          {user.full_name && (
            <div>
              <span className="font-medium">Полное имя:</span> {user.full_name}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

