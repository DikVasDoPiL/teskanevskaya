from flask import Blueprint

mail_bp = Blueprint('mail_bp', __name__)

# Импортируем services, чтобы они были доступны
from app.blueprints.mail import services