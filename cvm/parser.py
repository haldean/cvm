names = { }

def mkparser(reserved, tokens, lexer):
  def p_statements(t):
    '''statements : statement statements
     | statement'''
    if len(t) == 3:
      t[0] = t[2]
    else:
      t[0] = t[1]

  def p_statement(t):
    'statement : assignment'
    t[0] = names

  def p_statement_assign(t):
    'assignment : IDENTIFIER ASSIGN expression'
    names[t[1]] = t[3]

  def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

  def p_expression_ident(t):
    'expression : IDENTIFIER'
    try:
      t[0] = names[t[1]]
    except LookupError:
      print('Variable referenced before assigned')
      t[0] = None

  def p_error(t):
    print('Syntax error at "%s"' % t.value)

  import ply.yacc as yacc
  return yacc.yacc()
