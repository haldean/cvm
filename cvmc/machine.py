import collections
import numpy

class machine(object):
  def __init__(self, heap_size, stack_size, code):
    self.stack_size = stack_size
    self.heap_start_addr = stack_size + 1
    self.heap_size = heap_size
    self.stack_top = 0

    self.memory = numpy.empty(heap_size, dtype=numpy.int8)
    self.code = code

  def push_frame(frame):
    for i, byte in enumerate(frame.encode()):
      self.memory[i + self.stack_top] = byte

  def run(self):
    print('Run machine:')
    print(self.code)


class stackframe(object):
  def __init__(
      self, retaddr, params, loc):
    pass

  def encode(self):
    pass
