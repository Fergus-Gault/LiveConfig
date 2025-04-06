from livevars import liveclass, liveinstance
from livevars.core import manager

@liveclass
class ExampleClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
def test_manager_get_liveinstance_by_name():

    instance = liveinstance("instance_name")(ExampleClass("Fred", 19))

    assert "instance_name" in manager.live_instances, "Instance not registered in manager"
    assert instance in ExampleClass._instances, "Instance not registered in its class."

    instance_by_name = manager.get_live_instance_by_name("instance_name")
    assert instance_by_name is not None, "Instance should not be None"