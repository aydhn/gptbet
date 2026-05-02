import json

def write_json(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
