from env import *
from cvm.parse import parse
from cvm.preprocessor import preprocessor
from cvm.util import print_tree

def compile(source):
  print_tree(parse(preprocessor(source)))

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
    compile(line)
else:
  if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
      s = f.read()
  else:
    s = sys.stdin.read()
  compile(s)
