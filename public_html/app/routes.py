from flask import request, render_template
from . import app

@app.route('/', methods=['get'])
def index():
    return render_template('home.html', name='teskanevskaya')