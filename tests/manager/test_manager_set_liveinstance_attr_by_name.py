from LiveConfig import liveclass, liveinstance
from LiveConfig.core import manager

@liveclass
class ExampleClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
def test_manager_set_liveinstance_attr_by_name():

    instance = liveinstance("set_attr_example")(ExampleClass("Bob", 25))

    assert "set_attr_example" in manager.live_instances, "Instance was not registered"

    assert manager.get_live_instance_attr_by_name("set_attr_example", "name") == "Bob", "Did not get attr"

    manager.set_live_instance_attr_by_name("set_attr_example", "name", "Steve")

    assert manager.get_live_instance_attr_by_name("set_attr_example", "name") == "Steve", "Attr was not changed"