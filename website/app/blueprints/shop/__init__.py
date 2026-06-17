# Blueprint системы заказов
# Создание и экспорт объекта Blueprint
from flask import Blueprint


shop_bp = Blueprint('shop', __name__)
from app.blueprints.shop import routes