from livevars import liveclass, liveinstance, FileHandler
from livevars.core import manager

FileHandler("./tests/filehandler/")
@liveclass
class SampleClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
def test_filehandler_added_to_manager():
    instance = liveinstance("file_handling_instance")(SampleClass("Steve", 23))
    assert "file_handling_instance" in manager.live_instances, "Instance not registered in manager."
    assert manager.file_handler is not None, "File handler not added to manager"
