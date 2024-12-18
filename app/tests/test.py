import pytest
import os
import subprocess
import numpy as np
from pathlib import Path

# Define paths for the repository and the cleaned repository
ORIGINAL_REPO_PATH = "./app/original_repo"
CLEANED_REPO_PATH = "./app/cleaned_repo"


def test_basic_code_functionality_original():
    """Verify the original code produces expected results before any changes."""
    from app.original_repo.main import runner

    expected_results = {
        "add": 8,  # 5 + 3
        "multiply": 15,  # 5 * 3
        "subtract": 2,  # 5 - 3
        "power": 125,  # 5^3
    }
    results = runner()

    # Check only the basic operations (backward compatibility)
    for key in expected_results:
        assert (
            results[key] == expected_results[key]
        ), f"Original code produced unexpected results for {key}: {results[key]}"


def test_basic_code_functionality_cleaned():
    """Verify the original code produces expected results before any changes."""
    from app.cleaned_repo.main import runner

    expected_results = {
        "add": 8,  # 5 + 3
        "multiply": 15,  # 5 * 3
        "subtract": 2,  # 5 - 3
        "power": 125,  # 5^3
    }
    results = runner()

    # Check only the basic operations (backward compatibility)
    for key in expected_results:
        assert (
            results[key] == expected_results[key]
        ), f"Original code produced unexpected results for {key}: {results[key]}"


def test_advanced_operations_original():
    """Test the new advanced operations and statistical features."""
    from app.original_repo.main import runner
    from app.original_repo.main import CalculationConfig

    config = CalculationConfig(precision=3, base_numbers=[2.0, 3.0, 4.0, 5.0, 6.0])

    results = runner(config)

    # Verify advanced metrics exist
    assert "statistics" in results, "Advanced statistics not present in results"
    assert "fibonacci_power_sum" in results, "Fibonacci power sum not present"
    assert "percentage_changes" in results, "Percentage changes not present"

    # Verify statistics calculations
    stats = results["statistics"]
    assert abs(stats["mean"] - 4.0) < 1e-6, "Incorrect mean calculation"
    assert abs(stats["geometric_mean"] - 3.728) < 1e-3, "Incorrect geometric mean"

    # Verify percentage changes
    changes = results["percentage_changes"]
    assert len(changes) == 4, "Incorrect number of percentage changes"
    assert abs(changes[0] - 50.0) < 1e-6, "Incorrect percentage change calculation"


def test_advanced_operations_cleaned():
    """Test the new advanced operations and statistical features."""
    from app.cleaned_repo.main import runner
    from app.cleaned_repo.main import CalculationConfig

    config = CalculationConfig(precision=3, base_numbers=[2.0, 3.0, 4.0, 5.0, 6.0])

    results = runner(config)

    # Verify advanced metrics exist
    assert "statistics" in results, "Advanced statistics not present in results"
    assert "fibonacci_power_sum" in results, "Fibonacci power sum not present"
    assert "percentage_changes" in results, "Percentage changes not present"

    # Verify statistics calculations
    stats = results["statistics"]
    assert abs(stats["mean"] - 4.0) < 1e-6, "Incorrect mean calculation"
    assert abs(stats["geometric_mean"] - 3.728) < 1e-3, "Incorrect geometric mean"

    # Verify percentage changes
    changes = results["percentage_changes"]
    assert len(changes) == 4, "Incorrect number of percentage changes"
    assert abs(changes[0] - 50.0) < 1e-6, "Incorrect percentage change calculation"


def test_error_handling_original():
    """Test error handling and input validation."""
    from app.original_repo.helper1 import BasicOperations, compute_percentage
    from app.original_repo.helper2 import AdvancedOperations

    basic_ops = BasicOperations()
    advanced_ops = AdvancedOperations()

    # Test input validation
    with pytest.raises(TypeError):
        basic_ops.add("not a number", 5)

    with pytest.raises(ValueError):
        advanced_ops.divide(10, 0)

    # Test decorator validation
    with pytest.raises(ValueError):
        compute_percentage(-1, 100)


def test_error_handling_cleaned():
    """Test error handling and input validation."""
    from app.cleaned_repo.helper1 import BasicOperations, compute_percentage
    from app.cleaned_repo.helper2 import AdvancedOperations

    basic_ops = BasicOperations()
    advanced_ops = AdvancedOperations()

    # Test input validation
    with pytest.raises(TypeError):
        basic_ops.add("not a number", 5)

    with pytest.raises(ValueError):
        advanced_ops.divide(10, 0)

    # Test decorator validation
    with pytest.raises(ValueError):
        compute_percentage(-1, 100)


def test_configuration_management_original():
    """Test that configuration options work correctly."""
    from app.original_repo.main import runner
    from app.original_repo.main import CalculationConfig

    # Test default configuration
    default_config = CalculationConfig()
    assert default_config.precision == 2
    assert default_config.cache_size == 128
    assert len(default_config.base_numbers) == default_config.sample_size

    # Test custom configuration
    custom_config = CalculationConfig(
        precision=4, cache_size=256, base_numbers=[1.0, 2.0, 3.0, 4.0, 5.0]
    )
    results = runner(custom_config)

    # Verify precision is respected
    assert isinstance(results["add"], float), "Precision not applied correctly"
    assert (
        str(results["add"]).count(".") == 0
        or len(str(results["add"]).split(".")[1]) <= 4
    )


def test_configuration_management_cleaned():
    """Test that configuration options work correctly."""
    from app.cleaned_repo.main import runner
    from app.cleaned_repo.main import CalculationConfig

    # Test default configuration
    default_config = CalculationConfig()
    assert default_config.precision == 2
    assert default_config.cache_size == 128
    assert len(default_config.base_numbers) == default_config.sample_size

    # Test custom configuration
    custom_config = CalculationConfig(
        precision=4, cache_size=256, base_numbers=[1.0, 2.0, 3.0, 4.0, 5.0]
    )
    results = runner(custom_config)

    # Verify precision is respected
    assert isinstance(results["add"], float), "Precision not applied correctly"
    assert (
        str(results["add"]).count(".") == 0
        or len(str(results["add"]).split(".")[1]) <= 4
    )


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
