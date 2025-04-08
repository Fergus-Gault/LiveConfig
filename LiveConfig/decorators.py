from liveconfig.core import manager

def liveclass(cls):
    """
    Decorator to track the attributes of a class and its instances
    """
    class LiveClass(cls):
        _instances = []
        def __init__(self, *args, **kwargs) -> None:
            self._tracked_attrs = set()
            super().__init__(*args, **kwargs)

        def __setattr__(self, name, value) -> None:
            super().__setattr__(name, value)
            if name != "_tracked_attrs":
                self._tracked_attrs.add(name)

        def get_tracked_attrs(self):
            return {attr for attr in self._tracked_attrs if attr != "_tracked_attrs"}
        
        def get_tracked_attrs_values(self):
            return {name: getattr(self, name) for name in self._tracked_attrs if name != "_tracked_attrs"}

    LiveClass.__name__ = cls.__name__
    LiveClass.__qualname__ = cls.__qualname__
    LiveClass.__module__ = cls.__module__
    LiveClass.__doc__ = cls.__doc__

    manager.register_class(LiveClass)
    return LiveClass

def liveinstance(name=None):
    """
    Decorator to track the attributes of a class instance
    """
    def wrapper(obj):
        if not hasattr(obj, "get_tracked_attrs") or not hasattr(obj, "get_tracked_attrs_values"):
            raise TypeError("Instance is not from a @liveclass-decorated class. Use @liveclass on the class first.")
        obj_name = name if name else f"instance_{id(obj)}"
        manager.register_instance(obj_name, obj)
        return obj
    return wrapper
