from parse.c import parse
from util import print_tree, print_instructions
from translate import translate
from link import link
from binary import write_binary, parse_instructions
from preprocess import preprocess

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
    if args.print_ast:
      print_tree(tree)
    if not tree:
      return

    instructions = link(*translate(tree))
    if args.print_assembly:
      print_instructions(instructions)

    with open(args.output, 'w') as binout:
      write_binary(instructions, binout)
