from flask import Flask
from .config import Config
from .models import init_db
from .routes import auth_bp
from .project_routes import project_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(project_bp, url_prefix="/projects")

    return app
