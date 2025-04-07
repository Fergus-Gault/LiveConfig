from LiveConfig import liveclass, liveinstance
from LiveConfig.core import manager

@liveclass
class SampleClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
def test_liveinstance_modify_attr():
    # Create an instance of SampleClass
    instance = liveinstance("example_instance")(SampleClass("Alice", 30))
    
    # Modify an attribute of the instance
    instance.name = "Bob"
    
    # Check if the instance is registered in the manager
    assert "example_instance" in manager.live_instances, "Instance not registered in manager."
    
    # Check if the instance is registered in its class
    assert instance in SampleClass._instances, "Instance not registered in its class."
    
    # Check if the tracked attributes are correct after modification
    tracked_attrs = instance.get_tracked_attrs()
    assert "name" in tracked_attrs and "age" in tracked_attrs, "Tracked attributes are incorrect."
    
    # Check if the tracked attribute values are correct after modification
    tracked_attrs_values = instance.get_tracked_attrs_values()
    assert tracked_attrs_values["name"] == "Bob" and tracked_attrs_values["age"] == 30, "Tracked attribute values are incorrect."