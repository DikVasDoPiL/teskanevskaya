from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from . import app, db
from .forms import LoginForm
from .models import User


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