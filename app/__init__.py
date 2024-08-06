from flask import Flask
from .config import Config
from .models import init_db
from .routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
