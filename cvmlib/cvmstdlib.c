char *malloc(unsigned int size) {
  asm("LLOAD 0");
  asm("ALLOC -1");
  asm("RETURN");
}
