from typing import get_type_hints, Any, Optional, Tuple, Literal, Sequence
from dataclasses import dataclass
from syntax_tree.structure.observable import ObservableNode
from semantics import dispatch
from itertools import count
from functools import cached_property
from semantics.types import *


class Scope:
    symbols: dict['Identifier', int]
    id: int
    parent: Optional['Scope']
    children: list['Scope']

    instances = count()

    def __init__(self) -> None:
        self.symbols = dict()
        self.id = Scope.instances.__next__()
        self.parent = None
        self.children = []

    def define(self, id: 'Identifier') -> None:
        self.symbols[id] = id.line

    def has_element_before(self, element: 'Identifier') -> bool:
        return any(e.name == element.name and e.line <= element.line for e in self.symbols.keys())
    
    def type(self, name: str) -> str:
        for element in self.symbols.keys():
            if element.name == name:
                return element.type

    def __repr__(self) -> str:
        return str(self.id)


@dataclass
class Node:
#   parent: Optional['Node'] - prototyped at runtime
#   owner: Optional['Scope']          -//-
#   structurized: bool                -//-

    def __post_init__(self) -> None:
        self.parent: Optional[Node] = None
        self.owner: Optional[Scope] = None
        self.structurized = False

        if self.defines_scope:
            self.scope = Scope()
            self.symbols = self.scope.symbols

    def structurize(self, parent: Optional['Node'] = None, owner: Optional['Scope'] = None) -> None:
        if self.structurized:
            return
    
        self.structurized = True
        self.parent = parent
        self.owner = owner

        next_owner = self.scope\
            if self.defines_scope\
            else owner

        if self.defines_self\
                and self.parent.defines_symbol\
                and not self.defined:
            self.owner.define(self)
        
        for child in self.children:
            child.structurize(self, next_owner)

    @property
    def children(self) -> Sequence['Node']:
        for name in list(vars(self)):
            match self.__getattribute__(name):
                case field if issubclass(field.__class__, Node):
                    yield field

                case fields if isinstance(fields, list):
                    for field in fields:
                        if issubclass(field.__class__, Node):
                            yield field

    @property
    def superscopes(self) -> Sequence[Scope]:
        parent = self.parent

        while parent is not None:
            if parent.defines_scope:
                yield parent.scope

            parent = parent.parent

        # parent = self.parent
        # previous = None

        # while parent is not None:
        #     if not parent.defines_scope:
        #         parent = parent.parent
        #         continue



        #     if previous is not None:
        #         previous.parent = parent.scope
        #         parent.scope.children.append(previous)

        #     previous = parent.scope
        #     parent = parent.parent

        #     yield previous


@dataclass
class Action(Node):
    pass


@dataclass
class Statement(Action):
    pass


@dataclass(repr=False)
class Block(
        Action, 
        metaclass=ObservableNode, 
        display={ 'inline': ['scope', 'symbols'], 'recursive': ['actions'] },
        defines={ 'scope': True }
):
    actions: list[Action]

    def check_types(self) -> None:
        for action in self.actions:
            action.check_types()


@dataclass
class Program(
        Node, 
        metaclass=ObservableNode, 
        display={ 'recursive': ['content'] }
):
    content: Block

    @property
    def superscopes(self) -> Sequence['Block']:
        yield self.content
        # return (self.content for _ in range(1))


@dataclass
class Identifier(
        Node, 
        metaclass=ObservableNode, 
        display={ 'inline': ['owner'], 'simple': ['name', 'type', 'line'] },
        typecheck={ 'source' : [] },
        defines={ 'self': True }
):
    name: str
    line: int
    type: Type = None

    @property
    def defined(self) -> bool:
        return any(
            self in scope.symbols and scope.symbols[self] < self.line 
            for scope in self.superscopes
        )

    def typing_hook(self) -> None:
        # if self.defined:
        #     self.type = 
        #     print(f'Identifier {self.fancy_repr} is defined in scope {self.scope}')
        #     return

        if self.owner.has_element_before(self):
            self.type = self.owner.type(self.name)
            return

        for scope in self.superscopes:
            if scope.has_element_before(self):
                self.type = scope.type(self.name)
                print(f'Identifier {self.fancy_repr} is defined in scope {scope}')
                return

        print(f'Identifier {self.fancy_repr} is undefined')

    @property
    def fancy_repr(self) -> str:
        return f'{self.name} [{self.line}]: {self.type}'

    def __hash__(self) -> int:
        return hash((self.name, self.line, self.type))


@dataclass
class Expression(
        Node, 
        metaclass=ObservableNode, 
        display={ 'simple': ['value', 'type'] }
):
    value: Any
    type: Type


@dataclass
class ExpressionList(
        Node, 
        metaclass=ObservableNode, 
        display={ 'recursive': ['elements'] }
):
    elements: list[Expression]


@dataclass
class Vector(
        ExpressionList, 
        metaclass=ObservableNode, 
        display={ 'inline': ['length'], 'simple': ['type'] },
        typecheck={ 'source': ['elements'] }
):
    type: Optional[str]
    length: int
    element_type: Type = None

    def typing_hook(self) -> None:
        type = self.type[0]

        if any(element != type for element in self.type):
            raise Exception('')  # TODO precise error
        
        self.element_type = type
        self.type = Collection('vector', type)


