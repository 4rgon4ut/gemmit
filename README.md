# gemmit [WIP]

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

## Usage

To generate a commit message, use the `gemmit` command:

```bash
gemmit [options] <template>
```

### Options

*   `-a`, `--add`: Stage all tracked files before committing.
*   `-h`, `--help`: Show the help message.
*   `-p`, `--prompt`: Pass a prompt to the `gemini` command.
*   `-y`: Automatically use the generated commit message without confirmation.

### Templates

`gemmit` uses templates to generate commit messages. You can define your own templates in the `~/.gemmit/config.json` file.

The default templates are:

*   `oneline`: Generates a oneline commit message in the [Conventional Commits](https://www.conventionalcommits.org/) format.
*   `kernel`: Generates a verbose commit message in the Linux Kernel format.

### Configuration

You can configure `gemmit` by editing the `~/.gemmit/config.json` file.

#### Confirmation Prompt

By default, `gemmit` will ask for confirmation before using a generated commit message. You can disable this by setting the `autoconfirm` option to `true` in the `config.json` file.

```json
{
  "autoconfirm": true
}
```

### Examples

*   **Generate a oneline commit message:**
    ```bash
    gemmit oneline
    ```

*   **Stage all files and generate a kernel commit message:**
    ```bash
    gemmit -a kernel
    ```
