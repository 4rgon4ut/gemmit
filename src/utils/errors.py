# This module provides a centralized error handling function.

import sys

def handle_error(message, error=None, max_lines=5):
    """Prints a formatted error message and exits."""
    print(f"Error: {message}", file=sys.stderr)
    if error:
        error_str = str(error)
        error_lines = error_str.split('\n')
        # Truncate long error messages.
        if len(error_lines) > max_lines:
            truncated_error = '\n'.join(error_lines[:max_lines])
            print(f"Details:\n{truncated_error}\n[...]", file=sys.stderr)
        else:
            print(f"Details:\n{error_str}", file=sys.stderr)
    sys.exit(1)
