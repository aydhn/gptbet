from sports_signal_bot.resilience_advisor.synthesis import synthesize_remediation_playbook
from sports_signal_bot.resilience_advisor.contracts import PatternSimilarityRecord

def test_synthesize_remediation_playbook():
    matches = [PatternSimilarityRecord(pattern_id="p1", similarity_score=0.9, similarity_band="strong_match", explanation="")]
    playbook = synthesize_remediation_playbook(matches, {})
    assert playbook.target_incident_family == "quarantine_recovery"
    assert len(playbook.steps) == 2
    assert playbook.steps[0].step_family == "isolate_source"
