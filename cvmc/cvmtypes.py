class cvmtype(object):
  def __init__(self, bytecount, signed, integral):
    self.bytecount = bytecount
    self.signed = signed
    self.integral = integral

  def __str__(self):
    return '<cvmtype %d-byte %s %s>' % (
        self.bytecount, self.signed == 's' and 'signed' or 'unsigned',
        self.integral == 'i' and 'integer' or 'floating-point')
  __repr__ = __str__

class cvmptr(object):
  bytecount = 1

  def __init__(self, pointsto):
    self.pointsto = pointsto

  def __str__(self):
    return '<ptr %s>' % self.pointsto
  __repr__ = __str__

cvmtypes = {
    'char'    : cvmtype(1, 's', 'i'),
    'uchar'   : cvmtype(1, 'u', 'i'),
    'short'   : cvmtype(2, 's', 'i'),
    'ushort'  : cvmtype(2, 'u', 'i'),
    'int'     : cvmtype(4, 's', 'i'),
    'uint'    : cvmtype(4, 'u', 'i'),
    'long'    : cvmtype(8, 's', 'i'),
    'ulong'   : cvmtype(8, 'u', 'i'),
    'llong'   : cvmtype(16, 's', 'i'),
    'ullong'  : cvmtype(16, 'u', 'i'),
    'float'   : cvmtype(32, 's', 'f'),
    'double'  : cvmtype(64, 's', 'f'),
    'ldouble' : cvmtype(128, 's', 'f'),
    }

def declarator(declarator):
  if isinstance(declarator[0], list):
    ctype = typefor(declarator[0])
    if isinstance(declarator[1][0], list):
      for ptr in declarator[1][0]:
        if ptr == '*':
          ctype = cvmptr(ctype)
      return (ctype, declarator[1][1][0])
    return (typefor(declarator[0]), declarator[1][0])
  return (cvmtypes['int'], declarator[0])

def typefor(types):
  types = set(types)
  if 'char' in types:
    if 'unsigned' in types:
      return cvmtypes['uchar']
    else:
      return cvmtypes['char']
  if 'short' in types:
    if 'unsigned' in types:
      return cvmtypes['ushort']
    else:
      return cvmtypes['short']
  if 'long' in types and 'double' not in types:
    if types.count('long') == 1:
      if 'unsigned' in types:
        return cvmtypes['ulong']
      else:
        return cvmtypes['long']
    if types.count('long') == 2:
      if 'unsigned' in types:
        return cvmtypes['ullong']
      else:
        return cvmtypes['llong']
  if 'int' in types:
    if 'unsigned' in types:
      return cvmtypes['uint']
    else:
      return cvmtypes['int']
  if 'float' in types:
    return cvmtypes['float']
  if 'double' in types and 'long' in types:
    return cvmtypes['ldouble']
  if 'double' in types:
    return cvmtypes['double']
  raise Exception('Type defined by specifier %s not available.' % types)

