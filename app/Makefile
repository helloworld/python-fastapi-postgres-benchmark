CC=gcc
CFLAGS=-Wall -Wextra -I.

all: libmath.a test_runner

libmath.a: math.o
	ar rcs libmath.a math.o

math.o: math.c math.h
	$(CC) $(CFLAGS) -c math.c

test_runner: llm_test.o libmath.a
	$(CC) $(CFLAGS) -o test_runner llm_test.o -L. -lmath

llm_test.o: llm_test.c math.h
	$(CC) $(CFLAGS) -c llm_test.c

clean:
	rm -f *.o *.a test_runner