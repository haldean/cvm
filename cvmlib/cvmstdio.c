void putc(char c) {
  asm("LLOAD 0");
  asm("PRINT");
  return;
}
