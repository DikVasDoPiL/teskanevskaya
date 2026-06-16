# Конфигурационные настройки проекта
import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.abspath(os.path.dirname(CURRENT_DIR))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    DEBUG = bool(os.environ.get('DEBUG')) or False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    # Отключаем ненужную систему оповещений SQLAlchemy для экономии памяти
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

