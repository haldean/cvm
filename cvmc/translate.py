from binary import parse_instructions
from function import function
from link import is_var
import cvmtypes

def translate(root):
  glob = {}
  funcs = {}

  init_code = []
  for item in root:
    if item[0] == 'fun':
      func = translate_function(item, glob, funcs)
      funcs[item[2][0][0]] = func
    elif item[0] == 'declare':
      for var, init in item[2]:
        cvmtype, name = cvmtypes.declarator((item[1], var))
        glob[name] = (cvmtype, init)
        if init:
          init_code.extend(
              translate_declaration(name, (cvmtype, init), glob, funcs))
    else:
      raise Exception('Only function definitions and declarations'
        'are allowed at top level.')

  return glob, funcs, init_code

def translate_function(ftree, glob, funcs):
  fname = ftree[2][0][0]
  fargs = list(map(cvmtypes.declarator, ftree[2][1]))
  fcode, flocals = translate_compound(ftree[3], glob, funcs)
  if 'void' in ftree[1]:
    fret = None
  else:
    fret = cvmtypes.typefor(ftree[1])

  func = function(fname, [], fargs, fret, flocals)

  # Calculate storage required for stack frame
  func.frame_size = 0
  local_addr_offsets = {}

  for cvmtype, name in fargs:
    local_addr_offsets[name] = func.frame_size
    func.frame_size += cvmtype.bytecount

  for name, cvmtype in map(lambda x: (x[0], x[1][0]), flocals.items()):
    local_addr_offsets[name] = func.frame_size
    func.frame_size += cvmtype.bytecount

  prepend = []
  for name, init in map(lambda x: (x[0], x[1][1]), flocals.items()):
    if init:
      prepend += translate_statement(init, glob, funcs)
      prepend.append(('lstore', local_addr_offsets[name]))

  for cvmtype, name in reversed(fargs):
    prepend.append(('lstore', local_addr_offsets[name]))
  fcode = prepend + fcode

  for line in fcode:
    if len(line) > 1 and is_var(line[1]) and line[1][0] in local_addr_offsets:
      if line[0] in ['load', 'store']:
        func.code.append(('l%s' % line[0], local_addr_offsets[line[1][0]]))
      else:
        raise Exception('Accessed non-register memory in an instruction other'
            ' than load and store')
    else:
      func.code.append(line)

  return func

def add_declaration(loc, decl):
  for var, init in decl[2]:
    cvmtype, name = cvmtypes.declarator((decl[1], var))
    loc[name] = (cvmtype, init)

def translate_compound(ftree, glob, funcs):
  if not ftree: return [], {}

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
      code.extend(translate_declaration(var, data, glob, funcs))
  for node in ftree[first_statement:]:
    code.extend(translate_statement(node, glob, funcs))

  return code, loc

def translate_declaration(var, data, glob, funcs):
  return (
      translate_statement(data[1], glob, funcs) +
      [('store', (var, 'var'))])

