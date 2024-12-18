import os
import subprocess
import pytest
import re


def check_test_file_exists():
    """Verify that the LLM created the test file"""
    test_file = "app/llm_test.c"  # Changed to use path from root directory
    assert os.path.exists(test_file), f"LLM must create a test file at {test_file}"
    return test_file


def count_test_functions(test_file: str) -> set:
    """Extract test function names from the C test file"""
    with open(test_file, "r") as f:
        content = f.read()

    # Look for test function declarations (test_*)
    test_funcs = set(re.findall(r"void\s+(test_\w+)\s*\(\s*void\s*\)", content))

    # Extract the actual function being tested from the test name
    return {func[5:] for func in test_funcs}  # Remove 'test_' prefix


def count_assertions(test_file: str) -> int:
    """Count the number of assertions in the test file"""
    with open(test_file, "r") as f:
        content = f.read()

    # Count assert statements - looking for assert(*) patterns
    assertions = re.findall(r"assert\s*\([^;]+\);", content)
    return len(assertions)


def get_required_functions():
    """Get the list of functions that should be tested"""
    return {"add", "subtract", "multiply", "is_even", "calculate_expression"}


def compile_and_run_tests():
    """Compile and run the C tests"""
    # Change to app directory
    os.chdir("app")

    # Run make clean and make
    try:
        subprocess.run(["make", "clean"], check=True, capture_output=True)
        subprocess.run(["make"], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile tests: {e.stderr.decode()}")

    # Run the test executable
    try:
        result = subprocess.run(["./test_runner"], check=True, capture_output=True)
        success = result.returncode == 0
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Tests failed with output: {e.stderr.decode()}")
        success = False
    finally:
        # Change back to original directory
        os.chdir("..")
        return success


def test_llm_test_implementation():
    """Main test to verify LLM's test file"""
    # 1. Check if test file exists
    test_file = check_test_file_exists()

    # 2. Get functions that should be tested
    required_functions = get_required_functions()

    # 3. Get functions that are actually tested
    tested_functions = count_test_functions(test_file)

    # 4. Check if all functions are tested
    missing_tests = required_functions - tested_functions
    assert not missing_tests, f"Missing tests for functions: {missing_tests}"

    # 5. Check for minimum assertion count (at least one per function)
    min_required_assertions = len(required_functions)
    actual_assertions = count_assertions(test_file)

    assert (
        actual_assertions >= min_required_assertions
    ), f"Expected at least {min_required_assertions} assertions, but found {actual_assertions}"

    # 6. Compile and run the tests
    assert compile_and_run_tests(), "C tests failed to execute successfully"


if __name__ == "__main__":
    pytest.main([__file__])
