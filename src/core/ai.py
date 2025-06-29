
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

    for i in range(max_retries):
        try:
            process = subprocess.run(
                ['gemini', '-p', prompt],
                capture_output=True,
                text=True,
                check=True
            )
            return process.stdout.strip()
        except subprocess.CalledProcessError as e:
            if "429" in e.stderr or "Quota exceeded" in e.stderr:
                if i < max_retries - 1:
                    print(
                        f"API quota error (429). Retrying in {retry_delay}s... [{i+1}/{max_retries}]",
                        file=sys.stderr
                    )
                    time.sleep(retry_delay)
                else:
                    handle_error("API quota exceeded after maximum retries.", e.stderr)
            else:
                handle_error("An unexpected error occurred while calling the Gemini CLI.", e.stderr)
        except FileNotFoundError:
            # This is a fallback, as shutil.which should catch it first.
            handle_error("'gemini' command not found. Make sure it is installed and in your PATH.")

    # This part should not be reached, but as a safeguard.
    handle_error("Failed to generate commit message after all retries.")
