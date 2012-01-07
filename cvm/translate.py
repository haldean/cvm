from function import function
import cvmtypes

def translate(root):
  glob = {}
  for item in root:
    if item[0] == 'fun':
      function = translate_function(item, glob)
      glob[item[2][0][0]] = function
    elif item[0] == 'declare':
      pass
    else:
      raise Exception('Only function definitions and declarations'
        'are allowed at top level.')

  for k, v in glob.items():
    print('%s: %s' % (k, v))
  for c in glob['main'].code:
    print(c)

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
  for node in ftree[first_statement:]:
    code.extend(translate_statement(node))

  return code, loc

def translate_statement(ftree):
  # Assignment
  if ftree[0] == '=':
    rhs = translate_statement(ftree[2])
    return rhs + [('store', ('result', 'reg'), ftree[1])]

  # Variable access
  if ftree[1] == 'var':
    return [('load', ftree)]

  # Unary arithmetic operators
  if ftree[0] == '++':
    return translate_unop_expression(('incr', ('result', 'reg')), ftree)
  if ftree[0] == '--':
    return translate_unop_expression(('decr', ('result', 'reg')), ftree)

  # Binary arithmetic operators
  if ftree[0] == '*':
    return translate_binop_expression('mul', ftree)
  if ftree[0] == '+':
    return translate_binop_expression('add', ftree)
  if ftree[0] == '-':
    return translate_binop_expression('sub', ftree)
  if ftree[0] == '/':
    return translate_binop_expression('div', ftree)

  if ftree[0] == '&':
    return [('addr', ftree[1])]
  return []

def translate_unop_expression(op, ftree):
  return (
      translate_statement(ftree[1]) + [op] +
      [('store', ('result', 'reg'), ftree[1])])

def translate_binop_expression(op, ftree):
  return (
      translate_statement(ftree[1]) +
      [('store', ('result', 'reg'), ('t0', 'reg'))] +
      translate_statement(ftree[2]) +
      [(op, ('result', 'reg'), ('t0', 'reg'))])
