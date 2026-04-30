import json
from datetime import datetime

def format_timestamp(dt: datetime) -> str:
    return dt.isoformat()
