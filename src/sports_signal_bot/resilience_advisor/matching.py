from typing import List, Dict, Any
from .contracts import FailurePatternRecord, PatternSimilarityRecord, PatternMatchRecord, FailureSignatureRecord
from .signatures import build_failure_signature, compare_failure_signatures, explain_signature_similarity

def compute_pattern_similarity(incident_sig: FailureSignatureRecord, pattern: FailurePatternRecord) -> PatternSimilarityRecord:
    score = compare_failure_signatures(incident_sig, pattern.incident_signature)

    if score > 0.8:
        band = "strong_match"
    elif score > 0.5:
        band = "plausible_match"
    else:
        band = "weak_match"

    return PatternSimilarityRecord(
        pattern_id=pattern.pattern_id,
        similarity_score=score,
        similarity_band=band,
        explanation=explain_signature_similarity(incident_sig, pattern.incident_signature)
    )

def find_relevant_failure_patterns(patterns: List[FailurePatternRecord], incident_signals: Dict[str, Any]) -> List[PatternSimilarityRecord]:
    incident_sig = build_failure_signature(incident_signals)
    results = []
    for p in patterns:
        sim = compute_pattern_similarity(incident_sig, p)
        if sim.similarity_score > 0.2:
            results.append(sim)
    return results

def penalize_stale_or_conflicting_patterns(similarities: List[PatternSimilarityRecord]) -> List[PatternSimilarityRecord]:
    # Placeholder for penalty logic
    return similarities

def rank_pattern_matches(similarities: List[PatternSimilarityRecord]) -> List[PatternSimilarityRecord]:
    return sorted(similarities, key=lambda x: x.similarity_score, reverse=True)

def summarize_pattern_match_quality(match_record: PatternMatchRecord) -> str:
    return f"Top match band: {match_record.top_match_band} with {len(match_record.matches)} matches."
