from liveconfig.core import manager
from liveconfig.typechecker import TypeChecker

class Register:

    def cls(cls):
        """
        Register a class to be tracked
        """
        manager.live_classes[cls.__name__] = cls
        return cls
    
    def instance(name, instance):
        """
        Register an instance of a class to be tracked
        """
        if name in manager.live_instances:
            raise ValueError(f"Instance with name {name} already exists.")
        
        # Load value from file if it exists, else use the default value
        if manager.file_handler is not None and manager.file_handler.loaded_values is not None and "live_instances" in manager.file_handler.loaded_values:
            saved_attrs = manager.file_handler.loaded_values["live_instances"].get(name, {})
            instance = manager.load_values_into_instance(instance, saved_attrs)
        
        manager.live_instances[name] = instance
        # Register the instance in its class if it has a _instances attribute
        cls = type(instance)
        if hasattr(cls, "_instances"):
            cls._instances.append(instance)
        else:
            cls._instances = [instance]


    def variable(name, live_variable):
        """
        Register a variable to be tracked.
        It ensures that the value is a basic type.
        It loads the value from the file into the live variable if it exists, otherwise it uses the default value.
        """
        if name in manager.live_variables:
            raise ValueError(f"Variable with name {name} already exists.")
        
        if not isinstance(live_variable.value, (int, float, str, bool, tuple, list, set)):
            raise TypeError("Value must be a basic type (int, float, str, bool, tuple, list, set).")
        
        if manager.file_handler is not None and manager.file_handler.loaded_values is not None and "live_variables" in manager.file_handler.loaded_values:
            saved_value = manager.file_handler.loaded_values["live_variables"].get(name, None)
            if saved_value is not None:
                # If the value is saved, load it into the live variable
                live_variable.value = TypeChecker.handle_variable_type(saved_value)
                manager.live_variables[name] = live_variable
            else:
                manager.live_variables[name] = live_variable
        else:
            manager.live_variables[name] = live_variable