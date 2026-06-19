from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.widgets import DateInput


class FormButtons:
    submit_send = SubmitField('Создать заказ')
    submit_cancel = SubmitField('Отмена')


class OrderForm(FlaskForm, FormButtons):
    username = StringField('Ваше имя', validators=[DataRequired(), Length(min=2, max=64)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=20)])
    installation = BooleanField('Запросить установку или подключение', default=True)
    delivery = BooleanField('Запросить доставку по адресу', default=True)
    address = TextAreaField('Адрес доставки')
    usercomment = TextAreaField('Комментарий к заказу')
    product_id = IntegerField('Товар', validators=[DataRequired()])
    closed = BooleanField('Заказ исполнен', default=False)
    created_at = DateField('Заказ создан', format='%Y-%m-%d', widget=DateInput(), validators=[Optional()])
    updated_at = DateField('Статус заказа обновлен', format='%Y-%m-%d', widget=DateInput(), validators=[Optional()])

