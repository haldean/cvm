int main() {
  int a = 2, b, *c, **d, e = 8;
  b = a * e;
  c = &b;
  d = &c;
  b++;
}
