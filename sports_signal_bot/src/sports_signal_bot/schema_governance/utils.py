from typing import Dict, Any

def normalize_enum_value(value: str) -> str:
    return value.lower()

def map_deprecated_status(status: str) -> str:
    mapping = {
        "old_status": "new_status"
    }
    return mapping.get(status, status)

def validate_enum_compatibility(old_enum: list, new_enum: list) -> bool:
    return set(old_enum).issubset(set(new_enum))

def handle_unknown_enum_safely(value: str, fallback: str = "unknown") -> str:
    return value if value else fallback
