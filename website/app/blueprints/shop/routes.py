from flask import render_template, redirect, url_for, request, flash
from sqlalchemy.orm import joinedload

from app import db

from app.models import Category, Product, Order

from app.blueprints.shop import shop_bp
from app.blueprints.shop.forms import OrderForm
from app.blueprints.shop.functions import send_message

from app.blueprints.admin.forms import ProductForm


PER_PAGE=25

@shop_bp.route('/')
@shop_bp.route('/<int:page>')
def index(page=1):
    context = {}
    per_page = PER_PAGE
    categories = Category.query.all()
    products = (Product.query
                .options(joinedload(Product.category))
                .paginate(page=page,
                         per_page=per_page,
                         error_out=False))

    return render_template('./shop/index.html',
                           title=f"Каталог товаров",
                           pagination=products,
                           categories=categories,
                           context=context)


@shop_bp.route('/<string:cat_name>')
@shop_bp.route('/<string:cat_name>/<int:page>')
def products_by_category(cat_name:str, page=1):
    context = {}
    per_page = PER_PAGE
    categories = Category.query.all()
    cat = Category.query.filter_by(name=cat_name).first()

    context['cat_name'] = cat.name

    if not cat:
        return redirect(url_for('shop.index'))

    products = (Product.query
                .filter_by(category_id=cat.id)
                .options(joinedload(Product.category))
                .paginate(page=page, per_page=per_page, error_out=False))

    return render_template('./shop/index.html',
                           title=f"Каталог товаров",
                           pagination=products,
                           categories=categories,
                           context=context)


@shop_bp.route('/<string:category_name>/<string:product_name>', methods=["GET", "POST"])
def order(category_name, product_name):
    context = {'cat_name': category_name, 
               'product_name': product_name, 
               }
    back_url = request.args.get('back_url', default=url_for('shop.index'))
    cat = Category.query.filter_by(name=category_name).first()
    product = Product.query.filter_by(name=product_name).first()
    selected_fields = {item.id: item.name for item in cat.fields}

    if not cat or not product:
        return redirect(url_for('main.index'))

    order_form = OrderForm()
    product_form = ProductForm(obj=product)
    order_form.product_id.data = product.id

    saved_data = product_form.custom_fields_data.data
    context['custom_fields'] = {value: saved_data.get(str(id)) for id, value in selected_fields.items()}
    context['product_fields'] = {
        field.name : {
            'label' : field.label.text,
            'data' : field.data
            } for field in product_form if field.name not in [
                'csrf_token', 
                'submit_save', 
                'submit_cancel', 
                'submit_delete', 
                'submit_new', 
                'image']
            }
    
    if request.method == "POST":
        if order_form.submit_cancel.data:
            return redirect(back_url)
        if order_form.validate_on_submit():
            
            order_new = Order()
            order_form.populate_obj(order_new)
            db.session.add(order_new)
            db.session.commit()

            email_body = f"""
                Новый заказ №{order_new.id}!

                Отправитель: {order_form.username.data}
                Телефон: {order_form.phone.data}

                Продукт: {product.category.name}: {product.name} {'+ установка' if order_form.installation.data else ""}
                {'Доставка: ' + order_form.address.data if order_form.address.data else "Самовывоз"}

                Комментарий к заказу: {order_form.usercomment.data}
            """

            result = send_message(email_body)

            flash(f'Заказ [{order_new.username}, {product.name}] создан и сохранен! 😊')
            
            return redirect(url_for('shop.index'))
    
    return render_template('./shop/order.html',
                           title=f"Заказ {product_name}",
                           form=order_form,
                           context=context)

