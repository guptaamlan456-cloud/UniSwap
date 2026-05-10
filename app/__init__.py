import cloudinary
import cloudinary.uploader
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from config import Config

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models before creating tables
    from app import models

    with app.app_context():
        db.create_all()

    cloudinary.config(
        cloud_name=app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=app.config.get("CLOUDINARY_API_KEY"),
        api_secret=app.config.get("CLOUDINARY_API_SECRET"),
    )

    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    from app.routes.listings import listings_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_current_year():
        return {"current_year": datetime.now().year}

    return app