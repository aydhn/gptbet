from typing import List
from .contracts import CatchupWindowRecord, SlotScheduleRecord
import datetime

def evaluate_catchup_needs(policy_name: str, missed_slots: List[SlotScheduleRecord], current_time: datetime.datetime) -> CatchupWindowRecord:
    valid_slots = []
    relevance_window = 24 if policy_name == "daily_summary_backfill" else 4
    if policy_name == "no_catchup":
        return CatchupWindowRecord(policy_name=policy_name, missed_slots=[], relevance_window_hours=0)

    for slot in missed_slots:
        slot_dt = datetime.datetime.combine(slot.date, slot.start_time)
        hours_diff = (current_time - slot_dt).total_seconds() / 3600
        if hours_diff <= relevance_window:
            valid_slots.append(slot.slot_id)

    return CatchupWindowRecord(
        policy_name=policy_name,
        missed_slots=valid_slots,
        relevance_window_hours=relevance_window
    )
