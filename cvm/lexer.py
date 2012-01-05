def parse_integral_flags(flags):
  if not flags:
    return 'i'
  elif 'l' in flags:
    return flags
  else:
    return flags + 'i'

def parse_floatpt_flags(flags):
  if not flags:
    return 'd'
  elif 'f' in flags or 'd' in flags:
    return flags
  else:
    return flags + 'd'

def mklex(reserved, tokens):
  t_ignore = ' \t'

  def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value.lower()
    if t.value in reserved:
      t.type = t.value.upper()
    else:
      t.value = (t.value, 'i')
    return t

  def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

  def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)

  # Constants

  def t_floatpt_constant(t):
    r'(?P<value>([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)([eE][+-]?[0-9]+)?)(?P<flags>[fFlL]?)'
    t.value = (float(t.lexer.lexmatch.group('value')),
        parse_floatpt_flags(t.lexer.lexmatch.group('flags')))
    t.type = 'NUMBER'
    return t

  def t_floatpt_constant_nodecimal(t):
    r'(?P<value>([1-9][0-9]*|0))(?P<flags>[fFlLdD])'
    t.value = (float(t.lexer.lexmatch.group('value')),
        parse_floatpt_flags(t.lexer.lexmatch.group('flags')))
    t.type = 'NUMBER'
    return t

  def t_decimal_int_constant(t):
    r'(?P<value>[1-9][0-9]*)(?P<flags>[uUlL]{0,2})'
    t.value = (int(t.lexer.lexmatch.group('value')),
        parse_integral_flags(t.lexer.lexmatch.group('flags')))
    t.type = 'NUMBER'
    return t

  def t_hex_constant(t):
    r'(?P<value>0[xX][a-fA-F0-9]+)(?P<flags>[uUlL]{0,2})'
    t.value = (int(t.lexer.lexmatch.group('value'), 16),
        parse_integral_flags(t.lexer.lexmatch.group('flags')))
    t.type = 'NUMBER'
    return t

  def t_octal_int_constant(t):
    r'(?P<value>0[0-7]+)(?P<flags>[uUlL]{0,2})'
    t.value = (int(t.lexer.lexmatch.group('value'), 8),
        parse_integral_flags(t.lexer.lexmatch.group('flags')))
    t.type = 'NUMBER'
    return t

  def t_STRING_CONSTANT(t):
    r'"([^"]|\")*?"'
    t.value = (t.value[1:-1], 's')
    return t

  # Operators and other misc. punctuation

  t_ADD = r'\+'
  t_ADD_ASSIGN = r'\+\='
  t_AND_ASSIGN = r'&='
  t_ASSIGN = r'='
  t_BITWISE_AND = r'&'
  t_BITWISE_NOT = r'~'
  t_BITWISE_OR = r'\|'
  t_BITWISE_XOR = r'\^'
  t_BOOLEAN_AND = r'&&'
  t_BOOLEAN_NOT = r'\!'
  t_BOOLEAN_OR = r'\|\|'
  t_CLOSE_BRACE = r'\}'
  t_COLON = r':'
  t_COMMA = r','
  t_DECREMENT = r'\-\-'
  t_DEREF_ARROW = r'\-\>'
  t_DIVIDE = r'/'
  t_DIVIDE_ASSIGN = r'/='
  t_ELLIPSIS = r'\.\.\.'
  t_EQ = r'=='
  t_GEQ = r'\>='
  t_GT = r'\>'
  t_INCREMENT = r'\+\+'
  t_LBRACE = r'\['
  t_LEFT_ASSIGN = r'\<\<='
  t_LEQ = r'\<='
  t_LPAREN = r'\('
  t_LSHIFT = r'\<\<'
  t_LT = r'\<'
  t_MINUS = r'-'
  t_MODULUS = r'%'
  t_MODULUS_ASSIGN = r'%='
  t_MULTIPLY_ASSIGN = r'\*\='
  t_NEQ = r'!='
  t_OPEN_BRACE = r'\{'
  t_OR_ASSIGN = r'\|='
  t_PERIOD = r'\.'
  t_RBRACE = r'\]'
  t_RIGHT_ASSIGN = r'\>\>='
  t_RPAREN = r'\)'
  t_RSHIFT = r'\>\>'
  t_SEMICOLON = r';'
  t_STAR = r'\*'
  t_SUBTRACT_ASSIGN = r'-='
  t_TERNARY = r'\?'
  t_XOR_ASSIGN = r'\^='

  import ply.lex as lex
  return lex.lex()

def test_lex():
  import env
  import cvm.parse
  import sys

  lx = mklex(cvm.parse.reserved, cvm.parse.tokens)
  lx.input(' '.join(sys.argv[1:]))
  for tok in lx:
    print(tok)

if __name__ == '__main__':
  test_lex()
