from LiveConfig.core import manager
from LiveConfig.decorators import liveclass, livefunction

@liveclass
class SampleClass:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def method(self, c: int) -> int:
        return self.a + self.b + c
    

def test_manager_liveclass_one_class():
    # Check if the class is registered
    assert "SampleClass" in manager.live_classes, "SampleClass should be registered"
    
    # Check if the class has the expected attributes
    test_instance = SampleClass(1, 2)
    assert hasattr(test_instance, "a"), "SampleClass instance should have attribute 'a'"
    assert hasattr(test_instance, "b"), "SampleClass instance should have attribute 'b'"
    
    # Check if the method works as expected
    result = test_instance.method(3)
    assert result == 6, f"Expected 6, got {result}"
    
