from liveconfig import liveclass, liveinstance
from liveconfig.core import manager

@liveclass
class SampleClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
def test_manager_get_live_instance_attr_by_name():
    instance = liveinstance("instance_attr_by_name")(SampleClass("Bob", 23))

    assert "instance_attr_by_name" in manager.live_instances, "Instance not registered in manager."

    assert instance in SampleClass._instances, "Instance not registered in its class."

    attr = manager.get_live_instance_attr_by_name("instance_attr_by_name", "name")

    assert attr == "Bob", "Instance attribute was not found"