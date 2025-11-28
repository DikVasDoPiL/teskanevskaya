

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, IntegerField, \
    SelectField, FloatField, DecimalField
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
    image_path = StringField('Изображение', validators=[
        Length(max=200, message='Слишком длинное имя файла, Максимум 200 символов')
    ])
    image = FileField('Изображение', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], "Только изображения jpg, png, jpeg!")
    ])


    submit_new = SubmitField('Создать')
    submit_save = SubmitField('Сохранить')
    submit_cancel = SubmitField('Отмена')
    submit_end = SubmitField('Завершить')


class ProductForm(FlaskForm):
    name = StringField('Название', validators=[
        DataRequired(message='Название обязательно'),
        Length(max=64, message='Максимум 64 символа')
    ])
    description = TextAreaField('Описание', validators=[
        Optional(),
        Length(max=1000, message='Максимум 1000 символов')
    ])
    image_path = StringField('Изображение', validators=[
        Optional(),
        Length(max=200, message='Максимум 200 символов')
    ])
    price = DecimalField('Стоимость, руб', validators=[
        Optional(),
        NumberRange(min=0, message='Стоимость не может быть отрицательной')
    ],
        render_kw={'step': '0.01', 'class': 'form-control'}
    )
    image = FileField('Изображение', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], "Только изображения jpg, png, jpeg!")
    ])
    power = FloatField('Мощность (кВт)', validators=[
        Optional(),
        NumberRange(min=0, message='Мощность не может быть отрицательной')
    ])
    btu = IntegerField('BTU (холодопроизводительность)', validators=[
        Optional(),
        NumberRange(min=0, message='BTU не может быть отрицательной')
    ])
    cop = FloatField('COP (коэффициент эффективности)', validators=[
        Optional(),
        NumberRange(min=0, message='COP не может быть отрицательной')
    ])
    type = StringField('Тип', validators=[
        DataRequired(message='Тип обязателен'),
        Length(max=64, message='Максимум 64 символа')
    ])
    visible = BooleanField('В наличии', default=True)

    category_id = SelectField('Категория', validators=[DataRequired()],
                              coerce=int)  # В view: form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    promo_id = SelectField('Промо (опционально)', validators=[Optional()],
                           choices=[(0, 'Нет')],
                           coerce=int)  # В view: добавь [(p.id, p.name) for p in Promotion.query.all()] + [(0, 'Нет')]

    submit_new = SubmitField('Создать')
    submit_save = SubmitField('Сохранить')
    submit_cancel = SubmitField('Отмена')
    submit_delete = SubmitField('Удалить')
