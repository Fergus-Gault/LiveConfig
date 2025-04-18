from functools import total_ordering
from .. import logger

@total_ordering
class LiveVariable:
    """
    Wrapper class for live variables.
    This class allows for dynamic tracking of variable values and provides
    a consistent interface for mathematical operations and comparisons.
    """
    def __init__(self, name, value):
        self.name = name
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    # Dynamically delegate mathematical and comparison operations
    def _delegate_operation(self, operation, other, reverse=False):
        try:
            if reverse:
                return operation(other, self._value)
            return operation(self._value, other)
        except Exception as e:
            logger.warning(e)
            return None

    # Define mathematical operations
    def __add__(self, other): return self._delegate_operation(lambda x, y: x + y, other)
    def __sub__(self, other): return self._delegate_operation(lambda x, y: x - y, other)
    def __mul__(self, other): return self._delegate_operation(lambda x, y: x * y, other)
    def __truediv__(self, other): return self._delegate_operation(lambda x, y: x / y, other)
    def __floordiv__(self, other): return self._delegate_operation(lambda x, y: x // y, other)
    def __mod__(self, other): return self._delegate_operation(lambda x, y: x % y, other)
    def __pow__(self, other): return self._delegate_operation(lambda x, y: x ** y, other)

    # Define reverse mathematical operations
    def __radd__(self, other): return self._delegate_operation(lambda x, y: x + y, other, reverse=True)
    def __rsub__(self, other): return self._delegate_operation(lambda x, y: x - y, other, reverse=True)
    def __rmul__(self, other): return self._delegate_operation(lambda x, y: x * y, other, reverse=True)
    def __rtruediv__(self, other): return self._delegate_operation(lambda x, y: x / y, other, reverse=True)
    def __rfloordiv__(self, other): return self._delegate_operation(lambda x, y: x // y, other, reverse=True)
    def __rmod__(self, other): return self._delegate_operation(lambda x, y: x % y, other, reverse=True)
    def __rpow__(self, other): return self._delegate_operation(lambda x, y: x ** y, other, reverse=True)

    # Define comparison operations
    def __eq__(self, other): return self._delegate_operation(lambda x, y: x == y, other)
    def __lt__(self, other): return self._delegate_operation(lambda x, y: x < y, other)

    # Type conversion methods
    def __int__(self): return int(self._value)
    def __float__(self): return float(self._value)
    def __str__(self): return str(self._value)
    def __repr__(self): return repr(self._value)
    def __hash__(self): return hash(self._value)
    def __bool__(self): return bool(self._value)

    # Callable and container methods
    def __call__(self, *args, **kwargs):
        try:
            return self._value(*args, **kwargs)
        except Exception as e:
            logger.warning(e)
            return None

    def __len__(self):
        try:
            return len(self._value)
        except Exception as e:
            logger.warning(e)
            return 0

    def __iter__(self):
        try:
            return iter(self._value)
        except Exception as e:
            logger.warning(e)
            return iter([])

    def __getitem__(self, key):
        try:
            return self._value[key]
        except Exception as e:
            logger.warning(e)
            return None

    def __setitem__(self, key, value):
        try:
            self._value[key] = value
        except Exception as e:
            logger.warning(e)

    def __delitem__(self, key):
        try:
            del self._value[key]
        except Exception as e:
            logger.warning(e)

    def __contains__(self, item):
        try:
            return item in self._value
        except Exception as e:
            logger.warning(e)
            return False

    def __copy__(self):
        try:
            return LiveVariable(self.name, self._value)
        except Exception as e:
            logger.warning(e)
            return None