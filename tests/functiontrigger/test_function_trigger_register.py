from liveconfig import trigger
from liveconfig.core import manager


@trigger
def sample_function(name, age):
    print("Function triggered!")
    return True

def test_function_trigger_register():
    assert "sample_function" in manager.function_triggers, "Function should be registered"
    print(manager.function_triggers)