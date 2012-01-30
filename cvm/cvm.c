#include <stdio.h>
#include <stdlib.h>
#include "opcodes.h"

//#define DEBUG
#define MEMORY_SIZE 128
#define STACK_DEPTH 128
#define NIL 0

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

struct memory_page_struct {
  memory_cell *memory;
  unsigned char *used;
  uint size;
} typedef memory_page;

struct stack_frame_struct {
  register_stack *return_addresses;
  register_stack *stack_frame_addr;
  register_stack *stack_frame_len;
} typedef stack_frames;

struct machine_state_struct {
  register_stack *reg_stack;
  stack_frames *stack;

  memory_page *memory;

  unsigned char* code;
  uint code_len;
  uint program_counter;

  uint error;
} typedef machine_state;

memory_page *memory_page_create(uint size) {
  memory_page *mem = malloc(sizeof(memory_page));
  mem->memory = malloc(size * sizeof(memory_cell));
  mem->used = malloc(size / 8);
  mem->size = size;
  return mem;
}

void memory_cell_set_used(memory_page *mem, uint addr) {
  mem->used[addr / 8] |= 1 << (addr % 8);
}

unsigned char memory_cell_is_used(memory_page *mem, uint addr) {
  return mem->used[addr / 8] & (1 << (addr % 8));
}

void memory_cell_write(memory_page *mem, uint addr, memory_cell value) {
  if (addr >= mem->size || addr == NIL) {
    printf("Illegal write to address %d (memory size %d)\n", addr, mem->size);
    exit(1);
  }

  memory_cell_set_used(mem, addr);
  mem->memory[addr] = value;
}

memory_cell memory_cell_read(memory_page *mem, uint addr) {
  if (addr >= mem->size || addr == NIL) {
    printf("Illegal read to address %d (memory size %d)\n", addr, mem->size);
    exit(1);
  }

  if (memory_cell_is_used(mem, addr) == 0) {
    printf("Warning: accessing memory that has not been initialized.");
  }

  return mem->memory[addr];
}

void memory_cell_free(memory_page *mem, uint addr) {
  if ((mem->used[addr / 8] & (1 << (addr % 8))) == 0) {
    printf("Warning: attempted to free memory that is not in use.");
    return;
  }

  mem->used[addr / 8] ^= 1 << (addr % 8);
}

void memory_cell_free_range(memory_page *mem, uint addr, uint len) {
  int i = 0;
  for (; i < len; i++) {
    memory_cell_free(mem, addr + i);
  }
}

void memory_page_free(memory_page *mem) {
  free(mem->memory);
  free(mem->used);
  free(mem);
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

memory_cell reg_stack_peek(register_stack *stack) {
  if (stack->size > 0) {
    return stack->stack[stack->size - 1];
  } else {
    fprintf(stderr, "Register stack underflow.");
    exit(1);
  }
}

void reg_stack_free(register_stack *stack) {
  free(stack->stack);
  free(stack);
}

stack_frames *stack_frames_create(uint stack_depth) {
  stack_frames *sfs = malloc(sizeof(stack_frames));
  sfs->return_addresses = reg_stack_create(stack_depth);
  sfs->stack_frame_addr = reg_stack_create(stack_depth);
  sfs->stack_frame_len = reg_stack_create(stack_depth);
  return sfs;
}

machine_state *machine_create() {
  machine_state *machine = malloc(sizeof(machine_state));
  machine->memory = memory_page_create(MEMORY_SIZE);
  machine->reg_stack = reg_stack_create(32);
  machine->stack = stack_frames_create(STACK_DEPTH);
  machine->code = NULL;
  machine->code_len = 0;
  machine->program_counter = 0;
  return machine;
}

void mem_print(machine_state *machine) {
  int i = 0;
  for (; i < machine->memory->size; i++) {
    printf("%02X ", machine->memory->memory[i]);
    if ((i + 1) % 32 == 0) {
      printf("\n");
    }
  }
}

void reg_stack_print(register_stack *reg_stack) {
  int i = 0;
  for (; i < reg_stack->size; i++) {
    printf("%d ", reg_stack->stack[i]);
  }
  printf("\n");
}

void machine_free(machine_state *machine) {
  free(machine->code);
  memory_page_free(machine->memory);
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

uint find_free_memory_of_size(uint size, memory_page *mem) {
  if (size == 0) {
    return NIL;
  } 

  int start_addr = NIL + 1;
  int offset;

  while (start_addr + size < mem->size) {
    if (!mem->used[start_addr]) {
      offset = 0;
      while (!memory_cell_is_used(mem, start_addr + offset) && offset < size) {
        offset++;
      }

      if (offset == size) {
        for (offset = 0; offset < size; offset++) {
          memory_cell_set_used(mem, start_addr + offset);
        }
        return start_addr;
      }
    }

    start_addr++;
  }

  printf("Out of memory: could not find a memory block of size %d\n", size);
  return NIL;
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
      reg_stack_push(
          machine->stack->return_addresses, machine->program_counter + 1);
      // operand1 is the length of the stack frame to be allocated.
      operand1 = RS_POP;
      reg_stack_push(machine->stack->stack_frame_len, operand1);
      reg_stack_push(
          machine->stack->stack_frame_addr,
          find_free_memory_of_size(operand1, machine->memory));
      machine->program_counter = argument;
      goto skip_pc_incr;

    case RETURN:
      machine->program_counter =
        reg_stack_pop(machine->stack->return_addresses);
      // operand1 is the start address of the stack frame
      operand1 = reg_stack_pop(machine->stack->stack_frame_addr);
      // operand2 is the length of the stack frame to free
      operand2 = reg_stack_pop(machine->stack->stack_frame_len);
      memory_cell_free_range(machine->memory, operand1, operand2);
      goto skip_pc_incr;

    case ALLOC:
      if (argument == -1) {
        argument = RS_POP;
      }
      RS_PUSH(find_free_memory_of_size(argument, machine->memory));
      break;

    case LSTORE:
      if (argument == -1) {
        operand1 = RS_POP + reg_stack_peek(machine->stack->stack_frame_addr);
      } else {
        operand1 = argument + reg_stack_peek(machine->stack->stack_frame_addr);
      }
      memory_cell_write(machine->memory, operand1, RS_POP);
      break;

    case LLOAD:
      if (argument == -1) {
        operand1 = RS_POP + reg_stack_peek(machine->stack->stack_frame_addr);
      } else {
        operand1 = argument + reg_stack_peek(machine->stack->stack_frame_addr);
      }
      RS_PUSH(memory_cell_read(machine->memory, operand1));
      break;

    case STORE:
      if (argument == -1) {
        operand1 = RS_POP;
        memory_cell_write(machine->memory, operand1, RS_POP);
      } else {
        memory_cell_write(machine->memory, argument, RS_POP);
      }
      break;

    case LOAD:
      if (argument == -1) {
        RS_PUSH(memory_cell_read(machine->memory, RS_POP));
      } else {
        RS_PUSH(memory_cell_read(machine->memory, argument));
      }
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

    default:
      printf("Unknown opcode: 0x%02X / %d\n", opcode, opcode);
  }

  machine->program_counter++;

skip_pc_incr:

#ifdef DEBUG
  printf("PC: %d\nREG: ", machine->program_counter);
  reg_stack_print(machine->reg_stack);
  printf("ADDR: ");
  reg_stack_print(machine->stack->stack_frame_addr);
  printf("\n");
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
