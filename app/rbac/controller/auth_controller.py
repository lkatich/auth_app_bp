from ..service.auth_service import login_user, logout_user
from flask_restx import Resource
from app.instances import basic_auth, token_auth
from app.dto import AuthDto

api = AuthDto.api
parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers',
                    help='Bearer Access Token', required=True)


@api.route('')
class AuthLogin(Resource):
    @api.response(200, 'User successfully authorized.')
    @api.response(404, 'User not found.')
    @basic_auth.login_required
    def post(self):
        return login_user()


@api.route('/logout')
class AuthLogout(Resource):
    @token_auth.login_required
    def post(self):
        return logout_user()


