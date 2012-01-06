from function import function
import cvmtypes

def translate(root):
  glob = {'printf':'printf'}
  for item in root:
    if item[0] == 'fun':
      function = translate_function(item, glob)
      glob[item[2][0][0]] = function
    elif item[0] == 'declare':
      pass
    else:
      raise Exception('Only function definitions and declarations'
        'are allowed at top level.')
  print glob

def translate_function(ftree, glob):
  fname = ftree[2][0][0]
  fargs = ftree[2][1]
  fcode, flocals = None, None #translate_compound(ftree[3])
  fret = cvmtypes.typefor(ftree[1])
  return function(fname, fcode, fargs, fret, flocals)
