#include <cvmstdio.c>

int main() {
  char x;
  for (x = 'a'; x <= 'z'; x++) {
    putc(x);
  }
  putc('\n');
}
