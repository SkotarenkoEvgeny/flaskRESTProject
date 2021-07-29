import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(
    #     BASE_DIR / 'data' /
    #     'db.sqlite3'
    #     )
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://flask_user:master@127.0.0.1:5432" \
                   "/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
