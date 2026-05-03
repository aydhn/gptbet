from sports_signal_bot.resilience_advisor.memory import FailurePatternMemory
from sports_signal_bot.resilience_advisor.contracts import FailurePatternRecord, FailureSignatureRecord

def test_pattern_storage():
    memory = FailurePatternMemory()
    sig = FailureSignatureRecord(source_family="test", event_families=["fb"])
    pattern = FailurePatternRecord(
        pattern_id="p1", pattern_family="sync", incident_signature=sig,
        trigger_conditions=[], observed_symptoms=[], root_cause_hypotheses=[],
        remediation_history=[], recovery_outcome_summary="", confidence_notes=""
    )
    memory.store_failure_pattern(pattern)
    assert len(memory.get_all_patterns()) == 1

def test_summarize_coverage():
    memory = FailurePatternMemory()
    sig = FailureSignatureRecord()
    pattern = FailurePatternRecord(
        pattern_id="p1", pattern_family="sync", incident_signature=sig,
        trigger_conditions=[], observed_symptoms=[], root_cause_hypotheses=[],
        remediation_history=[], recovery_outcome_summary="", confidence_notes=""
    )
    memory.store_failure_pattern(pattern)
    cov = memory.summarize_pattern_memory_coverage()
    assert cov.get("sync") == 1
