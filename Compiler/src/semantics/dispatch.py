expressions = {
    'binary': {
        '+': {
            ('int32', 'int32'): 'int32',
            ('int32', 'float64'): 'float64',
            ('float64', 'int32'): 'float64',
            ('float64', 'float64'): 'float64',
            ('string', 'string'): 'string'
        },
        '-': {
            ('int32', 'int32'): 'int32',
            ('int32', 'float64'): 'float64',
            ('float64', 'int32'): 'float64',
            ('float64', 'float64'): 'float64'
        },
        '*': {
            ('int32', 'int32'): 'int32',
            ('int32', 'float64'): 'float64',
            ('float64', 'int32'): 'float64',
            ('float64', 'float64'): 'float64',
            ('string', 'int'): 'string',
            ('int', 'string'): 'string'
        },
        '/': {
            ('int32', 'int32'): 'float64',
            ('int32', 'float64'): 'float64',
            ('float64', 'int32'): 'float64',
            ('float64', 'float64'): 'float64'
        },
        '%': {
            ('int32', 'int32'): 'int32'
        },
        '.+': {
            ('matrix', 'int32'): 'matrix',
            ('matrix', 'float64'): 'matrix',
            ('int32', 'matrix'): 'matrix',
            ('float64', 'matrix'): 'matrix',
            ('matrix', 'matrix'): 'matrix',

            ('vector', 'int32'): 'vector',
            ('vector', 'float64'): 'vector',
            ('int32', 'vector'): 'vector',
            ('float64', 'vector'): 'vector',
            ('vector', 'vector'): 'vector',
        },
        '.-': {
            ('matrix', 'int32'): 'matrix',
            ('matrix', 'float64'): 'matrix',
            ('int32', 'matrix'): 'matrix',
            ('float64', 'matrix'): 'matrix',
            ('matrix', 'matrix'): 'matrix',

            ('vector', 'int32'): 'vector',
            ('vector', 'float64'): 'vector',
            ('int32', 'vector'): 'vector',
            ('float64', 'vector'): 'vector',
            ('vector', 'vector'): 'vector',
        },
        '.*': {
            ('matrix', 'int32'): 'matrix',
            ('matrix', 'float64'): 'matrix',
            ('int32', 'matrix'): 'matrix',
            ('float64', 'matrix'): 'matrix',
            ('matrix', 'matrix'): 'matrix',

            ('vector', 'int32'): 'vector',
            ('vector', 'float64'): 'vector',
            ('int32', 'vector'): 'vector',
            ('float64', 'vector'): 'vector',
            ('vector', 'vector'): 'vector',
        },
        './': {
            ('matrix', 'int32'): 'matrix',
            ('matrix', 'float64'): 'matrix',
            ('int32', 'matrix'): 'matrix',
            ('float64', 'matrix'): 'matrix',
            ('matrix', 'matrix'): 'matrix',

            ('vector', 'int32'): 'vector',
            ('vector', 'float64'): 'vector',
            ('int32', 'vector'): 'vector',
            ('float64', 'vector'): 'vector',
            ('vector', 'vector'): 'vector',
        },
        '.%': {
            ('matrix', 'int32'): 'matrix',
            ('matrix', 'float64'): 'matrix',
            ('int32', 'matrix'): 'matrix',
            ('float64', 'matrix'): 'matrix',
            ('matrix', 'matrix'): 'matrix',

            ('vector', 'int32'): 'vector',
            ('vector', 'float64'): 'vector',
            ('int32', 'vector'): 'vector',
            ('float64', 'vector'): 'vector',
            ('vector', 'vector'): 'vector',
        },
        '==': {
            ('int32', 'int32'): 'bool',
            ('float64', 'float64'): 'bool',
            ('bool', 'bool'): 'bool',
            ('string', 'string'): 'bool',
            ('vector', 'vector'): 'bool',
            ('matrix', 'matrix'): 'bool',
        },
        '!=': {
            ('int32', 'int32'): 'bool',
            ('float64', 'float64'): 'bool',
            ('bool', 'bool'): 'bool',
            ('string', 'string'): 'bool',
            ('vector', 'vector'): 'bool',
            ('matrix', 'matrix'): 'bool',
        },
        '<': {
            ('int32', 'int32'): 'bool',
            ('float64', 'float64'): 'bool',
            ('bool', 'bool'): 'bool',
            ('string', 'string'): 'bool',
            ('vector', 'vector'): 'bool',
            ('matrix', 'matrix'): 'bool',
        },
        '<=': {
            ('int32', 'int32'): 'bool',
            ('float64', 'float64'): 'bool',
            ('bool', 'bool'): 'bool',
            ('string', 'string'): 'bool',
            ('vector', 'vector'): 'bool',
            ('matrix', 'matrix'): 'bool',
        },
        '>': {
            ('int32', 'int32'): 'bool',
            ('float64', 'float64'): 'bool',
            ('bool', 'bool'): 'bool',
            ('string', 'string'): 'bool',
            ('vector', 'vector'): 'bool',
            ('matrix', 'matrix'): 'bool',
        },
        '>=': {
            ('int32', 'int32'): 'bool',
            ('float64', 'float64'): 'bool',
            ('bool', 'bool'): 'bool',
            ('string', 'string'): 'bool',
            ('vector', 'vector'): 'bool',
            ('matrix', 'matrix'): 'bool',
        },
        'and': {
            ('bool', 'bool'): 'bool'
        },
        'or': {
            ('bool', 'bool'): 'bool'
        },
        'xor': {
            ('bool', 'bool'): 'bool'
        }
    },
    'unary': {
        "'": {
            ('matrix',): 'matrix',
            ('vector',): 'matrix'
        },
        '-': {
            ('int32',): 'int32',
            ('float64',): 'float64',
            ('vector',): 'vector',
            ('matrix'): 'matrix'
        },
        'not': {
            ('bool',): 'bool'
        }
    },
    'range': {
        'unit': {
            ('int', 'int'): 'range<int>'
        }
    }
}
