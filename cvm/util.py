def all_scalar(iterable):
  for item in iterable:
    if isinstance(item, list) or isinstance(item, tuple):
      return False
  return True

def print_tree(root, tablvl=0):
  if isinstance(root, list):
    if len(root) <= 2 and all_scalar(root):
      print('  ' * tablvl + str(root))
    else:
      print('  ' * tablvl + '[')
      for item in root:
        print_tree(item, tablvl=tablvl+1)
      print('  ' * tablvl + ']')

  elif isinstance(root, tuple):
    if len(root) <= 2 and all_scalar(root):
      print('  ' * tablvl + str(root))
    else:
      print('  ' * tablvl + '(')
      for item in root:
        print_tree(item, tablvl=tablvl+1)
      print('  ' * tablvl + ')')

  else:
    if root != None:
      print('  ' * tablvl + str(root))
    else:
      print('  ' * tablvl + 'None')
