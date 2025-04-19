from liveconfig.livevariable import LiveVariable
from liveconfig.registration import Register
import inspect


def liveclass(cls: object) -> object:
    """
    Decorator to track the attributes of a class and register it with the manager.
    This decorator adds methods to the class to track attributes and their values.
    It ensures that the class is still recognised by IDEs and type checkers.
    """
    original_init = cls.__init__
    original_setattr = getattr(cls, '__setattr__', object.__setattr__)

    def __init__(self, *args, **kwargs) -> None:
        self._tracked_attrs = set()
        original_init(self, *args, **kwargs)

    def __setattr__(self, name, value) -> None:
        original_setattr(self, name, value)
        if name != "_tracked_attrs":
            self._tracked_attrs.add(name)

    def get_tracked_attrs(self) -> set:
        return {attr for attr in self._tracked_attrs if attr != "_tracked_attrs"}

    def get_tracked_attrs_values(self) -> dict:
        return {name: getattr(self, name) for name in self._tracked_attrs if name != "_tracked_attrs"}

    cls.__init__ = __init__
    cls.__setattr__ = __setattr__
    cls.get_tracked_attrs = get_tracked_attrs
    cls.get_tracked_attrs_values = get_tracked_attrs_values

    Register.cls(cls)
    return cls


def liveinstance(name=None) -> object:
    """
    Decorator to track the attributes of a class instance
    Usage: instance = liveinstance("instance_name")(MyClass())
    """
    def wrapper(obj):
        if not hasattr(obj, "get_tracked_attrs") or not hasattr(obj, "get_tracked_attrs_values"):
            raise TypeError("Instance is not from a @liveclass-decorated class. Use @liveclass on the class first.")
        obj_name = name if name else f"instance_{id(obj)}"
        Register.instance(obj_name, obj)
        return obj
    return wrapper
    

def livevar(name=None) -> object:
    """
    Decorator to track the value of a variable.
    Usage: variable = livevar("variable_name")(value)
    """
    def wrapper(value):
        if not isinstance(value, (int, float, str, bool, tuple, list, set)):
            raise TypeError("Value must be a basic type (int, float, str, bool, tuple, list, set).")
        if name is None:
            raise ValueError("Variable name must be provided.")
        live_variable = LiveVariable(name, value)
        Register.variable(name, live_variable)
        return live_variable
    return wrapper


def trigger(func: callable) -> callable:
    """
    Decorator to track the function and its arguments.
    Usage: @trigger
           def my_function(arg1, arg2):
               pass
    """
    if not callable(func):
        raise TypeError("Function must be callable.")
    if not hasattr(func, "__name__"):
        raise TypeError("Function must have a name.")
    if not hasattr(func, "__code__"):
        raise TypeError("Function must have code.")
    
    # Register the function with empty args/kwargs initially
    signature = inspect.signature(func)
    param_names = list(signature.parameters.keys())
    Register.trigger(func, param_names=param_names, args=[], kwargs={})
    
    # Return a wrapper that will be called when the function is invoked
    def wrapper(*args, **kwargs):
        # Update registration with actual args/kwargs when called
        Register.trigger(func, list(args), dict(kwargs))  
        return func(*args, **kwargs)
        
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__dict__.update(func.__dict__)
    return wrapper

