import pytest
import os
import subprocess
from pathlib import Path

# Define paths for the repository and the cleaned repository
ORIGINAL_REPO_PATH = "./app/original_repo"
CLEANED_REPO_PATH = "./app/cleaned_repo"


def test_original_code_functionality():
    """Verify the original code produces expected results before any changes."""
    from app.original_repo.main import runner

    expected_results = {
        "add": 8,  # 5 + 3
        "multiply": 15,  # 5 * 3
        "subtract": -3,  # 2 - 5
        "power": 125,  # 5^3
    }
    results = runner()
    assert (
        results == expected_results
    ), f"Original code produced unexpected results: {results}"


def test_cleaned_code_functionality():
    """Verify the cleaned/refactored code produces identical results."""
    from app.cleaned_repo.main import runner

    expected_results = {
        "add": 8,  # 5 + 3
        "multiply": 15,  # 5 * 3
        "subtract": -3,  # 2 - 5
        "power": 125,  # 5^3
    }
    results = runner()
    assert (
        results == expected_results
    ), f"Cleaned code produced different results: {results}"


def test_no_redundant_functions():
    """Verify that the cleaned code has removed all redundant/unused functions."""
    # Get all functions used in main.py
    used_functions = set()
    main_path = Path(CLEANED_REPO_PATH) / "main.py"
    with open(main_path, "r") as f:
        main_content = f.read()
        # Extract imported function names
        for line in main_content.split("\n"):
            if "import" in line:
                functions = line.split("import")[1].strip().split(",")
                used_functions.update(f.strip() for f in functions)

    # Check each helper file for unused functions
    helper_files = ["helper1.py", "helper2.py", "helper3.py"]
    for helper_file in helper_files:
        file_path = Path(CLEANED_REPO_PATH) / helper_file
        with open(file_path, "r") as f:
            content = f.read()
            # Find all function definitions
            for line in content.split("\n"):
                if line.strip().startswith("def "):
                    func_name = line.split("def ")[1].split("(")[0].strip()
                    assert (
                        func_name in used_functions
                    ), f"Found unused function '{func_name}' in {helper_file}"


def test_module_structure():
    """Verify the cleaned code maintains proper module structure."""
    required_files = [
        "__init__.py",
        "main.py",
        "helper1.py",
        "helper2.py",
        "helper3.py",
    ]

    for file in required_files:
        path = Path(CLEANED_REPO_PATH) / file
        assert path.exists(), f"Required file {file} is missing from cleaned code"
        assert path.stat().st_size > 0, f"Required file {file} is empty"


def test_direct_execution():
    """Verify both original and cleaned code can be executed directly."""
    # Test original code execution
    orig_result = subprocess.run(
        ["python", "-m", "app.original_repo.main"],
        capture_output=True,
        text=True,
    )
    assert (
        orig_result.returncode == 0
    ), f"Original main.py failed to execute: {orig_result.stderr}"

    # Test cleaned code execution
    clean_result = subprocess.run(
        ["python", "-m", "app.cleaned_repo.main"],
        capture_output=True,
        text=True,
    )
    assert (
        clean_result.returncode == 0
    ), f"Cleaned main.py failed to execute: {clean_result.stderr}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
