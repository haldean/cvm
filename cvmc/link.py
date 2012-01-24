def link(glob, funcs, init_code):
  code = []
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

  code = replace_function_addresses(code, func_locations)
  code = static_allocate(code, glob)
  return code

def is_var(term):
  return isinstance(term, tuple) and len(term) == 2 and term[1] == 'var'

def replace_function_addresses(code, func_locations):
  def replace_for_instruction(instr):
    def arg_sub(arg):
      if isinstance(arg, tuple) and len(arg) == 2 and arg[1] == 'func':
        return func_locations[arg[0]]
      else: return arg
    return tuple(map(arg_sub, instr))
  return map(replace_for_instruction, code)

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
    if len(line) > 2 and is_var(line[2]):
      terms[2] = glob_locations[line[2][0]]
    gen.append(tuple(terms))
  return gen
