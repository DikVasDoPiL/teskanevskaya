import os
import sys
sys.path.append('/home/c/ci08648/venv/lib/python3.10/site-packages/')

from app import app as application

application.config.from_object('config.ProdConfig')

import routes

if __name__ == "__main__":
    app.run()