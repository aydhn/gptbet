import yaml
from pathlib import Path
def load_config(path: str) -> dict:
    try:
        with open(path, "r") as f: return yaml.safe_load(f)
    except Exception: return {}
