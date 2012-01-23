import ctypes

ops = [
    'nop',
    'halt',
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
    'ojmp',
    'ldconst',
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

def generate_c_header():
  for op in ops:
    print('#define %s 0x%02X' % (op.upper(), opcodes[op]))

if __name__ == '__main__':
  generate_c_header()
