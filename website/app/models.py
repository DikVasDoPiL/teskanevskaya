from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from app.extentions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(256))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Реализация пользовательских коллекций полей свойтсв для категорий
custom_field_category = db.Table('custom_field_category',
    db.Column('custom_field_id', db.Integer, db.ForeignKey('customfields.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
    )


class CustomFields(db.Model):
    __tablename__ = 'customfields'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Fileds {self.id}: {self.name}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)
    fields = db.relationship('CustomFields', secondary=custom_field_category, backref=db.backref('category', lazy='dynamic'))
    image_path = db.Column(db.String(255), nullable=True)
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.id}: {self.name}>'
    


class Promotion(db.Model):
    __tablename__ = 'promotions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    start = db.Column(db.DateTime, default=datetime.now, nullable=False)
    end = db.Column(db.DateTime, default=True, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    products = db.relationship('Product', backref='promotion', lazy=True)

    def __repr__(self):
        return f'<Promotion {self.id}: {self.name} from {self.start} to {self.end}>'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=True)
    visible = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    promo_id = db.Column(db.Integer, db.ForeignKey('promotions.id'), nullable=True)
    custom_fields_data = db.Column(db.JSON, nullable=True)
    orders = db.relationship('Order', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    usercomment = db.Column(db.Text, nullable=True)
    installation = db.Column(db.Boolean, default=False)
    # cost = db.Column(db.Float, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)


    def __repr__(self):
        return f'<Order {self.username}: {self.cost}>'