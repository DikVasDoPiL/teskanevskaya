from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    """Функция, которая выполняется в отдельном потоке."""
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body=None):
    """
    Главная функция для импорта в другие blueprints.
    """
    # Получаем реальный объект приложения из контекста
    app = current_app._get_current_object()
    
    # Создаем сообщение
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body

    # Запускаем отправку в фоновом потоке
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr