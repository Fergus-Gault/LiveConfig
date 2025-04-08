import logging
logger = logging.getLogger(__name__)

class TypeChecker:

    # TODO: Create a generalized function to handle all types to allow recursive types.
    # Such as nested tuples, lists, dicts, etc.

    def handle_bool(value):
        """
        Handle boolean values for the web interface.
        """
        if isinstance(value, str):
            if value.lower() in ["true", "1", "yes", "y"]:
                return True
            elif value.lower() in ["false", "0", "no", "n"]:
                return False
        return value
    
    def handle_int(value):
        """
        Handle integer values for the web interface.
        """
        if isinstance(value, str):
            try:
                value = float(value)
                return int(value)
            except ValueError:
                return value
        return value
    
    def handle_tuple(tup, instance, attr_name):
        """
        Handles parsing of tuples from interface to the object.
        """
        tuple_types = TypeChecker._parse_tuple_type(instance, attr_name)
        values = tup.strip("()")
        values = values.split(",")
        if len(values) != len(tuple_types):
            logger.warning(f"WARNING: Cannot change size of tuple: {len(values)} != {len(tuple_types)}")
            return None
        c = 0
        try:
            new_values = []
            for i in range(len(values)):
                stripped_value = "".join(x.strip() for x in values[i])
                if tuple_types[i] == str:
                    stripped_value = stripped_value.strip("'\"")
                    new_values.append(stripped_value)
                else:
                    new_values.append(tuple_types[i](stripped_value))
            values = tuple(new_values)
            c += 1
            return values
        except (ValueError, TypeError):
            logger.warning(f"WARNING: Failed to update: '{values[c]}' must be of type '{tuple_types[c]}'")
            return None
    
    def _parse_tuple_type(instance: object, tuple_name: str):
        """
        Parse types of individual elements of a tuple.
        """
        tup = getattr(instance, tuple_name)
        if isinstance(tup, tuple):
            return tuple(type(i) for i in tup)
        else:
            raise TypeError(f"Attribute {tuple_name} is not a tuple.")
        
    def handle_list(lst: list, instance: object, lst_name: str):
        # TODO, Make it so that the user has to specify the type of the item if they add/change the item.
        # Check for '->' in the string to specify the type.
        # Otherwise assume the type is the same as the original.
        # Default to string otherwise.
        """
        Handles parsing of lists from interface to the object.
        """
        list_types = TypeChecker._parse_list_type(instance, lst_name)
        values = lst.strip("[]")
        values = values.split(",")
        new_values = []
        for i in range(len(values)):
            try:
                stripped_value = "".join(x.strip() for x in values[i])
                if i >= len(list_types):
                    new_values.append(stripped_value)
                else:
                    if list_types[i] == str:
                        stripped_value = stripped_value.strip("'\"")
                        new_values.append(stripped_value)
                    else:
                        new_values.append(list_types[i](stripped_value))
            except (ValueError, TypeError):
                # Type has changed, so check to see if type has been specified.
                # If not, then just return the original value.
                if '->' in values[i]:
                    new_value = values[i].split("->")
                    if len(new_value) == 2:
                        try:
                            new_type = TypeChecker._str_to_type(new_value[1])
                            new_value = new_type(new_value[0])
                            new_values.append(new_value)
                        except (ValueError, TypeError):
                            logger.warning(f"WARNING: Unrecognized type '{new_value[1]}'")
                            return None
                else:
                    logger.warning(f"WARNING: Type has changed for value {values[i]}. Specify the type with `value->type`.")
                
        value = list(new_values)
        return value

    def _parse_list_type(instance: object, lst_name: str):
        """
        Parse types of individual elements of a list.
        """
        lst = getattr(instance, lst_name)
        if isinstance(lst, list):
            return tuple(type(i) for i in lst)
        else:
            raise TypeError(f"Attribute {lst_name} is not a list.")
        
    def _str_to_type(type_str: str):
        """
        Convert a string to a type.
        """
        type_map = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "tuple": tuple,
            "list": list,
            "dict": dict,
            "set": set,
        }
        return type_map.get(type_str.strip().lower(), None)
