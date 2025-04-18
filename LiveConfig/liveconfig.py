from liveconfig.core import manager
from . import logger

import os
import json
import ast

class LiveConfig:
    def __init__(self, path=None):
        self.path = path
        self.setup_file()

        manager.file_handler = self
        self.loaded_values = None
        self.load()

    def setup_file(self):
        """
        This member method sets up the file for saving and loading variables.
        If the filepath is provided by the user, otherwise it uses a default one.
        It also checks if the path includes a filename.
        """
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


    def save(self):
        """
        Saves all of the live variables to the specified file.
        Returns True if success, False otherwise.
        """
        serialized_instance = self.serialize_instances()
        serialized_variables = self.serialize_variables()
        data = {**serialized_instance, **serialized_variables}
        try:
            with open(self.path, 'w') as file:
                json.dump(data, file, indent=4)
                logger.info("Successfully saved live variables.")
            return True
        except Exception as e:
            logger.error(f"ERROR: Error saving file: {e}")
            return False
        
    def load(self):
        """
        Loads all of the variables from the specified file.
        Saves type as a class variable.
        Everything is stored as a string, then evaluated when loaded.
        Manager then checks if values exist upon registering a live variable.
        If exists then loads into position.
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
            logger.error(f"ERROR: Error loading: {e}")
            return False
        
    def reload(self):
        """
        Reloads the variables from the file.
        """
        try:
            self.load()
            saved_instances = self.loaded_values.get("live_instances", {})
            manager.load_values_into_instances(saved_instances)

            saved_variables = self.loaded_values.get("live_variables", {})
            manager.load_values_into_variables(saved_variables)

            logger.info("Successfully reloaded live variables.")
            return True
        except Exception as e:
            logger.error(f"ERROR: Error reloading file: {e}")
            return False
        
    def serialize_instances(self):
        """
        This member function serializes the live instances to be saved.
        It removes any attributes that are not created by the user.
        All attributes are converted to strings, so tuples/sets are not stored as lists.
        """
        instances = manager.live_instances
        serialized_instances = {}
        serialized_instances["live_instances"] = {}
        for instance_name, live_instance in instances.items():
            attributes = vars(live_instance)
            clean_attrs = {}
            for attr, value in attributes.items():
                if attr.startswith("__") or attr.startswith("_tracked_attrs"):
                    continue
                clean_attrs[attr] = str(value)

            serialized_instances["live_instances"][instance_name] = clean_attrs
        return serialized_instances
    

    def serialize_variables(self):
        """
        This member function serializes the live variables to be saved.
        All variables are converted to strings, so tuples/sets are not stored as lists.
        """
        variables = manager.live_variables
        serialized_variables = {}
        serialized_variables["live_variables"] = {}
        for var_name, var_obj in variables.items():
            if isinstance(var_obj.value, (int, float, str, bool, tuple, list, set)):
                serialized_variables["live_variables"][var_name] = str(var_obj.value)
            else:
                raise TypeError(f"Unsupported variable type: {type(var_obj.value)}")
        return serialized_variables