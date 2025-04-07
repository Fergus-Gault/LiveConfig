from liveconfig import liveclass, liveinstance
from liveconfig.core import manager


@liveclass
class SampleClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
def test_manager_liveinstance_modify_attry():
    instance = liveinstance("modify_example")(SampleClass("Bob", 53))

    # Check if the instance is registered in the manager
    assert "modify_example" in manager.live_instances, "Instance not registered in manager."

    # Check if the instance is registered in its class
    assert instance in SampleClass._instances, "Instance not registered in its class."
    
    # Check if the tracked attributes are correct after modification
    tracked_attrs = instance.get_tracked_attrs()
    assert "name" in tracked_attrs and "age" in tracked_attrs, "Tracked attributes are incorrect."
    
    # Check if the tracked attribute values are correct after modification
    tracked_attrs_values = instance.get_tracked_attrs_values()
    assert tracked_attrs_values["name"] == "Bob" and tracked_attrs_values["age"] == 53, "Tracked attribute values are incorrect."

    tracked_attrs_values["name"] = "James"
    assert tracked_attrs_values["name"] == "James" and tracked_attrs_values["age"] == 53, "Tracked attribute values should have changed."
