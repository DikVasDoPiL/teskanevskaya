import os
import sys
sys.path.append('/home/c/ci08648/venv/lib/python3.10/site-packages/')

from app import app

app.config['DEBUG']=False
application = app


import routes

if __name__ == "__main__":
    application.run()