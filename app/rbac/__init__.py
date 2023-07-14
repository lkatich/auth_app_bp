from flask import Blueprint
from flask_restx import Api
from app.dto import AuthDto, UserDto
from app.rbac.controller import auth_controller, user_controller


AUTHORIZATIONS = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
    'basic': {
        'type': 'basic',
        'in': 'header'
    }
}


rbac_blueprint = Blueprint('rbac', __name__)
rbac_api = Api(rbac_blueprint,
               version="1.0",
               title='Auth and users management API',
               description='Auth and users management API',
               security='Bearer Auth',
               authorizations=AUTHORIZATIONS)

rbac_api.add_namespace(AuthDto.api)
rbac_api.add_namespace(UserDto.api)


