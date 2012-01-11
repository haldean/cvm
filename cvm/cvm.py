from parse.c import parse
from util import print_tree
from translate import translate

def run(source):
  tree = parse(preprocess(source))
  print_tree(tree)
  if tree:
    translate(tree)

def preprocess(source):
  result = ''
  for line in source.split('\n'):
    if not line.startswith('#'):
      result += line + '\n'
    else:
      result += '\n'
  return result
