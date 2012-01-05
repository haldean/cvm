def mkparser(reserved, tokens, lexer):
  def p_statements(t):
    '''statements : statement statements
     | statement'''
    if len(t) == 3:
      t[0] = [t[1]] + t[2]
    else:
      t[0] = [t[1]]

  def p_statement(t):
    'statement : expression SEMICOLON'
    t[0] = t[1]

  def p_expression(t):
    'expression : assignment_expression'
    t[0] = t[1]

  def p_primary_expression(t):
    '''primary_expression : NUMBER
      | IDENTIFIER
      | STRING_CONSTANT
      | LPAREN expression RPAREN'''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = t[2]

  def p_unary_expression(t):
    '''unary_expression : primary_expression
    | INCREMENT unary_expression
    | DECREMENT unary_expression
    | unary_operator unary_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[1], t[2])

  def p_unary_operator(t):
    '''unary_operator : BITWISE_AND
    | STAR
    | ADD
    | MINUS
    | BITWISE_NOT
    | BOOLEAN_NOT
    '''
    t[0] = t[1]

  def p_cast_expression(t):
    '''cast_expression : unary_expression'''
    # TODO: actually support casts
    t[0] = t[1]

  def p_multiplicative_expression(t):
    '''multiplicative_expression : cast_expression
    | multiplicative_expression STAR cast_expression
    | multiplicative_expression DIVIDE cast_expression
    | multiplicative_expression MODULUS cast_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_additive_expression(t):
    '''additive_expression : multiplicative_expression
    | additive_expression ADD multiplicative_expression
    | additive_expression MINUS multiplicative_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_shift_expression(t):
    '''shift_expression : additive_expression
    | shift_expression LSHIFT additive_expression
    | shift_expression RSHIFT additive_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_relational_expression(t):
    '''relational_expression : shift_expression
    | relational_expression LT shift_expression
    | relational_expression GT shift_expression
    | relational_expression LEQ shift_expression
    | relational_expression GEQ shift_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_equality_expression(t):
    '''equality_expression : relational_expression
    | equality_expression EQ relational_expression
    | equality_expression NEQ relational_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_and_expression(t):
    '''and_expression : equality_expression
    | and_expression BITWISE_AND equality_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_xor_expression(t):
    '''xor_expression : and_expression
    | xor_expression BITWISE_XOR and_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_or_expression(t):
    '''or_expression : xor_expression
    | or_expression BITWISE_OR xor_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_boolean_and_expression(t):
    '''boolean_and_expression : or_expression
    | boolean_and_expression BOOLEAN_AND or_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_boolean_or_expression(t):
    '''boolean_or_expression : boolean_and_expression
    | boolean_or_expression BOOLEAN_OR boolean_and_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_conditional_expression(t):
    '''conditional_expression : boolean_or_expression
    | boolean_or_expression TERNARY expression COLON conditional_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = ('?', t[1], t[3], t[5])

  def p_assignment_expression(t):
    '''assignment_expression : conditional_expression
    | unary_expression assignment_operator assignment_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[2], t[1], t[3])

  def p_assignment_operator(t):
    '''assignment_operator : ASSIGN
    | MULTIPLY_ASSIGN
    | DIVIDE_ASSIGN
    | MODULUS_ASSIGN
    | ADD_ASSIGN
    | SUBTRACT_ASSIGN
    | LEFT_ASSIGN
    | RIGHT_ASSIGN
    | AND_ASSIGN
    | XOR_ASSIGN
    | OR_ASSIGN
    '''
    t[0] = t[1]

  def p_error(t):
    if t:
      print('Syntax error at "%s" (line %d)' % (t.value, t.lexer.lineno))
    else:
      print('Syntax error')

  import ply.yacc as yacc
  return yacc.yacc()
