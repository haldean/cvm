from cvmc.env import *
from cvmc.cvm import run
from argparse import ArgumentParser

def main():
  ap = ArgumentParser(description='Run the CVM compiler.')
  ap.add_argument(
      '-a', '--assemble', action='store_true',
      help='convert a file containing assembly to bytecode')
  ap.add_argument(
      '-o', '--output', default='out.cvm', metavar='BYTECODE_FILE',
      help='output bytecode file')
  ap.add_argument(
      '--print-assembly', action='store_true',
      help='write out generated assembly instructions')
  ap.add_argument(
      '--print-ast', action='store_true',
      help='write out AST')
  ap.add_argument('input_file', metavar='INPUT_FILE')

  args = ap.parse_args()
  #try:
  run(args)
  #except Exception as e:
  #  print(e)

main()
