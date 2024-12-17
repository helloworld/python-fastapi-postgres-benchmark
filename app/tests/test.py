import os
import subprocess
import pytest
import time

# Log file location (expected)
LOG_FILE = os.path.expanduser("~/.cmd_logger_history.txt")

# CLI Command
CMD_LOGGER_CMD = "python cmd_logger.py"


@pytest.fixture
def clean_log_file():
    """
    Fixture to ensure the log file starts clean for each test.
    """
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    yield
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


def run_command(cmd):
    """
    Helper to run a shell command and return its output, error, and exit code.
    """
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    out, err = proc.communicate()
    return out.decode("utf-8").strip(), err.decode("utf-8").strip(), proc.returncode


def test_help_documentation(clean_log_file):
    """
    Test that --help works correctly.
    """
    out, err, code = run_command(f"{CMD_LOGGER_CMD} --help")
    assert code == 0
    assert "Usage:" in out
    assert "start" in out
    assert "stop" in out
    assert "status" in out


def test_start_creates_log_file(clean_log_file):
    """
    Test that 'start' creates the log file.
    """
    out, err, code = run_command(f"{CMD_LOGGER_CMD} start")
    assert code == 0
    assert "Logging started" in out
    assert os.path.exists(LOG_FILE)


def test_logging_commands(clean_log_file):
    """
    Test that 'start' logs commands to the file.
    """
    # Start logging
    run_command(f"{CMD_LOGGER_CMD} start")
    time.sleep(1)  # Allow tool to initialize

    # Run some sample shell commands
    run_command("echo Hello")
    run_command("ls")
    run_command("pwd")

    # Stop logging
    run_command(f"{CMD_LOGGER_CMD} stop")
    time.sleep(1)  # Allow clean stop

    # Verify the log file contents
    with open(LOG_FILE, "r") as f:
        content = f.read()

    assert "echo Hello" in content
    assert "ls" in content
    assert "pwd" in content


def test_stop_logging_commands(clean_log_file):
    """
    Test that after 'stop', no commands are logged.
    """
    # Start logging
    run_command(f"{CMD_LOGGER_CMD} start")
    time.sleep(1)

    # Run a command
    run_command("echo FirstCommand")

    # Stop logging
    run_command(f"{CMD_LOGGER_CMD} stop")
    time.sleep(1)

    # Run another command (should NOT be logged)
    run_command("echo ShouldNotLog")

    # Verify the log file
    with open(LOG_FILE, "r") as f:
        content = f.read()

    assert "FirstCommand" in content
    assert "ShouldNotLog" not in content


def test_status_after_start_and_stop(clean_log_file):
    """
    Test the 'status' command to show logging activity.
    """
    # Check status before starting
    out, _, _ = run_command(f"{CMD_LOGGER_CMD} status")
    assert "not active" in out.lower()

    # Start logging
    run_command(f"{CMD_LOGGER_CMD} start")
    time.sleep(1)

    # Check status
    out, _, _ = run_command(f"{CMD_LOGGER_CMD} status")
    assert "active" in out.lower()

    # Stop logging
    run_command(f"{CMD_LOGGER_CMD} stop")
    time.sleep(1)

    # Check status again
    out, _, _ = run_command(f"{CMD_LOGGER_CMD} status")
    assert "not active" in out.lower()


def test_invalid_command(clean_log_file):
    """
    Test that an invalid command shows an error message.
    """
    out, err, code = run_command(f"{CMD_LOGGER_CMD} invalid_command")
    assert code != 0
    assert "Unknown command" in err or "Error" in err


def test_append_mode(clean_log_file):
    """
    Test that the log file appends new commands, rather than overwriting.
    """
    # Start logging and run a command
    run_command(f"{CMD_LOGGER_CMD} start")
    time.sleep(1)
    run_command("echo FirstCommand")
    run_command(f"{CMD_LOGGER_CMD} stop")
    time.sleep(1)

    # Restart logging and run another command
    run_command(f"{CMD_LOGGER_CMD} start")
    time.sleep(1)
    run_command("echo SecondCommand")
    run_command(f"{CMD_LOGGER_CMD} stop")

    # Verify both commands are in the file
    with open(LOG_FILE, "r") as f:
        content = f.read()

    assert "FirstCommand" in content
    assert "SecondCommand" in content
