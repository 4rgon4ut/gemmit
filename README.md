# gemmit

A simple tool to generate commit messages using the gemini agent.

## Prerequisites

*   You must have the `gemini` agent installed and available in your system's `PATH`.

## Installation

To install gemmit, run the following command:

```bash
./install.sh
```

This will install the tool in `~/.gemmit`. You will also need to add `~/.gemmit` to your `PATH` by adding the following line to your shell profile (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
export PATH="$HOME/.gemmit:$PATH"
```

## Usage

To use gemmit, you need to set it up as a git hook in your repository. Run the following command in your git repository:

```bash
ln -s ~/.gemmit/gemmit-hook .git/hooks/prepare-commit-msg
```

Then, you can use the `gemmit` command to generate commit messages:

```bash
gemmit <template>
```

To add all files before committing, use the `--add` flag:

```bash
gemmit --add <template>
```

After generating the message, the tool will ask for your confirmation before committing. To bypass this confirmation, you can either use the `-y` flag:

```bash
gemmit <template> -y
```

Or, you can set the `autoconfirm` option to `true` in your `~/.gemmit/config.json` file.

### Available Templates

*   `semantic`: Generates a commit message in the format `type(scope): message`.
*   `kernel`: Generates a commit message in the Linux kernel style.

### Custom Templates

You can add your own templates to `~/.gemmit/config.json`.
