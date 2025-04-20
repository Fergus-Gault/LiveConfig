from . import logger
import ast


class TypeChecker:

    def handle_instance_type(instance: object, attr_name: str, value: str):
        """Handle instance types from the interface."""
        # TODO: Add support for objects, enums, and other types.
        attr = type(getattr(instance, attr_name))
        if attr in {int, float, bool, list, tuple, set}:
            parsed_value = TypeChecker.handle_type(value)
        else:
            parsed_value = type(getattr(instance, attr_name))(value)

        return parsed_value
    
    def handle_variable_type(value: str):
        """Handle variable types from interface."""
        try:
            parsed_value = ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            parsed_value = value
        return parsed_value

    
    def handle_type(value: str):
        """
        Handles the conversion of a string representation 
        to the appropriate type.

        Args:
            value (str): The string representation of the type.
        
        Raises:
            ValueError: If the value cannot be parsed into a type.
            SyntaxError: If the value has a syntax error.

        Returns:
            int | float | bool | list | tuple | set: The parsed value.
        """
        # TODO: Add support for more types
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            logger.warning(f"Failed to parse value: {e}")