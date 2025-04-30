from flask import Flask, render_template, request
from liveconfig.core import manager
import threading

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

@app.route('/')
def index():
    """Index route"""
    return render_template('index.html')


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
    
    # Use loaded_values if available, otherwise serialize current state
    if manager.file_handler.loaded_values \
        and "live_instances" in manager.file_handler.loaded_values:
        loaded_instances = manager.file_handler.loaded_values["live_instances"]
        all_instances = manager.file_handler.serialize_instances()["live_instances"]
        # Merge loaded instances with all instances to get the latest state
        instances = {**loaded_instances, **all_instances}
    else:
        instances = manager.file_handler.serialize_instances()["live_instances"]
        
    return render_template('classes.html', class_instances=instances)

@app.route('/variables', methods=['GET', 'POST'])
def variables():
    """
    Render all of the live variables with their values.
    Update values on form submission.
    """
    if request.method == 'POST':
        variable_name = request.form.get('name')
        value = request.form.get('value')
        manager.set_live_variable_by_name(variable_name, value)
    
    # Use loaded_values if available, otherwise serialize current state
    if manager.file_handler.loaded_values and "live_variables" in manager.file_handler.loaded_values:
        variables = manager.file_handler.loaded_values["live_variables"]
    else:
        variables = manager.file_handler.serialize_variables()["live_variables"]
        
    return render_template('variables.html', live_variables=variables)

@app.route('/triggers', methods=['GET', 'POST'])
def triggers():
    """
    Render all of the function triggers with their kwargs if they have any.
    Run the function on form submission.
    """
    if request.method == 'POST':
        function_name = request.form.get('function_name')
        kwargs = {param_name: request.form.get(f'arg[{param_name}]') 
                  for param_name in manager.get_function_args_by_name(function_name)}
        manager.trigger_function_by_name(function_name, **kwargs)
    return render_template('triggers.html', function_triggers=manager.function_triggers)

@app.route('/save', methods=['POST'])
def save():
    """Save the current variables."""
    manager.file_handler.save()
    return '', 204

@app.route('/reload', methods=['POST'])
def reload():
    """Reload the current variables."""
    success = manager.file_handler.reload()
    return {'success': success}, 200 if success else 500



def run_web_interface(port):
    """Run the web interface on its own thread, uses port 5000 by default."""
    thread = threading.Thread(target=app.run, args=('0.0.0.0',), kwargs={'port': port})
    thread.daemon = True
    thread.start()

