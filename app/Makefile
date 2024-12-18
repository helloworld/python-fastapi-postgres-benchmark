CC=gcc
CFLAGS=-Wall -Wno-unused-function -Wconversion -std=c99 -g -I.

# Object files
OBJS=snake/state.o snake/snake_utils.o llm_test.o

# Main target
test_runner: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

# Individual object files
snake/state.o: snake/state.c snake/state.h snake/snake_utils.h
	$(CC) $(CFLAGS) -c -o $@ $<

snake/snake_utils.o: snake/snake_utils.c snake/snake_utils.h
	$(CC) $(CFLAGS) -c -o $@ $<

llm_test.o: llm_test.c snake/state.h
	$(CC) $(CFLAGS) -c -o $@ $<

.PHONY: clean test
clean:
	rm -f test_runner *.o snake/*.o

test: test_runner
	./test_runner
