from parse.c import parse
from util import print_tree
from translate import translate
from link import link
from binary import write_binary, parse_instructions

def run(args):
  if args.input_file:
    with open(args.input_file, 'r') as input_file:
      source = input_file.read()
  else:
    import sys
    source = sys.stdin.read()

  if args.assemble:
    with open(args.output, 'w') as binout:
      write_binary(parse_instructions(source), binout)
  else:
    tree = parse(preprocess(source))
    print_tree(tree)
    if tree:
      with open(args.output, 'w') as binout:
        write_binary(link(*translate(tree)), binout)

def preprocess(source):
  result = ''
  for line in source.split('\n'):
    if not line.startswith('#'):
      result += line + '\n'
    else:
      result += '\n'
  return result
