from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import uuid
from .contracts import (
    ExpansionWaveRecord, ExpansionWaveStatus, WaveCooldownRecord, FamilySequencingRecord
)

def validate_wave_coordination(
    wave: ExpansionWaveRecord,
    active_waves: List[ExpansionWaveRecord],
    cooldowns: List[WaveCooldownRecord],
    sequencing: List[FamilySequencingRecord],
    max_overlap: int = 2
) -> Tuple[bool, str]:
    """Checks if a new wave can be admitted based on coordination policies."""

    # 1. Overlap Check
    if len(active_waves) >= max_overlap:
         return False, f"Cannot admit wave: Max overlap of {max_overlap} active waves reached."

    # 2. Cooldown Check
    for cd in cooldowns:
        if datetime.utcnow() < cd.ends_at:
             # Check if cooldown applies generally or specifically to this wave's families
             return False, f"Wave admission blocked by active cooldown ending at {cd.ends_at}."

    # 3. Sequencing Check
    for seq in sequencing:
         for i in range(1, len(seq.family_order)):
             current_fam = seq.family_order[i]
             prev_fam = seq.family_order[i-1]

             if current_fam in wave.target_families:
                 # In a real implementation, we'd check if prev_fam has stabilized.
                 # Mocking check: if prev_fam is in active waves, it hasn't stabilized.
                 prev_is_active = any(prev_fam in w.target_families for w in active_waves)
                 if prev_is_active:
                     return False, f"Sequencing violation: Family '{prev_fam}' must stabilize before '{current_fam}' can activate."

    return True, "Wave coordination checks passed."

def apply_wave_cooldowns(wave_id: str, duration_hours: int = 24) -> WaveCooldownRecord:
    """Creates a cooldown period preventing immediate subsequent waves, e.g., after a rollback."""
    return WaveCooldownRecord(
        cooldown_id=f"cd_{uuid.uuid4().hex[:8]}",
        wave_id=wave_id,
        ends_at=datetime.utcnow() + timedelta(hours=duration_hours)
    )

def summarize_wave_scheduler_pressure(active_waves: List[ExpansionWaveRecord], pending_waves: int) -> str:
    """Summarizes current wave scheduling load."""
    active_count = len(active_waves)
    high_concurrency = sum(1 for w in active_waves if w.concurrency_level > 5)

    return f"Active Waves: {active_count} (High Concurrency: {high_concurrency}). Pending: {pending_waves}."

def check_wave_admission_against_budget(wave: ExpansionWaveRecord, global_budget_remaining: float) -> Tuple[bool, str]:
    if wave.budget_cost > global_budget_remaining:
        return False, f"Wave cost ({wave.budget_cost}) exceeds global budget remaining ({global_budget_remaining})."
    return True, "Budget sufficient."
