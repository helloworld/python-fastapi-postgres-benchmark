# LLM C Unit Test Writing Challenge

Your task is to write C unit tests for a C file containing mathematical functions. This is a test of your ability to:
1. Read and understand existing code
2. Write comprehensive unit tests in C
3. Ensure proper test coverage
4. Create tests that pass compilation and execution

## Instructions

1. First, read and analyze the code in `app/math.h` and `app/math.c`. These files contain several mathematical functions that need to be tested.

2. Create a new file at `app/llm_test.c` that contains C unit tests for ALL functions in math.c. Your test file should:
   - Include necessary headers (`math.h`, `assert.h`)
   - Have a `main()` function that runs all tests
   - Use the standard C `assert()` macro for validations

3. Requirements for your tests:
   - Write a test function for each function in math.c
   - Name your test functions as `void test_<function_name>(void)` (e.g., `void test_add(void)` for the `add` function)
   - Include meaningful assertions that verify the correct behavior of each function
   - Test both normal cases and edge cases where appropriate
   - Call all test functions from main()

4. Example test structure:
```c
#include <assert.h>
#include "math.h"

void test_add(void) {
    assert(add(2, 3) == 5);
    assert(add(-1, 1) == 0);
}

int main(void) {
    test_add();
    // ... other test function calls ...
    return 0;
}
```

5. Your tests will be compiled and run using:
```bash
cd app
make
./test_runner
```

## Success Criteria

Your submission will be considered successful if:
1. All functions from math.c have corresponding test functions
2. Each test function contains at least one meaningful assertion
3. The code compiles successfully with `make`
4. All tests pass when running the test executable

Remember to test both the basic functionality and any edge cases for each function.