# utils.py
from datetime import datetime, timezone


def is_expired(valid_until: datetime) -> bool:
    return datetime.now(timezone.utc) > valid_until
