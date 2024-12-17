# TASK
You need to implement a CLI tool called `cmd-logger` that can:
1. Start logging every command executed in the terminal to a continuously growing `.txt` file.
2. Stop logging commands.
3. Show whether logging is active or not.
4. Provide a helpful `--help` output.
  
This includes:
- A `start` command that begins logging new commands to a persistent log file (e.g. `~/.cmd_logger_history.txt`).
- A `stop` command that halts further logging.
- A `status` command that shows if logging is currently active.
- A `--help` command (or `-h`) that prints usage information.

The solution should handle unexpected commands gracefully and should be straightforward for both developers and non-technical team members to run. Tests will be provided to verify that all functionalities work as expected.

# REQUIREMENTS
1. **CLI Structure:**
   - The CLI must have `start`, `stop`, `status`, and `--help` (or `-h`) commands.
   - Running `start` should create or open the log file and enable logging.
   - Running `stop` should disable logging.
   - Running `status` should print whether logging is active.
   - Running `--help` or `-h` should print usage information.
   
2. **Logging Behavior:**
   - When `start` is active, any executed terminal command (like `ls`, `pwd`, `echo "Hello"`) should be appended to the log file, one command per line.
   - Stopping logging should prevent any further commands from being recorded.
   - The log file (`~/.cmd_logger_history.txt`) should not be overwritten when restarting logging. It should continue appending commands at the end.
   
3. **Error Handling:**
   - Invalid subcommands (e.g. `cmd-logger foo`) must print a helpful error message and exit with a non-zero status code.
   - If the log file cannot be written to, the tool should print a user-friendly error message.
   
4. **Help and Documentation:**
   - The `--help` option must clearly describe how to use `start`, `stop`, `status`.
   
5. **Tests & Verification:**
   - The provided test suite will run commands and verify:
     - Help output correctness.
     - Proper start/stop/status functionality.
     - Correct logging behavior (commands appear in the file as expected).
     - Error handling for unknown commands and permissions issues.
   
6. **Implementation Constraints:**
   - Must use Python's standard libraries (e.g., `argparse` for CLI parsing).
   - Code should be clean, well-structured, and documented.
   - Include a README or instructions in the code repository.

# IMPLEMENTATION
Carefully read the provided tests (test cases and pseudo-code examples). Implement the `cmd-logger` tool so that all these tests pass. You may create any necessary files, such as:

- `cmd_logger.py`: The main CLI implementation using `argparse`.
- A script for logging logic (if separate from CLI code).
- A `README.md` or similar document explaining installation and usage.
- The logging mechanism for capturing executed commands (you may need to consider shell integration or a simulation for the sake of testing, depending on the environment).

Ensure that after your implementation is complete, running the test suite as described (e.g., `pytest tests/test.py`) results in all tests passing successfully.