@dataclass
class Matrix(
        Expression, 
        metaclass=ObservableNode, 
        display={ 'inline': ['shape'], 'recursive': ['rows'] },
        typecheck={ 'source': ['rows'] }
):
    rows: list[Vector]
    shape: Tuple[int, int]
    element_type: Type = None

    def typing_hook(self) -> None:
        type = self.type[0]

        if any(element != type for element in self.type):
            raise Exception('')  # TODO precise error
        
        type = self.rows[0].element_type

        self.element_type = type
        self.type = Collection('matrix', type)


@dataclass
class UnaryExpression(
        Expression, 
        metaclass=ObservableNode, 
        display={ 'simple': ['operator'], 'recursive': ['operand'] },
        typecheck={ 'source': ['operand'] },
        dispatch={ 'key': 'operator', 'table': dispatch.expressions['unary'] }
):
    operator: str
    operand: Expression


@dataclass
class BinaryExpression(
        Expression, 
        metaclass=ObservableNode, 
        display={ 'inline': ['operator'], 'simple': ['broadcast'], 'recursive': ['left', 'right'] },
        typecheck={ 'source': ['left', 'right'] },
        dispatch={ 'key': 'operator', 'table': dispatch.expressions['binary'] }
):
    operator: str
    left: Optional[Expression]
    right: Optional[Expression]
    broadcast: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.broadcast = '.' in self.operator


@dataclass
class RelationalExpression(BinaryExpression):
    pass


@dataclass
class ArithmeticExpression(BinaryExpression):
    pass


@dataclass
class LogicalExpression(BinaryExpression):
    pass


@dataclass
class Range(
        Expression, 
        metaclass=ObservableNode, 
        display={ 'recursive': ['start', 'end'] },
        typecheck={ 'source': ['start', 'end'] },
        dispatch={ 'key': 'interval', 'table': dispatch.expressions['range'] }  # unit range is default by now
):
    start: Expression
    end: Expression
    interval: str = 'unit'


@dataclass
class Subscription(
        Expression, 
        metaclass=ObservableNode, 
        display={ 'recursive': ['source', 'index'] },
        typecheck={ 'source': ['source'] }
):
    source: Expression
    index: Expression

    def typing_hook(self) -> None:
        self.type = self.source.type


@dataclass
class Call(
        Expression, 
        metaclass=ObservableNode, 
        display={ 'recursive': ['function', 'parameters'] },
        dispatch={ 'key': 'name', 'table': 'functions' }
):
    function: Expression
    parameters: ExpressionList
#   name: str

    def __post_init__(self) -> None:
        super().__post_init__()
        self.name = self.function.name


    def typing_hook(self) -> None:
        pass  # TODO check LUT or mark as 'any' to move checking to runtime


class Loop:
    pass


@dataclass
class Assignment(
        Statement,
        metaclass=ObservableNode, 
        display={ 'inline': ['operator'], 'recursive': ['left', 'right'] },
        typecheck={ 'source': ['right'], 'sink': ['left'] },
        defines={ 'symbol': True }
):
    operator: str
    left: Expression
    right: Expression

    def __post_init__(self) -> None:
        super().__post_init__()

    @cached_property
    def defines(self):
        return '=' in self.operator


@dataclass
class If(
        Statement,
        metaclass=ObservableNode, 
        display={ 'recursive': ['condition', 'body', 'else_body'] },
        typecheck={ 'source': ['condition'], 'sink': ['condition'] }
):
    condition: Expression
    body: Block
    else_body: Optional[Block]


@dataclass
class While(
        Statement, Loop,
        metaclass=ObservableNode, 
        display={ 'recursive': ['condition', 'body'] },
        typecheck={ 'source': ['condition'], 'sink': ['condition'] }
):
    condition: Expression
    body: Block


@dataclass
class For(
        Statement, Loop,
        metaclass=ObservableNode, 
        display={ 'inline': ['scope', 'symbols'], 'recursive': ['iterator', 'range', 'body'] },
        typecheck={ 'source': ['range'], 'sink': ['iterator'], 'decapsulate': True },
        defines={ 'symbol': True, 'scope': True }
):
    iterator: Any
    range: Expression
    body: Block


@dataclass
class Function(
        Statement,
        metaclass=ObservableNode, 
        display={ 'inline': ['name', 'scope'], 'recursive': ['arguments', 'body'] },
        defines={ 'symbol': True, 'scope': True }
):
    name: str
    arguments: ExpressionList
    body: Block


@dataclass
class Return(
        Statement, 
        metaclass=ObservableNode, 
        display={ 'recursive': ['value', 'type', 'expression'] },
        typecheck={ 'source': ['expression'] }
):
    value: Any
    type: Type
    expression: Optional[Expression]


@dataclass
class Control(
        Statement, 
        metaclass=ObservableNode, 
        display={ 'inline': ['instruction'], 'recursive': ['expression'] },
        typecheck={ 'source': ['expression'] }
):  # break, continue, throw etc.
    instruction: Literal['break', 'continue']
    expression: Optional[Expression] = None
    type: Type = nothing

    def typing_hook(self) -> None:
        if not issubclass(self.parent.__class__, Loop):
            print(f'Control statement "{self.instruction}" outside loop')
