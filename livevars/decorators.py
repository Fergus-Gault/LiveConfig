from functools import wraps
from livevars.core import manager

def liveclass(cls):
    """
    Decorator to track the attributes of a class and its instances
    """
    class LiveClass(cls):
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
    manager.register_class(LiveClass)
    return LiveClass

def livefunction(func):
    """
    Decorator to track the parameters of a function and their values
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.tracked_params = {
            "args": args,
            "kwargs": kwargs
        }
        wrapper.tracked_params_values = {
            **{f"arg{i}": arg for i, arg in enumerate(args)},
            **kwargs
        }
        return func(*args, **kwargs)
    
    manager.register_function(wrapper)
    return wrapper