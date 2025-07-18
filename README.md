# gemmit

A command-line tool that uses the `gemini` CLI to generate Git commit messages from your staged changes.

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

    Add the following line to your `~/.bashrc`, `~/.zshrc`, or other shell profile:
    ```bash
    export PATH="$HOME/.gemmit:$PATH"
    ```

## Usage

```bash
gemmit [options] <template>
```

### Interactive Mode

By default, `gemmit` runs in an interactive mode that allows you to review, edit, or regenerate the commit message before committing.

```
--- Generated Commit Message ---
feat: Add interactive editing to gemmit

This commit introduces a new interactive mode to the gemmit tool.
Users can now review, edit, or regenerate the AI-generated commit
message before it is committed.
--------------------------------
Use this message? [Y]es, [E]dit, [R]egenerate, [N]o: 
```

*   **[Y]es:** Accepts the message and commits.
*   **[E]dit:** Opens the message in your default text editor for manual changes.
*   **[R]egenerate:** Generates a new message using the same template.
*   **[N]o:** Aborts the commit.

**Note:** The "Edit" feature relies on the `$EDITOR` environment variable. Make sure it is configured in your shell profile (e.g., `export EDITOR=vim`). If it's not set, it will default to `vim`.

### Options

Flags can be combined (e.g., `-apy`).

*   `-a`: Stage all tracked files (`git add .`) before generating the message.
*   `-p`: Push changes to the remote repository after a successful commit.
*   `-y`: (YOLO mode) Skip the interactive confirmation and commit directly.
*   `-h`: Show the help message.

### Examples

**1. Basic Commit**

Stage your files manually, then generate a commit message using the `kernel` template.

```bash
# Stage your changes
git add src/gemmit.py

# Generate the commit message
gemmit kernel
```

**2. Stage, Commit, and Push**

An end-to-end workflow: stage all files, generate and confirm the message, and push to the remote repository.

```bash
gemmit -a -p kernel
```

```
Adding all files...
--- Generated Commit Message ---
feat(gemmit): Refactor core logic for scalability

The core logic has been refactored to use a more modular
and scalable architecture. This makes it easier to add new
commands and maintain the existing codebase.
--------------------------------
Use this message? [Y]es, [E]dit, [R]egenerate, [N]o: y
[main 1234567] feat(gemmit): Refactor core logic for scalability
 1 file changed, 10 insertions(+), 5 deletions(-)
Pushing changes to origin/main...
```

### Configuration

You can customize templates and behavior by editing `~/.gemmit/config.json`.

*   **`templates`**: Define your own templates with custom prompts.
*   **`autoconfirm`**: Set to `true` to make the `-y` flag the default behavior.
*   **`highlight_color`**: Set a hex color code (e.g., `#FFA500`) for `gemmit`'s output.