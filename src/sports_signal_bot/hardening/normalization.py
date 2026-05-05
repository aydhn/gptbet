"""
Normalization utilities.
"""
from typing import Dict, Any

def normalize_text_ordering(data: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(data, dict):
        return {k: normalize_text_ordering(v) for k, v in sorted(data.items())}
    if isinstance(data, list):
        try:
            return sorted(normalize_text_ordering(v) for v in data)
        except TypeError:
            return [normalize_text_ordering(v) for v in data]
    return data
