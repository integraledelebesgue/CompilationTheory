from typing import Any, Optional, Sequence
from itertools import count
from virtual_machine.bytecode import *
import virtual_machine.stdlib as std


class FrameState:
    FINISH = 0
    CALL = 1


class Frame:
    instances = count()
    id: int

    vm: 'VirtualMachine'
    context: dict[str, Any]
    code: list[Any]
    stack: list[Any]  # TODO precise typing
    debug: bool
    execution: Sequence[FrameState]

    def __init__(self, vm: 'VirtualMachine', context: dict[str, Any], code: list['Any'], *, debug: bool = False) -> None:
        self.id = next(Frame.instances)
        self.vm = vm
        self.context = context
        self.code = code
        self.stack = []
        self.debug = debug
        self.execution = self.execute()

    def __hash__(self) -> int:
        return hash(self.id)

    def execute(self) -> Sequence[tuple[FrameState, Any]]:
        n = len(self.code)
        i = 0

        result = None

        while i < n:
            if self.debug:
                print(f'{self.stack}\n\n{self.code[i]}')

            match self.code[i]:
                case (Operation.PUSH, value):
                    self.stack.append(value)

                case Operation.POP:
                    self.stack.pop()

                case Operation.CLONE:
                    self.stack.append(self.stack[-1])

                case Operation.SWAP:
                    self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

                case (Operation.STORE_NAME, name):
                    self.context[name] = self.stack.pop()

                case (Operation.LOAD_NAME, name):
                    self.stack.append(self.context[name])

                case (Operation.JUMP, delta):
                    i += delta - 1

                case (Operation.JUMP_IF_FALSE, delta):
                    if not self.stack.pop():
                        i += delta - 1

                case Operation.RETURN:
                    result = self.stack[-2]\
                        if self.stack[-1] == StackMarker.RETURN\
                        else None
                    
                    break

                case Operation.CLEAR_LOOP:
                    while self.stack.pop() != StackMarker.BEGIN_LOOP:
                        pass 

                case (Operation.APPEND, offset):
                    self.stack[offset].append(self.stack.pop())

                case (Operation.LEN, offset):
                    self.stack.append(len(self.stack[offset]))

                case Operation.MAKE_LIST:
                    self.stack.append([])

                case Operation.MAKE_ENUMERATE:
                    end = self.stack.pop()
                    start = self.stack.pop()

                    self.stack.append(iter(range(start, end)))

                case (Operation.MAKE_CONST_SEQUENCE, value):
                    length = self.stack.pop()

                    self.stack.append((value for _ in range(length)))

                case (Operation.ITER_NEXT, offset, jump):
                    iterator = self.stack[offset]

                    match next(iterator):
                        case None:
                            i += jump - 1

                        case something:
                            self.stack.append(something)

                case (Operation.SUBSCRIPT_READ, n_indices):
                    indices = self.stack[-n_indices:]
                    self.stack[-n_indices:] = []

                    source = self.stack.pop()

                    deref = source

                    for index in reversed(indices):
                        deref = deref[index - 1]

                    self.stack.append(deref)

                case (Operation.SUBSCRIPT_WRITE, n_indices):
                    element = self.stack.pop()

                    indices = self.stack[-n_indices:]
                    self.stack[-n_indices:] = []

                    source = self.stack.pop()

                    deref = source

                    for index in reversed(indices[1:]):
                        deref = deref[index - 1]

                    deref[indices[0] - 1] = element

                case (Operation.CALL, n_args):
                    raise NotImplementedError('Function calls are not supported')
                    yield (FrameState.CALL, 'fun_name')

                case (Operation.BINARY_OP, operator):
                    left = self.stack.pop()
                    right = self.stack.pop()

                    result = std.binary_ops[operator](left, right)
                    self.stack.append(result)

                case (Operation.UNARY_OP, operator):
                    operand = self.stack.pop()

                    result = std.unary_ops[operator](operand)
                    self.stack.append(result)

                case Operation.INCREMENT:
                    self.stack[-1] += 1

                case Operation.DECREMENT:
                    self.stack[-1] -= 1

                case (Operation.PRINT, n_args):
                    args = self.stack[-n_args:]
                    print(*args, sep='\n')

                case Operation.PRINT_STACK:
                    print(*self.stack, sep='\n')

            i += 1

        if self.debug:
            print(self.stack)

        yield (FrameState.FINISH, result)


class VirtualMachine:
    call_stack: list[Frame]

    def __init__(self) -> None:
        self.call_stack = []

    def load(self, code: list[Any], *, debug: bool = False) -> None:
        initial = Frame(
            self, 
            dict(), 
            code,
            debug=debug
        )  # provide valid context etc.
        
        self.call_stack.append(initial)

    def run(self) -> None:
        while len(self.call_stack) > 0:
            frame = self.call_stack[-1]

            match next(frame.execution):
                case (FrameState.CALL, function):
                    pass

                case (FrameState.FINISH, None):
                    self.call_stack.pop()

                case (FrameState.FINISH, result):
                    self.call_stack.pop()
                    
                    if len(self.call_stack) > 0:
                        self.call_stack[-1].stack.append(result)

                    else:
                        print(f'Process finished with result {result}')

