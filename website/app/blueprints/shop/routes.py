from flask import render_template, redirect, url_for, request, flash
from app import db

from app.models import Category, CustomFields, Promotion, Product

from app.blueprints.shop import shop_bp
from app.blueprints.shop.forms import OrderForm
from app.blueprints.admin.forms import ProductForm


@shop_bp.route('/<string:category_name>/<string:product_name>', methods=["GET", "POST"])
def order(category_name, product_name):
    cat = Category.query.filter_by(name=category_name).first()
    product = Product.query.filter_by(name=product_name).first()
    selected_fields = cat.fields

    if not cat or not product:
        return redirect(url_for('main.index'))

    order_form = OrderForm()
    product_form = ProductForm(obj=product)

    
    return render_template('./shop/order.html',
                           title=f"Заказ {product_name}",
                           form=order_form,
                           product=product_form,
                           custom_fields=selected_fields)

