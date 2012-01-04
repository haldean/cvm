reserved = set([
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
    'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
    'if', 'int', 'long', 'register', 'return', 'short' 'signed',
    'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned',
    'void', 'volatile', 'while'
    ])


tokens = [
    'IDENTIFIER',
    'NUMBER',
    'ASSIGN',
    'STRING_LITERAL',
    ] + map(str.upper, reserved)

import cvm.lexer as lx
import cvm.parser as ps

lexer = lx.mklex(reserved, tokens)
parser = ps.mkparser(reserved, tokens, lexer)

def parse(string):
  return parser.parse(string)
