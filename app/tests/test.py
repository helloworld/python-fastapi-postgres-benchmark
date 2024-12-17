import os
import subprocess
import pytest

# Path to the log file (as per spec)
LOG_FILE = os.path.expanduser("~/.cmd_logger_history.txt")


@pytest.fixture
def cleanup_log_file():
    """Fixture to clean up the log file before and after tests."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    yield
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


@pytest.fixture
def stop_cmd_log():
    """Ensures logging is stopped before tests start."""
    subprocess.run(
        ["cmd-logger", "stop", "cmd-log"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


@pytest.fixture
def setup_env(cleanup_log_file, stop_cmd_log):
    """Combines cleanup and stopping logging for a clean slate."""
    pass


def run_cmd(args):
    """Utility to run a command and capture its output."""
    return subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )


def test_help_command(setup_env):
    """Test that the --help and -h commands print usage information."""
    result = run_cmd(["cmd-logger", "--help"])
    assert result.returncode == 0
    assert "start" in result.stdout
    assert "stop" in result.stdout
    assert "status" in result.stdout

    result = run_cmd(["cmd-logger", "-h"])
    assert result.returncode == 0
    assert "start" in result.stdout


def test_invalid_command(setup_env):
    """Test that invalid subcommands print an error and exit non-zero."""
    result = run_cmd(["cmd-logger", "foo"])
    assert result.returncode != 0
    assert "Invalid command" in result.stderr


def test_start_logging_creates_file(setup_env):
    """Test that starting logging creates the log file if it does not exist."""
    result = run_cmd(["cmd-logger", "start", "cmd-log"])
    assert result.returncode == 0
    assert "Logging started" in result.stdout
    assert os.path.exists(LOG_FILE)


def test_stop_logging(setup_env):
    """Test stopping logging gracefully."""
    run_cmd(["cmd-logger", "start", "cmd-log"])
    result = run_cmd(["cmd-logger", "stop", "cmd-log"])
    assert result.returncode == 0
    assert "Logging stopped" in result.stdout


def test_status_logging_active(setup_env):
    """Test that status shows logging is active after starting."""
    run_cmd(["cmd-logger", "start", "cmd-log"])
    result = run_cmd(["cmd-logger", "status", "cmd-log"])
    assert result.returncode == 0
    assert "Logging is active" in result.stdout


def test_status_logging_inactive(setup_env):
    """Test that status shows logging is inactive when stopped."""
    result = run_cmd(["cmd-logger", "status", "cmd-log"])
    assert result.returncode == 0
    assert "Logging is inactive" in result.stdout


def test_logging_commands_to_file(setup_env):
    """Test that executed commands are logged when logging is active."""
    run_cmd(["cmd-logger", "start", "cmd-log"])
    # Simulate a command
    subprocess.run(["echo", "Hello, world!"])
    subprocess.run(["ls"])

    # Stop logging
    run_cmd(["cmd-logger", "stop", "cmd-log"])

    # Verify that the command was logged
    assert os.path.exists(LOG_FILE)
    with open(LOG_FILE, "r") as f:
        log_contents = f.read()
    assert "echo Hello, world!" in log_contents
    assert "ls" in log_contents


def test_logging_does_not_append_when_stopped(setup_env):
    """Test that no new commands are logged when logging is stopped."""
    run_cmd(["cmd-logger", "start", "cmd-log"])
    subprocess.run(["echo", "Logged Command"])
    run_cmd(["cmd-logger", "stop", "cmd-log"])
    subprocess.run(["echo", "Unlogged Command"])

    # Verify only the first command was logged
    with open(LOG_FILE, "r") as f:
        log_contents = f.read()
    assert "Logged Command" in log_contents
    assert "Unlogged Command" not in log_contents


def test_log_file_persistence(setup_env):
    """Test that the log file persists between multiple start/stop cycles."""
    run_cmd(["cmd-logger", "start", "cmd-log"])
    subprocess.run(["echo", "First Command"])
    run_cmd(["cmd-logger", "stop", "cmd-log"])

    run_cmd(["cmd-logger", "start", "cmd-log"])
    subprocess.run(["echo", "Second Command"])
    run_cmd(["cmd-logger", "stop", "cmd-log"])

    # Verify both commands are logged
    with open(LOG_FILE, "r") as f:
        log_contents = f.read()
    assert "First Command" in log_contents
    assert "Second Command" in log_contents


def test_log_file_error_handling(setup_env):
    """Test that the tool handles file write errors gracefully."""
    # Make log file unwritable
    open(LOG_FILE, "w").close()
    os.chmod(LOG_FILE, 0o444)  # Read-only

    result = run_cmd(["cmd-logger", "start", "cmd-log"])
    assert result.returncode != 0
    assert "Error: Cannot write to log file" in result.stderr

    os.chmod(LOG_FILE, 0o644)  # Restore permissions
