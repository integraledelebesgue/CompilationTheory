from sys import argv
from os.path import abspath
from lexer.lexer import Scanner

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

    scanner = Scanner()
    tokens = scanner.tokenize(source)

    print(*list(tokens), sep='\n')
