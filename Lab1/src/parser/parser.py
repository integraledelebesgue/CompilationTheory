import sly
from sly.yacc import YaccProduction as Production
from lexer import Lexer


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
        ('left', CALL, SUBSCRIPT),
        ('nonassoc', SHORT_IF),
        ('nonassoc', ELSE),
    )

    #= TOP LEVEL ENTITY =#

    start = 'program'

    @_('action')
    def program(self, p: Production):
        return p
    
    @_('program action')
    def program(self, p: Production):
        return p
    
    actions = [
        'expr',
        'statement',
        'function'
    ]

    @_(*actions)
    def action(self, p: Production):
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
        return p
    
    unary_expr = [
        'MINUS expr %prec UMINUS',
        'NOT expr %prec UNEG',
        '''expr "'" %prec TRANSPOSE'''
    ]

    @_(*unary_expr)
    def expr(self, p: Production):
        return p
    
    @_('"(" expr ")"')
    def expr(self, p: Production):
        return p

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
    def parameter_list(self, p: Production):
        return p
    
    @_('expr')
    def parameter_list(self, p: Production):
        return p

    @_('parameter_list "," expr')
    def parameter_list(self, p: Production):
        return p
    
    keyword_expr = [
        'EYE "(" parameter_list ")"',
        'ONES "(" parameter_list ")"',
        'ZEROS "(" parameter_list ")"',
    ]

    @_(*keyword_expr)
    def expr(self, p: Production):
        return p
    
    @_('expr "(" parameter_list ")" %prec CALL')  # (TODO fix) expr causes error at the moment 
    def expr(self, p: Production):
        return p
    
    @_('expr "[" parameter_list "]" %prec SUBSCRIPT')  # (TODO fix) Doesn't work
    def expr(self, p: Production):
        return p
    
    #= STATEMENTS =#

    parenless_statement = [
        'PRINT expr',
        'RETURN expr'
    ]

    @_(*parenless_statement)
    def statement(self, p: Production):
        return p
    
    loop_control = [
        'BREAK',
        'CONTINUE'
    ]

    @_(*loop_control)
    def statement(self, p: Production):
        return p

    assign_statement = [
        'ID ASSIGN expr',
        'ID PLUS_ASSIGN expr',
        'ID MINUS_ASSIGN expr',
        'ID TIMES_ASSIGN expr',
        'ID DIVIDE_ASSIGN expr',
        'ID REMAINDER_ASSIGN expr'
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
    
    @_('FUNCTION ID "(" parameter_list ")" statement')
    def function(self, p: Production):
        return p
