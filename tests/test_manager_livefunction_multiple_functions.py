from livevars.decorators import livefunction
from livevars.core import manager

@livefunction
def example_1(a, b, c=3):
    return a + b + c

@livefunction
def example_2(x, y, z=5):
    return x * y + z

def test_livefunction_decorator_multiple_functions():
    # Get the registered functions in the manager (with full module path)
    registered_function_1 = manager.live_functions.get('tests.test_manager_livefunction_multiple_functions.example_1')
    registered_function_2 = manager.live_functions.get('tests.test_manager_livefunction_multiple_functions.example_2')

    # Check if the functions are registered
    assert registered_function_1 is not None, "Function example_1 should be registered"
    assert registered_function_2 is not None, "Function example_2 should be registered"

    # Check if the function names are correct
    assert registered_function_1.__name__ == 'example_1', "Function name should be 'example_1'"
    assert registered_function_2.__name__ == 'example_2', "Function name should be 'example_2'"