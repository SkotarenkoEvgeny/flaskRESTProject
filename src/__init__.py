from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from  flask_migrate import Migrate

from src import config

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from . import routes, models
