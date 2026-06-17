import json

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, SubmitField, IntegerField, StringField, BooleanField, DateField, FileField, \
    DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Optional, NumberRange
from wtforms.widgets import DateInput

DATA_REQUIRED_MESSAGE = "Необходимо заполнить"


class JsonField(TextAreaField):
    """Кастомное поле WTForms для автоматической работы с JSON."""

    def _value(self):
        # Превращает Python dict/list из базы данных в красивую строку для HTML
        if self.data is not None:
            return json.dumps(self.data, indent=4, ensure_ascii=False)
        return ''

    def process_formdata(self, valuelist):
        # Принимает строку из HTML-формы и превращает её обратно в Python dict/list
        if valuelist and valuelist[0].strip():
            try:
                self.data = json.loads(valuelist[0])
            except ValueError:
                self.data = None
                raise ValidationError('Некорректный синтаксис JSON!')
        else:
            self.data = {}  # Или None, если поле может быть пустым


class FormButtons:
    submit_new = SubmitField('Создать')
    submit_save = SubmitField('Сохранить')
    submit_cancel = SubmitField('Отмена')


class CustomFieldsForm(FlaskForm, FormButtons):
    id = IntegerField()
    name = StringField('Название', validators=[DataRequired(DATA_REQUIRED_MESSAGE), Length(min=3, max=64)])
    active = BooleanField('Активно', default=True)


class CategoryForm(FlaskForm, FormButtons):
    id = IntegerField()
    name = StringField('Название', validators=[DataRequired(DATA_REQUIRED_MESSAGE), Length(min=3, max=64)])
    description = TextAreaField('Описание', validators=[
        Optional(),
        Length(max=500, message='Максимум 500 символов')
    ])
    active = BooleanField('Активно', default=True)
    image_path = StringField('Изображение', validators=[
        Optional(),
        Length(max=200, message='Максимум 200 символов')
    ])
    image = FileField('Изображение', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], "Только изображения jpg, png, jpeg!")
    ])


class PromotionForm(FlaskForm, FormButtons):
    id = IntegerField()
    submit_end = SubmitField('Завершить')

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


class ProductForm(FlaskForm, FormButtons):
    submit_delete = SubmitField('Удалить')

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
    price = DecimalField('Цена', validators=[
        Optional(),
        NumberRange(min=0, message='Стоимость не может быть отрицательной')
    ],
        render_kw={'step': '0.01', 'class': 'form-control'}
    )
    image = FileField('Изображение', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], "Только изображения jpg, png, jpeg!")
    ])

    visible = BooleanField('В наличии', default=True)

    custom_fields_data = JsonField('Описание', validators=[Optional()])

    category_id = SelectField('Категория', validators=[DataRequired()],
                              coerce=int)  # В view: form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    promo_id = SelectField('Промо (опционально)', validators=[Optional()],
                           choices=[(0, 'Нет')],
                           coerce=int)  # В view: добавь [(p.id, p.name) for p in Promotion.query.all()] + [(0, 'Нет')]