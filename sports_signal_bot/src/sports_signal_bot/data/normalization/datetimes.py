from datetime import datetime, timezone
from dateutil import parser

def parse_datetime_to_utc(date_str: str) -> datetime:
    """Parses a datetime string and returns a UTC aware datetime."""
    try:
        dt = parser.parse(date_str)
        if dt.tzinfo is None:
            # Assume UTC if no timezone is provided
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            # Convert to UTC
            dt = dt.astimezone(timezone.utc)
        return dt
    except Exception as e:
        raise ValueError(f"Could not parse datetime string: {date_str}") from e
