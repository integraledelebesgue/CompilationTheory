from typing import Any, Optional, List, Dict, Tuple
from dataclasses import dataclass


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
class Program:
    actions: List[Action]


@dataclass
class Expression(Node):
    value: Any
    type: Optional[str]


@dataclass
class UnaryExpression(Expression):
    operator: str
    operand: Expression


@dataclass
class BinaryExpression(Expression):
    operator: str
    left: Optional[Expression]
    right: Optional[Expression]
    

@dataclass
class Subscription(Expression):
    source: Expression
    index: Expression


@dataclass
class Call(Expression):
    function: Expression
    parameters: List[Expression]


@dataclass
class RelationalExpression(BinaryExpression):
    pass


@dataclass
class AssignStatement(Statement):
    operator: str
    left: Expression
    right: Expression
    

@dataclass
class Condition(Expression):
    pass


@dataclass
class WhileStatement(Statement):
    condition: Condition
    body: List[Statement]


@dataclass
class ForStatement(Statement):
    iterator: Any
    range: Expression
    body: List[Statement]


@dataclass
class FunctionDefinition(Statement):
    name: str
    parameters: Dict[str, Tuple[str, Expression]]
    body: List[Statement]