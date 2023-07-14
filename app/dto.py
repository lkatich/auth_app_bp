from flask_restx import Namespace, Model
from flask_restx.fields import String


class StringUuid(String):
    __schema_type__ = 'string'
    __schema_format__ = 'string_uuid'
    __schema_example__ = 'dd582923-b56d-4847-aed2-174f16b5dc3c'


class EmailString(String):
    __schema_type__ = 'string'
    __schema_format__ = 'email_string'
    __schema_example__ = 'support@test.net'


user_model = Model('User', {
    'email': EmailString(required=True, description='user email address'),
    'username': String(required=True, description='user username'),
    'uuid': StringUuid(description='user Identifier'),
})


class AuthDto:
    api = Namespace('auth', description='Auth methods')
    token = api.model('Token', {
        'token': String(required=True, description='rbac token'),
        'user_uuid': StringUuid(required=True, description='user id'),
    })


class UserDto:
    api = Namespace('user', description='User related operations')
    model = api.model('UserOutput', user_model)
    input_model = api.inherit('User', model, {
        'password': String(description='user password', pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,20}$")
    })


