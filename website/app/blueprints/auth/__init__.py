# Blueprint системы авторизации
from flask import Blueprint

# Создаем blueprint. Имя 'auth' будет использоваться в url_for('auth.login')
auth_bp = Blueprint('auth', __name__)

from app.blueprints.auth import routes