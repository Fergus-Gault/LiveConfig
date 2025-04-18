from liveconfig import livevar
from liveconfig.core import manager


def test_live_var_registers():
    """
    Test to ensure that the live variable is registered correctly in the manager.
    """
    variable = livevar("test_variable")(42)
    # Check if the variable is registered in the manager
    assert "test_variable" in manager.live_variables, "Live variable not registered in manager."
    
    # Check if the variable value is correct
    assert manager.live_variables["test_variable"] == 42, "Live variable value is incorrect."
    assert variable == 42, "Live variable value is incorrect."


    manager.live_variables["test_variable"] = 100

    # Check if the variable value is updated correctly
    assert manager.live_variables["test_variable"] == 100, "Live variable value is incorrect."