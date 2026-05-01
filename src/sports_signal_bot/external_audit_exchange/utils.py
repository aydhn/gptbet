import json
from typing import Dict, Any

def serialize_record(record: Any) -> str:
    return record.model_dump_json()

def deserialize_record(data: str, model_class: Any) -> Any:
    return model_class.model_validate_json(data)
