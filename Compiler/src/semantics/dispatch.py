from semantics.types import *


expressions = {
    'binary': {
        '+': {
            (int32, int32): int32,
            (int32, float64): float64,
            (float64, int32): float64,
            (float64, float64): float64,
            (string, string): string
        },
        '-': {
            (int32, int32): int32,
            (int32, float64): float64,
            (float64, int32): float64,
            (float64, float64): float64
        },
        '*': {
            (int32, int32): int32,
            (int32, float64): float64,
            (float64, int32): float64,
            (float64, float64): float64,
            (string, int32): string,
            (int32, string): string,

            (matrix_int32, matrix_int32): matrix_int32,
            (matrix_float64, matrix_float64): matrix_float64,

            (matrix_float64, matrix_int32): matrix_float64,
            (matrix_float64, matrix_int32): matrix_float64
        },
        '/': {
            (int32, int32): float64,
            (int32, float64): float64,
            (float64, int32): float64,
            (float64, float64): float64
        },
        '%': {
            (int32, int32): int32
        },
        '.+': {
            (matrix_int32, int32): matrix_int32,
            (matrix_int32, float64): matrix_float64,
            (int32, matrix_int32): matrix_int32,
            (float64, matrix_int32): matrix_float64,
            (matrix_int32, matrix_int32): matrix_int32,

            (matrix_float64, int32): matrix_float64,
            (matrix_float64, float64): matrix_float64,
            (int32, matrix_float64): matrix_float64,
            (float64, matrix_float64): matrix_float64,
            (matrix_float64, matrix_float64): matrix_float64,

            (matrix_int32, matrix_float64): matrix_float64,
            (matrix_float64, matrix_int32): matrix_float64,

            (vector_int32, int32): vector_int32,
            (vector_int32, float64): vector_float64,
            (int32, vector_int32): vector_int32,
            (float64, vector_int32): vector_float64,
            (vector_int32, vector_int32): vector_int32,

            (vector_float64, int32): vector_float64,
            (vector_float64, float64): vector_float64,
            (int32, vector_float64): vector_float64,
            (float64, vector_float64): vector_float64,
            (vector_float64, vector_float64): vector_float64,

            (vector_int32, vector_float64): vector_float64,
            (vector_float64, vector_int32): vector_float64,
        },
        '.-': {
            (matrix_int32, int32): matrix_int32,
            (matrix_int32, float64): matrix_float64,
            (int32, matrix_int32): matrix_int32,
            (float64, matrix_int32): matrix_float64,
            (matrix_int32, matrix_int32): matrix_int32,

            (matrix_float64, int32): matrix_float64,
            (matrix_float64, float64): matrix_float64,
            (int32, matrix_float64): matrix_float64,
            (float64, matrix_float64): matrix_float64,
            (matrix_float64, matrix_float64): matrix_float64,

            (matrix_int32, matrix_float64): matrix_float64,
            (matrix_float64, matrix_int32): matrix_float64,

            (vector_int32, int32): vector_int32,
            (vector_int32, float64): vector_float64,
            (int32, vector_int32): vector_int32,
            (float64, vector_int32): vector_float64,
            (vector_int32, vector_int32): vector_int32,

            (vector_float64, int32): vector_float64,
            (vector_float64, float64): vector_float64,
            (int32, vector_float64): vector_float64,
            (float64, vector_float64): vector_float64,
            (vector_float64, vector_float64): vector_float64,

            (vector_int32, vector_float64): vector_float64,
            (vector_float64, vector_int32): vector_float64,
        },
        '.*': {
            (matrix_int32, int32): matrix_int32,
            (matrix_int32, float64): matrix_float64,
            (int32, matrix_int32): matrix_int32,
            (float64, matrix_int32): matrix_float64,
            (matrix_int32, matrix_int32): matrix_int32,

            (matrix_float64, int32): matrix_float64,
            (matrix_float64, float64): matrix_float64,
            (int32, matrix_float64): matrix_float64,
            (float64, matrix_float64): matrix_float64,
            (matrix_float64, matrix_float64): matrix_float64,

            (matrix_int32, matrix_float64): matrix_float64,
            (matrix_float64, matrix_int32): matrix_float64,

            (vector_int32, int32): vector_int32,
            (vector_int32, float64): vector_float64,
            (int32, vector_int32): vector_int32,
            (float64, vector_int32): vector_float64,
            (vector_int32, vector_int32): vector_int32,

            (vector_float64, int32): vector_float64,
            (vector_float64, float64): vector_float64,
            (int32, vector_float64): vector_float64,
            (float64, vector_float64): vector_float64,
            (vector_float64, vector_float64): vector_float64,

            (vector_int32, vector_float64): vector_float64,
            (vector_float64, vector_int32): vector_float64,
        },
        './': {
            (matrix_int32, int32): matrix_int32,
            (matrix_int32, float64): matrix_float64,
            (int32, matrix_int32): matrix_int32,
            (float64, matrix_int32): matrix_float64,
            (matrix_int32, matrix_int32): matrix_int32,

            (matrix_float64, int32): matrix_float64,
            (matrix_float64, float64): matrix_float64,
            (int32, matrix_float64): matrix_float64,
            (float64, matrix_float64): matrix_float64,
            (matrix_float64, matrix_float64): matrix_float64,

            (matrix_int32, matrix_float64): matrix_float64,
            (matrix_float64, matrix_int32): matrix_float64,

            (vector_int32, int32): vector_int32,
            (vector_int32, float64): vector_float64,
            (int32, vector_int32): vector_int32,
            (float64, vector_int32): vector_float64,
            (vector_int32, vector_int32): vector_int32,

            (vector_float64, int32): vector_float64,
            (vector_float64, float64): vector_float64,
            (int32, vector_float64): vector_float64,
            (float64, vector_float64): vector_float64,
            (vector_float64, vector_float64): vector_float64,

            (vector_int32, vector_float64): vector_float64,
            (vector_float64, vector_int32): vector_float64,
        },
        '.%': {
            (matrix_int32, int32): matrix_int32,
            (int32, matrix_int32): matrix_int32,
            (matrix_int32, matrix_int32): matrix_int32,

            (vector_int32, int32): vector_int32,
            (int32, vector_int32): vector_int32,
            (vector_int32, vector_int32): vector_int32,

        },
        '==': {
            (int32, int32): boolean,
            (float64, float64): boolean,
            (boolean, boolean): boolean,
            (string, string): boolean,
            
            (vector_int32, vector_int32): boolean,
            (vector_float64, vector_float64): boolean,
            (vector_int32, vector_float64): boolean,
            (vector_float64, vector_int32): boolean,

            (matrix_int32, matrix_int32): boolean,
            (matrix_float64, matrix_float64): boolean,
            (matrix_int32, matrix_float64): boolean,
            (matrix_float64, matrix_int32): boolean,
        },
        '!=': {
            (int32, int32): boolean,
            (float64, float64): boolean,
            (boolean, boolean): boolean,
            (string, string): boolean,
            
            (vector_int32, vector_int32): boolean,
            (vector_float64, vector_float64): boolean,
            (vector_int32, vector_float64): boolean,
            (vector_float64, vector_int32): boolean,

            (matrix_int32, matrix_int32): boolean,
            (matrix_float64, matrix_float64): boolean,
            (matrix_int32, matrix_float64): boolean,
            (matrix_float64, matrix_int32): boolean,
        },
        '<': {
            (int32, int32): boolean,
            (float64, float64): boolean,
            (boolean, boolean): boolean,
            (string, string): boolean,
        },
        '<=': {
            (int32, int32): boolean,
            (float64, float64): boolean,
            (boolean, boolean): boolean,
            (string, string): boolean,
            (vector_int32, vector_int32): boolean,
            (matrix_int32, matrix_int32): boolean,
        },
        '>': {
            (int32, int32): boolean,
            (float64, float64): boolean,
            (boolean, boolean): boolean,
            (string, string): boolean
        },
        '>=': {
            (int32, int32): boolean,
            (float64, float64): boolean,
            (boolean, boolean): boolean,
            (string, string): boolean
        },
        'and': {
            (boolean, boolean): boolean
        },
        'or': {
            (boolean, boolean): boolean
        },
        'xor': {
            (boolean, boolean): boolean
        }
    },
    'unary': {
        "'": {
            (matrix_int32,): matrix_int32,
            (vector_int32,): matrix_int32,
            (matrix_float64,): matrix_float64,
            (vector_float64,): matrix_float64,
        },
        '-': {
            (int32,): int32,
            (float64,): float64,
            (vector_int32,): vector_int32,
            (matrix_int32): matrix_int32,
            (vector_float64,): vector_float64,
            (matrix_float64): matrix_float64
        },
        'not': {
            (boolean,): boolean
        }
    },
    'range': {
        'unit': {
            (int32, int32): range_int32
        }
    }
}

functions = {
    'zeros': {
        (int32, int32): matrix_int32,
        (int32,): matrix_int32
    },
    'ones': {
        (int32, int32): matrix_int32,
        (int32,): matrix_int32
    },
    'eye': {
        (int32,): matrix_int32
    },
    'print': {
        (int32,): nothing,
        (float64,): nothing,
        (boolean,): nothing,
        (vector_int32,): nothing,
        (vector_float64,): nothing,
        (matrix_int32,): nothing,
        (matrix_float64,): nothing,
    }
}
