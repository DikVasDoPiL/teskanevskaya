from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

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
                if not Category.query.filter_by(name=form.name.data).first():
                    category = Category()
                    form.populate_obj(category)
                    print(
                        category.name,
                        category.description,
                        # category.parent_id,
                        # category.children,
                        category.active
                    )
                    db.session.add(category)
                    db.session.commit()
                    flash(f'Категория {category.name} добавлена успешно! 🚀')
                    categories_all.append(category)
                else:
                    flash('Категория с таким названием уже существует! Выберите другое имя.', 'error')
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
    category = Category.query.filter_by(name=name).first()
    if not category:
        return redirect(url_for('categories'))
    form = CategoryForm(obj=category)
    if category:
        print(category)

    if request.method == "POST":
        if form.validate_on_submit():
            print(category)
            if form.submit_save.data:
                if not Category.query.filter_by(name=form.name.data).first():
                    form.populate_obj(category)
                    db.session.commit()
                    flash(f'Категория [{category.name}] сохранена! 😊')
                else:
                    flash('Категория с таким названием уже существует! Выберите другое имя.', 'error')
                return redirect(url_for('categories'))
            if form.submit_cancel.data:
                return redirect(url_for('categories'))
        return render_template('category.html',
                               title=f"Категория {category.name}",
                               category=category,
                               form=form)
        # return redirect(url_for('category'))

    return render_template('category.html',
                           title=f"Категория {category.name}",
                           category=category,
                           form=form)


@login_required
@app.route("/dash/promotions", methods=["GET", "POST"])
def promotions():
    promotions_all = Promotion.query.order_by(Promotion.name).all()

    form = PromotionForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit_new.data:
                if Promotion.query.filter_by(name=form.name.data).first():
                    flash('Такая акция уже существует! Выберите другое имя.', 'error')
                else:
                    promo = Promotion()
                    form.populate_obj(promo)
                    print(
                        promo.name,
                        promo.description
                    )
                    db.session.add(promo)
                    db.session.commit()
                    flash(f'Категория {promo.name} добавлена успешно! 🚀')
                    promotions_all.append(promo)
        else:
            flash('Ошибка создания записи, заполните корректно поля формы', 'error')

    return render_template('promotions.html',
                           title="Категории",
                           promotions=promotions_all,
                           form=form)

@login_required
@app.route("/dash/promotions/<string:name>", methods=["GET", "POST"])
def promotion(name):
    promotion = Category.query.filter_by(name=name).first()
    if not promotion:
        return redirect(url_for('promotions'))
    form = PromotionForm(obj=promotion)
    if category:
        print(category)
    return render_template('promotions.html',
                           title="Промоакции",
                           promotion=promotion,
                           form=form)