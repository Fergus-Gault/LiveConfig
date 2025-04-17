from . import logger
import ast


class TypeChecker:

    def handle_type(instance: object, attr_name: str, value):
        # TODO: Add support for objects, enums, and other types.
        attr = type(getattr(instance, attr_name))
        if attr == bool:
            value = TypeChecker.handle_bool(value)
        elif attr == int or attr == float:
            value = TypeChecker.handle_numerical(value)
        elif attr == tuple or attr == list or attr == set:
            item = getattr(instance, attr_name, None)
            value = TypeChecker.handle_iterable(value, item)
        else:
            value = type(getattr(instance, attr_name))(value)

        return value


    def handle_bool(value):
        """
        Handle boolean values from interface.
        """
        if isinstance(value, str):
            if value.lower() in ["true", "1", "yes", "y"]:
                return True
            elif value.lower() in ["false", "0", "no", "n"]:
                return False
        return value
    
    def handle_numerical(value):
        """
        Handles numerical values from the interface.
        """
        # TODO: Add support for complex numbers and other numerical types, increase checking.
        try:
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            logger.warning(f"WARNING: Failed to parse numerical value: {e}")
            return None
        return value
    
    def handle_iterable(value, iterable):
        """
        Handles parsing of iterable types from the interface.
        """
        # TODO:Increase checking for tuples, so that sizes are checked.
        try:
            iterable = ast.literal_eval(value)
        except (ValueError, SyntaxError) as e:
            logger.warning(f"WARNING: Failed to parse iterable value: {e}")
            return
        return iterable
