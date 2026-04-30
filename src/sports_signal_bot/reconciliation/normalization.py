
from typing import Any

def canonicalize_field_value(field_name: str, value: Any) -> Any:
    return value

def normalize_timestamp_field(value: Any) -> Any:
    return value

def normalize_status_field(value: Any) -> Any:
    if isinstance(value, str):
        val = value.lower()
        if val in ["finished", "ended", "ft"]: return "finished"
        if val in ["cancelled", "canceled", "canc"]: return "cancelled"
    return value

def normalize_selection_labels(value: Any) -> Any:
    return value

def normalize_score_payload(value: Any) -> Any:
    return value

def normalize_team_name_field(value: Any) -> Any:
    return value
