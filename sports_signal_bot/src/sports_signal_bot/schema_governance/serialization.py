import json
from typing import Dict, Any

def serialize_versioned_payload(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, default=str)

def deserialize_versioned_payload(data: str) -> Dict[str, Any]:
    return json.loads(data)

def canonicalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return json.loads(json.dumps(payload, sort_keys=True, default=str))
