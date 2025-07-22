import pytest
import subprocess
import os
import json
import sys
import shutil

# --- Test Setup and Fixtures ---

@pytest.fixture
def test_repo(tmp_path):
    """Creates a temporary git repository for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    
    # Initialize Git repo
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)
    
    # Create a dummy file
    (repo_path / "test.txt").write_text("initial content")
    subprocess.run(["git", "add", "test.txt"], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)
    
    yield repo_path
    
    # Cleanup is handled by tmp_path fixture

@pytest.fixture
def mock_gemmit_home(tmp_path):
    """Creates a mock ~/.gemmit directory."""
    gemmit_home = tmp_path / ".gemmit"
    gemmit_home.mkdir()

    # Install the gemmit package in editable mode
    subprocess.run([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-e",
        ".",
    ], check=True, cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Create a mock config.json
    config_data = {
        "autoconfirm": False, # Set to false to trigger interactive prompt
        "templates": {
            "test": {"prompt": "A test prompt"}
        }
    }
    (gemmit_home / "config.json").write_text(json.dumps(config_data))
    
    # Create a mock gemini CLI script
    gemini_script_path = gemmit_home / "gemini"
    gemini_script_path.write_text('#!/bin/bash\necho "feat: Mocked commit message"\n')
    os.chmod(gemini_script_path, 0o755)

    
    yield gemmit_home


# --- Integration Tests ---

def test_end_to_end_commit_autoconfirm(test_repo, mock_gemmit_home):
    """Tests the full, end-to-end workflow with autoconfirm=true."""
    # Set autoconfirm to true for this test
    config_path = mock_gemmit_home / "config.json"
    with open(config_path, "r+") as f:
        data = json.load(f)
        data["autoconfirm"] = True
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    (test_repo / "test.txt").write_text("new content for autoconfirm")
    subprocess.run(["git", "add", "test.txt"], cwd=test_repo, check=True)
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + os.pathsep + env.get("PYTHONPATH", "")
    env["PATH"] = str(mock_gemmit_home) + os.pathsep + env["PATH"]
    env["HOME"] = str(mock_gemmit_home.parent)

    gemmit_cmd = shutil.which('gemmit')
    assert gemmit_cmd, "gemmit executable not found in PATH"
    subprocess.run([str(gemmit_cmd), "test", "-y"], cwd=test_repo, check=True, env=env)
    
    result = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=test_repo, check=True, capture_output=True, text=True)
    assert "feat: Mocked commit message" in result.stdout.strip()

def test_end_to_end_commit_edit(test_repo, mock_gemmit_home):
    """Tests the interactive edit workflow."""
    (test_repo / "test.txt").write_text("new content for edit test")
    subprocess.run(["git", "add", "test.txt"], cwd=test_repo, check=True)
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + os.pathsep + env.get("PYTHONPATH", "")
    env["PATH"] = str(mock_gemmit_home) + os.pathsep + env["PATH"]
    env["HOME"] = str(mock_gemmit_home.parent)
    # Create a mock editor script
    editor_script_path = mock_gemmit_home / "mock_editor.py"
    editor_script_path.write_text("""
import sys
file_path = sys.argv[1]
with open(file_path, 'r') as f:
    content = f.read()
content = content.replace('Mocked', 'Edited')
with open(file_path, 'w') as f:
    f.write(content)
""")
    env["EDITOR"] = f"python3 {editor_script_path}"

    gemmit_cmd = shutil.which('gemmit')
    assert gemmit_cmd, "gemmit executable not found in PATH"
    
    # We pipe 'e' for edit into the script's stdin
    subprocess.run([str(gemmit_cmd), "test"], cwd=test_repo, check=True, env=env, input="e\n", text=True)
    
    result = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=test_repo, check=True, capture_output=True, text=True)
    assert "feat: Edited commit message" in result.stdout.strip()