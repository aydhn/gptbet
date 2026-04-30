from .base import BaseTournamentStrategy
from typing import Dict, Any

class PolicyFocusedTournamentStrategy(BaseTournamentStrategy):
    def __init__(self, config: Dict[str, Any] = None):
        cfg = config or {}
        cfg.setdefault("required_metrics", ["decision_quality_delta", "no_bet_burden_delta"])
        super().__init__(cfg)
