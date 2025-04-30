from liveconfig.core import manager
from . import logger

import os
import json
import ast

class LiveConfig:
    """
    Initialiser class for LiveConfig.
    Responsible for setting up the file handler for saving and loading variables.
    """
    def __init__(self, path=None):
        self.path = path
        self.setup_file()

        manager.file_handler = self
        self.loaded_values = None
        self.load()

    def setup_file(self) -> None:
        """Sets up the file path for saving and loading variables."""
        if self.path is None:
            self.path = os.path.join(os.getcwd(), "variables.json")
        else:
            if "." not in (self.path.split("/"))[-1]:
                self.path = os.path.abspath(self.path + "/variables.json")
            else:
                self.path = os.path.abspath(self.path)

        # Ensure the file exists
        if not os.path.exists(self.path):
            with open(self.path, 'w') as file:
                file.write('{}')


    def save(self) -> bool:
        """Saves serialized values to the specified file."""
        serialized_instance = self.serialize_instances()
        serialized_variables = self.serialize_variables()
        data = {**serialized_instance, **serialized_variables}
        try:
            with open(self.path, 'w') as file:
                json.dump(data, file, indent=4)
                logger.info("Successfully saved live variables.")
            return True
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return False
        
    def load(self) -> bool:
        """
        Loads the serialized values from the specified file.
        It attempts to convert the string values back to their original types.
        If the conversion fails, it keeps the value as a string.
        The manager will then load these values into their correct place.
        """
        try:
            with open(self.path, 'r') as file:
                loaded_values = json.load(file)
            
            # Load live instances
            saved_instances = loaded_values.get("live_instances", {})
            for name, attrs in saved_instances.items():
                for attr, value in attrs.items():
                    # Attempt to evaluate the type from the saved string.
                    try:
                        value = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        value = str(value)
                    attrs[attr] = value
                saved_instances[name] = attrs
            self.loaded_values = {"live_instances": saved_instances}

            # Load live variables
            saved_variables = loaded_values.get("live_variables", {})
            for name, value in saved_variables.items():
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    value = str(value)
                saved_variables[name] = value
            self.loaded_values["live_variables"] = saved_variables

            return True
        except Exception as e:
            logger.error(f"Error loading: {e}")
            return False
        
    def reload(self) -> bool:
        """Reloads the saved values"""
        try:
            self.load()
            saved_instances = self.loaded_values.get("live_instances", {})
            manager.load_values_into_instances(saved_instances)

            saved_variables = self.loaded_values.get("live_variables", {})
            manager.load_values_into_variables(saved_variables)

            logger.info("Successfully reloaded live variables.")
            return True
        except Exception as e:
            logger.error(f"Error reloading file: {e}")
            return False
        
    def serialize_instances(self) -> dict:
        """Serializes the instances to be saved."""
        instances = manager.live_instances
        serialized_instances = {}
        serialized_instances["live_instances"] = {}
        for instance_name, live_instance in instances.items():
            attributes = vars(live_instance)
            clean_attrs = {}
            for attr, value in attributes.items():
                if attr.startswith("__") or attr.startswith("_"):
                    continue
                clean_attrs[attr] = str(value)

            serialized_instances["live_instances"][instance_name] = clean_attrs
        return serialized_instances
    

    def serialize_variables(self) -> dict:
        """Serializes the live variables to be saved."""
        variables = manager.live_variables
        serialized_variables = {}
        serialized_variables["live_variables"] = {}
        for var_name, var_obj in variables.items():
            if isinstance(var_obj.value, (int, float, str, bool, tuple, list, set)):
                serialized_variables["live_variables"][var_name] = str(var_obj.value)
            else:
                raise TypeError(f"Unsupported variable type: {type(var_obj.value)}")
        return serialized_variables