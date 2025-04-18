from liveconfig import liveclass, liveinstance
from liveconfig.core import manager

@liveclass
class SampleClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
def test_filehandler_added_to_manager():
    instance = liveinstance("file_saving_example")(SampleClass("Steve", 23))
    assert "file_saving_example" in manager.live_instances, "Instance not registered in manager."
    assert manager.file_handler is not None, "File handler not added to manager"

    success = manager.file_handler.save()

    assert success == True, "File did not save successfully"
