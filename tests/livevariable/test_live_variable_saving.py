from liveconfig import livevar
from liveconfig.core import manager

import pytest

@pytest.fixture(autouse=True)
def reset_manager():
    manager.live_variables = {}


def test_live_variable_saving():
    """
    Test to ensure that the live variable is saved correctly in the manager.
    """
    variable = livevar("test_saving_variable")("Hello, World")
    another_variable = livevar("another_saving_variable")([1, 2, 3])
    
    # Check if the variable is registered in the manager
    assert "test_saving_variable" in manager.live_variables, "Live variable not registered in manager."
    assert "another_saving_variable" in manager.live_variables, "Another live variable not registered in manager."

    # Check if the variable value is correct
    assert manager.get_live_variable_by_name("test_saving_variable") == "Hello, World", "Live variable value is incorrect."
    assert variable == "Hello, World", "Live variable value is incorrect."
    assert manager.get_live_variable_by_name("another_saving_variable") == [1, 2, 3], "Another live variable value is incorrect."
    assert another_variable == [1, 2, 3], "Another live variable value is incorrect."
    
    manager.file_handler.save()
    