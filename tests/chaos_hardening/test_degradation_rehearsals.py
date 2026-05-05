import pytest
from sports_signal_bot.chaos_hardening.contracts import DegradationRehearsalRecord

def test_degradation_rehearsal():
    rehearsal = DegradationRehearsalRecord(
        rehearsal_id="rh-1",
        rehearsal_family="preview_degradation_rehearsal",
        stage_refs=["stg-1"],
        fallback_refs=[],
        degradation_path_refs=[],
        residue_refs=[],
        outcome_status="degraded_honestly",
        warnings=[]
    )
    assert rehearsal.outcome_status == "degraded_honestly"
