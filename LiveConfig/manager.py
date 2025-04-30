from . import logger
from liveconfig.typechecker import TypeChecker


class LiveManager:
    """Manager for live classes, instances, variables, and functions."""
    def __init__(self):
        self.live_classes = {}
        self.live_instances = {}
        self.live_variables = {}
        self.function_triggers = {}
        self.file_handler = None

    def get_live_class_by_name(self, class_name: str) -> object:
        """Get a live class by name"""
        return self.live_classes.get(class_name)
    

    def load_values_into_instances(self, saved_instances: dict) -> None:
        """
        Loads the values from the save file into each instance.

        Args:
            saved_instances (dict): Instances that have been saved to a file.
        """
        for instance_name, attrs in saved_instances.items():
            instance = self.get_live_instance_by_name(instance_name)
            if instance:
                self.load_values_into_instance(instance_name, instance, attrs)

    def load_values_into_instance(self, instance_name: str, instance: object, attrs: dict) -> object:
        """
        Loads the values of the attributes into the instance.

        Args:
            instance (object): The instance to load the values into.
            attrs (dict): The attributes to load into the instance.

        Returns:
            object: The instance with the loaded values.
        """
        to_pop = []
        for attr, value in attrs.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
            else:
                # Queue for removal if the attribute doesn't exist
                to_pop.append(attr)

        # Remove attributes that don't exist in the instance
        for attr in to_pop:
            self.file_handler.loaded_values["live_instances"][instance_name].pop(attr)
        return instance
    
    
    def get_live_instances(self, class_name: str) -> list | None:
        """Get all instances of a live class."""
        cls = self.get_live_class_by_name(class_name)
        if cls:
            return getattr(cls, "_instances", [])
        return None
    
    def list_all_instances(self) -> str:
        """Generate a string of all live instances."""
        string = ""
        for name, instance in self.live_instances.items():
            string += f"{name}: {instance}\n"
        return string
    
    def list_instance_attrs_by_name(self, 
                                    instance_name: str) -> str | None:
        """Get all attributes of a live instance."""
        instance = self.get_live_instance_by_name(instance_name)
        if instance:
            string = ""
            attrs = instance.get_tracked_attrs_values()
            for attr, value in attrs.items():
                string += f"{attr}: {value}\n"
            return string
        return None
    
    def get_live_instance_by_name(self, 
                                  instance_name: str) -> object | None:
        """
        Gets a live instance by its saved name.

        Args:
            instance_name (str): The name of the instance.

        Returns:
            object | None: The instance if it exists, otherwise None.
        """
        if instance_name in self.live_instances:
            return self.live_instances[instance_name]
        else:
            logger.warning(f"Instance '{instance_name}' does not exist")
            return None
        
    def get_live_instance_attr_by_name(self, 
                                       instance_name: str, 
                                       attr_name: str) -> object | None:
        """
        Get the attribute of a live instance by its name.

        Args:
            instance_name (str): Name of the instance.
            attr_name (str): Name of the attribute.

        Returns:
            object | None: The attribute if it exists, otherwise None.
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance is None: return

        attr = getattr(instance, attr_name, None)
        if not hasattr(instance, attr_name):
            logger.warning(
                f"Attribute '{attr_name}' does not exist on '{instance_name}'")
        return attr
        
    
    def set_live_instance_attr_by_name(self, 
                                       instance_name: str, 
                                       attr_name: str, 
                                       value: str) -> None:
        """
        This method sets the value of an attribute of a live instance.
        It parses the value to the correct type and sets it on the instance.

        Args:
            instance_name (str): Name of the instance.
            attr_name (str): Name of the attribute.
            value (str): Value to set on the attribute.
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance is None: return
        attr = self.get_live_instance_attr_by_name(instance_name, attr_name)
        if attr is None: return
        elif attr_name.startswith("_"):
            logger.warning(
                f"Attribute '{attr_name}' is private and cannot be modified")
            return
        value = TypeChecker.handle_instance_type(instance, attr_name, value)
        if value is None: return         
        try:
            setattr(instance, attr_name, value)
        except Exception as e:
            logger.warning(
                f"Failed to update: {e}. Reverting to previous value.")
    
    def get_live_variable_by_name(self, name: str) -> object | None:
        """Get a live variable by name."""
        return self.live_variables.get(name)
    
    def get_live_variable_value_by_name(self, name: str) -> object | None:
        """Get the value of a live variable by name"""
        live_variable = self.get_live_variable_by_name(name)
        if live_variable:
            return live_variable.value
        return None
    
    def set_live_variable_by_name(self, name: str, value: str) -> None:
        """
        This method sets the value of a live variable by its name.
        The type is parsed from the value and set on the variable.

        Args:
            name (str): Name of the variable.
            value (str): Value to set on the variable.

        Raises:
            ValueError: Raised if the variable does not exist.
        """
        if name not in self.live_variables:
            raise ValueError(f"Variable with name {name} does not exist.")
        self.live_variables[name].value = TypeChecker.handle_variable_type(value)
    
    def load_values_into_variables(self, saved_variables: dict) -> None:
        for name, value in saved_variables.items():
            self.set_live_variable_by_name(name, value)


    def list_all_variables(self) -> str:
        """Generate a string of all live variables."""
        string = ""
        for name, _ in self.live_variables.items():
            string += f"{name}\n"
        return string
    

    def list_variable_by_name(self, name: str):
        """Get a live variable by name"""
        variable = self.get_live_variable_by_name(name)
        if variable:
            return variable.value
        return None
    

    def get_function_by_name(self, name: str):
        """Get a function by name"""
        return self.function_triggers.get(name)
    

    def get_function_args_by_name(self, name: str):
        """Get the arguments of a function by name"""
        function_info = self.get_function_by_name(name)
        if function_info:
            return function_info["param_names"]
        return None
    

    def trigger_function_by_name(self, name: str, **kwargs):
        """
        This function triggers a function trigger with the given name.
        It checks if the function exists, and if so, 
        it calls the function with the provided arguments.

        Args:
            name (str): Name of the function to trigger.

        Raises:
            ValueError: Raised if the function does not exist.

        Returns:
            Any : The result of the function call, or None if the function does not exist.
        """
        if name not in self.function_triggers:
            raise ValueError(f"Function with name {name} does not exist.")
        
        function_info = self.function_triggers[name]
        func = function_info["function"]
        
        corrected_args = {}

        for arg_name in function_info["param_names"]:
            if arg_name in kwargs:
                corrected_arg = TypeChecker.handle_variable_type(kwargs[arg_name])
                corrected_args[arg_name] = corrected_arg
        
        try:
            result = func(**corrected_args)
            self.function_triggers[name]["kwargs"] = kwargs.get("kwargs", [])
            return result
        except Exception as e:
            logger.warning(f" Failed to trigger function '{name}': {e}")
            return None
        
    
    def list_all_triggers(self) -> str:
        """Generates a string of all function triggers."""
        string = ""
        for name, func_info in self.function_triggers.items():
            string += f"{name}: {func_info['function']}\n"
        return string
    
    
    def list_all_trigger_args(self, name: str) -> str:
        """Generates a string of all arguments of a function trigger."""
        function_info = self.get_function_by_name(name)
        if function_info:
            string = ""
            for arg in function_info["param_names"]:
                string += f"{arg}\n"
            if len(function_info["param_names"]) == 0:
                string += "No arguments"
            return string
        return None