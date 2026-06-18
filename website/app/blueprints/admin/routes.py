# Контроллеры и маршруты этого модуля
from datetime import datetime

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user

from app import db
from app.blueprints.admin import admin_bp
from app.blueprints.admin.forms import CategoryForm, CustomFieldsForm, PromotionForm, ProductForm
from app.blueprints.admin.functions import replace_image, delete_images
from app.models import Category, CustomFields, Promotion, Product


@admin_bp.route("/home", methods=["GET"])
@admin_bp.route("/", methods=["GET"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'), 301)
    return render_template('./admin/home.html',
                           title="Панель управления")


@admin_bp.route("custom_fields", methods=["GET", "POST"])
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
                    redirect(url_for("admin.custom_fields"), code=301)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('./admin/custom_fields.html',
                           title="Пользовательские поля категорий",
                           all_fields=custom_fields_all,
                           form=form)


@admin_bp.route('custom_fields/<string:name>', methods=["GET", "POST"])
def custom_field(name):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'), 301)
    field = CustomFields.query.filter_by(name=name).first()

    if not field:
        return redirect(url_for('admin.custom_fields'))
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
                    return redirect(url_for('admin.custom_fields'))
                else:
                    print("error_save:", target_obj)
                    flash(f'Свойство {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('./admin/custom_field.html',
                                    title="Редактирование свойства",
                                    form=form)
            if form.submit_cancel.data:
                return redirect(url_for('admin.custom_fields'))

    return render_template('./admin/custom_field.html',
                           title=f"Категория {name}",
                           form=form)


@admin_bp.route("/categories", methods=["GET", "POST"])
def categories():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'), 301)
    categories_all = Category.query.order_by(Category.name).all()
    form = CategoryForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit_new.data:
                cat_new = Category()
                form.populate_obj(cat_new)
                if Category.query.filter_by(name=form.name.data).first():
                    flash(f'Категория  {cat_new.name}  уже существует! Выберите другое имя.', 'error')
                    return redirect(url_for("admin.categories"), code=301)
                else:
                    db.session.add(cat_new)
                    db.session.commit()
                    flash(f'Категория {cat_new.name} добавлена успешно! 🚀')
                    # categories_all.append(cat_new)
                    return redirect(url_for('admin.category', name=cat_new.name), code=301)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('./admin/categories.html',
                           title="Категории",
                           categories=categories_all,
                           form=form)


@admin_bp.route('/categories/<string:name>', methods=["GET", "POST"])
def category(name):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'), 301)
    cat = Category.query.filter_by(name=name).first()
    available_fields = CustomFields.query.filter_by(active=True).all()
    selected_fields = cat.fields

    if not cat:
        return redirect(url_for('admin.categories'))

    form = CategoryForm(obj=cat)
    if request.method == "POST":

        if form.validate_on_submit():
            target_obj = Category.query.filter_by(name=form.name.data).first()

            if form.submit_save.data:
                updated_fields = CustomFields.query.filter(
                    CustomFields.name.in_(request.form.getlist('custom_field'))).all()

                if not target_obj or cat.id == target_obj.id:
                    if form.image.data:
                        # Set image name in object
                        form.image_path.data = replace_image(
                            data=form.image.data,
                            img_path=target_obj.image_path,
                            prefix='cat')

                    form.populate_obj(cat)
                    cat.fields = updated_fields
                    db.session.commit()
                    flash(f'Категория [{cat.name}] сохранена! 😊')
                    return redirect(url_for('admin.categories'))
                else:
                    print("error_save:", target_obj)
                    flash(f'Категория {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('./admin/category.html',
                                    title="Редактирование категории",
                                    form=form,
                                    available_fields=available_fields,
                                    selected_fields=selected_fields)
            if form.submit_cancel.data:
                return redirect(url_for('admin.categories'))
    return render_template('./admin/category.html',
                           title=f"Категория {name}",
                           form=form,
                           available_fields=available_fields,
                           selected_fields=selected_fields)


@admin_bp.route("/promotions", methods=["GET", "POST"])
def promotions():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'), 301)
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
                    # promotions_all.append(promo)
                    return redirect(url_for('admin.promotion', name=promo.name), code=301)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('./admin/promotions.html',
                           title="Категории",
                           promotions=promotions_all,
                           form=form,
                           today=datetime.now())


@admin_bp.route("/promotions/<string:name>", methods=["GET", "POST"])
def promotion(name):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'), 301)
    promo = Promotion.query.filter_by(name=name).first()
    if not promotion:
        return redirect(url_for('admin.promotions'))
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
                        form.image_path.data = replace_image(
                            data=form.image.data,
                            img_path=target_obj.image_path,
                            prefix='promo')

                    form.populate_obj(promo)
                    db.session.commit()
                    flash(f'Промоакция [{promo.name}] сохранена! 😊')
                    return redirect(url_for('admin.promotions'))
                else:
                    print("error_save:", target_obj)
                    flash(f'Промоакция {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('./admin/promotion.html',
                                    title="Редактирование промоакции",
                                    form=form)
            if form.submit_cancel.data:
                return redirect(url_for('admin.promotions'))
    return render_template('./admin/promotion.html',
                           title=f"Промоакция {name}",
                           form=form)


@admin_bp.route("/products", methods=["GET", "POST"])
def products():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))
    produtcs_all = Product.query.order_by(Product.name).all()

    # for product in produtcs_all:
    #     if current_cat := Category.query.filter_by(id=product.category_id).first():
    #         product.category.name = current_cat.name
    #     else:
    #         product.category.name = '---'

    #     if current_promo := Promotion.query.filter_by(id=product.promo_id).first():
    #         product.promo = current_promo.name
    #     else:
    #         product.promo = '---'

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
                    return redirect(url_for('admin.product', name=product.name), code=301)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('./admin/products.html',
                           title="Товары и услуги",
                           products=produtcs_all,
                           form=form)


@admin_bp.route("/products/<string:name>", methods=["GET", "POST"])
def product(name):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'), 301)

    product = Product.query.filter_by(name=name).first()
    if not product:
        return redirect(url_for('admin.products')) 

    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    form.promo_id.choices = [(0, 'Нет')] + [(p.id, p.name) for p in Promotion.query.all()]

    form.custom_fields = Category.query.filter_by(id=product.category_id).first().fields
    saved_data = form.custom_fields_data.data

    if request.method == "POST":
        if form.validate_on_submit():
            target_obj = Product.query.filter_by(name=form.name.data).first()

            if form.submit_save.data:
                new_data = {field.id: request.form.get(field.name) for field in form.custom_fields}

                if not target_obj or product.id == target_obj.id:
                    if form.image.data:
                        # Set image name in object
                        form.image_path.data = replace_image(
                            data=form.image.data,
                            img_path=target_obj.image_path,
                            prefix='product')

                    form.custom_fields_data.data = new_data
                    form.populate_obj(product)
                    db.session.commit()
                    flash(f'Продукт [{product.name}] сохранен! 😊')
                    return redirect(url_for('admin.products'))
                else:
                    flash(f'Продукт {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('./admin/product.html',
                                    title="Редактирование продукта",
                                    form=form,
                                    saved_data=new_data,
                                    custom_fields=custom_fields)
            if form.submit_cancel.data:
                return redirect(url_for('admin.products'))

            if form.submit_delete.data:
                delete_images(product.image_path)
                db.session.delete(product)
                db.session.commit()

                flash(f'Продукт [{product.name}] удален')
                return redirect(url_for('admin.products'))

    return render_template('./admin/product.html',
                           title=f"Продукт {name}",
                           form=form,
                           saved_data=saved_data,
                           custom_fields=custom_fields)