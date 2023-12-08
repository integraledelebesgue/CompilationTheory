from dataclasses import dataclass
from typing import Optional, Callable, Any
from icecream import ic

UNSPECIFIED = '*'
ANY = 'any'
NOTHING = 'nothing'

def hash_method(parameters) -> Callable[[Any], int]:
    def __hash__(obj):
        return hash(tuple(
            obj.name, 
            *(obj.__getattribute__(name) for name in parameters)
        ))
    
    return __hash__

def instantiate_method(parameters) -> Callable:
    typed_args = ', '.join(map(
        lambda p: f'{p}: str',
        parameters
    ))

    parameter_assignments = ''.join(map(
        lambda name: f'    instance.{name} = {name}\n',
        parameters
    ))

    print(parameters)
    
    code = f'''
def instantiate(obj, {typed_args}, *, name: Optional[str] = None) -> 'Type':
    instance = type(obj)(obj.name)

    if name is not None:
        instance.abstract_name = obj.name
        instance.name = name

{parameter_assignments}

    return instance
    '''

    exec(compile(code, 'file', 'exec'))

    return locals()['instantiate']


def abstract_method(parameters) -> Callable:
    parameter_assignments = ''.join(map(
        lambda name: f'    instance.{name} = "{UNSPECIFIED}"\n',
        parameters
    ))
    
    code = f'''
def abstract(obj) -> 'Type':
    instance = type(obj)(obj.abstract_name)

{parameter_assignments}

    return instance
    '''

    exec(compile(code, 'file', 'exec'))

    return locals()['abstract']


def repr_method(parameters) -> Callable[[Any], str]:
    def __repr__(obj):
        # fields = ', '.join(map(
        #     lambda name: f'{name}: {obj.__getattribute__(name)}',
        #     vars(obj)
        # ))

        info = f"'{obj.name}'"

        if obj.supertype is not None:
            info = info + f'<: {obj.supertype}'

        if len(parameters) == 0:
            return f'{obj.__class__.__name__} {info}'

        parameter_values = ', '.join(map(
            lambda name: f'{name}: {obj.__getattribute__(name)}',
            parameters
        ))

        return f'{obj.__class__.__name__}<{parameter_values}> {info}'

    return __repr__


def code_method(parameters) -> Callable[[Any], str]:
    def code(obj):
        parameter_names = ', '.join(parameters)
        postfix = ''\
            if len(parameters) == 0\
            else f'<{parameter_names}>'

        return f'{obj.name}' + postfix
    
    return code


class MetaType(type):
    def __new__(cls, name, bases, dct, *, parameters: Optional[list[str]]):
        parameters = parameters or []

        for parameter in parameters:
            dct[parameter] = UNSPECIFIED

        if len(parameters) > 0:
            dct['instantiate'] = instantiate_method(parameters)
        
        dct['__hash__'] = hash_method(parameters)
        dct['__repr__'] = repr_method(parameters)
        
        dct['abstract'] = abstract_method(parameters)
        dct['instances'] = []

        return super().__new__(cls, name, bases, dct)


class Type:
    name: str = NOTHING
    supertype: Optional['Type'] = None

    def __init__(self, name: str, supertype: Optional['Type'] = None) -> None:
        self.name = name
        self.supertype = supertype
    
    # def match_code(cls, code: str) -> Optional['Type']:
    #     for member in cls.members:
    #         if member.code() == code:
    #             return member
    
    def match_name(cls, name: str) -> Optional['Type']:
        for member in cls.members:
            if member.name == name:
                return member


class Primitive(
    Type,
    metaclass=MetaType,
    parameters=[]
):
    pass

Primitive.members = [
    Primitive('bool'),
    Primitive('i32'),
    Primitive('f64'),
    Primitive('string')
]


class AbstractArray(
    Type,
    metaclass=MetaType,
    parameters=[
        'element_type',
        'n_dimensions'
    ]
):
    pass

AbstractArray.members = [
    AbstractArray('array')
]


if __name__ == '__main__':
    print(AbstractArray.members)
    
    matrix_type = AbstractArray.members[0].instantiate(Primitive('i32'), 2, name='matrix')
    print(matrix_type)

    matrix_abstract_parent = matrix_type.abstract()
    print(matrix_abstract_parent)

