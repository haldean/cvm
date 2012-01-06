from parse.c import parse
from util import print_tree

def run(source):
  print_tree(parse(preprocess(source)))

def preprocess(source):
  result = ''
  for line in source.split('\n'):
    if not line.startswith('#'):
      result += line + '\n'
    else:
      result += '\n'
  return result
