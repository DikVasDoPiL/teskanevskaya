

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from wtforms.widgets import DateInput

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
    id = IntegerField()
    name = StringField('Название', validators=[DataRequired(DATA_REQUIRED_MESSAGE), Length(min=3, max=64)])
    description = TextAreaField('Описание', validators=[
        Optional(),
        Length(max=500, message='Максимум 500 символов')
    ])
    active = BooleanField('Активно', default=True)
    # QuerySelectField для parent_id: выбор из активных категорий (исключая текущую)
    # parent = QuerySelectField(
    #     label='Родительская категория',
    #     query_factory=lambda: Category.query.filter_by(active=True),
    #     get_label='name',
    #     get_pk=lambda obj: obj.id,
    #     allow_blank=True,  # Опционально: без родителя
    #     blank_text='- Нет родителя -'
    # )
    submit_new = SubmitField('Создать')
    submit_save = SubmitField('Сохранить')
    submit_cancel = SubmitField('Отмена')
    submit_end = SubmitField('Завершить')


class PromotionForm(FlaskForm):
    id = IntegerField()

    name = StringField('Название', validators=[
        DataRequired(message='Название обязательно'),
        Length(min=3, max=64, message='Максимум 64 символа')
    ])
    description = TextAreaField('Описание', validators=[
        Optional(),
        Length(max=500, message='Максимум 500 символов')
    ])
    start = DateField('Начало', format='%Y-%m-%d', widget=DateInput(), validators=[
        DataRequired(message='Дата начала обязательно'),
        Optional()
    ])
    end = DateField('Конец', format='%Y-%m-%d', widget=DateInput(), validators=[
        DataRequired(message='Дата окончания обязательно'),
        Optional()
    ])
    image_path = FileField('Изображение', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'svg'], "Только изображения jpg, png, jpeg, svg!")
    ])

    submit_new = SubmitField('Создать')
    submit_save = SubmitField('Сохранить')
    submit_cancel = SubmitField('Отмена')
    submit_end = SubmitField('Завершить')

