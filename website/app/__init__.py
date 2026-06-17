# Главный пакет приложения
# Инициализация приложения и фабрика (Application Factory)
import os

from flask import Flask, send_from_directory

from app.config import Config
from app.extentions import db, migrate, login_manager, mail
from app.models import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Автоматическое создание папки uploads при старте приложения
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Роут для отдачи файлов. Доступен по адресу: /uploads/имя_файла.jpg
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        # Безопасно отдаем файл из глобальной директории конфигурации
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Привязываем расширения к конкретному экземпляру app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Функция для восстановления объекта пользователя из сессии по его id
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Импортируем модели, чтобы Flask-Migrate "увидел" их перед созданием таблиц
    from app import models

    from app.blueprints.main import main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.blueprints.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.blueprints.shop import shop_bp
    app.register_blueprint(shop_bp, url_prefix='/shop')
    
    return app

