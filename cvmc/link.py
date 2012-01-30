def link(glob, funcs, init_code):
  code = [('ldconst', funcs['main'].frame_size), ('call', ('main', 'func'))]
  code.extend(init_code)
  func_locations = {}

  # Add main method first, so it naturally executes first.
  func_locations['main'] = len(code)
  code.extend(funcs['main'].code)
  code.append(('halt',))

  for func, codeobj in funcs.items():
    if func == 'main':
      continue
    func_locations[func] = len(code)
    code.extend(codeobj.code)

  code = replace_function_addresses(code, funcs, func_locations)
  code = static_allocate(code, glob)
  return code

def is_var(term):
  return isinstance(term, tuple) and len(term) == 2 and term[1] == 'var'

def is_func(term):
  return isinstance(term, tuple) and len(term) == 2 and term[1] == 'func'

def replace_function_addresses(code, funcs, func_locations):
  gen = []
  for line in code:
    if line[0] == 'call' and len(line) > 1 and is_func(line[1]):
      gen.append((line[0], func_locations[line[1][0]]))
    elif line[0] == 'ldconst' and len(line) > 1 and is_func(line[1]):
      gen.append((line[0], funcs[line[1][0]].frame_size))
    else:
      gen.append(line)
  return gen

def static_allocate(code, glob):
  glob_locations = {}
  next_location = 0
  for var, spec in glob.items():
    # spec is a 2-tuple of type, init value
    glob_locations[var] = next_location
    next_location += spec[0].bytecount

  gen = []
  for line in code:
    terms = list(line)
    if len(line) > 1 and is_var(line[1]):
      terms[1] = glob_locations[line[1][0]]
    elif len(line) > 2:
      raise Exception('Only support 1 argument per instruction in linker')
    gen.append(tuple(terms))
  return gen
