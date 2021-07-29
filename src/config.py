import pathlib

from decouple import config

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://" \
                              f"{config('USERNAME_DB')}:" \
                              f"{config('PASSWORD_DB')}@127.0.0.1:5432/" \
                              f"{config('DATABASE_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
