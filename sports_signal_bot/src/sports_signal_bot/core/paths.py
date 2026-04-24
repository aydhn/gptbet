import os
from pathlib import Path

def get_project_root() -> Path:
    """Returns the project root directory."""
    # Assuming this file is at src/sports_signal_bot/core/paths.py
    # Root is 4 levels up
    return Path(__file__).resolve().parent.parent.parent.parent

def get_data_dir() -> Path:
    return get_project_root() / "data"

def get_configs_dir() -> Path:
    return get_project_root() / "configs"
