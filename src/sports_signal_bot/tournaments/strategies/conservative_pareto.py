from .base import BaseTournamentStrategy
from typing import Dict, Any

class ConservativeParetoStrategy(BaseTournamentStrategy):
    """
    Strong safety filters, low-risk shortlist bias. Default ops strategy.
    """
    def __init__(self, config: Dict[str, Any] = None):
        cfg = config or {}
        cfg.setdefault("max_blast_radius", 0.2)
        cfg.setdefault("min_support_strength", 0.8)
        cfg.setdefault("strict_blast_radius", True)
        cfg.setdefault("high_risk_blast_threshold", 0.1)
        cfg.setdefault("safe_support_threshold", 0.85)
        cfg.setdefault("advisory_support_threshold", 0.8)
        cfg.setdefault("blast_radius_penalty_weight", 20.0)
        super().__init__(cfg)
