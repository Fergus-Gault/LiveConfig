from liveconfig import livevar
from liveconfig.core import manager

def test_live_variable_update_value():
    """
    Test to ensure that the live variable value is updated correctly in the manager.
    """
    variable = livevar("test_variable")(42)
    
    # Check if the variable is registered in the manager
    assert "test_variable" in manager.live_variables, "Live variable not registered in manager."
    
    # Check if the variable value is correct
    assert manager.get_live_variable_by_name("test_variable") == 42, "Live variable value is incorrect."
    assert variable == 42, "Live variable value is incorrect."

    # Update the live variable value
    manager.set_live_variable_by_name("test_variable","100")

    # Check if the variable value is updated correctly
    assert manager.get_live_variable_by_name("test_variable") == 100, "Live variable value is incorrect."