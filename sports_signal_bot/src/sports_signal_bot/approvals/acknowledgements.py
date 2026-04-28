import uuid
from datetime import datetime, timezone
from sports_signal_bot.approvals.contracts import AlarmAckRecord, AcknowledgementSummary

def acknowledge_alert(alarm_id: str, operator_id: str, note: str, resolved: bool = False) -> AlarmAckRecord:
    return AlarmAckRecord(
        ack_id=f"ack_{uuid.uuid4().hex[:8]}",
        alarm_id=alarm_id,
        operator_id=operator_id,
        note=note,
        resolved=resolved
    )

def summarize_unacked_criticals(acks: list[AlarmAckRecord], total_critical: int) -> AcknowledgementSummary:
    # A simplified stub for summarizing
    resolved_count = sum(1 for ack in acks if ack.resolved)
    unacked = max(0, total_critical - resolved_count)
    return AcknowledgementSummary(
        summary_id=f"asum_{uuid.uuid4().hex[:8]}",
        unacked_critical_alarms=unacked,
        recent_acks=acks[-10:] # last 10
    )
