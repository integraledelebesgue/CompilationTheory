from typing import Callable, Any
from virtual_machine.bytecode import Operation, StackMarker
from syntax_tree.structure.nodes import *
from functools import singledispatch
import virtual_machine.stdlib

class Placeholder:
    BREAK = 0
    CONTINUE = 1


def disassemble(code: list[Operation]) -> str:
    line_width = int(len(max(Operation._member_names_, key=len)) * 1.5)

    representation = ''

    for command in code:
        match command:
            case (op, *args):
                name = op.__repr__()
                spaces = line_width - len(name)
                
                if isinstance(args[0], int) and args[0] < 0:
                    spaces -= 1

                representation += name + spaces * ' ' + ', '.join(map(str, args)) + '\n'

            case op:
                representation += op.__repr__() + '\n'

    return representation


@singledispatch
def compile(node: Node) -> list[Operation]:
    raise NotImplementedError(f'Not implemented for {node.__class__.__name__}')


@compile.register
def _(node: Program) -> list[Operation]:
    return compile(node.content)


@compile.register
def _(node: Block) -> list[Operation]:
    return sum((compile(action) for action in node.actions), start=[])


@compile.register
def _(node: Identifier) -> list[Operation]:
    return [
        (Operation.LOAD_NAME, node.name)
    ]


@compile.register
def _(node: Expression) -> list[Operation]:
    return [
        (Operation.PUSH, node.value)
    ]


@compile.register
def _(node: Vector) -> list[Operation]:
    operations = [
        [(Operation.PUSH, element.value),
        (Operation.APPEND, -2)]
        for element in node.elements
    ]
    
    return sum(operations, start=[Operation.MAKE_LIST])


@compile.register
def _(node: Matrix) -> list[Operation]:
    vectors = map(
        lambda vec: compile(vec) + [(Operation.APPEND, -2)], 
        node.rows
    )

    return sum(vectors, start=[Operation.MAKE_LIST])


@compile.register
def _(node: UnaryExpression):
    return [
        (Operation.LOAD_NAME, node.operand.name),
        (Operation.UNARY_OP, node.operator)
    ]


@compile.register
def _(node: BinaryExpression) -> list[Operation]:
    return [
        *compile(node.left),
        *compile(node.right),
        (Operation.BINARY_OP, node.operator)
    ]


@compile.register
def _(node: Range) -> list[Operation]:
    return [
        (Operation.PUSH, lambda n: n),
        *compile(node.start),
        *compile(node.end),
        Operation.MAKE_ITER
    ]


@compile.register
def _(node: Subscription) -> list[Operation]:
    if not isinstance(node.index, ExpressionList):
        return [
            *compile(node.source),
            *compile(node.index),
            (Operation.SUBSCRIPT_READ, 1)
        ]
    
    indices = [compile(e) for e in node.index.elements]
    n = len(indices)

    indices = sum(indices, start=[])

    return [
        *compile(node.source),
        *indices,
        (Operation.SUBSCRIPT_READ, n)
    ]


@compile.register
def _(node: Call) -> list[Operation]:
    args = sum((compile(p) for p in node.parameters.elements), start=[])
    
    return [
        *args,
        (Operation.PUSH, node.name),
        (Operation.CALL, len(args))
    ]


@compile.register
def _(node: Assignment) -> list[Operation]:
    operator = node.operator

    match node.left:
        case sub if isinstance(sub, Subscription):
            if isinstance(sub.index, ExpressionList):
                n_indices = len(sub.index.elements)
                indices = sum((
                    compile(element)
                    for element in sub.index.elements
                ), start=[])

            else:
                n_indices = 1
                indices = compile(sub.index)

            if operator == '=':
                return [
                    *compile(sub.source),
                    *indices,
                    *compile(node.right),
                    (Operation.SUBSCRIPT_WRITE, n_indices)
                ]
            
            names = [
                f'__local_index_{i}'
                for i in range(n_indices)
            ]
            
            store_indices = sum((
                [compute, 
                (Operation.STORE_NAME, name)]
                for compute, name in zip(indices, names)
            ), start=[])

            load_indices = [
                (Operation.LOAD_NAME, name)
                for name in reversed(names)
            ]
            
            return [
                *compile(sub.source),
                *store_indices,
                *load_indices,
                (Operation.SUBSCRIPT_READ, n_indices),
                *compile(node.right),
                (Operation.BINARY_OP, operator[0]),
                (Operation.STORE_NAME, '__local_element'),
                *load_indices,
                (Operation.LOAD_NAME, '__local_element'),
                (Operation.SUBSCRIPT_WRITE, n_indices)
            ]

        case id if isinstance(id, Identifier) and operator == '=':
            return [
                *compile(node.right),
                (Operation.STORE_NAME, id.name)
            ]

        case id if isinstance(id, Identifier):
            return [
                (Operation.LOAD_NAME, id.name),
                *compile(node.right),
                (Operation.BINARY_OP, operator[0]),
                (Operation.STORE_NAME, id.name),
            ]


