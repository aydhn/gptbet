"""
Summary generation logic.
"""
from typing import Dict, Any
import json

def format_hardening_summary(data: Dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True)
