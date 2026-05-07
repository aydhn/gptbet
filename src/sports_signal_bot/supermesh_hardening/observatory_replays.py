from typing import List
from .contracts import HandoffObservatoryReplayRecord, HandoffObservatoryWindowRecord, HandoffObservatoryGapRecord

def verify_handoff_observatory_window(window: HandoffObservatoryWindowRecord) -> bool:
    return not window.is_ownerless

def diff_handoff_observatory_replay(replay: HandoffObservatoryReplayRecord) -> List[str]:
    diffs = []
    if replay.is_stale:
        diffs.append("Stale replay")
    if not replay.no_safe_preserved:
        diffs.append("No-safe visibility lost in replay")
    if not replay.sovereignty_preserved:
        diffs.append("Sovereignty visibility lost in replay")
    return diffs

def replay_handoff_observatory(replay: HandoffObservatoryReplayRecord) -> bool:
    diffs = diff_handoff_observatory_replay(replay)
    return len(diffs) == 0

def detect_handoff_observatory_gaps(windows: List[HandoffObservatoryWindowRecord], gaps: List[HandoffObservatoryGapRecord]) -> List[str]:
    detected = []
    for w in windows:
        if w.is_ownerless:
            detected.append(f"Gap: Ownerless window {w.window_id}")
    for g in gaps:
        if g.is_hidden:
            detected.append(f"Gap: Hidden observatory gap {g.gap_id}")
        else:
            detected.append(f"Gap: Explicit observatory gap {g.gap_id}")
    return detected

def summarize_handoff_observatory_windows(windows: List[HandoffObservatoryWindowRecord]) -> dict:
    return {
        "total_windows": len(windows),
        "ownerless_windows": sum(1 for w in windows if w.is_ownerless)
    }
