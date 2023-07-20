import uuid
import datetime

from app.instances import db
from app.models import User
from flask_restx import abort
from flask import g


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            uuid=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    else:
        response_object = {
            'status': 'error',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return db.session.query(User).filter_by(is_active=True).all()


def get_user(user_uuid):
    user = db.session.query(User).filter_by(uuid=user_uuid).first()
    if not user:
        abort(404, 'Not found')
    return user


def update_user(user_uuid, data):
    user = db.session.query(User).filter_by(uuid=user_uuid).filter_by(is_active=True).first()
    if not user:
        return abort(404, 'User not found')

    kwargs = {k: v for k, v in data.items() if k in (column.key for column in User.__table__.columns)}

    email = data.get('email')
    username = data.get('username')

    if username:
        found_user = db.session.query(User).filter_by(username=username, is_active=True).first()
        if found_user and user is not found_user:
            return abort(422, f'User with username = {username} already exists', status='fail')

    if email and user.email != email:
        if db.session.query(User).filter_by(email=email, is_active=True).first():
            return abort(422, f'User with email = {email} already exists. Please change your email', status='fail')

    for key, value in kwargs.items():
        if key in ('id', 'uuid', 'password'):
            continue
        setattr(user, key, value)
    db.session.commit()
    return user


def delete_user(user_uuid):
    user = db.session.query(User).filter_by(uuid=user_uuid, is_active=True).first()
    if not user:
        return abort(404, 'User not found')
    if user is g.user:
        return abort(403, 'You cannot remove yourself')
    db.session.delete(user)
    db.session.commit()
    return None, 204
