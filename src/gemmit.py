#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import shutil
import time

def get_git_diff():
    """Gets the staged git diff."""
    return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')

def generate_commit_message(template_name, diff):
    """Generates a commit message from a template, with retries for quota errors."""
    config_path = os.path.expanduser('~/.gemmit/config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing config file at {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if template_name not in config.get('templates', {}):
        print(f"Error: Template '{template_name}' not found in config.", file=sys.stderr)
        sys.exit(1)

    template = config['templates'][template_name]
    prompt = template.get('prompt', '') + '\n\n' + diff

    if not shutil.which('gemini'):
        print("Error: gemini not found in PATH.", file=sys.stderr)
        print("Please install the gemini agent and ensure it is in your PATH.", file=sys.stderr)
        sys.exit(1)

    max_retries = 5
    retry_delay = 1

    for i in range(max_retries):
        try:
            process = subprocess.run(
                ['gemini', '-p', prompt],
                capture_output=True,
                text=True,
                check=True
            )
            return process.stdout.strip()
        except subprocess.CalledProcessError as e:
            if "429" in e.stderr or "Quota exceeded" in e.stderr:
                if i < max_retries - 1:
                    print(
                        f"API quota error (429). Retrying in {retry_delay}s... [{i+1}/{max_retries}]",
                        file=sys.stderr
                    )
                    time.sleep(retry_delay)
                else:
                    print("API quota exceeded after maximum retries.", file=sys.stderr)
                    print(f"Final error from Gemini CLI:\n{e.stderr}", file=sys.stderr)
                    sys.exit(1)
            else:
                print("An unexpected error occurred while calling the Gemini CLI.", file=sys.stderr)
                print(f"Stderr:\n{e.stderr}", file=sys.stderr)
                sys.exit(1)
        except FileNotFoundError:
            # This is a fallback, as shutil.which should catch it first.
            print("Error: 'gemini' command not found. Make sure it is installed and in your PATH.", file=sys.stderr)
            sys.exit(1)

    # This part should not be reached, but as a safeguard.
    print("Failed to generate commit message after all retries.", file=sys.stderr)
    sys.exit(1)


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: gemmit.py <template>", file=sys.stderr)
        sys.exit(1)

    template_name = sys.argv[1]
    diff = get_git_diff()
    if not diff:
        print("No staged changes found.", file=sys.stderr)
        sys.exit(0)

    commit_message = generate_commit_message(template_name, diff)
    print(commit_message)

if __name__ == '__main__':
    main()
