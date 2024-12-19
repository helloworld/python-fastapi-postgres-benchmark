import os
import subprocess
import pytest
import re


def check_test_file_exists():
    """Verify that the LLM created the test file"""
    test_file = "app/unit_tests.c"  # Changed from llm_test.c to unit_tests.c
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


def check_memory_tests(test_file: str) -> bool:
    """Check if the test file includes memory leak checks"""
    with open(test_file, "r") as f:
        content = f.read()
    
    # Look for common memory testing patterns
    memory_patterns = [
        r"free\s*\([^;]+\);",  # Check for free() calls
        r"valgrind",  # Check for valgrind references in comments
        r"malloc\s*\([^;]+\);",  # Check for malloc() calls
        r"memory leak",  # Check for memory leak references in comments
    ]
    
    return all(re.search(pattern, content, re.IGNORECASE) for pattern in memory_patterns)


def check_error_handling(test_file: str) -> bool:
    """Check if the test file includes error handling tests"""
    with open(test_file, "r") as f:
        content = f.read()
    
    # Look for error handling patterns
    error_patterns = [
        r"NULL",  # Check for NULL tests
        r"assert\s*\([^;]+==\s*NULL[^;]+\);",  # Check for NULL assertions
        r"assert\s*\([^;]+!=\s*NULL[^;]+\);",  # Check for non-NULL assertions
    ]
    
    return any(re.search(pattern, content) for pattern in error_patterns)


def get_required_functions():
    """Get the list of functions that should be tested"""
    return {
        "create_default_state",
        "free_state",
        "print_board",
        "save_board",
        "load_board",
        "get_board_at",
        "update_state",
        "initialize_snakes",
        "is_tail",
        "is_head",
        "is_snake",
    }


def compile_and_run_tests():
    """Compile and run the C tests"""
    original_dir = os.getcwd()
    try:
        # Change to app directory
        os.chdir("app")

        # Run make clean and make
        subprocess.run(["make", "clean"], check=True, capture_output=True)
        subprocess.run(["make"], check=True, capture_output=True)

        # Run the test executable
        result = subprocess.run(["./test_runner"], check=True, capture_output=True)
        
        # Check for memory leaks if valgrind is available
        try:
            valgrind_result = subprocess.run(
                ["valgrind", "--leak-check=full", "./test_runner"],
                check=True,
                capture_output=True,
                text=True
            )
            assert "no leaks are possible" in valgrind_result.stderr.lower(), "Memory leaks detected"
        except FileNotFoundError:
            print("Warning: valgrind not available, skipping memory leak check")
        
        return result.returncode == 0

    except subprocess.CalledProcessError as e:
        pytest.fail(f"Test execution failed: {e.stderr.decode()}")
        return False
    finally:
        os.chdir(original_dir)


def test_llm_test_implementation():
    """Main test to verify LLM's test file"""
    # 1. Check if test file exists
    test_file = check_test_file_exists()

    # 2. Get functions that should be tested
    required_functions = get_required_functions()

    # 3. Get functions that are actually tested
    tested_functions = count_test_functions(test_file)

    # 4. Check if all required functions are tested
    missing_tests = required_functions - tested_functions
    assert not missing_tests, f"Missing tests for functions: {missing_tests}"

    # 5. Check for minimum assertion count (at least 2 assertions per function on average)
    min_assertions = len(required_functions) * 2
    actual_assertions = count_assertions(test_file)
    assert actual_assertions >= min_assertions, \
        f"Expected at least {min_assertions} assertions, but found {actual_assertions}"

    # 6. Check for memory leak tests
    assert check_memory_tests(test_file), \
        "Test file should include memory leak checks"

    # 7. Check for error handling
    assert check_error_handling(test_file), \
        "Test file should include error handling tests (NULL checks, invalid inputs)"

    # 8. Compile and run the tests
    assert compile_and_run_tests(), "C tests failed to execute successfully"


if __name__ == "__main__":
    pytest.main([__file__])
