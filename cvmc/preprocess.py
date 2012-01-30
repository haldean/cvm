import os

include_paths = ['.', './cvmlib']

def expand_directive(line, defs):
  command, args = line.split(' ', 1)
  if command == '#include':
    path = args.strip('<>" ')
    for searchdir in include_paths:
      try:
        with open(searchdir + '/' + path) as f:
          return f.read()
      except IOError:
        pass
    raise Exception(
        'Could not find included file %s in paths %s.' % (path, include_paths))

def preprocess(source):
  result = ''
  for line in source.split('\n'):
    if not line.startswith('#'):
      result += line + '\n'
    else:
      result += expand_directive(line, {})
  return result
