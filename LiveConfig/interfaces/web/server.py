from flask import Flask, render_template, request
from LiveConfig.core import manager
import threading

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/functions')
def functions():
    return render_template('functions.html')

@app.route('/classes', methods=['GET', 'POST'])
def classes():
    """
    Render all of the instances of classes with their attributes.
    Update attributes on form submission.
    """
    if request.method == 'POST':
        instance_name = request.form.get('instance_name')
        attribute = request.form.get('attribute')
        value = request.form.get('value')
        manager.set_live_instance_attr_by_name(instance_name, attribute, value)
    return render_template('classes.html', class_instances=manager.serialize_instances()["live_instances"])


@app.route('/save', methods=['POST'])
def save():
    """
    Save the current variables.
    """
    manager.file_handler.save()
    return '', 204


def run_web_interface(port):
    """
    Run the web interface on its own thread, uses port 5000 by default.
    """
    thread = threading.Thread(target=app.run, args=('0.0.0.0',), kwargs={'port': port})
    thread.daemon = True
    thread.start()

