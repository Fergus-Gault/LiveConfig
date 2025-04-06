from livevars.decorators import livefunction
from livevars.core import manager


@livefunction
def example_function(a, b, c=3):
    return a + b + c


def test_livefunction_decorator():
    # Get the registered function in the manager (with full module path)
    registered_function = manager.live_functions.get('tests.manager.test_manager_livefunction_one_function.example_function')

    # Check if the function is registered
    assert registered_function is not None, "Function should be registered"

    assert registered_function.__name__ == 'example_function', "Function name should be 'example_function'"
    
