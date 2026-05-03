from sports_signal_bot.resilience_advisor.confidence import compute_advisory_confidence
from sports_signal_bot.resilience_advisor.contracts import PatternSimilarityRecord, RemediationPlaybookRecord

def test_compute_confidence():
    matches = [PatternSimilarityRecord(pattern_id="p1", similarity_score=0.9, similarity_band="strong_match", explanation="")]
    playbook = RemediationPlaybookRecord(
        playbook_id="pb1", playbook_family="test", target_incident_family="test",
        synthesized_from_pattern_refs=[], steps=[], prerequisites=[],
        risk_notes=[], rollback_notes=[], expected_signals=[]
    )
    conf = compute_advisory_confidence(matches, playbook)
    assert conf.confidence_band == "high"
