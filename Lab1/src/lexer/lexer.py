from sly import Lexer
from sly.lex import Token
from typing import Any


class Scanner(Lexer):
    tokens = {
        INT_NUMBER, FLOAT_NUMBER,
        ID, IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT,
        PLUS, MINUS, TIMES, DIVIDE,
        DOT_PLUS, DOT_MINUS, DOT_TIMES, DOT_DIVIDE, DOT,
        PLUS_ASSIGN, MINUS_ASSIGN, TIMES_ASSIGN, DIVIDE_ASSIGN,
        EQUAL, NOT_EQUAL, GREATER_EQUAL, GREATER, LOWER_EQUAL, LOWER, ASSIGN
    }

    literals = {'{', '}', '[', ']', '(', ')', ';', ':', "'", '"'}

    ignore = ' \t'
    ignore_comment = r'\#.*'

    PLUS_ASSIGN = r'\+='
    MINUS_ASSIGN = r'\-='
    TIMES_ASSIGN = r'\*='
    DIVIDE_ASSIGN = r'/='

    DOT_PLUS = r'\.\+'
    DOT_MINUS = r'\.-'
    DOT_TIMES = r'\.\*'
    DOT_DIVIDE = r'\./'
    DOT = r'\.'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    
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

    @_(r'\d+')
    def INT_NUMBER(self, token: Token) -> Token:
        token.value = int(token.value)
        return token

    @_(r'\d*\.\d+')
    def FLOAT_NUMBER(self, token: Token) -> Token:
        token.value = float(token.value)
        return token

    @_(r'\n+')
    def ignore_newline(self, token: Token) -> None:
        self.lineno += len(token.value);

    def error(self, t: Any):
        print(f"Illegal character in line {self.lineno}: '{t.value[0]}'")
        self.index += 1

