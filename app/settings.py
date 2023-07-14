import os

DATABASE = {
    'HOST': os.environ['DB_HOST'],
    'PORT': os.environ['DB_PORT'],
    'NAME': os.environ['DB_NAME'],
    'USER': os.environ['DB_USER'],
    'PASSWORD': os.environ['DB_PASSWORD'],
}

# DATABASE = {
#     'HOST': '127.0.0.1',
#     'PORT': 5432,
#     'NAME': 'bp_app',
#     'USER': 'postgres',
#     'PASSWORD': 'postgres',
# }

REDIS = {
    'HOST': os.environ['REDIS_HOST'],
    'PORT': os.environ['REDIS_PORT'],
    'DB': os.environ['REDIS_DB']
}

# REDIS = {
#     'HOST': '127.0.0.1',
#     'PORT': 6379,
#     'DB': 0
# }

SECRET_KEY = "AuthAppSecretKey"

TOKEN_EXPIRES_IN = 3600
REFRESH_TOKEN_EXPIRES_IN = 3600
ENCODING_SECRET_KEY = "sw_secret"