import ctypes

ops = [
    'nop',
    'halt',
    'push',
    'pop',
    'store',
    'load',
    'incr',
    'decr',
    'not',
    'bnot',
    'mul',
    'add',
    'sub',
    'div',
    'mod',
    'and',
    'or',
    'lsh',
    'rsh',
    'band',
    'bor',
    'eq',
    'geq',
    'leq',
    'gt',
    'lt',
    'neq',
    'xor',
    'addr',
    'ozjmp',
    'onzjmp',
    'ojmp',
    'ldconst',
    'print',
    'return',
    'call',
    'lload',
    'lstore',
    'alloc',
    ]

opcodes = dict(zip(ops, range(len(ops))))

def arg_to_binary(a):
  if a == None:
    return 0x00
  return ctypes.c_uint8(a).value

def write_binary(code, out):
  def to_binary(line, out):
    opcode = opcodes[line[0]]
    if opcode == None:
      return
    out.write(chr(opcode))

    if len(line) == 2:
      arg = arg_to_binary(line[1])
      out.write(chr(arg))
    elif len(line) > 2:
      print('Binary output can only write one-argument instructions.')
    else:
      out.write(chr(arg_to_binary(None)))

  for line in code:
    to_binary(line, out)

def parse_instructions(source):
  def instr_from_line(line):
    def arg_from_str(ar):
      try:
        return int(ar)
      except:
        return ord(eval(ar)[0])

    args = map(str.lower, line.split(' '))
    args[1:] = map(arg_from_str, args[1:])
    return tuple(args)

  instructions = map(instr_from_line, filter(lambda x: x, source.split('\n')))
  return instructions

def generate_c_header():
  print('#ifndef __CVM_OPCODES__\n#define __CVM_OPCODES__')
  print('/* DO NOT EDIT: AUTOMATICALLY GENERATED BY cvmc/binary.py */\n')
  print('#include <stdlib.h>')

  for op in ops:
    print('#define %s %d' % (op.upper(), opcodes[op]))

  print('char **opcode_map() {')
  print('  char **opcode_names = malloc(%d * sizeof(char *));' % (len(ops),))

  for op in ops:
    print('  opcode_names[%s] = "%s";' % (op.upper(), op.upper()))

  print('  return opcode_names;\n}\n#endif')

if __name__ == '__main__':
  generate_c_header()
