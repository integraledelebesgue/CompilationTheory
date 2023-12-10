from typing import Callable, Any
from virtual_machine.bytecode import Operation

def make_broadcast(bases: dict[str, Callable[[Any, Any], Any]], operator: str) -> Callable[[list[Any], list[Any]], list[Any]]:
    def broadcast(l1: list[Any], l2: list[Any]):
        if isinstance(l1, list):
            return [
                broadcast(e1, e2) 
                for e1, e2 in zip(l1, l2)
            ]
        
        function = bases[operator]

        return [function(e1, e2) for e1, e2 in zip(l1, l2)]
    
    return broadcast


binary_ops = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
    'and': lambda x, y: x and y,
    'or': lambda x, y: x or y,
    'xor': lambda x, y: x ^ y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '<=': lambda x, y: x <= y,
    '>=': lambda x, y: x >= y,
}

broadcasts = {
    '.' + operator: make_broadcast(binary_ops, operator) 
    for operator in binary_ops.keys()
}

binary_ops = {
    **binary_ops,
    **broadcasts
}


class Iterator:
    gen: Callable[[int], Any]
    current: int
    stop: int
    exhausted: bool

    def __init__(self, gen: Callable[[int], Any], start: int, stop: int) -> None:
        self.gen = gen
        self.current = start
        self.stop = stop
        self.exhausted = False

    def next(self) -> Any:
        element = self.gen(self.current)
        self.current += 1

        if self.current == self.stop:
            self.exhausted = True

        return element


make_zeros = [  # m & n lay on stack
    (Operation.STORE_NAME, 'm'),
    (Operation.STORE_NAME, 'n'),

    (Operation.MAKE_LIST),

    (Operation.PUSH, lambda x: x),
    (Operation.PUSH, 0),
    (Operation.LOAD_NAME, 'n'),
    (Operation.MAKE_ITER),

    (Operation.ITER_NEXT, -1, 14),
    (Operation.POP),
    (Operation.MAKE_LIST),

    (Operation.PUSH, lambda x: x),
    (Operation.PUSH, 0),
    (Operation.LOAD_NAME, 'm'),
    (Operation.MAKE_ITER),

    (Operation.ITER_NEXT, -1, 5),
    (Operation.POP),
    (Operation.PUSH, 0),
    (Operation.APPEND, -3),
    (Operation.JUMP, -4),

    (Operation.APPEND, -3),
    (Operation.JUMP, -13),

    Operation.RETURN
]

make_zeros_vector = [
    (Operation.STORE_NAME, 'n'),

    (Operation.PUSH, lambda _: 0),
    (Operation.PUSH, 0),
    (Operation.LOAD_NAME, 'n'),
    (Operation.MAKE_ITER),

    (Operation.MAKE_LIST),

    (Operation.ITER_NEXT, -2, 3),
    (Operation.APPEND, -2),
    (Operation.JUMP, -2),

    (Operation.RETURN),
]

make_ones = [  # m & n lay on stack
    (Operation.STORE_NAME, 'm'),
    (Operation.STORE_NAME, 'n'),

    (Operation.MAKE_LIST),

    (Operation.PUSH, lambda x: x),
    (Operation.PUSH, 0),
    (Operation.LOAD_NAME, 'n'),
    (Operation.MAKE_ITER),

    (Operation.ITER_NEXT, -1, 14),
    (Operation.POP),
    (Operation.MAKE_LIST),

    (Operation.PUSH, lambda x: x),
    (Operation.PUSH, 0),
    (Operation.LOAD_NAME, 'm'),
    (Operation.MAKE_ITER),

    (Operation.ITER_NEXT, -1, 5),
    (Operation.POP),
    (Operation.PUSH, 1),
    (Operation.APPEND, -3),
    (Operation.JUMP, -4),

    (Operation.APPEND, -3),
    (Operation.JUMP, -13),

    Operation.RETURN
]

make_eye = [  # n lay on stack
    (Operation.STORE_NAME, 'n'),

    (Operation.MAKE_LIST),
    (Operation.STORE_NAME, 'array'),

    (Operation.PUSH, lambda n: n),
    (Operation.PUSH, 0),
    (Operation.LOAD_NAME, 'n'),
    (Operation.MAKE_ITER),

    # outer loop begin
    (Operation.PUSH, lambda n: 0),
    (Operation.PUSH, 0),
    (Operation.LOAD_NAME, 'n'),
    (Operation.MAKE_ITER),

    (Operation.MAKE_LIST),

    # inner loop begin
    (Operation.ITER_NEXT, -2, 3),
    (Operation.APPEND, -2),
    (Operation.JUMP, -2),
    # inner loop end

    (Operation.ITER_NEXT, -2, 8),
    (Operation.PUSH, 1),
    (Operation.SUBSCRIPT_WRITE),

    (Operation.LOAD_NAME, 'array'),
    (Operation.SWAP),
    (Operation.APPEND, -2),
    (Operation.STORE_NAME, 'array'),
    (Operation.JUMP, -15),
    #outer loop end

    (Operation.LOAD_NAME, 'array'),
    (Operation.RETURN)
]

vec_binary = [
    # implementation
    (Operation.STORE_NAME, 'operator'),

    (Operation.LEN, -1),
    (Operation.STORE_NAME, 'len'),

    (Operation.STORE_NAME, 'v1'),
    (Operation.STORE_NAME, 'v2'),

    (Operation.LOAD_NAME, 'len'),
    (Operation.PUSH, 'zeros_vec'),
    (Operation.CALL, 1),
    (Operation.STORE_NAME, 'result'),

    (Operation.PUSH, lambda n: n),
    (Operation.PUSH, 0),
    (Operation.LOAD_NAME, 'len'),
    (Operation.MAKE_ITER),

    # loop begin
    (Operation.ITER_NEXT, -1, 21),
    (Operation.STORE_NAME, 'i'),

    (Operation.LOAD_NAME, 'v1'),
    (Operation.LOAD_NAME, 'i'),
    (Operation.SUBSCRIPT_READ),
    (Operation.SWAP),
    (Operation.POP),
    
    (Operation.LOAD_NAME, 'v2'),
    (Operation.LOAD_NAME, 'i'),
    (Operation.SUBSCRIPT_READ),
    (Operation.SWAP),
    (Operation.POP),

    (Operation.LOAD_NAME, 'operator'),
    (Operation.BINARY_OP_TOP),

    (Operation.LOAD_NAME, 'result'),
    (Operation.SWAP),
    (Operation.LOAD_NAME, 'i'),
    (Operation.SWAP),
    (Operation.SUBSCRIPT_WRITE),
    (Operation.POP),
    (Operation.JUMP, -20),

    (Operation.LOAD_NAME, 'result'),
    (Operation.RETURN),
]

context = {
    'zeros': make_zeros,
    'zeros_vec': make_zeros_vector,
    'ones': make_ones,
    'eye': make_eye,
    'vec_binary': vec_binary,
}
