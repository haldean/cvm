class function(object):
  def __init__(self, name, code, args, retype, loc):
    self.name = name
    self.code = code
    self.args = args
    self.retype = retype
    self.loc = loc
    self.frame_size = 0

  def __str__(self):
    return 'function %s: %s -> %s' % (self.name, self.args, self.retype)
  __repr__ = __str__
