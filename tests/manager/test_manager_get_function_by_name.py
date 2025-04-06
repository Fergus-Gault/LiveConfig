from livevars import livefunction
from livevars.core import manager

@livefunction
def add(a, b):
    return a + b

def test_manager_get_function_by_name():
    # Get the registered function in the manager (with full module path)
    registered_function = manager.get_live_function_by_name('tests.manager.test_manager_get_function_by_name.add')

    # Check if the function is registered
    assert registered_function is not None, "Function 'add' should be registered"

    # Check if the function name is correct
    assert registered_function.__name__ == 'add', "Function name should be 'add'"

    # Check if the function works as expected
    result = registered_function(2, 3)
    assert result == 5, f"Expected 5, got {result}"