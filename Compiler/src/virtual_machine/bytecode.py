from enum import Enum, auto

class StackMarker(Enum):
    BEGIN_LOOP = auto()
    END_LOOP = auto()
    RETURN = auto()


class Operation(Enum):
    PUSH = auto()
    POP = auto()
    CLONE = auto()
    SWAP = auto()

    STORE_NAME = auto()
    LOAD_NAME = auto()

    JUMP = auto()
    JUMP_IF_FALSE = auto()
    JUMP_TOP = auto()
    JUMP_TOP_IF_FALSE = auto()

    RETURN = auto()

    CLEAR_LOOP = auto()

    APPEND = auto()
    LEN = auto()

    MAKE_LIST = auto()
    MAKE_ITER = auto()
    MAKE_ENUMERATE = auto()
    MAKE_CONST_SEQUENCE = auto()

    ITER_NEXT = auto()

    SUBSCRIPT_WRITE = auto()
    SUBSCRIPT_READ = auto()

    CALL = auto()

    SWITCH_CONTEXT = auto()
    DROP_CONTEXT = auto()

    BINARY_OP = auto()
    BINARY_OP_TOP = auto()

    UNARY_OP = auto()

    INCREMENT = auto()
    DECREMENT = auto()

    PRINT = auto()
    PRINT_STACK = auto()

    def __repr__(self) -> str:
        return self._name_
    