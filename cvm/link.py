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

  print(func_locations)
  for c in code:
    print(c)
