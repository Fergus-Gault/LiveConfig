from . import logger
from liveconfig.typechecker import TypeChecker


class LiveManager:
    def __init__(self):
        self.live_classes = {}
        self.live_instances = {}
        self.live_variables = {}
        self.function_triggers = {}
        self.file_handler = None

    def load_values_into_instances(self, saved_instances: dict) -> None:
        for name, attrs in saved_instances.items():
            instance = self.live_instances.get(name)
            if instance:
                self.load_values_into_instance(instance, attrs)

    def load_values_into_instance(self, instance: object, attrs: dict) -> object:
        """
        Loads the values from the save file into the instance.
        """
        for attr, value in attrs.items():
            setattr(instance, attr, value)
        return instance
    
    def get_live_class_by_name(self, class_name: str) -> object:
        """
        Get a live class by name
        """
        return self.live_classes.get(class_name)
    
    def get_live_instances(self, class_name: str) -> list | None:
        """
        Get all instances of a live class
        """
        cls = self.get_live_class_by_name(class_name)
        if cls:
            return getattr(cls, "_instances", [])
        return None
    
    def list_all_instances(self) -> str:
        """
        Get all live instances
        """
        string = ""
        for name, instance in self.live_instances.items():
            string += f"{name}: {instance}\n"
        return string
    
    def list_instance_attrs_by_name(self, instance_name: str) -> str | None:
        """
        Get all attributes of a live instance by name
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance:
            string = ""
            attrs = instance.get_tracked_attrs_values()
            for attr, value in attrs.items():
                string += f"{attr}: {value}\n"
            return string
        return None
    
    def list_all_attributes(self, instance_name: str) -> set | None:
        """
        Get all attributes of a live instance
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance:
            return instance.get_tracked_attrs()
        return None
    
    def get_live_instance_by_name(self, instance_name: str) -> object | None:
        """
        Get a live class instance by name
        """
        if instance_name in self.live_instances:
            return self.live_instances[instance_name]
        else:
            logger.warning(f"Instance '{instance_name}' does not exist")
            return None
        
    def get_live_instance_attr_by_name(self, instance_name: str, attr_name: str) -> object | None:
        """
        Get an attribute of a live instance by name
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance is not None:
            attr = getattr(instance, attr_name, None)
            if not hasattr(instance, attr_name):
                logger.warning(f"Attribute '{attr_name}' does not exist on '{instance_name}'")
            return attr
        
    
    def set_live_instance_attr_by_name(self, instance_name: str, attr_name: str, value: str) -> None:
        """
        Set an attribute of a live instance.
        Type is parsed from the input string.
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance is None: return
        attr = self.get_live_instance_attr_by_name(instance_name, attr_name)
        if attr is None: return
        value = TypeChecker.handle_instance_type(instance, attr_name, value)
        if value is not None:            
            try:
                setattr(instance, attr_name, value)
            except Exception as e:
                logger.warning(f"Failed to update: {e}. Reverting to previous value.")
        return
    
    def get_live_variable_by_name(self, name: str) -> object | None:
        """
        Get a live variable by name
        """
        return self.live_variables.get(name)
    
    def get_live_variable_value_by_name(self, name: str) -> object | None:
        """
        Get the value of a live variable by name
        """
        live_variable = self.get_live_variable_by_name(name)
        if live_variable:
            return live_variable.value
        return None
    
    def set_live_variable_by_name(self, name: str, value: str) -> None:
        """
        Set a live variable by name and update any references to it
        """
        if name not in self.live_variables:
            raise ValueError(f"Variable with name {name} does not exist.")
        self.live_variables[name].value = TypeChecker.handle_variable_type(value)
    
    def load_values_into_variables(self, saved_variables: dict) -> None:
        for name, value in saved_variables.items():
            self.set_live_variable_by_name(name, value)


    def list_all_variables(self) -> str:
        """
        Get all live variables
        """
        string = ""
        for name, _ in self.live_variables.items():
            string += f"{name}\n"
        return string
    

    def list_variable_by_name(self, name: str):
        """
        Get a live variable by name
        """
        variable = self.get_live_variable_by_name(name)
        if variable:
            return variable.value
        return None
    

    def get_function_by_name(self, name: str):
        """
        Get a function by name
        """
        return self.function_triggers.get(name)
    

    def get_function_args_by_name(self, name: str):
        """
        Get the arguments of a function by name
        """
        function_info = self.get_function_by_name(name)
        if function_info:
            return function_info["param_names"]
        return None
    

    def trigger_function_by_name(self, name: str, **kwargs):
        """
        Trigger a function by name
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
        """
        List all triggers
        """
        string = ""
        for name, func_info in self.function_triggers.items():
            string += f"{name}: {func_info['function']}\n"
        return string
    
    
    def list_all_trigger_args(self, name: str) -> str:
        """
        List all trigger arguments
        """
        function_info = self.get_function_by_name(name)
        if function_info:
            string = ""
            for arg in function_info["param_names"]:
                string += f"{arg}\n"
            if len(function_info["param_names"]) == 0:
                string += "No arguments"
            return string
        return None