from flask import request
from flask_restx import Resource

from app.dto import UserDto
from ..service.user_service import save_new_user, get_user, update_user, delete_user, get_all_users
from app.instances import token_auth


api = UserDto.api
user = UserDto.model
user_input_model = UserDto.input_model


@api.route('')
class User(Resource):
    @api.expect(user_input_model, validate=True)
    @api.response(201, 'User successfully created.')
    def post(self):
        """Create a new User """
        data = request.json
        return save_new_user(data=data)

    @token_auth.login_required
    @api.marshal_list_with(user)
    def get(self):
        """List all registered users"""
        return get_all_users()


@api.route('/<uuid>')
@api.param('uuid', 'The User identifier')
@api.response(404, 'User not found.')
class UserByUuidResource(Resource):
    @token_auth.login_required
    @api.marshal_with(user, skip_none=True)
    def get(self, uuid):
        """Get a user given its identifier"""
        return get_user(uuid)

    @api.response(200, 'User successfully update')
    @token_auth.login_required
    @api.marshal_with(user, skip_none=True)
    def put(self, uuid):
        """Update user"""
        data = request.json
        return update_user(uuid, data)

    @api.response(200, 'User removed')
    @token_auth.login_required
    def delete(self, uuid):
        """Delete user"""
        return delete_user(uuid)
