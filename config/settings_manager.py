import json
import os

SETTINGS_FILE = os.path.join("config", "settings.json")


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
