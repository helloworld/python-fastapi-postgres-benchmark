# TASK
You need to implement a CLI tool called `cmd-logger` that can:
1. Start logging every command executed in the terminal to a continuously growing `.txt` file.
2. Stop logging commands.
3. Show whether logging is active or not.
4. Provide a helpful `--help` output.
5. Ensure that after your implementation is complete, all tests in app/tests/test.py are passing.
  
This includes:
- A `start cmd-log` command that begins logging new commands to a persistent log file (e.g. `~/.cmd_logger_history.txt`).
- A `stop cmd-log` command that halts further logging.
- A `status cmd-log` command that shows if logging is currently active.
- A `cmd-log --help` command (or `-h`) that prints usage information.

The solution should handle unexpected commands gracefully and should be straightforward for both developers and non-technical team members to run. Tests will be provided to verify that all functionalities work as expected.

# REQUIREMENTS
1. **CLI Structure:**
   - The CLI must have `start`, `stop`, `status`, and `--help` (or `-h`) commands.
   - Running `start cmd-log` should create or open the log file and enable logging.
   - Running `stop cmd-log` should disable logging.
   - Running `status cmd-log` should print whether logging is active.
   - Running `cmd-log --help` or `-h` should print usage information.
   
2. **Logging Behavior:**
   - When `start cmd-log` is active, any executed terminal command (like `ls`, `pwd`, `echo "Hello"`) should be appended to the log file, one command per line.
   - Stopping logging should prevent any further commands from being recorded.
   - The log file (`~/.cmd_logger_history.txt`) should not be overwritten when restarting logging. It should continue appending commands at the end.
   
3. **Error Handling:**
   - Invalid subcommands (e.g. `cmd-logger foo`) must print a helpful error message and exit with a non-zero status code.
   - If the log file cannot be written to, the tool should print a user-friendly error message.
   
4. **Help and Documentation:**
   - The `--help` option must clearly describe how to use `start`, `stop`, `status`.
   
5. **Implementation Constraints:**
   - Must use Python's standard libraries (e.g., `argparse` for CLI parsing).
   - Code should be clean, well-structured, and documented.
   - Include a README or instructions in the code repository.

# IMPLEMENTATION
CAREFULLY read the provided tests first to understand the precise bounds of this spec. Implement the `cmd-logger` tool so that all these tests pass.

Ensure that after your implementation is complete, all tests in app/tests/test.py are passing.
