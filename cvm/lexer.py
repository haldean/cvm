def mklex(reserved, tokens):
  t_ASSIGN = r'='
  t_ignore = ' \t'

  def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value.lower()
    if t.value in reserved:
      t.type = t.value
    return t

  def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

  def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)

  def t_hex_constant(t):
    r'0[xX][a-fA-F0-9]+'
    t.value = int(t.value, 16)
    t.type = 'NUMBER'
    return t

  def t_decimal_int_constant(t):
    r'[1-9][0-9]*'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t

  def t_octal_int_constant(t):
    r'0[0-7]*'
    t.value = int(t.value, 8)
    t.type = 'NUMBER'
    return t

  import ply.lex as lex
  return lex.lex()

