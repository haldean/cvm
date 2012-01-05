from env import *
from cvm.parse import parse
from cvm.util import print_tree

if '-i' in sys.argv:
  import readline
  while True:
    try:
      line = read_input('> ')
      if not line.endswith(';'):
        line += ';'
    except EOFError:
      break
    if line == 'quit':
      break
    print_tree(parse(line))
else:
  s = sys.stdin.read()
  result = parse(s)
  print(result)
