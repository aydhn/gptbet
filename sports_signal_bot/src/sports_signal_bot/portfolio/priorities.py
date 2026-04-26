from typing import List
from sports_signal_bot.portfolio.contracts import PortfolioCandidateRecord, PortfolioConfig

def compute_allocation_priority(candidate: PortfolioCandidateRecord, config: PortfolioConfig) -> float:
    # Base score
    score = candidate.signal_score * 10.0

    # Edge boost
    score += candidate.edge_estimate * 100.0

    # Confidence & Uncertainty
    score += candidate.confidence * 2.0
    score -= candidate.uncertainty * 5.0
    score -= candidate.disagreement * 2.0
    score += candidate.data_quality_score * 1.0

    # Action Class Tier
    if candidate.action_class == "approved_candidate":
        score *= config.approved_priority_multiplier
    elif candidate.action_class == "candidate":
        score *= config.candidate_priority_multiplier

    # Ensure positive
    return max(0.1, score)

def rank_candidates_within_bucket(candidates: List[PortfolioCandidateRecord], config: PortfolioConfig) -> List[PortfolioCandidateRecord]:
    # Add priority score dynamically or just sort based on a tuple
    return sorted(
        candidates,
        key=lambda c: (
            compute_allocation_priority(c, config),
            1.0 - c.uncertainty,
            c.data_quality_score,
            -c.event_datetime_utc.timestamp(), # earlier is better tie-breaker
            c.event_id
        ),
        reverse=True
    )
