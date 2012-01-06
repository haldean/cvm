def preprocessor(source):
  result = ''
  for line in source.split('\n'):
    if not line.startswith('#'):
      result += line + '\n'
  print(result)
  return result
