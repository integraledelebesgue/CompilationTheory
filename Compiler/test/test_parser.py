import unittest
from typing import Callable
from pipe import Pipe
import sys

sys.path.append('src')

from parser import Parser
from lexer import Lexer


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def assert_no_throw(method: Callable) -> Callable:
    def inner(self) -> None:
        thrown = False

        try:
            method(self)
        except Exception as e:
            thrown = e

        message = f'{method.__name__}:\n{thrown}'

        self.assertFalse(
            thrown,
            message
        )

    return inner


class TestParser(unittest.TestCase):
    lexer = Lexer()
    parser = Parser()

    def process(self, path: str) -> None:
        read = Pipe(read_file)
        tokenize = Pipe(lambda text: self.lexer.tokenize(text))
        parse = Pipe(lambda tokens: self.parser.parse(tokens))

        path | read | tokenize | parse

    @assert_no_throw
    def test_example_1(self):
        self.process('data/example1.m')

    @assert_no_throw
    def test_example_2(self):
        self.process('data/example2.m')

    @assert_no_throw
    def test_example_3(self):
        self.process('data/example3.m')

    @assert_no_throw
    def test_sample_code(self):
        self.process('data/sample_code.txt')

    @assert_no_throw
    def test_sample_code_with_functions(self):
        self.process('data/sample_code_with_functions.txt')

