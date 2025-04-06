from livevars import start_interface, liveclass, liveinstance


@liveclass
class ExampleClass:
    def __init__(self, a : int, b : int):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b
    

example_instance = liveinstance("example_instance")(ExampleClass(10, 5))


start_interface("web")