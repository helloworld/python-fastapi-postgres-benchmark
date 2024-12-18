# LLM Unit Test Writing Challenge

Your task is to write unit tests for a C file containing mathematical functions. This is a test of your ability to:
1. Read and understand existing code
2. Write comprehensive unit tests
3. Ensure proper test coverage
4. Create tests that pass validation

## Instructions

1. First, read and analyze the C code in `app/math.c`. This file contains several mathematical functions that need to be tested.

2. Create a new file at `app/tests/llm_generated_test.py` that contains unit tests for ALL functions in the C file.

3. Requirements for your tests:
   - Write at least one test function for each function in math.c
   - Name your test functions as `test_<function_name>` (e.g., `test_add` for the `add` function)
   - Include meaningful assertions that verify the correct behavior of each function
   - Test both normal cases and edge cases where appropriate
   - Ensure your tests can be run using pytest

4. Your tests will be validated by running:
```bash
pytest app/tests/test.py
```

This will check that:
- All functions have corresponding test functions
- Each function has at least one assertion
- The tests are syntactically correct and can be executed
- The test file exists in the correct location

## Success Criteria

Your submission will be considered successful if:
1. All functions from math.c have corresponding test functions
2. Each test function contains at least one meaningful assertion
3. Running `pytest app/tests/test.py` passes without any failures

Remember to test both the basic functionality and any edge cases for each function.