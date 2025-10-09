from decouple import config


ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)

ENV_ID = config("HUBBLY_ENV_ID", default = "local")
SECRET_KEY = config("HUBBLY_SECRET_KEY")