from sports_signal_bot.resilience_advisor.hypotheses import generate_root_cause_hypotheses
from sports_signal_bot.resilience_advisor.contracts import PatternSimilarityRecord

def test_generate_hypotheses_strong_match():
    matches = [
        PatternSimilarityRecord(
            pattern_id="p1",
            similarity_score=0.95,
            similarity_band="strong_match",
            explanation="Very similar"
        )
    ]
    hypotheses = generate_root_cause_hypotheses(matches, {})
    assert len(hypotheses) == 1
    assert hypotheses[0].hypothesis_id == "hyp_p1"
    assert hypotheses[0].confidence_score == 0.95
    assert hypotheses[0].hypothesis_family == "likely_source_freshness_issue"
    assert hypotheses[0].support_signals == ["pattern_match"]

def test_generate_hypotheses_highly_relevant():
    matches = [
        PatternSimilarityRecord(
            pattern_id="p2",
            similarity_score=0.85,
            similarity_band="highly_relevant_match",
            explanation="Relevant"
        )
    ]
    hypotheses = generate_root_cause_hypotheses(matches, {})
    assert len(hypotheses) == 1
    assert hypotheses[0].hypothesis_id == "hyp_p2"
    assert hypotheses[0].confidence_score == 0.85

def test_generate_hypotheses_ignores_weak_matches():
    matches = [
        PatternSimilarityRecord(
            pattern_id="p3",
            similarity_score=0.5,
            similarity_band="weak_match",
            explanation="Not very similar"
        ),
        PatternSimilarityRecord(
            pattern_id="p4",
            similarity_score=0.2,
            similarity_band="no_match",
            explanation="No match"
        )
    ]
    hypotheses = generate_root_cause_hypotheses(matches, {})
    assert len(hypotheses) == 0

def test_generate_hypotheses_mixed_matches():
    matches = [
        PatternSimilarityRecord(
            pattern_id="p1",
            similarity_score=0.9,
            similarity_band="strong_match",
            explanation="Very similar"
        ),
        PatternSimilarityRecord(
            pattern_id="p2",
            similarity_score=0.4,
            similarity_band="weak_match",
            explanation="Not similar"
        ),
        PatternSimilarityRecord(
            pattern_id="p3",
            similarity_score=0.8,
            similarity_band="highly_relevant_match",
            explanation="Relevant"
        )
    ]
    hypotheses = generate_root_cause_hypotheses(matches, {})
    assert len(hypotheses) == 2
    assert hypotheses[0].hypothesis_id == "hyp_p1"
    assert hypotheses[1].hypothesis_id == "hyp_p3"
