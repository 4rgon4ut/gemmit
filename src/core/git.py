# This module contains helper functions for interacting with Git.

import subprocess
from utils.errors import handle_error

def get_staged_diff():
    """Gets the staged diff from git."""
    try:
        return subprocess.check_output(['git', 'diff', '--cached'], text=True)
    except subprocess.CalledProcessError as e:
        handle_error("getting staged diff", e)

def stage_all_files():
    """Stages all tracked files in the repository."""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
    except subprocess.CalledProcessError as e:
        handle_error("staging all files", e)
