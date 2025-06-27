#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import shutil

def get_git_diff():
    return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')

def generate_commit_message(template_name, diff):
    config_path = os.path.expanduser('~/.gemmit/config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    template = config['templates'][template_name]
    prompt = template['prompt'] + '\n\n' + diff

    if not shutil.which('gemini'):
        print("Error: gemini not found in PATH.", file=sys.stderr)
        print("Please install the gemini agent and ensure it is in your PATH.", file=sys.stderr)
        sys.exit(1)

    try:
        commit_message = subprocess.check_output(['gemini', '-p', prompt], text=True).strip()
        return commit_message
    except subprocess.CalledProcessError as e:
        print(f"Error calling gemini: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'gemini' command not found. Make sure it is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def main():
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