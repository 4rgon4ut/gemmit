# Project State Summary: gemmit

This file summarizes the state of the 'gemmit' project to provide context for a new Gemini session.

## 1. Project Goal

The user wants to create a command-line tool named `gemmit` that uses the `gemini` CLI to generate Git commit messages from templates based on the output of `git diff --cached`.

## 2. Development Process

After making any changes to the application, it is crucial to run the automated test suite to ensure that existing functionality has not been broken. 

To run the tests, execute the following command from the project root:

```bash
pytest
```

All tests must pass before committing changes.

## 3. Current File Structure

The user has reorganized the project. The current structure is:

-   `/install.sh`: The main installation script.
-   `/src/`: A directory containing all the core application files.
    -   `/src/gemmit`: The user-facing wrapper script.
    -   `/src/gemmit-hook`: The script that acts as the `prepare-commit-msg` Git hook.
    -   `/src/gemmit.py`: The main Python script with the core logic.
    -   `/src/config.json`: Configuration for templates and settings.
-   `/tests/`: A directory containing all the automated tests.

The tool is installed into `~/.gemmit`.

## 4. The Problem We Are Solving

The confirmation prompt (`Use this commit message? [Y/n]`) is not appearing, even when `autoconfirm` is `false` in the config. This is because the `gemmit.py` script was using a method (`open('/dev/tty')`) to get user input that fails silently when run inside a Git hook.

## 5. The Fix (Already Implemented in `src/`)

The code in `/src/gemmit.py` has already been modified to use Python's standard `input()` function, which correctly handles interactive prompts in this scenario.

## 6. The Blocker (What to do next)

The `install.sh` script is broken. It has not been updated to account for the new `/src` directory. It is still trying to copy files from a `gemmit/` subdirectory, which no longer exists.

## 7. Action Plan for Next Session

1.  **Read the `install.sh` file.**
2.  **Modify the `SOURCE_DIR` variable** inside `install.sh`.
    -   **Change this:** `SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/gemmit"`
    -   **To this:** `SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/src"`
3.  **Instruct the user to run `./install.sh`**. This will copy the corrected `gemmit.py` (with the `input()` fix) to `~/.gemmit`.
4.  **Ask the user to test the tool** to confirm the interactive prompt now works.