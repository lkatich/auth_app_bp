import datetime
from uuid import uuid4
from passlib.apps import custom_app_context
from sqlalchemy import (Column, Integer, String, Boolean, DateTime)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app.instances import db


class User(db.Model):

    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(), index=True)
    _email = Column('email', String(256))
    _password = Column(String)
    registered_on = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=lambda: uuid4())
    is_active = Column('is_active', Boolean, default=True)

    def __str__(self):
        return f'{self.username}'

    @hybrid_property
    def email(self):
        return self._email

    @email.getter
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email.strip().lower()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self._password)

