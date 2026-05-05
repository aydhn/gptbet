"""
Diffing utilities.
"""
from typing import Dict, Any

def generate_structured_diff(expected: Dict[str, Any], actual: Dict[str, Any]) -> Dict[str, Any]:
    return {"diff_type": "none" if expected == actual else "structural"}
