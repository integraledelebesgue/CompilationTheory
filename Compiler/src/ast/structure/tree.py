from typing import get_args, Any, Optional, Literal, Set
from dataclasses import dataclass

import sys

sys.path.append('src')

from lexer import Lexer

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


# BinaryOperator = Literal[
#     '+', '.+', '-', '.-', '*', '.*', '/', './', '%', '.%', 
#     '<', '<=', '>', '>=', '==', '!=', 
#     'and', 'or', 'xor', 
#     'in', ':'
# ]

BinaryOperator = Literal[*Lexer.binary_operators()]

@dataclass
class BinaryExpression(Expression):
    left: Optional[Expression] = None
    right: Optional[Expression] = None
    operator: BinaryOperator
    

@dataclass
class Subscription(Expression):
    source: Expression
    index: Expression


RelationalOperator = Literal['<', '<=', '>', '>=', '==', '!=', 'in']

@dataclass
class RelationalExpression(BinaryExpression):
    operator: RelationalOperator


AssignOperator = Literal['=', '+=', '*=', '/=', '%=']

@dataclass
class Assign(Statement):
    left: Expression
    right: Expression
    operator: AssignOperator


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

