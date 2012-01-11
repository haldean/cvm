from function import function
import cvmtypes

def translate(root):
  glob = {}
  init_code = []
  for item in root:
    if item[0] == 'fun':
      function = translate_function(item, glob)
      glob[item[2][0][0]] = function
    elif item[0] == 'declare':
      for var, init in item[2]:
        cvmtype, name = cvmtypes.declarator((item[1], var))
        glob[name] = (cvmtype, init)
        if init:
          init_code.extend(
              translate_declaration(name, (cvmtype, init), glob))
    else:
      raise Exception('Only function definitions and declarations'
        'are allowed at top level.')

  return glob, init_code

def translate_function(ftree, glob):
  fname = ftree[2][0][0]
  fargs = list(map(cvmtypes.declarator, ftree[2][1]))
  fcode, flocals = translate_compound(ftree[3], glob)
  fret = cvmtypes.typefor(ftree[1])
  return function(fname, fcode, fargs, fret, flocals)

def add_declaration(loc, decl):
  for var, init in decl[2]:
    cvmtype, name = cvmtypes.declarator((decl[1], var))
    loc[name] = (cvmtype, init)

def translate_compound(ftree, glob):
  declarations = []
  loc = {}

  for first_statement, node in enumerate(ftree):
    if node[0] == 'declare':
      declarations.append(node)
    else:
      break

  for decl in declarations:
    add_declaration(loc, decl)

  code = []
  for var, data in loc.items():
    if data[1]:
      code.extend(translate_declaration(var, data, glob))
  for node in ftree[first_statement:]:
    code.extend(translate_statement(node, glob))

  return code, loc

def translate_declaration(var, data, glob):
  return (
      translate_statement(data[1], glob) +
      [('store', ('result', 'reg'), (var, 'var'))])

