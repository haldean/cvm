from parse.c import parse
from util import print_tree
from translate import translate
from link import link
from binary import write_binary

def run(source):
  tree = parse(preprocess(source))
  print_tree(tree)
  if tree:
    with open('out.cvm', 'w') as binout:
      write_binary(link(*translate(tree)), binout)

def preprocess(source):
  result = ''
  for line in source.split('\n'):
    if not line.startswith('#'):
      result += line + '\n'
    else:
      result += '\n'
  return result
