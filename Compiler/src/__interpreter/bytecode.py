from enum import Enum

# class EnumDict(dict):
#     def __init__(self) -> None:
#         self.counter = itertools.count()

#     def __getitem__(self, key: Any) -> Any:
#         if key not in self:
#             self[key] = self.counter.__next__()

#         return super().__getitem__(key)
    

# class MetaEnum(type):
#     def __prepare__(name, bases):
#         return EnumDict()


# class Enum(metaclass=MetaEnum):
#     pass


class Operation(Enum):
    PUSH = 1
    POP = 2
    CLONE = 3
    STORE_NAME = 4
    LOAD_NAME = 5
    RETURN = 6
    MAKE_LIST = 7
    APPEND = 8
    MAKE_ITER = 9
    ITER_NEXT = 10
    SWITCH_CONTEXT = 14
    DROP_CONTEXT = 15
    BINARY_OP = 16
    BINARY_OP_TOP = 69
    CALL = 17
    SUBSCRIPT_WRITE = 18
    SUBSCRIPT_READ = 19
    SWAP_TOP = 25
    PRINT = 30
    PRINT_STACK = 31
    JUMP = 41
    JUMP_IF_FALSE = 42
    JUMP_TOP = 43
    JUMP_TOP_IF_FALSE = 44
    LEN = 51
    DECREMENT = 61
    



