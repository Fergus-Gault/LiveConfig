from flask import Flask, render_template
from livevars.core import manager

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/functions')
def functions():
    return render_template('functions.html')

@app.route('/classes')
def classes():
    return render_template('classes.html')



def run_web_interface():
    app.run('0.0.0.0', port=5000)

