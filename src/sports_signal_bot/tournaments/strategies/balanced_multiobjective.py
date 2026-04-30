from .base import BaseTournamentStrategy
from typing import Dict, Any

class BalancedMultiObjectiveStrategy(BaseTournamentStrategy):
    """
    Balanced objective set. Pareto + secondary ranking. Default strategy.
    """
    def __init__(self, config: Dict[str, Any] = None):
        cfg = config or {}
        cfg.setdefault("max_blast_radius", 0.5)
        cfg.setdefault("min_support_strength", 0.5)
        cfg.setdefault("strict_blast_radius", True)
        cfg.setdefault("high_risk_blast_threshold", 0.3)
        cfg.setdefault("safe_support_threshold", 0.6)
        cfg.setdefault("advisory_support_threshold", 0.5)
        cfg.setdefault("blast_radius_penalty_weight", 10.0)
        cfg.setdefault("support_weight", 5.0)
        super().__init__(cfg)
