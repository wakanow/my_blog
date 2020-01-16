from . import main
from flask import render_template


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/chart')
def showChart():
    return render_template('chart.html')