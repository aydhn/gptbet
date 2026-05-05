"""
Golden dataset management.
"""
from typing import Dict, Any

def get_golden_dataset(set_name: str) -> Dict[str, Any]:
    return {"status": "loaded", "name": set_name, "cases": []}

def check_stale_golden(golden_ref: str, age_days: int) -> bool:
    return age_days > 30
