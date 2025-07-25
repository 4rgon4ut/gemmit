import pytest
from unittest.mock import patch
import subprocess
from gemmit.core import git


@patch("subprocess.check_output")
def test_get_staged_diff_success(mock_check_output):
    """Tests that get_staged_diff returns the correct diff on success."""
    mock_check_output.return_value = b"diff --git a/file.txt b/file.txt\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-hello\n+world"

    diff = git.get_staged_diff()
    assert "-hello" in diff
    assert "+world" in diff
    mock_check_output.assert_called_once_with(["git", "diff", "--cached"])


@patch("subprocess.check_output")
def test_get_staged_diff_no_changes(mock_check_output):
    """Tests that get_staged_diff returns an empty string when there are no changes."""
    mock_check_output.return_value = b""

    diff = git.get_staged_diff()
    assert diff == ""


@patch("subprocess.check_output")
def test_get_staged_diff_error(mock_check_output):
    """Tests that get_staged_diff handles errors from git."""
    mock_check_output.side_effect = subprocess.CalledProcessError(
        1, ["git", "diff", "--cached"], b"fatal: not a git repository"
    )

    with pytest.raises(SystemExit):
        git.get_staged_diff()
