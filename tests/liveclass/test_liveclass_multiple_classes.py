from liveconfig.decorators import liveclass

@liveclass
class testClass1:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_sum(self) -> int:
        return self.x + self.y
    
@liveclass
class testClass2:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def get_product(self) -> int:
        return self.a * self.b
    
def test_liveclass_multiple_classes():
    class1 = testClass1(1, 2)
    class2 = testClass2(3, 4)
    assert class1.get_sum() == 3, "Sum should be 3"
    print(class1.get_sum())  # Output: 3
    assert class2.get_product() == 12, "Product should be 12"
    print(class2.get_product())  # Output: 12
    assert class1.get_tracked_attrs() == {'x', 'y'}, "Tracked attributes should be x and y"
    print(class1.get_tracked_attrs())  # Output: {'x', 'y'}
    assert class2.get_tracked_attrs() == {'a', 'b'}, "Tracked attributes should be a and b"
    print(class2.get_tracked_attrs())  # Output: {'a', 'b'}
    class1.z = 3
    assert class1.get_tracked_attrs() == {'x', 'y', 'z'}, "Tracked attributes should be x, y, and z"
    print(class1.get_tracked_attrs())  # Output: {'x', 'y', 'z'}
    class2.c = 5
    assert class2.get_tracked_attrs() == {'a', 'b', 'c'}, "Tracked attributes should be a, b, and c"
    print(class2.get_tracked_attrs())  # Output: {'a', 'b', 'c'}
    class1.x = 5
    assert class1.get_tracked_attrs_values() == {'x': 5, 'y': 2, 'z': 3}, "Tracked attributes values should be updated"
    print(class1.get_tracked_attrs_values()) # Output: {'x': 5, 'y': 2, 'z': 3}
    class2.a = 6
    assert class2.get_tracked_attrs_values() == {'a': 6, 'b': 4, 'c': 5}, "Tracked attributes values should be updated"
    print(class2.get_tracked_attrs_values()) # Output: {'a': 6, 'b': 4, 'c': 5}