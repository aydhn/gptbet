from .base import BaseTournamentStrategy
from typing import Dict, Any

class ProviderFocusedTournamentStrategy(BaseTournamentStrategy):
    def __init__(self, config: Dict[str, Any] = None):
        cfg = config or {}
        cfg.setdefault("required_metrics", ["provider_failover_burden", "support_strength"])
        super().__init__(cfg)
