import os
import sys
import json
import subprocess
import shutil

def get_git_diff():
    return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')

def generate_commit_message(template_name, diff):
    config_path = os.path.expanduser('~/.gemmits/config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    template = config['templates'][template_name]
    prompt = template['prompt'] + '\n\n' + diff

    if not shutil.which('gemini-cli'):
        print("Error: gemini-cli not found in PATH.", file=sys.stderr)
        print("Please install the gemini-cli agent and ensure it is in your PATH.", file=sys.stderr)
        sys.exit(1)

    try:
        commit_message = subprocess.check_output(['gemini-cli', prompt], text=True).strip()
        return commit_message
    except subprocess.CalledProcessError as e:
        print(f"Error calling gemini-cli: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'gemini-cli' command not found. Make sure it is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def main():
    commit_msg_filepath = sys.argv[1]
    template_name = 'semantic'  # Default template

    # Load config to check templates and autoconfirm
    config_path = os.path.expanduser('~/.gemmits/config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    autoconfirm = config.get('autoconfirm', False)

    with open(commit_msg_filepath, 'r') as f:
        first_line = f.readline().strip()
        if first_line:
            args = first_line.split()
            if args and args[0] in config['templates']:
                template_name = args[0]
            if '-y' in args:
                autoconfirm = True

    diff = get_git_diff()
    if not diff:
        sys.exit(0)

    commit_message = generate_commit_message(template_name, diff)

    if not autoconfirm:
        print("--- Generated Commit Message ---")
        print(commit_message)
        print("--------------------------------")
        try:
            with open('/dev/tty') as tty:
                tty.write("Use this commit message? [Y/n] ")
                answer = tty.readline().strip()
                if answer.lower() == 'n':
                    print("Commit aborted by user.", file=sys.stderr)
                    sys.exit(1)
        except (IOError, OSError):
            # If /dev/tty is not available, proceed with the commit
            pass

    with open(commit_msg_filepath, 'w') as f:
        f.write(commit_message)

if __name__ == '__main__':
    main()
