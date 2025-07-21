# This module contains helper functions for interacting with Git.

import subprocess
from utils.errors import handle_error

def get_staged_diff():
    """Gets the staged diff from git."""
    try:
        return subprocess.check_output(['git', 'diff', '--cached']).decode()
    except subprocess.CalledProcessError as e:
        handle_error("getting staged diff", e)

def get_current_branch():
    """Gets the current git branch name."""
    try:
        return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
    except subprocess.CalledProcessError as e:
        handle_error("getting current branch", e)

def get_remote_url():
    """Gets the URL of the remote repository."""
    try:
        return subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip()
    except subprocess.CalledProcessError:
        # If the remote doesn't exist, return an empty string
        return ""

def stage_all_files():
    """Stages all tracked files in the repository."""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
    except subprocess.CalledProcessError as e:
        handle_error("staging all files", e)
