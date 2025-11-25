import os
from datetime import datetime

from PIL import Image
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from . import app, db
from .forms import LoginForm, CategoryForm, PromotionForm
from .models import User, Category, Promotion


@app.route('/', methods=['get'])
def index():
    return render_template('home.html', name='teskanevskaya')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect('/dash')
    form = LoginForm()
    return render_template('login.html', name='login', form=form, title="Авторизация")


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
            return redirect('/dash')
        else:
            return render_template('login.html', title='Авторизация', form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
    return redirect(url_for('login_get'))


@app.route("/dash", methods=["GET"])
def dashboard():
    return render_template('dashboard.html', title="Панель управления")


# @app.route('/sitemap.xml')
# def serve_robots_sitemap():
#     return send_from_directory(app.root_path, 'sitemap.xml')


@login_required
@app.route("/dash/categories", methods=["GET", "POST"])
def categories():
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
                    categories_all.append(category)
                else:
                    flash(f'Категория  {cat_new.name}  уже существует! Выберите другое имя.', 'error')
                    redirect(url_for("categories"), code=301)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('categories.html',
                           title="Категории",
                           categories=categories_all,
                           form=form)


@login_required
@app.route('/dash/categories/<string:name>', methods=["GET", "POST"])
def category(name):
    cat = Category.query.filter_by(name=name).first()
    if not cat:
        return redirect(url_for('categories'))
    form = CategoryForm(obj=cat)

    if request.method == "POST":
        if form.validate_on_submit():
            target_obj = Category.query.filter_by(name=form.name.data).first()
            if form.submit_save.data:
                print("submit_save:", target_obj)
                if not target_obj or cat.id == target_obj.id:
                    form.populate_obj(cat)
                    db.session.commit()
                    flash(f'Категория [{cat.name}] сохранена! 😊')
                    return redirect(url_for('categories'))
                else:
                    print("error_save:", target_obj)
                    flash(f'Категория {target_obj.name} уже существует! Выберите другое имя.', 'error')
                    render_template('category.html',
                                    title="Редактирование категории",
                                    form=form)
            if form.submit_cancel.data:
                return redirect(url_for('categories'))
    return render_template('category.html',
                           title=f"Категория {name}",
                           form=form)


@login_required
@app.route("/dash/promotions", methods=["GET", "POST"])
def promotions():
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

    return render_template('promotions.html',
                           title="Категории",
                           promotions=promotions_all,
                           form=form,
                           today=datetime.now())


def replace_image(data, old_path: str) -> str:
    filename = ".".join([
        str(datetime.timestamp(datetime.now())),
        secure_filename(data.filename)
    ])

    # Folder configs
    full_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
    thumb_folder = os.path.join(full_folder, 'thumbs')
    os.makedirs(full_folder, exist_ok=True)
    os.makedirs(thumb_folder, exist_ok=True)

    # Delete old images
    if os.path.isfile(file := os.path.join(full_folder, old_path)):
        os.remove(file)
    if os.path.isfile(file := os.path.join(thumb_folder, old_path)):
        os.remove(file)

    def calculate_size(img: Image, a: int) -> tuple:
        width, height = img.size
        kt = max(width / a, height / a)

        return int(width / kt), int(height / kt)

    # Resize uploaded image and make thumbnail
    with Image.open(data) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)

        full = img.resize(calculate_size(img, 600), Image.Resampling.LANCZOS)
        full.save(os.path.join(full_folder, filename), 'PNG', compress_level=5)
        thumb = img.resize(calculate_size(img, 200), Image.Resampling.LANCZOS)
        thumb.save(os.path.join(thumb_folder, filename), 'PNG', compress_level=5)

    return filename


@login_required
@app.route("/dash/promotions/<string:name>", methods=["GET", "POST"])
def promotion(name):
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
                        form.image_path.data = replace_image(form.image.data, target_obj.image_path)

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
    return render_template('promotion.html',
                           title=f"Промоакция {name}",
                           form=form)
