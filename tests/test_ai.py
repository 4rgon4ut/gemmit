
import pytest
from unittest.mock import patch, MagicMock
import subprocess
from core import ai

# Successful response from the gemini CLI
MOCK_SUCCESS_RESPONSE = MagicMock(
    stdout="feat: Implement the new feature",
    stderr="",
    returncode=0
)

# Error response for quota exceeded
MOCK_QUOTA_ERROR_RESPONSE = MagicMock(
    stdout="",
    stderr="Error: 429 Quota exceeded for model.",
    returncode=1
)

# Generic error response
MOCK_GENERIC_ERROR_RESPONSE = MagicMock(
    stdout="",
    stderr="An unexpected error occurred.",
    returncode=1
)

@patch('shutil.which', return_value='/usr/local/bin/gemini')
@patch('subprocess.run')
def test_generate_commit_message_success(mock_run, mock_which):
    """Tests a successful commit message generation."""
    mock_run.return_value = MOCK_SUCCESS_RESPONSE

    message = ai.generate_commit_message("some prompt")
    assert message == "feat: Implement the new feature"
    mock_run.assert_called_once()

@patch('shutil.which', return_value='/usr/local/bin/gemini')
@patch('subprocess.run')
def test_generate_commit_message_filters_mcp_lines(mock_run, mock_which):
    """Tests that MCP lines are filtered from the output."""
    mock_run.return_value = MagicMock(
        stdout="MCP STDOUT: some debug info\nfeat: A new feature\nMCP STDOUT: more info",
        stderr="MCP STDERR: some error\nAnother error",
        returncode=0
    )

    message = ai.generate_commit_message("a prompt")
    assert message == "feat: A new feature"

@patch('shutil.which', return_value='/usr/local/bin/gemini')
@patch('subprocess.run')
def test_generate_commit_message_retry_then_succeed(mock_run, mock_which):
    """Tests that the retry logic works on quota errors."""
    # Simulate a quota error, then a success
    mock_run.side_effect = [subprocess.CalledProcessError(1, ['gemini'], stderr="Error: 429 Quota exceeded for model."), MOCK_SUCCESS_RESPONSE]

    with patch('time.sleep') as mock_sleep: # Don't actually sleep in tests
        message = ai.generate_commit_message("some prompt")
        assert message == "feat: Implement the new feature"
        assert mock_run.call_count == 2
        mock_sleep.assert_called_once()

@patch('shutil.which', return_value='/usr/local/bin/gemini')
@patch('subprocess.run')
def test_generate_commit_message_max_retries_exceeded(mock_run, mock_which):
    """Tests that the function exits after the maximum number of retries."""
    # Simulate continuous quota errors
    mock_run.side_effect = subprocess.CalledProcessError(1, ['gemini'], stderr="Error: 429 Quota exceeded for model.")

    with pytest.raises(SystemExit):
        with patch('time.sleep'): # Don't actually sleep in tests
            ai.generate_commit_message("some prompt")
    
    assert mock_run.call_count == 5 # Default max_retries is 5

@patch('shutil.which', return_value=None)
def test_generate_commit_message_gemini_not_found(mock_which):
    """Tests that the function exits if the gemini CLI is not found."""
    with pytest.raises(SystemExit):
        ai.generate_commit_message("some prompt")


