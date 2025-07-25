import pytest
from unittest.mock import patch, mock_open
from gemmit.core import config

# A mock of the config.json file content
MOCK_CONFIG_CONTENT = """
{
    "autoconfirm": false,
    "templates": {
        "kernel": {
            "prompt": "Write a commit message in the style of a Linux kernel commit."
        },
        "conventional": {
            "prompt": "Write a conventional commit message."
        }
    }
}
"""


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_CONFIG_CONTENT)
def test_load_config(mock_file):
    """Tests that the config is loaded and parsed correctly."""
    cfg = config.load_config()
    assert cfg["autoconfirm"] is False
    assert "kernel" in cfg["templates"]


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_CONFIG_CONTENT)
def test_get_template_success(mock_file):
    """Tests retrieving an existing template."""
    template = config.get_template("kernel")
    assert (
        template["prompt"]
        == "Write a commit message in the style of a Linux kernel commit."
    )


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_CONFIG_CONTENT)
def test_get_template_not_found(mock_file):
    """Tests that a non-existent template raises an error."""
    with pytest.raises(SystemExit):
        config.get_template("nonexistent")


@patch("os.path.exists", return_value=True)
@patch("builtins.open", side_effect=FileNotFoundError)
def test_load_config_file_not_found(mock_open, mock_exists):
    """
    Tests that an error is raised if the config file is supposed to exist
    but cannot be opened.
    """
    with pytest.raises(SystemExit):
        config.load_config()
