
import json
import os
from utils.errors import handle_error

CONFIG_FILE = os.path.expanduser('~/.gemmit/config.json')

def load_config():
    """Loads the configuration file."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        handle_error(f"reading or parsing config file at {CONFIG_FILE}", e)

def get_template(template_name):
    """Gets a specific template from the config."""
    config = load_config()
    templates = config.get('templates', {})
    if template_name not in templates:
        handle_error(f"Template '{template_name}' not found in config.")
    return templates[template_name]
