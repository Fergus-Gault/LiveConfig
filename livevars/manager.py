class LiveManager:
    def __init__(self):
        self.live_functions = {}
        self.live_classes = {}
        self.live_instances = {}

    def register_function(self, func):
        """
        Register a function to be tracked
        """
        key = f"{func.__module__}.{func.__name__}"
        self.live_functions[key] = func
        return func
    
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
        self.live_instances[name] = instance
        # Register the instance in its class if it has a _instances attribute
        cls = type(instance)
        if hasattr(cls, "_instances"):
            cls._instances.append(instance)
        else:
            cls._instances = [instance]
    
    def get_live_functions(self):
        """
        Get all live functions
        """
        return self.live_functions
    
    def get_live_classes(self):
        """
        Get all live classes
        """
        return self.live_classes
    
    def get_live_function_by_name(self, func_name):
        """
        Get a live function by name
        """
        return self.live_functions.get(func_name)
    
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
    
    def get_live_instance_by_name(self, instance_name):
        """
        Get a live class instance by name
        """
        if instance_name in self.live_instances:
            return self.live_instances[instance_name]
        else:
            return None
        
    def get_live_instance_attr_by_name(self, instance_name, attr_name):
        """
        Get an attribute of a live instance by name
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance is not None:
            return getattr(instance, attr_name)
            
        return None