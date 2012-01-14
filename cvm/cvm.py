from parse.c import parse
from util import print_tree
from translate import translate
from link import link

def run(source):
  tree = parse(preprocess(source))
  print_tree(tree)
  if tree:
    link(*translate(tree))

def preprocess(source):
  result = ''
  for line in source.split('\n'):
    if not line.startswith('#'):
      result += line + '\n'
    else:
      result += '\n'
  return result
