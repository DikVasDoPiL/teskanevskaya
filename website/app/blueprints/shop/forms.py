from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


class FormButtons:
    submit_new = SubmitField('Создать заказ')
    submit_cancel = SubmitField('Отмена')


class OrderForm(FlaskForm):
    username = StringField('Ваше имя', validators=[DataRequired(), Length(min=2, max=64)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=20)])
    installation = BooleanField('Выездной монтаж', default=True)
    address = TextAreaField('Адрес доставки')
    description = TextAreaField('Комментарий к заказу')
    product_id = SelectField('Товар', validators=[DataRequired()],
                              coerce=int)

