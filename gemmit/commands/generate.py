# This module contains the logic for the `generate` command.

import sys
import subprocess
import tempfile
import os
from rich.console import Console

from ..core.ai import generate_commit_message
from ..core.config import get_template, load_config
from ..core.git import get_staged_diff
from ..utils.errors import handle_error


def run(args):
    """Generates a commit message and provides options to accept, edit, or regenerate."""
    if not args:
        config = load_config()
        template_name = config.get("default_template")
        if not template_name:
            handle_error(
                "No template specified and no default template set.",
                "Usage: gemmit add <template> or gemmit --set-default <template>",
            )
            return
    else:
        template_name = args[0]

    template = get_template(template_name)
    diff = get_staged_diff()

    if not diff:
        print("No staged changes found.")
        sys.exit(0)

    console = Console()
    commit_message = ""

    while True:
        prompt = template.get("prompt", "") + "\n\n" + diff
        commit_message = generate_commit_message(prompt)

        config = load_config()
        highlight_color = config.get("highlight_color", "green")

        console.print(
            f"[{highlight_color}]--- Generated Commit Message ---[/{highlight_color}]\n"
        )
        console.print(f"[{highlight_color}]{commit_message}[/{highlight_color}]\n")
        console.print(
            f"[{highlight_color}]--------------------------------[/{highlight_color}]\n"
        )

        answer = console.input(
            "Use this message? [Y]es, [E]dit, [R]egenerate, [N]o: "
        ).lower()

        if answer in ["y", "yes", ""]:
            break
        elif answer in ["e", "edit"]:
            editor = os.getenv("EDITOR", "vim")
            with tempfile.NamedTemporaryFile(
                mode="w+", delete=False, suffix=".md"
            ) as tmpfile:
                tmpfile.write(commit_message)
                tmpfile.flush()
                subprocess.run(editor.split() + [tmpfile.name])
                tmpfile.seek(0)
                commit_message = tmpfile.read().strip()
            break
        elif answer in ["r", "regenerate"]:
            console.print("[yellow]Regenerating...[/yellow]")
            continue
        elif answer in ["n", "no"]:
            console.print("[red]Commit aborted.[/red]")
            sys.exit(1)

    # Return the final commit message.
    return commit_message
