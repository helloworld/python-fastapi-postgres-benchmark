# LLM C Unit Test Writing Challenge

Your task is to write a comprehensive C unit test suite for a snake game implementation. This is a test of your ability to:
1. Read and understand existing C code
2. Write thorough unit tests for multiple functions
3. Handle memory management correctly in C
4. Test both happy paths and error cases
5. Create tests that pass compilation and execution

## Instructions

1. First, read and analyze the code in:
   - `app/snake/state.h` - Contains function declarations and data structures
   - `app/snake/state.c` - Contains the implementation

2. Next, read the tests defined at app/tests/test.py to learn about the success conditions of your task: running `python -m pytest app/tests/test.py -v` should pass in the end.

3. Create a new file at `app/unit_tests.c` that contains a complete test suite. Your test file should:
   - Include necessary headers (`state.h`, `assert.h`)
   - Have a `main()` function that runs all tests
   - Use the standard C `assert()` macro for validations
   - Properly free any allocated memory
   - Include memory leak checks
   - Test error handling cases

4. Required test functions:
   - State Management:
     - `void test_create_default_state(void)`
     - `void test_free_state(void)`
     - `void test_initialize_snakes(void)`
   - Board Operations:
     - `void test_print_board(void)`
     - `void test_save_board(void)`
     - `void test_load_board(void)`
     - `void test_get_board_at(void)`
   - Snake Movement:
     - `void test_update_state(void)`
   - Helper Functions:
     - `void test_is_tail(void)`
     - `void test_is_head(void)`
     - `void test_is_snake(void)`

5. Testing Requirements:
   - Each test function must be properly named (test_function_name)
   - Include at least 2 assertions per function on average
   - Test both valid and invalid inputs
   - Include NULL pointer checks where appropriate
   - Verify memory management (allocation and cleanup)
   - Test edge cases and error conditions

6. Memory Management:
   - All allocated memory must be properly freed
   - Tests should check for memory leaks
   - Include error handling for failed memory allocations

## Success Criteria

Your submission will be considered successful if:
1. All required test functions are implemented
2. Tests contain sufficient assertions (minimum 2 per function average)
3. Memory management is properly tested
4. Error handling is verified
5. The code compiles successfully
6. All tests pass when run
7. No memory leaks are detected

## Running Tests

Your tests will be compiled and run using:
```bash
python -m pytest app/tests/test.py -v
```

This will:
1. Verify the presence of all required test functions
2. Check assertion coverage
3. Verify memory leak testing
4. Check error handling
5. Compile and run the tests
6. Run memory leak detection (when valgrind is available)
