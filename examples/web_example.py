from liveconfig import start_interface, liveclass, liveinstance
import time

start_interface("web")

@liveclass
class ExampleClass:
    def __init__(self, a : int, b : int):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b
    

example_instance = liveinstance("example_instance")(ExampleClass(10, 5))
another_instance = liveinstance("another_instance")(ExampleClass(17, 22))

while True:
    print(f"Example instance: {example_instance.add()}")
    print(f"Another instance: {another_instance.add()}")
    time.sleep(2)