import os
import json
from datetime import datetime

from PIL import Image
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from . import app, db
from .forms import LoginForm, CategoryForm, PromotionForm, ProductForm, CustomFieldsForm
from .models import User, Category, Promotion, Product, CustomFields
from .functions import get_products_per_category


@app.route('/', methods=['get'])
def index():
    products_all = get_products_per_category(6)

    return render_template('./public/home.html',
                           name='teskanevskaya',
                           products_all=products_all)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('./public/404.html'), 404


@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect('/dash')
    form = LoginForm()
    return render_template('./admin/login.html', name='login', form=form, title="Авторизация")


@app.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect('/dash')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            print(form.username.data, generate_password_hash(form.password.data))
            user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data))
            if user is None or not user.check_password(form.password.data):
                flash('Ошибка авторизации - проверьте вводимые имя пользователя и пароль')
                return render_template('login.html', title='Авторизация', form=form)
            login_user(user, remember=True)
            return redirect('/dash/products')
        else:
            return render_template('./admin/login.html', title='Авторизация', form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
    return redirect(url_for('login_get'))


@app.route("/dash", methods=["GET"])
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    return render_template('./admin/dashboard.html', title="Панель управления")


@app.route("/dash/categories", methods=["GET", "POST"])
def categories():
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    categories_all = Category.query.order_by(Category.name).all()
    form = CategoryForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit_new.data:
                cat_new = Category()
                form.populate_obj(cat_new)
                if not Category.query.filter_by(name=form.name.data).first():
                    db.session.add(cat_new)
                    db.session.commit()
                    flash(f'Категория {cat_new.name} добавлена успешно! 🚀')
                    categories_all.append(cat_new)
                else:
                    flash(f'Категория  {cat_new.name}  уже существует! Выберите другое имя.', 'error')
                    redirect(url_for("categories"), code=301)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('./admin/categories.html',
                           title="Категории",
                           categories=categories_all,
                           form=form)


@app.route('/dash/categories/<string:name>', methods=["GET", "POST"])
def category(name):
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    cat = Category.query.filter_by(name=name).first()
    available_fields = CustomFields.query.filter_by(active=True).all()
    selected_fields = cat.fields
    
    if not cat:
        return redirect(url_for('categories'))
    form = CategoryForm(obj=cat)

    if request.method == "POST":
        
        if form.validate_on_submit():
            target_obj = Category.query.filter_by(name=form.name.data).first()
            if form.submit_save.data:
                print("submit_save:", target_obj)
                updated_fields = CustomFields.query.filter(CustomFields.name.in_(request.form.getlist('custom_field'))).all()
                if not target_obj or cat.id == target_obj.id:
                    form.populate_obj(cat)
                    cat.fields = updated_fields
                    db.session.commit()
                    flash(f'Категория [{cat.name}] сохранена! 😊')
                    return redirect(url_for('categories'))
                else:
                    print("error_save:", target_obj)
                    flash(f'Категория {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('category.html',
                                    title="Редактирование категории",
                                    form=form,
                                    available_fields=available_fields,
                                    selected_fields=selected_fields)
            if form.submit_cancel.data:
                return redirect(url_for('categories'))
    return render_template('./admin/category.html',
                           title=f"Категория {name}",
                           form=form,
                           available_fields=available_fields,
                           selected_fields=selected_fields)


@app.route("/dash/promotions", methods=["GET", "POST"])
def promotions():
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    promotions_all = Promotion.query.order_by(Promotion.end.desc()).all()

    form = PromotionForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit_new.data:
                if Promotion.query.filter_by(name=form.name.data).first():
                    flash('Такая акция уже существует! Выберите другое имя.', 'error')
                elif form.end.data < datetime.date(datetime.now()):
                    flash('Дата окончания акции не может быть раньше сегодня', 'error')
                else:
                    promo = Promotion()
                    form.populate_obj(promo)
                    db.session.add(promo)
                    db.session.commit()
                    flash(f'Категория {promo.name} добавлена успешно! 🚀')
                    promotions_all.append(promo)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('./admin/promotions.html',
                           title="Категории",
                           promotions=promotions_all,
                           form=form,
                           today=datetime.now())


def delete_images(img_path: str | None):
    full_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
    thumb_folder = os.path.join(full_folder, 'thumbs')

    if img_path:
        if os.path.isfile(file := os.path.join(full_folder, img_path)):
            os.remove(file)
        if os.path.isfile(file := os.path.join(thumb_folder, img_path)):
            os.remove(file)


def replace_image(data, img_path: str | None, prefix: str = 'img') -> str:
    filename = ".".join([
        prefix,
        str(datetime.timestamp(datetime.now())),
        'png'
    ])

    # Folder configs
    full_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
    thumb_folder = os.path.join(full_folder, 'thumbs')
    os.makedirs(full_folder, exist_ok=True)
    os.makedirs(thumb_folder, exist_ok=True)

    # Delete old images
    delete_images(img_path)

    def calculate_size(img: Image, a: int) -> tuple:
        width, height = img.size
        kt = max(width / a, height / a)

        return int(width / kt), int(height / kt)

    # Resize uploaded image and make thumbnail
    with Image.open(data) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)

        full = img.resize(calculate_size(img, 800), Image.Resampling.LANCZOS)
        full.save(os.path.join(full_folder, filename), 'PNG', compress_level=5, quality=90)
        thumb = img.resize(calculate_size(img, 400), Image.Resampling.LANCZOS)
        thumb.save(os.path.join(thumb_folder, filename), 'PNG', compress_level=5, quality=90)

    return filename


