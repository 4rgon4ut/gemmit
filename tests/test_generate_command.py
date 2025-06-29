
import pytest
from unittest.mock import patch, MagicMock
from commands import generate

@patch('commands.generate.get_template')
@patch('commands.generate.get_staged_diff')
@patch('commands.generate.generate_commit_message')
def test_run_success(mock_generate_commit, mock_get_diff, mock_get_template):
    """Tests the successful run of the generate command."""
    # Setup mocks
    mock_get_template.return_value = {"prompt": "Test prompt"}
    mock_get_diff.return_value = "diff --git a/file.txt b/file.txt"
    mock_generate_commit.return_value = "feat: This is a test commit"

    # Run the command
    with patch('builtins.print') as mock_print:
        generate.run(["my-template"])

    # Assertions
    mock_get_template.assert_called_once_with("my-template")
    mock_get_diff.assert_called_once()
    expected_prompt = "Test prompt\n\ndiff --git a/file.txt b/file.txt"
    mock_generate_commit.assert_called_once_with(expected_prompt)
    mock_print.assert_called_once_with("feat: This is a test commit")

@patch('commands.generate.get_template')
@patch('commands.generate.get_staged_diff')
def test_run_no_staged_changes(mock_get_diff, mock_get_template):
    """Tests that the command exits gracefully if there are no staged changes."""
    # Setup mocks
    mock_get_template.return_value = {"prompt": "Test prompt"}
    mock_get_diff.return_value = ""  # No diff

    with pytest.raises(SystemExit) as e:
        generate.run(["my-template"])
    
    assert e.value.code == 0 # Should exit successfully

@patch('commands.generate.handle_error')
def test_run_no_template_specified(mock_handle_error):
    """Tests that the command calls the error handler if no template is given."""
    generate.run([]) # No arguments
    mock_handle_error.assert_called_once_with("No template specified.", "Usage: gemmit add <template>")
