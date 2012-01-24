#include <stdio.h>
#include <stdlib.h>
#include "opcodes.h"

//#define DEBUG
#define MEMORY_SIZE 128
#define STACK_DEPTH 128

#define RS_PUSH(x) reg_stack_push(machine->reg_stack, (x))
#define RS_POP reg_stack_pop(machine->reg_stack)

typedef unsigned int uint;
typedef unsigned char instr_op;
typedef signed char instr_arg;
typedef unsigned char memory_cell;

struct register_stack_struct {
  memory_cell* stack;
  uint size;
  uint capacity;
} typedef register_stack;

struct machine_state_struct {
  register_stack *reg_stack;
  register_stack *return_addresses;

  memory_cell *memory;
  uint memory_size;

  unsigned char* code;
  uint code_len;
  uint program_counter;

  uint error;
} typedef machine_state;

memory_cell *mem_create(uint size) {
  return malloc(size * sizeof(char));
}

register_stack *reg_stack_create(uint initial_capacity) {
  register_stack *stack = malloc(sizeof(register_stack));
  stack->stack = malloc(sizeof(memory_cell) * initial_capacity);
  stack->capacity = initial_capacity;
  stack->size = 0;
  return stack;
}

void reg_stack_push(register_stack *stack, memory_cell value) {
  if (stack->size < stack->capacity) {
    stack->stack[stack->size] = value;
    stack->size++;
  } else {
    fprintf(stderr, "Register stack overflow.");
    exit(1);
  }
}

memory_cell reg_stack_pop(register_stack *stack) {
  if (stack->size > 0) {
    stack->size--;
    return stack->stack[stack->size];
  } else {
    fprintf(stderr, "Register stack underflow.");
    exit(1);
  }
}

void reg_stack_free(register_stack *stack) {
  free(stack->stack);
  free(stack);
}

machine_state *machine_create() {
  machine_state *machine = malloc(sizeof(machine_state));
  machine->memory = mem_create(MEMORY_SIZE);
  machine->memory_size = MEMORY_SIZE;
  machine->reg_stack = reg_stack_create(32);
  machine->return_addresses = reg_stack_create(STACK_DEPTH);
  machine->code = NULL;
  machine->code_len = 0;
  machine->program_counter = 0;
  return machine;
}

void mem_print(machine_state *machine) {
  int i = 0;
  for (; i < machine->memory_size; i++) {
    printf("%02X ", machine->memory[i]);
    if ((i + 1) % 32 == 0) {
      printf("\n");
    }
  }
}

void reg_stack_print(machine_state *machine) {
  int i = 0;
  for (; i < machine->reg_stack->size; i++) {
    printf("%d ", machine->reg_stack->stack[i]);
  }
  printf("\n");
}

void machine_free(machine_state *machine) {
  free(machine->memory);
  free(machine->code);
  reg_stack_free(machine->reg_stack);
  free(machine);
}

void machine_load_program(machine_state *machine, FILE *data) {
  machine->code_len = 0;
  machine->program_counter = 0;
  fseek(data, 0, SEEK_END);
  machine->code_len = ftell(data);
  fseek(data, 0, SEEK_SET);

  machine->code = malloc(machine->code_len);
  if (machine->code_len !=
      fread(machine->code, sizeof(char), machine->code_len, data)) {
    machine_free(machine);
    fprintf(stderr, "Could not read input file.");
  }
}

