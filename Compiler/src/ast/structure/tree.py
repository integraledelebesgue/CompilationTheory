from typing import Any, Optional, Literal
from dataclasses import dataclass


@dataclass
class Node:
    pass

@dataclass
class Statement(Node):
    pass

@dataclass
class Expression(Node):
    value: Any
    type: Optional[str]

@dataclass
class BinaryExpression(Expression):
    left: Optional[Expression] = None
    right: Optional[Expression] = None
    operator: Literal
    
@dataclass
class Subscription(Expression):
    source: Expression
    index: Expression

@dataclass
class RelationalExpression(BinaryExpression):
    pass

@dataclass
class Assignment(Statement):
    left: Expression
    right: Expression
    operator: str

@dataclass
class Condition(Expression):
    pass

@dataclass
class While(Statement):
    condition: Condition
    action: Statement

@dataclass
class For(Statement):
    iterator: Any
    range: Expression
    action: Statement

