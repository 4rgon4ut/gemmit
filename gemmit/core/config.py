# This module manages the configuration for gemmit.

import json
import os
from ..utils.errors import handle_error

CONFIG_FILE = os.path.expanduser('~/.gemmit/config.json')

def load_config():
    """Loads the configuration file, creating it if it doesn't exist."""
    if not os.path.exists(CONFIG_FILE):
        print(f"Configuration file not found at {CONFIG_FILE}. Creating a default one.")
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        default_config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(default_config_path, 'r') as src, open(CONFIG_FILE, 'w') as dest:
            dest.write(src.read())

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

def save_config(config):
    """Saves the configuration file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        handle_error(f"writing to config file at {CONFIG_FILE}", e)

def set_default_template(template_name):
    """Sets the default template in the config."""
    config = load_config()
    config['default_template'] = template_name
    save_config(config)
    print(f"Default template set to '{template_name}'.")