void machine_run_instruction(
    machine_state *machine, instr_op opcode, instr_arg argument) {
  memory_cell operand1, operand2;

  switch (opcode) {
    case NOP:
      break;
    case HALT:
      machine->error = 1;
      break;

    case PUSH:
      operand1 = RS_POP;
      RS_PUSH(operand1);
      RS_PUSH(operand1);
      break;
    case POP:
      RS_POP;
      break;

    case CALL:
      reg_stack_push(machine->return_addresses, machine->program_counter + 1);
      machine->program_counter = argument;
      goto skip_pc_incr;

    case RETURN:
      machine->program_counter = reg_stack_pop(machine->return_addresses);
      goto skip_pc_incr;

    case STORE:
      machine->memory[(uint) argument] = RS_POP;
      break;
    case LOAD:
      RS_PUSH(machine->memory[(uint) argument]);
      break;

    case INCR:
      RS_PUSH(RS_POP + 1);
      break;
    case DECR:
      RS_PUSH(RS_POP - 1);
      break;

    case NOT:
      RS_PUSH(!RS_POP);
      break;
    case BNOT:
      RS_PUSH(~RS_POP);
      break;

    case MUL:
      RS_PUSH(RS_POP * RS_POP);
      break;
    case ADD:
      RS_PUSH(RS_POP + RS_POP);
      break;
    case SUB:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 - operand2);
      break;
    case DIV:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 / operand2);
      break;
    case MOD:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 % operand2);
      break;

    case AND:
      RS_PUSH(RS_POP & RS_POP);
      break;
    case OR:
      RS_PUSH(RS_POP | RS_POP);
      break;
    case XOR:
      RS_PUSH(RS_POP ^ RS_POP);
      break;

    case LSH:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 << operand2);
      break;
    case RSH:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 >> operand2);
      break;

    case BAND:
      RS_PUSH(RS_POP && RS_POP);
      break;
    case BOR:
      RS_PUSH(RS_POP || RS_POP);
      break;

    case EQ:
      RS_PUSH(RS_POP == RS_POP);
      break;
    case GEQ:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 >= operand2);
      break;
    case LEQ:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 <= operand2);
      break;
    case GT:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 > operand2);
      break;
    case LT:
      operand2 = RS_POP;
      operand1 = RS_POP;
      RS_PUSH(operand1 < operand2);
      break;
    case NEQ:
      RS_PUSH(RS_POP != RS_POP);
      break;

    case OZJMP:
      if (RS_POP == 0) {
        machine->program_counter += (signed char) argument;
        goto skip_pc_incr;
      }
      break;
    case ONZJMP:
      if (RS_POP != 0) {
        machine->program_counter += (signed char) argument;
        goto skip_pc_incr;
      }
      break;
    case OJMP:
      machine->program_counter += (signed char) argument;
      goto skip_pc_incr;

    case LDCONST:
      RS_PUSH(argument);
      break;

    case PRINT:
      printf("%c", (unsigned char) RS_POP);
      break;
  }

  machine->program_counter++;

skip_pc_incr:

#ifdef DEBUG
  printf("PC: %d, REG: ", machine->program_counter);
  reg_stack_print(machine);
#endif

  return;
}

void machine_run(machine_state *machine) {
  char **opcode_names = opcode_map();
  instr_op opcode;
  instr_arg argument;

  while (!machine->error) {
    opcode = machine->code[2 * machine->program_counter];
    argument = machine->code[2 * machine->program_counter + 1];
#ifdef DEBUG
    printf("%s 0x%02X (%d)\n",
        opcode_names[(uint) opcode], argument, argument);
#endif
    machine_run_instruction(machine, opcode, argument);
  }

#ifdef DEBUG
  mem_print(machine);
#endif

  free(opcode_names);
}

void machine_print_code(machine_state *machine) {
  char **opcode_names = opcode_map();
  int i = 0;

  for (; i < machine->code_len; i += 2) {
    instr_op opcode = machine->code[i];
    instr_arg argument = machine->code[i + 1];
    printf("%s 0x%02X (%d)\n",
        opcode_names[(uint) opcode], argument, argument);
  }
}

int main(int argc, char** argv) {
  machine_state *machine = machine_create();

  FILE *input_file = fopen(argv[1], "rb");
  machine_load_program(machine, input_file);
  fclose(input_file);

  machine_run(machine);
  machine_free(machine);
  return 0;
}
