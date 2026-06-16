# Веб-формы авторизации
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

DATA_REQUIRED_MESSAGE = "Необходимо заполнить"


class LoginForm(FlaskForm):
    username = StringField('Пользователь', validators=[
        DataRequired(DATA_REQUIRED_MESSAGE)
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(DATA_REQUIRED_MESSAGE)
    ])
    submit = SubmitField('Войти')