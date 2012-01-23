int a = 1, b = 1;
int c = 1;

int main() {
  do {
    a = c * (a + b);
  } while (a < 6);
}
