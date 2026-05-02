from datetime import datetime
import yaml
from typing import Dict, Any

def get_utc_now() -> datetime:
    return datetime.utcnow()

def load_yaml_config(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def validate_exchange_freshness(valid_until: datetime) -> bool:
    if not valid_until:
        return True
    return valid_until > get_utc_now()

def classify_staleness_across_registries(freshness_score: float) -> str:
    if freshness_score > 0.8:
        return "fresh"
    return "stale"

def block_critical_stale_imports(freshness_score: float) -> bool:
    return freshness_score < 0.2