@app.route("/dash/promotions/<string:name>", methods=["GET", "POST"])
def promotion(name):
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    promo = Promotion.query.filter_by(name=name).first()
    if not promotion:
        return redirect(url_for('promotions'))
    form = PromotionForm(obj=promo)

    if request.method == "POST":
        if form.validate_on_submit():
            target_obj = Promotion.query.filter_by(name=form.name.data).first()

            if form.submit_save.data:
                if not target_obj or promo.id == target_obj.id:
                    if form.end.data < datetime.date(datetime.now()):
                        flash(f'Промоакция {form.name.data} завершена!', 'error')
                    if form.image.data:
                        # Set image name in object
                        form.image_path.data = replace_image(form.image.data, target_obj.image_path, 'promo')

                    form.populate_obj(promo)
                    db.session.commit()
                    flash(f'Промоакция [{promo.name}] сохранена! 😊')
                    return redirect(url_for('promotions'))
                else:
                    print("error_save:", target_obj)
                    flash(f'Промоакция {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('promotion.html',
                                    title="Редактирование промоакции",
                                    form=form)
            if form.submit_cancel.data:
                return redirect(url_for('promotions'))
    return render_template('./admin/promotion.html',
                           title=f"Промоакция {name}",
                           form=form)


def create_object(form, target):
    pass


@app.route("/dash/products", methods=["GET", "POST"])
def products():
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    produtcs_all = Product.query.order_by(Product.name).all()

    for product in produtcs_all:
        if current_cat := Category.query.filter_by(id=product.category_id).first():
            product.category = current_cat.name
        else:
            product.category = '---'

        if current_promo := Promotion.query.filter_by(id=product.promo_id).first():
            product.promo = current_promo.name
        else:
            product.promo = '---'

    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    form.promo_id.choices = [(0, 'Нет')] + [(p.id, p.name) for p in Promotion.query.all()]

    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit_new.data:
                if Product.query.filter_by(name=form.name.data).first():
                    flash('Такой продукт уже существует! Выберите другое имя.', 'error')
                else:
                    product = Product()
                    if form.image.data:
                        form.image_path.data = replace_image(
                            data=form.image.data,
                            img_path=form.image_path.data,
                            prefix='product')

                    form.populate_obj(product)
                    db.session.add(product)
                    db.session.commit()
                    flash(f'Продукт {product.name} добавлен успешно! 🚀')
                    produtcs_all.append(product)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('./admin/products.html',
                           title="Товары и услуги",
                           products=produtcs_all,
                           form=form)


