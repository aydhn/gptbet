def export_manifest(manifest, path: str):
    import json
    with open(path, "w") as f:
        f.write(manifest.json())
