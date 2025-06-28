
import subprocess
from utils.errors import handle_error

def get_staged_diff():
    """Gets the staged git diff."""
    try:
        return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
    except subprocess.CalledProcessError as e:
        handle_error("getting git diff", e)
