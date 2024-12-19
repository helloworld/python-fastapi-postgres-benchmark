import os
import pytest
from pathlib import Path

REQUIRED_CLASSES = [
    "BDDReachabilityAnalysisFactory",
    "BDDReachabilityAnalysis",
    "BidirectionalReachabilityAnalysis",
    "ForwardingAnalysisImpl",
    "FibImpl",
    "IncrementalDataPlane",
]


def check_output_file_exists():
    """Verify that the output file exists"""
    output_file = "app/files_to_explore.txt"
    assert os.path.exists(output_file), f"Output file must exist at {output_file}"
    return output_file


def read_file_paths(output_file: str) -> list:
    """Read and validate the file paths from the output file"""
    with open(output_file, "r") as f:
        paths = [line.strip() for line in f.readlines() if line.strip()]

    # Check if file list is empty
    assert paths, "File list cannot be empty"

    # Validate path format
    invalid_paths = [
        p for p in paths if not p.startswith("./") and not p.startswith("/")
    ]
    assert not invalid_paths, (
        f"The following paths are not properly formatted (should start with ./ or /):\n"
        + "\n".join(f"  {p}" for p in invalid_paths)
    )

    return paths


def check_required_classes(paths: list) -> dict:
    """Check if all required classes are present in the file paths"""
    found_classes = {cls: False for cls in REQUIRED_CLASSES}

    for file_path in paths:
        filename = Path(file_path).name
        for required_class in REQUIRED_CLASSES:
            if required_class in filename:
                found_classes[required_class] = True

    return found_classes


def test_output_file_contents():
    """Main test to verify the output file contents"""
    # 1. Check if output file exists
    output_file = check_output_file_exists()

    # 2. Read and validate file paths
    paths = read_file_paths(output_file)

    # 3. Check for required classes
    found_classes = check_required_classes(paths)

    # 4. Assert all required classes are found
    missing_classes = [cls for cls, found in found_classes.items() if not found]
    assert (
        not missing_classes
    ), f"The following required classes are missing from the file list:\n" + "\n".join(
        f"  {cls}" for cls in missing_classes
    )


def test_paths_exist():
    """Test that all listed paths actually exist in the repository"""
    output_file = check_output_file_exists()
    paths = read_file_paths(output_file)

    # Remove leading ./ if present for path checking
    normalized_paths = [p[2:] if p.startswith("./") else p for p in paths]

    # Check if each path exists
    missing_paths = [p for p in normalized_paths if not os.path.exists(p)]
    assert (
        not missing_paths
    ), f"The following paths do not exist in the repository:\n" + "\n".join(
        f"  {p}" for p in missing_paths
    )


def test_java_files_only():
    """Test that all listed files are Java files"""
    output_file = check_output_file_exists()
    paths = read_file_paths(output_file)

    non_java_files = [p for p in paths if not p.endswith(".java")]
    assert not non_java_files, f"The following files are not Java files:\n" + "\n".join(
        f"  {p}" for p in non_java_files
    )


if __name__ == "__main__":
    pytest.main([__file__])
