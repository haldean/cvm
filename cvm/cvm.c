#include <stdio.h>
#include <stdlib.h>
#include "opcodes.h"

int main(int argc, char** argv) {
  char **opcode_names = opcode_map();
  char opcode, argument;
  int i_opcode;
  FILE *input_file = fopen(argv[1], "rb");

  while ((i_opcode = fgetc(input_file)) != EOF) {
    opcode = (char) i_opcode;
    argument = fgetc(input_file);
    printf("%s 0x%02X (%d)\n",
        opcode_names[(unsigned int) opcode], argument, (signed int) argument);
  }

  free(opcode_names);
  return 0;
}
