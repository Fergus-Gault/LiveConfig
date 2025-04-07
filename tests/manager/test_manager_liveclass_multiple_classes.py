from LiveConfig.core import manager
from LiveConfig.decorators import liveclass, livefunction

@liveclass
class SampleClass1:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def method(self, c: int) -> int:
        return self.a + self.b + c
    
@liveclass
class SampleClass2:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def method(self, z: int) -> int:
        return self.x * self.y * z
    
def test_manager_liveclass_multiple_classes():
    # Check if the classes are registered
    assert "SampleClass1" in manager.live_classes, "SampleClass1 should be registered"
    assert "SampleClass2" in manager.live_classes, "SampleClass2 should be registered"
    
    # Check if the classes have the expected attributes
    test_instance1 = SampleClass1(1, 2)
    assert hasattr(test_instance1, "a"), "SampleClass1 instance should have attribute 'a'"
    assert hasattr(test_instance1, "b"), "SampleClass1 instance should have attribute 'b'"
    
    test_instance2 = SampleClass2(3, 4)
    assert hasattr(test_instance2, "x"), "SampleClass2 instance should have attribute 'x'"
    assert hasattr(test_instance2, "y"), "SampleClass2 instance should have attribute 'y'"
    
    # Check if the methods work as expected
    result1 = test_instance1.method(3)
    assert result1 == 6, f"Expected 6 from SampleClass1, got {result1}"
    
    result2 = test_instance2.method(5)
    assert result2 == 60, f"Expected 60 from SampleClass2, got {result2}"