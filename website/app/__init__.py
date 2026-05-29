# Главный пакет приложения
# Инициализация приложения и фабрика (Application Factory)
import os
from flask import Flask
from .config import Config
from .extentions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)


    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.admin import dash_bp
    app.register_blueprint(dash_bp)
    
    from app.public import public_bp
    app.register_blueprint(public_bp)

    return app