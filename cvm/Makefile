BINARY=cvm
PYTHON=pypy
CC=clang
CFLAGS=-c -Wall
LDFLAGS=
SOURCES=$(wildcard *.c)
OBJECTS=$(SOURCES:.c=.o)

all: $(SOURCES) $(BINARY)
	
$(BINARY): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -o $@

opcodes: ../cvmc/binary.py
	$(PYTHON) ../cvmc/binary.py > opcodes.h

run: all
	./${BINARY}

clean:
	rm -f ${OBJECTS} ${BINARY} opcodes.h
