# This module contains the logic for the `generate` command.

import sys
from core.ai import generate_commit_message
from core.config import get_template
from core.git import get_staged_diff
from utils.errors import handle_error

def run(args):
    """Generates a commit message and prints it to stdout."""
    if not args:
        handle_error("No template specified.", "Usage: gemmit add <template>")
        return

    template_name = args[0]
    template = get_template(template_name)
    diff = get_staged_diff()

    # Exit gracefully if there are no staged changes.
    if not diff:
        print("No staged changes found.")
        sys.exit(0)

    prompt = template.get('prompt', '') + '\n\n' + diff
    commit_message = generate_commit_message(prompt)

    # Print the commit message to stdout for the calling script.
    print(commit_message)

