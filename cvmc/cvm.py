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
    if args.write_ast:
      print_tree(tree)
    if not tree:
      return

    instructions = link(*translate(tree))
    if args.write_assembly:
      for c in instructions:
        print(c)

    with open(args.output, 'w') as binout:
      write_binary(instructions, binout)

def preprocess(source):
  result = ''
  for line in source.split('\n'):
    if not line.startswith('#'):
      result += line + '\n'
    else:
      result += '\n'
  return result
