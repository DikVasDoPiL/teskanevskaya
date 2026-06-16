# Blueprint основного контента
# Создание и экспорт объекта Blueprint
from flask import Blueprint


main_bp = Blueprint('main', __name__)
from app.blueprints.main import routes