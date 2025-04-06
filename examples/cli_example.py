"""
A simple example of the CLI.
Example usage:
    >>> test_class_instance name Bob
    >>> test_class_instance a 10
    >>> save
"""

from livevars import liveclass, liveinstance, start_interface, FileHandler
import time

FileHandler("./examples/")

@liveclass
class CliTestClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.name = "Steve"

    def print_attr(self):
        print(f"a = {self.a}, b = {self.b}")


if __name__ == "__main__":
    test_class_instance = liveinstance("test_class_instance")(CliTestClass(1,2))
    start_interface("cli")
    while True:
        test_class_instance.print_attr()
        time.sleep(1)