@compile.register
def _(node: If) -> list[Operation]:
    true_block = compile(node.body)
    false_block = []\
        if node.else_body is None\
        else compile(node.else_body)

    return [
        *compile(node.condition),
        (Operation.JUMP_IF_FALSE, len(true_block) + 1),
        *true_block,
        *false_block
    ]


@compile.register
def _(node: Control) -> list[Operation]:
    match node.instruction:
        case 'break':
            return [(Operation.JUMP, Placeholder.BREAK)]

        case 'continue':
            return [(Operation.JUMP, Placeholder.CONTINUE)]
        

@compile.register
def _(node: ExpressionList) -> list[Operation]:  # happens only in return
    if len(node.elements) == 1:
        return compile(node.elements[0])

    code = [Operation.MAKE_LIST]

    for element in node.elements:
        code.extend(compile(element))
        code.append((Operation.APPEND, -2))

    return code

        
@compile.register
def _(node: Return) -> list[Operation]:
    if node.expression is None:
        return [Operation.RETURN]

    return [
        *compile(node.expression),
        (Operation.PUSH, StackMarker.RETURN),
        Operation.RETURN
    ]


@compile.register
def _(node: While) -> list[Operation]:
    condition = compile(node.condition)
    body = compile(node.body)

    condition_jump = len(condition) + 1
    backward_jump = condition_jump + len(body)

    body.append((Operation.JUMP, -backward_jump))
    end = len(body)
    
    for i, element in enumerate(body): 
        match element:
            case (Operation.JUMP, Placeholder.BREAK):
                body[i] = (Operation.JUMP, end - i)

            case (Operation.JUMP, Placeholder.CONTINUE):
                body[i] = (Operation.JUMP, -(i + condition_jump))

    return [
        (Operation.PUSH, StackMarker.BEGIN_LOOP),
        *condition,
        (Operation.JUMP_IF_FALSE, end),
        *body,
        (Operation.PUSH, StackMarker.END_LOOP),
        Operation.CLEAR_LOOP
    ]

# BEGIN_LOOP
# 1. condition
# 2
# 3
# 4 value lays on stack
# JUMP_IF_FALSE
# 1. body
# 2
# 3 continue (i = 2)
# 4 break (i = 3)
# 5
# 6 JUMP_BACK
# END_LOOP

@compile.register
def _(node: Range) -> list[Operation]:
    start = compile(node.start)
    stop = compile(node.end)

    return [
        *start,
        *stop,
        Operation.MAKE_ENUMERATE
    ]


@compile.register
def _(node: For) -> list[Operation]:
    range = compile(node.range)
    body = compile(node.body)

    n = len(body)

    body = [
        (Operation.ITER_NEXT, -1, n + 3),
        (Operation.STORE_NAME, node.iterator.name),       
        *body,
        (Operation.JUMP, -(n + 2)),
    ]

    n += 3

    for i, element in enumerate(body): 
        match element:
            case (Operation.JUMP, Placeholder.BREAK):
                body[i] = (Operation.JUMP, n - i)

            case (Operation.JUMP, Placeholder.CONTINUE):
                body[i] = (Operation.JUMP, -i)

    return [
        (Operation.PUSH, StackMarker.BEGIN_LOOP),
        *range,
        *body,
        (Operation.PUSH, StackMarker.END_LOOP),
        Operation.CLEAR_LOOP
    ]



