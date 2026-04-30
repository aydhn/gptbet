def load_yaml_config(path: str) -> dict:
    import yaml
    import os
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f)
