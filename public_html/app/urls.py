from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from . import app, db
from .forms import LoginForm
from .models import User, Category


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


@app.route("/dash/categories", methods=["GET"])
def list_categories():
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    query = Category.query
    if active_only:
        query = query.filter_by(active=True)
    categories = query.order_by(Category.name).all()
    for cat in categories:
        cat.children

    return render_template('categories.html',
                          title="Категории",
                          categories=categories,
                          active_only=active_only)


