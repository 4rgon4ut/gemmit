# gemmit

`gemmit` is a command-line tool that uses the [gemini-cli](https://github.com/google/gemini-cli) to generate Git commit messages from templates based on your staged changes.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/gemmit.git
    cd gemmit
    ```

2.  **Run the installer:**
    ```bash
    ./install.sh
    ```

3.  **Update your shell profile:**

    Add the following line to your shell profile (e.g., `~/.bashrc`, `~/.zshrc`):
    ```bash
    export PATH="$HOME/.gemmit:$PATH"
    ```

4.  **Set up the Git hook:**

    In your Git repository, run the following command to set up the `prepare-commit-msg` hook:
    ```bash
    ln -s ~/.gemmit/gemmit-hook .git/hooks/prepare-commit-msg
    ```

## Usage

To generate a commit message, use the `gemmit` command:

```bash
gemmit [options] <template>
```

### Options

*   `-a`, `--add`: Stage all tracked files before committing.
*   `-h`, `--help`: Show the help message.
*   `-y`: Automatically use the generated commit message without confirmation.

### Templates

`gemmit` uses templates to generate commit messages. You can define your own templates in the `~/.gemmit/config.json` file.

The default templates are:

*   `semantic`: Generates a commit message in the [Conventional Commits](https://www.conventionalcommits.org/) format.
*   `kernel`: Generates a commit message in the Linux kernel format.

### Examples

*   **Generate a semantic commit message:**
    ```bash
    gemmit semantic
    ```

*   **Stage all files and generate a kernel commit message:**
    ```bash
    gemmit -a kernel
    ```
