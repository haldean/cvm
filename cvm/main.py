from env import *
from cvm.parse import parse

if '-i' in sys.argv:
  while True:
    try:
      line = read_input('> ')
    except EOFError:
      break
    if line == 'quit':
      break
    print(parse(line))
else:
  s = sys.stdin.read()
  result = parse(s)
  print(result)
