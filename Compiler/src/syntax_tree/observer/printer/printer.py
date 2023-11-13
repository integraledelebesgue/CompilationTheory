from syntax_tree.observer.decorators import addToClass

vertical_line = '│'
vertical_branch = '├'
vertical_branch_end = '└'
horizontal_line = '──'
#                 '  ' 2


from syntax_tree.structure.nodes import (
    Program, 
    Identifier,
    Expression,
    ExpressionList,
    Matrix,
    UnaryExpression,
    BinaryExpression,
    Range,
    Subscription,
    Call,
    Assignment,
    If,
    While,
    For,
    Arguments,
    Function,
    Return,
    Control
)

def name(obj) -> str:
    return obj.__class__.__name__


def clean(prefix: str) -> str:
    return prefix.replace(vertical_branch, vertical_line).replace(horizontal_line, '  ').replace(vertical_branch_end, ' ')


def print_action(action, prefix):
    if isinstance(action, list):
        print(prefix + 'Block')            
        
        for subaction in action[:-1]:
            subaction.display('    ' + vertical_branch + horizontal_line)

        action[-1].display('    ' + vertical_branch_end + horizontal_line)

        return

    action.display(prefix)
    

@addToClass(Program)
def display(self: Program) -> None:
    print(name(self))

    if len(self.actions) == 0:
        print(f'{vertical_branch_end} none')
        return

    for action in self.actions[:-1]:
        print_action(action, vertical_branch + horizontal_line + ' ')

    print_action(self.actions[-1], vertical_branch_end + horizontal_line + ' ')


@addToClass(Identifier)
def display(self: Identifier, prefix: str) -> None:
    print(prefix + f"{name(self)} '{self.name}'")


@addToClass(Expression)
def display(self: Expression, prefix='') -> None:
    print(prefix + f"{name(self)} {self.type or 'any'}: '{self.value}'")


@addToClass(ExpressionList)
def display(self: ExpressionList, prefix='') -> None:
    end = 'empty' if len(self.elements) == 0 else ''
    print(prefix + f'{name(self)}: ' + end)

    clean_prefix = clean(prefix)
    block_prefix = clean_prefix + vertical_branch + horizontal_line + ' '
    block_end_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '

    for element in self.elements[:-1]:
        element.display(block_prefix)

    self.elements[-1].display(block_end_prefix)


@addToClass(Matrix)
def display(self: Matrix, prefix='') -> None:
    print(prefix + f'{name(self)}: {self.type or 'any'} of shape {self.shape}')


@addToClass(UnaryExpression)
def display(self: UnaryExpression, prefix='') -> None:
    print(prefix + f'{name(self)} ({self.operator})')

    new_prefix = clean(prefix) + vertical_branch_end + horizontal_line + ' '

    self.operand.display(new_prefix)


@addToClass(BinaryExpression)
def display(self: BinaryExpression, prefix='') -> None:
    print(prefix + f'{name(self)} ({self.operator})')

    clean_prefix = clean(prefix)

    left_prefix = clean_prefix + vertical_branch + horizontal_line + ' '
    right_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '

    self.left.display(left_prefix)
    self.right.display(right_prefix)


@addToClass(Range)
def display(self: Range, prefix='') -> None:
    print(prefix + f'{name(self)}')

    clean_prefix = clean(prefix)

    left_prefix = clean_prefix + vertical_branch + horizontal_line + ' '
    right_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '

    self.start.display(left_prefix)
    self.end.display(right_prefix)


@addToClass(Subscription)
def display(self: Subscription, prefix='') -> None:
    print(prefix + f'{name(self)}')

    clean_prefix = clean(prefix)

    left_prefix = clean_prefix + vertical_branch + horizontal_line + ' '
    right_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '

    self.source.display(left_prefix)
    self.index.display(right_prefix)


@addToClass(Call)
def display(self: Call, prefix='') -> None:
    print(prefix + f"{name(self)} '{self.function}'")  # unsafe, usable only for by-name calls

    new_prefix = clean(prefix) + vertical_branch_end + horizontal_line + ' '

    self.parameters.display(new_prefix)


