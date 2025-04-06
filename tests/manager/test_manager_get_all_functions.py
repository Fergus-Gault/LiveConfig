from livevars.core import manager
from livevars import livefunction

@livefunction
def add(a, b):
    return a + b

@livefunction
def subtract(a, b):
    return a - b

def test_get_all_functions():
    # Get all live functions
    live_functions = manager.get_live_functions()
    print(live_functions)
    
    # Check if the function is registered
    assert f"{add.__module__}.{add.__name__}" in live_functions, "Function not registered"
    assert f"{subtract.__module__}.{subtract.__name__}" in live_functions, "Function not registered"
    
    # Check if the function is the same as the one registered
    assert live_functions[f"{add.__module__}.{add.__name__}"] == add, "Function reference mismatch"
    assert live_functions[f"{subtract.__module__}.{subtract.__name__}"] == subtract, "Function reference mismatch"