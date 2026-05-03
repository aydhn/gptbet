from typing import Dict, Any, List
from .contracts import AdvisoryConfidenceRecord, PatternSimilarityRecord, RemediationPlaybookRecord

def compute_advisory_confidence(matches: List[PatternSimilarityRecord], playbook: RemediationPlaybookRecord) -> AdvisoryConfidenceRecord:
    if not matches:
         return AdvisoryConfidenceRecord(
            confidence_band="low",
            score=0.1,
            factors={"no_matches": True}
        )

    top_match = matches[0]
    score = top_match.similarity_score

    band = "moderate"
    if score > 0.8:
        band = "high"
    elif score < 0.3:
        band = "low"

    return AdvisoryConfidenceRecord(
        confidence_band=band,
        score=score,
        factors={"top_match_score": score, "playbook_steps": len(playbook.steps)}
    )

def explain_confidence_breakdown(confidence: AdvisoryConfidenceRecord) -> str:
    return f"Confidence is {confidence.confidence_band} (Score: {confidence.score:.2f})"

def cap_confidence_due_to_risk(confidence: AdvisoryConfidenceRecord, risks: List[str]) -> AdvisoryConfidenceRecord:
    if risks and confidence.confidence_band == "high":
        confidence.confidence_band = "high_with_caveats"
    return confidence

def summarize_confidence_limits(confidence: AdvisoryConfidenceRecord) -> str:
    return f"Confidence band: {confidence.confidence_band}"