@addToClass(Assignment)
def display(self: Assignment, prefix='') -> None:
    print(prefix + f'Assign ({self.operator}):')

    clean_prefix = clean(prefix)

    left_prefix = clean_prefix + vertical_branch + horizontal_line + ' '
    right_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '

    self.left.display(left_prefix)
    self.right.display(right_prefix)


@addToClass(If)
def display(self: If, prefix='') -> None:
    clean_prefix = clean(prefix)
    condition_prefix = clean_prefix + vertical_branch + horizontal_line + ' '

    if self.else_body is None:
        then_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '
    else:
        then_prefix = clean_prefix + vertical_branch + horizontal_line + ' '
        else_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '

    block_prefix = clean(then_prefix) + vertical_branch + horizontal_line + ' '
    block_end_prefix = clean(then_prefix) + vertical_branch_end + horizontal_line + ' '

    print(prefix + 'If')
    self.condition.display(condition_prefix)
    
    print(then_prefix + 'Then')
    for action in self.body[:-1]:
        action.display(block_prefix)

    self.body[-1].display(block_end_prefix)

    if self.else_body is None:
        return
    
    else_block_prefix = clean_prefix + '    ' + vertical_branch + horizontal_line + ' '
    else_block_end_prefix = clean_prefix + '    ' + vertical_branch_end + horizontal_line + ' '
    
    print(else_prefix + 'Else')
    for action in self.else_body[:-1]:
        action.display(else_block_prefix)

    self.else_body[-1].display(else_block_end_prefix)


@addToClass(While)
def display(self: While, prefix='') -> None:
    clean_prefix = clean(prefix)
    condition_prefix = clean_prefix + vertical_branch + horizontal_line + ' '
    do_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '
    block_prefix = clean_prefix + '    ' +vertical_branch + horizontal_line + ' '
    block_end_prefix = clean_prefix + '    ' + vertical_branch_end + horizontal_line + ' '
    
    print(prefix + 'While')
    self.condition.display(condition_prefix)
    
    print(do_prefix + 'Do')
    
    for action in self.body[:-1]:
        action.display(block_prefix)

    self.body[-1].display(block_end_prefix)


@addToClass(For)
def display(self: For, prefix='') -> None:
    clean_prefix = clean(prefix)
    iterator_prefix = clean_prefix + vertical_branch + horizontal_line + ' '
    do_prefix = clean_prefix + vertical_branch_end + horizontal_line + ' '
    range_prefix = clean(iterator_prefix) + vertical_branch_end + horizontal_line + ' '

    block_prefix = clean_prefix + '    ' + vertical_branch + horizontal_line + ' '
    block_end_prefix = clean_prefix + '    ' + vertical_branch_end + horizontal_line + ' '

    print(prefix + 'For')
    print(iterator_prefix + 'Iterator')
    self.iterator.display(range_prefix)

    print(iterator_prefix + 'In')
    self.range.display(range_prefix)

    print(do_prefix + 'Do')
    
    for action in self.body[:-1]:
        action.display(block_prefix)

    self.body[-1].display(block_end_prefix)


@addToClass(Arguments)  # TODO
def display(self: Arguments, prefix='') -> None:
    new_prefix = clean(prefix) + ''

    for argument, type, value in zip(self.names, self.types, self.default_values):
        print(prefix + f'{argument}: {type or 'any'}', end=' ')
        
        if value is None:
            print()
        
        else:
            print('default')
            value.display(prefix + '\t')


@addToClass(Function)  # TODO
def display(self: Function, prefix='') -> None:
    print(prefix + f"Function '{self.name}': {self.type or 'any'}")
    
    print(prefix + 'With arguments:')
    self.arguments.display(prefix + '\t')

    print(prefix + 'Do:')
    for action in self.body:
        action.display(prefix + '\t')


@addToClass(Return)
def display(self: Return, prefix='') -> None:
    print(prefix + 'Return')

    if self.expression is None:
        return

    new_prefix = clean(prefix) + vertical_branch_end + horizontal_line + ' '

    self.expression.display(new_prefix)


@addToClass(Control)
def display(self: Control, prefix='') -> None:
    print(prefix + self.type.title())

    if self.expression is None:
        return

    print()
    self.expression.display(prefix + '\t')

