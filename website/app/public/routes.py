# Контроллеры и маршруты этого модуля
from flask import render_template

from . import public_bp as app
from .services import get_products_per_category


@app.route('/', methods=['GET'])
def index():
    products_all = get_products_per_category(6)
    return render_template('public/home.html',
                           name='teskanevskaya',
                           products_all = products_all)

@app.app_errorhandler(404)
def page_not_found(e):
    return render_template('./public/404.html'), 404