from decouple import config

DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('HUBBLY_SECRET_KEY')