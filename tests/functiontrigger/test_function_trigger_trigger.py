from liveconfig import trigger
from liveconfig.core import manager

@trigger
def trigger_test(values, num):
    print(f"Function triggered: {values}, {num}!")
    return True


def test_function_trigger_trigger_success():
    assert "trigger_test" in manager.function_triggers, "Function should be registered"
    
    result = manager.trigger_function_by_name("trigger_test", values="test", num=42)
    assert result is True, "Function should return True"

    print(manager.function_triggers["trigger_test"])


def test_function_trigger_trigger_no_args():
    assert "trigger_test" in manager.function_triggers, "Function should be registered"
    
    result = manager.trigger_function_by_name("trigger_test")
    assert result is None, "Function should return None when no args are provided"
    

def test_function_trigger_call_function_normally():
    assert "trigger_test" in manager.function_triggers, "Function should be registered"
    
    result = trigger_test(values="test", num=42)
    assert result is True, "Function should return True"

    print(manager.function_triggers["trigger_test"])