from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from app import settings


db = SQLAlchemy()
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

DB_URI = f"postgresql+psycopg2://" \
       f"{settings.DATABASE['USER']}:{settings.DATABASE['PASSWORD']}@{settings.DATABASE['HOST']}:" \
       f"{settings.DATABASE['PORT']}/{settings.DATABASE['NAME']}"

REDIS_URL = f"redis://{settings.REDIS['HOST']}:{settings.REDIS['PORT']}/{settings.REDIS['DB']}"

app = Flask(__name__)

app.config.update(SQLALCHEMY_DATABASE_URI=DB_URI,
                  SECRET_KEY=settings.SECRET_KEY,
                  REDIS_URL=REDIS_URL)

db.init_app(app)
redis_db = FlaskRedis(app)

token_auth = HTTPTokenAuth()
basic_auth = HTTPBasicAuth()





