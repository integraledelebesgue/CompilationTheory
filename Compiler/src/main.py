from sys import argv
from os.path import abspath
from lexer import Lexer
from parser import Parser
from virtual_machine.code_generator import compile, disassemble
from virtual_machine.virtual_machine import VirtualMachine

# import syntax_tree._observer.printer

from utilities.colors import ANSII


def print_error() -> None:
    ansii_red = "\033[91m {}\033[00m"
    error = 'No input specified. '
    usage = 'Usage: python main.py <path_to source>'
    
    print(ansii_red.format(error), usage, sep='', end='\n')


def read_source(path: str) -> str:
    absolute_path = abspath(path)

    with open(absolute_path, 'r') as file:
        return file.read()


if __name__ == '__main__':
    match argv:
        case [_, path, *_]:
            source = read_source(path)
        case _:
            print_error()
            exit(-1)

    lexer = Lexer()
    tokens = lexer.tokenize(source)

    #print(*list(tokens), sep='\n')

    parser = Parser()
    parser.parse(tokens)

    # print(*parser.root.actions, sep='\n')

    parser.root.structurize()
    parser.root.content.check_types()
    parser.root.display()
    
    code = compile(parser.root)
    
    print('\n' + disassemble(code))

    vm = VirtualMachine()
    vm.load(code, debug=False)
    vm.run()

    # print(parser.root.superscopes)


