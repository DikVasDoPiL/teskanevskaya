# Контроллеры и маршруты этого модуля
from flask import render_template

from . import auth_bp as app

@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect('/dash')
    form = LoginForm()
    return render_template('./admin/login.html', name='login', form=form, title="Авторизация")
