from . import logger
from liveconfig.typechecker import TypeChecker


class LiveManager:
    def __init__(self):
        self.live_classes = {}
        self.live_instances = {}
        self.live_variables = {}
        self.file_handler = None
    
    def register_class(self, cls):
        """
        Register a class to be tracked
        """
        self.live_classes[cls.__name__] = cls
        return cls
    
    def register_instance(self, name, instance):
        """
        Register an instance of a class to be tracked
        """
        if name in self.live_instances:
            raise ValueError(f"Instance with name {name} already exists.")
        
        # Load value from file if it exists, else use the default value
        if self.file_handler is not None and self.file_handler.loaded_values is not None and "live_instances" in self.file_handler.loaded_values:
            saved_attrs = self.file_handler.loaded_values["live_instances"].get(name, {})
            instance = self.load_values_into_instance(instance, saved_attrs)
        
        self.live_instances[name] = instance
        # Register the instance in its class if it has a _instances attribute
        cls = type(instance)
        if hasattr(cls, "_instances"):
            cls._instances.append(instance)
        else:
            cls._instances = [instance]

    def load_values_into_instances(self, saved_instances):
        for name, attrs in saved_instances.items():
            instance = self.live_instances.get(name)
            if instance:
                self.load_values_into_instance(instance, attrs)

    def load_values_into_instance(self, instance, attrs):
        """
        Loads the values from the save file into the instance.
        """
        for attr, value in attrs.items():
            setattr(instance, attr, value)
        return instance
    
    def get_live_classes(self):
        """
        Get all live classes
        """
        return self.live_classes
    
    def get_live_class_by_name(self, class_name):
        """
        Get a live class by name
        """
        return self.live_classes.get(class_name)
    
    def get_live_instances(self, class_name):
        """
        Get all instances of a live class
        """
        cls = self.get_live_class_by_name(class_name)
        if cls:
            return getattr(cls, "_instances", [])
        return None
    
    def get_all_instances(self):
        """
        Get all live instances
        """
        return self.live_instances
    
    def get_live_instance_by_name(self, instance_name):
        """
        Get a live class instance by name
        """
        if instance_name in self.live_instances:
            return self.live_instances[instance_name]
        else:
            logger.warning(f"WARNING: Instance '{instance_name}' does not exist")
            return None
        
    def get_live_instance_attr_by_name(self, instance, attr_name):
        """
        Get an attribute of a live instance by name
        """
        if instance is not None:
            attr = getattr(instance, attr_name, None)
            if not hasattr(instance, attr_name):
                logger.warning(f"WARNING: Attribute '{attr_name}' does not exist on '{instance}'")
            return attr
        
    
    def set_live_instance_attr_by_name(self, instance_name, attr_name, value):
        """
        Set an attribute of a live instance.
        Type is parsed from the input string.
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance is None: return
        attr = self.get_live_instance_attr_by_name(instance, attr_name)
        if attr is None: return
        value = TypeChecker.handle_instance_type(instance, attr_name, value)
        if value is not None:            
            try:
                setattr(instance, attr_name, value)
            except Exception as e:
                logger.warning(f"WARNING: Failed to update: {e}. Reverting to previous value.")
        return
    
    def register_variable(self, name, live_variable):
        """
        Register a variable to be tracked.
        """
        if name in self.live_variables:
            raise ValueError(f"Variable with name {name} already exists.")
        
        # Ensure that the value within the live variable is a basic type
        if not isinstance(live_variable.value, (int, float, str, bool, tuple, list, set)):
            raise TypeError("Value must be a basic type (int, float, str, bool, tuple, list, set).")
        
        # Load value from file if it exists, else use the default value
        if self.file_handler is not None and self.file_handler.loaded_values is not None and "live_variables" in self.file_handler.loaded_values:
            saved_value = self.file_handler.loaded_values["live_variables"].get(name, None)
            if saved_value is not None:
                # If the value is in the file, then assign it to the live variable, and store the object itself in the set
                live_variable.value = TypeChecker.handle_variable_type(saved_value)
                self.live_variables[name] = live_variable
            else:
                # If the value is not in the file, then assign the default value to the live variable, and store the object itself in the set
                self.live_variables[name] = live_variable
        else:
            # If the file handler is not set, then just store the live variable in the set
            self.live_variables[name] = live_variable
    
    def get_live_variables(self):
        """
        Get all live variables
        """
        return self.live_variables
    
    def get_live_variable_by_name(self, name):
        """
        Get a live variable by name
        """
        return self.live_variables.get(name)
    
    def get_live_variable_value_by_name(self, name):
        """
        Get the value of a live variable by name
        """
        live_variable = self.get_live_variable_by_name(name)
        if live_variable:
            return live_variable.value
        return None
    
    def set_live_variable_by_name(self, name, value):
        """
        Set a live variable by name and update any references to it
        """
        if name not in self.live_variables:
            raise ValueError(f"Variable with name {name} does not exist.")
        self.live_variables[name].value = TypeChecker.handle_variable_type(value)
    
    def load_values_into_variables(self, saved_variables):
        for name, value in saved_variables.items():
            self.set_live_variable_by_name(name, value)
    