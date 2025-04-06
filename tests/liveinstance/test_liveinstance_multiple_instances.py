from livevars import liveclass, liveinstance
from livevars.core import manager

@liveclass
class SampleClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
def test_liveinstance_multiple_instances():
    # Create multiple instances of SampleClass
    instance1 = liveinstance("sample_instance_1")(SampleClass("Alice", 30))
    instance2 = liveinstance("sample_instance_2")(SampleClass("Bob", 25))
    
    # Check if the instances are registered in the manager
    assert "sample_instance_1" in manager.live_instances, "Instance 1 not registered in manager."
    assert "sample_instance_2" in manager.live_instances, "Instance 2 not registered in manager."
    
    # Check if the instances are registered in their class
    assert instance1 in SampleClass._instances, "Instance 1 not registered in its class."
    assert instance2 in SampleClass._instances, "Instance 2 not registered in its class."
    
    # Check if the tracked attributes are correct for both instances
    tracked_attrs1 = instance1.get_tracked_attrs()
    tracked_attrs2 = instance2.get_tracked_attrs()
    
    assert "name" in tracked_attrs1 and "age" in tracked_attrs1, "Tracked attributes for instance 1 are incorrect."
    assert "name" in tracked_attrs2 and "age" in tracked_attrs2, "Tracked attributes for instance 2 are incorrect."
    
    # Check if the tracked attribute values are correct for both instances
    tracked_attrs_values1 = instance1.get_tracked_attrs_values()
    tracked_attrs_values2 = instance2.get_tracked_attrs_values()
    
    assert tracked_attrs_values1["name"] == "Alice" and tracked_attrs_values1["age"] == 30, "Tracked attribute values for instance 1 are incorrect."
    assert tracked_attrs_values2["name"] == "Bob" and tracked_attrs_values2["age"] == 25, "Tracked attribute values for instance 2 are incorrect."