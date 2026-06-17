# Конфигурационные настройки проекта
import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.abspath(os.path.dirname(CURRENT_DIR))

def get_env_bool(var_name, default=False):
    value = os.environ.get(var_name)
    if value is None:
        return default
    return value.lower() in ('true', '1', 't', 'yes', 'y')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    DEBUG = get_env_bool('DEBUG')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    # Отключаем ненужную систему оповещений SQLAlchemy для экономии памяти
    SQLALCHEMY_TRACK_MODIFICATIONS = get_env_bool('DEBUG')
    UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

