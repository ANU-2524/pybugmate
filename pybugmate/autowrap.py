from .decorators import bugmate
import types

def autowrap(scope):
    for name, obj in scope.items():
        if isinstance(obj, types.FunctionType) and not name.startswith("__"):
            scope[name] = bugmate(obj)
