from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login


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


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)

    # Внешний ключ на саму себя для родителя
    # parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Связи: дети (один-ко-многим) и родитель (многие-к-одному)
    # children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]),
    #                            lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'


class Promotion(db.Model):
    __tablename__ = 'promotions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    start = db.Column(db.DateTime, default=datetime.now, nullable=False)
    end = db.Column(db.DateTime, default=True, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Promotion {self.name} from {self.start} to {self.end}>'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=True)
    power = db.Column(db.Float, nullable=True)  # потребляемая электрическая мощность, кВт
    btu = db.Column(db.Integer, nullable=True)  # холодопроизводительность, BTU
    cop = db.Column(db.Float, nullable=True)  # коэффициент преобразования - теплоэффективность, безразмерное
    type = db.Column(db.String(64), nullable=False)
    visible = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    promo_id = db.Column(db.Integer, db.ForeignKey('promotions.id'), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'
