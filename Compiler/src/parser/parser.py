import sly
from sly.yacc import YaccProduction as Production
from lexer import Lexer
from syntax_tree.structure.nodes import *

class Parser(sly.Parser):
    debugfile = 'debug/parser_out.txt'

    tokens = Lexer.tokens

    precedence = (
        ('right', ASSIGN, PLUS_ASSIGN, MINUS_ASSIGN, TIMES_ASSIGN, DIVIDE_ASSIGN, REMAINDER_ASSIGN),
        ('nonassoc', ':'),
        ('left', AND, OR, XOR),
        ('left', EQUAL, NOT_EQUAL, GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL),
        ('left', PLUS, MINUS, DOT_PLUS, DOT_MINUS),
        ('left', TIMES, DIVIDE, REMAINDER, DOT_TIMES, DOT_DIVIDE, DOT_REMAINDER),
        ('right', UMINUS, UNEG),
        ('left', TRANSPOSE),
        ('left', CALL, SUBSCRIPT),  # may be obsolete, deleting considered
        ('nonassoc', SHORT_IF),
        ('nonassoc', ELSE)
    )

    _stack = None

    @property
    def stack(self) -> list[Node]:
        if self._stack is None:
            self._stack = []

        return self._stack

    #= TOP LEVEL ENTITY =#

    start = 'program'

    actions = [
        # macros, annotations, imports etc. can go here
        'statement'
    ]

    @_(*actions)
    def action(self, p: Production):
        self.stack.append(p := p.statement)
        return p

    @_('action')
    def program(self, p: Production):
        self.stack.append(p := Program([p.action]))
        return p
    
    @_('program action')
    def program(self, p: Production):
        print(p.program)
        print(p.action)
        print(2 * '\n')
        self.stack.append(p.program)
        return p

    #= EXPRESSIONS =#

    binary_expr = [
        'expr PLUS expr',
        'expr MINUS expr',
        'expr TIMES expr',
        'expr DIVIDE expr',
        'expr REMAINDER expr',
        'expr DOT_PLUS expr',
        'expr DOT_MINUS expr',
        'expr DOT_TIMES expr',
        'expr DOT_DIVIDE expr',
        'expr DOT_REMAINDER expr',
        'expr EQUAL expr',
        'expr NOT_EQUAL expr',
        'expr GREATER expr',
        'expr GREATER_EQUAL expr',
        'expr LOWER expr',
        'expr LOWER_EQUAL expr',
        'expr AND expr',
        'expr OR expr',
        'expr XOR expr',
        'expr ":" expr'
    ]

    @_(*binary_expr)
    def expr(self, p: Production):
        self.stack.append(BinaryExpression(
            None, 
            None,
            operator=p[1],
            left=p[0],
            right=p[2]
        ))

        return p
    
    prefix_unary_expr = [
        'MINUS expr %prec UMINUS',
        'NOT expr %prec UNEG'
    ]

    @_(*prefix_unary_expr)
    def expr(self, p: Production):
        self.stack.append(UnaryExpression(
            None, 
            None,
            operator=p[0],
            operand=p[1]
        ))

        return p
    
    postfix_unary_expr = [
        '''expr "'" %prec TRANSPOSE'''
    ]

    @_(*postfix_unary_expr)
    def expr(self, p: Production):
        self.stack.append(UnaryExpression(
            None,
            None,
            operand=p[0],
            operator=p[1]
        ))

        return p
    
    @_('"(" expr ")"')
    def expr(self, p: Production):
        self.stack.append(p[1])

    simple_expr = [
        'ID',
        'INT_NUMBER',
        'FLOAT_NUMBER',
        'STRING'
    ]

    @_(*simple_expr)
    def expr(self, p: Production):
        return p
    
    @_('')
    def expr_list(self, p: Production): # (TODO fix) Shift-reduce conflict
        return p

    @_('expr_list "," expr')
    def expr_list(self, p: Production):
        return p
    
    @_('expr')
    def expr_list(self, p: Production):
        return p
    
    @_('"[" expr_list "]"')
    def vector(self, p: Production):
        return p

    @_('vector')
    def vector_list(self, p: Production):
        return p

    @_('vector_list "," vector')
    def vector_list(self, p: Production):
        return p

    @_('"[" vector_list "]"')
    def matrix(self, p: Production):
        return p
    
    @_('vector', 'matrix')
    def expr(self, p: Production):
        return p
    
    keyword_expr = [
        'EYE "(" expr_list ")"',
        'ONES "(" expr_list ")"',
        'ZEROS "(" expr_list ")"',
    ]

    @_(*keyword_expr)
    def expr(self, p: Production):
        return p
    
    @_('expr "(" expr_list ")" %prec CALL') 
    def expr(self, p: Production):
        return p
    
    @_('expr "[" expr_list "]" %prec SUBSCRIPT')
    def expr(self, p: Production):
        return p
    
    #= DEFINITIONS =# 

    # structs etc. belong here

    @_('FUNCTION ID "(" expr_list ")" statement')
    def function(self, p: Production):
        return p
    
    #= STATEMENTS =#

    @_('expr ";"')
    def statement(self, p: Production):
        return p.expr
    
    @_('function')
    def statement(self, p: Production):
        return p.function

    parenless_statement = [
        'PRINT expr_list ";"',
        'RETURN expr_list ";"'
    ]

    @_(*parenless_statement)
    def statement(self, p: Production):
        return p
    
    loop_control = [
        'BREAK ";"',
        'CONTINUE ";"'
    ]

    @_(*loop_control)
    def statement(self, p: Production):
        return p

    assign_statement = [
        'expr ASSIGN expr ";"',
        'expr PLUS_ASSIGN expr ";"',
        'expr MINUS_ASSIGN expr ";"',
        'expr TIMES_ASSIGN expr ";"',
        'expr DIVIDE_ASSIGN expr ";"',
        'expr REMAINDER_ASSIGN expr ";"'
    ]

    @_(*assign_statement)
    def statement(self, p: Production):
        return p
    
    if_statement = [
        'IF "(" expr ")" statement %prec SHORT_IF',
        'IF "(" expr ")" statement ELSE statement',
    ]

    @_(*if_statement)
    def statement(self, p: Production):
        return p

    @_('WHILE "(" expr ")" statement')
    def statement(self, p: Production):
        return p

    @_('FOR "(" ID IN expr ")" statement')
    def statement(self, p: Production):
        return p
    
    @_('"{" statement_series "}"')
    def statement(self, p: Production):
        return p

    @_('statement')
    def statement_series(self, p: Production):
        return p
    
    @_('statement_series statement')
    def statement_series(self, p: Production):
        return p

