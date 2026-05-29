# Blueprint основного контента
# Создание и экспорт объекта Blueprint
from flask import Blueprint


public_bp = Blueprint('public', __name__)
from app.public import routes