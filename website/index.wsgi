import os 
import sys 
from datetime import timedelta
sys.path.append('/home/c/ci08648/venv/lib/python3.10/site-packages/') 
sys.path.insert(0, os.path.dirname(__file__))   #######
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))#########


from app import create_app

app = create_app()

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        # Принудительно очищаем префикс скрипта, чтобы index.wsgi исчез из ссылок
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)
 
app.config['DEBUG']=False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
app.config['SESSION_COOKIE_NAME'] = 'teskanevskaya_session'
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
) 


application = app 

if __name__ == "__main__": 
  app.run()
