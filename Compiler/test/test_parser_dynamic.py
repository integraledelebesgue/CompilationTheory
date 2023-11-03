import unittest
import sys
from glob import glob
from typing import Self, Dict, Callable, Any
from pipe import Pipe

sys.path.append('src')
from parser import Parser
from lexer import Lexer


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()
    

def assert_no_throw(method: Callable) -> Callable:
    def wrapper(obj) -> None:
        thrown = False

        try:
            method(obj)
        except Exception as e:
            thrown = e

        message = f'{method.__name__}:\n{thrown}'

        obj.assertFalse(
            thrown,
            message
        )

    return wrapper


class DynamicTest(type):
    '''Instead of maually defining test methods for each source code file, 
    simply use this handy metaprogramming hell to create them from the pattern provided.'''

    def __new__(cls, name, bases, dct, *, pattern: str) -> Self:
        bases = (*bases, unittest.TestCase)

        cls.insert_properties(dct)
        cls.insert_process_method(dct)
        cls.insert_tests(dct, pattern)

        return super().__new__(cls, name, bases, dct)

    @classmethod
    def insert_properties(cls, dct: Dict[str, Any]) -> None:
        dct['lexer'] = Lexer()
        dct['parser'] = Parser()
        dct['read'] = Pipe(read_file)
        dct['tokenize'] = Pipe(lambda text: dct['lexer'].tokenize(text))
        dct['parse'] = Pipe(lambda tokens: dct['parser'].parse(tokens))

    @classmethod
    def insert_process_method(cls, dct: Dict[str, Any]) -> None:
        def process(obj, path: str) -> None:
            path | obj.read | obj.tokenize | obj.parse

        dct['process'] = process

    @classmethod
    def insert_tests(cls, dct: Dict[str, Any], pattern: str) -> None:
        dct.update({
            (cls.name(path), cls.test_method(path)) 
            for path in glob(pattern)
        })
    
    @classmethod
    def name(cls, path: str) -> str:
        return 'test_' + path\
            .split('/')[-1]\
            .replace('.', '_')\

    @classmethod
    def test_method(cls, path: str) -> Callable:
        @assert_no_throw
        def test(obj):
            obj.process(path)

        return test


class TestExtendedSyntax(metaclass=DynamicTest, pattern='data/*.txt'):
    pass

class TestMatLabSyntax(metaclass=DynamicTest, pattern='data/*.m'):
    pass
