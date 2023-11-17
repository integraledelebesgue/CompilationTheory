from typing import Any, Optional, List, Dict, Tuple, Literal
from dataclasses import dataclass
from utilities.colors import ANSII
from syntax_tree.structure.observable import ObservableNode


@dataclass
class Node:
    pass


@dataclass
class Action(Node):
    pass


@dataclass
class Statement(Action):
    pass


@dataclass
class Block(Action, metaclass=ObservableNode, recursive=['actions']):
    actions: list[Action]


@dataclass()
class Program(Node, metaclass=ObservableNode, recursive=['content']):
    content: Block


@dataclass
class Identifier(Node, metaclass=ObservableNode, simple=['name', 'type']):
    name: str
    type: Optional[str] = None


@dataclass
class Expression(Node, metaclass=ObservableNode, simple=['value', 'type']):
    value: Any
    type: Optional[str]


@dataclass
class ExpressionList(Node, metaclass=ObservableNode, recursive=['elements']):
    elements: List[Expression]


@dataclass
class Vector(ExpressionList, metaclass=ObservableNode, inline=['length']):
    length: int


@dataclass
class Matrix(Expression, metaclass=ObservableNode, simple=['shape']):
    elements: List[Vector]
    shape: Tuple[int, int]


@dataclass
class UnaryExpression(Expression, metaclass=ObservableNode, simple=['operator'], recursive=['operand']):
    operator: str
    operand: Expression


@dataclass
class BinaryExpression(Expression, metaclass=ObservableNode, inline=['operator'], simple=['broadcast'], recursive=['left', 'right']):
    operator: str
    left: Optional[Expression]
    right: Optional[Expression]
    broadcast: bool = False

    def __post_init__(self):
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
class Range(Expression, metaclass=ObservableNode, recursive=['start', 'end']):
    start: Expression
    end: Expression


@dataclass
class Subscription(Expression, metaclass=ObservableNode, recursive=['source', 'index']):
    source: Expression
    index: Expression


@dataclass
class Call(Expression, metaclass=ObservableNode, recursive=['function', 'parameters']):
    function: Expression
    parameters: ExpressionList


@dataclass
class BuiltinCall(Call):  # Useless, delete as soon as modules with builtin functions are introduced
    pass


@dataclass
class Assignment(Statement, metaclass=ObservableNode, inline=['operator'], recursive=['left', 'right']):
    operator: str
    left: Expression
    right: Expression
    


@dataclass
class If(Statement, metaclass=ObservableNode, recursive=['condition', 'body', 'else_body']):
    condition: Expression
    body: Block
    else_body: Optional[Block]


@dataclass
class While(Statement, metaclass=ObservableNode, recursive=['condition', 'body']):
    condition: Expression
    body: Block


@dataclass
class For(Statement, metaclass=ObservableNode, recursive=['iterator', 'range', 'body']):
    iterator: Any
    range: Expression
    body: Block


@dataclass
class Function(Statement, metaclass=ObservableNode, inline=['name'], recursive=['arguments', 'body']):
    name: str
    arguments: ExpressionList
    body: Block


@dataclass
class Return(Statement, metaclass=ObservableNode, recursive=['value', 'type', 'expression']):
    value: Any
    type: Optional[str]
    expression: Optional[Expression]


@dataclass
class Control(Statement, metaclass=ObservableNode, inline=['type'], recursive=['expression']):  # break, continue, throw etc.
    type: Literal['break', 'continue']
    expression: Optional[Expression]
