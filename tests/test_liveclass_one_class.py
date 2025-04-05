from livevars.decorators import liveclass

@liveclass
class testClass:
    """
    Test class to demonstrate the liveclass decorator
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_sum(self) -> int:
        return self.x + self.y


# Example usage
def test_liveclass_one_class():
    obj = testClass(1, 2)
    assert obj.get_sum() == 3, "Sum should be 3"
    print(obj.get_sum())  # Output: 3
    assert obj.get_tracked_attrs() == {'x', 'y'}, "Tracked attributes should be x and y"
    print(obj.get_tracked_attrs())  # Output: {'x', 'y'}
    obj.z = 3
    assert obj.get_tracked_attrs() == {'x', 'y', 'z'}, "Tracked attributes should be x, y, and z"
    print(obj.get_tracked_attrs())  # Output: {'x', 'y', 'z'}
    obj.x = 5
    assert obj.get_tracked_attrs_values() == {'x': 5, 'y': 2, 'z': 3}, "Tracked attributes values should be updated"
    print(obj.get_tracked_attrs_values()) # Output: {'x': 5, 'y': 2, 'z': 3}