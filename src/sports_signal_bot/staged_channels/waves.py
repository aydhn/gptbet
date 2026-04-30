import uuid
import datetime
from typing import List, Dict
from sports_signal_bot.staged_channels.contracts import RolloutWaveRecord

def build_rollout_wave(candidates: List[str], target_channel: str, capacity_budget: Dict[str, int]) -> RolloutWaveRecord:
    return RolloutWaveRecord(
        wave_id=f"wave_{uuid.uuid4().hex[:8]}",
        included_candidates=candidates,
        target_channel=target_channel,
        start_time=datetime.datetime.now(datetime.timezone.utc),
        evaluation_window_hours=24,
        capacity_budget=capacity_budget
    )

def validate_wave_coherence(wave: RolloutWaveRecord) -> bool:
    if len(wave.included_candidates) == 0:
        return False
    return True

def summarize_wave_pressure(wave: RolloutWaveRecord) -> dict:
    return {
        "candidate_count": len(wave.included_candidates),
        "target_channel": wave.target_channel
    }
