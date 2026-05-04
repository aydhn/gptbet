import json

def write_manifest(manifest_data: dict, dest: str):
    with open(dest, "w") as f:
        json.dump(manifest_data, f, indent=2)
