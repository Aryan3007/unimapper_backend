from flask import Flask
from flask_cors import CORS
import os

from .config import Config
from .models import init_db
from .routes import auth_bp
from .note_routes import note_bp
from .flowcharts_routes import flowcharts_bp


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})

    init_db(app)

    os.makedirs(app.config.get("UPLOAD_FOLDER_PATH"), exist_ok=True)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(note_bp, url_prefix="/notes")
    app.register_blueprint(flowcharts_bp, url_prefix="/flowcharts")

    return app
