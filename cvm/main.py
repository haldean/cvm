from env import *
from cvm import run

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
    run(line)
else:
  if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
      s = f.read()
  else:
    s = sys.stdin.read()
  run(s)
