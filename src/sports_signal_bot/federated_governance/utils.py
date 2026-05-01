from typing import Dict, Any

def extract_safe_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Ensure sensitive data is not leaked in logging or evidence
    safe = {}
    for k, v in payload.items():
        if "secret" not in k.lower() and "key" not in k.lower():
            safe[k] = v
    return safe
