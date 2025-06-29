
import pytest
import subprocess
import os
import json

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
    
    # Create a mock config.json
    config_data = {
        "autoconfirm": True, # Set to true to avoid interactive prompts in tests
        "templates": {
            "test": {"prompt": "A test prompt"}
        }
    }
    (gemmit_home / "config.json").write_text(json.dumps(config_data))
    
    # Create a mock gemini CLI script
    gemini_script_path = gemmit_home / "gemini"
    gemini_script_path.write_text('#!/bin/bash\necho "feat: Mocked commit message"\n')
    os.chmod(gemini_script_path, 0o755)
    
    # Symlink the real gemmit script into our mock home
    # This allows us to run the real script but control its environment
    os.symlink(os.path.abspath("src/gemmit"), gemmit_home / "gemmit")
    os.symlink(os.path.abspath("src/gemmit.py"), gemmit_home / "gemmit.py")
    os.symlink(os.path.abspath("src/commands"), gemmit_home / "commands", target_is_directory=True)
    os.symlink(os.path.abspath("src/core"), gemmit_home / "core", target_is_directory=True)
    os.symlink(os.path.abspath("src/utils"), gemmit_home / "utils", target_is_directory=True)

    
    yield gemmit_home

# --- Integration Test ---

def test_end_to_end_commit(test_repo, mock_gemmit_home):
    """Tests the full, end-to-end workflow of the gemmit tool."""
    # 1. Make a change to a file
    (test_repo / "test.txt").write_text("new content")
    
    # 2. Stage the change
    subprocess.run(["git", "add", "test.txt"], cwd=test_repo, check=True)
    
    # 3. Run the gemmit command from our mock home
    # We need to modify the PATH to ensure our mock gemini is used.
    env = os.environ.copy()
    env["PATH"] = str(mock_gemmit_home) + os.pathsep + env["PATH"]
    env["HOME"] = str(mock_gemmit_home.parent) # Make sure it finds ~/.gemmit

    gemmit_cmd = mock_gemmit_home / "gemmit"
    os.chmod(gemmit_cmd, 0o755)
    subprocess.run([str(gemmit_cmd), "test"], cwd=test_repo, check=True, env=env)
    
    # 4. Verify the commit was created with the mocked message
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"], 
        cwd=test_repo, 
        check=True, 
        capture_output=True, 
        text=True
    )
    
    assert "feat: Mocked commit message" in result.stdout.strip()
