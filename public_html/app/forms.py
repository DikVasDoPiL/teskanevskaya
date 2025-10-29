from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length
from wtforms_sqlalchemy.fields import QuerySelectField

from .models import Category

DATA_REQUIRED_MESSAGE = "Необходимо заполнить"


class LoginForm(FlaskForm):
    username = StringField('Пользователь', validators=[
        DataRequired(DATA_REQUIRED_MESSAGE)
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(DATA_REQUIRED_MESSAGE)
    ])
    submit = SubmitField('Войти')


class CategoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(DATA_REQUIRED_MESSAGE), Length(min=1, max=64)])
    description = TextAreaField('Описание', validators=[Optional()])
    active = BooleanField('Активна', default=True)
    # QuerySelectField для parent_id: выбор из активных категорий (исключая текущую)
    parent = QuerySelectField(
        label='Родительская категория',
        query_factory=lambda: Category.query.filter_by(active=True),
        get_label='name',
        get_pk=lambda obj: obj.id,
        allow_blank=True,  # Опционально: без родителя
        blank_text='- Нет родителя -'
    )
    submit_new = SubmitField('Создать')
    submit_save = SubmitField('Сохранить')
    submit_delete = SubmitField('Удалить')