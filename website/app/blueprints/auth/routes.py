# Контроллеры и маршруты этого модуля
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, logout_user, login_user, login_required

from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import LoginForm
from app.models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        # однократно для создания пользователя
        # from werkzeug.security import generate_password_hash
        # print(username, generate_password_hash(password))

        # Проверяем пользователя и валидность хэша пароля
        if not user or not user.check_password(password):
            flash('Неверное имя пользователя или пароль.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash(f'Добро пожаловать, {user.username}!', 'success')
        return redirect(url_for('admin.home'))

    form = LoginForm()
    return render_template('./auth/login.html',
                           name='login',
                           form=form,
                           title="Авторизация")

@auth_bp.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.index'))





# Логика регистрации пользователя отложена за ненадобностью
# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#
#         # Проверка, существует ли пользователь
#         if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
#             flash('Пользователь с таким именем или email уже существует.', 'danger')
#             return redirect(url_for('auth.register'))
#
#         new_user = User(username=username, email=email)
#         new_user.set_password(password)  # Хэшируем пароль
#
#         db.session.add(new_user)
#         db.session.commit()
#
#         flash('Вы успешно зарегистрировались! Теперь можно войти.', 'success')
#         return redirect(url_for('auth.login'))
#
#     return render_template('auth/register.html')

