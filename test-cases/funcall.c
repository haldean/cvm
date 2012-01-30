void putc(char c) {
  /* loads c and puts it on the stack. */
  c;
  asm("PRINT");
  return;
}

int main() {
  putc('a');
  putc('\n');
}
