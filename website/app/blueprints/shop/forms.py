from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


class FormButtons:
    submit_send = SubmitField('Создать заказ')
    submit_cancel = SubmitField('Отмена')


class OrderForm(FlaskForm, FormButtons):
    username = StringField('Ваше имя', validators=[DataRequired(), Length(min=2, max=64)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=20)])
    installation = BooleanField('Нужна установка', default=True)
    address = TextAreaField('Адрес доставки')
    usercomment = TextAreaField('Комментарий к заказу')
    product_id = SelectField('Товар', validators=[DataRequired()],
                              coerce=int)

