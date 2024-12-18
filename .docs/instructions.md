# Task: Code Cleanup - Removing Redundant or Unused Code

## Objective
Your task is to review the code in this repository and perform a cleanup to remove redundant or unused code. The repository consists of the following files:

1. `helper1.py`: Contains utility functions, some of which are unused or redundant.
2. `helper2.py`: Contains additional utilities, with potential overlap with `helper1.py`.
3. `helper3.py`: Contains more utilities, some of which may not be used in the project.
4. `main.py`: The main application logic that uses functions from the `helper` files.

## Instructions
1. **Analyze the Repository**:
   - Carefully examine the code app/original_repo/.
   - Identify functions or code blocks that are not used anywhere in the repository.
   - Identify redundancy where similar or identical functionality is implemented multiple times.

2. **Clean Up**:
   - Make a copy of app/original_repo in app/cleaned_repo
   - Remove any code that is unused across the repository.
   - Consolidate redundant functionality to a single implementation and update references accordingly.
   - Ensure that all necessary imports and functions used in `main.py` are preserved and functional.

3. **Validate Functionality**:
   - After the cleanup, ensure the `main.py` script runs without errors.
   - The core functionality of the repository should remain unchanged.

4. MANDATORY: there is a test suite located in app/tests/test.py. make sure to read it and make sure that it passes to verify that you have finished the objective correctly.

## Output
Submit the cleaned-up repository. The cleaned code should:
- Contain no unused or redundant functions.
- Preserve all functionality used in `main.py`.
- Be well-organized and easy to read.
- MANDATORY: there is a test suite located in app/tests/test.py. make sure to read it and make sure that it passes.

## Notes
- Focus on readability and maintainability of the code.
- Avoid introducing new functionality or altering the logic in `main.py` beyond updating references to cleaned-up functions.
