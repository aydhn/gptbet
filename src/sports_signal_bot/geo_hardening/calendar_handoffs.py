from typing import Any, Dict


def verify_calendar_handoff(shift_from: dict, shift_to: dict) -> bool:
    if shift_from.get("end_time") != shift_to.get("start_time"):
        return False
    if not shift_to.get("owner"):
        return False
    return True


def validate_escalation_reachability(calendar: dict, escalation_path: list) -> bool:
    if not escalation_path:
        return False
    for step in escalation_path:
        if step not in calendar.get("owners", []):
            return False
    return True


def detect_ownerless_windows(schedule: list) -> list:
    windows = []
    for shift in schedule:
        if not shift.get("owner"):
            windows.append(shift.get("id"))
    return windows


def summarize_calendar_coverage(schedule: list) -> Dict[str, Any]:
    ownerless = detect_ownerless_windows(schedule)
    return {
        "total_shifts": len(schedule),
        "ownerless_shifts": len(ownerless),
        "status": "gapped" if ownerless else "verified",
    }
