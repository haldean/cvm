#ifndef __CVM_OPCODES__
#define __CVM_OPCODES__
/* DO NOT EDIT: AUTOMATICALLY GENERATED BY cvmc/binary.py */

#include <stdlib.h>
#define NOP 0
#define HALT 1
#define PUSH 2
#define POP 3
#define STORE 4
#define LOAD 5
#define INCR 6
#define DECR 7
#define NOT 8
#define BNOT 9
#define MUL 10
#define ADD 11
#define SUB 12
#define DIV 13
#define MOD 14
#define AND 15
#define OR 16
#define LSH 17
#define RSH 18
#define BAND 19
#define BOR 20
#define EQ 21
#define GEQ 22
#define LEQ 23
#define GT 24
#define LT 25
#define NEQ 26
#define XOR 27
#define ADDR 28
#define OZJMP 29
#define ONZJMP 30
#define OJMP 31
#define LDCONST 32
#define PRINT 33
char **opcode_map() {
  char **opcode_names = malloc(34 * sizeof(char *));
  opcode_names[NOP] = "NOP";
  opcode_names[HALT] = "HALT";
  opcode_names[PUSH] = "PUSH";
  opcode_names[POP] = "POP";
  opcode_names[STORE] = "STORE";
  opcode_names[LOAD] = "LOAD";
  opcode_names[INCR] = "INCR";
  opcode_names[DECR] = "DECR";
  opcode_names[NOT] = "NOT";
  opcode_names[BNOT] = "BNOT";
  opcode_names[MUL] = "MUL";
  opcode_names[ADD] = "ADD";
  opcode_names[SUB] = "SUB";
  opcode_names[DIV] = "DIV";
  opcode_names[MOD] = "MOD";
  opcode_names[AND] = "AND";
  opcode_names[OR] = "OR";
  opcode_names[LSH] = "LSH";
  opcode_names[RSH] = "RSH";
  opcode_names[BAND] = "BAND";
  opcode_names[BOR] = "BOR";
  opcode_names[EQ] = "EQ";
  opcode_names[GEQ] = "GEQ";
  opcode_names[LEQ] = "LEQ";
  opcode_names[GT] = "GT";
  opcode_names[LT] = "LT";
  opcode_names[NEQ] = "NEQ";
  opcode_names[XOR] = "XOR";
  opcode_names[ADDR] = "ADDR";
  opcode_names[OZJMP] = "OZJMP";
  opcode_names[ONZJMP] = "ONZJMP";
  opcode_names[OJMP] = "OJMP";
  opcode_names[LDCONST] = "LDCONST";
  opcode_names[PRINT] = "PRINT";
  return opcode_names;
}
#endif