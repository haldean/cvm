from env import *
from cvm.parse import parse

if '-i' in sys.argv:
  try:
    import readline
  except:
    pass
  while True:
    try:
      line = read_input('> ')
      if not line.endswith(';'):
        line += ';'
    except EOFError:
      break
    if line == 'quit':
      break
    print(parse(line))
else:
  s = sys.stdin.read()
  result = parse(s)
  print(result)
