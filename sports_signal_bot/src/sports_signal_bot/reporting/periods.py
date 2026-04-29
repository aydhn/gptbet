from datetime import datetime, timedelta
from typing import Tuple


def build_reporting_period(
    period_id: str, anchor_time: datetime = None
) -> Tuple[datetime, datetime]:
    if anchor_time is None:
        anchor_time = datetime.now()

    if period_id == "daily":
        start_time = anchor_time - timedelta(days=1)
    elif period_id == "weekly":
        start_time = anchor_time - timedelta(days=7)
    elif period_id == "slot":
        start_time = anchor_time - timedelta(hours=4)
    elif period_id == "monthly":
        start_time = anchor_time - timedelta(days=30)
    else:
        start_time = anchor_time - timedelta(hours=24)  # fallback

    return start_time, anchor_time


def summarize_period_scope(period_id: str, start: datetime, end: datetime) -> str:
    return f"{period_id.capitalize()} reporting from {start.isoformat()} to {end.isoformat()}"


def attach_period_caveats(period_id: str) -> list[str]:
    if period_id == "slot":
        return [
            "Slot metrics are highly volatile and dependent on the volume of events in the time window."
        ]
    return []
