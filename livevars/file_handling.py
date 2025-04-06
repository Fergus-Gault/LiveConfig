from livevars.core import manager

import os
import json


class FileHandler:
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

    def serialize_instances(self):
        """
        This member function serializes the live instances to be saved.
        It removes any attributes that are not created by the user.
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
                try:
                    json.dumps(value)
                    clean_attrs[attr] = value
                except (TypeError, ValueError):
                    clean_attrs[attr] = str(value)

            serialized_instances["live_instances"][instance_name] = clean_attrs
        return serialized_instances

    def save(self):
        """
        Saves all of the live variables to the specified file.
        Returns True if success, False otherwise.
        """
        serialized_instance = self.serialize_instances()
        try:
            with open(self.path, 'w') as file:
                json.dump(serialized_instance, file, indent=4)
                print("Successfully saved live variables.")
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
        
    def load(self):
        """
        Loads all of the variables from the specified file.
        Saves type as a class variable.
        Manager then checks if values exist upon registering a live variable.
        If exists then loads into position.
        """
        try:
            with open(self.path) as file:
                self.loaded_values = json.load(file)
            return True
        except Exception as e:
            print(f"Error loading: {e}")
            return False
        