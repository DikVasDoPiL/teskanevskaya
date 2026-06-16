# Контроллеры и маршруты этого модуля
from flask import render_template

from app.blueprints.main import main_bp
from .services import get_products_per_category


@main_bp.route('/')
@main_bp.route('/index')
def index():
    products_all = get_products_per_category(6)
    return render_template('main/home.html',
                           name='teskanevskaya',
                           products_all = products_all)

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('./main/404.html'), 404
