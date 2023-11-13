from typing import Any, Optional, List, Dict, Tuple, Literal
from dataclasses import dataclass
from utilities.colors import ANSII


def abstract(cls):
    return cls


@abstract
@dataclass
class Node:
    pass


@abstract
@dataclass
class Action(Node):
    pass


@abstract
@dataclass
class Statement(Action):
    pass


@dataclass()
class Program:
    actions: List[Action]

    
@dataclass
class Identifier(Node):
    name: str
    type: Optional[str] = None


@abstract
@dataclass
class Expression(Node):
    value: Any
    type: Optional[str]


@dataclass
class ExpressionList(Node):
    elements: List[Expression]
    types: List[str]


@dataclass
class Vector(ExpressionList):
    length: int
    pass


@dataclass
class Matrix(Expression):
    value: List[Vector]
    shape: Tuple[int, int]


@dataclass
class UnaryExpression(Expression):
    operator: str
    operand: Expression


@dataclass
class BinaryExpression(Expression):
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
class Range(Expression):
    start: Expression
    end: Expression


@dataclass
class Subscription(Expression):
    source: Expression
    index: Expression


@dataclass
class Call(Expression):
    function: Expression
    parameters: ExpressionList


@dataclass
class BuiltinCall(Call):  # Useless, delete as soon as modules with builtin functions are introduced
    pass


@dataclass
class Assignment(Statement):
    operator: str
    left: Expression
    right: Expression
    


@dataclass
class If(Statement):
    condition: Expression
    body: List[Statement]
    else_body: Optional[List[Statement]]


@dataclass
class While(Statement):
    condition: Expression
    body: List[Statement]


@dataclass
class For(Statement):
    iterator: Any
    range: Expression
    body: List[Statement]


@dataclass
class Arguments:
    names: List[str]
    types: List[Optional[str]]
    default_values: List[Optional[Expression]]


@dataclass
class Function(Statement):
    name: str
    arguments: Arguments
    body: List[Statement]


@dataclass
class Return(Statement):
    value: Any
    type: Optional[str]
    expression: Optional[Expression]


@dataclass
class Control(Statement):  # break, continue, throw etc.
    type: Literal['break', 'continue']
    expression: Optional[Expression]
