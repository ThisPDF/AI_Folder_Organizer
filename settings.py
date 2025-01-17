import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")

# Default settings
default_settings = {
    "theme": "dark"
}

def load_settings():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# Initialize settings
settings = load_settings()
