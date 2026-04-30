# Module for manifest serialization/deserialization for staged channels
import json
from typing import List, Dict, Any

def read_manifest(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_manifest(path: str, data: List[Dict[str, Any]]):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
