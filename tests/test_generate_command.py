
import pytest
from unittest.mock import patch, MagicMock
from commands import generate

@patch('commands.generate.Console')
@patch('commands.generate.get_template')
@patch('commands.generate.get_staged_diff')
@patch('commands.generate.generate_commit_message')
def test_run_success(mock_generate_commit, mock_get_diff, mock_get_template, mock_console):
    """Tests the successful run of the generate command with user accepting."""
    # Setup mocks
    mock_get_template.return_value = {"prompt": "Test prompt"}
    mock_get_diff.return_value = "diff --git a/file.txt b/file.txt"
    mock_generate_commit.return_value = "feat: This is a test commit"
    
    # Mock the console input to return 'y' for 'yes'
    mock_console_instance = MagicMock()
    mock_console_instance.input.return_value = "y"
    mock_console.return_value = mock_console_instance

    # Run the command
    result = generate.run(["my-template"])

    # Assertions
    assert result == "feat: This is a test commit"
    mock_get_template.assert_called_once_with("my-template")
    mock_get_diff.assert_called_once()
    expected_prompt = "Test prompt\n\ndiff --git a/file.txt b/file.txt"
    mock_generate_commit.assert_called_once_with(expected_prompt)
    mock_console_instance.input.assert_called_once_with("Use this message? [Y]es, [E]dit, [R]egenerate, [N]o: ")


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

@patch('commands.generate.load_config')
@patch('commands.generate.handle_error')
def test_run_no_template_specified(mock_handle_error, mock_load_config):
    """Tests that the command calls the error handler if no template is given."""
    mock_load_config.return_value = {}
    generate.run([]) # No arguments
    mock_handle_error.assert_called_once_with("No template specified and no default template set.", "Usage: gemmit add <template> or gemmit --set-default <template>")
