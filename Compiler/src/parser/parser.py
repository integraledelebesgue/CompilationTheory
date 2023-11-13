from typing import *
import sly
from sly.yacc import YaccProduction as Production
from lexer import Lexer
from syntax_tree.structure.nodes import *
from functools import reduce
from operator import add

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

    root: Optional[Node] = None

    #= TOP LEVEL ENTITY =#

    start = 'program'

    actions = [
        # macros, annotations, imports etc. can go here
        'statement'
    ]

    @_(*actions)
    def action(self, p: Production):
        return p.statement

    @_('action')
    def program(self, p: Production):
        node = Program([p.action])
        self.root = node
        return node
    
    @_('program action')
    def program(self, p: Production):
        node = p.program
        node.actions.append(p.action)

        self.root = node

        return node

    #= EXPRESSIONS =#

    arithmetic_expr = [
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
    ]

    @_(*arithmetic_expr)
    def expr(self, p: Production):        
        return ArithmeticExpression(
            None, 
            None,
            operator=p[1],
            left=p[0],
            right=p[2]
        )
    
    relational_expression = [
        'expr EQUAL expr',
        'expr NOT_EQUAL expr',
        'expr GREATER expr',
        'expr GREATER_EQUAL expr',
        'expr LOWER expr',
        'expr LOWER_EQUAL expr',
    ]

    @_(*relational_expression)
    def expr(self, p: Production):
        return RelationalExpression(
            None,
            None,
            operator=p[1],
            left=p[0],
            right=p[2]
        )
    
    logical_expression = [
        'expr AND expr',
        'expr OR expr',
        'expr XOR expr',
    ]

    @_(*logical_expression)
    def expr(self, p: Production):
        return LogicalExpression(
            None,
            None,
            operator=p[1],
            left=p[0],
            right=p[2]
        )

    @_('expr ":" expr')
    def expr(self, p: Production):
        return Range(
            None,
            None,
            start=p[0],
            end=p[2]
        )

    prefix_unary_expr = [
        'MINUS expr %prec UMINUS',
        'NOT expr %prec UNEG'
    ]

    @_(*prefix_unary_expr)
    def expr(self, p: Production):
        return UnaryExpression(
            None, 
            None,
            operator=p[0],
            operand=p[1]
        )
    
    postfix_unary_expr = [
        '''expr "'" %prec TRANSPOSE'''
    ]

    @_(*postfix_unary_expr)
    def expr(self, p: Production):
        return UnaryExpression(
            None,
            None,
            operand=p[0],
            operator=p[1]
        )
    
    @_('"(" expr ")"')
    def expr(self, p: Production):
        return p[1]
    
    @_('ID')
    def expr(self, p: Production):
        return Identifier(p.ID)
    
    @_('INT_NUMBER')
    def expr(self, p: Production):
        return Expression(
            p.INT_NUMBER,
            'int'
        )

    @_('FLOAT_NUMBER')
    def expr(self, p: Production):
        return Expression(
            p.FLOAT_NUMBER,
            'float64'
        )
    
    @_('STRING')
    def expr(self, p: Production):
        return Expression(
            p.STRING,
            'string'
        )
    
    @_('')
    def expr_list(self, p: Production): # (TODO fix) Shift-reduce conflict
        return ExpressionList([], [])

    @_('expr_list "," expr')
    def expr_list(self, p: Production):
        node = p.expr_list
        node.elements.append(p.expr)
        node.types.append(None)

        return node
    
    @_('expr')
    def expr_list(self, p: Production):
        return ExpressionList([p.expr], [None])
    
    @_('"[" expr_list "]"')
    def vector(self, p: Production):
        return Vector(
            elements=p.expr_list.elements,
            types=p.expr_list.types,
            length=len(p.expr_list.elements)
        )

    @_('vector')
    def vector_list(self, p: Production):
        return [p.vector]

    @_('vector_list "," vector')
    def vector_list(self, p: Production):
        return p.vector_list + [p.vector]

    @staticmethod
    def homogeneous_shape(vectors: List[Vector]) -> bool:
        return set(map(lambda v: v.length, vectors)).__len__() == 1
    
    @staticmethod
    def homogeneous_type(vectors: List[Vector]) -> bool:
        return reduce(set.union, map(lambda v: set(v.types), vectors)).__len__() == 1
    
    @staticmethod
    def verify(vectors: List[Vector]) -> None:
        if not Parser.homogeneous_shape(vectors):
            raise Exception('') # TODO Error handling
        
        if not Parser.homogeneous_type(vectors):
            raise Exception('')

    @_('"[" vector_list "]"')
    def matrix(self, p: Production):
        vectors = p.vector_list

        Parser.verify(vectors)
        
        type = vectors[0].types[0]
        
        shape = (
            len(vectors), 
            vectors[0].length
        )

        return Matrix(
            vectors,
            type,
            shape
        )
    
    @_('vector')
    def expr(self, p: Production):
        return p.vector
    
    @_('matrix')
    def expr(self, p: Production):
        return p.matrix
    
    keyword_expr = [
        'EYE "(" expr_list ")"',
        'ONES "(" expr_list ")"',
        'ZEROS "(" expr_list ")"',
    ]

    @_(*keyword_expr)
    def expr(self, p: Production):
        return BuiltinCall(
            None,
            'matrix',
            p[0],
            p.expr_list
        )
    
    @_('expr "(" expr_list ")" %prec CALL') 
    def expr(self, p: Production):
        return Call(
            None,
            None,
            p[0],
            p.expr_list
        )
    
    @_('expr "[" expr_list "]" %prec SUBSCRIPT')
    def expr(self, p: Production):
        return Subscription(
            None,
            None,
            p[0],
            p.expr_list
        )
    
    #= DEFINITIONS =# 

    @staticmethod
    def ensure_block(statement_or_block: Union[Statement, List[Statement]]) -> List[Statement]:
        block = statement_or_block\
            if isinstance(statement_or_block, list)\
            else [statement_or_block]
        
        return block

    # structs etc. belong here

    @_('FUNCTION ID "(" expr_list ")" statement')
    def function(self, p: Production):
        argument_names = p.expr_list.elements
        
        arguments = Arguments(
            argument_names,
            [None for _ in argument_names],
            [None for _ in argument_names]
        )

        body = Parser.ensure_block(p.statement)
        
        return Function(
            p.ID,
            arguments,
            body
        )
    
    #= STATEMENTS =#

    @_('expr ";"')
    def statement(self, p: Production):
        return p.expr
    
    @_('function')
    def statement(self, p: Production):
        return p.function

    parenless_calls = [
        'PRINT expr_list ";"',  # Move to functions in the future
    ]

    @_(*parenless_calls)
    def statement(self, p: Production):
        return BuiltinCall(
            None,
            None,
            p[0],
            p.expr_list
        )

    @_('RETURN expr_list ";"')
    def statement(self, p: Production):
        return Return(
            None,
            None,
            p.expr_list
        )
    
    loop_control = [
        'BREAK ";"',
        'CONTINUE ";"'
    ]

    @_(*loop_control)
    def statement(self, p: Production):
        return Control(
            p[0].lower(),
            None
        )

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
        return Assignment(
            p[1],
            p[0],
            p[2]
        )

    @_('IF "(" expr ")" statement %prec SHORT_IF')
    def statement(self, p: Production):
        body = Parser.ensure_block(p.statement)
        
        return If(
            p.expr,
            body,
            None
        )
    
    @_('IF "(" expr ")" statement ELSE statement')
    def statement(self, p: Production):
        body = Parser.ensure_block(p[4])
        else_body = Parser.ensure_block(p[6])

        return If(
            p.expr,
            body,
            else_body
        )

    @_('WHILE "(" expr ")" statement')
    def statement(self, p: Production):
        body = Parser.ensure_block(p.statement)

        return While(
            p.expr,
            body
        )

    @_('FOR "(" ID IN expr ")" statement')
    def statement(self, p: Production):
        body = Parser.ensure_block(p.statement)

        return For(
            Identifier(p.ID),
            p.expr,
            body
        )
    
    @_('"{" statement_series "}"')
    def statement(self, p: Production):
        return p.statement_series

    @_('statement')
    def statement_series(self, p: Production):
        return [p.statement]
    
    @_('statement_series statement')
    def statement_series(self, p: Production):
        return p.statement_series + [p.statement]

