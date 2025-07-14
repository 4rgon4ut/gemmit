#!/usr/bin/env python3

import argparse
import sys
import subprocess
from core.ai import generate_commit_message
from core.config import get_template, set_default_template, load_config
from core.git import get_staged_diff, stage_all_files
from utils.errors import handle_error

def main():
    """Main entry point for the gemmit tool."""
    parser = argparse.ArgumentParser(
        description="A tool to generate commit messages using AI.",
        usage="gemmit <template> [<args>]"
    )
    
    parser.add_argument(
        'template',
        nargs='?',
        default=None,
        help='The name of the template to use for the commit message.'
    )
    parser.add_argument(
        '--set-default',
        dest='default_template',
        metavar='TEMPLATE_NAME',
        help='Set the default template to use.'
    )
    parser.add_argument(
        '-a', '--add',
        action='store_true',
        help='Stage all tracked files before committing.'
    )
    parser.add_argument(
        '-p', '--push',
        action='store_true',
        help='Push after committing.'
    )
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Skip confirmation prompt.'
    )

    args = parser.parse_args()

    if args.default_template:
        set_default_template(args.default_template)
        return

    if args.add:
        print("Adding all files...")
        stage_all_files()

    template_name = args.template
    if not template_name:
        config = load_config()
        template_name = config.get('default_template')
        if not template_name:
            parser.error("a template name is required, or a default must be set with --set-default.")

    template = get_template(template_name)
    diff = get_staged_diff()

    # Exit gracefully if there are no staged changes.
    if not diff:
        print("No staged changes found.")
        sys.exit(0)

    prompt = template.get('prompt', '') + '\n\n' + diff
    commit_message = generate_commit_message(prompt)

    if not args.yes and sys.stdout.isatty():
        print("--- Generated Commit Message ---")
        print(commit_message)
        print("--------------------------------")
        answer = input("Use this message? [Y/n] ")
        if answer.lower() not in ['y', 'yes', '']:
            print("Commit aborted by user.")
            sys.exit(1)

    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
    except subprocess.CalledProcessError as e:
        handle_error("committing changes", e)

    if args.push:
        try:
            print("Pushing changes...")
            subprocess.run(['git', 'push'], check=True)
        except subprocess.CalledProcessError as e:
            handle_error("pushing changes", e)

if __name__ == '__main__':
    main()