@app.route("/dash/products/<string:name>", methods=["GET", "POST"])
def product(name):
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    product = Product.query.filter_by(name=name).first()
    if not product:
        return redirect(url_for('products'))
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    form.promo_id.choices = [(0, 'Нет')] + [(p.id, p.name) for p in Promotion.query.all()]

    form.custom_fields = Category.query.filter_by(id=product.category_id).first().fields
    saved_data = form.custom_fields_data.data
    print(saved_data, type(saved_data))
    
    if request.method == "POST":
        if form.validate_on_submit():
            target_obj = Product.query.filter_by(name=form.name.data).first()
            print(target_obj)
            if form.submit_save.data:
                if not target_obj or product.id == target_obj.id:
                    if form.image.data:
                        # Set image name in object
                        form.image_path.data = replace_image(
                            data=form.image.data,
                            img_path=target_obj.image_path,
                            prefix='product')
                    new_data = {field.id: request.form.get(field.name) for field in form.custom_fields}
                    form.custom_fields_data.data = new_data
                    print(new_data, form.custom_fields_data.data)
                    form.populate_obj(product)
                    db.session.commit()
                    flash(f'Продукт [{product.name}] сохранена! 😊')
                    return redirect(url_for('products'))
                else:
                    print("error_save:", target_obj)
                    flash(f'Продукт {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('./admin/product.html',
                                    title="Редактирование продукта",
                                    form=form,
                                    saved_data=new_data,
                                    custom_fields=custom_fields)
            if form.submit_cancel.data:
                return redirect(url_for('products'))

            if form.submit_delete.data:
                delete_images(product.image_path)
                db.session.delete(product)
                db.session.commit()

                flash(f'Продукт [{product.name}] удален')
                return redirect(url_for('products'))

    return render_template('./admin/product.html',
                           title=f"Продукт {name}",
                           form=form,
                           saved_data=saved_data,
                           custom_fields=custom_fields)


@app.route("/dash/custom_fields", methods=["GET", "POST"])
def custom_fields():
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    custom_fields_all = CustomFields.query.order_by(CustomFields.name).all()
    for f in custom_fields_all:
        f.categories = [d.name for d in f.category.all()]
    form = CustomFieldsForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit_new.data:
                field_new = CustomFields()
                form.populate_obj(field_new)
                if not CustomFields.query.filter_by(name=form.name.data).first():
                    db.session.add(field_new)
                    db.session.commit()
                    flash(f'Свойство {field_new.name} добавлено успешно! 🚀')
                    custom_fields_all.append(field_new)
                else:
                    flash(f'Свойство  {field_new.name}  уже существует! Выберите другое имя.', 'error')
                    redirect(url_for("custom_fields"), code=301)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('./admin/custom_fields.html',
                           title="Пользовательские поля категорий",
                           all_fields=custom_fields_all,
                           form=form)


@app.route('/dash/custom_fields/<string:name>', methods=["GET", "POST"])
def custom_field(name):
    if not current_user.is_authenticated:
        return redirect(url_for('index'), 301)
    field = CustomFields.query.filter_by(name=name).first()

    if not field:
        return redirect(url_for('custom_fields'))
    form = CustomFieldsForm(obj=field)

    if request.method == "POST":
        if form.validate_on_submit():
            target_obj = CustomFields.query.filter_by(name=form.name.data).first()
            if form.submit_save.data:
                print("submit_save:", target_obj)
                if not target_obj or field.id == target_obj.id:
                    form.populate_obj(field)
                    db.session.commit()
                    flash(f'Свойтсво [{field.name}] сохранено! 😊')
                    return redirect(url_for('custom_fields'))
                else:
                    print("error_save:", target_obj)
                    flash(f'Свойство {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('custom_field.html',
                                    title="Редактирование свойства",
                                    form=form)
            if form.submit_cancel.data:
                return redirect(url_for('custom_fields'))
    
    return render_template('./admin/custom_field.html',
                           title=f"Категория {name}",
                           form=form)
