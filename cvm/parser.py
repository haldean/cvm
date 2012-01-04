def mkparser(reserved, tokens, lexer):
  def p_statements(t):
    '''statements : statement statements
     | statement'''
    if len(t) == 3:
      t[0] = [t[1]] + t[2]
    else:
      t[0] = [t[1]]

  def p_statement(t):
    'statement : expression'
    t[0] = t[1]

  def p_expression_constant(t):
    'expression : NUMBER'
    t[0] = t[1]

  def p_error(t):
    print('Syntax error at "%s"' % t.value)

  import ply.yacc as yacc
  return yacc.yacc()
