from flask import Flask
from livevars.core import manager

app = Flask(__name__)

@app.route('/')
def index():
    return f"{manager.live_functions}"



def run_web_interface():
    app.run('0.0.0.0', port=5000)

