from typing import Dict, Any, List
from sports_signal_bot.dynamic_weighting.contracts import WeightComponentRecord

def compute_base_prior(source_family: str, market_type: str, config: Dict[str, Any]) -> float:
    # config format: {'market_type': {'family': weight}}
    market_config = config.get(market_type, {})
    default_config = config.get('default', {})

    prior = market_config.get(source_family, default_config.get(source_family, 1.0))
    return float(prior)

def compute_trust_weight_component(trust_score: float, damping: float = 1.0) -> float:
    return trust_score * damping

def compute_regime_weight_component(regime_fit: float, sample_size: int, damping_factor: float = 0.5) -> float:
    # If sample size is small, move towards 0 (neutral effect if additive)
    effective_regime = regime_fit * (1.0 - damping_factor / max(1, sample_size))
    return max(0.0, effective_regime)

def compute_disagreement_component(source_prob: float, peer_probs: List[float], min_peers: int = 3, penalty_weight: float = 1.0) -> float:
    if len(peer_probs) < min_peers:
        return 0.0

    avg_peer_prob = sum(peer_probs) / len(peer_probs)
    diff = abs(source_prob - avg_peer_prob)

    # Mild penalty for high disagreement
    if diff > 0.15:
        return -diff * penalty_weight
    return 0.0

def compute_recency_component(is_stale: bool, penalty_weight: float = 0.5) -> float:
    return -penalty_weight if is_stale else 0.0

def combine_weight_components(
    trust: float, regime: float, disagreement: float, recency: float,
    health: float, prior: float, bonus: float, policy: Any
) -> WeightComponentRecord:

    combined = (
        prior +
        (trust * policy.trust_component_weight) +
        (regime * policy.regime_component_weight) +
        (disagreement * policy.disagreement_penalty_weight) +
        (recency * policy.recency_penalty_weight) +
        (health * policy.health_component_weight) +
        bonus
    )

    return WeightComponentRecord(
        trust_score=trust,
        regime_fit_score=regime,
        disagreement_penalty=disagreement,
        recency_penalty=recency,
        health_score=health,
        family_prior=prior,
        calibration_bonus=bonus,
        combined_score=max(0.0, combined), # Ensure no negative combined score
        explanation=f"Combined: {combined:.2f} (Prior:{prior:.2f}, Trust:{trust:.2f}, Regime:{regime:.2f})"
    )
