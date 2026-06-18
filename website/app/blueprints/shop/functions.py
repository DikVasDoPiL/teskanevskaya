from flask_mail import Message
from app import mail
from flask import current_app


def send_message(body_text, mail_subject='Онлайн-заказ с teskanevskaya.ru'):
    # Получатель, тема и ваше готовое тело сообщения
    recipient_email = "firelli@li.ru"


    msg = Message(subject=mail_subject, 
                  sender=current_app.config['MAIL_USERNAME'], 
                  recipients=[recipient_email])
    
    msg.body = body_text 
    
    print(current_app.config['MAIL_SERVER'])

    try:
        mail.send(msg)
        return "Сообщение успешно отправлено!"
    except Exception as e:
        return f"Ошибка при отправке: {e}"