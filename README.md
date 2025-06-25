# gemmits

A simple tool to generate commit messages using the gemini-cli agent.

## Prerequisites

*   You must have the `gemini-cli` agent installed and available in your system's `PATH`.

## Installation

To install gemmits, run the following command:

```bash
./install.sh
```

This will install the tool in `~/.gemmits`.

## Usage

To use gemmits, you need to set it up as a git hook in your repository. Run the following command in your git repository:

```bash
ln -s ~/.gemmits/gemmits.py .git/hooks/prepare-commit-msg
```

Then, when you run `git commit`, you can specify a template like this:

```bash
git commit -m "semantic"
```

This will generate a commit message using the `semantic` template. If you don't specify a template, it will default to `semantic`.

After generating the message, the tool will ask for your confirmation before committing. To bypass this confirmation, you can either use the `-y` flag in your commit message:

```bash
git commit -m "semantic -y"
```

Or, you can set the `autoconfirm` option to `true` in your `~/.gemmits/config.json` file.

### Available Templates

*   `semantic`: Generates a commit message in the format `type(scope): message`.
*   `kernel`: Generates a commit message in the Linux kernel style.

### Custom Templates

You can add your own templates to `~/.gemmits/config.json`.
