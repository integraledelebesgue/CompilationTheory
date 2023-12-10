from typing import Any
import stdlib
from bytecode import Operation
from enum import Enum


class StackMarker(Enum):
    BEGIN_CALL = 1


class Interpreter:
    stack: list[Any]
    context: dict[str, Any]
    supercontexts: list[dict[str, Any]]

    def __init__(self) -> None:
        self.stack = []
        self.supercontexts = []
        self.context = stdlib.context

    def get(self, name: str) -> Any:
        if name in self.context:
            return self.context[name]
        
        for context in reversed(self.supercontexts):
            if name in context:
                return context[name]
            
    def switch_to(self, context: dict[str, Any]) -> None:
        self.supercontexts.append(self.context)
        self.context = context

    def drop_context(self) -> None:
        self.context = self.supercontexts.pop()

    def execute(self, code: list[Operation | tuple[Operation, Any]]):
        n = len(code)
        i = 0

        while i < n:
            print(self.stack)
            print()
            print(code[i])

            match code[i]:
                case (Operation.BINARY_OP, operator):
                    a = self.stack.pop()
                    b = self.stack.pop()
                    func = stdlib.binary_ops[operator]

                    self.stack.append(func(a, b))

                case Operation.BINARY_OP_TOP:
                    operator = self.stack.pop()
                    a = self.stack.pop()
                    b = self.stack.pop()
                    func = stdlib.binary_ops[operator]

                    self.stack.append(func(a, b))

                case (Operation.PUSH, val):
                    self.stack.append(val)

                case Operation.POP:
                    _ = self.stack.pop()
                
                case Operation.RETURN:
                    if self.stack[-1] == StackMarker.BEGIN_CALL:
                        self.stack.pop()
                        return
                    
                    to_return = self.stack[-1]
                    
                    while self.stack.pop() != StackMarker.BEGIN_CALL:
                        pass

                    self.stack.append(to_return)

                    # print(f'Returning {self.stack[-1]}')

                case Operation.MAKE_ITER:
                    stop = self.stack.pop()
                    start = self.stack.pop()
                    gen = self.stack.pop()

                    self.stack.append(stdlib.Iterator(gen, start, stop))

                case Operation.MAKE_LIST:
                    self.stack.append([])

                case (Operation.ITER_NEXT, offset, delta):
                    iterator = self.stack[offset]

                    if iterator.exhausted:
                        i += delta - 1
                        self.stack.pop(offset)  # reconsider this
                    else:
                        self.stack.append(iterator.next())

                case (Operation.CALL, argc):
                    func = self.get(self.stack.pop())
                    self.switch_to(dict())

                    self.stack.insert(-(argc + 1), StackMarker.BEGIN_CALL)
                    self.execute(func)
                    
                    self.drop_context()

                case Operation.SUBSCRIPT_READ:
                    index = self.stack.pop()
                    source = self.stack[-1]

                    self.stack.append(source[index])

                case Operation.SUBSCRIPT_WRITE:
                    element = self.stack.pop()
                    index = self.stack.pop()
                    source = self.stack[-1]

                    source[index] = element

                case (Operation.JUMP, offset):
                    i += offset - 1
                    # print(f'Jump to {code[i + 1]} at {i + 1}')

                case (Operation.JUMP_IF_FALSE, offset):
                    if self.stack.pop():
                        i += offset - 1

                case Operation.JUMP_TOP:
                    offset = self.stack.pop()
                    i += offset - 1

                case Operation.JUMP_TOP_IF_FALSE:
                    offset = self.stack.pop()
                    condition = self.stack.pop()

                    if condition:
                        i += offset - 1

                case (Operation.SWITCH_CONTEXT, context):
                    self.switch_to(context)

                case Operation.DROP_CONTEXT:
                    self.drop_context()

                case (Operation.STORE_NAME, name):
                    self.context[name] = self.stack.pop()

                case (Operation.LOAD_NAME, name):
                    self.stack.append(self.context[name])

                case (Operation.APPEND, offset):
                    self.stack[offset].append(self.stack.pop())

                case Operation.SWAP_TOP:
                    self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

                case (Operation.PRINT, argc):
                    for _ in range(argc):
                        print(self.stack.pop())

                case Operation.PRINT_STACK:
                    print(*self.stack, sep='\n')

                case (Operation.LEN, offset):
                    self.stack.append(len(self.stack[offset]))

                case (Operation.DECREMENT):
                    self.stack[-1] -= 1

            i += 1

        # print(self.stack)

program = [
    (Operation.PUSH, 1),
    (Operation.PUSH, 5),
    (Operation.PUSH, 'zeros'),
    (Operation.CALL, 2),
    (Operation.PRINT_STACK)
]

vector_op = [
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
    (Operation.SWAP_TOP),
    (Operation.POP),
    
    (Operation.LOAD_NAME, 'v2'),
    (Operation.LOAD_NAME, 'i'),
    (Operation.SUBSCRIPT_READ),
    (Operation.SWAP_TOP),
    (Operation.POP),

    (Operation.LOAD_NAME, 'operator'),
    (Operation.BINARY_OP_TOP),

    (Operation.LOAD_NAME, 'result'),
    (Operation.SWAP_TOP),
    (Operation.LOAD_NAME, 'i'),
    (Operation.SWAP_TOP),
    (Operation.SUBSCRIPT_WRITE),
    (Operation.POP),
    (Operation.JUMP, -20),

    (Operation.LOAD_NAME, 'result'),
    (Operation.RETURN),
]


Interpreter().execute(vector_op)
