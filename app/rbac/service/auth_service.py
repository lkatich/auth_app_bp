from flask import request, g
from flask_restx import abort
import datetime
import jwt

from app.instances import db, redis_db, basic_auth, token_auth
from app.models import User
from app import settings


def generate_token(user, expires_in):
    now = datetime.datetime.utcnow()
    payload = {
        'iat': now,
        'exp': now + datetime.timedelta(seconds=expires_in),
        'uuid': str(user.uuid)
    }
    token = jwt.encode(payload, settings.ENCODING_SECRET_KEY, algorithm='HS256')
    redis_db.set(token, str(user.uuid), ex=expires_in)
    return token


@basic_auth.verify_password
def verify_password(email, password):
    email = email.strip().lower()
    g.user = None
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return abort(404, 'User does not exist')
    if not user.password:
        return abort(401, error_code=102, text='Password expired or not set')
    if not user.verify_password(password):
        return abort(401, error_code=101, text='Incorrect password')
    g.user = user
    return user


@token_auth.verify_token
def verify_token(token):
    g.user = None
    g.token = token
    user_uuid = redis_db.get(token)
    if not user_uuid:
        return False
    user = db.session.query(User).filter_by(uuid=user_uuid.decode('utf-8')).first()
    if not user:
        return False
    if not user.password:
        redis_db.delete(token)
        return False
    g.user = user
    return True


def login_user():
    user = g.user
    exp = request.args.get('exp') or settings.TOKEN_EXPIRES_IN
    refresh_exp = request.args.get('refresh_exp') or settings.REFRESH_TOKEN_EXPIRES_IN

    token = generate_token(user, exp)
    ref_token = generate_token(user, refresh_exp)

    response = {
        'user_uuid': str(user.uuid),
        'token': token,
    }
    return response, 200, {'Set-Cookie': f'refresh-token={ref_token}; HttpOnly; Path=/'}


def logout_user():
    user = g.user
    token = g.token
    if token:
        redis_db.delete(token)
    return {
        'status': 'success',
        'message': str(user.uuid)
    }


def refresh_token():
    ref_token = request.cookies.get('refresh-token')
    if not ref_token:
        return abort(401, 'Cannot find refresh token')
    user_uuid = redis_db.get(ref_token)
    if not user_uuid:
        return abort(401, 'Refresh token expired')
    redis_db.delete(ref_token)
    user = db.session.query(User).filter_by(uuid=user_uuid).first()
    g.user = user
    return login_user()


