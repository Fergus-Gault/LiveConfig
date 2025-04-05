class LiveManager:
    def __init__(self):
        self.live_functions = {}
        self.live_classes = {}

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