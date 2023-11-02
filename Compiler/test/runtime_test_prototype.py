import unittest
import sys
from unittest import TestCase, TestSuite, TextTestRunner
from glob import glob
from pipe import Pipe
from typing import Callable

sys.path.append('src')
from parser import Parser
from lexer import Lexer


lexer = Lexer()
parser = Parser()

def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()

read = Pipe(lambda path: read_file(path))
tokenize = Pipe(lambda file: lexer.tokenize(file))
parse = Pipe(lambda tokens: parser.parse(tokens))


def to_name(path: str) -> str:
    return path\
        .replace('/', '_')\
        .replace('.', '_')


def test_method_from_file(instance: TestCase, path: str) -> Callable:
    def test(self):
        thrown = None
        
        try:
            path | read | tokenize | parse
            thrown = False
        except Exception as e:
            thrown = e
        
        instance.assertFalse(
            thrown,
            thrown
        )

    return test


def insert_from_matching_files(instance: TestCase, pattern: str) -> None:
    for path in glob(pattern):
        setattr(
            instance, 
            f'test_{to_name(path)}',
            test_method_from_file(instance, path)
        )


class directory:
    pattern: str

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def __call__(self, constructor: Callable) -> Callable:
        def inner(*args, **kwargs):
            instance = constructor(*args, **kwargs)
            insert_from_matching_files(instance, self.pattern)  
            return instance
        
        return inner


matlab = 'data/*.m'
better_lang = 'data/*.txt'

@directory(matlab)
class TestParserMatlab(TestCase):
    # def __init__(self, methodName: str = "runTest") -> None:
    #     super().__init__(methodName)
    pass

@directory(better_lang)
class TestParserMine(TestCase):
    # def __init__(self, methodName: str = "runTest") -> None:
    #     super().__init__(methodName)
    pass


# def add_tests(suite, cls):
#     for name in filter(lambda s: s.startswith('test'), dir(cls)):
#         suite.add(cls(name))

# def suite():
#     suite = TestSuite()
    
#     add_tests(suite, TestParserMatlab)
#     add_tests(suite, TestParserMine)

#     return suite


# if __name__ == '__main__':
#     runner = TextTestRunner()
#     runner.run(s := suite())
#     print(s)

if __name__ == '__main__':
    for method in filter(lambda s: s.startswith('test'), dir(instance := TestParserMatlab())):
        getattr(instance, method)(instance)


