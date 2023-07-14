from app.instances import app, db
from flask_migrate import Migrate
from app.models import User
from app.rbac import rbac_blueprint

Migrate(app, db)

app.register_blueprint(rbac_blueprint, url_prefix='/api/v1/rbac')

