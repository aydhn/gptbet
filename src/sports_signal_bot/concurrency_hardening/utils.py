import json

def write_json_artifact(filepath: str, data: dict):
    """Writes a dictionary to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
