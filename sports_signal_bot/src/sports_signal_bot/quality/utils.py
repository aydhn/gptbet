from typing import Dict, Any, List

def normalize_dynamic_fields(data: Any, dynamic_keys: List[str]) -> Any:
    """Recursively normalizes dynamic fields like timestamps or run_ids for golden comparison."""
    if isinstance(data, dict):
        normalized = {}
        for k, v in data.items():
            if k in dynamic_keys:
                normalized[k] = "<NORMALIZED>"
            else:
                normalized[k] = normalize_dynamic_fields(v, dynamic_keys)
        return normalized
    elif isinstance(data, list):
        return [normalize_dynamic_fields(item, dynamic_keys) for item in data]
    return data

def compare_with_tolerance(actual: float, expected: float, tolerance: float = 1e-5) -> bool:
    return abs(actual - expected) <= tolerance

def stable_sort_records_for_compare(records: List[Dict[str, Any]], sort_key: str) -> List[Dict[str, Any]]:
    return sorted(records, key=lambda x: str(x.get(sort_key, "")))
