#Blueprint админки сайта
from flask import Blueprint

dash_bp = Blueprint('dash', __name__)

from app.admin import routes