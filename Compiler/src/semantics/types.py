from typing import Any

class Type:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Type):
            return False
        
        return self.name == other.name


class Primitive(Type):
    pass


class Collection(Type):
    element_type: Primitive

    def __init__(self, name: str, element_type: Primitive) -> None:
        super().__init__(name)
        self.element_type = element_type

    def __hash__(self) -> int:
        return hash((self.name, self.element_type))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Collection):
            return False
        
        return self.name == other.name and\
            self.element_type == other.element_type

    def __repr__(self) -> str:
        return f'{self.name}<{self.element_type}>'
    

int32 = Primitive('int32')
float64 = Primitive('float64')
boolean = Primitive('boolean')
string = Primitive('string')

function = Primitive('function')
nothing = Primitive('nothing')

vector_int32 = Collection('vector', int32)
vector_float64 = Collection('vector', float64)

matrix_int32 = Collection('matrix', int32)
matrix_float64 = Collection('matrix', float64)

range_int32 = Collection('range', int32)
