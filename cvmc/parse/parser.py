# Heavily inspired by Jeff Lee's Yacc grammar, by way of Jutta Degener's 1995
# post (http://www.lysator.liu.se/c/ANSI-C-grammar-y.html)

def mkparser(reserved, tokens, lexer):
  def p_translation_unit(t):
    '''translation_unit : external_declaration
    | translation_unit external_declaration
    '''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = t[1] + [t[2]]

  def p_external_declaration(t):
    '''external_declaration : function_definition
    | declaration'''
    t[0] = t[1]

  def p_function_definition(t):
    '''function_definition : declaration_specifiers declarator compound_statement
    '''
    # TODO: support all function definitions
    t[0] = ('fun', t[1], t[2], t[3])

  # Statements

  def p_statement(t):
    '''statement : expression_statement
    | compound_statement
    | selection_statement
    | iteration_statement
    | jump_statement
    '''
    # TODO: label statement
    t[0] = t[1]

  def p_statement_list(t):
    '''statement_list : statement
    | statement_list statement'''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = t[1] + [t[2]]

  def p_jump_statement(t):
    '''jump_statement : GOTO IDENTIFIER SEMICOLON
    | CONTINUE SEMICOLON
    | BREAK SEMICOLON
    | RETURN SEMICOLON
    | RETURN expression SEMICOLON
    '''
    if t[1].lower() == 'goto':
      t[0] = ('goto', t[2])
    elif t[1].lower() == 'return':
      if len(t) == 3:
        val = None
      else:
        val = t[2]
      t[0] = ('return', val)
    else:
      t[0] = t[1]

  def p_iteration_statement(t):
    '''iteration_statement : WHILE LPAREN expression RPAREN statement
    | DO statement WHILE LPAREN expression RPAREN SEMICOLON
    | FOR LPAREN expression_statement expression_statement RPAREN statement
    | FOR LPAREN expression_statement expression_statement expression RPAREN statement
    '''
    if t[1].lower() == 'while':
      t[0] = ('while', t[3], t[5])
    elif t[1].lower() == 'do':
      t[0] = ('do', t[5], t[2])
    else:
      if len(t) == 7:
        update = None
        body = t[6]
      else:
        update = t[5]
        body = t[7]
      t[0] = ('for', t[3], t[4], update, body)

  def p_compound_statement(t):
    '''compound_statement : OPEN_BRACE CLOSE_BRACE
    | OPEN_BRACE statement_list CLOSE_BRACE
    | OPEN_BRACE declaration_list CLOSE_BRACE
    | OPEN_BRACE declaration_list statement_list CLOSE_BRACE
    '''
    if len(t) == 3:
      t[0] = None
    elif len(t) == 4:
      t[0] = t[2]
    else:
      t[0] = t[2] + t[3]

  def p_expression_statement(t):
    '''expression_statement : expression SEMICOLON
    | SEMICOLON'''
    if t[1] == ';':
      t[0] = None
    else:
      t[0] = t[1]

  def p_selection_statement(t):
    '''selection_statement : IF LPAREN expression RPAREN statement
    | IF LPAREN expression RPAREN statement ELSE statement
    '''
    # TODO: support switch
    if len(t) == 6:
      el = None
    else:
      el = t[7]
    t[0] = ('if', t[3], t[5], el)

  # Expressions

  def p_expression(t):
    'expression : assignment_expression'
    t[0] = t[1]

  def p_constant_expression(t):
    'constant_expression : conditional_expression'
    t[0] = t[1]

  def p_primary_expression(t):
    '''primary_expression : NUMBER
      | IDENTIFIER
      | string_literal
      | LPAREN expression RPAREN'''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = t[2]

  def p_string_literal(t):
    '''string_literal : STRING_CONSTANT
    | string_literal STRING_CONSTANT
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = t[1] + t[2]

  def p_postfix_expression(t):
    '''postfix_expression : primary_expression
    | postfix_expression LBRACE expression RBRACE
    | postfix_expression LPAREN RPAREN
    | postfix_expression LPAREN argument_expression_list RPAREN
    | postfix_expression PERIOD IDENTIFIER
    | postfix_expression DEREF_ARROW IDENTIFIER
    | postfix_expression INCREMENT
    | postfix_expression DECREMENT
    '''
    if len(t) == 2:
      t[0] = t[1]
    elif len(t) == 3:
      t[0] = (t[2], t[1])
    elif len(t) == 4:
      if t[2] == '.' or t[2] == '->':
        t[0] = (t[2], t[1], t[3])
      else:
        t[0] = ('call', t[1], [])
    elif len(t) == 5:
      if t[2] == '[':
        t[0] = ('array', t[1], t[3])
      else:
        t[0] = ('call', t[1], t[3])

  def p_argument_expression_list(t):
    '''argument_expression_list : assignment_expression
    | argument_expression_list COMMA assignment_expression
    '''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = t[1] + [t[2]]

  def p_unary_expression(t):
    '''unary_expression : postfix_expression
    | INCREMENT unary_expression
    | DECREMENT unary_expression
    | SIZEOF unary_expression
    | unary_operator unary_expression
    '''
    if len(t) == 2:
      t[0] = t[1]
    elif len(t) == 3:
      t[0] = (t[1].lower(), t[2])
    else:
      t[0] = (t[1].lower(), t[3])

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

  # Declarations

  def p_declaration(t):
    '''declaration : declaration_specifiers init_declarator_list SEMICOLON'''
    t[0] = ('declare', t[1], t[2])

  def p_declaration_list(t):
    '''declaration_list : declaration
    | declaration_list declaration'''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = t[1] + [t[2]]

  def p_declaration_specifiers(t):
    '''declaration_specifiers : storage_class_specifier
    | storage_class_specifier declaration_specifiers
    | type_specifier
    | type_specifier declaration_specifiers
    | type_qualifier
    | type_qualifier declaration_specifiers
    '''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = [t[1]] + t[2]

  def p_storage_class(t):
    '''storage_class_specifier : TYPEDEF
    | EXTERN
    | STATIC
    | AUTO
    | REGISTER
    '''
    t[0] = t[1]

  def p_type(t):
    '''type_specifier : VOID
    | CHAR
    | SHORT
    | INT
    | LONG
    | FLOAT
    | DOUBLE
    | SIGNED
    | UNSIGNED
    '''
    t[0] = t[1]

  def p_type_qualifier(t):
    '''type_qualifier : CONST
    | VOLATILE
    '''
    t[0] = t[1]

  def p_init_declarator_list(t):
    '''init_declarator_list : init_declarator
    | init_declarator_list COMMA init_declarator
    '''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = t[1] + [t[3]]

  def p_init_declarator(t):
    '''init_declarator : declarator
    | declarator ASSIGN initializer'''
    if len(t) == 2:
      t[0] = (t[1], None)
    else:
      t[0] = (t[1], t[3])

  def p_declarator(t):
    '''declarator : direct_declarator
    | pointer direct_declarator'''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = (t[1], t[2])

  def p_initializer(t):
    '''initializer : assignment_expression'''
    # TODO: support initializer lists
    t[0] = t[1]

  def p_pointer(t):
    '''pointer : STAR
    | STAR type_qualifier_list
    | STAR pointer
    | STAR type_qualifier_list pointer
    '''
    if len(t) == 2:
      t[0] = [t[1]]
    elif len(t) == 3:
      t[0] = [t[1]] + t[2]
    else:
      t[0] = [t[1]] + t[2] + t[3]

  def p_type_qualifier_list(t):
    '''type_qualifier_list : type_qualifier
    | type_qualifier_list type_qualifier
    '''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = t[1] + [t[2]]

  def p_direct_declarator(t):
    '''direct_declarator : IDENTIFIER
    | LPAREN declarator RPAREN
    | direct_declarator LBRACE constant_expression RBRACE
    | direct_declarator LBRACE RBRACE
    '''
    # Declarators are a 2-tuple of (identifier, array-size). array-size is None
    # for scalars.
    if len(t) == 2:
      t[0] = t[1]
    elif t[1] == '(':
      t[0] = t[2]
    else:
      if len(t) == 5:
        arrsize = t[3]
      else:
        arrsize = 0
      # array tuple: (identifier, type (with 'a' for array), array size)
      t[0] = (t[1][0], t[1][1] + 'a', arrsize)
  
  def p_function_declarator(t):
    '''direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN
    | direct_declarator LPAREN identifier_list RPAREN
    | direct_declarator LPAREN RPAREN'''
    if len(t) == 4:
      args = []
    else:
      args = t[3]
    t[0] = (t[1], args)

  def p_parameter_type_list(t):
    '''parameter_type_list : parameter_list
    | parameter_list COMMA ELLIPSIS
    '''
    if len(t) == 2:
      t[0] = t[1]
    else:
      t[0] = t[1] + [t[3]]

  def p_parameter_list(t):
    '''parameter_list : parameter_declaration
    | parameter_list COMMA parameter_declaration
    '''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = t[1] + [t[3]]

  def p_parameter_declaration(t):
    '''parameter_declaration : declaration_specifiers declarator
    | declaration_specifiers
    '''
    if len(t) == 2:
      t[0] = (t[1], None)
    else:
      t[0] = (t[1], t[2])

  def p_identifier_list(t):
    '''identifier_list : IDENTIFIER
    | identifier_list COMMA IDENTIFIER
    '''
    if len(t) == 2:
      t[0] = [t[1]]
    else:
      t[0] = t[1] + [t[3]]

  # Plumbing

  def p_error(t):
    if t:
      print('Syntax error at "%s" (line %d)' % (t.value, t.lexer.lineno))
    else:
      print('Syntax error')

  import ply.yacc as yacc
  return yacc.yacc(outputdir='./cvmc/', debug=False)
