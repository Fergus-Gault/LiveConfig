from liveconfig import livevar, LiveConfig
LiveConfig("./tests/livevariable/test_live_variable_reload.json")
from liveconfig.core import manager

def test_live_variable_reload():
    """
    Test if the live variable reloads correctly.
    """
    # Define a variable with a specific name and value
    test_var = livevar("test_var")(42)

    # Save the current state of the variables to a file
    manager.file_handler.save()

    assert manager.get_live_variable_by_name("test_var") == 42, "Live variable was not saved correctly."
    assert test_var == 42, "Variable was not saved correctly."

    # Change the value of the variable
    manager.set_live_variable_by_name("test_var", 100)

    # Check if the variable has been changed correctly
    assert manager.get_live_variable_by_name("test_var") == 100, "Live variable was not changed correctly."
    assert test_var == 100, "Variable was not changed correctly."

    # Reload the variables from the file
    manager.file_handler.reload()

    # Check if the variable has been reloaded correctly
    assert manager.get_live_variable_by_name("test_var") == 42, "Variable was not reloaded correctly."
    assert test_var == 42, "Variable was not reloaded correctly."
