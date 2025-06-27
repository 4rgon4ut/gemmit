#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import shutil
import argparse

def get_git_diff():
    """Gets the staged git diff."""
    return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')

def call_gemini(prompt):
    """Calls the gemini CLI with the given prompt."""
    if not shutil.which('gemini'):
        print("Error: gemini not found in PATH.", file=sys.stderr)
        print("Please install the gemini agent and ensure it is in your PATH.", file=sys.stderr)
        sys.exit(1)
    try:
        # The '-p -' tells gemini to read the prompt from stdin
        process = subprocess.run(
            ['gemini', '-p', '-'],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error calling gemini: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'gemini' command not found. Make sure it is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def generate_commit_message_from_template(template_name, diff):
    """Generates a commit message from a template."""
    config_path = os.path.expanduser('~/.gemmit/config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {config_path}", file=sys.stderr)
        sys.exit(1)


    if template_name not in config.get('templates', {}):
        print(f"Error: Template '{template_name}' not found in config.", file=sys.stderr)
        sys.exit(1)

    template = config['templates'][template_name]
    prompt = template.get('prompt', '') + '\n\n' + diff
    return call_gemini(prompt)

def generate_commit_message_from_prompt(custom_prompt, diff):
    """Generates a commit message from a custom prompt."""
    prompt = custom_prompt + '\n\n' + diff
    return call_gemini(prompt)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate a commit message using Gemini.")
    parser.add_argument('template', nargs='?', default=None, help='The name of the template to use.')
    parser.add_argument('--prompt', default=None, help='A custom prompt to use instead of a template.')

    args = parser.parse_args()

    if not args.template and not args.prompt:
        parser.error("either a template or a --prompt must be provided.")

    if args.template and args.prompt:
        parser.error("you cannot provide both a template and a --prompt.")

    diff = get_git_diff()
    if not diff:
        print("No staged changes found.", file=sys.stderr)
        sys.exit(0)

    if args.prompt:
        commit_message = generate_commit_message_from_prompt(args.prompt, diff)
    else:
        commit_message = generate_commit_message_from_template(args.template, diff)

    print(commit_message)

if __name__ == '__main__':
    main()
