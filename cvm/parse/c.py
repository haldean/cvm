reserved = set([
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
    'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
    'if', 'int', 'long', 'register', 'return', 'short', 'signed',
    'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned',
    'void', 'volatile', 'while'
    ])

tokens = [
    'ADD', 'ADD_ASSIGN', 'AND_ASSIGN', 'ASSIGN', 'BITWISE_AND', 'BITWISE_NOT',
    'BITWISE_OR', 'BITWISE_XOR', 'BOOLEAN_AND', 'BOOLEAN_NOT', 'BOOLEAN_OR',
    'CLOSE_BRACE', 'COLON', 'COMMA', 'DECREMENT', 'DEREF_ARROW', 'DIVIDE',
    'DIVIDE_ASSIGN', 'ELLIPSIS', 'EQ', 'GEQ', 'GT', 'IDENTIFIER', 'INCREMENT',
    'LBRACE', 'LEFT_ASSIGN', 'LEQ', 'LPAREN', 'LSHIFT', 'LT', 'MINUS',
    'MODULUS', 'MODULUS_ASSIGN', 'MULTIPLY_ASSIGN', 'NEQ', 'NUMBER',
    'OPEN_BRACE', 'OR_ASSIGN', 'PERIOD', 'RBRACE', 'RIGHT_ASSIGN', 'RPAREN',
    'RSHIFT', 'SEMICOLON', 'STAR', 'STRING_CONSTANT', 'SUBTRACT_ASSIGN',
    'TERNARY', 'XOR_ASSIGN',
    ] + map(str.upper, reserved)

import lexer as lx
import parser as ps

lexer = lx.mklex(reserved, tokens)
parser = ps.mkparser(reserved, tokens, lexer)

def parse(string):
  return parser.parse(string)
