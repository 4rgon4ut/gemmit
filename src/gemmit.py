#!/usr/bin/env python3

import argparse
import sys
import subprocess
from commands.generate import run as generate_run
from core.config import get_template, set_default_template, load_config
from core.git import get_staged_diff, stage_all_files, get_current_branch, get_remote_url
from utils.errors import handle_error
from core.ai import generate_commit_message


def main():
    """Main entry point for the gemmit tool."""
    parser = argparse.ArgumentParser(
        description="A tool to generate commit messages using AI.",
        usage="gemmit <template> [<args>]",
    )

    parser.add_argument(
        "template",
        nargs="?",
        default=None,
        help="The name of the template to use for the commit message.",
    )
    parser.add_argument(
        "--set-default",
        dest="default_template",
        metavar="TEMPLATE_NAME",
        help="Set the default template to use.",
    )
    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Stage all tracked files before committing.",
    )
    parser.add_argument(
        "-p", "--push", action="store_true", help="Push after committing."
    )
    parser.add_argument(
        "-y", "--yes", action="store_true", help="Skip confirmation prompt."
    )

    args, unknown_args = parser.parse_known_args()

    if args.default_template:
        set_default_template(args.default_template)
        return

    if args.add:
        print("Adding all files...")
        stage_all_files()

    template_name = args.template
    if not template_name:
        config = load_config()
        template_name = config.get("default_template")
        if not template_name:
            parser.error(
                "a template name is required, or a default must be set with --set-default."
            )

    commit_message = None
    if args.yes:
        template = get_template(template_name)
        diff = get_staged_diff()
        if not diff:
            print("No staged changes found.")
            sys.exit(0)
        print("Generating commit message...")
        prompt = template.get("prompt", "") + "\n\n" + diff
        commit_message = generate_commit_message(prompt)
    else:
        commit_message = generate_run(unknown_args + ([template_name] if template_name and not unknown_args else []))

    if commit_message:
        try:
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
        except subprocess.CalledProcessError as e:
            handle_error("committing changes", e)

        if args.push:
            try:
                branch = get_current_branch()
                remote_url = get_remote_url()
                config = load_config()
                highlight_color = config.get("highlight_color", "green")
                from rich.console import Console
                console = Console()
                if remote_url:
                    console.print(f"[{highlight_color}]Pushing to {remote_url}...[/{highlight_color}]")
                else:
                    console.print(f"[{highlight_color}]Pushing changes...[/{highlight_color}]")
                subprocess.run(["git", "push", "-u", "origin", branch], check=True)
            except subprocess.CalledProcessError as e:
                handle_error("pushing changes", e)


if __name__ == "__main__":
    main()

