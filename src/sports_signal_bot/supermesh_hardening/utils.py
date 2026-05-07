import json

def read_json_artifact(filepath: str) -> dict:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return {}