def translate_statement(ftree, glob):
  '''
  TODO:

  BREAK
  CALL
  GOTO
  RETURN
  '''
  # Assignment
  if ftree[0] == '=':
    rhs = translate_statement(ftree[2], glob)
    return rhs + [('store', ('result', 'reg'), ftree[1])]

  # Variable access
  if ftree[1] == 'var':
    return [('load', ftree)]

  # Unary operators
  if ftree[0] == '++':
    return translate_unop_expression('incr', ftree, glob)
  if ftree[0] == '--':
    return translate_unop_expression('decr', ftree, glob)
  if ftree[0] == '~':
    return translate_unop_expression('not', ftree, glob)
  if ftree[0] == '!':
    return translate_unop_expression('bnot', ftree, glob)

  # Binary operators
  if ftree[0] == '*' and len(ftree) == 3:
    return translate_binop_expression('mul', ftree, glob)
  if ftree[0] == '+':
    return translate_binop_expression('add', ftree, glob)
  if ftree[0] == '-':
    return translate_binop_expression('sub', ftree, glob)
  if ftree[0] == '/':
    return translate_binop_expression('div', ftree, glob)
  if ftree[0] == '%':
    return translate_binop_expression('mod', ftree, glob)

  if ftree[0] == '&' and len(ftree[0]) == 3:
    return translate_binop_expression('and', ftree, glob)
  if ftree[0] == '|':
    return translate_binop_expression('or', ftree, glob)
  if ftree[0] == '^':
    return translate_binop_expression('or', ftree, glob)

  if ftree[0] == '<<':
    return translate_binop_expression('lsh', ftree, glob)
  if ftree[0] == '>>':
    return translate_binop_expression('rsh', ftree, glob)

  if ftree[0] == '&&':
    return translate_binop_expression('band', ftree, glob)
  if ftree[0] == '||':
    return translate_binop_expression('bor', ftree, glob)

  # Comparison operators
  if ftree[0] == '==':
    return translate_binop_expression('eq', ftree, glob)
  if ftree[0] == '>=':
    return translate_binop_expression('geq', ftree, glob)
  if ftree[0] == '<=':
    return translate_binop_expression('leq', ftree, glob)
  if ftree[0] == '>':
    return translate_binop_expression('gt', ftree, glob)
  if ftree[0] == '<':
    return translate_binop_expression('lt', ftree, glob)
  if ftree[0] == '!=':
    return translate_binop_expression('neq', ftree, glob)

  # Assignment operators
  if ftree[0] == '+=':
    return translate_assign_expression('add', ftree, glob)
  if ftree[0] == '-=':
    return translate_assign_expression('sub', ftree, glob)
  if ftree[0] == '*=':
    return translate_assign_expression('mul', ftree, glob)
  if ftree[0] == '/=':
    return translate_assign_expression('div', ftree, glob)
  if ftree[0] == '%=':
    return translate_assign_expression('mod', ftree, glob)

  if ftree[0] == '&=':
    return translate_assign_expression('and', ftree, glob)
  if ftree[0] == '|=':
    return translate_assign_expression('or', ftree, glob)
  if ftree[0] == '^=':
    return translate_assign_expression('xor', ftree, glob)
  if ftree[0] == '>>=':
    return translate_assign_expression('rsh', ftree, glob)
  if ftree[0] == '<<=':
    return translate_assign_expression('lsh', ftree, glob)

  # Dereferencing
  if ftree[0] == '->':
    pass
  if ftree[0] == '.':
    pass
  if ftree[0] == '&':
    return [('addr', ftree[1])]
  if ftree[0] == '*':
    return (
        translate_statement(ftree[1], glob) +
        [('load', ('result', 'reg'))])

  # Conditionals
  if ftree[0] == 'if':
    code_true, ignore = translate_compound(ftree[2], glob)
    code_false, ignore = translate_compound(ftree[3], glob)
    return (
        translate_statement(ftree[1], glob) +
        # Conditional Offset Zero JuMP -- 
        # relative jump if result register == 0
        [('ozjmp', len(code_true) + 2)] +
        code_true +
        [('ojmp', len(code_false))] +
        code_false)

  if ftree[0] == '?':
    code_true = translate_statement(ftree[2], glob)
    code_false = translate_statement(ftree[3], glob)
    return (
        translate_statement(ftree[1], glob) +
        # Conditional Offset Zero JuMP -- 
        # relative jump if result register == 0
        [('ozjmp', len(code_true) + 2)] +
        code_true +
        [('ojmp', len(code_false))] +
        code_false +
        [('nop',)])

  if ftree[0] == 'while':
    condition = translate_statement(ftree[1], glob)
    code_true, ignore = translate_compound(ftree[2], glob)
    return (
        condition +
        [('ozjmp', len(code_true) + 2)] +
        code_true +
        [('ojmp', -len(code_true) - len(condition) - 1), ('nop',)])

  if ftree[0] == 'do':
    condition = translate_statement(ftree[1], glob)
    code_true, ignore = translate_compound(ftree[2], glob)
    return (
        code_true +
        condition +
        [('ozjmp', 2),
         ('ojmp', -len(code_true) - len(condition) - 1),
         ('nop',)])

  if ftree[0] == 'for':
    body, ignore = translate_compound(ftree[4], glob)
    condition = translate_statement(ftree[2], glob)
    update = []
    if ftree[3]:
      update = translate_statement(ftree[3], glob)

    return (
        translate_statement(ftree[1], glob) +
        condition +
        [('ozjmp', len(body) + len(update) + 2)] +
        body + update +
        [('ojmp', -len(body) - len(update) - len(condition) - 1), ('nop',)])

  # Numeric constant
  if 'i' in ftree[1] or 'l' in ftree[1] or 'f' in ftree[1] or 'd' in ftree[1]:
    return [('ldconst', ftree[0])]

  print('Warning: statement tree %s could not be translated.' % ftree)
  return []

def translate_unop_expression(op, ftree, glob):
  return (
      translate_statement(ftree[1], glob) + 
      [(op, ('result', 'reg'))] +
      [('store', ('result', 'reg'), ftree[1])])

def translate_binop_expression(op, ftree, glob):
  return (
      translate_statement(ftree[1], glob) +
      [('store', ('result', 'reg'), ('t0', 'reg'))] +
      translate_statement(ftree[2], glob) +
      [(op, ('result', 'reg'), ('t0', 'reg'))])

def translate_assign_expression(op, ftree, glob):
  return (
      translate_binop_expression(op, ftree, glob) +
      [('store', ('result', 'reg'), ftree[1])])
