from typing import *

def addToClass(cls):
    def wrapper(function: Callable) -> Callable:
        setattr(cls, function.__name__, function)
        return function
    
    return wrapper
