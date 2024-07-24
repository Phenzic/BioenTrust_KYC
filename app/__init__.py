from flask_jwt_extended import JWTManager
from .api.views import sandbox, live
from .client_app.views import c_app
from .config.database import get_db
from .services.views import api
from .admin.views import admin
from .utils import init_utils
from .auth.views import auth
from flask_cors import CORS
from .config import Config
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True, origins=app.config["CORS_ORIGINS"])

    app.register_blueprint(sandbox, url_prefix='/api/sandbox')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(live, url_prefix='/api/live')
    app.register_blueprint(auth, url_prefix="/user")
    app.register_blueprint(c_app, url_prefix='/app')
    app.register_blueprint(api, url_prefix='/api')

    init_utils(app)
    jwt = JWTManager(app)
    with app.app_context():
        app.db = get_db()

    return app
