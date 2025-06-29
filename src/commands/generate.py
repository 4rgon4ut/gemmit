
import sys
from core.ai import generate_commit_message
from core.config import get_template
from core.git import get_staged_diff
from utils.errors import handle_error

def run(args):
    """Generates a commit message and adds it to the staging area."""
    if not args:
        handle_error("No template specified.", "Usage: gemmit add <template>")
        return

    template_name = args[0]
    template = get_template(template_name)
    diff = get_staged_diff()

    if not diff:
        print("No staged changes found.")
        sys.exit(0)

    prompt = template.get('prompt', '') + '\n\n' + diff
    commit_message = generate_commit_message(prompt)

    # The commit message is printed to stdout, which the git hook will capture.
    print(commit_message)
