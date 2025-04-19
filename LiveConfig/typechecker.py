from . import logger
import ast


class TypeChecker:

    def handle_instance_type(instance: object, attr_name: str, value: str):
        # TODO: Add support for objects, enums, and other types.
        attr = type(getattr(instance, attr_name))
        if attr in {int, float, bool}:
            value = TypeChecker.handle_non_iterable(value)
        elif attr in {list, tuple, set}:
            item = getattr(instance, attr_name, None)
            value = TypeChecker.handle_iterable(value, item)
        else:
            value = type(getattr(instance, attr_name))(value)

        return value
    
    def handle_variable_type(value: str):
        """
        Handle variable types from interface.
        """
        try:
            new_value = ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            new_value = value
        return new_value

    
    def handle_non_iterable(value: str):
        """
        Handles numerical values from the interface.
        """
        # TODO: Add support for complex numbers and other numerical types, increase checking.
        try:
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            logger.warning(f"Failed to parse numerical value: {e}")
            return None
        return value
    
    def handle_iterable(value: str, iterable):
        """
        Handles parsing of iterable types from the interface.
        """
        # TODO:Increase checking for tuples, so that sizes are checked.
        try:
            iterable = ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            logger.warning(f"Failed to parse iterable value: {e}")
            return
        return iterable
