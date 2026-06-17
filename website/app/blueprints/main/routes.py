# Контроллеры и маршруты этого модуля
from flask import render_template

from app.blueprints.main import main_bp
from .services import get_products_per_category, get_product_by_name, get_products_by_category


@main_bp.route('/index')
@main_bp.route('/')
def index():
    products_all = get_products_per_category(6)
    return render_template('main/home.html',
                           name='teskanevskaya',
                           products_all = products_all)

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('./main/404.html'), 404


@main_bp.route('/product/<name>')
def product(name):
    if the_product := get_product_by_name(name):
        # another_products = get_products_by_category(the_product10)
        
        return render_template('main/product.html',
                            name='teskanevskaya',
                            product=the_product.__dict__)
    return render_template('./main/404.html'), 404
