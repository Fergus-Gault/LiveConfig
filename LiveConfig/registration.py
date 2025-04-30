from liveconfig.core import manager
from liveconfig.typechecker import TypeChecker
import inspect

class Register:

    def cls(cls: object) -> object:
        """
        This function registers a class to be tracked.

        Args:
            cls (object): The class to be registered.

        Returns:
            object: The registered class.
        """
        manager.live_classes[cls.__name__] = cls
        return cls
    

    def instance(name: str, instance: object) -> None:
        """
        This method registers an instance to be tracked.
        The instance is added to its respective liveclass.

        Args:
            name (str): The name of the instance to be registered.
            instance (object): The instance to be registered.

        Raises:
            ValueError: Raised if the instance name already exists.
        """

        if name in manager.live_instances:
            raise ValueError(f"Instance with name {name} already exists.")
        
        # Load value from file if it exists, else use the default value
        if manager.file_handler is not None \
            and manager.file_handler.loaded_values is not None \
            and "live_instances" in manager.file_handler.loaded_values:

            saved_attrs = manager.file_handler.loaded_values["live_instances"].get(name, {})
            instance = manager.load_values_into_instance(name, instance, saved_attrs)
        
        manager.live_instances[name] = instance
        # Register the instance in its class if it has a _instances attribute
        cls = type(instance)
        if hasattr(cls, "_instances"):
            cls._instances.append(instance)
        else:
            cls._instances = [instance]


    def variable(name: str, live_variable: object) -> None:
        """
        This method registers a variable to be tracked.
        The live_variable is generated from the livevar decorator.
        A live variable is a wrapped variable that can be modified.

        Args:
            name (str): Name of the variable to be registered.
            live_variable (object): The generated object from the livevar decorator.

        Raises:
            ValueError: Raised if the variable name already exists.
            TypeError: Raised if the variable value is not a basic type.
        """
        if name in manager.live_variables:
            raise ValueError(f"Variable with name {name} already exists.")
        
        if not isinstance(
            live_variable.value, 
            (int, float, str, bool, tuple, list, set)):
            raise TypeError(
                "Value must be a basic type "
                "(int, float, str, bool, tuple, list, set).")
        
        # If no file handler is set, register the variable directly
        if manager.file_handler is None \
            or manager.file_handler.loaded_values is None:
            manager.live_variables[name] = live_variable
            return
        
        # If the value is not saved then set it directly.
        saved_value = manager.file_handler.loaded_values["live_variables"].get(name, None)
        if saved_value is None:
            manager.live_variables[name] = live_variable
            return
        
        # If the value is saved, load it into the live variable
        live_variable.value = TypeChecker.handle_variable_type(saved_value)
        manager.live_variables[name] = live_variable
        

    def trigger(func: callable, args: list = None, kwargs: dict = None) -> callable:
        """
        Registers a trigger function to the manager.
        Triggers can be called through the interface to execute once.

        Args:
            func (callable): The function to be registered.
            args (list, optional): Function arguments. Defaults to None.
            kwargs (dict, optional): Function keyword arguments. Defaults to None.

        Raises:
            TypeError: Raised if the provided function is not callable.

        Returns:
            callable: The registered function.
        """

        if not callable(func):
            raise TypeError("Function must be callable.")
        
        func_name = func.__name__
        signature = inspect.signature(func)
        param_names = list(signature.parameters.keys())

        # FIXME: Temporary solution to avoid triggers in classes
        # Should be able to call instance methods as well
        # Will need to generate for each instance of the class.
        # Class will need to be a @liveclass
        if "self" in param_names:
            raise TypeError(
                "Function trigger cannot be a member function.")
        
        # Update existing entry or create new one
        if func_name in manager.function_triggers:
            if args is not None:
                manager.function_triggers[func_name]["args"] = args
            if kwargs is not None:
                manager.function_triggers[func_name]["kwargs"] = kwargs
            if param_names is not None:
                manager.function_triggers[func_name]["param_names"] = param_names
        else:
            manager.function_triggers[func_name] = {
                "function": func,
                "param_names": param_names or [],
                "args": args or [],
                "kwargs": kwargs or {}
            }
        
        return func