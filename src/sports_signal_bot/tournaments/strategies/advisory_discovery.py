from .base import BaseTournamentStrategy
from typing import Dict, Any

class AdvisoryDiscoveryStrategy(BaseTournamentStrategy):
    """
    Exploratory candidates are more visible. Looser shortlist threshold.
    """
    def __init__(self, config: Dict[str, Any] = None):
        cfg = config or {}
        cfg.setdefault("max_blast_radius", 0.8)
        cfg.setdefault("min_support_strength", 0.2)
        cfg.setdefault("strict_blast_radius", False)
        cfg.setdefault("high_risk_blast_threshold", 0.6)
        cfg.setdefault("safe_support_threshold", 0.4)
        cfg.setdefault("advisory_support_threshold", 0.2)
        cfg.setdefault("blast_radius_penalty_weight", 2.0)
        super().__init__(cfg)
