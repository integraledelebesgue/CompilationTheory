import sly
from sly.lex import Token
from typing import Any, Set
from functools import cached_property

#= 
# Ignore all the warnings concerning token constants and '@_'.
# They are defined at runtime by the 'sly' framework
# =#


class Lexer(sly.Lexer):
    tokens = {
        INT_NUMBER, FLOAT_NUMBER, STRING,
        ID, IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT, IN, FUNCTION,
        AND, OR, XOR, NOT,
        PLUS, MINUS, TIMES, DIVIDE, REMAINDER,
        DOT_PLUS, DOT_MINUS, DOT_TIMES, DOT_DIVIDE, DOT_REMAINDER,
        ASSIGN, PLUS_ASSIGN, MINUS_ASSIGN, TIMES_ASSIGN, DIVIDE_ASSIGN, REMAINDER_ASSIGN,
        EQUAL, NOT_EQUAL, GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL
    }

    @classmethod
    def binary_operators(cls) -> Set[str]: 
        return cls.arithmetic_operators() | cls.relational_operators() | cls.logical_operators()

    @classmethod
    def arithmetic_operators(cls) -> Set[str]:
        return {
            cls.PLUS, cls.MINUS, cls.TIMES, cls.DIVIDE, cls.REMAINDER,
            cls.DOT_PLUS, cls.DOT_MINUS, cls.DOT_TIMES, cls.DOT_DIVIDE, cls.DOT_REMAINDER,
            ':'
        }

    @classmethod
    def logical_operators(cls) -> Set[str]:
        return {
            cls.AND, cls.OR, cls.XOR
        }

    @classmethod
    def unary_operators(cls) -> Set[str]: 
        return {
            cls.NOT, "'"
        }

    @classmethod
    def relational_operators(cls) -> Set[str]:
        return {
            cls.EQUAL, cls.NOT_EQUAL, cls.GREATER, cls.GREATER_EQUAL, cls.LOWER, cls.LOWER_EQUAL, cls.IN
        }

    @classmethod
    def assigns(cls) -> Set[str]:
        return {
            cls.ASSIGN, cls.PLUS_ASSIGN, cls.MINUS_ASSIGN, cls.TIMES_ASSIGN, cls.DIVIDE_ASSIGN, cls.REMAINDER_ASSIGN
        }

    literals = {
        '{', '}', '[', ']', '(', ')', 
        ';', ':', '.', ',', 
        "'", '"',
    #    '+', '-', '*', '/',
    #    '<', '>', '=',
    }

    ignore = ' \t'
    ignore_comment = r'\#.*'

    PLUS_ASSIGN = r'\+='
    MINUS_ASSIGN = r'\-='
    TIMES_ASSIGN = r'\*='
    DIVIDE_ASSIGN = r'/='
    REMAINDER_ASSIGN = r'%='

    DOT_PLUS = r'\.\+'
    DOT_MINUS = r'\.-'
    DOT_TIMES = r'\.\*'
    DOT_DIVIDE = r'\./'
    DOT_REMAINDER = r'\.%'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    REMAINDER = r'%'
    
    EQUAL = r'=='
    NOT_EQUAL = r'!='
    GREATER_EQUAL = r'>='
    GREATER = r'>'
    LOWER_EQUAL = r'<='
    LOWER = r'<'

    ASSIGN = r'='

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT
    ID['and'] = AND
    ID['or'] = OR
    ID['xor'] = XOR
    ID['not'] = NOT
    ID['in'] = IN
    ID['function'] = FUNCTION

    STRING = r'\".*?\"'

    @_(r'\d*\.\d+')
    def FLOAT_NUMBER(self, token: Token) -> Token:
        token.value = float(token.value)
        return token

    @_(r'\d+')
    def INT_NUMBER(self, token: Token) -> Token:
        token.value = int(token.value)
        return token

    @_(r'\n+')
    def ignore_newline(self, token: Token) -> None:
        self.lineno += len(token.value);

    def error(self, t: Any):
        print(f"Illegal character in line {self.lineno}: '{t.value[0]}'")
        self.index += 1

