from livevars import start_interface, livefunction


@livefunction
def add(a, b):
    """
    Add two numbers and return the result.
    """
    return a + b


start_interface("web")