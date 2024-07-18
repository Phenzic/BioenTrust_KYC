from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config.database import get_db
from .config import Config
from .utils import init_utils


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True, origins=app.config["CORS_ORIGINS"])

    from .auth.views import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/user")

    init_utils(app)
    jwt = JWTManager(app)
    with app.app_context():
        app.db = get_db()

    return app
