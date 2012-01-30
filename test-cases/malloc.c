#include <cvmstdlib.c>
#include <cvmstdio.c>

int main() {
  char* addr = malloc(10);
  putc('0' + addr);
  putc('\n');
}
