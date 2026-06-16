# Подключение БД, авторизации и других расширений
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Куда перенаправлять пользователя, если у него нет доступа к приватной странице
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, авторизуйтесь для доступа к этой странице.'
login_manager.login_message_category = 'info'