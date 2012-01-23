import ctypes

opcodes = {
    'nop': None,
    'store': 0x01,
    'load': 0x02,
    'incr': 0x03,
    'decr': 0x04,
    'not': 0x05,
    'bnot': 0x06,
    'mul': 0x07,
    'add': 0x08,
    'sub': 0x09,
    'div': 0x0A,
    'mod': 0x0B,
    'and': 0x0C,
    'or': 0x0D,
    'lsh': 0x0E,
    'rsh': 0x0F,
    'band': 0x10,
    'bor': 0x11,
    'eq': 0x12,
    'geq': 0x13,
    'leq': 0x14,
    'gt': 0x15,
    'lt': 0x16,
    'neq': 0x17,
    'xor': 0x18,
    'addr': 0x19,
    'ozjmp': 0x1A,
    'ojmp': 0x1B,
    'ldconst': 0x1C,
    'halt': 0x1D,
    }

def arg_to_binary(a):
  if a == None:
    return 0x00
  print(ctypes.c_uint8(a))
  return ctypes.c_uint8(a).value

def write_binary(code, out):
  def to_binary(line, out):
    opcode = opcodes[line[0]]
    if opcode == None:
      return
    out.write(chr(opcode))

    if len(line) == 2:
      arg = arg_to_binary(line[1])
      print(arg)
      out.write(chr(arg))
    elif len(line) > 2:
      print('Binary output can only write one-argument instructions.')
    else:
      out.write(chr(arg_to_binary(None)))

  for line in code:
    to_binary(line, out)