def translate_statement(ftree, glob, funcs):
  '''
  TODO:

  BREAK
  GOTO
  '''
  # Assignment
  if ftree[0] == '=':
    rhs = translate_statement(ftree[2], glob, funcs)
    return rhs + [('store', ftree[1])]

  # Variable access
  if ftree[1] == 'var':
    return [('load', ftree)]

  # Call stack-related
  if ftree[0] == 'call':
    # Calls to asm() skip translation and go straight to instruction parser.
    if ftree[1][0] == 'asm':
      return parse_instructions(ftree[2][0][0])
    func = funcs[ftree[1][0]]
    if len(func.args) != len(ftree[2]):
      raise Exception('Not enough arguments to function "%s"' % ftree[1][0])

    arg_evals = []
    for arg in ftree[2]:
      arg_evals.extend(translate_statement(arg, glob, funcs))
    funcpair = (ftree[1][0], 'func')
    return arg_evals + [('ldconst', funcpair), ('call', funcpair)]

  if ftree[0] == 'return':
    if ftree[1]:
      return translate_statement(ftree[1], glob, funcs) + [('return',)]
    else:
      return [('return',)]

  # Unary operators
  if ftree[0] == '++':
    return translate_unop_expression('incr', ftree, glob, funcs)
  if ftree[0] == '--':
    return translate_unop_expression('decr', ftree, glob, funcs)
  if ftree[0] == '~':
    return translate_unop_expression('not', ftree, glob, funcs)
  if ftree[0] == '!':
    return translate_unop_expression('bnot', ftree, glob, funcs)

  # Binary operators
  if ftree[0] == '*' and len(ftree) == 3:
    return translate_binop_expression('mul', ftree, glob, funcs)
  if ftree[0] == '+':
    return translate_binop_expression('add', ftree, glob, funcs)
  if ftree[0] == '-':
    return translate_binop_expression('sub', ftree, glob, funcs)
  if ftree[0] == '/':
    return translate_binop_expression('div', ftree, glob, funcs)
  if ftree[0] == '%':
    return translate_binop_expression('mod', ftree, glob, funcs)

  if ftree[0] == '&' and len(ftree[0]) == 3:
    return translate_binop_expression('and', ftree, glob, funcs)
  if ftree[0] == '|':
    return translate_binop_expression('or', ftree, glob, funcs)
  if ftree[0] == '^':
    return translate_binop_expression('xor', ftree, glob, funcs)

  if ftree[0] == '<<':
    return translate_binop_expression('lsh', ftree, glob, funcs)
  if ftree[0] == '>>':
    return translate_binop_expression('rsh', ftree, glob, funcs)

  if ftree[0] == '&&':
    return translate_binop_expression('band', ftree, glob, funcs)
  if ftree[0] == '||':
    return translate_binop_expression('bor', ftree, glob, funcs)

  # Comparison operators
  if ftree[0] == '==':
    return translate_binop_expression('eq', ftree, glob, funcs)
  if ftree[0] == '>=':
    return translate_binop_expression('geq', ftree, glob, funcs)
  if ftree[0] == '<=':
    return translate_binop_expression('leq', ftree, glob, funcs)
  if ftree[0] == '>':
    return translate_binop_expression('gt', ftree, glob, funcs)
  if ftree[0] == '<':
    return translate_binop_expression('lt', ftree, glob, funcs)
  if ftree[0] == '!=':
    return translate_binop_expression('neq', ftree, glob, funcs)

  # Assignment operators
  if ftree[0] == '+=':
    return translate_assign_expression('add', ftree, glob, funcs)
  if ftree[0] == '-=':
    return translate_assign_expression('sub', ftree, glob, funcs)
  if ftree[0] == '*=':
    return translate_assign_expression('mul', ftree, glob, funcs)
  if ftree[0] == '/=':
    return translate_assign_expression('div', ftree, glob, funcs)
  if ftree[0] == '%=':
    return translate_assign_expression('mod', ftree, glob, funcs)

  if ftree[0] == '&=':
    return translate_assign_expression('and', ftree, glob, funcs)
  if ftree[0] == '|=':
    return translate_assign_expression('or', ftree, glob, funcs)
  if ftree[0] == '^=':
    return translate_assign_expression('xor', ftree, glob, funcs)
  if ftree[0] == '>>=':
    return translate_assign_expression('rsh', ftree, glob, funcs)
  if ftree[0] == '<<=':
    return translate_assign_expression('lsh', ftree, glob, funcs)

  # Dereferencing
  if ftree[0] == '->':
    pass
  if ftree[0] == '.':
    pass
  if ftree[0] == '&':
    return [('addr', ftree[1])]
  if ftree[0] == '*':
    return (
        translate_statement(ftree[1], glob, funcs) +
        [('load', ('result', 'reg'))])

  # Conditionals
  if ftree[0] == 'if':
    code_true, ignore = translate_compound(ftree[2], glob, funcs)
    code_false, ignore = translate_compound(ftree[3], glob, funcs)
    return (
        translate_statement(ftree[1], glob, funcs) +
        # Conditional Offset Zero JuMP -- 
        # relative jump if result register == 0
        [('ozjmp', len(code_true) + 2)] +
        code_true +
        [('ojmp', len(code_false))] +
        code_false)

  if ftree[0] == '?':
    code_true = translate_statement(ftree[2], glob, funcs)
    code_false = translate_statement(ftree[3], glob, funcs)
    return (
        translate_statement(ftree[1], glob, funcs) +
        # Conditional Offset Zero JuMP -- 
        # relative jump if result register == 0
        [('ozjmp', len(code_true) + 2)] +
        code_true +
        [('ojmp', len(code_false))] +
        code_false +
        [('nop',)])

  if ftree[0] == 'while':
    condition = translate_statement(ftree[1], glob, funcs)
    code_true, ignore = translate_compound(ftree[2], glob, funcs)
    return (
        condition +
        [('ozjmp', len(code_true) + 2)] +
        code_true +
        [('ojmp', -len(code_true) - len(condition) - 1), ('nop',)])

  if ftree[0] == 'do':
    condition = translate_statement(ftree[1], glob, funcs)
    code_true, ignore = translate_compound(ftree[2], glob, funcs)
    return (
        code_true +
        condition +
        [('ozjmp', 2),
         ('ojmp', -len(code_true) - len(condition) - 1),
         ('nop',)])

  if ftree[0] == 'for':
    body, ignore = translate_compound(ftree[4], glob, funcs)
    condition = translate_statement(ftree[2], glob, funcs)
    update = []
    if ftree[3]:
      update = translate_statement(ftree[3], glob, funcs)

    return (
        translate_statement(ftree[1], glob, funcs) +
        condition +
        [('ozjmp', len(body) + len(update) + 2)] +
        body + update +
        [('ojmp', -len(body) - len(update) - len(condition) - 1), ('nop',)])

  # Numeric constant
  if ('i' in ftree[1] or 'l' in ftree[1] or
      'f' in ftree[1] or 'd' in ftree[1] or
      'c' in ftree[1]):
    return [('ldconst', ftree[0])]

  print('Warning: statement tree %s could not be translated.' % (ftree,))
  return []

def translate_unop_expression(op, ftree, glob, funcs):
  return (
      translate_statement(ftree[1], glob, funcs) + 
      [(op,), ('store', ftree[1])])

def translate_binop_expression(op, ftree, glob, funcs):
  return (
      translate_statement(ftree[1], glob, funcs) +
      translate_statement(ftree[2], glob, funcs) +
      [(op,)])

def translate_assign_expression(op, ftree, glob, funcs):
  return (
      translate_binop_expression(op, ftree, glob, funcs) +
      [('store', ftree[1])])
