from sports_signal_bot.resilience_advisor.signatures import build_failure_signature, compare_failure_signatures
from sports_signal_bot.resilience_advisor.matching import compute_pattern_similarity, find_relevant_failure_patterns
from sports_signal_bot.resilience_advisor.contracts import FailurePatternRecord

def test_signature_comparison():
    sig1 = build_failure_signature({"source_family": "odds", "swarm_agreement_status": "ok"})
    sig2 = build_failure_signature({"source_family": "odds", "swarm_agreement_status": "split"})
    score = compare_failure_signatures(sig1, sig2)
    assert score == 0.5 # One match out of two fields

def test_find_relevant_patterns():
    sig1 = build_failure_signature({"source_family": "odds", "swarm_agreement_status": "split"})
    pattern = FailurePatternRecord(
        pattern_id="p1", pattern_family="sync", incident_signature=sig1,
        trigger_conditions=[], observed_symptoms=[], root_cause_hypotheses=[],
        remediation_history=[], recovery_outcome_summary="", confidence_notes=""
    )
    matches = find_relevant_failure_patterns([pattern], {"source_family": "odds", "swarm_agreement_status": "split"})
    assert len(matches) == 1
    assert matches[0].similarity_band == "strong_match"
