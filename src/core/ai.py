# This module handles the interaction with the Gemini CLI.

import subprocess
import shutil
import time
import sys
from utils.errors import handle_error

def generate_commit_message(prompt):
    """Generates a commit message from a prompt, with retries for quota errors."""
    if not shutil.which('gemini'):
        handle_error("gemini not found in PATH", "Please install the gemini agent and ensure it is in your PATH.")

    max_retries = 5
    retry_delay = 1

    # Retry on API quota errors (HTTP 429).
    for i in range(max_retries):
        try:
            process = subprocess.run(
                ['gemini', '-p', prompt],
                capture_output=True,
                text=True,
                check=True
            )
            # Filter out unwanted lines from the output.
            lines = process.stdout.strip().split('\n')
            filtered_lines = [line for line in lines if not line.strip().startswith("MCP")]
            return '\n'.join(filtered_lines)
        except subprocess.CalledProcessError as e:
            # Filter out MCP lines from stderr
            stderr_lines = e.stderr.strip().split('\n')
            filtered_stderr_lines = [line for line in stderr_lines if not line.strip().startswith("MCP")]
            filtered_stderr = '\n'.join(filtered_stderr_lines)

            if "429" in e.stderr or "Quota exceeded" in e.stderr:
                if i < max_retries - 1:
                    print(
                        f"API quota error (429). Retrying in {retry_delay}s... [{i+1}/{max_retries}]",
                        file=sys.stderr
                    )
                    time.sleep(retry_delay)
                else:
                    handle_error("API quota exceeded after maximum retries.", filtered_stderr)
            elif not filtered_stderr.strip():
                # Stderr only contained MCP lines, so we can treat it as a success.
                # Filter stdout from the exception and return it.
                stdout_lines = e.stdout.strip().split('\n')
                filtered_stdout_lines = [line for line in stdout_lines if not line.strip().startswith("MCP")]
                commit_message = '\n'.join(filtered_stdout_lines)
                if commit_message.strip():
                    return commit_message
                else:
                    handle_error("Command failed with only MCP errors, but produced no output on stdout.")
            else:
                handle_error("An unexpected error occurred while calling the Gemini CLI.", filtered_stderr)
        except FileNotFoundError:
            handle_error("'gemini' command not found. Make sure it is installed and in your PATH.")

    handle_error("Failed to generate commit message after all retries.")
